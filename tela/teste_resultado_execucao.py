"""Testes do H-0043 — tela padrao de resultado (ADR-0036).

Cobre validacao de perfil, escolha documento/envelope, schema do envelope,
preservacao literal, carregamento unico, nao-releitura em redesenho/SIGWINCH
e comparacao integral dos seis quadros 80x24.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from tela.loader import (
    PERFIL_RESULTADO_EXECUCAO,
    TelaCampoObrigatorioAusente,
    TelaEstruturaInvalida,
    carregar_estilo,
    carregar_tela,
)
from tela.renderizador import renderizar_tela
from tela import resultado_execucao as re
from tela.resultado_execucao import (
    APRESENTACAO_DOCUMENTO,
    APRESENTACAO_ENVELOPE,
    CAMPOS_ENVELOPE_ORDEM,
    DIAGNOSTICO_CODIGO_NAO_ZERO,
    DIAGNOSTICO_INTERRUPCAO,
    DIAGNOSTICO_RESULTADO_AUSENTE,
    DIAGNOSTICO_RESULTADO_MALFORMADO,
    DIAGNOSTICO_RESULTADO_SEMANTICO,
    EXIBICAO_INDISPONIVEL,
    DocumentoRuntime,
    carregar_documento_runtime,
    carregar_sessao_resultado,
    classificar_apresentacao,
    construir_modelo_resultado,
    materializar_envelope,
)

_RAIZ = Path(__file__).resolve().parents[1]
_FIX = _RAIZ / "demo" / "fixtures"
_RAIZ_TELAS = "config/telas/demo"
_ESTILO = carregar_estilo()

_CENARIOS = (
    "h0043_resultado_sucesso",
    "h0043_resultado_parcial",
    "h0043_resultado_falha_semantica",
    "h0043_envelope_falha_operacional",
    "h0043_envelope_resultado_invalido",
    "h0043_envelope_interrupcao",
)

_QUADROS = {
    "h0043_resultado_sucesso": "h0043_quadro_sucesso_80x24.txt",
    "h0043_resultado_parcial": "h0043_quadro_parcial_80x24.txt",
    "h0043_resultado_falha_semantica": "h0043_quadro_falha_semantica_80x24.txt",
    "h0043_envelope_falha_operacional": "h0043_quadro_falha_operacional_80x24.txt",
    "h0043_envelope_resultado_invalido": "h0043_quadro_resultado_invalido_80x24.txt",
    "h0043_envelope_interrupcao": "h0043_quadro_interrupcao_80x24.txt",
}


def _tela_base(**overrides):
    dados = {
        "schema": "tela.v1",
        "id": "resultado_execucao",
        "perfil": "resultado_execucao",
        "cabecalho": {
            "titulo": "Resultado da execução",
            "descricao": "Resultado estruturado da operação realizada.",
        },
        "corpo": {
            "arranjo": "vertical",
            "elementos": [
                {
                    "id": "console_resultado",
                    "tipo": "console",
                    "titulo": "Resultado",
                    "formato": {
                        "excesso": {"politica_modo": "somente_verboso"}
                    },
                }
            ],
        },
        "barra_de_menus": {
            "distribuicao": "horizontal",
            "chips": [
                {
                    "id": "esc",
                    "tecla": "Esc",
                    "texto": "Voltar",
                    "acao": "voltar",
                }
            ],
        },
    }
    dados.update(overrides)
    return dados


def _escrever_tela(tmpdir, dados):
    caminho = Path(tmpdir) / "config" / "telas" / "demo"
    caminho.mkdir(parents=True, exist_ok=True)
    id_tela = dados["id"]
    arq = caminho / (id_tela + ".json")
    arq.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n")
    return str(tmpdir)


# ---------------------------------------------------------------------------
# Tela e perfil
# ---------------------------------------------------------------------------


def test_tela_resultado_execucao_valida_d23_puro():
    tela = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS)
    assert tela["perfil"] == PERFIL_RESULTADO_EXECUCAO
    elems = tela["corpo"]["elementos"]
    assert len(elems) == 1
    console = elems[0]
    assert console["id"] == "console_resultado"
    assert console["tipo"] == "console"
    assert set(console) <= {"id", "tipo", "titulo", "formato"}
    assert console["formato"]["excesso"]["politica_modo"] == "somente_verboso"
    assert "modo_inicial" not in console["formato"]["excesso"]
    chips = tela["barra_de_menus"]["chips"]
    assert len(chips) == 1
    assert chips[0]["tecla"] == "Esc"
    assert chips[0]["texto"] == "Voltar"
    assert "origem_dados" not in console
    assert tela["_raw"].get("perfil") == "resultado_execucao"


def test_ausencia_de_perfil_rejeitada_para_id_resultado():
    with tempfile.TemporaryDirectory() as tmp:
        dados = _tela_base()
        del dados["perfil"]
        _escrever_tela(tmp, dados)
        with pytest.raises(TelaCampoObrigatorioAusente) as exc:
            carregar_tela(tmp, "resultado_execucao", "config/telas/demo")
        assert exc.value.campo == "perfil"


def test_perfil_desconhecido_rejeitado():
    with tempfile.TemporaryDirectory() as tmp:
        dados = _tela_base(perfil="desconhecido", id="perfil_x")
        dados["id"] = "perfil_x"
        _escrever_tela(tmp, dados)
        with pytest.raises(TelaEstruturaInvalida) as exc:
            carregar_tela(tmp, "perfil_x", "config/telas/demo")
        assert "perfil desconhecido" in str(exc.value)


@pytest.mark.parametrize(
    "mutacao,trecho",
    [
        (
            lambda d: d["corpo"]["elementos"].append(
                {
                    "id": "outro",
                    "tipo": "console",
                    "titulo": "X",
                    "formato": {
                        "excesso": {"politica_modo": "somente_verboso"}
                    },
                }
            ),
            "exatamente um",
        ),
        (
            lambda d: d["corpo"]["elementos"].__setitem__(
                0,
                {
                    "id": "dash",
                    "tipo": "dashboard",
                    "titulo": "D",
                    "origem_dados": None,
                    "itens": [],
                    "politica_composicao": {},
                    "politica_navegacao": {},
                    "politica_selecao": "nenhuma",
                    "politica_paginacao": "sem",
                    "politica_exibicao": {},
                },
            ),
            "console",
        ),
        (
            lambda d: d["barra_de_menus"]["chips"].append(
                {"id": "extra", "tecla": "?", "texto": "Ajuda"}
            ),
            "exatamente um",
        ),
        (
            lambda d: d["barra_de_menus"].__setitem__("chips", []),
            "Esc/Voltar",
        ),
        (
            lambda d: d["barra_de_menus"].__setitem__(
                "chips",
                [{"id": "v", "tecla": "V", "texto": "Verboso"}],
            ),
            "Esc/Voltar",
        ),
        (
            lambda d: d["corpo"]["elementos"][0]["formato"]["excesso"].__setitem__(
                "modo_inicial", "verboso"
            ),
            "modo_inicial",
        ),
        (
            lambda d: d["corpo"]["elementos"][0]["formato"]["excesso"].__setitem__(
                "politica_modo", "somente_nao_verboso"
            ),
            "somente_verboso",
        ),
        (
            lambda d: d["corpo"]["elementos"][0]["formato"]["excesso"].__setitem__(
                "overflow_normal", "truncar_com_reticencias"
            ),
            "overflow_normal",
        ),
        (
            lambda d: d["corpo"].__setitem__(
                "distribuicao", {"modo": "igual"}
            ),
            "distribuicao",
        ),
    ],
)
def test_perfil_rejeita_estrutura_invalida(mutacao, trecho):
    with tempfile.TemporaryDirectory() as tmp:
        dados = _tela_base()
        mutacao(dados)
        _escrever_tela(tmp, dados)
        with pytest.raises(TelaEstruturaInvalida) as exc:
            carregar_tela(tmp, "resultado_execucao", "config/telas/demo")
        assert trecho in str(exc.value)


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("origem_dados", None),
        ("itens", []),
        ("politica_composicao", {"alinhamento": "esquerda"}),
        ("politica_navegacao", {"navegavel": False}),
        ("politica_selecao", "nenhuma"),
        ("politica_paginacao", "sem"),
        ("politica_exibicao", {}),
    ],
)
def test_perfil_rejeita_campo_classico_d23(campo, valor):
    with tempfile.TemporaryDirectory() as tmp:
        dados = _tela_base()
        dados["corpo"]["elementos"][0][campo] = valor
        _escrever_tela(tmp, dados)
        with pytest.raises(TelaEstruturaInvalida) as exc:
            carregar_tela(tmp, "resultado_execucao", "config/telas/demo")
        msg = str(exc.value)
        assert (
            campo in msg
            or "mutuamente exclusivos" in msg
            or "campos classicos" in msg
            or "nao permitidos" in msg
        )


def test_conteudo_runtime_incorporado_a_tela_rejeitado():
    with tempfile.TemporaryDirectory() as tmp:
        dados = _tela_base()
        dados["corpo"]["elementos"][0]["dados"] = [{"id": "x"}]
        _escrever_tela(tmp, dados)
        with pytest.raises(TelaEstruturaInvalida) as exc:
            carregar_tela(tmp, "resultado_execucao", "config/telas/demo")
        assert "dados" in str(exc.value)


# ---------------------------------------------------------------------------
# Documento versus envelope
# ---------------------------------------------------------------------------


def _doc_sucesso_minimo():
    return {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "conjuntos_campos",
            "niveis": [
                {
                    "id": "secao",
                    "tipo": "container",
                    "conteudo": "titulo",
                    "designador": {"tipo": "nenhum"},
                },
                {
                    "id": "registro",
                    "tipo": "container",
                    "conteudo": "titulo",
                    "designador": {"tipo": "nenhum"},
                },
                {
                    "id": "campo",
                    "tipo": "nome_valor",
                    "conteudo": {"nome": "nome", "valor": "valor"},
                    "designador": {"tipo": "nenhum"},
                },
            ],
            "campos": {},
        },
        "dados": [
            {
                "id": "secao_resumo",
                "nivel": "secao",
                "titulo": "Resumo",
                "filhos": [
                    {
                        "id": "reg_execucao",
                        "nivel": "registro",
                        "titulo": "Execução",
                        "filhos": [
                            {
                                "id": "resumo_modo",
                                "nivel": "campo",
                                "nome": "modo",
                                "valor": "executar",
                            },
                            {
                                "id": "resumo_status",
                                "nivel": "campo",
                                "nome": "status",
                                "valor": "sucesso",
                            },
                            {
                                "id": "resumo_solicitados",
                                "nivel": "campo",
                                "nome": "solicitados",
                                "valor": 0,
                            },
                            {
                                "id": "resumo_processados",
                                "nivel": "campo",
                                "nome": "processados",
                                "valor": 0,
                            },
                            {
                                "id": "resumo_ignorados",
                                "nivel": "campo",
                                "nome": "ignorados",
                                "valor": 0,
                            },
                            {
                                "id": "resumo_nao_encontrados",
                                "nivel": "campo",
                                "nome": "nao_encontrados",
                                "valor": 0,
                            },
                            {
                                "id": "resumo_falhos",
                                "nivel": "campo",
                                "nome": "falhos",
                                "valor": 0,
                            },
                        ],
                    }
                ],
            },
            {
                "id": "secao_itens",
                "nivel": "secao",
                "titulo": "Itens",
                "filhos": [],
            },
        ],
    }


@pytest.mark.parametrize(
    "status",
    ["sucesso", "parcial", "falha"],
)
def test_documento_valido_codigo_zero_apresenta_documento(status):
    doc = _doc_sucesso_minimo()
    doc["dados"][0]["filhos"][0]["filhos"][1]["valor"] = status
    bruto = json.dumps(doc, ensure_ascii=False)
    runtime = DocumentoRuntime(0, "", "", bruto)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_DOCUMENTO
    assert diag is None


def test_codigo_nao_zero_com_json_valido_gera_envelope():
    bruto = json.dumps(_doc_sucesso_minimo(), ensure_ascii=False)
    runtime = DocumentoRuntime(1, "out", "err", bruto)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_CODIGO_NAO_ZERO


def test_codigo_nao_zero_sem_resultado_gera_envelope():
    runtime = DocumentoRuntime(2, "", "", None)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_CODIGO_NAO_ZERO


def test_resultado_ausente_codigo_zero():
    runtime = DocumentoRuntime(0, "", "", None)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_RESULTADO_AUSENTE


def test_json_malformado_gera_envelope():
    runtime = DocumentoRuntime(0, "", "", "{nao")
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_RESULTADO_MALFORMADO


def test_documento_semanticamente_invalido_gera_envelope():
    runtime = DocumentoRuntime(0, "", "", '{"tipo":"multinivel"}')
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_RESULTADO_SEMANTICO


def test_interrupcao_codigo_130():
    runtime = DocumentoRuntime(130, "", "", None)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_INTERRUPCAO


def test_interrupcao_preserva_resultado_previo():
    bruto = '  {\n  "previo": true\n}  '
    runtime = DocumentoRuntime(130, "o", "e", bruto)
    apr, diag = classificar_apresentacao(runtime)
    assert apr == APRESENTACAO_ENVELOPE
    assert diag == DIAGNOSTICO_INTERRUPCAO
    envelope = materializar_envelope(runtime, diag)
    filhos = envelope["dados"][0]["filhos"]
    mapa = {f["nome"]: f["valor"] for f in filhos}
    assert mapa["resultado_json"] == bruto


# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------


def test_envelope_ordem_e_campos_obrigatorios():
    runtime = DocumentoRuntime(1, "", "", None)
    envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
    filhos = envelope["dados"][0]["filhos"]
    assert [f["nome"] for f in filhos] == list(CAMPOS_ENVELOPE_ORDEM)
    assert len(filhos) == 6
    assert filhos[0]["valor"] == "falha"


@pytest.mark.parametrize(
    "diag",
    [
        DIAGNOSTICO_CODIGO_NAO_ZERO,
        DIAGNOSTICO_RESULTADO_AUSENTE,
        DIAGNOSTICO_RESULTADO_MALFORMADO,
        DIAGNOSTICO_RESULTADO_SEMANTICO,
        DIAGNOSTICO_INTERRUPCAO,
    ],
)
def test_diagnosticos_canonicos(diag):
    codigo = 130 if diag == DIAGNOSTICO_INTERRUPCAO else 1
    runtime = DocumentoRuntime(codigo, "", "", None)
    envelope = materializar_envelope(runtime, diag)
    filhos = envelope["dados"][0]["filhos"]
    assert filhos[1]["valor"] == diag
    assert filhos[0]["valor"] == "falha"


def test_canais_vazios_exibem_indisponivel_resultado_json_permanece_null():
    runtime = DocumentoRuntime(1, "", "", None)
    envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
    mapa = {f["nome"]: f["valor"] for f in envelope["dados"][0]["filhos"]}
    assert mapa["stdout"] == EXIBICAO_INDISPONIVEL
    assert mapa["stderr"] == EXIBICAO_INDISPONIVEL
    # QA-IMPL-H0043-001: o modelo preserva a ausencia semantica como `None`;
    # somente a apresentacao converte para o texto "indisponível".
    assert mapa["resultado_json"] is None


def test_resultado_json_null_e_campo_obrigatorio_na_sexta_posicao():
    runtime = DocumentoRuntime(1, "", "", None)
    envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
    filhos = envelope["dados"][0]["filhos"]
    assert [f["nome"] for f in filhos] == list(CAMPOS_ENVELOPE_ORDEM)
    assert filhos[5]["nome"] == "resultado_json"
    assert filhos[5]["valor"] is None


def test_resultado_json_null_apresentado_como_indisponivel_no_quadro():
    tela = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS)
    runtime = DocumentoRuntime(1, "", "", None)
    sessao = construir_modelo_resultado(tela, runtime)
    assert sessao.conteudo_apresentado["dados"][0]["filhos"][5]["valor"] is None
    saida = renderizar_tela(
        sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
    )
    assert "resultado_json" in saida
    assert "indisponível" in saida


def test_resultado_json_com_conteudo_nao_e_substituido_por_indisponivel():
    for bruto in (
        '{\n  "a": 1,\n  "b": 2\n}',
        '{"a":\n',
        '  {\n  "previo": true\n}  ',
    ):
        runtime = DocumentoRuntime(1, "x", "y", bruto)
        envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
        mapa = {f["nome"]: f["valor"] for f in envelope["dados"][0]["filhos"]}
        assert mapa["resultado_json"] == bruto
        assert mapa["resultado_json"] != EXIBICAO_INDISPONIVEL


def test_preservacao_literal_json_valido_e_invalido():
    valido = '{\n  "a": 1,\n  "b": 2\n}'
    invalido = '{\n  "a":\n'
    for bruto in (valido, invalido):
        runtime = DocumentoRuntime(1, "x", "y", bruto)
        envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
        mapa = {f["nome"]: f["valor"] for f in envelope["dados"][0]["filhos"]}
        assert mapa["resultado_json"] == bruto
    # Nao reserializa: ordem/espacos do texto bruto permanecem.
    reserializado = json.dumps(json.loads(valido), ensure_ascii=False)
    assert valido != reserializado
    runtime = DocumentoRuntime(1, "", "", valido)
    mapa = {
        f["nome"]: f["valor"]
        for f in materializar_envelope(
            runtime, DIAGNOSTICO_CODIGO_NAO_ZERO
        )["dados"][0]["filhos"]
    }
    assert mapa["resultado_json"] == valido
    assert mapa["resultado_json"] != reserializado


def test_ausencia_de_normalizacao_e_estilo_especial():
    bruto = '{"z":1,"a":2}'
    runtime = DocumentoRuntime(7, "stdout-x", "stderr-y", bruto)
    envelope = materializar_envelope(runtime, DIAGNOSTICO_CODIGO_NAO_ZERO)
    assert "cor_alerta" not in json.dumps(envelope)
    assert envelope["formato"]["apresentacao"] == "conjuntos_campos"
    mapa = {f["nome"]: f["valor"] for f in envelope["dados"][0]["filhos"]}
    assert mapa["resultado_json"] == bruto
    assert mapa["stdout"] == "stdout-x"
    assert mapa["stderr"] == "stderr-y"


# ---------------------------------------------------------------------------
# Sessao, carregamento unico, SIGWINCH
# ---------------------------------------------------------------------------


def test_carregamento_unico_e_modelo_em_memoria(monkeypatch):
    contadores = {"tela": 0, "runtime": 0}
    original_tela = carregar_tela
    original_runtime = carregar_documento_runtime

    def spy_tela(*args, **kwargs):
        contadores["tela"] += 1
        return original_tela(*args, **kwargs)

    def spy_runtime(*args, **kwargs):
        contadores["runtime"] += 1
        return original_runtime(*args, **kwargs)

    monkeypatch.setattr(re, "carregar_documento_runtime", spy_runtime)
    monkeypatch.setattr(
        "tela.resultado_execucao.carregar_tela", spy_tela
    )
    monkeypatch.setattr(
        "tela.loader.carregar_tela", spy_tela
    )

    sessao = carregar_sessao_resultado(
        None,
        "h0043_resultado_sucesso",
        _FIX / "h0043_resultado_sucesso.json",
    )
    assert contadores["tela"] == 1
    assert contadores["runtime"] == 1
    saida1 = renderizar_tela(
        sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
    )
    saida2 = renderizar_tela(
        sessao.modelo, _ESTILO, largura=100, altura=30, verboso=True
    )
    assert contadores["tela"] == 1
    assert contadores["runtime"] == 1
    assert saida1.count("\n") == 24
    assert saida2.count("\n") == 30
    assert saida1 != saida2


def test_alteracao_posterior_da_origem_nao_afeta_sessao():
    with tempfile.TemporaryDirectory() as tmp:
        origem = Path(tmp) / "runtime.json"
        shutil.copy(_FIX / "h0043_resultado_sucesso.json", origem)
        sessao = carregar_sessao_resultado(
            None, "tmp", origem
        )
        antes = renderizar_tela(
            sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
        )
        origem.write_text(
            json.dumps(
                {
                    "codigo_saida": 130,
                    "stdout": "",
                    "stderr": "",
                    "resultado_bruto": None,
                }
            ),
            encoding="utf-8",
        )
        depois = renderizar_tela(
            sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
        )
        assert antes == depois
        assert sessao.apresentacao == APRESENTACAO_DOCUMENTO


def test_sigwinch_recalcula_sem_releitura(monkeypatch):
    leituras = {"n": 0}
    caminho = _FIX / "h0043_envelope_interrupcao.json"
    original = Path.read_text

    def spy_read(self, *args, **kwargs):
        if self.resolve() == caminho.resolve():
            leituras["n"] += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", spy_read)
    sessao = carregar_sessao_resultado(None, "int", caminho)
    n_apos_carga = leituras["n"]
    assert n_apos_carga >= 1
    q1 = renderizar_tela(
        sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
    )
    q2 = renderizar_tela(
        sessao.modelo, _ESTILO, largura=90, altura=28, verboso=True
    )
    assert leituras["n"] == n_apos_carga
    assert q1.count("\n") == 24
    assert q2.count("\n") == 28
    assert "A execução foi interrompida." in q1
    assert "A execução foi interrompida." in q2


def test_quadro_sem_residuos_entre_cenarios():
    saidas = []
    for cenario in _CENARIOS:
        sessao = carregar_sessao_resultado(
            None, cenario, _FIX / (cenario + ".json")
        )
        saida = renderizar_tela(
            sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
        )
        saidas.append(saida)
    assert len(set(saidas)) == 6


# ---------------------------------------------------------------------------
# Integracao e quadros 80x24
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cenario", _CENARIOS)
def test_quadro_80x24_integral(cenario):
    sessao = carregar_sessao_resultado(
        None, cenario, _FIX / (cenario + ".json")
    )
    obtido = renderizar_tela(
        sessao.modelo, _ESTILO, largura=80, altura=24, verboso=True
    )
    esperado = (_FIX / _QUADROS[cenario]).read_text(encoding="utf-8")
    assert obtido == esperado
    assert obtido.count("\n") == 24
    for linha in obtido.split("\n")[:-1]:
        assert len(linha) <= 80
    assert "[Esc] Voltar" in obtido
    assert "[V]" not in obtido


def test_seis_cenarios_via_demo_carregar_modelo():
    from demo import demo as demo_mod

    for cenario in _CENARIOS:
        modelo = demo_mod._carregar_modelo_por_id(cenario)
        assert modelo.id == "resultado_execucao"
        assert modelo.corpo.elementos[0].politica_modo == "somente_verboso"
        saida = renderizar_tela(
            modelo, _ESTILO, largura=80, altura=24, verboso=True
        )
        esperado = (_FIX / _QUADROS[cenario]).read_text(encoding="utf-8")
        assert saida == esperado


def test_catalogo_resultado_nao_usa_conteudo_externo_classico():
    from demo import demo as demo_mod

    for cenario in _CENARIOS:
        assert demo_mod.id_conteudo_externo_de(cenario) is None
        assert cenario in demo_mod._CATALOGO_CENARIOS_RESULTADO_EXECUCAO


def test_fixtures_runtime_forma_h0042():
    for cenario in _CENARIOS:
        doc = carregar_documento_runtime(_FIX / (cenario + ".json"))
        assert isinstance(doc.codigo_saida, int)
        assert isinstance(doc.stdout, str)
        assert isinstance(doc.stderr, str)


def test_construir_modelo_resultado_nao_altera_runtime():
    bruto = ' {"x":1} '
    runtime = DocumentoRuntime(1, "a", "b", bruto)
    tela = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS)
    sessao = construir_modelo_resultado(tela, runtime)
    assert runtime.resultado_bruto == bruto
    assert sessao.apresentacao == APRESENTACAO_ENVELOPE
