"""Testes focais do ciclo modal demonstrativo H-0056."""

import copy
import importlib.util
from pathlib import Path

from tela.renderizacao import popup


_SPEC = importlib.util.spec_from_file_location(
    "h0056_demo_under_test",
    Path(__file__).with_name("demo.py"),
)
demo = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(demo)


def test_abertura_resolve_declaracao_e_preserva_tela_subjacente():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = demo.criar_estado_inicial()
    declaracao_original = copy.deepcopy(modelo._raw["popups"])

    aberto = demo.processar_comando(estado, "p", modelo)

    assert aberto["popup"].id == "popup_basico"
    assert aberto["tela_atual"] == estado["tela_atual"] == "demo"
    assert aberto["pilha_telas"] == estado["pilha_telas"] == []
    assert aberto["popup"].conteudo == {
        "tipo": "texto",
        "texto": "Exemplo de pop-up.",
    }
    assert modelo._raw["popups"] == declaracao_original
    assert "texto" not in modelo._raw["popups"]["popup_basico"]


def test_modal_captura_tecla_nao_declarada_e_renderiza_overlay():
    modelo = demo._carregar_modelo_por_id("demo")
    estilo = demo.carregar_estilo()
    estado = dict(demo.criar_estado_inicial(), estilo=estilo)
    aberto = demo.processar_comando(estado, "p", modelo)
    antes = {
        chave: aberto.get(chave)
        for chave in (
            "tela_atual",
            "pilha_telas",
            "foco_console",
            "cursores",
            "selecoes",
            "pagina_atual",
        )
    }

    ignorado = demo.processar_comando(aberto, "x", modelo)
    depois = {
        chave: ignorado.get(chave)
        for chave in antes
    }
    assert ignorado["popup"] is aberto["popup"]
    assert depois == antes
    quadro = demo.renderizar_estado(aberto, modelo, largura=80, altura=24)
    assert "Mensagem" in quadro
    assert "Exemplo de pop-up." in quadro
    assert "Esc" in quadro
    assert "Voltar" in quadro or "VOLTAR" in quadro


def test_esc_fecha_com_abortado_sem_payload_e_reativa_mesma_tela():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = demo.criar_estado_inicial()
    aberto = demo.processar_comando(estado, "p", modelo)
    fechado = demo.processar_comando(aberto, "\x1b", modelo)

    assert fechado["popup"] is None
    assert fechado["popup_resultado"] == {"status": "ABORTADO"}
    assert "valor" not in fechado["popup_resultado"]
    assert fechado["tela_atual"] == "demo"
    assert fechado["pilha_telas"] == []

    reativado = demo.processar_comando(fechado, "d", modelo)
    assert reativado["popup"] is None
    assert reativado["tela_atual"] == "destino_minimo"
    assert reativado["pilha_telas"] == ["demo"]


def test_acionamento_referencia_popup_basico_e_nao_barra_de_menus():
    modelo = demo._carregar_modelo_por_id("demo")
    assert demo._popup_acionado_por(modelo, "p") == "popup_basico"
    assert modelo._raw["acionamentos"][0] == {
        "tipo": "popup",
        "tecla": "p",
        "popup": "popup_basico",
    }
    ids_barra = [chip["id"] for chip in modelo._raw["barra_de_menus"]["chips"]]
    assert "popup_basico_voltar" not in ids_barra


def test_h0057_declara_popup_fixture_runtime_sem_conteudo_no_json():
    modelo = demo._carregar_modelo_por_id("demo")
    declaracao = modelo._raw["popups"]["popup_texto_dinamico"]
    assert "id" not in declaracao
    assert "conteudo" not in declaracao
    assert demo._popup_acionado_por(modelo, "w") == "popup_texto_dinamico"

    estado = demo.criar_estado_inicial()
    aberto = demo.processar_comando(estado, "w", modelo)
    assert aberto["popup"].id == "popup_texto_dinamico"
    assert aberto["popup"].conteudo == demo.conteudo_popup_h0057()


