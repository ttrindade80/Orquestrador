"""Designadores de conteúdo multinível."""



_ROMANOS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def _romano(n):
    """Numeral romano maiusculo de ``n`` (n >= 1)."""
    if n < 1:
        return ""
    resultado = []
    for valor, simbolo in _ROMANOS:
        while n >= valor:
            resultado.append(simbolo)
            n -= valor
    return "".join(resultado)


def _alfabetico(n, maiusculo=False):
    """Sequencia alfabetica bijetiva de ``n`` (1->a, 26->z, 27->aa)."""
    if n < 1:
        return ""
    letras = []
    base = ord("A") if maiusculo else ord("a")
    while n > 0:
        n, resto = divmod(n - 1, 26)
        letras.append(chr(base + resto))
    return "".join(reversed(letras))


def _texto_designador(designador, ordinal, ancestrais):
    """Calcula o texto concreto do designador de um no (H-0036 secao 13.7).

    ``ordinal`` e a posicao 1-based entre irmaos do mesmo nivel; ``ancestrais``
    e a lista de ordinais decimais dos ancestrais (para ``decimal_composto``).
    Aplica ``prefixo`` e ``sufixo`` quando declarados. ``nenhum`` produz string
    vazia (sem marcador).
    """
    if not isinstance(designador, dict):
        return ""
    tipo = designador.get("tipo", "nenhum")
    if tipo == "nenhum":
        return ""
    prefixo = designador.get("prefixo", "")
    sufixo = designador.get("sufixo", "")
    if tipo == "simbolo":
        nucleo = designador.get("valor", "•")
    elif tipo == "personalizado":
        nucleo = designador.get("valor", "")
    elif tipo == "decimal":
        nucleo = str(ordinal)
    elif tipo == "alfabetico_minusculo":
        nucleo = _alfabetico(ordinal, maiusculo=False)
    elif tipo == "alfabetico_maiusculo":
        nucleo = _alfabetico(ordinal, maiusculo=True)
    elif tipo == "romano_minusculo":
        nucleo = _romano(ordinal).lower()
    elif tipo == "romano_maiusculo":
        nucleo = _romano(ordinal)
    elif tipo == "decimal_composto":
        separador = designador.get("separador", ".")
        nucleo = separador.join(str(n) for n in (list(ancestrais) + [ordinal]))
    else:
        nucleo = ""
    return "{0}{1}{2}".format(prefixo, nucleo, sufixo)


def _texto_no_conteudo(no, nivel):
    """Texto exibivel de um no conforme o tipo do seu nivel.

    - ``container``/``conteudo``: valor do campo nomeado por ``nivel.conteudo``.
    - ``nome_valor``: ``"nome: valor"`` a partir dos campos declarados.
    """
    if nivel is None:
        return ""
    if nivel.tipo == "nome_valor":
        campo_nome = nivel.conteudo.get("nome")
        campo_valor = nivel.conteudo.get("valor")
        return "{0}: {1}".format(
            no.campos.get(campo_nome, ""), no.campos.get(campo_valor, "")
        )
    campo = nivel.conteudo
    return "{0}".format(no.campos.get(campo, ""))
