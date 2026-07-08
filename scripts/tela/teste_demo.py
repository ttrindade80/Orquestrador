"""Diagnostico da aplicacao demonstravel H-0008 (tela/demo.py).

Executavel via:
    python tela/teste_demo.py

Cobre os criterios de aceite testaveis do handoff H-0008:

Secao 1 - Estado inicial:
- criar_estado_inicial() retorna dict;
- estado inicial tem tipo_borda == "curva";
- estado inicial tem saindo == False;
- duas chamadas retornam dicts independentes.

Secao 2 - processar_comando:
- "b" sobre curva -> reta;
- "b" sobre reta -> curva;
- "b" nao altera saindo;
- "s" define saindo == True;
- "s" nao altera tipo_borda;
- "s" sobre reta preserva tipo_borda == "reta";
- comando desconhecido "x" nao altera tipo_borda nem saindo;
- string vazia nao altera estado;
- "B" (maiusculo) nao tem efeito (case-sensitive);
- "S" (maiusculo) nao altera saindo (case-sensitive);
- processar_comando nao modifica o dict original com "b";
- processar_comando nao modifica o dict original com "s";
- alternancia completa curva -> reta -> curva.

Secao 3 - renderizar_estado:
- renderizar_estado com tipo_borda="curva" retorna str;
- saida curva comeca com "╭ ORQUESTRADOR";
- saida curva bate com _EXPECTED_CURVA (igualdade estrita);
- renderizar_estado com tipo_borda="reta" retorna str;
- saida reta comeca com "┌ ORQUESTRADOR";
- saida reta bate com _EXPECTED_RETA (igualdade estrita);
- renderizar_estado nao altera estado;
- renderizar_estado nao altera modelo.

Secao 4 - Integracao via subprocess (demo completo):
- python tela/demo.py com input "b\ns\n" encerra com codigo 0;
- stdout contem render curva inicial;
- stdout contem render reta apos "b";
- stdout bate com _EXPECTED_CURVA + _EXPECTED_RETA;
- stderr vazio;
- config/telas/orquestrador.json inalterado apos demo.

Secao 5 - Preservacao do diagnostico:
- gerar_diagnostico_tela() nao lanca excecao;
- retorno de gerar_diagnostico_tela() e str;
- retorno bate com _EXPECTED_CURVA (default curva H-0006/H-0007);
- python tela/diagnostico.py encerra com codigo 0;
- stdout de diagnostico.py bate com _EXPECTED_CURVA;
- diagnostico.py nao contem sys.stdin;
- diagnostico.py nao contem input(.

Alem disso, verifica proibicoes de importacao em tela/demo.py e o
comportamento de EOF sem "s" (encerra com codigo 0).

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))

import subprocess  # noqa: E402

from tela.loader import carregar_tela  # noqa: E402
from tela.modelo import construir_modelo, ModeloTela  # noqa: E402
from tela.renderizador import renderizar_tela  # noqa: E402
from tela.demo import (  # noqa: E402
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
)
from tela.diagnostico import gerar_diagnostico_tela  # noqa: E402


_RESULTADOS = []


_EXPECTED_CURVA = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)

_EXPECTED_RETA = (
    "┌ ORQUESTRADOR ──────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "└────────────────────────────────────────┘\n"
    "\n"
    "┌ DASHBOARD ─────────────────────────────┐\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "└────────────────────────────────────────┘\n"
    "\n"
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _carregar_modelo():
    tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
    return construir_modelo(tela_raw)


def teste_estado_inicial():
    print("")
    print("== Secao 1 - Estado inicial ==")

    est = criar_estado_inicial()
    _registrar(
        "criar_estado_inicial() retorna dict",
        isinstance(est, dict),
        "tipo={0}".format(type(est).__name__),
    )
    _registrar(
        "estado inicial tem tipo_borda == 'curva'",
        est.get("tipo_borda") == "curva",
        "tipo_borda={0!r}".format(est.get("tipo_borda")),
    )
    _registrar(
        "estado inicial tem saindo == False",
        est.get("saindo") is False,
        "saindo={0!r}".format(est.get("saindo")),
    )
    _registrar(
        "duas chamadas retornam dicts independentes",
        criar_estado_inicial() is not criar_estado_inicial(),
    )


def teste_processar_comando():
    print("")
    print("== Secao 2 - processar_comando ==")

    base = {"tipo_borda": "curva", "saindo": False}

    _registrar(
        "'b' sobre curva -> tipo_borda == 'reta'",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "b")["tipo_borda"] == "reta",
    )
    _registrar(
        "'b' sobre reta -> tipo_borda == 'curva'",
        processar_comando({"tipo_borda": "reta", "saindo": False}, "b")["tipo_borda"] == "curva",
    )
    _registrar(
        "'b' nao altera saindo",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "b")["saindo"] is False,
    )
    _registrar(
        "'s' define saindo == True",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "s")["saindo"] is True,
    )
    _registrar(
        "'s' nao altera tipo_borda (curva preservado)",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "s")["tipo_borda"] == "curva",
    )
    _registrar(
        "'s' sobre reta preserva tipo_borda == 'reta'",
        processar_comando({"tipo_borda": "reta", "saindo": False}, "s")["tipo_borda"] == "reta",
    )

    res_x = processar_comando({"tipo_borda": "curva", "saindo": False}, "x")
    _registrar(
        "comando desconhecido 'x' nao altera tipo_borda",
        res_x["tipo_borda"] == "curva",
    )
    _registrar(
        "comando desconhecido 'x' nao altera saindo",
        res_x["saindo"] is False,
    )

    res_vazio = processar_comando({"tipo_borda": "reta", "saindo": True}, "")
    _registrar(
        "string vazia nao altera estado (tipo_borda preservado)",
        res_vazio["tipo_borda"] == "reta",
    )
    _registrar(
        "string vazia nao altera estado (saindo preservado)",
        res_vazio["saindo"] is True,
    )

    _registrar(
        "'B' (maiusculo) nao tem efeito sobre tipo_borda",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "B")["tipo_borda"] == "curva",
    )
    _registrar(
        "'S' (maiusculo) nao altera saindo",
        processar_comando({"tipo_borda": "curva", "saindo": False}, "S")["saindo"] is False,
    )

    estado_original = {"tipo_borda": "curva", "saindo": False}
    processar_comando(estado_original, "b")
    _registrar(
        "processar_comando nao modifica o dict original com 'b'",
        estado_original["tipo_borda"] == "curva" and estado_original["saindo"] is False,
        "estado apos chamada={0!r}".format(estado_original),
    )

    estado_original_s = {"tipo_borda": "curva", "saindo": False}
    processar_comando(estado_original_s, "s")
    _registrar(
        "processar_comando nao modifica o dict original com 's'",
        estado_original_s["tipo_borda"] == "curva" and estado_original_s["saindo"] is False,
        "estado apos chamada={0!r}".format(estado_original_s),
    )

    e1 = processar_comando(base, "b")
    e2 = processar_comando(e1, "b")
    _registrar(
        "alternancia completa: curva -> reta -> curva",
        e2["tipo_borda"] == "curva",
        "tipo_borda final={0!r}".format(e2["tipo_borda"]),
    )


def teste_renderizar_estado(modelo):
    print("")
    print("== Secao 3 - renderizar_estado ==")

    estado_curva = {"tipo_borda": "curva", "saindo": False}
    estado_reta = {"tipo_borda": "reta", "saindo": False}

    res_curva = renderizar_estado(estado_curva, modelo)
    _registrar(
        "renderizar_estado com tipo_borda='curva' retorna str",
        isinstance(res_curva, str),
        "tipo={0}".format(type(res_curva).__name__),
    )
    _registrar(
        "saida curva comeca com '╭ ORQUESTRADOR'",
        res_curva.startswith("╭ ORQUESTRADOR"),
    )
    bate_curva = res_curva == _EXPECTED_CURVA
    _registrar(
        "saida curva bate com _EXPECTED_CURVA (igualdade estrita)",
        bate_curva,
        "" if bate_curva else "ver diff abaixo",
    )
    if not bate_curva:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_CURVA))
        print("--- obtido (repr) ---")
        print(repr(res_curva))

    _registrar(
        "renderizar_estado(estado_curva, modelo) == renderizar_tela(modelo, 'curva')",
        res_curva == renderizar_tela(modelo, "curva"),
    )

    res_reta = renderizar_estado(estado_reta, modelo)
    _registrar(
        "renderizar_estado com tipo_borda='reta' retorna str",
        isinstance(res_reta, str),
        "tipo={0}".format(type(res_reta).__name__),
    )
    _registrar(
        "saida reta comeca com '┌ ORQUESTRADOR'",
        res_reta.startswith("┌ ORQUESTRADOR"),
    )
    bate_reta = res_reta == _EXPECTED_RETA
    _registrar(
        "saida reta bate com _EXPECTED_RETA (igualdade estrita)",
        bate_reta,
        "" if bate_reta else "ver diff abaixo",
    )
    if not bate_reta:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_RETA))
        print("--- obtido (repr) ---")
        print(repr(res_reta))

    _registrar(
        "renderizar_estado(estado_reta, modelo) == renderizar_tela(modelo, 'reta')",
        res_reta == renderizar_tela(modelo, "reta"),
    )

    estado_snapshot = {"tipo_borda": "curva", "saindo": False}
    renderizar_estado(estado_snapshot, modelo)
    _registrar(
        "renderizar_estado nao altera estado",
        estado_snapshot == {"tipo_borda": "curva", "saindo": False},
    )

    cabecalho_antes = dict(modelo.cabecalho)
    renderizar_estado({"tipo_borda": "reta", "saindo": False}, modelo)
    _registrar(
        "renderizar_estado nao altera modelo.cabecalho",
        modelo.cabecalho == cabecalho_antes,
    )


def teste_integracao_subprocess():
    print("")
    print("== Secao 4 - Integracao via subprocess (demo completo) ==")

    caminho_json = _BASE_PADRAO / "config" / "telas" / "orquestrador.json"
    json_antes = caminho_json.read_text(encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
    )

    _registrar(
        "python tela/demo.py com 'b\\ns\\n' encerra com codigo 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)

    _registrar(
        "stdout contem render curva inicial ('╭ ORQUESTRADOR')",
        "╭ ORQUESTRADOR" in proc.stdout,
    )
    _registrar(
        "stdout contem render reta apos 'b' ('┌ ORQUESTRADOR')",
        "┌ ORQUESTRADOR" in proc.stdout,
    )

    saida_esperada = _EXPECTED_CURVA + _EXPECTED_RETA
    bate = proc.stdout == saida_esperada
    _registrar(
        "stdout bate com _EXPECTED_CURVA + _EXPECTED_RETA",
        bate,
        "" if bate else "ver diff abaixo",
    )
    if not bate:
        print("--- esperado (repr) ---")
        print(repr(saida_esperada))
        print("--- stdout (repr) ---")
        print(repr(proc.stdout))

    _registrar(
        "stderr esta vazio",
        proc.stderr == "",
        "stderr={0!r}".format(proc.stderr),
    )

    json_depois = caminho_json.read_text(encoding="utf-8")
    _registrar(
        "config/telas/orquestrador.json inalterado apos demo",
        json_antes == json_depois,
    )


def teste_eof_sem_s():
    print("")
    print("== EOF sem 's' (encerra com codigo 0) ==")

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="",
        capture_output=True,
        text=True,
    )
    _registrar(
        "printf '' | python tela/demo.py encerra com codigo 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    _registrar(
        "stdout com EOF sem 's' contem apenas render curva inicial",
        proc.stdout == _EXPECTED_CURVA,
        "" if proc.stdout == _EXPECTED_CURVA else "stdout diverge",
    )


def teste_preservacao_diagnostico():
    print("")
    print("== Secao 5 - Preservacao do diagnostico ==")

    try:
        resultado = gerar_diagnostico_tela()
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "gerar_diagnostico_tela() nao lanca excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar("gerar_diagnostico_tela() nao lanca excecao", True)

    _registrar(
        "retorno de gerar_diagnostico_tela() e str",
        isinstance(resultado, str),
        "tipo={0}".format(type(resultado).__name__),
    )

    _registrar(
        "gerar_diagnostico_tela() bate com _EXPECTED_CURVA (default curva)",
        resultado == _EXPECTED_CURVA,
    )

    proc = subprocess.run(
        [sys.executable, "tela/diagnostico.py"],
        cwd=str(_BASE_PADRAO),
        capture_output=True,
        text=True,
    )
    _registrar(
        "python tela/diagnostico.py encerra com codigo 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    _registrar(
        "stdout de diagnostico.py bate com _EXPECTED_CURVA",
        proc.stdout == _EXPECTED_CURVA,
    )

    caminho_mod = _BASE_PADRAO / "tela" / "diagnostico.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")
    _registrar(
        "diagnostico.py nao contem 'sys.stdin'",
        "sys.stdin" not in texto_mod,
    )
    _registrar(
        "diagnostico.py nao contem 'input('",
        "input(" not in texto_mod,
    )


def teste_proibicoes_importacao_demo():
    print("")
    print("== Proibicoes de import no modulo tela/demo.py ==")

    caminho_mod = _BASE_PADRAO / "tela" / "demo.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "demo.py nao importa 'json'",
        "import json" not in texto_mod,
    )
    _registrar(
        "demo.py nao importa 'os'",
        "import os" not in texto_mod,
    )
    _registrar(
        "demo.py nao importa 'pathlib'",
        "import pathlib" not in texto_mod and "from pathlib" not in texto_mod,
    )
    _registrar(
        "demo.py nao importa bibliotecas de UI (curses/textual/rich)",
        "import curses" not in texto_mod
        and "from curses" not in texto_mod
        and "import textual" not in texto_mod
        and "from textual" not in texto_mod
        and "import rich" not in texto_mod
        and "from rich" not in texto_mod,
    )
    _registrar(
        "demo.py nao usa subprocess/exec/eval",
        "subprocess" not in texto_mod and "exec(" not in texto_mod and "eval(" not in texto_mod,
    )


def _finalizar():
    print("")
    print("== Resumo ==")
    total = len(_RESULTADOS)
    passaram = sum(1 for _, ok in _RESULTADOS if ok)
    falharam = total - passaram
    print("Total de verificacoes: {0}".format(total))
    print("Passaram: {0}".format(passaram))
    print("Falharam: {0}".format(falharam))
    if falharam:
        print("")
        print("Verificacoes falhadas:")
        for nome, ok in _RESULTADOS:
            if not ok:
                print("  - {0}".format(nome))
    return 0 if falharam == 0 else 1


def main():
    print("Diagnostico H-0008 - aplicacao demonstravel minima com borda/sair")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_estado_inicial()
    teste_processar_comando()

    modelo = _carregar_modelo()
    teste_renderizar_estado(modelo)

    teste_integracao_subprocess()
    teste_eof_sem_s()
    teste_preservacao_diagnostico()
    teste_proibicoes_importacao_demo()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
