"""Renderização de consoles e mapa físico de itens."""

from tela.renderizacao.conteudo_externo import _linhas_conteudo_externo
from tela.renderizacao.conteudo_externo import (
    _linhas_apresentacao_hierarquia_com_mapa,
    _linhas_dois_niveis_formatado,
    _linhas_dois_niveis_formatado_com_mapa,
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


def _selecao_multinivel(elemento):
    from tela.navegacao import tipo_navegacao_efetivo

    return (
        getattr(elemento, "tipo", None) == "console"
        and tipo_navegacao_efetivo(elemento) in (
            "selecao_multinivel", "dois_niveis_por_foco"
        )
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


def _parametros_renderizacao_multinivel(elemento):
    estado = _estado_runtime_arvore(elemento)
    estado["selecoes"] = _navegacao_atual.get("selecoes") or {}
    focalizavel, focado = _contexto_foco_arvore(elemento)
    from tela import navegacao
    from tela import selecao

    if navegacao.tipo_navegacao_efetivo(elemento) == "dois_niveis_por_foco":
        estrutural = navegacao._sequencia_estrutural_dois_niveis(elemento)
        estado = selecao.inicializar_escolhas_dois_niveis(estado, elemento)
    else:
        estrutural = navegacao._sequencia_estrutural_selecao_multinivel(elemento)
    cursor = (estado.get("cursores") or {}).get(elemento.id)
    corrente_id = None
    if focado and isinstance(cursor, int) and 0 <= cursor < len(estrutural):
        corrente_id = estrutural[cursor].id
    indicador = _navegacao_atual.get("simbolo") if focalizavel else None
    indicador_off = _navegacao_atual.get("off") if focalizavel else None
    selecionados = (estado.get("selecoes") or {}).get(elemento.id, ())
    incluido_on = _navegacao_atual.get(
        "inc_on", _navegacao_atual.get("incluido_on", "●")
    )
    incluido_off = _navegacao_atual.get(
        "inc_off", _navegacao_atual.get("incluido_off", "○")
    )
    return (
        estado, focalizavel, corrente_id, indicador, indicador_off,
        selecionados, incluido_on, incluido_off,
    )


def _largura_renderizada_arvore(elemento, content_w, focalizavel):
    if focalizavel and content_w is not None:
        return max(0, content_w - 2)
    return content_w


def _largura_renderizada_multinivel(content_w, focalizavel):
    if focalizavel and content_w is not None:
        return max(0, content_w - 4)
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
    if _selecao_multinivel(elemento) and getattr(conteudo, "apresentacao", None) == "hierarquia":
        (
            estado, focalizavel, corrente_id, indicador, indicador_off,
            selecionados, incluido_on, incluido_off,
        ) = _parametros_renderizacao_multinivel(elemento)
        largura_conteudo = _largura_renderizada_multinivel(content_w, focalizavel)
        # H-0072 / ADR-0047: quando o console declara
        # formato.dois_niveis_por_foco.filho, a formatacao generica dos
        # filhos (tabulacao/designador/apresentacao/tabela) substitui a
        # composicao hierarquica generica SOMENTE para este console. Consoles
        # dois_niveis_por_foco sem a configuracao (ex.: h0055/h0063) e
        # consoles selecao_multinivel preservam o caminho vigente intocado.
        config_filho = getattr(elemento, "formato_filho_dois_niveis", None)
        if config_filho is not None:
            return _linhas_dois_niveis_formatado(
                conteudo,
                config_filho,
                largura_conteudo,
                verboso,
                no_corrente_id=corrente_id,
                indicador=indicador,
                indicador_off=indicador_off,
                selecoes=selecionados,
                incluir_selecao=True,
                incluido_on=incluido_on,
                incluido_off=incluido_off,
            )
        return _linhas_conteudo_externo(
            conteudo,
            largura_conteudo,
            verboso,
            no_corrente_id=corrente_id,
            indicador=indicador,
            indicador_off=indicador_off,
            selecoes=selecionados,
            incluir_selecao=True,
            incluido_on=incluido_on,
            incluido_off=incluido_off,
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
    if _selecao_multinivel(elemento):
        (
            estado, focalizavel, corrente_id, indicador, indicador_off,
            selecionados, incluido_on, incluido_off,
        ) = _parametros_renderizacao_multinivel(elemento)
        largura_conteudo = largura_util_itens_console(largura, elemento)
        largura_conteudo = _largura_renderizada_multinivel(
            largura_conteudo, focalizavel
        )
        config_filho = getattr(elemento, "formato_filho_dois_niveis", None)
        if config_filho is not None:
            entradas = _linhas_dois_niveis_formatado_com_mapa(
                elemento.conteudo_externo,
                config_filho,
                largura_conteudo,
                verboso,
                no_corrente_id=corrente_id,
                indicador=indicador,
                indicador_off=indicador_off,
                selecoes=selecionados,
                incluir_selecao=True,
                incluido_on=incluido_on,
                incluido_off=incluido_off,
            )
        else:
            entradas = _linhas_apresentacao_hierarquia_com_mapa(
                elemento.conteudo_externo,
                largura_conteudo,
                verboso,
                no_corrente_id=corrente_id,
                indicador=indicador,
                indicador_off=indicador_off,
                selecoes=selecionados,
                incluir_selecao=True,
                incluido_on=incluido_on,
                incluido_off=incluido_off,
            )
        from tela.navegacao import _nos_em_pre_ordem, no_multinivel_navegavel

        nos = _nos_em_pre_ordem(elemento.conteudo_externo.nos)
        mapa = []
        navegavel_idx = 0
        for indice, entrada in enumerate(entradas):
            no = nos[indice] if indice < len(nos) else None
            navegavel = no is not None and no_multinivel_navegavel(no)
            item_logico = navegavel_idx if navegavel else None
            if navegavel:
                navegavel_idx += 1
            mapa.append({
                "indice_fisico": indice,
                "id": entrada["id"],
                "item_logico": item_logico,
                "item_logico_ou_id": item_logico if navegavel else entrada["id"],
                "navegavel": navegavel,
                "linhas_fisicas": len(entrada["linhas"]),
                # H-0054 reusa a politica universal de paginacao: linhas
                # hierarquicas cabem juntas na pagina e so um item maior que
                # a pagina pode ser fragmentado.
                "politica_quebra": "permitir_quebra_somente_se_maior_que_pagina",
            })
        return mapa
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
\n