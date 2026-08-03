"""Planejamento puro de paginacao limitada para consoles (H-0045).

O modulo nao renderiza texto nem acessa arquivos. A ocupacao fisica dos itens
vem da autoridade publica do renderer, importada sob demanda para evitar ciclo
de importacao em tempo de carga.
"""

from __future__ import annotations


POLITICAS_QUEBRA = frozenset(
    (
        "evitar_quebra",
        "permitir_quebra",
        "permitir_quebra_somente_se_maior_que_pagina",
    )
)


def _capacidade(altura_interna):
    try:
        return max(1, int(altura_interna))
    except (TypeError, ValueError):
        return 1


def _mapa(elemento, largura, altura_interna, verboso, desconto_estrutural=0):
    from tela.renderizador import mapa_fisico_de_itens

    return mapa_fisico_de_itens(
        elemento,
        largura,
        altura_interna,
        verboso,
        desconto_estrutural=desconto_estrutural,
    )


def _nova_pagina(paginas):
    paginas.append({"pagina": len(paginas) + 1, "fragmentos": [], "usadas": 0})
    return paginas[-1]


def _adicionar_fragmento(pagina, entrada, inicio, quantidade):
    pagina["fragmentos"].append(
        {
            "pagina": pagina["pagina"],
            "id": entrada.get("id"),
            "item_logico_ou_id": entrada.get("item_logico_ou_id"),
            "item_logico": entrada.get("item_logico"),
            "navegavel": bool(entrada.get("navegavel")),
            "inicio_linha": inicio,
            "linhas_fisicas": quantidade,
            "linhas_item_total": entrada.get("linhas_fisicas", quantidade),
            "primeira_linha_do_item": inicio == 0,
            "continua_de_anterior": inicio > 0,
        }
    )
    pagina["usadas"] += quantidade


def _fragmentar_entrada(paginas, pagina, entrada, capacidade):
    restante = max(1, int(entrada.get("linhas_fisicas") or 1))
    inicio = 0
    while restante > 0:
        if pagina["usadas"] >= capacidade:
            pagina = _nova_pagina(paginas)
        espaco = capacidade - pagina["usadas"]
        quantidade = min(restante, espaco)
        _adicionar_fragmento(pagina, entrada, inicio, quantidade)
        restante -= quantidade
        inicio += quantidade
    return pagina


def plano_de_paginacao(
    elemento,
    largura,
    altura_interna,
    verboso,
    desconto_estrutural=0,
):
    """Retorna o plano fisico de paginas do console.

    Itens navegaveis e nao navegaveis visiveis participam da ocupacao. Um item
    navegavel so conta para foco na pagina em que sua primeira linha fisica
    aparece.
    """
    capacidade = _capacidade(altura_interna)
    entradas = _mapa(
        elemento, largura, altura_interna, verboso,
        desconto_estrutural=desconto_estrutural,
    )
    paginas = []
    pagina = _nova_pagina(paginas)

    for entrada in entradas:
        linhas = max(1, int(entrada.get("linhas_fisicas") or 1))
        entrada = dict(entrada)
        entrada["linhas_fisicas"] = linhas
        politica = entrada.get("politica_quebra") or "evitar_quebra"
        if politica not in POLITICAS_QUEBRA:
            politica = "evitar_quebra"

        if politica == "permitir_quebra":
            # Fluxo continuo: comeca na proxima linha disponivel (inclusive a
            # ultima linha util) e continua nas paginas seguintes se preciso.
            pagina = _fragmentar_entrada(paginas, pagina, entrada, capacidade)
            continue

        if politica == "evitar_quebra":
            # Sempre comeca na primeira linha util de uma pagina nova, mesmo
            # havendo espaco na pagina anterior; se maior que uma pagina,
            # continua nas seguintes.
            if pagina["usadas"] > 0:
                pagina = _nova_pagina(paginas)
            if linhas <= capacidade:
                _adicionar_fragmento(pagina, entrada, 0, linhas)
            else:
                pagina = _fragmentar_entrada(paginas, pagina, entrada, capacidade)
            continue

        # permitir_quebra_somente_se_maior_que_pagina: mantem junto quando
        # possivel — aproveita o residuo se couber inteiro; senao, pagina
        # seguinte inteira; se maior que a pagina, comeca no topo seguinte.
        if linhas <= capacidade:
            if pagina["usadas"] > 0 and pagina["usadas"] + linhas > capacidade:
                pagina = _nova_pagina(paginas)
            _adicionar_fragmento(pagina, entrada, 0, linhas)
            continue

        if pagina["usadas"] > 0:
            pagina = _nova_pagina(paginas)
        pagina = _fragmentar_entrada(paginas, pagina, entrada, capacidade)

    for pag in paginas:
        pag["linhas_usadas"] = pag.pop("usadas")
    pagina_por_item = {}
    for pag in paginas:
        for frag in pag["fragmentos"]:
            if frag["navegavel"] and frag["primeira_linha_do_item"]:
                pagina_por_item.setdefault(frag["item_logico"], pag["pagina"])
    return {
        "altura_interna": capacidade,
        "total_paginas": max(1, len(paginas)),
        "paginas": paginas,
        "pagina_por_item_logico": pagina_por_item,
    }


