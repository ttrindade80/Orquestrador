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
    Itens com ``texto`` acima de 15 caracteres levantam ``RenderizadorErro``
    -- nunca truncar, nunca abreviar. Lista vazia produz caixa sem linhas
    de conteudo.
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


class RenderizadorErro(Exception):
    """Erro de renderizacao visual de tela."""


TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38

_TEXTO_ITEM_MAX = 15

_PLACEHOLDER_CONSOLE = "(console)"
_LABEL_BARRA = "Menus"

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


def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max):
    """Monta uma caixa bordeada com label no topo e linhas de conteudo."""
    partes = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto, borda, content_w))
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


def _linhas_lancador(elemento):
    """Linhas de conteudo para elemento lancador a partir de itens[].

    Cada item e renderizado como ``"[{chip}] {texto}"``. Itens com
    ``texto`` acima de ``_TEXTO_ITEM_MAX`` (15) caracteres levantam
    ``RenderizadorErro`` -- nunca truncar, nunca abreviar. Lista vazia
    produz caixa sem linhas de conteudo.
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    linhas = []
    for item in itens:
        if not isinstance(item, dict):
            continue
        chip = item.get("chip", "")
        texto = item.get("texto", "")
        if len(texto) > _TEXTO_ITEM_MAX:
            raise RenderizadorErro(
                "texto de item de lancador acima do limite de {0} "
                "caracteres: {1!r} (id={2!r})".format(
                    _TEXTO_ITEM_MAX, texto, item.get("id")
                )
            )
        linhas.append("[{0}] {1}".format(chip, texto))
    return linhas


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


def _caixa_de_elemento(elemento, borda, inner_w, content_w, label_max):
    """Despacha um elemento funcional para sua caixa bordeada.

    Retorna a string da caixa do elemento (console/dashboard/lancador) ou
    ``None`` quando o tipo nao e funcional. Usado tanto para elementos
    diretos de ``corpo.elementos[]`` (lista plana) quanto para os elementos
    funcionais internos de um grupo estrutural (H-0012) -- o despacho e
    identico nos dois casos.
    """
    if elemento.tipo == "console":
        titulo_el = elemento._campos_inertes.get("titulo", "CONSOLE")
        return _caixa(
            titulo_el.upper(), _linhas_console(elemento),
            borda, inner_w, content_w, label_max,
        )
    if elemento.tipo == "dashboard":
        titulo_el = elemento._campos_inertes.get("titulo", "DASHBOARD")
        return _caixa(
            titulo_el.upper(), _linhas_dashboard(elemento),
            borda, inner_w, content_w, label_max,
        )
    if elemento.tipo == "lancador":
        titulo_el = elemento._campos_inertes.get("titulo", "LANCADOR")
        return _caixa(
            titulo_el.upper(), _linhas_lancador(elemento),
            borda, inner_w, content_w, label_max,
        )
    return None


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
            (default), o comportamento atual e preservado integralmente:
            nenhuma linha de preenchimento e inserida e a saida tem apenas
            as linhas das caixas (cabecalho + corpo + barra_de_menus).
            Quando fornecida (H-0015 / ADR-0013 -- ocupacao vertical da
            janela do terminal pelo corpo), o renderer preenche a area do
            corpo entre o cabecalho e a barra_de_menus com linhas fisicas
            de ``largura`` espacos ate que a saida tenha exatamente
            ``altura`` linhas. Esse preenchimento nao vem do JSON e nao e
            novo arranjo nem novo elemento do corpo. Se a altura for
            insuficiente para cabecalho + barra_de_menus ou para o
            conteudo do corpo, lancar RenderizadorErro (sem truncamento
            silencioso). ``altura`` interage apenas com o eixo vertical;
            ``corpo.arranjo = "vertical"`` (composicao, ADR-0011) nao e
            reinterpretado.

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

    for elemento in modelo.corpo.elementos:
        if elemento.tipo == "grupo":
            # Grupo estrutural (H-0012): container sem caixa visual propria.
            # Percorre os elementos funcionais internos e os renderiza com o
            # mesmo despacho da lista plana, sem borda/titulo/linha extra.
            for interno in elemento.elementos:
                caixa = _caixa_de_elemento(
                    interno, borda, inner_w, content_w, label_max
                )
                if caixa is not None:
                    partes.append(caixa)
        else:
            caixa = _caixa_de_elemento(
                elemento, borda, inner_w, content_w, label_max
            )
            if caixa is not None:
                partes.append(caixa)

    # Linhas de conteudo da barra_de_menus, computadas uma vez e reutilizadas
    # tanto para a contagem de L_barra (H-0015) quanto para a caixa final.
    # H-0016: distribuicao horizontal responsiva (ADR-0014) derivada de
    # barra_de_menus.distribuicao + chips[], usando a largura de conteudo
    # disponivel para decidir linha unica vs multilinha vs erro_layout.
    linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)

    # H-0015 / ADR-0013: ocupacao vertical da janela do terminal pelo corpo.
    # Quando ``altura`` e fornecida, preenche a area do corpo entre o
    # cabecalho e a barra_de_menus com linhas fisicas de ``total_w`` espacos
    # ate que a saida tenha exatamente ``altura`` linhas. O preenchimento e
    # responsabilidade do renderer (nao do JSON), nao e novo arranjo nem novo
    # elemento do corpo e nao reinterpreta ``corpo.arranjo = "vertical"``.
    # Quando ``altura is None``, nenhum preenchimento e inserido e o caminho
    # atual (comportamento anterior) e tomado integralmente.
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
        if l_corpo_fill > 0:
            # Linhas fisicas de preenchimento, cada uma com exatamente
            # ``total_w`` espacos, inseridas apos o ultimo box de elemento
            # do corpo e antes do box da barra_de_menus. Preserva os
            # invariantes: cada linha nao-vazia tem ``total_w`` chars e a
            # saida nao contem "\n\n".
            partes.append(
                "\n".join(" " * total_w for _ in range(l_corpo_fill))
            )

    partes.append(_caixa(
        _LABEL_BARRA, linhas_barra,
        borda, inner_w, content_w, label_max,
    ))

    return "\n".join(partes) + "\n"
