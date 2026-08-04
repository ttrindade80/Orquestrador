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

import pytest as _pytest_qa002
from tela.loader import carregar_estilo as _carregar_estilo_qa002
from tela import navegacao as _nav_qa002
from tela import selecao as _sel_qa002
from tela import renderizador as _rend_qa002
from tela.loader import carregar_tela as _carregar_tela_p21
from tela.modelo import construir_modelo as _construir_modelo_p21
from tela import navegacao as _nav_p21



__all__ = [
    'teste_selecao_multipla_h0041',
    'test_qah0041_002_chip_enter_sem_selecao_ativo',
    'test_qah0041_002_chip_enter_com_selecao_inativo',
    'test_qah0041_002_estado_logico_independente_do_rotulo',
    'test_qah0041_002_chip_enter_inativo_distingue_de_ativo',
    'test_qah0041_002_chip_enter_inativo_nao_cria_operacao',
    'test_qah0041_002_console_sem_selecao_multipla_preserva_ativo',
    'test_qah0041_002_renderer_avalia_regra_ativo_nao_ignora',
    'test_h0041_manual_001_espaco_inativo_em_item_nao_selecionavel',
    'test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao',
    'test_h0041_manual_001_espaco_recalculado_por_movimento',
    'test_h0041_manual_002_enter_inativo_com_selecao_visual',
    'test_h0041_manual_003_todos_e_redraw_no_mesmo_quadro',
    'test_h0041_manual_003_selecao_vazia_apresenta_todos_ativo',
    'test_h0041_manual_001_console_sem_selecao_multipla_sem_espaco_inativo',
    'test_h0041_p04_chip_ativo_preserva_apresentacao',
    'test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura',
    'test_h0041_p04_estado_logico_nao_inferido_pelo_rotulo',
    'test_h0041_p04_texto_chip_barra_nao_usa_lower',
    'TestRotuloDinamicoEscP21',
]


def teste_selecao_multipla_h0041():
    """Testes de integracao da coluna ``tg`` e chips dinamicos (H-0041).

    Exercita o renderer sobre a fixture D-SEL-22 (oito itens; seis navegaveis,
    dois nao navegaveis; quatro selecionaveis) com estado de selecao por
    console. Valida: coluna ``ec`` exclusiva do cursor; coluna ``tg``
    distinguindo incluido/nao incluido/nao selecionavel; item nao navegavel
    visivel sem cursor e com ``tg`` vazio; chip ``Espaco``/``Enter`` presentes;
    rotulo dinamico ``Todos``/``Executar``; ``Executar`` inativo (nenhuma
    operacao externa).
    """
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    from tela import navegacao as _nav

    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav.lista_foco(modelo)
    console = lista[0]

    def _render(selecoes):
        return renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes=selecoes,
        )

    # --- Estado inicial: cursor em item_01, selecao vazia ---
    saida_ini = _render({})
    _registrar(
        "H-0041 CA-07: cursor ec aparece em item_01 (estado inicial)",
        "Item um" in saida_ini and "→" in saida_ini,
    )
    # tg nao-incluido (○) nos selecionaveis; vazio nos nao selecionaveis.
    _registrar(
        "H-0041 CA-08: tg nao-incluido (○) presente em selecionaveis",
        saida_ini.count("○") >= 4,
        "contagem ○ = {0}".format(saida_ini.count("○")),
    )
    _registrar(
        "H-0041 CA-09: item_04/item_08 visiveis sem cursor",
        "nao navegavel" in saida_ini,
    )
    _registrar(
        "H-0041 chip Enter=Todos (selecao vazia)",
        "Todos" in saida_ini,
    )
    _registrar(
        "H-0041 chip Espaco presente (selecao multipla)",
        "␣" in saida_ini,
    )

    # --- Apos marcar item_01: tg incluido (●) em item_01 ---
    saida_marcado = _render({console.id: ["item_01"]})
    _registrar(
        "H-0041 CA-08: tg incluido (●) presente apos marcar item_01",
        "●" in saida_marcado,
        "contagem ● = {0}".format(saida_marcado.count("●")),
    )
    # QA-H0041-002 (P02): chip Enter com selecao e INATIVO por estado logico
    # (``regra_ativo: selecao_vazia`` avaliada), nao por inferencia do rotulo.
    # H-0041 P04: representacao visual inativa usa cor_inativo (nao caixa baixa).
    from tela import selecao as _sel
    from tela import renderizador as _rend
    estado_sel = {"selecoes": {console.id: ["item_01"]}}
    codigo_inativo = _rend._codigo_ansi_de_cor(_ESTILO_CURVA.cor_inativo)
    _registrar(
        "H-0041 chip Enter INATIVO (estado logico via regra_ativo, nao rotulo)",
        _sel.rotulo_enter(estado_sel, console) == "Executar"
        and _rend._navegacao_atual.get("estado_ativo_chips", {}).get(
            "chip_enter"
        ) is False
        and "Executar" in saida_marcado
        and "executar" not in saida_marcado
        and codigo_inativo in saida_marcado
        and _rend._ANSI_RESET_FG in saida_marcado,
        "rotulo={0!r} ativo={1!r}".format(
            _sel.rotulo_enter(estado_sel, console),
            _rend._navegacao_atual.get("estado_ativo_chips", {}).get(
                "chip_enter"
            ),
        ),
    )

    # --- Apos Todos: inclui item_01,03,05,07 ---
    saida_todos = _render({console.id: ["item_01", "item_03", "item_05", "item_07"]})
    _registrar(
        "H-0041 CA-08: Todos marca exatamente 4 selecionaveis (●)",
        saida_todos.count("●") == 4,
        "contagem ● = {0}".format(saida_todos.count("●")),
    )

    # --- ec independente da selecao (cursor em item_01, selecao em item_03) ---
    saida_div = _render({console.id: ["item_03"]})
    _registrar(
        "H-0041 CA-07: ec independe da selecao (cursor item_01, sel item_03)",
        saida_div.count("→") == 1 and saida_div.count("●") == 1,
        "→ = {0}, ● = {1}".format(saida_div.count("→"), saida_div.count("●")),
    )


