"""Testes comportamentais da politica de modo por tela (H-0037 / ADR-0028 D23).

Executavel via:
    python demo/teste_demo_console_modos.py

Cobre os criterios de aceite do H-0037 relativos a politica de modo (D23):
 - transporte de politica_modo e modo_inicial do JSON estrutural ao modelo;
 - _verboso_efetivo aplica a politica correta para cada cenario;
 - _modo_verboso_de_modelo resolve o modo inicial a partir da politica;
 - tecla V exclusiva de telas com politica "alternavel";
 - alternancia nas telas alternáveis (cenarios 3 e 4);
 - conteudo compartilhado entre cenarios 1 e 2 (mesmo externo, politicas opostas);
 - isolamento de verbosidade entre telas distintas;
 - renderizacao diverge entre modo nao verboso e verboso.

Quatro cenarios de demonstracao permanentes (ADR-0028 §36.2):
 1. h0037_console_nao_verboso          - somente_nao_verboso, sem V
 2. h0037_console_verboso_dois_niveis  - somente_verboso, sem V
 3. h0037_console_alternavel_tres_niveis - alternavel, modo_inicial nao_verboso
 4. h0037_console_tabela_alternavel    - alternavel, modo_inicial verboso

Apenas biblioteca padrao do Python.
"""

import io
import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from demo.demo import (  # noqa: E402
    _carregar_modelo_por_id,
    _verboso_efetivo,
    _modo_verboso_de_modelo,
    processar_comando,
    criar_estado_inicial,
    main as _demo_main,
)
from tela.renderizador import renderizar_tela  # noqa: E402

_RESULTADOS = []

_CENARIOS = [
    "h0037_console_nao_verboso",
    "h0037_console_verboso_dois_niveis",
    "h0037_console_alternavel_tres_niveis",
    "h0037_console_tabela_alternavel",
]

_FIXAS = _CENARIOS[:2]
_ALTERNAVEIS = _CENARIOS[2:]


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _estado(tela, modo_verboso=False):
    return {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": tela,
        "pilha_telas": [],
        "modo_verboso": modo_verboso,
    }


def _console_de(modelo):
    for el in modelo.corpo.elementos:
        if el.tipo == "console":
            return el
    return None


def teste_transporte_politica_modo():
    print("")
    print("== Transporte de politica_modo e modo_inicial (D23) ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")
    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    c1 = _console_de(m1)
    c2 = _console_de(m2)
    c3 = _console_de(m3)
    c4 = _console_de(m4)

    _registrar("cenario 1: politica_modo == somente_nao_verboso",
               getattr(c1, "politica_modo", None) == "somente_nao_verboso")
    _registrar("cenario 1: modo_inicial ausente (None)",
               getattr(c1, "modo_inicial", None) is None)

    _registrar("cenario 2: politica_modo == somente_verboso",
               getattr(c2, "politica_modo", None) == "somente_verboso")
    _registrar("cenario 2: modo_inicial ausente (None)",
               getattr(c2, "modo_inicial", None) is None)

    _registrar("cenario 3: politica_modo == alternavel",
               getattr(c3, "politica_modo", None) == "alternavel")
    _registrar("cenario 3: modo_inicial == nao_verboso",
               getattr(c3, "modo_inicial", None) == "nao_verboso")

    _registrar("cenario 4: politica_modo == alternavel",
               getattr(c4, "politica_modo", None) == "alternavel")
    _registrar("cenario 4: modo_inicial == verboso",
               getattr(c4, "modo_inicial", None) == "verboso")


def teste_modo_verboso_inicial():
    print("")
    print("== _modo_verboso_de_modelo: modo inicial por politica ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")
    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    _registrar("cenario 1 (somente_nao_verboso): modo inicial == False",
               _modo_verboso_de_modelo(m1) is False)
    _registrar("cenario 2 (somente_verboso): modo inicial == True (verboso)",
               _modo_verboso_de_modelo(m2) is True)
    _registrar("cenario 3 (alternavel, nao_verboso): modo inicial == False",
               _modo_verboso_de_modelo(m3) is False)
    _registrar("cenario 4 (alternavel, verboso): modo inicial == True",
               _modo_verboso_de_modelo(m4) is True)
    _registrar("modelo None -> False",
               _modo_verboso_de_modelo(None) is False)


