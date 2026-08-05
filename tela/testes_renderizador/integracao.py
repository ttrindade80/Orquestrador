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
from tela.testes_renderizador.conteudo_externo import (
    teste_h0037_qapp7_verb_sem_corte_silencioso as _teste_h0037_qapp7_verb_sem_corte_silencioso,
)



__all__ = [
    'test_h0045_p04_dois_consoles_ids_unicos_foco_cursor_e_paginas_independentes',
    'test_h0045_p06_distribuicao_vertical_geometria_por_console_e_renderer_concordam',
    'test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao',
    'test_h0045_p07_console_direto_preservado_regressao',
    'test_h0045_p07_console_dentro_de_grupo_geometria_real',
    'test_h0045_p07_dois_consoles_mesmo_grupo_geometrias_independentes',
    'test_h0045_p07_grupo_aninhado_geometria_considera_ancestrais',
    'test_h0045_p07_console_ausente_retorna_none_sem_fallback',
    'test_h0045_p07_estrutura_matriz_geometria_por_celula',
    'test_h0045_p10_mapa_fisico_usa_largura_da_celula_e_preserva_fragmentos',
    'test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos',
    'test_h0045_p12_quebra_textual_por_largura_marcadores_unicos',
    'test_h0045_p12_continuacao_sem_cursor_regular_e_alta',
    'test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica',
    'test_h0045_ph07_largura_horizontal_celula_unica_quatro_larguras',
    'test_h0045_ph07_coerencia_renderer_mapa_fisico',
    'test_h0045_ph07_distribuicao_matricial_multiplas_celulas_preservada',
    'test_h0045_ph07_regressao_h0037_console_externo',
    'test_h0045_ph07_cinco_telas_validacao',
]


_DM_H0045_P07 = {
    "formacao": {"politica": "preferencia_colunas", "colunas": {"minimo": 1, "maximo": 1}},
    "ordem": "por_linha",
    "dimensionamento": {"colunas": {"politica": "uniforme"}, "linhas": {"politica": "uniforme"}},
    "espacamento": {
        "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
        "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
        "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
    },
    "distribuicao_horizontal": {"politica": "inicio"},
    "distribuicao_vertical": {"politica": "inicio"},
    "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos", "vertical": "uniforme_margens_e_vaos"},
    "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
    "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
}


def _console_paginado_h0045p07(idc, prefixo, n_itens, titulo):
    from tela.modelo import ElementoCorpo

    itens = [
        {"id": "{0}{1:02d}".format(prefixo, i), "texto": "{0}{1:02d}".format(prefixo, i), "navegavel": True}
        for i in range(1, n_itens + 1)
    ]
    return ElementoCorpo(
        id=idc, tipo="console",
        _campos_inertes={
            "titulo": titulo, "itens": itens,
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "unica",
            "politica_paginacao": "com",
        },
        distribuicao_matricial=_DM_H0045_P07,
    )


def _grupo_h0045p07(idg, elementos, arranjo="horizontal", distribuicao=None,
                     estrutura=None, matriz=None):
    from tela.modelo import ElementoCorpo

    return ElementoCorpo(
        id=idg, tipo="grupo",
        _campos_inertes={
            "arranjo": arranjo, "distribuicao": distribuicao,
            "estrutura": estrutura, "matriz": matriz,
        },
        elementos=elementos,
    )