def _carregar_fixture_h0041_qa002():
    """Carrega o modelo e o console da fixture D-SEL-22 para QA-H0041-002."""
    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    return modelo, lista, lista[0]


def _chip_enter_fixture(modelo):
    """Devolve o dict do chip_enter declarado na barra_de_menus da fixture."""
    chips = (modelo.barra_de_menus or {}).get("chips") or []
    for chip in chips:
        if isinstance(chip, dict) and chip.get("id") == "chip_enter":
            return chip
    return None


@_pytest_qa002.fixture(name="fixture_h0041_qa002")
def _fixture_h0041_qa002():
    return _carregar_fixture_h0041_qa002()


def test_qah0041_002_chip_enter_sem_selecao_ativo(fixture_h0041_qa002):
    # caso_sem_selecao: rotulo=Todos, estado_logico=ATIVO, visual=ativa.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    assert chip.get("regra_ativo") == "selecao_vazia"
    estado_sel = {"selecoes": {}}
    assert _sel_qa002.rotulo_enter(estado_sel, console) == "Todos"
    # Estado logico via regra_ativo (nao via rotulo).
    assert _rend_qa002._avaliar_regra_ativo(
        chip.get("regra_ativo"), selecao_vazia=True
    ) is True
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is True
    assert "Todos" in saida
    assert "todos" not in saida  # representacao visual ativa (sem caixa baixa)


def test_qah0041_002_chip_enter_com_selecao_inativo(fixture_h0041_qa002):
    # caso_com_selecao: rotulo=Executar, estado_logico=INATIVO, visual=inativa.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    assert chip.get("regra_ativo") == "selecao_vazia"
    estado_sel = {"selecoes": {console.id: ["item_01"]}}
    assert _sel_qa002.rotulo_enter(estado_sel, console) == "Executar"
    # Estado logico via regra_ativo (nao via rotulo == "Executar").
    assert _rend_qa002._avaliar_regra_ativo(
        chip.get("regra_ativo"), selecao_vazia=False
    ) is False
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # H-0041 P04: capitalizacao preservada; inatividade via cor_inativo.
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo and codigo in saida
    assert _rend_qa002._ANSI_RESET_FG in saida


