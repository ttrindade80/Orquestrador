"""Testes focais H-0067 — envelope de confirmacao a partir da solicitacao."""

from __future__ import annotations

import copy
from pathlib import Path

from tela.estilo import (
    ControladorTelaEstilo,
    ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO,
    SolicitacaoAplicacaoEstilo,
)
from tela.loader import RuntimeEstilo, carregar_tela
from tela.modelo import construir_modelo
from tela.renderizacao import popup


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


def test_id_popup_e_declaracao_estrutural_tipo_texto():
    modelo = _modelo_estilo()
    assert ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO in modelo._raw["popups"]
    declaracao = popup.resolver_popup(
        modelo, ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO
    )
    assert declaracao["tipo"] == "texto"
    teclas = [chip["tecla"] for chip in declaracao["chips"]]
    assert teclas == ["Esc", "Enter"]
    assert declaracao["chips"][0]["texto"] == "Voltar"
    assert declaracao["chips"][1]["texto"] == "Confirmar"


def test_envelope_derivado_da_solicitacao_sem_reconsultar_candidato(tmp_path):
    runtime = _runtime(tmp_path)
    _, controlador, _, modelo = _abrir(runtime)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    original = (tmp_path / "config" / "estilo.json").read_text(encoding="utf-8")

    from tela.carregamento.estilo import definir_preset_candidato

    proposta = copy.deepcopy(runtime.candidato)
    definir_preset_candidato(
        proposta, ("borda", "preset_default"), _outro_preset(runtime, "borda")
    )
    runtime.materializar_local(proposta)
    solicitacao = controlador.solicitar_aplicacao()
    assert isinstance(solicitacao, SolicitacaoAplicacaoEstilo)

    envelope = ControladorTelaEstilo.conteudo_popup_confirmacao(solicitacao)
    assert envelope["tipo"] == "texto"
    assert isinstance(envelope["texto"], str) and envelope["texto"]
    assert "\n" not in envelope["texto"]
    assert set(envelope) == {"tipo", "texto"}

    # Envelope nao depende de mutacao posterior do runtime.
    proposta2 = copy.deepcopy(runtime.candidato)
    definir_preset_candidato(
        proposta2,
        ("chip", "preset_default"),
        _outro_preset(runtime, "chip"),
    )
    runtime.materializar_local(proposta2)
    envelope2 = ControladorTelaEstilo.conteudo_popup_confirmacao(solicitacao)
    assert envelope2 == envelope

    instancia = popup.abrir_popup(
        modelo, ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO, envelope
    )
    assert instancia.conteudo == envelope
    assert popup.consumir_tecla_popup(instancia, "\r") == {"status": "CONFIRMADO"}

    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert (tmp_path / "config" / "estilo.json").read_text(encoding="utf-8") == original


def test_solicitar_aplicacao_inativa_nao_produz_envelope():
    _, controlador, _, _ = _abrir()
    assert controlador.aplicar_disponivel is False
    assert controlador.solicitar_aplicacao() is None
