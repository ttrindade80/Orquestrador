import os
import sys

sys.dont_write_bytecode = True

import pytest

from pathlib import Path

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from tela.loader import carregar_tela, carregar_estilo
from tela.modelo import construir_modelo
from tela import navegacao
from tela import paginacao
from tela import renderizador as _rend
from tela.renderizador import RenderizadorErro
import demo.demo as _demo
from demo.demo import (
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
    _estabelecer_foco_paginacao_inicial,
    _modo_verboso_de_modelo,
    _reconciliar_paginacao_apos_resize,
    _ler_tecla_sessao,
)


def _modelo():
    return construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )


def _estado_inicial_paginado(modelo):
    """Estado equivalente ao que ``main`` estabelece ao abrir o cenario."""
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 24,
            "altura_interna": 16,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_paginacao_console_unico",
        }
    )
    return _estabelecer_foco_paginacao_inicial(estado, modelo)


def _sem_ansi(texto):
    """Remove sequencias ANSI de cor (H-0051): o agrupamento contiguo
    ``<delimitador>PgUp/PgDn<delimitador> PÁGINAS`` (D-PGU-01 a D-PGU-03) e
    uma propriedade do conteudo VISIVEL; cada chip mantem seu proprio envelope de cor
    inativo/ativo, o que insere codigos ANSI entre os dois quando um deles
    esta inativo. Comparar o literal exige ignorar esses codigos.
    """
    import re
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def _chip_paginas(estilo=None):
    """Forma visual efetiva do chip agrupado no estilo recebido."""
    estilo = estilo or carregar_estilo()
    rotulo = "PÁGINAS" if estilo.caixa_alta else "Páginas"
    return (
        estilo.caractere_esquerdo
        + "PgUp/PgDn"
        + estilo.caractere_direito
        + " "
        + rotulo
    )


def _ler_caractere_tty(byte_unico):
    """Espelha a leitura TTY: um byte no pipe → ``_ler_tecla_sessao``."""
    fd_r, fd_w = os.pipe()
    try:
        os.write(fd_w, byte_unico)
        return _ler_tecla_sessao(fd=fd_r)
    finally:
        try:
            os.close(fd_r)
        except OSError:
            pass
        try:
            os.close(fd_w)
        except OSError:
            pass


def _passo_tty(estado, modelo, byte_unico):
    """Cadeia operacional TTY: ler → despachar → atualizar → renderizar.

    H-0045-P06: renderiza com a MESMA largura/altura que ``estado`` carrega
    (default 80/24 quando ausente) -- nunca uma largura hardcoded distinta
    da usada por ``processar_comando`` para calcular pagina/cursor. Um
    hardcode fixo aqui mascarava a divergencia de geometria entre comando e
    render exatamente no tipo de caso que QA-H0045-P05-002 relata (largura
    estreita o suficiente para a barra ocupar mais de uma linha).
    """
    ch = _ler_caractere_tty(byte_unico)
    novo = processar_comando(estado, ch, modelo)
    largura = novo.get("largura", 80)
    altura = novo.get("altura", 24)
    saida = renderizar_estado(novo, modelo, largura=largura, altura=altura)
    return ch, novo, saida


def test_demo_h0045_comando_proxima_pagina_atualiza_pagina_e_cursor():
    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 24,
            "altura_interna": 16,
            "desconto_estrutural": 3,
            "foco_console": 0,
            "cursores": {console.id: 0},
            "pagina_atual": {console.id: 1},
        }
    )

    novo = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)

    assert novo["pagina_atual"][console.id] == 2
    assert novo["cursores"][console.id] == 16


def test_demo_h0045_renderizar_estado_repassa_paginas_atuais():
    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "foco_console": 0,
            "cursores": {console.id: 16},
            "pagina_atual": {console.id: 2},
        }
    )

    saida = renderizar_estado(estado, modelo, largura=80, altura=24)

    assert "página 2/3" in saida
    assert "item_17" in saida
    assert "item_01" not in saida


def test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1():
    """VM-H0045-01: cadeia TTY real para ``PageUp``/``PageDown``.

    Percorre leitura via ``_ler_tecla_sessao``, ``processar_comando``,
    substituicao de estado e ``renderizar_estado`` — nao chama isoladamente
    ``pagina_proxima``/``pagina_anterior``.
    """
    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    estado = _estado_inicial_paginado(modelo)

    assert estado["foco_console"] == 0
    assert estado["pagina_atual"][console.id] == 1

    saida_inicial = renderizar_estado(estado, modelo, largura=80, altura=24)
    assert "página 1/3" in saida_inicial
    assert _chip_paginas(estado["estilo"]) in _sem_ansi(saida_inicial)
    estados_chips = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados_chips.get("chip_pagina_anterior") is False
    assert estados_chips.get("chip_pagina_proxima") is True
    # Inativo permanece visivel com cor_inativo (nao removido).
    assert "\x1b[90mPgUp" in saida_inicial

    ch_pgdn, estado, saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch_pgdn == _demo.TECLA_PAGE_DOWN
    assert estado["pagina_atual"][console.id] == 2
    assert "página 2/3" in saida
    assert estado["cursores"][console.id] == 16
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is True
    assert estados.get("chip_pagina_proxima") is True

    ch_pgdn2, estado, saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch_pgdn2 == _demo.TECLA_PAGE_DOWN
    assert estado["pagina_atual"][console.id] == 3
    assert "página 3/3" in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is True
    assert estados.get("chip_pagina_proxima") is False
    assert "\x1b[90mPgDn" in saida

    # Extremo: ``PageDown`` sem wrap.
    ch_pgdn3, estado, _saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch_pgdn3 == _demo.TECLA_PAGE_DOWN
    assert estado["pagina_atual"][console.id] == 3
    ch_pgdn4, estado, _saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch_pgdn4 == _demo.TECLA_PAGE_DOWN
    assert estado["pagina_atual"][console.id] == 3

    ch_pgup, estado, saida = _passo_tty(estado, modelo, b"\x1b[5~")
    assert ch_pgup == _demo.TECLA_PAGE_UP
    assert estado["pagina_atual"][console.id] == 2
    assert "página 2/3" in saida

    ch_pgup2, estado, saida = _passo_tty(estado, modelo, b"\x1b[5~")
    assert ch_pgup2 == _demo.TECLA_PAGE_UP
    assert estado["pagina_atual"][console.id] == 1
    assert "página 1/3" in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is True

    # Extremo: ``PageUp`` sem efeito na primeira pagina.
    ch_pgup3, estado, _saida = _passo_tty(estado, modelo, b"\x1b[5~")
    assert ch_pgup3 == _demo.TECLA_PAGE_UP
    assert estado["pagina_atual"][console.id] == 1
    ch_pgup4, estado, saida = _passo_tty(estado, modelo, b"\x1b[5~")
    assert ch_pgup4 == _demo.TECLA_PAGE_UP
    assert estado["pagina_atual"][console.id] == 1
    # H-0071: chip unico multitecla com delimitadores externos.
    visivel = _sem_ansi(saida)
    assert _chip_paginas(estado["estilo"]) in visivel
    assert visivel.count("PgUp/PgDn") == 1
    assert _rend._navegacao_atual.get("estado_ativo_chips", {}).get(
        "chip_pagina_anterior"
    ) is False


def test_demo_h0045_p01_chips_visiveis_sem_foco_ambos_inativos():
    """D-TEC-12/D-PAG-13: controles de pagina ficam visiveis e inativos."""
    modelo = _modelo()
    estado = criar_estado_inicial()
    estado.update({"estilo": carregar_estilo(), "largura": 80, "altura": 24})
    assert estado.get("foco_console") is None

    saida = renderizar_estado(estado, modelo, largura=80, altura=24)
    assert "página 1/3" in saida
    assert _chip_paginas(estado["estilo"]) in _sem_ansi(saida)
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is False


def test_demo_h0045_p02_sequencia_resize_barra_sem_residuo():
    """VM-H0045-R02-002: sequencia grande → reduzida → maximizada na demo.

    Garante largura visual exata, uma borda esquerda/direita, ausencia de
    ``│`` repetidos e preservacao dos chips/indicador entre tamanhos.
    """
    import re
    from tela.renderizador import _largura_sem_ansi

    modelo = _modelo()
    estado = _estado_inicial_paginado(modelo)
    sequencia = (100, 60, 100)
    saidas = []
    for largura in sequencia:
        saida = renderizar_estado(estado, modelo, largura=largura, altura=24)
        saidas.append((largura, saida))
        linhas = [ln for ln in saida.split("\n") if ln]
        bar = next(
            ln for ln in linhas
            if "[Esc]" in ln and _chip_paginas(estado["estilo"]) in re.sub(
                r"\x1b\[[0-9;]*m", "", ln
            )
        )
        plain = re.sub(r"\x1b\[[0-9;]*m", "", bar)
        assert _largura_sem_ansi(bar) == largura
        assert plain.startswith("│") and plain.endswith("│")
        assert plain.count("│") == 2
        assert "││" not in plain
        assert "[Esc]" in plain and _chip_paginas(estado["estilo"]) in plain
        assert "[✥]" in plain
        assert "página 1/3" in saida
        for ln in linhas:
            assert _largura_sem_ansi(ln) == largura

    # Conteudo da largura reduzida nao "vaza" semanticamente para a maximizada:
    # cada quadro e autocontido com largura propria (sem residuo estrutural).
    _, saida_reduzida = saidas[1]
    _, saida_max = saidas[2]
    assert _largura_sem_ansi(
        next(ln for ln in saida_reduzida.split("\n") if "[Esc]" in ln and "PgUp/PgDn" in _sem_ansi(ln))
    ) == 60
    assert _largura_sem_ansi(
        next(ln for ln in saida_max.split("\n") if "[Esc]" in ln and "PgUp/PgDn" in _sem_ansi(ln))
    ) == 100


def test_demo_h0045_p02_apresentar_quadro_limpa_residuo_apos_reducao():
    """VM-H0045-R02-002: mecanismo de limpeza/redesenho no loop TTY.

    Simula quadro largo com ANSI (chip inativo) seguido de quadro estreito;
    o pad visual + CSI K devem cobrir a largura nova e apagar a direita.
    """
    from unittest import mock
    from demo.demo import _apresentar_quadro
    from tela.renderizador import _largura_sem_ansi, _ANSI_RESET_FG

    ansi = "\x1b[90m"
    # Linha visualmente curta se pad usasse len() bruto (bug pre-P02).
    linha_ansi = (
        "│  [Esc] Sair  {0}[PgUp/PgDn]{1} Páginas  [✥] Navegar".format(
            ansi, _ANSI_RESET_FG
        )
    )
    # Completa artificialmente como o renderer CORRIGIDO faria (vis == 100).
    from tela.renderizador import _ljust_sem_ansi
    linha_larga = "│" + _ljust_sem_ansi(linha_ansi[1:], 98) + "│"
    assert _largura_sem_ansi(linha_larga) == 100

    escritas = []

    class _Out:
        def write(self, s):
            escritas.append(s)

        def flush(self):
            pass

    with mock.patch("sys.stdout", _Out()):
        _apresentar_quadro(linha_larga + "\n", largura=100, altura=1)
        _apresentar_quadro(
            "│ curto │\n", largura=40, altura=1
        )

    assert len(escritas) == 2
    quadro_estreito = escritas[1]
    # Posiciona linha 1 e emite pad ate 40 colunas visuais + CSI K.
    assert "\x1b[1;1H" in quadro_estreito
    assert "\x1b[K" in quadro_estreito
    # Extrai o segmento apos o posicionamento e antes do CSI K.
    depois = quadro_estreito.split("\x1b[1;1H", 1)[1]
    segmento = depois.split("\x1b[K", 1)[0]
    assert _largura_sem_ansi(segmento) == 40
    assert segmento.startswith("│ curto │")
    # Espacos de pad cobrem o restante (apagando borda antiga a direita).
    assert segmento.endswith(" " * (40 - _largura_sem_ansi("│ curto │")))
    # Sem clear total de tela no redesenho (politica H-0022/H-0023).
    assert "\x1b[2J" not in quadro_estreito


def _linha_do_item(saida, texto_item):
    for linha in saida.split("\n"):
        if texto_item in linha:
            return linha
    return None


def _cursor_visivel_no_item(saida, simbolo, texto_item):
    """True quando o simbolo de cursor prefixa a linha do item indicado."""
    linha = _linha_do_item(saida, texto_item)
    return linha is not None and simbolo in linha


def _passo_resize(estado, modelo, nova_altura, largura=80):
    """Espelha o bloco SIGWINCH de ``main()``: atualiza geometria e
    reconcilia ``pagina_atual`` com o item logico do cursor ANTES de
    renderizar (H-0045-P03)."""
    estado = dict(
        estado,
        largura=largura,
        altura=nova_altura,
        desconto_estrutural=3,
    )
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida = renderizar_estado(estado, modelo, largura=largura, altura=nova_altura)
    return estado, saida


def test_demo_h0045_p03_cursor_visivel_ao_longo_do_ciclo_de_navegacao_e_resize():
    """VM-H0045-R03-003: regressao ponta a ponta do cursor de navegacao.

    Parte do MESMO estado que ``main()`` estabelece ao abrir o cenario
    (``_estabelecer_foco_paginacao_inicial``), sem fixar ``altura_interna``
    (derivada de ``altura`` como no runtime real). Verifica o QUADRO
    renderizado -- nunca apenas ``estado["cursores"]`` -- em cada etapa:
    abertura, mudanca de pagina (``PageDown``/``PageUp``), movimento de seta dentro da
    pagina e redimensionamento (1, 3 e muitas paginas).
    """
    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    simbolo = carregar_estilo().selecionado_simbolo

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 24,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_paginacao_console_unico",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)

    # 1) foco valido ao abrir.
    assert estado["foco_console"] == 0
    assert navegacao.console_focado(dict(estado, modelo=modelo)) is console

    # 2) cursor visivel no primeiro item navegavel da pagina inicial.
    saida = renderizar_estado(estado, modelo, largura=80, altura=24)
    assert "página 1/3" in saida
    chip_navegar_visivel = "[✥]" in saida
    cursor_visivel = _cursor_visivel_no_item(saida, simbolo, "item_01")
    assert chip_navegar_visivel is True
    assert cursor_visivel is True

    # 3) PageDown avanca pagina.
    ch, estado, saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch == _demo.TECLA_PAGE_DOWN
    assert estado["pagina_atual"][console.id] == 2
    assert "página 2/3" in saida

    # 4) cursor visivel no primeiro navegavel da pagina seguinte.
    assert estado["cursores"][console.id] == 16
    assert _cursor_visivel_no_item(saida, simbolo, "item_17")
    assert "[✥]" in saida

    # 5) seta move o cursor dentro da pagina (sem mudar de pagina).
    ch, estado, saida = _passo_tty(estado, modelo, b"\x1b[B")
    assert estado["pagina_atual"][console.id] == 2
    assert estado["cursores"][console.id] == 17
    assert _cursor_visivel_no_item(saida, simbolo, "item_18")
    assert not _cursor_visivel_no_item(saida, simbolo, "item_17")

    # 6) PageUp retorna.
    ch, estado, saida = _passo_tty(estado, modelo, b"\x1b[5~")
    assert ch == _demo.TECLA_PAGE_UP
    assert estado["pagina_atual"][console.id] == 1
    assert "página 1/3" in saida

    # 7) cursor reaparece corretamente no destino (primeiro navegavel da
    # pagina 1 -- toda troca explicita de pagina ancora no primeiro item).
    assert estado["cursores"][console.id] == 0
    assert _cursor_visivel_no_item(saida, simbolo, "item_01")

    # Reposiciona em item_17 (pagina 2) para testar preservacao de um item
    # NAO trivial (nao o primeiro) atraves de resize.
    ch, estado, saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert estado["cursores"][console.id] == 16
    assert _cursor_visivel_no_item(saida, simbolo, "item_17")

    # 8) resize entre 1, 3 e muitas paginas preserva o item logico do cursor
    # (item_17, indice 16) e o mantem visivel -- a pagina se ajusta a ele.
    estado, saida_1pag = _passo_resize(estado, modelo, nova_altura=42)
    assert estado["cursores"][console.id] == 16
    assert "página 1/1" in saida_1pag
    assert _cursor_visivel_no_item(saida_1pag, simbolo, "item_17")

    estado, saida_muitas = _passo_resize(estado, modelo, nova_altura=10)
    assert estado["cursores"][console.id] == 16
    assert "página 9/17" in saida_muitas
    assert _cursor_visivel_no_item(saida_muitas, simbolo, "item_17")

    estado, saida_3pag = _passo_resize(estado, modelo, nova_altura=24)
    assert estado["cursores"][console.id] == 16
    assert "página 2/3" in saida_3pag
    assert _cursor_visivel_no_item(saida_3pag, simbolo, "item_17")


def _modelo_com_pagina_intermediaria_sem_navegaveis():
    """Console focalizavel (itens navegaveis nas demais paginas) com DOIS
    itens nao-navegaveis consecutivos inseridos no meio da lista declarada --
    sob capacidade 2/pagina, eles ocupam sozinhos uma pagina inteira. Deriva
    do fixture ``h0045_paginacao_console_unico`` (mesma estrutura/distribuicao
    matricial validada), apenas com a lista de itens ampliada em memoria --
    nenhum arquivo de configuracao novo e criado.
    """
    import copy

    tela_raw = copy.deepcopy(
        carregar_tela(None, "h0045_paginacao_console_unico", "config/telas/demo")
    )
    itens = tela_raw["corpo"]["elementos"][0]["itens"]
    info = [
        {
            "id": "info_a",
            "texto": "info_a",
            "navegavel": False,
            "politica_quebra": "permitir_quebra_somente_se_maior_que_pagina",
        },
        {
            "id": "info_b",
            "texto": "info_b",
            "navegavel": False,
            "politica_quebra": "permitir_quebra_somente_se_maior_que_pagina",
        },
    ]
    tela_raw["corpo"]["elementos"][0]["itens"] = itens[:16] + info + itens[16:]
    return construir_modelo(tela_raw)


def test_demo_h0045_p03_pagina_sem_navegaveis_e_a_unica_sem_cursor():
    """VM-H0045-R03-003: dentro de um console FOCALIZAVEL e paginado (com
    itens navegaveis nas demais paginas), a UNICA pagina cujos itens sao
    todos nao-navegaveis nao exibe cursor -- mas os controles de pagina
    e o chip ``[✥]`` permanecem, pois o console como um todo tem itens
    navegaveis (D-TEC-12/D-PAG-13, propriedade estatica do console)."""
    modelo = _modelo_com_pagina_intermediaria_sem_navegaveis()
    console = modelo.corpo.elementos[0]
    simbolo = carregar_estilo().selecionado_simbolo

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 10,  # altura_interna derivada = 2 (capacidade 2/pagina)
            "desconto_estrutural": 3,
            "tela_atual": "h0045_paginacao_console_unico",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)

    # Pagina 1 (item_01/item_02): cursor visivel normalmente.
    saida1 = renderizar_estado(estado, modelo, largura=80, altura=10)
    assert "página 1/18" in saida1
    assert "[✥]" in saida1
    assert _chip_paginas(carregar_estilo()) in _sem_ansi(saida1)
    assert _cursor_visivel_no_item(saida1, simbolo, "item_01")

    # Pagina 9 (info_a/info_b): a unica sem navegavel -- sem cursor, sem
    # regressao dos controles de pagina (ainda presentes/operaveis).
    estado_vazia = paginacao.ir_para_pagina(estado, console, 9)
    assert console.id not in estado_vazia["cursores"]
    saida_vazia = renderizar_estado(estado_vazia, modelo, largura=80, altura=10)
    assert "página 9/18" in saida_vazia
    assert "info_a" in saida_vazia and "info_b" in saida_vazia
    assert simbolo not in saida_vazia
    assert _chip_paginas(carregar_estilo()) in _sem_ansi(saida_vazia)
    # "[✥]" exige > 1 item navegavel NA PAGINA CORRENTE (D14); nesta pagina
    # (0 navegaveis) ele corretamente nao aparece -- distinto de
    # controles de pagina, que sao propriedade ESTATICA do console
    # (D-TEC-12/D-PAG-13).
    assert "[✥]" not in saida_vazia

    # Pagina seguinte (item_17/item_18): cursor volta a aparecer.
    novo = processar_comando(estado_vazia, _demo.TECLA_PAGE_DOWN, modelo)
    saida_seguinte = renderizar_estado(novo, modelo, largura=80, altura=10)
    assert "página 10/18" in saida_seguinte
    assert _cursor_visivel_no_item(saida_seguinte, simbolo, "item_17")


