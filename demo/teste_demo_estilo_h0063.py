"""Testes focais F4 / tela normal / resize H-0063 sem TTY."""

from __future__ import annotations

import copy
import io
import json
import os
import re
import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "demo_h0063_mod", Path(__file__).with_name("demo.py")
)
_DEMO = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_DEMO)

TECLA_F4 = _DEMO.TECLA_F4
_ID_TELA_H0063 = _DEMO._ID_TELA_H0063
_carregar_modelo_por_id = _DEMO._carregar_modelo_por_id
_ler_tecla_sessao = _DEMO._ler_tecla_sessao
_preparar_modelo_estilo = _DEMO._preparar_modelo_estilo
_preparar_estado_estilo = _DEMO._preparar_estado_estilo
_anexar_tela_estilo = _DEMO._anexar_tela_estilo
criar_estado_inicial = _DEMO.criar_estado_inicial
processar_comando = _DEMO.processar_comando
renderizar_estado = _DEMO.renderizar_estado
main = _DEMO.main

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
from tela.loader import RuntimeEstilo
from tela import navegacao
from tela.renderizacao.texto_ansi import _ANSI_RESET_FG, _codigo_ansi_de_cor
from tela.renderizador import _navegacao_atual

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _sem_ansi(texto):
    return _ANSI.sub("", texto)


RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"


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


def _quadro_resolvido(estado, modelo, largura, altura):
    return _DEMO._resolver_conteudo(estado, modelo, largura, altura)


def test_decoder_fisico_normaliza_f4():
    leitura, escrita = os.pipe()
    try:
        os.write(escrita, b"\x1bOS")
        assert _ler_tecla_sessao(leitura) == TECLA_F4
    finally:
        os.close(leitura)
        os.close(escrita)


def test_f4_abre_tela_normal_com_cabecalho_console_e_barra():
    estado, modelo = _abrir()
    assert modelo.id == _ID_TELA_H0063
    assert modelo.cabecalho["titulo"] == "Estilo"
    assert any(e.tipo == "console" for e in modelo.corpo.elementos)
    assert modelo.barra_de_menus["chips"]
    quadro = _quadro(estado, modelo)
    assert "ESTILO" in quadro or "Estilo" in quadro
    assert "borda" in quadro
    assert "chip" in quadro
    assert "[?] Ajuda" in quadro or "Ajuda" in quadro
    assert "popup" not in quadro.lower()
    assert estado.get("popup") is None


def test_ajuda_ultimo_e_aplicar_presente_inativo_sem_entrada_no_nivel():
    estado, modelo = _abrir()
    chips = modelo.barra_de_menus["chips"]
    assert chips[-1]["id"] == "chip_ajuda"
    assert chips[-1]["tecla"] == "?"
    textos = [c.get("texto", "") for c in chips]
    assert "entrada no nível" not in textos
    assert "entrada no nivel" not in textos
    _quadro(estado, modelo)
    assert _navegacao_atual["estado_ativo_chips"]["chip_ajuda"] is True
    # H-0066: chip_aplicar passa a existir sempre, declarado antes de Ajuda;
    # com candidato==baseline na abertura, permanece inativo (nao ausente).
    ids = [c["id"] for c in chips]
    assert "chip_aplicar" in ids
    assert ids.index("chip_aplicar") < ids.index("chip_ajuda")
    assert "Aplicar" in textos
    assert _navegacao_atual["estado_ativo_chips"]["chip_aplicar"] is False


def test_quatro_pais_e_presets_dinamicos_no_quadro(tmp_path):
    configuracao = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    padrao = configuracao["chip"]["preset_default"]
    configuracao["chip"]["presets"]["Fixture Sintetica"] = copy.deepcopy(
        configuracao["chip"]["presets"][padrao]
    )
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(
        json.dumps(configuracao, ensure_ascii=False), encoding="utf-8"
    )
    runtime = RuntimeEstilo(tmp_path)
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    assert tuple(p.nome for p in controlador.pais) == CATEGORIAS_ESTILO
    assert "Fixture Sintetica" in [p.nome for p in controlador.filhos["chip"]]
    quadro = _quadro(estado, modelo)
    for nome in CATEGORIAS_ESTILO:
        assert nome in quadro


