"""API pura de selecao multipla por conjunto de IDs em console de nivel unico
(H-0041 / ADR-0034 Handoff 1, D-SEL-01 a D-SEL-10).

Este modulo implementa EXCLUSIVAMENTE o estado da selecao multipla como um
conjunto de IDs estaveis, por console, em runtime. Sem estado mutavel de
modulo e sem I/O. Toda transicao devolve um NOVO dict; nenhum dict recebido e
mutado (mesmo estilo de ``tela/navegacao.py``).

A selecao e INDEPENDENTE do cursor (D-SEL-01): o cursor e posicao (item
logico corrente); a selecao e inclusao (conjunto de IDs marcados). Marcar ou
desmarcar um item nunca move o cursor.

Decisoes cobertas:
- D-SEL-01: estado por conjunto de IDs, por console, runtime, sem duplicatas;
- D-SEL-02: a referencia de ordenacao e a ordem logica do console (a mesma de
  ``itens_navegaveis``), nunca a ordem de marcacao, posicao visual, pagina ou
  filtro;
- D-SEL-03: reconciliacao remove IDs inexistentes e itens que deixaram de ser
  selecionaveis, preservando a ordem logica;
- D-SEL-04: ``Todos`` com selecao vazia seleciona todos os selecionaveis;
- D-SEL-05: ``Espaco`` alterna somente item selecionavel, sem mover o cursor;
- D-SEL-06: ``Todos`` com zero selecionaveis produz conjunto vazio;
- D-SEL-09: inclusao e decidida por ``selecionavel`` (campo de item).

ESCOPO (H-0041 / ADR-0034 Handoff 1):
- Apenas selecao multipla por conjunto de IDs em console de nivel unico ja
  navegavel (H-0040 / ADR-0031).
- Sem operacao consumidora, sem execucao, sem protocolo de script, sem
  dry-run (D-SEL-07/D-SEL-21: ``Enter`` com selecao e INATIVO neste handoff).
- Sem memoria de selecao entre sessoes (estado exclusivamente runtime, NC-005).
- Sem estado global mutavel de modulo; toda funcao e pura.

Apenas biblioteca padrao do Python.
"""


def _selecao_do_console(estado, console):
    """Retorna a lista de IDs selecionados do ``console`` (copia, nunca None).

    A selecao e armazenada no estado de runtime em ``estado["selecoes"]`` como
    dict ``id_do_console -> lista de IDs``. Consoles sem entrada possuem
    selecao vazia. Nunca devolve ``None`` e nunca devolve a lista interna
    (sempre uma copia), de modo que mutacoes posteriores nao vazam.
    """
    selecoes = estado.get("selecoes") or {}
    return list(selecoes.get(console.id, ()))


def _escrever_selecao(estado, console, ids):
    """Retorna novo ``estado`` com a selecao de ``console`` substituida por ``ids``.

    Nao muta o dict recebido. ``ids`` e armazenado como lista nova (copia),
    independentemente do tipo de iteravel recebido. ``estado["selecoes"]`` e
    recriado (copia rasa do dict com a entrada de ``console.id`` atualizada).
    """
    selecoes = dict(estado.get("selecoes") or {})
    selecoes[console.id] = list(ids)
    novo = dict(estado)
    novo["selecoes"] = selecoes
    return novo


def itens_selecionaveis(console):
    """Lista de IDs selecionaveis do console na ordem declarada (D-SEL-02).

    Um item e selecionavel quando e um dict com ``navegavel`` verdadeiro E
    ``selecionavel`` verdadeiro. A ordem e a mesma de ``itens_navegaveis`` (a
    declaracao do JSON): a referencia de ordenacao da selecao sempre e a ordem
    logica do console, nunca a ordem de marcacao (D-SEL-02/D-SEL-03).

    Itens nao navegaveis e itens nao selecionaveis (``selecionavel`` ausente ou
    falso) ficam de fora. Retorna lista de IDs (strings), na ordem declarada.
    """
    if _eh_selecao_multinivel(console) or _eh_dois_niveis_por_foco(console):
        from tela import navegacao

        conteudo = getattr(console, "conteudo_externo", None)
        nos = getattr(conteudo, "nos", ()) if conteudo is not None else ()
        return [
            no.id for no in navegacao._nos_em_pre_ordem(nos)
            if navegacao.no_multinivel_selecionavel(no)
            and no.id is not None
        ]

    itens = console._campos_inertes.get("itens", []) or []
    return [
        item.get("id")
        for item in itens
        if isinstance(item, dict)
        and item.get("navegavel")
        and item.get("selecionavel")
        and item.get("id") is not None
    ]