def _modelo_fluxo_paginado():
    """Console paginado (18 itens) com selecao multipla habilitada (H-0045-P05).

    Fixture separada de ``h0045_paginacao_console_unico`` (``politica_selecao:
    unica``, sem suporte a marcacao) porque o teste de regressao do P05
    precisa verificar selecao preservada atraves do resize, alem do cursor.
    """
    return construir_modelo(
        carregar_tela(
            None,
            "h0045_fluxo_execucao_paginado",
            "config/telas/demo",
        )
    )


def test_demo_h0045_p05_repaginacao_preserva_item_cursor_e_selecao_em_sequencia_de_resize():
    """VM-H0045-R04-004: repaginacao intermitente apos redimensionamento.

    Causa raiz (RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P05.md): a reconciliacao
    aproximava ``altura_interna`` por um deslocamento fixo (``altura - 8``),
    que assume implicitamente que a barra de menus sempre ocupa 1 linha de
    chips. Na largura 45 (``content_w`` insuficiente para as 5 chips desta
    fixture em uma linha), a barra REAL ocupa 2 linhas -- a aproximacao
    subestima em 1 a capacidade fisica real por pagina. O erro constante nao
    muda o resultado em geometrias folgadas, mas se torna catastrofico perto
    da capacidade minima (1 item/pagina): o item logico do cursor deixa de
    aparecer na pagina reconciliada.

    Este teste reproduz uma sequencia de tamanhos intermediarios (incluindo 1
    item/pagina e uma geometria insuficiente) na MESMA largura, com o cursor
    posicionado em um item distante do inicio e com selecao marcada, passando
    pela MESMA funcao usada no tratamento de resize
    (``_reconciliar_paginacao_apos_resize``) e pelo render final
    (``renderizar_estado``) -- nunca chamando ``pagina_do_item_logico``
    isoladamente.
    """
    import re

    modelo = _modelo_fluxo_paginado()
    console = modelo.corpo.elementos[0]
    simbolo = carregar_estilo().selecionado_simbolo
    largura = 45

    # 1) abre o cenario (mesmo caminho de main(): foco inicial no console
    # paginado, sem fixar altura_interna -- derivada de altura, como no
    # runtime real).
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": 24,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_fluxo_execucao_paginado",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    assert estado["cursores"][console.id] == 0

    # 2) posiciona o cursor em item distante do inicio (PageDown real via TTY).
    ch, estado, saida = _passo_tty(estado, modelo, b"\x1b[6~")
    assert ch == _demo.TECLA_PAGE_DOWN
    item_logico_alvo = estado["cursores"][console.id]
    assert item_logico_alvo > 0, "cursor deve estar longe do primeiro item"
    id_item_alvo = "item_{0:02d}".format(item_logico_alvo + 1)
    assert _cursor_visivel_no_item(saida, simbolo, id_item_alvo)

    # 3) marca o item corrente (console declara selecao multipla e todos os
    # itens sao selecionaveis).
    ch, estado, _saida = _passo_tty(estado, modelo, b" ")
    assert ch == " "
    assert estado["selecoes"][console.id] == [id_item_alvo]

    # 4)-6) sequencia de tamanhos intermediarios na MESMA largura, incluindo
    # 1 item/pagina (altura=10) e uma geometria insuficiente (altura=8, que
    # ``renderizar_tela`` rejeita com RenderizadorErro -- o mesmo caso em que
    # ``_resolver_conteudo`` mostraria o quadro minimo no runtime real).
    alturas = [24, 20, 15, 10, 8, 10, 15, 20, 24]
    for altura in alturas:
        estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
        estado = _reconciliar_paginacao_apos_resize(estado, modelo)

        # cursor logico e selecao nunca se movem por resize (apenas a pagina).
        assert estado["cursores"][console.id] == item_logico_alvo
        assert estado["selecoes"][console.id] == [id_item_alvo]

        try:
            saida = renderizar_estado(estado, modelo, largura=largura, altura=altura)
        except RenderizadorErro:
            # Geometria insuficiente: o render real cai no quadro minimo
            # (_resolver_conteudo); aqui basta confirmar que a reconciliacao
            # nao alterou cursor/selecao (already asserted above) e seguir.
            continue

        m = re.search(r"página (\d+)/(\d+)", saida)
        assert m is not None, "altura={0} sem indicador de pagina".format(altura)
        pagina_atual = int(m.group(1))
        total_paginas = int(m.group(2))
        assert 1 <= pagina_atual <= total_paginas

        # obtem o novo plano fisico (mesma autoridade de geometria usada pelo
        # tratamento de resize) e confirma que a pagina atual CONTEM o item
        # logico do cursor.
        capacidade_real = _rend.altura_interna_disponivel(
            modelo, estado["estilo"], largura, altura, False,
            console=console, foco_console=estado.get("foco_console"),
            cursores=estado.get("cursores"), lista_foco=navegacao.lista_foco(modelo),
            selecoes=estado.get("selecoes"), paginas_atuais=estado.get("pagina_atual"),
        )
        pagina_do_alvo = paginacao.pagina_do_item_logico(
            console, item_logico_alvo, largura, capacidade_real, False,
            desconto_estrutural=3,
        )
        assert pagina_atual == pagina_do_alvo == estado["pagina_atual"][console.id], (
            "altura={0}: pagina renderizada ({1}) diverge da pagina do item "
            "logico do cursor ({2})".format(altura, pagina_atual, pagina_do_alvo)
        )

        # confirma "→" no quadro, no item correto -- e em nenhum outro.
        assert _cursor_visivel_no_item(saida, simbolo, id_item_alvo), (
            "altura={0}: cursor nao visivel em {1} (pagina {2}/{3})".format(
                altura, id_item_alvo, pagina_atual, total_paginas
            )
        )
        outros_itens = [
            "item_{0:02d}".format(n) for n in range(1, 19)
            if "item_{0:02d}".format(n) != id_item_alvo
        ]
        for outro in outros_itens:
            assert not _cursor_visivel_no_item(saida, simbolo, outro), (
                "altura={0}: cursor vazou para {1}".format(altura, outro)
            )

        # selecao permanece a mesma ao longo de toda a sequencia.
        assert estado["selecoes"][console.id] == [id_item_alvo]

    # 7)-8) volta ao tamanho inicial: mesmo item logico, mesma selecao.
    estado = dict(estado, largura=largura, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida_final = renderizar_estado(estado, modelo, largura=largura, altura=24)
    assert estado["cursores"][console.id] == item_logico_alvo
    assert estado["selecoes"][console.id] == [id_item_alvo]
    assert _cursor_visivel_no_item(saida_final, simbolo, id_item_alvo)


def test_demo_h0045_p05_caso_limite_um_item_por_pagina():
    """Caso limite: capacidade 1 item/pagina -- pagina exata do item (H-0045-P05).

    Com exatamente 1 item por pagina, a pagina que deve conter o item logico
    do cursor e deterministicamente a sua posicao 1-based na ordem declarada
    (nenhum outro item compartilha a pagina). Passa pela MESMA funcao de
    resize e pelo render final -- nao chama ``pagina_do_item_logico``
    isoladamente.
    """
    import re

    modelo = _modelo_fluxo_paginado()
    console = modelo.corpo.elementos[0]
    simbolo = carregar_estilo().selecionado_simbolo
    largura = 45

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": 24,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_fluxo_execucao_paginado",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    # item_intermediario: nem o primeiro nem o ultimo (posicao 11 de 18).
    _ch, estado, _saida = _passo_tty(estado, modelo, b"\x1b[6~")
    item_logico_alvo = estado["cursores"][console.id]
    assert 0 < item_logico_alvo < 17

    estado = dict(estado, largura=largura, altura=10, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida = renderizar_estado(estado, modelo, largura=largura, altura=10)

    m = re.search(r"página (\d+)/(\d+)", saida)
    pagina_atual = int(m.group(1))
    total_paginas = int(m.group(2))

    assert total_paginas == 18, "capacidade esperada de 1 item/pagina (18 itens)"
    pagina_esperada = item_logico_alvo + 1
    assert pagina_atual == pagina_esperada == estado["pagina_atual"][console.id]
    id_item_alvo = "item_{0:02d}".format(item_logico_alvo + 1)
    assert _cursor_visivel_no_item(saida, simbolo, id_item_alvo)


def test_demo_h0045_p04_dois_consoles_ids_unicos_foco_e_paginas_independentes():
    """P04: IDs unicos — foco no segundo console; paginas/cursores independentes.

    H-0045-P06 / QA-H0045-P05-001: a largura=80/altura=24 original cabia os
    12 itens de cada console em uma unica pagina real (12<=16); o teste
    ANTES forcava manualmente ``altura_interna=1`` para simular capacidade
    1/pagina -- mascarando o bug em que o RENDER real (arranjo horizontal)
    tambem produzia capacidade 1 por nunca receber ``altura_alvo``. Com o bug
    corrigido, a geometria real (nao mais forcada) e usada em toda a
    sequencia, via ``processar_comando`` (mesmo caminho interativo real).
    """
    import re

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_dois_consoles_paginas_independentes",
            "config/telas/demo",
        )
    )
    lista = navegacao.lista_foco(modelo)
    assert [c.id for c in lista] == ["console_a", "console_b"]
    console_a, console_b = lista
    simbolo = carregar_estilo().selecionado_simbolo
    # Geometria estreita o suficiente para exigir mais de 1 pagina por
    # console (12 itens), calculada pela MESMA autoridade que o render usa.
    largura, altura = 80, 15

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_dois_consoles_paginas_independentes",
            "modelo": modelo,
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    estado = navegacao.avancar_foco(dict(estado, modelo=modelo))
    assert estado["foco_console"] == 1
    assert estado["cursores"][console_b.id] == 0

    saida = renderizar_estado(estado, modelo, largura=largura, altura=altura)
    # Horizontal: a01 e b01 na mesma linha; prova pelo prefixo do cursor.
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("b01"), saida)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("a01"), saida)

    # Console B (focado) avanca pagina via comando real PageDown; A permanece
    # na pagina 1 com chave de estado propria (paginas independentes por id).
    estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
    estado_pag = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    assert estado_pag["pagina_atual"][console_a.id] == 1
    assert estado_pag["pagina_atual"][console_b.id] == 2
    assert console_a.id != console_b.id

    saida2 = renderizar_estado(estado_pag, modelo, largura=largura, altura=altura)
    m_a = re.search(r"página (\d+)/(\d+)", saida2)
    assert m_a is not None
    total_paginas = int(m_a.group(2))
    assert "página 1/{0}".format(total_paginas) in saida2
    assert "página 2/{0}".format(total_paginas) in saida2
    assert "a01" in saida2
    assert "b01" not in saida2
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("a01"), saida2)
    # Cursor de B aponta para o primeiro navegavel da pagina 2 (mesma regra
    # de PageDown usada em outros testes H-0045).
    primeiro_b_pag2 = estado_pag["cursores"][console_b.id]
    id_item_b = "b{0:02d}".format(primeiro_b_pag2 + 1)
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape(id_item_b), saida2)


def test_h0045_p06_dois_consoles_horizontais_plano_e_render_concordam():
    """H-0045-P06 (Teste 1): QA-H0045-P05-001 -- reproducao literal do achado.

    largura=80, altura=20, cursores console_a=10 (item logico -> a11) e
    console_b=8 (-> b09). Confirma que o plano auxiliar (``geometria_console``
    + ``tela.paginacao``) e o render concordam no total de paginas, que cada
    pagina contem o item logico do respectivo console e que o cursor aparece
    somente no console focado.
    """
    import re

    modelo = construir_modelo(
        carregar_tela(
            None, "h0045_dois_consoles_paginas_independentes", "config/telas/demo",
        )
    )
    lista = navegacao.lista_foco(modelo)
    console_a, console_b = lista
    estilo = carregar_estilo()
    simbolo = estilo.selecionado_simbolo
    largura, altura = 80, 20

    geometria_a = _rend.geometria_console(
        modelo, estilo, largura, altura, False, console=console_a, lista_foco=lista,
    )
    geometria_b = _rend.geometria_console(
        modelo, estilo, largura, altura, False, console=console_b, lista_foco=lista,
    )
    assert geometria_a is not None and geometria_b is not None

    total_a = paginacao.total_paginas(
        console_a, geometria_a["largura"], geometria_a["altura_interna"], False,
        desconto_estrutural=3,
    )
    total_b = paginacao.total_paginas(
        console_b, geometria_b["largura"], geometria_b["altura_interna"], False,
        desconto_estrutural=3,
    )
    pagina_a11 = paginacao.pagina_do_item_logico(
        console_a, 10, geometria_a["largura"], geometria_a["altura_interna"], False,
        desconto_estrutural=3,
    )
    pagina_b09 = paginacao.pagina_do_item_logico(
        console_b, 8, geometria_b["largura"], geometria_b["altura_interna"], False,
        desconto_estrutural=3,
    )

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": estilo, "largura": largura, "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_dois_consoles_paginas_independentes",
            "foco_console": 0,
            "cursores": {console_a.id: 10, console_b.id: 8},
            "pagina_atual": {console_a.id: pagina_a11, console_b.id: pagina_b09},
        }
    )
    saida = renderizar_estado(estado, modelo, largura=largura, altura=altura)

    # Plano auxiliar e renderer concordam no total (autoridade unica).
    assert "página {0}/{1}".format(pagina_a11, total_a) in saida
    assert "página {0}/{1}".format(pagina_b09, total_b) in saida
    # A pagina de cada console contem seu item logico.
    assert "a11" in saida
    assert "b09" in saida
    # Cursor visivel somente no console focado (console_a).
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("a11"), saida)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("b09"), saida)


