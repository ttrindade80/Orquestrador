"""Montagem recursiva dos containers do corpo."""

from tela.renderizacao.contexto_execucao import (
    DESCONTO_ESTRUTURAL_CONSOLE,
    _console_tem_paginacao,
)
from tela.renderizacao.dashboard import _linhas_dashboard
from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.geometria_caixa import (
    _LABEL_BARRA,
    _caixa,
    _contar_linhas,
    _distribuir_alturas,
    _distribuir_larguras,
    _linha_base,
    _pesos_distribuicao,
)
from tela.renderizacao.lancador import _linhas_lancador
from tela.renderizacao.matriz_participantes import largura_util_itens_console
from tela.renderizacao.matriz_participantes import (
    _aplicar_indicador_linhas,
    _contar_elementos_visuais,
)
from tela.renderizacao.paginacao_interna import (
    _elemento_fragmentado_para_pagina,
    _linhas_distribuicao_matricial,
    _recortar_linhas_paginadas,
    _texto_base_paginacao,
)
from tela.renderizacao.console import _linhas_console

def _caixa_de_elemento(
    elemento, borda, inner_w, content_w, label_max,
    altura_alvo=None, verboso=False, registro_geometria=None,
):
    """Despacha um elemento funcional para sua caixa bordeada.

    Retorna a string da caixa do elemento (console/dashboard/lancador) ou
    ``None`` quando o tipo nao e funcional. Usado tanto para elementos
    diretos de ``corpo.elementos[]`` (lista plana) quanto para os elementos
    funcionais internos de um grupo estrutural (H-0012) -- o despacho e
    identico nos dois casos.

    ``altura_alvo`` (H-0025 / ADR-0018 D4): quando fornecida, a moldura do
    elemento ocupa exatamente essa altura, preenchendo internamente com
    linhas em branco bordeadas quando o conteudo natural e menor que a cota.
    Quando ``None``, preserva o comportamento anterior (topo + conteudo +
    base, sem preenchimento interno).

    ``registro_geometria`` (H-0045-P07 / QA-H0045-P06-001): dict opcional
    ``console.id -> {"largura": int, "altura_interna": int}`` populado como
    efeito colateral quando ``elemento`` e um console e ``altura_alvo`` e um
    inteiro concreto (cota fisica resolvida pelo container pai). Esta funcao
    e o UNICO ponto de despacho de console em toda a arvore de containers
    (raiz, grupo, grupo aninhado, estrutura matriz -- todos convergem aqui
    via ``_renderizar_container*``), portanto registrar aqui, com os MESMOS
    ``inner_w``/``altura_alvo`` que o render efetivamente usa para montar a
    caixa, garante que a geometria relatada nunca diverge da caixa
    renderizada, sem duplicar nenhuma regra de particionamento/distribuicao.
    Quando ``altura_alvo`` e ``None`` (altura natural, orientada pelo
    conteudo), nenhuma entrada e registrada -- essa geometria nao e uma cota
    fisica estavel utilizavel por paginacao (ausencia explicita).
    """
    if (
        registro_geometria is not None
        and altura_alvo is not None
        and getattr(elemento, "tipo", None) == "console"
    ):
        registro_geometria[elemento.id] = {
            "largura": inner_w + 2,
            "altura_interna": max(1, altura_alvo - 2),
        }
    # H-0035 / ADR-0025: quando o elemento funcional declara distribuicao_
    # matricial, ela organiza os participantes imediatos em grade. Para console
    # substitui as politicas geometricas antigas (DEC-APP-0025-03); para lancador
    # tem precedencia sobre ADR-0001/0002/0003 (DEC-APP-0025-02); para dashboard
    # organiza os campos. Ausencia preserva o comportamento anterior.
    dm = getattr(elemento, "distribuicao_matricial", None)
    if dm is not None and elemento.tipo in ("console", "dashboard", "lancador"):
        rotulo_padrao = {
            "console": "CONSOLE",
            "dashboard": "DASHBOARD",
            "lancador": "LANCADOR",
        }[elemento.tipo]
        titulo_el = elemento._campos_inertes.get("titulo", rotulo_padrao)
        # QAI40-001/QAI40-002: no caminho matricial, o indicador é reservado
        # DENTRO de cada célula (uma coluna indicadora por item, lado a lado),
        # de modo que content_w_itens == content_w (a reserva por célula é
        # tratada internamente por _linhas_distribuicao_matricial). A largura
        # útil final dos itens coincide com a consumida pela navegação, que
        # aplica o mesmo desconto estrutural explícito (AT-0021/PN-0016).
        content_w_itens = content_w
        elemento_render = elemento
        texto_base = None
        if _console_tem_paginacao(elemento):
            elemento_render = _elemento_fragmentado_para_pagina(
                elemento, content_w_itens, altura_alvo, verboso
            )
            texto_base = _texto_base_paginacao(
                elemento, content_w_itens, altura_alvo, verboso
            )
        linhas = _linhas_distribuicao_matricial(
            elemento_render, content_w_itens, altura_alvo, verboso=verboso,
        )
        # QAI40-001: o indicador matricial já é aplicado dentro das células;
        # _aplicar_indicador_linhas permanece apenas para o caminho sem grade.
        return _caixa(
            titulo_el.upper(), linhas,
            borda, inner_w, content_w, label_max, altura_alvo,
            texto_base=texto_base,
        )

    if elemento.tipo == "console":
        titulo_el = elemento._campos_inertes.get("titulo", "CONSOLE")
        # QAI40-002: largura útil dos itens pela autoridade única do renderer.
        total_w = content_w + DESCONTO_ESTRUTURAL_CONSOLE if content_w is not None else None
        content_w_itens = largura_util_itens_console(total_w, elemento)
        linhas_console = _linhas_console(elemento, content_w_itens, verboso)
        # H-0040: indicador de cursor de navegacao no console sem grade.
        linhas_console = _aplicar_indicador_linhas(
            linhas_console, elemento, content_w, content_w_itens
        )
        texto_base = None
        if _console_tem_paginacao(elemento):
            linhas_console = _recortar_linhas_paginadas(
                elemento, linhas_console, content_w, altura_alvo, verboso
            )
            texto_base = _texto_base_paginacao(
                elemento, content_w, altura_alvo, verboso
            )
        return _caixa(
            titulo_el.upper(), linhas_console,
            borda, inner_w, content_w, label_max, altura_alvo,
            texto_base=texto_base,
        )
    if elemento.tipo == "dashboard":
        titulo_el = elemento._campos_inertes.get("titulo", "DASHBOARD")
        return _caixa(
            titulo_el.upper(), _linhas_dashboard(elemento),
            borda, inner_w, content_w, label_max, altura_alvo,
        )
    if elemento.tipo == "lancador":
        titulo_el = elemento._campos_inertes.get("titulo", "LANCADOR")
        return _caixa(
            titulo_el.upper(), _linhas_lancador(elemento, content_w),
            borda, inner_w, content_w, label_max, altura_alvo,
        )
    return None


