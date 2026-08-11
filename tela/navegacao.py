"""API pura de foco, cursor, grade e selecao unica em console de nivel unico
(H-0040 / ADR-0031 D1-D15).

Este modulo implementa EXCLUSIVAMENTE a camada de navegacao de console de nivel
unico, sem estado mutavel de modulo e sem I/O. Toda a geometria consumida aqui
e a MESMA consumida pelo renderizador, via
``tela.distribuicao_matricial.calcular_distribuicao``. Nao existe grade
paralela independente (NC-003/NC-006): a identidade logica do item independe da
posicao fisica, e a geometria depende da largura atual e corresponde a grade
renderizada.

Decisoes cobertas: D2 (elegibilidade), D3 (lista por profundidade), D4 (ordem
entre irmaos), D5 (Tab/Shift+Tab circulares), D6 (entrada no item 0), D7 (row
-major), D8 (toroide por eixo + celulas vazias excluidas), D9 (degenerados),
D10 (preservar item logico em redimensionamento/mudanca de modo), D13 (selecao
unica como item sob cursor) e D15 (setas restritas a pagina atual).

ESCOPO (H-0040):
- Apenas navegacao de nivel unico entre itens ja expandidos de consoles
  focalizaveis.
- Sem paginacao interativa (D15/ITEM-0003), sem selecao multipla (D13/ITEM-0006),
  sem memoria de cursor por console (D6), sem acoes de Enter (ITEM-0004).
- Sem persistencia de estado: ``foco_console`` e ``cursores`` sao campos de
  runtime, NUNCA persistidos em JSON (NC-005).
- Sem estado global mutavel de modulo; toda funcao e pura.

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela
from tela.distribuicao_matricial import calcular_distribuicao


# ---------------------------------------------------------------------------
# D2 / D3 / D4 -- Elegibilidade e lista de foco por travessia em profundidade
# ---------------------------------------------------------------------------


def _item_eh_navegavel(item):
    """True quando ``item`` e um dict com ``navegavel`` verdadeiro."""
    return isinstance(item, dict) and bool(item.get("navegavel"))


def _campo_no(no, nome, padrao=None):
    """Le um campo de navegacao do no externo sem ampliar o modelo."""
    campos = getattr(no, "campos", {})
    if not isinstance(campos, dict):
        return padrao
    return campos.get(nome, padrao)


def no_multinivel_navegavel(no):
    """True quando o no externo participa do percurso multinivel.

    O modelo de conteudo externo transporta campos desconhecidos em
    ``NoConteudo.campos``. A ausencia de ``navegavel`` conserva a semantica
    hierarquica vigente: o no e navegavel por default. A politica explicita
    H-0054 continua sendo decidida somente pelo console.
    """
    return _campo_no(no, "navegavel", True) is not False


def no_multinivel_selecionavel(no):
    """True quando o no externo pode entrar no conjunto de selecao."""
    return bool(_campo_no(no, "selecionavel", False)) and no_multinivel_navegavel(no)


def _eh_selecao_multinivel(elemento):
    return tipo_navegacao_efetivo(elemento) == "selecao_multinivel"


def _eh_dois_niveis_por_foco(elemento):
    return tipo_navegacao_efetivo(elemento) == "dois_niveis_por_foco"


def estrutura_dois_niveis_valida(elemento):
    """Valida a topologia fechada de pais e filhos diretos do H-0055."""
    conteudo = getattr(elemento, "conteudo_externo", None)
    raizes = getattr(conteudo, "nos", ()) if conteudo is not None else ()
    if not raizes:
        return False
    ids = set()
    for pai in raizes:
        if not no_multinivel_navegavel(pai) or not pai.id or pai.id in ids:
            return False
        ids.add(pai.id)
        filhos = list(getattr(pai, "filhos", ()) or ())
        if not filhos:
            return False
        for filho in filhos:
            if (
                not no_multinivel_selecionavel(filho)
                or not filho.id
                or filho.id in ids
                or bool(getattr(filho, "filhos", ()))
            ):
                return False
            ids.add(filho.id)
    return True


def itens_navegaveis(elemento):
    """Lista de itens navegaveis do console na ordem declarada (D7).

    A fonte e ``ElementoCorpo._campos_inertes["itens"]`` (NC-002). A ordem
    declarada e preservada: ``["A", "B", "C"]`` torna-se ``[0, 1, 2]``
    (AT-0020). Nao recorre a hierarquia, nao infere, nao reordena.

    Retorna a lista de dicts (cada item navegavel). Consoles sem
    ``_campos_inertes["itens"]`` sao tratados como sem item navegavel.
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    return [i for i in itens if _item_eh_navegavel(i)]


def tipo_navegacao_efetivo(elemento):
    """Resolve o tipo declarado da politica de navegacao.

    A ausencia de ``tipo`` em uma politica valida preserva a compatibilidade
    legada com ``nivel_unico``. Uma politica que nao seja objeto nao recebe
    esse fallback; o loader a rejeita como estrutura invalida.
    """
    campos = getattr(elemento, "_campos_inertes", {})
    politica = campos.get("politica_navegacao") if isinstance(campos, dict) else None
    if not isinstance(politica, dict):
        return None
    return politica.get("tipo", "nivel_unico")


