"""Testes focais das amostras visuais H-0064 (derivacao e composicao)."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
from tela.loader import RuntimeEstilo
from tela.renderizacao.estilo import (
    PAYLOAD_CANONICO_CHIP,
    SEPARADOR_NOME_AMOSTRA,
    amostra_borda,
    amostra_chip,
    amostra_incluido,
    amostra_selecionado,
    compor_titulo_com_amostra,
    _codigo_ansi_de_fundo,
)
from tela.renderizacao.texto_ansi import (
    _ANSI_RESET_FG,
    _codigo_ansi_de_cor,
    _ljust_sem_ansi,
    _largura_sem_ansi,
)


RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"

_CAMPOS_BORDA = (
    "canto_superior_esquerdo",
    "canto_superior_direito",
    "canto_inferior_esquerdo",
    "canto_inferior_direito",
    "traco_superior",
    "traco_inferior",
    "lateral",
)


def _runtime(tmp_path=None, mutar=None):
    if tmp_path is None and mutar is None:
        return RuntimeEstilo()
    configuracao = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    if mutar is not None:
        mutar(configuracao)
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(
        json.dumps(configuracao, ensure_ascii=False), encoding="utf-8"
    )
    return RuntimeEstilo(tmp_path)


def _filho_por_preset(controlador, categoria, nome):
    for no_pai in controlador.conteudo.nos:
        if no_pai.campos.get("categoria") != categoria:
            continue
        for no_filho in no_pai.filhos:
            if no_filho.campos.get("preset") == nome:
                return no_filho
    raise AssertionError(
        "filho nao encontrado: {0}/{1}".format(categoria, nome)
    )


def test_quatro_pais_preservados():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    assert tuple(p.nome for p in controlador.pais) == CATEGORIAS_ESTILO


def test_todo_filho_tem_nome_separador_e_amostra_em_uma_linha():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    for categoria in controlador.categorias:
        largura_nome = max(
            _largura_sem_ansi(preset.nome)
            for preset in categoria.presets
        )
        for preset in categoria.presets:
            no = _filho_por_preset(controlador, categoria.nome, preset.nome)
            titulo = no.campos["titulo"]
            assert "\n" not in titulo
            nome_formatado = _ljust_sem_ansi(preset.nome, largura_nome)
            assert titulo.startswith(
                nome_formatado + SEPARADOR_NOME_AMOSTRA
            )
            coluna_amostra = _largura_sem_ansi(
                nome_formatado + SEPARADOR_NOME_AMOSTRA
            )
            amostra = titulo[len(nome_formatado) + len(SEPARADOR_NOME_AMOSTRA) :]
            assert amostra
            assert amostra == amostra_de_categoria(categoria.nome, preset.dados)
            assert _largura_sem_ansi(
                titulo[: len(nome_formatado) + len(SEPARADOR_NOME_AMOSTRA)]
            ) == coluna_amostra


def amostra_de_categoria(categoria, dados):
    if categoria == "borda":
        return amostra_borda(dados)
    if categoria == "chip":
        return amostra_chip(dados)
    if categoria == "indicadores.selecionado":
        return amostra_selecionado(dados)
    if categoria == "indicadores.incluido":
        return amostra_incluido(dados)
    raise AssertionError(categoria)


def test_amostra_borda_incorpora_sete_campos():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    for preset in controlador.filhos["borda"]:
        amostra = amostra_borda(preset.dados)
        for campo in _CAMPOS_BORDA:
            assert campo in preset.dados
            assert preset.dados[campo] in amostra
        esperado = (
            preset.dados["canto_superior_esquerdo"]
            + preset.dados["traco_superior"]
            + preset.dados["canto_superior_direito"]
            + preset.dados["lateral"]
            + preset.dados["lateral"]
            + preset.dados["canto_inferior_esquerdo"]
            + preset.dados["traco_inferior"]
            + preset.dados["canto_inferior_direito"]
        )
        assert amostra == esperado
        titulo = _filho_por_preset(
            controlador, "borda", preset.nome
        ).campos["titulo"]
        assert esperado in titulo


def test_amostra_chip_campos_payload_e_caixa_alta():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    assert PAYLOAD_CANONICO_CHIP == "A"
    for preset in controlador.filhos["chip"]:
        dados = preset.dados
        for campo in (
            "caractere_esquerdo",
            "caractere_direito",
            "caixa_alta",
            "cor_texto",
            "cor_fundo",
        ):
            assert campo in dados
        amostra = amostra_chip(dados)
        payload = (
            PAYLOAD_CANONICO_CHIP.upper()
            if dados["caixa_alta"]
            else PAYLOAD_CANONICO_CHIP
        )
        assert payload == "A"
        assert payload in amostra
        assert "Ab" not in amostra
        assert "AB" not in amostra
        assert dados["caractere_esquerdo"] in amostra
        assert dados["caractere_direito"] in amostra
        # Payload visual: exatamente uma letra ``A`` entre os delimitadores.
        sem_ansi = re.sub(r"\x1b\[\d+m", "", amostra)
        esq = dados["caractere_esquerdo"]
        dir_ = dados["caractere_direito"]
        assert sem_ansi.startswith(esq)
        assert sem_ansi.endswith(dir_)
        fim = len(sem_ansi) - len(dir_) if dir_ else len(sem_ansi)
        assert sem_ansi[len(esq) : fim] == "A"
        assert _largura_sem_ansi(amostra) == len(esq) + 1 + len(dir_)


def test_chip_cor_texto_diferente_produz_ansi_diferente():
    base = {
        "caractere_esquerdo": "<",
        "caractere_direito": ">",
        "caixa_alta": False,
        "cor_texto": "azul",
        "cor_fundo": "padrão",
    }
    outro = dict(base, cor_texto="verde")
    a = amostra_chip(base)
    b = amostra_chip(outro)
    assert a != b
    assert _codigo_ansi_de_cor("azul") in a
    assert _codigo_ansi_de_cor("verde") in b
    assert _ANSI_RESET_FG in a
    assert _ANSI_RESET_FG in b


def test_chip_cor_fundo_diferente_produz_ansi_diferente_e_mesma_largura():
    base = {
        "caractere_esquerdo": " ",
        "caractere_direito": " ",
        "caixa_alta": True,
        "cor_texto": "padrão",
        "cor_fundo": "azul",
    }
    outro = dict(base, cor_fundo="amarelo")
    a = amostra_chip(base)
    b = amostra_chip(outro)
    assert a != b
    assert _codigo_ansi_de_fundo("azul") in a
    assert _codigo_ansi_de_fundo("amarelo") in b
    assert _largura_sem_ansi(a) == _largura_sem_ansi(b)
    # Espelha Destaque Texto vs Destaque Fundo do catalogo real.
    catalogo = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    destaque_texto = amostra_chip(catalogo["chip"]["presets"]["Destaque Texto"])
    destaque_fundo = amostra_chip(catalogo["chip"]["presets"]["Destaque Fundo"])
    assert destaque_texto != destaque_fundo
    assert _largura_sem_ansi(destaque_texto) == _largura_sem_ansi(destaque_fundo)


def test_chip_reset_ansi_nao_vaza_para_conteudo_subsequente():
    dados = {
        "caractere_esquerdo": "[",
        "caractere_direito": "]",
        "caixa_alta": False,
        "cor_texto": "azul",
        "cor_fundo": "amarelo",
    }
    amostra = amostra_chip(dados)
    assert _codigo_ansi_de_cor("azul") in amostra
    assert _codigo_ansi_de_fundo("amarelo") in amostra
    assert _ANSI_RESET_FG in amostra
    assert "\x1b[49m" in amostra
    # Reset ocorre apos o payload/delimitadores da amostra.
    assert amostra.index(PAYLOAD_CANONICO_CHIP) < amostra.rindex(_ANSI_RESET_FG)
    assert amostra.index(PAYLOAD_CANONICO_CHIP) < amostra.rindex("\x1b[49m")
    # Conteudo subsequente na mesma linha permanece apos o reset.
    linha = amostra + " SEGUINTE"
    assert linha.endswith(" SEGUINTE")
    assert linha.rindex(_ANSI_RESET_FG) < linha.index(" SEGUINTE")
    assert linha.rindex("\x1b[49m") < linha.index(" SEGUINTE")


def test_amostra_selecionado_usa_simbolo_do_preset():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    for preset in controlador.filhos["indicadores.selecionado"]:
        assert amostra_selecionado(preset.dados) == preset.dados["simbolo"]
        titulo = _filho_por_preset(
            controlador, "indicadores.selecionado", preset.nome
        ).campos["titulo"]
        assert preset.dados["simbolo"] in titulo


def test_amostra_incluido_expoe_on_e_off_simultaneamente():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    for preset in controlador.filhos["indicadores.incluido"]:
        amostra = amostra_incluido(preset.dados)
        assert preset.dados["on"] in amostra
        assert preset.dados["off"] in amostra
        assert amostra.index(preset.dados["on"]) < amostra.index(
            preset.dados["off"]
        ) or preset.dados["on"] != preset.dados["off"]
        titulo = _filho_por_preset(
            controlador, "indicadores.incluido", preset.nome
        ).campos["titulo"]
        assert amostra in titulo


def test_preset_sintetico_aparece_com_amostra(tmp_path):
    def mutar(config):
        config["borda"]["presets"]["Borda Sintetica QA"] = {
            "canto_superior_esquerdo": "A",
            "canto_superior_direito": "B",
            "canto_inferior_esquerdo": "C",
            "canto_inferior_direito": "D",
            "traco_superior": "E",
            "traco_inferior": "F",
            "lateral": "G",
        }
        config["chip"]["presets"]["Chip Sintetico QA"] = {
            "caractere_esquerdo": "{",
            "caractere_direito": "}",
            "cor_texto": "verde",
            "cor_fundo": "cinza",
            "caixa_alta": True,
        }

    controlador = ControladorTelaEstilo(_runtime(tmp_path, mutar))
    nomes_borda = [p.nome for p in controlador.filhos["borda"]]
    nomes_chip = [p.nome for p in controlador.filhos["chip"]]
    assert "Borda Sintetica QA" in nomes_borda
    assert "Chip Sintetico QA" in nomes_chip

    titulo_borda = _filho_por_preset(
        controlador, "borda", "Borda Sintetica QA"
    ).campos["titulo"]
    assert "AEBGGCFD" in titulo_borda

    titulo_chip = _filho_por_preset(
        controlador, "chip", "Chip Sintetico QA"
    ).campos["titulo"]
    assert "Chip Sintetico QA" in titulo_chip
    assert "A" in titulo_chip
    assert "Ab" not in titulo_chip
    assert "AB" not in titulo_chip
    assert "{" in titulo_chip and "}" in titulo_chip
    assert _codigo_ansi_de_cor("verde") in titulo_chip
    assert _codigo_ansi_de_fundo("cinza") in titulo_chip


def test_compor_titulo_nao_usa_nome_do_preset_para_glifos():
    dados_a = {
        "canto_superior_esquerdo": "1",
        "canto_superior_direito": "2",
        "canto_inferior_esquerdo": "3",
        "canto_inferior_direito": "4",
        "traco_superior": "5",
        "traco_inferior": "6",
        "lateral": "7",
    }
    t1 = compor_titulo_com_amostra("Nome Alpha", "borda", dados_a)
    t2 = compor_titulo_com_amostra("Nome Beta", "borda", dados_a)
    assert t1.endswith("15277364")
    assert t2.endswith("15277364")
    assert t1.startswith("Nome Alpha")
    assert t2.startswith("Nome Beta")


def test_fronteira_navegacao_nao_muta_candidato_nem_config(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    original = CONFIG_ESTILO.read_text(encoding="utf-8")
    destino.write_text(original, encoding="utf-8")
    runtime = RuntimeEstilo(tmp_path)
    baseline = copy.deepcopy(runtime.baseline)
    candidato = copy.deepcopy(runtime.candidato)
    global_antes = runtime.global_vigente

    controlador = ControladorTelaEstilo(runtime)
    # Presenca das amostras nao cria mutacao.
    assert any(
        SEPARADOR_NOME_AMOSTRA in no.campos["titulo"]
        for pai in controlador.conteudo.nos
        for no in pai.filhos
    )
    assert runtime.baseline == baseline
    assert runtime.candidato == candidato
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
    # H-0066: solicitar_aplicacao passa a existir (capacidade compartilhada
    # de ControladorTelaEstilo); acionar/produzir a solicitacao continua
    # fora do escopo de H-0064 e nao muta candidato/baseline/global/arquivo.
    assert hasattr(controlador, "solicitar_aplicacao")
    assert runtime.baseline == baseline
    assert runtime.candidato == candidato
    assert runtime.global_vigente == global_antes
    assert destino.read_text(encoding="utf-8") == original
