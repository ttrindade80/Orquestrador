"""Motor geometrico centralizado da capacidade `distribuicao_matricial` (ADR-0025 / H-0035).

Este modulo implementa o calculo geometrico deterministico da distribuicao
matricial de nivel unico. Ele organiza os *participantes imediatos* de um
elemento declarante (dashboard, console ou lancador) em uma grade, dentro da
area util ja alocada a esse elemento.

ESCOPO (H-0035):
- Apenas geometria pura: sem I/O, sem leitura de arquivo, sem estado global.
- Nivel unico: organiza somente os participantes imediatos; nao percorre
  descendentes, nao propaga configuracao, nao cria recursao/heranca/cascata.
- Determinismo total: mesma entrada -> mesma saida, com criterios completos
  de desempate por ordem declarada.
- Validacao estrutural da configuracao e responsabilidade do loader
  (`tela/loader.py`). Este motor assume config ja validada, mas ainda assim
  levanta `DistribuicaoMatricialErro` para invariantes geometricos violados
  em tempo de calculo (defesa em profundidade).

O ponto publico e `calcular_distribuicao`.

Apenas biblioteca padrao do Python.
"""

from math import ceil


class DistribuicaoMatricialErro(Exception):
    """Erro de dominio no calculo geometrico da distribuicao matricial."""


# ---------------------------------------------------------------------------
# Parse da configuracao (a config chega ja validada estruturalmente pelo loader)
# ---------------------------------------------------------------------------


def _medida(espacamento, chave):
    """Devolve (minimo, maximo) de uma medida de espacamento.

    ``maximo`` pode ser ``None`` (ilimitado). ``minimo`` >= 0.
    """
    medida = espacamento.get(chave, {})
    minimo = medida.get("minimo", 0)
    maximo = medida.get("maximo")
    return int(minimo), (None if maximo is None else int(maximo))


# ---------------------------------------------------------------------------
# Formacao: enumeracao de candidatas na ordem de preferencia
# ---------------------------------------------------------------------------


def _formacoes_candidatas(formacao, n):
    """Gera as formacoes (n_linhas, n_colunas) candidatas em ordem de preferencia.

    - ``preferencia_linhas``: n_linhas cresce de lin_min ate lin_max (ou n);
      para cada n_linhas, n_colunas = ceil(n / n_linhas), limitado por bounds
      de colunas quando declarados.
    - ``preferencia_colunas``: n_colunas cresce de col_min ate col_max (ou n);
      para cada n_colunas, n_linhas = ceil(n / n_colunas), limitado por bounds
      de linhas quando declarados.
    - ``matriz_fixa``: exatamente linhas.fixo x colunas.fixo.

    A ordem em que as formacoes sao geradas define o desempate: a primeira que
    couber geometricamente e selecionada.
    """
    politica = formacao.get("politica")
    linhas = formacao.get("linhas", {}) or {}
    colunas = formacao.get("colunas", {}) or {}

    if n <= 0:
        return []

    if politica == "matriz_fixa":
        return [(int(linhas["fixo"]), int(colunas["fixo"]))]

    if politica == "preferencia_linhas":
        lin_min = int(linhas.get("minimo", 1))
        lin_max = linhas.get("maximo")
        lin_max = n if lin_max is None else min(int(lin_max), n)
        col_min = colunas.get("minimo")
        col_max = colunas.get("maximo")
        candidatas = []
        for n_linhas in range(lin_min, lin_max + 1):
            n_colunas = ceil(n / n_linhas)
            if col_min is not None and n_colunas < int(col_min):
                continue
            if col_max is not None and n_colunas > int(col_max):
                continue
            candidatas.append((n_linhas, n_colunas))
        return candidatas

    if politica == "preferencia_colunas":
        col_min = int(colunas.get("minimo", 1))
        col_max = colunas.get("maximo")
        col_max = n if col_max is None else min(int(col_max), n)
        lin_min = linhas.get("minimo")
        lin_max = linhas.get("maximo")
        candidatas = []
        for n_colunas in range(col_min, col_max + 1):
            n_linhas = ceil(n / n_colunas)
            if lin_min is not None and n_linhas < int(lin_min):
                continue
            if lin_max is not None and n_linhas > int(lin_max):
                continue
            candidatas.append((n_linhas, n_colunas))
        return candidatas

    raise DistribuicaoMatricialErro(
        "formacao.politica desconhecida: {0!r}".format(politica)
    )


