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
