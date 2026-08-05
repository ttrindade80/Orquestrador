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
    'TestRenderizadorMatrizH0028',
    'TestCardinalidadeUnitariaH0029',
    'TestTelasPermanentesH0029',
    'TestCatalogoH0030',
    'TestDistribuicaoMatricialH0035',
]


def _modelo_matriz_render_h0028(elementos, arranjo="vertical", distribuicao=None):
    if distribuicao is None:
        distribuicao = {"modo": "igual"}
    return ModeloTela(
        id="teste_h0028",
        schema="tela.v1",
        cabecalho={"titulo": "H28", "descricao": "matriz", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo=arranjo, elementos=elementos, distribuicao=distribuicao),
        barra_de_menus={"chips": [{"id": "ok", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


def _linhas_corpo_renderizado(saida):
    linhas = saida.splitlines()
    return linhas[3:-3]


def _posicoes_bordas_linha(linha):
    bordas = set("│┃║┌┐└┘┼├┤┬┴╭╮╰╯─")
    return [i for i, ch in enumerate(linha) if ch in bordas]


class TestRenderizadorMatrizH0028:
    """Testes de grade compartilhada para grupos matriciais (H-0028)."""

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _render_matriz(self, grupo, largura=80, altura=24):
        modelo = _modelo_matriz_render_h0028([grupo])
        return renderizar_tela(modelo, _ESTILO_CURVA, largura=largura, altura=altura)

    def test_matriz_2x2_alinhamento_vertical_e_horizontal(self):
        grupo = _grupo_matriz_render_h0028()
        largura = 80
        altura = 24
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 1])
        larguras = _distribuir_larguras(largura, [1, 1])
        cortes = [0, larguras[0] - 1, larguras[0], largura - 1]

        self._r(
            "H-0028 renderer: matriz 2x2 ocupa soma de alturas do corpo",
            len(corpo) == sum(alturas),
            "len={0} alturas={1!r}".format(len(corpo), alturas),
        )
        self._r(
            "H-0028 renderer: divisorias verticais 2x2 compartilham coordenadas",
            all(all(pos in _posicoes_bordas_linha(linha) for pos in cortes)
                for linha in corpo),
            "cortes={0!r}".format(cortes),
        )
        self._r(
            "H-0028 renderer: divisoria horizontal 2x2 inicia segunda linha na cota comum",
            "E3" in "\n".join(corpo[alturas[0]:])
            and "E1" in "\n".join(corpo[:alturas[0]]),
        )

    def test_matriz_2x4_pesos_assimetricos_compartilhados(self):
        grupo = _grupo_matriz_render_h0028(
            n_linhas=2,
            n_colunas=4,
            dist_linhas={"modo": "fracao", "valores": [1, 2]},
            dist_colunas={"modo": "fracao", "valores": [1, 2, 1, 2]},
        )
        largura = 90
        altura = 30
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 2])
        larguras = _distribuir_larguras(largura, [1, 2, 1, 2])
        acumulado = 0
        cortes = [0]
        for w in larguras:
            acumulado += w
            cortes.extend([acumulado - 1, acumulado])
        cortes = [c for c in cortes if 0 <= c < largura]

        self._r(
            "H-0028 renderer: matriz 2x4 linhas [1,2] aplicadas uma vez",
            alturas[1] >= alturas[0] * 2 - 1 and sum(alturas) == len(corpo),
            "alturas={0!r}".format(alturas),
        )
        self._r(
            "H-0028 renderer: matriz 2x4 colunas [1,2,1,2] aplicadas uma vez",
            sum(larguras) == largura and larguras[1] >= larguras[0] * 2 - 1,
            "larguras={0!r}".format(larguras),
        )
        self._r(
            "H-0028 renderer: cortes 2x4 aparecem nas duas faixas de linha",
            all(all(pos in _posicoes_bordas_linha(corpo[i]) for pos in cortes)
                for i in [0, alturas[0], len(corpo) - 1]),
            "cortes={0!r}".format(cortes),
        )

    def test_dimensoes_impares_e_restos_por_eixo(self):
        grupo = _grupo_matriz_render_h0028(
            n_linhas=3,
            n_colunas=3,
            dist_linhas={"modo": "fracao", "valores": [1, 2, 3]},
            dist_colunas={"modo": "fracao", "valores": [3, 2, 1]},
        )
        largura = 83
        altura = 29
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 2, 3])
        larguras = _distribuir_larguras(largura, [3, 2, 1])
        self._r(
            "H-0028 renderer: restos fecham soma exata das linhas em dimensao impar",
            sum(alturas) == len(corpo) and len(alturas) == 3,
            "alturas={0!r}".format(alturas),
        )
        self._r(
            "H-0028 renderer: restos fecham soma exata das colunas em dimensao impar",
            sum(larguras) == largura and len(larguras) == 3,
            "larguras={0!r}".format(larguras),
        )

    def test_celulas_fora_de_ordem_posicionam_por_coordenada(self):
        filhos = [
            _funcional("a", "console", "A1"),
            _funcional("b", "console", "B2"),
            _funcional("c", "console", "C3"),
            _funcional("d", "console", "D4"),
        ]
        celulas = [
            {"linha": 2, "coluna": 2, "elemento": "d"},
            {"linha": 1, "coluna": 1, "elemento": "a"},
            {"linha": 2, "coluna": 1, "elemento": "c"},
            {"linha": 1, "coluna": 2, "elemento": "b"},
        ]
        grupo = _grupo_matriz_render_h0028(filhos=filhos, celulas=celulas)
        saida = self._render_matriz(grupo, largura=80, altura=24)
        corpo = _linhas_corpo_renderizado(saida)
        topo = "\n".join(corpo[:len(corpo) // 2])
        base = "\n".join(corpo[len(corpo) // 2:])
        self._r(
            "H-0028 renderer: celulas fora de ordem usam coordenadas, nao ordem do array",
            "A1" in topo and "B2" in topo and "C3" in base and "D4" in base,
        )

    def test_tipos_permitidos_e_grupo_livre_em_celula(self):
        grupo_livre = _grupo(
            "g_livre", "vertical",
            [_funcional("interno", "console", "INT")],
            distribuicao={"modo": "igual"},
        )
        filhos = [
            _funcional("c", "console", "CON"),
            _funcional("l", "lancador", "LAN"),
            _funcional("d", "dashboard", "DAS"),
            grupo_livre,
        ]
        celulas = [
            {"linha": 1, "coluna": 1, "elemento": "c"},
            {"linha": 1, "coluna": 2, "elemento": "l"},
            {"linha": 2, "coluna": 1, "elemento": "d"},
            {"linha": 2, "coluna": 2, "elemento": "g_livre"},
        ]
        grupo = _grupo_matriz_render_h0028(filhos=filhos, celulas=celulas)
        saida = self._render_matriz(grupo, largura=80, altura=24)
        self._r(
            "H-0028 renderer: matriz renderiza console, lancador, dashboard e grupo livre",
            all(texto in saida for texto in ["CON", "LAN", "DAS", "INT"]),
        )

    def test_grupo_livre_contendo_matriz(self):
        matriz = _grupo_matriz_render_h0028(gid="mat_interna")
        livre = _grupo(
            "livre", "vertical", [matriz],
            distribuicao={"modo": "igual"},
        )
        modelo = _modelo_matriz_render_h0028([livre])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0028 renderer: grupo livre contendo matriz renderiza matriz interna",
            "E1" in saida and "E4" in saida,
        )

    def test_redimensionamento_recalcula_grade(self):
        grupo = _grupo_matriz_render_h0028(
            dist_colunas={"modo": "fracao", "valores": [1, 2]},
        )
        saida_80 = self._render_matriz(grupo, largura=80, altura=24)
        saida_100 = self._render_matriz(grupo, largura=100, altura=24)
        corpo_80 = _linhas_corpo_renderizado(saida_80)
        corpo_100 = _linhas_corpo_renderizado(saida_100)
        self._r(
            "H-0028 renderer: redimensionamento altera largura das linhas da grade",
            len(corpo_80[0]) == 80 and len(corpo_100[0]) == 100
            and corpo_80[0] != corpo_100[0],
        )

    def test_terminal_pequeno_propaga_erro_global_existente(self):
        grupo = _grupo_matriz_render_h0028()
        _espera_excecao(
            "H-0028 renderer: matriz estreita propaga RenderizadorErro existente",
            lambda: self._render_matriz(grupo, largura=18, altura=24),
            RenderizadorErro,
        )

    def run_all(self):
        print("")
        print("== TestRenderizadorMatrizH0028: grade matricial compartilhada ==")
        self.test_matriz_2x2_alinhamento_vertical_e_horizontal()
        self.test_matriz_2x4_pesos_assimetricos_compartilhados()
        self.test_dimensoes_impares_e_restos_por_eixo()
        self.test_celulas_fora_de_ordem_posicionam_por_coordenada()
        self.test_tipos_permitidos_e_grupo_livre_em_celula()
        self.test_grupo_livre_contendo_matriz()
        self.test_redimensionamento_recalcula_grade()
        self.test_terminal_pequeno_propaga_erro_global_existente()


def _h0029_larguras(saida):
    return [len(l) for l in saida.splitlines() if l.strip()]


def _h0029_barra_posicao(saida, altura):
    linhas = saida.splitlines()
    for i in range(len(linhas) - 1, -1, -1):
        if linhas[i].startswith("╭") or linhas[i].startswith("┌"):
            return i
    return -1


class TestCardinalidadeUnitariaH0029:
    """Testes de distribuicao em containers com cardinalidade unitaria (H-0029).

    Cobre a matriz minima do handoff: ausencia preservada; corpo e grupo com
    modos igual/fracao/percentual para cardinalidade 1; composicao em dois niveis;
    equivalencia geometrica; preservacao de 2+ filhos; preservacao da ausencia;
    preservacao dos JSONs reais; comportamento em duas alturas de terminal.
    """

    LARGURA = 42
    ALTURA = 20
    # l_cab=3, l_barra=3, l_corpo_disponivel=14

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            self._r(nome, True, str(exc))
            return exc

    def _render(self, elementos, corpo_dist=None, altura=None):
        m = _modelo_h0029(elementos, corpo_dist=corpo_dist)
        kw = {"largura": self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # -------------------------------------------------- M01: ausencia funcional
    def test_M01_ausencia_funcional_preserva_natural(self):
        """M01: corpo sem dist, 1 funcional direto -> DA-01 ocupa area integral."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M01: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M01: DA-01 (ADR-0024) - funcional ocupa area integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M01: DA-01 - sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
            "fill_ext={0}".format(len(fill_ext)),
        )

    # -------------------------------------------------- M02: corpo igual funcional
    def test_M02_igual_funcional_direto_ocupa_area(self):
        """M02: corpo=igual, 1 funcional direto -> filho recebe toda a area."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M02: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        corpo_alts = _corpo_alturas(saida)
        # l_corpo_disponivel=14; com dist, funcional ocupa 14 linhas
        self._r(
            "H-0029 M02: funcional recebe toda a area distribuivel (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M02: sem fill externo (dist absorve area internamente)",
            len(fill_ext) == 0,
            "fill_ext={0}".format(len(fill_ext)),
        )
        self._r(
            "H-0029 M02: barra na posicao correta (linha altura-3 = 17)",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
            "barra_pos={0}".format(_h0029_barra_posicao(saida, self.ALTURA)),
        )

    # -------------------------------------------------- M03: fracao[1] funcional
    def test_M03_fracao1_funcional_equivale_igual(self):
        """M03: corpo=fracao[1], 1 funcional -> geometricamente equivalente a M02."""
        saida_ig = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M03: fracao[1] total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M03: fracao[1] geometricamente identico a igual (cardinalidade 1)",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M04: percentual[100] funcional
    def test_M04_percentual100_funcional_equivale_igual(self):
        """M04: corpo=percentual[100], 1 funcional -> equivalente a M02."""
        saida_ig = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "percentual", "valores": [100]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M04: percentual[100] total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M04: percentual[100] geometricamente identico a igual (cardinalidade 1)",
            saida_pc == saida_ig,
        )

    # ---- M05: corpo=igual, grupo sem dist, 1 filho -> DA-01 repassa cota ao filho
    def test_M05_igual_grupo_sem_dist_1filho(self):
        """M05: corpo=igual, grupo sem dist, 1 filho -> DA-01 ocupa cota integral.

        Reproduz o defeito pre-H-0029: output era 8 linhas em vez de 20.
        Apos ADR-0024 DA-01: grupo repassa cota integralmente ao unico filho.
        """
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M05: total de linhas == altura (defeito pre-H-0029 era 8 linhas)",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0} (esperado {1})".format(_h0029_linhas_totais(saida), self.ALTURA),
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M05: DA-01 (ADR-0024) - filho ocupa cota integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        self._r(
            "H-0029 M05: barra na posicao correta",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
            "barra_pos={0}".format(_h0029_barra_posicao(saida, self.ALTURA)),
        )
        linhas = saida.splitlines()
        corpo_linhas = linhas[3:self.ALTURA - 3]
        self._r(
            "H-0029 M05: corpo ocupa exatamente l_corpo_disponivel=14 linhas",
            len(corpo_linhas) == 14,
            "len_corpo={0}".format(len(corpo_linhas)),
        )

    # -------------------------------------------------- M06: fracao[1] grupo sem dist
    def test_M06_fracao1_grupo_sem_dist_1filho(self):
        """M06: corpo=fracao[1], grupo sem dist, 1 filho -> equivalente a M05."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M06: fracao[1] grupo sem dist total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M06: fracao[1] grupo sem dist geometricamente igual a M05 (igual)",
            saida_fr == saida_ig,
        )

    # ---- M07: corpo sem dist, grupo=igual, 1 filho -> DA-01 repassa area ao grupo
    def test_M07_ausencia_corpo_grupo_igual_1filho(self):
        """M07: corpo sem dist, grupo=igual, 1 filho -> DA-01 repassa area integral ao grupo."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M07: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        # DA-01 (ADR-0024): grupo e unico descendente visual -> recebe area integral.
        # DA-03: grupo estrutural repassa area ao filho interno.
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M07: DA-01+DA-03 - filho ocupa area integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M07: DA-01 - sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
        )

    # -------------------------------------------------- M08: fracao[1] interno
    def test_M08_ausencia_corpo_grupo_fracao1_1filho(self):
        """M08: corpo sem dist, grupo=fracao[1], 1 filho -> equivalente a M07."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "fracao", "valores": [1]})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M08: fracao[1] interno total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M08: fracao[1] interno geometricamente identico a igual interno",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M09: percentual[100] interno
    def test_M09_ausencia_corpo_grupo_percentual100_1filho(self):
        """M09: corpo sem dist, grupo=percentual[100], 1 filho -> equivalente a M07."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "percentual", "valores": [100]})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M09: percentual[100] interno total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M09: percentual[100] interno geometricamente identico a igual interno",
            saida_pc == saida_ig,
        )

    # ---- M10: corpo=igual, grupo=igual, 1 filho -> dois niveis distribuicao integral
    def test_M10_igual_grupo_igual_1filho_dois_niveis(self):
        """M10: corpo=igual, grupo=igual, 1 filho -> filho ocupa area interna completa."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M10: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M10: filho ocupa area interna completa (14 linhas = l_corpo_disponivel)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M10: sem fill externo (dois niveis de dist absorvem area)",
            len(fill_ext) == 0,
        )
        self._r(
            "H-0029 M10: barra na posicao correta",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
        )

    # -------------------------------------------------- M11: fracao[1]/fracao[1]
    def test_M11_fracao1_grupo_fracao1_1filho(self):
        """M11: corpo=fracao[1], grupo=fracao[1], 1 filho -> equivalente a M10."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "fracao", "valores": [1]})],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M11: fracao[1]/fracao[1] total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M11: fracao[1]/fracao[1] geometricamente identico a igual/igual",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M12: percentual[100]/percentual[100]
    def test_M12_percentual100_grupo_percentual100_1filho(self):
        """M12: corpo=percentual[100], grupo=percentual[100], 1 filho -> equivalente a M10."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "percentual", "valores": [100]})],
            corpo_dist={"modo": "percentual", "valores": [100]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M12: percentual[100]/percentual[100] total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M12: percentual[100]/percentual[100] geometricamente identico a igual/igual",
            saida_pc == saida_ig,
        )

    # -------------------------------------------------- M13: preservacao 2+ filhos
    def test_M13_preservacao_dois_ou_mais_filhos(self):
        """M13: corpo=igual, grupo=igual, 2+ filhos -> comportamento existente preservado."""
        saida = self._render(
            [_grupo("g1", "vertical", [
                _funcional("d1", "dashboard", "D1"),
                _funcional("d2", "dashboard", "D2"),
            ], distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M13: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M13: dois filhos somam l_corpo_disponivel=14",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )
        self._r(
            "H-0029 M13: dois filhos presentes nas caixas do corpo",
            len(corpo_alts) == 2,
            "n_caixas={0}".format(len(corpo_alts)),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M13: sem fill externo com 2 filhos distribuidos",
            len(fill_ext) == 0,
        )

    # -------------------------------------------------- largura das linhas
    def test_largura_linhas(self):
        """Todas as linhas nao vazias tem a largura correta."""
        for nome, corpo_dist, filhos in [
            ("sem dist, 1 funcional", None, [_funcional("d1", "dashboard", "D1")]),
            ("igual, 1 funcional", {"modo": "igual"}, [_funcional("d1", "dashboard", "D1")]),
            ("igual, 1 grupo sem dist 1 filho",
             {"modo": "igual"},
             [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])]),
            ("igual, 1 grupo igual 1 filho",
             {"modo": "igual"},
             [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                     distribuicao={"modo": "igual"})]),
        ]:
            saida = self._render(filhos, corpo_dist=corpo_dist, altura=self.ALTURA)
            larguras = [len(l) for l in saida.splitlines() if l.strip()]
            todas_corretas = all(w == self.LARGURA for w in larguras)
            self._r(
                "H-0029 largura: {0} -> todas as linhas nao vazias com {1} chars".format(
                    nome, self.LARGURA),
                todas_corretas,
                "larguras={0}".format(sorted(set(larguras))),
            )

    # -------------------------------------------------- redimensionamento (2 alturas)
    def test_redimensionamento_duas_alturas(self):
        """Duas alturas de terminal produzem resultados corretos."""
        for alt in (20, 30):
            for nome, corpo_dist, filhos in [
                ("igual, 1 grupo sem dist 1 filho",
                 {"modo": "igual"},
                 [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])]),
                ("igual, 1 grupo igual 1 filho",
                 {"modo": "igual"},
                 [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                         distribuicao={"modo": "igual"})]),
            ]:
                saida = self._render(filhos, corpo_dist=corpo_dist, altura=alt)
                n = _h0029_linhas_totais(saida)
                self._r(
                    "H-0029 redim: {0} altura={1} -> {1} linhas".format(nome, alt),
                    n == alt,
                    "got={0}".format(n),
                )

    # -------------------------------------------------- soma exata das cotas
    def test_soma_cotas_exata(self):
        """Soma das cotas atribuidas pelo corpo == l_corpo_disponivel."""
        l_corpo = self.ALTURA - 3 - 3  # cab=3, barra=3
        for nome, corpo_dist, filhos in [
            ("igual, 1 funcional",
             {"modo": "igual"},
             [_funcional("d1", "dashboard", "D1")]),
            ("igual, 2 funcionais",
             {"modo": "igual"},
             [_funcional("d1", "dashboard", "D1"), _funcional("d2", "dashboard", "D2")]),
            ("fracao[2,1], 2 funcionais",
             {"modo": "fracao", "valores": [2, 1]},
             [_funcional("d1", "dashboard", "D1"), _funcional("d2", "dashboard", "D2")]),
        ]:
            pesos = _pesos_distribuicao(corpo_dist, len(filhos))
            cotas = _distribuir_alturas(l_corpo, pesos)
            self._r(
                "H-0029 cotas: {0} -> soma({1}) == {2}".format(nome, cotas, l_corpo),
                sum(cotas) == l_corpo,
                "soma={0}".format(sum(cotas)),
            )

    # -------------------------------------------------- composicao 2 niveis unitaria
    def test_composicao_dois_niveis_unitaria(self):
        """Composicao com cardinalidade unitaria em 2 niveis funciona corretamente."""
        # g1 sem dist, g2 com dist=igual, 1 funcional
        saida_a = self._render(
            [_grupo("g1", "vertical", [
                _grupo("g2", "vertical", [_funcional("d1", "dashboard", "D1")],
                       distribuicao={"modo": "igual"})
            ])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 2niveis: g1_sem_dist > g2_igual > 1dash total linhas == altura",
            _h0029_linhas_totais(saida_a) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida_a)),
        )
        # g1 com dist=igual, g2 com dist=igual, 1 funcional
        saida_b = self._render(
            [_grupo("g1", "vertical", [
                _grupo("g2", "vertical", [_funcional("d1", "dashboard", "D1")],
                       distribuicao={"modo": "igual"})
            ], distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 2niveis: g1_igual > g2_igual > 1dash total linhas == altura",
            _h0029_linhas_totais(saida_b) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida_b)),
        )
        corpo_alts_b = _corpo_alturas(saida_b)
        self._r(
            "H-0029 2niveis: g1_igual > g2_igual > 1dash filho expande para 14",
            corpo_alts_b == [14],
            "corpo_alturas={0}".format(corpo_alts_b),
        )

    # -------------------------------------------------- area insuficiente
    def test_area_insuficiente_rejeicao_deterministica(self):
        """Area insuficiente levanta RenderizadorErro deterministico."""
        self._espera_erro(
            "H-0029 area insuficiente: cab+barra > altura levanta RenderizadorErro",
            lambda: self._render(
                [_funcional("d1", "dashboard", "D1")],
                corpo_dist={"modo": "igual"},
                altura=4,  # impossivel: cab=3 + barra=3 > 4
            ),
        )

    # ---------------------------------------- integracao JSON real grupo_minimo
    def test_integracao_json_grupo_minimo(self):
        """Integracao loader -> modelo -> renderer com grupo_minimo.json real."""
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO))
        self._r(
            "H-0029 integracao: grupo_minimo.json distribuicao is None (sem dist)",
            modelo.corpo.distribuicao is None,
        )
        saida20 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H-0029 integracao: grupo_minimo.json altura=20 -> 20 linhas",
            _h0029_linhas_totais(saida20) == 20,
            "got={0}".format(_h0029_linhas_totais(saida20)),
        )
        # DA-01 (ADR-0024): grupo contem 1 visual -> area integral repassada ao filho.
        corpo_alts = _corpo_alturas(saida20)
        self._r(
            "H-0029 integracao: grupo_minimo.json DA-01 - filho ocupa area integral (14 linhas)",
            len(corpo_alts) == 1 and corpo_alts[0] == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )
        # Sem fill externo (ADR-0024 DA-01)
        fill_ext = [l for l in saida20.splitlines() if l == " " * 42]
        self._r(
            "H-0029 integracao: grupo_minimo.json sem fill externo (ADR-0024 DA-01)",
            len(fill_ext) == 0,
        )
        saida_sem = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0029 integracao: grupo_minimo.json sem altura produz saida nao vazia",
            bool(saida_sem.strip()),
        )

    # ---------------------------------------- preservacao ausencia nos JSONs reais
    def test_preservacao_jsons_sem_dist(self):
        """destino_minimo.json e stub_b.json nao declaram distribuicao: preservados."""
        for id_tela in ("destino_minimo", "stub_b"):
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            self._r(
                "H-0029 preserv: {0} distribuicao is None".format(id_tela),
                modelo.corpo.distribuicao is None,
            )
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
            self._r(
                "H-0029 preserv: {0} altura=20 -> 20 linhas".format(id_tela),
                _h0029_linhas_totais(saida) == 20,
                "got={0}".format(_h0029_linhas_totais(saida)),
            )

    def run_all(self):
        print("")
        print("== TestCardinalidadeUnitariaH0029: distribuicao com cardinalidade 1 ==")
        self.test_M01_ausencia_funcional_preserva_natural()
        self.test_M02_igual_funcional_direto_ocupa_area()
        self.test_M03_fracao1_funcional_equivale_igual()
        self.test_M04_percentual100_funcional_equivale_igual()
        self.test_M05_igual_grupo_sem_dist_1filho()
        self.test_M06_fracao1_grupo_sem_dist_1filho()
        self.test_M07_ausencia_corpo_grupo_igual_1filho()
        self.test_M08_ausencia_corpo_grupo_fracao1_1filho()
        self.test_M09_ausencia_corpo_grupo_percentual100_1filho()
        self.test_M10_igual_grupo_igual_1filho_dois_niveis()
        self.test_M11_fracao1_grupo_fracao1_1filho()
        self.test_M12_percentual100_grupo_percentual100_1filho()
        self.test_M13_preservacao_dois_ou_mais_filhos()
        self.test_largura_linhas()
        self.test_redimensionamento_duas_alturas()
        self.test_soma_cotas_exata()
        self.test_composicao_dois_niveis_unitaria()
        self.test_area_insuficiente_rejeicao_deterministica()
        self.test_integracao_json_grupo_minimo()
        self.test_preservacao_jsons_sem_dist()


_H0029_TELAS_DASHBOARD = (
    "h0029_dashboard_igual",
    "h0029_dashboard_fracao",
    "h0029_dashboard_percentual",
)


_H0029_TELAS_GRUPO_DISTRIBUIDO = (
    "h0029_grupo_igual",
    "h0029_grupo_fracao",
    "h0029_grupo_percentual",
)


_H0029_TELAS_GRUPO_SEM_DIST = ("h0029_grupo_pai_distribuido",)


_H0029_TELAS_TODAS = (
    _H0029_TELAS_DASHBOARD
    + _H0029_TELAS_GRUPO_SEM_DIST
    + _H0029_TELAS_GRUPO_DISTRIBUIDO
)


def _h0029_caminho_json(id_tela):
    return _BASE_PADRAO / "config" / "telas" / "demo" / (id_tela + ".json")


def _h0029_dashboard_topo(saida):
    """Indice da borda superior (╭/┌) do primeiro dashboard apos o cabecalho."""
    linhas = saida.splitlines()
    for i, linha in enumerate(linhas):
        if i < 3:
            continue
        if linha.startswith("╭") or linha.startswith("┌"):
            return i
    return -1


def _h0029_dashboard_base(saida):
    """Indice da borda inferior (╰/└) do primeiro dashboard apos o cabecalho."""
    linhas = saida.splitlines()
    topo = _h0029_dashboard_topo(saida)
    if topo < 0:
        return -1
    for i in range(topo + 1, len(linhas)):
        if linhas[i].startswith("╰") or linhas[i].startswith("└"):
            return i
    return -1


def _h0029_barra_topo(saida):
    """Indice da borda superior da caixa da barra_de_menus (ultima caixa)."""
    linhas = saida.splitlines()
    for i in range(len(linhas) - 1, -1, -1):
        if linhas[i].startswith("╭") or linhas[i].startswith("┌"):
            return i
    return -1


def _h0029_bordas_laterais_continuas(saida, topo, base):
    """True se as linhas internas entre topo e base comecam e terminam com a
    borda vertical (│) do conjunto curva."""
    linhas = saida.splitlines()
    for i in range(topo + 1, base):
        if i >= len(linhas):
            return False
        linha = linhas[i]
        if not linha.startswith("│") or not linha.endswith("│"):
            return False
    return True


class TestTelasPermanentesH0029:
    """Testes nominais de integracao para os sete JSONs permanentes h0029_*.

    Carrega cada JSON pelo loader real, constroi o modelo e verifica a geometria
    materialmente relevante em pelo menos duas alturas, conforme a secao 12.2 do
    handoff H-0029. Nao se limita a contagem de linhas: inspeciona bordas do
    dashboard, posicao da barra_de_menus, continuidade das bordas laterais,
    ausencia de sobreposicao e equivalencia entre os tres modos de cada grupo.
    """

    LARGURA = 42
    ALTURAS = (20, 30)

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # --------------------------------------------------- existencia e sintaxe
    def test_existencia_e_sintaxe(self):
        import json as _json
        for id_tela in _H0029_TELAS_TODAS:
            caminho = _h0029_caminho_json(id_tela)
            existe = caminho.is_file()
            self._r(
                "H-0029 JSON {0}: arquivo existe".format(id_tela),
                existe,
                "caminho={0}".format(caminho),
            )
            if not existe:
                continue
            try:
                with caminho.open(encoding="utf-8") as fh:
                    dados = _json.load(fh)
            except Exception as exc:
                self._r(
                    "H-0029 JSON {0}: sintaxe JSON valida".format(id_tela),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )
                continue
            self._r(
                "H-0029 JSON {0}: sintaxe JSON valida".format(id_tela),
                isinstance(dados, dict),
            )

    # ------------------------------------------- carregamento e construcao
    def test_carregamento_modelo(self):
        for id_tela in _H0029_TELAS_TODAS:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
            except Exception as exc:
                self._r(
                    "H-0029 JSON {0}: carrega e constroi modelo".format(id_tela),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )
                continue
            self._r(
                "H-0029 JSON {0}: carrega e constroi modelo".format(id_tela),
                isinstance(modelo, ModeloTela),
            )
            self._r(
                "H-0029 JSON {0}: id corresponde ao arquivo".format(id_tela),
                modelo.id == id_tela,
                "id={0!r}".format(modelo.id),
            )
            self._r(
                "H-0029 JSON {0}: schema tela.v1".format(id_tela),
                modelo.schema == "tela.v1",
                "schema={0!r}".format(modelo.schema),
            )
            self._r(
                "H-0029 JSON {0}: corpo tem exatamente 1 filho direto".format(id_tela),
                len(modelo.corpo.elementos) == 1,
                "n_filhos={0}".format(len(modelo.corpo.elementos)),
            )

    # ------------------------------------------- distribuicao declarada do corpo
    def test_distribuicao_corpo_declarada(self):
        espec = {
            "h0029_dashboard_igual": {"modo": "igual"},
            "h0029_dashboard_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_dashboard_percentual": {"modo": "percentual", "valores": [100]},
            "h0029_grupo_pai_distribuido": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_igual": {"modo": "igual"},
            "h0029_grupo_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_percentual": {"modo": "percentual", "valores": [100]},
        }
        for id_tela, esperado in espec.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            dist = modelo.corpo.distribuicao
            self._r(
                "H-0029 JSON {0}: corpo.distribuicao == {1!r}".format(id_tela, esperado),
                dist == esperado,
                "dist={0!r}".format(dist),
            )

    # ----------------------------------------------- tipo do filho direto
    def test_tipo_do_filho_do_corpo(self):
        espec = {
            "h0029_dashboard_igual": "dashboard",
            "h0029_dashboard_fracao": "dashboard",
            "h0029_dashboard_percentual": "dashboard",
            "h0029_grupo_pai_distribuido": "grupo",
            "h0029_grupo_igual": "grupo",
            "h0029_grupo_fracao": "grupo",
            "h0029_grupo_percentual": "grupo",
        }
        for id_tela, esperado in espec.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            filho = modelo.corpo.elementos[0]
            self._r(
                "H-0029 JSON {0}: filho do corpo e tipo {1!r}".format(id_tela, esperado),
                filho.tipo == esperado,
                "tipo={0!r}".format(filho.tipo),
            )

    # ----------------------------- distribuicao interna do grupo (presenca/ausencia)
    def test_distribuicao_interna_do_grupo(self):
        # Telas com grupo: pai_distribuido SEM dist interna; demais COM dist interna.
        sem_dist = {"h0029_grupo_pai_distribuido"}
        com_dist = {
            "h0029_grupo_igual": {"modo": "igual"},
            "h0029_grupo_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_percentual": {"modo": "percentual", "valores": [100]},
        }
        for id_tela in sem_dist:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            grupo = modelo.corpo.elementos[0]
            dist_g = grupo._campos_inertes.get("distribuicao")
            self._r(
                "H-0029 JSON {0}: grupo SEM distribuicao interna".format(id_tela),
                dist_g is None,
                "dist_g={0!r}".format(dist_g),
            )
            self._r(
                "H-0029 JSON {0}: grupo tem 1 filho interno".format(id_tela),
                len(grupo.elementos) == 1,
                "n={0}".format(len(grupo.elementos)),
            )
            self._r(
                "H-0029 JSON {0}: filho interno e dashboard".format(id_tela),
                grupo.elementos[0].tipo == "dashboard",
            )
        for id_tela, esperado in com_dist.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            grupo = modelo.corpo.elementos[0]
            dist_g = grupo._campos_inertes.get("distribuicao")
            self._r(
                "H-0029 JSON {0}: grupo.distribuicao == {1!r}".format(id_tela, esperado),
                dist_g == esperado,
                "dist_g={0!r}".format(dist_g),
            )
            self._r(
                "H-0029 JSON {0}: grupo tem 1 filho interno".format(id_tela),
                len(grupo.elementos) == 1,
            )
            self._r(
                "H-0029 JSON {0}: filho interno e dashboard".format(id_tela),
                grupo.elementos[0].tipo == "dashboard",
            )

    # ------------------------- geometria: altura total, largura, barra (2 alturas)
    def test_geometria_altura_largura_barra(self):
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                linhas = saida.splitlines()
                self._r(
                    "H-0029 JSON {0} alt={1}: total de linhas == altura".format(
                        id_tela, altura
                    ),
                    len(linhas) == altura,
                    "linhas={0}".format(len(linhas)),
                )
                larguras = {len(l) for l in linhas if l.strip()}
                self._r(
                    "H-0029 JSON {0} alt={1}: largura uniforme == {2}".format(
                        id_tela, altura, self.LARGURA
                    ),
                    larguras == {self.LARGURA},
                    "larguras={0}".format(sorted(larguras)),
                )
                barra = _h0029_barra_topo(saida)
                self._r(
                    "H-0029 JSON {0} alt={1}: barra_topo == altura-3 ({2})".format(
                        id_tela, altura, altura - 3
                    ),
                    barra == altura - 3,
                    "barra_topo={0}".format(barra),
                )

    # ----------------------------- geometria: dashboard preenche area distribuida
    def test_geometria_dashboard_preenche_area(self):
        """Telas 11A.1-11A.3 e 11A.5-11A.7: dashboard ocupa toda a area."""
        preenche = _H0029_TELAS_DASHBOARD + _H0029_TELAS_GRUPO_DISTRIBUIDO
        for id_tela in preenche:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                topo = _h0029_dashboard_topo(saida)
                base = _h0029_dashboard_base(saida)
                barra = _h0029_barra_topo(saida)
                self._r(
                    "H-0029 JSON {0} alt={1}: dashboard topo == 3".format(
                        id_tela, altura
                    ),
                    topo == 3,
                    "topo={0}".format(topo),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: dashboard base == altura-4 ({2})".format(
                        id_tela, altura, altura - 4
                    ),
                    base == altura - 4,
                    "base={0}".format(base),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: borda inferior imediatamente antes "
                    "da barra (gap == 0)".format(id_tela, altura),
                    base >= 0 and barra == base + 1,
                    "base={0} barra={1}".format(base, barra),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: bordas laterais continuas".format(
                        id_tela, altura
                    ),
                    _h0029_bordas_laterais_continuas(saida, topo, base),
                )
                # Ausencia de linhas externas (branco total) entre dashboard e barra.
                entre = [
                    l for l in saida.splitlines()[base + 1:barra]
                    if l == " " * self.LARGURA
                ]
                self._r(
                    "H-0029 JSON {0} alt={1}: sem linhas externas entre dashboard "
                    "e barra".format(id_tela, altura),
                    len(entre) == 0,
                    "linhas_externas={0}".format(len(entre)),
                )

    # ----------------------------- geometria: grupo_pai_distribuido (DA-01)
    def test_geometria_grupo_pai_distribuido_natural(self):
        """Tela 11A.4: DA-01 (ADR-0024) - dashboard ocupa area integral do grupo."""
        id_tela = "h0029_grupo_pai_distribuido"
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
        for altura in self.ALTURAS:
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA,
                largura=self.LARGURA, altura=altura,
            )
            linhas = saida.splitlines()
            topo = _h0029_dashboard_topo(saida)
            base = _h0029_dashboard_base(saida)
            barra = _h0029_barra_topo(saida)
            l_corpo_disponivel = altura - 3 - 3  # l_cab=3, l_barra=3
            # DA-01 (ADR-0024): grupo repassa cota integral ao unico visual filho.
            # Dashboard expande de 2 linhas naturais para l_corpo_disponivel linhas.
            self._r(
                "H-0029 JSON {0} alt={1}: dashboard topo == 3".format(
                    id_tela, altura
                ),
                topo == 3,
                "topo={0}".format(topo),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: DA-01 - dashboard base == altura-4 ({2})".format(
                    id_tela, altura, altura - 4
                ),
                base == altura - 4,
                "base={0}".format(base),
            )
            # DA-01: dashboard ocupa toda a area; barra imediatamente apos (gap==0).
            self._r(
                "H-0029 JSON {0} alt={1}: DA-01 - borda inferior imediatamente "
                "antes da barra (gap == 0)".format(id_tela, altura),
                base >= 0 and barra == base + 1,
                "base={0} barra={1}".format(base, barra),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: barra_topo == altura-3 ({2})".format(
                    id_tela, altura, altura - 3
                ),
                barra == altura - 3,
                "barra={0}".format(barra),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: sem sobreposicao (base < barra)".format(
                    id_tela, altura
                ),
                base < barra and len(linhas) == altura,
            )

    # --------------------------------------------- equivalencia: dashboards
    def test_equivalencia_dashboard_tres_modos(self):
        """h0029_dashboard_igual/fracao/percentual geometricamente equivalentes."""
        saidas = {}
        for altura in self.ALTURAS:
            saidas[altura] = {}
            for id_tela in _H0029_TELAS_DASHBOARD:
                modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
                saidas[altura][id_tela] = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
            igual = saidas[altura]["h0029_dashboard_igual"]
            frac = saidas[altura]["h0029_dashboard_fracao"]
            perc = saidas[altura]["h0029_dashboard_percentual"]
            # Geometria (bordas) deve coincidir; textos do cabecalho diferem.
            for id_tela, s in (("fracao", frac), ("percentual", perc)):
                top_i = _h0029_dashboard_topo(igual)
                top_o = _h0029_dashboard_topo(s)
                base_i = _h0029_dashboard_base(igual)
                base_o = _h0029_dashboard_base(s)
                barra_i = _h0029_barra_topo(igual)
                barra_o = _h0029_barra_topo(s)
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} topo".format(
                        altura, id_tela
                    ),
                    top_i == top_o,
                    "igual={0} {1}={2}".format(top_i, id_tela, top_o),
                )
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} base".format(
                        altura, id_tela
                    ),
                    base_i == base_o,
                    "igual={0} {1}={2}".format(base_i, id_tela, base_o),
                )
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} barra".format(
                        altura, id_tela
                    ),
                    barra_i == barra_o,
                    "igual={0} {1}={2}".format(barra_i, id_tela, barra_o),
                )
                # Altura do corpo (dashboard) identica.
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} altura dashboard".format(
                        altura, id_tela
                    ),
                    (base_i - top_i) == (base_o - top_o),
                    "igual={0} {1}={2}".format(base_i - top_i, id_tela, base_o - top_o),
                )

    # ------------------------------------------------- equivalencia: grupos
    def test_equivalencia_grupo_tres_modos(self):
        """h0029_grupo_igual/fracao/percentual geometricamente equivalentes."""
        saidas = {}
        for altura in self.ALTURAS:
            saidas[altura] = {}
            for id_tela in _H0029_TELAS_GRUPO_DISTRIBUIDO:
                modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
                saidas[altura][id_tela] = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
            igual = saidas[altura]["h0029_grupo_igual"]
            frac = saidas[altura]["h0029_grupo_fracao"]
            perc = saidas[altura]["h0029_grupo_percentual"]
            for id_tela, s in (("fracao", frac), ("percentual", perc)):
                top_i = _h0029_dashboard_topo(igual)
                top_o = _h0029_dashboard_topo(s)
                base_i = _h0029_dashboard_base(igual)
                base_o = _h0029_dashboard_base(s)
                barra_i = _h0029_barra_topo(igual)
                barra_o = _h0029_barra_topo(s)
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} topo".format(
                        altura, id_tela
                    ),
                    top_i == top_o,
                    "igual={0} {1}={2}".format(top_i, id_tela, top_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} base".format(
                        altura, id_tela
                    ),
                    base_i == base_o,
                    "igual={0} {1}={2}".format(base_i, id_tela, base_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} barra".format(
                        altura, id_tela
                    ),
                    barra_i == barra_o,
                    "igual={0} {1}={2}".format(barra_i, id_tela, barra_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} altura dashboard".format(
                        altura, id_tela
                    ),
                    (base_i - top_i) == (base_o - top_o),
                    "igual={0} {1}={2}".format(base_i - top_i, id_tela, base_o - top_o),
                )

    # --------------------------- area adicional absorvida (redimensionamento)
    def test_area_adicional_absorvida(self):
        """Altura maior: area extra absorvida corretamente; barra permanece no fim."""
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            s20 = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=self.LARGURA, altura=20
            )
            s30 = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=self.LARGURA, altura=30
            )
            barra20 = _h0029_barra_topo(s20)
            barra30 = _h0029_barra_topo(s30)
            self._r(
                "H-0029 JSON {0}: barra acompanha nova altura (17->27)".format(id_tela),
                barra20 == 17 and barra30 == 27,
                "barra20={0} barra30={1}".format(barra20, barra30),
            )
            # DA-01 (ADR-0024): todos os JSONs h0029_* expandem o dashboard
            # para preencher a area disponivel, incluindo grupo_pai_distribuido
            # (grupo sem dist interna recebe area via DA-01 e repassa ao filho).
            base20 = _h0029_dashboard_base(s20)
            base30 = _h0029_dashboard_base(s30)
            self._r(
                "H-0029 JSON {0}: borda inferior acompanha cota (16->26)".format(
                    id_tela
                ),
                base20 == 16 and base30 == 26,
                "base20={0} base30={1}".format(base20, base30),
            )

    # ----------------------------------- ausencia de sobreposicao (geral)
    def test_ausencia_sobreposicao(self):
        """Nenhuma tela produz linhas duplicadas nem desaparecimento de bordas."""
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                linhas = saida.splitlines()
                # Sem linha em branco entre caixas (invariante do renderer).
                self._r(
                    "H-0029 JSON {0} alt={1}: sem '\\n\\n' (sem linha em branco)".format(
                        id_tela, altura
                    ),
                    "\n\n" not in saida,
                )
                # Contagem de bordas superiores: 3 caixas (cabecalho, corpo, barra).
                top_count = sum(
                    1 for l in linhas if l.startswith("╭")
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: exatamente 3 caixas (3 bordas superiores)".format(
                        id_tela, altura
                    ),
                    top_count == 3,
                    "top_count={0}".format(top_count),
                )

    def run_all(self):
        print("")
        print("== TestTelasPermanentesH0029: sete JSONs nominais ==")
        self.test_existencia_e_sintaxe()
        self.test_carregamento_modelo()
        self.test_distribuicao_corpo_declarada()
        self.test_tipo_do_filho_do_corpo()
        self.test_distribuicao_interna_do_grupo()
        self.test_geometria_altura_largura_barra()
        self.test_geometria_dashboard_preenche_area()
        self.test_geometria_grupo_pai_distribuido_natural()
        self.test_equivalencia_dashboard_tres_modos()
        self.test_equivalencia_grupo_tres_modos()
        self.test_area_adicional_absorvida()
        self.test_ausencia_sobreposicao()


_TELAS_H0030 = [
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_3x2",
    "h0030_matriz_2x4",
]


_GEO_H0030 = {
    "h0030_matriz_2x2": (2, 2),
    "h0030_matriz_3x2": (3, 2),
    "h0030_matriz_2x4": (2, 4),
}


_ALTURA_MATRIZ_H0030 = 24


class TestCatalogoH0030:
    """Renderizacao do catalogo H-0030 (5 telas permanentes).

    Cobre (H-0030 secoes 14.3 e 14.3-G):
    - renderizar_tela das 5 telas sem excecao e com saida nao vazia;
    - conteudo deterministico do console unico e do dashboard unico;
    - para cada matriz: quantidade de linhas/colunas de celulas, cobertura
      integral (todos os rotulos de posicao presentes), divisorias verticais
      e horizontais, ausencia de lacunas e de sobreposicoes;
    - largura alternativa 120 para cada matriz (sem excecao, mesmas regioes).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _carregar(self, id_tela):
        return construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))

    # ---------------------------------- 14.3: render sem excecao, nao vazio
    def test_renderizar_cinco_telas(self):
        for id_tela in _TELAS_H0030:
            modelo = self._carregar(id_tela)
            eh_matriz = id_tela in _GEO_H0030
            altura = _ALTURA_MATRIZ_H0030 if eh_matriz else 24
            try:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA, largura=80, altura=altura
                )
                ok = isinstance(saida, str) and saida != ""
            except Exception as exc:
                ok = False
                saida = ""
                detalhe = "{0}: {1}".format(type(exc).__name__, exc)
            else:
                detalhe = "len={0}".format(len(saida))
            self._r(
                "H-0030 render: renderizar_tela({0}) nao lanca e saida nao vazia".format(
                    id_tela
                ),
                ok,
                detalhe,
            )
            self._r(
                "H-0030 render: {0} saida nao e None".format(id_tela),
                saida is not None,
            )

    # ---------------------------------------------- 14.3: conteudo deterministico
    def test_console_unico_conteudo(self):
        modelo = self._carregar("h0030_console_unico")
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0030 render: console_unico exibe titulo 'CONSOLE'",
            "CONSOLE" in saida,
        )
        self._r(
            "H-0030 render: console_unico exibe placeholder '(console)'",
            "(console)" in saida,
        )
        self._r(
            "H-0030 render: console_unico exibe barra '[Esc] Voltar'",
            "[Esc] Voltar" in saida,
        )

    def test_dashboard_unico_conteudo(self):
        modelo = self._carregar("h0030_dashboard_unico")
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0030 render: dashboard_unico exibe 'dashboard único'",
            "dashboard único" in saida,
        )
        self._r(
            "H-0030 render: dashboard_unico exibe 'H-0030'",
            "H-0030" in saida,
        )
        self._r(
            "H-0030 render: dashboard_unico exibe titulo 'DASHBOARD'",
            "DASHBOARD" in saida,
        )

    # ---------------------------------------------- 14.3-G: geometria das matrizes
    def test_matrizes_geometria(self):
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            self._r(
                "H-0030 geo: {0} render sem excecao (largura=80)".format(id_matriz),
                isinstance(saida, str) and saida != "",
            )

            # Rotulos de posicao: cada celula declara "linha N, coluna M".
            rotulos_esperados = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos_esperados if r in saida}
            self._r(
                "H-0030 geo: {0} exibe todos os {1} rotulos de posicao".format(
                    id_matriz, n_linhas * n_colunas
                ),
                presentes == rotulos_esperados,
                "faltam={0!r}".format(sorted(rotulos_esperados - presentes)),
            )

            # Titulos das celulas ("L<n> C<m>") tambem aparecem.
            titulos_esperados = {
                "L{0} C{1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            titulos_presentes = {t for t in titulos_esperados if t in saida}
            self._r(
                "H-0030 geo: {0} exibe todos os titulos de celula (L<n> C<m>)".format(
                    id_matriz
                ),
                titulos_presentes == titulos_esperados,
                "faltam={0!r}".format(sorted(titulos_esperados - titulos_presentes)),
            )

            # Cobertura: cada rotulo aparece exatamente uma vez (sem duplicidade
            # de celula, sem lacuna).
            for rotulo in sorted(rotulos_esperados):
                self._r(
                    "H-0030 geo: {0} rotulo {1!r} aparece exatamente uma vez".format(
                        id_matriz, rotulo
                    ),
                    saida.count(rotulo) == 1,
                    "count={0}".format(saida.count(rotulo)),
                )

            # Quantidade de linhas de conteudo de celula: cada linha do grid
            # tem sua propria faixa horizontal de caixas. Conta-se quantas
            # linhas de texto possuem o rotulo de coluna 1 (borda esquerda da
            # primeira celula de cada linha).
            # Estrutura: cabecalho(3) + (n_linhas faixas) + barra(3).
            linhas = saida.split("\n")
            # Numero de linhas de grade = contagem de linhas que iniciam uma
            # caixa de celula na primeira coluna (topo "╭ L1 C1" etc.).
            inicioss = [
                i for i, l in enumerate(linhas)
                if l.startswith("╭ L") or l.startswith("┌ L")
            ]
            self._r(
                "H-0030 geo: {0} possui {1} linhas de celulas (faixas horizontais)".format(
                    id_matriz, n_linhas
                ),
                len(inicioss) == n_linhas,
                "inicios={0!r}".format(inicioss),
            )

            # Divisorias verticais: entre colunas adjacentes, cada linha de
            # conteudo possui bordas verticais nas coordenadas dos cortes.
            # Verifica-se que o numero de caixas por faixa (linha do grid)
            # equivale a n_colunas: cada faixa contem n_colunas rotulos de
            # titulo "L<n> C<m>".
            for i_linha, linha_grid in enumerate(inicioss, start=1):
                # Rotulos esperados nesta faixa (linha do grid = i_linha).
                titulos_linha = [
                    "L{0} C{1}".format(i_linha, co)
                    for co in range(1, n_colunas + 1)
                ]
                # A faixa vai do inicio atual ate o proximo inicio (ou ate a barra).
                fim_faixa = (
                    inicioss[i_linha] if i_linha < len(inicioss) else len(linhas)
                )
                bloco_faixa = "\n".join(linhas[linha_grid:fim_faixa])
                self._r(
                    "H-0030 geo: {0} faixa {1} contem {2} colunas (titulos L{1} C*)".format(
                        id_matriz, i_linha, n_colunas
                    ),
                    all(t in bloco_faixa for t in titulos_linha)
                    and len(titulos_linha) == n_colunas,
                    "faixa={0!r}".format(bloco_faixa[:60]),
                )

            # Divisoria horizontal: entre faixas verticais adjacentes deve
            # existir uma linha de borda (base da faixa superior/topo da
            # faixa inferior). Os proprios inicios das faixas (exceto a 1a)
            # marcam essa transicao; como cada faixa tem topo e base em
            # coordenadas compartilhadas, a existencia de >=2 faixas ja
            # implica ao menos uma divisoria horizontal central.
            if n_linhas >= 2:
                self._r(
                    "H-0030 geo: {0} tem divisoria horizontal (>=2 faixas empilhadas)".format(
                        id_matriz
                    ),
                    len(inicioss) >= 2,
                    "faixas={0}".format(len(inicioss)),
                )

            # Divisorias verticais: em largura 80 com n_colunas colunas iguais,
            # cada faixa possui n_colunas caixas lado a lado, separadas por
            # divisores verticais (╮╭ ou ┐┌). Verifica-se pela presenca do
            # padrao de juncao entre caixas ("╮╭" no conjunto curva).
            if n_colunas >= 2:
                padrao_juncao = "╮╭"
                tem_divisoria_vertical = padrao_juncao in saida
                self._r(
                    "H-0030 geo: {0} tem divisoria(s) vertical(is) entre colunas".format(
                        id_matriz
                    ),
                    tem_divisoria_vertical,
                    "padrao_juncao={0!r} presente={1}".format(
                        padrao_juncao, tem_divisoria_vertical
                    ),
                )

            # Ausencia de sobreposicao: cada titulo "L<n> C<m>" aparece uma
            # unica vez (ja verificado acima); como adicional, nenhum rotulo
            # de posicao se sobrepoe a outro na mesma linha (cada linha de
            # texto contem no maximo n_colunas rotulos). Verifica-se que nao
            # ha duas ocorrencias do mesmo rotulo na mesma linha visivel.
            sobreposicoes = 0
            for l in linhas:
                for rotulo in rotulos_esperados:
                    if l.count(rotulo) > 1:
                        sobreposicoes += 1
            self._r(
                "H-0030 geo: {0} sem sobreposicao de rotulos na mesma linha".format(
                    id_matriz
                ),
                sobreposicoes == 0,
                "sobreposicoes={0}".format(sobreposicoes),
            )

    def test_matrizes_geometria_coordenadas(self):
        """Fortalece test_matrizes_geometria com provas por coordenadas reais.

        As assercoes a seguir derivam as propriedades estruturais (faixas,
        colunas, bordas externas, cortes verticais, divisoria horizontal,
        alinhamento dos cortes entre faixas, pontos de encontro, contiguidade,
        ausencia de lacunas e de sobreposicao de retangulos) diretamente das
        posicoes dos caracteres de borda na saida renderizada. Nao reimplementam
        o algoritmo produtivo nem aceitam `len(faixas) >= 2` como prova de
        divisoria, nem duplicidade de rotulo como prova de ausencia de
        sobreposicao.
        """
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            linhas = saida.splitlines()
            corpo = _linhas_corpo_renderizado(saida)

            # 1. Quantidade correta de faixas de linhas: cada faixa comeca
            #    num caractere de topo de caixa ("╭"/"┌") na coluna 0.
            inicios_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╭") or l.startswith("┌")
            ]
            # 2. Quantidade correta de colunas por faixa: cada faixa termina
            #    num caractere de base de caixa ("╰"/"└") na coluna 0.
            fins_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╰") or l.startswith("└")
            ]
            self._r(
                "H-0030 geo-coord: {0} tem {1} faixas de linha".format(
                    id_matriz, n_linhas
                ),
                len(inicios_faixas) == n_linhas,
                "inicios={0!r} corpo={1}".format(inicios_faixas, len(corpo)),
            )
            self._r(
                "H-0030 geo-coord: {0} tem {1} bases de faixa".format(
                    id_matriz, n_linhas
                ),
                len(fins_faixas) == n_linhas,
                "fins={0!r}".format(fins_faixas),
            )

            # Faixas: lista de (inicio, fim) em indices do corpo.
            faixas = list(zip(inicios_faixas, fins_faixas))
            alturas_faixas = [fim - ini + 1 for ini, fim in faixas]

            # 10. Ausencia de linha vazia inesperada entre faixas: a base de
            #     uma faixa precede imediatamente o topo da seguinte.
            sem_linha_vazia = all(
                faixas[k][1] + 1 == faixas[k + 1][0]
                for k in range(len(faixas) - 1)
            )
            self._r(
                "H-0030 geo-coord: {0} sem linha vazia entre faixas".format(
                    id_matriz
                ),
                sem_linha_vazia,
                "alturas_faixas={0!r}".format(alturas_faixas),
            )

            # 3. Coordenadas das bordas externas (colunas e linhas do corpo).
            #    Coluna esquerda = 0; coluna direita = largura - 1.
            #    Linha do corpo de topo externo = inicios_faixas[0];
            #    linha de base externa = fins_faixas[-1].
            borda_esq = 0
            borda_dir = largura - 1
            self._r(
                "H-0030 geo-coord: {0} bordas externas col 0 e {1}".format(
                    id_matriz, borda_dir
                ),
                corpo[inicios_faixas[0]][borda_esq] in "╭┌"
                and corpo[fins_faixas[-1]][borda_esq] in "╰└"
                and corpo[inicios_faixas[0]][borda_dir] in "╮┐"
                and corpo[fins_faixas[-1]][borda_dir] in "╯┘",
                "externos=[{0},{1}]".format(
                    corpo[inicios_faixas[0]][0],
                    corpo[fins_faixas[-1]][-1],
                ),
            )

            # 4/6. Cortes verticais e alinhamento entre faixas: derivados das
            #      posicoes de borda de uma linha de conteudo de cada faixa.
            #      Os cortes internos (entre celulas) sao as colunas onde
            #      aparece "|" e que nao sao as bordas externas. O par (k, k+1)
            #      representa o encontro base/topo de caixas vizinhas; a coluna
            #      do corte interno e k+1 (ou k, dependendo da convensao); aqui
            #      verificamos o conjunto de colunas de borda que se repete em
            #      todas as faixas (alinhamento dos cortes).
            cortes_por_faixa = []
            for ini, fim in faixas:
                # Linha de conteudo valida: primeira linha apos o topo da faixa
                # que comeca com "│" e contem o rotulo de posicao.
                linhas_conteudo = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                self._r(
                    "H-0030 geo-coord: {0} faixa {1} tem linha de conteudo".format(
                        id_matriz, ini
                    ),
                    len(linhas_conteudo) >= 1,
                    "ini={0}".format(ini),
                )
                if not linhas_conteudo:
                    cortes_por_faixa.append(set())
                    continue
                pos = _posicoes_bordas_linha(linhas_conteudo[0])
                # Cortes internos = bordas verticais que nao sao os externos.
                cortes_internos = {
                    p for p in pos if p != borda_esq and p != borda_dir
                }
                cortes_por_faixa.append(cortes_internos)

            # 4. Coordenadas dos cortes verticais em cada faixa: o numero de
            #    cortes internos distintos por faixa deve ser 2*(n_colunas-1)
            #    (cada juncao entre duas caixas vizinhas gera um par de bordas
            #    em colunas adjacentes) — equivalente a n_colunas-1 divisores.
            for k_faixa, cortes in enumerate(cortes_por_faixa, start=1):
                # Agrupa colunas adjacentes em divisores: cada divisor ocupa
                # duas colunas consecutivas (parede direita de uma caixa e
                # parede esquerda da seguinte).
                ordenados = sorted(cortes)
                divisores = []
                i = 0
                while i < len(ordenados):
                    if i + 1 < len(ordenados) and ordenados[i + 1] - ordenados[i] == 1:
                        divisores.append((ordenados[i], ordenados[i + 1]))
                        i += 2
                    else:
                        divisores.append((ordenados[i], ordenados[i]))
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} faixa {1} tem {2} divisores verticais".format(
                        id_matriz, k_faixa, n_colunas - 1
                    ),
                    len(divisores) == n_colunas - 1,
                    "divisores={0!r} cortes={1!r}".format(divisores, ordenados),
                )

            # 6. Alinhamento dos cortes verticais entre as faixas: o conjunto
            #    de cortes internos deve ser identico em todas as faixas.
            alinhados = all(
                cortes == cortes_por_faixa[0] for cortes in cortes_por_faixa
            )
            self._r(
                "H-0030 geo-coord: {0} cortes verticais alinhados entre faixas".format(
                    id_matriz
                ),
                alinhados,
                "cortes_por_faixa={0!r}".format(cortes_por_faixa),
            )

            # 2 (reconfirmado). Colunas por faixa derivadas dos cortes internos
            #    da faixa 0: n_colunas = n_divisores + 1.
            if cortes_por_faixa:
                divisores_f0 = sorted(cortes_por_faixa[0])
                n_div = 0
                i = 0
                while i < len(divisores_f0):
                    if i + 1 < len(divisores_f0) and divisores_f0[i + 1] - divisores_f0[i] == 1:
                        n_div += 1
                        i += 2
                    else:
                        n_div += 1
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} colunas por faixa = {1}".format(
                        id_matriz, n_colunas
                    ),
                    n_div + 1 == n_colunas,
                    "n_divisores={0}".format(n_div),
                )

            # 5. Divisoria horizontal: a base da faixa superior e o topo da
            #    faixa inferior ficam em linhas consecutivas do corpo. A linha
            #    de base termina com "╰"/"└" e a linha seguinte comeca com
            #    "╭"/"┌" — isso prova uma divisoria horizontal real (nao apenas
            #    `len(faixas) >= 2`).
            divisorias_horizontais = 0
            for k in range(len(faixas) - 1):
                base = corpo[faixas[k][1]]
                topo_seg = corpo[faixas[k + 1][0]]
                if (base.startswith("╰") or base.startswith("└")) and (
                    topo_seg.startswith("╭") or topo_seg.startswith("┌")
                ) and faixas[k][1] + 1 == faixas[k + 1][0]:
                    divisorias_horizontais += 1
            self._r(
                "H-0030 geo-coord: {0} tem {1} divisoria(s) horizontal(is) por base/topo".format(
                    id_matriz, n_linhas - 1
                ),
                divisorias_horizontais == n_linhas - 1,
                "divisorias={0}".format(divisorias_horizontais),
            )

            # 7. Pontos de encontro entre bordas horizontais e verticais:
            #    no cruzamento de uma divisoria horizontal com um corte
            #    vertical, a coluna do corte na linha de base da faixa superior
            #    deve conter um caractere de borda (parede vertical cruza a
            #    base). Verifica-se para cada divisor da faixa superior.
            if cortes_por_faixa and n_linhas >= 2:
                base_faixa_sup = corpo[faixas[0][1]]
                cortes_sup = sorted(cortes_por_faixa[0])
                # colunas de borda presentes na linha de base
                bordas_base = _posicoes_bordas_linha(base_faixa_sup)
                # Cada divisor (par de colunas adjacentes) deve aparecer como
                # borda na linha de base (ponto de encontro).
                encontros = 0
                i = 0
                while i < len(cortes_sup):
                    if i + 1 < len(cortes_sup) and cortes_sup[i + 1] - cortes_sup[i] == 1:
                        if cortes_sup[i] in bordas_base and cortes_sup[i + 1] in bordas_base:
                            encontros += 1
                        i += 2
                    else:
                        if cortes_sup[i] in bordas_base:
                            encontros += 1
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} encontros HxV na divisoria horizontal".format(
                        id_matriz
                    ),
                    encontros == n_colunas - 1,
                    "encontros={0} bordas_base={1!r}".format(encontros, bordas_base),
                )

            # 8. Contiguidade entre caixas adjacentes: para cada faixa, em uma
            #    linha de conteudo, a parede direita de uma caixa (coluna k) e
            #    a parede esquerda da caixa seguinte (coluna k+1) devem ser
            #    consecutivas, sem coluna de espaco entre elas. Os cortes
            #    internos formam pares de colunas adjacentes (um divisor por
            #    juncao); dentro de cada par a distancia deve ser 1.
            contiguo = True
            detalhe_contig = []
            for ini, fim in faixas:
                linhas_c = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                if not linhas_c:
                    continue
                pos = _posicoes_bordas_linha(linhas_c[0])
                internos = sorted(
                    p for p in pos if p != borda_esq and p != borda_dir
                )
                # Agrupa internos em pares de colunas adjacentes (divisores).
                i = 0
                while i < len(internos):
                    if (
                        i + 1 < len(internos)
                        and internos[i + 1] - internos[i] == 1
                    ):
                        i += 2
                    else:
                        contiguo = False
                        detalhe_contig.append((ini, internos))
                        break
            self._r(
                "H-0030 geo-coord: {0} caixas adjacentes contiguas (sem coluna vazia)".format(
                    id_matriz
                ),
                contiguo,
                "quebras={0!r}".format(detalhe_contig),
            )

            # 9. Ausencia de coluna vazia inesperada entre caixas: derivado da
            #    contiguidade acima — reafirma em separado como cobertura 9.
            #    (Sempre passa se a contiguidade passar; registrado para fins
            #    de rastreabilidade da cobertura exigida.)
            self._r(
                "H-0030 geo-coord: {0} sem coluna vazia entre caixas".format(
                    id_matriz
                ),
                contiguo,
                "ver teste de contiguidade acima",
            )

            # 11/12. Cobertura integral + ausencia de sobreposicao entre
            #        retangulos de celulas distintas: constroi os retangulos
            #        (intervalos [linha, coluna]) de cada celula a partir dos
            #        cortes por faixa e verifica (a) que cobrem toda a regiao
            #        da matriz sem lacuna e (b) que retangulos distintos nao se
            #        intersectam.
            retangulos = []  # (linha_corpo_inicio, linha_corpo_fim, col_ini, col_fim)
            for (ini, fim), cortes in zip(faixas, cortes_por_faixa):
                ordenados = sorted(cortes)
                # Fronteiras de coluna: 0, depois os cortes agrupados em pares.
                fronteira = [borda_esq]
                i = 0
                while i < len(ordenados):
                    if i + 1 < len(ordenados) and ordenados[i + 1] - ordenados[i] == 1:
                        fronteira.append(ordenados[i + 1])
                        i += 2
                    else:
                        fronteira.append(ordenados[i])
                        i += 1
                fronteira.append(borda_dir)
                # Celulas: intervalos [fronteira[k], fronteira[k+1]].
                for k in range(len(fronteira) - 1):
                    retangulos.append(
                        (ini, fim, fronteira[k], fronteira[k + 1])
                    )

            # (a) Cobertura integral: numero de retangulos == n_linhas*n_colunas.
            self._r(
                "H-0030 geo-coord: {0} cobertura integral com {1} celulas".format(
                    id_matriz, n_linhas * n_colunas
                ),
                len(retangulos) == n_linhas * n_colunas,
                "retangulos={0}".format(len(retangulos)),
            )

            # (b) Ausencia de sobreposicao: retangulos distintos na mesma faixa
            #     nao compartilham colunas; retangulos em faixas distintas nao
            #     compartilham linhas. (As celulas sao disjuntas por
            #     construcao da grade.)
            sobreposicao = False
            for a in range(len(retangulos)):
                for b in range(a + 1, len(retangulos)):
                    la_i, la_f, ca_i, ca_f = retangulos[a]
                    lb_i, lb_f, cb_i, cb_f = retangulos[b]
                    # Intersecao de intervalos (linha e coluna).
                    inter_linha = not (la_f < lb_i or lb_f < la_i)
                    inter_coluna = not (ca_f < cb_i or cb_f < ca_i)
                    if inter_linha and inter_coluna:
                        # Tolerancia: as paredes compartilhadas (limite
                        # comum) nao sao sobreposicao de area. Ha
                        # sobreposicao real apenas se houver area interna
                        # comum, i.e., mais do que a parede divisoria.
                        area_comum = (
                            (min(la_f, lb_f) - max(la_i, lb_i))
                            * (min(ca_f, cb_f) - max(ca_i, cb_i))
                        )
                        if area_comum > 0:
                            sobreposicao = True
            self._r(
                "H-0030 geo-coord: {0} sem sobreposicao de retangulos distintos".format(
                    id_matriz
                ),
                not sobreposicao,
                "sobreposicao={0}".format(sobreposicao),
            )

            # (c) Contiguidade vertical entre faixas: a faixa k termina na
            #     linha imediatamente anterior ao inicio da faixa k+1.
            self._r(
                "H-0030 geo-coord: {0} faixas contiguas verticalmente".format(
                    id_matriz
                ),
                all(
                    faixas[k][1] + 1 == faixas[k + 1][0]
                    for k in range(len(faixas) - 1)
                ),
                "faixas={0!r}".format(faixas),
            )

            # 13. Preservacao dos rotulos e titulos esperados: ja coberto em
            #     test_matrizes_geometria; reafirma cobertura integral dos
            #     rotulos de posicao aqui como parte da prova por coordenadas.
            rotulos = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos if r in saida}
            self._r(
                "H-0030 geo-coord: {0} preserva todos os rotulos de posicao".format(
                    id_matriz
                ),
                presentes == rotulos,
                "faltam={0!r}".format(sorted(rotulos - presentes)),
            )

            # 14. Largura padrao prevista: toda linha nao-vazia tem largura 80.
            larguras_linhas = {len(l) for l in linhas if l != ""}
            self._r(
                "H-0030 geo-coord: {0} largura 80 em todas as linhas".format(
                    id_matriz
                ),
                larguras_linhas == {80},
                "larguras={0!r}".format(sorted(larguras_linhas)),
            )

            # Cada rotulo aparece exatamente uma vez (sem celula duplicada nem
            # ausente) — cobertura adicional derivada por contagem.
            unicidade = all(saida.count(r) == 1 for r in rotulos)
            self._r(
                "H-0030 geo-coord: {0} cada rotulo aparece exatamente uma vez".format(
                    id_matriz
                ),
                unicidade,
                "contagens={0!r}".format(
                    {r: saida.count(r) for r in sorted(rotulos)}
                ),
            )

    def test_matrizes_cortes_distribuicao_igual(self):
        """Prova os cortes verticais contra coordenadas esperadas da distribuicao igual.

        Cobre a pendencia residual do achado QA-IMP-H0030-MEDIO-001 identificada
        pelo QA pos-patch (RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md, secao 5):

        (i)  a cobertura anterior derivava os cortes da propria saida e verificava
             apenas quantidade e alinhamento entre faixas, sem exigir os valores
             esperados para distribuicao igual. Um corte vertical deslocado de
             forma consistente poderia passar.
        (ii) a verificacao de encontros HxV contra a linha de base era pouco
             discriminante, pois `_posicoes_bordas_linha` tambem considera o
             caractere horizontal `─`, de modo que uma base horizontal completa
             tende a conter qualquer coluna de corte deslocado.

        As assercoes a seguir derivam as coordenadas esperadas da largura e do
        numero de colunas (independente do algoritmo produtivo e da propria
        saida) e comprovam duas propriedades geométricas independentes:

        1. Os cortes verticais internos caem exatamente nas colunas exigidas
           pela distribuicao igual em largura 80: cada par (k*passo-1, k*passo)
           com passo = largura // n_colunas. Para 2 colunas -> (39,40); para
           4 colunas -> (19,20),(39,40),(59,60). Um corte deslocado falha.
        2. O encontro entre a divisoria vertical e a divisoria horizontal (HxV)
           ocorre em caracteres de quina (╮╭ no topo, ╯╰ na base) e nunca em
           traco horizontal `─`. Isso torna a prova especifica: se o corte
           estiver deslocado para uma coluna de base preenchida por `─`, o par
           esperado nao aparecera como quina.
        """
        # Quinas de juncao entre faixas horizontais: o corte vertical de cada
        # coluna divide a borda de topo (╮╭) e a borda de base (╯╰) em pares
        # de quinas adjacentes. O traco horizontal `─` nao e quina.
        quinas_topo = ("╮", "╭")
        quinas_base = ("╯", "╰")
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            corpo = _linhas_corpo_renderizado(saida)

            # Faixas (inicio, fim) a partir de topo/base na coluna 0.
            inicios_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╭") or l.startswith("┌")
            ]
            fins_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╰") or l.startswith("└")
            ]
            faixas = list(zip(inicios_faixas, fins_faixas))

            # Coordenadas esperadas dos cortes internos para distribuicao igual.
            # Invariante geometrico: em largura L com C colunas iguais, o k-esimo
            # corte cai entre as colunas (k*L//C - 1) e (k*L//C), formando um par
            # de paredes adjacentes. O algoritmo produtivo nao e consultado; os
            # valores derivam somente de L e C.
            passo = largura // n_colunas
            cortes_esperados = [
                (k * passo - 1, k * passo) for k in range(1, n_colunas)
            ]

            # Propriedade 1 (corte deslocado): para cada faixa, a linha de
            # conteudo apresenta exatamente os pares de colunas esperados como
            # paredes verticais internas. Extrai-se as paredes (apenas "|") em
            # colunas internas e agrupa-se em pares adjacentes; o conjunto
            # resultante deve ser igual ao esperado.
            for k_faixa, (ini, fim) in enumerate(faixas, start=1):
                linhas_c = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                # Colunas com parede vertical "|" (nao qualquer caractere de
                # borda): isso isola as paredes laterais das celulas.
                paredes = [
                    p for p, ch in enumerate(linhas_c[0])
                    if ch == "│" and 0 < p < largura - 1
                ]
                ordenados = sorted(paredes)
                pares = []
                i = 0
                while i < len(ordenados):
                    if (
                        i + 1 < len(ordenados)
                        and ordenados[i + 1] - ordenados[i] == 1
                    ):
                        pares.append((ordenados[i], ordenados[i + 1]))
                        i += 2
                    else:
                        pares.append((ordenados[i], ordenados[i]))
                        i += 1
                self._r(
                    "H-0030 geo-igual: {0} faixa {1} cortes internos nas "
                    "colunas esperadas {2}".format(
                        id_matriz, k_faixa, cortes_esperados
                    ),
                    pares == cortes_esperados,
                    "pares={0!r} esperados={1!r}".format(pares, cortes_esperados),
                )

            # Propriedade 2 (encontro HxV especifico): na divisoria horizontal
            # entre cada par de faixas vizinhas, cada corte interno esperado
            # aparece como um par de quinas adjacentes (╮╭ no topo da faixa
            # inferior e ╯╰ na base da faixa superior), nunca como `─`. Isso
            # prova que o corte vertical realmente cruza a divisoria horizontal
            # numa interseccao de quina, e nao apenas numa coluna qualquer de
            # uma base horizontal completa.
            for k in range(len(faixas) - 1):
                base_sup = corpo[faixas[k][1]]
                topo_inf = corpo[faixas[k + 1][0]]
                for (c_esq, c_dir) in cortes_esperados:
                    par_base = (base_sup[c_esq], base_sup[c_dir])
                    par_topo = (topo_inf[c_esq], topo_inf[c_dir])
                    self._r(
                        "H-0030 geo-igual: {0} div.h.{1} corte {2},{3} "
                        "quina base (╯╰)".format(
                            id_matriz, k + 1, c_esq, c_dir
                        ),
                        par_base == quinas_base,
                        "par_base={0!r}".format(par_base),
                    )
                    self._r(
                        "H-0030 geo-igual: {0} div.h.{1} corte {2},{3} "
                        "quina topo (╮╭)".format(
                            id_matriz, k + 1, c_esq, c_dir
                        ),
                        par_topo == quinas_topo,
                        "par_topo={0!r}".format(par_topo),
                    )

            # Regressao explicita de lacuna/coluna vazia no corte: a coluna
            # imediatamente anterior (c_esq) e a imediatamente posterior (c_dir)
            # a um corte esperado devem ambas conter parede vertical numa linha
            # de conteudo; se o renderer inserir um espaco em branco em uma das
            # duas, a contiguidade entre caixas vizinhas esta quebrada.
            ini0, fim0 = faixas[0]
            conteudo0 = [
                corpo[i] for i in range(ini0 + 1, fim0)
                if corpo[i].startswith("│") and "linha" in corpo[i]
            ][0]
            for (c_esq, c_dir) in cortes_esperados:
                self._r(
                    "H-0030 geo-igual: {0} corte {1},{2} sem coluna vazia "
                    "(paredes nas duas colunas)".format(
                        id_matriz, c_esq, c_dir
                    ),
                    conteudo0[c_esq] == "│" and conteudo0[c_dir] == "│",
                    "chars={0!r}".format(
                        (conteudo0[c_esq], conteudo0[c_dir])
                    ),
                )

    def test_matrizes_largura_alternativa_120(self):
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            try:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA, largura=120,
                    altura=_ALTURA_MATRIZ_H0030,
                )
                ok = isinstance(saida, str) and saida != ""
            except Exception as exc:
                ok = False
                detalhe = "{0}: {1}".format(type(exc).__name__, exc)
            else:
                detalhe = "len={0}".format(len(saida))
            self._r(
                "H-0030 geo: {0} largura=120 nao lanca excecao".format(id_matriz),
                ok,
                detalhe,
            )
            # Largura 120 mantem o mesmo numero de regioes de celula.
            rotulos_esperados = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos_esperados if r in saida}
            self._r(
                "H-0030 geo: {0} largura=120 mantem {1} regioes de celula".format(
                    id_matriz, n_linhas * n_colunas
                ),
                presentes == rotulos_esperados,
                "faltam={0!r}".format(sorted(rotulos_esperados - presentes)),
            )
            # Cada linha nao-vazia tem exatamente 120 chars.
            self._r(
                "H-0030 geo: {0} largura=120: linhas nao-vazias tem 120 chars".format(
                    id_matriz
                ),
                all(len(ln) == 120 for ln in saida.split("\n") if ln != ""),
                "larguras={0}".format(
                    sorted({len(ln) for ln in saida.split("\n") if ln != ""})
                ),
            )

    def test_preservacao_telas_anteriores(self):
        """Telas anteriores continuam renderizando sem regressao."""
        for id_perm in ("destino_minimo", "grupo_minimo", "demo"):
            modelo = self._carregar(id_perm)
            try:
                saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=42)
                ok = isinstance(saida, str) and saida != ""
            except Exception:
                ok = False
            self._r(
                "H-0030 render: tela anterior {0} ainda renderiza".format(id_perm),
                ok,
            )

    def run_all(self):
        print("")
        print("== TestCatalogoH0030: render do catalogo de 5 telas permanentes ==")
        self.test_renderizar_cinco_telas()
        self.test_console_unico_conteudo()
        self.test_dashboard_unico_conteudo()
        self.test_matrizes_geometria()
        self.test_matrizes_geometria_coordenadas()
        self.test_matrizes_cortes_distribuicao_igual()
        self.test_matrizes_largura_alternativa_120()
        self.test_preservacao_telas_anteriores()


