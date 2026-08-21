"""Distribuição matricial e indicadores de participantes."""

from tela.distribuicao_matricial import (
    alinhar_na_celula,
    calcular_distribuicao,
)
from tela.renderizacao.contexto_execucao import (
    DESCONTO_ESTRUTURAL_CONSOLE,
    _console_declarou_selecao_multipla,
    _console_focalizavel_de_contexto,
    _console_focado_de_contexto,
    _console_original_de_contexto,
    _ids_selecionaveis_do_elemento,
    _item_corrente_de_contexto,
    _itens_navegaveis_do_elemento,
    _navegacao_atual,
    _participante_eh_selecionavel,
    _selecao_do_console_de_contexto,
)
from tela.renderizacao.composicao_textual import compor_texto
from tela.renderizacao.conteudo_externo import _participantes_de_conteudo_externo
from tela.renderizacao.texto_ansi import _cortar_sem_ansi

def _aplicar_indicador_linhas(linhas, elemento, content_w, largura_grade):
    """Prefixa a coluna do indicador em cada linha de console (D12).

    D12: cada item recebe uma coluna indicadora estável antes do conteúdo. A
    primeira linha física do item corrente (no console focado) recebe
    ``estilo.selecionado_simbolo``; todas as demais linhas (continuações do item
    corrente e todos os demais itens) recebem ``estilo.selecionado_off``. A
    coluna é estável: não desloca o conteúdo quando o cursor muda de item.

    A reserva da coluna do indicador participa do cálculo de largura útil
    disponível para o conteúdo do item (D12), coerente com
    ``tela.navegacao.grade_de_itens`` (que aplica o MESMO desconto para consoles
    focalizaveis), garantindo equivalência (AT-0021/PN-0016).

    Quando o contexto de navegacao nao esta ativo ou o console nao e
    focalizavel, retorna as linhas inalteradas (compatibilidade retroativa).
    """
    simbolo = _navegacao_atual.get("simbolo")
    off = _navegacao_atual.get("off")
    if simbolo is None or off is None:
        return linhas
    if not _console_focalizavel_de_contexto(elemento):
        return linhas
    if not _console_focado_de_contexto(elemento):
        # Consoles focalizaveis mas nao focados: reservam a coluna (estável)
        # sem marca visual. PN-0008: nenhum símbolo em console nao focado.
        off2 = off + " "
        return [
            _cortar_sem_ansi(off2 + ln, content_w)
            if content_w is not None else off2 + ln
            for ln in linhas
        ]
    # Console focado: marcar a primeira linha física do item corrente.
    item_corrente = _item_corrente_de_contexto(elemento)
    linhas_primeiras = _linhas_fisicas_por_item(elemento, largura_grade)
    resultado = []
    for idx, ln in enumerate(linhas):
        eh_primeira_do_corrente = (
            item_corrente is not None
            and idx in linhas_primeiras
            and linhas_primeiras[idx] == item_corrente
        )
        marcador = simbolo if eh_primeira_do_corrente else off
        novo = marcador + " " + ln
        if content_w is not None:
            novo = _cortar_sem_ansi(novo, content_w)
        resultado.append(novo)
    return resultado


def _largura_indicador_do_elemento(elemento):
    """Largura total das colunas indicadoras reservadas para ``elemento``.

    H-0040 / ADR-0031 D12: retorna ``LARGURA_INDICADOR_COLUNA`` (símbolo + 1
    espaco) quando o elemento e um console focalizavel no contexto vigente;
    ``0`` caso contrario.

    H-0041 / ADR-0034 D-SEL-09: quando o console declara selecao multipla,
    soma ``LARGURA_INDICADOR_INCLUSAO`` (coluna ``tg``, adjacente a ``ec``).
    Essa reserva e a MESMA aplicada por ``tela.navegacao.grade_de_itens``
    (AT-0021/PN-0016): renderer e navegacao aplicam o MESMO desconto para que
    as geometrias coincidam.
    """
    if elemento.tipo != "console":
        return 0
    if not _console_focalizavel_de_contexto(elemento):
        return 0
    from tela.navegacao import (
        LARGURA_INDICADOR_COLUNA,
        LARGURA_INDICADOR_INCLUSAO,
    )
    total = LARGURA_INDICADOR_COLUNA
    if _console_declarou_selecao_multipla(elemento):
        total += LARGURA_INDICADOR_INCLUSAO
    return total