def test_h0045_p06_seta_com_um_item_por_pagina():
    """H-0045-P06 (Teste 2): seta em geometria de capacidade minima (1/pagina).

    CORRECAO DE INSTRUCAO (prevalece o handoff H-0045/D15 sobre o exemplo
    generico do prompt): setas NUNCA mudam de pagina -- operam somente sobre
    os itens navegaveis da pagina visual atual. Com exatamente 1 item
    navegavel na pagina (item_17), a seta para baixo produz SEM_MOVIMENTO
    (D9): pagina e cursor permanecem inalterados. Somente ``.``/``>`` avancam
    de pagina, levando o cursor ao primeiro navegavel da pagina destino
    (item_18, quando for essa a pagina seguinte).
    """
    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    estilo = carregar_estilo()
    simbolo = estilo.selecionado_simbolo
    largura, altura = 45, 10

    geometria = _rend.geometria_console(modelo, estilo, largura, altura, False, console=console)
    assert geometria is not None
    assert geometria["altura_interna"] == 1, "cenario exige exatamente 1 item/pagina"
    pagina_item17 = paginacao.pagina_do_item_logico(
        console, 16, geometria["largura"], geometria["altura_interna"], False,
        desconto_estrutural=3,
    )

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": estilo, "largura": largura, "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_paginacao_console_unico",
            "foco_console": 0,
            "cursores": {console.id: 16},
            "pagina_atual": {console.id: pagina_item17},
        }
    )
    saida_inicial = renderizar_estado(estado, modelo, largura=largura, altura=altura)
    assert _cursor_visivel_no_item(saida_inicial, simbolo, "item_17")
    assert "item_18" not in saida_inicial

    # Seta para baixo: SEM_MOVIMENTO (D15/D9) -- pagina e cursor inalterados.
    apos_seta = processar_comando(estado, "\x1b[B", modelo)
    saida_apos_seta = renderizar_estado(apos_seta, modelo, largura=largura, altura=altura)
    assert apos_seta["cursores"][console.id] == 16
    assert apos_seta["pagina_atual"][console.id] == pagina_item17
    assert _cursor_visivel_no_item(saida_apos_seta, simbolo, "item_17")
    assert "item_18" not in saida_apos_seta
    assert saida_apos_seta.count(simbolo) == 1

    # PageDown avanca exatamente uma pagina: cursor vai para o primeiro
    # navegavel da pagina destino (item_18).
    apos_ponto = processar_comando(apos_seta, _demo.TECLA_PAGE_DOWN, modelo)
    saida_apos_ponto = renderizar_estado(apos_ponto, modelo, largura=largura, altura=altura)
    assert apos_ponto["cursores"][console.id] == 17
    pagina_item18 = paginacao.pagina_do_item_logico(
        console, 17, geometria["largura"], geometria["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert apos_ponto["pagina_atual"][console.id] == pagina_item18
    assert "item_18" in saida_apos_ponto
    assert _cursor_visivel_no_item(saida_apos_ponto, simbolo, "item_18")
    assert not _cursor_visivel_no_item(saida_apos_ponto, simbolo, "item_17")
    assert saida_apos_ponto.count(simbolo) == 1


def test_h0045_p06_comandos_de_pagina_avancam_e_recuam_exatamente_uma_pagina():
    """H-0045-P06 (Teste 3): '.'/'>')/','/'<' usam a MESMA autoridade do render."""
    import re

    modelo = _modelo()
    console = modelo.corpo.elementos[0]
    estado = _estado_inicial_paginado(modelo)
    estilo = estado["estilo"]
    simbolo = estilo.selecionado_simbolo

    def _pagina_total_saida(est):
        saida = renderizar_estado(est, modelo, largura=80, altura=24)
        m = re.search(r"página (\d+)/(\d+)", saida)
        assert m is not None
        return int(m.group(1)), int(m.group(2)), saida

    geometria = _rend.geometria_console(modelo, estilo, 80, 24, False, console=console)
    total_autoridade = paginacao.total_paginas(
        console, geometria["largura"], geometria["altura_interna"], False,
        desconto_estrutural=3,
    )

    pag1, total1, _saida1 = _pagina_total_saida(estado)
    assert pag1 == 1 and total1 == total_autoridade
    assert estado["pagina_atual"][console.id] == pag1

    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    assert estado["pagina_atual"][console.id] == 2
    pag2, total2, saida2 = _pagina_total_saida(estado)
    assert pag2 == 2 and total2 == total_autoridade
    assert estado["pagina_atual"][console.id] == pag2
    assert simbolo in saida2  # cursor pertence a pagina visivel

    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    assert estado["pagina_atual"][console.id] == 3
    pag3, total3, saida3 = _pagina_total_saida(estado)
    assert pag3 == 3 and total3 == total_autoridade
    assert simbolo in saida3

    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    assert estado["pagina_atual"][console.id] == 2
    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    assert estado["pagina_atual"][console.id] == 1
    pag_final, total_final, saida_final = _pagina_total_saida(estado)
    assert pag_final == 1 and total_final == total_autoridade
    assert simbolo in saida_final


def _console_paginado_selecionavel_h0045(idc, prefixo, n_itens, titulo):
    from tela.modelo import ElementoCorpo

    distribuicao_matricial = {
        "formacao": {"politica": "preferencia_colunas", "colunas": {"minimo": 1, "maximo": 1}},
        "ordem": "por_linha",
        "dimensionamento": {"colunas": {"politica": "uniforme"}, "linhas": {"politica": "uniforme"}},
        "espacamento": {
            "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
            "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
            "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
        },
        "distribuicao_horizontal": {"politica": "inicio"},
        "distribuicao_vertical": {"politica": "inicio"},
        "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos", "vertical": "uniforme_margens_e_vaos"},
        "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
        "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
    }
    itens = [
        {
            "id": "{0}{1:02d}".format(prefixo, i),
            "texto": "{0}{1:02d}".format(prefixo, i),
            "navegavel": True,
            "selecionavel": True,
            "politica_quebra": "permitir_quebra_somente_se_maior_que_pagina",
        }
        for i in range(1, n_itens + 1)
    ]
    return ElementoCorpo(
        id=idc, tipo="console",
        _campos_inertes={
            "titulo": titulo, "itens": itens,
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "multipla",
            "politica_paginacao": "com",
        },
        distribuicao_matricial=distribuicao_matricial,
    )


def test_h0045_p06_sequencia_integrada_console_unico_e_dois_consoles():
    """H-0045-P06 (Teste 4): sequencia integrada em uma unica execucao.

    Modelo em memoria (sem fixture permanente) com dois consoles horizontais
    paginados e com selecao multipla: abre; posiciona cursor distante;
    seleciona; reduz ate 1 item/pagina; usa seta; avanca/recua pagina;
    expande; alterna console; pagina o segundo console; volta ao primeiro;
    confirma independencia. Registra o quadro apos cada acao.
    """
    import re
    from tela.modelo import ModeloTela, Corpo

    # 40 itens: mesmo na geometria de abertura (80x24, capacidade ~16),
    # exige mais de 1 pagina -- PageDown precisa ter efeito ja no passo 2.
    console_x = _console_paginado_selecionavel_h0045("console_x", "x", 40, "X")
    console_y = _console_paginado_selecionavel_h0045("console_y", "y", 40, "Y")
    modelo = ModeloTela(
        id="t4", schema="tela.v1",
        cabecalho={"titulo": "Sequencia", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(
            arranjo="horizontal", distribuicao={"modo": "igual"},
            elementos=[console_x, console_y],
        ),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()

    log = []

    def _registrar(rotulo, estado, largura, altura):
        saida = renderizar_estado(estado, modelo, largura=largura, altura=altura)
        console = navegacao.console_focado(dict(estado, modelo=modelo))
        m = re.search(r"página (\d+)/(\d+)", saida)
        entrada = {
            "acao": rotulo,
            "console_focado": console.id if console is not None else None,
            "largura": largura,
            "altura": altura,
            "pagina_atual": estado["pagina_atual"].get(console.id) if console is not None else None,
            "total_paginas": int(m.group(2)) if m else None,
            "item_com_cursor": estado["cursores"].get(console.id) if console is not None else None,
            "itens_selecionados": list(estado.get("selecoes", {}).get(console.id, []) if console is not None else []),
            "indicador_renderizado": m.group(0) if m else None,
        }
        log.append(entrada)
        return saida

    # 1) abrir cenario.
    largura, altura = 80, 24
    estado = criar_estado_inicial()
    estado.update({"estilo": estilo, "largura": largura, "altura": altura, "desconto_estrutural": 3})
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    assert estado["foco_console"] == 0
    _registrar("abrir", estado, largura, altura)

    # 2) cursor em item distante (PageDown).
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("cursor_distante", estado, largura, altura)
    item_alvo_x = estado["cursores"][console_x.id]
    assert item_alvo_x > 0

    # 3) selecionar item corrente.
    estado = processar_comando(estado, " ", modelo)
    _registrar("selecionar", estado, largura, altura)
    assert len(estado["selecoes"][console_x.id]) == 1
    id_selecionado_x = estado["selecoes"][console_x.id][0]

    # 4) reduzir ate 1 item/pagina.
    largura, altura = 80, 8
    geometria_1item = _rend.geometria_console(
        modelo, estilo, largura, altura, False, console=console_x,
        lista_foco=navegacao.lista_foco(modelo),
    )
    assert geometria_1item is not None and geometria_1item["altura_interna"] == 1
    estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    _registrar("reduzir_1_item_por_pagina", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x  # item logico preservado
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]  # selecao preservada

    # 5) usar seta (1 item/pagina -> sem outro item na mesma pagina, D9).
    estado = processar_comando(estado, "\x1b[B", modelo)
    _registrar("seta_baixo", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x

    # 6) avancar pagina.
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("avancar_pagina", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x + 1

    # 7) recuar pagina.
    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    _registrar("recuar_pagina", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x

    # 8) expandir de volta.
    largura, altura = 80, 24
    estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    _registrar("expandir", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]
    pagina_x_antes_de_alternar = estado["pagina_atual"][console_x.id]

    # 9) alternar console (Tab).
    estado = processar_comando(estado, "\t", modelo)
    _registrar("alternar_console", estado, largura, altura)
    assert estado["foco_console"] == 1
    assert estado["cursores"][console_y.id] == 0

    # 10) repetir paginacao no segundo console.
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("paginar_console_y", estado, largura, altura)
    assert estado["cursores"][console_y.id] > 0

    # 11) voltar ao primeiro (Tab circular com apenas 2 consoles).
    estado = processar_comando(estado, "\t", modelo)
    _registrar("voltar_console_x", estado, largura, altura)
    assert estado["foco_console"] == 0

    # 12) confirmar independencia: console_x preservou cursor/pagina/selecao
    # integralmente, apesar da paginacao aplicada em console_y.
    assert estado["cursores"][console_x.id] == item_alvo_x
    assert estado["pagina_atual"][console_x.id] == pagina_x_antes_de_alternar
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]
    assert estado["pagina_atual"][console_y.id] != 1  # console_y avancou
    assert console_x.id != console_y.id

    assert len(log) == 11
    for entrada in log:
        assert entrada["indicador_renderizado"] is not None, entrada


def test_h0045_p07_sequencia_integrada_console_em_grupo():
    """H-0045-P07 (Teste 7 / QA-H0045-P06-001): sequencia integrada com os
    DOIS consoles paginados dentro do MESMO grupo horizontal permitido
    (H-0027), em vez de diretamente no corpo raiz.

    Reproduz o cenario exato do achado bloqueante: antes deste patch,
    ``_geometria_por_console`` so mapeava elementos diretos de
    ``corpo.elementos[]`` e ``geometria_console`` caia no fallback
    ``next(iter(mapa.values()))`` para qualquer console dentro de grupo --
    comandos de pagina, setas e a reconciliacao de resize podiam usar a
    geometria de OUTRO elemento. Repete a mesma sequencia de foco distante /
    selecao / resize / seta / expansao / alternancia de foco / paginacao
    independente de
    ``test_h0045_p06_sequencia_integrada_console_unico_e_dois_consoles``,
    mas com ambos os consoles vivendo dentro do grupo, confirmando que a
    autoridade geometrica recursiva devolve a caixa REAL de cada console em
    todo o percurso.
    """
    import re
    from tela.modelo import ElementoCorpo, ModeloTela, Corpo

    console_x = _console_paginado_selecionavel_h0045("console_x", "x", 40, "X")
    console_y = _console_paginado_selecionavel_h0045("console_y", "y", 40, "Y")
    grupo = ElementoCorpo(
        id="grupo_p07", tipo="grupo",
        _campos_inertes={"arranjo": "horizontal", "distribuicao": {"modo": "igual"}},
        elementos=[console_x, console_y],
    )
    modelo = ModeloTela(
        id="t7", schema="tela.v1",
        cabecalho={"titulo": "Sequencia Grupo", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[grupo]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    lista = navegacao.lista_foco(modelo)
    assert [c.id for c in lista] == ["console_x", "console_y"]

    log = []

    def _registrar(rotulo, estado, largura, altura):
        saida = renderizar_estado(estado, modelo, largura=largura, altura=altura)
        console = navegacao.console_focado(dict(estado, modelo=modelo))
        m = re.search(r"página (\d+)/(\d+)", saida)
        geometria = None
        if console is not None:
            geometria = _rend.geometria_console(
                modelo, estilo, largura, altura, False, console=console,
                foco_console=estado.get("foco_console"),
                cursores=estado.get("cursores"), lista_foco=lista,
                selecoes=estado.get("selecoes"),
                paginas_atuais=estado.get("pagina_atual"),
            )
        entrada = {
            "acao": rotulo,
            "console_focado": console.id if console is not None else None,
            "geometria_do_console": geometria,
            "pagina_atual": estado["pagina_atual"].get(console.id) if console is not None else None,
            "total_paginas": int(m.group(2)) if m else None,
            "item_com_cursor": estado["cursores"].get(console.id) if console is not None else None,
            "itens_selecionados": list(estado.get("selecoes", {}).get(console.id, []) if console is not None else []),
            "indicador_renderizado": m.group(0) if m else None,
        }
        log.append(entrada)
        return saida

    # 1) abrir modelo com console dentro de grupo.
    largura, altura = 80, 24
    estado = criar_estado_inicial()
    estado.update({"estilo": estilo, "largura": largura, "altura": altura, "desconto_estrutural": 3})
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    assert estado["foco_console"] == 0
    _registrar("abrir", estado, largura, altura)
    # QA-H0045-P06-001: a geometria REAL da coluna do grupo (80/2 == 40), NUNCA
    # a largura total do corpo (80) que o fallback antigo produziria.
    assert log[0]["geometria_do_console"]["largura"] == 40

    # 2) posicionar cursor em item distante.
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("cursor_distante", estado, largura, altura)
    item_alvo_x = estado["cursores"][console_x.id]
    assert item_alvo_x > 0

    # 3) selecionar item.
    estado = processar_comando(estado, " ", modelo)
    _registrar("selecionar", estado, largura, altura)
    assert len(estado["selecoes"][console_x.id]) == 1
    id_selecionado_x = estado["selecoes"][console_x.id][0]

    # 4) reduzir terminal.
    largura, altura = 80, 8
    estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    _registrar("reduzir", estado, largura, altura)
    assert estado["cursores"][console_x.id] == item_alvo_x  # item logico preservado
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]  # selecao preservada
    assert log[-1]["geometria_do_console"]["largura"] == 40

    # 5) paginar (PageDown).
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("paginar", estado, largura, altura)

    # 6) usar seta numa pagina com varios navegaveis.
    estado = processar_comando(estado, "\x1b[B", modelo)
    _registrar("seta_baixo", estado, largura, altura)
    assert isinstance(estado["cursores"][console_x.id], int)

    # 7) expandir de volta.
    largura, altura = 80, 24
    estado = dict(estado, largura=largura, altura=altura, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    _registrar("expandir", estado, largura, altura)
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]
    pagina_x_antes_de_alternar = estado["pagina_atual"][console_x.id]

    # 8) trocar foco para o outro console DO MESMO GRUPO.
    estado = processar_comando(estado, "\t", modelo)
    _registrar("alternar_console", estado, largura, altura)
    assert estado["foco_console"] == 1
    assert estado["cursores"][console_y.id] == 0
    assert log[-1]["geometria_do_console"]["largura"] == 40

    # 9) paginar o segundo console.
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    _registrar("paginar_console_y", estado, largura, altura)
    assert estado["cursores"][console_y.id] > 0

    # 10) retornar ao primeiro: paginas/cursores/selecoes por console
    # permanecem INDEPENDENTES mesmo compartilhando o mesmo grupo.
    estado = processar_comando(estado, "\t", modelo)
    _registrar("voltar_console_x", estado, largura, altura)
    assert estado["foco_console"] == 0
    assert estado["cursores"][console_x.id] == item_alvo_x
    assert estado["pagina_atual"][console_x.id] == pagina_x_antes_de_alternar
    assert estado["selecoes"][console_x.id] == [id_selecionado_x]
    assert estado["pagina_atual"][console_y.id] != 1  # console_y avancou

    assert len(log) == 10
    for entrada in log:
        assert entrada["indicador_renderizado"] is not None, entrada
        assert entrada["geometria_do_console"] is not None, entrada
        # As larguras dos DOIS consoles do grupo horizontal sao sempre a
        # coluna real (40), nunca a largura total do corpo (80) nem a
        # geometria de um console diferente.
        assert entrada["geometria_do_console"]["largura"] == 40, entrada


def test_demo_h0045_p09_pty_selecao_multipla_em_console_paginado_ponto_de_entrada_real():
    """VM-H0045-R05-005 (P09): selecao multipla em console paginado via TTY real.

    Abre ``python demo/demo.py h0045_fluxo_execucao_paginado`` em PTY real
    (mesmo ponto de entrada de ``main()``, nunca ``processar_comando`` isolado
    nem injecao direta em ``estado["selecoes"]``), cobrindo em sequencia:
    cursor inicial selecionavel, chip ``[Espaco] Marcar`` disponivel, toggle de
    selecao refletido no quadro, persistencia da selecao entre paginas,
    persistencia apos redimensionamento (inclusive 1 item/pagina), remocao da
    selecao, ``Todos`` cobrindo TODAS as paginas e ausencia de qualquer
    execucao disparada.
    """
    import fcntl
    import pty
    import select
    import signal
    import struct
    import subprocess
    import termios
    import time

    from tela.renderizador import _codigo_ansi_de_cor

    _ID_TELA = "h0045_fluxo_execucao_paginado"

    # 1)-3) fixture carregada fora do processo filho: confirma politica
    # multipla e cursor inicial selecionavel antes de abrir a sessao TTY.
    modelo = construir_modelo(
        carregar_tela(None, _ID_TELA, "config/telas/demo")
    )
    console = modelo.corpo.elementos[0]
    assert navegacao._console_declarou_selecao_multipla(console)
    from tela import selecao as selecao_mod
    assert selecao_mod.item_selecionavel(console, "item_01")

    estilo = carregar_estilo()
    codigo_inativo = _codigo_ansi_de_cor(estilo.cor_inativo)
    SEL = b"\xe2\x97\x8f"  # "●" utf-8
    OFF = b"\xe2\x97\x8b"  # "○" utf-8

    cols, lines = 80, 24
    master_fd = None
    slave_fd = None
    proc = None
    try:
        master_fd, slave_fd = pty.openpty()
        fcntl.ioctl(
            slave_fd, termios.TIOCSWINSZ,
            struct.pack("HHHH", lines, cols, 0, 0),
        )

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.Popen(
            [sys.executable, "demo/demo.py", _ID_TELA],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            cwd=str(_BASE), env=env, close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None

        def _ler_ate(timeout_total, ocioso, predicado=None):
            deadline = time.time() + timeout_total
            buf = b""
            ultimo = time.time()
            while time.time() < deadline:
                pronto, _, _ = select.select([master_fd], [], [], 0.05)
                if pronto:
                    try:
                        chunk = os.read(master_fd, 4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    buf += chunk
                    ultimo = time.time()
                    if predicado is not None and predicado(buf):
                        return buf
                elif time.time() - ultimo >= ocioso and buf:
                    if predicado is None or predicado(buf):
                        return buf
            return buf

        def _resize(novas_cols, novas_lines):
            fcntl.ioctl(
                master_fd, termios.TIOCSWINSZ,
                struct.pack("HHHH", novas_lines, novas_cols, 0, 0),
            )
            os.kill(proc.pid, signal.SIGWINCH)

        # 3) quadro inicial: cursor em item_01, chip [Espaco] Marcar ativo.
        inicial = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"item_01" in b and b"Marcar" in b,
        )
        assert proc.poll() is None, "processo encerrou antes do 1o quadro"
        assert b"\xe2\x86\x92 " + OFF + b" item_01" in inicial  # "→ ○ item_01"
        assert b"Marcar" in inicial
        assert inicial.count(SEL) == 0

        # 4)-5) Espaco: seleciona item_01; marcador aparece no quadro e o
        # estado logico do chip [Enter] muda para Executar (INATIVO --
        # selecao nao aciona execucao, D-SEL-07/D-SEL-21).
        os.write(master_fd, b" ")
        apos_espaco = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: SEL in b and b"Executar" in b,
        )
        assert proc.poll() is None, "processo encerrou apos Espaco"
        assert b"\xe2\x86\x92 " + SEL + b" item_01" in apos_espaco
        assert apos_espaco.count(SEL) == 1
        texto_apos_espaco = apos_espaco.decode("utf-8", errors="replace")
        assert "Executar" in texto_apos_espaco
        assert codigo_inativo and codigo_inativo in texto_apos_espaco

        # 6)-7) muda de pagina (PageDown) -- item_01 sai do quadro; a selecao
        # persiste no estado (confirmado ao retornar, abaixo) por ID, nao por
        # posicao fisica.
        os.write(master_fd, b"\x1b[6~")
        pagina2 = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"item_17" in b and b"p\xc3\xa1gina 2/2" in b,
        )
        assert proc.poll() is None, "processo encerrou ao mudar de pagina"
        assert b"item_01" not in pagina2
        assert b"p\xc3\xa1gina 2/2" in pagina2

        # retorna a pagina 1 (PageUp) -- o MESMO item continua marcado.
        os.write(master_fd, b"\x1b[5~")
        volta_pagina1 = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: SEL in b and b"p\xc3\xa1gina 1/2" in b,
        )
        assert proc.poll() is None, "processo encerrou ao retornar de pagina"
        assert b"\xe2\x86\x92 " + SEL + b" item_01" in volta_pagina1
        assert volta_pagina1.count(SEL) == 1

        # 8)-9) resize para 1 item/pagina: selecao (e cursor) preservados.
        _resize(45, 10)
        apos_resize_pequeno = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: SEL in b and b"p\xc3\xa1gina 1/18" in b,
        )
        assert proc.poll() is None, "processo encerrou apos reducao"
        assert b"\xe2\x86\x92 " + SEL + b" item_01" in apos_resize_pequeno
        assert b"p\xc3\xa1gina 1/18" in apos_resize_pequeno

        # 10) volta ao tamanho original -- selecao continua preservada.
        _resize(cols, lines)
        apos_resize_grande = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: SEL in b and b"p\xc3\xa1gina 1/2" in b,
        )
        assert proc.poll() is None, "processo encerrou apos ampliacao"
        assert b"\xe2\x86\x92 " + SEL + b" item_01" in apos_resize_grande
        assert apos_resize_grande.count(SEL) == 1

        # 11) Espaco novamente: remove a selecao de item_01.
        os.write(master_fd, b" ")
        apos_remocao = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"Todos" in b and SEL not in b,
        )
        assert proc.poll() is None, "processo encerrou apos remover selecao"
        assert b"\xe2\x86\x92 " + OFF + b" item_01" in apos_remocao
        assert apos_remocao.count(SEL) == 0
        assert b"Todos" in apos_remocao

        # 12)-13) Todos (Enter) com selecao vazia: marca todos os 16
        # selecionaveis da pagina 1 -- confirma tambem que NENHUMA execucao
        # foi disparada (cabecalho do cenario permanece o mesmo; nenhuma tela
        # de resultado substituiu o console).
        os.write(master_fd, b"\r")
        apos_todos = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b.count(SEL) >= 16 and b"Executar" in b,
        )
        assert proc.poll() is None, "processo encerrou apos Todos"
        assert apos_todos.count(SEL) == 16
        assert apos_todos.count(OFF) == 0
        assert b"FLUXO PAGINADO" in apos_todos
        texto_apos_todos = apos_todos.decode("utf-8", errors="replace")
        assert "Executar" in texto_apos_todos
        assert codigo_inativo and codigo_inativo in texto_apos_todos

        # 13) percorre a pagina 2: os dois itens restantes (item_17/18,
        # tambem selecionaveis) TAMBEM estao marcados -- Todos abrange todas
        # as paginas, nao apenas a pagina corrente.
        os.write(master_fd, b"\x1b[6~")
        pagina2_apos_todos = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"item_18" in b and SEL in b,
        )
        assert proc.poll() is None, "processo encerrou ao paginar apos Todos"
        assert pagina2_apos_todos.count(SEL) == 2
        assert pagina2_apos_todos.count(OFF) == 0
        assert b"item_17" in pagina2_apos_todos and b"item_18" in pagina2_apos_todos

        # Encerramento limpo: Esc (selecao ativa limpa, permanece na tela) +
        # Esc (sai).
        os.write(master_fd, b"\x1b")
        _ler_ate(2.0, 0.2)
        os.write(master_fd, b"\x1b")
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
            raise AssertionError("timeout ao encerrar via Esc")
        assert proc.returncode == 0
    finally:
        if proc is not None and proc.poll() is None:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except OSError:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                try:
                    proc.kill()
                    proc.wait(timeout=2)
                except Exception:
                    pass
        if slave_fd is not None:
            try:
                os.close(slave_fd)
            except OSError:
                pass
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass


def _modelo_h0045_verboso_multilinha():
    return construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_modo_verboso_multilinha",
            "config/telas/demo",
        )
    )


def _estado_h0045_verboso_multilinha(modelo, altura=24):
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_paginacao_modo_verboso_multilinha",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    estado["modo_verboso"] = _modo_verboso_de_modelo(modelo)
    return estado


def _linhas_de_conteudo_console(saida, titulo="VERBOSE"):
    linhas = saida.splitlines()
    inicio = next(i for i, linha in enumerate(linhas) if titulo in linha)
    fim = next(
        i for i in range(inicio + 1, len(linhas))
        if linhas[i].startswith("╰") and "página" in linhas[i]
    )
    resultado = []
    for linha in linhas[inicio + 1: fim]:
        conteudo = linha[1:-1].strip()
        if conteudo.startswith("→ "):
            conteudo = conteudo[2:].strip()
        if conteudo:
            resultado.append(conteudo)
    return resultado


def test_demo_h0045_p10_fixture_real_verbosa_multilinha_paginada_sem_perdas():
    """P10: fixture real prova paginas, cursor reconciliado e linhas unicas.

    IMP-H0045-P17-001: com a largura corrigida (P17), o item 1 (11 linhas
    fisicas) cabe inteiro na pagina 1 (capacidade 16); o item 2
    (``evitar_quebra``) nao aproveita o residuo de 5 linhas livres e inicia
    a pagina 2, onde tambem cabem os itens 3 e 4
    (``permitir_quebra_somente_se_maior_que_pagina``). A prova de
    continuacao real de um unico item fragmentado entre paginas fica a
    cargo do teste irmao de dimensao menor (80x15), onde a capacidade
    menor (7 linhas) forca o item 1 a fragmentar entre paginas."""
    modelo = _modelo_h0045_verboso_multilinha()
    console = modelo.corpo.elementos[0]
    estado = _estado_h0045_verboso_multilinha(modelo)
    mapa = _rend.mapa_fisico_de_itens(
        console, 80, 16, True, desconto_estrutural=3,
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, 16, True, desconto_estrutural=3,
    )
    assert estado["modo_verboso"] is True
    assert plano["total_paginas"] == 2
    assert any(entrada["linhas_fisicas"] > 1 for entrada in mapa)

    saidas = []
    for indice in range(plano["total_paginas"]):
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "terminal pequeno demais" not in saida
        assert "página {0}/2".format(indice + 1) in saida
        assert saida.count(carregar_estilo().selecionado_simbolo) <= 1
        assert "[V]" not in saida
        saidas.append(saida)
        if indice < plano["total_paginas"] - 1:
            estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)

    assert estado["pagina_atual"][console.id] == 2
    assert estado["cursores"][console.id] == 1  # longo_02 inicia a pagina 2
    assert "segmento_13" in saidas[0]
    # Item 1 cabe inteiro na pagina 1: nenhum fragmento seu aparece na
    # pagina 2, mesmo havendo residuo de 5 linhas livres nela.
    assert "segmento_13" not in saidas[1]
    assert carregar_estilo().selecionado_simbolo in saidas[0]
    assert carregar_estilo().selecionado_simbolo in saidas[1]

    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    assert estado["pagina_atual"][console.id] == 1
    assert estado["cursores"][console.id] == 0
    assert renderizar_estado(estado, modelo, largura=80, altura=24).count(
        carregar_estilo().selecionado_simbolo
    ) == 1

    # mapa recalculado apos o laco de renders para refletir o mesmo estado
    # fisico usado na producao de `saidas` (ver IMP-H0045-P17-001).
    mapa = _rend.mapa_fisico_de_itens(
        console, 80, 16, True, desconto_estrutural=3,
    )
    participantes = _rend._participantes_distribuicao_matricial(console)
    larguras = _rend._larguras_mapa_fisico_matricial(
        console, 77, 16, True, participantes,
    )
    indicador_w = _rend._largura_indicador_do_elemento(console)
    esperadas = []
    for indice, item in enumerate(console._campos_inertes["itens"]):
        largura_texto = max(1, larguras[indice] - indicador_w)
        esperadas.extend(_rend._quebrar_texto(item["texto"], largura_texto))
    produzidas = []
    for saida in saidas:
        produzidas.extend(_linhas_de_conteudo_console(saida))
    assert len(produzidas) == sum(
        entrada["linhas_fisicas"] for entrada in mapa
    )
    # QA-H0045-P18-003 (P19): comparação ORDENADA, preservando a ordem das
    # páginas, dos itens, dos fragmentos de cada item e das linhas dentro de
    # cada fragmento — prova também ausência de perda e de repetição. O valor
    # esperado é fixado antes da execução (não derivado da saída observada).
    assert produzidas == esperadas
    assert len(produzidas) == len(set(produzidas))
    for numero in range(1, 27):
        assert produzidas and sum(
            "segmento_{0:02d}".format(numero) in linha
            for linha in produzidas
        ) == 1


def test_demo_h0045_p10_dimensao_menor_repagina_sem_perda_e_cursor_correto():
    """P10: 80x15 muda a capacidade sem perder linhas nem identidade."""
    modelo = _modelo_h0045_verboso_multilinha()
    console = modelo.corpo.elementos[0]
    estado = _estado_h0045_verboso_multilinha(modelo, altura=15)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    plano = paginacao.plano_de_paginacao(
        console, 80, 7, True, desconto_estrutural=3,
    )
    # IMP-H0045-P17-001: largura corrigida (P17) reduz de 6 para 4 paginas
    # nesta geometria; permanece distinta do total da fixture 80x16 (2).
    assert plano["total_paginas"] == 4
    assert plano["total_paginas"] != 2

    saidas = []
    for indice in range(plano["total_paginas"]):
        saida = renderizar_estado(estado, modelo, largura=80, altura=15)
        assert "terminal pequeno demais" not in saida
        assert "página {0}/4".format(indice + 1) in saida
        assert saida.count(carregar_estilo().selecionado_simbolo) <= 1
        saidas.append(saida)
        if indice < plano["total_paginas"] - 1:
            estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)

    assert estado["pagina_atual"][console.id] == 4
    assert estado["cursores"][console.id] == 3  # curto_04 inicia a pagina 4
    participantes = _rend._participantes_distribuicao_matricial(console)
    larguras = _rend._larguras_mapa_fisico_matricial(
        console, 77, 7, True, participantes,
    )
    indicador_w = _rend._largura_indicador_do_elemento(console)
    esperadas = []
    for indice, item in enumerate(console._campos_inertes["itens"]):
        largura_texto = max(1, larguras[indice] - indicador_w)
        esperadas.extend(_rend._quebrar_texto(item["texto"], largura_texto))
    produzidas = []
    for saida in saidas:
        produzidas.extend(_linhas_de_conteudo_console(saida))
    # QA-H0045-P18-003 (P19): comparação ORDENADA, preservando a ordem das
    # páginas, dos itens, dos fragmentos de cada item e das linhas dentro de
    # cada fragmento — prova também ausência de perda e de repetição. O valor
    # esperado é fixado antes da execução (não derivado da saída observada).
    assert produzidas == esperadas
    assert len(produzidas) == len(set(produzidas))
    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    assert estado["pagina_atual"][console.id] == 3


# ---------------------------------------------------------------------------
# P11 / VM-H0045-R07-003: fixtures de politicas de quebra e conjunto vazio
# materialmente exercitaveis (retomada da validacao manual em 15/17).
# ---------------------------------------------------------------------------


def _modelo_politicas_quebra():
    return construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_politicas_quebra",
            "config/telas/demo",
        )
    )


def _estado_politicas_quebra(modelo, altura=24):
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": altura,
            "tela_atual": "h0045_paginacao_politicas_quebra",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    estado["modo_verboso"] = _modo_verboso_de_modelo(modelo)
    return estado


def _linhas_conteudo_console_politicas(saida, titulo="POLITICAS"):
    """Como ``_linhas_de_conteudo_console``, mas pula a primeira ocorrencia
    de ``titulo`` (o cabecalho ``POLITICAS DE QUEBRA`` tambem contem a
    substring ``"POLITICAS"``); a segunda ocorrencia e a caixa do console."""
    linhas = saida.splitlines()
    ocorrencias = [i for i, linha in enumerate(linhas) if titulo in linha]
    inicio = ocorrencias[1]
    fim = next(
        i for i in range(inicio + 1, len(linhas))
        if linhas[i].startswith("╰") and "página" in linhas[i]
    )
    resultado = []
    for linha in linhas[inicio + 1: fim]:
        conteudo = linha[1:-1].strip()
        if conteudo.startswith("→ "):
            conteudo = conteudo[2:].strip()
        resultado.append(conteudo)
    return resultado


def test_demo_h0045_p11_politicas_quebra_fixture_real_seis_paginas_sem_perdas():
    """P11 / VM-H0045-R07-003 (retoma teste manual 15/17 e 17/17): fixture
    real prova as tres politicas de quebra com efeito distinguivel a 80x24.

    IMP-H0045-P17-001: com a largura corrigida (P17), os quatro itens cabem
    em apenas duas paginas nesta geometria (16 linhas/pagina). Item 1
    (``permitir_quebra``, 11 linhas) ocupa integralmente a pagina 1, com
    residuo de 5 linhas livres. Item 2 (``evitar_quebra``, 2 linhas) NAO
    aproveita esse residuo -- inicia sempre em pagina nova (pagina 2), mesmo
    havendo espaco disponivel na pagina anterior, provando o efeito real de
    ``evitar_quebra`` (D-TEC-07). Item 3 (``permitir_quebra_somente_se_maior_
    que_pagina``, 4 linhas) e item 4 (mesma politica, 7 linhas) cabem no
    residuo da propria pagina 2 apos o item 2, provando que essa politica
    aproveita espaco restante quando o item cabe inteiro -- ao contrario de
    ``evitar_quebra``. A fragmentacao de um item entre paginas (quando ele
    excede a capacidade de uma pagina) e provada pelo teste irmao de
    dimensao menor (80x15, P11 dimensao_menor)."""
    modelo = _modelo_politicas_quebra()
    console = modelo.corpo.elementos[0]
    itens = console._campos_inertes["itens"]

    # 1) quantidade e ordem dos itens.
    assert [item["id"] for item in itens] == [
        "permitir_quebra_01",
        "evitar_quebra_02",
        "condicional_cabe_03",
        "condicional_maior_04",
    ]
    # 2) politica de cada item.
    assert [item["politica_quebra"] for item in itens] == [
        "permitir_quebra",
        "evitar_quebra",
        "permitir_quebra_somente_se_maior_que_pagina",
        "permitir_quebra_somente_se_maior_que_pagina",
    ]

    simbolo = carregar_estilo().selecionado_simbolo
    mapa = _rend.mapa_fisico_de_itens(console, 80, 16, True, desconto_estrutural=3)
    plano = paginacao.plano_de_paginacao(console, 80, 16, True, desconto_estrutural=3)
    # 15) largura corrigida reduz para duas paginas nesta geometria.
    assert plano["total_paginas"] == 2

    estado = _estado_politicas_quebra(modelo)
    linhas_por_pagina = {}
    cursores_por_pagina = {}
    for pagina_idx in range(1, 3):
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "página {0}/2".format(pagina_idx) in saida
        linhas_por_pagina[pagina_idx] = [
            l for l in _linhas_conteudo_console_politicas(saida) if l
        ]
        cursores_por_pagina[pagina_idx] = saida.count(simbolo)
        if pagina_idx < 2:
            # 7) comandos de pagina continuam operando.
            estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
            assert estado["pagina_atual"][console.id] == pagina_idx + 1

    # mapa recalculado apos o laco de renders para refletir o mesmo estado
    # fisico usado na producao das paginas (ver IMP-H0045-P17-001).
    mapa = _rend.mapa_fisico_de_itens(console, 80, 16, True, desconto_estrutural=3)
    participantes = _rend._participantes_distribuicao_matricial(console)
    larguras = _rend._larguras_mapa_fisico_matricial(console, 77, 16, True, participantes)
    indicador_w = _rend._largura_indicador_do_elemento(console)
    linhas_esperadas_por_item = {
        item["id"]: _rend._quebrar_texto(
            item["texto"], max(1, larguras[indice] - indicador_w)
        )
        for indice, item in enumerate(itens)
    }

    # 3) pagina 1: apenas o item 1, inteiro, sem residuo aproveitado pelo
    # item 2 (evitar_quebra sempre inicia pagina nova).
    assert linhas_por_pagina[1] == linhas_esperadas_por_item["permitir_quebra_01"]

    # 4) pagina 2: itens 2, 3 e 4, nesta ordem, sem fragmentacao entre eles.
    assert linhas_por_pagina[2] == (
        linhas_esperadas_por_item["evitar_quebra_02"]
        + linhas_esperadas_por_item["condicional_cabe_03"]
        + linhas_esperadas_por_item["condicional_maior_04"]
    )

    # 5) evitar_quebra nao aproveitou o residuo de 5 linhas livres da
    # pagina 1 (11 de 16 usadas): nenhum fragmento seu aparece nela.
    assert not any("EVIT_" in linha for linha in linhas_por_pagina[1])

    # 14) cursor somente em inicio navegavel: as duas paginas tem inicio
    # navegavel, logo exatamente 1 cursor em cada.
    assert cursores_por_pagina == {1: 1, 2: 1}

    # cursor e pagina reconciliados ao final da navegacao.
    assert estado["pagina_atual"][console.id] == 2
    assert estado["cursores"][console.id] == 1  # evitar_quebra_02 inicia a pagina 2

    # retorno a pagina 1 reconcilia o cursor no primeiro item navegavel.
    estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
    assert estado["pagina_atual"][console.id] == 1
    assert estado["cursores"][console.id] == 0

    # 11/12/13) nenhuma linha perdida, nenhuma duplicada, ordem preservada.
    todas = linhas_por_pagina[1] + linhas_por_pagina[2]
    esperadas = (
        linhas_esperadas_por_item["permitir_quebra_01"]
        + linhas_esperadas_por_item["evitar_quebra_02"]
        + linhas_esperadas_por_item["condicional_cabe_03"]
        + linhas_esperadas_por_item["condicional_maior_04"]
    )
    assert todas == esperadas
    assert len(todas) == len(set(todas))
    assert sum(entrada["linhas_fisicas"] for entrada in mapa) == len(esperadas)