def test_qah0041_002_estado_logico_independente_do_rotulo(fixture_h0041_qa002):
    # independencia: alterar_apenas_rotulo nao define estado;
    # estado_logico nao e inferido do texto.
    modelo, lista, console = fixture_h0041_qa002
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    regra = chip.get("regra_ativo")
    assert regra == "selecao_vazia"
    # Mesmo com texto forçado para "Executar", selecao vazia => ATIVO.
    assert _rend_qa002._avaliar_regra_ativo(
        regra, selecao_vazia=True
    ) is True
    # Mesmo com texto forçado para "Todos", selecao nao vazia => INATIVO.
    assert _rend_qa002._avaliar_regra_ativo(
        regra, selecao_vazia=False
    ) is False
    # regra_ativo "sempre" permanece ATIVO independente da selecao/rotulo.
    assert _rend_qa002._avaliar_regra_ativo(
        "sempre", selecao_vazia=False
    ) is True
    # Prova de que o renderer consome a regra da fixture: com selecao, o
    # estado materializado e INATIVO porque regra=selecao_vazia (se fosse
    # derivado so do rotulo sem avaliar a regra, o teste acima de "sempre"
    # nao distinguiria a autoridade).
    estilo = _carregar_estilo_qa002()
    renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # Rotulo e estado sao propriedades distintas apos render.
    assert _sel_qa002.rotulo_enter(
        {"selecoes": {console.id: ["item_01"]}}, console
    ) == "Executar"


def test_qah0041_002_chip_enter_inativo_distingue_de_ativo(fixture_h0041_qa002):
    # Distincao visual e consequencia do estado logico (R-6: chip permanece).
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    saida_ativo = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    ativo_logico = _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"]
    saida_inativo = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    inativo_logico = _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"]
    assert ativo_logico is True
    assert inativo_logico is False
    assert "Todos" in saida_ativo
    assert "Executar" in saida_inativo
    assert "executar" not in saida_inativo
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida_inativo
    assert codigo not in saida_ativo
    assert "⏎" in saida_ativo
    assert "⏎" in saida_inativo


def test_qah0041_002_chip_enter_inativo_nao_cria_operacao(fixture_h0041_qa002):
    # Enter_em_Executar: nenhuma operacao/callback/mensagem provisoria.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    assert "executando" not in saida.lower()
    assert "resultado" not in saida.lower()


def test_qah0041_002_console_sem_selecao_multipla_preserva_ativo():
    # consoles_sem_selecao_multipla: comportamento anterior preservado.
    tela_raw = carregar_tela(
        None, "h0040_nav_console_unico_linear", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    console = lista[0]
    estilo = _carregar_estilo_qa002()
    assert not _nav_qa002._console_declarou_selecao_multipla(console)
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    # Sem chip Enter de selecao; chips existentes permanecem ATIVOS
    # (regra_ativo=sempre). Nenhum rotulo forcado para caixa baixa.
    estados = _rend_qa002._navegacao_atual.get("estado_ativo_chips") or {}
    assert "chip_enter" not in estados
    for ativo in estados.values():
        assert ativo is True
    assert "executar" not in saida


def test_qah0041_002_renderer_avalia_regra_ativo_nao_ignora(fixture_h0041_qa002):
    # O teste principal deve falhar se o renderer ignorar regra_ativo.
    # Comprova: fixture declara selecao_vazia; com selecao o estado e INATIVO;
    # se regra fosse ignorada (sempre ATIVO), esta asserção quebraria.
    modelo, lista, console = fixture_h0041_qa002
    chip = _chip_enter_fixture(modelo)
    assert chip.get("regra_ativo") != "sempre"
    assert chip.get("regra_ativo") == "selecao_vazia"
    estilo = _carregar_estilo_qa002()
    renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    # Se o renderer ignorasse regra_ativo e usasse default ATIVO, falharia.
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # Se enter_inativo fosse so rotulo_enter == "Executar" sem consumir a
    # regra, a troca da regra para "sempre" manteria inativo — prova inversa:
    assert _rend_qa002._avaliar_regra_ativo(
        "sempre", selecao_vazia=False
    ) is True
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


def _carregar_fixture_h0041_p03():
    """Carrega modelo/estilo/console/lista da fixture D-SEL-22 para o P03."""
    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    estilo = _carregar_estilo_qa002()
    return modelo, lista, lista[0], estilo


def _renderizar_h0041_p03(modelo, lista, console, estilo, *, foco, selecoes):
    """Renderiza a fixture com foco/selecoes dados e devolve (saida, chips)."""
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: foco}, lista_foco=lista, selecoes=selecoes,
    )
    chips = _rend_qa002._navegacao_atual["estado_ativo_chips"]
    return saida, chips


