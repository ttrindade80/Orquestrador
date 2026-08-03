"""Estado de execução e contexto compartilhado do renderizador."""



_quadro_minimo_lancador_ativo = False


def _ativar_quadro_minimo_lancador():
    global _quadro_minimo_lancador_ativo
    _quadro_minimo_lancador_ativo = True


def _quadro_minimo_lancador_esta_ativo():
    return _quadro_minimo_lancador_ativo


def _reiniciar_quadro_minimo_lancador():
    global _quadro_minimo_lancador_ativo
    _quadro_minimo_lancador_ativo = False

# H-0040 / ADR-0031: contexto de navegação de runtime repassado por
# ``renderizar_tela`` aos helpers de console e barra_de_menus. Os dados são
# EXCLUSIVAMENTE de runtime (foco_console, cursores, lista_foco, largura,
# símbolos do estilo); nunca persistem em JSON. O renderer é puro: o contexto
# é redefinido no início de cada ``renderizar_tela`` e nunca persiste entre
# chamadas (R-14), seguindo o mesmo padrão de ``_quadro_minimo_lancador_ativo``.
# ``None`` em todos os campos preserva o comportamento pré-H-0040 (sem
# indicador, sem chips dinâmicos).
_navegacao_atual = {
    "lista_foco": None,        # lista de ElementoCorpo focalizaveis
    "foco_console": None,      # indice do console focado na lista_foco
    "cursores": {},            # dict id-do-console -> item logico corrente
    "largura": None,           # largura vigente para a grade de navegacao
    "simbolo": None,           # estilo.selecionado_simbolo
    "off": None,               # estilo.selecionado_off
    # H-0041 / ADR-0034: estado de selecao multipla (runtime, por console) e
    # simbolos do indicador de inclusao (``tg``), paralelos aos de cursor
    # (``ec``). ``selecoes`` mapeia id-do-console -> lista de IDs marcados.
    # ``inc_on``/``inc_off`` derivam de ``estilo.incluido_on/off`` (ja
    # resolvidos pelo loader). ``None`` preserva o comportamento pre-H-0041.
    "selecoes": {},            # dict id-do-console -> [ids marcados]
    "inc_on": None,            # estilo.incluido_on
    "inc_off": None,           # estilo.incluido_off
    # QA-H0041-002 (P02): estado logico ATIVO/INATIVO por chip, derivado da
    # avaliacao de ``regra_ativo`` (independente do rotulo apresentado).
    # Preenchido em ``_linhas_barra``; consultavel por testes apos render.
    "estado_ativo_chips": {},  # dict id-do-chip -> bool (True=ATIVO)
    # H-0044 / ADR-0037: conjunto de IDs de chips ja resolvidos pelo chamador
    # para receber ``cor_alerta`` (destaque). O renderer nao decide dry-run.
    "chips_destacados": frozenset(),
    # Quando nao-None, altera a avaliacao de ``selecao_vazia`` para Executar
    # (H-0044): selecao nao vazia fica ativa somente se True. None preserva
    # H-0041 (Executar inativo).
    "executar_disponivel": None,
    "paginas_atuais": {},
}

def _mesmo_console_de_contexto(e, elemento):
    """True quando ``e`` (da lista de foco) e ``elemento`` sao o MESMO console.

    H-0045-P03: no caminho de paginacao matricial, ``elemento`` pode ser um
    CLONE recortado para a pagina atual (``_elemento_fragmentado_para_pagina``
    -- ``copy.copy`` com ``_campos_inertes["itens"]`` substituido pela fatia
    da pagina). O clone e um objeto Python distinto: comparacao por identidade
    (``is``) nunca casa, mesmo sendo logicamente "o mesmo console". A
    correspondencia por ``id`` (estavel entre o console original e seu clone
    de pagina, preservado por ``copy.copy``) e a autoridade correta -- a MESMA
    usada por ``tela.navegacao`` para nomear consoles (NC-002/NC-003).

    H-0045-P04 / QA-H0045-P03-001: a correspondencia por ``id`` so e segura
    porque o loader rejeita IDs de console duplicados antes do runtime
    (``_validar_unicidade_ids_consoles``). Com unicidade garantida, o casamento
    clone/original permanece deterministico e o foco de um console nunca
    materializa cursor em outro.
    """
    if e is elemento:
        return True
    return (
        getattr(e, "tipo", None) == "console"
        and getattr(elemento, "tipo", None) == "console"
        and e.id == elemento.id
    )


