from pathlib import Path

import pytest

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



__all__ = [
    'teste_renderizador_orquestrador',
    'teste_renderizador_destino_minimo',
    'teste_renderizador_grupo_minimo',
    'teste_modelo_fabricado',
    'teste_erros_renderizador',
    'teste_proibicoes_importacao',
    'teste_inspecao_fonte_hardcoded',
    'teste_inercia',
    'teste_alternancia_borda',
    'teste_largura_explicita',
    'teste_altura_explicita',
]


def _cabecalho_h0049(titulo, descricao, **sobreposicoes):
    cabecalho = {
        "titulo": titulo,
        "descricao": descricao,
        "apresentacao": {
            "titulo": {
                "posicao": "esquerda",
                "recuo_lateral": 0,
                "capitalizacao": "maiusculas",
                "formato_na_borda": "com_espacos_laterais",
            },
            "descricao": {
                "max_caracteres": 200,
                "alinhamento": "esquerda",
                "recuo": 1,
                "capitalizacao": "preservar",
            },
        },
    }
    for caminho, valor in sobreposicoes.items():
        alvo = cabecalho
        partes = caminho.split(".")
        for parte in partes[:-1]:
            alvo = alvo[parte]
        alvo[partes[-1]] = valor
    return cabecalho


def _modelo_h0049(titulo="titulo", descricao="descricao", **sobreposicoes):
    return ModeloTela(
        id="h0049_renderer",
        schema="tela.v1",
        cabecalho=_cabecalho_h0049(titulo, descricao, **sobreposicoes),
        corpo=Corpo(
            arranjo="vertical",
            elementos=[ElementoCorpo(id="console", tipo="console")],
        ),
        barra_de_menus={"chips": []},
        _raw={},
    )


def teste_renderizador_orquestrador():
    print("")
    print("== Renderer sobre modelo de config/telas/demo/demo.json ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return

    try:
        saida = renderizar_tela(modelo, _ESTILO_CURVA)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela aceita ModeloTela valido sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
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
        "saida NAO contem '[PgUp][PgDn] Paginas' (chip removido do Orquestrador)",
        "[PgUp][PgDn] Páginas" not in saida,
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

    saida2 = renderizar_tela(modelo, _ESTILO_CURVA)
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


def teste_renderizador_destino_minimo():
    print("")
    print("== Renderer sobre modelo de config/telas/demo/destino_minimo.json (H-0010A) ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "destino_minimo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo (destino_minimo)",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "pipeline carregar_tela + construir_modelo (destino_minimo)",
        True,
    )

    try:
        saida = renderizar_tela(modelo, _ESTILO_CURVA)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(destino_minimo, _ESTILO_CURVA) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar("renderizar_tela(destino_minimo, _ESTILO_CURVA) sem excecao", True)

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


def teste_renderizador_grupo_minimo():
    print("")
    print("== Renderer sobre modelo de config/telas/demo/grupo_minimo.json (H-0012) ==")
    try:
        tela_raw = carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(tela_raw)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "pipeline carregar_tela + construir_modelo (grupo_minimo)",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "pipeline carregar_tela + construir_modelo (grupo_minimo)",
        True,
    )

    try:
        saida = renderizar_tela(modelo, _ESTILO_CURVA)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(grupo_minimo, _ESTILO_CURVA) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar("renderizar_tela(grupo_minimo, _ESTILO_CURVA) sem excecao", True)

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
    saida_plano = renderizar_tela(modelo_plano, _ESTILO_CURVA)
    _registrar(
        "saida do grupo == saida da lista plana equivalente (CA-23)",
        saida == saida_plano,
    )

    # CA-24 reforco: Orquestrador (lista plana) segue inalterado
    tela_o = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    modelo_o = construir_modelo(tela_o)
    saida_o = renderizar_tela(modelo_o, _ESTILO_CURVA)
    _registrar(
        "demo (lista plana) permanece inalterado (CA-24)",
        saida_o == _EXPECTED_ORQUESTRADOR,
    )


