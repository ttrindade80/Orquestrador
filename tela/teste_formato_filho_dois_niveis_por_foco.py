"""Testes da capacidade generica de formatacao dos filhos (H-0072 / ADR-0047).

Cobre os 18 criterios de teste do handoff H-0072 §21: unidade deslocada,
tabulacao minimo/maximo/intermediario, designadores decimal_composto /
alfabetico_maiusculo / nenhum, apresentacao texto e tabela, alinhamento
global entre pais diferentes, espacamento minimo/maximo, sobra a direita,
quebra multilinha, continuacao sem novo cursor/toggle, resize preservando o
item logico, rejeicao dos onze casos de schema invalido (V-DNF-01..11) e
preservacao integral da navegacao de ``dois_niveis_por_foco`` (ADR-0042).

P01 acrescenta cobertura de §21.1: adornos ``prefixo``/``sufixo`` no
designador estrutural (incluindo o caso de capacidade equivalente a
H-0055, ``A)``), rejeicao V-DNF-12..16 e retrocompatibilidade da ausencia
de adornos. A regressao original dos 18 criterios permanece.

Reutiliza os helpers de construcao de ``ElementoCorpo``/estado de
``tela/teste_navegacao.py`` (``_estado``) e a API pura de
``tela/navegacao.py`` e ``tela/selecao.py``, sem alterar semantica de
navegacao/selecao. A formatacao e testada diretamente sobre
``tela.renderizacao.conteudo_externo._linhas_dois_niveis_formatado_com_mapa``
(geometria pura, sem TTY), e a validacao de schema via ``carregar_tela``
sobre documentos minimos escritos em ``tmp_path``.

Apenas biblioteca padrao do Python + pytest.
"""

import json
from pathlib import Path

import pytest

from tela.carregamento.erros import TelaEstruturaInvalida
from tela.loader import carregar_tela
from tela.modelo import ConteudoExterno, ElementoCorpo, NivelConteudo, NoConteudo
from tela import navegacao
from tela import selecao
from tela.renderizacao import conteudo_externo
from tela.teste_navegacao import _estado


# ---------------------------------------------------------------------------
# Construcao de ElementoCorpo/ConteudoExterno sintaticos dedicados (H-0072)
# ---------------------------------------------------------------------------


def _no_filho(idc, **campos):
    base = {"navegavel": True, "selecionavel": True}
    base.update(campos)
    return NoConteudo(id=idc, nivel="filho", campos=base, filhos=[])


def _no_pai(idc, filhos, titulo=None, navegavel=True):
    campos = {"navegavel": navegavel, "selecionavel": False}
    if titulo is not None:
        campos["titulo"] = titulo
    return NoConteudo(id=idc, nivel="pai", campos=campos, filhos=list(filhos))


def _conteudo(nos):
    return ConteudoExterno(
        tipo="multinivel",
        apresentacao="hierarquia",
        niveis=[
            NivelConteudo(
                id="pai", tipo="container", conteudo="titulo",
                designador={"tipo": "decimal", "sufixo": "."},
            ),
            NivelConteudo(
                id="filho", tipo="conteudo", conteudo="titulo",
                designador={"tipo": "nenhum"},
            ),
        ],
        nos=nos,
    )


def _console_formatado(idc, nos, config_filho):
    console = ElementoCorpo(
        id=idc,
        tipo="console",
        _campos_inertes={
            "titulo": "C",
            "politica_navegacao": {"navegavel": True, "tipo": "dois_niveis_por_foco"},
            "politica_selecao": "multipla",
        },
    )
    console.conteudo_externo = _conteudo(nos)
    console.formato_filho_dois_niveis = config_filho
    return console


def _renderizar(nos, config, content_w, verboso=False, no_corrente_id=None,
                 selecoes=None):
    return conteudo_externo._linhas_dois_niveis_formatado_com_mapa(
        _conteudo(nos), config, content_w, verboso,
        no_corrente_id=no_corrente_id, indicador="●", indicador_off="○",
        selecoes=selecoes or set(), incluir_selecao=True,
        incluido_on="◆", incluido_off="◇",
    )


def _entrada(entradas, id_no):
    return next(e for e in entradas if e["id"] == id_no)


