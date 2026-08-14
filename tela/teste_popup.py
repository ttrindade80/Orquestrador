"""Testes focais do popup textual H-0056."""

import copy
import re

import pytest

from tela.carregamento.estilo import carregar_estilo
from tela.renderizacao import popup

_RE_ANSI_TESTE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _visivel(texto):
    """Texto sem sequencias SGR, para comparar composicao por coluna visual."""
    return _RE_ANSI_TESTE.sub("", texto)


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


def test_overlay_corpo_com_ansi_usa_largura_visual_e_preserva_borda(estilo):
    """Regressao generica H-0067-P01: uma linha do corpo com SGR ANSI (cujo
    ``len`` bruto excede a largura visual) fora do retangulo do popup nao
    pode inflar ``largura_corpo`` nem deslocar a centralizacao; a borda e o
    conteudo ANSI dessa linha devem sobreviver intactos, byte a byte."""
    instancia = _instancia_texto("confirma")
    intrinseca = popup.geometria_popup(instancia, estilo)["largura"]
    largura_visual = intrinseca + 20
    altura = 12
    ansi_cor = "\x1b[34m"
    ansi_reset = "\x1b[39m"

    linha_plana = "│" + "x" * (largura_visual - 2) + "│"
    linha_ansi = (
        "│" + "x" * 3 + ansi_cor + "Ab" + ansi_reset
        + "x" * (largura_visual - 2 - 3 - 2) + "│"
    )
    assert popup._largura_sem_ansi(linha_ansi) == largura_visual
    assert len(linha_ansi) > largura_visual  # delta introduzido pelo SGR

    linhas_corpo = [linha_plana] * altura
    linhas_corpo[0] = linha_ansi
    linhas_corpo[-1] = linha_ansi
    corpo = "\n".join(linhas_corpo)

    sobreposto = popup.sobrepor_no_corpo(corpo, instancia, estilo, altura=altura)
    linhas = sobreposto.split("\n")
    if linhas and linhas[-1] == "":
        linhas.pop()

    # Nenhuma linha final excede visualmente a viewport do corpo.
    assert all(
        popup._largura_sem_ansi(linha) == largura_visual for linha in linhas
    )

    # Linhas fora do retangulo do popup (extremos, aqui) sao preservadas
    # byte a byte -- inclusive o SGR e a borda direita "│".
    assert linhas[0] == linha_ansi
    assert linhas[-1] == linha_ansi

    # Centralizacao usa a largura VISUAL (identica ao caso sem ANSI), nao o
    # ``len`` bruto inflado pelo SGR das linhas 0/-1.
    largura_popup = popup.geometria_popup(
        instancia, estilo, largura_corpo=largura_visual
    )["largura"]
    x = (largura_visual - largura_popup) // 2
    altura_popup = popup.geometria_popup(
        instancia, estilo, largura_corpo=largura_visual, altura_corpo=altura,
    )["altura"]
    y = (altura - altura_popup) // 2
    linha_topo_popup = linhas[y]
    assert linha_topo_popup[:x] == linha_plana[:x]
    assert linha_topo_popup[-x:] == linha_plana[-x:] if x else True
    assert "Voltar" in sobreposto