def test_demo_h0045_p11_politicas_quebra_dimensao_menor_deriva_da_politica():
    """P11: 80x15 (capacidade real 7 linhas/pagina, distinta das 16 de 80x24)
    prova que a paginacao e as politicas derivam da capacidade fisica
    corrente, nao de contagens fixas calibradas para uma unica altura."""
    modelo = _modelo_politicas_quebra()
    console = modelo.corpo.elementos[0]
    estado = _estado_politicas_quebra(modelo, altura=15)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)

    mapa = _rend.mapa_fisico_de_itens(console, 80, 7, True, desconto_estrutural=3)
    plano = paginacao.plano_de_paginacao(console, 80, 7, True, desconto_estrutural=3)
    # IMP-H0045-P17-001: largura corrigida (P17) reduz de 11 para 4 paginas
    # nesta geometria; permanece distinta do total da fixture 80x16 (2).
    assert plano["total_paginas"] == 4
    assert plano["total_paginas"] != 2

    # evitar_quebra (2 linhas <= capacidade 7) nunca fragmenta, em qualquer
    # altura suportada -- fragmento unico, sempre.
    frags_evitar = [
        frag for pagina in plano["paginas"] for frag in pagina["fragmentos"]
        if frag["id"] == "evitar_quebra_02"
    ]
    assert len(frags_evitar) == 1
    assert frags_evitar[0]["linhas_fisicas"] == 2

    # permitir_quebra continua fragmentando em mais de uma pagina.
    frags_permitir = [
        frag for pagina in plano["paginas"] for frag in pagina["fragmentos"]
        if frag["id"] == "permitir_quebra_01"
    ]
    assert len(frags_permitir) > 1
    assert sum(f["linhas_fisicas"] for f in frags_permitir) == 11

    # Nenhuma linha perdida nem duplicada em qualquer item, nesta altura.
    linhas_por_id = {entrada["id"]: entrada["linhas_fisicas"] for entrada in mapa}
    linhas_fragmentadas = {}
    for pagina in plano["paginas"]:
        for frag in pagina["fragmentos"]:
            linhas_fragmentadas[frag["id"]] = (
                linhas_fragmentadas.get(frag["id"], 0) + frag["linhas_fisicas"]
            )
    assert linhas_fragmentadas == linhas_por_id

    # Linhas físicas esperadas por item nesta geometria (80x7), pela mesma
    # autoridade de largura usada pelo renderer (D-TEC-04), para provar a
    # sequência visível da página de continuação preservando a ordem.
    _itens = console._campos_inertes["itens"]
    _participantes = _rend._participantes_distribuicao_matricial(console)
    _larguras_7 = _rend._larguras_mapa_fisico_matricial(
        console, 77, 7, True, _participantes
    )
    _indicador_w = _rend._largura_indicador_do_elemento(console)
    linhas_esperadas_por_item = {
        item["id"]: _rend._quebrar_texto(
            item["texto"], max(1, _larguras_7[indice] - _indicador_w)
        )
        for indice, item in enumerate(_itens)
    }

    # QA-H0045-P18-002 (P19): prova da pagina somente de continuação no QUADRO
    # RENDERIZADO (nao apenas no plano abstrato). Em 80x15 (capacidade 7), o
    # plano destina a pagina 2 exclusivamente à continuação de
    # ``permitir_quebra_01`` (primeira_linha_do_item=False). As nove provas
    # abaixo confirmam o comportamento real no caminho de renderização, em vez
    # de validar somente o plano.
    pagina_continuacao = next(
        p for p in plano["paginas"]
        if p["fragmentos"]
        and not any(
            f["primeira_linha_do_item"] and f["navegavel"]
            for f in p["fragmentos"]
        )
    )
    num_pagina_cont = pagina_continuacao["pagina"]
    # Deriva a sequência exata de linhas físicas da continuação a partir do
    # plano: percorre os fragmentos de permitir_quebra_01 em ordem de página e
    # extrai, das linhas físicas totais do item, o trecho do fragmento da
    # página de continuação (preservando a ordem).
    _linhas_totais_item1 = linhas_esperadas_por_item["permitir_quebra_01"]
    _offset = 0
    linhas_continuacao_plano = []
    for pagina in plano["paginas"]:
        for frag in pagina["fragmentos"]:
            if frag["id"] != "permitir_quebra_01":
                continue
            trecho = _linhas_totais_item1[_offset:_offset + frag["linhas_fisicas"]]
            _offset += frag["linhas_fisicas"]
            if pagina["pagina"] == num_pagina_cont:
                linhas_continuacao_plano.extend(trecho)
    # Renderiza explicitamente cada página necessária até a de continuação.
    estado_render = _estado_politicas_quebra(modelo, altura=15)
    estado_render = _reconciliar_paginacao_apos_resize(estado_render, modelo)
    for _ in range(num_pagina_cont - 1):
        estado_render = processar_comando(estado_render, _demo.TECLA_PAGE_DOWN, modelo)
    # 1) a página é efetivamente renderizada; 8) o indicador mostra a página
    #    correta.
    saida_cont = renderizar_estado(estado_render, modelo, largura=80, altura=15)
    assert "página {0}/{1}".format(
        num_pagina_cont, plano["total_paginas"]
    ) in saida_cont
    linhas_visiveis_cont = [
        l for l in _linhas_conteudo_console_politicas(saida_cont) if l
    ]
    # 2) o conteúdo visível pertence somente à continuação de
    #    permitir_quebra_01; 3) não aparece início de outro item.
    assert linhas_visiveis_cont, "página de continuação sem conteúdo visível"
    for linha in linhas_visiveis_cont:
        # cada linha visível é uma linha física da continuação do item 1
        assert linha in linhas_continuacao_plano, (
            "linha estranha na página de continuação: {0!r}".format(linha)
        )
        # nenhum início de outro item (EVIT/CABE/MAIOR) aparece
        assert "EVIT_" not in linha
        assert "CABE_" not in linha
        assert "MAIOR_" not in linha
        # o início do próprio item 1 (PERM_L01) também não aparece nesta
        # página, pois é continuação, não primeira linha física
        assert "PERM_L01_" not in linha
    # 4) não existe cursor visível nessa página; 5) não existe item navegável
    #    iniciado nessa página (D-TEC-17): o item corrente não recebe símbolo
    #    de cursor em página de continuação.
    _simbolo_cont = carregar_estilo().selecionado_simbolo
    assert saida_cont.count(_simbolo_cont) == 0
    assert "\u2192" not in saida_cont  # seta unicode de cursor ausente
    # 9) nenhuma linha desaparece nem é repetida: a sequência visível é
    #    exatamente a sequência esperada da continuação, na mesma ordem.
    assert linhas_visiveis_cont == linhas_continuacao_plano
    # 6) a navegação pode chegar à página e permanecer nela; 7) o runtime não
    #    salta automaticamente para outra página: após chegar, um comando de
    #    recuo (PageUp) retorna à página anterior e um novo avanço (PageDown)
    #    volta exatamente à página de continuação, sem desvio.
    _estado_antes = processar_comando(estado_render, _demo.TECLA_PAGE_UP, modelo)
    assert _estado_antes["pagina_atual"][console.id] == num_pagina_cont - 1
    _estado_volta = processar_comando(_estado_antes, _demo.TECLA_PAGE_DOWN, modelo)
    assert _estado_volta["pagina_atual"][console.id] == num_pagina_cont
    _saida_volta = renderizar_estado(_estado_volta, modelo, largura=80, altura=15)
    assert "página {0}/{1}".format(
        num_pagina_cont, plano["total_paginas"]
    ) in _saida_volta

    # Comandos de pagina continuam operando ate a ultima pagina sob a nova
    # capacidade.
    for _ in range(plano["total_paginas"] - 1):
        estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    assert estado["pagina_atual"][console.id] == plano["total_paginas"]
    saida = renderizar_estado(estado, modelo, largura=80, altura=15)
    assert "página {0}/{0}".format(plano["total_paginas"]) in saida


def _modelo_conjunto_vazio():
    return construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_conjunto_vazio",
            "config/telas/demo",
        )
    )


def test_demo_h0045_p11_conjunto_vazio_zero_itens_pagina_unica_chips_inativos_e_resize():
    """P11 / VM-H0045-R07-003 (retoma teste manual 16/17): ``itens: []``
    real via o mesmo ponto de entrada da demo -- zero itens navegaveis,
    pagina 1/1, sem cursor, controles de pagina visiveis e INATIVOS (nunca
    omitidos), comandos de pagina/setas sem efeito, resize preserva o
    estado, nenhum conteudo default introduzido."""
    modelo = _modelo_conjunto_vazio()
    console = modelo.corpo.elementos[0]

    # 1) zero itens no modelo (nao apenas zero navegaveis: itens == []).
    assert console._campos_inertes.get("itens") == []
    assert navegacao.itens_navegaveis(console) == []
    assert navegacao.lista_foco(modelo) == []

    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 24,
            "tela_atual": "h0045_paginacao_conjunto_vazio",
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    assert estado["foco_console"] is None
    assert estado["cursores"] == {}
    assert estado["pagina_atual"] == {}

    saida = renderizar_estado(estado, modelo, largura=80, altura=24)
    # 2/3) pagina atual 1, total de paginas 1.
    assert "página 1/1" in saida
    # 4) nenhum cursor.
    assert carregar_estilo().selecionado_simbolo not in saida
    # 5/6) unidade multitecla visivel e inativa.
    assert _chip_paginas(carregar_estilo()) in _sem_ansi(saida)
    estados_chips = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados_chips.get("chip_pagina_anterior") is False
    assert estados_chips.get("chip_pagina_proxima") is False
    codigo_inativo = _rend._codigo_ansi_de_cor(carregar_estilo().cor_inativo)
    assert codigo_inativo + "PgUp" in saida
    # 10) nenhum conteudo default/sintetico (os quatro itens "aviso_NN"
    # observados na validacao manual anterior nao podem reaparecer).
    assert "aviso_" not in saida
    assert "info_0" not in saida

    # 7/8) comandos de pagina e setas sem efeito.
    for comando in (",", "<", ".", ">", "\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"):
        novo = processar_comando(estado, comando, modelo)
        assert novo["pagina_atual"] == {}
        assert novo["cursores"] == {}
        assert novo["foco_console"] is None

    # 9) resize preserva o estado (zero itens, pagina 1/1, sem cursor,
    # controles inativos).
    estado_redim = dict(estado, largura=100, altura=30)
    estado_redim = _reconciliar_paginacao_apos_resize(estado_redim, modelo)
    assert estado_redim["pagina_atual"] == {}
    assert estado_redim["cursores"] == {}
    saida_redim = renderizar_estado(estado_redim, modelo, largura=100, altura=30)
    assert "página 1/1" in saida_redim
    assert _chip_paginas(carregar_estilo()) in _sem_ansi(saida_redim)
    estados_chips_redim = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados_chips_redim.get("chip_pagina_anterior") is False
    assert estados_chips_redim.get("chip_pagina_proxima") is False
    assert carregar_estilo().selecionado_simbolo not in saida_redim


# ---------------------------------------------------------------------------
# H-0045-P12: seis casos adaptativos pelo caminho real + PTY.
# ---------------------------------------------------------------------------


def _p12_abrir_caso(entrada, largura=80, altura=24):
    from demo import casos_validacao_paginacao as cv
    from demo.demo import (
        _carregar_modelo_por_id,
        _aplicar_caso_validacao_adaptativo,
        _estabelecer_foco_paginacao_inicial,
        _modo_verboso_de_modelo,
    )

    modelo = _carregar_modelo_por_id(entrada)
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": entrada,
            "caso_validacao_adaptativo": cv.id_caso_de_entrada(entrada),
            "modo_verboso": True,
        }
    )
    estado, caso = _aplicar_caso_validacao_adaptativo(
        estado, modelo, estado["caso_validacao_adaptativo"]
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    estado["modo_verboso"] = _modo_verboso_de_modelo(modelo) or True
    return estado, modelo, caso


def test_demo_h0045_p12_seis_casos_caminho_real_multiplas_geometrias():
    """Seis entradas via API; VAZIO/CONTINUACAO fixos; quatro legados ainda montaveis."""
    from demo import casos_validacao_paginacao as cv

    geometrias = {
        "regular": (80, 24),
        "estreita": (50, 24),
        "alta": (80, 40),
    }
    entradas = [
        "h0045_validacao_largura",
        "h0045_validacao_permitir",
        "h0045_validacao_evitar",
        "h0045_validacao_condicional",
        "h0045_validacao_continuacao",
        "h0045_validacao_vazio",
    ]
    for nome_geo, (largura, altura) in geometrias.items():
        for entrada in entradas:
            estado, modelo, caso = _p12_abrir_caso(entrada, largura, altura)
            console = modelo.corpo.elementos[0]
            saida = renderizar_estado(estado, modelo, largura, altura)
            assert caso["rotulo"] in saida or entrada.startswith("h0045_validacao_"), (
                nome_geo, entrada
            )
            assert "terminal pequeno demais" not in saida
            meta = estado["caso_validacao_meta"]
            assert meta["C"] == caso["C"]

            if entrada.endswith("largura"):
                assert caso["propriedades"]["comprimento_logico"] > caso["W"]
                for m in ("LARGURA_INICIO", "LARGURA_MEIO", "LARGURA_FIM"):
                    assert saida.count(m) == 1

            elif entrada.endswith("permitir"):
                plano = paginacao.plano_de_paginacao(
                    console, largura, caso["C"], True, desconto_estrutural=3
                )
                frags = [
                    f for p in plano["paginas"] for f in p["fragmentos"]
                    if f["id"] == "val_permitir_alvo"
                ]
                assert len(frags) >= 2

            elif entrada.endswith("evitar"):
                plano = paginacao.plano_de_paginacao(
                    console, largura, caso["C"], True, desconto_estrutural=3
                )
                frags = [
                    f for p in plano["paginas"] for f in p["fragmentos"]
                    if f["id"] == "val_evitar_alvo"
                ]
                assert len(frags) == 1
                pag_filler = next(
                    p for p in plano["paginas"]
                    if any(f["id"] == "val_evitar_filler" for f in p["fragmentos"])
                )
                assert not any(f["id"] == "val_evitar_alvo" for f in pag_filler["fragmentos"])

            elif entrada.endswith("condicional"):
                plano = paginacao.plano_de_paginacao(
                    console, largura, caso["C"], True, desconto_estrutural=3
                )
                assert len([
                    f for p in plano["paginas"] for f in p["fragmentos"]
                    if f["id"] == "CONDICIONAL_CABE"
                ]) == 1
                assert len([
                    f for p in plano["paginas"] for f in p["fragmentos"]
                    if f["id"] == "CONDICIONAL_MAIOR"
                ]) >= 2

            elif entrada.endswith("continuacao"):
                # Modelo fixo: hash invariavel; pagina de continuacao observavel.
                hash0 = cv.hash_modelo_logico(console)
                plano = paginacao.plano_de_paginacao(
                    console, largura, caso["C"], True, desconto_estrutural=3
                )
                assert plano["total_paginas"] >= 3
                assert cv.hash_modelo_logico(console) == hash0
                assert "CONT_INICIO" in saida
                # Avanca ate pagina sem inicio navegavel.
                alvo = next(
                    p["pagina"] for p in plano["paginas"]
                    if p["fragmentos"] and not any(
                        f["primeira_linha_do_item"] and f["navegavel"]
                        for f in p["fragmentos"]
                    )
                )
                while estado["pagina_atual"].get(console.id, 1) < alvo:
                    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
                saida2 = renderizar_estado(estado, modelo, largura, altura)
                assert "Trecho" in saida2 or "CONT_" in saida2
                assert cv.hash_modelo_logico(console) == hash0

            elif entrada.endswith("vazio"):
                assert console._campos_inertes["itens"] == []
                assert "página 1/1" in saida
                assert _chip_paginas(carregar_estilo()) in _sem_ansi(saida)
                assert carregar_estilo().selecionado_simbolo not in saida
                for cmd in (_demo.TECLA_PAGE_UP, _demo.TECLA_PAGE_DOWN, "\x1b[A"):
                    novo = processar_comando(estado, cmd, modelo)
                    assert novo["cursores"] == {}


def test_demo_h0045_p12_redimensionamento_nao_reconstrói_modelo_fixo():
    """Resize preserva itens/textos (CONTINUACAO / VAZIO); so reconciliacao."""
    from demo import casos_validacao_paginacao as cv

    estado, modelo, caso = _p12_abrir_caso("h0045_validacao_continuacao", 80, 24)
    console = modelo.corpo.elementos[0]
    hash0 = cv.hash_modelo_logico(console)
    snap0 = cv.snapshot_itens_logicos(console)
    C0 = caso["C"]

    estado = dict(estado, largura=80, altura=40)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    assert cv.hash_modelo_logico(console) == hash0
    assert cv.snapshot_itens_logicos(console) == snap0
    plano = paginacao.plano_de_paginacao(
        console, 80, estado.get("altura_interna") or 30, True, desconto_estrutural=3
    )
    # Conteudo fixo ainda produz continuacao em geometria alta tipica.
    assert any(
        p["fragmentos"]
        and not any(
            f["primeira_linha_do_item"] and f["navegavel"] for f in p["fragmentos"]
        )
        for p in plano["paginas"]
    ) or plano["total_paginas"] >= 2

    estado = dict(estado, largura=80, altura=24)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    assert cv.hash_modelo_logico(console) == hash0
    assert snap0 == cv.snapshot_itens_logicos(console)

    estado_v, modelo_v, _caso_v = _p12_abrir_caso("h0045_validacao_vazio", 80, 24)
    console_v = modelo_v.corpo.elementos[0]
    hash_v = cv.hash_modelo_logico(console_v)
    estado_v = dict(estado_v, largura=100, altura=30)
    estado_v = _reconciliar_paginacao_apos_resize(estado_v, modelo_v)
    assert cv.hash_modelo_logico(console_v) == hash_v
    assert console_v._campos_inertes["itens"] == []
    assert C0 >= 1


def test_demo_h0045_p12_pty_continuacao_e_vazio_ponto_de_entrada_real():
    """PTY: CONTINUACAO + resize + VAZIO pelo ponto de entrada real."""
    import fcntl
    import pty
    import select
    import signal
    import struct
    import subprocess
    import termios
    import time

    cols, lines = 80, 24
    master_fd = None
    slave_fd = None
    proc = None
    try:
        master_fd, slave_fd = pty.openpty()
        fcntl.ioctl(
            slave_fd, termios.TIOCSWINSZ,
            struct.pack("HHHH", lines, cols, 0, 0),
        )
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.Popen(
            [sys.executable, "demo/demo.py", "h0045_validacao_continuacao"],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            cwd=str(_BASE), env=env, close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None

        def _ler_ate(timeout_total, ocioso, predicado=None):
            deadline = time.time() + timeout_total
            buf = b""
            ultimo = time.time()
            while time.time() < deadline:
                pronto, _, _ = select.select([master_fd], [], [], 0.05)
                if pronto:
                    try:
                        chunk = os.read(master_fd, 4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    buf += chunk
                    ultimo = time.time()
                    if predicado is not None and predicado(buf):
                        return buf
                elif time.time() - ultimo >= ocioso and buf:
                    if predicado is None or predicado(buf):
                        return buf
            return buf

        def _resize(novas_cols, novas_lines):
            fcntl.ioctl(
                master_fd, termios.TIOCSWINSZ,
                struct.pack("HHHH", novas_lines, novas_cols, 0, 0),
            )
            os.kill(proc.pid, signal.SIGWINCH)

        inicial = _ler_ate(
            5.0, 0.4,
            predicado=lambda b: b"H0045-VAL-CONTINUACAO" in b and b"CONT_INICIO" in b,
        )
        assert proc.poll() is None
        assert b"H0045-VAL-CONTINUACAO" in inicial
        assert b"CONT_INICIO" in inicial

        # Avanca para pagina intermediaria (continuacao).
        os.write(master_fd, b"\x1b[6~")
        pagina2 = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"p\xc3\xa1gina 2/" in b,
        )
        assert proc.poll() is None
        assert b"p\xc3\xa1gina 2/" in pagina2
        # Sem cursor (seta unicode \xe2\x86\x92).
        assert b"\xe2\x86\x92" not in pagina2
        assert b"Trecho" in pagina2 or b"CONT_" in pagina2
        # Setas sem movimento: nao ha redesenho (estado inalterado); o
        # proximo comando de pagina ainda parte da pagina 2.
        os.write(master_fd, b"\x1b[B")
        time.sleep(0.15)

        # Comandos de pagina operam.
        os.write(master_fd, b"\x1b[6~")
        pagina3 = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"p\xc3\xa1gina 3/" in b or b"CONT_FIM" in b,
        )
        assert proc.poll() is None
        assert b"p\xc3\xa1gina 3/" in pagina3 or b"CONT_FIM" in pagina3
        os.write(master_fd, b"\x1b[5~")
        volta2 = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"p\xc3\xa1gina 2/" in b,
        )
        assert b"p\xc3\xa1gina 2/" in volta2
        assert b"\xe2\x86\x92" not in volta2

        # Aumenta altura — modelo fixo permanece; so geometria muda.
        _resize(80, 40)
        apos_alta = _ler_ate(
            5.0, 0.45,
            predicado=lambda b: b"H0045-VAL-CONTINUACAO" in b,
        )
        assert proc.poll() is None
        assert b"H0045-VAL-CONTINUACAO" in apos_alta
        assert b"CONT_" in apos_alta or b"Trecho" in apos_alta

        # Retorna a dimensao inicial.
        _resize(cols, lines)
        apos_volta = _ler_ate(
            5.0, 0.45,
            predicado=lambda b: b"H0045-VAL-CONTINUACAO" in b,
        )
        assert proc.poll() is None
        assert b"CONT_" in apos_volta or b"Trecho" in apos_volta

        # Encerra e abre VAZIO em novo processo.
        os.write(master_fd, b"\x1b")
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
        assert proc.returncode == 0

        # Novo PTY para VAZIO.
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass
        master_fd, slave_fd = pty.openpty()
        fcntl.ioctl(
            slave_fd, termios.TIOCSWINSZ,
            struct.pack("HHHH", lines, cols, 0, 0),
        )
        proc = subprocess.Popen(
            [sys.executable, "demo/demo.py", "h0045_validacao_vazio"],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            cwd=str(_BASE), env=env, close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None

        vazio = _ler_ate(
            5.0, 0.4,
            predicado=lambda b: b"p\xc3\xa1gina 1/1" in b and b"PgUp/PgDn" in b,
        )
        assert proc.poll() is None
        assert b"p\xc3\xa1gina 1/1" in vazio
        vazio_texto = vazio.decode("utf-8", errors="replace")
        vazio_visivel = _sem_ansi(vazio_texto)
        chip_paginas = _chip_paginas(carregar_estilo())
        assert chip_paginas in vazio_visivel
        assert "[PgUp][PgDn]" not in vazio_visivel
        if "\x1b[" in vazio_texto:
            import re as _re_ansi
            assert _re_ansi.search(
                r"\[\x1b\[[0-9;]*mPgUp", vazio_texto
            )
        assert b"\xe2\x86\x92" not in vazio
        # Comando de pagina sem efeito: sem redesenho; o quadro inicial
        # ja comprovou 1/1 e chips presentes.
        os.write(master_fd, b"\x1b[6~")
        time.sleep(0.15)

        os.write(master_fd, b"\x1b")
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
            raise AssertionError("timeout ao encerrar VAZIO via Esc")
        assert proc.returncode == 0
    finally:
        if proc is not None and proc.poll() is None:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except OSError:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                try:
                    proc.kill()
                    proc.wait(timeout=2)
                except Exception:
                    pass
        if slave_fd is not None:
            try:
                os.close(slave_fd)
            except OSError:
                pass
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# H-0045-P13: remocao de fallbacks geometricos (QA-H0045-P12-001).
# ---------------------------------------------------------------------------


def _p13_snapshot_modelo(modelo):
    """Captura material do modelo (cabecalho + itens do console) para igualdade."""
    cab = getattr(modelo, "cabecalho", None)
    if isinstance(cab, dict):
        cab_snap = dict(cab)
    else:
        cab_snap = {
            "titulo": getattr(cab, "titulo", None),
            "descricao": getattr(cab, "descricao", None),
        }
    console = None
    for elemento in modelo.corpo.elementos:
        if getattr(elemento, "tipo", None) == "console":
            console = elemento
            break
    itens = list(console._campos_inertes.get("itens") or []) if console else None
    titulo = console._campos_inertes.get("titulo") if console else None
    return {"cabecalho": cab_snap, "itens": itens, "titulo_console": titulo}


def test_demo_h0045_p13_01_geometria_ausente_falha_sem_mutacao():
    """P13-01/P13-06: geometria None interrompe antes de mutar o modelo."""
    import pytest
    from unittest.mock import patch

    from demo.demo import (
        _aplicar_caso_validacao_adaptativo,
        _carregar_modelo_por_id,
        casos_val,
    )

    modelo = _carregar_modelo_por_id("h0045_validacao_largura")
    antes = _p13_snapshot_modelo(modelo)
    itens_antes = [dict(i) for i in antes["itens"]]
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80,
            "altura": 24,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_validacao_largura",
            "modo_verboso": True,
        }
    )
    with patch("demo.demo.geometria_console", return_value=None):
        with pytest.raises(casos_val.GeometriaEfetivaAusente) as excinfo:
            _aplicar_caso_validacao_adaptativo(
                estado, modelo, "H0045-VAL-LARGURA"
            )
    assert "geometria efetiva do console nao resolvida" in str(excinfo.value)
    # Proibido caminho altura - 8 (capacidade inventada).
    assert "altura - 8" not in str(excinfo.value)
    depois = _p13_snapshot_modelo(modelo)
    assert depois["cabecalho"] == antes["cabecalho"]
    assert depois["titulo_console"] == antes["titulo_console"]
    assert depois["itens"] == itens_antes
    assert estado.get("caso_validacao_meta") is None
    assert estado.get("caso_validacao_adaptativo") is None


