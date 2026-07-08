"""Diagnostico do modelo interno normalizado de tela (H-0002).

Executavel via:
    python tela/teste_modelo.py

Cobre os criterios de aceite testaveis do handoff H-0002:
- construcao do modelo a partir do dict do loader (H-0001) para
  config/telas/orquestrador.json;
- acesso por atributo a id, schema, cabecalho, corpo, barra_de_menus;
- corpo.arranjo e corpo.elementos acessiveis;
- cada elemento acessivel por id e tipo;
- tipos presentes = {console, dashboard, lancador};
- _campos_inertes preserva origem_dados pendente sem executar;
- barra_de_menus nao vazio;
- _raw preserva JSON original;
- diagnostico() retorna string nao vazia contendo id;
- construir_modelo({}) levanta ModeloTelaErro.

Apenas biblioteca padrao do Python.
"""

import sys
from pathlib import Path


_BASE_PADRAO = Path(__file__).resolve().parent.parent

sys.dont_write_bytecode = True

sys.path.insert(0, str(_BASE_PADRAO))

from tela.loader import carregar_tela  # noqa: E402
from tela.modelo import (  # noqa: E402
    Corpo,
    ElementoCorpo,
    ModeloTela,
    ModeloTelaErro,
    TIPOS_CORPO_VALIDOS,
    construir_modelo,
)


_RESULTADOS = []


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


