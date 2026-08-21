"""Composição canônica de texto físico da TUI.

O módulo cuida somente da transformação de texto em linhas físicas e da
justificação explicitamente solicitada. Padding, alinhamento estrutural e
geometria pertencem ao consumidor.
"""

from tela.renderizacao.texto_ansi import (
    _atualizar_sgr,
    _estado_sgr_vazio,
    _prefixo_sgr,
    _sufixo_sgr,
    _tokens_ansi,
    _largura_sem_ansi,
)


def _unidades_visuais(texto):
    """Retorna unidades visuais e os controles finais.

    O parser ANSI continua sendo o de ``texto_ansi``. Cada unidade guarda os
    controles que a precedem, o caractere visível e o estado SGR após esses
    controles. Isso permite materializar linhas sem partir CSI ou palavras.
    """
    unidades = []
    pendente = ""
    estado = _estado_sgr_vazio()
    for tipo, valor in _tokens_ansi(texto):
        if tipo == "sgr":
            pendente += valor
            _atualizar_sgr(estado, valor)
            continue
        unidades.append((pendente + valor, valor, dict(estado)))
        pendente = ""
    return unidades, pendente


def _controles(unidades):
    """Retorna os controles CSI de ``unidades`` sem suas células visíveis."""
    return "".join(
        tipo_valor
        for unidade in unidades
        for tipo, tipo_valor in _tokens_ansi(unidade[0])
        if tipo == "sgr"
    )


def _palavras_e_vaos(unidades):
    """Separa palavras e vãos sem quebrar uma palavra visual.

    A separação é deliberadamente lexical: uma palavra é uma sequência de
    células não brancas e um vão é a sequência de células brancas entre duas
    palavras. Os elementos continuam sendo as unidades produzidas pelo
    parser ANSI existente, logo controles CSI nunca são tratados como
    caracteres nem podem ser partidos.
    """
    palavras = []
    vaos = []
    palavra = []
    vao = []
    controles_iniciais = ""

    for unidade in unidades:
        if unidade[1].isspace():
            if palavra:
                vao.append(unidade)
            else:
                controles_iniciais += _controles([unidade])
            continue
        if palavra and vao:
            palavras.append(palavra)
            vaos.append(vao)
            palavra = []
            vao = []
        if palavra:
            palavra.append(unidade)
            continue
        palavra = [unidade]

    if palavra:
        palavras.append(palavra)
    return controles_iniciais, palavras, vaos


def _largura_unidades(unidades):
    return len(unidades)


def _materializar_linhas(linhas, controles_finais):
    """Materializa linhas lógicas e fecha/restaura SGR entre linhas."""
    resultado = []
    estado = _estado_sgr_vazio()
    for indice_linha, elementos in enumerate(linhas):
        partes = [_prefixo_sgr(estado)]
        estado_linha = dict(estado)
        for unidade in elementos:
            partes.append(unidade[0])
            for tipo, valor in _tokens_ansi(unidade[0]):
                if tipo == "sgr":
                    _atualizar_sgr(estado_linha, valor)
        ultima = indice_linha == len(linhas) - 1
        if ultima:
            partes.append(controles_finais)
            for tipo, valor in _tokens_ansi(controles_finais):
                if tipo == "sgr":
                    _atualizar_sgr(estado_linha, valor)
        partes.append(_sufixo_sgr(estado_linha))
        resultado.append("".join(partes))
        estado = estado_linha
    return resultado


def _formar_linhas_por_palavra(unidades, largura):
    """Forma linhas por palavras, aceitando uma palavra larga intacta."""
    controles_iniciais, palavras, vaos = _palavras_e_vaos(unidades)
    if not palavras:
        return None

    linhas = []
    atual = []
    largura_atual = 0
    for indice, palavra in enumerate(palavras):
        largura_palavra = _largura_unidades(palavra)
        vao = vaos[indice - 1] if indice else []
        largura_vao = _largura_unidades(vao)
        candidato = largura_atual + largura_vao + largura_palavra
        if atual and candidato > largura:
            linhas.append(atual)
            atual = []
            largura_atual = 0
            # O espaço que marcou a fronteira não é uma palavra. Seus
            # controles, porém, precisam preceder a próxima palavra para
            # conservar transições ANSI feitas nesse vão.
            if vao:
                controles = _controles(vao)
                if controles:
                    atual.append((controles, "", {}))
            atual.extend(palavra)
            largura_atual = largura_palavra
            continue
        if atual:
            atual.extend(vao)
            largura_atual += largura_vao
        atual.extend(palavra)
        largura_atual += largura_palavra
    if atual:
        linhas.append(atual)

    if controles_iniciais:
        linhas[0].insert(0, (controles_iniciais, "", {}))
    return linhas


def _quebrar_texto(texto, largura):
    """Quebra um parágrafo em linhas compostas por palavras inteiras."""
    if isinstance(largura, bool) or not isinstance(largura, int):
        raise ValueError("largura util nao inteira")
    if largura <= 0:
        raise ValueError("largura util nao positiva")
    unidades, controles_finais = _unidades_visuais(texto)
    if not unidades:
        return [texto]
    linhas = _formar_linhas_por_palavra(unidades, largura)
    if linhas is None:
        return [texto]
    if len(linhas) == 1:
        return [texto]
    return _materializar_linhas(linhas, controles_finais)


def _justificar_linha(texto, largura):
    """Expande somente vãos internos existentes até ``largura`` visual."""
    extra = largura - _largura_sem_ansi(texto)
    if extra <= 0:
        return texto

    unidades, controles_finais = _unidades_visuais(texto)
    vãos = []
    indice = 0
    while indice < len(unidades):
        if not unidades[indice][1].isspace():
            indice += 1
            continue
        inicio = indice
        while indice < len(unidades) and unidades[indice][1].isspace():
            indice += 1
        if (
            inicio > 0
            and indice < len(unidades)
            and not unidades[inicio - 1][1].isspace()
            and not unidades[indice][1].isspace()
        ):
            vãos.append((inicio, indice))

    if not vãos:
        return texto

    base, resto = divmod(extra, len(vãos))
    acrescimos = [base + (1 if indice < resto else 0) for indice in range(len(vãos))]
    por_fim = {fim - 1: acrescimo for (_, fim), acrescimo in zip(vãos, acrescimos)}
    partes = []
    for indice, unidade in enumerate(unidades):
        partes.append(unidade[0])
        partes.append(" " * por_fim.get(indice, 0))
    partes.append(controles_finais)
    return "".join(partes)


def compor_texto(texto, largura_util, modo="normal", justificar_ultima=True):
    """Compõe texto em linhas físicas para uma largura útil positiva.

    ``modo`` aceita ``"normal"`` ou ``"justificado"``. No segundo caso a
    justificação é explícita e a opção ``justificar_ultima`` deixa a política
    da última linha sob controle do consumidor.
    """
    if not isinstance(texto, str):
        raise ValueError("texto deve ser textual")
    if isinstance(largura_util, bool) or not isinstance(largura_util, int):
        raise ValueError("largura util nao inteira")
    if largura_util <= 0:
        raise ValueError("largura util nao positiva")
    if modo not in {"normal", "justificado"}:
        raise ValueError("modo de composicao desconhecido")
    if not isinstance(justificar_ultima, bool):
        raise ValueError("justificar_ultima deve ser booleana")

    linhas = _quebrar_texto(texto, largura_util)
    if modo != "justificado":
        return linhas
    return [
        _justificar_linha(linha, largura_util)
        if (justificar_ultima or indice < len(linhas) - 1)
        else linha
        for indice, linha in enumerate(linhas)
    ]
