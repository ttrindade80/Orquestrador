"""Adaptacao de projecao e amostras visuais da tela normal de Estilo (H-0064).

Nao compoe popup, moldura propria nem Cabecalho artesanal. A tela passa pelo
renderer normal; este modulo associa a projecao multinivel ao Console e
compoe, em uma unica linha logica por filho, nome + separador + amostra
derivada dos campos concretos do preset.
"""

from __future__ import annotations

import re

from tela.renderizacao.texto_ansi import (
    _ANSI_RESET_FG,
    _codigo_ansi_de_cor,
    _ljust_sem_ansi,
    _largura_sem_ansi,
)


# Separador estrutural fixo entre nome e amostra (igual para todo filho).
SEPARADOR_NOME_AMOSTRA = "  "

# Payload demonstrativo da amostra de chip na tela de Estilo — uma letra.
PAYLOAD_CANONICO_CHIP = "A"

_ANSI_RESET_BG = "\x1b[49m"
_RE_SGR_NUMERO = re.compile(r"\x1b\[(\d+)m")


def _codigo_ansi_de_fundo(nome_semantico):
    """Deriva SGR de fundo a partir da traducao canonica de foreground.

    Reutiliza ``_codigo_ansi_de_cor`` (paleta unica) e aplica o deslocamento
    estrutural FG→BG do SGR (30–37→40–47, 90–97→100–107). Nao cria catalogo
    paralelo de nomes semânticos.
    """
    codigo_fg = _codigo_ansi_de_cor(nome_semantico)
    if not codigo_fg:
        return ""
    match = _RE_SGR_NUMERO.fullmatch(codigo_fg)
    if match is None:
        return ""
    numero = int(match.group(1))
    if 30 <= numero <= 37:
        return "\x1b[{0}m".format(numero + 10)
    if 90 <= numero <= 97:
        return "\x1b[{0}m".format(numero + 10)
    return ""


def amostra_borda(dados):
    """Amostra compacta de borda em uma linha (H-0064 §6)."""
    return (
        "{canto_superior_esquerdo}{traco_superior}{canto_superior_direito}"
        "{lateral}{lateral}"
        "{canto_inferior_esquerdo}{traco_inferior}{canto_inferior_direito}"
    ).format(
        canto_superior_esquerdo=dados["canto_superior_esquerdo"],
        traco_superior=dados["traco_superior"],
        canto_superior_direito=dados["canto_superior_direito"],
        lateral=dados["lateral"],
        canto_inferior_esquerdo=dados["canto_inferior_esquerdo"],
        traco_inferior=dados["traco_inferior"],
        canto_inferior_direito=dados["canto_inferior_direito"],
    )


def _valor_estilo(dados, campo, padrao=None):
    """Le um campo de estilo tanto de dicts de preset quanto de runtime."""
    if isinstance(dados, dict):
        return dados.get(campo, padrao)
    return getattr(dados, campo, padrao)


def _conteudo_chip(teclas, dados, estados=None, destaques=None):
    """Compõe o conteúdo textual de uma unidade visual de chip.

    A composição é compartilhada pela amostra da tela de Estilo e pela Barra
    real. Delimitadores pertencem somente às extremidades da unidade; o
    separador estrutural entre teclas é sempre ``/``.
    """
    estados = tuple(estados or (False,) * len(teclas))
    destaques = tuple(destaques or (False,) * len(teclas))
    cor_texto = _valor_estilo(dados, "cor_texto", "padrão")
    cor_fundo = _valor_estilo(dados, "cor_fundo", "padrão")
    cor_alerta = _valor_estilo(dados, "cor_alerta", "padrão")
    cor_inativo = _valor_estilo(dados, "cor_inativo", "padrão")

    payload = "/".join(teclas)
    codigo_fg = _codigo_ansi_de_cor(cor_texto)
    codigo_bg = _codigo_ansi_de_fundo(cor_fundo)

    tem_estado_por_tecla = any(estados) or any(destaques)
    if tem_estado_por_tecla:
        partes = []
        for tecla, inativo, destacado in zip(teclas, estados, destaques):
            if inativo:
                codigo = _codigo_ansi_de_cor(cor_inativo)
            elif destacado:
                codigo = _codigo_ansi_de_cor(cor_alerta)
            else:
                codigo = codigo_fg
            if codigo:
                partes.append("{0}{1}{2}".format(codigo, tecla, _ANSI_RESET_FG))
            else:
                partes.append(tecla)
        conteudo = "/".join(partes)
    elif codigo_fg:
        conteudo = "{0}{1}{2}".format(codigo_fg, payload, _ANSI_RESET_FG)
    else:
        conteudo = payload

    esquerdo = _valor_estilo(dados, "caractere_esquerdo", "")
    direito = _valor_estilo(dados, "caractere_direito", "")
    if codigo_bg:
        return "{0}{1}{2}{3}{4}".format(
            codigo_bg, esquerdo, conteudo, direito, _ANSI_RESET_BG,
        )
    return "{0}{1}{2}".format(esquerdo, conteudo, direito)


