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
from dataclasses import dataclass
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


class EstiloErro(Exception):
    """Erro de carregamento ou validacao de ``config/estilo.json`` (H-0039).

    Levantada por ``carregar_estilo`` em qualquer condicao invalida listada
    nas validacoes V-01 a V-29 (ADR-0030 D9). Configuracao parcialmente
    resolvida nunca produz ``EstiloResolvido`` -- nao existe fallback
    silencioso.
    """


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

# H-0037 / ADR-0028 D23: politicas de modo e modos iniciais validos para
# elementos console (contrato_json_console.md secao 13.13.2).
_POLITICAS_MODO_VALIDAS = frozenset({
    "somente_verboso", "somente_nao_verboso", "alternavel"
})
_MODOS_INICIAIS_VALIDOS = frozenset({"verboso", "nao_verboso"})

# Telas legadas reconhecidas nominalmente: ausencia de politica_modo nessas
# telas e aceita por compatibilidade (ADR-0028 §13.13.8; §39; §43 item 3). Sao
# telas criadas antes da incorporacao de D23, consumidoras de conteudo multinivel
# externo, que permanecem validas sem declarar politica ate futura decisao de
# migracao. O inventario e estritamente nominal e historico — nao vira regra
# generica para telas futuras (que devem declarar politica obrigatoriamente).
# Inclui os cenarios de console do H-0035 (adaptados em H-0036) e os tres
# cenarios canonicos do H-0036.
_TELAS_LEGADAS_D23 = frozenset({
    # H-0036: cenarios canonicos de conteudo multinivel (tabela, hierarquia,
    # conjuntos_campos). Pre-D23, sem politica declarada, sem chip [V].
    "h0036_console_hierarquia",
    "h0036_console_tabela",
    "h0036_console_conjuntos",
    # H-0035: cenarios de console que adotaram ADR-0025 (distribuicao
    # matricial) e foram adaptados em H-0036 para consumir conteudo externo.
    # Pre-D23, sem politica declarada.
    "h0035_console_com",
    "h0035_console_sem",
})

# Inventario nominal das configuracoes historicas comprovadas que usam a
# variante 2 do envelope pre-ADR-0028 (``regra_geracao_itens`` + 6 campos base,
# sem ``itens``). Essa variante nao tem schema interno fechado para
# ``regra_geracao_itens`` (Resultado B do portao documental); sua aceitacao e
# por compatibilidade restrita com a forma historica comprovada, nao por
# regra geral. Telas novas ou revisadas NAO podem usar ``regra_geracao_itens``
# para evitar D23 (H0037-IMPL-QAPP5-001). A deteccao e estritamente nominal e
# historica — nao vira regra por prefixo nem valha para telas futuras.
# Atualmente: ``demo`` (config/telas/demo/demo.json), cujo ``console_principal``
# declara ``regra_geracao_itens`` + os 6 campos base como rascunho pendente
# (DOC-B008/DOC-B009).
_TELAS_VARIANTE2_LEGADAS = frozenset({"demo"})

# Campos do envelope pre-ADR-0028 de um elemento ``console`` (contrato_json_console.md
# secao 4 / secao 5). A presenca de qualquer um deles indica que o elemento usa o
# envelope classico de console (declaracao direta de ``itens`` com ``origem_dados``,
# politicas de composicao/navegacao/selecao/paginacao/exibicao), e portanto NAO e
# um consumidor de conteudo multinivel externo regido pela ADR-0028. ADR-0028 §6
# limita seu escopo a "dados multinivel exibidos em componentes do tipo console":
# consoles de envelope pre-ADR-0028 estao fora desse escopo e preservam o
# comportamento contratual anterior. A deteccao e estrutural (campos do elemento),
# nao nominal por id de tela, para que valha para qualquer tela futura de envelope.
_CAMPOS_ENVELOPE_PRE_ADR_0028 = frozenset({
    "itens",
    "origem_dados",
    "politica_composicao",
    "politica_navegacao",
    "politica_selecao",
    "politica_paginacao",
    "politica_exibicao",
})

# Campos base do envelope pre-ADR-0028 (excluindo a fonte de itens). O envelope
# classico admite duas variantes mutuamente exclusivas de fonte de itens
# (contrato_console.md §3: "itens OU regra de geracao de itens"), ambas
# combinadas com o mesmo conjunto base de seis campos: origem_dados e as cinco
# politicas (composicao, navegacao, selecao, paginacao, exibicao).
#   - variante 1: ``itens`` + 6 campos base;
#   - variante 2: ``regra_geracao_itens`` + 6 campos base (forma usada por
#     ``console_principal`` de demo.json).
# ``itens`` e ``regra_geracao_itens`` sao duas fontes concorrentes de itens e
# nao podem coexistir. Nao ha schema interno fechado para ``regra_geracao_itens``
# (Resultado B do portao documental), mas a forma historica da variante 2 e
# preservada como tipo estrutural real pre-ADR-0028 (H0037-IMPL-QAPP5-001).
_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 = frozenset({
    "origem_dados",
    "politica_composicao",
    "politica_navegacao",
    "politica_selecao",
    "politica_paginacao",
    "politica_exibicao",
})


_POLITICA_SELECAO_VALIDOS = frozenset({"nenhuma", "unica", "multipla"})
_POLITICA_PAGINACAO_VALIDOS = frozenset({"sem", "com"})


