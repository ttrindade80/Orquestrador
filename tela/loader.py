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

# Arranjos validos para o container raiz corpo (H-0019 / ADR-0011 / ADR-0015).
# Ausencia (None) e "vertical" preservam comportamento atual.
# "horizontal" ativa particionamento contíguo da largura disponível.
# "sobreposto" e "lado_a_lado" sao aliases transicionais literais aceitos.
ARRANJOS_CORPO_VALIDOS = {None, "vertical", "horizontal", "sobreposto", "lado_a_lado"}

# Modos validos de corpo.distribuicao (H-0025 / ADR-0018). A ausencia de
# corpo.distribuicao NAO equivale a "igual": preserva a construcao orientada
# pelo conteudo (ADR-0018 D2). "igual" so existe quando declarado.
MODOS_DISTRIBUICAO_CORPO_VALIDOS = {"igual", "percentual", "fracao"}

ESTRUTURAS_GRUPO_VALIDAS = {None, "livre", "matriz"}

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
    """Diretorio raiz do repositorio do Orquestrador (pai de tela/)."""
    return Path(__file__).resolve().parent.parent


def _eh_numero_nao_bool(valor):
    """True quando valor e int/float mas nao bool (bool e subclasse de int)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _validar_distribuicao_corpo(distribuicao, n_elementos, prefixo_caminho="corpo"):
    """Valida corpo.distribuicao declarado (H-0025 / ADR-0018).

    A distribuicao e OPCIONAL. Esta funcao so e chamada quando o campo existe.
    A ausencia de distribuicao preserva a construcao orientada pelo conteudo
    (ADR-0018 D2) e nao e tratada aqui.

    Regras (H-0025 secao 2; contrato_composicao_corpo.md secao 5.7):

    - deve ser um objeto;
    - ``modo`` em {igual, percentual, fracao};
    - ``igual``: nao exige ``valores`` (pesos equivalentes entre os filhos
      diretos); nao e fallback da ausencia;
    - ``percentual``: um valor por filho direto, todos positivos, soma
      exatamente 100, associacao posicional;
    - ``fracao``: um peso por filho direto, todos estritamente positivos,
      denominador igual a soma dos pesos, associacao posicional;
    - ``len(valores) == n_elementos`` (filhos diretos do container).

    Erros sao levantados como ``TelaEstruturaInvalida`` (categoria ja usada
    para corpo.arranjo), de forma deterministica, sem fallback silencioso.
    Nao muta o dict recebido.

    prefixo_caminho: caminho estrutural do container que declara a distribuicao
    (ex.: "corpo" para o corpo raiz; "corpo → g1" para um grupo). Usado para
    compor mensagens de diagnóstico que reflitam o container afetado.
    """
    _p = prefixo_caminho
    if not isinstance(distribuicao, dict):
        raise TelaEstruturaInvalida(
            "{0}.distribuicao deve ser um objeto; recebido: {1}".format(
                _p, type(distribuicao).__name__
            )
        )

    modo = distribuicao.get("modo")
    if modo not in MODOS_DISTRIBUICAO_CORPO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.modo invalido: {1!r}; valores aceitos: "
            "igual, percentual, fracao".format(_p, modo)
        )

    if modo == "igual":
        # igual nao exige vetor concreto (H-0025 secao 2). Pesos equivalentes
        # sao derivados no renderer ([1]*n). Nao ha validacao de valores aqui.
        return

    valores = distribuicao.get("valores")
    if not isinstance(valores, list):
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.valores invalido para modo {1!r}: "
            "esperado lista".format(_p, modo)
        )

    if len(valores) != n_elementos:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.valores com quantidade {1} divergente da "
            "quantidade de filhos diretos ({2})".format(
                _p, len(valores), n_elementos
            )
        )

    for indice, valor in enumerate(valores):
        if not _eh_numero_nao_bool(valor) or valor <= 0:
            raise TelaEstruturaInvalida(
                "{0}.distribuicao.valores[{1}] invalido: {2!r}; esperado "
                "numero estritamente positivo".format(_p, indice, valor)
            )

    if modo == "percentual" and sum(valores) != 100:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao percentual exige soma igual a 100; soma "
            "encontrada: {1}".format(_p, sum(valores))
        )


# ---------------------------------------------------------------------------
# H-0035 / ADR-0025: validacao de distribuicao_matricial (26 caminhos)
# ---------------------------------------------------------------------------

_DM_CAMPOS_VALIDOS = {
    "formacao", "ordem", "dimensionamento", "espacamento",
    "distribuicao_horizontal", "distribuicao_vertical",
    "ordem_expansao", "politica_resto", "alinhamento_interno",
}
_DM_FORMACAO_POLITICAS = {"preferencia_linhas", "preferencia_colunas", "matriz_fixa"}
_DM_ORDENS = {"por_linha", "por_coluna"}
_DM_DIM_COLUNAS = {"maior_da_coluna", "uniforme", "minimo_fixo"}
_DM_DIM_LINHAS = {"maior_da_linha", "uniforme", "minimo_fixo"}
_DM_DIST_H = {"inicio", "centro", "fim", "entre_participantes", "uniforme", "margens_limitadas"}
_DM_DIST_V = {"inicio", "centro", "fim", "entre_linhas", "uniforme", "margens_limitadas"}
_DM_EXPANSAO = {"margens_primeiro_depois_vaos", "uniforme_margens_e_vaos", "vaos_primeiro_depois_margens"}
_DM_RESTO = {"ao_primeiro", "ao_ultimo"}
_DM_ALINH_H = {"inicio", "centro", "fim"}
_DM_ALINH_V = {"topo", "centro", "base"}


def _dm_int(valor, minimo, caminho):
    """Exige inteiro nao booleano >= minimo; lanca TelaEstruturaInvalida."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TelaEstruturaInvalida(
            "{0} deve ser inteiro nao booleano; recebido: {1!r}".format(
                caminho, valor
            )
        )
    if valor < minimo:
        raise TelaEstruturaInvalida(
            "{0} deve ser >= {1}; recebido: {2}".format(caminho, minimo, valor)
        )
    return valor


def _dm_literal(valor, aceitos, caminho):
    """Exige string dentro do vocabulario fechado ``aceitos``."""
    if valor not in aceitos:
        raise TelaEstruturaInvalida(
            "{0} invalido: {1!r}; valores aceitos: {2}".format(
                caminho, valor, ", ".join(sorted(aceitos))
            )
        )
    return valor


