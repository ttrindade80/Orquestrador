"""Popup textual modal do H-0056.

Este modulo mantem separadas a declaracao estrutural, resolvida por chave em
``popups``, e o envelope de conteudo recebido pela abertura. O popup nao
carrega dados, nao executa acoes e nao usa a barra de menus como area visual.
"""

import copy
import re
from dataclasses import dataclass

from tela.renderizacao.barra_menus import _texto_chip_barra
from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.geometria_caixa import (
    _borda_de_estilo,
    _caixa,
)
from tela.renderizacao.texto_ansi import _largura_sem_ansi


class PopupErro(RenderizadorErro):
    """Erro de declaracao, envelope ou geometria do popup."""


_ALINHAMENTOS = {"esquerda", "centralizado", "justificado"}
_CAMPOS_POPUP = {
    "tipo",
    "titulo",
    "alinhamento",
    "espacamento_superior",
    "espacamento_conteudo_chips",
    "espacamento_inferior",
    "espacamento_horizontal",
    "chips",
}
_CAMPOS_CHIP = {
    "id",
    "tipo",
    "tecla",
    "texto",
    "acao",
    "referencia_regra",
    "regra_existencia",
    "regra_ativo",
    "forma_exibicao",
}
_CAMPOS_CHIP_OBRIGATORIOS = _CAMPOS_CHIP - {"acao", "referencia_regra"}


@dataclass(frozen=True)
class PopupInstancia:
    """Instancia runtime imutavel por convencao de um popup aberto."""

    declaracao: dict
    conteudo: dict

    @property
    def id(self):
        """ID estrutural resolvido pela chave do mapa ``popups``."""
        return self.declaracao["_id"]


def _raw_da_fonte(fonte):
    if isinstance(fonte, dict):
        return fonte
    raw = getattr(fonte, "_raw", None)
    if isinstance(raw, dict):
        return raw
    raise PopupErro(
        "resolucao de popup exige documento estrutural ou ModeloTela"
    )


def _exigir_texto(valor, caminho):
    if not isinstance(valor, str) or not valor or "\n" in valor or "\r" in valor:
        raise PopupErro("{0} deve ser texto curto sem quebra de linha".format(caminho))
    return valor


def _exigir_espacamento(valor, caminho, minimo, maximo):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise PopupErro("{0} deve ser inteiro".format(caminho))
    if not minimo <= valor <= maximo:
        raise PopupErro(
            "{0} fora do dominio [{1}, {2}]".format(caminho, minimo, maximo)
        )
    return valor


def _validar_chip(chip, indice):
    caminho = "popups.popup_basico.chips[{0}]".format(indice)
    if not isinstance(chip, dict):
        raise PopupErro("{0} deve ser objeto".format(caminho))
    desconhecidos = sorted(set(chip) - _CAMPOS_CHIP)
    if desconhecidos:
        raise PopupErro(
            "{0} possui campos nao autorizados: {1}".format(
                caminho, ", ".join(desconhecidos)
            )
        )
    faltantes = sorted(_CAMPOS_CHIP_OBRIGATORIOS - set(chip))
    if faltantes:
        raise PopupErro(
            "{0} incompleto; ausente: {1}".format(caminho, ", ".join(faltantes))
        )
    if not isinstance(chip.get("acao"), dict) and not isinstance(
        chip.get("referencia_regra"), dict
    ):
        raise PopupErro(
            "{0} exige acao ou referencia_regra".format(caminho)
        )
    if not isinstance(chip["id"], str) or not chip["id"]:
        raise PopupErro("{0}.id invalido".format(caminho))
    if chip["id"] == "popup_basico":
        raise PopupErro("ID do chip deve ser distinto de popup_basico")
    if chip["tipo"] != "especifico":
        raise PopupErro("{0}.tipo deve ser 'especifico'".format(caminho))
    if chip["tecla"] != "Esc":
        raise PopupErro("{0}.tecla deve ser a tecla fisica 'Esc'".format(caminho))
    _exigir_texto(chip["texto"], caminho + ".texto")
    if chip["regra_existencia"] != "sempre":
        raise PopupErro("{0}.regra_existencia deve ser 'sempre'".format(caminho))
    if chip["regra_ativo"] != "sempre":
        raise PopupErro("{0}.regra_ativo deve ser 'sempre'".format(caminho))
    if chip["forma_exibicao"] != "ativo":
        raise PopupErro("{0}.forma_exibicao deve ser 'ativo'".format(caminho))
    referencia = chip.get("referencia_regra")
    if isinstance(referencia, dict):
        resultado = referencia.get("resultado")
        if not isinstance(resultado, dict) or resultado.get("status") != "ABORTADO":
            raise PopupErro(
                "{0}.referencia_regra deve declarar resultado ABORTADO".format(caminho)
            )
    return copy.deepcopy(chip)