def _barra_chip(saida, tecla):
    """Extrai a linha da barra que contem o chip de ``tecla`` (␣ ou ⏎)."""
    for linha in saida.split("\n"):
        if tecla in linha:
            return linha
    return ""


def test_h0041_manual_001_espaco_inativo_em_item_nao_selecionavel():
    # H0041-MANUAL-001: cursor em item_02 (nao selecionavel) com selecao ativa.
    # O chip Espaco deve estar INATIVO (item nao selecionavel); o chip Enter
    # deve estar INATIVO (selecao nao vazia = Executar). O estado logico e a
    # prova; a caixa baixa e consequencia (R-6).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_02 e indice logico 1; precondicao selecao=[item_01].
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=1, selecoes={console.id: ["item_01"]},
    )
    # Estado logico (prova, independente do rotulo).
    assert chips["chip_espaco"] is False
    assert chips["chip_enter"] is False
    # Texto renderizado: capitalizacao preservada; inatividade via cor_inativo.
    barra = _barra_chip(saida, "␣")
    assert "Marcar" in barra
    assert "marcar" not in barra
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in barra
    assert _rend_qa002._ANSI_RESET_FG in barra


def test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao():
    # H0041-MANUAL-001 (precondicao espelhada): cursor em item_03 (selecionavel)
    # com selecao=[item_01]. O chip Espaco deve estar ATIVO; Enter permanece
    # INATIVO (Executar). Prova que o estado do Espaco depende do item sob
    # cursor, nao apenas da existencia de selecao multipla.
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_03 e indice logico 2; precondicao selecao=[item_01].
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=2, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is True
    assert chips["chip_enter"] is False
    barra = _barra_chip(saida, "␣")
    assert "Marcar" in barra
    assert "Executar" in saida
    assert "executar" not in saida
    # Espaco ativo nao recebe cor_inativo; Enter inativo sim (mesma linha).
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert "{0}[␣]".format(codigo) not in barra
    assert "[␣] Marcar" in barra
    assert "{0}[⏎] Executar{1}".format(codigo, _rend_qa002._ANSI_RESET_FG) in barra


def test_h0041_manual_001_espaco_recalculado_por_movimento():
    # O estado do chip Espaco e recalculado apos cada movimento do cursor
    # (sem estado visual residual entre renders consecutivos).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_01 (selecionavel) -> ATIVO
    _, chips_01 = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips_01["chip_espaco"] is True
    # item_02 (nao selecionavel) -> INATIVO
    _, chips_02 = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=1, selecoes={},
    )
    assert chips_02["chip_espaco"] is False
    # volta a item_01 -> ATIVO de novo (sem residuo)
    _, chips_01b = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips_01b["chip_espaco"] is True


def test_h0041_manual_002_enter_inativo_com_selecao_visual():
    # H0041-MANUAL-002: o estado logico INATIVO do chip Enter (regra_ativo=
    # selecao_vazia) se materializa na barra. A prova e o estado logico; a
    # caixa baixa e consequencia material (nao aceita como solucao unica).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=0, selecoes={console.id: ["item_01"]},
    )
    assert _sel_qa002.rotulo_enter(
        {"selecoes": {console.id: ["item_01"]}}, console
    ) == "Executar"
    assert chips["chip_enter"] is False
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida
    assert _rend_qa002._ANSI_RESET_FG in saida
    # Nao e por comparacao direta de rotulo: a regra e a autoridade.
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


