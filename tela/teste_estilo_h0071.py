"""Testes focais da composição de chips do H-0071."""

import copy
import re

import pytest

from tela.carregamento.estilo import (
    carregar_configuracao_estilo,
    materializar_configuracao_estilo,
)
from tela.estilo import ControladorTelaEstilo
from tela.loader import RuntimeEstilo
from tela.renderizacao.barra_menus import (
    _texto_chip_barra,
    _texto_chip_multitecla,
)
from tela.renderizacao.conteudo_externo import (
    _linhas_apresentacao_hierarquia_com_mapa,
)
from tela.renderizacao.estilo import (
    _ANSI_RESET_BG,
    _largura_sem_ansi,
    amostra_chip,
    compor_chip_multitecla,
)
from tela.renderizacao.texto_ansi import _ANSI_RESET_FG, _codigo_ansi_de_cor


_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_FAMILIAS = ("Colchete", "Curva", "Ornamental", "Traço")
_TODOS_PRESETS = _FAMILIAS + ("Ponto", "Destaque Texto", "Destaque Fundo")
_DELIMITADORES_CANONICOS = {
    "Curva": ("╭", "╮"),
    "Ornamental": ("❲", "❳"),
}


def _sem_ansi(texto):
    return _ANSI.sub("", texto)


def _preset(nome):
    configuracao = carregar_configuracao_estilo()
    configuracao["chip"]["preset_default"] = nome
    return materializar_configuracao_estilo(configuracao)


def _dados_preset(nome, teclas=None):
    configuracao = carregar_configuracao_estilo()
    dados = copy.deepcopy(configuracao["chip"]["presets"][nome])
    if teclas is not None:
        dados["teclas"] = tuple(teclas)
    return dados


@pytest.mark.parametrize("nome", _TODOS_PRESETS)
def test_chip_de_uma_tecla_preserva_forma_em_todos_os_presets(nome):
    dados = _dados_preset(nome)
    esperado = (
        dados["caractere_esquerdo"]
        + "A"
        + dados["caractere_direito"]
    )
    assert _sem_ansi(amostra_chip(dados)) == esperado


@pytest.mark.parametrize("nome", _TODOS_PRESETS)
def test_amostra_multitecla_e_unidade_unica_com_separador_canonico(nome):
    dados = _dados_preset(nome, ("PgUp", "PgDn"))
    visual = amostra_chip(dados)
    esperado = (
        dados["caractere_esquerdo"]
        + "PgUp/PgDn"
        + dados["caractere_direito"]
    )
    assert _sem_ansi(visual) == esperado
    assert "[PgUp][PgDn]" not in _sem_ansi(visual)
    assert _sem_ansi(visual).count("/") == 1
    assert _largura_sem_ansi(visual) == len(esperado)


def test_curva_e_ornamental_distintos_por_expectativa_canonica():
    curva_esq, curva_dir = _DELIMITADORES_CANONICOS["Curva"]
    orn_esq, orn_dir = _DELIMITADORES_CANONICOS["Ornamental"]
    assert (curva_esq, curva_dir) != (orn_esq, orn_dir)

    configuracao = carregar_configuracao_estilo()
    presets = configuracao["chip"]["presets"]
    assert presets["Curva"]["caractere_esquerdo"] == curva_esq
    assert presets["Curva"]["caractere_direito"] == curva_dir
    assert presets["Ornamental"]["caractere_esquerdo"] == orn_esq
    assert presets["Ornamental"]["caractere_direito"] == orn_dir

    amostra_curva = _sem_ansi(amostra_chip(_dados_preset("Curva")))
    amostra_ornamental = _sem_ansi(amostra_chip(_dados_preset("Ornamental")))
    assert amostra_curva == curva_esq + "A" + curva_dir
    assert amostra_ornamental == orn_esq + "A" + orn_dir
    assert amostra_curva != amostra_ornamental

    unidade_curva = _sem_ansi(amostra_chip(_dados_preset("Curva", ("PgUp", "PgDn"))))
    unidade_ornamental = _sem_ansi(
        amostra_chip(_dados_preset("Ornamental", ("PgUp", "PgDn")))
    )
    assert unidade_curva == curva_esq + "PgUp/PgDn" + curva_dir
    assert unidade_ornamental == orn_esq + "PgUp/PgDn" + orn_dir
    assert unidade_curva != unidade_ornamental


def test_ponto_multitecla_tem_espaco_e_um_unico_ponto():
    visual = amostra_chip(_dados_preset("Ponto", ("PgUp", "PgDn")))
    assert _sem_ansi(visual) == " PgUp/PgDn."
    assert _sem_ansi(visual).count(".") == 1


