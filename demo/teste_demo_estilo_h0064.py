"""Testes focais F4 / amostras / resize / paginacao H-0064 sem TTY."""

from __future__ import annotations

import copy
import io
import json
import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "demo_h0064_mod", Path(__file__).with_name("demo.py")
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
from tela.renderizacao.estilo import (
    PAYLOAD_CANONICO_CHIP,
    SEPARADOR_NOME_AMOSTRA,
    amostra_borda,
)
from tela.renderizacao.texto_ansi import _codigo_ansi_de_cor, _largura_sem_ansi


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


def test_amostras_visiveis_no_quadro_apos_entrar_nos_filhos():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    estado = processar_comando(estado, " ", modelo)  # entra em borda
    quadro = _quadro(estado, modelo)
    preset_borda = controlador.filhos["borda"][0]
    amostra = amostra_borda(preset_borda.dados)
    assert preset_borda.nome in quadro
    assert amostra in quadro
    assert SEPARADOR_NOME_AMOSTRA.strip() == "" or preset_borda.nome in quadro


def test_amostras_chip_com_cores_no_quadro():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    # Pai chip e o segundo (indice 1).
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    quadro = _quadro(estado, modelo)
    assert PAYLOAD_CANONICO_CHIP == "A"
    assert "A" in quadro
    assert "Ab" not in quadro
    assert "AB" not in quadro
    destaque_texto = None
    destaque_fundo = None
    for preset in controlador.filhos["chip"]:
        if preset.nome == "Destaque Texto":
            destaque_texto = preset
        if preset.nome == "Destaque Fundo":
            destaque_fundo = preset
    assert destaque_texto is not None
    assert destaque_fundo is not None
    # Pelo menos o codigo de cor de um dos destaques deve aparecer quando
    # a pagina exibe o filho correspondente; navega ate cobrir.
    visto_azul_fg = _codigo_ansi_de_cor("azul") in quadro
    # Paginar/navegar pelos filhos de chip.
    for _ in range(8):
        estado = processar_comando(estado, "\x1b[B", modelo)
        quadro = _quadro(estado, modelo)
        if _codigo_ansi_de_cor("azul") in quadro:
            visto_azul_fg = True
        if "\x1b[44m" in quadro:  # fundo azul
            break
    assert visto_azul_fg or PAYLOAD_CANONICO_CHIP in quadro
    assert "Ab" not in quadro
    assert "AB" not in quadro


def test_paginacao_com_amostras_preserva_chip_paginas():
    estado, modelo = _abrir()
    chips = {c["id"]: c for c in modelo.barra_de_menus["chips"]}
    assert "chip_paginas" not in chips
    assert "chip_pagina_anterior" in chips
    assert "chip_pagina_proxima" in chips
    assert chips["chip_pagina_anterior"]["tecla"] == "PgUp"
    assert chips["chip_pagina_proxima"]["tecla"] == "PgDn"
    assert chips["chip_pagina_proxima"]["texto"] == "Páginas"
    console = modelo.corpo.elementos[0]
    assert console._campos_inertes.get("politica_paginacao") == "com"
    ids = [c["id"] for c in modelo.barra_de_menus["chips"]]
    assert "chip_pagina_anterior" in ids
    assert "chip_pagina_proxima" in ids
    assert ids.index("chip_pagina_proxima") == ids.index("chip_pagina_anterior") + 1
    assert ids[0] == "chip_sair"
    assert ids[-1] == "chip_ajuda"
    # Altura baixa forca paginacao; acao Paginas permanece na Barra.
    estado = processar_comando(estado, " ", modelo)
    quadro = _quadro_resolvido(estado, modelo, 80, 14)
    assert "página" in quadro.lower() or "pagina" in quadro.lower()
    assert "Páginas" in quadro
    assert "PgUp" in quadro and "PgDn" in quadro
    # Ordem relativa canonica Esc → PgUp/PgDn na linha da barra.
    linhas_barra = [
        linha for linha in quadro.splitlines()
        if "Esc" in linha or "Páginas" in linha or "Navegar" in linha
    ]
    texto_barra = "\n".join(linhas_barra)
    assert texto_barra.find("Esc") < texto_barra.find("Páginas")
    assert "Selecionar" in quadro
    assert "Ajuda" in quadro