def teste_modelo_fabricado():
    print("")
    print("== Modelo fabricado: renderer usa dados do modelo, nao do JSON ==")

    modelo_fab = ModeloTela(
        id="teste_fabricado",
        schema="tela.v0",
        cabecalho=_cabecalho_h0049("Fab", "desc fab"),
        corpo=Corpo(
            arranjo="linear",
            elementos=[ElementoCorpo(id="e1", tipo="console")],
        ),
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )

    saida_fab = renderizar_tela(modelo_fab, _ESTILO_CURVA)

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
        "renderizar_tela(None, _ESTILO_CURVA) lanca RenderizadorErro",
        lambda: renderizar_tela(None, _ESTILO_CURVA),
        RenderizadorErro,
    )
    _espera_excecao(
        "renderizar_tela(<dict>, _ESTILO_CURVA) lanca RenderizadorErro",
        lambda: renderizar_tela({"id": "x"}, _ESTILO_CURVA),
        RenderizadorErro,
    )

    print("")
    print("-- Rejeicao de item de lancador com texto > 15 chars (H-0010A) --")

    modelo_item_longo = ModeloTela(
        id="x",
        schema="tela.v1",
        cabecalho=_cabecalho_h0049("X", "D"),
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
                    parametros_tipo={
                        "vaos": {
                            "chip_texto": {"minimo": 1, "maximo": 3},
                            "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                        },
                        "vertical": {
                            "margem_borda_superior": 1,
                            "margem_borda_inferior": 1,
                        },
                        "verificacao": {"texto": {"max_caracteres": 15}},
                    },
                )
            ],
        ),
        barra_de_menus={"chips": []},
        _raw={},
    )
    exc_item = _espera_excecao(
        "item com texto de 16 chars levanta RenderizadorErro (sem truncamento)",
        lambda: renderizar_tela(modelo_item_longo, _ESTILO_CURVA),
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
        cabecalho=_cabecalho_h0049("Y", "D"),
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
                    parametros_tipo=_PARAMS_LANCADOR_DEMO,
                )
            ],
        ),
        barra_de_menus={"chips": []},
        _raw={},
    )
    try:
        saida_limite = renderizar_tela(modelo_item_limite, _ESTILO_CURVA)
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
        "_campos_inertes" in (
            (_BASE_PADRAO / "tela" / "renderizacao" / "contexto_execucao.py")
            .read_text(encoding="utf-8")
        ),
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
        "_campos_inertes" in (
            (_BASE_PADRAO / "tela" / "renderizacao" / "matriz_participantes.py")
            .read_text(encoding="utf-8")
        ),
    )
    _registrar(
        "renderer fonte contem 'barra_de_menus' (leitura declarativa)",
        "barra_de_menus" in (
            (_BASE_PADRAO / "tela" / "renderizacao" / "barra_menus.py")
            .read_text(encoding="utf-8")
        ),
    )


