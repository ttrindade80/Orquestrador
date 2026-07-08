"""Diagnostico da aplicacao demonstravel H-0008/H-0009/H-0010A (tela/demo.py).

Executavel via:
    python tela/teste_demo.py

Cobre os criterios de aceite testaveis dos handoffs H-0008, H-0009 e
H-0010A (navegacao minima com tela destino).

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
- "\x1b" (Esc) define saindo == True sem alterar tipo_borda (H-0009);
- "\x1b" nao altera tipo_borda (curva nem reta) (H-0009);
- processar_comando nao modifica o dict original com "\x1b" (H-0009);
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
- renderizar_estado nao altera modelo;
- renderizar_estado(..., largura=42) bate com _EXPECTED_* (H-0009);
- renderizar_estado(..., largura=60) produz linhas de 60 chars (H-0009);
- renderizar_estado(..., largura=None) equivale a omitir largura (H-0009).

Secao 4 - Integracao via subprocess (demo completo):
- python tela/demo.py com input "b\ns\n" encerra com codigo 0;
- stdout contem render curva inicial;
- stdout contem render reta apos "b";
- stdout nao contem "\n\n" entre caixas (H-0009);
- stdout bate com renderizar_tela(..., largura=80) curva+reta (H-0009);
- stderr vazio;
- config/telas/orquestrador.json inalterado apos demo;
- subprocess com "b\n\x1b\n" encerra 0 e sai identico a "b\ns\n" (H-0009).

Secao 5 - Preservacao do diagnostico:
- gerar_diagnostico_tela() nao lanca excecao;
- retorno de gerar_diagnostico_tela() e str;
- retorno bate com _EXPECTED_CURVA (default curva H-0006/H-0007, sem "\n\n");
- python tela/diagnostico.py encerra com codigo 0;
- stdout de diagnostico.py bate com _EXPECTED_CURVA;
- diagnostico.py nao contem sys.stdin;
- diagnostico.py nao contem input(.

Secao 6 - Inspecao de codigo para modo sem echo (H-0009):
- demo.py contem termios, tty, shutil.get_terminal_size, isatty;
- demo.py nao contem input(, curses, textual, rich.

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
import os  # noqa: E402

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


_LARGURA_SUBPROCESS = 80


_EXPECTED_CURVA = (
    "╭ ORQUESTRADOR ────────────────────────────────────────────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de su│\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ ITENS ───────────────────────────────────────────────────────────────────────╮\n"
    "│ (console)                                                                    │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ INFO ────────────────────────────────────────────────────────────────────────╮\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ NAVEGAR ─────────────────────────────────────────────────────────────────────╮\n"
    "│ [d] Destino                                                                  │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ Menus ───────────────────────────────────────────────────────────────────────╮\n"
    "│ [Esc] Sair                                                                   │\n"
    "│ [<>] Páginas                                                                 │\n"
    "│ [-+] Colunas                                                                 │\n"
    "│ [#] Grupos                                                                   │\n"
    "│ [⇆] Alternar                                                                 │\n"
    "│ [✥] Navegar                                                                  │\n"
    "│ [␣] Selecionar                                                               │\n"
    "│ [⏎] Todos                                                                    │\n"
    "│ [|] Estilo                                                                   │\n"
    "│ [V] Verboso                                                                  │\n"
    "│ [?] Ajuda                                                                    │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
)

_EXPECTED_RETA = (
    "┌ ORQUESTRADOR ────────────────────────────────────────────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de su│\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ ITENS ───────────────────────────────────────────────────────────────────────┐\n"
    "│ (console)                                                                    │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ INFO ────────────────────────────────────────────────────────────────────────┐\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ NAVEGAR ─────────────────────────────────────────────────────────────────────┐\n"
    "│ [d] Destino                                                                  │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ Menus ───────────────────────────────────────────────────────────────────────┐\n"
    "│ [Esc] Sair                                                                   │\n"
    "│ [<>] Páginas                                                                 │\n"
    "│ [-+] Colunas                                                                 │\n"
    "│ [#] Grupos                                                                   │\n"
    "│ [⇆] Alternar                                                                 │\n"
    "│ [✥] Navegar                                                                  │\n"
    "│ [␣] Selecionar                                                               │\n"
    "│ [⏎] Todos                                                                    │\n"
    "│ [|] Estilo                                                                   │\n"
    "│ [V] Verboso                                                                  │\n"
    "│ [?] Ajuda                                                                    │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
)


_EXPECTED_DIAGNOSTICO_CURVA_42 = (
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


_EXPECTED_DESTINO_MINIMO_CURVA_80 = (
    "╭ DESTINO MINIMO ──────────────────────────────────────────────────────────────╮\n"
    "│ Tela de destino para teste do lancador                                       │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ TESTE ───────────────────────────────────────────────────────────────────────╮\n"
    "│ Tela de destino para teste do lancador                                       │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ Menus ───────────────────────────────────────────────────────────────────────╮\n"
    "│ [Esc] Voltar                                                                 │\n"
    "│ [?] Ajuda                                                                    │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
)


_EXPECTED_DESTINO_MINIMO_RETA_80 = (
    "┌ DESTINO MINIMO ──────────────────────────────────────────────────────────────┐\n"
    "│ Tela de destino para teste do lancador                                       │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ TESTE ───────────────────────────────────────────────────────────────────────┐\n"
    "│ Tela de destino para teste do lancador                                       │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ Menus ───────────────────────────────────────────────────────────────────────┐\n"
    "│ [Esc] Voltar                                                                 │\n"
    "│ [?] Ajuda                                                                    │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
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


def _carregar_modelo_por_id(id_tela):
    tela_raw = carregar_tela(_BASE_PADRAO, id_tela)
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
        "estado inicial tem tela_atual == 'orquestrador' (H-0010A)",
        est.get("tela_atual") == "orquestrador",
        "tela_atual={0!r}".format(est.get("tela_atual")),
    )
    _registrar(
        "estado inicial tem pilha_telas == [] (H-0010A)",
        est.get("pilha_telas") == [],
        "pilha_telas={0!r}".format(est.get("pilha_telas")),
    )
    _registrar(
        "duas chamadas retornam dicts independentes",
        criar_estado_inicial() is not criar_estado_inicial(),
    )


def teste_processar_comando():
    print("")
    print("== Secao 2 - processar_comando ==")

    base = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}

    _registrar(
        "'b' sobre curva -> tipo_borda == 'reta'",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "b")["tipo_borda"] == "reta",
    )
    _registrar(
        "'b' sobre reta -> tipo_borda == 'curva'",
        processar_comando({"tipo_borda": "reta", "saindo": False, "pilha_telas": []}, "b")["tipo_borda"] == "curva",
    )
    _registrar(
        "'b' nao altera saindo",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "b")["saindo"] is False,
    )
    _registrar(
        "'s' define saindo == True",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "s")["saindo"] is True,
    )
    _registrar(
        "'s' nao altera tipo_borda (curva preservado)",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "s")["tipo_borda"] == "curva",
    )
    _registrar(
        "'s' sobre reta preserva tipo_borda == 'reta'",
        processar_comando({"tipo_borda": "reta", "saindo": False, "pilha_telas": []}, "s")["tipo_borda"] == "reta",
    )

    _registrar(
        "'\\x1b' (Esc) define saindo == True",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "\x1b")["saindo"] is True,
    )
    _registrar(
        "'\\x1b' nao altera tipo_borda (curva preservado)",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "\x1b")["tipo_borda"] == "curva",
    )
    _registrar(
        "'\\x1b' nao altera tipo_borda (reta preservado)",
        processar_comando({"tipo_borda": "reta", "saindo": False, "pilha_telas": []}, "\x1b")["tipo_borda"] == "reta",
    )

    estado_original_esc = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    processar_comando(estado_original_esc, "\x1b")
    _registrar(
        "processar_comando nao modifica o dict original com '\\x1b'",
        estado_original_esc["tipo_borda"] == "curva"
        and estado_original_esc["saindo"] is False,
        "estado apos chamada={0!r}".format(estado_original_esc),
    )

    res_x = processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "x")
    _registrar(
        "comando desconhecido 'x' nao altera tipo_borda",
        res_x["tipo_borda"] == "curva",
    )
    _registrar(
        "comando desconhecido 'x' nao altera saindo",
        res_x["saindo"] is False,
    )

    res_vazio = processar_comando({"tipo_borda": "reta", "saindo": True, "pilha_telas": []}, "")
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
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "B")["tipo_borda"] == "curva",
    )
    _registrar(
        "'S' (maiusculo) nao altera saindo",
        processar_comando({"tipo_borda": "curva", "saindo": False, "pilha_telas": []}, "S")["saindo"] is False,
    )

    estado_original = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    processar_comando(estado_original, "b")
    _registrar(
        "processar_comando nao modifica o dict original com 'b'",
        estado_original["tipo_borda"] == "curva" and estado_original["saindo"] is False,
        "estado apos chamada={0!r}".format(estado_original),
    )

    estado_original_s = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
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


def teste_navegacao_minima(modelo):
    print("")
    print("== Secao 2b - Navegacao minima (H-0010A) ==")

    estado_raiz = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "orquestrador",
        "pilha_telas": [],
    }

    res_d = processar_comando(estado_raiz, "d", modelo)
    _registrar(
        "chip 'd' muda tela_atual para 'destino_minimo'",
        res_d["tela_atual"] == "destino_minimo",
        "tela_atual={0!r}".format(res_d.get("tela_atual")),
    )
    _registrar(
        "chip 'd' empilha 'orquestrador' em pilha_telas",
        res_d["pilha_telas"] == ["orquestrador"],
        "pilha_telas={0!r}".format(res_d.get("pilha_telas")),
    )
    _registrar(
        "chip 'd' nao altera tipo_borda nem saindo",
        res_d["tipo_borda"] == "curva" and res_d["saindo"] is False,
    )

    estado_interno = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "destino_minimo",
        "pilha_telas": ["orquestrador"],
    }
    res_esc_volta = processar_comando(estado_interno, "\x1b")
    _registrar(
        "Esc em tela interna volta para 'orquestrador' (pop pilha)",
        res_esc_volta["tela_atual"] == "orquestrador"
        and res_esc_volta["pilha_telas"] == [],
        "tela_atual={0!r} pilha={1!r}".format(
            res_esc_volta.get("tela_atual"), res_esc_volta.get("pilha_telas")
        ),
    )
    _registrar(
        "Esc em tela interna NAO define saindo == True",
        res_esc_volta["saindo"] is False,
    )

    res_s_volta = processar_comando(estado_interno, "s")
    _registrar(
        "'s' em tela interna tambem volta (atalho de Esc)",
        res_s_volta["tela_atual"] == "orquestrador"
        and res_s_volta["pilha_telas"] == []
        and res_s_volta["saindo"] is False,
    )

    res_esc_raiz = processar_comando(estado_raiz, "\x1b")
    _registrar(
        "Esc na raiz (pilha vazia) define saindo == True",
        res_esc_raiz["saindo"] is True,
    )
    _registrar(
        "Esc na raiz nao altera tela_atual",
        res_esc_raiz["tela_atual"] == "orquestrador",
    )
    _registrar(
        "Esc na raiz mantem pilha_telas vazia",
        res_esc_raiz["pilha_telas"] == [],
    )

    res_chip_desconhecido = processar_comando(estado_raiz, "z", modelo)
    _registrar(
        "chip nao declarado ('z') nao altera tela_atual",
        res_chip_desconhecido["tela_atual"] == "orquestrador",
    )
    _registrar(
        "chip nao declarado ('z') nao empilha",
        res_chip_desconhecido["pilha_telas"] == [],
    )

    estado_original = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "orquestrador",
        "pilha_telas": [],
    }
    processar_comando(estado_original, "d", modelo)
    _registrar(
        "processar_comando nao modifica o dict original com chip 'd'",
        estado_original["tela_atual"] == "orquestrador"
        and estado_original["pilha_telas"] == [],
        "estado apos chamada={0!r}".format(estado_original),
    )

    e_d = processar_comando(estado_raiz, "d", modelo)
    e_esc = processar_comando(e_d, "\x1b")
    _registrar(
        "ciclo completo: raiz -> destino -> raiz",
        e_esc["tela_atual"] == "orquestrador"
        and e_esc["pilha_telas"] == []
        and e_esc["saindo"] is False,
    )

    estado_com_borda = {
        "tipo_borda": "reta",
        "saindo": False,
        "tela_atual": "orquestrador",
        "pilha_telas": [],
    }
    res_d_reta = processar_comando(estado_com_borda, "d", modelo)
    _registrar(
        "chip 'd' preserva tipo_borda ao navegar",
        res_d_reta["tipo_borda"] == "reta",
    )


def teste_renderizar_estado(modelo):
    print("")
    print("== Secao 3 - renderizar_estado ==")

    estado_curva = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    estado_reta = {"tipo_borda": "reta", "saindo": False, "pilha_telas": []}

    res_curva = renderizar_estado(estado_curva, modelo, largura=_LARGURA_SUBPROCESS)
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
        "saida curva bate com _EXPECTED_CURVA (largura 80, igualdade estrita)",
        bate_curva,
        "" if bate_curva else "ver diff abaixo",
    )
    if not bate_curva:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_CURVA))
        print("--- obtido (repr) ---")
        print(repr(res_curva))

    _registrar(
        "renderizar_estado(estado_curva, modelo, largura=80) == renderizar_tela(modelo, 'curva', largura=80)",
        res_curva == renderizar_tela(modelo, "curva", largura=_LARGURA_SUBPROCESS),
    )

    res_reta = renderizar_estado(estado_reta, modelo, largura=_LARGURA_SUBPROCESS)
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
        "saida reta bate com _EXPECTED_RETA (largura 80, igualdade estrita)",
        bate_reta,
        "" if bate_reta else "ver diff abaixo",
    )
    if not bate_reta:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_RETA))
        print("--- obtido (repr) ---")
        print(repr(res_reta))

    _registrar(
        "renderizar_estado(estado_reta, modelo, largura=80) == renderizar_tela(modelo, 'reta', largura=80)",
        res_reta == renderizar_tela(modelo, "reta", largura=_LARGURA_SUBPROCESS),
    )

    estado_snapshot = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    renderizar_estado(estado_snapshot, modelo)
    _registrar(
        "renderizar_estado nao altera estado",
        estado_snapshot == {"tipo_borda": "curva", "saindo": False, "pilha_telas": []},
    )

    cabecalho_antes = dict(modelo.cabecalho)
    renderizar_estado({"tipo_borda": "reta", "saindo": False, "pilha_telas": []}, modelo)
    _registrar(
        "renderizar_estado nao altera modelo.cabecalho",
        modelo.cabecalho == cabecalho_antes,
    )

    _registrar(
        "renderizar_estado(estado_curva, modelo, largura=42) == _EXPECTED_DIAGNOSTICO_CURVA_42",
        renderizar_estado(estado_curva, modelo, largura=42) == _EXPECTED_DIAGNOSTICO_CURVA_42,
    )
    _registrar(
        "renderizar_estado(estado_reta, modelo, largura=42) bate formato 42 chars",
        all(len(ln) == 42 for ln in renderizar_estado(estado_reta, modelo, largura=42).split("\n") if ln),
    )

    res_60 = renderizar_estado(estado_curva, modelo, largura=60)
    linhas_60_ok = all(len(ln) == 60 for ln in res_60.split("\n") if ln != "")
    _registrar(
        "renderizar_estado(..., largura=60): cada linha nao-vazia tem 60 chars",
        linhas_60_ok,
    )
    _registrar(
        "renderizar_estado(estado, modelo) == renderizar_estado(estado, modelo, largura=None)",
        renderizar_estado(estado_curva, modelo)
        == renderizar_estado(estado_curva, modelo, largura=None),
    )


def teste_integracao_subprocess():
    print("")
    print("== Secao 4 - Integracao via subprocess (demo completo) ==")

    caminho_json = _BASE_PADRAO / "config" / "telas" / "orquestrador.json"
    json_antes = caminho_json.read_text(encoding="utf-8")

    modelo = _carregar_modelo()
    esperado_curva_80 = renderizar_tela(
        modelo, tipo_borda="curva", largura=_LARGURA_SUBPROCESS
    )
    esperado_reta_80 = renderizar_tela(
        modelo, tipo_borda="reta", largura=_LARGURA_SUBPROCESS
    )
    saida_esperada = esperado_curva_80 + esperado_reta_80

    env_sem_columns = {k: v for k, v in os.environ.items() if k != "COLUMNS"}

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
        env=env_sem_columns,
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
    _registrar(
        "stdout nao contem linha em branco entre caixas ('\\n\\n' ausente)",
        "\n\n" not in proc.stdout,
    )

    bate = proc.stdout == saida_esperada
    _registrar(
        "stdout bate com renderizar_tela(..., largura=80) curva+reta",
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

    proc_esc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_columns,
    )
    _registrar(
        "demo com 'b\\n\\x1b\\n' encerra com codigo 0",
        proc_esc.returncode == 0,
        "returncode={0}".format(proc_esc.returncode),
    )
    _registrar(
        "stdout de 'b\\n\\x1b\\n' contem render curva e reta apos 'b'",
        "╭ ORQUESTRADOR" in proc_esc.stdout and "┌ ORQUESTRADOR" in proc_esc.stdout,
    )
    _registrar(
        "stdout de 'b\\n\\x1b\\n' e identico ao de 'b\\ns\\n'",
        proc_esc.stdout == proc.stdout,
    )


def teste_eof_sem_s():
    print("")
    print("== EOF sem 's' (encerra com codigo 0) ==")

    modelo = _carregar_modelo()
    esperado_curva_80 = renderizar_tela(
        modelo, tipo_borda="curva", largura=_LARGURA_SUBPROCESS
    )
    env_sem_columns = {k: v for k, v in os.environ.items() if k != "COLUMNS"}

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="",
        capture_output=True,
        text=True,
        env=env_sem_columns,
    )
    _registrar(
        "printf '' | python tela/demo.py encerra com codigo 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    _registrar(
        "stdout com EOF sem 's' contem apenas render curva inicial (largura 80)",
        proc.stdout == esperado_curva_80,
        "" if proc.stdout == esperado_curva_80 else "stdout diverge",
    )


def teste_navegacao_subprocess():
    print("")
    print("== Secao 4b - Navegacao via subprocess (H-0010A) ==")

    caminho_json_orq = _BASE_PADRAO / "config" / "telas" / "orquestrador.json"
    caminho_json_des = _BASE_PADRAO / "config" / "telas" / "destino_minimo.json"
    json_orq_antes = caminho_json_orq.read_text(encoding="utf-8")
    json_des_antes = caminho_json_des.read_text(encoding="utf-8")

    modelo_orq = _carregar_modelo()
    modelo_des = _carregar_modelo_por_id("destino_minimo")
    esperado_orq_curva_80 = renderizar_tela(
        modelo_orq, tipo_borda="curva", largura=_LARGURA_SUBPROCESS
    )
    esperado_orq_reta_80 = renderizar_tela(
        modelo_orq, tipo_borda="reta", largura=_LARGURA_SUBPROCESS
    )
    esperado_des_curva_80 = renderizar_tela(
        modelo_des, tipo_borda="curva", largura=_LARGURA_SUBPROCESS
    )
    esperado_des_reta_80 = renderizar_tela(
        modelo_des, tipo_borda="reta", largura=_LARGURA_SUBPROCESS
    )

    env_sem_columns = {k: v for k, v in os.environ.items() if k != "COLUMNS"}

    proc_nav = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="d\n\x1b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_columns,
    )
    saida_esperada_nav = (
        esperado_orq_curva_80
        + esperado_des_curva_80
        + esperado_orq_curva_80
    )
    _registrar(
        "demo com 'd\\n\\x1b\\n\\x1b\\n' encerra com codigo 0",
        proc_nav.returncode == 0,
        "returncode={0}".format(proc_nav.returncode),
    )
    if proc_nav.returncode != 0:
        sys.stderr.write(proc_nav.stdout)
        sys.stderr.write(proc_nav.stderr)
    _registrar(
        "demo 'd\\n\\x1b\\n\\x1b\\n' exibe render destino_minimo ('DESTINO MINIMO')",
        "DESTINO MINIMO" in proc_nav.stdout,
    )
    _registrar(
        "demo 'd\\n\\x1b\\n\\x1b\\n' exibe render destino com '[Esc] Voltar'",
        "[Esc] Voltar" in proc_nav.stdout,
    )
    _registrar(
        "demo 'd\\n\\x1b\\n\\x1b\\n' NAO exibe '[B] Borda'",
        "[B] Borda" not in proc_nav.stdout,
    )
    bate_nav = proc_nav.stdout == saida_esperada_nav
    _registrar(
        "demo 'd\\n\\x1b\\n\\x1b\\n' gera 3 renders (orq,dest,orq) curva largura 80",
        bate_nav,
        "" if bate_nav else "ver diff abaixo",
    )
    if not bate_nav:
        print("--- esperado (repr) ---")
        print(repr(saida_esperada_nav))
        print("--- stdout (repr) ---")
        print(repr(proc_nav.stdout))

    _registrar(
        "demo 'd\\n\\x1b\\n\\x1b\\n' stderr vazio",
        proc_nav.stderr == "",
        "stderr={0!r}".format(proc_nav.stderr),
    )

    proc_nav_borda = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\nd\n\x1b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_columns,
    )
    saida_esperada_nav_borda = (
        esperado_orq_curva_80
        + esperado_orq_reta_80
        + esperado_des_reta_80
        + esperado_orq_reta_80
    )
    _registrar(
        "demo 'b\\nd\\n\\x1b\\n\\x1b\\n' encerra com codigo 0",
        proc_nav_borda.returncode == 0,
        "returncode={0}".format(proc_nav_borda.returncode),
    )
    if proc_nav_borda.returncode != 0:
        sys.stderr.write(proc_nav_borda.stdout)
        sys.stderr.write(proc_nav_borda.stderr)
    bate_nav_borda = proc_nav_borda.stdout == saida_esperada_nav_borda
    _registrar(
        "demo 'b\\nd\\n\\x1b\\n\\x1b\\n' gera 4 renders (orq-c,orq-r,des-r,orq-r)",
        bate_nav_borda,
        "" if bate_nav_borda else "ver diff abaixo",
    )
    if not bate_nav_borda:
        print("--- esperado (repr) ---")
        print(repr(saida_esperada_nav_borda))
        print("--- stdout (repr) ---")
        print(repr(proc_nav_borda.stdout))

    json_orq_depois = caminho_json_orq.read_text(encoding="utf-8")
    json_des_depois = caminho_json_des.read_text(encoding="utf-8")
    _registrar(
        "orquestrador.json inalterado apos navegacao",
        json_orq_antes == json_orq_depois,
    )
    _registrar(
        "destino_minimo.json inalterado apos navegacao",
        json_des_antes == json_des_depois,
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
        "gerar_diagnostico_tela() bate com _EXPECTED_DIAGNOSTICO_CURVA_42 (default curva, 42)",
        resultado == _EXPECTED_DIAGNOSTICO_CURVA_42,
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
        "stdout de diagnostico.py bate com _EXPECTED_DIAGNOSTICO_CURVA_42",
        proc.stdout == _EXPECTED_DIAGNOSTICO_CURVA_42,
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


def teste_inspecao_codigo_demo():
    print("")
    print("== Secao 6 - Inspecao de codigo para modo sem echo (H-0009) ==")

    caminho_mod = _BASE_PADRAO / "tela" / "demo.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    _registrar(
        "demo.py contem 'termios'",
        "termios" in texto_mod,
    )
    _registrar(
        "demo.py contem 'tty'",
        "tty" in texto_mod,
    )
    _registrar(
        "demo.py contem 'shutil.get_terminal_size'",
        "shutil.get_terminal_size" in texto_mod,
    )
    _registrar(
        "demo.py contem 'isatty'",
        "isatty" in texto_mod,
    )
    _registrar(
        "demo.py nao contem 'input('",
        "input(" not in texto_mod,
    )
    _registrar(
        "demo.py nao contem 'curses'",
        "curses" not in texto_mod,
    )
    _registrar(
        "demo.py nao contem 'textual'",
        "textual" not in texto_mod,
    )
    _registrar(
        "demo.py nao contem 'rich'",
        "rich" not in texto_mod,
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
    print("Diagnostico H-0010A - aplicacao demonstravel com borda/sair/navegacao")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_estado_inicial()
    teste_processar_comando()

    modelo = _carregar_modelo()
    teste_navegacao_minima(modelo)
    teste_renderizar_estado(modelo)

    teste_integracao_subprocess()
    teste_navegacao_subprocess()
    teste_eof_sem_s()
    teste_preservacao_diagnostico()
    teste_proibicoes_importacao_demo()
    teste_inspecao_codigo_demo()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
