"""Primitivas de caixa e distribuição geométrica."""

from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.texto_ansi import _cortar_sem_ansi, _ljust_sem_ansi

TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38

_PLACEHOLDER_CONSOLE = "(console)"
_LABEL_BARRA = "Menus"

def _borda_de_estilo(estilo):
    """Materializa o dict interno de borda a partir de ``EstiloResolvido``.

    H-0039 / ADR-0030: os caracteres de borda deixam de ser hardcoded em
    ``_BORDAS`` e passam a derivar do estilo global resolvido. O dict usa as
    chaves internas consumidas pelas helpers de renderizacao (``tl``, ``tr``,
    ``bl``, ``br``, ``v``, ``h_superior``, ``h_inferior``). Os tracos superior
    e inferior sao distintos para suportar presets como ``"Linha"``, onde
    ``traco_superior`` difere de ``traco_inferior``.
    """
    return {
        "tl": estilo.canto_superior_esquerdo,
        "tr": estilo.canto_superior_direito,
        "bl": estilo.canto_inferior_esquerdo,
        "br": estilo.canto_inferior_direito,
        "v": estilo.lateral,
        "h_superior": estilo.traco_superior,
        "h_inferior": estilo.traco_inferior,
    }


def _capitalizar_inicio_de_frase(texto):
    """Capitaliza somente o primeiro caractere alfabético de ``texto``."""
    for indice, caractere in enumerate(texto):
        if caractere.isalpha():
            return texto[:indice] + caractere.upper() + texto[indice + 1:]
    return texto


def _capitalizar_cabecalho(texto, capitalizacao):
    if capitalizacao == "maiusculas":
        return texto.upper()
    if capitalizacao == "inicio_de_frase":
        return _capitalizar_inicio_de_frase(texto)
    if capitalizacao == "preservar":
        return texto
    raise RenderizadorErro(
        "capitalizacao de cabecalho desconhecida: {0!r}".format(
            capitalizacao
        )
    )


def _linha_topo(label, borda, label_max, apresentacao=None):
    """Monta a borda superior com label.

    Formato: {tl} {LABEL} {h x (label_max-len(LABEL))}{tr}
    Comprimento total: label_max + 4 == total_w.
    """
    if apresentacao is not None:
        configuracao = apresentacao["titulo"]
        titulo = _capitalizar_cabecalho(
            label, configuracao["capitalizacao"]
        )
        if configuracao["formato_na_borda"] != "com_espacos_laterais":
            raise RenderizadorErro(
                "formato_na_borda de cabecalho nao suportado: {0!r}".format(
                    configuracao["formato_na_borda"]
                )
            )

        largura_interna = label_max + 2
        posicao = configuracao["posicao"]
        recuo = configuracao["recuo_lateral"]
        if largura_interna < 2:
            raise RenderizadorErro(
                "geometria impossivel para bloco do titulo do cabecalho"
            )
        if posicao == "centro":
            limite_titulo = largura_interna - 2
            titulo = titulo[:limite_titulo]
            bloco = " " + titulo + " "
            espaco = largura_interna - len(bloco)
            esquerda = espaco // 2
            direita = espaco - esquerda
        else:
            limite_titulo = largura_interna - recuo - 2
            if limite_titulo < 0:
                raise RenderizadorErro(
                    "geometria impossivel para recuo_lateral do cabecalho"
                )
            titulo = titulo[:limite_titulo]
            bloco = " " + titulo + " "
            if posicao == "esquerda":
                esquerda = recuo
                direita = largura_interna - len(bloco) - esquerda
            elif posicao == "direita":
                direita = recuo
                esquerda = largura_interna - len(bloco) - direita
            else:
                raise RenderizadorErro(
                    "posicao de titulo de cabecalho desconhecida: {0!r}".format(
                        posicao
                    )
                )
        return "{tl}{0}{1}{2}{tr}".format(
            borda["h_superior"] * esquerda,
            bloco,
            borda["h_superior"] * direita,
            tl=borda["tl"],
            tr=borda["tr"],
        )

    label_trunc = label[:label_max]
    dashes = label_max - len(label_trunc)
    return "{tl} {0} {1}{tr}".format(
        label_trunc, borda["h_superior"] * dashes, tl=borda["tl"], tr=borda["tr"]
    )