def _dm_medida(valor, caminho):
    """Valida uma medida ``{minimo: int>=0, maximo?: int>=minimo}``."""
    if not isinstance(valor, dict):
        raise TelaEstruturaInvalida(
            "{0} deve ser objeto com minimo (e maximo opcional)".format(caminho)
        )
    campos_desconhecidos = set(valor) - {"minimo", "maximo"}
    if campos_desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(campos_desconhecidos))
            )
        )
    if "minimo" not in valor:
        raise TelaEstruturaInvalida("{0}.minimo ausente".format(caminho))
    minimo = _dm_int(valor["minimo"], 0, "{0}.minimo".format(caminho))
    if "maximo" in valor and valor["maximo"] is not None:
        maximo = _dm_int(valor["maximo"], 0, "{0}.maximo".format(caminho))
        if maximo < minimo:
            raise TelaEstruturaInvalida(
                "{0}.maximo ({1}) menor que minimo ({2})".format(
                    caminho, maximo, minimo
                )
            )


def _validar_dm_formacao(formacao, caminho):
    if not isinstance(formacao, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(formacao) - {"politica", "linhas", "colunas"}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    if "politica" not in formacao:
        raise TelaEstruturaInvalida("{0}.politica ausente".format(caminho))
    politica = _dm_literal(
        formacao["politica"], _DM_FORMACAO_POLITICAS,
        "{0}.politica".format(caminho),
    )
    matriz_fixa = politica == "matriz_fixa"
    for eixo in ("linhas", "colunas"):
        _validar_dm_formacao_eixo(
            formacao.get(eixo), matriz_fixa,
            "{0}.{1}".format(caminho, eixo),
        )


def _validar_dm_formacao_eixo(eixo_cfg, matriz_fixa, caminho):
    if eixo_cfg is None:
        if matriz_fixa:
            raise TelaEstruturaInvalida(
                "{0}.fixo obrigatorio em politica matriz_fixa".format(caminho)
            )
        return
    if not isinstance(eixo_cfg, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(eixo_cfg) - {"minimo", "maximo", "fixo"}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    if matriz_fixa:
        if "minimo" in eixo_cfg or "maximo" in eixo_cfg:
            raise TelaEstruturaInvalida(
                "{0}: minimo/maximo invalidos em politica matriz_fixa; "
                "use fixo".format(caminho)
            )
        if "fixo" not in eixo_cfg:
            raise TelaEstruturaInvalida(
                "{0}.fixo obrigatorio em politica matriz_fixa".format(caminho)
            )
        _dm_int(eixo_cfg["fixo"], 1, "{0}.fixo".format(caminho))
    else:
        if "fixo" in eixo_cfg:
            raise TelaEstruturaInvalida(
                "{0}.fixo invalido fora de politica matriz_fixa".format(caminho)
            )
        minimo = None
        if "minimo" in eixo_cfg:
            minimo = _dm_int(eixo_cfg["minimo"], 1, "{0}.minimo".format(caminho))
        if "maximo" in eixo_cfg:
            maximo = _dm_int(eixo_cfg["maximo"], 1, "{0}.maximo".format(caminho))
            base = minimo if minimo is not None else 1
            if maximo < base:
                raise TelaEstruturaInvalida(
                    "{0}.maximo ({1}) menor que minimo ({2})".format(
                        caminho, maximo, base
                    )
                )


def _validar_dm_dimensionamento(dim, caminho):
    if not isinstance(dim, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(dim) - {"colunas", "linhas"}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    _validar_dm_dim_eixo(
        dim.get("colunas"), _DM_DIM_COLUNAS, "{0}.colunas".format(caminho)
    )
    _validar_dm_dim_eixo(
        dim.get("linhas"), _DM_DIM_LINHAS, "{0}.linhas".format(caminho)
    )


def _validar_dm_dim_eixo(eixo_cfg, politicas, caminho):
    if not isinstance(eixo_cfg, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(eixo_cfg) - {"politica", "minimo"}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    if "politica" not in eixo_cfg:
        raise TelaEstruturaInvalida("{0}.politica ausente".format(caminho))
    politica = _dm_literal(
        eixo_cfg["politica"], politicas, "{0}.politica".format(caminho)
    )
    if politica == "minimo_fixo":
        if "minimo" not in eixo_cfg:
            raise TelaEstruturaInvalida(
                "{0}.minimo obrigatorio em politica minimo_fixo".format(caminho)
            )
        _dm_int(eixo_cfg["minimo"], 0, "{0}.minimo".format(caminho))
    else:
        if "minimo" in eixo_cfg:
            raise TelaEstruturaInvalida(
                "{0}.minimo invalido fora de politica minimo_fixo".format(caminho)
            )


def _validar_dm_espacamento(esp, caminho):
    if not isinstance(esp, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    medidas = (
        "margem_superior", "margem_inferior", "margem_esquerda",
        "margem_direita", "vao_horizontal", "vao_vertical",
    )
    desconhecidos = set(esp) - set(medidas)
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    for medida in medidas:
        if medida not in esp:
            raise TelaEstruturaInvalida(
                "{0}.{1} ausente".format(caminho, medida)
            )
        _dm_medida(esp[medida], "{0}.{1}".format(caminho, medida))


def _validar_dm_politica_simples(cfg, chave_interna, aceitos, caminho):
    if not isinstance(cfg, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(cfg) - {chave_interna}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    if chave_interna not in cfg:
        raise TelaEstruturaInvalida(
            "{0}.{1} ausente".format(caminho, chave_interna)
        )
    _dm_literal(cfg[chave_interna], aceitos, "{0}.{1}".format(caminho, chave_interna))


def _validar_dm_par_eixos(cfg, aceitos_h, aceitos_v, caminho):
    if not isinstance(cfg, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))
    desconhecidos = set(cfg) - {"horizontal", "vertical"}
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )
    for eixo, aceitos in (("horizontal", aceitos_h), ("vertical", aceitos_v)):
        if eixo not in cfg:
            raise TelaEstruturaInvalida("{0}.{1} ausente".format(caminho, eixo))
        _dm_literal(cfg[eixo], aceitos, "{0}.{1}".format(caminho, eixo))


def _validar_distribuicao_matricial(valor, caminho_elem):
    """Valida o campo ``distribuicao_matricial`` de um elemento funcional.

    Cobre os 26 caminhos normativos (contrato_json_dashboard.md secao 9.2):
    tipos, literais fechados, limites, dependencias condicionais, combinacoes
    invalidas e campos desconhecidos. Erros sao levantados como
    ``TelaEstruturaInvalida`` (erro de dominio) de forma deterministica, sem
    fallback silencioso e sem efeito parcial.
    """
    caminho = "{0}.distribuicao_matricial".format(caminho_elem)
    if not isinstance(valor, dict):
        raise TelaEstruturaInvalida("{0} deve ser objeto".format(caminho))

    desconhecidos = set(valor) - _DM_CAMPOS_VALIDOS
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "{0}: campo(s) desconhecido(s): {1}".format(
                caminho, ", ".join(sorted(desconhecidos))
            )
        )

    for obrigatorio in _DM_CAMPOS_VALIDOS:
        if obrigatorio not in valor:
            raise TelaEstruturaInvalida(
                "{0}.{1} ausente (obrigatorio quando distribuicao_matricial "
                "esta presente)".format(caminho, obrigatorio)
            )

    _validar_dm_formacao(valor["formacao"], "{0}.formacao".format(caminho))
    _dm_literal(valor["ordem"], _DM_ORDENS, "{0}.ordem".format(caminho))
    _validar_dm_dimensionamento(
        valor["dimensionamento"], "{0}.dimensionamento".format(caminho)
    )
    _validar_dm_espacamento(
        valor["espacamento"], "{0}.espacamento".format(caminho)
    )
    _validar_dm_politica_simples(
        valor["distribuicao_horizontal"], "politica", _DM_DIST_H,
        "{0}.distribuicao_horizontal".format(caminho),
    )
    _validar_dm_politica_simples(
        valor["distribuicao_vertical"], "politica", _DM_DIST_V,
        "{0}.distribuicao_vertical".format(caminho),
    )
    _validar_dm_par_eixos(
        valor["ordem_expansao"], _DM_EXPANSAO, _DM_EXPANSAO,
        "{0}.ordem_expansao".format(caminho),
    )
    _validar_dm_par_eixos(
        valor["politica_resto"], _DM_RESTO, _DM_RESTO,
        "{0}.politica_resto".format(caminho),
    )
    _validar_dm_par_eixos(
        valor["alinhamento_interno"], _DM_ALINH_H, _DM_ALINH_V,
        "{0}.alinhamento_interno".format(caminho),
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


def _carregar_e_validar_config_lancador(base):
    """Carrega e valida config/elementos/lancador.json (H-0034 / ADR-0023).

    Retorna dict com os parametros normativos validados (subset de 'layout'):
        {
            "vaos": {
                "chip_texto": {"minimo": int, "maximo": int},
                "entre_itens_colunas_margem": {"minimo": int, "maximo": int}
            },
            "vertical": {
                "margem_borda_superior": int,
                "margem_borda_inferior": int
            }
        }

    Lanca:
        TelaArquivoNaoEncontrado: arquivo ausente ou ilegivel.
        TelaJsonInvalido: conteudo nao e JSON valido.
        TelaCampoObrigatorioAusente: campo normativo obrigatorio ausente.
        TelaEstruturaInvalida: tipo incorreto, booleano, negativo ou min > max.
    """
    caminho_relativo = os.path.join("config", "elementos", "lancador.json")
    caminho_arquivo = base / caminho_relativo

    if not caminho_arquivo.is_file():
        raise TelaArquivoNaoEncontrado(
            "Config do tipo lancador nao encontrada: {0}".format(
                caminho_relativo
            )
        )

    try:
        texto = caminho_arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        raise TelaArquivoNaoEncontrado(
            "Config do tipo lancador nao encontrada: {0} ({1})".format(
                caminho_relativo, exc
            )
        )

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise TelaJsonInvalido(
            "JSON invalido em config do tipo lancador: {0} - {1}".format(
                caminho_relativo, exc
            )
        )

    if not isinstance(dados, dict):
        raise TelaEstruturaInvalida(
            "config/elementos/lancador.json: raiz nao e um objeto"
        )

    def _exigir_int_nao_bool_nao_negativo(valor, campo):
        """Valida int nao-bool nao-negativo; lanca TelaEstruturaInvalida."""
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TelaEstruturaInvalida(
                "config/elementos/lancador.json: {0} deve ser inteiro nao "
                "booleano; recebido: {1!r}".format(campo, valor)
            )
        if valor < 0:
            raise TelaEstruturaInvalida(
                "config/elementos/lancador.json: {0} deve ser >= 0; "
                "recebido: {1}".format(campo, valor)
            )

    layout = dados.get("layout")
    if not isinstance(layout, dict):
        raise TelaCampoObrigatorioAusente(
            "layout (config/elementos/lancador.json)"
        )

    vaos = layout.get("vaos")
    if not isinstance(vaos, dict):
        raise TelaCampoObrigatorioAusente(
            "layout.vaos (config/elementos/lancador.json)"
        )

    chip_texto = vaos.get("chip_texto")
    if not isinstance(chip_texto, dict):
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.chip_texto (config/elementos/lancador.json)"
        )

    ct_min = chip_texto.get("minimo")
    if ct_min is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.chip_texto.minimo (config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(ct_min, "layout.vaos.chip_texto.minimo")

    ct_max = chip_texto.get("maximo")
    if ct_max is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.chip_texto.maximo (config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(ct_max, "layout.vaos.chip_texto.maximo")
    if ct_max < ct_min:
        raise TelaEstruturaInvalida(
            "config/elementos/lancador.json: layout.vaos.chip_texto.maximo "
            "({0}) menor que minimo ({1})".format(ct_max, ct_min)
        )

    entre_itens = vaos.get("entre_itens_colunas_margem")
    if not isinstance(entre_itens, dict):
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.entre_itens_colunas_margem "
            "(config/elementos/lancador.json)"
        )

    ei_min = entre_itens.get("minimo")
    if ei_min is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.entre_itens_colunas_margem.minimo "
            "(config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(
        ei_min, "layout.vaos.entre_itens_colunas_margem.minimo"
    )

    ei_max = entre_itens.get("maximo")
    if ei_max is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vaos.entre_itens_colunas_margem.maximo "
            "(config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(
        ei_max, "layout.vaos.entre_itens_colunas_margem.maximo"
    )
    if ei_max < ei_min:
        raise TelaEstruturaInvalida(
            "config/elementos/lancador.json: "
            "layout.vaos.entre_itens_colunas_margem.maximo ({0}) menor que "
            "minimo ({1})".format(ei_max, ei_min)
        )

    vertical = layout.get("vertical")
    if not isinstance(vertical, dict):
        raise TelaCampoObrigatorioAusente(
            "layout.vertical (config/elementos/lancador.json)"
        )

    m_sup = vertical.get("margem_borda_superior")
    if m_sup is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vertical.margem_borda_superior "
            "(config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(
        m_sup, "layout.vertical.margem_borda_superior"
    )

    m_inf = vertical.get("margem_borda_inferior")
    if m_inf is None:
        raise TelaCampoObrigatorioAusente(
            "layout.vertical.margem_borda_inferior "
            "(config/elementos/lancador.json)"
        )
    _exigir_int_nao_bool_nao_negativo(
        m_inf, "layout.vertical.margem_borda_inferior"
    )

    verificacao = dados.get("verificacao")
    if not isinstance(verificacao, dict):
        raise TelaCampoObrigatorioAusente(
            "verificacao (config/elementos/lancador.json)"
        )

    verif_texto = verificacao.get("texto")
    if not isinstance(verif_texto, dict):
        raise TelaCampoObrigatorioAusente(
            "verificacao.texto (config/elementos/lancador.json)"
        )

    mc = verif_texto.get("max_caracteres")
    if mc is None:
        raise TelaCampoObrigatorioAusente(
            "verificacao.texto.max_caracteres "
            "(config/elementos/lancador.json)"
        )
    if isinstance(mc, bool) or not isinstance(mc, int):
        raise TelaEstruturaInvalida(
            "config/elementos/lancador.json: verificacao.texto.max_caracteres "
            "deve ser inteiro nao booleano; recebido: {0!r}".format(mc)
        )
    if mc <= 0:
        raise TelaEstruturaInvalida(
            "config/elementos/lancador.json: verificacao.texto.max_caracteres "
            "deve ser > 0; recebido: {0}".format(mc)
        )

    return {
        "vaos": {
            "chip_texto": {"minimo": ct_min, "maximo": ct_max},
            "entre_itens_colunas_margem": {"minimo": ei_min, "maximo": ei_max},
        },
        "vertical": {
            "margem_borda_superior": m_sup,
            "margem_borda_inferior": m_inf,
        },
        "verificacao": {"texto": {"max_caracteres": mc}},
    }


def _para_base(caminho_base):
    if caminho_base is None:
        return _caminho_padrao_base()
    if isinstance(caminho_base, Path):
        return caminho_base
    return Path(caminho_base)


def _validar_quantidade_matriz(matriz, eixo, id_grupo, caminho_grupo):
    caminho_eixo = "{0}.matriz.{1}".format(caminho_grupo, eixo)
    dados_eixo = matriz.get(eixo)
    if not isinstance(dados_eixo, dict):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} deve ser um objeto".format(
                id_grupo, caminho_grupo, caminho_eixo
            )
        )

    quantidade = dados_eixo.get("quantidade")
    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade < 2
        or quantidade > 4
    ):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2}.quantidade invalida: {3!r}; "
            "esperado inteiro entre 2 e 4".format(
                id_grupo, caminho_grupo, caminho_eixo, quantidade
            )
        )
    return dados_eixo, quantidade