def teste_inercia():
    print("")
    print("== Inercia: renderer nao executa/resolve/ativa ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    modelo = construir_modelo(tela_raw)
    raw_antes = dict(modelo._raw)
    cabecalho_antes = dict(modelo.cabecalho)
    elementos_antes = [(e.id, e.tipo) for e in modelo.corpo.elementos]
    chips_antes = list(modelo.barra_de_menus.get("chips", []))

    saida = renderizar_tela(modelo, _ESTILO_CURVA)

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
    print("== Consumo do EstiloResolvido pelo renderer (H-0039 / ADR-0030) ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    modelo = construir_modelo(tela_raw)

    try:
        saida_curva_explicita = renderizar_tela(modelo, estilo=_ESTILO_CURVA)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(modelo, estilo=_ESTILO_CURVA) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "renderizar_tela(modelo, estilo=_ESTILO_CURVA) sem excecao",
        True,
    )

    saida_default = renderizar_tela(modelo, _ESTILO_CURVA)
    _registrar(
        "renderizar_tela(modelo, _ESTILO_CURVA) e estavel entre chamadas",
        saida_curva_explicita == saida_default,
    )

    try:
        saida_reta = renderizar_tela(modelo, estilo=_ESTILO_RETA)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "renderizar_tela(modelo, estilo=_ESTILO_RETA) sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return
    _registrar(
        "renderizar_tela(modelo, estilo=_ESTILO_RETA) sem excecao",
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
        "trocar estilo altera somente os quatro cantos",
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

    # H-0039 CA-R2/R3: ``tipo_borda`` foi removido da assinatura; passar o
    # argumento removido levanta TypeError (sem compatibilidade permanente).
    _espera_excecao(
        "renderizar_tela(modelo, estilo, tipo_borda=...) levanta TypeError "
        "(argumento removido)",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, tipo_borda="invalida"),
        TypeError,
    )
    _espera_excecao(
        "renderizar_tela(modelo, estilo, tipo_borda='CURVA') levanta TypeError",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, tipo_borda="CURVA"),
        TypeError,
    )

    _registrar(
        "saida reta e deterministica (duas chamadas identicas)",
        renderizar_tela(modelo, _ESTILO_RETA) == renderizar_tela(modelo, _ESTILO_RETA),
    )

    # H-0039 CA-R1: ``_BORDAS`` foi removido do renderer.
    import tela.renderizador as _mod_rend
    _registrar(
        "renderer nao possui atributo _BORDAS (CA-R1)",
        not hasattr(_mod_rend, "_BORDAS"),
    )

    # H-0039 CA-R6: borda deriva do EstiloResolvido. Substituir o canto
    # superior esquerdo por um valor alternativo altera a saida.
    estilo_alt = EstiloResolvido(
        canto_superior_esquerdo="X",
        canto_superior_direito=_ESTILO_CURVA.canto_superior_direito,
        canto_inferior_esquerdo=_ESTILO_CURVA.canto_inferior_esquerdo,
        canto_inferior_direito=_ESTILO_CURVA.canto_inferior_direito,
        traco_superior=_ESTILO_CURVA.traco_superior,
        traco_inferior=_ESTILO_CURVA.traco_inferior,
        lateral=_ESTILO_CURVA.lateral,
        caractere_esquerdo=_ESTILO_CURVA.caractere_esquerdo,
        caractere_direito=_ESTILO_CURVA.caractere_direito,
        cor_texto=_ESTILO_CURVA.cor_texto,
        caixa_alta=_ESTILO_CURVA.caixa_alta,
        cor_fundo=_ESTILO_CURVA.cor_fundo,
        concluido_on=_ESTILO_CURVA.concluido_on,
        concluido_off=_ESTILO_CURVA.concluido_off,
        selecionado_simbolo=_ESTILO_CURVA.selecionado_simbolo,
        selecionado_off=_ESTILO_CURVA.selecionado_off,
        incluido_on=_ESTILO_CURVA.incluido_on,
        incluido_off=_ESTILO_CURVA.incluido_off,
    )
    saida_alt = renderizar_tela(modelo, estilo_alt)
    _registrar(
        "borda deriva do EstiloResolvido (canto_alt -> saida diferente)",
        saida_alt != saida_curva_explicita and "X" in saida_alt,
    )

    # H-0039 CA-R7: delimitador de chip deriva do estilo.
    estilo_chip_alt = EstiloResolvido(
        canto_superior_esquerdo=_ESTILO_CURVA.canto_superior_esquerdo,
        canto_superior_direito=_ESTILO_CURVA.canto_superior_direito,
        canto_inferior_esquerdo=_ESTILO_CURVA.canto_inferior_esquerdo,
        canto_inferior_direito=_ESTILO_CURVA.canto_inferior_direito,
        traco_superior=_ESTILO_CURVA.traco_superior,
        traco_inferior=_ESTILO_CURVA.traco_inferior,
        lateral=_ESTILO_CURVA.lateral,
        caractere_esquerdo="<",
        caractere_direito=">",
        cor_texto=_ESTILO_CURVA.cor_texto,
        caixa_alta=_ESTILO_CURVA.caixa_alta,
        cor_fundo=_ESTILO_CURVA.cor_fundo,
        concluido_on=_ESTILO_CURVA.concluido_on,
        concluido_off=_ESTILO_CURVA.concluido_off,
        selecionado_simbolo=_ESTILO_CURVA.selecionado_simbolo,
        selecionado_off=_ESTILO_CURVA.selecionado_off,
        incluido_on=_ESTILO_CURVA.incluido_on,
        incluido_off=_ESTILO_CURVA.incluido_off,
    )
    saida_chip_alt = renderizar_tela(modelo, estilo_chip_alt)
    _registrar(
        "delimitador de chip deriva do estilo (< > -> [Esc] vira <Esc>)",
        "<Esc>" in saida_chip_alt and "[Esc]" not in saida_chip_alt,
    )

    # H-0039 CA-R8: caixa_alta=False preserva capitalizacao declarada.
    _registrar(
        "caixa_alta=False preserva 'Sair' (sem forcar maiusculas)",
        "Sair" in saida_curva_explicita and "SAIR" not in saida_curva_explicita,
    )

    # H-0039 CA-R9: caixa_alta=True aplica .upper() ao rotulo (tecla Esc fica).
    saida_caixa_alta = renderizar_tela(modelo, estilo=_ESTILO_CAIXA_ALTA)
    _registrar(
        "caixa_alta=True aplica maiusculas ao rotulo ('Sair' -> 'SAIR')",
        "SAIR" in saida_caixa_alta,
    )
    _registrar(
        "caixa_alta=True preserva a tecla 'Esc' (nao aplica upper na tecla)",
        "[Esc]" in saida_caixa_alta,
    )

    # H-0039 CA-R10/R11: renderer nao abre config/estilo.json nem escolhe
    # preset. A proibicao de importar tela.loader (e assim chamar
    # carregar_estilo) e coberta por teste_proibicoes_importacao; aqui
    # confirma-se que o renderer nao invoca o loader de estilo.
    caminho_mod = _BASE_PADRAO / "tela" / "renderizador.py"
    texto_mod = caminho_mod.read_text(encoding="utf-8")
    _registrar(
        "renderer nao invoca carregar_estilo (CA-R10/R11)",
        "carregar_estilo(" not in texto_mod,
    )

    # H-0039: cor_texto e cor_fundo do EstiloResolvido sao consultados
    # materialmente no caminho de renderizacao (_texto_chip_barra).
    _registrar(
        "renderer acessa estilo.cor_texto no caminho de renderizacao",
        "estilo.cor_texto" in (
            (_BASE_PADRAO / "tela" / "renderizacao" / "barra_menus.py")
            .read_text(encoding="utf-8")
        ),
    )
    _registrar(
        "renderer acessa estilo.cor_fundo no caminho de renderizacao",
        "estilo.cor_fundo" in (
            (_BASE_PADRAO / "tela" / "renderizacao" / "barra_menus.py")
            .read_text(encoding="utf-8")
        ),
    )


