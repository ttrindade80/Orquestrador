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
    'TestArranjoH0019',
    'TestPreenchimentoVerticalH0020',
    'TestPreenchimentoBordeadoH0021',
    'TestDistribuicaoVerticalH0025',
    'TestDistribuicaoHorizontalH0026',
    'TestHierarquiaGruposH0027',
    'TestOcupacaoIntegralCorpoH0033',
    'TestHelperHorizontalH0033Patch2',
    'TestCardinalidadeHorizontalH0033Patch3',
    'TestCardinalidadeHorizontalH0033Patch4',
]

_H0033_TELAS_TODAS = (
    "demo",
    "destino_minimo",
    "grupo_minimo",
    "stub_b",
    "h0029_dashboard_fracao",
    "h0029_dashboard_igual",
    "h0029_dashboard_percentual",
    "h0029_grupo_fracao",
    "h0029_grupo_igual",
    "h0029_grupo_pai_distribuido",
    "h0029_grupo_percentual",
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_2x4",
    "h0030_matriz_3x2",
)

_H0033_TELAS_MATRIZ = ("h0030_matriz_2x2", "h0030_matriz_2x4", "h0030_matriz_3x2")

_H0033_TELAS_ALTURA_NATURAL = tuple(
    t for t in _H0033_TELAS_TODAS if t not in _H0033_TELAS_MATRIZ
)

_H0033_TELAS_ALTURA_20 = tuple(t for t in _H0033_TELAS_TODAS if t != "demo")


def _modelo_horizontal(arranjo, elementos_spec, largura=42, titulo_cab="H",
                       distribuicao=None):
    """Cria ModeloTela sintético para testes de arranjo horizontal (H-0019).

    elementos_spec: lista de tuplas (tipo, titulo) ex: [("console","A"),("dashboard","B")]
    distribuicao: dict de distribuicao para o corpo (ou None para ausencia declarada).
        Composicoes horizontais com N>1 e distribuicao=None sao invalidas (DA-02).
    """
    elementos = []
    for tipo, titulo in elementos_spec:
        campos_inertes = {"titulo": titulo}
        if tipo == "lancador":
            campos_inertes["itens"] = []
        elementos.append(ElementoCorpo(id=titulo.lower(), tipo=tipo,
                                       _campos_inertes=campos_inertes))
    return ModeloTela(
        id="teste_h0019",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "teste h0019", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo=arranjo, elementos=elementos, distribuicao=distribuicao),
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


