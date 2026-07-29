"""Aplicacao demonstravel minima com borda/sair e navegacao minima
(H-0008 / H-0009 / H-0010A / H-0022 / H-0023).

Ponto de entrada executavel da demonstracao. Exercita a API entregue pelo
renderer (``renderizar_tela``) sobre a tela raiz demonstrativa e a tela
destino minima, permitindo abrir a tela destino via chip do lancador e
voltar via Esc.

H-0039 / ADR-0030: a borda e os chips derivam de ``config/estilo.json``
via ``carregar_estilo`` (carregado uma vez em ``main``). O comando ``b``
(alternancia de borda) foi removido.

Executavel via: python demo/demo.py

Encadeamento do pipeline:

    config/telas/demo/<id_tela>.json
        -> carregar_tela(None, id_tela, raiz_telas)  [tela/loader.py       - H-0001]
        -> construir_modelo(tela_raw)                [tela/modelo.py       - H-0002]
        -> ModeloTela
        -> renderizar_tela(modelo, estilo)           [tela/renderizador.py - H-0006/H-0007/H-0009/H-0010A]
        -> str

ESCOPO (H-0008):
- Aplicacao demonstravel local minima, separada de tela/diagnostico.py.
- Aceita o comando interno ``s`` para sair (atalho auxiliar para pipe).
- O comando ``s`` e interno da demo: nao e binding declarativo, nao e
  registry de acao.

ADICOES DO H-0009:
- Largura visual lida do terminal via ``shutil.get_terminal_size``.
- Deteccao de TTY via ``sys.stdin.isatty() and sys.stdout.isatty()``:
  - Em TTY: leitura por tecla unica em modo cbreak (``termios``/``tty``),
    sem Enter e sem echo; ISIG preservado (Ctrl+C gera KeyboardInterrupt
    capturado silenciosamente no loop); ``Esc`` sai; terminal restaurado
    em ``finally``.
  - Fora de TTY (pipe/teste): leitura linha a linha preservada, com
    ``s`` e ``"\\x1b"`` como comandos de saida.
- ``processar_comando`` aceita ``"\\x1b"`` como saida;
  ``"s"`` permanece como atalho auxiliar.
- ``renderizar_estado`` aceita ``largura`` opcional repassada ao
  renderer.

ADICOES DO H-0010A (navegacao minima local):
- Estado ganha ``tela_atual`` (default ``"demo"``) e
  ``pilha_telas`` (default ``[]``).
- ``processar_comando`` ganha terceiro argumento opcional ``modelo=None``;
  quando ``modelo`` e fornecido e o comando coincide com o ``chip`` de
  algum item de lancador declarado em ``corpo.elementos[]``, a tela
  atual e empilhada em ``pilha_telas`` e ``tela_atual`` passa a ser o
  ``tela_destino`` do item.
- ``Esc`` com ``pilha_telas`` nao vazia faz pop e volta para a tela
  anterior; ``Esc`` com pilha vazia define ``saindo = True`` (sai).
- A decisao Sair/Voltar depende apenas do estado da pilha -- nao depende
  de id de tela hardcoded. O texto do chip Esc (``"Sair"`` ou
  ``"Voltar"``) vem do JSON; o comportamento (sair ou voltar) vem do
  estado da demo.
- ``main()`` recarrega o modelo via ``carregar_tela(_RAIZ_TELAS_DEMO, tela_atual)``
  sempre que ``tela_atual`` muda; renderiza apos alternar borda ou
  mudar de tela.
- Nao implementa registry completo de telas nem registry completo de
  acoes; nao faz descoberta automatica ampla.

ADICOES DO H-0022 (correcao da sessao TUI conforme ADR-0016):
- Modo cbreak (``tty.setcbreak``) em vez de raw: preserva OPOST e ISIG,
  eliminando progressao diagonal de linhas e permitindo Ctrl+C escopado.
- Alternate screen com autowrap desativado (``\\x1b[?7l``) na entrada;
  restauracao de autowrap (``\\x1b[?7h``) na saida.
- Limpeza de tela (ESC[2J) exatamente uma vez, na entrada da sessao.
- Redesenho por posicionamento absoluto linha a linha (``CSI n;1H``):
  sem dependencia de ``\\n`` para retorno de coluna.
- Escrita atomica por quadro: synchronized output (``\\x1b[?2026h/l``) em
  volta de cada quadro; conteudo inteiro emitido em uma unica chamada
  ``write()`` + ``flush()``.
- ``captura_interrupcao_de_script``: context manager reutilizavel que
  captura ``KeyboardInterrupt`` localmente, para uso futuro ao redor de
  chamadas a scripts/processos internos. Nao esta em uso na UI atual
  (nenhum fluxo de execucao de script existe ainda).
- ``KeyboardInterrupt`` fora desse mecanismo (loop principal) e capturado
  e ignorado silenciosamente: sessao TUI permanece ativa.
- ``finally`` cobre restauracao completa em toda saida do loop principal.

ADICOES DO H-0023 (redimensionamento reativo -- ADR-0017):
- SIGWINCH em sessao TTY ativa detecta alteracao de tamanho da janela.
- Wakeup pipe: handler minimo escreve um byte; loop principal usa
  select duplo (stdin + pipe) para acordar sem bloquear.
- Cadeia de obtencao: ioctl(TIOCGWINSZ) -> LINES/COLUMNS -> fallback
  fixo (80,24) na inicializacao; ultimas dimensoes validas apos resize.
- Par valido: ambos inteiros positivos; largura e altura sempre atualizados
  juntos; fontes nunca misturadas.
- Redesenho somente quando novo par valido difere do estado atual.
- Quadro minimo de aviso quando terminal pequeno demais; recuperacao
  automatica sem acao do usuario quando dimensoes voltam a ser suficientes.
- ``_iniciar_sessao_tui`` com rollback interno completo (auxiliar visual
  ``_restaurar_efeitos_visuais_tui`` reutilizada no encerramento normal).
- Sentinelas de aquisicao; cleanup condicional; excecao primaria preservada.

A apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

import fcntl
import os
import select
import shutil
import signal
import struct
import termios
import tty

from tela.loader import (
    carregar_tela,
    carregar_conteudo_externo,
    carregar_estilo,
)
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import (
    renderizar_tela,
    RenderizadorErro,
    DESCONTO_ESTRUTURAL_CONSOLE,
)
from tela import navegacao
from tela import selecao
from tela import resultado_execucao as resultado_execucao_mod

LARGURA_MINIMA_TELA = 10
ALTURA_MINIMA_TELA = 6

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")

# H-0036 / ADR-0026 / ADR-0027: catalogo interno de associacao entre cenario e
# documento externo de conteudo. A associacao pertence ao ponto de entrada
# (demo.py), NUNCA ao JSON estrutural da tela (sem campo de vinculo). Cada chave
# e o id da tela estrutural; o valor e o id (nome base) do documento externo de
# conteudo na mesma raiz de demonstracao. A AUSENCIA de conteudo externo e
# representada explicitamente pela AUSENCIA da chave (nao herdada, nao implicita):
# cenarios fora deste dict preservam o placeholder "(console)".
_CATALOGO_CONTEUDO_EXTERNO = {
    "h0036_console_hierarquia": "h0036_hierarquia_conteudo",
    "h0036_console_tabela": "h0036_tabela_conteudo",
    "h0036_console_conjuntos": "h0036_conjuntos_conteudo",
    "h0035_console_com": "h0035_console_com_conteudo",
    "h0035_console_sem": "h0035_console_sem_conteudo",
    # H-0037 / ADR-0028: cenarios de politica de modo por tela.
    # Cenarios 1 e 2 compartilham o mesmo documento externo.
    "h0037_console_nao_verboso": "h0037_dois_niveis_conteudo",
    "h0037_console_verboso_dois_niveis": "h0037_dois_niveis_conteudo",
    "h0037_console_alternavel_tres_niveis": "h0037_tres_niveis_conteudo",
    "h0037_console_tabela_alternavel": "h0037_tabela_conteudo",
}

# H-0043 / ADR-0036: cenarios da tela padrao de resultado. Todos resolvem para
# a mesma tela estrutural ``resultado_execucao``; o valor e o nome-base da
# fixture de documento de runtime em ``demo/fixtures/``. A associacao nao
# vive no JSON estrutural e nao usa ``_CATALOGO_CONTEUDO_EXTERNO``.
_CATALOGO_CENARIOS_RESULTADO_EXECUCAO = {
    "h0043_resultado_sucesso": "h0043_resultado_sucesso",
    "h0043_resultado_parcial": "h0043_resultado_parcial",
    "h0043_resultado_falha_semantica": "h0043_resultado_falha_semantica",
    "h0043_envelope_falha_operacional": "h0043_envelope_falha_operacional",
    "h0043_envelope_resultado_invalido": "h0043_envelope_resultado_invalido",
    "h0043_envelope_interrupcao": "h0043_envelope_interrupcao",
}

_ID_TELA_RESULTADO_EXECUCAO = "resultado_execucao"
_DIR_FIXTURES_DEMO = os.path.join("demo", "fixtures")


def criar_estado_inicial():
    """Retorna o estado inicial da demonstracao.

    Retorna sempre um novo dict independente a cada chamada, sem estado
    global mutavel, sem leitura de arquivo, JSON ou sys.stdin. Campos:

    - ``saindo``: ``False``.
    - ``tela_atual``: ``"demo"`` (tela raiz da demonstracao).
    - ``pilha_telas``: ``[]`` (sem telas empilhadas).
    - ``modo_verboso``: ``False`` (alternancia de verbosidade, H-0037).

    H-0039 / ADR-0030: o estado nao carrega mais ``tipo_borda`` -- a borda
    vem de ``config/estilo.json`` via ``carregar_estilo`` e o ``EstiloResolvido``
    e injetado em ``estado`` pelo ``main`` (uma vez por sessao).

    H-0040 / ADR-0031: campos de runtime de navegacao -- ``foco_console``
    (indice do console focado na lista de foco, ou ``None``) e ``cursores``
    (dict id-do-console -> item logico corrente). Sao EXCLUSIVAMENTE runtime:
    nao persistem em JSON, nao alteram schema (NC-005). ``foco_console=None``
    significa "sem foco estabelecido ainda"; Tab/Shift+Tab o estabelecem.

    H-0041 / ADR-0034: campo de runtime de selecao multipla -- ``selecoes``
    (dict id-do-console -> lista de IDs marcados). EXCLUSIVAMENTE runtime,
    independente do cursor (D-SEL-01). Inicialmente vazio por console.
    """
    return {
        "saindo": False,
        "tela_atual": "demo",
        "pilha_telas": [],
        "modo_verboso": False,
        "foco_console": None,
        "cursores": {},
        "selecoes": {},
    }


def _modo_verboso_de_modelo(modelo):
    """Retorna o modo_verboso inicial para a tela do modelo (H-0037).

    Para politica 'somente_verboso' ou 'alternavel' com modo_inicial 'verboso',
    retorna True (ADR-0028 D23). Para todas as outras politicas, retorna False.
    """
    if modelo is None:
        return False
    try:
        elementos = modelo.corpo.elementos
    except AttributeError:
        return False
    for elemento in elementos:
        if elemento.tipo == "console":
            politica = getattr(elemento, "politica_modo", None)
            if politica == "somente_verboso":
                return True
            if (politica == "alternavel"
                    and getattr(elemento, "modo_inicial", None) == "verboso"):
                return True
            break
    return False


def _verboso_efetivo(estado, modelo):
    """Determina o flag verboso efetivo para o modelo corrente (H-0037).

    Aplica a politica de modo do console da tela:
    - somente_verboso: sempre True (nao afetado pelo toggle).
    - somente_nao_verboso: sempre False (nao afetado pelo toggle).
    - alternavel: estado.get("modo_verboso", False).
    - Sem politica (legado): False.

    QAI40-003: um override explicito (``modo_verboso_forcado``) injetado por um
    ponto de entrada derivado (ex.: ``--verboso`` da demo de navegacao) tem
    precedencia sobre a politica do modelo, alcancando o runtime e o renderer
    reais. O override nao cria politica nova no JSON nem torna a tecla ``V``
    disponivel onde nao era contratada.
    """
    if estado.get("modo_verboso_forcado") is True:
        return True
    if modelo is None:
        return False
    try:
        elementos = modelo.corpo.elementos
    except AttributeError:
        return False
    for elemento in elementos:
        if elemento.tipo == "console":
            politica = getattr(elemento, "politica_modo", None)
            if politica == "somente_verboso":
                return True
            if politica == "somente_nao_verboso":
                return False
            if politica == "alternavel":
                return bool(estado.get("modo_verboso", False))
            break
    return False


def processar_comando(estado, comando, modelo=None):
    """Processa um comando sobre o estado, retornando um novo dict.

    Nao modifica o dict ``estado`` recebido como argumento. Retorna
    sempre um novo dict independente com as chaves ``"saindo"``,
    ``"tela_atual"``, ``"pilha_telas"``, ``"modo_verboso"``,
    ``"foco_console"`` e ``"cursores"``.

    H-0039 / ADR-0030: o comando ``"b"`` (alternancia de borda) foi removido
    -- a borda agora vem de ``config/estilo.json`` via ``carregar_estilo`` e
    nao e alternavel em runtime por esta via. O estado nao carrega mais
    ``tipo_borda``.

    H-0040 / ADR-0031: navegacao de console de nivel unico. Tab/Shift+Tab
    alternam o console focado circularmente (D5) e entram sempre no item
    logico 0 (D6). As setas movem o cursor por eixo com toroide na mesma
    linha/coluna (D8), respeitando celulas vazias (D8) e degenerados (D9).
    Espaco nao altera selecao (D13/PN-0017). Enter NAO recebe nova funcao
    neste handoff: nenhum dispatcher de acao, nenhuma nova resposta
    demonstrativa (PN-0013); o comportamento preexistente (preservar estado)
    e mantido.

    Comportamento (case-sensitive):

    - ``"s"`` ou ``"\\x1b"`` (Esc):
      - Se ``pilha_telas`` nao vazia: faz pop; ``tela_atual`` passa a
        ser o ultimo elemento removido da pilha; ``saindo`` permanece
        ``False``.
      - Se ``pilha_telas`` vazia: define ``saindo = True`` (sai).
    - Tab (``"\\t"``): avanca o foco circularmente; entra no item 0.
    - Shift+Tab (``"\\x1b[Z"`` ou ``"\\x1b\\t"``): recua o foco circularmente;
      entra no item 0 (NC-001 -- ambas as sequencias reconhecidas).
    - Setas ``"\\x1b[A/C/B/D"`` (cima/direita/baixo/esquerda): movem o cursor
      no console focado por toroide na mesma coluna/linha.
    - Espaco (``" "``): nao altera selecao (PN-0017).
    - ``"V"``/``"v"``: alterna verbosidade em telas alterhaveis (preserva item
      logico -- D10/PN-0011).
    - Qualquer outro comando (incluindo string vazia): se ``modelo`` for
      diferente de ``None``, percorre ``modelo.corpo.elementos[]`` em
      busca de elemento do tipo ``"lancador"``; para cada item em
      ``_campos_inertes["itens"]`` cujo ``chip`` coincida com o comando,
      empilha ``tela_atual`` em ``pilha_telas`` e troca ``tela_atual``
      para o ``tela_destino`` do item (primeira coincidencia). Comandos
      sem coincidencia nao alteram o estado.

    Compatibilidade:
        O terceiro argumento ``modelo`` e opcional (default ``None``)
        para preservar o comportamento anterior quando omitido. Estados
        sem ``tela_atual`` ou ``pilha_telas`` sao tratados com defaults
        (``"demo"`` e ``[]``). Estados legados sem ``foco_console``/
        ``cursores`` sao tratados com defaults (``None``/``{}``) -- o
        runtime novo e retrocompativel com estados criados por
        ``criar_estado_inicial`` antes do H-0040.
    """
    # H-0040: estado de navegacao de runtime. ``foco_console``/``cursores``
    # sao preservados entre comandos. Defaults defensivos aceitam estados
    # legados criados antes do H-0040 (sem essas chaves).
    novo = {
        "saindo": estado["saindo"],
        "tela_atual": estado.get("tela_atual", "demo"),
        "pilha_telas": list(estado.get("pilha_telas", [])),
        "modo_verboso": estado.get("modo_verboso", False),
        "foco_console": estado.get("foco_console"),
        "cursores": dict(estado.get("cursores", {})),
        # H-0041: selecao multipla por console (runtime). Preservada entre
        # comandos; nunca persiste em JSON (NC-005/D-SEL-01).
        "selecoes": dict(estado.get("selecoes", {})),
    }
    # QAI40-003 / patch pos-validacao manual: ``modo_verboso_forcado`` e
    # override de runtime (ex.: ``--verboso``) e deve permanecer no estado
    # durante toda a sessao. Nao persiste em JSON; ausente em chamadas sem
    # override (comportamento anterior preservado).
    if estado.get("modo_verboso_forcado") is True:
        novo["modo_verboso_forcado"] = True
    # H-0039: o EstiloResolvido e imutavel e sessão-scopo; preservado entre
    # comandos para que renderizar_estado continue consumindo o mesmo objeto.
    if "estilo" in estado:
        novo["estilo"] = estado["estilo"]
    # H-0040 / patch VM-11: geometria corrente do terminal usada pela navegacao
    # para consumir a MESMA geometria do renderer (calcular_distribuicao).
    # ``largura``, ``altura``, ``altura_interna`` e ``desconto_estrutural`` sao
    # transitivos como o estilo; nunca persistem em JSON. Ausentes em estados
    # legados (defaults tratados pelas funcoes de navegacao).
    #
    # VM-11: ``desconto_estrutural`` DEVE ser preservado entre comandos. Se for
    # descartado, a primeira seta apos redimensionamento recalcula a grade com
    # area util diferente da do renderer e pode reutilizar a formacao anterior
    # (ex.: 2x3 vs 3x2 na fronteira de largura).
    if "largura" in estado:
        novo["largura"] = estado["largura"]
    if "altura" in estado:
        novo["altura"] = estado["altura"]
    if "altura_interna" in estado:
        novo["altura_interna"] = estado["altura_interna"]
    if "desconto_estrutural" in estado:
        novo["desconto_estrutural"] = estado["desconto_estrutural"]

    if comando == "s" or comando == "\x1b":
        # H-0041 / ADR-0034 D-SEL-08: quando o console focado declara selecao
        # multipla e ha selecao ativa, o primeiro Esc LIMPA a selecao e
        # PERMANECE na tela (nao sai/volta). Somente quando a selecao esta
        # vazia o comportamento vigente de H-0040 (Sair/Voltar) e preservado.
        # A decisao depende do estado reconciliado do console focado.
        if modelo is not None and comando == "\x1b":
            console_foco = navegacao.console_focado(
                dict(novo, modelo=modelo)
            )
            if (console_foco is not None
                    and navegacao._console_declarou_selecao_multipla(console_foco)
                    and not selecao.esta_vazia(novo, console_foco)):
                novo = selecao.limpar(novo, console_foco)
                return novo
        if novo["pilha_telas"]:
            novo["tela_atual"] = novo["pilha_telas"][-1]
            novo["pilha_telas"] = novo["pilha_telas"][:-1]
        else:
            novo["saindo"] = True
        return novo

    # H-0040 / ADR-0031: navegacao de console de nivel unico. As teclas de
    # navegacao sao tratadas ANTES do dispatch de lancador (chip por comando)
    # porque nao colidem com chips de lancador existentes (Esc/Sair, lancador
    # por chip). Tab/Shift+Tab alternam foco; setas movem cursor por eixo.
    # H-0041 / ADR-0034: Espaco/Enter delegam a ``tela/selecao.py`` quando o
    # console focado declara selecao multipla (toggle/Todos); caso contrario,
    # preservam o comportamento de H-0040 (Espaço no-op; Enter sem acao,
    # PN-0013). O estado de navegacao e selecao e exclusivamente runtime (NC-005).
    if modelo is not None and (
        navegacao.e_tab(comando)
        or navegacao.e_shift_tab(comando)
        or comando in ("\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D", " ", "\r", "\n")
    ):
        nav_estado = dict(novo)
        nav_estado["modelo"] = modelo
        if navegacao.e_tab(comando):
            nav_estado = navegacao.avancar_foco(nav_estado)
        elif navegacao.e_shift_tab(comando):
            nav_estado = navegacao.recuar_foco(nav_estado)
        elif comando in ("\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"):
            console = navegacao.console_focado(nav_estado)
            if console is not None:
                if comando == "\x1b[C":
                    nav_estado = navegacao.mover_direita(nav_estado, console)
                elif comando == "\x1b[D":
                    nav_estado = navegacao.mover_esquerda(nav_estado, console)
                elif comando == "\x1b[B":
                    nav_estado = navegacao.mover_baixo(nav_estado, console)
                elif comando == "\x1b[A":
                    nav_estado = navegacao.mover_cima(nav_estado, console)
        else:
            # H-0041: Espaco/Enter no console focado. Quando o console declara
            # selecao multipla, delega ao modulo de selecao (D-SEL-05/D-SEL-04).
            # Caso contrario, preserva H-0040 (Espaço no-op; Enter sem acao).
            #
            # H0041-MANUAL-R02-001 (P04): em TTY real com ``tty.setcbreak``,
            # ICRNL permanece ativo e traduz Enter (``\\r``) para ``\\n`` antes
            # da leitura. O caminho direto ``processar_comando(..., "\\r")``
            # funcionava; o loop TTY recebia ``\\n`` e descartava a tecla.
            # Ambos os bytes sao Enter.
            console = navegacao.console_focado(nav_estado)
            if (console is not None
                    and navegacao._console_declarou_selecao_multipla(console)):
                if comando == " ":
                    item = navegacao.item_selecionado(console, nav_estado)
                    if isinstance(item, dict):
                        nav_estado = selecao.alternar(
                            nav_estado, console, item.get("id")
                        )
                elif comando in ("\r", "\n"):
                    # D-SEL-04/D-SEL-07/D-SEL-21: Enter com selecao vazia age
                    # como Todos; com selecao, Enter e INATIVO (nenhuma execucao
                    # neste handoff).
                    #
                    # QA-H0041-001 (patch P01): a decisao entre ``Todos`` e
                    # nao-executar considera o estado EXISTENTE no INICIO do
                    # acionamento, ANTES de descartar IDs residuais. Uma selecao
                    # originalmente NAO vazia, mas composta apenas por IDs
                    # invalidos, torna-se vazia apos reconciliacao; nesse caso o
                    # acionamento SOMENTE reconcilia (deixa a selecao vazia) e
                    # NAO aplica ``Todos`` no mesmo acionamento. ``selecionar_
                    # todos`` so e aplicada quando a selecao JA ESTAVA
                    # originalmente vazia (antes de qualquer reconciliacao).
                    # IDs invalidos nunca sao preservados (D-SEL-03).
                    # ``selecao_originalmente_vazia`` lê a lista bruta (sem
                    # reconciliar); ``esta_vazia`` lê a lista reconciliada.
                    selecao_originalmente_vazia = (
                        len(selecao._selecao_do_console(nav_estado, console)) == 0
                    )
                    if not selecao_originalmente_vazia:
                        # Selecao com residuo: reconcilia (descarta IDs
                        # invalidos) sem aplicar Todos nem executar.
                        nav_estado = selecao.reconciliar(nav_estado, console)
                    elif selecao.esta_vazia(nav_estado, console):
                        nav_estado = selecao.selecionar_todos(nav_estado, console)
            elif comando == " ":
                # D13/PN-0017: espaco nao cria nem alterna selecao (legado).
                nav_estado = navegacao.processar_espaco(nav_estado)
        # O modelo nao e estado de runtime; e removido antes de devolver.
        novo["foco_console"] = nav_estado.get("foco_console")
        novo["cursores"] = dict(nav_estado.get("cursores", {}))
        novo["selecoes"] = dict(nav_estado.get("selecoes", {}))
        return novo

    # H-0037: tecla V (maiuscula) ou v (minuscula) alterna verbosidade
    # somente em telas com politica 'alternavel'. As duas entradas são
    # tratadas nominalmente aqui, sem normalizar todas as teclas em
    # maiusculas globalmente (outros comandos continuam case-sensitive).
    # Telas fixas (somente_verboso / somente_nao_verboso) e telas legadas
    # ignoram ambas sem alterar o estado (H0037-MANUAL-003).
    if comando in ("V", "v") and modelo is not None:
        for elemento in modelo.corpo.elementos:
            if elemento.tipo == "console":
                if getattr(elemento, "politica_modo", None) == "alternavel":
                    novo["modo_verboso"] = not novo["modo_verboso"]
                break
        return novo

    if modelo is not None:
        for elemento in modelo.corpo.elementos:
            if elemento.tipo != "lancador":
                continue
            itens = elemento._campos_inertes.get("itens", []) or []
            for item in itens:
                if not isinstance(item, dict):
                    continue
                if item.get("chip") == comando:
                    novo["pilha_telas"].append(novo["tela_atual"])
                    novo["tela_atual"] = item.get("tela_destino")
                    return novo

    return novo


def renderizar_estado(estado, modelo, largura=None, altura=None):
    """Delega para o renderer usando o estilo do estado e a largura dada.

    Nao modifica ``estado`` nem ``modelo``. Nenhum efeito colateral
    alem da chamada a ``renderizar_tela``. ``largura=None`` produz
    saida deterministica com fallback 42 chars. ``altura=None``
    preserva o comportamento atual (sem preenchimento vertical); quando
    fornecida, repassa a altura ao renderer para a ocupacao vertical da
    janela do terminal pelo corpo (H-0015 / ADR-0013).

    H-0039 / ADR-0030: o ``EstiloResolvido`` e lido de ``estado["estilo"]``
    (carregado uma vez em ``main``); a borda nao e mais alternavel nem
    carregada por ``tipo_borda``.

    H-0040 / ADR-0031: repassa parametros opcionais de navegacao ao renderer:
    ``foco_console`` (indice do console focado), ``cursores`` (dict id->item
    logico) e ``lista_foco`` (lista de consoles focalizaveis). Esses dados
    sao de runtime e derivados do modelo corrente; o renderer os consume para
    materializar o indicador de cursor no console focado e aplicar as regras
    dinamicas de existencia dos chips ``[⇆]``/``[✥]`` (D11/D12/D14).
    """
    lista_foco = navegacao.lista_foco(modelo) if modelo is not None else []
    return renderizar_tela(
        modelo, estado["estilo"], largura=largura, altura=altura,
        verboso=_verboso_efetivo(estado, modelo),
        foco_console=estado.get("foco_console"),
        cursores=estado.get("cursores", {}),
        lista_foco=lista_foco,
        largura_navegacao=largura,
        selecoes=estado.get("selecoes", {}),
    )


def id_conteudo_externo_de(id_tela):
    """Retorna o id do documento externo associado a ``id_tela``, ou None.

    A associacao vem exclusivamente do catalogo interno do ponto de entrada
    (``_CATALOGO_CONTEUDO_EXTERNO``); a ausencia de associacao e explicita
    (chave ausente -> None). Nunca le vinculo do JSON estrutural.
    """
    return _CATALOGO_CONTEUDO_EXTERNO.get(id_tela)


def _carregar_modelo_por_id(id_tela):
    """Helper: carrega e constroi o ModeloTela para ``id_tela`` da raiz demo.

    H-0036: identifica o cenario, localiza o JSON estrutural e, quando o
    catalogo associa um documento externo, localiza e carrega o conteudo
    SEPARADAMENTE (dois documentos, duas leituras), entregando ambos como
    entradas distintas a ``construir_modelo``. A distincao entre origens e
    preservada: o conteudo nunca e reinserido no objeto bruto do JSON
    estrutural. Cenarios sem conteudo externo preservam o comportamento
    historico (placeholder). Cada chamada reconstroi o modelo do zero, sem
    estado residual entre trocas de cenario (sem heranca, sem vazamento).

    H-0043: identificadores ``h0043_*`` resolvem para a tela estrutural
    ``resultado_execucao`` e para a fixture de runtime homonima, via
    ``tela.resultado_execucao`` (loader → classificacao → modelo composto).
    """
    if id_tela in _CATALOGO_CENARIOS_RESULTADO_EXECUCAO:
        fixture = _CATALOGO_CENARIOS_RESULTADO_EXECUCAO[id_tela]
        caminho_runtime = os.path.join(
            _DIR_FIXTURES_DEMO, fixture + ".json"
        )
        sessao = resultado_execucao_mod.carregar_sessao_resultado(
            None,
            id_tela,
            caminho_runtime,
            raiz_telas=_RAIZ_TELAS_DEMO,
            id_tela=_ID_TELA_RESULTADO_EXECUCAO,
        )
        return sessao.modelo

    tela_raw = carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
    id_conteudo = id_conteudo_externo_de(id_tela)
    conteudo_externo = None
    if id_conteudo is not None:
        conteudo_externo = carregar_conteudo_externo(
            None, id_conteudo, _RAIZ_TELAS_DEMO
        )
    return construir_modelo(tela_raw, conteudo_externo=conteudo_externo)


def _ler_tecla_sessao(fd=None):
    """Le uma tecla, distinguindo Esc isolado de sequencias de escape.

    Em modo cbreak, sequencias de terminal chegam caractere a caractere e
    comecam pelo mesmo ``Esc`` usado para sair. Apos esse primeiro caractere,
    aguarda brevemente por continuacao: se houver, consome toda a sequencia
    ja disponivel e a devolve como comando desconhecido (portanto ignorado);
    sem continuacao, devolve o Esc isolado normalmente.

    Opera inteiramente sobre o descritor de arquivo bruto (``os.read``) para
    evitar o dessincronismo entre o buffer interno do ``TextIOWrapper`` e o
    ``select.select``: o buffer do TextIOWrapper pode drenar mais bytes do SO
    do que os devolvidos, fazendo ``select`` reportar erroneamente "nenhum byte
    pendente" quando ja ha bytes prontos no buffer interno.
    """
    if fd is None:
        fd = sys.stdin.fileno()
    raw = os.read(fd, 1)
    if not raw:
        return ""
    ch = raw.decode("latin-1")
    if ch != "\x1b":
        return ch

    prontos, _, _ = select.select([fd], [], [], 0.03)
    if not prontos:
        return ch

    raw2 = os.read(fd, 1)
    if not raw2:
        return ch
    sequencia = ch + raw2.decode("latin-1")
    while select.select([fd], [], [], 0)[0]:
        proximo = os.read(fd, 1)
        if not proximo:
            break
        sequencia += proximo.decode("latin-1")
    return sequencia


class captura_interrupcao_de_script:
    """Context manager de captura escopada de KeyboardInterrupt.

    Para uso futuro ao redor de chamadas a scripts/processos internos
    disparados pela aplicacao. Captura KeyboardInterrupt localmente:
    interrompe apenas o bloco protegido; a sessao TUI permanece ativa.
    Outras excecoes propagam normalmente.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is KeyboardInterrupt