def _validar_distribuicao_matriz(dados_eixo, quantidade, eixo, id_grupo, caminho_grupo):
    caminho_eixo = "{0}.matriz.{1}".format(caminho_grupo, eixo)
    if "distribuicao" not in dados_eixo:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2}.distribuicao ausente; "
            "distribuicao de {3} e obrigatoria em matriz".format(
                id_grupo, caminho_grupo, caminho_eixo, eixo
            )
        )
    _validar_distribuicao_corpo(
        dados_eixo.get("distribuicao"), quantidade, caminho_eixo
    )


def _validar_celulas_matriz(matriz, sub, id_grupo, caminho_grupo, n_linhas, n_colunas):
    caminho_celulas = "{0}.matriz.celulas".format(caminho_grupo)
    celulas = matriz.get("celulas")
    if not isinstance(celulas, list):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} deve ser uma lista".format(
                id_grupo, caminho_grupo, caminho_celulas
            )
        )

    esperado = n_linhas * n_colunas
    if len(celulas) != esperado:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} com quantidade invalida; "
            "esperado {3}, encontrado {4} (cobertura completa obrigatoria)".format(
                id_grupo, caminho_grupo, caminho_celulas, esperado, len(celulas)
            )
        )

    ids_filhos = []
    for indice, item in enumerate(sub):
        id_item = item.get("id") if isinstance(item, dict) else None
        if not isinstance(id_item, str) or id_item == "":
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': elementos[{2}].id invalido para "
                "cobertura de matriz".format(id_grupo, caminho_grupo, indice)
            )
        ids_filhos.append(id_item)

    ids_filhos_set = set(ids_filhos)
    if len(ids_filhos_set) != len(ids_filhos):
        vistos = set()
        duplicado = None
        for id_item in ids_filhos:
            if id_item in vistos:
                duplicado = id_item
                break
            vistos.add(id_item)
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': elementos[] contem id duplicado para "
            "matriz: {2!r}".format(id_grupo, caminho_grupo, duplicado)
        )

    coordenadas_vistas = set()
    elementos_vistos = set()
    for indice, celula in enumerate(celulas):
        caminho_celula = "{0}[{1}]".format(caminho_celulas, indice)
        if not isinstance(celula, dict):
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} deve ser objeto com linha, "
                "coluna e elemento".format(id_grupo, caminho_grupo, caminho_celula)
            )

        linha = celula.get("linha")
        coluna = celula.get("coluna")
        elemento_ref = celula.get("elemento")

        if not isinstance(linha, int) or isinstance(linha, bool) or linha < 1:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.linha invalida: {3!r}; "
                "coordenadas iniciam em 1".format(
                    id_grupo, caminho_grupo, caminho_celula, linha
                )
            )
        if not isinstance(coluna, int) or isinstance(coluna, bool) or coluna < 1:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.coluna invalida: {3!r}; "
                "coordenadas iniciam em 1".format(
                    id_grupo, caminho_grupo, caminho_celula, coluna
                )
            )
        if not isinstance(elemento_ref, str) or elemento_ref == "":
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.elemento invalido; "
                "celula vazia e proibida".format(
                    id_grupo, caminho_grupo, caminho_celula
                )
            )

        if linha > n_linhas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.linha fora do limite: {3}; "
                "limite de linhas: {4}".format(
                    id_grupo, caminho_grupo, caminho_celula, linha, n_linhas
                )
            )
        if coluna > n_colunas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.coluna fora do limite: {3}; "
                "limite de colunas: {4}".format(
                    id_grupo, caminho_grupo, caminho_celula, coluna, n_colunas
                )
            )

        coordenada = (linha, coluna)
        if coordenada in coordenadas_vistas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} contem coordenada duplicada: "
                "linha={3}, coluna={4}".format(
                    id_grupo, caminho_grupo, caminho_celulas, linha, coluna
                )
            )
        coordenadas_vistas.add(coordenada)

        if elemento_ref in elementos_vistos:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} contem elemento duplicado: {3!r}".format(
                    id_grupo, caminho_grupo, caminho_celulas, elemento_ref
                )
            )
        elementos_vistos.add(elemento_ref)

        if elemento_ref not in ids_filhos_set:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.elemento referencia filho direto "
                "inexistente: {3!r}".format(
                    id_grupo, caminho_grupo, caminho_celula, elemento_ref
                )
            )

    coordenadas_esperadas = {
        (linha, coluna)
        for linha in range(1, n_linhas + 1)
        for coluna in range(1, n_colunas + 1)
    }
    faltantes = coordenadas_esperadas - coordenadas_vistas
    if faltantes:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': cobertura incompleta em matriz.celulas; "
            "coordenadas faltantes: {2!r}".format(
                id_grupo, caminho_grupo, sorted(faltantes)
            )
        )

    filhos_sem_celula = ids_filhos_set - elementos_vistos
    if filhos_sem_celula:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': elementos sem celula na cobertura da matriz: "
            "{2!r}".format(id_grupo, caminho_grupo, sorted(filhos_sem_celula))
        )


