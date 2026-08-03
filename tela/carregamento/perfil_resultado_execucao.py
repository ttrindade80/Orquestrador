"""Validação do perfil resultado_execucao."""

from tela.carregamento.envelope_pre_adr_0028 import _console_em_escopo_d23
from tela.carregamento.erros import TelaEstruturaInvalida
from tela.carregamento.taxonomia import PERFIL_RESULTADO_EXECUCAO

_CAMPOS_CONSOLE_RESULTADO_PERMITIDOS = frozenset({"id", "tipo", "titulo", "formato"})

# Campos classicos do envelope pre-ADR-0028 proibidos no consumidor D23 do
# perfil resultado_execucao (alem da exclusao mutua ja aplicada por
# ``_console_em_escopo_d23``).
_CAMPOS_CLASSICOS_PROIBIDOS_RESULTADO = frozenset({
    "origem_dados",
    "itens",
    "regra_geracao_itens",
    "politica_composicao",
    "politica_navegacao",
    "politica_selecao",
    "politica_paginacao",
    "politica_exibicao",
    "verboso",
    "overflow_normal",
    "dados",
    "conteudo",
    "documento",
    "resultado",
})
def _validar_perfil_resultado_execucao(dados, elementos, distribuicao_corpo):
    """Valida a estrutura obrigatoria do perfil ``resultado_execucao`` (H-0043).

    Exige console unico consumidor D23 puro com ``politica_modo: somente_verboso``,
    sem ``modo_inicial``, sem campos classicos, sem segundo elemento funcional,
    sem ``corpo.distribuicao`` e com exatamente o chip ``Esc``/``Voltar``.
    Nao decide documento versus envelope e nao relaxa ``_console_em_escopo_d23``.
    """
    if distribuicao_corpo is not None:
        raise TelaEstruturaInvalida(
            "perfil '{0}': corpo.distribuicao e proibido (cardinalidade "
            "unitaria)".format(PERFIL_RESULTADO_EXECUCAO)
        )

    if not isinstance(elementos, list) or len(elementos) != 1:
        raise TelaEstruturaInvalida(
            "perfil '{0}': corpo.elementos deve conter exatamente um "
            "elemento".format(PERFIL_RESULTADO_EXECUCAO)
        )

    elemento = elementos[0]
    if not isinstance(elemento, dict):
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento unico invalido".format(
                PERFIL_RESULTADO_EXECUCAO
            )
        )

    tipo = elemento.get("tipo")
    if tipo != "console":
        raise TelaEstruturaInvalida(
            "perfil '{0}': unico elemento deve ser console; recebido: "
            "{1!r}".format(PERFIL_RESULTADO_EXECUCAO, tipo)
        )

    if tipo in ("dashboard", "lancador", "grupo") or tipo != "console":
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento funcional adicional ou tipo proibido: "
            "{1!r}".format(PERFIL_RESULTADO_EXECUCAO, tipo)
        )

    id_elemento = elemento.get("id", "?")
    extras = set(elemento) - _CAMPOS_CONSOLE_RESULTADO_PERMITIDOS
    classicos = extras & _CAMPOS_CLASSICOS_PROIBIDOS_RESULTADO
    if classicos:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' declara campos classicos "
            "proibidos no consumidor D23: {2}".format(
                PERFIL_RESULTADO_EXECUCAO,
                id_elemento,
                ", ".join(sorted(classicos)),
            )
        )
    if extras:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' declara campos nao permitidos no "
            "consumidor D23 puro: {2}".format(
                PERFIL_RESULTADO_EXECUCAO,
                id_elemento,
                ", ".join(sorted(extras)),
            )
        )

    # Garante exclusao mutua D23 (nao relaxa a regra vigente).
    if not _console_em_escopo_d23(elemento, dados.get("id")):
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' nao e consumidor D23 puro".format(
                PERFIL_RESULTADO_EXECUCAO, id_elemento
            )
        )

    formato = elemento.get("formato")
    if not isinstance(formato, dict):
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' exige formato objeto".format(
                PERFIL_RESULTADO_EXECUCAO, id_elemento
            )
        )
    extras_formato = set(formato) - {"excesso"}
    if extras_formato:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' declara chaves extras em formato: "
            "{2}".format(
                PERFIL_RESULTADO_EXECUCAO,
                id_elemento,
                ", ".join(sorted(extras_formato)),
            )
        )
    excesso = formato.get("excesso")
    if not isinstance(excesso, dict):
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' exige formato.excesso objeto".format(
                PERFIL_RESULTADO_EXECUCAO, id_elemento
            )
        )
    if "modo_inicial" in excesso:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' nao aceita modo_inicial".format(
                PERFIL_RESULTADO_EXECUCAO, id_elemento
            )
        )
    if "overflow_normal" in excesso or "overflow_normal" in elemento:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' nao aceita regra de truncamento "
            "(overflow_normal)".format(PERFIL_RESULTADO_EXECUCAO, id_elemento)
        )
    extras_excesso = set(excesso) - {"politica_modo"}
    if extras_excesso:
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' declara chaves extras em "
            "formato.excesso: {2}".format(
                PERFIL_RESULTADO_EXECUCAO,
                id_elemento,
                ", ".join(sorted(extras_excesso)),
            )
        )
    if excesso.get("politica_modo") != "somente_verboso":
        raise TelaEstruturaInvalida(
            "perfil '{0}': elemento '{1}' exige politica_modo "
            "'somente_verboso'; recebido: {2!r}".format(
                PERFIL_RESULTADO_EXECUCAO,
                id_elemento,
                excesso.get("politica_modo"),
            )
        )

    barra = dados.get("barra_de_menus")
    if not isinstance(barra, dict):
        raise TelaEstruturaInvalida(
            "perfil '{0}': barra_de_menus invalida".format(
                PERFIL_RESULTADO_EXECUCAO
            )
        )
    chips = barra.get("chips")
    if not isinstance(chips, list) or len(chips) != 1:
        raise TelaEstruturaInvalida(
            "perfil '{0}': barra_de_menus.chips deve conter exatamente um "
            "chip (Esc/Voltar)".format(PERFIL_RESULTADO_EXECUCAO)
        )
    chip = chips[0]
    if not isinstance(chip, dict):
        raise TelaEstruturaInvalida(
            "perfil '{0}': chip unico invalido".format(PERFIL_RESULTADO_EXECUCAO)
        )
    tecla = chip.get("tecla")
    texto = chip.get("texto")
    if tecla != "Esc" or texto != "Voltar":
        raise TelaEstruturaInvalida(
            "perfil '{0}': chip unico deve ser Esc/Voltar; recebido "
            "tecla={1!r} texto={2!r}".format(
                PERFIL_RESULTADO_EXECUCAO, tecla, texto
            )
        )
    if tecla == "V" or texto == "Verboso" or chip.get("id") in {"v", "chip_v", "V"}:
        raise TelaEstruturaInvalida(
            "perfil '{0}': chip [V] e proibido".format(PERFIL_RESULTADO_EXECUCAO)
        )
