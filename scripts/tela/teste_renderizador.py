"""Diagnostico do renderer estrutural de tela (H-0005).

Executavel via:
    python tela/teste_renderizador.py

Cobre os criterios de aceite testaveis do handoff H-0005:
- renderizar_tela aceita ModeloTela valido sem excecao;
- saida e str;
- saida comeca com "TELA: orquestrador";
- saida contem "SCHEMA: tela.v1";
- saida contem "REGIAO: cabecalho";
- saida contem "titulo: Orquestrador";
- saida contem "descricao:";
- saida contem "REGIAO: corpo";
- saida contem "arranjo: sobreposto";
- saida contem cada componente do corpo como "[{tipo}] {id}";
- saida contem "REGIAO: barra_de_menus";
- saida contem "[chip_esc]" e "[chip_ajuda]";
- saida e deterministica (duas chamadas com mesmo modelo sao identicas);
- saida bate com expected output literal do handoff H-0005 (igualdade
  estrita, incluindo o \\n final);
- modelo fabricado com id="teste_fabricado" produz saida usando dados
  do modelo, nao do JSON em disco (com corpo e chips tambem verificados);
- renderizar_tela(None) lanca RenderizadorErro;
- renderer nao importa json/os/pathlib nem chama carregar_tela;
- renderer nao acessa _campos_inertes dos elementos;
- renderer nao executa acao, binding, filtro ou navegacao.

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
    "TELA: orquestrador\n"
    "SCHEMA: tela.v1\n"
    "\n"
    "REGIAO: cabecalho\n"
    "  titulo: Orquestrador\n"
    "  descricao: Tela raiz do sistema — ponto de entrada e visao "
    "consolidada do pipeline de survey\n"
    "\n"
    "REGIAO: corpo\n"
    "  arranjo: sobreposto\n"
    "  componentes:\n"
    "    [console] console_principal\n"
    "    [dashboard] dashboard_info\n"
    "    [lancador] lancador_principal\n"
    "\n"
    "REGIAO: barra_de_menus\n"
    "  chips:\n"
    "    [chip_esc] Sair\n"
    "    [chip_paginas] Páginas\n"
    "    [chip_colunas] Colunas\n"
    "    [chip_grupos] Grupos\n"
    "    [chip_alternar] Alternar\n"
    "    [chip_navegar] Navegar\n"
    "    [chip_selecionar] Selecionar\n"
    "    [chip_enter] Todos\n"
    "    [chip_estilo] Estilo\n"
    "    [chip_verboso] Verboso\n"
    "    [chip_ajuda] Ajuda\n"
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
        "saida comeca com 'TELA: orquestrador'",
        saida.startswith("TELA: orquestrador"),
    )
    _registrar(
        "saida contem 'SCHEMA: tela.v1'",
        "SCHEMA: tela.v1" in saida,
    )
    _registrar(
        "saida contem 'REGIAO: cabecalho'",
        "REGIAO: cabecalho" in saida,
    )
    _registrar(
        "saida contem 'titulo: Orquestrador'",
        "titulo: Orquestrador" in saida,
    )
    _registrar(
        "saida contem 'descricao:'",
        "descricao:" in saida,
    )
    _registrar(
        "saida contem 'REGIAO: corpo'",
        "REGIAO: corpo" in saida,
    )
    _registrar(
        "saida contem 'arranjo: sobreposto'",
        "arranjo: sobreposto" in saida,
    )
    _registrar(
        "saida contem '[console] console_principal'",
        "[console] console_principal" in saida,
    )
    _registrar(
        "saida contem '[dashboard] dashboard_info'",
        "[dashboard] dashboard_info" in saida,
    )
    _registrar(
        "saida contem '[lancador] lancador_principal'",
        "[lancador] lancador_principal" in saida,
    )
    _registrar(
        "saida contem 'REGIAO: barra_de_menus'",
        "REGIAO: barra_de_menus" in saida,
    )
    _registrar(
        "saida contem '[chip_esc]'",
        "[chip_esc]" in saida,
    )
    _registrar(
        "saida contem '[chip_ajuda]'",
        "[chip_ajuda]" in saida,
    )

    saida2 = renderizar_tela(modelo)
    _registrar(
        "saida e deterministica (duas chamadas identicas)",
        saida == saida2,
    )

    bate = saida == _EXPECTED_ORQUESTRADOR
    _registrar(
        "saida bate com expected output literal do handoff H-0005",
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
        "saida fabricada comeca com 'TELA: teste_fabricado'",
        saida_fab.startswith("TELA: teste_fabricado"),
        "prefixo={0!r}".format(saida_fab[:40]),
    )
    _registrar(
        "saida fabricada contem 'SCHEMA: tela.v0'",
        "SCHEMA: tela.v0" in saida_fab,
    )
    _registrar(
        "saida fabricada contem 'arranjo: linear'",
        "arranjo: linear" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '[console] e1'",
        "[console] e1" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '[c1] Ok'",
        "[c1] Ok" in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona orquestrador",
        "orquestrador" not in saida_fab,
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

    console = modelo.elemento_por_id("console_principal")
    lancador = modelo.elemento_por_id("lancador_principal")
    inertes_console_antes = dict(console._campos_inertes)
    inertes_lancador_antes = dict(lancador._campos_inertes)

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
        "console._campos_inertes preserva origem_dados.referencia == 'pendente' (inerte)",
        console._campos_inertes == inertes_console_antes
        and console._campos_inertes.get("origem_dados", {}).get("referencia")
        == "pendente",
    )
    _registrar(
        "lancador._campos_inertes['itens'] == [] preservado (inerte)",
        lancador._campos_inertes == inertes_lancador_antes
        and lancador._campos_inertes.get("itens") == [],
    )
    _registrar(
        "saida nao vaza campos inertes (origem_dados/bindings/filtros/tela_destino/regra_existencia)",
        "origem_dados" not in saida
        and "bindings" not in saida
        and "filtros" not in saida
        and "tela_destino" not in saida
        and "regra_existencia" not in saida,
    )


def main():
    print("Diagnostico H-0005 - renderer estrutural de tela")
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