def _renderizar_container_vertical(
    distribuicao, elementos, borda, total_w,
    inner_w, content_w, label_max, altura_disponivel,
    verboso=False, registro_geometria=None,
):
    """Renderiza elementos em disposicao vertical dentro de um container.

    Quando distribuicao e altura_disponivel sao ambos fornecidos, reparte a
    altura entre os filhos pelos maiores restos (ADR-0018 D6/D7).

    Quando distribuicao e None mas altura_disponivel e fornecida, aplica
    ADR-0024 DA-01/DA-02/DA-04:
    - DA-01: unico descendente visual ocupa integralmente a area disponivel.
    - DA-02: multiplos descendentes visuais sem distribuicao sao rejeitados
      quando ha area nao coberta pelos filhos naturais.
    - DA-04: area disponivel sem nenhum elemento visual e rejeitada.

    Quando altura_disponivel e None, cada filho usa sua altura natural
    (orientado pelo conteudo — ADR-0018 D2).
    Grupo e despachado recursivamente via _renderizar_container (H-0027).

    ``registro_geometria`` (H-0045-P07): repassado inalterado a cada chamada
    recursiva e a cada ``_caixa_de_elemento`` -- ver docstring de
    ``_caixa_de_elemento``.
    """
    partes = []

    if distribuicao is not None and altura_disponivel is not None:
        pesos = _pesos_distribuicao(distribuicao, len(elementos))
        cotas = _distribuir_alturas(altura_disponivel, pesos)
        for indice, elemento in enumerate(elementos):
            cota = cotas[indice]
            if elemento.tipo == "grupo":
                estrutura_g = elemento._campos_inertes.get("estrutura")
                arranjo_g = elemento._campos_inertes.get("arranjo")
                dist_g = elemento._campos_inertes.get("distribuicao")
                matriz_g = elemento._campos_inertes.get("matriz")
                bloco = _renderizar_container(
                    arranjo_g, dist_g, elemento.elementos, borda, total_w, cota,
                    estrutura=estrutura_g, matriz_config=matriz_g,
                    verboso=verboso, registro_geometria=registro_geometria,
                )
                fill_linha = " " * total_w
                if bloco:
                    linhas_bloco = bloco.split("\n")
                    while len(linhas_bloco) < cota:
                        linhas_bloco.append(fill_linha)
                    partes.append("\n".join(linhas_bloco))
                elif cota > 0:
                    partes.append("\n".join(fill_linha for _ in range(cota)))
            else:
                caixa = _caixa_de_elemento(
                    elemento, borda, inner_w, content_w, label_max,
                    altura_alvo=cota, verboso=verboso,
                    registro_geometria=registro_geometria,
                )
                if caixa is not None:
                    partes.append(caixa)
    elif distribuicao is None and altura_disponivel is not None:
        # ADR-0024: sem distribuicao mas com area delimitada.
        # Aplica DA-01 (cardinalidade unitaria), DA-02 e DA-04.
        n_visual = _contar_elementos_visuais(elementos)
        if n_visual == 1:
            # DA-01 (ADR-0024): unico descendente visual ocupa toda a area.
            # DA-03 (ADR-0024): grupos repassam integralmente a area.
            for elemento in elementos:
                if elemento.tipo == "grupo":
                    estrutura_g = elemento._campos_inertes.get("estrutura")
                    arranjo_g = elemento._campos_inertes.get("arranjo")
                    dist_g = elemento._campos_inertes.get("distribuicao")
                    matriz_g = elemento._campos_inertes.get("matriz")
                    bloco = _renderizar_container(
                        arranjo_g, dist_g, elemento.elementos, borda,
                        total_w, altura_disponivel,
                        estrutura=estrutura_g, matriz_config=matriz_g,
                        verboso=verboso, registro_geometria=registro_geometria,
                    )
                    if bloco:
                        partes.append(bloco)
                else:
                    caixa = _caixa_de_elemento(
                        elemento, borda, inner_w, content_w, label_max,
                        altura_alvo=altura_disponivel, verboso=verboso,
                        registro_geometria=registro_geometria,
                    )
                    if caixa is not None:
                        partes.append(caixa)
        else:
            # n_visual == 0 ou > 1: renderizar com altura natural e verificar.
            for elemento in elementos:
                if elemento.tipo == "grupo":
                    estrutura_g = elemento._campos_inertes.get("estrutura")
                    arranjo_g = elemento._campos_inertes.get("arranjo")
                    dist_g = elemento._campos_inertes.get("distribuicao")
                    matriz_g = elemento._campos_inertes.get("matriz")
                    bloco = _renderizar_container(
                        arranjo_g, dist_g, elemento.elementos, borda,
                        total_w, None,
                        estrutura=estrutura_g, matriz_config=matriz_g,
                        verboso=verboso, registro_geometria=registro_geometria,
                    )
                    if bloco:
                        partes.append(bloco)
                else:
                    caixa = _caixa_de_elemento(
                        elemento, borda, inner_w, content_w, label_max,
                        verboso=verboso, registro_geometria=registro_geometria,
                    )
                    if caixa is not None:
                        partes.append(caixa)
            # DA-02/DA-04 (ADR-0024): verificar se ha area nao coberta.
            l_conteudo = sum(_contar_linhas(p) for p in partes)
            l_fill = altura_disponivel - l_conteudo
            if l_fill > 0:
                if n_visual == 0:
                    raise RenderizadorErro(
                        "DA-04 (ADR-0024): composicao invalida — {0} linhas "
                        "disponiveis sem nenhum elemento visual; toda area do "
                        "corpo deve pertencer a console, dashboard ou "
                        "lancador".format(l_fill)
                    )
                else:
                    raise RenderizadorErro(
                        "DA-02 (ADR-0024): composicao invalida — {0} elementos "
                        "visuais disputam o eixo vertical sem distribuicao "
                        "declarada; distribuicao e obrigatoria quando ha area "
                        "a distribuir entre multiplos "
                        "elementos".format(n_visual)
                    )
    else:
        # altura_disponivel e None: altura natural orientada pelo conteudo
        # (ADR-0018 D2). Sem restricao de area, sem DA-02/DA-04.
        for elemento in elementos:
            if elemento.tipo == "grupo":
                estrutura_g = elemento._campos_inertes.get("estrutura")
                arranjo_g = elemento._campos_inertes.get("arranjo")
                dist_g = elemento._campos_inertes.get("distribuicao")
                matriz_g = elemento._campos_inertes.get("matriz")
                bloco = _renderizar_container(
                    arranjo_g, dist_g, elemento.elementos, borda, total_w, None,
                    estrutura=estrutura_g, matriz_config=matriz_g,
                    verboso=verboso, registro_geometria=registro_geometria,
                )
                if bloco:
                    partes.append(bloco)
            else:
                caixa = _caixa_de_elemento(
                    elemento, borda, inner_w, content_w, label_max,
                    verboso=verboso, registro_geometria=registro_geometria,
                )
                if caixa is not None:
                    partes.append(caixa)

    return "\n".join(partes)


