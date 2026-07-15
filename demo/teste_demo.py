"""Diagnostico da aplicacao demonstravel H-0008/H-0009/H-0010A/H-0022 (demo/demo.py).

Executavel via:
    python demo/teste_demo.py

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
- python demo/demo.py com input "b\ns\n" encerra com codigo 0;
- stdout contem render curva inicial;
- stdout contem render reta apos "b";
- stdout nao contem "\n\n" entre caixas (H-0009);
- stdout bate com renderizar_tela(..., largura=80) curva+reta (H-0009);
- stderr vazio;
- config/telas/demo/demo.json inalterado apos demo;
- subprocess com "b\n\x1b\n" encerra 0 e sai identico a "b\ns\n" (H-0009).

Secao 5 - Preservacao do diagnostico:
- gerar_diagnostico_tela() nao lanca excecao;
- retorno de gerar_diagnostico_tela() e str;
- retorno bate com _EXPECTED_CURVA (default curva H-0006/H-0007, sem "\n\n");
- python demo/diagnostico.py encerra com codigo 0;
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

Alem disso, verifica proibicoes de importacao em demo/demo.py e o
comportamento de EOF sem "s" (encerra com codigo 0).

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

import signal  # noqa: E402
import subprocess  # noqa: E402
import os  # noqa: E402

from tela.loader import carregar_tela  # noqa: E402
from tela.modelo import construir_modelo, ModeloTela  # noqa: E402
from tela.renderizador import renderizar_tela  # noqa: E402
from demo.demo import (  # noqa: E402
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
    _iniciar_sessao_tui,
    _encerrar_sessao_tui,
    _restaurar_efeitos_visuais_tui,
    _apresentar_quadro,
    _ler_tecla_sessao,
    captura_interrupcao_de_script,
    _par_dimensoes_valido,
    _obter_dimensoes_ioctl,
    _obter_dimensoes_env,
    _obter_dimensoes_iniciais,
    _obter_dimensoes_apos_sigwinch,
    _instalar_handler_sigwinch,
    _restaurar_handler_sigwinch,
    _tela_pequena_demais,
    _quadro_minimo_aviso,
    _resolver_conteudo,
    LARGURA_MINIMA_TELA,
    ALTURA_MINIMA_TELA,
)
from demo.diagnostico import gerar_diagnostico_tela  # noqa: E402


_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")

_RESULTADOS = []


_LARGURA_SUBPROCESS = 80
# Altura deterministica do subprocess da demo (H-0015 / H-0030). Em contexto de
# pipe/nao-tty, ``shutil.get_terminal_size(fallback=(80, 24))`` usa o fallback
# ``lines=24``. A partir do H-0030 o lancador do demo possui 7 itens
# (d, g, 1..5), de modo que a caixa NAVEGAR exige mais linhas e o demo
# requer altura >= 28 em largura 80. Para garantir determinismo entre ambientes
# (ACH-H15-03) e acomodar o lancador ampliado, o env do subprocess define
# COLUMNS=80 e LINES=30 explicitamente; o esperado e computado com largura=80 e
# altura=30.
_ALTURA_SUBPROCESS = 30


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
    "│ [1] Console                                                                  │\n"
    "│ [2] Dashboard                                                                │\n"
    "│ [3] Matriz 2x2                                                               │\n"
    "│ [4] Matriz 3x2                                                               │\n"
    "│ [5] Matriz 2x4                                                               │\n"
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
    "│ [1] Console                                                                  │\n"
    "│ [2] Dashboard                                                                │\n"
    "│ [3] Matriz 2x2                                                               │\n"
    "│ [4] Matriz 3x2                                                               │\n"
    "│ [5] Matriz 2x4                                                               │\n"
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
    "│ [1] Console                            │\n"
    "│ [2] Dashboard                          │\n"
    "│ [3] Matriz 2x2                         │\n"
    "│ [4] Matriz 3x2                         │\n"
    "│ [5] Matriz 2x4                         │\n"
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
    tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw)


def _carregar_modelo_por_id(id_tela):
    tela_raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
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
        "estado inicial tem tela_atual == 'demo' (H-0010A)",
        est.get("tela_atual") == "demo",
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
        "tela_atual": "demo",
        "pilha_telas": [],
    }

    res_d = processar_comando(estado_raiz, "d", modelo)
    _registrar(
        "chip 'd' muda tela_atual para 'destino_minimo'",
        res_d["tela_atual"] == "destino_minimo",
        "tela_atual={0!r}".format(res_d.get("tela_atual")),
    )
    _registrar(
        "chip 'd' empilha 'demo' em pilha_telas",
        res_d["pilha_telas"] == ["demo"],
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
        "pilha_telas": ["demo"],
    }
    res_esc_volta = processar_comando(estado_interno, "\x1b")
    _registrar(
        "Esc em tela interna volta para 'demo' (pop pilha)",
        res_esc_volta["tela_atual"] == "demo"
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
        res_s_volta["tela_atual"] == "demo"
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
        res_esc_raiz["tela_atual"] == "demo",
    )
    _registrar(
        "Esc na raiz mantem pilha_telas vazia",
        res_esc_raiz["pilha_telas"] == [],
    )

    res_chip_desconhecido = processar_comando(estado_raiz, "z", modelo)
    _registrar(
        "chip nao declarado ('z') nao altera tela_atual",
        res_chip_desconhecido["tela_atual"] == "demo",
    )
    _registrar(
        "chip nao declarado ('z') nao empilha",
        res_chip_desconhecido["pilha_telas"] == [],
    )

    estado_original = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "demo",
        "pilha_telas": [],
    }
    processar_comando(estado_original, "d", modelo)
    _registrar(
        "processar_comando nao modifica o dict original com chip 'd'",
        estado_original["tela_atual"] == "demo"
        and estado_original["pilha_telas"] == [],
        "estado apos chamada={0!r}".format(estado_original),
    )

    e_d = processar_comando(estado_raiz, "d", modelo)
    e_esc = processar_comando(e_d, "\x1b")
    _registrar(
        "ciclo completo: raiz -> destino -> raiz",
        e_esc["tela_atual"] == "demo"
        and e_esc["pilha_telas"] == []
        and e_esc["saindo"] is False,
    )

    estado_com_borda = {
        "tipo_borda": "reta",
        "saindo": False,
        "tela_atual": "demo",
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
        "tela_atual": "demo",
        "pilha_telas": [],
    }

    res_g = processar_comando(estado_raiz_g, "g", modelo)
    _registrar(
        "chip 'g' muda tela_atual para 'grupo_minimo' (H-0013)",
        res_g["tela_atual"] == "grupo_minimo",
        "tela_atual={0!r}".format(res_g.get("tela_atual")),
    )
    _registrar(
        "chip 'g' empilha 'demo' em pilha_telas (H-0013)",
        res_g["pilha_telas"] == ["demo"],
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
        "pilha_telas": ["demo"],
    }
    res_esc_grupo = processar_comando(estado_grupo_interno, "\x1b")
    _registrar(
        "Esc em grupo_minimo volta para 'demo' (H-0013)",
        res_esc_grupo["tela_atual"] == "demo"
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
        "ciclo completo: demo -> grupo_minimo -> demo (H-0013)",
        e_g_esc["tela_atual"] == "demo"
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
    # H-0030: o demo com 7 itens no lancador requer altura >= 29 em
    # largura 42 (fracao [2,1,2]); usa-se altura=30 para exercitar o fill.
    res_30 = renderizar_estado(
        estado_curva, modelo, largura=42, altura=30
    )
    _registrar(
        "renderizar_estado(estado, modelo, largura=42, altura=30) -> 30 linhas",
        isinstance(res_30, str) and res_30.count("\n") == 30,
        "count={0}".format(res_30.count("\n") if isinstance(res_30, str) else "n/a"),
    )

    # CA-01 / CA-03: altura minima sem preenchimento, saida identica
    # ao comportamento natural (sem altura). H-0016: com a barra horizontal
    # responsiva em 1 linha, L_barra=3. H-0030: com 7 itens no lancador,
    # L_corpo_conteudo=14 (ITENS=3, INFO=2, NAVEGAR=9) -> n_minimo=20.
    #
    # H-0025 secao 11.5 (item 1): o demo real agora declara
    # distribuicao (fracao [2,1,2]); em altura=20 essa distribuicao produz
    # uma cota menor que a altura natural de algum filho — terminal
    # insuficiente, caso explicitamente fora de escopo (ADR-0018 D8). Para
    # preservar a cobertura "altura minima sem fill = saida natural", o
    # sub-cenario usa um modelo SEM distribuicao (ausencia preserva o
    # preenchimento externo H-0013/ADR-0018 D2). altura=20 nao e altura
    # suportada normativa do produto; e apenas o minimo natural desta tela.
    tela_raw_sd = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    corpo_sd = dict(tela_raw_sd["corpo"])
    corpo_sd.pop("distribuicao", None)
    tela_raw_sd = dict(tela_raw_sd)
    tela_raw_sd["corpo"] = corpo_sd
    modelo_sd = construir_modelo(tela_raw_sd)
    res_20 = renderizar_estado(
        estado_curva, modelo_sd, largura=42, altura=20
    )
    _registrar(
        "renderizar_estado(..., altura=20, sem distribuicao) -> 20 linhas (sem fill)",
        res_20.count("\n") == 20,
        "count={0}".format(res_20.count("\n")),
    )
    _registrar(
        "renderizar_estado(..., altura=20, sem distribuicao) == "
        "renderizar_estado(..., largura=42) [sem altura]",
        res_20 == renderizar_estado(estado_curva, modelo_sd, largura=42),
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
        "renderizar_estado(..., altura=30) == renderizar_tela(modelo, 'curva', "
        "largura=42, altura=30)",
        res_30 == renderizar_tela(
            modelo, tipo_borda="curva", largura=42, altura=30
        ),
    )

    # Barra_de_menus preservada no rodape (ultima linha nao-vazia termina
    # com a borda inferior) e invariante de largura preservado.
    linhas_30 = res_30.split("\n")
    ultima = [ln for ln in linhas_30 if ln != ""][-1]
    _registrar(
        "renderizar_estado(..., altura=30): barra_de_menus no rodape ('╯')",
        ultima.endswith("╯"),
        "ultima={0!r}".format(ultima),
    )
    _registrar(
        "renderizar_estado(..., altura=30): cada linha nao-vazia tem 42 chars",
        all(len(ln) == 42 for ln in linhas_30 if ln != ""),
    )

    # renderizar_estado nao altera estado nem modelo.
    estado_snap = {"tipo_borda": "curva", "saindo": False, "pilha_telas": []}
    cabecalho_antes = dict(modelo.cabecalho)
    renderizar_estado(estado_snap, modelo, largura=42, altura=30)
    _registrar(
        "renderizar_estado(..., altura=30) nao altera estado",
        estado_snap == {"tipo_borda": "curva", "saindo": False, "pilha_telas": []},
    )
    _registrar(
        "renderizar_estado(..., altura=30) nao altera modelo.cabecalho",
        modelo.cabecalho == cabecalho_antes,
    )


def teste_integracao_subprocess():
    print("")
    print("== Secao 4 - Integracao via subprocess (demo completo) ==")

    caminho_json = _BASE_PADRAO / "config" / "telas" / "demo" / "demo.json"
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

    # H-0030: o demo com 7 itens no lancador requer altura >= 28 em
    # largura 80. O env do subprocess fixa COLUMNS=80 e LINES=30 (em vez de
    # remover as variaveis) para que a demo renderize em dimensao
    # deterministica suficiente.
    env_sem_dimensoes = dict(
        (k, v) for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    )
    env_sem_dimensoes["COLUMNS"] = str(_LARGURA_SUBPROCESS)
    env_sem_dimensoes["LINES"] = str(_ALTURA_SUBPROCESS)

    proc = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
    )

    _registrar(
        "python demo/demo.py com 'b\\ns\\n' encerra com codigo 0",
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
        "config/telas/demo/demo.json inalterado apos demo",
        json_antes == json_depois,
    )

    proc_esc = subprocess.run(
        [sys.executable, "demo/demo.py"],
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
    # H-0030: o demo com 7 itens no lancador requer altura >= 28 em
    # largura 80. O env do subprocess fixa COLUMNS=80 e LINES=30 (em vez de
    # remover as variaveis) para que a demo renderize em dimensao
    # deterministica suficiente.
    env_sem_dimensoes = dict(
        (k, v) for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    )
    env_sem_dimensoes["COLUMNS"] = str(_LARGURA_SUBPROCESS)
    env_sem_dimensoes["LINES"] = str(_ALTURA_SUBPROCESS)

    proc = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="",
        capture_output=True,
        text=True,
        env=env_sem_dimensoes,
    )
    _registrar(
        "printf '' | python demo/demo.py encerra com codigo 0",
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

    caminho_json_orq = _BASE_PADRAO / "config" / "telas" / "demo" / "demo.json"
    caminho_json_des = _BASE_PADRAO / "config" / "telas" / "demo" / "destino_minimo.json"
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

    # H-0030: o demo com 7 itens no lancador requer altura >= 28 em
    # largura 80. O env do subprocess fixa COLUMNS=80 e LINES=30 (em vez de
    # remover as variaveis) para que a demo renderize em dimensao
    # deterministica suficiente.
    env_sem_dimensoes = dict(
        (k, v) for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    )
    env_sem_dimensoes["COLUMNS"] = str(_LARGURA_SUBPROCESS)
    env_sem_dimensoes["LINES"] = str(_ALTURA_SUBPROCESS)

    proc_nav = subprocess.run(
        [sys.executable, "demo/demo.py"],
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
        [sys.executable, "demo/demo.py"],
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
        "demo.json inalterado apos navegacao",
        json_orq_antes == json_orq_depois,
    )
    _registrar(
        "destino_minimo.json inalterado apos navegacao",
        json_des_antes == json_des_depois,
    )

    print("")
    print("-- Navegacao grupo_minimo via subprocess (H-0013) --")

    caminho_json_grupo = _BASE_PADRAO / "config" / "telas" / "demo" / "grupo_minimo.json"
    json_grupo_antes = caminho_json_grupo.read_text(encoding="utf-8")

    modelo_grupo = _carregar_modelo_por_id("grupo_minimo")
    esperado_grupo_curva_80 = renderizar_tela(
        modelo_grupo, tipo_borda="curva",
        largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
    )

    proc_nav_grupo = subprocess.run(
        [sys.executable, "demo/demo.py"],
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
    # fixados no env (80x30), cada um dos 3 renders (orq-c, grupo-c, orq-c)
    # deve ter exatamente 30 linhas -> total 90.
    _registrar(
        "demo 'g\\n\\x1b\\n\\x1b\\n' propaga altura=30: stdout tem 90 "
        "newlines (3 renders x 30) (ACH-H15-03)",
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
        [sys.executable, "demo/diagnostico.py"],
        cwd=str(_BASE_PADRAO),
        capture_output=True,
        text=True,
    )
    _registrar(
        "python demo/diagnostico.py encerra com codigo 0",
        proc.returncode == 0,
        "returncode={0}".format(proc.returncode),
    )
    _registrar(
        "stdout de diagnostico.py bate com _EXPECTED_DIAGNOSTICO_CURVA_42",
        proc.stdout == _EXPECTED_DIAGNOSTICO_CURVA_42,
    )

    caminho_mod = _BASE_PADRAO / "demo" / "diagnostico.py"
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
    print("== Proibicoes de import no modulo demo/demo.py ==")

    caminho_mod = _BASE_PADRAO / "demo" / "demo.py"
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

    caminho_mod = _BASE_PADRAO / "demo" / "demo.py"
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

    caminho_mod = _BASE_PADRAO / "demo" / "demo.py"
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

    # H-0030: o demo com 7 itens no lancador requer altura >= 28 em
    # largura 80. O env do subprocess fixa COLUMNS=80 e LINES=30 (em vez de
    # remover as variaveis) para que a demo renderize em dimensao
    # deterministica suficiente.
    env_sem_dimensoes = dict(
        (k, v) for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    )
    env_sem_dimensoes["COLUMNS"] = str(_LARGURA_SUBPROCESS)
    env_sem_dimensoes["LINES"] = str(_ALTURA_SUBPROCESS)
    proc_pipe = subprocess.run(
        [sys.executable, "demo/demo.py"],
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
        [sys.executable, "demo/demo.py"],
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

    import demo.demo as _demo_mod_ref
    from unittest.mock import patch as _patch

    _chamadas_7h = [0]
    _ESTADO_SAINDO_7H = {
        "tipo_borda": "curva",
        "saindo": True,
        "tela_atual": "demo",
        "pilha_telas": [],
    }

    def _processar_com_ki(estado, ch, modelo=None):
        _chamadas_7h[0] += 1
        if _chamadas_7h[0] == 1:
            raise KeyboardInterrupt("simulado durante processamento")
        return _ESTADO_SAINDO_7H

    _ki_propagou_7h = [False]
    _resultado_7h = [-1]
    # Com o novo main() TTY: select duplo, wakeup pipe e handler de SIGWINCH.
    # Mockar select.select para retornar fd imediatamente (sem bloqueio) e
    # mockar instalacao/restauracao do handler para evitar efeitos colaterais.
    try:
        with _patch("demo.demo.processar_comando", side_effect=_processar_com_ki), \
             _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
             _patch("demo.demo._apresentar_quadro"), \
             _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
             _patch("demo.demo._encerrar_sessao_tui"), \
             _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
             _patch("demo.demo.renderizar_estado", return_value=""), \
             _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
             _patch("demo.demo._restaurar_handler_sigwinch"), \
             _patch("select.select", return_value=([0], [], [])), \
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


def teste_redimensionamento_reativo_h0023():
    print("")
    print("== Secao 8 - Redimensionamento reativo (H-0023 / ADR-0017) ==")

    import struct as _struct
    import io as _io
    from unittest.mock import patch as _patch, MagicMock, call as _call
    import demo.demo as _demo_mod

    # --- 8.1: _par_dimensoes_valido ---
    print("")
    print("-- 8.1: _par_dimensoes_valido --")

    _registrar("8.1: (80, 24) valido", _par_dimensoes_valido(80, 24))
    _registrar("8.1: (0, 24) invalido (zero)", not _par_dimensoes_valido(0, 24))
    _registrar("8.1: (80, 0) invalido (zero)", not _par_dimensoes_valido(80, 0))
    _registrar("8.1: (-1, 24) invalido (negativo)", not _par_dimensoes_valido(-1, 24))
    _registrar("8.1: ('abc', 24) invalido (nao inteiro)", not _par_dimensoes_valido("abc", 24))
    _registrar("8.1: (None, 24) invalido (ausente)", not _par_dimensoes_valido(None, 24))
    _registrar("8.1: (80, None) invalido (ausente)", not _par_dimensoes_valido(80, None))
    _registrar("8.1: ('80', '24') valido (string inteira)", _par_dimensoes_valido("80", "24"))

    # --- 8.2: _obter_dimensoes_ioctl ---
    print("")
    print("-- 8.2: _obter_dimensoes_ioctl --")

    import fcntl as _fcntl
    import termios as _termios

    buf_valido = _struct.pack("HHHH", 24, 80, 0, 0)
    with _patch("fcntl.ioctl", return_value=buf_valido):
        r_ioctl = _obter_dimensoes_ioctl(0)
    _registrar("8.2: ioctl valido retorna (80, 24)", r_ioctl == (80, 24))

    buf_zero = _struct.pack("HHHH", 0, 0, 0, 0)
    with _patch("fcntl.ioctl", return_value=buf_zero):
        r_ioctl_zero = _obter_dimensoes_ioctl(0)
    _registrar("8.2: ioctl (0,0) retorna None (par invalido)", r_ioctl_zero is None)

    with _patch("fcntl.ioctl", side_effect=OSError("ioctl failed")):
        r_ioctl_err = _obter_dimensoes_ioctl(0)
    _registrar("8.2: ioctl OSError retorna None", r_ioctl_err is None)

    # --- 8.3: _obter_dimensoes_env ---
    print("")
    print("-- 8.3: _obter_dimensoes_env --")

    with _patch.dict(os.environ, {"LINES": "24", "COLUMNS": "80"}, clear=False):
        r_env = _obter_dimensoes_env()
    _registrar("8.3: LINES=24 COLUMNS=80 retorna (80, 24)", r_env == (80, 24))

    env_sem_cols = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_sem_cols["LINES"] = "24"
    with _patch.dict(os.environ, env_sem_cols, clear=True):
        r_env_sem_cols = _obter_dimensoes_env()
    _registrar("8.3: LINES sem COLUMNS retorna None", r_env_sem_cols is None)

    with _patch.dict(os.environ, {"LINES": "24", "COLUMNS": "0"}, clear=False):
        r_env_zero = _obter_dimensoes_env()
    _registrar("8.3: COLUMNS=0 retorna None (zero invalido)", r_env_zero is None)

    with _patch.dict(os.environ, {"LINES": "abc", "COLUMNS": "80"}, clear=False):
        r_env_inv = _obter_dimensoes_env()
    _registrar("8.3: LINES='abc' retorna None (nao inteiro)", r_env_inv is None)

    # --- 8.4: _obter_dimensoes_iniciais ---
    print("")
    print("-- 8.4: _obter_dimensoes_iniciais --")

    buf_100_50 = _struct.pack("HHHH", 50, 100, 0, 0)
    with _patch("fcntl.ioctl", return_value=buf_100_50), \
         _patch.dict(os.environ, {"LINES": "24", "COLUMNS": "80"}, clear=False):
        r_ini_ioctl = _obter_dimensoes_iniciais(0)
    _registrar("8.4: ioctl prevalece sobre env: (100,50)", r_ini_ioctl == (100, 50))

    env_vals = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_vals.update({"LINES": "24", "COLUMNS": "80"})
    with _patch("fcntl.ioctl", side_effect=OSError), \
         _patch.dict(os.environ, env_vals, clear=True):
        r_ini_env = _obter_dimensoes_iniciais(0)
    _registrar("8.4: ioctl None, env valido: retorna par env", r_ini_env == (80, 24))

    env_so_lines = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_so_lines["LINES"] = "24"
    with _patch("fcntl.ioctl", side_effect=OSError), \
         _patch.dict(os.environ, env_so_lines, clear=True):
        r_ini_fallback = _obter_dimensoes_iniciais(0)
    _registrar("8.4: ioctl None, env invalido: retorna (80,24)", r_ini_fallback == (80, 24))

    env_vazio = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    with _patch("fcntl.ioctl", side_effect=OSError), \
         _patch.dict(os.environ, env_vazio, clear=True):
        r_ini_nada = _obter_dimensoes_iniciais(0)
    _registrar("8.4: ioctl None, env None: retorna (80,24)", r_ini_nada == (80, 24))

    # --- 8.5: _obter_dimensoes_apos_sigwinch ---
    print("")
    print("-- 8.5: _obter_dimensoes_apos_sigwinch --")

    buf_120_40 = _struct.pack("HHHH", 40, 120, 0, 0)
    with _patch("fcntl.ioctl", return_value=buf_120_40):
        r_sw_ioctl = _obter_dimensoes_apos_sigwinch(0, (80, 24))
    _registrar("8.5: ioctl valido retorna par ioctl (120,40)", r_sw_ioctl == (120, 40))

    env_sw = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_sw.update({"LINES": "30", "COLUMNS": "100"})
    with _patch("fcntl.ioctl", side_effect=OSError), \
         _patch.dict(os.environ, env_sw, clear=True):
        r_sw_env = _obter_dimensoes_apos_sigwinch(0, (80, 24))
    _registrar("8.5: ioctl None, env valido: retorna par env", r_sw_env == (100, 30))

    env_sw_vazio = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    with _patch("fcntl.ioctl", side_effect=OSError), \
         _patch.dict(os.environ, env_sw_vazio, clear=True):
        r_sw_ultimas = _obter_dimensoes_apos_sigwinch(0, (120, 40))
    _registrar("8.5: todas fontes falham: retorna ultimas_validas", r_sw_ultimas == (120, 40))
    _registrar("8.5: (80,24) nao aparece com ultimas_validas=(120,40)", r_sw_ultimas != (80, 24))

    # --- 8.6: Handler de SIGWINCH ---
    print("")
    print("-- 8.6: Handler de SIGWINCH --")

    with _patch("signal.signal") as _mock_signal_install:
        _mock_signal_install.return_value = signal.SIG_DFL
        h_ant_test = _instalar_handler_sigwinch(99, [False])
    _registrar(
        "8.6: _instalar_handler_sigwinch chama signal.signal com SIGWINCH",
        _mock_signal_install.called and _mock_signal_install.call_args[0][0] == signal.SIGWINCH,
    )
    _registrar("8.6: retorna handler anterior", h_ant_test == signal.SIG_DFL)

    # Verificar que chamadas efetivas a _instalar_handler_sigwinch ocorrem
    # apenas no ramo TTY (inspecao de codigo-fonte)
    _texto_demo_8 = (_BASE_PADRAO / "demo" / "demo.py").read_text(encoding="utf-8")
    _linhas_demo_8 = _texto_demo_8.split("\n")
    _chamadas_efetivas_h = [
        l for l in _linhas_demo_8
        if "_instalar_handler_sigwinch(" in l and not l.strip().startswith("def ")
    ]
    _registrar(
        "8.6: _instalar_handler_sigwinch chamado exatamente uma vez (no ramo TTY)",
        len(_chamadas_efetivas_h) == 1,
        "chamadas={0}".format(len(_chamadas_efetivas_h)),
    )

    # --- 8.7: Flag, pipe e coalescencia ---
    print("")
    print("-- 8.7: Flag, pipe e coalescencia --")

    # Pipe nao bloqueante
    r_nb, w_nb = os.pipe()
    try:
        os.set_blocking(r_nb, False)
        os.set_blocking(w_nb, False)
        _registrar("8.7: r_wakeup nao bloqueante", not os.get_blocking(r_nb))
        _registrar("8.7: w_wakeup nao bloqueante", not os.get_blocking(w_nb))
    finally:
        try:
            os.close(r_nb)
        except OSError:
            pass
        try:
            os.close(w_nb)
        except OSError:
            pass

    # Handler escreve no pipe e define flag
    r_h, w_h = os.pipe()
    try:
        os.set_blocking(r_h, False)
        os.set_blocking(w_h, False)
        pend_h = [False]
        h_ant_h = _instalar_handler_sigwinch(w_h, pend_h)
        try:
            handler_atual = signal.getsignal(signal.SIGWINCH)
            handler_atual(signal.SIGWINCH, None)
            _registrar("8.7: handler define resize_pendente[0]=True", pend_h[0])
            dados_h = os.read(r_h, 64)
            _registrar("8.7: handler escreve pelo menos um byte no pipe", len(dados_h) >= 1)
        finally:
            _restaurar_handler_sigwinch(h_ant_h)
    finally:
        try:
            os.close(r_h)
        except OSError:
            pass
        try:
            os.close(w_h)
        except OSError:
            pass

    # Pipe cheio: BlockingIOError silenciada, flag permanece True
    r_pf, w_pf = os.pipe()
    try:
        os.set_blocking(r_pf, False)
        os.set_blocking(w_pf, False)
        pend_pf = [False]
        h_ant_pf = _instalar_handler_sigwinch(w_pf, pend_pf)
        _exc_pf_propagou = [False]
        try:
            with _patch("os.write", side_effect=BlockingIOError("pipe cheio")):
                try:
                    handler_pf = signal.getsignal(signal.SIGWINCH)
                    handler_pf(signal.SIGWINCH, None)
                except Exception:
                    _exc_pf_propagou[0] = True
            _registrar("8.7: pipe cheio: nenhuma excecao propaga do handler", not _exc_pf_propagou[0])
            _registrar("8.7: pipe cheio: resize_pendente[0] permanece True", pend_pf[0])
        finally:
            _restaurar_handler_sigwinch(h_ant_pf)
    finally:
        try:
            os.close(r_pf)
        except OSError:
            pass
        try:
            os.close(w_pf)
        except OSError:
            pass

    # Coalescencia: multiplos sinais -> apenas uma notificacao
    r_co, w_co = os.pipe()
    try:
        os.set_blocking(r_co, False)
        os.set_blocking(w_co, False)
        pend_co = [False]
        h_ant_co = _instalar_handler_sigwinch(w_co, pend_co)
        try:
            handler_co = signal.getsignal(signal.SIGWINCH)
            # Primeira chamada: escreve no pipe
            handler_co(signal.SIGWINCH, None)
            # Chamadas subsequentes: pipe cheio (simulado)
            with _patch("os.write", side_effect=BlockingIOError("pipe cheio")):
                handler_co(signal.SIGWINCH, None)
                handler_co(signal.SIGWINCH, None)
            _registrar("8.7: coalescencia: flag permanece True apos multiplos sinais", pend_co[0])
            # Drena o pipe
            total_co = b""
            while True:
                try:
                    chunk = os.read(r_co, 64)
                    if not chunk:
                        break
                    total_co += chunk
                except BlockingIOError:
                    break
            _registrar("8.7: coalescencia: drenagem le bytes disponiveis", len(total_co) >= 1)
        finally:
            _restaurar_handler_sigwinch(h_ant_co)
    finally:
        try:
            os.close(r_co)
        except OSError:
            pass
        try:
            os.close(w_co)
        except OSError:
            pass

    # Drenagem nao bloqueante
    r_dr, w_dr = os.pipe()
    try:
        os.set_blocking(r_dr, False)
        os.write(w_dr, b"abc")
        total_dr = b""
        while True:
            try:
                chunk = os.read(r_dr, 64)
                if not chunk:
                    break
                total_dr += chunk
            except BlockingIOError:
                break
            except OSError:
                break
        _registrar("8.7: drenagem: le todos os bytes e termina", len(total_dr) == 3)
        # Pipe vazio deve retornar EAGAIN
        try:
            os.read(r_dr, 64)
            _registrar("8.7: drenagem: pipe vazio -> vazio ou EAGAIN", True)
        except BlockingIOError:
            _registrar("8.7: drenagem: pipe vazio -> BlockingIOError (EAGAIN)", True)
    finally:
        try:
            os.close(r_dr)
        except OSError:
            pass
        try:
            os.close(w_dr)
        except OSError:
            pass

    # --- 8.8: Loop com select (integracao via mock) ---
    print("")
    print("-- 8.8: Loop com select (integracao via mock) --")

    # Resize valido: _apresentar_quadro chamado com nova largura
    # Estrategia: interceptar os.pipe() para capturar o r_wakeup real que
    # main() cria; usar esse fd no mock de select.select para simular wakeup.
    _pq_calls_8 = []
    _estado_saindo_8 = {
        "tipo_borda": "curva", "saindo": True,
        "tela_atual": "demo", "pilha_telas": [],
    }
    _estado_normal_8 = {
        "tipo_borda": "curva", "saindo": False,
        "tela_atual": "demo", "pilha_telas": [],
    }

    _captured_r_wakeup = [None]
    _select_calls_8 = [0]
    _orig_os_pipe = os.pipe

    def _pipe_capture_8():
        r, w = _orig_os_pipe()
        _captured_r_wakeup[0] = r
        return r, w

    def _select_side_8(rlist, wlist, xlist, *args):
        _select_calls_8[0] += 1
        r_wp = _captured_r_wakeup[0]
        if r_wp is not None and _select_calls_8[0] == 1 and r_wp in rlist:
            # Primeira chamada: simular wakeup pipe pronto + fd pronto
            return ([rlist[0], r_wp], [], [])
        return ([rlist[0]], [], [])

    def _pq_side_8(conteudo, largura=None):
        _pq_calls_8.append(largura)

    _sw_calls_8 = [0]
    def _sw_side_8(fd, ultimas):
        _sw_calls_8[0] += 1
        return (100, 30)

    _loop_cmd_8 = [0]
    def _processar_8(estado, ch, modelo=None):
        _loop_cmd_8[0] += 1
        if _loop_cmd_8[0] >= 2:
            return _estado_saindo_8
        return _estado_normal_8

    with _patch("demo.demo._apresentar_quadro", side_effect=_pq_side_8), \
         _patch("demo.demo.processar_comando", side_effect=_processar_8), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui"), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._obter_dimensoes_apos_sigwinch", side_effect=_sw_side_8), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("demo.demo._restaurar_handler_sigwinch"), \
         _patch("os.pipe", side_effect=_pipe_capture_8), \
         _patch("select.select", side_effect=_select_side_8), \
         _patch("sys.stdin") as _stdin_8, \
         _patch("sys.stdout") as _stdout_8:
        _stdin_8.isatty.return_value = True
        _stdin_8.fileno.return_value = 0
        _stdout_8.isatty.return_value = True
        _demo_mod.main()

    _registrar(
        "8.8: resize valido: _apresentar_quadro chamado com nova largura (100)",
        100 in _pq_calls_8,
        "larguras={0}".format(_pq_calls_8),
    )
    _registrar(
        "8.8: resize: _obter_dimensoes_apos_sigwinch chamado apos wakeup",
        _sw_calls_8[0] >= 1,
    )

    # Handler restaurado ao final (saida normal)
    _sig_rest_calls = []
    _SAINDO_8b = {
        "tipo_borda": "curva", "saindo": True,
        "tela_atual": "demo", "pilha_telas": [],
    }
    with _patch("demo.demo.processar_comando", return_value=_SAINDO_8b), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._apresentar_quadro"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui"), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("demo.demo._restaurar_handler_sigwinch",
                side_effect=lambda h: _sig_rest_calls.append(h)), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _stdin_8b, \
         _patch("sys.stdout") as _stdout_8b:
        _stdin_8b.isatty.return_value = True
        _stdin_8b.fileno.return_value = 0
        _stdout_8b.isatty.return_value = True
        _demo_mod.main()
    _registrar(
        "8.8: handler restaurado apos saida normal por Esc",
        len(_sig_rest_calls) == 1 and _sig_rest_calls[0] == signal.SIG_DFL,
    )

    # Handler restaurado apos excecao no loop
    _sig_rest_exc = []
    with _patch("demo.demo.processar_comando", side_effect=RuntimeError("loop fail")), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._apresentar_quadro"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui"), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("demo.demo._restaurar_handler_sigwinch",
                side_effect=lambda h: _sig_rest_exc.append(h)), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _stdin_8c, \
         _patch("sys.stdout") as _stdout_8c:
        _stdin_8c.isatty.return_value = True
        _stdin_8c.fileno.return_value = 0
        _stdout_8c.isatty.return_value = True
        try:
            _demo_mod.main()
        except RuntimeError:
            pass
    _registrar(
        "8.8: handler restaurado apos excecao no loop",
        len(_sig_rest_exc) >= 1,
    )

    # Handler restaurado ANTES do fechamento de w_wakeup
    _order_calls = []
    _orig_close = os.close
    def _close_track(fd):
        _order_calls.append(("close", fd))
        _orig_close(fd)

    with _patch("demo.demo.processar_comando", return_value=_SAINDO_8b), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._apresentar_quadro"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui"), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("demo.demo._restaurar_handler_sigwinch",
                side_effect=lambda h: _order_calls.append(("restore_handler", h))), \
         _patch("os.close", side_effect=_close_track), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _stdin_8d, \
         _patch("sys.stdout") as _stdout_8d:
        _stdin_8d.isatty.return_value = True
        _stdin_8d.fileno.return_value = 0
        _stdout_8d.isatty.return_value = True
        _demo_mod.main()

    _handler_before_close = False
    _handler_idx = next(
        (i for i, e in enumerate(_order_calls) if e[0] == "restore_handler"), None
    )
    _w_close_idx = next(
        (i for i, e in enumerate(_order_calls) if e[0] == "close"), None
    )
    if _handler_idx is not None and _w_close_idx is not None:
        _handler_before_close = _handler_idx < _w_close_idx
    _registrar(
        "8.8: handler restaurado antes do fechamento do pipe",
        _handler_before_close,
    )

    # --- 8.9: _quadro_minimo_aviso ---
    print("")
    print("-- 8.9: _quadro_minimo_aviso --")

    q80_24 = _quadro_minimo_aviso(80, 24)
    _registrar("8.9: (80,24): count newlines == 24", q80_24.count("\n") == 24)
    _registrar("8.9: (80,24): primeira linha comeca com 'terminal pequeno demais'",
               q80_24.split("\n")[0].startswith("terminal pequeno demais"))

    q9_3 = _quadro_minimo_aviso(9, 3)
    _registrar("8.9: (9,3): primeira linha comeca com 'tela peq.'",
               q9_3.split("\n")[0].startswith("tela peq."))

    q5_2 = _quadro_minimo_aviso(5, 2)
    _registrar("8.9: (5,2): primeira linha tem exatamente 5 chars antes do newline",
               len(q5_2.split("\n")[0]) == 5)
    _registrar("8.9: (5,2): primeira linha preenchida com espacos (limite fisico)",
               q5_2.split("\n")[0] == "     ")
    _registrar("8.9: (5,2): '!' nao aparece como mensagem normativa",
               "!" not in q5_2)

    q23_1 = _quadro_minimo_aviso(23, 1)
    _registrar("8.9: (23,1): count newlines == 1", q23_1.count("\n") == 1)
    _registrar("8.9: (23,1): unica linha tem exatamente 23 chars",
               len(q23_1.split("\n")[0]) == 23)

    for _ql, _qa in [(1, 1), (3, 5), (10, 6), (80, 24), (200, 50)]:
        _qr = _quadro_minimo_aviso(_ql, _qa)
        _registrar(
            "8.9: ({0},{1}) count newlines == altura".format(_ql, _qa),
            _qr.count("\n") == _qa,
        )
        _max_len = max(len(ln) for ln in _qr.split("\n") if ln != "")
        _registrar(
            "8.9: ({0},{1}) nenhuma linha excede largura".format(_ql, _qa),
            _max_len <= _ql,
        )

    # --- 8.10: _tela_pequena_demais ---
    print("")
    print("-- 8.10: _tela_pequena_demais --")

    _registrar("8.10: (9,24) -> True", _tela_pequena_demais(9, 24))
    _registrar("8.10: (10,24) -> False", not _tela_pequena_demais(10, 24))
    _registrar("8.10: (80,5) -> True", _tela_pequena_demais(80, 5))
    _registrar("8.10: (80,6) -> False", not _tela_pequena_demais(80, 6))
    _registrar("8.10: (10,6) -> False", not _tela_pequena_demais(10, 6))
    _registrar("8.10: constantes: LARGURA_MINIMA_TELA=10", LARGURA_MINIMA_TELA == 10)
    _registrar("8.10: constantes: ALTURA_MINIMA_TELA=6", ALTURA_MINIMA_TELA == 6)

    # --- 8.11: _apresentar_quadro com parametro largura ---
    print("")
    print("-- 8.11: _apresentar_quadro com parametro largura --")

    _escritas_com_l = []
    _shutil_chamado = [False]

    class _MockOut11:
        def write(self, s):
            _escritas_com_l.append(s)
        def flush(self):
            pass

    class _FakeTermSize11:
        columns = 99
        lines = 99

    def _shutil_track(*a, **kw):
        _shutil_chamado[0] = True
        return _FakeTermSize11()

    with _patch("sys.stdout", _MockOut11()), \
         _patch("shutil.get_terminal_size", side_effect=_shutil_track):
        _apresentar_quadro("AB\nCD\n", largura=20)

    _registrar("8.11: com largura=20: shutil.get_terminal_size nao chamado",
               not _shutil_chamado[0])
    _conteudo_20 = _escritas_com_l[0] if _escritas_com_l else ""
    _registrar("8.11: com largura=20: linha preenchida a 20 chars",
               "AB" + " " * 18 in _conteudo_20)

    _escritas_sem_l = []
    _shutil_chamado2 = [False]
    _shutil_cols = [0]

    class _MockOut11b:
        def write(self, s):
            _escritas_sem_l.append(s)
        def flush(self):
            pass

    class _FakeTermSize11b:
        columns = 15
        lines = 15

    def _shutil_track2(*a, **kw):
        _shutil_chamado2[0] = True
        return _FakeTermSize11b()

    with _patch("sys.stdout", _MockOut11b()), \
         _patch("shutil.get_terminal_size", side_effect=_shutil_track2):
        _apresentar_quadro("AB\nCD\n")

    _registrar("8.11: sem largura: shutil.get_terminal_size chamado",
               _shutil_chamado2[0])

    # --- 8.12: _resolver_conteudo ---
    print("")
    print("-- 8.12: _resolver_conteudo --")

    _estado_rc = {"tipo_borda": "curva", "saindo": False,
                  "tela_atual": "demo", "pilha_telas": []}
    _modelo_rc = _carregar_modelo_por_id("demo")

    r_rc_peq = _resolver_conteudo(_estado_rc, _modelo_rc, 5, 3)
    _registrar("8.12: terminal pequeno (5,3): retorna quadro minimo",
               r_rc_peq.count("\n") == 3)

    # H-0030: o demo com 7 itens no lancador requer altura >= 28 em
    # largura 80; dimensoes normais usam (80, 30) para que o render ocorra.
    r_rc_ok = _resolver_conteudo(_estado_rc, _modelo_rc, 80, 30)
    _registrar("8.12: dimensoes normais (80,30): retorna render normal",
               "ORQUESTRADOR" in r_rc_ok)
    _registrar("8.12: corpo.arranjo nao alterado apos resolver_conteudo",
               _modelo_rc.corpo.arranjo is not None)

    from tela.renderizador import RenderizadorErro as _RenderizadorErro
    with _patch("demo.demo.renderizar_estado", side_effect=_RenderizadorErro("r")):
        r_rc_err = _resolver_conteudo(_estado_rc, _modelo_rc, 80, 30)
    _registrar("8.12: RenderizadorErro: retorna quadro minimo",
               r_rc_err.count("\n") == 30)

    # --- 8.13: Falhas parciais na inicializacao e cleanup ---
    print("")
    print("-- 8.13: Falhas parciais --")

    # _iniciar_sessao_tui: rollback quando write falha
    _writes_rb = []
    def _write_rb(s):
        _writes_rb.append(s)
        if len(_writes_rb) == 1:
            raise ValueError("write falhou")

    _tsa_rb_calls = []
    with _patch("termios.tcgetattr", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("tty.setcbreak"), \
         _patch("termios.tcsetattr",
                side_effect=lambda *a: _tsa_rb_calls.append(a)), \
         _patch("sys.stdout") as _mock_out_rb:
        _mock_out_rb.write.side_effect = _write_rb
        _mock_out_rb.flush.return_value = None
        _exc_rb = None
        try:
            _iniciar_sessao_tui(0)
        except ValueError as e:
            _exc_rb = e

    _registrar("8.13: write falha: excecao original propagada", _exc_rb is not None)
    _registrar("8.13: write falha: tentativa de restauracao visual",
               len(_writes_rb) >= 2 and
               any("\x1b[?7h\x1b[?25h\x1b[?1049l" in w for w in _writes_rb[1:]))
    _registrar("8.13: write falha: termios restaurado apos rollback visual",
               len(_tsa_rb_calls) >= 1)
    _registrar("8.13: write falha: nao ha \\x1b[2J no rollback",
               all("\x1b[2J" not in w for w in _writes_rb[1:]))

    # _iniciar_sessao_tui: rollback quando flush falha
    _writes_fl = []
    def _write_fl(s):
        _writes_fl.append(s)

    _flush_fl_calls = [0]
    def _flush_fl():
        _flush_fl_calls[0] += 1
        if _flush_fl_calls[0] == 1:
            raise ValueError("flush falhou")

    _tsa_fl_calls = []
    with _patch("termios.tcgetattr", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("tty.setcbreak"), \
         _patch("termios.tcsetattr",
                side_effect=lambda *a: _tsa_fl_calls.append(a)), \
         _patch("sys.stdout") as _mock_out_fl:
        _mock_out_fl.write.side_effect = _write_fl
        _mock_out_fl.flush.side_effect = _flush_fl
        _exc_fl = None
        try:
            _iniciar_sessao_tui(0)
        except ValueError as e:
            _exc_fl = e

    _registrar("8.13: flush falha: excecao original propagada", _exc_fl is not None)
    _registrar("8.13: flush falha: termios restaurado", len(_tsa_fl_calls) >= 1)

    # _iniciar_sessao_tui: tcgetattr falha -> sem rollback visual
    _writes_tga = []
    _tsa_tga_calls = []
    with _patch("termios.tcgetattr", side_effect=OSError("tcgetattr failed")), \
         _patch("tty.setcbreak"), \
         _patch("sys.stdout") as _mock_out_tga:
        _mock_out_tga.write.side_effect = lambda s: _writes_tga.append(s)
        _mock_out_tga.flush.return_value = None
        _exc_tga = None
        try:
            _iniciar_sessao_tui(0)
        except OSError as e:
            _exc_tga = e

    _registrar("8.13: tcgetattr falha: excecao propagada", _exc_tga is not None)
    _registrar("8.13: tcgetattr falha: nenhuma escrita visual (nenhuma modificacao aplicada)",
               len(_writes_tga) == 0)

    # _restaurar_efeitos_visuais_tui: nao lanca excecao propria quando write/flush falham
    _exc_rev = None
    with _patch("sys.stdout") as _mock_out_rev:
        _mock_out_rev.write.side_effect = Exception("write fail")
        _mock_out_rev.flush.side_effect = Exception("flush fail")
        try:
            _restaurar_efeitos_visuais_tui()
        except Exception as e:
            _exc_rev = e
    _registrar("8.13: _restaurar_efeitos_visuais_tui nao propaga excecao",
               _exc_rev is None)

    # Rollback interno: write do rollback falha -> termios ainda tentado
    _writes_rb2 = []
    _tsa_rb2_calls = []
    _write_rb2_count = [0]
    def _write_rb2(s):
        _write_rb2_count[0] += 1
        _writes_rb2.append(s)
        raise ValueError("write fail")

    with _patch("termios.tcgetattr", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("tty.setcbreak"), \
         _patch("termios.tcsetattr",
                side_effect=lambda *a: _tsa_rb2_calls.append(a)), \
         _patch("sys.stdout") as _mock_out_rb2:
        _mock_out_rb2.write.side_effect = _write_rb2
        _mock_out_rb2.flush.return_value = None
        _exc_rb2 = None
        try:
            _iniciar_sessao_tui(0)
        except ValueError as e:
            _exc_rb2 = e

    _registrar("8.13: rollback visual falha: termios ainda tentado", len(_tsa_rb2_calls) >= 1)
    _registrar("8.13: rollback visual falha: excecao original preservada", _exc_rb2 is not None)

    # Coerencia: rollback e encerramento normal usam a mesma sequencia visual
    _writes_enc = []
    _tsa_enc_calls = []
    with _patch("termios.tcsetattr", side_effect=lambda *a: _tsa_enc_calls.append(a)), \
         _patch("sys.stdout") as _mock_enc:
        _mock_enc.write.side_effect = lambda s: _writes_enc.append(s)
        _mock_enc.flush.return_value = None
        _encerrar_sessao_tui(0, [0, 0, 0, 0, 0, 0, []])

    _seq_enc = next((w for w in _writes_enc if "\x1b[?7h" in w), None)
    _registrar("8.13: _encerrar_sessao_tui usa _restaurar_efeitos_visuais_tui",
               _seq_enc is not None and "\x1b[?7h\x1b[?25h\x1b[?1049l" in _seq_enc)
    _registrar("8.13: _encerrar_sessao_tui: \\x1b[2J nao presente na restauracao",
               all("\x1b[2J" not in w for w in _writes_enc))

    # Falha em os.pipe(): _iniciar_sessao_tui e _encerrar_sessao_tui nao chamados
    with _patch("os.pipe", side_effect=OSError("pipe fail")), \
         _patch("demo.demo._iniciar_sessao_tui") as _mock_init_fp, \
         _patch("demo.demo._encerrar_sessao_tui") as _mock_enc_fp, \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("sys.stdin") as _mock_stdin_fp, \
         _patch("sys.stdout") as _mock_stdout_fp:
        _mock_stdin_fp.isatty.return_value = True
        _mock_stdin_fp.fileno.return_value = 0
        _mock_stdout_fp.isatty.return_value = True
        _exc_fp = None
        try:
            _demo_mod.main()
        except OSError as e:
            _exc_fp = e
    _registrar("8.13: os.pipe() falha: excecao propagada", _exc_fp is not None)
    _registrar("8.13: os.pipe() falha: _iniciar_sessao_tui nao chamado",
               not _mock_init_fp.called)
    _registrar("8.13: os.pipe() falha: _encerrar_sessao_tui nao chamado",
               not _mock_enc_fp.called)

    # Falha em set_blocking(r_wakeup): ambos os fds fechados pelo finally
    _fds_sb = []
    _orig_pipe_sb = os.pipe
    def _pipe_sb_track():
        r, w = _orig_pipe_sb()
        _fds_sb.extend([r, w])
        return r, w

    with _patch("os.pipe", side_effect=_pipe_sb_track), \
         _patch("os.set_blocking", side_effect=OSError("set_blocking fail")), \
         _patch("demo.demo._iniciar_sessao_tui") as _mock_init_sb, \
         _patch("demo.demo._encerrar_sessao_tui") as _mock_enc_sb, \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("sys.stdin") as _mock_stdin_sb, \
         _patch("sys.stdout") as _mock_stdout_sb:
        _mock_stdin_sb.isatty.return_value = True
        _mock_stdin_sb.fileno.return_value = 0
        _mock_stdout_sb.isatty.return_value = True
        try:
            _demo_mod.main()
        except OSError:
            pass

    _registrar("8.13: set_blocking falha: _iniciar_sessao_tui nao chamado",
               not _mock_init_sb.called)
    if len(_fds_sb) >= 2:
        _r_sb, _w_sb = _fds_sb[0], _fds_sb[1]
        try:
            os.fstat(_r_sb)
            _r_closed = False
        except OSError:
            _r_closed = True
        try:
            os.fstat(_w_sb)
            _w_closed = False
        except OSError:
            _w_closed = True
        _registrar("8.13: set_blocking falha: r_wakeup fechado", _r_closed)
        _registrar("8.13: set_blocking falha: w_wakeup fechado", _w_closed)
    else:
        _registrar("8.13: set_blocking falha: fds fechados (pipe nao criado)", False)

    # _iniciar_sessao_tui falha: sessao_iniciada permanece False, pipe fechado
    _fds_it = []
    def _pipe_it_track():
        r, w = _orig_pipe_sb()
        _fds_it.extend([r, w])
        return r, w

    with _patch("os.pipe", side_effect=_pipe_it_track), \
         _patch("demo.demo._iniciar_sessao_tui",
                side_effect=RuntimeError("init fail")), \
         _patch("demo.demo._encerrar_sessao_tui") as _mock_enc_it, \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("sys.stdin") as _mock_stdin_it, \
         _patch("sys.stdout") as _mock_stdout_it:
        _mock_stdin_it.isatty.return_value = True
        _mock_stdin_it.fileno.return_value = 0
        _mock_stdout_it.isatty.return_value = True
        _exc_it = None
        try:
            _demo_mod.main()
        except RuntimeError as e:
            _exc_it = e
    _registrar("8.13: _iniciar_sessao_tui falha: excecao propagada", _exc_it is not None)
    _registrar("8.13: _iniciar_sessao_tui falha: _encerrar_sessao_tui nao chamado",
               not _mock_enc_it.called)
    if len(_fds_it) >= 2:
        _r_it, _w_it = _fds_it[0], _fds_it[1]
        try:
            os.fstat(_r_it)
            _r_it_closed = False
        except OSError:
            _r_it_closed = True
        try:
            os.fstat(_w_it)
            _w_it_closed = False
        except OSError:
            _w_it_closed = True
        _registrar("8.13: _iniciar_sessao_tui falha: r_wakeup fechado", _r_it_closed)
        _registrar("8.13: _iniciar_sessao_tui falha: w_wakeup fechado", _w_it_closed)
    else:
        _registrar("8.13: _iniciar_sessao_tui falha: fds fechados (pipe nao criado)", False)

    # _instalar_handler_sigwinch falha: handler_instalado permanece False
    with _patch("demo.demo._instalar_handler_sigwinch",
                side_effect=OSError("signal fail")), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui") as _mock_enc_sig, \
         _patch("demo.demo._restaurar_handler_sigwinch") as _mock_rest_sig, \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _mock_stdin_sig, \
         _patch("sys.stdout") as _mock_stdout_sig:
        _mock_stdin_sig.isatty.return_value = True
        _mock_stdin_sig.fileno.return_value = 0
        _mock_stdout_sig.isatty.return_value = True
        _exc_sig = None
        try:
            _demo_mod.main()
        except OSError as e:
            _exc_sig = e
    _registrar("8.13: signal.signal falha: excecao propagada", _exc_sig is not None)
    _registrar("8.13: signal.signal falha: _restaurar_handler_sigwinch nao chamado",
               not _mock_rest_sig.called)
    _registrar("8.13: signal.signal falha: _encerrar_sessao_tui chamado (sessao foi iniciada)",
               _mock_enc_sig.called)

    # _restaurar_handler_sigwinch silencia erros internamente (nao propaga)
    # Portanto falha interna nunca bloqueia _encerrar_sessao_tui no finally
    _cleanup_seq = []
    with _patch("demo.demo.processar_comando", return_value=_SAINDO_8b), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._apresentar_quadro"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui",
                side_effect=lambda *a: _cleanup_seq.append("encerrar")), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("demo.demo._restaurar_handler_sigwinch",
                side_effect=lambda *a: _cleanup_seq.append("restore_handler")), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _mock_stdin_cl, \
         _patch("sys.stdout") as _mock_stdout_cl:
        _mock_stdin_cl.isatty.return_value = True
        _mock_stdin_cl.fileno.return_value = 0
        _mock_stdout_cl.isatty.return_value = True
        _demo_mod.main()

    _registrar(
        "8.13: _restaurar_handler_sigwinch chamado antes de _encerrar_sessao_tui",
        "restore_handler" in _cleanup_seq and "encerrar" in _cleanup_seq and
        _cleanup_seq.index("restore_handler") < _cleanup_seq.index("encerrar"),
    )

    # _restaurar_handler_sigwinch silencia excecoes internas (signal.signal falhando)
    _exc_sig_rest = None
    try:
        with _patch("signal.signal", side_effect=OSError("signal.signal fail")):
            _restaurar_handler_sigwinch(signal.SIG_DFL)
    except Exception as _e:
        _exc_sig_rest = _e
    _registrar(
        "8.13: _restaurar_handler_sigwinch silencia OSError de signal.signal",
        _exc_sig_rest is None,
    )

    # Excecao original preservada mesmo quando signal.signal falha no restore
    # _restaurar_handler_sigwinch tem try/except interno, logo nunca propaga;
    # a excecao original do loop (RuntimeError) e sempre preservada.
    _exc_primary = None
    with _patch("demo.demo.processar_comando",
                side_effect=RuntimeError("primary error")), \
         _patch("demo.demo._ler_tecla_sessao", return_value="x"), \
         _patch("demo.demo._apresentar_quadro"), \
         _patch("demo.demo._iniciar_sessao_tui", return_value=[0, 0, 0, 0, 0, 0, []]), \
         _patch("demo.demo._encerrar_sessao_tui"), \
         _patch("demo.demo._carregar_modelo_por_id", return_value=object()), \
         _patch("demo.demo._instalar_handler_sigwinch", return_value=signal.SIG_DFL), \
         _patch("signal.signal", side_effect=OSError("signal fail during restore")), \
         _patch("select.select", return_value=([0], [], [])), \
         _patch("sys.stdin") as _mock_stdin_ep, \
         _patch("sys.stdout") as _mock_stdout_ep:
        _mock_stdin_ep.isatty.return_value = True
        _mock_stdin_ep.fileno.return_value = 0
        _mock_stdout_ep.isatty.return_value = True
        try:
            _demo_mod.main()
        except RuntimeError as e:
            _exc_primary = e
        except Exception:
            pass  # outras excecoes nao sao o foco aqui
    _registrar(
        "8.13: excecao original (RuntimeError) preservada mesmo com signal.signal falhando",
        isinstance(_exc_primary, RuntimeError) and "primary error" in str(_exc_primary),
    )

    # Nao-TTY: handler de SIGWINCH nao instalado
    _sigwinch_installed_notty = [False]
    def _track_sigwinch_install(*a, **kw):
        _sigwinch_installed_notty[0] = True
        return signal.SIG_DFL

    # H-0030: o demo com 7 itens requer altura >= 28 em largura 80;
    # o env do nao-TTY define COLUMNS=80/LINES=30 para que a demo renderize.
    env_notty = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_notty["COLUMNS"] = "80"
    env_notty["LINES"] = "30"
    with _patch("demo.demo._instalar_handler_sigwinch",
                side_effect=_track_sigwinch_install), \
         _patch.dict(os.environ, env_notty, clear=False), \
         _patch("sys.stdin") as _mock_stdin_nt, \
         _patch("sys.stdout") as _mock_stdout_nt:
        _mock_stdin_nt.isatty.return_value = False
        _mock_stdout_nt.isatty.return_value = False
        _mock_stdin_nt.__iter__ = lambda self: iter([])
        _demo_mod.main()
    _registrar("8.13: nao-TTY: _instalar_handler_sigwinch nao chamado",
               not _sigwinch_installed_notty[0])

    # --- 8.14: Regressao fluxo nao-TTY ---
    print("")
    print("-- 8.14: Regressao nao-TTY --")

    # H-0030: o demo com 7 itens requer altura >= 28 em largura 80;
    # o env do nao-TTY define COLUMNS=80/LINES=30 para que a demo renderize.
    env_sem_dims = {k: v for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")}
    env_sem_dims["COLUMNS"] = "80"
    env_sem_dims["LINES"] = "30"
    proc_notty = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="b\ns\n",
        capture_output=True,
        text=True,
        env=env_sem_dims,
    )
    _registrar("8.14: nao-TTY subprocess 'b\\ns\\n' encerra com codigo 0",
               proc_notty.returncode == 0)
    _registrar("8.14: nao-TTY stdout nao contem \\x1b[?1049h",
               "\x1b[?1049h" not in proc_notty.stdout)
    _registrar("8.14: nao-TTY stdout nao contem sequencias SIGWINCH",
               "SIGWINCH" not in proc_notty.stdout)
    _registrar("8.14: nao-TTY stderr vazio", proc_notty.stderr == "")

    # --- 8.15: Inspecao: \x1b[2J somente na entrada ---
    print("")
    print("-- 8.15: Inspecao de codigo --")

    _texto_demo_insp = (_BASE_PADRAO / "demo" / "demo.py").read_text(encoding="utf-8")
    _count_2j = _texto_demo_insp.count("\\x1b[2J")
    _registrar("8.15: \\x1b[2J aparece exatamente uma vez no codigo",
               _count_2j == 1, "count={0}".format(_count_2j))
    _registrar("8.15: 'fcntl' importado no demo.py",
               "import fcntl" in _texto_demo_insp)
    _registrar("8.15: 'struct' importado no demo.py",
               "import struct" in _texto_demo_insp)
    _registrar("8.15: 'signal' importado no demo.py",
               "import signal" in _texto_demo_insp)
    _registrar("8.15: RenderizadorErro importado no demo.py",
               "RenderizadorErro" in _texto_demo_insp)
    _registrar("8.15: LARGURA_MINIMA_TELA = 10 no codigo",
               "LARGURA_MINIMA_TELA = 10" in _texto_demo_insp)
    _registrar("8.15: ALTURA_MINIMA_TELA = 6 no codigo",
               "ALTURA_MINIMA_TELA = 6" in _texto_demo_insp)
    _registrar("8.15: select.select com dois descritores (select duplo)",
               "select.select([fd, r_wakeup]" in _texto_demo_insp)

    # --- 8.16: Pseudo-TTY: redimensionamento reativo completo ---
    print("")
    print("-- 8.16: Pseudo-TTY (pty.openpty): reducao -> redraw -> ampliacao --")

    def _ler_pty_ate_ocioso(fd_master, timeout_total, ocioso):
        """Le do master PTY com deadline explicito, ate ficar ocioso.

        Usa ``select`` com deadline (nao depende apenas de ``time.sleep``).
        Drena todos os bytes disponiveis e encerra quando nao chega dado novo
        por ``ocioso`` segundos apos algum dado, ou quando ``timeout_total``
        expira. Retorna os bytes acumulados. Nunca fica pendurado: o laco e
        limitado por ``timeout_total``.
        """
        import select as _sel
        import time as _t
        dados = b""
        fim = _t.monotonic() + timeout_total
        ultimo_dado = None
        while _t.monotonic() < fim:
            restante = fim - _t.monotonic()
            prontos, _, _ = _sel.select(
                [fd_master], [], [], min(0.1, max(0.0, restante))
            )
            if prontos:
                try:
                    chunk = os.read(fd_master, 4096)
                except (BlockingIOError, OSError):
                    chunk = b""
                if chunk:
                    dados += chunk
                    ultimo_dado = _t.monotonic()
                    continue
            if ultimo_dado is not None and (_t.monotonic() - ultimo_dado) >= ocioso:
                break
        return dados

    def _linhas_ultimo_quadro(saida_bytes):
        """Extrai as linhas visiveis do ultimo quadro synchronized-output.

        Localiza o ultimo bloco entre ``ESC[?2026h`` e ``ESC[?2026l``, separa
        por marcadores de posicionamento absoluto ``ESC[<n>;1H`` e remove as
        demais sequencias ANSI de cada segmento. Retorna a lista de linhas de
        texto visivel do quadro (uma por posicionamento), permitindo medir
        numero de linhas e largura apos remocao controlada das sequencias.
        """
        import re as _re
        _esc = "\x1b"
        texto = saida_bytes.decode("utf-8", errors="replace")
        inicio = texto.rfind(_esc + "[?2026h")
        if inicio == -1:
            return []
        fim = texto.find(_esc + "[?2026l", inicio)
        bloco = texto[inicio:fim] if fim != -1 else texto[inicio:]
        partes = _re.split(_esc + r"\[\d+;1H", bloco)
        linhas = []
        for parte in partes[1:]:
            limpa = _re.sub(_esc + r"\[[0-9;?]*[A-Za-z]", "", parte)
            linhas.append(limpa)
        return linhas

    _pseudo_pty_executado = [False]
    _pseudo_pty_limitacoes = []

    try:
        import pty as _pty
        import struct as _struct_pty

        _master_fd = None
        _slave_fd = None
        _proc_pty = None

        # Dimensoes deterministas:
        #   normal   40x30 -> tela normal (contem "ORQUESTRADOR")
        #   reduzido 30x5  -> quadro minimo ("terminal pequeno demais"): altura < 6
        #   ampliado 40x30 -> tela normal restaurada
        # H-0030: o demo com 7 itens no lancador requer altura >= 28
        # mesmo em largura 40; _LINS_NORM subiu de 20 para 30.
        _COLS_NORM, _LINS_NORM = 40, 30
        _COLS_RED, _LINS_RED = 30, 5

        try:
            import fcntl as _fcntl_pty
            import termios as _termios_pty

            _master_fd, _slave_fd = _pty.openpty()

            _win_ini = _struct_pty.pack("HHHH", _LINS_NORM, _COLS_NORM, 0, 0)
            _fcntl_pty.ioctl(_slave_fd, _termios_pty.TIOCSWINSZ, _win_ini)

            _proc_pty = subprocess.Popen(
                [sys.executable, "demo/demo.py"],
                stdin=_slave_fd,
                stdout=_slave_fd,
                stderr=_slave_fd,
                cwd=str(_BASE_PADRAO),
                close_fds=True,
            )

            os.close(_slave_fd)
            _slave_fd = None
            os.set_blocking(_master_fd, False)

            # --- Fase 1: estado normal inicial ---
            _saida_inicial = _ler_pty_ate_ocioso(_master_fd, 3.0, 0.3)
            _vivo_inicial = _proc_pty.poll() is None
            _quadro_inicial_ok = (
                _vivo_inicial
                and len(_saida_inicial) > 0
                and b"\x1b[?2026h" in _saida_inicial
                and b"ORQUESTRADOR" in _saida_inicial
            )
            _registrar(
                "PTY: quadro inicial capturado (processo ativo, quadro TUI, conteudo normal)",
                _quadro_inicial_ok,
                "vivo={0} bytes={1}".format(_vivo_inicial, len(_saida_inicial)),
            )

            # --- Fase 2: reducao -> quadro minimo ---
            _win_red = _struct_pty.pack("HHHH", _LINS_RED, _COLS_RED, 0, 0)
            _fcntl_pty.ioctl(_master_fd, _termios_pty.TIOCSWINSZ, _win_red)
            os.kill(_proc_pty.pid, signal.SIGWINCH)
            _saida_reducao = _ler_pty_ate_ocioso(_master_fd, 3.0, 0.3)
            _vivo_reducao = _proc_pty.poll() is None

            _redraw_reducao = (
                len(_saida_reducao) > 0 and b"\x1b[?2026h" in _saida_reducao
            )
            _registrar(
                "PTY: reducao produziu redraw (novo quadro apos SIGWINCH, nao apenas processo ativo)",
                _redraw_reducao,
                "bytes={0}".format(len(_saida_reducao)),
            )

            _registrar(
                "PTY: quadro minimo apareceu na reducao ('terminal pequeno demais')",
                b"terminal pequeno demais" in _saida_reducao
                and b"ORQUESTRADOR" not in _saida_reducao,
            )

            _linhas_red = _linhas_ultimo_quadro(_saida_reducao)
            _maxw_red = max((len(l) for l in _linhas_red), default=0)
            _registrar(
                "PTY: quadro reduzido respeita dimensoes (<= {0} colunas e <= {1} linhas, sem linha extra)".format(
                    _COLS_RED, _LINS_RED
                ),
                len(_linhas_red) > 0
                and len(_linhas_red) <= _LINS_RED
                and _maxw_red <= _COLS_RED,
                "nlinhas={0} maxw={1}".format(len(_linhas_red), _maxw_red),
            )

            _registrar(
                "PTY: redraw de resize sem clear total (ESC[2J ausente na reducao)",
                b"\x1b[2J" not in _saida_reducao,
            )

            # --- Fase 3: ampliacao -> conteudo normal restaurado ---
            _win_amp = _struct_pty.pack("HHHH", _LINS_NORM, _COLS_NORM, 0, 0)
            _fcntl_pty.ioctl(_master_fd, _termios_pty.TIOCSWINSZ, _win_amp)
            os.kill(_proc_pty.pid, signal.SIGWINCH)
            _saida_ampliacao = _ler_pty_ate_ocioso(_master_fd, 3.0, 0.3)
            _vivo_ampliacao = _proc_pty.poll() is None

            _redraw_ampliacao = (
                len(_saida_ampliacao) > 0 and b"\x1b[?2026h" in _saida_ampliacao
            )
            _registrar(
                "PTY: ampliacao produziu redraw (novo quadro apos segundo SIGWINCH)",
                _redraw_ampliacao,
                "bytes={0}".format(len(_saida_ampliacao)),
            )

            _registrar(
                "PTY: conteudo normal retornou apos ampliacao ('ORQUESTRADOR' presente, quadro minimo ausente)",
                b"ORQUESTRADOR" in _saida_ampliacao
                and b"terminal pequeno demais" not in _saida_ampliacao,
            )

            _linhas_amp = _linhas_ultimo_quadro(_saida_ampliacao)
            _maxw_amp = max((len(l) for l in _linhas_amp), default=0)
            _registrar(
                "PTY: quadro ampliado usa novas dimensoes (<= {0} colunas e <= {1} linhas)".format(
                    _COLS_NORM, _LINS_NORM
                ),
                len(_linhas_amp) > 0
                and len(_linhas_amp) <= _LINS_NORM
                and _maxw_amp <= _COLS_NORM,
                "nlinhas={0} maxw={1}".format(len(_linhas_amp), _maxw_amp),
            )

            _registrar(
                "PTY: processo permaneceu ativo nos dois resizes",
                _vivo_reducao and _vivo_ampliacao,
                "reducao={0} ampliacao={1}".format(_vivo_reducao, _vivo_ampliacao),
            )

            # --- Fase 4: Esc e encerramento ---
            try:
                os.write(_master_fd, b"\x1b")
            except OSError:
                pass

            _encerrou_ok = True
            try:
                _proc_pty.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _encerrou_ok = False
                _proc_pty.kill()
                _proc_pty.wait()

            _registrar(
                "PTY: Esc encerrou o processo dentro do timeout",
                _encerrou_ok,
            )
            _registrar(
                "PTY: codigo de saida 0 apos Esc",
                _proc_pty.returncode == 0,
                "returncode={0}".format(_proc_pty.returncode),
            )
            _pseudo_pty_executado[0] = True

        except Exception as _pty_exc:
            _registrar("PTY: execucao sem excecao fatal", False,
                       "{0}".format(_pty_exc))
            _pseudo_pty_limitacoes.append(str(_pty_exc))
        finally:
            _cleanup_ok = True
            if _slave_fd is not None:
                try:
                    os.close(_slave_fd)
                except OSError:
                    _cleanup_ok = False
            if _master_fd is not None:
                try:
                    os.close(_master_fd)
                except OSError:
                    _cleanup_ok = False
            if _proc_pty is not None and _proc_pty.poll() is None:
                _proc_pty.kill()
                try:
                    _proc_pty.wait(timeout=2)
                except Exception:
                    _cleanup_ok = False
            _registrar("PTY: cleanup concluido (descritores fechados e processo finalizado)",
                       _cleanup_ok)

    except ImportError:
        _registrar("PTY: modulo pty disponivel", False, "import pty falhou")
        _pseudo_pty_limitacoes.append("modulo pty nao disponivel")



def teste_navegacao_h0030(modelo):
    """Smoke tests do ponto de entrada real para o catalogo H-0030 (14.6).

    Para cada chip 1..5:
    - processar_comando abre a tela_destino correta e empilha o demo;
    - subprocess (<chip>\\nEsc\\nEsc\\n) percorre o ciclo real
      demo -> chip -> tela correta -> Esc -> demo -> Esc -> exit;
    - a tela aberta e identificada pelo seu marcador de cabecalho;
    - o demo reaparece apos Esc (retorno comprovado).

    Preservacoes:
    - chips d e g continuam abrindo destino_minimo e grupo_minimo;
    - Esc na raiz encerra o subprocess com codigo 0.
    """
    print("")
    print("== Secao 4c - Catalogo H-0030: navegacao real pelos chips 1-5 ==")

    # Mapeamento: chip -> (id_tela, marcador de cabecalho, texto do lancador).
    chip_para_h0030 = [
        ("1", "h0030_console_unico", "H-0030 CONSOLE", "Console"),
        ("2", "h0030_dashboard_unico", "H-0030 DASHBOARD", "Dashboard"),
        ("3", "h0030_matriz_2x2", "H-0030 MATRIZ 2X2", "Matriz 2x2"),
        ("4", "h0030_matriz_3x2", "H-0030 MATRIZ 3X2", "Matriz 3x2"),
        ("5", "h0030_matriz_2x4", "H-0030 MATRIZ 2X4", "Matriz 2x4"),
    ]

    estado_raiz = {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "demo",
        "pilha_telas": [],
    }

    # --- processar_comando: cada chip abre a tela correta ---
    for chip, id_tela, _marker, _texto in chip_para_h0030:
        res = processar_comando(estado_raiz, chip, modelo)
        _registrar(
            "H-0030 proc: chip {0!r} abre tela_atual == {1!r}".format(chip, id_tela),
            res["tela_atual"] == id_tela,
            "tela_atual={0!r}".format(res.get("tela_atual")),
        )
        _registrar(
            "H-0030 proc: chip {0!r} empilha 'demo'".format(chip),
            res["pilha_telas"] == ["demo"],
            "pilha={0!r}".format(res.get("pilha_telas")),
        )
        _registrar(
            "H-0030 proc: chip {0!r} nao define saindo".format(chip),
            res["saindo"] is False,
        )

    # --- Ciclo real por subprocess: chip -> tela -> Esc -> demo ---
    env_h0030 = dict(
        (k, v) for k, v in os.environ.items() if k not in ("COLUMNS", "LINES")
    )
    env_h0030["COLUMNS"] = str(_LARGURA_SUBPROCESS)
    env_h0030["LINES"] = str(_ALTURA_SUBPROCESS)

    for chip, id_tela, marker, texto in chip_para_h0030:
        modelo_dest = _carregar_modelo_por_id(id_tela)
        esperado_orq = renderizar_tela(
            modelo, tipo_borda="curva",
            largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
        )
        esperado_dest = renderizar_tela(
            modelo_dest, tipo_borda="curva",
            largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS,
        )
        # Entrada: <chip> (abre) -> Esc (volta p/ demo) -> Esc (sai).
        entrada = "{0}\n\x1b\n\x1b\n".format(chip)
        proc = subprocess.run(
            [sys.executable, "demo/demo.py"],
            cwd=str(_BASE_PADRAO),
            input=entrada,
            capture_output=True,
            text=True,
            env=env_h0030,
        )
        _registrar(
            "H-0030 demo: chip {0!r} ciclo encerra com codigo 0".format(chip),
            proc.returncode == 0,
            "returncode={0}".format(proc.returncode),
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout)
            sys.stderr.write(proc.stderr)
        _registrar(
            "H-0030 demo: chip {0!r} abre {1!r} (marcador {2!r} presente)".format(
                chip, id_tela, marker
            ),
            marker in proc.stdout,
            "marker_presente={0}".format(marker in proc.stdout),
        )
        _registrar(
            "H-0030 demo: chip {0!r} stdout contem demo apos retorno".format(
                chip
            ),
            proc.stdout.count("ORQUESTRADOR") >= 2,
            "orq_count={0}".format(proc.stdout.count("ORQUESTRADOR")),
        )
        # O destino incorreto nao deve aparecer: nenhum marcador de outra tela
        # do catalogo pode estar presente (cada tela so aparece quando aberta).
        outros_markers = [m for c, _, m, _ in chip_para_h0030 if c != chip]
        _registrar(
            "H-0030 demo: chip {0!r} nao abre destino incorreto".format(chip),
            all(other not in proc.stdout or other == marker
                for other in outros_markers),
        )
        # Saida esperada: demo -> destino -> demo.
        saida_esperada = esperado_orq + esperado_dest + esperado_orq
        _registrar(
            "H-0030 demo: chip {0!r} gera 3 renders (orq,dest,orq) largura 80 altura 30".format(
                chip
            ),
            proc.stdout == saida_esperada,
            "" if proc.stdout == saida_esperada else "ver diff abaixo",
        )
        if proc.stdout != saida_esperada:
            print("--- esperado (repr) ---")
            print(repr(saida_esperada))
            print("--- stdout (repr) ---")
            print(repr(proc.stdout))
        _registrar(
            "H-0030 demo: chip {0!r} stderr vazio".format(chip),
            proc.stderr == "",
            "stderr={0!r}".format(proc.stderr),
        )
        # Altura deterministica propagada: 3 renders x 30 linhas = 90.
        _registrar(
            "H-0030 demo: chip {0!r} propaga altura=30 (stdout tem 90 newlines)".format(
                chip
            ),
            proc.stdout.count("\n") == 3 * _ALTURA_SUBPROCESS,
            "count={0}".format(proc.stdout.count("\n")),
        )

    # --- Preservacao dos fluxos existentes (d, g, Esc na raiz) ---
    print("")
    print("-- H-0030: preservacao dos chips d/g e Esc na raiz --")

    # d continua abrindo destino_minimo.
    res_d = processar_comando(estado_raiz, "d", modelo)
    _registrar(
        "H-0030 preservacao: chip 'd' continua abrindo destino_minimo",
        res_d["tela_atual"] == "destino_minimo",
        "tela_atual={0!r}".format(res_d.get("tela_atual")),
    )
    # g continua abrindo grupo_minimo.
    res_g = processar_comando(estado_raiz, "g", modelo)
    _registrar(
        "H-0030 preservacao: chip 'g' continua abrindo grupo_minimo",
        res_g["tela_atual"] == "grupo_minimo",
        "tela_atual={0!r}".format(res_g.get("tela_atual")),
    )

    # Esc na raiz encerra o subprocess (saida vigente por Esc na raiz).
    proc_esc_raiz = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO),
        input="\x1b\n",
        capture_output=True,
        text=True,
        env=env_h0030,
    )
    _registrar(
        "H-0030 preservacao: Esc na raiz encerra com codigo 0",
        proc_esc_raiz.returncode == 0,
        "returncode={0}".format(proc_esc_raiz.returncode),
    )
    _registrar(
        "H-0030 preservacao: Esc na raiz exibe demo (curva) uma vez",
        "ORQUESTRADOR" in proc_esc_raiz.stdout
        and proc_esc_raiz.stdout.count("ORQUESTRADOR") == 1,
        "orq_count={0}".format(proc_esc_raiz.stdout.count("ORQUESTRADOR")),
    )

    # Chips nao declarados (ex.: 'z') nao abrem destino algum.
    res_z = processar_comando(estado_raiz, "z", modelo)
    _registrar(
        "H-0030 preservacao: chip nao declarado 'z' nao altera tela_atual",
        res_z["tela_atual"] == "demo" and res_z["pilha_telas"] == [],
        "tela_atual={0!r}".format(res_z.get("tela_atual")),
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
    teste_redimensionamento_reativo_h0023()
    teste_navegacao_h0030(modelo)

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