def validar_declaracao_popup(declaracao, popup_id="popup_basico"):
    """Valida e copia uma declaracao estrutural sem alterar sua origem."""
    if not isinstance(declaracao, dict):
        raise PopupErro("declaracao de popup deve ser objeto")
    if "id" in declaracao:
        raise PopupErro("declaracao de popup nao aceita id interno redundante")
    if "conteudo" in declaracao:
        raise PopupErro(
            "conteudo concreto nao pertence a declaracao estrutural do popup"
        )
    faltantes = sorted(_CAMPOS_POPUP - set(declaracao))
    if faltantes:
        raise PopupErro(
            "declaracao de popup incompleta; ausente: {0}".format(
                ", ".join(faltantes)
            )
        )
    desconhecidos = sorted(set(declaracao) - _CAMPOS_POPUP)
    if desconhecidos:
        raise PopupErro(
            "campos nao autorizados na declaracao de popup: {0}".format(
                ", ".join(desconhecidos)
            )
        )
    if declaracao["tipo"] != "texto":
        raise PopupErro("popup suporta somente tipo 'texto' neste handoff")
    _exigir_texto(declaracao["titulo"], "popup.titulo")
    if declaracao["alinhamento"] not in _ALINHAMENTOS:
        raise PopupErro(
            "popup.alinhamento deve ser um de: esquerda, centralizado, justificado"
        )
    _exigir_espacamento(declaracao["espacamento_superior"], "popup.espacamento_superior", 0, 1)
    _exigir_espacamento(
        declaracao["espacamento_conteudo_chips"],
        "popup.espacamento_conteudo_chips",
        0,
        1,
    )
    _exigir_espacamento(declaracao["espacamento_inferior"], "popup.espacamento_inferior", 0, 1)
    _exigir_espacamento(
        declaracao["espacamento_horizontal"],
        "popup.espacamento_horizontal",
        1,
        5,
    )
    chips = declaracao["chips"]
    if not isinstance(chips, list) or len(chips) != 1:
        raise PopupErro("popup deve declarar exatamente um chip Esc")
    chip = _validar_chip(chips[0], 0)
    if chip["texto"] != "Voltar":
        raise PopupErro("o chip Esc demonstrativo deve ter texto 'Voltar'")
    copia = copy.deepcopy(declaracao)
    copia["chips"] = [chip]
    return copia


def resolver_popup(fonte, popup_id):
    """Resolve ``popups[popup_id]`` sem aceitar IDs internos redundantes."""
    raw = _raw_da_fonte(fonte)
    popups = raw.get("popups")
    if popups is None:
        raise PopupErro("declaracao de popup inexistente: {0!r}".format(popup_id))
    if not isinstance(popups, dict):
        raise PopupErro("popups deve ser um mapa")
    if popup_id not in popups:
        raise PopupErro("ID de popup inexistente: {0!r}".format(popup_id))
    declaracao = validar_declaracao_popup(popups[popup_id], popup_id)
    declaracao["_id"] = popup_id
    return declaracao


def validar_popups(fonte):
    """Valida o campo geral opcional; ausencia e mapa vazio sao validos."""
    raw = _raw_da_fonte(fonte)
    if "popups" not in raw:
        return {}
    popups = raw["popups"]
    if not isinstance(popups, dict):
        raise PopupErro("popups deve ser um mapa")
    resultado = {}
    for popup_id, declaracao in popups.items():
        if not isinstance(popup_id, str) or not popup_id:
            raise PopupErro("ID de popup deve ser chave textual nao vazia")
        resultado[popup_id] = validar_declaracao_popup(declaracao, popup_id)
    return resultado


def validar_conteudo_popup(conteudo):
    """Valida o envelope runtime textual pronto do chamador."""
    if not isinstance(conteudo, dict):
        raise PopupErro("conteudo_popup deve ser objeto")
    if conteudo.get("tipo") != "texto":
        raise PopupErro("conteudo_popup.tipo deve ser 'texto'")
    _exigir_texto(conteudo.get("texto"), "conteudo_popup.texto")
    return copy.deepcopy(conteudo)


def abrir_popup(fonte, popup_id, conteudo):
    """Cria uma instancia sem consumir ou mutar a declaracao estrutural."""
    declaracao = resolver_popup(fonte, popup_id)
    return PopupInstancia(declaracao, validar_conteudo_popup(conteudo))