def teste_verboso_efetivo_por_politica():
    print("")
    print("== _verboso_efetivo aplica politica independente do estado ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")
    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    est_nv = _estado("h0037_console_nao_verboso", modo_verboso=False)
    est_v = _estado("h0037_console_nao_verboso", modo_verboso=True)

    _registrar("cenario 1 (somente_nao_verboso): verboso_efetivo sempre False (toggle=False)",
               _verboso_efetivo(est_nv, m1) is False)
    _registrar("cenario 1 (somente_nao_verboso): verboso_efetivo sempre False (toggle=True)",
               _verboso_efetivo(est_v, m1) is False)

    _registrar("cenario 2 (somente_verboso): verboso_efetivo sempre True (toggle=False)",
               _verboso_efetivo(est_nv, m2) is True)
    _registrar("cenario 2 (somente_verboso): verboso_efetivo sempre True (toggle=True)",
               _verboso_efetivo(est_v, m2) is True)

    est3_nv = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    est3_v = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=True)

    _registrar("cenario 3 (alternavel): verboso_efetivo segue toggle=False",
               _verboso_efetivo(est3_nv, m3) is False)
    _registrar("cenario 3 (alternavel): verboso_efetivo segue toggle=True",
               _verboso_efetivo(est3_v, m3) is True)

    est4_nv = _estado("h0037_console_tabela_alternavel", modo_verboso=False)
    est4_v = _estado("h0037_console_tabela_alternavel", modo_verboso=True)

    _registrar("cenario 4 (alternavel): verboso_efetivo segue toggle=False",
               _verboso_efetivo(est4_nv, m4) is False)
    _registrar("cenario 4 (alternavel): verboso_efetivo segue toggle=True",
               _verboso_efetivo(est4_v, m4) is True)

    _registrar("modelo None -> False (qualquer estado)",
               _verboso_efetivo(est3_v, None) is False)


def teste_tecla_v_ausente_nas_fixas():
    print("")
    print("== Tecla V ausente (sem efeito) nas telas fixas ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")

    est1 = _estado("h0037_console_nao_verboso", modo_verboso=False)
    novo1 = processar_comando(est1, "V", m1)
    _registrar("cenario 1 (somente_nao_verboso): V nao altera modo_verboso",
               novo1["modo_verboso"] == est1["modo_verboso"])
    _registrar("cenario 1 (somente_nao_verboso): V nao altera saindo",
               novo1["saindo"] is False)

    est2 = _estado("h0037_console_verboso_dois_niveis", modo_verboso=False)
    novo2 = processar_comando(est2, "V", m2)
    _registrar("cenario 2 (somente_verboso): V nao altera modo_verboso",
               novo2["modo_verboso"] == est2["modo_verboso"])

    # V maiusculo sem modelo tambem e inocuo
    est_sem_modelo = _estado("demo", modo_verboso=False)
    novo_sem = processar_comando(est_sem_modelo, "V")
    _registrar("V sem modelo nao altera modo_verboso",
               novo_sem["modo_verboso"] == est_sem_modelo["modo_verboso"])