# ---------------------------------------------------------------------------
# Atribuicao de participantes a celulas
# ---------------------------------------------------------------------------


def _atribuir_celulas(n, n_linhas, n_colunas, ordem):
    """Mapeia cada participante ``i`` (0..n-1) a uma celula (linha, coluna).

    - ``por_linha``: preenche a grade linha a linha (linha = i // n_colunas).
    - ``por_coluna``: preenche a grade coluna a coluna (linha = i % n_linhas).

    A sequencia original dos participantes e preservada; apenas a celula muda.
    Retorna lista de (linha, coluna) indexada por participante, mais os
    conjuntos de indices de participantes por coluna e por linha.
    """
    atribuicao = []
    for i in range(n):
        if ordem == "por_linha":
            linha = i // n_colunas
            coluna = i % n_colunas
        elif ordem == "por_coluna":
            linha = i % n_linhas
            coluna = i // n_linhas
        else:
            raise DistribuicaoMatricialErro(
                "ordem desconhecida: {0!r}".format(ordem)
            )
        atribuicao.append((linha, coluna))
    return atribuicao


# ---------------------------------------------------------------------------
# Dimensionamento base de colunas e linhas
# ---------------------------------------------------------------------------


def _dimensao_base(politica, minimo_fixo, indices_por_faixa, medidas_min, todos_min):
    """Calcula a dimensao base de cada faixa (coluna ou linha).

    - ``maior_da_coluna`` / ``maior_da_linha``: max dos minimos dos participantes
      daquela faixa (0 quando a faixa esta vazia).
    - ``uniforme``: todas as faixas recebem o max global dos minimos.
    - ``minimo_fixo``: todas as faixas recebem exatamente ``minimo_fixo``.

    ``indices_por_faixa``: lista (por faixa) de listas de indices de participantes.
    ``medidas_min``: lista (por participante) do requisito minimo no eixo.
    ``todos_min``: max global dos minimos (para ``uniforme``).
    """
    n_faixas = len(indices_por_faixa)
    if politica == "minimo_fixo":
        return [int(minimo_fixo)] * n_faixas
    if politica == "uniforme":
        return [todos_min] * n_faixas
    # maior_da_coluna / maior_da_linha
    dims = []
    for indices in indices_por_faixa:
        if indices:
            dims.append(max(medidas_min[i] for i in indices))
        else:
            dims.append(0)
    return dims


# ---------------------------------------------------------------------------
# Distribuicao da sobra entre margens e vaos
# ---------------------------------------------------------------------------