def consumir_tecla_popup(instancia, tecla):
    """Consome qualquer tecla; Esc encerra com o resultado nao confirmatorio."""
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    if tecla == "\x1b":
        return {"status": "ABORTADO"}
    return None


_VAO_ENTRE_CHIPS_POPUP = 2


def _texto_chip_popup(chip, estilo):
    """Materializa um chip com a mesma primitiva textual da barra."""
    return _texto_chip_barra(chip, estilo, vao=1)


def _erro_geometria(motivo):
    return PopupErro("popup geometria insuficiente: {0}".format(motivo))


def _quebrar_texto(texto, largura_util):
    """Quebra uma string em linhas fisicas sem descartar caracteres."""
    if isinstance(largura_util, bool) or not isinstance(largura_util, int):
        raise _erro_geometria("largura util nao inteira")
    if largura_util <= 0:
        raise _erro_geometria("largura util nao positiva")
    if not texto:
        return [""]

    linhas = []
    corrente = ""

    def emitir_separador(separador):
        nonlocal corrente
        while separador:
            disponivel = largura_util - len(corrente)
            if disponivel == 0:
                linhas.append(corrente)
                corrente = ""
                continue
            corrente += separador[:disponivel]
            separador = separador[disponivel:]
            if len(corrente) == largura_util:
                linhas.append(corrente)
                corrente = ""

    def emitir_palavra(palavra):
        nonlocal corrente
        while palavra:
            if corrente and len(corrente) + len(palavra) > largura_util:
                linhas.append(corrente)
                corrente = ""
                continue
            disponivel = largura_util - len(corrente)
            trecho = palavra[:disponivel]
            corrente += trecho
            palavra = palavra[len(trecho):]
            if len(corrente) == largura_util:
                linhas.append(corrente)
                corrente = ""

    for token in re.findall(r"\S+|\s+", texto):
        if token.isspace():
            emitir_separador(token)
        else:
            emitir_palavra(token)

    if corrente:
        linhas.append(corrente)
    return linhas or [""]


def _justificar_linha(texto, largura):
    comprimento_atual = _largura_sem_ansi(texto)
    extra = largura - comprimento_atual
    if extra <= 0:
        return texto
    partes = re.split(r"(\s+)", texto)
    indices = [
        indice
        for indice in range(1, len(partes) - 1, 2)
        if partes[indice] and partes[indice - 1] and partes[indice + 1]
        and not partes[indice - 1].isspace()
        and not partes[indice + 1].isspace()
    ]
    if not indices:
        return texto + " " * extra
    base, resto = divmod(extra, len(indices))
    for ordem, indice in enumerate(indices):
        adicionais = base + (1 if ordem < resto else 0)
        partes[indice] += " " * adicionais
    return "".join(partes)


def _formatar_linha(texto, largura, alinhamento, margem, ultima=True):
    disponivel = largura - (2 * margem)
    if disponivel < _largura_sem_ansi(texto):
        raise _erro_geometria("linha excede a largura util")
    sobra = disponivel - _largura_sem_ansi(texto)
    if alinhamento == "centralizado":
        esquerda = sobra // 2
        central = " " * esquerda + texto + " " * (sobra - esquerda)
    elif alinhamento == "justificado" and not ultima:
        central = _justificar_linha(texto, disponivel)
    else:
        central = texto + " " * sobra
    return " " * margem + central + " " * margem


def _distribuir_chips(chips, largura_util, estilo):
    """Distribui chips inteiros em linhas, preservando a ordem declarada."""
    if not isinstance(largura_util, int) or isinstance(largura_util, bool):
        raise _erro_geometria("largura util nao inteira")
    textos = [_texto_chip_popup(chip, estilo) for chip in chips]
    if not textos:
        return []
    for texto in textos:
        if _largura_sem_ansi(texto) > largura_util:
            raise _erro_geometria("chip isolado nao cabe na largura util")

    linhas = []
    corrente = ""
    for texto in textos:
        candidato = texto if not corrente else "{}{}{}".format(
            corrente, " " * _VAO_ENTRE_CHIPS_POPUP, texto
        )
        if corrente and _largura_sem_ansi(candidato) > largura_util:
            linhas.append(corrente)
            corrente = texto
        else:
            corrente = candidato
    if corrente:
        linhas.append(corrente)
    return linhas


