"""Testes focais do popup textual H-0056."""

import copy

import pytest

from tela.carregamento.estilo import carregar_estilo
from tela.renderizacao import popup


def _declaracao():
    return {
        "tipo": "texto",
        "titulo": "Mensagem",
        "alinhamento": "centralizado",
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


def _fonte():
    return {"popups": {"popup_basico": _declaracao()}}


def _conteudo():
    return {"tipo": "texto", "texto": "Exemplo de pop-up."}


@pytest.fixture(scope="module")
def estilo():
    return carregar_estilo()


def test_popups_opcional_ausente_e_mapa_vazio_sao_validos():
    assert popup.validar_popups({}) == {}
    assert popup.validar_popups({"popups": {}}) == {}


def test_popups_null_presente_e_invalido():
    with pytest.raises(popup.PopupErro):
        popup.validar_popups({"popups": None})


def test_resolve_por_chave_e_rejeita_id_inexistente():
    declaracao = popup.resolver_popup(_fonte(), "popup_basico")
    assert declaracao["_id"] == "popup_basico"
    with pytest.raises(popup.PopupErro):
        popup.resolver_popup(_fonte(), "nao_existe")


def test_declaracao_nao_tem_id_redundante_nem_conteudo():
    declaracao = _declaracao()
    declaracao["id"] = "popup_basico"
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)
    declaracao = _declaracao()
    declaracao["conteudo"] = _conteudo()
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)


def test_conteudo_runtime_separado_e_declaracao_reutilizavel():
    fonte = _fonte()
    original = copy.deepcopy(fonte)
    primeira = popup.abrir_popup(fonte, "popup_basico", _conteudo())
    segunda = popup.abrir_popup(fonte, "popup_basico", _conteudo())
    assert primeira.conteudo == _conteudo()
    assert segunda.conteudo == _conteudo()
    assert fonte == original
    assert "conteudo" not in fonte["popups"]["popup_basico"]


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("alinhamento", "diagonal"),
        ("espacamento_superior", 2),
        ("espacamento_conteudo_chips", -1),
        ("espacamento_inferior", 2),
        ("espacamento_horizontal", 0),
        ("espacamento_horizontal", 6),
    ],
)
def test_dominios_de_alinhamento_e_espacamentos(campo, valor):
    declaracao = _declaracao()
    declaracao[campo] = valor
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)


def test_schema_canonico_do_chip_e_texto_sem_rotulo():
    declaracao = _declaracao()
    chip = declaracao["chips"][0]
    del chip["texto"]
    chip["rotulo"] = "Voltar"
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)

    for campo in (
        "id",
        "tipo",
        "tecla",
        "regra_existencia",
        "regra_ativo",
        "forma_exibicao",
    ):
        declaracao = _declaracao()
        del declaracao["chips"][0][campo]
        with pytest.raises(popup.PopupErro):
            popup.validar_declaracao_popup(declaracao)

    declaracao = _declaracao()
    del declaracao["chips"][0]["referencia_regra"]
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)


def test_chip_esc_tem_regra_abortado_sem_payload():
    instancia = popup.abrir_popup(_fonte(), "popup_basico", _conteudo())
    assert popup.consumir_tecla_popup(instancia, "x") is None
    resultado = popup.consumir_tecla_popup(instancia, "\x1b")
    assert resultado == {"status": "ABORTADO"}
    assert "valor" not in resultado


@pytest.mark.parametrize("alinhamento", ["esquerda", "centralizado", "justificado"])
def test_geometria_simples_e_caixa_sem_wrapping(estilo, alinhamento):
    fonte = _fonte()
    fonte["popups"]["popup_basico"]["alinhamento"] = alinhamento
    instancia = popup.abrir_popup(fonte, "popup_basico", _conteudo())
    medidas = popup.geometria_popup(instancia, estilo)
    caixa = popup.renderizar_popup(instancia, estilo)
    linhas = caixa.splitlines()
    assert len(linhas) == medidas["altura"]
    assert all(len(linha) == medidas["largura"] for linha in linhas)
    assert "Exemplo de pop-up." in caixa
    assert "Esc" in caixa
    assert "Voltar" in caixa or "VOLTAR" in caixa


