"""Prova dos 18 criterios de H-0073 sobre a tela real H-0063.

Obtem ``amostra`` por comparacao com ``amostra_de_preset``, nunca por
parsing de ``titulo``. Nao altera ``tela/teste_estilo_h0070.py``.

Apenas biblioteca padrao do Python + pytest.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
from tela.loader import RuntimeEstilo, carregar_tela
from tela.modelo import construir_modelo
from tela import navegacao
from tela import selecao
from tela.renderizacao.conteudo_externo import (
    _linhas_dois_niveis_formatado_com_mapa,
)
from tela.renderizacao.composicao_textual import compor_texto
from tela.renderizacao.estilo import (
    amostra_de_preset,
    compor_titulo_com_amostra,
)
from tela.renderizacao.texto_ansi import (
    _ANSI_RESET_BG,
    _cortar_sem_ansi,
    _largura_sem_ansi,
)


RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"
RAIZ_TELAS_DEMO = RAIZ / "config" / "telas" / "demo"
ID_TELA = "h0063_estilo_estrutura_navegacao_dois_niveis"
CAMINHO_H0063 = RAIZ_TELAS_DEMO / (
    "h0063_estilo_estrutura_navegacao_dois_niveis.json"
)
CAMINHO_H0062 = RAIZ_TELAS_DEMO / "h0062_estilo.json"
_CHAVES_VISUAIS = frozenset({
    "tabulacao", "designador", "apresentacao", "tabela", "formato",
    "prefixo", "sufixo", "espacamento", "colunas",
})


def _modelo_estilo():
    return construir_modelo(carregar_tela(None, ID_TELA, RAIZ_TELAS_DEMO))


def _abrir(runtime=None):
    runtime = runtime or RuntimeEstilo()
    controlador = ControladorTelaEstilo(runtime)
    modelo = controlador.aplicar_ao_modelo(_modelo_estilo())
    estado = controlador.inicializar_estado(
        {"cursores": {}, "selecoes": {}, "foco_console": 0},
        modelo,
    )
    return runtime, controlador, estado, modelo


def _config_filho(modelo):
    console = next(e for e in modelo.corpo.elementos if e.tipo == "console")
    return console.formato_filho_dois_niveis


def _filhos_por_categoria(controlador, categoria):
    pai = next(
        no for no in controlador.conteudo.nos
        if no.campos.get("categoria") == categoria
    )
    return list(pai.filhos)


def _renderizar(controlador, content_w, corrente=None, selecoes=None):
    estilo = controlador.runtime.global_vigente
    config = _config_filho(_modelo_estilo())
    if corrente is None:
        corrente = _filhos_por_categoria(controlador, "borda")[0].id
    if selecoes is None:
        selecoes = set(controlador.ids_escolha_inicial)
    return _linhas_dois_niveis_formatado_com_mapa(
        controlador.conteudo,
        config,
        content_w,
        no_corrente_id=corrente,
        indicador=estilo.selecionado_simbolo,
        indicador_off=estilo.selecionado_off,
        selecoes=selecoes,
        incluir_selecao=True,
        incluido_on=estilo.incluido_on,
        incluido_off=estilo.incluido_off,
    )


def _entrada(entradas, id_no):
    return next(e for e in entradas if e["id"] == id_no)


def test_01_02_03_04_05_projecao_preset_titulo_amostra_sem_parsing():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    for categoria in controlador.categorias:
        largura_nome = max(
            len(preset.nome) for preset in categoria.presets
        )
        for preset in categoria.presets:
            no = next(
                filho for filho in _filhos_por_categoria(
                    controlador, categoria.nome
                )
                if filho.campos["preset"] == preset.nome
            )
            esperado_amostra = amostra_de_preset(categoria.nome, preset.dados)
            esperado_titulo = compor_titulo_com_amostra(
                preset.nome, categoria.nome, preset.dados,
                largura_nome=largura_nome,
            )
            assert no.campos["preset"] == preset.nome
            assert no.campos["titulo"] == esperado_titulo
            assert "amostra" in no.campos
            assert no.campos["amostra"] == esperado_amostra
            assert no.campos["amostra"] is not no.campos["titulo"]


def test_06_07_08_09_10_configuracao_estrutural_tabulacao_tabela():
    bruto = json.loads(CAMINHO_H0063.read_text(encoding="utf-8"))
    filho = bruto["corpo"]["elementos"][0]["formato"]["dois_niveis_por_foco"][
        "filho"
    ]
    assert filho["tabulacao"] == {"minimo": 5, "maximo": 10}
    assert filho["designador"] == {"tipo": "nenhum"}
    assert filho["apresentacao"] == "tabela"
    assert [c["campo"] for c in filho["tabela"]["colunas"]] == [
        "preset", "amostra",
    ]
    assert filho["tabela"]["espacamento"] == {"minimo": 3, "maximo": 8}

    modelo = _modelo_estilo()
    config = _config_filho(modelo)
    assert config["tabulacao"] == {"minimo": 5, "maximo": 10}
    assert config["designador"]["tipo"] == "nenhum"
    assert config["apresentacao"] == "tabela"
    assert [c["campo"] for c in config["tabela"]["colunas"]] == [
        "preset", "amostra",
    ]
    assert config["tabela"]["espacamento"] == {"minimo": 3, "maximo": 8}


def test_11_alinhamento_entre_pais_diferentes():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    entradas = _renderizar(controlador, 160)
    filho_borda = _filhos_por_categoria(controlador, "borda")[0]
    filho_chip = _filhos_por_categoria(controlador, "chip")[0]
    linha_borda = _entrada(entradas, filho_borda.id)["linhas"][0]
    linha_chip = _entrada(entradas, filho_chip.id)["linhas"][0]
    pos_borda = linha_borda.index(filho_borda.campos["amostra"])
    pos_chip = linha_chip.index(filho_chip.campos["amostra"])
    assert pos_borda == pos_chip
    assert linha_borda.index(filho_borda.campos["preset"]) == linha_chip.index(
        filho_chip.campos["preset"]
    )


def test_12_13_unidade_deslocada_sem_designador_visual():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    filho = _filhos_por_categoria(controlador, "borda")[0]
    estilo = controlador.runtime.global_vigente
    entradas = _renderizar(controlador, 160, corrente=filho.id)
    linha = _entrada(entradas, filho.id)["linhas"][0]
    pos_ec = linha.index(estilo.selecionado_simbolo)
    assert 5 <= pos_ec <= 10
    pos_tg = linha.index(estilo.incluido_on)
    pos_preset = linha.index(filho.campos["preset"])
    pos_amostra = linha.index(filho.campos["amostra"])
    assert pos_ec < pos_tg < pos_preset < pos_amostra
    assert "A)" not in linha
    assert "B)" not in linha
    assert "1.1" not in linha
    irmao = _filhos_por_categoria(controlador, "borda")[1]
    linha_irmao = _entrada(entradas, irmao.id)["linhas"][0]
    assert linha_irmao.index(estilo.incluido_off) == pos_tg
    assert estilo.selecionado_simbolo not in linha_irmao[:pos_preset]


def test_14_conteudo_visual_preset_e_amostra_preservados():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    entradas = _renderizar(controlador, 200)
    for categoria in controlador.categorias:
        for preset in categoria.presets:
            no = next(
                filho for filho in _filhos_por_categoria(
                    controlador, categoria.nome
                )
                if filho.campos["preset"] == preset.nome
            )
            linha = _entrada(entradas, no.id)["linhas"][0]
            assert preset.nome in linha
            assert no.campos["amostra"] in linha
            assert no.campos["amostra"] == amostra_de_preset(
                categoria.nome, preset.dados
            )


def test_15_navegacao_e_selecao_preservadas():
    runtime, controlador, estado, modelo = _abrir()
    console = controlador.console_do_modelo(modelo)
    assert navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"
    iniciais = list(estado["selecoes"][console.id])
    assert len(iniciais) == 4
    estado = navegacao.entrar_nivel_filhos(estado, console)
    assert navegacao.em_nivel_filhos(estado, console) is True
    movido = navegacao.mover_baixo(estado, console)
    assert movido["cursores"][console.id] != estado["cursores"][console.id]
    assert movido["selecoes"][console.id] == iniciais
    pais = navegacao.retornar_nivel_pais(movido, console)
    assert navegacao.em_nivel_filhos(pais, console) is False
    assert pais["selecoes"][console.id] == iniciais
    assert selecao.limpar(pais, console)["selecoes"][console.id] == iniciais


def test_16_candidato_baseline_aplicacao_persistencia_publicacao():
    runtime = RuntimeEstilo()
    baseline = copy.deepcopy(runtime.baseline)
    candidato = copy.deepcopy(runtime.candidato)
    global_antes = runtime.global_vigente
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    controlador = ControladorTelaEstilo(runtime)
    assert runtime.baseline == baseline
    assert runtime.candidato == candidato
    assert runtime.global_vigente == global_antes
    assert CONFIG_ESTILO.read_text(encoding="utf-8") == original
    assert controlador.aplicar_disponivel is False
    assert controlador.solicitar_aplicacao() is None
    assert controlador.escolhas_iniciais["borda"] == baseline["borda"][
        "preset_default"
    ]


def test_17_resize_recalcula_disposicao_preservando_item():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    corrente = _filhos_por_categoria(controlador, "borda")[0].id
    larga = _renderizar(controlador, 180, corrente=corrente)
    estreita = _renderizar(controlador, 36, corrente=corrente)
    ids_larga = [e["id"] for e in larga]
    ids_estreita = [e["id"] for e in estreita]
    assert ids_larga == ids_estreita
    assert corrente in ids_larga
    linha_larga = _entrada(larga, corrente)["linhas"][0]
    linha_estreita = _entrada(estreita, corrente)["linhas"][0]
    assert 5 <= linha_larga.index("→") <= 10
    assert 5 <= linha_estreita.index("→") <= 10
    assert (
        linha_larga != linha_estreita
        or len(_entrada(estreita, corrente)["linhas"])
        != len(_entrada(larga, corrente)["linhas"])
    )


def test_18_configuracao_visual_fora_dos_dados():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    bruto = json.loads(CAMINHO_H0063.read_text(encoding="utf-8"))
    assert "formato" in bruto["corpo"]["elementos"][0]
    for pai in controlador.conteudo.nos:
        assert _CHAVES_VISUAIS.isdisjoint(pai.campos)
        for filho in pai.filhos:
            assert _CHAVES_VISUAIS.isdisjoint(filho.campos)
            assert "preset" in filho.campos
            assert "titulo" in filho.campos
            assert "amostra" in filho.campos
    raw = controlador.conteudo._raw
    assert "formato" in raw
    assert "dois_niveis_por_foco" not in json.dumps(raw, ensure_ascii=False)


def test_h0062_permanece_intocado():
    import subprocess
    rel = "config/telas/demo/h0062_estilo.json"
    committed = subprocess.check_output(
        ["git", "show", "HEAD:{0}".format(rel)], cwd=str(RAIZ)
    )
    assert CAMINHO_H0062.read_bytes() == committed


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


def test_fatiamento_por_bytes_parte_csi_corte_ansi_aware_nao():
    amostra = "\x1b[44m A \x1b[49m"
    linha = "            ○ Destaque Fundo     " + amostra
    limite_no_csi = len(linha) - 1
    fatiado = linha[:limite_no_csi]
    assert fatiado.endswith("\x1b[49")
    assert "\x1b[49m" not in fatiado
    assert _csi_incompleto(fatiado)

    vis = _largura_sem_ansi(linha)
    assert vis < limite_no_csi
    seguro = _cortar_sem_ansi(linha, limite_no_csi)
    assert seguro == linha
    assert "\x1b[49m" in seguro
    assert not _csi_incompleto(seguro)
    assert _largura_sem_ansi(seguro) == vis

    vis_antes_reset = _largura_sem_ansi("Destaque Fundo ") + 2
    cortado = _cortar_sem_ansi("Destaque Fundo " + amostra, vis_antes_reset)
    assert "\x1b[44m" in cortado
    assert cortado.endswith(_ANSI_RESET_BG)
    assert not _csi_incompleto(cortado)
    assert _largura_sem_ansi(cortado) == vis_antes_reset
    assert not cortado.endswith("\x1b[49")


def test_quebrar_texto_ansi_nao_parte_csi_nem_vaza_fundo():
    # Duas palavras estilizadas exercitam a quebra lexical; nenhuma palavra
    # deve ser dividida apenas porque a largura util e estreita.
    amostra = "\x1b[44m A B \x1b[49m"
    unica = compor_texto(amostra, 10)
    assert unica == [amostra]
    assert unica[0].endswith(_ANSI_RESET_BG)

    estreita = compor_texto(amostra, 1)
    assert len(estreita) >= 2
    for frag in estreita:
        assert not _csi_incompleto(frag)
        assert _ANSI_RESET_BG in frag
        assert _largura_sem_ansi(frag) <= 1
    assert estreita[0].startswith("\x1b[44m")
    assert "\x1b[44m" in estreita[1]
    seguinte = "linha posterior neutra"
    assert "\x1b[" not in seguinte
    assert estreita[-1].endswith(_ANSI_RESET_BG)

    compacta = compor_texto(amostra, 2)
    assert all(not _csi_incompleto(frag) for frag in compacta)
    assert all(_ANSI_RESET_BG in frag for frag in compacta)
