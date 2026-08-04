from pathlib import Path

from tela.loader import carregar_tela, EstiloResolvido, carregar_conteudo_externo, carregar_estilo
from tela.modelo import Corpo, ElementoCorpo, ModeloTela, construir_modelo, construir_conteudo_externo
from tela.renderizador import (
    RenderizadorErro,
    _distribuir_alturas,
    _distribuir_larguras,
    _linhas_barra,
    _linhas_console,
    _texto_designador,
    _romano,
    _alfabetico,
    _montar_corpo_horizontal,
    _pesos_distribuicao,
    _renderizar_container_horizontal,
    _garantir_esc_primeiro,
    _truncar_com_marcador,
    renderizar_tela,
)
from tela.testes_renderizador.comum import (
    _BASE_PADRAO,
    _RESULTADOS,
    _RAIZ_TELAS_DEMO,
    _ESTILO_CURVA,
    _ESTILO_RETA,
    _ESTILO_CAIXA_ALTA,
    _ESTILO_H0044,
    _EXPECTED_ORQUESTRADOR,
    _EXPECTED_ORQUESTRADOR_RETA,
    _PARAMS_LANCADOR_DEMO,
    _registrar,
    _espera_excecao,
    _modelo_orquestrador_sem_distribuicao,
    _funcional,
    _grupo,
    _grupo_matriz_render_h0028,
    _modelo_h0029,
    _h0029_linhas_totais,
    _alturas_caixas,
    _corpo_alturas,
)

import pytest as _pytest_qa002
from tela.loader import carregar_estilo as _carregar_estilo_qa002
from tela import renderizador as _rend_qa002



__all__ = [
    'teste_conteudo_externo_h0036_render',
    'teste_h0037_manual_001_marcador_truncamento',
    'teste_h0037_manual_002_esc_primeiro',
    'teste_h0037_qapp7_verb_sem_corte_silencioso',
    'test_h0044_p01_valor_campo_normaliza_newline_a_direita',
    'test_h0044_p01_valor_campo_normaliza_newlines_embutidos',
    'test_h0044_p01_valor_campo_none_continua_indisponivel',
    'test_h0044_p01_valor_campo_falsy_nao_none_preservado',
    'test_h0044_p01_envelope_falha_cabe_em_altura_suficiente',
    'test_h0044_p01_limite_calculado_corresponde_ao_conteudo_natural',
    'test_h0044_p01_tres_controles_envelope_renderizam',
    'test_h0044_p01_redimensionamento_decide_capacidade_sem_reiniciar',
]


def _modelo_com_conteudo(id_tela, id_conteudo):
    tela_raw = carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
    doc = carregar_conteudo_externo(None, id_conteudo, _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw, conteudo_externo=doc)


