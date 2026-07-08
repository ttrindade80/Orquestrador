"""Renderer visual com borda da tela raiz (H-0006 / H-0007 / H-0009).

Evolui o renderer estrutural (H-0005) para uma representacao visual
com tres caixas bordeadas: cabecalho (derivado do modelo), dashboard
(placeholder hardcoded) e menu (placeholder inerte hardcoded).

O H-0007 estende `renderizar_tela` com o parametro opcional
`tipo_borda`, permitindo alternar em memoria entre dois conjuntos de
caracteres de borda (`"curva"` e `"reta"`). A chamada padrao sem
`tipo_borda` produz exatamente a saida H-0006 (borda curva). Nao ha
persistencia, nao ha leitura de config, nao ha UI interativa, nao ha
captura de teclado.

O H-0009 estende `renderizar_tela` com o parametro opcional `largura`:
quando omitido (`None`), usa o fallback deterministico `TOTAL_WIDTH = 42`
(saida identica ao H-0006/H-0007); quando fornecido, ajusta a largura
visual das caixas. O H-0009 tambem remove a linha em branco entre
caixas/regioes visuais (separadores `"\n\n"` -> `"\n"`), sem alterar o
espacamento interno das caixas (conformidade com R-10 do contrato de
composicao fica fora de escopo deste ciclo).

Consome o ModeloTela produzido pelo pipeline H-0001 + H-0002
(`carregar_tela` -> `construir_modelo` -> `ModeloTela`) e gera uma
string visual deterministica, sem dependencia de terminal, sem
execucao de acao, sem ativacao de binding e sem consulta a JSON.

ESCOPO (H-0006 / H-0007):
- Apenas renderizacao visual com borda a partir de ModeloTela.
- Caixa de cabecalho derivada de modelo.cabecalho (titulo/descricao).
- Caixa de dashboard totalmente hardcoded (placeholder de teste).
- Caixa de menu totalmente hardcoded (texto inerte [Esc] Sair e [B] Borda).
- Alternancia de borda em memoria entre `"curva"` (default) e `"reta"`,
  definida como constante `_BORDAS` em nivel de modulo.
- Nao acessa config/telas/orquestrador.json diretamente.
- Nao chama carregar_tela nem construir_modelo.
- Nao importa json, os ou pathlib.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo.
- Nao calcula largura de terminal, nao paginar, nao selecionar.
- Nao acessa campos inertes internos de nenhum ElementoCorpo.
- Nao acessa modelo.corpo, modelo.barra_de_menus, modelo.id nem modelo.schema.
- [Esc] Sair e [B] Borda sao apenas texto inerte -- nenhum binding.
- Nao le config/estilo.json, config/barra_de_menus.json,
  config/layout_console.json nem config/lancador.json.
- Nao persiste tipo_borda entre chamadas.

A largura total e parametrizavel desde o H-0009: `renderizar_tela`
aceita `largura` opcional; quando omitida (`None`), usa o fallback
deterministico `TOTAL_WIDTH = 42` (heranca tecnica provisoria do
H-0006, sem carater normativo de layout). As constantes
`INNER_WIDTH`, `CONTENT_WIDTH` e `_LABEL_MAX` permanecem como
marcadores do fallback (42 -> 40/39/38) e nao sao regra normativa.

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela


class RenderizadorErro(Exception):
    """Erro de renderizacao visual de tela."""


TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38


_BORDAS = {
    "curva": {
        "tl": "╭", "tr": "╮",
        "bl": "╰", "br": "╯",
        "v":  "│", "h":  "─",
    },
    "reta": {
        "tl": "┌", "tr": "┐",
        "bl": "└", "br": "┘",
        "v":  "│", "h":  "─",
    },
}


def _linha_topo(label, borda, label_max):
    """Monta a borda superior com label.

    Formato: {tl} {LABEL} {h x (label_max-len(LABEL))}{tr}
    Comprimento total: label_max + 4 == total_w.
    """
    label_trunc = label[:label_max]
    dashes = label_max - len(label_trunc)
    return "{tl} {0} {1}{tr}".format(
        label_trunc, borda["h"] * dashes, tl=borda["tl"], tr=borda["tr"]
    )


def _linha_base(borda, inner_w):
    """Monta a borda inferior: {bl}{h x inner_w}{br}.

    Comprimento total: inner_w + 2 == total_w.
    """
    return "{bl}{0}{br}".format(
        borda["h"] * inner_w, bl=borda["bl"], br=borda["br"]
    )


def _linha_conteudo(texto, borda, content_w):
    """Monta uma linha de conteudo: {v} {text:<content_w}{v}.

    Comprimento total: content_w + 3 == total_w.
    """
    txt = texto[:content_w]
    pad = " " * (content_w - len(txt))
    return "{v} {0}{1}{v}".format(txt, pad, v=borda["v"])


def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max):
    """Monta uma caixa bordeada com label no topo e linhas de conteudo."""
    partes = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto, borda, content_w))
    partes.append(_linha_base(borda, inner_w))
    return "\n".join(partes)


def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None) -> str:
    """Renderiza ModeloTela como string visual com borda (H-0006/H-0007/H-0009).

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).
        tipo_borda: nome do conjunto de caracteres de borda a usar.
            Valores aceitos: ``"curva"`` (default, saida identica ao
            H-0006) e ``"reta"``. Outros valores lancam RenderizadorErro.
            A validacao e case-sensitive.
        largura: largura total (em caracteres Python) de cada linha
            nao-vazia da saida. Quando ``None`` (default), usa o fallback
            deterministico ``TOTAL_WIDTH = 42`` (comportamento identico
            ao H-0006/H-0007). Quando fornecida, deriva
            ``inner_w = largura - 2``, ``content_w = largura - 3`` e
            ``label_max = largura - 4``. ``largura < 10`` tem comportamento
            indefinido neste ciclo (nao validado, nao tratado).

    Retorna:
        str com a representacao visual no formato definido pelos
        handoffs H-0006 / H-0007 / H-0009 (tres caixas bordeadas
        consecutivas, sem linha em branco entre elas: cabecalho
        derivado do modelo, dashboard placeholder hardcoded, menu
        placeholder hardcoded inerte). Os caracteres de canto variam
        conforme ``tipo_borda``; o restante (bordas vertical/horizontal
        e conteudo textual) e identico entre conjuntos. Cada linha
        nao-vazia tem exatamente ``largura`` (ou 42 no fallback) chars
        Python; a string termina com ``"\\n"``.

    Lancamentos:
        RenderizadorErro quando:
            - o argumento ``modelo`` nao e um ModeloTela valido
              (ex.: None ou objeto de outro tipo);
            - o argumento ``tipo_borda`` nao e ``"curva"`` nem ``"reta"``.

    Efeitos colaterais:
        Nenhum. Nao altera o modelo, nao grava arquivo, nao consulta
        JSON em disco, nao executa acao, nao ativa binding, nao
        persiste tipo_borda entre chamadas, nao le o terminal.
    """
    if not isinstance(modelo, ModeloTela):
        raise RenderizadorErro(
            "renderizar_tela exige ModeloTela; recebido: {0}".format(
                type(modelo).__name__
            )
        )

    if tipo_borda not in _BORDAS:
        raise RenderizadorErro(
            "tipo_borda invalido: {0!r}; valores aceitos: curva, reta".format(
                tipo_borda
            )
        )

    total_w = TOTAL_WIDTH if largura is None else largura
    inner_w = total_w - 2
    content_w = total_w - 3
    label_max = total_w - 4
    borda = _BORDAS[tipo_borda]

    titulo = modelo.cabecalho.get("titulo", "(ausente)")
    descricao = modelo.cabecalho.get("descricao", "(ausente)")
    label_cabecalho = titulo.upper()

    caixa_cabecalho = _caixa(
        label_cabecalho, [descricao], borda, inner_w, content_w, label_max
    )
    caixa_dashboard = _caixa(
        "DASHBOARD",
        ["Dashboard de teste", "Sem dados carregados"],
        borda, inner_w, content_w, label_max,
    )
    caixa_menu = _caixa(
        "Menu", ["[Esc] Sair    [B] Borda"], borda, inner_w, content_w, label_max
    )

    return (
        caixa_cabecalho + "\n"
        + caixa_dashboard + "\n"
        + caixa_menu + "\n"
    )