# ---------------------------------------------------------------------------
# Caso 1 -- unidade inteira do filho deslocada (ec + tg + designador + conteudo)
# ---------------------------------------------------------------------------


def teste_unidade_inteira_do_filho_desloca_junto():
    nos = [_no_pai("pai1", [
        _no_filho("f1", titulo="Um"), _no_filho("f2", titulo="Dois"),
    ], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {"tipo": "decimal_composto"},
        "apresentacao": "texto",
    }
    entradas = _renderizar(nos, config, content_w=60, no_corrente_id="f1")
    linha = _entrada(entradas, "f1")["linhas"][0]
    # tabulacao(5) -> ec("● ") -> tg("◇ ", nao marcado) -> designador("1.1 ") -> texto
    assert linha == "     ● ◇ 1.1 Um"


# ---------------------------------------------------------------------------
# Casos 2-4 -- tabulacao minima, maxima e intermediaria
# ---------------------------------------------------------------------------


def _config_tabulacao(minimo, maximo):
    return {
        "tabulacao": {"minimo": minimo, "maximo": maximo},
        "designador": {"tipo": "nenhum"},
        "apresentacao": "texto",
    }


def _recuo_de(linha):
    return len(linha) - len(linha.lstrip(" "))


def teste_tabulacao_no_minimo_quando_so_o_minimo_cabe():
    nos = [_no_pai("pai1", [_no_filho("f1", titulo="X")], titulo="Pai 1")]
    config = _config_tabulacao(5, 10)
    # ind_w(2) + tg_w(2) + MIN_UTIL(10) = 14; minimo(5) cabe em 19, maximo(6) nao.
    entradas = _renderizar(nos, config, content_w=19)
    linha = _entrada(entradas, "f1")["linhas"][0]
    assert _recuo_de(linha) == 5


def teste_tabulacao_no_maximo_quando_maximo_cabe():
    nos = [_no_pai("pai1", [_no_filho("f1", titulo="X")], titulo="Pai 1")]
    config = _config_tabulacao(5, 10)
    entradas = _renderizar(nos, config, content_w=40)
    linha = _entrada(entradas, "f1")["linhas"][0]
    assert _recuo_de(linha) == 10


def teste_tabulacao_em_valor_intermediario():
    nos = [_no_pai("pai1", [_no_filho("f1", titulo="X")], titulo="Pai 1")]
    config = _config_tabulacao(5, 10)
    # 7 cabe (21-11=10>=10); 8 nao cabe (21-12=9<10).
    entradas = _renderizar(nos, config, content_w=21)
    linha = _entrada(entradas, "f1")["linhas"][0]
    assert _recuo_de(linha) == 7


# ---------------------------------------------------------------------------
# Casos 5-7 -- designadores decimal_composto, alfabetico_maiusculo, nenhum
# ---------------------------------------------------------------------------


def teste_designador_decimal_composto():
    nos = [_no_pai("pai1", [
        _no_filho("f1", titulo="Um"), _no_filho("f2", titulo="Dois"),
    ], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {"tipo": "decimal_composto"},
        "apresentacao": "texto",
    }
    entradas = _renderizar(nos, config, content_w=60)
    assert "1.1" in _entrada(entradas, "f1")["linhas"][0]
    assert "1.2" in _entrada(entradas, "f2")["linhas"][0]


def teste_designador_alfabetico_maiusculo():
    nos = [_no_pai("pai1", [
        _no_filho("f1", titulo="Um"), _no_filho("f2", titulo="Dois"),
    ], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {"tipo": "alfabetico_maiusculo"},
        "apresentacao": "texto",
    }
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    linha_f2 = _entrada(entradas, "f2")["linhas"][0]
    assert " A " in linha_f1
    assert " B " in linha_f2


def teste_designador_nenhum_sem_marcador():
    nos = [_no_pai("pai1", [_no_filho("f1", titulo="Unico")], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {"tipo": "nenhum"},
        "apresentacao": "texto",
    }
    entradas = _renderizar(nos, config, content_w=60)
    linha = _entrada(entradas, "f1")["linhas"][0]
    # tabulacao(5) + ec("○ ", nenhum cursor corrente) + tg("◇ ") + texto,
    # sem separador de designador.
    assert linha == "     ○ ◇ Unico"


# ---------------------------------------------------------------------------
# Caso 8 -- apresentacao texto preserva o fluxo vigente (uma linha + truncamento)
# ---------------------------------------------------------------------------


def teste_apresentacao_texto_uma_linha_com_truncamento():
    texto_longo = "Texto suficientemente longo para exceder a largura disponivel"
    nos = [_no_pai("pai1", [_no_filho("f1", titulo=texto_longo)], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 0, "maximo": 0},
        "designador": {"tipo": "nenhum"},
        "apresentacao": "texto",
    }
    entradas = _renderizar(nos, config, content_w=20, verboso=False)
    linhas = _entrada(entradas, "f1")["linhas"]
    assert len(linhas) == 1
    assert linhas[0].endswith("...")
    assert len(linhas[0]) <= 20


# ---------------------------------------------------------------------------
# Casos 9-12 -- apresentacao tabela, alinhamento global e espacamento
# ---------------------------------------------------------------------------


def _nos_tabela():
    pai1 = _no_pai("pai1", [
        _no_filho("f11", a="AAAA", b="Valor1"),
        _no_filho("f12", a="BB", b="Bx"),
    ], titulo="Pai 1")
    pai2 = _no_pai("pai2", [
        _no_filho("f21", a="CCC", b="Cy"),
        _no_filho("f22", a="D", b="Zeta12"),
    ], titulo="Pai 2")
    return [pai1, pai2]


def _config_tabela(espacamento_min, espacamento_max):
    return {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {"tipo": "nenhum"},
        "apresentacao": "tabela",
        "tabela": {
            "colunas": [{"campo": "a"}, {"campo": "b"}],
            "espacamento": {"minimo": espacamento_min, "maximo": espacamento_max},
        },
    }


def teste_apresentacao_tabela_com_duas_colunas():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)
    entradas = _renderizar(nos, config, content_w=60)
    linha_f11 = _entrada(entradas, "f11")["linhas"][0]
    assert "AAAA" in linha_f11
    assert "Valor1" in linha_f11


def teste_alinhamento_de_colunas_entre_pais_diferentes():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)
    entradas = _renderizar(nos, config, content_w=60)
    linha_f11 = _entrada(entradas, "f11")["linhas"][0]  # pai1
    linha_f21 = _entrada(entradas, "f21")["linhas"][0]  # pai2
    # Coluna "a" tem largura global fixa (max("AAAA","BB","CCC","D")=4):
    # a coluna "b" comeca na MESMA posicao para filhos de pais diferentes.
    prefixo_fixo = "     ○ ◇ "  # tabulacao(5) + ec(off) + tg, sem designador
    inicio_b_f11 = linha_f11.index("Valor1")
    inicio_b_f21 = linha_f21.index("Cy")
    assert inicio_b_f11 == inicio_b_f21
    assert linha_f11.startswith(prefixo_fixo)


def teste_espacamento_no_minimo_quando_so_o_minimo_cabe():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)
    # prefixo fixo = 5(tab)+2(ec)+2(tg) = 9; sum(col)=4+6=10; content_w=22 ->
    # disponivel=13; espacamento 3 cabe (10+3=13<=13), 4 nao (10+4=14>13).
    entradas = _renderizar(nos, config, content_w=22)
    linha_f11 = _entrada(entradas, "f11")["linhas"][0]
    resto = linha_f11[len("     ● ◇ "):]
    col_a, _, resto_b = resto.partition("   ")  # 3 espacos = minimo
    assert col_a == "AAAA"
    assert resto_b.startswith("Valor1")


def teste_espacamento_no_maximo_quando_maximo_cabe():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)
    entradas = _renderizar(nos, config, content_w=70)
    linha_f11 = _entrada(entradas, "f11")["linhas"][0]
    resto = linha_f11[len("     ● ◇ "):]
    assert resto.startswith("AAAA" + " " * 8 + "Valor1")


