"""Renderer declarativo derivado do modelo/JSON (H-0006 / H-0007 / H-0009 / H-0010A).

O renderer interpreta o ModeloTela produzido pelo pipeline H-0001 + H-0002
(``carregar_tela`` -> ``construir_modelo`` -> ``ModeloTela``) e gera uma
string visual deterministica composta por caixas bordeadas. O H-0010A
substitui os placeholders hardcoded do H-0006 por conteudo derivado do
modelo/JSON:

- cabecalho: titulo/descricao lidos de ``modelo.cabecalho``.
- corpo.elementos[]: percorridos na ordem declarada no JSON. Cada elemento
  e renderizado como uma caixa:
  - ``console`` -> caixa com titulo do elemento e linha placeholder fixa
    ``"(console)"`` (unica excecao declarada de texto nao proveniente do
    JSON, como marcador explicito de escopo).
  - ``dashboard`` -> caixa com titulo do elemento; para cada campo em
    ``_campos_inertes["campos"]`` com ``fonte == "literal"`` inclui o
    ``valor`` como linha de conteudo; campos com outra ``fonte`` sao
    ignorados (sem texto, sem erro).
  - ``lancador`` -> caixa com titulo do elemento; para cada item em
    ``_campos_inertes["itens"]`` inclui a linha ``"[{chip}] {texto}"``.
    Itens com ``texto`` acima de ``max_caracteres`` (lido de
    ``config/elementos/lancador.json`` via pipeline) levantam
    ``RenderizadorErro`` -- nunca truncar, nunca abreviar. Lista vazia
    produz caixa sem linhas de conteudo.
- barra_de_menus: caixa com label fixo ``"Menus"`` (rotulo visual apenas,
  sem comportamento derivado do label); os chips de
  ``modelo.barra_de_menus["chips"]`` sao dispostos horizontalmente de
  forma responsiva a partir de ``barra_de_menus.distribuicao`` (H-0016 /
  ADR-0014): tenta linha unica, depois multilinha (ate
  ``linhas.maximo``) e, se nao couber, levanta ``RenderizadorErro``
  (``erro_layout``) -- nunca omite/trunca/reordena chips. Cada chip na
  saida usa o formato ``"[{tecla}] {texto}"`` e aparece exatamente uma
  vez, na ordem declarada em ``chips[]``. ``regra_existencia`` e
  ``regra_ativo`` nao sao avaliadas neste ciclo.

O renderer continua recebendo os parametros opcionais ``tipo_borda``
(``"curva"`` default ou ``"reta"``) e ``largura`` (quando ``None``,
fallback ``TOTAL_WIDTH = 42``). Quando ``largura`` e fornecida, deriva
``inner_w = largura - 2``, ``content_w = largura - 3`` e
``label_max = largura - 4``.

ESCOPO (H-0010A):
- Apenas renderizacao visual declarativa a partir de ModeloTela.
- Nenhum texto de item, chip, tecla, tela_destino, rotulo de menu ou
  valor de dashboard e hardcoded -- todos vem do modelo/JSON. A unica
  excecao e a linha placeholder ``"(console)"`` do elemento console,
  declarada explicitamente como marcador de escopo.
- O binding interno de borda da demo (``b``) deixa de aparecer na saida
  do renderer, pois nunca foi declarado no JSON; o comando permanece
  apenas como controle interno da demo.
- Nao acessa config/telas/*.json diretamente.
- Nao chama carregar_tela nem construir_modelo.
- Nao importa json, os, pathlib nem tela.loader.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo.
- Nao calcula largura de terminal, nao paginar, nao selecionar.
- Nao avalia regra_existencia nem regra_ativo.
- Nao decide Sair/Voltar por id de tela -- o texto do chipEsc vem do JSON.

A largura total e parametrizavel desde o H-0009: ``renderizar_tela`` aceita
``largura`` opcional; quando omitida (``None``), usa o fallback
deterministico ``TOTAL_WIDTH = 42`` (heranca tecnica provisoria do
H-0006, sem carater normativo de layout).

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela
from tela.distribuicao_matricial import (
    calcular_distribuicao,
    alinhar_na_celula,
)


class RenderizadorErro(Exception):
    """Erro de renderizacao visual de tela."""


TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38

_PLACEHOLDER_CONSOLE = "(console)"
_LABEL_BARRA = "Menus"



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


# Sinalização de quadro mínimo global acionado por inviabilidade do ``lancador``
# (ADR-0023). Quando uma função auxiliar detecta ``content_w <
# coluna_minima_content_w``, atribui ``True`` neste atributo de módulo para que
# ``renderizar_tela`` substitua a tela normal pelo quadro mínimo canônico
# (ADR-0017). O renderer é puro: o sinal é redefinido no início de cada
# ``renderizar_tela`` e nunca persiste entre chamadas (R-14).
_quadro_minimo_lancador_ativo = False

# Defaults normativos do alias transitório ``distribuicao = "horizontal"`` e
# de ``distribuicao`` ausente/None (H-0016 / ADR-0014). Replica o objeto
# canônico de referência, exceto por ``ancoras`` vazio (apenas o objeto
# canônico declarado no JSON pode definir âncoras).
_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT = {
    "modo": "horizontal_responsiva",
    "ordem": {
        "politica": "declaracao",
        "ancoras": {},
    },
    "tentativa_inicial": "linha_unica",
    "quebra": "multilinha_quando_nao_couber",
    "preenchimento_multilinha": "coluna_a_coluna",
    "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
    "linhas": {"minimo": 1, "maximo": 2, "preferir_menor_numero": True},
    "alinhamento_linhas": "esquerda",
    "espacamentos": {
        "margem_horizontal":         {"minimo": 1, "maximo": None},
        "vao_chip_texto":            {"minimo": 1, "maximo": 3},
        "vao_entre_chips":           {"minimo": 2, "maximo": 6},
        "vao_entre_colunas":         {"minimo": 2, "maximo": 8},
        "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0},
    },
    "colunas": {
        "largura": "por_maior_item_da_coluna",
        "subcolunas": {
            "chip":  {"alinhamento": "esquerda"},
            "texto": {"alinhamento": "esquerda"},
        },
    },
    "overflow": {
        "quando_nao_couber": "erro_layout",
        "nao_omitir_chips":  True,
        "nao_truncar_texto": True,
        "nao_reordenar":     True,
    },
}

_PREENCHIMENTOS_MULTILINHA_VALIDOS = ("coluna_a_coluna", "linha_a_linha")


_BORDAS = {
    "curva": {
        "tl": "╭", "tr": "╮",
        "bl": "╰", "br": "╯",
        "v":  "│", "h":  "─",
    },
    "reta": {
        "tl": "┌", "tr": "┐",
        "bl": "└", "br": "┘",
        "v":  "│", "h":  "─",
    },
}


def _linha_topo(label, borda, label_max):
    """Monta a borda superior com label.

    Formato: {tl} {LABEL} {h x (label_max-len(LABEL))}{tr}
    Comprimento total: label_max + 4 == total_w.
    """
    label_trunc = label[:label_max]
    dashes = label_max - len(label_trunc)
    return "{tl} {0} {1}{tr}".format(
        label_trunc, borda["h"] * dashes, tl=borda["tl"], tr=borda["tr"]
    )


def _linha_base(borda, inner_w):
    """Monta a borda inferior: {bl}{h x inner_w}{br}.

    Comprimento total: inner_w + 2 == total_w.
    """
    return "{bl}{0}{br}".format(
        borda["h"] * inner_w, bl=borda["bl"], br=borda["br"]
    )


def _linha_conteudo(texto, borda, content_w):
    """Monta uma linha de conteudo: {v} {text:<content_w}{v}.

    Comprimento total: content_w + 3 == total_w.
    """
    txt = texto[:content_w]
    pad = " " * (content_w - len(txt))
    return "{v} {0}{1}{v}".format(txt, pad, v=borda["v"])


def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max, altura_alvo=None):
    """Monta uma caixa bordeada com label no topo e linhas de conteudo.

    Quando altura_alvo e fornecida, a caixa ocupa exatamente essa altura:
    linhas de fill bordeadas (borda["v"] + " " * inner_w + borda["v"]) sao
    inseridas entre o conteudo e a base ate que a caixa tenha altura_alvo linhas.
    Quando None, comportamento atual preservado (topo + conteudo + base).
    """
    partes = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto, borda, content_w))
    if altura_alvo is not None:
        linha_fill = borda["v"] + " " * inner_w + borda["v"]
        while len(partes) < altura_alvo - 1:
            partes.append(linha_fill)
    partes.append(_linha_base(borda, inner_w))
    return "\n".join(partes)


def _contar_linhas(caixa_str):
    """Conta o numero de linhas de um bloco multi-linha sem trailing newline.

    Uma caixa gerada por ``_caixa`` (ou um bloco de preenchimento) e uma
    string contendo ``N`` linhas separadas por ``"\\n"``, sem ``"\\n"`` final.
    Portanto o numero de linhas e ``caixa_str.count("\\n") + 1``.
    Usado pela ocupacao vertical (H-0015) para calcular ``L_cab``,
    ``L_corpo_conteudo`` e ``L_barra``.
    """
    return caixa_str.count("\n") + 1


def _pesos_distribuicao(distribuicao, n_filhos):
    """Devolve a lista de pesos positivos a partir da declaracao de distribuicao.

    - ``igual``: pesos equivalentes (``[1] * n_filhos``) — ADR-0018 D5.
    - ``percentual``/``fracao``: os proprios valores declarados, associados
      posicionalmente a ordem declarada dos filhos — ADR-0018 D6/D7.

    O algoritmo e generico: nenhum vetor concreto e hardcoded. O dict ja
    validado pelo loader e usado como-esta, sem substituir seus valores.
    """
    modo = distribuicao.get("modo")
    if modo == "igual":
        return [1] * n_filhos
    return list(distribuicao.get("valores", []))


def _distribuir_alturas(altura_disponivel, pesos):
    """Reparte ``altura_disponivel`` entre os pesos pelo metodo dos maiores
    restos (ADR-0015 secao 5.8; ADR-0018 D6/D7).

    Invariantes:
    - ``sum(cotas) == altura_disponivel`` (soma exata);
    - cada cota e inteira nao negativa;
    - empates de resto fracionario sao resolvidos pela ORDEM DECLARADA
      (menor indice prevalece).

    Algoritmo:
    1. cota ideal real de cada filho = ``altura_disponivel * peso / soma``;
    2. parte inteira (floor) de cada cota;
    3. ``faltam = altura_disponivel - sum(partes_inteiras)``;
    4. ordenar filhos por resto fracionario decrescente, desempatando por
       indice crescente (ordem declarada);
    5. atribuir uma unidade aos ``faltam`` maiores restos.
    """
    n = len(pesos)
    if n == 0:
        return []
    soma = float(sum(pesos))
    if soma <= 0:
        raise RenderizadorErro(
            "distribuicao: soma de pesos nao e positiva: {0}".format(soma)
        )
    ideais = [altura_disponivel * p / soma for p in pesos]
    cotas = [int(x) for x in ideais]  # floor (valores >= 0)
    faltam = altura_disponivel - sum(cotas)
    restos = sorted(
        range(n),
        key=lambda i: (-ideais[i] + int(ideais[i]), i),
    )
    for k in range(faltam):
        cotas[restos[k]] += 1
    return cotas


def _distribuir_larguras(largura_disponivel, pesos):
    """Reparte ``largura_disponivel`` entre os pesos pelo metodo dos maiores
    restos no eixo horizontal (H-0026 / ADR-0015 D5-D8; ADR-0018 D6/D7).

    Analogico a ``_distribuir_alturas``: o algoritmo de maiores restos e
    identico para qualquer eixo. Esta e uma rotina LOCAL ao calculo de cotas
    horizontais, independente do helper vertical, para preservar sem risco o
    comportamento aprovado pelo H-0025.

    Invariantes:
    - ``sum(cotas) == largura_disponivel`` (soma exata);
    - cada cota e inteira nao negativa;
    - empates de resto fracionario sao resolvidos pela ORDEM DECLARADA
      (menor indice prevalece).
    """
    n = len(pesos)
    if n == 0:
        return []
    soma = float(sum(pesos))
    if soma <= 0:
        raise RenderizadorErro(
            "distribuicao: soma de pesos nao e positiva: {0}".format(soma)
        )
    ideais = [largura_disponivel * p / soma for p in pesos]
    cotas = [int(x) for x in ideais]  # floor (valores >= 0)
    faltam = largura_disponivel - sum(cotas)
    restos = sorted(
        range(n),
        key=lambda i: (-ideais[i] + int(ideais[i]), i),
    )
    for k in range(faltam):
        cotas[restos[k]] += 1
    return cotas


def _linhas_console(elemento):
    """Linhas de conteudo para elemento console (placeholder de escopo)."""
    return [_PLACEHOLDER_CONSOLE]


def _linhas_dashboard(elemento):
    """Linhas de conteudo para elemento dashboard a partir de campos[].

    Apenas campos com ``fonte == "literal"`` contribuem com o ``valor``
    como linha de conteudo. Campos com outra ``fonte`` (ex.: ``"pendente"``)
    sao ignorados -- sem texto, sem erro, sem placeholder.
    """
    campos = elemento._campos_inertes.get("campos", []) or []
    linhas = []
    for campo in campos:
        if not isinstance(campo, dict):
            continue
        if campo.get("fonte") == "literal":
            valor = campo.get("valor", "")
            linhas.append(valor)
    return linhas


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
        global _quadro_minimo_lancador_ativo
        _quadro_minimo_lancador_ativo = True
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


def _texto_chip_barra(chip, vao=1):
    """Monta o texto de um chip da barra no formato ``"[{tecla}]{padding}{texto}"``."""
    tecla = chip.get("tecla", "")
    texto = chip.get("texto", "")
    return "[{0}]{1}{2}".format(tecla, " " * vao, texto)


def _normalizar_distribuicao(distribuicao):
    """Normaliza ``barra_de_menus.distribuicao`` (H-0016 / ADR-0014).

    - ``None``/ausente ou string ``"horizontal"`` -> objeto canônico default
      (defaults normativos do ADR-0014, sem âncoras).
    - dict -> retornado como declarado (validado depois).
    - outros valores (string desconhecida, tipo invalido) -> ``RenderizadorErro``.

    Não muta o dict recebido. O renderer é inerte.
    """
    if distribuicao is None:
        return _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT
    if isinstance(distribuicao, str):
        if distribuicao == "horizontal":
            return _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT
        raise RenderizadorErro(
            "modo de distribuicao desconhecido: {0!r}; valores aceitos: "
            "objeto canônico com modo 'horizontal_responsiva' ou alias "
            "'horizontal'".format(distribuicao)
        )
    if isinstance(distribuicao, dict):
        return distribuicao
    raise RenderizadorErro(
        "distribuicao com tipo invalido: {0}; esperado objeto canônico, "
        "alias 'horizontal' ou ausente".format(type(distribuicao).__name__)
    )


def _eh_int_nao_bool(valor):
    """True quando ``valor`` é int mas não bool (bool é subclasse de int)."""
    return isinstance(valor, int) and not isinstance(valor, bool)


def _validar_distribuicao(distribuicao):
    """Validações defensivas determinísticas da declaração (H-0016).

    Segue o padrão defensivo de ``modo`` desconhecido (handoff H-0016),
    estendido aos campos cobertos pelas notas PR-M-01 a PR-M-04 da
    auditoria pós-revisão. Não bloqueia a migração canônica (valores
    válidos); apenas rejeita valores inválidos de forma determinística.
    Levanta ``RenderizadorErro`` em qualquer divergência. Não muta o dict.
    """
    modo = distribuicao.get("modo")
    if modo != "horizontal_responsiva":
        raise RenderizadorErro(
            "modo de distribuicao desconhecido: {0!r}; unico modo suportado "
            "neste ciclo: 'horizontal_responsiva'".format(modo)
        )

    tentativa = distribuicao.get("tentativa_inicial")
    if tentativa is not None and tentativa != "linha_unica":
        raise RenderizadorErro(
            "tentativa_inicial {0!r} nao suportado neste ciclo; "
            "valor aceito: 'linha_unica'".format(tentativa)
        )

    quebra_val = distribuicao.get("quebra")
    if quebra_val is not None and quebra_val != "multilinha_quando_nao_couber":
        raise RenderizadorErro(
            "quebra {0!r} nao suportado neste ciclo; "
            "valor aceito: 'multilinha_quando_nao_couber'".format(quebra_val)
        )

    ordem = distribuicao.get("ordem") or {}
    politica = ordem.get("politica")
    if politica != "declaracao":
        raise RenderizadorErro(
            "ordem.politica nao suportada: {0!r}; unico valor suportado "
            "neste ciclo: 'declaracao'".format(politica)
        )

    preench = distribuicao.get("preenchimento_multilinha")
    suportados = distribuicao.get("preenchimentos_multilinha_suportados") or []
    if preench not in _PREENCHIMENTOS_MULTILINHA_VALIDOS:
        raise RenderizadorErro(
            "preenchimento_multilinha desconhecido: {0!r}; valores aceitos: "
            "coluna_a_coluna, linha_a_linha".format(preench)
        )
    if preench not in suportados:
        raise RenderizadorErro(
            "preenchimento_multilinha {0!r} nao esta em "
            "preenchimentos_multilinha_suportados {1!r}".format(preench, suportados)
        )

    linhas_cfg = distribuicao.get("linhas") or {}
    minimo = linhas_cfg.get("minimo")
    maximo = linhas_cfg.get("maximo")
    if not _eh_int_nao_bool(minimo) or minimo < 1:
        raise RenderizadorErro(
            "linhas.minimo invalido: {0!r}; esperado int >= 1".format(minimo)
        )
    if not _eh_int_nao_bool(maximo) or maximo < 1:
        raise RenderizadorErro(
            "linhas.maximo invalido: {0!r}; esperado int >= 1".format(maximo)
        )
    if maximo < minimo:
        raise RenderizadorErro(
            "linhas.maximo ({0}) menor que linhas.minimo ({1})".format(
                maximo, minimo
            )
        )

    overflow = distribuicao.get("overflow") or {}
    quando = overflow.get("quando_nao_couber")
    if quando != "erro_layout":
        raise RenderizadorErro(
            "overflow.quando_nao_couber desconhecido: {0!r}; unico valor "
            "aceito neste ciclo: 'erro_layout'".format(quando)
        )
    for flag in ("nao_omitir_chips", "nao_truncar_texto", "nao_reordenar"):
        val = overflow.get(flag)
        if not isinstance(val, bool):
            raise RenderizadorErro(
                "overflow.{0} deve ser booleano; recebido: {1!r} "
                "({2})".format(flag, val, type(val).__name__)
            )
        if val is False:
            raise RenderizadorErro(
                "overflow.{0} deve ser true; recebido: false".format(flag)
            )

    preferir = linhas_cfg.get("preferir_menor_numero")
    if preferir is not None:
        if not isinstance(preferir, bool):
            raise RenderizadorErro(
                "linhas.preferir_menor_numero deve ser bool; "
                "recebido: {0!r} ({1})".format(preferir, type(preferir).__name__)
            )
        if preferir is False:
            raise RenderizadorErro(
                "preferir_menor_numero=false nao suportado neste ciclo"
            )

    alinhamento = distribuicao.get("alinhamento_linhas")
    if alinhamento is not None and alinhamento != "esquerda":
        raise RenderizadorErro(
            "alinhamento_linhas {0!r} nao suportado neste ciclo; "
            "valor aceito: 'esquerda'".format(alinhamento)
        )

    esp = distribuicao.get("espacamentos") or {}

    vao_vert_cfg = esp.get("vao_vertical_entre_linhas") or {}
    vav_min = vao_vert_cfg.get("minimo", 0)
    vav_max = vao_vert_cfg.get("maximo", 0)
    if (
        (_eh_int_nao_bool(vav_min) and vav_min > 0)
        or (_eh_int_nao_bool(vav_max) and vav_max > 0)
    ):
        raise RenderizadorErro(
            "vao_vertical_entre_linhas com valor > 0 nao suportado neste ciclo"
        )

    margem_cfg = esp.get("margem_horizontal") or {}
    margem_min = margem_cfg.get("minimo")
    if margem_min is not None:
        if not _eh_int_nao_bool(margem_min) or margem_min < 0:
            raise RenderizadorErro(
                "margem_horizontal.minimo invalido: {0!r}; "
                "esperado int >= 0".format(margem_min)
            )
        margem_max = margem_cfg.get("maximo")
        if margem_max is not None:
            if not _eh_int_nao_bool(margem_max) or margem_max < margem_min:
                raise RenderizadorErro(
                    "margem_horizontal.maximo invalido: {0!r}; "
                    "esperado null ou int >= minimo ({1})".format(
                        margem_max, margem_min
                    )
                )

    vao_ct_cfg = esp.get("vao_chip_texto") or {}
    vao_ct_min = vao_ct_cfg.get("minimo")
    if vao_ct_min is not None:
        if not _eh_int_nao_bool(vao_ct_min) or vao_ct_min < 1:
            raise RenderizadorErro(
                "vao_chip_texto.minimo invalido: {0!r}; "
                "esperado int >= 1".format(vao_ct_min)
            )
        vao_ct_max = vao_ct_cfg.get("maximo")
        if vao_ct_max is not None:
            if not _eh_int_nao_bool(vao_ct_max) or vao_ct_max < vao_ct_min:
                raise RenderizadorErro(
                    "vao_chip_texto.maximo invalido: {0!r}; "
                    "esperado null ou int >= minimo ({1})".format(
                        vao_ct_max, vao_ct_min
                    )
                )

    vao_chips_cfg = esp.get("vao_entre_chips") or {}
    vao_chips_min = vao_chips_cfg.get("minimo", 1)
    vao_chips_max = vao_chips_cfg.get("maximo")
    if vao_chips_max is not None:
        if not _eh_int_nao_bool(vao_chips_max) or vao_chips_max < vao_chips_min:
            raise RenderizadorErro(
                "vao_entre_chips.maximo invalido: {0!r}; "
                "esperado null ou int >= minimo ({1})".format(
                    vao_chips_max, vao_chips_min
                )
            )

    vao_colunas_cfg = esp.get("vao_entre_colunas") or {}
    vao_colunas_min = vao_colunas_cfg.get("minimo", 1)
    vao_colunas_max = vao_colunas_cfg.get("maximo")
    if vao_colunas_max is not None:
        if not _eh_int_nao_bool(vao_colunas_max) or vao_colunas_max < vao_colunas_min:
            raise RenderizadorErro(
                "vao_entre_colunas.maximo invalido: {0!r}; "
                "esperado null ou int >= minimo ({1})".format(
                    vao_colunas_max, vao_colunas_min
                )
            )

    colunas = distribuicao.get("colunas") or {}
    largura_col = colunas.get("largura")
    if largura_col is not None and largura_col != "por_maior_item_da_coluna":
        raise RenderizadorErro(
            "colunas.largura {0!r} nao suportado neste ciclo; "
            "valor aceito: 'por_maior_item_da_coluna'".format(largura_col)
        )

    subcolunas = colunas.get("subcolunas") or {}
    for sub in ("chip", "texto"):
        alin = (subcolunas.get(sub) or {}).get("alinhamento")
        if alin is not None and alin != "esquerda":
            raise RenderizadorErro(
                "subcolunas.{0}.alinhamento {1!r} nao suportado neste ciclo; "
                "valor aceito: 'esquerda'".format(sub, alin)
            )


def _validar_ancoras(chips, distribuicao):
    """Valida âncoras como restrição declarativa (H-0016 / ADR-0014).

    - ``ancoras.primeiro`` valida que os ids declarados ocupam as posições
      iniciais de ``chips[]``, na ordem declarada.
    - ``ancoras.ultimo`` valida que os ids declarados ocupam as posições
      finais de ``chips[]``, na ordem declarada.
    - id declarado em âncora mas inexistente em ``chips[]`` -> erro.
    - id existente mas em posição errada -> erro.

    O renderer NÃO reordena chips para satisfazer âncoras: a violação é
    erro determinístico, não correção silenciosa. Sem ``ancoras`` (ausente
    ou vazio), nenhuma validação de âncora é executada.
    """
    ordem = distribuicao.get("ordem") or {}
    ancora = ordem.get("ancoras") or {}
    ids = [c.get("id") for c in chips]
    n = len(ids)

    primeiro = ancora.get("primeiro") or []
    if primeiro:
        for aid in primeiro:
            if aid not in ids:
                raise RenderizadorErro(
                    "ancora primeiro: id {0!r} nao existe em chips[]".format(aid)
                )
        for i, aid in enumerate(primeiro):
            if i >= n or ids[i] != aid:
                raise RenderizadorErro(
                    "ancora primeiro violada: esperado id {0!r} na posicao "
                    "{1}, encontrado {2!r}".format(aid, i, ids[i] if i < n else None)
                )

    ultimo = ancora.get("ultimo") or []
    if ultimo:
        for aid in ultimo:
            if aid not in ids:
                raise RenderizadorErro(
                    "ancora ultimo: id {0!r} nao existe em chips[]".format(aid)
                )
        k = len(ultimo)
        for i, aid in enumerate(ultimo):
            pos = n - k + i
            if pos < 0 or ids[pos] != aid:
                raise RenderizadorErro(
                    "ancora ultimo violada: esperado id {0!r} na posicao "
                    "final, encontrado {1!r}".format(aid, ids[pos] if pos >= 0 else None)
                )


def _montar_coluna_a_coluna(texto_chips, n_linhas, vao_entre_colunas):
    """Distribui ``texto_chips`` em ``n_linhas`` no modo coluna_a_coluna.

    Preenche coluna por coluna (de cima para baixo); a largura de cada
    coluna é a do maior chip da coluna; colunas separadas por
    ``vao_entre_colunas`` espaços. Retorna a lista de linhas (strings).
    """
    n = len(texto_chips)
    n_colunas = (n + n_linhas - 1) // n_linhas
    colunas = [[] for _ in range(n_colunas)]
    for idx, txt in enumerate(texto_chips):
        colunas[idx // n_linhas].append(txt)
    larguras = [max(len(s) for s in col) for col in colunas]
    sep = " " * vao_entre_colunas
    linhas = []
    for r in range(n_linhas):
        partes = []
        for c in range(n_colunas):
            if r < len(colunas[c]):
                partes.append(colunas[c][r].ljust(larguras[c]))
        linhas.append(sep.join(partes).rstrip())
    return linhas


def _montar_linha_a_linha(texto_chips, n_linhas, vao_entre_chips):
    """Distribui ``texto_chips`` em ``n_linhas`` no modo linha_a_linha.

    Preenche linha por linha; cada linha recebe até ``ceil(N/K)`` chips
    consecutivos, separados por ``vao_entre_chips`` espaços. Retorna a
    lista de linhas (strings).
    """
    n = len(texto_chips)
    chips_por_linha = (n + n_linhas - 1) // n_linhas
    sep = " " * vao_entre_chips
    linhas = []
    for i in range(n_linhas):
        chunk = texto_chips[i * chips_por_linha:(i + 1) * chips_por_linha]
        if chunk:
            linhas.append(sep.join(chunk))
    return linhas


def _linhas_barra(barra_de_menus, content_w):
    """Linhas de conteudo para a caixa da barra de menus (H-0016).

    Renderiza os chips da ``barra_de_menus`` em distribuição horizontal
    responsiva (ADR-0014), a partir de ``barra_de_menus.distribuicao`` e
    ``barra_de_menus.chips[]``:

    1. normaliza ``distribuicao`` (alias string ``"horizontal"``/ausente ->
       defaults normativos; objeto canônico -> usado como declarado);
    2. valida defensivamente a declaração e as âncoras (restrição, nunca
       reordenação);
    3. tenta linha única; se couber em ``content_w``, retorna uma linha;
    4. caso contrário, tenta multilinha de 2 até ``linhas.maximo`` linhas,
       aplicando ``preenchimento_multilinha`` (``coluna_a_coluna`` ou
       ``linha_a_linha``); retorna na primeira configuração que encaixar;
    5. se nenhuma configuração couber, levanta ``RenderizadorErro``
       (``overflow.quando_nao_couber = "erro_layout"``) -- nunca omite,
       nunca trunca, nunca reordena.

    Cada chip é renderizado como ``"[{tecla}] {texto}"``. A ordem de
    saída é sempre a ordem declarada em ``chips[]``. ``regra_existencia``
    e ``regra_ativo`` não são avaliadas neste ciclo.

    ``content_w`` é a largura disponível para conteúdo dentro da caixa
    (``total_w - 3``). Retorna lista de strings, cada uma uma linha de
    conteúdo da caixa (invariante de ``l_barra = len(linhas_barra) + 2``
    preservado).
    """
    if not isinstance(barra_de_menus, dict):
        return []
    chips_raw = barra_de_menus.get("chips", []) or []
    chips = [c for c in chips_raw if isinstance(c, dict)]
    if not chips:
        return []

    distribuicao = _normalizar_distribuicao(
        barra_de_menus.get("distribuicao")
    )
    _validar_distribuicao(distribuicao)
    _validar_ancoras(chips, distribuicao)

    esp = distribuicao.get("espacamentos") or {}
    vao_ct = (esp.get("vao_chip_texto") or {}).get("minimo", 1)
    margem = (esp.get("margem_horizontal") or {}).get("minimo", 0)
    vao_entre_chips = (esp.get("vao_entre_chips") or {}).get("minimo", 2)
    vao_entre_colunas = (esp.get("vao_entre_colunas") or {}).get("minimo", 2)

    texto_chips = [_texto_chip_barra(c, vao=vao_ct) for c in chips]
    prefixo = " " * margem
    largura_util = content_w - 2 * margem

    linhas_cfg = distribuicao.get("linhas") or {}
    minimo = linhas_cfg.get("minimo", 1)
    maximo = linhas_cfg.get("maximo", 2)
    preenchimento = distribuicao.get("preenchimento_multilinha", "coluna_a_coluna")

    sep_chips = " " * vao_entre_chips
    linha_unica = sep_chips.join(texto_chips)
    if minimo <= 1 and largura_util >= 0 and len(linha_unica) <= largura_util:
        return [prefixo + linha_unica]

    inicio_multilinha = max(2, minimo)
    for n_linhas in range(inicio_multilinha, maximo + 1):
        if preenchimento == "coluna_a_coluna":
            linhas = _montar_coluna_a_coluna(
                texto_chips, n_linhas, vao_entre_colunas
            )
        else:
            linhas = _montar_linha_a_linha(
                texto_chips, n_linhas, vao_entre_chips
            )
        if linhas and largura_util >= 0 and max(len(l) for l in linhas) <= largura_util:
            return [prefixo + l for l in linhas]

    raise RenderizadorErro(
        "erro_layout: chips da barra_de_menus ({0}) nao cabem em {1} "
        "caracteres uteis (content_w={2}, margem={3}) com no maximo {4} linhas "
        "(preenchimento={5}); overflow.quando_nao_couber='erro_layout' proibe "
        "omitir/truncar/reordenar".format(
            len(texto_chips), largura_util, content_w, margem, maximo, preenchimento
        )
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


def _linhas_distribuicao_matricial(elemento, content_w, altura_alvo):
    """Renderiza os participantes de um elemento em grade (motor centralizado).

    H-0035 / ADR-0025: usa ``calcular_distribuicao`` para organizar os
    participantes imediatos do elemento dentro da area util (``content_w`` de
    largura por ``altura_alvo - 2`` de altura interna). Devolve a lista de
    linhas de conteudo (cada uma com no maximo ``content_w`` caracteres) para
    ser embrulhada por ``_caixa``.

    Quando o motor sinaliza fallback (nenhuma formacao cabe), sinaliza o quadro
    minimo canonico global (mecanismo ADR-0017/ADR-0023) e devolve ``[]`` — o
    ``renderizar_tela`` substitui integralmente a tela pelo quadro minimo.

    Determinismo: a saida depende apenas do elemento, ``content_w`` e
    ``altura_alvo``. Sem estado residual, sem efeito parcial antes de erro.
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

    # Requisito minimo interno de cada participante: largura = comprimento do
    # texto; altura = 1 linha. DEC-APP-0025-01: quando minimo_fixo e excedido,
    # o participante recebe a area calculada e trata seu conteudo internamente;
    # o distribuidor externo NAO cresce a coluna/linha por essa exigencia.
    min_ws = [len(p) for p in participantes]
    min_hs = [1 for _ in participantes]

    # Altura util para o motor. Quando altura_alvo e None (composicao orientada
    # pelo conteudo), estimamos uma area suficiente para a formacao caber, de
    # modo que a caixa cresca naturalmente. Usamos um limite generoso baseado
    # no numero de participantes; o motor selecionara a formacao preferida.
    if area_h is None:
        # Estimativa: cada participante em sua propria linha caberia; deixamos
        # o motor decidir com area vertical folgada.
        area_h_calc = max(1, n) + 8
    else:
        area_h_calc = area_h

    resultado = calcular_distribuicao(
        area_w=area_w,
        area_h=area_h_calc,
        n_participantes=n,
        config=config,
        min_ws=min_ws,
        min_hs=min_hs,
    )

    if resultado["fallback"]:
        global _quadro_minimo_lancador_ativo
        _quadro_minimo_lancador_ativo = True
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

    for celula in resultado["celulas"]:
        # DEC-APP-0025-01: a camada matricial entrega o conteudo integral ao
        # participante; a fronteira interna decide a visibilidade fisica.
        _renderizar_participante_na_celula(
            canvas=canvas,
            texto_integral=participantes[celula["participante"]],
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


def _caixa_de_elemento(elemento, borda, inner_w, content_w, label_max, altura_alvo=None):
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
    """
    # H-0035 / ADR-0025: quando o elemento funcional declara distribuicao_
    # matricial, ela organiza os participantes imediatos em grade. Para console
    # substitui as politicas geometricas antigas (DEC-APP-0025-03); para
    # lancador tem precedencia sobre ADR-0001/0002/0003 (DEC-APP-0025-02); para
    # dashboard organiza os campos. Ausencia preserva o comportamento anterior.
    dm = getattr(elemento, "distribuicao_matricial", None)
    if dm is not None and elemento.tipo in ("console", "dashboard", "lancador"):
        rotulo_padrao = {
            "console": "CONSOLE",
            "dashboard": "DASHBOARD",
            "lancador": "LANCADOR",
        }[elemento.tipo]
        titulo_el = elemento._campos_inertes.get("titulo", rotulo_padrao)
        linhas = _linhas_distribuicao_matricial(elemento, content_w, altura_alvo)
        return _caixa(
            titulo_el.upper(), linhas,
            borda, inner_w, content_w, label_max, altura_alvo,
        )

    if elemento.tipo == "console":
        titulo_el = elemento._campos_inertes.get("titulo", "CONSOLE")
        return _caixa(
            titulo_el.upper(), _linhas_console(elemento),
            borda, inner_w, content_w, label_max, altura_alvo,
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
                    altura_alvo=cota,
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
                    )
                    if bloco:
                        partes.append(bloco)
                else:
                    caixa = _caixa_de_elemento(
                        elemento, borda, inner_w, content_w, label_max,
                        altura_alvo=altura_disponivel,
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
                    )
                    if bloco:
                        partes.append(bloco)
                else:
                    caixa = _caixa_de_elemento(
                        elemento, borda, inner_w, content_w, label_max
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
                )
                if bloco:
                    partes.append(bloco)
            else:
                caixa = _caixa_de_elemento(
                    elemento, borda, inner_w, content_w, label_max
                )
                if caixa is not None:
                    partes.append(caixa)

    return "\n".join(partes)


def _renderizar_container_horizontal(
    distribuicao, elementos, borda, total_w, altura_disponivel, larguras=None,
):
    """Renderiza elementos em disposicao horizontal dentro de um container.

    Quando larguras e None, aplica DA-01/DA-02 (ADR-0024):
    - N == 1 sem distribuicao: participante unico recebe largura integral (DA-01).
    - N > 1 sem distribuicao: composicao invalida rejeitada com RenderizadorErro
      DA-02; ausencia de distribuicao nunca equivale a particionamento uniforme.
    Quando larguras sao fornecidas externamente (ex.: matriz), usa-as diretamente.
    Grupo e despachado recursivamente via _renderizar_container (H-0027).
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
                estrutura=estrutura_g, matriz_config=matriz_g,
            )
            linhas_area = bloco.split("\n") if bloco else []
        else:
            caixa_str = _caixa_de_elemento(elemento, borda, w - 2, w - 3, w - 4)
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