def _console_focalizavel_de_contexto(elemento):
    """True quando ``elemento`` esta na lista de foco do contexto vigente.

    A coluna do indicador (D12) e reservada para consoles FOCALIZAVEIS (D2):
    consoles na lista de foco. Consoles nao focalizaveis (placeholder, sem
    itens navegaveis, nao navegaveis) NAO reservam a coluna e permanecem
    inalterados, preservando a compatibilidade retroativa. Quando o contexto
    de navegacao nao esta ativo (lista_foco ausente), nenhum console e
    considerado focalizavel (comportamento pre-H-0040).

    H-0045-P03: casa tambem por ``id`` (``_mesmo_console_de_contexto``) para
    reconhecer o clone de paginacao como o mesmo console da lista de foco.
    """
    lista = _navegacao_atual.get("lista_foco")
    if not lista:
        return False
    return any(_mesmo_console_de_contexto(e, elemento) for e in lista)


def _console_focado_de_contexto(elemento):
    """True quando ``elemento`` e o console focalizado do contexto vigente.

    D11: somente o console focado exibe o indicador. Consoles nao focados
    nao exibem o símbolo em nenhum item (PN-0008). Quando o contexto de
    navegacao nao esta ativo (lista_foco/foco_console ausentes), nenhum
    console e considerado focado (comportamento pre-H-0040).

    H-0045-P03: casa tambem por ``id`` (``_mesmo_console_de_contexto``) para
    reconhecer o clone de paginacao como o console focado.
    """
    lista = _navegacao_atual.get("lista_foco")
    foco = _navegacao_atual.get("foco_console")
    if not lista or foco is None:
        return False
    if foco < 0 or foco >= len(lista):
        return False
    return _mesmo_console_de_contexto(lista[foco], elemento)


def _console_original_de_contexto(elemento):
    """Resolve o console ORIGINAL (itens completos) correspondente a ``elemento``.

    H-0045-P03: no caminho de paginacao matricial, ``elemento`` pode ser um
    clone recortado para a pagina atual (``_elemento_fragmentado_para_pagina``),
    cujo ``_campos_inertes["itens"]`` contem SOMENTE os itens fisicos da
    pagina corrente. ``cursores[console.id]`` armazena o item logico GLOBAL
    (indice na lista COMPLETA de itens navegaveis do console -- a mesma
    autoridade usada por ``tela.navegacao.grade_de_itens`` e por
    ``tela.paginacao``): resolver o item corrente a partir da lista LOCAL do
    clone produz um indice fora de alcance (ou, pior, aponta para o item
    errado) a partir da segunda pagina. Retorna o console original da lista de
    foco (mesmo ``id``); quando nao ha correspondencia, retorna ``elemento``
    inalterado (compatibilidade retroativa fora do contexto de paginacao).

    H-0045-P04: com IDs unicos no loader, a busca por ``id`` encontra no
    maximo um console na lista de foco -- nao ha escolha arbitraria entre
    homonimos. Se o contexto estiver inconsistente (elemento sem
    correspondente), devolve ``elemento`` sem inventar outro console.
    """
    lista = _navegacao_atual.get("lista_foco")
    if lista:
        for e in lista:
            if _mesmo_console_de_contexto(e, elemento):
                return e
    return elemento


def _console_declarou_selecao_multipla(elemento):
    """True quando ``elemento`` declara ``politica_selecao == "multipla"``.

    H-0041 / ADR-0034: a coluna ``tg`` e os chips ``Espaco``/``Enter`` (Todos/
    Executar) aplicam-se a consoles que declaram selecao multipla. Leitura
    direta de ``_campos_inertes["politica_selecao"]`` (transporte inerte do
    modelo). Consoles sem a chave (legado) retornam ``False`` (preserva H-0040).
    """
    if getattr(elemento, "tipo", None) != "console":
        return False
    return elemento._campos_inertes.get("politica_selecao") == "multipla"