def test_overlay_corta_segmento_ansi_no_meio_sem_corromper_sequencia(estilo):
    """Regressao generica H-0067-P01: quando o retangulo do popup CORTA um
    trecho colorido do corpo (abre antes de x, fecha depois de x+largura),
    a composicao final nao pode truncar a sequencia SGR nem embaralhar
    colunas -- o texto visivel (sem SGR) precisa reconstruir exatamente
    prefixo + linha_do_popup + sufixo, coluna a coluna."""
    instancia = _instancia_texto("confirma")
    largura_popup_esperado = popup.geometria_popup(instancia, estilo)["largura"]
    largura_visual = largura_popup_esperado + 40
    altura = 8
    ansi_cor = "\x1b[34m"
    ansi_reset = "\x1b[39m"
    x = (largura_visual - largura_popup_esperado) // 2

    antes = x - 2
    depois = largura_visual - 2 - antes - (largura_popup_esperado + 4)
    assert antes >= 0 and depois >= 0
    linha_original = (
        "│" + "x" * antes + ansi_cor + "x" * (largura_popup_esperado + 4)
        + ansi_reset + "x" * depois + "│"
    )
    assert popup._largura_sem_ansi(linha_original) == largura_visual

    corpo = "\n".join([linha_original] * altura)
    sobreposto = popup.sobrepor_no_corpo(corpo, instancia, estilo, altura=altura)
    linhas = sobreposto.split("\n")
    if linhas and linhas[-1] == "":
        linhas.pop()

    assert all(
        popup._largura_sem_ansi(linha) == largura_visual for linha in linhas
    )

    largura_popup = popup.geometria_popup(
        instancia, estilo, largura_corpo=largura_visual
    )["largura"]
    altura_popup = popup.geometria_popup(
        instancia, estilo, largura_corpo=largura_visual, altura_corpo=altura,
    )["altura"]
    y = (altura - altura_popup) // 2
    caixa = popup.renderizar_popup(
        instancia, estilo, largura=largura_visual, altura=altura,
    ).split("\n")

    for offset, linha_popup in enumerate(caixa):
        linha_final = linhas[y + offset]
        assert "\x1b" not in _visivel(linha_final)
        assert _visivel(linha_final) == (
            _visivel(linha_original)[:x]
            + _visivel(linha_popup)
            + _visivel(linha_original)[x + largura_popup:]
        )


def test_overlay_sinaliza_altura_inviavel_sem_remover_conteudo(estilo):
    instancia = _instancia_texto("texto que precisa de varias linhas")
    corpo = "\n".join("x" * 19 for _ in range(3))
    with pytest.raises(popup.PopupErro, match="altura derivada"):
        popup.sobrepor_no_corpo(corpo, instancia, estilo, largura=19, altura=3)


def _declaracao_marcacao(politica="exclusiva"):
    declaracao = _declaracao()
    declaracao["tipo"] = "marcacao"
    declaracao["marcacao"] = politica
    declaracao["titulo"] = "Lista"
    declaracao["alinhamento"] = "esquerda"
    declaracao["chips"].append(
        {
            "id": "lista_confirmar",
            "tipo": "especifico",
            "tecla": "Enter",
            "texto": "Confirmar",
            "referencia_regra": {"resultado": {"status": "CONFIRMADO"}},
            "regra_existencia": "sempre",
            "regra_ativo": "sempre",
            "forma_exibicao": "ativo",
        }
    )
    return declaracao


def _conteudo_marcacao(
    ids=None, marcados=None, instrucao="Escolha uma opção:", textos=None
):
    ids = ids or ["opcao_1", "opcao_2", "opcao_3", "opcao_4", "opcao_5", "opcao_6"]
    textos = textos or [
        "Opção " + item_id.rsplit("_", 1)[-1] for item_id in ids
    ]
    return {
        "tipo": "marcacao",
        "instrucao": instrucao,
        "itens": [
            {"id": item_id, "texto": texto}
            for item_id, texto in zip(ids, textos)
        ],
        "marcados": list(marcados if marcados is not None else [ids[1]]),
    }


def _instancia_marcacao(
    estilo, politica="exclusiva", ids=None, marcados=None,
    instrucao="Escolha uma opção:", textos=None,
):
    fonte = {"popups": {"lista": _declaracao_marcacao(politica)}}
    instancia = popup.abrir_popup(
        fonte, "lista", _conteudo_marcacao(
            ids=ids, marcados=marcados, instrucao=instrucao, textos=textos
        )
    )
    return instancia


