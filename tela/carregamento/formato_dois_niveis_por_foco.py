"""Validação do bloco formato.dois_niveis_por_foco.filho (ADR-0047 / H-0072)."""

from tela.carregamento.erros import TelaEstruturaInvalida

_DESIGNADORES_FILHO_VALIDOS = frozenset({
    "decimal_composto", "alfabetico_maiusculo", "nenhum",
})
_APRESENTACOES_FILHO_VALIDAS = frozenset({"texto", "tabela"})


def _exigir_inteiro_positivo(valor, caminho):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise TelaEstruturaInvalida(
            "'{0}' deve ser inteiro positivo; recebido: {1!r}".format(
                caminho, valor
            )
        )


def _validar_intervalo_minimo_maximo(bloco, caminho):
    if not isinstance(bloco, dict):
        raise TelaEstruturaInvalida("'{0}' deve ser objeto".format(caminho))
    desconhecidos = sorted(set(bloco) - {"minimo", "maximo"})
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "campo(s) desconhecido(s) em '{0}': {1}".format(
                caminho, ", ".join(repr(c) for c in desconhecidos)
            )
        )
    if "minimo" not in bloco:
        raise TelaEstruturaInvalida("'{0}.minimo' ausente".format(caminho))
    if "maximo" not in bloco:
        raise TelaEstruturaInvalida("'{0}.maximo' ausente".format(caminho))
    minimo = bloco["minimo"]
    maximo = bloco["maximo"]
    _exigir_inteiro_positivo(minimo, "{0}.minimo".format(caminho))
    _exigir_inteiro_positivo(maximo, "{0}.maximo".format(caminho))
    if minimo > maximo:
        raise TelaEstruturaInvalida(
            "'{0}': minimo ({1}) deve ser menor ou igual a maximo "
            "({2})".format(caminho, minimo, maximo)
        )


def _validar_designador_filho(designador, caminho):
    if not isinstance(designador, dict):
        raise TelaEstruturaInvalida("'{0}' deve ser objeto".format(caminho))
    # V-DNF-14: objeto fechado em tipo, prefixo e sufixo.
    desconhecidos = sorted(set(designador) - {"tipo", "prefixo", "sufixo"})
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "campo(s) desconhecido(s) em '{0}': {1}".format(
                caminho, ", ".join(repr(c) for c in desconhecidos)
            )
        )
    if "tipo" not in designador:
        raise TelaEstruturaInvalida("'{0}.tipo' ausente".format(caminho))
    tipo = designador["tipo"]
    if tipo not in _DESIGNADORES_FILHO_VALIDOS:
        raise TelaEstruturaInvalida(
            "'{0}.tipo' invalido: {1!r}; aceitos: {2}".format(
                caminho, tipo, ", ".join(sorted(_DESIGNADORES_FILHO_VALIDOS))
            )
        )
    # V-DNF-12 / V-DNF-15
    if "prefixo" in designador:
        if not isinstance(designador["prefixo"], str):
            raise TelaEstruturaInvalida(
                "'{0}.prefixo' deve ser string".format(caminho)
            )
        if tipo == "nenhum":
            raise TelaEstruturaInvalida(
                "'{0}.prefixo' nao e admitido quando tipo e 'nenhum'".format(
                    caminho
                )
            )
    # V-DNF-13 / V-DNF-16
    if "sufixo" in designador:
        if not isinstance(designador["sufixo"], str):
            raise TelaEstruturaInvalida(
                "'{0}.sufixo' deve ser string".format(caminho)
            )
        if tipo == "nenhum":
            raise TelaEstruturaInvalida(
                "'{0}.sufixo' nao e admitido quando tipo e 'nenhum'".format(
                    caminho
                )
            )


def _validar_colunas_tabela(colunas, caminho):
    if not isinstance(colunas, list) or len(colunas) == 0:
        raise TelaEstruturaInvalida(
            "'{0}' deve ser lista com ao menos 1 elemento".format(caminho)
        )
    for indice, coluna in enumerate(colunas):
        caminho_item = "{0}[{1}]".format(caminho, indice)
        if not isinstance(coluna, dict) or set(coluna) != {"campo"}:
            raise TelaEstruturaInvalida(
                "'{0}' deve ser objeto com exatamente o campo "
                "'campo'".format(caminho_item)
            )
        if not isinstance(coluna["campo"], str) or not coluna["campo"]:
            raise TelaEstruturaInvalida(
                "'{0}.campo' deve ser string nao vazia".format(caminho_item)
            )


