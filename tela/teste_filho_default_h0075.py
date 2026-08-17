"""Testes do controlador H-0075 — Aplicar, snapshot, persistir filho_default."""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
from pathlib import Path

import pytest

from tela import navegacao, selecao
from tela.carregamento.conteudo_externo import carregar_conteudo_externo
from tela.carregamento.erros import TelaEstruturaInvalida
from tela.loader import carregar_tela
from tela.modelo import (
    ConteudoExterno,
    Corpo,
    ElementoCorpo,
    ModeloTela,
    NoConteudo,
    construir_modelo,
)


RAIZ = Path(__file__).resolve().parents[1]
RAIZ_TELAS = "config/telas/demo"
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"
ID_H0055 = "h0055_dois_niveis_por_foco"
ID_H0072 = "h0072_formatacao_generica_dois_niveis_por_foco"
CONTEUDO_H0055 = "h0055_dois_niveis_por_foco_conteudo"
CONTEUDO_H0072 = "h0072_formatacao_generica_dois_niveis_por_foco_conteudo"


def _sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def _copiar_conteudo(tmp_path, id_conteudo):
    origem = RAIZ / RAIZ_TELAS / (id_conteudo + ".json")
    destino = tmp_path / (id_conteudo + ".json")
    destino.write_bytes(origem.read_bytes())
    return destino


def _abrir(tmp_path, id_tela, id_conteudo):
    destino = _copiar_conteudo(tmp_path, id_conteudo)
    tela = carregar_tela(None, id_tela, RAIZ_TELAS)
    bruto = carregar_conteudo_externo(
        None, id_conteudo, RAIZ_TELAS, caminho_arquivo=destino
    )
    modelo = construir_modelo(tela, bruto, caminho_conteudo=destino)
    estado = {"selecoes": {}, "cursores": {}, "foco_console": 0}
    for console in navegacao.lista_foco(modelo):
        estado = selecao.inicializar_escolhas_dois_niveis(estado, console)
    return estado, modelo, destino


def _abrir_h0055(tmp_path):
    return _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)


def _abrir_h0072(tmp_path):
    return _abrir(tmp_path, ID_H0072, CONTEUDO_H0072)


def _consoles(modelo):
    return [
        console for console in selecao._enumerar_consoles_modelo(modelo)
        if navegacao.tipo_navegacao_efetivo(console) == "dois_niveis_por_foco"
    ]


def _filho_alternativo(pai):
    atual = pai.campos["filho_default"]
    for filho in pai.filhos:
        if filho.id != atual:
            return filho.id
    raise AssertionError("pai sem filho alternativo: {0}".format(pai.id))


def _sem_filho_default(documento):
    copia = copy.deepcopy(documento)

    def _strip(nos):
        for no in nos or ():
            if isinstance(no, dict):
                no.pop("filho_default", None)
                _strip(no.get("filhos"))

    _strip(copia.get("dados"))
    return copia


def _console_politica(idc, conteudo, tipo):
    console = ElementoCorpo(
        id=idc,
        tipo="console",
        _campos_inertes={
            "politica_navegacao": {"navegavel": True, "tipo": tipo},
            "politica_selecao": "multipla",
            "itens": [],
        },
    )
    console.conteudo_externo = conteudo
    return console


def _modelo_sintetico(consoles, conteudo, caminho=None):
    if caminho is not None:
        conteudo.caminho_origem = caminho
    return ModeloTela(
        id="sintetico_h0075",
        schema="tela.v1",
        cabecalho={},
        corpo=Corpo(arranjo="vertical", elementos=list(consoles)),
        barra_de_menus={},
        _raw={},
        conteudo_externo=conteudo,
    )


def _no(idc, nivel, filho_default=None, filhos=None):
    campos = {
        "titulo": idc,
        "navegavel": True,
        "selecionavel": nivel != "pai",
    }
    if filho_default is not None:
        campos["filho_default"] = filho_default
    return NoConteudo(
        id=idc, nivel=nivel, campos=campos, filhos=list(filhos or [])
    )


# --- Aplicar -----------------------------------------------------------------

def teste_01_aplicar_inativo_sem_divergencia(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is False


def teste_02_aplicar_ativo_com_um_pai(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, console, alvo, modelo=modelo)
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is True


def teste_03_aplicar_ativo_com_varios_pais(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[1]),
        modelo=modelo,
    )
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is True
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    assert len(solicitacao.candidato) == 5


