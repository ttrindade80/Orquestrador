"""Fixture autouse do H-0038: converte `_registrar(False)` em falha pytest.

Os dez scripts de teste da suite registram o resultado de cada verificacao
interna em uma lista de modulo `_RESULTADOS` (no padrao
`(nome, passou)`), e dependiam do bloco `main()` para computar o codigo de
saida. Como o pytest coleta e executa os itens diretamente, sem chamar
`main()`, uma verificacao interna registrada como falsa precisava de um
mecanismo adicional para se tornar falha de item pytest.

Este modulo define uma unica fixture `autouse` de escopo `function` que:

1. obtem o modulo do item coletado;
2. localiza `_RESULTADOS` quando existir;
3. limpa `_RESULTADOS` antes de cada item (isolamento entre itens);
4. permite que a funcao de teste execute todas as suas verificacoes;
5. inspeciona `_RESULTADOS` apos o item;
6. reune todas as entradas cujo resultado seja falso;
7. produz falha real do pytest, com os nomes das verificacoes reprovadas;
8. nao depende de `main()`;
9. nao altera `_registrar()` nos arquivos de teste;
10. nao esconde nem transforma em aprovacao uma falha ou excecao nativa do
    teste (a fixture so levanta apos a execucao do item, e qualquer
    AssertionError ou excecao nativa ja tera reprovado o item antes).

Quando o modulo do item nao possuir `_RESULTADOS`, a fixture funciona como
operacao neutra (no-op).

Nenhuma outra politica funcional e adicionada neste arquivo.
"""

import pytest


def _iter_nomes_falsos(resultados):
    """Itera sobre os nomes das verificacoes registradas como falsas.

    Aceita tuplas no padrao `(nome, passou)` usado pelos dez scripts. Se uma
    entrada tiver formato inesperado, ela e ignorada de forma defensiva para
    nao mascarar o comportamento das demais.
    """
    for entrada in resultados:
        if not isinstance(entrada, (tuple, list)) or len(entrada) < 2:
            continue
        nome, passou = entrada[0], entrada[1]
        if not passou:
            yield nome


@pytest.fixture(autouse=True)
def verificar_resultados_internos(request):
    """Gate do H-0038: limpa e verifica `_RESULTADOS` ao redor de cada item.

    O `yield` fica entre a limpeza (setup) e a inspecao (teardown), de modo
    que qualquer excecao nativa levantada pela funcao de teste reprova o item
    antes da inspecao. A inspecao so roteia entradas falsas para
    `AssertionError` quando o proprio item nao falhou por outro motivo.
    """
    modulo = getattr(request, "module", None)
    resultados = getattr(modulo, "_RESULTADOS", None)

    # Quando o modulo nao possui _RESULTADOS, a fixture e neutra.
    if resultados is None:
        yield
        return

    # Limpa antes do item para garantir isolamento entre funcoes de teste.
    try:
        resultados.clear()
    except AttributeError:
        # _RESULTADOS existe mas nao e uma lista mutavel com clear(); nao
        # tenta reatribuir para nao alterar a logica dos arquivos de teste.
        pass

    yield

    # Apos a execucao, inspeciona o acumulado. Reprova apenas se houver
    # entradas falsas; caso contrario, o item permanece no estado definido
    # pela sua propria execucao (passou, falhou nativamente ou erro).
    nomes_falsos = list(_iter_nomes_falsos(resultados))
    if nomes_falsos:
        lista = ", ".join(repr(n) for n in nomes_falsos)
        raise AssertionError(
            "verificacoes internas reprovadas pelo gate do H-0038: "
            "{0}".format(lista)
        )
