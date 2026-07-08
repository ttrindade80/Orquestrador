"""Renderer declarativo derivado do modelo/JSON (H-0006 / H-0007 / H-0009 / H-0010A).

O renderer interpreta o ModeloTela produzido pelo pipeline H-0001 + H-0002
(``carregar_tela`` -> ``construir_modelo`` -> ``ModeloTela``) e gera uma
string visual deterministica composta por caixas bordeadas. O H-0010A
substitui os placeholders hardcoded do H-0006 por conteudo derivado do
modelo/JSON:

- cabecalho: titulo/descricao lidos de ``modelo.cabecalho``.
- corpo.elementos[]: percorridos na ordem declarada no JSON. Cada elemento
  e renderizado como uma caixa:
  - ``console`` -> caixa com titulo do elemento e linha placeholder fixa
    ``"(console)"`` (unica excecao declarada de texto nao proveniente do
    JSON, como marcador explicito de escopo).
  - ``dashboard`` -> caixa com titulo do elemento; para cada campo em
    ``_campos_inertes["campos"]`` com ``fonte == "literal"`` inclui o
    ``valor`` como linha de conteudo; campos com outra ``fonte`` sao
    ignorados (sem texto, sem erro).
  - ``lancador`` -> caixa com titulo do elemento; para cada item em
    ``_campos_inertes["itens"]`` inclui a linha ``"[{chip}] {texto}"``.
    Itens com ``texto`` acima de 15 caracteres levantam ``RenderizadorErro``
    -- nunca truncar, nunca abreviar. Lista vazia produz caixa sem linhas
    de conteudo.
- barra_de_menus: caixa com label fixo ``"Menus"`` (rotulo visual apenas,
  sem comportamento derivado do label); para cada chip em
  ``modelo.barra_de_menus["chips"]`` inclui linha ``"[{tecla}] {texto}"``
  na ordem declarada. ``regra_existencia`` e ``regra_ativo`` nao sao
  avaliadas neste ciclo -- todos os chips declarados sao renderizados.

O renderer continua recebendo os parametros opcionais ``tipo_borda``
(``"curva"`` default ou ``"reta"``) e ``largura`` (quando ``None``,
fallback ``TOTAL_WIDTH = 42``). Quando ``largura`` e fornecida, deriva
``inner_w = largura - 2``, ``content_w = largura - 3`` e
``label_max = largura - 4``.

ESCOPO (H-0010A):
- Apenas renderizacao visual declarativa a partir de ModeloTela.
- Nenhum texto de item, chip, tecla, tela_destino, rotulo de menu ou
  valor de dashboard e hardcoded -- todos vem do modelo/JSON. A unica
  excecao e a linha placeholder ``"(console)"`` do elemento console,
  declarada explicitamente como marcador de escopo.
- O binding interno de borda da demo (``b``) deixa de aparecer na saida
  do renderer, pois nunca foi declarado no JSON; o comando permanece
  apenas como controle interno da demo.
- Nao acessa config/telas/*.json diretamente.
- Nao chama carregar_tela nem construir_modelo.
- Nao importa json, os, pathlib nem tela.loader.
- Nao executa acao, nao ativa binding, nao navega por tela_destino,
  nao aplica filtro, nao altera estado, nao grava arquivo.
- Nao calcula largura de terminal, nao paginar, nao selecionar.
- Nao avalia regra_existencia nem regra_ativo.
- Nao decide Sair/Voltar por id de tela -- o texto do chipEsc vem do JSON.

A largura total e parametrizavel desde o H-0009: ``renderizar_tela`` aceita
``largura`` opcional; quando omitida (``None``), usa o fallback
deterministico ``TOTAL_WIDTH = 42`` (heranca tecnica provisoria do
H-0006, sem carater normativo de layout).

Apenas biblioteca padrao do Python.
"""

from tela.modelo import ModeloTela


class RenderizadorErro(Exception):
    """Erro de renderizacao visual de tela."""


TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38

_TEXTO_ITEM_MAX = 15

_PLACEHOLDER_CONSOLE = "(console)"
_LABEL_BARRA = "Menus"


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


def _linhas_console(elemento):
    """Linhas de conteudo para elemento console (placeholder de escopo)."""
    return [_PLACEHOLDER_CONSOLE]


def _linhas_dashboard(elemento):
    """Linhas de conteudo para elemento dashboard a partir de campos[].

    Apenas campos com ``fonte == "literal"`` contribuem com o ``valor``
    como linha de conteudo. Campos com outra ``fonte`` (ex.: ``"pendente"``)
    sao ignorados -- sem texto, sem erro, sem placeholder.
    """
    campos = elemento._campos_inertes.get("campos", []) or []
    linhas = []
    for campo in campos:
        if not isinstance(campo, dict):
            continue
        if campo.get("fonte") == "literal":
            valor = campo.get("valor", "")
            linhas.append(valor)
    return linhas