def _renderizar_container_matriz(matriz_config, elementos, borda, total_w, altura_disponivel):
    """Renderiza um grupo ``estrutura: matriz`` com grade bidimensional comum.

    As cotas dos dois eixos sao calculadas uma unica vez para o container
    matricial e compartilhadas por todas as celulas. As linhas sao renderizadas
    como containers horizontais com larguras pre-computadas, preservando as
    primitivas de borda e preenchimento ja existentes.
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
        )
        if bloco:
            blocos.append(bloco)

    return "\n".join(blocos)


def _renderizar_container(
    arranjo, distribuicao, elementos, borda, total_w, altura_disponivel,
    estrutura=None, matriz_config=None,
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
    """
    if not elementos:
        return ""

    if estrutura == "matriz":
        return _renderizar_container_matriz(
            matriz_config, elementos, borda, total_w, altura_disponivel
        )

    arr = arranjo
    if arr == "sobreposto":
        arr = "vertical"
    if arr == "lado_a_lado":
        arr = "horizontal"

    if arr == "horizontal":
        return _renderizar_container_horizontal(
            distribuicao, elementos, borda, total_w, altura_disponivel
        )
    else:
        inner_w = total_w - 2
        content_w = total_w - 3
        label_max = total_w - 4
        return _renderizar_container_vertical(
            distribuicao, elementos, borda,
            total_w, inner_w, content_w, label_max, altura_disponivel,
        )


