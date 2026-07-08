"""Renderer visual com borda fixa da tela raiz (H-0006).

Evolui o renderer estrutural (H-0005) para uma representacao visual
com tres caixas bordeadas (largura total fixa de 42 caracteres Python
por linha): cabecalho (derivado do modelo), dashboard (placeholder
hardcoded) e menu (placeholder inerte hardcoded).

Consome o ModeloTela produzido pelo pipeline H-0001 + H-0002
(`carregar_tela` -> `construir_modelo` -> `ModeloTela`) e gera uma
string visual deterministica, sem dependencia de terminal, sem
execucao de acao, sem ativacao de binding e sem consulta a JSON.

ESCOPO (H-0006):
- Apenas renderizacao visual com borda fixa a partir de ModeloTela.
- Caixa de cabecalho derivada de modelo.cabecalho (titulo/descricao).
- Caixa de dashboard totalmente hardcoded (placeholder de teste).
- Caixa de menu totalmente hardcoded (texto inerte [Esc] Sair e [B] Borda).
- Nao acessa config/telas/orquestrador.json diretamente.
- Nao chama carregar_tela nem construir_modelo.
- Nao importa json, os ou pathlib.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo.
- Nao calcula largura de terminal, nao paginar, nao selecionar.
- Nao acessa campos inertes internos de nenhum ElementoCorpo.
- Nao acessa modelo.corpo, modelo.barra_de_menus, modelo.id nem modelo.schema.
- [Esc] Sair e [B] Borda sao apenas texto inerte -- nenhum binding.

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela


class RenderizadorErro(Exception):
    """Erro de renderizacao visual de tela."""


TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38


def _linha_topo(label):
    """Monta a borda superior com label.

    Formato: ╭ {LABEL} {─×(38-len(LABEL))}╮
    """
    label_trunc = label[:_LABEL_MAX]
    dashes = _LABEL_MAX - len(label_trunc)
    return "╭ {0} {1}╮".format(label_trunc, "─" * dashes)


def _linha_base():
    """Monta a borda inferior: ╰{─×40}╯."""
    return "╰{0}╯".format("─" * INNER_WIDTH)


def _linha_conteudo(texto):
    """Monta uma linha de conteudo: │ {text:<39}│."""
    return "│ {0:<39}│".format(texto[:CONTENT_WIDTH])


def _caixa(label, linhas_conteudo):
    """Monta uma caixa bordeada com label no topo e linhas de conteudo."""
    partes = [_linha_topo(label)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto))
    partes.append(_linha_base())
    return "\n".join(partes)


def renderizar_tela(modelo: ModeloTela) -> str:
    """Renderiza ModeloTela como string visual com borda fixa (H-0006).

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).

    Retorna:
        str com a representacao visual no formato definido pelo
        handoff H-0006 (tres caixas bordeadas de 42 chars por linha:
        cabecalho derivado do modelo, dashboard placeholder hardcoded,
        menu placeholder hardcoded inerte).

    Lancamentos:
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

    titulo = modelo.cabecalho.get("titulo", "(ausente)")
    descricao = modelo.cabecalho.get("descricao", "(ausente)")
    label_cabecalho = titulo.upper()

    caixa_cabecalho = _caixa(label_cabecalho, [descricao])
    caixa_dashboard = _caixa(
        "DASHBOARD",
        ["Dashboard de teste", "Sem dados carregados"],
    )
    caixa_menu = _caixa("Menu", ["[Esc] Sair    [B] Borda"])

    return (
        caixa_cabecalho + "\n\n"
        + caixa_dashboard + "\n\n"
        + caixa_menu + "\n"
    )
