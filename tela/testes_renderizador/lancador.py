from pathlib import Path

from tela.loader import carregar_tela, EstiloResolvido, carregar_conteudo_externo, carregar_estilo
from tela.modelo import Corpo, ElementoCorpo, ModeloTela, construir_modelo, construir_conteudo_externo
from tela.renderizador import (
    RenderizadorErro,
    _distribuir_alturas,
    _distribuir_larguras,
    _linhas_barra,
    _linhas_console,
    _texto_designador,
    _romano,
    _alfabetico,
    _montar_corpo_horizontal,
    _pesos_distribuicao,
    _renderizar_container_horizontal,
    _garantir_esc_primeiro,
    _truncar_com_marcador,
    renderizar_tela,
)
from tela.testes_renderizador.comum import (
    _BASE_PADRAO,
    _RESULTADOS,
    _RAIZ_TELAS_DEMO,
    _ESTILO_CURVA,
    _ESTILO_RETA,
    _ESTILO_CAIXA_ALTA,
    _ESTILO_H0044,
    _EXPECTED_ORQUESTRADOR,
    _EXPECTED_ORQUESTRADOR_RETA,
    _PARAMS_LANCADOR_DEMO,
    _registrar,
    _espera_excecao,
    _modelo_orquestrador_sem_distribuicao,
    _funcional,
    _grupo,
    _grupo_matriz_render_h0028,
    _modelo_h0029,
    _h0029_linhas_totais,
    _alturas_caixas,
    _corpo_alturas,
)



__all__ = [
    'TestDistribuicaoResponsivaH0034',
]


_H0034_ITENS_DEMO = [
    {"id": "i0", "chip": "d", "texto": "Destino"},
    {"id": "i1", "chip": "g", "texto": "Grupo Min."},
    {"id": "i2", "chip": "1", "texto": "Console"},
    {"id": "i3", "chip": "2", "texto": "Dashboard"},
    {"id": "i4", "chip": "3", "texto": "Matriz 2x2"},
    {"id": "i5", "chip": "4", "texto": "Matriz 3x2"},
    {"id": "i6", "chip": "5", "texto": "Matriz 2x4"},
]


