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

import copy
import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

import fcntl
import os
import re
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
    _navegacao_atual,
    _largura_sem_ansi,
    _texto_chip_barra,
    geometria_console,
)
from tela import navegacao
from tela import paginacao
from tela import selecao
from tela import resultado_execucao as resultado_execucao_mod
from tela import fluxo_execucao as fluxo_execucao_mod
from tela.controle_execucao import (
    ControleExecucao,
    ControleExecucaoRepresentacao,
)
from tela.registro_acoes import RegistroAcoes, validar_elegibilidade
import importlib.util as _importlib_util_executor

_spec_executor = _importlib_util_executor.spec_from_file_location(
    "demo_executor_controle_execucao",
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "executor_controle_execucao.py",
    ),
)
_mod_executor = _importlib_util_executor.module_from_spec(_spec_executor)
_spec_executor.loader.exec_module(_mod_executor)
executar_controle_execucao = _mod_executor.executar
documento_resultado_observavel = _mod_executor.documento_resultado_observavel

# H-0045-P12: carrega o helper por caminho absoluto. ``python demo/demo.py``
# registra este arquivo como modulo ``demo``, o que impede
# ``from demo import casos_validacao_paginacao``.
import importlib.util as _importlib_util

_spec_casos = _importlib_util.spec_from_file_location(
    "demo_casos_validacao_paginacao",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "casos_validacao_paginacao.py"),
)
casos_val = _importlib_util.module_from_spec(_spec_casos)
_spec_casos.loader.exec_module(casos_val)

LARGURA_MINIMA_TELA = 10
ALTURA_MINIMA_TELA = 6

# H-0051 / ADR-0041: sequencias fisicas de PageUp/PageDown (CSI 5~/6~),
# unicas entradas de teclado que acionam paginacao. Substituem integralmente
# ","/"<"/"."/">" (H-0045), sem alias nem fallback residual desses caracteres.
TECLA_PAGE_UP = "\x1b[5~"
TECLA_PAGE_DOWN = "\x1b[6~"

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
    # H-0052: a fixture envelope passiva reutiliza a tabela canônica H-0036.
    "h0052_tabela_passiva": "h0036_tabela_conteudo",
    "h0035_console_com": "h0035_console_com_conteudo",
    "h0035_console_sem": "h0035_console_sem_conteudo",
    # H-0037 / ADR-0028: cenarios de politica de modo por tela.
    # Cenarios 1 e 2 compartilham o mesmo documento externo.
    "h0037_console_nao_verboso": "h0037_dois_niveis_conteudo",
    "h0037_console_verboso_dois_niveis": "h0037_dois_niveis_conteudo",
    "h0037_console_alternavel_tres_niveis": "h0037_tres_niveis_conteudo",
    "h0037_console_tabela_alternavel": "h0037_tabela_conteudo",
    "h0053_arvore_colapsavel": "h0053_arvore_colapsavel_conteudo",
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
_ID_TELA_H0044 = fluxo_execucao_mod.ID_TELA_H0044
_ID_ACAO_H0050 = "h0050.controle_execucao"
_FIXTURE_H0050 = os.path.join(
    _DIR_FIXTURES_DEMO, "h0050_execucao_universal_fixture.json"
)


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
        "pagina_atual": {},
    }


def _registro_acoes_h0050():
    """Cria o registro explícito da ação sintética da demonstração."""
    registro = RegistroAcoes()
    registro.registrar(
        _ID_ACAO_H0050,
        "processo",
        modos_execucao_aceitos=("executar", "dry_run"),
        executor=lambda captura: executar_controle_execucao(
            captura, _FIXTURE_H0050
        ),
    )
    return registro


def _chip_controle_execucao_de(modelo):
    raw = getattr(modelo, "_raw", {}) if modelo is not None else {}
    barra = raw.get("barra_de_menus", {}) if isinstance(raw, dict) else {}
    chips = barra.get("chips", []) if isinstance(barra, dict) else []
    for chip in chips:
        if (
            isinstance(chip, dict)
            and chip.get("forma_exibicao") == "controle_execucao"
            and isinstance(chip.get("id"), str)
        ):
            return chip["id"]
    return "chip_controle_execucao"


def _anexar_controle_execucao(estado, modelo):
    """Anexa uma instância nova somente na abertura de uma tela adotante."""
    raw = getattr(modelo, "_raw", {}) if modelo is not None else {}
    if not isinstance(raw, dict) or "controle_execucao" not in raw:
        # Um controle suspenso permanece associado à origem até seu retorno;
        # uma nova sessão começa com criar_estado_inicial(), sem esse campo.
        return dict(estado)
    if (
        isinstance(estado.get("controle_execucao"), ControleExecucao)
        and estado.get("_controle_execucao_tela") == getattr(modelo, "id", None)
        and estado.get("_sessao_resultado_controle") is None
    ):
        return dict(estado)
    registro = _registro_acoes_h0050()
    acoes = validar_elegibilidade(raw, registro)
    novo = dict(estado)
    novo["controle_execucao"] = ControleExecucao(
        raw["controle_execucao"],
        acoes,
        chip_id=_chip_controle_execucao_de(modelo),
    )
    novo["_controle_execucao_tela"] = getattr(modelo, "id", None)
    lista = navegacao.lista_foco(modelo)
    if lista and novo.get("foco_console") is None:
        novo["foco_console"] = 0
        novo["cursores"] = {lista[0].id: 0}
        novo["selecoes"] = {lista[0].id: []}
        novo["pagina_atual"] = {lista[0].id: 1}
    novo.pop("resultado_controle_execucao", None)
    novo.pop("_sessao_resultado_controle", None)
    novo.pop("_modelo_origem_controle", None)
    return novo


def _preparar_estado_h0053(estado, modelo):
    """Prepara o ramo aberto usado exclusivamente pela demonstracao H-0053.

    A ausencia de IDs fechados continua sendo apenas o estado transitório da
    árvore; esta preparação não altera schema nem cria uma política global de
    expansão. Ela torna explícita e determinística a condição inicial da
    fixture demonstrativa no ponto de entrada da demo.
    """
    if getattr(modelo, "id", None) != "h0053_arvore_colapsavel":
        return estado
    arvores = [
        console for console in navegacao.lista_foco(modelo)
        if navegacao.tipo_navegacao_efetivo(console) == "arvore_colapsavel"
    ]
    if not arvores:
        return estado
    ramos = dict(estado.get("ramos_fechados", {}) or {})
    for console in arvores:
        ramos.setdefault(console.id, frozenset())
    novo = dict(estado)
    novo["ramos_fechados"] = ramos
    return _reconciliar_cursor_focalizado(novo, modelo)


def _reconciliar_cursor_focalizado(estado, modelo):
    """Entrega ao contexto de árvore o cursor reconciliado do runtime."""
    if modelo is None:
        return dict(estado)
    reconciliado = navegacao.reconciliar_cursor_arvore(
        dict(estado, modelo=modelo)
    )
    novo = dict(estado)
    novo["cursores"] = dict(reconciliado.get("cursores", {}))
    return novo


