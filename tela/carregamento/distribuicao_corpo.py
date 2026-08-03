"""Validação de corpo.distribuicao."""

from tela.carregamento.erros import TelaEstruturaInvalida
from tela.carregamento.taxonomia import MODOS_DISTRIBUICAO_CORPO_VALIDOS

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