def _renderizar_container_horizontal(
    distribuicao, elementos, borda, total_w, altura_disponivel,
    larguras=None, verboso=False, registro_geometria=None,
):
    """Renderiza elementos em disposicao horizontal dentro de um container.

    Quando larguras e None, aplica DA-01/DA-02 (ADR-0024):
    - N == 1 sem distribuicao: participante unico recebe largura integral (DA-01).
    - N > 1 sem distribuicao: composicao invalida rejeitada com RenderizadorErro
      DA-02; ausencia de distribuicao nunca equivale a particionamento uniforme.
    Quando larguras sao fornecidas externamente (ex.: matriz), usa-as diretamente.
    Grupo e despachado recursivamente via _renderizar_container (H-0027).

    ``registro_geometria`` (H-0045-P07): repassado inalterado a cada chamada
    recursiva e a cada ``_caixa_de_elemento`` -- ver docstring de
    ``_caixa_de_elemento``.
    """
    N = len(elementos)

    # Cardinalidade de larguras explicitas (coerente com _montar_corpo_horizontal).
    # Validada antes de qualquer indexacao, iteracao ou renderizacao, garantindo
    # ausencia de saida parcial e de IndexError/truncamento.
    if larguras is not None:
        L = len(larguras)
        if L != N:
            raise RenderizadorErro(
                "cardinalidade horizontal incoerente: {0} participante(s) "
                "para {1} largura(s) explicita(s)".format(N, L)
            )

    if N == 0:
        return ""

    if larguras is not None:
        pass  # larguras pre-computadas (passadas externamente)
    elif distribuicao is not None:
        pesos = _pesos_distribuicao(distribuicao, N)
        larguras = _distribuir_larguras(total_w, pesos)
    else:
        if N == 1:
            # DA-01 (ADR-0024): participante unico recebe largura integral.
            larguras = [total_w]
        else:
            # DA-02 (ADR-0024): multiplos elementos sem distribuicao — invalido.
            raise RenderizadorErro(
                "DA-02 (ADR-0024): composicao invalida — {0} elementos "
                "disputam o eixo horizontal sem distribuicao declarada; "
                "distribuicao e obrigatoria quando multiplos elementos "
                "competem no mesmo eixo".format(N)
            )

    for i, w in enumerate(larguras):
        if w < 10:
            raise RenderizadorErro(
                "arranjo horizontal: largura {0} insuficiente para {1} "
                "elementos no particionamento horizontal (minimo 10 chars "
                "por area; area {2} calculada com {3})".format(
                    total_w, N, i, w
                )
            )

    todas_as_linhas_por_area = []
    for i, elemento in enumerate(elementos):
        w = larguras[i]
        if elemento.tipo == "grupo":
            estrutura_g = elemento._campos_inertes.get("estrutura")
            arranjo_g = elemento._campos_inertes.get("arranjo")
            dist_g = elemento._campos_inertes.get("distribuicao")
            matriz_g = elemento._campos_inertes.get("matriz")
            bloco = _renderizar_container(
                arranjo_g, dist_g, elemento.elementos, borda, w, altura_disponivel,
                estrutura=estrutura_g, matriz_config=matriz_g, verboso=verboso,
                registro_geometria=registro_geometria,
            )
            linhas_area = bloco.split("\n") if bloco else []
        else:
            # QA-H0045-P05-001: ``altura_alvo`` DEVE ser repassado aqui (nao
            # so no preenchimento posterior abaixo). Sem isso, um console
            # paginado dentro de uma coluna horizontal renderiza sua caixa
            # com altura NATURAL (``altura_alvo=None``), fazendo
            # ``_fragmentos_e_total_paginacao`` cair no fallback interno
            # ``capacidade=1`` -- divergente da capacidade real da coluna
            # (mesma ``altura_disponivel`` usada pela geometria auxiliar
            # ``geometria_console``). Chamar com ``altura_alvo=altura_
            # disponivel`` e idempotente para elementos nao paginados: quando
            # a caixa ja atinge exatamente essa altura, o preenchimento
            # posterior abaixo nao adiciona nem remove linhas.
            caixa_str = _caixa_de_elemento(
                elemento, borda, w - 2, w - 3, w - 4,
                altura_alvo=altura_disponivel, verboso=verboso,
                registro_geometria=registro_geometria,
            )
            if caixa_str is None or caixa_str == "":
                linhas_area = []
            else:
                linhas_area = caixa_str.split("\n")
        todas_as_linhas_por_area.append(linhas_area)

    altura_max = max(
        (len(linhas) for linhas in todas_as_linhas_por_area), default=0
    )
    if altura_max == 0:
        return ""

    altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max
    if altura_alvo < altura_max:
        altura_alvo = altura_max

    for i, linhas in enumerate(todas_as_linhas_por_area):
        w = larguras[i]
        if altura_disponivel is not None:
            if linhas:
                base_linha = linhas.pop()
            else:
                base_linha = _linha_base(borda, w - 2)
            linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
            while len(linhas) < altura_alvo - 1:
                linhas.append(linha_fill)
            linhas.append(base_linha)
        else:
            while len(linhas) < altura_alvo:
                linhas.append(" " * w)

    linhas_resultado = []
    for r in range(altura_alvo):
        linha = ""
        for linhas in todas_as_linhas_por_area:
            linha += linhas[r]
        linhas_resultado.append(linha)

    return "\n".join(linhas_resultado)


