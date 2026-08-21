"""Demonstracao H-0073 da tela H-0063 reconciliada pelo ponto de entrada real.

Prova que ``h0063_estilo_estrutura_navegacao_dois_niveis`` e carregada e
renderizada por ``demo/demo.py`` (carregamento estrutural, injecao da
projecao dinamica, ``processar_comando``/``renderizar_estado``), nunca
apenas por chamada direta ao renderer.

Executavel via:
    python demo/teste_demo_h0073_h0063_reconciliado.py

Apenas biblioteca padrao do Python + pytest.
"""

import re
import sys
from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from demo.demo import (  # noqa: E402
    _ID_TELA_H0063,
    _anexar_tela_estilo,
    _carregar_modelo_por_id,
    _preparar_estado_estilo,
    _preparar_modelo_estilo,
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
)
from tela.estilo import CATEGORIAS_ESTILO  # noqa: E402
from tela.loader import RuntimeEstilo  # noqa: E402
from tela import navegacao  # noqa: E402
from tela.renderizacao.estilo import amostra_de_preset  # noqa: E402
from tela.renderizacao.conteudo_externo import (  # noqa: E402
    _linhas_dois_niveis_formatado_com_mapa,
)

_ID_TELA = _ID_TELA_H0063
_CAMINHO_ESTRUTURAL = (
    _BASE_PADRAO / "config" / "telas" / "demo"
    / "h0063_estilo_estrutura_navegacao_dois_niveis.json"
)


def _sem_ansi(texto):
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def _miolo(linha):
    return linha.split("│", 1)[1] if "│" in linha else linha


def _coluna_cursor(quadro):
    for linha in quadro.splitlines():
        miolo = _miolo(linha)
        if "→" in miolo:
            return miolo.index("→")
    raise AssertionError("cursor ausente")


def _abrir():
    runtime = RuntimeEstilo()
    estado = dict(
        criar_estado_inicial(),
        estilo_runtime=runtime,
        estilo=runtime.global_vigente,
        tela_atual=_ID_TELA,
        largura=120,
        altura=40,
    )
    modelo = _carregar_modelo_por_id(_ID_TELA)
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)
    estado = processar_comando(estado, "", modelo)
    return estado, modelo


def teste_carregamento_via_ponto_de_entrada_real():
    estado, modelo = _abrir()
    assert modelo.id == _ID_TELA
    console = navegacao.lista_foco(modelo)[0]
    assert console.id == "console_h0063_estilo"
    config = console.formato_filho_dois_niveis
    assert config["tabulacao"] == {"minimo": 5, "maximo": 10}
    assert config["designador"]["tipo"] == "nenhum"
    assert config["apresentacao"] == "tabela"
    assert [c["campo"] for c in config["tabela"]["colunas"]] == [
        "preset", "amostra",
    ]
    assert config["tabela"]["espacamento"] == {"minimo": 3, "maximo": 8}
    bruto = _CAMINHO_ESTRUTURAL.read_text(encoding="utf-8")
    assert '"campo": "preset"' in bruto
    assert '"campo": "amostra"' in bruto


def teste_projecao_dinamica_expoe_preset_e_amostra():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    assert tuple(p.nome for p in controlador.pais) == CATEGORIAS_ESTILO
    for categoria in controlador.categorias:
        for preset in categoria.presets:
            no = next(
                filho for pai in controlador.conteudo.nos
                for filho in pai.filhos
                if filho.campos.get("preset") == preset.nome
                and filho.campos.get("categoria") == categoria.nome
            )
            assert no.campos["preset"] == preset.nome
            assert no.campos["titulo"]
            assert no.campos["amostra"] == amostra_de_preset(
                categoria.nome, preset.dados
            )