def console_e_focalizavel(elemento):
    """True quando ``elemento`` satisfaz D2: tipo ``console`` com
    ``politica_navegacao.navegavel == True`` E ao menos um item navegavel.

    ``lancador``, ``dashboard`` e ``grupo`` nunca sao focalizaveis (D1).
    Consoles sem ``politica_navegacao`` ou sem item navegavel ficam de fora.
    Consoles sem ``_campos_inertes["itens"]`` sao tratados como nao
    focalizaveis.
    """
    if elemento is None:
        return False
    if getattr(elemento, "tipo", None) != "console":
        return False
    politica = elemento._campos_inertes.get("politica_navegacao")
    if not isinstance(politica, dict) or not politica.get("navegavel"):
        return False
    tipo = tipo_navegacao_efetivo(elemento)
    if tipo == "arvore_colapsavel":
        conteudo = getattr(elemento, "conteudo_externo", None)
        return conteudo is not None and bool(getattr(conteudo, "nos", None))
    if tipo == "selecao_multinivel":
        conteudo = getattr(elemento, "conteudo_externo", None)
        if conteudo is None or not getattr(conteudo, "nos", None):
            return False
        return any(
            no_multinivel_navegavel(no)
            for no in _nos_em_pre_ordem(getattr(conteudo, "nos", ()))
        )
    if tipo == "dois_niveis_por_foco":
        return estrutura_dois_niveis_valida(elemento)
    if tipo != "nivel_unico":
        return False
    return len(itens_navegaveis(elemento)) > 0


def _atravessar_elementos(elementos, acumulador):
    """Travessia em profundidade (D3) que coleta consoles focalizaveis.

    Grupos sao atravessados para alcancar descendentes, mas nunca entram na
    lista de foco (PN-0001). A ordem entre irmaos segue a declaracao do JSON
    (D4). A quantidadade desigual de descendentes nao altera a travessia: cada
    ramo e esgotado antes do proximo irmao.
    """
    for elemento in elementos:
        if elemento.tipo == "grupo":
            _atravessar_elementos(elemento.elementos, acumulador)
        elif elemento.tipo == "console" and console_e_focalizavel(elemento):
            acumulador.append(elemento)


def lista_foco(modelo):
    """Lista plana de consoles focalizaveis por travessia em profundidade.

    Resultado de D3/D4: lista linear ordenada de referencias aos consoles
    focalizaveis, da esquerda para a direita e de cima para baixo. Grupos
    sao percorridos mas nao entram na lista (PN-0001). ``lancador`` e
    ``dashboard`` sao excluidos (PN-0002/PN-0003). Consoles nao navegaveis ou
    sem item navegavel sao excluidos (PN-0004).

    Aceita ``ModeloTela`` (percorre ``corpo.elementos``), uma lista de
    ``ElementoCorpo`` direta, ou ``None``/falso. Lista vazia ou entrada
    invalida nao altera estado (D5).
    """
    if modelo is None:
        return []
    if isinstance(modelo, ModeloTela):
        elementos = modelo.corpo.elementos
    elif isinstance(modelo, list):
        elementos = modelo
    else:
        # Entrada invalida (mock em testes, etc.): sem lista de foco.
        return []
    acumulador = []
    _atravessar_elementos(elementos, acumulador)
    return acumulador


# ---------------------------------------------------------------------------
# D5 / D6 -- Tab/Shift+Tab circulares e entrada no item logico 0
# ---------------------------------------------------------------------------

# Sequencias de Shift+Tab efetivamente recebidas pelo mecanismo atual de leitura
# (NC-001). Ambas sao reconhecidas; Tab simples permanece ``"\t"``.
SHIFT_TAB_SEQUENCIAS = ("\x1b[Z", "\x1b\t")
TAB = "\t"


def e_tab(tecla):
    """True quando ``tecla`` e Tab simples (``"\\t"``)."""
    return tecla == TAB


def e_shift_tab(tecla):
    """True quando ``tecla`` e alguma sequencia de Shift+Tab reconhecida.

    Testa ambas as sequencias ``"\\x1b[Z"`` e ``"\\x1b\\t"`` conforme NC-001,
    preservando Tab simples como tabulacao. Nao escolhe apenas uma sem teste.
    """
    return tecla in SHIFT_TAB_SEQUENCIAS


def avancar_foco(estado):
    """Retorna novo estado com foco avancado circularmente (D5, Tab).

    Tab percorre a lista de foco no sentido direto e circular: o ultimo
    avanca para o primeiro. A entrada em qualquer console posiciona o cursor
    no item logico 0 (D6): o runtime NAO mantem memoria de cursor por console
    para restaurar ao retornar (PN-0005). Lista vazia nao altera o estado.

    ``estado`` e um dict com ``foco_console`` (int ou None) e ``cursores``
    (dict id->int). Retorna um NOVO dict sem mutar o recebido.
    """
    foco = estado.get("foco_console")
    lista = lista_foco(estado.get("modelo"))
    if not lista:
        return dict(estado)
    if foco is None:
        novo_foco = 0
    else:
        novo_foco = (foco + 1) % len(lista)
    novo = dict(estado)
    novo["foco_console"] = novo_foco
    # D6: toda entrada posiciona cursor no item logico 0. Nao restaura cursor
    # anterior do console destino (PN-0005).
    console = lista[novo_foco]
    cursores = dict(estado.get("cursores", {}))
    cursores[console.id] = 0
    novo["cursores"] = cursores
    return novo


def recuar_foco(estado):
    """Retorna novo estado com foco recuado circularmente (D5, Shift+Tab).

    Shift+Tab percorre a mesma lista no sentido inverso e circular: o primeiro
    recua para o ultimo. A entrada em qualquer console posiciona o cursor no
    item logico 0 (D6). Lista vazia nao altera o estado.

    ``estado`` e um dict com ``foco_console`` (int ou None) e ``cursores``.
    Retorna um NOVO dict sem mutar o recebido.
    """
    foco = estado.get("foco_console")
    lista = lista_foco(estado.get("modelo"))
    if not lista:
        return dict(estado)
    if foco is None:
        novo_foco = len(lista) - 1
    else:
        novo_foco = (foco - 1) % len(lista)
    novo = dict(estado)
    novo["foco_console"] = novo_foco
    console = lista[novo_foco]
    cursores = dict(estado.get("cursores", {}))
    cursores[console.id] = 0
    novo["cursores"] = cursores
    return novo