def _validar_valores_envelope_pre_adr_0028(elemento):
    """Valida os valores dos campos base do envelope pre-ADR-0028.

    Chamada quando o envelope pre-ADR-0028 esta completo (fonte de itens + os 6
    campos base). A validacao depende da variante (H0037-IMPL-QAPP5-001):

      - **variante 1** (``itens`` presente, sem ``regra_geracao_itens``):
        validacao estrita dos tipos/valores canonicos de cada campo
        (contrato_json_console.md secao 4/5): ``itens`` lista, ``origem_dados``
        objeto ou null, ``politica_composicao``/``navegacao``/``exibicao``
        objeto, ``politica_selecao``/``paginacao`` string em vocabulario
        fechado. Vale para qualquer tela.

      - **variante 2** (``regra_geracao_itens`` presente, sem ``itens``):
        aceitacao por compatibilidade restrita com a forma historica comprovada
        (``_TELAS_VARIANTE2_LEGADAS``). Nao ha schema interno fechado para
        ``regra_geracao_itens`` nem para as formas historicas de
        ``politica_paginacao``/``origem_dados`` em rascunho (demo.json usa
        ``politica_paginacao: {paginacao: "com"}`` e ``origem_dados`` como
        objeto pendente). A validacao estrita da variante 1 NAO e reaplicada —
        preserva-se a forma historica sem inventar schema novo. A completude
        estrutural e a exclusividade ja foram garantidas pelo chamador.
    """
    id_elem = elemento.get("id", "?")
    orig = "elemento '{0}'".format(id_elem)

    # Variante 2 (regra_geracao_itens sem itens): compatibilidade restrta com a
    # forma historica. Nao valida tipos escalares — o chamador ja garantiu
    # completude (6 campos base), exclusividade (sem itens) e id_tela legada.
    if "regra_geracao_itens" in elemento and "itens" not in elemento:
        return

    # Variante 1 (itens presente): validacao estrita dos tipos/valores canonicos.
    itens = elemento.get("itens")
    if not isinstance(itens, list):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'itens' deve ser lista; "
            "recebido: {1!r}".format(orig, type(itens).__name__)
        )

    origem_dados = elemento.get("origem_dados")
    if not isinstance(origem_dados, (dict, type(None))):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'origem_dados' deve ser objeto ou "
            "null; recebido: {1!r}".format(orig, type(origem_dados).__name__)
        )

    pol_comp = elemento.get("politica_composicao")
    if not isinstance(pol_comp, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_composicao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_comp).__name__)
        )

    pol_nav = elemento.get("politica_navegacao")
    if not isinstance(pol_nav, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_navegacao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_nav).__name__)
        )

    pol_sel = elemento.get("politica_selecao")
    if not isinstance(pol_sel, str) or pol_sel not in _POLITICA_SELECAO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_selecao' deve ser uma de "
            "{1}; recebido: {2!r}".format(
                orig, ", ".join(sorted(_POLITICA_SELECAO_VALIDOS)), pol_sel
            )
        )

    pol_pag = elemento.get("politica_paginacao")
    if not isinstance(pol_pag, str) or pol_pag not in _POLITICA_PAGINACAO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_paginacao' deve ser 'sem' "
            "ou 'com'; recebido: {1!r}".format(orig, pol_pag)
        )

    pol_exib = elemento.get("politica_exibicao")
    if not isinstance(pol_exib, dict):
        raise TelaEstruturaInvalida(
            "{0}: envelope pre-ADR-0028: 'politica_exibicao' deve ser "
            "objeto; recebido: {1!r}".format(orig, type(pol_exib).__name__)
        )


