"""Renderer textual estatico minimo de tela (H-0003).

Consome o ModeloTela produzido pelo pipeline H-0001 + H-0002
(`carregar_tela` -> `construir_modelo` -> `ModeloTela`) e geram uma
string textual auditavel, deterministica, sem dependencia de terminal,
sem execucao de acao, sem ativacao de binding e sem consulta a JSON.

ESCOPO (H-0003):
- Apenas renderizacao textual estatica a partir de ModeloTela.
- Nao acessa config/telas/orquestrador.json diretamente.
- Nao chama carregar_tela nem construir_modelo.
- Nao importa json, os ou pathlib.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo.
- Nao calcula largura de terminal, nao paginar, nao selecionar.
- Campos pendentes (DOC-B008 / DOC-B009) sao preservados como
  declaracao inerte, sem execucao.

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela


class RenderizadorErro(Exception):
    """Erro de renderizacao textual de tela."""


def renderizar_tela(modelo: ModeloTela) -> str:
    """Renderiza ModeloTela como string textual estatica e deterministica.

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).

    Retorna:
        str com a representacao textual estatica no formato definido
        pelo handoff H-0003 (seccoes TELA, SCHEMA, CABECALHO, CORPO e
        BARRA_DE_MENUS).

    Lanca:
        RenderizadorErro quando o argumento nao e um ModeloTela valido
        (ex.: None ou objeto de outro tipo).

    Efeitos colaterais:
        Nenhum. Nao altera o modelo, nao grava arquivo, nao consulta
        JSON em disco, nao executa acao, nao ativa binding.
    """
    if not isinstance(modelo, ModeloTela):
        raise RenderizadorErro(
            "renderizar_tela exige ModeloTela; recebido: {0}".format(
                type(modelo).__name__
            )
        )

    linhas = []

    linhas.append("TELA: {0}".format(modelo.id))
    linhas.append("SCHEMA: {0}".format(modelo.schema))
    linhas.append("")

    linhas.append("CABECALHO")
    titulo = modelo.cabecalho.get("titulo", "(ausente)")
    descricao = modelo.cabecalho.get("descricao", "(ausente)")
    linhas.append("  titulo: {0}".format(titulo))
    linhas.append("  descricao: {0}".format(descricao))
    linhas.append("")

    linhas.append("CORPO")
    arranjo = modelo.corpo.arranjo or "(não declarado)"
    linhas.append("  arranjo: {0}".format(arranjo))
    linhas.append("  elementos:")
    for elemento in modelo.corpo.elementos:
        linhas.append(
            "    - id: {0} | tipo: {1}".format(elemento.id, elemento.tipo)
        )
    linhas.append("")

    linhas.append("BARRA_DE_MENUS")
    linhas.append("  chips:")
    for chip in modelo.barra_de_menus.get("chips", []):
        chip_id = chip.get("id")
        chip_texto = chip.get("texto", "(ausente)")
        linhas.append(
            "    - id: {0} | texto: {1}".format(chip_id, chip_texto)
        )

    return "\n".join(linhas) + "\n"
