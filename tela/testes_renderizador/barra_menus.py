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

from tela import renderizador as _rend_qa002



__all__ = [
    'test_h0044_chip_destacado_usa_cor_alerta',
    'test_h0044_chip_ativo_normal_sem_destaque',
    'test_h0044_chip_inativo_cinza_nao_amarelo',
    'test_h0044_destaque_nao_inativa',
    'test_h0044_largura_sem_ansi_destaque',
    'test_h0044_cor_nao_vaza_entre_chips',
    'test_h0044_executar_disponivel_ativa_selecao_nao_vazia',
    'test_h0044_regressao_sem_destaque_identica',
    'test_h0045_renderiza_apenas_fragmentos_da_pagina_atual_com_indicador',
    'test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo',
    'test_h0045_p02_barra_alinhada_na_sequencia_de_larguras',
    'TestLinhasBarra',
    'TestDistribuicaoH0018',
    'TestH0045P23BarraCincoLinhas',
    'TestH0045P23RegressaoDuasLinhas',
]


def _dist_canonica(preenchimento="coluna_a_coluna", **sobrepos):
    """Copia mutável do objeto canônico de distribuicao para testes H-0016."""
    d = {
        "modo": "horizontal_responsiva",
        "ordem": {"politica": "declaracao", "ancoras": {}},
        "tentativa_inicial": "linha_unica",
        "quebra": "multilinha_quando_nao_couber",
        "preenchimento_multilinha": preenchimento,
        "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
        "linhas": {"minimo": 1, "maximo": 2, "preferir_menor_numero": True},
        "alinhamento_linhas": "esquerda",
        "espacamentos": {
            "margem_horizontal": {"minimo": 1, "maximo": None},
            "vao_chip_texto": {"minimo": 1, "maximo": 3},
            "vao_entre_chips": {"minimo": 2, "maximo": 6},
            "vao_entre_colunas": {"minimo": 2, "maximo": 8},
            "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0},
        },
        "colunas": {
            "largura": "por_maior_item_da_coluna",
            "subcolunas": {
                "chip": {"alinhamento": "esquerda"},
                "texto": {"alinhamento": "esquerda"},
            },
        },
        "overflow": {
            "quando_nao_couber": "erro_layout",
            "nao_omitir_chips": True,
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        },
    }
    for chave, valor in sobrepos.items():
        d[chave] = valor
    return d


def _chip(cid, tecla, texto):
    """Chip minimal para testes de _linhas_barra."""
    return {"id": cid, "tecla": tecla, "texto": texto}