def _console_em_escopo_d23(elemento, id_tela):
    """Determina se um elemento ``console`` esta em escopo D23 (ADR-0028 §6 + D23).

    O escopo de ADR-0028 (e portanto de D23) e "dados multinivel exibidos em
    componentes do tipo console" (ADR-0028 §6), aplicavel exclusivamente a
    instancias que recebem conteudo multinivel externo (``tipo: "multinivel"``)
    — contrato_console.md §21.1. A deteccao e estrutural e independe da presenca
    de ``formato.excesso``.

    DECISAO POR TIPO ESTRUTURAL REAL (H0037-IMPL-QAPP5-001):

    Nao existe schema interno fechado para ``regra_geracao_itens`` nos contratos,
    ADRs ou NOMENCLATURA — apenas a frase "regra de geracao de itens" como
    alternativa contratual a ``itens`` (contrato_console.md §3). O envelope
    pre-ADR-0028 admite duas variantes mutuamente exclusivas de fonte de itens,
    ambas combinadas com o mesmo conjunto base de seis campos
    (``_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028``: origem_dados e as cinco politicas):

      - **variante 1** (classica): ``itens`` + 6 campos base;
      - **variante 2** (geracao interna): ``regra_geracao_itens`` + 6 campos base
        (forma historica usada por ``console_principal`` de demo.json).

    Classificacao estrutural (decide o escopo D23, sem discriminar pela mera
    presenca de ``regra_geracao_itens``):

    - **Envelope pre-ADR-0028 completo** (variante 1 ou 2 com a fonte de itens
      + os 6 campos base presentes): console pre-ADR-0028, FORA do escopo D23.
      Os valores dos campos base sao validados (``_validar_valores_envelope_pre_adr_0028``).
      ``demo.json`` e valido por essa via (variante 2).
    - **Envelope incompleto** (fonte de itens presente mas faltam campos base):
      ``TelaEstruturaInvalida`` — envelope parcial nao e forma historica valida.
    - **Duas fontes concorrentes** (``itens`` E ``regra_geracao_itens``):
      ``TelaEstruturaInvalida`` — sao mutuamente exclusivas (contrato_console.md §3).
    - **Consumidor de conteudo multinivel externo** (0 campos de envelope, sem
      ``regra_geracao_itens``): consumidor puro, DENTRO do escopo D23 (salvo
      legado nominal em ``_TELAS_LEGADAS_D23``).
    - **Hibrido consumidor + regra_geracao_itens** (0 campos de envelope + chave
      ``regra_geracao_itens``): ``TelaEstruturaInvalida`` — geracao interna e
      consumo externo sao mutuamente exclusivos. Qualquer valor sob a chave
      (``{}``, ``null``, tipos incorretos, objetos incompletos) e rejeitado; nao
      ha schema fechado, portanto a chave nunca isenta de D23.
    - **Hibrido envelope + marcadores D23** (envelope pre-ADR-0028 + politica_modo
      /modo_inicial em formato.excesso): ``TelaEstruturaInvalida`` — envelope
      pre-ADR-0028 e consumidor multinivel sao mutuamente exclusivos.

    ``regra_geracao_itens`` nunca concede isencao por mera presenca: ou faz
    parte da variante 2 completa (junto dos 6 campos base) ou e rejeitada como
    incompativel. Nenhum valor sob a chave (incl. ``{}``) serve como bypass.
    """
    campos_base_presentes = _CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 & set(elemento)
    n_base = len(campos_base_presentes)
    n_base_total = len(_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028)
    tem_itens = "itens" in elemento
    tem_regra = "regra_geracao_itens" in elemento
    tem_fonte_itens = tem_itens or tem_regra
    n_fontes = (1 if tem_itens else 0) + (1 if tem_regra else 0)

    _fmt = elemento.get("formato")
    _exc = _fmt.get("excesso") if isinstance(_fmt, dict) else None
    _tem_d23 = isinstance(_exc, dict) and (
        "politica_modo" in _exc or "modo_inicial" in _exc
    )

    # Hibrido envelope + marcadores D23 de consumidor multinivel. Rejeitado em
    # qualquer cardinalidade de envelope (mesmo um campo base + D23 e
    # incompativel). A mera presenca de envelope classico ou de fonte de itens
    # coloca o elemento fora do escopo de conteudo multinivel externo; misturar
    # com marcadores D23 e estruturalmente invalido (contrato_console.md §21.1).
    if (n_base >= 1 or tem_fonte_itens) and _tem_d23:
        _partes = sorted(campos_base_presentes)
        if tem_itens:
            _partes = ["itens"] + _partes
        if tem_regra:
            _partes = ["regra_geracao_itens"] + _partes
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campos de envelope "
            "pre-ADR-0028 presentes ({1}) coexistindo com marcadores D23 "
            "(politica_modo/modo_inicial em formato.excesso); envelope "
            "pre-ADR-0028 e consumidor multinivel externo sao mutuamente "
            "exclusivos".format(
                elemento.get("id", "?"), ", ".join(_partes),
            )
        )

    # Duas fontes de itens concorrentes (itens E regra_geracao_itens).
    # Mutuamente exclusivas por contrato (contrato_console.md §3).
    if n_fontes == 2:
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campos 'itens' e "
            "'regra_geracao_itens' coexistem como duas fontes concorrentes de "
            "geracao de itens; sao mutuamente exclusivos "
            "(contrato_console.md §3)".format(elemento.get("id", "?"))
        )

    # Hibrido consumidor multinivel + regra_geracao_itens (sem nenhum campo de
    # envelope). Geracao interna e consumo de conteudo externo sao mutuamente
    # exclusivos. Nao ha schema fechado para regra_geracao_itens (Resultado B do
    # portao documental), portanto nenhum valor sob a chave e valido aqui:
    # {}, null, string, lista, bool, numero e objetos incompletos sao todos
    # rejeitados (H0037-IMPL-QAPP5-001).
    if tem_regra and n_base == 0:
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompativel: campo "
            "'regra_geracao_itens' (geracao interna de itens, alternativa a "
            "'itens' — contrato_console.md §3) nao pode coexistir com um "
            "consumidor de conteudo multinivel externo (sem campos de envelope "
            "pre-ADR-0028); geracao interna e consumo de conteudo externo sao "
            "mutuamente exclusivos (valor sob a chave ignorado: nao ha schema "
            "fechado)".format(elemento.get("id", "?"))
        )

    # Envelope pre-ADR-0028 com fonte de itens: variantes 1 (itens) ou 2
    # (regra_geracao_itens). As duas exigem os 6 campos base completos.
    if tem_fonte_itens:
        if n_base != n_base_total:
            # Envelope incompleto: fonte de itens presente mas faltam campos
            # base. Nao e forma historica valida nem consumidor multinivel.
            _faltantes = sorted(
                _CAMPOS_ENVELOPE_BASE_PRE_ADR_0028 - campos_base_presentes
            )
            raise TelaEstruturaInvalida(
                "elemento '{0}': envelope pre-ADR-0028 incompleto: fonte de "
                "itens ({1}) presente, mas faltam {2} de {3} campos base "
                "({4}); envelope historico exige origem_dados e as cinco "
                "politicas (composicao, navegacao, selecao, paginacao, "
                "exibicao)".format(
                    elemento.get("id", "?"),
                    "itens" if tem_itens else "regra_geracao_itens",
                    len(_faltantes), n_base_total, ", ".join(_faltantes),
                )
            )
        # Envelope completo (variante 1 ou 2). A validacao de valores depende
        # da variante (H0037-IMPL-QAPP5-001):
        #   - variante 1 (itens): validacao estrita dos tipos/valores canonicos
        #     (contrato_json_console.md secao 4/5); vale para qualquer tela.
        #   - variante 2 (regra_geracao_itens, sem itens): aceitacao por
        #     compatibilidade restrita com a forma historica comprovada
        #     (inventario nominal _TELAS_VARIANTE2_LEGADAS). Nao ha schema
        #     fechado para regra_geracao_itens, portanto os tipos internos nao
        #     sao validados pelos escalares da variante 1 — preserva-se a forma
        #     historica existente. Telas novas/revisadas nao podem usar
        #     regra_geracao_itens para evitar D23.
        if tem_regra and id_tela not in _TELAS_VARIANTE2_LEGADAS:
            raise TelaEstruturaInvalida(
                "elemento '{0}': variante 2 do envelope pre-ADR-0028 "
                "(regra_geracao_itens) nao aceita para tela nova/revisada "
                "'{1}'; regra_geracao_itens nao e schema fechado e telas novas "
                "nao podem usa-lo para evitar D23 (H0037-IMPL-QAPP5-001)".format(
                    elemento.get("id", "?"), id_tela,
                )
            )
        # Valida valores conforme a variante. Variante 1 valida tipos canonicos;
        # variante 2 (legada comprovada) preserva a forma historica sem validar
        # schema interno de regra_geracao_itens.
        _validar_valores_envelope_pre_adr_0028(elemento)
        return False

    if n_base >= 1:
        # Campos base sem fonte de itens: nem envelope completo (variante 1 ou
        # 2) nem consumidor multinivel puro. Estrutura incompleta/invalida.
        raise TelaEstruturaInvalida(
            "elemento '{0}': estrutura incompleta: {1} campo(s) de envelope "
            "pre-ADR-0028 ({2}) sem fonte de itens ('itens' ou "
            "'regra_geracao_itens'); nao e envelope historico completo nem "
            "consumidor multinivel".format(
                elemento.get("id", "?"),
                n_base, ", ".join(sorted(campos_base_presentes)),
            )
        )

    # n_base == 0 e sem fonte de itens: consumidor de conteudo multinivel
    # externo puro. Legado nominalmente reconhecido (H-0035/H-0036) e isento;
    # telas novas ou revisadas estao em escopo D23 (ADR-0028 §13.13.3).
    return id_tela not in _TELAS_LEGADAS_D23


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


# Campos que tornam uma entrada de ``formato.tabela.cabecalho`` estruturalmente
# reconhecivel como coluna (H-0037 / ADR-0028 §33 V-01 + V-14). ``titulo`` e o
# rotulo da coluna; ``nivel`` e ``campo`` sao origens (verificados por V-14).
_CAMPOS_COLUNA_RECONHECIVEL = frozenset({"titulo", "nivel", "campo"})


