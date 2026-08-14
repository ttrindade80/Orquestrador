"""Testes focais H-0065 — vinculacao escolha ↔ candidato de estilo."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
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


def _runtime(tmp_path=None, mutar=None):
    if tmp_path is None and mutar is None:
        return RuntimeEstilo()
    configuracao = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    if mutar is not None:
        mutar(configuracao)
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(configuracao, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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
    raise AssertionError("categoria sem terceiro preset: " + categoria)


def _preset_candidato(runtime, categoria):
    return _em(runtime.candidato, _CAMINHOS[categoria])["preset_default"]


def _preset_baseline(runtime, categoria):
    return _em(runtime.baseline, _CAMINHOS[categoria])["preset_default"]


def test_abertura_cria_candidato_da_baseline_e_selecoes_correspondem():
    runtime = RuntimeEstilo()
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    _, controlador, estado, modelo = _abrir(runtime)

    assert runtime.candidato == baseline
    assert runtime.comparar_candidato_baseline()
    assert controlador.escolhas_de(estado, modelo) == controlador.escolhas_iniciais
    assert controlador.escolhas_de(estado, modelo) == controlador.presets_do_candidato()
    assert controlador.invariavel_candidato_selecoes(estado, modelo)
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes


@pytest.mark.parametrize("categoria", CATEGORIAS_ESTILO)
def test_espaco_atomico_quatro_categorias(categoria, tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    _, controlador, estado, modelo = _abrir(runtime)

    presets_antes = controlador.presets_do_candidato()
    alvo = _outro_preset(runtime, categoria)
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, categoria, alvo
    )

    depois = controlador.presets_do_candidato()
    assert depois[categoria] == alvo
    assert controlador.escolhas_de(estado, modelo)[categoria] == alvo
    for outra in CATEGORIAS_ESTILO:
        if outra != categoria:
            assert depois[outra] == presets_antes[outra]
            assert controlador.escolhas_de(estado, modelo)[outra] == presets_antes[outra]
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert controlador.invariavel_candidato_selecoes(estado, modelo)


def test_troca_sucessiva_a_b_c():
    runtime, controlador, estado, modelo = _abrir()
    a = _preset_candidato(runtime, "borda")
    b = _outro_preset(runtime, "borda")
    c = _terceiro_preset(runtime, "borda", {a, b})

    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert _preset_candidato(runtime, "borda") == b
    assert controlador.escolhas_de(estado, modelo)["borda"] == b

    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", c)
    assert _preset_candidato(runtime, "borda") == c
    assert controlador.escolhas_de(estado, modelo)["borda"] == c
    assert controlador.invariavel_candidato_selecoes(estado, modelo)


def test_pais_independentes_acumulam():
    runtime, controlador, estado, modelo = _abrir()
    b1 = _outro_preset(runtime, "borda")
    c1 = _outro_preset(runtime, "chip")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b1)
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "chip", c1)
    assert _preset_candidato(runtime, "borda") == b1
    assert _preset_candidato(runtime, "chip") == c1
    escolhas = controlador.escolhas_de(estado, modelo)
    assert escolhas["borda"] == b1
    assert escolhas["chip"] == c1


def test_preset_invalido_preserva_candidato_e_selecoes(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    _, controlador, estado, modelo = _abrir(runtime)
    a = _preset_candidato(runtime, "borda")
    candidato_antes = copy.deepcopy(runtime.candidato)
    escolhas_antes = dict(controlador.escolhas_de(estado, modelo))

    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, "borda", "Preset Inexistente XYZ"
    )

    assert runtime.candidato == candidato_antes
    assert _preset_candidato(runtime, "borda") == a
    assert controlador.escolhas_de(estado, modelo) == escolhas_antes
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original


def test_divergencia_artificial_reconcilia_a_favor_do_candidato():
    runtime, controlador, estado, modelo = _abrir()
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    console = controlador.console_do_modelo(modelo)
    # Divergencia artificial: selecoes volta para A enquanto candidato=B.
    a = _preset_baseline(runtime, "borda")
    selecoes = dict(estado["selecoes"])
    ids = list(selecoes[console.id])
    ids[0] = "estilo.borda.{0}".format(a)
    selecoes[console.id] = ids
    estado = dict(estado, selecoes=selecoes)
    assert controlador.escolhas_de(estado, modelo)["borda"] == a
    assert _preset_candidato(runtime, "borda") == b

    estado = controlador.reconciliar_selecoes_com_candidato(estado, modelo)
    assert controlador.escolhas_de(estado, modelo)["borda"] == b
    assert _preset_candidato(runtime, "borda") == b


def test_resize_redraw_preserva_candidato_e_selecoes():
    runtime, controlador, estado, modelo = _abrir()
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    estado = controlador.reconciliar_selecoes_com_candidato(estado, modelo)
    assert _preset_candidato(runtime, "borda") == b
    assert controlador.escolhas_de(estado, modelo)["borda"] == b
    # Recomposicao (como prepare/redraw) nao perde mutacao candidata.
    estado = controlador.reconciliar_selecoes_com_candidato(estado, modelo)
    assert _preset_candidato(runtime, "borda") == b
    assert controlador.escolhas_de(estado, modelo)["borda"] == b


def test_saida_efetiva_restaura_baseline_candidato_selecoes_imediatamente(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    _, controlador, estado, modelo = _abrir(runtime)
    a = _preset_baseline(runtime, "borda")
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert _preset_candidato(runtime, "borda") == b

    estado = controlador.descartar_visita(estado, modelo)

    assert _preset_baseline(runtime, "borda") == a
    assert _preset_candidato(runtime, "borda") == a
    assert controlador.escolhas_de(estado, modelo)["borda"] == a
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.comparar_candidato_baseline()


def test_saida_multi_categoria():
    runtime, controlador, estado, modelo = _abrir()
    borda_a = _preset_baseline(runtime, "borda")
    chip_a = _preset_baseline(runtime, "chip")
    borda_b = _outro_preset(runtime, "borda")
    chip_d = _outro_preset(runtime, "chip")
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, "borda", borda_b
    )
    estado = controlador.aplicar_espaco_filho_invalido(
        estado, modelo, "chip", chip_d
    )
    estado = controlador.descartar_visita(estado, modelo)
    assert _preset_candidato(runtime, "borda") == borda_a
    assert _preset_candidato(runtime, "chip") == chip_a
    escolhas = controlador.escolhas_de(estado, modelo)
    assert escolhas["borda"] == borda_a
    assert escolhas["chip"] == chip_a


def test_saida_corrige_cache_divergente():
    runtime, controlador, estado, modelo = _abrir()
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    # Simula candidato ja restaurado com selecoes ainda antigo.
    runtime.criar_candidato()
    assert _preset_candidato(runtime, "borda") == _preset_baseline(runtime, "borda")
    console = controlador.console_do_modelo(modelo)
    selecoes = dict(estado["selecoes"])
    selecoes[console.id] = list(selecoes[console.id])
    selecoes[console.id][0] = "estilo.borda.{0}".format(b)
    estado = dict(estado, selecoes=selecoes)
    assert controlador.escolhas_de(estado, modelo)["borda"] == b

    estado = controlador.descartar_visita(estado, modelo)
    a = _preset_baseline(runtime, "borda")
    assert _preset_candidato(runtime, "borda") == a
    assert controlador.escolhas_de(estado, modelo)["borda"] == a


def test_f4_defensivo_apos_saida():
    runtime, controlador, estado, modelo = _abrir()
    b = _outro_preset(runtime, "borda")
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    estado = controlador.descartar_visita(estado, modelo)
    a = _preset_baseline(runtime, "borda")
    assert _preset_candidato(runtime, "borda") == a
    assert controlador.escolhas_de(estado, modelo)["borda"] == a

    # Nova visita (equivalente a F4): cria candidato e reconcilia.
    controlador2 = ControladorTelaEstilo(runtime)
    modelo2 = controlador2.aplicar_ao_modelo(_modelo_estilo())
    estado2 = controlador2.inicializar_estado(
        {"cursores": {}, "selecoes": {}, "foco_console": 0},
        modelo2,
    )
    assert _preset_candidato(runtime, "borda") == a
    assert controlador2.escolhas_de(estado2, modelo2)["borda"] == a
    assert runtime.comparar_candidato_baseline()


def test_sem_aplicar_persistencia_ou_publicacao():
    runtime, controlador, estado, modelo = _abrir()
    # H-0066: solicitar_aplicacao passa a existir (capacidade compartilhada);
    # a edicao por Espaco continua sem persistir/publicar por si so.
    assert hasattr(controlador, "solicitar_aplicacao")
    b = _outro_preset(runtime, "borda")
    global_antes = runtime.global_vigente
    estado = controlador.aplicar_espaco_filho_invalido(estado, modelo, "borda", b)
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global