def test_destaque_texto_so_foreground_com_espacos_normais():
    texto = amostra_chip(_dados_preset("Destaque Texto", ("PgUp", "PgDn")))
    visivel = _sem_ansi(texto)
    assert visivel == " PgUp/PgDn "
    assert visivel.startswith(" ")
    assert visivel.endswith(" ")
    assert visivel[0] == " " and visivel[-1] == " "
    assert texto.startswith(" ")
    assert texto.endswith(" ")
    assert "\x1b[34mPgUp/PgDn\x1b[39m" in texto
    assert "\x1b[44m" not in texto
    assert _ANSI_RESET_BG not in texto
    assert not visivel.startswith("\x1b")


def test_destaque_fundo_cobre_unidade_sem_regressao():
    fundo = amostra_chip(_dados_preset("Destaque Fundo", ("PgUp", "PgDn")))
    assert _sem_ansi(fundo) == " PgUp/PgDn "
    assert fundo.startswith("\x1b[44m")
    assert fundo.endswith(_ANSI_RESET_BG)
    assert "\x1b[44m PgUp/PgDn \x1b[49m" in fundo


def test_barra_real_paginas_e_unidade_unica_sem_concatenacao():
    estilo = _preset("Colchete")
    barra = _texto_chip_multitecla(
        {"tecla": "PgUp", "texto": "Páginas"},
        {"tecla": "PgDn", "texto": "Páginas"},
        estilo,
        vao=1,
        estados=(False, False),
        destaques=(False, False),
    )
    visivel = _sem_ansi(barra)
    assert visivel == "[PgUp/PgDn] Páginas"
    assert "[PgUp][PgDn] Páginas" not in visivel
    assert "[PgUp][PgDn]" not in visivel


def test_aplicar_inativo_usa_cor_inativo():
    estilo = _preset("Colchete")
    codigo = _codigo_ansi_de_cor(estilo.cor_inativo)
    texto = _texto_chip_barra(
        {"tecla": "Enter", "texto": "Aplicar"},
        estilo,
        vao=1,
        inativo=True,
    )
    visivel = _sem_ansi(texto)
    assert visivel == "[Enter] Aplicar"
    assert "{0}Enter{1}".format(codigo, _ANSI_RESET_FG) in texto
    assert codigo not in visivel
    assert texto.index(codigo) < texto.index(_ANSI_RESET_FG) < texto.index("Aplicar")


def test_paginas_inativo_usa_cor_inativo():
    estilo = _preset("Colchete")
    codigo = _codigo_ansi_de_cor(estilo.cor_inativo)
    texto = _texto_chip_multitecla(
        {"tecla": "PgUp", "texto": "Páginas"},
        {"tecla": "PgDn", "texto": "Páginas"},
        estilo,
        vao=1,
        estados=(True, True),
        destaques=(False, False),
    )
    visivel = _sem_ansi(texto)
    assert visivel == "[PgUp/PgDn] Páginas"
    assert "[PgUp][PgDn]" not in visivel
    unidade = (
        "[" + codigo + "PgUp" + _ANSI_RESET_FG
        + "/" + codigo + "PgDn" + _ANSI_RESET_FG + "]"
    )
    assert unidade in texto
    assert texto.index(codigo) < texto.index(_ANSI_RESET_FG) < texto.index("Páginas")


@pytest.mark.parametrize("nome", ("Colchete", "Destaque Texto", "Destaque Fundo"))
def test_pgup_pgdn_estados_diferentes_preservados_na_unidade(nome):
    estilo = _preset(nome)
    codigo = _codigo_ansi_de_cor(estilo.cor_inativo)
    texto = _texto_chip_multitecla(
        {"tecla": "PgUp", "texto": "Páginas"},
        {"tecla": "PgDn", "texto": "Páginas"},
        estilo,
        vao=1,
        estados=(True, False),
        destaques=(False, False),
    )
    visivel = _sem_ansi(texto)
    assert "PgUp/PgDn" in visivel
    assert "[PgUp][PgDn]" not in visivel
    assert codigo + "PgUp" + _ANSI_RESET_FG in texto
    trecho_pgdn = texto.split("PgUp", 1)[1]
    assert codigo + "PgDn" not in trecho_pgdn
    assert visivel.count("PgUp/PgDn") == 1