def item_selecionavel(console, id_item):
    """True quando ``id_item`` e um item selecionavel do console (D-SEL-05).

    Selecionabilidade requer ``navegavel`` verdadeiro E ``selecionavel``
    verdadeiro. Usado pelo toggle e pela reconciliacao para decidir inclusao.
    """
    return id_item in itens_selecionaveis(console)


def selecao(console, estado):
    """Retorna a selecao corrente do ``console`` como lista de IDs (D-SEL-01).

    A selecao e sempre devolvida na ordem logica do console (D-SEL-02): a
    lista interna pode ter sido construida por marcacao arbitraria, mas a
    apresentacao e o consumo seguem a ordem de ``itens_selecionaveis``.
    Reconciliacao implicita (D-SEL-03): IDs inexistentes sao removidos na
    leitura, de modo que a selecao observada nunca carrega residuo.
    """
    marcados = _selecao_do_console(estado, console)
    if _eh_dois_niveis_por_foco(console):
        return _reconciliar_ids_dois_niveis(console, marcados)
    validos = itens_selecionaveis(console)
    valido_set = set(validos)
    # D-SEL-03: remove IDs inexistentes/não selecionáveis na leitura.
    presentes = [i for i in marcados if i in valido_set]
    # D-SEL-02: reordena pela ordem lógica do console.
    return [i for i in validos if i in set(presentes)]


def limpar(estado, console):
    """Retorna novo ``estado`` com selecao do ``console`` vazia (D-SEL-08).

    ``Esc`` com selecao ativa limpa e permanece na tela (o chamador decide
    se o proximo ``Esc`` volta/sai). Nenhum dict recebido e mutado.
    """
    if _eh_dois_niveis_por_foco(console):
        return _escrever_selecao(
            estado, console,
            _reconciliar_ids_dois_niveis(
                console, _selecao_do_console(estado, console)
            ),
        )
    return _escrever_selecao(estado, console, [])


def alternar(estado, console, id_item):
    """Retorna novo ``estado`` com a inclusao de ``id_item`` alternada (D-SEL-05).

    ``Espaco`` alterna a inclusao do item quando ele e selecionavel; nao move o
    cursor (o cursor e campo independente da selecao, D-SEL-01). Item nao
    selecionavel ignora o comando (sem efeito). Nao duplica IDs: se o item ja
    estava selecionado, ele e removido.

    Apos a transicao, a selecao e reordenada pela ordem logica do console
    (D-SEL-02), de modo que a marcacao nunca introduz ordem propria observavel.
    """
    if _eh_selecao_multinivel(console):
        return _alternar_multinivel(estado, console, id_item)
    if _eh_dois_niveis_por_foco(console):
        return _transferir_escolha_dois_niveis(
            estado, console, id_item
        )
    if not item_selecionavel(console, id_item):
        # D-SEL-05: item não selecionável ignora Espaço (sem efeito).
        return _escrever_selecao(estado, console, _selecao_do_console(estado, console))
    atual = selecao(console, estado)
    if id_item in atual:
        novo = [i for i in atual if i != id_item]
    else:
        novo = atual + [id_item]
    # D-SEL-02: reordena pela ordem lógica do console.
    ordem = itens_selecionaveis(console)
    ordem_set = set(novo)
    ordenado = [i for i in ordem if i in ordem_set]
    return _escrever_selecao(estado, console, ordenado)


def _eh_selecao_multinivel(console):
    campos = getattr(console, "_campos_inertes", {})
    politica = campos.get("politica_navegacao") if isinstance(campos, dict) else None
    return isinstance(politica, dict) and politica.get("tipo") == "selecao_multinivel"


