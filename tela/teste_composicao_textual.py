"""Testes diretos do núcleo canônico e de sua integração com o popup."""

import re

import pytest

from tela.carregamento.estilo import carregar_estilo
from tela.renderizacao import composicao_textual, popup
from tela.renderizacao.texto_ansi import _largura_sem_ansi


def _declaracao(alinhamento="esquerda"):
    return {
        "tipo": "texto",
        "titulo": "Mensagem",
        "alinhamento": alinhamento,
        "espacamento_superior": 1,
        "espacamento_conteudo_chips": 1,
        "espacamento_inferior": 1,
        "espacamento_horizontal": 2,
        "chips": [
            {
                "id": "popup_basico_voltar",
                "tipo": "especifico",
                "tecla": "Esc",
                "texto": "Voltar",
                "referencia_regra": {"resultado": {"status": "ABORTADO"}},
                "regra_existencia": "sempre",
                "regra_ativo": "sempre",
                "forma_exibicao": "ativo",
            }
        ],
    }


def _instancia(texto, alinhamento="esquerda"):
    return popup.abrir_popup(
        {"popups": {"popup": _declaracao(alinhamento)}},
        "popup",
        {"tipo": "texto", "texto": texto},
    )


@pytest.mark.parametrize(
    ("texto", "largura", "esperado"),
    [
        ("alpha beta gamma", 10, ["alpha beta", "gamma"]),
        ("alpha beta gamma", 5, ["alpha", "beta", "gamma"]),
        ("alpha beta gamma", 20, ["alpha beta gamma"]),
    ],
)
def test_nucleo_compoe_paragrafo_por_palavras_em_larguras_distintas(
    texto, largura, esperado
):
    assert composicao_textual.compor_texto(texto, largura) == esperado
    assert all(
        palavra in " ".join(esperado)
        for palavra in ("alpha", "beta", "gamma")
    )


def test_nucleo_nao_divide_palavra_em_mais_de_uma_linha():
    texto = "alpha beta gamma"
    linhas = composicao_textual.compor_texto(texto, 5)

    assert [linha.split() for linha in linhas] == [
        ["alpha"], ["beta"], ["gamma"]
    ]
    assert all(
        sum(len(palavra) for palavra in linha.split()) <= 5
        for linha in linhas
    )


def test_nucleo_mantem_palavra_maior_que_largura_inteira():
    palavra = "abcdefghij"

    linhas = composicao_textual.compor_texto(palavra, 4)

    assert linhas == [palavra]
    assert "".join(linhas) == palavra
    assert _largura_sem_ansi(linhas[0]) > 4


def test_nucleo_recompoe_o_paragrafo_original_em_tres_larguras():
    texto = "um paragrafo logico com palavras inteiras"
    esperado = texto.split()
    resultados = []

    for largura in (40, 20, 10):
        linhas = composicao_textual.compor_texto(texto, largura)
        resultados.append(linhas)
        assert [palavra for linha in linhas for palavra in linha.split()] == esperado

    assert len({tuple(linhas) for linhas in resultados}) == 3
    assert composicao_textual.compor_texto(texto, 40) == resultados[0]


def test_nucleo_mantem_ordem_do_conteudo_sem_politica_de_espacamento():
    texto = "alpha  beta gamma"
    linhas = composicao_textual.compor_texto(texto, 7)

    visivel = "".join(linhas)
    assert "".join(char for char in visivel if not char.isspace()) == "".join(
        char for char in texto if not char.isspace()
    )
    assert all(_largura_sem_ansi(linha) <= 7 for linha in linhas)


def test_justificacao_e_explicita_e_distinta_de_padding_estrutural():
    normal = composicao_textual.compor_texto("abc", 10)
    justificada = composicao_textual.compor_texto(
        "a b c", 9, modo="justificado"
    )
    sem_vao = composicao_textual.compor_texto(
        "palavra", 12, modo="justificado"
    )

    assert normal == ["abc"]
    assert _largura_sem_ansi(justificada[0]) == 9
    assert justificada[0].replace(" ", "") == "abc"
    assert "".join(char for char in sem_vao[0] if not char.isspace()) == "palavra"
    assert _largura_sem_ansi(sem_vao[0]) <= 12