def _controle_execucao_ativo(estado, modelo=None):
    controle = estado.get("controle_execucao")
    tela_corrente = (
        getattr(modelo, "id", None)
        if modelo is not None
        else estado.get("tela_atual")
    )
    # Durante o resultado, o modelo corrente e o da tela de resultado; a
    # autoridade do controle permanece na origem suspensa.
    if estado.get("_sessao_resultado_controle") is not None:
        return False
    if estado.get("_modelo_origem_controle") is not None:
        tela_corrente = getattr(
            estado.get("_modelo_origem_controle"), "id", tela_corrente
        )
    return (
        isinstance(controle, ControleExecucao)
        and estado.get("_controle_execucao_tela") == tela_corrente
    )


def _resultado_controle_ativo(estado):
    return estado.get("_sessao_resultado_controle") is not None


def _abrir_resultado_controle(estado, modelo, resultado):
    """Abre a tela vigente de resultado sem pilha paralela nem fluxo H-0044."""
    origem = estado.get("_modelo_origem_controle") or modelo
    tela_raw = carregar_tela(
        None, _ID_TELA_RESULTADO_EXECUCAO, _RAIZ_TELAS_DEMO
    )
    ids = list(resultado.get("lote_reconciliado") or ())
    modo = resultado.get("modo")
    marcador = resultado.get("resultado")
    stdout = "modo={0}\nids={1}\nresultado={2}\n".format(
        modo,
        ",".join(ids),
        marcador,
    )
    # Documento observável no schema H-0042 (modo + IDs). A serialização
    # permanece no executor sintético para respeitar o gate sem ``json`` aqui.
    resultado_bruto = resultado.get("resultado_bruto")
    if not isinstance(resultado_bruto, str) or not resultado_bruto:
        resultado_bruto = documento_resultado_observavel(resultado)
    documento = resultado_execucao_mod.DocumentoRuntime(
        codigo_saida=0,
        stdout=stdout,
        stderr="",
        resultado_bruto=resultado_bruto,
    )
    sessao = resultado_execucao_mod.construir_modelo_resultado(
        tela_raw, documento
    )
    novo = dict(estado)
    novo["resultado_controle_execucao"] = resultado
    novo["_sessao_resultado_controle"] = sessao
    novo["_modelo_origem_controle"] = origem
    return novo


