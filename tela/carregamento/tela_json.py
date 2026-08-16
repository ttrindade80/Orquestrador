"""Orquestração macro do carregamento de tela.json."""

import json
import os

from tela.carregamento.caminho_base import _para_base
from tela.carregamento.d23_console import _validar_d23_console
from tela.carregamento.distribuicao_corpo import _validar_distribuicao_corpo
from tela.carregamento.envelope_pre_adr_0028 import _console_em_escopo_d23
from tela.carregamento.formato_dois_niveis_por_foco import (
    _validar_formato_dois_niveis_filho,
)
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
_CONTROLE_EXECUCAO_AUSENTE = object()
_MODOS_EXECUCAO_VALIDOS = frozenset(("executar", "dry_run"))

_CAMPOS_CABECALHO = frozenset(("titulo", "descricao", "apresentacao"))
_CAMPOS_APRESENTACAO_TITULO = frozenset(
    ("posicao", "recuo_lateral", "capitalizacao", "formato_na_borda")
)
_CAMPOS_APRESENTACAO_DESCRICAO = frozenset(
    ("max_caracteres", "alinhamento", "recuo", "capitalizacao")
)
_POSICOES_CABECALHO = frozenset(("esquerda", "centro", "direita"))
_CAPITALIZACOES_CABECALHO = frozenset(("maiusculas", "inicio_de_frase"))
_CAPITALIZACOES_DESCRICAO = frozenset(
    ("maiusculas", "inicio_de_frase", "preservar")
)
_FORMATO_NA_BORDA_VALIDO = "com_espacos_laterais"


def _validar_objeto_fechado(objeto, caminho, campos_esperados):
    """Valida o tipo e a superfície fechada de um objeto declarativo."""
    if not isinstance(objeto, dict):
        raise TelaEstruturaInvalida(
            "'{0}' nao e um objeto".format(caminho)
        )
    desconhecidos = sorted(set(objeto) - campos_esperados)
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "campo(s) desconhecido(s) em {0}: {1}".format(
                caminho, ", ".join(repr(campo) for campo in desconhecidos)
            )
        )


def _exigir_campo(objeto, campo, caminho):
    if campo not in objeto:
        raise TelaCampoObrigatorioAusente(
            campo="{0}.{1}".format(caminho, campo)
        )
    return objeto[campo]


def _exigir_string(valor, caminho):
    if not isinstance(valor, str):
        raise TelaEstruturaInvalida(
            "'{0}' deve ser string".format(caminho)
        )


def _validar_controle_execucao(controle):
    """Valida a configuração fechada, sem criar estado de runtime."""
    caminho = "controle_execucao"
    if not isinstance(controle, dict):
        raise TelaEstruturaInvalida(
            "CONFIGURACAO_INVALIDA em {0}: esperado objeto".format(caminho)
        )
    desconhecidos = sorted(set(controle) - {"modo_inicial"})
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "CONFIGURACAO_INVALIDA em {0}: campo(s) desconhecido(s) {1!r}".format(
                caminho, desconhecidos
            )
        )
    if "modo_inicial" not in controle:
        raise TelaEstruturaInvalida(
            "CONFIGURACAO_INVALIDA em {0}.modo_inicial: campo ausente".format(
                caminho
            )
        )
    modo = controle["modo_inicial"]
    if not isinstance(modo, str) or modo not in _MODOS_EXECUCAO_VALIDOS:
        raise TelaEstruturaInvalida(
            "CONFIGURACAO_INVALIDA em {0}.modo_inicial: valor {1!r}".format(
                caminho, modo
            )
        )