# ---------------------------------------------------------------------------
# D7 / D8 / D9 -- Grade de itens, geometria e toroide por eixo
# ---------------------------------------------------------------------------


def grade_de_itens(elemento, largura, altura_interna=None, desconto_estrutural=0):
    """Grade row-major dos itens navegaveis do console para a largura atual.

    Funcao nova autorizada em ``tela/navegacao.py`` (NC-003/NC-006). Consome o
    MESMO resultado efetivamente usado pela exibicao atual: chama
    ``calcular_distribuicao`` com os mesmos ``participantes`` (cada item
    navegavel, na ordem declarada) e a mesma ``distribuicao_matricial``
    declarada pelo console. Nao cria distribuicao paralela divergente.

    Retorna uma lista de listas (linhas), onde cada celula e o item (dict) ou
    ``None`` para celula vazia (AT-0019). Celulas vazias nao recebem cursor e
    nao participam do toroide (D8/PN-0006). A identidade logica do item
    independe da posicao fisica (D7).

    QAI40-002 (geometria unica): a largura util dos itens e calculada pela
    AUTORIDADE UNICA do renderer. A navegacao NAO conhece implicitamente o
    desconto estrutural do renderer; ele e recebido como parametro EXPLICITO
    ``desconto_estrutural`` (default 0 = sem desconto, preservando chamadas que
    ja passam a largura interna). A sequencia e inequivoca:

    ```
    largura (total ou interna, conforme desconto_estrutural)
    → desconto estrutural explicito do renderer, quando fornecido
    → reserva da coluna indicadora POR ITEM (qai40-001), quando focalizavel
    → largura util entregue a calcular_distribuicao
    ```

    QAI40-001: cada item navegavel possui sua propria coluna indicadora (itens
    lado a lado tem colunas independentes). A reserva entra no requisito minimo
    de largura de cada item (``min_w = texto + LARGURA_INDICADOR_COLUNA``), de
    modo que a formacao calculada coincide EXATAMENTE com a grade renderizada
    (AT-0021/PN-0016), que aplica a mesma reserva por celula.

    O runtime real (``demo/demo.py``) repassa o desconto estrutural declarado
    pelo renderer (``DESCONTO_ESTRUTURAL_CONSOLE``), de modo que a grade de
    navegacao corresponde EXATAMENTE a grade renderizada (AT-0021/PN-0016).

    ``altura_interna`` opcional permite fixar a area interna (altura da caixa
    menos topo/base). Quando ``None``, estima area suficiente (orientada pelo
    conteudo), coerente com o renderer.
    """
    config = getattr(elemento, "distribuicao_matricial", None)
    navegaveis = itens_navegaveis(elemento)
    n = len(navegaveis)
    # QAI40-002: aplica o desconto estrutural EXPLICITO (nao hardcoded). A area
    # de distribuicao NAO desconta o indicador separadamente: a reserva entra
    # no min_w de cada item (QAI40-001), igual ao renderer.
    area_w = max(0, largura - desconto_estrutural)
    if altura_interna is None:
        area_h = max(1, n) + 8
    else:
        area_h = max(0, altura_interna)

    if n == 0 or config is None:
        return [[item] for item in navegaveis] if navegaveis else []

    # QAI40-001: o requisito minimo de cada item inclui a coluna indicadora
    # quando o console e focalizavel (uma coluna por item, lado a lado).
    ind_w = LARGURA_INDICADOR_COLUNA if console_e_focalizavel(elemento) else 0
    # H-0041 / ADR-0034 D-SEL-09: quando o console declara selecao multipla,
    # cada item reserva tambem a coluna ``tg`` (inclusao), adjacente a ``ec``.
    # A soma preserva a paridade geometrica com o renderer (AT-0021/PN-0016).
    ind_w += LARGURA_INDICADOR_INCLUSAO if _console_declarou_selecao_multipla(elemento) else 0
    min_ws = [len(item.get("texto", item.get("valor", ""))) + ind_w for item in navegaveis]
    min_hs = [1 for _ in navegaveis]

    resultado = calcular_distribuicao(
        area_w=area_w,
        area_h=area_h,
        n_participantes=n,
        config=config,
        min_ws=min_ws,
        min_hs=min_hs,
    )

    grade_grid = resultado["grade"]
    if grade_grid is None:
        return [[item] for item in navegaveis]

    n_linhas, n_colunas = resultado["formacao"]
    matriz = [[None] * n_colunas for _ in range(n_linhas)]
    for celula in resultado["celulas"]:
        participante = celula["participante"]
        matriz[celula["linha"]][celula["coluna"]] = navegaveis[participante]
    return matriz


# D12: largura reservada para a coluna do indicador de cursor (simbolo + 1
# espaco separador). A reserva e estavel e participa do calculo de largura
# util disponivel para o conteudo do item (ADR-0031 D12). Renderer e navegacao
# aplicam o MESMO desconto para que as geometrias coincidam (AT-0021/PN-0016).
LARGURA_INDICADOR_COLUNA = 2

# H-0041 / ADR-0034 D-SEL-09: largura reservada para a coluna do indicador de
# inclusao (``tg``), paralela e adjacente a coluna ``ec`` (simbolo + 1 espaco
# separador). Mesmo principio de ``LARGURA_INDICADOR_COLUNA``: a reserva entra
# no ``min_w`` de cada item quando o console declara ``politica_selecao:
# "multipla"``, preservando a paridade geometrica com a coluna renderizada
# (AT-0021/PN-0016). O loader ja aceita ``"multipla"`` em
# ``_POLITICA_SELECAO_VALIDOS`` (campo declarado, nao validado por aqui).
LARGURA_INDICADOR_INCLUSAO = 2


