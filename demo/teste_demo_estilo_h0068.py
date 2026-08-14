"""Testes de integracao H-0068 — aplicacao definitiva apos CONFIRMADO."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

from tela.carregamento.erros import EstiloErro
from tela.estilo import SolicitacaoAplicacaoEstilo
from tela.loader import RuntimeEstilo


_SPEC = importlib.util.spec_from_file_location(
    "demo_h0068_mod", Path(__file__).with_name("demo.py")
)
_DEMO = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_DEMO)

TECLA_F4 = _DEMO.TECLA_F4
_ID_TELA_H0063 = _DEMO._ID_TELA_H0063
_carregar_modelo_por_id = _DEMO._carregar_modelo_por_id
_preparar_modelo_estilo = _DEMO._preparar_modelo_estilo
_preparar_estado_estilo = _DEMO._preparar_estado_estilo
_anexar_tela_estilo = _DEMO._anexar_tela_estilo
criar_estado_inicial = _DEMO.criar_estado_inicial
processar_comando = _DEMO.processar_comando

RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"

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


def _estado_base(runtime):
    return dict(
        criar_estado_inicial(),
        estilo_runtime=runtime,
        estilo=runtime.global_vigente,
    )


def _abrir(runtime):
    estado = _estado_base(runtime)
    modelo = _carregar_modelo_por_id("demo")
    estado = processar_comando(estado, TECLA_F4, modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)
    return estado, modelo


def _entrar_e_selecionar_proximo_filho(estado, modelo):
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    return estado


def _runtime_tmp(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    return RuntimeEstilo(tmp_path), destino


def _abrir_confirmacao(tmp_path):
    runtime, destino = _runtime_tmp(tmp_path)
    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert estado["tela_estilo"].aplicar_disponivel is True
    estado = processar_comando(estado, "\r", modelo)
    return estado, modelo, runtime, destino


def test_sucesso_completo_confirmado_aplica_e_sincroniza(tmp_path):
    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    candidato_confirmado = copy.deepcopy(solicitacao.candidato)
    estilo_antes = estado["estilo"]
    assert estado["tela_estilo"].aplicar_disponivel is True

    estado = processar_comando(estado, "\r", modelo)

    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == candidato_confirmado
    assert runtime.baseline == candidato_confirmado
    assert runtime.candidato == candidato_confirmado
    assert runtime.global_vigente is estado["estilo"]
    assert estado["estilo"] is not estilo_antes
    assert estado["tela_estilo"].aplicar_disponivel is False
    assert estado["tela_estilo"].invariavel_candidato_selecoes(estado, modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063


def test_abortado_nao_aplica(tmp_path):
    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]
    candidato_antes = copy.deepcopy(runtime.candidato)

    estado = processar_comando(estado, "\x1b", modelo)

    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["estilo"] is estilo_antes
    assert runtime.candidato == candidato_antes
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert estado["tela_atual"] == _ID_TELA_H0063


def test_ausencia_de_solicitacao_valida_nao_aplica(tmp_path):
    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]
    estado = dict(estado)
    estado.pop("solicitacao_aplicacao_estilo")

    estado = processar_comando(estado, "\r", modelo)

    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["estilo"] is estilo_antes
    assert estado.get("solicitacao_aplicacao_estilo") is None


def test_aplicar_inativo_nao_aplica(tmp_path):
    runtime, destino = _runtime_tmp(tmp_path)
    original = destino.read_text(encoding="utf-8")
    estado, modelo = _abrir(runtime)
    assert estado["tela_estilo"].aplicar_disponivel is False
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado = processar_comando(estado, "\r", modelo)

    assert estado.get("popup") is None
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes


def test_snapshot_da_solicitacao_e_autoridade(tmp_path):
    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    snapshot_b = copy.deepcopy(solicitacao.candidato)

    from tela.carregamento.estilo import definir_preset_candidato

    proposta_c = copy.deepcopy(runtime.candidato)
    secao_chip = _em(proposta_c, _CAMINHOS["chip"])
    atual = secao_chip["preset_default"]
    outro = next(nome for nome in secao_chip["presets"] if nome != atual)
    definir_preset_candidato(proposta_c, ("chip", "preset_default"), outro)
    runtime.materializar_local(proposta_c)
    assert runtime.candidato != snapshot_b

    estado = processar_comando(estado, "\r", modelo)

    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == snapshot_b
    assert runtime.baseline == snapshot_b
    assert runtime.candidato == snapshot_b
    assert runtime.global_vigente is estado["estilo"]
    assert solicitacao.candidato == snapshot_b
    assert estado.get("solicitacao_aplicacao_estilo") is None


def test_falha_persistencia_fail_closed_sem_escapar_do_dispatch(
    tmp_path, monkeypatch
):
    import tela.carregamento.estilo as modulo_estilo

    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    original = destino.read_text(encoding="utf-8")
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    candidato_tentado = copy.deepcopy(solicitacao.candidato)

    def persistir_falha(candidato, caminho_destino):
        raise EstiloErro("falha controlada de persistencia")

    monkeypatch.setattr(
        modulo_estilo, "persistir_configuracao_estilo", persistir_falha
    )

    estado = processar_comando(estado, "\r", modelo)

    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["estilo"] is estilo_antes
    assert runtime.candidato == candidato_tentado
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert estado["tela_atual"] == _ID_TELA_H0063


def test_duas_categorias_simultaneas_no_documento_aplicado(tmp_path):
    runtime, destino = _runtime_tmp(tmp_path)
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    baseline_doc = json.loads(destino.read_text(encoding="utf-8"))

    alvos = {}
    for categoria in ("borda", "chip"):
        secao = _em(runtime.candidato, _CAMINHOS[categoria])
        atual = secao["preset_default"]
        outro = next(nome for nome in secao["presets"] if nome != atual)
        alvos[categoria] = outro
        estado = controlador.aplicar_espaco_filho_invalido(
            estado, modelo, categoria, outro
        )

    assert controlador.aplicar_disponivel is True
    estado = processar_comando(estado, "\r", modelo)
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    esperado = copy.deepcopy(solicitacao.candidato)
    estado = processar_comando(estado, "\r", modelo)

    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == esperado
    assert persistido["borda"]["preset_default"] == alvos["borda"]
    assert persistido["chip"]["preset_default"] == alvos["chip"]
    assert persistido["borda"]["preset_default"] != baseline_doc["borda"]["preset_default"]
    assert persistido["chip"]["preset_default"] != baseline_doc["chip"]["preset_default"]
    assert runtime.baseline == esperado
    assert runtime.candidato == esperado
    assert runtime.global_vigente is estado["estilo"]
    assert estado["tela_estilo"].aplicar_disponivel is False
    assert estado.get("solicitacao_aplicacao_estilo") is None


def test_regressao_confirmado_agora_persiste(tmp_path):
    """Reestrutura a fronteira H-0067: CONFIRMADO aplica de fato."""
    estado, modelo, runtime, destino = _abrir_confirmacao(tmp_path)
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert "valor" not in estado["popup_resultado"]
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert json.loads(destino.read_text(encoding="utf-8")) == solicitacao.candidato
    assert runtime.baseline == solicitacao.candidato
    assert runtime.global_vigente is estado["estilo"]
    assert estado["tela_estilo"].aplicar_disponivel is False
    assert estado["tela_atual"] == _ID_TELA_H0063