def test_justificacao_ocorre_depois_da_formacao_por_palavras():
    normal = composicao_textual.compor_texto("alpha beta gamma", 11)
    justificada = composicao_textual.compor_texto(
        "alpha beta gamma", 11, modo="justificado", justificar_ultima=False
    )

    assert normal == ["alpha beta", "gamma"]
    assert [linha.replace(" ", "") for linha in justificada] == [
        "alphabeta", "gamma"
    ]
    assert _largura_sem_ansi(justificada[0]) == 11
    assert _largura_sem_ansi(justificada[-1]) < 11


def test_justificacao_nao_exige_distribuicao_matematica_especifica():
    linha = composicao_textual.compor_texto(
        "a b c", 8, modo="justificado"
    )[0]

    assert _largura_sem_ansi(linha) == 8
    assert linha.replace(" ", "") == "abc"


def test_ultima_linha_e_opcao_do_consumidor():
    todas = composicao_textual.compor_texto(
        "a b c d e", 7, modo="justificado"
    )
    sem_ultima = composicao_textual.compor_texto(
        "a b c d e", 7, modo="justificado", justificar_ultima=False
    )

    assert _largura_sem_ansi(todas[0]) == 7
    assert _largura_sem_ansi(sem_ultima[-1]) < 7
    assert todas[:-1] == sem_ultima[:-1]


def test_ansi_preserva_palavra_estilizada_csi_e_isola_sgr():
    texto = "alpha \x1b[34mbeta\x1b[39m gamma"
    linhas = composicao_textual.compor_texto(texto, 10)
    padrao_csi = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

    assert [_largura_sem_ansi(linha) for linha in linhas] == [10, 5]
    assert [padrao_csi.sub("", linha) for linha in linhas] == [
        "alpha beta", "gamma"
    ]
    assert "\x1b[34m" in linhas[0]
    assert "\x1b[39m" in linhas[0]
    assert all(
        padrao_csi.fullmatch(codigo)
        for linha in linhas
        for codigo in padrao_csi.findall(linha)
    )
    assert linhas[0].endswith("\x1b[39m")


def test_popup_usa_diretamente_o_nucleo_e_consumo_coerente():
    assert popup._quebrar_texto is composicao_textual.compor_texto
    assert popup._justificar_linha is composicao_textual._justificar_linha

    estilo = carregar_estilo()
    instancia = _instancia("alpha beta gamma delta", alinhamento="justificado")
    layout = popup._layout_popup(instancia, estilo, largura_corpo=20)
    esperado = composicao_textual.compor_texto(
        instancia.conteudo["texto"],
        layout["largura_util"],
        modo="justificado",
        justificar_ultima=False,
    )
    saida = popup.renderizar_popup(instancia, estilo, largura=20)

    assert layout["linhas_texto"] == esperado
    assert len(saida.splitlines()) == layout["altura"]
    assert all(len(linha) == 20 for linha in saida.splitlines())
    assert "".join(
        char
        for linha in layout["linhas_texto"]
        for char in linha
        if not char.isspace()
    ) == "".join(
        char for char in instancia.conteudo["texto"] if not char.isspace()
    )


def test_popup_recompoe_com_mudanca_de_largura_sem_reabrir_instancia():
    estilo = carregar_estilo()
    instancia = _instancia("texto longo para recompor em linhas")

    largo = popup.renderizar_popup(instancia, estilo, largura=32)
    estreito = popup.renderizar_popup(instancia, estilo, largura=20)
    restaurado = popup.renderizar_popup(instancia, estilo, largura=32)

    assert largo != estreito
    assert restaurado == largo
    assert all(len(linha) == 32 for linha in largo.splitlines())
    assert all(len(linha) == 20 for linha in estreito.splitlines())


def test_popup_recompoe_sempre_com_o_paragrafo_logico_original(monkeypatch):
    estilo = carregar_estilo()
    texto = "paragrafo longo para verificar recomposicao completa"
    instancia = _instancia(texto)
    recebidos = []
    compor_original = popup.compor_texto

    def observar(texto_recebido, *args, **kwargs):
        recebidos.append(texto_recebido)
        return compor_original(texto_recebido, *args, **kwargs)

    monkeypatch.setattr(popup, "compor_texto", observar)
    popup.renderizar_popup(instancia, estilo, largura=40)
    popup.renderizar_popup(instancia, estilo, largura=20)
    popup.renderizar_popup(instancia, estilo, largura=40)

    assert recebidos == [texto, texto, texto]