class TestLinhasBarra:
    """Casos H-0016: distribuicao horizontal responsiva da barra_de_menus.

    Cobertura obrigatoria do handoff H-0016: linha unica, multilinha,
    erro_layout, alias string, distribuicao ausente, chips vazia, ancoras
    (valida/violada/inexistente), ordem preservada, chips do lancador
    ausentes da barra, coluna_a_coluna, linha_a_linha, renderizar_tela com
    canonico, preservacao da altura H-0015, altura minima com barra
    horizontal, fluxo g/d/b/Esc, e validacoes defensivas (PR-M-01..04).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn):
        try:
            fn()
        except RenderizadorErro as exc:
            self._r(nome, True, "{0}: {1}".format(type(exc).__name__, exc))
            return exc
        except Exception as exc:  # pragma: no cover - diagnostico
            self._r(nome, False,
                    "esperava RenderizadorErro; obteve {0}: {1}".format(
                        type(exc).__name__, exc))
            return None
        self._r(nome, False, "esperava RenderizadorErro; nenhuma excecao")
        return None

    def test_linha_unica_cabe(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "linha unica: retorna lista com 1 string quando cabe (content_w=39)",
            isinstance(linhas, list) and len(linhas) == 1,
            "linhas={0!r}".format(linhas),
        )
        self._r(
            "linha unica contem ambos os chips",
            "[Esc] Sair" in linhas[0] and "[?] Ajuda" in linhas[0],
            "linha={0!r}".format(linhas[0] if linhas else None),
        )

    def test_linha_unica_nao_cabe_vai_para_multilinha(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        # single = 21 > 15; multilinha K=2 (1 coluna, 2 linhas) cabe (max 10).
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 15)
        self._r(
            "multilinha: content_w=15 -> 2 linhas",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )

    def test_multilinha_nao_cabe_erro_layout(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        exc = self._espera_erro(
            "erro_layout: content_w=5 nao cabe em nenhuma config",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 5),
        )
        if exc is not None:
            self._r(
                "mensagem de erro_layout contem 'erro_layout'",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_alias_string_horizontal_aceito(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": "horizontal", "chips": chips}
        try:
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
            ok = isinstance(linhas, list) and len(linhas) == 1
        except RenderizadorErro as exc:
            ok = False
            self._r("alias string 'horizontal' aceito sem erro", False, str(exc))
            return
        self._r("alias string 'horizontal' aceito sem erro", ok,
                "linhas={0!r}".format(linhas))

    def test_distribuicao_ausente_aceito(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"chips": chips}  # sem 'distribuicao'
        try:
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
            ok = isinstance(linhas, list) and len(linhas) >= 1
        except RenderizadorErro as exc:
            ok = False
            self._r("distribuicao ausente/None aceito sem erro", False, str(exc))
            return
        self._r("distribuicao ausente/None aceito sem erro", ok,
                "linhas={0!r}".format(linhas))

    def test_chips_vazia_retorna_lista_vazia(self):
        bar = {"distribuicao": _dist_canonica(), "chips": []}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "chips vazia retorna lista vazia",
            linhas == [],
            "linhas={0!r}".format(linhas),
        )

    def test_ancora_primeiro_valida(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_esc"]}
        bar = {"distribuicao": dist, "chips": chips}
        try:
            _linhas_barra(bar, _ESTILO_CURVA, 39)
            self._r("ancora primeiro valida: sem erro", True)
        except RenderizadorErro as exc:
            self._r("ancora primeiro valida: sem erro", False, str(exc))

    def test_ancora_primeiro_violada(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_ajuda"]}  # nao eh o 1o
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora primeiro violada -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ancora_ultimo_valida(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"ultimo": ["chip_ajuda"]}
        bar = {"distribuicao": dist, "chips": chips}
        try:
            _linhas_barra(bar, _ESTILO_CURVA, 39)
            self._r("ancora ultimo valida: sem erro", True)
        except RenderizadorErro as exc:
            self._r("ancora ultimo valida: sem erro", False, str(exc))

    def test_ancora_ultimo_violada(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"ultimo": ["chip_esc"]}  # nao eh o ultimo
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora ultimo violada -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ancora_id_inexistente(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_inexistente"]}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora com id inexistente -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ordem_preservada(self):
        chips = [
            _chip("a", "1", "AAA"),
            _chip("b", "2", "BBB"),
            _chip("c", "3", "CCC"),
        ]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 100)
        saida = " ".join(linhas)
        self._r(
            "ordem preservada na saida (a antes de b antes de c)",
            saida.find("[1] AAA") < saida.find("[2] BBB")
            and saida.find("[2] BBB") < saida.find("[3] CCC"),
            "saida={0!r}".format(saida),
        )

    def test_chips_declarados_aparecem_exatamente_uma_vez(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        junta = " ".join(linhas)
        self._r(
            "cada chip declarado aparece exatamente uma vez",
            junta.count("[Esc] Sair") == 1 and junta.count("[?] Ajuda") == 1,
            "junta={0!r}".format(junta),
        )

    def test_chips_do_lancador_nao_entram_na_barra(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 39)
        junta = " ".join(linhas)
        self._r(
            "barra contem chips da barra ([Esc], [?])",
            "[Esc]" in junta and "[?]" in junta,
            "junta={0!r}".format(junta),
        )
        self._r(
            "barra NAO contem chips do lancador ([d], [g])",
            "[d]" not in junta and "[g]" not in junta,
            "junta={0!r}".format(junta),
        )
        # corpo.arranjo nao influencia a barra: o lancador continua no corpo.
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "lancador ([d]/[g]) permanece no corpo, nao na barra",
            "[d] Destino" in saida and "[g] Grupo Min." in saida,
        )

    def test_coluna_a_coluna_layout(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        # Forca multilinha K=2: single = 5*5 + 2*4 = 33 > 23 (largura_util com margem=1).
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["linhas"] = {"minimo": 1, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 25)
        self._r(
            "coluna_a_coluna K=2 -> 2 linhas (content_w=25)",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )
        if isinstance(linhas, list) and len(linhas) == 2:
            # Preenchimento coluna-a-coluna: line0 tem A,C,E; line1 tem B,D.
            self._r(
                "coluna_a_coluna: linha 0 contem A, C, E (coluna-major)",
                "[1] A" in linhas[0] and "[3] C" in linhas[0]
                and "[5] E" in linhas[0],
                "linha0={0!r}".format(linhas[0]),
            )
            self._r(
                "coluna_a_coluna: linha 1 contem B, D (coluna-major)",
                "[2] B" in linhas[1] and "[4] D" in linhas[1],
                "linha1={0!r}".format(linhas[1]),
            )
            self._r(
                "coluna_a_coluna: linha 1 NAO contem A, C, E",
                "[1] A" not in linhas[1] and "[3] C" not in linhas[1]
                and "[5] E" not in linhas[1],
            )

    def test_linha_a_linha_implementado(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        dist = _dist_canonica(preenchimento="linha_a_linha")
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 25)
        self._r(
            "linha_a_linha K=2 -> 2 linhas (content_w=25)",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )
        if isinstance(linhas, list) and len(linhas) == 2:
            # Preenchimento linha-a-linha: line0=A,B,C; line1=D,E.
            self._r(
                "linha_a_linha: linha 0 contem A, B, C (linha-major)",
                "[1] A" in linhas[0] and "[2] B" in linhas[0]
                and "[3] C" in linhas[0],
                "linha0={0!r}".format(linhas[0]),
            )
            self._r(
                "linha_a_linha: linha 1 contem D, E (linha-major)",
                "[4] D" in linhas[1] and "[5] E" in linhas[1],
                "linha1={0!r}".format(linhas[1]),
            )

    def test_modo_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["modo"] = "vertical"
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "modo desconhecido ('vertical') -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_politica_desconhecida_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["ordem"] = {"politica": "grupos_declarados", "ancoras": {}}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ordem.politica nao suportada ('grupos_declarados') -> "
            "RenderizadorErro (PR-M-01)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_preenchimento_multilinha_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("x", "?", "Aj")]
        dist = _dist_canonica(preenchimento="outro_modo")
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "preenchimento_multilinha desconhecido -> RenderizadorErro (PR-M-02)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 15),
        )

    def test_linhas_minimo_invalido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 0, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.minimo invalido (0) -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_linhas_maximo_menor_que_minimo_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 3, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.maximo < minimo -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_overflow_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("x", "?", "Aj")]
        dist = _dist_canonica()
        dist["overflow"] = {
            "quando_nao_couber": "omitir",
            "nao_omitir_chips": True,
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        }
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "overflow.quando_nao_couber desconhecido -> RenderizadorErro (PR-M-04)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_overflow_flag_nao_booleana_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["overflow"] = {
            "quando_nao_couber": "erro_layout",
            "nao_omitir_chips": "sim",
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        }
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "overflow flag nao booleana -> RenderizadorErro (PR-M-04)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_renderizar_tela_com_distribuicao_canonica(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        dist = modelo.barra_de_menus.get("distribuicao")
        self._r(
            "JSON migrado expoe distribuicao como objeto com modo canonico",
            isinstance(dist, dict)
            and dist.get("modo") == "horizontal_responsiva"
            and dist.get("ordem", {}).get("politica") == "declaracao",
            "modo={0!r}".format(dist.get("modo") if isinstance(dist, dict) else None),
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "renderizar_tela com canonico: barra em linha horizontal",
            saida == _EXPECTED_ORQUESTRADOR,
            "" if saida == _EXPECTED_ORQUESTRADOR else "snapshot diverge",
        )

    def test_renderizar_tela_preserva_altura_h0015(self):
        # ADR-0024 DA-02: modelo sem distribuicao com 3 visuais + area residual
        # levanta RenderizadorErro (fill externo proibido).
        modelo = _modelo_orquestrador_sem_distribuicao()
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 39)
        l_barra = len(linhas) + 2
        self._r(
            "altura explicita: L_barra = len(linhas_barra)+2 = 3 (1 linha horizontal)",
            l_barra == 3 and len(linhas) == 1,
            "l_barra={0} linhas={1}".format(l_barra, len(linhas)),
        )
        excecao_da02 = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "ADR-0024 DA-02: sem dist + 3 visuais + altura=24 -> RenderizadorErro",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    def test_altura_minima_com_barra_horizontal(self):
        # H-0025: modelo sem distribuicao preserva o comportamento H-0015
        # (preenchimento externo) em altura minima. A tela demo agora
        # declara distribuicao; a cobertura de distribuicao vertical esta em
        # TestDistribuicaoVerticalH0025.
        modelo = _modelo_orquestrador_sem_distribuicao()
        # H-0016 / H-0037 / H-0034: com 11 itens no lancador em matriz 6x2 com
        # margens verticais, NAVEGAR tem 10 linhas, n_minimo = L_cab(3) +
        # L_corpo(15) + L_barra(3) = 21.
        saida_21 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=21)
        self._r(
            "altura minima = 21 com barra horizontal (sem distribuicao)",
            saida_21.count("\n") == 21
            and saida_21 == renderizar_tela(modelo, _ESTILO_CURVA, largura=42),
            "count={0}".format(saida_21.count("\n")),
        )

    def test_fluxo_g_d_b_esc_preservado(self):
        # O renderer continua exibindo lancador ([d]/[g]) no corpo e os chips
        # da barra ([Esc]/[?]) no rodape; a navegacao g/d/b/Esc (tratada pela
        # demo) depende desses chips continuarem presentes e corretos.
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "fluxo g/d/b/Esc: lancador [d]/[g] e barra [Esc]/[?] presentes",
            "[d] Destino" in saida and "[g] Grupo Min." in saida
            and "[Esc] Sair" in saida and "[?] Ajuda" in saida,
        )

    def run_all(self):
        print("")
        print("== H-0016 - distribuicao horizontal responsiva da barra_de_menus ==")
        self.test_linha_unica_cabe()
        self.test_linha_unica_nao_cabe_vai_para_multilinha()
        self.test_multilinha_nao_cabe_erro_layout()
        self.test_alias_string_horizontal_aceito()
        self.test_distribuicao_ausente_aceito()
        self.test_chips_vazia_retorna_lista_vazia()
        self.test_ancora_primeiro_valida()
        self.test_ancora_primeiro_violada()
        self.test_ancora_ultimo_valida()
        self.test_ancora_ultimo_violada()
        self.test_ancora_id_inexistente()
        self.test_ordem_preservada()
        self.test_chips_declarados_aparecem_exatamente_uma_vez()
        self.test_chips_do_lancador_nao_entram_na_barra()
        self.test_coluna_a_coluna_layout()
        self.test_linha_a_linha_implementado()
        self.test_modo_desconhecido_erro()
        self.test_politica_desconhecida_erro()
        self.test_preenchimento_multilinha_desconhecido_erro()
        self.test_linhas_minimo_invalido_erro()
        self.test_linhas_maximo_menor_que_minimo_erro()
        self.test_overflow_desconhecido_erro()
        self.test_overflow_flag_nao_booleana_erro()
        self.test_renderizar_tela_com_distribuicao_canonica()
        self.test_renderizar_tela_preserva_altura_h0015()
        self.test_altura_minima_com_barra_horizontal()
        self.test_fluxo_g_d_b_esc_preservado()


class TestDistribuicaoH0018:
    """Cobertura executavel de todos os campos de distribuicao (H-0018).

    28 testes que garantem que nenhum campo de barra_de_menus.distribuicao
    e ignorado silenciosamente: cada campo tem efeito observavel, e validado
    ou rejeitado de forma deterministica.
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

    # ------------------------------------------------------------------ 1-3
    def test_vao_chip_texto_altera_distancia(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 3
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "vao_chip_texto=3: chip contem 3 espacos entre ] e texto",
            isinstance(linhas, list) and any("[Esc]   Sair" in l for l in linhas),
            "linhas={0!r}".format(linhas),
        )

    def test_vao_chip_texto_10_espaco_extra(self):
        chips = [_chip("c_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 10
        dist["espacamentos"]["vao_chip_texto"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "vao_chip_texto=10: chip contem 10 espacos entre ] e texto",
            isinstance(linhas, list) and any("[Esc]          Sair" in l for l in linhas),
            "linhas={0!r}".format(linhas),
        )

    def test_vao_chip_texto_altera_comprimento_linha(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        d1 = _dist_canonica()
        d1["espacamentos"]["vao_chip_texto"]["minimo"] = 1
        d5 = _dist_canonica()
        d5["espacamentos"]["vao_chip_texto"]["minimo"] = 5
        d5["espacamentos"]["vao_chip_texto"]["maximo"] = None
        l1 = _linhas_barra({"distribuicao": d1, "chips": chips}, _ESTILO_CURVA, 80)
        l5 = _linhas_barra({"distribuicao": d5, "chips": chips}, _ESTILO_CURVA, 80)
        self._r(
            "vao_chip_texto=5 produz linha mais longa que vao=1",
            isinstance(l1, list) and isinstance(l5, list)
            and l5 and l1 and len(l5[0]) > len(l1[0]),
            "vao1={0!r} vao5={1!r}".format(l1, l5),
        )

    # ------------------------------------------------------------------ 4-6
    def test_margem_horizontal_altera_padding(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 4
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "margem_horizontal=4: linha comeca com 4 espacos",
            isinstance(linhas, list) and linhas and linhas[0].startswith("    "),
            "linhas={0!r}".format(linhas),
        )

    def test_margem_horizontal_participa_do_overflow(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 50
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "margem_horizontal=50 com content_w=39 -> RenderizadorErro (largura_util negativa)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_margem_horizontal_0_permitido(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 0
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "margem_horizontal=0: linha comeca diretamente com [",
            isinstance(linhas, list) and linhas and linhas[0].startswith("["),
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 7-8
    def test_vao_entre_chips_altera_distancia(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 6
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 80)
        self._r(
            "vao_entre_chips=6: linha contem 6 espacos entre chips",
            isinstance(linhas, list) and linhas
            and "[Esc] Sair      [?] Ajuda" in linhas[0],
            "linhas={0!r}".format(linhas),
        )

    def test_vao_entre_colunas_altera_distancia_multilinha(self):
        chips = [
            _chip("c1", "1", "AAAAA"),
            _chip("c2", "2", "BBBBB"),
            _chip("c3", "3", "CCCCC"),
            _chip("c4", "4", "DDDDD"),
        ]
        d2 = _dist_canonica(preenchimento="coluna_a_coluna")
        d2["espacamentos"]["vao_entre_colunas"]["minimo"] = 2
        d8 = _dist_canonica(preenchimento="coluna_a_coluna")
        d8["espacamentos"]["vao_entre_colunas"]["minimo"] = 8
        l2 = _linhas_barra({"distribuicao": d2, "chips": chips}, _ESTILO_CURVA, 40)
        l8 = _linhas_barra({"distribuicao": d8, "chips": chips}, _ESTILO_CURVA, 40)
        self._r(
            "vao_entre_colunas=8 produz linha mais larga que vao=2 na multilinha",
            isinstance(l2, list) and isinstance(l8, list)
            and l2 and l8 and len(l8[0]) > len(l2[0]),
            "vao2={0!r} vao8={1!r}".format(l2[0] if l2 else None, l8[0] if l8 else None),
        )

    # ------------------------------------------------------------------ 9-11
    def test_vao_vertical_entre_linhas_rejeitado(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_vertical_entre_linhas"] = {"minimo": 1, "maximo": 1}
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_vertical_entre_linhas.minimo=1 -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_vertical_entre_linhas nao suportado",
                "vao_vertical_entre_linhas" in str(exc),
                str(exc),
            )

    def test_alinhamento_linhas_esquerda_funciona(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["alinhamento_linhas"] = "esquerda"
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "alinhamento_linhas='esquerda': aceito sem erro",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def test_alinhamento_linhas_nao_suportado_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["alinhamento_linhas"] = "centro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "alinhamento_linhas='centro' -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona alinhamento_linhas nao suportado",
                "alinhamento_linhas" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 12-15
    def test_linhas_minimo_maior_que_1_pula_linha_unica(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 2, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "linhas.minimo=2: chips que caberiam em 1 linha -> forcado 2 linhas",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )

    def test_linhas_maximo_1_overflow_se_nao_couber(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 1, "maximo": 1, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "linhas.maximo=1 com chips que nao cabem em linha unica -> erro_layout",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 10),
        )
        if exc is not None:
            self._r(
                "mensagem menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_linhas_maximo_1_ok_se_couber(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 1, "maximo": 1, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "linhas.maximo=1 com chips que cabem -> 1 linha sem erro",
            isinstance(linhas, list) and len(linhas) == 1,
            "linhas={0!r}".format(linhas),
        )

    def test_linhas_maximo_3_tres_linhas(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["linhas"] = {"minimo": 1, "maximo": 3, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        # K=2 nao cabe (19 > largura_util=18); K=3 cabe (12 <= 18)
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 20)
        self._r(
            "linhas.maximo=3: 5 chips que nao cabem em K=2 -> K=3 (3 linhas)",
            isinstance(linhas, list) and len(linhas) == 3,
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 16-17
    def test_preferir_menor_numero_false_rejeitado(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"]["preferir_menor_numero"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preferir_menor_numero=false -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preferir_menor_numero nao suportado",
                "preferir_menor_numero" in str(exc),
                str(exc),
            )

    def test_preferir_menor_numero_nao_bool_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"]["preferir_menor_numero"] = "sim"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preferir_menor_numero='sim' (nao bool) -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preferir_menor_numero deve ser bool",
                "preferir_menor_numero" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 18-19
    def test_colunas_largura_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["largura"] = "por_percentual"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "colunas.largura='por_percentual' -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona colunas.largura nao suportado",
                "colunas.largura" in str(exc),
                str(exc),
            )

    def test_colunas_largura_ausente_usa_default(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        del dist["colunas"]["largura"]
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "colunas.largura ausente: aceito sem erro (usa default)",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 20-21
    def test_subcoluna_chip_alinhamento_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["subcolunas"]["chip"]["alinhamento"] = "centro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "subcolunas.chip.alinhamento='centro' -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona subcolunas.chip.alinhamento nao suportado",
                "subcolunas.chip.alinhamento" in str(exc),
                str(exc),
            )

    def test_subcoluna_texto_alinhamento_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["subcolunas"]["texto"]["alinhamento"] = "direita"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "subcolunas.texto.alinhamento='direita' -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona subcolunas.texto.alinhamento nao suportado",
                "subcolunas.texto.alinhamento" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 22-24
    def test_overflow_nao_omitir_chips_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_omitir_chips"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_omitir_chips=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_omitir_chips deve ser true",
                "nao_omitir_chips" in str(exc),
                str(exc),
            )

    def test_overflow_nao_truncar_texto_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_truncar_texto"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_truncar_texto=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_truncar_texto deve ser true",
                "nao_truncar_texto" in str(exc),
                str(exc),
            )

    def test_overflow_nao_reordenar_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_reordenar"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_reordenar=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_reordenar deve ser true",
                "nao_reordenar" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 25
    def test_preenchimentos_multilinha_suportados_valida_preenchimento(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["preenchimentos_multilinha_suportados"] = ["linha_a_linha"]
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preenchimento='coluna_a_coluna' ausente em suportados -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preenchimento nao esta em suportados",
                "preenchimentos_multilinha_suportados" in str(exc)
                or "preenchimento_multilinha" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 26-28
    def test_valores_exagerados_margem_50(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 50
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "margem=50 com content_w=39 -> erro_layout (largura_util=-61)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "erro com margem exagerada menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_valores_exagerados_vao_chip_texto_10(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 10
        dist["espacamentos"]["vao_chip_texto"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        # single=19+2+18=39>37 (largura_util) -> multilinha K=2: max=19<=37 -> 2 linhas
        try:
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
            self._r(
                "vao_chip_texto=10: resultado deterministico (multilinha, nao silencio)",
                isinstance(linhas, list) and len(linhas) >= 1,
                "linhas={0!r}".format(linhas),
            )
            self._r(
                "vao_chip_texto=10: chip contem 10 espacos entre ] e texto",
                any("[Esc]          Sair" in l for l in linhas),
                "linhas={0!r}".format(linhas),
            )
        except RenderizadorErro as exc:
            self._r(
                "vao_chip_texto=10: RenderizadorErro deterministico (nao silencio)",
                True,
                str(exc),
            )

    def test_valores_exagerados_vao_entre_chips_20(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 20
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        # single=10+20+9=39>18 (largura_util com content_w=20) -> multilinha K=2: max=10<=18 -> 2l
        try:
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 20)
            self._r(
                "vao_entre_chips=20: resultado deterministico (multilinha, nao silencio)",
                isinstance(linhas, list) and len(linhas) >= 1,
                "linhas={0!r}".format(linhas),
            )
        except RenderizadorErro as exc:
            self._r(
                "vao_entre_chips=20: erro_layout deterministico (nao silencio)",
                "erro_layout" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 29-35
    def test_vao_entre_chips_maximo_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 4
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = 2
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_chips.maximo < minimo -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_chips.maximo invalido",
                "vao_entre_chips.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_colunas_maximo_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_colunas"]["minimo"] = 4
        dist["espacamentos"]["vao_entre_colunas"]["maximo"] = 2
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_colunas.maximo < minimo -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_colunas.maximo invalido",
                "vao_entre_colunas.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_chips_maximo_nao_int_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = "seis"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_chips.maximo nao-int -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_chips.maximo invalido",
                "vao_entre_chips.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_colunas_maximo_null_aceito(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_colunas"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "vao_entre_colunas.maximo=None: aceito sem erro",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def test_tentativa_inicial_invalida_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["tentativa_inicial"] = "multilinha_primeiro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "tentativa_inicial='multilinha_primeiro' -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona tentativa_inicial nao suportado",
                "tentativa_inicial" in str(exc),
                str(exc),
            )

    def test_quebra_invalida_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["quebra"] = "truncar"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "quebra='truncar' -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona quebra nao suportado",
                "quebra" in str(exc),
                str(exc),
            )

    def test_tentativa_inicial_e_quebra_validos_aceitos(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["tentativa_inicial"] = "linha_unica"
        dist["quebra"] = "multilinha_quando_nao_couber"
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        self._r(
            "tentativa_inicial='linha_unica' e quebra='multilinha_quando_nao_couber': aceitos",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def run_all(self):
        print("")
        print("== H-0018 - cobertura executavel de todos os campos de distribuicao ==")
        self.test_vao_chip_texto_altera_distancia()
        self.test_vao_chip_texto_10_espaco_extra()
        self.test_vao_chip_texto_altera_comprimento_linha()
        self.test_margem_horizontal_altera_padding()
        self.test_margem_horizontal_participa_do_overflow()
        self.test_margem_horizontal_0_permitido()
        self.test_vao_entre_chips_altera_distancia()
        self.test_vao_entre_colunas_altera_distancia_multilinha()
        self.test_vao_vertical_entre_linhas_rejeitado()
        self.test_alinhamento_linhas_esquerda_funciona()
        self.test_alinhamento_linhas_nao_suportado_erro()
        self.test_linhas_minimo_maior_que_1_pula_linha_unica()
        self.test_linhas_maximo_1_overflow_se_nao_couber()
        self.test_linhas_maximo_1_ok_se_couber()
        self.test_linhas_maximo_3_tres_linhas()
        self.test_preferir_menor_numero_false_rejeitado()
        self.test_preferir_menor_numero_nao_bool_erro()
        self.test_colunas_largura_invalido_erro()
        self.test_colunas_largura_ausente_usa_default()
        self.test_subcoluna_chip_alinhamento_invalido_erro()
        self.test_subcoluna_texto_alinhamento_invalido_erro()
        self.test_overflow_nao_omitir_chips_false_erro()
        self.test_overflow_nao_truncar_texto_false_erro()
        self.test_overflow_nao_reordenar_false_erro()
        self.test_preenchimentos_multilinha_suportados_valida_preenchimento()
        self.test_valores_exagerados_margem_50()
        self.test_valores_exagerados_vao_chip_texto_10()
        self.test_valores_exagerados_vao_entre_chips_20()
        self.test_vao_entre_chips_maximo_invalido_erro()
        self.test_vao_entre_colunas_maximo_invalido_erro()
        self.test_vao_entre_chips_maximo_nao_int_erro()
        self.test_vao_entre_colunas_maximo_null_aceito()
        self.test_tentativa_inicial_invalida_erro()
        self.test_quebra_invalida_erro()
        self.test_tentativa_inicial_e_quebra_validos_aceitos()


class TestH0045P23BarraCincoLinhas:
    """VM-H0045-R08-001: distribuicao canônica com linhas.maximo=5 da barra."""

    def test_config_declarou_objeto_canonico_com_maximo_cinco(self):
        """Caso 1: a configuracao materializou o objeto canônico (nao alias)."""
        modelo = _modelo_fluxo_paginado_p23()
        dist = modelo.barra_de_menus["distribuicao"]
        assert isinstance(dist, dict)
        assert dist["linhas"]["minimo"] == 1
        assert dist["linhas"]["maximo"] == 5
        assert dist["preenchimento_multilinha"] == "coluna_a_coluna"
        assert dist["overflow"]["quando_nao_couber"] == "erro_layout"
        # Preservacoes exigidas pelo patch.
        assert dist["espacamentos"]["margem_horizontal"]["minimo"] == 1
        assert dist["overflow"]["nao_omitir_chips"] is True
        assert dist["overflow"]["nao_truncar_texto"] is True
        assert dist["overflow"]["nao_reordenar"] is True

    def test_barra_escolhe_menor_quantidade_valida(self):
        """Caso 7: a barra escolhe automaticamente a menor qtd valida."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # Em largura folgada, uma linha basta; nunca usa mais que o necessario.
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 120 - 3)
        assert len(linhas) == 1

    def test_barra_usa_uma_linha_em_largura_suficiente(self):
        """Caso 2: uma linha quando couber (~65 colunas)."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 65 - 3)
        assert len(linhas) == 1

    def test_barra_usa_duas_linhas_em_41_colunas(self):
        """Caso 3: duas linhas em ~41 colunas."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 41 - 3)
        assert len(linhas) == 2

    def test_barra_usa_tres_linhas_em_36_colunas(self):
        """Caso 4: tres linhas em ~36 colunas.

        H-0051: o agrupamento visual indivisivel ``[PgUp][PgDn] Páginas``
        reduz a largura total dos chips; a largura que produz exatamente
        tres linhas desloca de ~29 para ~36 colunas (recalibrado, sem
        alterar o mecanismo de distribuicao).
        """
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 36 - 3)
        assert len(linhas) == 3

    def test_barra_usa_quatro_linhas_em_28_colunas(self):
        """Caso 5: quatro linhas conforme distribuicao real (~28 colunas)."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 28 - 3)
        assert len(linhas) == 4

    def test_barra_grupo_paginacao_reduz_arranjo_maximo_pratico_para_quatro(self):
        """H-0051: nenhuma largura chega a exigir a quinta linha.

        ``chip_pagina_anterior``/``chip_pagina_proxima`` viram um grupo
        visual indivisivel (``[PgUp][PgDn] Páginas``), reduzindo de 5 para
        4 os grupos independentes da barra desta fixture. O teto declarado
        (``linhas.maximo == 5``) permanece intacto no JSON (teste
        ``test_config_declarou_objeto_canonico_com_maximo_cinco``), mas a
        menor largura que ainda comporta os chips ja usa 4 linhas (uma por
        grupo); abaixo dela, o layout falha diretamente com
        ``erro_layout``, sem nunca passar por um arranjo de 5 linhas.
        """
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 25 - 3)
        assert len(linhas) == 4
        import pytest as _pytest_p23b
        with _pytest_p23b.raises(RenderizadorErro):
            _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 24 - 3)

    def test_barra_nao_excede_cinco_linhas(self):
        """O maximo declarado (5) e respeitado em larguras intermediarias."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        for w in (40, 36, 35, 30, 25):
            linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, w - 3)
            assert 1 <= len(linhas) <= 5

    def test_barra_erro_layout_em_largura_insuficiente_abaixo_do_limite(self):
        """Caso 8: largura insuficiente mesmo com cinco linhas -> erro_layout."""
        import pytest as _pytest_p23
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # 16 colunas: nenhum arranjo de 5 linhas comporta os chips no content_w.
        with _pytest_p23.raises(RenderizadorErro) as ei:
            _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 16 - 3)
        assert "erro_layout" in str(ei.value)

    def test_barra_preserva_ordem_e_chips_em_multilinha(self):
        """Casos 23/24: ausencia de truncamento/reordenacao em multilinha."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # Em 28 colunas (4 linhas), todos os chips aparecem, na ordem declarada.
        import re
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 28 - 3)
        joined = re.sub(r"\x1b\[[0-9;]*m", "", " ".join(linhas))
        # [Esc] e sempre primeiro (regra contratual); os demais seguem a ordem.
        assert "[Esc]" in joined
        assert "[PgUp][PgDn] Páginas" in joined
        assert "[␣]" in joined
        assert "[⏎]" in joined
        # Esc precede os demais chips de paginacao (contrato §8.2).
        assert joined.index("[Esc]") < joined.index("[PgUp]")


class TestH0045P23RegressaoDuasLinhas:
    """Caso 29: telas que NAO declaram maximo continuam com teto de 2 linhas."""

    def test_tela_padrao_continua_com_maximo_global_duas_linhas(self):
        """A configuracao P23 nao altera o default global de duas linhas."""
        # h0045_paginacao_console_unico usa alias "horizontal" (default max=2).
        tela_raw = carregar_tela(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = construir_modelo(tela_raw)
        _preparar_ctx_p23(modelo)
        # Em largura que cabe em 2, exatamente <=2 linhas (nao 3, 4 ou 5).
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 45 - 3)
        assert len(linhas) <= 2


def test_h0044_chip_destacado_usa_cor_alerta():
    chip = {"id": "chip_x", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=False, destacado=True
    )
    codigo = _rend_qa002._codigo_ansi_de_cor(_ESTILO_H0044.cor_alerta)
    assert codigo == "\x1b[33m"
    assert codigo in texto
    assert texto.endswith(_rend_qa002._ANSI_RESET_FG)
    assert "Dry-Run" in texto


def test_h0044_chip_ativo_normal_sem_destaque():
    chip = {"id": "chip_x", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=False, destacado=False
    )
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") not in texto


def test_h0044_chip_inativo_cinza_nao_amarelo():
    chip = {"id": "chip_e", "tecla": "⏎", "texto": "Executar"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=True, destacado=True
    )
    # Inativo tem precedencia; destaque nao se aplica.
    assert _rend_qa002._codigo_ansi_de_cor("cinza") in texto
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in texto


def test_h0044_destaque_nao_inativa():
    assert _rend_qa002._avaliar_regra_ativo("sempre") is True
    chip = {"id": "chip_dry_run", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, destacado=True, inativo=False
    )
    assert "Dry-Run" in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") not in texto


def test_h0044_largura_sem_ansi_destaque():
    chip = {"tecla": "Ins", "texto": "Dry-Run"}
    base = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=False)
    dest = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=True)
    assert _rend_qa002._largura_sem_ansi(base) == _rend_qa002._largura_sem_ansi(dest)


def test_h0044_cor_nao_vaza_entre_chips():
    chips = [
        {"id": "a", "tecla": "Ins", "texto": "Dry-Run"},
        {"id": "b", "tecla": "Esc", "texto": "Sair"},
    ]
    t0 = _rend_qa002._texto_chip_barra(
        chips[0], _ESTILO_H0044, destacado=True
    )
    t1 = _rend_qa002._texto_chip_barra(
        chips[1], _ESTILO_H0044, destacado=False
    )
    assert t0.endswith(_rend_qa002._ANSI_RESET_FG)
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in t1


def test_h0044_executar_disponivel_ativa_selecao_nao_vazia():
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False, executar_disponivel=True
    ) is True
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False, executar_disponivel=False
    ) is False
    # Sem contexto H-0044: preserva H-0041 (Executar inativo).
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