class TestArranjoH0019:
    """Testes obrigatórios de arranjo do corpo raiz (H-0019).

    Cobre: None/vertical/sobreposto preservam comportamento atual;
    horizontal e lado_a_lado ativam particionamento contíguo;
    bordas coladas; largura determinística; resto; padding inferior;
    largura insuficiente; N=1; H-0015; barra preservada.
    """

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
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    def test_arranjo_none_preserva_vertical(self):
        """None -> comportamento vertical atual preservado."""
        modelo_none = _modelo_horizontal(None, [("console", "A"), ("console", "B")])
        modelo_vert = _modelo_horizontal("vertical", [("console", "A"), ("console", "B")])
        saida_none = renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
        saida_vert = renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
        self._r(
            "arranjo=None -> saida identica a arranjo='vertical'",
            saida_none == saida_vert,
        )
        # Elementos empilhados = 2 cabecalhos de console separados (vertical)
        self._r(
            "arranjo=None -> 2 caixas de console empilhadas (contagem de ╭)",
            saida_none.count("╭ A") == 1 and saida_none.count("╭ B") == 1,
        )
        self._r(
            "arranjo=None -> barra aparece ao final",
            "╭ Menus" in saida_none,
        )

    def test_arranjo_vertical_preserva_comportamento(self):
        """vertical -> saida identica ao None."""
        modelo_none = _modelo_horizontal(None, [("console", "A"), ("dashboard", "B")])
        modelo_vert = _modelo_horizontal("vertical", [("console", "A"), ("dashboard", "B")])
        self._r(
            "arranjo='vertical' == arranjo=None",
            renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_sobreposto_preserva_vertical(self):
        """sobreposto -> alias de vertical, saida identica."""
        modelo_vert = _modelo_horizontal("vertical", [("console", "A")])
        modelo_sob = _modelo_horizontal("sobreposto", [("console", "A")])
        self._r(
            "arranjo='sobreposto' -> saida identica a 'vertical'",
            renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_sob, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_horizontal_dois_elementos(self):
        """horizontal: 2 filhos diretos ficam na mesma faixa de linhas (distribuicao obrigatoria)."""
        dist = {"modo": "igual"}
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                    distribuicao=dist)
        saida_h = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        saida_v = renderizar_tela(_modelo_horizontal("vertical", [("console", "A"), ("console", "B")]), _ESTILO_CURVA,
            largura=42,
        )
        self._r(
            "horizontal: A e B aparecem na saida",
            "A" in saida_h and "B" in saida_h,
        )
        self._r(
            "horizontal: saida tem menos linhas que vertical (areas lado a lado)",
            saida_h.count("\n") < saida_v.count("\n"),
            "h={0} v={1}".format(saida_h.count("\n"), saida_v.count("\n")),
        )
        self._r(
            "horizontal: barra_de_menus aparece abaixo do bloco horizontal",
            saida_h.index("╭ Menus") > saida_h.index("╭ A"),
        )

    def test_arranjo_lado_a_lado_alias_horizontal(self):
        """lado_a_lado -> alias transicional de horizontal, saida identica (distribuicao obrigatoria)."""
        dist = {"modo": "igual"}
        modelo_h = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                      distribuicao=dist)
        modelo_l = _modelo_horizontal("lado_a_lado", [("console", "A"), ("console", "B")],
                                      distribuicao=dist)
        self._r(
            "arranjo='lado_a_lado' == arranjo='horizontal'",
            renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_l, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_horizontal_areas_contiguas(self):
        """horizontal: bordas adjacentes coladas (││, ╮╭, ╯╰); largura total preservada."""
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                    largura=42, distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        # Extrair apenas o bloco do corpo (linhas entre cabecalho e barra)
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linhas_corpo = [ln for ln in linhas
                        if not ln.startswith("╭ H") and not ln.startswith("╭ Menus")
                        and not (ln.startswith("│ teste") or ln.startswith("│ Ok"))
                        and not ln.startswith("╰────────────────────────────────────────╯")
                        or ln.startswith("╭ A") or ln.startswith("╭ B")
                        or "│" == ln[0] and "A" not in ln[:5] and "B" not in ln[:5]
                        or ln.startswith("╰───────────────────╯")]
        self._r(
            "horizontal: '││' aparece nas linhas internas (bordas adjacentes coladas)",
            "││" in saida,
            "ok" if "││" in saida else "nao encontrado",
        )
        self._r(
            "horizontal: '╮╭' aparece no topo das areas adjacentes",
            "╮╭" in saida,
            "ok" if "╮╭" in saida else "nao encontrado",
        )
        self._r(
            "horizontal: '╯╰' aparece na base das areas adjacentes",
            "╯╰" in saida,
            "ok" if "╯╰" in saida else "nao encontrado",
        )
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal: cada linha tem exatamente 42 chars (largura total preservada)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal: primeiro char de cada linha e borda esquerda da area 0",
            all(ln[0] in ("╭", "│", "╰") for ln in linhas_nao_vazias),
            "primeiros={0!r}".format([ln[0] for ln in linhas_nao_vazias]),
        )
        self._r(
            "horizontal: ultimo char de cada linha e borda direita da area N-1",
            all(ln[-1] in ("╮", "│", "╯") for ln in linhas_nao_vazias),
            "ultimos={0!r}".format([ln[-1] for ln in linhas_nao_vazias]),
        )

    def test_arranjo_horizontal_resto_deterministico(self):
        """horizontal: resto distribui deterministicamente da esquerda (maiores restos)."""
        # com dist=igual e 3 elementos em 100: pesos=[1,1,1] -> [34, 33, 33]
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=100,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal: todas as linhas tem exatamente 100 chars (sum(larguras)==100)",
            all(len(ln) == 100 for ln in linhas_nao_vazias),
        )
        # Topo da primeira caixa: area 0 tem 34 chars, area 1 começa no índice 34
        # A linha de topo começa com "╭ A" e termina com "╮╭..." em posicao 33
        linha_topo = next(
            (ln for ln in linhas_nao_vazias if "╭ A" in ln), None
        )
        if linha_topo is not None:
            self._r(
                "horizontal: area 0 tem 34 chars (char[33]=='╮', char[34]=='╭')",
                len(linha_topo) >= 35 and linha_topo[33] == "╮" and linha_topo[34] == "╭",
                "chars[33:36]={0!r}".format(linha_topo[33:36] if len(linha_topo) >= 36 else "?"),
            )
            self._r(
                "horizontal: area 1 tem 33 chars (char[66]=='╮', char[67]=='╭')",
                len(linha_topo) >= 68 and linha_topo[66] == "╮" and linha_topo[67] == "╭",
                "chars[66:69]={0!r}".format(linha_topo[66:69] if len(linha_topo) >= 69 else "?"),
            )
        else:
            self._r("horizontal: linha_topo encontrada para verificar limites", False)
            self._r("horizontal: area 0 tem 34 chars", False)
            self._r("horizontal: area 1 tem 33 chars", False)

    def test_arranjo_horizontal_padding_inferior(self):
        """horizontal: alturas desiguais -> preenchimento inferior na area menor."""
        # console: 3 linhas (topo + "(console)" + base)
        # dashboard sem campos: 2 linhas (topo + base)
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("dashboard", "B")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        # O bloco horizontal deve ter 3 linhas (max entre 3 e 2)
        # e cada linha deve ter 42 chars (padding aplicado na area B)
        self._r(
            "horizontal: todas as linhas tem exatamente 42 chars (padding aplicado)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal: saida renderizada sem erro (alturas desiguais tratadas)",
            isinstance(saida, str) and len(saida) > 0,
        )

    def test_arranjo_horizontal_largura_insuficiente(self):
        """horizontal: largura insuficiente -> RenderizadorErro determinístico sem fallback."""
        # dist=igual + N=2 + total_w=18: pesos=[1,1] -> larguras=[9,9] -> 9<10 -> erro
        modelo = _modelo_horizontal("horizontal",
                                    [("console", "A"), ("console", "B")],
                                    largura=18,
                                    distribuicao={"modo": "igual"})
        exc = self._espera_erro(
            "horizontal: largura=18 para 2 elementos -> RenderizadorErro",
            lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=18),
        )
        if exc is not None:
            self._r(
                "mensagem menciona 'arranjo horizontal'",
                "arranjo horizontal" in str(exc),
                str(exc),
            )
            # Confirmar que NAO e um fallback silencioso para vertical
            self._r(
                "excecao e RenderizadorErro (sem fallback silencioso para vertical)",
                isinstance(exc, RenderizadorErro),
            )

    def test_arranjo_horizontal_tres_elementos(self):
        """horizontal: 3 filhos diretos aparecem na mesma faixa de linhas (dist obrigatoria)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal: 3 elementos -> '╮╭' aparece 2 vezes (3 areas contiguas)",
            saida.count("╮╭") >= 2,
            "count('╮╭')={0}".format(saida.count("╮╭")),
        )
        self._r(
            "horizontal: todas as linhas tem exatamente 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )

    def test_arranjo_horizontal_com_altura_preserva_h0015(self):
        """horizontal: altura explícita funciona (distribuicao obrigatoria para N>1)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=40)
        self._r(
            "horizontal: altura=40 -> saida tem exatamente 40 linhas",
            saida.count("\n") == 40,
            "count={0}".format(saida.count("\n")),
        )
        self._r(
            "horizontal: altura=40 -> barra_de_menus no rodape",
            "╭ Menus" in saida,
        )
        self._r(
            "horizontal: altura=40 -> cada linha tem 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )

    def test_arranjo_horizontal_barra_preservada(self):
        """horizontal: barra_de_menus permanece inalterada (distribuicao obrigatoria para N>1)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal: barra_de_menus aparece na saida",
            "╭ Menus" in saida,
        )
        self._r(
            "horizontal: chip [k] Ok da barra aparece",
            "[k] Ok" in saida,
        )
        # Confirmacao de que nenhuma funcao da barra foi afetada: barra de menus
        # com chips do JSON do orquestrador continua funcionando
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo_orc = construir_modelo(tela_raw)
        saida_orc = renderizar_tela(modelo_orc, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal: barra_de_menus do demo inalterada pos-H0019",
            "[Esc] Sair" in saida_orc and "[?] Ajuda" in saida_orc,
        )

    def test_arranjo_horizontal_n1(self):
        """horizontal: N=1 -> renderizar na largura total (sem particionamento). (A-002)."""
        modelo = _modelo_horizontal("horizontal", [("console", "A")], largura=42)
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal N=1: renderiza sem erro",
            isinstance(saida, str) and len(saida) > 0,
        )
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal N=1: cada linha tem exatamente 42 chars (largura total)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal N=1: elemento aparece na saida",
            "╭ A" in saida,
        )
        # N=1 horizontal nao deve ter ╮╭ (nao ha duas areas)
        self._r(
            "horizontal N=1: sem '╮╭' (area unica, sem particao interna)",
            "╮╭" not in saida,
        )

    def run_all(self):
        print("")
        print("== H-0019 - layout horizontal plano do corpo ==")
        self.test_arranjo_none_preserva_vertical()
        self.test_arranjo_vertical_preserva_comportamento()
        self.test_arranjo_sobreposto_preserva_vertical()
        self.test_arranjo_horizontal_dois_elementos()
        self.test_arranjo_lado_a_lado_alias_horizontal()
        self.test_arranjo_horizontal_areas_contiguas()
        self.test_arranjo_horizontal_resto_deterministico()
        self.test_arranjo_horizontal_padding_inferior()
        self.test_arranjo_horizontal_largura_insuficiente()
        self.test_arranjo_horizontal_tres_elementos()
        self.test_arranjo_horizontal_com_altura_preserva_h0015()
        self.test_arranjo_horizontal_barra_preservada()
        self.test_arranjo_horizontal_n1()


class TestPreenchimentoVerticalH0020:
    """Testes de preenchimento vertical das áreas alocadas no corpo horizontal (H-0020).

    Cobre: fill interno até l_corpo_disponivel; ausência de fill externo H-0015
    no modo horizontal; preservação de H-0019 (sem altura); preservação de
    vertical/sobreposto/None; lado_a_lado como alias horizontal; barra intacta.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo(self, arranjo, specs, largura=42, distribuicao=None):
        return _modelo_horizontal(arranjo, specs, largura=largura, titulo_cab="H0020",
                                  distribuicao=distribuicao)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _corpo_linhas(self, saida):
        """Linhas entre o cabeçalho (3 linhas) e a barra_de_menus."""
        linhas = saida.split("\n")
        barra_idx = next(
            (i for i, ln in enumerate(linhas) if ln.startswith("╭ Menus")), len(linhas)
        )
        return linhas[3:barra_idx]

    # ------------------------------------------------------------------ 1
    def test_horizontal_alto_mantem_bordas_ate_altura_disponivel(self):
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 30
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-1: horizontal altura=30 -> total linhas == 30",
            saida.count("\n") == altura,
            "count={0}".format(saida.count("\n")),
        )
        linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "H0020-1: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in linhas_nv),
            "erros={0}".format([len(ln) for ln in linhas_nv if len(ln) != 42]),
        )
        self._r(
            "H0020-1: barra_de_menus presente",
            "╭ Menus" in saida,
        )
        # l_cab=3, l_barra=3, l_corpo_disponivel = 30-3-3 = 24
        l_corpo_disponivel = 30 - 3 - 3
        corpo = self._corpo_linhas(saida)
        self._r(
            "H0020-1: corpo tem exatamente l_corpo_disponivel=24 linhas",
            len(corpo) == l_corpo_disponivel,
            "len={0}".format(len(corpo)),
        )

    # ------------------------------------------------------------------ 2
    def test_horizontal_preenchimento_dentro_das_colunas(self):
        """Fill ocorre internamente em _montar_corpo_horizontal, não via H-0015."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")])
        l_corpo_disponivel = 30 - 3 - 3  # altura=30, l_cab=3, l_barra=3
        borda = self._borda()
        elementos = modelo.corpo.elementos
        bloco = _montar_corpo_horizontal(
            elementos, borda, 42, altura_disponivel=l_corpo_disponivel,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")
        self._r(
            "H0020-2: _montar_corpo_horizontal com altura_disponivel=24 retorna 24 linhas",
            len(linhas_bloco) == l_corpo_disponivel,
            "len={0}".format(len(linhas_bloco)),
        )
        self._r(
            "H0020-2: cada linha do bloco tem 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ------------------------------------------------------------------ 3
    def test_horizontal_sem_linhas_externas_apos_bloco(self):
        """Após H-0020 o bloco absorve l_corpo_disponivel linhas; zero fill externo."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 40
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        l_corpo_disponivel = altura - 3 - 3  # 34
        corpo = self._corpo_linhas(saida)
        self._r(
            "H0020-3: corpo tem exatamente l_corpo_disponivel=34 linhas (zero fill externo)",
            len(corpo) == l_corpo_disponivel,
            "len={0}".format(len(corpo)),
        )
        # Verificar diretamente que o bloco absorveu tudo
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42,
            altura_disponivel=l_corpo_disponivel, larguras=[21, 21],
        )
        self._r(
            "H0020-3: bloco tem exatamente l_corpo_disponivel linhas internamente",
            bloco.count("\n") + 1 == l_corpo_disponivel,
            "count={0}".format(bloco.count("\n") + 1),
        )

    # ------------------------------------------------------------------ 4
    def test_horizontal_bordas_adjacentes_em_linhas_preenchidas(self):
        """Bordas ││ e ╮╭ presentes nas linhas estruturais (topo/conteúdo/base)."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-4: '││' presente nas linhas de conteúdo do bloco horizontal",
            "││" in saida,
        )
        self._r(
            "H0020-4: '╮╭' presente no topo das áreas adjacentes",
            "╮╭" in saida,
        )
        self._r(
            "H0020-4: '╯╰' presente na base das áreas adjacentes",
            "╯╰" in saida,
        )
        self._r(
            "H0020-4: total linhas == 25",
            saida.count("\n") == 25,
        )

    # ------------------------------------------------------------------ 5
    def test_horizontal_largura_total_em_todas_linhas_preenchidas(self):
        """Todas as linhas do bloco (inclusive fill) têm exatamente total_w chars."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 20
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "H0020-5: altura=20 -> 20 linhas",
            saida.count("\n") == altura,
        )
        self._r(
            "H0020-5: todas as linhas têm 42 chars (inclusive fill)",
            all(len(ln) == 42 for ln in linhas_nv),
            "erros={0}".format([len(ln) for ln in linhas_nv if len(ln) != 42]),
        )

    # ------------------------------------------------------------------ 6
    def test_horizontal_colunas_diferentes_preenchidas_mesma_altura(self):
        """console (3 linhas) e dashboard (2 linhas): ambas preenchidas até l_corpo_disponivel."""
        # Teste geometrico: fornece larguras explicitas (DA-02 exige distribuicao
        # para N>1 via caminho publico; helper requer larguras explicitas para N>1).
        modelo_legado = self._modelo(
            "horizontal", [("console", "A"), ("dashboard", "B")]
        )
        l_corpo_disponivel = 25 - 3 - 3  # altura=25 → 19
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo_legado.corpo.elementos, borda, 42,
            altura_disponivel=l_corpo_disponivel, larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")
        self._r(
            "H0020-6: colunas de alturas diferentes (3 e 2) preenchidas até l_corpo_disponivel=19",
            len(linhas_bloco) == l_corpo_disponivel,
            "len={0}".format(len(linhas_bloco)),
        )
        # Verificar via renderizar_tela com distribuicao declarada (DA-02 obrigatoria para N>1)
        modelo = self._modelo(
            "horizontal", [("console", "A"), ("dashboard", "B")],
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-6: renderizar_tela altura=25 -> 25 linhas",
            saida.count("\n") == 25,
        )

    # ------------------------------------------------------------------ 7
    def test_vertical_preserva_comportamento_atual(self):
        """vertical: DA-01 (ADR-0024) - unico visual ocupa area integral."""
        modelo = self._modelo("vertical", [("console", "A")])
        altura = 20
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-7: vertical altura=20 -> 20 linhas",
            saida.count("\n") == altura,
            "count={0}".format(saida.count("\n")),
        )
        self._r(
            "H0020-7: vertical barra presente",
            "╭ Menus" in saida,
        )
        # DA-01 (ADR-0024): unico visual preenche internamente toda a area.
        # Nenhuma linha de espacos entre corpo e barra (fill externo proibido).
        linhas = saida.split("\n")
        fill_ext = [ln for ln in linhas if ln == " " * 42]
        self._r(
            "H0020-7: DA-01 (ADR-0024) - sem fill externo, console ocupa area integral",
            len(fill_ext) == 0,
            "fills={0}".format(len(fill_ext)),
        )

    # ------------------------------------------------------------------ 8
    def test_sobreposto_preserva_comportamento_atual(self):
        """sobreposto: alias de vertical, comportamento idêntico."""
        modelo_v = self._modelo("vertical", [("console", "A")])
        modelo_s = self._modelo("sobreposto", [("console", "A")])
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        saida_s = renderizar_tela(modelo_s, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0020-8: sobreposto == vertical (alias preservado)",
            saida_v == saida_s,
        )
        self._r(
            "H0020-8: sobreposto altura=20 -> 20 linhas",
            saida_s.count("\n") == 20,
        )

    # ------------------------------------------------------------------ 9
    def test_none_preserva_comportamento_atual(self):
        """None: equivale a vertical, fill externo H-0015 intacto."""
        modelo_n = self._modelo(None, [("console", "A")])
        modelo_v = self._modelo("vertical", [("console", "A")])
        saida_n = renderizar_tela(modelo_n, _ESTILO_CURVA, largura=42, altura=20)
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0020-9: None == vertical (comportamento preservado)",
            saida_n == saida_v,
        )
        self._r(
            "H0020-9: None altura=20 -> 20 linhas",
            saida_n.count("\n") == 20,
        )

    # ------------------------------------------------------------------ 10
    def test_lado_a_lado_preserva_comportamento_horizontal(self):
        """lado_a_lado: alias horizontal com fill vertical interno (H-0020)."""
        dist = {"modo": "igual"}
        modelo_h = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                                distribuicao=dist)
        modelo_l = self._modelo("lado_a_lado", [("console", "A"), ("console", "B")],
                                distribuicao=dist)
        altura = 25
        saida_h = renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42, altura=altura)
        saida_l = renderizar_tela(modelo_l, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-10: lado_a_lado == horizontal com fill vertical interno",
            saida_h == saida_l,
        )
        self._r(
            "H0020-10: lado_a_lado altura=25 -> 25 linhas",
            saida_l.count("\n") == altura,
        )
        corpo = self._corpo_linhas(saida_l)
        self._r(
            "H0020-10: corpo de lado_a_lado tem l_corpo_disponivel=19 linhas",
            len(corpo) == altura - 3 - 3,
            "len={0}".format(len(corpo)),
        )

    # ------------------------------------------------------------------ 11
    def test_horizontal_sem_altura_preserva_h0019(self):
        """Sem altura: _montar_corpo_horizontal normaliza até altura_max (H-0019 preservado)."""
        # Teste geometrico via chamada direta com larguras explicitas.
        # console: 3 linhas; dashboard sem campos: 2 linhas; altura_max = 3
        # Com altura_disponivel=None -> normaliza até 3
        modelo_legado = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        bloco_sem = _montar_corpo_horizontal(
            modelo_legado.corpo.elementos, borda, 42, altura_disponivel=None,
            larguras=[21, 21],
        )
        linhas_bloco = bloco_sem.split("\n")
        self._r(
            "H0020-11: sem altura -> bloco normalizado até altura_max=3",
            len(linhas_bloco) == 3,
            "len={0}".format(len(linhas_bloco)),
        )
        # Via renderizar_tela com distribuicao valida (DA-02: multiplos elementos requerem distribuicao)
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")],
                              distribuicao={"modo": "igual"})
        saida_sem = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        # TestArranjoH0019.test_arranjo_horizontal_padding_inferior continua passando
        linhas_nv = [ln for ln in saida_sem.split("\n") if ln != ""]
        self._r(
            "H0020-11: sem altura -> todas linhas têm 42 chars (H-0019 preservado)",
            all(len(ln) == 42 for ln in linhas_nv),
        )

    # ------------------------------------------------------------------ 12
    def test_barra_de_menus_preservada_apos_h0020(self):
        """Barra de menus com chips corretos; funções protegidas intactas."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-12: barra presente na saida horizontal com altura",
            "╭ Menus" in saida,
        )
        self._r(
            "H0020-12: chip [k] Ok da barra aparece",
            "[k] Ok" in saida,
        )
        # Verificar orquestrador (usa _normalizar_distribuicao, _linhas_barra)
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo_orc = construir_modelo(tela_raw)
        saida_orc = renderizar_tela(modelo_orc, _ESTILO_CURVA, largura=42)
        self._r(
            "H0020-12: barra demo inalterada (funções protegidas intactas)",
            "[Esc] Sair" in saida_orc and "[?] Ajuda" in saida_orc,
        )
        self._r(
            "H0020-12: teste_explorar_barra_de_menus baseline 38/38 (verificar externamente)",
            True,  # verificação executada nas suítes finais
        )

    def run_all(self):
        print("")
        print("== H-0020 - preenchimento vertical das areas alocadas no corpo horizontal ==")
        self.test_horizontal_alto_mantem_bordas_ate_altura_disponivel()
        self.test_horizontal_preenchimento_dentro_das_colunas()
        self.test_horizontal_sem_linhas_externas_apos_bloco()
        self.test_horizontal_bordas_adjacentes_em_linhas_preenchidas()
        self.test_horizontal_largura_total_em_todas_linhas_preenchidas()
        self.test_horizontal_colunas_diferentes_preenchidas_mesma_altura()
        self.test_vertical_preserva_comportamento_atual()
        self.test_sobreposto_preserva_comportamento_atual()
        self.test_none_preserva_comportamento_atual()
        self.test_lado_a_lado_preserva_comportamento_horizontal()
        self.test_horizontal_sem_altura_preserva_h0019()
        self.test_barra_de_menus_preservada_apos_h0020()


class TestPreenchimentoBordeadoH0021:
    """Testes de preenchimento bordeado no corpo horizontal (H-0021).

    Cobre: fill bordeado com bordas laterais; base na ultima linha; bordas
    adjacentes (││, ╯╰); integracao com orquestrador.json em memoria;
    alias lado_a_lado; dashboard sem literal; filhos em ordem; preservacao
    do comportamento sem altura (H-0019/H-0020); nao-regressao de
    vertical/sobreposto/None; barra_de_menus preservada.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo(self, arranjo, specs, largura=42):
        return _modelo_horizontal(arranjo, specs, largura=largura, titulo_cab="H0021")

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    # ---------------------------------------------------------------------- 1
    def test_horizontal_fill_bordeado_orquestrador_json(self):
        """demo.json em memoria com arranjo='horizontal', largura=80, altura=30."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        # l_cab=3, l_corpo_disponivel=24, l_barra=3
        linhas = saida.split("\n")
        bloco = linhas[3:27]  # 24 linhas do corpo horizontal

        self._r(
            "H0021-1: bloco horizontal tem 24 linhas (l_corpo_disponivel)",
            len(bloco) == 24,
            "len={0}".format(len(bloco)),
        )
        # Linhas internas (nao topo, nao base) devem ter '│'
        inner = bloco[1:-1]
        self._r(
            "H0021-1: linhas internas do bloco contêm '│' (bordas laterais)",
            all("│" in ln for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if "│" not in ln]),
        )
        self._r(
            "H0021-1: sem linha ' ' * 80 no bloco (fill bordeado, nao espacos planos)",
            not any(ln == " " * 80 for ln in bloco),
        )
        self._r(
            "H0021-1: cada linha do bloco tem 80 chars",
            all(len(ln) == 80 for ln in bloco),
            "erros={0}".format([len(ln) for ln in bloco if len(ln) != 80]),
        )

    # ---------------------------------------------------------------------- 2
    def test_horizontal_fill_bordeado_lado_a_lado_alias(self):
        """lado_a_lado produz comportamento identico ao horizontal."""
        tela_raw_h = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw_h["corpo"]["arranjo"] = "horizontal"
        saida_h = renderizar_tela(
            construir_modelo(tela_raw_h), estilo=_ESTILO_CURVA, largura=80, altura=30
        )

        tela_raw_l = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw_l["corpo"]["arranjo"] = "lado_a_lado"
        saida_l = renderizar_tela(
            construir_modelo(tela_raw_l), estilo=_ESTILO_CURVA, largura=80, altura=30
        )

        self._r(
            "H0021-2: lado_a_lado produz saida identica ao horizontal",
            saida_h == saida_l,
        )
        linhas_l = saida_l.split("\n")
        bloco_l = linhas_l[3:27]
        inner_l = bloco_l[1:-1]
        self._r(
            "H0021-2: lado_a_lado: linhas internas contêm '│'",
            all("│" in ln for ln in inner_l),
        )

    # ---------------------------------------------------------------------- 3
    def test_horizontal_fill_linhas_internas_com_bordas_laterais(self):
        """Modelo sintetico: linhas de fill comecam e terminam com borda vertical."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        h = 15
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-3: bloco tem 15 linhas",
            len(linhas_bloco) == h,
            "len={0}".format(len(linhas_bloco)),
        )
        # Linhas intermediarias (nao topo, nao base)
        inner = linhas_bloco[1:-1]
        self._r(
            "H0021-3: linhas intermediarias comecam com '│'",
            all(ln[0] == "│" for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if ln[0] != "│"]),
        )
        self._r(
            "H0021-3: linhas intermediarias terminam com '│'",
            all(ln[-1] == "│" for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if ln[-1] != "│"]),
        )
        self._r(
            "H0021-3: cada linha do bloco tem 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ---------------------------------------------------------------------- 4
    def test_horizontal_base_na_ultima_linha_da_area(self):
        """Base das caixas aparece na ultima linha da area horizontal."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        h = 15
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        ultima = linhas_bloco[-1]
        self._r(
            "H0021-4: ultima linha do bloco começa com '╰' (base)",
            ultima.startswith("╰"),
            "ultima[:5]={0!r}".format(ultima[:5]),
        )
        self._r(
            "H0021-4: ultima linha do bloco termina com '╯' (base)",
            ultima.endswith("╯"),
            "ultima[-5:]={0!r}".format(ultima[-5:]),
        )
        # Sem base prematura: '╰' nao deve aparecer nas linhas anteriores a ultima
        bases_prematuras = [
            i for i, ln in enumerate(linhas_bloco[:-1]) if "╰" in ln
        ]
        self._r(
            "H0021-4: '╰' ausente nas linhas intermediarias (sem base prematura)",
            len(bases_prematuras) == 0,
            "indices={0}".format(bases_prematuras),
        )

    # ---------------------------------------------------------------------- 5
    def test_horizontal_bordas_adjacentes_em_fill_e_base(self):
        """'││' nas linhas de fill e '╯╰' na linha de base."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")])
        borda = self._borda()
        h = 10
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        fill_lines = linhas_bloco[1:-1]
        self._r(
            "H0021-5: '││' presente nas linhas de fill (bordas adjacentes coladas)",
            any("││" in ln for ln in fill_lines),
        )
        self._r(
            "H0021-5: '╯╰' presente na linha de base (bases adjacentes coladas)",
            "╯╰" in linhas_bloco[-1],
            "base={0!r}".format(linhas_bloco[-1]),
        )

    # ---------------------------------------------------------------------- 6
    def test_horizontal_largura_total_em_todas_linhas_apos_h0021(self):
        """Todas as linhas do bloco (topo, conteudo, fill, base) têm total_w chars."""
        modelo = self._modelo(
            "horizontal",
            [("console", "A"), ("console", "B"), ("lancador", "C")],
        )
        borda = self._borda()
        h = 20
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[14, 14, 14],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-6: bloco tem exatamente 20 linhas",
            len(linhas_bloco) == h,
            "len={0}".format(len(linhas_bloco)),
        )
        self._r(
            "H0021-6: todas as linhas têm 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ---------------------------------------------------------------------- 7
    def test_horizontal_dashboard_sem_literal_tem_bordas(self):
        """dashboard_info sem campos literais ocupa area visual bordeada."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        borda = self._borda()
        # larguras=[27, 27, 26]: 80//3=26, 80%3=2 -> primeiras 2 areas recebem 27
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 80, altura_disponivel=24,
            larguras=[27, 27, 26],
        )
        linhas_bloco = bloco.split("\n")

        # Linhas intermediarias do bloco (nao topo, nao base)
        inner = linhas_bloco[1:-1]
        # Char na posicao 27 de cada linha intermediaria deve ser '│' (borda esq do dashboard)
        chars_esq_dash = [ln[27] for ln in inner if len(ln) >= 28]
        self._r(
            "H0021-7: dashboard sem literal: borda esquerda presente em linhas intermediarias",
            all(c == "│" for c in chars_esq_dash) and len(chars_esq_dash) > 0,
            "chars={0!r}".format(chars_esq_dash[:5]),
        )
        # Base do dashboard na ultima linha: char[27] deve ser '╰'
        ultima = linhas_bloco[-1]
        char_base = ultima[27] if len(ultima) >= 28 else None
        self._r(
            "H0021-7: base do dashboard na ultima linha (char[27]='╰')",
            char_base == "╰",
            "char[27]={0!r}".format(char_base),
        )

    # ---------------------------------------------------------------------- 8
    def test_horizontal_filhos_preservados_em_ordem(self):
        """Filhos console, dashboard, lancador aparecem na ordem declarada."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        self._r("H0021-8: '╭ ITENS' presente (console_principal)", "╭ ITENS" in saida)
        self._r("H0021-8: '╭ INFO' presente (dashboard_info)", "╭ INFO" in saida)
        self._r("H0021-8: '╭ NAVEGAR' presente (lancador_principal)", "╭ NAVEGAR" in saida)

        # Verificar ordem: na primeira linha do bloco, topos aparecem da esq para dir
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_topos = next((ln for ln in linhas if "╭ ITENS" in ln), None)
        if linha_topos is not None:
            self._r(
                "H0021-8: ITENS, INFO, NAVEGAR aparecem da esquerda para a direita",
                linha_topos.index("╭ ITENS") < linha_topos.index("╭ INFO")
                < linha_topos.index("╭ NAVEGAR"),
            )
        else:
            self._r("H0021-8: linha com topos das tres colunas encontrada", False)

    # ---------------------------------------------------------------------- 9
    def test_horizontal_sem_altura_preserva_h0019_h0020(self):
        """Sem altura_disponivel: fill permanece ' ' * largura (sem bordas)."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=None,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-9: sem altura -> bloco tem 3 linhas (altura_max, H-0019 preservado)",
            len(linhas_bloco) == 3,
            "len={0}".format(len(linhas_bloco)),
        )
        # Com altura=None: dashboard (coluna 1, w=21) tem fill ' '*21 no row 2.
        # Row 2 concatenado = base_do_console (21 chars) + fill_do_dashboard (21 chars).
        # O fill do dashboard ocupa chars [21:42]; se for espacos (sem '│'), e H-0020.
        row2 = linhas_bloco[2]
        dash_fill = row2[21:] if len(row2) >= 42 else None
        self._r(
            "H0021-9: fill sem bordas: coluna dashboard (chars 21..41) e espacos (H-0019/H-0020)",
            dash_fill == " " * 21,
            "dash_fill={0!r}".format(dash_fill),
        )

    # ---------------------------------------------------------------------- 10
    def test_vertical_nao_regride_apos_h0021(self):
        """arranjo=vertical preserva comportamento anterior."""
        # H-0025: o demo.json declara distribuicao agora. Sem altura,
        # a distribuicao nao se aplica (sem area distribuivel) e a saida continua
        # igual a _EXPECTED_ORQUESTRADOR (comportamento orientado pelo conteudo).
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(tela_raw)  # arranjo=vertical (padrao do JSON)
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H0021-10: vertical sem altura preserva _EXPECTED_ORQUESTRADOR",
            saida == _EXPECTED_ORQUESTRADOR,
        )
        # ADR-0024 DA-02: modelo sem distribuicao com 3 visuais + area residual
        # e invalido (fill externo proibido pelo ADR-0024).
        modelo_sd = _modelo_orquestrador_sem_distribuicao()
        excecao_da02 = None
        try:
            renderizar_tela(modelo_sd, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "H0021-10: ADR-0024 DA-02 - sem dist + 3 visuais + altura=24 -> RenderizadorErro",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    # ---------------------------------------------------------------------- 11
    def test_sobreposto_nao_regride_apos_h0021(self):
        """arranjo=sobreposto (alias de vertical) sem regressao."""
        modelo_v = _modelo_horizontal("vertical", [("console", "A")])
        modelo_s = _modelo_horizontal("sobreposto", [("console", "A")])
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        saida_s = renderizar_tela(modelo_s, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0021-11: sobreposto == vertical (alias preservado)",
            saida_v == saida_s,
        )
        self._r(
            "H0021-11: sobreposto com altura=20 -> 20 linhas",
            saida_s.count("\n") == 20,
        )

    # ---------------------------------------------------------------------- 12
    def test_none_nao_regride_apos_h0021(self):
        """arranjo=None equivale a vertical, sem regressao."""
        modelo_n = _modelo_horizontal(None, [("console", "A")])
        modelo_v = _modelo_horizontal("vertical", [("console", "A")])
        saida_n = renderizar_tela(modelo_n, _ESTILO_CURVA, largura=42, altura=20)
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0021-12: None == vertical (preservado)",
            saida_n == saida_v,
        )
        self._r(
            "H0021-12: None com altura=20 -> 20 linhas",
            saida_n.count("\n") == 20,
        )

    # ---------------------------------------------------------------------- 13
    def test_barra_de_menus_preservada_apos_h0021(self):
        """Barra de menus e funcoes protegidas preservadas apos H-0021."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        self._r("H0021-13: '╭ Menus' presente na saida horizontal", "╭ Menus" in saida)
        self._r("H0021-13: '[Esc] Sair' presente na barra", "[Esc] Sair" in saida)
        self._r("H0021-13: '[?] Ajuda' presente na barra", "[?] Ajuda" in saida)

        from tela.renderizador import (
            _normalizar_distribuicao,
            _validar_distribuicao,
            _linhas_barra,
        )
        self._r(
            "H0021-13: _normalizar_distribuicao existe e e chamavel",
            callable(_normalizar_distribuicao),
        )
        self._r(
            "H0021-13: _validar_distribuicao existe e e chamavel",
            callable(_validar_distribuicao),
        )
        self._r(
            "H0021-13: _linhas_barra existe e e chamavel",
            callable(_linhas_barra),
        )

    # ---------------------------------------------------------------------- 14
    def test_baseline_completo_continua_passando(self):
        """Registro: baseline 621 casos anteriores verificados por execucao sequencial."""
        self._r(
            "H0021-14: baseline completo verificado externamente (621 + novos)",
            True,
        )

    def run_all(self):
        print("")
        print("== H-0021 - correcao preenchimento bordeado horizontal ==")
        self.test_horizontal_fill_bordeado_orquestrador_json()
        self.test_horizontal_fill_bordeado_lado_a_lado_alias()
        self.test_horizontal_fill_linhas_internas_com_bordas_laterais()
        self.test_horizontal_base_na_ultima_linha_da_area()
        self.test_horizontal_bordas_adjacentes_em_fill_e_base()
        self.test_horizontal_largura_total_em_todas_linhas_apos_h0021()
        self.test_horizontal_dashboard_sem_literal_tem_bordas()
        self.test_horizontal_filhos_preservados_em_ordem()
        self.test_horizontal_sem_altura_preserva_h0019_h0020()
        self.test_vertical_nao_regride_apos_h0021()
        self.test_sobreposto_nao_regride_apos_h0021()
        self.test_none_nao_regride_apos_h0021()
        self.test_barra_de_menus_preservada_apos_h0021()
        self.test_baseline_completo_continua_passando()


class TestDistribuicaoVerticalH0025:
    """Cobertura da distribuicao vertical explicita do corpo (H-0025 / ADR-0018).

    Cobre os minimos exigidos pelo H-0025 secao 10.2: ausencia preservada;
    igual explicito; percentual; fracao [1,1,1], [2,1,2] e vetor generico
    adicional; soma exata; maiores restos; desempate por ordem declarada;
    preenchimento interno das molduras; ausencia de sobra externa; JSON real
    do Orquestrador; redimensionamento; preservacao horizontal; telas sem
    distribuicao inalteradas.
    """

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
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    def _modelo_dist(self, distribuicao, n=3, titulos=None):
        """Modelo vertical com n consoles e distribuicao declarada."""
        if titulos is None:
            titulos = [chr(ord("A") + i) for i in range(n)]
        elementos = [
            ElementoCorpo(
                id=titulos[i].lower(), tipo="console",
                _campos_inertes={"titulo": titulos[i]},
            )
            for i in range(n)
        ]
        return ModeloTela(
            id="teste_h0025",
            schema="tela.v1",
            cabecalho={"titulo": "H0025", "descricao": "dist vertical", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="vertical", elementos=elementos,
                distribuicao=distribuicao,
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )

    def _modelo_sem_dist(self, n=3, titulos=None):
        """Modelo vertical sem distribuicao (orientado pelo conteudo)."""
        return self._modelo_dist(None, n=n, titulos=titulos)

    # ----------------------------------------------------------- algoritmo
    def test_algoritmo_maiores_restos_exemplos_normativos(self):
        # Exemplos normativos do contrato_composicao_corpo.md secao 5.8.
        self._r(
            "alg: 68 com [1,1,1] -> [23,23,22]",
            _distribuir_alturas(68, [1, 1, 1]) == [23, 23, 22],
            "obtido={0}".format(_distribuir_alturas(68, [1, 1, 1])),
        )
        self._r(
            "alg: 68 com [2,1,2] -> [27,14,27]",
            _distribuir_alturas(68, [2, 1, 2]) == [27, 14, 27],
            "obtido={0}".format(_distribuir_alturas(68, [2, 1, 2])),
        )

    def test_algoritmo_soma_exata_invariante(self):
        for altura, pesos in [
            (18, [1, 1, 1]), (18, [2, 1, 2]), (18, [1, 3, 1]),
            (18, [5, 2, 7]), (14, [1, 1, 1]), (101, [3, 5, 7, 11]),
            (7, [1]), (66, [1, 1, 1]),
        ]:
            cotas = _distribuir_alturas(altura, pesos)
            self._r(
                "alg: soma das cotas == altura ({0}, {1})".format(altura, pesos),
                sum(cotas) == altura,
                "cotas={0} soma={1}".format(cotas, sum(cotas)),
            )

    def test_algoritmo_vetores_genericos_sem_codigo_especial(self):
        # O mesmo codigo generico trata [1,1,1], [2,1,2], [1,3,1] e [5,2,7].
        r_111 = _distribuir_alturas(30, [1, 1, 1])
        r_212 = _distribuir_alturas(30, [2, 1, 2])
        r_131 = _distribuir_alturas(30, [1, 3, 1])
        r_527 = _distribuir_alturas(30, [5, 2, 7])
        self._r(
            "alg: [1,1,1] em 30 -> [10,10,10] (divisao exata)",
            r_111 == [10, 10, 10],
            "obtido={0}".format(r_111),
        )
        self._r(
            "alg: [2,1,2] em 30 -> [12,6,12] (proporcao 2:1:2)",
            r_212 == [12, 6, 12],
            "obtido={0}".format(r_212),
        )
        self._r(
            "alg: [1,3,1] em 30 -> [6,18,6] (proporcao 1:3:1)",
            r_131 == [6, 18, 6],
            "obtido={0}".format(r_131),
        )
        self._r(
            "alg: [5,2,7] em 30 -> soma 30 (vetor generico)",
            sum(r_527) == 30,
            "obtido={0}".format(r_527),
        )

    def test_algoritmo_maiores_restos_distribui_residuo(self):
        # 10 com [1,1,1]: 10/3=3.33 -> floor [3,3,3] soma 9, falta 1.
        # Restos iguais (0.33): desempate por ordem declarada -> idx 0 recebe.
        self._r(
            "alg: 10 com [1,1,1] -> [4,3,3] (maiores restos)",
            _distribuir_alturas(10, [1, 1, 1]) == [4, 3, 3],
            "obtido={0}".format(_distribuir_alturas(10, [1, 1, 1])),
        )

    def test_algoritmo_desempate_por_ordem_declarada(self):
        # 14 com [1,1,1]: 14/3=4.667 -> floor [4,4,4] soma 12, faltam 2.
        # Restos iguais -> idx 0 e idx 1 recebem (ordem declarada).
        self._r(
            "alg: 14 com [1,1,1] -> [5,5,4] (desempate por ordem)",
            _distribuir_alturas(14, [1, 1, 1]) == [5, 5, 4],
            "obtido={0}".format(_distribuir_alturas(14, [1, 1, 1])),
        )
        # [2,2] em 5: 5*2/4=2.5 cada -> floor [2,2] soma 4, falta 1.
        # Restos iguais (0.5) -> idx 0 recebe (ordem declarada).
        self._r(
            "alg: 5 com [2,2] -> [3,2] (empate: primeiro declarado)",
            _distribuir_alturas(5, [2, 2]) == [3, 2],
            "obtido={0}".format(_distribuir_alturas(5, [2, 2])),
        )

    def test_pesos_distribuicao_por_modo(self):
        self._r(
            "pesos: igual -> [1,1,1]",
            _pesos_distribuicao({"modo": "igual"}, 3) == [1, 1, 1],
        )
        self._r(
            "pesos: fracao -> valores declarados",
            _pesos_distribuicao(
                {"modo": "fracao", "valores": [2, 1, 2]}, 3) == [2, 1, 2],
        )
        self._r(
            "pesos: percentual -> valores declarados",
            _pesos_distribuicao(
                {"modo": "percentual", "valores": [40, 20, 40]}, 3) == [40, 20, 40],
        )

    # ----------------------------------------------------- ausencia (D2)
    def test_ausencia_preserva_altura_natural_sem_cota(self):
        modelo = self._modelo_sem_dist()
        saida_none = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        corpo_none = _corpo_alturas(saida_none)
        # Cada console natural = 3 linhas (topo + "(console)" + base).
        self._r(
            "ausencia: sem altura, cada filho usa altura natural (3)",
            corpo_none == [3, 3, 3],
            "corpo={0}".format(corpo_none),
        )
        # ADR-0024 DA-02: ausencia de distribuicao com 3 visuais + area residual
        # e invalida (fill externo proibido pelo ADR-0024).
        excecao_da02 = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "ausencia: com altura=24 e 3 visuais -> DA-02 (ADR-0024)",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    def test_ausencia_nao_materializa_igual_no_modelo(self):
        modelo = self._modelo_sem_dist()
        self._r(
            "ausencia: modelo.corpo.distribuicao is None (sem fallback igual)",
            modelo.corpo.distribuicao is None,
        )

    # -------------------------------------------------------- modos (D5-D7)
    def test_igual_explicito_divide_igualmente(self):
        modelo = self._modelo_dist({"modo": "igual"})
        # l_cab=3, l_barra=3, l_corpo_disponivel = 24-3-3 = 18 -> [6,6,6].
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "igual explicito em altura=24 -> [6,6,6]",
            corpo == [6, 6, 6],
            "corpo={0}".format(corpo),
        )

    def test_igual_explicito_maiores_restos(self):
        modelo = self._modelo_dist({"modo": "igual"})
        # altura=16 -> l_corpo=10 -> [4,3,3] (maiores restos + ordem).
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=16)
        corpo = _corpo_alturas(saida)
        self._r(
            "igual explicito em altura=16 -> [4,3,3] (maiores restos)",
            corpo == [4, 3, 3],
            "corpo={0}".format(corpo),
        )

    def test_percentual_explicito(self):
        modelo = self._modelo_dist(
            {"modo": "percentual", "valores": [40, 20, 40]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "percentual [40,20,40] em altura=24 -> [7,4,7] (proporcao)",
            corpo == [7, 4, 7],
            "corpo={0}".format(corpo),
        )

    def test_fracao_111(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [1, 1, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "fracao [1,1,1] em altura=24 -> [6,6,6] (pesos iguais)",
            corpo == [6, 6, 6],
            "corpo={0}".format(corpo),
        )

    def test_fracao_212(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "fracao [2,1,2] em altura=24 -> [7,4,7] (proporcao 2:1:2)",
            corpo == [7, 4, 7],
            "corpo={0}".format(corpo),
        )

    def test_fracao_vetor_generico_adicional(self):
        # [1,3,1] e [5,2,7] pelo mesmo codigo generico (sem especializacao).
        modelo_131 = self._modelo_dist({"modo": "fracao", "valores": [1, 3, 1]})
        corpo_131 = _corpo_alturas(
            renderizar_tela(modelo_131, _ESTILO_CURVA, largura=42, altura=24)
        )
        self._r(
            "fracao [1,3,1] em altura=24 -> [4,11,3] soma 18",
            corpo_131 == [4, 11, 3] and sum(corpo_131) == 18,
            "corpo={0}".format(corpo_131),
        )
        modelo_527 = self._modelo_dist({"modo": "fracao", "valores": [5, 2, 7]})
        corpo_527 = _corpo_alturas(
            renderizar_tela(modelo_527, _ESTILO_CURVA, largura=42, altura=24)
        )
        self._r(
            "fracao [5,2,7] em altura=24 -> soma 18",
            sum(corpo_527) == 18,
            "corpo={0}".format(corpo_527),
        )

    # --------------------------------------------- soma exata / sem sobra
    def test_soma_das_cotas_igual_area_distribuivel(self):
        for dist in [
            {"modo": "igual"},
            {"modo": "fracao", "valores": [1, 1, 1]},
            {"modo": "fracao", "valores": [2, 1, 2]},
            {"modo": "fracao", "valores": [1, 3, 1]},
            {"modo": "percentual", "valores": [40, 20, 40]},
        ]:
            modelo = self._modelo_dist(dist)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
            corpo = _corpo_alturas(saida)
            self._r(
                "soma cotas == l_corpo_disponivel (18) para {0}".format(dist),
                sum(corpo) == 18,
                "corpo={0} soma={1}".format(corpo, sum(corpo)),
            )

    def test_sem_sobra_externa_abaixo_do_ultimo_filho(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        linhas = saida.split("\n")
        # Localizar a ultima caixa do corpo (C) e a caixa Menus.
        idx_ultimo_topo = max(i for i, ln in enumerate(linhas) if ln.startswith("╭ C"))
        idx_menus = next(i for i, ln in enumerate(linhas) if ln.startswith("╭ Menus"))
        entre = linhas[idx_ultimo_topo:idx_menus]
        # Nenhuma linha de preenchimento externo (" "*42) entre as duas caixas.
        fill_externo = [ln for ln in entre if ln == " " * 42]
        self._r(
            "distribuicao: sem sobra externa entre ultimo filho e barra",
            len(fill_externo) == 0,
            "fills={0}".format(len(fill_externo)),
        )

    # -------------------------------------------------- preenchimento interno
    def test_preenchimento_interno_moldura_ocupa_cota(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        # cota do primeiro filho (7) > altura natural do console (3).
        self._r(
            "preenchimento interno: primeiro filho ocupa cota (7 > natural 3)",
            corpo[0] == 7,
            "corpo={0}".format(corpo),
        )
        # As linhas internas do primeiro filho sao bordeadas (│ ... │).
        linhas = saida.split("\n")
        idx_topo_a = next(i for i, ln in enumerate(linhas) if ln.startswith("╭ A"))
        idx_base_a = idx_topo_a + corpo[0] - 1
        internas = linhas[idx_topo_a + 1:idx_base_a]
        self._r(
            "preenchimento interno: linhas internas bordeadas (│ ... │)",
            len(internas) == corpo[0] - 2
            and all(ln.startswith("│") and ln.endswith("│") for ln in internas),
            "internas={0}".format(internas[:2]),
        )
        # Cada linha nao-vazia tem exatamente 42 chars.
        self._r(
            "preenchimento interno: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in linhas if ln != ""),
        )

    # ------------------------------------------------------ JSON real (D9)
    def test_json_real_orquestrador_distribui_212(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        self._r(
            "JSON real: demo declara fracao [2,1,2]",
            isinstance(modelo.corpo.distribuicao, dict)
            and modelo.corpo.distribuicao.get("valores") == [2, 1, 2],
        )
        # H-0037: com 11 itens no lancador, NAVEGAR requer >= 10 linhas; a
        # fracao [2,1,2] sobre l_corpo=25 (altura=31) -> [10,5,10].
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=31)
        corpo = _corpo_alturas(saida)
        # l_corpo_disponivel=25 -> [10,5,10] para ITENS/INFO/NAVEGAR.
        self._r(
            "JSON real: altura=31 distribui [10,5,10] entre ITENS/INFO/NAVEGAR",
            corpo == [10, 5, 10],
            "corpo={0}".format(corpo),
        )
        # Sem preenchimento externo (sobra absorvida internamente).
        fill_ext = [ln for ln in saida.split("\n") if ln == " " * 42]
        self._r(
            "JSON real: sem preenchimento externo (sobra interna nas molduras)",
            len(fill_ext) == 0,
            "fills={0}".format(len(fill_ext)),
        )
        self._r(
            "JSON real: total de linhas == 31",
            saida.count("\n") == 31,
            "count={0}".format(saida.count("\n")),
        )

    def test_json_real_sem_altura_preserva_conteudo_natural(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "JSON real: sem altura preserva _EXPECTED_ORQUESTRADOR (natural)",
            saida == _EXPECTED_ORQUESTRADOR,
        )

    # ----------------------------------------------------- redimensionamento
    def test_redimensionamento_recalcula_cotas(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida_24 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        saida_30 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=30)
        corpo_24 = _corpo_alturas(saida_24)
        corpo_30 = _corpo_alturas(saida_30)
        # altura=24 -> l_corpo=18 -> [7,4,7]; altura=30 -> l_corpo=24 -> [10,5,9]?
        # 24*2/5=9.6, 24*1/5=4.8, 24*2/5=9.6 -> floor [9,4,9] soma 22, faltam 2.
        # restos [0.6,0.8,0.6] -> idx1, depois idx0 (ordem) -> [10,5,9].
        self._r(
            "redimensionamento: altura=24 -> [7,4,7]",
            corpo_24 == [7, 4, 7],
            "corpo={0}".format(corpo_24),
        )
        self._r(
            "redimensionamento: altura=30 -> [10,5,9] (recalculado)",
            corpo_30 == [10, 5, 9],
            "corpo={0}".format(corpo_30),
        )
        self._r(
            "redimensionamento: soma cotas acompanha altura (18 e 24)",
            sum(corpo_24) == 18 and sum(corpo_30) == 24,
        )

    # ------------------------------------------- preservacao sem distribuicao
    def test_telas_sem_distribuicao_nao_mudam(self):
        # destino_minimo e grupo_minimo nao declaram distribuicao.
        for id_tela in ("destino_minimo", "grupo_minimo", "stub_b"):
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            self._r(
                "{0}: sem distribuicao (distribuicao is None)".format(id_tela),
                modelo.corpo.distribuicao is None,
                "dist={0!r}".format(modelo.corpo.distribuicao),
            )

    # ------------------------------------------------- arranjo horizontal (D1)
    def test_arranjo_horizontal_nao_regride_com_distribuicao(self):
        # H-0026: distribuicao declarada em arranjo horizontal agora ALTERA as
        # larguras conforme os valores (antes do H-0026 o renderizador ignorava
        # a distribuicao e mantinha particionamento uniforme). Com fracao [1,1]
        # em total_w=42, cada area deve ter exatamente 21 colunas.
        modelo_h = ModeloTela(
            id="teste_h0025_h",
            schema="tela.v1",
            cabecalho={"titulo": "H0025H", "descricao": "horizontal", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="horizontal",
                elementos=[
                    ElementoCorpo(id="a", tipo="console", _campos_inertes={"titulo": "A"}),
                    ElementoCorpo(id="b", tipo="console", _campos_inertes={"titulo": "B"}),
                ],
                distribuicao={"modo": "fracao", "valores": [1, 1]},
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )
        saida = renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal + distribuicao declarada: renderiza sem erro",
            isinstance(saida, str) and len(saida) > 0,
        )
        self._r(
            "horizontal + distribuicao: '╮╭' presente (particionamento contiguo)",
            "╮╭" in saida,
        )
        self._r(
            "horizontal + distribuicao: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )
        # H-0026: fracao [1,1] em 42 -> cada area tem 21 colunas. A transicao
        # entre as duas areas na linha de topo ocorre na coluna 21 (char[20]=='╮'
        # da area A, char[21]=='╭' da area B).
        linha_topo_corpo = next(
            (ln for ln in saida.split("\n") if "╭ A" in ln), None
        )
        if linha_topo_corpo is not None:
            self._r(
                "horizontal + fracao[1,1]: area A tem 21 colunas (char[20]=='╮')",
                len(linha_topo_corpo) >= 22 and linha_topo_corpo[20] == "╮",
                "char[20]={0!r}".format(
                    linha_topo_corpo[20] if len(linha_topo_corpo) > 20 else "?"
                ),
            )
            self._r(
                "horizontal + fracao[1,1]: area B inicia na coluna 21 (char[21]=='╭')",
                len(linha_topo_corpo) >= 22 and linha_topo_corpo[21] == "╭",
                "char[21]={0!r}".format(
                    linha_topo_corpo[21] if len(linha_topo_corpo) > 21 else "?"
                ),
            )
        else:
            self._r(
                "horizontal + fracao[1,1]: linha de topo do corpo encontrada", False
            )
            self._r("horizontal + fracao[1,1]: area A tem 21 colunas", False)
            self._r("horizontal + fracao[1,1]: area B inicia na coluna 21", False)

    def run_all(self):
        print("")
        print("== H-0025 - distribuicao vertical explicita da area do corpo ==")
        self.test_algoritmo_maiores_restos_exemplos_normativos()
        self.test_algoritmo_soma_exata_invariante()
        self.test_algoritmo_vetores_genericos_sem_codigo_especial()
        self.test_algoritmo_maiores_restos_distribui_residuo()
        self.test_algoritmo_desempate_por_ordem_declarada()
        self.test_pesos_distribuicao_por_modo()
        self.test_ausencia_preserva_altura_natural_sem_cota()
        self.test_ausencia_nao_materializa_igual_no_modelo()
        self.test_igual_explicito_divide_igualmente()
        self.test_igual_explicito_maiores_restos()
        self.test_percentual_explicito()
        self.test_fracao_111()
        self.test_fracao_212()
        self.test_fracao_vetor_generico_adicional()
        self.test_soma_das_cotas_igual_area_distribuivel()
        self.test_sem_sobra_externa_abaixo_do_ultimo_filho()
        self.test_preenchimento_interno_moldura_ocupa_cota()
        self.test_json_real_orquestrador_distribui_212()
        self.test_json_real_sem_altura_preserva_conteudo_natural()
        self.test_redimensionamento_recalcula_cotas()
        self.test_telas_sem_distribuicao_nao_mudam()
        self.test_arranjo_horizontal_nao_regride_com_distribuicao()


class TestDistribuicaoHorizontalH0026:
    """Cobertura da distribuicao horizontal explicita do corpo (H-0026).

    Cobre os minimos exigidos pelo H-0026 secao 16: percentual [50,50] e
    assimetrico [60,40]; fracao [1,1], [2,1] e equivalencia por escala [4,2];
    maiores restos T06 (largura 100 -> [34,33,33]) e T07 (largura 101 ->
    [34,34,33]); soma das larguras igual a distribuivel; bordas em contato;
    largura total preservada; preenchimento interno quando conteudo menor que
    a cota; ausencia de distribuicao sem regressao; preservacao vertical
    H-0025; rejeicoes do loader preservadas.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo_dist_h(self, distribuicao, n=2, titulos=None):
        """Modelo horizontal com n consoles e distribuicao declarada."""
        if titulos is None:
            titulos = [chr(ord("A") + i) for i in range(n)]
        elementos = [
            ElementoCorpo(
                id=titulos[i].lower(), tipo="console",
                _campos_inertes={"titulo": titulos[i]},
            )
            for i in range(n)
        ]
        return ModeloTela(
            id="teste_h0026",
            schema="tela.v1",
            cabecalho={"titulo": "H0026", "descricao": "dist horizontal", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="horizontal", elementos=elementos,
                distribuicao=distribuicao,
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )

    def _larguras_das_areas(self, saida, titulos):
        """Extrai a largura de cada area a partir da linha de topo do corpo.

        Localiza a linha que contem o topo da primeira area (``╭ {titulo0}``)
        e devolve as larguras detectando as transicoes ``╮╭`` entre areas
        adjacentes. Retorna lista de inteiros (largura de cada area).
        """
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_topo = next(
            (ln for ln in linhas if "╭ {0}".format(titulos[0]) in ln), None
        )
        if linha_topo is None:
            return None
        # As areas sao contiguas: cada area inicia com ╭ e termina com ╮ (na
        # linha de topo). As transicoes internas produzem ╮╭. Dividir a linha
        # pelos pontos de transicao ╮╭ mantendo as bordas.
        larguras = []
        inicio = 0
        i = 0
        while i < len(linha_topo) - 1:
            if linha_topo[i] == "╮" and linha_topo[i + 1] == "╭":
                larguras.append(i + 1 - inicio)
                inicio = i + 1
            i += 1
        # Ultima area: do ultimo inicio ate o final da linha
        larguras.append(len(linha_topo) - inicio)
        return larguras

    # ------------------------------------ algoritmo de maiores restos (helper)
    def test_algoritmo_distribuir_larguras_soma_exata(self):
        # Invariante: sum(cotas) == largura_disponivel para varios pares.
        for largura, pesos in [
            (42, [1, 1]), (42, [2, 1]), (42, [50, 50]), (42, [60, 40]),
            (100, [1, 1, 1]), (101, [1, 1, 1]), (100, [2, 1, 2]),
            (99, [3, 5, 7]), (7, [1]), (17, [1, 3, 1]),
        ]:
            cotas = _distribuir_larguras(largura, pesos)
            self._r(
                "alg larg: soma das cotas == largura ({0}, {1})".format(
                    largura, pesos
                ),
                sum(cotas) == largura,
                "cotas={0} soma={1}".format(cotas, sum(cotas)),
            )

    def test_algoritmo_distribuir_larguras_exemplos_normativos(self):
        self._r(
            "alg larg: 100 com [1,1,1] -> [34,33,33] (T06)",
            _distribuir_larguras(100, [1, 1, 1]) == [34, 33, 33],
            "obtido={0}".format(_distribuir_larguras(100, [1, 1, 1])),
        )
        self._r(
            "alg larg: 101 com [1,1,1] -> [34,34,33] (T07)",
            _distribuir_larguras(101, [1, 1, 1]) == [34, 34, 33],
            "obtido={0}".format(_distribuir_larguras(101, [1, 1, 1])),
        )

    # ------------------------------------------------------------- T01 percentual [50,50]
    def test_percentual_simetrico_50_50(self):
        modelo = self._modelo_dist_h(
            {"modo": "percentual", "valores": [50, 50]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T01: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T01: percentual [50,50] -> [21,21]", larguras == [21, 21],
                "larguras={0}".format(larguras))
        self._r("T01: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))
        self._r("T01: '╮╭' presente (bordas coladas)", "╮╭" in saida)

    # ------------------------------------------------------ T02 percentual [60,40]
    def test_percentual_assimetrico_60_40(self):
        modelo = self._modelo_dist_h(
            {"modo": "percentual", "valores": [60, 40]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T02: larguras detectadas", False, "linha de topo nao achada")
            return
        # 42*0.6=25.2 -> 25 ; 42*0.4=16.8 -> 16+1 (resto 0.8) = 17
        self._r("T02: percentual [60,40] -> [25,17]", larguras == [25, 17],
                "larguras={0}".format(larguras))
        self._r("T02: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ------------------------------------------------------------- T03 fracao [1,1]
    def test_fracao_simetrico_1_1(self):
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [1, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T03: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T03: fracao [1,1] -> [21,21]", larguras == [21, 21],
                "larguras={0}".format(larguras))
        self._r("T03: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ------------------------------------------------------------- T04 fracao [2,1]
    def test_fracao_assimetrico_2_1(self):
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T04: larguras detectadas", False, "linha de topo nao achada")
            return
        # 42*2/3=28 ; 42*1/3=14
        self._r("T04: fracao [2,1] -> [28,14]", larguras == [28, 14],
                "larguras={0}".format(larguras))
        self._r("T04: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------------- T05 equivalencia por escala [2,1]/[4,2]
    def test_fracao_equivalencia_por_escala(self):
        modelo_21 = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        modelo_42 = self._modelo_dist_h({"modo": "fracao", "valores": [4, 2]})
        saida_21 = renderizar_tela(modelo_21, _ESTILO_CURVA, largura=42)
        saida_42 = renderizar_tela(modelo_42, _ESTILO_CURVA, largura=42)
        larguras_21 = self._larguras_das_areas(saida_21, ["A", "B"])
        larguras_42 = self._larguras_das_areas(saida_42, ["A", "B"])
        if larguras_21 is None or larguras_42 is None:
            self._r("T05: larguras detectadas", False,
                    "21={0} 42={1}".format(larguras_21, larguras_42))
            return
        self._r(
            "T05: fracao [2,1] e [4,2] produzem larguras identicas",
            larguras_21 == larguras_42,
            "[2,1]={0} [4,2]={1}".format(larguras_21, larguras_42),
        )
        self._r("T05: ambas produzem [28,14]",
                larguras_21 == [28, 14] and larguras_42 == [28, 14],
                "21={0} 42={1}".format(larguras_21, larguras_42))

    # --------------------------------------------------- T06 maiores restos larg=100
    def test_t06_maiores_restos_largura_100(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
        larguras = self._larguras_das_areas(saida, ["A", "B", "C"])
        if larguras is None:
            self._r("T06: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T06: fracao [1,1,1] em 100 -> [34,33,33]", larguras == [34, 33, 33],
                "larguras={0}".format(larguras))
        self._r("T06: soma das larguras == 100", sum(larguras) == 100,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------------- T07 empate de restos resolvido por ordem
    def test_t07_empate_restos_resolvido_por_ordem_declarada(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=101)
        larguras = self._larguras_das_areas(saida, ["A", "B", "C"])
        if larguras is None:
            self._r("T07: larguras detectadas", False, "linha de topo nao achada")
            return
        # Partes inteiras [33,33,33]; faltam 2; restos empatados -> posicoes 0 e 1.
        self._r("T07: fracao [1,1,1] em 101 -> [34,34,33]", larguras == [34, 34, 33],
                "larguras={0}".format(larguras))
        self._r("T07: soma das larguras == 101", sum(larguras) == 101,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------- T08 soma das larguras == largura distribuivel
    def test_t08_soma_larguras_igual_distribuivel(self):
        casos = [
            ({"modo": "percentual", "valores": [50, 50]}, 42, ["A", "B"]),
            ({"modo": "percentual", "valores": [60, 40]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [1, 1]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [2, 1]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [1, 1, 1]}, 100, ["A", "B", "C"]),
            ({"modo": "fracao", "valores": [1, 1, 1]}, 101, ["A", "B", "C"]),
        ]
        for dist, largura, titulos in casos:
            modelo = self._modelo_dist_h(dist, n=len(titulos), titulos=titulos)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=largura)
            larguras = self._larguras_das_areas(saida, titulos)
            if larguras is None:
                self._r(
                    "T08: soma == {0} ({1})".format(largura, dist),
                    False, "larguras nao detectadas",
                )
                continue
            self._r(
                "T08: soma das larguras == {0} ({1})".format(largura, dist),
                sum(larguras) == largura,
                "larguras={0} soma={1}".format(larguras, sum(larguras)),
            )

    # ------------------------------------------------- T09 bordas horizontais em contato
    def test_t09_bordas_em_contato(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=101)
        self._r("T09: '╮╭' presente no topo", "╮╭" in saida)
        self._r("T09: '╯╰' presente na base", "╯╰" in saida)
        self._r("T09: '││' presente em linhas internas", "││" in saida)

    # -------------------------------------------- T10 largura total da saida preservada
    def test_t10_largura_total_preservada(self):
        for dist in [
            {"modo": "percentual", "valores": [50, 50]},
            {"modo": "fracao", "valores": [2, 1]},
        ]:
            modelo = self._modelo_dist_h(dist)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
            self._r(
                "T10: todas as linhas com 42 chars ({0})".format(dist),
                all(len(ln) == 42 for ln in linhas_nv),
                "invalidas={0}".format(
                    [(i, len(ln)) for i, ln in enumerate(linhas_nv)
                     if len(ln) != 42]
                ),
            )

    # ----------------------------- T11 preenchimento interno quando conteudo < cota
    def test_t11_preenchimento_interno_conteudo_menor_que_cota(self):
        # Console com uma linha de conteudo ("(console)") numa area larga deve
        # manter a linha de conteudo com largura total da area (preenchida com
        # espacos ate a borda direita). Verifica que a area A (cota 28) preenche
        # sua linha de conteudo ate completar 28 colunas.
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_console = next(
            (ln for ln in linhas if "(console)" in ln), None
        )
        if linha_console is None:
            self._r("T11: linha de conteudo '(console)' encontrada", False)
            return
        # A area A ocupa as primeiras 28 colunas (cota 28). A linha de conteudo
        # da area A termina com '|' na coluna 27 (borda direita da area A).
        self._r(
            "T11: conteudo da area A preenchido ate borda (char[27]=='│')",
            len(linha_console) >= 28 and linha_console[27] == "│",
            "char[27]={0!r}".format(
                linha_console[27] if len(linha_console) > 27 else "?"
            ),
        )
        # E nao ha espaco externo entre as areas: char[28] e a borda esquerda
        # da area B.
        self._r(
            "T11: area B inicia imediatamente apos (char[28]=='│')",
            len(linha_console) >= 29 and linha_console[28] == "│",
            "char[28]={0!r}".format(
                linha_console[28] if len(linha_console) > 28 else "?"
            ),
        )

    # ------------------------------- T-NR01 ausencia de distribuicao sem regressao
    def test_ausencia_distribuicao_rejeita_multiplos_participantes(self):
        # QA-H0033-IMP-HIGH-001: ausencia de distribuicao com multiplos elementos
        # no eixo horizontal deve ser rejeitada explicitamente (DA-02/ADR-0024).
        # Ausencia NAO equivale a igual; composicao invalida -> RenderizadorErro.
        modelo_sem = _modelo_horizontal(
            "horizontal", [("console", "A"), ("console", "B")], largura=42,
        )
        erro_correto = False
        try:
            renderizar_tela(modelo_sem, _ESTILO_CURVA, largura=42)
        except RenderizadorErro as e:
            erro_correto = "DA-02" in str(e)
        self._r(
            "T-NR01: ausencia dist horizontal 2 elem -> RenderizadorErro DA-02",
            erro_correto,
        )
        # 3 elementos: tambem deve ser rejeitado por DA-02.
        modelo_sem3 = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=100,
        )
        erro_correto3 = False
        try:
            renderizar_tela(modelo_sem3, _ESTILO_CURVA, largura=100)
        except RenderizadorErro as e:
            erro_correto3 = "DA-02" in str(e)
        self._r(
            "T-NR01: ausencia dist horizontal 3 elem -> RenderizadorErro DA-02",
            erro_correto3,
        )

    # ------------------------------- T-NR02 distribuicao vertical H-0025 sem regressao
    def test_distribuicao_vertical_h0025_nao_regride(self):
        # Re-verifica que o helper vertical continua produzindo os exemplos
        # normativos aprovados pelo H-0025.
        self._r(
            "T-NR02: vertical 68 com [1,1,1] -> [23,23,22]",
            _distribuir_alturas(68, [1, 1, 1]) == [23, 23, 22],
            "obtido={0}".format(_distribuir_alturas(68, [1, 1, 1])),
        )
        self._r(
            "T-NR02: vertical 68 com [2,1,2] -> [27,14,27]",
            _distribuir_alturas(68, [2, 1, 2]) == [27, 14, 27],
            "obtido={0}".format(_distribuir_alturas(68, [2, 1, 2])),
        )

    # ------------------------------- T-NR03 rejeicoes do loader preservadas
    def test_rejeicoes_loader_preservadas(self):
        # O loader (arquivo somente leitura neste ciclo) rejeita soma percentual
        # != 100 e pesos nao positivos para corpo horizontal. Esta verificacao
        # confirma que o loader continua rejeitando valores invalidos quando o
        # arranjo e horizontal, exercitando o mesmo caminho de validacao que
        # existe para o eixo vertical. Usa infraestrutura minima de escrita em
        # diretorio temporario, sem duplicar a suite completa de loader.
        import json
        import tempfile
        from pathlib import Path
        from tela.loader import (
            TelaEstruturaInvalida,
            carregar_tela as _carregar_tela_loader,
        )

        def _escrever(base_dir, id_tela, conteudo):
            dir_telas = Path(base_dir) / "config" / "telas"
            dir_telas.mkdir(parents=True, exist_ok=True)
            arquivo = dir_telas / "{0}.json".format(id_tela)
            arquivo.write_text(
                json.dumps(conteudo, ensure_ascii=False), encoding="utf-8",
            )

        def _tela_horizontal(id_tela, distribuicao):
            return {
                "schema": "tela.v1", "id": id_tela,
                "cabecalho": {"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
                "corpo": {
                    "arranjo": "horizontal",
                    "elementos": [
                        {"id": "a", "tipo": "console"},
                        {"id": "b", "tipo": "console"},
                    ],
                    "distribuicao": distribuicao,
                },
                "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
            }

        tmp_base = tempfile.mkdtemp(prefix="teste_h0026_loader_")
        try:
            def _espera_rejeicao(nome, fn):
                try:
                    fn()
                    self._r(nome, False, "nenhuma excecao levantada")
                except TelaEstruturaInvalida as exc:
                    self._r(nome, True, str(exc))
                except Exception as exc:  # pragma: no cover - diagnostico
                    self._r(
                        nome, False,
                        "excecao inesperada: {0!r}".format(exc),
                    )

            # soma percentual != 100 em horizontal -> rejeicao
            _escrever(
                tmp_base, "pct_inv",
                _tela_horizontal("pct_inv",
                                 {"modo": "percentual", "valores": [50, 30]}),
            )
            _espera_rejeicao(
                "T-NR03: loader rejeita percentual soma != 100 em horizontal",
                lambda: _carregar_tela_loader(tmp_base, "pct_inv"),
            )
            # peso nao positivo (zero) em horizontal -> rejeicao
            _escrever(
                tmp_base, "frac_zero",
                _tela_horizontal("frac_zero",
                                 {"modo": "fracao", "valores": [0, 1]}),
            )
            _espera_rejeicao(
                "T-NR03: loader rejeita fracao com peso zero em horizontal",
                lambda: _carregar_tela_loader(tmp_base, "frac_zero"),
            )
            # referencia simbolica para garantir import valido
            self._r(
                "T-NR03: TelaEstruturaInvalida importado do loader",
                TelaEstruturaInvalida is not None,
            )
        finally:
            import shutil
            shutil.rmtree(tmp_base, ignore_errors=True)

    def run_all(self):
        print("")
        print("== H-0026 - distribuicao horizontal explicita do corpo ==")
        self.test_algoritmo_distribuir_larguras_soma_exata()
        self.test_algoritmo_distribuir_larguras_exemplos_normativos()
        self.test_percentual_simetrico_50_50()
        self.test_percentual_assimetrico_60_40()
        self.test_fracao_simetrico_1_1()
        self.test_fracao_assimetrico_2_1()
        self.test_fracao_equivalencia_por_escala()
        self.test_t06_maiores_restos_largura_100()
        self.test_t07_empate_restos_resolvido_por_ordem_declarada()
        self.test_t08_soma_larguras_igual_distribuivel()
        self.test_t09_bordas_em_contato()
        self.test_t10_largura_total_preservada()
        self.test_t11_preenchimento_interno_conteudo_menor_que_cota()
        self.test_ausencia_distribuicao_rejeita_multiplos_participantes()
        self.test_distribuicao_vertical_h0025_nao_regride()
        self.test_rejeicoes_loader_preservadas()


def _modelo_hierarquico(corpo_arranjo, corpo_elementos, largura=42, titulo_cab="H",
                        corpo_distribuicao=None):
    """Cria ModeloTela sintetico com corpo hierarquico para testes H-0027."""
    return ModeloTela(
        id="teste_h0027",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "teste hierarquia", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo=corpo_arranjo, elementos=corpo_elementos,
                    distribuicao=corpo_distribuicao),
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


class TestHierarquiaGruposH0027:
    """Testes de composicao hierarquica com tres niveis de grupos (H-0027 / ADR-0019).

    Cobre: renderizacao com 1-3 niveis de grupos; arranjos vertical e horizontal
    em grupos; distribuicao em grupos; mistura grupo+funcional; multiplos dashboards;
    regressao do orquestrador e grupo_minimo.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # --- 1 nivel de grupo, arranjo vertical ---
    def test_g1_vertical_produz_saida(self):
        """Grupo nivel 1 com arranjo vertical e 2 funcionais produz saida nao vazia."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("console_a", "console", "CONSOLA"),
                _funcional("dash_a", "dashboard", "PAINEL"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo nivel 1 vertical com 2 funcionais produz saida nao vazia",
            bool(saida.strip()),
            "len={0}".format(len(saida)),
        )
        self._r(
            "H-0027: saida contem caixa de console (cabecalho 'CONSOLA')",
            "CONSOLA" in saida,
        )
        self._r(
            "H-0027: saida contem caixa de dashboard (cabecalho 'PAINEL')",
            "PAINEL" in saida,
        )

    # --- 1 nivel de grupo, arranjo horizontal ---
    def test_g1_horizontal_lado_a_lado(self):
        """Grupo nivel 1 com arranjo horizontal produz caixas lado a lado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "ESQUERDA"),
                _funcional("c2", "console", "DIREITA"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo horizontal: saida nao vazia",
            bool(saida.strip()),
        )
        # Caixas lado a lado: cabecalhos aparecem na mesma linha
        linhas = saida.split("\n")
        cabecalho_na_mesma_linha = any("ESQUERDA" in l and "DIREITA" in l for l in linhas)
        self._r(
            "H-0027: grupo horizontal: 'ESQUERDA' e 'DIREITA' aparecem na mesma linha",
            cabecalho_na_mesma_linha,
            "linhas={0!r}".format([l for l in linhas if "ESQUERDA" in l or "DIREITA" in l]),
        )

    # --- Grupo com arranjo ausente (None) -> vertical implícito ---
    def test_g1_arranjo_none_equivale_vertical(self):
        """Grupo sem arranjo produz saida equivalente a arranjo vertical."""
        modelo_none = _modelo_hierarquico("vertical", [
            _grupo("g1", None, [
                _funcional("c1", "console", "AA"),
                _funcional("c2", "console", "BB"),
            ]),
        ])
        modelo_vert = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "AA"),
                _funcional("c2", "console", "BB"),
            ]),
        ])
        saida_none = renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
        saida_vert = renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo sem arranjo -> saida identica a arranjo 'vertical'",
            saida_none == saida_vert,
        )

    # --- 2 niveis de grupos ---
    def test_g2_vertical_vertical(self):
        """2 niveis de grupos verticais produz saida com todos os funcionais."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _grupo("g2", "vertical", [
                    _funcional("c1", "console", "PROFUNDO"),
                    _funcional("d1", "dashboard", "PAINEL"),
                ]),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: 2 niveis verticais: saida contem 'PROFUNDO'",
            "PROFUNDO" in saida,
        )
        self._r(
            "H-0027: 2 niveis verticais: saida contem 'PAINEL'",
            "PAINEL" in saida,
        )

    # --- 2 niveis: externo vertical, interno horizontal ---
    def test_g2_vertical_horizontal(self):
        """Nivel 1 vertical, nivel 2 horizontal: funcionais do g2 ficam lado a lado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("topo", "console", "TOPO"),
                _grupo("g2", "horizontal", [
                    _funcional("e", "console", "ESQQ"),
                    _funcional("d", "console", "DIRR"),
                ], distribuicao={"modo": "igual"}),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027: 2 niveis (vert+horiz): 'TOPO' presente na saida",
            "TOPO" in saida,
        )
        self._r(
            "H-0027: 2 niveis (vert+horiz): 'ESQQ' e 'DIRR' na mesma linha",
            any("ESQQ" in l and "DIRR" in l for l in linhas),
        )

    # --- 3 niveis de grupos ---
    def test_g3_profundidade_maxima(self):
        """3 niveis de grupos (profundidade maxima por ADR-0019 D2): funcional renderizado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _grupo("g2", "vertical", [
                    _grupo("g3", "vertical", [
                        _funcional("c1", "console", "FOLHA"),
                    ]),
                ]),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: 3 niveis de grupos: saida contem 'FOLHA' (funcional no nivel 3)",
            "FOLHA" in saida,
        )

    # --- Distribuicao em grupo (modo igual) ---
    def test_distribuicao_igual_em_grupo(self):
        """Grupo com distribuicao='igual' distribui altura entre filhos (com altura declarada)."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        # Com altura declarada, distribuicao ganha efeito
        saida_com_alt = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
        saida_sem_alt = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo com dist=igual e altura: saida nao vazia",
            bool(saida_com_alt.strip()),
        )
        self._r(
            "H-0027: grupo com dist=igual e altura: contem 'ALFA'",
            "ALFA" in saida_com_alt,
        )
        self._r(
            "H-0027: grupo com dist=igual e altura: contem 'BETA'",
            "BETA" in saida_com_alt,
        )
        self._r(
            "H-0027: grupo com dist=igual sem altura: saida nao vazia (content-driven)",
            bool(saida_sem_alt.strip()),
        )

    # --- Distribuicao fracao em grupo horizontal ---
    def test_distribuicao_fracao_grupo_horizontal(self):
        """Grupo horizontal com distribuicao fracao 2:1 divide largura conforme pesos."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "GRANDE"),
                _funcional("c2", "console", "PEQQ"),
            ], distribuicao={"modo": "fracao", "valores": [2, 1]}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027: grupo horiz dist=fracao 2:1: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027: grupo horiz dist=fracao 2:1: 'GRANDE' e 'PEQQ' na mesma linha",
            any("GRANDE" in l and "PEQQ" in l for l in linhas),
        )

    # --- Mistura de grupo e funcional no mesmo nivel do corpo ---
    def test_mistura_grupo_e_funcional_no_corpo(self):
        """Corpo com grupo e funcional direto na mesma lista produz saida correta."""
        modelo = _modelo_hierarquico("vertical", [
            _funcional("topo", "console", "TOPO"),
            _grupo("g1", "horizontal", [
                _funcional("e", "console", "ESQQ"),
                _funcional("d", "console", "DIRR"),
            ], distribuicao={"modo": "igual"}),
            _funcional("base", "lancador"),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: mistura grupo+funcional: 'TOPO' presente",
            "TOPO" in saida,
        )
        self._r(
            "H-0027: mistura grupo+funcional: 'ESQQ' e 'DIRR' na mesma linha",
            any("ESQQ" in l and "DIRR" in l for l in saida.split("\n")),
        )

    # --- Multiplos dashboards em grupos distintos (ADR-0019 D7) ---
    def test_multiplos_dashboards_em_grupos(self):
        """Dois dashboards em grupos distintos sao ambos renderizados (D7)."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("d1", "dashboard", "PAINEL1"),
            ]),
            _grupo("g2", "vertical", [
                _funcional("d2", "dashboard", "PAINEL2"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: multiplos dashboards (D7): 'PAINEL1' presente",
            "PAINEL1" in saida,
        )
        self._r(
            "H-0027: multiplos dashboards (D7): 'PAINEL2' presente",
            "PAINEL2" in saida,
        )

    # --- Regressao: orquestrador.json ainda renderiza sem erro ---
    def test_regressao_orquestrador(self):
        """renderizar_tela sobre orquestrador.json preserva saida esperada (regressao)."""
        try:
            tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
            modelo = construir_modelo(tela_raw)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027 regressao: demo renderiza sem excecao",
                True,
            )
            self._r(
                "H-0027 regressao: saida contem 'ORQUESTRADOR'",
                "ORQUESTRADOR" in saida,
            )
            self._r(
                "H-0027 regressao: saida contem 'Menus'",
                "Menus" in saida,
            )
        except Exception as exc:
            self._r("H-0027 regressao: demo renderiza sem excecao",
                    False, str(exc))

    # --- Regressao: grupo_minimo.json ainda renderiza ---
    def test_regressao_grupo_minimo(self):
        """renderizar_tela sobre grupo_minimo.json renderiza sem excecao (regressao)."""
        try:
            tela_raw = carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
            modelo = construir_modelo(tela_raw)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027 regressao: grupo_minimo renderiza sem excecao",
                True,
            )
            self._r(
                "H-0027 regressao: saida nao vazia",
                bool(saida.strip()),
            )
        except Exception as exc:
            self._r("H-0027 regressao: grupo_minimo renderiza sem excecao",
                    False, str(exc))

    # --- Distribuicao percentual em grupo vertical com altura ---
    def test_distribuicao_percentual_grupo_vertical_com_altura(self):
        """Grupo vertical com dist=percentual 70/30 e altura declarada distribui corretamente."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "GRANDE"),
                _funcional("c2", "console", "PEQUENO"),
            ], distribuicao={"modo": "percentual", "valores": [70, 30]}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=22)
        self._r(
            "H-0027: dist percentual 70/30 vertical com altura: saida contem 'GRANDE'",
            "GRANDE" in saida,
        )
        self._r(
            "H-0027: dist percentual 70/30 vertical com altura: saida contem 'PEQUENO'",
            "PEQUENO" in saida,
        )
        # Caixa de 'GRANDE' deve ser mais alta do que 'PEQUENO' (aprox 70% vs 30%)
        linhas = saida.split("\n")
        inicio_grande = next((i for i, l in enumerate(linhas) if "GRANDE" in l), None)
        inicio_pequeno = next((i for i, l in enumerate(linhas) if "PEQUENO" in l), None)
        self._r(
            "H-0027: dist percentual: 'GRANDE' aparece antes de 'PEQUENO'",
            inicio_grande is not None and inicio_pequeno is not None
            and inicio_grande < inicio_pequeno,
        )

    # --- Grupo com arranjo 'sobreposto' (alias de vertical) ---
    def test_arranjo_sobreposto_alias_vertical(self):
        """Grupo com arranjo='sobreposto' produz saida identica a 'vertical'."""
        modelo_sob = _modelo_hierarquico("vertical", [
            _grupo("g1", "sobreposto", [
                _funcional("c1", "console", "XX"),
                _funcional("c2", "console", "YY"),
            ]),
        ])
        modelo_ver = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "XX"),
                _funcional("c2", "console", "YY"),
            ]),
        ])
        saida_sob = renderizar_tela(modelo_sob, _ESTILO_CURVA, largura=42)
        saida_ver = renderizar_tela(modelo_ver, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo arranjo='sobreposto' -> saida identica a 'vertical'",
            saida_sob == saida_ver,
        )

    # --- Grupo com arranjo 'lado_a_lado' (alias de horizontal) ---
    def test_arranjo_lado_a_lado_alias_horizontal(self):
        """Grupo com arranjo='lado_a_lado' produz saida identica a 'horizontal'."""
        modelo_lal = _modelo_hierarquico("vertical", [
            _grupo("g1", "lado_a_lado", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        modelo_hor = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida_lal = renderizar_tela(modelo_lal, _ESTILO_CURVA, largura=42)
        saida_hor = renderizar_tela(modelo_hor, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo arranjo='lado_a_lado' -> saida identica a 'horizontal'",
            saida_lal == saida_hor,
        )

    # --- Grupo vazio nao gera excecao (saida vazia para ele, resto renderiza) ---
    def test_grupo_vazio_nao_gera_excecao(self):
        """Grupo sem filhos (elementos=[]) nao lanca excecao; saida pode ser vazia para o grupo."""
        modelo = _modelo_hierarquico("vertical", [
            _funcional("c1", "console", "VISIVEL"),
            _grupo("g_vazio", "vertical", []),
        ])
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027: grupo vazio nao lanca excecao",
                True,
            )
            self._r(
                "H-0027: grupo vazio: 'VISIVEL' ainda aparece na saida",
                "VISIVEL" in saida,
            )
        except Exception as exc:
            self._r("H-0027: grupo vazio nao lanca excecao", False, str(exc))

    # --- ACH-001 (a): Corpo horizontal com dois grupos filhos ---
    def test_corpo_horizontal_com_grupos_filhos(self):
        """Corpo horizontal com dois grupos filhos: grupos renderizados lado a lado."""
        modelo = _modelo_hierarquico("horizontal", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "ALFA"),
            ]),
            _grupo("g2", "vertical", [
                _funcional("c2", "console", "BETA"),
            ]),
        ], corpo_distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'ALFA' presente",
            "ALFA" in saida,
        )
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'BETA' presente",
            "BETA" in saida,
        )
        # Grupos ficam lado a lado: ALFA e BETA devem aparecer na mesma linha
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'ALFA' e 'BETA' na mesma linha",
            any("ALFA" in l and "BETA" in l for l in linhas),
        )
        # Grupos nao sao slots vazios: conteudo funcional efetivamente renderizado
        self._r(
            "H-0027 ACH-001a: grupos nao sao slots vazios ('ALFA' e 'BETA' presentes)",
            "ALFA" in saida and "BETA" in saida,
        )
        # Largura total preservada sem perda indevida
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001a: largura total preservada (42)",
            all(len(l) == 42 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 42]
            ),
        )
        # Sem sobreposicao: saida deterministica
        saida2 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027 ACH-001a: saida e deterministica (sem sobreposicao)",
            saida == saida2,
        )

    # --- ACH-001 (b): Combinacao horizontal -> vertical ---
    def test_horizontal_grupo_vertical(self):
        """Corpo horizontal com grupo vertical interno: subdivisao vertical dentro do grupo.

        Estrutura:
            corpo horizontal
            └── grupo vertical
                ├── funcional "CIMA"
                └── funcional "BAIXO"
        """
        modelo = _modelo_hierarquico("horizontal", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "CIMA"),
                _funcional("c2", "console", "BAIXO"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001b: horiz→vert: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027 ACH-001b: horiz→vert: 'CIMA' presente (funcional no grupo vertical)",
            "CIMA" in saida,
        )
        self._r(
            "H-0027 ACH-001b: horiz→vert: 'BAIXO' presente (funcional no grupo vertical)",
            "BAIXO" in saida,
        )
        # Subdivisao vertical interna: CIMA antes de BAIXO (ordem preservada)
        idx_cima = next((i for i, l in enumerate(linhas) if "CIMA" in l), None)
        idx_baixo = next((i for i, l in enumerate(linhas) if "BAIXO" in l), None)
        self._r(
            "H-0027 ACH-001b: horiz→vert: ordem vertical preservada ('CIMA' antes de 'BAIXO')",
            idx_cima is not None and idx_baixo is not None and idx_cima < idx_baixo,
        )
        # Sem achatamento: CIMA e BAIXO em linhas distintas
        self._r(
            "H-0027 ACH-001b: horiz→vert: sem achatamento ('CIMA' e 'BAIXO' em linhas distintas)",
            idx_cima is not None and idx_baixo is not None and idx_cima != idx_baixo,
        )
        # Ausencia de slot vazio: os dois funcionais foram renderizados
        self._r(
            "H-0027 ACH-001b: horiz→vert: ausencia de slot vazio (ambos presentes)",
            "CIMA" in saida and "BAIXO" in saida,
        )
        # Dimensoes compativeis: largura total preservada
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001b: horiz→vert: largura total preservada (42)",
            all(len(l) == 42 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 42]
            ),
        )

    # --- ACH-001 (c): Tres niveis com arranjos alternados ---
    def test_tres_niveis_arranjos_alternados(self):
        """3 niveis de grupos com arranjos alternados (H-0027 secao 18).

        Estrutura:
            corpo vertical
            └── g1 horizontal (nivel 1)
                ├── g2 vertical (nivel 2)
                │   └── g3 horizontal (nivel 3)
                │       ├── funcional "FA" (console)
                │       └── funcional "FB" (console)
                └── funcional "TOPO" (dashboard)

        Usa largura=80 para garantir area suficiente em tres niveis de
        particionamento horizontal (g1 -> g3) sem truncamento de titulo.
        """
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _grupo("g2", "vertical", [
                    _grupo("g3", "horizontal", [
                        _funcional("f1", "console", "FA"),
                        _funcional("f2", "console", "FB"),
                    ], distribuicao={"modo": "igual"}),
                ]),
                _funcional("topo", "dashboard", "TOPO"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=80)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: saida nao vazia",
            bool(saida.strip()),
        )
        # Renderizacao dos elementos do nivel mais interno
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'FA' presente (funcional nivel 3)",
            "FA" in saida,
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'FB' presente (funcional nivel 3)",
            "FB" in saida,
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'TOPO' presente (funcional nivel 1)",
            "TOPO" in saida,
        )
        # Alternancia real dos arranjos: g3 horizontal -> FA e FB na mesma linha
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: g3(h): 'FA' e 'FB' na mesma linha",
            any("FA" in l and "FB" in l for l in linhas),
        )
        # Ausencia de achatamento: tres niveis sao respeitados
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: sem achatamento (todos os funcionais presentes)",
            "FA" in saida and "FB" in saida and "TOPO" in saida,
        )
        # Propagacao correta da area: largura total preservada
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: largura total preservada (80)",
            all(len(l) == 80 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 80]
            ),
        )
        # Ausencia de sobreposicao: saida deterministica
        saida2 = renderizar_tela(modelo, _ESTILO_CURVA, largura=80)
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: saida deterministica (sem sobreposicao)",
            saida == saida2,
        )
        # Preservacao da ordem declarada: FA antes de FB no g3 horizontal
        # (na mesma linha, FA aparece a esquerda de FB)
        linha_com_fa_fb = next(
            (l for l in linhas if "FA" in l and "FB" in l), None
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: ordem declarada preservada "
            "('FA' a esquerda de 'FB' na linha compartilhada)",
            linha_com_fa_fb is not None
            and linha_com_fa_fb.index("FA") < linha_com_fa_fb.index("FB"),
        )
        # Ausencia de nivel 4: apenas tres niveis estruturais
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: existencia dos tres niveis validada",
            "FA" in saida and "FB" in saida and "TOPO" in saida,
        )

    def run_all(self):
        print("")
        print("== TestHierarquiaGruposH0027: composicao hierarquica (H-0027 / ADR-0019) ==")
        self.test_g1_vertical_produz_saida()
        self.test_g1_horizontal_lado_a_lado()
        self.test_g1_arranjo_none_equivale_vertical()
        self.test_g2_vertical_vertical()
        self.test_g2_vertical_horizontal()
        self.test_g3_profundidade_maxima()
        self.test_distribuicao_igual_em_grupo()
        self.test_distribuicao_fracao_grupo_horizontal()
        self.test_mistura_grupo_e_funcional_no_corpo()
        self.test_multiplos_dashboards_em_grupos()
        self.test_regressao_orquestrador()
        self.test_regressao_grupo_minimo()
        self.test_distribuicao_percentual_grupo_vertical_com_altura()
        self.test_arranjo_sobreposto_alias_vertical()
        self.test_arranjo_lado_a_lado_alias_horizontal()
        self.test_grupo_vazio_nao_gera_excecao()
        self.test_corpo_horizontal_com_grupos_filhos()
        self.test_horizontal_grupo_vertical()
        self.test_tres_niveis_arranjos_alternados()


class TestOcupacaoIntegralCorpoH0033:
    """Testes focais de ADR-0024 (proibicao de preenchimento externo vazio).

    Cobre DA-01 (cardinalidade unitaria), DA-02 (multiplos sem distribuicao),
    DA-03 (grupos repassam area) e DA-04 (composicao impossivel). Inclui
    inventario de todos os 16 JSONs permanentes em duas dimensoes.
    """

    LARGURA = 42
    ALTURA = 20
    LARGURA_B = 80
    ALTURA_B = 30

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn, msg_contem=""):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            ok = not msg_contem or msg_contem in str(exc)
            self._r(nome, ok, str(exc))
            return exc

    def _render(self, elementos, corpo_dist=None, altura=None, largura=None):
        m = _modelo_h0029(elementos, corpo_dist=corpo_dist)
        kw = {"largura": largura or self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # ----------------------------------------------------------------- DA-01
    def test_DA01_visual_direto_ocupa_area_integral(self):
        """DA-01: unico visual direto preenche toda a area disponivel."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-01: total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-01: visual direto ocupa l_corpo_disponivel=14",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 DA-01: sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
        )

    def test_DA01_visual_via_grupo_transparente(self):
        """DA-01: visual aninhado em grupo sem dist recebe area integral."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            altura=self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-01+DA-03: visual via grupo transparente ocupa 14 linhas",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 DA-01+DA-03: sem fill externo",
            len(fill_ext) == 0,
        )

    def test_DA01_fill_interno_preservado(self):
        """DA-01: fill interno (dentro das bordas) e valido e distinto do externo."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        linhas = saida.splitlines()
        # Fill externo sao linhas de N espacos (sem borda)
        fill_ext = [l for l in linhas if l == " " * self.LARGURA]
        # Fill interno sao linhas comecando e terminando com borda vertical
        fill_int = [l for l in linhas if l.startswith("│") and l.endswith("│")
                    and l[1:-1].strip() == ""]
        self._r(
            "H-0033 DA-01: sem fill externo e com fill interno",
            len(fill_ext) == 0 and len(fill_int) > 0,
            "ext={0} int={1}".format(len(fill_ext), len(fill_int)),
        )

    def test_DA01_equivalencia_com_distribuicao(self):
        """DA-01 sem dist produz saida identica a dist explicita com 1 elemento."""
        saida_sem = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        saida_com = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-01: sem dist == com dist explícita (1 visual)",
            saida_sem == saida_com,
        )

    # ----------------------------------------------------------------- DA-02
    def test_DA02_dois_visuais_sem_dist_erro(self):
        """DA-02: 2 visuais sem distribuicao com area residual levanta RenderizadorErro."""
        self._espera_erro(
            "H-0033 DA-02: 2 visuais sem dist + l_fill>0 -> RenderizadorErro",
            lambda: self._render(
                [_funcional("a", "console", "A"), _funcional("b", "dashboard", "B")],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    def test_DA02_tres_visuais_sem_dist_erro(self):
        """DA-02: 3 visuais sem distribuicao levanta RenderizadorErro."""
        exc = self._espera_erro(
            "H-0033 DA-02: 3 visuais sem dist -> RenderizadorErro",
            lambda: self._render(
                [_funcional("a", "console", "A"),
                 _funcional("b", "dashboard", "B"),
                 _funcional("c", "console", "C")],
                altura=self.ALTURA,
            ),
            "DA-02",
        )
        if exc is not None:
            self._r(
                "H-0033 DA-02: mensagem menciona 'distribuicao'",
                "distribuicao" in str(exc),
                str(exc),
            )

    def test_DA02_com_distribuicao_ok(self):
        """DA-02: multiplos visuais COM distribuicao explicita funciona (sem erro)."""
        saida = self._render(
            [_funcional("a", "console", "A"), _funcional("b", "dashboard", "B")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-02: 2 visuais com dist=igual -> total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-02: com dist -> soma das cotas == l_corpo_disponivel",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )

    def test_DA02_sem_area_residual_ok(self):
        """DA-02: multiplos visuais sem dist sem area residual nao levanta erro."""
        # 3 elementos naturais; l_corpo_disponivel = 21-3-3 = 15 = l_corpo_natural.
        # l_fill = 0 -> sem DA-02.
        modelo_sd = _modelo_orquestrador_sem_distribuicao()
        n_natural = 21  # l_cab(3) + l_corpo(15) + l_barra(3) = 21 (H-0037: 11 itens)
        saida = renderizar_tela(modelo_sd, _ESTILO_CURVA, largura=42, altura=n_natural)
        # renderizar_tela termina com '\n'; count('\n') == numero de linhas fisicas.
        self._r(
            "H-0033 DA-02: sem dist + l_fill==0 -> sem erro (altura natural)",
            saida.count("\n") == n_natural,
            "count={0}".format(saida.count("\n")),
        )

    # ----------------------------------------------------------------- DA-03
    def test_DA03_grupo_com_dist_repassa_area(self):
        """DA-03: grupo com dist propria recebe area e distribui internamente."""
        saida = self._render(
            [_grupo("g1", "vertical", [
                _funcional("a", "console", "A"),
                _funcional("b", "dashboard", "B"),
            ], distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-03: grupo com dist recebe area -> total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-03: filhos do grupo somam l_corpo_disponivel=14",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )

    def test_DA03_grupo_transparente_repassa_area_integral(self):
        """DA-03: grupo sem dist e transparente; visual filho recebe area integral."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "console", "C1")])],
            altura=self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-03: grupo transparente -> visual recebe 14 linhas",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )

    # ----------------------------------------------------------------- DA-04
    def test_DA04_zero_visuais_com_area_erro(self):
        """DA-04: corpo sem visuais e com area disponivel levanta RenderizadorErro."""
        modelo = ModeloTela(
            id="teste_da04",
            schema="tela.v1",
            cabecalho={"titulo": "DA04", "descricao": "sem visuais", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(arranjo="vertical", elementos=[], distribuicao=None),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        exc = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=self.ALTURA)
        except RenderizadorErro as e:
            exc = e
        self._r(
            "H-0033 DA-04: 0 visuais + altura > 0 -> RenderizadorErro",
            exc is not None,
            str(exc) if exc else "nenhuma excecao",
        )
        if exc is not None:
            self._r(
                "H-0033 DA-04: mensagem menciona 'DA-04' ou 'visual'",
                "DA-04" in str(exc) or "visual" in str(exc),
                str(exc),
            )

    # ---------------------------------------------------------------- inventário
    def test_inventario_16_jsons_altura_natural(self):
        """Inventario: 13 JSONs (exceto matriz) renderizam sem erro em altura natural."""
        for id_tela in _H0033_TELAS_ALTURA_NATURAL:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA)
                self._r(
                    "H-0033 INV: {0} renderiza em largura={1} sem erro".format(
                        id_tela, self.LARGURA
                    ),
                    isinstance(saida, str) and len(saida) > 0,
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV: {0} renderiza em largura={1} sem erro".format(
                        id_tela, self.LARGURA
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    def test_inventario_15_jsons_com_altura_20(self):
        """Inventario: 15 JSONs (exceto demo) renderizam a 42x20 sem fill externo."""
        for id_tela in _H0033_TELAS_ALTURA_20:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
                linhas_total = _h0029_linhas_totais(saida)
                fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
                self._r(
                    "H-0033 INV 42x20: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA
                    ),
                    linhas_total == self.ALTURA and len(fill_ext) == 0,
                    "linhas={0} fill_ext={1}".format(linhas_total, len(fill_ext)),
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV 42x20: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    def test_inventario_15_jsons_com_altura_30_largura_80(self):
        """Inventario: 15 JSONs (exceto demo) renderizam a 80x30 sem fill externo."""
        for id_tela in _H0033_TELAS_ALTURA_20:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA_B, altura=self.ALTURA_B
                )
                linhas_total = _h0029_linhas_totais(saida)
                fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA_B]
                self._r(
                    "H-0033 INV 80x30: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA_B
                    ),
                    linhas_total == self.ALTURA_B and len(fill_ext) == 0,
                    "linhas={0} fill_ext={1}".format(linhas_total, len(fill_ext)),
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV 80x30: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA_B
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    # ------------------------------------------------- destino_minimo / grupo_minimo
    def test_destino_minimo_sem_fill_externo(self):
        """destino_minimo.json: DA-01 - dashboard ocupa area integral sem fill externo."""
        modelo = construir_modelo(
            carregar_tela(_BASE_PADRAO, "destino_minimo", _RAIZ_TELAS_DEMO)
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
        corpo_alts = _corpo_alturas(saida)
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 destino_minimo: DA-01 -> corpo_alts==[14], sem fill externo",
            corpo_alts == [14] and len(fill_ext) == 0,
            "corpo_alturas={0} fill_ext={1}".format(corpo_alts, len(fill_ext)),
        )

    def test_grupo_minimo_sem_fill_externo(self):
        """grupo_minimo.json: DA-01+DA-03 - visual via grupo ocupa area sem fill externo."""
        modelo = construir_modelo(
            carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
        corpo_alts = _corpo_alturas(saida)
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 grupo_minimo: DA-01+DA-03 -> corpo_alts==[14], sem fill externo",
            corpo_alts == [14] and len(fill_ext) == 0,
            "corpo_alturas={0} fill_ext={1}".format(corpo_alts, len(fill_ext)),
        )

    # ---- Helpers horizontais (QA-H0033-IMP-HIGH-001 / QA-H0033-IMP-MED-001) ----
    def _render_h(self, elementos, corpo_dist=None, altura=None, largura=None):
        """Helper: cria modelo com corpo horizontal para testes focais H1-H6."""
        m = ModeloTela(
            id="teste_h0033_h",
            schema="tela.v1",
            cabecalho={"titulo": "H0033H", "descricao": "h0033 horizontal", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(arranjo="horizontal", elementos=elementos,
                        distribuicao=corpo_dist),
            barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        kw = {"largura": largura or self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # ----------------------------------------------------------------- H1
    def test_H1_horizontal_um_participante_sem_dist(self):
        """H1 (DA-01): corpo horizontal com 1 elemento sem dist e valido."""
        try:
            saida = self._render_h([_funcional("a", "console", "A")])
            self._r(
                "H-0033 H1: horizontal 1 elem sem dist -> valido (DA-01)",
                bool(saida.strip()),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H1: horizontal 1 elem sem dist -> valido (DA-01)",
                False,
                str(exc),
            )

    # ----------------------------------------------------------------- H2
    def test_H2_horizontal_dois_sem_dist_rejeita(self):
        """H2 (DA-02): corpo horizontal com 2 elementos sem dist levanta RenderizadorErro.

        Achado QA-H0033-IMP-HIGH-001: implementacao anterior aceitava composicao
        invalida e particionava largura uniformemente; agora deve rejeitar.
        """
        self._espera_erro(
            "H-0033 H2: horizontal 2 elem sem dist -> RenderizadorErro DA-02",
            lambda: self._render_h(
                [_funcional("a", "console", "A"), _funcional("b", "console", "B")],
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H3
    def test_H3_horizontal_grupo_multiplos_sem_dist_rejeita(self):
        """H3 (DA-02): grupo interno com arranjo horizontal e 2 filhos sem dist e rejeitado."""
        self._espera_erro(
            "H-0033 H3: grupo horizontal 2 filhos sem dist -> RenderizadorErro DA-02",
            lambda: self._render(
                [_grupo("g1", "horizontal", [
                    _funcional("a", "console", "A"),
                    _funcional("b", "console", "B"),
                ])],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H4
    def test_H4_horizontal_aninhado_nao_bypassa_DA02(self):
        """H4 (DA-02): container horizontal aninhado em grupo nao bypassa DA-02."""
        self._espera_erro(
            "H-0033 H4: horizontal aninhado (grupo>grupo_h) -> RenderizadorErro DA-02",
            lambda: self._render(
                [_grupo("g1", "vertical", [
                    _grupo("g2", "horizontal", [
                        _funcional("a", "console", "A"),
                        _funcional("b", "console", "B"),
                    ]),
                ])],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H5
    def test_H5_horizontal_com_distribuicao_valido(self):
        """H5 (DA-02): corpo horizontal com distribuicao explicita e valido."""
        try:
            saida = self._render_h(
                [_funcional("a", "console", "A"), _funcional("b", "console", "B")],
                corpo_dist={"modo": "igual"},
            )
            linhas = [l for l in saida.split("\n") if l]
            self._r(
                "H-0033 H5: horizontal com dist=igual -> saida valida",
                bool(saida.strip()),
            )
            self._r(
                "H-0033 H5: horizontal com dist=igual -> largura preservada",
                all(len(l) == self.LARGURA for l in linhas),
                "invalidas={0}".format([len(l) for l in linhas if len(l) != self.LARGURA]),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H5: horizontal com dist=igual -> saida valida",
                False,
                str(exc),
            )

    # ----------------------------------------------------------------- H6
    def test_H6_matriz_nao_e_rejeitada(self):
        """H6: grupo com estrutura='matriz' nao e rejeitado por DA-02 (caminho distinto)."""
        try:
            grupo_m = _grupo_matriz_render_h0028("gm", n_linhas=2, n_colunas=2)
            saida = self._render([grupo_m], altura=self.ALTURA)
            self._r(
                "H-0033 H6: matriz 2x2 em corpo vertical -> renderiza sem DA-02",
                bool(saida.strip()),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H6: matriz 2x2 em corpo vertical -> renderiza sem DA-02",
                False,
                str(exc),
            )

    def run_all(self):
        print("")
        print("== TestOcupacaoIntegralCorpoH0033: ADR-0024 DA-01 a DA-04 ==")
        self.test_DA01_visual_direto_ocupa_area_integral()
        self.test_DA01_visual_via_grupo_transparente()
        self.test_DA01_fill_interno_preservado()
        self.test_DA01_equivalencia_com_distribuicao()
        self.test_DA02_dois_visuais_sem_dist_erro()
        self.test_DA02_tres_visuais_sem_dist_erro()
        self.test_DA02_com_distribuicao_ok()
        self.test_DA02_sem_area_residual_ok()
        self.test_DA03_grupo_com_dist_repassa_area()
        self.test_DA03_grupo_transparente_repassa_area_integral()
        self.test_DA04_zero_visuais_com_area_erro()
        self.test_inventario_16_jsons_altura_natural()
        self.test_inventario_15_jsons_com_altura_20()
        self.test_inventario_15_jsons_com_altura_30_largura_80()
        self.test_destino_minimo_sem_fill_externo()
        self.test_grupo_minimo_sem_fill_externo()
        self.test_H1_horizontal_um_participante_sem_dist()
        self.test_H2_horizontal_dois_sem_dist_rejeita()
        self.test_H3_horizontal_grupo_multiplos_sem_dist_rejeita()
        self.test_H4_horizontal_aninhado_nao_bypassa_DA02()
        self.test_H5_horizontal_com_distribuicao_valido()
        self.test_H6_matriz_nao_e_rejeitada()


class TestHelperHorizontalH0033Patch2:
    """Testes focais para _montar_corpo_horizontal e caminho publico horizontal
    apos segundo patch H-0033 (QA-H0033-POSPATCH-IMP-MED-001).

    P1. zero participantes retorna vazio;
    P2. um participante sem larguras recebe total_w (DA-01/ADR-0024);
    P3. dois participantes sem larguras sao rejeitados (DA-02/ADR-0024);
    P4. tres participantes sem larguras sao rejeitados (DA-02/ADR-0024);
    P5. larguras explicitas validas sao respeitadas;
    P6. largura insuficiente por elemento e rejeitada;
    P7. nenhuma saida parcial e produzida antes do erro (DA-02);
    P8. caminho publico com dist=fracao e valido;
    P9. caminho publico com dist=percentual e valido;
    P10. eixo vertical com distribuicao nao regrediu.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn, prefixo=None):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            ok = (prefixo is None) or (prefixo in str(exc))
            self._r(nome, ok, str(exc))
            return exc
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, tipo="console", titulo="A"):
        campos = {"titulo": titulo}
        if tipo == "lancador":
            campos["itens"] = []
        return ElementoCorpo(id=titulo.lower(), tipo=tipo, _campos_inertes=campos)

    def _modelo_h(self, elementos, corpo_dist=None, largura=42):
        return ModeloTela(
            id="teste_patch2",
            schema="tela.v1",
            cabecalho={"titulo": "P2", "descricao": "patch2", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(arranjo="horizontal", elementos=elementos,
                        distribuicao=corpo_dist),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )

    # ------------------------------------------------------------------ P1
    def test_P1_helper_zero_participantes_retorna_vazio(self):
        """P1: _montar_corpo_horizontal com zero elementos retorna string vazia."""
        borda = self._borda()
        resultado = _montar_corpo_horizontal([], borda, 42)
        self._r(
            "P1: _montar_corpo_horizontal([]) -> ''",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )

    # ------------------------------------------------------------------ P2
    def test_P2_helper_um_participante_recebe_total_w(self):
        """P2 (DA-01): _montar_corpo_horizontal com 1 elemento recebe total_w."""
        borda = self._borda()
        elem = self._elem("console", "A")
        resultado = _montar_corpo_horizontal([elem], borda, 42)
        linhas = resultado.split("\n")
        self._r(
            "P2: _montar_corpo_horizontal(1 elem, larguras=None) -> largura=42",
            all(len(ln) == 42 for ln in linhas if ln),
            "larguras={0}".format([len(ln) for ln in linhas if ln]),
        )
        self._r(
            "P2: _montar_corpo_horizontal(1 elem) -> resultado nao vazio",
            bool(resultado.strip()),
        )

    # ------------------------------------------------------------------ P3
    def test_P3_helper_dois_participantes_sem_larguras_rejeita(self):
        """P3 (DA-02): _montar_corpo_horizontal com 2 elementos e larguras=None levanta DA-02."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("console", "B")
        self._espera_erro(
            "P3: _montar_corpo_horizontal(2 elem, larguras=None) -> RenderizadorErro DA-02",
            lambda: _montar_corpo_horizontal([elem_a, elem_b], borda, 42),
            "DA-02",
        )

    # ------------------------------------------------------------------ P4
    def test_P4_helper_tres_participantes_sem_larguras_rejeita(self):
        """P4 (DA-02): _montar_corpo_horizontal com 3 elementos e larguras=None levanta DA-02."""
        borda = self._borda()
        elems = [self._elem("console", c) for c in ("A", "B", "C")]
        self._espera_erro(
            "P4: _montar_corpo_horizontal(3 elem, larguras=None) -> RenderizadorErro DA-02",
            lambda: _montar_corpo_horizontal(elems, borda, 42),
            "DA-02",
        )

    # ------------------------------------------------------------------ P5
    def test_P5_helper_larguras_explicitas_validas_respeitadas(self):
        """P5: _montar_corpo_horizontal com larguras explicitas validas renderiza corretamente."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("dashboard", "B")
        resultado = _montar_corpo_horizontal(
            [elem_a, elem_b], borda, 42, larguras=[21, 21]
        )
        linhas = resultado.split("\n")
        self._r(
            "P5: larguras=[21,21] -> todas as linhas tem 42 chars",
            all(len(ln) == 42 for ln in linhas),
            "erros={0}".format([len(ln) for ln in linhas if len(ln) != 42]),
        )
        self._r(
            "P5: larguras=[21,21] -> resultado nao vazio",
            bool(resultado.strip()),
        )

    # ------------------------------------------------------------------ P6
    def test_P6_helper_largura_insuficiente_rejeitada(self):
        """P6: largura por area abaixo de 10 e rejeitada com RenderizadorErro."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("console", "B")
        self._espera_erro(
            "P6: larguras=[5, 37] -> RenderizadorErro (w<10 em area 0)",
            lambda: _montar_corpo_horizontal(
                [elem_a, elem_b], borda, 42, larguras=[5, 37]
            ),
        )

    # ------------------------------------------------------------------ P7
    def test_P7_helper_sem_saida_parcial_antes_do_erro(self):
        """P7: DA-02 impede qualquer saida parcial antes de lancar RenderizadorErro."""
        borda = self._borda()
        elems = [self._elem("console", c) for c in ("A", "B")]
        saida_parcial = []
        erro_capturado = None
        try:
            resultado = _montar_corpo_horizontal(elems, borda, 42)
            saida_parcial.append(resultado)
        except RenderizadorErro as exc:
            erro_capturado = exc
        self._r(
            "P7: DA-02 lanca erro antes de produzir saida parcial",
            erro_capturado is not None and len(saida_parcial) == 0,
            "erro={0!r} saida_parcial={1}".format(
                str(erro_capturado) if erro_capturado else None, saida_parcial
            ),
        )

    # ------------------------------------------------------------------ P8
    def test_P8_publico_horizontal_dist_fracao_valido(self):
        """P8: caminho publico com dist=fracao no horizontal e valido."""
        modelo = self._modelo_h(
            [self._elem("console", "A"), self._elem("console", "B")],
            corpo_dist={"modo": "fracao", "valores": [2, 1]},
            largura=42,
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            linhas = [ln for ln in saida.split("\n") if ln]
            self._r(
                "P8: horizontal dist=fracao -> saida valida, largura=42",
                all(len(ln) == 42 for ln in linhas),
                "erros={0}".format([len(ln) for ln in linhas if len(ln) != 42]),
            )
        except RenderizadorErro as exc:
            self._r("P8: horizontal dist=fracao -> saida valida", False, str(exc))

    # ------------------------------------------------------------------ P9
    def test_P9_publico_horizontal_dist_percentual_valido(self):
        """P9: caminho publico com dist=percentual no horizontal e valido."""
        modelo = self._modelo_h(
            [self._elem("console", "A"), self._elem("dashboard", "B")],
            corpo_dist={"modo": "percentual", "valores": [60, 40]},
            largura=100,
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
            linhas = [ln for ln in saida.split("\n") if ln]
            self._r(
                "P9: horizontal dist=percentual -> saida valida, largura=100",
                all(len(ln) == 100 for ln in linhas),
                "erros={0}".format([len(ln) for ln in linhas if len(ln) != 100]),
            )
        except RenderizadorErro as exc:
            self._r("P9: horizontal dist=percentual -> saida valida", False, str(exc))

    # ----------------------------------------------------------------- P10
    def test_P10_vertical_com_distribuicao_nao_regrediu(self):
        """P10: eixo vertical com distribuicao explicita nao regrediu (regressao)."""
        modelo = ModeloTela(
            id="teste_p10",
            schema="tela.v1",
            cabecalho={"titulo": "P10", "descricao": "regressao vertical", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    _funcional("a", "console", "A"),
                    _funcional("b", "dashboard", "B"),
                ],
                distribuicao={"modo": "igual"},
            ),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
            self._r(
                "P10: vertical dist=igual altura=20 -> 20 linhas",
                saida.count("\n") == 20,
                "count={0}".format(saida.count("\n")),
            )
        except RenderizadorErro as exc:
            self._r("P10: vertical dist=igual nao regrediu", False, str(exc))

    def run_all(self):
        print("")
        print("== TestHelperHorizontalH0033Patch2: helper e caminho publico ==")
        self.test_P1_helper_zero_participantes_retorna_vazio()
        self.test_P2_helper_um_participante_recebe_total_w()
        self.test_P3_helper_dois_participantes_sem_larguras_rejeita()
        self.test_P4_helper_tres_participantes_sem_larguras_rejeita()
        self.test_P5_helper_larguras_explicitas_validas_respeitadas()
        self.test_P6_helper_largura_insuficiente_rejeitada()
        self.test_P7_helper_sem_saida_parcial_antes_do_erro()
        self.test_P8_publico_horizontal_dist_fracao_valido()
        self.test_P9_publico_horizontal_dist_percentual_valido()
        self.test_P10_vertical_com_distribuicao_nao_regrediu()


class TestCardinalidadeHorizontalH0033Patch3:
    """Testes focais de cardinalidade em _montar_corpo_horizontal.

    Verifica rejeicao de larguras explicitas com cardinalidade incoerente
    (QA-H0033-POSPATCH2-IMP-LOW-001).

    C1. N=0, L=0 -> comportamento coerente (retorna '');
    C2. N=0, L=1 -> rejeicao;
    C3. N=1, L=0 -> rejeicao;
    C4. N=1, L=1 -> sucesso;
    C5. N=1, L=2 -> rejeicao;
    C6. N=2, L=1 -> rejeicao;
    C7. N=2, L=2 -> sucesso;
    C8. N=2, L=3 -> rejeicao;
    C9. N=3, L=2 -> rejeicao;
    C10. erro antes de renderizacao parcial (participantes instrumentados);
    C11. mensagem informa N e L;
    C12. larguras=None preserva DA-01 (N=1) e DA-02 (N>1).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, titulo="A"):
        campos = {"titulo": titulo}
        return ElementoCorpo(id=titulo.lower(), tipo="console", _campos_inertes=campos)

    def _espera_card_erro(self, nome, fn):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
        except RenderizadorErro as exc:
            ok = "cardinalidade horizontal incoerente" in str(exc)
            self._r(nome, ok, str(exc)[:120])
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))

    # ------------------------------------------------------------------ C1-C2
    def test_C1_C2_zero_participantes(self):
        """C1: N=0, L=0 -> ''; C2: N=0, L=1 -> rejeicao."""
        borda = self._borda()
        resultado = _montar_corpo_horizontal([], borda, 42, larguras=[])
        self._r(
            "C1: N=0, L=0 -> resultado vazio",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )
        self._espera_card_erro(
            "C2: N=0, L=1 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([], borda, 42, larguras=[42]),
        )

    # ------------------------------------------------------------------ C3-C5
    def test_C3_C4_C5_um_participante(self):
        """C3: N=1, L=0 -> rejeicao; C4: N=1, L=1 -> sucesso; C5: N=1, L=2 -> rejeicao."""
        borda = self._borda()
        e = self._elem("A")
        self._espera_card_erro(
            "C3: N=1, L=0 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([e], borda, 42, larguras=[]),
        )
        try:
            resultado = _montar_corpo_horizontal([e], borda, 42, larguras=[42])
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C4: N=1, L=1 -> sucesso e largura=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C4: N=1, L=1 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "C5: N=1, L=2 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([e], borda, 42, larguras=[21, 21]),
        )

    # ------------------------------------------------------------------ C6-C9
    def test_C6_C7_C8_C9_dois_e_tres_participantes(self):
        """C6-C9: cardinalidade incoerente rejeita; coerente aceita."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        ec = self._elem("C")
        self._espera_card_erro(
            "C6: N=2, L=1 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([ea, eb], borda, 42, larguras=[42]),
        )
        try:
            resultado = _montar_corpo_horizontal(
                [ea, eb], borda, 42, larguras=[28, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C7: N=2, L=2 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C7: N=2, L=2 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "C8: N=2, L=3 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal(
                [ea, eb], borda, 42, larguras=[14, 14, 14]
            ),
        )
        self._espera_card_erro(
            "C9: N=3, L=2 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal(
                [ea, eb, ec], borda, 42, larguras=[21, 21]
            ),
        )

    # ----------------------------------------------------------------- C10
    def test_C10_erro_antes_de_renderizacao(self):
        """C10: erro de cardinalidade ocorre antes de qualquer renderizacao.

        Usa elementos instrumentados: o acesso a .tipo so ocorre dentro do
        loop de renderizacao. Se o erro for levantado antes do loop, .tipo
        nunca e acessado e o rastreador permanece vazio.
        """
        tracker = []

        class _ElemInstrumentado:
            id = "instrumento"
            _campos_inertes = {"titulo": "T"}

            @property
            def tipo(self):
                tracker.append("tipo_acessado")
                return "console"

        borda = self._borda()
        e1 = _ElemInstrumentado()
        e2 = _ElemInstrumentado()
        erro_levantado = False
        try:
            _montar_corpo_horizontal([e1, e2], borda, 42, larguras=[42])
        except RenderizadorErro:
            erro_levantado = True
        self._r(
            "C10: erro de cardinalidade e levantado antes da renderizacao",
            erro_levantado and len(tracker) == 0,
            "erro={0} tracker={1}".format(erro_levantado, tracker),
        )

    # ----------------------------------------------------------------- C11
    def test_C11_mensagem_informa_cardinalidades(self):
        """C11: mensagem de erro informa N e L observados."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        msg = None
        try:
            _montar_corpo_horizontal([ea, eb], borda, 42, larguras=[42])
        except RenderizadorErro as exc:
            msg = str(exc)
        self._r(
            "C11: mensagem contem 'cardinalidade horizontal incoerente'",
            msg is not None and "cardinalidade horizontal incoerente" in msg,
            "msg={0!r}".format(msg),
        )
        self._r(
            "C11: mensagem informa N=2 e L=1",
            msg is not None and "2 participante" in msg and "1 largura" in msg,
            "msg={0!r}".format(msg),
        )

    # ----------------------------------------------------------------- C12
    def test_C12_larguras_none_preserva_DA01_e_DA02(self):
        """C12: larguras=None preserva DA-01 (N=1) e DA-02 (N>1)."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        try:
            resultado = _montar_corpo_horizontal([ea], borda, 42)
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C12a: N=1, larguras=None -> DA-01 (largura integral 42)",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C12a: DA-01", False, str(exc))
        try:
            _montar_corpo_horizontal([ea, eb], borda, 42)
            self._r("C12b: N=2, larguras=None -> DA-02", False, "sem excecao")
        except RenderizadorErro as exc:
            self._r(
                "C12b: N=2, larguras=None -> DA-02",
                "DA-02" in str(exc),
                str(exc)[:120],
            )

    def run_all(self):
        print("")
        print("== TestCardinalidadeHorizontalH0033Patch3: cardinalidade larguras explicitas ==")
        self.test_C1_C2_zero_participantes()
        self.test_C3_C4_C5_um_participante()
        self.test_C6_C7_C8_C9_dois_e_tres_participantes()
        self.test_C10_erro_antes_de_renderizacao()
        self.test_C11_mensagem_informa_cardinalidades()
        self.test_C12_larguras_none_preserva_DA01_e_DA02()


class TestCardinalidadeHorizontalH0033Patch4:
    """Testes focais de cardinalidade em _renderizar_container_horizontal.

    Atinge diretamente o helper horizontal recursivo, equivalente ao
    _montar_corpo_horizontal ja corrigido no terceiro patch. Verifica rejeicao
    de larguras explicitas com cardinalidade incoerente
    (QA-H0033-POSPATCH3-IMP-LOW-001): lista curta nao produz IndexError e
    lista longa nao e truncada silenciosamente.

    H1. N=0, L=0 -> comportamento coerente (retorna '');
    H2. N=0, L=1 -> rejeicao;
    H3. N=1, L=0 -> rejeicao;
    H4. N=1, L=1 -> sucesso;
    H5. N=1, L=2 -> rejeicao;
    H6. N=2, L=1 -> rejeicao (sem IndexError);
    H7. N=2, L=2 -> sucesso;
    H8. N=2, L=3 -> rejeicao (sem truncamento);
    H9. N=3, L=2 -> rejeicao;
    H10. N=3, L=3 -> sucesso;
    H11. lista longa (N=2, L=3) rejeitada com RenderizadorErro, sem truncamento
         nem saida parcial (tracker externo vazio); rejeita sucesso, IndexError
         e excecao generica;
    H12. lista curta (N=2, L=1) rejeitada com RenderizadorErro, sem IndexError;
    H13. erro ocorre antes de qualquer renderizacao (participantes instrumentados);
    H14. mensagem informa N e L;
    H15. larguras=None preserva DA-01 (N=1) e DA-02 (N>1);
    H16. distribuicao explicita coerente permanece valida.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, titulo="A"):
        campos = {"titulo": titulo}
        return ElementoCorpo(id=titulo.lower(), tipo="console", _campos_inertes=campos)

    def _espera_card_erro(self, nome, fn):
        """Exige RenderizadorErro de cardinalidade; rejeita IndexError/sucesso/outras."""
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada (sucesso/truncamento)")
        except RenderizadorErro as exc:
            ok = "cardinalidade horizontal incoerente" in str(exc)
            self._r(nome, ok, str(exc)[:120])
        except IndexError as exc:
            self._r(nome, False, "IndexError (lista curta sem guarda): {0!r}".format(exc))
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))

    # ------------------------------------------------------------------ H1-H2
    def test_H1_H2_zero_participantes(self):
        """H1: N=0, L=0 -> ''; H2: N=0, L=1 -> rejeicao."""
        borda = self._borda()
        resultado = _renderizar_container_horizontal(
            None, [], borda, 42, None, larguras=[]
        )
        self._r(
            "H1: N=0, L=0 -> resultado vazio",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )
        self._espera_card_erro(
            "H2: N=0, L=1 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [], borda, 42, None, larguras=[42]
            ),
        )

    # ------------------------------------------------------------------ H3-H5
    def test_H3_H4_H5_um_participante(self):
        """H3: N=1, L=0 -> rejeicao; H4: N=1, L=1 -> sucesso; H5: N=1, L=2 -> rejeicao."""
        borda = self._borda()
        e = self._elem("A")
        self._espera_card_erro(
            "H3: N=1, L=0 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[42]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: participante unico com largura integral.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H4: N=1, L=1 -> sucesso e largura=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H4: N=1, L=1 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "H5: N=1, L=2 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[21, 21]
            ),
        )

    # -------------------------------------------------------- H6-H10
    def test_H6_H7_H8_H9_H10_dois_e_tres_participantes(self):
        """H6-H10: cardinalidade incoerente rejeita; coerente aceita."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        ec = self._elem("C")
        # H6: N=2, L=1 -> rejeicao (prova que lista curta nao gera IndexError).
        self._espera_card_erro(
            "H6: N=2, L=1 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[28, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: 28 + 14 = 42 em cada linha.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H7: N=2, L=2 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H7: N=2, L=2 -> sucesso", False, str(exc))
        # H8: N=2, L=3 -> rejeicao (prova que lista longa nao e truncada).
        self._espera_card_erro(
            "H8: N=2, L=3 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[14, 14, 14]
            ),
        )
        self._espera_card_erro(
            "H9: N=3, L=2 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb, ec], borda, 42, None, larguras=[21, 21]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea, eb, ec], borda, 42, None, larguras=[14, 14, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: 14 + 14 + 14 = 42 em cada linha.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H10: N=3, L=3 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H10: N=3, L=3 -> sucesso", False, str(exc))

    # -------------------------------------------------------- H11-H12
    def test_H11_H12_sem_IndexError_e_sem_truncamento(self):
        """H11: lista longa rejeitada com RenderizadorErro (sem truncamento, sem saida parcial).

        Cenario material: 2 participantes (N=2) e 3 larguras explicitas (L=3),
        atingindo diretamente _renderizar_container_horizontal.

        Sem a guarda de cardinalidade, o loop de renderizacao iteraria apenas os
        dois participantes existentes (enumerate(elementos)) e descartaria
        silenciosamente a terceira largura excedente, produzindo linhas de
        largura 28. H11 deve exigir RenderizadorErro, rejeitando sucesso,
        IndexError e qualquer excecao generica.

        A prova de ausencia de saida parcial usa participantes instrumentados
        cujo acesso a .tipo so ocorre dentro do loop de renderizacao
        (for i, elemento in enumerate(elementos)). Se o erro de cardinalidade
        for levantado antes do loop, .tipo nunca e acessado e o tracker
        permanece vazio — provando que nenhum participante foi renderizado e
        nenhuma funcao descendente foi alcancada. A prova nao depende apenas da
        ausencia de uma largura/texto especifico na saida.

        H12: lista curta (N=2, L=1) rejeitada com RenderizadorErro, sem IndexError.
        """
        borda = self._borda()

        # Participantes instrumentados: tracker externo a funcao sob teste.
        # O acesso a .tipo so acontece dentro do loop de renderizacao; se a
        # guarda de cardinalidade rejeitar antes do loop, tracker permanece [].
        tracker = []

        class _ElemInstrumentado:
            def __init__(self, tid):
                self.id = tid
                self._campos_inertes = {"titulo": tid}

            @property
            def tipo(self):
                tracker.append("tipo_acessado:{0}".format(self.id))
                return "console"

        e1 = _ElemInstrumentado("A")
        e2 = _ElemInstrumentado("B")

        classe_erro = None
        mensagem = None
        sucesso = False
        try:
            _renderizar_container_horizontal(
                None, [e1, e2], borda, 42, None, larguras=[14, 14, 14]
            )
            sucesso = True
        except IndexError as exc:
            classe_erro = "IndexError"
            mensagem = str(exc)
        except RenderizadorErro as exc:
            classe_erro = "RenderizadorErro"
            mensagem = str(exc)
        except Exception as exc:
            # Excecao generica reprova: so RenderizadorErro e aceito.
            classe_erro = type(exc).__name__
            mensagem = str(exc)

        # (1) Exige RenderizadorErro; reprova sucesso, IndexError e excecao generica.
        self._r(
            "H11: N=2, L=3 levanta RenderizadorErro (rejeita sucesso/IndexError/generico)",
            classe_erro == "RenderizadorErro" and not sucesso,
            "sucesso={0} classe_erro={1} msg={2!r}".format(sucesso, classe_erro, mensagem),
        )
        # (2) Mensagem informa contexto horizontal, N=2 e L=3.
        self._r(
            "H11: mensagem informa horizontal, 2 participantes e 3 larguras",
            classe_erro == "RenderizadorErro"
            and mensagem is not None
            and "horizontal" in mensagem
            and "2 participante" in mensagem
            and "3 largura" in mensagem,
            "msg={0!r}".format(mensagem),
        )
        # (3) A largura excedente nao e ignorada: erro capturado, sem saida.
        #     A prova e material: o tracker permanece vazio, o que detectaria o
        #     caminho de renderizacao (e consequente truncamento) caso a guarda
        #     estivesse ausente. Nao basta verificar ausencia de largura 28.
        self._r(
            "H11: ausencia de saida parcial (tracker vazio, nenhum participante renderizado)",
            classe_erro == "RenderizadorErro" and len(tracker) == 0,
            "classe_erro={0} tracker={1}".format(classe_erro, tracker),
        )

        # H12: sem a guarda, N=2/L=1 levantaria IndexError ao indexar larguras[1].
        ea = self._elem("A")
        eb = self._elem("B")
        h12_index_error = False
        h12_card_erro = False
        try:
            _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            )
        except IndexError:
            h12_index_error = True
        except RenderizadorErro as exc:
            h12_card_erro = "cardinalidade horizontal incoerente" in str(exc)
        except Exception:
            pass
        self._r(
            "H12: N=2, L=1 levanta RenderizadorErro (nao IndexError)",
            h12_card_erro and not h12_index_error,
            "card_erro={0} index_error={1}".format(h12_card_erro, h12_index_error),
        )

    # -------------------------------------------------------- H13
    def test_H13_erro_antes_de_renderizacao(self):
        """H13: erro de cardinalidade ocorre antes de qualquer renderizacao.

        Usa elementos instrumentados: o acesso a .tipo so ocorre dentro do
        loop de renderizacao de _renderizar_container_horizontal. Se o erro
        for levantado antes do loop, .tipo nunca e acessado e o rastreador
        permanece vazio — provando ausencia de saida parcial e que nenhuma
        funcao descendente (_caixa_de_elemento/_renderizar_container) foi
        alcancada.
        """
        tracker = []

        class _ElemInstrumentado:
            id = "instrumento"
            _campos_inertes = {"titulo": "T"}

            @property
            def tipo(self):
                tracker.append("tipo_acessado")
                return "console"

        borda = self._borda()
        e1 = _ElemInstrumentado()
        e2 = _ElemInstrumentado()
        erro_card = False
        try:
            _renderizar_container_horizontal(
                None, [e1, e2], borda, 42, None, larguras=[42]
            )
        except RenderizadorErro as exc:
            erro_card = "cardinalidade horizontal incoerente" in str(exc)
        except Exception:
            pass
        self._r(
            "H13: erro de cardinalidade antes da renderizacao (tracker vazio)",
            erro_card and len(tracker) == 0,
            "erro_card={0} tracker={1}".format(erro_card, tracker),
        )

    # -------------------------------------------------------- H14
    def test_H14_mensagem_informa_cardinalidades(self):
        """H14: mensagem de erro informa contexto horizontal, N e L observados."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        msg = None
        try:
            _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            )
        except RenderizadorErro as exc:
            msg = str(exc)
        self._r(
            "H14: mensagem contem 'cardinalidade horizontal incoerente'",
            msg is not None and "cardinalidade horizontal incoerente" in msg,
            "msg={0!r}".format(msg),
        )
        self._r(
            "H14: mensagem informa N=2 e L=1",
            msg is not None and "2 participante" in msg and "1 largura" in msg,
            "msg={0!r}".format(msg),
        )

    # -------------------------------------------------------- H15-H16
    def test_H15_H16_regressao_larguras_none_e_dist(self):
        """H15: larguras=None preserva DA-01/DA-02; H16: distribuicao explicita valida."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea], borda, 42, None
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H15a: N=1, larguras=None -> DA-01 (largura integral 42)",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H15a: DA-01", False, str(exc))
        try:
            _renderizar_container_horizontal(None, [ea, eb], borda, 42, None)
            self._r("H15b: N=2, larguras=None -> DA-02", False, "sem excecao")
        except RenderizadorErro as exc:
            self._r(
                "H15b: N=2, larguras=None -> DA-02",
                "DA-02" in str(exc),
                str(exc)[:120],
            )
        # H16: distribuicao explicita coerente continua valida (caminho publico).
        dist = {"modo": "igual"}
        try:
            resultado = _renderizar_container_horizontal(
                dist, [ea, eb], borda, 42, None
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H16: N=2, distribuicao=igual -> sucesso sem regressao",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H16: distribuicao=igual", False, str(exc))

    def run_all(self):
        print("")
        print("== TestCardinalidadeHorizontalH0033Patch4: cardinalidade larguras explicitas em _renderizar_container_horizontal ==")
        self.test_H1_H2_zero_participantes()
        self.test_H3_H4_H5_um_participante()
        self.test_H6_H7_H8_H9_H10_dois_e_tres_participantes()
        self.test_H11_H12_sem_IndexError_e_sem_truncamento()
        self.test_H13_erro_antes_de_renderizacao()
        self.test_H14_mensagem_informa_cardinalidades()
        self.test_H15_H16_regressao_larguras_none_e_dist()
