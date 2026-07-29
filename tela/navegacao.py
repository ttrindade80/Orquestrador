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


def _coluna_com_itens(grade, coluna):
    """Lista de linhas ocupadas na ``coluna`` (toroide vertical)."""
    ocupadas = []
    for linha in range(len(grade)):
        if coluna < len(grade[linha]) and grade[linha][coluna] is not None:
            ocupadas.append(linha)
    return ocupadas


def _linha_com_itens(grade, linha):
    """Lista de colunas ocupadas na ``linha`` (toroide horizontal)."""
    ocupadas = []
    if 0 <= linha < len(grade):
        for coluna in range(len(grade[linha])):
            if grade[linha][coluna] is not None:
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


def mover_direita(estado, console):
    """Move o cursor para a direita com toroide na mesma linha (D8).

    Dominio: itens ocupados da mesma linha. Topologia TOROIDAL. Nao muda de
    linha (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma linha, produz SEM_MOVIMENTO (D9). Setas nunca alteram
    ``pagina_atual`` (D15/PN-0014).
    """
    return _mover_horizontal(estado, console, +1)


def mover_esquerda(estado, console):
    """Move o cursor para a esquerda com toroide na mesma linha (D8).

    Dominio: itens ocupados da mesma linha. Topologia TOROIDAL. Nao muda de
    linha (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma linha, produz SEM_MOVIMENTO (D9).
    """
    return _mover_horizontal(estado, console, -1)


def _mover_horizontal(estado, console, passo):
    """Nucleo do movimento horizontal toroidal (D8/D9)."""
    largura = estado.get("largura", 0)
    altura_interna = estado.get("altura_interna")
    desconto = estado.get("desconto_estrutural", 0)
    grade = grade_de_itens(console, largura, altura_interna, desconto_estrutural=desconto)
    cursores = dict(estado.get("cursores", {}))
    item_logico = cursores.get(console.id, 0)
    pos = _posicao_do_item_logico(grade, item_logico)
    if pos is None:
        return estado
    linha, _coluna = pos
    ocupadas = _linha_com_itens(grade, linha)
    idx = ocupadas.index(_coluna)
    novo_idx = (idx + passo) % len(ocupadas)
    nova_coluna = ocupadas[novo_idx]
    novo_item = item_logico_de_posicao(grade, linha, nova_coluna)
    novo = dict(estado)
    if novo_item is not None:
        cursores[console.id] = novo_item
    novo["cursores"] = cursores
    return novo


def mover_baixo(estado, console):
    """Move o cursor para baixo com toroide na mesma coluna (D8).

    Dominio: itens ocupados da mesma coluna. Topologia TOROIDAL. Nao muda de
    coluna (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma coluna, produz SEM_MOVIMENTO (D9).
    """
    return _mover_vertical(estado, console, +1)


def mover_cima(estado, console):
    """Move o cursor para cima com toroide na mesma coluna (D8).

    Dominio: itens ocupados da mesma coluna. Topologia TOROIDAL. Nao muda de
    coluna (PN-0007). Celulas vazias sao excluidas do toroide (PN-0006).

    Retorna novo estado com o item logico atualizado. Quando nao ha outro item
    ocupado na mesma coluna, produz SEM_MOVIMENTO (D9).
    """
    return _mover_vertical(estado, console, -1)


def _mover_vertical(estado, console, passo):
    """Nucleo do movimento vertical toroidal (D8/D9)."""
    largura = estado.get("largura", 0)
    altura_interna = estado.get("altura_interna")
    desconto = estado.get("desconto_estrutural", 0)
    grade = grade_de_itens(console, largura, altura_interna, desconto_estrutural=desconto)
    cursores = dict(estado.get("cursores", {}))
    item_logico = cursores.get(console.id, 0)
    pos = _posicao_do_item_logico(grade, item_logico)
    if pos is None:
        return estado
    _linha, coluna = pos
    ocupadas = _coluna_com_itens(grade, coluna)
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
    return len(itens_navegaveis(console)) > 1


def console_focado(estado):
    """Retorna o ElementoCorpo do console focado, ou ``None``."""
    lista = lista_foco(estado.get("modelo"))
    foco = estado.get("foco_console")
    if not lista or foco is None:
        return None
    if foco < 0 or foco >= len(lista):
        return None
    return lista[foco]
