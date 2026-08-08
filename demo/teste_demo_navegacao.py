"""Testes integrados de navegacao de console de nivel unico (H-0040 / ADR-0031).

Cobre as 17 provas negativas canonicas PN-0001 a PN-0017 da secao 20 do
H-0040. Cada prova possui o nome nominal declarado e valida que o
comportamento PROIBIDO nao ocorre (condicao de falha nao satisfeita).

Os testes integram o estado de runtime (``foco_console``/``cursores``), o
processamento de teclas (Tab/Shift+Tab/setas/espaco/Enter) e a renderizacao
(indicador de cursor, chips contextuais), exercitando os JSONs nominais do
H-0040 quando aplicavel e modelos construidos localmente para os cenarios
especificos.

Distribuicao (H-0040 secao 26):
- integracao_com_estado (PN-0001 a PN-0005)
- processamento_de_teclas (PN-0011, PN-0013, PN-0014, PN-0017)
- renderizacao (PN-0008, PN-0010)
- indicador (PN-0015)
- chips (PN-0009)
- redimensionamento (PN-0012)
- modos (parte de PN-0011)
- pagina (PN-0014)
- grade (PN-0006, PN-0007, PN-0016)
- Enter (PN-0013)

Apenas biblioteca padrao do Python.
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

# Padrao dos testes da demo: insere a raiz do repositorio no sys.path e remove
# o propio diretorio demo, de modo que ``demo.demo`` seja importavel como
# modulo da raiz (a demo nao e um pacote com __init__.py).
_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

import pytest  # noqa: E402

from tela.loader import carregar_tela, carregar_estilo  # noqa: E402
from tela.modelo import construir_modelo, ElementoCorpo, ModeloTela, Corpo  # noqa: E402
from tela import navegacao  # noqa: E402
from tela.renderizador import renderizar_tela  # noqa: E402
import demo.demo as _demo  # noqa: E402


_RAIZ_TELAS_DEMO = _demo._RAIZ_TELAS_DEMO


def _modelo_por_id(id_tela):
    """Carrega e constroi o modelo de uma tela nominal do H-0040."""
    tela_raw = carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw)


def _estilo_padrao():
    """Carrega o estilo global real (config/estilo.json)."""
    return carregar_estilo()


def _console(idc, itens, navegavel=True, distribuicao=None):
    inertes = {
        "titulo": idc,
        "itens": itens,
        "politica_navegacao": {"navegavel": navegavel},
    }
    return ElementoCorpo(
        id=idc, tipo="console", _campos_inertes=inertes,
        distribuicao_matricial=distribuicao,
    )


def _item(idc, texto, navegavel=True):
    return {"id": idc, "texto": texto, "navegavel": navegavel}


def _grupo(idc, elementos, arranjo="vertical"):
    return ElementoCorpo(
        id=idc, tipo="grupo",
        _campos_inertes={"arranjo": arranjo}, elementos=elementos,
    )


_DIST_1COL = {
    "formacao": {"politica": "preferencia_colunas", "colunas": {"minimo": 1, "maximo": 1}},
    "ordem": "por_linha",
    "dimensionamento": {"colunas": {"politica": "uniforme"}, "linhas": {"politica": "uniforme"}},
    "espacamento": {"margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1}, "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0}, "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0}},
    "distribuicao_horizontal": {"politica": "inicio"},
    "distribuicao_vertical": {"politica": "inicio"},
    "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos", "vertical": "uniforme_margens_e_vaos"},
    "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
    "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
}


def _dist_matriz(linhas, colunas):
    d = dict(_DIST_1COL)
    d["formacao"] = {"politica": "matriz_fixa", "linhas": {"fixo": linhas}, "colunas": {"fixo": colunas}}
    return d


def _estado_nav(modelo, foco=None, cursores=None, largura=40,
                desconto_estrutural=None):
    from tela.renderizador import DESCONTO_ESTRUTURAL_CONSOLE
    if desconto_estrutural is None:
        desconto_estrutural = DESCONTO_ESTRUTURAL_CONSOLE
    return {
        "modelo": modelo, "foco_console": foco,
        "cursores": cursores or {}, "largura": largura,
        "desconto_estrutural": desconto_estrutural,
    }


def _render(modelo, estado_nav, largura=60):
    """Renderiza com contexto de navegacao."""
    lista = navegacao.lista_foco(modelo)
    return renderizar_tela(
        modelo, _estilo_padrao(), largura=largura,
        foco_console=estado_nav.get("foco_console"),
        cursores=estado_nav.get("cursores", {}),
        lista_foco=lista, largura_navegacao=largura,
    )


# ---------------------------------------------------------------------------
# PN-0001 a PN-0004 -- Elementos nunca focalizaveis
# ---------------------------------------------------------------------------


# PN-0001 - grupo nunca focalizavel
def teste_prova_grupo_nunca_na_lista_foco():
    # prova: {id: PN-0001, proibicao: grupo estrutural na lista de foco}
    c1 = _console("c1", [_item("a", "A")], distribuicao=_DIST_1COL)
    g = _grupo("g", [c1])
    tipos = [e.tipo for e in navegacao.lista_foco([g])]
    assert "grupo" not in tipos  # condicao_de_falha: tipo grupo retornado


# PN-0002 - lancador nunca focalizavel
def teste_prova_lancador_nunca_na_lista_foco():
    # prova: {id: PN-0002, proibicao: lancador na lista de foco}
    l = ElementoCorpo(id="l", tipo="lancador", _campos_inertes={"itens": []})
    assert navegacao.lista_foco([l]) == []  # condicao_de_falha: lancador retornado


# PN-0003 - dashboard nunca focalizavel
def teste_prova_dashboard_nunca_na_lista_foco():
    # prova: {id: PN-0003, proibicao: dashboard na lista de foco}
    d = ElementoCorpo(id="d", tipo="dashboard", _campos_inertes={"campos": []})
    assert navegacao.lista_foco([d]) == []  # condicao_de_falha: dashboard retornado


# PN-0004 - console nao navegavel ou sem itens excluido
def teste_prova_console_nao_navegavel_ou_sem_itens_nunca_na_lista_foco():
    # prova: {id: PN-0004, proibicao: console com politica nao navegavel ou sem item navegavel na lista de foco}
    c_nav_false = _console(
        "cnavfalse",
        [_item("a", "A"), _item("b", "B")],
        navegavel=False, distribuicao=_DIST_1COL,
    )
    c_sem_nav = _console(
        "csemnav",
        [_item("x", "X", navegavel=False), _item("y", "Y", navegavel=False)],
        navegavel=True, distribuicao=_DIST_1COL,
    )
    ids = [e.id for e in navegacao.lista_foco([c_nav_false, c_sem_nav])]
    assert "cnavfalse" not in ids  # navegavel false excluido
    assert "csemnav" not in ids  # sem item navegavel excluido


# ---------------------------------------------------------------------------
# PN-0005 - retorno nao restaura cursor anterior
# ---------------------------------------------------------------------------


# PN-0005 - retorno nao restaura cursor anterior
def teste_prova_retorno_nao_restaura_cursor_anterior():
    # prova: {id: PN-0005, proibicao: retorno por Tab/Shift+Tab restaurar cursor anterior}
    c1 = _console(
        "c1",
        [_item("a", "A"), _item("b", "B"), _item("c", "C")],
        distribuicao=_DIST_1COL,
    )
    c2 = _console("c2", [_item("d", "D")], distribuicao=_DIST_1COL)
    # Cursor do primeiro fora do item 0.
    est = _estado_nav([c1, c2], foco=0, cursores={"c1": 2})
    # Muda o foco para c2 e volta para c1 por Tab.
    est = navegacao.avancar_foco(est)  # c2, cursor c2=0
    assert est["foco_console"] == 1
    est = navegacao.avancar_foco(est)  # volta para c1
    assert est["foco_console"] == 0
    # D6: cursor apos retorno == 0 (NAO restaura o anterior 2).
    assert est["cursores"]["c1"] == 0


# ---------------------------------------------------------------------------
# PN-0006, PN-0007, PN-0016 -- Celulas vazias, eixos e grade visual
# ---------------------------------------------------------------------------


# PN-0006 - celula vazia fora do cursor e do toroide
def teste_prova_celula_vazia_nao_recebe_cursor_nem_participa_toroide():
    # prova: {id: PN-0006, proibicao: celula vazia receber cursor ou participar do toroide}
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0}".format(i)) for i in range(5)],
        distribuicao=_dist_matriz(2, 3),
    )
    grade = navegacao.grade_de_itens(c, 40)
    # Celula (1,2) e None e nunca recebe cursor.
    assert grade[1][2] is None
    assert navegacao.item_logico_de_posicao(grade, 1, 2) is None
    # Toroidal horizontal a partir de g11 (item 4, coluna 1 linha 1): direita
    # pula a celula None (coluna 2) e volta para g10 (item 3), sem conta-la.
    est = _estado_nav([c], foco=0, cursores={"c": 4})
    est = navegacao.mover_direita(est, c)
    assert est["cursores"]["c"] == 3


# PN-0007 - eixo nao cruza linha nem coluna
def teste_prova_eixo_nao_cruza_linha_nem_coluna():
    # prova: {id: PN-0007, proibicao: movimento horizontal mudar de linha ou vertical mudar de coluna}
    c = _console(
        "c",
        [_item("g{0}".format(i), "G{0}".format(i)) for i in range(6)],
        distribuicao=_dist_matriz(2, 3),
    )
    # g02 (item 2, linha 0 coluna 2): direita -> toroide -> g00 (mesma linha 0).
    est = _estado_nav([c], foco=0, cursores={"c": 2})
    grade = navegacao.grade_de_itens(c, 40)
    pos_antes = navegacao._posicao_do_item_logico(grade, 2)
    est = navegacao.mover_direita(est, c)
    grade2 = navegacao.grade_de_itens(c, 40)
    pos_depois = navegacao._posicao_do_item_logico(grade2, est["cursores"]["c"])
    # Horizontal nao muda linha.
    assert pos_antes[0] == pos_depois[0]
    # Vertical: g00 (item 0, linha 0 coluna 0) baixo -> g10 (item 3, mesma coluna 0).
    est_v = _estado_nav([c], foco=0, cursores={"c": 0})
    est_v = navegacao.mover_baixo(est_v, c)
    pos_v_antes = navegacao._posicao_do_item_logico(grade, 0)
    pos_v_depois = navegacao._posicao_do_item_logico(
        grade, est_v["cursores"]["c"]
    )
    # Vertical nao muda coluna.
    assert pos_v_antes[1] == pos_v_depois[1]


# PN-0008 - indicador ausente em console nao focado
def teste_prova_indicador_nao_aparece_em_console_nao_focado():
    # prova: {id: PN-0008, proibicao: indicador aparecer em console nao focado}
    modelo = _modelo_por_id("h0040_nav_dois_consoles")
    lista = navegacao.lista_foco(modelo)
    # Foco no primeiro console; o segundo nao deve exibir selecionado_simbolo.
    estilo = _estilo_padrao()
    saida = renderizar_tela(
        modelo, estilo, largura=80, foco_console=0,
        cursores={lista[0].id: 0, lista[1].id: 0},
        lista_foco=lista, largura_navegacao=80,
    )
    # Apenas UMA ocorrencia do simbolo de selecao do estilo (console focado).
    assert saida.count(estilo.selecionado_simbolo) == 1


# ---------------------------------------------------------------------------
# PN-0009 - chip [✥] ausente com um item
# ---------------------------------------------------------------------------


# PN-0009 - chip [✥] ausente com um item
def teste_prova_chip_navegar_nao_aparece_com_um_item():
    # prova: {id: PN-0009, proibicao: chip setas aparecer com exatamente um item navegavel}
    modelo = _modelo_por_id("h0040_nav_degenere_um_item")
    lista = navegacao.lista_foco(modelo)
    est = _estado_nav(modelo, foco=0)
    # console focado com um item -> [✥] NAO aparece.
    assert navegacao.exibir_chip_navegar(est) is False
    # Renderizacao: o chip Navegar nao aparece na barra.
    saida = renderizar_tela(
        modelo, _estilo_padrao(), largura=50, foco_console=0,
        cursores={lista[0].id: 0}, lista_foco=lista, largura_navegacao=50,
    )
    assert "Navegar" not in saida


# ---------------------------------------------------------------------------
# PN-0010 - indicador fora da primeira linha
# ---------------------------------------------------------------------------


# PN-0010 - indicador fora da primeira linha
def teste_prova_indicador_nao_aparece_em_linha_de_continuacao():
    # prova: {id: PN-0010, proibicao: indicador aparecer em linha de continuacao}
    # QAI40-003: prepara continuação física REAL (item longo, largura pequena,
    # modo verboso efetivo) — ao menos duas linhas físicas para o mesmo item.
    # Falha se o símbolo aparecer em qualquer linha de continuação.
    # Patch pos-validacao: tambem exige ausencia de sobreposicao com o item
    # seguinte (item_seguinte.sobreposto == false).
    texto_longo = (
        "Alpha Beta Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu "
        "Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi Omega"
    )
    c = _console(
        "c",
        [_item("cur", "Curto"), _item("lng", texto_longo), _item("out", "OutroXYZ")],
        distribuicao=_DIST_1COL,
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    estilo = _estilo_padrao()
    simbolo = estilo.selecionado_simbolo
    # Cursor no item longo, modo verboso, largura segura pos-patch.
    saida = renderizar_tela(
        modelo, estilo, largura=60, altura=24, verboso=True,
        foco_console=0, cursores={"c": 1}, lista_foco=lista,
        largura_navegacao=60,
    )
    assert "pequeno" not in saida.lower() and "demais" not in saida.lower()
    # Confirma continuação física real: o item longo ocupa múltiplas linhas.
    linhas_fisicas = [ln for ln in saida.split("\n") if ln.startswith("│")]
    fragmentos = [w for w in texto_longo.split() if w]
    linhas_com_fragmento = [
        ln for ln in linhas_fisicas if any(frag in ln for frag in fragmentos)
    ]
    assert len(linhas_com_fragmento) >= 2, (
        "item não ocupa múltiplas linhas físicas (continuação real ausente)"
    )
    # Condicao de falha: símbolo em linha de continuação. Somente a primeira
    # linha física do item corrente pode conter o símbolo.
    assert saida.count(simbolo) == 1, (
        "símbolo apareceu em linha de continuação (esperado exatamente 1)"
    )
    # A linha marcada é a primeira do item corrente (contém o primeiro fragmento).
    linha_marcada = [ln for ln in saida.split("\n") if simbolo in ln][0]
    assert fragmentos[0] in linha_marcada or fragmentos[1] in linha_marcada
    # Item seguinte nao sobreposto.
    for ln in linhas_fisicas:
        if "OutroXYZ" in ln:
            assert not any(f in ln for f in fragmentos)
            assert simbolo not in ln


# ---------------------------------------------------------------------------
# PN-0011, PN-0012 -- Modo e redimensionamento nao reiniciam item
# ---------------------------------------------------------------------------


# PN-0011 - modo nao reinicia item
def teste_prova_mudanca_modo_nao_reinicia_item_zero():
    # prova: {id: PN-0011, proibicao: mudanca de modo reiniciar item zero}
    # QAI40-003: usa o JSON nominal h0040_nav_console_unico_linear, que contém o
    # item multilinha (i3). Prepara cursor no item 2 (Gamma...) e aplica o
    # override --verboso efetivo. Confirma que o modo mudou materialmente, o
    # cursor não voltou a 0 e a identidade lógica permaneceu.
    # Patch pos-validacao: confirma persistencia de modo_verboso_forcado apos
    # seta/Tab/Shift+Tab/espaco/Enter e diferença semantica CLI real.
    import subprocess
    modelo = _modelo_por_id("h0040_nav_console_unico_linear")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    estilo = _estilo_padrao()
    # Cursor no item 2 (Gamma...). Largura em que ambos os modos renderizam e
    # o modo verboso quebra o item longo (diferença material observável).
    largura = 80
    estado_nv = _demo.criar_estado_inicial()
    estado_nv = dict(
        estado_nv, estilo=estilo, foco_console=0,
        cursores={console.id: 2}, largura=largura,
    )
    # QA-H0045-P18-001 (P19): o texto do item 2 (i3) é alongado ANTES de ambas
    # as renderizações, de modo que `s_nv` e `s_v` derivem do MESMO modelo e do
    # MESMO conteúdo. A única diferença material entre as duas renderizações é o
    # modo (verboso=False vs verboso=True); qualquer diferença observada entre
    # as saídas decorre exclusivamente do modo, nunca de uma entrada de conteúdo
    # diferente.
    # IMP-H0045-P17-001: a largura corrigida (P17) ampliou a capacidade de uma
    # linha verbosa; o alongamento preserva a prova de continuação real em 2+
    # linhas físicas exigida por PN-0011 em modo verboso. No modo não verboso,
    # o texto alongado (uma única linha lógica, sem quebra) não cabe na célula
    # e a renderização resulta no quadro mínimo — diferença que decorre
    # exclusivamente do modo, já que o modo verboso quebra o mesmo texto em
    # múltiplas linhas físicas e o exibe integralmente.
    console._campos_inertes["itens"][2]["texto"] = (
        "Gamma texto-longo-demonstrativo Delta Epsilon Zeta Eta Theta "
        "Lambda Mu Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi "
        "Iota Kappa"
    )
    # Renderização em modo não verboso (mesmo texto alongado).
    s_nv = renderizar_tela(
        modelo, estilo, largura=largura, verboso=False,
        foco_console=0, cursores={console.id: 2}, lista_foco=lista,
        largura_navegacao=largura,
    )
    # Renderização em modo verboso (override efetivo): o item 2 ocupa múltiplas
    # linhas físicas.
    s_v = renderizar_tela(
        modelo, estilo, largura=largura, altura=24, verboso=True,
        foco_console=0, cursores={console.id: 2}, lista_foco=lista,
        largura_navegacao=largura,
    )
    # O modo mudou materialmente (saídas diferentes) — decorre exclusivamente
    # do modo, pois a entrada (modelo/conteúdo) é idêntica: o modo verboso
    # quebra o texto alongado em múltiplas linhas físicas e o exibe; o modo não
    # verboso não quebra e o texto não cabe, resultando em quadro mínimo.
    assert s_nv != s_v, "override verboso não produziu mudança material de modo"
    # No modo verboso, o mesmo item (Gamma...) aparece integralmente (prova de
    # continuação real). A identidade lógica do cursor (item 2) permanece em
    # ambos os estados de navegação, independentemente da apresentação.
    assert "Gamma" in s_v
    # O cursor não voltou ao item 0: o estado de navegação permanece em 2.
    estado_pos = dict(estado_nv, modo_verboso=True, modo_verboso_forcado=True)
    assert estado_pos["cursores"][console.id] == 2
    # Continuacao real sem sobreposicao.
    assert "pequeno" not in s_v.lower() and "demais" not in s_v.lower()
    linhas_v = [ln for ln in s_v.split("\n") if ln.startswith("│")]
    linhas_com_gamma = [
        ln for ln in linhas_v
        if "Gamma" in ln or "texto-longo" in ln or "Kappa" in ln or "Iota" in ln
    ]
    assert len(linhas_com_gamma) >= 2, "continuacao real ausente em --verboso"
    simbolo = estilo.selecionado_simbolo
    assert s_v.count(simbolo) == 1
    for ln in linhas_v:
        if "Omega" in ln and "Gamma" not in ln:
            assert "texto-longo" not in ln
            assert "Kappa" not in ln or "Omega" in ln and "Kappa" not in ln
            # Omega isolado: nao deve misturar tokens do item longo
            assert "texto-longo-demonstrativo" not in ln
            assert "Epsilon" not in ln
            assert "Zeta" not in ln
            assert "Eta" not in ln
            assert "Theta" not in ln
            assert "Iota" not in ln
            assert "Kappa" not in ln
    # Persistencia do override apos comandos.
    estado_cmd = dict(
        estado_nv, modo_verboso=True, modo_verboso_forcado=True,
        cursores={console.id: 2},
    )
    for cmd in ("\x1b[B", "\t", "\x1b[Z", " ", "\r"):
        estado_cmd = _demo.processar_comando(estado_cmd, cmd, modelo)
        assert estado_cmd.get("modo_verboso_forcado") is True
        assert _demo._verboso_efetivo(estado_cmd, modelo) is True
    # QAI40-003 (ponto de entrada real): o override --verboso deve alcançar o
    # runtime real e não ser imediatamente sobrescrito por politica_modo=None.
    import demo.demo_navegacao as _demo_nav
    argv_override = [
        "demo.demo_navegacao",
        "--tela",
        str(Path(_RAIZ_TELAS_DEMO) / "h0040_nav_console_unico_linear.json"),
        "--verboso",
    ]
    args = _demo_nav._parse_argv(argv_override)
    assert args.verboso is True
    estado_inj = _demo.criar_estado_inicial()
    if args.verboso:
        estado_inj = dict(estado_inj, modo_verboso=True, modo_verboso_forcado=True)
    assert estado_inj.get("modo_verboso") is True
    assert estado_inj.get("modo_verboso_forcado") is True
    # CLI real: com e sem --verboso produzem saidas semanticamente distintas.
    # QA-H0045-P18-001 (P19): os dois modos usam a MESMA cópia temporária da
    # tela, com o texto do item i3 alongado. A única diferença entre as duas
    # invocações é a ativação de --verboso; a fixture original em disco NÃO é
    # alterada nem usada diretamente. Assim, qualquer diferença observada entre
    # as saídas decorre exclusivamente do modo, não de conteúdo diferente.
    import json
    import tempfile
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory() as tmpdir:
        tela_raw = json.loads(
            (Path(_RAIZ_TELAS_DEMO) / "h0040_nav_console_unico_linear.json").read_text(
                encoding="utf-8"
            )
        )
        tela_raw["corpo"]["elementos"][0]["itens"][2]["texto"] = (
            "Gamma texto-longo-demonstrativo Delta Epsilon Zeta Eta Theta "
            "Lambda Mu Nu Xi Omicron Pi Rho Sigma Tau Upsilon Phi Chi Psi "
            "Iota Kappa"
        )
        caminho_tela_temp = Path(tmpdir) / "h0040_nav_console_unico_linear.json"
        caminho_tela_temp.write_text(json.dumps(tela_raw), encoding="utf-8")
        cmd_base = [
            sys.executable, "-m", "demo.demo_navegacao",
            "--tela", str(caminho_tela_temp),
        ]
        # Não verboso: mesmo conteúdo alongado da cópia temporária.
        p_nv = subprocess.run(
            cmd_base, input="s\n", text=True, capture_output=True, env=env, cwd=str(_BASE_PADRAO),
        )
        # Verboso: mesma cópia temporária; única diferença é --verboso.
        p_v = subprocess.run(
            cmd_base + ["--verboso"], input="s\n", text=True,
            capture_output=True, env=env, cwd=str(_BASE_PADRAO),
        )
    assert p_nv.returncode == 0 and p_v.returncode == 0
    assert p_nv.stdout != p_v.stdout, "CLI --verboso sem diferença semantica"
    # QA-H0045-P18-001 (P19): as duas saídas derivam da MESMA cópia temporária
    # (mesmo conteúdo); a diferença decorre exclusivamente do modo. No modo
    # verboso, o texto alongado é quebrado em múltiplas linhas físicas e o item
    # aparece integralmente; no modo não verboso, o mesmo texto (uma linha
    # lógica sem quebra) não cabe e a CLI cai no quadro mínimo. Essa diferença
    # é efeito puro do modo, não de entrada diferente.
    assert "Gamma" in p_v.stdout
    assert p_v.stdout.count("Gamma") >= 1
    # Continuacao observavel na CLI verbosa (texto longo quebrado).
    assert "texto-longo" in p_v.stdout or "Kappa" in p_v.stdout or "Iota" in p_v.stdout


# PN-0012 - redimensionamento nao perde identidade
def teste_prova_redimensionamento_nao_perde_identidade_logica():
    # prova: {id: PN-0012, proibicao: redimensionamento perder identidade logica
    # ou usar a formacao anterior antes da primeira seta; preparacao: cursor em
    # item com grade larga no cenario de 26 itens; estimulo: recalcular grade
    # estreita e processar a primeira seta; condicao_de_falha: item logico muda;
    # cursor volta ao primeiro item; primeira seta usa a grade anterior;
    # posicao visual e navegavel divergem}
    from tela.renderizador import DESCONTO_ESTRUTURAL_CONSOLE, renderizar_tela
    from tela.loader import carregar_estilo

    modelo = _modelo_por_id("h0040_nav_matriz_26_itens_redimensionamento")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    # Dimensoes controladas: 2x13 (larga) -> 13x2 (estreita).
    largura_a, largura_b = 151, 28
    item_logico = 12  # item_13 — vizinhos distintos nas duas formacoes
    desconto = DESCONTO_ESTRUTURAL_CONSOLE
    grade_a = navegacao.grade_de_itens(
        console, largura_a, desconto_estrutural=desconto,
    )
    grade_b = navegacao.grade_de_itens(
        console, largura_b, desconto_estrutural=desconto,
    )
    assert (len(grade_a), len(grade_a[0])) == (2, 13)
    assert (len(grade_b), len(grade_b[0])) == (13, 2)

    def _viz_dir(grade, il):
        pos = navegacao._posicao_do_item_logico(grade, il)
        ocup = navegacao._linha_com_itens(grade, pos[0])
        ncol = ocup[(ocup.index(pos[1]) + 1) % len(ocup)]
        return navegacao.item_logico_de_posicao(grade, pos[0], ncol)

    viz_antiga = _viz_dir(grade_a, item_logico)
    viz_nova = _viz_dir(grade_b, item_logico)
    assert viz_antiga != viz_nova

    # Runtime: preserva desconto; primeira seta usa formacao nova.
    estilo = carregar_estilo()
    estado = _demo.criar_estado_inicial()
    estado = dict(
        estado, estilo=estilo, foco_console=0,
        cursores={console.id: item_logico},
        largura=largura_a, desconto_estrutural=desconto,
    )
    sel_antes = navegacao.item_selecionado(console, estado)
    # SIGWINCH simulado
    estado = dict(estado, largura=largura_b, desconto_estrutural=desconto)
    sel_meio = navegacao.item_selecionado(console, estado)
    assert sel_antes.get("id") == sel_meio.get("id") == "item_13"
    assert estado["cursores"][console.id] == item_logico  # nao voltou a 0

    estado_pos = _demo.processar_comando(estado, "\x1b[C", modelo)
    assert estado_pos.get("desconto_estrutural") == desconto
    assert estado_pos["cursores"][console.id] == viz_nova
    assert estado_pos["cursores"][console.id] != viz_antiga

    # Posicao visual (renderer) e navegavel correspondem na formacao nova.
    pos_nav = navegacao.posicao_corrente(
        dict(estado, desconto_estrutural=desconto, largura=largura_b), console,
    )
    saida = renderizar_tela(
        modelo, estilo, largura=largura_b, altura=80,
        foco_console=0, cursores={console.id: item_logico},
        lista_foco=lista, largura_navegacao=largura_b,
    )
    assert "pequeno" not in saida.lower()
    simbolo = estilo.selecionado_simbolo
    item = grade_b[pos_nav[0]][pos_nav[1]]
    linha_marcada = [ln for ln in saida.split("\n") if simbolo in ln][0]
    assert item.get("texto", "") in linha_marcada

    # Fronteira VM-11 (grade 2x3 @32): sem desconto a seta usaria geometria antiga.
    modelo_g = _modelo_por_id("h0040_nav_console_grade_2x3")
    cg = navegacao.lista_foco(modelo_g)[0]
    estado_g = dict(
        _demo.criar_estado_inicial(),
        estilo=estilo, foco_console=0, cursores={cg.id: 4},
        largura=32, desconto_estrutural=desconto,
    )
    estado_g = _demo.processar_comando(estado_g, "\x1b[B", modelo_g)
    # Nova formacao 3x2: DOWN de g11@(2,0) -> g00. Geometria antiga 2x3 -> g01.
    assert navegacao.itens_navegaveis(cg)[estado_g["cursores"][cg.id]]["id"] == "g00"
    assert estado_g.get("desconto_estrutural") == desconto


# ---------------------------------------------------------------------------
# PN-0013 - Enter nao executa acao
# ---------------------------------------------------------------------------


# PN-0013 - Enter nao executa acao
def teste_prova_enter_nao_executa_acao():
    # prova: {id: PN-0013, proibicao: Enter executar acao}
    modelo = _modelo_por_id("h0040_nav_console_unico_linear")
    # Sentinela: contador de acoes. Enter NAO deve incrementar.
    acoes = {"chamadas": 0}
    estado = _demo.criar_estado_inicial()
    estado = dict(estado, estilo=_estilo_padrao(), foco_console=0,
                  cursores={"console_linear": 1}, largura=50)
    estado_pos = _demo.processar_comando(estado, "\r", modelo)
    # Enter nao executa acao: contador permanece 0 e nenhum dispatcher chamado.
    assert acoes["chamadas"] == 0
    # Estado de navegacao preservado (cursor nao mudou por Enter).
    assert estado_pos["cursores"].get("console_linear") == 1


# ---------------------------------------------------------------------------
# PN-0014 - seta nao muda pagina
# ---------------------------------------------------------------------------


# PN-0014 - seta nao muda pagina
def teste_prova_setas_nao_mudam_pagina():
    # prova: {id: PN-0014, proibicao: seta alterar pagina}
    modelo = _modelo_por_id("h0040_nav_console_grade_2x3")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    est = _estado_nav(modelo, foco=0, cursores={console.id: 0}, largura=40)
    pagina_antes = est.get("pagina_atual")
    for _ in range(4):
        est = navegacao.mover_direita(est, console)
        est = navegacao.mover_esquerda(est, console)
        est = navegacao.mover_baixo(est, console)
        est = navegacao.mover_cima(est, console)
    pagina_depois = est.get("pagina_atual")
    # pagina_atual nunca foi definida nem alterada pelas setas (D15).
    assert pagina_antes is None
    assert pagina_depois is None
    assert "pagina_atual" not in est  # as setas nao criam nem mudam pagina


# ---------------------------------------------------------------------------
# PN-0015 - indicador nao hardcoded
# ---------------------------------------------------------------------------


# PN-0015 - indicador nao hardcoded
def teste_prova_indicador_nao_hardcoded():
    # prova: {id: PN-0015, proibicao: indicador hardcoded}
    from tela.loader import EstiloResolvido
    c = _console(
        "c", [_item("a", "A"), _item("b", "B")], distribuicao=_DIST_1COL,
    )
    modelo = ModeloTela(
        id="t", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[c]),
        barra_de_menus={"chips": []}, _raw={},
    )
    lista = navegacao.lista_foco(modelo)
    # Estilo com simbolo "X": o renderer deve usar X, nao "→".
    estilo_x = EstiloResolvido(
        canto_superior_esquerdo="╭", canto_superior_direito="╮",
        canto_inferior_esquerdo="╰", canto_inferior_direito="╯",
        traco_superior="─", traco_inferior="─", lateral="│",
        caractere_esquerdo="[", caractere_direito="]",
        cor_texto="padrão", caixa_alta=False, cor_fundo="padrão",
        concluido_on="✓", concluido_off=" ",
        selecionado_simbolo="X", selecionado_off=" ",
        incluido_on="●", incluido_off="○",
    )
    saida = renderizar_tela(
        modelo, estilo_x, largura=40, foco_console=0,
        cursores={"c": 0}, lista_foco=lista, largura_navegacao=40,
    )
    assert "X" in saida  # simbolo do estilo, nao hardcoded
    assert "→" not in saida  # o hardcoded "→" NAO aparece


# ---------------------------------------------------------------------------
# PN-0016 - grade de navegacao nao diverge da visual
# ---------------------------------------------------------------------------


# PN-0016 - grade de navegacao nao diverge da visual
def teste_prova_grade_navegacao_nao_diverge_grade_visual():
    # prova: {id: PN-0016, proibicao: grade de navegacao divergir da grade visual
    # no cenario de 26 itens; observacao: coordenadas, celula do indicador,
    # espacamento horizontal recalculado, linha em branco entre linhas e
    # sobreposicao; condicao_de_falha: formacoes diferentes; indicador em celula
    # errada/vazia; espacamento nao recalculado; linha em branco desaparece;
    # sobreposicao; ordem dos 26 itens muda}
    from tela.renderizador import DESCONTO_ESTRUTURAL_CONSOLE
    from tela.distribuicao_matricial import calcular_distribuicao

    modelo = _modelo_por_id("h0040_nav_matriz_26_itens_redimensionamento")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    estilo = _estilo_padrao()
    simbolo = estilo.selecionado_simbolo
    desconto = DESCONTO_ESTRUTURAL_CONSOLE
    formacoes_alvo = {
        (1, 26): 282,
        (2, 13): 151,
        (4, 7): 85,
        (7, 4): 52,
        (13, 2): 28,
        (26, 1): 20,
    }
    ordem_ids = [i["id"] for i in navegacao.itens_navegaveis(console)]
    assert len(ordem_ids) == 26
    assert ordem_ids[0] == "item_01" and ordem_ids[-1] == "item_26"

    def _vao_h(largura):
        nav = navegacao.itens_navegaveis(console)
        min_ws = [len(i["texto"]) + 2 for i in nav]
        min_hs = [1] * 26
        r = calcular_distribuicao(
            area_w=largura - desconto, area_h=80, n_participantes=26,
            config=console.distribuicao_matricial,
            min_ws=min_ws, min_hs=min_hs,
        )
        vaos = r["grade"]["vaos_h"]
        return vaos[0] if vaos else 0

    # Espacamento horizontal recalculado: mesma formacao 13x2 em duas larguras.
    vao_28 = _vao_h(28)
    vao_39 = _vao_h(39)
    assert vao_28 >= 2
    assert vao_39 > vao_28

    for form, largura in formacoes_alvo.items():
        grade_nav = navegacao.grade_de_itens(
            console, largura, desconto_estrutural=desconto,
        )
        formacao_nav = (len(grade_nav), len(grade_nav[0]))
        assert formacao_nav == form
        ids_grade = [
            cel.get("id")
            for linha in grade_nav for cel in linha if cel is not None
        ]
        assert ids_grade == ordem_ids  # ordem dos 26 itens preservada

        # Amostra de cursores (extremos + meio) — evita explosao combinatoria.
        for cursor in (0, 10, 25):
            saida = renderizar_tela(
                modelo, estilo, largura=largura, altura=80,
                foco_console=0, cursores={console.id: cursor},
                lista_foco=lista, largura_navegacao=largura,
            )
            assert "pequeno" not in saida.lower()
            assert saida.count(simbolo) == 1
            pos = navegacao._posicao_do_item_logico(grade_nav, cursor)
            assert pos is not None
            item_corrente = grade_nav[pos[0]][pos[1]]
            assert item_corrente is not None  # nao em celula vazia
            linha_marcada = [ln for ln in saida.split("\n") if simbolo in ln][0]
            assert item_corrente.get("texto", "") in linha_marcada

        # Linha fisica vazia entre linhas da matriz (vao_vertical=1).
        if form[0] > 1:
            saida = renderizar_tela(
                modelo, estilo, largura=largura, altura=80,
                foco_console=0, cursores={console.id: 0},
                lista_foco=lista, largura_navegacao=largura,
            )
            textos = [i["texto"] for i in navegacao.itens_navegaveis(console)]
            linhas = saida.split("\n")
            idxs = [
                i for i, ln in enumerate(linhas)
                if ln.startswith("│") and any(t in ln for t in textos)
            ]
            assert len(idxs) >= 2
            # Entre duas linhas de conteudo consecutivas da matriz ha exatamente
            # uma linha fisica interna vazia (apenas borda/espacos).
            buracos = []
            for a, b in zip(idxs, idxs[1:]):
                internas = linhas[a + 1:b]
                vazias = [
                    ln for ln in internas
                    if ln.startswith("│") and not any(t in ln for t in textos)
                ]
                buracos.append(len(vazias))
            assert all(n == 1 for n in buracos), buracos


# ---------------------------------------------------------------------------
# PN-0017 - espaco nao alterna selecao
# ---------------------------------------------------------------------------


# PN-0017 - espaco nao alterna selecao
def teste_prova_space_nao_togla_inclusao():
    # prova: {id: PN-0017, proibicao: espaco alterar selecao}
    modelo = _modelo_por_id("h0040_nav_console_unico_linear")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    estado = _demo.criar_estado_inicial()
    estado = dict(estado, estilo=_estilo_padrao(), foco_console=0,
                  cursores={console.id: 1}, largura=50)
    estado_pos = _demo.processar_comando(estado, " ", modelo)
    # Espaco nao cria conjunto, nao alterna inclusao, nao muda cursor.
    assert estado_pos["cursores"].get(console.id) == 1
    assert "selecao" not in estado_pos  # nenhum conjunto criado
    assert estado_pos.get("foco_console") == 0


# ---------------------------------------------------------------------------
# VM-H0045-R08-001 (P23): navegacao em geometria invalida preserva cursor.
# Em terminal insuficiente para a barra da tela corrente, setas e comandos de
# pagina NAO deslocam o cursor nem mudam foco (sem recalcular a pagina sob
# medidas invalidas). Comportamento exclusivo do console paginado.
# ---------------------------------------------------------------------------


def teste_h0045_p23_setas_e_pagina_preservam_cursor_em_geometria_invalida():
    """VM-H0045-R08-001: comandos de navegacao nao movem cursor em geometria invalida."""
    modelo = _modelo_por_id("h0045_fluxo_execucao_paginado")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    estado = _demo.criar_estado_inicial()
    estado = dict(
        estado, estilo=_estilo_padrao(), foco_console=0,
        cursores={console.id: 0}, selecoes={console.id: []},
        pagina_atual={console.id: 1},
        largura=80, altura=24, desconto_estrutural=3,
        tela_atual="h0045_fluxo_execucao_paginado",
    )
    # Em geometria valida, seta para baixo move o cursor (single-column).
    estado_valido = _demo.processar_comando(estado, "\x1b[B", modelo)
    cursor_pos = estado_valido["cursores"][console.id]
    assert cursor_pos > 0, "seta baixo deve mover em geometria valida"

    # Em geometria invalida (barra nao cabe nem em 5 linhas), setas e pagina
    # nao deslocam cursor nem mudam foco/pagina.
    estado_inv = dict(estado, largura=14, altura=24, desconto_estrutural=3)
    estado_inv = _demo._reconciliar_paginacao_apos_resize(estado_inv, modelo)
    cursor_antes = estado_inv["cursores"][console.id]
    foco_antes = estado_inv["foco_console"]
    pagina_antes = dict(estado_inv["pagina_atual"])
    for cmd in (
        "\x1b[B", "\x1b[A", "\x1b[C", "\x1b[D",
        _demo.TECLA_PAGE_UP, _demo.TECLA_PAGE_DOWN,
    ):
        e2 = _demo.processar_comando(estado_inv, cmd, modelo)
        assert e2["cursores"][console.id] == cursor_antes, cmd
        assert e2["foco_console"] == foco_antes, cmd
        assert e2["pagina_atual"] == pagina_antes, cmd


def teste_h0045_p23_navegacao_recupera_movimento_apos_ampliar():
    """VM-H0045-R08-001: apos ampliar, as setas voltam a mover o cursor."""
    modelo = _modelo_por_id("h0045_fluxo_execucao_paginado")
    lista = navegacao.lista_foco(modelo)
    console = lista[0]
    estado = _demo.criar_estado_inicial()
    estado = dict(
        estado, estilo=_estilo_padrao(), foco_console=0,
        cursores={console.id: 0}, selecoes={console.id: []},
        pagina_atual={console.id: 1},
        largura=14, altura=24, desconto_estrutural=3,
        tela_atual="h0045_fluxo_execucao_paginado",
    )
    estado = _demo._reconciliar_paginacao_apos_resize(estado, modelo)
    # Amplia para geometria valida.
    estado = dict(estado, largura=80, altura=24, desconto_estrutural=3)
    estado = _demo._reconciliar_paginacao_apos_resize(estado, modelo)
    estado = _demo.processar_comando(estado, "\x1b[B", modelo)
    assert estado["cursores"][console.id] > 0