def teste_largura_explicita():
    print("")
    print("== Largura explicita (H-0009) ==")

    tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    modelo = construir_modelo(tela_raw)

    saida_42 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
    bate_42 = saida_42 == _EXPECTED_ORQUESTRADOR
    _registrar(
        "renderizar_tela(modelo, _ESTILO_CURVA, largura=42) == _EXPECTED_ORQUESTRADOR "
        "(fallback equivalente)",
        bate_42,
        "" if bate_42 else "ver diff abaixo",
    )
    if not bate_42:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR))
        print("--- obtido (repr) ---")
        print(repr(saida_42))

    saida_42_reta = renderizar_tela(modelo, largura=42, estilo=_ESTILO_RETA)
    bate_42_reta = saida_42_reta == _EXPECTED_ORQUESTRADOR_RETA
    _registrar(
        "renderizar_tela(modelo, largura=42, estilo=_ESTILO_RETA) == "
        "_EXPECTED_ORQUESTRADOR_RETA",
        bate_42_reta,
        "" if bate_42_reta else "ver diff abaixo",
    )
    if not bate_42_reta:
        print("--- esperado (repr) ---")
        print(repr(_EXPECTED_ORQUESTRADOR_RETA))
        print("--- obtido (repr) ---")
        print(repr(saida_42_reta))

    saida_60 = renderizar_tela(modelo, _ESTILO_CURVA, largura=60)
    _registrar(
        "renderizar_tela(modelo, _ESTILO_CURVA, largura=60) retorna str",
        isinstance(saida_60, str),
        "tipo={0}".format(type(saida_60).__name__),
    )

    linhas_60_ok = all(
        len(ln) == 60 for ln in saida_60.split("\n") if ln != ""
    )
    _registrar(
        "cada linha nao-vazia de renderizar_tela(modelo, _ESTILO_CURVA, largura=60) tem 60 chars",
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
        "renderizar_tela(modelo, _ESTILO_CURVA) == renderizar_tela(modelo, _ESTILO_CURVA, largura=None)",
        renderizar_tela(modelo, _ESTILO_CURVA) == renderizar_tela(modelo, _ESTILO_CURVA, largura=None),
    )


