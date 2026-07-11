"""Diagnostico da aplicacao demonstravel H-0008/H-0009/H-0010A/H-0022 (tela/demo.py).

Executavel via:
    python tela/teste_demo.py

Cobre os criterios de aceite testaveis dos handoffs H-0008, H-0009,
H-0010A (navegacao minima com tela destino) e H-0022 (sessao TUI corrigida
conforme ADR-0016).

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

Secao 7 - Sessao TUI (H-0022 / ADR-0016):
- 7A: Inspecao de codigo (setcbreak, sem setraw, sequencias obrigatorias,
      \x1b[2J exatamente uma vez, synchronized output, captura KI, finally).
- 7B: _iniciar_sessao_tui (setcbreak, sequencias de entrada, atributos).
- 7C: _encerrar_sessao_tui (tcsetattr, \x1b[?7h, \x1b[?25h, \x1b[?1049l).
- 7D: _apresentar_quadro (escrita atomica, posicionamento absoluto,
      synchronized output, sem newline, preenchimento ate largura).
- 7E: captura_interrupcao_de_script (captura KI, nao interfere em execucao
      normal, nao suprime outras excecoes).
- 7F: Restauracao por excecao (tcsetattr + sequencias apos RuntimeError).
- 7G: Fallback nao-TTY sem sequencias TUI via subprocess (item 11).

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
    _iniciar_sessao_tui,
    _encerrar_sessao_tui,
    _apresentar_quadro,
    _ler_tecla_sessao,
    captura_interrupcao_de_script,
)
from tela.diagnostico import gerar_diagnostico_tela  # noqa: E402


_RESULTADOS = []


_LARGURA_SUBPROCESS = 80
# Altura deterministica do subprocess da demo (H-0015). Em contexto de
# pipe/nao-tty, ``shutil.get_terminal_size(fallback=(80, 24))`` usa o fallback
# ``lines=24``. Para garantir determinismo entre ambientes (ACH-H15-03), o env
# do subprocess remove COLUMNS e LINES, forçando o fallback (80, 24); o
# esperado e entao computado com largura=80 e altura=24.
_ALTURA_SUBPROCESS = 24


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
    "│ [g] Grupo Min.                                                               │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ Menus ───────────────────────────────────────────────────────────────────────╮\n"
    "│  [Esc] Sair  [?] Ajuda                                                       │\n"
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
    "│ [g] Grupo Min.                                                               │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ Menus ───────────────────────────────────────────────────────────────────────┐\n"
    "│  [Esc] Sair  [?] Ajuda                                                       │\n"
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
    "│ [g] Grupo Min.                         │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menus ─────────────────────────────────╮\n"
    "│  [Esc] Sair  [?] Ajuda                 │\n"
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
    "│  [Esc] Voltar  [?] Ajuda                                                     │\n"
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
    "│  [Esc] Voltar  [?] Ajuda                                                     │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
)


_EXPECTED_GRUPO_MINIMO_CURVA_80 = (
    "╭ GRUPO MINIMO ────────────────────────────────────────────────────────────────╮\n"
    "│ Tela de teste — grupo estrutural com dashboard simples                       │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ CONTEUDO ────────────────────────────────────────────────────────────────────╮\n"
    "│ Dashboard dentro de grupo estrutural                                         │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
    "╭ Menus ───────────────────────────────────────────────────────────────────────╮\n"
    "│  [Esc] Voltar  [?] Ajuda                                                     │\n"
    "╰──────────────────────────────────────────────────────────────────────────────╯\n"
)


_EXPECTED_GRUPO_MINIMO_RETA_80 = (
    "┌ GRUPO MINIMO ────────────────────────────────────────────────────────────────┐\n"
    "│ Tela de teste — grupo estrutural com dashboard simples                       │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ CONTEUDO ────────────────────────────────────────────────────────────────────┐\n"
    "│ Dashboard dentro de grupo estrutural                                         │\n"
    "└──────────────────────────────────────────────────────────────────────────────┘\n"
    "┌ Menus ───────────────────────────────────────────────────────────────────────┐\n"
    "│  [Esc] Voltar  [?] Ajuda                                                     │\n"
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

    print("")
    print("-- Navegacao grupo_minimo (H-0013) --")

    estado_raiz_g = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "orquestrador",
        "pilha_telas": [],
    }

    res_g = processar_comando(estado_raiz_g, "g", modelo)
    _registrar(
        "chip 'g' muda tela_atual para 'grupo_minimo' (H-0013)",
        res_g["tela_atual"] == "grupo_minimo",
        "tela_atual={0!r}".format(res_g.get("tela_atual")),
    )
    _registrar(
        "chip 'g' empilha 'orquestrador' em pilha_telas (H-0013)",
        res_g["pilha_telas"] == ["orquestrador"],
        "pilha_telas={0!r}".format(res_g.get("pilha_telas")),
    )
    _registrar(
        "chip 'g' nao altera tipo_borda nem saindo (H-0013)",
        res_g["tipo_borda"] == "curva" and res_g["saindo"] is False,
    )

    estado_grupo_interno = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "grupo_minimo",
        "pilha_telas": ["orquestrador"],
    }
    res_esc_grupo = processar_comando(estado_grupo_interno, "\x1b")
    _registrar(
        "Esc em grupo_minimo volta para 'orquestrador' (H-0013)",
        res_esc_grupo["tela_atual"] == "orquestrador"
        and res_esc_grupo["pilha_telas"] == [],
        "tela_atual={0!r} pilha={1!r}".format(
            res_esc_grupo.get("tela_atual"), res_esc_grupo.get("pilha_telas")
        ),
    )
    _registrar(
        "Esc em grupo_minimo NAO define saindo == True (H-0013)",
        res_esc_grupo["saindo"] is False,
    )

    e_g = processar_comando(estado_raiz_g, "g", modelo)
    e_g_esc = processar_comando(e_g, "\x1b")
    _registrar(
        "ciclo completo: orquestrador -> grupo_minimo -> orquestrador (H-0013)",
        e_g_esc["tela_atual"] == "orquestrador"
        and e_g_esc["pilha_telas"] == []
        and e_g_esc["saindo"] is False,
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


def teste_renderizar_estado_altura(modelo):
    print("")
    print("== Secao 3b - renderizar_estado com altura (H-0015) ==")

    estado_curva = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}

    # CA-02: altura explicita suficiente -> exatamente `altura` linhas.
    res_24 = renderizar_estado(
        estado_curva, modelo, largura=42, altura=24
    )
    _registrar(
        "renderizar_estado(estado, modelo, largura=42, altura=24) -> 24 linhas",
        isinstance(res_24, str) and res_24.count("\n") == 24,
        "count={0}".format(res_24.count("\n") if isinstance(res_24, str) else "n/a"),
    )

    # CA-01 / CA-03: altura minima (15) sem preenchimento, saida identica
    # ao comportamento natural (sem altura). H-0016: com a barra horizontal
    # responsiva em 1 linha, L_barra=3 e n_minimo=15.
    res_16 = renderizar_estado(
        estado_curva, modelo, largura=42, altura=15
    )
    _registrar(
        "renderizar_estado(..., altura=15) -> 15 linhas (sem fill)",
        res_16.count("\n") == 15,
        "count={0}".format(res_16.count("\n")),
    )
    _registrar(
        "renderizar_estado(..., altura=15) == renderizar_estado(..., largura=42)",
        res_16 == renderizar_estado(estado_curva, modelo, largura=42),
    )

    # altura=None preserva o comportamento atual.
    _registrar(
        "renderizar_estado(estado, modelo, largura=42) == "
        "renderizar_estado(estado, modelo, largura=42, altura=None)",
        renderizar_estado(estado_curva, modelo, largura=42)
        == renderizar_estado(estado_curva, modelo, largura=42, altura=None),
    )

    # Consistencia: renderizar_estado repassa altura ao renderer.
    _registrar(
        "renderizar_estado(..., altura=24) == renderizar_tela(modelo, 'curva', "
        "largura=42, altura=24)",
        res_24 == renderizar_tela(
            modelo, tipo_borda="curva", largura=42, altura=24
        ),
    )

    # Barra_de_menus preservada no rodape (ultima linha nao-vazia termina
    # com a borda inferior) e invariante de largura preservado.
    linhas_24 = res_24.split("\n")
    ultima = [ln for ln in linhas_24 if ln != ""][-1]
    _registrar(
        "renderizar_estado(..., altura=24): barra_de_menus no rodape ('╯')",
        ultima.endswith("╯"),
        "ultima={0!r}".format(ultima),
    )
    _registrar(
        "renderizar_estado(..., altura=24): cada linha nao-vazia tem 42 chars",
        all(len(ln) == 42 for ln in linhas_24 if ln != ""),
    )

    # renderizar_estado nao altera estado nem modelo.
    estado_snap = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    cabecalho_antes = dict(modelo.cabecalho)
    renderizar_estado(estado_snap, modelo, largura=42, altura=24)
    _registrar(
        "renderizar_estado(..., altura=24) nao altera estado",
        estado_snap == {"tipo_borda": "curva", "saindo": False, "pilha_telas": []},
    )
    _registrar(
        "renderizar_estado(..., altura=24) nao altera modelo.cabecalho",
        modelo.cabecalho == cabecalho_antes,
    )


def teste_integracao_subprocess():
    print("")
    print("== Secao 4 - Integracao via subprocess (demo completo) ==")

    caminho_json = _BASE_PADRAO / "config" / "telas" / "orquestrador.json"
    json_antes = caminho_json.read_text(encoding="utf-8")

    modelo = _carregar_modelo()
    esperado_curva_80 = renderizar_tela(
        modelo, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    esperado_reta_80 = renderizar_tela(
        modelo, tipo_borda="reta",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    saida_esperada = esperado_curva_80 + esperado_reta_80

    env_sem_dimensoes = {
        k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    }

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
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
        env=env_sem_dimensoes,
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
        modelo, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    env_sem_dimensoes = {
        k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    }

    proc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
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
        modelo_orq, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    esperado_orq_reta_80 = renderizar_tela(
        modelo_orq, tipo_borda="reta",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    esperado_des_curva_80 = renderizar_tela(
        modelo_des, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )
    esperado_des_reta_80 = renderizar_tela(
        modelo_des, tipo_borda="reta",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )

    env_sem_dimensoes = {
        k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    }

    proc_nav = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="d\n\x1b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
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
        env=env_sem_dimensoes,
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

    print("")
    print("-- Navegacao grupo_minimo via subprocess (H-0013) --")

    caminho_json_grupo = _BASE_PADRAO / "config" / "telas" / "grupo_minimo.json"
    json_grupo_antes = caminho_json_grupo.read_text(encoding="utf-8")

    modelo_grupo = _carregar_modelo_por_id("grupo_minimo")
    esperado_grupo_curva_80 = renderizar_tela(
        modelo_grupo, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )

    proc_nav_grupo = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="g\n\x1b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
    )
    saida_esperada_nav_grupo = (
        esperado_orq_curva_80
        + esperado_grupo_curva_80
        + esperado_orq_curva_80
    )
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' encerra com codigo 0 (H-0013)",
        proc_nav_grupo.returncode == 0,
        "returncode={0}".format(proc_nav_grupo.returncode),
    )
    if proc_nav_grupo.returncode != 0:
        sys.stderr.write(proc_nav_grupo.stdout)
        sys.stderr.write(proc_nav_grupo.stderr)
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' exibe render grupo_minimo ('GRUPO MINIMO') (H-0013)",
        "GRUPO MINIMO" in proc_nav_grupo.stdout,
    )
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' exibe '[Esc] Voltar' (H-0013)",
        "[Esc] Voltar" in proc_nav_grupo.stdout,
    )
    bate_nav_grupo = proc_nav_grupo.stdout == saida_esperada_nav_grupo
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' gera 3 renders (orq-c,grupo-c,orq-c) largura 80 (H-0013)",
        bate_nav_grupo,
        "" if bate_nav_grupo else "ver diff abaixo",
    )
    if not bate_nav_grupo:
        print("--- esperado (repr) ---")
        print(repr(saida_esperada_nav_grupo))
        print("--- stdout (repr) ---")
        print(repr(proc_nav_grupo.stdout))
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' stderr vazio (H-0013)",
        proc_nav_grupo.stderr == "",
        "stderr={0!r}".format(proc_nav_grupo.stderr),
    )

    # ACH-H15-03: determinismo da altura em subprocess. Com COLUMNS e LINES
    # removidos do env, a demo usa fallback (80, 24); cada um dos 3 renders
    # (orq-c, grupo-c, orq-c) deve ter exatamente 24 linhas -> total 72.
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' propaga altura=24: stdout tem 72 "
        "newlines (3 renders x 24) (ACH-H15-03)",
        proc_nav_grupo.stdout.count("\n") == 3 * _ALTURA_SUBPROCESS,
        "count={0}".format(proc_nav_grupo.stdout.count("\n")),
    )

    json_grupo_depois = caminho_json_grupo.read_text(encoding="utf-8")
    _registrar(
        "grupo_minimo.json inalterado apos navegacao (H-0013)",
        json_grupo_antes == json_grupo_depois,
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
        "demo.py importa 'os' (necessario para os.read em _ler_tecla_sessao)",
        "import os" in texto_mod,
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


def teste_sessao_tui_h0022():
    print("")
    print("== Secao 7 - Sessao TUI (H-0022 / ADR-0016) ==")

    import io
    from unittest.mock import patch

    caminho_mod = _BASE_PADRAO / "tela" / "demo.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")

    # --- 7A: Inspecao de codigo ---
    print("")
    print("-- 7A: Inspecao de codigo --")

    _registrar(
        "H-0022 item 2: 'setcbreak' presente no codigo",
        "setcbreak" in texto_mod,
    )
    _registrar(
        "H-0022 item 2: 'setraw' ausente no codigo",
        "setraw" not in texto_mod,
    )
    _registrar(
        "H-0022 item 3: alternate screen ativado (\\x1b[?1049h) presente",
        "\\x1b[?1049h" in texto_mod,
    )
    _registrar(
        "H-0022 item 3: cursor ocultado (\\x1b[?25l) presente",
        "\\x1b[?25l" in texto_mod,
    )
    _registrar(
        "H-0022 item 3: cursor restaurado (\\x1b[?25h) presente",
        "\\x1b[?25h" in texto_mod,
    )
    _registrar(
        "H-0022 item 3: alternate screen encerrado (\\x1b[?1049l) presente",
        "\\x1b[?1049l" in texto_mod,
    )
    _registrar(
        "H-0022 item 4: autowrap desativado (\\x1b[?7l) presente",
        "\\x1b[?7l" in texto_mod,
    )
    _registrar(
        "H-0022 item 4: autowrap restaurado (\\x1b[?7h) presente",
        "\\x1b[?7h" in texto_mod,
    )
    _registrar(
        "H-0022 item 6: 'shutil.get_terminal_size' presente",
        "shutil.get_terminal_size" in texto_mod,
    )
    contagem_2j = texto_mod.count("\\x1b[2J")
    _registrar(
        "H-0022 item 7: \\x1b[2J aparece exatamente uma vez no codigo",
        contagem_2j == 1,
        "count={0}".format(contagem_2j),
    )
    _registrar(
        "H-0022 item 8: synchronized output on (\\x1b[?2026h) presente",
        "\\x1b[?2026h" in texto_mod,
    )
    _registrar(
        "H-0022 item 8: synchronized output off (\\x1b[?2026l) presente",
        "\\x1b[?2026l" in texto_mod,
    )
    _registrar(
        "H-0022 item 9: 'captura_interrupcao_de_script' definido no codigo",
        "captura_interrupcao_de_script" in texto_mod,
    )
    _registrar(
        "H-0022 item 9: 'except KeyboardInterrupt' presente no codigo",
        "except KeyboardInterrupt" in texto_mod,
    )
    _registrar(
        "H-0022 item 10: bloco 'finally:' presente no codigo",
        "finally:" in texto_mod,
    )

    # --- 7B: _iniciar_sessao_tui ---
    print("")
    print("-- 7B: _iniciar_sessao_tui --")

    atributos_fake = [0, 0, 0, 0, 0, 0, [b"\x03", b"\x1c", b"\x7f"]]
    fd_fake = 0
    buf_init = io.StringIO()

    with patch("termios.tcgetattr", return_value=atributos_fake) as mock_tga, \
         patch("tty.setcbreak") as mock_sc, \
         patch("sys.stdout", buf_init):
        buf_init.flush = lambda: None
        resultado_attrs = _iniciar_sessao_tui(fd_fake)

    conteudo_init = buf_init.getvalue()
    _registrar(
        "7B: tcgetattr chamado com fd_stdin",
        mock_tga.called and mock_tga.call_args[0][0] == fd_fake,
    )
    _registrar(
        "7B: tty.setcbreak chamado (nao setraw)",
        mock_sc.called,
    )
    _registrar(
        "7B: atributos originais retornados",
        resultado_attrs == atributos_fake,
    )
    _registrar(
        "7B: alternate screen ativado (\\x1b[?1049h) na inicializacao",
        "\x1b[?1049h" in conteudo_init,
    )
    _registrar(
        "7B: cursor ocultado (\\x1b[?25l) na inicializacao",
        "\x1b[?25l" in conteudo_init,
    )
    _registrar(
        "7B: autowrap desativado (\\x1b[?7l) na inicializacao",
        "\x1b[?7l" in conteudo_init,
    )
    _registrar(
        "7B: tela limpa (\\x1b[2J) na inicializacao",
        "\x1b[2J" in conteudo_init,
    )
    _registrar(
        "7B: cursor no topo (\\x1b[H) na inicializacao",
        "\x1b[H" in conteudo_init,
    )

    # _ler_tecla_sessao: testa via pipe real para reproduzir fielmente o
    # cenario de buffering (TextIOWrapper vs. descritor do SO) que causava
    # sequencias de escape serem tratadas como Esc isolado.
    #
    # Caso 1: sequencia completa (seta para cima). Os tres bytes sao escritos
    # de uma vez no pipe, simulando a rajada unica que o terminal entrega.
    fd_r, fd_w = os.pipe()
    try:
        os.write(fd_w, b"\x1b[A")
        tecla_scroll = _ler_tecla_sessao(fd=fd_r)
    finally:
        try:
            os.close(fd_r)
        except OSError:
            pass
        try:
            os.close(fd_w)
        except OSError:
            pass
    estado_apos_scroll = processar_comando(criar_estado_inicial(), tecla_scroll)
    _registrar(
        "7B: sequencia de seta para cima retorna sequencia completa via pipe real",
        tecla_scroll == "\x1b[A",
        "tecla={0!r}".format(tecla_scroll),
    )
    _registrar(
        "7B: sequencia de seta para cima nao encerra a sessao",
        estado_apos_scroll["saindo"] is False,
        "tecla={0!r} saindo={1!r}".format(tecla_scroll, estado_apos_scroll["saindo"]),
    )

    # Caso 2: Esc realmente isolado. Apenas b"\x1b" escrito; lado de escrita
    # permanece aberto (sem EOF), forcando o timeout de 0.03 s do select.
    fd_r2, fd_w2 = os.pipe()
    try:
        os.write(fd_w2, b"\x1b")
        tecla_esc = _ler_tecla_sessao(fd=fd_r2)
    finally:
        try:
            os.close(fd_r2)
        except OSError:
            pass
        try:
            os.close(fd_w2)
        except OSError:
            pass
    estado_apos_esc = processar_comando(criar_estado_inicial(), tecla_esc)
    _registrar(
        "7B: Esc isolado via pipe retorna Esc apos timeout (sem travar)",
        tecla_esc == "\x1b",
        "tecla={0!r}".format(tecla_esc),
    )
    _registrar(
        "7B: Esc isolado sem bytes subsequentes encerra a sessao",
        tecla_esc == "\x1b" and estado_apos_esc["saindo"] is True,
        "tecla={0!r} saindo={1!r}".format(tecla_esc, estado_apos_esc["saindo"]),
    )

    # --- 7C: _encerrar_sessao_tui ---
    print("")
    print("-- 7C: _encerrar_sessao_tui --")

    atributos_fake2 = [0, 0, 0, 0, 0, 0, [b"\x03"]]
    fd_fake2 = 1
    buf_enc = io.StringIO()
    tsa_args = []

    with patch("termios.tcsetattr", side_effect=lambda *a: tsa_args.append(a)), \
         patch("sys.stdout", buf_enc):
        buf_enc.flush = lambda: None
        _encerrar_sessao_tui(fd_fake2, atributos_fake2)

    conteudo_enc = buf_enc.getvalue()
    _registrar(
        "7C: tcsetattr chamado com atributos originais",
        len(tsa_args) > 0 and tsa_args[0][2] == atributos_fake2,
    )
    _registrar(
        "7C: autowrap restaurado (\\x1b[?7h) na restauracao",
        "\x1b[?7h" in conteudo_enc,
    )
    _registrar(
        "7C: cursor mostrado (\\x1b[?25h) na restauracao",
        "\x1b[?25h" in conteudo_enc,
    )
    _registrar(
        "7C: alternate screen encerrado (\\x1b[?1049l) na restauracao",
        "\x1b[?1049l" in conteudo_enc,
    )

    # --- 7D: _apresentar_quadro ---
    print("")
    print("-- 7D: _apresentar_quadro --")

    escritas = []
    flush_count = [0]

    class _MockOut:
        def write(self, s):
            escritas.append(s)
        def flush(self):
            flush_count[0] += 1

    class _FakeTermSize:
        columns = 10
        lines = 5

    with patch("sys.stdout", _MockOut()), \
         patch("shutil.get_terminal_size", return_value=_FakeTermSize()):
        _apresentar_quadro("AB\nCD\n")

    _registrar(
        "7D: exatamente uma chamada write() por quadro (escrita atomica)",
        len(escritas) == 1,
        "count={0}".format(len(escritas)),
    )
    _registrar(
        "7D: exatamente uma chamada flush() por quadro",
        flush_count[0] == 1,
        "count={0}".format(flush_count[0]),
    )

    conteudo_quadro = escritas[0] if escritas else ""
    _registrar(
        "7D: synchronized output on (\\x1b[?2026h) no inicio do quadro",
        conteudo_quadro.startswith("\x1b[?2026h"),
    )
    _registrar(
        "7D: synchronized output off (\\x1b[?2026l) no fim do quadro",
        conteudo_quadro.endswith("\x1b[?2026l"),
    )
    _registrar(
        "7D: posicionamento absoluto linha 1 (\\x1b[1;1H) presente",
        "\x1b[1;1H" in conteudo_quadro,
    )
    _registrar(
        "7D: posicionamento absoluto linha 2 (\\x1b[2;1H) presente",
        "\x1b[2;1H" in conteudo_quadro,
    )
    _registrar(
        "7D: sem '\\n' no conteudo do quadro (nao usa newline para quebra de linha)",
        "\n" not in conteudo_quadro,
    )
    _registrar(
        "7D: linha 1 preenchida ate largura do terminal (pad a 10 chars)",
        "AB        " in conteudo_quadro,
    )
    _registrar(
        "7D: linha 2 preenchida ate largura do terminal (pad a 10 chars)",
        "CD        " in conteudo_quadro,
    )

    # Segundo quadro: verifica escrita atomica independente
    escritas2 = []
    flush_count2 = [0]

    class _MockOut2:
        def write(self, s):
            escritas2.append(s)
        def flush(self):
            flush_count2[0] += 1

    with patch("sys.stdout", _MockOut2()), \
         patch("shutil.get_terminal_size", return_value=_FakeTermSize()):
        _apresentar_quadro("XY\n")

    _registrar(
        "7D: segundo quadro tambem tem exatamente uma write() e uma flush()",
        len(escritas2) == 1 and flush_count2[0] == 1,
        "write={0} flush={1}".format(len(escritas2), flush_count2[0]),
    )

    # --- 7E: captura_interrupcao_de_script ---
    print("")
    print("-- 7E: captura_interrupcao_de_script --")

    resultado_ki = []
    with captura_interrupcao_de_script():
        raise KeyboardInterrupt
    resultado_ki.append("pos-ki")
    _registrar(
        "7E: captura_interrupcao_de_script suprime KeyboardInterrupt",
        resultado_ki == ["pos-ki"],
    )

    resultado_normal = []
    with captura_interrupcao_de_script():
        resultado_normal.append("dentro")
    resultado_normal.append("fora")
    _registrar(
        "7E: captura_interrupcao_de_script nao interfere em execucao normal",
        resultado_normal == ["dentro", "fora"],
    )

    excecao_propagada = []
    try:
        with captura_interrupcao_de_script():
            raise ValueError("outro erro")
    except ValueError:
        excecao_propagada.append("ValueError")
    _registrar(
        "7E: captura_interrupcao_de_script nao suprime outras excecoes",
        excecao_propagada == ["ValueError"],
    )

    # --- 7F: Restauracao por excecao ---
    print("")
    print("-- 7F: Restauracao por excecao --")

    atributos_fake3 = [0, 0, 0, 0, 0, 0, [b"\x03"]]
    fd_fake3 = 0
    buf_exc = io.StringIO()
    tsa_args3 = []

    with patch("termios.tcgetattr", return_value=atributos_fake3), \
         patch("termios.tcsetattr", side_effect=lambda *a: tsa_args3.append(a)), \
         patch("tty.setcbreak"), \
         patch("sys.stdout", buf_exc):
        buf_exc.flush = lambda: None
        try:
            attrs3 = _iniciar_sessao_tui(fd_fake3)
            try:
                raise RuntimeError("excecao simulada")
            finally:
                _encerrar_sessao_tui(fd_fake3, attrs3)
        except RuntimeError:
            pass

    conteudo_exc = buf_exc.getvalue()
    _registrar(
        "7F: tcsetattr chamado apos excecao",
        len(tsa_args3) > 0,
    )
    _registrar(
        "7F: cursor mostrado apos excecao (\\x1b[?25h)",
        "\x1b[?25h" in conteudo_exc,
    )
    _registrar(
        "7F: alternate screen encerrado apos excecao (\\x1b[?1049l)",
        "\x1b[?1049l" in conteudo_exc,
    )
    _registrar(
        "7F: autowrap restaurado apos excecao (\\x1b[?7h)",
        "\x1b[?7h" in conteudo_exc,
    )

    # --- 7G: Fallback nao-TTY via subprocess ---
    print("")
    print("-- 7G: Fallback nao-TTY --")

    env_sem_dimensoes = {
        k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    }
    proc_pipe = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
    )
    _registrar(
        "7G: printf 'b\\ns\\n' | demo.py encerra com codigo 0",
        proc_pipe.returncode == 0,
        "returncode={0}".format(proc_pipe.returncode),
    )
    _registrar(
        "7G: saida pipe nao contem \\x1b[?1049h (alternate screen)",
        "\x1b[?1049h" not in proc_pipe.stdout,
    )
    _registrar(
        "7G: saida pipe nao contem \\x1b[?25l (cursor)",
        "\x1b[?25l" not in proc_pipe.stdout,
    )
    _registrar(
        "7G: saida pipe nao contem \\x1b[?7l (autowrap)",
        "\x1b[?7l" not in proc_pipe.stdout,
    )
    _registrar(
        "7G: saida pipe nao contem \\x1b[?2026h (synchronized output)",
        "\x1b[?2026h" not in proc_pipe.stdout,
    )
    _registrar(
        "7G: stderr vazio em modo pipe",
        proc_pipe.stderr == "",
        "stderr={0!r}".format(proc_pipe.stderr),
    )

    # Item 11: printf 'b\n\x1b\n' deve ser identico a 'b\ns\n'
    proc_pipe_esc = subprocess.run(
        [sys.executable, "tela/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\n\x1b\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
    )
    _registrar(
        "7G (item 11): printf 'b\\n\\x1b\\n' | demo.py encerra com codigo 0",
        proc_pipe_esc.returncode == 0,
        "returncode={0}".format(proc_pipe_esc.returncode),
    )
    _registrar(
        "7G (item 11): saida 'b\\n\\x1b\\n' identica a 'b\\ns\\n'",
        proc_pipe_esc.stdout == proc_pipe.stdout,
    )

    # --- 7H: KI durante processamento/renderizacao (ACH-BLOQ-01) ---
    print("")
    print("-- 7H: KeyboardInterrupt durante processamento/renderizacao (ACH-BLOQ-01) --")

    import tela.demo as _demo_mod_ref
    from unittest.mock import patch as _patch

    _chamadas_7h = [0]
    _ESTADO_SAINDO_7H = {
        "tipo_borda": "curva",
        "saindo": True,
        "tela_atual": "orquestrador",
        "pilha_telas": [],
    }

    def _processar_com_ki(estado, ch, modelo=None):
        _chamadas_7h[0] += 1
        if _chamadas_7h[0] == 1:
            raise KeyboardInterrupt("simulado durante processamento")
        return _ESTADO_SAINDO_7H

    class _FakeTamanho7H:
        columns = 80
        lines = 24

    _ki_propagou_7h = [False]
    _resultado_7h = [-1]
    try:
        with _patch("tela.demo.processar_comando", side_effect=_processar_com_ki), \
             _patch("tela.demo._ler_tecla_sessao", return_value="x"), \
             _patch("tela.demo._apresentar_quadro"), \
             _patch("tela.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
             _patch("tela.demo._encerrar_sessao_tui"), \
             _patch("tela.demo._carregar_modelo_por_id", return_value=object()), \
             _patch("tela.demo.renderizar_estado", return_value=""), \
             _patch("shutil.get_terminal_size", return_value=_FakeTamanho7H()), \
             _patch("sys.stdin") as _stdin_7h, \
             _patch("sys.stdout") as _stdout_7h:
            _stdin_7h.isatty.return_value = True
            _stdin_7h.fileno.return_value = 0
            _stdout_7h.isatty.return_value = True
            _resultado_7h[0] = _demo_mod_ref.main()
    except KeyboardInterrupt:
        _ki_propagou_7h[0] = True

    _registrar(
        "7H: KI durante processar_comando nao propaga para fora do loop",
        not _ki_propagou_7h[0],
        "propagou={0}".format(_ki_propagou_7h[0]),
    )
    _registrar(
        "7H: loop continua apos KI (processar_comando chamado 2 vezes)",
        _chamadas_7h[0] >= 2,
        "chamadas={0}".format(_chamadas_7h[0]),
    )
    _registrar(
        "7H: main() retorna 0 apos KI silencioso",
        _resultado_7h[0] == 0,
        "resultado={0!r}".format(_resultado_7h[0]),
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
    print("Diagnostico H-0010A/H-0022 - aplicacao demonstravel com borda/sair/navegacao/TUI")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_estado_inicial()
    teste_processar_comando()

    modelo = _carregar_modelo()
    teste_navegacao_minima(modelo)
    teste_renderizar_estado(modelo)
    teste_renderizar_estado_altura(modelo)

    teste_integracao_subprocess()
    teste_navegacao_subprocess()
    teste_eof_sem_s()
    teste_preservacao_diagnostico()
    teste_proibicoes_importacao_demo()
    teste_inspecao_codigo_demo()
    teste_sessao_tui_h0022()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