def largura_util_itens_console(total_w, elemento, focalizavel=None):
    """Largura útil REAL disponível para os itens de um console (QAI40-002).

    Autoridade ÚNICA de geometria: o renderer determina a largura útil dos itens
    a partir da largura total e do desconto estrutural próprio, reservando em
    seguida a coluna do indicador quando o console é focalizável. ``grade_de_itens``
    (navegação) e a composição visual (renderer) consomem exatamente este valor.

    Sequência inequívoca:

    ```
    largura total do console
    → desconto estrutural do renderer (content_w = total_w - DESCONTO_ESTRUTURAL)
    → reserva da coluna indicadora, quando aplicável
    → largura útil entregue a calcular_distribuicao
    ```

    A navegação NÃO conhece o desconto estrutural do renderer: ela recebe
    ``content_w`` (largura interna já calculada pelo renderer) e aplica somente
    a reserva do indicador, evitando acoplamento invertido ao layout do renderer.

    ``focalizavel`` opcional permite resolver a condição de focalização fora do
    contexto de runtime (em testes/sem ``lista_foco``). Quando ``None``, usa o
    contexto vigente (``_console_focalizavel_de_contexto``).
    """
    if total_w is None:
        return None
    content_w = total_w - DESCONTO_ESTRUTURAL_CONSOLE
    if content_w < 0:
        content_w = 0
    eh_foc = (
        focalizavel if focalizavel is not None
        else _console_focalizavel_de_contexto(elemento)
    )
    if eh_foc and getattr(elemento, "tipo", None) == "console":
        from tela.navegacao import LARGURA_INDICADOR_COLUNA
        content_w = max(0, content_w - LARGURA_INDICADOR_COLUNA)
    return content_w


def _linhas_fisicas_por_item(elemento, largura_grade):
    """Mapeia índice de linha física -> id do item dono daquela linha.

    O mapeamento depende do caminho de renderização:

    - ``distribuicao_matricial`` declarada: a grade é row-major e cada item
      ocupa exatamente uma linha física no canvas (altura 1). A linha física
      ``k`` (0-based, na ordem dos participantes) pertence ao item lógico
      ``k``. (As células vazias geram linhas em branco, mapeadas para ``None``.)
    - sem ``distribuicao_matricial``: cada item gera uma ou mais linhas físicas
      (modo verboso pode quebrar). Aqui contamos apenas a primeira linha física
      de cada item.

    Retorna dict {indice_da_linha_fisica: id_do_item_dono_da_primeira_linha}.
    """
    dm = getattr(elemento, "distribuicao_matricial", None)
    if dm is not None:
        grade = _grade_de_itens_para_indicador(elemento, largura_grade)
        mapeamento = {}
        linha_fisica = 0
        for r in range(len(grade)):
            for c in range(len(grade[r])):
                item = grade[r][c]
                if item is not None:
                    mapeamento[linha_fisica] = item.get("id")
                linha_fisica += 1
        return mapeamento
    # Sem distribuicao_matricial: cada item navegavel contribui com ao menos
    # uma linha física; mapeamos somente a primeira. (Caminho legado raro para
    # console navegavel sem grade -- mantido para robustez.)
    navegaveis = _itens_navegaveis_do_elemento(elemento)
    mapeamento = {}
    linha_fisica = 0
    for item in navegaveis:
        mapeamento[linha_fisica] = item.get("id")
        linha_fisica += 1
    return mapeamento


def _grade_de_itens_para_indicador(elemento, largura_grade):
    """Grade row-major de itens navegaveis (mesma da navegacao) para indicador.

    Importa ``tela.navegacao.grade_de_itens`` (modulo novo autorizado) para
    garantir MESMO_RESULTADO_DA_EXIBICAO_ATUAL (AT-0021/PN-0016). A grade aqui
    e a usada para localizar a primeira linha física do item corrente.

    QAI40-002: repassa o desconto estrutural EXPLICITO do renderer para que a
    grade de navegação coincida com a geometria visualmente renderizada.
    """
    from tela.navegacao import grade_de_itens
    return grade_de_itens(
        elemento, largura_grade, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    )