def _restaurar_efeitos_visuais_tui():
    """Emite sequencias de restauracao do terminal de forma defensiva.

    Usada tanto no rollback interno de ``_iniciar_sessao_tui`` quanto no
    encerramento normal via ``_encerrar_sessao_tui``. Silencia erros
    internamente; nunca lanca excecao propria.
    """
    try:
        sys.stdout.write("\x1b[?7h\x1b[?25h\x1b[?1049l")
    except Exception:
        pass
    try:
        sys.stdout.flush()
    except Exception:
        pass


def _iniciar_sessao_tui(fd_stdin):
    """Salva estado TTY, ativa cbreak mode e entra em alternate screen.

    Usa ``tty.setcbreak`` (preserva OPOST e ISIG; rejeita modo raw).
    Desativa autowrap (ESC[?7l) e limpa a tela uma unica vez (ESC[2J).
    Retorna os atributos originais do terminal para restauracao posterior.

    Em caso de falha de ``write`` ou ``flush`` apos ``setcbreak``,
    executa rollback interno completo (restauracao visual + termios) e
    propaga a excecao original. ``sessao_iniciada`` permanece ``False``
    no chamador.
    """
    atributos_originais = termios.tcgetattr(fd_stdin)
    tty.setcbreak(fd_stdin)
    try:
        sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J\x1b[H")
        sys.stdout.flush()
    except Exception:
        _restaurar_efeitos_visuais_tui()
        try:
            termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)
        except Exception:
            pass
        raise
    return atributos_originais