# ---------------------------------------------------------------------------
# Caso 13 -- sobra de largura a direita depois do maximo (sem ampliacao artificial)
# ---------------------------------------------------------------------------


def teste_sobra_permanece_a_direita_sem_ampliar_tabulacao_ou_espacamento():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)
    largura_generosa = 120
    entradas = _renderizar(nos, config, content_w=largura_generosa)
    linha_f11 = _entrada(entradas, "f11")["linhas"][0]
    assert _recuo_de(linha_f11) == 5  # tabulacao nao ultrapassa o maximo (5)
    assert "AAAA" + " " * 8 + "Valor1" in linha_f11
    assert len(linha_f11) < largura_generosa  # sobra nao e preenchida artificialmente


# ---------------------------------------------------------------------------
# Casos 14-15 -- quebra multilinha e continuacao sem novo cursor/toggle/id
# ---------------------------------------------------------------------------


def teste_quebra_multilinha_quando_nao_cabe_mesmo_apos_compactacao():
    nos = _nos_tabela()
    # O caso multilinear deve nascer de duas palavras logicas, nao da antiga
    # divisao fisica da palavra unica ``Valor1``.
    nos[0].filhos[0].campos["b"] = "Valor um"
    config = _config_tabela(3, 8)
    # Largura extremamente apertada: nem o espacamento minimo cabe -> a
    # ultima coluna quebra em multiplas linhas fisicas.
    entradas = _renderizar(nos, config, content_w=15)
    entrada_f11 = _entrada(entradas, "f11")
    assert len(entrada_f11["linhas"]) > 1