def teste_altura_explicita():
    print("")
    print("== Altura explicita (H-0015 / ADR-0013 - ocupacao vertical) ==")

    # H-0025: usa modelo demo SEM distribuicao para preservar a
    # cobertura H-0015 de preenchimento externo (telas sem distribuicao nao
    # sofrem alteracao de comportamento — ADR-0018 D2). A tela demo
    # agora declara distribuicao, que redireciona a sobra para preenchimento
    # interno; a cobertura desse novo comportamento esta em
    # TestDistribuicaoVerticalH0025.
    modelo = _modelo_orquestrador_sem_distribuicao()

    # Contabilidade verificada contra o demo.json (largura=42).
    # H-0016: a barra_de_menus agora e horizontal responsiva. Com 2 chips em
    # largura 42 (content_w=39), "[Esc] Sair" + "  " + "[?] Ajuda" = 21 <= 39,
    # logo cabem em linha unica -> N_linhas_barra = 1.
    # H-0037: o lancador_principal tem agora 11 itens (d,g,1..9).
    # H-0034: o lancador e distribuido em matriz (n_rows=6, n_col=2) em
    # largura 42 (content_w=39; fila exige >39) e adiciona margens verticais
    # canonicas (1 branco topo + 1 branco base dentro da caixa). A caixa
    # NAVEGAR tem 10 linhas (topo + 1 branco topo + 6 linhas matriz + 1 branco
    # base + base).
    #   L_cab = 3 (1 topo + 1 descricao + 1 base)
    #   L_corpo_conteudo = 15 (ITENS=3, INFO=2, NAVEGAR=10)
    #   L_barra = 3 (1 topo + 1 linha horizontal + 1 base)
    #   altura natural (sem preenchimento) = 3 + 15 + 3 = 21
    l_cab = 3
    l_corpo_conteudo = 15
    l_barra = 3
    n_minimo = l_cab + l_corpo_conteudo + l_barra  # 21

    # CA-09 / CA-10: altura=None preserva o comportamento atual.
    _registrar(
        "renderizar_tela(modelo, _ESTILO_CURVA, largura=42) == "
        "renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=None)",
        renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        == renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=None),
    )

    # CA-03: altura exatamente minima -> sem preenchimento (L_corpo_fill == 0),
    # saida identica ao comportamento natural.
    saida_min = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=n_minimo)
    _registrar(
        "altura=N_minimo (21) -> count('\\n') == 21 (sem fill) (CA-03)",
        saida_min.count("\n") == n_minimo,
        "count={0}".format(saida_min.count("\n")),
    )
    _registrar(
        "altura=N_minimo (21) gera saida identica a altura=None",
        saida_min == renderizar_tela(modelo, _ESTILO_CURVA, largura=42),
    )

    # ADR-0024 DA-02: 3 visuais sem distribuicao + area residual e invalido.
    # CA-01 e CA-02 tornados invalidos: o modelo sem distribuicao com 3 elementos
    # visuais levanta RenderizadorErro quando l_fill > 0 (area nao coberta).
    _espera_excecao(
        "ADR-0024 DA-02: altura=23 (3 visuais sem dist, l_fill=2) -> RenderizadorErro",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=23),
        RenderizadorErro,
    )
    _espera_excecao(
        "ADR-0024 DA-02: altura=26 (3 visuais sem dist, l_fill=5) -> RenderizadorErro",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=26),
        RenderizadorErro,
    )

    # CA-06 / CA-07: com altura=n_minimo (sem area residual), cabecalho e barra
    # continuam corretos (verificados sobre saida_min ja computada).
    _registrar(
        "cabecalho no topo: primeira linha comeca com '╭ ORQUESTRADOR' (CA-06)",
        saida_min.startswith("╭ ORQUESTRADOR"),
    )
    ultima_nao_vazia = [ln for ln in saida_min.split("\n") if ln != ""][-1]
    _registrar(
        "barra_de_menus no rodape: ultima linha nao-vazia termina com '╯' (CA-07)",
        ultima_nao_vazia.endswith("╯"),
        "ultima={0!r}".format(ultima_nao_vazia),
    )

    # ADR-0024 DA-02 em outras larguras e bordas com 3 visuais sem dist.
    _espera_excecao(
        "ADR-0024 DA-02: largura=60 altura=24 (3 visuais sem dist) -> RenderizadorErro",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=60, altura=24),
        RenderizadorErro,
    )
    _espera_excecao(
        "ADR-0024 DA-02: borda_reta altura=26 (3 visuais sem dist) -> RenderizadorErro",
        lambda: renderizar_tela(modelo, largura=42, altura=26, estilo=_ESTILO_RETA),
        RenderizadorErro,
    )

    # CA-12: altura insuficiente para o corpo (overflow) -> RenderizadorErro.
    # N_overflow = L_cab + L_barra + L_corpo_conteudo - 1 = 20 (H-0037).
    n_overflow = l_cab + l_barra + l_corpo_conteudo - 1
    exc_overflow = _espera_excecao(
        "altura=20 (corpo overflow) levanta RenderizadorErro (CA-12)",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=n_overflow),
        RenderizadorErro,
    )
    if exc_overflow is not None:
        _registrar(
            "mensagem de overflow menciona corpo/area disponivel (CA-13)",
            "corpo" in str(exc_overflow) and "20" in str(exc_overflow),
            str(exc_overflow),
        )

    # CA-11: altura insuficiente para cabecalho + barra -> RenderizadorErro.
    # Para o Orquestrador (H-0016): L_cab(3) + L_barra(3) = 6 > 5.
    exc_pequeno = _espera_excecao(
        "altura=5 (cabecalho + barra > altura) levanta RenderizadorErro (CA-11)",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=5),
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
    # quando L_corpo_conteudo(15) > 0 e L_corpo_disponivel = 0.
    _espera_excecao(
        "altura == L_cab + L_barra (6) com corpo nao vazio levanta "
        "RenderizadorErro (sem truncamento silencioso)",
        lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=6),
        RenderizadorErro,
    )

    # Determinismo: duas chamadas identicas com altura=n_minimo (sem area residual)
    # produzem saidas identicas.
    _registrar(
        "altura explicita e deterministica (duas chamadas identicas)",
        renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=n_minimo)
        == renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=n_minimo),
    )