def _distribuir_sobra(sobra, slots, politica_global, ordem_expansao, politica_resto):
    """Distribui ``sobra`` (>= 0) entre os slots de espacamento de um eixo.

    ``slots``: lista ordenada de dicts, cada um com:
        ``tipo`` in {"margem_ini", "margem_fim", "vao"}
        ``minimo`` (int >= 0), ``maximo`` (int ou None)
    A ordem de ``slots`` no eixo horizontal e:
        [margem_ini, vao, vao, ..., margem_fim]
    Os valores partem sempre do minimo (invioláveis) e recebem sobra conforme
    ``politica_global`` (posicao/uso do excedente), ``ordem_expansao`` (quais
    slots recebem primeiro) e ``politica_resto`` (a quem vai o pixel residual).

    Retorna a lista de valores finais (um por slot, na mesma ordem).
    """
    valores = [s["minimo"] for s in slots]

    def _idx(tipos):
        return [i for i, s in enumerate(slots) if s["tipo"] in tipos]

    idx_margem_ini = _idx(("margem_ini",))
    idx_margem_fim = _idx(("margem_fim",))
    idx_vaos = _idx(("vao",))
    idx_margens = idx_margem_ini + idx_margem_fim

    def _capacidade(i):
        maximo = slots[i]["maximo"]
        if maximo is None:
            return None  # ilimitado
        return maximo - valores[i]

    def _adicionar(indices, quantidade):
        """Distribui ``quantidade`` uniformemente entre ``indices`` respeitando
        maximos. Devolve o que sobrou sem colocar. Determinismo: distribuicao
        base uniforme; resto inteiro segue ``politica_resto``.
        """
        restante = quantidade
        if not indices or restante <= 0:
            return restante
        # Rodadas ate esgotar restante ou saturar todos.
        while restante > 0:
            abertos = [i for i in indices if _capacidade(i) is None or _capacidade(i) > 0]
            if not abertos:
                break
            base = restante // len(abertos)
            if base == 0:
                break
            algum = False
            for i in abertos:
                cap = _capacidade(i)
                dar = base if cap is None else min(cap, base)
                if dar > 0:
                    valores[i] += dar
                    restante -= dar
                    algum = True
            if not algum:
                break
        # Resto inteiro (< len(abertos)): distribui uma unidade por slot pela
        # ordem definida por politica_resto.
        abertos = [i for i in indices if _capacidade(i) is None or _capacidade(i) > 0]
        if politica_resto == "ao_ultimo":
            abertos = list(reversed(abertos))
        for i in abertos:
            if restante <= 0:
                break
            valores[i] += 1
            restante -= 1
        return restante

    if politica_global == "inicio":
        # Excedente vai para a margem final; margem inicial no minimo.
        _adicionar(idx_margem_fim, sobra)
    elif politica_global == "fim":
        _adicionar(idx_margem_ini, sobra)
    elif politica_global == "centro":
        # Divide igualmente entre margem inicial e final; resto por politica_resto.
        metade = sobra // 2
        resto = sobra - 2 * metade
        _adicionar(idx_margem_ini, metade)
        _adicionar(idx_margem_fim, metade)
        if resto:
            alvo = idx_margem_ini if politica_resto == "ao_primeiro" else idx_margem_fim
            _adicionar(alvo, resto)
    elif politica_global in ("entre_participantes", "entre_linhas"):
        # Excedente para os vaos internos (uniforme entre vaos).
        sobra_restante = _adicionar(idx_vaos, sobra)
        # Se nao ha vaos (uma coluna/linha) ou saturaram, cai para margens.
        if sobra_restante > 0:
            _adicionar(idx_margens, sobra_restante)
    elif politica_global == "uniforme":
        # Excedente para todos os slots (margens + vaos) pela ordem de expansao.
        _distribuir_por_ordem_expansao(
            sobra, idx_margens, idx_vaos, ordem_expansao, _adicionar
        )
    elif politica_global == "margens_limitadas":
        # Margens primeiro (ate max), depois vaos.
        sobra_restante = _adicionar(idx_margens, sobra)
        if sobra_restante > 0:
            _adicionar(idx_vaos, sobra_restante)
    else:
        raise DistribuicaoMatricialErro(
            "distribuicao politica desconhecida: {0!r}".format(politica_global)
        )

    return valores


def _distribuir_por_ordem_expansao(sobra, idx_margens, idx_vaos, ordem_expansao, adicionar):
    """Aplica ``ordem_expansao`` ao distribuir ``sobra`` entre margens e vaos."""
    if ordem_expansao == "margens_primeiro_depois_vaos":
        restante = adicionar(idx_margens, sobra)
        if restante > 0:
            adicionar(idx_vaos, restante)
    elif ordem_expansao == "vaos_primeiro_depois_margens":
        restante = adicionar(idx_vaos, sobra)
        if restante > 0:
            adicionar(idx_margens, restante)
    elif ordem_expansao == "uniforme_margens_e_vaos":
        todos = idx_margens + idx_vaos
        adicionar(todos, sobra)
    else:
        raise DistribuicaoMatricialErro(
            "ordem_expansao desconhecida: {0!r}".format(ordem_expansao)
        )


# ---------------------------------------------------------------------------
# Montagem dos slots de um eixo
# ---------------------------------------------------------------------------


def _montar_slots(margem_ini, margem_fim, vao, n_faixas):
    """Monta a lista ordenada de slots de espacamento de um eixo.

    Ordem: [margem_ini, vao_1, ..., vao_(n_faixas-1), margem_fim].
    ``margem_ini``/``margem_fim``/``vao`` sao pares (minimo, maximo).
    """
    slots = [{"tipo": "margem_ini", "minimo": margem_ini[0], "maximo": margem_ini[1]}]
    for _ in range(max(0, n_faixas - 1)):
        slots.append({"tipo": "vao", "minimo": vao[0], "maximo": vao[1]})
    slots.append({"tipo": "margem_fim", "minimo": margem_fim[0], "maximo": margem_fim[1]})
    return slots


def _min_slots(margem_ini, margem_fim, vao, n_faixas):
    """Soma dos minimos de espacamento de um eixo (margens + vaos)."""
    return margem_ini[0] + margem_fim[0] + max(0, n_faixas - 1) * vao[0]


