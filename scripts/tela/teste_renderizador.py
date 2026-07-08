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
- largura explicita (H-0009).

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
    "╭ ITENS ─────────────────────────────────╮\n"
    "│ (console)                              │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ INFO ──────────────────────────────────╮\n"
    "╰────────────────────────────────────────╯\n"
    "╭ NAVEGAR ───────────────────────────────╮\n"
    "│ [d] Destino                            │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menus ─────────────────────────────────╮\n"
    "│ [Esc] Sair                             │\n"
    "│ [<>] Páginas                           │\n"
    "│ [-+] Colunas                           │\n"
    "│ [#] Grupos                             │\n"
    "│ [⇆] Alternar                           │\n"
    "│ [✥] Navegar                            │\n"
    "│ [␣] Selecionar                         │\n"
    "│ [⏎] Todos                              │\n"
    "│ [|] Estilo                             │\n"
    "│ [V] Verboso                            │\n"
    "│ [?] Ajuda                              │\n"
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
    "└────────────────────────────────────────┘\n"
    "┌ Menus ─────────────────────────────────┐\n"
    "│ [Esc] Sair                             │\n"
    "│ [<>] Páginas                           │\n"
    "│ [-+] Colunas                           │\n"
    "│ [#] Grupos                             │\n"
    "│ [⇆] Alternar                           │\n"
    "│ [✥] Navegar                            │\n"
    "│ [␣] Selecionar                         │\n"
    "│ [⏎] Todos                              │\n"
    "│ [|] Estilo                             │\n"
    "│ [V] Verboso                            │\n"
    "│ [?] Ajuda                              │\n"
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
        "saida contem '[<>] Páginas' (chip do JSON)",
        "[<>] Páginas" in saida,
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


def main():
    print("Diagnostico H-0010A - renderer declarativo (curva/reta)")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_renderizador_orquestrador()
    teste_renderizador_destino_minimo()
    teste_modelo_fabricado()
    teste_erros_renderizador()
    teste_proibicoes_importacao()
    teste_inspecao_fonte_hardcoded()
    teste_inercia()
    teste_alternancia_borda()
    teste_largura_explicita()

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
