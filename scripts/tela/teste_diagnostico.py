"""Diagnostico integrado do ponto de entrada H-0004 (tela/diagnostico.py).

Executavel via:
    python tela/teste_diagnostico.py

Cobre os criterios de aceite testaveis do handoff H-0004, com as
verificacoes de formato atualizadas para o renderer visual H-0006
(tres caixas bordeadas de 42 chars por linha):
- gerar_diagnostico_tela() nao lanca excecao para o padrao "orquestrador";
- retorno e str;
- saida comeca com "╭ ORQUESTRADOR";
- saida contem "│ Tela raiz do sistema", "╭ DASHBOARD",
  "Dashboard de teste", "Sem dados carregados", "╭ Menu",
  "[Esc] Sair", "[B] Borda", "╰" (borda inferior),
  "│" (borda lateral);
- saida e deterministica (duas chamadas identicas);
- saida bate com expected output literal do H-0006 (igualdade estrita);
- modo executavel `python tela/diagnostico.py` imprime a mesma string
  (verificado via subprocess.run com capture_output=True);
- campos inertes (origem_dados, bindings, filtros, tela_destino,
  regra_existencia) nao vazam na saida;
- gerar_diagnostico_tela("orquestrador") == gerar_diagnostico_tela();
- invariantes H-0001, H-0002 e H-0006 preservados (via subprocess.run,
  executados antes dos demais testes);
- proibicoes de importacao no modulo tela/diagnostico.py.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))

import subprocess  # noqa: E402

from tela.diagnostico import gerar_diagnostico_tela  # noqa: E402


_RESULTADOS = []


_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def teste_invariantes_anteriores():
    """Confirma via subprocess que H-0001, H-0002 e H-0006 ainda passam.

    Executado antes dos demais testes para garantir estado de partida
    limpo. Esse e o uso autorizado de subprocess para invocar os ciclos
    anteriores (o modo executavel de tela/diagnostico.py tambem e
    verificado por subprocess, conforme tabela de verificacoes do
    handoff H-0004). A linha do renderer foi atualizada para H-0006
    porque tela/teste_renderizador.py agora verifica o formato visual
    H-0006 com borda fixa.
    """
    print("")
    print("== Invariantes dos ciclos anteriores (subprocess) ==")
    todos_ok = True
    for rotulo, script in (
        ("H-0001", "tela/teste_loader.py"),
        ("H-0002", "tela/teste_modelo.py"),
        ("H-0006", "tela/teste_renderizador.py"),
    ):
        proc = subprocess.run(
            [sys.executable, script],
            cwd=str(_BASE_PADRAO),
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        _registrar(
            "invariantes {0} preservados ({1} retorna 0)".format(
                rotulo, script
            ),
            ok,
            "returncode={0}".format(proc.returncode),
        )
        if not ok:
            todos_ok = False
            sys.stderr.write(proc.stdout)
            sys.stderr.write(proc.stderr)
    return todos_ok


def teste_gerar_diagnostico():
    print("")
    print("== gerar_diagnostico_tela sobre orquestrador.json ==")

    try:
        resultado = gerar_diagnostico_tela()
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "gerar_diagnostico_tela() nao lanca excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("gerar_diagnostico_tela() nao lanca excecao", True)

    _registrar(
        "retorno e str",
        isinstance(resultado, str),
        "tipo={0}".format(type(resultado).__name__),
    )
    _registrar(
        "resultado comeca com '╭ ORQUESTRADOR'",
        resultado.startswith("╭ ORQUESTRADOR"),
    )
    _registrar(
        "resultado contem '╭ ORQUESTRADOR'",
        "╭ ORQUESTRADOR" in resultado,
    )
    _registrar(
        "resultado contem '│ Tela raiz do sistema'",
        "│ Tela raiz do sistema" in resultado,
    )
    _registrar(
        "resultado contem '╭ DASHBOARD'",
        "╭ DASHBOARD" in resultado,
    )
    _registrar(
        "resultado contem 'Dashboard de teste'",
        "Dashboard de teste" in resultado,
    )
    _registrar(
        "resultado contem 'Sem dados carregados'",
        "Sem dados carregados" in resultado,
    )
    _registrar(
        "resultado contem '╭ Menu'",
        "╭ Menu" in resultado,
    )
    _registrar(
        "resultado contem '[Esc] Sair'",
        "[Esc] Sair" in resultado,
    )
    _registrar(
        "resultado contem '[B] Borda'",
        "[B] Borda" in resultado,
    )
    _registrar(
        "resultado contem '╰' (borda inferior presente)",
        "╰" in resultado,
    )
    _registrar(
        "resultado contem '│' (borda lateral presente)",
        "│" in resultado,
    )

    resultado2 = gerar_diagnostico_tela()
    _registrar(
        "resultado e deterministico (duas chamadas identicas)",
        resultado == resultado2,
    )

    bate = resultado == _EXPECTED_ORQUESTRADOR
    _registrar(
        "resultado bate com saida esperada do H-0006 (igualdade estrita)",
        bate,
        "" if bate else "ver diff abaixo",
    )
    if not bate:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR))
        print("--- obtido (repr) ---")
        print(repr(resultado))

    inertes_ok = (
        "origem_dados" not in resultado
        and "bindings" not in resultado
        and "filtros" not in resultado
        and "tela_destino" not in resultado
        and "regra_existencia" not in resultado
    )
    _registrar(
        "campos inertes nao vazam na saida "
        "(origem_dados/bindings/filtros/tela_destino/regra_existencia)",
        inertes_ok,
    )

    explicito = gerar_diagnostico_tela("orquestrador")
    _registrar(
        "gerar_diagnostico_tela('orquestrador') == gerar_diagnostico_tela()",
        explicito == resultado,
    )

    return resultado


def teste_modo_executavel(resultado_esperado):
    print("")
    print("== Modo executavel: python tela/diagnostico.py ==")

    proc = subprocess.run(
        [sys.executable, "tela/diagnostico.py"],
        cwd=str(_BASE_PADRAO),
        capture_output=True,
        text=True,
    )
    _registrar(
        "modo executavel encerra com codigo de saida 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        return

    stdout_igual = proc.stdout == resultado_esperado
    _registrar(
        "'python tela/diagnostico.py' stdout == gerar_diagnostico_tela()",
        stdout_igual,
        "" if stdout_igual else "stdout diverge da string esperada",
    )
    if not stdout_igual:
        print("--- esperado (repr) ---")
        print(repr(resultado_esperado))
        print("--- stdout (repr) ---")
        print(repr(proc.stdout))


def teste_proibicoes_importacao():
    print("")
    print("== Proibicoes de import no modulo tela/diagnostico.py ==")

    caminho_mod = _BASE_PADRAO / "tela" / "diagnostico.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "diagnostico nao importa 'json'",
        "import json" not in texto_mod,
    )
    _registrar(
        "diagnostico nao importa 'os'",
        "import os" not in texto_mod,
    )
    _registrar(
        "diagnostico nao importa 'pathlib'",
        "import pathlib" not in texto_mod
        and "from pathlib" not in texto_mod,
    )
    _registrar(
        "diagnostico nao usa subprocess/exec/eval",
        "subprocess" not in texto_mod
        and "exec(" not in texto_mod
        and "eval(" not in texto_mod,
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
    print("Diagnostico H-0004 - ponto de entrada executavel da tela raiz")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    # Pre-condicao obrigatoria: invariantes dos ciclos anteriores devem
    # passar antes de qualquer teste sobre o diagnostico.
    teste_invariantes_anteriores()

    resultado = teste_gerar_diagnostico()

    if resultado is not None:
        teste_modo_executavel(resultado)

    teste_proibicoes_importacao()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
