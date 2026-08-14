"""Testes focais F4 / Espaco / saida efetiva H-0065 sem TTY."""

from __future__ import annotations

import copy
import io
import json
import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "demo_h0065_mod", Path(__file__).with_name("demo.py")
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
renderizar_estado = _DEMO.renderizar_estado
main = _DEMO.main

from tela.estilo import CATEGORIAS_ESTILO
from tela.loader import RuntimeEstilo
from tela import navegacao


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


def _preset(runtime, fonte, categoria):
    doc = runtime.baseline if fonte == "baseline" else runtime.candidato
    return _em(doc, _CAMINHOS[categoria])["preset_default"]


def _estado_base(runtime=None):
    runtime = runtime or RuntimeEstilo()
    return dict(
        criar_estado_inicial(),
        estilo_runtime=runtime,
        estilo=runtime.global_vigente,
    )


def _abrir(runtime=None):
    estado = _estado_base(runtime)
    modelo = _carregar_modelo_por_id("demo")
    estado = processar_comando(estado, TECLA_F4, modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)
    return estado, modelo


def _quadro(estado, modelo, largura=100, altura=28):
    return renderizar_estado(estado, modelo, largura=largura, altura=altura)


def _entrar_e_selecionar_proximo_filho(estado, modelo):
    estado = processar_comando(estado, " ", modelo)  # entra nos filhos
    estado = processar_comando(estado, "\x1b[B", modelo)  # proximo
    estado = processar_comando(estado, " ", modelo)  # Espaco seletor
    return estado


def test_f4_cria_candidato_da_baseline_e_selecoes_correspondem():
    runtime = RuntimeEstilo()
    baseline = copy.deepcopy(runtime.baseline)
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    assert runtime.candidato == baseline
    assert controlador.escolhas_de(estado, modelo) == controlador.presets_do_candidato()
    assert controlador.invariavel_candidato_selecoes(estado, modelo)