def test_marcacao_valida_separa_declaracao_envelope_e_estado(estilo):
    instancia = _instancia_marcacao(estilo, marcados=["opcao_2"])
    assert instancia.declaracao["marcacao"] == "exclusiva"
    assert instancia.conteudo["tipo"] == "marcacao"
    assert "marcacao" not in instancia.conteudo
    assert instancia.cursor_id == "opcao_1"
    assert instancia.marcados == ["opcao_2"]

    with pytest.raises(popup.PopupErro):
        popup.validar_conteudo_popup({
            "tipo": "marcacao",
            "instrucao": "Escolha",
            "itens": [{"id": "a", "texto": "A"}],
            "marcados": [],
            "extra": True,
        })
    with pytest.raises(popup.PopupErro):
        popup.validar_conteudo_popup({
            "tipo": "marcacao",
            "instrucao": "Escolha",
            "itens": [],
            "marcados": [],
        })
    with pytest.raises(popup.PopupErro):
        popup.validar_conteudo_popup({
            "tipo": "marcacao",
            "instrucao": "Escolha",
            "itens": [{"id": "a", "texto": "A"}, {"id": "a", "texto": "A2"}],
            "marcados": ["a"],
        })
    with pytest.raises(popup.PopupErro):
        popup.validar_conteudo_popup({
            "tipo": "marcacao",
            "instrucao": "Escolha",
            "itens": [{"id": "a", "texto": "A"}],
            "marcados": ["inexistente"],
        })
    declaracao = _declaracao_marcacao("invalida")
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)
    with pytest.raises(popup.PopupErro):
        popup.abrir_popup(
            {"popups": {"lista": _declaracao_marcacao("exclusiva")}},
            "lista",
            _conteudo_marcacao(marcados=[]),
        )


def test_marcacao_renderiza_instrucao_foco_marcas_moldura_e_chip(estilo):
    instancia = _instancia_marcacao(estilo)
    caixa = popup.renderizar_popup(instancia, estilo, largura=50, altura=20)
    assert "Escolha uma opção:" in caixa
    assert "Opção 1" in caixa and "Opção 6" in caixa
    assert getattr(estilo, "selecionado_simbolo") in caixa
    assert getattr(estilo, "incluido_on") in caixa
    assert getattr(estilo, "incluido_off") in caixa
    assert "Esc" in caixa and "Voltar" in caixa
    assert all(len(linha) == 50 for linha in caixa.splitlines())
    assert instancia.cursor_id == "opcao_1"
    assert instancia.marcados == ["opcao_2"]


def test_formacoes_coluna_matriz_linha_e_preenchimento_vertical(estilo):
    coluna = _instancia_marcacao(estilo)
    popup.renderizar_popup(coluna, estilo, largura=50, altura=20)
    assert coluna.formacao == "coluna"
    assert coluna.grade == tuple(("opcao_{}".format(indice),) for indice in range(1, 7))

    matriz = _instancia_marcacao(estilo)
    popup.renderizar_popup(matriz, estilo, largura=40, altura=10)
    assert matriz.formacao == "matriz"
    assert matriz.grade == (
        ("opcao_1", "opcao_4"),
        ("opcao_2", "opcao_5"),
        ("opcao_3", "opcao_6"),
    )

    linha = _instancia_marcacao(estilo)
    popup.renderizar_popup(linha, estilo, largura=100, altura=8)
    assert linha.formacao == "linha"
    assert linha.grade == (
        tuple("opcao_{}".format(indice) for indice in range(1, 7)),
    )


def test_matriz_maximiza_colunas_reais_e_rejeita_colunas_vazias():
    ids = ["a", "b", "c", "d", "e", "f", "g"]
    larguras = [5] * len(ids)

    formacao, colunas = popup._selecionar_formacao(
        ids, larguras, largura_util=26, linhas_disponiveis=2
    )

    assert formacao == "matriz"
    assert len(colunas) == 4
    assert all(colunas)
    assert [item_id for coluna in colunas for item_id in coluna] == ids

    colunas_nominais = popup._colunas_formacao(ids, larguras, 10)
    assert len(colunas_nominais) == len(ids)
    assert all(colunas_nominais)
    _, grade = popup._grade_para_formacao(
        ids, "matriz", colunas=colunas_nominais
    )
    assert grade == [["a", "b", "c", "d", "e", "f", "g"]]