def teste_saida_fisica_tabela_duas_colunas_sem_designador_com_alinhamento():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    quadro = _sem_ansi(renderizar_estado(estado, modelo, largura=120, altura=40))
    assert "(console)" not in quadro
    for nome in CATEGORIAS_ESTILO:
        assert nome in quadro

    filho_borda = next(
        filho for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if pai.campos.get("categoria") == "borda"
    )
    filho_chip = next(
        filho for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if pai.campos.get("categoria") == "chip"
    )
    amostra_borda = _sem_ansi(filho_borda.campos["amostra"])
    amostra_chip = _sem_ansi(filho_chip.campos["amostra"])
    linha_borda = next(
        linha for linha in quadro.splitlines()
        if filho_borda.campos["preset"] in _miolo(linha)
        and amostra_borda in _miolo(linha)
    )
    linha_chip = next(
        linha for linha in quadro.splitlines()
        if filho_chip.campos["preset"] in _miolo(linha)
        and amostra_chip in _miolo(linha)
    )
    miolo_borda = _miolo(linha_borda)
    miolo_chip = _miolo(linha_chip)
    assert "A)" not in miolo_borda
    assert "B)" not in miolo_borda
    coluna_pai = _coluna_cursor(quadro)
    filhos = processar_comando(estado, " ", modelo)
    quadro_filhos = _sem_ansi(renderizar_estado(filhos, modelo, largura=120, altura=40))
    coluna_filho = _coluna_cursor(quadro_filhos)
    assert 5 <= coluna_filho - coluna_pai <= 10
    assert miolo_borda.index(amostra_borda) == miolo_chip.index(amostra_chip)
    assert miolo_borda.index(filho_borda.campos["preset"]) == miolo_chip.index(
        filho_chip.campos["preset"]
    )


def teste_navegacao_e_selecao_pelo_fluxo_real():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    console = controlador.console_do_modelo(modelo)
    iniciais = list(estado["selecoes"][console.id])
    assert len(iniciais) == 4
    filhos = processar_comando(estado, " ", modelo)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    movido = processar_comando(filhos, "\x1b[B", modelo)
    assert movido["cursores"][console.id] != filhos["cursores"][console.id]
    assert movido["selecoes"][console.id] == iniciais
    quadro = _sem_ansi(renderizar_estado(movido, modelo, largura=120, altura=40))
    assert "(console)" not in quadro
    retorno = processar_comando(movido, "\x1b", modelo)
    assert navegacao.em_nivel_filhos(retorno, console) is False
    assert retorno["selecoes"][console.id] == iniciais


def teste_resize_real_da_tabela_reduz_tabulacao_preserva_colunas_e_espacamento():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    console = controlador.console_do_modelo(modelo)
    corrente = next(
        filho.id for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if pai.campos.get("categoria") == "borda"
    )
    # A largura visual maxima da amostra ANSI e 3, enquanto a maior amostra
    # de borda ocupa 8 colunas. As larguras globais corrigidas produzem 10,
    # 9 e 5 sem contar os bytes SGR como colunas; 39 e a regressao explicita
    # contra a compactacao prematura do P02 (10 ainda cabe com gap 3).
    larguras = (51, 39, 38, 34)
    recuos = []
    ids = []
    linhas = []
    for content_w in larguras:
        entradas = _linhas_dois_niveis_formatado_com_mapa(
            controlador.conteudo,
            console.formato_filho_dois_niveis,
            content_w=content_w,
            no_corrente_id=corrente,
            indicador="→",
            indicador_off=" ",
            selecoes=set(controlador.ids_escolha_inicial),
            incluir_selecao=True,
            incluido_on="●",
            incluido_off="○",
        )
        ids.append([entrada["id"] for entrada in entradas])
        linha = next(
            entrada["linhas"][0] for entrada in entradas
            if entrada["id"] == corrente
        )
        linhas.append(_sem_ansi(linha))
        recuos.append(len(linha) - len(linha.lstrip(" ")))

    assert recuos == [10, 10, 9, 5]
    assert all(5 <= recuo <= 10 for recuo in recuos)
    assert all(anterior >= atual for anterior, atual in zip(recuos, recuos[1:]))
    assert ids[0] == ids[1] == ids[2]
    assert all("A)" not in linha and "1.1" not in linha for linha in linhas)
    assert all("Borda Curva" in linha and "╭─╮││╰─╯" in linha for linha in linhas)

    destaque = next(
        filho for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if filho.campos.get("preset") == "Destaque Texto"
    )
    assert "\x1b[" in destaque.campos["amostra"]
    destaque_linhas = []
    for content_w in larguras:
        entradas = _linhas_dois_niveis_formatado_com_mapa(
            controlador.conteudo,
            console.formato_filho_dois_niveis,
            content_w=content_w,
            no_corrente_id=corrente,
            indicador="→",
            indicador_off=" ",
            selecoes=set(controlador.ids_escolha_inicial),
            incluir_selecao=True,
            incluido_on="●",
            incluido_off="○",
        )
        destaque_linhas.append(_sem_ansi(next(
            entrada["linhas"][0] for entrada in entradas
            if entrada["id"] == destaque.id
        )))
    gaps = [
        linha.index(_sem_ansi(destaque.campos["amostra"]))
        - linha.index("Destaque Texto")
        - len("Destaque Texto")
        for linha in destaque_linhas
    ]
    assert gaps == [8, 3, 3, 3]
    assert all(3 <= gap <= 8 for gap in gaps)