def _eh_dois_niveis_por_foco(console):
    campos = getattr(console, "_campos_inertes", {})
    politica = campos.get("politica_navegacao") if isinstance(campos, dict) else None
    return isinstance(politica, dict) and politica.get("tipo") == "dois_niveis_por_foco"


def _reconciliar_ids_dois_niveis(console, ids):
    """Mantem exatamente a escolha de um filho direto por pai."""
    from tela import navegacao

    if not navegacao.estrutura_dois_niveis_valida(console):
        return []
    marcados = set(ids or ())
    escolhas = []
    for pai in console.conteudo_externo.nos:
        escolhido = next(
            (filho for filho in pai.filhos if filho.id in marcados),
            pai.filhos[0],
        )
        escolhas.append(escolhido.id)
    return escolhas


def _transferir_escolha_dois_niveis(estado, console, id_item):
    """Transfere a escolha somente entre filhos diretos do mesmo pai."""
    atuais = _reconciliar_ids_dois_niveis(
        console, _selecao_do_console(estado, console)
    )
    pai_alvo = next(
        (
            pai for pai in console.conteudo_externo.nos
            if any(filho.id == id_item for filho in pai.filhos)
        ),
        None,
    )
    if pai_alvo is None:
        return _escrever_selecao(estado, console, atuais)
    ids_do_pai = {filho.id for filho in pai_alvo.filhos}
    novo = [id_atual for id_atual in atuais if id_atual not in ids_do_pai]
    novo.append(id_item)
    return _escrever_selecao(
        estado, console, _reconciliar_ids_dois_niveis(console, novo)
    )


def inicializar_escolhas_dois_niveis(estado, console):
    """Materializa no runtime a escolha inicial derivada da ordem dos filhos."""
    if not _eh_dois_niveis_por_foco(console):
        return dict(estado)
    return _escrever_selecao(
        estado, console,
        _reconciliar_ids_dois_niveis(
            console, _selecao_do_console(estado, console)
        ),
    )


def _alvos_multinivel(console, id_item):
    """Resolve o item corrente e seu alcance recursivo selecionável.

    O próprio item selecionável faz parte do alcance. Isso permite que um
    pai sem filhos selecionáveis imediatos ainda seja alternado como estado
    binário independente; quando há filhos selecionáveis, a reconciliação
    posterior deriva o estado parental pela unanimidade.
    """
    from tela import navegacao

    conteudo = getattr(console, "conteudo_externo", None)
    nos = getattr(conteudo, "nos", ()) if conteudo is not None else ()
    corrente = next(
        (
            no for no in navegacao._nos_em_pre_ordem(nos)
            if no.id == id_item
        ),
        None,
    )
    if corrente is None:
        return []
    # A configuração válida não possui selecionáveis sob um nó não
    # selecionável. Sem suporte transitório para esse cenário inválido,
    # Espaço só resolve o alcance de um item selecionável.
    if not navegacao.no_multinivel_selecionavel(corrente):
        return []
    candidatos = [corrente] + navegacao._descendentes(corrente)
    return [
        no.id for no in candidatos
        if navegacao.no_multinivel_selecionavel(no) and no.id is not None
    ]


def _nos_e_pais_multinivel(console):
    """Retorna nós em pré-ordem e o pai lógico de cada nó."""
    from tela import navegacao

    conteudo = getattr(console, "conteudo_externo", None)
    nos = getattr(conteudo, "nos", ()) if conteudo is not None else ()
    todos = []
    pais = {}

    def recorrer(atual, pai=None):
        for no in atual or ():
            todos.append(no)
            if pai is not None and no.id is not None:
                pais[no.id] = pai
            recorrer(getattr(no, "filhos", ()), no)

    recorrer(nos)
    return todos, pais


