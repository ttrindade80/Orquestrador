"""Carregamento e validação da configuração de lancador."""

import json
import os

from tela.carregamento.erros import (
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaEstruturaInvalida,
    TelaJsonInvalido,
)

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
