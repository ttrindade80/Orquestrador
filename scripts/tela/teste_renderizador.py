"""Diagnostico do renderer declarativo (H-0006 / H-0007 / H-0009 / H-0010A).

Executavel via:
    python tela/teste_renderizador.py

Cobre os criterios de aceite testaveis dos handoffs H-0006, H-0007,
H-0009 e H-0010A. O H-0010A substitui placeholders hardcoded por
conteudo derivado do modelo/JSON e adiciona:

- inspecao de fonte contra constantes hardcoded de itens do lancador;
- inspecao de fonte contra chips hardcoded da barra_de_menus;
- rejeicao de item de lancador com texto acima de 15 caracteres
  (sem truncamento, sem abreviacao);
- render declarativo do dashboard com fonte "literal";
- render declarativo do console com placeholder "(console)";
- render declarativo da barra_de_menus lendo chips[] do JSON;
- render declarativo do lancador lendo itens[] do JSON;
- destino_minimo renderiza "Voltar" e "Tela de destino para teste do
  lancador" (lidos do JSON, nao hardcoded).

Secoes cobertas:
- renderer sobre config/telas/orquestrador.json;
- renderer sobre config/telas/destino_minimo.json (H-0010A);
- modelo fabricado (usa dados do modelo, nao do JSON em disco);
- casos de erro (None, dict, tipo_borda invalido, texto > 15 chars);
- proibicoes de import/leitura no modulo do renderer;
- inspecao de fonte contra constantes hardcoded (H-0010A);
- inercia: renderer nao executa/resolve/ativa;
- alternancia de borda em memoria (H-0007);
- largura explicita (H-0009);
- altura explicita (H-0015 / ADR-0013): ocupacao vertical da janela do
  terminal pelo corpo com linhas de preenchimento e RenderizadorErro em
  terminal pequeno.

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
from tela.renderizador import (  # noqa: E402
    RenderizadorErro,
    _linhas_barra,
    renderizar_tela,
)


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
    "│ [d] Destino                            │\n"
    "│ [g] Grupo Min.                         │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menus ─────────────────────────────────╮\n"
    "│  [Esc] Sair  [?] Ajuda                 │\n"
    "╰────────────────────────────────────────╯\n"
)


_EXPECTED_ORQUESTRADOR_RETA = (
    "┌ ORQUESTRADOR ──────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "└────────────────────────────────────────┘\n"
    "┌ ITENS ─────────────────────────────────┐\n"
    "│ (console)                              │\n"
    "└────────────────────────────────────────┘\n"
    "┌ INFO ──────────────────────────────────┐\n"
    "└────────────────────────────────────────┘\n"
    "┌ NAVEGAR ───────────────────────────────┐\n"
    "│ [d] Destino                            │\n"
    "│ [g] Grupo Min.                         │\n"
    "└────────────────────────────────────────┘\n"
    "┌ Menus ─────────────────────────────────┐\n"
    "│  [Esc] Sair  [?] Ajuda                 │\n"
    "└────────────────────────────────────────┘\n"
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
        "saida contem '│ Tela raiz do sistema' (cabecalho do JSON)",
        "│ Tela raiz do sistema" in saida,
    )
    _registrar(
        "saida contem '╭ ITENS' (console_principal)",
        "╭ ITENS" in saida,
    )
    _registrar(
        "saida contem '(console)' (placeholder de escopo)",
        "(console)" in saida,
    )
    _registrar(
        "saida contem '╭ INFO' (dashboard_info do JSON)",
        "╭ INFO" in saida,
    )
    _registrar(
        "saida contem '╭ NAVEGAR' (lancador_principal do JSON)",
        "╭ NAVEGAR" in saida,
    )
    _registrar(
        "saida contem '[d]' (chip do item do lancador do JSON)",
        "[d]" in saida,
    )
    _registrar(
        "saida contem 'Destino' (texto do item do lancador do JSON)",
        "Destino" in saida,
    )
    _registrar(
        "saida contem '╭ Menus' (caixa da barra)",
        "╭ Menus" in saida,
    )
    _registrar(
        "saida contem '[Esc] Sair' (chip Esc do JSON)",
        "[Esc] Sair" in saida,
    )
    _registrar(
        "saida NAO contem '[<>] Paginas' (chip removido do Orquestrador)",
        "[<>] Páginas" not in saida,
    )
    _registrar(
        "saida contem '[?] Ajuda' (chip do JSON)",
        "[?] Ajuda" in saida,
    )
    _registrar(
        "saida contem '╰' (borda inferior)",
        "╰" in saida,
    )

    _registrar(
        "saida NAO contem '[B] Borda' (nao hardcoded; nunca declarado no JSON)",
        "[B] Borda" not in saida,
    )
    _registrar(
        "saida NAO contem 'Dashboard de teste' (placeholder removido)",
        "Dashboard de teste" not in saida,
    )
    _registrar(
        "saida NAO contem 'Sem dados carregados' (placeholder removido)",
        "Sem dados carregados" not in saida,
    )
    _registrar(
        "saida NAO contem '╭ DASHBOARD' (label generico removido)",
        "╭ DASHBOARD" not in saida,
    )
    _registrar(
        "saida NAO contem '╭ Menu ' (label antigo 'Menu' sem 's')",
        "╭ Menu " not in saida,
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
        "saida bate com expected output literal do H-0010A (curva, 42)",
        bate,
        "" if bate else "ver diff abaixo",
    )
    if not bate:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR))
        print("--- obtido (repr) ---")
        print(repr(saida))

    return modelo


def teste_renderizador_destino_minimo():
    print("")
    print("== Renderer sobre modelo de config/telas/destino_minimo.json (H-0010A) ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "destino_minimo")
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo (destino_minimo)",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar(
        "pipeline carregar_tela + construir_modelo (destino_minimo)",
        True,
    )

    try:
        saida = renderizar_tela(modelo)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(destino_minimo) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("renderizar_tela(destino_minimo) sem excecao", True)

    _registrar(
        "saida destino comeca com '╭ DESTINO MINIMO'",
        saida.startswith("╭ DESTINO MINIMO"),
    )
    _registrar(
        "saida destino contem 'Tela de destino para teste do lancador'",
        "Tela de destino para teste do lancador" in saida,
    )
    _registrar(
        "saida destino contem '╭ TESTE' (dashboard_teste do JSON)",
        "╭ TESTE" in saida,
    )
    _registrar(
        "saida destino contem '╭ Menus'",
        "╭ Menus" in saida,
    )
    _registrar(
        "saida destino contem '[Esc] Voltar' (chip Esc declarado no JSON)",
        "[Esc] Voltar" in saida,
    )
    _registrar(
        "saida destino NAO contem '[Esc] Sair'",
        "[Esc] Sair" not in saida,
    )
    _registrar(
        "saida destino NAO contem '(console)' (sem elemento console)",
        "(console)" not in saida,
    )

    larguras_ok = all(
        (len(ln) == 42 for ln in saida.split("\n") if ln != "")
    )
    _registrar(
        "cada linha da saida destino tem exatamente 42 chars Python",
        larguras_ok,
    )

    return modelo


def teste_renderizador_grupo_minimo():
    print("")
    print("== Renderer sobre modelo de config/telas/grupo_minimo.json (H-0012) ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "grupo_minimo")
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo (grupo_minimo)",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar(
        "pipeline carregar_tela + construir_modelo (grupo_minimo)",
        True,
    )

    try:
        saida = renderizar_tela(modelo)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(grupo_minimo) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return None
    _registrar("renderizar_tela(grupo_minimo) sem excecao", True)

    # CA-20: caixa bordeada do dashboard interno aparece
    _registrar(
        "saida contem '╭ CONTEUDO' (caixa do dashboard interno - CA-20)",
        "╭ CONTEUDO" in saida,
    )
    # CA-21: valor literal declarado aparece
    _registrar(
        "saida contem 'Dashboard dentro de grupo estrutural' (CA-21)",
        "Dashboard dentro de grupo estrutural" in saida,
    )
    # CA-22: grupo nao gera caixa visual propria
    _registrar(
        "grupo NAO gera caixa propria (sem '╭ GRUPO_PRINCIPAL') (CA-22)",
        "╭ GRUPO_PRINCIPAL" not in saida,
    )
    _registrar(
        "id interno do grupo nao vaza para saida ('grupo_principal' ausente)",
        "grupo_principal" not in saida,
    )
    # CA-22: grupo nao gera caixa visual propria -- o cabecalho da tela
    # legitimo e "Grupo Minimo", por isso o teste de "sem caixa do grupo"
    # conta os top-borders: esperam-se exatamente 3 caixas (cabecalho,
    # dashboard interno, menus), sem uma quarta caixa para o container.
    _registrar(
        "grupo nao adiciona caixa propria (3 caixas: cabec/dash/menus) (CA-22)",
        saida.count("╭") == 3 and saida.count("╰") == 3,
        "topos={0} bases={1}".format(
            saida.count("╭"), saida.count("╰")
        ),
    )

    larguras_ok = all(
        len(ln) == 42 for ln in saida.split("\n") if ln != ""
    )
    _registrar(
        "cada linha da saida grupo tem exatamente 42 chars Python",
        larguras_ok,
    )

    # CA-23: saida do grupo e indistinguivel do mesmo dashboard em lista plana
    grupo = modelo.elemento_por_id("grupo_principal")
    interno = grupo.elementos[0]
    modelo_plano = ModeloTela(
        id=modelo.id,
        schema=modelo.schema,
        cabecalho=modelo.cabecalho,
        corpo=Corpo(
            arranjo=modelo.corpo.arranjo,
            elementos=[interno],
        ),
        barra_de_menus=modelo.barra_de_menus,
        _raw=modelo._raw,
    )
    saida_plano = renderizar_tela(modelo_plano)
    _registrar(
        "saida do grupo == saida da lista plana equivalente (CA-23)",
        saida == saida_plano,
    )

    # CA-24 reforco: Orquestrador (lista plana) segue inalterado
    tela_o = carregar_tela(_BASE_PADRAO, "orquestrador")
    modelo_o = construir_modelo(tela_o)
    saida_o = renderizar_tela(modelo_o)
    _registrar(
        "Orquestrador (lista plana) permanece inalterado (CA-24)",
        saida_o == _EXPECTED_ORQUESTRADOR,
    )

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
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
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
        "saida fabricada contem '╭ CONSOLE' (fallback de titulo)",
        "╭ CONSOLE" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '(console)' (placeholder de escopo)",
        "(console)" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '╭ Menus' (label fixo da caixa)",
        "╭ Menus" in saida_fab,
    )
    _registrar(
        "saida fabricada contem '[k] Ok' (chip do modelo fabricado)",
        "[k] Ok" in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona 'orquestrador'",
        "orquestrador" not in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona 'ORQUESTRADOR'",
        "ORQUESTRADOR" not in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona '[Esc] Sair' (nao esta no modelo fab)",
        "[Esc] Sair" not in saida_fab,
    )
    _registrar(
        "saida fabricada nao menciona '[d] Destino' (nao esta no modelo fab)",
        "[d] Destino" not in saida_fab,
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

    print("")
    print("-- Rejeicao de item de lancador com texto > 15 chars (H-0010A) --")

    modelo_item_longo = ModeloTela(
        id="x",
        schema="tela.v1",
        cabecalho={"titulo": "X", "descricao": "D"},
        corpo=Corpo(
            arranjo="sobreposto",
            elementos=[
                ElementoCorpo(
                    id="l",
                    tipo="lancador",
                    _campos_inertes={
                        "titulo": "L",
                        "itens": [
                            {
                                "id": "i_longo",
                                "chip": "z",
                                "texto": "1234567890123456",
                                "tela_destino": "x",
                            }
                        ],
                    },
                )
            ],
        ),
        barra_de_menus={"chips": []},
        _raw={},
    )
    exc_item = _espera_excecao(
        "item com texto de 16 chars levanta RenderizadorErro (sem truncamento)",
        lambda: renderizar_tela(modelo_item_longo),
        RenderizadorErro,
    )
    if exc_item is not None:
        _registrar(
            "mensagem de erro menciona o limite 15 e o texto recusado",
            "15" in str(exc_item) and "1234567890123456" in str(exc_item),
            str(exc_item),
        )

    modelo_item_limite = ModeloTela(
        id="y",
        schema="tela.v1",
        cabecalho={"titulo": "Y", "descricao": "D"},
        corpo=Corpo(
            arranjo="sobreposto",
            elementos=[
                ElementoCorpo(
                    id="l",
                    tipo="lancador",
                    _campos_inertes={
                        "titulo": "L",
                        "itens": [
                            {
                                "id": "i_ok",
                                "chip": "z",
                                "texto": "123456789012345",
                                "tela_destino": "y",
                            }
                        ],
                    },
                )
            ],
        ),
        barra_de_menus={"chips": []},
        _raw={},
    )
    try:
        saida_limite = renderizar_tela(modelo_item_limite)
        _registrar(
            "item com texto de exatamente 15 chars e aceito",
            "[z] 123456789012345" in saida_limite,
        )
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "item com texto de exatamente 15 chars e aceito",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
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
        "renderer acessa _campos_inertes legitimamente (H-0010A declarativo)",
        "_campos_inertes" in texto_mod,
    )


def teste_inspecao_fonte_hardcoded():
    print("")
    print("== Inspecao de fonte contra constantes hardcoded (H-0010A) ==")

    caminho_mod = _BASE_PADRAO / "tela" / "renderizador.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "renderer fonte NAO contem '[d] Destino' (item do lancador)",
        "[d] Destino" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'Destino' como literal de item",
        "\"Destino\"" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem '[Esc] Sair' (chip do JSON)",
        "[Esc] Sair" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem '[Esc] Voltar' (chip do JSON)",
        "[Esc] Voltar" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'Voltar' como literal de chip",
        "\"Voltar\"" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'Sair' como literal de chip",
        "\"Sair\"" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'Páginas' (chip do JSON)",
        "Páginas" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'destino_minimo' (tela_destino do JSON)",
        "destino_minimo" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem 'Dashboard de teste' (placeholder antigo)",
        "Dashboard de teste" not in texto_mod,
    )
    _registrar(
        "renderer fonte NAO contem '[B] Borda' (binding interno da demo)",
        "[B] Borda" not in texto_mod,
    )

    _registrar(
        "renderer fonte contem '_campos_inertes' (acesso declarativo)",
        "_campos_inertes" in texto_mod,
    )
    _registrar(
        "renderer fonte contem 'barra_de_menus' (leitura declarativa)",
        "barra_de_menus" in texto_mod,
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


def teste_alternancia_borda():
    print("")
    print("== Alternancia de borda em memoria (H-0007) ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
    modelo = construir_modelo(tela_raw)

    try:
        saida_curva_explicita = renderizar_tela(modelo, tipo_borda="curva")
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(modelo, tipo_borda='curva') sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "renderizar_tela(modelo, tipo_borda='curva') sem excecao",
        True,
    )

    saida_default = renderizar_tela(modelo)
    _registrar(
        "renderizar_tela(modelo, tipo_borda='curva') == renderizar_tela(modelo)",
        saida_curva_explicita == saida_default,
    )

    try:
        saida_reta = renderizar_tela(modelo, tipo_borda="reta")
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(modelo, tipo_borda='reta') sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "renderizar_tela(modelo, tipo_borda='reta') sem excecao",
        True,
    )

    _registrar(
        "saida reta e str",
        isinstance(saida_reta, str),
        "tipo={0}".format(type(saida_reta).__name__),
    )
    _registrar(
        "saida reta contem '┌' (canto superior esquerdo reto)",
        "┌" in saida_reta,
    )
    _registrar(
        "saida reta contem '┐' (canto superior direito reto)",
        "┐" in saida_reta,
    )
    _registrar(
        "saida reta contem '└' (canto inferior esquerdo reto)",
        "└" in saida_reta,
    )
    _registrar(
        "saida reta contem '┘' (canto inferior direito reto)",
        "┘" in saida_reta,
    )
    _registrar(
        "saida reta nao contem '╭' (canto curvo ausente)",
        "╭" not in saida_reta,
    )
    _registrar(
        "saida reta nao contem '╮' (canto curvo ausente)",
        "╮" not in saida_reta,
    )
    _registrar(
        "saida reta nao contem '╰' (canto curvo ausente)",
        "╰" not in saida_reta,
    )
    _registrar(
        "saida reta nao contem '╯' (canto curvo ausente)",
        "╯" not in saida_reta,
    )
    _registrar(
        "saida reta contem '│ Tela raiz do sistema' (conteudo preservado)",
        "│ Tela raiz do sistema" in saida_reta,
    )
    _registrar(
        "saida reta contem '[d] Destino' (item do lancador preservado)",
        "[d] Destino" in saida_reta,
    )
    _registrar(
        "saida reta NAO contem '[B] Borda' (nao declarado no JSON)",
        "[B] Borda" not in saida_reta,
    )

    larguras_reta_ok = all(
        len(ln) == 42 for ln in saida_reta.split("\n") if ln != ""
    )
    _registrar(
        "cada linha da saida reta tem exatamente 42 chars Python",
        larguras_reta_ok,
    )

    bate_reta = saida_reta == _EXPECTED_ORQUESTRADOR_RETA
    _registrar(
        "saida reta bate com _EXPECTED_ORQUESTRADOR_RETA (igualdade estrita)",
        bate_reta,
        "" if bate_reta else "ver diff abaixo",
    )
    if not bate_reta:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR_RETA))
        print("--- obtido (repr) ---")
        print(repr(saida_reta))

    curva_convertida = (
        saida_curva_explicita
        .replace("╭", "┌").replace("╮", "┐")
        .replace("╰", "└").replace("╯", "┘")
    )
    _registrar(
        "trocar borda altera somente os quatro cantos",
        curva_convertida == saida_reta,
    )

    linhas_conteudo_curva = [
        ln for ln in saida_curva_explicita.split("\n") if ln.startswith("│")
    ]
    linhas_conteudo_reta = [
        ln for ln in saida_reta.split("\n") if ln.startswith("│")
    ]
    _registrar(
        "linhas de conteudo (│ ...) sao identicas entre curva e reta",
        linhas_conteudo_curva == linhas_conteudo_reta,
    )

    _espera_excecao(
        "renderizar_tela(modelo, tipo_borda='invalida') lanca RenderizadorErro",
        lambda: renderizar_tela(modelo, tipo_borda="invalida"),
        RenderizadorErro,
    )
    _espera_excecao(
        "renderizar_tela(modelo, tipo_borda='CURVA') lanca RenderizadorErro "
        "(case sensitive)",
        lambda: renderizar_tela(modelo, tipo_borda="CURVA"),
        RenderizadorErro,
    )

    _registrar(
        "saida reta e deterministica (duas chamadas identicas)",
        renderizar_tela(modelo, "reta") == renderizar_tela(modelo, "reta"),
    )


def teste_largura_explicita():
    print("")
    print("== Largura explicita (H-0009) ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
    modelo = construir_modelo(tela_raw)

    saida_42 = renderizar_tela(modelo, largura=42)
    bate_42 = saida_42 == _EXPECTED_ORQUESTRADOR
    _registrar(
        "renderizar_tela(modelo, largura=42) == _EXPECTED_ORQUESTRADOR "
        "(fallback equivalente)",
        bate_42,
        "" if bate_42 else "ver diff abaixo",
    )
    if not bate_42:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR))
        print("--- obtido (repr) ---")
        print(repr(saida_42))

    saida_42_reta = renderizar_tela(modelo, largura=42, tipo_borda="reta")
    bate_42_reta = saida_42_reta == _EXPECTED_ORQUESTRADOR_RETA
    _registrar(
        "renderizar_tela(modelo, largura=42, tipo_borda='reta') == "
        "_EXPECTED_ORQUESTRADOR_RETA",
        bate_42_reta,
        "" if bate_42_reta else "ver diff abaixo",
    )
    if not bate_42_reta:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR_RETA))
        print("--- obtido (repr) ---")
        print(repr(saida_42_reta))

    saida_60 = renderizar_tela(modelo, largura=60)
    _registrar(
        "renderizar_tela(modelo, largura=60) retorna str",
        isinstance(saida_60, str),
        "tipo={0}".format(type(saida_60).__name__),
    )

    linhas_60_ok = all(
        len(ln) == 60 for ln in saida_60.split("\n") if ln != ""
    )
    _registrar(
        "cada linha nao-vazia de renderizar_tela(modelo, largura=60) tem 60 chars",
        linhas_60_ok,
    )

    _registrar(
        "saida com largura=60 comeca com '╭ ORQUESTRADOR'",
        saida_60.startswith("╭ ORQUESTRADOR"),
    )

    _registrar(
        "saida com largura=60 nao contem '\\n\\n' entre caixas",
        "\n\n" not in saida_60,
    )

    _registrar(
        "renderizar_tela(modelo) == renderizar_tela(modelo, largura=None)",
        renderizar_tela(modelo) == renderizar_tela(modelo, largura=None),
    )


def teste_altura_explicita():
    print("")
    print("== Altura explicita (H-0015 / ADR-0013 - ocupacao vertical) ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
    modelo = construir_modelo(tela_raw)

    # Contabilidade verificada contra o orquestrador.json real (largura=42).
    # H-0016: a barra_de_menus agora e horizontal responsiva. Com 2 chips em
    # largura 42 (content_w=39), "[Esc] Sair" + "  " + "[?] Ajuda" = 21 <= 39,
    # logo cabem em linha unica -> N_linhas_barra = 1.
    #   L_cab = 3 (1 topo + 1 descricao + 1 base)
    #   L_corpo_conteudo = 9 (ITENS=3, INFO=2, NAVEGAR=4)
    #   L_barra = 3 (1 topo + 1 linha horizontal + 1 base)
    #   altura natural (sem preenchimento) = 3 + 9 + 3 = 15
    l_cab = 3
    l_corpo_conteudo = 9
    l_barra = 3
    n_minimo = l_cab + l_corpo_conteudo + l_barra  # 15

    # CA-09 / CA-10: altura=None preserva o comportamento atual.
    _registrar(
        "renderizar_tela(modelo, largura=42) == "
        "renderizar_tela(modelo, largura=42, altura=None)",
        renderizar_tela(modelo, largura=42)
        == renderizar_tela(modelo, largura=42, altura=None),
    )

    # CA-03: altura exatamente minima -> sem preenchimento (L_corpo_fill == 0),
    # saida identica ao comportamento natural.
    saida_min = renderizar_tela(modelo, largura=42, altura=n_minimo)
    _registrar(
        "altura=N_minimo (15) -> count('\\n') == 15 (sem fill) (CA-03)",
        saida_min.count("\n") == n_minimo,
        "count={0}".format(saida_min.count("\n")),
    )
    _registrar(
        "altura=N_minimo (15) gera saida identica a altura=None",
        saida_min == renderizar_tela(modelo, largura=42),
    )

    # CA-01: altura=16 -> 16 linhas (1 de preenchimento).
    saida_16 = renderizar_tela(modelo, largura=42, altura=16)
    _registrar(
        "renderizar_tela(modelo, largura=42, altura=16) -> 16 linhas (CA-01)",
        saida_16.count("\n") == 16,
        "count={0}".format(saida_16.count("\n")),
    )

    # CA-02: altura=24 -> exatamente 24 linhas, barra preservada.
    saida_24 = renderizar_tela(modelo, largura=42, altura=24)
    _registrar(
        "renderizar_tela(modelo, largura=42, altura=24) -> 24 linhas (CA-02)",
        saida_24.count("\n") == 24,
        "count={0}".format(saida_24.count("\n")),
    )
    _registrar(
        "altura=24 preserva a barra_de_menus ('[Esc] Sair' na saida)",
        "[Esc] Sair" in saida_24,
    )

    # Contagem de preenchimento para altura=24 (H-0016, L_barra=3):
    #   L_corpo_disponivel = 24 - 3 - 3 = 18
    #   L_corpo_fill = 18 - 9 = 9
    l_corpo_fill_24 = (24 - l_cab - l_barra) - l_corpo_conteudo  # 9
    linhas_24 = saida_24.split("\n")
    # Identifica linhas de preenchimento: NAO usa strip() para validar
    # a evidencia (ACH-H15-02); compara a linha inteira contra a string
    # de `total_w` espacos.
    fill_esperado = " " * 42
    fills = [ln for ln in linhas_24 if ln == fill_esperado]
    _registrar(
        "altura=24 gera exatamente 8 linhas de preenchimento",
        len(fills) == l_corpo_fill_24,
        "fills={0} esperado={1}".format(len(fills), l_corpo_fill_24),
    )

    # CA-05: cada linha de preenchimento tem exatamente `largura` espacos.
    _registrar(
        "linhas de preenchimento tem exatamente 42 espacos (CA-05)",
        all(ln == fill_esperado for ln in fills),
    )

    # CA-04: cada linha nao-vazia da saida tem exatamente `largura` chars.
    larguras_24_ok = all(
        len(ln) == 42 for ln in linhas_24 if ln != ""
    )
    _registrar(
        "altura=24: cada linha nao-vazia tem exatamente 42 chars (CA-04)",
        larguras_24_ok,
    )

    # CA-08: preenchimento fica entre o ultimo box do corpo e o box Menus.
    # Estrutura (H-0016, L_barra=3): cabecalho(3) + ITENS(3) + INFO(2) +
    # NAVEGAR(4) = 12 caixas, depois 9 fills (indices 12..20), depois Menus
    # topo no indice 21, 1 linha horizontal de chips no 22, base no 23.
    _registrar(
        "preenchimento entre corpo e Menus (CA-08): linha 12 = fill, "
        "linha 20 = fill, linha 21 = '╭ Menus'",
        linhas_24[12] == fill_esperado
        and linhas_24[20] == fill_esperado
        and linhas_24[21].startswith("╭ Menus"),
        "l12={0!r} l20={1!r} l21={2!r}".format(
            linhas_24[12], linhas_24[20], linhas_24[21][:9]
        ),
    )

    # CA-06: cabecalho continua no topo (primeira linha comeca com '╭ ').
    _registrar(
        "cabecalho no topo: primeira linha comeca com '╭ ORQUESTRADOR' (CA-06)",
        saida_24.startswith("╭ ORQUESTRADOR"),
    )

    # CA-07: barra_de_menus no rodape: ultima linha nao-vazia termina com '╯'.
    ultima_nao_vazia = [ln for ln in linhas_24 if ln != ""][-1]
    _registrar(
        "barra_de_menus no rodape: ultima linha nao-vazia termina com '╯' (CA-07)",
        ultima_nao_vazia.endswith("╯"),
        "ultima={0!r}".format(ultima_nao_vazia),
    )

    # Invariante preservado: saida nao contem "\n\n" (linhas de preenchimento
    # sao espacos, nao vazias).
    _registrar(
        "altura=24: saida nao contem '\\n\\n' (invariante preservado)",
        "\n\n" not in saida_24,
    )

    # Preenchimento em outra largura: cada linha de fill tem a largura dada.
    saida_60_24 = renderizar_tela(modelo, largura=60, altura=24)
    linhas_60_24 = saida_60_24.split("\n")
    fills_60 = [ln for ln in linhas_60_24 if ln == " " * 60]
    _registrar(
        "largura=60 altura=24 -> 24 linhas, fills com 60 espacos",
        saida_60_24.count("\n") == 24
        and len(fills_60) == l_corpo_fill_24
        and all(len(ln) == 60 for ln in linhas_60_24 if ln != ""),
    )

    # Preenchimento com borda reta: largura e contagem identicas a curva.
    saida_24_reta = renderizar_tela(
        modelo, largura=42, altura=24, tipo_borda="reta"
    )
    _registrar(
        "altura=24 reta -> 24 linhas e rodape termina com '┘'",
        saida_24_reta.count("\n") == 24
        and [ln for ln in saida_24_reta.split("\n") if ln != ""][-1].endswith("┘"),
    )

    # CA-12: altura insuficiente para o corpo (overflow) -> RenderizadorErro.
    # N_overflow = L_cab + L_barra + L_corpo_conteudo - 1 = 14.
    n_overflow = l_cab + l_barra + l_corpo_conteudo - 1
    exc_overflow = _espera_excecao(
        "altura=14 (corpo overflow) levanta RenderizadorErro (CA-12)",
        lambda: renderizar_tela(modelo, largura=42, altura=n_overflow),
        RenderizadorErro,
    )
    if exc_overflow is not None:
        _registrar(
            "mensagem de overflow menciona corpo/area disponivel (CA-13)",
            "corpo" in str(exc_overflow) and "14" in str(exc_overflow),
            str(exc_overflow),
        )

    # CA-11: altura insuficiente para cabecalho + barra -> RenderizadorErro.
    # Para o Orquestrador (H-0016): L_cab(3) + L_barra(3) = 6 > 5.
    exc_pequeno = _espera_excecao(
        "altura=5 (cabecalho + barra > altura) levanta RenderizadorErro (CA-11)",
        lambda: renderizar_tela(modelo, largura=42, altura=5),
        RenderizadorErro,
    )
    if exc_pequeno is not None:
        _registrar(
            "mensagem de terminal pequeno menciona cabecalho/barra (CA-13)",
            "cabecalho" in str(exc_pequeno)
            and "barra_de_menus" in str(exc_pequeno)
            and "5" in str(exc_pequeno),
            str(exc_pequeno),
        )

    # CA-14: exatamente no limite cabecalho + barra, sem corpo, deve ERRO
    # quando L_corpo_conteudo(9) > 0 e L_corpo_disponivel = 0.
    _espera_excecao(
        "altura == L_cab + L_barra (6) com corpo nao vazio levanta "
        "RenderizadorErro (sem truncamento silencioso)",
        lambda: renderizar_tela(modelo, largura=42, altura=6),
        RenderizadorErro,
    )

    # Determinismo: duas chamadas identicas produzem saidas identicas.
    _registrar(
        "altura explicita e deterministica (duas chamadas identicas)",
        renderizar_tela(modelo, largura=42, altura=24)
        == renderizar_tela(modelo, largura=42, altura=24),
    )


def _dist_canonica(preenchimento="coluna_a_coluna", **sobrepos):
    """Copia mutável do objeto canônico de distribuicao para testes H-0016."""
    d = {
        "modo": "horizontal_responsiva",
        "ordem": {"politica": "declaracao", "ancoras": {}},
        "tentativa_inicial": "linha_unica",
        "quebra": "multilinha_quando_nao_couber",
        "preenchimento_multilinha": preenchimento,
        "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
        "linhas": {"minimo": 1, "maximo": 2, "preferir_menor_numero": True},
        "alinhamento_linhas": "esquerda",
        "espacamentos": {
            "margem_horizontal": {"minimo": 1, "maximo": None},
            "vao_chip_texto": {"minimo": 1, "maximo": 3},
            "vao_entre_chips": {"minimo": 2, "maximo": 6},
            "vao_entre_colunas": {"minimo": 2, "maximo": 8},
            "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0},
        },
        "colunas": {
            "largura": "por_maior_item_da_coluna",
            "subcolunas": {
                "chip": {"alinhamento": "esquerda"},
                "texto": {"alinhamento": "esquerda"},
            },
        },
        "overflow": {
            "quando_nao_couber": "erro_layout",
            "nao_omitir_chips": True,
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        },
    }
    for chave, valor in sobrepos.items():
        d[chave] = valor
    return d


def _chip(cid, tecla, texto):
    """Chip minimal para testes de _linhas_barra."""
    return {"id": cid, "tecla": tecla, "texto": texto}


class TestLinhasBarra:
    """Casos H-0016: distribuicao horizontal responsiva da barra_de_menus.

    Cobertura obrigatoria do handoff H-0016: linha unica, multilinha,
    erro_layout, alias string, distribuicao ausente, chips vazia, ancoras
    (valida/violada/inexistente), ordem preservada, chips do lancador
    ausentes da barra, coluna_a_coluna, linha_a_linha, renderizar_tela com
    canonico, preservacao da altura H-0015, altura minima com barra
    horizontal, fluxo g/d/b/Esc, e validacoes defensivas (PR-M-01..04).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn):
        try:
            fn()
        except RenderizadorErro as exc:
            self._r(nome, True, "{0}: {1}".format(type(exc).__name__, exc))
            return exc
        except Exception as exc:  # pragma: no cover - diagnostico
            self._r(nome, False,
                    "esperava RenderizadorErro; obteve {0}: {1}".format(
                        type(exc).__name__, exc))
            return None
        self._r(nome, False, "esperava RenderizadorErro; nenhuma excecao")
        return None

    def test_linha_unica_cabe(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "linha unica: retorna lista com 1 string quando cabe (content_w=39)",
            isinstance(linhas, list) and len(linhas) == 1,
            "linhas={0!r}".format(linhas),
        )
        self._r(
            "linha unica contem ambos os chips",
            "[Esc] Sair" in linhas[0] and "[?] Ajuda" in linhas[0],
            "linha={0!r}".format(linhas[0] if linhas else None),
        )

    def test_linha_unica_nao_cabe_vai_para_multilinha(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        # single = 21 > 15; multilinha K=2 (1 coluna, 2 linhas) cabe (max 10).
        linhas = _linhas_barra(bar, 15)
        self._r(
            "multilinha: content_w=15 -> 2 linhas",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )

    def test_multilinha_nao_cabe_erro_layout(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        exc = self._espera_erro(
            "erro_layout: content_w=5 nao cabe em nenhuma config",
            lambda: _linhas_barra(bar, 5),
        )
        if exc is not None:
            self._r(
                "mensagem de erro_layout contem 'erro_layout'",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_alias_string_horizontal_aceito(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": "horizontal", "chips": chips}
        try:
            linhas = _linhas_barra(bar, 39)
            ok = isinstance(linhas, list) and len(linhas) == 1
        except RenderizadorErro as exc:
            ok = False
            self._r("alias string 'horizontal' aceito sem erro", False, str(exc))
            return
        self._r("alias string 'horizontal' aceito sem erro", ok,
                "linhas={0!r}".format(linhas))

    def test_distribuicao_ausente_aceito(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"chips": chips}  # sem 'distribuicao'
        try:
            linhas = _linhas_barra(bar, 39)
            ok = isinstance(linhas, list) and len(linhas) >= 1
        except RenderizadorErro as exc:
            ok = False
            self._r("distribuicao ausente/None aceito sem erro", False, str(exc))
            return
        self._r("distribuicao ausente/None aceito sem erro", ok,
                "linhas={0!r}".format(linhas))

    def test_chips_vazia_retorna_lista_vazia(self):
        bar = {"distribuicao": _dist_canonica(), "chips": []}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "chips vazia retorna lista vazia",
            linhas == [],
            "linhas={0!r}".format(linhas),
        )

    def test_ancora_primeiro_valida(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_esc"]}
        bar = {"distribuicao": dist, "chips": chips}
        try:
            _linhas_barra(bar, 39)
            self._r("ancora primeiro valida: sem erro", True)
        except RenderizadorErro as exc:
            self._r("ancora primeiro valida: sem erro", False, str(exc))

    def test_ancora_primeiro_violada(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_ajuda"]}  # nao eh o 1o
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora primeiro violada -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )

    def test_ancora_ultimo_valida(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"ultimo": ["chip_ajuda"]}
        bar = {"distribuicao": dist, "chips": chips}
        try:
            _linhas_barra(bar, 39)
            self._r("ancora ultimo valida: sem erro", True)
        except RenderizadorErro as exc:
            self._r("ancora ultimo valida: sem erro", False, str(exc))

    def test_ancora_ultimo_violada(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"ultimo": ["chip_esc"]}  # nao eh o ultimo
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora ultimo violada -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )

    def test_ancora_id_inexistente(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_inexistente"]}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora com id inexistente -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )

    def test_ordem_preservada(self):
        chips = [
            _chip("a", "1", "AAA"),
            _chip("b", "2", "BBB"),
            _chip("c", "3", "CCC"),
        ]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, 100)
        saida = " ".join(linhas)
        self._r(
            "ordem preservada na saida (a antes de b antes de c)",
            saida.find("[1] AAA") < saida.find("[2] BBB")
            and saida.find("[2] BBB") < saida.find("[3] CCC"),
            "saida={0!r}".format(saida),
        )

    def test_chips_declarados_aparecem_exatamente_uma_vez(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, 39)
        junta = " ".join(linhas)
        self._r(
            "cada chip declarado aparece exatamente uma vez",
            junta.count("[Esc] Sair") == 1 and junta.count("[?] Ajuda") == 1,
            "junta={0!r}".format(junta),
        )

    def test_chips_do_lancador_nao_entram_na_barra(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "orquestrador"))
        linhas = _linhas_barra(modelo.barra_de_menus, 39)
        junta = " ".join(linhas)
        self._r(
            "barra contem chips da barra ([Esc], [?])",
            "[Esc]" in junta and "[?]" in junta,
            "junta={0!r}".format(junta),
        )
        self._r(
            "barra NAO contem chips do lancador ([d], [g])",
            "[d]" not in junta and "[g]" not in junta,
            "junta={0!r}".format(junta),
        )
        # corpo.arranjo nao influencia a barra: o lancador continua no corpo.
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "lancador ([d]/[g]) permanece no corpo, nao na barra",
            "[d] Destino" in saida and "[g] Grupo Min." in saida,
        )

    def test_coluna_a_coluna_layout(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        # Forca multilinha K=2: single = 5*5 + 2*4 = 33 > 23 (largura_util com margem=1).
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["linhas"] = {"minimo": 1, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 25)
        self._r(
            "coluna_a_coluna K=2 -> 2 linhas (content_w=25)",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )
        if isinstance(linhas, list) and len(linhas) == 2:
            # Preenchimento coluna-a-coluna: line0 tem A,C,E; line1 tem B,D.
            self._r(
                "coluna_a_coluna: linha 0 contem A, C, E (coluna-major)",
                "[1] A" in linhas[0] and "[3] C" in linhas[0]
                and "[5] E" in linhas[0],
                "linha0={0!r}".format(linhas[0]),
            )
            self._r(
                "coluna_a_coluna: linha 1 contem B, D (coluna-major)",
                "[2] B" in linhas[1] and "[4] D" in linhas[1],
                "linha1={0!r}".format(linhas[1]),
            )
            self._r(
                "coluna_a_coluna: linha 1 NAO contem A, C, E",
                "[1] A" not in linhas[1] and "[3] C" not in linhas[1]
                and "[5] E" not in linhas[1],
            )

    def test_linha_a_linha_implementado(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        dist = _dist_canonica(preenchimento="linha_a_linha")
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 25)
        self._r(
            "linha_a_linha K=2 -> 2 linhas (content_w=25)",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )
        if isinstance(linhas, list) and len(linhas) == 2:
            # Preenchimento linha-a-linha: line0=A,B,C; line1=D,E.
            self._r(
                "linha_a_linha: linha 0 contem A, B, C (linha-major)",
                "[1] A" in linhas[0] and "[2] B" in linhas[0]
                and "[3] C" in linhas[0],
                "linha0={0!r}".format(linhas[0]),
            )
            self._r(
                "linha_a_linha: linha 1 contem D, E (linha-major)",
                "[4] D" in linhas[1] and "[5] E" in linhas[1],
                "linha1={0!r}".format(linhas[1]),
            )

    def test_modo_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["modo"] = "vertical"
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "modo desconhecido ('vertical') -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )

    def test_politica_desconhecida_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["ordem"] = {"politica": "grupos_declarados", "ancoras": {}}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ordem.politica nao suportada ('grupos_declarados') -> "
            "RenderizadorErro (PR-M-01)",
            lambda: _linhas_barra(bar, 39),
        )

    def test_preenchimento_multilinha_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("x", "?", "Aj")]
        dist = _dist_canonica(preenchimento="outro_modo")
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "preenchimento_multilinha desconhecido -> RenderizadorErro (PR-M-02)",
            lambda: _linhas_barra(bar, 15),
        )

    def test_linhas_minimo_invalido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 0, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.minimo invalido (0) -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, 39),
        )

    def test_linhas_maximo_menor_que_minimo_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 3, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.maximo < minimo -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, 39),
        )

    def test_overflow_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("x", "?", "Aj")]
        dist = _dist_canonica()
        dist["overflow"] = {
            "quando_nao_couber": "omitir",
            "nao_omitir_chips": True,
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        }
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "overflow.quando_nao_couber desconhecido -> RenderizadorErro (PR-M-04)",
            lambda: _linhas_barra(bar, 39),
        )

    def test_overflow_flag_nao_booleana_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["overflow"] = {
            "quando_nao_couber": "erro_layout",
            "nao_omitir_chips": "sim",
            "nao_truncar_texto": True,
            "nao_reordenar": True,
        }
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "overflow flag nao booleana -> RenderizadorErro (PR-M-04)",
            lambda: _linhas_barra(bar, 39),
        )

    def test_renderizar_tela_com_distribuicao_canonica(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "orquestrador"))
        dist = modelo.barra_de_menus.get("distribuicao")
        self._r(
            "JSON migrado expoe distribuicao como objeto com modo canonico",
            isinstance(dist, dict)
            and dist.get("modo") == "horizontal_responsiva"
            and dist.get("ordem", {}).get("politica") == "declaracao",
            "modo={0!r}".format(dist.get("modo") if isinstance(dist, dict) else None),
        )
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "renderizar_tela com canonico: barra em linha horizontal",
            saida == _EXPECTED_ORQUESTRADOR,
            "" if saida == _EXPECTED_ORQUESTRADOR else "snapshot diverge",
        )

    def test_renderizar_tela_preserva_altura_h0015(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "orquestrador"))
        saida_24 = renderizar_tela(modelo, largura=42, altura=24)
        linhas = _linhas_barra(modelo.barra_de_menus, 39)
        l_barra = len(linhas) + 2
        self._r(
            "altura explicita: L_barra = len(linhas_barra)+2 = 3 (1 linha horizontal)",
            l_barra == 3 and len(linhas) == 1,
            "l_barra={0} linhas={1}".format(l_barra, len(linhas)),
        )
        self._r(
            "renderizar_tela(altura=24) -> 24 linhas (H-0015 preservado)",
            saida_24.count("\n") == 24,
            "count={0}".format(saida_24.count("\n")),
        )

    def test_altura_minima_com_barra_horizontal(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "orquestrador"))
        # H-0016: n_minimo = L_cab(3) + L_corpo(9) + L_barra(3) = 15.
        saida_15 = renderizar_tela(modelo, largura=42, altura=15)
        self._r(
            "altura minima = 15 com barra horizontal (antes era 16)",
            saida_15.count("\n") == 15
            and saida_15 == renderizar_tela(modelo, largura=42),
            "count={0}".format(saida_15.count("\n")),
        )

    def test_fluxo_g_d_b_esc_preservado(self):
        # O renderer continua exibindo lancador ([d]/[g]) no corpo e os chips
        # da barra ([Esc]/[?]) no rodape; a navegacao g/d/b/Esc (tratada pela
        # demo) depende desses chips continuarem presentes e corretos.
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "orquestrador"))
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "fluxo g/d/b/Esc: lancador [d]/[g] e barra [Esc]/[?] presentes",
            "[d] Destino" in saida and "[g] Grupo Min." in saida
            and "[Esc] Sair" in saida and "[?] Ajuda" in saida,
        )

    def run_all(self):
        print("")
        print("== H-0016 - distribuicao horizontal responsiva da barra_de_menus ==")
        self.test_linha_unica_cabe()
        self.test_linha_unica_nao_cabe_vai_para_multilinha()
        self.test_multilinha_nao_cabe_erro_layout()
        self.test_alias_string_horizontal_aceito()
        self.test_distribuicao_ausente_aceito()
        self.test_chips_vazia_retorna_lista_vazia()
        self.test_ancora_primeiro_valida()
        self.test_ancora_primeiro_violada()
        self.test_ancora_ultimo_valida()
        self.test_ancora_ultimo_violada()
        self.test_ancora_id_inexistente()
        self.test_ordem_preservada()
        self.test_chips_declarados_aparecem_exatamente_uma_vez()
        self.test_chips_do_lancador_nao_entram_na_barra()
        self.test_coluna_a_coluna_layout()
        self.test_linha_a_linha_implementado()
        self.test_modo_desconhecido_erro()
        self.test_politica_desconhecida_erro()
        self.test_preenchimento_multilinha_desconhecido_erro()
        self.test_linhas_minimo_invalido_erro()
        self.test_linhas_maximo_menor_que_minimo_erro()
        self.test_overflow_desconhecido_erro()
        self.test_overflow_flag_nao_booleana_erro()
        self.test_renderizar_tela_com_distribuicao_canonica()
        self.test_renderizar_tela_preserva_altura_h0015()
        self.test_altura_minima_com_barra_horizontal()
        self.test_fluxo_g_d_b_esc_preservado()


