"""Sessao TTY interativa do H-0041 (selecao multipla em console de nivel unico).

Ponto de entrada executavel da demonstracao do H-0041 / ADR-0034 Handoff 1.
Reutiliza integralmente o mecanismo real do projeto (sessao TUI,
redimensionamento via SIGWINCH, estilo global, estado de runtime de navegacao
e selecao) entregue por ``demo/demo.py``; NAO cria renderer alternativo nem
fluxo paralelo simplificado.

Interface:

    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao --tela <caminho-json>

A demonstracao carrega a tela JSON a partir do CAMINHO passado em ``--tela``.
Quando o caminho aponta para um arquivo dentro de ``config/telas/demo`` (o caso
nominal dos JSONs do H-0041), o id e a raiz sao derivados do proprio caminho,
preservando a validacao de id do loader (``TelaIdNaoCoincideComArquivo``).

H-0041 / ADR-0034 D-SEL-07: Enter com selecao permanece INATIVO neste handoff
-- nao ha operacao consumidora, protocolo de script, dry-run nem tela de
resultado. Espaco alterna inclusao (D-SEL-05); Enter=Todos com selecao vazia
(D-SEL-04); Esc limpa a selecao antes de sair/voltar (D-SEL-08).

A apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)

import argparse
import os

from tela.loader import (
    carregar_tela,
    carregar_conteudo_externo,
    TelaArquivoNaoEncontrado,
)
from tela.modelo import construir_modelo
import demo.demo as _demo
import demo.demo_navegacao as _demo_nav


def _resolver_caminho_tela(caminho):
    """Resolve (raiz_telas, id_tela) a partir de ``caminho`` informado em --tela.

    Reaproveita o resolvedor da demo de navegacao (mesma logica de derivacao de
    raiz/id a partir do caminho), preservando a checagem de id do loader.
    """
    return _demo_nav._resolver_caminho_tela(caminho)


def carregar_modelo_por_caminho(caminho):
    """Carrega e constroi o ModeloTela a partir do caminho informado em --tela.

    Reaproveita o carregador da demo de navegacao (mecanismo real do projeto).
    O H-0041 nao adiciona associacoes de conteudo externo aos seus JSONs.
    """
    return _demo_nav.carregar_modelo_por_caminho(caminho)


def _parse_argv(argv):
    """Parse de argv com ``--tela`` (obrigatorio)."""
    parser = argparse.ArgumentParser(
        prog="demo.demo_selecao",
        description="Demonstracao H-0041: selecao multipla em console de nivel unico.",
        add_help=True,
    )
    parser.add_argument(
        "--tela",
        required=True,
        help="Caminho do JSON de tela a ser carregado.",
    )
    return parser.parse_args(argv[1:])


def main(argv=None):
    """Entrada principal da demonstracao H-0041.

    Carrega a tela informada por ``--tela`` (caminho do JSON), estabelece o
    foco no primeiro console focalizavel ao iniciar (materializando o indicador
    de cursor desde o primeiro quadro) e delega ao ``main`` real de
    ``demo/demo.py`` -- reutilizando a sessao TUI, o redimensionamento via
    SIGWINCH, o estilo global e o estado de runtime de navegacao e selecao.
    Retorna o codigo de saida da sessao (0 = saida limpa).
    """
    if argv is None:
        argv = sys.argv
    args = _parse_argv(argv)
    # Carrega o modelo uma vez para validar o caminho e a coerencia do id ANTES
    # de iniciar a sessao TUI (falha rapida, sem alternate screen em caso de
    # arquivo invalido). A sessao recarrega o modelo por id a partir do estado.
    modelo = carregar_modelo_por_caminho(args.tela)
    raiz_telas, id_tela = _resolver_caminho_tela(args.tela)

    estado = _demo.criar_estado_inicial()
    from tela.loader import carregar_estilo
    estilo = carregar_estilo()
    estado = dict(estado, estilo=estilo)
    estado = dict(estado, tela_atual=id_tela)

    # H-0041: estabelece o foco no primeiro console focalizavel ao iniciar,
    # materializando o indicador de cursor e a coluna ``tg`` desde o primeiro
    # quadro. Mesmo principio da demo de navegacao (H-0040), aplicado a selecao.
    from tela import navegacao
    lista_foco_inicial = navegacao.lista_foco(modelo)
    if lista_foco_inicial:
        estado = dict(estado, foco_console=0)
        cursores_inicial = dict(estado.get("cursores", {}))
        cursores_inicial[lista_foco_inicial[0].id] = 0
        estado = dict(estado, cursores=cursores_inicial)

    # Monta argv para o main real: o id da tela como argumento posicional.
    if os.path.normpath(raiz_telas) != os.path.normpath(_demo._RAIZ_TELAS_DEMO):
        # Tela fora da raiz demo: registra resolucao de raiz por id (mesmo
        # mecanismo da demo de navegacao).
        _demo_nav._registrar_raiz_alternativa(id_tela, raiz_telas)

    return _demo.main([argv[0], id_tela], estado_inicial=estado)


if __name__ == "__main__":
    sys.exit(main())
