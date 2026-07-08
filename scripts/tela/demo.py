"""Aplicacao demonstravel minima com borda/sair e navegacao minima
(H-0008 / H-0009 / H-0010A).

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

A apenas biblioteca padrao do Python.
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


def renderizar_estado(estado, modelo, largura=None):
    """Delega para o renderer usando a borda do estado e a largura dada.

    Nao modifica ``estado`` nem ``modelo``. Nenhum efeito colateral
    alem da chamada a ``renderizar_tela``. ``largura=None`` produz
    saida deterministica com fallback 42 chars.
    """
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"], largura=largura)


def _carregar_modelo_por_id(id_tela):
    """Helper: carrega e constroi o ModeloTela para ``id_tela``."""
    tela_raw = carregar_tela(None, id_tela)
    return construir_modelo(tela_raw)


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
    vez em modo raw (sem Enter, sem echo): ``b`` alterna a borda; o
    ``chip`` de algum item de lancador abre a tela destino; ``Esc``
    (``"\\x1b"``) volta ou sai conforme o estado da pilha. Fora de TTY
    (pipe/teste), le linha a linha. Apos alternar borda ou mudar de
    tela, renderiza e imprime o novo estado. Retorna 0 (saida limpa).
    """
    estado = criar_estado_inicial()
    largura = shutil.get_terminal_size(fallback=(80, 24)).columns
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    print(renderizar_estado(estado, modelo, largura), end="")

    if sys.stdin.isatty():
        while True:
            ch = _ler_tecla_unica()
            tela_antes = estado["tela_atual"]
            estado = processar_comando(estado, ch, modelo)
            if estado["saindo"]:
                break
            if estado["tela_atual"] != tela_antes:
                modelo = _carregar_modelo_por_id(estado["tela_atual"])
            if ch == "b" or estado["tela_atual"] != tela_antes:
                print(renderizar_estado(estado, modelo, largura), end="")
    else:
        for linha in sys.stdin:
            comando = linha.strip()
            tela_antes = estado["tela_atual"]
            estado = processar_comando(estado, comando, modelo)
            if estado["saindo"]:
                break
            if estado["tela_atual"] != tela_antes:
                modelo = _carregar_modelo_por_id(estado["tela_atual"])
            if comando == "b" or estado["tela_atual"] != tela_antes:
                print(renderizar_estado(estado, modelo, largura), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
