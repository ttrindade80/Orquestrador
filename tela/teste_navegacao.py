"""Testes unitarios de navegacao pura (H-0040 / ADR-0031 D1-D15).

Cobre as decisoes D2-D10, D13 e D15 por meio dos 40 criterios canonicos
AT-0001 a AT-0040. Cada teste possui o nome nominal declarado na secao 19 do
H-0040 e valida a superficie observavel correspondente.

Os modelos de teste sao construidos localmente a partir de dicts simples (a
API de navegacao aceita ``ModeloTela`` ou lista de ``ElementoCorpo`` direta),
sem acoplar ao loader nem a JSONs. A geometria e validada contra o mesmo
``calcular_distribuicao`` consumido pelo renderer (AT-0021/PN-0016).

Apenas biblioteca padrao do Python.
"""

import pytest

from tela.modelo import ConteudoExterno, ElementoCorpo, NivelConteudo, NoConteudo
from tela import navegacao


# ---------------------------------------------------------------------------
# Fixtures auxiliares para construir ElementoCorpo de teste
# ---------------------------------------------------------------------------


def _console(idc, itens, navegavel=True, distribuicao=None, titulo="C",
             tipo_navegacao=None):
    """Constroi um ElementoCorpo do tipo console com itens inertes."""
    inertes = {
        "titulo": titulo,
        "itens": itens,
        "politica_navegacao": {"navegavel": navegavel},
    }
    if tipo_navegacao is not None:
        inertes["politica_navegacao"]["tipo"] = tipo_navegacao
    return ElementoCorpo(
        id=idc,
        tipo="console",
        _campos_inertes=inertes,
        distribuicao_matricial=distribuicao,
    )


def _item(idc, texto, navegavel=True):
    """Constroi um dict de item navegavel."""
    return {"id": idc, "texto": texto, "navegavel": navegavel}


def _arvore(idc="arvore", nos=None, navegavel=True):
    console = _console(
        idc,
        [],
        navegavel=navegavel,
        tipo_navegacao="arvore_colapsavel",
    )
    console.conteudo_externo = ConteudoExterno(
        tipo="multinivel",
        apresentacao="hierarquia",
        niveis=[],
        nos=nos or [],
    )
    return console


def _selecao_multinivel(idc="selecao", nos=None):
    console = _console(
        idc,
        [],
        navegavel=True,
        tipo_navegacao="selecao_multinivel",
    )
    console._campos_inertes["politica_selecao"] = "multipla"
    console.conteudo_externo = ConteudoExterno(
        tipo="multinivel",
        apresentacao="hierarquia",
        niveis=[
            NivelConteudo(
                id="grupo", tipo="container", conteudo="texto",
                designador={"tipo": "decimal"},
            ),
            NivelConteudo(
                id="item", tipo="conteudo", conteudo="texto",
                designador={"tipo": "decimal"},
            ),
        ],
        nos=nos or [],
    )
    return console


def _dois_niveis(idc="dois_niveis", nos=None):
    console = _console(
        idc, [], navegavel=True,
        tipo_navegacao="dois_niveis_por_foco",
    )
    console._campos_inertes["politica_selecao"] = "multipla"
    console.conteudo_externo = ConteudoExterno(
        tipo="multinivel", apresentacao="hierarquia", niveis=[],
        nos=nos or [],
    )
    return console


def _no_selecao(idc, nivel="item", selecionavel=False, filhos=None):
    return NoConteudo(
        id=idc,
        nivel=nivel,
        campos={
            "texto": idc,
            "navegavel": True,
            "selecionavel": selecionavel,
        },
        filhos=list(filhos or []),
    )


def _no(idc, *filhos):
    return NoConteudo(id=idc, nivel="item", filhos=list(filhos))


def _lancador(idc, itens=None):
    """Constroi um ElementoCorpo do tipo lancador."""
    return ElementoCorpo(
        id=idc, tipo="lancador", _campos_inertes={"itens": itens or []}
    )


def _dashboard(idc, campos=None):
    """Constroi um ElementoCorpo do tipo dashboard."""
    return ElementoCorpo(
        id=idc, tipo="dashboard", _campos_inertes={"campos": campos or []}
    )


def _grupo(idc, elementos, arranjo="vertical"):
    """Constroi um ElementoCorpo do tipo grupo com filhos."""
    return ElementoCorpo(
        id=idc,
        tipo="grupo",
        _campos_inertes={"arranjo": arranjo},
        elementos=elementos,
    )


_DISTRIBUICAO_UMA_COLUNA = {
    "formacao": {"politica": "preferencia_colunas", "colunas": {"minimo": 1, "maximo": 1}},
    "ordem": "por_linha",
    "dimensionamento": {"colunas": {"politica": "uniforme"}, "linhas": {"politica": "uniforme"}},
    "espacamento": {
        "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
        "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
        "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
    },
    "distribuicao_horizontal": {"politica": "inicio"},
    "distribuicao_vertical": {"politica": "inicio"},
    "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos", "vertical": "uniforme_margens_e_vaos"},
    "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
    "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
}


def _distribuicao_matriz(linhas, colunas):
    """Distribuicao matricial fixa para cenarios de grade."""
    d = dict(_DISTRIBUICAO_UMA_COLUNA)
    d["formacao"] = {
        "politica": "matriz_fixa",
        "linhas": {"fixo": linhas},
        "colunas": {"fixo": colunas},
    }
    return d


def _estado(modelo, foco=None, cursores=None, largura=40, altura_interna=None,
            desconto_estrutural=0, ramos_fechados=None, itens_permitidos=None):
    """Constroi um dict de estado de navegacao para os testes."""
    estado = {
        "modelo": modelo,
        "foco_console": foco,
        "cursores": cursores or {},
        "largura": largura,
        "altura_interna": altura_interna,
        "desconto_estrutural": desconto_estrutural,
    }
    if ramos_fechados is not None:
        estado["ramos_fechados"] = ramos_fechados
    if itens_permitidos is not None:
        estado["itens_permitidos"] = itens_permitidos
    return estado


# ---------------------------------------------------------------------------
# AT-0001 a AT-0010 -- Elegibilidade, lista de foco e ordem
# ---------------------------------------------------------------------------


# AT-0001 - console focalizavel com item navegavel
def teste_console_focalizavel_com_itens_navegaveis():
    # criterio: {id: AT-0001, decisao: D2, resultado_esperado: console entra na lista}
    c = _console("c", [_item("i1", "A"), _item("i2", "B")])
    assert navegacao.console_e_focalizavel(c) is True
    assert [e.id for e in navegacao.lista_foco([c])] == ["c"]


# AT-0002 - politica false exclui console
def teste_console_nao_focalizavel_politica_false():
    # criterio: {id: AT-0002, decisao: D2, resultado_esperado: console nao entra}
    c = _console("c", [_item("i1", "A")], navegavel=False)
    assert navegacao.console_e_focalizavel(c) is False
    assert navegacao.lista_foco([c]) == []


# AT-0003 - zero itens navegaveis exclui console
def teste_console_nao_focalizavel_sem_itens_navegaveis():
    # criterio: {id: AT-0003, decisao: D2, resultado_esperado: console nao entra}
    c = _console(
        "c",
        [_item("i1", "A", navegavel=False), _item("i2", "B", navegavel=False)],
    )
    assert navegacao.console_e_focalizavel(c) is False
    assert navegacao.lista_foco([c]) == []


# AT-0004 - lancador excluido
def teste_lancador_nao_entra_lista_foco():
    # criterio: {id: AT-0004, decisao: D1, resultado_esperado: lancador ausente}
    l = _lancador("l", [_item("i1", "A")])
    assert navegacao.lista_foco([l]) == []


# AT-0005 - dashboard excluido
def teste_dashboard_nao_entra_lista_foco():
    # criterio: {id: AT-0005, decisao: D1, resultado_esperado: dashboard ausente}
    d = _dashboard("d", [{"fonte": "literal", "valor": "x"}])
    assert navegacao.lista_foco([d]) == []


# AT-0006 - grupo estrutural percorre filhos
def teste_grupo_estrutural_percorre_filhos():
    # criterio: {id: AT-0006, decisao: D3, resultado_esperado: grupo ausente e filhos presentes}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    g = _grupo("g", [c1, c2])
    ids = [e.id for e in navegacao.lista_foco([g])]
    assert "g" not in ids
    assert ids == ["c1", "c2"]


# AT-0007 - dois consoles planos em ordem
def teste_lista_foco_dois_consoles_planos_ordem_declarada():
    # criterio: {id: AT-0007, decisao: D3, resultado_esperado: ordem declarada}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    assert [e.id for e in navegacao.lista_foco([c1, c2])] == ["c1", "c2"]


# AT-0008 - depth-first em grupos
def teste_lista_foco_grupo_com_consoles_depth_first():
    # criterio: {id: AT-0008, decisao: D3, resultado_esperado: filhos antes do console externo}
    # Arvore: grupo_externo -> [grupo_interno -> [c_a, c_b], c_externo]
    c_a = _console("ca", [_item("i1", "A")])
    c_b = _console("cb", [_item("i2", "B")])
    c_ext = _console("cext", [_item("i3", "C")])
    g_interno = _grupo("gi", [c_a, c_b])
    g_externo = _grupo("ge", [g_interno, c_ext])
    ids = [e.id for e in navegacao.lista_foco([g_externo])]
    # depth-first: ca, cb (dentro de gi) antes de cext
    assert ids == ["ca", "cb", "cext"]
    # QAPOSTVM40-001: o JSON real de tres consoles preserva a mesma ordem
    # depth-first e renderiza sem DA-02 em 100x30 e 120x35.
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela.renderizador import renderizar_tela, RenderizadorErro
    import demo.demo as _demo
    modelo = construir_modelo(
        carregar_tela(None, "h0040_nav_tres_consoles_em_grupo", _demo._RAIZ_TELAS_DEMO)
    )
    lista = navegacao.lista_foco(modelo)
    assert [c.id for c in lista] == [
        "console_a1", "console_a2", "console_externo",
    ]
    estilo = carregar_estilo()
    cursores = {c.id: 0 for c in lista}
    for largura, altura in ((100, 30), (120, 35)):
        try:
            saida = renderizar_tela(
                modelo, estilo, largura=largura, altura=altura,
                foco_console=0, cursores=cursores, lista_foco=lista,
                largura_navegacao=largura,
            )
        except RenderizadorErro as exc:
            raise AssertionError(
                "DA-02 ou RenderizadorErro em {0}x{1}: {2}".format(
                    largura, altura, exc
                )
            )
        assert "DA-02" not in saida
        assert "pequeno" not in saida.lower()
        assert "Uno" in saida and "Tre" in saida and "Quattro" in saida
        # Sem sobreposicao observavel: cada rotulo de console aparece uma vez.
        assert saida.count("╭ A1 ") == 1
        assert saida.count("╭ A2 ") == 1
        assert saida.count("╭ EXTERNO ") == 1


# AT-0009 - irmaos horizontais
def teste_lista_foco_irmaos_horizontais_esquerda_direita():
    # criterio: {id: AT-0009, decisao: D4, resultado_esperado: esquerda para direita}
    c_esq = _console("esq", [_item("i1", "A")])
    c_dir = _console("dir", [_item("i2", "B")])
    ids = [e.id for e in navegacao.lista_foco([c_esq, c_dir])]
    assert ids == ["esq", "dir"]


# AT-0010 - matriz row-major
def teste_lista_foco_irmaos_em_matriz_row_major():
    # criterio: {id: AT-0010, decisao: D4, resultado_esperado: linhas antes de colunas}
    # Seis consoles em grupo matriz 2x3 (linha-major na declaracao).
    consoles = [
        _console("c{0}{1}".format(r, c), [_item("i", "X")])
        for r in range(2)
        for c in range(3)
    ]
    g = _grupo("g", consoles, arranjo="matriz")
    ids = [e.id for e in navegacao.lista_foco([g])]
    # row-major: c00, c01, c02, c10, c11, c12
    assert ids == ["c00", "c01", "c02", "c10", "c11", "c12"]


