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
        "modelo.corpo.arranjo == 'vertical'",
        modelo.corpo.arranjo == "vertical",
        "arranjo={0!r}".format(modelo.corpo.arranjo),
    )
    # H-0025 / ADR-0018: modelo preserva distribuicao declarada sem conversao.
    dist_modelo = modelo.corpo.distribuicao
    _registrar(
        "H-0025: modelo.corpo.distribuicao preserva fracao [2,1,2]",
        isinstance(dist_modelo, dict)
        and dist_modelo.get("modo") == "fracao"
        and dist_modelo.get("valores") == [2, 1, 2],
        "dist={0!r}".format(dist_modelo),
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
        and len(lancador._campos_inertes.get("itens")) == 7
    )
    _registrar(
        "lancador_principal._campos_inertes['itens'] e lista com 7 itens "
        "(H-0013 d/g + H-0030 chips 1-5)",
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

    # H-0016: modelo expoe distribuicao como objeto canônico ao renderer.
    dist = modelo.barra_de_menus.get("distribuicao")
    _registrar(
        "H-0016: modelo.barra_de_menus.distribuicao e objeto (nao string)",
        isinstance(dist, dict),
        "dist={0!r}".format(dist),
    )
    _registrar(
        "H-0016: modelo expoe distribuicao.modo == 'horizontal_responsiva'",
        isinstance(dist, dict) and dist.get("modo") == "horizontal_responsiva",
        "modo={0!r}".format(dist.get("modo") if isinstance(dist, dict) else None),
    )
    _registrar(
        "H-0016: modelo expoe distribuicao.ordem.politica == 'declaracao'",
        isinstance(dist, dict)
        and dist.get("ordem", {}).get("politica") == "declaracao",
    )

    chip_estilo = None
    for chip in modelo.barra_de_menus.get("chips", []):
        if isinstance(chip, dict) and chip.get("id") == "chip_estilo":
            chip_estilo = chip
            break
    _registrar(
        "chip_estilo removido da barra_de_menus do Orquestrador "
        "(capacidade nao implementada - ADR-0012/H-0014)",
        chip_estilo is None,
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
    # H-0025 / ADR-0018 D2: ausencia de distribuicao e preservada como None
    # (nao vira "igual" implicito).
    _registrar(
        "H-0025: grupo_minimo sem distribuicao -> modelo.corpo.distribuicao is None",
        modelo.corpo.distribuicao is None,
        "dist={0!r}".format(modelo.corpo.distribuicao),
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
        and grupo._campos_inertes.get("arranjo") == "vertical",
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


def _raw_tela(id_tela, corpo):
    """Constroi o dict minimo que carregar_tela retornaria para uso direto em construir_modelo."""
    raw_json = {
        "schema": "tela.v1", "id": id_tela,
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": corpo,
        "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
    }
    return {
        "schema": raw_json["schema"],
        "id": raw_json["id"],
        "cabecalho": raw_json["cabecalho"],
        "corpo": raw_json["corpo"],
        "barra_de_menus": raw_json["barra_de_menus"],
        "_raw": raw_json,
    }


def teste_hierarquia_grupos_adr0019_modelo():
    """Testes de arvore recursiva de grupos no modelo — ADR-0019 / H-0027 (secao 20.3)."""
    print("")
    print("== ADR-0019 / H-0027: hierarquia de grupos — modelo ==")

    # --- 2 niveis: g1 (nivel 1) -> g2 (nivel 2) -> funcional ---
    raw2 = _raw_tela("m_g2", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "horizontal",
                  "distribuicao": {"modo": "igual"},
                  "elementos": [
                      {"id": "c1", "tipo": "console"},
                      {"id": "d1", "tipo": "dashboard"},
                  ]},
             ]},
        ],
    })
    try:
        m2 = construir_modelo(raw2)
        _registrar("construir_modelo aceita 2 niveis de grupos (ADR-0019 D2)", True)
    except Exception as exc:
        _registrar("construir_modelo aceita 2 niveis de grupos (ADR-0019 D2)",
                   False, str(exc))
        return

    g1 = m2.corpo.elementos[0]
    _registrar("nivel 1: grupo g1 e ElementoCorpo tipo='grupo'",
               isinstance(g1, ElementoCorpo) and g1.tipo == "grupo")
    _registrar("nivel 1: g1._campos_inertes preserva arranjo='vertical'",
               g1._campos_inertes.get("arranjo") == "vertical")

    _registrar("nivel 1: g1.elementos tem 1 filho (g2)",
               isinstance(g1.elementos, list) and len(g1.elementos) == 1)

    g2 = g1.elementos[0] if g1.elementos else None
    _registrar("nivel 2: g2 e ElementoCorpo tipo='grupo'",
               g2 is not None and isinstance(g2, ElementoCorpo) and g2.tipo == "grupo")
    _registrar("nivel 2: g2._campos_inertes preserva arranjo='horizontal'",
               g2 is not None and g2._campos_inertes.get("arranjo") == "horizontal")
    _registrar(
        "nivel 2: g2._campos_inertes preserva distribuicao={'modo': 'igual'}",
        g2 is not None and g2._campos_inertes.get("distribuicao") == {"modo": "igual"},
    )
    _registrar("nivel 2: g2.elementos tem 2 filhos funcionais",
               g2 is not None and len(g2.elementos) == 2)

    if g2 and len(g2.elementos) == 2:
        c1 = g2.elementos[0]
        d1 = g2.elementos[1]
        _registrar("nivel 2 filho 0: c1 tipo='console'",
                   isinstance(c1, ElementoCorpo) and c1.tipo == "console")
        _registrar("nivel 2 filho 1: d1 tipo='dashboard'",
                   isinstance(d1, ElementoCorpo) and d1.tipo == "dashboard")
        _registrar("funcional nao e container: c1.elementos == []",
                   c1.elementos == [])

    # --- 3 niveis: g1 -> g2 -> g3 -> funcional ---
    raw3 = _raw_tela("m_g3", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "fracao", "valores": [1]},
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [
                      {"id": "g3", "tipo": "grupo", "arranjo": "horizontal",
                       "distribuicao": {"modo": "percentual", "valores": [70, 30]},
                       "elementos": [
                           {"id": "c1", "tipo": "console"},
                           {"id": "l1", "tipo": "lancador"},
                       ]},
                  ]},
             ]},
        ],
    })
    try:
        m3 = construir_modelo(raw3)
        _registrar("construir_modelo aceita 3 niveis de grupos (ADR-0019 D2)", True)
    except Exception as exc:
        _registrar("construir_modelo aceita 3 niveis de grupos (ADR-0019 D2)",
                   False, str(exc))
        return

    g1_3 = m3.corpo.elementos[0]
    _registrar(
        "nivel 1 (3-niveis): g1._campos_inertes preserva distribuicao fracao",
        g1_3._campos_inertes.get("distribuicao") == {"modo": "fracao", "valores": [1]},
    )
    g2_3 = g1_3.elementos[0] if g1_3.elementos else None
    g3_3 = g2_3.elementos[0] if (g2_3 and g2_3.elementos) else None
    _registrar("nivel 3 existe e e tipo='grupo'",
               g3_3 is not None and g3_3.tipo == "grupo")
    _registrar(
        "nivel 3: g3._campos_inertes preserva arranjo='horizontal' e distribuicao percentual",
        g3_3 is not None
        and g3_3._campos_inertes.get("arranjo") == "horizontal"
        and g3_3._campos_inertes.get("distribuicao") == {
            "modo": "percentual", "valores": [70, 30]
        },
    )
    _registrar("nivel 3 tem 2 filhos funcionais (c1, l1)",
               g3_3 is not None and len(g3_3.elementos) == 2)

    # --- Multiplos filhos de grupo no mesmo nivel (D3) ---
    raw_multi = _raw_tela("m_multi", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2a", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "c1", "tipo": "console"}]},
                 {"id": "g2b", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "d1", "tipo": "dashboard"}]},
                 {"id": "g2c", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "l1", "tipo": "lancador"}]},
             ]},
        ],
    })
    try:
        m_multi = construir_modelo(raw_multi)
        g1_m = m_multi.corpo.elementos[0]
        _registrar("multiplos filhos de grupo no nivel 2: g1 tem 3 grupos filhos (D3)",
                   len(g1_m.elementos) == 3)
        ids_filhos = [e.id for e in g1_m.elementos]
        _registrar("ids dos 3 grupos filhos corretos",
                   ids_filhos == ["g2a", "g2b", "g2c"])
    except Exception as exc:
        _registrar("multiplos filhos de grupo no nivel 2 (D3)", False, str(exc))

    # --- elemento_por_id: escopo plano (nao desce em grupos) ---
    raw_plano = _raw_tela("m_plano", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "gtopo", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "interno", "tipo": "console"}]},
            {"id": "direto", "tipo": "lancador"},
        ],
    })
    m_plano = construir_modelo(raw_plano)
    _registrar(
        "elemento_por_id('direto') retorna elemento nivel raiz (escopo plano)",
        m_plano.elemento_por_id("direto") is not None
        and m_plano.elemento_por_id("direto").tipo == "lancador",
    )
    _registrar(
        "elemento_por_id('interno') retorna None (escopo plano, nao desce em grupos)",
        m_plano.elemento_por_id("interno") is None,
    )
    _registrar(
        "elementos_por_tipo('console') retorna [] (escopo plano, console esta dentro do grupo)",
        m_plano.elementos_por_tipo("console") == [],
    )
    _registrar(
        "elementos_por_tipo('grupo') retorna [gtopo] (escopo plano inclui o grupo raiz)",
        len(m_plano.elementos_por_tipo("grupo")) == 1
        and m_plano.elementos_por_tipo("grupo")[0].id == "gtopo",
    )
    _registrar(
        "elemento interno acessivel por navegacao direta: gtopo.elementos[0].id == 'interno'",
        m_plano.elemento_por_id("gtopo").elementos[0].id == "interno",
    )