def teste_modelo_orquestrador():
    print("")
    print("== Construcao do modelo para config/telas/orquestrador.json ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "construir_modelo(carregar_tela(orquestrador))",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("construir_modelo(carregar_tela(orquestrador))", True)

    _registrar(
        "modelo.id == 'orquestrador'",
        modelo.id == "orquestrador",
        "id={0!r}".format(modelo.id),
    )
    _registrar(
        "modelo.schema == 'tela.v1'",
        modelo.schema == "tela.v1",
        "schema={0!r}".format(modelo.schema),
    )
    _registrar(
        "modelo.cabecalho e dict com 'titulo' e 'descricao'",
        isinstance(modelo.cabecalho, dict)
        and "titulo" in modelo.cabecalho
        and "descricao" in modelo.cabecalho,
    )

    _registrar(
        "modelo.corpo e Corpo com arranjo e elementos",
        isinstance(modelo.corpo, Corpo)
        and hasattr(modelo.corpo, "arranjo")
        and hasattr(modelo.corpo, "elementos"),
    )
    _registrar(
        "modelo.corpo.arranjo == 'sobreposto'",
        modelo.corpo.arranjo == "sobreposto",
        "arranjo={0!r}".format(modelo.corpo.arranjo),
    )
    _registrar(
        "modelo.corpo.elementos e lista com 3 itens",
        isinstance(modelo.corpo.elementos, list)
        and len(modelo.corpo.elementos) == 3,
        "n={0}".format(len(modelo.corpo.elementos)),
    )

    todos_sao_elementos = all(
        isinstance(e, ElementoCorpo)
        and isinstance(e.id, str)
        and isinstance(e.tipo, str)
        for e in modelo.corpo.elementos
    )
    _registrar(
        "cada elemento e ElementoCorpo com id e tipo acessiveis",
        todos_sao_elementos,
    )

    tipos_presentes = sorted(e.tipo for e in modelo.corpo.elementos)
    _registrar(
        "tipos presentes = {console, dashboard, lancador}",
        tipos_presentes == ["console", "dashboard", "lancador"],
        "tipos={0!r}".format(tipos_presentes),
    )

    console = modelo.elemento_por_id("console_principal")
    dashboard = modelo.elemento_por_id("dashboard_info")
    lancador = modelo.elemento_por_id("lancador_principal")
    _registrar(
        "elemento_por_id('console_principal') retorna elemento tipo console",
        console is not None and console.tipo == "console",
    )
    _registrar(
        "elemento_por_id('dashboard_info') retorna elemento tipo dashboard",
        dashboard is not None and dashboard.tipo == "dashboard",
    )
    _registrar(
        "elemento_por_id('lancador_principal') retorna elemento tipo lancador",
        lancador is not None and lancador.tipo == "lancador",
    )
    _registrar(
        "elemento_por_id('inexistente') retorna None",
        modelo.elemento_por_id("inexistente") is None,
    )

    consoles = modelo.elementos_por_tipo("console")
    _registrar(
        "elementos_por_tipo('console') retorna lista com 1 item",
        isinstance(consoles, list) and len(consoles) == 1,
        "n={0}".format(len(consoles) if isinstance(consoles, list) else "?"),
    )

    print("")
    print("-- Declaracao inerte preservada (DOC-B008 / DOC-B009) --")

    origem_ok = (
        console is not None
        and isinstance(console._campos_inertes, dict)
        and isinstance(console._campos_inertes.get("origem_dados"), dict)
        and console._campos_inertes.get("origem_dados", {}).get("referencia")
        == "pendente"
    )
    _registrar(
        "console_principal._campos_inertes preserva origem_dados.referencia == 'pendente' (inerte)",
        origem_ok,
    )

    itens_inerte_ok = (
        lancador is not None
        and isinstance(lancador._campos_inertes.get("itens"), list)
        and len(lancador._campos_inertes.get("itens")) == 2
    )
    _registrar(
        "lancador_principal._campos_inertes['itens'] e lista com 2 itens (H-0013)",
        itens_inerte_ok,
        "itens={0!r}".format(
            lancador._campos_inertes.get("itens") if lancador else None
        ),
    )
    if itens_inerte_ok:
        item_inerte = lancador._campos_inertes["itens"][0]
        _registrar(
            "item[0] inerte preserva chip == 'd'",
            isinstance(item_inerte, dict)
            and item_inerte.get("chip") == "d",
        )
        _registrar(
            "item[0] inerte preserva texto == 'Destino'",
            isinstance(item_inerte, dict)
            and item_inerte.get("texto") == "Destino",
        )
        _registrar(
            "item[0] inerte preserva tela_destino == 'destino_minimo'",
            isinstance(item_inerte, dict)
            and item_inerte.get("tela_destino") == "destino_minimo",
        )
        _registrar(
            "item[0] inerte preserva id == 'item_destino_minimo'",
            isinstance(item_inerte, dict)
            and item_inerte.get("id") == "item_destino_minimo",
        )
        item_grupo_inerte = lancador._campos_inertes["itens"][1]
        _registrar(
            "item[1] inerte preserva chip == 'g' (H-0013)",
            isinstance(item_grupo_inerte, dict)
            and item_grupo_inerte.get("chip") == "g",
        )
        _registrar(
            "item[1] inerte preserva texto == 'Grupo Min.' (H-0013)",
            isinstance(item_grupo_inerte, dict)
            and item_grupo_inerte.get("texto") == "Grupo Min.",
        )
        _registrar(
            "item[1] inerte preserva tela_destino == 'grupo_minimo' (H-0013)",
            isinstance(item_grupo_inerte, dict)
            and item_grupo_inerte.get("tela_destino") == "grupo_minimo",
        )
        _registrar(
            "item[1] inerte preserva id == 'item_grupo_minimo' (H-0013)",
            isinstance(item_grupo_inerte, dict)
            and item_grupo_inerte.get("id") == "item_grupo_minimo",
        )

    _registrar(
        "modelo.barra_de_menus e dict nao vazio",
        isinstance(modelo.barra_de_menus, dict)
        and len(modelo.barra_de_menus) > 0,
    )

    chip_estilo = None
    for chip in modelo.barra_de_menus.get("chips", []):
        if isinstance(chip, dict) and chip.get("id") == "chip_estilo":
            chip_estilo = chip
            break
    _registrar(
        "chip_estilo.acao.tela_destino == 'pendente' preservado (inerte)",
        isinstance(chip_estilo, dict)
        and chip_estilo.get("acao", {}).get("tela_destino") == "pendente",
    )

    _registrar(
        "modelo._raw preserva JSON original completo",
        isinstance(modelo._raw, dict)
        and modelo._raw.get("id") == "orquestrador",
    )
    _registrar(
        "modelo._raw['bindings'] preservado como dict inerte",
        isinstance(modelo._raw.get("bindings"), dict),
    )
    _registrar(
        "modelo._raw['referencias_de_acoes'] preservado como dict inerte",
        isinstance(modelo._raw.get("referencias_de_acoes"), dict),
    )
    _registrar(
        "modelo._raw['filtros'] preservado como lista inerte",
        isinstance(modelo._raw.get("filtros"), list),
    )

    diag = modelo.diagnostico()
    _registrar(
        "modelo.diagnostico() retorna string nao vazia contendo id",
        isinstance(diag, str)
        and len(diag) > 0
        and "orquestrador" in diag,
    )
    _registrar(
        "diagnostico contem schema, arranjo e tipo de cada elemento",
        isinstance(diag, str)
        and "tela.v1" in diag
        and "console" in diag
        and "dashboard" in diag
        and "lancador" in diag,
    )

    _registrar(
        "TIPOS_CORPO_VALIDOS reexportado por tela.modelo == {console, lancador, dashboard}",
        TIPOS_CORPO_VALIDOS == {"console", "lancador", "dashboard"},
        "valor={0!r}".format(TIPOS_CORPO_VALIDOS),
    )

    return modelo


def teste_modelo_grupo_minimo():
    print("")
    print("== Construcao do modelo para config/telas/grupo_minimo.json (H-0012) ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "grupo_minimo")
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "construir_modelo(carregar_tela(grupo_minimo))",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("construir_modelo(carregar_tela(grupo_minimo))", True)

    _registrar(
        "modelo.id == 'grupo_minimo'",
        modelo.id == "grupo_minimo",
        "id={0!r}".format(modelo.id),
    )
    _registrar(
        "modelo.corpo.elementos e lista com 1 item",
        isinstance(modelo.corpo.elementos, list)
        and len(modelo.corpo.elementos) == 1,
        "n={0}".format(len(modelo.corpo.elementos)),
    )

    grupo = modelo.elemento_por_id("grupo_principal")
    _registrar(
        "elemento_por_id('grupo_principal') retorna elemento tipo 'grupo' (CA-18)",
        grupo is not None and grupo.tipo == "grupo",
    )
    grupos = modelo.elementos_por_tipo("grupo")
    _registrar(
        "elementos_por_tipo('grupo') retorna lista com 1 item (CA-19)",
        isinstance(grupos, list) and len(grupos) == 1,
        "n={0}".format(len(grupos) if isinstance(grupos, list) else "?"),
    )

    _registrar(
        "grupo e ElementoCorpo com id e tipo acessiveis",
        isinstance(grupo, ElementoCorpo)
        and isinstance(grupo.id, str) and isinstance(grupo.tipo, str),
    )

    _registrar(
        "grupo preserva arranjo em _campos_inertes",
        grupo is not None
        and grupo._campos_inertes.get("arranjo") == "sobreposto",
    )

    # CA-15: elemento funcional interno acessivel sem manipular dict cru
    _registrar(
        "grupo.elementos e lista com 1 ElementoCorpo interno (CA-15)",
        grupo is not None
        and isinstance(grupo.elementos, list)
        and len(grupo.elementos) == 1
        and isinstance(grupo.elementos[0], ElementoCorpo),
    )

    interno = grupo.elementos[0] if grupo else None
    _registrar(
        "elemento interno tem id == 'dashboard_conteudo'",
        interno is not None and interno.id == "dashboard_conteudo",
    )
    _registrar(
        "elemento interno tem tipo == 'dashboard' (CA-16)",
        interno is not None and interno.tipo == "dashboard",
    )
    _registrar(
        "elemento interno._campos_inertes preserva titulo e campos (CA-16)",
        interno is not None
        and interno._campos_inertes.get("titulo") == "Conteudo"
        and isinstance(interno._campos_inertes.get("campos"), list)
        and len(interno._campos_inertes.get("campos")) == 1,
    )
    _registrar(
        "elemento interno tem lista 'elementos' vazia (nao e container)",
        interno is not None and interno.elementos == [],
    )

    _registrar(
        "modelo distingue grupo de funcional: grupo.tipo nao e funcional",
        grupo is not None and grupo.tipo not in TIPOS_CORPO_VALIDOS,
    )
    _registrar(
        "modelo distingue grupo de funcional: interno.tipo e funcional",
        interno is not None and interno.tipo in TIPOS_CORPO_VALIDOS,
    )

    diag = modelo.diagnostico()
    _registrar(
        "diagnostico do modelo de grupo e string contendo id",
        isinstance(diag, str) and "grupo_minimo" in diag and "grupo" in diag,
    )


def teste_erros_modelo():
    print("")
    print("== Casos de erro do construtor de modelo ==")

    _espera_excecao(
        "construir_modelo({}) levanta ModeloTelaErro",
        lambda: construir_modelo({}),
        ModeloTelaErro,
    )
    _espera_excecao(
        "construir_modelo(None) levanta ModeloTelaErro",
        lambda: construir_modelo(None),
        ModeloTelaErro,
    )

    sem_corpo = {
        "id": "x",
        "schema": "tela.v1",
        "cabecalho": {},
        "barra_de_menus": {},
        "_raw": {},
    }
    _espera_excecao(
        "construir_modelo sem 'corpo' levanta ModeloTelaErro",
        lambda: construir_modelo(sem_corpo),
        ModeloTelaErro,
    )

    sem_elementos = {
        "id": "x",
        "schema": "tela.v1",
        "cabecalho": {},
        "barra_de_menus": {},
        "_raw": {},
        "corpo": {"arranjo": None},
    }
    _espera_excecao(
        "construir_modelo sem 'corpo.elementos' levanta ModeloTelaErro",
        lambda: construir_modelo(sem_elementos),
        ModeloTelaErro,
    )

    tipo_invalido = {
        "id": "x",
        "schema": "tela.v1",
        "cabecalho": {},
        "barra_de_menus": {},
        "_raw": {},
        "corpo": {
            "arranjo": None,
            "elementos": [{"id": "e1", "tipo": "tabela"}],
        },
    }
    _espera_excecao(
        "construir_modelo com tipo fora da taxonomia levanta ModeloTelaErro",
        lambda: construir_modelo(tipo_invalido),
        ModeloTelaErro,
    )


def main():
    print("Diagnostico H-0002 - modelo interno normalizado de tela")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    modelo = teste_modelo_orquestrador()
    teste_modelo_grupo_minimo()
    teste_erros_modelo()

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

    if modelo is not None:
        print("")
        print("== Diagnostico do modelo ==")
        print(modelo.diagnostico())

    return 0 if falharam == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
