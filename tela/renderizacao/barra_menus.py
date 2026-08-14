"""Renderização da barra de menus."""

from tela.renderizacao.contexto_execucao import (
    DESCONTO_ESTRUTURAL_CONSOLE,
    _algum_console_paginado_no_corpo,
    _console_declarou_selecao_multipla,
    _console_tem_paginacao,
    _itens_navegaveis_do_elemento,
    _navegacao_atual,
    _pagina_atual_de_contexto,
)
from tela.controle_execucao import ControleExecucaoRepresentacao
from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.texto_ansi import (
    _ANSI_POR_NOME_SEMANTICO,
    _cortar_sem_ansi,
    _largura_sem_ansi,
    _ljust_sem_ansi,
)
from tela.renderizacao.estilo import (
    compor_chip_multitecla,
)

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

def _avaliar_regra_ativo(
    regra, *, selecao_vazia=None, item_focalizado_selecionavel=None,
    executar_disponivel=None, pagina_nao_e_primeira=None,
    pagina_nao_e_ultima=None, candidato_divergente=None,
):
    """Avalia ``regra_ativo`` do chip e devolve o estado logico ATIVO.

    QA-H0041-002 (P02): o estado ATIVO/INATIVO e propriedade distinta do
    rotulo. Esta funcao consome a regra declarada no JSON; nao infere
    inatividade a partir do texto (``Todos``/``Executar``).

    Valores reconhecidos (convencao paralela a ``regra_existencia``):

    - ``None`` / ``"sempre"``: sempre ATIVO (comportamento pre-existente);
    - ``"selecao_vazia"``: ATIVO somente quando a selecao reconciliada do
      console focado esta vazia (chip Enter=Todos); INATIVO com selecao
      (chip Enter=Executar, D-SEL-07/D-SEL-21). H-0044: quando
      ``executar_disponivel`` nao e ``None``, selecao nao vazia fica ATIVA
      somente se ``executar_disponivel`` for verdadeiro (ativacao cumulativa
      de Executar); ``None`` preserva o comportamento H-0041.
    - ``"item_focalizado_selecionavel"``: ATIVO somente quando o item sob
      cursor no console focado e selecionavel (chip Espaco=Marcar,
      D-SEL-05/D-SEL-09); INATIVO quando o item sob cursor nao e
      selecionavel. H0041-MANUAL-001: o comando ``Espaco`` corretamente
      ignora itens nao selecionaveis, mas a barra deve apresentar a
      indisponibilidade — nao basta o comando nao produzir efeito.

    Sem contexto de selecao (``selecao_vazia is None``) ou sem item
    focalizado (``item_focalizado_selecionavel is None``), regras
    dependentes nao forcam inativo — preserva consoles/barras sem selecao
    multipla. Regras desconhecidas nao restringem (ATIVO), para nao inventar
    politica nova.
    """
    if regra is None or regra == "sempre":
        return True
    if regra == "selecao_vazia":
        if selecao_vazia is None:
            return True
        if selecao_vazia:
            return True
        # Selecao nao vazia -> rotulo Executar.
        if executar_disponivel is not None:
            return bool(executar_disponivel)
        return False
    if regra == "item_focalizado_selecionavel":
        if item_focalizado_selecionavel is None:
            return True
        return bool(item_focalizado_selecionavel)
    if regra == "pagina_nao_e_primeira":
        if pagina_nao_e_primeira is None:
            return True
        return bool(pagina_nao_e_primeira)
    if regra == "pagina_nao_e_ultima":
        if pagina_nao_e_ultima is None:
            return True
        return bool(pagina_nao_e_ultima)
    if regra == "candidato_divergente":
        if candidato_divergente is None:
            return True
        return bool(candidato_divergente)
    return True