# ---------------------------------------------------------------------------
# Ponto publico
# ---------------------------------------------------------------------------


def calcular_distribuicao(area_w, area_h, n_participantes, config,
                          min_ws=None, min_hs=None):
    """Calcula o layout matricial dos participantes na area util dada.

    Parametros:
        area_w, area_h: dimensoes da area util (inteiros >= 0).
        n_participantes: numero de participantes imediatos (>= 0).
        config: dict `distribuicao_matricial` ja validado pelo loader.
        min_ws: lista (por participante) da largura minima interna exigida.
            None -> assume 0 para todos.
        min_hs: lista (por participante) da altura minima interna exigida.
            None -> assume 0 para todos.

    Retorna dict:
        {
          "fallback": bool,
          "formacao": (n_linhas, n_colunas),
          "celulas": [ {participante, linha, coluna, x, y, largura, altura}, ... ],
          "grade": {
             "larguras_colunas", "alturas_linhas",
             "margem_esq", "margem_dir", "margem_sup", "margem_inf",
             "vaos_h", "vaos_v",
          },
        }

    Quando nenhuma formacao permitida couber respeitando todos os minimos,
    ``fallback`` = True e os demais campos ficam vazios/None. O consumidor
    (renderer) deve entao acionar o quadro minimo canonico global.

    Determinismo: dado o mesmo conjunto de argumentos, sempre retorna o mesmo
    dict. Desempate de formacao por ordem de preferencia; desempate de resto
    inteiro por ``politica_resto``.
    """
    if n_participantes < 0:
        raise DistribuicaoMatricialErro("n_participantes negativo")

    if min_ws is None:
        min_ws = [0] * n_participantes
    if min_hs is None:
        min_hs = [0] * n_participantes
    if len(min_ws) != n_participantes or len(min_hs) != n_participantes:
        raise DistribuicaoMatricialErro(
            "min_ws/min_hs incoerentes com n_participantes"
        )

    formacao = config["formacao"]
    ordem = config["ordem"]
    dim = config["dimensionamento"]
    esp = config["espacamento"]

    dim_col_pol = dim["colunas"]["politica"]
    dim_lin_pol = dim["linhas"]["politica"]
    dim_col_min = dim["colunas"].get("minimo")
    dim_lin_min = dim["linhas"].get("minimo")

    margem_esq = _medida(esp, "margem_esquerda")
    margem_dir = _medida(esp, "margem_direita")
    margem_sup = _medida(esp, "margem_superior")
    margem_inf = _medida(esp, "margem_inferior")
    vao_h = _medida(esp, "vao_horizontal")
    vao_v = _medida(esp, "vao_vertical")

    dist_h = config["distribuicao_horizontal"]["politica"]
    dist_v = config["distribuicao_vertical"]["politica"]
    exp_h = config["ordem_expansao"]["horizontal"]
    exp_v = config["ordem_expansao"]["vertical"]
    resto_h = config["politica_resto"]["horizontal"]
    resto_v = config["politica_resto"]["vertical"]

    todos_w = max(min_ws) if min_ws else 0
    todos_h = max(min_hs) if min_hs else 0

    resultado_vazio = {
        "fallback": True,
        "formacao": None,
        "celulas": [],
        "grade": None,
    }

    if n_participantes == 0:
        # Sem participantes: nada a distribuir; nao e fallback.
        return {
            "fallback": False,
            "formacao": (0, 0),
            "celulas": [],
            "grade": {
                "larguras_colunas": [],
                "alturas_linhas": [],
                "margem_esq": margem_esq[0],
                "margem_dir": margem_dir[0],
                "margem_sup": margem_sup[0],
                "margem_inf": margem_inf[0],
                "vaos_h": [],
                "vaos_v": [],
            },
        }

    candidatas = _formacoes_candidatas(formacao, n_participantes)

    for (n_linhas, n_colunas) in candidatas:
        if n_linhas <= 0 or n_colunas <= 0:
            continue
        if n_linhas * n_colunas < n_participantes:
            continue

        atribuicao = _atribuir_celulas(
            n_participantes, n_linhas, n_colunas, ordem
        )

        indices_por_coluna = [[] for _ in range(n_colunas)]
        indices_por_linha = [[] for _ in range(n_linhas)]
        for i, (lin, col) in enumerate(atribuicao):
            indices_por_coluna[col].append(i)
            indices_por_linha[lin].append(i)

        larguras_colunas = _dimensao_base(
            dim_col_pol, dim_col_min, indices_por_coluna, min_ws, todos_w
        )
        alturas_linhas = _dimensao_base(
            dim_lin_pol, dim_lin_min, indices_por_linha, min_hs, todos_h
        )

        total_min_w = (
            _min_slots(margem_esq, margem_dir, vao_h, n_colunas)
            + sum(larguras_colunas)
        )
        total_min_h = (
            _min_slots(margem_sup, margem_inf, vao_v, n_linhas)
            + sum(alturas_linhas)
        )

        if total_min_w > area_w or total_min_h > area_h:
            continue  # nao cabe; tentar proxima formacao

        # --- Distribuicao horizontal ---
        slots_h = _montar_slots(margem_esq, margem_dir, vao_h, n_colunas)
        sobra_w = area_w - total_min_w
        vals_h = _distribuir_sobra(sobra_w, slots_h, dist_h, exp_h, resto_h)
        m_esq = vals_h[0]
        m_dir = vals_h[-1]
        vaos_h = [vals_h[k] for k in range(1, len(vals_h) - 1)]

        # --- Distribuicao vertical ---
        slots_v = _montar_slots(margem_sup, margem_inf, vao_v, n_linhas)
        sobra_h = area_h - total_min_h
        vals_v = _distribuir_sobra(sobra_h, slots_v, dist_v, exp_v, resto_v)
        m_sup = vals_v[0]
        m_inf = vals_v[-1]
        vaos_v = [vals_v[k] for k in range(1, len(vals_v) - 1)]

        # --- Coordenadas x de cada coluna ---
        x_colunas = []
        x = m_esq
        for c in range(n_colunas):
            x_colunas.append(x)
            x += larguras_colunas[c]
            if c < n_colunas - 1:
                x += vaos_h[c]

        # --- Coordenadas y de cada linha ---
        y_linhas = []
        y = m_sup
        for r in range(n_linhas):
            y_linhas.append(y)
            y += alturas_linhas[r]
            if r < n_linhas - 1:
                y += vaos_v[r]

        celulas = []
        for i, (lin, col) in enumerate(atribuicao):
            celulas.append({
                "participante": i,
                "linha": lin,
                "coluna": col,
                "x": x_colunas[col],
                "y": y_linhas[lin],
                "largura": larguras_colunas[col],
                "altura": alturas_linhas[lin],
            })

        return {
            "fallback": False,
            "formacao": (n_linhas, n_colunas),
            "celulas": celulas,
            "grade": {
                "larguras_colunas": larguras_colunas,
                "alturas_linhas": alturas_linhas,
                "margem_esq": m_esq,
                "margem_dir": m_dir,
                "margem_sup": m_sup,
                "margem_inf": m_inf,
                "vaos_h": vaos_h,
                "vaos_v": vaos_v,
            },
        }

    # Nenhuma formacao coube: fallback canonico.
    return resultado_vazio