def _retornar_de_resultado_controle(estado):
    """Retorna à mesma instância de origem, preservando modo e seleção."""
    novo = dict(estado)
    origem = novo.get("_modelo_origem_controle")
    novo.pop("_sessao_resultado_controle", None)
    novo.pop("resultado_controle_execucao", None)
    # Mantém a referência viva da origem para o loop reapresentar a mesma
    # instância (espelha origem_ativa do mecanismo vigente H-0044).
    if origem is not None:
        novo["_modelo_origem_controle"] = origem
    return novo


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
            # Envelopes pre-ADR-0028 legados transportam o modo em
            # politica_exibicao; nao confundir esse caminho fixo com a
            # politica_modo D23, que e a autoridade das telas novas.
            exibicao = elemento._campos_inertes.get("politica_exibicao", {})
            if (
                politica is None
                and isinstance(exibicao, dict)
                and (
                    exibicao.get("verboso") is True
                    or exibicao.get("modo_inicial") == "verboso"
                )
            ):
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
            exibicao = elemento._campos_inertes.get("politica_exibicao", {})
            if (
                politica is None
                and isinstance(exibicao, dict)
                and (
                    exibicao.get("verboso") is True
                    or exibicao.get("modo_inicial") == "verboso"
                )
            ):
                return True
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
        "pagina_atual": dict(estado.get("pagina_atual", {})),
        # H-0041: selecao multipla por console (runtime). Preservada entre
        # comandos; nunca persiste em JSON (NC-005/D-SEL-01).
        "selecoes": dict(estado.get("selecoes", {})),
    }
    if "ramos_fechados" in estado:
        novo["ramos_fechados"] = dict(estado.get("ramos_fechados", {}))
    if isinstance(estado.get("controle_execucao"), ControleExecucao):
        # A instância é da tela aberta: suspensão e retorno carregam a mesma
        # referência; nova abertura/reload chama _anexar_controle_execucao.
        novo["controle_execucao"] = estado["controle_execucao"]
        novo["_controle_execucao_tela"] = estado.get("_controle_execucao_tela")
    if "resultado_controle_execucao" in estado:
        novo["resultado_controle_execucao"] = estado["resultado_controle_execucao"]
    if estado.get("_sessao_resultado_controle") is not None:
        novo["_sessao_resultado_controle"] = estado["_sessao_resultado_controle"]
    # Origem viva permanece após retorno do resultado (mesma instância).
    if estado.get("_modelo_origem_controle") is not None:
        novo["_modelo_origem_controle"] = estado["_modelo_origem_controle"]
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
    # H-0044: coordenador focal (objeto de runtime; preservado por referencia).
    if "fluxo_execucao" in estado:
        novo["fluxo_execucao"] = estado["fluxo_execucao"]
    # H-0045-P12: caso adaptativo de validacao (somente runtime; nao persiste).
    if "caso_validacao_adaptativo" in estado:
        novo["caso_validacao_adaptativo"] = estado["caso_validacao_adaptativo"]
    if "caso_validacao_meta" in estado:
        novo["caso_validacao_meta"] = estado["caso_validacao_meta"]

    # Boundary de estado: uma árvore focalizada com nós visíveis não chega a
    # chip/renderer sem o cursor reconciliado pela navegação vigente.
    novo = _reconciliar_cursor_focalizado(novo, modelo)

    fluxo = estado.get("fluxo_execucao")
    if fluxo is not None and isinstance(fluxo, fluxo_execucao_mod.FluxoExecucao):
        # Resultado ativo: somente Esc (e teclas ignoradas) via fluxo.
        if fluxo.resultado_ativo:
            novo_estado, _modelo_r, consumido = fluxo.processar_comando(
                novo, comando, modelo
            )
            if consumido:
                # Preserva campos de sessao nao tocados pelo retorno.
                for chave in (
                    "estilo", "largura", "altura", "altura_interna",
                    "desconto_estrutural", "fluxo_execucao", "saindo",
                    "tela_atual", "pilha_telas", "modo_verboso",
                    "modo_verboso_forcado", "pagina_atual",
                ):
                    if chave in novo and chave not in novo_estado:
                        novo_estado[chave] = novo[chave]
                novo_estado["fluxo_execucao"] = fluxo
                return novo_estado
        elif comando in (
            fluxo_execucao_mod.TECLA_INSERT,
            "\r",
            "\n",
        ):
            novo_estado, _modelo_r, consumido = fluxo.processar_comando(
                novo, comando, modelo
            )
            if consumido:
                for chave in (
                    "estilo", "largura", "altura", "altura_interna",
                    "desconto_estrutural", "fluxo_execucao", "saindo",
                    "tela_atual", "pilha_telas", "modo_verboso",
                    "modo_verboso_forcado", "pagina_atual",
                ):
                    if chave in novo and chave not in novo_estado:
                        novo_estado[chave] = novo[chave]
                novo_estado["fluxo_execucao"] = fluxo
                return novo_estado

    # H-0050: resultado observável usa a tela vigente; Esc retorna à origem.
    if _resultado_controle_ativo(novo):
        if comando == "\x1b":
            return _retornar_de_resultado_controle(novo)
        # Insert/Enter e demais teclas nao atuam no resultado.
        return novo

    controle = novo.get("controle_execucao")
    if _controle_execucao_ativo(novo, modelo):
        if comando == fluxo_execucao_mod.TECLA_INSERT:
            controle.alternar()
            return novo
        if comando in ("\r", "\n") and modelo is not None:
            console = navegacao.console_focado(dict(novo, modelo=modelo))
            if console is not None and navegacao._console_declarou_selecao_multipla(
                console
            ):
                # Mesmo acionamento semântico Enter: vazio→Todos; lote→executar.
                # Não duplica caminho de teclado/chip; consome aqui o Enter da
                # tela adotante (H-0041 permanece para telas sem controle).
                selecao_bruta = selecao._selecao_do_console(novo, console)
                reconciliado = selecao.reconciliar(novo, console)
                lote = list(selecao.selecao(console, reconciliado))
                novo["selecoes"] = dict(reconciliado.get("selecoes", {}))
                if len(selecao_bruta) > 0 and not lote:
                    # Resíduo inválido: só reconcilia; não aplica Todos.
                    novo.pop("resultado_controle_execucao", None)
                    return novo
                if not lote:
                    # Enter=Todos: seleção coletiva dos selecionáveis.
                    novo = selecao.selecionar_todos(novo, console)
                    return novo
                resultado = controle.executar(lote)
                if resultado is not None:
                    return _abrir_resultado_controle(novo, modelo, resultado)
                return novo

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
            novo.pop("ramos_fechados", None)
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
        or comando in (
            "\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D",
            " ", "\r", "\n", TECLA_PAGE_UP, TECLA_PAGE_DOWN,
        )
    ):
        nav_estado = dict(novo)
        nav_estado["modelo"] = modelo
        if navegacao.e_tab(comando):
            nav_estado = navegacao.avancar_foco(nav_estado)
            console = navegacao.console_focado(nav_estado)
            if console is not None and console._campos_inertes.get("politica_paginacao") == "com":
                # VM-H0045-R08-001 (P23): geometria invalida -> nao repagina
                # a partir de medidas invalidas; preserva cursor/pagina.
                nav_estado, geo = _com_geometria_real_do_console(nav_estado, modelo, console)
                if geo is not None:
                    nav_estado = paginacao.ir_para_pagina(
                        nav_estado, console, paginacao.pagina_atual(nav_estado, console)
                    )
        elif navegacao.e_shift_tab(comando):
            nav_estado = navegacao.recuar_foco(nav_estado)
            console = navegacao.console_focado(nav_estado)
            if console is not None and console._campos_inertes.get("politica_paginacao") == "com":
                # VM-H0045-R08-001 (P23): geometria invalida -> nao repagina
                # a partir de medidas invalidas; preserva cursor/pagina.
                nav_estado, geo = _com_geometria_real_do_console(nav_estado, modelo, console)
                if geo is not None:
                    nav_estado = paginacao.ir_para_pagina(
                        nav_estado, console, paginacao.pagina_atual(nav_estado, console)
                    )
        elif comando in (TECLA_PAGE_UP, TECLA_PAGE_DOWN):
            console = navegacao.console_focado(nav_estado)
            if console is not None and console._campos_inertes.get("politica_paginacao") == "com":
                # QA-H0045-P05-002: geometria REAL do console focado (largura
                # de coluna + altura interna), nunca o fallback altura-8.
                # VM-H0045-R08-001 (P23): geometria invalida (``geo is None``)
                # -> pagina_anterior/proxima seriam no-op sobre medidas
                # invalidas; preserva pagina/cursor sem deslocar.
                nav_estado, geo = _com_geometria_real_do_console(nav_estado, modelo, console)
                if geo is not None:
                    if comando == TECLA_PAGE_UP:
                        nav_estado = paginacao.pagina_anterior(nav_estado, console)
                    else:
                        nav_estado = paginacao.pagina_proxima(nav_estado, console)
        elif comando in ("\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"):
            console = navegacao.console_focado(nav_estado)
            if console is not None:
                itens_permitidos = None
                # VM-H0045-R08-001 (P23): ``geo_invalida`` distingue "console
                # paginado cuja geometria corrente nao comporta a barra" (setas
                # sem movimento, sem recalcular pagina sob medidas invalidas)
                # de "console paginado valido, inclusive pagina sem navegaveis"
                # (itens_permitidos == [] -> sem movimento por D-PAG-03) e de
                # "console nao paginado" (grade orientada pelo conteudo).
                geo_invalida = False
                if console._campos_inertes.get("politica_paginacao") == "com":
                    # QA-H0045-P05-002: mesma autoridade geometrica dos
                    # comandos de pagina -- as setas devem restringir-se aos
                    # itens navegaveis da MESMA pagina que o quadro exibe
                    # (D15). Escopo limitado a consoles PAGINADOS: consoles
                    # sem paginacao (matrizes de navegacao H-0040) preservam
                    # a area de grade orientada pelo conteudo (fora do
                    # escopo geometrico de H-0045).
                    nav_estado, geo = _com_geometria_real_do_console(nav_estado, modelo, console)
                    if geo is None:
                        geo_invalida = True
                    else:
                        itens_permitidos = paginacao.linhas_logicas_navegaveis_da_pagina(
                            nav_estado, console
                        )
                if not geo_invalida:
                    if comando == "\x1b[C":
                        nav_estado = navegacao.mover_direita(
                            nav_estado, console, itens_permitidos=itens_permitidos
                        )
                    elif comando == "\x1b[D":
                        nav_estado = navegacao.mover_esquerda(
                            nav_estado, console, itens_permitidos=itens_permitidos
                        )
                    elif comando == "\x1b[B":
                        nav_estado = navegacao.mover_baixo(
                            nav_estado, console, itens_permitidos=itens_permitidos
                        )
                    elif comando == "\x1b[A":
                        nav_estado = navegacao.mover_cima(
                            nav_estado, console, itens_permitidos=itens_permitidos
                        )
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
                if navegacao.tipo_navegacao_efetivo(console) == "arvore_colapsavel":
                    nav_estado = navegacao.alternar_ramo(nav_estado, console)
                else:
                    # D13/PN-0017: espaco nao cria nem alterna selecao (legado).
                    nav_estado = navegacao.processar_espaco(nav_estado)
        # O modelo nao e estado de runtime; e removido antes de devolver.
        novo["foco_console"] = nav_estado.get("foco_console")
        novo["cursores"] = dict(nav_estado.get("cursores", {}))
        novo["selecoes"] = dict(nav_estado.get("selecoes", {}))
        if "ramos_fechados" in nav_estado:
            novo["ramos_fechados"] = dict(nav_estado.get("ramos_fechados", {}))
        else:
            novo.pop("ramos_fechados", None)
        novo["pagina_atual"] = dict(nav_estado.get("pagina_atual", {}))
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
                    novo.pop("ramos_fechados", None)
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
    estado_render = _reconciliar_cursor_focalizado(estado, modelo)
    modelo_render, contexto_chip = _modelo_com_chip_arvore(
        estado_render, modelo
    )
    lista_foco = _lista_foco_para_renderizacao(estado_render, modelo_render)
    fluxo = estado_render.get("fluxo_execucao")
    chips_destacados = None
    executar_disponivel = None
    controle = estado_render.get("controle_execucao")
    if _controle_execucao_ativo(estado_render, modelo):
        chips_destacados, executar_disponivel = controle.contexto_renderizacao()
    elif fluxo is not None and isinstance(fluxo, fluxo_execucao_mod.FluxoExecucao):
        chips_destacados = fluxo.chips_destacados()
        if not fluxo.resultado_ativo:
            executar_disponivel = fluxo.executar_disponivel(estado_render)
    marcador_anterior = _navegacao_atual.get("ramos_fechados")
    _navegacao_atual["ramos_fechados"] = dict(
        estado_render.get("ramos_fechados", {})
    )
    try:
        quadro = renderizar_tela(
            modelo_render, estado_render["estilo"], largura=largura, altura=altura,
            verboso=_verboso_efetivo(estado_render, modelo_render),
            foco_console=estado_render.get("foco_console"),
            cursores=estado_render.get("cursores", {}),
            lista_foco=lista_foco,
            largura_navegacao=largura,
            selecoes=estado_render.get("selecoes", {}),
            chips_destacados=chips_destacados,
            executar_disponivel=executar_disponivel,
            paginas_atuais=estado_render.get("pagina_atual", {}),
        )
        if contexto_chip is not None:
            chip, estado_chip = contexto_chip
            quadro = _aplicar_inatividade_chip_arvore(
                quadro, chip, estado_chip, estado_render["estilo"], modelo_render
            )
            _navegacao_atual.setdefault("estado_ativo_chips", {})[
                chip.get("id")
            ] = bool(estado_chip.get("ativo"))
        return quadro
    finally:
        if marcador_anterior is None:
            _navegacao_atual.pop("ramos_fechados", None)
        else:
            _navegacao_atual["ramos_fechados"] = marcador_anterior