def _layout_popup(instancia, estilo, largura_corpo=None):
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    declaracao = instancia.declaracao
    texto = instancia.conteudo["texto"]
    margem = declaracao["espacamento_horizontal"]
    textos_chips = [
        _texto_chip_popup(chip, estilo) for chip in declaracao["chips"]
    ]
    chips_uma_linha = " " * _VAO_ENTRE_CHIPS_POPUP
    chips_uma_linha = chips_uma_linha.join(textos_chips)
    largura_intrinseca = max(
        len(declaracao["titulo"]) + 4,
        3 + 2 * margem + max(len(texto), _largura_sem_ansi(chips_uma_linha)),
    )
    if largura_corpo is None:
        largura = largura_intrinseca
    else:
        if isinstance(largura_corpo, bool) or not isinstance(largura_corpo, int):
            raise _erro_geometria("largura fisica do corpo nao inteira")
        largura = min(largura_intrinseca, largura_corpo)

    if largura < len(declaracao["titulo"]) + 4:
        raise _erro_geometria("titulo nao cabe na moldura")
    content_w = largura - 3
    largura_util = content_w - 2 * margem
    if largura_util <= 0:
        raise _erro_geometria("largura util nao positiva")
    linhas_texto = _quebrar_texto(texto, largura_util)
    linhas_chips = _distribuir_chips(
        declaracao["chips"], largura_util, estilo
    )
    altura = (
        2
        + declaracao["espacamento_superior"]
        + len(linhas_texto)
        + declaracao["espacamento_conteudo_chips"]
        + len(linhas_chips)
        + declaracao["espacamento_inferior"]
    )
    return {
        "largura": largura,
        "altura": altura,
        "content_w": content_w,
        "largura_util": largura_util,
        "linhas_texto": linhas_texto,
        "linhas_chips": linhas_chips,
    }


def geometria_popup(instancia, estilo, largura_corpo=None):
    """Calcula a geometria intrinseca ou limitada pelo corpo fisico."""
    layout = _layout_popup(instancia, estilo, largura_corpo=largura_corpo)
    return {"largura": layout["largura"], "altura": layout["altura"]}


def renderizar_popup(instancia, estilo, largura=None):
    """Renderiza a caixa do popup com wrapping e altura derivada."""
    layout = _layout_popup(instancia, estilo, largura_corpo=largura)
    declaracao = instancia.declaracao
    popup_largura = layout["largura"]
    content_w = layout["content_w"]
    margem = declaracao["espacamento_horizontal"]
    linhas = []
    vazio = " " * content_w
    linhas.extend([vazio] * declaracao["espacamento_superior"])
    for indice, texto in enumerate(layout["linhas_texto"]):
        linhas.append(
            _formatar_linha(
                texto,
                content_w,
                declaracao["alinhamento"],
                margem,
                ultima=indice == len(layout["linhas_texto"]) - 1,
            )
        )
    linhas.extend([vazio] * declaracao["espacamento_conteudo_chips"])
    for texto in layout["linhas_chips"]:
        linhas.append(
            _formatar_linha(
                texto, content_w, "centralizado", margem, ultima=True
            )
        )
    linhas.extend([vazio] * declaracao["espacamento_inferior"])
    return _caixa(
        declaracao["titulo"],
        linhas,
        _borda_de_estilo(estilo),
        popup_largura - 2,
        content_w,
        popup_largura - 4,
    )


def sobrepor_no_corpo(corpo, instancia, estilo, largura=None, altura=None):
    """Sobrepoe a caixa no centro do bloco fisico do corpo."""
    if not isinstance(corpo, str):
        raise PopupErro("corpo materializado invalido")
    linhas_corpo = corpo.split("\n")
    if linhas_corpo and linhas_corpo[-1] == "":
        linhas_corpo.pop()
    if not linhas_corpo:
        raise PopupErro("popup exige corpo materializado")
    largura_corpo = max(len(linha) for linha in linhas_corpo)
    altura_corpo = len(linhas_corpo) if altura is None else altura
    if altura_corpo != len(linhas_corpo):
        raise PopupErro("altura fisica do corpo divergente da composicao")
    medidas = _layout_popup(instancia, estilo, largura_corpo=largura_corpo)
    caixa = renderizar_popup(instancia, estilo, largura=largura_corpo).split("\n")
    largura_popup = medidas["largura"]
    if len(caixa) > altura_corpo:
        raise _erro_geometria("altura derivada nao cabe no corpo")
    x = (largura_corpo - largura_popup) // 2
    y = (altura_corpo - len(caixa)) // 2
    for indice, linha in enumerate(caixa):
        linha_atual = linhas_corpo[y + indice]
        if len(linha_atual) < largura_corpo:
            linha_atual = linha_atual.ljust(largura_corpo)
        linhas_corpo[y + indice] = (
            linha_atual[:x]
            + linha
            + linha_atual[x + largura_popup:]
        )
    return "\n".join(linhas_corpo)