def _grupo_matriz_modelo_h0028():
    return {
        "id": "g_matriz",
        "tipo": "grupo",
        "estrutura": "matriz",
        "matriz": {
            "linhas": {
                "quantidade": 2,
                "distribuicao": {"modo": "fracao", "valores": [1, 2]},
            },
            "colunas": {
                "quantidade": 2,
                "distribuicao": {"modo": "percentual", "valores": [40, 60]},
            },
            "celulas": [
                {"linha": 2, "coluna": 2, "elemento": "d"},
                {"linha": 1, "coluna": 1, "elemento": "a"},
                {"linha": 1, "coluna": 2, "elemento": "b"},
                {"linha": 2, "coluna": 1, "elemento": "c"},
            ],
        },
        "elementos": [
            {"id": "a", "tipo": "console", "titulo": "A"},
            {"id": "b", "tipo": "dashboard", "titulo": "B"},
            {"id": "c", "tipo": "lancador", "titulo": "C", "itens": []},
            {
                "id": "d",
                "tipo": "grupo",
                "estrutura": "livre",
                "arranjo": "vertical",
                "elementos": [{"id": "d1", "tipo": "console"}],
            },
        ],
    }


class TestModeloMatrizH0028:
    """Confirma transporte inerte de estrutura/matriz no modelo."""

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def test_campos_inertes_preservam_estrutura_matriz_e_distribuicoes(self):
        grupo_raw = _grupo_matriz_modelo_h0028()
        modelo = construir_modelo(_raw_tela(
            "modelo_matriz",
            {"arranjo": "vertical", "elementos": [grupo_raw]},
        ))
        grupo = modelo.corpo.elementos[0]
        matriz = grupo._campos_inertes.get("matriz")
        self._r(
            "H-0028 modelo: grupo preserva estrutura='matriz' em _campos_inertes",
            grupo._campos_inertes.get("estrutura") == "matriz",
        )
        self._r(
            "H-0028 modelo: matriz preserva linhas/colunas/celulas",
            isinstance(matriz, dict)
            and matriz.get("linhas") == grupo_raw["matriz"]["linhas"]
            and matriz.get("colunas") == grupo_raw["matriz"]["colunas"]
            and matriz.get("celulas") == grupo_raw["matriz"]["celulas"],
        )

    def test_ordem_de_elementos_e_vinculo_por_ids_preservados(self):
        grupo_raw = _grupo_matriz_modelo_h0028()
        modelo = construir_modelo(_raw_tela(
            "modelo_matriz_ordem",
            {"arranjo": "vertical", "elementos": [grupo_raw]},
        ))
        grupo = modelo.corpo.elementos[0]
        ids_filhos = [elemento.id for elemento in grupo.elementos]
        celulas = grupo._campos_inertes["matriz"]["celulas"]
        self._r(
            "H-0028 modelo: ordem declarativa de elementos[] preservada",
            ids_filhos == ["a", "b", "c", "d"],
            "ids={0!r}".format(ids_filhos),
        )
        self._r(
            "H-0028 modelo: celulas continuam vinculadas por ids declarados",
            [c["elemento"] for c in celulas] == ["d", "a", "b", "c"],
        )
        self._r(
            "H-0028 modelo: elementos nao foram duplicados por coordenadas",
            len(grupo.elementos) == 4 and len(set(ids_filhos)) == 4,
        )

    def test_grupo_livre_dentro_de_celula_preservado_no_limite(self):
        grupo_raw = _grupo_matriz_modelo_h0028()
        modelo = construir_modelo(_raw_tela(
            "modelo_matriz_grupo_livre",
            {"arranjo": "vertical", "elementos": [grupo_raw]},
        ))
        grupo_matriz = modelo.corpo.elementos[0]
        grupo_livre = grupo_matriz.elementos[3]
        self._r(
            "H-0028 modelo: grupo dentro de celula permanece grupo",
            grupo_livre.tipo == "grupo" and grupo_livre.id == "d",
        )
        self._r(
            "H-0028 modelo: grupo livre interno preserva arranjo e filho",
            grupo_livre._campos_inertes.get("estrutura") == "livre"
            and grupo_livre._campos_inertes.get("arranjo") == "vertical"
            and len(grupo_livre.elementos) == 1
            and grupo_livre.elementos[0].id == "d1",
        )

    def run_all(self):
        print("")
        print("== TestModeloMatrizH0028: preservacao inerte de matriz (H-0028) ==")
        self.test_campos_inertes_preservam_estrutura_matriz_e_distribuicoes()
        self.test_ordem_de_elementos_e_vinculo_por_ids_preservados()
        self.test_grupo_livre_dentro_de_celula_preservado_no_limite()