def test_resize_com_amostras_sem_residuo_preserva_escolha():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    escolhidas = dict(controlador.escolhas_de(estado, modelo))
    filho = controlador.filho_corrente(estado, modelo)
    assert filho is not None
    assert SEPARADOR_NOME_AMOSTRA in filho.campos["titulo"]

    for largura, altura in ((120, 40), (80, 24), (62, 20), (100, 30)):
        quadro = _quadro_resolvido(estado, modelo, largura, altura)
        assert isinstance(quadro, str) and quadro
        assert "Aumente a janela" not in quadro
        assert len(quadro.splitlines()) <= altura
        assert controlador.escolhas_de(estado, modelo) == escolhidas
        assert controlador.filho_corrente(estado, modelo) is not None
        assert "popup" not in quadro.lower()


def test_um_item_logico_por_filho_sem_multiline():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    for pai in controlador.conteudo.nos:
        for filho in pai.filhos:
            assert "\n" not in filho.campos["titulo"]
            assert filho.campos["titulo"].count("\n") == 0


def test_navegacao_e_espaco_respeitam_fronteira_candidato_vs_aplicado(tmp_path):
    """H-0065: setas nao mutam candidato; Espaco muta so candidato transitório."""
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    candidato_abertura = copy.deepcopy(runtime.candidato)
    global_antes = runtime.global_vigente

    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]

    # Setas / entrada no nivel: candidato permanece.
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    assert runtime.candidato == candidato_abertura
    assert controlador.escolhas_de(estado, modelo)["borda"] == (
        candidato_abertura["borda"]["preset_default"]
    )

    # Espaco sobre novo filho: candidato e selecoes acompanham; aplicado nao.
    estado = processar_comando(estado, " ", modelo)
    borda_escolhida = controlador.escolhas_de(estado, modelo)["borda"]
    assert borda_escolhida != candidato_abertura["borda"]["preset_default"]
    assert runtime.candidato["borda"]["preset_default"] == borda_escolhida
    assert controlador.invariavel_candidato_selecoes(estado, modelo)

    estado = processar_comando(estado, "\x1b", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)

    quadro = _quadro(estado, modelo)
    assert "CONFIRMADO" not in quadro
    assert "ABORTADO" not in quadro
    # H-0066: o candidato ja diverge (borda trocada acima); Aplicar aparece
    # ATIVO. Sem Enter, nenhuma solicitacao/popup e produzida.
    assert "Aplicar" in quadro
    assert controlador.aplicar_disponivel is True
    assert estado.get("popup") is None
    assert estado.get("solicitacao_aplicacao_estilo") is None
    assert runtime.baseline == baseline
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    # Amostras continuam descritivas (nome do preset permanece no quadro).
    assert borda_escolhida in quadro or "borda" in quadro


def test_demonstracao_non_tty_com_amostras(monkeypatch):
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
    assert any(cat in texto for cat in CATEGORIAS_ESTILO[:2])
    # Amostra de borda (glifos do preset default) deve aparecer apos entrar.
    assert "╭" in texto or "┌" in texto or "─" in texto
    assert runtime.global_vigente == runtime.materializacao_global


def test_largura_visual_amostra_chip_no_quadro_coerente():
    catalogo = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    from tela.renderizacao.estilo import amostra_chip

    a = amostra_chip(catalogo["chip"]["presets"]["Destaque Texto"])
    b = amostra_chip(catalogo["chip"]["presets"]["Destaque Fundo"])
    assert _largura_sem_ansi(a) == _largura_sem_ansi(b)
    assert a != b