def _texto_chip_barra(
    chip, estilo, vao=1, inativo=False, destacado=False,
    aplicar_estilo=False,
):
    """Monta o texto de um chip com estilo contido na unidade visual.

    H-0039 / ADR-0030 D5: os delimitadores e a capitalizacao do rotulo vêm do
    ``EstiloResolvido`` (``caractere_esquerdo``, ``caractere_direito``,
    ``caixa_alta``), nunca hardcoded. ``caixa_alta`` aplica-se apenas ao
    rotulo (``texto``) -- a tecla permanece como declarada no JSON, para nao
    quebrar identificadores como ``Esc``. ``cor_texto``/``cor_fundo`` sao
    lidos do estilo pela composicao compartilhada. O padding e o texto
    descritivo ficam fora da unidade visual estilizada.

    H-0041 P04: quando ``inativo=True``, o chip recebe ``estilo.cor_inativo``
    (nome semantico resolvido pelo loader a partir de ``config/estilo.json``),
    traduzido pela paleta canônica do renderer (R-7). A capitalizacao normal
    do rotulo e preservada — caixa baixa como indicacao de inatividade e
    proibida. A sequencia de cor e delimitada e seguida de restauracao do
    foreground (``_ANSI_RESET_FG``), sem vazar para o texto descritivo ou
    chips posteriores.
    O estado logico continua vindo de ``regra_ativo`` / ``estado_ativo_chips``,
    nunca inferido pelo rotulo. Consoles sem selecao multipla preservam o
    comportamento anterior (``inativo`` default ``False``).

    H-0044 / ADR-0037: quando ``destacado=True`` e o chip nao esta inativo,
    aplica ``estilo.cor_alerta`` ao texto integral do chip. Destaque nao
    implica inatividade. O conjunto de chips destacados e resolvido pelo
    chamador — o renderer nao decide dry-run nem hardcoda IDs de chip.
    """
    tecla = chip.get("tecla", "")
    texto = chip.get("texto", "")
    if estilo.caixa_alta:
        texto = texto.upper()
    visual = compor_chip_multitecla(
        [tecla], estilo, estados=(inativo,), destaques=(destacado,)
    )
    return "{0}{1}{2}".format(visual, " " * vao, texto)


def _conteudo_chip_multitecla(
    teclas, estilo, familia, estados, destaques
):
    """Compatibilidade interna para a composição compartilhada."""
    return compor_chip_multitecla(
        teclas, estilo, estados=estados, destaques=destaques
    )


def _texto_chip_multitecla(
    anterior, proxima, estilo, vao, estados, destaques
):
    """Monta o par de paginação como uma unidade visual única."""
    texto = proxima.get("texto", "")
    if estilo.caixa_alta:
        texto = texto.upper()
    chip = _conteudo_chip_multitecla(
        [anterior.get("tecla", ""), proxima.get("tecla", "")],
        estilo,
        None,
        estados,
        destaques,
    )
    return "{0}{1}{2}".format(chip, " " * vao, texto)


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
    larguras = [max(_largura_sem_ansi(s) for s in col) for col in colunas]
    sep = " " * vao_entre_colunas
    linhas = []
    for r in range(n_linhas):
        partes = []
        for c in range(n_colunas):
            if r < len(colunas[c]):
                partes.append(_ljust_sem_ansi(colunas[c][r], larguras[c]))
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


def _garantir_esc_primeiro(chips):
    """Garante que o chip ``[Esc]`` ocupe a primeira posição (H0037-MANUAL-002).

    Regra contratual central (contrato_barra_de_menus.md §8.2): ``[Esc]`` é
    sempre o primeiro chip quando declarado. A ordenação é aplicada nesta
    camada central — origem única da ordem da barra — valendo para qualquer
    tela, sem condição específica por ID de tela, JSON ou cenário.

    Comportamento:
    - nenhum chip ``Esc`` declarado: lista retornada sem alteração;
    - chip ``Esc`` declarado (tecla ``"Esc"``): movido para a primeira
      posição; os demais chips preservam a ordem relativa entre si;
    - ausência de duplicação: somente o primeiro ``Esc`` encontrado é
      promovido (teclas duplicadas já são rejeitadas em outro ponto do
      contrato para a mesma instância).

    Não muta a lista recebida. Não inventa chip ``Esc`` em telas que não o
    declaram. Não altera texto, tecla nem função dos demais chips.
    """
    esc = None
    demais = []
    for chip in chips:
        if esc is None and isinstance(chip, dict) and chip.get("tecla") == "Esc":
            esc = chip
        else:
            demais.append(chip)
    if esc is None:
        return list(chips)
    return [esc] + demais