def test_h0041_manual_003_todos_e_redraw_no_mesmo_quadro():
    # H0041-MANUAL-003: apos Enter iniciado com selecao vazia (Todos), uma
    # unica renderizacao apresenta conjuntamente os 4 tg incluidos E o chip
    # Enter como Executar INATIVO. O contexto dos chips nao pode ser calculado
    # antes da alteracao da selecao e reutilizado depois dela: como cada
    # render ler ``selecoes`` do estado corrente, o estado e sempre sincrono.
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    quatro = ["item_01", "item_03", "item_05", "item_07"]
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=2, selecoes={console.id: quatro},
    )
    # tg incluidos no mesmo quadro (4 marcadores ●).
    assert saida.count("●") == 4
    # chip Enter = Executar INATIVO no mesmo quadro.
    assert chips["chip_enter"] is False
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida
    # chip Espaco conforme item sob cursor (item_03 selecionavel -> ATIVO).
    assert chips["chip_espaco"] is True


def test_h0041_manual_003_selecao_vazia_apresenta_todos_ativo():
    # Espelho do MANUAL-003 no estado inicial (pre-Todos): selecao vazia =>
    # chip Enter = Todos ATIVO, tg todos nao-incluidos (○). Confirma que a
    # transicao vazia->Executar INATIVO e observavel (nao eh default fixo).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=2, selecoes={},
    )
    assert chips["chip_enter"] is True
    assert "Todos" in saida
    assert "todos" not in saida  # ativo: caixa alta (sem reducao de enfase)