def test_h0049_renderer_consumes_apresentacao_local():
    esquerda = _modelo_h0049(
        "titulo",
        "descricao",
        **{
            "apresentacao.titulo.posicao": "esquerda",
            "apresentacao.titulo.recuo_lateral": 0,
        },
    )
    centro = _modelo_h0049(
        "titulo",
        "descricao",
        **{
            "apresentacao.titulo.posicao": "centro",
            "apresentacao.titulo.recuo_lateral": 99,
        },
    )
    direita = _modelo_h0049(
        "titulo",
        "descricao",
        **{
            "apresentacao.titulo.posicao": "direita",
            "apresentacao.titulo.recuo_lateral": 2,
        },
    )
    linhas = [
        renderizar_tela(modelo, _ESTILO_CURVA, largura=30).splitlines()[0]
        for modelo in (esquerda, centro, direita)
    ]
    assert len({linha for linha in linhas}) == 3
    assert all(len(linha) == 30 for linha in linhas)
    assert linhas[0].startswith("╭ TITULO ")
    assert " TITULO " in linhas[1]
    assert linhas[2].endswith("──╮")
    assert linhas[0].count(" TITULO ") == 1
    assert linhas[1].count(" TITULO ") == 1
    assert linhas[2].count(" TITULO ") == 1


def test_h0049_renderer_ordem_capitalizacao_truncamento_alinhamento_unicode():
    modelo = _modelo_h0049(
        "ßeta",
        "  ßeta REST. segunda frase.",
        **{
            "apresentacao.titulo.capitalizacao": "inicio_de_frase",
            "apresentacao.descricao.max_caracteres": 6,
            "apresentacao.descricao.capitalizacao": "inicio_de_frase",
            "apresentacao.descricao.alinhamento": "direita",
            "apresentacao.descricao.recuo": 2,
        },
    )
    linhas = renderizar_tela(modelo, _ESTILO_CURVA, largura=30).splitlines()
    assert linhas[0].startswith("╭ SSeta ")
    assert "SSeta" in linhas[1]
    assert "REST" not in linhas[1]
    assert "segunda" not in linhas[1]

    vazio = _modelo_h0049(
        "sem letras",
        "123 --",
        **{
            "apresentacao.titulo.capitalizacao": "inicio_de_frase",
            "apresentacao.descricao.capitalizacao": "inicio_de_frase",
        },
    )
    vazias = renderizar_tela(vazio, _ESTILO_CURVA, largura=30).splitlines()
    assert "123 --" in vazias[1]

    casos_preservar = (
        ("desc fab", "desc fab"),
        ("Desc fab", "Desc fab"),
        ("  execução da API REST", "  execução da API REST"),
        ("123 - execução", "123 - execução"),
        ("ßeta", "ßeta"),
    )
    for entrada, esperado in casos_preservar:
        modelo = _modelo_h0049(
            "t",
            entrada,
            **{"apresentacao.descricao.capitalizacao": "preservar"},
        )
        linha = renderizar_tela(modelo, _ESTILO_CURVA, largura=42).splitlines()[1]
        assert esperado in linha

    vazio = _modelo_h0049(
        "t",
        "",
        **{"apresentacao.descricao.capitalizacao": "preservar"},
    )
    linha_vazia = renderizar_tela(vazio, _ESTILO_CURVA, largura=42).splitlines()[1]
    assert linha_vazia == "│" + (" " * 40) + "│"

    maiusculas = _modelo_h0049(
        "t",
        "desc fab",
        **{"apresentacao.descricao.capitalizacao": "maiusculas"},
    )
    linha_maiusculas = renderizar_tela(
        maiusculas, _ESTILO_CURVA, largura=42
    ).splitlines()[1]
    assert "DESC FAB" in linha_maiusculas
    assert "desc fab" not in linha_maiusculas


