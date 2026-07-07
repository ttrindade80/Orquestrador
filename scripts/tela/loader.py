"""Loader e validador macro de tela.json (H-0001).

Carrega `config/telas/<id_tela>.json` a partir de um caminho base, valida a
estrutura macro conforme `docs/contratos/contrato_tela_json.md` (secao 3) e
produz uma representacao interna simples e auditavel.

ESCOPO (H-0001):
- Apenas validacao macro (schema, id, cabecalho, corpo, barra_de_menus,
  corpo.elementos[] com id+tipo, taxonomia fechada de tipos).
- Campos declarativos pendentes (bindings, referencias_de_acoes, filtros,
  chips, tela_destino, origem_dados, itens do lancador, etc.) sao carregados
  e preservados como declaracao inerte. Nao sao executados, nao sao
  resolvidos, nao recebem validacao funcional.
- Nao executa acoes, nao ativa bindings, nao resolve tela_destino, nao
  altera JSONs de configuracao.

Apenas biblioteca padrao do Python.
"""

import json
import os
from pathlib import Path


TIPOS_CORPO_VALIDOS = {"console", "lancador", "dashboard"}

_ID_TELA_RAIZ = "orquestrador"


class TelaErro(Exception):
    """Base das excecoes de validacao de tela.json."""


class TelaArquivoNaoEncontrado(TelaErro):
    """Arquivo de tela nao encontrado em disco."""


class TelaJsonInvalido(TelaErro):
    """Conteudo do arquivo nao e JSON sintaticamente valido."""


class TelaCampoObrigatorioAusente(TelaErro):
    """Campo macro obrigatorio ausente ou vazio."""

    def __init__(self, campo):
        self.campo = campo
        super().__init__(
            "Campo obrigatorio ausente: {0}".format(campo)
        )


class TelaIdNaoCoincideComArquivo(TelaErro):
    """id interno diverge do nome base do arquivo."""

    def __init__(self, id_interno, basename):
        self.id_interno = id_interno
        self.basename = basename
        super().__init__(
            "id interno '{0}' nao coincide com nome do arquivo '{1}'".format(
                id_interno, basename
            )
        )


class TelaIdIncorreto(TelaErro):
    """id incorreto para a tela raiz."""

    def __init__(self, encontrado, esperado=_ID_TELA_RAIZ):
        self.encontrado = encontrado
        self.esperado = esperado
        super().__init__(
            "id esperado para tela raiz: '{0}'; encontrado: '{1}'".format(
                esperado, encontrado
            )
        )


class TelaEstruturaInvalida(TelaErro):
    """Estrutura macro invalida (tipo errado, formato errado)."""


class TelaElementoSemId(TelaErro):
    """Elemento de corpo sem campo id."""

    def __init__(self, indice):
        self.indice = indice
        super().__init__(
            "Elemento na posicao {0} nao possui campo 'id'".format(indice)
        )


class TelaElementoSemTipo(TelaErro):
    """Elemento de corpo sem campo tipo."""

    def __init__(self, indice, id_elemento):
        self.indice = indice
        self.id_elemento = id_elemento
        super().__init__(
            "Elemento '{0}' (posicao {1}) nao possui campo 'tipo'".format(
                id_elemento, indice
            )
        )


class TelaTipoDesconhecido(TelaErro):
    """tipo de elemento de corpo fora da taxonomia fechada."""

    def __init__(self, tipo, id_elemento):
        self.tipo = tipo
        self.id_elemento = id_elemento
        super().__init__(
            "Tipo desconhecido '{0}' em elemento '{1}'; tipos validos: "
            "console, lancador, dashboard".format(tipo, id_elemento)
        )


def _caminho_padrao_base():
    """Diretorio raiz do repositorio de scripts (pai de tela/)."""
    return Path(__file__).resolve().parent.parent


def _para_base(caminho_base):
    if caminho_base is None:
        return _caminho_padrao_base()
    if isinstance(caminho_base, Path):
        return caminho_base
    return Path(caminho_base)