def teste_continuacao_sem_novo_cursor_toggle_ou_identidade():
    nos = _nos_tabela()
    # Mantem um unico item logico e cria a continuacao pela fronteira entre
    # palavras inteiras, sem fragmentar ``Valor1``.
    nos[0].filhos[0].campos["b"] = "Valor um"
    config = _config_tabela(3, 8)
    entradas = _renderizar(nos, config, content_w=15, no_corrente_id="f11")
    # Um unico item logico (uma entrada) para f11, mesmo com varias linhas.
    ocorrencias_f11 = [e for e in entradas if e["id"] == "f11"]
    assert len(ocorrencias_f11) == 1
    linhas = ocorrencias_f11[0]["linhas"]
    assert len(linhas) > 1
    # Apenas a primeira linha fisica recebe o indicador de cursor; as demais
    # nao repetem "●" nem criam novo prefixo indicador/toggle.
    assert linhas[0].startswith("     ● ")
    for continuacao in linhas[1:]:
        assert not continuacao.startswith("     ● ")
        assert "●" not in continuacao


# ---------------------------------------------------------------------------
# Caso 16 -- resize preserva o item logico corrente e recalcula geometria
# ---------------------------------------------------------------------------


def teste_resize_preserva_item_logico_e_recalcula_geometria():
    nos = _nos_tabela()
    config = _config_tabela(3, 8)

    entradas_estreita = _renderizar(nos, config, content_w=22)
    entradas_larga = _renderizar(nos, config, content_w=70)

    ids_estreita = [e["id"] for e in entradas_estreita]
    ids_larga = [e["id"] for e in entradas_larga]
    # Mesma sequencia de identidades logicas (pai/filho) independente da
    # largura: nenhuma geometria calculada altera a identidade dos itens.
    assert ids_estreita == ids_larga

    linha_estreita = _entrada(entradas_estreita, "f11")["linhas"][0]
    linha_larga = _entrada(entradas_larga, "f11")["linhas"][0]
    # A geometria (espacamento efetivo) e recalculada a cada largura.
    assert linha_estreita != linha_larga

    # A navegacao (D10 / ADR-0031, nao redefinida por H-0072) preserva o item
    # logico corrente do console atraves de navegacao.redimensionar.
    console = _console_formatado("console_resize", nos, config)
    estado = _estado([console], foco=0, cursores={console.id: 0})
    filhos_estado = navegacao.entrar_nivel_filhos(estado, console)
    redimensionado = navegacao.redimensionar(filhos_estado, 120, 40)
    assert redimensionado["cursores"][console.id] == filhos_estado["cursores"][console.id]


