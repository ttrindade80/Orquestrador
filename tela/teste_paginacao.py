import os
import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))

from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela import paginacao
from tela.renderizador import DESCONTO_ESTRUTURAL_CONSOLE, mapa_fisico_de_itens


_RAIZ = os.path.join("config", "telas", "demo")


def _console(id_tela):
    modelo = construir_modelo(carregar_tela(None, id_tela, _RAIZ))
    return modelo.corpo.elementos[0]


def test_plano_console_unico_tem_tres_paginas_e_primeiro_item_por_pagina():
    console = _console("h0045_paginacao_console_unico")
    assert paginacao.total_paginas(
        console, 80, 16, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == 3
    assert paginacao.primeiro_item_logico_da_pagina(
        console, 2, 80, 16, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == 16
    assert paginacao.pagina_do_item_logico(
        console, 32, 80, 16, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == 3


def test_mudanca_de_pagina_atualiza_cursor_para_primeiro_navegavel():
    console = _console("h0045_paginacao_console_unico")
    estado = {
        "largura": 80,
        "altura_interna": 16,
        "desconto_estrutural": DESCONTO_ESTRUTURAL_CONSOLE,
        "cursores": {console.id: 0},
        "pagina_atual": {console.id: 1},
    }
    novo = paginacao.pagina_proxima(estado, console)
    assert novo["pagina_atual"][console.id] == 2
    assert novo["cursores"][console.id] == 16


def test_conjunto_vazio_produz_pagina_unica_sem_cursor_e_sem_conteudo():
    """VM-H0045-R07-003: ``itens: []`` real -- pagina 1/1, sem cursor, sem
    fragmentos (distinto do caso "pagina sem navegavel dentro de um console
    com outros itens", ja coberto por
    ``demo/teste_demo_paginacao.py::test_demo_h0045_p03_pagina_sem_navegaveis_e_a_unica_sem_cursor``)."""
    console = _console("h0045_paginacao_conjunto_vazio")
    assert console._campos_inertes.get("itens") == []
    estado = {
        "largura": 80,
        "altura_interna": 2,
        "desconto_estrutural": DESCONTO_ESTRUTURAL_CONSOLE,
        "cursores": {console.id: 0},
        "pagina_atual": {console.id: 1},
    }
    novo = paginacao.ir_para_pagina(estado, console, 1)
    assert console.id not in novo["cursores"]
    assert novo["pagina_atual"][console.id] == 1
    assert paginacao.total_paginas(
        console, 80, 2, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == 1
    assert paginacao.intervalo_da_pagina(
        console, 1, 80, 2, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == []


def test_politicas_de_quebra_preservam_ocupacao_fisica_total_por_item():
    console = _console("h0045_paginacao_politicas_quebra")
    mapa = mapa_fisico_de_itens(
        console, 28, 2, True,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    plano = paginacao.plano_de_paginacao(
        console, 28, 2, True,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    total_por_id = {entrada["id"]: 0 for entrada in mapa}
    continuacoes = []
    for pagina in plano["paginas"]:
        for frag in pagina["fragmentos"]:
            total_por_id[frag["id"]] += frag["linhas_fisicas"]
            if frag["continua_de_anterior"]:
                continuacoes.append(frag["id"])
    assert total_por_id == {entrada["id"]: entrada["linhas_fisicas"] for entrada in mapa}
    assert "permitir_quebra_01" in continuacoes


# ---------------------------------------------------------------------------
# H-0045-P16: tres politicas distintas + modelo fixo invariavel.
# ---------------------------------------------------------------------------


def _console_sintetico(itens):
    console = _console("h0045_paginacao_politicas_quebra")
    console._campos_inertes["itens"] = list(itens)
    return console


def _item(id_item, linhas, politica, navegavel=True):
    # Token de 38 cols: uma linha fisica sob largura 80 + desconto 3.
    texto = " ".join(
        ("L{0:02d}_".format(i + 1) + ("x" * 34))[:38] for i in range(linhas)
    )
    return {
        "id": id_item,
        "texto": texto,
        "navegavel": navegavel,
        "politica_quebra": politica,
    }


def _item_p16_palavras_inteiras(id_item, palavras, politica, navegavel=True):
    # A celula do fixture reserva dois indicadores, portanto a largura textual
    # efetiva e 76. Palavras de 37 colunas permitem duas por linha (75 com o
    # vao), mantendo a quebra exclusivamente entre palavras inteiras.
    texto = " ".join(
        ("P{0:02d}_".format(i + 1) + ("y" * 33))[:37]
        for i in range(palavras)
    )
    return {
        "id": id_item,
        "texto": texto,
        "navegavel": navegavel,
        "politica_quebra": politica,
    }


def test_p16_fluxo_continuo_comeca_na_proxima_linha_disponivel():
    """permitir_quebra: aproveita residuo; pode iniciar na ultima linha util."""
    C = 5
    console = _console_sintetico(
        [
            # 7 e 5 palavras produzem 4 e 3 linhas físicas canônicas.
            _item_p16_palavras_inteiras("a", 7, "permitir_quebra"),
            _item_p16_palavras_inteiras("b", 5, "permitir_quebra"),
        ]
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    )
    # a usa 4; b comeca na ultima linha da pagina 1 e continua na 2.
    pag1_ids = [f["id"] for f in plano["paginas"][0]["fragmentos"]]
    assert pag1_ids == ["a", "b"]
    assert plano["paginas"][0]["linhas_usadas"] == 5
    frags_b = [
        f for p in plano["paginas"] for f in p["fragmentos"] if f["id"] == "b"
    ]
    assert len(frags_b) == 2
    assert frags_b[0]["linhas_fisicas"] == 1
    assert frags_b[1]["continua_de_anterior"] is True


def test_p16_evitar_quebra_sempre_nova_pagina_mesmo_com_residuo():
    """evitar_quebra: nunca aproveita residuo da pagina anterior."""
    C = 6
    console = _console_sintetico(
        [
            _item("a", 2, "evitar_quebra"),
            _item("b", 2, "evitar_quebra"),  # caberia no residuo 4, mas nao usa
        ]
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    )
    assert plano["paginas"][0]["linhas_usadas"] == 2
    assert [f["id"] for f in plano["paginas"][0]["fragmentos"]] == ["a"]
    assert [f["id"] for f in plano["paginas"][1]["fragmentos"]] == ["b"]
    assert plano["paginas"][1]["fragmentos"][0]["primeira_linha_do_item"] is True


def test_p16_condicional_mantem_junto_quando_cabe_no_residuo():
    """permitir_quebra_somente_se_maior_que_pagina: aproveita residuo se couber."""
    C = 6
    politica = "permitir_quebra_somente_se_maior_que_pagina"
    console = _console_sintetico(
        [
            _item("a", 2, politica),
            _item("b", 2, politica),  # cabe no residuo 4
        ]
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    )
    assert len(plano["paginas"]) == 1
    assert [f["id"] for f in plano["paginas"][0]["fragmentos"]] == ["a", "b"]


def test_p16_condicional_move_inteiro_quando_nao_cabe_no_residuo():
    C = 6
    politica = "permitir_quebra_somente_se_maior_que_pagina"
    console = _console_sintetico(
        [
            # A composição canônica produz 4 linhas físicas para ``a`` e 3
            # para ``b``; ``b`` não cabe no resíduo 2.
            _item_p16_palavras_inteiras("a", 7, politica),
            _item_p16_palavras_inteiras(
                "b", 5, politica
            ),  # nao cabe no residuo 2; cabe em pagina vazia
        ]
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    )
    assert [f["id"] for f in plano["paginas"][0]["fragmentos"]] == ["a"]
    assert [f["id"] for f in plano["paginas"][1]["fragmentos"]] == ["b"]
    assert len(plano["paginas"][1]["fragmentos"]) == 1


def test_p16_item_maior_que_pagina_nas_tres_politicas():
    C = 4
    linhas_fisicas_esperadas = 9
    for politica, id_item in (
        ("permitir_quebra", "perm"),
        ("evitar_quebra", "evit"),
        ("permitir_quebra_somente_se_maior_que_pagina", "cond"),
    ):
        console = _console_sintetico(
            [
                _item_p16_palavras_inteiras("pre", 1, politica),
                # 17 palavras do fixture compõem 9 linhas físicas canônicas.
                _item_p16_palavras_inteiras(id_item, 17, politica),
            ]
        )
        plano = paginacao.plano_de_paginacao(
            console, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
        )
        frags = [
            f for p in plano["paginas"] for f in p["fragmentos"] if f["id"] == id_item
        ]
        assert sum(f["linhas_fisicas"] for f in frags) == linhas_fisicas_esperadas
        assert len(frags) >= 2
        # Condicional e evitar comecam o item grande em pagina nova (pre ocupa 1).
        if politica != "permitir_quebra":
            assert frags[0]["pagina"] >= 2
            assert frags[0]["primeira_linha_do_item"] is True
            pag_pre = next(
                p for p in plano["paginas"] if any(f["id"] == "pre" for f in p["fragmentos"])
            )
            assert not any(f["id"] == id_item for f in pag_pre["fragmentos"])
        else:
            # Fluxo continuo: pode comecar no residuo da pagina do pre.
            assert frags[0]["pagina"] == 1


def test_p16_mesmo_modelo_em_varias_geometrias_sem_perda_nem_duplicacao():
    from demo import casos_validacao_paginacao as cv

    console = _console("h0045_validacao_fluxo_continuo")
    hash0 = cv.hash_modelo_logico(console)
    snap0 = cv.snapshot_itens_logicos(console)
    for largura, C in ((80, 8), (60, 5), (100, 12), (40, 3)):
        assert cv.hash_modelo_logico(console) == hash0
        assert cv.snapshot_itens_logicos(console) == snap0
        mapa = mapa_fisico_de_itens(
            console, largura, C, True,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        plano = paginacao.plano_de_paginacao(
            console, largura, C, True,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        totais = {e["id"]: 0 for e in mapa}
        for p in plano["paginas"]:
            for f in p["fragmentos"]:
                totais[f["id"]] += f["linhas_fisicas"]
        assert totais == {e["id"]: e["linhas_fisicas"] for e in mapa}


def test_p16_vazio_e_continuacao_modelo_fixo():
    from demo import casos_validacao_paginacao as cv

    vazio = _console("h0045_validacao_vazio")
    assert vazio._campos_inertes.get("itens") == []
    assert cv.hash_modelo_logico(vazio) == cv.hash_modelo_logico(
        _console("h0045_validacao_vazio")
    )
    assert paginacao.total_paginas(
        vazio, 80, 8, False, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
    ) == 1

    cont = _console("h0045_validacao_continuacao")
    texto = cont._campos_inertes["itens"][0]["texto"]
    assert "CONT_INICIO" in texto and "CONT_MEIO" in texto and "CONT_FIM" in texto
    hash_c = cv.hash_modelo_logico(cont)
    for C in (4, 8, 16, 32):
        assert cv.hash_modelo_logico(cont) == hash_c
        plano = paginacao.plano_de_paginacao(
            cont, 80, C, True, desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE
        )
        assert plano["total_paginas"] >= 3
        assert any(
            p["fragmentos"]
            and not any(
                f["primeira_linha_do_item"] and f["navegavel"] for f in p["fragmentos"]
            )
            for p in plano["paginas"]
        )


def test_p16_evitar_e_condicional_nao_compartilham_mesmo_efeito():
    """Prova de ramos distintos: mesmo setup, politicas divergem."""
    C = 6
    itens_base = [
        _item("a", 2, "evitar_quebra"),
        _item("b", 2, "evitar_quebra"),
    ]
    plano_ev = paginacao.plano_de_paginacao(
        _console_sintetico(itens_base), 80, C, True,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    itens_cond = [
        _item("a", 2, "permitir_quebra_somente_se_maior_que_pagina"),
        _item("b", 2, "permitir_quebra_somente_se_maior_que_pagina"),
    ]
    plano_co = paginacao.plano_de_paginacao(
        _console_sintetico(itens_cond), 80, C, True,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    )
    assert plano_ev["total_paginas"] == 2
    assert plano_co["total_paginas"] == 1


# Compatibilidade residual dos construtores legados (API de teste).
def test_h0045_p12_conjunto_vazio_adaptativo():
    from demo import casos_validacao_paginacao as cv

    caso = cv.construir_caso_vazio(20, 8)
    assert caso["itens"] == []
    console = _console("h0045_paginacao_conjunto_vazio")
    assert console._campos_inertes.get("itens") == []
    assert paginacao.total_paginas(
        console, 80, 8, False,
        desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
    ) == 1