def _renderizar_container_matriz(
    matriz_config, elementos, borda, total_w, altura_disponivel, verboso=False,
    registro_geometria=None,
):
    """Renderiza um grupo ``estrutura: matriz`` com grade bidimensional comum.

    As cotas dos dois eixos sao calculadas uma unica vez para o container
    matricial e compartilhadas por todas as celulas. As linhas sao renderizadas
    como containers horizontais com larguras pre-computadas, preservando as
    primitivas de borda e preenchimento ja existentes.

    ``registro_geometria`` (H-0045-P07): repassado inalterado a cada linha
    (``_renderizar_container_horizontal``) -- ver docstring de
    ``_caixa_de_elemento``.
    """
    if not isinstance(matriz_config, dict):
        raise RenderizadorErro("estrutura matriz sem objeto matriz validado")
    if altura_disponivel is None:
        raise RenderizadorErro(
            "estrutura matriz requer altura_disponivel para distribuir linhas"
        )

    n_linhas = matriz_config["linhas"]["quantidade"]
    n_colunas = matriz_config["colunas"]["quantidade"]
    dist_linhas = matriz_config["linhas"]["distribuicao"]
    dist_colunas = matriz_config["colunas"]["distribuicao"]

    pesos_linhas = _pesos_distribuicao(dist_linhas, n_linhas)
    pesos_colunas = _pesos_distribuicao(dist_colunas, n_colunas)
    alturas = _distribuir_alturas(altura_disponivel, pesos_linhas)
    larguras = _distribuir_larguras(total_w, pesos_colunas)

    elem_por_id = {elemento.id: elemento for elemento in elementos}
    celula_para_id = {
        (celula["linha"], celula["coluna"]): celula["elemento"]
        for celula in matriz_config["celulas"]
    }

    blocos = []
    for linha in range(1, n_linhas + 1):
        elementos_linha = [
            elem_por_id[celula_para_id[(linha, coluna)]]
            for coluna in range(1, n_colunas + 1)
        ]
        bloco = _renderizar_container_horizontal(
            distribuicao=None,
            elementos=elementos_linha,
            borda=borda,
            total_w=total_w,
            altura_disponivel=alturas[linha - 1],
            larguras=larguras,
            verboso=verboso,
            registro_geometria=registro_geometria,
        )
        if bloco:
            blocos.append(bloco)

    return "\n".join(blocos)