def teste_tabulacao_dinamica_monotona_na_mesma_estrutura():
    nos = [_no_pai("pai1", [
        _no_filho("f1", titulo="Filho 01.01"),
    ], titulo="Pai 1")]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 10},
        "designador": {
            "tipo": "alfabetico_maiusculo",
            "sufixo": ")",
        },
        "apresentacao": "texto",
    }

    # Larguras uteis derivadas da composicao real: o prefixo ec/tg/designador
    # ocupa 7 colunas e o texto mede 11. Assim, 28 aceita 10, 27 aceita 9 e
    # 23 aceita somente o minimo 5.
    larguras = (28, 27, 23)
    recuos = []
    ids = []
    linhas = []
    for content_w in larguras:
        entradas = _renderizar(
            nos, config, content_w=content_w, no_corrente_id="f1",
        )
        ids.append([entrada["id"] for entrada in entradas])
        linha = _entrada(entradas, "f1")["linhas"][0]
        linhas.append(linha)
        recuos.append(_recuo_de(linha))

    assert recuos == [10, 9, 5]
    assert all(5 <= recuo <= 10 for recuo in recuos)
    assert all(anterior >= atual for anterior, atual in zip(recuos, recuos[1:]))
    assert ids[0] == ids[1] == ids[2]
    assert all("A)" in linha for linha in linhas)
    for linha, recuo in zip(linhas, recuos):
        corpo = linha[recuo:]
        assert corpo.startswith("●")
        assert corpo.index("●") < corpo.index("◇") < corpo.index("A)")
        assert corpo.index("A)") < corpo.index("Filho 01.01")


# ---------------------------------------------------------------------------
# Caso 17 -- rejeicao fechada dos onze casos de schema invalido (V-DNF-01..11)
# ---------------------------------------------------------------------------


_CABECALHO_MINIMO = {
    "titulo": "T",
    "descricao": "D",
    "apresentacao": {
        "titulo": {
            "posicao": "esquerda", "recuo_lateral": 0,
            "capitalizacao": "maiusculas",
            "formato_na_borda": "com_espacos_laterais",
        },
        "descricao": {
            "max_caracteres": 80, "alinhamento": "esquerda",
            "recuo": 0, "capitalizacao": "preservar",
        },
    },
}


def _escrever_tela_com_console(tmp_path, id_tela, console):
    documento = {
        "schema": "tela.v1",
        "id": id_tela,
        "cabecalho": _CABECALHO_MINIMO,
        "corpo": {"arranjo": "vertical", "elementos": [console]},
        "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
    }
    dir_telas = tmp_path / "config" / "telas"
    dir_telas.mkdir(parents=True, exist_ok=True)
    (dir_telas / (id_tela + ".json")).write_text(
        json.dumps(documento, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path


def _console_envelope(tipo_navegacao, navegavel, formato_filho=None):
    console = {
        "id": "console_1",
        "tipo": "console",
        "itens": [],
        "origem_dados": None,
        "politica_composicao": {
            "alinhamento": "esquerda",
            "overflow_normal": "truncar_com_reticencias",
        },
        "politica_navegacao": {"navegavel": navegavel, "tipo": tipo_navegacao},
        "politica_selecao": "nenhuma",
        "politica_paginacao": "sem",
        "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
    }
    if formato_filho is not None:
        console["formato"] = {"dois_niveis_por_foco": {"filho": formato_filho}}
    return console


_FILHO_BASE_TEXTO = {
    "tabulacao": {"minimo": 5, "maximo": 10},
    "designador": {"tipo": "decimal_composto"},
    "apresentacao": "texto",
}

_FILHO_BASE_TABELA = {
    "tabulacao": {"minimo": 5, "maximo": 10},
    "designador": {"tipo": "decimal_composto"},
    "apresentacao": "tabela",
    "tabela": {
        "colunas": [{"campo": "a"}, {"campo": "b"}],
        "espacamento": {"minimo": 3, "maximo": 8},
    },
}


def teste_schema_valido_e_aceito(tmp_path):
    console = _console_envelope("dois_niveis_por_foco", True, _FILHO_BASE_TEXTO)
    _escrever_tela_com_console(tmp_path, "h0072_valido", console)
    carregada = carregar_tela(tmp_path, "h0072_valido")
    assert carregada["id"] == "h0072_valido"


def teste_v_dnf_01_tabulacao_minimo_maior_que_maximo(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, tabulacao={"minimo": 10, "maximo": 5})
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v01", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v01")


def teste_v_dnf_02_tabulacao_nao_inteiro_positivo(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, tabulacao={"minimo": 0, "maximo": 5})
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v02", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v02")


def teste_v_dnf_03_apresentacao_fora_do_vocabulario(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, apresentacao="grade")
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v03", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v03")