def teste_04_cursor_irrelevante_para_aplicar(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    inativo = selecao.aplicar_disponivel_filho_default(estado, modelo)
    estado["cursores"] = {console.id: 3}
    estado["foco_console"] = 0
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is inativo
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    ativo = selecao.aplicar_disponivel_filho_default(estado, modelo)
    estado["cursores"] = {console.id: 0}
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is ativo


def teste_05_snapshot_frozen_nao_acompanha_selecoes(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, console, alvo, modelo=modelo)
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    assert isinstance(solicitacao, selecao.SolicitacaoAplicacaoFilhoDefault)
    candidato_congelado = copy.deepcopy(solicitacao.candidato)
    outro = modelo.conteudo_externo.nos[0].filhos[0].id
    if outro == alvo:
        outro = modelo.conteudo_externo.nos[0].filhos[-1].id
    estado = selecao.alternar(estado, console, outro, modelo=modelo)
    assert solicitacao.candidato == candidato_congelado
    assert solicitacao.candidato != selecao.mapa_candidato_filho_default(
        estado, modelo
    )


def teste_38_a_41_inconsistencia_nao_e_divergencia_aplicavel(tmp_path):
    estado, modelo, destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    hash_antes = _sha256(destino)
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, consoles[0], alvo)
    with pytest.raises(TelaEstruturaInvalida):
        selecao.mapa_candidato_filho_default(estado, modelo)
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is False
    assert selecao.solicitar_aplicacao_filho_default(estado, modelo) is None
    assert _sha256(destino) == hash_antes


def teste_39_inconsistencia_independe_da_ordem(tmp_path):
    estado, modelo, _destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, consoles[0], alvo)
    invertido = _modelo_sintetico(
        list(reversed(list(modelo.corpo.elementos))),
        modelo.conteudo_externo,
        modelo.conteudo_externo.caminho_origem,
    )
    with pytest.raises(TelaEstruturaInvalida):
        selecao.mapa_candidato_filho_default(estado, modelo)
    with pytest.raises(TelaEstruturaInvalida):
        selecao.mapa_candidato_filho_default(estado, invertido)


# --- Snapshot / ABORTADO / CONFIRMADO / falha --------------------------------

def teste_08_a_10_abortado_preserva_estado_e_arquivo(tmp_path):
    estado, modelo, destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    hash_antes = _sha256(destino)
    baseline = copy.deepcopy(selecao.mapa_baseline_filho_default(modelo))
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    candidato = copy.deepcopy(selecao.mapa_candidato_filho_default(estado, modelo))
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    assert solicitacao is not None
    assert _sha256(destino) == hash_antes
    assert selecao.mapa_candidato_filho_default(estado, modelo) == candidato
    assert selecao.mapa_baseline_filho_default(modelo) == baseline
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is True
    nova = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    assert isinstance(nova, selecao.SolicitacaoAplicacaoFilhoDefault)


