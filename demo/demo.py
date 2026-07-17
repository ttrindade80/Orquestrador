"""Aplicacao demonstravel minima com borda/sair e navegacao minima
(H-0008 / H-0009 / H-0010A / H-0022 / H-0023).

Ponto de entrada executavel da demonstracao. Exercita a API entregue pelo
renderer (``renderizar_tela``) sobre a tela raiz demonstrativa e a tela
destino minima, permitindo alternar em memoria entre borda curva e reta,
abrir a tela destino via chip do lancador e voltar via Esc.

Executavel via: python demo/demo.py

Encadeamento do pipeline:

    config/telas/demo/<id_tela>.json
        -> carregar_tela(None, id_tela, raiz_telas)  [tela/loader.py       - H-0001]
        -> construir_modelo(tela_raw)                [tela/modelo.py       - H-0002]
        -> ModeloTela
        -> renderizar_tela(modelo, tipo_borda)       [tela/renderizador.py - H-0006/H-0007/H-0009/H-0010A]
        -> str

ESCOPO (H-0008):
- Aplicacao demonstravel local minima, separada de tela/diagnostico.py.
- Renderiza inicialmente com borda curva (default H-0006/H-0007).
- Aceita o comando interno ``b`` para alternar curva <-> reta em memoria.
- Aceita o comando interno ``s`` para sair (atalho auxiliar para pipe).
- Estado de borda mantido somente em memoria; nao grava arquivo,
  nao altera JSON, nao persiste preferencia.
- Os comandos ``b`` e ``s`` sao internos da demo: nao sao bindings
  declarativos, nao sao registry de acoes.

ADICOES DO H-0009:
- Largura visual lida do terminal via ``shutil.get_terminal_size``.
- Deteccao de TTY via ``sys.stdin.isatty() and sys.stdout.isatty()``:
  - Em TTY: leitura por tecla unica em modo cbreak (``termios``/``tty``),
    sem Enter e sem echo; ISIG preservado (Ctrl+C gera KeyboardInterrupt
    capturado silenciosamente no loop); ``b`` alterna a borda; ``Esc``
    sai; terminal restaurado em ``finally``.
  - Fora de TTY (pipe/teste): leitura linha a linha preservada, com
    ``s`` e ``"\\x1b"`` como comandos de saida.
- ``processar_comando`` aceita ``"\\x1b"`` como saida (mantendo
  ``tipo_borda``); ``"s"`` permanece como atalho auxiliar.
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

from tela.loader import carregar_tela, carregar_conteudo_externo
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela, RenderizadorErro

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
}


def criar_estado_inicial():
    """Retorna o estado inicial da demonstracao.

    Retorna sempre um novo dict independente a cada chamada, sem estado
    global mutavel, sem leitura de arquivo, JSON ou sys.stdin. Campos:

    - ``tipo_borda``: ``"curva"`` (default do renderer).
    - ``saindo``: ``False``.
    - ``tela_atual``: ``"demo"`` (tela raiz da demonstracao).
    - ``pilha_telas``: ``[]`` (sem telas empilhadas).
    """
    return {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "demo",
        "pilha_telas": [],
    }


def processar_comando(estado, comando, modelo=None):
    """Processa um comando sobre o estado, retornando um novo dict.

    Nao modifica o dict ``estado`` recebido como argumento. Retorna
    sempre um novo dict independente com as chaves ``"tipo_borda"``,
    ``"saindo"``, ``"tela_atual"`` e ``"pilha_telas"``.

    Comportamento (case-sensitive):

    - ``"b"`` alterna ``tipo_borda``: curva -> reta ou reta -> curva.
      Nao altera ``saindo`` nem ``tela_atual`` nem ``pilha_telas``.
    - ``"s"`` ou ``"\\x1b"`` (Esc):
      - Se ``pilha_telas`` nao vazia: faz pop; ``tela_atual`` passa a
        ser o ultimo elemento removido da pilha; ``saindo`` permanece
        ``False``.
      - Se ``pilha_telas`` vazia: define ``saindo = True`` (sai).
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
        (``"demo"`` e ``[]``).
    """
    novo = {
        "tipo_borda": estado["tipo_borda"],
        "saindo": estado["saindo"],
        "tela_atual": estado.get("tela_atual", "demo"),
        "pilha_telas": list(estado.get("pilha_telas", [])),
    }

    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
        return novo

    if comando == "s" or comando == "\x1b":
        if novo["pilha_telas"]:
            novo["tela_atual"] = novo["pilha_telas"][-1]
            novo["pilha_telas"] = novo["pilha_telas"][:-1]
        else:
            novo["saindo"] = True
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
    """Delega para o renderer usando a borda do estado e a largura dada.

    Nao modifica ``estado`` nem ``modelo``. Nenhum efeito colateral
    alem da chamada a ``renderizar_tela``. ``largura=None`` produz
    saida deterministica com fallback 42 chars. ``altura=None``
    preserva o comportamento atual (sem preenchimento vertical); quando
    fornecida, repassa a altura ao renderer para a ocupacao vertical da
    janela do terminal pelo corpo (H-0015 / ADR-0013).
    """
    return renderizar_tela(
        modelo, tipo_borda=estado["tipo_borda"], largura=largura, altura=altura
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
    """
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


def main(argv=None):
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
    tela_inicial = _tela_inicial_de_argv(argv)
    if tela_inicial != estado["tela_atual"]:
        estado = dict(estado, tela_atual=tela_inicial)
    modelo = _carregar_modelo_por_id(estado["tela_atual"])

    if sys.stdin.isatty() and sys.stdout.isatty():
        fd = sys.stdin.fileno()
        largura, altura = _obter_dimensoes_iniciais(fd)
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
                            _apresentar_quadro(
                                _resolver_conteudo(estado, modelo, largura, altura),
                                largura,
                            )
                        if fd not in prontos:
                            continue
                    ch = _ler_tecla_sessao(fd=fd)
                    tela_antes = estado["tela_atual"]
                    estado = processar_comando(estado, ch, modelo)
                    if estado["saindo"]:
                        break
                    if estado["tela_atual"] != tela_antes:
                        modelo = _carregar_modelo_por_id(estado["tela_atual"])
                    if ch == "b" or estado["tela_atual"] != tela_antes:
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
        print(renderizar_estado(estado, modelo, largura, altura=altura), end="")
        for linha in sys.stdin:
            comando = linha.strip()
            tela_antes = estado["tela_atual"]
            estado = processar_comando(estado, comando, modelo)
            if estado["saindo"]:
                break
            if estado["tela_atual"] != tela_antes:
                modelo = _carregar_modelo_por_id(estado["tela_atual"])
            if comando == "b" or estado["tela_atual"] != tela_antes:
                print(renderizar_estado(estado, modelo, largura, altura=altura), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