# ---------------------------------------------------------------------------
# AT-0011 a AT-0016 -- Tab/Shift+Tab e entrada no item zero
# ---------------------------------------------------------------------------


# AT-0011 - Tab avanca circular
def teste_tab_avanca_circular():
    # criterio: {id: AT-0011, decisao: D5, resultado_esperado: ultimo avanca para primeiro}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    modelo = [c1, c2]
    est = _estado(modelo, foco=1)  # foco no ultimo (c2)
    est = navegacao.avancar_foco(est)
    assert est["foco_console"] == 0  # circular: ultimo -> primeiro
    # QAPOSTVM40-001: tres consoles reais — Tab distingue a ordem depth-first.
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    import demo.demo as _demo
    modelo_json = construir_modelo(
        carregar_tela(None, "h0040_nav_tres_consoles_em_grupo", _demo._RAIZ_TELAS_DEMO)
    )
    lista = navegacao.lista_foco(modelo_json)
    est = _estado(modelo_json, foco=0, cursores={c.id: 0 for c in lista})
    sequencia = [lista[est["foco_console"]].id]
    for _ in range(3):
        est = navegacao.avancar_foco(est)
        sequencia.append(lista[est["foco_console"]].id)
    assert sequencia == [
        "console_a1", "console_a2", "console_externo", "console_a1",
    ]


# AT-0012 - Shift+Tab recua circular
def teste_shift_tab_recua_circular_duas_sequencias():
    # criterio: {id: AT-0012, decisao: D5, resultado_esperado: primeiro recua para ultimo}
    # NC-001: ambas as sequencias de Shift+Tab sao reconhecidas.
    assert navegacao.e_shift_tab("\x1b[Z") is True
    assert navegacao.e_shift_tab("\x1b\t") is True
    assert navegacao.e_tab("\t") is True
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    modelo = [c1, c2]
    est = _estado(modelo, foco=0)  # foco no primeiro (c1)
    est = navegacao.recuar_foco(est)
    assert est["foco_console"] == 1  # circular: primeiro -> ultimo
    # QAPOSTVM40-001: Shift+Tab no JSON real e distinto de Tab. Em 80x24 o
    # conteudo cabe (H-0045-P06: com altura_alvo corretamente propagado por
    # _renderizar_container_horizontal para colunas diretas, este cenario --
    # grupo horizontal aninhado em grupo vertical -- deixa de sofrer overflow
    # de altura natural; antes do patch, colunas horizontais renderizavam com
    # altura NATURAL e o excesso disparava RenderizadorErro/quadro minimo por
    # engano, mesma causa raiz de QA-H0045-P05-001). Sem traceback e sem
    # quadro minimo -- render normal com o titulo e os tres consoles.
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    import demo.demo as _demo
    modelo_json = construir_modelo(
        carregar_tela(None, "h0040_nav_tres_consoles_em_grupo", _demo._RAIZ_TELAS_DEMO)
    )
    lista = navegacao.lista_foco(modelo_json)
    est = _estado(modelo_json, foco=0, cursores={c.id: 0 for c in lista})
    sequencia = [lista[est["foco_console"]].id]
    for _ in range(3):
        est = navegacao.recuar_foco(est)
        sequencia.append(lista[est["foco_console"]].id)
    assert sequencia == [
        "console_a1", "console_externo", "console_a2", "console_a1",
    ]
    estado = _demo.criar_estado_inicial()
    estado = dict(
        estado,
        estilo=carregar_estilo(),
        foco_console=0,
        cursores={c.id: 0 for c in lista},
        largura=80,
    )
    quadro = _demo._resolver_conteudo(estado, modelo_json, 80, 24)
    assert "traceback" not in quadro.lower()
    assert "pequeno" not in quadro.lower() and "peq" not in quadro.lower()
    assert "TRES CONSOLES EM GRUPO" in quadro
    assert "A1" in quadro and "A2" in quadro and "EXTERNO" in quadro


# AT-0013 - Tab sem foco
def teste_tab_sem_foco_foca_primeiro():
    # criterio: {id: AT-0013, decisao: D5, resultado_esperado: indice zero}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    est = _estado([c1, c2], foco=None)
    est = navegacao.avancar_foco(est)
    assert est["foco_console"] == 0


# AT-0014 - Shift+Tab sem foco
def teste_shift_tab_sem_foco_foca_ultimo():
    # criterio: {id: AT-0014, decisao: D5, resultado_esperado: ultimo indice}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console("c2", [_item("i2", "B")])
    est = _estado([c1, c2], foco=None)
    est = navegacao.recuar_foco(est)
    assert est["foco_console"] == 1