def test_matriz_tem_duas_linhas_e_linha_exige_uma_linha_disponivel():
    ids = ["a", "b", "c", "d", "e", "f"]
    larguras = [5] * len(ids)

    formacao, colunas = popup._selecionar_formacao(
        ids, larguras, largura_util=40, linhas_disponiveis=2
    )
    assert formacao == "matriz"
    assert max(len(coluna) for coluna in colunas) >= 2

    formacao, colunas = popup._selecionar_formacao(
        ids, larguras, largura_util=40, linhas_disponiveis=1
    )
    assert formacao == "linha"
    assert colunas == [ids]

    with pytest.raises(popup.PopupErro, match="altura disponivel"):
        popup._selecionar_formacao(
            ids, larguras, largura_util=10, linhas_disponiveis=2
        )


def test_vano_da_formacao_e_unico_no_calculo_e_na_saida(estilo):
    instancia = _instancia_marcacao(estilo, ids=["a", "b"])
    itens = instancia.conteudo["itens"]
    larguras = [
        popup._largura_item_marcacao(item["texto"], estilo)
        for item in itens
    ]
    largura_linha = sum(larguras) + popup._VAO_ENTRE_ITENS_POPUP
    largura_corpo = 3 + 2 * instancia.declaracao["espacamento_horizontal"] + largura_linha
    preliminar = popup._layout_popup_marcacao(
        instancia, estilo, largura_corpo=largura_corpo
    )
    overhead = preliminar["altura"] - len(preliminar["linhas_itens"])
    layout = popup._layout_popup_marcacao(
        instancia,
        estilo,
        largura_corpo=largura_corpo,
        altura_corpo=overhead + 1,
    )
    partes = [
        popup._texto_item_marcacao(instancia, item, estilo)
        for item in itens
    ]

    assert popup._VAO_ENTRE_ITENS_POPUP == 2
    assert layout["formacao"] == "linha"
    assert layout["largura_util"] == largura_linha
    assert layout["linhas_itens"] == [
        (" " * popup._VAO_ENTRE_ITENS_POPUP).join(partes)
    ]


def test_largura_integral_do_item_considera_indicadores_e_texto(estilo):
    texto = "texto integral sem truncamento"
    largura = popup._largura_item_marcacao(texto, estilo)
    esperada = (
        max(
            popup._largura_sem_ansi(getattr(estilo, "selecionado_simbolo")),
            popup._largura_sem_ansi(getattr(estilo, "selecionado_off")),
        )
        + max(
            popup._largura_sem_ansi(getattr(estilo, "incluido_on")),
            popup._largura_sem_ansi(getattr(estilo, "incluido_off")),
        )
        + 1
        + len(texto)
    )
    assert largura == esperada

    instancia = _instancia_marcacao(
        estilo, ids=["item"], marcados=["item"], textos=[texto]
    )
    caixa = popup.renderizar_popup(instancia, estilo, largura=largura + 7, altura=10)
    assert texto in caixa
    assert "..." not in caixa


def test_overhead_de_marcacao_desconta_instrucao_e_chips_wrapped(estilo):
    instancia = _instancia_marcacao(
        estilo,
        ids=["a", "b", "c", "d", "e", "f"],
        instrucao="Instrucao longa para ocupar mais de uma linha fisica",
    )
    layout = popup._layout_popup_marcacao(
        instancia, estilo, largura_corpo=30, altura_corpo=20
    )
    esperado = (
        2
        + instancia.declaracao["espacamento_superior"]
        + len(layout["linhas_instrucao"])
        + instancia.declaracao["espacamento_conteudo_chips"]
        + len(layout["linhas_chips"])
        + instancia.declaracao["espacamento_inferior"]
        + len(layout["linhas_itens"])
    )

    assert len(layout["linhas_instrucao"]) > 1
    assert len(layout["linhas_chips"]) > 1
    assert layout["altura"] == esperado


