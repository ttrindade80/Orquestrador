"""Primitivas de texto físico e códigos ANSI."""



_ANSI_POR_NOME_SEMANTICO = {
    "padrão": "",
    "cinza": "\x1b[90m",
    "azul": "\x1b[34m",
    "amarelo": "\x1b[33m",
    "verde": "\x1b[32m",
}
_ANSI_RESET_FG = "\x1b[39m"
_ANSI_RESET_BG = "\x1b[49m"


def _codigo_ansi_de_cor(nome_semantico):
    """Devolve a sequencia SGR para ``nome_semantico``, ou ``\"\"`` se neutro.

    Nomes ausentes da paleta nao inventam cor (string vazia) — o renderer
    nao hardcoda ANSI ad-hoc fora desta tabela.
    """
    if not isinstance(nome_semantico, str):
        return ""
    return _ANSI_POR_NOME_SEMANTICO.get(nome_semantico, "")


def _tokens_ansi(texto):
    """Percorre ``texto`` em tokens ``('sgr', seq)`` ou ``('ch', char)``.

    Sequencias CSI incompletas (sem terminador alfabético) nao sao emitidas
    — nunca devolve CSI partido.
    """
    if not texto:
        return
    i = 0
    comprimento = len(texto)
    while i < comprimento:
        ch = texto[i]
        if ch == "\x1b" and i + 1 < comprimento and texto[i + 1] == "[":
            j = i + 2
            while j < comprimento:
                fim = texto[j]
                j += 1
                if "A" <= fim <= "Z" or "a" <= fim <= "z":
                    yield ("sgr", texto[i:j])
                    i = j
                    break
            else:
                break
            continue
        yield ("ch", ch)
        i += 1


def _estado_sgr_vazio():
    return {"fg": None, "bg": None}


def _atualizar_sgr(estado, sequencia):
    if not sequencia.endswith("m"):
        return
    interno = sequencia[2:-1]
    partes = interno.split(";") if interno else ["0"]
    for parte in partes:
        if parte == "":
            numero = 0
        else:
            try:
                numero = int(parte)
            except ValueError:
                continue
        if numero == 0:
            estado["fg"] = None
            estado["bg"] = None
        elif numero == 39:
            estado["fg"] = None
        elif numero == 49:
            estado["bg"] = None
        elif 30 <= numero <= 37 or 90 <= numero <= 97:
            estado["fg"] = numero
        elif 40 <= numero <= 47 or 100 <= numero <= 107:
            estado["bg"] = numero


def _prefixo_sgr(estado):
    partes = []
    if estado["fg"] is not None:
        partes.append("\x1b[{0}m".format(estado["fg"]))
    if estado["bg"] is not None:
        partes.append("\x1b[{0}m".format(estado["bg"]))
    return "".join(partes)


def _sufixo_sgr(estado):
    partes = []
    if estado["fg"] is not None:
        partes.append(_ANSI_RESET_FG)
    if estado["bg"] is not None:
        partes.append(_ANSI_RESET_BG)
    return "".join(partes)


def _largura_sem_ansi(texto):
    """Largura visual de ``texto`` ignorando sequencias SGR ``CSI ... m``."""
    if not texto:
        return 0
    n = 0
    for tipo, _valor in _tokens_ansi(texto):
        if tipo == "ch":
            n += 1
    return n


def _cortar_sem_ansi(texto, largura):
    """Corta ``texto`` para no maximo ``largura`` caracteres visiveis.

    Sequencias SGR sao preservadas integralmente; apenas caracteres
    visiveis entram na contagem do limite. CSI incompleto nao e emitido.
    Se o corte ocorrer com SGR ainda ativo, o estado e neutralizado com
    os resets canonicos de foreground e/ou background, sem alterar a
    largura visual.
    """
    if largura <= 0:
        return ""
    if not texto or _largura_sem_ansi(texto) <= largura:
        return texto
    out = []
    estado = _estado_sgr_vazio()
    n = 0
    for tipo, valor in _tokens_ansi(texto):
        if tipo == "sgr":
            out.append(valor)
            _atualizar_sgr(estado, valor)
            continue
        if n >= largura:
            break
        out.append(valor)
        n += 1
    return "".join(out) + _sufixo_sgr(estado)


def _ljust_sem_ansi(texto, largura):
    """Equivalente a ``str.ljust`` contando apenas caracteres visiveis."""
    pad = largura - _largura_sem_ansi(texto)
    if pad <= 0:
        return texto
    return texto + (" " * pad)


def _quebrar_sem_ansi(texto, largura):
    """Quebra ``texto`` em linhas de ate ``largura`` colunas visuais.

    Nao parte CSI. Cada linha fisica fecha SGR ativo; a seguinte reabre o
    estilo somente quando a regiao estilizada continua.
    """
    if largura is None or largura <= 0:
        return [texto] if texto else [""]
    if not texto:
        return [""]
    unidades = []
    pendente = ""
    estado_pendente = _estado_sgr_vazio()
    for tipo, valor in _tokens_ansi(texto):
        if tipo == "sgr":
            pendente += valor
            _atualizar_sgr(estado_pendente, valor)
            continue
        unidades.append((pendente, valor, dict(estado_pendente)))
        pendente = ""
    sgr_final = pendente
    if not unidades:
        return [texto]
    if len(unidades) <= largura:
        return [texto]

    linhas = []
    indice = 0
    estado_linha = _estado_sgr_vazio()
    while indice < len(unidades):
        restante = len(unidades) - indice
        if restante <= largura:
            partes = [_prefixo_sgr(estado_linha)]
            for sgr, ch, estado_ch in unidades[indice:]:
                partes.append(sgr)
                partes.append(ch)
                estado_linha = estado_ch
            partes.append(sgr_final)
            for tipo, valor in _tokens_ansi(sgr_final):
                if tipo == "sgr":
                    _atualizar_sgr(estado_linha, valor)
            partes.append(_sufixo_sgr(estado_linha))
            linhas.append("".join(partes))
            break
        corte = largura
        for posicao in range(largura - 1, -1, -1):
            if unidades[indice + posicao][1] == " ":
                corte = posicao
                break
        if corte <= 0:
            corte = largura
        partes = [_prefixo_sgr(estado_linha)]
        for sgr, ch, estado_ch in unidades[indice:indice + corte]:
            partes.append(sgr)
            partes.append(ch)
            estado_linha = estado_ch
        partes.append(_sufixo_sgr(estado_linha))
        linhas.append("".join(partes))
        indice += corte
        while indice < len(unidades) and unidades[indice][1] == " ":
            estado_linha = unidades[indice][2]
            indice += 1
    return [linha for linha in linhas if _largura_sem_ansi(linha)] or [""]
\n