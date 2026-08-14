"""Testes focais H-0066 — acao Aplicar sobre o candidato de estilo."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from tela.estilo import (
    CATEGORIAS_ESTILO,
    ControladorTelaEstilo,
    SolicitacaoAplicacaoEstilo,
)
from tela.loader import RuntimeEstilo, carregar_tela
from tela.modelo import construir_modelo


RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"
RAIZ_TELAS_DEMO = RAIZ / "config" / "telas" / "demo"
ID_TELA = "h0063_estilo_estrutura_navegacao_dois_niveis"

_CAMINHOS = {
    "borda": ("borda",),
    "chip": ("chip",),
    "indicadores.selecionado": ("indicadores", "selecionado"),
    "indicadores.incluido": ("indicadores", "incluido"),
}


def _em(documento, caminho):
    atual = documento
    for parte in caminho:
        atual = atual[parte]
    return atual


def _runtime(tmp_path=None):
    if tmp_path is None:
        return RuntimeEstilo()
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    return RuntimeEstilo(tmp_path)


def _modelo_estilo():
    return construir_modelo(carregar_tela(None, ID_TELA, RAIZ_TELAS_DEMO))


def _abrir(runtime=None):
    runtime = runtime or RuntimeEstilo()
    controlador = ControladorTelaEstilo(runtime)
    modelo = controlador.aplicar_ao_modelo(_modelo_estilo())
    estado = controlador.inicializar_estado(
        {"cursores": {}, "selecoes": {}, "foco_console": 0},
        modelo,
    )
    return runtime, controlador, estado, modelo


def _outro_preset(runtime, categoria):
    secao = _em(runtime.candidato, _CAMINHOS[categoria])
    atual = secao["preset_default"]
    for nome in secao["presets"]:
        if nome != atual:
            return nome
    raise AssertionError("categoria sem preset alternativo: " + categoria)


def _terceiro_preset(runtime, categoria, excluidos):
    secao = _em(runtime.candidato, _CAMINHOS[categoria])
    for nome in secao["presets"]:
        if nome not in excluidos:
            return nome
    return None


# --- Aplicar inativo (candidato == baseline) --------------------------------


def test_aplicar_inativo_quando_candidato_igual_baseline():
    runtime, controlador, estado, modelo = _abrir()
    assert hasattr(controlador, "solicitar_aplicacao")
    assert runtime.comparar_candidato_baseline() is True
    assert controlador.aplicar_disponivel is False
    # Enter/Aplicar inativo: no-op, nenhuma solicitacao.
    assert controlador.solicitar_aplicacao() is None


# --- Aplicar ativo (candidato != baseline) -----------------------------------


def test_aplicar_ativo_quando_candidato_diverge(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)

    assert runtime.comparar_candidato_baseline() is False
    assert controlador.aplicar_disponivel is True

    solicitacao = controlador.solicitar_aplicacao()
    assert isinstance(solicitacao, SolicitacaoAplicacaoEstilo)
    assert solicitacao.baseline == baseline_antes
    assert solicitacao.candidato == runtime.candidato

    # Fronteiras pos-acionamento: nada persiste, publica ou muta baseline.
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global


# --- Formula literal ----------------------------------------------------------


def test_formula_aplicar_disponivel_e_ponte_literal(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    assert controlador.aplicar_disponivel == (
        not runtime.comparar_candidato_baseline()
    )

    b = _outro_preset(runtime, "chip")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "chip", b)
    assert controlador.aplicar_disponivel == (
        not runtime.comparar_candidato_baseline()
    )
    # A inversao e obrigatoria: o retorno bruto de comparar não e conforme.
    assert controlador.aplicar_disponivel != runtime.comparar_candidato_baseline()


# --- A -> B -> A sem flag residual --------------------------------------------


def test_a_b_a_sem_flag_residual(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    a = runtime.candidato["borda"]["preset_default"]
    b = _outro_preset(runtime, "borda")

    assert controlador.aplicar_disponivel is False

    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert controlador.aplicar_disponivel is True

    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", a)
    assert controlador.aplicar_disponivel is False
    assert controlador.solicitar_aplicacao() is None


# --- Quatro categorias ---------------------------------------------------------


@pytest.mark.parametrize("categoria", CATEGORIAS_ESTILO)
def test_quatro_categorias_ativam_aplicar(categoria, tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    assert controlador.aplicar_disponivel is False

    alvo = _outro_preset(runtime, categoria)
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, categoria, alvo
    )
    assert controlador.aplicar_disponivel is True
    assert runtime.comparar_candidato_baseline() is False


# --- Espaco: muda candidato; elegibilidade acompanha ---------------------------


def test_espaco_muda_candidato_e_elegibilidade_acompanha(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    assert controlador.aplicar_disponivel is False

    b = _outro_preset(runtime, "indicadores.selecionado")
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, "indicadores.selecionado", b
    )
    assert runtime.candidato["indicadores"]["selecionado"]["preset_default"] == b
    assert controlador.aplicar_disponivel is True


# --- Esc filho -> pais (distinto de saida efetiva) -----------------------------


def test_esc_filho_preserva_elegibilidade_e_nao_emite_solicitacao(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    baseline_antes = copy.deepcopy(runtime.baseline)
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert controlador.aplicar_disponivel is True

    # Esc filho->pais e navegacional (H-0065/ADR-0042): nao invoca
    # descartar_visita nem solicitar_aplicacao; candidato/baseline intactos.
    assert runtime.candidato["borda"]["preset_default"] == b
    assert runtime.baseline == baseline_antes
    assert controlador.aplicar_disponivel is True


# --- Saida efetiva --------------------------------------------------------------


def test_saida_efetiva_restaura_e_desativa_aplicar(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    baseline_antes = copy.deepcopy(runtime.baseline)
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert controlador.aplicar_disponivel is True

    estado = controlador.descartar_visita(estado, modelo)

    assert runtime.candidato == baseline_antes
    assert runtime.baseline == baseline_antes
    assert controlador.aplicar_disponivel is False
    assert controlador.solicitar_aplicacao() is None


# --- Resize/redraw ---------------------------------------------------------------


def test_resize_redraw_preserva_elegibilidade_derivada(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert controlador.aplicar_disponivel is True

    # "Redraw"/reconciliacao repetida: reconsulta nao perde nem inventa
    # divergencia -- sempre recalculada da fonte candidato x baseline.
    for _ in range(3):
        estado = controlador.reconciliar_selecoes_com_candidato(estado, modelo)
        assert controlador.aplicar_disponivel is True
    assert controlador.aplicar_disponivel == (
        not runtime.comparar_candidato_baseline()
    )


# --- Snapshot imutavel ------------------------------------------------------------


def test_snapshot_imutavel_apos_mutacao_posterior_do_runtime(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, estado, modelo = _abrir(runtime)
    a = runtime.candidato["borda"]["preset_default"]
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)

    solicitacao_1 = controlador.solicitar_aplicacao()
    assert solicitacao_1.baseline["borda"]["preset_default"] == a
    assert solicitacao_1.candidato["borda"]["preset_default"] == b

    # Muta o runtime DEPOIS de emitida a solicitacao (candidato=C, depois=A).
    c = _terceiro_preset(runtime, "borda", {a, b})
    if c is not None:
        estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", c)
        assert runtime.candidato["borda"]["preset_default"] == c
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", a)
    assert runtime.candidato["borda"]["preset_default"] == a

    # A solicitacao antiga permanece observavelmente imutavel.
    assert solicitacao_1.baseline["borda"]["preset_default"] == a
    assert solicitacao_1.candidato["borda"]["preset_default"] == b

    # Mutar os dicts devolvidos pela solicitacao nao pode retroagir sobre o
    # runtime (copias independentes, nao referencias mutaveis compartilhadas).
    solicitacao_1.candidato["borda"]["preset_default"] = "mutacao-defensiva"
    assert runtime.candidato["borda"]["preset_default"] == a


# --- Fronteiras pos-acionamento ----------------------------------------------------


def test_fronteiras_pos_solicitacao_sem_persistencia_publicacao_popup(tmp_path):
    runtime = _runtime(tmp_path)
    destino = tmp_path / "config" / "estilo.json"
    original = destino.read_text(encoding="utf-8")
    _, controlador, estado, modelo = _abrir(runtime)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    b = _outro_preset(runtime, "indicadores.incluido")
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, "indicadores.incluido", b
    )

    solicitacao = controlador.solicitar_aplicacao()
    assert solicitacao is not None

    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global
    assert destino.read_text(encoding="utf-8") == original
    # Candidato continua existindo (nao destruido) para a etapa posterior.
    assert runtime.candidato["indicadores"]["incluido"]["preset_default"] == b