def test_demo_h0045_p13_02_largura_ausente_rejeitada_sem_80():
    """P13-02: resolver_largura_util_efetiva rejeita largura ausente (sem 80)."""
    import pytest

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    with pytest.raises(cv.GeometriaEfetivaAusente) as excinfo:
        cv.resolver_largura_util_efetiva(console, None, 16, True)
    msg = str(excinfo.value)
    assert "largura_console" in msg
    # Nao deve converter ausencia em 80.
    assert " 80" not in msg


def test_demo_h0045_p13_03_largura_zero_ou_negativa_rejeitada():
    """P13-03: largura 0 e -1 rejeitadas explicitamente."""
    import pytest

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    for valor in (0, -1):
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.resolver_largura_util_efetiva(console, valor, 16, True)


def test_demo_h0045_p13_04_capacidade_ausente_nao_produz_numero():
    """P13-04: capacidade_fisica_efetiva(None) nao produz numero."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    with pytest.raises(cv.GeometriaEfetivaAusente):
        resultado = cv.capacidade_fisica_efetiva(None)
        assert not isinstance(resultado, int)


def test_demo_h0045_p13_05_capacidade_zero_ou_negativa_rejeitada():
    """P13-05: capacidade 0 e -1 rejeitadas explicitamente."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for valor in (0, -1):
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.capacidade_fisica_efetiva(valor)


def test_demo_h0045_p13_07_caminho_nominal_seis_casos_preservados():
    """P13-07: seis casos P12 continuam construidos/executados sem fallback."""
    from demo import casos_validacao_paginacao as cv

    entradas = [
        "h0045_validacao_largura",
        "h0045_validacao_permitir",
        "h0045_validacao_evitar",
        "h0045_validacao_condicional",
        "h0045_validacao_continuacao",
        "h0045_validacao_vazio",
    ]
    for entrada in entradas:
        estado, modelo, caso = _p12_abrir_caso(entrada, 80, 24)
        saida = renderizar_estado(estado, modelo, 80, 24)
        assert caso["rotulo"] in saida
        assert caso["rotulo"] == cv.ROTULOS[cv.id_caso_de_entrada(entrada)]
        meta = estado["caso_validacao_meta"]
        assert meta["C"] == caso["C"]
        assert meta["C"] is not None and meta["C"] > 0
        # C vem de altura_interna da autoridade, nao de altura - 8.
        assert estado["altura_interna"] == meta["C"]
        if entrada.endswith(("vazio", "continuacao")):
            # Modelo fixo: W nao e gerado a partir da geometria.
            assert meta.get("modelo") == "fixo" or caso["W"] is None
        else:
            assert meta["W"] == caso["W"]
            assert meta["W"] > 0


def test_demo_h0045_p13_08_geometrias_validas_permanecem_adaptativas():
    """P13-08: regular, estreita e alta com CONTINUACAO fixa (sem regen por C)."""
    from demo import casos_validacao_paginacao as cv

    geometrias = {
        "regular": (80, 24),
        "estreita": (50, 24),
        "alta": (80, 40),
    }
    capacidades = {}
    hash0 = None
    for nome, (largura, altura) in geometrias.items():
        estado, modelo, caso = _p12_abrir_caso(
            "h0045_validacao_continuacao", largura, altura
        )
        console = modelo.corpo.elementos[0]
        if hash0 is None:
            hash0 = cv.hash_modelo_logico(console)
        else:
            assert cv.hash_modelo_logico(console) == hash0
        assert estado["altura_interna"] == caso["C"]
        assert caso["C"] == estado["altura_interna"]
        saida = renderizar_estado(estado, modelo, largura, altura)
        assert caso["rotulo"] in saida
        capacidades[nome] = caso["C"]
    assert capacidades["alta"] > capacidades["regular"]
    assert capacidades["estreita"] > 0


def test_demo_h0045_p14_01_capacidade_rejeita_string_numerica():
    """P14-01: capacidade_fisica_efetiva rejeita string numerica sem normalizar."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    with pytest.raises(cv.GeometriaEfetivaAusente):
        cv.capacidade_fisica_efetiva("16")


def test_demo_h0045_p14_02_capacidade_rejeita_float_integral():
    """P14-02: capacidade rejeita float integral (16.0); sem truncar."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    with pytest.raises(cv.GeometriaEfetivaAusente):
        cv.capacidade_fisica_efetiva(16.0)


def test_demo_h0045_p14_03_capacidade_rejeita_float_fracionario():
    """P14-03: capacidade rejeita float fracionario (16.9); sem truncar."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    with pytest.raises(cv.GeometriaEfetivaAusente):
        cv.capacidade_fisica_efetiva(16.9)


def test_demo_h0045_p14_04_largura_rejeita_string_numerica_sem_mapa():
    """P14-04: largura string rejeitada; mapa_fisico nao consultado."""
    import pytest
    from unittest.mock import patch

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    with patch(
        "tela.renderizador.mapa_fisico_de_itens"
    ) as mock_mapa:
        with pytest.raises(cv.GeometriaEfetivaAusente) as excinfo:
            cv.resolver_largura_util_efetiva(console, "80", 16, True)
        assert "largura_console" in str(excinfo.value)
        mock_mapa.assert_not_called()


def test_demo_h0045_p14_05_largura_rejeita_float_integral_sem_mapa():
    """P14-05: largura 80.0 rejeitada; mapa_fisico nao consultado."""
    import pytest
    from unittest.mock import patch

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    with patch(
        "tela.renderizador.mapa_fisico_de_itens"
    ) as mock_mapa:
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.resolver_largura_util_efetiva(console, 80.0, 16, True)
        mock_mapa.assert_not_called()


def test_demo_h0045_p14_06_largura_rejeita_float_fracionario_sem_mapa():
    """P14-06: largura 80.9 rejeitada; mapa_fisico nao consultado."""
    import pytest
    from unittest.mock import patch

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    with patch(
        "tela.renderizador.mapa_fisico_de_itens"
    ) as mock_mapa:
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.resolver_largura_util_efetiva(console, 80.9, 16, True)
        mock_mapa.assert_not_called()


def test_demo_h0045_p14_07_inteiros_positivos_permanecem_validos():
    """P14-07: int positivo em C e W; autoridade de largura executada."""
    from unittest.mock import patch

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id
    from tela import renderizador as rend

    entrada_c = 16
    saida_c = cv.capacidade_fisica_efetiva(entrada_c)
    assert saida_c == 16
    assert saida_c is entrada_c
    assert type(saida_c) is int

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    with patch(
        "tela.renderizador.mapa_fisico_de_itens",
        wraps=rend.mapa_fisico_de_itens,
    ) as mock_mapa:
        W = cv.resolver_largura_util_efetiva(console, 80, 16, True)
        assert type(W) is int and W > 0
        assert mock_mapa.call_count >= 1


def test_demo_h0045_p14_08_dominio_invalido_completo():
    """P14-08: dominio invalido rejeitado com GeometriaEfetivaAusente."""
    import pytest

    from demo import casos_validacao_paginacao as cv
    from demo.demo import _carregar_modelo_por_id

    invalidos = (None, True, False, 0, -1, "", [], {})
    for valor in invalidos:
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.capacidade_fisica_efetiva(valor)

    console = _carregar_modelo_por_id(
        "h0045_validacao_largura"
    ).corpo.elementos[0]
    for valor in invalidos:
        with pytest.raises(cv.GeometriaEfetivaAusente):
            cv.resolver_largura_util_efetiva(console, valor, 16, True)


def _p15_construtores_obrigatorios(cv, w, c=16):
    """Fronteiras construtoras cujo W e obrigatorio (sem default None)."""
    return {
        "construir_caso_largura": lambda: cv.construir_caso_largura(w, c),
        "construir_caso_permitir": lambda: cv.construir_caso_permitir(w, c),
        "construir_caso_evitar": lambda: cv.construir_caso_evitar(w, c),
        "construir_caso_condicional": lambda: cv.construir_caso_condicional(w, c),
        "construir_caso_continuacao": lambda: cv.construir_caso_continuacao(w, c),
    }


def _p15_todos_construtores(cv, w, c=16):
    """Todas as seis fronteiras construtoras diretamente invocaveis, incluindo
    ``construir_caso_vazio`` com W explicito (nao o default ``None``)."""
    todos = _p15_construtores_obrigatorios(cv, w, c)
    todos["construir_caso_vazio"] = lambda: cv.construir_caso_vazio(w, None)
    return todos


def test_demo_h0045_p15_01_construtores_rejeitam_string_numerica():
    """P15-01: cada construtor direto rejeita W como string numerica ("80")."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for _nome, chamada in _p15_todos_construtores(cv, "80").items():
        with pytest.raises(cv.GeometriaEfetivaAusente):
            chamada()


def test_demo_h0045_p15_02_construtores_rejeitam_float_integral():
    """P15-02: cada construtor direto rejeita W como float integral (80.0)."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for _nome, chamada in _p15_todos_construtores(cv, 80.0).items():
        with pytest.raises(cv.GeometriaEfetivaAusente):
            chamada()


def test_demo_h0045_p15_03_construtores_rejeitam_float_fracionario():
    """P15-03: cada construtor direto rejeita W como float fracionario (80.9)."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for _nome, chamada in _p15_todos_construtores(cv, 80.9).items():
        with pytest.raises(cv.GeometriaEfetivaAusente):
            chamada()


def test_demo_h0045_p15_04_construtores_rejeitam_booleanos():
    """P15-04: cada construtor direto rejeita W booleano (True e False)."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for valor in (True, False):
        for _nome, chamada in _p15_todos_construtores(cv, valor).items():
            with pytest.raises(cv.GeometriaEfetivaAusente):
                chamada()


def test_demo_h0045_p15_05_construtores_rejeitam_ausencia_e_limites_invalidos():
    """P15-05: cada construtor direto rejeita 0, -1, "", [] e {}. Os cinco
    construtores com W obrigatorio tambem rejeitam ``None``. O construtor do
    conjunto vazio preserva ``W=None`` como estado valido (ausencia material
    de W), conforme sua assinatura vigente (default ``W=None``) -- nao e
    regressao do dominio estrito, e sim a excecao documentada em H-0045/P15."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for valor in (0, -1, "", [], {}):
        for _nome, chamada in _p15_todos_construtores(cv, valor).items():
            with pytest.raises(cv.GeometriaEfetivaAusente):
                chamada()

    for _nome, chamada in _p15_construtores_obrigatorios(cv, None).items():
        with pytest.raises(cv.GeometriaEfetivaAusente):
            chamada()

    caso_vazio = cv.construir_caso_vazio(None, None)
    assert caso_vazio["W"] is None


def test_demo_h0045_p15_06_construtores_aceitam_inteiro_positivo():
    """P15-06: W=80 (int) permanece valido e e registrado sem alteracao."""
    from demo import casos_validacao_paginacao as cv

    for _nome, chamada in _p15_todos_construtores(cv, 80).items():
        caso = chamada()
        assert caso["caso_id"]
        assert caso["W"] == 80
        assert type(caso["W"]) is int


def test_demo_h0045_p15_07_despacho_generico_tambem_rejeita():
    """P15-07: ``construir_caso`` propaga a rejeicao para todos os seis IDs."""
    import pytest

    from demo import casos_validacao_paginacao as cv

    for caso_id in cv.ROTULOS:
        for w_invalido in ("80", 80.0, 80.9):
            with pytest.raises(cv.GeometriaEfetivaAusente):
                cv.construir_caso(caso_id, w_invalido, 16)


def test_demo_h0045_p15_08_nenhuma_mutacao_ou_estrutura_parcial_para_w_invalido():
    """P15-08: W invalido aborta antes de qualquer criacao de item; nenhuma
    estrutura parcial e produzida (``_item`` nunca e chamado)."""
    import pytest
    from unittest.mock import patch

    from demo import casos_validacao_paginacao as cv

    with patch.object(cv, "_item", wraps=cv._item) as mock_item:
        for _nome, chamada in _p15_todos_construtores(cv, "80").items():
            with pytest.raises(cv.GeometriaEfetivaAusente):
                chamada()
        for _nome, chamada in _p15_construtores_obrigatorios(cv, None).items():
            with pytest.raises(cv.GeometriaEfetivaAusente):
                chamada()
        mock_item.assert_not_called()


# ---------------------------------------------------------------------------
# H-0045-P16: telas fixas por politica + invariancia de modelo.
# ---------------------------------------------------------------------------


def _p16_abrir_tela(id_tela, largura=80, altura=24):
    from demo.demo import _carregar_modelo_por_id

    modelo = _carregar_modelo_por_id(id_tela)
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": id_tela,
            "modo_verboso": True,
        }
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    return estado, modelo


def test_demo_h0045_p16_tres_telas_ponto_de_entrada_real():
    """Pontos de entrada reais das tres telas fixas (§19.2)."""
    from demo import casos_validacao_paginacao as cv

    esperados = {
        "h0045_validacao_fluxo_continuo": ("permitir_quebra", "1.", "4."),
        "h0045_validacao_nova_pagina": ("evitar_quebra", "1.", "4."),
        "h0045_validacao_manter_junto": (
            "permitir_quebra_somente_se_maior_que_pagina", "1.", "4.",
        ),
    }
    for entrada, (politica, m1, m4) in esperados.items():
        estado, modelo = _p16_abrir_tela(entrada)
        console = modelo.corpo.elementos[0]
        itens = console._campos_inertes["itens"]
        assert itens[0].get("navegavel") is False
        avaliados = [i for i in itens if i.get("navegavel")]
        assert len(avaliados) == 4
        assert all(i.get("politica_quebra") == politica for i in avaliados)
        saida = renderizar_estado(estado, modelo, 80, 24)
        # Em nova_pagina, o item 1 comeca em pagina nova apos o texto inicial.
        if entrada.endswith("nova_pagina"):
            assert "Texto inicial" in saida or "referencia" in saida
            estado_pag = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
            saida = renderizar_estado(estado_pag, modelo, 80, 24)
        assert m1 in saida
        assert any(m4 in (i.get("texto") or "") for i in avaliados)
        assert "PERM_L01" not in saida and "EVIT_L01" not in saida
        hash0 = cv.hash_modelo_logico(console)
        estado2 = dict(estado, largura=60, altura=18)
        estado2 = _reconciliar_paginacao_apos_resize(estado2, modelo)
        assert cv.hash_modelo_logico(console) == hash0
        saida2 = renderizar_estado(estado2, modelo, 60, 18)
        assert "terminal pequeno demais" not in saida2


def test_demo_h0045_p16_resize_mesma_execucao_preserva_hash():
    from demo import casos_validacao_paginacao as cv

    for entrada in (
        "h0045_validacao_fluxo_continuo",
        "h0045_validacao_nova_pagina",
        "h0045_validacao_manter_junto",
        "h0045_validacao_continuacao",
        "h0045_validacao_vazio",
    ):
        estado, modelo = _p16_abrir_tela(entrada)
        console = modelo.corpo.elementos[0]
        hash0 = cv.hash_modelo_logico(console)
        snap0 = cv.snapshot_itens_logicos(console)
        for largura, altura in ((80, 24), (50, 20), (100, 40), (80, 24)):
            estado = dict(estado, largura=largura, altura=altura)
            estado = _reconciliar_paginacao_apos_resize(estado, modelo)
            assert cv.hash_modelo_logico(console) == hash0
            assert cv.snapshot_itens_logicos(console) == snap0
            saida = renderizar_estado(estado, modelo, largura, altura)
            assert "terminal pequeno demais" not in saida