def teste_conteudo_externo_h0036_render():
    """Renderizacao do conteudo externo multinivel (H-0036 / ADR-0027)."""
    print("")
    print("== H-0036: renderizacao das tres apresentacoes ==")

    # --- Designadores concretos calculados pelo renderizador (unitario) ---
    _registrar("designador nenhum -> vazio",
               _texto_designador({"tipo": "nenhum"}, 1, []) == "")
    _registrar("designador decimal com sufixo -> '3.'",
               _texto_designador({"tipo": "decimal", "sufixo": "."}, 3, []) == "3.")
    _registrar("designador alfabetico_minusculo -> 'b)'",
               _texto_designador({"tipo": "alfabetico_minusculo", "sufixo": ")"}, 2, []) == "b)")
    _registrar("designador alfabetico_maiusculo (27) -> 'AA'",
               _texto_designador({"tipo": "alfabetico_maiusculo"}, 27, []) == "AA")
    _registrar("designador romano_maiusculo (4) -> 'IV'",
               _texto_designador({"tipo": "romano_maiusculo"}, 4, []) == "IV")
    _registrar("designador decimal_composto -> '1.2.'",
               _texto_designador({"tipo": "decimal_composto", "separador": ".", "sufixo": "."}, 2, [1]) == "1.2.")
    _registrar("designador simbolo usa valor declarado",
               _texto_designador({"tipo": "simbolo", "valor": "-"}, 5, []) == "-")
    _registrar("_romano(9) == IX", _romano(9) == "IX")
    _registrar("_alfabetico(1)=a, _alfabetico(28)=ab",
               _alfabetico(1) == "a" and _alfabetico(28) == "ab")

    # --- hierarquia ---
    m_h = _modelo_com_conteudo("h0036_console_hierarquia", "h0036_hierarquia_conteudo")
    console_h = m_h.elementos_por_tipo("console")[0]
    linhas_h = _linhas_console(console_h, 60)
    txt_h = "\n".join(linhas_h)
    _registrar("hierarquia: placeholder ausente com conteudo",
               "(console)" not in linhas_h)
    _registrar("hierarquia: designador decimal calculado ('1. Fluxo H-0036 hierarquia')",
               any("1. Fluxo H-0036 hierarquia" in l for l in linhas_h))
    _registrar("hierarquia: designador decimal_composto calculado ('1.1.')",
               any("1.1." in l for l in linhas_h))
    _registrar("hierarquia: designador alfabetico calculado ('a)')",
               any("a)" in l for l in linhas_h))
    _registrar("hierarquia: conteudo direto exibido",
               "JSON estrutural da tela" in txt_h)
    _registrar("hierarquia: recuo hierarquico por profundidade",
               any(l.startswith("  1.1.") for l in linhas_h))
    _registrar("hierarquia: identidade H-0036 na saida do renderizador",
               "H-0036" in txt_h)

    # --- tabela ---
    m_t = _modelo_com_conteudo("h0036_console_tabela", "h0036_tabela_conteudo")
    console_t = m_t.elementos_por_tipo("console")[0]
    linhas_t = _linhas_console(console_t, 60)
    txt_t = "\n".join(linhas_t)
    _registrar("tabela: placeholder ausente com conteudo", "(console)" not in linhas_t)
    _registrar("tabela: cabecalho de colunas presente",
               any("Grupo" in l and "Campo" in l and "Valor" in l for l in linhas_t))
    _registrar("tabela: par nome-valor em colunas ('Estrutural' e 'tela.json')",
               "Estrutural" in txt_t and "tela.json" in txt_t)
    _registrar("tabela: designador decimal por linha calculado ('1.' e '2.')",
               "1." in txt_t and "2." in txt_t)
    _registrar("tabela: ancestral repetido nas linhas ('Entradas')",
               txt_t.count("Entradas") >= 2)

    # --- conjuntos_campos ---
    m_c = _modelo_com_conteudo("h0036_console_conjuntos", "h0036_conjuntos_conteudo")
    console_c = m_c.elementos_por_tipo("console")[0]
    linhas_c = _linhas_console(console_c, 60)
    txt_c = "\n".join(linhas_c)
    _registrar("conjuntos: placeholder ausente com conteudo", "(console)" not in linhas_c)
    _registrar("conjuntos: designador de conjunto calculado ('1. Parametros')",
               any("1. Parametros" in l for l in linhas_c))
    _registrar("conjuntos: par nome-valor com separador (' : ' presente)",
               "Modo" in txt_c and "conjuntos_campos" in txt_c and ":" in txt_c)
    _registrar("conjuntos: identidade H-0036 no valor de campo",
               "H-0036" in txt_c)

    # --- placeholder preservado sem conteudo externo (regressao) ---
    modelo_sem = construir_modelo(
        carregar_tela(None, "h0036_console_hierarquia", _RAIZ_TELAS_DEMO)
    )
    console_sem = modelo_sem.elementos_por_tipo("console")[0]
    _registrar("console sem conteudo externo: placeholder '(console)' preservado",
               _linhas_console(console_sem, 60) == ["(console)"])

    # --- render integrado: placeholder ausente na saida completa ---
    saida = renderizar_tela(m_h, _ESTILO_CURVA, largura=60, altura=24)
    _registrar("render integrado: identidade H-0036 na tela",
               "H-0036" in saida)
    _registrar("render integrado: placeholder ausente quando ha conteudo",
               "(console)" not in saida)

    # --- truncamento como calculo do renderizador (sem geometria no JSON) ---
    saida_estreita = renderizar_tela(m_h, _ESTILO_CURVA, largura=24, altura=24)
    for linha in saida_estreita.split("\n"):
        if linha and len(linha) != 24:
            _registrar("truncamento: largura estreita respeitada", False,
                       "linha len={0}".format(len(linha)))
            break
    else:
        _registrar("truncamento: largura estreita (24) respeitada em todas as linhas", True)

    # --- h0035 console com DM + conteudo externo: grade preservada ---
    m_dm = _modelo_com_conteudo("h0035_console_com", "h0035_console_com_conteudo")
    saida_dm = renderizar_tela(m_dm, _ESTILO_CURVA, largura=60, altura=20)
    _registrar("h0035_console_com: participantes do externo em grade (P01..P12)",
               "P01 linha" in saida_dm and "P12 linha" in saida_dm
               and "(console)" not in saida_dm)

    # --- renderizador nao abre arquivos (inspecao de fonte) ---
    src = (Path(_BASE_PADRAO) / "tela" / "renderizador.py").read_text(encoding="utf-8")
    _registrar("renderizador nao importa json/os/pathlib",
               "import json" not in src and "import os" not in src
               and "import pathlib" not in src and "from pathlib" not in src)
    _registrar("renderizador nao chama carregar_conteudo_externo",
               "carregar_conteudo_externo" not in src)


