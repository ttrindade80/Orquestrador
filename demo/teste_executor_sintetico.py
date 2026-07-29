"""Testes focais do executor sintetico (H-0042)."""

import json
import sys
from pathlib import Path

import pytest

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))
_this = str(Path(__file__).resolve().parent)
while _this in sys.path:
    sys.path.remove(_this)

import demo.executor_sintetico as ex  # noqa: E402
from tela.execucao_focal import EntradaInvalida  # noqa: E402


FIXTURES = _BASE / "demo" / "fixtures"
BASELINE = FIXTURES / "h0042_fixture_execucao.json"


def _campo_resumo(doc, nome):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Resumo":
            for reg in secao["filhos"]:
                for campo in reg["filhos"]:
                    if campo.get("nome") == nome:
                        return campo.get("valor")
    raise AssertionError(nome)


def _campo_item(doc, id_item, nome):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Itens":
            for reg in secao["filhos"]:
                if reg.get("titulo") == id_item:
                    for campo in reg["filhos"]:
                        if campo.get("nome") == nome:
                            return campo.get("valor")
    raise AssertionError(f"{id_item}.{nome}")


def _ids_itens(doc):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Itens":
            return [r["titulo"] for r in secao["filhos"]]
    raise AssertionError("Itens")


def _preparar(tmp_path, ids, fixture_texto=None):
    entrada = tmp_path / "entrada.json"
    resultado = tmp_path / "resultado.json"
    fixture = tmp_path / "fixture_trabalho.json"
    entrada.write_text(
        json.dumps({"schema": "selecao_execucao.v1", "ids": ids}),
        encoding="utf-8",
    )
    resultado.write_text("", encoding="utf-8")
    fixture.write_text(
        fixture_texto if fixture_texto is not None else BASELINE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return entrada, resultado, fixture


class TestValidacaoExecutor:
    def test_schema_valido(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(tmp_path, ["item_01"])
        codigo = ex.executar(entrada, resultado, dry_run=True)
        assert codigo == 0
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert doc["tipo"] == "multinivel"
        assert doc["formato"]["apresentacao"] == "conjuntos_campos"

    @pytest.mark.parametrize(
        "dados",
        [
            {"ids": ["a"]},
            {"schema": "outro.v1", "ids": ["a"]},
            {"schema": "selecao_execucao.v1"},
            {"schema": "selecao_execucao.v1", "ids": "a"},
            {"schema": "selecao_execucao.v1", "ids": []},
            {"schema": "selecao_execucao.v1", "ids": [""]},
            {"schema": "selecao_execucao.v1", "ids": [1]},
            {"schema": "selecao_execucao.v1", "ids": ["a", "a"]},
        ],
    )
    def test_rejeicao_integral(self, tmp_path, dados, capsys):
        entrada = tmp_path / "entrada.json"
        resultado = tmp_path / "resultado.json"
        fixture = tmp_path / "fixture_trabalho.json"
        entrada.write_text(json.dumps(dados), encoding="utf-8")
        resultado.write_text("", encoding="utf-8")
        antes = BASELINE.read_text(encoding="utf-8")
        fixture.write_text(antes, encoding="utf-8")
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo != 0
        assert fixture.read_text(encoding="utf-8") == antes
        err = capsys.readouterr().err
        assert "entrada invalida" in err


class TestSemantica:
    def test_dry_run_item_01(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(tmp_path, ["item_01"])
        antes = fixture.read_text(encoding="utf-8")
        codigo = ex.executar(entrada, resultado, dry_run=True)
        assert codigo == 0
        assert fixture.read_text(encoding="utf-8") == antes
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _campo_item(doc, "item_01", "resultado") == "processado"
        assert _campo_item(doc, "item_01", "aplicado") is False
        assert _campo_item(doc, "item_01", "processado_depois") is True
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

    def test_execucao_real_e_ignorado(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(tmp_path, ["item_01", "item_03"])
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 0
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _campo_resumo(doc, "status") == "sucesso"
        assert _ids_itens(doc) == ["item_01", "item_03"]
        assert _campo_item(doc, "item_03", "resultado") == "ignorado"
        fx = json.loads(fixture.read_text(encoding="utf-8"))
        assert {i["id"]: i["processado"] for i in fx["itens"]}["item_01"] is True
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

    def test_parcial(self, tmp_path):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["item_01", "item_inexistente"]
        )
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 0
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _campo_resumo(doc, "status") == "parcial"
        assert _ids_itens(doc) == ["item_01", "item_inexistente"]
        assert _campo_item(doc, "item_inexistente", "diagnostico") == (
            ex.DIAGNOSTICO_NAO_ENCONTRADO
        )

    def test_sucesso_com_aviso(self, tmp_path, capsys):
        # CA-09: somente item_03 ja processado.
        entrada = FIXTURES / "h0042_entrada_sucesso_aviso.json"
        resultado = tmp_path / "resultado.json"
        fixture = tmp_path / "fixture_trabalho.json"
        resultado.write_text("", encoding="utf-8")
        antes = BASELINE.read_text(encoding="utf-8")
        fixture.write_text(antes, encoding="utf-8")
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 0
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _campo_resumo(doc, "status") == "sucesso"
        assert _campo_item(doc, "item_03", "resultado") == "ignorado"
        assert fixture.read_text(encoding="utf-8") == antes
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ex.AVISO_TODOS_PROCESSADOS

    def test_sucesso_misto_sem_aviso(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(tmp_path, ["item_01", "item_03"])
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 0
        assert capsys.readouterr().err == ""

    def test_falha_operacional(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["__falha_operacional__"]
        )
        antes = fixture.read_text(encoding="utf-8")
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo != 0
        assert fixture.read_text(encoding="utf-8") == antes
        assert capsys.readouterr().err == ex.STDERR_FALHA_OPERACIONAL

    def test_resultado_invalido_literal(self, tmp_path):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["__resultado_invalido__"]
        )
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 0
        assert resultado.read_text(encoding="utf-8") == ex.TEXTO_RESULTADO_INVALIDO

    def test_interrupcao(self, tmp_path):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["item_01", "__interrupcao__"]
        )
        codigo = ex.executar(entrada, resultado, dry_run=False)
        assert codigo == 130
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _campo_resumo(doc, "status") == "interrompido"
        assert _campo_item(doc, "item_01", "aplicado") is True
        fx = json.loads(fixture.read_text(encoding="utf-8"))
        assert {i["id"]: i["processado"] for i in fx["itens"]}["item_01"] is True

    def test_controle_nao_e_nao_encontrado(self, tmp_path, capsys):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["__falha_operacional__"]
        )
        ex.executar(entrada, resultado, dry_run=False)
        # Nao grava documento de sucesso com nao_encontrado.
        texto = resultado.read_text(encoding="utf-8")
        assert "nao_encontrado" not in texto

    def test_controles_ausentes_baseline(self):
        fx = json.loads(BASELINE.read_text(encoding="utf-8"))
        ids = {i["id"] for i in fx["itens"]}
        for c in ex.CONTROLES:
            assert c not in ids

    def test_cli_sem_fixture(self):
        with pytest.raises(SystemExit):
            ex._parse_argv(
                [
                    "demo.executor_sintetico",
                    "--entrada",
                    "a.json",
                    "--resultado",
                    "b.json",
                    "--fixture",
                    "c.json",
                ]
            )

    def test_ordem_preservada(self, tmp_path):
        entrada, resultado, fixture = _preparar(
            tmp_path, ["item_07", "item_01", "item_05"]
        )
        codigo = ex.executar(entrada, resultado, dry_run=True)
        assert codigo == 0
        doc = json.loads(resultado.read_text(encoding="utf-8"))
        assert _ids_itens(doc) == ["item_07", "item_01", "item_05"]