def test_wrapping_da_instrucao_muda_formacao_na_fronteira_e_materializa(estilo):
    largura, altura = 55, 13
    curta = _instancia_marcacao(estilo, instrucao="Escolha uma opção:")
    longa = _instancia_marcacao(
        estilo,
        instrucao="Instrucao longa para ocupar mais de uma linha fisica",
    )

    layout_curta = popup._layout_popup_marcacao(
        curta, estilo, largura_corpo=largura, altura_corpo=altura
    )
    layout_longa = popup._layout_popup_marcacao(
        longa, estilo, largura_corpo=largura, altura_corpo=altura
    )
    saida_curta = popup.renderizar_popup(
        curta, estilo, largura=largura, altura=altura
    )
    saida_longa = popup.renderizar_popup(
        longa, estilo, largura=largura, altura=altura
    )

    assert len(layout_curta["linhas_instrucao"]) == 1
    assert len(layout_longa["linhas_instrucao"]) == 2
    assert layout_curta["formacao"] == "coluna"
    assert layout_longa["formacao"] == "matriz"
    assert len(saida_curta.splitlines()) == 13
    assert len(saida_longa.splitlines()) == 10
    assert "Escolha uma opção:" in saida_curta
    assert "Instrucao longa" in saida_longa and "fisica" in saida_longa
    assert all(
        item["texto"] in saida_curta for item in curta.conteudo["itens"]
    )
    assert all(
        item["texto"] in saida_longa for item in longa.conteudo["itens"]
    )


def test_wrapping_dos_chips_muda_formacao_na_fronteira_e_materializa(estilo):
    altura = 13
    larga = _instancia_marcacao(estilo)
    estreita = _instancia_marcacao(estilo)

    layout_larga = popup._layout_popup_marcacao(
        larga, estilo, largura_corpo=40, altura_corpo=altura
    )
    layout_estreita = popup._layout_popup_marcacao(
        estreita, estilo, largura_corpo=35, altura_corpo=altura
    )
    saida_larga = popup.renderizar_popup(
        larga, estilo, largura=40, altura=altura
    )
    saida_estreita = popup.renderizar_popup(
        estreita, estilo, largura=35, altura=altura
    )

    assert len(layout_larga["linhas_chips"]) == 1
    assert len(layout_estreita["linhas_chips"]) == 2
    assert layout_larga["formacao"] == "coluna"
    assert layout_estreita["formacao"] == "matriz"
    assert len(saida_larga.splitlines()) == 13
    assert len(saida_estreita.splitlines()) == 11
    assert all(
        item["texto"] in saida_larga for item in larga.conteudo["itens"]
    )
    assert all(
        item["texto"] in saida_estreita for item in estreita.conteudo["itens"]
    )