def _h0034_modelo_lancador(itens, largura=42, titulo_cab="T"):
    """Modelo minimo em memoria com um unico lancador (arranjo vertical).

    Usado pelos testes basicos de fila/matriz/coluna-minima/quadro-minimo.
    A area do lancador coincide com a largura passada ao renderer (arranjo
    vertical repassa total_w aos filhos), como nos testes de fronteira global
    suplementares. Para isolamento causal do gatilho interno, ver
    ``_h0034_modelo_isolado``.
    """
    corpo = Corpo(
        arranjo="vertical",
        elementos=[
            ElementoCorpo(
                id="lanc_t",
                tipo="lancador",
                _campos_inertes={"titulo": "Navegar", "itens": list(itens)},
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            )
        ],
    )
    return ModeloTela(
        id="t_lancador",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


def _h0034_modelo_isolado(area_lancador_w, terminal_w=80):
    """Modelo sintetico em memoria com arranjo horizontal e area do lancador
    controlada independentemente do viewport global (H-0034 secao 9.5.2).

    ``terminal_w`` fica constante; o lancador recebe ``area_lancador_w`` via
    distribuicao fracao. Isola o gatilho interno ``area_lancador_w <
    lancador_caixa_min_w`` do gatilho global de terminal pequeno.
    """
    area_restante = terminal_w - area_lancador_w
    corpo = Corpo(
        arranjo="horizontal",
        distribuicao={"modo": "fracao", "valores": [area_lancador_w, area_restante]},
        elementos=[
            ElementoCorpo(
                id="lancador_teste",
                tipo="lancador",
                _campos_inertes={
                    "titulo": "Navegar",
                    "itens": [
                        {"id": it["id"], "chip": it["chip"], "texto": it["texto"]}
                        for it in _H0034_ITENS_DEMO
                    ],
                },
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            ),
            ElementoCorpo(
                id="console_resto",
                tipo="console",
                _campos_inertes={"titulo": "Console"},
            ),
        ],
    )
    return ModeloTela(
        id="teste_isolamento_lancador",
        schema="tela.v1",
        cabecalho={"titulo": "TESTE", "descricao": "Isolamento", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


def _h0034_row_of(saida, marker):
    """Indice da primeira linha que contem ``marker``, ou -1."""
    for i, linha in enumerate(saida.splitlines()):
        if marker in linha:
            return i
    return -1


def _h0034_modelo_alinhamento(itens, alinhamento, largura):
    """Modelo minimo em memoria com lancador cujo layout.alinhamento esta
    declarado em _campos_inertes.

    Usado pelos testes de alinhamento horizontal por instancia (R-10).
    """
    campos_inertes = {"titulo": "Navegar", "itens": list(itens)}
    if alinhamento is not None:
        campos_inertes["layout"] = {"alinhamento": alinhamento}
    corpo = Corpo(
        arranjo="vertical",
        elementos=[
            ElementoCorpo(
                id="lanc_alin",
                tipo="lancador",
                _campos_inertes=campos_inertes,
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            )
        ],
    )
    return ModeloTela(
        id="t_alin",
        schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


class TestDistribuicaoResponsivaH0034:
    """Cobertura focal do H-0034: fila, matriz, coluna minima, quadro minimo,
    ordem coluna-a-coluna, larguras independentes, alinhamento por instancia,
    ausencia de paginacao/duplicacao/perda, recupeiracao e isolamento causal.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # ---- Cobertura basica (T-01 a T-05, T-14, T-15) ----------------------

    def test_fila_cardinalidades_basicas(self):
        print("")
        print("== H-0034 basicas: fila, cardinalidades, limite, coluna minima ==")

        # T-03: cardinalidade zero -> 0 linhas de conteudo do lancador, sem erro.
        m_zero = _h0034_modelo_lancador([], largura=42)
        s_zero = renderizar_tela(m_zero, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0034 T-03: cardinalidade zero nao levanta erro",
            isinstance(s_zero, str) and "[d]" not in s_zero,
        )

        # T-02: cardinalidade um -> exatamente 1 linha de conteudo do lancador.
        # item chip "X" texto "Unico" (5): fila_min = 2 + 9 + 2 = 13 (content_w
        # minimo). Em content_w=13 (area=16) deve caber em 1 linha.
        m_um = _h0034_modelo_lancador(
            [{"id": "x", "chip": "X", "texto": "Unico"}], largura=16
        )
        s_um = renderizar_tela(m_um, _ESTILO_CURVA, largura=16)
        # Conta quantas linhas dentro da caixa do lancador contem "[X]".
        linhas_x = [l for l in s_um.splitlines() if "[X]" in l]
        self._r(
            "H-0034 T-02: cardinalidade 1 -> exatamente 1 linha de conteudo",
            len(linhas_x) == 1,
            "linhas_com_X={0}".format(len(linhas_x)),
        )

        # T-01 / T-04: dois itens em fila no limite exato.
        # chip "A" texto "Uno" -> item_w = 3+1+3 = 7; chip "B" texto "Dos" -> 7.
        # fila_content_w_min = 2 + 7+7 + 1*2 + 2 = 20 -> area_lancador_w min = 23.
        itens_2 = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        # Limite exato: area=23 -> content_w=20 -> fila cabe.
        m_2 = _h0034_modelo_lancador(itens_2, largura=23)
        s_23 = renderizar_tela(m_2, _ESTILO_CURVA, largura=23)
        # No limite exato, [A] e [B] estao na mesma linha (fila).
        linha_a = _h0034_row_of(s_23, "[A]")
        linha_b = _h0034_row_of(s_23, "[B]")
        self._r(
            "H-0034 T-01/T-04: content_w=fila_min (area=23) -> fila ([A],[B] "
            "mesma linha)",
            linha_a != -1 and linha_a == linha_b,
            "la={0} lb={1}".format(linha_a, linha_b),
        )

        # T-05: uma unidade abaixo do limite -> matriz (coluna unica, 2 linhas).
        m_2b = _h0034_modelo_lancador(itens_2, largura=22)
        s_22 = renderizar_tela(m_2b, _ESTILO_CURVA, largura=22)
        linha_a = _h0034_row_of(s_22, "[A]")
        linha_b = _h0034_row_of(s_22, "[B]")
        self._r(
            "H-0034 T-05: content_w=fila_min-1 (area=22) -> matriz "
            "([A],[B] linhas diferentes)",
            linha_a != -1 and linha_a != linha_b,
            "la={0} lb={1}".format(linha_a, linha_b),
        )

    def test_quadro_minimo_fronteira_e_recuperacao(self):
        # T-14: itens chip "A" texto "ABCDE"(5), chip "B" texto "XY"(2).
        # max_chip_sub=3, max_texto_sub=5.
        # coluna_minima_content_w = 2 + 3 + 1 + 5 + 2 = 13 -> caixa_min = 16.
        itens_cm = [
            {"id": "a", "chip": "A", "texto": "ABCDE"},
            {"id": "b", "chip": "B", "texto": "XY"},
        ]
        # content_w=13 (area=16): coluna minima valida -> chips presentes.
        m_16 = _h0034_modelo_lancador(itens_cm, largura=16)
        s_16 = renderizar_tela(m_16, _ESTILO_CURVA, largura=16)
        self._r(
            "H-0034 T-14: content_w=coluna_minima (area=16) -> [A],[B] presentes",
            "[A]" in s_16 and "[B]" in s_16,
        )
        # content_w=12 (area=15): abaixo do minimo -> quadro minimo global.
        m_15 = _h0034_modelo_lancador(itens_cm, largura=15)
        s_15 = renderizar_tela(m_15, _ESTILO_CURVA, largura=15)
        self._r(
            "H-0034 T-14: content_w=coluna_minima-1 (area=15) -> quadro minimo "
            "(nenhum chip do lancador)",
            "[A]" not in s_15 and "[B]" not in s_15,
        )
        # T-15: recuperacao automatica apos quadro minimo.
        s_rec = renderizar_tela(m_16, _ESTILO_CURVA, largura=16)
        self._r(
            "H-0034 T-15: recuperacao automatica -> chips presentes novamente",
            "[A]" in s_rec and "[B]" in s_rec,
        )

    # ---- Ordem coluna-a-coluna e ausencia de paginacao (T-06, T-08, T-09) -

    def test_ordem_coluna_a_coluna_e_determinismo(self):
        print("")
        print("== H-0034 ordem coluna-a-coluna, paginacao, determinismo ==")

        # T-06: tres itens, 2 colunas. chip A/B/C texto AAA/BBB/CCC.
        # item_w = 3+1+3 = 7 cada. fila_min = 2+7+7+7+2*2+2 = 30.
        # content_w=20 < 30 -> matriz. n_rows=2, n_col=2.
        # col0=[A,B], col1=[C]. matriz_min = 2 + 7+7 + 1*2 + 2 = 20 -> cabe.
        itens_3 = [
            {"id": "a", "chip": "A", "texto": "AAA"},
            {"id": "b", "chip": "B", "texto": "BBB"},
            {"id": "c", "chip": "C", "texto": "CCC"},
        ]
        m_3 = _h0034_modelo_lancador(itens_3, largura=23)  # area=23 -> cw=20
        s_3 = renderizar_tela(m_3, _ESTILO_CURVA, largura=23)
        la = _h0034_row_of(s_3, "[A]")
        lb = _h0034_row_of(s_3, "[B]")
        lc = _h0034_row_of(s_3, "[C]")
        self._r(
            "H-0034 T-06: ordem coluna-a-coluna ([A],[C] mesma linha; "
            "[B] linha abaixo)",
            la != -1 and la == lc and lb == la + 1,
            "la={0} lb={1} lc={2}".format(la, lb, lc),
        )

        # T-08: ausencia de paginacao. 10 itens (chip 0-9, texto "abcd"=4).
        # coluna_minima_content_w = 2+3+1+4+2 = 12. Em content_w=12 (area=15)
        # coluna unica valida com 10 linhas -> todos os chips presentes.
        itens_10 = [
            {"id": "k{0}".format(i), "chip": str(i), "texto": "abcd"}
            for i in range(10)
        ]
        m_10 = _h0034_modelo_lancador(itens_10, largura=15)
        s_10 = renderizar_tela(m_10, _ESTILO_CURVA, largura=15)
        todos_presentes = all("[{0}]".format(i) in s_10 for i in range(10))
        self._r(
            "H-0034 T-08: 10 itens em coluna minima -> nenhum omitido "
            "(sem paginacao)",
            todos_presentes,
        )

        # T-09: determinismo (reducao/ampliacao). Mesmo conjunto em largura 20
        # depois 25 depois 20 -> primeira e terceira saidas identicas.
        itens_d = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        m_d = _h0034_modelo_lancador(itens_d, largura=23)
        s_a = renderizar_tela(m_d, _ESTILO_CURVA, largura=23)
        renderizar_tela(m_d, _ESTILO_CURVA, largura=30)
        s_b = renderizar_tela(m_d, _ESTILO_CURVA, largura=23)
        self._r(
            "H-0034 T-09: determinismo (mesma largura + itens -> mesma saida)",
            s_a == s_b,
        )

    # ---- Colunas independentes (T-07) ------------------------------------

    def test_colunas_independentes_t07(self):
        print("")
        print("== H-0034 T-07: larguras de coluna independentes ==")

        # T-07 (valores derivados das autoridades, H-0034 secao 10.3):
        #   A "Curto"         -> item_w = 3+1+5  = 9
        #   B "MuitoMaisLong" -> item_w = 3+1+13 = 17  (13 <= 15, valido)
        #   C "Ok"            -> item_w = 3+1+2  = 6
        # fila_min = 2 + 9+17+6 + 2*2 + 2 = 38 > 30 -> nao cabe.
        # matriz n_rows=2, n_col=2:
        #   col0 = [A, B]: chip_sub=max(3,3)=3, texto_sub=max(5,13)=13 -> col_w=17
        #   col1 = [C]:    chip_sub=3, texto_sub=2 -> col_w=6
        # matriz_min = 2 + 17+6 + 1*2 + 2 = 29 <= 30 -> cabe.
        itens_07 = [
            {"id": "a", "chip": "A", "texto": "Curto"},
            {"id": "b", "chip": "B", "texto": "MuitoMaisLong"},
            {"id": "c", "chip": "C", "texto": "Ok"},
        ]
        # area=33 -> content_w=30.
        m_07 = _h0034_modelo_lancador(itens_07, largura=33)
        s_07 = renderizar_tela(m_07, _ESTILO_CURVA, largura=33)

        # [A] e [C] na mesma linha (row 0); [B] na linha abaixo.
        la = _h0034_row_of(s_07, "[A]")
        lb = _h0034_row_of(s_07, "[B]")
        lc = _h0034_row_of(s_07, "[C]")
        self._r(
            "H-0034 T-07: [A] e [C] mesma linha; [B] linha abaixo",
            la != -1 and la == lc and lb == la + 1,
            "la={0} lb={1} lc={2}".format(la, lb, lc),
        )

        # Posicao inicial de col1 = margin_left + col_w_0 + vao_entre_colunas.
        # Independentemente do excesso: col_w_0=17, col_w_1=6 (distintos).
        # Verifica que [C] inicia DEPOIS de [B] (col_w_0=17 aplicado so a col0).
        linha_c = s_07.splitlines()[lc]
        pos_c = linha_c.find("[C]")
        pos_a = s_07.splitlines()[la].find("[A]")
        # col0 largura 17 -> col1 comeca apos 17 (+ margens/vaos). col1 largura
        # 6 -> [C] ocupa poucos chars. Uma implementacao com largura global
        # unica colocaria col1 muito mais a direita (largura 17 ou 6 global).
        self._r(
            "H-0034 T-07: col_w_0=17 != col_w_1=6 (colunas independentes)",
            pos_c > pos_a + 14,  # col0 >= 14 (chip+vao+texto >= 9); col1 bem depois
            "pos_a={0} pos_c={1}".format(pos_a, pos_c),
        )
        # Falha explicita se largura global unica fosse usada: col0 teria a
        # mesma largura que col1. Confirmamos que [B] (texto 13) cabe em col0
        # e [C] (texto 2) em col1, com col1 mais estreito.
        linha_b = s_07.splitlines()[lb]
        self._r(
            "H-0034 T-07: [B] MuitoMaisLong(13) presente integralmente",
            "MuitoMaisLong" in linha_b,
        )

    # ---- Configuracao demo: limites 80/109/110 (T-10 a T-13) ------------

    def _modelo_demo(self):
        raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(raw)
        assert modelo.id == "demo", "id esperado demo, obtido {0}".format(modelo.id)
        return modelo

    def test_demo_fila_110(self):
        print("")
        print("== H-0034 demo: matriz 2 linhas em 110, matriz 3 linhas em 80 ==")
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]

        # T-10 (H-0037 atualizado): com 11 itens, fila_content_w_min=170, fila
        # exigiria area>=173. A area=110 entrega matriz 2 linhas, nao fila.
        # row0=[d,1,3,5,7,9]; row1=[g,2,4,6,8].
        s110 = renderizar_tela(modelo, _ESTILO_CURVA, largura=110, altura=30)
        rd = _h0034_row_of(s110, "[d]")
        rg = _h0034_row_of(s110, "[g]")
        self._r(
            "H-0034 T-10: area=110 -> matriz 2 linhas ([d] e [g] em linhas "
            "diferentes); 11 chips presentes",
            rd != -1 and rd != rg
            and all(c in s110 for c in _CHIPS),
            "rd={0} rg={1}".format(rd, rg),
        )
        # [d] inicia na posicao 4 (borda+padding+2 margem).
        linha_d = s110.splitlines()[rd]
        pos_colchete_d = linha_d.find("[d]")
        self._r(
            "H-0034 T-10: [d] inicia na posicao 4 da linha "
            "(borda+padding+margem esquerda=2)",
            pos_colchete_d == 4,
            "pos={0}".format(pos_colchete_d),
        )
        # [g] inicia na mesma posicao (col0), linha seguinte.
        linha_g = s110.splitlines()[rg]
        pos_g = linha_g.find("[g]")
        self._r(
            "H-0034 T-10: [g] inicia na mesma coluna que [d] (posicao 4)",
            pos_g == 4,
            "pos_g={0}".format(pos_g),
        )
        # Exatamente 2 linhas de itens do lancador em area=110.
        linhas_itens = [
            l for l in s110.splitlines() if any(c in l for c in _CHIPS)
        ]
        self._r(
            "H-0034 T-10: 11 itens em exatamente 2 linhas (matriz 6x2)",
            len(linhas_itens) == 2,
            "linhas_itens={0}".format(len(linhas_itens)),
        )

    def test_demo_matriz_109_e_80(self):
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]

        # T-12: area=109 -> matriz ([d] e [g] linhas diferentes); 11 chips.
        s109 = renderizar_tela(modelo, _ESTILO_CURVA, largura=109, altura=30)
        rd = _h0034_row_of(s109, "[d]")
        rg = _h0034_row_of(s109, "[g]")
        self._r(
            "H-0034 T-12: area=109 -> matriz ([d] e [g] linhas diferentes); "
            "sem quadro minimo",
            rd != -1 and rd != rg and all(c in s109 for c in _CHIPS),
            "rd={0} rg={1}".format(rd, rg),
        )

        # T-11 (H-0037 atualizado): area=80 -> content_w=77 -> matriz 4x3,
        # ordem coluna-a-coluna com 11 itens.
        # col0=[d,g,1] col1=[2,3,4] col2=[5,6,7] col3=[8,9]
        # row0: [d],[2],[5],[8]  row1: [g],[3],[6],[9]  row2: [1],[4],[7]
        s80 = renderizar_tela(modelo, _ESTILO_CURVA, largura=80, altura=30)
        rd = _h0034_row_of(s80, "[d]")
        rg = _h0034_row_of(s80, "[g]")
        r1 = _h0034_row_of(s80, "[1]")
        r2 = _h0034_row_of(s80, "[2]")
        r3 = _h0034_row_of(s80, "[3]")
        r4 = _h0034_row_of(s80, "[4]")
        r5 = _h0034_row_of(s80, "[5]")
        r6 = _h0034_row_of(s80, "[6]")
        r7 = _h0034_row_of(s80, "[7]")
        r8 = _h0034_row_of(s80, "[8]")
        r9 = _h0034_row_of(s80, "[9]")
        self._r(
            "H-0034 T-11: area=80 matriz 4x3 ([d]&[g] linhas diferentes)",
            rd != -1 and rd != rg,
            "rd={0} rg={1}".format(rd, rg),
        )
        # Preenchimento coluna-a-coluna (H-0034 secao 4.3), 11 itens, 4 cols,
        # 3 linhas: row0=[d,2,5,8]; row1=[g,3,6,9]; row2=[1,4,7].
        self._r(
            "H-0034 T-11: ordem coluna-a-coluna "
            "(row0=[d][2][5][8]; row1=[g][3][6][9]; row2=[1][4][7])",
            rd == r2 and rd == r5 and rd == r8
            and rg == r3 and rg == r6 and rg == r9
            and r1 == r4 and r1 == r7
            and rd < rg < r1,
            "rd={0} r2={1} r5={2} r8={3} rg={4} r3={5} r6={6} r9={7} "
            "r1={8} r4={9} r7={10}".format(
                rd, r2, r5, r8, rg, r3, r6, r9, r1, r4, r7
            ),
        )
        # Larguras independentes (H-0034 secao 4.3), 11 itens:
        #   col0=max(11,14,11)=14, col1=max(13,14,14)=14,
        #   col2=max(14,15,11)=15, col3=max(14,15)=15.
        # row0 contem [d](col0), [2](col1), [5](col2), [8](col3).
        linha0 = s80.splitlines()[rd]
        pd = linha0.find("[d]")
        p2 = linha0.find("[2]")
        p5 = linha0.find("[5]")
        p8 = linha0.find("[8]")
        # Distancia [d]->[2] = col_w_0(14) + vao(5) = 19 (vao maximo).
        self._r(
            "H-0034 T-11: col0=14 -> [2] inicia 19 apos [d] (14+5 vao)",
            p2 - pd == 19,
            "pd={0} p2={1} d={2}".format(pd, p2, p2 - pd),
        )
        # Distancia [2]->[5] = col_w_1(14) + vao(5) = 19.
        self._r(
            "H-0034 T-11: col1=14 -> [5] inicia 19 apos [2] (14+5 vao)",
            p5 - p2 == 19,
            "p2={0} p5={1} d={2}".format(p2, p5, p5 - p2),
        )
        # Distancia [5]->[8] = col_w_2(15) + vao(5) = 20.
        self._r(
            "H-0034 T-11: col2=15 -> [8] inicia 20 apos [5] (15+5 vao)",
            p8 - p5 == 20,
            "p5={0} p8={1} d={2}".format(p5, p8, p8 - p5),
        )
        # col2(15) != col0(14): distancias 20 e 19 sao diferentes.
        self._r(
            "H-0034 T-11: col2(15) != col0(14) — distancias 20 != 19",
            (p8 - p5) != (p2 - pd),
        )
        # T-13: componentes nao relacionados preservados em area=80.
        self._r(
            "H-0034 T-13: cabecalho, barra e caixa NAVEGAR preservados em 80",
            "ORQUESTRADOR" in s80 and "NAVEGAR" in s80 and "[Esc] Sair" in s80,
        )
        # Ausencia de paginacao: todos os 11 chips presentes.
        self._r(
            "H-0034 T-11: ausencia de paginacao (11 chips presentes em 80)",
            all(c in s80 for c in _CHIPS),
        )

    def test_demo_sem_paginacao_em_todas_larguras_validas(self):
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]
        # Com 11 itens, max item_w=15 (Nao Verboso / Tab Altern.),
        # coluna_minima_content_w = 2+15+2 = 19 -> area_lancador_min = 22.
        # Larguras estreitas (22, 37) empilham mais linhas -> altura=45.
        # Larguras validas (area>=22): todos os 11 chips presentes.
        ok = True
        for larg in (22, 37, 53, 68, 80, 109, 110):
            try:
                s = renderizar_tela(modelo, _ESTILO_CURVA, largura=larg, altura=45)
                if not all(c in s for c in _CHIPS):
                    ok = False
            except RenderizadorErro:
                ok = False
        self._r(
            "H-0034: sem paginacao em larguras 22/37/53/68/80/109/110",
            ok,
        )

    # ---- Fronteira global suplementar 20/21 (demo vertical) -------------

    def test_demo_fronteira_global_suplementar(self):
        print("")
        print("== H-0034 fronteira global suplementar 21/22 (demo vertical) ==")
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]
        # Estas provas NAO isolam o gatilho interno do lancador (arranjo
        # vertical => terminal_w == area_lancador_w). Sao suplementares.
        # Com 11 itens, max item_w=15 -> coluna_minima_content_w=19 -> area>=22.
        # area=22 -> content_w=19 = coluna_minima -> coluna unica valida.
        # 11 itens em coluna unica requerem mais altura: usar altura=45.
        s22 = renderizar_tela(modelo, _ESTILO_CURVA, largura=22, altura=45)
        self._r(
            "H-0034 suplementar: area=22 -> coluna minima valida (chips "
            "presentes) [nao isola gatilho interno]",
            all(c in s22 for c in _CHIPS),
        )
        # area=21 -> content_w=18 < coluna_minima(19) -> quadro minimo global.
        s21 = renderizar_tela(modelo, _ESTILO_CURVA, largura=21, altura=45)
        self._r(
            "H-0034 suplementar: area=21 -> quadro minimo global (sem chips) "
            "[nao isola gatilho interno]",
            all(c not in s21 for c in _CHIPS),
        )
        # Recuperacao suplementar: 21 -> 110 restaura a matriz (todos os chips).
        s110 = renderizar_tela(modelo, _ESTILO_CURVA, largura=110, altura=30)
        self._r(
            "H-0034 suplementar: recuperacao 21->110 restaura matriz "
            "(todos os 11 chips presentes)",
            all(c in s110 for c in _CHIPS),
        )

    # ---- Prova isolada do gatilho interno (T-ISOL-01/02/03) -------------

    def test_isolamento_gatilho_interno(self):
        print("")
        print("== H-0034 prova isolada do gatilho interno (T-ISOL-01/02/03) ==")
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]"]

        # Cota real dos pesos via algoritmo de maiores restos (verificado
        # independentemente em RELATORIO_QA_POS_SEGUNDO_PATCH secao 6):
        #   _distribuir_larguras(80, [20,60]) -> [20,60] (soma=80, sem resto)
        #   _distribuir_larguras(80, [21,59]) -> [21,59] (soma=80, sem resto)
        # Confirma computacionalmente o esperado:
        self._r(
            "H-0034 ISOL: _distribuir_larguras(80,[20,60]) == [20,60]",
            _distribuir_larguras(80, [20, 60]) == [20, 60],
        )
        self._r(
            "H-0034 ISOL: _distribuir_larguras(80,[21,59]) == [21,59]",
            _distribuir_larguras(80, [21, 59]) == [21, 59],
        )

        # T-ISOL-02 (controle): terminal_w=80, area_lancador_w=21.
        # content_w_lancador = 21-3 = 18 = coluna_minima -> tela normal.
        m21 = _h0034_modelo_isolado(21, terminal_w=80)
        s_isol_21 = renderizar_tela(m21, _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-02: terminal_w=80, area_lancador=21 -> tela normal "
            "(7 chips presentes)",
            all(c in s_isol_21 for c in _CHIPS),
        )
        # O controle prova que os requisitos globais da tela estavam satisfeitos
        # (mesmo terminal, mesmos itens, mesmo segundo elemento).
        # T-ISOL-01 (insuficiente): terminal_w=80 (idem), area_lancador_w=20.
        # content_w_lancador = 20-3 = 17 < coluna_minima(18) -> quadro minimo.
        m20 = _h0034_modelo_isolado(20, terminal_w=80)
        s_isol_20 = renderizar_tela(m20, _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-01: terminal_w=80, area_lancador=20 -> quadro "
            "minimo global (nenhum chip do lancador)",
            all(c not in s_isol_20 for c in _CHIPS),
        )
        # Causa comprovada: unica diferenca material entre T-ISOL-01 e
        # T-ISOL-02 e area_lancador_w (20 vs 21), com terminal_w=80 constante.
        # T-ISOL-03 (recuperacao deterministica): 21 -> 20 -> 21.
        s_p1 = renderizar_tela(_h0034_modelo_isolado(21), _ESTILO_CURVA, largura=80, altura=30)
        renderizar_tela(_h0034_modelo_isolado(20), _ESTILO_CURVA, largura=80, altura=30)
        s_p3 = renderizar_tela(_h0034_modelo_isolado(21), _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-03: sequencia 21->20->21 deterministica "
            "(s_passo1 == s_passo3)",
            s_p1 == s_p3,
        )
        # Ausencia de persistencia indevida: o passo 2 (quadro minimo) nao
        # afeta o passo 3 (tela normal reconstruida).
        self._r(
            "H-0034 T-ISOL-03: passo3 contem os 7 chips (tela normal restaurada)",
            all(c in s_p3 for c in _CHIPS),
        )

    # ---- Alinhamento horizontal por instancia (ALTO-001 / R-10) ----------

    def test_alinhamento_horizontal_por_instancia(self):
        print("")
        print("== H-0034 ALTO-001: alinhamento horizontal por instancia (R-10) ==")

        # Caso fila com excesso residual=3 apos expandir vaos e margens ao max.
        # 2 itens: chip 1-char (sub=3), texto 3 chars -> item_w=7 cada.
        # fila_min = 2 + 7+7 + 1*2 + 2 = 20. content_w=32 (largura=35).
        # excesso=12 -> vaos absorvem 3 (max) -> margens absorvem 3+3 -> residual=3.
        itens_f = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        # Mesma largura para os tres casos; unica variavel = layout.alinhamento.
        m_esq = _h0034_modelo_alinhamento(itens_f, "esquerda", largura=35)
        m_dir = _h0034_modelo_alinhamento(itens_f, "direita", largura=35)
        m_cen = _h0034_modelo_alinhamento(itens_f, "centro", largura=35)

        s_esq = renderizar_tela(m_esq, _ESTILO_CURVA, largura=35)
        s_dir = renderizar_tela(m_dir, _ESTILO_CURVA, largura=35)
        s_cen = renderizar_tela(m_cen, _ESTILO_CURVA, largura=35)

        # Os tres alinhamentos devem produzir saidas distintas (excesso residual=3).
        self._r(
            "H-0034 ALTO-001: fila esq != dir",
            s_esq != s_dir,
        )
        self._r(
            "H-0034 ALTO-001: fila esq != cen",
            s_esq != s_cen,
        )
        self._r(
            "H-0034 ALTO-001: fila dir != cen",
            s_dir != s_cen,
        )

        # Chips e textos presentes integralmente em todos os tres (nao perde
        # conteudo ao redistribuir o excesso).
        for s, nome in ((s_esq, "esq"), (s_dir, "dir"), (s_cen, "cen")):
            self._r(
                "H-0034 ALTO-001: fila {0} contem [A] e [B]".format(nome),
                "[A]" in s and "[B]" in s and "Uno" in s and "Dos" in s,
            )

        # Posicoes esperadas na linha de conteudo:
        #   layout: exc_esq|margem_esq=5|[A] Uno|vao=5|[B] Dos|margem_dir=5|exc_dir
        #   line format: borda(1)+space(1)+content -> [A] at pos 2+content_offset
        #   "esquerda": exc_esq=0 -> [A] at content offset 5 -> pos 7 na linha
        #   "direita":  exc_esq=3 -> [A] at content offset 8 -> pos 10 na linha
        #   "centro":   exc_esq=2 -> [A] at content offset 7 -> pos 9 na linha
        linha_fila_esq = s_esq.splitlines()[_h0034_row_of(s_esq, "[A]")]
        linha_fila_dir = s_dir.splitlines()[_h0034_row_of(s_dir, "[A]")]
        linha_fila_cen = s_cen.splitlines()[_h0034_row_of(s_cen, "[A]")]

        pos_A_esq = linha_fila_esq.find("[A]")
        pos_A_dir = linha_fila_dir.find("[A]")
        pos_A_cen = linha_fila_cen.find("[A]")

        self._r(
            "H-0034 ALTO-001: fila esquerda -> excesso a direita do bloco "
            "(exc_esq=0, [A] pos 7)",
            pos_A_esq == 7,
            "pos={0}".format(pos_A_esq),
        )
        self._r(
            "H-0034 ALTO-001: fila direita -> excesso a esquerda do bloco "
            "(exc_esq=3, [A] pos 10)",
            pos_A_dir == 10,
            "pos={0}".format(pos_A_dir),
        )
        self._r(
            "H-0034 ALTO-001: fila centro -> excesso dividido "
            "(exc_esq=2, [A] pos 9)",
            pos_A_cen == 9,
            "pos={0}".format(pos_A_cen),
        )

        # Vaos internos e largura de bloco identicos nos tres alinhamentos
        # ([A] a [B] = item_A(7) + vao(5) = 12 posicoes em todos).
        pos_B_esq = linha_fila_esq.find("[B]")
        pos_B_dir = linha_fila_dir.find("[B]")
        pos_B_cen = linha_fila_cen.find("[B]")
        self._r(
            "H-0034 ALTO-001: fila: vao entre [A] e [B] igual nos tres "
            "alinhamentos (12 posicoes)",
            (pos_B_esq - pos_A_esq) == 12
            and (pos_B_dir - pos_A_dir) == 12
            and (pos_B_cen - pos_A_cen) == 12,
            "d_esq={0} d_dir={1} d_cen={2}".format(
                pos_B_esq - pos_A_esq, pos_B_dir - pos_A_dir, pos_B_cen - pos_A_cen
            ),
        )

        # Caso matriz com excesso residual=3.
        # 3 itens: chip 1-char (sub=3), texto 7 chars -> item_w=11 cada.
        # fila_min = 2+11+11+11+2*2+2 = 41. Para forcar matriz: content_w < 41.
        # content_w=40 (largura=43). matriz n_rows=2, n_col=2:
        #   col0=[A,B] col_w=11, col1=[C] col_w=11. matriz_min=28.
        # excesso=12 -> vaos absorvem 3 -> margens absorvem 3+3 -> residual=3.
        itens_m = [
            {"id": "a", "chip": "A", "texto": "ABCDEFG"},
            {"id": "b", "chip": "B", "texto": "HIJKLMN"},
            {"id": "c", "chip": "C", "texto": "OPQRSTU"},
        ]
        m_m_esq = _h0034_modelo_alinhamento(itens_m, "esquerda", largura=43)
        m_m_dir = _h0034_modelo_alinhamento(itens_m, "direita", largura=43)
        m_m_cen = _h0034_modelo_alinhamento(itens_m, "centro", largura=43)

        s_m_esq = renderizar_tela(m_m_esq, _ESTILO_CURVA, largura=43)
        s_m_dir = renderizar_tela(m_m_dir, _ESTILO_CURVA, largura=43)
        s_m_cen = renderizar_tela(m_m_cen, _ESTILO_CURVA, largura=43)

        # Saidas distintas.
        self._r(
            "H-0034 ALTO-001: matriz esq != dir",
            s_m_esq != s_m_dir,
        )
        self._r(
            "H-0034 ALTO-001: matriz esq != cen",
            s_m_esq != s_m_cen,
        )

        # Chips presentes em todos os tres.
        for s, nome in ((s_m_esq, "esq"), (s_m_dir, "dir"), (s_m_cen, "cen")):
            self._r(
                "H-0034 ALTO-001: matriz {0}: [A],[B],[C] presentes".format(nome),
                "[A]" in s and "[B]" in s and "[C]" in s,
            )

        # Ordem coluna-a-coluna preservada em todos os alinhamentos:
        # [A] e [C] na mesma linha (row 0), [B] na linha abaixo.
        for s, nome in ((s_m_esq, "esq"), (s_m_dir, "dir"), (s_m_cen, "cen")):
            ra = _h0034_row_of(s, "[A]")
            rb = _h0034_row_of(s, "[B]")
            rc = _h0034_row_of(s, "[C]")
            self._r(
                "H-0034 ALTO-001: matriz {0}: [A],[C] mesma linha; [B] abaixo".format(
                    nome
                ),
                ra != -1 and ra == rc and rb == ra + 1,
                "ra={0} rb={1} rc={2}".format(ra, rb, rc),
            )

        # Posicoes de [A] na row 0 para cada alinhamento:
        #   exc_esq|margem_esq=5|col0(11)|vao=5|col1(11)|margem_dir=5|exc_dir
        #   "esquerda": exc_esq=0 -> [A] content offset 5 -> line pos 7
        #   "direita":  exc_esq=3 -> [A] content offset 8 -> line pos 10
        #   "centro":   exc_esq=2 -> [A] content offset 7 -> line pos 9
        row0_esq = s_m_esq.splitlines()[_h0034_row_of(s_m_esq, "[A]")]
        row0_dir = s_m_dir.splitlines()[_h0034_row_of(s_m_dir, "[A]")]
        row0_cen = s_m_cen.splitlines()[_h0034_row_of(s_m_cen, "[A]")]

        self._r(
            "H-0034 ALTO-001: matriz esquerda -> [A] na pos 7 (exc_esq=0)",
            row0_esq.find("[A]") == 7,
            "pos={0}".format(row0_esq.find("[A]")),
        )
        self._r(
            "H-0034 ALTO-001: matriz direita -> [A] na pos 10 (exc_esq=3)",
            row0_dir.find("[A]") == 10,
            "pos={0}".format(row0_dir.find("[A]")),
        )
        self._r(
            "H-0034 ALTO-001: matriz centro -> [A] na pos 9 (exc_esq=2)",
            row0_cen.find("[A]") == 9,
            "pos={0}".format(row0_cen.find("[A]")),
        )

        # Sem alinhamento declarado (None) -> comportamento identico a "esquerda".
        m_none = _h0034_modelo_alinhamento(itens_f, None, largura=35)
        s_none = renderizar_tela(m_none, _ESTILO_CURVA, largura=35)
        self._r(
            "H-0034 ALTO-001: alinhamento None -> identico a esquerda",
            s_none == s_esq,
        )

        # Alinhamento invalido -> RenderizadorErro (R-10).
        m_inv = _h0034_modelo_alinhamento(
            itens_f, "invalido", largura=35
        )
        try:
            renderizar_tela(m_inv, _ESTILO_CURVA, largura=35)
            self._r("H-0034 ALTO-001: alinhamento invalido -> RenderizadorErro", False)
        except RenderizadorErro:
            self._r("H-0034 ALTO-001: alinhamento invalido -> RenderizadorErro", True)

        # Regressao demo: chips presentes e [d] na posicao esperada (esquerda).
        modelo_demo = self._modelo_demo()
        s_demo_r = renderizar_tela(modelo_demo, _ESTILO_CURVA, largura=110, altura=30)
        linha_d_r = s_demo_r.splitlines()[_h0034_row_of(s_demo_r, "[d]")]
        self._r(
            "H-0034 ALTO-001: regressao demo 110 -> [d] na pos 4 (esquerda, excesso=0)",
            linha_d_r.find("[d]") == 4,
            "pos={0}".format(linha_d_r.find("[d]")),
        )

    # ---- Inercia: renderer nao importa json/os/pathlib (preservado) -----

    def test_parametros_tipo_ausente_levanta_erro(self):
        # H-0034 ALTO-002: lancador sem parametros_tipo (construido fora do
        # pipeline) deve levantar RenderizadorErro ao renderizar.
        modelo_sem_params = ModeloTela(
            id="sem_params",
            schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    ElementoCorpo(
                        id="lanc_sem",
                        tipo="lancador",
                        _campos_inertes={
                            "titulo": "Nav",
                            "itens": [{"id": "i0", "chip": "a", "texto": "Item"}],
                        },
                        # parametros_tipo ausente (None por default)
                    )
                ],
            ),
            barra_de_menus={"chips": []},
            _raw={},
        )
        exc = _espera_excecao(
            "H-0034 ALTO-002: lancador sem parametros_tipo levanta RenderizadorErro",
            lambda: renderizar_tela(modelo_sem_params, _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc is not None:
            self._r(
                "H-0034 ALTO-002: mensagem menciona parametros_tipo",
                "parametros_tipo" in str(exc),
                str(exc),
            )

    def test_renderer_preserva_proibicoes_import(self):
        # H-0010A / H-0034 ALTO-002: o renderer continua proibido de importar
        # json/os/pathlib nem abrir arquivos. Os parametros normativos chegam
        # via elemento.parametros_tipo propagado pelo pipeline loader → modelo.
        caminho_mod = _BASE_PADRAO / "tela" / "renderizador.py"
        texto = caminho_mod.read_text(encoding="utf-8")
        self._r(
            "H-0034: renderer continua sem importar json/os/pathlib",
            "import json" not in texto
            and "import os" not in texto
            and "import pathlib" not in texto,
        )
        self._r(
            "H-0034: renderer continua sem abrir arquivos",
            "open(" not in texto and ".read_text(" not in texto,
        )

    def test_max_caracteres_configuravel(self):
        """max_caracteres vem de params['verificacao']['texto']['max_caracteres'], nao hardcoded."""
        import tela.renderizador as _rend_mod

        # Constante hardcoded não deve mais existir no módulo
        self._r(
            "H-0034: _TEXTO_ITEM_MAX removido do renderer",
            not hasattr(_rend_mod, "_TEXTO_ITEM_MAX"),
        )

        def _modelo_mc(itens, mc):
            return ModeloTela(
                id="mc_t",
                schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                corpo=Corpo(
                    arranjo="vertical",
                    elementos=[
                        ElementoCorpo(
                            id="l_mc",
                            tipo="lancador",
                            _campos_inertes={"titulo": "Nav", "itens": list(itens)},
                            parametros_tipo={
                                "vaos": {
                                    "chip_texto": {"minimo": 1, "maximo": 3},
                                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                                },
                                "vertical": {
                                    "margem_borda_superior": 1,
                                    "margem_borda_inferior": 1,
                                },
                                "verificacao": {"texto": {"max_caracteres": mc}},
                            },
                        )
                    ],
                ),
                barra_de_menus={"chips": []},
                _raw={},
            )

        # mc=3: "Uno" (3 chars) aceito
        _itens_uno = [{"id": "u", "chip": "U", "texto": "Uno", "tela_destino": "x"}]
        try:
            renderizar_tela(_modelo_mc(_itens_uno, 3), _ESTILO_CURVA)
            self._r("H-0034: mc=3 aceita texto de 3 chars ('Uno')", True)
        except Exception as exc:
            self._r("H-0034: mc=3 aceita texto de 3 chars ('Uno')", False, str(exc))

        # mc=3: "Quat" (4 chars) rejeitado
        _itens_quat = [{"id": "q", "chip": "Q", "texto": "Quat", "tela_destino": "x"}]
        exc_quat = _espera_excecao(
            "H-0034: mc=3 rejeita texto de 4 chars ('Quat')",
            lambda: renderizar_tela(_modelo_mc(_itens_quat, 3), _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc_quat is not None:
            self._r(
                "H-0034: mc=3 mensagem menciona limite 3 e texto 'Quat'",
                "3" in str(exc_quat) and "Quat" in str(exc_quat),
                str(exc_quat),
            )

        # mc=3: "Quatro" (6 chars) rejeitado
        _itens_seis = [{"id": "s", "chip": "S", "texto": "Quatro", "tela_destino": "x"}]
        exc_seis = _espera_excecao(
            "H-0034: mc=3 rejeita texto de 6 chars ('Quatro')",
            lambda: renderizar_tela(_modelo_mc(_itens_seis, 3), _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc_seis is not None:
            self._r(
                "H-0034: mc=3 mensagem menciona 'Quatro'",
                "Quatro" in str(exc_seis),
                str(exc_seis),
            )

        # mc=15: "Quatro" (6 chars) aceito
        try:
            renderizar_tela(_modelo_mc(_itens_seis, 15), _ESTILO_CURVA)
            self._r("H-0034: mc=15 aceita texto de 6 chars ('Quatro')", True)
        except Exception as exc:
            self._r("H-0034: mc=15 aceita texto de 6 chars ('Quatro')", False, str(exc))

        # _PARAMS_LANCADOR_DEMO preserva max_caracteres==15
        self._r(
            "H-0034: _PARAMS_LANCADOR_DEMO.verificacao.texto.max_caracteres == 15",
            _PARAMS_LANCADOR_DEMO.get("verificacao", {}).get("texto", {}).get("max_caracteres") == 15,
        )

    def test_caminho_legado_valida_texto(self):
        """Caminho legado _linhas_lancador(elem, content_w=None) usa a sequencia
        comum de normalizacao: parametros_tipo -> max_caracteres ->
        _itens_lancador_normalizados. Prova equivalencia com rota responsiva."""
        from tela.renderizador import _linhas_lancador

        def _elem_legado(itens, mc):
            return ElementoCorpo(
                id="leg",
                tipo="lancador",
                _campos_inertes={"titulo": "Nav", "itens": list(itens)},
                parametros_tipo={
                    "vaos": {
                        "chip_texto": {"minimo": 1, "maximo": 3},
                        "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                    },
                    "vertical": {
                        "margem_borda_superior": 1,
                        "margem_borda_inferior": 1,
                    },
                    "verificacao": {"texto": {"max_caracteres": mc}},
                },
            )

        # Cardinalidade zero: retorna [] sem consultar parametros_tipo.
        elem_zero = ElementoCorpo(
            id="leg_zero",
            tipo="lancador",
            _campos_inertes={"titulo": "Nav", "itens": []},
        )
        resultado_zero = _linhas_lancador(elem_zero, content_w=None)
        self._r(
            "H-0034 LEGADO: cardinalidade zero retorna [] sem parametros_tipo",
            resultado_zero == [],
            repr(resultado_zero),
        )

        # parametros_tipo=None para lancador nao vazio -> RenderizadorErro.
        elem_sem_params = ElementoCorpo(
            id="leg_sem",
            tipo="lancador",
            _campos_inertes={
                "titulo": "Nav",
                "itens": [{"id": "i", "chip": "A", "texto": "Item"}],
            },
        )
        exc_sem = _espera_excecao(
            "H-0034 LEGADO: parametros_tipo=None levanta RenderizadorErro",
            lambda: _linhas_lancador(elem_sem_params, content_w=None),
            RenderizadorErro,
        )
        if exc_sem is not None:
            self._r(
                "H-0034 LEGADO: mensagem menciona parametros_tipo",
                "parametros_tipo" in str(exc_sem),
                str(exc_sem),
            )

        # Estrutura incompleta (verificacao ausente) -> erro; sem fallback.
        elem_inc = ElementoCorpo(
            id="leg_inc",
            tipo="lancador",
            _campos_inertes={
                "titulo": "Nav",
                "itens": [{"id": "i", "chip": "A", "texto": "Item"}],
            },
            parametros_tipo={
                "vaos": {
                    "chip_texto": {"minimo": 1, "maximo": 3},
                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                },
                "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            },
        )
        _espera_excecao(
            "H-0034 LEGADO: estrutura incompleta (verificacao ausente) levanta erro",
            lambda: _linhas_lancador(elem_inc, content_w=None),
            Exception,
        )

        # mc=3: texto com exatamente 3 chars aceito.
        _itens_tres = [{"id": "u", "chip": "U", "texto": "Uno"}]
        try:
            _linhas_lancador(_elem_legado(_itens_tres, 3), content_w=None)
            self._r("H-0034 LEGADO mc=3: texto de 3 chars ('Uno') aceito", True)
        except Exception as exc:
            self._r("H-0034 LEGADO mc=3: texto de 3 chars ('Uno') aceito", False, str(exc))

        # mc=3: texto com 4 chars rejeitado.
        _itens_quatro = [{"id": "q", "chip": "Q", "texto": "Quat"}]
        exc_quat = _espera_excecao(
            "H-0034 LEGADO mc=3: texto de 4 chars ('Quat') rejeitado",
            lambda: _linhas_lancador(_elem_legado(_itens_quatro, 3), content_w=None),
            RenderizadorErro,
        )
        if exc_quat is not None:
            self._r(
                "H-0034 LEGADO mc=3: mensagem menciona limite 3 e texto 'Quat'",
                "3" in str(exc_quat) and "Quat" in str(exc_quat),
                str(exc_quat),
            )

        # mc=3: "Quatro" (6 chars) rejeitado.
        _itens_seis = [{"id": "s", "chip": "S", "texto": "Quatro"}]
        exc_seis = _espera_excecao(
            "H-0034 LEGADO mc=3: 'Quatro' (6 chars) rejeitado",
            lambda: _linhas_lancador(_elem_legado(_itens_seis, 3), content_w=None),
            RenderizadorErro,
        )
        if exc_seis is not None:
            self._r(
                "H-0034 LEGADO mc=3: mensagem menciona 'Quatro'",
                "Quatro" in str(exc_seis),
                str(exc_seis),
            )

        # mc=15: texto valido aceito; saida legada preserva formato "[chip] texto".
        _itens_validos = [{"id": "d", "chip": "d", "texto": "Destino"}]
        try:
            saida = _linhas_lancador(_elem_legado(_itens_validos, 15), content_w=None)
            self._r("H-0034 LEGADO mc=15: texto valido aceito", True)
            self._r(
                "H-0034 LEGADO mc=15: saida preserva formato '[chip] texto'",
                saida == ["[d] Destino"],
                repr(saida),
            )
        except Exception as exc:
            self._r("H-0034 LEGADO mc=15: texto valido aceito", False, str(exc))
            self._r(
                "H-0034 LEGADO mc=15: saida preserva formato '[chip] texto'",
                False,
                str(exc),
            )

        # Equivalencia: mesmo texto rejeitado em content_w=None e content_w valido.
        _itens_inv = [{"id": "e", "chip": "E", "texto": "ABCD"}]
        elem_inv = _elem_legado(_itens_inv, 3)
        _espera_excecao(
            "H-0034 EQUIV: content_w=None rejeita texto acima do max",
            lambda: _linhas_lancador(elem_inv, content_w=None),
            RenderizadorErro,
        )
        modelo_inv = ModeloTela(
            id="equiv_t",
            schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    ElementoCorpo(
                        id="l_inv",
                        tipo="lancador",
                        _campos_inertes={"titulo": "Nav", "itens": list(_itens_inv)},
                        parametros_tipo={
                            "vaos": {
                                "chip_texto": {"minimo": 1, "maximo": 3},
                                "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                            },
                            "vertical": {
                                "margem_borda_superior": 1,
                                "margem_borda_inferior": 1,
                            },
                            "verificacao": {"texto": {"max_caracteres": 3}},
                        },
                    )
                ],
            ),
            barra_de_menus={"chips": []},
            _raw={},
        )
        _espera_excecao(
            "H-0034 EQUIV: content_w valido rejeita mesmo texto acima do max",
            lambda: renderizar_tela(modelo_inv, _ESTILO_CURVA, largura=42),
            RenderizadorErro,
        )

    def run_all(self):
        print("")
        print("== H-0034: distribuicao responsiva do lancador (fila/matriz) ==")
        self.test_fila_cardinalidades_basicas()
        self.test_quadro_minimo_fronteira_e_recuperacao()
        self.test_ordem_coluna_a_coluna_e_determinismo()
        self.test_colunas_independentes_t07()
        self.test_demo_fila_110()
        self.test_demo_matriz_109_e_80()
        self.test_demo_sem_paginacao_em_todas_larguras_validas()
        self.test_demo_fronteira_global_suplementar()
        self.test_isolamento_gatilho_interno()
        self.test_alinhamento_horizontal_por_instancia()
        self.test_parametros_tipo_ausente_levanta_erro()
        self.test_renderer_preserva_proibicoes_import()
        self.test_max_caracteres_configuravel()
        self.test_caminho_legado_valida_texto()