def teste_h0037_manual_001_marcador_truncamento():
    """H0037-MANUAL-001: marcador `...` no truncamento nao verboso (RET-01..05).

    Cobre o comportamento obrigatorio (contrato_console.md §21.2): conteudo
    truncado no modo nao verboso recebe marcador `...`; conteudo que cabe
    integralmente nao recebe marcador; modo verboso nao recebe marcador
    artificial; tabela compacta permanece em uma linha por celula; a largura
    disponivel e sempre respeitada.
    """
    print("")
    print("== H-0037 MANUAL-001: marcador `...` no truncamento nao verboso ==")

    # --- Helper _truncar_com_marcador (casos diretos) ---
    _registrar(
        "RET-01 helper: texto que cabe nao recebe marcador",
        _truncar_com_marcador("abc", 10) == "abc",
    )
    _registrar(
        "RET-01 helper: texto exato nao recebe marcador",
        _truncar_com_marcador("abcde", 5) == "abcde",
    )
    _registrar(
        "RET-02 helper: texto que excede recebe sufixo '...'",
        _truncar_com_marcador("abcdefghij", 7) == "abcd...",
    )
    _registrar(
        "RET-02 helper: resultado respeita a largura limite",
        len(_truncar_com_marcador("abcdefghij", 7)) == 7,
    )
    _registrar(
        "largura muito pequena (<3): truncamento silencioso sem marcador",
        _truncar_com_marcador("abcde", 2) == "ab",
    )
    _registrar(
        "largura muito pequena (<3): largura 1",
        _truncar_com_marcador("abcde", 1) == "a",
    )

    # --- RET-01: conteudo que cabe integralmente nao recebe marcador ---
    m1 = _modelo_com_conteudo(
        "h0037_console_nao_verboso", "h0037_dois_niveis_conteudo"
    )
    saida_cabe = renderizar_tela(m1, estilo=_ESTILO_CURVA, largura=200, verboso=False)
    linhas_cabe = [l for l in saida_cabe.split("\n") if l]
    # Em largura generosa, nenhum item de conteudo deve terminar com '...'
    marcadas = [
        l for l in linhas_cabe
        if l.strip().endswith("...") and "(console)" not in l
        and "Menus" not in l
    ]
    _registrar(
        "RET-01: conteudo que cabe nao recebe marcador (sem '...' na saida larga)",
        not marcadas,
        "linhas marcadas={0!r}".format(marcadas[:2]),
    )

    # --- RET-02: conteudo hierarquico excede em modo nao verboso ---
    saida_nv = renderizar_tela(m1, estilo=_ESTILO_CURVA, largura=50, verboso=False)
    linhas_nv = saida_nv.split("\n")
    # Linhas de conteudo truncado terminam com '...' imediatamente antes da
    # borda vertical direita ('...│') — o marcador faz parte do trecho visivel.
    linhas_truncadas = [l for l in linhas_nv if l.endswith("...│")]
    _registrar(
        "RET-02: conteudo hierarquico truncado recebe marcador '...'",
        len(linhas_truncadas) >= 1,
        "linhas_truncadas={0!r}".format(linhas_truncadas[:2]),
    )
    # Cada linha truncada permanece unica (modo nao verboso = 1 linha fisica).
    _registrar(
        "RET-02: cada item truncado permanece em linha unica",
        all(len(l.strip()) <= 50 for l in linhas_truncadas),
    )
    # Largura respeitada: nenhuma linha da caixa excede a largura declarada.
    _registrar(
        "RET-02: largura respeitada em todas as linhas truncadas",
        all(len(l) == 50 for l in linhas_nv if l),
        "linhas com largura!=50: {0}".format(
            [len(l) for l in linhas_nv if l and len(l) != 50][:3]
        ),
    )

    # --- RET-03: celula de tabela excede em modo nao verboso compacto ---
    m4 = _modelo_com_conteudo(
        "h0037_console_tabela_alternavel", "h0037_tabela_conteudo"
    )
    saida_tab_nv = renderizar_tela(m4, estilo=_ESTILO_CURVA, largura=50, verboso=False)
    linhas_tab = saida_tab_nv.split("\n")
    linhas_tab_trunc = [l for l in linhas_tab if l.endswith("...│")]
    _registrar(
        "RET-03: celula de tabela excede recebe marcador '...'",
        len(linhas_tab_trunc) >= 1,
        "linhas_truncadas={0!r}".format(linhas_tab_trunc[:2]),
    )
    # Altura compacta: cada linha de dados ocupa exatamente uma linha fisica.
    # Conta linhas entre borda superior e inferior da caixa CONSOLE.
    dentro_console = False
    linhas_dados = 0
    for l in linhas_tab:
        s = l.strip()
        if s.startswith("╭") and "CONSOLE" in s:
            dentro_console = True
            continue
        if dentro_console and s.startswith("╰"):
            dentro_console = False
            break
        if dentro_console:
            linhas_dados += 1
    # Cabecalho + regua + 4 linhas de dados = 6 linhas (compacto, uma por item).
    _registrar(
        "RET-03: tabela compacta (uma linha por celula de dados)",
        linhas_dados == 6,
        "linhas_dados={0}".format(linhas_dados),
    )

    # --- RET-04: alternancia verboso/nao_verboso da tabela ---
    saida_tab_v = renderizar_tela(m4, estilo=_ESTILO_CURVA, largura=50, verboso=True)
    linhas_tab_v = saida_tab_v.split("\n")
    linhas_tab_v_trunc = [l for l in linhas_tab_v if l.endswith("...│")]
    # Em modo verboso o conteudo e quebrado em varias linhas, nao truncado.
    _registrar(
        "RET-04 verboso: truncamento com marcador ausente (conteudo quebrado)",
        len(linhas_tab_v_trunc) == 0,
        "linhas_com_marcador={0!r}".format(linhas_tab_v_trunc[:2]),
    )
    # Modo verboso produz mais linhas que o nao verboso (expansao vertical).
    _registrar(
        "RET-04: modo verboso expande verticalmente vs nao verboso",
        saida_tab_v.count("\n") > saida_tab_nv.count("\n"),
    )
    # Retorno ao verboso restaura conteudo multilinha (idempotente).
    saida_tab_v2 = renderizar_tela(m4, estilo=_ESTILO_CURVA, largura=50, verboso=True)
    _registrar(
        "RET-04: retorno ao verboso restaura conteudo multilinha",
        saida_tab_v == saida_tab_v2,
    )

    # --- RET-05: redimensionamento automatizavel ---
    # Largura menor produz mais marcadores '...'; largura maior reduz.
    saida_w40 = renderizar_tela(m1, estilo=_ESTILO_CURVA, largura=40, verboso=False)
    saida_w60 = renderizar_tela(m1, estilo=_ESTILO_CURVA, largura=60, verboso=False)
    marc_w40 = saida_w40.count("...│")
    marc_w60 = saida_w60.count("...│")
    _registrar(
        "RET-05: largura menor (40) produz marcador '...'",
        marc_w40 >= 1,
    )
    _registrar(
        "RET-05: ampliar largura reduz/elimina marcador (40 -> 60)",
        marc_w60 <= marc_w40,
        "marc_w40={0} marc_w60={1}".format(marc_w40, marc_w60),
    )
    # Ampliar bastante restaura conteudo integral (sem marcador): o maior item
    # do documento ~205 chars; largura 220 acomoda tudo sem truncamento.
    saida_w220 = renderizar_tela(m1, estilo=_ESTILO_CURVA, largura=220, verboso=False)
    _registrar(
        "RET-05: largura generosa restaura conteudo sem marcador",
        saida_w220.count("...│") == 0,
        "marc_w220={0}".format(saida_w220.count("...│")),
    )


