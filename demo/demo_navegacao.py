"""Sessao TTY interativa do H-0040 (navegacao de console de nivel unico).

Ponto de entrada executavel da demonstracao do H-0040 / ADR-0031. Reutiliza
integralmente o mecanismo real do projeto (sessao TUI, redimensionamento via
SIGWINCH, modos verboso/nao verboso, estilo global) entregue por
``demo/demo.py``; NAO cria renderer alternativo nem fluxo paralelo simplificado.

Interface:

    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela <caminho-json>
    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela <caminho-json> --verboso

A demonstracao carrega a tela JSON a partir do CAMINHO passado em ``--tela``.
Quando o caminho aponta para um arquivo dentro de ``config/telas/demo`` (o caso
nominal dos JSONs do H-0040), o id e a raiz sao derivados do proprio caminho,
preservando a validacao de id do loader (``TelaIdNaoCoincideComArquivo``).
Caminhos fora dessa raiz tambem sao aceitos quando o ``id`` interno do JSON
coincide com o nome base do arquivo.

O H-0040 nao autoriza nova funcao para Enter: nenhum dispatcher de acao, nenhuma
nova resposta demonstrativa. O comportamento preexistente e preservado
(PN-0013).

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


def _raiz_demo_absoluta():
    """Caminho absoluto do diretorio ``config/telas/demo`` do repositorio."""
    base = _demo._raiz_scripts if hasattr(_demo, "_raiz_scripts") else os.getcwd()
    aqui = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(aqui)
    return os.path.join(repo, "config", "telas", "demo")


def _resolver_caminho_tela(caminho):
    """Resolve (raiz_telas, id_tela) a partir de ``caminho`` informado em --tela.

    O caminho pode ser relativo ao diretorio corrente ou absoluto. Quando o
    arquivo esta dentro de ``config/telas/demo``, retorna essa raiz e o id
    (nome base sem extensao). Caso contrario, retorna a raiz como o diretorio
    do arquivo e o id como o nome base sem extensao -- preservando a checagem
    de id do loader (``TelaIdNaoCoincideComArquivo``).
    """
    if not os.path.isabs(caminho):
        caminho = os.path.abspath(caminho)
    if not os.path.isfile(caminho):
        raise TelaArquivoNaoEncontrado(
            "Arquivo de tela nao encontrado: {0}".format(caminho)
        )
    raiz_demo = _raiz_demo_absoluta()
    diretorio = os.path.dirname(caminho)
    nome_base = os.path.basename(caminho)
    if nome_base.endswith(".json"):
        nome_base = nome_base[: -len(".json")]
    if os.path.normpath(diretorio) == os.path.normpath(raiz_demo):
        return raiz_demo, nome_base
    return diretorio, nome_base


def carregar_modelo_por_caminho(caminho):
    """Carrega e constroi o ModeloTela a partir do caminho informado em --tela.

    Reutiliza ``carregar_tela`` + ``construir_modelo`` (mecanismo real do
    projeto). Quando o catalogo da demo associa um documento externo ao id da
    tela, carrega tambem o conteudo externo (separadamente, duas leituras),
    preservando a distincao entre origens (H-0036). O H-0040 nao adiciona
    associacoes de conteudo externo aos seus JSONs nominais.
    """
    raiz_telas, id_tela = _resolver_caminho_tela(caminho)
    tela_raw = carregar_tela(None, id_tela, raiz_telas)
    id_conteudo = _demo.id_conteudo_externo_de(id_tela)
    conteudo_externo = None
    if id_conteudo is not None:
        # Somente telas sob config/telas/demo tem associacao por catalogo;
        # telas fora dessa raiz nao possuem conteudo externo associado.
        try:
            conteudo_externo = carregar_conteudo_externo(
                None, id_conteudo, _demo._RAIZ_TELAS_DEMO
            )
        except TelaArquivoNaoEncontrado:
            conteudo_externo = None
    return construir_modelo(tela_raw, conteudo_externo=conteudo_externo)


def _parse_argv(argv):
    """Parse de argv com ``--tela`` (obrigatorio) e ``--verboso`` (opcional)."""
    parser = argparse.ArgumentParser(
        prog="demo.demo_navegacao",
        description="Demonstracao H-0040: navegacao de console de nivel unico.",
        add_help=True,
    )
    parser.add_argument(
        "--tela",
        required=True,
        help="Caminho do JSON de tela a ser carregado.",
    )
    parser.add_argument(
        "--verboso",
        action="store_true",
        help="Inicia em modo verboso (quando a tela suporta).",
    )
    return parser.parse_args(argv[1:])


def main(argv=None):
    """Entrada principal da demonstracao H-0040.

    Carrega a tela informada por ``--tela`` (caminho do JSON), opcionalmente
    forca o modo verboso via ``--verboso`` (quando a politica da tela permite)
    e delega ao ``main`` real de ``demo/demo.py`` -- reutilizando a sessao TUI,
    o redimensionamento via SIGWINCH, o estilo global e o estado de runtime de
    navegacao. Retorna o codigo de saida da sessao (0 = saida limpa).
    """
    if argv is None:
        argv = sys.argv
    args = _parse_argv(argv)
    # Carrega o modelo uma vez para validar o caminho e a coerencia do id ANTES
    # de iniciar a sessao TUI (falha rapida, semalternate screen em caso de
    # arquivo invalido). A sessao recarrega o modelo por id a partir do estado.
    modelo = carregar_modelo_por_caminho(args.tela)
    raiz_telas, id_tela = _resolver_caminho_tela(args.tela)

    estado = _demo.criar_estado_inicial()
    from tela.loader import carregar_estilo
    estilo = carregar_estilo()
    estado = dict(estado, estilo=estilo)
    estado = dict(estado, tela_atual=id_tela)

    # QAI40-003: força modo verboso inicial quando --verboso. O override
    # ``modo_verboso_forcado`` alcansa o runtime e o renderer reais via
    # ``_verboso_efetivo`` (precedencia sobre a politica do modelo), sem ser
    # sobrescrito por ``politica_modo=None`` e sem criar politica nova no JSON.
    # Preserva o item logico corrente e nao torna a tecla ``V`` disponivel onde
    # nao era contratada.
    if args.verboso:
        estado = dict(estado, modo_verboso=True, modo_verboso_forcado=True)

    # H-0040: estabelece o foco no primeiro console focalizavel ao iniciar,
    # materializando o indicador de cursor desde o primeiro quadro. Quando nao
    # ha console focalizavel (cenario "nao focalizavel"), o foco permanece
    # None (D5: lista vazia nao altera o estado; chips ausentes).
    from tela import navegacao
    lista_foco_inicial = navegacao.lista_foco(modelo)
    if lista_foco_inicial:
        estado = dict(estado, foco_console=0)
        cursores_inicial = dict(estado.get("cursores", {}))
        cursores_inicial[lista_foco_inicial[0].id] = 0
        estado = dict(estado, cursores=cursores_inicial)

    # Monta argv para o main real: o id da tela como argumento posicional.
    # O main do demo.py carrega o modelo por id a partir da raiz demo. Quando a
    # tela esta fora da raiz demo, injetamos uma associacao de catalogo e um
    # carregador adaptado para que o id seja resolvido na raiz correta.
    if os.path.normpath(raiz_telas) != os.path.normpath(_demo._RAIZ_TELAS_DEMO):
        # Tela fora da raiz demo: registra resolucao de raiz por id para que o
        # mecanismo real carregue corretamente durante a sessao.
        _registrar_raiz_alternativa(id_tela, raiz_telas)

    return _demo.main([argv[0], id_tela], estado_inicial=estado)


# ---------------------------------------------------------------------------
# Resolucao de raiz alternativa para telas fora de config/telas/demo
# ---------------------------------------------------------------------------

# Mapa id_tela -> raiz_telas para telas carregadas por caminho fora da raiz
# padrao da demo. Esvaziado a cada invocacao de main (processo novo).
_RAIZES_ALTERNATIVAS = {}


def _registrar_raiz_alternativa(id_tela, raiz_telas):
    """Registra raiz alternativa para ``id_tela`` (telas fora da raiz demo)."""
    _RAIZES_ALTERNATIVAS[id_tela] = raiz_telas
    # Patch defensivo do carregador usado pela demo: substitui
    # _carregar_modelo_por_id para honrar a raiz registrada.
    original = _demo._carregar_modelo_por_id

    def _carregar_com_raiz_alt(id_t_arg):
        raiz_alt = _RAIZES_ALTERNATIVAS.get(id_t_arg)
        if raiz_alt is not None:
            tela_raw_alt = carregar_tela(None, id_t_arg, raiz_alt)
            id_conteudo_alt = _demo.id_conteudo_externo_de(id_t_arg)
            conteudo_alt = None
            if id_conteudo_alt is not None:
                try:
                    conteudo_alt = carregar_conteudo_externo(
                        None, id_conteudo_alt, _demo._RAIZ_TELAS_DEMO
                    )
                except TelaArquivoNaoEncontrado:
                    conteudo_alt = None
            return construir_modelo(tela_raw_alt, conteudo_externo=conteudo_alt)
        return original(id_t_arg)

    _demo._carregar_modelo_por_id = _carregar_com_raiz_alt


if __name__ == "__main__":
    sys.exit(main())
