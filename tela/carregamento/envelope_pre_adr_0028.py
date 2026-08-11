"""Compatibilidade do envelope pré-ADR-0028 e escopo D23."""

from tela.carregamento.erros import TelaEstruturaInvalida

_TELAS_LEGADAS_D23 = frozenset({
    # H-0036: cenarios canonicos de conteudo multinivel (tabela, hierarquia,
    # conjuntos_campos). Pre-D23, sem politica declarada, sem chip [V].
    "h0036_console_hierarquia",
    "h0036_console_tabela",
    "h0036_console_conjuntos",
    # H-0035: cenarios de console que adotaram ADR-0025 (distribuicao
    # matricial) e foram adaptados em H-0036 para consumir conteudo externo.
    # Pre-D23, sem politica declarada.
    "h0035_console_com",
    "h0035_console_sem",
})

# Inventario nominal das configuracoes historicas comprovadas que usam a
# variante 2 do envelope pre-ADR-0028 (``regra_geracao_itens`` + 6 campos base,
# sem ``itens``). Essa variante nao tem schema interno fechado para
# ``regra_geracao_itens`` (Resultado B do portao documental); sua aceitacao e
# por compatibilidade restrita com a forma historica comprovada, nao por
# regra geral. Telas novas ou revisadas NAO podem usar ``regra_geracao_itens``
# para evitar D23 (H0037-IMPL-QAPP5-001). A deteccao e estritamente nominal e
# historica — nao vira regra por prefixo nem valha para telas futuras.
# Atualmente: ``demo`` (config/telas/demo/demo.json), cujo ``console_principal``
# declara ``regra_geracao_itens`` + os 6 campos base como rascunho pendente
# (DOC-B008/DOC-B009).
_TELAS_VARIANTE2_LEGADAS = frozenset({"demo"})

# Campos do envelope pre-ADR-0028 de um elemento ``console`` (contrato_json_console.md
# secao 4 / secao 5). A presenca de qualquer um deles indica que o elemento usa o
# envelope classico de console (declaracao direta de ``itens`` com ``origem_dados``,
# politicas de composicao/navegacao/selecao/paginacao/exibicao), e portanto NAO e
# um consumidor de conteudo multinivel externo regido pela ADR-0028. ADR-0028 §6
# limita seu escopo a "dados multinivel exibidos em componentes do tipo console":
# consoles de envelope pre-ADR-0028 estao fora desse escopo e preservam o
# comportamento contratual anterior. A deteccao e estrutural (campos do elemento),
# nao nominal por id de tela, para que valha para qualquer tela futura de envelope.
_CAMPOS_ENVELOPE_PRE_ADR_0028 = frozenset({
    "itens",
    "origem_dados",
    "politica_composicao",
    "politica_navegacao",
    "politica_selecao",
    "politica_paginacao",
    "politica_exibicao",
})

# Campos base do envelope pre-ADR-0028 (excluindo a fonte de itens). O envelope
# classico admite duas variantes mutuamente exclusivas de fonte de itens
# (contrato_console.md §3: "itens OU regra de geracao de itens"), ambas
# combinadas com o mesmo conjunto base de seis campos: origem_dados e as cinco
# politicas (composicao, navegacao, selecao, paginacao, exibicao).
#   - variante 1: ``itens`` + 6 campos base;
#   - variante 2: ``regra_geracao_itens`` + 6 campos base (forma usada por
#     ``console_principal`` de demo.json).
# ``itens`` e ``regra_geracao_itens`` sao duas fontes concorrentes de itens e
# nao podem coexistir. Nao ha schema interno fechado para ``regra_geracao_itens``
# (Resultado B do portao documental), mas a forma historica da variante 2 e
# preservada como tipo estrutural real pre-ADR-0028 (H0037-IMPL-QAPP5-001).
_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 = frozenset({
    "origem_dados",
    "politica_composicao",
    "politica_navegacao",
    "politica_selecao",
    "politica_paginacao",
    "politica_exibicao",
})