def _modelo_com_chip_arvore(estado, modelo):
    """Projeta o chip declarativo de Espaço para o estado corrente.

    A barra continua sendo composta pelo JSON. O ponto de entrada apenas
    prepara uma cópia efêmera do rótulo dinâmico já declarado; a política e o
    estado continuam sendo derivados por ``tela.navegacao``.
    """
    contexto = navegacao.estado_chip_arvore(
        dict(estado, modelo=modelo)
    )
    if contexto is None or modelo is None:
        return modelo, None
    barra = copy.deepcopy(modelo.barra_de_menus)
    chips = barra.get("chips", []) if isinstance(barra, dict) else []
    chip_arvore = next(
        (
            chip for chip in chips
            if isinstance(chip, dict)
            and chip.get("tipo") == "acao"
            and chip.get("tecla") == "␣"
            and chip.get("forma_exibicao") == "rotulo_dinamico"
        ),
        None,
    )
    if chip_arvore is None:
        return modelo, None
    chip_arvore["texto"] = contexto["texto"]
    projetado = copy.copy(modelo)
    projetado.barra_de_menus = barra
    return projetado, (chip_arvore, contexto)


def _aplicar_inatividade_chip_arvore(quadro, chip, contexto, estilo, modelo):
    """Aplica a apresentação inativa já contratada ao chip projetado.

    O rótulo ``Expandir``/``Recolher`` tem a mesma largura. Assim, a troca
    preserva a distribuição calculada pela barra e apenas reaplica a cor
    canônica de inatividade quando o item corrente é folha.
    """
    if contexto.get("ativo"):
        return quadro
    distribuicao = modelo.barra_de_menus.get("distribuicao")
    vao = 1
    if isinstance(distribuicao, dict):
        espacamentos = distribuicao.get("espacamentos") or {}
        vao = (espacamentos.get("vao_chip_texto") or {}).get("minimo", 1)
    ativo = _texto_chip_barra(chip, estilo, vao=vao, inativo=False)
    inativo = _texto_chip_barra(chip, estilo, vao=vao, inativo=True)
    return quadro.replace(ativo, inativo, 1)


def _lista_foco_para_renderizacao(estado, modelo):
    """Adapta a disponibilidade legada do chip à projeção da árvore.

    A barra de menus histórica consulta ``itens`` apenas para decidir se o
    chip de navegação existe. Para uma árvore, o modelo canônico continua
    sendo ``conteudo_externo``; esta cópia efêmera só expõe os nós atualmente
    alcançáveis a esse consumidor legado durante o render.
    """
    lista = navegacao.lista_foco(modelo) if modelo is not None else []
    resultado = []
    estado_arvore = {
        "ramos_fechados": estado.get("ramos_fechados", {}),
        "cursores": estado.get("cursores", {}),
        "pagina_atual": estado.get("pagina_atual", {}),
        "largura": estado.get("largura", 80),
        "altura_interna": estado.get("altura_interna"),
    }
    for console in lista:
        if navegacao.tipo_navegacao_efetivo(console) != "arvore_colapsavel":
            resultado.append(console)
            continue
        projetado = copy.copy(console)
        campos = dict(console._campos_inertes)
        nos = navegacao.sequencia_visivel_arvore(console, estado_arvore)
        campos["itens"] = [
            {"id": no.id, "texto": "", "navegavel": True}
            for no in nos
        ]
        projetado._campos_inertes = campos
        resultado.append(projetado)
    return resultado


def id_conteudo_externo_de(id_tela):
    """Retorna o id do documento externo associado a ``id_tela``, ou None.

    A associacao vem exclusivamente do catalogo interno do ponto de entrada
    (``_CATALOGO_CONTEUDO_EXTERNO``); a ausencia de associacao e explicita
    (chave ausente -> None). Nunca le vinculo do JSON estrutural.
    """
    return _CATALOGO_CONTEUDO_EXTERNO.get(id_tela)


def _recarregador_focal_h0044(modelo):
    """Recarregador focal observavel da demonstracao H-0044.

    Nao altera a fixture baseline H-0042. Atualiza conteudo a partir da
    entrada permanente da tela de origem, preservando a identidade do modelo.
    """
    tela_raw = carregar_tela(None, _ID_TELA_H0044, _RAIZ_TELAS_DEMO)
    itens = None
    try:
        elementos = (tela_raw.get("corpo") or {}).get("elementos") or []
        for el in elementos:
            if isinstance(el, dict) and el.get("id") == "console_selecao":
                itens = el.get("itens")
                break
    except AttributeError:
        itens = None
    if itens is None:
        return modelo
    for elemento in modelo.corpo.elementos:
        if elemento.tipo == "console" and elemento.id == "console_selecao":
            elemento._campos_inertes["itens"] = list(itens)
            break
    return modelo


def _anexar_fluxo_h0044(estado, modelo):
    """Cria o coordenador focal e estabelece foco inicial em item_01."""
    contador = {"n": 0}

    def _recarregador(origem):
        contador["n"] += 1
        return _recarregador_focal_h0044(origem)

    fluxo = fluxo_execucao_mod.FluxoExecucao.criar_sessao(
        modelo,
        raiz_telas=_RAIZ_TELAS_DEMO,
        recarregador=_recarregador,
    )
    fluxo._contador_recarga_demo = contador  # observavel em testes
    lista = navegacao.lista_foco(modelo)
    novo = dict(estado)
    novo["fluxo_execucao"] = fluxo
    if lista:
        novo["foco_console"] = 0
        novo["cursores"] = {lista[0].id: 0}
        novo["selecoes"] = {lista[0].id: []}
        novo["pagina_atual"] = {lista[0].id: 1}
    return novo