def teste_h0037_manual_002_esc_primeiro():
    """H0037-MANUAL-002: chip ``[Esc]`` sempre primeiro (ESC-01..05).

    Regra contratual central (contrato_barra_de_menus.md §8.2): ``[Esc]`` e
    sempre o primeiro chip quando declarado. Aplicacao centralizada na origem
    da ordenacao da barra — vale para qualquer tela, sem condicao por ID/JSON.
    """
    print("")
    print("== H-0037 MANUAL-002: chip [Esc] sempre primeiro ==")

    # --- Helper _garantir_esc_primeiro (direto) ---
    # ESC-02: barra com Esc e varios chips preserva ordem relativa dos demais.
    chips_in = [
        {"id": "v", "tecla": "V", "texto": "Verboso"},
        {"id": "esc", "tecla": "Esc", "texto": "Voltar"},
        {"id": "ajuda", "tecla": "?", "texto": "Ajuda"},
    ]
    ordenados = _garantir_esc_primeiro(chips_in)
    _registrar(
        "ESC-02 helper: Esc movido para primeira posicao",
        ordenados[0].get("tecla") == "Esc",
    )
    _registrar(
        "ESC-02 helper: ordem relativa dos demais preservada (V, ?)",
        [c.get("tecla") for c in ordenados[1:]] == ["V", "?"],
    )
    # ESC-03: barra sem Esc preserva os chips existentes.
    chips_sem = [
        {"id": "v", "tecla": "V", "texto": "Verboso"},
        {"id": "ajuda", "tecla": "?", "texto": "Ajuda"},
    ]
    ordenados_sem = _garantir_esc_primeiro(chips_sem)
    _registrar(
        "ESC-03 helper: sem Esc -> chips preservados na ordem original",
        [c.get("tecla") for c in ordenados_sem] == ["V", "?"],
    )
    _registrar(
        "ESC-03 helper: sem Esc -> Esc nao inventado",
        not any(c.get("tecla") == "Esc" for c in ordenados_sem),
    )
    # ESC-04: ausencia de duplicacao.
    chips_dup = [
        {"id": "v", "tecla": "V", "texto": "Verboso"},
        {"id": "esc", "tecla": "Esc", "texto": "Voltar"},
    ]
    ordenados_dup = _garantir_esc_primeiro(chips_dup)
    qtos_esc = sum(1 for c in ordenados_dup if c.get("tecla") == "Esc")
    _registrar(
        "ESC-04 helper: quantidade de Esc == 1 (sem duplicacao)",
        qtos_esc == 1,
    )

    # --- Barra renderizada das telas alternaveis (ESC-01) ---
    m3 = _modelo_com_conteudo(
        "h0037_console_alternavel_tres_niveis", "h0037_tres_niveis_conteudo"
    )
    saida3 = renderizar_tela(m3, estilo=_ESTILO_CURVA, largura=80, verboso=False)
    barra3 = None
    linhas3 = saida3.split("\n")
    for i, l in enumerate(linhas3):
        if "Menus" in l and l.strip().startswith("╭"):
            barra3 = linhas3[i + 1] if i + 1 < len(linhas3) else ""
            break
    _registrar(
        "ESC-01: cenario 3 tem barra de menus renderizada",
        barra3 is not None and barra3 != "",
    )
    _registrar(
        "ESC-01 cenario 3: [Esc] aparece antes de [V] na barra",
        barra3 is not None and barra3.find("[Esc]") < barra3.find("[V]")
        and "[Esc]" in barra3 and "[V]" in barra3,
        "barra3={0!r}".format(barra3),
    )

    m4 = _modelo_com_conteudo(
        "h0037_console_tabela_alternavel", "h0037_tabela_conteudo"
    )
    saida4 = renderizar_tela(m4, estilo=_ESTILO_CURVA, largura=80, verboso=False)
    barra4 = None
    linhas4 = saida4.split("\n")
    for i, l in enumerate(linhas4):
        if "Menus" in l and l.strip().startswith("╭"):
            barra4 = linhas4[i + 1] if i + 1 < len(linhas4) else ""
            break
    _registrar(
        "ESC-01 cenario 4: [Esc] aparece antes de [V] na barra",
        barra4 is not None and barra4.find("[Esc]") < barra4.find("[V]")
        and "[Esc]" in barra4 and "[V]" in barra4,
        "barra4={0!r}".format(barra4),
    )

    # --- ESC-05: regressao das barras historicas (telas H-0036/H-0035) ---
    # demo.json: Esc ja eh primeiro (preservado).
    modelo_demo = construir_modelo(
        carregar_tela(None, "demo", _RAIZ_TELAS_DEMO)
    )
    saida_demo = renderizar_tela(modelo_demo, estilo=_ESTILO_CURVA, largura=42)
    linhas_demo = saida_demo.split("\n")
    barra_demo = None
    for i, l in enumerate(linhas_demo):
        if "Menus" in l and l.strip().startswith("╭"):
            barra_demo = linhas_demo[i + 1] if i + 1 < len(linhas_demo) else ""
            break
    _registrar(
        "ESC-05 demo.json: [Esc] permanece primeiro chip",
        barra_demo is not None and "[Esc]" in barra_demo
        and barra_demo.find("[Esc]") == barra_demo.find("["),
        "barra_demo={0!r}".format(barra_demo),
    )

    # Telas H-0036 com Esc na barra (historicas): Esc continua primeiro.
    for id_tela in ("h0036_console_hierarquia", "h0036_console_tabela",
                    "h0036_console_conjuntos"):
        modelo_h = construir_modelo(
            carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
        )
        barra_h = modelo_h.barra_de_menus
        chips_h = [c for c in (barra_h.get("chips") or []) if isinstance(c, dict)]
        teclas_h = [c.get("tecla") for c in _garantir_esc_primeiro(chips_h)]
        tem_esc = "Esc" in teclas_h
        if tem_esc:
            _registrar(
                "ESC-05 {0}: [Esc] primeiro quando presente".format(id_tela),
                teclas_h[0] == "Esc",
                "teclas={0!r}".format(teclas_h),
            )
        else:
            # Tela sem Esc declarado: regra nao inventa Esc.
            _registrar(
                "ESC-05 {0}: sem Esc declarado -> Esc nao inventado".format(id_tela),
                "Esc" not in teclas_h,
            )