def teste_11_a_18_confirmado_persiste_snapshot_e_promove(tmp_path):
    estado, modelo, destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    bruto_antes = json.loads(destino.read_text(encoding="utf-8"))
    pai_a = modelo.conteudo_externo.nos[0]
    pai_b = modelo.conteudo_externo.nos[1]
    alvo_a = _filho_alternativo(pai_a)
    alvo_b = _filho_alternativo(pai_b)
    estado = selecao.alternar(estado, console, alvo_a, modelo=modelo)
    estado = selecao.alternar(estado, console, alvo_b, modelo=modelo)
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    snapshot = copy.deepcopy(solicitacao.candidato)
    outro = pai_a.filhos[-1].id
    if outro == alvo_a:
        outro = pai_a.filhos[0].id
    estado_mutado = selecao.alternar(estado, console, outro, modelo=modelo)
    from tela.carregamento import conteudo_externo as ce_mod

    persistir_original = ce_mod.persistir_conteudo_externo
    chamadas = []

    def _contar(documento, caminho):
        chamadas.append(caminho)
        return persistir_original(documento, caminho)

    ce_mod.persistir_conteudo_externo = _contar
    try:
        novo, sucesso = selecao.aplicar_solicitacao_filho_default(
            solicitacao, estado_mutado, modelo
        )
    finally:
        ce_mod.persistir_conteudo_externo = persistir_original

    assert sucesso is True
    assert len(chamadas) == 1
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido["dados"][0]["filho_default"] == alvo_a
    assert persistido["dados"][1]["filho_default"] == alvo_b
    assert persistido["dados"][0]["filho_default"] != outro
    assert _sem_filho_default(persistido) == _sem_filho_default(bruto_antes)
    assert modelo.conteudo_externo.nos[0].campos["filho_default"] == alvo_a
    assert modelo.conteudo_externo.nos[1].campos["filho_default"] == alvo_b
    assert selecao.mapa_candidato_filho_default(novo, modelo) == snapshot
    assert selecao.aplicar_disponivel_filho_default(novo, modelo) is False

    recarregado = carregar_conteudo_externo(
        None, CONTEUDO_H0055, RAIZ_TELAS, caminho_arquivo=destino
    )
    modelo2 = construir_modelo(
        carregar_tela(None, ID_H0055, RAIZ_TELAS),
        recarregado,
        caminho_conteudo=destino,
    )
    estado2 = {"selecoes": {}, "cursores": {}}
    for console2 in navegacao.lista_foco(modelo2):
        estado2 = selecao.inicializar_escolhas_dois_niveis(estado2, console2)
    assert modelo2.conteudo_externo.nos[0].campos["filho_default"] == alvo_a
    assert selecao.mapa_candidato_filho_default(estado2, modelo2)[
        pai_a.id
    ] == alvo_a


def teste_19_a_22_falha_preserva_arquivo_baseline_e_candidato(tmp_path, monkeypatch):
    estado, modelo, destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    hash_antes = _sha256(destino)
    baseline = copy.deepcopy(selecao.mapa_baseline_filho_default(modelo))
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    candidato = copy.deepcopy(selecao.mapa_candidato_filho_default(estado, modelo))
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)

    def _falhar(documento, caminho):
        raise TelaEstruturaInvalida("falha injetada")

    monkeypatch.setattr(
        "tela.carregamento.conteudo_externo.persistir_conteudo_externo",
        _falhar,
    )
    novo, sucesso = selecao.aplicar_solicitacao_filho_default(
        solicitacao, estado, modelo
    )
    assert sucesso is False
    assert _sha256(destino) == hash_antes
    assert selecao.mapa_baseline_filho_default(modelo) == baseline
    assert selecao.mapa_candidato_filho_default(novo, modelo) == candidato
    assert selecao.aplicar_disponivel_filho_default(novo, modelo) is True
    assert modelo.conteudo_externo.nos[0].campos["filho_default"] == (
        baseline[modelo.conteudo_externo.nos[0].id]
    )


