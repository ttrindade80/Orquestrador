"""Testes de integracao H-0069 — demonstracao integrada com override local.

Cobre exclusivamente o fluxo ``Enter/Aplicar`` -> demonstracao local
(Cabecalho + Console + Dashboard + Barra) -> popup de confirmacao (H-0067)
-> ``ABORTADO``/``CONFIRMADO`` (reutilizando H-0068 sem modificar mecanismo).
Nao duplica a cobertura completa de H-0068; apenas prova que o novo passo
de demonstracao nao introduz caminho alternativo de aplicacao.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

from tela.loader import RuntimeEstilo


_SPEC = importlib.util.spec_from_file_location(
    "demo_h0069_mod", Path(__file__).with_name("demo.py")
)
_DEMO = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_DEMO)

TECLA_F4 = _DEMO.TECLA_F4
_ID_TELA_H0063 = _DEMO._ID_TELA_H0063
_ID_TELA_H0069_DEMONSTRACAO = _DEMO._ID_TELA_H0069_DEMONSTRACAO
_carregar_modelo_por_id = _DEMO._carregar_modelo_por_id
_preparar_modelo_estilo = _DEMO._preparar_modelo_estilo
_preparar_estado_estilo = _DEMO._preparar_estado_estilo
_anexar_tela_estilo = _DEMO._anexar_tela_estilo
_modelo_corrente = _DEMO._modelo_corrente
_estado_estilo_observavel = _DEMO._estado_estilo_observavel
criar_estado_inicial = _DEMO.criar_estado_inicial
processar_comando = _DEMO.processar_comando
renderizar_estado = _DEMO.renderizar_estado

RAIZ = Path(__file__).resolve().parents[1]
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"

_CAMINHOS = {
    "borda": ("borda",),
    "chip": ("chip",),
    "indicadores.selecionado": ("indicadores", "selecionado"),
    "indicadores.incluido": ("indicadores", "incluido"),
}


def _em(documento, caminho):
    atual = documento
    for parte in caminho:
        atual = atual[parte]
    return atual


def _runtime_tmp(tmp_path):
    destino = tmp_path / "config" / "estilo.json"
    destino.parent.mkdir(parents=True)
    destino.write_text(CONFIG_ESTILO.read_text(encoding="utf-8"), encoding="utf-8")
    return RuntimeEstilo(tmp_path), destino


def _abrir(runtime):
    estado = dict(
        criar_estado_inicial(), estilo_runtime=runtime, estilo=runtime.global_vigente
    )
    modelo = _carregar_modelo_por_id("demo")
    estado = processar_comando(estado, TECLA_F4, modelo)
    assert estado["tela_atual"] == _ID_TELA_H0063
    modelo = _carregar_modelo_por_id(estado["tela_atual"])
    estado = _anexar_tela_estilo(estado)
    modelo = _preparar_modelo_estilo(modelo, estado)
    estado = _preparar_estado_estilo(estado, modelo)
    return estado, modelo


def _entrar_e_selecionar_proximo_filho(estado, modelo):
    """Diverge exatamente uma categoria (a sob o pai focado inicialmente)."""
    estado = processar_comando(estado, " ", modelo)
    estado = processar_comando(estado, "\x1b[B", modelo)
    estado = processar_comando(estado, " ", modelo)
    return estado


def _outro_preset(runtime, categoria):
    secao = _em(runtime.candidato, _CAMINHOS[categoria])
    atual = secao["preset_default"]
    for nome in secao["presets"]:
        if nome != atual:
            return nome
    raise AssertionError("categoria sem preset alternativo: " + categoria)


def _abrir_demonstracao(tmp_path):
    """Abre a tela de Estilo, diverge o candidato e aciona Enter/Aplicar."""
    runtime, destino = _runtime_tmp(tmp_path)
    estado, modelo = _abrir(runtime)
    estado = _entrar_e_selecionar_proximo_filho(estado, modelo)
    assert estado["tela_estilo"].aplicar_disponivel is True
    candidato_antes = copy.deepcopy(runtime.candidato)
    estado = processar_comando(estado, "\r", modelo)
    return estado, modelo, runtime, destino, candidato_antes


def _pos_comando_como_main(estado, modelo, comando):
    """Espelha o recorte de ``demo.py:main`` que falhou no TTY apos CONFIRMADO.

    Observa estilo, processa o comando com o modelo do loop, reobtem o
    modelo corrente (tela_atual nao muda no overlay H-0069) e observa de
    novo. E esta segunda observacao que acessava ``conteudo_externo.nos``.
    """
    tela_antes = estado["tela_atual"]
    estilo_antes = _estado_estilo_observavel(estado, modelo)
    estado = processar_comando(estado, comando, modelo)
    assert estado["saindo"] is False
    assert estado["tela_atual"] == tela_antes
    modelo = _modelo_corrente(estado, modelo)
    estilo_depois = _estado_estilo_observavel(estado, modelo)
    return estado, modelo, estilo_antes, estilo_depois


def _console_estilo(estado, modelo):
    return estado["tela_estilo"].console_do_modelo(modelo)


def test_candidato_divergente_abre_demonstracao_com_quatro_regioes(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)

    assert estado.get("popup") is not None
    sessao = estado.get("_sessao_demonstracao_estilo")
    assert sessao is not None
    assert sessao.id == _ID_TELA_H0069_DEMONSTRACAO
    # ADR-0046 secao 5: Cabecalho + Console + Dashboard + Barra simultaneos.
    tipos = {getattr(el, "tipo", None) for el in sessao.corpo.elementos}
    assert {"console", "dashboard"} <= tipos
    assert sessao.cabecalho is not None
    assert sessao.barra_de_menus is not None
    # tela_atual permanece Estilo -- nao ha navegacao paralela de pilha.
    assert estado["tela_atual"] == _ID_TELA_H0063


def test_materializacao_local_corresponde_ao_candidato(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)

    materializacao = estado.get("estilo_demonstracao_local")
    assert materializacao is not None
    esperado_borda = candidato_c["borda"]["presets"][
        candidato_c["borda"]["preset_default"]
    ]
    assert materializacao.canto_superior_esquerdo == esperado_borda[
        "canto_superior_esquerdo"
    ]
    assert materializacao is not runtime.global_vigente


def test_isolamento_global_baseline_config_durante_demonstracao(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)

    original = json.loads(CONFIG_ESTILO.read_text(encoding="utf-8"))
    assert runtime.baseline == original
    assert destino.read_text(encoding="utf-8") == CONFIG_ESTILO.read_text(
        encoding="utf-8"
    )
    # O candidato materializado difere do global vigente (senao Aplicar
    # nao estaria ativo); o global vigente segue intocado.
    assert runtime.global_vigente is estado["estilo"]
    assert estado["estilo"].canto_superior_esquerdo == original["borda"]["presets"][
        original["borda"]["preset_default"]
    ]["canto_superior_esquerdo"]


def test_candidato_nao_vaza_para_estado_estilo_global(tmp_path):
    """``estado["estilo"]`` fora do contexto local nunca vira o candidato C."""
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)

    assert estado["estilo"] is not estado["estilo_demonstracao_local"]
    assert (
        estado["estilo"].canto_superior_esquerdo
        != estado["estilo_demonstracao_local"].canto_superior_esquerdo
    )


def test_popup_usa_a_mesma_materializacao_local_da_demonstracao(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    modelo_corrente = _modelo_corrente(estado, modelo)
    assert modelo_corrente.id == _ID_TELA_H0069_DEMONSTRACAO
    materializacao = estado["estilo_demonstracao_local"]
    borda_baseline = runtime.baseline["borda"]["presets"][
        runtime.baseline["borda"]["preset_default"]
    ]
    assert (
        materializacao.canto_superior_esquerdo
        != borda_baseline["canto_superior_esquerdo"]
    )

    quadro = renderizar_estado(estado, modelo_corrente, largura=80, altura=30)

    # Um unico quadro cobre tela + popup sobreposto: os cantos da baseline
    # nao aparecem em lugar nenhum e os do candidato aparecem -- prova de
    # que o popup foi desenhado sob a mesma materializacao local da
    # demonstracao, nao sob o global vigente.
    assert borda_baseline["canto_superior_esquerdo"] not in quadro
    assert materializacao.canto_superior_esquerdo in quadro
    assert "Confirmar" in quadro
    assert "AMOSTRAS" in quadro
    assert "RESUMO" in quadro


def test_render_quatro_regioes_simultaneas_sob_candidato(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    modelo_corrente = _modelo_corrente(estado, modelo)

    quadro = renderizar_estado(estado, modelo_corrente, largura=80, altura=30)

    assert "DEMONSTRACAO DO CANDIDATO" in quadro
    assert "AMOSTRAS" in quadro
    assert "RESUMO" in quadro
    assert "Menus" in quadro
    assert "Amostra 1" in quadro


def test_abortado_fecha_demonstracao_preserva_candidato_e_global(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente
    estilo_antes = estado["estilo"]

    modelo_corrente = _modelo_corrente(estado, modelo)
    estado = processar_comando(estado, "\x1b", modelo_corrente)

    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert "_sessao_demonstracao_estilo" not in estado
    assert "_modelo_origem_demonstracao_estilo" not in estado
    assert "estilo_demonstracao_local" not in estado
    assert "solicitacao_aplicacao_estilo" not in estado
    assert runtime.candidato == candidato_c
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["estilo"] is estilo_antes
    assert destino.read_text(encoding="utf-8") == CONFIG_ESTILO.read_text(
        encoding="utf-8"
    )
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert estado["tela_estilo"].aplicar_disponivel is True
    modelo_apos = _modelo_corrente(estado, modelo_corrente)
    assert modelo_apos.id == _ID_TELA_H0063


def test_confirmado_integra_h0068_e_encerra_demonstracao(tmp_path):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)

    modelo_corrente = _modelo_corrente(estado, modelo)
    estado = processar_comando(estado, "\r", modelo_corrente)

    assert estado.get("popup") is None
    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert "_sessao_demonstracao_estilo" not in estado
    assert "_modelo_origem_demonstracao_estilo" not in estado
    assert "estilo_demonstracao_local" not in estado
    assert "solicitacao_aplicacao_estilo" not in estado
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == candidato_c
    assert runtime.baseline == candidato_c
    assert runtime.candidato == candidato_c
    assert runtime.global_vigente is estado["estilo"]
    assert estado["tela_estilo"].aplicar_disponivel is False
    assert estado["tela_estilo"].invariavel_candidato_selecoes(
        estado, _modelo_corrente(estado, modelo_corrente)
    )
    assert estado["tela_atual"] == _ID_TELA_H0063
    modelo_apos = _modelo_corrente(estado, modelo_corrente)
    assert modelo_apos.id == _ID_TELA_H0063


def test_confirmado_pos_comando_do_main_retorna_a_estilo_sem_crash(tmp_path):
    """Regressao do crash TTY: avaliacao pos-CONFIRMADO equivalente ao main."""
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    modelo_loop = _modelo_corrente(estado, modelo)
    assert modelo_loop.id == _ID_TELA_H0069_DEMONSTRACAO

    estado, modelo_pos, _antes, _depois = _pos_comando_como_main(
        estado, modelo_loop, "\r"
    )

    assert estado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert modelo_pos.id == _ID_TELA_H0063
    console = _console_estilo(estado, modelo_pos)
    assert console is not None
    assert console.conteudo_externo is not None
    assert getattr(console.conteudo_externo, "nos", None)
    assert estado["tela_atual"] == _ID_TELA_H0063
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido == candidato_c
    assert runtime.baseline == candidato_c
    assert runtime.candidato == candidato_c
    assert runtime.global_vigente is estado["estilo"]
    assert estado["tela_estilo"].aplicar_disponivel is False
    assert "_sessao_demonstracao_estilo" not in estado
    assert "_modelo_origem_demonstracao_estilo" not in estado
    assert "estilo_demonstracao_local" not in estado


def test_abortado_pos_comando_do_main_nao_quebra_nem_deixa_modelo_incompativel(
    tmp_path,
):
    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    modelo_loop = _modelo_corrente(estado, modelo)
    baseline_antes = copy.deepcopy(runtime.baseline)
    global_antes = runtime.global_vigente

    estado, modelo_pos, _antes, _depois = _pos_comando_como_main(
        estado, modelo_loop, "\x1b"
    )

    assert estado.get("popup_resultado") == {"status": "ABORTADO"}
    assert modelo_pos.id == _ID_TELA_H0063
    console = _console_estilo(estado, modelo_pos)
    assert console is not None
    assert console.conteudo_externo is not None
    assert estado["tela_atual"] == _ID_TELA_H0063
    assert runtime.candidato == candidato_c
    assert runtime.baseline == baseline_antes
    assert runtime.global_vigente is global_antes
    assert estado["tela_estilo"].aplicar_disponivel is True
    assert "_sessao_demonstracao_estilo" not in estado
    assert "_modelo_origem_demonstracao_estilo" not in estado
    assert "estilo_demonstracao_local" not in estado


def test_duas_categorias_visiveis_na_demonstracao(tmp_path):
    runtime, destino = _runtime_tmp(tmp_path)
    estado, modelo = _abrir(runtime)
    controlador = estado["tela_estilo"]

    for categoria in ("borda", "chip"):
        alvo = _outro_preset(runtime, categoria)
        estado = controlador.aplicar_espaco_filho_invalido(
            estado, modelo, categoria, alvo
        )
    assert controlador.aplicar_disponivel is True
    candidato_c = copy.deepcopy(runtime.candidato)

    estado = processar_comando(estado, "\r", modelo)

    materializacao = estado["estilo_demonstracao_local"]
    borda_ativa = candidato_c["borda"]["presets"][
        candidato_c["borda"]["preset_default"]
    ]
    chip_ativo = candidato_c["chip"]["presets"][
        candidato_c["chip"]["preset_default"]
    ]
    assert materializacao.canto_superior_esquerdo == borda_ativa[
        "canto_superior_esquerdo"
    ]
    assert materializacao.caractere_esquerdo == chip_ativo["caractere_esquerdo"]
    assert materializacao.caractere_direito == chip_ativo["caractere_direito"]


def test_config_producao_nao_sofre_delta_apos_ciclo_completo(tmp_path):
    """Confirma que os testes desta suite nunca tocam config/estilo.json real."""
    original = CONFIG_ESTILO.read_text(encoding="utf-8")

    estado, modelo, runtime, destino, candidato_c = _abrir_demonstracao(tmp_path)
    modelo_corrente = _modelo_corrente(estado, modelo)
    processar_comando(estado, "\r", modelo_corrente)

    assert CONFIG_ESTILO.read_text(encoding="utf-8") == original