def test_h0044_regressao_sem_destaque_identica():
    chip = {"tecla": "Esc", "texto": "Sair"}
    a = _rend_qa002._texto_chip_barra(chip, _ESTILO_CURVA)
    b = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=False)
    assert a == b


def test_h0045_renderiza_apenas_fragmentos_da_pagina_atual_com_indicador():
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    saida = renderizar_tela(
        modelo,
        carregar_estilo(),
        largura=80,
        altura=24,
        foco_console=0,
        cursores={console.id: 16},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={console.id: 2},
    )

    assert "página 2/3" in saida
    assert "item_17" in saida
    assert "item_01" not in saida


def test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo():
    """VM-H0045-01: na pagina 1, ``[PgUp]`` visivel/inativo e ``[PgDn]`` ativo."""
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela import renderizador as _rend
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    saida = renderizar_tela(
        modelo,
        carregar_estilo(),
        largura=80,
        altura=24,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={console.id: 1},
    )

    import re
    saida_sem_ansi = re.sub(r"\x1b\[[0-9;]*m", "", saida)
    assert "página 1/3" in saida
    assert "[PgUp][PgDn] Páginas" in saida_sem_ansi
    assert "\x1b[90m[PgUp]" in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is True


def _h0045_linha_barra_menus(saida):
    """Retorna a linha de conteudo da barra (chips) e a versao sem ANSI."""
    import re
    from tela.renderizador import _largura_sem_ansi

    linhas = saida.split("\n")
    if linhas and linhas[-1] == "":
        linhas = linhas[:-1]
    candidatas = [
        ln for ln in linhas
        if "[Esc]" in re.sub(r"\x1b\[[0-9;]*m", "", ln)
        and "[PgUp][PgDn] Páginas" in re.sub(r"\x1b\[[0-9;]*m", "", ln)
    ]
    assert candidatas, "linha da barra com chips nao encontrada"
    linha = candidatas[0]
    plain = re.sub(r"\x1b\[[0-9;]*m", "", linha)
    return linha, plain, _largura_sem_ansi(linha)