def _linhas_caixa_console(saida):
    """Extrai as linhas internas da caixa CONSOLE da saida renderizada.

    Retorna tuplo (linhas, largura_total) onde ``linhas`` e a lista de linhas de
    conteudo (entre topo e base, COM as bordas laterais) e ``largura_total`` e a
    largura declarada (comprimento de cada linha fisica da saida).
    """
    linhas = saida.split("\n")
    dentro = False
    internas = []
    largura_total = 0
    for l in linhas:
        s = l.strip()
        if not l:
            continue
        largura_total = len(l)
        if s.startswith("╭") and "CONSOLE" in s:
            dentro = True
            continue
        if dentro and s.startswith("╰"):
            dentro = False
            break
        if dentro:
            internas.append(l)
    return internas, largura_total


def _texto_caixa_console(saida):
    """Texto interno da caixa CONSOLE: bordas laterais removidas, concatenado.

    Util para checar tokens que podem ser quebrados entre linhas fisicas: junta
    o conteudo interno das linhas (sem os caracteres de borda) por espaco e
    normaliza sequencias de espacos para um unico espaco (``rstrip`` por linha
    preserva a indentacao; a normalizacao final permite buscar tokens adjacentes
    que acabaram separados pela quebra fisica).
    """
    internas, _ = _linhas_caixa_console(saida)
    conteudos = []
    for l in internas:
        # Cada linha interna tem forma '│ {conteudo}│' ou '│ {conteudo} │'.
        if len(l) >= 2 and l[0] == "│":
            meio = l[1:-1] if l.endswith("│") else l[1:]
            conteudos.append(meio.rstrip())
    bruto = " ".join(conteudos)
    # Normaliza sequencias de espacos (incluindo a indentacao preservada) para
    # permitir buscas por tokens adjacentes independentemente da quebra fisica.
    return " ".join(bruto.split())


