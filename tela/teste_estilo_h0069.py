"""Testes focais H-0069 — materializacao local isolada (ADR-0046 secao 5).

Cobre exclusivamente a propriedade de isolamento de que a demonstracao
integrada depende: ``EstadoEstiloRuntime.materializar_local`` (ja entregue
por H-0061/H-0066, reutilizada sem alteracao) produz uma materializacao do
candidato sem tocar ``baseline`` nem ``global_vigente``, e sem persistir em
``config/estilo.json``. Nao testa a UI da demonstracao (ver
``demo/teste_demo_estilo_h0069.py``); nao altera ``tela/carregamento/
estilo.py`` nem ``tela/estilo.py``.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from tela.carregamento.estilo import definir_preset_candidato
from tela.loader import RuntimeEstilo


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


def _runtime(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    return RuntimeEstilo(tmp_path), destino


def _outro_preset(runtime, categoria):
    secao = _em(runtime.candidato, _CAMINHOS[categoria])
    atual = secao["preset_default"]
    for nome in secao["presets"]:
        if nome != atual:
            return nome
    raise AssertionError("categoria sem preset alternativo: " + categoria)


def _candidato_divergente(runtime, *categorias):
    proposta = copy.deepcopy(runtime.candidato)
    alvos = {}
    for categoria in categorias:
        alvo = _outro_preset(runtime, categoria)
        alvos[categoria] = alvo
        definir_preset_candidato(
            proposta, _CAMINHOS[categoria] + ("preset_default",), alvo
        )
    return proposta, alvos


def test_materializar_local_reflete_candidato_sem_tocar_global_nem_baseline(
    tmp_path,
):
    runtime, destino = _runtime(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    original = destino.read_text(encoding="utf-8")

    proposta, alvos = _candidato_divergente(runtime, "borda")
    materializacao = runtime.materializar_local(proposta)

    assert materializacao.canto_superior_esquerdo != (
        global_antes.canto_superior_esquerdo
    )
    assert runtime.global_vigente is global_antes
    assert runtime.baseline == baseline_antes
    assert destino.read_text(encoding="utf-8") == original
    assert alvos["borda"] == proposta["borda"]["preset_default"]


def test_materializar_local_nao_persiste_em_config_estilo(tmp_path):
    runtime, destino = _runtime(tmp_path)
    original = destino.read_text(encoding="utf-8")
    proposta, _ = _candidato_divergente(runtime, "chip")

    runtime.materializar_local(proposta)

    assert destino.read_text(encoding="utf-8") == original
    assert json.loads(original) == runtime.baseline


def test_materializar_local_nao_cria_segundo_runtime(tmp_path):
    runtime, _ = _runtime(tmp_path)
    proposta, _ = _candidato_divergente(runtime, "indicadores.selecionado")

    materializacao = runtime.materializar_local(proposta)

    # Mesma instancia de runtime; nenhuma segunda materializacao global
    # existe fora do valor de retorno desta chamada.
    assert runtime.materializacao_global is runtime.global_vigente
    assert runtime.materializacao_global is not materializacao


def test_duas_categorias_simultaneas_na_materializacao_local(tmp_path):
    runtime, _ = _runtime(tmp_path)
    global_antes = runtime.global_vigente
    proposta, alvos = _candidato_divergente(runtime, "chip", "indicadores.incluido")

    materializacao = runtime.materializar_local(proposta)

    assert materializacao.caractere_esquerdo != global_antes.caractere_esquerdo or (
        materializacao.caractere_direito != global_antes.caractere_direito
    )
    assert (
        materializacao.incluido_on != global_antes.incluido_on
        or materializacao.incluido_off != global_antes.incluido_off
    )
    assert runtime.global_vigente is global_antes
    assert runtime.baseline == json.loads(
        (tmp_path / "config" / "estilo.json").read_text(encoding="utf-8")
    )


def test_apos_descarte_materializacao_local_nao_sobrevive(tmp_path):
    """Equivalente de ABORTADO no nivel do runtime: descarte da tentativa."""
    runtime, destino = _runtime(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    proposta, _ = _candidato_divergente(runtime, "borda")
    runtime.materializar_local(proposta)

    # Saida efetiva da visita (H-0065): candidato recriado a partir da
    # baseline vigente; a materializacao local da tentativa nao persiste.
    candidato_reiniciado = runtime.criar_candidato()

    assert candidato_reiniciado == baseline_antes
    assert runtime.global_vigente is global_antes
    assert runtime.baseline == baseline_antes
    assert destino.read_text(encoding="utf-8") == CONFIG_ESTILO.read_text(
        encoding="utf-8"
    )