def _selecao_do_console_de_contexto(elemento):
    """Retorna o conjunto de IDs selecionados de ``elemento`` (reconciliado).

    H-0041 / ADR-0034 D-SEL-03: remove IDs inexistentes e itens que deixaram de
    ser selecionaveis, devolvendo o conjunto observado. Quando o contexto de
    selecao nao esta ativo (``selecoes`` ausente) ou o console nao esta no
    mapa, retorna conjunto vazio (preserva H-0040).
    """
    selecoes = _navegacao_atual.get("selecoes") or {}
    marcados = selecoes.get(elemento.id, ())
    if not marcados:
        return set()
    # Reconciliacao: somente IDs de itens selecionaveis permanecem.
    validos = set(_ids_selecionaveis_do_elemento(elemento))
    return set(marcados) & validos


def _ids_selecionaveis_do_elemento(elemento):
    """Lista de IDs selecionaveis do console na ordem declarada (D-SEL-02).

    Selecionavel requer ``navegavel`` E ``selecionavel`` verdadeiros. A ordem e
    a mesma de ``_itens_navegaveis_do_elemento`` (a ordem logica do console).
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    return [
        item.get("id")
        for item in itens
        if isinstance(item, dict)
        and item.get("navegavel")
        and item.get("selecionavel")
        and item.get("id") is not None
    ]


def _participante_eh_selecionavel(elemento, participante_idx):
    """True quando o participante de indice ``participante_idx`` e selecionavel.

    H-0041 / ADR-0034: resolve a selecionabilidade a partir do indice do
    participante na ordem declarada de itens. Itens nao dict e itens sem
    ``selecionavel`` verdadeiro retornam ``False`` (recebem ``tg`` vazio).
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    if participante_idx < 0 or participante_idx >= len(itens):
        return False
    item = itens[participante_idx]
    return (
        isinstance(item, dict)
        and bool(item.get("navegavel"))
        and bool(item.get("selecionavel"))
    )

DESCONTO_ESTRUTURAL_CONSOLE = 3

def _item_corrente_de_contexto(elemento):
    """Retorna o id do item navegavel corrente do ``elemento`` (console focado).

    Lê ``_navegacao_atual["cursores"][elemento.id]`` e resolve qual item
    navegavel da ordem declarada corresponde ao item logico armazenado. Quando
    ausente, retorna ``None`` (sem cursor materializado).

    H-0045-P03: o item logico e um indice GLOBAL (ordem declarada de itens
    navegaveis do console INTEIRO -- mesma autoridade de
    ``tela.navegacao.grade_de_itens``/``tela.paginacao``), nao um indice local
    da pagina. Resolve contra ``_console_original_de_contexto(elemento)`` (a
    lista COMPLETA) para que o mapeamento indice->id permaneca correto mesmo
    quando ``elemento`` e o clone recortado de uma pagina especifica.
    """
    cursores = _navegacao_atual.get("cursores") or {}
    idx = cursores.get(elemento.id)
    if idx is None:
        return None
    origem = _console_original_de_contexto(elemento)
    navegaveis = _itens_navegaveis_do_elemento(origem)
    if not navegaveis or idx < 0 or idx >= len(navegaveis):
        return None
    return navegaveis[idx].get("id")


def _itens_navegaveis_do_elemento(elemento):
    """Lista de itens navegaveis do elemento na ordem declarada (NC-002)."""
    itens = elemento._campos_inertes.get("itens", []) or []
    return [i for i in itens if isinstance(i, dict) and i.get("navegavel")]

def _console_tem_paginacao(elemento):
    return (
        getattr(elemento, "tipo", None) == "console"
        and elemento._campos_inertes.get("politica_paginacao") == "com"
    )


def _algum_console_paginado_no_corpo(elementos):
    """True se algum console de ``elementos`` declara ``politica_paginacao: "com"``.

    VM-H0045-R07-003: existencia de ``[<]``/``[>]`` (``contrato_console.md``
    §12: "existem quando a instancia declara paginacao: com") e propriedade
    ESTATICA do console declarado no corpo -- independente de o console ser
    FOCALIZAVEL (ADR-0031 D2 exige >= 1 item navegavel para entrar em
    ``navegacao.lista_foco``). Um console paginado com zero itens navegaveis
    (cenario "conjunto vazio") nunca aparece em ``lista_foco`` e por isso
    nao pode ser a fonte desta verificacao (usar ``lista_foco`` aqui omitia
    os chips por completo, em vez de exibi-los inativos). Percorre grupos
    recursivamente (mesma travessia de ``navegacao._atravessar_elementos``),
    sem aplicar o filtro de focalizabilidade.
    """
    for elemento in elementos or []:
        if getattr(elemento, "tipo", None) == "grupo":
            if _algum_console_paginado_no_corpo(elemento.elementos):
                return True
        elif _console_tem_paginacao(elemento):
            return True
    return False