def _console_declarou_selecao_multipla(elemento):
    """True quando ``elemento`` declara ``politica_selecao == "multipla"``.

    H-0041 / ADR-0034: a coluna ``tg`` e reservada para consoles que declaram
    selecao multipla, independentemente de haver itens selecionaveis. A leitura
    e direta de ``_campos_inertes["politica_selecao"]`` (transporte inerte do
    modelo); nenhum default e inventado e nenhum campo novo e exigido do JSON.
    Consoles sem a chave (legado) retornam ``False`` (preserva H-0040).
    """
    if getattr(elemento, "tipo", None) != "console":
        return False
    politica = elemento._campos_inertes.get("politica_selecao")
    return politica == "multipla"


def _posicao_do_item_logico(grade, item_logico):
    """Retorna (linha, coluna) do item logico ``item_logico`` na ``grade``.

    Percorre a grade em row-major (D7) contando somente celulas ocupadas (nao
    ``None``) como itens logicos. Retorna ``None`` quando o item logico nao
    existe na grade (por exemplo, apos redimensionamento que reduziu a
    cardinalidade visivel -- cenario nao coberto por nivel unico vigente).
    """
    contador = 0
    for linha in range(len(grade)):
        for coluna in range(len(grade[linha])):
            if grade[linha][coluna] is not None:
                if contador == item_logico:
                    return (linha, coluna)
                contador += 1
    return None


def item_logico_de_posicao(grade, linha, coluna):
    """Retorna o item logico (indice) da celula (linha, coluna), ou ``None``.

    Celulas vazias (``None``) e posicoes fora da grade retornam ``None``: elas
    nao recebem cursor e nao participam do toroide (D8).
    """
    if linha < 0 or linha >= len(grade):
        return None
    if coluna < 0 or coluna >= len(grade[linha]):
        return None
    if grade[linha][coluna] is None:
        return None
    contador = 0
    for r in range(len(grade)):
        for c in range(len(grade[r])):
            if grade[r][c] is None:
                continue
            if (r, c) == (linha, coluna):
                return contador
            contador += 1
    return None


def _posicoes_permitidas(grade, itens_permitidos):
    if itens_permitidos is None:
        return None
    permitidos = set(itens_permitidos)
    posicoes = set()
    contador = 0
    for linha in range(len(grade)):
        for coluna in range(len(grade[linha])):
            if grade[linha][coluna] is None:
                continue
            if contador in permitidos:
                posicoes.add((linha, coluna))
            contador += 1
    return posicoes


def _coluna_com_itens(grade, coluna, itens_permitidos=None):
    """Lista de linhas ocupadas na ``coluna`` (toroide vertical)."""
    posicoes = _posicoes_permitidas(grade, itens_permitidos)
    ocupadas = []
    for linha in range(len(grade)):
        if coluna < len(grade[linha]) and grade[linha][coluna] is not None:
            if posicoes is not None and (linha, coluna) not in posicoes:
                continue
            ocupadas.append(linha)
    return ocupadas


def _linha_com_itens(grade, linha, itens_permitidos=None):
    """Lista de colunas ocupadas na ``linha`` (toroide horizontal)."""
    posicoes = _posicoes_permitidas(grade, itens_permitidos)
    ocupadas = []
    if 0 <= linha < len(grade):
        for coluna in range(len(grade[linha])):
            if grade[linha][coluna] is not None:
                if posicoes is not None and (linha, coluna) not in posicoes:
                    continue
                ocupadas.append(coluna)
    return ocupadas


def _mover_toroide_lista(atual, ocupados):
    """Avanca/recua em ``ocupados`` com toroide (wrap) independentemente por eixo.

    ``atual`` e o valor corrente; ``ocupados`` e a lista ordenada de posicoes
    validas do eixo. Retorna a proxima/anterior posicao com wraparound. Quando
    ``atual`` nao esta em ``ocupados`` (celula vazia) ou ha menos de 2
    ocupados, retorna ``atual`` (SEM_MOVIMENTO -- D9).
    """
    if len(ocupados) < 2:
        return atual
    if atual not in ocupados:
        return atual
    idx = ocupados.index(atual)
    return ocupados[(idx + 1) % len(ocupados)]


def mover_direita(estado, console, itens_permitidos=None):
    """Move o cursor para a direita com toroide na mesma linha (D8).

    Dominio: itens ocupados da mesma linha. Topologia TOROIDAL. Nao muda de
    linha (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma linha, produz SEM_MOVIMENTO (D9). Setas nunca alteram
    ``pagina_atual`` (D15/PN-0014).
    """
    return _mover_horizontal(estado, console, +1, itens_permitidos=itens_permitidos)


def mover_esquerda(estado, console, itens_permitidos=None):
    """Move o cursor para a esquerda com toroide na mesma linha (D8).

    Dominio: itens ocupados da mesma linha. Topologia TOROIDAL. Nao muda de
    linha (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma linha, produz SEM_MOVIMENTO (D9).
    """
    return _mover_horizontal(estado, console, -1, itens_permitidos=itens_permitidos)


def _mover_horizontal(estado, console, passo, itens_permitidos=None):
    """Nucleo do movimento horizontal toroidal (D8/D9)."""
    if tipo_navegacao_efetivo(console) == "dois_niveis_por_foco":
        return _mover_dois_niveis(estado, console, passo, itens_permitidos)
    if tipo_navegacao_efetivo(console) != "nivel_unico":
        return estado
    largura = estado.get("largura", 0)
    altura_interna = estado.get("altura_interna")
    desconto = estado.get("desconto_estrutural", 0)
    grade = grade_de_itens(console, largura, altura_interna, desconto_estrutural=desconto)
    cursores = dict(estado.get("cursores", {}))
    item_logico = cursores.get(console.id, 0)
    if itens_permitidos is not None and item_logico not in set(itens_permitidos):
        return estado
    pos = _posicao_do_item_logico(grade, item_logico)
    if pos is None:
        return estado
    linha, _coluna = pos
    ocupadas = _linha_com_itens(grade, linha, itens_permitidos=itens_permitidos)
    if _coluna not in ocupadas:
        return estado
    idx = ocupadas.index(_coluna)
    novo_idx = (idx + passo) % len(ocupadas)
    nova_coluna = ocupadas[novo_idx]
    novo_item = item_logico_de_posicao(grade, linha, nova_coluna)
    novo = dict(estado)
    if novo_item is not None:
        cursores[console.id] = novo_item
    novo["cursores"] = cursores
    return novo