def test_h0057_wrapping_recompoe_e_preserva_a_mesma_instancia():
    modelo = demo._carregar_modelo_por_id("demo")
    estilo = demo.carregar_estilo()
    estado = dict(demo.criar_estado_inicial(), estilo=estilo)
    aberto = demo.processar_comando(estado, "w", modelo)
    instancia = aberto["popup"]

    largo = demo.renderizar_estado(aberto, modelo, largura=80, altura=24)
    estreito = demo.renderizar_estado(aberto, modelo, largura=75, altura=24)
    restaurado = demo.renderizar_estado(aberto, modelo, largura=80, altura=24)

    assert aberto["popup"] is instancia
    assert largo != estreito
    assert restaurado == largo
    assert all(len(linha) == 80 for linha in largo.splitlines())
    assert all(len(linha) == 75 for linha in estreito.splitlines())
    assert all(palavra in estreito for palavra in ("conteudo", "wrapping", "instancia"))
    assert popup.geometria_popup(instancia, estilo, largura_corpo=75)["largura"] == 75


def test_h0057_resize_vertical_usa_quadro_geral_e_retorna_sem_reabrir():
    modelo = demo._carregar_modelo_por_id("demo")
    estilo = demo.carregar_estilo()
    estado = dict(demo.criar_estado_inicial(), estilo=estilo)
    aberto = demo.processar_comando(estado, "w", modelo)
    instancia = aberto["popup"]

    pequeno = demo._resolver_conteudo(aberto, modelo, 75, 10)
    assert "Terminal pequeno demais" in pequeno
    assert aberto["popup"] is instancia

    recuperado = demo._resolver_conteudo(aberto, modelo, 75, 24)
    assert "Texto dinamico" in recuperado
    assert demo.renderizar_estado(aberto, modelo, 75, 24) == recuperado
    assert aberto["popup"] is instancia


def test_h0057_dimensoes_invalidas_preservam_ultimo_par_valido(monkeypatch):
    monkeypatch.setattr(demo, "_obter_dimensoes_ioctl", lambda fd: None)
    monkeypatch.setattr(demo, "_obter_dimensoes_env", lambda: None)
    assert demo._obter_dimensoes_apos_sigwinch(0, (75, 24)) == (75, 24)


def test_h0057_modalidade_esc_abortado_sem_payload_e_tecla_x_inerte():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = demo.criar_estado_inicial()
    aberto = demo.processar_comando(estado, "w", modelo)
    instancia = aberto["popup"]
    ignorado = demo.processar_comando(aberto, "x", modelo)
    assert ignorado["popup"] is instancia
    assert ignorado["tela_atual"] == "demo"

    fechado = demo.processar_comando(ignorado, "\x1b", modelo)
    assert fechado["popup"] is None
    assert fechado["popup_resultado"] == {"status": "ABORTADO"}
    assert "valor" not in fechado["popup_resultado"]
    assert fechado["tela_atual"] == "demo"


def test_h0058_acionamentos_e_m_abrem_fixtures_separadas_com_seis_itens():
    modelo = demo._carregar_modelo_por_id("demo")
    assert demo._popup_acionado_por(modelo, "e") == "popup_lista_exclusiva"
    assert demo._popup_acionado_por(modelo, "m") == "popup_lista_multipla"

    estado = demo.criar_estado_inicial()
    exclusivo = demo.processar_comando(estado, "e", modelo)
    multiplo = demo.processar_comando(estado, "m", modelo)
    assert exclusivo["popup"].id == "popup_lista_exclusiva"
    assert multiplo["popup"].id == "popup_lista_multipla"
    assert [item["id"] for item in exclusivo["popup"].conteudo["itens"]] == [
        "opcao_1", "opcao_2", "opcao_3", "opcao_4", "opcao_5", "opcao_6"
    ]
    assert exclusivo["popup"].marcados == ["opcao_2"]
    assert multiplo["popup"].marcados == ["opcao_2", "opcao_4"]