_POLITICA_SELECAO_VALIDOS = frozenset({"nenhuma", "unica", "multipla"})
_POLITICA_PAGINACAO_VALIDOS = frozenset({"sem", "com"})
_TIPOS_POLITICA_NAVEGACAO_VALIDOS = frozenset({
    "nivel_unico",
    "tabela",
    "arvore_colapsavel",
    "selecao_multinivel",
    "dois_niveis_por_foco",
})


def _h0055_d23_valido(elemento, id_tela, tem_itens, tem_regra):
    """Reconhece somente o envelope nominal H-0055 com D23.

    H-0055 conserva os campos declarativos do console para reutilizar as
    superfícies vigentes, mas também declara ``formato.excesso`` para D23.
    Essa combinação é válida apenas para a fixture nominal; não altera a
    classificação geral de envelopes híbridos nem introduz vocabulário novo.
    """
    if id_tela != "h0055_dois_niveis_por_foco" or not tem_itens or tem_regra:
        return False
    if elemento.get("itens") != []:
        return False
    origem = elemento.get("origem_dados")
    composicao = elemento.get("politica_composicao")
    navegacao = elemento.get("politica_navegacao")
    formato = elemento.get("formato")
    excesso = formato.get("excesso") if isinstance(formato, dict) else None
    return (
        isinstance(origem, dict)
        and isinstance(composicao, dict)
        and isinstance(navegacao, dict)
        and navegacao.get("navegavel") is True
        and navegacao.get("tipo") == "dois_niveis_por_foco"
        and elemento.get("politica_selecao") == "multipla"
        and elemento.get("politica_paginacao") == "com"
        and isinstance(excesso, dict)
        and excesso.get("politica_modo") == "somente_nao_verboso"
        and "modo_inicial" not in excesso
    )


def _validar_valores_envelope_pre_adr_0028(elemento):
    """Valida os valores dos campos base do envelope pre-ADR-0028.

    Chamada quando o envelope pre-ADR-0028 esta completo (fonte de itens + os 6
    campos base). A validacao depende da variante (H0037-IMPL-QAPP5-001):

      - **variante 1** (``itens`` presente, sem ``regra_geracao_itens``):
        validacao estrita dos tipos/valores canonicos de cada campo
        (contrato_json_console.md secao 4/5): ``itens`` lista, ``origem_dados``
        objeto ou null, ``politica_composicao``/``navegacao``/``exibicao``
        objeto, ``politica_selecao``/``paginacao`` string em vocabulario
        fechado. Vale para qualquer tela.

      - **variante 2** (``regra_geracao_itens`` presente, sem ``itens``):
        aceitacao por compatibilidade restrita com a forma historica comprovada
        (``_TELAS_VARIANTE2_LEGADAS``). Nao ha schema interno fechado para
        ``regra_geracao_itens`` nem para as formas historicas de
        ``politica_paginacao``/``origem_dados`` em rascunho (demo.json usa
        ``politica_paginacao: {paginacao: "com"}`` e ``origem_dados`` como
        objeto pendente). A validacao estrita da variante 1 NAO e reaplicada —
        preserva-se a forma historica sem inventar schema novo. A completude
        estrutural e a exclusividade ja foram garantidas pelo chamador.
    """
    id_elem = elemento.get("id", "?")
    orig = "elemento '{0}'".format(id_elem)

    # Variante 2 (regra_geracao_itens sem itens): compatibilidade restrta com a
    # forma historica. Nao valida tipos escalares — o chamador ja garantiu
    # completude (6 campos base), exclusividade (sem itens) e id_tela legada.
    if "regra_geracao_itens" in elemento and "itens" not in elemento:
        return

    # Variante 1 (itens presente): validacao estrita dos tipos/valores canonicos.
    itens = elemento.get("itens")
    if not isinstance(itens, list):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'itens' deve ser lista; "
            "recebido: {1!r}".format(orig, type(itens).__name__)
        )

    origem_dados = elemento.get("origem_dados")
    if not isinstance(origem_dados, (dict, type(None))):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'origem_dados' deve ser objeto ou "
            "null; recebido: {1!r}".format(orig, type(origem_dados).__name__)
        )

    pol_comp = elemento.get("politica_composicao")
    if not isinstance(pol_comp, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_composicao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_comp).__name__)
        )

    pol_nav = elemento.get("politica_navegacao")
    if not isinstance(pol_nav, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_navegacao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_nav).__name__)
        )

    if "tipo" in pol_nav:
        tipo_navegacao = pol_nav.get("tipo")
        if (not isinstance(tipo_navegacao, str)
                or tipo_navegacao not in _TIPOS_POLITICA_NAVEGACAO_VALIDOS):
            raise TelaEstruturaInvalida(
                "{0}: envelope pre-ADR-0028: 'politica_navegacao.tipo' "
                "deve ser um dos cinco literais {1}; recebido: {2!r}".format(
                    orig,
                    ", ".join(sorted(_TIPOS_POLITICA_NAVEGACAO_VALIDOS)),
                    tipo_navegacao,
                )
            )
        if (tipo_navegacao == "tabela"
                and pol_nav.get("navegavel")):
            raise TelaEstruturaInvalida(
                "{0}: envelope pre-ADR-0028: politica_navegacao.tipo "
                "'tabela' e incompativel com navegavel=true".format(orig)
            )

    pol_sel = elemento.get("politica_selecao")
    if not isinstance(pol_sel, str) or pol_sel not in _POLITICA_SELECAO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_selecao' deve ser uma de "
            "{1}; recebido: {2!r}".format(
                orig, ", ".join(sorted(_POLITICA_SELECAO_VALIDOS)), pol_sel
            )
        )

    pol_pag = elemento.get("politica_paginacao")
    if not isinstance(pol_pag, str) or pol_pag not in _POLITICA_PAGINACAO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_paginacao' deve ser 'sem' "
            "ou 'com'; recebido: {1!r}".format(orig, pol_pag)
        )

    pol_exib = elemento.get("politica_exibicao")
    if not isinstance(pol_exib, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_exibicao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_exib).__name__)
        )


