"""Aplicacao demonstravel minima com borda/sair e navegacao minima
(H-0008 / H-0009 / H-0010A / H-0022).

Ponto de entrada executavel local que exercita a API entregue pelo
renderer (``renderizar_tela``) sobre a tela raiz do Orquestrador e a tela
destino minima, permitindo alternar em memoria entre borda curva e reta,
abrir a tela destino via chip do lancador e voltar via Esc.

Encadeamento do pipeline herdado:

    config/telas/<id_tela>.json
        -> carregar_tela(None, id_tela)         [tela/loader.py       - H-0001]
        -> construir_modelo(tela_raw)           [tela/modelo.py       - H-0002]
        -> ModeloTela
        -> renderizar_tela(modelo, tipo_borda)  [tela/renderizador.py - H-0006/H-0007/H-0009/H-0010A]
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
- Estado ganha ``tela_atual`` (default ``"orquestrador"``) e
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
- ``main()`` recarrega o modelo via ``carregar_tela(None, tela_atual)``
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

A apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

import os
import shutil
import select
import termios
import tty

from tela.loader import carregar_tela
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela


def criar_estado_inicial():
    """Retorna o estado inicial da demonstracao.

    Retorna sempre um novo dict independente a cada chamada, sem estado
    global mutavel, sem leitura de arquivo, JSON ou sys.stdin. Campos:

    - ``tipo_borda``: ``"curva"`` (default do renderer).
    - ``saindo``: ``False``.
    - ``tela_atual``: ``"orquestrador"`` (tela raiz).
    - ``pilha_telas``: ``[]`` (sem telas empilhadas).
    """
    return {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "orquestrador",
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
        (``"orquestrador"`` e ``[]``).
    """
    novo = {
        "tipo_borda": estado["tipo_borda"],
        "saindo": estado["saindo"],
        "tela_atual": estado.get("tela_atual", "orquestrador"),
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


def _carregar_modelo_por_id(id_tela):
    """Helper: carrega e constroi o ModeloTela para ``id_tela``."""
    tela_raw = carregar_tela(None, id_tela)
    return construir_modelo(tela_raw)


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


def _iniciar_sessao_tui(fd_stdin):
    """Salva estado TTY, ativa cbreak mode e entra em alternate screen.

    Usa ``tty.setcbreak`` (preserva OPOST e ISIG; rejeita modo raw).
    Desativa autowrap (ESC[?7l) e limpa a tela uma unica vez (ESC[2J).
    Retorna os atributos originais do terminal para restauracao posterior.
    """
    atributos_originais = termios.tcgetattr(fd_stdin)
    tty.setcbreak(fd_stdin)
    sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J\x1b[H")
    sys.stdout.flush()
    return atributos_originais


def _encerrar_sessao_tui(fd_stdin, atributos_originais):
    """Restaura atributos TTY, autowrap, cursor e encerra alternate screen.

    Executa cada passo em bloco try separado para garantir restauracao
    mesmo que uma das etapas falhe.
    """
    try:
        termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)
    except Exception:
        pass
    try:
        sys.stdout.write("\x1b[?7h\x1b[?25h\x1b[?1049l")
        sys.stdout.flush()
    except Exception:
        pass


def _apresentar_quadro(conteudo):
    """Apresenta um quadro completo por posicionamento absoluto linha a linha.

    Cada linha e precedida por CSI n;1H (posicionamento absoluto na coluna 1)
    e preenchida com espacos ate a largura do terminal. Todo o conteudo e
    emitido em uma unica chamada write() seguida de uma unica flush().
    Synchronized output (ESC[?2026h/l) envolve o conteudo de cada quadro.
    Nao usa \\n como mecanismo de quebra de linha (ADR-0016 item 5).
    """
    w = shutil.get_terminal_size(fallback=(80, 24)).columns
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


def main():
    """Entrada principal da aplicacao demonstravel.

    Renderiza com a largura e altura reais do terminal. Em TTY interativo
    (stdin e stdout sao TTY), ativa alternate screen, oculta cursor,
    desativa autowrap e entra em cbreak mode para a duracao da sessao;
    cada quadro e apresentado por posicionamento absoluto linha a linha
    com escrita atomica (synchronized output); KeyboardInterrupt no loop
    principal e capturado e ignorado silenciosamente (sessao continua);
    o terminal e restaurado em ``finally``. Fora de TTY (pipe/teste),
    usa leitura linha a linha e ``print`` normal. Retorna 0 (saida limpa).
    """
    estado = criar_estado_inicial()
    tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
    largura = tamanho_terminal.columns
    altura = tamanho_terminal.lines
    modelo = _carregar_modelo_por_id(estado["tela_atual"])

    if sys.stdin.isatty() and sys.stdout.isatty():
        fd = sys.stdin.fileno()
        atributos_originais = _iniciar_sessao_tui(fd)
        try:
            _apresentar_quadro(renderizar_estado(estado, modelo, largura, altura=altura))
            while True:
                try:
                    ch = _ler_tecla_sessao()
                    tela_antes = estado["tela_atual"]
                    estado = processar_comando(estado, ch, modelo)
                    if estado["saindo"]:
                        break
                    if estado["tela_atual"] != tela_antes:
                        modelo = _carregar_modelo_por_id(estado["tela_atual"])
                    if ch == "b" or estado["tela_atual"] != tela_antes:
                        _apresentar_quadro(renderizar_estado(estado, modelo, largura, altura=altura))
                except KeyboardInterrupt:
                    continue
        finally:
            _encerrar_sessao_tui(fd, atributos_originais)
    else:
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
