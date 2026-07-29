"""Testes da demonstracao completa do protocolo focal (H-0042)."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))
_this = str(Path(__file__).resolve().parent)
while _this in sys.path:
    sys.path.remove(_this)

import demo.demo_execucao_focal as demo  # noqa: E402
import demo.executor_sintetico as ex  # noqa: E402
from tela import execucao_focal  # noqa: E402


FIXTURES = _BASE / "demo" / "fixtures"
BASELINE = FIXTURES / "h0042_fixture_execucao.json"
ENTRADA_SUCESSO = FIXTURES / "h0042_entrada_sucesso.json"
ENTRADA_AVISO = FIXTURES / "h0042_entrada_sucesso_aviso.json"
ENTRADA_PARCIAL = FIXTURES / "h0042_entrada_parcial.json"
ENTRADA_FALHA = FIXTURES / "h0042_entrada_falha_operacional.json"
ENTRADA_INVALIDO = FIXTURES / "h0042_entrada_resultado_invalido.json"
ENTRADA_INTERRUPCAO = FIXTURES / "h0042_entrada_interrupcao.json"


def _rodar_demo(entrada, *, dry_run=False):
    cmd = [
        sys.executable,
        "-m",
        "demo.demo_execucao_focal",
        "--entrada",
        str(entrada),
        "--fixture",
        str(BASELINE),
    ]
    if dry_run:
        cmd.append("--dry-run")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(_BASE),
        env=env,
        check=False,
    )


def _baseline():
    return BASELINE.read_text(encoding="utf-8")


def _ids_de(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))["ids"]


class TestDemoExecucaoFocal:
    def test_dry_run(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_SUCESSO, dry_run=True)
        assert proc.returncode == 0
        assert "codigo_saida: 0" in proc.stdout
        assert "classificacao: sucesso" in proc.stdout
        assert "status: sucesso" in proc.stdout
        assert "temporario_removido: True" in proc.stdout
        assert "baseline_intacta: True" in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_execucao_real(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_SUCESSO, dry_run=False)
        assert proc.returncode == 0
        assert "codigo_saida: 0" in proc.stdout
        assert "classificacao: sucesso" in proc.stdout
        assert "stderr: ''" in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_sucesso_com_aviso_ca09(self):
        antes = _baseline()
        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_AVISO, BASELINE, dry_run=False
        )
        assert r["codigo_saida"] == 0
        assert r["stderr"] == ex.AVISO_TODOS_PROCESSADOS
        doc = json.loads(r["resultado_bruto"])
        status = None
        for secao in doc["dados"]:
            if secao.get("titulo") == "Resumo":
                for reg in secao["filhos"]:
                    for campo in reg["filhos"]:
                        if campo.get("nome") == "status":
                            status = campo.get("valor")
        assert status == "sucesso"

        proc = _rodar_demo(ENTRADA_AVISO, dry_run=False)
        assert proc.returncode == 0
        assert "codigo_saida: 0" in proc.stdout
        assert "classificacao: sucesso" in proc.stdout
        assert "status: sucesso" in proc.stdout
        assert repr(ex.AVISO_TODOS_PROCESSADOS) in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_parcial(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_PARCIAL)
        assert proc.returncode == 0
        assert "status: parcial" in proc.stdout
        assert "classificacao: sucesso" in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_sucesso_aviso_parcial_retornam_zero_no_demonstrador(self):
        for entrada in (ENTRADA_SUCESSO, ENTRADA_AVISO, ENTRADA_PARCIAL):
            proc = _rodar_demo(entrada)
            assert proc.returncode == 0, entrada.name

    def test_falha_operacional_esperada_retorna_zero(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_FALHA)
        assert proc.returncode == 0
        assert "codigo_saida: 1" in proc.stdout or "codigo_saida: " in proc.stdout
        assert "classificacao: falha" in proc.stdout
        # Codigo observado do executor permanece nao zero no resumo.
        linha = [
            ln for ln in proc.stdout.splitlines() if ln.startswith("codigo_saida:")
        ][0]
        codigo_obs = int(linha.split(":", 1)[1].strip())
        assert codigo_obs != 0
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_resultado_invalido_esperado_retorna_zero(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_INVALIDO)
        assert proc.returncode == 0
        assert "codigo_saida: 0" in proc.stdout
        assert "classificacao: falha" in proc.stdout
        assert "resultado_semanticamente_valido: False" in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_interrupcao_esperada_retorna_zero(self):
        antes = _baseline()
        proc = _rodar_demo(ENTRADA_INTERRUPCAO)
        assert proc.returncode == 0
        assert "codigo_saida: 130" in proc.stdout
        assert "status: interrompido" in proc.stdout
        assert "classificacao: falha" in proc.stdout
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_resumo_preserva_codigos_observados_1_0_130(self):
        p_falha = _rodar_demo(ENTRADA_FALHA)
        p_inv = _rodar_demo(ENTRADA_INVALIDO)
        p_int = _rodar_demo(ENTRADA_INTERRUPCAO)
        assert p_falha.returncode == 0
        assert p_inv.returncode == 0
        assert p_int.returncode == 0
        assert "codigo_saida: 1" in p_falha.stdout
        assert "codigo_saida: 0" in p_inv.stdout
        assert "codigo_saida: 130" in p_int.stdout

    def test_cenario_divergente_retorna_nao_zero(self, tmp_path, monkeypatch):
        # Entrada normal exige sucesso; forca classificacao divergente.
        entrada = tmp_path / "entrada.json"
        entrada.write_text(
            json.dumps({"schema": "selecao_execucao.v1", "ids": ["item_01"]}),
            encoding="utf-8",
        )
        fixture = tmp_path / "fixture.json"
        fixture.write_text(_baseline(), encoding="utf-8")

        def _falso(*args, **kwargs):
            return {
                "codigo_saida": 1,
                "stdout": "",
                "stderr": "erro\n",
                "resultado_bruto": None,
                "resultado_existe": False,
                "classificacao": "falha",
                "entrada_valida": True,
                "invocou": True,
                "dry_run": False,
                "diretorio_removido": True,
            }

        monkeypatch.setattr(demo.execucao_focal, "executar_protocolo_focal", _falso)
        codigo = demo.main(
            [
                "demo.demo_execucao_focal",
                "--entrada",
                str(entrada),
                "--fixture",
                str(fixture),
            ]
        )
        assert codigo != 0

    def test_expectativa_determinada_pelos_ids(self):
        assert demo.expectativa_de_ids(["item_01", "item_03"])["cenario"] == "normal"
        assert (
            demo.expectativa_de_ids(["__falha_operacional__"])["cenario"]
            == "falha_operacional"
        )
        assert (
            demo.expectativa_de_ids(["__resultado_invalido__"])["cenario"]
            == "resultado_invalido"
        )
        assert (
            demo.expectativa_de_ids(["item_01", "__interrupcao__"])["cenario"]
            == "interrupcao"
        )
        assert demo.expectativa_de_ids(["item_01", "__interrupcao__"])[
            "exige_alteracao_pre_interrupcao"
        ] is True

    def test_expectativa_nao_depende_do_nome_do_arquivo(self, tmp_path):
        # Mesmo conteudo de falha operacional com nome arbitrario.
        entrada = tmp_path / "nome_qualquer_sucesso.json"
        entrada.write_text(
            json.dumps(
                {"schema": "selecao_execucao.v1", "ids": ["__falha_operacional__"]}
            ),
            encoding="utf-8",
        )
        ids = _ids_de(entrada)
        exp = demo.expectativa_de_ids(ids)
        assert exp["cenario"] == "falha_operacional"
        assert entrada.name == "nome_qualquer_sucesso.json"
        # Demonstracao usa somente ids, nao o nome do arquivo.
        proc = _rodar_demo(entrada)
        assert proc.returncode == 0
        assert "classificacao: falha" in proc.stdout
        linha = [
            ln for ln in proc.stdout.splitlines() if ln.startswith("codigo_saida:")
        ][0]
        assert int(linha.split(":", 1)[1].strip()) != 0

    def test_limpeza_e_baseline_apos_todos(self):
        antes = _baseline()
        for entrada, dry in [
            (ENTRADA_SUCESSO, True),
            (ENTRADA_SUCESSO, False),
            (ENTRADA_AVISO, False),
            (ENTRADA_PARCIAL, False),
            (ENTRADA_FALHA, False),
            (ENTRADA_INVALIDO, False),
            (ENTRADA_INTERRUPCAO, False),
        ]:
            proc = _rodar_demo(entrada, dry_run=dry)
            assert proc.returncode == 0, entrada.name
        assert BASELINE.read_text(encoding="utf-8") == antes
