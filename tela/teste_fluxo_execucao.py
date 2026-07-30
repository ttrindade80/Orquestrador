"""Testes focais do coordenador H-0044 / ADR-0037.

Cobre transicao atomica, origem suspensa por referencia, retornos dry-run/real,
ativacao cumulativa de Executar, limpeza e ausencia de pilha generica.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from tela import fluxo_execucao as fe
from tela import navegacao
from tela import selecao
from tela.loader import carregar_estilo, carregar_tela
from tela.modelo import construir_modelo

_RAIZ = Path(__file__).resolve().parent.parent
_RAIZ_TELAS = str(_RAIZ / "config" / "telas" / "demo")
_FIXTURE = _RAIZ / "demo" / "fixtures" / "h0042_fixture_execucao.json"
_BASELINE_HASH = None


def _hash_fixture():
    return hashlib.sha256(_FIXTURE.read_bytes()).hexdigest()


@pytest.fixture(autouse=True)
def _baseline_intacta():
    global _BASELINE_HASH
    antes = _hash_fixture()
    if _BASELINE_HASH is None:
        _BASELINE_HASH = antes
    yield
    assert _hash_fixture() == antes
    assert _hash_fixture() == _BASELINE_HASH


@pytest.fixture
def modelo_origem():
    raw = carregar_tela(None, fe.ID_TELA_H0044, raiz_telas=_RAIZ_TELAS)
    return construir_modelo(raw)


@pytest.fixture
def estado_inicial(modelo_origem):
    lista = navegacao.lista_foco(modelo_origem)
    cons = lista[0]
    return {
        "saindo": False,
        "tela_atual": fe.ID_TELA_H0044,
        "pilha_telas": [],
        "foco_console": 0,
        "cursores": {cons.id: 0},
        "selecoes": {cons.id: []},
        "estilo": carregar_estilo(),
        "filtro": "filtro_demo",
        "pagina": 1,
    }


@pytest.fixture
def fluxo(modelo_origem):
    chamadas = {"n": 0}

    def recarregador(origem):
        chamadas["n"] += 1
        return origem

    f = fe.FluxoExecucao.criar_sessao(
        modelo_origem,
        raiz_telas=_RAIZ_TELAS,
        caminho_fixture=_FIXTURE,
        recarregador=recarregador,
    )
    f._obs_recarga = chamadas
    return f


def _console(modelo, estado):
    nav = dict(estado, modelo=modelo)
    return navegacao.console_focado(nav)


def _marcar(estado, modelo, *ids):
    console = _console(modelo, estado)
    for id_item in ids:
        estado = selecao.alternar(estado, console, id_item)
    return estado


def test_tela_h0044_oito_itens_ordem(modelo_origem):
    cons = modelo_origem.corpo.elementos[0]
    itens = cons._campos_inertes["itens"]
    ids = [i["id"] for i in itens]
    assert ids == [
        "item_01", "item_05", "item_03", "item_07",
        "item_inexistente", "__falha_operacional__",
        "__resultado_invalido__", "__interrupcao__",
    ]
    assert all(i.get("navegavel") and i.get("selecionavel") for i in itens)


def test_tela_h0044_chip_dry_run(modelo_origem):
    chips = (modelo_origem.barra_de_menus or {}).get("chips") or []
    dry = next(c for c in chips if c["id"] == "chip_dry_run")
    assert dry["tecla"] == "Ins"
    assert dry["texto"] == "Dry-Run"
    assert dry["tipo"] == "alternancia"
    assert dry["regra_ativo"] == "sempre"


def test_toggle_insert_liga_desliga(fluxo, estado_inicial, modelo_origem):
    assert fluxo.dry_run_ativo is False
    e, m, ok = fluxo.processar_comando(
        estado_inicial, fe.TECLA_INSERT, modelo_origem
    )
    assert ok and fluxo.dry_run_ativo is True
    assert fluxo.chips_destacados() == frozenset({fe.ID_CHIP_DRY_RUN})
    e, m, ok = fluxo.processar_comando(e, fe.TECLA_INSERT, modelo_origem)
    assert ok and fluxo.dry_run_ativo is False
    assert fluxo.chips_destacados() == frozenset()


def test_toggle_nao_altera_selecao_foco_cursor(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    cons = _console(modelo_origem, estado)
    sel_antes = selecao.selecao(cons, estado)
    foco_antes = estado["foco_console"]
    cur_antes = dict(estado["cursores"])
    e, _, _ = fluxo.processar_comando(estado, fe.TECLA_INSERT, modelo_origem)
    assert selecao.selecao(cons, e) == sel_antes
    assert e["foco_console"] == foco_antes
    assert e["cursores"] == cur_antes


def test_insert_nao_age_com_resultado_ativo(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.dry_run_ativo = True
    estado, modelo_res, ok = fluxo.processar_comando(
        estado, "\r", modelo_origem
    )
    assert ok and fluxo.resultado_ativo
    assert fluxo.dry_run_ativo is True
    e2, _, ok2 = fluxo.processar_comando(estado, fe.TECLA_INSERT, modelo_res)
    assert ok2
    assert fluxo.dry_run_ativo is True


def test_executar_ativo_com_lote_valido(fluxo, estado_inicial, modelo_origem):
    assert fluxo.executar_disponivel(estado_inicial) is False
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    assert fluxo.executar_disponivel(estado) is True


def test_executar_inativo_sem_executor(modelo_origem, estado_inicial):
    f = fe.FluxoExecucao.criar_sessao(
        modelo_origem, raiz_telas=_RAIZ_TELAS, executor_disponivel=False
    )
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    assert f.executar_disponivel(estado) is False


def test_executar_inativo_sem_prevalidacao(modelo_origem, estado_inicial):
    f = fe.FluxoExecucao(
        modelo_origem,
        tela_resultado_raw=None,
        caminho_fixture=_FIXTURE,
        executor_disponivel=True,
    )
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    assert f.executar_disponivel(estado) is False


def test_reconciliacao_esvazia_nao_aplica_todos(fluxo, estado_inicial, modelo_origem):
    cons = _console(modelo_origem, estado_inicial)
    estado = dict(estado_inicial)
    estado["selecoes"] = {cons.id: ["id_fantasma"]}
    e, _, ok = fluxo.processar_comando(estado, "\r", modelo_origem)
    assert ok
    assert selecao.selecao(cons, e) == []
    assert not fluxo.resultado_ativo
    assert selecao.rotulo_enter(e, cons) == "Todos"


def test_transicao_preserva_identidade_origem(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    origem = fluxo.origem_ativa
    eventos = []

    def protocolo(entrada, fixture, *, dry_run=False, **kw):
        eventos.append("protocolo")
        assert fluxo.origem_ativa is origem
        assert fluxo.origem_suspensa is None
        # Delega ao protocolo real para obter documento valido.
        from tela.execucao_focal import executar_protocolo_focal
        return executar_protocolo_focal(entrada, fixture, dry_run=dry_run)

    fluxo._protocolo = protocolo
    estado, modelo_res = fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.origem_suspensa is origem
    assert fluxo.origem_ativa is None
    assert fluxo.modelo_resultado is not None
    assert modelo_res is fluxo.modelo_resultado.modelo
    assert "protocolo" in eventos


def test_suspensao_somente_apos_modelo(fluxo, estado_inicial, modelo_origem, monkeypatch):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    origem = modelo_origem
    ordem = []
    real_construir = fe.construir_modelo_resultado

    def spy_construir(tela, doc):
        ordem.append("construir")
        assert fluxo.origem_ativa is origem
        assert fluxo.origem_suspensa is None
        return real_construir(tela, doc)

    monkeypatch.setattr(fe, "construir_modelo_resultado", spy_construir)
    fluxo.executar_transicao(estado, modelo_origem)
    ordem.append("suspenso")
    assert ordem == ["construir", "suspenso"]
    assert fluxo.origem_suspensa is origem


def test_ausencia_pilha_generica(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.executar_transicao(estado, modelo_origem)
    assert not hasattr(fluxo, "pilha_telas")
    assert not isinstance(getattr(fluxo, "origem_suspensa", None), list)
    assert estado_inicial.get("pilha_telas") == []


def test_transicao_real_via_protocolo(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    estado, modelo_res = fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.resultado_ativo
    assert modelo_res.id == "resultado_execucao"
    assert fluxo.modelo_resultado.apresentacao in ("documento", "envelope")


def test_retorno_dry_run_zero_recargas(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.dry_run_ativo = True
    origem = fluxo.origem_ativa
    estado, _, _ = fluxo.processar_comando(estado, "\r", modelo_origem)
    assert fluxo.resultado_ativo
    estado2, modelo2, ok = fluxo.processar_comando(estado, "\x1b", None)
    assert ok
    assert modelo2 is origem
    assert fluxo.origem_ativa is origem
    assert fluxo.chamadas_recarregador == 0
    assert fluxo._obs_recarga["n"] == 0
    cons = _console(origem, estado2)
    assert selecao.selecao(cons, estado2) == ["item_01"]
    assert fluxo.dry_run_ativo is True
    assert estado2.get("filtro") == "filtro_demo"
    assert estado2.get("pagina") == 1
    assert estado2["foco_console"] == 0
    assert estado2["cursores"][cons.id] == 0


def test_retorno_real_uma_recarga_selecao_limpa(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.dry_run_ativo = False
    origem = fluxo.origem_ativa
    estado, _, _ = fluxo.processar_comando(estado, "\r", modelo_origem)
    estado2, modelo2, ok = fluxo.processar_comando(estado, "\x1b", None)
    assert ok and modelo2 is origem
    assert fluxo.chamadas_recarregador == 1
    assert fluxo._obs_recarga["n"] == 1
    cons = _console(origem, estado2)
    assert selecao.selecao(cons, estado2) == []
    assert fluxo.dry_run_ativo is False
    assert estado2.get("filtro") == "filtro_demo"


def test_retorno_real_preserva_cursor_por_id(fluxo, estado_inicial, modelo_origem):
    cons = _console(modelo_origem, estado_inicial)
    estado = dict(estado_inicial)
    estado["cursores"] = {cons.id: 1}
    estado = selecao.alternar(estado, cons, "item_05")
    fluxo.executar_transicao(estado, modelo_origem)
    estado2 = fluxo._retornar_de_resultado(estado)
    assert estado2["cursores"][cons.id] == 1
    item = navegacao.item_selecionado(cons, estado2)
    assert item.get("id") == "item_05"


def test_retorno_real_fallback_cursor(fluxo, estado_inicial, modelo_origem):
    cons = _console(modelo_origem, estado_inicial)
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.executar_transicao(estado, modelo_origem)
    fluxo._ids_cursor_suspensos = {cons.id: "id_removido"}
    estado2 = fluxo._retornar_de_resultado(estado)
    assert estado2["cursores"][cons.id] == 0


def test_falha_operacional_abre_resultado(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "__falha_operacional__")
    estado, modelo_res = fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.resultado_ativo
    assert fluxo.modelo_resultado.apresentacao == "envelope"


def test_resultado_invalido_abre_resultado(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "__resultado_invalido__")
    estado, modelo_res = fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.resultado_ativo
    assert fluxo.modelo_resultado.apresentacao == "envelope"


def test_interrupcao_130_abre_resultado(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "__interrupcao__")
    estado, modelo_res = fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.resultado_ativo
    assert fluxo.modelo_resultado.documento_runtime.codigo_saida == 130
    estado2, _, ok = fluxo.processar_comando(estado, "\x1b", None)
    assert ok
    assert estado2.get("saindo") is not True
    assert fluxo.origem_ativa is not None


def test_excecao_antes_da_suspensao(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    origem = fluxo.origem_ativa

    def falha(*a, **k):
        raise RuntimeError("falha_interna")

    fluxo._protocolo = falha
    with pytest.raises(RuntimeError, match="falha_interna"):
        fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.origem_ativa is origem
    assert fluxo.origem_suspensa is None
    assert fluxo.modelo_resultado is None
    assert fluxo.transicao_em_andamento is False


def test_excecao_depois_da_construcao_restaura(
    fluxo, estado_inicial, modelo_origem, monkeypatch
):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    origem = fluxo.origem_ativa
    real = fe.construir_modelo_resultado

    def boom(tela, doc):
        real(tela, doc)
        raise RuntimeError("pos_modelo")

    monkeypatch.setattr(fe, "construir_modelo_resultado", boom)
    with pytest.raises(RuntimeError, match="pos_modelo"):
        fluxo.executar_transicao(estado, modelo_origem)
    assert fluxo.origem_ativa is origem
    assert fluxo.origem_suspensa is None
    assert fluxo.modelo_resultado is None


def test_limpeza_entrada_temporaria(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    vistos = []
    real = fluxo._criar_entrada_temporaria

    def spy(ids):
        caminho = real(ids)
        vistos.append(caminho)
        return caminho

    fluxo._criar_entrada_temporaria = spy
    fluxo.executar_transicao(estado, modelo_origem)
    assert vistos
    assert not os.path.exists(vistos[0])


def test_teclas_no_resultado_nao_mutam_origem(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    sel_antes = {k: list(v) for k, v in estado["selecoes"].items()}
    fluxo.executar_transicao(estado, modelo_origem)
    fluxo.processar_comando(estado, " ", None)
    assert fluxo._selecoes_suspensas == sel_antes


def test_sigwinch_semantico_preservado(fluxo, estado_inicial, modelo_origem):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.dry_run_ativo = True
    fluxo.executar_transicao(estado, modelo_origem)
    estado_geo = dict(estado, largura=100, altura=30)
    estado2 = fluxo._retornar_de_resultado(estado_geo)
    assert estado2.get("largura") == 100
    assert estado2.get("altura") == 30
    cons = _console(fluxo.origem_ativa, estado2)
    assert selecao.selecao(cons, estado2) == ["item_01"]
    assert fluxo.chamadas_recarregador == 0


def test_dry_run_depois_execucao_real_mesma_selecao(
    fluxo, estado_inicial, modelo_origem
):
    estado = _marcar(estado_inicial, modelo_origem, "item_01")
    fluxo.dry_run_ativo = True
    origem = fluxo.origem_ativa
    estado, _, _ = fluxo.processar_comando(estado, "\r", modelo_origem)
    estado, _, _ = fluxo.processar_comando(estado, "\x1b", None)
    assert selecao.selecao(_console(origem, estado), estado) == ["item_01"]
    assert fluxo.dry_run_ativo is True
    estado, _, _ = fluxo.processar_comando(estado, fe.TECLA_INSERT, origem)
    assert fluxo.dry_run_ativo is False
    estado, _, _ = fluxo.processar_comando(estado, "\r", origem)
    assert fluxo.resultado_ativo
    estado, _, _ = fluxo.processar_comando(estado, "\x1b", None)
    assert selecao.selecao(_console(origem, estado), estado) == []
    assert fluxo.chamadas_recarregador == 1