def _validar_tabela_filho(tabela, caminho):
    if not isinstance(tabela, dict):
        raise TelaEstruturaInvalida("'{0}' deve ser objeto".format(caminho))
    desconhecidos = sorted(set(tabela) - {"colunas", "espacamento"})
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "campo(s) desconhecido(s) em '{0}': {1}".format(
                caminho, ", ".join(repr(c) for c in desconhecidos)
            )
        )
    if "colunas" not in tabela:
        raise TelaEstruturaInvalida("'{0}.colunas' ausente".format(caminho))
    _validar_colunas_tabela(tabela["colunas"], caminho + ".colunas")
    if "espacamento" not in tabela:
        raise TelaEstruturaInvalida(
            "'{0}.espacamento' ausente".format(caminho)
        )
    _validar_intervalo_minimo_maximo(
        tabela["espacamento"], caminho + ".espacamento"
    )


def _validar_formato_dois_niveis_filho(elemento, id_elemento, tipo_navegacao):
    """Valida ``formato.dois_niveis_por_foco.filho`` de um elemento console.

    Analogo em forma a ``_validar_d23_console`` (``formato.excesso``):
    recebe o elemento cru do JSON, o id para mensagens de erro e o
    ``politica_navegacao.tipo`` ja lido pelo chamador (``None`` quando
    ausente/invalido). A ausencia do bloco nunca e erro (V-DNF-11 cobre
    apenas a presenca indevida). Falha fechada: rejeita
    CONFIGURACAO_INVALIDA sem fallback silencioso (ADR-0047 D-DNF-01..11 /
    H-0072 §20; P01 acrescenta V-DNF-12..16 em designador).
    """
    formato = elemento.get("formato")
    if not isinstance(formato, dict) or "dois_niveis_por_foco" not in formato:
        return

    bloco = formato["dois_niveis_por_foco"]
    caminho_base = "elemento '{0}'.formato.dois_niveis_por_foco".format(
        id_elemento
    )
    if not isinstance(bloco, dict) or set(bloco) != {"filho"}:
        raise TelaEstruturaInvalida(
            "{0} deve ser objeto com exatamente o campo 'filho'".format(
                caminho_base
            )
        )

    # V-DNF-11: o bloco so existe quando a politica de navegacao efetiva do
    # console e 'dois_niveis_por_foco'.
    if tipo_navegacao != "dois_niveis_por_foco":
        raise TelaEstruturaInvalida(
            "{0}.filho presente, mas politica_navegacao.tipo nao e "
            "'dois_niveis_por_foco' (recebido: {1!r})".format(
                caminho_base, tipo_navegacao
            )
        )

    filho = bloco["filho"]
    caminho = caminho_base + ".filho"
    if not isinstance(filho, dict):
        raise TelaEstruturaInvalida("'{0}' deve ser objeto".format(caminho))

    campos_permitidos = {"tabulacao", "designador", "apresentacao", "tabela"}
    desconhecidos = sorted(set(filho) - campos_permitidos)
    if desconhecidos:
        raise TelaEstruturaInvalida(
            "campo(s) desconhecido(s) em '{0}': {1}".format(
                caminho, ", ".join(repr(c) for c in desconhecidos)
            )
        )
    for campo in ("tabulacao", "designador", "apresentacao"):
        if campo not in filho:
            raise TelaEstruturaInvalida(
                "'{0}.{1}' ausente".format(caminho, campo)
            )

    # V-DNF-01 / V-DNF-02
    _validar_intervalo_minimo_maximo(filho["tabulacao"], caminho + ".tabulacao")
    # V-DNF-10 / V-DNF-12..16
    _validar_designador_filho(filho["designador"], caminho + ".designador")

    # V-DNF-03
    apresentacao = filho["apresentacao"]
    if apresentacao not in _APRESENTACOES_FILHO_VALIDAS:
        raise TelaEstruturaInvalida(
            "'{0}.apresentacao' invalida: {1!r}; aceitos: 'texto', "
            "'tabela'".format(caminho, apresentacao)
        )

    tem_tabela = "tabela" in filho
    # V-DNF-04
    if apresentacao == "tabela" and not tem_tabela:
        raise TelaEstruturaInvalida(
            "'{0}.tabela' ausente; obrigatorio quando apresentacao == "
            "'tabela'".format(caminho)
        )
    # V-DNF-05
    if apresentacao == "texto" and tem_tabela:
        raise TelaEstruturaInvalida(
            "'{0}.tabela' presente, mas apresentacao == 'texto' (bloco "
            "redundante proibido)".format(caminho)
        )
    if tem_tabela:
        # V-DNF-06 / V-DNF-07 / V-DNF-08 / V-DNF-09
        _validar_tabela_filho(filho["tabela"], caminho + ".tabela")
