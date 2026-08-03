"""Primitivas de texto físico e códigos ANSI."""



_ANSI_POR_NOME_SEMANTICO = {
    "padrão": "",
    "cinza": "\x1b[90m",
    "azul": "\x1b[34m",
    "amarelo": "\x1b[33m",
    "verde": "\x1b[32m",
}
_ANSI_RESET_FG = "\x1b[39m"


def _codigo_ansi_de_cor(nome_semantico):
    """Devolve a sequencia SGR para ``nome_semantico``, ou ``\"\"`` se neutro.

    Nomes ausentes da paleta nao inventam cor (string vazia) — o renderer
    nao hardcoda ANSI ad-hoc fora desta tabela.
    """
    if not isinstance(nome_semantico, str):
        return ""
    return _ANSI_POR_NOME_SEMANTICO.get(nome_semantico, "")


def _largura_sem_ansi(texto):
    """Largura visual de ``texto`` ignorando sequencias SGR ``CSI ... m``."""
    if not texto:
        return 0
    n = 0
    i = 0
    comprimento = len(texto)
    while i < comprimento:
        ch = texto[i]
        if ch == "\x1b" and i + 1 < comprimento and texto[i + 1] == "[":
            i += 2
            while i < comprimento:
                fim = texto[i]
                i += 1
                if "A" <= fim <= "Z" or "a" <= fim <= "z":
                    break
            continue
        n += 1
        i += 1
    return n


def _cortar_sem_ansi(texto, largura):
    """Corta ``texto`` para no maximo ``largura`` caracteres visiveis.

    Sequencias SGR sao preservadas integralmente; apenas caracteres
    visiveis entram na contagem do limite.
    """
    if largura <= 0:
        return ""
    if not texto or _largura_sem_ansi(texto) <= largura:
        return texto
    out = []
    n = 0
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
                    break
            out.append(texto[i:j])
            i = j
            continue
        if n >= largura:
            break
        out.append(ch)
        n += 1
        i += 1
    return "".join(out)


def _ljust_sem_ansi(texto, largura):
    """Equivalente a ``str.ljust`` contando apenas caracteres visiveis."""
    pad = largura - _largura_sem_ansi(texto)
    if pad <= 0:
        return texto
    return texto + (" " * pad)