def _pagina_atual_de_contexto(elemento):
    paginas = _navegacao_atual.get("paginas_atuais") or {}
    try:
        return max(1, int(paginas.get(elemento.id, 1)))
    except (TypeError, ValueError):
        return 1

def _preparar_contexto_navegacao(
    estilo, largura, altura, verboso,
    foco_console=None, cursores=None, lista_foco=None,
    largura_navegacao=None, selecoes=None, chips_destacados=None,
    executar_disponivel=None, paginas_atuais=None, modelo=None,
):
    """Repopula o contexto de runtime ``_navegacao_atual`` (H-0045-P05).

    Extraido de ``renderizar_tela`` para ser reutilizado por
    ``altura_interna_disponivel``: a autoridade de geometria vertical usada
    pela reconciliacao de pagina (``tela.paginacao``) precisa avaliar
    EXATAMENTE o mesmo contexto de chips (``regra_existencia``/``regra_ativo``
    da barra de menus, D-TEC-12) que o render real vai usar -- caso contrario
    a contagem de linhas da barra (``l_barra``) pode divergir entre a
    reconciliacao e o quadro efetivamente renderizado (VM-H0045-R04-004). O
    renderer e puro: o contexto e redefinido a cada chamada (R-14), nunca
    persiste entre redesenhos.

    VM-H0045-R07-003: ``modelo``, quando fornecido, alimenta
    ``_navegacao_atual["existe_console_paginado"]`` via
    ``_algum_console_paginado_no_corpo`` -- travessia do corpo INTEIRO
    (todos os consoles declarados, inclusive nao focalizaveis), distinta de
    ``lista_foco`` (apenas consoles focalizaveis, ADR-0031 D2). Sem
    ``modelo`` (chamadores legados), preserva a aproximacao anterior a
    partir de ``lista_foco``.
    """
    global _quadro_minimo_lancador_ativo
    _quadro_minimo_lancador_ativo = False
    _navegacao_atual["lista_foco"] = lista_foco
    if modelo is not None:
        _navegacao_atual["existe_console_paginado"] = _algum_console_paginado_no_corpo(
            modelo.corpo.elementos
        )
    else:
        _navegacao_atual["existe_console_paginado"] = any(
            _console_tem_paginacao(c) for c in (lista_foco or [])
        )
    _navegacao_atual["foco_console"] = foco_console
    _navegacao_atual["cursores"] = cursores or {}
    _navegacao_atual["largura"] = (
        largura_navegacao if largura_navegacao is not None else largura
    )
    _navegacao_atual["altura_interna"] = max(1, (altura if altura is not None else 24) - 8)
    _navegacao_atual["verboso"] = bool(verboso)
    _navegacao_atual["paginas_atuais"] = paginas_atuais or {}
    _navegacao_atual["simbolo"] = getattr(estilo, "selecionado_simbolo", None)
    _navegacao_atual["off"] = getattr(estilo, "selecionado_off", None)
    _navegacao_atual["selecoes"] = selecoes or {}
    _navegacao_atual["inc_on"] = getattr(estilo, "incluido_on", None)
    _navegacao_atual["inc_off"] = getattr(estilo, "incluido_off", None)
    _navegacao_atual["estado_ativo_chips"] = {}
    if chips_destacados is None:
        _navegacao_atual["chips_destacados"] = frozenset()
    elif isinstance(chips_destacados, dict):
        _navegacao_atual["chips_destacados"] = frozenset(
            k for k, v in chips_destacados.items() if v
        )
    else:
        _navegacao_atual["chips_destacados"] = frozenset(chips_destacados)
    _navegacao_atual["executar_disponivel"] = executar_disponivel