def teste_resize_real_do_estado_recalcula_tabulacao_na_mesma_tela():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    console = controlador.console_do_modelo(modelo)
    quadro_pai = _sem_ansi(renderizar_estado(estado, modelo, largura=120, altura=40))
    coluna_pai = _coluna_cursor(quadro_pai)
    filhos = processar_comando(estado, " ", modelo)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    pai_l1 = controlador.pai_corrente(filhos, modelo)
    filho_l1 = controlador.filho_corrente(filhos, modelo)
    assert filho_l1 is not None
    id_filho = filho_l1.id
    foco_l1 = filhos.get("foco_console")
    cursor_l1 = filhos["cursores"][console.id]
    selecao_l1 = list(filhos["selecoes"][console.id])

    # L1: estado filho ja ativo; render explicito ANTES de qualquer resize.
    quadro_l1 = _sem_ansi(renderizar_estado(filhos, modelo, largura=48, altura=40))
    tab_l1 = _coluna_cursor(quadro_l1) - coluna_pai

    # L2: primeiro resize sobre o mesmo estado logico, depois novo render.
    estado_l2 = navegacao.redimensionar(filhos, 44, 40)
    quadro_l2 = _sem_ansi(renderizar_estado(estado_l2, modelo, largura=44, altura=40))
    tab_l2 = _coluna_cursor(quadro_l2) - coluna_pai

    # L3: segundo resize derivado do mesmo fluxo, depois novo render.
    estado_l3 = navegacao.redimensionar(estado_l2, 43, 40)
    quadro_l3 = _sem_ansi(renderizar_estado(estado_l3, modelo, largura=43, altura=40))
    tab_l3 = _coluna_cursor(quadro_l3) - coluna_pai

    assert tab_l1 == 10
    assert 5 < tab_l2 < 10
    assert tab_l3 == 5
    assert tab_l1 > tab_l2 >= tab_l3
    assert tab_l2 == 6
    assert (tab_l1, tab_l2, tab_l3) == (10, 6, 5)

    for etapa in (filhos, estado_l2, estado_l3):
        assert etapa["tela_atual"] == _ID_TELA
        assert modelo.id == _ID_TELA
        assert navegacao.em_nivel_filhos(etapa, console) is True
        assert etapa.get("foco_console") == foco_l1
        assert etapa["cursores"][console.id] == cursor_l1
        assert list(etapa["selecoes"][console.id]) == selecao_l1
        assert etapa["cursores"] == filhos["cursores"]
        assert etapa["selecoes"] == filhos["selecoes"]
        assert controlador.pai_corrente(etapa, modelo) == pai_l1
        filho_etapa = controlador.filho_corrente(etapa, modelo)
        assert filho_etapa is not None and filho_etapa.id == id_filho

    amostra_destaque = _sem_ansi(next(
        filho.campos["amostra"] for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if filho.campos.get("preset") == "Destaque Texto"
    ))
    for quadro in (quadro_l1, quadro_l2, quadro_l3):
        linha = next(
            linha for linha in quadro.splitlines()
            if "Borda Curva" in _miolo(linha) and "→" in _miolo(linha)
        )
        corpo = _miolo(linha)
        assert "Borda Curva" in corpo and "╭─╮││╰─╯" in corpo
        assert "A)" not in corpo and "1.1" not in corpo
        linha_destaque = next(
            linha for linha in quadro.splitlines()
            if "Destaque Texto" in _miolo(linha)
        )
        visual = _miolo(linha_destaque)
        gap = (
            visual.index(amostra_destaque)
            - visual.index("Destaque Texto")
            - len("Destaque Texto")
        )
        # H0063_ESPACAMENTO_COLUNAS_3_8: PRESERVADO
        assert 3 <= gap <= 8


