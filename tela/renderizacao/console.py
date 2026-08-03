"""Renderização de consoles e mapa físico de itens."""

from tela.renderizacao.conteudo_externo import _linhas_conteudo_externo
from tela.renderizacao.geometria_caixa import _PLACEHOLDER_CONSOLE
from tela.renderizacao.matriz_participantes import (
    _altura_quebra_item,
    _itens_visiveis_console,
    _largura_indicador_do_elemento,
    _larguras_mapa_fisico_matricial,
    _participantes_distribuicao_matricial,
    _politica_quebra_item,
    _item_console_e_navegavel,
)

def _linhas_console(elemento, content_w=None, verboso=False):
    """Linhas de conteudo para elemento console.

    H-0036 / ADR-0026 / ADR-0027: quando o console possui conteudo externo
    multinivel associado (``elemento.conteudo_externo``), exibe as tres
    apresentacoes (``tabela``, ``hierarquia``, ``conjuntos_campos``) a partir do
    conteudo ja carregado e validado, calculando designadores concretos e a
    geometria (recuo, colunas, truncamento). O renderizador NAO abre arquivos,
    NAO escolhe fonte e NAO infere hierarquia (usa ``filhos`` como declarado).

    Sem conteudo externo, preserva o placeholder historico ``"(console)"``
    (compatibilidade retroativa com todas as telas existentes).
    """
    conteudo = getattr(elemento, "conteudo_externo", None)
    if conteudo is None:
        return [_PLACEHOLDER_CONSOLE]
    return _linhas_conteudo_externo(conteudo, content_w, verboso)

def mapa_fisico_de_itens(
    elemento,
    largura,
    altura_interna,
    verboso,
    desconto_estrutural=0,
):
    """Autoridade publica do mapa fisico de itens de console (H-0045).

    Retorna uma lista de dicts com identidade declarada, navegabilidade e
    linhas fisicas efetivas. O modulo ``tela.paginacao`` consome esta funcao;
    o renderer tambem a usa ao recortar fragmentos da pagina atual.
    """
    if getattr(elemento, "tipo", None) != "console":
        return []
    participantes = _participantes_distribuicao_matricial(elemento)
    itens = _itens_visiveis_console(elemento)
    navegavel_idx = 0
    try:
        area_w = max(0, int(largura) - int(desconto_estrutural or 0))
    except (TypeError, ValueError):
        area_w = 0
    larguras_celulas = _larguras_mapa_fisico_matricial(
        elemento, area_w, altura_interna, verboso, participantes
    )

    entradas = []
    for idx, texto in enumerate(participantes):
        item = itens[idx] if idx < len(itens) else None
        navegavel = _item_console_e_navegavel(item)
        if verboso and idx in larguras_celulas:
            ind_w = _largura_indicador_do_elemento(elemento)
            texto_w = max(1, larguras_celulas[idx] - ind_w)
            linhas = _altura_quebra_item(str(texto), texto_w)
        else:
            linhas = 1
        item_logico = navegavel_idx if navegavel else None
        if navegavel:
            navegavel_idx += 1
        item_id = item.get("id") if isinstance(item, dict) else None
        entradas.append(
            {
                "indice_fisico": idx,
                "id": item_id if item_id is not None else idx,
                "item_logico": item_logico,
                "item_logico_ou_id": item_logico if navegavel else (item_id if item_id is not None else idx),
                "navegavel": navegavel,
                "linhas_fisicas": linhas,
                "politica_quebra": _politica_quebra_item(item),
            }
        )
    return entradas