def _renderizar_container(
    arranjo, distribuicao, elementos, borda, total_w, altura_disponivel,
    estrutura=None, matriz_config=None, verboso=False, registro_geometria=None,
):
    """Renderiza os filhos de um container recursivamente (H-0027 / ADR-0019).

    Grupo e no estrutural sem caixa visual propria: sua area e preenchida
    pelos filhos via composicao recursiva. Arranjos sao independentes entre
    pai e filho (ADR-0019 D5 / ADR-0015 dec. 6).

    arranjo: None / "vertical" / "sobreposto" -> pilha vertical
             "horizontal" / "lado_a_lado"      -> lado a lado
    distribuicao: None (orientado pelo conteudo) ou dict validado.
    elementos: lista de ElementoCorpo.
    total_w: largura total disponivel para este container.
    altura_disponivel: altura alocada pelo pai (None = conteudo natural).

    ``registro_geometria`` (H-0045-P07 / QA-H0045-P06-001): dict opcional
    ``console.id -> {"largura": int, "altura_interna": int}``, repassado
    recursivamente por TODOS os ramos (vertical/horizontal/matriz, incluindo
    grupos aninhados) ate ``_caixa_de_elemento``, onde e efetivamente
    populado para cada console -- a UNICA funcao de despacho de console de
    toda a arvore. Usado por ``tela.renderizador._geometria_por_console``
    para obter a geometria real recursiva sem duplicar nenhuma regra de
    particionamento/distribuicao: e a MESMA chamada usada pelo render real
    (``renderizar_tela`` nao passa ``registro_geometria``, portanto o
    comportamento/desempenho do render normal e inalterado).
    """
    if not elementos:
        return ""

    if estrutura == "matriz":
        return _renderizar_container_matriz(
            matriz_config, elementos, borda, total_w, altura_disponivel,
            verboso=verboso, registro_geometria=registro_geometria,
        )

    arr = arranjo
    if arr == "sobreposto":
        arr = "vertical"
    if arr == "lado_a_lado":
        arr = "horizontal"

    if arr == "horizontal":
        return _renderizar_container_horizontal(
            distribuicao, elementos, borda, total_w, altura_disponivel,
            verboso=verboso, registro_geometria=registro_geometria,
        )
    else:
        inner_w = total_w - 2
        content_w = total_w - 3
        label_max = total_w - 4
        return _renderizar_container_vertical(
            distribuicao, elementos, borda,
            total_w, inner_w, content_w, label_max, altura_disponivel,
            verboso=verboso, registro_geometria=registro_geometria,
        )


