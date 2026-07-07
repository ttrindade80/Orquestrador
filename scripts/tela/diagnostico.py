"""Diagnostico executavel da tela raiz (H-0004).

Ponto de entrada unico e auditavel que encadeia o pipeline completo
dos handoffs anteriores sobre a tela raiz do Orquestrador:

    config/telas/orquestrador.json
        -> carregar_tela(None, id_tela)        [tela/loader.py      - H-0001]
        -> construir_modelo(tela_raw)         [tela/modelo.py      - H-0002]
        -> renderizar_tela(modelo)            [tela/renderizador.py - H-0003]
        -> str

ESCOPO (H-0004):
- Apenas o encadeamento acima. Nenhuma logica de negocio e adicionada.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo, nao
  consulta JSON diretamente (isso fica a cargo do loader).
- Excecoes dos modulos subjacentes propagam naturalmente para o
  chamador (Tela*, ModeloTelaErro, RenderizadorErro).

AJUSTE INTERNO DOCUMENTADO (handoff H-0004, secao "Estrutura esperada",
permite ajustes internos desde que o comportamento externo seja
exatamente o especificado):
- Quando executado como `python tela/diagnostico.py`, Python coloca
  `tela/` (nao a raiz do repositorio) em sys.path[0], fazendo
  `from tela.* import ...` falhar com ModuleNotFoundError.
- Os modulos Irmaos tela/teste_loader.py, tela/teste_modelo.py e
  tela/teste_renderizador.py resolvem isso adicionando a raiz do
  repositorio de scripts ao sys.path antes de importar tela.*.
- Este modulo faz o mesmo, utilizando APENAS `sys` (ja autorizado pelo
  handoff), sem importar os, pathlib ou json, e sem nenhum mecanismo
  de execucao de processo externo, preservando todas as proibicoes
  de importacao do H-0004.
- O bootstrap e restrito a `__name__ == "__main__"` para nao interferir
  no comportamento quando importado como `tela.diagnostico`.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela


def gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str:
    """Encadeia carregar_tela -> construir_modelo -> renderizar_tela.

    Parametros:
        id_tela: identificador estavel da tela (padrao "orquestrador").
            E repassado diretamente para carregar_tela(None, id_tela).

    Retorna:
        str produzida por renderizar_tela sobre o modelo construido
        a partir do dict retornado por carregar_tela.

    Efeitos colaterais:
        Nenhum. Nao altera JSON, nao executa acao, nao ativa binding,
        nao grava arquivo.

    Determinismo:
        Dado o mesmo id_tela e o mesmo JSON em disco, sempre retorna
        a mesma string.

    Lancamentos:
        Propaga naturalmente as excecoes de tela.loader (TelaErro e
        derivadas), tela.modelo (ModeloTelaErro) e tela.renderizador
        (RenderizadorErro). Nao captura, nao relanca, nao transforma.
    """
    tela_raw = carregar_tela(None, id_tela)
    modelo = construir_modelo(tela_raw)
    return renderizar_tela(modelo)


if __name__ == "__main__":
    resultado = gerar_diagnostico_tela()
    print(resultado, end="")
    sys.exit(0)