def _chips_destacados_e_executar(estado):
    """Deriva ``chips_destacados``/``executar_disponivel`` do fluxo focal ativo.

    Extraido para reuso entre ``_reconciliar_paginacao_apos_resize`` e
    ``_com_geometria_real_do_console`` (H-0045-P06): ambos precisam do MESMO
    contexto de chips que o render seguinte vai usar, para que a geometria
    calculada por ``tela.renderizador.geometria_console`` reproduza
    exatamente ``l_barra``.
    """
    controle = estado.get("controle_execucao")
    if _controle_execucao_ativo(estado):
        return controle.contexto_renderizacao()
    fluxo = estado.get("fluxo_execucao")
    if fluxo is None or not isinstance(fluxo, fluxo_execucao_mod.FluxoExecucao):
        return None, None
    chips_destacados = fluxo.chips_destacados()
    executar_disponivel = None
    if not fluxo.resultado_ativo:
        executar_disponivel = fluxo.executar_disponivel(estado)
    return chips_destacados, executar_disponivel


def _com_geometria_real_do_console(nav_estado, modelo, console):
    """Injeta a largura/altura_interna REAIS do console focado (H-0045-P06).

    QA-H0045-P05-002: os comandos de pagina (``,``/``<``/``.``/``>``) e as
    setas consultavam ``tela.paginacao``/``tela.navegacao`` sem geometria
    explicita, caindo no fallback ``altura - 8`` de
    ``tela.paginacao._geometria_do_estado`` (e na largura TOTAL do terminal
    em vez da largura da coluna, em arranjo horizontal) -- capacidade e plano
    fisico divergentes do quadro que o render seguinte exibe. Autoridade
    UNICA: mesma ``tela.renderizador.geometria_console`` usada pela
    reconciliacao de resize (``_reconciliar_paginacao_apos_resize``) e,
    transitivamente, pelo proprio render (``_renderizar_container_
    horizontal``/``_renderizar_container_vertical`` particionam a mesma
    ``altura``/``largura`` do corpo). Nao-op quando ``console`` e ``None`` ou
    a geometria e insuficiente (preserva o estado corrente -- o render
    seguinte cairia no quadro minimo de qualquer forma).

    VM-H0045-R08-001 (P23): enquando a geometria estiver invalida (a barra de
    chips da tela corrente nao cabe nem no maximo de linhas declarado para
    ela), o comando dependente de geometria NAO pode deixar a excecao
    escapar, recalcular pagina a partir de medidas invalidas, deslocar cursor,
    mudar foco, perder selecao, alterar item logico ou corromper a pilha.
    Insuficiencia geometrica classificada (erro_layout) preserva o estado
    corrente integralmente -- o render seguinte exibe o quadro controlado de
    terminal insuficiente (``_resolver_conteudo``).

    Retorna ``(novo_estado, geometria)`` onde ``geometria`` e o dict
    ``{"largura", "altura_interna"}`` resolvido, ou ``None`` quando a
    geometria e insuficiente ou ``console`` e ``None``. Os chamadores de
    pagina/setas consultam o segundo elemento para decidir se podem operar
    sobre geometria valida ou se devem preservar o estado (no-op).
    """
    if console is None:
        return nav_estado, None
    chips_destacados, executar_disponivel = _chips_destacados_e_executar(nav_estado)
    try:
        geometria = geometria_console(
            modelo, nav_estado["estilo"],
            nav_estado.get("largura", 80), nav_estado.get("altura", 24),
            _verboso_efetivo(nav_estado, modelo),
            console=console,
            foco_console=nav_estado.get("foco_console"),
            cursores=nav_estado.get("cursores"),
            lista_foco=navegacao.lista_foco(modelo),
            selecoes=nav_estado.get("selecoes"),
            chips_destacados=chips_destacados,
            executar_disponivel=executar_disponivel,
            paginas_atuais=nav_estado.get("pagina_atual"),
        )
    except RenderizadorErro as exc:
        if _e_insuficiencia_geometrica(exc):
            return nav_estado, None
        raise
    if geometria is None:
        return nav_estado, None
    novo = dict(nav_estado)
    novo["largura"] = geometria["largura"]
    novo["altura_interna"] = geometria["altura_interna"]
    return novo, geometria


def _reconciliar_paginacao_apos_resize(estado, modelo):
    """H-0045-P03/P05: recalcula ``pagina_atual`` de todo console paginado apos resize.

    VM-H0045-R03-003: redimensionar o terminal muda a capacidade fisica por
    pagina (``altura_interna`` deriva de ``altura``); sem recalcular o NUMERO
    de pagina que contem o item logico do cursor, o quadro seguinte exibe a
    pagina antiga apenas clampada ao novo total, e o cursor deixa de aparecer
    em qualquer fragmento renderizado dessa pagina. Percorre todos os consoles
    paginados da lista de foco (nao so o focado): cada um mantem sua propria
    entrada em ``pagina_atual``/``cursores`` (paginas independentes).

    H-0045-P05/P06 (VM-H0045-R04-004 / QA-H0045-P05-001): a reconciliacao usa
    ``renderizador.geometria_console`` -- a MESMA autoridade de geometria
    (cabecalho + barra de menus + particionamento vertical/horizontal do
    corpo, incluindo a largura de COLUNA em arranjo horizontal) que o render
    seguinte vai usar -- em vez do fallback fixo ``altura - 8`` de
    ``tela.paginacao._geometria_do_estado`` e da largura total do terminal.
    Esse fallback assume implicitamente que a barra sempre ocupa 1 linha de
    chips e ignora particionamento horizontal; quando a barra real ocupa
    outro numero de linhas (largura estreita, ou o chip ``[✥]``
    aparecendo/desaparecendo no limiar de 1 item/pagina) ou o console vive em
    uma coluna horizontal, o fallback diverge da geometria real e a pagina
    reconciliada deixa de ser a pagina que o quadro seguinte exibe. Geometria
    insuficiente (``None``) preserva a pagina corrente sem reconciliar -- o
    render seguinte substitui a tela pelo quadro minimo (mesmo tratamento de
    ``RenderizadorErro`` em ``_resolver_conteudo``).

    VM-H0045-R08-001 (P23): durante o resize, a consulta de geometria NAO pode
    deixar escapar a excecao de insuficiencia geometrica (erro_layout da barra
    da tela corrente) ate o usuario -- isso encerraria a demonstracao com
    traceback. Insuficiencia geometrica classificada preserva selecao, foco,
    cursor, item logico, pagina, pilha e estado de execucao sem reconciliar;
    o quadro seguinte exibe o estado controlado de terminal insuficiente, e a
    recuperacao e automatica quando a geometria volta a ser suficiente. Outros
    ``RenderizadorErro`` (modelo/configuracao/campo/invariante) propagam.
    """
    lista = navegacao.lista_foco(modelo)
    consoles_paginados = [
        c for c in lista if c._campos_inertes.get("politica_paginacao") == "com"
    ]
    if not consoles_paginados:
        return estado

    largura = estado.get("largura", 80)
    altura = estado.get("altura", 24)
    chips_destacados, executar_disponivel = _chips_destacados_e_executar(estado)

    novo = estado
    for console in consoles_paginados:
        try:
            geometria = geometria_console(
                modelo, estado["estilo"], largura, altura,
                _verboso_efetivo(estado, modelo),
                console=console,
                foco_console=estado.get("foco_console"),
                cursores=estado.get("cursores"),
                lista_foco=lista,
                selecoes=estado.get("selecoes"),
                chips_destacados=chips_destacados,
                executar_disponivel=executar_disponivel,
                paginas_atuais=estado.get("pagina_atual"),
            )
        except RenderizadorErro as exc:
            if _e_insuficiencia_geometrica(exc):
                return estado
            raise
        if geometria is None:
            continue
        novo = paginacao.reconciliar_pagina_com_cursor(
            novo, console,
            altura_interna=geometria["altura_interna"],
            largura=geometria["largura"],
        )
    return novo


