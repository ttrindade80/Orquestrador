"""Popup textual modal do H-0056.

Este modulo mantem separadas a declaracao estrutural, resolvida por chave em
``popups``, e o envelope de conteudo recebido pela abertura. O popup nao
carrega dados, nao executa acoes e nao usa a barra de menus como area visual.
"""

import copy
import re
from dataclasses import dataclass, field

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
    "marcacao",
    "titulo",
    "alinhamento",
    "espacamento_superior",
    "espacamento_conteudo_chips",
    "espacamento_inferior",
    "espacamento_horizontal",
    "chips",
}
_CAMPOS_POPUP_OBRIGATORIOS = _CAMPOS_POPUP - {"marcacao"}
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
    """Instancia runtime de um popup aberto.

    A declaracao e o envelope continuam sendo copias separadas e estaveis.
    ``_estado`` e a unica parte mutavel: representa o cursor e as marcacoes
    provisarias da modalidade ``marcacao`` durante a vida da mesma instancia.
    """

    declaracao: dict
    conteudo: dict
    _estado: dict = field(default_factory=dict, repr=False, compare=False)

    @property
    def id(self):
        """ID estrutural resolvido pela chave do mapa ``popups``."""
        return self.declaracao["_id"]

    @property
    def cursor_id(self):
        """ID do item corrente; ``None`` para popup textual."""
        return self._estado.get("cursor_id")

    @property
    def cursor(self):
        """Alias legivel para o ID do cursor corrente."""
        return self.cursor_id

    @property
    def marcados(self):
        """IDs marcados na ordem logica declarada."""
        return list(self._estado.get("marcados", ()))

    @property
    def marcacoes(self):
        """Alias legivel para as marcacoes vivas."""
        return self.marcados

    @property
    def formacao(self):
        """Formacao fisica corrente: coluna, matriz ou linha."""
        return self._estado.get("formacao")

    @property
    def grade(self):
        """Grade fisica corrente sem placeholders navegaveis."""
        return tuple(tuple(linha) for linha in self._estado.get("grade", ()))

    @property
    def ultimo_resultado(self):
        """Ultimo resultado interno de navegacao ou marcacao."""
        return self._estado.get("ultimo_resultado")


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
    if chip["tecla"] not in {"Esc", "Enter"}:
        raise PopupErro(
            "{0}.tecla deve ser a tecla fisica 'Esc' ou 'Enter'".format(caminho)
        )
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
        if chip["tecla"] == "Esc":
            if resultado != {"status": "ABORTADO"}:
                raise PopupErro(
                    "{0}.referencia_regra deve declarar resultado ABORTADO sem payload".format(
                        caminho
                    )
                )
        elif resultado != {"status": "CONFIRMADO"}:
            raise PopupErro(
                "{0}.referencia_regra deve declarar resultado CONFIRMADO".format(
                    caminho
                )
            )
    elif chip["tecla"] == "Enter":
        raise PopupErro(
            "{0}.referencia_regra deve declarar resultado CONFIRMADO".format(caminho)
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
    faltantes = sorted(_CAMPOS_POPUP_OBRIGATORIOS - set(declaracao))
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
    if declaracao["tipo"] not in {"texto", "marcacao"}:
        raise PopupErro("popup.tipo deve ser 'texto' ou 'marcacao'")
    if declaracao["tipo"] == "texto":
        if "marcacao" in declaracao:
            raise PopupErro("popup textual nao aceita politica de marcacao")
    else:
        if declaracao.get("marcacao") not in {"exclusiva", "multipla"}:
            raise PopupErro(
                "popup.marcacao deve ser 'exclusiva' ou 'multipla'"
            )
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
    if not isinstance(chips, list) or not 1 <= len(chips) <= 2:
        raise PopupErro("popup deve declarar um chip Esc e, no maximo, um Enter")
    chips_validados = [
        _validar_chip(chip, indice) for indice, chip in enumerate(chips)
    ]
    ids = [chip["id"] for chip in chips_validados]
    if len(set(ids)) != len(ids):
        raise PopupErro("IDs de chips de popup devem ser unicos")
    chips_esc = [chip for chip in chips_validados if chip["tecla"] == "Esc"]
    chips_enter = [chip for chip in chips_validados if chip["tecla"] == "Enter"]
    if len(chips_esc) != 1:
        raise PopupErro("popup deve declarar exatamente um chip Esc")
    if len(chips_enter) > 1:
        raise PopupErro("popup deve declarar no maximo um chip Enter")
    if chips_esc[0]["texto"] != "Voltar":
        raise PopupErro("o chip Esc demonstrativo deve ter texto 'Voltar'")
    if declaracao["tipo"] == "texto" and chips_enter:
        raise PopupErro("popup textual nao aceita regra de confirmacao")
    if chips_enter and chips_enter[0]["texto"] != "Confirmar":
        raise PopupErro("o chip Enter demonstrativo deve ter texto 'Confirmar'")
    copia = copy.deepcopy(declaracao)
    copia["chips"] = chips_validados
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
    """Valida o envelope runtime pronto, sem incorporar estado vivo."""
    if not isinstance(conteudo, dict):
        raise PopupErro("conteudo_popup deve ser objeto")
    if conteudo.get("tipo") == "texto":
        _exigir_texto(conteudo.get("texto"), "conteudo_popup.texto")
        return copy.deepcopy(conteudo)
    if conteudo.get("tipo") != "marcacao":
        raise PopupErro("conteudo_popup.tipo deve ser 'texto' ou 'marcacao'")
    campos = {"tipo", "instrucao", "itens", "marcados"}
    desconhecidos = sorted(set(conteudo) - campos)
    if desconhecidos:
        raise PopupErro(
            "conteudo_popup possui campos nao autorizados: {0}".format(
                ", ".join(desconhecidos)
            )
        )
    if set(conteudo) != campos:
        raise PopupErro(
            "conteudo_popup de marcacao exige tipo, instrucao, itens e marcados"
        )
    _exigir_texto(conteudo["instrucao"], "conteudo_popup.instrucao")
    itens = conteudo["itens"]
    if not isinstance(itens, list) or not itens:
        raise PopupErro("conteudo_popup.itens deve ser lista nao vazia")
    ids = []
    for indice, item in enumerate(itens):
        caminho = "conteudo_popup.itens[{0}]".format(indice)
        if not isinstance(item, dict):
            raise PopupErro("{0} deve ser objeto".format(caminho))
        if set(item) != {"id", "texto"}:
            raise PopupErro("{0} deve conter somente id e texto".format(caminho))
        item_id = item["id"]
        if not isinstance(item_id, str) or not item_id:
            raise PopupErro("{0}.id invalido".format(caminho))
        if item_id in ids:
            raise PopupErro("ID duplicado em {0}.id".format(caminho))
        _exigir_texto(item["texto"], caminho + ".texto")
        ids.append(item_id)
    marcados = conteudo["marcados"]
    if not isinstance(marcados, list):
        raise PopupErro("conteudo_popup.marcados deve ser lista")
    if any(not isinstance(item_id, str) or not item_id for item_id in marcados):
        raise PopupErro("conteudo_popup.marcados deve conter IDs textuais")
    if any(marcados.count(item_id) > 1 for item_id in marcados):
        raise PopupErro("conteudo_popup.marcados nao pode conter duplicatas")
    if any(item_id not in ids for item_id in marcados):
        raise PopupErro("conteudo_popup.marcados referencia ID inexistente")
    return copy.deepcopy(conteudo)


def _estado_inicial_marcacao(declaracao, conteudo):
    """Cria o estado vivo sem copiar politica para o envelope."""
    if conteudo.get("tipo") != "marcacao":
        return {}
    ids = [item["id"] for item in conteudo["itens"]]
    marcados = [item_id for item_id in ids if item_id in conteudo["marcados"]]
    if declaracao["marcacao"] == "exclusiva" and len(marcados) != 1:
        raise PopupErro("marcacao exclusiva exige exatamente uma marcacao")
    return {
        "cursor_id": ids[0],
        "marcados": marcados,
        "formacao": "coluna",
        "grade": [[item_id] for item_id in ids],
        "colunas": [ids],
        "ultimo_resultado": None,
    }


def abrir_popup(fonte, popup_id, conteudo):
    """Cria uma instancia sem consumir ou mutar a declaracao estrutural."""
    declaracao = resolver_popup(fonte, popup_id)
    envelope = validar_conteudo_popup(conteudo)
    if declaracao["tipo"] == "texto" and envelope["tipo"] != "texto":
        raise PopupErro("popup textual exige envelope tipo 'texto'")
    if declaracao["tipo"] == "marcacao" and envelope["tipo"] != "marcacao":
        raise PopupErro("popup de marcacao exige envelope tipo 'marcacao'")
    estado = _estado_inicial_marcacao(declaracao, envelope)
    return PopupInstancia(declaracao, envelope, estado)


def consumir_tecla_popup(instancia, tecla):
    """Consome a tecla na modalidade vigente e produz resultados terminais."""
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    if instancia._estado.get("_resultado_terminal"):
        return None
    if tecla == "\x1b":
        resultado = {"status": "ABORTADO"}
        instancia._estado["_resultado_terminal"] = True
        return resultado
    if instancia.declaracao.get("tipo") != "marcacao":
        return None
    if tecla in {"\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"}:
        resultado = _navegar_marcacao(instancia, tecla)
        instancia._estado["ultimo_resultado"] = resultado
        return resultado
    if tecla == " ":
        resultado = _alternar_marcacao(instancia)
        instancia._estado["ultimo_resultado"] = resultado
        return resultado
    if tecla in {"\r", "\n"}:
        return _confirmar_marcacao(instancia)
    return None


def _ids_marcacao(instancia):
    return [item["id"] for item in instancia.conteudo["itens"]]


def _reconciliar_estado_marcacao(instancia):
    """Mantem cursor/marcacoes validos por ID e na ordem declarada."""
    estado = instancia._estado
    ids = _ids_marcacao(instancia)
    ids_validos = set(ids)
    cursor = estado.get("cursor_id")
    if cursor not in ids_validos:
        estado["cursor_id"] = ids[0]
    marcados = estado.get("marcados", [])
    marcados_validos = set(marcados) & ids_validos
    ordenados = [item_id for item_id in ids if item_id in marcados_validos]
    if instancia.declaracao["marcacao"] == "exclusiva":
        if not ordenados:
            ordenados = [estado["cursor_id"]]
        else:
            ordenados = ordenados[:1]
    estado["marcados"] = ordenados


def _regra_confirmacao_declarada(instancia):
    """Retorna a regra Enter somente quando o contrato é compatível."""
    for chip in instancia.declaracao.get("chips", ()):
        if chip.get("tecla") != "Enter":
            continue
        referencia = chip.get("referencia_regra")
        if isinstance(referencia, dict) and referencia.get("resultado") == {
            "status": "CONFIRMADO"
        }:
            return chip
    return None


def _valor_confirmacao(instancia):
    """Reconcile a marcação viva sem transformar estado inválido em valor."""
    estado = instancia._estado
    ids = _ids_marcacao(instancia)
    marcados = estado.get("marcados")
    if not isinstance(marcados, list):
        return False, None
    if len(set(marcados)) != len(marcados):
        return False, None
    if any(item_id not in ids for item_id in marcados):
        return False, None
    marcados_ordenados = [item_id for item_id in ids if item_id in marcados]
    if instancia.declaracao["marcacao"] == "exclusiva":
        if len(marcados_ordenados) != 1:
            return False, None
        valor = marcados_ordenados[0]
    elif instancia.declaracao["marcacao"] == "multipla":
        valor = marcados_ordenados
    else:
        return False, None
    estado["marcados"] = marcados_ordenados
    return True, valor


def _confirmar_marcacao(instancia):
    if _regra_confirmacao_declarada(instancia) is None:
        return None
    valido, valor = _valor_confirmacao(instancia)
    if not valido:
        return None
    resultado = {"status": "CONFIRMADO", "valor": copy.deepcopy(valor)}
    instancia._estado["_resultado_terminal"] = True
    return resultado


def _grade_para_formacao(ids, formacao, colunas=None):
    if formacao == "coluna":
        return [list(ids)], [[item_id] for item_id in ids]
    if formacao == "linha":
        return [list(ids)], [list(ids)]
    if formacao != "matriz" or not colunas:
        return [list(ids)], [[item_id] for item_id in ids]
    linhas = max(len(coluna) for coluna in colunas)
    grade = []
    for linha in range(linhas):
        grade.append([
            coluna[linha]
            for coluna in colunas
            if linha < len(coluna)
        ])
    return [list(coluna) for coluna in colunas], grade


def _posicoes_grade(grade):
    posicoes = {}
    for linha, ids_linha in enumerate(grade):
        for coluna, item_id in enumerate(ids_linha):
            posicoes[item_id] = (linha, coluna)
    return posicoes


def _ciclo(ids, atual, passo):
    if len(ids) <= 1:
        return None
    indice = ids.index(atual)
    return ids[(indice + passo) % len(ids)]


def _navegar_marcacao(instancia, tecla):
    estado = instancia._estado
    _reconciliar_estado_marcacao(instancia)
    grade = estado.get("grade") or [[estado["cursor_id"]]]
    formacao = estado.get("formacao", "coluna")
    posicoes = _posicoes_grade(grade)
    atual = estado["cursor_id"]
    linha, coluna = posicoes[atual]
    if formacao == "coluna":
        if tecla not in {"\x1b[A", "\x1b[B"}:
            return {"movimento": "SEM_MOVIMENTO"}
        ids_eixo = [ids_linha[0] for ids_linha in grade]
        alvo = _ciclo(ids_eixo, atual, -1 if tecla == "\x1b[A" else 1)
    elif formacao == "linha":
        if tecla not in {"\x1b[C", "\x1b[D"}:
            return {"movimento": "SEM_MOVIMENTO"}
        ids_eixo = grade[0]
        alvo = _ciclo(ids_eixo, atual, 1 if tecla == "\x1b[C" else -1)
    else:
        if tecla in {"\x1b[A", "\x1b[B"}:
            ids_eixo = [ids_linha[coluna] for ids_linha in grade
                        if coluna < len(ids_linha)]
            alvo = _ciclo(ids_eixo, atual, -1 if tecla == "\x1b[A" else 1)
        elif tecla in {"\x1b[C", "\x1b[D"}:
            # O eixo horizontal conserva a linha e ignora somente as celulas
            # vazias dessa mesma linha; nao ha compensacao vertical.
            ids_eixo = list(grade[linha])
            alvo = _ciclo(ids_eixo, atual, 1 if tecla == "\x1b[C" else -1)
        else:
            alvo = None
    if alvo is None:
        return {"movimento": "SEM_MOVIMENTO"}
    estado["cursor_id"] = alvo
    return {"movimento": "MOVIDO"}


def _alternar_marcacao(instancia):
    estado = instancia._estado
    _reconciliar_estado_marcacao(instancia)
    atual = estado["cursor_id"]
    marcados = estado["marcados"]
    if instancia.declaracao["marcacao"] == "exclusiva":
        if marcados == [atual]:
            return {"marcacao": "SEM_MUDANCA"}
        estado["marcados"] = [atual]
        return {"marcacao": "TRANSFERIDA"}
    if atual in marcados:
        estado["marcados"] = [item_id for item_id in marcados if item_id != atual]
        return {"marcacao": "DESMARCADA"}
    ids = _ids_marcacao(instancia)
    estado["marcados"] = [
        item_id for item_id in ids
        if item_id in set(marcados + [atual])
    ]
    return {"marcacao": "MARCADA"}


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


def _largura_grade(colunas):
    larguras = [
        max((_largura_sem_ansi(item_id) for item_id in coluna), default=0)
        for coluna in colunas
    ]
    return sum(larguras) + max(0, len(larguras) - 1) * 2


def _colunas_formacao(ids, larguras, quantidade):
    if quantidade == 1:
        return [list(ids)]
    linhas = (len(ids) + quantidade - 1) // quantidade
    return [
        list(ids[indice * linhas:min((indice + 1) * linhas, len(ids))])
        for indice in range(quantidade)
    ]


def _selecionar_formacao(ids, larguras, largura_util, linhas_disponiveis):
    """Escolhe coluna, menor matriz cabivel ou linha, nessa ordem."""
    largura_coluna = max(larguras)
    if len(ids) <= linhas_disponiveis and largura_coluna <= largura_util:
        return "coluna", _colunas_formacao(ids, larguras, 1)

    for quantidade in range(2, len(ids)):
        colunas = _colunas_formacao(ids, larguras, quantidade)
        linhas = max(len(coluna) for coluna in colunas)
        largura = _largura_grade([
            ["x" * max(
                (larguras[ids.index(item_id)] for item_id in coluna),
                default=0,
            ) for item_id in coluna]
            for coluna in colunas
        ])
        if linhas <= linhas_disponiveis and largura <= largura_util:
            return "matriz", colunas

    largura_linha = sum(larguras) + max(0, len(ids) - 1) * 2
    if linhas_disponiveis >= 1 and largura_linha <= largura_util:
        return "linha", _colunas_formacao(ids, larguras, len(ids))

    if largura_coluna > largura_util:
        raise _erro_geometria("item de marcacao excede a largura util")
    raise _erro_geometria("lista de marcacao excede a altura disponivel")


def _texto_item_marcacao(instancia, item, estilo):
    """Usa os indicadores universais resolvidos para foco e marcacao."""
    item_id = item["id"]
    estado = instancia._estado
    marcado = item_id in estado.get("marcados", ())
    focado = item_id == estado.get("cursor_id")
    foco = getattr(estilo, "selecionado_simbolo", " ")
    if not focado:
        foco = getattr(estilo, "selecionado_off", " ")
    marcado_visual = getattr(estilo, "incluido_on", "")
    if not marcado:
        marcado_visual = getattr(estilo, "incluido_off", "")
    return "{}{} {}".format(foco, marcado_visual, item["texto"])


def _largura_item_marcacao(texto, estilo):
    foco = getattr(estilo, "selecionado_simbolo", " ")
    foco_off = getattr(estilo, "selecionado_off", " ")
    incluido_on = getattr(estilo, "incluido_on", "")
    incluido_off = getattr(estilo, "incluido_off", "")
    return max(
        _largura_sem_ansi(foco), _largura_sem_ansi(foco_off)
    ) + max(
        _largura_sem_ansi(incluido_on), _largura_sem_ansi(incluido_off)
    ) + 1 + _largura_sem_ansi(texto)


def _layout_popup_marcacao(instancia, estilo, largura_corpo=None, altura_corpo=None):
    _reconciliar_estado_marcacao(instancia)
    declaracao = instancia.declaracao
    conteudo = instancia.conteudo
    margem = declaracao["espacamento_horizontal"]
    itens = conteudo["itens"]
    ids = [item["id"] for item in itens]
    larguras = [
        _largura_item_marcacao(item["texto"], estilo) for item in itens
    ]
    texto_instrucao = conteudo["instrucao"]
    chips_uma_linha = " " * _VAO_ENTRE_CHIPS_POPUP
    chips_uma_linha = chips_uma_linha.join(
        _texto_chip_popup(chip, estilo) for chip in declaracao["chips"]
    )
    largura_linha = sum(larguras) + max(0, len(ids) - 1) * 2
    largura_intrinseca = max(
        len(declaracao["titulo"]) + 4,
        3 + 2 * margem + max(
            len(texto_instrucao), max(larguras), largura_linha,
            _largura_sem_ansi(chips_uma_linha),
        ),
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
    linhas_instrucao = _quebrar_texto(texto_instrucao, largura_util)
    linhas_chips = _distribuir_chips(declaracao["chips"], largura_util, estilo)
    overhead = (
        2
        + declaracao["espacamento_superior"]
        + len(linhas_instrucao)
        + declaracao["espacamento_conteudo_chips"]
        + len(linhas_chips)
        + declaracao["espacamento_inferior"]
    )
    if altura_corpo is None:
        linhas_disponiveis = len(ids)
    else:
        if isinstance(altura_corpo, bool) or not isinstance(altura_corpo, int):
            raise _erro_geometria("altura fisica do corpo nao inteira")
        linhas_disponiveis = altura_corpo - overhead
    formacao, colunas = _selecionar_formacao(
        ids, larguras, largura_util, linhas_disponiveis
    )
    colunas_ids, grade = _grade_para_formacao(
        ids, formacao, colunas=colunas
    )
    instancia._estado["formacao"] = formacao
    instancia._estado["colunas"] = colunas_ids
    instancia._estado["grade"] = grade
    _reconciliar_estado_marcacao(instancia)

    itens_por_id = {item["id"]: item for item in itens}
    linhas_itens = []
    for ids_linha in grade:
        partes = [
            _texto_item_marcacao(instancia, itens_por_id[item_id], estilo)
            for item_id in ids_linha
        ]
        linhas_itens.append("  ".join(partes))
    altura = overhead + len(linhas_itens)
    return {
        "largura": largura,
        "altura": altura,
        "content_w": content_w,
        "largura_util": largura_util,
        "linhas_instrucao": linhas_instrucao,
        "linhas_itens": linhas_itens,
        "linhas_chips": linhas_chips,
        "formacao": formacao,
        "grade": grade,
    }


def _layout_popup(instancia, estilo, largura_corpo=None, altura_corpo=None):
    if not isinstance(instancia, PopupInstancia):
        raise PopupErro("instancia de popup invalida")
    if instancia.declaracao.get("tipo") == "marcacao":
        return _layout_popup_marcacao(
            instancia, estilo, largura_corpo=largura_corpo,
            altura_corpo=altura_corpo,
        )
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


def geometria_popup(instancia, estilo, largura_corpo=None, altura_corpo=None):
    """Calcula a geometria intrinseca ou limitada pelo corpo fisico."""
    layout = _layout_popup(
        instancia, estilo, largura_corpo=largura_corpo,
        altura_corpo=altura_corpo,
    )
    return {"largura": layout["largura"], "altura": layout["altura"]}


def renderizar_popup(instancia, estilo, largura=None, altura=None):
    """Renderiza a caixa do popup com wrapping e altura derivada."""
    layout = _layout_popup(
        instancia, estilo, largura_corpo=largura, altura_corpo=altura
    )
    declaracao = instancia.declaracao
    popup_largura = layout["largura"]
    content_w = layout["content_w"]
    margem = declaracao["espacamento_horizontal"]
    linhas = []
    vazio = " " * content_w
    linhas.extend([vazio] * declaracao["espacamento_superior"])
    linhas_texto = layout.get("linhas_texto", layout.get("linhas_instrucao"))
    for indice, texto in enumerate(linhas_texto):
        linhas.append(
            _formatar_linha(
                texto,
                content_w,
                declaracao["alinhamento"],
                margem,
                ultima=indice == len(linhas_texto) - 1,
            )
        )
    if "linhas_itens" in layout:
        for texto in layout["linhas_itens"]:
            linhas.append(
                _formatar_linha(
                    texto, content_w, declaracao["alinhamento"], margem,
                    ultima=True,
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
    medidas = _layout_popup(
        instancia, estilo, largura_corpo=largura_corpo,
        altura_corpo=altura_corpo,
    )
    caixa = renderizar_popup(
        instancia, estilo, largura=largura_corpo, altura=altura_corpo
    ).split("\n")
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
