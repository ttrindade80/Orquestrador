"""Renderização de consoles e mapa físico de itens."""

from tela.renderizacao.conteudo_externo import _linhas_conteudo_externo
from tela.renderizacao.conteudo_externo import (
    _linhas_apresentacao_hierarquia_com_mapa,
)
from tela.renderizacao.geometria_caixa import _PLACEHOLDER_CONSOLE
from tela.renderizacao.contexto_execucao import _navegacao_atual
from tela.renderizacao.matriz_participantes import (
    _altura_quebra_item,
    _itens_visiveis_console,
    _largura_indicador_do_elemento,
    _larguras_mapa_fisico_matricial,
    _participantes_distribuicao_matricial,
    _politica_quebra_item,
    _item_console_e_navegavel,
    largura_util_itens_console,
)


def _estado_runtime_arvore(elemento):
    return {
        "ramos_fechados": _navegacao_atual.get("ramos_fechados") or {},
        "cursores": _navegacao_atual.get("cursores") or {},
        "pagina_atual": _navegacao_atual.get("paginas_atuais") or {},
        "largura": _navegacao_atual.get("largura") or 80,
        "altura_interna": _navegacao_atual.get("altura_interna"),
        "modelo": None,
    }


def _arvore_colapsavel(elemento):
    from tela.navegacao import tipo_navegacao_efetivo

    return (
        getattr(elemento, "tipo", None) == "console"
        and tipo_navegacao_efetivo(elemento) == "arvore_colapsavel"
        and getattr(elemento, "conteudo_externo", None) is not None
    )


def _contexto_foco_arvore(elemento):
    lista = _navegacao_atual.get("lista_foco") or []
    focalizavel = any(getattr(c, "id", None) == elemento.id for c in lista)
    foco = _navegacao_atual.get("foco_console")
    focado = (
        focalizavel and isinstance(foco, int) and 0 <= foco < len(lista)
        and getattr(lista[foco], "id", None) == elemento.id
    )
    return focalizavel, focado


def _parametros_renderizacao_arvore(elemento):
    estado = _estado_runtime_arvore(elemento)
    focalizavel, focado = _contexto_foco_arvore(elemento)
    from tela.navegacao import _sequencia_estrutural_arvore

    estrutural = _sequencia_estrutural_arvore(elemento, estado)
    # O cursor deve chegar reconciliado pelo boundary de estado. Ausência não
    # significa item 0: o renderer não inventa um item corrente localmente.
    cursor = (estado.get("cursores") or {}).get(elemento.id)
    corrente_id = None
    if focado and isinstance(cursor, int) and 0 <= cursor < len(estrutural):
        corrente_id = estrutural[cursor].id
    indicador = _navegacao_atual.get("simbolo") if focalizavel else None
    indicador_off = _navegacao_atual.get("off") if focalizavel else None
    return estado, focalizavel, corrente_id, indicador, indicador_off


def _largura_renderizada_arvore(elemento, content_w, focalizavel):
    if focalizavel and content_w is not None:
        return max(0, content_w - 2)
    return content_w


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
    if _arvore_colapsavel(elemento) and getattr(conteudo, "apresentacao", None) == "hierarquia":
        estado, focalizavel, corrente_id, indicador, indicador_off = (
            _parametros_renderizacao_arvore(elemento)
        )
        largura_conteudo = _largura_renderizada_arvore(
            elemento, content_w, focalizavel
        )
        return _linhas_conteudo_externo(
            conteudo,
            largura_conteudo,
            verboso,
            ramos_fechados=(estado.get("ramos_fechados") or {}).get(elemento.id, ()),
            no_corrente_id=corrente_id,
            indicador=indicador,
            indicador_off=indicador_off,
        )
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
    if _arvore_colapsavel(elemento):
        estado, focalizavel, corrente_id, indicador, indicador_off = (
            _parametros_renderizacao_arvore(elemento)
        )
        largura_conteudo = largura_util_itens_console(largura, elemento)
        largura_conteudo = _largura_renderizada_arvore(
            elemento, largura_conteudo, focalizavel
        )
        entradas = _linhas_apresentacao_hierarquia_com_mapa(
            elemento.conteudo_externo,
            largura_conteudo,
            verboso,
            ramos_fechados=(estado.get("ramos_fechados") or {}).get(
                elemento.id, ()
            ),
            no_corrente_id=corrente_id,
            indicador=indicador,
            indicador_off=indicador_off,
        )
        return [
            {
                "indice_fisico": indice,
                "id": entrada["id"],
                "item_logico": indice,
                "item_logico_ou_id": indice,
                "navegavel": True,
                "linhas_fisicas": len(entrada["linhas"]),
                "politica_quebra": "evitar_quebra",
            }
            for indice, entrada in enumerate(entradas)
        ]
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