def _ramos_fechados_do_console(estado, console):
    todos = estado.get("ramos_fechados", {}) or {}
    fechados = todos.get(console.id, ()) if isinstance(todos, dict) else ()
    return set(fechados or ())


def _nos_em_pre_ordem(nos):
    """Achata uma hierarquia externa preservando a ordem declarada."""
    resultado = []

    def recorrer(atual):
        for no in atual or ():
            resultado.append(no)
            recorrer(getattr(no, "filhos", ()))

    recorrer(nos)
    return resultado


def _sequencia_estrutural_selecao_multinivel(elemento):
    """Retorna a topologia unica de nos navegaveis do H-0054."""
    conteudo = getattr(elemento, "conteudo_externo", None)
    if conteudo is None:
        return []
    return [
        no for no in _nos_em_pre_ordem(getattr(conteudo, "nos", ()))
        if no_multinivel_navegavel(no)
    ]


def _sequencia_estrutural_dois_niveis(elemento):
    """Retorna pais e filhos em pre-ordem, somente para topologia valida."""
    if not estrutura_dois_niveis_valida(elemento):
        return []
    return _nos_em_pre_ordem(elemento.conteudo_externo.nos)


def _indices_dois_niveis(elemento):
    """Mapeia cada raiz e seus filhos aos indices logicos renderizados."""
    resultado = []
    indice = 0
    for pai in elemento.conteudo_externo.nos:
        indice_pai = indice
        indice += 1
        filhos = []
        for filho in pai.filhos:
            filhos.append((indice, filho))
            indice += 1
        resultado.append((indice_pai, pai, filhos))
    return resultado


def _toroide_ativo_dois_niveis(elemento, estado, itens_permitidos=None):
    """Resolve o toroide corrente sem armazenar um campo adicional de nivel."""
    estruturas = _indices_dois_niveis(elemento)
    cursor = (estado.get("cursores", {}) or {}).get(elemento.id, 0)
    if itens_permitidos is None:
        itens_permitidos = _itens_permitidos_da_pagina(estado, elemento)
    permitidos = None if itens_permitidos is None else set(itens_permitidos)
    for indice_pai, pai, filhos in estruturas:
        if cursor == indice_pai:
            candidatos = [(i, no) for i, no, _filhos in estruturas]
            break
        if any(cursor == indice_filho for indice_filho, _filho in filhos):
            candidatos = filhos
            break
    else:
        return []
    if permitidos is not None:
        candidatos = [par for par in candidatos if par[0] in permitidos]
    return candidatos


def em_nivel_filhos(estado, console):
    """True quando o cursor corrente pertence a um filho direto."""
    if not _eh_dois_niveis_por_foco(console):
        return False
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    return any(
        cursor == indice_filho
        for _indice_pai, _pai, filhos in _indices_dois_niveis(console)
        for indice_filho, _filho in filhos
    )


def rotulo_esc_dois_niveis(estado, console):
    """Deriva o rótulo de Esc a partir do nível ativo de H-0055."""
    if not _eh_dois_niveis_por_foco(console):
        return None
    return "Voltar" if em_nivel_filhos(estado, console) else "Sair"