class TestDistribuicaoMatricialH0035:
    """Integracao do renderer com distribuicao_matricial (H-0035 / ADR-0025).

    Cobre (contrato H-0035 secoes 37.3-37.6): dashboard com e sem o campo;
    console substituindo politicas geometricas quando presente e preservando-as
    quando ausente; lancador com precedencia quando presente e ADR-0001/2/3
    preservados quando ausente; compatibilidade (ausencia = comportamento
    anterior); fallback via quadro minimo; ausencia de dupla autoridade.

    Expectativas geometricas derivadas por geometria fechada, nao pelo proprio
    algoritmo de producao.
    """

    def _dm(self, **over):
        base = {
            "formacao": {"politica": "matriz_fixa",
                         "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
            "ordem": "por_linha",
            "dimensionamento": {
                "colunas": {"politica": "minimo_fixo", "minimo": 5},
                "linhas": {"politica": "minimo_fixo", "minimo": 1},
            },
            "espacamento": {
                "margem_superior": {"minimo": 0},
                "margem_inferior": {"minimo": 0},
                "margem_esquerda": {"minimo": 0},
                "margem_direita": {"minimo": 0},
                "vao_horizontal": {"minimo": 1},
                "vao_vertical": {"minimo": 0},
            },
            "distribuicao_horizontal": {"politica": "inicio"},
            "distribuicao_vertical": {"politica": "inicio"},
            "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos",
                               "vertical": "uniforme_margens_e_vaos"},
            "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
            "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
        }
        base.update(over)
        return base

    def _modelo_dashboard(self, com_dm):
        campos = [
            {"id": "c1", "rotulo": "", "fonte": "literal", "valor": "AA"},
            {"id": "c2", "rotulo": "", "fonte": "literal", "valor": "BB"},
            {"id": "c3", "rotulo": "", "fonte": "literal", "valor": "CC"},
            {"id": "c4", "rotulo": "", "fonte": "literal", "valor": "DD"},
        ]
        el = ElementoCorpo(
            id="dash", tipo="dashboard",
            _campos_inertes={"titulo": "Grade", "campos": campos},
            distribuicao_matricial=self._dm() if com_dm else None,
        )
        corpo = Corpo(arranjo="vertical",
                      elementos=[el],
                      distribuicao={"modo": "igual"})
        return ModeloTela(
            id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=corpo,
            barra_de_menus={"chips": [
                {"id": "e", "tipo": "acao", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )

    def test_dashboard_com_grade(self):
        # 2x2, coluna largura 5, vao_h 1, ordem por_linha, alinhamento inicio.
        # Participante 0 "AA" em (0,0) x=0; participante 1 "BB" em (0,1) x=6.
        # Linha 0 do corpo: "AA" nas colunas 0-1 e "BB" a partir da coluna 6.
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        linhas = saida.split("\n")
        # Localiza a caixa GRADE.
        idx = next(i for i, l in enumerate(linhas) if "GRADE" in l)
        # Primeira linha de conteudo do dashboard.
        conteudo0 = linhas[idx + 1]
        # Formato de _linha_conteudo: "│ " + content + "│".
        corpo0 = conteudo0[2:2 + 39]
        ok_aa = corpo0[0:2] == "AA"
        ok_bb = corpo0[6:8] == "BB"
        _registrar("H0035 dashboard grade AA@0 BB@6",
                   ok_aa and ok_bb, repr(corpo0[:10]))
        conteudo1 = linhas[idx + 2]
        corpo1 = conteudo1[2:2 + 39]
        ok_cc = corpo1[0:2] == "CC"
        ok_dd = corpo1[6:8] == "DD"
        _registrar("H0035 dashboard grade CC/DD segunda linha",
                   ok_cc and ok_dd, repr(corpo1[:10]))

    def test_dashboard_sem_preserva(self):
        # Sem o campo: comportamento anterior (uma linha por campo literal).
        m = self._modelo_dashboard(com_dm=False)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        # Cada valor aparece em sua propria linha (comportamento _linhas_dashboard).
        _registrar("H0035 dashboard sem campo preserva (AA e BB em linhas)",
                   "│ AA " in saida and "│ BB " in saida)

    def test_ordem_preservada(self):
        # A grade nao reordena; participantes preservam a sequencia declarada.
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        pos_aa = saida.find("AA")
        pos_bb = saida.find("BB")
        pos_cc = saida.find("CC")
        pos_dd = saida.find("DD")
        _registrar("H0035 ordem preservada AA<BB<CC<DD",
                   pos_aa < pos_bb < pos_cc < pos_dd,
                   "{0},{1},{2},{3}".format(pos_aa, pos_bb, pos_cc, pos_dd))

    def test_sem_perda_nem_duplicacao(self):
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        _registrar("H0035 dashboard sem perda",
                   all(saida.count(v) == 1 for v in ("AA", "BB", "CC", "DD")))

    def test_console_com_substitui(self):
        itens = [
            {"id": "l1", "texto": "XX"},
            {"id": "l2", "texto": "YY"},
        ]
        el = ElementoCorpo(
            id="con", tipo="console",
            _campos_inertes={"titulo": "Console", "itens": itens},
            distribuicao_matricial=self._dm(
                formacao={"politica": "matriz_fixa",
                          "linhas": {"fixo": 1}, "colunas": {"fixo": 2}}),
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        m = ModeloTela(id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=12)
        # Com a grade, XX e YY aparecem lado a lado na mesma linha (1x2).
        for l in saida.split("\n"):
            if "XX" in l and "YY" in l:
                _registrar("H0035 console com: XX e YY na mesma linha (grade)",
                           True)
                break
        else:
            _registrar("H0035 console com: XX e YY na mesma linha (grade)", False)

    def test_console_sem_preserva(self):
        # Sem o campo, console mantem o placeholder de escopo "(console)".
        el = ElementoCorpo(
            id="con", tipo="console",
            _campos_inertes={"titulo": "Console"},
        )
        corpo = Corpo(arranjo="vertical", elementos=[el], distribuicao=None)
        m = ModeloTela(id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42)
        _registrar("H0035 console sem campo preserva placeholder",
                   "(console)" in saida)

    def _modelo_lancador(self, com_dm):
        itens = [
            {"id": "i1", "chip": "A", "texto": "um", "tela_destino": "t"},
            {"id": "i2", "chip": "B", "texto": "do", "tela_destino": "t"},
            {"id": "i3", "chip": "C", "texto": "tr", "tela_destino": "t"},
            {"id": "i4", "chip": "D", "texto": "qu", "tela_destino": "t"},
        ]
        params = {
            "vaos": {
                "chip_texto": {"minimo": 1, "maximo": 3},
                "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
            },
            "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            "verificacao": {"texto": {"max_caracteres": 15}},
        }
        el = ElementoCorpo(
            id="lan", tipo="lancador",
            _campos_inertes={"titulo": "Lancador", "itens": itens},
            parametros_tipo=params,
            distribuicao_matricial=self._dm(
                dimensionamento={
                    "colunas": {"politica": "maior_da_coluna"},
                    "linhas": {"politica": "minimo_fixo", "minimo": 1}},
            ) if com_dm else None,
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        return ModeloTela(id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                          corpo=corpo,
                          barra_de_menus={"chips": [
                              {"id": "e", "tipo": "acao", "tecla": "Esc",
                               "texto": "Sair"}]},
                          _raw={})

    def test_lancador_com_precedencia(self):
        # Com o campo: grade 2x2 por_linha. [A] um e [B] do na primeira linha.
        m = self._modelo_lancador(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        achou = False
        for l in saida.split("\n"):
            if "[A] um" in l and "[B] do" in l:
                achou = True
                break
        _registrar("H0035 lancador com: [A] um e [B] do na mesma linha", achou)

    def test_lancador_sem_preserva(self):
        # Sem o campo: politica historica (ADR-0001/2/3). Todos os itens numa
        # unica fila (cabendo em 42 chars) — comportamento _linhas_lancador.
        m = self._modelo_lancador(com_dm=False)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        # Fila: todos os quatro itens na mesma linha.
        achou_fila = False
        for l in saida.split("\n"):
            if all(t in l for t in ("[A] um", "[B] do", "[C] tr", "[D] qu")):
                achou_fila = True
                break
        _registrar("H0035 lancador sem campo preserva fila historica",
                   achou_fila)

    def test_fallback_quadro_minimo(self):
        # Grade que nao cabe -> quadro minimo canonico global.
        el = ElementoCorpo(
            id="dash", tipo="dashboard",
            _campos_inertes={"titulo": "Grade", "campos": [
                {"id": "c1", "rotulo": "", "fonte": "literal", "valor": "X"},
                {"id": "c2", "rotulo": "", "fonte": "literal", "valor": "Y"},
            ]},
            distribuicao_matricial=self._dm(
                formacao={"politica": "matriz_fixa",
                          "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
                dimensionamento={
                    "colunas": {"politica": "minimo_fixo", "minimo": 40},
                    "linhas": {"politica": "minimo_fixo", "minimo": 1}}),
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        m = ModeloTela(id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        _registrar("H0035 fallback -> quadro minimo canonico",
                   "terminal pequeno demais" in saida and "GRADE" not in saida)

    def test_telas_permanentes_carregam(self):
        # As telas h0035_* de conteudo carregam e renderizam pelo pipeline.
        ids = [
            "h0035_pref_linhas", "h0035_pref_colunas", "h0035_matriz_fixa_cabe",
            "h0035_uma_linha", "h0035_uma_coluna", "h0035_console_com",
            "h0035_console_sem", "h0035_lancador_com", "h0035_lancador_sem",
            "h0035_dashboard_com", "h0035_dashboard_sem",
            "h0035_minimo_fixo_excedido", "h0035_tres_centralizados",
        ]
        todas_ok = True
        for id_tela in ids:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=44, altura=16)
                if saida.count("\n") != 16:
                    todas_ok = False
            except Exception as exc:  # pragma: no cover
                todas_ok = False
                _registrar("H0035 tela permanente {0}".format(id_tela),
                           False, "{0}: {1}".format(type(exc).__name__, exc))
        _registrar("H0035 telas permanentes carregam e renderizam", todas_ok)

    def test_minimo_fixo_nao_cresce(self):
        # DEC-APP-0025-01: coluna minimo_fixo=5 nao cresce por conteudo maior.
        # 1x1, participante "ABCDEFGH" (8) em coluna de 5: coluna permanece 5.
        # Prova comportamental: fronteira interna recebe o conteudo integral.
        import inspect
        import importlib
        _mod = importlib.import_module("tela.renderizacao.matriz_participantes")
        chamadas = []
        _original = _mod._renderizar_participante_na_celula

        def _espiao(canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
                    canvas_h, area_w, alinh_h, alinh_v):
            chamadas.append({
                "texto_integral": texto_integral,
                "cel_w": cel_w,
                "cel_h": cel_h,
            })
            return _original(
                canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
                canvas_h, area_w, alinh_h, alinh_v,
            )

        _mod._renderizar_participante_na_celula = _espiao
        try:
            el = ElementoCorpo(
                id="dash", tipo="dashboard",
                _campos_inertes={"titulo": "Grade", "campos": [
                    {"id": "c1", "rotulo": "", "fonte": "literal",
                     "valor": "ABCDEFGH"}]},
                distribuicao_matricial=self._dm(
                    formacao={"politica": "matriz_fixa",
                              "linhas": {"fixo": 1}, "colunas": {"fixo": 1}},
                    dimensionamento={
                        "colunas": {"politica": "minimo_fixo", "minimo": 5},
                        "linhas": {"politica": "minimo_fixo", "minimo": 1}},
                    distribuicao_horizontal={"politica": "inicio"}),
            )
            corpo = Corpo(arranjo="vertical", elementos=[el],
                          distribuicao={"modo": "igual"})
            m = ModeloTela(id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                           corpo=corpo,
                           barra_de_menus={"chips": [
                               {"id": "e", "tipo": "acao", "tecla": "Esc",
                                "texto": "Sair"}]},
                           _raw={})
            saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=12)
            linhas = saida.split("\n")
            # 1: Formacao valida (grade renderizada).
            idx = next((i for i, l in enumerate(linhas) if "GRADE" in l), -1)
            _registrar("H0035 minimo_fixo: formacao externa valida",
                       idx >= 0, "idx GRADE = {0}".format(idx))
            # 2: Fronteira interna foi chamada pelo distribuidor externo.
            _registrar(
                "H0035 minimo_fixo: fronteira interna chamada",
                len(chamadas) >= 1,
                "chamadas = {0}".format(len(chamadas)),
            )
            # 3: Conteudo integral "ABCDEFGH" recebido pela fronteira interna.
            conteudo_recebido = chamadas[0]["texto_integral"] if chamadas else ""
            _registrar(
                "H0035 minimo_fixo: conteudo integral ABCDEFGH recebido",
                conteudo_recebido == "ABCDEFGH",
                "recebido = {0!r}".format(conteudo_recebido),
            )
            # 4: Largura da celula recebida e 5 (dimensao externa nao cresceu).
            cel_w_recebida = chamadas[0]["cel_w"] if chamadas else -1
            _registrar(
                "H0035 minimo_fixo: largura da celula e 5",
                cel_w_recebida == 5,
                "cel_w = {0}".format(cel_w_recebida),
            )
            # 5: Auxiliar — sem [:cel_w] no corpo da funcao matricial externa.
            from tela.renderizador import _linhas_distribuicao_matricial as _ldm
            fonte = inspect.getsource(_ldm)
            _registrar(
                "H0035 minimo_fixo: [:cel_w] ausente na camada matricial (auxiliar)",
                "[:cel_w]" not in fonte,
                "[:cel_w] no fonte = {0}".format("[:cel_w]" in fonte),
            )
        finally:
            _mod._renderizar_participante_na_celula = _original

    def test_fronteira_interna_celula(self):
        # Prova direta de _renderizar_participante_na_celula:
        # recebe conteudo integral, respeita a area fisica, nao invade vizinha.
        from tela.renderizador import _renderizar_participante_na_celula
        # Canvas 10 colunas x 1 linha; celula largura 5 em x=0.
        canvas = [[" "] * 10]
        _renderizar_participante_na_celula(
            canvas=canvas,
            texto_integral="ABCDEFGH",
            cel_x=0, cel_y=0, cel_w=5, cel_h=1,
            canvas_h=1, area_w=10,
            alinh_h="inicio", alinh_v="topo",
        )
        linha = "".join(canvas[0])
        _registrar(
            "H0035 fronteira_interna: primeiros 5 chars escritos na celula",
            linha[:5] == "ABCDE",
            "canvas = {0!r}".format(linha),
        )
        _registrar(
            "H0035 fronteira_interna: celula vizinha nao invadida (pos 5-9)",
            linha[5:] == "     ",
            "pos5-9 = {0!r}".format(linha[5:]),
        )
        # Celula em x=5: conteudo breve nao invade celula em x=0.
        canvas2 = [[" "] * 10]
        _renderizar_participante_na_celula(
            canvas=canvas2,
            texto_integral="XY",
            cel_x=5, cel_y=0, cel_w=5, cel_h=1,
            canvas_h=1, area_w=10,
            alinh_h="inicio", alinh_v="topo",
        )
        linha2 = "".join(canvas2[0])
        _registrar(
            "H0035 fronteira_interna: vizinha direita nao invade esquerda",
            linha2[:5] == "     " and linha2[5:7] == "XY",
            "canvas = {0!r}".format(linha2),
        )

    def run_all(self):
        self.test_dashboard_com_grade()
        self.test_dashboard_sem_preserva()
        self.test_ordem_preservada()
        self.test_sem_perda_nem_duplicacao()
        self.test_console_com_substitui()
        self.test_console_sem_preserva()
        self.test_lancador_com_precedencia()
        self.test_lancador_sem_preserva()
        self.test_fallback_quadro_minimo()
        self.test_telas_permanentes_carregam()
        self.test_minimo_fixo_nao_cresce()
        self.test_fronteira_interna_celula()