def _csi_incompleto(texto):
    indice = 0
    while True:
        inicio = texto.find("\x1b[", indice)
        if inicio < 0:
            return False
        cursor = inicio + 2
        while cursor < len(texto) and not (
            "A" <= texto[cursor] <= "Z" or "a" <= texto[cursor] <= "z"
        ):
            cursor += 1
        if cursor >= len(texto):
            return True
        indice = cursor + 1


def teste_quadro_real_destaque_fundo_nao_vaza_ansi_no_resize():
    estado, modelo = _abrir()
    controlador = estado["tela_estilo"]
    console = controlador.console_do_modelo(modelo)
    filhos = processar_comando(estado, " ", modelo)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    amostra = next(
        filho.campos["amostra"] for pai in controlador.conteudo.nos
        for filho in pai.filhos
        if filho.campos.get("preset") == "Destaque Fundo"
    )
    assert "\x1b[44m" in amostra
    assert amostra.endswith("\x1b[49m")

    larguras = (120, 50, 48, 44, 43, 40)
    for largura in larguras:
        etapa = navegacao.redimensionar(filhos, largura, 40)
        quadro = renderizar_estado(etapa, modelo, largura=largura, altura=40)
        assert not _csi_incompleto(quadro)
        linhas = quadro.splitlines()
        indices = [
            indice for indice, linha in enumerate(linhas)
            if "Destaque Fundo" in _sem_ansi(linha)
        ]
        assert indices
        for indice in indices:
            linha = linhas[indice]
            assert "\x1b[44m" in linha
            assert "\x1b[49m" in linha
            depois = linha.split("\x1b[49m", 1)[1]
            assert "\x1b[44m" not in depois
            miolo = _miolo(linha)
            vis = _sem_ansi(miolo)
            if "Destaque Fundo" in vis and _sem_ansi(amostra) in vis:
                gap = (
                    vis.index(_sem_ansi(amostra))
                    - vis.index("Destaque Fundo")
                    - len("Destaque Fundo")
                )
                assert 3 <= gap <= 8
            if indice > 0:
                acima = linhas[indice - 1]
                if "Destaque Fundo" not in _sem_ansi(acima):
                    assert "\x1b[44m" not in acima
            if indice + 1 < len(linhas):
                abaixo = linhas[indice + 1]
                if "Destaque Fundo" not in _sem_ansi(abaixo):
                    assert "\x1b[44m" not in abaixo
                    assert not abaixo.startswith("\x1b[44m")
        assert "\x1b[44m" not in linhas[0]
        assert "\x1b[44m" not in linhas[-1]


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
