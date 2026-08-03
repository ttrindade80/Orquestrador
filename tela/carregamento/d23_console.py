"""Validação da política de modo D23 de consoles."""

from tela.carregamento.envelope_pre_adr_0028 import _TELAS_LEGADAS_D23
from tela.carregamento.erros import TelaEstruturaInvalida

_POLITICAS_MODO_VALIDAS = frozenset({
    "somente_verboso", "somente_nao_verboso", "alternavel"
})
_MODOS_INICIAIS_VALIDOS = frozenset({"verboso", "nao_verboso"})
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