def _encerrar_sessao_tui(fd_stdin, atributos_originais):
    """Restaura atributos TTY, autowrap, cursor e encerra alternate screen.

    Executa cada passo de forma defensiva para garantir restauracao
    mesmo que uma das etapas falhe.
    """
    try:
        termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)
    except Exception:
        pass
    _restaurar_efeitos_visuais_tui()


def _par_dimensoes_valido(largura, altura):
    """Retorna True se e somente se largura e altura sao inteiros positivos."""
    try:
        l = int(largura)
        a = int(altura)
        return l > 0 and a > 0
    except (TypeError, ValueError):
        return False


def _obter_dimensoes_ioctl(fd):
    """Consulta dimensoes do terminal via ioctl(TIOCGWINSZ).

    Retorna ``(largura, altura)`` quando o par e valido, ``None``
    caso contrario.
    """
    try:
        buf = struct.pack("HHHH", 0, 0, 0, 0)
        buf = fcntl.ioctl(fd, termios.TIOCGWINSZ, buf)
        rows, cols, _, _ = struct.unpack("HHHH", buf)
        if _par_dimensoes_valido(cols, rows):
            return int(cols), int(rows)
        return None
    except (OSError, struct.error):
        return None


def _obter_dimensoes_env():
    """Obtem dimensoes das variaveis de ambiente LINES e COLUMNS.

    Aceita somente quando ambas estao presentes e formam par valido.
    Retorna ``(largura, altura)`` ou ``None``.
    """
    try:
        cols = int(os.environ["COLUMNS"])
        rows = int(os.environ["LINES"])
        if _par_dimensoes_valido(cols, rows):
            return cols, rows
        return None
    except (KeyError, ValueError):
        return None