def _console_em_escopo_d23(elemento, id_tela):
    """Determina se um elemento ``console`` esta em escopo D23 (ADR-0028 §6 + D23).

    O escopo de ADR-0028 (e portanto de D23) e "dados multinivel exibidos em
    componentes do tipo console" (ADR-0028 §6), aplicavel exclusivamente a
    instancias que recebem conteudo multinivel externo (``tipo: "multinivel"``)
    — contrato_console.md §21.1. A deteccao e estrutural e independe da presenca
    de ``formato.excesso``.

    DECISAO POR TIPO ESTRUTURAL REAL (H0037-IMPL-QAPP5-001):

    Nao existe schema interno fechado para ``regra_geracao_itens`` nos contratos,
    ADRs ou NOMENCLATURA — apenas a frase "regra de geracao de itens" como
    alternativa contratual a ``itens`` (contrato_console.md §3). O envelope
    pre-ADR-0028 admite duas variantes mutuamente exclusivas de fonte de itens,
    ambas combinadas com o mesmo conjunto base de seis campos
    (``_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028``: origem_dados e as cinco politicas):

      - **variante 1** (classica): ``itens`` + 6 campos base;
      - **variante 2** (geracao interna): ``regra_geracao_itens`` + 6 campos base
        (forma historica usada por ``console_principal`` de demo.json).

    Classificacao estrutural (decide o escopo D23, sem discriminar pela mera
    presenca de ``regra_geracao_itens``):

    - **Envelope pre-ADR-0028 completo** (variante 1 ou 2 com a fonte de itens
      + os 6 campos base presentes): console pre-ADR-0028, FORA do escopo D23.
      Os valores dos campos base sao validados (``_validar_valores_envelope_pre_adr_0028``).
      ``demo.json`` e valido por essa via (variante 2).
    - **Envelope incompleto** (fonte de itens presente mas faltam campos base):
      ``TelaEstruturaInvalida`` — envelope parcial nao e forma historica valida.
    - **Duas fontes concorrentes** (``itens`` E ``regra_geracao_itens``):
      ``TelaEstruturaInvalida`` — sao mutuamente exclusivas (contrato_console.md §3).
    - **Consumidor de conteudo multinivel externo** (0 campos de envelope, sem
      ``regra_geracao_itens``): consumidor puro, DENTRO do escopo D23 (salvo
      legado nominal em ``_TELAS_LEGADAS_D23``).
    - **Hibrido consumidor + regra_geracao_itens** (0 campos de envelope + chave
      ``regra_geracao_itens``): ``TelaEstruturaInvalida`` — geracao interna e
      consumo externo sao mutuamente exclusivos. Qualquer valor sob a chave
      (``{}``, ``null``, tipos incorretos, objetos incompletos) e rejeitado; nao
      ha schema fechado, portanto a chave nunca isenta de D23.
    - **Hibrido envelope + marcadores D23** (envelope pre-ADR-0028 + politica_modo
      /modo_inicial em formato.excesso): ``TelaEstruturaInvalida`` — envelope
      pre-ADR-0028 e consumidor multinivel sao mutuamente exclusivos.

    ``regra_geracao_itens`` nunca concede isencao por mera presenca: ou faz
    parte da variante 2 completa (junto dos 6 campos base) ou e rejeitada como
    incompativel. Nenhum valor sob a chave (incl. ``{}``) serve como bypass.
    """
    campos_base_presentes = _CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 & set(elemento)
    n_base = len(campos_base_presentes)
    n_base_total = len(_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028)
    tem_itens = "itens" in elemento
    tem_regra = "regra_geracao_itens" in elemento
    tem_fonte_itens = tem_itens or tem_regra
    n_fontes = (1 if tem_itens else 0) + (1 if tem_regra else 0)

    _fmt = elemento.get("formato")
    _exc = _fmt.get("excesso") if isinstance(_fmt, dict) else None
    _tem_d23 = isinstance(_exc, dict) and (
        "politica_modo" in _exc or "modo_inicial" in _exc
    )

    # H-0055: a única exceção focal à separação estrutural é a combinação
    # nominal e validada acima. Todas as demais combinações híbridas seguem
    # rejeitadas pelo ramo geral imediatamente abaixo.
    if _tem_d23 and _h0055_d23_valido(
        elemento, id_tela, tem_itens, tem_regra
    ):
        # A fixture nominal H-0055 nao fornece politica_exibicao. Reutiliza a
        # validacao estrita dos demais campos sem transformar essa ausencia
        # historicamente aceita em requisito novo; qualquer valor fornecido
        # para o campo ainda passa pela validacao estrita e rejeita []/tipos
        # invalidos.
        elemento_para_validar = elemento
        if elemento.get("politica_exibicao") is None:
            elemento_para_validar = dict(elemento, politica_exibicao={})
        _validar_valores_envelope_pre_adr_0028(elemento_para_validar)
        return True

    # Hibrido envelope + marcadores D23 de consumidor multinivel. Rejeitado em
    # qualquer cardinalidade de envelope (mesmo um campo base + D23 e
    # incompativel). A mera presenca de envelope classico ou de fonte de itens
    # coloca o elemento fora do escopo de conteudo multinivel externo; misturar
    # com marcadores D23 e estruturalmente invalido (contrato_console.md §21.1).
    if (n_base >= 1 or tem_fonte_itens) and _tem_d23:
        _partes = sorted(campos_base_presentes)
        if tem_itens:
            _partes = ["itens"] + _partes
        if tem_regra:
            _partes = ["regra_geracao_itens"] + _partes
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campos de envelope "
            "pre-ADR-0028 presentes ({1}) coexistindo com marcadores D23 "
            "(politica_modo/modo_inicial em formato.excesso); envelope "
            "pre-ADR-0028 e consumidor multinivel externo sao mutuamente "
            "exclusivos".format(
                elemento.get("id", "?"), ", ".join(_partes),
            )
        )

    # Duas fontes de itens concorrentes (itens E regra_geracao_itens).
    # Mutuamente exclusivas por contrato (contrato_console.md §3).
    if n_fontes == 2:
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campos 'itens' e "
            "'regra_geracao_itens' coexistem como duas fontes concorrentes de "
            "geracao de itens; sao mutuamente exclusivos "
            "(contrato_console.md §3)".format(elemento.get("id", "?"))
        )

    # Hibrido consumidor multinivel + regra_geracao_itens (sem nenhum campo de
    # envelope). Geracao interna e consumo de conteudo externo sao mutuamente
    # exclusivos. Nao ha schema fechado para regra_geracao_itens (Resultado B do
    # portao documental), portanto nenhum valor sob a chave e valido aqui:
    # {}, null, string, lista, bool, numero e objetos incompletos sao todos
    # rejeitados (H0037-IMPL-QAPP5-001).
    if tem_regra and n_base == 0:
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campo "
            "'regra_geracao_itens' (geracao interna de itens, alternativa a "
            "'itens' — contrato_console.md §3) nao pode coexistir com um "
            "consumidor de conteudo multinivel externo (sem campos de envelope "
            "pre-ADR-0028); geracao interna e consumo de conteudo externo sao "
            "mutuamente exclusivos (valor sob a chave ignorado: nao ha schema "
            "fechado)".format(elemento.get("id", "?"))
        )

    # Envelope pre-ADR-0028 com fonte de itens: variantes 1 (itens) ou 2
    # (regra_geracao_itens). As duas exigem os 6 campos base completos.
    if tem_fonte_itens:
        if n_base != n_base_total:
            # Envelope incompleto: fonte de itens presente mas faltam campos
            # base. Nao e forma historica valida nem consumidor multinivel.
            _faltantes = sorted(
                _CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 - campos_base_presentes
            )
            raise TelaEstruturaInvalida(
                "elemento '{0}': envelope pre-ADR-0028 incompleto: fonte de "
                "itens ({1}) presente, mas faltam {2} de {3} campos base "
                "({4}); envelope historico exige origem_dados e as cinco "
                "politicas (composicao, navegacao, selecao, paginacao, "
                "exibicao)".format(
                    elemento.get("id", "?"),
                    "itens" if tem_itens else "regra_geracao_itens",
                    len(_faltantes), n_base_total, ", ".join(_faltantes),
                )
            )
        # Envelope completo (variante 1 ou 2). A validacao de valores depende
        # da variante (H0037-IMPL-QAPP5-001):
        #   - variante 1 (itens): validacao estrita dos tipos/valores canonicos
        #     (contrato_json_console.md secao 4/5); vale para qualquer tela.
        #   - variante 2 (regra_geracao_itens, sem itens): aceitacao por
        #     compatibilidade restrita com a forma historica comprovada
        #     (inventario nominal _TELAS_VARIANTE2_LEGADAS). Nao ha schema
        #     fechado para regra_geracao_itens, portanto os tipos internos nao
        #     sao validados pelos escalares da variante 1 — preserva-se a forma
        #     historica existente. Telas novas/revisadas nao podem usar
        #     regra_geracao_itens para evitar D23.
        if tem_regra and id_tela not in _TELAS_VARIANTE2_LEGADAS:
            raise TelaEstruturaInvalida(
                "elemento '{0}': variante 2 do envelope pre-ADR-0028 "
                "(regra_geracao_itens) nao aceita para tela nova/revisada "
                "'{1}'; regra_geracao_itens nao e schema fechado e telas novas "
                "nao podem usa-lo para evitar D23 (H0037-IMPL-QAPP5-001)".format(
                    elemento.get("id", "?"), id_tela,
                )
            )
        # Valida valores conforme a variante. Variante 1 valida tipos canonicos;
        # variante 2 (legada comprovada) preserva a forma historica sem validar
        # schema interno de regra_geracao_itens.
        _validar_valores_envelope_pre_adr_0028(elemento)
        return False

    if n_base >= 1:
        # Campos base sem fonte de itens: nem envelope completo (variante 1 ou
        # 2) nem consumidor multinivel puro. Estrutura incompleta/invalida.
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompleta: {1} campo(s) de envelope "
            "pre-ADR-0028 ({2}) sem fonte de itens ('itens' ou "
            "'regra_geracao_itens'); nao e envelope historico completo nem "
            "consumidor multinivel".format(
                elemento.get("id", "?"),
                n_base, ", ".join(sorted(campos_base_presentes)),
            )
        )

    # n_base == 0 e sem fonte de itens: consumidor de conteudo multinivel
    # externo puro. Legado nominalmente reconhecido (H-0035/H-0036) e isento;
    # telas novas ou revisadas estao em escopo D23 (ADR-0028 §13.13.3).
    return id_tela not in _TELAS_LEGADAS_D23