def test_navegacao_toroidal_e_eixos_sem_movimento(estilo):
    coluna = _instancia_marcacao(estilo)
    popup.renderizar_popup(coluna, estilo, largura=50, altura=20)
    assert popup.consumir_tecla_popup(coluna, "\x1b[A") == {"movimento": "MOVIDO"}
    assert coluna.cursor_id == "opcao_6"
    assert popup.consumir_tecla_popup(coluna, "\x1b[C") == {"movimento": "SEM_MOVIMENTO"}

    linha = _instancia_marcacao(estilo)
    popup.renderizar_popup(linha, estilo, largura=100, altura=8)
    assert popup.consumir_tecla_popup(linha, "\x1b[D") == {"movimento": "MOVIDO"}
    assert linha.cursor_id == "opcao_6"
    assert popup.consumir_tecla_popup(linha, "\x1b[A") == {"movimento": "SEM_MOVIMENTO"}

    matriz = _instancia_marcacao(
        estilo, ids=["a", "b", "c", "d", "e"], marcados=["b"]
    )
    popup.renderizar_popup(matriz, estilo, largura=41, altura=9)
    assert matriz.formacao == "matriz"
    assert matriz.grade == (("a", "c", "e"), ("b", "d"))
    assert popup.consumir_tecla_popup(matriz, "\x1b[C") == {"movimento": "MOVIDO"}
    assert matriz.cursor_id == "c"
    assert popup.consumir_tecla_popup(matriz, "\x1b[C") == {"movimento": "MOVIDO"}
    assert matriz.cursor_id == "e"
    assert popup.consumir_tecla_popup(matriz, "\x1b[A") == {"movimento": "SEM_MOVIMENTO"}
    assert popup.consumir_tecla_popup(matriz, "\x1b[C") == {"movimento": "MOVIDO"}
    assert matriz.cursor_id == "a"

    matriz_completa = _instancia_marcacao(estilo)
    popup.renderizar_popup(matriz_completa, estilo, largura=40, altura=10)
    assert popup.consumir_tecla_popup(matriz_completa, "\x1b[B") == {
        "movimento": "MOVIDO"
    }
    assert matriz_completa.cursor_id == "opcao_2"
    assert popup.consumir_tecla_popup(matriz_completa, "\x1b[A") == {
        "movimento": "MOVIDO"
    }
    assert matriz_completa.cursor_id == "opcao_1"
    assert popup.consumir_tecla_popup(matriz_completa, "\x1b[C") == {
        "movimento": "MOVIDO"
    }
    assert matriz_completa.cursor_id == "opcao_4"
    assert popup.consumir_tecla_popup(matriz_completa, "\x1b[D") == {
        "movimento": "MOVIDO"
    }
    assert matriz_completa.cursor_id == "opcao_1"


def test_marcacao_exclusiva_transfere_e_nao_muda_no_item_marcado(estilo):
    instancia = _instancia_marcacao(estilo, marcados=["opcao_2"])
    assert instancia.marcados == ["opcao_2"]
    assert popup.consumir_tecla_popup(instancia, " ") == {"marcacao": "TRANSFERIDA"}
    assert instancia.marcados == ["opcao_1"]
    assert popup.consumir_tecla_popup(instancia, " ") == {"marcacao": "SEM_MUDANCA"}
    assert instancia.cursor_id == "opcao_1"
    assert popup.consumir_tecla_popup(instancia, "\x1b[B") == {"movimento": "MOVIDO"}
    assert instancia.marcados == ["opcao_1"]


def test_marcacao_multipla_alterna_e_preserva_ordem_declarada(estilo):
    instancia = _instancia_marcacao(
        estilo, politica="multipla", marcados=["opcao_4", "opcao_2"]
    )
    assert instancia.marcados == ["opcao_2", "opcao_4"]
    assert popup.consumir_tecla_popup(instancia, " ") == {"marcacao": "MARCADA"}
    assert instancia.marcados == ["opcao_1", "opcao_2", "opcao_4"]
    assert popup.consumir_tecla_popup(instancia, " ") == {"marcacao": "DESMARCADA"}
    assert instancia.marcados == ["opcao_2", "opcao_4"]
    assert popup.consumir_tecla_popup(instancia, "\x1b[B") == {"movimento": "MOVIDO"}
    assert instancia.marcados == ["opcao_2", "opcao_4"]


def test_resize_preserva_instancia_cursor_marcacoes_e_recomposicao(estilo):
    instancia = _instancia_marcacao(estilo, politica="multipla")
    identidade = instancia
    popup.renderizar_popup(instancia, estilo, largura=50, altura=20)
    popup.consumir_tecla_popup(instancia, "\x1b[B")
    popup.consumir_tecla_popup(instancia, " ")
    cursor = instancia.cursor_id
    marcados = instancia.marcados
    popup.renderizar_popup(instancia, estilo, largura=40, altura=10)
    assert instancia is identidade
    assert instancia.cursor_id == cursor
    assert instancia.marcados == marcados
    assert all(item_id.startswith("opcao_") for item_id in instancia.marcados)
    popup.renderizar_popup(instancia, estilo, largura=50, altura=20)
    assert instancia is identidade
    assert instancia.cursor_id == cursor
    assert instancia.marcados == marcados


