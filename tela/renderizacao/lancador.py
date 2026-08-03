"""Renderização de lançadores."""

from tela.renderizacao.contexto_execucao import _ativar_quadro_minimo_lancador
from tela.renderizacao.erros import RenderizadorErro

def _split_excesso_lancador(excesso, alinhamento):
    """Divide excesso residual em (exc_esq, exc_dir) conforme alinhamento.

    "direita": tudo à esquerda do bloco.
    "centro": divisão inteira; maiores-restos para a esquerda.
    "esquerda" ou None: tudo à direita do bloco.
    """
    if alinhamento == "direita":
        return excesso, 0
    if alinhamento == "centro":
        esq = (excesso + 1) // 2
        return esq, excesso - esq
    return 0, excesso

def _itens_lancador_normalizados(elemento, max_caracteres):
    """Devolve a lista de itens válidos (dict com chip e texto) do lancador.

    Levanta ``RenderizadorErro`` quando algum ``texto`` excede ``max_caracteres``
    — nunca trunca, nunca abrevia (R-3). O limite vem de
    ``config/elementos/lancador.json`` via pipeline loader → modelo.
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    normais = []
    for item in itens:
        if not isinstance(item, dict):
            continue
        chip = item.get("chip", "")
        texto = item.get("texto", "")
        if len(texto) > max_caracteres:
            raise RenderizadorErro(
                "texto de item de lancador acima do limite de {0} "
                "caracteres: {1!r} (id={2!r})".format(
                    max_caracteres, texto, item.get("id")
                )
            )
        normais.append((chip, texto))
    return normais


def _chip_sub_w(chip):
    """Largura da sub-coluna do chip: ``"[" + chip + "]"``."""
    return len(chip) + 2


def _distribuir_excesso_total(excesso, n_vaos, vao_max):
    """Distribui ``excesso`` por ``n_vaos`` vãos uniformemente, respeitando
    ``vao_max``. Retorna a expansão (inteira) aplicada a cada vão, pela ordem
    declarada (maior-resto absorvido pelos primeiros vãos), limitada ao teto.
    Devolve o total efetivamente absorvido.
    """
    base = min(excesso // n_vaos if n_vaos > 0 else 0, vao_max)
    expansao = [base] * n_vaos
    absorvido = base * n_vaos
    restante = excesso - absorvido
    i = 0
    while restante > 0 and i < n_vaos:
        cabem = vao_max - expansao[i]
        if cabem > 0:
            dar = min(cabem, restante)
            expansao[i] += dar
            restante -= dar
        i += 1
    return expansao


def _linhas_lancador(elemento, content_w=None):
    """Linhas de conteudo para elemento lancador (H-0034 / ADR-0023).

    Implementa a distribuição responsiva do ``lancador`` e o gatilho do quadro
    mínimo canônico global. Quando ``content_w`` é fornecido (caminho normal de
    ``renderizar_tela`` / ``_caixa_de_elemento``), aplica a sequência normativa
    de decisão (contrato_lancador.md seção 6.7, ADR-0023 seção 3.3):

    ```
    content_w >= coluna_minima_content_w ?
      -> fila se couber; senão matriz com mais colunas; senão coluna mínima
    content_w < coluna_minima_content_w ?
      -> sinalizar quadro mínimo global (ADR-0023) e retornar []
    ```

    Sempre inclui as margens verticais canônicas (1 linha em branco acima do
    primeiro item e 1 abaixo do último), conforme contrato_lancador.md 6.6.

    Comportamento preservado quando ``content_w is None``: renderiza cada item
    como ``"[{chip}] {texto}"``, um por linha (legado; sem margens verticais
    nem cálculo responsivo). Mantido para compatibilidade com eventuais
    chamadas externas; o caminho de ``renderizar_tela`` sempre fornece
    ``content_w``.
    """
    # Cardinalidade zero: verificado sobre itens brutos, antes de qualquer
    # validação de texto ou consulta a parametros_tipo.
    _itens_brutos = [
        i for i in (elemento._campos_inertes.get("itens", []) or [])
        if isinstance(i, dict)
    ]
    if not _itens_brutos:
        return []

    # Parâmetros normativos do tipo lancador propagados pelo pipeline
    # loader → modelo (config/elementos/lancador.json / H-0034 / ADR-0023).
    # O renderer não lê arquivos nem importa json/os/pathlib.
    params = elemento.parametros_tipo
    if params is None:
        raise RenderizadorErro(
            "lancador: parametros_tipo ausente; elemento deve ser construido "
            "pelo pipeline carregar_tela + construir_modelo com "
            "config/elementos/lancador.json disponivel"
        )

    # max_caracteres vem de verificacao.texto.max_caracteres propagado via loader.
    # Normalização aplicada antes de qualquer ramificação de caminho.
    max_caracteres = params["verificacao"]["texto"]["max_caracteres"]
    itens = _itens_lancador_normalizados(elemento, max_caracteres)

    # Caminho legado (sem content_w): um item por linha, sem layout responsivo.
    # Preserva formato anterior para entradas válidas; valida texto via
    # sequência comum acima (parametros_tipo + _itens_lancador_normalizados).
    if content_w is None:
        return [
            "[{0}] {1}".format(chip, texto)
            for chip, texto in itens
        ]

    # Alinhamento horizontal declarado pela instância (R-10 /
    # contrato_lancador.md 6.4). None é tratado como "esquerda".
    layout_inst = elemento._campos_inertes.get("layout") or {}
    alinhamento = layout_inst.get("alinhamento")
    if alinhamento is not None and alinhamento not in ("esquerda", "centro", "direita"):
        raise RenderizadorErro(
            "lancador: alinhamento horizontal desconhecido: {0!r}; "
            "valores aceitos: esquerda, centro, direita (R-10)".format(alinhamento)
        )

    _vaos = params["vaos"]
    vao_chip_texto = _vaos["chip_texto"]["minimo"]
    vao_itens = _vaos["entre_itens_colunas_margem"]["minimo"]
    vao_itens_max = _vaos["entre_itens_colunas_margem"]["maximo"]
    _vert = params["vertical"]
    margem_v_sup = _vert["margem_borda_superior"]
    margem_v_inf = _vert["margem_borda_inferior"]
    margem = vao_itens  # margem horizontal borda-elemento (entre_itens_colunas_margem.minimo)

    # --- H-0034 / ADR-0023: distribuição responsiva ----------------------

    # Largura mínima de um item isolado (vão chip-texto no mínimo).
    def _item_w_min(chip, texto):
        return _chip_sub_w(chip) + vao_chip_texto + len(texto)

    n = len(itens)

    max_chip_sub = max(_chip_sub_w(chip) for chip, _ in itens)
    max_texto_sub = max(len(texto) for _, texto in itens)

    coluna_minima_content_w = (
        margem + max_chip_sub + vao_chip_texto + max_texto_sub + margem
    )

    # Etapa 4 (ADR-0023): abaixo da coluna mínima → quadro mínimo canônico
    # global. Sinaliza e retorna linhas vazias; ``renderizar_tela`` substitui
    # a tela normal inteira pelo quadro mínimo (mecanismo ADR-0017).
    if content_w < coluna_minima_content_w:
        _ativar_quadro_minimo_lancador()
        return []

    # --- Renderização dos modos válidos -----------------------------------
    def _render_linha_itens(itens_linha, vao_entre):
        """Renderiza uma linha de itens (modo fila)."""
        textos = []
        for chip, texto in itens_linha:
            textos.append("[{0}]{1}{2}".format(
                chip, " " * vao_chip_texto, texto
            ))
        return (" " * margem) + (" " * vao_entre).join(textos)

    # Etapa 1 — tentativa de fila.
    fila_min = (
        margem
        + sum(_item_w_min(chip, texto) for chip, texto in itens)
        + (n - 1) * vao_itens
        + margem
    )
    if content_w >= fila_min:
        excesso = content_w - fila_min
        # Passo 1: expandir vãos internos (prioridade, distribuição_de_sobra).
        # Cada vão expande independentemente até o teto; maiores restos nos
        # primeiros vãos (config/elementos/lancador.json distribuicao_de_sobra).
        vaos = [vao_itens] * (n - 1)
        if excesso > 0 and n > 1:
            expansao = _distribuir_excesso_total(
                excesso, n - 1, vao_itens_max - vao_itens
            )
            for i, e in enumerate(expansao):
                vaos[i] += e
            excesso -= sum(expansao)
        # Passo 2: expandir margens (esquerda primeiro, depois direita).
        margem_esq = margem
        margem_dir = margem
        if excesso > 0:
            cap_esq = vao_itens_max - margem_esq
            dar_esq = min(cap_esq, excesso)
            margem_esq += dar_esq
            excesso -= dar_esq
        if excesso > 0:
            cap_dir = vao_itens_max - margem_dir
            dar_dir = min(cap_dir, excesso)
            margem_dir += dar_dir
            excesso -= dar_dir
        # Passo 3: excesso residual conforme alinhamento declarado pela
        # instância (R-10 / contrato_lancador.md 6.4).
        exc_esq, exc_dir = _split_excesso_lancador(excesso, alinhamento)
        textos = [
            "[{0}]{1}{2}".format(chip, " " * vao_chip_texto, texto)
            for chip, texto in itens
        ]
        partes_linha = [" " * exc_esq, " " * margem_esq]
        for i, t in enumerate(textos):
            partes_linha.append(t)
            if i < len(textos) - 1:
                partes_linha.append(" " * vaos[i])
        partes_linha.append(" " * margem_dir)
        partes_linha.append(" " * exc_dir)
        linha = "".join(partes_linha)
        return (
            [""] * margem_v_sup
            + [linha]
            + [""] * margem_v_inf
        )

    # Etapa 2 — distribuição em matriz (maximiza colunas, n_rows crescente).
    def _tentar_matriz(n_rows):
        n_col = (n + n_rows - 1) // n_rows
        # Largura independente por coluna (maior item da própria coluna).
        colunas = []
        for j in range(n_col):
            itens_col = itens[j * n_rows:(j + 1) * n_rows]
            if not itens_col:
                break
            chip_w_col = max(_chip_sub_w(c) for c, _ in itens_col)
            texto_w_col = max(len(t) for _, t in itens_col)
            col_w = chip_w_col + vao_chip_texto + texto_w_col
            colunas.append((itens_col, chip_w_col, texto_w_col, col_w))

        matriz_min = (
            margem
            + sum(col[3] for col in colunas)
            + (len(colunas) - 1) * vao_itens
            + margem
        )
        if content_w < matriz_min:
            return None

        excesso = content_w - matriz_min
        # Passo 1: expandir vãos entre colunas (cada vão independentemente até
        # o teto; maiores restos nos primeiros vãos).
        n_vaos = len(colunas) - 1
        vaos = [vao_itens] * n_vaos
        if excesso > 0 and n_vaos > 0:
            expansao = _distribuir_excesso_total(
                excesso, n_vaos, vao_itens_max - vao_itens
            )
            for i, e in enumerate(expansao):
                vaos[i] += e
            excesso -= sum(expansao)
        # Passo 2: expandir margens.
        margem_esq = margem
        margem_dir = margem
        if excesso > 0:
            cap_esq = vao_itens_max - margem_esq
            dar_esq = min(cap_esq, excesso)
            margem_esq += dar_esq
            excesso -= dar_esq
        if excesso > 0:
            cap_dir = vao_itens_max - margem_dir
            dar_dir = min(cap_dir, excesso)
            margem_dir += dar_dir
            excesso -= dar_dir
        # Passo 3: excesso residual conforme alinhamento declarado pela
        # instância (R-10 / contrato_lancador.md 6.4).
        exc_esq, exc_dir = _split_excesso_lancador(excesso, alinhamento)
        linhas_linha = []
        for r in range(n_rows):
            partes = []
            for idx_col, (itens_col, chip_w_col, texto_w_col, col_w) in enumerate(colunas):
                if r < len(itens_col):
                    chip, texto = itens_col[r]
                    celula = "[{0}]{1}{2}".format(
                        chip, " " * vao_chip_texto, texto
                    )
                    # Sub-colunas independentes alinhadas à esquerda dentro
                    # da largura da coluna.
                    partes.append(celula.ljust(col_w))
                else:
                    # Célula vazia ocupa a largura da coluna para manter o
                    # alinhamento horizontal das colunas subsequentes.
                    partes.append(" " * col_w)
            linha = (" " * exc_esq) + (" " * margem_esq)
            for idx_p, p in enumerate(partes):
                linha += p
                if idx_p < len(partes) - 1:
                    linha += " " * vaos[idx_p]
            linha += (" " * margem_dir) + (" " * exc_dir)
            linhas_linha.append(linha)
        return linhas_linha

    for n_rows in range(2, n + 1):
        linhas_linha = _tentar_matriz(n_rows)
        if linhas_linha is not None:
            return [""] * margem_v_sup + linhas_linha + [""] * margem_v_inf

    # Etapa 3 — coluna mínima válida (n_col=1, n_rows=n_itens).
    # Já garantido por content_w >= coluna_minima_content_w acima.
    excesso_min = content_w - coluna_minima_content_w
    exc_esq_min, exc_dir_min = _split_excesso_lancador(excesso_min, alinhamento)
    linhas_linha = []
    for chip, texto in itens:
        texto_padded = texto + " " * (max_texto_sub - len(texto))
        celula = "[{0}]{1}{2}".format(chip, " " * vao_chip_texto, texto_padded)
        linha = (
            " " * exc_esq_min
            + " " * margem
            + celula
            + " " * margem
            + " " * exc_dir_min
        )
        linhas_linha.append(linha)
    return [""] * margem_v_sup + linhas_linha + [""] * margem_v_inf