def test_centralizacao_sobre_o_corpo_e_area_independente_da_barra(estilo):
    instancia = popup.abrir_popup(_fonte(), "popup_basico", _conteudo())
    largura, altura = 42, 14
    corpo = "\n".join("x" * largura for _ in range(altura))
    sobreposto = popup.sobrepor_no_corpo(
        corpo, instancia, estilo, largura, altura=altura
    )
    linhas = sobreposto.splitlines()
    medidas = popup.geometria_popup(instancia, estilo)
    x = (largura - medidas["largura"]) // 2
    y = (altura - medidas["altura"]) // 2
    assert linhas[0] == "x" * largura
    assert linhas[-1] == "x" * largura
    assert linhas[y].startswith("x" * x)
    assert "Mensagem" in linhas[y]
    assert not hasattr(popup, "_linhas_barra")
    assert not hasattr(popup, "paginacao")


def _instancia_texto(texto, **alteracoes):
    fonte = _fonte()
    fonte["popups"]["popup_basico"].update(alteracoes)
    return popup.abrir_popup(
        fonte, "popup_basico", {"tipo": "texto", "texto": texto}
    )


def _chip(id_, tecla, texto):
    return {
        "id": id_,
        "tipo": "especifico",
        "tecla": tecla,
        "texto": texto,
        "referencia_regra": {"resultado": {"status": "ABORTADO"}},
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "ativo",
    }


def test_largura_intrinseca_cap_corpo_e_padding_horizontal(estilo):
    instancia = _instancia_texto("texto curto")
    intrinseca = popup.geometria_popup(instancia, estilo)
    assert intrinseca["largura"] == max(
        len("Mensagem") + 4, 3 + 4 + len("[Esc] Voltar")
    )

    instancia_longa = _instancia_texto("texto longo para quebrar")
    limitada = popup.geometria_popup(instancia_longa, estilo, largura_corpo=20)
    assert limitada["largura"] == 20
    assert limitada["altura"] > intrinseca["altura"]

    com_padding = _instancia_texto("x" * 20, espacamento_horizontal=3)
    medidas = popup.geometria_popup(com_padding, estilo)
    assert medidas["largura"] == 3 + 2 * 3 + 20


def test_wrapping_preserva_palavras_sem_truncamento_ou_paginacao(estilo):
    texto = "alpha beta gamma delta"
    linhas = popup._quebrar_texto(texto, 10)
    assert len(linhas) > 1
    assert all(len(linha) <= 10 for linha in linhas)
    assert "".join(linhas) == texto
    assert all(palavra in " ".join(linhas) for palavra in texto.split())

    instancia = _instancia_texto(texto)
    caixa = popup.renderizar_popup(instancia, estilo, largura=20)
    assert "alpha" in caixa and "beta" in caixa
    assert "gamma" in caixa and "delta" in caixa
    assert "..." not in caixa
    assert len(caixa.splitlines()) == popup.geometria_popup(
        instancia, estilo, largura_corpo=20
    )["altura"]


@pytest.mark.parametrize(
    ("texto", "largura", "esperado"),
    [
        ("a  b", 3, ["a  ", "b"]),
        ("a   b", 4, ["a   ", "b"]),
        ("aa  bb", 4, ["aa  ", "bb"]),
    ],
)
def test_wrapping_preserva_separadores_multiplos(texto, largura, esperado):
    linhas = popup._quebrar_texto(texto, largura)

    assert linhas == esperado
    assert "".join(linhas) == texto
    assert all(len(linha) <= largura for linha in linhas)


def test_wrapping_preserva_string_somente_de_espacos():
    linhas = popup._quebrar_texto("     ", 3)

    assert linhas == ["   ", "  "]
    assert "".join(linhas) == "     "
    assert all(len(linha) <= 3 for linha in linhas)


@pytest.mark.parametrize("texto", ["  abc", "abc  ", "  abc  "])
def test_wrapping_preserva_whitespace_nas_extremidades(texto):
    linhas = popup._quebrar_texto(texto, 3)

    assert "".join(linhas) == texto
    assert all(len(linha) <= 3 for linha in linhas)


def test_palavra_maior_que_largura_util_e_dividida_somente_se_inevitavel():
    assert popup._quebrar_texto("abcdefghij", 4) == ["abcd", "efgh", "ij"]


def test_alinhamentos_sao_aplicados_depois_do_wrapping():
    esquerda = popup._formatar_linha("abc", 10, "esquerda", 1)
    centro = popup._formatar_linha("abc", 10, "centralizado", 1)
    justificado = popup._formatar_linha(
        "abc def", 10, "justificado", 1, ultima=False
    )
    ultima = popup._formatar_linha(
        "abc def", 10, "justificado", 1, ultima=True
    )
    assert esquerda[1:4] == "abc"
    assert centro.index("abc") == 3
    assert "abc  def" in justificado
    assert "abc def" in ultima