def teste_23_nenhuma_publicacao_de_estilo(tmp_path):
    hash_estilo = _sha256(CONFIG_ESTILO)
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    estado["estilo"] = object()
    marca = estado["estilo"]
    console = _consoles(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    novo, sucesso = selecao.aplicar_solicitacao_filho_default(
        solicitacao, estado, modelo
    )
    assert sucesso is True
    assert novo["estilo"] is marca
    assert _sha256(CONFIG_ESTILO) == hash_estilo


# --- Compartilhamento H-0072 -------------------------------------------------

def teste_26_a_34_h0072_compartilhamento_e_persistencia(tmp_path):
    estado, modelo, destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    assert len(consoles) == 3
    baseline = selecao.mapa_baseline_filho_default(modelo)
    for console in consoles:
        reconciliado = selecao._reconciliar_ids_dois_niveis(
            console, estado["selecoes"][console.id]
        )
        for pai in modelo.conteudo_externo.nos:
            assert pai.campos["filho_default"] == baseline[pai.id]
        assert reconciliado == [
            baseline["h0072_pai_01"], baseline["h0072_pai_02"]
        ]

    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    p2_b = estado["selecoes"][consoles[1].id][1]
    estado = selecao.alternar(estado, consoles[0], alvo, modelo=modelo)
    assert alvo in estado["selecoes"][consoles[1].id]
    assert estado["selecoes"][consoles[1].id][1] == p2_b
    assert estado["selecoes"][consoles[2].id][0] == alvo

    outro = modelo.conteudo_externo.nos[0].filhos[0].id
    if outro == alvo:
        outro = modelo.conteudo_externo.nos[0].filhos[-1].id
    estado = selecao.alternar(estado, consoles[1], outro, modelo=modelo)
    assert estado["selecoes"][consoles[0].id][0] == outro
    assert estado["selecoes"][consoles[2].id][0] == outro

    mapa_antes = selecao.mapa_candidato_filho_default(estado, modelo)
    estado["foco_console"] = 2
    estado["cursores"] = {c.id: 1 for c in consoles}
    assert selecao.mapa_candidato_filho_default(estado, modelo) == mapa_antes

    mapa = selecao.mapa_candidato_filho_default(estado, modelo)
    assert set(mapa) == {"h0072_pai_01", "h0072_pai_02"}
    assert mapa["h0072_pai_01"] == outro

    invertido = _modelo_sintetico(
        list(reversed(list(modelo.corpo.elementos))),
        modelo.conteudo_externo,
        modelo.conteudo_externo.caminho_origem,
    )
    assert selecao.mapa_candidato_filho_default(estado, invertido) == mapa
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is True

    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    novo, sucesso = selecao.aplicar_solicitacao_filho_default(
        solicitacao, estado, modelo
    )
    assert sucesso is True
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido["dados"][0]["filho_default"] == outro
    for console in consoles:
        assert novo["selecoes"][console.id][0] == outro
    recarregado = carregar_conteudo_externo(
        None, CONTEUDO_H0072, RAIZ_TELAS, caminho_arquivo=destino
    )
    assert recarregado["dados"][0]["filho_default"] == outro


def teste_35_fonte_nao_elege_vencedor():
    fonte_mapa = inspect.getsource(selecao.mapa_candidato_filho_default)
    fonte_sync = inspect.getsource(selecao._sincronizar_escolha_pai)
    fonte_aplicar = inspect.getsource(selecao.aplicar_disponivel_filho_default)
    assert "lista_foco" not in fonte_mapa
    assert "lista_foco" not in fonte_sync
    assert "lista_foco" not in fonte_aplicar
    assert "console_focado" not in fonte_mapa


def teste_37_duas_representacoes_equivalentes_uma_entrada(tmp_path):
    estado, modelo, _destino = _abrir_h0072(tmp_path)
    mapa = selecao.mapa_candidato_filho_default(estado, modelo)
    assert mapa["h0072_pai_01"] == "h0072_filho_01_02"
    assert list(mapa).count("h0072_pai_01") == 1


def teste_43_politica_diferente_nao_recebe_propagacao(tmp_path):
    destino = tmp_path / "sint.json"
    pai = _no(
        "p1", "pai", filho_default="f1",
        filhos=[_no("f1", "filho"), _no("f2", "filho")],
    )
    conteudo = ConteudoExterno(
        tipo="multinivel", apresentacao="hierarquia", niveis=[], nos=[pai],
        caminho_origem=destino,
    )
    dnf = _console_politica("dnf", conteudo, "dois_niveis_por_foco")
    outra = _console_politica("outra", conteudo, "selecao_multinivel")
    modelo = _modelo_sintetico([dnf, outra], conteudo, destino)
    estado = {"selecoes": {"outra": ["marcador"]}, "cursores": {}}
    estado = selecao.inicializar_escolhas_dois_niveis(estado, dnf)
    estado = selecao.alternar(estado, dnf, "f2", modelo=modelo)
    assert estado["selecoes"]["outra"] == ["marcador"]
    assert "f2" not in estado["selecoes"]["outra"]


def teste_44_console_sem_pai_nao_recebe_filho(tmp_path):
    destino = tmp_path / "sint.json"
    p1 = _no(
        "p1", "pai", filho_default="f1",
        filhos=[_no("f1", "filho"), _no("f2", "filho")],
    )
    p2 = _no(
        "p2", "pai", filho_default="g1",
        filhos=[_no("g1", "filho"), _no("g2", "filho")],
    )
    conteudo_a = ConteudoExterno(
        tipo="multinivel", apresentacao="hierarquia", niveis=[],
        nos=[p1, p2], caminho_origem=destino,
    )
    conteudo_b = ConteudoExterno(
        tipo="multinivel", apresentacao="hierarquia", niveis=[],
        nos=[copy.deepcopy(p2)],
    )
    a = _console_politica("a", conteudo_a, "dois_niveis_por_foco")
    b = _console_politica("b", conteudo_b, "dois_niveis_por_foco")
    modelo = _modelo_sintetico([a, b], conteudo_a, destino)
    estado = {"selecoes": {}, "cursores": {}}
    estado = selecao.inicializar_escolhas_dois_niveis(estado, a)
    estado = selecao.inicializar_escolhas_dois_niveis(estado, b)
    ids_b_antes = list(estado["selecoes"][b.id])
    estado = selecao.alternar(estado, a, "f2", modelo=modelo)
    assert estado["selecoes"][b.id] == ids_b_antes
    assert "f2" not in estado["selecoes"][b.id]


def teste_45_sincronizar_um_pai_preserva_os_demais(tmp_path):
    estado, modelo, _destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    alvo_p2 = _filho_alternativo(modelo.conteudo_externo.nos[1])
    estado = selecao.alternar(estado, consoles[1], alvo_p2)
    p2_destino = estado["selecoes"][consoles[1].id][1]
    alvo_p1 = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, consoles[0], alvo_p1, modelo=modelo)
    assert estado["selecoes"][consoles[1].id][0] == alvo_p1
    assert estado["selecoes"][consoles[1].id][1] == p2_destino
    assert selecao.aplicar_disponivel_filho_default(estado, modelo) is False