def test_setas_nao_mutam_candidato_nem_escolhido():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    candidato_antes = copy.deepcopy(runtime.candidato)
    escolhas_antes = dict(controlador.escolhas_de(estado, modelo))

    estado = processar_comando(estado, " ", modelo)
    filho_antes = controlador.filho_corrente(estado, modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    filho_depois = controlador.filho_corrente(estado, modelo)
    assert filho_depois is not None and filho_antes is not None
    assert filho_depois.id != filho_antes.id
    assert runtime.candidato == candidato_antes
    assert controlador.escolhas_de(estado, modelo) == escolhas_antes


def test_espaco_atualiza_candidato_e_selecoes_borda(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    a = _preset(runtime, "candidato", "borda")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = controlador.escolhas_de(estado, modelo)["borda"]
    assert b != a
    assert _preset(runtime, "candidato", "borda") == b
    assert _preset(runtime, "baseline", "borda") == a
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert estado.get("popup") is None


def test_troca_sucessiva_e_pais_independentes():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    # borda A→B
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    borda_b = controlador.escolhas_de(estado, modelo)["borda"]
    assert _preset(runtime, "candidato", "borda") == borda_b
    # Esc aos pais, ir ao chip, selecionar outro
    estado = processar_comando(estado, "\x1b", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    chip_c = controlador.escolhas_de(estado, modelo)["chip"]
    assert _preset(runtime, "candidato", "chip") == chip_c
    assert _preset(runtime, "candidato", "borda") == borda_b
    assert controlador.escolhas_de(estado, modelo)["borda"] == borda_b


def test_esc_filho_preserva_candidato_e_selecoes():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    a = _preset(runtime, "baseline", "borda")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = _preset(runtime, "candidato", "borda")
    assert b != a
    escolhidas = dict(controlador.escolhas_de(estado, modelo))
    estado = processar_comando(estado, "\x1b", modelo)
    console = controlador.console_do_modelo(modelo)
    assert not navegacao.em_nivel_filhos(estado, console)
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert _preset(runtime, "candidato", "borda") == b
    assert _preset(runtime, "baseline", "borda") == a
    assert controlador.escolhas_de(estado, modelo) == escolhidas


def test_saida_efetiva_restaura_antes_de_qualquer_f4(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estado, modelo = _abrir(runtime)
    a = _preset(runtime, "baseline", "borda")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = _preset(runtime, "candidato", "borda")
    assert b != a
    estado = processar_comando(estado, "\x1b", modelo)  # pais
    estado = processar_comando(estado, "\x1b", modelo)  # saida efetiva

    # Imediatamente, antes de F4:
    assert estado["tela_atual"] == "demo"
    assert _preset(runtime, "baseline", "borda") == a
    assert _preset(runtime, "candidato", "borda") == a
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.comparar_candidato_baseline()


def test_f4_depois_da_saida_mantem_coerencia():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    a = _preset(runtime, "baseline", "borda")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert _preset(runtime, "candidato", "borda") != a
    estado = processar_comando(estado, "\x1b", modelo)
    estado = processar_comando(estado, "\x1b", modelo)
    assert _preset(runtime, "candidato", "borda") == a

    modelo_demo = _carregar_modelo_por_id("demo")
    estado = processar_comando(estado, TECLA_F4, modelo_demo)
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)
    controlador = estado["tela_estilo"]
    assert _preset(runtime, "candidato", "borda") == a
    assert controlador.escolhas_de(estado, modelo)["borda"] == a


def test_resize_preserva_candidato_apos_espaco():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = _preset(runtime, "candidato", "borda")
    escolhidas = dict(controlador.escolhas_de(estado, modelo))
    for largura, altura in ((120, 40), (80, 24), (62, 20)):
        _quadro(estado, modelo, largura=largura, altura=altura)
        estado = _preparar_estado_estilo(estado, modelo)
        assert _preset(runtime, "candidato", "borda") == b
        assert controlador.escolhas_de(estado, modelo) == escolhidas


def test_demonstracao_non_tty_ciclo_completo(monkeypatch, tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    # Espaco entra, seta, Espaco escolhe, Esc pais, Esc sai.
    entrada = io.StringIO(" \n\x1b[B\n \n\x1b\n\x1b\n")
    saida = io.StringIO()
    monkeypatch.setattr(_DEMO.sys, "stdin", entrada)
    monkeypatch.setattr(_DEMO.sys, "stdout", saida)

    codigo = main(
        ["demo.py", "demo"],
        estado_inicial=dict(
            criar_estado_inicial(),
            estilo_runtime=runtime,
            estilo=runtime.global_vigente,
            tela_atual="demo",
            largura=100,
            altura=30,
        ),
    )
    # Sem F4 na entrada: apenas prova ausencia de Aplicar/popup no quadro demo.
    assert codigo == 0
    texto = saida.getvalue()
    assert "Aplicar" not in texto
    assert "CONFIRMADO" not in texto
    assert "ABORTADO" not in texto

    # Ciclo com F4 via processar_comando (caminho real).
    estado, modelo = _abrir(runtime)
    assert runtime.candidato == baseline
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert _preset(runtime, "candidato", "borda") != _preset(
        runtime, "baseline", "borda"
    )
    quadro = _quadro(estado, modelo)
    # H-0066: candidato ja diverge (Espaco escolheu novo preset); Aplicar
    # aparece ATIVO. Sem Enter, nenhum popup/solicitacao e produzido.
    assert "Aplicar" in quadro
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert "popup" not in quadro.lower()
    assert estado.get("popup") is None
    assert estado.get("solicitacao_aplicacao_estilo") is None
    estado = processar_comando(estado, "\x1b", modelo)
    assert _preset(runtime, "candidato", "borda") != _preset(
        runtime, "baseline", "borda"
    )
    estado = processar_comando(estado, "\x1b", modelo)
    assert runtime.candidato == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original

    estado, modelo = _abrir(runtime)
    assert runtime.candidato == baseline
    assert estado["tela_estilo"].escolhas_de(estado, modelo)[
        "borda"
    ] == _preset(runtime, "baseline", "borda")


def test_aplicar_presente_ativo_sem_preview_real_no_quadro():
    """H-0066: Aplicar existe declarativamente; ativo quando candidato diverge."""
    runtime = RuntimeEstilo()
    global_antes = runtime.global_vigente
    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    quadro = _quadro(estado, modelo)
    chips = modelo.barra_de_menus["chips"]
    assert "Aplicar" in [c.get("texto", "") for c in chips]
    assert "Aplicar" in quadro
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert estado.get("popup") is None
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert "CONFIRMADO" not in quadro
    assert "ABORTADO" not in quadro
    # Sem preview real: global permanece o materializado da baseline.
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global
    assert not runtime.comparar_candidato_baseline()