def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None,
                             larguras=None, verboso=False):
    """Particionamento horizontal contiguo do corpo raiz (H-0019 / H-0020 / H-0026 / ADR-0024).

    Quando ``larguras`` e ``None`` (ausencia de distribuicao declarada):
    - Zero participantes: retorna string vazia — sem conteudo, sem particao.
    - Um participante (DA-01 / ADR-0024): ``larguras = [total_w]``; o unico
      elemento recebe integralmente a largura disponivel.
    - Multiplos participantes (DA-02 / ADR-0024): composicao invalida —
      ausencia de distribuicao com mais de um elemento competindo no eixo
      horizontal e rejeitada com ``RenderizadorErro``; nao existe particionamento
      uniforme implicito; composicao invalida e rejeitada por DA-04.

    Quando ``larguras`` e fornecida (lista de inteiros com soma == ``total_w``,
    ja calculada externamente via ``_distribuir_larguras`` a partir dos pesos
    declarados em ``corpo.distribuicao``): usa essas larguras explicitas,
    implementando os modos ``percentual``, ``fracao`` e ``igual`` no arranjo
    horizontal (H-0026 / ADR-0015 D5-D8, ADR-0018 D6/D7). Larguras multiplas
    somente sao validas quando resultam de distribuicao explicita ja validada.

    Grupos nao sao expandidos aqui: contam como slot com area visualmente
    vazia. O caminho principal de renderizar_tela usa _renderizar_container
    desde H-0027, que expande grupos recursivamente via
    _renderizar_container_horizontal.

    ``altura_disponivel`` (H-0020): quando fornecida, cada coluna e preenchida
    ate essa altura (fill bordeado). Quando ``None``, normaliza ate altura_max
    (comportamento H-0019). Se o conteudo exceder ``altura_disponivel``, mantem
    altura_max sem truncar.
    """
    N = len(elementos)

    if larguras is not None:
        L = len(larguras)
        if L != N:
            raise RenderizadorErro(
                "cardinalidade horizontal incoerente: {0} participante(s) "
                "para {1} largura(s) explicita(s)".format(N, L)
            )

    if N == 0:
        return ""

    if larguras is None:
        if N == 1:
            # DA-01 (ADR-0024): participante unico recebe largura integral.
            larguras = [total_w]
        else:
            # DA-02 (ADR-0024): multiplos elementos sem distribuicao — invalido.
            raise RenderizadorErro(
                "DA-02 (ADR-0024): composicao invalida — {0} elementos "
                "disputam o eixo horizontal sem distribuicao declarada; "
                "distribuicao e obrigatoria quando multiplos elementos "
                "competem no mesmo eixo".format(N)
            )

    # Verificar cabimento mínimo antes de renderizar
    for i, w in enumerate(larguras):
        if w < 10:
            raise RenderizadorErro(
                "arranjo horizontal: largura {0} insuficiente para {1} "
                "elementos no particionamento horizontal (minimo 10 chars "
                "por area; area {2} calculada com {3})".format(
                    total_w, N, i, w
                )
            )

    # Renderizar cada filho dentro da largura de sua área alocada
    todas_as_linhas_por_area = []
    for i, elemento in enumerate(elementos):
        w = larguras[i]
        caixa_str = _caixa_de_elemento(
            elemento, borda, w - 2, w - 3, w - 4, verboso=verboso,
        )
        if caixa_str is None or caixa_str == "":
            # Grupo ou tipo sem visual: área inicialmente vazia, será preenchida
            linhas_area = []
        else:
            linhas_area = caixa_str.split("\n")
        todas_as_linhas_por_area.append(linhas_area)

    # Normalizar altura com preenchimento inferior (ADR-0015 D10 / H-0020)
    altura_max = max(
        (len(linhas) for linhas in todas_as_linhas_por_area), default=0
    )
    if altura_max == 0:
        return ""

    # H-0020: altura_disponivel fornecida -> normalizar cada coluna até a
    # altura total do corpo (ADR-0015 D5: área alocada preservada).
    # None -> comportamento H-0019 (altura_alvo = altura_max).
    # Conteúdo acima de altura_disponivel -> manter altura_max sem truncar.
    altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max
    if altura_alvo < altura_max:
        altura_alvo = altura_max

    for i, linhas in enumerate(todas_as_linhas_por_area):
        w = larguras[i]
        if altura_disponivel is not None:
            # H-0021: fill bordeado — extrair base, preencher com bordas, reposicionar base.
            # A base existente (gerada por _caixa()) e temporariamente removida para que o
            # fill bordeado seja inserido antes dela, mantendo-a na posicao altura_alvo-1.
            if linhas:
                base_linha = linhas.pop()
            else:
                base_linha = _linha_base(borda, w - 2)
            linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
            while len(linhas) < altura_alvo - 1:
                linhas.append(linha_fill)
            linhas.append(base_linha)
        else:
            # Comportamento H-0019/H-0020 preservado: fill de espacos sem bordas.
            while len(linhas) < altura_alvo:
                linhas.append(" " * w)

    # Concatenar áreas linha a linha, sem separador externo (ADR-0015 D9).
    # Bordas adjacentes surgem naturalmente: ││ em linhas internas,
    # ╮╭ no topo, ╯╰ na base. Invariante: len(linha) == total_w.
    linhas_resultado = []
    for r in range(altura_alvo):
        linha = ""
        for linhas in todas_as_linhas_por_area:
            linha += linhas[r]
        linhas_resultado.append(linha)

    return "\n".join(linhas_resultado)