def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None,
                             larguras=None):
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
            elemento, borda, w - 2, w - 3, w - 4
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


def _quadro_minimo_global(total_w, altura):
    """Gera o quadro mínimo canônico global (ADR-0017 seção 9 / ADR-0023).

    Reutilizado tanto para terminal fisicamente pequeno (ADR-0017) quanto para
    inviabilidade da área alocada ao ``lancador`` (ADR-0023): em ambos os casos
    o quadro mínimo substitui integralmente toda a tela normal. Comunica
    inequivocamente "terminal pequeno demais", adequa-se à largura disponível,
    não gera scroll nem overflow, não cria mensagem local do ``lancador`` e é
    substituído automaticamente pela tela normal quando o espaço retorna.

    ``altura`` pode ser ``None``: neste caso, o quadro usa apenas a linha de
    aviso (comportamento determinístico sem ocupação vertical).
    """
    if total_w >= 23:
        msg = "terminal pequeno demais"
    elif total_w >= 9:
        msg = "tela peq."
    else:
        msg = ""
    linha_aviso = msg[:total_w].ljust(total_w)
    linha_vazia = " " * total_w
    if altura is None:
        return linha_aviso + "\n"
    linhas = [linha_aviso] + [linha_vazia] * (altura - 1)
    return "\n".join(linhas) + "\n"