def _posicionar_controle_execucao_apos_enter(chips):
    """Mantem o chip de execucao imediatamente depois do chip Enter."""
    indice_controle = next(
        (
            i for i, chip in enumerate(chips)
            if chip.get("forma_exibicao") == "controle_execucao"
        ),
        None,
    )
    if indice_controle is None:
        return list(chips)

    controle = chips[indice_controle]
    restantes = list(chips[:indice_controle]) + list(chips[indice_controle + 1:])
    indice_enter = next(
        (
            i for i, chip in enumerate(restantes)
            if chip.get("forma_exibicao") == "rotulo_dinamico_selecao"
            or chip.get("tecla") in ("Enter", "⏎")
        ),
        None,
    )
    if indice_enter is None:
        return list(chips)
    restantes.insert(indice_enter + 1, controle)
    return restantes


def _linhas_barra(barra_de_menus, estilo, content_w, controle_execucao=None):
    """Linhas de conteudo para a caixa da barra de menus (H-0016).

    Renderiza os chips da ``barra_de_menus`` em distribuição horizontal
    responsiva (ADR-0014), a partir de ``barra_de_menus.distribuicao`` e
    ``barra_de_menus.chips[]``:

    1. normaliza ``distribuicao`` (alias string ``"horizontal"``/ausente ->
       defaults normativos; objeto canônico -> usado como declarado);
    2. valida defensivamente a declaração e as âncoras (restrição, nunca
       reordenação);
    3. aplica a regra contratual ``[Esc]`` primeiro (contrato_barra_de_menus.md
       §8.2: ``[Esc]`` é o primeiro chip quando declarado) — qualquer chip
       cuja ``tecla`` seja ``"Esc"`` é movido para a primeira posição,
       preservando a ordem relativa dos demais chips. Não duplica, não
       inventa ``[Esc]`` em telas que não o declaram;
    4. tenta linha única; se couber em ``content_w``, retorna uma linha;
    5. caso contrário, tenta multilinha de 2 até ``linhas.maximo`` linhas,
       aplicando ``preenchimento_multilinha`` (``coluna_a_coluna`` ou
       ``linha_a_linha``); retorna na primeira configuração que encaixar;
    6. se nenhuma configuração couber, levanta ``RenderizadorErro``
       (``overflow.quando_nao_couber = "erro_layout"``) -- nunca omite,
       nunca trunca, nunca reordena chips além da regra contratual ``[Esc]``.

    Cada chip é renderizado como ``"{ec}{tecla}{ed} {texto}"``, onde os
    delimitadores e a capitalização do rótulo vêm do ``EstiloResolvido``
    (H-0039 / ADR-0030 D5). ``regra_existencia`` é avaliada para os chips
    dinâmicos de navegação (H-0040) e seleção múltipla (H-0041); o rótulo
    dinâmico ``Todos``/``Executar`` do chip ``[Enter]`` é materializado quando
    a forma de exibição ``rotulo_dinamico_selecao`` está declarada (H-0041).
    ``regra_ativo`` é avaliada por chip (QA-H0041-002 / P02): o estado lógico
    ATIVO/INATIVO é independente do rótulo apresentado.

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

    # H-0050: a barra apenas materializa a representação fornecida pelo
    # controle por instância. A elegibilidade e a transição pertencem ao
    # controle/registro; nenhum modo é inferido de ID, texto ou comportamento.
    representacao = controle_execucao
    if representacao is None:
        candidato = _navegacao_atual.get("executar_disponivel")
        if isinstance(candidato, ControleExecucaoRepresentacao):
            representacao = candidato
    if isinstance(representacao, ControleExecucaoRepresentacao):
        chips = [
            (
                dict(chip, tecla="Ins", texto=representacao.rotulo)
                if chip.get("forma_exibicao") == "controle_execucao"
                and chip.get("id") == representacao.chip_id
                else chip
            )
            for chip in chips
        ]

    # H-0040 / ADR-0031 D14: regras dinamicas de existencia dos chips de
    # navegacao ``[⇆]`` (alternancia de foco) e ``[✥]`` (navegacao por setas).
    # A regra_existencia e campo ja contratado (NC-004; mudanca_de_schema: false).
    # ``[⇆]`` aparece somente quando a tela tem >= 2 consoles focalizaveis;
    # ``[✥]`` aparece somente quando o console focado tem > 1 item navegavel.
    # Nao existe estado inativo para ``[✥]``: ou esta presente, ou ausente
    # (regra_existencia exclusiva).
    lista = _navegacao_atual.get("lista_foco")
    # H-0041: ``rotulo_enter`` e definido apenas quando o contexto de navegacao
    # esta ativo e o console focado declara selecao multipla; ``None`` caso
    # contrario (preserva o comportamento pre-H-0041 para a barra de menus).
    rotulo_enter = None
    # QA-H0041-002 (P02): contexto para ``regra_ativo`` (independente do rotulo).
    # ``None`` = sem contexto de selecao multipla (nao forca inativo).
    selecao_vazia = None
    # H0041-MANUAL-001 (P03): selecionabilidade do item sob cursor no console
    # focado (contexto para ``regra_ativo: item_focalizado_selecionavel`` do
    # chip Espaco). ``None`` = sem console focado/selecao multipla (nao forca
    # inativo). Reaproveita ``tela.selecao.chip_espaco_ativo``, que resolve o
    # item corrente via ``tela.navegacao`` sem acoplamento por import direto.
    item_focalizado_selecionavel = None
    console_tem_paginacao = False
    pagina_nao_e_primeira = None
    pagina_nao_e_ultima = None
    # VM-H0045-R06-001 (P21): console focado e acessivel tambem fora do bloco
    # de selecao multipla para resolver o rotulo dinamico do chip ``[Esc]``.
    # Inicializado aqui (antes do bloco ``if lista is not None``) para que a
    # materializacao do ``rotulo_dinamico_esc`` funcione mesmo quando o
    # contexto de navegacao esta inativo (``lista is None`` => ``None`` =>
    # nenhum chip Esc e alterado, preservando o rotulo original).
    console_foco = None
    if lista is not None:
        # D-TEC-12 / H-0045-P01 / VM-H0045-R07-003: existencia de ``[<]``/
        # ``[>]`` e propriedade ESTATICA de qualquer console do corpo que
        # declara ``politica_paginacao: "com"`` (contrato_console.md §12:
        # "existem quando a instancia declara paginacao: com"), nao
        # condicionada a foco corrente NEM a focalizabilidade (ADR-0031 D2 —
        # um console paginado com zero itens navegaveis nunca entra em
        # ``lista_foco``, mas ainda declara paginacao "com" e deve exibir os
        # chips INATIVOS, nunca omiti-los). Fonte: ``existe_console_paginado``
        # (``_algum_console_paginado_no_corpo``, travessia do corpo inteiro),
        # nao ``lista`` (apenas consoles focalizaveis).
        console_tem_paginacao = bool(_navegacao_atual.get("existe_console_paginado"))
        tem_alternar = len(lista) >= 2
        foco = _navegacao_atual.get("foco_console")
        tem_navegar = False
        if lista and foco is not None and 0 <= foco < len(lista):
            console_foco = lista[foco]
            if _console_tem_paginacao(console_foco):
                from tela import paginacao

                largura = _navegacao_atual.get("largura") or 80
                altura_interna = _navegacao_atual.get("altura_interna") or max(1, 24 - 8)
                total = paginacao.total_paginas(
                    console_foco,
                    largura,
                    altura_interna,
                    bool(_navegacao_atual.get("verboso")),
                    desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
                )
                pagina_ctx = _pagina_atual_de_contexto(console_foco)
                pagina_nao_e_primeira = pagina_ctx > 1
                pagina_nao_e_ultima = pagina_ctx < total
                tem_navegar = (
                    len(
                        paginacao.linhas_logicas_navegaveis_da_pagina(
                            {
                                "pagina_atual": _navegacao_atual.get("paginas_atuais") or {},
                                "largura": largura,
                                "altura_interna": altura_interna,
                                "modo_verboso": bool(_navegacao_atual.get("verboso")),
                                "desconto_estrutural": DESCONTO_ESTRUTURAL_CONSOLE,
                            },
                            console_foco,
                        )
                    )
                    > 1
                )
            else:
                tem_navegar = len(_itens_navegaveis_do_elemento(console_foco)) > 1
                if console_tem_paginacao:
                    pagina_nao_e_primeira = False
                    pagina_nao_e_ultima = False
        elif console_tem_paginacao:
            pagina_nao_e_primeira = False
            pagina_nao_e_ultima = False
        # H-0041 / ADR-0034 D-SEL-09: regras dinamicas dos chips ``[Espaço]``
        # e ``[Enter]``. ``[Espaço]`` existe quando o console focado declara
        # selecao multipla (``regra_existencia: console_focado_com_selecao_multipla``).
        # ``[Enter]`` existe com a mesma condicao; seu rotulo e dinamico:
        # ``Todos`` quando a selecao esta vazia, ``Executar`` quando ha
        # selecao. O estado logico ATIVO/INATIVO vem de ``regra_ativo``
        # (ex.: ``selecao_vazia``), nao do texto do rotulo.
        tem_selecao_multipla = (
            console_foco is not None
            and _console_declarou_selecao_multipla(console_foco)
        )
        if tem_selecao_multipla and console_foco is not None:
            from tela import selecao as _sel_mod
            from tela import navegacao as _nav_mod
            estado_sel = {
                "selecoes": _navegacao_atual.get("selecoes") or {},
                "cursores": _navegacao_atual.get("cursores") or {},
            }
            rotulo_enter = _sel_mod.rotulo_enter(estado_sel, console_foco)
            selecao_vazia = _sel_mod.esta_vazia(estado_sel, console_foco)
            # H0041-MANUAL-001: o chip Espaco deve refletir a selecionabilidade
            # do item sob cursor (D-SEL-09), recalculada a cada movimento.
            item_focalizado_selecionavel = _sel_mod.chip_espaco_ativo(
                console_foco, estado_sel, _nav_mod
            )
        filtrados = []
        for chip in chips:
            regra = chip.get("regra_existencia")
            if regra == "tela_com_pelo_menos_dois_consoles_focalizaveis":
                if tem_alternar:
                    filtrados.append(chip)
                continue
            if regra == "console_focado_com_mais_de_um_item_navegavel":
                if tem_navegar:
                    filtrados.append(chip)
                continue
            if regra == "console_focado_com_selecao_multipla":
                if tem_selecao_multipla:
                    filtrados.append(chip)
                continue
            if regra == "console_com_paginacao":
                if console_tem_paginacao:
                    filtrados.append(chip)
                continue
            filtrados.append(chip)
        chips = filtrados

    # H-0041: materializa o rotulo dinamico ``Todos``/``Executar`` do chip
    # ``[Enter]``. ``forma_exibicao: "rotulo_dinamico_selecao"`` ja e campo
    # contratado (presente em fixtures H-0029/H-0030 para rotulos dinamicos de
    # dashboard); o renderer apenas decide o valor quando a regra de existencia
    # manteve o chip. O rotulo e independente do estado logico ATIVO/INATIVO.
    if rotulo_enter is not None:
        chips = [
            (dict(c, texto=rotulo_enter)
             if c.get("forma_exibicao") == "rotulo_dinamico_selecao"
             else c)
            for c in chips
        ]

    # VM-H0045-R06-001 (P21): materializa o rotulo dinamico ``Limpar``/original
    # do chip ``[Esc]``. Reutiliza o MESMO mecanismo contratado de
    # ``forma_exibicao`` (nenhum campo novo): quando a instancia declara
    # ``forma_exibicao: "rotulo_dinamico_esc"``, o renderer resolve o texto do
    # chip Esc via ``tela.selecao.rotulo_esc`` a partir do console FOCADO e do
    # rotulo original configurado (Sair, Voltar ou outro rotulo valido).
    # Devolve ``Limpar`` quando o console focado declara selecao multipla e
    # possui selecao reconciliada NAO VAZIA; o rotulo original em todos os
    # demais casos (console sem selecao multipla, selecao vazia, sem console
    # focado, ou chip que nao usa a nova forma de exibicao).
    #
    # Isolamento por console focal: somente a selecao do console focado
    # determina o rotulo (D-SEL-01/03). Configuracoes de selecao unica nao
    # declaram ``rotulo_dinamico_esc`` e permanecem com o chip original. O
    # texto substituido e SOMENTE o exibido: tecla, ordem, atividade, cores e
    # demais propriedades do chip sao preservados. O comportamento funcional
    # de Esc (limpar selecao e manter a tela aberta) ja existe em
    # ``demo/demo.py`` e nao e alterado por este patch.
    if any(
        c.get("tecla") == "Esc"
        and c.get("forma_exibicao") == "rotulo_dinamico_esc"
        for c in chips
    ):
        from tela import selecao as _sel_mod_esc

        estado_sel_esc = {
            "selecoes": _navegacao_atual.get("selecoes") or {},
            "cursores": _navegacao_atual.get("cursores") or {},
        }
        chips = [
            (dict(
                c,
                texto=_sel_mod_esc.rotulo_esc(
                    estado_sel_esc, console_foco, c.get("texto")
                ),
            )
             if c.get("tecla") == "Esc"
             and c.get("forma_exibicao") == "rotulo_dinamico_esc"
             else c)
            for c in chips
        ]

    # QA-H0041-002 (P02): avalia ``regra_ativo`` por chip. O estado logico e
    # materializado em ``_navegacao_atual["estado_ativo_chips"]`` para consulta
    # pelos testes; a representacao visual inativa (cor_inativo) e apenas
    # consequencia desse estado — nunca deriva de ``rotulo_enter == "Executar"``.
    # H0041-MANUAL-001 (P03): ``item_focalizado_selecionavel`` e repassado para
    # que ``regra_ativo: item_focalizado_selecionavel`` (chip Espaco) reflita a
    # selecionabilidade do item sob cursor, recalculada a cada movimento.
    estado_ativo_chips = {}
    executar_disponivel = _navegacao_atual.get("executar_disponivel")
    candidato_divergente = _navegacao_atual.get("aplicar_disponivel")
    for c in chips:
        chip_id = c.get("id")
        ativo = _avaliar_regra_ativo(
            c.get("regra_ativo"),
            selecao_vazia=selecao_vazia,
            item_focalizado_selecionavel=item_focalizado_selecionavel,
            executar_disponivel=executar_disponivel,
            pagina_nao_e_primeira=pagina_nao_e_primeira,
            pagina_nao_e_ultima=pagina_nao_e_ultima,
            candidato_divergente=candidato_divergente,
        )
        if chip_id is not None:
            estado_ativo_chips[chip_id] = ativo
    _navegacao_atual["estado_ativo_chips"] = estado_ativo_chips

    distribuicao = _normalizar_distribuicao(
        barra_de_menus.get("distribuicao")
    )
    _validar_distribuicao(distribuicao)
    _validar_ancoras(chips, distribuicao)

    # H0037-MANUAL-002: regra contratual central — ``[Esc]`` é sempre o
    # primeiro chip quando declarado (contrato_barra_de_menus.md §8.2).
    # A aplicação é centralizada na origem da ordenação da barra, valendo
    # para qualquer tela, sem condição específica por ID/JSON/cenário.
    chips = _garantir_esc_primeiro(chips)
    chips = _posicionar_controle_execucao_apos_enter(chips)

    esp = distribuicao.get("espacamentos") or {}
    vao_ct = (esp.get("vao_chip_texto") or {}).get("minimo", 1)
    margem = (esp.get("margem_horizontal") or {}).get("minimo", 0)
    vao_entre_chips = (esp.get("vao_entre_chips") or {}).get("minimo", 2)
    vao_entre_colunas = (esp.get("vao_entre_colunas") or {}).get("minimo", 2)

    chips_destacados = set(
        _navegacao_atual.get("chips_destacados") or frozenset()
    )
    if (
        isinstance(representacao, ControleExecucaoRepresentacao)
        and representacao.destacado
    ):
        chips_destacados.add(representacao.chip_id)
    # H-0051 / D-PGU-01 a D-PGU-03: agrupamento focal exclusivo de
    # ``chip_pagina_anterior`` + ``chip_pagina_proxima`` (contiguos na
    # ordem declarada). Todos os presets formam uma unidade visual multitecla
    # com separador estrutural ``/``.
    # Cada chip preserva id, regra_existencia e regra_ativo proprios
    # (avaliados acima, em ``estado_ativo_chips``); nenhum outro par de chips
    # e afetado.
    texto_chips = []
    pular_proximo = False
    for idx, c in enumerate(chips):
        if pular_proximo:
            pular_proximo = False
            continue
        chip_id = c.get("id")
        proximo = chips[idx + 1] if idx + 1 < len(chips) else None
        if (
            chip_id == "chip_pagina_anterior"
            and proximo is not None
            and proximo.get("id") == "chip_pagina_proxima"
        ):
            prox_id = proximo.get("id")
            texto_chips.append(
                _texto_chip_multitecla(
                    c,
                    proximo,
                    estilo,
                    vao_ct,
                    (
                        not estado_ativo_chips.get(chip_id, True),
                        not estado_ativo_chips.get(prox_id, True),
                    ),
                    (
                        chip_id in chips_destacados,
                        prox_id in chips_destacados,
                    ),
                )
            )
            pular_proximo = True
            continue
        texto_chips.append(
            _texto_chip_barra(
                c, estilo, vao=vao_ct,
                # Estado visual inativo = consequencia de regra_ativo == False.
                inativo=not estado_ativo_chips.get(chip_id, True),
                destacado=(chip_id in chips_destacados),
            )
        )
    prefixo = " " * margem
    largura_util = content_w - 2 * margem

    linhas_cfg = distribuicao.get("linhas") or {}
    minimo = linhas_cfg.get("minimo", 1)
    maximo = linhas_cfg.get("maximo", 2)
    preenchimento = distribuicao.get("preenchimento_multilinha", "coluna_a_coluna")

    sep_chips = " " * vao_entre_chips
    linha_unica = sep_chips.join(texto_chips)
    if (
        minimo <= 1
        and largura_util >= 0
        and _largura_sem_ansi(linha_unica) <= largura_util
    ):
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
        if (
            linhas
            and largura_util >= 0
            and max(_largura_sem_ansi(l) for l in linhas) <= largura_util
        ):
            return [prefixo + l for l in linhas]

    raise RenderizadorErro(
        "erro_layout: chips da barra_de_menus ({0}) nao cabem em {1} "
        "caracteres uteis (content_w={2}, margem={3}) com no maximo {4} linhas "
        "(preenchimento={5}); overflow.quando_nao_couber='erro_layout' proibe "
        "omitir/truncar/reordenar".format(
            len(texto_chips), largura_util, content_w, margem, maximo, preenchimento
        )
    )
