"""Diagnostico do renderer visual com borda fixa (H-0006).

Executavel via:
    python tela/teste_renderizador.py

Cobre os criterios de aceite testaveis do handoff H-0006:
- renderizar_tela aceita ModeloTela valido sem excecao;
- saida e str;
- saida comeca com "╭ ORQUESTRADOR";
- saida contem "│ Tela raiz do sistema";
- saida contem "╭ DASHBOARD", "Dashboard de teste",
  "Sem dados carregados";
- saida contem "╭ Menu", "[Esc] Sair", "[B] Borda";
- saida contem "╰" (borda inferior);
- saida e deterministica (duas chamadas com mesmo modelo sao identicas);
- saida bate com expected output literal do handoff H-0006 (igualdade
  estrita, incluindo o \\n final);
- cada linha da saida tem exatamente 42 chars Python (sem o \\n);
- modelo fabricado com titulo="Fab" produz saida usando dados do
  modelo, nao do JSON em disco (label "FAB", conteudo "desc fab",
  caixas hardcoded DASHBOARD e Menu presentes);
- renderizar_tela(None) e renderizar_tela(<dict>) lancam RenderizadorErro;
- renderer nao importa json/os/pathlib nem chama carregar_tela;
- renderer nao acessa _campos_inertes dos elementos;
- renderer nao executa acao, binding, filtro ou navegacao;
- saida nao vaza campos inertes (origem_dados/bindings/filtros/
  tela_destino/regra_existencia) nem ids internos de chip.

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))

from tela.loader import carregar_tela  # noqa: E402
from tela.modelo import (  # noqa: E402
    Corpo,
    ElementoCorpo,
    ModeloTela,
    construir_modelo,
)
from tela.renderizador import RenderizadorErro, renderizar_tela  # noqa: E402


_RESULTADOS = []


_EXPECTED_ORQUESTRADOR = (
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


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _espera_excecao(nome, fn, tipo_esperado):
    try:
        fn()
    except tipo_esperado as exc:
        _registrar(nome, True, "{0}: {1}".format(type(exc).__name__, exc))
        return exc
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            nome,
            False,
            "esperava {0}; obteve {1}: {2}".format(
                tipo_esperado.__name__, type(exc).__name__, exc
            ),
        )
        return None
    _registrar(
        nome,
        False,
        "esperava {0}; nenhuma excecao lancada".format(
            tipo_esperado.__name__
        ),
    )
    return None


def teste_renderizador_orquestrador():
    print("")
    print("== Renderer sobre modelo de config/telas/orquestrador.json ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None

    try:
        saida = renderizar_tela(modelo)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela aceita ModeloTela valido sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("renderizar_tela aceita ModeloTela valido sem excecao", True)

    _registrar(
        "saida e str",
        isinstance(saida, str),
        "tipo={0}".format(type(saida).__name__),
    )
    _registrar(
        "saida comeca com '╭ ORQUESTRADOR'",
        saida.startswith("╭ ORQUESTRADOR"),
    )
    _registrar(
        "saida contem '│ Tela raiz do sistema'",
        "│ Tela raiz do sistema" in saida,
    )
    _registrar(
        "saida contem '╭ DASHBOARD'",
        "╭ DASHBOARD" in saida,
    )
    _registrar(
        "saida contem 'Dashboard de teste'",
        "Dashboard de teste" in saida,
    )
    _registrar(
        "saida contem 'Sem dados carregados'",
        "Sem dados carregados" in saida,
    )
    _registrar(
        "saida contem '╭ Menu'",
        "╭ Menu" in saida,
    )
    _registrar(
        "saida contem '[Esc] Sair'",
        "[Esc] Sair" in saida,
    )
    _registrar(
        "saida contem '[B] Borda'",
        "[B] Borda" in saida,
    )
    _registrar(
        "saida contem '╰' (borda inferior)",
        "╰" in saida,
    )

    saida2 = renderizar_tela(modelo)
    _registrar(
        "saida e deterministica (duas chamadas identicas)",
        saida == saida2,
    )

    larguras_ok = all(
        (len(ln) == 42 for ln in saida.split("\n") if ln != "")
    )
    _registrar(
        "cada linha da saida tem exatamente 42 chars Python",
        larguras_ok,
    )

    bate = saida == _EXPECTED_ORQUESTRADOR
    _registrar(
        "saida bate com expected output literal do handoff H-0006",
        bate,
        "" if bate else "ver diff abaixo",
    )
    if not bate:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR))
        print("--- obtido (repr) ---")
        print(repr(saida))

    return modelo


def teste_modelo_fabricado():
    print("")
    print("== Modelo fabricado: renderer usa dados do modelo, nao do JSON ==")

    modelo_fab = ModeloTela(
        id="teste_fabricado",
        schema="tela.v0",
        cabecalho={"titulo": "Fab", "descricao": "desc fab"},
        corpo=Corpo(
            arranjo="linear",
            elementos=[ElementoCorpo(id="e1", tipo="console")],
        ),
        barra_de_menus={"chips": [{"id": "c1", "texto": "Ok"}]},
        _raw={},
    )

    saida_fab = renderizar_tela(modelo_fab)

    _registrar(
        "saida fabricada comeca com '╭ FAB'",
        saida_fab.startswith("╭ FAB"),
        "prefixo={0!r}".format(saida_fab[:40]),
    )
    _registrar(
        "saida fabricada contem 'desc fab'",
        "desc fab" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '╭ DASHBOARD' (hardcoded)",
        "╭ DASHBOARD" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '[Esc] Sair' (hardcoded)",
        "[Esc] Sair" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '[B] Borda' (hardcoded)",
        "[B] Borda" in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona 'orquestrador'",
        "orquestrador" not in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona 'ORQUESTRADOR'",
        "ORQUESTRADOR" not in saida_fab,
    )


def teste_erros_renderizador():
    print("")
    print("== Casos de erro do renderer ==")

    _espera_excecao(
        "renderizar_tela(None) lanca RenderizadorErro",
        lambda: renderizar_tela(None),
        RenderizadorErro,
    )
    _espera_excecao(
        "renderizar_tela(<dict>) lanca RenderizadorErro",
        lambda: renderizar_tela({"id": "x"}),
        RenderizadorErro,
    )


def teste_proibicoes_importacao():
    print("")
    print("== Proibicoes de import/leitura no modulo do renderer ==")

    caminho_mod = _BASE_PADRAO / "tela" / "renderizador.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "renderer nao importa 'json'",
        "import json" not in texto_mod,
    )
    _registrar(
        "renderer nao importa 'os'",
        "import os" not in texto_mod,
    )
    _registrar(
        "renderer nao importa 'pathlib'",
        "import pathlib" not in texto_mod and "from pathlib" not in texto_mod,
    )
    _registrar(
        "renderer nao importa tela.loader (nao chama carregar_tela)",
        "from tela.loader" not in texto_mod and "import tela.loader" not in texto_mod,
    )
    _registrar(
        "renderer nao abre nem le arquivos (open/read_text/read_bytes)",
        "open(" not in texto_mod
        and ".read_text(" not in texto_mod
        and ".read_bytes(" not in texto_mod,
    )
    _registrar(
        "renderer nao usa subprocess/exec/eval",
        "subprocess" not in texto_mod
        and "exec(" not in texto_mod
        and "eval(" not in texto_mod,
    )
    _registrar(
        "renderer nao acessa _campos_inertes dos elementos",
        "_campos_inertes" not in texto_mod,
    )


def teste_inercia():
    print("")
    print("== Inercia: renderer nao executa/resolve/ativa ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
    modelo = construir_modelo(tela_raw)
    raw_antes = dict(modelo._raw)
    cabecalho_antes = dict(modelo.cabecalho)
    elementos_antes = [(e.id, e.tipo) for e in modelo.corpo.elementos]
    chips_antes = list(modelo.barra_de_menus.get("chips", []))

    saida = renderizar_tela(modelo)

    _registrar(
        "renderizar_tela nao altera modelo._raw",
        modelo._raw == raw_antes,
    )
    _registrar(
        "renderizar_tela nao altera modelo.cabecalho",
        modelo.cabecalho == cabecalho_antes,
    )
    _registrar(
        "renderizar_tela nao altera corpo.elementos",
        [(e.id, e.tipo) for e in modelo.corpo.elementos] == elementos_antes,
    )
    _registrar(
        "renderizar_tela nao altera barra_de_menus.chips",
        modelo.barra_de_menus.get("chips", []) == chips_antes,
    )
    _registrar(
        "saida nao vaza campos inertes "
        "(origem_dados/bindings/filtros/tela_destino/regra_existencia)",
        "origem_dados" not in saida
        and "bindings" not in saida
        and "filtros" not in saida
        and "tela_destino" not in saida
        and "regra_existencia" not in saida,
    )
    _registrar(
        "saida nao expoe id interno de chip ('[chip_esc]')",
        "[chip_esc]" not in saida,
    )


def main():
    print("Diagnostico H-0006 - renderer visual com borda fixa")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_renderizador_orquestrador()
    teste_modelo_fabricado()
    teste_erros_renderizador()
    teste_proibicoes_importacao()
    teste_inercia()

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


if __name__ == "__main__":
    sys.exit(main())