def _coluna_reconhecivel(entrada):
    """True quando ``entrada`` satisfaz a forma contratual minima de coluna.

    Usado por V-01 (cabecalho) e distinto de V-14 (origem da coluna).
    Uma coluna e estruturalmente reconhecivel quando:

    - e uma string com ao menos um caractere nao-espaco (cabecalho simples,
      como ``["Grupo", "Valor"]``), ou
    - e um objeto em que ao menos um campo minimo (``titulo``, ``nivel`` ou
      ``campo``) possui valor semanticamente nao vazio.

    Valor semanticamente vazio: None, string vazia ou string composta apenas de
    espacos. A simples presenca da chave nao basta — o valor deve ser nao vazio.
    Entradas nulas, tipos incorretos, objetos vazios, objetos sem campos minimos
    e objetos cujos campos minimos possuem valores semanticamente vazios NAO sao
    colunas reconheciveis.

    Distincao com V-14: V-14 rejeita coluna reconhecivel (forma valida) sem
    origem; V-01 rejeita ausencia total de qualquer coluna reconhecivel.
    """
    if isinstance(entrada, str):
        return entrada.strip() != ""
    if isinstance(entrada, dict):
        for campo in _CAMPOS_COLUNA_RECONHECIVEL:
            if campo not in entrada:
                continue
            v = entrada[campo]
            if v is not None and not (isinstance(v, str) and v.strip() == ""):
                return True
        return False
    return False