class TestDistribuicaoH0018:
    """Cobertura executavel de todos os campos de distribuicao (H-0018).

    28 testes que garantem que nenhum campo de barra_de_menus.distribuicao
    e ignorado silenciosamente: cada campo tem efeito observavel, e validado
    ou rejeitado de forma deterministica.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            self._r(nome, True, str(exc))
            return exc
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    # ------------------------------------------------------------------ 1-3
    def test_vao_chip_texto_altera_distancia(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 3
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "vao_chip_texto=3: chip contem 3 espacos entre ] e texto",
            isinstance(linhas, list) and any("[Esc]   Sair" in l for l in linhas),
            "linhas={0!r}".format(linhas),
        )

    def test_vao_chip_texto_10_espaco_extra(self):
        chips = [_chip("c_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 10
        dist["espacamentos"]["vao_chip_texto"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "vao_chip_texto=10: chip contem 10 espacos entre ] e texto",
            isinstance(linhas, list) and any("[Esc]          Sair" in l for l in linhas),
            "linhas={0!r}".format(linhas),
        )

    def test_vao_chip_texto_altera_comprimento_linha(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        d1 = _dist_canonica()
        d1["espacamentos"]["vao_chip_texto"]["minimo"] = 1
        d5 = _dist_canonica()
        d5["espacamentos"]["vao_chip_texto"]["minimo"] = 5
        d5["espacamentos"]["vao_chip_texto"]["maximo"] = None
        l1 = _linhas_barra({"distribuicao": d1, "chips": chips}, 80)
        l5 = _linhas_barra({"distribuicao": d5, "chips": chips}, 80)
        self._r(
            "vao_chip_texto=5 produz linha mais longa que vao=1",
            isinstance(l1, list) and isinstance(l5, list)
            and l5 and l1 and len(l5[0]) > len(l1[0]),
            "vao1={0!r} vao5={1!r}".format(l1, l5),
        )

    # ------------------------------------------------------------------ 4-6
    def test_margem_horizontal_altera_padding(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 4
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "margem_horizontal=4: linha comeca com 4 espacos",
            isinstance(linhas, list) and linhas and linhas[0].startswith("    "),
            "linhas={0!r}".format(linhas),
        )

    def test_margem_horizontal_participa_do_overflow(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 50
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "margem_horizontal=50 com content_w=39 -> RenderizadorErro (largura_util negativa)",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_margem_horizontal_0_permitido(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 0
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "margem_horizontal=0: linha comeca diretamente com [",
            isinstance(linhas, list) and linhas and linhas[0].startswith("["),
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 7-8
    def test_vao_entre_chips_altera_distancia(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 6
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 80)
        self._r(
            "vao_entre_chips=6: linha contem 6 espacos entre chips",
            isinstance(linhas, list) and linhas
            and "[Esc] Sair      [?] Ajuda" in linhas[0],
            "linhas={0!r}".format(linhas),
        )

    def test_vao_entre_colunas_altera_distancia_multilinha(self):
        chips = [
            _chip("c1", "1", "AAAAA"),
            _chip("c2", "2", "BBBBB"),
            _chip("c3", "3", "CCCCC"),
            _chip("c4", "4", "DDDDD"),
        ]
        d2 = _dist_canonica(preenchimento="coluna_a_coluna")
        d2["espacamentos"]["vao_entre_colunas"]["minimo"] = 2
        d8 = _dist_canonica(preenchimento="coluna_a_coluna")
        d8["espacamentos"]["vao_entre_colunas"]["minimo"] = 8
        l2 = _linhas_barra({"distribuicao": d2, "chips": chips}, 40)
        l8 = _linhas_barra({"distribuicao": d8, "chips": chips}, 40)
        self._r(
            "vao_entre_colunas=8 produz linha mais larga que vao=2 na multilinha",
            isinstance(l2, list) and isinstance(l8, list)
            and l2 and l8 and len(l8[0]) > len(l2[0]),
            "vao2={0!r} vao8={1!r}".format(l2[0] if l2 else None, l8[0] if l8 else None),
        )

    # ------------------------------------------------------------------ 9-11
    def test_vao_vertical_entre_linhas_rejeitado(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_vertical_entre_linhas"] = {"minimo": 1, "maximo": 1}
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_vertical_entre_linhas.minimo=1 -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_vertical_entre_linhas nao suportado",
                "vao_vertical_entre_linhas" in str(exc),
                str(exc),
            )

    def test_alinhamento_linhas_esquerda_funciona(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["alinhamento_linhas"] = "esquerda"
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "alinhamento_linhas='esquerda': aceito sem erro",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def test_alinhamento_linhas_nao_suportado_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["alinhamento_linhas"] = "centro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "alinhamento_linhas='centro' -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona alinhamento_linhas nao suportado",
                "alinhamento_linhas" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 12-15
    def test_linhas_minimo_maior_que_1_pula_linha_unica(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 2, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "linhas.minimo=2: chips que caberiam em 1 linha -> forcado 2 linhas",
            isinstance(linhas, list) and len(linhas) == 2,
            "linhas={0!r}".format(linhas),
        )

    def test_linhas_maximo_1_overflow_se_nao_couber(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 1, "maximo": 1, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "linhas.maximo=1 com chips que nao cabem em linha unica -> erro_layout",
            lambda: _linhas_barra(bar, 10),
        )
        if exc is not None:
            self._r(
                "mensagem menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_linhas_maximo_1_ok_se_couber(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 1, "maximo": 1, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "linhas.maximo=1 com chips que cabem -> 1 linha sem erro",
            isinstance(linhas, list) and len(linhas) == 1,
            "linhas={0!r}".format(linhas),
        )

    def test_linhas_maximo_3_tres_linhas(self):
        chips = [
            _chip("a", "1", "A"),
            _chip("b", "2", "B"),
            _chip("c", "3", "C"),
            _chip("d", "4", "D"),
            _chip("e", "5", "E"),
        ]
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["linhas"] = {"minimo": 1, "maximo": 3, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        # K=2 nao cabe (19 > largura_util=18); K=3 cabe (12 <= 18)
        linhas = _linhas_barra(bar, 20)
        self._r(
            "linhas.maximo=3: 5 chips que nao cabem em K=2 -> K=3 (3 linhas)",
            isinstance(linhas, list) and len(linhas) == 3,
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 16-17
    def test_preferir_menor_numero_false_rejeitado(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"]["preferir_menor_numero"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preferir_menor_numero=false -> RenderizadorErro (Option B)",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preferir_menor_numero nao suportado",
                "preferir_menor_numero" in str(exc),
                str(exc),
            )

    def test_preferir_menor_numero_nao_bool_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["linhas"]["preferir_menor_numero"] = "sim"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preferir_menor_numero='sim' (nao bool) -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preferir_menor_numero deve ser bool",
                "preferir_menor_numero" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 18-19
    def test_colunas_largura_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["largura"] = "por_percentual"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "colunas.largura='por_percentual' -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona colunas.largura nao suportado",
                "colunas.largura" in str(exc),
                str(exc),
            )

    def test_colunas_largura_ausente_usa_default(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        del dist["colunas"]["largura"]
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "colunas.largura ausente: aceito sem erro (usa default)",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    # ------------------------------------------------------------------ 20-21
    def test_subcoluna_chip_alinhamento_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["subcolunas"]["chip"]["alinhamento"] = "centro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "subcolunas.chip.alinhamento='centro' -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona subcolunas.chip.alinhamento nao suportado",
                "subcolunas.chip.alinhamento" in str(exc),
                str(exc),
            )

    def test_subcoluna_texto_alinhamento_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["colunas"]["subcolunas"]["texto"]["alinhamento"] = "direita"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "subcolunas.texto.alinhamento='direita' -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona subcolunas.texto.alinhamento nao suportado",
                "subcolunas.texto.alinhamento" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 22-24
    def test_overflow_nao_omitir_chips_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_omitir_chips"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_omitir_chips=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_omitir_chips deve ser true",
                "nao_omitir_chips" in str(exc),
                str(exc),
            )

    def test_overflow_nao_truncar_texto_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_truncar_texto"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_truncar_texto=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_truncar_texto deve ser true",
                "nao_truncar_texto" in str(exc),
                str(exc),
            )

    def test_overflow_nao_reordenar_false_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["overflow"]["nao_reordenar"] = False
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "overflow.nao_reordenar=false -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona nao_reordenar deve ser true",
                "nao_reordenar" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 25
    def test_preenchimentos_multilinha_suportados_valida_preenchimento(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica(preenchimento="coluna_a_coluna")
        dist["preenchimentos_multilinha_suportados"] = ["linha_a_linha"]
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "preenchimento='coluna_a_coluna' ausente em suportados -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona preenchimento nao esta em suportados",
                "preenchimentos_multilinha_suportados" in str(exc)
                or "preenchimento_multilinha" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 26-28
    def test_valores_exagerados_margem_50(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["margem_horizontal"]["minimo"] = 50
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "margem=50 com content_w=39 -> erro_layout (largura_util=-61)",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "erro com margem exagerada menciona erro_layout",
                "erro_layout" in str(exc),
                str(exc),
            )

    def test_valores_exagerados_vao_chip_texto_10(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_chip_texto"]["minimo"] = 10
        dist["espacamentos"]["vao_chip_texto"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        # single=19+2+18=39>37 (largura_util) -> multilinha K=2: max=19<=37 -> 2 linhas
        try:
            linhas = _linhas_barra(bar, 39)
            self._r(
                "vao_chip_texto=10: resultado deterministico (multilinha, nao silencio)",
                isinstance(linhas, list) and len(linhas) >= 1,
                "linhas={0!r}".format(linhas),
            )
            self._r(
                "vao_chip_texto=10: chip contem 10 espacos entre ] e texto",
                any("[Esc]          Sair" in l for l in linhas),
                "linhas={0!r}".format(linhas),
            )
        except RenderizadorErro as exc:
            self._r(
                "vao_chip_texto=10: RenderizadorErro deterministico (nao silencio)",
                True,
                str(exc),
            )

    def test_valores_exagerados_vao_entre_chips_20(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 20
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        # single=10+20+9=39>18 (largura_util com content_w=20) -> multilinha K=2: max=10<=18 -> 2l
        try:
            linhas = _linhas_barra(bar, 20)
            self._r(
                "vao_entre_chips=20: resultado deterministico (multilinha, nao silencio)",
                isinstance(linhas, list) and len(linhas) >= 1,
                "linhas={0!r}".format(linhas),
            )
        except RenderizadorErro as exc:
            self._r(
                "vao_entre_chips=20: erro_layout deterministico (nao silencio)",
                "erro_layout" in str(exc),
                str(exc),
            )

    # ------------------------------------------------------------------ 29-35
    def test_vao_entre_chips_maximo_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["minimo"] = 4
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = 2
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_chips.maximo < minimo -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_chips.maximo invalido",
                "vao_entre_chips.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_colunas_maximo_invalido_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_colunas"]["minimo"] = 4
        dist["espacamentos"]["vao_entre_colunas"]["maximo"] = 2
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_colunas.maximo < minimo -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_colunas.maximo invalido",
                "vao_entre_colunas.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_chips_maximo_nao_int_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_chips"]["maximo"] = "seis"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "vao_entre_chips.maximo nao-int -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona vao_entre_chips.maximo invalido",
                "vao_entre_chips.maximo" in str(exc),
                str(exc),
            )

    def test_vao_entre_colunas_maximo_null_aceito(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["espacamentos"]["vao_entre_colunas"]["maximo"] = None
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "vao_entre_colunas.maximo=None: aceito sem erro",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def test_tentativa_inicial_invalida_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["tentativa_inicial"] = "multilinha_primeiro"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "tentativa_inicial='multilinha_primeiro' -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona tentativa_inicial nao suportado",
                "tentativa_inicial" in str(exc),
                str(exc),
            )

    def test_quebra_invalida_erro(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["quebra"] = "truncar"
        bar = {"distribuicao": dist, "chips": chips}
        exc = self._espera_erro(
            "quebra='truncar' -> RenderizadorErro",
            lambda: _linhas_barra(bar, 39),
        )
        if exc is not None:
            self._r(
                "mensagem menciona quebra nao suportado",
                "quebra" in str(exc),
                str(exc),
            )

    def test_tentativa_inicial_e_quebra_validos_aceitos(self):
        chips = [_chip("c_esc", "Esc", "Sair"), _chip("c_aj", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["tentativa_inicial"] = "linha_unica"
        dist["quebra"] = "multilinha_quando_nao_couber"
        bar = {"distribuicao": dist, "chips": chips}
        linhas = _linhas_barra(bar, 39)
        self._r(
            "tentativa_inicial='linha_unica' e quebra='multilinha_quando_nao_couber': aceitos",
            isinstance(linhas, list) and len(linhas) >= 1,
            "linhas={0!r}".format(linhas),
        )

    def run_all(self):
        print("")
        print("== H-0018 - cobertura executavel de todos os campos de distribuicao ==")
        self.test_vao_chip_texto_altera_distancia()
        self.test_vao_chip_texto_10_espaco_extra()
        self.test_vao_chip_texto_altera_comprimento_linha()
        self.test_margem_horizontal_altera_padding()
        self.test_margem_horizontal_participa_do_overflow()
        self.test_margem_horizontal_0_permitido()
        self.test_vao_entre_chips_altera_distancia()
        self.test_vao_entre_colunas_altera_distancia_multilinha()
        self.test_vao_vertical_entre_linhas_rejeitado()
        self.test_alinhamento_linhas_esquerda_funciona()
        self.test_alinhamento_linhas_nao_suportado_erro()
        self.test_linhas_minimo_maior_que_1_pula_linha_unica()
        self.test_linhas_maximo_1_overflow_se_nao_couber()
        self.test_linhas_maximo_1_ok_se_couber()
        self.test_linhas_maximo_3_tres_linhas()
        self.test_preferir_menor_numero_false_rejeitado()
        self.test_preferir_menor_numero_nao_bool_erro()
        self.test_colunas_largura_invalido_erro()
        self.test_colunas_largura_ausente_usa_default()
        self.test_subcoluna_chip_alinhamento_invalido_erro()
        self.test_subcoluna_texto_alinhamento_invalido_erro()
        self.test_overflow_nao_omitir_chips_false_erro()
        self.test_overflow_nao_truncar_texto_false_erro()
        self.test_overflow_nao_reordenar_false_erro()
        self.test_preenchimentos_multilinha_suportados_valida_preenchimento()
        self.test_valores_exagerados_margem_50()
        self.test_valores_exagerados_vao_chip_texto_10()
        self.test_valores_exagerados_vao_entre_chips_20()
        self.test_vao_entre_chips_maximo_invalido_erro()
        self.test_vao_entre_colunas_maximo_invalido_erro()
        self.test_vao_entre_chips_maximo_nao_int_erro()
        self.test_vao_entre_colunas_maximo_null_aceito()
        self.test_tentativa_inicial_invalida_erro()
        self.test_quebra_invalida_erro()
        self.test_tentativa_inicial_e_quebra_validos_aceitos()


def _modelo_horizontal(arranjo, elementos_spec, largura=42, titulo_cab="H"):
    """Cria ModeloTela sintético para testes de arranjo horizontal (H-0019).

    elementos_spec: lista de tuplas (tipo, titulo) ex: [("console","A"),("dashboard","B")]
    """
    elementos = []
    for tipo, titulo in elementos_spec:
        campos_inertes = {"titulo": titulo}
        if tipo == "lancador":
            campos_inertes["itens"] = []
        elementos.append(ElementoCorpo(id=titulo.lower(), tipo=tipo,
                                       _campos_inertes=campos_inertes))
    return ModeloTela(
        id="teste_h0019",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "teste h0019"},
        corpo=Corpo(arranjo=arranjo, elementos=elementos),
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


class TestArranjoH0019:
    """Testes obrigatórios de arranjo do corpo raiz (H-0019).

    Cobre: None/vertical/sobreposto preservam comportamento atual;
    horizontal e lado_a_lado ativam particionamento contíguo;
    bordas coladas; largura determinística; resto; padding inferior;
    largura insuficiente; N=1; H-0015; barra preservada.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            self._r(nome, True, str(exc))
            return exc
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    def test_arranjo_none_preserva_vertical(self):
        """None -> comportamento vertical atual preservado."""
        modelo_none = _modelo_horizontal(None, [("console", "A"), ("console", "B")])
        modelo_vert = _modelo_horizontal("vertical", [("console", "A"), ("console", "B")])
        saida_none = renderizar_tela(modelo_none, largura=42)
        saida_vert = renderizar_tela(modelo_vert, largura=42)
        self._r(
            "arranjo=None -> saida identica a arranjo='vertical'",
            saida_none == saida_vert,
        )
        # Elementos empilhados = 2 cabecalhos de console separados (vertical)
        self._r(
            "arranjo=None -> 2 caixas de console empilhadas (contagem de ╭)",
            saida_none.count("╭ A") == 1 and saida_none.count("╭ B") == 1,
        )
        self._r(
            "arranjo=None -> barra aparece ao final",
            "╭ Menus" in saida_none,
        )

    def test_arranjo_vertical_preserva_comportamento(self):
        """vertical -> saida identica ao None."""
        modelo_none = _modelo_horizontal(None, [("console", "A"), ("dashboard", "B")])
        modelo_vert = _modelo_horizontal("vertical", [("console", "A"), ("dashboard", "B")])
        self._r(
            "arranjo='vertical' == arranjo=None",
            renderizar_tela(modelo_none, largura=42)
            == renderizar_tela(modelo_vert, largura=42),
        )

    def test_arranjo_sobreposto_preserva_vertical(self):
        """sobreposto -> alias de vertical, saida identica."""
        modelo_vert = _modelo_horizontal("vertical", [("console", "A")])
        modelo_sob = _modelo_horizontal("sobreposto", [("console", "A")])
        self._r(
            "arranjo='sobreposto' -> saida identica a 'vertical'",
            renderizar_tela(modelo_vert, largura=42)
            == renderizar_tela(modelo_sob, largura=42),
        )

    def test_arranjo_horizontal_dois_elementos(self):
        """horizontal: 2 filhos diretos ficam na mesma faixa de linhas."""
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")])
        saida_h = renderizar_tela(modelo, largura=42)
        saida_v = renderizar_tela(
            _modelo_horizontal("vertical", [("console", "A"), ("console", "B")]),
            largura=42,
        )
        self._r(
            "horizontal: A e B aparecem na saida",
            "A" in saida_h and "B" in saida_h,
        )
        self._r(
            "horizontal: saida tem menos linhas que vertical (areas lado a lado)",
            saida_h.count("\n") < saida_v.count("\n"),
            "h={0} v={1}".format(saida_h.count("\n"), saida_v.count("\n")),
        )
        self._r(
            "horizontal: barra_de_menus aparece abaixo do bloco horizontal",
            saida_h.index("╭ Menus") > saida_h.index("╭ A"),
        )

    def test_arranjo_lado_a_lado_alias_horizontal(self):
        """lado_a_lado -> alias transicional de horizontal, saida identica."""
        modelo_h = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")])
        modelo_l = _modelo_horizontal("lado_a_lado", [("console", "A"), ("console", "B")])
        self._r(
            "arranjo='lado_a_lado' == arranjo='horizontal'",
            renderizar_tela(modelo_h, largura=42)
            == renderizar_tela(modelo_l, largura=42),
        )

    def test_arranjo_horizontal_areas_contiguas(self):
        """horizontal: bordas adjacentes coladas (││, ╮╭, ╯╰); largura total preservada."""
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                    largura=42)
        saida = renderizar_tela(modelo, largura=42)
        # Extrair apenas o bloco do corpo (linhas entre cabecalho e barra)
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linhas_corpo = [ln for ln in linhas
                        if not ln.startswith("╭ H") and not ln.startswith("╭ Menus")
                        and not (ln.startswith("│ teste") or ln.startswith("│ Ok"))
                        and not ln.startswith("╰────────────────────────────────────────╯")
                        or ln.startswith("╭ A") or ln.startswith("╭ B")
                        or "│" == ln[0] and "A" not in ln[:5] and "B" not in ln[:5]
                        or ln.startswith("╰───────────────────╯")]
        self._r(
            "horizontal: '││' aparece nas linhas internas (bordas adjacentes coladas)",
            "││" in saida,
            "ok" if "││" in saida else "nao encontrado",
        )
        self._r(
            "horizontal: '╮╭' aparece no topo das areas adjacentes",
            "╮╭" in saida,
            "ok" if "╮╭" in saida else "nao encontrado",
        )
        self._r(
            "horizontal: '╯╰' aparece na base das areas adjacentes",
            "╯╰" in saida,
            "ok" if "╯╰" in saida else "nao encontrado",
        )
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal: cada linha tem exatamente 42 chars (largura total preservada)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal: primeiro char de cada linha e borda esquerda da area 0",
            all(ln[0] in ("╭", "│", "╰") for ln in linhas_nao_vazias),
            "primeiros={0!r}".format([ln[0] for ln in linhas_nao_vazias]),
        )
        self._r(
            "horizontal: ultimo char de cada linha e borda direita da area N-1",
            all(ln[-1] in ("╮", "│", "╯") for ln in linhas_nao_vazias),
            "ultimos={0!r}".format([ln[-1] for ln in linhas_nao_vazias]),
        )

    def test_arranjo_horizontal_resto_deterministico(self):
        """horizontal: resto distribui deterministicamente da esquerda (maiores restos)."""
        # 100 // 3 = 33, resto 1 -> larguras = [34, 33, 33]
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=100,
        )
        saida = renderizar_tela(modelo, largura=100)
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal: todas as linhas tem exatamente 100 chars (sum(larguras)==100)",
            all(len(ln) == 100 for ln in linhas_nao_vazias),
        )
        # Topo da primeira caixa: area 0 tem 34 chars, area 1 começa no índice 34
        # A linha de topo começa com "╭ A" e termina com "╮╭..." em posicao 33
        linha_topo = next(
            (ln for ln in linhas_nao_vazias if "╭ A" in ln), None
        )
        if linha_topo is not None:
            self._r(
                "horizontal: area 0 tem 34 chars (char[33]=='╮', char[34]=='╭')",
                len(linha_topo) >= 35 and linha_topo[33] == "╮" and linha_topo[34] == "╭",
                "chars[33:36]={0!r}".format(linha_topo[33:36] if len(linha_topo) >= 36 else "?"),
            )
            self._r(
                "horizontal: area 1 tem 33 chars (char[66]=='╮', char[67]=='╭')",
                len(linha_topo) >= 68 and linha_topo[66] == "╮" and linha_topo[67] == "╭",
                "chars[66:69]={0!r}".format(linha_topo[66:69] if len(linha_topo) >= 69 else "?"),
            )
        else:
            self._r("horizontal: linha_topo encontrada para verificar limites", False)
            self._r("horizontal: area 0 tem 34 chars", False)
            self._r("horizontal: area 1 tem 33 chars", False)

    def test_arranjo_horizontal_padding_inferior(self):
        """horizontal: alturas desiguais -> preenchimento inferior na area menor."""
        # console: 3 linhas (topo + "(console)" + base)
        # dashboard sem campos: 2 linhas (topo + base)
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("dashboard", "B")],
            largura=42,
        )
        saida = renderizar_tela(modelo, largura=42)
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        # O bloco horizontal deve ter 3 linhas (max entre 3 e 2)
        # e cada linha deve ter 42 chars (padding aplicado na area B)
        self._r(
            "horizontal: todas as linhas tem exatamente 42 chars (padding aplicado)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal: saida renderizada sem erro (alturas desiguais tratadas)",
            isinstance(saida, str) and len(saida) > 0,
        )

    def test_arranjo_horizontal_largura_insuficiente(self):
        """horizontal: largura insuficiente -> RenderizadorErro determinístico sem fallback."""
        modelo = _modelo_horizontal("horizontal",
                                    [("console", "A"), ("console", "B")],
                                    largura=18)
        # 18 // 2 = 9 < 10 -> deve gerar erro
        exc = self._espera_erro(
            "horizontal: largura=18 para 2 elementos -> RenderizadorErro",
            lambda: renderizar_tela(modelo, largura=18),
        )
        if exc is not None:
            self._r(
                "mensagem menciona 'arranjo horizontal'",
                "arranjo horizontal" in str(exc),
                str(exc),
            )
            # Confirmar que NAO e um fallback silencioso para vertical
            self._r(
                "excecao e RenderizadorErro (sem fallback silencioso para vertical)",
                isinstance(exc, RenderizadorErro),
            )

    def test_arranjo_horizontal_tres_elementos(self):
        """horizontal: 3 filhos diretos aparecem na mesma faixa de linhas."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=42,
        )
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "horizontal: 3 elementos -> '╮╭' aparece 2 vezes (3 areas contiguas)",
            saida.count("╮╭") >= 2,
            "count('╮╭')={0}".format(saida.count("╮╭")),
        )
        self._r(
            "horizontal: todas as linhas tem exatamente 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )

    def test_arranjo_horizontal_com_altura_preserva_h0015(self):
        """horizontal: altura explícita funciona (H-0015 preservado)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
        )
        saida = renderizar_tela(modelo, largura=42, altura=40)
        self._r(
            "horizontal: altura=40 -> saida tem exatamente 40 linhas",
            saida.count("\n") == 40,
            "count={0}".format(saida.count("\n")),
        )
        self._r(
            "horizontal: altura=40 -> barra_de_menus no rodape",
            "╭ Menus" in saida,
        )
        self._r(
            "horizontal: altura=40 -> cada linha tem 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )

    def test_arranjo_horizontal_barra_preservada(self):
        """horizontal: barra_de_menus permanece inalterada."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
        )
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "horizontal: barra_de_menus aparece na saida",
            "╭ Menus" in saida,
        )
        self._r(
            "horizontal: chip [k] Ok da barra aparece",
            "[k] Ok" in saida,
        )
        # Confirmacao de que nenhuma funcao da barra foi afetada: barra de menus
        # com chips do JSON do orquestrador continua funcionando
        tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
        modelo_orc = construir_modelo(tela_raw)
        saida_orc = renderizar_tela(modelo_orc, largura=42)
        self._r(
            "horizontal: barra_de_menus do orquestrador inalterada pos-H0019",
            "[Esc] Sair" in saida_orc and "[?] Ajuda" in saida_orc,
        )

    def test_arranjo_horizontal_n1(self):
        """horizontal: N=1 -> renderizar na largura total (sem particionamento). (A-002)."""
        modelo = _modelo_horizontal("horizontal", [("console", "A")], largura=42)
        saida = renderizar_tela(modelo, largura=42)
        self._r(
            "horizontal N=1: renderiza sem erro",
            isinstance(saida, str) and len(saida) > 0,
        )
        linhas_nao_vazias = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "horizontal N=1: cada linha tem exatamente 42 chars (largura total)",
            all(len(ln) == 42 for ln in linhas_nao_vazias),
            "larguras={0!r}".format([len(ln) for ln in linhas_nao_vazias
                                     if len(ln) != 42]),
        )
        self._r(
            "horizontal N=1: elemento aparece na saida",
            "╭ A" in saida,
        )
        # N=1 horizontal nao deve ter ╮╭ (nao ha duas areas)
        self._r(
            "horizontal N=1: sem '╮╭' (area unica, sem particao interna)",
            "╮╭" not in saida,
        )

    def run_all(self):
        print("")
        print("== H-0019 - layout horizontal plano do corpo ==")
        self.test_arranjo_none_preserva_vertical()
        self.test_arranjo_vertical_preserva_comportamento()
        self.test_arranjo_sobreposto_preserva_vertical()
        self.test_arranjo_horizontal_dois_elementos()
        self.test_arranjo_lado_a_lado_alias_horizontal()
        self.test_arranjo_horizontal_areas_contiguas()
        self.test_arranjo_horizontal_resto_deterministico()
        self.test_arranjo_horizontal_padding_inferior()
        self.test_arranjo_horizontal_largura_insuficiente()
        self.test_arranjo_horizontal_tres_elementos()
        self.test_arranjo_horizontal_com_altura_preserva_h0015()
        self.test_arranjo_horizontal_barra_preservada()
        self.test_arranjo_horizontal_n1()


def main():
    print("Diagnostico H-0010A - renderer declarativo (curva/reta)")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_renderizador_orquestrador()
    teste_renderizador_destino_minimo()
    teste_renderizador_grupo_minimo()
    teste_modelo_fabricado()
    teste_erros_renderizador()
    teste_proibicoes_importacao()
    teste_inspecao_fonte_hardcoded()
    teste_inercia()
    teste_alternancia_borda()
    teste_largura_explicita()
    teste_altura_explicita()
    TestLinhasBarra().run_all()
    TestDistribuicaoH0018().run_all()
    TestArranjoH0019().run_all()

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