def _estabelecer_foco_paginacao_inicial(estado, modelo):
    """H-0045-P01: materializa foco no primeiro console paginado ao abrir.

    VM-H0045-01: ``python demo/demo.py h0045_paginacao_console_unico`` partia
    com ``foco_console=None``. Sem foco, ``[PgUp]``/``[PgDn]`` nao apareciam
    na barra (existencia avaliada so no console focado) e ``PageUp``/
    ``PageDown`` nao alteravam pagina (``console_focado`` ausente). Espelha
    o padrao de
    ``demo_navegacao``/``demo_selecao`` apenas para consoles com
    ``politica_paginacao: "com"``. Nao sobrescreve foco ja estabelecido via
    ``estado_inicial``.
    """
    if estado.get("foco_console") is not None:
        return estado
    lista = navegacao.lista_foco(modelo)
    if not lista:
        return estado
    if not any(
        c._campos_inertes.get("politica_paginacao") == "com" for c in lista
    ):
        return estado
    console = lista[0]
    novo = dict(estado)
    novo["foco_console"] = 0
    cursores = dict(estado.get("cursores") or {})
    cursores[console.id] = 0
    novo["cursores"] = cursores
    paginas = dict(estado.get("pagina_atual") or {})
    paginas.setdefault(console.id, 1)
    novo["pagina_atual"] = paginas
    return novo


def _modelo_corrente(estado, modelo):
    """Resolve o modelo a apresentar (origem ou resultado H-0044/H-0050)."""
    sessao_controle = estado.get("_sessao_resultado_controle")
    if sessao_controle is not None:
        return sessao_controle.modelo
    origem_controle = estado.get("_modelo_origem_controle")
    if origem_controle is not None:
        return origem_controle
    fluxo = estado.get("fluxo_execucao")
    if fluxo is not None and isinstance(fluxo, fluxo_execucao_mod.FluxoExecucao):
        if fluxo.resultado_ativo:
            return fluxo.modelo_resultado.modelo
        if fluxo.origem_ativa is not None:
            return fluxo.origem_ativa
    return modelo


def _resolver_entrada_tela(id_solicitado):
    """Resolve id de tela estrutural e eventual caso de validacao (H-0045).

    Casos ``h0045_validacao_*`` mapeados carregam o esqueleto/fixture JSON.
    VAZIO/CONTINUACAO usam fixture fixa propria; os quatro adaptativos
    legados mantêm esqueleto apenas para compatibilidade de testes.
    """
    caso_id = casos_val.id_caso_de_entrada(id_solicitado)
    if caso_id is None:
        return id_solicitado, None
    return casos_val.esqueleto_de_caso(caso_id), caso_id


def _console_principal(modelo):
    for elemento in modelo.corpo.elementos:
        if getattr(elemento, "tipo", None) == "console":
            return elemento
    return None