def _linha_base(borda, inner_w, texto_direita=None):
    """Monta a borda inferior: {bl}{h x inner_w}{br}.

    Comprimento total: inner_w + 2 == total_w.
    """
    miolo = borda["h_inferior"] * inner_w
    if texto_direita:
        marcador = " {0} ".format(texto_direita)
        if len(marcador) <= inner_w:
            inicio = inner_w - len(marcador)
            miolo = miolo[:inicio] + marcador
    return "{bl}{0}{br}".format(miolo, bl=borda["bl"], br=borda["br"])


def _linha_conteudo(texto, borda, content_w, apresentacao=None):
    """Monta uma linha de conteudo: {v} {text:<content_w}{v}.

    Comprimento total VISUAL: content_w + 3 == total_w.
    Truncamento e preenchimento ignoram sequencias SGR ANSI (chips com
    ``cor_inativo``/destaque nao deslocam a borda direita nem encurtam
    a moldura — H-0045-P02 / VM-H0045-R02-002).
    """
    if apresentacao is not None:
        configuracao = apresentacao["descricao"]
        texto = texto[:configuracao["max_caracteres"]]
        texto = _capitalizar_cabecalho(
            texto, configuracao["capitalizacao"]
        )
        largura_interna = content_w + 1
        alinhamento = configuracao["alinhamento"]
        recuo = configuracao["recuo"]

        if alinhamento == "centro":
            texto = _cortar_sem_ansi(texto, largura_interna)
            espaco = largura_interna - len(texto)
            esquerda = espaco // 2
            direita = espaco - esquerda
        else:
            limite_texto = largura_interna - recuo
            if limite_texto < 0:
                raise RenderizadorErro(
                    "geometria impossivel para recuo da descricao do cabecalho"
                )
            texto = _cortar_sem_ansi(texto, limite_texto)
            if alinhamento == "esquerda":
                esquerda = recuo
                direita = largura_interna - esquerda - len(texto)
            elif alinhamento == "direita":
                direita = recuo
                esquerda = largura_interna - direita - len(texto)
            else:
                raise RenderizadorErro(
                    "alinhamento de descricao de cabecalho desconhecido: {0!r}".format(
                        alinhamento
                    )
                )
        miolo = " " * esquerda + texto + " " * direita
        return "{v}{0}{v}".format(miolo, v=borda["v"])

    txt = _cortar_sem_ansi(texto, content_w)
    miolo = _ljust_sem_ansi(txt, content_w)
    return "{v} {0}{v}".format(miolo, v=borda["v"])


def _caixa(
    label,
    linhas_conteudo,
    borda,
    inner_w,
    content_w,
    label_max,
    altura_alvo=None,
    texto_base=None,
    apresentacao=None,
):
    """Monta uma caixa bordeada com label no topo e linhas de conteudo.

    Quando altura_alvo e fornecida, a caixa ocupa exatamente essa altura:
    linhas de fill bordeadas (borda["v"] + " " * inner_w + borda["v"]) sao
    inseridas entre o conteudo e a base ate que a caixa tenha altura_alvo linhas.
    Quando None, comportamento atual preservado (topo + conteudo + base).
    """
    partes = [_linha_topo(label, borda, label_max, apresentacao=apresentacao)]
    for texto in linhas_conteudo:
        partes.append(
            _linha_conteudo(
                texto, borda, content_w, apresentacao=apresentacao
            )
        )
    if altura_alvo is not None:
        linha_fill = borda["v"] + " " * inner_w + borda["v"]
        while len(partes) < altura_alvo - 1:
            partes.append(linha_fill)
    partes.append(_linha_base(borda, inner_w, texto_direita=texto_base))
    return "\n".join(partes)


