"""Orquestração macro do carregamento de tela.json."""

import json
import os

from tela.carregamento.caminho_base import _para_base
from tela.carregamento.d23_console import _validar_d23_console
from tela.carregamento.distribuicao_corpo import _validar_distribuicao_corpo
from tela.carregamento.envelope_pre_adr_0028 import _console_em_escopo_d23
from tela.carregamento.erros import (
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaElementoSemId,
    TelaElementoSemTipo,
    TelaEstruturaInvalida,
    TelaIdIncorreto,
    TelaIdNaoCoincideComArquivo,
    TelaJsonInvalido,
    TelaTipoDesconhecido,
)
from tela.carregamento.grupos import _validar_grupo
from tela.carregamento.lancador_config import _carregar_e_validar_config_lancador
from tela.carregamento.perfil_resultado_execucao import _validar_perfil_resultado_execucao
from tela.carregamento.taxonomia import (
    ARRANJOS_CORPO_VALIDOS,
    PERFIL_RESULTADO_EXECUCAO,
    TIPOS_CORPO_VALIDOS,
    TIPOS_ESTRUTURAIS_VALIDOS,
)
from tela.carregamento.validacao_matricial import _validar_distribuicao_matricial

_ID_TELA_RAIZ = "orquestrador"

_PERFIL_AUSENTE = object()

def _tem_lancador_em_elementos(elementos):
    """Verifica recursivamente se algum elemento e do tipo 'lancador'."""
    for e in elementos:
        if not isinstance(e, dict):
            continue
        tipo = e.get("tipo")
        if tipo == "lancador":
            return True
        if tipo == "grupo":
            if _tem_lancador_em_elementos(e.get("elementos", [])):
                return True
    return False


def _iterar_consoles_do_corpo(elementos, caminho="corpo.elementos"):
    """Percorre recursivamente o corpo e rende ``(id, caminho)`` de cada console.

    Inclui consoles aninhados em grupos. Usado para garantir unicidade de
    identidade estavel (contrato_console.md §3; estado de runtime
    cursores/pagina_atual/selecoes indexado por ``console.id``).
    """
    if not isinstance(elementos, list):
        return
    for indice, elemento in enumerate(elementos):
        if not isinstance(elemento, dict):
            continue
        caminho_item = "{0}[{1}]".format(caminho, indice)
        tipo = elemento.get("tipo")
        id_elemento = elemento.get("id")
        if tipo == "console":
            yield id_elemento, caminho_item
        elif tipo == "grupo":
            id_grupo = id_elemento if isinstance(id_elemento, str) else "?"
            yield from _iterar_consoles_do_corpo(
                elemento.get("elementos", []),
                "{0} → {1}.elementos".format(caminho_item, id_grupo),
            )


def _validar_unicidade_ids_consoles(elementos):
    """Rejeita IDs de console duplicados no escopo do ``tela.json``.

    ``cursores``, ``pagina_atual`` e ``selecoes`` usam ``console.id`` como
    chave de estado de runtime; a correspondencia por id no renderer
    (clone paginado vs original) tambem depende dessa unicidade. Duplicatas
    tornam cursor, pagina, selecao e foco inerentemente ambiguos — devem
    ser rejeitadas como erro estrutural antes da construcao do runtime.
    Autoridade: contrato_console.md §3 (``id`` estavel e unico no escopo
    do ``tela.json``). Abrange todos os consoles do corpo (incluidos em
    grupos), nao apenas os focalizaveis ou presentes em ``lista_foco``.
    """
    vistos = {}
    for id_console, caminho in _iterar_consoles_do_corpo(elementos):
        if not isinstance(id_console, str) or id_console == "":
            # id vazio ja e rejeitado antes (TelaElementoSemId / grupo);
            # ignora aqui para nao mascarar o erro canonico anterior.
            continue
        if id_console in vistos:
            raise TelaEstruturaInvalida(
                "id de console duplicado: {0!r} "
                "(ja declarado em {1}; duplicado em {2})".format(
                    id_console, vistos[id_console], caminho
                )
            )
        vistos[id_console] = caminho
