"""Diagnostico integrado do ponto de entrada demo (H-0032).

Executavel via:
    python demo/teste_diagnostico.py

Cobre os criterios de aceite testaveis do handoff H-0032, com as
verificacoes de formato atualizadas para o renderer declarativo H-0010A
(caixas bordeadas derivadas do modelo/JSON, 42 chars por linha):
- gerar_diagnostico_tela() nao lanca excecao para o padrao "demo";
- retorno e str;
- saida comeca com "╭ ORQUESTRADOR";
- saida contem "│ Tela raiz do sistema", "╭ ITENS", "(console)",
  "╭ INFO", "╭ NAVEGAR", "[d] Destino", "╭ Menus", "[Esc] Sair",
  "╰" (borda inferior), "│" (borda lateral);
- saida NAO contem "[B] Borda" (nunca declarado no JSON);
- saida e deterministica (duas chamadas identicas);
- saida bate com expected output literal do H-0010A (igualdade estrita);
- modo executavel `python demo/diagnostico.py` imprime a mesma string
  (verificado via subprocess.run com capture_output=True);
- campos inertes (origem_dados, bindings, filtros, tela_destino,
  regra_existencia) nao vazam na saida;
- gerar_diagnostico_tela("demo") == gerar_diagnostico_tela();
- invariantes H-0001, H-0002 e H-0010A preservados (via subprocess.run,
  executados antes dos demais testes);
- proibicoes de importacao no modulo demo/diagnostico.py.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

import subprocess  # noqa: E402

from demo.diagnostico import gerar_diagnostico_tela  # noqa: E402
from tela.loader import carregar_estilo  # noqa: E402

# H-0039: estilo global resolvido, carregado uma vez para os testes que
# chamam renderizar_tela diretamente. O ponto de entrada real carrega da
# mesma forma em runtime.
_ESTILO = carregar_estilo()


_RESULTADOS = []


_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ ITENS ─────────────────────────────────╮\n"
    "│ (console)                              │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ INFO ──────────────────────────────────╮\n"
    "╰────────────────────────────────────────╯\n"
    "╭ NAVEGAR ───────────────────────────────╮\n"
    "│                                        │\n"
    "│    [d] Destino        [5] Matriz 2x4   │\n"
    "│    [g] Grupo Min.     [6] Nao Verboso  │\n"
    "│    [1] Console        [7] Verboso      │\n"
    "│    [2] Dashboard      [8] Alternavel   │\n"
    "│    [3] Matriz 2x2     [9] Tab Altern.  │\n"
    "│    [4] Matriz 3x2                      │\n"
    "│                                        │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menus ─────────────────────────────────╮\n"
    "│  [Esc] Sair  [?] Ajuda                 │\n"
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
    """Confirma via subprocess que H-0001, H-0002 e H-0010A ainda passam.

    Executado antes dos demais testes para garantir estado de partida
    limpo. Esse e o uso autorizado de subprocess para invocar os ciclos
    anteriores (o modo executavel de demo/diagnostico.py tambem e
    verificado por subprocess, conforme tabela de verificacoes do
    handoff H-0032). A linha do renderer foi atualizada para H-0006
    porque tela/teste_renderizador.py agora verifica o formato visual
    H-0006 com borda fixa.
    """
    print("")
    print("== Invariantes dos ciclos anteriores (subprocess) ==")
    todos_ok = True
    for rotulo, script in (
        ("H-0001", "tela/teste_loader.py"),
        ("H-0002", "tela/teste_modelo.py"),
        ("H-0010A", "tela/teste_renderizador.py"),
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


def teste_gerar_diagnostico():
    print("")
    print("== gerar_diagnostico_tela sobre demo.json ==")

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
        "resultado contem '╭ ITENS' (console_principal do JSON)",
        "╭ ITENS" in resultado,
    )
    _registrar(
        "resultado contem '(console)' (placeholder de escopo)",
        "(console)" in resultado,
    )
    _registrar(
        "resultado contem '╭ INFO' (dashboard_info do JSON)",
        "╭ INFO" in resultado,
    )
    _registrar(
        "resultado contem '╭ NAVEGAR' (lancador_principal do JSON)",
        "╭ NAVEGAR" in resultado,
    )
    _registrar(
        "resultado contem '[d] Destino' (item do lancador do JSON)",
        "[d] Destino" in resultado,
    )
    _registrar(
        "resultado contem '╭ Menus'",
        "╭ Menus" in resultado,
    )
    _registrar(
        "resultado contem '[Esc] Sair' (chip Esc declarado no JSON)",
        "[Esc] Sair" in resultado,
    )
    _registrar(
        "resultado NAO contem '[B] Borda' (nao declarado no JSON)",
        "[B] Borda" not in resultado,
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
        "resultado bate com saida esperada do H-0010A (igualdade estrita)",
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

    explicito = gerar_diagnostico_tela("demo")
    _registrar(
        "gerar_diagnostico_tela('demo') == gerar_diagnostico_tela()",
        explicito == resultado,
    )


def teste_modo_executavel():
    print("")
    print("== Modo executavel: python demo/diagnostico.py ==")

    proc = subprocess.run(
        [sys.executable, "demo/diagnostico.py"],
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

    # H-0038: resultado esperado calculado internamente pela propria funcao,
    # eliminando o parametro posicional que causava ERROR de setup no pytest
    # (fixture 'resultado_esperado' not found). O valor computado aqui e o
    # mesmo que `main()` repassava anteriormente a partir de
    # `teste_gerar_diagnostico()`.
    resultado_esperado = gerar_diagnostico_tela()
    stdout_igual = proc.stdout == resultado_esperado
    _registrar(
        "'python demo/diagnostico.py' stdout == gerar_diagnostico_tela()",
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
    print("== Proibicoes de import no modulo demo/diagnostico.py ==")

    caminho_mod = _BASE_PADRAO / "demo" / "diagnostico.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "diagnostico nao importa 'json'",
        "import json" not in texto_mod,
    )
    _registrar(
        "diagnostico importa 'os' (para _RAIZ_TELAS_DEMO)",
        "import os" in texto_mod,
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
    _registrar(
        "diagnostico define _RAIZ_TELAS_DEMO",
        "_RAIZ_TELAS_DEMO" in texto_mod,
    )
    _registrar(
        "diagnostico usa raiz demo na chamada carregar_tela",
        "_RAIZ_TELAS_DEMO" in texto_mod and "carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)" in texto_mod,
    )


def teste_telas_h0035_diagnostico():
    """Diagnostico das telas permanentes h0035_* (H-0035 / ADR-0025).

    Verifica que cada tela de conteudo carrega, constroi e renderiza pelo
    pipeline (carregar -> construir -> renderizar) via gerar_diagnostico_tela,
    com identidade material (o titulo do cabecalho aparece na saida). Verifica
    tambem que uma configuracao invalida e rejeitada por erro de dominio.
    """
    print("")
    print("== H-0035: diagnostico das telas permanentes ==")

    from tela.loader import carregar_tela, TelaEstruturaInvalida  # noqa: E402
    from tela.modelo import construir_modelo  # noqa: E402
    from tela.renderizador import renderizar_tela  # noqa: E402
    import os  # noqa: E402
    import tempfile  # noqa: E402
    import json  # noqa: E402

    raiz = os.path.join("config", "telas", "demo")

    # Telas de conteudo (nao o catalogo, que exige terminal maior para a fila).
    # Nota: gerar_diagnostico_tela usa largura padrao 42. Telas com DM que exigem
    # mais colunas (ex: h0035_matriz_fixa_cabe: 4 cols x min_w=13 = 57 min) sao
    # verificadas via pipeline direto com largura adequada.
    casos_largura_padrao = [
        ("h0035_pref_linhas", "H0035 PREF LINHAS"),
        ("h0035_pref_colunas", "H0035 PREF COLUNAS"),
        ("h0035_uma_linha", "H0035 UMA LINHA"),
        ("h0035_uma_coluna", "H0035 UMA COLUNA"),
        ("h0035_console_com", "H0035 CONSOLE COM"),
        ("h0035_lancador_com", "H0035 LANCADOR COM"),
        ("h0035_dashboard_com", "H0035 DASH COM"),
        ("h0035_dashboard_sem", "H0035 DASH SEM"),
        ("h0035_minimo_fixo_excedido", "H0035 MIN FIXO"),
    ]
    for id_tela, titulo_esperado in casos_largura_padrao:
        try:
            saida = gerar_diagnostico_tela(id_tela)
            ident = titulo_esperado in saida
            _registrar(
                "H0035 diagnostico {0} (identidade material)".format(id_tela),
                isinstance(saida, str) and ident,
                "titulo presente" if ident else "titulo ausente",
            )
        except Exception as exc:  # pragma: no cover
            _registrar(
                "H0035 diagnostico {0}".format(id_tela),
                False, "{0}: {1}".format(type(exc).__name__, exc),
            )

    # h0035_matriz_fixa_cabe: 4 colunas x min_w=13 = 57 chars minimos; requer
    # largura explicita (largura padrao 42 resulta em "terminal pequeno demais").
    try:
        tela_raw = carregar_tela(None, "h0035_matriz_fixa_cabe", raiz)
        modelo_mc = construir_modelo(tela_raw)
        saida_mc = renderizar_tela(modelo_mc, estilo=_ESTILO, largura=80, altura=30)
        ident_mc = "H0035 MATRIZ 3X4" in saida_mc
        _registrar(
            "H0035 diagnostico h0035_matriz_fixa_cabe (identidade material)",
            isinstance(saida_mc, str) and ident_mc,
            "titulo presente" if ident_mc else "titulo ausente",
        )
    except Exception as exc:  # pragma: no cover
        _registrar(
            "H0035 diagnostico h0035_matriz_fixa_cabe",
            False, "{0}: {1}".format(type(exc).__name__, exc),
        )

    # Configuracao invalida rejeitada por erro de dominio (sem estado externo).
    tmp = Path(tempfile.mkdtemp(prefix="diag_h0035_"))
    try:
        dir_telas = tmp / "config" / "telas" / "demo"
        dir_telas.mkdir(parents=True, exist_ok=True)
        tela_inv = {
            "schema": "tela.v1", "id": "h0035_invalida",
            "cabecalho": {"titulo": "T", "descricao": "D"},
            "corpo": {"arranjo": "vertical", "distribuicao": {"modo": "igual"},
                      "elementos": [{
                          "id": "d", "tipo": "dashboard", "titulo": "G",
                          "campos": [],
                          "distribuicao_matricial": {"ordem": "diagonal"}}]},
            "barra_de_menus": {"chips": []},
        }
        (dir_telas / "h0035_invalida.json").write_text(
            json.dumps(tela_inv, ensure_ascii=False), encoding="utf-8")
        try:
            carregar_tela(tmp, "h0035_invalida", raiz)
            _registrar("H0035 diagnostico config invalida rejeitada", False,
                       "nenhuma excecao")
        except TelaEstruturaInvalida:
            _registrar("H0035 diagnostico config invalida rejeitada", True)
        except Exception as exc:  # pragma: no cover
            _registrar("H0035 diagnostico config invalida rejeitada", False,
                       "excecao errada: {0}".format(type(exc).__name__))
    finally:
        import shutil  # noqa: E402
        try:
            shutil.rmtree(tmp)
        except OSError:
            pass


def teste_pipeline_h0036():
    """Pipeline integrado H-0036: carregar tela + carregar externo + render.

    Cobre §19.4 do handoff: para cada cenario H-0036 e para os consoles h0035
    adaptados, o demo.py carrega os dois documentos separadamente pelo catalogo
    e o renderizador exibe o conteudo (sem placeholder). Cenario sem conteudo
    preserva o placeholder.
    """
    print("")
    print("== H-0036: pipeline integrado (demo.py + externo) ==")

    from demo.demo import _carregar_modelo_por_id, id_conteudo_externo_de  # noqa: E402
    from tela.renderizador import renderizar_tela  # noqa: E402

    casos = [
        ("h0036_console_hierarquia", "H0036 HIERARQUIA", "H-0036"),
        ("h0036_console_tabela", "H0036 TABELA", "tabela H-0036"),
        ("h0036_console_conjuntos", "H0036 CONJUNTOS", "H-0036"),
        ("h0035_console_com", "H0035 CONSOLE COM", "P01 linha"),
        ("h0035_console_sem", "H0035 CONSOLE SEM", "Linha alfa"),
    ]
    for id_tela, titulo, marca in casos:
        try:
            modelo = _carregar_modelo_por_id(id_tela)
            saida = renderizar_tela(modelo, estilo=_ESTILO, largura=70, altura=28)
            ok = (
                titulo in saida
                and marca in saida
                and "(console)" not in saida
                and modelo.conteudo_externo is not None
            )
            _registrar(
                "pipeline {0}: tela+externo renderizados sem placeholder".format(id_tela),
                ok,
                "titulo={0} marca={1} placeholder_ausente={2}".format(
                    titulo in saida, marca in saida, "(console)" not in saida
                ),
            )
        except Exception as exc:  # pragma: no cover
            _registrar("pipeline {0}".format(id_tela), False,
                       "{0}: {1}".format(type(exc).__name__, exc))

    # Cenario sem conteudo externo: catalogo nao associa; placeholder presente.
    _registrar("catalogo: cenario 'demo' sem conteudo externo (ausencia explicita)",
               id_conteudo_externo_de("demo") is None)
    try:
        modelo_sem = _carregar_modelo_por_id("h0030_console_unico")
        saida_sem = renderizar_tela(modelo_sem, estilo=_ESTILO, largura=60, altura=20)
        _registrar(
            "pipeline sem conteudo: placeholder '(console)' presente; sem externo",
            "(console)" in saida_sem and modelo_sem.conteudo_externo is None,
        )
    except Exception as exc:  # pragma: no cover
        _registrar("pipeline sem conteudo", False,
                   "{0}: {1}".format(type(exc).__name__, exc))


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
    print("Diagnostico H-0032 - ponto de entrada executavel da tela demo")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    # Pre-condicao obrigatoria: invariantes dos ciclos anteriores devem
    # passar antes de qualquer teste sobre o diagnostico.
    teste_invariantes_anteriores()

    teste_gerar_diagnostico()

    # H-0038: teste_modo_executavel() agora computa internamente o resultado
    # esperado via gerar_diagnostico_tela(); main() nao repassa mais retorno.
    teste_modo_executavel()

    teste_proibicoes_importacao()

    teste_telas_h0035_diagnostico()

    teste_pipeline_h0036()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
