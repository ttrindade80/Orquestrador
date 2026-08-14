"""Integração da composição H-0070 na Barra de Menus real."""

from __future__ import annotations

import re

from tela.carregamento.estilo import definir_preset_candidato
from tela.loader import RuntimeEstilo, carregar_tela
from tela.modelo import construir_modelo
from tela.navegacao import lista_foco
from tela.renderizador import renderizar_tela
from tela.renderizacao.barra_menus import (
    _texto_chip_barra,
    _texto_chip_multitecla,
)
from tela.renderizacao.texto_ansi import (
    _ANSI_RESET_FG,
    _largura_sem_ansi,
    _codigo_ansi_de_cor,
)


_RAIZ_TELAS = "config/telas/demo"


def _par():
    return (
        {"id": "chip_pagina_anterior", "tecla": "PgUp", "texto": ""},
        {"id": "chip_pagina_proxima", "tecla": "PgDn", "texto": "Páginas"},
    )


def _estilo_chip(nome):
    runtime = RuntimeEstilo()
    candidato = runtime.candidato
    definir_preset_candidato(candidato, ("chip", "preset_default"), nome)
    return runtime.materializar_local(candidato)


def _modelo_estado():
    modelo = construir_modelo(
        carregar_tela(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS
        )
    )
    console = modelo.corpo.elementos[0]
    return modelo, console


def _barra_real(estilo, largura=80, pagina=1):
    modelo, console = _modelo_estado()
    return renderizar_tela(
        modelo,
        estilo,
        largura=largura,
        altura=24,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=lista_foco(modelo),
        largura_navegacao=largura,
        paginas_atuais={console.id: pagina},
    )


def _sem_ansi(texto):
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def test_presets_de_uma_tecla_e_delimitado_preservam_composicao():
    chip = {"tecla": "PgUp", "texto": "Páginas"}
    for nome in (
        "Colchete", "Curva", "Ornamental", "Traço", "Ponto",
        "Destaque Texto", "Destaque Fundo",
    ):
        estilo = _estilo_chip(nome)
        esperado = "{0}PgUp{1} {2}".format(
            estilo.caractere_esquerdo,
            estilo.caractere_direito,
            "PÁGINAS" if estilo.caixa_alta else "Páginas",
        )
        assert _sem_ansi(_texto_chip_barra(chip, estilo)) == esperado

    estilo = _estilo_chip("Colchete")
    anterior, proxima = _par()
    assert _sem_ansi(
        _texto_chip_multitecla(
            anterior, proxima, estilo, 1, (False, False), (False, False)
        )
    ) == "[PgUp/PgDn] Páginas"


def test_ponto_multitecla_e_um_chip_com_ponto_unico():
    anterior, proxima = _par()
    texto = _texto_chip_multitecla(
        anterior, proxima, _estilo_chip("Ponto"), 1,
        (False, False), (False, False),
    )
    assert _sem_ansi(texto) == " PgUp/PgDn. PÁGINAS"
    assert _sem_ansi(texto).count(".") == 1


def test_destaque_texto_multitecla_aplica_cor_e_largura_do_chip():
    anterior, proxima = _par()
    estilo = _estilo_chip("Destaque Texto")
    texto = _texto_chip_multitecla(
        anterior, proxima, estilo, 1, (False, False), (False, False)
    )
    assert _sem_ansi(texto) == " PgUp/PgDn  PÁGINAS"
    assert _codigo_ansi_de_cor(estilo.cor_texto) in texto
    assert _ANSI_RESET_FG in texto
    assert _largura_sem_ansi(texto) == len(" PgUp/PgDn  PÁGINAS")
    assert texto.rindex(_ANSI_RESET_FG) < texto.index("PÁGINAS")


def test_destaque_fundo_multitecla_cobre_espacos_laterais():
    anterior, proxima = _par()
    estilo = _estilo_chip("Destaque Fundo")
    texto = _texto_chip_multitecla(
        anterior, proxima, estilo, 1, (False, False), (False, False)
    )
    assert _sem_ansi(texto) == " PgUp/PgDn  PÁGINAS"
    assert "\x1b[44m PgUp/PgDn \x1b[49m" in texto
    assert _largura_sem_ansi(texto) == len(" PgUp/PgDn  PÁGINAS")
    assert texto.index("\x1b[44m") < texto.index(" PgUp/PgDn ")
    assert texto.rindex("\x1b[49m") < texto.index("PÁGINAS")


def test_barra_real_usa_preset_runtime_e_recompoe_apos_resize():
    for nome, trecho in (
        ("Ponto", " PgUp/PgDn. PÁGINAS"),
        ("Destaque Texto", " PgUp/PgDn  PÁGINAS"),
        ("Destaque Fundo", " PgUp/PgDn  PÁGINAS"),
    ):
        estilo = _estilo_chip(nome)
        for largura in (100, 60, 100):
            saida = _barra_real(estilo, largura=largura)
            assert trecho in _sem_ansi(saida)
            linhas = [linha for linha in saida.splitlines() if linha]
            assert all(_largura_sem_ansi(linha) == largura for linha in linhas)
        saida = _barra_real(estilo, largura=80, pagina=2)
        assert trecho in _sem_ansi(saida)