def _validar_matriz_grupo(elemento, sub, id_grupo, caminho_grupo):
    matriz = elemento.get("matriz")
    if not isinstance(matriz, dict):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': matriz deve ser objeto obrigatorio em "
            "estrutura: \"matriz\"".format(id_grupo, caminho_grupo)
        )

    linhas, n_linhas = _validar_quantidade_matriz(
        matriz, "linhas", id_grupo, caminho_grupo
    )
    colunas, n_colunas = _validar_quantidade_matriz(
        matriz, "colunas", id_grupo, caminho_grupo
    )
    _validar_distribuicao_matriz(
        linhas, n_linhas, "linhas", id_grupo, caminho_grupo
    )
    _validar_distribuicao_matriz(
        colunas, n_colunas, "colunas", id_grupo, caminho_grupo
    )
    _validar_celulas_matriz(
        matriz, sub, id_grupo, caminho_grupo, n_linhas, n_colunas
    )


def _validar_grupo(elemento, id_grupo, nivel_grupo=1, caminho="corpo"):
    """Valida os invariantes do tipo estrutural 'grupo' (ADR-0019 / H-0027).

    Valida recursivamente com contagem de profundidade exclusivamente por nós
    estruturais ``grupo`` (ADR-0019 D1). Niveis 1, 2 e 3 sao validos; nivel
    4 e invalido e rejeitado com erro determinístico (ADR-0019 D4). Multiplos
    filhos e grupos irmaos sao permitidos (ADR-0019 D5, D6).

    Parametros:
        elemento: dict do grupo a validar.
        id_grupo: id declarado do grupo.
        nivel_grupo: profundidade do grupo atual (1 = filho direto do corpo).
        caminho: string de contexto para diagnostico (ex.: "corpo → g1").
    """
    estrutura = elemento.get("estrutura")
    if estrutura not in ESTRUTURAS_GRUPO_VALIDAS:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com estrutura invalida em {1}.estrutura: "
            "{2!r}; valores aceitos: livre, matriz, ou ausente".format(
                id_grupo, caminho, estrutura
            )
        )

    # Validar arranjo contra o mesmo conjunto do corpo raiz (ADR-0015 / H-0027).
    arranjo = elemento.get("arranjo")
    if estrutura == "matriz" and arranjo is not None:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' declara arranjo em estrutura: \"matriz\"; "
            "arranjo e proibido em matriz".format(id_grupo, caminho)
        )
    if estrutura != "matriz" and arranjo not in ARRANJOS_CORPO_VALIDOS:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com arranjo invalido: {2!r}; "
            "valores aceitos: vertical, horizontal, sobreposto, lado_a_lado, "
            "ou ausente".format(id_grupo, caminho, arranjo)
        )

    if "elementos" not in elemento:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' sem campo 'elementos'".format(
                id_grupo, caminho
            )
        )

    sub = elemento.get("elementos")
    if not isinstance(sub, list):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com 'elementos' nao e uma lista".format(
                id_grupo, caminho
            )
        )

    if len(sub) == 0:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com 'elementos' vazio".format(
                id_grupo, caminho
            )
        )

    # Caminho que inclui o grupo atual, usado em erros dos filhos e na
    # distribuicao (para que mensagens reflitam o container afetado, nao "corpo").
    caminho_grupo = "{0} → {1}".format(caminho, id_grupo)

    if estrutura == "matriz":
        try:
            _validar_matriz_grupo(elemento, sub, id_grupo, caminho_grupo)
        except TelaEstruturaInvalida as exc:
            raise TelaEstruturaInvalida(
                "Grupo '{0}' em '{1}': {2}".format(id_grupo, caminho, exc)
            ) from exc

    # Validar distribuicao do grupo se declarada (ADR-0015 / ADR-0019).
    # Passa caminho_grupo como prefixo para que as mensagens de erro usem o
    # caminho estrutural real (ex.: "corpo → g1.distribuicao.modo invalido")
    # em vez de "corpo.distribuicao.modo invalido" (ACH-005 patch H-0027).
    distribuicao = elemento.get("distribuicao")
    if estrutura != "matriz" and distribuicao is not None:
        try:
            _validar_distribuicao_corpo(distribuicao, len(sub), caminho_grupo)
        except TelaEstruturaInvalida as exc:
            raise TelaEstruturaInvalida(
                "Grupo '{0}' em '{1}': {2}".format(id_grupo, caminho, exc)
            ) from exc

    for sub_indice, item in enumerate(sub):
        if not isinstance(item, dict) or "id" not in item:
            raise TelaGrupoInvalido(
                "Elemento interno na posicao {0} do grupo '{1}' em '{2}' "
                "sem campo 'id'".format(sub_indice, id_grupo, caminho)
            )
        id_item = item.get("id")
        if not isinstance(id_item, str) or id_item == "":
            raise TelaGrupoInvalido(
                "Elemento interno na posicao {0} do grupo '{1}' em '{2}' "
                "com 'id' invalido".format(sub_indice, id_grupo, caminho)
            )

        if "tipo" not in item:
            raise TelaGrupoInvalido(
                "Elemento interno '{0}' do grupo '{1}' em '{2}' sem campo "
                "'tipo'".format(id_item, id_grupo, caminho)
            )
        tipo_item = item.get("tipo")
        if not isinstance(tipo_item, str) or tipo_item == "":
            raise TelaGrupoInvalido(
                "Elemento interno '{0}' do grupo '{1}' em '{2}' com 'tipo' "
                "invalido".format(id_item, id_grupo, caminho)
            )

        if tipo_item == "grupo":
            if nivel_grupo == 3:
                # Grupo filho de grupo no nivel 3 estaria no nivel 4: invalido.
                raise TelaGrupoInvalido(
                    "Grupo '{0}' em '{1}' criaria nivel 4 de grupo, que e "
                    "invalido; maximo e 3 niveis de grupos "
                    "(ADR-0019 D4)".format(id_item, caminho_grupo)
                )
            # Recursao: validar grupo filho com nivel_grupo + 1.
            _validar_grupo(item, id_item, nivel_grupo + 1, caminho_grupo)
        elif tipo_item in TIPOS_CORPO_VALIDOS:
            # H-0035 / ADR-0025: elemento funcional interno de grupo pode
            # declarar distribuicao_matricial (adocao explicita, nivel unico).
            if "distribuicao_matricial" in item:
                _validar_distribuicao_matricial(
                    item["distribuicao_matricial"],
                    "{0} → {1}".format(caminho_grupo, id_item),
                )
        else:
            raise TelaTipoDesconhecido(tipo=tipo_item, id_elemento=id_item)


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
        elementos_internos.append(elemento)

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

    # H-0034 / ADR-0023: carregar parametros normativos do tipo lancador
    # quando ha ao menos um lancador na tela (direto ou em grupo). Carregado
    # uma vez por operacao; propagado ao modelo via _config_lancador.
    config_lancador = None
    if _tem_lancador_em_elementos(elementos_internos):
        config_lancador = _carregar_e_validar_config_lancador(base)

    return {
        "id": id_interno,
        "schema": dados.get("schema"),
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


# ---------------------------------------------------------------------------
# H-0036 / ADR-0026 / ADR-0027: documento externo de conteudo multinivel
# ---------------------------------------------------------------------------
#
# O console recebe conteudo de runtime por um documento externo separado do
# JSON estrutural da tela (ADR-0026 D1-D4). O schema semantico multinivel e as
# 20 validacoes sao decididos e obrigatorios (ADR-0027 D11/D13;
# contrato_json_console.md secao 12). Este loader abre e decodifica o
# documento, executa as 20 validacoes semanticas e devolve o documento
# validado como representacao semantica. NAO calcula geometria, NAO infere
# hierarquia (a hierarquia e declarada por ``filhos``) e NAO reinsere o
# conteudo no objeto bruto do JSON estrutural. As classes de erro reutilizam
# as excecoes de dominio existentes (TelaEstruturaInvalida,
# TelaCampoObrigatorioAusente, TelaJsonInvalido, TelaArquivoNaoEncontrado).

# Apresentacoes previstas (contrato_json_console.md secao 12.2).
APRESENTACOES_CONTEUDO_VALIDAS = {"tabela", "hierarquia", "conjuntos_campos"}

# Tipos de nivel (contrato_json_console.md secao 12.3).
TIPOS_NIVEL_CONTEUDO_VALIDOS = {"container", "conteudo", "nome_valor"}

# Tipos de designador (contrato_json_console.md secao 12.3 / secao 13.7 H-0036).
TIPOS_DESIGNADOR_VALIDOS = {
    "nenhum", "simbolo", "decimal", "alfabetico_minusculo",
    "alfabetico_maiusculo", "romano_minusculo", "romano_maiusculo",
    "decimal_composto", "personalizado",
}

# Blocos especificos por apresentacao (contrato_json_console.md secao 12.2):
# ``tabela`` somente em ``tabela``; ``campos`` somente em ``conjuntos_campos``;
# nenhum bloco especifico em ``hierarquia``.
_BLOCO_ESPECIFICO_POR_APRESENTACAO = {
    "tabela": "tabela",
    "conjuntos_campos": "campos",
}
_BLOCOS_ESPECIFICOS_APRESENTACAO = {"tabela", "campos"}

# Nomes de campo de resultado fisico calculado proibidos no documento externo
# (contrato_json_console.md secao 12.6; H-0036 secao 13.8). Cada nome mapeia
# uma das formas fisicas proibidas normativas. A deteccao rejeita qualquer
# ocorrencia destes nomes de campo em qualquer profundidade do documento.
CAMPOS_RESULTADO_FISICO_PROIBIDOS = {
    "largura_efetiva",        # largura efetiva
    "altura_efetiva",         # altura efetiva
    "linhas_calculadas",      # quantidade fisica calculada de linhas
    "colunas_calculadas",     # quantidade fisica calculada de colunas
    "posicao_final",          # posicao final
    "coordenada_final",       # coordenada fisica final
    "pagina_calculada",       # pagina calculada
    "quebra_pronta",          # quebra fisica pronta
    "truncamento_aplicado",   # truncamento ja aplicado
    "distribuicao_concreta",  # distribuicao concreta do espaco restante
    "celulas_vazias",         # celulas vazias calculadas
    "geometria_final",        # geometria final
    "numeracao_concreta",     # numeracao concreta de designadores
}


def _validar_designador_conteudo(designador, id_nivel, origem):
    """Valida a politica declarativa de designador de um nivel.

    O designador declara a forma do marcador; o renderizador calcula a
    sequencia concreta. O documento externo NAO armazena a numeracao ja
    calculada (contrato_json_console.md secao 12.3 / secao 13.7 do H-0036).
    """
    if not isinstance(designador, dict):
        raise TelaEstruturaInvalida(
            "{0}: nivel {1!r}.designador deve ser objeto".format(origem, id_nivel)
        )
    if "tipo" not in designador:
        raise TelaCampoObrigatorioAusente(
            campo="formato.niveis[{0}].designador.tipo".format(id_nivel)
        )
    tipo_desig = designador["tipo"]
    if tipo_desig not in TIPOS_DESIGNADOR_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: nivel {1!r}.designador.tipo invalido: {2!r}; aceitos: "
            "{3}".format(
                origem, id_nivel, tipo_desig,
                ", ".join(sorted(TIPOS_DESIGNADOR_VALIDOS)),
            )
        )