def _obter_dimensoes_iniciais(fd):
    """Cadeia de obtencao na inicializacao: ioctl -> env -> (80, 24)."""
    par = _obter_dimensoes_ioctl(fd)
    if par is not None:
        return par
    par = _obter_dimensoes_env()
    if par is not None:
        return par
    return 80, 24


def _obter_dimensoes_apos_sigwinch(fd, ultimas_validas):
    """Cadeia de obtencao apos SIGWINCH: ioctl -> env -> ultimas_validas.

    O fallback fixo (80, 24) nao aparece aqui; em sessao ativa, fontes
    invalidas preservam as ultimas dimensoes validas conhecidas.
    """
    par = _obter_dimensoes_ioctl(fd)
    if par is not None:
        return par
    par = _obter_dimensoes_env()
    if par is not None:
        return par
    return ultimas_validas


def _instalar_handler_sigwinch(w_wakeup, resize_pendente):
    """Instala handler de SIGWINCH que escreve no wakeup pipe.

    O handler executa somente operacoes async-signal-safe: atribuicao e
    ``os.write``. Pipe cheio e tratado silenciosamente. Retorna o
    handler anterior.
    """
    def _handler(signum, frame):
        resize_pendente[0] = True
        try:
            os.write(w_wakeup, b"\x00")
        except OSError:
            pass
    handler_anterior = signal.signal(signal.SIGWINCH, _handler)
    return handler_anterior