def compor_chip_multitecla(teclas, dados, estados=None, destaques=None):
    """Retorna uma unidade visual para qualquer quantidade de teclas."""
    teclas = tuple(str(tecla) for tecla in teclas)
    if not teclas:
        return ""
    return _conteudo_chip(teclas, dados, estados, destaques)


def amostra_chip(dados):
    """Amostra de chip usando a mesma composição da Barra real."""
    teclas = dados.get("teclas")
    if teclas is None:
        teclas = (PAYLOAD_CANONICO_CHIP,)
    elif isinstance(teclas, str):
        teclas = (teclas,)
    return compor_chip_multitecla(teclas, dados)


def amostra_selecionado(dados):
    """Simbolo concreto do preset de indicadores.selecionado."""
    return "{0}".format(dados["simbolo"])


def amostra_incluido(dados):
    """Par on/off concreto, ambos reconheciveis na mesma linha."""
    return "{0}/{1}".format(dados["on"], dados["off"])


def amostra_de_preset(categoria, dados):
    """Deriva a amostra da categoria a partir dos campos do preset."""
    if categoria == "borda":
        return amostra_borda(dados)
    if categoria == "chip":
        return amostra_chip(dados)
    if categoria == "indicadores.selecionado":
        return amostra_selecionado(dados)
    if categoria == "indicadores.incluido":
        return amostra_incluido(dados)
    raise ValueError("categoria de amostra desconhecida: {0!r}".format(categoria))


def compor_titulo_com_amostra(
    nome_preset, categoria, dados, largura_nome=None
):
    """``<nome> + separador canonico + <amostra>`` em uma unica linha logica."""
    nome = nome_preset
    if largura_nome is not None:
        nome = _ljust_sem_ansi(nome, largura_nome)
    return "{0}{1}{2}".format(
        nome,
        SEPARADOR_NOME_AMOSTRA,
        amostra_de_preset(categoria, dados),
    )


def associar_conteudo_estilo(modelo, conteudo):
    """Associa ``conteudo`` ao modelo e a cada Console do corpo."""
    modelo.conteudo_externo = conteudo
    for elemento in modelo.corpo.elementos:
        if getattr(elemento, "tipo", None) == "console":
            elemento.conteudo_externo = conteudo
        elif getattr(elemento, "tipo", None) == "grupo":
            for filho in getattr(elemento, "elementos", ()) or ():
                if getattr(filho, "tipo", None) == "console":
                    filho.conteudo_externo = conteudo
    return modelo


__all__ = [
    "PAYLOAD_CANONICO_CHIP",
    "SEPARADOR_NOME_AMOSTRA",
    "amostra_borda",
    "amostra_chip",
    "amostra_de_preset",
    "amostra_incluido",
    "amostra_selecionado",
    "associar_conteudo_estilo",
    "compor_titulo_com_amostra",
    "compor_chip_multitecla",
    "_codigo_ansi_de_fundo",
    "_largura_sem_ansi",
]