def test_h0045_p02_barra_alinhada_na_sequencia_de_larguras():
    """VM-H0045-R02-002: sequencia grande → reduzida → maximizada.

    Verifica alinhamento das bordas, largura visual exata, uma unica
    borda esquerda/direita, ausencia de ``│`` repetidos e manutencao
    dos quatro chips + indicador sem regressao.
    """
    import re
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    lista = navegacao.lista_foco(modelo)
    estilo = carregar_estilo()
    sequencia = (100, 60, 100)

    for largura in sequencia:
        saida = renderizar_tela(
            modelo,
            estilo,
            largura=largura,
            altura=24,
            foco_console=0,
            cursores={console.id: 0},
            lista_foco=lista,
            paginas_atuais={console.id: 1},
            largura_navegacao=largura,
        )
        linha, plain, vis = _h0045_linha_barra_menus(saida)
        assert vis == largura, (
            "largura visual da barra {0} != {1}".format(vis, largura)
        )
        assert plain.startswith("│"), "borda esquerda ausente/deslocada"
        assert plain.endswith("│"), "borda direita ausente/deslocada"
        assert plain.count("│") == 2, (
            "esperado exatamente 2 bordas verticais, obtido {0}: {1!r}".format(
                plain.count("│"), plain
            )
        )
        assert "││" not in plain, "sequencia artificial de │ presente"
        assert "[Esc]" in plain
        assert "[PgUp][PgDn] Páginas" in plain
        assert "[✥]" in plain
        assert "página 1/3" in saida
        # Nenhuma linha do quadro deve ser visualmente mais curta que largura
        # quando contem ANSI de chip inativo (residuo potencial a direita).
        for ln in saida.split("\n"):
            if not ln:
                continue
            from tela.renderizador import _largura_sem_ansi
            assert _largura_sem_ansi(ln) == largura

    # Pagina 1: [PgUp] inativo permanece (cor_inativo), sem regressao P01.
    saida_final = renderizar_tela(
        modelo,
        estilo,
        largura=100,
        altura=24,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=lista,
        paginas_atuais={console.id: 1},
        largura_navegacao=100,
    )
    assert "\x1b[90m[PgUp]" in saida_final