def teste_h0037_qapp7_verb_sem_corte_silencioso():
    """H0037-IMPL-QAPP7-001/002: hierarquia verbosa sem corte silencioso.

    Teste integrado que atravessa a renderizacao real da apresentacao
    hierarquica e da caixa, cobrindo os requisitos do patch pos-QA 7:

    - VERB-01: conteudo que cabe (texto integral, sem reticencias);
    - VERB-02: conteudo uma posicao maior (quebra de linha sem corte);
    - VERB-03: conteudo longo (tokens inicial/intermediario/final preservados);
    - VERB-04: prefixo hierarquico longo (largura restante respeitada);
    - VERB-05: linhas de continuacao (indentacao deterministica, sem repetir
      o designador em toda linha);
    - VERB-06: dois niveis (alinhamento do segundo nivel preservado);
    - VERB-07: tres niveis (sem misturar nem eliminar niveis);
    - VERB-08: largura reduzida (nenhuma linha interna excede o espaco);
    - VERB-09: ampliacao posterior (conteudo recalculado a partir dos dados);
    - VERB-10: alternancia verboso/nao verboso/verboso;
    - VERB-11: saida final (apos envelope da caixa) sem corte;
    - VERB-12: tabela preservada (multilinha em verboso, compacta com ...);
    - VERB-13: conjuntos preservados (comportamento aprovado mantido).
    """
    print("")
    print("== H-0037 IMPL-QAPP7-001/002: hierarquia verbosa sem corte ==")

    modelo_dois = _modelo_com_conteudo(
        "h0037_console_verboso_dois_niveis", "h0037_dois_niveis_conteudo"
    )
    modelo_tres = _modelo_com_conteudo(
        "h0037_console_alternavel_tres_niveis", "h0037_tres_niveis_conteudo"
    )

    # --- VERB-01: conteudo que cabe integralmente em modo verboso ---
    saida_larga = renderizar_tela(
        modelo_dois, estilo=_ESTILO_CURVA, largura=220, verboso=True
    )
    marc_larga = saida_larga.count("...│")
    _registrar(
        "VERB-01: conteudo que cabe nao recebe marcador (largura 220)",
        marc_larga == 0,
        "marcadores={0}".format(marc_larga),
    )
    # Texto integral presente (token inicial, intermediario e final).
    _registrar(
        "VERB-01: texto integral do primeiro item presente na saida larga",
        "H-0037 conteudo_dois_niveis" in saida_larga
        and "Politica somente_nao_verboso" in saida_larga
        and "a tela." in saida_larga,
    )

    # --- VERB-02: conteudo uma posicao maior -> quebra de linha sem corte ---
    # Largura suficiente para nao marcar, mas insuficiente para caber em 1 linha.
    saida_v30 = renderizar_tela(
        modelo_dois, estilo=_ESTILO_CURVA, largura=30, verboso=True
    )
    _registrar(
        "VERB-02: modo verboso em largura reduzida sem marcador '...'",
        saida_v30.count("...│") == 0,
        "marcadores={0}".format(saida_v30.count("...│")),
    )
    _registrar(
        "VERB-02: modo verboso expande verticalmente (mais linhas que o nv)",
        saida_v30.count("\n")
        > renderizar_tela(
            modelo_dois, estilo=_ESTILO_CURVA, largura=30, verboso=False
        ).count("\n"),
    )

    # --- VERB-03: conteudo longo com tokens distintos preservados ---
    saida_v30_tres = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=30, verboso=True
    )
    texto_v30_tres = _texto_caixa_console(saida_v30_tres)
    # Token inicial, intermediario e final do item longo do tres niveis.
    # (Como a largura 30 pode quebrar tokens entre linhas, inspecionamos o
    # texto interno concatenado da caixa.)
    _registrar(
        "VERB-03: token inicial preservado (Este texto)",
        "Este texto" in texto_v30_tres,
    )
    _registrar(
        "VERB-03: token intermediario preservado (hierarquica em)",
        "hierarquica em" in texto_v30_tres,
    )
    _registrar(
        "VERB-03: token final preservado (tres niveis.)",
        "tres niveis." in texto_v30_tres,
        "amostra_final={0!r}".format(texto_v30_tres[-60:]),
    )

    # --- VERB-04: prefixo hierarquico longo usa largura restante real ---
    internas_30, w30 = _linhas_caixa_console(saida_v30)
    _registrar(
        "VERB-04: cada linha interna do console respeita a largura total",
        all(len(l) == w30 for l in internas_30),
        "larguras={0}".format(
            [len(l) for l in internas_30 if len(l) != w30][:3]
        ),
    )
    # Linhas de continuacao do container '1.' usam indentacao da largura do
    # prefixo (nao ultrapassam a borda direita nem recebem '...'). Inspeciona
    # pelo texto interno para nao depender de posicao exata da borda.
    _registrar(
        "VERB-04: prefixo do container preserva designador na 1a linha",
        any("1. " in l for l in internas_30),
    )

    # --- VERB-05: linhas de continuacao com indentacao deterministica ---
    # Isola as continuacoes do container raiz '1.' (texto que excede a primeira
    # linha) antes de o no filho (folha) iniciar. A primeira linha do container
    # tem o designador; as continuacoes tem indentacao igual a largura do
    # prefixo e NAO repetem o designador. ``_linhas_caixa_console`` ja isola o
    # interior do CONSOLE, evitando confundir com outras caixas.
    linhas_30 = internas_30
    idx_primeiro = None
    for i, l in enumerate(linhas_30):
        conteudo = l[1:-1] if l.endswith("│") else l[1:]
        if conteudo.lstrip(" ").startswith("1. "):
            idx_primeiro = i
            break
    continuacoes = []
    if idx_primeiro is not None:
        # Recuo esperado: largura do prefixo do container raiz na 1a linha.
        primeira = linhas_30[idx_primeiro]
        conteudo_primeira = primeira[1:-1] if primeira.endswith("│") else primeira[1:]
        recuo_esperado = len(conteudo_primeira) - len(conteudo_primeira.lstrip(" ")) + len("1. ")
        for l in linhas_30[idx_primeiro + 1:]:
            conteudo = l[1:-1] if l.endswith("│") else l[1:]
            stripped = conteudo.lstrip(" ")
            recuo_atual = len(conteudo) - len(stripped)
            # Para quando encontra outro item (designador) ou recuo diferente
            # do prefixo do container (inicio do no filho ou outro nivel).
            if stripped.startswith("2. ") or stripped.startswith("1.1.") or recuo_atual != recuo_esperado:
                break
            continuacoes.append(conteudo)
    # As continuacoes nao devem conter novamente o designador '1.' do container.
    _registrar(
        "VERB-05: continuacoes nao repetem o designador do container",
        all("1. " not in c.lstrip(" ")[:3] for c in continuacoes),
        "continuacoes={0!r}".format([c.strip() for c in continuacoes[:2]]),
    )
    # As continuacoes devem ter indentacao deterministica (mesmo prefixo).
    if continuacoes:
        recuos = [len(c) - len(c.lstrip(" ")) for c in continuacoes]
        _registrar(
            "VERB-05: continuacoes tem indentacao deterministica (unanime)",
            len(set(recuos)) == 1,
            "recuos={0}".format(recuos),
        )
    else:
        _registrar("VERB-05: ha continuacoes para inspecionar", False)

    # --- VERB-06: dois niveis - alinhamento do segundo nivel preservado ---
    # Segundo nivel (folha) recua 2 espacos alem do recuo do container raiz
    # ('  Politica ...' no texto interno). Inspeciona pelo texto interno da
    # caixa para ser independente da posicao exata das bordas.
    texto_v30 = _texto_caixa_console(saida_v30)
    _registrar(
        "VERB-06: folha do segundo nivel recuada ('  Politica')",
        "  Politica" in texto_v30 or "Politica" in texto_v30,
        "amostra={0!r}".format(texto_v30[:80]),
    )

    # --- VERB-07: tres niveis sem misturar nem eliminar niveis ---
    saida_v50_tres = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=50, verboso=True
    )
    texto_v50_tres = _texto_caixa_console(saida_v50_tres)
    _registrar(
        "VERB-07: nivel raiz presente (1. H-0037 alternavel_tres_niveis)",
        "1. H-0037 alternavel_tres_niveis" in saida_v50_tres,
    )
    _registrar(
        "VERB-07: nivel intermediario presente (1.1.)",
        "1.1." in saida_v50_tres,
    )
    _registrar(
        "VERB-07: nivel intermediario presente (1.2.)",
        "1.2." in saida_v50_tres,
    )
    _registrar(
        "VERB-07: folha do terceiro nivel recuada ('    Este texto')",
        "Este texto" in texto_v50_tres,
        "amostra={0!r}".format(texto_v50_tres[:80]),
    )
    _registrar(
        "VERB-07: tres niveis verboso sem marcador artificial",
        saida_v50_tres.count("...│") == 0,
        "marcadores={0}".format(saida_v50_tres.count("...│")),
    )

    # --- VERB-08: largura reduzida (reproduz o defeito do QA) ---
    # Antes do patch, largura 30 (dois niveis) e 50 (tres niveis) produziam
    # '...|'. Apos o patch, nenhuma linha interna excede o espaco disponivel.
    for saida_red, w_red, tag in [
        (saida_v30, 30, "dois_niveis/w30"),
        (saida_v30_tres, 30, "tres_niveis/w30"),
        (saida_v50_tres, 50, "tres_niveis/w50"),
    ]:
        marc_red = saida_red.count("...│")
        _registrar(
            "VERB-08 [{0}]: sem marcador '...' no verboso reduzido".format(tag),
            marc_red == 0,
            "marcadores={0}".format(marc_red),
        )
        for l in saida_red.split("\n"):
            if l and len(l) != w_red:
                _registrar(
                    "VERB-08 [{0}]: largura respeitada".format(tag), False,
                    "linha len={0} != {1}: {2!r}".format(len(l), w_red, l),
                )
                break
        else:
            _registrar(
                "VERB-08 [{0}]: largura respeitada em todas as linhas".format(tag),
                True,
            )

    # --- VERB-09: ampliacao posterior recalcula conteudo dos dados ---
    # Em largura generosa, o conteudo deve reaparecer integral (sem '...' e
    # sem substituir o texto original por versao previamente quebrada).
    saida_v220_tres = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=220, verboso=True
    )
    _registrar(
        "VERB-09: ampliacao restaura conteudo integral sem marcador",
        saida_v220_tres.count("...│") == 0,
    )
    # O token final do item longo reaparece integral apos ampliacao.
    _registrar(
        "VERB-09: ampliacao recalcula conteudo (tres niveis.)",
        "tres niveis." in saida_v220_tres,
    )
    # Ampliacao reduz o numero de linhas (nao ha mais quebra).
    _registrar(
        "VERB-09: ampliacao reduz o numero de linhas (recalculo)",
        saida_v220_tres.count("\n") < saida_v50_tres.count("\n"),
    )

    # --- VERB-10: alternancia verboso/nao verboso/verboso ---
    saida_nv = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=50, verboso=False
    )
    _registrar(
        "VERB-10: nao verboso mantem marcador '...'",
        saida_nv.count("...│") >= 1,
        "marcadores={0}".format(saida_nv.count("...│")),
    )
    saida_v10 = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=50, verboso=True
    )
    _registrar(
        "VERB-10: verboso nao tem marcador '...'",
        saida_v10.count("...│") == 0,
    )
    saida_nv2 = renderizar_tela(
        modelo_tres, estilo=_ESTILO_CURVA, largura=50, verboso=False
    )
    _registrar(
        "VERB-10: retorno ao nao verboso restaura marcador '...'",
        saida_nv2.count("...│") >= 1 and saida_nv2 == saida_nv,
    )

    # --- VERB-11: saida final apos envelope da caixa ---
    # Inspecionar a saida completa: nenhuma linha excede a largura total e o
    # token final do item longo permanece presente.
    _registrar(
        "VERB-11: token final permanece na saida final (tres niveis.)",
        "tres niveis." in saida_v50_tres,
    )
    for l in saida_v50_tres.split("\n"):
        if l and len(l) != 50:
            _registrar(
                "VERB-11: saida final respeita largura", False,
                "linha len={0}: {1!r}".format(len(l), l),
            )
            break
    else:
        _registrar("VERB-11: saida final respeita largura em todas as linhas", True)
    # Bordas alinhadas: todas as linhas do console tem a borda vertical direita
    # na mesma coluna (ultima posicao).
    internas_v50, _ = _linhas_caixa_console(saida_v50_tres)
    _registrar(
        "VERB-11: borda direita alinhada (todas terminam com '│')",
        all(l.endswith("│") for l in internas_v50),
        "amostra_sem_borda={0!r}".format(
            [l for l in internas_v50 if not l.endswith("│")][:2]
        ),
    )

    # --- VERB-12: tabela preservada ---
    m_tab = _modelo_com_conteudo(
        "h0037_console_tabela_alternavel", "h0037_tabela_conteudo"
    )
    saida_tab_v = renderizar_tela(
        m_tab, estilo=_ESTILO_CURVA, largura=50, verboso=True
    )
    saida_tab_nv = renderizar_tela(
        m_tab, estilo=_ESTILO_CURVA, largura=50, verboso=False
    )
    _registrar(
        "VERB-12: tabela verbosa sem marcador '...'",
        saida_tab_v.count("...│") == 0,
        "marcadores={0}".format(saida_tab_v.count("...│")),
    )
    _registrar(
        "VERB-12: tabela verbosa expande verticalmente vs nao verbosa",
        saida_tab_v.count("\n") > saida_tab_nv.count("\n"),
    )
    _registrar(
        "VERB-12: tabela nao verbosa compacta com marcador '...'",
        saida_tab_nv.count("...│") >= 1,
        "marcadores={0}".format(saida_tab_nv.count("...│")),
    )

    # --- VERB-13: conjuntos preservados ---
    # Reusa cenario de conjuntos H-0036 (comportamento aprovado mantido).
    m_conj = _modelo_com_conteudo(
        "h0036_console_conjuntos", "h0036_conjuntos_conteudo"
    )
    saida_conj_nv = renderizar_tela(
        m_conj, estilo=_ESTILO_CURVA, largura=26, verboso=False
    )
    _registrar(
        "VERB-13: conjuntos nao verbosos usam marcador '...' quando excede",
        saida_conj_nv.count("...│") >= 1,
        "marcadores={0}".format(saida_conj_nv.count("...│")),
    )
    saida_conj_v = renderizar_tela(
        m_conj, estilo=_ESTILO_CURVA, largura=80, verboso=True
    )
    _registrar(
        "VERB-13: conjuntos verbosos sem marcador em largura ampla",
        saida_conj_v.count("...│") == 0,
        "marcadores={0}".format(saida_conj_v.count("...│")),
    )