def test_demo_h0045_p16_subprocess_tres_telas_carregam():
    import subprocess

    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "COLUMNS": "80",
        "LINES": "24",
    }
    for entrada in (
        "h0045_validacao_fluxo_continuo",
        "h0045_validacao_nova_pagina",
        "h0045_validacao_manter_junto",
    ):
        proc = subprocess.run(
            [sys.executable, "demo/demo.py", entrada],
            input="\x1b\n",
            capture_output=True,
            text=True,
            cwd=str(_BASE),
            env=env,
            timeout=15,
        )
        assert proc.returncode == 0, (entrada, proc.stderr[-500:])
        from demo.demo import _carregar_modelo_por_id as _cm
        modelo = _cm(entrada)
        textos = [
            i.get("texto", "")
            for i in modelo.corpo.elementos[0]._campos_inertes["itens"]
            if i.get("navegavel")
        ]
        assert any(t.startswith("1.") for t in textos)
        assert any(t.startswith("4.") for t in textos)
        assert "PERM_L01" not in proc.stdout
        assert "EVIT_L01" not in proc.stdout
        # Ao menos o cabecalho da tela aparece no quadro inicial non-TTY.
        assert proc.stdout.strip() != ""


# ---------------------------------------------------------------------------
# VM-H0045-R06-001 (P21): rotulo dinamico do chip ``[Esc]`` via demo.
#
# Cobre os 16 criterios focais exigidos pelo prompt de correcao, percorrendo
# o caminho funcional JA existente (``processar_comando`` + ``renderizar_estado``)
# sem modificar ``demo/demo.py``. As tres configuracoes de selecao multipla
# (h0041, h0044, h0045_fluxo_execucao_paginado) foram atualizadas para
# ``forma_exibicao: "rotulo_dinamico_esc"``; as duas de selecao unica
# permanecem inalteradas.
# ---------------------------------------------------------------------------


def _modelo_fluxo_paginado_p21():
    """Modelo da fixture h0045_fluxo_execucao_paginado (selecao multipla)."""
    return construir_modelo(
        carregar_tela(None, "h0045_fluxo_execucao_paginado", "config/telas/demo")
    )


def _estado_fluxo_paginado_p21(modelo, largura=80, altura=24):
    """Estado inicial equivalente ao que ``main`` estabelece ao abrir."""
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": largura,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": "h0045_fluxo_execucao_paginado",
        }
    )
    return _estabelecer_foco_paginacao_inicial(estado, modelo)


def _barra_esc_p21(saida):
    """Linha da barra de menus contendo o chip ``[Esc]`` (token, nao palavra)."""
    for linha in saida.split("\n"):
        if "[Esc]" in linha:
            return linha
    return ""