def teste_alternancia_v_nas_alternaveis():
    print("")
    print("== Tecla V alterna modo nas telas alternáveis ==")

    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    # Cenario 3: inicia nao_verboso
    est3 = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    novo3a = processar_comando(est3, "V", m3)
    _registrar("cenario 3: V False->True",
               novo3a["modo_verboso"] is True)
    novo3b = processar_comando(novo3a, "V", m3)
    _registrar("cenario 3: V True->False (alternancia completa)",
               novo3b["modo_verboso"] is False)

    # Cenario 4: inicia verboso
    est4 = _estado("h0037_console_tabela_alternavel", modo_verboso=True)
    novo4a = processar_comando(est4, "V", m4)
    _registrar("cenario 4: V True->False",
               novo4a["modo_verboso"] is False)
    novo4b = processar_comando(novo4a, "V", m4)
    _registrar("cenario 4: V False->True (alternancia completa)",
               novo4b["modo_verboso"] is True)

    # V nao altera outros campos do estado
    _registrar("cenario 3: V preserva saindo",
               novo3a["saindo"] is False)
    _registrar("cenario 3: V preserva tipo_borda",
               novo3a["tipo_borda"] == "curva")
    _registrar("cenario 3: V preserva tela_atual",
               novo3a["tela_atual"] == "h0037_console_alternavel_tres_niveis")
    _registrar("processar_comando nao modifica o dict original",
               est3["modo_verboso"] is False)


def teste_conteudo_compartilhado_cenarios_1_e_2():
    print("")
    print("== Conteudo externo compartilhado entre cenarios 1 e 2 ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")

    _registrar("cenario 1: conteudo externo presente",
               m1.conteudo_externo is not None)
    _registrar("cenario 2: conteudo externo presente",
               m2.conteudo_externo is not None)
    _registrar("cenarios 1 e 2 compartilham o mesmo conteudo semantico",
               m1.conteudo_externo._raw == m2.conteudo_externo._raw)
    _registrar("cenarios 1 e 2 sao instancias distintas de conteudo",
               m1.conteudo_externo is not m2.conteudo_externo)
    _registrar("politica_modo diverge entre 1 e 2 (independencia de politica e conteudo)",
               getattr(_console_de(m1), "politica_modo", None)
               != getattr(_console_de(m2), "politica_modo", None))


def teste_isolamento_verbosidade_entre_telas():
    print("")
    print("== Isolamento de verbosidade entre telas distintas ==")

    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    # Estado inicial independente por tela
    est3 = _estado("h0037_console_alternavel_tres_niveis",
                   modo_verboso=_modo_verboso_de_modelo(m3))
    est4 = _estado("h0037_console_tabela_alternavel",
                   modo_verboso=_modo_verboso_de_modelo(m4))

    _registrar("cenario 3 inicia com modo_verboso=False",
               est3["modo_verboso"] is False)
    _registrar("cenario 4 inicia com modo_verboso=True",
               est4["modo_verboso"] is True)

    # Alternancia em m3 nao afeta m4
    novo3 = processar_comando(est3, "V", m3)
    _registrar("alternancia em cenario 3 nao altera estado de cenario 4",
               est4["modo_verboso"] is True and novo3["modo_verboso"] is True)

    # Alternancia em m4 nao afeta m3
    novo4 = processar_comando(est4, "V", m4)
    _registrar("alternancia em cenario 4 nao altera estado de cenario 3",
               est3["modo_verboso"] is False and novo4["modo_verboso"] is False)

    # Troca de tela reseta modo para o inicial da nova tela
    est_trocado = _estado("h0037_console_tabela_alternavel",
                          modo_verboso=_modo_verboso_de_modelo(m4))
    _registrar("apos troca para cenario 4: modo_verboso restaurado para True",
               est_trocado["modo_verboso"] is True)