def _contar_elementos_visuais(elementos):
    """Conta descendentes visuais (console/dashboard/lancador) para ADR-0024.

    Grupos SEM gestao propria (sem distribuicao, verticais, sem matriz) sao
    containers estruturais transparentes: a contagem percorre seus filhos.
    Grupos COM gestao propria (com distribuicao, horizontais ou matriciais)
    contam como 1 unidade — eles resolvem internamente sua area.

    Usado para aplicar DA-01 (cardinalidade unitaria) e detectar DA-02
    (multiplos sem distribuicao) conforme ADR-0024.
    """
    count = 0
    for elem in elementos:
        if elem.tipo == "grupo":
            dist_g = elem._campos_inertes.get("distribuicao")
            arranjo_g = elem._campos_inertes.get("arranjo", "vertical")
            estrutura_g = elem._campos_inertes.get("estrutura")
            if (dist_g is not None
                    or arranjo_g in ("horizontal", "lado_a_lado")
                    or estrutura_g == "matriz"):
                # Grupo auto-gerenciado: conta como 1 unidade visual.
                count += 1
            else:
                count += _contar_elementos_visuais(elem.elementos)
        else:
            count += 1
    return count


def _participantes_distribuicao_matricial(elemento):
    """Extrai os participantes imediatos de um elemento funcional para a grade.

    H-0035 / ADR-0025: os "participantes" organizados pela distribuicao
    matricial de nivel unico sao as unidades de conteudo do elemento:

    - dashboard: cada campo (rotulo + valor literal), na ordem declarada;
    - lancador:  cada item ``[chip] texto``, na ordem declarada;
    - console:   cada item de conteudo, na ordem declarada.

    Retorna lista de strings (uma por participante, texto de identidade). A
    ordem original e preservada: a grade so muda a celula, nunca a sequencia.
    """
    if elemento.tipo == "dashboard":
        participantes = []
        campos = elemento._campos_inertes.get("campos", []) or []
        for campo in campos:
            if not isinstance(campo, dict):
                continue
            if campo.get("fonte") == "literal":
                rotulo = campo.get("rotulo")
                valor = campo.get("valor", "")
                if rotulo:
                    participantes.append("{0}: {1}".format(rotulo, valor))
                else:
                    participantes.append("{0}".format(valor))
        return participantes
    if elemento.tipo == "lancador":
        participantes = []
        itens = elemento._campos_inertes.get("itens", []) or []
        for item in itens:
            if not isinstance(item, dict):
                continue
            chip = item.get("chip", "")
            texto = item.get("texto", "")
            participantes.append("[{0}] {1}".format(chip, texto))
        return participantes
    if elemento.tipo == "console":
        # H-0036: quando ha conteudo externo, os participantes vem do documento
        # externo (dados de runtime), preservando a distribuicao matricial
        # (ADR-0025). Sem conteudo externo, mantem o comportamento anterior
        # (itens inertes do JSON estrutural — vazio apos a separacao H-0036).
        conteudo = getattr(elemento, "conteudo_externo", None)
        if conteudo is not None:
            return _participantes_de_conteudo_externo(conteudo)
        participantes = []
        itens = elemento._campos_inertes.get("itens", []) or []
        for item in itens:
            if isinstance(item, dict):
                texto = item.get("texto", item.get("valor", ""))
                participantes.append("{0}".format(texto))
            else:
                participantes.append("{0}".format(item))
        return participantes
    return []


def _renderizar_participante_na_celula(
    canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
    canvas_h, area_w, alinh_h, alinh_v
):
    """Fronteira interna: escreve o conteudo integral do participante na celula.

    Recebe o conteudo integral e a area calculada; escreve no canvas os
    caracteres que cabem fisicamente dentro dos limites da celula, sem
    invadir celulas vizinhas. A decisao de visibilidade pertence a esta
    camada interna, nao ao distribuidor externo (H-0035 §17; DEC-APP-0025-01).
    """
    dx, dy = alinhar_na_celula(
        len(texto_integral), 1, cel_w, cel_h, alinh_h, alinh_v
    )
    px = cel_x + dx
    py = cel_y + dy
    cel_x_fim = cel_x + cel_w
    for k, ch in enumerate(texto_integral):
        cx = px + k
        if 0 <= py < canvas_h and 0 <= cx < area_w and cx < cel_x_fim:
            canvas[py][cx] = ch


