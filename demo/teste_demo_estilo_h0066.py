"""Testes focais F4 / Enter / Aplicar H-0066 sem TTY."""

from __future__ import annotations

import copy
import io
import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "demo_h0066_mod", Path(__file__).with_name("demo.py")
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

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo, SolicitacaoAplicacaoEstilo
from tela.loader import RuntimeEstilo
from tela import navegacao
from tela.renderizador import _navegacao_atual


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


def _estado_ativo_chip_aplicar():
    return _navegacao_atual["estado_ativo_chips"].get("chip_aplicar")


# --- Aplicar inativo (baseline == candidato) -----------------------------------


def test_aplicar_presente_inativo_enter_no_op_sem_solicitacao():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    assert controlador.aplicar_disponivel is False

    quadro = _quadro(estado, modelo)
    ids = [c["id"] for c in modelo.barra_de_menus["chips"]]
    assert "chip_aplicar" in ids
    assert "Aplicar" in quadro
    assert _estado_ativo_chip_aplicar() is False

    estado2 = processar_comando(estado, "\r", modelo)
    assert estado2.get("solicitacao_aplicacao_estilo") is None
    assert estado2["tela_atual"] == _ID_TELA_H0063
    assert estado2.get("popup") is None


# --- Aplicar ativo (baseline != candidato) --------------------------------------


def test_aplicar_presente_ativo_enter_produz_somente_solicitacao(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    controlador = estado["tela_estilo"]
    assert controlador.aplicar_disponivel is True

    quadro = _quadro(estado, modelo)
    assert "Aplicar" in quadro
    assert _estado_ativo_chip_aplicar() is True

    estado = processar_comando(estado, "\r", modelo)
    solicitacao = estado.get("solicitacao_aplicacao_estilo")
    assert isinstance(solicitacao, SolicitacaoAplicacaoEstilo)
    assert solicitacao.baseline == baseline_antes
    assert solicitacao.candidato == runtime.candidato

    # H-0067: Enter ativo abre popup de confirmacao no mesmo evento.
    assert estado.get("popup") is not None
    assert estado["popup"].id == "popup_confirmacao_aplicacao_estilo"
    assert estado["popup"].conteudo["tipo"] == "texto"
    assert estado.get("popup_resultado") is None
    # Ainda sem decisao: literais CONFIRMADO/ABORTADO nao sao estado de tela.
    assert "CONFIRMADO" not in quadro and "ABORTADO" not in quadro
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global
    assert destino.read_text(encoding="utf-8") == original


# --- Formula literal --------------------------------------------------------------


def test_formula_aplicar_disponivel_ponte_literal():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    assert controlador.aplicar_disponivel == (
        not runtime.comparar_candidato_baseline()
    )
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert controlador.aplicar_disponivel == (
        not runtime.comparar_candidato_baseline()
    )
    assert controlador.aplicar_disponivel != runtime.comparar_candidato_baseline()


# --- A -> B -> A -------------------------------------------------------------------


def test_a_b_a_inativo_ativo_inativo():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    assert controlador.aplicar_disponivel is False
    quadro = _quadro(estado, modelo)
    assert _estado_ativo_chip_aplicar() is False

    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert controlador.aplicar_disponivel is True
    quadro = _quadro(estado, modelo)
    assert _estado_ativo_chip_aplicar() is True

    # Espaco de volta ao preset original da baseline reverte a divergencia.
    a = _preset(estado["estilo_runtime"], "baseline", "borda")
    console = controlador.console_do_modelo(modelo)
    assert navegacao.em_nivel_filhos(estado, console)
    # Percorre os filhos de borda ate cair de volta no preset original.
    for _ in range(len(controlador.filhos["borda"])):
        atual = controlador.escolhas_de(estado, modelo)["borda"]
        if atual == a:
            break
        estado = processar_comando(estado, "\x1b[B", modelo)
        estado = processar_comando(estado, " ", modelo)
    assert controlador.escolhas_de(estado, modelo)["borda"] == a
    assert controlador.aplicar_disponivel is False
    quadro = _quadro(estado, modelo)
    assert _estado_ativo_chip_aplicar() is False


# --- Quatro categorias ---------------------------------------------------------------


def test_quatro_categorias_ativam_aplicar_via_dispatch(tmp_path):
    for categoria in CATEGORIAS_ESTILO:
        base = tmp_path / categoria.replace(".", "_")
        destino = base / "config" / "estilo.json"
        destino.parent.mkdir(parents=True)
        destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
        runtime = RuntimeEstilo(base)
        estado, modelo = _abrir(runtime)
        controlador = estado["tela_estilo"]
        assert controlador.aplicar_disponivel is False

        indice = CATEGORIAS_ESTILO.index(categoria)
        estado = processar_comando(estado, " ", modelo)
        for _ in range(indice):
            estado = processar_comando(estado, "\x1b", modelo)
            estado = processar_comando(estado, "\x1b[B", modelo)
            estado = processar_comando(estado, " ", modelo)
        estado = processar_comando(estado, "\x1b[B", modelo)
        estado = processar_comando(estado, " ", modelo)
        assert controlador.aplicar_disponivel is True


# --- Setas: nao mudam candidato nem elegibilidade ---------------------------------------


def test_setas_nao_mudam_candidato_nem_elegibilidade():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    candidato_antes = copy.deepcopy(runtime.candidato)
    assert controlador.aplicar_disponivel is False

    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    assert runtime.candidato == candidato_antes
    assert controlador.aplicar_disponivel is False

    estado = processar_comando(estado, " ", modelo)  # entra nos filhos
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, "\x1b[A", modelo)
    assert runtime.candidato == candidato_antes
    assert controlador.aplicar_disponivel is False