def _restaurar_handler_sigwinch(handler_anterior):
    """Restaura o handler de SIGWINCH anterior de forma defensiva."""
    try:
        signal.signal(signal.SIGWINCH, handler_anterior)
    except Exception:
        pass


def _tela_pequena_demais(largura, altura):
    """Retorna True quando as dimensoes sao insuficientes para a tela normal."""
    return largura < LARGURA_MINIMA_TELA or altura < ALTURA_MINIMA_TELA


def _quadro_minimo_aviso(largura, altura):
    """Gera quadro de aviso para terminal pequeno demais.

    Retorna string com exatamente ``altura`` linhas terminadas por ``\\n``,
    cada linha com exatamente ``largura`` caracteres antes do ``\\n``.
    """
    if largura >= 23:
        msg = "terminal pequeno demais"
    elif largura >= 9:
        msg = "tela peq."
    else:
        msg = ""
    linha_aviso = msg[:largura].ljust(largura)
    linha_vazia = " " * largura
    linhas = [linha_aviso] + [linha_vazia] * (altura - 1)
    return "\n".join(linhas) + "\n"


def _resolver_conteudo(estado, modelo, largura, altura):
    """Resolve o conteudo a apresentar para as dimensoes correntes.

    Retorna quadro minimo de aviso quando terminal pequeno demais ou
    quando o renderer levanta ``RenderizadorErro``.
    """
    if _tela_pequena_demais(largura, altura):
        return _quadro_minimo_aviso(largura, altura)
    try:
        return renderizar_estado(estado, modelo, largura, altura=altura)
    except RenderizadorErro:
        return _quadro_minimo_aviso(largura, altura)