def teste_v_dnf_04_tabela_ausente_quando_apresentacao_tabela(tmp_path):
    filho = {
        "tabulacao": {"minimo": 5, "maximo": 10},
        "designador": {"tipo": "decimal_composto"},
        "apresentacao": "tabela",
    }
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v04", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v04")


def teste_v_dnf_05_tabela_presente_quando_apresentacao_texto(tmp_path):
    filho = dict(_FILHO_BASE_TABELA, apresentacao="texto")
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v05", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v05")


def teste_v_dnf_06_colunas_vazio(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TABELA))
    filho["tabela"]["colunas"] = []
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v06", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v06")


def teste_v_dnf_07_coluna_sem_campo_campo(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TABELA))
    filho["tabela"]["colunas"] = [{}]
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v07", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v07")


def teste_v_dnf_08_espacamento_minimo_maior_que_maximo(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TABELA))
    filho["tabela"]["espacamento"] = {"minimo": 8, "maximo": 3}
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v08", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v08")


def teste_v_dnf_09_espacamento_nao_inteiro_positivo(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TABELA))
    filho["tabela"]["espacamento"] = {"minimo": 0, "maximo": 3}
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v09", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v09")


def teste_v_dnf_10_designador_fora_do_vocabulario(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, designador={"tipo": "romano_maiusculo"})
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v10", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v10")


def teste_v_dnf_11_bloco_presente_fora_de_dois_niveis_por_foco(tmp_path):
    console = _console_envelope("nivel_unico", True, _FILHO_BASE_TEXTO)
    _escrever_tela_com_console(tmp_path, "h0072_v11", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v11")


# ---------------------------------------------------------------------------
# Caso 18 -- preservacao integral da navegacao de dois_niveis_por_foco
# ---------------------------------------------------------------------------


def teste_navegacao_dois_niveis_preservada_com_configuracao_presente():
    nos = [
        _no_pai("pai_a", [
            _no_filho("a1", titulo="A1"), _no_filho("a2", titulo="A2"),
            _no_filho("a3", titulo="A3"),
        ], titulo="Pai A"),
        _no_pai("pai_b", [
            _no_filho("b1", titulo="B1"), _no_filho("b2", titulo="B2"),
        ], titulo="Pai B"),
    ]
    config = _config_tabela(3, 8)
    console = _console_formatado("console_nav", nos, config)

    # A capacidade generica nao altera elegibilidade nem topologia (ADR-0042).
    assert navegacao.console_e_focalizavel(console) is True
    assert navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"
    assert navegacao.estrutura_dois_niveis_valida(console) is True
    assert navegacao.formato_filho_dois_niveis(console) == config

    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado["selecoes"] = {console.id: ["a1", "b1"]}

    # Toroide dos pais: 0 (pai_a) -> 4 (pai_b) -> 0 (mesma topologia do H-0055).
    estado = navegacao.mover_cima(estado, console)
    assert estado["cursores"][console.id] == 4
    estado = navegacao.mover_baixo(estado, console)
    assert estado["cursores"][console.id] == 0

    filhos = navegacao.entrar_nivel_filhos(estado, console)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    assert filhos["cursores"][console.id] == 1  # a1, primeiro filho de pai_a

    pais = navegacao.retornar_nivel_pais(filhos, console)
    assert pais["cursores"][console.id] == 0
    assert pais["selecoes"] == filhos["selecoes"]

    # Selecao exclusiva obrigatoria por pai continua intocada.
    transferido = selecao.alternar(filhos, console, "a2")
    assert transferido["selecoes"][console.id] == ["a2", "b1"]


# ---------------------------------------------------------------------------
# P01 §21.1 -- prefixo/sufixo no designador estrutural (V-DNF-12..16)
# ---------------------------------------------------------------------------


_BASE_REPOSITORIO = Path(__file__).resolve().parent.parent
_RAIZ_TELAS_DEMO = "config/telas/demo"
_ID_FIXTURE_H0072 = "h0072_formatacao_generica_dois_niveis_por_foco"


def _nos_dois_filhos():
    return [_no_pai("pai1", [
        _no_filho("f1", titulo="Um", a="AAAA", b="Valor1"),
        _no_filho("f2", titulo="Dois", a="BB", b="Bx"),
    ], titulo="Pai 1")]


def _config_texto_designador(designador):
    return {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": designador,
        "apresentacao": "texto",
    }


def teste_p01_alfabetico_maiusculo_sem_adornos_produz_a():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({"tipo": "alfabetico_maiusculo"})
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    linha_f2 = _entrada(entradas, "f2")["linhas"][0]
    assert " A " in linha_f1
    assert " B " in linha_f2
    assert "A)" not in linha_f1
    assert "(A)" not in linha_f1


def teste_p01_capacidade_equivalente_h0055_alfabetico_com_sufixo():
    # Capacidade equivalente a H-0055: sufixo vem da configuracao estrutural
    # usada pelo teste, nunca do documento externo de H-0055 (intocado).
    nos = _nos_dois_filhos()
    config = _config_texto_designador({
        "tipo": "alfabetico_maiusculo",
        "sufixo": ")",
    })
    assert ")" not in nos[0].filhos[0].campos["titulo"]
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    linha_f2 = _entrada(entradas, "f2")["linhas"][0]
    assert "A)" in linha_f1
    assert "B)" in linha_f2
    assert " A " not in linha_f1
    assert " B " not in linha_f2


def teste_p01_prefixo_isolado():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({
        "tipo": "alfabetico_maiusculo",
        "prefixo": "(",
    })
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    assert "(A " in linha_f1
    assert "(A)" not in linha_f1


def teste_p01_prefixo_e_sufixo_juntos():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({
        "tipo": "alfabetico_maiusculo",
        "prefixo": "(",
        "sufixo": ")",
    })
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    linha_f2 = _entrada(entradas, "f2")["linhas"][0]
    assert "(A)" in linha_f1
    assert "(B)" in linha_f2


def teste_p01_decimal_composto_sem_adornos_produz_1_1():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({"tipo": "decimal_composto"})
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    assert "1.1" in linha_f1
    assert "[1.1]" not in linha_f1
    assert "(1.1)" not in linha_f1


def teste_p01_decimal_composto_com_adornos_envolve_somente_a_base():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({
        "tipo": "decimal_composto",
        "prefixo": "[",
        "sufixo": "]",
    })
    entradas = _renderizar(nos, config, content_w=60)
    linha_f1 = _entrada(entradas, "f1")["linhas"][0]
    linha_f2 = _entrada(entradas, "f2")["linhas"][0]
    assert "[1.1]" in linha_f1
    assert "[1.2]" in linha_f2
    assert "1.1" in linha_f1


def teste_v_dnf_12_prefixo_nao_string(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TEXTO))
    filho["designador"]["prefixo"] = 1
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v12", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v12")