def total_paginas(elemento, largura, altura_interna, verboso, desconto_estrutural=0):
    return plano_de_paginacao(
        elemento, largura, altura_interna, verboso,
        desconto_estrutural=desconto_estrutural,
    )["total_paginas"]


def _pagina_clamp(plano, pagina):
    total = plano["total_paginas"]
    try:
        p = int(pagina)
    except (TypeError, ValueError):
        p = 1
    return min(max(1, p), total)


def intervalo_da_pagina(
    elemento,
    pagina,
    largura,
    altura_interna,
    verboso,
    desconto_estrutural=0,
):
    plano = plano_de_paginacao(
        elemento, largura, altura_interna, verboso,
        desconto_estrutural=desconto_estrutural,
    )
    p = _pagina_clamp(plano, pagina)
    for pag in plano["paginas"]:
        if pag["pagina"] == p:
            return list(pag["fragmentos"])
    return []


def primeiro_item_logico_da_pagina(
    elemento,
    pagina,
    largura,
    altura_interna,
    verboso,
    desconto_estrutural=0,
):
    for frag in intervalo_da_pagina(
        elemento, pagina, largura, altura_interna, verboso,
        desconto_estrutural=desconto_estrutural,
    ):
        if frag["navegavel"] and frag["primeira_linha_do_item"]:
            return frag["item_logico"]
    return None


def pagina_do_item_logico(
    elemento,
    item_logico,
    largura,
    altura_interna,
    verboso,
    desconto_estrutural=0,
):
    plano = plano_de_paginacao(
        elemento, largura, altura_interna, verboso,
        desconto_estrutural=desconto_estrutural,
    )
    return plano["pagina_por_item_logico"].get(item_logico, 1)


def pagina_atual(estado, console):
    paginas = estado.get("pagina_atual") or {}
    try:
        return max(1, int(paginas.get(console.id, 1)))
    except (TypeError, ValueError):
        return 1


def _geometria_do_estado(estado):
    largura = estado.get("largura", 80)
    altura_interna = estado.get("altura_interna")
    if altura_interna is None:
        altura_interna = max(1, int(estado.get("altura", 24)) - 8)
    verboso = bool(
        estado.get("modo_verboso_forcado") is True
        or estado.get("modo_verboso", False)
    )
    desconto = estado.get("desconto_estrutural", 0)
    return largura, altura_interna, verboso, desconto


def ir_para_pagina(estado, console, pagina):
    largura, altura_interna, verboso, desconto = _geometria_do_estado(estado)
    plano = plano_de_paginacao(
        console, largura, altura_interna, verboso,
        desconto_estrutural=desconto,
    )
    destino = _pagina_clamp(plano, pagina)
    novo = dict(estado)
    paginas = dict(estado.get("pagina_atual") or {})
    paginas[console.id] = destino
    novo["pagina_atual"] = paginas

    primeiro = primeiro_item_logico_da_pagina(
        console, destino, largura, altura_interna, verboso,
        desconto_estrutural=desconto,
    )
    cursores = dict(estado.get("cursores") or {})
    if primeiro is None:
        cursores.pop(console.id, None)
    else:
        cursores[console.id] = primeiro
    novo["cursores"] = cursores
    return novo