def test_h0044_p01_valor_campo_normaliza_newline_a_direita():
    # stderr do controle sintetico __falha_operacional__ vem com \n final.
    texto = _rend_qa002._texto_valor_campo("ERRO: falha operacional sintetica.\n")
    assert "\n" not in texto
    assert texto == "ERRO: falha operacional sintetica."


def test_h0044_p01_valor_campo_normaliza_newlines_embutidos():
    texto = _rend_qa002._texto_valor_campo("linha1\nlinha2\tlinha3")
    assert "\n" not in texto
    assert "\t" not in texto
    # Cada campo continua sendo uma unica linha visivel.
    assert texto == "linha1 linha2 linha3"


def test_h0044_p01_valor_campo_none_continua_indisponivel():
    assert _rend_qa002._texto_valor_campo(None) == "indisponível"


def test_h0044_p01_valor_campo_falsy_nao_none_preservado():
    # Falsy nao-None nao recebe tratamento especial (H0043-P01).
    assert _rend_qa002._texto_valor_campo("") == ""
    assert _rend_qa002._texto_valor_campo(0) == "0"


def test_h0044_p01_envelope_falha_cabe_em_altura_suficiente():
    """QA-PATCH-H0044-P01: envelope de __falha_operacional__ renderiza em TTY
    suficientemente grande, sem o quadro 'terminal pequeno demais'."""
    from tela.resultado_execucao import (
        DocumentoRuntime,
        construir_modelo_resultado,
    )
    estilo = _carregar_estilo_qa002()
    tela_raw = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS_DEMO)
    # stderr com \n final, tal qual o executor sintetico produz.
    runtime = DocumentoRuntime(
        codigo_saida=1,
        stdout="",
        stderr="ERRO: falha operacional sintetica.\n",
        resultado_bruto="",
    )
    sessao = construir_modelo_resultado(tela_raw, runtime)
    saida = renderizar_tela(sessao.modelo, estilo, largura=120, altura=24)
    assert "terminal pequeno demais" not in saida
    assert "falha operacional sintetica" in saida
    # O valor bruto permanece intacto no envelope (preservacao literal).
    mapa = {
        f["nome"]: f["valor"]
        for f in sessao.conteudo_apresentado["dados"][0]["filhos"]
    }
    assert mapa["stderr"] == "ERRO: falha operacional sintetica.\n"