def test_h0041_manual_001_console_sem_selecao_multipla_sem_espaco_inativo():
    # Preservacao de consoles sem selecao multipla: nenhum chip forcado para
    # inativo por item (nao ha regra_ativo=item_focalizado_selecionavel).
    tela_raw = carregar_tela(
        None, "h0040_nav_console_unico_linear", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    console = lista[0]
    estilo = _carregar_estilo_qa002()
    assert not _nav_qa002._console_declarou_selecao_multipla(console)
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    estados = _rend_qa002._navegacao_atual.get("estado_ativo_chips") or {}
    assert "chip_espaco" not in estados
    for ativo in estados.values():
        assert ativo is True
    assert "marcar" not in saida


def test_h0041_p04_chip_ativo_preserva_apresentacao():
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips["chip_espaco"] is True
    assert chips["chip_enter"] is True
    barra_espaco = _barra_chip(saida, "␣")
    assert "Marcar" in barra_espaco
    assert "Todos" in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo not in barra_espaco


def test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura():
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=1, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is False
    assert chips["chip_enter"] is False
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert estilo.cor_inativo == "cinza"
    assert codigo == "\x1b[90m"
    # Fragmento do chip Espaco: cor antes do rotulo e reset apos.
    barra = _barra_chip(saida, "␣")
    idx_cor = barra.find(codigo)
    idx_marcar = barra.find("Marcar")
    idx_reset = barra.find(_rend_qa002._ANSI_RESET_FG, idx_cor)
    assert idx_cor != -1
    assert idx_marcar != -1
    assert idx_cor < idx_marcar < idx_reset
    assert "Executar" in saida
    assert "marcar" not in saida
    assert "executar" not in saida


def test_h0041_p04_estado_logico_nao_inferido_pelo_rotulo():
    # Mesmo com rotulos capitalizados, o estado vem de regra_ativo.
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False
    assert _rend_qa002._avaliar_regra_ativo(
        "item_focalizado_selecionavel", item_focalizado_selecionavel=False
    ) is False


def test_h0041_p04_texto_chip_barra_nao_usa_lower():
    chip = {"tecla": "⏎", "texto": "Executar"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_CURVA, vao=1, inativo=True
    )
    assert "Executar" in texto
    assert "executar" not in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") in texto
    assert texto.endswith(_rend_qa002._ANSI_RESET_FG)


def _carregar_fixture_p21(id_tela):
    """Carrega modelo/lista/console/estilo de uma fixture para os testes P21."""
    tela_raw = _carregar_tela_p21(None, id_tela, _RAIZ_TELAS_DEMO)
    modelo = _construir_modelo_p21(tela_raw)
    lista = _nav_p21.lista_foco(modelo)
    return modelo, lista, lista[0]


def _barra_esc_p21(saida):
    """Extrai a linha da barra de menus que contem o chip ``[Esc]``.

    A descricao do cabecalho pode mencionar ``Esc`` (ex.: \"Esc limpa antes
    de sair\"); por isso casamos pelo token do chip ``[Esc]`` e nao pela
    palavra solta ``Esc``.
    """
    for linha in saida.split("\n"):
        if "[Esc]" in linha:
            return linha
    return ""


class TestRotuloDinamicoEscP21:
    """VM-H0045-R06-001 (P21): chip ``[Esc]`` dinamico via ``forma_exibicao``."""

    def test_chip_esc_usa_rotulo_dinamico_esc_na_fixture_h0041(self):
        # Confirmacao focal: a fixture h0041 declara a nova forma de exibicao.
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        assert chip_esc["forma_exibicao"] == "rotulo_dinamico_esc"
        # Texto original preservado como fallback.
        assert chip_esc["texto"] == "Sair"

    # (1) selecao multipla VAZIA exibe o rotulo original ``Sair``.
    def test_rotulo_original_sair_quando_selecao_vazia(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra

    # (3) uma selecao exibe ``Limpar``.
    def test_limpar_quando_uma_selecao(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra
        assert "Sair" not in barra

    # (4) varias selecoes exibem ``Limpar``.
    def test_limpar_quando_varias_selecoes(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01", "item_03", "item_05", "item_07"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra

    # (10) ``Limpar`` e o rotulo original nunca coexistem para Esc.
    def test_limpar_e_sair_nunca_coexistem(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        s_vazio = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        s_sel = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        b_vazio = _barra_esc_p21(s_vazio)
        b_sel = _barra_esc_p21(s_sel)
        assert "[Esc] Sair" in b_vazio and "Limpar" not in b_vazio
        assert "[Esc] Limpar" in b_sel and "Sair" not in b_sel

    # (8) Apos limpar (voltar ao vazio), reaparece o rotulo original.
    def test_apos_limpar_reaparece_rotulo_original(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        # Estado inicialmente com selecao -> ``Limpar``.
        s_sel = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        assert "[Esc] Limpar" in _barra_esc_p21(s_sel)
        # Apos limpar (Esc), selecao volta a vazia -> rotulo original.
        s_pos = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        assert "[Esc] Sair" in _barra_esc_p21(s_pos)
        assert "Limpar" not in _barra_esc_p21(s_pos)

    # (13) Troca de foco: somente o console focal determina o rotulo.
    def test_troca_de_foco_considera_somente_console_focal(self):
        # h0045_dois_consoles: ambos selecao UNICA => Esc sempre ``Sair``.
        tela_raw = _carregar_tela_p21(
            None, "h0045_dois_consoles_paginas_independentes", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        lista = _nav_p21.lista_foco(modelo)
        # Cada console tem selecao unica => chip Esc original preservado,
        # independentemente de foco (prova que selecao unica nao recebe
        # ``Limpar`` e que a troca de foco nao inventa ``Limpar``).
        for foco in range(len(lista)):
            saida = renderizar_tela(
                modelo, _ESTILO_CURVA, largura=100, foco_console=foco,
                cursores={lista[0].id: 0, lista[1].id: 0},
                lista_foco=lista, selecoes={},
                paginas_atuais={lista[0].id: 1, lista[1].id: 1},
            )
            barra = _barra_esc_p21(saida)
            assert "[Esc] Sair" in barra, foco
            assert "Limpar" not in barra, foco

    # (14) Console de selecao UNICA preserva seu chip original.
    def test_console_selecao_unica_preserva_chip_original(self):
        tela_raw = _carregar_tela_p21(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        # Confirmacao: selecao unica NAO declara rotulo_dinamico_esc.
        assert chip_esc["forma_exibicao"] != "rotulo_dinamico_esc"
        lista = _nav_p21.lista_foco(modelo)
        if not lista:
            return  # console nao focalizavel (sem itens navegaveis) -- nada a
            # provar aqui; o chip original ja e preservado por exclusao.
        console = lista[0]
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=80, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
            paginas_atuais={console.id: 1},
        )
        assert "[Esc] Sair" in saida
        assert "Limpar" not in saida

    # Preservacao: tecla, ordem, atividade, cores do chip Esc mantidas.
    def test_chip_esc_preserva_tecla_ordem_atividade(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        # Esc permanece o PRIMEIRO chip (regra contratual ``_garantir_esc_primeiro``).
        barra = _barra_esc_p21(saida)
        assert barra.index("[Esc]") < barra.index("[␣]")
        # Estado logico do chip Esc permanece ATIVO (regra_ativo: sempre).
        from tela import renderizador as _rend_p21
        assert _rend_p21._navegacao_atual["estado_ativo_chips"].get(
            "chip_esc"
        ) is True

    # Isolamento por console focal: selecao em OUTRO console nao produz
    # ``Limpar`` para o console focal (cenario com selecao multipla).
    def test_selecao_em_outro_console_nao_afeta_rotulo_do_focal(self):
        # h0045_dois_consoles e selecao unica; constroimos dois consoles
        # multipla manualmente para isolar a regra do renderer.
        from tela.modelo import ElementoCorpo, ModeloTela, Corpo
        itens_a = [
            {"id": "a1", "texto": "A1", "navegavel": True, "selecionavel": True},
            {"id": "a2", "texto": "A2", "navegavel": True, "selecionavel": True},
        ]
        itens_b = [
            {"id": "b1", "texto": "B1", "navegavel": True, "selecionavel": True},
            {"id": "b2", "texto": "B2", "navegavel": True, "selecionavel": True},
        ]
        ca = ElementoCorpo(
            id="console_a", tipo="console",
            _campos_inertes={
                "titulo": "A", "itens": itens_a,
                "politica_navegacao": {"navegavel": True},
                "politica_selecao": "multipla",
            },
        )
        cb = ElementoCorpo(
            id="console_b", tipo="console",
            _campos_inertes={
                "titulo": "B", "itens": itens_b,
                "politica_navegacao": {"navegavel": True},
                "politica_selecao": "multipla",
            },
        )
        modelo = ModeloTela(
            id="t_p21", schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": ""},
            corpo=Corpo(arranjo="vertical", elementos=[ca, cb]),
            barra_de_menus={
                "distribuicao": "horizontal",
                "chips": [
                    {"id": "chip_esc", "tipo": "acao", "tecla": "Esc",
                     "texto": "Sair", "regra_existencia": "sempre",
                     "regra_ativo": "sempre",
                     "forma_exibicao": "rotulo_dinamico_esc"},
                ],
            },
            _raw={},
        )
        lista = [ca, cb]
        # Foco em console_a (sem selecao); console_b COM selecao.
        # O chip Esc deve exibir ``Sair`` (rotulo do focal), nao ``Limpar``.
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={ca.id: 0, cb.id: 0}, lista_foco=lista,
            selecoes={cb.id: ["b1"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra
        # Trocando o foco para console_b (com selecao): agora ``Limpar``.
        saida_b = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=1,
            cursores={ca.id: 0, cb.id: 0}, lista_foco=lista,
            selecoes={cb.id: ["b1"]},
        )
        assert "[Esc] Limpar" in _barra_esc_p21(saida_b)

    # Forma de exibicao ausente/outra preserva o rotulo original (nao inventa).
    def test_forma_exibicao_visivel_ativo_preserva_rotulo_original(self):
        # h0045_paginacao_console_unico usa ``visivel_ativo`` (selecao unica);
        # o renderer NAO resolve rotulo dinamico, exibindo o texto configurado.
        tela_raw = _carregar_tela_p21(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        lista = _nav_p21.lista_foco(modelo)
        if not lista:
            return
        console = lista[0]
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=80, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
            paginas_atuais={console.id: 1},
        )
        assert "[Esc] Sair" in saida
