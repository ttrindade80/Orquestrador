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

# Tipos estruturais de composicao (H-0012 / ADR-0010). Sao distintos da
# taxonomia funcional fechada (console, lancador, dashboard). Container
# estrutural nao e elemento funcional, nao gera caixa visual propria, nao e
# navegavel e nao tem foco/chip/acao/registry.
TIPOS_ESTRUTURAIS_VALIDOS = {"grupo"}

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


class TelaGrupoInvalido(TelaErro):
    """Invariante do tipo estrutural 'grupo' violada (H-0012)."""


def _caminho_padrao_base():
    """Diretorio raiz do repositorio de scripts (pai de tela/)."""
    return Path(__file__).resolve().parent.parent


def _para_base(caminho_base):
    if caminho_base is None:
        return _caminho_padrao_base()
    if isinstance(caminho_base, Path):
        return caminho_base
    return Path(caminho_base)


def _validar_grupo(elemento, id_grupo):
    """Valida os invariantes do tipo estrutural 'grupo' no H-0012.

    O grupo e container estrutural de composicao, nao elemento funcional.
    Invariantes deste ciclo (H-0012):

    - campo ``elementos`` presente, lista nao vazia, com exatamente 1 item;
    - o item interno tem ``id`` e ``tipo``;
    - o ``tipo`` do item interno e funcional (console/lancador/dashboard);
    - o ``tipo`` do item interno nao e ``"grupo"`` (proibir aninhamento);
    - ``arranjo`` do grupo, se presente, nao e ``"horizontal"`` nem seu
      alias transicional ``"lado_a_lado"`` (ADR-0011; H-0014).

    Mantem o elemento interno como declaracao inerte acessivel ao modelo
    (preservado no dict de saida do loader).
    """
    arranjo = elemento.get("arranjo")
    if arranjo in ("horizontal", "lado_a_lado"):
        raise TelaGrupoInvalido(
            "Grupo '{0}' com arranjo '{1}' e fora de escopo no H-0014 "
            "(arranjo horizontal nao implementado para grupo; "
            "'lado_a_lado' e alias transicional de 'horizontal' — ADR-0011)".format(
                id_grupo, arranjo
            )
        )

    if "elementos" not in elemento:
        raise TelaGrupoInvalido(
            "Grupo '{0}' sem campo 'elementos'".format(id_grupo)
        )

    sub = elemento.get("elementos")
    if not isinstance(sub, list):
        raise TelaGrupoInvalido(
            "Grupo '{0}' com 'elementos' nao e uma lista".format(id_grupo)
        )

    if len(sub) == 0:
        raise TelaGrupoInvalido(
            "Grupo '{0}' com 'elementos' vazio".format(id_grupo)
        )

    if len(sub) > 1:
        raise TelaGrupoInvalido(
            "Grupo '{0}' com mais de 1 elemento interno (H-0012 exige "
            "exatamente 1)".format(id_grupo)
        )

    item = sub[0]
    if not isinstance(item, dict) or "id" not in item:
        raise TelaGrupoInvalido(
            "Elemento interno do grupo '{0}' sem campo 'id'".format(id_grupo)
        )
    id_item = item.get("id")
    if not isinstance(id_item, str) or id_item == "":
        raise TelaGrupoInvalido(
            "Elemento interno do grupo '{0}' com 'id' invalido".format(
                id_grupo
            )
        )

    if "tipo" not in item:
        raise TelaGrupoInvalido(
            "Elemento interno '{0}' do grupo '{1}' sem campo 'tipo'".format(
                id_item, id_grupo
            )
        )
    tipo_item = item.get("tipo")
    if not isinstance(tipo_item, str) or tipo_item == "":
        raise TelaGrupoInvalido(
            "Elemento interno '{0}' do grupo '{1}' com 'tipo' invalido".format(
                id_item, id_grupo
            )
        )

    if tipo_item == "grupo":
        raise TelaGrupoInvalido(
            "Grupo '{0}' contem grupo aninhado (fora de escopo no "
            "H-0012)".format(id_grupo)
        )

    if tipo_item not in TIPOS_CORPO_VALIDOS:
        raise TelaTipoDesconhecido(tipo=tipo_item, id_elemento=id_item)


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
        if tipo in TIPOS_ESTRUTURAIS_VALIDOS:
            _validar_grupo(elemento, id_elemento)
        elif tipo not in TIPOS_CORPO_VALIDOS:
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