def _rejeitar_resultados_fisicos_conteudo(obj, origem, caminho="documento"):
    """Rejeita recursivamente campos de resultado fisico calculado (validacao 20).

    Percorre objetos e arrays em qualquer profundidade. Nao amplia a proibicao
    para campos semanticos validos: rejeita apenas os nomes exatos declarados
    em ``CAMPOS_RESULTADO_FISICO_PROIBIDOS`` (contrato_json_console.md 12.6).
    """
    if isinstance(obj, dict):
        for chave, valor in obj.items():
            if chave in CAMPOS_RESULTADO_FISICO_PROIBIDOS:
                raise TelaEstruturaInvalida(
                    "{0}: campo de resultado fisico calculado proibido: "
                    "{1!r} em {2} (contrato_json_console 12.6)".format(
                        origem, chave, caminho
                    )
                )
            _rejeitar_resultados_fisicos_conteudo(
                valor, origem, "{0}.{1}".format(caminho, chave)
            )
    elif isinstance(obj, list):
        for indice, item in enumerate(obj):
            _rejeitar_resultados_fisicos_conteudo(
                item, origem, "{0}[{1}]".format(caminho, indice)
            )


def _validar_no_conteudo(no, niveis_por_id, origem, caminho):
    """Valida um no de ``dados``/``filhos`` (validacoes 12-17).

    Recursivo para nos de tipo ``container`` (validacao 17). A ordem dos
    arrays e preservada (validacao 18): esta funcao nao reordena nada.
    """
    if not isinstance(no, dict):
        raise TelaEstruturaInvalida(
            "{0}: {1} nao e objeto".format(origem, caminho)
        )
    # Validacao 12: cada no possui id e nivel.
    if "id" not in no:
        raise TelaCampoObrigatorioAusente(campo="{0}.id".format(caminho))
    if "nivel" not in no:
        raise TelaCampoObrigatorioAusente(campo="{0}.nivel".format(caminho))
    nivel_ref = no["nivel"]
    # Validacao 13: nivel referencia item declarado em formato.niveis.
    if nivel_ref not in niveis_por_id:
        raise TelaEstruturaInvalida(
            "{0}: {1}.nivel referencia nivel nao declarado: {2!r}".format(
                origem, caminho, nivel_ref
            )
        )
    nivel = niveis_por_id[nivel_ref]
    tipo_nivel = nivel["tipo"]
    conteudo_decl = nivel["conteudo"]

    if tipo_nivel == "container":
        # Validacao 14: campo semantico declarado + filhos como array.
        if not isinstance(conteudo_decl, str) or conteudo_decl not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (container)".format(caminho, conteudo_decl)
            )
        filhos = no.get("filhos")
        if not isinstance(filhos, list):
            raise TelaEstruturaInvalida(
                "{0}: {1} (nivel container) exige 'filhos' como array".format(
                    origem, caminho
                )
            )
        # Validacao 17: filhos validados recursivamente com as mesmas regras.
        for indice, filho in enumerate(filhos):
            _validar_no_conteudo(
                filho, niveis_por_id, origem,
                "{0}.filhos[{1}]".format(caminho, indice),
            )
    elif tipo_nivel == "conteudo":
        # Validacao 15: campo semantico declarado.
        if not isinstance(conteudo_decl, str) or conteudo_decl not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (conteudo)".format(caminho, conteudo_decl)
            )
    elif tipo_nivel == "nome_valor":
        # Validacao 16: campos de nome e valor declarados presentes.
        campo_nome = conteudo_decl.get("nome")
        campo_valor = conteudo_decl.get("valor")
        if campo_nome not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (nome_valor.nome)".format(caminho, campo_nome)
            )
        if campo_valor not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (nome_valor.valor)".format(caminho, campo_valor)
            )