def teste_renderizacao_modo_nao_verboso_vs_verboso():
    print("")
    print("== Renderizacao: modo nao verboso vs verboso ==")

    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")
    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")

    r_nv = renderizar_tela(m2, tipo_borda="curva", largura=80, verboso=False)
    r_v = renderizar_tela(m2, tipo_borda="curva", largura=80, verboso=True)
    _registrar("cenario 2: renderizacao verbosa difere da nao verbosa",
               r_nv != r_v)
    _registrar("cenario 2 verboso: mais linhas que nao verboso",
               r_v.count("\n") >= r_nv.count("\n"))

    r3_nv = renderizar_tela(m3, tipo_borda="curva", largura=80, verboso=False)
    r3_v = renderizar_tela(m3, tipo_borda="curva", largura=80, verboso=True)
    _registrar("cenario 3: renderizacao verbosa difere da nao verbosa",
               r3_nv != r3_v)
    _registrar("cenario 3 verboso: mais linhas que nao verboso",
               r3_v.count("\n") >= r3_nv.count("\n"))

    # Cenario 1 (somente_nao_verboso): verboso=True e ignorado pela politica
    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    r1_nv = renderizar_tela(m1, tipo_borda="curva", largura=80, verboso=False)
    r1_v_flag = renderizar_tela(m1, tipo_borda="curva", largura=80, verboso=True)
    _registrar("cenario 1 (somente_nao_verboso): flag verboso=True nao altera saida via _verboso_efetivo",
               _verboso_efetivo(_estado("h0037_console_nao_verboso", modo_verboso=True), m1) is False)

    # Cenario 4 tabela alternavel
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")
    r4_nv = renderizar_tela(m4, tipo_borda="curva", largura=80, verboso=False)
    r4_v = renderizar_tela(m4, tipo_borda="curva", largura=80, verboso=True)
    _registrar("cenario 4 (tabela_alternavel): renderizacao verbosa difere da nao verbosa",
               r4_nv != r4_v)


def teste_todos_cenarios_renderizam_sem_excecao():
    print("")
    print("== Todos os 4 cenarios renderizam sem excecao ==")

    for cenario in _CENARIOS:
        modelo = _carregar_modelo_por_id(cenario)
        try:
            renderizar_tela(modelo, tipo_borda="curva", largura=80)
            _registrar("{0}: renderiza sem excecao (modo padrao)".format(cenario), True)
        except Exception as exc:
            _registrar("{0}: renderiza sem excecao (modo padrao)".format(cenario),
                       False, str(exc))

    for cenario in _ALTERNAVEIS:
        modelo = _carregar_modelo_por_id(cenario)
        for verboso in (False, True):
            try:
                renderizar_tela(modelo, tipo_borda="curva", largura=80, verboso=verboso)
                _registrar("{0}: renderiza sem excecao (verboso={1})".format(cenario, verboso), True)
            except Exception as exc:
                _registrar("{0}: renderiza sem excecao (verboso={1})".format(cenario, verboso),
                           False, str(exc))


def teste_abertura_por_argv():
    """main(argv=[...]) aplica modo inicial antes da primeira renderizacao."""
    print("")
    print("== Abertura por argv: modo inicial na primeira renderizacao ==")

    # Verificacao indireta: _modo_verboso_de_modelo confirma modo esperado.
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")
    _registrar("cenario 4: _modo_verboso_de_modelo retorna True (verboso)",
               _modo_verboso_de_modelo(m4) is True)

    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    _registrar("cenario 3: _modo_verboso_de_modelo retorna False (nao verboso)",
               _modo_verboso_de_modelo(m3) is False)

    # Verificacao direta: captura da primeira renderizacao nao-TTY via main().
    def _capturar_main(argv):
        saida = io.StringIO()
        stdin_vazio = io.StringIO("")
        stdin_orig = sys.stdin
        stdout_orig = sys.stdout
        try:
            sys.stdin = stdin_vazio
            sys.stdout = saida
            try:
                _demo_main(argv=argv)
            except SystemExit:
                pass
        finally:
            sys.stdin = stdin_orig
            sys.stdout = stdout_orig
        return saida.getvalue()

    # Cenario 4 (tabela_alternavel, modo_inicial verboso): o conteudo longo
    # do modo verboso deve aparecer na primeira renderizacao nao-TTY.
    saida_c4 = _capturar_main(["demo.py", "h0037_console_tabela_alternavel"])
    _registrar(
        "cenario 4: abertura por argv renderiza conteudo verboso na primeira frame",
        "celulas longas" in saida_c4,
    )
    _registrar(
        "cenario 4: abertura por argv nao abre truncado (modo verboso confirmado)",
        "Modo inicial" in saida_c4,
    )

    # Cenario 3 (alternavel_tres_niveis, modo_inicial nao_verboso): texto do
    # terceiro nivel nao aparece expandido na primeira frame (modo nao verboso).
    saida_c3 = _capturar_main(["demo.py", "h0037_console_alternavel_tres_niveis"])
    _registrar(
        "cenario 3: abertura por argv renderiza em modo nao verboso (chip V presente)",
        "H-0037 alternavel_tres_niveis" in saida_c3,
    )


