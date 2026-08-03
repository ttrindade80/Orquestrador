"""Validação declarativa de distribuicao_matricial."""

from tela.carregamento.erros import TelaEstruturaInvalida

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