def _apresentar_quadro(conteudo, largura=None):
    """Apresenta um quadro completo por posicionamento absoluto linha a linha.

    Cada linha e precedida por CSI n;1H (posicionamento absoluto na coluna 1)
    e preenchida com espacos ate a largura do terminal. Todo o conteudo e
    emitido em uma unica chamada write() seguida de uma unica flush().
    Synchronized output (ESC[?2026h/l) envolve o conteudo de cada quadro.
    Nao usa \\n como mecanismo de quebra de linha (ADR-0016 item 5).

    ``largura``: quando fornecida, usa esse valor; caso contrario, consulta
    ``shutil.get_terminal_size`` como fallback (compatibilidade com chamadas
    existentes sem o parametro).
    """
    w = largura if largura is not None else shutil.get_terminal_size(fallback=(80, 24)).columns
    linhas = conteudo.split("\n")
    if linhas and linhas[-1] == "":
        linhas = linhas[:-1]

    partes = ["\x1b[?2026h"]
    for i, linha in enumerate(linhas, start=1):
        partes.append("\x1b[{0};1H".format(i))
        pad = w - len(linha)
        partes.append(linha + (" " * pad if pad > 0 else ""))
    partes.append("\x1b[?2026l")

    sys.stdout.write("".join(partes))
    sys.stdout.flush()