def _reconciliar_ids_multinivel(console, ids):
    """Reconcilia estados parentais binários em pós-ordem.

    Para cada nó selecionável que possui filhos selecionáveis imediatos, o
    estado é derivado exclusivamente desses filhos. Nós não selecionáveis e
    pais sem filhos selecionáveis não recebem estado derivado. A saída segue
    a ordem lógica dos IDs estáveis já usada pelo console.
    """
    from tela import navegacao

    validos = set(itens_selecionaveis(console))
    marcados = {id_item for id_item in ids if id_item in validos}
    todos, _pais = _nos_e_pais_multinivel(console)

    # A pré-ordem coloca todos os descendentes depois de seus pais; invertê-la
    # garante que um pai leia estados já reconciliados dos filhos.
    for no in reversed(todos):
        if not navegacao.no_multinivel_selecionavel(no):
            continue
        filhos_selecionaveis = [
            filho for filho in getattr(no, "filhos", ()) or ()
            if navegacao.no_multinivel_selecionavel(filho)
            and filho.id is not None
        ]
        if not filhos_selecionaveis:
            continue
        if all(filho.id in marcados for filho in filhos_selecionaveis):
            marcados.add(no.id)
        else:
            marcados.discard(no.id)

    return [id_item for id_item in itens_selecionaveis(console)
            if id_item in marcados]


def _alternar_multinivel(estado, console, id_item):
    """Alterna um item e reconcilia todos os pais afetados H-0054."""
    alvos = _alvos_multinivel(console, id_item)
    if not alvos:
        return _escrever_selecao(
            estado,
            console,
            _reconciliar_ids_multinivel(
                console, _selecao_do_console(estado, console)
            ),
        )
    atual = _reconciliar_ids_multinivel(console, selecao(console, estado))
    atual_set = set(atual)
    if all(id_alvo in atual_set for id_alvo in alvos):
        novo_set = atual_set.difference(alvos)
    else:
        novo_set = atual_set.union(alvos)
    return _escrever_selecao(
        estado,
        console,
        _reconciliar_ids_multinivel(console, novo_set),
    )


def selecionar_todos(estado, console):
    """Retorna novo ``estado`` com todos os selecionaveis marcados (D-SEL-04).

    ``Enter`` com selecao vazia age como ``Todos``: marca todos os itens
    selecionaveis navegaveis (snapshot de IDs, D-SEL-01). Com zero itens
    selecionaveis, o conjunto permanece vazio (D-SEL-06). O snapshot segue a
    ordem logica do console (D-SEL-02).

    Nao executa, nao consome, nao produz resultado: a marcacao e o unico
    efeito (D-SEL-21).
    """
    ids = itens_selecionaveis(console)
    if _eh_selecao_multinivel(console):
        ids = _reconciliar_ids_multinivel(console, ids)
    return _escrever_selecao(estado, console, ids)


def reconciliar(estado, console):
    """Retorna novo ``estado`` com a selecao reconciliada (D-SEL-03).

    Remove IDs inexistentes (nao presentes no console) e itens que deixaram de
    ser selecionaveis, preservando a ordem logica. Funcao pura, isolada do
    binding de teclas: testavel diretamente. ``Reconciliacao vazia apos Enter
    nao executa nem aplica Todos no mesmo acionamento`` (D-SEL-04): esta
    funcao apenas limpa residuo, nunca marca.
    """
    ids = selecao(console, estado)
    if _eh_selecao_multinivel(console):
        ids = _reconciliar_ids_multinivel(console, ids)
    elif _eh_dois_niveis_por_foco(console):
        ids = _reconciliar_ids_dois_niveis(console, ids)
    return _escrever_selecao(estado, console, ids)


def esta_vazia(estado, console):
    """True quando a selecao do ``console`` esta vazia apos reconciliacao.

    Decide o rotulo dinamico de ``[Enter]``: vazia -> ``Todos``; nao vazia ->
    ``Executar`` (este, INATIVO neste handoff, D-SEL-07/D-SEL-21).
    """
    return len(selecao(console, estado)) == 0