def _renderizar_participante_com_indicador(
    canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
    canvas_h, area_w, alinh_h, alinh_v, ind_w, eh_corrente, quebrar,
    ec_w=0, tg_w=0, tg_marcador=None,
):
    """Escreve o conteúdo do item reservando as colunas indicadoras (QAI40-001/H-0041).

    Os indicadores são inseridos DENTRO da célula antes da composição horizontal
    do texto do item:

    - coluna ``ec`` (cursor, D12): ``ec_w`` caracteres (símbolo + separador);
      recebe ``selecionado_simbolo`` na primeira linha física do item corrente
      no console focado, ou ``selecionado_off`` caso contrário;
    - coluna ``tg`` (inclusão, D-SEL-09): ``tg_w`` caracteres adjacentes a
      ``ec`` (apenas quando o console declara seleção multipla); recebe
      ``tg_marcador`` (``incluido_on``/``incluido_off``) na primeira linha
      física do item — ``None`` deixa a coluna em branco (item não
      selecionável ou console sem seleção multipla);
    - o texto do item começa em ``cel_x + ind_w`` (largura útil de texto =
      ``cel_w - ind_w``), onde ``ind_w = ec_w + tg_w``;
    - quando ``quebrar`` (modo verboso efetivo), o texto é quebrado em múltiplas
      linhas físicas pela largura útil de texto (QAI40-003). Os indicadores
      aparecem somente na primeira linha física; as linhas de continuação
      recebem ``selecionado_off`` (ec) e espaço (tg).

    Apenas a primeira linha física do item corrente recebe o símbolo; nenhuma
    linha vazia recebe o indicador (D11/D12). As colunas indicadoras são
    estáveis (não deslocam o conteúdo entre mudanças de cursor/seleção).
    """
    simbolo = _navegacao_atual.get("simbolo")
    off = _navegacao_atual.get("off")
    if simbolo is None or off is None:
        # Sem estilo de indicador: comporta-se como participante simples.
        _renderizar_participante_na_celula(
            canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
            canvas_h, area_w, alinh_h, alinh_v,
        )
        return

    # Largura útil de texto dentro da célula (após os indicadores).
    texto_w = max(0, cel_w - ind_w)
    cel_x_fim = cel_x + cel_w

    # Fragmentos do texto: uma linha (modo não verboso) ou quebra pela largura
    # útil de texto (modo verboso). No modo não verboso, o texto que excede é
    # simplesmente truncado pela fronteira da célula (comportamento histórico).
    if quebrar and texto_w > 0:
        fragmentos = compor_texto(texto_integral, texto_w)
    else:
        fragmentos = [texto_integral]

    # Alinhamento vertical: quantas linhas o item ocupa e o deslocamento dy.
    n_frags = len(fragmentos)
    dy_align = alinhar_na_celula(texto_w, n_frags, cel_w, cel_h, alinh_h, alinh_v)[1]

    for frag_idx, frag in enumerate(fragmentos):
        py = cel_y + dy_align + frag_idx
        # Continuações e texto permanecem dentro da célula: nunca invadem a
        # célula seguinte (patch pos-validação manual H-0040 / VM-07).
        if not (0 <= py < canvas_h) or py >= cel_y + cel_h:
            continue
        # Coluna ``ec``: símbolo na primeira linha física do item corrente;
        # selecionado_off nas demais linhas (continuações) e demais itens.
        ec_marcador = simbolo if (eh_corrente and frag_idx == 0) else off
        for k in range(ec_w):
            cx = cel_x + k
            if 0 <= cx < area_w and cx < cel_x_fim:
                canvas[py][cx] = ec_marcador if k == 0 else off
        # Coluna ``tg`` (inclusão, D-SEL-09): símbolo apenas na primeira linha
        # física do item; continuação e itens não selecionáveis ficam vazios
        # (espaço). ``tg_simbolo`` None -> coluna em branco (sem símbolo de
        # inclusão); caso contrário, símbolo na 1a coluna + espaço separador.
        tg_simbolo = tg_marcador if (frag_idx == 0 and tg_marcador is not None) else None
        for k in range(tg_w):
            cx = cel_x + ec_w + k
            if 0 <= cx < area_w and cx < cel_x_fim:
                canvas[py][cx] = (tg_simbolo if k == 0 else " ") if tg_simbolo is not None else " "
        # Texto do item a partir de cel_x + ind_w.
        for k, ch in enumerate(frag):
            cx = cel_x + ind_w + k
            if cx < cel_x_fim and 0 <= cx < area_w:
                canvas[py][cx] = ch


def _altura_quebra_item(texto, largura_texto):
    """Número de linhas físicas reais de ``texto`` na largura dada (modo verboso)."""
    if largura_texto <= 0:
        return 1
    return max(1, len(compor_texto(texto, largura_texto)))


def _item_console_e_navegavel(item):
    return isinstance(item, dict) and bool(item.get("navegavel"))


def _politica_quebra_item(item):
    if isinstance(item, dict):
        return item.get("politica_quebra") or "evitar_quebra"
    return "evitar_quebra"


def _itens_visiveis_console(elemento):
    conteudo = getattr(elemento, "conteudo_externo", None)
    if conteudo is not None:
        return []
    return list(elemento._campos_inertes.get("itens", []) or [])