def teste_v_dnf_13_sufixo_nao_string(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TEXTO))
    filho["designador"]["sufixo"] = True
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v13", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v13")


def teste_v_dnf_14_chave_desconhecida_em_designador(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TEXTO))
    filho["designador"]["fonte"] = "conteudo"
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v14", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v14")


def teste_v_dnf_15_nenhum_com_prefixo(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, designador={"tipo": "nenhum", "prefixo": "("})
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v15", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v15")


def teste_v_dnf_16_nenhum_com_sufixo(tmp_path):
    filho = dict(_FILHO_BASE_TEXTO, designador={"tipo": "nenhum", "sufixo": ")"})
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_v16", console)
    with pytest.raises(TelaEstruturaInvalida):
        carregar_tela(tmp_path, "h0072_v16")


def teste_p01_nenhum_sem_adornos_nao_produz_designador():
    nos = _nos_dois_filhos()
    config = _config_texto_designador({"tipo": "nenhum"})
    entradas = _renderizar(nos, config, content_w=60)
    linha = _entrada(entradas, "f1")["linhas"][0]
    assert linha == "     ○ ◇ Um"
    assert "A" not in linha
    assert "1.1" not in linha


def teste_p01_ausencia_de_adornos_retrocompativel_na_fixture():
    carregada = carregar_tela(
        _BASE_REPOSITORIO, _ID_FIXTURE_H0072, _RAIZ_TELAS_DEMO,
    )
    consoles = {
        e["id"]: e
        for e in carregada["corpo"]["elementos"]
        if e.get("tipo") == "console"
    }
    desig_texto = consoles["console_h0072_texto"]["formato"][
        "dois_niveis_por_foco"
    ]["filho"]["designador"]
    desig_nenhum = consoles["console_h0072_sem_designador"]["formato"][
        "dois_niveis_por_foco"
    ]["filho"]["designador"]
    desig_tabela = consoles["console_h0072_tabela"]["formato"][
        "dois_niveis_por_foco"
    ]["filho"]["designador"]
    assert desig_texto == {"tipo": "decimal_composto"}
    assert desig_nenhum == {"tipo": "nenhum"}
    assert desig_tabela["tipo"] == "alfabetico_maiusculo"
    assert desig_tabela["prefixo"] == "("
    assert desig_tabela["sufixo"] == ")"
    assert "prefixo" not in desig_texto
    assert "sufixo" not in desig_texto
    assert "prefixo" not in desig_nenhum
    assert "sufixo" not in desig_nenhum