def test_h0049_renderer_alinhamentos_recuos_formato_borda_e_borda_global():
    for alinhamento, recuo in (
        ("esquerda", 1),
        ("centro", 20),
        ("direita", 2),
    ):
        modelo = _modelo_h0049(
            "titulo",
            "abc",
            **{
                "apresentacao.descricao.alinhamento": alinhamento,
                "apresentacao.descricao.recuo": recuo,
            },
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=30)
        assert all(len(linha) == 30 for linha in saida.splitlines())
        assert " titulo " not in saida.splitlines()[0]
        assert " TITULO " in saida.splitlines()[0]

    modelo = _modelo_h0049(
        "titulo",
        "texto",
        **{
            "apresentacao.descricao.alinhamento": "centro",
            "apresentacao.descricao.recuo": 99,
            "apresentacao.descricao.capitalizacao": "inicio_de_frase",
        },
    )
    saida_reta = renderizar_tela(modelo, _ESTILO_RETA, largura=30)
    assert saida_reta.startswith("┌ TITULO ")
    assert "Texto" in saida_reta.splitlines()[1]


def test_h0049_renderer_largura_reduzida_e_impossibilidade_geometrica():
    modelo = _modelo_h0049(
        "titulo muito comprido",
        "uma descrição suficientemente longa",
        **{"apresentacao.descricao.max_caracteres": 200},
    )
    saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=14)
    assert all(len(linha) == 14 for linha in saida.splitlines())

    titulo_impossivel = _modelo_h0049(
        "x", "d", **{"apresentacao.titulo.recuo_lateral": 100}
    )
    with pytest.raises(RenderizadorErro):
        renderizar_tela(titulo_impossivel, _ESTILO_CURVA, largura=14)

    descricao_impossivel = _modelo_h0049(
        "x", "d", **{"apresentacao.descricao.recuo": 100}
    )
    with pytest.raises(RenderizadorErro):
        renderizar_tela(descricao_impossivel, _ESTILO_CURVA, largura=14)


def test_h0049_renderer_baseline_e_variacoes_locais_tem_geometrias_coerentes():
    baseline = _modelo_h0049("mesmo titulo", "mesma descricao")
    variante = _modelo_h0049(
        "mesmo titulo",
        "mesma descricao",
        **{
            "apresentacao.titulo.posicao": "direita",
            "apresentacao.titulo.recuo_lateral": 1,
            "apresentacao.descricao.alinhamento": "centro",
            "apresentacao.descricao.recuo": 17,
        },
    )
    saida_baseline = renderizar_tela(baseline, _ESTILO_CURVA, largura=30)
    saida_variante = renderizar_tela(variante, _ESTILO_CURVA, largura=30)
    assert saida_baseline.splitlines()[0] != saida_variante.splitlines()[0]
    assert saida_baseline.splitlines()[1] != saida_variante.splitlines()[1]
    assert len(saida_baseline.splitlines()) == len(saida_variante.splitlines())
    assert all(len(linha) == 30 for linha in saida_baseline.splitlines())
    assert all(len(linha) == 30 for linha in saida_variante.splitlines())
    assert "titulo" not in saida_baseline.splitlines()[0]
    assert "TITULO" in saida_baseline.splitlines()[0]


def test_h0049_renderer_remove_upper_incondicional_do_cabecalho():
    fonte = (_BASE_PADRAO / "tela" / "renderizacao" / "tela.py").read_text(
        encoding="utf-8"
    )
    assert "label_cabecalho = titulo.upper()" not in fonte
    assert "titulo.upper()" not in fonte