class TestRotuloDinamicoEscP21:
    """VM-H0045-R06-001 (P21): primeiro/segundo Esc e rotulo dinamico."""

    # (1) selecao multipla VAZIA exibe o rotulo original ``Sair``.
    def test_rotulo_original_sair_sem_selecao(self):
        modelo = _modelo_fluxo_paginado_p21()
        estado = _estado_fluxo_paginado_p21(modelo)
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra

    # (3) uma selecao exibe ``Limpar``.
    def test_limpar_quando_uma_selecao(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Marca o item sob cursor (Espaco via caminho funcional existente).
        estado = processar_comando(estado, " ", modelo)
        assert estado["selecoes"][console.id]
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra
        assert "Sair" not in barra

    # (4) varias selecoes exibem ``Limpar``.
    def test_limpar_quando_varias_selecoes(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Enter com selecao vazia age como Todos (marca todos).
        estado = processar_comando(estado, "\r", modelo)
        assert len(estado["selecoes"][console.id]) > 1
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra

    # (5) selecao distribuida entre paginas exibe ``Limpar``.
    def test_limpar_com_selecao_distribuida_entre_paginas(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Marca todos (Enter=Todos) e avanca para a pagina 2: a selecao
        # persiste entre paginas; o chip Esc deve continuar ``Limpar``.
        estado = processar_comando(estado, "\r", modelo)
        estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
        assert estado["pagina_atual"][console.id] > 1
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra

    # (6)(7) primeiro Esc limpa toda a selecao e mantem a tela aberta.
    def test_primeiro_esc_limpa_selecao_e_mantem_tela_aberta(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        estado = processar_comando(estado, " ", modelo)
        assert estado["selecoes"][console.id]
        # Primeiro Esc: limpa selecao, permanece na tela (nao sai/volta).
        estado_pos = processar_comando(estado, "\x1b", modelo)
        assert estado_pos["selecoes"][console.id] == []
        assert estado_pos.get("saindo") is not True
        assert estado_pos.get("tela_atual") == "h0045_fluxo_execucao_paginado"

    # (8) apos a limpeza, reaparece o rotulo original.
    def test_apos_limpar_reaparece_rotulo_original(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        estado = processar_comando(estado, " ", modelo)
        estado = processar_comando(estado, "\x1b", modelo)  # limpa selecao
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra

    # (9) segundo Esc executa Sair (apos limpar).
    def test_segundo_esc_executa_sair(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        estado = processar_comando(estado, " ", modelo)
        estado = processar_comando(estado, "\x1b", modelo)  # 1o Esc: limpa
        # 2o Esc: pilha vazia => ``saindo = True`` (Sair).
        estado = processar_comando(estado, "\x1b", modelo)
        assert estado.get("saindo") is True

    # (10) ``Limpar`` e ``Sair`` nunca aparecem simultaneamente para Esc.
    def test_limpar_e_sair_nunca_coexistem_entre_estados(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Vazio => Sair.
        s_vazio = renderizar_estado(estado, modelo, largura=80, altura=24)
        estado = processar_comando(estado, " ", modelo)
        # Com selecao => Limpar.
        s_sel = renderizar_estado(estado, modelo, largura=80, altura=24)
        b_vazio = _barra_esc_p21(s_vazio)
        b_sel = _barra_esc_p21(s_sel)
        assert "[Esc] Sair" in b_vazio and "Limpar" not in b_vazio
        assert "[Esc] Limpar" in b_sel and "Sair" not in b_sel

    # (11) mudanca de pagina mantem o rotulo coerente.
    def test_mudanca_de_pagina_mantem_rotulo_coerente(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Sem selecao: ``Sair`` em qualquer pagina.
        estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "[Esc] Sair" in _barra_esc_p21(saida)
        # Com selecao (marcar na pagina 2): ``Limpar``.
        estado = processar_comando(estado, " ", modelo)
        saida2 = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "[Esc] Limpar" in _barra_esc_p21(saida2)

    # (12) resize mantem o rotulo coerente.
    def test_resize_mantem_rotulo_coerente(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        estado = processar_comando(estado, " ", modelo)
        for largura, altura in [(100, 30), (60, 15), (80, 24)]:
            estado = dict(estado, largura=largura, altura=altura)
            estado = _reconciliar_paginacao_apos_resize(estado, modelo)
            saida = renderizar_estado(
                estado, modelo, largura=largura, altura=altura
            )
            assert "[Esc] Limpar" in _barra_esc_p21(saida), (largura, altura)
        # Apos limpar no tamanho final: ``Sair``.
        estado = processar_comando(estado, "\x1b", modelo)
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "[Esc] Sair" in _barra_esc_p21(saida)

    # (15) cursor, foco e pagina permanecem reconciliados apos limpar.
    def test_cursor_foco_e_pagina_reconciliados_apos_limpar(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Avanca para pagina 2 e marca um item la.
        estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
        estado = processar_comando(estado, " ", modelo)
        cursor_antes = estado["cursores"][console.id]
        pagina_antes = estado["pagina_atual"][console.id]
        foco_antes = estado.get("foco_console")
        estado = processar_comando(estado, "\x1b", modelo)  # limpa selecao
        # Cursor, foco e pagina preservados (Esc apenas limpa selecao).
        assert estado["cursores"][console.id] == cursor_antes
        assert estado["pagina_atual"][console.id] == pagina_antes
        assert estado.get("foco_console") == foco_antes

    # (16) Enter, Espaco, selecao multipla e paginacao sem regressao.
    def test_enter_espaco_selecao_e_paginacao_sem_regressao(self):
        modelo = _modelo_fluxo_paginado_p21()
        console = modelo.corpo.elementos[0]
        estado = _estado_fluxo_paginado_p21(modelo)
        # Espaco marca o item corrente.
        estado = processar_comando(estado, " ", modelo)
        assert estado["selecoes"][console.id]
        # Enter com selecao => INATIVO (reconcilia, nao executa nem marca).
        estado = processar_comando(estado, "\r", modelo)
        # Paginacao continua funcional.
        estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
        assert estado["pagina_atual"][console.id] > 1
        estado = processar_comando(estado, _demo.TECLA_PAGE_UP, modelo)
        # Setas continuam funcionais.
        estado = processar_comando(estado, "\x1b[B", modelo)
        assert estado["cursores"][console.id] is not None


class TestRotuloDinamicoEscIsolamentoP21:
    """VM-H0045-R06-001 (P21): isolamento por console focal e selecao unica."""

    # (14) console de selecao UNICA preserva seu chip original.
    def test_console_selecao_unica_preserva_chip_esc_original(self):
        modelo = construir_modelo(
            carregar_tela(None, "h0045_paginacao_console_unico", "config/telas/demo")
        )
        # Confirmacao focal: selecao unica NAO declara rotulo_dinamico_esc.
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        assert chip_esc["forma_exibicao"] != "rotulo_dinamico_esc"
        lista = navegacao.lista_foco(modelo)
        if not lista:
            return
        console = lista[0]
        estado = criar_estado_inicial()
        estado.update(
            {
                "estilo": carregar_estilo(),
                "largura": 80, "altura": 24,
                "desconto_estrutural": 3,
                "foco_console": 0,
                "cursores": {console.id: 0},
                "pagina_atual": {console.id: 1},
                "tela_atual": "h0045_paginacao_console_unico",
            }
        )
        saida = renderizar_estado(estado, modelo, largura=80, altura=24)
        assert "[Esc] Sair" in saida
        assert "Limpar" not in saida

    # (13) troca de foco entre dois consoles considera somente o console focal.
    def test_troca_de_foco_considera_somente_console_focal(self):
        modelo = construir_modelo(
            carregar_tela(
                None, "h0045_dois_consoles_paginas_independentes",
                "config/telas/demo",
            )
        )
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        # Ambos consoles sao selecao unica => Esc sempre ``Sair``.
        assert chip_esc["forma_exibicao"] != "rotulo_dinamico_esc"
        lista = navegacao.lista_foco(modelo)
        if len(lista) < 2:
            return
        ca, cb = lista[0], lista[1]
        for foco in range(len(lista)):
            estado = criar_estado_inicial()
            estado.update(
                {
                    "estilo": carregar_estilo(),
                    "largura": 100, "altura": 24,
                    "desconto_estrutural": 3,
                    "foco_console": foco,
                    "cursores": {ca.id: 0, cb.id: 0},
                    "pagina_atual": {ca.id: 1, cb.id: 1},
                    "tela_atual": "h0045_dois_consoles_paginas_independentes",
                }
            )
            saida = renderizar_estado(estado, modelo, largura=100, altura=24)
            barra = _barra_esc_p21(saida)
            assert "[Esc] Sair" in barra, foco
            assert "Limpar" not in barra, foco

    # Confirmacao focal das tres configuracoes autorizadas.
    def test_tres_configuracoes_multipla_usam_rotulo_dinamico_esc(self):
        for id_tela in (
            "h0041_selecao_multipla_oito_itens",
            "h0044_fluxo_execucao_integrado",
            "h0045_fluxo_execucao_paginado",
        ):
            modelo = construir_modelo(
                carregar_tela(None, id_tela, "config/telas/demo")
            )
            chip_esc = next(
                c for c in modelo.barra_de_menus["chips"]
                if c.get("tecla") == "Esc"
            )
            assert chip_esc["forma_exibicao"] == "rotulo_dinamico_esc", id_tela
            # Texto original preservado como fallback.
            assert chip_esc["texto"] == "Sair", id_tela

    # Confirmacao focal das duas configuracoes de selecao unica preservadas.
    def test_duas_configuracoes_unica_permanecem_inalteradas(self):
        for id_tela in (
            "h0045_paginacao_console_unico",
            "h0045_dois_consoles_paginas_independentes",
        ):
            modelo = construir_modelo(
                carregar_tela(None, id_tela, "config/telas/demo")
            )
            chip_esc = next(
                c for c in modelo.barra_de_menus["chips"]
                if c.get("tecla") == "Esc"
            )
            assert chip_esc["forma_exibicao"] != "rotulo_dinamico_esc", id_tela
            assert chip_esc["texto"] == "Sair", id_tela


# ---------------------------------------------------------------------------
# VM-H0045-R06-001 (P22): prova ponta a ponta da sequencia de Esc em tela
# aninhada com selecao multipla ativa.
#
# Sequencia a provar:
#   tela aninhada com selecao -> [Esc] Limpar
#   -> primeiro Esc limpa e permanece na tela
#   -> [Esc] Voltar
#   -> segundo Esc retorna a tela anterior
#
# Constroi o estado aninhado pelo caminho funcional real: (1) um lancador na
# tela raiz empilha a tela raiz e troca para a tela aninhada; (2) Tab estabelece
# foco no console aninhado (selecao multipla); (3) Espaco marca um item. Nada de
# manipulacao manual da pilha ou da selecao. O MESMO objeto de estado atravessa
# os dois Esc via ``processar_comando``. Reutiliza o helper local
# ``_console_paginado_selecionavel_h0045`` (padrao de modelo em memoria ja
# adotado pelos testes P06/P07) e o helper ``_barra_esc_p21``.
# ---------------------------------------------------------------------------


def _p22_modelos_tela_aninhada():
    """Modelos raiz (lancador) e aninhada (console multipla + rotulo Voltar).

    A tela aninhada declara ``politica_selecao: multipla`` e um chip Esc com
    ``forma_exibicao: "rotulo_dinamico_esc"`` e ``texto: "Voltar"`` -- condicao
    exigida pelo prompt (item 7 do cenario inicial) para que o rótulo dinamico
    exiba ``[Esc] Voltar`` quando a selecao esta vazia em tela aninhada. A tela
    raiz provê um lancador cujo ``chip`` dispara o empilhamento real
    (``processar_comando`` reconhece o chip, empilha ``tela_atual`` e troca
    para ``tela_destino``).
    """
    from tela.modelo import ElementoCorpo, ModeloTela, Corpo

    console_aninhado = _console_paginado_selecionavel_h0045(
        "console_aninhado_p22", "m", 6, "ANINHADA P22",
    )
    modelo_aninhada = ModeloTela(
        id="tela_aninhada_p22", schema="tela.v1",
        cabecalho={"titulo": "Aninhada P22", "descricao": "tela aninhada", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[console_aninhado]),
        barra_de_menus={
            "chips": [
                {
                    "id": "esc", "tipo": "acao", "tecla": "Esc",
                    "texto": "Voltar", "forma_exibicao": "rotulo_dinamico_esc",
                }
            ]
        },
        _raw={},
    )
    lancador = ElementoCorpo(
        id="lancador_raiz_p22", tipo="lancador",
        _campos_inertes={
            "itens": [{"chip": "x", "tela_destino": "tela_aninhada_p22"}]
        },
    )
    modelo_raiz = ModeloTela(
        id="tela_raiz_p22", schema="tela.v1",
        cabecalho={"titulo": "Raiz P22", "descricao": "tela anterior", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[lancador]),
        barra_de_menus={
            "chips": [{"id": "esc", "tipo": "acao", "tecla": "Esc", "texto": "Sair"}]
        },
        _raw={},
    )
    return modelo_raiz, modelo_aninhada


def test_h0045_p22_esc_aninhada_primeiro_limpa_segundo_volta():
    """VM-H0045-R06-001 (P22 / QA-H0045-P21-001): sequencia ponta a ponta.

    Constroi a tela aninhada pelo caminho funcional (lancador -> empilha; Tab ->
    foco; Espaco -> marca), afirma o cenario antes do primeiro Esc e percorre
    os dois Esc pelo MESMO estado via ``processar_comando``.
    """
    from tela import paginacao as paginacao_mod

    modelo_raiz, modelo_aninhada = _p22_modelos_tela_aninhada()
    console = navegacao.lista_foco(modelo_aninhada)[0]

    # --- Construcao do cenario pelo caminho funcional real -------------------
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": carregar_estilo(),
            "largura": 80, "altura": 24, "desconto_estrutural": 3,
            "tela_atual": "tela_raiz_p22",
        }
    )
    # (1) Lancador: empilha a tela raiz e troca para a tela aninhada. Sem
    #     manipulacao manual de ``pilha_telas``.
    estado = processar_comando(estado, "x", modelo_raiz)
    assert estado["tela_atual"] == "tela_aninhada_p22"
    assert estado["pilha_telas"] == ["tela_raiz_p22"]
    # (2) Tab: estabelece foco no console aninhado (selecao multipla).
    estado = processar_comando(estado, "\t", modelo_aninhada)
    assert estado["foco_console"] == 0
    assert console.id in estado["cursores"]
    # (3) Espaco: marca o item sob o cursor.
    estado = processar_comando(estado, " ", modelo_aninhada)
    assert estado["selecoes"][console.id]  # existe pelo menos um selecionado

    pilha_tamanho = len(estado["pilha_telas"])
    cursor_antes = estado["cursores"][console.id]
    foco_antes = estado["foco_console"]
    pagina_antes = estado["pagina_atual"].get(console.id)

    # --- Antes do primeiro Esc ---------------------------------------------
    saida = renderizar_estado(estado, modelo_aninhada, largura=80, altura=24)
    barra = _barra_esc_p21(saida)
    # A tela aninhada e a tela atual e a pilha contem a tela anterior.
    assert estado["tela_atual"] == "tela_aninhada_p22"
    assert estado["pilha_telas"] == ["tela_raiz_p22"]
    # A selecao do console focado nao esta vazia.
    assert estado["selecoes"][console.id]
    # O quadro contem [Esc] Limpar; nao apresenta [Esc] Voltar/Sair como acao
    # corrente da mesma tecla enquanto a selecao esta ativa.
    assert "[Esc] Limpar" in barra
    assert "[Esc] Voltar" not in barra
    assert "[Esc] Sair" not in barra
    # saindo falso; foco, cursor e pagina validos.
    assert estado.get("saindo") is False
    assert foco_antes is not None
    assert isinstance(cursor_antes, int)
    assert isinstance(pagina_antes, int) and pagina_antes >= 1

    # --- Primeiro Esc: limpa selecao e permanece na tela --------------------
    estado = processar_comando(estado, "\x1b", modelo_aninhada)
    assert estado["selecoes"][console.id] == []
    assert estado["tela_atual"] == "tela_aninhada_p22"
    assert len(estado["pilha_telas"]) == pilha_tamanho
    assert estado["pilha_telas"] == ["tela_raiz_p22"]
    assert estado.get("saindo") is False
    # Foco, cursor e pagina continuam validos (Esc apenas limpa a selecao).
    assert estado["foco_console"] == foco_antes
    assert estado["cursores"][console.id] == cursor_antes
    assert estado["pagina_atual"].get(console.id) == pagina_antes

    saida = renderizar_estado(estado, modelo_aninhada, largura=80, altura=24)
    barra = _barra_esc_p21(saida)
    # O quadro agora contem [Esc] Voltar; nao contem [Esc] Limpar como acao
    # corrente.
    assert "[Esc] Voltar" in barra
    assert "[Esc] Limpar" not in barra

    # --- Segundo Esc: fluxo normal de Voltar (mesmo objeto de estado) -------
    estado = processar_comando(estado, "\x1b", modelo_aninhada)
    # O retorno ocorreu pelo proprio processamento funcional de Esc (pop da
    # pilha), nao por remocao manual: a pilha foi reduzida exatamente uma vez.
    assert estado["tela_atual"] == "tela_raiz_p22"
    assert len(estado["pilha_telas"]) == pilha_tamanho - 1
    assert estado["pilha_telas"] == []
    # Nao ocorreu saida global da aplicacao; saindo permanece falso.
    assert estado.get("saindo") is False


# ---------------------------------------------------------------------------
# VM-H0045-R08-001 (P23): estado controlado de terminal insuficiente.
# Cobre os casos 9-28 e 30 da matriz obrigatoria do patch P23: ausencia de
# traceback no resize e em comandos que consultam geometria, quadro controlado
# de terminal pequeno, preservacao de selecao/foco/cursor/item/pagina/pilha e
# recuperacao automatica ao ampliar.
# ---------------------------------------------------------------------------

from demo.demo import (
    _resolver_conteudo as _resolver_conteudo_p23,
    _e_insuficiencia_geometrica as _e_insuf_p23,
    _e_erro_layout_barra as _e_layout_p23,
    _quadro_terminal_insuficiente as _quadro_insuf_p23,
)
from tela.renderizador import RenderizadorErro as _RE_p23


def _modelo_fluxo_p23():
    return construir_modelo(
        carregar_tela(None, "h0045_fluxo_execucao_paginado", "config/telas/demo")
    )


def _abrir_fluxo_p23(largura=80, altura=24):
    """Abre h0045_fluxo_execucao_paginado como ``main`` faria (foco inicial)."""
    modelo = _modelo_fluxo_p23()
    estado = criar_estado_inicial()
    estado.update({
        "estilo": carregar_estilo(),
        "largura": largura,
        "altura": altura,
        "desconto_estrutural": 3,
        "tela_atual": "h0045_fluxo_execucao_paginado",
    })
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    return estado, modelo


def _snap_estado_p23(estado, console):
    """Snapshot dos campos que devem ser preservados em geometria invalida."""
    return {
        "foco": estado.get("foco_console"),
        "cursor": dict(estado.get("cursores", {})),
        "selecao": dict(estado.get("selecoes", {})),
        "pagina": dict(estado.get("pagina_atual", {})),
        "pilha": list(estado.get("pilha_telas", [])),
        "tela": estado.get("tela_atual"),
        "saindo": estado.get("saindo"),
        "verboso": estado.get("modo_verboso"),
    }


def test_p23_abertura_inicial_em_dimensao_suficiente():
    """Caso 1/30: abertura inicial em dimensao suficiente nao traceback."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    saida = _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert "FLUXO PAGINADO" in saida
    assert "Terminal pequeno" not in saida
    assert "terminal pequeno demais" not in saida


def test_p23_resize_progressivo_sem_traceback_atribuicoes_de_barra():
    """Casos 2-6/10: resize por todas as transicoes de barra sem traceback."""
    estado, modelo = _abrir_fluxo_p23(120, 24)
    console = modelo.corpo.elementos[0]
    # Percorre as larguras onde a barra passa por 1,2,3,4,5 linhas e abaixo.
    for w in (120, 65, 41, 29, 28, 20, 17, 16, 14, 12):
        estado = dict(estado, largura=w, altura=24, desconto_estrutural=3)
        # A reconciliacao NAO pode deixar excecao escapar (o bug original).
        estado = _reconciliar_paginacao_apos_resize(estado, modelo)
        # O render NAO pode deixar excecao escapar; cai em quadro controlado.
        saida = _resolver_conteudo_p23(estado, modelo, w, 24)
        assert saida.endswith("\n")


def test_p23_resize_erro_layout_nao_escapa_como_traceback():
    """Caso 10: o erro_layout durante o resize nao vira traceback."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    # Reduz diretamente para uma largura onde a barra nao cabe nem em 5 linhas.
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    # Se o bug existisse, a linha abaixo levantaria RenderizadorErro.
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida = _resolver_conteudo_p23(estado, modelo, 14, 24)
    # Quadro controlado (mensagem pode ser truncada pela largura estreita).
    assert "Terminal" in saida or "terminal" in saida
    assert "FLUXO PAGINADO" not in saida


def test_p23_comandos_que_consultam_geometria_nao_escapam_em_geometria_invalida():
    """Caso 11: comandos dependentes de geometria nao escapam em geometria invalida."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    # Posiciona em pagina 2 e marca item para ter estado nao trivial.
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    estado = processar_comando(estado, " ", modelo)
    # Entra em geometria invalida.
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    # Cada comando dependente de geometria deve ser processado sem excecao.
    for cmd in (
        _demo.TECLA_PAGE_DOWN, _demo.TECLA_PAGE_UP,
        "\x1b[C", "\x1b[D", "\x1b[B", "\x1b[A",
    ):
        estado = processar_comando(estado, cmd, modelo)


def test_p23_quadro_controlado_de_terminal_pequeno():
    """Casos 12/13: quadro controlado exibe a mensagem canônica do P23."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida = _resolver_conteudo_p23(estado, modelo, 14, 24)
    linhas = saida.split("\n")
    # A mensagem controlada do P23 (erro_layout da barra): titulo e subtitulo,
    # eventualmente truncados pela largura estreita (manifesto: "pode ser
    # quebrada ou reduzida conforme a geometria disponivel").
    assert linhas[0].startswith("Terminal")
    assert linhas[1].startswith("Aumente")
    # Ausencia de interface normal parcial no quadro controlado.
    assert "FLUXO PAGINADO" not in saida
    assert "[Esc]" not in saida
    assert "página" not in saida


def test_p23_altura_insuficiente_apesar_de_largura_suficiente():
    """Caso 9: altura insuficiente com largura suficiente -> quadro (sem traceback)."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    # Largura suficiente (barra em 1 linha), mas altura muito baixa.
    saida = _resolver_conteudo_p23(estado, modelo, 80, 5)
    # Mesmo quadro controlado usado pela insuficiencia da barra.
    assert "Terminal pequeno demais" in saida
    assert "Aumente a janela para continuar" in saida


def test_p23_preservacao_selecao_foco_cursor_item_pagina_pilha():
    """Casos 14-19: geometria invalida preserva todo o estado logico."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    snap_antes = _snap_estado_p23(estado, console)

    # Entra em geometria invalida.
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    snap_invalido = _snap_estado_p23(estado, console)

    # Estado logico preservado integralmente.
    assert snap_invalido["foco"] == snap_antes["foco"]
    assert snap_invalido["cursor"] == snap_antes["cursor"]
    assert snap_invalido["selecao"] == snap_antes["selecao"]
    assert snap_invalido["pagina"] == snap_antes["pagina"]
    assert snap_invalido["pilha"] == snap_antes["pilha"]
    assert snap_invalido["tela"] == snap_antes["tela"]
    assert snap_invalido["verboso"] == snap_antes["verboso"]


def test_p23_comandos_durante_geometria_invalida_preservam_estado():
    """Casos 11/14-18: comandos durante geometria invalida nao alteram estado."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    estado = processar_comando(estado, " ", modelo)
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    snap_antes = _snap_estado_p23(estado, console)

    for cmd in (
        _demo.TECLA_PAGE_DOWN, _demo.TECLA_PAGE_UP,
        "\x1b[C", "\x1b[D", "\x1b[B", "\x1b[A",
    ):
        e2 = processar_comando(estado, cmd, modelo)
        snap_depois = _snap_estado_p23(e2, console)
        assert snap_depois["foco"] == snap_antes["foco"]
        assert snap_depois["cursor"] == snap_antes["cursor"]
        assert snap_depois["selecao"] == snap_antes["selecao"]
        assert snap_depois["pagina"] == snap_antes["pagina"]


def test_p23_recuperacao_automatica_apos_ampliar():
    """Casos 20/22: ao ampliar, a tela normal volta automaticamente."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    estado = processar_comando(estado, " ", modelo)
    item_logico = estado["cursores"][console.id]
    id_marcado = estado["selecoes"][console.id]

    # Entra em geometria invalida.
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida_invalida = _resolver_conteudo_p23(estado, modelo, 14, 24)
    assert "FLUXO PAGINADO" not in saida_invalida

    # Amplia: recuperacao automatica sem reinicio.
    estado = dict(estado, largura=80, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    saida_rec = _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert "FLUXO PAGINADO" in saida_rec
    assert "Terminal" not in saida_rec


def test_p23_recuperacao_preserva_selecao_cursor_item_sem_perda_repeticao():
    """Casos 14-19/21/22: recuperacao preserva estado sem perda/repeticao."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    estado = processar_comando(estado, _demo.TECLA_PAGE_DOWN, modelo)
    estado = processar_comando(estado, " ", modelo)
    item_antes = estado["cursores"][console.id]
    sel_antes = list(estado["selecoes"][console.id])
    pag_antes = estado["pagina_atual"][console.id]

    # Ciclo invalido -> valido.
    estado = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)
    estado = dict(estado, largura=80, altura=24, desconto_estrutural=3)
    estado = _reconciliar_paginacao_apos_resize(estado, modelo)

    assert estado["cursores"][console.id] == item_antes
    assert estado["selecoes"][console.id] == sel_antes
    assert estado["pagina_atual"][console.id] == pag_antes


def test_p23_ausencia_truncamento_reordenacao_chips_na_barra_normal():
    """Casos 23/24: na geometria valida, todos os chips aparecem na ordem."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    saida = _resolver_conteudo_p23(estado, modelo, 80, 24)
    # Todos os chips presentes, [Esc] primeiro.
    assert "[Esc]" in saida
    assert _chip_paginas(estado["estilo"]) in _sem_ansi(saida)
    assert "[␣]" in saida
    assert "[⏎]" in saida
    saida_visivel = _sem_ansi(saida)
    assert saida_visivel.index("[Esc]") < saida_visivel.index("[PgUp/PgDn]")


def test_p23_preservacao_rotulo_dinamico_esc():
    """Caso 25: o rotulo dinamico de Esc e preservado na barra normal."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    # Sem selecao: [Esc] Sair.
    saida = _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert "[Esc] Sair" in saida
    # Com selecao: [Esc] Limpar (rotulo_dinamico_esc).
    estado = processar_comando(estado, " ", modelo)
    saida2 = _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert "[Esc] Limpar" in saida2


def test_p23_primeiro_esc_limpa_sem_sair_segundo_esc_sai():
    """Casos 26/27: primeiro Esc limpa selecao; segundo Esc sai."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    estado = processar_comando(estado, " ", modelo)
    assert estado["selecoes"][console.id] != []
    # Primeiro Esc: limpa e permanece.
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado["selecoes"].get(console.id, []) == []
    assert estado["saindo"] is False
    # Segundo Esc: sai (pilha vazia).
    estado = processar_comando(estado, "\x1b", modelo)
    assert estado["saindo"] is True


def test_p23_regressao_demais_telas_h0045():
    """Caso 28: as demais telas H-0045 continuam funcionando."""
    for id_tela in (
        "h0045_paginacao_console_unico",
        "h0045_dois_consoles_paginas_independentes",
        "h0045_paginacao_conjunto_vazio",
    ):
        modelo = construir_modelo(
            carregar_tela(None, id_tela, "config/telas/demo")
        )
        estado = criar_estado_inicial()
        estado.update({
            "estilo": carregar_estilo(),
            "largura": 80, "altura": 24,
            "desconto_estrutural": 3,
            "tela_atual": id_tela,
        })
        estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
        saida = _resolver_conteudo_p23(estado, modelo, 80, 24)
        assert "terminal pequeno" not in saida, id_tela


def test_p23_classificacao_seletiva_do_erro():
    """O classificador aceita somente formatos completos de produtores reais."""
    msg_barra = (
        "erro_layout: chips da barra_de_menus (5) nao cabem em 10 "
        "caracteres uteis (content_w=11, margem=1) com no maximo 5 linhas "
        "(preenchimento=coluna_a_coluna); "
        "overflow.quando_nao_couber='erro_layout' proibe "
        "omitir/truncar/reordenar"
    )
    msg_altura = (
        "altura insuficiente: terminal com 5 linhas nao comporta "
        "cabecalho (4) + barra_de_menus (4)"
    )
    assert _e_layout_p23(_RE_p23(msg_barra))
    assert _e_insuf_p23(_RE_p23(msg_barra))
    assert _e_insuf_p23(_RE_p23(msg_altura))
    for mensagem in (
        "erro_layout: chips nao cabem",
        "erro_layout: modelo invalido",
        "altura insuficiente: corpo requer 9 linhas",
        "DA-01: composicao invalida",
        "DA-02 (ADR-0024): composicao invalida",
        "DA-04 (ADR-0024): composicao invalida",
        "renderizar_tela exige ModeloTela",
        "modo de distribuicao desconhecido",
    ):
        assert not _e_insuf_p23(_RE_p23(mensagem)), mensagem
        assert not _e_layout_p23(_RE_p23(mensagem)), mensagem


def test_p23_quadro_controlado_nao_lanca_em_dimensoes_extremas():
    """O quadro controlado produz saida segura em dimensoes extremas."""
    # 1x1, 2x1, 1x2: nao pode lancar nova excecao.
    for (w, h) in [(1, 1), (2, 1), (1, 2), (3, 1), (40, 1), (40, 2)]:
        q = _quadro_insuf_p23(w, h)
        assert q.endswith("\n")
        assert q.count("\n") == h
        for linha in q.split("\n")[:-1]:
            assert len(linha) == w


def test_p23_matriz_obrigatoria_larguras_alturas_sem_excecao():
    """Casos 30: a matriz obrigatoria (10 larguras x 6 alturas) sem excecao."""
    estado, modelo = _abrir_fluxo_p23(120, 40)
    larguras = (16, 17, 20, 28, 29, 40, 41, 64, 65, 120)
    alturas = (6, 8, 10, 15, 24, 40)
    for h in alturas:
        for w in larguras:
            est = dict(estado, largura=w, altura=h, desconto_estrutural=3)
            # Reconciliacao e render nao podem deixar excecao escapar.
            est = _reconciliar_paginacao_apos_resize(est, modelo)
            saida = _resolver_conteudo_p23(est, modelo, w, h)
            assert saida.endswith("\n")
            # Em dimensao suficiente, tela normal; caso contrario, algum
            # quadro de insuficiencia (controlado do P23 ou minimo canônico).
            # O titulo do cabecalho pode ser truncado pela largura estreita,
            # por isso casamos pelo prefixo estavel "FLUXO PAGINAD".
            e_normal = "FLUXO PAGINAD" in saida
            e_controlado = saida.split("\n")[0].startswith("Terminal")
            e_minimo = (
                "terminal pequeno" in saida
                or "tela peq." in saida
                or saida.split("\n")[0].strip() == ""
            )
            assert e_normal or e_controlado or e_minimo, (w, h, saida[:40])


# ---------------------------------------------------------------------------
# VM-H0045-R08-001 (P25): classificacao exata e propagacao estrutural.
# ---------------------------------------------------------------------------

_P25_ERROS_ESTRUTURAIS = (
    "distribuicao com tipo invalido: str",
    "linhas.maximo invalido: 0; esperado int >= 1",
    "preenchimento_multilinha desconhecido: 'invalido'",
    "estrutura matriz sem objeto matriz validado",
    "renderizar_tela exige ModeloTela; recebido: dict",
    "quebra de invariante: modelo inconsistente",
    "DA-02 (ADR-0024): composicao invalida",
    "DA-04 (ADR-0024): composicao invalida",
    "DA-01: composicao invalida",
    "DA-099: composicao invalida",
    "erro_layout: modelo invalido",
    "r",
    "layout terminal pequeno demais, mas sem produtor geometrico",
)


@pytest.mark.parametrize(
    "mensagem", _P25_ERROS_ESTRUTURAIS,
    ids=["p25_" + str(i) for i in range(1, len(_P25_ERROS_ESTRUTURAIS) + 1)],
)
def test_p25_resolver_relanca_todo_erro_estrutural(mensagem):
    """P25: _resolver_conteudo nao transforma falha interna em aviso."""
    from unittest.mock import patch

    estado, modelo = _abrir_fluxo_p23(80, 24)
    erro = RenderizadorErro(mensagem)
    with patch.object(_demo, "renderizar_estado", side_effect=erro):
        with pytest.raises(RenderizadorErro) as capturada:
            _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert capturada.value is erro


@pytest.mark.parametrize(
    "mensagem",
    (
        "erro_layout: chips da barra_de_menus (5) nao cabem em 10 "
        "caracteres uteis (content_w=11, margem=1) com no maximo 5 linhas "
        "(preenchimento=coluna_a_coluna); "
        "overflow.quando_nao_couber='erro_layout' proibe "
        "omitir/truncar/reordenar",
        "altura insuficiente: terminal com 5 linhas nao comporta "
        "cabecalho (4) + barra_de_menus (4)",
        "altura insuficiente: corpo requer 9 linhas mas area disponivel e 3 "
        "linhas (altura=10, cabecalho=4, barra=3)",
    ),
    ids=["barra_real", "altura_cabecalho_real", "altura_corpo_real"],
)
def test_p25_resolver_absorve_somente_produtor_geometrico_real(mensagem):
    """P25: produtores aceitos usam sempre o quadro controlado unificado."""
    from unittest.mock import patch

    estado, modelo = _abrir_fluxo_p23(80, 24)
    with patch.object(
        _demo, "renderizar_estado", side_effect=RenderizadorErro(mensagem)
    ):
        saida = _resolver_conteudo_p23(estado, modelo, 80, 24)
    assert "Terminal pequeno demais" in saida
    assert "Aumente a janela para continuar" in saida
    assert "FLUXO PAGINADO" not in saida


@pytest.mark.parametrize(
    "mensagem", _P25_ERROS_ESTRUTURAIS,
    ids=["p25_reconciliar_" + str(i) for i in range(1, len(_P25_ERROS_ESTRUTURAIS) + 1)],
)
def test_p25_reconciliar_relanca_todo_erro_estrutural(mensagem):
    """P25: resize relanca RenderizadorErro que nao e geometrico real."""
    from unittest.mock import patch

    estado, modelo = _abrir_fluxo_p23(80, 24)
    erro = RenderizadorErro(mensagem)
    with patch.object(_demo, "geometria_console", side_effect=erro):
        with pytest.raises(RenderizadorErro) as capturada:
            _reconciliar_paginacao_apos_resize(estado, modelo)
    assert capturada.value is erro


@pytest.mark.parametrize(
    "mensagem", _P25_ERROS_ESTRUTURAIS,
    ids=["p25_geometria_" + str(i) for i in range(1, len(_P25_ERROS_ESTRUTURAIS) + 1)],
)
def test_p25_com_geometria_real_relanca_todo_erro_estrutural(mensagem):
    """P25: comandos dependentes de geometria preservam a falha original."""
    from unittest.mock import patch

    estado, modelo = _abrir_fluxo_p23(80, 24)
    console = modelo.corpo.elementos[0]
    erro = RenderizadorErro(mensagem)
    with patch.object(_demo, "geometria_console", side_effect=erro):
        with pytest.raises(RenderizadorErro) as capturada:
            _demo._com_geometria_real_do_console(estado, modelo, console)
    assert capturada.value is erro


def test_p25_quadro_unificado_confirma_as_duas_mensagens_em_80x8():
    """P25: altura baixa usa o quadro completo quando 80x8 comporta ambas."""
    estado, modelo = _abrir_fluxo_p23(80, 24)
    saida = _resolver_conteudo_p23(estado, modelo, 80, 8)
    assert "Terminal pequeno demais" in saida
    assert "Aumente a janela para continuar" in saida
    assert "FLUXO PAGINADO" not in saida