def test_justificacao_divisivel_distribui_igualmente_e_fecha_largura():
    linha = popup._justificar_linha("a b c", 9)

    assert linha == "a   b   c"
    assert len(linha) == 9


def test_justificacao_com_resto_um_prioriza_o_primeiro_vao():
    linha = popup._justificar_linha("a b c", 8)

    assert linha == "a   b  c"
    assert len(linha) == 8


def test_justificacao_com_resto_maior_distribui_da_esquerda():
    linha = popup._justificar_linha("a b c d", 12)

    assert linha == "a   b   c  d"
    assert len(linha) == 12


def test_justificacao_preserva_whitespace_original_dos_vaos():
    linha = popup._justificar_linha("a  b   c", 13)

    assert linha == "a     b     c"
    assert len(linha) == 13


def test_ultima_linha_justificada_permanece_alinhada_a_esquerda():
    linha = popup._formatar_linha("a b c", 10, "justificado", 1, ultima=True)

    assert linha == " a b c    "
    assert len(linha) == 10


def test_linha_justificada_sem_vao_nao_inventa_espacos_internos():
    linha = popup._formatar_linha("palavra", 12, "justificado", 1, ultima=False)

    assert linha == " palavra    "
    assert len(linha) == 12


def test_altura_derivada_preserva_tres_espacamentos(estilo):
    instancia = _instancia_texto(
        "uma frase com varias palavras para ocupar duas linhas",
        espacamento_superior=0,
        espacamento_conteudo_chips=1,
        espacamento_inferior=0,
    )
    layout = popup._layout_popup(instancia, estilo, largura_corpo=19)
    esperada = (
        2
        + instancia.declaracao["espacamento_superior"]
        + len(layout["linhas_texto"])
        + instancia.declaracao["espacamento_conteudo_chips"]
        + len(layout["linhas_chips"])
        + instancia.declaracao["espacamento_inferior"]
    )
    assert layout["altura"] == esperada


def test_chips_multilinha_preservam_ordem_e_indivisibilidade(estilo):
    chips = [
        _chip("a", "A", "Um"),
        _chip("b", "B", "Dois"),
        _chip("c", "C", "Tres"),
    ]
    linhas = popup._distribuir_chips(chips, 16, estilo)
    assert len(linhas) == 2
    assert "[A]" in linhas[0] and "[B]" in linhas[0]
    assert "[C]" in linhas[1]
    assert all(len(linha) <= 16 for linha in linhas)
    assert linhas[0].index("[A]") < linhas[0].index("[B]")
    with pytest.raises(popup.PopupErro, match="chip isolado"):
        popup._distribuir_chips([_chip("l", "Longa", "Etiqueta")], 5, estilo)


def test_chips_multilinha_aumentam_altura_e_cada_linha_e_centralizada(estilo):
    chips = [_chip("a", "A", "Um"), _chip("b", "B", "Dois"), _chip("c", "C", "Tres")]
    declaracao = _declaracao()
    declaracao["chips"] = chips
    declaracao["_id"] = "popup_teste_chips"
    instancia = popup.PopupInstancia(
        declaracao, {"tipo": "texto", "texto": "curto"}
    )
    layout = popup._layout_popup(instancia, estilo, largura_corpo=23)
    assert len(layout["linhas_chips"]) > 1
    assert layout["altura"] == 2 + 1 + 1 + 1 + len(layout["linhas_chips"]) + 1
    caixa = popup.renderizar_popup(instancia, estilo, largura=23)
    assert all(len(linha) == 23 for linha in caixa.splitlines())


def test_overlay_usa_largura_fisica_do_corpo_e_posicao_deterministica(estilo):
    instancia = _instancia_texto("texto longo para recompor")
    corpo = "\n".join("x" * 24 for _ in range(12))
    primeira = popup.sobrepor_no_corpo(corpo, instancia, estilo, largura=80, altura=12)
    segunda = popup.sobrepor_no_corpo(corpo, instancia, estilo, largura=24, altura=12)
    assert primeira == segunda
    assert popup.geometria_popup(instancia, estilo, largura_corpo=24)["largura"] <= 24
    assert primeira.count("Mensagem") == 1


def test_overlay_sinaliza_altura_inviavel_sem_remover_conteudo(estilo):
    instancia = _instancia_texto("texto que precisa de varias linhas")
    corpo = "\n".join("x" * 19 for _ in range(3))
    with pytest.raises(popup.PopupErro, match="altura derivada"):
        popup.sobrepor_no_corpo(corpo, instancia, estilo, largura=19, altura=3)