# Telas permanentes do catalogo H-0030.
_TELAS_H0030_MODELO = [
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_3x2",
    "h0030_matriz_2x4",
]

# Dimensoes esperadas de cada matriz (linhas, colunas).
_DIMENSOES_H0030 = {
    "h0030_matriz_2x2": (2, 2),
    "h0030_matriz_3x2": (3, 2),
    "h0030_matriz_2x4": (2, 4),
}


class TestModeloCatalogoH0030:
    """Interpretacao do modelo para o catalogo H-0030 (5 telas permanentes).

    Cobre (H-0030 secao 14.2):
    - construir_modelo nao lanca excecao para cada tela;
    - interpretacao correta do console unico;
    - interpretacao correta do dashboard unico;
    - dimensoes corretas das matrizes (linhas/colunas);
    - coordenadas explicitas presentes em cada matriz;
    - grade integral (cobertura completa de celulas);
    - identificadores consistentes (celulas referenciam filhos existentes).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _carregar(self, id_tela):
        return construir_modelo(carregar_tela(_BASE_PADRAO, id_tela))

    def test_modelo_cada_tela_nao_lanca(self):
        for id_tela in _TELAS_H0030_MODELO:
            try:
                modelo = self._carregar(id_tela)
                ok = modelo is not None and modelo.id == id_tela
            except Exception as exc:
                ok = False
                detalhe = "{0}: {1}".format(type(exc).__name__, exc)
            else:
                detalhe = ""
            self._r(
                "H-0030 modelo: construir_modelo({0}) nao lanca e id confere".format(
                    id_tela
                ),
                ok,
                detalhe,
            )

    def test_console_unico(self):
        modelo = self._carregar("h0030_console_unico")
        corpo = modelo.corpo
        self._r(
            "H-0030 modelo: console_unico corpo tem 1 elemento",
            len(corpo.elementos) == 1,
            "n={0}".format(len(corpo.elementos)),
        )
        elem = corpo.elementos[0]
        self._r(
            "H-0030 modelo: console_unico corpo[0].id == 'console_catalogo'",
            elem.id == "console_catalogo",
        )
        self._r(
            "H-0030 modelo: console_unico corpo[0].tipo == 'console'",
            elem.tipo == "console",
        )
        self._r(
            "H-0030 modelo: console_unico origem_dados preservado inerte (null)",
            elem._campos_inertes.get("origem_dados") is None,
            "origem_dados={0!r}".format(elem._campos_inertes.get("origem_dados")),
        )
        self._r(
            "H-0030 modelo: console_unico itens == [] (vazio deterministico)",
            elem._campos_inertes.get("itens") == [],
        )

    def test_dashboard_unico(self):
        modelo = self._carregar("h0030_dashboard_unico")
        corpo = modelo.corpo
        self._r(
            "H-0030 modelo: dashboard_unico corpo tem 1 elemento",
            len(corpo.elementos) == 1,
        )
        elem = corpo.elementos[0]
        self._r(
            "H-0030 modelo: dashboard_unico corpo[0].id == 'dashboard_catalogo'",
            elem.id == "dashboard_catalogo",
        )
        self._r(
            "H-0030 modelo: dashboard_unico corpo[0].tipo == 'dashboard'",
            elem.tipo == "dashboard",
        )
        campos = elem._campos_inertes.get("campos")
        self._r(
            "H-0030 modelo: dashboard_unico tem 2 campos literais",
            isinstance(campos, list) and len(campos) == 2
            and all(c.get("fonte") == "literal" for c in campos),
            "campos={0!r}".format(campos),
        )
        valores = {c.get("id"): c.get("valor") for c in campos}
        self._r(
            "H-0030 modelo: dashboard_unico Tipo='dashboard único' e Ciclo='H-0030'",
            valores.get("tipo_corpo") == "dashboard único"
            and valores.get("ciclo") == "H-0030",
            "valores={0!r}".format(valores),
        )

    def test_matrizes_dimensoes_e_coordenadas(self):
        for id_matriz, (n_linhas, n_colunas) in _DIMENSOES_H0030.items():
            modelo = self._carregar(id_matriz)
            grupo = modelo.corpo.elementos[0]
            self._r(
                "H-0030 modelo: {0} corpo[0].tipo == 'grupo'".format(id_matriz),
                grupo.tipo == "grupo",
            )
            matriz = grupo._campos_inertes.get("matriz")
            self._r(
                "H-0030 modelo: {0} tem matriz.linhas.quantidade == {1}".format(
                    id_matriz, n_linhas
                ),
                isinstance(matriz, dict)
                and matriz.get("linhas", {}).get("quantidade") == n_linhas,
            )
            self._r(
                "H-0030 modelo: {0} tem matriz.colunas.quantidade == {1}".format(
                    id_matriz, n_colunas
                ),
                isinstance(matriz, dict)
                and matriz.get("colunas", {}).get("quantidade") == n_colunas,
            )
            self._r(
                "H-0030 modelo: {0} distribuicao igual em ambos os eixos".format(
                    id_matriz
                ),
                isinstance(matriz, dict)
                and matriz.get("linhas", {}).get("distribuicao", {}).get("modo") == "igual"
                and matriz.get("colunas", {}).get("distribuicao", {}).get("modo") == "igual",
            )
            celulas = matriz.get("celulas") if isinstance(matriz, dict) else None
            self._r(
                "H-0030 modelo: {0} tem {1} celulas (grade integral)".format(
                    id_matriz, n_linhas * n_colunas
                ),
                isinstance(celulas, list) and len(celulas) == n_linhas * n_colunas,
                "n={0}".format(len(celulas) if isinstance(celulas, list) else "?"),
            )

            # Coordenadas explicitas: todas (linha,coluna) unicas e dentro do grid.
            coordenadas = [
                (c.get("linha"), c.get("coluna"))
                for c in celulas
                if isinstance(c, dict)
            ]
            esperadas = {
                (ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            self._r(
                "H-0030 modelo: {0} coordenadas cobrem toda a grade sem lacuna".format(
                    id_matriz
                ),
                set(coordenadas) == esperadas and len(coordenadas) == len(set(coordenadas)),
                "coordenadas={0!r}".format(sorted(coordenadas)),
            )

            # Identificadores consistentes: celulas[].elemento referenciam filhos.
            ids_filhos = {e.id for e in grupo.elementos}
            refs_celulas = {c.get("elemento") for c in celulas}
            self._r(
                "H-0030 modelo: {0} celulas referenciam somente filhos existentes".format(
                    id_matriz
                ),
                refs_celulas <= ids_filhos,
                "refs={0!r} filhos={1!r}".format(refs_celulas, ids_filhos),
            )
            self._r(
                "H-0030 modelo: {0} cada filho tem exatamente uma celula".format(
                    id_matriz
                ),
                len(refs_celulas) == len(ids_filhos) == (n_linhas * n_colunas),
                "refs={0} filhos={1}".format(len(refs_celulas), len(ids_filhos)),
            )

            # Cada filho e dashboard com titulo "L<n> C<n>" e campo pos literal.
            for filho in grupo.elementos:
                self._r(
                    "H-0030 modelo: {0} filho {1} e dashboard".format(
                        id_matriz, filho.id
                    ),
                    filho.tipo == "dashboard",
                )

    def test_preservacao_validacoes_vigentes(self):
        """Telas anteriores continuam carregando no modelo sem regressao."""
        for id_perm in ("destino_minimo", "grupo_minimo", "orquestrador"):
            try:
                m = self._carregar(id_perm)
                ok = m is not None
            except Exception:
                ok = False
            self._r(
                "H-0030 modelo: tela anterior {0} ainda constroi modelo".format(
                    id_perm
                ),
                ok,
            )

    def run_all(self):
        print("")
        print("== TestModeloCatalogoH0030: modelo das 5 telas permanentes ==")
        self.test_modelo_cada_tela_nao_lanca()
        self.test_console_unico()
        self.test_dashboard_unico()
        self.test_matrizes_dimensoes_e_coordenadas()
        self.test_preservacao_validacoes_vigentes()


def main():
    print("Diagnostico H-0002 - modelo interno normalizado de tela")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    modelo = teste_modelo_orquestrador()
    teste_modelo_grupo_minimo()
    teste_erros_modelo()
    teste_hierarquia_grupos_adr0019_modelo()
    TestModeloMatrizH0028().run_all()
    TestModeloCatalogoH0030().run_all()

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