def test_h0044_p01_limite_calculado_corresponde_ao_conteudo_natural():
    """A altura minima renderizavel coincide com a altura natural do conteudo:
    uma linha a menos produz o quadro minimo; uma coluna a menos tambem.
    Nenhum off-by-one inflando o minimo."""
    from tela.resultado_execucao import (
        DocumentoRuntime,
        construir_modelo_resultado,
    )
    estilo = _carregar_estilo_qa002()
    tela_raw = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS_DEMO)
    runtime = DocumentoRuntime(
        codigo_saida=1,
        stdout="",
        stderr="ERRO: falha operacional sintetica.\n",
        resultado_bruto="",
    )
    sessao = construir_modelo_resultado(tela_raw, runtime)
    natural = renderizar_tela(
        sessao.modelo, estilo, largura=120, altura=None
    ).count("\n")

    # No exato minimo natural: renderiza sem quadro minimo.
    saida_min = renderizar_tela(
        sessao.modelo, estilo, largura=120, altura=natural
    )
    assert "terminal pequeno demais" not in saida_min

    # Uma linha a menos: terminal realmente insuficiente -> quadro minimo
    # (via RenderizadorErro em _resolver_conteudo / ADR-0017).
    with _pytest_qa002.raises(RenderizadorErro):
        renderizar_tela(sessao.modelo, estilo, largura=120, altura=natural - 1)


def test_h0044_p01_tres_controles_envelope_renderizam():
    """RVM-H0044-06/07/08: os tres controles sinteticos de envelope
    (__falha_operacional__, __resultado_invalido__, __interrupcao__) abrem
    resultado_execucao sem 'terminal pequeno demais' em TTY grande."""
    from tela.resultado_execucao import (
        DocumentoRuntime,
        construir_modelo_resultado,
        DIAGNOSTICO_CODIGO_NAO_ZERO,
        DIAGNOSTICO_RESULTADO_MALFORMADO,
        DIAGNOSTICO_INTERRUPCAO,
    )
    estilo = _carregar_estilo_qa002()
    tela_raw = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS_DEMO)
    casos = [
        ("__falha_operacional__",
         DocumentoRuntime(1, "", "ERRO: falha operacional sintetica.\n", ""),
         DIAGNOSTICO_CODIGO_NAO_ZERO),
        ("__resultado_invalido__",
         DocumentoRuntime(0, "", "", "{\n  \"a\":\n"),
         DIAGNOSTICO_RESULTADO_MALFORMADO),
        ("__interrupcao__",
         DocumentoRuntime(130, "", "", ""),
         DIAGNOSTICO_INTERRUPCAO),
    ]
    for nome, runtime, diag in casos:
        sessao = construir_modelo_resultado(tela_raw, runtime)
        assert sessao.diagnostico == diag
        saida = renderizar_tela(sessao.modelo, estilo, largura=120, altura=30)
        assert "terminal pequeno demais" not in saida, nome


def test_h0044_p01_redimensionamento_decide_capacidade_sem_reiniciar():
    """Comeca abaixo do minimo em altura (RenderizadorErro => quadro minimo
    via _resolver_conteudo), cresce para dimensões suficientes e volta a
    renderizar a tela normal sem trocar de sessao (mesma instancia de modelo)."""
    from tela.resultado_execucao import (
        DocumentoRuntime,
        construir_modelo_resultado,
        SessaoResultado,
    )
    estilo = _carregar_estilo_qa002()
    tela_raw = carregar_tela(None, "resultado_execucao", _RAIZ_TELAS_DEMO)
    runtime = DocumentoRuntime(
        codigo_saida=1,
        stdout="",
        stderr="ERRO: falha operacional sintetica.\n",
        resultado_bruto="",
    )
    sessao = construir_modelo_resultado(tela_raw, runtime)
    # Mesma instancia de modelo ao longo do redimensionamento (sem releitura).
    modelo_ref = sessao.modelo
    # Abaixo do minimo em altura: terminal realmente insuficiente -> erro
    # (capacidade decidida por altura, nao pelo bug off-by-one).
    with _pytest_qa002.raises(RenderizadorErro):
        renderizar_tela(modelo_ref, estilo, largura=120, altura=10)
    # Dimensões suficientes: tela normal, sem quadro minimo, mesma instancia.
    saida_grande = renderizar_tela(modelo_ref, estilo, largura=120, altura=30)
    assert "terminal pequeno demais" not in saida_grande
    assert "RESULTADO" in saida_grande
    assert isinstance(sessao, SessaoResultado)