def _tela_inicial_de_argv(argv):
    """Resolve a tela inicial a partir de argv (H-0036).

    Aceita opcionalmente um id de tela como primeiro argumento posicional
    (analogo a ``demo/demo_distribuicao.py <id_tela>``), permitindo abrir
    diretamente qualquer cenario — inclusive os cenarios H-0036 com conteudo
    externo (``h0036_console_hierarquia``, ``h0036_console_tabela``,
    ``h0036_console_conjuntos``) e os cenarios adaptados
    (``h0035_console_com``, ``h0035_console_sem``). Sem argumento, usa a tela
    raiz da demonstracao (``"demo"``), preservando o comportamento historico.
    """
    for arg in argv[1:]:
        if arg and not arg.startswith("-"):
            return arg
    return "demo"


def main(argv=None, estado_inicial=None):
    """Entrada principal da aplicacao demonstravel.

    Em TTY interativo (stdin e stdout sao TTY), ativa alternate screen,
    oculta cursor, desativa autowrap e entra em cbreak mode. Dimensoes
    obtidas por ioctl(TIOCGWINSZ) na inicializacao. SIGWINCH e tratado
    via wakeup pipe e select duplo; cada redesenho usa as dimensoes
    correntes. Terminal pequeno demais exibe quadro de aviso com
    recuperacao automatica. Restauracao completa em ``finally`` com
    cleanup condicional por sentinelas. Fora de TTY (pipe/teste), usa
    leitura linha a linha e ``print`` normal. Retorna 0 (saida limpa).

    H-0036: aceita opcionalmente um id de tela inicial via argv (default
    ``"demo"``); ``python demo/demo.py h0036_console_hierarquia`` abre o
    cenario H-0036 diretamente, carregando o conteudo externo associado pelo
    catalogo. Sem argumento, o comportamento historico e preservado.
    """
    if argv is None:
        argv = sys.argv
    estado = criar_estado_inicial()
    # H-0040: permite que um ponto de entrada derivado (demo_navegacao) injete
    # um estado pre-populado (ex.: foco no primeiro console ao iniciar), sem
    # reescrever o loop TUI. Quando ``estado_inicial`` e None, o comportamento
    # historico e preservado integralmente.
    if estado_inicial is not None:
        estado = dict(estado_inicial)
    # H-0039 / ADR-0030: carrega o estilo global uma unica vez por sessao a
    # partir de config/estilo.json. O EstiloResolvido e imutavel e repassado
    # ao renderer via estado["estilo"]; nao e recarregado por comando/render.
    estilo = carregar_estilo()
    estado = dict(estado, estilo=estilo)
    tela_inicial = _tela_inicial_de_argv(argv)
    if tela_inicial != estado["tela_atual"]:
        estado = dict(estado, tela_atual=tela_inicial)
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    # Override ``--verboso`` (modo_verboso_forcado) tem precedencia sobre a
    # politica do modelo ao iniciar a sessao; sem override, restaura o modo
    # inicial da politica (comportamento anterior).
    if estado.get("modo_verboso_forcado") is True:
        estado = dict(estado, modo_verboso=True)
    else:
        estado = dict(estado, modo_verboso=_modo_verboso_de_modelo(modelo))

    if sys.stdin.isatty() and sys.stdout.isatty():
        fd = sys.stdin.fileno()
        largura, altura = _obter_dimensoes_iniciais(fd)
        # H-0040: largura no estado para a navegacao consumir a mesma geometria
        # do renderer desde o primeiro quadro.
        estado = dict(
            estado,
            largura=largura,
            altura=altura,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        resize_pendente = [False]
        r_wakeup = None
        w_wakeup = None
        sessao_iniciada = False
        handler_instalado = False
        handler_anterior = None
        atributos_originais = None
        try:
            r_wakeup, w_wakeup = os.pipe()
            os.set_blocking(r_wakeup, False)
            os.set_blocking(w_wakeup, False)
            atributos_originais = _iniciar_sessao_tui(fd)
            sessao_iniciada = True
            handler_anterior = _instalar_handler_sigwinch(w_wakeup, resize_pendente)
            handler_instalado = True
            _apresentar_quadro(
                _resolver_conteudo(estado, modelo, largura, altura), largura
            )
            while True:
                try:
                    prontos, _, _ = select.select([fd, r_wakeup], [], [])
                    if r_wakeup in prontos:
                        while True:
                            try:
                                dados = os.read(r_wakeup, 64)
                                if not dados:
                                    break
                            except BlockingIOError:
                                break
                            except OSError:
                                break
                        resize_pendente[0] = False
                        nova_l, nova_a = _obter_dimensoes_apos_sigwinch(
                            fd, (largura, altura)
                        )
                        if nova_l != largura or nova_a != altura:
                            largura, altura = nova_l, nova_a
                            # D10 / patch VM-11: redimensionamento preserva o
                            # item logico e atualiza largura/altura/desconto no
                            # estado ANTES de qualquer seta, para a navegacao
                            # recalcular formacao, vizinhos e toroide na
                            # geometria vigente (mesma do renderer).
                            estado = dict(
                                estado,
                                largura=largura,
                                altura=altura,
                                desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
                            )
                            _apresentar_quadro(
                                _resolver_conteudo(estado, modelo, largura, altura),
                                largura,
                            )
                        if fd not in prontos:
                            continue
                    ch = _ler_tecla_sessao(fd=fd)
                    tela_antes = estado["tela_atual"]
                    verboso_antes = estado.get("modo_verboso", False)
                    foco_antes = estado.get("foco_console")
                    cursores_antes = dict(estado.get("cursores", {}))
                    selecoes_antes = dict(estado.get("selecoes", {}))
                    estado = dict(
                        estado,
                        largura=largura,
                        altura=altura,
                        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
                    )
                    estado = processar_comando(estado, ch, modelo)
                    if estado["saindo"]:
                        break
                    if estado["tela_atual"] != tela_antes:
                        modelo = _carregar_modelo_por_id(estado["tela_atual"])
                        if estado.get("modo_verboso_forcado") is True:
                            estado = dict(estado, modo_verboso=True)
                        else:
                            estado = dict(
                                estado,
                                modo_verboso=_modo_verboso_de_modelo(modelo),
                            )
                    verboso_mudou = estado.get("modo_verboso", False) != verboso_antes
                    foco_mudou = estado.get("foco_console") != foco_antes
                    cursores_mudou = estado.get("cursores", {}) != cursores_antes
                    selecoes_mudou = estado.get("selecoes", {}) != selecoes_antes
                    if (
                        estado["tela_atual"] != tela_antes
                        or verboso_mudou
                        or foco_mudou
                        or cursores_mudou
                        or selecoes_mudou
                    ):
                        _apresentar_quadro(
                            _resolver_conteudo(estado, modelo, largura, altura),
                            largura,
                        )
                except KeyboardInterrupt:
                    continue
        finally:
            if handler_instalado:
                _restaurar_handler_sigwinch(handler_anterior)
            if r_wakeup is not None:
                try:
                    os.close(r_wakeup)
                except OSError:
                    pass
            if w_wakeup is not None:
                try:
                    os.close(w_wakeup)
                except OSError:
                    pass
            if sessao_iniciada:
                _encerrar_sessao_tui(fd, atributos_originais)
    else:
        tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
        largura = tamanho_terminal.columns
        altura = tamanho_terminal.lines
        estado = dict(
            estado,
            largura=largura,
            altura=altura,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        # Mesmo tratamento do caminho TTY: quadro minimo quando a geometria
        # nao cabe (RenderizadorErro), em vez de traceback no smoke non-TTY.
        print(_resolver_conteudo(estado, modelo, largura, altura), end="")
        for linha in sys.stdin:
            comando = linha.strip()
            tela_antes = estado["tela_atual"]
            verboso_antes = estado.get("modo_verboso", False)
            foco_antes = estado.get("foco_console")
            cursores_antes = dict(estado.get("cursores", {}))
            selecoes_antes = dict(estado.get("selecoes", {}))
            # Patch VM-11: reafirma geometria corrente antes de cada comando
            # (mesma autoridade do caminho TTY), para a primeira seta usar a
            # formacao atual mesmo apos mudancas de dimensao.
            estado = dict(
                estado,
                largura=largura,
                altura=altura,
                desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
            )
            estado = processar_comando(estado, comando, modelo)
            if estado["saindo"]:
                break
            if estado["tela_atual"] != tela_antes:
                modelo = _carregar_modelo_por_id(estado["tela_atual"])
                if estado.get("modo_verboso_forcado") is True:
                    estado = dict(estado, modo_verboso=True)
                else:
                    estado = dict(
                        estado,
                        modo_verboso=_modo_verboso_de_modelo(modelo),
                    )
            verboso_mudou = estado.get("modo_verboso", False) != verboso_antes
            foco_mudou = estado.get("foco_console") != foco_antes
            cursores_mudou = estado.get("cursores", {}) != cursores_antes
            selecoes_mudou = estado.get("selecoes", {}) != selecoes_antes
            if (
                estado["tela_atual"] != tela_antes
                or verboso_mudou
                or foco_mudou
                or cursores_mudou
                or selecoes_mudou
            ):
                print(_resolver_conteudo(estado, modelo, largura, altura), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