def entrar_nivel_filhos(estado, console):
    """Entra nos filhos do pai corrente, posicionando no filho escolhido."""
    if not _eh_dois_niveis_por_foco(console):
        return dict(estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    estrutura = next(
        (item for item in _indices_dois_niveis(console) if item[0] == cursor),
        None,
    )
    if estrutura is None:
        return dict(estado)
    _indice_pai, _pai, filhos = estrutura
    escolhidos = set((estado.get("selecoes", {}) or {}).get(console.id, ()))
    indice = next((i for i, no in filhos if no.id in escolhidos), filhos[0][0])
    novo = dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    cursores[console.id] = indice
    novo["cursores"] = cursores
    return novo


def retornar_nivel_pais(estado, console):
    """Retorna do filho corrente ao respectivo pai, preservando escolhas."""
    if not _eh_dois_niveis_por_foco(console):
        return dict(estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    indice_pai = next(
        (
            ip for ip, _pai, filhos in _indices_dois_niveis(console)
            if any(cursor == indice for indice, _filho in filhos)
        ),
        None,
    )
    if indice_pai is None:
        return dict(estado)
    novo = dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    cursores[console.id] = indice_pai
    novo["cursores"] = cursores
    return novo


def _sequencia_com_indices_selecao_multinivel(
    elemento, estado, itens_permitidos=None
):
    estrutural = _sequencia_estrutural_selecao_multinivel(elemento)
    if itens_permitidos is None:
        itens_permitidos = _itens_permitidos_da_pagina(estado, elemento)
    if itens_permitidos is None:
        return list(enumerate(estrutural))
    permitidos = set(itens_permitidos)
    return [
        (indice, no)
        for indice, no in enumerate(estrutural)
        if indice in permitidos
    ]


def sequencia_visivel_selecao_multinivel(
    elemento, estado, itens_permitidos=None
):
    """Retorna a projeção paginada da topologia única do H-0054."""
    return [
        no for _indice, no in
        _sequencia_com_indices_selecao_multinivel(
            elemento, estado, itens_permitidos
        )
    ]


def _sequencia_estrutural_arvore(elemento, estado):
    """Deriva a pre-ordem visivel da hierarquia canonica do console."""
    conteudo = getattr(elemento, "conteudo_externo", None)
    if conteudo is None or not getattr(conteudo, "nos", None):
        return []
    fechados = _ramos_fechados_do_console(estado, elemento)
    resultado = []

    def recorrer(nos):
        for no in nos:
            resultado.append(no)
            if no.id not in fechados and no.filhos:
                recorrer(no.filhos)

    recorrer(conteudo.nos)
    return resultado


def _itens_permitidos_da_pagina(estado, console):
    """Obtém a projeção de paginação já calculada pela infraestrutura vigente."""
    declarados = estado.get("itens_permitidos")
    if isinstance(declarados, dict) and console.id in declarados:
        return declarados[console.id]
    if console._campos_inertes.get("politica_paginacao") != "com":
        return None
    from tela import paginacao

    return paginacao.linhas_logicas_navegaveis_da_pagina(estado, console)


def _sequencia_com_indices_arvore(elemento, estado, itens_permitidos=None):
    estrutural = _sequencia_estrutural_arvore(elemento, estado)
    if itens_permitidos is None:
        itens_permitidos = _itens_permitidos_da_pagina(estado, elemento)
    if itens_permitidos is None:
        return list(enumerate(estrutural))
    permitidos = set(itens_permitidos)
    return [
        (indice, no)
        for indice, no in enumerate(estrutural)
        if indice in permitidos
    ]


def sequencia_visivel_arvore(elemento, estado, itens_permitidos=None):
    """Retorna a projeção linear navegável da árvore na página corrente.

    A hierarquia continua sendo exclusivamente ``conteudo_externo``. O
    resultado é uma lista transitória em pré-ordem, filtrada pela projeção de
    página fornecida pela paginação existente quando aplicável.
    """
    return [
        no for _indice, no in
        _sequencia_com_indices_arvore(elemento, estado, itens_permitidos)
    ]


def reconciliar_cursor_arvore(estado, console=None):
    """Reconcilia o cursor da árvore focalizada com a projeção visível.

    A entrada normal na navegação já posiciona o cursor no primeiro item. Este
    boundary aplica a mesma regra quando o foco chega acompanhado de um mapa
    de cursores ainda vazio ou inválido, antes de qualquer projeção contextual.
    Uma projeção vazia não recebe cursor sintético.
    """
    if console is None:
        console = console_focado(estado)
    if console is None:
        return dict(estado)

    tipo = tipo_navegacao_efetivo(console)
    if tipo == "arvore_colapsavel":
        acessiveis = _sequencia_com_indices_arvore(console, estado)
    elif tipo == "selecao_multinivel":
        acessiveis = _sequencia_com_indices_selecao_multinivel(console, estado)
    elif tipo == "dois_niveis_por_foco":
        acessiveis = _toroide_ativo_dois_niveis(console, estado)
    else:
        return dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    if not acessiveis:
        cursores.pop(console.id, None)
    else:
        indices = [indice for indice, _no in acessiveis]
        if cursores.get(console.id) not in indices:
            cursores[console.id] = indices[0]

    novo = dict(estado)
    novo["cursores"] = cursores
    return novo


def alternar_ramo(estado, console):
    """Alterna o ramo corrente sem criar seleção ou ação para folhas."""
    if tipo_navegacao_efetivo(console) != "arvore_colapsavel":
        return dict(estado)
    estrutural = _sequencia_estrutural_arvore(console, estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    if cursor < 0 or cursor >= len(estrutural):
        return dict(estado)
    corrente = estrutural[cursor]
    if not corrente.filhos:
        return dict(estado)

    fechados_por_console = dict(estado.get("ramos_fechados", {}) or {})
    fechados = set(fechados_por_console.get(console.id, ()) or ())
    if corrente.id in fechados:
        fechados.remove(corrente.id)
    else:
        fechados.add(corrente.id)
    fechados_por_console[console.id] = frozenset(fechados)

    novo = dict(estado)
    novo["ramos_fechados"] = fechados_por_console
    nova_sequencia = _sequencia_estrutural_arvore(console, novo)
    por_id = {no.id: indice for indice, no in enumerate(nova_sequencia)}
    cursores = dict(estado.get("cursores", {}) or {})
    if corrente.id in por_id:
        cursores[console.id] = por_id[corrente.id]
    novo["cursores"] = cursores
    return novo


def mover_baixo(estado, console, itens_permitidos=None):
    """Move o cursor para baixo com toroide na mesma coluna (D8).

    Dominio: itens ocupados da mesma coluna. Topologia TOROIDAL. Nao muda de
    coluna (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma coluna, produz SEM_MOVIMENTO (D9).
    """
    if tipo_navegacao_efetivo(console) == "arvore_colapsavel":
        return _mover_arvore(estado, console, +1, itens_permitidos)
    if tipo_navegacao_efetivo(console) == "selecao_multinivel":
        return _mover_selecao_multinivel(estado, console, +1, itens_permitidos)
    if tipo_navegacao_efetivo(console) == "dois_niveis_por_foco":
        return _mover_dois_niveis(estado, console, +1, itens_permitidos)
    return _mover_vertical(estado, console, +1, itens_permitidos=itens_permitidos)


def mover_cima(estado, console, itens_permitidos=None):
    """Move o cursor para cima com toroide na mesma coluna (D8).

    Dominio: itens ocupados da mesma coluna. Topologia TOROIDAL. Nao muda de
    coluna (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma coluna, produz SEM_MOVIMENTO (D9).
    """
    if tipo_navegacao_efetivo(console) == "arvore_colapsavel":
        return _mover_arvore(estado, console, -1, itens_permitidos)
    if tipo_navegacao_efetivo(console) == "selecao_multinivel":
        return _mover_selecao_multinivel(estado, console, -1, itens_permitidos)
    if tipo_navegacao_efetivo(console) == "dois_niveis_por_foco":
        return _mover_dois_niveis(estado, console, -1, itens_permitidos)
    return _mover_vertical(estado, console, -1, itens_permitidos=itens_permitidos)


def _mover_arvore(estado, console, passo, itens_permitidos=None):
    """Move pelo índice estrutural da projeção visível corrente."""
    acessiveis = _sequencia_com_indices_arvore(
        console, estado, itens_permitidos
    )
    if len(acessiveis) < 2:
        return dict(estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    indices = [indice for indice, _no in acessiveis]
    if cursor not in indices:
        return dict(estado)
    posicao = indices.index(cursor)
    novo_posicao = posicao + passo
    if novo_posicao < 0 or novo_posicao >= len(acessiveis):
        return dict(estado)
    novo = dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    cursores[console.id] = acessiveis[novo_posicao][0]
    novo["cursores"] = cursores
    return novo


def _mover_selecao_multinivel(estado, console, passo, itens_permitidos=None):
    """Move cima/baixo na sequencia linear de todos os niveis navegaveis."""
    acessiveis = _sequencia_com_indices_selecao_multinivel(
        console, estado, itens_permitidos
    )
    if len(acessiveis) < 2:
        return dict(estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    indices = [indice for indice, _no in acessiveis]
    if cursor not in indices:
        return dict(estado)
    posicao = indices.index(cursor)
    novo_posicao = posicao + passo
    if novo_posicao < 0 or novo_posicao >= len(acessiveis):
        return dict(estado)
    novo = dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    cursores[console.id] = acessiveis[novo_posicao][0]
    novo["cursores"] = cursores
    return novo


def _mover_dois_niveis(estado, console, passo, itens_permitidos=None):
    """Move com wrap apenas no toroide de pais ou de filhos ativo."""
    acessiveis = _toroide_ativo_dois_niveis(
        console, estado, itens_permitidos
    )
    if len(acessiveis) < 2:
        return dict(estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
    indices = [indice for indice, _no in acessiveis]
    if cursor not in indices:
        return dict(estado)
    novo = dict(estado)
    cursores = dict(estado.get("cursores", {}) or {})
    cursores[console.id] = indices[(indices.index(cursor) + passo) % len(indices)]
    novo["cursores"] = cursores
    return novo


def _mover_vertical(estado, console, passo, itens_permitidos=None):
    """Nucleo do movimento vertical toroidal (D8/D9)."""
    if tipo_navegacao_efetivo(console) != "nivel_unico":
        return estado
    largura = estado.get("largura", 0)
    altura_interna = estado.get("altura_interna")
    desconto = estado.get("desconto_estrutural", 0)
    grade = grade_de_itens(console, largura, altura_interna, desconto_estrutural=desconto)
    cursores = dict(estado.get("cursores", {}))
    item_logico = cursores.get(console.id, 0)
    if itens_permitidos is not None and item_logico not in set(itens_permitidos):
        return estado
    pos = _posicao_do_item_logico(grade, item_logico)
    if pos is None:
        return estado
    _linha, coluna = pos
    ocupadas = _coluna_com_itens(grade, coluna, itens_permitidos=itens_permitidos)
    if _linha not in ocupadas:
        return estado
    idx = ocupadas.index(_linha)
    novo_idx = (idx + passo) % len(ocupadas)
    nova_linha = ocupadas[novo_idx]
    novo_item = item_logico_de_posicao(grade, nova_linha, coluna)
    novo = dict(estado)
    if novo_item is not None:
        cursores[console.id] = novo_item
    novo["cursores"] = cursores
    return novo


# ---------------------------------------------------------------------------
# D10 -- Preservar item logico em redimensionamento/mudanca de modo
# ---------------------------------------------------------------------------


def posicao_corrente(estado, console):
    """Retorna (linha, coluna) fisica do item corrente na grade vigente (D10).

    A posicao fisica e recalculada a partir do item logico corrente na grade da
    largura atual: o item logico e preservado, mas a linha, a coluna e os
    vizinhos sao recalculados. Retorna ``None`` quando o console nao tem item
    corrente ou o item nao aparece na grade atual.
    """
    cursores = estado.get("cursores", {})
    item_logico = cursores.get(console.id, 0)
    grade = grade_de_itens(
        console, estado.get("largura", 0), estado.get("altura_interna"),
        desconto_estrutural=estado.get("desconto_estrutural", 0),
    )
    return _posicao_do_item_logico(grade, item_logico)


def redimensionar(estado, nova_largura, nova_altura=None):
    """Retorna novo estado apos mudanca de dimensao preservando item logico (D10).

    Preserva a identidade do item logico corrente, o console focado, a pagina
    atual (quando aplicavel) e o modo atual. Descarta qualquer geometria
    anterior (formacao, linha/coluna, vizinhos, largura/altura anteriores): a
    grade, os vizinhos e o toroide sao sempre recalculados a partir da
    largura/altura correntes na primeira seta (patch VM-11 / PN-0012).

    O cursor NAO volta ao item 0 (PN-0012). ``nova_altura`` opcional atualiza
    ``altura`` no estado quando fornecida.
    """
    novo = dict(estado)
    novo["largura"] = nova_largura
    if nova_altura is not None:
        novo["altura"] = nova_altura
    # Nenhuma formacao/vizinhanca e cacheada no estado: movers e posicao_corrente
    # consomem sempre ``grade_de_itens`` com a geometria corrente.
    return novo


# ---------------------------------------------------------------------------
# D13 -- Selecao unica como item sob cursor
# ---------------------------------------------------------------------------


def item_selecionado(console, estado):
    """Retorna o item sob o cursor (D13: selecao unica).

    A selecao unica e o item logico corrente: sem conjunto de selecao, sem
    toggle por espaco e sem indicador de inclusao. Retorna o dict do item
    navegavel corrente ou ``None`` quando o console nao tem item navegavel.
    """
    if tipo_navegacao_efetivo(console) in (
        "selecao_multinivel", "dois_niveis_por_foco"
    ):
        if tipo_navegacao_efetivo(console) == "selecao_multinivel":
            acessiveis = _sequencia_com_indices_selecao_multinivel(console, estado)
        else:
            acessiveis = list(enumerate(
                _sequencia_estrutural_dois_niveis(console)
            ))
        cursor = (estado.get("cursores", {}) or {}).get(console.id, 0)
        no = next(
            (no for indice, no in acessiveis if indice == cursor),
            None,
        )
        if no is None:
            return None
        return {
            "id": no.id,
            "texto": "",
            "navegavel": True,
            "selecionavel": no_multinivel_selecionavel(no),
            "_no_multinivel": no,
        }

    navegaveis = itens_navegaveis(console)
    if not navegaveis:
        return None
    cursores = estado.get("cursores", {})
    idx = cursores.get(console.id, 0)
    if idx < 0 or idx >= len(navegaveis):
        idx = 0
    return navegaveis[idx]


def processar_espaco(estado):
    """Espaco nao cria, alterna nem alterna selecao (D13/PN-0017).

    Retorna o estado inalterado (copia). A barra de espaco pertence ao ciclo de
    selecao multipla (ITEM-0006), fora do escopo do H-0040.
    """
    return dict(estado)


# ---------------------------------------------------------------------------
# D14 -- Condicoes dos chips [⇆] e [✥]
# ---------------------------------------------------------------------------


def exibir_chip_alternar(estado):
    """True quando ``[⇆]`` deve aparecer: >= 2 consoles focalizaveis (D14).

    A condicao considera consoles FOCALIZAVEIS (D2), nao apenas declarados como
    navegaveis. Consoles navegaveis sem itens navegaveis nao entram na contagem.
    """
    return len(lista_foco(estado.get("modelo"))) >= 2


def exibir_chip_navegar(estado):
    """True quando ``[✥]`` deve aparecer: console focado com > 1 item (D14).

    ``[✥]`` so aparece no console focado com mais de um item navegavel. Nao
    aparece com zero itens, um item ou nenhum console focado. Nao existe
    estado inativo para ``[✥]`` (regra_existencia exclusiva).
    """
    lista = lista_foco(estado.get("modelo"))
    if not lista:
        return False
    foco = estado.get("foco_console")
    if foco is None:
        return False
    console = lista[foco]
    if tipo_navegacao_efetivo(console) == "arvore_colapsavel":
        return len(sequencia_visivel_arvore(console, estado)) > 1
    if tipo_navegacao_efetivo(console) == "selecao_multinivel":
        return len(sequencia_visivel_selecao_multinivel(console, estado)) > 1
    if tipo_navegacao_efetivo(console) == "dois_niveis_por_foco":
        return len(_toroide_ativo_dois_niveis(console, estado)) > 1
    if console._campos_inertes.get("politica_paginacao") == "com":
        from tela import paginacao

        return len(paginacao.linhas_logicas_navegaveis_da_pagina(estado, console)) > 1
    return len(itens_navegaveis(console)) > 1


def estado_chip_arvore(estado):
    """Deriva o rótulo e a atividade do Espaço pelo item corrente da árvore.

    A projeção usa o mesmo universo visível consumido pelos movimentos. Se o
    console não estiver focalizado ou o cursor não apontar para um item dessa
    projeção, não há estado válido a materializar.
    """
    console = console_focado(estado)
    if console is None or tipo_navegacao_efetivo(console) != "arvore_colapsavel":
        return None
    acessiveis = _sequencia_com_indices_arvore(console, estado)
    cursor = (estado.get("cursores", {}) or {}).get(console.id)
    corrente = next(
        (no for indice, no in acessiveis if indice == cursor),
        None,
    )
    if corrente is None:
        return None
    fechados = _ramos_fechados_do_console(estado, console)
    possui_filhos = bool(corrente.filhos)
    return {
        "console_id": console.id,
        "item_id": corrente.id,
        "texto": "Expandir" if not possui_filhos or corrente.id in fechados else "Recolher",
        "ativo": possui_filhos,
    }


def _descendentes(no):
    resultado = []

    def recorrer(filhos):
        for filho in filhos or ():
            resultado.append(filho)
            recorrer(getattr(filho, "filhos", ()))

    recorrer(getattr(no, "filhos", ()))
    return resultado


def no_tem_alcance_selecao(no):
    """True quando Espaço tem ao menos um alvo selecionavel no no corrente."""
    # Em uma configuração válida, toda seleção abaixo já torna o nó corrente
    # selecionável. Não há alcance especial através de pai não selecionável.
    return no is not None and no_multinivel_selecionavel(no)


def estado_chip_selecao(estado):
    """Deriva a acionabilidade do chip ``[␣] Selecionar`` do H-0054."""
    console = console_focado(estado)
    if console is None or tipo_navegacao_efetivo(console) not in (
        "selecao_multinivel", "dois_niveis_por_foco"
    ):
        return None
    item = item_selecionado(console, estado)
    no = item.get("_no_multinivel") if isinstance(item, dict) else None
    if no is None:
        return None
    ativo = no_tem_alcance_selecao(no)
    if tipo_navegacao_efetivo(console) == "dois_niveis_por_foco":
        ativo = bool(getattr(no, "filhos", ())) or no_multinivel_selecionavel(no)
    return {
        "console_id": console.id,
        "item_id": no.id,
        "texto": "Selecionar",
        "ativo": ativo,
    }


def console_focado(estado):
    """Retorna o ElementoCorpo do console focado, ou ``None``."""
    lista = lista_foco(estado.get("modelo"))
    foco = estado.get("foco_console")
    if not lista or foco is None:
        return None
    if foco < 0 or foco >= len(lista):
        return None
    return lista[foco]
