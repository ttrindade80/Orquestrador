"""Testes focais do ciclo modal demonstrativo H-0056."""

import copy
import importlib.util
from pathlib import Path


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