def _validar_d23_console(excesso, id_elemento, id_tela=None, em_escopo=True):
    """Valida a politica de modo D23 de um elemento console (ADR-0028 D23).

    Verifica combinacoes validas de politica_modo e modo_inicial conforme
    a matriz de validade em contrato_json_console.md secao 13.13.2.

    O escopo D23 e determinado estruturalmente pelo chamador via
    ``_console_em_escopo_d23`` (ADR-0028 §6 + D23), independentemente da
    presenca de ``formato.excesso``. Quando ``em_escopo`` e False, o elemento
    nao esta sujeito a D23 (envelope pre-ADR-0028 ou estrutura fora do escopo
    de console multinivel) e a funcao preserva o comportamento anterior sem
    exigir politica. Quando ``em_escopo`` e True, telas nominalmente legadas
    H-0036 (``_TELAS_LEGADAS_D23``) podem omitir politica_modo; telas novas ou
    revisadas devem declarar politica_modo obrigatoriamente, mesmo se o bloco
    ``formato.excesso`` estiver ausente.
    """
    # Fora do escopo D23 (envelope pre-ADR-0028 ou estrutura nao multinivel):
    # preserva o comportamento contratual anterior.
    if not em_escopo:
        return

    politica = excesso.get("politica_modo")
    modo_inicial = excesso.get("modo_inicial")

    if modo_inicial is not None and politica is None:
        raise TelaEstruturaInvalida(
            "elemento '{0}': D23: modo_inicial declarado sem politica_modo".format(
                id_elemento
            )
        )
    if politica is None:
        if id_tela in _TELAS_LEGADAS_D23:
            return
        raise TelaEstruturaInvalida(
            "elemento '{0}': D23: politica_modo ausente; telas novas ou "
            "revisadas de console multinivel devem declarar politica_modo em "
            "formato.excesso (ausencia do bloco nao isenta a "
            "tela)".format(id_elemento)
        )
    if politica not in _POLITICAS_MODO_VALIDAS:
        raise TelaEstruturaInvalida(
            "elemento '{0}': D23: politica_modo invalida: {1!r}; aceitas: "
            "{2}".format(
                id_elemento,
                politica,
                ", ".join(sorted(_POLITICAS_MODO_VALIDAS)),
            )
        )
    if politica == "alternavel":
        if modo_inicial is None:
            raise TelaEstruturaInvalida(
                "elemento '{0}': D23: politica_modo 'alternavel' exige "
                "modo_inicial".format(id_elemento)
            )
        if modo_inicial not in _MODOS_INICIAIS_VALIDOS:
            raise TelaEstruturaInvalida(
                "elemento '{0}': D23: modo_inicial invalido para 'alternavel': "
                "{1!r}; aceitos: verboso, nao_verboso".format(
                    id_elemento, modo_inicial
                )
            )
    else:
        if modo_inicial is not None:
            raise TelaEstruturaInvalida(
                "elemento '{0}': D23: politica_modo {1!r} nao aceita "
                "modo_inicial".format(id_elemento, politica)
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
        # V-05: container com filhos declarados mas vazios e invalido.
        if len(filhos) == 0:
            raise TelaEstruturaInvalida(
                "{0}: V-05: {1} (container) com 'filhos' vazio; pelo menos "
                "um filho e obrigatorio".format(origem, caminho)
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
        # V-04: no folha (conteudo) nao pode declarar filhos (inclusive lista vazia).
        if "filhos" in no:
            raise TelaEstruturaInvalida(
                "{0}: V-04: {1} (conteudo, folha) nao pode declarar "
                "filhos".format(origem, caminho)
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
        # V-04: no folha (nome_valor) nao pode declarar filhos (inclusive lista vazia).
        if "filhos" in no:
            raise TelaEstruturaInvalida(
                "{0}: V-04: {1} (nome_valor, folha) nao pode declarar "
                "filhos".format(origem, caminho)
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
                    "{0}: V-06: nivel {1!r} (nome_valor) exige conteudo com "
                    "'nome' e 'valor' como nomes de campo string (campo "
                    "nome-valor sem origem do valor)".format(origem, id_nivel)
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

    # Catalogo estrutural de campos de nos de dados derivado de
    # ``formato.niveis[].conteudo`` (contrato_json_console.md §12.3). Para cada
    # nivel, ``conteudo`` declara os nomes dos campos do no que carregam
    # conteudo exibivel:
    #   - ``container``/``conteudo``: ``conteudo`` e uma string com o nome do
    #     campo de texto do no (ex.: "titulo", "texto");
    #   - ``nome_valor``: ``conteudo`` e um objeto declarando os campos
    #     ``nome`` e ``valor`` (nomes dos campos do no).
    # Esse conjunto e a autoridade estrutural para validar ``campo`` de colunas
    # de tabela em V-13 (H0037-IMPL-QAPP5-002): o contrato nao define um
    # catalogo literal fechado de valores de ``campo``, mas define onde estao os
    # campos validos — na estrutura declarada. ``nivel`` e validado contra
    # ``niveis_por_id`` (chaves do nivel); ``campo`` e validado contra os nomes
    # de campos de conteudo de todos os niveis. Nao inventa catalogo novo:
    # reaproveita exclusivamente o que ``formato.niveis`` declarou.
    _campos_validos_por_no = set()
    for _nivel_campo in niveis_por_id.values():
        _cont = _nivel_campo.get("conteudo")
        if isinstance(_cont, str) and _cont.strip() != "":
            _campos_validos_por_no.add(_cont)
        elif isinstance(_cont, dict):
            for _chave_cont in ("nome", "valor"):
                _nome_cont = _cont.get(_chave_cont)
                if isinstance(_nome_cont, str) and _nome_cont.strip() != "":
                    _campos_validos_por_no.add(_nome_cont)

    # --- Validacoes H-0037 / ADR-0028 (V-01 a V-15) ---

    # V-01: tabela sem cabecalho semanticamente reconhecivel.
    # O cabecalho deve ser uma lista contendo ao menos uma coluna valida. Nao
    # basta que a lista seja nao vazia: cada entrada deve satisfazer a forma
    # contratual de coluna. Uma coluna e estruturalmente reconhecivel quando e:
    #   - uma string nao vazia (cabecalho simples), ou
    #   - um objeto declarando origem/rotulo (campos minimos: 'titulo' para
    #     rotulo, ou 'nivel'/'campo' para origem - a forma verificada por V-14).
    # Uma lista sem nenhuma coluna reconhecivel (vazia, entradas nulas, tipos
    # incorretos, objetos sem os campos minimos) e rejeitada por V-01. A
    # distincao entre V-01 e V-14: V-01 cobre ausencia total de coluna
    # reconhecivel; V-14 cobre coluna reconhecivel sem origem.
    if apresentacao == "tabela":
        bloco_tabela = formato.get("tabela")
        cabecalho_tb = (
            bloco_tabela.get("cabecalho") if isinstance(bloco_tabela, dict) else None
        )
        if not isinstance(cabecalho_tb, list):
            raise TelaEstruturaInvalida(
                "{0}: V-01: apresentacao 'tabela' exige formato.tabela.cabecalho "
                "como lista de colunas".format(origem)
            )
        if not any(_coluna_reconhecivel(c) for c in cabecalho_tb):
            raise TelaEstruturaInvalida(
                "{0}: V-01: apresentacao 'tabela' exige formato.tabela.cabecalho "
                "com ao menos uma coluna semanticamente valida".format(origem)
            )

    # V-02: referencia a nivel filho inexistente em formato.niveis[].filhos.
    for nivel in niveis:
        id_nivel = nivel.get("id", "?")
        if "filhos" in nivel and isinstance(nivel["filhos"], list):
            for id_filho in nivel["filhos"]:
                if not isinstance(id_filho, str) or id_filho == "":
                    raise TelaEstruturaInvalida(
                        "{0}: V-02: nivel {1!r}.filhos contem entrada "
                        "nao-string ou vazia".format(origem, id_nivel)
                    )
                if id_filho not in niveis_por_id:
                    raise TelaEstruturaInvalida(
                        "{0}: V-02: nivel {1!r}.filhos referencia nivel filho "
                        "inexistente: {2!r}".format(origem, id_nivel, id_filho)
                    )

    # V-03: multiplas raizes na hierarquia de niveis (quando filhos declarados).
    _niveis_filhos_fmt = set()
    _tem_filhos_fmt = False
    for nivel in niveis:
        _f = nivel.get("filhos")
        if isinstance(_f, list):
            _tem_filhos_fmt = True
            for _id_f in _f:
                if isinstance(_id_f, str):
                    _niveis_filhos_fmt.add(_id_f)
    if _tem_filhos_fmt:
        _raizes = [
            n.get("id") for n in niveis
            if isinstance(n.get("id"), str)
            and n.get("id") not in _niveis_filhos_fmt
        ]
        if len(_raizes) > 1:
            raise TelaEstruturaInvalida(
                "{0}: V-03: hierarquia de niveis tem {1} raizes ({2!r}); "
                "deve haver exatamente uma raiz quando filhos sao "
                "declarados".format(origem, len(_raizes), _raizes)
            )

    # V-07: medidas negativas em formato.espacamento.
    _esp_fmt = formato.get("espacamento")
    if isinstance(_esp_fmt, dict):
        for _nome_mc, _val_mc in _esp_fmt.items():
            if isinstance(_val_mc, (int, float)) and _val_mc < 0:
                raise TelaEstruturaInvalida(
                    "{0}: V-07: medida negativa em formato.espacamento.{1}: "
                    "{2}".format(origem, _nome_mc, _val_mc)
                )

    # V-08: largura maxima inferior a minima em colunas de tabela.
    if apresentacao == "tabela":
        _bloco_tab_v8 = formato.get("tabela")
        _colunas_v8 = (
            _bloco_tab_v8.get("colunas", [])
            if isinstance(_bloco_tab_v8, dict) else []
        )
        if isinstance(_colunas_v8, list):
            for _i_col, _col in enumerate(_colunas_v8):
                if isinstance(_col, dict):
                    _lm = _col.get("largura_minima")
                    _lx = _col.get("largura_maxima")
                    if (
                        isinstance(_lm, (int, float))
                        and isinstance(_lx, (int, float))
                        and _lx < _lm
                    ):
                        raise TelaEstruturaInvalida(
                            "{0}: V-08: coluna[{1}]: largura_maxima ({2}) "
                            "inferior a largura_minima ({3})".format(
                                origem, _i_col, _lx, _lm
                            )
                        )

    # V-09: modo nao verboso configurado para mais de uma linha.
    _excesso_fmt = formato.get("excesso")
    if isinstance(_excesso_fmt, dict):
        _linhas_nv = _excesso_fmt.get("linhas_nao_verboso")
        if isinstance(_linhas_nv, int) and _linhas_nv > 1:
            raise TelaEstruturaInvalida(
                "{0}: V-09: formato.excesso.linhas_nao_verboso={1}; modo "
                "nao verboso deve ocupar exatamente uma linha".format(
                    origem, _linhas_nv
                )
            )

    # V-10: modo verboso sem regra de alinhamento da continuacao.
    if isinstance(_excesso_fmt, dict):
        _verboso_cfg = _excesso_fmt.get("verboso")
        if isinstance(_verboso_cfg, dict) and "continuacao" not in _verboso_cfg:
            raise TelaEstruturaInvalida(
                "{0}: V-10: formato.excesso.verboso declarado sem campo "
                "'continuacao' (regra de alinhamento obrigatoria)".format(origem)
            )

    # V-11: justificacao sem escopo em formato.alinhamento.
    _alin_fmt = formato.get("alinhamento")
    if isinstance(_alin_fmt, dict):
        if (
            _alin_fmt.get("tipo") == "justificado"
            and "escopo" not in _alin_fmt
        ):
            raise TelaEstruturaInvalida(
                "{0}: V-11: formato.alinhamento.tipo='justificado' sem campo "
                "'escopo' obrigatorio".format(origem)
            )

    # V-12: designador composto (decimal_composto) sem ancestral declarado.
    # Nivel com decimal_composto nao pode aparecer como no raiz nos dados.
    for _no_raiz in dados:
        _nivel_ref = _no_raiz.get("nivel") if isinstance(_no_raiz, dict) else None
        if _nivel_ref in niveis_por_id:
            _nivel_dec = niveis_por_id[_nivel_ref]
            if _nivel_dec.get("designador", {}).get("tipo") == "decimal_composto":
                raise TelaEstruturaInvalida(
                    "{0}: V-12: no raiz {1!r} usa nivel {2!r} com designador "
                    "'decimal_composto' que requer ancestral; designador "
                    "composto invalido em no raiz dos dados".format(
                        origem,
                        _no_raiz.get("id") if isinstance(_no_raiz, dict) else "?",
                        _nivel_ref,
                    )
                )

    # V-13: dados incompativeis com a estrutura declarada.
    # Coberto pelas validacoes 12-17 em _validar_no_conteudo (executadas acima).

    # V-14: coluna de tabela sem nivel ou campo de origem.
    if apresentacao == "tabela":
        _bloco_tab_v14 = formato.get("tabela")
        _colunas_v14 = (
            _bloco_tab_v14.get("colunas", [])
            if isinstance(_bloco_tab_v14, dict) else []
        )
        if isinstance(_colunas_v14, list):
            for _i_col, _col in enumerate(_colunas_v14):
                if isinstance(_col, dict):
                    _nv = _col.get("nivel") if "nivel" in _col else None
                    _cp = _col.get("campo") if "campo" in _col else None
                    _nivel_ok = (
                        "nivel" in _col
                        and isinstance(_nv, str)
                        and _nv.strip() != ""
                    )
                    _campo_ok = (
                        "campo" in _col
                        and isinstance(_cp, str)
                        and _cp.strip() != ""
                    )
                    if not _nivel_ok and not _campo_ok:
                        raise TelaEstruturaInvalida(
                            "{0}: V-14: coluna[{1}] de tabela sem campo "
                            "'nivel' ou 'campo' de origem valido".format(
                                origem, _i_col
                            )
                        )
                    # V-13: nivel declarado mas incompativel com a estrutura.
                    if _nivel_ok and _nv not in niveis_por_id:
                        raise TelaEstruturaInvalida(
                            "{0}: V-13: coluna[{1}] referencia nivel {2!r} "
                            "nao declarado em formato.niveis; nivel de coluna "
                            "incompativel com a estrutura "
                            "declarada".format(origem, _i_col, _nv)
                        )
                    # V-13 por campo (H0037-IMPL-QAPP5-002): campo declarado
                    # mas incompativel com a estrutura. O contrato nao define um
                    # catalogo literal de valores de ``campo`` (V-14 exige apenas
                    # presenca de string nao-vazia); mas define onde estao os
                    # campos validos — em ``formato.niveis[].conteudo``
                    # (contrato_json_console.md §12.3): o campo de texto do no
                    # (para ``container``/``conteudo``) ou os campos ``nome`` e
                    # ``valor`` (para ``nome_valor``). ``campo`` e validado contra
                    # esse conjunto estrutural, distinguindo:
                    #   - campo ausente/nulo/vazio/whitespace -> V-14 (origem sem
                    #     valor semantico, ja tratado acima);
                    #   - campo declarado mas inexistente na estrutura -> V-13
                    #     (origem declarada mas incompativel).
                    if _campo_ok and _cp not in _campos_validos_por_no:
                        raise TelaEstruturaInvalida(
                            "{0}: V-13: coluna[{1}] referencia campo {2!r} "
                            "nao declarado em formato.niveis[].conteudo; campo "
                            "de coluna incompativel com a estrutura "
                            "declarada".format(origem, _i_col, _cp)
                        )

    # V-15: condicao excepcional sem politica explicita declarada.
    # politica_modo, modo_inicial ou excesso.modo (legado) no documento externo
    # sao invalidos; campos de politica de modo pertencem ao JSON estrutural
    # da tela (ADR-0028 D23).
    _campos_politica = {"politica_modo", "modo_inicial", "modo"}
    if isinstance(_excesso_fmt, dict):
        _campos_encontrados = _campos_politica & _excesso_fmt.keys()
        if _campos_encontrados:
            raise TelaEstruturaInvalida(
                "{0}: V-15: campo(s) de politica de modo proibido(s) em "
                "formato.excesso do documento externo: {1!r}; politicas de "
                "modo pertencem ao JSON estrutural da tela "
                "(ADR-0028 D23)".format(origem, sorted(_campos_encontrados))
            )
    if "politica_modo" in documento:
        raise TelaEstruturaInvalida(
            "{0}: V-15: campo 'politica_modo' proibido na raiz do documento "
            "externo; politicas de modo pertencem ao JSON estrutural da "
            "tela".format(origem)
        )
    if "modo_inicial" in documento:
        raise TelaEstruturaInvalida(
            "{0}: V-15: campo 'modo_inicial' proibido na raiz do documento "
            "externo; modos iniciais pertencem ao JSON estrutural da "
            "tela".format(origem)
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


# ---------------------------------------------------------------------------
# H-0039 / ADR-0030 — Carregamento global e materializacao do estilo.
#
# ``config/estilo.json`` passa a ser a autoridade global exclusiva de
# aparencia (ADR-0030 D1). ``carregar_estilo`` le o arquivo UMA vez por
# inicializacao, valida toda a estrutura (V-01 a V-29), resolve os presets
# ativos e devolve um ``EstiloResolvido`` imutavel com 18 campos planos.
# Nao ha fallback silencioso: configuracao parcialmente resolvida nunca
# produz ``EstiloResolvido``. O renderer e demais consumidores recebem o
# objeto ja resolvido -- nao releem ``config/estilo.json`` a cada render.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EstiloResolvido:
    """Representacao de runtime do estilo global resolvido (H-0039 D6.2).

    ``frozen=True`` impede alteracao acidental em runtime (contrato_estilo.md
    R-4). Os 18 campos cobrem borda (7), chip (5) e indicadores (6). Nenhum
    campo pode ser omitido -- a configuracao parcialmente resolvida nao pode
    produzir instancia de ``EstiloResolvido``.
    """

    # Borda -- 7 campos (contrato_estilo.md secao 3.1).
    canto_superior_esquerdo: str
    canto_superior_direito: str
    canto_inferior_esquerdo: str
    canto_inferior_direito: str
    traco_superior: str
    traco_inferior: str
    lateral: str
    # Chip -- 5 campos (contrato_estilo.md secao 3.2).
    caractere_esquerdo: str
    caractere_direito: str
    cor_texto: str
    caixa_alta: bool
    cor_fundo: str
    # Indicadores -- 6 campos (contrato_estilo.md secao 3.3).
    concluido_on: str
    concluido_off: str
    selecionado_simbolo: str
    selecionado_off: str
    incluido_on: str
    incluido_off: str


def carregar_estilo(caminho_base=None):
    """Carrega, valida e materializa ``config/estilo.json`` (H-0039 / ADR-0030).

    Le o arquivo uma unica vez por inicializacao da execucao, valida toda a
    estrutura (secoes obrigatórias, ``preset_default``, catálogos, tipos,
    comprimento de caracteres conforme R-6 via ``len(valor) == 1``), resolve
    os presets ativos e devolve um ``EstiloResolvido`` integralmente válido.

    Falha antes de disponibilizar qualquer estilo parcial: toda condicao
    invalida levanta ``EstiloErro``. Nao existe fallback silencioso para
    preset inexistente (V-14 a V-17). O renderer nunca chama esta funcao --
    ele recebe o objeto ja resolvido.

    ``caminho_base`` segue a convenção de ``carregar_tela``: quando ``None``,
    usa a raiz do repositorio derivada de
    ``Path(__file__).resolve().parent.parent``.
    """
    base = _para_base(caminho_base)
    caminho = base / "config" / "estilo.json"

    # V-01: arquivo ausente -- erro explicito, encerramento imediato.
    if not caminho.is_file():
        raise EstiloErro(
            "Arquivo de estilo ausente: {0}".format(caminho)
        )

    # V-02: conteudo nao e JSON valido.
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError as exc:
        raise EstiloErro(
            "Falha ao ler arquivo de estilo {0}: {1}".format(caminho, exc)
        )
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise EstiloErro(
            "JSON invalido em {0}: {1}".format(caminho, exc)
        )

    if not isinstance(dados, dict):
        raise EstiloErro(
            "Raiz de {0} deve ser um objeto JSON; encontrado: {1}".format(
                caminho, type(dados).__name__
            )
        )

    # V-03 a V-05: secoes obrigatórias.
    for secao in ("borda", "chip", "indicadores"):
        if secao not in dados:
            raise EstiloErro(
                "Secao obrigatoria ausente em config/estilo.json: {0!r}".format(
                    secao
                )
            )

    borda_cfg = dados["borda"]
    chip_cfg = dados["chip"]
    indicadores_cfg = dados["indicadores"]

    borda = _resolver_borda(borda_cfg)
    chip = _resolver_chip(chip_cfg)
    concluido_on, concluido_off, selecionado_simbolo, selecionado_off, \
        incluido_on, incluido_off = _resolver_indicadores(indicadores_cfg)

    # V-29: so se chega aqui com todos os campos materializados; a construcao
    # abaixo falharia com TypeError se algum campo estivesse ausente, mas as
    # validacoes acima ja garantem presenca e tipo de cada valor.
    return EstiloResolvido(
        canto_superior_esquerdo=borda["canto_superior_esquerdo"],
        canto_superior_direito=borda["canto_superior_direito"],
        canto_inferior_esquerdo=borda["canto_inferior_esquerdo"],
        canto_inferior_direito=borda["canto_inferior_direito"],
        traco_superior=borda["traco_superior"],
        traco_inferior=borda["traco_inferior"],
        lateral=borda["lateral"],
        caractere_esquerdo=chip["caractere_esquerdo"],
        caractere_direito=chip["caractere_direito"],
        cor_texto=chip["cor_texto"],
        caixa_alta=chip["caixa_alta"],
        cor_fundo=chip["cor_fundo"],
        concluido_on=concluido_on,
        concluido_off=concluido_off,
        selecionado_simbolo=selecionado_simbolo,
        selecionado_off=selecionado_off,
        incluido_on=incluido_on,
        incluido_off=incluido_off,
    )


def _exigir_secao(cfg, secao, caminho_logico):
    """Devolve ``cfg[secao]`` exigindo que seja dict; senao EstiloErro."""
    if not isinstance(cfg, dict):
        raise EstiloErro(
            "{0} deve ser um objeto; encontrado: {1}".format(
                caminho_logico, type(cfg).__name__
            )
        )
    sub = cfg.get(secao)
    if not isinstance(sub, dict):
        raise EstiloErro(
            "{0}.{1} ausente ou nao e objeto".format(caminho_logico, secao)
        )
    return sub


def _resolver_preset_default(cfg, caminho_logico):
    """Exige ``preset_default`` presente e string (V-06..V-09)."""
    if "preset_default" not in cfg:
        raise EstiloErro(
            "{0}.preset_default ausente (sem fallback)".format(caminho_logico)
        )
    valor = cfg["preset_default"]
    if not isinstance(valor, str):
        raise EstiloErro(
            "{0}.preset_default deve ser texto; encontrado: {1}".format(
                caminho_logico, type(valor).__name__
            )
        )
    return valor


def _resolver_catalogo(cfg, caminho_logico):
    """Exige ``presets`` presente e nao vazio (V-10..V-13)."""
    if "presets" not in cfg:
        raise EstiloErro(
            "{0}.presets ausente (catalogo obrigatorio)".format(caminho_logico)
        )
    presets = cfg["presets"]
    if not isinstance(presets, dict) or not presets:
        raise EstiloErro(
            "{0}.presets vazio ou nao e objeto (catalogo obrigatorio)".format(
                caminho_logico
            )
        )
    return presets


def _resolver_preset_ativo(presets, preset_default, caminho_logico):
    """Devolve o preset ativo, sem fallback silencioso (V-14..V-17)."""
    ativo = presets.get(preset_default)
    if not isinstance(ativo, dict):
        raise EstiloErro(
            "{0}.preset_default {1!r} nao existe no catalogo "
            "(sem fallback)".format(caminho_logico, preset_default)
        )
    return ativo


def _campo_obrigatorio(preset, campo, caminho_logico):
    """Exige campo presente (V-18..V-23)."""
    if campo not in preset:
        raise EstiloErro(
            "Campo obrigatorio ausente: {0}.{1}".format(caminho_logico, campo)
        )
    return preset[campo]


def _validar_caractere(valor, caminho_logico):
    """Valida string de comprimento 1 (R-6 via ``len() == 1``).

    Cobre V-24 (nao string), V-27 (``len != 1``) e V-28 (string vazia). O
    limite tecnico de code point -- e nao largura visual de terminal -- e o
    aprovado pelo handoff H-0039 D6.6 e ADR-0030 D9.
    """
    if not isinstance(valor, str):
        raise EstiloErro(
            "{0} deve ser texto; encontrado: {1}".format(
                caminho_logico, type(valor).__name__
            )
        )
    if len(valor) != 1:
        raise EstiloErro(
            "{0} deve ter exatamente 1 caractere (R-6); "
            "encontrado: {1!r} (len={2})".format(
                caminho_logico, valor, len(valor)
            )
        )
    return valor


def _resolver_borda(borda_cfg):
    """Resolve o preset ativo de borda e materializa os 7 campos."""
    if not isinstance(borda_cfg, dict):
        raise EstiloErro("Secao 'borda' deve ser um objeto")
    preset_default = _resolver_preset_default(borda_cfg, "borda")
    presets = _resolver_catalogo(borda_cfg, "borda")
    ativo = _resolver_preset_ativo(presets, preset_default, "borda.presets")

    campos = {}
    for campo in (
        "canto_superior_esquerdo", "canto_superior_direito",
        "canto_inferior_esquerdo", "canto_inferior_direito",
        "traco_superior", "traco_inferior", "lateral",
    ):
        valor = _campo_obrigatorio(ativo, campo, "borda.presets[{0!r}]".format(
            preset_default
        ))
        campos[campo] = _validar_caractere(
            valor, "borda.presets[{0!r}].{1}".format(preset_default, campo)
        )
    return campos


def _resolver_chip(chip_cfg):
    """Resolve o preset ativo de chip e materializa os 5 campos."""
    if not isinstance(chip_cfg, dict):
        raise EstiloErro("Secao 'chip' deve ser um objeto")
    preset_default = _resolver_preset_default(chip_cfg, "chip")
    presets = _resolver_catalogo(chip_cfg, "chip")
    ativo = _resolver_preset_ativo(presets, preset_default, "chip.presets")

    caractere_esquerdo = _campo_obrigatorio(
        ativo, "caractere_esquerdo",
        "chip.presets[{0!r}]".format(preset_default),
    )
    caractere_direito = _campo_obrigatorio(
        ativo, "caractere_direito",
        "chip.presets[{0!r}]".format(preset_default),
    )
    cor_texto = _campo_obrigatorio(
        ativo, "cor_texto", "chip.presets[{0!r}]".format(preset_default),
    )
    cor_fundo = _campo_obrigatorio(
        ativo, "cor_fundo", "chip.presets[{0!r}]".format(preset_default),
    )
    if "caixa_alta" not in ativo:
        raise EstiloErro(
            "Campo obrigatorio ausente: chip.presets[{0!r}].caixa_alta".format(
                preset_default
            )
        )
    caixa_alta = ativo["caixa_alta"]
    if not isinstance(caixa_alta, bool):  # V-25
        raise EstiloErro(
            "chip.presets[{0!r}].caixa_alta deve ser booleano; encontrado: "
            "{1}".format(preset_default, type(caixa_alta).__name__)
        )
    if not isinstance(cor_texto, str):  # V-26
        raise EstiloErro(
            "chip.presets[{0!r}].cor_texto deve ser texto".format(
                preset_default
            )
        )
    if not isinstance(cor_fundo, str):  # V-26
        raise EstiloErro(
            "chip.presets[{0!r}].cor_fundo deve ser texto".format(
                preset_default
            )
        )

    return {
        "caractere_esquerdo": _validar_caractere(
            caractere_esquerdo,
            "chip.presets[{0!r}].caractere_esquerdo".format(preset_default),
        ),
        "caractere_direito": _validar_caractere(
            caractere_direito,
            "chip.presets[{0!r}].caractere_direito".format(preset_default),
        ),
        "cor_texto": cor_texto,
        "caixa_alta": caixa_alta,
        "cor_fundo": cor_fundo,
    }


def _resolver_indicadores(indicadores_cfg):
    """Materializa os 6 campos de indicadores.

    - ``concluido``: par direto ``on``/``off``.
    - ``selecionado``: preset ativo -> ``simbolo``; campo direto ``off``.
    - ``incluido``: preset ativo -> ``on``/``off``.
    """
    if not isinstance(indicadores_cfg, dict):
        raise EstiloErro("Secao 'indicadores' deve ser um objeto")

    # --- concluido (par direto) ---
    concluido = _exigir_secao(indicadores_cfg, "concluido", "indicadores")
    concluido_on = _campo_obrigatorio(
        concluido, "on", "indicadores.concluido"
    )  # V-22
    concluido_off = _campo_obrigatorio(
        concluido, "off", "indicadores.concluido"
    )  # V-22
    concluido_on = _validar_caractere(concluido_on, "indicadores.concluido.on")
    concluido_off = _validar_caractere(
        concluido_off, "indicadores.concluido.off"
    )

    # --- selecionado (preset + campo direto off) ---
    selecionado = _exigir_secao(
        indicadores_cfg, "selecionado", "indicadores"
    )
    sel_default = _resolver_preset_default(
        selecionado, "indicadores.selecionado"
    )  # V-08
    sel_presets = _resolver_catalogo(
        selecionado, "indicadores.selecionado"
    )  # V-12
    sel_ativo = _resolver_preset_ativo(
        sel_presets, sel_default, "indicadores.selecionado.presets"
    )  # V-16
    simbolo = _campo_obrigatorio(
        sel_ativo, "simbolo", "indicadores.selecionado.presets[{0!r}]".format(
            sel_default
        ),
    )  # V-20
    selecionado_simbolo = _validar_caractere(
        simbolo,
        "indicadores.selecionado.presets[{0!r}].simbolo".format(sel_default),
    )
    selecionado_off = _campo_obrigatorio(
        selecionado, "off", "indicadores.selecionado"
    )  # V-23
    selecionado_off = _validar_caractere(
        selecionado_off, "indicadores.selecionado.off"
    )

    # --- incluido (preset on/off) ---
    incluido = _exigir_secao(indicadores_cfg, "incluido", "indicadores")
    inc_default = _resolver_preset_default(
        incluido, "indicadores.incluido"
    )  # V-09
    inc_presets = _resolver_catalogo(
        incluido, "indicadores.incluido"
    )  # V-13
    inc_ativo = _resolver_preset_ativo(
        inc_presets, inc_default, "indicadores.incluido.presets"
    )  # V-17
    inc_on = _campo_obrigatorio(
        inc_ativo, "on", "indicadores.incluido.presets[{0!r}]".format(
            inc_default
        ),
    )  # V-21
    inc_off = _campo_obrigatorio(
        inc_ativo, "off", "indicadores.incluido.presets[{0!r}]".format(
            inc_default
        ),
    )  # V-21
    incluido_on = _validar_caractere(
        inc_on,
        "indicadores.incluido.presets[{0!r}].on".format(inc_default),
    )
    incluido_off = _validar_caractere(
        inc_off,
        "indicadores.incluido.presets[{0!r}].off".format(inc_default),
    )

    return (
        concluido_on, concluido_off,
        selecionado_simbolo, selecionado_off,
        incluido_on, incluido_off,
    )