@pytest.mark.parametrize("nome", ("Destaque Texto", "Destaque Fundo"))
def test_preset_nao_neutraliza_cor_inativo(nome):
    estilo = _preset(nome)
    codigo = _codigo_ansi_de_cor(estilo.cor_inativo)
    texto = _texto_chip_multitecla(
        {"tecla": "PgUp", "texto": "Páginas"},
        {"tecla": "PgDn", "texto": "Páginas"},
        estilo,
        vao=1,
        estados=(True, True),
        destaques=(False, False),
    )
    assert codigo + "PgUp" + _ANSI_RESET_FG in texto
    assert codigo + "PgDn" + _ANSI_RESET_FG in texto
    if nome == "Destaque Texto":
        assert _codigo_ansi_de_cor(estilo.cor_texto) + "PgUp" not in texto


def _linhas_filhos_estilo():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    pai = next(
        no for no in controlador.conteudo.nos
        if no.campos.get("categoria") == "chip"
    )
    filhos = list(pai.filhos)
    estilo = RuntimeEstilo().global_vigente
    entradas = _linhas_apresentacao_hierarquia_com_mapa(
        controlador.conteudo,
        content_w=240,
        no_corrente_id=filhos[0].id,
        indicador=estilo.selecionado_simbolo,
        indicador_off=estilo.selecionado_off,
        selecoes={filhos[0].id},
        incluir_selecao=True,
        incluido_on=estilo.incluido_on,
        incluido_off=estilo.incluido_off,
    )
    por_id = {entrada["id"]: entrada["linhas"][0] for entrada in entradas}
    return filhos, por_id, estilo


def test_ec_tg_tx_colunas_distintas_com_e_sem_cursor():
    filhos, linhas, estilo = _linhas_filhos_estilo()
    focal = linhas[filhos[0].id]
    irmao = linhas[filhos[1].id]
    titulo_focal = filhos[0].campos["titulo"]
    titulo_irmao = filhos[1].campos["titulo"]
    col_tx_focal = focal.index(titulo_focal)
    col_tx_irmao = irmao.index(titulo_irmao)
    col_tg_focal = focal.index(estilo.incluido_on)
    col_tg_irmao = irmao.index(estilo.incluido_off)
    col_ec = focal.index(estilo.selecionado_simbolo)

    assert col_ec < col_tg_focal < col_tx_focal
    assert col_tg_focal == col_tg_irmao
    assert col_tx_focal == col_tx_irmao
    assert estilo.selecionado_simbolo not in irmao[:col_tx_irmao]
    assert focal[col_ec + 1:col_tg_focal]
    assert all(ch == " " for ch in focal[col_ec + 1:col_tg_focal])
    assert all(ch == " " for ch in irmao[col_ec:col_tg_irmao])


@pytest.mark.parametrize("nome", _TODOS_PRESETS)
def test_barra_real_e_amostra_usam_a_mesma_unidade_visual(nome):
    estilo = _preset(nome)
    amostra = amostra_chip(_dados_preset(nome, ("PgUp", "PgDn")))
    barra = _texto_chip_multitecla(
        {"tecla": "PgUp", "texto": "Páginas"},
        {"tecla": "PgDn", "texto": "Páginas"},
        estilo,
        vao=1,
        estados=(False, False),
        destaques=(False, False),
    )
    assert _sem_ansi(barra).startswith(_sem_ansi(amostra) + " ")
    rotulo = "PÁGINAS" if estilo.caixa_alta else "Páginas"
    assert _sem_ansi(barra).endswith(" " + rotulo)


def test_estilo_ansi_nao_vaza_para_descricao_ou_chip_seguinte():
    estilo = _preset("Destaque Fundo")
    primeiro = _texto_chip_barra(
        {"tecla": "PgUp", "texto": "Páginas"}, estilo, vao=1
    )
    segundo = _texto_chip_barra(
        {"tecla": "Esc", "texto": "Sair"}, _preset("Curva"), vao=1
    )
    assert primeiro.endswith(" PÁGINAS")
    assert _ANSI.search(primeiro.split(" PÁGINAS", 1)[1]) is None
    assert _ANSI.search((primeiro + "  " + segundo).split(" SAIR", 1)[1]) is None


def test_largura_visual_ignora_ansi_na_unidade_e_no_alinhamento():
    estilo = _preset("Destaque Fundo")
    visual = compor_chip_multitecla(("PgUp", "PgDn"), estilo)
    assert _largura_sem_ansi(visual) == len(" PgUp/PgDn ")
    assert _largura_sem_ansi(visual + "  descrição") == len(" PgUp/PgDn   descrição")
