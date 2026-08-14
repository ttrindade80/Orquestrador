"""Testes focais H-0068 — orquestracao da aplicacao definitiva no controlador."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tela.carregamento.estilo import definir_preset_candidato
from tela.carregamento.erros import EstiloErro
from tela.estilo import (
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


def _runtime(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    return RuntimeEstilo(tmp_path), destino


def _modelo_estilo():
    return construir_modelo(carregar_tela(None, ID_TELA, RAIZ_TELAS_DEMO))


def _abrir(tmp_path):
    runtime, destino = _runtime(tmp_path)
    controlador = ControladorTelaEstilo(runtime)
    modelo = controlador.aplicar_ao_modelo(_modelo_estilo())
    estado = controlador.inicializar_estado(
        {
            "cursores": {},
            "selecoes": {},
            "foco_console": 0,
            "estilo": runtime.global_vigente,
        },
        modelo,
    )
    return runtime, controlador, estado, modelo, destino


def _outro_preset(runtime, categoria):
    secao = _em(runtime.candidato, _CAMINHOS[categoria])
    atual = secao["preset_default"]
    for nome in secao["presets"]:
        if nome != atual:
            return nome
    raise AssertionError("categoria sem preset alternativo: " + categoria)


def _divergir(controlador, estado, modelo, runtime, *categorias):
    for categoria in categorias:
        alvo = _outro_preset(runtime, categoria)
        estado = controlador.aplicar_espaco_filho_invalido(
            estado, modelo, categoria, alvo
        )
    return estado


def test_sucesso_persistencia_publicacao_baseline_reconciliacao(tmp_path):
    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]

    estado = _divergir(controlador, estado, modelo, runtime, "borda")
    assert controlador.aplicar_disponivel is True
    solicitacao = controlador.solicitar_aplicacao()
    assert isinstance(solicitacao, SolicitacaoAplicacaoEstilo)
    candidato_confirmado = copy.deepcopy(solicitacao.candidato)

    estado, materializacao = controlador.aplicar_solicitacao_confirmada(
        solicitacao, estado, modelo
    )

    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == candidato_confirmado
    assert persistido != json.loads(original)
    assert runtime.baseline == candidato_confirmado
    assert runtime.candidato == candidato_confirmado
    assert runtime.global_vigente is materializacao
    assert runtime.global_vigente != global_antes
    assert runtime.baseline != baseline_antes
    assert controlador.aplicar_disponivel is False
    assert runtime.comparar_candidato_baseline() is True
    assert controlador.invariavel_candidato_selecoes(estado, modelo)
    assert estado["estilo"] is estilo_antes
    assert destino.read_text(encoding="utf-8") != original


def test_snapshot_confirmado_e_autoridade_nao_runtime_candidato(tmp_path):
    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    estado = _divergir(controlador, estado, modelo, runtime, "borda")
    solicitacao = controlador.solicitar_aplicacao()
    snapshot_b = copy.deepcopy(solicitacao.candidato)
    preset_b = snapshot_b["borda"]["preset_default"]

    proposta_c = copy.deepcopy(runtime.candidato)
    definir_preset_candidato(
        proposta_c,
        ("chip", "preset_default"),
        _outro_preset(runtime, "chip"),
    )
    runtime.materializar_local(proposta_c)
    preset_c_chip = runtime.candidato["chip"]["preset_default"]
    assert runtime.candidato != snapshot_b

    chamadas = []
    original = runtime.aplicar_candidato

    def _rastrear(candidato, caminho_destino):
        chamadas.append((copy.deepcopy(candidato), caminho_destino))
        return original(candidato, caminho_destino)

    runtime.aplicar_candidato = _rastrear
    estado, materializacao = controlador.aplicar_solicitacao_confirmada(
        solicitacao, estado, modelo
    )

    assert len(chamadas) == 1
    assert chamadas[0][0] == snapshot_b
    assert chamadas[0][1] == runtime.caminho_destino
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == snapshot_b
    assert persistido["borda"]["preset_default"] == preset_b
    assert persistido["chip"]["preset_default"] != preset_c_chip
    assert runtime.baseline == snapshot_b
    assert runtime.candidato == snapshot_b
    assert runtime.global_vigente is materializacao
    assert solicitacao.candidato == snapshot_b


def test_falha_persistencia_fail_closed_descarta_tentativa(tmp_path, monkeypatch):
    import tela.carregamento.estilo as modulo_estilo

    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]

    estado = _divergir(controlador, estado, modelo, runtime, "borda")
    solicitacao = controlador.solicitar_aplicacao()
    estado["solicitacao_aplicacao_estilo"] = solicitacao
    candidato_tentado = copy.deepcopy(solicitacao.candidato)

    def persistir_falha(candidato, caminho_destino):
        raise EstiloErro("falha controlada de persistencia")

    monkeypatch.setattr(
        modulo_estilo, "persistir_configuracao_estilo", persistir_falha
    )

    with pytest.raises(EstiloErro, match="falha controlada"):
        controlador.aplicar_solicitacao_confirmada(solicitacao, estado, modelo)

    assert destino.read_text(encoding="utf-8") == original
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["estilo"] is estilo_antes
    assert runtime.candidato == candidato_tentado
    assert controlador.aplicar_disponivel is True
    estado.pop("solicitacao_aplicacao_estilo", None)
    assert "solicitacao_aplicacao_estilo" not in estado


def test_ausencia_de_solicitacao_valida_e_noop(tmp_path):
    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado2, materializacao = controlador.aplicar_solicitacao_confirmada(
        None, estado, modelo
    )
    assert materializacao is None
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert estado2["selecoes"] == estado["selecoes"]


def test_duas_categorias_no_mesmo_candidato_confirmado(tmp_path):
    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    estado = _divergir(controlador, estado, modelo, runtime, "borda", "chip")
    solicitacao = controlador.solicitar_aplicacao()
    esperado = copy.deepcopy(solicitacao.candidato)
    assert (
        esperado["borda"]["preset_default"]
        != runtime.baseline["borda"]["preset_default"]
    )
    assert (
        esperado["chip"]["preset_default"]
        != json.loads(destino.read_text(encoding="utf-8"))["chip"]["preset_default"]
    )

    estado, materializacao = controlador.aplicar_solicitacao_confirmada(
        solicitacao, estado, modelo
    )
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == esperado
    assert persistido["borda"]["preset_default"] == esperado["borda"]["preset_default"]
    assert persistido["chip"]["preset_default"] == esperado["chip"]["preset_default"]
    assert runtime.baseline == esperado
    assert runtime.candidato == esperado
    assert runtime.global_vigente is materializacao
    assert controlador.aplicar_disponivel is False
    assert controlador.invariavel_candidato_selecoes(estado, modelo)


def test_nao_cria_segunda_primitiva_de_persistencia(tmp_path):
    runtime, controlador, estado, modelo, destino = _abrir(tmp_path)
    estado = _divergir(controlador, estado, modelo, runtime, "borda")
    solicitacao = controlador.solicitar_aplicacao()

    chamadas = []
    original = runtime.aplicar_candidato

    def _rastrear(candidato, caminho_destino):
        chamadas.append((copy.deepcopy(candidato), caminho_destino))
        return original(candidato, caminho_destino)

    runtime.aplicar_candidato = _rastrear
    controlador.aplicar_solicitacao_confirmada(solicitacao, estado, modelo)
    assert len(chamadas) == 1
    assert chamadas[0][0] == solicitacao.candidato
    assert chamadas[0][1] == runtime.caminho_destino
    assert chamadas[0][1] == destino