def reconciliar_pagina_com_cursor(estado, console, altura_interna=None, largura=None):
    """Recalcula ``pagina_atual[console.id]`` para conter o item logico do cursor.

    H-0045-P03: apos redimensionamento, a capacidade fisica por pagina muda
    (``altura_interna`` deriva de ``altura``) e a distribuicao dos itens entre
    paginas e recalculada -- o NUMERO de pagina anteriormente armazenado pode
    nao conter mais o item logico do cursor (ex.: item que era o primeiro da
    pagina 2 sob uma altura passa a pertencer a pagina 5 sob outra). Sem essa
    reconciliacao, o quadro seguinte exibe a pagina antiga (apenas clampada ao
    novo total) e o cursor nao aparece em nenhum fragmento renderizado dessa
    pagina (D10: o item logico deve ser preservado; a pagina e que se ajusta a
    ele, nunca o contrario).

    ``altura_interna``, quando fornecida pelo chamador, tem PRECEDENCIA sobre
    ``estado.get("altura_interna")`` e sobre o fallback fixo (``altura - 8``)
    de ``_geometria_do_estado``. H-0045-P05 (VM-H0045-R04-004): esse fallback
    assume que a barra de menus sempre ocupa 1 linha de chips, o que nao vale
    em geral -- o numero real de linhas depende de quais chips existem
    (D-TEC-12) e da largura corrente (H-0016). Divergindo do valor usado pelo
    render seguinte, a pagina reconciliada podia nao ser a pagina exibida
    (cursor ausente do quadro). O chamador com acesso a modelo/estilo/contexto
    de navegacao deve calcular o valor real via
    ``tela.renderizador.geometria_console`` e repassa-lo aqui; sem esse valor
    (chamadores legados/testes), o comportamento anterior (aproximacao por
    ``estado``) e preservado.

    ``largura``, quando fornecida, tem a MESMA precedencia sobre
    ``estado.get("largura")``. H-0045-P06 (QA-H0045-P05-001): em arranjo
    horizontal, cada console ocupa uma COLUNA (largura menor que a largura
    total do terminal armazenada em ``estado["largura"]``); sem a largura de
    coluna real, o plano fisico recalculado aqui pode divergir do plano
    usado pelo render seguinte para esse console.

    Preserva ``cursores`` inalterado (a identidade do item logico corrente e
    do console focado nao muda por resize -- apenas a pagina). Quando o
    console nao tem cursor no estado (``pagina sem navegaveis`` ou console
    ainda nao inicializado), devolve o estado inalterado: nao ha item logico
    para ancorar a pagina, e ``ir_para_pagina``/render ja clampam a pagina
    existente ao novo total via ``_pagina_clamp``.
    """
    cursores = estado.get("cursores") or {}
    item_logico = cursores.get(console.id)
    if item_logico is None:
        return dict(estado)
    largura_estado, altura_interna_estado, verboso, desconto = _geometria_do_estado(estado)
    if altura_interna is None:
        altura_interna = altura_interna_estado
    if largura is None:
        largura = largura_estado
    nova_pagina = pagina_do_item_logico(
        console, item_logico, largura, altura_interna, verboso,
        desconto_estrutural=desconto,
    )
    novo = dict(estado)
    paginas = dict(estado.get("pagina_atual") or {})
    paginas[console.id] = nova_pagina
    novo["pagina_atual"] = paginas
    return novo


def pagina_anterior(estado, console):
    atual = pagina_atual(estado, console)
    if atual <= 1:
        return dict(estado)
    return ir_para_pagina(estado, console, atual - 1)


def pagina_proxima(estado, console):
    largura, altura_interna, verboso, desconto = _geometria_do_estado(estado)
    total = total_paginas(
        console, largura, altura_interna, verboso,
        desconto_estrutural=desconto,
    )
    atual = pagina_atual(estado, console)
    if atual >= total:
        return dict(estado)
    return ir_para_pagina(estado, console, atual + 1)


def linhas_logicas_navegaveis_da_pagina(
    estado,
    console,
    largura=None,
    altura_interna=None,
    verboso=None,
    desconto_estrutural=None,
):
    if largura is None or altura_interna is None or verboso is None or desconto_estrutural is None:
        g_largura, g_altura, g_verboso, g_desconto = _geometria_do_estado(estado)
        largura = g_largura if largura is None else largura
        altura_interna = g_altura if altura_interna is None else altura_interna
        verboso = g_verboso if verboso is None else verboso
        desconto_estrutural = g_desconto if desconto_estrutural is None else desconto_estrutural
    pagina = pagina_atual(estado, console)
    return [
        frag["item_logico"]
        for frag in intervalo_da_pagina(
            console, pagina, largura, altura_interna, verboso,
            desconto_estrutural=desconto_estrutural,
        )
        if frag["navegavel"] and frag["primeira_linha_do_item"]
    ]
