"""Fragmentação física para paginação interna."""

import copy

from tela.renderizacao.contexto_execucao import (
    DESCONTO_ESTRUTURAL_CONSOLE,
    _ativar_quadro_minimo_lancador,
    _console_declarou_selecao_multipla,
    _console_focalizavel_de_contexto,
    _console_focado_de_contexto,
    _console_tem_paginacao,
    _item_corrente_de_contexto,
    _navegacao_atual,
    _pagina_atual_de_contexto,
    _participante_eh_selecionavel,
    _selecao_do_console_de_contexto,
)
from tela.renderizacao.conteudo_externo import _quebrar_texto
from tela.renderizacao.console import mapa_fisico_de_itens
import tela.renderizacao.matriz_participantes as _matriz
from tela.renderizacao.matriz_participantes import (
    _altura_quebra_item,
    _item_console_e_navegavel,
    _itens_visiveis_console,
    _largura_indicador_do_elemento,
    _larguras_mapa_fisico_matricial,
    _participantes_distribuicao_matricial,
)

def _fragmentos_e_total_paginacao(elemento, content_w, altura_alvo, verboso):
    from tela import paginacao

    capacidade = max(1, (altura_alvo - 2) if altura_alvo is not None else 1)
    largura_total = content_w + DESCONTO_ESTRUTURAL_CONSOLE
    plano = paginacao.plano_de_paginacao(
        elemento,
        largura_total,
        capacidade,
        verboso,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    pagina = min(_pagina_atual_de_contexto(elemento), plano["total_paginas"])
    fragmentos = []
    for pag in plano["paginas"]:
        if pag["pagina"] == pagina:
            fragmentos = list(pag["fragmentos"])
            break
    return fragmentos, pagina, plano["total_paginas"], capacidade


def _recortar_linhas_paginadas(elemento, linhas, content_w, altura_alvo, verboso):
    fragmentos, _pagina, _total, capacidade = _fragmentos_e_total_paginacao(
        elemento, content_w, altura_alvo, verboso
    )
    if not fragmentos:
        return []
    mapa = mapa_fisico_de_itens(
        elemento,
        content_w + DESCONTO_ESTRUTURAL_CONSOLE,
        capacidade,
        verboso,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    inicios = {}
    cursor = 0
    for entrada in mapa:
        inicios[entrada["id"]] = cursor
        cursor += entrada["linhas_fisicas"]
    recortadas = []
    for frag in fragmentos:
        inicio_item = inicios.get(frag["id"], 0)
        inicio = inicio_item + frag["inicio_linha"]
        fim = inicio + frag["linhas_fisicas"]
        recortadas.extend(linhas[inicio:fim])
    return recortadas[:capacidade]


def _texto_base_paginacao(elemento, content_w, altura_alvo, verboso):
    if not _console_tem_paginacao(elemento):
        return None
    _fragmentos, pagina, total, _capacidade = _fragmentos_e_total_paginacao(
        elemento, content_w, altura_alvo, verboso
    )
    return "página {0}/{1}".format(pagina, total)


def _linhas_texto_item_para_pagina(
    texto, content_w, elemento, verboso, largura_texto=None,
):
    texto = str(texto)
    if not verboso:
        return [texto]
    if largura_texto is None:
        largura_texto = content_w - _largura_indicador_do_elemento(elemento)
    largura = max(1, largura_texto)
    return _quebrar_texto(texto, largura)


def _elemento_fragmentado_para_pagina(elemento, content_w, altura_alvo, verboso):
    fragmentos, _pagina, _total, _capacidade = _fragmentos_e_total_paginacao(
        elemento, content_w, altura_alvo, verboso
    )
    itens = _itens_visiveis_console(elemento)
    mapa = mapa_fisico_de_itens(
        elemento,
        content_w + DESCONTO_ESTRUTURAL_CONSOLE,
        max(1, (altura_alvo - 2) if altura_alvo is not None else 1),
        verboso,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    larguras_celulas = _larguras_mapa_fisico_matricial(
        elemento,
        content_w,
        max(1, (altura_alvo - 2) if altura_alvo is not None else 1),
        verboso,
        _participantes_distribuicao_matricial(elemento),
    )
    por_id = {entrada["id"]: entrada for entrada in mapa}
    novos_itens = []
    for frag in fragmentos:
        entrada = por_id.get(frag["id"])
        if entrada is None:
            continue
        idx = entrada["indice_fisico"]
        item_original = itens[idx] if idx < len(itens) else {}
        texto_original = (
            item_original.get("texto", item_original.get("valor", ""))
            if isinstance(item_original, dict)
            else item_original
        )
        linhas_texto = _linhas_texto_item_para_pagina(
            texto_original,
            content_w,
            elemento,
            verboso,
            largura_texto=(
                larguras_celulas.get(idx, content_w)
                - _largura_indicador_do_elemento(elemento)
            ),
        )
        inicio = frag["inicio_linha"]
        fim = inicio + frag["linhas_fisicas"]
        for offset, linha_texto in enumerate(linhas_texto[inicio:fim]):
            if isinstance(item_original, dict):
                item = dict(item_original)
            else:
                item = {"texto": str(item_original)}
            item["texto"] = linha_texto
            item["navegavel"] = bool(
                item.get("navegavel")
                and frag["primeira_linha_do_item"]
                and offset == 0
            )
            novos_itens.append(item)
    clone = copy.copy(elemento)
    clone._campos_inertes = dict(elemento._campos_inertes)
    clone._campos_inertes["itens"] = novos_itens
    return clone


def _linhas_distribuicao_matricial(elemento, content_w, altura_alvo, verboso=False):
    """Renderiza os participantes de um elemento em grade (motor centralizado).

    H-0035 / ADR-0025: usa ``calcular_distribuicao`` para organizar os
    participantes imediatos do elemento dentro da area util (``content_w`` de
    largura por ``altura_alvo - 2`` de altura interna). Devolve a lista de
    linhas de conteudo (cada uma com no maximo ``content_w`` caracteres) para
    ser embrulhada por ``_caixa``.

    Quando o motor sinaliza fallback (nenhuma formacao cabe), sinaliza o quadro
    minimo canonico global (mecanismo ADR-0017/ADR-0023) e devolve ``[]`` — o
    ``renderizar_tela`` substitui integralmente a tela pelo quadro minimo.

    QAI40-001 (indicador matricial): para consoles focalizaveis, cada item
    navegavel reserva a coluna do indicador DENTRO de sua celula antes da
    composicao horizontal — itens lado a lado possuem colunas indicadoras
    independentes. Somente a primeira linha física do item corrente (no console
    focado) recebe ``selecionado_simbolo``; demais células recebem
    ``selecionado_off``. Nenhuma linha vazia recebe o indicador (D11/D12).

    QAI40-003 (modo verboso): quando ``verboso`` e o elemento e um console com
    itens (sem conteudo externo multinivel), o texto longo de cada item e
    quebrado em multiplas linhas físicas pela largura util da celula
    (contrato_console.md §6 / ADR-0028), produzindo continuação física real.

    Determinismo: a saida depende apenas do elemento, ``content_w``,
    ``altura_alvo`` e ``verboso``. Sem estado residual, sem efeito parcial
    antes de erro.
    """
    config = elemento.distribuicao_matricial
    participantes = _participantes_distribuicao_matricial(elemento)
    n = len(participantes)

    # Altura util interna da caixa: total menos topo e base (2 linhas de borda).
    # Quando altura_alvo e None, usa a altura natural minima (uma linha por
    # linha da grade sera resolvida pelo motor com area suficiente).
    if altura_alvo is not None:
        area_h = max(0, altura_alvo - 2)
    else:
        area_h = None
    area_w = content_w

    if n == 0:
        return []

    # QAI40-001: consoles focalizaveis reservam a coluna do indicador DENTRO de
    # cada celula. O requisito mínimo de largura de cada item cresce pelo
    # indicador, de modo que a coluna geométrica acomode símbolo + texto.
    eh_console_com_indicador = (
        elemento.tipo == "console"
        and _console_focalizavel_de_contexto(elemento)
    )
    ind_w = _largura_indicador_do_elemento(elemento) if eh_console_com_indicador else 0

    # QAI40-003: em modo verboso, console com itens (sem conteudo externo) pode
    # quebrar o texto em multiplas linhas; o requisito mínimo de altura passa a
    # ser calculado pela quebra efetiva (nao fixo em 1).
    quebrar = (
        verboso and elemento.tipo == "console"
        and getattr(elemento, "conteudo_externo", None) is None
        and area_w is not None
    )

    # Largura util interna de cada item (texto): largura da celula menos o
    # indicador. Como a largura da celula ainda nao foi calculada, estimamos o
    # minimo de texto e somamos o indicador para o motor alocar espaco.
    #
    # QAI40-003: em modo verboso, o texto longo NAO exige a largura integral —
    # ele e quebrado em multiplas linhas. O minimo de largura de cada item e
    # entao uma fracao do texto (limite razoavel para permitir a quebra),
    # evitando fallback geometrico quando o item e longo. Em modo nao verboso,
    # o minimo e o comprimento integral (truncado pela fronteira da celula).
    if quebrar:
        # Altura mínima = quebra REAL por palavra. Usa a largura util real da
        # CELULA (area - margens min - indicador): subestimar a largura infla
        # a altura e provoca fallback indevido (e, no caminho antigo,
        # sobreposicao).
        esp = config.get("espacamento", {})
        marg_e = int((esp.get("margem_esquerda") or {}).get("minimo", 0) or 0)
        marg_d = int((esp.get("margem_direita") or {}).get("minimo", 0) or 0)
        largura_texto_est = max(1, area_w - ind_w - marg_e - marg_d)
        # VM-H0045-R07-001: quando a formacao limita a no maximo uma celula
        # por linha (colunas.fixo/maximo <= 1), o item usa toda a largura
        # util atribuida. Com mais de uma celula possivel por linha, mantem o
        # teto historico (metade da area util de texto, no minimo 10) para
        # que itens longos quebrem em vez de forcar fallback.
        colunas_cfg = (config.get("formacao") or {}).get("colunas") or {}
        colunas_max = colunas_cfg.get("fixo")
        if colunas_max is None:
            colunas_max = colunas_cfg.get("maximo")
        celula_unica_por_linha = isinstance(colunas_max, int) and colunas_max <= 1
    else:
        largura_texto_est = None
        celula_unica_por_linha = False

    min_ws = []
    for p in participantes:
        if quebrar:
            if celula_unica_por_linha:
                teto = max(10, largura_texto_est)
            else:
                teto = max(10, (area_w - ind_w) // 2)
            texto_min = max(10, min(len(p), teto))
        else:
            texto_min = len(p)
        min_ws.append(texto_min + ind_w)

    if quebrar:
        min_hs = [
            _altura_quebra_item(p, largura_texto_est) for p in participantes
        ]
    else:
        min_hs = [1 for _ in participantes]

    # Altura util para o motor. Quando altura_alvo e None (composicao orientada
    # pelo conteudo), estimamos uma area suficiente para a formacao caber, de
    # modo que a caixa cresca naturalmente. Usamos um limite generoso baseado
    # no numero de participantes; o motor selecionara a formacao preferida.
    if area_h is None:
        # Estimativa de area vertical suficiente para a formação caber. Com
        # dimensionamento ``uniforme`` de linhas, todas as linhas recebem a
        # altura do maior min_h — a estimativa deve refletir isso (n_linhas
        # potenciais * max(min_hs)) para não forçar fallback indevido.
        dim_lin_pol = config["dimensionamento"]["linhas"]["politica"]
        if dim_lin_pol == "uniforme" and min_hs:
            # Estimativa pessimista de número de linhas (cada item em sua linha).
            n_linhas_est = max(1, n)
            area_h_calc = n_linhas_est * max(min_hs) + 8
        else:
            area_h_calc = max(1, sum(min_hs)) + 8
    else:
        area_h_calc = area_h

    resultado = _matriz.calcular_distribuicao(
        area_w=area_w,
        area_h=area_h_calc,
        n_participantes=n,
        config=config,
        min_ws=min_ws,
        min_hs=min_hs,
    )

    # Patch pos-validacao VM-07: apos a primeira distribuicao, as larguras
    # reais das celulas sao conhecidas. Recalcula min_hs pela quebra efetiva
    # nessas larguras e redistribui se alguma celula ficou baixa demais —
    # evitando sobreposicao entre itens multilinha e o item seguinte.
    if quebrar and not resultado["fallback"] and resultado["celulas"]:
        min_hs_reais = list(min_hs)
        precisa_redistribuir = False
        for celula in resultado["celulas"]:
            pidx = celula["participante"]
            largura_texto_real = max(1, celula["largura"] - ind_w)
            h_real = _altura_quebra_item(participantes[pidx], largura_texto_real)
            if h_real > min_hs_reais[pidx]:
                min_hs_reais[pidx] = h_real
            if h_real > celula["altura"]:
                precisa_redistribuir = True
        if precisa_redistribuir or min_hs_reais != min_hs:
            if area_h is None:
                dim_lin_pol = config["dimensionamento"]["linhas"]["politica"]
                if dim_lin_pol == "uniforme" and min_hs_reais:
                    area_h_calc = max(1, n) * max(min_hs_reais) + 8
                else:
                    area_h_calc = max(1, sum(min_hs_reais)) + 8
            resultado = _matriz.calcular_distribuicao(
                area_w=area_w,
                area_h=area_h_calc,
                n_participantes=n,
                config=config,
                min_ws=min_ws,
                min_hs=min_hs_reais,
            )
            # Se ainda houver celula menor que a quebra real, nao aceitar
            # renderizacao com sobreposicao: fallback para quadro minimo.
            if not resultado["fallback"]:
                for celula in resultado["celulas"]:
                    pidx = celula["participante"]
                    largura_texto_real = max(1, celula["largura"] - ind_w)
                    h_real = _altura_quebra_item(
                        participantes[pidx], largura_texto_real
                    )
                    if h_real > celula["altura"]:
                        resultado = {
                            "fallback": True,
                            "grade": None,
                            "formacao": None,
                            "celulas": [],
                        }
                        break

    if resultado["fallback"]:
        _ativar_quadro_minimo_lancador()
        return []

    grade = resultado["grade"]
    n_linhas, n_colunas = resultado["formacao"]

    # Altura efetivamente ocupada pela grade (para modo orientado pelo conteudo).
    if area_h is None:
        ocupada_h = (
            grade["margem_sup"] + grade["margem_inf"]
            + sum(grade["alturas_linhas"])
            + sum(grade["vaos_v"])
        )
        canvas_h = max(1, ocupada_h)
    else:
        canvas_h = area_h

    # Canvas de caracteres (linhas x colunas) preenchido com espacos.
    canvas = [[" "] * area_w for _ in range(canvas_h)]

    alinh = config["alinhamento_interno"]
    alinh_h = alinh["horizontal"]
    alinh_v = alinh["vertical"]

    # QAI40-001: resolve o item corrente (id) do console focado para marcar
    # exatamente a celula/primeira linha física do item corrente.
    item_corrente_id = (
        _item_corrente_de_contexto(elemento)
        if eh_console_com_indicador and _console_focado_de_contexto(elemento)
        else None
    )
    # H-0041: o mapeamento participante -> id alinha-se com a ordem declarada de
    # TODOS os itens (``_participantes_distribuicao_matricial`` inclui itens
    # não navegáveis visivelmente). ``nav_ids`` lista o id de cada participante;
    # itens não navegáveis (sem ``navegavel``) ficam como ``None`` e nunca
    # recebem cursor (D8) — preserva o comportamento de consoles sem itens
    # mistos (todos navegáveis) e corrige o alinhamento quando há não navegáveis.
    nav_ids = None
    if eh_console_com_indicador:
        itens = elemento._campos_inertes.get("itens", []) or []
        nav_ids = [
            (it.get("id") if isinstance(it, dict) and it.get("navegavel") else None)
            for it in itens
        ]

    # H-0041 / ADR-0034: símbolos e larguras das colunas ``ec`` (cursor) e ``tg``
    # (inclusão). ``tg`` só aparece quando o console declara seleção multipla.
    inc_on = _navegacao_atual.get("inc_on")
    inc_off = _navegacao_atual.get("inc_off")
    tem_tg = (
        eh_console_com_indicador
        and _console_declarou_selecao_multipla(elemento)
        and inc_on is not None
        and inc_off is not None
    )
    selecao_corrente = (
        _selecao_do_console_de_contexto(elemento) if tem_tg else set()
    )
    from tela.navegacao import (
        LARGURA_INDICADOR_COLUNA as _EC_W,
        LARGURA_INDICADOR_INCLUSAO as _TG_W,
    )
    tg_w = _TG_W if tem_tg else 0

    for celula in resultado["celulas"]:
        participante_idx = celula["participante"]
        # H-0041: resolve o marcador de inclusão (``tg``) por participante.
        # ``None`` -> item não selecionável ou console sem seleção multipla:
        # a coluna ``tg`` fica em branco (sem símbolo de inclusão, D-SEL-09).
        tg_marcador = None
        if tem_tg and participante_idx < len(nav_ids):
            pid = nav_ids[participante_idx]
            if pid is not None and _participante_eh_selecionavel(elemento, participante_idx):
                tg_marcador = inc_on if pid in selecao_corrente else inc_off
        # QAI40-001: o indicador e inserido DENTRO da celula, antes do texto.
        # Para consoles focalizaveis, deslocamos o texto por ind_w e colocamos
        # o marcador na primeira coluna da celula (apenas na primeira linha
        # física do item corrente; demais recebem selecionado_off).
        if ind_w > 0:
            _matriz._renderizar_participante_com_indicador(
                canvas=canvas,
                texto_integral=participantes[participante_idx],
                cel_x=celula["x"],
                cel_y=celula["y"],
                cel_w=celula["largura"],
                cel_h=celula["altura"],
                canvas_h=canvas_h,
                area_w=area_w,
                alinh_h=alinh_h,
                alinh_v=alinh_v,
                ind_w=ind_w,
                eh_corrente=(
                    nav_ids is not None
                    and participante_idx < len(nav_ids)
                    and nav_ids[participante_idx] == item_corrente_id
                    and item_corrente_id is not None
                ),
                quebrar=quebrar,
                ec_w=_EC_W,
                tg_w=tg_w,
                tg_marcador=tg_marcador,
            )
        else:
            # DEC-APP-0025-01: a camada matricial entrega o conteudo integral ao
            # participante; a fronteira interna decide a visibilidade fisica.
            _matriz._renderizar_participante_na_celula(
                canvas=canvas,
                texto_integral=participantes[participante_idx],
                cel_x=celula["x"],
                cel_y=celula["y"],
                cel_w=celula["largura"],
                cel_h=celula["altura"],
                canvas_h=canvas_h,
                area_w=area_w,
                alinh_h=alinh_h,
                alinh_v=alinh_v,
            )


    return ["".join(linha) for linha in canvas]