def teste_origem_estrangeira_mesmo_id_nao_contamina_modelo(tmp_path):
    estado, modelo, _destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    real = consoles[0]
    selecoes_antes = copy.deepcopy(estado["selecoes"])
    candidato_antes = copy.deepcopy(
        selecao.mapa_candidato_filho_default(estado, modelo)
    )
    estrangeira = _console_politica(
        real.id, real.conteudo_externo, "dois_niveis_por_foco"
    )
    assert estrangeira is not real
    assert estrangeira.id == real.id
    assert estrangeira.conteudo_externo is real.conteudo_externo
    assert not any(
        membro is estrangeira
        for membro in selecao._enumerar_consoles_modelo(modelo)
    )
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    novo = selecao.alternar(estado, estrangeira, alvo, modelo=modelo)
    assert novo["selecoes"] == selecoes_antes
    assert novo["selecoes"][real.id] == selecoes_antes[real.id]
    for console in consoles:
        assert novo["selecoes"][console.id] == selecoes_antes[console.id]
    assert alvo not in novo["selecoes"][real.id]
    assert selecao.mapa_candidato_filho_default(novo, modelo) == candidato_antes


def teste_origem_real_do_modelo_sincroniza_legitimamente(tmp_path):
    estado, modelo, _destino = _abrir_h0072(tmp_path)
    consoles = _consoles(modelo)
    assert any(
        membro is consoles[0]
        for membro in selecao._enumerar_consoles_modelo(modelo)
    )
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    p2_b = estado["selecoes"][consoles[1].id][1]
    estado = selecao.alternar(estado, consoles[0], alvo, modelo=modelo)
    assert estado["selecoes"][consoles[0].id][0] == alvo
    assert estado["selecoes"][consoles[1].id][0] == alvo
    assert estado["selecoes"][consoles[1].id][1] == p2_b
    assert estado["selecoes"][consoles[2].id][0] == alvo


def teste_popup_envelope_generico(tmp_path):
    estado, modelo, _destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    envelope = selecao.conteudo_popup_confirmacao_filho_default(solicitacao)
    assert envelope["tipo"] == "texto"
    assert "filho_default" not in envelope["texto"]
    assert "filho_01" not in envelope["texto"]
    assert selecao.ID_POPUP_CONFIRMACAO_FILHO_DEFAULT == (
        "popup_confirmacao_aplicacao_filho_default"
    )


def teste_caminho_destino_congelado_nao_consulta_slot(tmp_path):
    estado, modelo, destino = _abrir_h0055(tmp_path)
    console = _consoles(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    solicitacao = selecao.solicitar_aplicacao_filho_default(estado, modelo)
    assert solicitacao.caminho_destino == str(destino)
    modelo.conteudo_externo.caminho_origem = tmp_path / "outro.json"
    novo, sucesso = selecao.aplicar_solicitacao_filho_default(
        solicitacao, estado, modelo
    )
    assert sucesso is True
    assert destino.exists()
    assert not (tmp_path / "outro.json").exists()
    assert novo is not None