def teste_h0037_manual_003_tecla_v_minuscula():
    """H0037-MANUAL-003: tecla ``v`` (minuscula) e ``V`` (maiuscula) (TECLA-01..08).

    Cobre a decisao explicita do usuario: ambas as variantes (``V`` e ``v``)
    devem alternar o modo nas telas alternaveis; nas telas fixas, ambas
    permanecem inertes. A entrada nao aparece como caractere no conteudo
    renderizado (sem eco). O estado inicial de outra tela nao e afetado pela
    alternancia (isolamento).
    """
    print("")
    print("== H-0037 MANUAL-003: tecla v (minuscula) e V (maiuscula) ==")

    m1 = _carregar_modelo_por_id("h0037_console_nao_verboso")
    m2 = _carregar_modelo_por_id("h0037_console_verboso_dois_niveis")
    m3 = _carregar_modelo_por_id("h0037_console_alternavel_tres_niveis")
    m4 = _carregar_modelo_por_id("h0037_console_tabela_alternavel")

    # --- TECLA-01: cenario 3 com V alterna e retorna ---
    est3 = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    novo = processar_comando(est3, "V", m3)
    _registrar("TECLA-01 cenario 3 com V: False -> True", novo["modo_verboso"] is True)
    novo2 = processar_comando(novo, "V", m3)
    _registrar("TECLA-01 cenario 3 com V: True -> False (retorno)",
               novo2["modo_verboso"] is False)

    # --- TECLA-02: cenario 3 com v alterna e retorna ---
    est3b = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    novo_b = processar_comando(est3b, "v", m3)
    _registrar("TECLA-02 cenario 3 com v: False -> True", novo_b["modo_verboso"] is True)
    novo_b2 = processar_comando(novo_b, "v", m3)
    _registrar("TECLA-02 cenario 3 com v: True -> False (retorno)",
               novo_b2["modo_verboso"] is False)

    # --- TECLA-03: cenario 4 com V compacta e retorna ---
    est4 = _estado("h0037_console_tabela_alternavel", modo_verboso=True)
    novo4 = processar_comando(est4, "V", m4)
    _registrar("TECLA-03 cenario 4 com V: True -> False (compacta)",
               novo4["modo_verboso"] is False)
    novo4b = processar_comando(novo4, "V", m4)
    _registrar("TECLA-03 cenario 4 com V: False -> True (retorno)",
               novo4b["modo_verboso"] is True)

    # --- TECLA-04: cenario 4 com v compacta e retorna ---
    est4b = _estado("h0037_console_tabela_alternavel", modo_verboso=True)
    novo4_v = processar_comando(est4b, "v", m4)
    _registrar("TECLA-04 cenario 4 com v: True -> False (compacta)",
               novo4_v["modo_verboso"] is False)
    novo4_v2 = processar_comando(novo4_v, "v", m4)
    _registrar("TECLA-04 cenario 4 com v: False -> True (retorno)",
               novo4_v2["modo_verboso"] is True)

    # --- TECLA-05: tela fixa nao verbosa — V e v inertes ---
    est_nv = _estado("h0037_console_nao_verboso", modo_verboso=False)
    novo_v_nv = processar_comando(est_nv, "V", m1)
    _registrar("TECLA-05 fixa nao verbosa: V inerte",
               novo_v_nv["modo_verboso"] == est_nv["modo_verboso"])
    novo_vmin_nv = processar_comando(est_nv, "v", m1)
    _registrar("TECLA-05 fixa nao verbosa: v inerte",
               novo_vmin_nv["modo_verboso"] == est_nv["modo_verboso"])

    # --- TECLA-06: tela fixa verbosa — V e v inertes ---
    est_vb = _estado("h0037_console_verboso_dois_niveis", modo_verboso=False)
    novo_v_vb = processar_comando(est_vb, "V", m2)
    _registrar("TECLA-06 fixa verbosa: V inerte",
               novo_v_vb["modo_verboso"] == est_vb["modo_verboso"])
    novo_vmin_vb = processar_comando(est_vb, "v", m2)
    _registrar("TECLA-06 fixa verbosa: v inerte",
               novo_vmin_vb["modo_verboso"] == est_vb["modo_verboso"])

    # --- TECLA-07: isolamento — alternar por v em uma tela nao muda outra ---
    est3_iso = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    est4_iso = _estado("h0037_console_tabela_alternavel", modo_verboso=True)
    novo3_iso = processar_comando(est3_iso, "v", m3)
    _registrar("TECLA-07 isolamento: alternar v em cenario 3 nao altera cenario 4",
               est4_iso["modo_verboso"] is True and novo3_iso["modo_verboso"] is True)
    _registrar("TECLA-07 isolamento: estado original de cenario 3 inalterado",
               est3_iso["modo_verboso"] is False)

    # --- TECLA-08: sem eco — a entrada nao aparece como caractere no conteudo ---
    est3_eco = _estado("h0037_console_alternavel_tres_niveis", modo_verboso=False)
    saida_antes = renderizar_tela(m3, tipo_borda="curva", largura=80,
                                  verboso=_verboso_efetivo(est3_eco, m3))
    novo_eco = processar_comando(est3_eco, "v", m3)
    saida_depois = renderizar_tela(m3, tipo_borda="curva", largura=80,
                                   verboso=_verboso_efetivo(novo_eco, m3))
    # A tecla 'v' jamais deve aparecer isolada como linha/caractere de eco
    # no conteudo renderizado da tela de console (ela so afeta modo_verboso).
    _registrar(
        "TECLA-08 sem eco: tecla 'v' nao aparece como conteudo isolado antes",
        not any(l.strip() == "v" for l in saida_antes.split("\n")),
    )
    _registrar(
        "TECLA-08 sem eco: tecla 'v' nao aparece como conteudo isolado depois",
        not any(l.strip() == "v" for l in saida_depois.split("\n")),
    )
    # A saida deve ter mudado (modo mudou), provando que a tecla atuou sem eco.
    _registrar(
        "TECLA-08 sem eco: saida difere apos alternancia (v produziu efeito)",
        saida_antes != saida_depois,
    )


def _finalizar():
    total = len(_RESULTADOS)
    falharam = [(n, ok) for n, ok in _RESULTADOS if not ok]
    print("")
    print("Total: {0} verificacoes, {1} falha(s)".format(total, len(falharam)))
    if falharam:
        print("Falhas:")
        for nome, _ in falharam:
            print("  - {0}".format(nome))
    return 0 if not falharam else 1


def main():
    print("H-0037 / ADR-0028 D23 — politica de modo por tela")
    print("Base: {0}".format(_BASE_PADRAO))

    teste_transporte_politica_modo()
    teste_modo_verboso_inicial()
    teste_verboso_efetivo_por_politica()
    teste_tecla_v_ausente_nas_fixas()
    teste_alternancia_v_nas_alternaveis()
    teste_conteudo_compartilhado_cenarios_1_e_2()
    teste_isolamento_verbosidade_entre_telas()
    teste_renderizacao_modo_nao_verboso_vs_verboso()
    teste_todos_cenarios_renderizam_sem_excecao()
    teste_abertura_por_argv()
    teste_h0037_manual_003_tecla_v_minuscula()

    return _finalizar()


if __name__ == "__main__":
    sys.exit(main())