def _modelo_fluxo_paginado_p23():
    """Carrega ``h0045_fluxo_execucao_paginado`` (barra com linhas.maximo=5)."""
    tela_raw = carregar_tela(None, "h0045_fluxo_execucao_paginado", _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw)


def _preparar_ctx_p23(modelo):
    """Prepara o contexto de navegacao para ``_linhas_barra`` (P23).

    Os chips ``[PgUp]``/``[PgDn]`` da fixture usam ``regra_existencia:
    console_com_paginacao`` e os chips ``[␣]``/``[⏎]`` usam
    ``console_focado_com_selecao_multipla`` -- ambos avaliados a partir do
    contexto de modulo ``_navegacao_atual``. Sem preparar o contexto (como
    ``renderizar_tela`` faz internamente), o estado de modulo persiste entre
    testes e filtra chips indevidamente. Esta funcao reproduz o setup minimo
    para que ``_linhas_barra`` veja os 5 chips declarados: o console focalizavel
    na lista de foco e focalizado, declarando selecao multipla e paginacao.
    """
    from tela.renderizador import _preparar_contexto_navegacao
    lista = [e for e in modelo.corpo.elementos if e.tipo == "console"]
    console = lista[0] if lista else None
    _preparar_contexto_navegacao(
        _ESTILO_CURVA, None, None, False,
        foco_console=0, cursores={console.id: 0} if console else {},
        lista_foco=lista,
        largura_navegacao=None, selecoes={console.id: []} if console else {},
        chips_destacados=None, executar_disponivel=None,
        paginas_atuais={console.id: 1} if console else {},
        modelo=modelo,
    )