def test_resize_recalcula_formacao_na_mesma_instancia_preservando_ids(estilo):
    instancia = _instancia_marcacao(estilo, politica="multipla")
    identidade = instancia
    conteudo = copy.deepcopy(instancia.conteudo)

    popup.renderizar_popup(instancia, estilo, largura=50, altura=20)
    assert instancia.formacao == "coluna"
    popup.consumir_tecla_popup(instancia, "\x1b[B")
    popup.consumir_tecla_popup(instancia, "\x1b[B")
    popup.consumir_tecla_popup(instancia, " ")
    cursor = instancia.cursor_id
    marcados = instancia.marcados
    assert cursor == "opcao_3"
    assert marcados == ["opcao_2", "opcao_3"]

    popup.renderizar_popup(instancia, estilo, largura=40, altura=10)
    assert instancia is identidade
    assert instancia.formacao == "matriz"
    assert instancia.grade == (
        ("opcao_1", "opcao_4"),
        ("opcao_2", "opcao_5"),
        ("opcao_3", "opcao_6"),
    )
    assert instancia.cursor_id == cursor
    assert instancia.marcados == marcados

    popup.renderizar_popup(instancia, estilo, largura=77, altura=8)
    assert instancia is identidade
    assert instancia.formacao == "linha"
    assert instancia.grade == (
        ("opcao_1", "opcao_2", "opcao_3", "opcao_4", "opcao_5", "opcao_6"),
    )
    assert instancia.cursor_id == cursor
    assert instancia.marcados == marcados

    popup.renderizar_popup(instancia, estilo, largura=50, altura=20)
    assert instancia is identidade
    assert instancia.formacao == "coluna"
    assert instancia.grade == tuple(
        ("opcao_{}".format(indice),) for indice in range(1, 7)
    )
    assert instancia.cursor_id == cursor
    assert instancia.marcados == marcados
    assert instancia.conteudo == conteudo


def test_confirmacao_exclusiva_devolve_id_vivo_sem_campos_fisicos(estilo):
    instancia = _instancia_marcacao(estilo, marcados=["opcao_2"])
    resultado = popup.consumir_tecla_popup(instancia, "\r")

    assert resultado == {"status": "CONFIRMADO", "valor": "opcao_2"}
    assert set(resultado) == {"status", "valor"}
    assert all(
        campo not in resultado
        for campo in ("cursor", "cursor_id", "formacao", "grade", "coordenadas", "historico")
    )
    assert popup.consumir_tecla_popup(instancia, "\n") is None


def test_confirmacao_multipla_preserva_ordem_logica_declarada(estilo):
    instancia = _instancia_marcacao(
        estilo, politica="multipla", marcados=["opcao_4", "opcao_2"]
    )
    instancia._estado["marcados"] = ["opcao_4", "opcao_2"]

    assert popup.consumir_tecla_popup(instancia, "\n") == {
        "status": "CONFIRMADO",
        "valor": ["opcao_2", "opcao_4"],
    }


def test_confirmacao_multipla_vazia_devolve_lista_vazia(estilo):
    instancia = _instancia_marcacao(estilo, politica="multipla", marcados=[])

    assert popup.consumir_tecla_popup(instancia, "\r") == {
        "status": "CONFIRMADO",
        "valor": [],
    }


def test_enter_sem_regra_compativel_e_texto_permanecem_abertos(estilo):
    fonte = {"popups": {"lista": _declaracao_marcacao()}}
    fonte["popups"]["lista"]["chips"] = fonte["popups"]["lista"]["chips"][:1]
    instancia = popup.abrir_popup(fonte, "lista", _conteudo_marcacao())
    assert popup.consumir_tecla_popup(instancia, "\r") is None
    assert instancia.marcados == ["opcao_2"]

    textual = popup.abrir_popup(_fonte(), "popup_basico", _conteudo())
    assert popup.consumir_tecla_popup(textual, "\n") is None
    assert popup.consumir_tecla_popup(textual, "\x1b") == {"status": "ABORTADO"}


