"""Testes de integracao H-0075 via processar_comando e copia em tmp_path."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from tela import navegacao, selecao
from tela.carregamento.conteudo_externo import carregar_conteudo_externo
from tela.carregamento.erros import TelaEstruturaInvalida
from tela.modelo import construir_modelo
from tela.loader import carregar_tela


_SPEC = importlib.util.spec_from_file_location(
    "demo_h0075_mod", Path(__file__).with_name("demo.py")
)
_DEMO = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_DEMO)

criar_estado_inicial = _DEMO.criar_estado_inicial
processar_comando = _DEMO.processar_comando
_carregar_modelo_por_id = _DEMO._carregar_modelo_por_id
_preparar_estado_h0055 = _DEMO._preparar_estado_h0055

RAIZ = Path(__file__).resolve().parents[1]
RAIZ_TELAS = "config/telas/demo"
CONFIG_ESTILO = RAIZ / "config" / "estilo.json"
ID_H0055 = "h0055_dois_niveis_por_foco"
ID_H0072 = "h0072_formatacao_generica_dois_niveis_por_foco"
CONTEUDO_H0055 = "h0055_dois_niveis_por_foco_conteudo"
CONTEUDO_H0072 = "h0072_formatacao_generica_dois_niveis_por_foco_conteudo"


def _sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def _copiar(tmp_path, id_conteudo):
    origem = RAIZ / RAIZ_TELAS / (id_conteudo + ".json")
    destino = tmp_path / (id_conteudo + ".json")
    destino.write_bytes(origem.read_bytes())
    return destino


def _abrir(tmp_path, id_tela, id_conteudo):
    destino = _copiar(tmp_path, id_conteudo)
    estado = dict(
        criar_estado_inicial(),
        tela_atual=id_tela,
        foco_console=0,
        caminhos_conteudo_externo={id_tela: destino},
    )
    modelo = _carregar_modelo_por_id(id_tela, caminho_conteudo=destino)
    estado = _preparar_estado_h0055(estado, modelo)
    console = navegacao.lista_foco(modelo)[0]
    cursores = dict(estado.get("cursores") or {})
    cursores.setdefault(console.id, 0)
    estado["cursores"] = cursores
    return estado, modelo, destino


def _filho_alternativo(pai):
    atual = pai.campos["filho_default"]
    for filho in pai.filhos:
        if filho.id != atual:
            return filho.id
    raise AssertionError("pai sem filho alternativo")


def teste_06_popup_abre_somente_com_aplicar_valido(tmp_path):
    estado, modelo, _destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    inativo = processar_comando(estado, "\r", modelo)
    assert inativo.get("popup") is None
    assert inativo.get("solicitacao_aplicacao_filho_default") is None

    console = navegacao.lista_foco(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    aberto = processar_comando(estado, "\r", modelo)
    assert aberto.get("popup") is not None
    assert aberto["popup"].id == selecao.ID_POPUP_CONFIRMACAO_FILHO_DEFAULT
    assert isinstance(
        aberto.get("solicitacao_aplicacao_filho_default"),
        selecao.SolicitacaoAplicacaoFilhoDefault,
    )


def teste_07_modalidade_nao_muta_selecoes_nem_cursores(tmp_path):
    estado, modelo, _destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    console = navegacao.lista_foco(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    aberto = processar_comando(estado, "\r", modelo)
    selecoes = dict(aberto.get("selecoes") or {})
    cursores = dict(aberto.get("cursores") or {})
    depois_seta = processar_comando(aberto, "\x1b[B", modelo)
    depois_espaco = processar_comando(depois_seta, " ", modelo)
    assert depois_espaco.get("popup") is not None
    assert depois_espaco["selecoes"] == selecoes
    assert depois_espaco["cursores"] == cursores


def teste_abortado_via_esc_nao_escreve(tmp_path):
    estado, modelo, destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    hash_antes = _sha256(destino)
    console = navegacao.lista_foco(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    candidato = list(estado["selecoes"][console.id])
    aberto = processar_comando(estado, "\r", modelo)
    abortado = processar_comando(aberto, "\x1b", modelo)
    assert abortado.get("popup") is None
    assert abortado.get("popup_resultado") == {"status": "ABORTADO"}
    assert abortado.get("solicitacao_aplicacao_filho_default") is None
    assert _sha256(destino) == hash_antes
    assert abortado["selecoes"][console.id] == candidato
    assert selecao.aplicar_disponivel_filho_default(abortado, modelo) is True
    assert abortado["tela_atual"] == ID_H0055


def teste_confirmado_via_enter_persiste_copia(tmp_path):
    estado, modelo, destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    hash_antes = _sha256(destino)
    bruto_antes = json.loads(destino.read_text(encoding="utf-8"))
    console = navegacao.lista_foco(modelo)[0]
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, console, alvo, modelo=modelo)
    aberto = processar_comando(estado, "\r", modelo)
    snapshot = dict(aberto["solicitacao_aplicacao_filho_default"].candidato)
    confirmado = processar_comando(aberto, "\r", modelo)
    assert confirmado.get("popup") is None
    assert confirmado.get("popup_resultado") == {"status": "CONFIRMADO"}
    assert confirmado.get("solicitacao_aplicacao_filho_default") is None
    assert _sha256(destino) != hash_antes
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido["dados"][0]["filho_default"] == snapshot[
        modelo.conteudo_externo.nos[0].id
    ]
    assert persistido["dados"][0]["filho_default"] == alvo
    assert persistido["id"] == bruto_antes["id"]
    assert persistido["formato"] == bruto_antes["formato"]
    assert selecao.aplicar_disponivel_filho_default(confirmado, modelo) is False
    recarregado = carregar_conteudo_externo(
        None, CONTEUDO_H0055, RAIZ_TELAS, caminho_arquivo=destino
    )
    assert recarregado["dados"][0]["filho_default"] == alvo


def teste_prova_hash_abortado_confirmado_reabertura(tmp_path):
    estado, modelo, destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    hash_antes = _sha256(destino)
    console = navegacao.lista_foco(modelo)[0]
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, console, alvo, modelo=modelo)
    aberto = processar_comando(estado, "\r", modelo)
    abortado = processar_comando(aberto, "\x1b", modelo)
    assert _sha256(destino) == hash_antes
    nova = processar_comando(abortado, "\r", modelo)
    confirmado = processar_comando(nova, "\r", modelo)
    persistido = json.loads(destino.read_text(encoding="utf-8"))
    assert persistido["dados"][0]["filho_default"] == alvo
    modelo2 = construir_modelo(
        carregar_tela(None, ID_H0055, RAIZ_TELAS),
        persistido,
        caminho_conteudo=destino,
    )
    estado2 = {"selecoes": {}, "cursores": {}}
    estado2 = selecao.inicializar_escolhas_dois_niveis(
        estado2, navegacao.lista_foco(modelo2)[0]
    )
    assert modelo2.conteudo_externo.nos[0].campos["filho_default"] == alvo
    assert estado2["selecoes"][navegacao.lista_foco(modelo2)[0].id][0] == alvo
    assert confirmado["tela_atual"] == ID_H0055


def teste_inconsistencia_enter_nao_abre_popup_nem_escreve(tmp_path):
    estado, modelo, destino = _abrir(tmp_path, ID_H0072, CONTEUDO_H0072)
    hash_antes = _sha256(destino)
    consoles = navegacao.lista_foco(modelo)
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado = selecao.alternar(estado, consoles[0], alvo)
    try:
        selecao.mapa_candidato_filho_default(estado, modelo)
        raise AssertionError("mapa deveria falhar fechado")
    except TelaEstruturaInvalida:
        pass
    depois = processar_comando(estado, "\r", modelo)
    assert depois.get("popup") is None
    assert _sha256(destino) == hash_antes


def teste_h0072_espaco_sincroniza_entre_consoles(tmp_path):
    estado, modelo, _destino = _abrir(tmp_path, ID_H0072, CONTEUDO_H0072)
    consoles = navegacao.lista_foco(modelo)
    alvo = _filho_alternativo(modelo.conteudo_externo.nos[0])
    estado["foco_console"] = 0
    estado = selecao.alternar(estado, consoles[0], alvo, modelo=modelo)
    assert estado["selecoes"][consoles[1].id][0] == alvo
    assert estado["selecoes"][consoles[2].id][0] == alvo


def teste_23_estilo_intocado_no_fluxo_demo(tmp_path):
    hash_estilo = _sha256(CONFIG_ESTILO)
    estado, modelo, destino = _abrir(tmp_path, ID_H0055, CONTEUDO_H0055)
    estado["estilo"] = object()
    marca = estado["estilo"]
    console = navegacao.lista_foco(modelo)[0]
    estado = selecao.alternar(
        estado, console, _filho_alternativo(modelo.conteudo_externo.nos[0]),
        modelo=modelo,
    )
    aberto = processar_comando(estado, "\r", modelo)
    confirmado = processar_comando(aberto, "\r", modelo)
    assert confirmado["estilo"] is marca
    assert _sha256(CONFIG_ESTILO) == hash_estilo
    assert destino.exists()


def teste_json_estrutural_declara_chip_e_popup():
    h0055 = json.loads(
        (RAIZ / RAIZ_TELAS / (ID_H0055 + ".json")).read_text(encoding="utf-8")
    )
    h0072 = json.loads(
        (RAIZ / RAIZ_TELAS / (ID_H0072 + ".json")).read_text(encoding="utf-8")
    )
    for tela in (h0055, h0072):
        ids = [chip["id"] for chip in tela["barra_de_menus"]["chips"]]
        assert "chip_aplicar" in ids
        assert ids.index("chip_aplicar") < ids.index("ajuda")
        popup = tela["popups"]["popup_confirmacao_aplicacao_filho_default"]
        assert popup["tipo"] == "texto"
        textos = [chip["texto"] for chip in popup["chips"]]
        assert textos == ["Voltar", "Confirmar"]