def renderizar_tela(
    modelo: ModeloTela,
    tipo_borda: str = "curva",
    largura: int | None = None,
    altura: int | None = None,
) -> str:
    """Renderiza ModeloTela como string visual declarativa (H-0010A).

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).
        tipo_borda: nome do conjunto de caracteres de borda a usar.
            Valores aceitos: ``"curva"`` (default) e ``"reta"``. Outros
            valores lancam RenderizadorErro (case-sensitive).
        largura: largura total (em caracteres Python) de cada linha
            nao-vazia da saida. Quando ``None`` (default), usa o fallback
            deterministico ``TOTAL_WIDTH = 42``. Quando fornecida, deriva
            ``inner_w = largura - 2``, ``content_w = largura - 3`` e
            ``label_max = largura - 4``. ``largura < 10`` tem comportamento
            indefinido neste ciclo (nao validado, nao tratado).
        altura: altura alvo (em linhas fisicas) da saida. Quando ``None``
            (default), nenhuma area distribuivel e considerada e a saida
            tem apenas as linhas das caixas (cabecalho + corpo +
            barra_de_menus) orientadas pelo conteudo. Quando fornecida,
            define a area disponivel do corpo (ADR-0024 DA-01 a DA-04):
            o descendente visual unico ocupa integralmente essa area
            (DA-01), grupos repassam a area aos filhos (DA-03), e
            composicoes invalidas — multiplos elementos sem distribuicao
            (DA-02) ou area sem elemento visual (DA-04) — sao rejeitadas
            com RenderizadorErro identificavel. Preenchimento externo
            vazio entre cabecalho e barra_de_menus e proibido (ADR-0024).
            Se a altura for insuficiente para cabecalho + barra_de_menus
            ou para o conteudo do corpo, lanca RenderizadorErro.

    Retorna:
        str com a representacao visual no formato definido pelo H-0010A:
        uma caixa de cabecalho derivada de ``modelo.cabecalho``, seguida
        de uma caixa por elemento de ``corpo.elementos[]`` (na ordem do
        JSON) e por fim uma caixa da ``barra_de_menus``. Os caracteres de
        canto variam conforme ``tipo_borda``; o restante (bordas
        vertical/horizontal e conteudo textual) e identico entre
        conjuntos. Cada linha nao-vazia tem exatamente ``largura`` (ou 42
        no fallback) chars Python; a string termina com ``"\\n"``. Quando
        ``altura`` e fornecida e suficiente, a saida tem exatamente
        ``altura`` linhas (``saida.count("\\n") == altura``).

    Lancamentos:
        RenderizadorErro quando:
            - o argumento ``modelo`` nao e um ModeloTela valido;
            - o argumento ``tipo_borda`` nao e ``"curva"`` nem ``"reta"``;
            - algum item de lancador possui ``texto`` acima de 15
              caracteres (rejeitado sem truncamento);
            - ``altura`` e fornecida e e insuficiente para cabecalho +
              barra_de_menus (``L_cab + L_barra > altura``) ou para o
              conteudo do corpo (``L_corpo_conteudo > L_corpo_disponivel``).

    Efeitos colaterais:
        Nenhum. Nao altera o modelo, nao grava arquivo, nao consulta
        JSON em disco, nao executa acao, nao ativa binding, nao
        persiste tipo_borda entre chamadas, nao le o terminal.
    """
    if not isinstance(modelo, ModeloTela):
        raise RenderizadorErro(
            "renderizar_tela exige ModeloTela; recebido: {0}".format(
                type(modelo).__name__
            )
        )

    if tipo_borda not in _BORDAS:
        raise RenderizadorErro(
            "tipo_borda invalido: {0!r}; valores aceitos: curva, reta".format(
                tipo_borda
            )
        )

    # H-0034 / ADR-0023: o sinal de quadro mínimo global é redefinido a cada
    # chamada — o renderer é puro e nunca persiste o estado entre redesenhos
    # (R-14). Se qualquer ``lancador`` da composição sinalizar inviabilidade
    # (``content_w < coluna_minima_content_w``), a tela normal inteira é
    # substituída pelo quadro mínimo canônico (ADR-0017).
    global _quadro_minimo_lancador_ativo
    _quadro_minimo_lancador_ativo = False

    total_w = TOTAL_WIDTH if largura is None else largura
    inner_w = total_w - 2
    content_w = total_w - 3
    label_max = total_w - 4
    borda = _BORDAS[tipo_borda]

    titulo = modelo.cabecalho.get("titulo", "(ausente)")
    descricao = modelo.cabecalho.get("descricao", "(ausente)")
    label_cabecalho = titulo.upper()

    partes = [
        _caixa(
            label_cabecalho, [descricao], borda, inner_w, content_w, label_max
        )
    ]

    # H-0019: normalizar arranjo do corpo (aliases transicionais — ADR-0011).
    # Normalizacao local ao renderer; modelo e loader nao sao alterados.
    arranjo_corpo = modelo.corpo.arranjo
    if arranjo_corpo == "sobreposto":
        arranjo_corpo = "vertical"
    if arranjo_corpo == "lado_a_lado":
        arranjo_corpo = "horizontal"

    # H-0020: linhas_barra inicializada antes do bloco de corpo para permitir
    # pré-computação no modo horizontal com altura (evitar dupla chamada — R-4).
    linhas_barra = None

    # H-0025 / ADR-0018: distribuicao vertical explicita. So ativa quando o
    # container declara ``distribuicao`` (ausencia NAO equivale a ``igual``),
    # o arranjo e vertical (None/sobreposto normalizados inclusive) e uma
    # ``altura`` util foi fornecida. Sem ``altura`` nao ha area distribuivel e
    # o caminho orientado pelo conteudo e tomado integralmente.
    distribuicao_corpo = modelo.corpo.distribuicao
    _corpo_vertical_distribuido = False

    # H-0027 / ADR-0019: composicao recursiva por container. Determina a altura
    # disponivel do corpo antes de renderizar para passar ao container raiz.
    # Ausencia de altura -> composicao orientada pelo conteudo (ADR-0018 D2).
    l_corpo_disponivel = None
    if altura is not None:
        if linhas_barra is None:
            linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
        l_cab = _contar_linhas(partes[0])
        l_barra = len(linhas_barra) + 2
        if l_cab + l_barra > altura:
            raise RenderizadorErro(
                "altura insuficiente: terminal com {0} linhas nao comporta "
                "cabecalho ({1}) + barra_de_menus ({2})".format(
                    altura, l_cab, l_barra
                )
            )
        l_corpo_disponivel = altura - l_cab - l_barra

    bloco_corpo = _renderizar_container(
        arranjo_corpo, distribuicao_corpo,
        modelo.corpo.elementos, borda, total_w, l_corpo_disponivel,
    )
    if bloco_corpo:
        partes.append(bloco_corpo)

    # Corpo absorveu todo o espaco internamente quando: arranjo horizontal
    # (fill por coluna em _renderizar_container_horizontal) ou arranjo
    # vertical com distribuicao e altura fornecidos (fill por cota em
    # _renderizar_container_vertical). Nenhum fill externo e necessario.
    _corpo_vertical_distribuido = (
        arranjo_corpo != "horizontal"
        and distribuicao_corpo is not None
        and l_corpo_disponivel is not None
    )

    # Linhas de conteudo da barra_de_menus, computadas uma vez e reutilizadas
    # tanto para a contagem de L_barra (H-0015) quanto para a caixa final.
    # H-0016: distribuicao horizontal responsiva (ADR-0014) derivada de
    # barra_de_menus.distribuicao + chips[], usando a largura de conteudo
    # disponivel para decidir linha unica vs multilinha vs erro_layout.
    # H-0020 (R-4): pular se já computada no modo horizontal com altura.
    if linhas_barra is None:
        linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)

    # ADR-0024 (H-0033): verificacao pos-renderizacao de ocupacao integral.
    # Quando ``altura`` e fornecida e o arranjo e vertical sem distribuicao,
    # _renderizar_container_vertical ja aplicou DA-01 (unico visual ocupa
    # toda a area) ou lancou DA-02/DA-04. Aqui apenas verificamos que nenhuma
    # area externa ficou descoberta (guarda de seguranca para caminhos
    # nao verticais ou casos distribuidos).
    # Quando ``altura is None``, o corpo usa altura natural e nao ha area
    # residual a verificar.
    if altura is not None:
        l_cab = _contar_linhas(partes[0])
        l_barra = len(linhas_barra) + 2
        l_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])

        if l_cab + l_barra > altura:
            raise RenderizadorErro(
                "altura insuficiente: terminal com {0} linhas nao comporta "
                "cabecalho ({1}) + barra_de_menus ({2})".format(
                    altura, l_cab, l_barra
                )
            )
        l_corpo_disponivel = altura - l_cab - l_barra
        if l_corpo_conteudo > l_corpo_disponivel:
            raise RenderizadorErro(
                "altura insuficiente: corpo requer {0} linhas mas area "
                "disponivel e {1} linhas (altura={2}, cabecalho={3}, "
                "barra={4})".format(
                    l_corpo_conteudo, l_corpo_disponivel,
                    altura, l_cab, l_barra,
                )
            )
        l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
        if l_corpo_fill > 0 and arranjo_corpo != "horizontal" and not _corpo_vertical_distribuido:
            # ADR-0024 DA-04: preenchimento externo vazio e proibido.
            # _renderizar_container_vertical deve ter detectado DA-02/DA-04
            # e lancado RenderizadorErro antes de chegar aqui. Se chegou,
            # e um estado inesperado que tambem viola o invariante.
            raise RenderizadorErro(
                "DA-04 (ADR-0024): preenchimento externo vazio detectado — "
                "{0} linhas nao pertencem a nenhum elemento visual; toda "
                "area do corpo deve pertencer a console, dashboard ou "
                "lancador".format(l_corpo_fill)
            )

    partes.append(_caixa(
        _LABEL_BARRA, linhas_barra,
        borda, inner_w, content_w, label_max,
    ))

    # H-0034 / ADR-0023: se algum ``lancador`` da composição sinalizou
    # inviabilidade (``content_w < coluna_minima_content_w``), a tela normal é
    # integralmente substituída pelo quadro mínimo canônico global
    # (``quadro mínimo de terminal pequeno``, ADR-0017). Cabeçalho, corpo,
    # ``lancador``, dashboards e ``barra_de_menus`` não são exibidos (R-12/R-13).
    # O quadro mínimo reutiliza o mecanismo canônico: aviso textual adequado à
    # largura, sem truncamento, sem overflow, sem mensagem local do ``lancador``.
    if _quadro_minimo_lancador_ativo:
        return _quadro_minimo_global(total_w, altura)

    return "\n".join(partes) + "\n"