def _declaracao_texto_com_enter():
    declaracao = _declaracao()
    declaracao["chips"].append(
        {
            "id": "popup_texto_confirmar",
            "tipo": "especifico",
            "tecla": "Enter",
            "texto": "Confirmar",
            "referencia_regra": {"resultado": {"status": "CONFIRMADO"}},
            "regra_existencia": "sempre",
            "regra_ativo": "sempre",
            "forma_exibicao": "ativo",
        }
    )
    return declaracao


def test_texto_com_enter_declaracao_valida_e_confirmado_sem_valor(estilo):
    declaracao = _declaracao_texto_com_enter()
    validada = popup.validar_declaracao_popup(declaracao)
    assert len(validada["chips"]) == 2
    assert validada["chips"][1]["tecla"] == "Enter"

    fonte = {"popups": {"popup_texto_confirmacao": declaracao}}
    instancia = popup.abrir_popup(
        fonte, "popup_texto_confirmacao", _conteudo()
    )
    resultado = popup.consumir_tecla_popup(instancia, "\r")
    assert resultado == {"status": "CONFIRMADO"}
    assert "valor" not in resultado
    assert set(resultado) == {"status"}
    # Segunda confirmacao apos terminal nao reabre contrato.
    assert popup.consumir_tecla_popup(instancia, "\n") is None


def test_texto_com_enter_lf_equivalente_e_esc_abortado(estilo):
    fonte = {"popups": {"popup_texto_confirmacao": _declaracao_texto_com_enter()}}
    instancia = popup.abrir_popup(
        fonte, "popup_texto_confirmacao", _conteudo()
    )
    assert popup.consumir_tecla_popup(instancia, "\n") == {"status": "CONFIRMADO"}

    instancia = popup.abrir_popup(
        fonte, "popup_texto_confirmacao", _conteudo()
    )
    resultado = popup.consumir_tecla_popup(instancia, "\x1b")
    assert resultado == {"status": "ABORTADO"}
    assert "valor" not in resultado


def test_texto_com_enter_invalido_continua_rejeitado():
    declaracao = _declaracao_texto_com_enter()
    declaracao["chips"][1]["texto"] = "Aplicar"
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)

    declaracao = _declaracao_texto_com_enter()
    declaracao["chips"][1]["referencia_regra"] = {
        "resultado": {"status": "ABORTADO"}
    }
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)

    # Marcacao continua exigida para politica exclusiva.
    declaracao = _declaracao()
    declaracao["marcacao"] = "exclusiva"
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)


@pytest.mark.parametrize(
    "alteracao",
    [
        lambda instancia: instancia._estado.update(marcados=[]),
        lambda instancia: instancia._estado.update(marcados=["opcao_2", "opcao_2"]),
        lambda instancia: instancia._estado.update(marcados=["nao_existe"]),
    ],
)
def test_confirmacao_rejeita_estado_vivo_invalido_sem_fabricar_valor(estilo, alteracao):
    instancia = _instancia_marcacao(estilo, marcados=["opcao_2"])
    alteracao(instancia)

    assert popup.consumir_tecla_popup(instancia, "\r") is None
    assert popup.consumir_tecla_popup(instancia, "\x1b") == {"status": "ABORTADO"}


def test_regra_enter_incompativel_e_chip_esc_com_payload_falham_fechadamente():
    declaracao = _declaracao_marcacao()
    declaracao["chips"][1]["referencia_regra"] = {
        "resultado": {"status": "ABORTADO"}
    }
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)

    declaracao = _declaracao()
    declaracao["chips"][0]["referencia_regra"]["resultado"]["valor"] = "x"
    with pytest.raises(popup.PopupErro):
        popup.validar_declaracao_popup(declaracao)


def test_esc_aborta_sem_valor_depois_de_marcacao(estilo):
    instancia = _instancia_marcacao(estilo, politica="multipla", marcados=["opcao_2"])
    popup.consumir_tecla_popup(instancia, " ")

    resultado = popup.consumir_tecla_popup(instancia, "\x1b")
    assert resultado == {"status": "ABORTADO"}
    assert "valor" not in resultado