def test_escolhas_iniciais_preset_default_e_cursor_nao_transfere():
    runtime = RuntimeEstilo()
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    iniciais = dict(controlador.escolhas_de(estado, modelo))
    assert iniciais == controlador.escolhas_iniciais
    assert len(estado["selecoes"][controlador.console_do_modelo(modelo).id]) == 4

    estado = processar_comando(estado, "\x1b[B", modelo)
    assert controlador.escolhas_de(estado, modelo) == iniciais

    estado = processar_comando(estado, " ", modelo)
    console = controlador.console_do_modelo(modelo)
    assert navegacao.em_nivel_filhos(estado, console)
    filho_antes = controlador.filho_corrente(estado, modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    filho_depois = controlador.filho_corrente(estado, modelo)
    assert filho_depois is not None
    assert filho_antes is not None
    assert filho_depois.id != filho_antes.id
    assert controlador.escolhas_de(estado, modelo) == iniciais


def test_espaco_transfere_escolha_e_muta_apenas_candidato(tmp_path):
    """H-0065: Espaco aceita candidato e projeta selecoes; baseline/global/arquivo intactos."""
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    borda_antes = runtime.candidato["borda"]["preset_default"]

    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]
    iniciais = dict(controlador.escolhas_de(estado, modelo))

    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    depois = controlador.escolhas_de(estado, modelo)
    assert depois["borda"] != iniciais["borda"]
    assert depois["chip"] == iniciais["chip"]
    assert depois["indicadores.selecionado"] == iniciais[
        "indicadores.selecionado"
    ]
    assert depois["indicadores.incluido"] == iniciais["indicadores.incluido"]
    assert (
        len(estado["selecoes"][controlador.console_do_modelo(modelo).id]) == 4
    )

    # Candidato transitório mutável; selecoes projeta o candidato.
    assert runtime.candidato["borda"]["preset_default"] == depois["borda"]
    assert runtime.candidato["borda"]["preset_default"] != borda_antes
    assert controlador.invariavel_candidato_selecoes(estado, modelo)

    # Estilo efetivamente aplicado e persistido permanecem imutáveis.
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert estado.get("popup") is None


def test_esc_nos_filhos_retorna_aos_pais_preservando_escolha():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    escolhidas = dict(controlador.escolhas_de(estado, modelo))
    quadro_filhos = _quadro(estado, modelo)
    assert "Voltar" in quadro_filhos
    assert "Retornar aos pais" not in quadro_filhos

    estado = processar_comando(estado, "\x1b", modelo)
    console = controlador.console_do_modelo(modelo)
    assert not navegacao.em_nivel_filhos(estado, console)
    assert controlador.escolhas_de(estado, modelo) == escolhidas
    assert estado["tela_atual"] == _ID_TELA_H0063
    quadro_pais = _quadro(estado, modelo)
    assert "Sair" in quadro_pais
    assert "Retornar aos pais" not in quadro_pais