def teste_p01_navegacao_e_selecao_permanecem_com_adornos():
    nos = [
        _no_pai("pai_a", [
            _no_filho("a1", titulo="A1"), _no_filho("a2", titulo="A2"),
            _no_filho("a3", titulo="A3"),
        ], titulo="Pai A"),
        _no_pai("pai_b", [
            _no_filho("b1", titulo="B1"), _no_filho("b2", titulo="B2"),
        ], titulo="Pai B"),
    ]
    config = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {
            "tipo": "alfabetico_maiusculo",
            "sufixo": ")",
        },
        "apresentacao": "texto",
    }
    console = _console_formatado("console_nav_p01", nos, config)
    assert navegacao.console_e_focalizavel(console) is True
    assert navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"
    assert navegacao.estrutura_dois_niveis_valida(console) is True
    estado = _estado([console], foco=0, cursores={console.id: 0})
    estado["selecoes"] = {console.id: ["a1", "b1"]}
    estado = navegacao.mover_cima(estado, console)
    assert estado["cursores"][console.id] == 4
    estado = navegacao.mover_baixo(estado, console)
    assert estado["cursores"][console.id] == 0
    filhos = navegacao.entrar_nivel_filhos(estado, console)
    assert navegacao.em_nivel_filhos(filhos, console) is True
    assert filhos["cursores"][console.id] == 1
    transferido = selecao.alternar(filhos, console, "a2")
    assert transferido["selecoes"][console.id] == ["a2", "b1"]


def teste_p01_apresentacoes_texto_e_tabela_permanecem_com_adornos():
    nos = _nos_tabela()
    config_texto = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {
            "tipo": "alfabetico_maiusculo",
            "prefixo": "(",
            "sufixo": ")",
        },
        "apresentacao": "texto",
    }
    entradas_texto = _renderizar(nos, config_texto, content_w=60)
    linhas_texto = _entrada(entradas_texto, "f11")["linhas"]
    assert len(linhas_texto) == 1
    assert "(A)" in linhas_texto[0]
    assert "AAAA" not in linhas_texto[0]

    config_tabela = {
        "tabulacao": {"minimo": 5, "maximo": 5},
        "designador": {
            "tipo": "alfabetico_maiusculo",
            "prefixo": "(",
            "sufixo": ")",
        },
        "apresentacao": "tabela",
        "tabela": {
            "colunas": [{"campo": "a"}, {"campo": "b"}],
            "espacamento": {"minimo": 3, "maximo": 8},
        },
    }
    entradas_tabela = _renderizar(nos, config_tabela, content_w=60)
    linha_tabela = _entrada(entradas_tabela, "f11")["linhas"][0]
    assert "(A)" in linha_tabela
    assert "AAAA" in linha_tabela
    assert "Valor1" in linha_tabela


def teste_p01_schema_aceita_adornos_string_opcionais(tmp_path):
    filho = json.loads(json.dumps(_FILHO_BASE_TEXTO))
    filho["designador"]["prefixo"] = "("
    filho["designador"]["sufixo"] = ")"
    console = _console_envelope("dois_niveis_por_foco", True, filho)
    _escrever_tela_com_console(tmp_path, "h0072_adornos_ok", console)
    carregada = carregar_tela(tmp_path, "h0072_adornos_ok")
    assert carregada["id"] == "h0072_adornos_ok"