def _linhas_lancador(elemento):
    """Linhas de conteudo para elemento lancador a partir de itens[].

    Cada item e renderizado como ``"[{chip}] {texto}"``. Itens com
    ``texto`` acima de ``_TEXTO_ITEM_MAX`` (15) caracteres levantam
    ``RenderizadorErro`` -- nunca truncar, nunca abreviar. Lista vazia
    produz caixa sem linhas de conteudo.
    """
    itens = elemento._campos_inertes.get("itens", []) or []
    linhas = []
    for item in itens:
        if not isinstance(item, dict):
            continue
        chip = item.get("chip", "")
        texto = item.get("texto", "")
        if len(texto) > _TEXTO_ITEM_MAX:
            raise RenderizadorErro(
                "texto de item de lancador acima do limite de {0} "
                "caracteres: {1!r} (id={2!r})".format(
                    _TEXTO_ITEM_MAX, texto, item.get("id")
                )
            )
        linhas.append("[{0}] {1}".format(chip, texto))
    return linhas


def _linhas_barra(barra_de_menus):
    """Linhas de conteudo para a caixa da barra de menus.

    Cada chip declarado em ``barra_de_menus["chips"]`` e renderizado como
    ``"[{tecla}] {texto}"`` em sua propria linha, na ordem declarada.
    ``regra_existencia`` e ``regra_ativo`` nao sao avaliadas -- todos os
    chips declarados sao renderizados.
    """
    if not isinstance(barra_de_menus, dict):
        return []
    chips = barra_de_menus.get("chips", []) or []
    linhas = []
    for chip in chips:
        if not isinstance(chip, dict):
            continue
        tecla = chip.get("tecla", "")
        texto = chip.get("texto", "")
        linhas.append("[{0}] {1}".format(tecla, texto))
    return linhas


def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None) -> str:
    """Renderiza ModeloTela como string visual declarativa (H-0010A).

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).
        tipo_borda: nome do conjunto de caracteres de borda a usar.
            Valores aceitos: ``"curva"`` (default) e ``"reta"``. Outros
            valores lancam RenderizadorErro (case-sensitive).
        largura: largura total (em caracteres Python) de cada linha
            nao-vazia da saida. Quando ``None`` (default), usa o fallback
            deterministico ``TOTAL_WIDTH = 42``. Quando fornecida, deriva
            ``inner_w = largura - 2``, ``content_w = largura - 3`` e
            ``label_max = largura - 4``. ``largura < 10`` tem comportamento
            indefinido neste ciclo (nao validado, nao tratado).

    Retorna:
        str com a representacao visual no formato definido pelo H-0010A:
        uma caixa de cabecalho derivada de ``modelo.cabecalho``, seguida
        de uma caixa por elemento de ``corpo.elementos[]`` (na ordem do
        JSON) e por fim uma caixa da ``barra_de_menus``. Os caracteres de
        canto variam conforme ``tipo_borda``; o restante (bordas
        vertical/horizontal e conteudo textual) e identico entre
        conjuntos. Cada linha nao-vazia tem exatamente ``largura`` (ou 42
        no fallback) chars Python; a string termina com ``"\\n"``.

    Lancamentos:
        RenderizadorErro quando:
            - o argumento ``modelo`` nao e um ModeloTela valido;
            - o argumento ``tipo_borda`` nao e ``"curva"`` nem ``"reta"``;
            - algum item de lancador possui ``texto`` acima de 15
              caracteres (rejeitado sem truncamento).

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

    partes = [
        _caixa(
            label_cabecalho, [descricao], borda, inner_w, content_w, label_max
        )
    ]

    for elemento in modelo.corpo.elementos:
        if elemento.tipo == "console":
            titulo_el = elemento._campos_inertes.get("titulo", "CONSOLE")
            partes.append(_caixa(
                titulo_el.upper(), _linhas_console(elemento),
                borda, inner_w, content_w, label_max,
            ))
        elif elemento.tipo == "dashboard":
            titulo_el = elemento._campos_inertes.get("titulo", "DASHBOARD")
            partes.append(_caixa(
                titulo_el.upper(), _linhas_dashboard(elemento),
                borda, inner_w, content_w, label_max,
            ))
        elif elemento.tipo == "lancador":
            titulo_el = elemento._campos_inertes.get("titulo", "LANCADOR")
            partes.append(_caixa(
                titulo_el.upper(), _linhas_lancador(elemento),
                borda, inner_w, content_w, label_max,
            ))

    partes.append(_caixa(
        _LABEL_BARRA, _linhas_barra(modelo.barra_de_menus),
        borda, inner_w, content_w, label_max,
    ))

    return "\n".join(partes) + "\n"
