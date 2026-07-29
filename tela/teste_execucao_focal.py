"""Testes unitarios e de integracao do protocolo focal (H-0042)."""

import inspect
import json
import subprocess
import sys
from pathlib import Path

import pytest

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))

from tela import execucao_focal
from demo import executor_sintetico as ex


FIXTURES = _BASE / "demo" / "fixtures"
BASELINE = FIXTURES / "h0042_fixture_execucao.json"
ENTRADA_SUCESSO = FIXTURES / "h0042_entrada_sucesso.json"
ENTRADA_AVISO = FIXTURES / "h0042_entrada_sucesso_aviso.json"
ENTRADA_PARCIAL = FIXTURES / "h0042_entrada_parcial.json"
ENTRADA_FALHA = FIXTURES / "h0042_entrada_falha_operacional.json"
ENTRADA_INVALIDO = FIXTURES / "h0042_entrada_resultado_invalido.json"
ENTRADA_INTERRUPCAO = FIXTURES / "h0042_entrada_interrupcao.json"


def _baseline_texto():
    return BASELINE.read_text(encoding="utf-8")


def _campo_resumo(doc, nome):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Resumo":
            for reg in secao["filhos"]:
                for campo in reg["filhos"]:
                    if campo.get("nome") == nome:
                        return campo.get("valor")
    raise AssertionError(f"campo resumo ausente: {nome}")


def _ids_itens(doc):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Itens":
            return [r["titulo"] for r in secao["filhos"]]
    raise AssertionError("secao Itens ausente")


def _campo_item(doc, id_item, nome):
    for secao in doc["dados"]:
        if secao.get("titulo") == "Itens":
            for reg in secao["filhos"]:
                if reg.get("titulo") == id_item:
                    for campo in reg["filhos"]:
                        if campo.get("nome") == nome:
                            return campo.get("valor")
    raise AssertionError(f"campo {nome} de {id_item} ausente")


def _doc_valido(*, status="sucesso", modo="executar", itens=None):
    if itens is None:
        itens = [
            {
                "id": "item_01",
                "resultado": "processado",
                "aplicado": True,
                "processado_antes": False,
                "processado_depois": True,
            }
        ]
    filhos_itens = []
    for item in itens:
        campos = [
            ("id", item["id"]),
            ("resultado", item["resultado"]),
            ("aplicado", item["aplicado"]),
            ("processado_antes", item["processado_antes"]),
            ("processado_depois", item["processado_depois"]),
        ]
        if "diagnostico" in item:
            campos.append(("diagnostico", item["diagnostico"]))
        filhos = [
            {
                "id": f"{item['id']}__{nome}",
                "nivel": "campo",
                "nome": nome,
                "valor": valor,
            }
            for nome, valor in campos
        ]
        filhos_itens.append(
            {
                "id": f"reg_{item['id']}",
                "nivel": "registro",
                "titulo": item["id"],
                "filhos": filhos,
            }
        )
    contagens = {
        "solicitados": len(itens),
        "processados": sum(1 for i in itens if i["resultado"] == "processado"),
        "ignorados": sum(1 for i in itens if i["resultado"] == "ignorado"),
        "nao_encontrados": sum(
            1 for i in itens if i["resultado"] == "nao_encontrado"
        ),
        "falhos": sum(1 for i in itens if i["resultado"] == "falhou"),
    }
    resumo_campos = [
        ("modo", modo),
        ("status", status),
        ("solicitados", contagens["solicitados"]),
        ("processados", contagens["processados"]),
        ("ignorados", contagens["ignorados"]),
        ("nao_encontrados", contagens["nao_encontrados"]),
        ("falhos", contagens["falhos"]),
    ]
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
                                "id": f"resumo_{nome}",
                                "nivel": "campo",
                                "nome": nome,
                                "valor": valor,
                            }
                            for nome, valor in resumo_campos
                        ],
                    }
                ],
            },
            {
                "id": "secao_itens",
                "nivel": "secao",
                "titulo": "Itens",
                "filhos": filhos_itens,
            },
        ],
    }


def _bruto_valido(**kwargs):
    return json.dumps(_doc_valido(**kwargs), ensure_ascii=False)


# ---------------------------------------------------------------------------
# Validacao de entrada
# ---------------------------------------------------------------------------


