"""Popup textual modal do H-0056.

Este modulo mantem separadas a declaracao estrutural, resolvida por chave em
``popups``, e o envelope de conteudo recebido pela abertura. O popup nao
carrega dados, nao executa acoes e nao usa a barra de menus como area visual.
"""

import copy
from dataclasses import dataclass

from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.geometria_caixa import (
    _borda_de_estilo,
    _caixa,
)


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


def _texto_chip_popup(chip, estilo):
    texto = chip["texto"]
    if estilo.caixa_alta:
        texto = texto.upper()
    # As propriedades cromaticas sao materializadas pelo estilo. Esta
    # primitiva textual nao cria uma paleta propria nem introduz ANSI novo.
    _ = (estilo.cor_texto, estilo.cor_fundo)
    return "{0}{1}{2} {3}".format(
        estilo.caractere_esquerdo,
        chip["tecla"],
        estilo.caractere_direito,
        texto,
    )


def geometria_popup(instancia, estilo):
    """Calcula a dimensao intrinseca simples da instancia textual."""
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    declaracao = instancia.declaracao
    texto = instancia.conteudo["texto"]
    chip = _texto_chip_popup(declaracao["chips"][0], estilo)
    horizontal = declaracao["espacamento_horizontal"]
    largura_conteudo = max(len(texto), len(chip)) + 2 * horizontal
    largura = max(len(declaracao["titulo"]) + 4, largura_conteudo + 3)
    altura = (
        4
        + declaracao["espacamento_superior"]
        + declaracao["espacamento_conteudo_chips"]
        + declaracao["espacamento_inferior"]
    )
    return {"largura": largura, "altura": altura}


def _formatar_linha(texto, largura, alinhamento, margem):
    disponivel = largura - (2 * margem)
    if disponivel < len(texto):
        raise PopupErro("geometria de popup insuficiente para texto sem wrapping")
    if alinhamento == "centralizado":
        central = texto.center(disponivel)
    else:
        # Com uma frase curta, justificado coincide com a disposicao inicial;
        # nao ha wrapping nem uma segunda palavra a distribuir.
        central = texto.ljust(disponivel)
    return " " * margem + central + " " * margem


def renderizar_popup(instancia, estilo):
    """Renderiza a caixa do popup usando as primitivas de caixa vigentes."""
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    medidas = geometria_popup(instancia, estilo)
    largura = medidas["largura"]
    inner_w = largura - 2
    content_w = largura - 3
    label_max = largura - 4
    declaracao = instancia.declaracao
    texto_chip = _texto_chip_popup(declaracao["chips"][0], estilo)
    linhas = []
    vazio = " " * content_w
    linhas.extend([vazio] * declaracao["espacamento_superior"])
    linhas.append(
        _formatar_linha(
            instancia.conteudo["texto"],
            content_w,
            declaracao["alinhamento"],
            declaracao["espacamento_horizontal"],
        )
    )
    linhas.extend([vazio] * declaracao["espacamento_conteudo_chips"])
    linhas.append(
        _formatar_linha(
            texto_chip,
            content_w,
            declaracao["alinhamento"],
            declaracao["espacamento_horizontal"],
        )
    )
    linhas.extend([vazio] * declaracao["espacamento_inferior"])
    return _caixa(
        declaracao["titulo"],
        linhas,
        _borda_de_estilo(estilo),
        inner_w,
        content_w,
        label_max,
    )


def sobrepor_no_corpo(corpo, instancia, estilo, largura, altura=None):
    """Sobrepoe a caixa no centro do bloco fisico do corpo."""
    if not isinstance(corpo, str):
        raise PopupErro("corpo materializado invalido")
    linhas_corpo = corpo.split("\n")
    if linhas_corpo and linhas_corpo[-1] == "":
        linhas_corpo.pop()
    if not linhas_corpo:
        raise PopupErro("popup exige corpo materializado")
    altura_corpo = len(linhas_corpo) if altura is None else altura
    if altura_corpo != len(linhas_corpo):
        raise PopupErro("altura fisica do corpo divergente da composicao")
    medidas = geometria_popup(instancia, estilo)
    caixa = renderizar_popup(instancia, estilo).split("\n")
    largura_popup = medidas["largura"]
    if largura_popup > largura or len(caixa) > altura_corpo:
        raise PopupErro("popup nao cabe no corpo sem tratamento de terminal pequeno")
    x = (largura - largura_popup) // 2
    y = (altura_corpo - len(caixa)) // 2
    for indice, linha in enumerate(caixa):
        linha_atual = linhas_corpo[y + indice]
        if len(linha_atual) < largura:
            linha_atual = linha_atual.ljust(largura)
        linhas_corpo[y + indice] = linha_atual[:x] + linha + linha_atual[x + largura_popup:]
    return "\n".join(linhas_corpo)