def carregar_tela(caminho_base, id_tela, raiz_telas=None):
    """Carrega e valida macro de `<raiz_telas>/<id_tela>.json`.

    Parametros:
        caminho_base: diretorio raiz do repositorio do Orquestrador. Se None,
            usa o pai do diretorio deste modulo (tela/).
        id_tela: identificador estavel da tela. Define o nome do arquivo
            (`<raiz_telas>/<id_tela>.json`) e e comparado ao `id` interno.
        raiz_telas: caminho relativo ao repositorio onde estao os JSONs de
            tela. Se None, usa `config/telas` (raiz do produto real). Para
            a demonstracao, passar `config/telas/demo` explicitamente. Nao
            ha fallback entre raizes: ausencia em uma raiz nao dispara
            tentativa na outra.

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

    if raiz_telas is None:
        raiz_telas = os.path.join("config", "telas")

    caminho_relativo = os.path.join(raiz_telas, id_tela + ".json")
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
        else:
            # H-0035 / ADR-0025: elemento funcional pode declarar
            # distribuicao_matricial (adocao explicita). Ausencia preserva o
            # comportamento anterior. Presenca e validada aqui (26 caminhos).
            if "distribuicao_matricial" in elemento:
                _validar_distribuicao_matricial(
                    elemento["distribuicao_matricial"],
                    "corpo → {0}".format(id_elemento),
                )
            # H-0037 / ADR-0028 D23: valida politica de modo de elementos
            # console. O escopo D23 e determinado estruturalmente por
            # ``_console_em_escopo_d23`` (console consumidor de conteudo
            # multinivel externo, sem envelope pre-ADR-0028), independentemente
            # da presenca de ``formato.excesso``. Legado H-0036 nominalmente
            # reconhecido permanece isento; telas novas/revisadas devem declarar
            # politica_modo obrigatoriamente (ADR-0028 §13.13.3).
            if tipo == "console":
                _fmt_elem = elemento.get("formato", {})
                _excesso_elem = _fmt_elem.get("excesso")
                _validar_d23_console(
                    _excesso_elem if _excesso_elem is not None else {},
                    id_elemento,
                    id_tela=id_interno,
                    em_escopo=_console_em_escopo_d23(elemento, id_interno),
                )
        elementos_internos.append(elemento)

    # H-0045-P04 / QA-H0045-P03-001: IDs de console devem ser unicos no escopo
    # do tela.json antes de qualquer construcao de runtime (cursor/pagina/
    # selecao/foco indexados por id). Deteccao minima apos validar a arvore
    # de elementos e antes de retornar o dict ao modelo.
    _validar_unicidade_ids_consoles(elementos_internos)

    arranjo = corpo.get("arranjo")
    if arranjo not in ARRANJOS_CORPO_VALIDOS:
        raise TelaEstruturaInvalida(
            "corpo.arranjo invalido: {0!r}; valores aceitos: "
            "vertical, horizontal, sobreposto (alias), lado_a_lado (alias)".format(
                arranjo
            )
        )

    # H-0025 / ADR-0018: corpo.distribuicao e OPCIONAL. A ausencia preserva
    # a construcao orientada pelo conteudo (nao materializa "igual"). Quando
    # declarada, e validada e preservada no dict de saida sem conversao.
    distribuicao = corpo.get("distribuicao")
    if distribuicao is not None:
        _validar_distribuicao_corpo(distribuicao, len(elementos_internos))

    # H-0043 / ADR-0036: campo raiz opcional ``perfil``. Valor reconhecido
    # ``resultado_execucao`` exige a estrutura obrigatoria do perfil; valor
    # desconhecido e CONFIGURACAO_INVALIDA. Ausencia permanece valida para
    # telas existentes — exceto quando o id concreto e ``resultado_execucao``.
    perfil = dados.get("perfil", _PERFIL_AUSENTE)
    if perfil is _PERFIL_AUSENTE:
        if id_interno == PERFIL_RESULTADO_EXECUCAO:
            raise TelaCampoObrigatorioAusente(campo="perfil")
        perfil = None
    elif perfil != PERFIL_RESULTADO_EXECUCAO:
        raise TelaEstruturaInvalida(
            "perfil desconhecido: {0!r}; valor reconhecido: {1}".format(
                perfil, PERFIL_RESULTADO_EXECUCAO
            )
        )
    else:
        _validar_perfil_resultado_execucao(
            dados, elementos_internos, distribuicao
        )

    # H-0034 / ADR-0023: carregar parametros normativos do tipo lancador
    # quando ha ao menos um lancador na tela (direto ou em grupo). Carregado
    # uma vez por operacao; propagado ao modelo via _config_lancador.
    config_lancador = None
    if _tem_lancador_em_elementos(elementos_internos):
        config_lancador = _carregar_e_validar_config_lancador(base)

    return {
        "id": id_interno,
        "schema": dados.get("schema"),
        "perfil": perfil,
        "cabecalho": dados.get("cabecalho"),
        "corpo": {
            "arranjo": arranjo,
            "distribuicao": distribuicao,
            "elementos": elementos_internos,
        },
        "barra_de_menus": dados.get("barra_de_menus"),
        "_raw": dados,
        "_config_lancador": config_lancador,
    }