class TestValidacaoEntrada:
    def test_schema_valido(self):
        ids = execucao_focal.validar_selecao_execucao(
            {"schema": "selecao_execucao.v1", "ids": ["item_01"]}
        )
        assert ids == ["item_01"]

    def test_schema_ausente(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao({"ids": ["a"]})

    def test_schema_divergente(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "outro.v1", "ids": ["a"]}
            )

    def test_ids_ausente(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1"}
            )

    def test_ids_nao_array(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1", "ids": "item_01"}
            )

    def test_lista_vazia(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1", "ids": []}
            )

    def test_id_vazio(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1", "ids": [""]}
            )

    def test_id_nao_string(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1", "ids": [1]}
            )

    def test_duplicata(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(
                {"schema": "selecao_execucao.v1", "ids": ["a", "a"]}
            )

    def test_raiz_nao_objeto(self):
        with pytest.raises(execucao_focal.EntradaInvalida):
            execucao_focal.validar_selecao_execucao(["item_01"])

    def test_sem_normalizacao_espacos(self):
        # ID com espacos nao e normalizado; permanece string valida.
        ids = execucao_focal.validar_selecao_execucao(
            {"schema": "selecao_execucao.v1", "ids": [" item_01 "]}
        )
        assert ids == [" item_01 "]


# ---------------------------------------------------------------------------
# Classificacao e validacao semantica
# ---------------------------------------------------------------------------


class TestClassificacao:
    def test_objeto_vazio_codigo_0_e_falha(self):
        assert execucao_focal.classificar_processo(0, "{}") == "falha"
        assert execucao_focal.resultado_semanticamente_valido("{}") is False

    def test_lista_codigo_0_e_falha(self):
        assert execucao_focal.classificar_processo(0, "[]") == "falha"
        assert execucao_focal.resultado_semanticamente_valido("[]") is False

    def test_tipo_incorreto_e_falha(self):
        doc = _doc_valido()
        doc["tipo"] = "outro"
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_apresentacao_incorreta_e_falha(self):
        doc = _doc_valido()
        doc["formato"]["apresentacao"] = "hierarquia"
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_niveis_ausentes_e_falha(self):
        doc = _doc_valido()
        doc["formato"]["niveis"] = []
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_niveis_incorretos_e_falha(self):
        doc = _doc_valido()
        doc["formato"]["niveis"][0]["id"] = "grupo"
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_resumo_ausente_e_falha(self):
        doc = _doc_valido()
        doc["dados"] = [d for d in doc["dados"] if d["titulo"] != "Resumo"]
        # completa com secao falsa para manter tamanho
        doc["dados"].insert(
            0,
            {
                "id": "secao_x",
                "nivel": "secao",
                "titulo": "Outro",
                "filhos": [],
            },
        )
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_itens_ausentes_e_falha(self):
        doc = _doc_valido()
        doc["dados"] = [d for d in doc["dados"] if d["titulo"] != "Itens"]
        doc["dados"].append(
            {
                "id": "secao_y",
                "nivel": "secao",
                "titulo": "Outro",
                "filhos": [],
            }
        )
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_registro_individual_incompleto_e_falha(self):
        doc = _doc_valido()
        # remove campo obrigatorio aplicado
        for secao in doc["dados"]:
            if secao["titulo"] == "Itens":
                secao["filhos"][0]["filhos"] = [
                    c
                    for c in secao["filhos"][0]["filhos"]
                    if c["nome"] != "aplicado"
                ]
        bruto = json.dumps(doc)
        assert execucao_focal.classificar_processo(0, bruto) == "falha"

    def test_documento_valido_sucesso(self):
        bruto = _bruto_valido(status="sucesso")
        assert execucao_focal.resultado_semanticamente_valido(bruto) is True
        assert execucao_focal.classificar_processo(0, bruto) == "sucesso"

    def test_documento_valido_parcial(self):
        bruto = _bruto_valido(
            status="parcial",
            itens=[
                {
                    "id": "item_01",
                    "resultado": "processado",
                    "aplicado": True,
                    "processado_antes": False,
                    "processado_depois": True,
                },
                {
                    "id": "item_x",
                    "resultado": "nao_encontrado",
                    "aplicado": False,
                    "processado_antes": None,
                    "processado_depois": None,
                    "diagnostico": "ausente",
                },
            ],
        )
        assert execucao_focal.resultado_semanticamente_valido(bruto) is True
        assert execucao_focal.classificar_processo(0, bruto) == "sucesso"

    def test_documento_valido_interrompido_codigo_130_e_falha(self):
        bruto = _bruto_valido(status="interrompido")
        assert execucao_focal.resultado_semanticamente_valido(bruto) is True
        assert execucao_focal.classificar_processo(130, bruto) == "falha"

    def test_resultado_invalido_preservado_byte_a_byte_na_classificacao(self):
        bruto = ex.TEXTO_RESULTADO_INVALIDO
        assert execucao_focal.classificar_processo(0, bruto) == "falha"
        assert bruto == ex.TEXTO_RESULTADO_INVALIDO

    def test_codigo_0_json_sintatico_invalido_e_falha(self):
        assert execucao_focal.classificar_processo(0, "{invalido") == "falha"

    def test_codigo_nao_zero_e_falha(self):
        assert execucao_focal.classificar_processo(1, _bruto_valido()) == "falha"

    def test_codigo_0_resultado_ausente_e_falha(self):
        assert execucao_focal.classificar_processo(0, None) == "falha"


# ---------------------------------------------------------------------------
# Executor autorizado (ACH-H0042-01)
# ---------------------------------------------------------------------------


class TestExecutorAutorizado:
    def test_assinatura_publica_sem_argv_executor(self):
        params = inspect.signature(
            execucao_focal.executar_protocolo_focal
        ).parameters
        assert "argv_executor" not in params

    def test_argv_executor_rejeitado(self):
        with pytest.raises(TypeError):
            execucao_focal.executar_protocolo_focal(
                ENTRADA_SUCESSO,
                BASELINE,
                dry_run=True,
                argv_executor=[sys.executable, "-c", "import sys; sys.exit(0)"],
            )

    def test_chamada_normal_usa_executor_autorizado(self, monkeypatch):
        capturado = {}

        def _fake(argv, *, cwd, env):
            capturado["argv"] = list(argv)
            capturado["shell_via_kwargs"] = False
            # Delega ao real apos registrar.
            return execucao_focal.subprocess.run(
                argv,
                capture_output=True,
                text=True,
                cwd=cwd,
                env=env,
                check=False,
                shell=False,
            )

        monkeypatch.setattr(execucao_focal, "_invocar_subprocesso", _fake)
        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True
        )
        assert r["invocou"] is True
        argv = capturado["argv"]
        assert argv[0] == sys.executable
        assert argv[1:3] == ["-m", "demo.executor_sintetico"]
        assert "--entrada" in argv
        assert "--resultado" in argv
        assert "--dry-run" in argv
        assert r["codigo_saida"] == 0

    def test_shell_false_na_invocacao(self, monkeypatch):
        capturado = {}
        original = subprocess.run

        def _spy(*args, **kwargs):
            capturado["shell"] = kwargs.get("shell", True)
            capturado["argv"] = list(args[0]) if args else list(kwargs.get("args"))
            return original(*args, **kwargs)

        monkeypatch.setattr(execucao_focal.subprocess, "run", _spy)
        execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True
        )
        assert capturado["shell"] is False
        assert capturado["argv"][1:3] == ["-m", "demo.executor_sintetico"]

    def test_comando_arbitrario_nao_e_executado(self, monkeypatch):
        executou = {"valor": False}

        def _bloqueado(argv, *, cwd, env):
            executou["valor"] = True
            executou["argv"] = list(argv)
            # Nao executa o argv recebido: comprova que a API nao aceita
            # substituicao; o caminho produtivo monta o argv autorizado.
            assert argv[0] == sys.executable
            assert argv[1:3] == ["-m", "demo.executor_sintetico"]
            raise RuntimeError("nao executar processo real neste teste")

        monkeypatch.setattr(execucao_focal, "_invocar_subprocesso", _bloqueado)
        with pytest.raises(RuntimeError, match="nao executar"):
            execucao_focal.executar_protocolo_focal(
                ENTRADA_SUCESSO, BASELINE, dry_run=True
            )
        assert executou["valor"] is True
        assert executou["argv"][1:3] == ["-m", "demo.executor_sintetico"]


