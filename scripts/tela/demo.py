"""Aplicacao demonstravel minima com borda/sair (H-0008 / H-0009).

Ponto de entrada executavel local que exercita a API entregue pelo
H-0007 (``renderizar_tela``) sobre a tela raiz do Orquestrador,
permitindo alternar em memoria entre borda curva e reta e sair.

Encadeamento do pipeline herdado:

    config/telas/orquestrador.json
        -> carregar_tela(None, "orquestrador")   [tela/loader.py       - H-0001]
        -> construir_modelo(tela_raw)            [tela/modelo.py       - H-0002]
        -> ModeloTela
        -> renderizar_tela(modelo, tipo_borda)   [tela/renderizador.py - H-0006/H-0007/H-0009]
        -> str

ESCOPO (H-0008):
- Aplicacao demonstravel local minima, separada de tela/diagnostico.py.
- Renderiza inicialmente com borda curva (default H-0006/H-0007).
- Aceita o comando interno ``b`` para alternar curva <-> reta em memoria.
- Aceita o comando interno ``s`` para sair (atalho auxiliar para pipe).
- Estado de borda mantido somente em memoria; nao grava arquivo,
  nao altera JSON, nao persiste preferencia.
- Os comandos ``b`` e ``s`` sao internos da demo: nao sao bindings
  declarativos, nao sao registry de acoes e nao concretizam os chips
  inertes ``[B] Borda`` e ``[Esc] Sair`` do JSON.

ADICOES DO H-0009:
- Largura visual lida do terminal via ``shutil.get_terminal_size``.
- Deteccao de TTY via ``sys.stdin.isatty()``:
  - Em TTY: leitura por tecla unica em modo raw (``termios``/``tty``),
    sem Enter e sem echo; ``b`` alterna a borda; ``Esc`` (``"\\x1b"``)
    sai imediatamente; o terminal e sempre restaurado em ``finally``.
  - Fora de TTY (pipe/teste): leitura linha a linha preservada, com
    ``s`` e ``"\\x1b"`` como comandos de saida.
- ``processar_comando`` aceita ``"\\x1b"`` como saida (mantendo
  ``tipo_borda``); ``"s"`` permanece como atalho auxiliar.
- ``renderizar_estado`` aceita ``largura`` opcional repassada ao
  renderer.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

import shutil
import termios
import tty

from tela.loader import carregar_tela
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela


def criar_estado_inicial():
    """Retorna o estado inicial da demonstracao.

    Retorna sempre um novo dict independente a cada chamada, sem estado
    global mutavel, sem leitura de arquivo, JSON ou sys.stdin.
    """
    return {"tipo_borda": "curva", "saindo": False}


def processar_comando(estado, comando):
    """Processa um comando sobre o estado, retornando um novo dict.

    Nao modifica o dict ``estado`` recebido como argumento. Retorna
    sempre um novo dict com as chaves ``"tipo_borda"`` e ``"saindo"``.

    Comandos (case-sensitive):
        ``"b"`` alterna ``tipo_borda``: curva -> reta ou reta -> curva.
        ``"s"`` define ``saindo=True`` sem alterar ``tipo_borda``
              (atalho auxiliar para pipe/testes sem TTY).
        ``"\\x1b"`` (Esc) define ``saindo=True`` sem alterar ``tipo_borda``.
        qualquer outro (incluindo string vazia) retorna copia sem alteracao.
    """
    novo = {"tipo_borda": estado["tipo_borda"], "saindo": estado["saindo"]}
    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
    elif comando == "s" or comando == "\x1b":
        novo["saindo"] = True
    return novo


def renderizar_estado(estado, modelo, largura=None):
    """Delega para a API H-0009 usando a borda do estado e a largura dada.

    Nao modifica ``estado`` nem ``modelo``. Nenhum efeito colateral
    alem da chamada a ``renderizar_tela``. ``largura=None`` produz
    saida deterministica com fallback 42 chars.
    """
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"], largura=largura)


def _ler_tecla_unica():
    """Le exatamente um caractere de stdin em modo raw, sem echo.

    Entra em modo raw (``tty.setraw``) sobre o file descriptor de
    stdin, le um caractere com ``sys.stdin.read(1)`` e restaura o
    estado original do terminal em ``finally`` (garantindo restauracao
    mesmo em caso de excecao). Retorna o caractere lido como ``str``.
    """
    fd = sys.stdin.fileno()
    config_original = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, config_original)
    return ch


def main():
    """Entrada principal da aplicacao demonstravel.

    Renderiza inicialmente com borda curva usando a largura real do
    terminal (``shutil.get_terminal_size``). Em TTY, le tecla unica por
    vez em modo raw (sem Enter, sem echo): ``b`` alterna a borda e
    ``Esc`` (``"\\x1b"``) sai. Fora de TTY (pipe/teste), le linha a
    linha, aceitando ``b``, ``s`` e ``"\\x1b"``. Retorna 0 (saida limpa).
    """
    tela_raw = carregar_tela(None, "orquestrador")
    modelo = construir_modelo(tela_raw)
    estado = criar_estado_inicial()
    largura = shutil.get_terminal_size(fallback=(80, 24)).columns
    print(renderizar_estado(estado, modelo, largura), end="")

    if sys.stdin.isatty():
        while True:
            ch = _ler_tecla_unica()
            estado = processar_comando(estado, ch)
            if estado["saindo"]:
                break
            if ch == "b":
                print(renderizar_estado(estado, modelo, largura), end="")
    else:
        for linha in sys.stdin:
            comando = linha.strip()
            estado = processar_comando(estado, comando)
            if estado["saindo"]:
                break
            if comando == "b":
                print(renderizar_estado(estado, modelo, largura), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
