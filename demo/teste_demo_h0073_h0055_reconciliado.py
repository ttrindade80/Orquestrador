"""Demonstracao H-0073 da tela H-0055 reconciliada pelo ponto de entrada real.

Prova que ``h0055_dois_niveis_por_foco`` e carregada e renderizada por
``demo/demo.py`` (catalogo, ``_carregar_modelo_por_id``,
``criar_estado_inicial``/``processar_comando``/``renderizar_estado``),
nunca apenas por chamada direta ao renderer.

Executavel via:
    python demo/teste_demo_h0073_h0055_reconciliado.py

Apenas biblioteca padrao do Python + pytest.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from demo.demo import (  # noqa: E402
    _CATALOGO_CONTEUDO_EXTERNO,
    id_conteudo_externo_de,
    _carregar_modelo_por_id,
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
)
from tela import navegacao  # noqa: E402
from tela.loader import carregar_estilo  # noqa: E402
from tela.renderizacao.conteudo_externo import (  # noqa: E402
    _linhas_dois_niveis_formatado_com_mapa,
)

_ESTILO = carregar_estilo()
_ID_TELA = "h0055_dois_niveis_por_foco"
_CAMINHO_ESTRUTURAL = (
    _BASE_PADRAO / "config" / "telas" / "demo" / "h0055_dois_niveis_por_foco.json"
)
_CAMINHO_CONTEUDO = (
    _BASE_PADRAO / "config" / "telas" / "demo"
    / "h0055_dois_niveis_por_foco_conteudo.json"
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


def _bytes_committed(caminho):
    rel = os.path.relpath(caminho, _BASE_PADRAO)
    return subprocess.check_output(
        ["git", "show", "HEAD:{0}".format(rel)],
        cwd=str(_BASE_PADRAO),
    )


def teste_catalogo_associa_cenario_h0055():
    assert _CATALOGO_CONTEUDO_EXTERNO[_ID_TELA] == (
        "h0055_dois_niveis_por_foco_conteudo"
    )
    assert id_conteudo_externo_de(_ID_TELA) == (
        "h0055_dois_niveis_por_foco_conteudo"
    )


def teste_conteudo_externo_permanece_byte_a_byte():
    atual = _CAMINHO_CONTEUDO.read_bytes()
    assert atual == _bytes_committed(_CAMINHO_CONTEUDO)
    assert b'"tipo": "alfabetico_maiusculo", "sufixo": ")"' in atual


def teste_configuracao_estrutural_declara_sufixo_e_apresentacao_texto():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    config = console.formato_filho_dois_niveis
    assert config["tabulacao"] == {"minimo": 5, "maximo": 10}
    assert config["designador"]["tipo"] == "alfabetico_maiusculo"
    assert config["designador"]["sufixo"] == ")"
    assert "prefixo" not in config["designador"]
    assert config["apresentacao"] == "texto"
    assert "tabela" not in config
    bruto = _CAMINHO_ESTRUTURAL.read_text(encoding="utf-8")
    assert '"sufixo": ")"' in bruto
    assert '"apresentacao": "texto"' in bruto
    dist = (modelo.barra_de_menus.get("distribuicao") or {})
    assert dist.get("linhas", {}).get("maximo") == 5
    assert (
        '"linhas": {"minimo": 1, "maximo": 5, "preferir_menor_numero": true}'
        in bruto
    )


def teste_renderizacao_real_exibe_a_com_sufixo_tabulacao_e_unidade():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    estado = dict(
        criar_estado_inicial(), estilo=_ESTILO, foco_console=0,
        cursores={console.id: 0}, largura=90, altura=30,
    )
    inicial = processar_comando(estado, "", modelo)
    quadro = _sem_ansi(renderizar_estado(inicial, modelo, largura=90, altura=30))
    assert "(console)" not in quadro
    assert "Pai 01" in quadro
    assert "Filho 01.01" in quadro

    linhas = [
        linha for linha in quadro.splitlines() if "Filho 01." in _miolo(linha)
    ]
    assert linhas
    assert any("A)" in linha and "Filho 01.01" in linha for linha in linhas)
    assert any("B)" in linha and "Filho 01.02" in linha for linha in linhas)
    assert any("C)" in linha and "Filho 01.03" in linha for linha in linhas)
    assert any("D)" in linha and "Filho 01.04" in linha for linha in linhas)

    coluna_pai = _coluna_cursor(quadro)
    filhos = processar_comando(inicial, " ", modelo)
    quadro_filhos = _sem_ansi(renderizar_estado(filhos, modelo, largura=90, altura=30))
    coluna_filho = _coluna_cursor(quadro_filhos)
    assert 5 <= coluna_filho - coluna_pai <= 10

    config = console.formato_filho_dois_niveis
    linha_corrente = next(
        linha for linha in quadro_filhos.splitlines()
        if "→" in _miolo(linha) and "A)" in linha
    )
    corpo = _miolo(linha_corrente)
    assert " A " not in corpo
    assert corpo.index("→") < corpo.index("●") < corpo.index("A)") < corpo.index("Filho")
    assert corpo[corpo.index("A)"):corpo.index("A)") + 2] == "A" + config["designador"]["sufixo"]


def teste_navegacao_e_selecao_permanecem():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    estado = dict(
        criar_estado_inicial(), estilo=_ESTILO, foco_console=0,
        cursores={console.id: 0}, largura=90, altura=30,
    )
    inicial = processar_comando(estado, "", modelo)
    assert inicial["selecoes"][console.id] == [
        "filho_01_01", "filho_02_01", "filho_03_01",
        "filho_04_01", "filho_05_01",
    ]
    filhos = processar_comando(inicial, " ", modelo)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    cursor = processar_comando(filhos, "\x1b[B", modelo)
    assert cursor["cursores"][console.id] == 2
    transferido = processar_comando(cursor, " ", modelo)
    assert transferido["selecoes"][console.id][0] == "filho_01_02"
    retorno = processar_comando(transferido, "\x1b", modelo)
    assert navegacao.em_nivel_filhos(retorno, console) is False
    assert retorno["selecoes"] == transferido["selecoes"]


def teste_resize_real_do_renderer_reduz_tabulacao_e_preserva_a_unidade():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    selecoes = {"filho_01_01"}
    larguras = (28, 27, 23)
    recuos = []
    ids = []
    linhas = []
    for content_w in larguras:
        entradas = _linhas_dois_niveis_formatado_com_mapa(
            console.conteudo_externo,
            console.formato_filho_dois_niveis,
            content_w=content_w,
            no_corrente_id="filho_01_01",
            indicador="→",
            indicador_off=" ",
            selecoes=selecoes,
            incluir_selecao=True,
            incluido_on="●",
            incluido_off="○",
        )
        ids.append([entrada["id"] for entrada in entradas])
        linha = next(
            entrada["linhas"][0] for entrada in entradas
            if entrada["id"] == "filho_01_01"
        )
        linhas.append(linha)
        recuos.append(len(linha) - len(linha.lstrip(" ")))

    assert recuos == [10, 9, 5]
    assert all(5 <= recuo <= 10 for recuo in recuos)
    assert all(anterior >= atual for anterior, atual in zip(recuos, recuos[1:]))
    assert ids[0] == ids[1] == ids[2]
    for linha in linhas:
        assert "A)" in linha
        assert linha.index("→") < linha.index("●") < linha.index("A)")
        assert linha.index("A)") < linha.index("Filho 01.01")


def teste_resize_real_do_estado_recalcula_tabulacao_na_mesma_tela():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    estado = dict(
        criar_estado_inicial(), estilo=_ESTILO, foco_console=0,
        cursores={console.id: 0}, largura=90, altura=30,
    )
    inicial = processar_comando(estado, "", modelo)
    quadro_pai = _sem_ansi(renderizar_estado(inicial, modelo, largura=90, altura=30))
    coluna_pai = _coluna_cursor(quadro_pai)
    filhos = processar_comando(inicial, " ", modelo)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    estrutural = navegacao._sequencia_estrutural_dois_niveis(console)
    id_filho = estrutural[filhos["cursores"][console.id]].id
    foco_l1 = filhos.get("foco_console")
    cursor_l1 = filhos["cursores"][console.id]
    selecao_l1 = list(filhos["selecoes"][console.id])

    quadro_l1 = _sem_ansi(renderizar_estado(filhos, modelo, largura=80, altura=30))
    tab_l1 = _coluna_cursor(quadro_l1) - coluna_pai
    linhas_barra_l1 = [
        linha for linha in quadro_l1.splitlines()
        if any(
            token in linha
            for token in ("Voltar", "Navegar", "Ajuda", "Selecionar", "Páginas")
        )
    ]
    assert len(linhas_barra_l1) == 1

    estado_l2 = navegacao.redimensionar(filhos, 36, 30)
    quadro_l2 = _sem_ansi(renderizar_estado(estado_l2, modelo, largura=36, altura=30))
    tab_l2 = _coluna_cursor(quadro_l2) - coluna_pai

    estado_l3 = navegacao.redimensionar(estado_l2, 32, 30)
    quadro_l3 = _sem_ansi(renderizar_estado(estado_l3, modelo, largura=32, altura=30))
    tab_l3 = _coluna_cursor(quadro_l3) - coluna_pai

    assert tab_l1 == 10
    assert 5 < tab_l2 < 10
    assert tab_l3 == 5
    assert (tab_l1, tab_l2, tab_l3) == (10, 9, 5)
    assert tab_l1 > tab_l2 >= tab_l3

    for etapa in (filhos, estado_l2, estado_l3):
        assert modelo.id == _ID_TELA
        assert navegacao.em_nivel_filhos(etapa, console) is True
        assert etapa.get("foco_console") == foco_l1
        assert etapa["cursores"][console.id] == cursor_l1
        assert list(etapa["selecoes"][console.id]) == selecao_l1
        assert estrutural[etapa["cursores"][console.id]].id == id_filho

    for quadro in (quadro_l1, quadro_l2, quadro_l3):
        linha = next(
            linha for linha in quadro.splitlines()
            if "→" in _miolo(linha) and "A)" in linha
        )
        corpo = _miolo(linha)
        assert "A)" in corpo
        assert corpo.index("→") < corpo.index("●") < corpo.index("A)")
        assert corpo.index("A)") < corpo.index("Filho 01.01")


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
\n