def _exigir_inteiro_nao_bool(valor, caminho, minimo=None, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TelaEstruturaInvalida(
            "'{0}' deve ser inteiro".format(caminho)
        )
    if minimo is not None and valor < minimo:
        raise TelaEstruturaInvalida(
            "'{0}' deve ser maior ou igual a {1}".format(caminho, minimo)
        )
    if maximo is not None and valor > maximo:
        raise TelaEstruturaInvalida(
            "'{0}' deve ser menor ou igual a {1}".format(caminho, maximo)
        )


def _exigir_enum(valor, caminho, valores):
    if not isinstance(valor, str) or valor not in valores:
        raise TelaEstruturaInvalida(
            "'{0}' invalido: {1!r}; valores aceitos: {2}".format(
                caminho, valor, ", ".join(sorted(valores))
            )
        )


def _validar_cabecalho(cabecalho):
    """Valida integralmente o schema fechado de ``cabecalho``."""
    _validar_objeto_fechado(cabecalho, "cabecalho", _CAMPOS_CABECALHO)

    titulo = _exigir_campo(cabecalho, "titulo", "cabecalho")
    descricao = _exigir_campo(cabecalho, "descricao", "cabecalho")
    apresentacao = _exigir_campo(cabecalho, "apresentacao", "cabecalho")
    _exigir_string(titulo, "cabecalho.titulo")
    _exigir_string(descricao, "cabecalho.descricao")
    _validar_objeto_fechado(
        apresentacao, "cabecalho.apresentacao",
        frozenset(("titulo", "descricao")),
    )

    apresentacao_titulo = _exigir_campo(
        apresentacao, "titulo", "cabecalho.apresentacao"
    )
    apresentacao_descricao = _exigir_campo(
        apresentacao, "descricao", "cabecalho.apresentacao"
    )
    _validar_objeto_fechado(
        apresentacao_titulo, "cabecalho.apresentacao.titulo",
        _CAMPOS_APRESENTACAO_TITULO,
    )
    _validar_objeto_fechado(
        apresentacao_descricao, "cabecalho.apresentacao.descricao",
        _CAMPOS_APRESENTACAO_DESCRICAO,
    )

    caminho_titulo = "cabecalho.apresentacao.titulo"
    posicao = _exigir_campo(apresentacao_titulo, "posicao", caminho_titulo)
    recuo_lateral = _exigir_campo(
        apresentacao_titulo, "recuo_lateral", caminho_titulo
    )
    capitalizacao_titulo = _exigir_campo(
        apresentacao_titulo, "capitalizacao", caminho_titulo
    )
    formato_na_borda = _exigir_campo(
        apresentacao_titulo, "formato_na_borda", caminho_titulo
    )
    _exigir_enum(posicao, caminho_titulo + ".posicao", _POSICOES_CABECALHO)
    _exigir_inteiro_nao_bool(
        recuo_lateral, caminho_titulo + ".recuo_lateral", minimo=0
    )
    _exigir_enum(
        capitalizacao_titulo,
        caminho_titulo + ".capitalizacao",
        _CAPITALIZACOES_CABECALHO,
    )
    if formato_na_borda != _FORMATO_NA_BORDA_VALIDO:
        raise TelaEstruturaInvalida(
            "'{0}.formato_na_borda' invalido: {1!r}; valor aceito: {2}".format(
                caminho_titulo, formato_na_borda, _FORMATO_NA_BORDA_VALIDO
            )
        )

    caminho_descricao = "cabecalho.apresentacao.descricao"
    max_caracteres = _exigir_campo(
        apresentacao_descricao, "max_caracteres", caminho_descricao
    )
    alinhamento = _exigir_campo(
        apresentacao_descricao, "alinhamento", caminho_descricao
    )
    recuo = _exigir_campo(apresentacao_descricao, "recuo", caminho_descricao)
    capitalizacao_descricao = _exigir_campo(
        apresentacao_descricao, "capitalizacao", caminho_descricao
    )
    _exigir_inteiro_nao_bool(
        max_caracteres,
        caminho_descricao + ".max_caracteres",
        minimo=1,
        maximo=200,
    )
    _exigir_enum(
        alinhamento, caminho_descricao + ".alinhamento", _POSICOES_CABECALHO
    )
    _exigir_inteiro_nao_bool(
        recuo, caminho_descricao + ".recuo", minimo=0
    )
    _exigir_enum(
        capitalizacao_descricao,
        caminho_descricao + ".capitalizacao",
        _CAPITALIZACOES_DESCRICAO,
    )

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
    _validar_cabecalho(dados["cabecalho"])

    if "corpo" not in dados:
        raise TelaCampoObrigatorioAusente(campo="corpo")

    if "barra_de_menus" not in dados:
        raise TelaCampoObrigatorioAusente(campo="barra_de_menus")

    controle_execucao = dados.get(
        "controle_execucao", _CONTROLE_EXECUCAO_AUSENTE
    )
    if controle_execucao is not _CONTROLE_EXECUCAO_AUSENTE:
        _validar_controle_execucao(controle_execucao)
    else:
        controle_execucao = None

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
                # H-0072 / ADR-0047: valida formato.dois_niveis_por_foco.filho
                # independentemente do escopo D23 (a regra V-DNF-11 depende
                # apenas de politica_navegacao.tipo, nao do envelope).
                _pol_nav_elem = elemento.get("politica_navegacao")
                _tipo_nav_elem = (
                    _pol_nav_elem.get("tipo")
                    if isinstance(_pol_nav_elem, dict) else None
                )
                _validar_formato_dois_niveis_filho(
                    elemento, id_elemento, _tipo_nav_elem
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
        "controle_execucao": controle_execucao,
        "_raw": dados,
        "_config_lancador": config_lancador,
    }
\n