def alinhar_na_celula(conteudo_w, conteudo_h, celula_w, celula_h,
                      alinhamento_h, alinhamento_v):
    """Calcula o deslocamento (dx, dy) do conteudo dentro da celula.

    ``alinhamento_h`` in {inicio, centro, fim}.
    ``alinhamento_v`` in {topo, centro, base}.
    Resto impar em centralizacao vai para o inicio/topo (regra deterministica
    documentada: floor((celula - conteudo) / 2)).
    Nunca devolve deslocamento negativo (conteudo maior que a celula fica em 0).
    """
    livre_w = max(0, celula_w - conteudo_w)
    livre_h = max(0, celula_h - conteudo_h)

    if alinhamento_h == "inicio":
        dx = 0
    elif alinhamento_h == "centro":
        dx = livre_w // 2
    elif alinhamento_h == "fim":
        dx = livre_w
    else:
        raise DistribuicaoMatricialErro(
            "alinhamento_interno.horizontal desconhecido: {0!r}".format(
                alinhamento_h
            )
        )

    if alinhamento_v == "topo":
        dy = 0
    elif alinhamento_v == "centro":
        dy = livre_h // 2
    elif alinhamento_v == "base":
        dy = livre_h
    else:
        raise DistribuicaoMatricialErro(
            "alinhamento_interno.vertical desconhecido: {0!r}".format(
                alinhamento_v
            )
        )

    return dx, dy