# --- Espaco: muda candidato; elegibilidade acompanha ------------------------------------


def test_espaco_muda_candidato_e_elegibilidade_acompanha():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    assert controlador.aplicar_disponivel is False
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert runtime.comparar_candidato_baseline() is False
    assert controlador.aplicar_disponivel is True


# --- Esc filho -> pais (distinto de saida efetiva) ---------------------------------------


def test_esc_filho_preserva_candidato_baseline_e_aplicar_ativo():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    baseline_antes = copy.deepcopy(runtime.baseline)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = _preset(runtime, "candidato", "borda")
    assert controlador.aplicar_disponivel is True

    estado = processar_comando(estado, "\x1b", modelo)  # Esc filho->pais
    console = controlador.console_do_modelo(modelo)
    assert not navegacao.em_nivel_filhos(estado, console)
    assert estado["tela_atual"] == _ID_TELA_H0063

    assert _preset(runtime, "candidato", "borda") == b
    assert runtime.baseline == baseline_antes
    assert controlador.aplicar_disponivel is True
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert estado.get("popup") is None


# --- Saida efetiva -------------------------------------------------------------------------


def test_saida_efetiva_restaura_candidato_e_desativa_aplicar(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert controlador.aplicar_disponivel is True

    estado = processar_comando(estado, "\x1b", modelo)  # pais
    estado = processar_comando(estado, "\x1b", modelo)  # saida efetiva

    assert estado["tela_atual"] == "demo"
    assert runtime.candidato == baseline_antes
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert controlador.aplicar_disponivel is False


# --- Resize/redraw ---------------------------------------------------------------------------


def test_resize_redraw_preserva_elegibilidade():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert controlador.aplicar_disponivel is True

    for largura, altura in ((120, 40), (80, 24), (62, 20), (100, 30)):
        quadro = _quadro(estado, modelo, largura=largura, altura=altura)
        assert isinstance(quadro, str) and quadro
        estado = _preparar_estado_estilo(estado, modelo)
        assert controlador.aplicar_disponivel is True
        assert _estado_ativo_chip_aplicar() is True


# --- Snapshot imutavel -------------------------------------------------------------------------


def test_snapshot_imutavel_apos_mutacao_posterior_via_dispatch():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    a = _preset(runtime, "baseline", "borda")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    b = _preset(runtime, "candidato", "borda")
    assert b != a

    estado = processar_comando(estado, "\r", modelo)
    solicitacao_1 = estado["solicitacao_aplicacao_estilo"]
    assert solicitacao_1.baseline["borda"]["preset_default"] == a
    assert solicitacao_1.candidato["borda"]["preset_default"] == b
    assert estado.get("popup") is not None

    # H-0067: fechar o popup modal (ABORTADO) antes de comandos da tela.
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None

    # Mutacao posterior do runtime/candidato via dispatch normal (nova
    # escolha de filho, e depois retorno ao preset original da baseline).
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b", modelo)  # pais
    estado = processar_comando(estado, "\x1b", modelo)  # saida efetiva: candidato=A

    assert runtime.candidato["borda"]["preset_default"] == a
    # A solicitacao emitida antes da mutacao continua representando A/B.
    assert solicitacao_1.baseline["borda"]["preset_default"] == a
    assert solicitacao_1.candidato["borda"]["preset_default"] == b


# --- Fronteiras posteriores ------------------------------------------------------------------


def test_fronteiras_apos_enter_aplicar_abre_popup_sem_persistencia_publicacao(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("solicitacao_aplicacao_estilo") is not None

    # H-0067: popup de confirmacao aberto, mas ainda sem decisao/persistencia.
    assert estado.get("popup") is not None
    assert estado["popup"].id == "popup_confirmacao_aplicacao_estilo"
    assert estado.get("popup_resultado") is None
    quadro = _quadro(estado, modelo)
    assert "Aplicar estilo" in quadro
    assert "CONFIRMADO" not in quadro
    assert "ABORTADO" not in quadro
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert runtime.global_vigente == runtime.materializacao_global
    assert destino.read_text(encoding="utf-8") == original
    # Candidato continua existindo (nao destruido/reinicializado).
    assert runtime.comparar_candidato_baseline() is False


def test_demonstracao_non_tty_ciclo_aplicar(monkeypatch, tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    # F4, entra nos filhos, seta, Espaco escolhe, Enter aciona Aplicar,
    # Esc pais, Esc sai.
    entrada = io.StringIO(" \n\x1b[B\n \n\r\n\x1b\n\x1b\n")
    saida = io.StringIO()
    monkeypatch.setattr(_DEMO.sys, "stdin", entrada)
    monkeypatch.setattr(_DEMO.sys, "stdout", saida)

    codigo = main(
        ["demo.py", _ID_TELA_H0063],
        estado_inicial=dict(
            criar_estado_inicial(),
            estilo_runtime=runtime,
            estilo=runtime.global_vigente,
            tela_atual=_ID_TELA_H0063,
            largura=100,
            altura=30,
        ),
    )
    assert codigo == 0
    texto = saida.getvalue()
    assert "borda" in texto
    assert "Aplicar" in texto
    assert "CONFIRMADO" not in texto
    assert "ABORTADO" not in texto
    # Sem TTY, o loop nao expõe o estado final ao teste; a fronteira de
    # ausencia de persistencia/publicacao e comprovada nos testes acima via
    # processar_comando direto. Aqui comprovamos apenas que o ciclo completo
    # (F4 -> divergencia -> Enter/Aplicar -> Esc -> Esc) roda sem excecao e
    # sem publicar/persistir o arquivo real.
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
