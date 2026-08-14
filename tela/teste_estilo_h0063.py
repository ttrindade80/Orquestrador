"""Testes focais do controlador e projecao H-0063."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
from tela.loader import RuntimeEstilo
from tela import navegacao
from tela import selecao


RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"


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


def test_exatamente_quatro_pais_sem_categorias_fora_de_escopo():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    assert tuple(p.nome for p in controlador.pais) == CATEGORIAS_ESTILO
    nomes = {p.nome for p in controlador.pais}
    assert "tiling" not in nomes
    assert "cor_inativo" not in nomes
    assert "cor_alerta" not in nomes
    assert "indicadores.concluido" not in nomes


def test_filhos_derivam_dinamicamente_dos_presets_e_sintetico_aparece(tmp_path):
    def mutar(config):
        padrao = config["chip"]["preset_default"]
        config["chip"]["presets"]["Fixture Sintetica"] = copy.deepcopy(
            config["chip"]["presets"][padrao]
        )

    controlador = ControladorTelaEstilo(_runtime(tmp_path, mutar))
    nomes_chip = [p.nome for p in controlador.filhos["chip"]]
    assert "Fixture Sintetica" in nomes_chip
    baseline = controlador.baseline
    for categoria in CATEGORIAS_ESTILO:
        secao = baseline
        for parte in categoria.split("."):
            secao = secao[parte]
        assert [p.nome for p in controlador.filhos[categoria]] == list(
            secao["presets"].keys()
        )


def test_escolhas_iniciais_correspondem_a_preset_default():
    runtime = RuntimeEstilo()
    controlador = ControladorTelaEstilo(runtime)
    baseline = runtime.baseline
    assert controlador.escolhas_iniciais == {
        "borda": baseline["borda"]["preset_default"],
        "chip": baseline["chip"]["preset_default"],
        "indicadores.selecionado": baseline["indicadores"]["selecionado"][
            "preset_default"
        ],
        "indicadores.incluido": baseline["indicadores"]["incluido"][
            "preset_default"
        ],
    }
    assert len(controlador.ids_escolha_inicial) == 4


def test_estrutura_dois_niveis_valida():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    assert navegacao.estrutura_dois_niveis_valida(
        type("C", (), {"conteudo_externo": controlador.conteudo})()
    )


def test_fronteira_sem_candidato_nem_mutacao_de_baseline(tmp_path):
    runtime = _runtime(tmp_path)
    original = (tmp_path / "config" / "estilo.json").read_text(encoding="utf-8")
    baseline = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    candidato_antes = copy.deepcopy(runtime.candidato)

    controlador = ControladorTelaEstilo(runtime)
    assert controlador.escolhas_iniciais["borda"] == baseline["borda"][
        "preset_default"
    ]
    assert runtime.baseline == baseline
    assert runtime.candidato == candidato_antes
    assert runtime.global_vigente == global_antes
    assert (tmp_path / "config" / "estilo.json").read_text(
        encoding="utf-8"
    ) == original
    # H-0066: solicitar_aplicacao passa a existir (capacidade compartilhada);
    # sem candidato divergente, permanece inativo/no-op (nao produz efeito).
    assert hasattr(controlador, "solicitar_aplicacao")
    assert controlador.aplicar_disponivel is False
    assert controlador.solicitar_aplicacao() is None