# ---------------------------------------------------------------------------
# Integracao via protocolo focal
# ---------------------------------------------------------------------------


class TestProtocoloIntegracao:
    def test_dry_run_nao_altera_copia(self):
        antes = _baseline_texto()
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")
            visto["dir"] = ctx["diretorio"]

        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] == 0
        assert r["classificacao"] == "sucesso"
        assert r["stdout"] == ""
        assert r["stderr"] == ""
        doc = json.loads(r["resultado_bruto"])
        assert _campo_resumo(doc, "modo") == "dry_run"
        assert _campo_resumo(doc, "status") == "sucesso"
        assert _campo_item(doc, "item_01", "resultado") == "processado"
        assert _campo_item(doc, "item_01", "aplicado") is False
        assert _campo_item(doc, "item_01", "processado_depois") is True
        assert json.loads(visto["fx"]) == json.loads(antes)
        assert not Path(visto["dir"]).exists()
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_execucao_real_altera_somente_copia(self):
        antes = _baseline_texto()
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")
            visto["dir"] = ctx["diretorio"]

        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=False, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] == 0
        assert r["classificacao"] == "sucesso"
        assert r["stdout"] == ""
        assert r["stderr"] == ""
        doc = json.loads(r["resultado_bruto"])
        assert _campo_resumo(doc, "modo") == "executar"
        assert _campo_resumo(doc, "status") == "sucesso"
        assert _ids_itens(doc) == ["item_01", "item_03"]
        assert _campo_item(doc, "item_01", "resultado") == "processado"
        assert _campo_item(doc, "item_01", "aplicado") is True
        assert _campo_item(doc, "item_03", "resultado") == "ignorado"
        fx = json.loads(visto["fx"])
        mapa = {i["id"]: i["processado"] for i in fx["itens"]}
        assert mapa["item_01"] is True
        assert mapa["item_03"] is True
        assert BASELINE.read_text(encoding="utf-8") == antes
        assert not Path(visto["dir"]).exists()

    def test_parcial_codigo_0(self):
        antes = _baseline_texto()
        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_PARCIAL, BASELINE, dry_run=False
        )
        assert r["codigo_saida"] == 0
        assert r["classificacao"] == "sucesso"
        doc = json.loads(r["resultado_bruto"])
        assert _campo_resumo(doc, "status") == "parcial"
        assert _ids_itens(doc) == ["item_01", "item_inexistente"]
        assert _campo_item(doc, "item_inexistente", "resultado") == "nao_encontrado"
        assert _campo_item(doc, "item_inexistente", "processado_antes") is None
        assert _campo_item(doc, "item_inexistente", "processado_depois") is None
        assert _campo_item(doc, "item_inexistente", "diagnostico")
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_sucesso_com_aviso(self):
        antes = _baseline_texto()
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")

        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_AVISO, BASELINE, dry_run=False, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] == 0
        assert r["classificacao"] == "sucesso"
        assert r["stdout"] == ""
        assert r["stderr"] == ex.AVISO_TODOS_PROCESSADOS
        doc = json.loads(r["resultado_bruto"])
        assert _campo_resumo(doc, "status") == "sucesso"
        assert _campo_item(doc, "item_03", "resultado") == "ignorado"
        assert json.loads(visto["fx"]) == json.loads(antes)
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_sucesso_misto_sem_aviso(self):
        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=False
        )
        assert r["codigo_saida"] == 0
        assert r["stdout"] == ""
        assert r["stderr"] == ""

    def test_stdout_nao_e_fonte_do_resultado(self, monkeypatch):
        capturado = {}

        def _fake(argv, *, cwd, env):
            capturado["argv"] = list(argv)
            assert argv[0] == sys.executable
            assert argv[1:3] == ["-m", "demo.executor_sintetico"]
            i = argv.index("--resultado")
            Path(argv[i + 1]).write_text(_bruto_valido(), encoding="utf-8")
            return subprocess.CompletedProcess(
                args=argv,
                returncode=0,
                stdout='{"tipo":"falso_via_stdout"}\n',
                stderr="",
            )

        monkeypatch.setattr(execucao_focal, "_invocar_subprocesso", _fake)
        r = execucao_focal.executar_protocolo_focal(ENTRADA_SUCESSO, BASELINE)
        assert '{"tipo":"falso_via_stdout"}' in r["stdout"].replace(" ", "")
        assert r["resultado_bruto"] is not None
        doc = json.loads(r["resultado_bruto"])
        assert doc["tipo"] == "multinivel"
        assert "falso_via_stdout" not in r["resultado_bruto"]
        assert r["classificacao"] == "sucesso"

    def test_falha_operacional(self):
        antes = _baseline_texto()
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")
            visto["dir"] = ctx["diretorio"]

        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_FALHA, BASELINE, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] != 0
        assert r["classificacao"] == "falha"
        assert r["stderr"] == ex.STDERR_FALHA_OPERACIONAL
        assert json.loads(visto["fx"]) == json.loads(antes)
        assert not Path(visto["dir"]).exists()
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_resultado_invalido_preservado_byte_a_byte(self):
        r = execucao_focal.executar_protocolo_focal(ENTRADA_INVALIDO, BASELINE)
        assert r["codigo_saida"] == 0
        assert r["classificacao"] == "falha"
        assert r["resultado_bruto"] == ex.TEXTO_RESULTADO_INVALIDO
        assert execucao_focal.resultado_semanticamente_valido(
            r["resultado_bruto"]
        ) is False

    def test_interrupcao(self):
        antes = _baseline_texto()
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")
            visto["dir"] = ctx["diretorio"]
            visto["bruto"] = ctx["resultado_bruto"]

        r = execucao_focal.executar_protocolo_focal(
            ENTRADA_INTERRUPCAO, BASELINE, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] == 130
        assert r["classificacao"] == "falha"
        doc = json.loads(visto["bruto"])
        assert _campo_resumo(doc, "status") == "interrompido"
        assert execucao_focal.resultado_semanticamente_valido(visto["bruto"])
        assert _campo_item(doc, "item_01", "resultado") == "processado"
        fx = json.loads(visto["fx"])
        assert {i["id"]: i["processado"] for i in fx["itens"]}["item_01"] is True
        assert not Path(visto["dir"]).exists()
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_entrada_invalida_sem_alteracao_e_limpeza(self, tmp_path):
        antes = _baseline_texto()
        entrada = tmp_path / "inv.json"
        entrada.write_text(
            json.dumps({"schema": "selecao_execucao.v1", "ids": []}),
            encoding="utf-8",
        )
        visto = {}

        def _insp(ctx):
            visto["fx"] = Path(ctx["fixture_trabalho"]).read_text(encoding="utf-8")
            visto["dir"] = ctx["diretorio"]

        r = execucao_focal.executar_protocolo_focal(
            entrada, BASELINE, antes_da_limpeza=_insp
        )
        assert r["codigo_saida"] != 0
        assert r["entrada_valida"] is False
        assert r["invocou"] is False
        assert json.loads(visto["fx"]) == json.loads(antes)
        assert not Path(visto["dir"]).exists()
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_diretorios_distintos_por_invocacao(self):
        dirs = []

        def _insp(ctx):
            dirs.append(ctx["diretorio"])

        execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True, antes_da_limpeza=_insp
        )
        execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True, antes_da_limpeza=_insp
        )
        assert dirs[0] != dirs[1]
        assert not Path(dirs[0]).exists()
        assert not Path(dirs[1]).exists()

    def test_nomes_internos_fixos(self):
        nomes = {}

        def _insp(ctx):
            nomes["entrada"] = Path(ctx["entrada"]).name
            nomes["resultado"] = Path(ctx["resultado"]).name
            nomes["fixture"] = Path(ctx["fixture_trabalho"]).name
            assert Path(ctx["resultado"]).is_file()
            assert Path(ctx["fixture_trabalho"]).is_file()

        execucao_focal.executar_protocolo_focal(
            ENTRADA_SUCESSO, BASELINE, dry_run=True, antes_da_limpeza=_insp
        )
        assert nomes == {
            "entrada": "entrada.json",
            "resultado": "resultado.json",
            "fixture": "fixture_trabalho.json",
        }

    def test_baseline_intacta_apos_suite_parcial(self):
        antes = _baseline_texto()
        for entrada, dry in [
            (ENTRADA_SUCESSO, True),
            (ENTRADA_SUCESSO, False),
            (ENTRADA_AVISO, False),
            (ENTRADA_PARCIAL, False),
            (ENTRADA_FALHA, False),
            (ENTRADA_INVALIDO, False),
            (ENTRADA_INTERRUPCAO, False),
        ]:
            execucao_focal.executar_protocolo_focal(entrada, BASELINE, dry_run=dry)
        assert BASELINE.read_text(encoding="utf-8") == antes

    def test_controles_ausentes_da_baseline(self):
        fx = json.loads(_baseline_texto())
        ids = {i["id"] for i in fx["itens"]}
        assert "__falha_operacional__" not in ids
        assert "__resultado_invalido__" not in ids
        assert "__interrupcao__" not in ids