def validar_conteudo_externo(documento, origem="documento externo"):
    """Executa as 20 validacoes semanticas do documento externo de conteudo.

    Autoridade: ADR-0027 D11/D13; contrato_json_console.md secao 12.5;
    H-0036 secao 14. As validacoes sao verificadas nominalmente e na ordem
    das secoes do contrato. Erros usam as classes de dominio existentes.

    Nao calcula geometria, nao infere hierarquia (declarada por ``filhos``),
    nao reordena arrays (validacao 18 e preservada por construcao) e nao muta
    o documento recebido. Devolve o proprio ``documento`` quando valido, para
    encadeamento conveniente.
    """
    # Validacao 1: raiz e objeto.
    if not isinstance(documento, dict):
        raise TelaEstruturaInvalida(
            "{0}: raiz do documento externo nao e objeto (recebido: {1})".format(
                origem, type(documento).__name__
            )
        )
    # Validacao 2: tipo presente e do tipo correto (string).
    if "tipo" not in documento:
        raise TelaCampoObrigatorioAusente(campo="tipo (documento externo)")
    tipo = documento["tipo"]
    if not isinstance(tipo, str):
        raise TelaEstruturaInvalida(
            "{0}: campo 'tipo' deve ser string; recebido: {1}".format(
                origem, type(tipo).__name__
            )
        )
    # Validacao 3: tipo igual a "multinivel".
    if tipo != "multinivel":
        raise TelaEstruturaInvalida(
            "{0}: tipo {1!r} nao suportado; unico tipo aceito: "
            "'multinivel'".format(origem, tipo)
        )
    # Validacao 4: formato presente e objeto.
    if "formato" not in documento:
        raise TelaCampoObrigatorioAusente(campo="formato (documento externo)")
    formato = documento["formato"]
    if not isinstance(formato, dict):
        raise TelaEstruturaInvalida(
            "{0}: 'formato' deve ser objeto".format(origem)
        )
    # Validacao 5: dados presente e array.
    if "dados" not in documento:
        raise TelaCampoObrigatorioAusente(campo="dados (documento externo)")
    dados = documento["dados"]
    if not isinstance(dados, list):
        raise TelaEstruturaInvalida(
            "{0}: 'dados' deve ser array".format(origem)
        )
    # Validacao 6: formato.apresentacao presente.
    if "apresentacao" not in formato:
        raise TelaCampoObrigatorioAusente(
            campo="formato.apresentacao (documento externo)"
        )
    apresentacao = formato["apresentacao"]
    # Validacao 7: apresentacao pertence ao conjunto previsto.
    if apresentacao not in APRESENTACOES_CONTEUDO_VALIDAS:
        raise TelaEstruturaInvalida(
            "{0}: formato.apresentacao invalida: {1!r}; aceitas: "
            "{2}".format(
                origem, apresentacao,
                ", ".join(sorted(APRESENTACOES_CONTEUDO_VALIDAS)),
            )
        )
    # Validacao 8: formato.niveis presente e array.
    if "niveis" not in formato:
        raise TelaCampoObrigatorioAusente(
            campo="formato.niveis (documento externo)"
        )
    niveis = formato["niveis"]
    if not isinstance(niveis, list):
        raise TelaEstruturaInvalida(
            "{0}: formato.niveis deve ser array".format(origem)
        )
    # Validacoes 9, 10, 11: cada nivel possui id/tipo/conteudo/designador;
    # ids nao vazios e unicos; tipos de nivel validos. Coleta niveis_por_id.
    niveis_por_id = {}
    for indice, nivel in enumerate(niveis):
        if not isinstance(nivel, dict):
            raise TelaEstruturaInvalida(
                "{0}: formato.niveis[{1}] nao e objeto".format(origem, indice)
            )
        # Validacao 9: possui id, tipo, conteudo e designador.
        for campo in ("id", "tipo", "conteudo", "designador"):
            if campo not in nivel:
                raise TelaCampoObrigatorioAusente(
                    campo="formato.niveis[{0}].{1}".format(indice, campo)
                )
        id_nivel = nivel["id"]
        # Validacao 10: id nao vazio e unico.
        if not isinstance(id_nivel, str) or id_nivel == "":
            raise TelaEstruturaInvalida(
                "{0}: formato.niveis[{1}].id vazio ou nao-string".format(
                    origem, indice
                )
            )
        if id_nivel in niveis_por_id:
            raise TelaEstruturaInvalida(
                "{0}: id de nivel duplicado em formato.niveis: {1!r}".format(
                    origem, id_nivel
                )
            )
        # Validacao 11: tipo de nivel pertence ao conjunto previsto.
        tipo_nivel = nivel["tipo"]
        if tipo_nivel not in TIPOS_NIVEL_CONTEUDO_VALIDOS:
            raise TelaEstruturaInvalida(
                "{0}: nivel {1!r} com tipo invalido: {2!r}; aceitos: "
                "{3}".format(
                    origem, id_nivel, tipo_nivel,
                    ", ".join(sorted(TIPOS_NIVEL_CONTEUDO_VALIDOS)),
                )
            )
        # Coerencia da declaracao de conteudo por tipo de nivel.
        conteudo_decl = nivel["conteudo"]
        if tipo_nivel == "nome_valor":
            if (
                not isinstance(conteudo_decl, dict)
                or not isinstance(conteudo_decl.get("nome"), str)
                or not isinstance(conteudo_decl.get("valor"), str)
            ):
                raise TelaEstruturaInvalida(
                    "{0}: nivel {1!r} (nome_valor) exige conteudo com 'nome' "
                    "e 'valor' (nomes de campo string)".format(origem, id_nivel)
                )
        else:
            if not isinstance(conteudo_decl, str) or conteudo_decl == "":
                raise TelaEstruturaInvalida(
                    "{0}: nivel {1!r} exige conteudo como nome de campo "
                    "(string nao vazia)".format(origem, id_nivel)
                )
        _validar_designador_conteudo(nivel["designador"], id_nivel, origem)
        niveis_por_id[id_nivel] = nivel

    # Validacao 19: blocos especificos compativeis com a apresentacao.
    for bloco in _BLOCOS_ESPECIFICOS_APRESENTACAO:
        if bloco in formato and _BLOCO_ESPECIFICO_POR_APRESENTACAO.get(
            apresentacao
        ) != bloco:
            raise TelaEstruturaInvalida(
                "{0}: bloco {1!r} incompativel com apresentacao {2!r}; "
                "'tabela' so em apresentacao tabela, 'campos' so em "
                "conjuntos_campos".format(origem, bloco, apresentacao)
            )

    # Validacao 20: documento nao contem resultados fisicos calculados.
    _rejeitar_resultados_fisicos_conteudo(documento, origem)

    # Validacoes 12-18: nos de dados (recursivo, ordem preservada).
    for indice, no in enumerate(dados):
        _validar_no_conteudo(
            no, niveis_por_id, origem, "dados[{0}]".format(indice)
        )

    return documento