def test_h0058_modal_captura_setas_espaco_enter_e_preserva_instancia():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = dict(
        demo.processar_comando(demo.criar_estado_inicial(), "e", modelo),
        estilo=demo.carregar_estilo(),
    )
    instancia = estado["popup"]
    quadro = demo.renderizar_estado(estado, modelo, largura=80, altura=24)
    assert "Escolha uma opção:" in quadro
    assert all("Opção " + str(indice) in quadro for indice in range(1, 7))
    assert "Esc" in quadro and "Voltar" in quadro

    movido = demo.processar_comando(estado, "\x1b[B", modelo)
    assert movido["popup"] is instancia
    assert instancia.cursor_id == "opcao_2"
    marcado = demo.processar_comando(movido, " ", modelo)
    assert marcado["popup"] is instancia
    assert instancia.marcados == ["opcao_2"]
    assert demo.processar_comando(marcado, "x", modelo)["popup"] is instancia
    for tecla in ("\r", "\n"):
        independente = dict(
            demo.processar_comando(demo.criar_estado_inicial(), "e", modelo),
            estilo=demo.carregar_estilo(),
        )
        independente = demo.processar_comando(independente, "\x1b[B", modelo)
        independente = demo.processar_comando(independente, " ", modelo)
        fechado = demo.processar_comando(independente, tecla, modelo)
        assert fechado["popup"] is None
        assert fechado["popup_resultado"] == {
            "status": "CONFIRMADO",
            "valor": "opcao_2",
        }


def test_h0058_multipla_resize_terminal_pequeno_e_esc():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = dict(
        demo.processar_comando(demo.criar_estado_inicial(), "m", modelo),
        estilo=demo.carregar_estilo(),
    )
    instancia = estado["popup"]
    demo.renderizar_estado(estado, modelo, largura=80, altura=24)
    demo.processar_comando(estado, "\x1b[B", modelo)
    assert instancia.cursor_id == "opcao_2"
    assert instancia.marcados == ["opcao_2", "opcao_4"]

    pequeno = demo._resolver_conteudo(estado, modelo, 9, 5)
    assert "terminal" not in pequeno.lower() or len(pequeno.splitlines()) == 5
    recuperado = demo._resolver_conteudo(estado, modelo, 80, 24)
    assert "Lista múltipla" in recuperado
    assert estado["popup"] is instancia
    assert instancia.cursor_id == "opcao_2"
    assert instancia.marcados == ["opcao_2", "opcao_4"]

    fechado = demo.processar_comando(estado, "\x1b", modelo)
    assert fechado["popup"] is None
    assert fechado["popup_resultado"] == {"status": "ABORTADO"}
    assert "valor" not in fechado["popup_resultado"]


def test_h0059_binding_consumido_fecha_modal_e_reativa_tela_sem_duplicar_tecla():
    modelo = demo._carregar_modelo_por_id("demo")
    estado = demo.criar_estado_inicial()
    aberto = demo.processar_comando(estado, "e", modelo)
    marcado = demo.processar_comando(aberto, " ", modelo)
    confirmado = demo.processar_comando(marcado, "\r", modelo)

    assert confirmado["popup"] is None
    assert confirmado["popup_resultado"] == {
        "status": "CONFIRMADO",
        "valor": "opcao_1",
    }
    assert confirmado["tela_atual"] == "demo"
    assert confirmado["pilha_telas"] == []

    depois = demo.processar_comando(confirmado, "d", modelo)
    assert depois["tela_atual"] == "destino_minimo"
    assert depois["pilha_telas"] == ["demo"]
    assert depois["popup_resultado"] == confirmado["popup_resultado"]

    sem_duplicar = demo.processar_comando(confirmado, "\n", modelo)
    assert sem_duplicar["popup"] is None
    assert sem_duplicar["popup_resultado"] == confirmado["popup_resultado"]


def test_h0059_binding_multiplo_entrega_lista_de_ids_na_ordem_logica():
    modelo = demo._carregar_modelo_por_id("demo")
    aberto = demo.processar_comando(demo.criar_estado_inicial(), "m", modelo)
    aberto["popup"]._estado["marcados"] = ["opcao_4", "opcao_2"]

    fechado = demo.processar_comando(aberto, "\n", modelo)
    assert fechado["popup"] is None
    assert fechado["popup_resultado"] == {
        "status": "CONFIRMADO",
        "valor": ["opcao_2", "opcao_4"],
    }