def carregar_tela(caminho_base, id_tela):
    """Carrega e valida macro de `config/telas/<id_tela>.json`.

    Parametros:
        caminho_base: diretorio raiz do repositorio de scripts. Se None,
            usa o pai do diretorio deste modulo (tela/).
        id_tela: identificador estavel da tela. Define o nome do arquivo
            (`config/telas/<id_tela>.json`) e e comparado ao `id` interno.

    Retorna:
        dict com representacao interna minima:
            {
                "id": str,
                "schema": str,
                "cabecalho": dict,
                "corpo": {"arranjo": str | None, "elementos": [...]},
                "barra_de_menus": dict,
                "_raw": dict,
            }

    Lanca:
        TelaArquivoNaoEncontrado, TelaJsonInvalido,
        TelaCampoObrigatorioAusente, TelaIdNaoCoincideComArquivo,
        TelaIdIncorreto, TelaEstruturaInvalida,
        TelaElementoSemId, TelaElementoSemTipo, TelaTipoDesconhecido.

    Observacoes:
        - Campos declarativos pendentes (DOC-B008 / DOC-B009) sao
          preservados em `_raw` e nos subdicts como declaracao inerte.
        - Nao executa, nao resolve nem valida funcionalmente esses campos.
    """
    base = _para_base(caminho_base)
    if not isinstance(id_tela, str) or not id_tela:
        raise TelaCampoObrigatorioAusente(campo="id (parametro id_tela)")

    caminho_relativo = os.path.join("config", "telas", id_tela + ".json")
    caminho_arquivo = base / caminho_relativo

    if not caminho_arquivo.is_file():
        raise TelaArquivoNaoEncontrado(
            "Arquivo nao encontrado: {0}".format(caminho_relativo)
        )

    try:
        texto = caminho_arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        raise TelaArquivoNaoEncontrado(
            "Arquivo nao encontrado: {0} ({1})".format(caminho_relativo, exc)
        )

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise TelaJsonInvalido(
            "JSON invalido em: {0} - {1}".format(caminho_relativo, exc)
        )

    if not isinstance(dados, dict):
        raise TelaJsonInvalido(
            "JSON invalido em: {0} - raiz nao e um objeto".format(
                caminho_relativo
            )
        )

    if "schema" not in dados:
        raise TelaCampoObrigatorioAusente(campo="schema")

    id_interno = dados.get("id")
    if not isinstance(id_interno, str) or id_interno == "":
        raise TelaCampoObrigatorioAusente(campo="id")

    basename = caminho_arquivo.stem
    if id_interno != basename:
        raise TelaIdNaoCoincideComArquivo(id_interno, basename)

    if id_tela == _ID_TELA_RAIZ and id_interno != _ID_TELA_RAIZ:
        raise TelaIdIncorreto(encontrado=id_interno)

    if "cabecalho" not in dados:
        raise TelaCampoObrigatorioAusente(campo="cabecalho")

    if "corpo" not in dados:
        raise TelaCampoObrigatorioAusente(campo="corpo")

    if "barra_de_menus" not in dados:
        raise TelaCampoObrigatorioAusente(campo="barra_de_menus")

    corpo = dados.get("corpo")
    if not isinstance(corpo, dict):
        raise TelaEstruturaInvalida(
            "'corpo' nao e um objeto"
        )

    if "elementos" not in corpo:
        raise TelaCampoObrigatorioAusente(campo="corpo.elementos")

    elementos = corpo.get("elementos")
    if not isinstance(elementos, list):
        raise TelaEstruturaInvalida(
            "'corpo.elementos' ausente ou nao e uma lista"
        )

    elementos_internos = []
    for indice, elemento in enumerate(elementos):
        if not isinstance(elemento, dict):
            raise TelaElementoSemId(indice=indice)
        if "id" not in elemento:
            raise TelaElementoSemId(indice=indice)
        id_elemento = elemento.get("id")
        if not isinstance(id_elemento, str) or id_elemento == "":
            raise TelaElementoSemId(indice=indice)
        if "tipo" not in elemento:
            raise TelaElementoSemTipo(indice=indice, id_elemento=id_elemento)
        tipo = elemento.get("tipo")
        if not isinstance(tipo, str) or tipo == "":
            raise TelaElementoSemTipo(indice=indice, id_elemento=id_elemento)
        if tipo not in TIPOS_CORPO_VALIDOS:
            raise TelaTipoDesconhecido(tipo=tipo, id_elemento=id_elemento)
        elementos_internos.append(elemento)

    arranjo = corpo.get("arranjo")

    return {
        "id": id_interno,
        "schema": dados.get("schema"),
        "cabecalho": dados.get("cabecalho"),
        "corpo": {
            "arranjo": arranjo,
            "elementos": elementos_internos,
        },
        "barra_de_menus": dados.get("barra_de_menus"),
        "_raw": dados,
    }