def carregar_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None):
    """Carrega, decodifica e valida um documento externo de conteudo.

    Parametros analogos a ``carregar_tela``: ``caminho_base`` (None usa a raiz
    do repositorio), ``id_conteudo`` (nome base do arquivo, sem extensao) e
    ``raiz_telas`` (diretorio relativo; None usa ``config/telas``; a
    demonstracao passa ``config/telas/demo``).

    Devolve o documento validado (dict) como representacao semantica. O
    consumidor (modelo) constroi a representacao tipada; o renderizador calcula
    a geometria. Este loader NAO abre o JSON estrutural, NAO vincula tela e
    conteudo (responsabilidade do ``demo.py``), NAO calcula geometria e NAO
    infere hierarquia.

    Lanca: TelaArquivoNaoEncontrado, TelaJsonInvalido,
    TelaCampoObrigatorioAusente, TelaEstruturaInvalida.
    """
    base = _para_base(caminho_base)
    if not isinstance(id_conteudo, str) or not id_conteudo:
        raise TelaCampoObrigatorioAusente(campo="id_conteudo (documento externo)")

    if raiz_telas is None:
        raiz_telas = os.path.join("config", "telas")

    caminho_relativo = os.path.join(raiz_telas, id_conteudo + ".json")
    caminho_arquivo = base / caminho_relativo

    if not caminho_arquivo.is_file():
        raise TelaArquivoNaoEncontrado(
            "Documento externo de conteudo nao encontrado: {0}".format(
                caminho_relativo
            )
        )

    try:
        texto = caminho_arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        raise TelaArquivoNaoEncontrado(
            "Documento externo de conteudo nao encontrado: {0} ({1})".format(
                caminho_relativo, exc
            )
        )

    try:
        documento = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise TelaJsonInvalido(
            "JSON invalido em documento externo: {0} - {1}".format(
                caminho_relativo, exc
            )
        )

    validar_conteudo_externo(documento, origem=caminho_relativo)
    return documento