def _aplicar_caso_validacao_adaptativo(estado, modelo, caso_id):
    """Resolve W/C e injeta o caso em memoria (API de teste / legado).

    H-0045-P16: o loop TUI da demo NAO reinvoca este helper apos SIGWINCH.
    Casos fixos (VAZIO/CONTINUACAO) nao regeneram itens — apenas resolvem
    metadados geometricos sobre o modelo ja carregado do JSON.
    """
    console = _console_principal(modelo)
    if console is None:
        raise casos_val.GeometriaEfetivaAusente(
            "geometria efetiva do console nao resolvida"
        )
    largura = estado.get("largura", 80)
    altura = estado.get("altura", 24)
    verboso = _verboso_efetivo(estado, modelo)
    chips_destacados, executar_disponivel = _chips_destacados_e_executar(estado)
    lista = navegacao.lista_foco(modelo)

    if casos_val.caso_usa_modelo_fixo(caso_id):
        # Modelo fixo: mede geometria sem alterar itens/textos/IDs/politicas.
        geometria = geometria_console(
            modelo, estado["estilo"], largura, altura, verboso,
            console=console,
            foco_console=estado.get("foco_console"),
            cursores=estado.get("cursores"),
            lista_foco=lista,
            selecoes=estado.get("selecoes"),
            chips_destacados=chips_destacados,
            executar_disponivel=executar_disponivel,
            paginas_atuais=estado.get("pagina_atual"),
        )
        if geometria is None:
            raise casos_val.GeometriaEfetivaAusente(
                "geometria efetiva do console nao resolvida"
            )
        C = casos_val.capacidade_fisica_efetiva(geometria["altura_interna"])
        caso = casos_val.meta_caso_fixo(caso_id)
        caso = dict(caso)
        caso["W"] = None
        caso["C"] = C
        novo = dict(estado)
        novo["largura"] = largura
        novo["altura"] = altura
        novo["altura_interna"] = geometria["altura_interna"]
        novo["desconto_estrutural"] = estado.get(
            "desconto_estrutural", DESCONTO_ESTRUTURAL_CONSOLE
        )
        novo["caso_validacao_adaptativo"] = caso_id
        novo["caso_validacao_meta"] = {
            "W": None,
            "C": C,
            "rotulo": caso.get("rotulo"),
            "fenomeno": caso.get("fenomeno"),
            "modelo": "fixo",
        }
        return novo, caso

    itens_originais = list(console._campos_inertes.get("itens") or [])
    caso = None
    altura_interna = None
    try:
        console._campos_inertes["itens"] = []
        geometria = geometria_console(
            modelo, estado["estilo"], largura, altura, verboso,
            console=console,
            foco_console=estado.get("foco_console"),
            cursores=estado.get("cursores"),
            lista_foco=lista,
            selecoes=estado.get("selecoes"),
            chips_destacados=chips_destacados,
            executar_disponivel=executar_disponivel,
            paginas_atuais=estado.get("pagina_atual"),
        )
        if geometria is None:
            raise casos_val.GeometriaEfetivaAusente(
                "geometria efetiva do console nao resolvida"
            )
        largura_console = geometria["largura"]
        altura_interna = geometria["altura_interna"]
        C = casos_val.capacidade_fisica_efetiva(altura_interna)
        W = casos_val.resolver_largura_util_efetiva(
            console,
            largura_console,
            altura_interna,
            verboso=True,
            desconto_estrutural=estado.get(
                "desconto_estrutural", DESCONTO_ESTRUTURAL_CONSOLE
            ),
        )
        caso = casos_val.construir_caso(caso_id, W, C)
    finally:
        console._campos_inertes["itens"] = itens_originais

    casos_val.aplicar_caso_ao_modelo(modelo, caso)
    novo = dict(estado)
    novo["largura"] = largura
    novo["altura"] = altura
    novo["altura_interna"] = altura_interna
    novo["desconto_estrutural"] = estado.get(
        "desconto_estrutural", DESCONTO_ESTRUTURAL_CONSOLE
    )
    novo["foco_console"] = None
    novo["cursores"] = {}
    novo["pagina_atual"] = {}
    novo["caso_validacao_adaptativo"] = caso_id
    novo["caso_validacao_meta"] = {
        "W": caso.get("W"),
        "C": caso.get("C"),
        "rotulo": caso.get("rotulo"),
        "fenomeno": caso.get("fenomeno"),
    }
    return novo, caso


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

    H-0045-P16: ids ``h0045_validacao_*`` carregam fixture/esqueleto uma
    unica vez; SIGWINCH nao reconstrói o modelo logico.
    """
    id_estrutural, _caso_id = _resolver_entrada_tela(id_tela)
    if id_estrutural in _CATALOGO_CENARIOS_RESULTADO_EXECUCAO:
        fixture = _CATALOGO_CENARIOS_RESULTADO_EXECUCAO[id_estrutural]
        caminho_runtime = os.path.join(
            _DIR_FIXTURES_DEMO, fixture + ".json"
        )
        sessao = resultado_execucao_mod.carregar_sessao_resultado(
            None,
            id_estrutural,
            caminho_runtime,
            raiz_telas=_RAIZ_TELAS_DEMO,
            id_tela=_ID_TELA_RESULTADO_EXECUCAO,
        )
        return sessao.modelo

    tela_raw = carregar_tela(None, id_estrutural, _RAIZ_TELAS_DEMO)
    id_conteudo = id_conteudo_externo_de(id_estrutural)
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


# VM-H0045-R08-001 (P23): classificacao seletiva do erro de geometria.
# So erro de layout causado por insuficiencia geometrica da tela corrente
# (a barra de chips, mesmo no maximo de linhas daquela tela, nao cabe na
# largura/altura disponivel) pode gerar o estado controlado de terminal
# insuficiente. ``RenderizadorErro`` generico (modelo invalido, configuracao
# invalida, campo desconhecido, invariante quebrada) NAO e capturado aqui:
# deve continuar visivel e falhar os testes (ver ``_resolver_conteudo``).
# VM-H0045-R08-001 (P25): somente os formatos produzidos pelos pontos
# geometricos reais do renderer podem entrar no estado controlado. As regexes
# sao ancoradas na mensagem completa para que erros estruturais que apenas
# contenham ``erro_layout`` ou ``altura insuficiente`` continuem propagando.
_ERRO_LAYOUT_BARRA_RE = re.compile(
    r"^erro_layout: chips da barra_de_menus \(\d+\) nao cabem em \d+ "
    r"caracteres uteis \(content_w=-?\d+, margem=\d+\) com no maximo "
    r"\d+ linhas \(preenchimento=(?:coluna_a_coluna|linha_a_linha)\); "
    r"overflow\.quando_nao_couber='erro_layout' proibe "
    r"omitir/truncar/reordenar$"
)
_ERRO_ALTURA_CABECALHO_RE = re.compile(
    r"^altura insuficiente: terminal com \d+ linhas nao comporta "
    r"cabecalho \(\d+\) \+ barra_de_menus \(\d+\)$"
)
_ERRO_ALTURA_CORPO_RE = re.compile(
    r"^altura insuficiente: corpo requer \d+ linhas mas area disponivel e "
    r"-?\d+ linhas \(altura=\d+, cabecalho=\d+, barra=\d+\)$"
)


def _e_insuficiencia_geometrica(exc):
    """True quando ``exc`` e erro de insuficiencia geometrica da tela corrente.

    Classificacao exata (P25 / VM-H0045-R08-001): reconhece somente a
    mensagem completa produzida por ``_linhas_barra`` para overflow da barra
    de menus ou pelas duas verificacoes reais de altura em
    ``tela.renderizador.renderizar_tela``. DA-01, DA-02, DA-04, mensagens
    sinteticas e erros estruturais nao sao produtores aceitos.
    """
    if not isinstance(exc, RenderizadorErro):
        return False
    msg = str(exc).strip()
    return bool(
        _ERRO_LAYOUT_BARRA_RE.fullmatch(msg)
        or _ERRO_ALTURA_CABECALHO_RE.fullmatch(msg)
        or _ERRO_ALTURA_CORPO_RE.fullmatch(msg)
    )


def _quadro_terminal_insuficiente(largura, altura):
    """Gera o quadro controlado de terminal insuficiente (P23 / VM-H0045-R08-001).

    Diferentemente do quadro minimo global (terminal fisicamente pequeno,
    ADR-0017), este quadro sinaliza que a TELA CORRENTE nao pode ser
    representada mesmo na altura maxima da barra permitida para ela: a
    interface normal e integralmente substituida por uma mensagem controlada,
    SEM traceback, SEM congelar o ultimo quadro valido e SEM alterar o estado
    logico. A recuperacao e automatica quando a geometria volta a ser
    suficiente (ver ``_resolver_conteudo`` e o trecho de resize em ``main``).

    A mensagem e adequada a geometria disponivel: cabe em duas linhas quando
    possivel; em dimensoes extremas, produz a menor saida segura possivel
    dentro das linhas e colunas existentes, sem lancar nova excecao.
    """
    titulo = "Terminal pequeno demais"
    subtitulo = "Aumente a janela para continuar"
    if altura is None or altura < 1:
        altura = 1
    if largura is None or largura < 1:
        largura = 1

    def _linha(texto):
        return (texto or "")[:largura].ljust(largura)

    linhas = []
    if altura >= 1:
        linhas.append(_linha(titulo))
    if altura >= 2:
        linhas.append(_linha(subtitulo))
    # Preenchimento restante com linhas em branco para ocupar exatamente
    # ``altura`` linhas fisicas e apagar qualquer residuo do quadro anterior.
    while len(linhas) < altura:
        linhas.append(" " * largura)
    return "\n".join(linhas) + "\n"


def _e_erro_layout_barra(exc):
    """True somente para a mensagem completa do produtor da barra."""
    if not isinstance(exc, RenderizadorErro):
        return False
    return bool(_ERRO_LAYOUT_BARRA_RE.fullmatch(str(exc).strip()))


def _resolver_conteudo(estado, modelo, largura, altura):
    """Resolve o conteudo a apresentar para as dimensoes correntes.

    Todas as insuficiencias geometricas aceitas usam o quadro controlado
    unificado. Qualquer ``RenderizadorErro`` que nao seja um produtor
    geometrico real reconhecido por ``_e_insuficiencia_geometrica`` e
    relancado com a excecao original.
    """
    modelo = _modelo_corrente(estado, modelo)
    if _tela_pequena_demais(largura, altura):
        return _quadro_terminal_insuficiente(largura, altura)
    try:
        conteudo = renderizar_estado(estado, modelo, largura, altura=altura)
        # Alguns caminhos legados do renderer sinalizam inviabilidade
        # geométrica do corpo retornando o quadro mínimo, em vez de lançar
        # RenderizadorErro. Converta somente esse quadro sentinela, sem
        # inspecionar mensagens estruturais, para manter a apresentação
        # unificada também na altura insuficiente material.
        if conteudo == _quadro_minimo_aviso(largura, altura):
            return _quadro_terminal_insuficiente(largura, altura)
        return conteudo
    except RenderizadorErro as exc:
        if _e_insuficiencia_geometrica(exc):
            return _quadro_terminal_insuficiente(largura, altura)
        raise


def _apresentar_quadro(conteudo, largura=None, altura=None):
    """Apresenta um quadro completo por posicionamento absoluto linha a linha.

    Cada linha e precedida por CSI n;1H (posicionamento absoluto na coluna 1)
    e preenchida com espacos ate a largura do terminal. O preenchimento conta
    apenas caracteres visiveis (sem SGR ANSI), para linhas com chips coloridos
    apagarem a area anteriormente ocupada apos resize (H-0045-P02). Apos o
    pad, ``CSI K`` apaga restos a direita do cursor. Quando ``altura`` e
    fornecida e maior que o numero de linhas do conteudo, as linhas abaixo
    sao sobrescritas com espacos (residual vertical apos reducao). Todo o
    conteudo e emitido em uma unica chamada write() seguida de uma unica
    flush(). Synchronized output (ESC[?2026h/l) envolve o conteudo de cada
    quadro. Nao usa \\n como mecanismo de quebra de linha (ADR-0016 item 5).

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
        pad = w - _largura_sem_ansi(linha)
        partes.append(linha + (" " * pad if pad > 0 else ""))
        # Apaga qualquer residuo a direita (borda antiga apos reducao).
        partes.append("\x1b[K")
    if altura is not None and altura > len(linhas):
        linha_vazia = " " * w
        for i in range(len(linhas) + 1, altura + 1):
            partes.append("\x1b[{0};1H".format(i))
            partes.append(linha_vazia)
            partes.append("\x1b[K")
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
    # H-0045-P16: valida desativacao de casos adaptativos legados; telas
    # vigentes carregam modelo fixo uma unica vez (sem regeneracao).
    casos_val.id_caso_de_entrada(tela_inicial)
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _preparar_estado_h0053(estado, modelo)
    if estado["tela_atual"] == _ID_TELA_H0044:
        estado = _anexar_fluxo_h0044(estado, modelo)
    else:
        estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
        estado = _anexar_controle_execucao(estado, modelo)
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
                            # H-0045-P16 / §19.1: SIGWINCH recalcula somente
                            # geometria, quebras fisicas, paginas, quadro e
                            # reconciliacao de cursor/pagina — nunca reconstrói
                            # textos, IDs, itens, ordem ou politicas.
                            estado = _reconciliar_paginacao_apos_resize(
                                estado, _modelo_corrente(estado, modelo)
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
                    ramos_fechados_antes = dict(
                        estado.get("ramos_fechados", {})
                    )
                    paginas_antes = dict(estado.get("pagina_atual", {}))
                    fluxo_antes = estado.get("fluxo_execucao")
                    controle_antes = estado.get("controle_execucao")
                    modo_controle_antes = getattr(
                        controle_antes, "modo_atual", None
                    )
                    dry_antes = bool(
                        getattr(fluxo_antes, "dry_run_ativo", False)
                    )
                    resultado_antes = bool(
                        getattr(fluxo_antes, "resultado_ativo", False)
                    )
                    resultado_controle_antes = _resultado_controle_ativo(estado)
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
                        if estado["tela_atual"] == _ID_TELA_H0044:
                            estado = _anexar_fluxo_h0044(estado, modelo)
                        else:
                            estado = _anexar_controle_execucao(estado, modelo)
                        if estado.get("modo_verboso_forcado") is True:
                            estado = dict(estado, modo_verboso=True)
                        else:
                            estado = dict(
                                estado,
                                modo_verboso=_modo_verboso_de_modelo(modelo),
                            )
                    modelo = _modelo_corrente(estado, modelo)
                    fluxo_depois = estado.get("fluxo_execucao")
                    dry_mudou = bool(
                        getattr(fluxo_depois, "dry_run_ativo", False)
                    ) != dry_antes
                    resultado_mudou = bool(
                        getattr(fluxo_depois, "resultado_ativo", False)
                    ) != resultado_antes
                    resultado_controle_mudou = (
                        _resultado_controle_ativo(estado)
                        != resultado_controle_antes
                    )
                    controle_depois = estado.get("controle_execucao")
                    controle_mudou = getattr(
                        controle_depois, "modo_atual", None
                    ) != modo_controle_antes
                    verboso_mudou = estado.get("modo_verboso", False) != verboso_antes
                    foco_mudou = estado.get("foco_console") != foco_antes
                    cursores_mudou = estado.get("cursores", {}) != cursores_antes
                    selecoes_mudou = estado.get("selecoes", {}) != selecoes_antes
                    ramos_fechados_mudou = (
                        estado.get("ramos_fechados", {})
                        != ramos_fechados_antes
                    )
                    paginas_mudou = estado.get("pagina_atual", {}) != paginas_antes
                    if (
                        estado["tela_atual"] != tela_antes
                        or verboso_mudou
                        or foco_mudou
                        or cursores_mudou
                        or selecoes_mudou
                        or ramos_fechados_mudou
                        or paginas_mudou
                        or dry_mudou
                        or resultado_mudou
                        or resultado_controle_mudou
                        or controle_mudou
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
            ramos_fechados_antes = dict(
                estado.get("ramos_fechados", {})
            )
            paginas_antes = dict(estado.get("pagina_atual", {}))
            fluxo_antes = estado.get("fluxo_execucao")
            controle_antes = estado.get("controle_execucao")
            modo_controle_antes = getattr(controle_antes, "modo_atual", None)
            dry_antes = bool(getattr(fluxo_antes, "dry_run_ativo", False))
            resultado_antes = bool(
                getattr(fluxo_antes, "resultado_ativo", False)
            )
            resultado_controle_antes = _resultado_controle_ativo(estado)
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
                if estado["tela_atual"] == _ID_TELA_H0044:
                    estado = _anexar_fluxo_h0044(estado, modelo)
                else:
                    estado = _anexar_controle_execucao(estado, modelo)
                if estado.get("modo_verboso_forcado") is True:
                    estado = dict(estado, modo_verboso=True)
                else:
                    estado = dict(
                        estado,
                        modo_verboso=_modo_verboso_de_modelo(modelo),
                    )
            modelo = _modelo_corrente(estado, modelo)
            fluxo_depois = estado.get("fluxo_execucao")
            dry_mudou = bool(
                getattr(fluxo_depois, "dry_run_ativo", False)
            ) != dry_antes
            resultado_mudou = bool(
                getattr(fluxo_depois, "resultado_ativo", False)
            ) != resultado_antes
            resultado_controle_mudou = (
                _resultado_controle_ativo(estado) != resultado_controle_antes
            )
            controle_depois = estado.get("controle_execucao")
            controle_mudou = getattr(
                controle_depois, "modo_atual", None
            ) != modo_controle_antes
            verboso_mudou = estado.get("modo_verboso", False) != verboso_antes
            foco_mudou = estado.get("foco_console") != foco_antes
            cursores_mudou = estado.get("cursores", {}) != cursores_antes
            selecoes_mudou = estado.get("selecoes", {}) != selecoes_antes
            ramos_fechados_mudou = (
                estado.get("ramos_fechados", {})
                != ramos_fechados_antes
            )
            paginas_mudou = estado.get("pagina_atual", {}) != paginas_antes
            if (
                estado["tela_atual"] != tela_antes
                or verboso_mudou
                or foco_mudou
                or cursores_mudou
                or selecoes_mudou
                or ramos_fechados_mudou
                or paginas_mudou
                or dry_mudou
                or resultado_mudou
                or resultado_controle_mudou
                or controle_mudou
            ):
                print(_resolver_conteudo(estado, modelo, largura, altura), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
