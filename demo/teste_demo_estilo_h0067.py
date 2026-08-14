"""Testes de integracao H-0067 — confirmacao da aplicacao de estilo sem TTY."""

from __future__ import annotations

import copy
import io
import importlib.util
import json
import re
from pathlib import Path

import pytest

_RE_ANSI_H0067 = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _visivel(texto):
    """Texto sem sequencias SGR; indices passam a corresponder a colunas
    visuais, evitando falso-positivo/negativo por causa de ANSI antes do
    ponto de corte (ver RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067.md)."""
    return _RE_ANSI_H0067.sub("", texto)

_SPEC = importlib.util.spec_from_file_location(
    "demo_h0067_mod", Path(__file__).with_name("demo.py")
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

from tela.estilo import (
    ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO,
    SolicitacaoAplicacaoEstilo,
)
from tela.loader import RuntimeEstilo
from tela.renderizacao import popup as popup_mod
from tela.renderizacao.texto_ansi import _largura_sem_ansi


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
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    return estado


def _abrir_confirmacao(runtime=None):
    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert estado["tela_estilo"].aplicar_disponivel is True
    estado = processar_comando(estado, "\r", modelo)
    return estado, modelo


# --- Entrada valida / invalida -------------------------------------------------


def test_aplicar_ativo_enter_abre_popup_com_solicitacao():
    estado, modelo = _abrir_confirmacao()
    solicitacao = estado.get("solicitacao_aplicacao_estilo")
    assert isinstance(solicitacao, SolicitacaoAplicacaoEstilo)
    assert estado.get("popup") is not None
    assert estado["popup"].id == ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO
    assert estado["popup"].conteudo["tipo"] == "texto"
    assert estado.get("popup_resultado") is None
    quadro = _quadro(estado, modelo)
    assert "Aplicar estilo" in quadro
    assert "Confirmar" in quadro or "CONFIRMAR" in quadro
    assert "Voltar" in quadro or "VOLTAR" in quadro


def test_aplicar_inativo_enter_nao_abre_popup():
    estado, modelo = _abrir()
    assert estado["tela_estilo"].aplicar_disponivel is False
    estado2 = processar_comando(estado, "\r", modelo)
    assert estado2.get("solicitacao_aplicacao_estilo") is None
    assert estado2.get("popup") is None
    assert estado2["tela_atual"] == _ID_TELA_H0063


# --- CONFIRMADO ----------------------------------------------------------------


def test_enter_popup_produz_confirmado_retendo_solicitacao(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    candidato_antes = copy.deepcopy(runtime.candidato)

    estado, modelo = _abrir_confirmacao(runtime)
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    a = solicitacao.baseline["borda"]["preset_default"]
    b = solicitacao.candidato["borda"]["preset_default"]
    assert b != a
    candidato_antes = copy.deepcopy(runtime.candidato)

    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert "valor" not in estado["popup_resultado"]
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert solicitacao.candidato["borda"]["preset_default"] == b

    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == solicitacao.candidato
    assert runtime.candidato == candidato_antes
    assert runtime.baseline == solicitacao.candidato
    assert runtime.global_vigente == estado["estilo"]
    assert runtime.global_vigente == runtime.materializacao_global
    assert runtime.global_vigente != global_antes
    assert runtime.baseline != baseline_antes
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert estado["tela_estilo"].aplicar_disponivel is False


# --- ABORTADO ------------------------------------------------------------------


def test_esc_popup_produz_abortado_descarta_solicitacao_preserva_candidato(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir_confirmacao(runtime)
    candidato_antes = copy.deepcopy(runtime.candidato)
    selecoes_antes = copy.deepcopy(estado.get("selecoes"))
    assert estado["tela_estilo"].aplicar_disponivel is True

    estado = processar_comando(estado, "\x1b", modelo)
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert runtime.candidato == candidato_antes
    assert estado.get("selecoes") == selecoes_antes
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original

    # Nova tentativa produz nova solicitacao e novo popup.
    estado = processar_comando(estado, "\r", modelo)
    assert isinstance(estado.get("solicitacao_aplicacao_estilo"), SolicitacaoAplicacaoEstilo)
    assert estado.get("popup") is not None


# --- Modalidade ----------------------------------------------------------------


def test_modalidade_bloqueia_tela_subjacente_enquanto_popup_aberto():
    estado, modelo = _abrir_confirmacao()
    controlador = estado["tela_estilo"]
    runtime = estado["estilo_runtime"]
    candidato_antes = copy.deepcopy(runtime.candidato)
    selecoes_antes = copy.deepcopy(estado.get("selecoes"))
    cursores_antes = copy.deepcopy(estado.get("cursores"))
    pagina_antes = copy.deepcopy(estado.get("pagina_atual"))
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    instancia = estado["popup"]

    # Setas / PgUp / PgDn / Espaco nao mutam a tela subjacente.
    for tecla in ("\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D", "\x1b[5~", "\x1b[6~", " "):
        estado = processar_comando(estado, tecla, modelo)
        assert estado.get("popup") is instancia
        assert estado.get("solicitacao_aplicacao_estilo") is solicitacao
        assert runtime.candidato == candidato_antes
        assert estado.get("selecoes") == selecoes_antes
        assert estado.get("cursores") == cursores_antes
        assert estado.get("pagina_atual") == pagina_antes
        assert estado["tela_atual"] == _ID_TELA_H0063

    # Esc no popup nao e saida efetiva H-0065.
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert runtime.candidato == candidato_antes
    assert controlador.aplicar_disponivel is True


def test_enter_com_popup_nao_reexecuta_aplicar_da_tela(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    estado, modelo = _abrir_confirmacao(runtime)
    assert estado.get("popup") is not None

    # Enter consome o popup (CONFIRMADO); nao cria segunda solicitacao.
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None


# --- Snapshot ------------------------------------------------------------------


def test_snapshot_confirmado_permanece_ligado_ao_original(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    estado, modelo = _abrir_confirmacao(runtime)
    a = _preset(runtime, "baseline", "borda")
    b = _preset(runtime, "candidato", "borda")
    solicitacao = estado["solicitacao_aplicacao_estilo"]
    assert solicitacao.candidato["borda"]["preset_default"] == b

    estado = processar_comando(estado, "\r", modelo)  # CONFIRMADO
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None

    # Mutacao posterior do candidato nao altera o snapshot confirmado.
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    assert solicitacao.candidato["borda"]["preset_default"] == b
    assert solicitacao.baseline["borda"]["preset_default"] == a


# --- Resize --------------------------------------------------------------------


def test_resize_com_popup_aberto_preserva_instancia():
    estado, modelo = _abrir_confirmacao()
    instancia = estado["popup"]
    solicitacao = estado["solicitacao_aplicacao_estilo"]

    for largura, altura in ((120, 40), (80, 24), (62, 20), (100, 30)):
        quadro = _quadro(estado, modelo, largura=largura, altura=altura)
        assert isinstance(quadro, str) and quadro
        assert "Aplicar estilo" in quadro
        assert estado.get("popup") is instancia
        assert estado.get("solicitacao_aplicacao_estilo") is solicitacao
        assert estado.get("popup_resultado") is None


# --- Geometria visual (H-0067-P01) ----------------------------------------------
#
# RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067.md: as amostras ANSI H-0064
# ("Destaque Texto"/"Destaque Fundo") inflavam largura_corpo via max(len()),
# deslocando a centralizacao do popup e apagando a borda direita do Console
# nas linhas atravessadas. Os testes abaixo provam a geometria corrigida
# sobre o FLUXO REAL H-0067 (F4 -> divergencia -> Enter -> popup), nao um
# corpo sintetico desligado da tela de Estilo.


def _geometria_popup_esperada(estado, largura, altura):
    """Geometria de referencia calculada pela mesma API de layout do popup,
    contra a largura VISUAL do corpo (nao ``len()``)."""
    estilo = (
        estado.get("estilo_demonstracao_local")
        if estado.get("_sessao_demonstracao_estilo") is not None
        else estado["estilo"]
    )
    medidas = popup_mod.geometria_popup(
        estado["popup"], estilo,
        largura_corpo=largura, altura_corpo=altura,
    )
    x = (largura - medidas["largura"]) // 2
    y = (altura - medidas["altura"]) // 2
    return {
        "largura_popup": medidas["largura"],
        "altura_popup": medidas["altura"],
        "x": x,
        "y": y,
        "x_final": x + medidas["largura"],
        "margem_esquerda": x,
        "margem_direita": largura - (x + medidas["largura"]),
    }


def test_popup_estilo_l100_margens_3_3_sem_overflow():
    """Caso concreto do diagnostico: L=100, intrinseca=94 -> margens 3/3,
    nunca x_final=102 (overflow de +2 medido antes do patch)."""
    estado, modelo = _abrir_confirmacao()
    largura, altura = 100, 28
    geometria = _geometria_popup_esperada(estado, largura, altura)
    assert geometria["largura_popup"] == 94
    assert geometria["x"] == 3
    assert geometria["x_final"] == 97
    assert geometria["margem_esquerda"] == 3
    assert geometria["margem_direita"] == 3

    quadro = _quadro(estado, modelo, largura=largura, altura=altura)
    linhas = [l for l in quadro.split("\n") if l]
    assert max(_largura_sem_ansi(l) for l in linhas) <= largura
    assert all(_largura_sem_ansi(l) <= largura for l in linhas), (
        "nenhuma linha final pode exceder a largura visual da viewport"
    )


@pytest.mark.parametrize("largura", [120, 100, 80, 70, 62])
def test_popup_estilo_multiplas_larguras_sem_overflow_visual(largura):
    estado, modelo = _abrir_confirmacao()
    altura = 28
    quadro = _quadro(estado, modelo, largura=largura, altura=altura)
    linhas = [l for l in quadro.split("\n") if l]
    maior = max(_largura_sem_ansi(l) for l in linhas)
    assert maior <= largura, (
        "popup Estilo excedeu a viewport em L={0}: max_visual={1}".format(
            largura, maior
        )
    )


def test_borda_console_subjacente_preservada_fora_do_popup():
    """O popup substitui somente seu retangulo na demonstracao integrada.

    A base autorizada aqui e a demonstracao H-0069 sob o candidato local C,
    nao o quadro global predecessor de H-0067.
    """
    largura, altura = 100, 28
    estado_com, modelo_predecessor = _abrir_confirmacao()
    modelo = _DEMO._modelo_corrente(estado_com, modelo_predecessor)
    assert modelo.id == _DEMO._ID_TELA_H0069_DEMONSTRACAO
    assert estado_com.get("_sessao_demonstracao_estilo") is not None
    estilo_local = estado_com["estilo_demonstracao_local"]

    # Mesmo estado de navegacao/cursor do popup aberto, sem o popup em si:
    # isola o efeito do overlay e mantem a demonstracao integrada sob C.
    estado_sem = dict(estado_com, popup=None)
    quadro_sem = _quadro(estado_sem, modelo, largura=largura, altura=altura)
    linhas_sem = quadro_sem.split("\n")

    quadro_com = _quadro(estado_com, modelo, largura=largura, altura=altura)
    linhas_com = quadro_com.split("\n")

    assert len(linhas_sem) == len(linhas_com)
    assert estilo_local.canto_superior_direito in _visivel(quadro_sem)
    assert estilo_local.canto_superior_direito in _visivel(quadro_com)
    assert max(_largura_sem_ansi(linha) for linha in linhas_sem) <= largura
    assert max(_largura_sem_ansi(linha) for linha in linhas_com) <= largura

    # O retangulo vertical do popup e o conjunto (contiguo) de linhas que o
    # overlay de fato altera -- deriva-se do proprio quadro, sem depender de
    # contar manualmente linhas de cabecalho/barra.
    diffs = [
        indice
        for indice, (a, b) in enumerate(zip(linhas_sem, linhas_com))
        if a != b
    ]
    assert diffs, "popup nao alterou nenhuma linha do quadro"
    assert diffs == list(range(diffs[0], diffs[-1] + 1)), (
        "linhas alteradas pelo popup nao formam um retangulo vertical contiguo"
    )

    geometria = _geometria_popup_esperada(estado_com, largura, altura)
    x, x_final = geometria["x"], geometria["x_final"]

    for indice, (linha_sem, linha_com) in enumerate(zip(linhas_sem, linhas_com)):
        if indice not in diffs:
            assert linha_com == linha_sem, (
                "linha {0} fora do retangulo do popup foi alterada".format(indice)
            )
            if linha_sem:
                assert _largura_sem_ansi(linha_com) == largura
                assert linha_com.rstrip()[-1:] == linha_sem.rstrip()[-1:]
            continue
        # Dentro do retangulo vertical: fora da faixa HORIZONTAL [x, x_final)
        # a linha nao pode ter mudado -- prova que o splice nao vazou nem
        # deslocou a borda direita do Console para colunas cobertas pelo
        # popup apenas verticalmente (linha atravessada, mas nao na coluna).
        # Comparado sobre o texto visivel (sem SGR) para que o indice
        # coincida com a coluna visual, mesmo nas duas linhas com amostra
        # ANSI H-0064 ("Destaque Texto"/"Destaque Fundo").
        visivel_sem = _visivel(linha_sem)
        visivel_com = _visivel(linha_com)
        assert visivel_com[:x] == visivel_sem[:x]
        assert visivel_com[x_final:] == visivel_sem[x_final:]
        assert _largura_sem_ansi(linha_com) == largura


def test_resize_popup_estilo_geometria_sem_residuo_em_cada_frame():
    """Ciclo 120 -> 80 -> 62 -> 100 -> 120 com popup aberto: em cada frame,
    overflow=0, popup centralizado pelo espaco disponivel, mesma instancia
    logica, sem borda deslocada nem linha residual."""
    estado, modelo = _abrir_confirmacao()
    instancia = estado["popup"]
    altura = 28

    for largura in (120, 80, 62, 100, 120):
        quadro = _quadro(estado, modelo, largura=largura, altura=altura)
        linhas = [l for l in quadro.split("\n") if l]
        assert max(_largura_sem_ansi(l) for l in linhas) <= largura
        assert all(_largura_sem_ansi(l) <= largura for l in linhas)
        geometria = _geometria_popup_esperada(estado, largura, altura)
        assert geometria["margem_esquerda"] >= 0
        assert geometria["margem_direita"] >= 0
        assert estado.get("popup") is instancia


# --- Fronteiras ----------------------------------------------------------------


def test_fronteiras_apos_confirmado_e_abortado(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir_confirmacao(runtime)
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == runtime.baseline
    assert runtime.global_vigente == estado["estilo"]
    assert runtime.baseline != baseline_antes
    assert runtime.global_vigente != global_antes
    assert estado["tela_estilo"].aplicar_disponivel is False

    # Nova divergencia + ABORTADO (sem efeito de persistencia/publicacao).
    baseline_pos = copy.deepcopy(runtime.baseline)
    global_pos = runtime.global_vigente
    original_pos = destino.read_text(encoding="utf-8")
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert estado["tela_estilo"].aplicar_disponivel is True
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup") is not None
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert runtime.baseline == baseline_pos
    assert runtime.global_vigente == global_pos
    assert destino.read_text(encoding="utf-8") == original_pos
    assert runtime.comparar_candidato_baseline() is False


# --- Demonstracao non-TTY ------------------------------------------------------


def test_demonstracao_non_tty_ciclo_confirmacao(tmp_path):
    """Fluxo real non-TTY via processar_comando (Enter nao sobrevive ao
    loop line-oriented de main(); mesma limitacao ja aceita em H-0066)."""
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    # F4 -> Estilo
    estado = _estado_base(runtime)
    modelo = _carregar_modelo_por_id("demo")
    estado = processar_comando(estado, TECLA_F4, modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)

    # Candidato divergente; Aplicar ativo
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert estado["tela_estilo"].aplicar_disponivel is True
    candidato_divergente = copy.deepcopy(runtime.candidato)

    # Enter -> solicitacao + popup tipo texto; tela subjacente bloqueada
    estado = processar_comando(estado, "\r", modelo)
    assert isinstance(estado.get("solicitacao_aplicacao_estilo"), SolicitacaoAplicacaoEstilo)
    solicitacao_1 = estado["solicitacao_aplicacao_estilo"]
    assert estado.get("popup") is not None
    assert estado["popup"].id == ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO
    assert estado["popup"].conteudo["tipo"] == "texto"
    quadro = _quadro(estado, modelo)
    assert "Aplicar estilo" in quadro
    estado_pos_seta = processar_comando(estado, "\x1b[B", modelo)
    assert estado_pos_seta.get("popup") is estado["popup"]
    assert runtime.candidato == candidato_divergente

    # Resize com popup aberto
    for largura, altura in ((80, 24), (62, 20), (100, 30)):
        assert "Aplicar estilo" in _quadro(estado, modelo, largura, altura)
        assert estado.get("popup") is not None

    # Esc -> ABORTADO; candidato preservado
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert runtime.candidato == candidato_divergente
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert estado["tela_estilo"].aplicar_disponivel is True

    # Nova tentativa -> Enter CONFIRMADO; solicitacao retida
    estado = processar_comando(estado, "\r", modelo)
    solicitacao_2 = estado["solicitacao_aplicacao_estilo"]
    assert solicitacao_2 is not solicitacao_1
    estado = processar_comando(estado, "\r", modelo)
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert "valor" not in estado["popup_resultado"]

    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == candidato_divergente
    assert runtime.baseline == candidato_divergente
    assert runtime.candidato == candidato_divergente
    assert runtime.global_vigente == estado["estilo"]
    assert runtime.global_vigente == runtime.materializacao_global
    assert runtime.baseline != baseline_antes
    assert runtime.global_vigente != global_antes
    assert estado["tela_estilo"].aplicar_disponivel is False


def test_demonstracao_main_non_tty_smoke_sem_excecao(monkeypatch, tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    # Smoke do loop main non-TTY (Enter via stdin line-oriented nao e
    # transportavel; coberta pelo ciclo processar_comando acima).
    entrada = io.StringIO(" \n\x1b[B\n \n\x1b\n\x1b\n")
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
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