def test_h0045_p04_dois_consoles_ids_unicos_foco_cursor_e_paginas_independentes():
    """P04: com IDs unicos, foco no segundo console materializa cursor so nele.

    Paginas permanecem independentes por console.id (sem compartilhamento).

    H-0045-P06 / QA-H0045-P05-001: largura=80/altura=24 da o suficiente para
    caber os 12 itens de cada console em uma unica pagina (capacidade real da
    coluna horizontal, nao mais o fallback ``capacidade=1`` que o bug de
    ``_renderizar_container_horizontal`` produzia). Uma altura MENOR (15) e
    usada para o segundo bloco, onde varias paginas sao necessarias --
    calculadas pela MESMA autoridade (``paginacao.plano_de_paginacao`` com a
    largura de coluna de ``geometria_console``), nunca por numero hardcoded.
    """
    import re
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao, paginacao
    from tela.renderizador import renderizar_tela, geometria_console

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_dois_consoles_paginas_independentes",
            "config/telas/demo",
        )
    )
    lista = navegacao.lista_foco(modelo)
    assert len(lista) == 2
    console_a, console_b = lista
    assert console_a.id == "console_a"
    assert console_b.id == "console_b"
    assert console_a.id != console_b.id

    estilo = carregar_estilo()
    simbolo = estilo.selecionado_simbolo

    # Foco no SEGUNDO console: cursor prefixa b01, nunca a01.
    saida = renderizar_tela(
        modelo,
        estilo,
        largura=80,
        altura=24,
        foco_console=1,
        cursores={console_a.id: 0, console_b.id: 0},
        lista_foco=lista,
        paginas_atuais={console_a.id: 1, console_b.id: 1},
    )
    assert "a01" in saida and "b01" in saida
    # Em arranjo horizontal os dois itens podem compartilhar a mesma linha
    # fisica; a prova e o PREFIXO do cursor imediatamente antes do item.
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("b01"), saida)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("a01"), saida)
    # QA-H0045-P05-001: os 12 itens cabem em uma unica pagina real; total
    # concorda entre o render e a autoridade de geometria/paginacao.
    assert "página 1/1" in saida
    geometria_a = geometria_console(
        modelo, estilo, 80, 24, False, console=console_a, lista_foco=lista,
    )
    total_a = paginacao.total_paginas(
        console_a, geometria_a["largura"], geometria_a["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total_a == 1

    # Paginas independentes com geometria estreita o suficiente para exigir
    # mais de uma pagina (capacidade real derivada -- nao hardcoded).
    largura, altura = 80, 15
    geometria_b = geometria_console(
        modelo, estilo, largura, altura, False, console=console_b, lista_foco=lista,
    )
    total_b = paginacao.total_paginas(
        console_b, geometria_b["largura"], geometria_b["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total_b > 1, "geometria={0} deveria exigir mais de 1 pagina".format(geometria_b)
    pagina_b09 = paginacao.pagina_do_item_logico(
        console_b, 8, geometria_b["largura"], geometria_b["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert pagina_b09 > 1, "b09 deveria estar fora da primeira pagina nesta geometria"

    saida_pag = renderizar_tela(
        modelo,
        estilo,
        largura=largura,
        altura=altura,
        foco_console=1,
        cursores={console_a.id: 0, console_b.id: 8},
        lista_foco=lista,
        paginas_atuais={console_a.id: 1, console_b.id: pagina_b09},
    )
    assert "página 1/{0}".format(total_b) in saida_pag
    assert "página {0}/{1}".format(pagina_b09, total_b) in saida_pag
    assert "a01" in saida_pag
    assert "b09" in saida_pag
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("b09"), saida_pag)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("a01"), saida_pag)


def test_h0045_p06_distribuicao_vertical_geometria_por_console_e_renderer_concordam():
    """H-0045-P06 (Teste 5): dois consoles em DISTRIBUICAO VERTICAL explicita.

    Modelo em memoria (sem fixture permanente em config/telas/): dois
    consoles paginados empilhados verticalmente com pesos DISTINTOS
    (``"fracao": [2, 1]``) recebem cotas de altura DIFERENTES -- confirma que
    ``geometria_console`` reproduz EXATAMENTE a mesma particao de
    ``_renderizar_container_vertical`` (``_distribuir_alturas``) e que o
    total de paginas/cursor do render concordam com o plano calculado pela
    MESMA autoridade (``paginacao.total_paginas``/``pagina_do_item_logico``).
    """
    import re
    from tela.loader import carregar_estilo
    from tela.modelo import ElementoCorpo, ModeloTela, Corpo
    from tela.renderizador import renderizar_tela, geometria_console
    from tela import paginacao

    distribuicao_matricial = {
        "formacao": {"politica": "preferencia_colunas", "colunas": {"minimo": 1, "maximo": 1}},
        "ordem": "por_linha",
        "dimensionamento": {"colunas": {"politica": "uniforme"}, "linhas": {"politica": "uniforme"}},
        "espacamento": {
            "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
            "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
            "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
        },
        "distribuicao_horizontal": {"politica": "inicio"},
        "distribuicao_vertical": {"politica": "inicio"},
        "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos", "vertical": "uniforme_margens_e_vaos"},
        "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
        "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
    }

    def _console_paginado(idc, prefixo, n_itens, titulo):
        itens = [
            {"id": "{0}{1:02d}".format(prefixo, i), "texto": "{0}{1:02d}".format(prefixo, i), "navegavel": True}
            for i in range(1, n_itens + 1)
        ]
        return ElementoCorpo(
            id=idc, tipo="console",
            _campos_inertes={
                "titulo": titulo, "itens": itens,
                "politica_navegacao": {"navegavel": True},
                "politica_selecao": "unica",
                "politica_paginacao": "com",
            },
            distribuicao_matricial=distribuicao_matricial,
        )

    console_x = _console_paginado("console_x", "x", 12, "X")
    console_y = _console_paginado("console_y", "y", 12, "Y")
    modelo = ModeloTela(
        id="t5", schema="tela.v1",
        cabecalho={"titulo": "Vertical", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(
            arranjo="vertical",
            distribuicao={"modo": "fracao", "valores": [2, 1]},
            elementos=[console_x, console_y],
        ),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 24
    lista_foco = [console_x, console_y]

    geometria_x = geometria_console(modelo, estilo, largura, altura, False, console=console_x)
    geometria_y = geometria_console(modelo, estilo, largura, altura, False, console=console_y)
    assert geometria_x is not None and geometria_y is not None
    # "fracao": [2, 1] -- X recebe o DOBRO da cota vertical de Y (mesmo
    # algoritmo _distribuir_alturas usado por _renderizar_container_vertical
    # -- nao uma aproximacao separada).
    assert geometria_x["altura_interna"] > geometria_y["altura_interna"]
    assert geometria_x["largura"] == geometria_y["largura"] == largura

    total_x = paginacao.total_paginas(
        console_x, geometria_x["largura"], geometria_x["altura_interna"], False,
        desconto_estrutural=3,
    )
    total_y = paginacao.total_paginas(
        console_y, geometria_y["largura"], geometria_y["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total_x >= 1 and total_y >= 1
    # X tem mais capacidade por pagina (cota maior); com o mesmo numero de
    # itens (12), X precisa de nao mais paginas que Y.
    assert total_x <= total_y

    simbolo = estilo.selecionado_simbolo
    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura,
        foco_console=0, cursores={console_x.id: 0, console_y.id: 0},
        lista_foco=lista_foco,
        paginas_atuais={console_x.id: 1, console_y.id: 1},
    )
    # Plano compartilhado (paginacao) e renderer concordam no total.
    assert "página 1/{0}".format(total_x) in saida
    assert "página 1/{0}".format(total_y) in saida
    # Cursor e pagina coerentes: apenas o console focado exibe cursor.
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("x01"), saida)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("y01"), saida)


def test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao(tmp_path):
    """P04: tela com IDs duplicados nao chega ao renderer (sem quadro parcial)."""
    import json
    from pathlib import Path
    from tela.loader import carregar_tela, TelaEstruturaInvalida
    from tela.modelo import construir_modelo
    from tela.renderizador import renderizar_tela
    from tela.loader import carregar_estilo

    def _console(cid):
        return {
            "id": cid,
            "tipo": "console",
            "titulo": cid,
            "itens": [
                {"id": "i1", "texto": "x", "navegavel": True},
            ],
            "origem_dados": None,
            "politica_composicao": {
                "alinhamento": "esquerda",
                "overflow_normal": "truncar_com_reticencias",
            },
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "unica",
            "politica_paginacao": "sem",
            "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
        }

    id_tela = "h0045_p04_dup_render"
    dados = {
        "schema": "tela.v1",
        "id": id_tela,
        "cabecalho": {"titulo": "X", "descricao": "Y", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        "corpo": {
            "arranjo": "horizontal",
            "distribuicao": {"modo": "igual"},
            "elementos": [_console("console_a"), _console("console_a")],
        },
        "barra_de_menus": {"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
    }
    raiz = Path(tmp_path) / "config" / "telas" / "demo"
    raiz.mkdir(parents=True)
    (raiz / "{0}.json".format(id_tela)).write_text(
        json.dumps(dados), encoding="utf-8"
    )

    renderizou = False
    try:
        tela = carregar_tela(str(tmp_path), id_tela, "config/telas/demo")
        modelo = construir_modelo(tela)
        renderizar_tela(modelo, carregar_estilo(), largura=80, altura=24)
        renderizou = True
    except TelaEstruturaInvalida as exc:
        assert "id de console duplicado" in str(exc)
    assert renderizou is False, "duplicidade nao pode produzir quadro parcial"


def test_h0045_p07_console_direto_preservado_regressao():
    """H-0045-P07 (Teste 1): console DIRETO no corpo raiz preserva o P06.

    Regressao positiva: a autoridade recursiva do P07 SO adiciona cobertura
    para grupo/matriz -- o caminho direto (console de primeiro nivel no
    corpo raiz), ja coberto por ``_renderizar_container_vertical``/
    ``_renderizar_container_horizontal`` antes deste patch, permanece
    identico: mesma geometria, mesma paginacao, mesmo cursor.
    """
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao, paginacao
    from tela.renderizador import renderizar_tela, geometria_console

    modelo = construir_modelo(
        carregar_tela(None, "h0045_dois_consoles_paginas_independentes", "config/telas/demo")
    )
    lista = navegacao.lista_foco(modelo)
    console_a, console_b = lista
    estilo = carregar_estilo()
    largura, altura = 80, 15

    geometria_a = geometria_console(
        modelo, estilo, largura, altura, False, console=console_a, lista_foco=lista,
    )
    geometria_b = geometria_console(
        modelo, estilo, largura, altura, False, console=console_b, lista_foco=lista,
    )
    assert geometria_a is not None and geometria_b is not None
    assert geometria_a == geometria_b  # colunas iguais (distribuicao "igual")
    assert geometria_a["largura"] == 40

    total_a = paginacao.total_paginas(
        console_a, geometria_a["largura"], geometria_a["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total_a > 1
    pagina_a09 = paginacao.pagina_do_item_logico(
        console_a, 8, geometria_a["largura"], geometria_a["altura_interna"], False,
        desconto_estrutural=3,
    )

    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura, foco_console=0,
        cursores={console_a.id: 8, console_b.id: 0}, lista_foco=lista,
        paginas_atuais={console_a.id: pagina_a09, console_b.id: 1},
    )
    assert "a09" in saida
    assert "página {0}/{1}".format(pagina_a09, total_a) in saida


def test_h0045_p07_console_dentro_de_grupo_geometria_real():
    """H-0045-P07 (Teste 2 / QA-H0045-P06-001): console PAGINADO em grupo.

    Antes deste patch, ``_geometria_por_console`` so mapeava elementos
    DIRETOS de ``corpo.elementos[]`` -- um console dentro de um grupo
    permitido (H-0027) nunca aparecia no mapa, e ``geometria_console``
    devolvia silenciosamente ``next(iter(mapa.values()))`` (a geometria de
    outro elemento). Confirma que a geometria devolvida agora e a caixa REAL
    do console interno e que paginacao/cursor concordam com o renderer.
    """
    from tela.modelo import ModeloTela, Corpo
    from tela.loader import carregar_estilo
    from tela.renderizador import renderizar_tela, geometria_console
    from tela import paginacao

    console_interno = _console_paginado_h0045p07("console_interno", "z", 30, "Z")
    grupo = _grupo_h0045p07("grupo_unico", [console_interno])
    modelo = ModeloTela(
        id="t2", schema="tela.v1",
        cabecalho={"titulo": "Grupo", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[grupo]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 12
    lista_foco = [console_interno]

    geometria = geometria_console(
        modelo, estilo, largura, altura, False, console=console_interno,
        lista_foco=lista_foco,
    )
    assert geometria is not None
    assert geometria["largura"] == largura  # DA-01: grupo unico ocupa a largura total
    assert geometria["altura_interna"] > 0

    total = paginacao.total_paginas(
        console_interno, geometria["largura"], geometria["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total > 1, "geometria={0} deveria exigir mais de 1 pagina".format(geometria)
    pagina_alvo = paginacao.pagina_do_item_logico(
        console_interno, 20, geometria["largura"], geometria["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert pagina_alvo > 1

    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura, foco_console=0,
        cursores={console_interno.id: 20}, lista_foco=lista_foco,
        paginas_atuais={console_interno.id: pagina_alvo},
    )
    assert "z21" in saida
    assert "página {0}/{1}".format(pagina_alvo, total) in saida


def test_h0045_p07_dois_consoles_mesmo_grupo_geometrias_independentes():
    """H-0045-P07 (Teste 3): dois consoles paginados no MESMO grupo horizontal.

    Confirma geometrias, paginas e cursor INDEPENDENTES por ``console.id``:
    nenhum dos dois recebe a geometria do outro (o fallback antigo produzia a
    MESMA geometria de "primeira entrada do mapa" para qualquer console
    solicitado do grupo).
    """
    import re
    from tela.modelo import ModeloTela, Corpo
    from tela.loader import carregar_estilo
    from tela.renderizador import renderizar_tela, geometria_console
    from tela import paginacao

    console_p = _console_paginado_h0045p07("console_p", "p", 20, "P")
    console_q = _console_paginado_h0045p07("console_q", "q", 20, "Q")
    grupo = _grupo_h0045p07(
        "grupo_par", [console_p, console_q], distribuicao={"modo": "igual"},
    )
    modelo = ModeloTela(
        id="t3", schema="tela.v1",
        cabecalho={"titulo": "Par", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[grupo]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 12
    lista_foco = [console_p, console_q]

    geometria_p = geometria_console(
        modelo, estilo, largura, altura, False, console=console_p, lista_foco=lista_foco,
    )
    geometria_q = geometria_console(
        modelo, estilo, largura, altura, False, console=console_q, lista_foco=lista_foco,
    )
    assert geometria_p is not None and geometria_q is not None
    assert geometria_p["largura"] == geometria_q["largura"] == 20  # coluna real (40/2)
    assert geometria_p["altura_interna"] == geometria_q["altura_interna"]

    total_p = paginacao.total_paginas(
        console_p, geometria_p["largura"], geometria_p["altura_interna"], False,
        desconto_estrutural=3,
    )
    total_q = paginacao.total_paginas(
        console_q, geometria_q["largura"], geometria_q["altura_interna"], False,
        desconto_estrutural=3,
    )
    assert total_p > 1 and total_q > 1

    pagina_p = paginacao.pagina_do_item_logico(
        console_p, 10, geometria_p["largura"], geometria_p["altura_interna"], False,
        desconto_estrutural=3,
    )
    simbolo = estilo.selecionado_simbolo
    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura, foco_console=0,
        cursores={console_p.id: 10, console_q.id: 0}, lista_foco=lista_foco,
        paginas_atuais={console_p.id: pagina_p, console_q.id: 1},
    )
    # Paginacao de um console em pagina avancada nao afeta o outro (pagina 1).
    assert "página {0}/{1}".format(pagina_p, total_p) in saida
    assert "página 1/{0}".format(total_q) in saida
    # Cursor aparece apenas no console focado (p), nunca em q.
    assert re.search(re.escape(simbolo) + r"\s*" + re.escape("p11"), saida)
    assert not re.search(re.escape(simbolo) + r"\s*" + re.escape("q01"), saida)


def test_h0045_p07_grupo_aninhado_geometria_considera_ancestrais():
    """H-0045-P07 (Teste 4): grupo dentro de grupo (H-0027 D5/D6, ate 3 niveis).

    O console de segundo nivel recebe a cota do SEU ancestral direto (grupo
    interno), que por sua vez recebeu uma FRACAO da cota do corpo -- nao a
    altura integral do corpo raiz. Confirma que a autoridade recursiva
    considera TODOS os ancestrais na cadeia, nao apenas o pai imediato.
    """
    from tela.modelo import ModeloTela, Corpo
    from tela.loader import carregar_estilo
    from tela.renderizador import renderizar_tela, geometria_console
    from tela import paginacao

    console_aninhado = _console_paginado_h0045p07("console_aninhado", "n", 20, "N")
    console_direto = _console_paginado_h0045p07("console_direto", "d", 20, "D")
    grupo_interno = _grupo_h0045p07("grupo_interno", [console_aninhado], arranjo="vertical")
    grupo_externo = _grupo_h0045p07(
        "grupo_externo", [grupo_interno, console_direto],
        arranjo="vertical", distribuicao={"modo": "fracao", "valores": [3, 1]},
    )
    modelo = ModeloTela(
        id="t4", schema="tela.v1",
        cabecalho={"titulo": "Aninhado", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[grupo_externo]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 24
    lista_foco = [console_aninhado, console_direto]

    geometria_aninhado = geometria_console(
        modelo, estilo, largura, altura, False, console=console_aninhado,
        lista_foco=lista_foco,
    )
    geometria_direto = geometria_console(
        modelo, estilo, largura, altura, False, console=console_direto,
        lista_foco=lista_foco,
    )
    assert geometria_aninhado is not None and geometria_direto is not None
    # fracao [3, 1]: o console de 2o nivel (dentro do grupo interno, que
    # recebeu a cota MAIOR da distribuicao do grupo externo) tem altura maior
    # que o console direto (cota menor) -- a cota considera o ANCESTRAL.
    assert geometria_aninhado["altura_interna"] > geometria_direto["altura_interna"]
    assert geometria_aninhado["largura"] == geometria_direto["largura"] == largura

    total_aninhado = paginacao.total_paginas(
        console_aninhado, geometria_aninhado["largura"], geometria_aninhado["altura_interna"],
        False, desconto_estrutural=3,
    )
    total_direto = paginacao.total_paginas(
        console_direto, geometria_direto["largura"], geometria_direto["altura_interna"],
        False, desconto_estrutural=3,
    )
    assert total_aninhado <= total_direto  # mais capacidade -> nao mais paginas

    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura, foco_console=0,
        cursores={console_aninhado.id: 0, console_direto.id: 0}, lista_foco=lista_foco,
        paginas_atuais={console_aninhado.id: 1, console_direto.id: 1},
    )
    assert "página 1/{0}".format(total_aninhado) in saida
    assert "página 1/{0}".format(total_direto) in saida


def test_h0045_p07_console_ausente_retorna_none_sem_fallback():
    """H-0045-P07 (Teste 5 / QA-H0045-P06-001): console fora do modelo.

    ``geometria_console`` NUNCA mais devolve a primeira entrada do mapa para
    um console ausente/inexistente -- retorna ``None`` explicitamente, sem
    alterar pagina/cursor/selecao (responsabilidade do chamador, que ja
    preserva o estado corrente quando recebe ``None``).
    """
    from tela.modelo import ElementoCorpo, ModeloTela, Corpo
    from tela.loader import carregar_estilo
    from tela.renderizador import geometria_console

    console_real = _console_paginado_h0045p07("console_real", "r", 5, "R")
    modelo = ModeloTela(
        id="t5", schema="tela.v1",
        cabecalho={"titulo": "Ausente", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[console_real]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 24

    # sanity: o console REAL tem geometria valida nesta configuracao.
    geometria_real = geometria_console(
        modelo, estilo, largura, altura, False, console=console_real,
    )
    assert geometria_real is not None

    console_estranho = ElementoCorpo(id="nao_existe", tipo="console", _campos_inertes={})
    resultado = geometria_console(
        modelo, estilo, largura, altura, False, console=console_estranho,
    )
    assert resultado is None, "console ausente nao pode receber geometria de outro elemento"
    assert resultado != geometria_real

    # console=None (nenhum console solicitado) tambem retorna None.
    assert geometria_console(modelo, estilo, largura, altura, False, console=None) is None


def test_h0045_p07_estrutura_matriz_geometria_por_celula():
    """H-0045-P07 (Teste 6): grupo ``estrutura: matriz`` com console por celula.

    Confirma que a autoridade recursiva atravessa
    ``_renderizar_container_matriz`` e atribui a cada console a
    largura/altura da SUA celula (linha x coluna), nao a area total do grupo
    nem a de outra celula.
    """
    from tela.modelo import ModeloTela, Corpo
    from tela.loader import carregar_estilo
    from tela.renderizador import renderizar_tela, geometria_console

    console_m1 = _console_paginado_h0045p07("console_m1", "m", 5, "M1")
    console_m2 = _console_paginado_h0045p07("console_m2", "n", 5, "M2")
    matriz_config = {
        "linhas": {"quantidade": 1, "distribuicao": {"modo": "igual"}},
        "colunas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
        "celulas": [
            {"linha": 1, "coluna": 1, "elemento": "console_m1"},
            {"linha": 1, "coluna": 2, "elemento": "console_m2"},
        ],
    }
    grupo_matriz = _grupo_h0045p07(
        "grupo_matriz", [console_m1, console_m2],
        arranjo=None, estrutura="matriz", matriz=matriz_config,
    )
    modelo = ModeloTela(
        id="t6", schema="tela.v1",
        cabecalho={"titulo": "Matriz", "descricao": "d", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[grupo_matriz]),
        barra_de_menus={"chips": []}, _raw={},
    )
    estilo = carregar_estilo()
    largura, altura = 40, 12
    lista_foco = [console_m1, console_m2]

    geometria_m1 = geometria_console(
        modelo, estilo, largura, altura, False, console=console_m1, lista_foco=lista_foco,
    )
    geometria_m2 = geometria_console(
        modelo, estilo, largura, altura, False, console=console_m2, lista_foco=lista_foco,
    )
    assert geometria_m1 is not None and geometria_m2 is not None
    assert geometria_m1["largura"] == geometria_m2["largura"] == 20  # 40/2 colunas iguais
    assert geometria_m1["altura_interna"] == geometria_m2["altura_interna"]

    saida = renderizar_tela(
        modelo, estilo, largura=largura, altura=altura, foco_console=0,
        cursores={console_m1.id: 0, console_m2.id: 0}, lista_foco=lista_foco,
        paginas_atuais={console_m1.id: 1, console_m2.id: 1},
    )
    assert isinstance(saida, str) and saida


def test_h0045_p10_mapa_fisico_usa_largura_da_celula_e_preserva_fragmentos():
    """P10: o mapa fisico e o renderer compartilham a quebra matricial real."""
    from tela import paginacao
    from tela.renderizador import mapa_fisico_de_itens

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_modo_verboso_multilinha",
            _RAIZ_TELAS_DEMO,
        )
    )
    console = modelo.corpo.elementos[0]
    mapa = mapa_fisico_de_itens(
        console, 80, 16, True, desconto_estrutural=3,
    )
    plano = paginacao.plano_de_paginacao(
        console, 80, 16, True, desconto_estrutural=3,
    )
    assert plano["total_paginas"] > 1
    assert any(entrada["linhas_fisicas"] > 1 for entrada in mapa)

    saida = renderizar_tela(
        modelo,
        _ESTILO_CURVA,
        largura=80,
        altura=24,
        verboso=True,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=[console],
        paginas_atuais={console.id: 1},
    )
    # VM-H0045-R07-001: a correcao de largura horizontal reduz o numero de
    # linhas fisicas por item (texto usa toda a largura util), diminuindo o
    # total de paginas em relacao ao calculo antigo -- o indicador deve
    # refletir o total corrente, nao um valor fixo historico.
    assert saida and "página 1/{0}".format(plano["total_paginas"]) in saida

    linhas_por_id = {entrada["id"]: entrada["linhas_fisicas"] for entrada in mapa}
    linhas_fragmentadas = {}
    for pagina in plano["paginas"]:
        for fragmento in pagina["fragmentos"]:
            linhas_fragmentadas[fragmento["id"]] = (
                linhas_fragmentadas.get(fragmento["id"], 0)
                + fragmento["linhas_fisicas"]
            )
    assert linhas_fragmentadas == linhas_por_id


def test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos():
    """VM-H0045-R07-003: console paginado com ``itens: []`` real nao e
    focalizavel (ADR-0031 D2 exige >= 1 item navegavel para entrar em
    ``navegacao.lista_foco``), mas ainda declara ``politica_paginacao:
    "com"`` -- ``contrato_console.md`` §12 exige que ``[<]``/``[>]``
    "existem quando a instancia declara paginacao: com", nao apenas quando o
    console e focalizavel. Antes deste patch, a existencia dos chips era
    derivada de ``lista_foco`` (somente consoles focalizaveis), omitindo os
    chips por completo em vez de exibi-los inativos."""
    from tela import navegacao
    from tela import renderizador as _rend

    modelo = construir_modelo(
        carregar_tela(None, "h0045_paginacao_conjunto_vazio", _RAIZ_TELAS_DEMO)
    )
    console = modelo.corpo.elementos[0]
    assert console._campos_inertes.get("itens") == []
    assert navegacao.console_e_focalizavel(console) is False
    assert navegacao.lista_foco(modelo) == []

    saida = renderizar_tela(
        modelo,
        _ESTILO_CURVA,
        largura=80,
        altura=24,
        foco_console=None,
        cursores={},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={},
    )
    assert "página 1/1" in saida
    assert "[<]" in saida
    assert "[>]" in saida
    codigo_inativo = _rend._codigo_ansi_de_cor(_ESTILO_CURVA.cor_inativo)
    assert codigo_inativo + "[<]" in saida
    assert codigo_inativo + "[>]" in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is False
    assert _rend._navegacao_atual.get("cursores") == {}
    # Nenhum conteudo default/sintetico: a caixa "Vazio" nao contem texto de
    # item algum (nem o placeholder historico "(console)", exclusivo de
    # conteudo_externo ausente -- fora de escopo aqui).
    assert "aviso_" not in saida
    assert "info_0" not in saida


def _p12_montar_caso_render(entrada, largura=80, altura=24):
    from demo import casos_validacao_paginacao as cv
    from demo.demo import (
        criar_estado_inicial,
        _carregar_modelo_por_id,
        _aplicar_caso_validacao_adaptativo,
        _estabelecer_foco_paginacao_inicial,
        _modo_verboso_de_modelo,
    )

    modelo = _carregar_modelo_por_id(entrada)
    estado = criar_estado_inicial()
    estado.update(
        {
            "estilo": _ESTILO_CURVA,
            "largura": largura,
            "altura": altura,
            "desconto_estrutural": 3,
            "tela_atual": entrada,
            "caso_validacao_adaptativo": cv.id_caso_de_entrada(entrada),
            "modo_verboso": True,
        }
    )
    estado, caso = _aplicar_caso_validacao_adaptativo(
        estado, modelo, estado["caso_validacao_adaptativo"]
    )
    estado = _estabelecer_foco_paginacao_inicial(estado, modelo)
    estado["modo_verboso"] = _modo_verboso_de_modelo(modelo) or True
    return estado, modelo, caso


def test_h0045_p12_quebra_textual_por_largura_marcadores_unicos():
    """Linha logica > W produz 2+ linhas fisicas; marcadores uma unica vez."""
    from demo import casos_validacao_paginacao as cv
    from tela.renderizador import mapa_fisico_de_itens

    for largura, altura in ((80, 24), (60, 24), (80, 40)):
        estado, modelo, caso = _p12_montar_caso_render(
            "h0045_validacao_largura", largura, altura
        )
        console = modelo.corpo.elementos[0]
        C = caso["C"]
        mapa = mapa_fisico_de_itens(
            console, largura, C, True, desconto_estrutural=3
        )
        assert mapa[0]["linhas_fisicas"] >= 2
        assert caso["propriedades"]["comprimento_logico"] > caso["W"]
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=largura, altura=altura,
            verboso=True, foco_console=estado.get("foco_console"),
            cursores=estado.get("cursores", {}),
            lista_foco=[console] if estado.get("foco_console") is not None else [],
            paginas_atuais=estado.get("pagina_atual", {}),
        )
        for marcador in ("LARGURA_INICIO", "LARGURA_MEIO", "LARGURA_FIM"):
            assert saida.count(marcador) == 1
        assert caso["rotulo"] in saida


def test_h0045_p12_continuacao_sem_cursor_regular_e_alta():
    """Pagina de continuacao sem cursor em geometria regular e alta."""
    from tela import paginacao
    from demo.demo import processar_comando, renderizar_estado

    for largura, altura in ((80, 24), (80, 40)):
        estado, modelo, caso = _p12_montar_caso_render(
            "h0045_validacao_continuacao", largura, altura
        )
        console = modelo.corpo.elementos[0]
        C = caso["C"]
        plano = paginacao.plano_de_paginacao(
            console, largura, C, True, desconto_estrutural=3
        )
        assert plano["total_paginas"] >= 3
        # Avanca ate a primeira pagina sem inicio navegavel.
        alvo = None
        for p in plano["paginas"]:
            if p["fragmentos"] and not any(
                f["primeira_linha_do_item"] and f["navegavel"]
                for f in p["fragmentos"]
            ):
                alvo = p["pagina"]
                break
        assert alvo is not None
        while estado["pagina_atual"].get(console.id, 1) < alvo:
            estado = processar_comando(estado, ".", modelo)
        saida = renderizar_estado(estado, modelo, largura, altura)
        assert saida.count(_ESTILO_CURVA.selecionado_simbolo) == 0
        assert "CONT_" in saida
        assert console.id not in estado.get("cursores", {})


def test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica():
    from tela import renderizador as _rend
    from tela.renderizador import geometria_console
    from demo.demo import processar_comando, renderizar_estado
    from tela import navegacao

    for largura, altura in ((80, 24), (80, 40), (50, 20)):
        estado, modelo, caso = _p12_montar_caso_render(
            "h0045_validacao_vazio", largura, altura
        )
        console = modelo.corpo.elementos[0]
        assert console._campos_inertes.get("itens") == []
        saida = renderizar_estado(estado, modelo, largura, altura)
        assert "página 1/1" in saida
        assert "[<]" in saida and "[>]" in saida
        assert _ESTILO_CURVA.selecionado_simbolo not in saida
        estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
        assert estados.get("chip_pagina_anterior") is False
        assert estados.get("chip_pagina_proxima") is False
        for cmd in (",", ".", "\x1b[A", "\x1b[B"):
            novo = processar_comando(estado, cmd, modelo)
            assert novo["cursores"] == {}
        # Autoridade geometrica permanece disponivel (nao regressao).
        geo = geometria_console(
            modelo, _ESTILO_CURVA, largura, altura, False,
            console=console, foco_console=None, cursores={},
            lista_foco=navegacao.lista_foco(modelo),
            paginas_atuais={},
        )
        assert geo is not None
        assert geo["altura_interna"] == caso["C"]


def _caixa_console_paginado_ph07(saida):
    """Isola a ULTIMA caixa cuja borda inferior contem o indicador de pagina.

    Os cenarios H-0045 desta secao tem uma caixa descritiva estatica seguida
    da caixa do console paginado, ambas as vezes com o MESMO titulo -- o
    indicador "pagina X/Y" na borda inferior identifica sem ambiguidade a
    caixa do console (a descritiva nunca o exibe). Retorna (linhas_da_caixa
    incluindo bordas, largura_total_da_linha).
    """
    linhas = [l for l in saida.split("\n") if l]
    caixas = []
    atual = None
    for l in linhas:
        s = l.strip()
        if s.startswith("╭"):
            atual = [l]
        elif atual is not None:
            atual.append(l)
            if s.startswith("╰"):
                caixas.append(atual)
                atual = None
    for caixa in reversed(caixas):
        if "página" in caixa[-1]:
            return caixa, len(caixa[0])
    return None, 0


def _margens_estruturais_ph07(console):
    esp = console.distribuicao_matricial.get("espacamento", {})
    marg_e = int((esp.get("margem_esquerda") or {}).get("minimo", 0) or 0)
    marg_d = int((esp.get("margem_direita") or {}).get("minimo", 0) or 0)
    return marg_e, marg_d


def test_h0045_ph07_largura_horizontal_celula_unica_quatro_larguras():
    """VM-H0045-R07-001: em 80/120/160/200 colunas, a celula unica do console
    matricial verboso (H-0045-VAL, coluna unica) usa toda a largura util
    atribuida -- sem o teto arbitrario de metade da area --, com coerencia
    entre a largura do mapa fisico e a largura util real, sem overflow, sem
    perda/duplicacao de conteudo, com o indicador de pagina preservado e com
    a identidade dos itens estavel entre geometrias (resize)."""
    from tela.renderizador import (
        mapa_fisico_de_itens,
        _larguras_mapa_fisico_matricial,
        _participantes_distribuicao_matricial,
        DESCONTO_ESTRUTURAL_CONSOLE,
        geometria_console,
    )
    from tela import navegacao, paginacao

    modelo = construir_modelo(
        carregar_tela(
            None, "h0045_paginacao_modo_verboso_multilinha", _RAIZ_TELAS_DEMO,
        )
    )
    console = modelo.corpo.elementos[0]
    lista_foco = navegacao.lista_foco(modelo)
    participantes = _participantes_distribuicao_matricial(console)
    marg_e, marg_d = _margens_estruturais_ph07(console)

    ids_totais = None
    maior_linha_anterior = -1
    altura = 24
    for largura in (80, 120, 160, 200):
        geo = geometria_console(
            modelo, _ESTILO_CURVA, largura, altura, False,
            console=console, lista_foco=lista_foco,
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=largura, altura=altura,
            verboso=True, foco_console=0, cursores={console.id: 0},
            lista_foco=[console], paginas_atuais={console.id: 1},
        )
        caixa, largura_total = _caixa_console_paginado_ph07(saida)
        assert caixa is not None

        # 7. ausencia de overflow: toda linha da caixa mede exatamente a
        # largura do terminal corrente.
        assert largura_total == largura
        assert all(len(l) == largura for l in caixa)

        # 1./2. celula unica usa a largura util; a maior linha fisica cresce
        # (nunca diminui) com a largura, e ultrapassa a metade da area --
        # prova objetiva de que o teto de metade da area foi removido.
        conteudos = [l[1:-1].rstrip() for l in caixa[1:-1] if l.startswith("│")]
        maior_linha = max((len(c) for c in conteudos), default=0)
        area_w = largura - DESCONTO_ESTRUTURAL_CONSOLE
        assert maior_linha > (area_w // 2)
        assert maior_linha >= maior_linha_anterior
        maior_linha_anterior = maior_linha

        # 3./4. largura do mapa fisico == largura util real (area menos
        # somente os descontos estruturais reais: margens; o indicador ja
        # esta incluso na largura da celula).
        larguras_mapa = _larguras_mapa_fisico_matricial(
            console, area_w, geo["altura_interna"], True, participantes,
        )
        largura_util_esperada = area_w - marg_e - marg_d
        assert larguras_mapa and all(
            w == largura_util_esperada for w in larguras_mapa.values()
        )

        # 5./6. ausencia de perda/duplicacao: fragmentos de todas as paginas
        # somam exatamente as linhas fisicas do mapa, por item (CA-H0045-09).
        mapa = mapa_fisico_de_itens(
            console, largura, geo["altura_interna"], True,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        plano = paginacao.plano_de_paginacao(
            console, largura, geo["altura_interna"], True,
            desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
        )
        linhas_por_id = {e["id"]: e["linhas_fisicas"] for e in mapa}
        linhas_fragmentadas = {}
        for pagina in plano["paginas"]:
            for frag in pagina["fragmentos"]:
                linhas_fragmentadas[frag["id"]] = (
                    linhas_fragmentadas.get(frag["id"], 0)
                    + frag["linhas_fisicas"]
                )
        assert linhas_fragmentadas == linhas_por_id

        # 9. resize: identidade/ordem dos itens preservada entre geometrias.
        ids_atuais = list(linhas_por_id)
        if ids_totais is None:
            ids_totais = ids_atuais
        assert ids_atuais == ids_totais

        # 8. indicador de pagina preservado e coerente com o total corrente.
        borda_inferior = caixa[-1]
        assert (
            "página 1/{0}".format(plano["total_paginas"]) in borda_inferior
        )


def test_h0045_ph07_coerencia_renderer_mapa_fisico():
    """VM-H0045-R07-001 (D-TEC-04): a largura de celula efetivamente usada
    pelo motor de distribuicao dentro de ``_linhas_distribuicao_matricial``
    (renderer) e IGUAL, nas quatro larguras exigidas, a largura calculada por
    ``_larguras_mapa_fisico_matricial`` (mapa fisico consumido pela
    paginacao) -- nunca dois calculos paralelos divergentes."""
    import importlib
    _rend = importlib.import_module("tela.renderizacao.matriz_participantes")
    from tela.renderizador import (
        _larguras_mapa_fisico_matricial,
        _participantes_distribuicao_matricial,
        DESCONTO_ESTRUTURAL_CONSOLE,
    )

    item_longo = "palavra " * 60
    console = ElementoCorpo(
        id="console_ph07_coerencia", tipo="console",
        _campos_inertes={
            "titulo": "PH07COER",
            "itens": [{"id": "i1", "texto": item_longo, "navegavel": True}],
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "unica",
        },
        distribuicao_matricial={
            "formacao": {"politica": "preferencia_colunas",
                         "colunas": {"minimo": 1, "maximo": 1}},
            "ordem": "por_linha",
            "dimensionamento": {"colunas": {"politica": "uniforme"},
                                 "linhas": {"politica": "uniforme"}},
            "espacamento": {
                "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
                "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
                "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
            },
            "distribuicao_horizontal": {"politica": "inicio"},
            "distribuicao_vertical": {"politica": "inicio"},
            "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos",
                               "vertical": "uniforme_margens_e_vaos"},
            "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
            "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
        },
    )
    modelo = ModeloTela(
        id="t_ph07_coerencia", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[console]),
        barra_de_menus={"chips": [
            {"id": "e", "tipo": "acao", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )

    original = _rend.calcular_distribuicao
    capturado = {}

    def _espiao(*args, **kwargs):
        resultado = original(*args, **kwargs)
        if not resultado["fallback"]:
            capturado["celulas"] = {
                c["participante"]: c["largura"] for c in resultado["celulas"]
            }
        return resultado

    _rend.calcular_distribuicao = _espiao
    try:
        for largura in (80, 120, 160, 200):
            capturado.clear()
            saida = renderizar_tela(
                modelo, _ESTILO_CURVA, largura=largura, altura=24, verboso=True,
                foco_console=0, cursores={console.id: 0}, lista_foco=[console],
            )
            assert "PH07COER" in saida
            largura_renderer = capturado["celulas"][0]

            area_w = largura - DESCONTO_ESTRUTURAL_CONSOLE
            participantes = _participantes_distribuicao_matricial(console)
            larguras_mapa = _larguras_mapa_fisico_matricial(
                console, area_w, 24 - 2, True, participantes,
            )
            assert larguras_mapa[0] == largura_renderer
    finally:
        _rend.calcular_distribuicao = original


def test_h0045_ph07_distribuicao_matricial_multiplas_celulas_preservada():
    """VM-H0045-R07-001: quando a formacao permite MAIS de uma celula por
    linha (``colunas.maximo`` > 1), o calculo historico (teto de metade da
    area util, por celula) permanece intacto -- a correcao deste patch e
    restrita a celula unica por linha; distribuicoes com multiplas celulas
    nao sao alteradas."""
    from tela.renderizador import (
        _larguras_mapa_fisico_matricial,
        _participantes_distribuicao_matricial,
        _largura_indicador_do_elemento,
        DESCONTO_ESTRUTURAL_CONSOLE,
    )

    item_a = "alfa " * 40
    item_b = "beta " * 40
    console = ElementoCorpo(
        id="console_ph07_multi", tipo="console",
        _campos_inertes={
            "titulo": "PH07MULTI",
            "itens": [
                {"id": "a", "texto": item_a, "navegavel": True},
                {"id": "b", "texto": item_b, "navegavel": True},
            ],
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "unica",
        },
        distribuicao_matricial={
            "formacao": {"politica": "preferencia_colunas",
                         "colunas": {"minimo": 1, "maximo": 2}},
            "ordem": "por_linha",
            "dimensionamento": {"colunas": {"politica": "uniforme"},
                                 "linhas": {"politica": "uniforme"}},
            "espacamento": {
                "margem_esquerda": {"minimo": 1}, "margem_direita": {"minimo": 1},
                "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
                "vao_horizontal": {"minimo": 1}, "vao_vertical": {"minimo": 0},
            },
            "distribuicao_horizontal": {"politica": "inicio"},
            "distribuicao_vertical": {"politica": "inicio"},
            "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos",
                               "vertical": "uniforme_margens_e_vaos"},
            "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
            "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
        },
    )
    modelo = ModeloTela(
        id="t_ph07_multi", schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "D", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=[console]),
        barra_de_menus={"chips": [
            {"id": "e", "tipo": "acao", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )

    for largura in (80, 120):
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=largura, altura=24, verboso=True,
            foco_console=0, cursores={console.id: 0}, lista_foco=[console],
        )
        assert "PH07MULTI" in saida
        area_w = largura - DESCONTO_ESTRUTURAL_CONSOLE
        participantes = _participantes_distribuicao_matricial(console)
        larguras_mapa = _larguras_mapa_fisico_matricial(
            console, area_w, 24 - 2, True, participantes,
        )
        ind_w = _largura_indicador_do_elemento(console)
        teto_historico = max(10, (area_w - ind_w) // 2) + ind_w
        assert larguras_mapa == {0: teto_historico, 1: teto_historico}
        # nao e a largura util integral (prova de que a celula unica NAO se
        # aplica aqui -- preservacao, nao regressao do teto).
        assert teto_historico < area_w - 2


def test_h0045_ph07_regressao_h0037_console_externo():
    """VM-H0045-R07-001: a correcao do ramo matricial verboso de itens
    internos (``_linhas_distribuicao_matricial``/``_larguras_mapa_fisico_
    matricial``) nao afeta o caminho externo H-0037 (``conteudo_externo``
    hierarquico/tabela/conjuntos), que fica fora do ramo ``quebrar`` (guarda
    ``conteudo_externo is None``) e usa fronteira de renderizacao propria.
    Reexecuta a cobertura ja aprovada VERB-01..VERB-13 dentro do gate pytest
    (a funcao original so roda via ``__main__``, fora da colecao padrao)."""
    _teste_h0037_qapp7_verb_sem_corte_silencioso()


def test_h0045_ph07_cinco_telas_validacao():
    """VM-H0045-R07-001 (secao 20.5 do handoff): as cinco telas de validacao
    exigidas usam a largura util integral (celula unica), sem overflow, com
    o indicador de pagina coerente com o total corrente, em duas larguras
    (80 e 160 colunas)."""
    from tela.renderizador import (
        _larguras_mapa_fisico_matricial,
        _participantes_distribuicao_matricial,
        DESCONTO_ESTRUTURAL_CONSOLE,
        geometria_console,
    )
    from tela import navegacao, paginacao

    nomes = (
        "h0045_validacao_continuacao",
        "h0045_validacao_fluxo_continuo",
        "h0045_validacao_nova_pagina",
        "h0045_validacao_manter_junto",
        "h0045_paginacao_modo_verboso_multilinha",
    )
    altura = 24
    for nome in nomes:
        modelo = construir_modelo(carregar_tela(None, nome, _RAIZ_TELAS_DEMO))
        console = modelo.corpo.elementos[0]
        lista_foco = navegacao.lista_foco(modelo)
        participantes = _participantes_distribuicao_matricial(console)
        marg_e, marg_d = _margens_estruturais_ph07(console)

        for largura in (80, 160):
            geo = geometria_console(
                modelo, _ESTILO_CURVA, largura, altura, False,
                console=console, lista_foco=lista_foco,
            )
            saida = renderizar_tela(
                modelo, _ESTILO_CURVA, largura=largura, altura=altura,
                verboso=True, foco_console=0, cursores={console.id: 0},
                lista_foco=[console], paginas_atuais={console.id: 1},
            )
            caixa, largura_total = _caixa_console_paginado_ph07(saida)
            assert caixa is not None, (nome, largura)

            # ausencia de overflow.
            assert largura_total == largura
            assert all(len(l) == largura for l in caixa)

            area_w = largura - DESCONTO_ESTRUTURAL_CONSOLE
            larguras_mapa = _larguras_mapa_fisico_matricial(
                console, area_w, geo["altura_interna"], True, participantes,
            )
            largura_util_esperada = area_w - marg_e - marg_d
            assert larguras_mapa and all(
                w == largura_util_esperada for w in larguras_mapa.values()
            ), (nome, largura, larguras_mapa, largura_util_esperada)

            plano = paginacao.plano_de_paginacao(
                console, largura, geo["altura_interna"], True,
                desconto_estrutural=DESCONTO_ESTRUTURAL_CONSOLE,
            )
            borda_inferior = caixa[-1]
            assert (
                "página 1/{0}".format(plano["total_paginas"])
                in borda_inferior
            ), (nome, largura, borda_inferior)