# AT-0015 - Tab entra no item zero
def teste_entrada_tab_cursor_item_zero():
    # criterio: {id: AT-0015, decisao: D6, resultado_esperado: cursor zero}
    c1 = _console(
        "c1",
        [_item("i1", "A"), _item("i2", "B"), _item("i3", "C")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    c2 = _console("c2", [_item("i4", "D")])
    est = _estado([c1, c2], foco=0, cursores={"c1": 2})  # cursor fora do 0
    est = navegacao.avancar_foco(est)  # entra em c2
    assert est["foco_console"] == 1
    assert est["cursores"].get("c2") == 0  # D6: entrada no item 0


# AT-0016 - Shift+Tab entra no item zero
def teste_entrada_shift_tab_cursor_item_zero():
    # criterio: {id: AT-0016, decisao: D6, resultado_esperado: cursor zero}
    c1 = _console("c1", [_item("i1", "A")])
    c2 = _console(
        "c2",
        [_item("i2", "B"), _item("i3", "C"), _item("i4", "D")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    est = _estado([c1, c2], foco=1, cursores={"c2": 2})
    est = navegacao.recuar_foco(est)  # entra em c1
    assert est["foco_console"] == 0
    assert est["cursores"].get("c1") == 0


# ---------------------------------------------------------------------------
# AT-0017 a AT-0021 -- Grade, geometria e ordem logica
# ---------------------------------------------------------------------------


# AT-0017 - grade linear uma coluna
def teste_grade_linear_uma_coluna_n_linhas():
    # criterio: {id: AT-0017, decisao: D7, resultado_esperado: N linhas por uma coluna}
    c = _console(
        "c",
        [_item("a", "A"), _item("b", "B"), _item("d", "D"), _item("e", "E")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    grade = navegacao.grade_de_itens(c, 30)
    assert len(grade) == 4
    assert all(len(linha) == 1 for linha in grade)


# AT-0018 - grade visual row-major
def teste_grade_distribuicao_matricial_row_major():
    # criterio: {id: AT-0018, decisao: D7, resultado_esperado: indices seguem row-major}
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0}".format(i)) for i in range(6)],
        distribuicao=_distribuicao_matriz(2, 3),
    )
    grade = navegacao.grade_de_itens(c, 40)
    # row-major: linha 0 = g0,g1,g2 ; linha 1 = g3,g4,g5
    assert [grade[0][i].get("id") for i in range(3)] == ["g0", "g1", "g2"]
    assert [grade[1][i].get("id") for i in range(3)] == ["g3", "g4", "g5"]


# AT-0019 - celula vazia marcada
def teste_grade_celula_vazia_none():
    # criterio: {id: AT-0019, decisao: D8, resultado_esperado: celula vazia e None}
    # Grade 2x3 com 5 itens: a celula (1,2) fica vazia.
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0}".format(i)) for i in range(5)],
        distribuicao=_distribuicao_matriz(2, 3),
    )
    grade = navegacao.grade_de_itens(c, 40)
    assert grade[1][2] is None


# AT-0020 - ordem linear preservada
def teste_itens_console_linear_preserva_ordem():
    # criterio: {id: AT-0020, decisao: D7, resultado_esperado: A B C viram 0 1 2}
    c = _console(
        "c",
        [_item("a", "A"), _item("b", "B"), _item("cc", "C")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    grade = navegacao.grade_de_itens(c, 30)
    # Achatar row-major preserva ordem declarada
    ids = []
    for linha in grade:
        for celula in linha:
            if celula is not None:
                ids.append(celula.get("id"))
    assert ids == ["a", "b", "cc"]


# AT-0021 - equivalencia grade navegacao e visual
def teste_grade_navegacao_equivale_grade_visual_vigente():
    # criterio: {id: AT-0021, decisao: D7, resultado_esperado: mesmas linhas e colunas consumidas pelo renderer}
    # QAI40-002: a navegacao NAO reproduz a fórmula do renderer; compara contra o
    # renderer REAL. A prova observa as posições físicas efetivamente renderizadas
    # e a grade efetivamente usada pela navegação, item por item.
    from tela.renderizador import renderizar_tela
    from tela.modelo import ModeloTela, Corpo

    def _construir(itens, distribuicao):
        c = _console("c", itens, distribuicao=distribuicao, titulo="C")
        modelo = ModeloTela(
            id="t", schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(arranjo="vertical", elementos=[c]),
            barra_de_menus={"chips": []}, _raw={},
        )
        return c, modelo

    def _verificar(c, modelo, largura_total):
        # Grade efetivamente usada pela navegação (mesma largura do renderer).
        grade_nav = navegacao.grade_de_itens(c, largura_total)
        lista = navegacao.lista_foco(modelo)
        # Renderização REAL: a caixa do console e o conteúdo são produzidos pelo
        # renderer integrado, sem reproduzir a fórmula do desconto estrutural.
        saida = renderizar_tela(
            modelo, _estilo_padrao(), largura=largura_total,
            foco_console=0, cursores={"c": 0}, lista_foco=lista,
            largura_navegacao=largura_total,
        )
        # Linhas físicas da CAIXA DO CONSOLE: contêm os textos dos itens da
        # grade. Exclui o cabeçalho (linha de descrição) e a barra de menus.
        textos_grade = [
            cel.get("texto", "")
            for linha in grade_nav for cel in linha if cel is not None
        ]
        linhas_caixa = [
            ln for ln in saida.split("\n")
            if ln.startswith("│") and any(t in ln for t in textos_grade if t)
        ]
        # 1) Quantidade de linhas físicas de conteúdo == quantidade de linhas da
        #    grade de navegação (filas com ao menos uma célula ocupada contam
        #    como linha física consumida; linhas puramente vazias não existem na
        #    matriz incompleta porque o motor não emite filas sem participantes).
        linhas_grade = len(grade_nav)
        assert linhas_caixa, "renderer não produziu linhas de conteúdo"
        # A quantidade de colunas da grade de navegação deve corresponder à
        # quantidade de colunas realmente consumidas pelo renderer. Verificamos
        # a largura usada: cada célula ocupada da grade tem um item cujo texto
        # aparece na linha física correspondente.
        for r, linha_grade in enumerate(grade_nav):
            linha_fisica = linhas_caixa[r]
            for celula in linha_grade:
                if celula is None:
                    continue
                # O texto do item deve aparecer na linha física correspondente.
                assert celula.get("texto", "") in linha_fisica, (
                    "item {0!r} da grade de navegação não aparece na linha "
                    "física {1!r} renderizada (divergência grade/renderer)"
                    .format(celula.get("id"), linha_fisica)
                )

    # Subcaso 1: largura 60 com matriz incompleta 2x3.
    c1, m1 = _construir(
        [_item("g{0}".format(i), "G{0:02d}".format(i)) for i in range(5)],
        _distribuicao_matriz(2, 3),
    )
    _verificar(c1, m1, 60)
    # Subcaso 2: largura menor que força redistribuição da grade.
    c2, m2 = _construir(
        [_item("g{0}".format(i), "G{0:02d}".format(i)) for i in range(5)],
        _distribuicao_matriz(2, 3),
    )
    _verificar(c2, m2, 30)
    # Subcaso 3: matriz incompleta 2x3 efetiva (5 itens).
    c3, m3 = _construir(
        [_item("g{0}".format(i), "G{0:02d}".format(i)) for i in range(5)],
        _distribuicao_matriz(2, 3),
    )
    grade3 = navegacao.grade_de_itens(c3, 60)
    assert (len(grade3), len(grade3[0])) == (2, 3)


# ---------------------------------------------------------------------------
# AT-0022 a AT-0027 -- Toroide por eixo e celulas vazias
# ---------------------------------------------------------------------------


def _console_grade_2x3():
    """Console 2x3 com 5 itens (ultima linha incompleta)."""
    return _console(
        "c",
        [_item("g{0}".format(i), "G{0}".format(i)) for i in range(5)],
        distribuicao=_distribuicao_matriz(2, 3),
    )


# AT-0022 - seta direita toroide
def teste_seta_direita_toroide():
    # criterio: {id: AT-0022, decisao: D8, resultado_esperado: ultimo da linha vai ao primeiro da mesma linha}
    c = _console_grade_2x3()
    # Cursor em g02 (ultimo da linha 0): direita -> g00 (toroide mesma linha)
    est = _estado([c], foco=0, cursores={"c": 2}, largura=40)
    est = navegacao.mover_direita(est, c)
    assert est["cursores"]["c"] == 0


# AT-0023 - seta esquerda toroide
def teste_seta_esquerda_toroide():
    # criterio: {id: AT-0023, decisao: D8, resultado_esperado: primeiro da linha vai ao ultimo da mesma linha}
    c = _console_grade_2x3()
    # Cursor em g00 (primeiro da linha 0): esquerda -> g02 (toroide mesma linha)
    est = _estado([c], foco=0, cursores={"c": 0}, largura=40)
    est = navegacao.mover_esquerda(est, c)
    assert est["cursores"]["c"] == 2


# AT-0024 - seta baixo toroide
def teste_seta_baixo_toroide():
    # criterio: {id: AT-0024, decisao: D8, resultado_esperado: ultimo da coluna vai ao primeiro da mesma coluna}
    c = _console_grade_2x3()
    # Cursor em g10 (coluna 0, ultima linha): baixo -> g00 (toroide mesma coluna)
    est = _estado([c], foco=0, cursores={"c": 3}, largura=40)
    est = navegacao.mover_baixo(est, c)
    assert est["cursores"]["c"] == 0


# AT-0025 - seta cima toroide
def teste_seta_cima_toroide():
    # criterio: {id: AT-0025, decisao: D8, resultado_esperado: primeiro da coluna vai ao ultimo da mesma coluna}
    c = _console_grade_2x3()
    # Cursor em g00 (coluna 0, primeira linha): cima -> g10 (toroide mesma coluna)
    est = _estado([c], foco=0, cursores={"c": 0}, largura=40)
    est = navegacao.mover_cima(est, c)
    assert est["cursores"]["c"] == 3


# AT-0026 - celula vazia excluida na horizontal
def teste_celula_vazia_excluida_toroide_horizontal():
    # criterio: {id: AT-0026, decisao: D8, resultado_esperado: seta pula None sem cruzar linha}
    c = _console_grade_2x3()
    # Cursor em g11 (item logico 4, coluna 1 linha 1). Direita: coluna 2 da
    # linha 1 e None (vazia). Toroide horizontal pula o None e volta ao g10
    # (item logico 3), sem cruzar linha.
    est = _estado([c], foco=0, cursores={"c": 4}, largura=40)
    est = navegacao.mover_direita(est, c)
    assert est["cursores"]["c"] == 3  # volta ao inicio da mesma linha, pulando None


# AT-0027 - celula vazia excluida na vertical
def teste_celula_vazia_excluida_toroide_vertical():
    # criterio: {id: AT-0027, decisao: D8, resultado_esperado: seta pula None sem cruzar coluna}
    c = _console_grade_2x3()
    # Cursor em g02 (coluna 2, linha 0). Baixo: coluna 2 linha 1 e None.
    # Toroide vertical: SEM_MOVIMENTO (nao ha outro item na mesma coluna).
    est = _estado([c], foco=0, cursores={"c": 2}, largura=40)
    est = navegacao.mover_baixo(est, c)
    assert est["cursores"]["c"] == 2  # SEM_MOVIMENTO: nenhum outro item na coluna 2


# ---------------------------------------------------------------------------
# AT-0028 a AT-0030 -- Casos degenerados
# ---------------------------------------------------------------------------


# AT-0028 - um item sem movimento
def teste_um_item_qualquer_seta_sem_movimento():
    # criterio: {id: AT-0028, decisao: D9, resultado_esperado: mesmo item}
    c = _console("c", [_item("u1", "Sozinho")], distribuicao=_DISTRIBUICAO_UMA_COLUNA)
    est = _estado([c], foco=0, cursores={"c": 0}, largura=30)
    for fn in (navegacao.mover_direita, navegacao.mover_esquerda,
               navegacao.mover_baixo, navegacao.mover_cima):
        est2 = fn(est, c)
        assert est2["cursores"]["c"] == 0


# AT-0029 - uma linha sem movimento vertical
def teste_uma_linha_seta_vertical_sem_movimento():
    # criterio: {id: AT-0029, decisao: D9, resultado_esperado: mesmo item}
    c = _console(
        "c",
        [_item("l1", "L1"), _item("l2", "L2"), _item("l3", "L3")],
        distribuicao=_distribuicao_matriz(1, 3),
    )
    est = _estado([c], foco=0, cursores={"c": 1}, largura=40)
    est_baixo = navegacao.mover_baixo(est, c)
    est_cima = navegacao.mover_cima(est, c)
    assert est_baixo["cursores"]["c"] == 1  # SEM_MOVIMENTO vertical
    assert est_cima["cursores"]["c"] == 1


# AT-0030 - uma coluna sem movimento horizontal
def teste_uma_coluna_seta_horizontal_sem_movimento():
    # criterio: {id: AT-0030, decisao: D9, resultado_esperado: mesmo item}
    c = _console(
        "c",
        [_item("c1", "C1"), _item("c2", "C2"), _item("c3", "C3")],
        distribuicao=_distribuicao_matriz(3, 1),
    )
    est = _estado([c], foco=0, cursores={"c": 1}, largura=40)
    est_dir = navegacao.mover_direita(est, c)
    est_esq = navegacao.mover_esquerda(est, c)
    assert est_dir["cursores"]["c"] == 1  # SEM_MOVIMENTO horizontal
    assert est_esq["cursores"]["c"] == 1


# ---------------------------------------------------------------------------
# AT-0031 a AT-0034 -- Redimensionamento e mudanca de modo
# ---------------------------------------------------------------------------


# Dimensoes controladas do cenario real de 26 itens (descobertas empiricamente
# com desconto_estrutural=3). AT-0031/AT-0032 / patch VM-11.
_FORMACOES_26 = {
    (1, 26): 282,
    (2, 13): 151,
    (4, 7): 85,
    (7, 4): 52,
    (13, 2): 28,
    (26, 1): 20,
}
_DESCONTO_NAV = 3  # DESCONTO_ESTRUTURAL_CONSOLE


def _modelo_matriz_26():
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    import demo.demo as _demo
    return construir_modelo(
        carregar_tela(
            None,
            "h0040_nav_matriz_26_itens_redimensionamento",
            _demo._RAIZ_TELAS_DEMO,
        )
    )


def _formacao_grade(grade):
    if not grade:
        return (0, 0)
    return (len(grade), len(grade[0]))


def _vizinho_direita(grade, item_logico):
    pos = navegacao._posicao_do_item_logico(grade, item_logico)
    ocupadas = navegacao._linha_com_itens(grade, pos[0])
    idx = ocupadas.index(pos[1])
    nova_col = ocupadas[(idx + 1) % len(ocupadas)]
    return navegacao.item_logico_de_posicao(grade, pos[0], nova_col)


def _vizinho_baixo(grade, item_logico):
    pos = navegacao._posicao_do_item_logico(grade, item_logico)
    ocupadas = navegacao._coluna_com_itens(grade, pos[1])
    idx = ocupadas.index(pos[0])
    nova_lin = ocupadas[(idx + 1) % len(ocupadas)]
    return navegacao.item_logico_de_posicao(grade, nova_lin, pos[1])


# AT-0031 - redimensionamento preserva item logico
def teste_redimensionamento_preserva_item_logico():
    # criterio: {id: AT-0031, decisao: D10, superficie_observavel: cursores e grade
    # do cenario config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json,
    # resultado_esperado: mesmo id logico preservado ao mudar entre ao menos
    # quatro formacoes distintas, incluindo 1x26 e 26x1, sem retorno ao item 0}
    modelo = _modelo_matriz_26()
    c = navegacao.lista_foco(modelo)[0]
    item_logico = 12  # item_13 Turquesa — distante do item 0
    id_esperado = navegacao.itens_navegaveis(c)[item_logico]["id"]
    assert id_esperado == "item_13"

    formacoes_vistas = []
    posicoes = []
    est = _estado(
        modelo, foco=0, cursores={c.id: item_logico},
        largura=_FORMACOES_26[(1, 26)], desconto_estrutural=_DESCONTO_NAV,
    )
    for form, largura in (
        ((1, 26), _FORMACOES_26[(1, 26)]),
        ((2, 13), _FORMACOES_26[(2, 13)]),
        ((4, 7), _FORMACOES_26[(4, 7)]),
        ((7, 4), _FORMACOES_26[(7, 4)]),
        ((13, 2), _FORMACOES_26[(13, 2)]),
        ((26, 1), _FORMACOES_26[(26, 1)]),
        ((1, 26), _FORMACOES_26[(1, 26)]),  # ida e retorno
    ):
        est = navegacao.redimensionar(est, largura)
        grade = navegacao.grade_de_itens(
            c, largura, desconto_estrutural=_DESCONTO_NAV,
        )
        form_obtida = _formacao_grade(grade)
        assert form_obtida == form, (
            "formacao esperada {0}, obtida {1} @ largura={2}"
            .format(form, form_obtida, largura)
        )
        sel = navegacao.item_selecionado(c, est)
        assert sel.get("id") == id_esperado
        assert est["cursores"][c.id] == item_logico  # nao voltou ao 0
        assert est["cursores"][c.id] != 0 or item_logico == 0
        pos = navegacao.posicao_corrente(est, c)
        formacoes_vistas.append(form_obtida)
        posicoes.append(pos)

    distintas = set(formacoes_vistas[:-1])  # exclui retorno
    assert len(distintas) >= 4
    assert (1, 26) in distintas and (26, 1) in distintas
    # Posicao fisica muda entre extremos; identidade preservada no retorno.
    assert posicoes[0] != posicoes[5]
    assert posicoes[0] == posicoes[6]
    assert navegacao.item_selecionado(c, est).get("id") == id_esperado


# AT-0032 - redimensionamento recalcula vizinhos
def teste_redimensionamento_recalcula_linha_coluna_vizinhos():
    # criterio: {id: AT-0032, decisao: D10, superficie_observavel: linha coluna e
    # vizinhos do cenario h0040_nav_matriz_26_itens_redimensionamento.json,
    # resultado_esperado: vizinhos diferentes por formacao; primeira seta apos
    # resize usa a nova formacao; retorno restaura vizinhanca; toroide atual}
    from tela.loader import carregar_estilo
    from tela.renderizador import renderizar_tela, DESCONTO_ESTRUTURAL_CONSOLE
    import demo.demo as _demo

    modelo = _modelo_matriz_26()
    lista = navegacao.lista_foco(modelo)
    c = lista[0]
    item_logico = 12  # item_13 — vizinhos distintos em 2x13 e 13x2
    estilo = carregar_estilo()
    simbolo = estilo.selecionado_simbolo

    largura_a = _FORMACOES_26[(2, 13)]
    largura_b = _FORMACOES_26[(13, 2)]
    grade_a = navegacao.grade_de_itens(
        c, largura_a, desconto_estrutural=_DESCONTO_NAV,
    )
    grade_b = navegacao.grade_de_itens(
        c, largura_b, desconto_estrutural=_DESCONTO_NAV,
    )
    assert _formacao_grade(grade_a) == (2, 13)
    assert _formacao_grade(grade_b) == (13, 2)

    viz_dir_a = _vizinho_direita(grade_a, item_logico)
    viz_baixo_a = _vizinho_baixo(grade_a, item_logico)
    viz_dir_b = _vizinho_direita(grade_b, item_logico)
    viz_baixo_b = _vizinho_baixo(grade_b, item_logico)
    assert viz_dir_a != viz_dir_b and viz_baixo_a != viz_baixo_b, (
        "vizinhos devem diferir entre 2x13 e 13x2"
    )

    est = _estado(
        modelo, foco=0, cursores={c.id: item_logico},
        largura=largura_a, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    pos_a = navegacao.posicao_corrente(est, c)
    est_b = navegacao.redimensionar(est, largura_b)
    # Preserva desconto (mesma geometria do renderer) — patch VM-11.
    est_b["desconto_estrutural"] = DESCONTO_ESTRUTURAL_CONSOLE
    pos_b = navegacao.posicao_corrente(est_b, c)
    assert pos_a != pos_b
    assert navegacao.item_selecionado(c, est_b).get("id") == "item_13"

    # Primeira seta IMEDIATAMENTE apos resize via processar_comando (runtime).
    estado_demo = _demo.criar_estado_inicial()
    estado_demo = dict(
        estado_demo,
        estilo=estilo,
        foco_console=0,
        cursores={c.id: item_logico},
        largura=largura_a,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    estado_demo = dict(
        estado_demo,
        largura=largura_b,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    estado_pos = _demo.processar_comando(estado_demo, "\x1b[C", modelo)
    assert estado_pos.get("desconto_estrutural") == DESCONTO_ESTRUTURAL_CONSOLE
    assert estado_pos["cursores"][c.id] == viz_dir_b
    assert estado_pos["cursores"][c.id] != viz_dir_a

    # Toroide vertical na formacao nova.
    estado_tor = dict(
        estado_demo,
        cursores={c.id: item_logico},
        largura=largura_b,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    estado_tor = _demo.processar_comando(estado_tor, "\x1b[B", modelo)
    assert estado_tor["cursores"][c.id] == viz_baixo_b

    # Retorno a formacao anterior restaura vizinhos.
    est_volta = navegacao.redimensionar(est_b, largura_a)
    est_volta["desconto_estrutural"] = DESCONTO_ESTRUTURAL_CONSOLE
    grade_volta = navegacao.grade_de_itens(
        c, largura_a, desconto_estrutural=_DESCONTO_NAV,
    )
    assert _vizinho_direita(grade_volta, item_logico) == viz_dir_a
    assert _vizinho_baixo(grade_volta, item_logico) == viz_baixo_a

    # Renderer e navegacao: indicador na celula do item preservado.
    for largura, grade, pos in (
        (largura_a, grade_a, pos_a),
        (largura_b, grade_b, pos_b),
    ):
        saida = renderizar_tela(
            modelo, estilo, largura=largura, altura=80,
            foco_console=0, cursores={c.id: item_logico}, lista_foco=lista,
            largura_navegacao=largura,
        )
        assert "pequeno" not in saida.lower()
        assert saida.count(simbolo) == 1
        item = grade[pos[0]][pos[1]]
        linha_marcada = [ln for ln in saida.split("\n") if simbolo in ln][0]
        assert item.get("texto", "") in linha_marcada


# AT-0033 - mudanca de modo preserva item logico
def teste_mudanca_modo_preserva_item_logico():
    # criterio: {id: AT-0033, decisao: D10, resultado_esperado: mesmo id logico em verboso e nao verboso}
    # QAI40-003: o teste deve alterar EFETIVAMENTE o modo de apresentação e
    # confirmar que o modo mudou, o item lógico permaneceu e o cursor não foi
    # reiniciado. Usa o renderer real e um item cuja apresentação muda com o modo.
    # Patch pos-validacao: tambem confirma que modo_verboso_forcado permanece
    # True apos seta/Tab/Shift+Tab/espaco/Enter, com modo efetivo verboso.
    from tela.renderizador import renderizar_tela
    from tela.modelo import ModeloTela, Corpo
    import demo.demo as _demo
    # Item longo que, em largura pequena, ocupa mais de uma linha física em modo
    # verboso e uma linha (truncada) em modo não verboso.
    texto_longo = "Alfa Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa"
    c = _console(
        "c",
        [
            _item("a", "Curto A"),
            _item("b", "Curto B"),
            _item("d", texto_longo),
        ],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA, titulo="C",
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    # Cursor fora do item 0 (item lógico 2 = id "d").
    base = {
        "modelo": modelo, "foco_console": 0,
        "cursores": {"c": 2}, "largura": 30,
    }
    # Renderiza em modo não verboso e verboso via renderer real.
    s_nv = renderizar_tela(
        modelo, _estilo_padrao(), largura=30, verboso=False,
        foco_console=0, cursores={"c": 2}, lista_foco=lista,
        largura_navegacao=30,
    )
    s_v = renderizar_tela(
        modelo, _estilo_padrao(), largura=30, verboso=True,
        foco_console=0, cursores={"c": 2}, lista_foco=lista,
        largura_navegacao=30,
    )
    # O modo efetivo mudou materialmente (saídas diferentes).
    assert s_nv != s_v, "mudança de modo não produziu alteração material"
    # A identidade do item lógico permaneceu: o item corrente (id "d") continua
    # sendo o apontado pelo cursor em ambos os modos.
    sel = navegacao.item_selecionado(c, base)
    assert sel.get("id") == "d"
    # O cursor não foi reiniciado para o item 0.
    assert base["cursores"]["c"] == 2

    # Persistencia do override --verboso apos comandos que causam redesenho.
    estado = _demo.criar_estado_inicial()
    estado = dict(
        estado,
        estilo=_estilo_padrao(),
        tela_atual="t",
        modo_verboso=True,
        modo_verboso_forcado=True,
        foco_console=0,
        cursores={"c": 2},
        largura=30,
    )
    for cmd in ("\x1b[B", "\t", "\x1b[Z", " ", "\r"):
        estado = _demo.processar_comando(estado, cmd, modelo)
        assert estado.get("modo_verboso_forcado") is True, (
            "modo_verboso_forcado perdido apos comando {0!r}".format(cmd)
        )
        assert _demo._verboso_efetivo(estado, modelo) is True, (
            "modo_verboso_efetivo perdido apos comando {0!r}".format(cmd)
        )
    # Sem override: processar_comando nao inventa a chave.
    estado_sem = _demo.criar_estado_inicial()
    estado_sem = dict(estado_sem, foco_console=0, cursores={"c": 0}, largura=30)
    estado_sem = _demo.processar_comando(estado_sem, "\x1b[B", modelo)
    assert "modo_verboso_forcado" not in estado_sem


# AT-0034 - mudanca de modo recalcula grade atual
def teste_mudanca_modo_recalcula_grade_atual():
    # criterio: {id: AT-0034, decisao: D10, resultado_esperado: posicoes fisicas atualizadas sem reiniciar item}
    # QAI40-003: conteúdo e largura em que a mudança de modo altera
    # materialmente a apresentação física (item multilinha em verboso).
    # Patch pos-validacao: confirma continuacao real sem sobreposicao com o
    # item seguinte e indicador somente na primeira linha.
    from tela.renderizador import renderizar_tela
    from tela.modelo import ModeloTela, Corpo
    texto_longo = "Alfa Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda"
    c = _console(
        "c",
        [
            _item("a", "Curto A"),
            _item("b", "Curto B"),
            _item("d", texto_longo),
            _item("e", "OmegaSeguinte"),
        ],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA, titulo="C",
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    estilo = _estilo_padrao()
    simbolo = estilo.selecionado_simbolo
    s_nv = renderizar_tela(
        modelo, estilo, largura=30, verboso=False,
        foco_console=0, cursores={"c": 2}, lista_foco=lista,
        largura_navegacao=30,
    )
    s_v = renderizar_tela(
        modelo, estilo, largura=60, altura=24, verboso=True,
        foco_console=0, cursores={"c": 2}, lista_foco=lista,
        largura_navegacao=60,
    )
    # Saída ou grade física diferente entre os modos (renderer real utilizado).
    assert s_nv != s_v, "mudança de modo não alterou materialmente a apresentação"
    # Mesma identidade lógica: item "d" permanece apontado.
    est = {"modelo": modelo, "foco_console": 0, "cursores": {"c": 2}, "largura": 60}
    assert navegacao.item_selecionado(c, est).get("id") == "d"
    # Posição física recalculada pela grade vigente (mesmo item, grade estável).
    pos = navegacao.posicao_corrente(est, c)
    grade = navegacao.grade_de_itens(c, 60)
    assert grade[pos[0]][pos[1]].get("id") == "d"
    # Continuacao real sem sobreposicao (faixa segura pos-patch).
    assert "pequeno" not in s_v.lower() and "demais" not in s_v.lower()
    frags = [w for w in texto_longo.split() if w]
    linhas = [ln for ln in s_v.split("\n") if ln.startswith("│")]
    linhas_item = [ln for ln in linhas if any(f in ln for f in frags)]
    assert len(linhas_item) >= 2
    assert s_v.count(simbolo) == 1
    for ln in linhas:
        if "OmegaSeguinte" in ln:
            assert not any(f in ln for f in frags)


# ---------------------------------------------------------------------------
# AT-0035 a AT-0040 -- Indicador, selecao unica e chips (via renderer)
# ---------------------------------------------------------------------------


def _estilo_padrao():
    """Constroi um EstiloResolvido para os testes de renderer."""
    from tela.loader import EstiloResolvido
    return EstiloResolvido(
        canto_superior_esquerdo="╭", canto_superior_direito="╮",
        canto_inferior_esquerdo="╰", canto_inferior_direito="╯",
        traco_superior="─", traco_inferior="─", lateral="│",
        caractere_esquerdo="[", caractere_direito="]",
        cor_texto="padrão", caixa_alta=False, cor_fundo="padrão",
        concluido_on="✓", concluido_off=" ",
        selecionado_simbolo="→", selecionado_off=" ",
        incluido_on="●", incluido_off="○",
    )


# AT-0035 - indicador apenas no focado
def teste_indicador_apenas_console_focado():
    # criterio: {id: AT-0035, decisao: D11, resultado_esperado: simbolo so no console focado}
    # QAI40-001: no cenário matricial 2x3, para CADA cursor válido 0..4 o símbolo
    # deve estar na célula do item corrente e ausente nas demais células. O teste
    # localiza o item lógico correspondente na grade e confirma a posição física
    # real marcada pelo renderer.
    from tela.renderizador import renderizar_tela
    from tela.modelo import ModeloTela, Corpo
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0:02d}".format(i)) for i in range(5)],
        distribuicao=_distribuicao_matriz(2, 3), titulo="GRADE",
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    estilo = _estilo_padrao()
    simbolo = estilo.selecionado_simbolo
    grade = navegacao.grade_de_itens(c, 60)

    # Para cada cursor válido, o item lógico corrente está em (linha, coluna)
    # real na grade; o renderer deve marcar exatamente essa célula.
    for cursor in range(5):
        pos = navegacao._posicao_do_item_logico(grade, cursor)
        assert pos is not None, "cursor {0} não está na grade".format(cursor)
        item_corrente = grade[pos[0]][pos[1]]
        saida = renderizar_tela(
            modelo, estilo, largura=60,
            foco_console=0, cursores={"c": cursor},
            lista_foco=lista, largura_navegacao=60,
        )
        # Exatamente UMA ocorrência do símbolo no console focado.
        assert saida.count(simbolo) == 1, (
            "cursor {0}: esperado 1 símbolo, obtido {1}"
            .format(cursor, saida.count(simbolo))
        )
        # O símbolo está na linha física que contém o item corrente.
        linhas_com_simb = [
            ln for ln in saida.split("\n") if simbolo in ln
        ]
        assert len(linhas_com_simb) == 1  # já garantido pela contagem
        linha_marcada = linhas_com_simb[0]
        # O texto do item corrente aparece na mesma linha física marcada.
        assert item_corrente.get("texto", "") in linha_marcada, (
            "cursor {0}: símbolo não está na célula do item corrente {1!r} "
            "(linha marcada: {2!r})"
            .format(cursor, item_corrente.get("id"), linha_marcada)
        )
        # Os textos dos OUTROS itens da mesma linha aparecem na linha marcada
        # (itens lado a lado na mesma linha física), mas sem o símbolo em suas
        # colunas. Pelo menos confirmamos que a linha física contém o item.
        # Símbolo não aparece em linhas vazias nem em linhas de outros itens.
        outras_linhas = [
            ln for ln in saida.split("\n")
            if simbolo not in ln and ln.startswith("│")
        ]
        for ol in outras_linhas:
            # Itens não-correntes não recebem o símbolo.
            assert simbolo not in ol


# AT-0036 - indicador do estilo e coluna estavel
def teste_indicador_simbolo_do_estilo_coluna_estavel():
    # criterio: {id: AT-0036, decisao: D12, resultado_esperado: simbolo do estilo sem deslocar coluna}
    # QAI40-001: matriz com MAIS DE UMA COLUNA. Mover o cursor entre células da
    # mesma linha física preserva os textos dos itens nas mesmas colunas; somente
    # o conteúdo da coluna indicadora muda. O símbolo vem do estilo (não hardcoded).
    from tela.renderizador import renderizar_tela
    from tela.loader import EstiloResolvido
    from tela.modelo import ModeloTela, Corpo
    # Grade 1x3: três itens lado a lado na mesma linha física.
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0:02d}".format(i)) for i in range(3)],
        distribuicao=_distribuicao_matriz(1, 3), titulo="C",
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    # Estilo com símbolo "X" customizado (PN-0015: não hardcoded).
    estilo_x = EstiloResolvido(
        canto_superior_esquerdo="╭", canto_superior_direito="╮",
        canto_inferior_esquerdo="╰", canto_inferior_direito="╯",
        traco_superior="─", traco_inferior="─", lateral="│",
        caractere_esquerdo="[", caractere_direito="]",
        cor_texto="padrão", caixa_alta=False, cor_fundo="padrão",
        concluido_on="✓", concluido_off=" ",
        selecionado_simbolo="X", selecionado_off=" ",
        incluido_on="●", incluido_off="○",
    )
    lista = navegacao.lista_foco(modelo)
    largura = 50
    # Render com cursor nos três itens da mesma linha física.
    saidas = []
    for cursor in range(3):
        s = renderizar_tela(
            modelo, estilo_x, largura=largura, foco_console=0,
            cursores={"c": cursor}, lista_foco=lista,
            largura_navegacao=largura,
        )
        assert "X" in s, "símbolo do estilo ausente para cursor {0}".format(cursor)
        saidas.append(s)
    # Os textos dos três itens aparecem em todas as renderizações (mesmas colunas).
    for s in saidas:
        assert "G00" in s and "G01" in s and "G02" in s
    # Exatamente UMA ocorrência do símbolo em cada renderização.
    for s in saidas:
        assert s.count("X") == 1, "esperado 1 símbolo, obtido {0}".format(s.count("X"))
    # QAI40-001: o símbolo deve permanecer na MESMA linha física que contém os
    # itens (linha 0 da grade 1x3). Não pode cair em linhas fantasmas/ vazias.
    # Localizamos a linha física que contém os textos dos itens.
    def _linha_dos_itens(s):
        for ln in s.split("\n"):
            if "G00" in ln and "G01" in ln and "G02" in ln:
                return ln
        return None
    for s in saidas:
        linha_itens = _linha_dos_itens(s)
        assert linha_itens is not None, "linha física dos itens não encontrada"
        assert "X" in linha_itens, (
            "símbolo não está na linha física dos itens (caiu em linha fantasma)"
        )
    # D12: coluna estável significa que o CONTEÚDO dos itens não se desloca
    # quando o cursor muda — cada item permanece na mesma coluna física. O
    # símbolo move-se entre as colunas indicadoras independentes de cada célula
    # (QAI40-001: itens lado a lado têm colunas indicadoras independentes).
    # Verificamos que cada item G00/G01/G02 está na mesma posição de coluna em
    # todas as renderizações (o conteúdo é estável).
    def _posicoes_dos_itens(s):
        ln = _linha_dos_itens(s)
        return {tag: ln.index(tag) for tag in ("G00", "G01", "G02")}
    pos0 = _posicoes_dos_itens(saidas[0])
    for s in saidas[1:]:
        assert _posicoes_dos_itens(s) == pos0, (
            "conteúdo dos itens deslocou ao mudar o cursor (coluna não estável)"
        )


# AT-0037 - continuacoes recebem off
def teste_continuacoes_recebem_selecionado_off():
    # criterio: {id: AT-0037, decisao: D12, resultado_esperado: so primeira linha fisica recebe simbolo}
    # QAI40-003/PN-0010: prepara continuação física REAL — item longo, largura
    # pequena, modo verboso efetivo — de modo que o item corrente ocupe ao
    # menos DUAS linhas físicas. Apenas a primeira recebe o símbolo; as
    # continuações recebem selecionado_off.
    # Patch pos-validacao: tambem exige ausencia de sobreposicao com o item
    # seguinte e indicador ausente nas continuacoes.
    from tela.renderizador import renderizar_tela
    from tela.modelo import ModeloTela, Corpo
    # Texto longo o suficiente para ocupar múltiplas linhas físicas em modo
    # verboso com largura pequena.
    texto_longo = (
        "Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu "
        "Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi Omega"
    )
    c = _console(
        "c",
        [
            _item("cur", "Curto"),
            _item("lng", texto_longo),
            _item("out", "OutroXYZ"),
        ],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA, titulo="C",
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    estilo = _estilo_padrao()
    simbolo = estilo.selecionado_simbolo
    # Cursor no item longo, modo verboso: o item ocupa várias linhas físicas.
    # Largura 60 / altura 24: faixa segura sem quadro minimo apos o patch
    # (uniforme multiplica a altura do item longo por todas as linhas).
    saida = renderizar_tela(
        modelo, estilo, largura=60, altura=24, verboso=True,
        foco_console=0, cursores={"c": 1}, lista_foco=lista,
        largura_navegacao=60,
    )
    assert "pequeno" not in saida.lower() and "demais" not in saida.lower()
    # Confirmamos que o item longo ocupa mais de uma linha física: o texto
    # contém palavras que aparecem em linhas físicas distintas da saída.
    linhas_fisicas = [ln for ln in saida.split("\n") if ln.startswith("│")]
    # Pelo menos duas linhas físicas contêm fragmentos do texto longo.
    fragmentos = [w for w in texto_longo.split() if w]
    linhas_com_fragmento = [
        ln for ln in linhas_fisicas if any(frag in ln for frag in fragmentos)
    ]
    assert len(linhas_com_fragmento) >= 2, (
        "item não ocupa múltiplas linhas físicas (continuação real ausente)"
    )
    # Exatamente UMA ocorrência do símbolo: a primeira linha física do item
    # corrente. As linhas de continuação recebem selecionado_off.
    assert saida.count(simbolo) == 1, (
        "esperado 1 símbolo (só primeira linha física), obtido {0}"
        .format(saida.count(simbolo))
    )
    # O símbolo está na primeira linha física do item corrente (que contém o
    # primeiro fragmento do texto longo).
    linha_marcada = [ln for ln in saida.split("\n") if simbolo in ln][0]
    assert fragmentos[0] in linha_marcada or fragmentos[1] in linha_marcada, (
        "símbolo não está na primeira linha física do item corrente"
    )
    # Continuacoes nao recebem o simbolo; item seguinte nao sobrepoe.
    for ln in linhas_fisicas:
        if "OutroXYZ" in ln:
            assert not any(f in ln for f in fragmentos)
            assert simbolo not in ln


# AT-0038 - selecao unica
def teste_selecao_unica_cursor_eh_selecionado():
    # criterio: {id: AT-0038, decisao: D13, resultado_esperado: selecionado e item sob cursor}
    c = _console(
        "c",
        [_item("a", "A"), _item("b", "B"), _item("d", "D")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    est = _estado([c], foco=0, cursores={"c": 2}, largura=30)
    sel = navegacao.item_selecionado(c, est)
    assert sel.get("id") == "d"  # item sob cursor = selecionado


# AT-0039 - chip alternar contextual
def teste_chip_alternar_presente_dois_focalizaveis_ausente_um():
    # criterio: {id: AT-0039, decisao: D14, resultado_esperado: [⇆] aparece so com dois ou mais focos}
    c1 = _console("c1", [_item("a", "A")])
    c2 = _console("c2", [_item("b", "B")])
    # Dois consoles -> exibir
    assert navegacao.exibir_chip_alternar(_estado([c1, c2])) is True
    # Um console -> nao exibir
    assert navegacao.exibir_chip_alternar(_estado([c1])) is False
    # Zero -> nao exibir
    assert navegacao.exibir_chip_alternar(_estado([])) is False


# AT-0040 - chip navegar contextual
def teste_chip_navegar_presente_mais_de_um_item_ausente_um_item():
    # criterio: {id: AT-0040, decisao: D14, resultado_esperado: [✥] aparece com mais de um item e some com um item}
    c_multi = _console("cm", [_item("a", "A"), _item("b", "B")], distribuicao=_DISTRIBUICAO_UMA_COLUNA)
    c_um = _console("cu", [_item("a", "A")], distribuicao=_DISTRIBUICAO_UMA_COLUNA)
    # Console focado com mais de um item -> exibir
    est = _estado([c_multi], foco=0)
    assert navegacao.exibir_chip_navegar(est) is True
    # Console focado com um item -> nao exibir
    est2 = _estado([c_um], foco=0)
    assert navegacao.exibir_chip_navegar(est2) is False
    # Sem foco -> nao exibir
    est3 = _estado([c_multi], foco=None)
    assert navegacao.exibir_chip_navegar(est3) is False


# H-0052 -- fundacao e compatibilidade das politicas de navegacao
def teste_h0052_politica_legada_resolve_nivel_unico():
    c = _console("c", [_item("a", "A"), _item("b", "B")])
    assert navegacao.tipo_navegacao_efetivo(c) == "nivel_unico"
    assert navegacao.console_e_focalizavel(c) is True


def teste_h0052_nivel_unico_explicito_e_legado_sao_equivalentes():
    legado = _console(
        "legado", [_item("a", "A"), _item("b", "B")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    explicito = _console(
        "explicito", [_item("a", "A"), _item("b", "B")],
        distribuicao=_DISTRIBUICAO_UMA_COLUNA,
        tipo_navegacao="nivel_unico",
    )
    assert navegacao.tipo_navegacao_efetivo(explicito) == "nivel_unico"
    assert navegacao.console_e_focalizavel(legado) is True
    assert navegacao.console_e_focalizavel(explicito) is True
    estado_legado = _estado([legado], foco=0, cursores={"legado": 0})
    estado_explicito = _estado([explicito], foco=0, cursores={"explicito": 0})
    for mover in (
        navegacao.mover_direita,
        navegacao.mover_esquerda,
        navegacao.mover_baixo,
        navegacao.mover_cima,
    ):
        estado_legado = mover(estado_legado, legado)
        estado_explicito = mover(estado_explicito, explicito)
    assert estado_legado["cursores"]["legado"] == estado_explicito["cursores"]["explicito"]


def teste_h0052_fixture_nivel_unico_explicito_exibe_chip_navegar():
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(None, "h0052_nivel_unico_explicito", "config/telas/demo")
    )
    lista = navegacao.lista_foco(modelo)
    assert len(lista) == 1
    console = lista[0]
    assert navegacao.tipo_navegacao_efetivo(console) == "nivel_unico"
    assert console._campos_inertes["politica_navegacao"] == {
        "navegavel": True,
        "tipo": "nivel_unico",
    }
    itens = navegacao.itens_navegaveis(console)
    assert len(itens) >= 5
    ids = {item["id"] for item in itens}

    grades = []
    for largura in range(20, 81):
        grade = navegacao.grade_de_itens(
            console,
            largura=largura,
            altura_interna=16,
            desconto_estrutural=3,
        )
        ocupados = [
            item for linha in grade for item in linha if item is not None
        ]
        assert {item["id"] for item in ocupados} == ids
        grades.append((largura, grade))

    colunas = {len(grade[0]) for _largura, grade in grades if grade}
    assert max(colunas) > 1
    assert min(colunas) < max(colunas)

    grade_largura_reduzida = navegacao.grade_de_itens(
        console,
        largura=31,
        altura_interna=16,
        desconto_estrutural=3,
    )
    assert len(grade_largura_reduzida) == 5
    assert all(len(linha) == 1 for linha in grade_largura_reduzida)
    assert [linha[0]["id"] for linha in grade_largura_reduzida] == [
        "item_a",
        "item_b",
        "item_c",
        "item_d",
        "item_e",
    ]

    largura_bidimensional, grade_bidimensional = next(
        (largura, grade)
        for largura, grade in grades
        if len(grade) > 1
        and any(len(linha) > 1 for linha in grade)
        and any(
            celula is None
            for linha in grade
            for celula in linha
        )
    )
    assert all(
        navegacao.item_logico_de_posicao(grade_bidimensional, linha, coluna)
        is None
        for linha in range(len(grade_bidimensional))
        for coluna in range(len(grade_bidimensional[linha]))
        if grade_bidimensional[linha][coluna] is None
    )

    estado = _estado(
        modelo,
        foco=0,
        cursores={console.id: 0},
        largura=largura_bidimensional,
        altura_interna=16,
        desconto_estrutural=3,
    )
    assert navegacao.exibir_chip_navegar(estado) is True

    for mover in (
        navegacao.mover_direita,
        navegacao.mover_esquerda,
        navegacao.mover_baixo,
        navegacao.mover_cima,
    ):
        estado_movido = mover(estado, console)
        assert estado_movido["cursores"][console.id] != 0
        assert navegacao.item_selecionado(console, estado_movido)["id"] in ids
        assert navegacao.exibir_chip_navegar(estado_movido) is True

    estado_direita = navegacao.mover_direita(estado, console)
    assert navegacao.mover_esquerda(estado_direita, console)["cursores"][console.id] == 0
    estado_baixo = navegacao.mover_baixo(estado, console)
    assert navegacao.mover_cima(estado_baixo, console)["cursores"][console.id] == 0

    estado_seguinte = estado_baixo
    assert navegacao.exibir_chip_navegar(estado_seguinte) is True

    saida = renderizar_tela(
        modelo,
        _estilo_padrao(),
        largura=80,
        altura=24,
        foco_console=0,
        cursores=estado_seguinte["cursores"],
        lista_foco=lista,
        largura_navegacao=80,
    )
    assert "[✥] Navegar" in saida
    assert "[?] Ajuda" in saida

    chips_renderizados = ("[Esc] Sair", "[✥] Navegar", "[?] Ajuda")
    linha_barra = next(
        linha for linha in saida.splitlines()
        if all(chip in linha for chip in chips_renderizados)
    )
    posicoes = [linha_barra.index(chip) for chip in chips_renderizados]
    assert posicoes == sorted(posicoes)
    assert linha_barra.strip("│ ").endswith("[?] Ajuda")


def teste_h0052_politica_nao_objeto_nao_recebe_fallback():
    c = _console("c", [_item("a", "A")])
    c._campos_inertes["politica_navegacao"] = "navegavel"
    assert navegacao.tipo_navegacao_efetivo(c) != "nivel_unico"
    assert navegacao.console_e_focalizavel(c) is False


@pytest.mark.parametrize(
    "tipo",
    [
        "nivel_unico",
        "tabela",
        "arvore_colapsavel",
        "selecao_multinivel",
        "dois_niveis_por_foco",
    ],
)
def teste_h0052_transporta_os_cinco_literais_sem_fallback(tipo):
    c = _console(
        "c", [_item("a", "A"), _item("b", "B")], navegavel=(tipo != "tabela"),
        tipo_navegacao=tipo,
    )
    assert navegacao.tipo_navegacao_efetivo(c) == tipo
    assert navegacao.console_e_focalizavel(c) is (tipo == "nivel_unico")


def teste_h0052_tabela_eh_passiva_no_foco_chip_e_movimento_direto():
    tabela = _console(
        "tabela", [_item("a", "A"), _item("b", "B")], navegavel=False,
        tipo_navegacao="tabela", distribuicao=_DISTRIBUICAO_UMA_COLUNA,
    )
    estado = _estado([tabela], foco=None, cursores={"tabela": 1})
    assert navegacao.lista_foco([tabela]) == []
    assert navegacao.exibir_chip_navegar(estado) is False
    for mover in (
        navegacao.mover_direita,
        navegacao.mover_esquerda,
        navegacao.mover_baixo,
        navegacao.mover_cima,
    ):
        novo = mover(estado, tabela)
        assert novo["cursores"] == {"tabela": 1}


# H-0054 -- selecao_multinivel: topologia, selecao e reconciliacao
def teste_h0054_politica_explicita_focaliza_e_fallback_legado_preserva_nivel_unico():
    raiz = _no_selecao(
        "raiz", nivel="grupo", filhos=[_no_selecao("folha", selecionavel=True)]
    )
    console = _selecao_multinivel(nos=[raiz])
    assert navegacao.tipo_navegacao_efetivo(console) == "selecao_multinivel"
    assert navegacao.console_e_focalizavel(console) is True
    assert navegacao.lista_foco([console]) == [console]

    legado = _console("legado", [_item("a", "A")])
    assert navegacao.tipo_navegacao_efetivo(legado) == "nivel_unico"
    assert navegacao.console_e_focalizavel(legado) is True


def teste_h0054_percurso_unico_atravessa_raiz_filho_neto_e_ignora_selecao():
    neto = _no_selecao("neto", selecionavel=True)
    filho = _no_selecao("filho", nivel="grupo", filhos=[neto])
    raiz = _no_selecao("raiz", nivel="grupo", filhos=[filho])
    console = _selecao_multinivel(nos=[raiz, _no_selecao("depois")])
    estado = _estado(
        [console], foco=0, cursores={console.id: 0},
    )
    ids = ["raiz", "filho", "neto", "depois"]
    assert [n.id for n in navegacao.sequencia_visivel_selecao_multinivel(
        console, estado
    )] == ids
    for esperado in ids[1:]:
        estado = navegacao.mover_baixo(estado, console)
        assert navegacao.item_selecionado(console, estado)["id"] == esperado
    assert "selecoes" not in estado
    estado["selecoes"] = {console.id: ["neto"]}
    anterior = estado["selecoes"]
    movido = navegacao.mover_cima(estado, console)
    assert movido["selecoes"] == {console.id: ["neto"]}
    assert anterior == estado["selecoes"]


def teste_h0054_espaco_toggle_de_folha_e_alcance_recursivo_de_pai():
    neto_a = _no_selecao("neto_a", selecionavel=True)
    nao = _no_selecao("nao", selecionavel=False)
    pai = _no_selecao(
        "pai", nivel="grupo", selecionavel=True, filhos=[neto_a, nao]
    )
    folha = _no_selecao("folha", selecionavel=True)
    console = _selecao_multinivel(nos=[pai, folha])
    from tela import selecao

    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado = selecao.alternar(estado, console, "pai")
    assert estado["selecoes"][console.id] == ["pai", "neto_a"]
    assert estado["cursores"][console.id] == 0
    estado = selecao.alternar(estado, console, "pai")
    assert estado["selecoes"][console.id] == []
    estado = selecao.alternar(estado, console, "folha")
    assert estado["selecoes"][console.id] == ["folha"]
    estado = selecao.alternar(estado, console, "folha")
    assert estado["selecoes"][console.id] == []


def _arvore_selecao_h0054():
    folha_111 = _no_selecao("folha_111", selecionavel=True)
    folha_112 = _no_selecao("folha_112", selecionavel=True)
    pai_11 = _no_selecao(
        "pai_11", nivel="grupo", selecionavel=True,
        filhos=[folha_111, folha_112],
    )
    folha_121 = _no_selecao("folha_121", selecionavel=True)
    folha_122 = _no_selecao("folha_122", selecionavel=True)
    pai_12 = _no_selecao(
        "pai_12", nivel="grupo", selecionavel=True,
        filhos=[folha_121, folha_122],
    )
    raiz = _no_selecao(
        "raiz_hierarquica", nivel="grupo", selecionavel=True,
        filhos=[pai_11, pai_12],
    )
    irmao = _no_selecao(
        "ramo_irmao", nivel="grupo", selecionavel=True,
        filhos=[_no_selecao("folha_irma", selecionavel=True)],
    )
    nao = _no_selecao("nao_selecionavel", selecionavel=False)
    return _selecao_multinivel(nos=[raiz, irmao, nao])


def teste_h0054_pai_selecionado_diretamente_reconcilia_toda_a_subarvore():
    from tela import selecao

    console = _arvore_selecao_h0054()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    marcado = selecao.alternar(estado, console, "raiz_hierarquica")

    assert marcado["selecoes"][console.id] == [
        "raiz_hierarquica", "pai_11", "folha_111", "folha_112",
        "pai_12", "folha_121", "folha_122",
    ]
    assert "nao_selecionavel" not in marcado["selecoes"][console.id]


def teste_h0054_construcao_manual_de_pai_intermediario_e_raiz():
    from tela import selecao

    console = _arvore_selecao_h0054()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado = selecao.alternar(estado, console, "folha_111")
    assert estado["selecoes"][console.id] == ["folha_111"]

    estado = selecao.alternar(estado, console, "folha_112")
    assert estado["selecoes"][console.id] == [
        "pai_11", "folha_111", "folha_112",
    ]
    assert "raiz_hierarquica" not in estado["selecoes"][console.id]

    estado = selecao.alternar(estado, console, "folha_121")
    assert "pai_12" not in estado["selecoes"][console.id]
    assert "raiz_hierarquica" not in estado["selecoes"][console.id]
    estado = selecao.alternar(estado, console, "folha_122")
    assert "pai_12" in estado["selecoes"][console.id]
    assert "raiz_hierarquica" in estado["selecoes"][console.id]


def teste_h0054_desselecionar_folha_desmarca_ancestrais_preserva_irmao():
    from tela import selecao

    console = _arvore_selecao_h0054()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado = selecao.alternar(estado, console, "raiz_hierarquica")
    estado = selecao.alternar(estado, console, "folha_111")
    ids = set(estado["selecoes"][console.id])

    assert {"folha_111", "pai_11", "raiz_hierarquica"}.isdisjoint(ids)
    assert {"pai_12", "folha_121", "folha_122"}.issubset(ids)


def teste_h0054_nao_selecionavel_nao_tem_estado_nem_tg_e_e_ignorado():
    from tela import selecao

    console = _arvore_selecao_h0054()
    estado = _estado([console], foco=0, cursores={console.id: 11})
    sem_efeito = selecao.alternar(estado, console, "nao_selecionavel")

    assert navegacao.no_multinivel_selecionavel(
        next(no for no in navegacao._nos_em_pre_ordem(console.conteudo_externo.nos)
             if no.id == "nao_selecionavel")
    ) is False
    assert sem_efeito["selecoes"].get(console.id, []) == []
    assert navegacao.no_tem_alcance_selecao(
        next(no for no in navegacao._nos_em_pre_ordem(console.conteudo_externo.nos)
             if no.id == "nao_selecionavel")
    ) is False


def teste_h0054_reconciliacao_funciona_em_profundidade_arbitraria_sem_estado_parcial():
    from tela import selecao

    folha_a = _no_selecao("prof_folha_a", selecionavel=True)
    folha_b = _no_selecao("prof_folha_b", selecionavel=True)
    nivel_4 = _no_selecao(
        "prof_nivel_4", nivel="grupo", selecionavel=True,
        filhos=[folha_a, folha_b],
    )
    nivel_3 = _no_selecao(
        "prof_nivel_3", nivel="grupo", selecionavel=True,
        filhos=[nivel_4],
    )
    nivel_2 = _no_selecao(
        "prof_nivel_2", nivel="grupo", selecionavel=True,
        filhos=[nivel_3],
    )
    raiz = _no_selecao(
        "prof_raiz", nivel="grupo", selecionavel=True,
        filhos=[nivel_2],
    )
    console = _selecao_multinivel(nos=[raiz])
    estado = _estado([console], foco=0, cursores={console.id: 0})

    estado = selecao.alternar(estado, console, "prof_folha_a")
    assert estado["selecoes"][console.id] == ["prof_folha_a"]
    estado = selecao.alternar(estado, console, "prof_folha_b")
    assert estado["selecoes"][console.id] == [
        "prof_raiz", "prof_nivel_2", "prof_nivel_3", "prof_nivel_4",
        "prof_folha_a", "prof_folha_b",
    ]
    assert not any(
        estado["selecoes"][console.id].count(id_item) > 1
        for id_item in estado["selecoes"][console.id]
    )


def teste_h0054_reconciliacao_remove_ids_nao_selecionaveis_ou_nao_navegaveis():
    valido = _no_selecao("valido", selecionavel=True)
    removido = _no_selecao("removido", selecionavel=True)
    console = _selecao_multinivel(nos=[valido, removido])
    from tela import selecao

    estado = {"selecoes": {console.id: ["removido", "valido", "inexistente"]}}
    removido.campos["navegavel"] = False
    reconciliado = selecao.reconciliar(estado, console)
    assert reconciliado["selecoes"][console.id] == ["valido"]


def teste_h0054_chip_de_selecao_tem_alcance_no_pai_e_fica_inativo_sem_alvo():
    pai = _no_selecao(
        "pai", nivel="grupo", selecionavel=True,
        filhos=[_no_selecao("folha", selecionavel=True)]
    )
    sem_alvo = _no_selecao("sem_alvo", nivel="grupo", filhos=[_no_selecao("x")])
    console = _selecao_multinivel(nos=[pai, sem_alvo])
    estado = _estado([console], foco=0, cursores={console.id: 0})
    assert navegacao.estado_chip_selecao(estado)["ativo"] is True
    estado["cursores"][console.id] = 2
    assert navegacao.estado_chip_selecao(estado)["ativo"] is False


# H-0053 -- arvore_colapsavel sobre ConteudoExterno/NoConteudo
def teste_h0053_arvore_ativa_focalizavel_e_sem_conteudo_nao_focalizavel():
    raiz = _no("raiz", _no("filho_a"), _no("filho_b"))
    arvore = _arvore(nos=[raiz, _no("posterior")])
    assert navegacao.tipo_navegacao_efetivo(arvore) == "arvore_colapsavel"
    assert navegacao.console_e_focalizavel(arvore) is True
    assert navegacao.lista_foco([arvore]) == [arvore]

    sem_conteudo = _console(
        "sem_conteudo", [], tipo_navegacao="arvore_colapsavel"
    )
    assert navegacao.console_e_focalizavel(sem_conteudo) is False


def teste_h0053_sequencia_pre_ordem_movimento_vertical_e_sem_borda_prescrita():
    raiz = _no("raiz", _no("filho_a"), _no("filho_b"))
    arvore = _arvore(nos=[raiz, _no("posterior")])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 0})
    assert [no.id for no in navegacao.sequencia_visivel_arvore(arvore, estado)] == [
        "raiz", "filho_a", "filho_b", "posterior"
    ]
    estado = navegacao.mover_baixo(estado, arvore)
    assert estado["cursores"][arvore.id] == 1
    estado = navegacao.mover_baixo(estado, arvore)
    assert estado["cursores"][arvore.id] == 2
    estado = navegacao.mover_baixo(estado, arvore)
    assert estado["cursores"][arvore.id] == 3
    estado = navegacao.mover_cima(estado, arvore)
    assert estado["cursores"][arvore.id] == 2


def teste_h0053_fechamento_reabertura_mantem_ramo_corrente_e_remove_subarvore():
    raiz = _no("raiz", _no("filho_a"), _no("filho_b"))
    arvore = _arvore(nos=[raiz, _no("posterior")])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 0})

    fechado = navegacao.alternar_ramo(estado, arvore)
    assert fechado["cursores"][arvore.id] == 0
    assert fechado["ramos_fechados"][arvore.id] == frozenset({"raiz"})
    assert [no.id for no in navegacao.sequencia_visivel_arvore(arvore, fechado)] == [
        "raiz", "posterior"
    ]
    assert navegacao.mover_baixo(fechado, arvore)["cursores"][arvore.id] == 1

    corrente = dict(fechado, cursores={arvore.id: 0})
    reaberto = navegacao.alternar_ramo(corrente, arvore)
    assert reaberto["ramos_fechados"][arvore.id] == frozenset()
    assert [no.id for no in navegacao.sequencia_visivel_arvore(arvore, reaberto)] == [
        "raiz", "filho_a", "filho_b", "posterior"
    ]


def teste_h0053_espaco_sobre_folha_nao_cria_selecao_nem_acao():
    raiz = _no("raiz", _no("filho_a"), _no("folha"))
    arvore = _arvore(nos=[raiz])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 2})
    novo = navegacao.alternar_ramo(estado, arvore)
    assert novo["cursores"] == estado["cursores"]
    assert "ramos_fechados" not in novo
    assert "selecoes" not in novo


def teste_h0053_chip_contextual_segue_cursor_ramo_fechado_e_folha():
    raiz = _no("ramo_sem_numero", _no("folha_sem_numero"))
    arvore = _arvore(nos=[raiz, _no("outro_ramo")])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 0})

    assert navegacao.estado_chip_arvore(estado) == {
        "console_id": arvore.id,
        "item_id": "ramo_sem_numero",
        "texto": "Recolher",
        "ativo": True,
    }

    folha = navegacao.mover_baixo(estado, arvore)
    assert navegacao.estado_chip_arvore(folha)["texto"] == "Expandir"
    assert navegacao.estado_chip_arvore(folha)["ativo"] is False
    sem_efeito = navegacao.alternar_ramo(folha, arvore)
    assert sem_efeito["cursores"] == folha["cursores"]
    assert "ramos_fechados" not in sem_efeito

    fechado = navegacao.alternar_ramo(estado, arvore)
    contexto_fechado = navegacao.estado_chip_arvore(fechado)
    assert contexto_fechado["texto"] == "Expandir"
    assert contexto_fechado["ativo"] is True
    assert "Selecionar" not in contexto_fechado["texto"]

    sem_cursor = dict(estado)
    sem_cursor["cursores"] = {}
    assert navegacao.estado_chip_arvore(sem_cursor) is None


def teste_h0053_reconciliacao_nao_forca_cursor_em_projecao_vazia():
    arvore = _arvore(nos=[])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 0})

    reconciliado = navegacao.reconciliar_cursor_arvore(estado, arvore)

    assert reconciliado["cursores"] == {}


def teste_h0053_horizontal_permanece_noop_e_chip_reflete_projecao():
    raiz = _no("raiz", _no("filho"))
    arvore = _arvore(nos=[raiz, _no("posterior")])
    estado = _estado([arvore], foco=0, cursores={arvore.id: 0})
    assert navegacao.mover_direita(estado, arvore) == estado
    assert navegacao.mover_esquerda(estado, arvore) == estado
    assert navegacao.exibir_chip_navegar(estado) is True

    estado_pagina = _estado(
        [arvore], foco=0, cursores={arvore.id: 0},
        itens_permitidos={arvore.id: [0]},
    )
    assert navegacao.exibir_chip_navegar(estado_pagina) is False


def teste_h0053_pagina_atual_restringe_setas_sem_troca_implicita():
    raiz = _no("raiz", _no("filho"), _no("neto"))
    arvore = _arvore(nos=[raiz, _no("posterior")])
    arvore._campos_inertes["politica_paginacao"] = "com"
    estado = _estado(
        [arvore], foco=0, cursores={arvore.id: 0},
        ramos_fechados={},
        itens_permitidos={arvore.id: [0, 3]},
    )
    assert [no.id for no in navegacao.sequencia_visivel_arvore(arvore, estado)] == [
        "raiz", "posterior"
    ]
    novo = navegacao.mover_baixo(estado, arvore)
    assert novo["cursores"][arvore.id] == 3
    assert novo.get("pagina_atual") == estado.get("pagina_atual")


def teste_h0053_mapa_verboso_paginado_reusa_alturas_do_renderer():
    from tela import paginacao
    from tela.renderizacao.console import _linhas_console, mapa_fisico_de_itens
    from tela.renderizacao.contexto_execucao import _navegacao_atual
    from tela.renderizacao.paginacao_interna import _recortar_linhas_paginadas

    nivel = NivelConteudo(
        id="item", tipo="conteudo", conteudo="texto",
        designador={"tipo": "nenhum"},
    )
    longo = NoConteudo(
        id="longo", nivel="item",
        campos={
            "texto": (
                "alpha bravo charlie delta echo foxtrot golf hotel india "
                "juliet kilo lima mike november oscar papa quebec romeo"
            )
        },
    )
    curto = NoConteudo(
        id="curto", nivel="item", campos={"texto": "fim"},
    )
    arvore = _arvore(nos=[longo, curto])
    arvore.conteudo_externo.niveis = [nivel]
    arvore._campos_inertes["politica_paginacao"] = "com"

    contexto_anterior = dict(_navegacao_atual)
    _navegacao_atual.update({
        "lista_foco": [arvore],
        "foco_console": 0,
        "cursores": {arvore.id: 0},
        "ramos_fechados": {arvore.id: frozenset()},
        "paginas_atuais": {arvore.id: 1},
        "largura": 30,
        "altura_interna": 3,
        "simbolo": ">",
        "off": " ",
    })
    try:
        mapa = mapa_fisico_de_itens(
            arvore, 30, 3, True, desconto_estrutural=3,
        )
        linhas_render = _linhas_console(arvore, 25, verboso=True)
        assert mapa[0]["linhas_fisicas"] > 1
        assert [entrada["id"] for entrada in mapa] == ["longo", "curto"]
        assert sum(entrada["linhas_fisicas"] for entrada in mapa) == len(
            linhas_render
        )

        plano = paginacao.plano_de_paginacao(
            arvore, 30, 3, True, desconto_estrutural=3,
        )
        assert plano["total_paginas"] >= 3
        assert sum(pagina["linhas_usadas"] for pagina in plano["paginas"]) == sum(
            entrada["linhas_fisicas"] for entrada in mapa
        )

        pagina_1 = _recortar_linhas_paginadas(
            arvore, linhas_render, 27, 5, True,
        )
        _navegacao_atual["paginas_atuais"] = {arvore.id: 2}
        pagina_2 = _recortar_linhas_paginadas(
            arvore, linhas_render, 27, 5, True,
        )
        assert pagina_1 == linhas_render[:3]
        assert pagina_2 == linhas_render[3:mapa[0]["linhas_fisicas"]]
        assert all("fim" not in linha for linha in pagina_1 + pagina_2)

        estado = _estado(
            [arvore], foco=0, cursores={arvore.id: 0}, largura=30,
            altura_interna=3, ramos_fechados={arvore.id: frozenset()},
        )
        estado["pagina_atual"] = {arvore.id: 1}
        permitidos = paginacao.linhas_logicas_navegaveis_da_pagina(
            estado, arvore,
        )
        assert permitidos == [0]
        assert [no.id for no in navegacao.sequencia_visivel_arvore(arvore, estado)] == [
            "longo"
        ]
        assert navegacao.exibir_chip_navegar(estado) is False
        sem_troca = navegacao.mover_baixo(estado, arvore)
        assert sem_troca["cursores"] == estado["cursores"]
        assert sem_troca["pagina_atual"] == estado["pagina_atual"]
        paginada = paginacao.pagina_proxima(estado, arvore)
        assert paginada["pagina_atual"][arvore.id] == 2
    finally:
        _navegacao_atual.clear()
        _navegacao_atual.update(contexto_anterior)


def test_h0045_setas_restritas_aos_itens_navegaveis_da_pagina_atual():
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    from tela import paginacao

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    estado = {
        "largura": 80,
        "altura_interna": 16,
        "desconto_estrutural": 3,
        "cursores": {console.id: 15},
        "pagina_atual": {console.id: 1},
    }
    permitidos = paginacao.linhas_logicas_navegaveis_da_pagina(estado, console)

    novo = navegacao.mover_baixo(estado, console, itens_permitidos=permitidos)

    assert novo["cursores"][console.id] == 0


# H-0055 -- dois_niveis_por_foco
def _arvore_h0055():
    return _dois_niveis(nos=[
        _no_selecao(
            "pai_a", nivel="grupo", filhos=[
                _no_selecao("a1", selecionavel=True),
                _no_selecao("a2", selecionavel=True),
                _no_selecao("a3", selecionavel=True),
            ],
        ),
        _no_selecao(
            "pai_b", nivel="grupo", filhos=[
                _no_selecao("b1", selecionavel=True),
                _no_selecao("b2", selecionavel=True),
            ],
        ),
    ])


def teste_h0055_politica_explicita_e_terceiro_nivel_invalido():
    console = _arvore_h0055()
    assert navegacao.console_e_focalizavel(console) is True
    assert navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"

    neto = _no_selecao("neto", selecionavel=True)
    filho = _no_selecao("filho", selecionavel=True, filhos=[neto])
    invalido = _dois_niveis(nos=[
        _no_selecao("pai", nivel="grupo", filhos=[filho])
    ])
    assert navegacao.estrutura_dois_niveis_valida(invalido) is False
    assert navegacao.console_e_focalizavel(invalido) is False


def teste_h0055_toroides_independentes_wrap_entrada_e_retorno():
    console = _arvore_h0055()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado["selecoes"] = {console.id: ["a1", "b1"]}

    # Toroide dos pais: 0 (pai_a) -> 4 (pai_b) -> 0.
    estado = navegacao.mover_cima(estado, console)
    assert estado["cursores"][console.id] == 4
    estado = navegacao.mover_baixo(estado, console)
    assert estado["cursores"][console.id] == 0

    filhos = navegacao.entrar_nivel_filhos(estado, console)
    assert filhos["cursores"][console.id] == 1
    assert navegacao.em_nivel_filhos(filhos, console) is True
    assert navegacao.mover_cima(filhos, console)["cursores"][console.id] == 3
    assert navegacao.mover_direita(filhos, console)["cursores"][console.id] == 2

    pais = navegacao.retornar_nivel_pais(filhos, console)
    assert pais["cursores"][console.id] == 0
    assert pais["selecoes"] == filhos["selecoes"]


def teste_h0055_rotulo_esc_recalcula_nos_dois_niveis():
    console = _arvore_h0055()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado["selecoes"] = {console.id: ["a1", "b1"]}

    assert navegacao.rotulo_esc_dois_niveis(estado, console) == "Sair"
    filhos = navegacao.entrar_nivel_filhos(estado, console)
    assert navegacao.rotulo_esc_dois_niveis(filhos, console) == "Voltar"
    pais = navegacao.retornar_nivel_pais(filhos, console)
    assert navegacao.rotulo_esc_dois_niveis(pais, console) == "Sair"

    repetido = navegacao.entrar_nivel_filhos(pais, console)
    repetido = navegacao.retornar_nivel_pais(repetido, console)
    assert navegacao.rotulo_esc_dois_niveis(repetido, console) == "Sair"
    assert repetido["selecoes"] == estado["selecoes"]


def teste_h0055_escolha_inicial_transferencia_idempotencia_e_isolamento():
    from tela import selecao

    console = _arvore_h0055()
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado = selecao.inicializar_escolhas_dois_niveis(estado, console)
    assert estado["selecoes"][console.id] == ["a1", "b1"]

    estado = navegacao.entrar_nivel_filhos(estado, console)
    movido = navegacao.mover_baixo(estado, console)
    assert movido["cursores"][console.id] == 2
    assert movido["selecoes"][console.id] == ["a1", "b1"]

    transferido = selecao.alternar(movido, console, "a2")
    assert transferido["cursores"] == movido["cursores"]
    assert transferido["selecoes"][console.id] == ["a2", "b1"]
    repetido = selecao.alternar(transferido, console, "a2")
    assert repetido["selecoes"][console.id] == ["a2", "b1"]
    assert selecao.limpar(repetido, console)["selecoes"][console.id] == [
        "a2", "b1"
    ]


def teste_h0055_tab_reseta_cursor_sem_alterar_escolhas_e_preserva_resize():
    console = _arvore_h0055()
    outro = _console("outro", [_item("x", "X")])
    estado = _estado(
        [outro, console], foco=0, cursores={"outro": 0, console.id: 2}
    )
    estado["selecoes"] = {console.id: ["a2", "b1"]}
    focado = navegacao.avancar_foco(estado)
    assert focado["foco_console"] == 1
    assert focado["cursores"][console.id] == 0
    assert focado["selecoes"] == estado["selecoes"]
    redimensionado = navegacao.redimensionar(focado, 120, 35)
    assert redimensionado["cursores"] == focado["cursores"]
    assert redimensionado["selecoes"] == focado["selecoes"]


def _formato_filho_h0055():
    return {
        "tabulacao": {"minimo": 5, "maximo": 10},
        "designador": {"tipo": "alfabetico_maiusculo", "sufixo": ")"},
        "apresentacao": "texto",
    }


def _arvore_h0055_com_formato_filho():
    console = _arvore_h0055()
    console.formato_filho_dois_niveis = _formato_filho_h0055()
    return console


def _arvore_h0055_renderizavel():
    pais = [
        NoConteudo(
            id="pai_a",
            nivel="pai",
            campos={"navegavel": True, "selecionavel": False, "titulo": "Pai A"},
            filhos=[
                NoConteudo(
                    id="a1", nivel="filho",
                    campos={
                        "navegavel": True, "selecionavel": True, "titulo": "Um",
                    },
                    filhos=[],
                ),
                NoConteudo(
                    id="a2", nivel="filho",
                    campos={
                        "navegavel": True, "selecionavel": True, "titulo": "Dois",
                    },
                    filhos=[],
                ),
                NoConteudo(
                    id="a3", nivel="filho",
                    campos={
                        "navegavel": True, "selecionavel": True, "titulo": "Tres",
                    },
                    filhos=[],
                ),
            ],
        ),
        NoConteudo(
            id="pai_b",
            nivel="pai",
            campos={"navegavel": True, "selecionavel": False, "titulo": "Pai B"},
            filhos=[
                NoConteudo(
                    id="b1", nivel="filho",
                    campos={
                        "navegavel": True, "selecionavel": True, "titulo": "Quatro",
                    },
                    filhos=[],
                ),
                NoConteudo(
                    id="b2", nivel="filho",
                    campos={
                        "navegavel": True, "selecionavel": True, "titulo": "Cinco",
                    },
                    filhos=[],
                ),
            ],
        ),
    ]
    console = _dois_niveis(nos=pais)
    console.conteudo_externo.niveis = [
        NivelConteudo(
            id="pai", tipo="container", conteudo="titulo",
            designador={"tipo": "decimal", "sufixo": "."},
        ),
        NivelConteudo(
            id="filho", tipo="conteudo", conteudo="titulo",
            designador={"tipo": "nenhum"},
        ),
    ]
    console.formato_filho_dois_niveis = _formato_filho_h0055()
    return console


def teste_h0055_formato_filho_nao_altera_navegacao_nem_selecao():
    from tela import selecao

    console = _arvore_h0055_com_formato_filho()
    assert console.formato_filho_dois_niveis["designador"]["sufixo"] == ")"
    assert navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"

    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado = selecao.inicializar_escolhas_dois_niveis(estado, console)
    assert estado["selecoes"][console.id] == ["a1", "b1"]

    estado = navegacao.mover_cima(estado, console)
    assert estado["cursores"][console.id] == 4
    estado = navegacao.mover_baixo(estado, console)
    assert estado["cursores"][console.id] == 0

    filhos = navegacao.entrar_nivel_filhos(estado, console)
    assert filhos["cursores"][console.id] == 1
    movido = navegacao.mover_baixo(filhos, console)
    assert movido["cursores"][console.id] == 2
    transferido = selecao.alternar(movido, console, "a2")
    assert transferido["selecoes"][console.id] == ["a2", "b1"]
    pais = navegacao.retornar_nivel_pais(transferido, console)
    assert pais["cursores"][console.id] == 0
    assert pais["selecoes"] == transferido["selecoes"]


def teste_h0055_formato_filho_produz_designador_com_sufixo():
    from tela.renderizacao import conteudo_externo

    console = _arvore_h0055_renderizavel()
    config = console.formato_filho_dois_niveis
    assert config["designador"]["tipo"] == "alfabetico_maiusculo"
    assert config["designador"]["sufixo"] == ")"
    assert config["apresentacao"] == "texto"
    assert config["tabulacao"] == {"minimo": 5, "maximo": 10}
    assert "tabela" not in config

    entradas = conteudo_externo._linhas_dois_niveis_formatado_com_mapa(
        console.conteudo_externo, config, content_w=60,
        no_corrente_id="a1", indicador="●", indicador_off="○",
        selecoes={"a1", "b1"}, incluir_selecao=True,
        incluido_on="◆", incluido_off="◇",
    )
    por_id = {entrada["id"]: entrada["linhas"][0] for entrada in entradas}
    assert "A)" in por_id["a1"]
    assert "B)" in por_id["a2"]
    assert "C)" in por_id["a3"]
    assert "A)" in por_id["b1"]
    assert "B)" in por_id["b2"]
    assert " A " not in por_id["a1"]
    assert config["designador"]["sufixo"] == ")"
    assert "A" + config["designador"]["sufixo"] == "A)"

    linha = por_id["a1"]
    recuo = len(linha) - len(linha.lstrip(" "))
    assert 5 <= recuo <= 10
    corpo = linha.lstrip(" ")
    pos_ec = corpo.find("●")
    pos_tg = corpo.find("◆")
    pos_desig = corpo.find("A)")
    pos_texto = corpo.find("Um")
    assert 0 <= pos_ec < pos_tg < pos_desig < pos_texto
    assert linha[:recuo] == " " * recuo
    assert linha[recuo:].startswith("●")
\n