"""Aplicacao demonstravel minima com borda/sair (H-0008).

Ponto de entrada executavel local que exercita a API entregue pelo
H-0007 (``renderizar_tela``) sobre a tela raiz do Orquestrador,
permitindo alternar em memoria entre borda curva e reta e sair.

Encadeamento do pipeline herdado:

    config/telas/orquestrador.json
        -> carregar_tela(None, "orquestrador")   [tela/loader.py       - H-0001]
        -> construir_modelo(tela_raw)            [tela/modelo.py       - H-0002]
        -> ModeloTela
        -> renderizar_tela(modelo, tipo_borda)   [tela/renderizador.py - H-0006/H-0007]
        -> str

ESCOPO (H-0008):
- Aplicacao demonstravel local minima, separada de tela/diagnostico.py.
- Renderiza inicialmente com borda curva (default H-0006/H-0007).
- Aceita o comando interno ``b`` para alternar curva <-> reta em memoria.
- Aceita o comando interno ``s`` para sair.
- Le comandos de sys.stdin linha a linha (suporta uso via pipe).
- Estado de borda mantido somente em memoria; nao grava arquivo,
  nao altera JSON, nao persiste preferencia.
- Nao usa bibliotecas externas de UI nem pacotes de terminal; apenas
  biblioteca padrao do Python.
- Nao imprime prompt interativo (sem input()).
- Os comandos ``b`` e ``s`` sao internos da demo H-0008: nao sao
  bindings declarativos, nao sao registry de acoes, nao sao acoes
  genéricas e nao concretizam os chips inertes ``[B] Borda`` e
  ``[Esc] Sair`` do JSON.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

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
        ``"s"`` define ``saindo=True`` sem alterar ``tipo_borda``.
        qualquer outro (incluindo string vazia) retorna copia sem alteracao.
    """
    novo = {"tipo_borda": estado["tipo_borda"], "saindo": estado["saindo"]}
    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
    elif comando == "s":
        novo["saindo"] = True
    return novo


def renderizar_estado(estado, modelo):
    """Delega para a API H-0007 usando a borda do estado.

    Nao modifica ``estado`` nem ``modelo``. Nenhum efeito colateral
    alem da chamada a ``renderizar_tela``.
    """
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"])


def main():
    """Entrada principal da aplicacao demonstravel.

    Renderiza inicialmente com borda curva, itera sobre sys.stdin linha
    a linha, alternando a borda com ``b`` e encerrando com ``s``.
    Retorna 0 (saida limpa).
    """
    tela_raw = carregar_tela(None, "orquestrador")
    modelo = construir_modelo(tela_raw)
    estado = criar_estado_inicial()
    print(renderizar_estado(estado, modelo), end="")
    for linha in sys.stdin:
        comando = linha.strip()
        novo_estado = processar_comando(estado, comando)
        estado = novo_estado
        if estado["saindo"]:
            break
        if comando == "b":
            print(renderizar_estado(estado, modelo), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