def _larguras_mapa_fisico_matricial(
    elemento, area_w, altura_interna, verboso, participantes,
):
    """Calcula as larguras de celula usadas pelo mapa fisico.

    O planejamento de pagina precisa usar a largura da celula, nao a largura
    total da caixa. A mesma distribuicao matricial usada pelo renderer fornece
    essas larguras; a altura de calculo e ampliada apenas quando o conjunto
    inteiro nao cabe em uma unica pagina, sem alterar a formacao preferida.
    """
    ind_w = _largura_indicador_do_elemento(elemento)
    quebrar = (
        verboso and elemento.tipo == "console"
        and getattr(elemento, "conteudo_externo", None) is None
        and area_w is not None
    )
    if quebrar:
        esp = elemento.distribuicao_matricial.get("espacamento", {})
        margem_esq = int(
            (esp.get("margem_esquerda") or {}).get("minimo", 0) or 0
        )
        margem_dir = int(
            (esp.get("margem_direita") or {}).get("minimo", 0) or 0
        )
        largura_texto_est = max(
            1, area_w - ind_w - margem_esq - margem_dir
        )
        colunas_cfg = (
            elemento.distribuicao_matricial.get("formacao") or {}
        ).get("colunas") or {}
        colunas_max = colunas_cfg.get("fixo")
        if colunas_max is None:
            colunas_max = colunas_cfg.get("maximo")
        celula_unica_por_linha = isinstance(colunas_max, int) and colunas_max <= 1

    min_ws = []
    for participante in participantes:
        if quebrar:
            if celula_unica_por_linha:
                # VM-H0045-R07-001: com no maximo uma celula por linha, o
                # item usa toda a largura util atribuida (apenas indicador e
                # margens descontados), sem o teto arbitrario de metade da
                # area que forcava a truncar o texto pela metade.
                teto = max(10, largura_texto_est)
            else:
                teto = max(10, (area_w - ind_w) // 2)
            texto_min = max(10, min(len(participante), teto))
        else:
            texto_min = len(participante)
        min_ws.append(texto_min + ind_w)

    if quebrar:
        min_hs = [
            _altura_quebra_item(participante, largura_texto_est)
            for participante in participantes
        ]
    else:
        min_hs = [1 for _ in participantes]

    try:
        altura_calculo = max(1, int(altura_interna))
    except (TypeError, ValueError):
        altura_calculo = 1
    resultado = calcular_distribuicao(
        area_w=area_w,
        area_h=altura_calculo,
        n_participantes=len(participantes),
        config=elemento.distribuicao_matricial,
        min_ws=min_ws,
        min_hs=min_hs,
    )
    if resultado["fallback"]:
        dim_lin_pol = elemento.distribuicao_matricial["dimensionamento"]["linhas"]["politica"]
        if dim_lin_pol == "uniforme" and min_hs:
            altura_calculo = max(1, len(participantes)) * max(min_hs) + 8
        else:
            altura_calculo = max(1, sum(min_hs)) + 8
        resultado = calcular_distribuicao(
            area_w=area_w,
            area_h=altura_calculo,
            n_participantes=len(participantes),
            config=elemento.distribuicao_matricial,
            min_ws=min_ws,
            min_hs=min_hs,
        )
    if resultado["fallback"]:
        return {}

    larguras = {
        celula["participante"]: celula["largura"]
        for celula in resultado["celulas"]
    }
    if not quebrar or not resultado["celulas"]:
        return larguras

    min_hs_reais = list(min_hs)
    for celula in resultado["celulas"]:
        participante_idx = celula["participante"]
        largura_texto = max(1, celula["largura"] - ind_w)
        min_hs_reais[participante_idx] = _altura_quebra_item(
            participantes[participante_idx], largura_texto
        )
    if min_hs_reais != min_hs:
        dim_lin_pol = elemento.distribuicao_matricial["dimensionamento"]["linhas"]["politica"]
        if dim_lin_pol == "uniforme" and min_hs_reais:
            altura_calculo = max(1, len(participantes)) * max(min_hs_reais) + 8
        else:
            altura_calculo = max(1, sum(min_hs_reais)) + 8
        resultado_recalculado = calcular_distribuicao(
            area_w=area_w,
            area_h=altura_calculo,
            n_participantes=len(participantes),
            config=elemento.distribuicao_matricial,
            min_ws=min_ws,
            min_hs=min_hs_reais,
        )
        if not resultado_recalculado["fallback"]:
            larguras = {
                celula["participante"]: celula["largura"]
                for celula in resultado_recalculado["celulas"]
            }
    return larguras