def test_esc_nos_pais_sai_pela_pilha_sem_mutacao(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    estado, modelo = _abrir(runtime)
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b", modelo)
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado["tela_atual"] == "demo"
    assert estado["pilha_telas"] == []
    assert estado.get("tela_estilo") is None
    assert destino.read_text(encoding="utf-8") == original
    assert runtime.global_vigente == runtime.materializacao_global


def test_barra_selecionar_canonico():
    estado, modelo = _abrir()
    estado = processar_comando(estado, " ", modelo)
    quadro = _quadro(estado, modelo)
    assert "Selecionar" in quadro
    assert "entrada no nível" not in quadro
    assert "entrada no nivel" not in quadro
    # H-0066: apenas entrar nos filhos (sem Espaco de escolha) nao diverge o
    # candidato; Aplicar permanece presente e inativo (nao ausente).
    assert "Aplicar" in quadro
    assert _navegacao_atual["estado_ativo_chips"]["chip_aplicar"] is False
    assert quadro.rstrip().splitlines()[-1].count("Ajuda") >= 0
    chips = modelo.barra_de_menus["chips"]
    assert chips[-1]["texto"] == "Ajuda"


def test_resize_dimensoes_suportadas_preserva_escolha_e_estrutura():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    escolhidas = dict(controlador.escolhas_de(estado, modelo))

    dimensoes = (
        (120, 40),  # larga
        (80, 24),   # media
        (62, 20),   # estreita ainda suportada
        (80, 12),   # baixa
        (100, 30),  # crescimento posterior
    )
    for largura, altura in dimensoes:
        quadro = _quadro_resolvido(estado, modelo, largura, altura)
        assert isinstance(quadro, str)
        assert quadro
        assert "Aumente a janela" not in quadro
        assert len(quadro.splitlines()) <= altura
        assert "borda" in quadro or "ESTILO" in quadro or "Estilo" in quadro
        assert "Ajuda" in quadro or "Esc" in quadro
        assert controlador.escolhas_de(estado, modelo) == escolhidas
        assert "Selecao interativa de presets" not in quadro


def test_terminal_pequeno_e_recuperacao():
    estado, modelo = _abrir()
    pequeno = _quadro_resolvido(estado, modelo, 8, 4)
    assert "Terminal" in pequeno
    assert "Aumente" in pequeno
    recuperado = _quadro_resolvido(estado, modelo, 80, 24)
    assert "borda" in recuperado
    assert "Ajuda" in recuperado
    assert "Aumente a janela" not in recuperado


def test_fronteira_sem_confirmado_abortado_aplicar_popup():
    estado, modelo = _abrir()
    for comando in (" ", "\x1b[B", " ", "\x1b", "\x1b[B", " "):
        estado = processar_comando(estado, comando, modelo)
    quadro = _quadro(estado, modelo)
    assert "CONFIRMADO" not in quadro
    assert "ABORTADO" not in quadro
    # H-0066: a sequencia acima diverge o candidato (Espaco em borda), entao
    # Aplicar aparece ATIVO; sem Enter, nenhuma solicitacao e produzida.
    assert "Aplicar" in quadro
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert estado.get("popup") is None
    assert estado.get("popup_resultado") is None
    assert estado.get("solicitacao_aplicacao_estilo") is None


def test_f1_f2_f3_f5_f11_nao_alteram_estado():
    estado, modelo = _abrir()
    anterior = estado["tela_atual"], list(estado["pilha_telas"])
    for comando in ("F1", "F2", "F3", "F5", "F11"):
        estado = processar_comando(estado, comando, modelo)
        assert (estado["tela_atual"], estado["pilha_telas"]) == anterior


def test_configuracao_real_h0063_paginas_unidade_canonica_inativa_em_1_de_1():
    estado, modelo = _abrir()
    caminho = RAIZ / "config" / "telas" / "demo" / (
        "h0063_estilo_estrutura_navegacao_dois_niveis.json"
    )
    assert modelo.id == _ID_TELA_H0063
    assert json.loads(caminho.read_text(encoding="utf-8"))["id"] == modelo.id

    ids = [c["id"] for c in modelo.barra_de_menus["chips"]]
    assert "chip_pagina_anterior" in ids
    assert "chip_pagina_proxima" in ids
    assert ids.index("chip_pagina_proxima") == ids.index("chip_pagina_anterior") + 1

    quadro = _quadro(estado, modelo, largura=100, altura=40)
    visivel = _sem_ansi(quadro)
    assert "[PgUp][PgDn]" not in visivel
    assert "[PgUp/PgDn] Páginas" in visivel
    assert "página 1/1" in visivel

    estados = _navegacao_atual["estado_ativo_chips"]
    assert estados["chip_pagina_anterior"] is False
    assert estados["chip_pagina_proxima"] is False

    codigo = _codigo_ansi_de_cor(estado["estilo"].cor_inativo)
    unidade_inativa = (
        "[" + codigo + "PgUp" + _ANSI_RESET_FG
        + "/" + codigo + "PgDn" + _ANSI_RESET_FG + "]"
    )
    assert codigo
    linha_barra = next(
        linha for linha in quadro.splitlines()
        if "[PgUp/PgDn] Páginas" in _sem_ansi(linha)
    )
    assert unidade_inativa in linha_barra
    assert linha_barra.index(codigo) < linha_barra.index("Páginas")
    assert visivel.index("[PgUp/PgDn]") < visivel.index("Páginas")


def test_demonstracao_non_tty_fixture_h0063(monkeypatch):
    runtime = RuntimeEstilo()
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
    assert "chip" in texto
    assert runtime.global_vigente == runtime.materializacao_global
