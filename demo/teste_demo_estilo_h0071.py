"""Integração focal da Barra de Menus real para o H-0071."""

import re

import pytest

from tela.carregamento.estilo import (
    carregar_configuracao_estilo,
    materializar_configuracao_estilo,
)
from tela.renderizacao.barra_menus import _texto_chip_barra
from tela.renderizador import _largura_sem_ansi, _linhas_barra


_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_PRESETS = ("Colchete", "Curva", "Ornamental", "Traço", "Ponto", "Destaque Texto", "Destaque Fundo")


def _estilo(nome):
    configuracao = carregar_configuracao_estilo()
    configuracao["chip"]["preset_default"] = nome
    return materializar_configuracao_estilo(configuracao)


def _barra_real():
    return {
        "distribuicao": "horizontal",
        "chips": [
            {
                "id": "chip_pagina_anterior",
                "tecla": "PgUp",
                "texto": "Páginas",
            },
            {
                "id": "chip_pagina_proxima",
                "tecla": "PgDn",
                "texto": "Páginas",
            },
            {"id": "chip_seguinte", "tecla": "?", "texto": "Ajuda"},
        ],
    }


def _sem_ansi(texto):
    return _ANSI.sub("", texto)


@pytest.mark.parametrize("nome", _PRESETS)
def test_barra_real_renderiza_unidade_multitecla_sem_concorrente(nome):
    estilo = _estilo(nome)
    linhas = _linhas_barra(_barra_real(), estilo, content_w=80)
    assert len(linhas) == 1
    linha = linhas[0]
    plain = _sem_ansi(linha)
    esperado = (
        estilo.caractere_esquerdo
        + "PgUp/PgDn"
        + estilo.caractere_direito
    )
    assert esperado in plain
    assert "[PgUp][PgDn]" not in plain
    assert plain.count("PgUp/PgDn") == 1
    assert _largura_sem_ansi(linha) <= 80
    rotulo = "PÁGINAS" if estilo.caixa_alta else "Páginas"
    assert " " + rotulo in plain


def test_barra_real_contem_ansi_antes_da_descricao_e_do_chip_seguinte():
    for nome in ("Destaque Texto", "Destaque Fundo"):
        linha = _linhas_barra(_barra_real(), _estilo(nome), content_w=80)[0]
        plain = _sem_ansi(linha)
        rotulo = "PÁGINAS" if _estilo(nome).caixa_alta else "Páginas"
        assert " " + rotulo + "  " in plain
        fim_descricao = linha.index(" " + rotulo) + len(rotulo) + 1
        proximo = _texto_chip_barra(
            {"tecla": "?", "texto": "Ajuda"}, _estilo(nome), vao=1
        )
        inicio_proximo = linha.index(proximo, fim_descricao)
        assert _ANSI.search(linha[fim_descricao:inicio_proximo]) is None


def test_barra_real_recompoe_apos_troca_de_estilo_e_resize():
    barra = _barra_real()
    saidas = []
    for nome, largura in (
        ("Ponto", 80),
        ("Destaque Texto", 40),
        ("Destaque Fundo", 80),
    ):
        linha = _linhas_barra(barra, _estilo(nome), content_w=largura)[0]
        saidas.append(_sem_ansi(linha))
        assert _largura_sem_ansi(linha) <= largura
    assert " PgUp/PgDn." in saidas[0]
    assert " PgUp/PgDn " in saidas[1]
    assert " PgUp/PgDn " in saidas[2]
    assert all("[PgUp][PgDn]" not in saida for saida in saidas)


def test_barra_real_destaque_texto_sem_fundo_e_colchete_unidade_unica():
    texto = _linhas_barra(_barra_real(), _estilo("Destaque Texto"), content_w=80)[0]
    visivel = _sem_ansi(texto)
    assert " PgUp/PgDn " in visivel
    assert visivel.count("PgUp/PgDn") == 1
    assert "[PgUp][PgDn]" not in visivel
    assert "\x1b[34mPgUp/PgDn\x1b[39m" in texto
    assert "\x1b[44m" not in texto

    colchete = _linhas_barra(_barra_real(), _estilo("Colchete"), content_w=80)[0]
    visivel_colchete = _sem_ansi(colchete)
    rotulo = "PÁGINAS" if _estilo("Colchete").caixa_alta else "Páginas"
    assert "[PgUp/PgDn] {0}".format(rotulo) in visivel_colchete
    assert "[PgUp][PgDn] {0}".format(rotulo) not in visivel_colchete