def rotulo_enter(estado, console):
    """Retorna o rotulo dinamico de ``[Enter]`` conforme a selecao corrente.

    - selecao vazia -> ``"Todos"`` (ativo: marca todos os selecionaveis);
    - selecao nao vazia -> ``"Executar"`` (INATIVO neste handoff, D-SEL-07).

    O rotulo e derivado do estado reconciliado; nao depende da ordem de
    marcacao nem do cursor.
    """
    return "Todos" if esta_vazia(estado, console) else "Executar"


def rotulo_esc(estado, console, rotulo_original):
    """Retorna o texto do chip ``[Esc]`` para o ``console`` focal (P21).

    VM-H0045-R06-001: o tratamento funcional de Esc em ``demo/demo.py`` ja
    limpa a selecao do console focado (declarando selecao multipla nao vazia)
    e mantem a tela aberta; o defeito a corrigir e exclusivamente VISUAL -- o
    chip continuava exibindo o rotulo original enquanto a acao corrente era
    limpar a selecao.

    Esta funcao pura devolve:

    - ``"Limpar"``, quando ``console`` declara ``politica_selecao ==
      "multipla"`` E possui selecao reconciliada nao vazia;
    - ``rotulo_original`` (ex.: Sair, Voltar ou outro rotulo valido) em todos os
      demais
      casos: console sem selecao multipla, selecao vazia, ou console/rotulo
      ausentes.

    ``console`` pode ser ``None`` (sem console focado): devolve o rotulo
    original. ``rotulo_original`` ``None``/vazio tambem e devolvido inalterado
    (nao inventa rotulo). A funcao nao le estado de modulo nem arquivo, nao
    move cursor nem altera selecao -- apenas descreve o texto a exibir.
    """
    if not rotulo_original:
        return rotulo_original
    if console is None:
        return rotulo_original
    if not _console_declarou_selecao_multipla(console):
        return rotulo_original
    if _eh_dois_niveis_por_foco(console):
        return rotulo_original
    if esta_vazia(estado, console):
        return rotulo_original
    return "Limpar"


def _console_declarou_selecao_multipla(console):
    """True quando ``console`` declara ``politica_selecao == "multipla"``.

    Espelha ``tela.navegacao._console_declarou_selecao_multipla`` /
    ``tela.renderizador._console_declarou_selecao_multipla``: leitura direta de
    ``_campos_inertes["politica_selecao"]`` (transporte inerte do modelo).
    Consoles sem a chave (legado) ou que nao sao ``ElementoCorpo`` retornam
    ``False``. Centralizada aqui para que ``rotulo_esc`` permaneca pura e
    isolada de imports de outros modulos (D-SEL-01).
    """
    if console is None:
        return False
    campos = getattr(console, "_campos_inertes", None)
    if not isinstance(campos, dict):
        return False
    return campos.get("politica_selecao") == "multipla"


def chip_espaco_ativo(console, estado, navegacao):
    """True quando o chip ``[Espaco]`` esta ativo (D-SEL-09).

    O chip ``Espaco`` existe quando o console em foco declara selecao multipla
    (decidido pelo chamador/fixture); esta funcao decide o ESTADO ativo/inativo
    a partir do item sob cursor: ativo quando o item sob cursor e selecionavel,
    inativo caso contrario. Recebe ``navegacao`` (o modulo) para resolver o
    item corrente sem acoplar a ``tela.navegacao`` por import direto (preserva
    o isolamento e facilita testes).
    """
    item = navegacao.item_selecionado(console, estado)
    if not isinstance(item, dict):
        return False
    tipo_navegacao = getattr(navegacao, "tipo_navegacao_efetivo", None)
    if tipo_navegacao is not None and tipo_navegacao(console) in (
        "selecao_multinivel", "dois_niveis_por_foco"
    ):
        no = item.get("_no_multinivel")
        return navegacao.no_tem_alcance_selecao(no)
    return bool(item.get("selecionavel"))


def criar_selecoes_iniciais():
    """Retorna o dict inicial de selecoes por console (D-SEL-01/D-SEL-22).

    Selecao inicial sempre vazia por console (estado de runtime). Funcao pura:
    nao le estado de modulo nem arquivo. Usada por ``criar_estado_inicial`` do
    ponto de entrada para popular ``estado["selecoes"]``.
    """
    return {}