def test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta():
    from tela.controle_execucao import ControleExecucaoRepresentacao
    from tela.loader import carregar_estilo
    from tela.renderizacao.texto_ansi import _codigo_ansi_de_cor

    estilo_h0050 = carregar_estilo()
    representacao = ControleExecucaoRepresentacao(
        modo="dry_run",
        chip_id="chip_controle_execucao",
        rotulo="Simulação",
        destacado=True,
    )
    bar = {
        "distribuicao": "horizontal",
        "chips": [
            {"id": "chip_esc", "tecla": "Esc", "texto": "Sair"},
            {
                "id": "chip_espaco",
                "tecla": "␣",
                "texto": "Marcar",
            },
            {
                "id": "chip_enter",
                "tecla": "⏎",
                "texto": "Todos",
                "forma_exibicao": "rotulo_dinamico_selecao",
            },
            {
                "id": "chip_controle_execucao",
                "tecla": "Ins",
                "texto": "Executar",
                "forma_exibicao": "controle_execucao",
            },
            {"id": "chip_verboso", "tecla": "V", "texto": "Verboso"},
            {"id": "chip_ajuda", "tecla": "?", "texto": "Ajuda"},
        ],
    }
    linhas = _linhas_barra(bar, estilo_h0050, 80, representacao)
    saida = " ".join(linhas)
    assert "[Espaço]" not in saida
    assert "[Enter]" not in saida
    assert "[Insert]" not in saida
    assert "[␣] Marcar" in saida
    assert "[⏎] Todos" in saida
    assert "[Ins] Simulação" in saida
    assert "[V] Verboso" in saida
    assert "[?] Ajuda" in saida
    assert saida.index("[␣]") < saida.index("[⏎]")
    assert saida.index("[⏎]") < saida.index("[Ins]")
    assert saida.index("[Ins]") < saida.index("[V]")
    assert saida.index("[Ins]") < saida.index("[?]")
    assert _codigo_ansi_de_cor(estilo_h0050.cor_alerta) in saida
    linhas_estreitas = _linhas_barra(bar, estilo_h0050, 50, representacao)
    junta_estreita = " ".join(linhas_estreitas)
    assert len(linhas_estreitas) >= 2
    assert "[␣] Marcar" in junta_estreita
    assert "[⏎] Todos" in junta_estreita
    assert "[Ins] Simulação" in junta_estreita
    assert "[V] Verboso" in junta_estreita
    assert "[?] Ajuda" in junta_estreita

    representacao_real = ControleExecucaoRepresentacao(
        modo="executar",
        chip_id="chip_controle_execucao",
        rotulo="Real",
        destacado=False,
    )
    saida_real = " ".join(
        _linhas_barra(bar, estilo_h0050, 80, representacao_real)
    )
    assert "[Ins] Real" in saida_real
    codigo_alerta = _codigo_ansi_de_cor(estilo_h0050.cor_alerta)
    codigo_inativo = _codigo_ansi_de_cor(estilo_h0050.cor_inativo)
    if codigo_alerta:
        assert codigo_alerta not in saida_real
    if codigo_inativo:
        assert codigo_inativo not in saida_real