def _contar_linhas(caixa_str):
    """Conta o numero de linhas de um bloco multi-linha sem trailing newline.

    Uma caixa gerada por ``_caixa`` (ou um bloco de preenchimento) e uma
    string contendo ``N`` linhas separadas por ``"\\n"``, sem ``"\\n"`` final.
    Portanto o numero de linhas e ``caixa_str.count("\\n") + 1``.
    Usado pela ocupacao vertical (H-0015) para calcular ``L_cab``,
    ``L_corpo_conteudo`` e ``L_barra``.
    """
    return caixa_str.count("\n") + 1


def _pesos_distribuicao(distribuicao, n_filhos):
    """Devolve a lista de pesos positivos a partir da declaracao de distribuicao.

    - ``igual``: pesos equivalentes (``[1] * n_filhos``) — ADR-0018 D5.
    - ``percentual``/``fracao``: os proprios valores declarados, associados
      posicionalmente a ordem declarada dos filhos — ADR-0018 D6/D7.

    O algoritmo e generico: nenhum vetor concreto e hardcoded. O dict ja
    validado pelo loader e usado como-esta, sem substituir seus valores.
    """
    modo = distribuicao.get("modo")
    if modo == "igual":
        return [1] * n_filhos
    return list(distribuicao.get("valores", []))


def _distribuir_alturas(altura_disponivel, pesos):
    """Reparte ``altura_disponivel`` entre os pesos pelo metodo dos maiores
    restos (ADR-0015 secao 5.8; ADR-0018 D6/D7).

    Invariantes:
    - ``sum(cotas) == altura_disponivel`` (soma exata);
    - cada cota e inteira nao negativa;
    - empates de resto fracionario sao resolvidos pela ORDEM DECLARADA
      (menor indice prevalece).

    Algoritmo:
    1. cota ideal real de cada filho = ``altura_disponivel * peso / soma``;
    2. parte inteira (floor) de cada cota;
    3. ``faltam = altura_disponivel - sum(partes_inteiras)``;
    4. ordenar filhos por resto fracionario decrescente, desempatando por
       indice crescente (ordem declarada);
    5. atribuir uma unidade aos ``faltam`` maiores restos.
    """
    n = len(pesos)
    if n == 0:
        return []
    soma = float(sum(pesos))
    if soma <= 0:
        raise RenderizadorErro(
            "distribuicao: soma de pesos nao e positiva: {0}".format(soma)
        )
    ideais = [altura_disponivel * p / soma for p in pesos]
    cotas = [int(x) for x in ideais]  # floor (valores >= 0)
    faltam = altura_disponivel - sum(cotas)
    restos = sorted(
        range(n),
        key=lambda i: (-ideais[i] + int(ideais[i]), i),
    )
    for k in range(faltam):
        cotas[restos[k]] += 1
    return cotas


def _distribuir_larguras(largura_disponivel, pesos):
    """Reparte ``largura_disponivel`` entre os pesos pelo metodo dos maiores
    restos no eixo horizontal (H-0026 / ADR-0015 D5-D8; ADR-0018 D6/D7).

    Analogico a ``_distribuir_alturas``: o algoritmo de maiores restos e
    identico para qualquer eixo. Esta e uma rotina LOCAL ao calculo de cotas
    horizontais, independente do helper vertical, para preservar sem risco o
    comportamento aprovado pelo H-0025.

    Invariantes:
    - ``sum(cotas) == largura_disponivel`` (soma exata);
    - cada cota e inteira nao negativa;
    - empates de resto fracionario sao resolvidos pela ORDEM DECLARADA
      (menor indice prevalece).
    """
    n = len(pesos)
    if n == 0:
        return []
    soma = float(sum(pesos))
    if soma <= 0:
        raise RenderizadorErro(
            "distribuicao: soma de pesos nao e positiva: {0}".format(soma)
        )
    ideais = [largura_disponivel * p / soma for p in pesos]
    cotas = [int(x) for x in ideais]  # floor (valores >= 0)
    faltam = largura_disponivel - sum(cotas)
    restos = sorted(
        range(n),
        key=lambda i: (-ideais[i] + int(ideais[i]), i),
    )
    for k in range(faltam):
        cotas[restos[k]] += 1
    return cotas
