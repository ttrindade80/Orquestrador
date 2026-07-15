"""Diagnostico executavel da tela demo (H-0032).

Ponto de entrada unico e auditavel que encadeia o pipeline completo
sobre a tela demo:

    config/telas/demo/demo.json
        -> carregar_tela(None, id_tela, raiz_telas)  [tela/loader.py      - H-0001]
        -> construir_modelo(tela_raw)                 [tela/modelo.py      - H-0002]
        -> renderizar_tela(modelo)                    [tela/renderizador.py - H-0003]
        -> str

ESCOPO (H-0032):
- Apenas o encadeamento acima. Nenhuma logica de negocio e adicionada.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo, nao
  consulta JSON diretamente (isso fica a cargo do loader).
- Excecoes dos modulos subjacentes propagam naturalmente para o
  chamador (Tela*, ModeloTelaErro, RenderizadorErro).

AJUSTE INTERNO DOCUMENTADO:
- Quando executado como `python demo/diagnostico.py`, Python coloca
  `demo/` (nao a raiz do repositorio) em sys.path[0], fazendo
  `from tela.* import ...` falhar com ModuleNotFoundError.
- O bootstrap insere a raiz do repositorio em sys.path antes de
  importar tela.*, utilizando APENAS `sys` e `os`.
- O bootstrap e restrito a `__name__ == "__main__"` para nao interferir
  no comportamento quando importado como `demo.diagnostico`.

Apenas biblioteca padrao do Python.
"""

import os
import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")


def gerar_diagnostico_tela(id_tela: str = "demo") -> str:
    """Encadeia carregar_tela -> construir_modelo -> renderizar_tela para a raiz demo.

    Parametros:
        id_tela: identificador estavel da tela demo (padrao "demo").
            E repassado para carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO).

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
    tela_raw = carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
    modelo = construir_modelo(tela_raw)
    return renderizar_tela(modelo)


if __name__ == "__main__":
    resultado = gerar_diagnostico_tela()
    print(resultado, end="")
    sys.exit(0)
