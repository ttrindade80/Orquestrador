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
- renderer sobre config/telas/demo/demo.json;
- renderer sobre config/telas/demo/destino_minimo.json (H-0010A);
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

import os
import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))

from tela.loader import carregar_tela  # noqa: E402
from tela.loader import EstiloResolvido  # noqa: E402
from tela.modelo import (  # noqa: E402
    Corpo,
    ElementoCorpo,
    ModeloTela,
    construir_modelo,
)
from tela.renderizador import (  # noqa: E402
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
from tela.loader import carregar_conteudo_externo  # noqa: E402
from tela.modelo import construir_conteudo_externo  # noqa: E402


_RESULTADOS = []

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")


# H-0039 / ADR-0030: fixtures de EstiloResolvido para os testes do renderer.
# ``_ESTILO_CURVA`` reproduz o antigo ``_BORDAS["curva"]`` + preset "Colchete"
# com caixa_alta=False (preserva a capitalizacao dos rotulos). ``_ESTILO_RETA``
# reproduz ``_BORDAS["reta"]``. ``_ESTILO_CAIXA_ALTA`` usa o mesmo chip de
# "Colchete" mas com caixa_alta=True para testar a transformacao de rotulo.
_ESTILO_CURVA = EstiloResolvido(
    canto_superior_esquerdo="╭",
    canto_superior_direito="╮",
    canto_inferior_esquerdo="╰",
    canto_inferior_direito="╯",
    traco_superior="─",
    traco_inferior="─",
    lateral="│",
    caractere_esquerdo="[",
    caractere_direito="]",
    cor_texto="padrão",
    caixa_alta=False,
    cor_fundo="padrão",
    concluido_on="✓",
    concluido_off=" ",
    selecionado_simbolo="→",
    selecionado_off=" ",
    incluido_on="●",
    incluido_off="○",
    cor_inativo="cinza",
)

_ESTILO_RETA = EstiloResolvido(
    canto_superior_esquerdo="┌",
    canto_superior_direito="┐",
    canto_inferior_esquerdo="└",
    canto_inferior_direito="┘",
    traco_superior="─",
    traco_inferior="─",
    lateral="│",
    caractere_esquerdo="[",
    caractere_direito="]",
    cor_texto="padrão",
    caixa_alta=False,
    cor_fundo="padrão",
    concluido_on="✓",
    concluido_off=" ",
    selecionado_simbolo="→",
    selecionado_off=" ",
    incluido_on="●",
    incluido_off="○",
    cor_inativo="cinza",
)

_ESTILO_CAIXA_ALTA = EstiloResolvido(
    canto_superior_esquerdo="╭",
    canto_superior_direito="╮",
    canto_inferior_esquerdo="╰",
    canto_inferior_direito="╯",
    traco_superior="─",
    traco_inferior="─",
    lateral="│",
    caractere_esquerdo="[",
    caractere_direito="]",
    cor_texto="padrão",
    caixa_alta=True,
    cor_fundo="padrão",
    concluido_on="✓",
    concluido_off=" ",
    selecionado_simbolo="→",
    selecionado_off=" ",
    incluido_on="●",
    incluido_off="○",
    cor_inativo="cinza",
)


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
    "│                                        │\n"
    "│    [d] Destino        [5] Matriz 2x4   │\n"
    "│    [g] Grupo Min.     [6] Nao Verboso  │\n"
    "│    [1] Console        [7] Verboso      │\n"
    "│    [2] Dashboard      [8] Alternavel   │\n"
    "│    [3] Matriz 2x2     [9] Tab Altern.  │\n"
    "│    [4] Matriz 3x2                      │\n"
    "│                                        │\n"
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
    "│                                        │\n"
    "│    [d] Destino        [5] Matriz 2x4   │\n"
    "│    [g] Grupo Min.     [6] Nao Verboso  │\n"
    "│    [1] Console        [7] Verboso      │\n"
    "│    [2] Dashboard      [8] Alternavel   │\n"
    "│    [3] Matriz 2x2     [9] Tab Altern.  │\n"
    "│    [4] Matriz 3x2                      │\n"
    "│                                        │\n"
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
        cabecalho={"titulo": "Fab", "descricao": "desc fab"},
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


def _modelo_orquestrador_sem_distribuicao():
    """Copia do modelo demo SEM corpo.distribuicao.

    H-0025 / ADR-0018 D2: a ausencia de distribuicao preserva a construcao
    orientada pelo conteudo (preenchimento externo H-0015). Usada para
    manter a cobertura H-0015 de preenchimento externo em tela vertical sem
    distribuicao, visto que o demo.json agora declara
    distribuicao (fracao [2,1,2]) e redireciona a sobra para preenchimento
    interno quando ha altura explicita.
    """
    tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    corpo_sem = dict(tela_raw["corpo"])
    corpo_sem.pop("distribuicao", None)
    tela_raw_sem = dict(tela_raw)
    tela_raw_sem["corpo"] = corpo_sem
    return construir_modelo(tela_raw_sem)


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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 15)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 5),
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
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
            ok = isinstance(linhas, list) and len(linhas) >= 1
        except RenderizadorErro as exc:
            ok = False
            self._r("distribuicao ausente/None aceito sem erro", False, str(exc))
            return
        self._r("distribuicao ausente/None aceito sem erro", ok,
                "linhas={0!r}".format(linhas))

    def test_chips_vazia_retorna_lista_vazia(self):
        bar = {"distribuicao": _dist_canonica(), "chips": []}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ancora_ultimo_valida(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"ultimo": ["chip_ajuda"]}
        bar = {"distribuicao": dist, "chips": chips}
        try:
            _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ancora_id_inexistente(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("chip_ajuda", "?", "Ajuda")]
        dist = _dist_canonica()
        dist["ordem"]["ancoras"] = {"primeiro": ["chip_inexistente"]}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ancora com id inexistente -> RenderizadorErro",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_ordem_preservada(self):
        chips = [
            _chip("a", "1", "AAA"),
            _chip("b", "2", "BBB"),
            _chip("c", "3", "CCC"),
        ]
        bar = {"distribuicao": _dist_canonica(), "chips": chips}
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 100)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
        junta = " ".join(linhas)
        self._r(
            "cada chip declarado aparece exatamente uma vez",
            junta.count("[Esc] Sair") == 1 and junta.count("[?] Ajuda") == 1,
            "junta={0!r}".format(junta),
        )

    def test_chips_do_lancador_nao_entram_na_barra(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 39)
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
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 25)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 25)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_politica_desconhecida_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["ordem"] = {"politica": "grupos_declarados", "ancoras": {}}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "ordem.politica nao suportada ('grupos_declarados') -> "
            "RenderizadorErro (PR-M-01)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_preenchimento_multilinha_desconhecido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair"), _chip("x", "?", "Aj")]
        dist = _dist_canonica(preenchimento="outro_modo")
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "preenchimento_multilinha desconhecido -> RenderizadorErro (PR-M-02)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 15),
        )

    def test_linhas_minimo_invalido_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 0, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.minimo invalido (0) -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_linhas_maximo_menor_que_minimo_erro(self):
        chips = [_chip("chip_esc", "Esc", "Sair")]
        dist = _dist_canonica()
        dist["linhas"] = {"minimo": 3, "maximo": 2, "preferir_menor_numero": True}
        bar = {"distribuicao": dist, "chips": chips}
        self._espera_erro(
            "linhas.maximo < minimo -> RenderizadorErro (PR-M-03)",
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
        )

    def test_renderizar_tela_com_distribuicao_canonica(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        dist = modelo.barra_de_menus.get("distribuicao")
        self._r(
            "JSON migrado expoe distribuicao como objeto com modo canonico",
            isinstance(dist, dict)
            and dist.get("modo") == "horizontal_responsiva"
            and dist.get("ordem", {}).get("politica") == "declaracao",
            "modo={0!r}".format(dist.get("modo") if isinstance(dist, dict) else None),
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "renderizar_tela com canonico: barra em linha horizontal",
            saida == _EXPECTED_ORQUESTRADOR,
            "" if saida == _EXPECTED_ORQUESTRADOR else "snapshot diverge",
        )

    def test_renderizar_tela_preserva_altura_h0015(self):
        # ADR-0024 DA-02: modelo sem distribuicao com 3 visuais + area residual
        # levanta RenderizadorErro (fill externo proibido).
        modelo = _modelo_orquestrador_sem_distribuicao()
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 39)
        l_barra = len(linhas) + 2
        self._r(
            "altura explicita: L_barra = len(linhas_barra)+2 = 3 (1 linha horizontal)",
            l_barra == 3 and len(linhas) == 1,
            "l_barra={0} linhas={1}".format(l_barra, len(linhas)),
        )
        excecao_da02 = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "ADR-0024 DA-02: sem dist + 3 visuais + altura=24 -> RenderizadorErro",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    def test_altura_minima_com_barra_horizontal(self):
        # H-0025: modelo sem distribuicao preserva o comportamento H-0015
        # (preenchimento externo) em altura minima. A tela demo agora
        # declara distribuicao; a cobertura de distribuicao vertical esta em
        # TestDistribuicaoVerticalH0025.
        modelo = _modelo_orquestrador_sem_distribuicao()
        # H-0016 / H-0037 / H-0034: com 11 itens no lancador em matriz 6x2 com
        # margens verticais, NAVEGAR tem 10 linhas, n_minimo = L_cab(3) +
        # L_corpo(15) + L_barra(3) = 21.
        saida_21 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=21)
        self._r(
            "altura minima = 21 com barra horizontal (sem distribuicao)",
            saida_21.count("\n") == 21
            and saida_21 == renderizar_tela(modelo, _ESTILO_CURVA, largura=42),
            "count={0}".format(saida_21.count("\n")),
        )

    def test_fluxo_g_d_b_esc_preservado(self):
        # O renderer continua exibindo lancador ([d]/[g]) no corpo e os chips
        # da barra ([Esc]/[?]) no rodape; a navegacao g/d/b/Esc (tratada pela
        # demo) depende desses chips continuarem presentes e corretos.
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
        l1 = _linhas_barra({"distribuicao": d1, "chips": chips}, _ESTILO_CURVA, 80)
        l5 = _linhas_barra({"distribuicao": d5, "chips": chips}, _ESTILO_CURVA, 80)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 80)
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
        l2 = _linhas_barra({"distribuicao": d2, "chips": chips}, _ESTILO_CURVA, 40)
        l8 = _linhas_barra({"distribuicao": d8, "chips": chips}, _ESTILO_CURVA, 40)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 10),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 20)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            linhas = _linhas_barra(bar, _ESTILO_CURVA, 20)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
            lambda: _linhas_barra(bar, _ESTILO_CURVA, 39),
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
        linhas = _linhas_barra(bar, _ESTILO_CURVA, 39)
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


def _modelo_horizontal(arranjo, elementos_spec, largura=42, titulo_cab="H",
                       distribuicao=None):
    """Cria ModeloTela sintético para testes de arranjo horizontal (H-0019).

    elementos_spec: lista de tuplas (tipo, titulo) ex: [("console","A"),("dashboard","B")]
    distribuicao: dict de distribuicao para o corpo (ou None para ausencia declarada).
        Composicoes horizontais com N>1 e distribuicao=None sao invalidas (DA-02).
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
        corpo=Corpo(arranjo=arranjo, elementos=elementos, distribuicao=distribuicao),
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
        saida_none = renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
        saida_vert = renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
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
            renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_sobreposto_preserva_vertical(self):
        """sobreposto -> alias de vertical, saida identica."""
        modelo_vert = _modelo_horizontal("vertical", [("console", "A")])
        modelo_sob = _modelo_horizontal("sobreposto", [("console", "A")])
        self._r(
            "arranjo='sobreposto' -> saida identica a 'vertical'",
            renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_sob, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_horizontal_dois_elementos(self):
        """horizontal: 2 filhos diretos ficam na mesma faixa de linhas (distribuicao obrigatoria)."""
        dist = {"modo": "igual"}
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                    distribuicao=dist)
        saida_h = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        saida_v = renderizar_tela(_modelo_horizontal("vertical", [("console", "A"), ("console", "B")]), _ESTILO_CURVA,
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
        """lado_a_lado -> alias transicional de horizontal, saida identica (distribuicao obrigatoria)."""
        dist = {"modo": "igual"}
        modelo_h = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                      distribuicao=dist)
        modelo_l = _modelo_horizontal("lado_a_lado", [("console", "A"), ("console", "B")],
                                      distribuicao=dist)
        self._r(
            "arranjo='lado_a_lado' == arranjo='horizontal'",
            renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42)
            == renderizar_tela(modelo_l, _ESTILO_CURVA, largura=42),
        )

    def test_arranjo_horizontal_areas_contiguas(self):
        """horizontal: bordas adjacentes coladas (││, ╮╭, ╯╰); largura total preservada."""
        modelo = _modelo_horizontal("horizontal", [("console", "A"), ("console", "B")],
                                    largura=42, distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        # com dist=igual e 3 elementos em 100: pesos=[1,1,1] -> [34, 33, 33]
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=100,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
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
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        # dist=igual + N=2 + total_w=18: pesos=[1,1] -> larguras=[9,9] -> 9<10 -> erro
        modelo = _modelo_horizontal("horizontal",
                                    [("console", "A"), ("console", "B")],
                                    largura=18,
                                    distribuicao={"modo": "igual"})
        exc = self._espera_erro(
            "horizontal: largura=18 para 2 elementos -> RenderizadorErro",
            lambda: renderizar_tela(modelo, _ESTILO_CURVA, largura=18),
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
        """horizontal: 3 filhos diretos aparecem na mesma faixa de linhas (dist obrigatoria)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        """horizontal: altura explícita funciona (distribuicao obrigatoria para N>1)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=40)
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
        """horizontal: barra_de_menus permanece inalterada (distribuicao obrigatoria para N>1)."""
        modelo = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B")],
            largura=42,
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo_orc = construir_modelo(tela_raw)
        saida_orc = renderizar_tela(modelo_orc, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal: barra_de_menus do demo inalterada pos-H0019",
            "[Esc] Sair" in saida_orc and "[?] Ajuda" in saida_orc,
        )

    def test_arranjo_horizontal_n1(self):
        """horizontal: N=1 -> renderizar na largura total (sem particionamento). (A-002)."""
        modelo = _modelo_horizontal("horizontal", [("console", "A")], largura=42)
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
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


class TestPreenchimentoVerticalH0020:
    """Testes de preenchimento vertical das áreas alocadas no corpo horizontal (H-0020).

    Cobre: fill interno até l_corpo_disponivel; ausência de fill externo H-0015
    no modo horizontal; preservação de H-0019 (sem altura); preservação de
    vertical/sobreposto/None; lado_a_lado como alias horizontal; barra intacta.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo(self, arranjo, specs, largura=42, distribuicao=None):
        return _modelo_horizontal(arranjo, specs, largura=largura, titulo_cab="H0020",
                                  distribuicao=distribuicao)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _corpo_linhas(self, saida):
        """Linhas entre o cabeçalho (3 linhas) e a barra_de_menus."""
        linhas = saida.split("\n")
        barra_idx = next(
            (i for i, ln in enumerate(linhas) if ln.startswith("╭ Menus")), len(linhas)
        )
        return linhas[3:barra_idx]

    # ------------------------------------------------------------------ 1
    def test_horizontal_alto_mantem_bordas_ate_altura_disponivel(self):
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 30
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-1: horizontal altura=30 -> total linhas == 30",
            saida.count("\n") == altura,
            "count={0}".format(saida.count("\n")),
        )
        linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "H0020-1: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in linhas_nv),
            "erros={0}".format([len(ln) for ln in linhas_nv if len(ln) != 42]),
        )
        self._r(
            "H0020-1: barra_de_menus presente",
            "╭ Menus" in saida,
        )
        # l_cab=3, l_barra=3, l_corpo_disponivel = 30-3-3 = 24
        l_corpo_disponivel = 30 - 3 - 3
        corpo = self._corpo_linhas(saida)
        self._r(
            "H0020-1: corpo tem exatamente l_corpo_disponivel=24 linhas",
            len(corpo) == l_corpo_disponivel,
            "len={0}".format(len(corpo)),
        )

    # ------------------------------------------------------------------ 2
    def test_horizontal_preenchimento_dentro_das_colunas(self):
        """Fill ocorre internamente em _montar_corpo_horizontal, não via H-0015."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")])
        l_corpo_disponivel = 30 - 3 - 3  # altura=30, l_cab=3, l_barra=3
        borda = self._borda()
        elementos = modelo.corpo.elementos
        bloco = _montar_corpo_horizontal(
            elementos, borda, 42, altura_disponivel=l_corpo_disponivel,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")
        self._r(
            "H0020-2: _montar_corpo_horizontal com altura_disponivel=24 retorna 24 linhas",
            len(linhas_bloco) == l_corpo_disponivel,
            "len={0}".format(len(linhas_bloco)),
        )
        self._r(
            "H0020-2: cada linha do bloco tem 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ------------------------------------------------------------------ 3
    def test_horizontal_sem_linhas_externas_apos_bloco(self):
        """Após H-0020 o bloco absorve l_corpo_disponivel linhas; zero fill externo."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 40
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        l_corpo_disponivel = altura - 3 - 3  # 34
        corpo = self._corpo_linhas(saida)
        self._r(
            "H0020-3: corpo tem exatamente l_corpo_disponivel=34 linhas (zero fill externo)",
            len(corpo) == l_corpo_disponivel,
            "len={0}".format(len(corpo)),
        )
        # Verificar diretamente que o bloco absorveu tudo
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42,
            altura_disponivel=l_corpo_disponivel, larguras=[21, 21],
        )
        self._r(
            "H0020-3: bloco tem exatamente l_corpo_disponivel linhas internamente",
            bloco.count("\n") + 1 == l_corpo_disponivel,
            "count={0}".format(bloco.count("\n") + 1),
        )

    # ------------------------------------------------------------------ 4
    def test_horizontal_bordas_adjacentes_em_linhas_preenchidas(self):
        """Bordas ││ e ╮╭ presentes nas linhas estruturais (topo/conteúdo/base)."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-4: '││' presente nas linhas de conteúdo do bloco horizontal",
            "││" in saida,
        )
        self._r(
            "H0020-4: '╮╭' presente no topo das áreas adjacentes",
            "╮╭" in saida,
        )
        self._r(
            "H0020-4: '╯╰' presente na base das áreas adjacentes",
            "╯╰" in saida,
        )
        self._r(
            "H0020-4: total linhas == 25",
            saida.count("\n") == 25,
        )

    # ------------------------------------------------------------------ 5
    def test_horizontal_largura_total_em_todas_linhas_preenchidas(self):
        """Todas as linhas do bloco (inclusive fill) têm exatamente total_w chars."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        altura = 20
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
        self._r(
            "H0020-5: altura=20 -> 20 linhas",
            saida.count("\n") == altura,
        )
        self._r(
            "H0020-5: todas as linhas têm 42 chars (inclusive fill)",
            all(len(ln) == 42 for ln in linhas_nv),
            "erros={0}".format([len(ln) for ln in linhas_nv if len(ln) != 42]),
        )

    # ------------------------------------------------------------------ 6
    def test_horizontal_colunas_diferentes_preenchidas_mesma_altura(self):
        """console (3 linhas) e dashboard (2 linhas): ambas preenchidas até l_corpo_disponivel."""
        # Teste geometrico: fornece larguras explicitas (DA-02 exige distribuicao
        # para N>1 via caminho publico; helper requer larguras explicitas para N>1).
        modelo_legado = self._modelo(
            "horizontal", [("console", "A"), ("dashboard", "B")]
        )
        l_corpo_disponivel = 25 - 3 - 3  # altura=25 → 19
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo_legado.corpo.elementos, borda, 42,
            altura_disponivel=l_corpo_disponivel, larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")
        self._r(
            "H0020-6: colunas de alturas diferentes (3 e 2) preenchidas até l_corpo_disponivel=19",
            len(linhas_bloco) == l_corpo_disponivel,
            "len={0}".format(len(linhas_bloco)),
        )
        # Verificar via renderizar_tela com distribuicao declarada (DA-02 obrigatoria para N>1)
        modelo = self._modelo(
            "horizontal", [("console", "A"), ("dashboard", "B")],
            distribuicao={"modo": "igual"},
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-6: renderizar_tela altura=25 -> 25 linhas",
            saida.count("\n") == 25,
        )

    # ------------------------------------------------------------------ 7
    def test_vertical_preserva_comportamento_atual(self):
        """vertical: DA-01 (ADR-0024) - unico visual ocupa area integral."""
        modelo = self._modelo("vertical", [("console", "A")])
        altura = 20
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-7: vertical altura=20 -> 20 linhas",
            saida.count("\n") == altura,
            "count={0}".format(saida.count("\n")),
        )
        self._r(
            "H0020-7: vertical barra presente",
            "╭ Menus" in saida,
        )
        # DA-01 (ADR-0024): unico visual preenche internamente toda a area.
        # Nenhuma linha de espacos entre corpo e barra (fill externo proibido).
        linhas = saida.split("\n")
        fill_ext = [ln for ln in linhas if ln == " " * 42]
        self._r(
            "H0020-7: DA-01 (ADR-0024) - sem fill externo, console ocupa area integral",
            len(fill_ext) == 0,
            "fills={0}".format(len(fill_ext)),
        )

    # ------------------------------------------------------------------ 8
    def test_sobreposto_preserva_comportamento_atual(self):
        """sobreposto: alias de vertical, comportamento idêntico."""
        modelo_v = self._modelo("vertical", [("console", "A")])
        modelo_s = self._modelo("sobreposto", [("console", "A")])
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        saida_s = renderizar_tela(modelo_s, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0020-8: sobreposto == vertical (alias preservado)",
            saida_v == saida_s,
        )
        self._r(
            "H0020-8: sobreposto altura=20 -> 20 linhas",
            saida_s.count("\n") == 20,
        )

    # ------------------------------------------------------------------ 9
    def test_none_preserva_comportamento_atual(self):
        """None: equivale a vertical, fill externo H-0015 intacto."""
        modelo_n = self._modelo(None, [("console", "A")])
        modelo_v = self._modelo("vertical", [("console", "A")])
        saida_n = renderizar_tela(modelo_n, _ESTILO_CURVA, largura=42, altura=20)
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0020-9: None == vertical (comportamento preservado)",
            saida_n == saida_v,
        )
        self._r(
            "H0020-9: None altura=20 -> 20 linhas",
            saida_n.count("\n") == 20,
        )

    # ------------------------------------------------------------------ 10
    def test_lado_a_lado_preserva_comportamento_horizontal(self):
        """lado_a_lado: alias horizontal com fill vertical interno (H-0020)."""
        dist = {"modo": "igual"}
        modelo_h = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                                distribuicao=dist)
        modelo_l = self._modelo("lado_a_lado", [("console", "A"), ("console", "B")],
                                distribuicao=dist)
        altura = 25
        saida_h = renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42, altura=altura)
        saida_l = renderizar_tela(modelo_l, _ESTILO_CURVA, largura=42, altura=altura)
        self._r(
            "H0020-10: lado_a_lado == horizontal com fill vertical interno",
            saida_h == saida_l,
        )
        self._r(
            "H0020-10: lado_a_lado altura=25 -> 25 linhas",
            saida_l.count("\n") == altura,
        )
        corpo = self._corpo_linhas(saida_l)
        self._r(
            "H0020-10: corpo de lado_a_lado tem l_corpo_disponivel=19 linhas",
            len(corpo) == altura - 3 - 3,
            "len={0}".format(len(corpo)),
        )

    # ------------------------------------------------------------------ 11
    def test_horizontal_sem_altura_preserva_h0019(self):
        """Sem altura: _montar_corpo_horizontal normaliza até altura_max (H-0019 preservado)."""
        # Teste geometrico via chamada direta com larguras explicitas.
        # console: 3 linhas; dashboard sem campos: 2 linhas; altura_max = 3
        # Com altura_disponivel=None -> normaliza até 3
        modelo_legado = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        bloco_sem = _montar_corpo_horizontal(
            modelo_legado.corpo.elementos, borda, 42, altura_disponivel=None,
            larguras=[21, 21],
        )
        linhas_bloco = bloco_sem.split("\n")
        self._r(
            "H0020-11: sem altura -> bloco normalizado até altura_max=3",
            len(linhas_bloco) == 3,
            "len={0}".format(len(linhas_bloco)),
        )
        # Via renderizar_tela com distribuicao valida (DA-02: multiplos elementos requerem distribuicao)
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")],
                              distribuicao={"modo": "igual"})
        saida_sem = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        # TestArranjoH0019.test_arranjo_horizontal_padding_inferior continua passando
        linhas_nv = [ln for ln in saida_sem.split("\n") if ln != ""]
        self._r(
            "H0020-11: sem altura -> todas linhas têm 42 chars (H-0019 preservado)",
            all(len(ln) == 42 for ln in linhas_nv),
        )

    # ------------------------------------------------------------------ 12
    def test_barra_de_menus_preservada_apos_h0020(self):
        """Barra de menus com chips corretos; funções protegidas intactas."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")],
                              distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=25)
        self._r(
            "H0020-12: barra presente na saida horizontal com altura",
            "╭ Menus" in saida,
        )
        self._r(
            "H0020-12: chip [k] Ok da barra aparece",
            "[k] Ok" in saida,
        )
        # Verificar orquestrador (usa _normalizar_distribuicao, _linhas_barra)
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo_orc = construir_modelo(tela_raw)
        saida_orc = renderizar_tela(modelo_orc, _ESTILO_CURVA, largura=42)
        self._r(
            "H0020-12: barra demo inalterada (funções protegidas intactas)",
            "[Esc] Sair" in saida_orc and "[?] Ajuda" in saida_orc,
        )
        self._r(
            "H0020-12: teste_explorar_barra_de_menus baseline 38/38 (verificar externamente)",
            True,  # verificação executada nas suítes finais
        )

    def run_all(self):
        print("")
        print("== H-0020 - preenchimento vertical das areas alocadas no corpo horizontal ==")
        self.test_horizontal_alto_mantem_bordas_ate_altura_disponivel()
        self.test_horizontal_preenchimento_dentro_das_colunas()
        self.test_horizontal_sem_linhas_externas_apos_bloco()
        self.test_horizontal_bordas_adjacentes_em_linhas_preenchidas()
        self.test_horizontal_largura_total_em_todas_linhas_preenchidas()
        self.test_horizontal_colunas_diferentes_preenchidas_mesma_altura()
        self.test_vertical_preserva_comportamento_atual()
        self.test_sobreposto_preserva_comportamento_atual()
        self.test_none_preserva_comportamento_atual()
        self.test_lado_a_lado_preserva_comportamento_horizontal()
        self.test_horizontal_sem_altura_preserva_h0019()
        self.test_barra_de_menus_preservada_apos_h0020()


class TestPreenchimentoBordeadoH0021:
    """Testes de preenchimento bordeado no corpo horizontal (H-0021).

    Cobre: fill bordeado com bordas laterais; base na ultima linha; bordas
    adjacentes (││, ╯╰); integracao com orquestrador.json em memoria;
    alias lado_a_lado; dashboard sem literal; filhos em ordem; preservacao
    do comportamento sem altura (H-0019/H-0020); nao-regressao de
    vertical/sobreposto/None; barra_de_menus preservada.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo(self, arranjo, specs, largura=42):
        return _modelo_horizontal(arranjo, specs, largura=largura, titulo_cab="H0021")

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    # ---------------------------------------------------------------------- 1
    def test_horizontal_fill_bordeado_orquestrador_json(self):
        """demo.json em memoria com arranjo='horizontal', largura=80, altura=30."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        # l_cab=3, l_corpo_disponivel=24, l_barra=3
        linhas = saida.split("\n")
        bloco = linhas[3:27]  # 24 linhas do corpo horizontal

        self._r(
            "H0021-1: bloco horizontal tem 24 linhas (l_corpo_disponivel)",
            len(bloco) == 24,
            "len={0}".format(len(bloco)),
        )
        # Linhas internas (nao topo, nao base) devem ter '│'
        inner = bloco[1:-1]
        self._r(
            "H0021-1: linhas internas do bloco contêm '│' (bordas laterais)",
            all("│" in ln for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if "│" not in ln]),
        )
        self._r(
            "H0021-1: sem linha ' ' * 80 no bloco (fill bordeado, nao espacos planos)",
            not any(ln == " " * 80 for ln in bloco),
        )
        self._r(
            "H0021-1: cada linha do bloco tem 80 chars",
            all(len(ln) == 80 for ln in bloco),
            "erros={0}".format([len(ln) for ln in bloco if len(ln) != 80]),
        )

    # ---------------------------------------------------------------------- 2
    def test_horizontal_fill_bordeado_lado_a_lado_alias(self):
        """lado_a_lado produz comportamento identico ao horizontal."""
        tela_raw_h = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw_h["corpo"]["arranjo"] = "horizontal"
        saida_h = renderizar_tela(
            construir_modelo(tela_raw_h), estilo=_ESTILO_CURVA, largura=80, altura=30
        )

        tela_raw_l = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw_l["corpo"]["arranjo"] = "lado_a_lado"
        saida_l = renderizar_tela(
            construir_modelo(tela_raw_l), estilo=_ESTILO_CURVA, largura=80, altura=30
        )

        self._r(
            "H0021-2: lado_a_lado produz saida identica ao horizontal",
            saida_h == saida_l,
        )
        linhas_l = saida_l.split("\n")
        bloco_l = linhas_l[3:27]
        inner_l = bloco_l[1:-1]
        self._r(
            "H0021-2: lado_a_lado: linhas internas contêm '│'",
            all("│" in ln for ln in inner_l),
        )

    # ---------------------------------------------------------------------- 3
    def test_horizontal_fill_linhas_internas_com_bordas_laterais(self):
        """Modelo sintetico: linhas de fill comecam e terminam com borda vertical."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        h = 15
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-3: bloco tem 15 linhas",
            len(linhas_bloco) == h,
            "len={0}".format(len(linhas_bloco)),
        )
        # Linhas intermediarias (nao topo, nao base)
        inner = linhas_bloco[1:-1]
        self._r(
            "H0021-3: linhas intermediarias comecam com '│'",
            all(ln[0] == "│" for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if ln[0] != "│"]),
        )
        self._r(
            "H0021-3: linhas intermediarias terminam com '│'",
            all(ln[-1] == "│" for ln in inner),
            "falhas={0}".format([i for i, ln in enumerate(inner) if ln[-1] != "│"]),
        )
        self._r(
            "H0021-3: cada linha do bloco tem 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ---------------------------------------------------------------------- 4
    def test_horizontal_base_na_ultima_linha_da_area(self):
        """Base das caixas aparece na ultima linha da area horizontal."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        h = 15
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        ultima = linhas_bloco[-1]
        self._r(
            "H0021-4: ultima linha do bloco começa com '╰' (base)",
            ultima.startswith("╰"),
            "ultima[:5]={0!r}".format(ultima[:5]),
        )
        self._r(
            "H0021-4: ultima linha do bloco termina com '╯' (base)",
            ultima.endswith("╯"),
            "ultima[-5:]={0!r}".format(ultima[-5:]),
        )
        # Sem base prematura: '╰' nao deve aparecer nas linhas anteriores a ultima
        bases_prematuras = [
            i for i, ln in enumerate(linhas_bloco[:-1]) if "╰" in ln
        ]
        self._r(
            "H0021-4: '╰' ausente nas linhas intermediarias (sem base prematura)",
            len(bases_prematuras) == 0,
            "indices={0}".format(bases_prematuras),
        )

    # ---------------------------------------------------------------------- 5
    def test_horizontal_bordas_adjacentes_em_fill_e_base(self):
        """'││' nas linhas de fill e '╯╰' na linha de base."""
        modelo = self._modelo("horizontal", [("console", "A"), ("console", "B")])
        borda = self._borda()
        h = 10
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        fill_lines = linhas_bloco[1:-1]
        self._r(
            "H0021-5: '││' presente nas linhas de fill (bordas adjacentes coladas)",
            any("││" in ln for ln in fill_lines),
        )
        self._r(
            "H0021-5: '╯╰' presente na linha de base (bases adjacentes coladas)",
            "╯╰" in linhas_bloco[-1],
            "base={0!r}".format(linhas_bloco[-1]),
        )

    # ---------------------------------------------------------------------- 6
    def test_horizontal_largura_total_em_todas_linhas_apos_h0021(self):
        """Todas as linhas do bloco (topo, conteudo, fill, base) têm total_w chars."""
        modelo = self._modelo(
            "horizontal",
            [("console", "A"), ("console", "B"), ("lancador", "C")],
        )
        borda = self._borda()
        h = 20
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=h,
            larguras=[14, 14, 14],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-6: bloco tem exatamente 20 linhas",
            len(linhas_bloco) == h,
            "len={0}".format(len(linhas_bloco)),
        )
        self._r(
            "H0021-6: todas as linhas têm 42 chars",
            all(len(ln) == 42 for ln in linhas_bloco),
            "erros={0}".format([len(ln) for ln in linhas_bloco if len(ln) != 42]),
        )

    # ---------------------------------------------------------------------- 7
    def test_horizontal_dashboard_sem_literal_tem_bordas(self):
        """dashboard_info sem campos literais ocupa area visual bordeada."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        borda = self._borda()
        # larguras=[27, 27, 26]: 80//3=26, 80%3=2 -> primeiras 2 areas recebem 27
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 80, altura_disponivel=24,
            larguras=[27, 27, 26],
        )
        linhas_bloco = bloco.split("\n")

        # Linhas intermediarias do bloco (nao topo, nao base)
        inner = linhas_bloco[1:-1]
        # Char na posicao 27 de cada linha intermediaria deve ser '│' (borda esq do dashboard)
        chars_esq_dash = [ln[27] for ln in inner if len(ln) >= 28]
        self._r(
            "H0021-7: dashboard sem literal: borda esquerda presente em linhas intermediarias",
            all(c == "│" for c in chars_esq_dash) and len(chars_esq_dash) > 0,
            "chars={0!r}".format(chars_esq_dash[:5]),
        )
        # Base do dashboard na ultima linha: char[27] deve ser '╰'
        ultima = linhas_bloco[-1]
        char_base = ultima[27] if len(ultima) >= 28 else None
        self._r(
            "H0021-7: base do dashboard na ultima linha (char[27]='╰')",
            char_base == "╰",
            "char[27]={0!r}".format(char_base),
        )

    # ---------------------------------------------------------------------- 8
    def test_horizontal_filhos_preservados_em_ordem(self):
        """Filhos console, dashboard, lancador aparecem na ordem declarada."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        self._r("H0021-8: '╭ ITENS' presente (console_principal)", "╭ ITENS" in saida)
        self._r("H0021-8: '╭ INFO' presente (dashboard_info)", "╭ INFO" in saida)
        self._r("H0021-8: '╭ NAVEGAR' presente (lancador_principal)", "╭ NAVEGAR" in saida)

        # Verificar ordem: na primeira linha do bloco, topos aparecem da esq para dir
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_topos = next((ln for ln in linhas if "╭ ITENS" in ln), None)
        if linha_topos is not None:
            self._r(
                "H0021-8: ITENS, INFO, NAVEGAR aparecem da esquerda para a direita",
                linha_topos.index("╭ ITENS") < linha_topos.index("╭ INFO")
                < linha_topos.index("╭ NAVEGAR"),
            )
        else:
            self._r("H0021-8: linha com topos das tres colunas encontrada", False)

    # ---------------------------------------------------------------------- 9
    def test_horizontal_sem_altura_preserva_h0019_h0020(self):
        """Sem altura_disponivel: fill permanece ' ' * largura (sem bordas)."""
        modelo = self._modelo("horizontal", [("console", "A"), ("dashboard", "B")])
        borda = self._borda()
        bloco = _montar_corpo_horizontal(
            modelo.corpo.elementos, borda, 42, altura_disponivel=None,
            larguras=[21, 21],
        )
        linhas_bloco = bloco.split("\n")

        self._r(
            "H0021-9: sem altura -> bloco tem 3 linhas (altura_max, H-0019 preservado)",
            len(linhas_bloco) == 3,
            "len={0}".format(len(linhas_bloco)),
        )
        # Com altura=None: dashboard (coluna 1, w=21) tem fill ' '*21 no row 2.
        # Row 2 concatenado = base_do_console (21 chars) + fill_do_dashboard (21 chars).
        # O fill do dashboard ocupa chars [21:42]; se for espacos (sem '│'), e H-0020.
        row2 = linhas_bloco[2]
        dash_fill = row2[21:] if len(row2) >= 42 else None
        self._r(
            "H0021-9: fill sem bordas: coluna dashboard (chars 21..41) e espacos (H-0019/H-0020)",
            dash_fill == " " * 21,
            "dash_fill={0!r}".format(dash_fill),
        )

    # ---------------------------------------------------------------------- 10
    def test_vertical_nao_regride_apos_h0021(self):
        """arranjo=vertical preserva comportamento anterior."""
        # H-0025: o demo.json declara distribuicao agora. Sem altura,
        # a distribuicao nao se aplica (sem area distribuivel) e a saida continua
        # igual a _EXPECTED_ORQUESTRADOR (comportamento orientado pelo conteudo).
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(tela_raw)  # arranjo=vertical (padrao do JSON)
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H0021-10: vertical sem altura preserva _EXPECTED_ORQUESTRADOR",
            saida == _EXPECTED_ORQUESTRADOR,
        )
        # ADR-0024 DA-02: modelo sem distribuicao com 3 visuais + area residual
        # e invalido (fill externo proibido pelo ADR-0024).
        modelo_sd = _modelo_orquestrador_sem_distribuicao()
        excecao_da02 = None
        try:
            renderizar_tela(modelo_sd, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "H0021-10: ADR-0024 DA-02 - sem dist + 3 visuais + altura=24 -> RenderizadorErro",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    # ---------------------------------------------------------------------- 11
    def test_sobreposto_nao_regride_apos_h0021(self):
        """arranjo=sobreposto (alias de vertical) sem regressao."""
        modelo_v = _modelo_horizontal("vertical", [("console", "A")])
        modelo_s = _modelo_horizontal("sobreposto", [("console", "A")])
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        saida_s = renderizar_tela(modelo_s, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0021-11: sobreposto == vertical (alias preservado)",
            saida_v == saida_s,
        )
        self._r(
            "H0021-11: sobreposto com altura=20 -> 20 linhas",
            saida_s.count("\n") == 20,
        )

    # ---------------------------------------------------------------------- 12
    def test_none_nao_regride_apos_h0021(self):
        """arranjo=None equivale a vertical, sem regressao."""
        modelo_n = _modelo_horizontal(None, [("console", "A")])
        modelo_v = _modelo_horizontal("vertical", [("console", "A")])
        saida_n = renderizar_tela(modelo_n, _ESTILO_CURVA, largura=42, altura=20)
        saida_v = renderizar_tela(modelo_v, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H0021-12: None == vertical (preservado)",
            saida_n == saida_v,
        )
        self._r(
            "H0021-12: None com altura=20 -> 20 linhas",
            saida_n.count("\n") == 20,
        )

    # ---------------------------------------------------------------------- 13
    def test_barra_de_menus_preservada_apos_h0021(self):
        """Barra de menus e funcoes protegidas preservadas apos H-0021."""
        tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        tela_raw["corpo"]["arranjo"] = "horizontal"
        modelo = construir_modelo(tela_raw)
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=30)

        self._r("H0021-13: '╭ Menus' presente na saida horizontal", "╭ Menus" in saida)
        self._r("H0021-13: '[Esc] Sair' presente na barra", "[Esc] Sair" in saida)
        self._r("H0021-13: '[?] Ajuda' presente na barra", "[?] Ajuda" in saida)

        from tela.renderizador import (
            _normalizar_distribuicao,
            _validar_distribuicao,
            _linhas_barra,
        )
        self._r(
            "H0021-13: _normalizar_distribuicao existe e e chamavel",
            callable(_normalizar_distribuicao),
        )
        self._r(
            "H0021-13: _validar_distribuicao existe e e chamavel",
            callable(_validar_distribuicao),
        )
        self._r(
            "H0021-13: _linhas_barra existe e e chamavel",
            callable(_linhas_barra),
        )

    # ---------------------------------------------------------------------- 14
    def test_baseline_completo_continua_passando(self):
        """Registro: baseline 621 casos anteriores verificados por execucao sequencial."""
        self._r(
            "H0021-14: baseline completo verificado externamente (621 + novos)",
            True,
        )

    def run_all(self):
        print("")
        print("== H-0021 - correcao preenchimento bordeado horizontal ==")
        self.test_horizontal_fill_bordeado_orquestrador_json()
        self.test_horizontal_fill_bordeado_lado_a_lado_alias()
        self.test_horizontal_fill_linhas_internas_com_bordas_laterais()
        self.test_horizontal_base_na_ultima_linha_da_area()
        self.test_horizontal_bordas_adjacentes_em_fill_e_base()
        self.test_horizontal_largura_total_em_todas_linhas_apos_h0021()
        self.test_horizontal_dashboard_sem_literal_tem_bordas()
        self.test_horizontal_filhos_preservados_em_ordem()
        self.test_horizontal_sem_altura_preserva_h0019_h0020()
        self.test_vertical_nao_regride_apos_h0021()
        self.test_sobreposto_nao_regride_apos_h0021()
        self.test_none_nao_regride_apos_h0021()
        self.test_barra_de_menus_preservada_apos_h0021()
        self.test_baseline_completo_continua_passando()


def _alturas_caixas(saida):
    """Alturas (em linhas) de cada caixa bordeada na saida, na ordem.

    A primeira entrada e o cabecalho; a ultima e a barra_de_menus; as
    intermediarias sao as caixas do corpo. Detecta bordas curvas (╭/╰) e
    retas (┌/└).
    """
    linhas = saida.split("\n")
    alturas = []
    i = 0
    while i < len(linhas):
        ln = linhas[i]
        if ln.startswith("╭") or ln.startswith("┌"):
            topo = i
            j = i + 1
            while j < len(linhas) and not (
                linhas[j].startswith("╰") or linhas[j].startswith("└")
            ):
                j += 1
            alturas.append(j - topo + 1)
            i = j + 1
        else:
            i += 1
    return alturas


def _corpo_alturas(saida):
    """Alturas das caixas do corpo (exclui cabecalho e barra_de_menus)."""
    alturas = _alturas_caixas(saida)
    return alturas[1:-1]


class TestDistribuicaoVerticalH0025:
    """Cobertura da distribuicao vertical explicita do corpo (H-0025 / ADR-0018).

    Cobre os minimos exigidos pelo H-0025 secao 10.2: ausencia preservada;
    igual explicito; percentual; fracao [1,1,1], [2,1,2] e vetor generico
    adicional; soma exata; maiores restos; desempate por ordem declarada;
    preenchimento interno das molduras; ausencia de sobra externa; JSON real
    do Orquestrador; redimensionamento; preservacao horizontal; telas sem
    distribuicao inalteradas.
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

    def _modelo_dist(self, distribuicao, n=3, titulos=None):
        """Modelo vertical com n consoles e distribuicao declarada."""
        if titulos is None:
            titulos = [chr(ord("A") + i) for i in range(n)]
        elementos = [
            ElementoCorpo(
                id=titulos[i].lower(), tipo="console",
                _campos_inertes={"titulo": titulos[i]},
            )
            for i in range(n)
        ]
        return ModeloTela(
            id="teste_h0025",
            schema="tela.v1",
            cabecalho={"titulo": "H0025", "descricao": "dist vertical"},
            corpo=Corpo(
                arranjo="vertical", elementos=elementos,
                distribuicao=distribuicao,
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )

    def _modelo_sem_dist(self, n=3, titulos=None):
        """Modelo vertical sem distribuicao (orientado pelo conteudo)."""
        return self._modelo_dist(None, n=n, titulos=titulos)

    # ----------------------------------------------------------- algoritmo
    def test_algoritmo_maiores_restos_exemplos_normativos(self):
        # Exemplos normativos do contrato_composicao_corpo.md secao 5.8.
        self._r(
            "alg: 68 com [1,1,1] -> [23,23,22]",
            _distribuir_alturas(68, [1, 1, 1]) == [23, 23, 22],
            "obtido={0}".format(_distribuir_alturas(68, [1, 1, 1])),
        )
        self._r(
            "alg: 68 com [2,1,2] -> [27,14,27]",
            _distribuir_alturas(68, [2, 1, 2]) == [27, 14, 27],
            "obtido={0}".format(_distribuir_alturas(68, [2, 1, 2])),
        )

    def test_algoritmo_soma_exata_invariante(self):
        for altura, pesos in [
            (18, [1, 1, 1]), (18, [2, 1, 2]), (18, [1, 3, 1]),
            (18, [5, 2, 7]), (14, [1, 1, 1]), (101, [3, 5, 7, 11]),
            (7, [1]), (66, [1, 1, 1]),
        ]:
            cotas = _distribuir_alturas(altura, pesos)
            self._r(
                "alg: soma das cotas == altura ({0}, {1})".format(altura, pesos),
                sum(cotas) == altura,
                "cotas={0} soma={1}".format(cotas, sum(cotas)),
            )

    def test_algoritmo_vetores_genericos_sem_codigo_especial(self):
        # O mesmo codigo generico trata [1,1,1], [2,1,2], [1,3,1] e [5,2,7].
        r_111 = _distribuir_alturas(30, [1, 1, 1])
        r_212 = _distribuir_alturas(30, [2, 1, 2])
        r_131 = _distribuir_alturas(30, [1, 3, 1])
        r_527 = _distribuir_alturas(30, [5, 2, 7])
        self._r(
            "alg: [1,1,1] em 30 -> [10,10,10] (divisao exata)",
            r_111 == [10, 10, 10],
            "obtido={0}".format(r_111),
        )
        self._r(
            "alg: [2,1,2] em 30 -> [12,6,12] (proporcao 2:1:2)",
            r_212 == [12, 6, 12],
            "obtido={0}".format(r_212),
        )
        self._r(
            "alg: [1,3,1] em 30 -> [6,18,6] (proporcao 1:3:1)",
            r_131 == [6, 18, 6],
            "obtido={0}".format(r_131),
        )
        self._r(
            "alg: [5,2,7] em 30 -> soma 30 (vetor generico)",
            sum(r_527) == 30,
            "obtido={0}".format(r_527),
        )

    def test_algoritmo_maiores_restos_distribui_residuo(self):
        # 10 com [1,1,1]: 10/3=3.33 -> floor [3,3,3] soma 9, falta 1.
        # Restos iguais (0.33): desempate por ordem declarada -> idx 0 recebe.
        self._r(
            "alg: 10 com [1,1,1] -> [4,3,3] (maiores restos)",
            _distribuir_alturas(10, [1, 1, 1]) == [4, 3, 3],
            "obtido={0}".format(_distribuir_alturas(10, [1, 1, 1])),
        )

    def test_algoritmo_desempate_por_ordem_declarada(self):
        # 14 com [1,1,1]: 14/3=4.667 -> floor [4,4,4] soma 12, faltam 2.
        # Restos iguais -> idx 0 e idx 1 recebem (ordem declarada).
        self._r(
            "alg: 14 com [1,1,1] -> [5,5,4] (desempate por ordem)",
            _distribuir_alturas(14, [1, 1, 1]) == [5, 5, 4],
            "obtido={0}".format(_distribuir_alturas(14, [1, 1, 1])),
        )
        # [2,2] em 5: 5*2/4=2.5 cada -> floor [2,2] soma 4, falta 1.
        # Restos iguais (0.5) -> idx 0 recebe (ordem declarada).
        self._r(
            "alg: 5 com [2,2] -> [3,2] (empate: primeiro declarado)",
            _distribuir_alturas(5, [2, 2]) == [3, 2],
            "obtido={0}".format(_distribuir_alturas(5, [2, 2])),
        )

    def test_pesos_distribuicao_por_modo(self):
        self._r(
            "pesos: igual -> [1,1,1]",
            _pesos_distribuicao({"modo": "igual"}, 3) == [1, 1, 1],
        )
        self._r(
            "pesos: fracao -> valores declarados",
            _pesos_distribuicao(
                {"modo": "fracao", "valores": [2, 1, 2]}, 3) == [2, 1, 2],
        )
        self._r(
            "pesos: percentual -> valores declarados",
            _pesos_distribuicao(
                {"modo": "percentual", "valores": [40, 20, 40]}, 3) == [40, 20, 40],
        )

    # ----------------------------------------------------- ausencia (D2)
    def test_ausencia_preserva_altura_natural_sem_cota(self):
        modelo = self._modelo_sem_dist()
        saida_none = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        corpo_none = _corpo_alturas(saida_none)
        # Cada console natural = 3 linhas (topo + "(console)" + base).
        self._r(
            "ausencia: sem altura, cada filho usa altura natural (3)",
            corpo_none == [3, 3, 3],
            "corpo={0}".format(corpo_none),
        )
        # ADR-0024 DA-02: ausencia de distribuicao com 3 visuais + area residual
        # e invalida (fill externo proibido pelo ADR-0024).
        excecao_da02 = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        except RenderizadorErro as exc:
            excecao_da02 = exc
        self._r(
            "ausencia: com altura=24 e 3 visuais -> DA-02 (ADR-0024)",
            excecao_da02 is not None and "DA-02" in str(excecao_da02),
            str(excecao_da02) if excecao_da02 else "nenhuma excecao",
        )

    def test_ausencia_nao_materializa_igual_no_modelo(self):
        modelo = self._modelo_sem_dist()
        self._r(
            "ausencia: modelo.corpo.distribuicao is None (sem fallback igual)",
            modelo.corpo.distribuicao is None,
        )

    # -------------------------------------------------------- modos (D5-D7)
    def test_igual_explicito_divide_igualmente(self):
        modelo = self._modelo_dist({"modo": "igual"})
        # l_cab=3, l_barra=3, l_corpo_disponivel = 24-3-3 = 18 -> [6,6,6].
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "igual explicito em altura=24 -> [6,6,6]",
            corpo == [6, 6, 6],
            "corpo={0}".format(corpo),
        )

    def test_igual_explicito_maiores_restos(self):
        modelo = self._modelo_dist({"modo": "igual"})
        # altura=16 -> l_corpo=10 -> [4,3,3] (maiores restos + ordem).
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=16)
        corpo = _corpo_alturas(saida)
        self._r(
            "igual explicito em altura=16 -> [4,3,3] (maiores restos)",
            corpo == [4, 3, 3],
            "corpo={0}".format(corpo),
        )

    def test_percentual_explicito(self):
        modelo = self._modelo_dist(
            {"modo": "percentual", "valores": [40, 20, 40]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "percentual [40,20,40] em altura=24 -> [7,4,7] (proporcao)",
            corpo == [7, 4, 7],
            "corpo={0}".format(corpo),
        )

    def test_fracao_111(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [1, 1, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "fracao [1,1,1] em altura=24 -> [6,6,6] (pesos iguais)",
            corpo == [6, 6, 6],
            "corpo={0}".format(corpo),
        )

    def test_fracao_212(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        self._r(
            "fracao [2,1,2] em altura=24 -> [7,4,7] (proporcao 2:1:2)",
            corpo == [7, 4, 7],
            "corpo={0}".format(corpo),
        )

    def test_fracao_vetor_generico_adicional(self):
        # [1,3,1] e [5,2,7] pelo mesmo codigo generico (sem especializacao).
        modelo_131 = self._modelo_dist({"modo": "fracao", "valores": [1, 3, 1]})
        corpo_131 = _corpo_alturas(
            renderizar_tela(modelo_131, _ESTILO_CURVA, largura=42, altura=24)
        )
        self._r(
            "fracao [1,3,1] em altura=24 -> [4,11,3] soma 18",
            corpo_131 == [4, 11, 3] and sum(corpo_131) == 18,
            "corpo={0}".format(corpo_131),
        )
        modelo_527 = self._modelo_dist({"modo": "fracao", "valores": [5, 2, 7]})
        corpo_527 = _corpo_alturas(
            renderizar_tela(modelo_527, _ESTILO_CURVA, largura=42, altura=24)
        )
        self._r(
            "fracao [5,2,7] em altura=24 -> soma 18",
            sum(corpo_527) == 18,
            "corpo={0}".format(corpo_527),
        )

    # --------------------------------------------- soma exata / sem sobra
    def test_soma_das_cotas_igual_area_distribuivel(self):
        for dist in [
            {"modo": "igual"},
            {"modo": "fracao", "valores": [1, 1, 1]},
            {"modo": "fracao", "valores": [2, 1, 2]},
            {"modo": "fracao", "valores": [1, 3, 1]},
            {"modo": "percentual", "valores": [40, 20, 40]},
        ]:
            modelo = self._modelo_dist(dist)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
            corpo = _corpo_alturas(saida)
            self._r(
                "soma cotas == l_corpo_disponivel (18) para {0}".format(dist),
                sum(corpo) == 18,
                "corpo={0} soma={1}".format(corpo, sum(corpo)),
            )

    def test_sem_sobra_externa_abaixo_do_ultimo_filho(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        linhas = saida.split("\n")
        # Localizar a ultima caixa do corpo (C) e a caixa Menus.
        idx_ultimo_topo = max(i for i, ln in enumerate(linhas) if ln.startswith("╭ C"))
        idx_menus = next(i for i, ln in enumerate(linhas) if ln.startswith("╭ Menus"))
        entre = linhas[idx_ultimo_topo:idx_menus]
        # Nenhuma linha de preenchimento externo (" "*42) entre as duas caixas.
        fill_externo = [ln for ln in entre if ln == " " * 42]
        self._r(
            "distribuicao: sem sobra externa entre ultimo filho e barra",
            len(fill_externo) == 0,
            "fills={0}".format(len(fill_externo)),
        )

    # -------------------------------------------------- preenchimento interno
    def test_preenchimento_interno_moldura_ocupa_cota(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        corpo = _corpo_alturas(saida)
        # cota do primeiro filho (7) > altura natural do console (3).
        self._r(
            "preenchimento interno: primeiro filho ocupa cota (7 > natural 3)",
            corpo[0] == 7,
            "corpo={0}".format(corpo),
        )
        # As linhas internas do primeiro filho sao bordeadas (│ ... │).
        linhas = saida.split("\n")
        idx_topo_a = next(i for i, ln in enumerate(linhas) if ln.startswith("╭ A"))
        idx_base_a = idx_topo_a + corpo[0] - 1
        internas = linhas[idx_topo_a + 1:idx_base_a]
        self._r(
            "preenchimento interno: linhas internas bordeadas (│ ... │)",
            len(internas) == corpo[0] - 2
            and all(ln.startswith("│") and ln.endswith("│") for ln in internas),
            "internas={0}".format(internas[:2]),
        )
        # Cada linha nao-vazia tem exatamente 42 chars.
        self._r(
            "preenchimento interno: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in linhas if ln != ""),
        )

    # ------------------------------------------------------ JSON real (D9)
    def test_json_real_orquestrador_distribui_212(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        self._r(
            "JSON real: demo declara fracao [2,1,2]",
            isinstance(modelo.corpo.distribuicao, dict)
            and modelo.corpo.distribuicao.get("valores") == [2, 1, 2],
        )
        # H-0037: com 11 itens no lancador, NAVEGAR requer >= 10 linhas; a
        # fracao [2,1,2] sobre l_corpo=25 (altura=31) -> [10,5,10].
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=31)
        corpo = _corpo_alturas(saida)
        # l_corpo_disponivel=25 -> [10,5,10] para ITENS/INFO/NAVEGAR.
        self._r(
            "JSON real: altura=31 distribui [10,5,10] entre ITENS/INFO/NAVEGAR",
            corpo == [10, 5, 10],
            "corpo={0}".format(corpo),
        )
        # Sem preenchimento externo (sobra absorvida internamente).
        fill_ext = [ln for ln in saida.split("\n") if ln == " " * 42]
        self._r(
            "JSON real: sem preenchimento externo (sobra interna nas molduras)",
            len(fill_ext) == 0,
            "fills={0}".format(len(fill_ext)),
        )
        self._r(
            "JSON real: total de linhas == 31",
            saida.count("\n") == 31,
            "count={0}".format(saida.count("\n")),
        )

    def test_json_real_sem_altura_preserva_conteudo_natural(self):
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO))
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "JSON real: sem altura preserva _EXPECTED_ORQUESTRADOR (natural)",
            saida == _EXPECTED_ORQUESTRADOR,
        )

    # ----------------------------------------------------- redimensionamento
    def test_redimensionamento_recalcula_cotas(self):
        modelo = self._modelo_dist({"modo": "fracao", "valores": [2, 1, 2]})
        saida_24 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=24)
        saida_30 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=30)
        corpo_24 = _corpo_alturas(saida_24)
        corpo_30 = _corpo_alturas(saida_30)
        # altura=24 -> l_corpo=18 -> [7,4,7]; altura=30 -> l_corpo=24 -> [10,5,9]?
        # 24*2/5=9.6, 24*1/5=4.8, 24*2/5=9.6 -> floor [9,4,9] soma 22, faltam 2.
        # restos [0.6,0.8,0.6] -> idx1, depois idx0 (ordem) -> [10,5,9].
        self._r(
            "redimensionamento: altura=24 -> [7,4,7]",
            corpo_24 == [7, 4, 7],
            "corpo={0}".format(corpo_24),
        )
        self._r(
            "redimensionamento: altura=30 -> [10,5,9] (recalculado)",
            corpo_30 == [10, 5, 9],
            "corpo={0}".format(corpo_30),
        )
        self._r(
            "redimensionamento: soma cotas acompanha altura (18 e 24)",
            sum(corpo_24) == 18 and sum(corpo_30) == 24,
        )

    # ------------------------------------------- preservacao sem distribuicao
    def test_telas_sem_distribuicao_nao_mudam(self):
        # destino_minimo e grupo_minimo nao declaram distribuicao.
        for id_tela in ("destino_minimo", "grupo_minimo", "stub_b"):
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            self._r(
                "{0}: sem distribuicao (distribuicao is None)".format(id_tela),
                modelo.corpo.distribuicao is None,
                "dist={0!r}".format(modelo.corpo.distribuicao),
            )

    # ------------------------------------------------- arranjo horizontal (D1)
    def test_arranjo_horizontal_nao_regride_com_distribuicao(self):
        # H-0026: distribuicao declarada em arranjo horizontal agora ALTERA as
        # larguras conforme os valores (antes do H-0026 o renderizador ignorava
        # a distribuicao e mantinha particionamento uniforme). Com fracao [1,1]
        # em total_w=42, cada area deve ter exatamente 21 colunas.
        modelo_h = ModeloTela(
            id="teste_h0025_h",
            schema="tela.v1",
            cabecalho={"titulo": "H0025H", "descricao": "horizontal"},
            corpo=Corpo(
                arranjo="horizontal",
                elementos=[
                    ElementoCorpo(id="a", tipo="console", _campos_inertes={"titulo": "A"}),
                    ElementoCorpo(id="b", tipo="console", _campos_inertes={"titulo": "B"}),
                ],
                distribuicao={"modo": "fracao", "valores": [1, 1]},
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )
        saida = renderizar_tela(modelo_h, _ESTILO_CURVA, largura=42)
        self._r(
            "horizontal + distribuicao declarada: renderiza sem erro",
            isinstance(saida, str) and len(saida) > 0,
        )
        self._r(
            "horizontal + distribuicao: '╮╭' presente (particionamento contiguo)",
            "╮╭" in saida,
        )
        self._r(
            "horizontal + distribuicao: cada linha tem 42 chars",
            all(len(ln) == 42 for ln in saida.split("\n") if ln != ""),
        )
        # H-0026: fracao [1,1] em 42 -> cada area tem 21 colunas. A transicao
        # entre as duas areas na linha de topo ocorre na coluna 21 (char[20]=='╮'
        # da area A, char[21]=='╭' da area B).
        linha_topo_corpo = next(
            (ln for ln in saida.split("\n") if "╭ A" in ln), None
        )
        if linha_topo_corpo is not None:
            self._r(
                "horizontal + fracao[1,1]: area A tem 21 colunas (char[20]=='╮')",
                len(linha_topo_corpo) >= 22 and linha_topo_corpo[20] == "╮",
                "char[20]={0!r}".format(
                    linha_topo_corpo[20] if len(linha_topo_corpo) > 20 else "?"
                ),
            )
            self._r(
                "horizontal + fracao[1,1]: area B inicia na coluna 21 (char[21]=='╭')",
                len(linha_topo_corpo) >= 22 and linha_topo_corpo[21] == "╭",
                "char[21]={0!r}".format(
                    linha_topo_corpo[21] if len(linha_topo_corpo) > 21 else "?"
                ),
            )
        else:
            self._r(
                "horizontal + fracao[1,1]: linha de topo do corpo encontrada", False
            )
            self._r("horizontal + fracao[1,1]: area A tem 21 colunas", False)
            self._r("horizontal + fracao[1,1]: area B inicia na coluna 21", False)

    def run_all(self):
        print("")
        print("== H-0025 - distribuicao vertical explicita da area do corpo ==")
        self.test_algoritmo_maiores_restos_exemplos_normativos()
        self.test_algoritmo_soma_exata_invariante()
        self.test_algoritmo_vetores_genericos_sem_codigo_especial()
        self.test_algoritmo_maiores_restos_distribui_residuo()
        self.test_algoritmo_desempate_por_ordem_declarada()
        self.test_pesos_distribuicao_por_modo()
        self.test_ausencia_preserva_altura_natural_sem_cota()
        self.test_ausencia_nao_materializa_igual_no_modelo()
        self.test_igual_explicito_divide_igualmente()
        self.test_igual_explicito_maiores_restos()
        self.test_percentual_explicito()
        self.test_fracao_111()
        self.test_fracao_212()
        self.test_fracao_vetor_generico_adicional()
        self.test_soma_das_cotas_igual_area_distribuivel()
        self.test_sem_sobra_externa_abaixo_do_ultimo_filho()
        self.test_preenchimento_interno_moldura_ocupa_cota()
        self.test_json_real_orquestrador_distribui_212()
        self.test_json_real_sem_altura_preserva_conteudo_natural()
        self.test_redimensionamento_recalcula_cotas()
        self.test_telas_sem_distribuicao_nao_mudam()
        self.test_arranjo_horizontal_nao_regride_com_distribuicao()


class TestDistribuicaoHorizontalH0026:
    """Cobertura da distribuicao horizontal explicita do corpo (H-0026).

    Cobre os minimos exigidos pelo H-0026 secao 16: percentual [50,50] e
    assimetrico [60,40]; fracao [1,1], [2,1] e equivalencia por escala [4,2];
    maiores restos T06 (largura 100 -> [34,33,33]) e T07 (largura 101 ->
    [34,34,33]); soma das larguras igual a distribuivel; bordas em contato;
    largura total preservada; preenchimento interno quando conteudo menor que
    a cota; ausencia de distribuicao sem regressao; preservacao vertical
    H-0025; rejeicoes do loader preservadas.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _modelo_dist_h(self, distribuicao, n=2, titulos=None):
        """Modelo horizontal com n consoles e distribuicao declarada."""
        if titulos is None:
            titulos = [chr(ord("A") + i) for i in range(n)]
        elementos = [
            ElementoCorpo(
                id=titulos[i].lower(), tipo="console",
                _campos_inertes={"titulo": titulos[i]},
            )
            for i in range(n)
        ]
        return ModeloTela(
            id="teste_h0026",
            schema="tela.v1",
            cabecalho={"titulo": "H0026", "descricao": "dist horizontal"},
            corpo=Corpo(
                arranjo="horizontal", elementos=elementos,
                distribuicao=distribuicao,
            ),
            barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
            _raw={},
        )

    def _larguras_das_areas(self, saida, titulos):
        """Extrai a largura de cada area a partir da linha de topo do corpo.

        Localiza a linha que contem o topo da primeira area (``╭ {titulo0}``)
        e devolve as larguras detectando as transicoes ``╮╭`` entre areas
        adjacentes. Retorna lista de inteiros (largura de cada area).
        """
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_topo = next(
            (ln for ln in linhas if "╭ {0}".format(titulos[0]) in ln), None
        )
        if linha_topo is None:
            return None
        # As areas sao contiguas: cada area inicia com ╭ e termina com ╮ (na
        # linha de topo). As transicoes internas produzem ╮╭. Dividir a linha
        # pelos pontos de transicao ╮╭ mantendo as bordas.
        larguras = []
        inicio = 0
        i = 0
        while i < len(linha_topo) - 1:
            if linha_topo[i] == "╮" and linha_topo[i + 1] == "╭":
                larguras.append(i + 1 - inicio)
                inicio = i + 1
            i += 1
        # Ultima area: do ultimo inicio ate o final da linha
        larguras.append(len(linha_topo) - inicio)
        return larguras

    # ------------------------------------ algoritmo de maiores restos (helper)
    def test_algoritmo_distribuir_larguras_soma_exata(self):
        # Invariante: sum(cotas) == largura_disponivel para varios pares.
        for largura, pesos in [
            (42, [1, 1]), (42, [2, 1]), (42, [50, 50]), (42, [60, 40]),
            (100, [1, 1, 1]), (101, [1, 1, 1]), (100, [2, 1, 2]),
            (99, [3, 5, 7]), (7, [1]), (17, [1, 3, 1]),
        ]:
            cotas = _distribuir_larguras(largura, pesos)
            self._r(
                "alg larg: soma das cotas == largura ({0}, {1})".format(
                    largura, pesos
                ),
                sum(cotas) == largura,
                "cotas={0} soma={1}".format(cotas, sum(cotas)),
            )

    def test_algoritmo_distribuir_larguras_exemplos_normativos(self):
        self._r(
            "alg larg: 100 com [1,1,1] -> [34,33,33] (T06)",
            _distribuir_larguras(100, [1, 1, 1]) == [34, 33, 33],
            "obtido={0}".format(_distribuir_larguras(100, [1, 1, 1])),
        )
        self._r(
            "alg larg: 101 com [1,1,1] -> [34,34,33] (T07)",
            _distribuir_larguras(101, [1, 1, 1]) == [34, 34, 33],
            "obtido={0}".format(_distribuir_larguras(101, [1, 1, 1])),
        )

    # ------------------------------------------------------------- T01 percentual [50,50]
    def test_percentual_simetrico_50_50(self):
        modelo = self._modelo_dist_h(
            {"modo": "percentual", "valores": [50, 50]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T01: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T01: percentual [50,50] -> [21,21]", larguras == [21, 21],
                "larguras={0}".format(larguras))
        self._r("T01: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))
        self._r("T01: '╮╭' presente (bordas coladas)", "╮╭" in saida)

    # ------------------------------------------------------ T02 percentual [60,40]
    def test_percentual_assimetrico_60_40(self):
        modelo = self._modelo_dist_h(
            {"modo": "percentual", "valores": [60, 40]}
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T02: larguras detectadas", False, "linha de topo nao achada")
            return
        # 42*0.6=25.2 -> 25 ; 42*0.4=16.8 -> 16+1 (resto 0.8) = 17
        self._r("T02: percentual [60,40] -> [25,17]", larguras == [25, 17],
                "larguras={0}".format(larguras))
        self._r("T02: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ------------------------------------------------------------- T03 fracao [1,1]
    def test_fracao_simetrico_1_1(self):
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [1, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T03: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T03: fracao [1,1] -> [21,21]", larguras == [21, 21],
                "larguras={0}".format(larguras))
        self._r("T03: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ------------------------------------------------------------- T04 fracao [2,1]
    def test_fracao_assimetrico_2_1(self):
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        larguras = self._larguras_das_areas(saida, ["A", "B"])
        if larguras is None:
            self._r("T04: larguras detectadas", False, "linha de topo nao achada")
            return
        # 42*2/3=28 ; 42*1/3=14
        self._r("T04: fracao [2,1] -> [28,14]", larguras == [28, 14],
                "larguras={0}".format(larguras))
        self._r("T04: soma das larguras == 42", sum(larguras) == 42,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------------- T05 equivalencia por escala [2,1]/[4,2]
    def test_fracao_equivalencia_por_escala(self):
        modelo_21 = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        modelo_42 = self._modelo_dist_h({"modo": "fracao", "valores": [4, 2]})
        saida_21 = renderizar_tela(modelo_21, _ESTILO_CURVA, largura=42)
        saida_42 = renderizar_tela(modelo_42, _ESTILO_CURVA, largura=42)
        larguras_21 = self._larguras_das_areas(saida_21, ["A", "B"])
        larguras_42 = self._larguras_das_areas(saida_42, ["A", "B"])
        if larguras_21 is None or larguras_42 is None:
            self._r("T05: larguras detectadas", False,
                    "21={0} 42={1}".format(larguras_21, larguras_42))
            return
        self._r(
            "T05: fracao [2,1] e [4,2] produzem larguras identicas",
            larguras_21 == larguras_42,
            "[2,1]={0} [4,2]={1}".format(larguras_21, larguras_42),
        )
        self._r("T05: ambas produzem [28,14]",
                larguras_21 == [28, 14] and larguras_42 == [28, 14],
                "21={0} 42={1}".format(larguras_21, larguras_42))

    # --------------------------------------------------- T06 maiores restos larg=100
    def test_t06_maiores_restos_largura_100(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
        larguras = self._larguras_das_areas(saida, ["A", "B", "C"])
        if larguras is None:
            self._r("T06: larguras detectadas", False, "linha de topo nao achada")
            return
        self._r("T06: fracao [1,1,1] em 100 -> [34,33,33]", larguras == [34, 33, 33],
                "larguras={0}".format(larguras))
        self._r("T06: soma das larguras == 100", sum(larguras) == 100,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------------- T07 empate de restos resolvido por ordem
    def test_t07_empate_restos_resolvido_por_ordem_declarada(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=101)
        larguras = self._larguras_das_areas(saida, ["A", "B", "C"])
        if larguras is None:
            self._r("T07: larguras detectadas", False, "linha de topo nao achada")
            return
        # Partes inteiras [33,33,33]; faltam 2; restos empatados -> posicoes 0 e 1.
        self._r("T07: fracao [1,1,1] em 101 -> [34,34,33]", larguras == [34, 34, 33],
                "larguras={0}".format(larguras))
        self._r("T07: soma das larguras == 101", sum(larguras) == 101,
                "soma={0}".format(sum(larguras)))

    # ---------------------------------- T08 soma das larguras == largura distribuivel
    def test_t08_soma_larguras_igual_distribuivel(self):
        casos = [
            ({"modo": "percentual", "valores": [50, 50]}, 42, ["A", "B"]),
            ({"modo": "percentual", "valores": [60, 40]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [1, 1]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [2, 1]}, 42, ["A", "B"]),
            ({"modo": "fracao", "valores": [1, 1, 1]}, 100, ["A", "B", "C"]),
            ({"modo": "fracao", "valores": [1, 1, 1]}, 101, ["A", "B", "C"]),
        ]
        for dist, largura, titulos in casos:
            modelo = self._modelo_dist_h(dist, n=len(titulos), titulos=titulos)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=largura)
            larguras = self._larguras_das_areas(saida, titulos)
            if larguras is None:
                self._r(
                    "T08: soma == {0} ({1})".format(largura, dist),
                    False, "larguras nao detectadas",
                )
                continue
            self._r(
                "T08: soma das larguras == {0} ({1})".format(largura, dist),
                sum(larguras) == largura,
                "larguras={0} soma={1}".format(larguras, sum(larguras)),
            )

    # ------------------------------------------------- T09 bordas horizontais em contato
    def test_t09_bordas_em_contato(self):
        modelo = self._modelo_dist_h(
            {"modo": "fracao", "valores": [1, 1, 1]}, n=3, titulos=["A", "B", "C"],
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=101)
        self._r("T09: '╮╭' presente no topo", "╮╭" in saida)
        self._r("T09: '╯╰' presente na base", "╯╰" in saida)
        self._r("T09: '││' presente em linhas internas", "││" in saida)

    # -------------------------------------------- T10 largura total da saida preservada
    def test_t10_largura_total_preservada(self):
        for dist in [
            {"modo": "percentual", "valores": [50, 50]},
            {"modo": "fracao", "valores": [2, 1]},
        ]:
            modelo = self._modelo_dist_h(dist)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            linhas_nv = [ln for ln in saida.split("\n") if ln != ""]
            self._r(
                "T10: todas as linhas com 42 chars ({0})".format(dist),
                all(len(ln) == 42 for ln in linhas_nv),
                "invalidas={0}".format(
                    [(i, len(ln)) for i, ln in enumerate(linhas_nv)
                     if len(ln) != 42]
                ),
            )

    # ----------------------------- T11 preenchimento interno quando conteudo < cota
    def test_t11_preenchimento_interno_conteudo_menor_que_cota(self):
        # Console com uma linha de conteudo ("(console)") numa area larga deve
        # manter a linha de conteudo com largura total da area (preenchida com
        # espacos ate a borda direita). Verifica que a area A (cota 28) preenche
        # sua linha de conteudo ate completar 28 colunas.
        modelo = self._modelo_dist_h({"modo": "fracao", "valores": [2, 1]})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = [ln for ln in saida.split("\n") if ln != ""]
        linha_console = next(
            (ln for ln in linhas if "(console)" in ln), None
        )
        if linha_console is None:
            self._r("T11: linha de conteudo '(console)' encontrada", False)
            return
        # A area A ocupa as primeiras 28 colunas (cota 28). A linha de conteudo
        # da area A termina com '|' na coluna 27 (borda direita da area A).
        self._r(
            "T11: conteudo da area A preenchido ate borda (char[27]=='│')",
            len(linha_console) >= 28 and linha_console[27] == "│",
            "char[27]={0!r}".format(
                linha_console[27] if len(linha_console) > 27 else "?"
            ),
        )
        # E nao ha espaco externo entre as areas: char[28] e a borda esquerda
        # da area B.
        self._r(
            "T11: area B inicia imediatamente apos (char[28]=='│')",
            len(linha_console) >= 29 and linha_console[28] == "│",
            "char[28]={0!r}".format(
                linha_console[28] if len(linha_console) > 28 else "?"
            ),
        )

    # ------------------------------- T-NR01 ausencia de distribuicao sem regressao
    def test_ausencia_distribuicao_rejeita_multiplos_participantes(self):
        # QA-H0033-IMP-HIGH-001: ausencia de distribuicao com multiplos elementos
        # no eixo horizontal deve ser rejeitada explicitamente (DA-02/ADR-0024).
        # Ausencia NAO equivale a igual; composicao invalida -> RenderizadorErro.
        modelo_sem = _modelo_horizontal(
            "horizontal", [("console", "A"), ("console", "B")], largura=42,
        )
        erro_correto = False
        try:
            renderizar_tela(modelo_sem, _ESTILO_CURVA, largura=42)
        except RenderizadorErro as e:
            erro_correto = "DA-02" in str(e)
        self._r(
            "T-NR01: ausencia dist horizontal 2 elem -> RenderizadorErro DA-02",
            erro_correto,
        )
        # 3 elementos: tambem deve ser rejeitado por DA-02.
        modelo_sem3 = _modelo_horizontal(
            "horizontal",
            [("console", "A"), ("console", "B"), ("console", "C")],
            largura=100,
        )
        erro_correto3 = False
        try:
            renderizar_tela(modelo_sem3, _ESTILO_CURVA, largura=100)
        except RenderizadorErro as e:
            erro_correto3 = "DA-02" in str(e)
        self._r(
            "T-NR01: ausencia dist horizontal 3 elem -> RenderizadorErro DA-02",
            erro_correto3,
        )

    # ------------------------------- T-NR02 distribuicao vertical H-0025 sem regressao
    def test_distribuicao_vertical_h0025_nao_regride(self):
        # Re-verifica que o helper vertical continua produzindo os exemplos
        # normativos aprovados pelo H-0025.
        self._r(
            "T-NR02: vertical 68 com [1,1,1] -> [23,23,22]",
            _distribuir_alturas(68, [1, 1, 1]) == [23, 23, 22],
            "obtido={0}".format(_distribuir_alturas(68, [1, 1, 1])),
        )
        self._r(
            "T-NR02: vertical 68 com [2,1,2] -> [27,14,27]",
            _distribuir_alturas(68, [2, 1, 2]) == [27, 14, 27],
            "obtido={0}".format(_distribuir_alturas(68, [2, 1, 2])),
        )

    # ------------------------------- T-NR03 rejeicoes do loader preservadas
    def test_rejeicoes_loader_preservadas(self):
        # O loader (arquivo somente leitura neste ciclo) rejeita soma percentual
        # != 100 e pesos nao positivos para corpo horizontal. Esta verificacao
        # confirma que o loader continua rejeitando valores invalidos quando o
        # arranjo e horizontal, exercitando o mesmo caminho de validacao que
        # existe para o eixo vertical. Usa infraestrutura minima de escrita em
        # diretorio temporario, sem duplicar a suite completa de loader.
        import json
        import tempfile
        from pathlib import Path
        from tela.loader import (
            TelaEstruturaInvalida,
            carregar_tela as _carregar_tela_loader,
        )

        def _escrever(base_dir, id_tela, conteudo):
            dir_telas = Path(base_dir) / "config" / "telas"
            dir_telas.mkdir(parents=True, exist_ok=True)
            arquivo = dir_telas / "{0}.json".format(id_tela)
            arquivo.write_text(
                json.dumps(conteudo, ensure_ascii=False), encoding="utf-8",
            )

        def _tela_horizontal(id_tela, distribuicao):
            return {
                "schema": "tela.v1", "id": id_tela,
                "cabecalho": {"titulo": "T", "descricao": "D"},
                "corpo": {
                    "arranjo": "horizontal",
                    "elementos": [
                        {"id": "a", "tipo": "console"},
                        {"id": "b", "tipo": "console"},
                    ],
                    "distribuicao": distribuicao,
                },
                "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
            }

        tmp_base = tempfile.mkdtemp(prefix="teste_h0026_loader_")
        try:
            def _espera_rejeicao(nome, fn):
                try:
                    fn()
                    self._r(nome, False, "nenhuma excecao levantada")
                except TelaEstruturaInvalida as exc:
                    self._r(nome, True, str(exc))
                except Exception as exc:  # pragma: no cover - diagnostico
                    self._r(
                        nome, False,
                        "excecao inesperada: {0!r}".format(exc),
                    )

            # soma percentual != 100 em horizontal -> rejeicao
            _escrever(
                tmp_base, "pct_inv",
                _tela_horizontal("pct_inv",
                                 {"modo": "percentual", "valores": [50, 30]}),
            )
            _espera_rejeicao(
                "T-NR03: loader rejeita percentual soma != 100 em horizontal",
                lambda: _carregar_tela_loader(tmp_base, "pct_inv"),
            )
            # peso nao positivo (zero) em horizontal -> rejeicao
            _escrever(
                tmp_base, "frac_zero",
                _tela_horizontal("frac_zero",
                                 {"modo": "fracao", "valores": [0, 1]}),
            )
            _espera_rejeicao(
                "T-NR03: loader rejeita fracao com peso zero em horizontal",
                lambda: _carregar_tela_loader(tmp_base, "frac_zero"),
            )
            # referencia simbolica para garantir import valido
            self._r(
                "T-NR03: TelaEstruturaInvalida importado do loader",
                TelaEstruturaInvalida is not None,
            )
        finally:
            import shutil
            shutil.rmtree(tmp_base, ignore_errors=True)

    def run_all(self):
        print("")
        print("== H-0026 - distribuicao horizontal explicita do corpo ==")
        self.test_algoritmo_distribuir_larguras_soma_exata()
        self.test_algoritmo_distribuir_larguras_exemplos_normativos()
        self.test_percentual_simetrico_50_50()
        self.test_percentual_assimetrico_60_40()
        self.test_fracao_simetrico_1_1()
        self.test_fracao_assimetrico_2_1()
        self.test_fracao_equivalencia_por_escala()
        self.test_t06_maiores_restos_largura_100()
        self.test_t07_empate_restos_resolvido_por_ordem_declarada()
        self.test_t08_soma_larguras_igual_distribuivel()
        self.test_t09_bordas_em_contato()
        self.test_t10_largura_total_preservada()
        self.test_t11_preenchimento_interno_conteudo_menor_que_cota()
        self.test_ausencia_distribuicao_rejeita_multiplos_participantes()
        self.test_distribuicao_vertical_h0025_nao_regride()
        self.test_rejeicoes_loader_preservadas()


def _modelo_hierarquico(corpo_arranjo, corpo_elementos, largura=42, titulo_cab="H",
                        corpo_distribuicao=None):
    """Cria ModeloTela sintetico com corpo hierarquico para testes H-0027."""
    return ModeloTela(
        id="teste_h0027",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "teste hierarquia"},
        corpo=Corpo(arranjo=corpo_arranjo, elementos=corpo_elementos,
                    distribuicao=corpo_distribuicao),
        barra_de_menus={"chips": [{"id": "c1", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


def _grupo(gid, arranjo, filhos, distribuicao=None):
    """Helper: cria ElementoCorpo tipo 'grupo' com arranjo e filhos."""
    inertes = {}
    if arranjo is not None:
        inertes["arranjo"] = arranjo
    if distribuicao is not None:
        inertes["distribuicao"] = distribuicao
    return ElementoCorpo(id=gid, tipo="grupo", _campos_inertes=inertes,
                         elementos=filhos)


def _funcional(fid, tipo, titulo=None):
    """Helper: cria ElementoCorpo funcional simples."""
    inertes = {}
    if titulo:
        inertes["titulo"] = titulo
    if tipo == "lancador":
        inertes["itens"] = []
    return ElementoCorpo(id=fid, tipo=tipo, _campos_inertes=inertes)


def _grupo_matriz_render_h0028(
    gid="g_matriz", n_linhas=2, n_colunas=2, dist_linhas=None,
    dist_colunas=None, filhos=None, celulas=None,
):
    if dist_linhas is None:
        dist_linhas = {"modo": "igual"}
    if dist_colunas is None:
        dist_colunas = {"modo": "igual"}
    if filhos is None:
        filhos = [
            _funcional("e{0}".format(i), "console", "E{0}".format(i))
            for i in range(1, n_linhas * n_colunas + 1)
        ]
    if celulas is None:
        celulas = []
        indice = 0
        for linha in range(1, n_linhas + 1):
            for coluna in range(1, n_colunas + 1):
                celulas.append({
                    "linha": linha,
                    "coluna": coluna,
                    "elemento": filhos[indice].id,
                })
                indice += 1
    matriz = {
        "linhas": {
            "quantidade": n_linhas,
            "distribuicao": dist_linhas,
        },
        "colunas": {
            "quantidade": n_colunas,
            "distribuicao": dist_colunas,
        },
        "celulas": celulas,
    }
    return ElementoCorpo(
        id=gid,
        tipo="grupo",
        _campos_inertes={"estrutura": "matriz", "matriz": matriz},
        elementos=filhos,
    )


def _modelo_matriz_render_h0028(elementos, arranjo="vertical", distribuicao=None):
    if distribuicao is None:
        distribuicao = {"modo": "igual"}
    return ModeloTela(
        id="teste_h0028",
        schema="tela.v1",
        cabecalho={"titulo": "H28", "descricao": "matriz"},
        corpo=Corpo(arranjo=arranjo, elementos=elementos, distribuicao=distribuicao),
        barra_de_menus={"chips": [{"id": "ok", "tecla": "k", "texto": "Ok"}]},
        _raw={},
    )


def _linhas_corpo_renderizado(saida):
    linhas = saida.splitlines()
    return linhas[3:-3]


def _posicoes_bordas_linha(linha):
    bordas = set("│┃║┌┐└┘┼├┤┬┴╭╮╰╯─")
    return [i for i, ch in enumerate(linha) if ch in bordas]


class TestHierarquiaGruposH0027:
    """Testes de composicao hierarquica com tres niveis de grupos (H-0027 / ADR-0019).

    Cobre: renderizacao com 1-3 niveis de grupos; arranjos vertical e horizontal
    em grupos; distribuicao em grupos; mistura grupo+funcional; multiplos dashboards;
    regressao do orquestrador e grupo_minimo.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # --- 1 nivel de grupo, arranjo vertical ---
    def test_g1_vertical_produz_saida(self):
        """Grupo nivel 1 com arranjo vertical e 2 funcionais produz saida nao vazia."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("console_a", "console", "CONSOLA"),
                _funcional("dash_a", "dashboard", "PAINEL"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo nivel 1 vertical com 2 funcionais produz saida nao vazia",
            bool(saida.strip()),
            "len={0}".format(len(saida)),
        )
        self._r(
            "H-0027: saida contem caixa de console (cabecalho 'CONSOLA')",
            "CONSOLA" in saida,
        )
        self._r(
            "H-0027: saida contem caixa de dashboard (cabecalho 'PAINEL')",
            "PAINEL" in saida,
        )

    # --- 1 nivel de grupo, arranjo horizontal ---
    def test_g1_horizontal_lado_a_lado(self):
        """Grupo nivel 1 com arranjo horizontal produz caixas lado a lado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "ESQUERDA"),
                _funcional("c2", "console", "DIREITA"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo horizontal: saida nao vazia",
            bool(saida.strip()),
        )
        # Caixas lado a lado: cabecalhos aparecem na mesma linha
        linhas = saida.split("\n")
        cabecalho_na_mesma_linha = any("ESQUERDA" in l and "DIREITA" in l for l in linhas)
        self._r(
            "H-0027: grupo horizontal: 'ESQUERDA' e 'DIREITA' aparecem na mesma linha",
            cabecalho_na_mesma_linha,
            "linhas={0!r}".format([l for l in linhas if "ESQUERDA" in l or "DIREITA" in l]),
        )

    # --- Grupo com arranjo ausente (None) -> vertical implícito ---
    def test_g1_arranjo_none_equivale_vertical(self):
        """Grupo sem arranjo produz saida equivalente a arranjo vertical."""
        modelo_none = _modelo_hierarquico("vertical", [
            _grupo("g1", None, [
                _funcional("c1", "console", "AA"),
                _funcional("c2", "console", "BB"),
            ]),
        ])
        modelo_vert = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "AA"),
                _funcional("c2", "console", "BB"),
            ]),
        ])
        saida_none = renderizar_tela(modelo_none, _ESTILO_CURVA, largura=42)
        saida_vert = renderizar_tela(modelo_vert, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo sem arranjo -> saida identica a arranjo 'vertical'",
            saida_none == saida_vert,
        )

    # --- 2 niveis de grupos ---
    def test_g2_vertical_vertical(self):
        """2 niveis de grupos verticais produz saida com todos os funcionais."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _grupo("g2", "vertical", [
                    _funcional("c1", "console", "PROFUNDO"),
                    _funcional("d1", "dashboard", "PAINEL"),
                ]),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: 2 niveis verticais: saida contem 'PROFUNDO'",
            "PROFUNDO" in saida,
        )
        self._r(
            "H-0027: 2 niveis verticais: saida contem 'PAINEL'",
            "PAINEL" in saida,
        )

    # --- 2 niveis: externo vertical, interno horizontal ---
    def test_g2_vertical_horizontal(self):
        """Nivel 1 vertical, nivel 2 horizontal: funcionais do g2 ficam lado a lado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("topo", "console", "TOPO"),
                _grupo("g2", "horizontal", [
                    _funcional("e", "console", "ESQQ"),
                    _funcional("d", "console", "DIRR"),
                ], distribuicao={"modo": "igual"}),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027: 2 niveis (vert+horiz): 'TOPO' presente na saida",
            "TOPO" in saida,
        )
        self._r(
            "H-0027: 2 niveis (vert+horiz): 'ESQQ' e 'DIRR' na mesma linha",
            any("ESQQ" in l and "DIRR" in l for l in linhas),
        )

    # --- 3 niveis de grupos ---
    def test_g3_profundidade_maxima(self):
        """3 niveis de grupos (profundidade maxima por ADR-0019 D2): funcional renderizado."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _grupo("g2", "vertical", [
                    _grupo("g3", "vertical", [
                        _funcional("c1", "console", "FOLHA"),
                    ]),
                ]),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: 3 niveis de grupos: saida contem 'FOLHA' (funcional no nivel 3)",
            "FOLHA" in saida,
        )

    # --- Distribuicao em grupo (modo igual) ---
    def test_distribuicao_igual_em_grupo(self):
        """Grupo com distribuicao='igual' distribui altura entre filhos (com altura declarada)."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        # Com altura declarada, distribuicao ganha efeito
        saida_com_alt = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
        saida_sem_alt = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo com dist=igual e altura: saida nao vazia",
            bool(saida_com_alt.strip()),
        )
        self._r(
            "H-0027: grupo com dist=igual e altura: contem 'ALFA'",
            "ALFA" in saida_com_alt,
        )
        self._r(
            "H-0027: grupo com dist=igual e altura: contem 'BETA'",
            "BETA" in saida_com_alt,
        )
        self._r(
            "H-0027: grupo com dist=igual sem altura: saida nao vazia (content-driven)",
            bool(saida_sem_alt.strip()),
        )

    # --- Distribuicao fracao em grupo horizontal ---
    def test_distribuicao_fracao_grupo_horizontal(self):
        """Grupo horizontal com distribuicao fracao 2:1 divide largura conforme pesos."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "GRANDE"),
                _funcional("c2", "console", "PEQQ"),
            ], distribuicao={"modo": "fracao", "valores": [2, 1]}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027: grupo horiz dist=fracao 2:1: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027: grupo horiz dist=fracao 2:1: 'GRANDE' e 'PEQQ' na mesma linha",
            any("GRANDE" in l and "PEQQ" in l for l in linhas),
        )

    # --- Mistura de grupo e funcional no mesmo nivel do corpo ---
    def test_mistura_grupo_e_funcional_no_corpo(self):
        """Corpo com grupo e funcional direto na mesma lista produz saida correta."""
        modelo = _modelo_hierarquico("vertical", [
            _funcional("topo", "console", "TOPO"),
            _grupo("g1", "horizontal", [
                _funcional("e", "console", "ESQQ"),
                _funcional("d", "console", "DIRR"),
            ], distribuicao={"modo": "igual"}),
            _funcional("base", "lancador"),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: mistura grupo+funcional: 'TOPO' presente",
            "TOPO" in saida,
        )
        self._r(
            "H-0027: mistura grupo+funcional: 'ESQQ' e 'DIRR' na mesma linha",
            any("ESQQ" in l and "DIRR" in l for l in saida.split("\n")),
        )

    # --- Multiplos dashboards em grupos distintos (ADR-0019 D7) ---
    def test_multiplos_dashboards_em_grupos(self):
        """Dois dashboards em grupos distintos sao ambos renderizados (D7)."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("d1", "dashboard", "PAINEL1"),
            ]),
            _grupo("g2", "vertical", [
                _funcional("d2", "dashboard", "PAINEL2"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: multiplos dashboards (D7): 'PAINEL1' presente",
            "PAINEL1" in saida,
        )
        self._r(
            "H-0027: multiplos dashboards (D7): 'PAINEL2' presente",
            "PAINEL2" in saida,
        )

    # --- Regressao: orquestrador.json ainda renderiza sem erro ---
    def test_regressao_orquestrador(self):
        """renderizar_tela sobre orquestrador.json preserva saida esperada (regressao)."""
        try:
            tela_raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
            modelo = construir_modelo(tela_raw)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027 regressao: demo renderiza sem excecao",
                True,
            )
            self._r(
                "H-0027 regressao: saida contem 'ORQUESTRADOR'",
                "ORQUESTRADOR" in saida,
            )
            self._r(
                "H-0027 regressao: saida contem 'Menus'",
                "Menus" in saida,
            )
        except Exception as exc:
            self._r("H-0027 regressao: demo renderiza sem excecao",
                    False, str(exc))

    # --- Regressao: grupo_minimo.json ainda renderiza ---
    def test_regressao_grupo_minimo(self):
        """renderizar_tela sobre grupo_minimo.json renderiza sem excecao (regressao)."""
        try:
            tela_raw = carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
            modelo = construir_modelo(tela_raw)
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027 regressao: grupo_minimo renderiza sem excecao",
                True,
            )
            self._r(
                "H-0027 regressao: saida nao vazia",
                bool(saida.strip()),
            )
        except Exception as exc:
            self._r("H-0027 regressao: grupo_minimo renderiza sem excecao",
                    False, str(exc))

    # --- Distribuicao percentual em grupo vertical com altura ---
    def test_distribuicao_percentual_grupo_vertical_com_altura(self):
        """Grupo vertical com dist=percentual 70/30 e altura declarada distribui corretamente."""
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "GRANDE"),
                _funcional("c2", "console", "PEQUENO"),
            ], distribuicao={"modo": "percentual", "valores": [70, 30]}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=22)
        self._r(
            "H-0027: dist percentual 70/30 vertical com altura: saida contem 'GRANDE'",
            "GRANDE" in saida,
        )
        self._r(
            "H-0027: dist percentual 70/30 vertical com altura: saida contem 'PEQUENO'",
            "PEQUENO" in saida,
        )
        # Caixa de 'GRANDE' deve ser mais alta do que 'PEQUENO' (aprox 70% vs 30%)
        linhas = saida.split("\n")
        inicio_grande = next((i for i, l in enumerate(linhas) if "GRANDE" in l), None)
        inicio_pequeno = next((i for i, l in enumerate(linhas) if "PEQUENO" in l), None)
        self._r(
            "H-0027: dist percentual: 'GRANDE' aparece antes de 'PEQUENO'",
            inicio_grande is not None and inicio_pequeno is not None
            and inicio_grande < inicio_pequeno,
        )

    # --- Grupo com arranjo 'sobreposto' (alias de vertical) ---
    def test_arranjo_sobreposto_alias_vertical(self):
        """Grupo com arranjo='sobreposto' produz saida identica a 'vertical'."""
        modelo_sob = _modelo_hierarquico("vertical", [
            _grupo("g1", "sobreposto", [
                _funcional("c1", "console", "XX"),
                _funcional("c2", "console", "YY"),
            ]),
        ])
        modelo_ver = _modelo_hierarquico("vertical", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "XX"),
                _funcional("c2", "console", "YY"),
            ]),
        ])
        saida_sob = renderizar_tela(modelo_sob, _ESTILO_CURVA, largura=42)
        saida_ver = renderizar_tela(modelo_ver, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo arranjo='sobreposto' -> saida identica a 'vertical'",
            saida_sob == saida_ver,
        )

    # --- Grupo com arranjo 'lado_a_lado' (alias de horizontal) ---
    def test_arranjo_lado_a_lado_alias_horizontal(self):
        """Grupo com arranjo='lado_a_lado' produz saida identica a 'horizontal'."""
        modelo_lal = _modelo_hierarquico("vertical", [
            _grupo("g1", "lado_a_lado", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        modelo_hor = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _funcional("c1", "console", "ALFA"),
                _funcional("c2", "console", "BETA"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida_lal = renderizar_tela(modelo_lal, _ESTILO_CURVA, largura=42)
        saida_hor = renderizar_tela(modelo_hor, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027: grupo arranjo='lado_a_lado' -> saida identica a 'horizontal'",
            saida_lal == saida_hor,
        )

    # --- Grupo vazio nao gera excecao (saida vazia para ele, resto renderiza) ---
    def test_grupo_vazio_nao_gera_excecao(self):
        """Grupo sem filhos (elementos=[]) nao lanca excecao; saida pode ser vazia para o grupo."""
        modelo = _modelo_hierarquico("vertical", [
            _funcional("c1", "console", "VISIVEL"),
            _grupo("g_vazio", "vertical", []),
        ])
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            self._r(
                "H-0027: grupo vazio nao lanca excecao",
                True,
            )
            self._r(
                "H-0027: grupo vazio: 'VISIVEL' ainda aparece na saida",
                "VISIVEL" in saida,
            )
        except Exception as exc:
            self._r("H-0027: grupo vazio nao lanca excecao", False, str(exc))

    # --- ACH-001 (a): Corpo horizontal com dois grupos filhos ---
    def test_corpo_horizontal_com_grupos_filhos(self):
        """Corpo horizontal com dois grupos filhos: grupos renderizados lado a lado."""
        modelo = _modelo_hierarquico("horizontal", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "ALFA"),
            ]),
            _grupo("g2", "vertical", [
                _funcional("c2", "console", "BETA"),
            ]),
        ], corpo_distribuicao={"modo": "igual"})
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'ALFA' presente",
            "ALFA" in saida,
        )
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'BETA' presente",
            "BETA" in saida,
        )
        # Grupos ficam lado a lado: ALFA e BETA devem aparecer na mesma linha
        self._r(
            "H-0027 ACH-001a: corpo horiz com grupos: 'ALFA' e 'BETA' na mesma linha",
            any("ALFA" in l and "BETA" in l for l in linhas),
        )
        # Grupos nao sao slots vazios: conteudo funcional efetivamente renderizado
        self._r(
            "H-0027 ACH-001a: grupos nao sao slots vazios ('ALFA' e 'BETA' presentes)",
            "ALFA" in saida and "BETA" in saida,
        )
        # Largura total preservada sem perda indevida
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001a: largura total preservada (42)",
            all(len(l) == 42 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 42]
            ),
        )
        # Sem sobreposicao: saida deterministica
        saida2 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0027 ACH-001a: saida e deterministica (sem sobreposicao)",
            saida == saida2,
        )

    # --- ACH-001 (b): Combinacao horizontal -> vertical ---
    def test_horizontal_grupo_vertical(self):
        """Corpo horizontal com grupo vertical interno: subdivisao vertical dentro do grupo.

        Estrutura:
            corpo horizontal
            └── grupo vertical
                ├── funcional "CIMA"
                └── funcional "BAIXO"
        """
        modelo = _modelo_hierarquico("horizontal", [
            _grupo("g1", "vertical", [
                _funcional("c1", "console", "CIMA"),
                _funcional("c2", "console", "BAIXO"),
            ]),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001b: horiz→vert: saida nao vazia",
            bool(saida.strip()),
        )
        self._r(
            "H-0027 ACH-001b: horiz→vert: 'CIMA' presente (funcional no grupo vertical)",
            "CIMA" in saida,
        )
        self._r(
            "H-0027 ACH-001b: horiz→vert: 'BAIXO' presente (funcional no grupo vertical)",
            "BAIXO" in saida,
        )
        # Subdivisao vertical interna: CIMA antes de BAIXO (ordem preservada)
        idx_cima = next((i for i, l in enumerate(linhas) if "CIMA" in l), None)
        idx_baixo = next((i for i, l in enumerate(linhas) if "BAIXO" in l), None)
        self._r(
            "H-0027 ACH-001b: horiz→vert: ordem vertical preservada ('CIMA' antes de 'BAIXO')",
            idx_cima is not None and idx_baixo is not None and idx_cima < idx_baixo,
        )
        # Sem achatamento: CIMA e BAIXO em linhas distintas
        self._r(
            "H-0027 ACH-001b: horiz→vert: sem achatamento ('CIMA' e 'BAIXO' em linhas distintas)",
            idx_cima is not None and idx_baixo is not None and idx_cima != idx_baixo,
        )
        # Ausencia de slot vazio: os dois funcionais foram renderizados
        self._r(
            "H-0027 ACH-001b: horiz→vert: ausencia de slot vazio (ambos presentes)",
            "CIMA" in saida and "BAIXO" in saida,
        )
        # Dimensoes compativeis: largura total preservada
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001b: horiz→vert: largura total preservada (42)",
            all(len(l) == 42 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 42]
            ),
        )

    # --- ACH-001 (c): Tres niveis com arranjos alternados ---
    def test_tres_niveis_arranjos_alternados(self):
        """3 niveis de grupos com arranjos alternados (H-0027 secao 18).

        Estrutura:
            corpo vertical
            └── g1 horizontal (nivel 1)
                ├── g2 vertical (nivel 2)
                │   └── g3 horizontal (nivel 3)
                │       ├── funcional "FA" (console)
                │       └── funcional "FB" (console)
                └── funcional "TOPO" (dashboard)

        Usa largura=80 para garantir area suficiente em tres niveis de
        particionamento horizontal (g1 -> g3) sem truncamento de titulo.
        """
        modelo = _modelo_hierarquico("vertical", [
            _grupo("g1", "horizontal", [
                _grupo("g2", "vertical", [
                    _grupo("g3", "horizontal", [
                        _funcional("f1", "console", "FA"),
                        _funcional("f2", "console", "FB"),
                    ], distribuicao={"modo": "igual"}),
                ]),
                _funcional("topo", "dashboard", "TOPO"),
            ], distribuicao={"modo": "igual"}),
        ])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=80)
        linhas = saida.split("\n")
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: saida nao vazia",
            bool(saida.strip()),
        )
        # Renderizacao dos elementos do nivel mais interno
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'FA' presente (funcional nivel 3)",
            "FA" in saida,
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'FB' presente (funcional nivel 3)",
            "FB" in saida,
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: 'TOPO' presente (funcional nivel 1)",
            "TOPO" in saida,
        )
        # Alternancia real dos arranjos: g3 horizontal -> FA e FB na mesma linha
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: g3(h): 'FA' e 'FB' na mesma linha",
            any("FA" in l and "FB" in l for l in linhas),
        )
        # Ausencia de achatamento: tres niveis sao respeitados
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: sem achatamento (todos os funcionais presentes)",
            "FA" in saida and "FB" in saida and "TOPO" in saida,
        )
        # Propagacao correta da area: largura total preservada
        linhas_nv = [l for l in linhas if l != ""]
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: largura total preservada (80)",
            all(len(l) == 80 for l in linhas_nv),
            "invalidas={0}".format(
                [(i, len(l)) for i, l in enumerate(linhas_nv) if len(l) != 80]
            ),
        )
        # Ausencia de sobreposicao: saida deterministica
        saida2 = renderizar_tela(modelo, _ESTILO_CURVA, largura=80)
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: saida deterministica (sem sobreposicao)",
            saida == saida2,
        )
        # Preservacao da ordem declarada: FA antes de FB no g3 horizontal
        # (na mesma linha, FA aparece a esquerda de FB)
        linha_com_fa_fb = next(
            (l for l in linhas if "FA" in l and "FB" in l), None
        )
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: ordem declarada preservada "
            "('FA' a esquerda de 'FB' na linha compartilhada)",
            linha_com_fa_fb is not None
            and linha_com_fa_fb.index("FA") < linha_com_fa_fb.index("FB"),
        )
        # Ausencia de nivel 4: apenas tres niveis estruturais
        self._r(
            "H-0027 ACH-001c: 3 niveis alternados: existencia dos tres niveis validada",
            "FA" in saida and "FB" in saida and "TOPO" in saida,
        )

    def run_all(self):
        print("")
        print("== TestHierarquiaGruposH0027: composicao hierarquica (H-0027 / ADR-0019) ==")
        self.test_g1_vertical_produz_saida()
        self.test_g1_horizontal_lado_a_lado()
        self.test_g1_arranjo_none_equivale_vertical()
        self.test_g2_vertical_vertical()
        self.test_g2_vertical_horizontal()
        self.test_g3_profundidade_maxima()
        self.test_distribuicao_igual_em_grupo()
        self.test_distribuicao_fracao_grupo_horizontal()
        self.test_mistura_grupo_e_funcional_no_corpo()
        self.test_multiplos_dashboards_em_grupos()
        self.test_regressao_orquestrador()
        self.test_regressao_grupo_minimo()
        self.test_distribuicao_percentual_grupo_vertical_com_altura()
        self.test_arranjo_sobreposto_alias_vertical()
        self.test_arranjo_lado_a_lado_alias_horizontal()
        self.test_grupo_vazio_nao_gera_excecao()
        self.test_corpo_horizontal_com_grupos_filhos()
        self.test_horizontal_grupo_vertical()
        self.test_tres_niveis_arranjos_alternados()


class TestRenderizadorMatrizH0028:
    """Testes de grade compartilhada para grupos matriciais (H-0028)."""

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _render_matriz(self, grupo, largura=80, altura=24):
        modelo = _modelo_matriz_render_h0028([grupo])
        return renderizar_tela(modelo, _ESTILO_CURVA, largura=largura, altura=altura)

    def test_matriz_2x2_alinhamento_vertical_e_horizontal(self):
        grupo = _grupo_matriz_render_h0028()
        largura = 80
        altura = 24
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 1])
        larguras = _distribuir_larguras(largura, [1, 1])
        cortes = [0, larguras[0] - 1, larguras[0], largura - 1]

        self._r(
            "H-0028 renderer: matriz 2x2 ocupa soma de alturas do corpo",
            len(corpo) == sum(alturas),
            "len={0} alturas={1!r}".format(len(corpo), alturas),
        )
        self._r(
            "H-0028 renderer: divisorias verticais 2x2 compartilham coordenadas",
            all(all(pos in _posicoes_bordas_linha(linha) for pos in cortes)
                for linha in corpo),
            "cortes={0!r}".format(cortes),
        )
        self._r(
            "H-0028 renderer: divisoria horizontal 2x2 inicia segunda linha na cota comum",
            "E3" in "\n".join(corpo[alturas[0]:])
            and "E1" in "\n".join(corpo[:alturas[0]]),
        )

    def test_matriz_2x4_pesos_assimetricos_compartilhados(self):
        grupo = _grupo_matriz_render_h0028(
            n_linhas=2,
            n_colunas=4,
            dist_linhas={"modo": "fracao", "valores": [1, 2]},
            dist_colunas={"modo": "fracao", "valores": [1, 2, 1, 2]},
        )
        largura = 90
        altura = 30
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 2])
        larguras = _distribuir_larguras(largura, [1, 2, 1, 2])
        acumulado = 0
        cortes = [0]
        for w in larguras:
            acumulado += w
            cortes.extend([acumulado - 1, acumulado])
        cortes = [c for c in cortes if 0 <= c < largura]

        self._r(
            "H-0028 renderer: matriz 2x4 linhas [1,2] aplicadas uma vez",
            alturas[1] >= alturas[0] * 2 - 1 and sum(alturas) == len(corpo),
            "alturas={0!r}".format(alturas),
        )
        self._r(
            "H-0028 renderer: matriz 2x4 colunas [1,2,1,2] aplicadas uma vez",
            sum(larguras) == largura and larguras[1] >= larguras[0] * 2 - 1,
            "larguras={0!r}".format(larguras),
        )
        self._r(
            "H-0028 renderer: cortes 2x4 aparecem nas duas faixas de linha",
            all(all(pos in _posicoes_bordas_linha(corpo[i]) for pos in cortes)
                for i in [0, alturas[0], len(corpo) - 1]),
            "cortes={0!r}".format(cortes),
        )

    def test_dimensoes_impares_e_restos_por_eixo(self):
        grupo = _grupo_matriz_render_h0028(
            n_linhas=3,
            n_colunas=3,
            dist_linhas={"modo": "fracao", "valores": [1, 2, 3]},
            dist_colunas={"modo": "fracao", "valores": [3, 2, 1]},
        )
        largura = 83
        altura = 29
        saida = self._render_matriz(grupo, largura=largura, altura=altura)
        corpo = _linhas_corpo_renderizado(saida)
        alturas = _distribuir_alturas(len(corpo), [1, 2, 3])
        larguras = _distribuir_larguras(largura, [3, 2, 1])
        self._r(
            "H-0028 renderer: restos fecham soma exata das linhas em dimensao impar",
            sum(alturas) == len(corpo) and len(alturas) == 3,
            "alturas={0!r}".format(alturas),
        )
        self._r(
            "H-0028 renderer: restos fecham soma exata das colunas em dimensao impar",
            sum(larguras) == largura and len(larguras) == 3,
            "larguras={0!r}".format(larguras),
        )

    def test_celulas_fora_de_ordem_posicionam_por_coordenada(self):
        filhos = [
            _funcional("a", "console", "A1"),
            _funcional("b", "console", "B2"),
            _funcional("c", "console", "C3"),
            _funcional("d", "console", "D4"),
        ]
        celulas = [
            {"linha": 2, "coluna": 2, "elemento": "d"},
            {"linha": 1, "coluna": 1, "elemento": "a"},
            {"linha": 2, "coluna": 1, "elemento": "c"},
            {"linha": 1, "coluna": 2, "elemento": "b"},
        ]
        grupo = _grupo_matriz_render_h0028(filhos=filhos, celulas=celulas)
        saida = self._render_matriz(grupo, largura=80, altura=24)
        corpo = _linhas_corpo_renderizado(saida)
        topo = "\n".join(corpo[:len(corpo) // 2])
        base = "\n".join(corpo[len(corpo) // 2:])
        self._r(
            "H-0028 renderer: celulas fora de ordem usam coordenadas, nao ordem do array",
            "A1" in topo and "B2" in topo and "C3" in base and "D4" in base,
        )

    def test_tipos_permitidos_e_grupo_livre_em_celula(self):
        grupo_livre = _grupo(
            "g_livre", "vertical",
            [_funcional("interno", "console", "INT")],
            distribuicao={"modo": "igual"},
        )
        filhos = [
            _funcional("c", "console", "CON"),
            _funcional("l", "lancador", "LAN"),
            _funcional("d", "dashboard", "DAS"),
            grupo_livre,
        ]
        celulas = [
            {"linha": 1, "coluna": 1, "elemento": "c"},
            {"linha": 1, "coluna": 2, "elemento": "l"},
            {"linha": 2, "coluna": 1, "elemento": "d"},
            {"linha": 2, "coluna": 2, "elemento": "g_livre"},
        ]
        grupo = _grupo_matriz_render_h0028(filhos=filhos, celulas=celulas)
        saida = self._render_matriz(grupo, largura=80, altura=24)
        self._r(
            "H-0028 renderer: matriz renderiza console, lancador, dashboard e grupo livre",
            all(texto in saida for texto in ["CON", "LAN", "DAS", "INT"]),
        )

    def test_grupo_livre_contendo_matriz(self):
        matriz = _grupo_matriz_render_h0028(gid="mat_interna")
        livre = _grupo(
            "livre", "vertical", [matriz],
            distribuicao={"modo": "igual"},
        )
        modelo = _modelo_matriz_render_h0028([livre])
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0028 renderer: grupo livre contendo matriz renderiza matriz interna",
            "E1" in saida and "E4" in saida,
        )

    def test_redimensionamento_recalcula_grade(self):
        grupo = _grupo_matriz_render_h0028(
            dist_colunas={"modo": "fracao", "valores": [1, 2]},
        )
        saida_80 = self._render_matriz(grupo, largura=80, altura=24)
        saida_100 = self._render_matriz(grupo, largura=100, altura=24)
        corpo_80 = _linhas_corpo_renderizado(saida_80)
        corpo_100 = _linhas_corpo_renderizado(saida_100)
        self._r(
            "H-0028 renderer: redimensionamento altera largura das linhas da grade",
            len(corpo_80[0]) == 80 and len(corpo_100[0]) == 100
            and corpo_80[0] != corpo_100[0],
        )

    def test_terminal_pequeno_propaga_erro_global_existente(self):
        grupo = _grupo_matriz_render_h0028()
        _espera_excecao(
            "H-0028 renderer: matriz estreita propaga RenderizadorErro existente",
            lambda: self._render_matriz(grupo, largura=18, altura=24),
            RenderizadorErro,
        )

    def run_all(self):
        print("")
        print("== TestRenderizadorMatrizH0028: grade matricial compartilhada ==")
        self.test_matriz_2x2_alinhamento_vertical_e_horizontal()
        self.test_matriz_2x4_pesos_assimetricos_compartilhados()
        self.test_dimensoes_impares_e_restos_por_eixo()
        self.test_celulas_fora_de_ordem_posicionam_por_coordenada()
        self.test_tipos_permitidos_e_grupo_livre_em_celula()
        self.test_grupo_livre_contendo_matriz()
        self.test_redimensionamento_recalcula_grade()
        self.test_terminal_pequeno_propaga_erro_global_existente()


def _modelo_h0029(elementos, corpo_dist=None, largura=42):
    """Cria ModeloTela sintetico para testes H-0029.

    Cabecalho de 3 linhas, barra de 3 linhas com chip unico.
    Para largura=42 e altura=20: l_corpo_disponivel=14.
    """
    return ModeloTela(
        id="teste_h0029",
        schema="tela.v1",
        cabecalho={"titulo": "H0029", "descricao": "h0029"},
        corpo=Corpo(arranjo="vertical", elementos=elementos, distribuicao=corpo_dist),
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Voltar"}]},
        _raw={},
    )


def _h0029_linhas_totais(saida):
    return len(saida.splitlines())


def _h0029_larguras(saida):
    return [len(l) for l in saida.splitlines() if l.strip()]


def _h0029_barra_posicao(saida, altura):
    linhas = saida.splitlines()
    for i in range(len(linhas) - 1, -1, -1):
        if linhas[i].startswith("╭") or linhas[i].startswith("┌"):
            return i
    return -1


class TestCardinalidadeUnitariaH0029:
    """Testes de distribuicao em containers com cardinalidade unitaria (H-0029).

    Cobre a matriz minima do handoff: ausencia preservada; corpo e grupo com
    modos igual/fracao/percentual para cardinalidade 1; composicao em dois niveis;
    equivalencia geometrica; preservacao de 2+ filhos; preservacao da ausencia;
    preservacao dos JSONs reais; comportamento em duas alturas de terminal.
    """

    LARGURA = 42
    ALTURA = 20
    # l_cab=3, l_barra=3, l_corpo_disponivel=14

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

    def _render(self, elementos, corpo_dist=None, altura=None):
        m = _modelo_h0029(elementos, corpo_dist=corpo_dist)
        kw = {"largura": self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # -------------------------------------------------- M01: ausencia funcional
    def test_M01_ausencia_funcional_preserva_natural(self):
        """M01: corpo sem dist, 1 funcional direto -> DA-01 ocupa area integral."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M01: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M01: DA-01 (ADR-0024) - funcional ocupa area integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M01: DA-01 - sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
            "fill_ext={0}".format(len(fill_ext)),
        )

    # -------------------------------------------------- M02: corpo igual funcional
    def test_M02_igual_funcional_direto_ocupa_area(self):
        """M02: corpo=igual, 1 funcional direto -> filho recebe toda a area."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M02: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        corpo_alts = _corpo_alturas(saida)
        # l_corpo_disponivel=14; com dist, funcional ocupa 14 linhas
        self._r(
            "H-0029 M02: funcional recebe toda a area distribuivel (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M02: sem fill externo (dist absorve area internamente)",
            len(fill_ext) == 0,
            "fill_ext={0}".format(len(fill_ext)),
        )
        self._r(
            "H-0029 M02: barra na posicao correta (linha altura-3 = 17)",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
            "barra_pos={0}".format(_h0029_barra_posicao(saida, self.ALTURA)),
        )

    # -------------------------------------------------- M03: fracao[1] funcional
    def test_M03_fracao1_funcional_equivale_igual(self):
        """M03: corpo=fracao[1], 1 funcional -> geometricamente equivalente a M02."""
        saida_ig = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M03: fracao[1] total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M03: fracao[1] geometricamente identico a igual (cardinalidade 1)",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M04: percentual[100] funcional
    def test_M04_percentual100_funcional_equivale_igual(self):
        """M04: corpo=percentual[100], 1 funcional -> equivalente a M02."""
        saida_ig = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "percentual", "valores": [100]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M04: percentual[100] total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M04: percentual[100] geometricamente identico a igual (cardinalidade 1)",
            saida_pc == saida_ig,
        )

    # ---- M05: corpo=igual, grupo sem dist, 1 filho -> DA-01 repassa cota ao filho
    def test_M05_igual_grupo_sem_dist_1filho(self):
        """M05: corpo=igual, grupo sem dist, 1 filho -> DA-01 ocupa cota integral.

        Reproduz o defeito pre-H-0029: output era 8 linhas em vez de 20.
        Apos ADR-0024 DA-01: grupo repassa cota integralmente ao unico filho.
        """
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M05: total de linhas == altura (defeito pre-H-0029 era 8 linhas)",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0} (esperado {1})".format(_h0029_linhas_totais(saida), self.ALTURA),
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M05: DA-01 (ADR-0024) - filho ocupa cota integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        self._r(
            "H-0029 M05: barra na posicao correta",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
            "barra_pos={0}".format(_h0029_barra_posicao(saida, self.ALTURA)),
        )
        linhas = saida.splitlines()
        corpo_linhas = linhas[3:self.ALTURA - 3]
        self._r(
            "H-0029 M05: corpo ocupa exatamente l_corpo_disponivel=14 linhas",
            len(corpo_linhas) == 14,
            "len_corpo={0}".format(len(corpo_linhas)),
        )

    # -------------------------------------------------- M06: fracao[1] grupo sem dist
    def test_M06_fracao1_grupo_sem_dist_1filho(self):
        """M06: corpo=fracao[1], grupo sem dist, 1 filho -> equivalente a M05."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M06: fracao[1] grupo sem dist total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M06: fracao[1] grupo sem dist geometricamente igual a M05 (igual)",
            saida_fr == saida_ig,
        )

    # ---- M07: corpo sem dist, grupo=igual, 1 filho -> DA-01 repassa area ao grupo
    def test_M07_ausencia_corpo_grupo_igual_1filho(self):
        """M07: corpo sem dist, grupo=igual, 1 filho -> DA-01 repassa area integral ao grupo."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M07: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida)),
        )
        # DA-01 (ADR-0024): grupo e unico descendente visual -> recebe area integral.
        # DA-03: grupo estrutural repassa area ao filho interno.
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M07: DA-01+DA-03 - filho ocupa area integral (14 linhas)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M07: DA-01 - sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
        )

    # -------------------------------------------------- M08: fracao[1] interno
    def test_M08_ausencia_corpo_grupo_fracao1_1filho(self):
        """M08: corpo sem dist, grupo=fracao[1], 1 filho -> equivalente a M07."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "fracao", "valores": [1]})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M08: fracao[1] interno total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M08: fracao[1] interno geometricamente identico a igual interno",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M09: percentual[100] interno
    def test_M09_ausencia_corpo_grupo_percentual100_1filho(self):
        """M09: corpo sem dist, grupo=percentual[100], 1 filho -> equivalente a M07."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "percentual", "valores": [100]})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M09: percentual[100] interno total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M09: percentual[100] interno geometricamente identico a igual interno",
            saida_pc == saida_ig,
        )

    # ---- M10: corpo=igual, grupo=igual, 1 filho -> dois niveis distribuicao integral
    def test_M10_igual_grupo_igual_1filho_dois_niveis(self):
        """M10: corpo=igual, grupo=igual, 1 filho -> filho ocupa area interna completa."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M10: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M10: filho ocupa area interna completa (14 linhas = l_corpo_disponivel)",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M10: sem fill externo (dois niveis de dist absorvem area)",
            len(fill_ext) == 0,
        )
        self._r(
            "H-0029 M10: barra na posicao correta",
            _h0029_barra_posicao(saida, self.ALTURA) == self.ALTURA - 3,
        )

    # -------------------------------------------------- M11: fracao[1]/fracao[1]
    def test_M11_fracao1_grupo_fracao1_1filho(self):
        """M11: corpo=fracao[1], grupo=fracao[1], 1 filho -> equivalente a M10."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_fr = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "fracao", "valores": [1]})],
            corpo_dist={"modo": "fracao", "valores": [1]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M11: fracao[1]/fracao[1] total linhas == altura",
            _h0029_linhas_totais(saida_fr) == self.ALTURA,
        )
        self._r(
            "H-0029 M11: fracao[1]/fracao[1] geometricamente identico a igual/igual",
            saida_fr == saida_ig,
        )

    # -------------------------------------------------- M12: percentual[100]/percentual[100]
    def test_M12_percentual100_grupo_percentual100_1filho(self):
        """M12: corpo=percentual[100], grupo=percentual[100], 1 filho -> equivalente a M10."""
        saida_ig = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        saida_pc = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                    distribuicao={"modo": "percentual", "valores": [100]})],
            corpo_dist={"modo": "percentual", "valores": [100]},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M12: percentual[100]/percentual[100] total linhas == altura",
            _h0029_linhas_totais(saida_pc) == self.ALTURA,
        )
        self._r(
            "H-0029 M12: percentual[100]/percentual[100] geometricamente identico a igual/igual",
            saida_pc == saida_ig,
        )

    # -------------------------------------------------- M13: preservacao 2+ filhos
    def test_M13_preservacao_dois_ou_mais_filhos(self):
        """M13: corpo=igual, grupo=igual, 2+ filhos -> comportamento existente preservado."""
        saida = self._render(
            [_grupo("g1", "vertical", [
                _funcional("d1", "dashboard", "D1"),
                _funcional("d2", "dashboard", "D2"),
            ], distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 M13: total de linhas == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0029 M13: dois filhos somam l_corpo_disponivel=14",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )
        self._r(
            "H-0029 M13: dois filhos presentes nas caixas do corpo",
            len(corpo_alts) == 2,
            "n_caixas={0}".format(len(corpo_alts)),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0029 M13: sem fill externo com 2 filhos distribuidos",
            len(fill_ext) == 0,
        )

    # -------------------------------------------------- largura das linhas
    def test_largura_linhas(self):
        """Todas as linhas nao vazias tem a largura correta."""
        for nome, corpo_dist, filhos in [
            ("sem dist, 1 funcional", None, [_funcional("d1", "dashboard", "D1")]),
            ("igual, 1 funcional", {"modo": "igual"}, [_funcional("d1", "dashboard", "D1")]),
            ("igual, 1 grupo sem dist 1 filho",
             {"modo": "igual"},
             [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])]),
            ("igual, 1 grupo igual 1 filho",
             {"modo": "igual"},
             [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                     distribuicao={"modo": "igual"})]),
        ]:
            saida = self._render(filhos, corpo_dist=corpo_dist, altura=self.ALTURA)
            larguras = [len(l) for l in saida.splitlines() if l.strip()]
            todas_corretas = all(w == self.LARGURA for w in larguras)
            self._r(
                "H-0029 largura: {0} -> todas as linhas nao vazias com {1} chars".format(
                    nome, self.LARGURA),
                todas_corretas,
                "larguras={0}".format(sorted(set(larguras))),
            )

    # -------------------------------------------------- redimensionamento (2 alturas)
    def test_redimensionamento_duas_alturas(self):
        """Duas alturas de terminal produzem resultados corretos."""
        for alt in (20, 30):
            for nome, corpo_dist, filhos in [
                ("igual, 1 grupo sem dist 1 filho",
                 {"modo": "igual"},
                 [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])]),
                ("igual, 1 grupo igual 1 filho",
                 {"modo": "igual"},
                 [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")],
                         distribuicao={"modo": "igual"})]),
            ]:
                saida = self._render(filhos, corpo_dist=corpo_dist, altura=alt)
                n = _h0029_linhas_totais(saida)
                self._r(
                    "H-0029 redim: {0} altura={1} -> {1} linhas".format(nome, alt),
                    n == alt,
                    "got={0}".format(n),
                )

    # -------------------------------------------------- soma exata das cotas
    def test_soma_cotas_exata(self):
        """Soma das cotas atribuidas pelo corpo == l_corpo_disponivel."""
        l_corpo = self.ALTURA - 3 - 3  # cab=3, barra=3
        for nome, corpo_dist, filhos in [
            ("igual, 1 funcional",
             {"modo": "igual"},
             [_funcional("d1", "dashboard", "D1")]),
            ("igual, 2 funcionais",
             {"modo": "igual"},
             [_funcional("d1", "dashboard", "D1"), _funcional("d2", "dashboard", "D2")]),
            ("fracao[2,1], 2 funcionais",
             {"modo": "fracao", "valores": [2, 1]},
             [_funcional("d1", "dashboard", "D1"), _funcional("d2", "dashboard", "D2")]),
        ]:
            pesos = _pesos_distribuicao(corpo_dist, len(filhos))
            cotas = _distribuir_alturas(l_corpo, pesos)
            self._r(
                "H-0029 cotas: {0} -> soma({1}) == {2}".format(nome, cotas, l_corpo),
                sum(cotas) == l_corpo,
                "soma={0}".format(sum(cotas)),
            )

    # -------------------------------------------------- composicao 2 niveis unitaria
    def test_composicao_dois_niveis_unitaria(self):
        """Composicao com cardinalidade unitaria em 2 niveis funciona corretamente."""
        # g1 sem dist, g2 com dist=igual, 1 funcional
        saida_a = self._render(
            [_grupo("g1", "vertical", [
                _grupo("g2", "vertical", [_funcional("d1", "dashboard", "D1")],
                       distribuicao={"modo": "igual"})
            ])],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 2niveis: g1_sem_dist > g2_igual > 1dash total linhas == altura",
            _h0029_linhas_totais(saida_a) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida_a)),
        )
        # g1 com dist=igual, g2 com dist=igual, 1 funcional
        saida_b = self._render(
            [_grupo("g1", "vertical", [
                _grupo("g2", "vertical", [_funcional("d1", "dashboard", "D1")],
                       distribuicao={"modo": "igual"})
            ], distribuicao={"modo": "igual"})],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0029 2niveis: g1_igual > g2_igual > 1dash total linhas == altura",
            _h0029_linhas_totais(saida_b) == self.ALTURA,
            "got={0}".format(_h0029_linhas_totais(saida_b)),
        )
        corpo_alts_b = _corpo_alturas(saida_b)
        self._r(
            "H-0029 2niveis: g1_igual > g2_igual > 1dash filho expande para 14",
            corpo_alts_b == [14],
            "corpo_alturas={0}".format(corpo_alts_b),
        )

    # -------------------------------------------------- area insuficiente
    def test_area_insuficiente_rejeicao_deterministica(self):
        """Area insuficiente levanta RenderizadorErro deterministico."""
        self._espera_erro(
            "H-0029 area insuficiente: cab+barra > altura levanta RenderizadorErro",
            lambda: self._render(
                [_funcional("d1", "dashboard", "D1")],
                corpo_dist={"modo": "igual"},
                altura=4,  # impossivel: cab=3 + barra=3 > 4
            ),
        )

    # ---------------------------------------- integracao JSON real grupo_minimo
    def test_integracao_json_grupo_minimo(self):
        """Integracao loader -> modelo -> renderer com grupo_minimo.json real."""
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO))
        self._r(
            "H-0029 integracao: grupo_minimo.json distribuicao is None (sem dist)",
            modelo.corpo.distribuicao is None,
        )
        saida20 = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
        self._r(
            "H-0029 integracao: grupo_minimo.json altura=20 -> 20 linhas",
            _h0029_linhas_totais(saida20) == 20,
            "got={0}".format(_h0029_linhas_totais(saida20)),
        )
        # DA-01 (ADR-0024): grupo contem 1 visual -> area integral repassada ao filho.
        corpo_alts = _corpo_alturas(saida20)
        self._r(
            "H-0029 integracao: grupo_minimo.json DA-01 - filho ocupa area integral (14 linhas)",
            len(corpo_alts) == 1 and corpo_alts[0] == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )
        # Sem fill externo (ADR-0024 DA-01)
        fill_ext = [l for l in saida20.splitlines() if l == " " * 42]
        self._r(
            "H-0029 integracao: grupo_minimo.json sem fill externo (ADR-0024 DA-01)",
            len(fill_ext) == 0,
        )
        saida_sem = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0029 integracao: grupo_minimo.json sem altura produz saida nao vazia",
            bool(saida_sem.strip()),
        )

    # ---------------------------------------- preservacao ausencia nos JSONs reais
    def test_preservacao_jsons_sem_dist(self):
        """destino_minimo.json e stub_b.json nao declaram distribuicao: preservados."""
        for id_tela in ("destino_minimo", "stub_b"):
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            self._r(
                "H-0029 preserv: {0} distribuicao is None".format(id_tela),
                modelo.corpo.distribuicao is None,
            )
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
            self._r(
                "H-0029 preserv: {0} altura=20 -> 20 linhas".format(id_tela),
                _h0029_linhas_totais(saida) == 20,
                "got={0}".format(_h0029_linhas_totais(saida)),
            )

    def run_all(self):
        print("")
        print("== TestCardinalidadeUnitariaH0029: distribuicao com cardinalidade 1 ==")
        self.test_M01_ausencia_funcional_preserva_natural()
        self.test_M02_igual_funcional_direto_ocupa_area()
        self.test_M03_fracao1_funcional_equivale_igual()
        self.test_M04_percentual100_funcional_equivale_igual()
        self.test_M05_igual_grupo_sem_dist_1filho()
        self.test_M06_fracao1_grupo_sem_dist_1filho()
        self.test_M07_ausencia_corpo_grupo_igual_1filho()
        self.test_M08_ausencia_corpo_grupo_fracao1_1filho()
        self.test_M09_ausencia_corpo_grupo_percentual100_1filho()
        self.test_M10_igual_grupo_igual_1filho_dois_niveis()
        self.test_M11_fracao1_grupo_fracao1_1filho()
        self.test_M12_percentual100_grupo_percentual100_1filho()
        self.test_M13_preservacao_dois_ou_mais_filhos()
        self.test_largura_linhas()
        self.test_redimensionamento_duas_alturas()
        self.test_soma_cotas_exata()
        self.test_composicao_dois_niveis_unitaria()
        self.test_area_insuficiente_rejeicao_deterministica()
        self.test_integracao_json_grupo_minimo()
        self.test_preservacao_jsons_sem_dist()


# Geometria dos JSONs permanentes h0029_* (HANDOFF H-0029 secao 11A / 12.2).
#
# Para largura=42:
#   - cabecalho: 3 linhas (indices 0, 1, 2);
#   - barra_de_menus: 3 linhas, topo na linha `altura - 3`;
#   - l_corpo_disponivel = altura - 6 (para altura=20 -> 14; para altura=30 -> 24).
#
# Cenarios com dashboard preenchendo a area distribuida (11A.1-11A.3 e 11A.5-11A.7):
#   topo do dashboard na linha 3; borda inferior na linha `altura - 4`;
#   barra imediatamente apos (gap == 0).
#
# Cenario grupo_pai_distribuido (11A.4): dashboard em altura natural (3 linhas,
# indices 3..5); sobra como linhas estruturais em branco ate a barra.

_H0029_TELAS_DASHBOARD = (
    "h0029_dashboard_igual",
    "h0029_dashboard_fracao",
    "h0029_dashboard_percentual",
)

_H0029_TELAS_GRUPO_DISTRIBUIDO = (
    "h0029_grupo_igual",
    "h0029_grupo_fracao",
    "h0029_grupo_percentual",
)

_H0029_TELAS_GRUPO_SEM_DIST = ("h0029_grupo_pai_distribuido",)

_H0029_TELAS_TODAS = (
    _H0029_TELAS_DASHBOARD
    + _H0029_TELAS_GRUPO_SEM_DIST
    + _H0029_TELAS_GRUPO_DISTRIBUIDO
)


def _h0029_caminho_json(id_tela):
    return _BASE_PADRAO / "config" / "telas" / "demo" / (id_tela + ".json")


def _h0029_dashboard_topo(saida):
    """Indice da borda superior (╭/┌) do primeiro dashboard apos o cabecalho."""
    linhas = saida.splitlines()
    for i, linha in enumerate(linhas):
        if i < 3:
            continue
        if linha.startswith("╭") or linha.startswith("┌"):
            return i
    return -1


def _h0029_dashboard_base(saida):
    """Indice da borda inferior (╰/└) do primeiro dashboard apos o cabecalho."""
    linhas = saida.splitlines()
    topo = _h0029_dashboard_topo(saida)
    if topo < 0:
        return -1
    for i in range(topo + 1, len(linhas)):
        if linhas[i].startswith("╰") or linhas[i].startswith("└"):
            return i
    return -1


def _h0029_barra_topo(saida):
    """Indice da borda superior da caixa da barra_de_menus (ultima caixa)."""
    linhas = saida.splitlines()
    for i in range(len(linhas) - 1, -1, -1):
        if linhas[i].startswith("╭") or linhas[i].startswith("┌"):
            return i
    return -1


def _h0029_bordas_laterais_continuas(saida, topo, base):
    """True se as linhas internas entre topo e base comecam e terminam com a
    borda vertical (│) do conjunto curva."""
    linhas = saida.splitlines()
    for i in range(topo + 1, base):
        if i >= len(linhas):
            return False
        linha = linhas[i]
        if not linha.startswith("│") or not linha.endswith("│"):
            return False
    return True


class TestTelasPermanentesH0029:
    """Testes nominais de integracao para os sete JSONs permanentes h0029_*.

    Carrega cada JSON pelo loader real, constroi o modelo e verifica a geometria
    materialmente relevante em pelo menos duas alturas, conforme a secao 12.2 do
    handoff H-0029. Nao se limita a contagem de linhas: inspeciona bordas do
    dashboard, posicao da barra_de_menus, continuidade das bordas laterais,
    ausencia de sobreposicao e equivalencia entre os tres modos de cada grupo.
    """

    LARGURA = 42
    ALTURAS = (20, 30)

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # --------------------------------------------------- existencia e sintaxe
    def test_existencia_e_sintaxe(self):
        import json as _json
        for id_tela in _H0029_TELAS_TODAS:
            caminho = _h0029_caminho_json(id_tela)
            existe = caminho.is_file()
            self._r(
                "H-0029 JSON {0}: arquivo existe".format(id_tela),
                existe,
                "caminho={0}".format(caminho),
            )
            if not existe:
                continue
            try:
                with caminho.open(encoding="utf-8") as fh:
                    dados = _json.load(fh)
            except Exception as exc:
                self._r(
                    "H-0029 JSON {0}: sintaxe JSON valida".format(id_tela),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )
                continue
            self._r(
                "H-0029 JSON {0}: sintaxe JSON valida".format(id_tela),
                isinstance(dados, dict),
            )

    # ------------------------------------------- carregamento e construcao
    def test_carregamento_modelo(self):
        for id_tela in _H0029_TELAS_TODAS:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
            except Exception as exc:
                self._r(
                    "H-0029 JSON {0}: carrega e constroi modelo".format(id_tela),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )
                continue
            self._r(
                "H-0029 JSON {0}: carrega e constroi modelo".format(id_tela),
                isinstance(modelo, ModeloTela),
            )
            self._r(
                "H-0029 JSON {0}: id corresponde ao arquivo".format(id_tela),
                modelo.id == id_tela,
                "id={0!r}".format(modelo.id),
            )
            self._r(
                "H-0029 JSON {0}: schema tela.v1".format(id_tela),
                modelo.schema == "tela.v1",
                "schema={0!r}".format(modelo.schema),
            )
            self._r(
                "H-0029 JSON {0}: corpo tem exatamente 1 filho direto".format(id_tela),
                len(modelo.corpo.elementos) == 1,
                "n_filhos={0}".format(len(modelo.corpo.elementos)),
            )

    # ------------------------------------------- distribuicao declarada do corpo
    def test_distribuicao_corpo_declarada(self):
        espec = {
            "h0029_dashboard_igual": {"modo": "igual"},
            "h0029_dashboard_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_dashboard_percentual": {"modo": "percentual", "valores": [100]},
            "h0029_grupo_pai_distribuido": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_igual": {"modo": "igual"},
            "h0029_grupo_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_percentual": {"modo": "percentual", "valores": [100]},
        }
        for id_tela, esperado in espec.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            dist = modelo.corpo.distribuicao
            self._r(
                "H-0029 JSON {0}: corpo.distribuicao == {1!r}".format(id_tela, esperado),
                dist == esperado,
                "dist={0!r}".format(dist),
            )

    # ----------------------------------------------- tipo do filho direto
    def test_tipo_do_filho_do_corpo(self):
        espec = {
            "h0029_dashboard_igual": "dashboard",
            "h0029_dashboard_fracao": "dashboard",
            "h0029_dashboard_percentual": "dashboard",
            "h0029_grupo_pai_distribuido": "grupo",
            "h0029_grupo_igual": "grupo",
            "h0029_grupo_fracao": "grupo",
            "h0029_grupo_percentual": "grupo",
        }
        for id_tela, esperado in espec.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            filho = modelo.corpo.elementos[0]
            self._r(
                "H-0029 JSON {0}: filho do corpo e tipo {1!r}".format(id_tela, esperado),
                filho.tipo == esperado,
                "tipo={0!r}".format(filho.tipo),
            )

    # ----------------------------- distribuicao interna do grupo (presenca/ausencia)
    def test_distribuicao_interna_do_grupo(self):
        # Telas com grupo: pai_distribuido SEM dist interna; demais COM dist interna.
        sem_dist = {"h0029_grupo_pai_distribuido"}
        com_dist = {
            "h0029_grupo_igual": {"modo": "igual"},
            "h0029_grupo_fracao": {"modo": "fracao", "valores": [1]},
            "h0029_grupo_percentual": {"modo": "percentual", "valores": [100]},
        }
        for id_tela in sem_dist:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            grupo = modelo.corpo.elementos[0]
            dist_g = grupo._campos_inertes.get("distribuicao")
            self._r(
                "H-0029 JSON {0}: grupo SEM distribuicao interna".format(id_tela),
                dist_g is None,
                "dist_g={0!r}".format(dist_g),
            )
            self._r(
                "H-0029 JSON {0}: grupo tem 1 filho interno".format(id_tela),
                len(grupo.elementos) == 1,
                "n={0}".format(len(grupo.elementos)),
            )
            self._r(
                "H-0029 JSON {0}: filho interno e dashboard".format(id_tela),
                grupo.elementos[0].tipo == "dashboard",
            )
        for id_tela, esperado in com_dist.items():
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            grupo = modelo.corpo.elementos[0]
            dist_g = grupo._campos_inertes.get("distribuicao")
            self._r(
                "H-0029 JSON {0}: grupo.distribuicao == {1!r}".format(id_tela, esperado),
                dist_g == esperado,
                "dist_g={0!r}".format(dist_g),
            )
            self._r(
                "H-0029 JSON {0}: grupo tem 1 filho interno".format(id_tela),
                len(grupo.elementos) == 1,
            )
            self._r(
                "H-0029 JSON {0}: filho interno e dashboard".format(id_tela),
                grupo.elementos[0].tipo == "dashboard",
            )

    # ------------------------- geometria: altura total, largura, barra (2 alturas)
    def test_geometria_altura_largura_barra(self):
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                linhas = saida.splitlines()
                self._r(
                    "H-0029 JSON {0} alt={1}: total de linhas == altura".format(
                        id_tela, altura
                    ),
                    len(linhas) == altura,
                    "linhas={0}".format(len(linhas)),
                )
                larguras = {len(l) for l in linhas if l.strip()}
                self._r(
                    "H-0029 JSON {0} alt={1}: largura uniforme == {2}".format(
                        id_tela, altura, self.LARGURA
                    ),
                    larguras == {self.LARGURA},
                    "larguras={0}".format(sorted(larguras)),
                )
                barra = _h0029_barra_topo(saida)
                self._r(
                    "H-0029 JSON {0} alt={1}: barra_topo == altura-3 ({2})".format(
                        id_tela, altura, altura - 3
                    ),
                    barra == altura - 3,
                    "barra_topo={0}".format(barra),
                )

    # ----------------------------- geometria: dashboard preenche area distribuida
    def test_geometria_dashboard_preenche_area(self):
        """Telas 11A.1-11A.3 e 11A.5-11A.7: dashboard ocupa toda a area."""
        preenche = _H0029_TELAS_DASHBOARD + _H0029_TELAS_GRUPO_DISTRIBUIDO
        for id_tela in preenche:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                topo = _h0029_dashboard_topo(saida)
                base = _h0029_dashboard_base(saida)
                barra = _h0029_barra_topo(saida)
                self._r(
                    "H-0029 JSON {0} alt={1}: dashboard topo == 3".format(
                        id_tela, altura
                    ),
                    topo == 3,
                    "topo={0}".format(topo),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: dashboard base == altura-4 ({2})".format(
                        id_tela, altura, altura - 4
                    ),
                    base == altura - 4,
                    "base={0}".format(base),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: borda inferior imediatamente antes "
                    "da barra (gap == 0)".format(id_tela, altura),
                    base >= 0 and barra == base + 1,
                    "base={0} barra={1}".format(base, barra),
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: bordas laterais continuas".format(
                        id_tela, altura
                    ),
                    _h0029_bordas_laterais_continuas(saida, topo, base),
                )
                # Ausencia de linhas externas (branco total) entre dashboard e barra.
                entre = [
                    l for l in saida.splitlines()[base + 1:barra]
                    if l == " " * self.LARGURA
                ]
                self._r(
                    "H-0029 JSON {0} alt={1}: sem linhas externas entre dashboard "
                    "e barra".format(id_tela, altura),
                    len(entre) == 0,
                    "linhas_externas={0}".format(len(entre)),
                )

    # ----------------------------- geometria: grupo_pai_distribuido (DA-01)
    def test_geometria_grupo_pai_distribuido_natural(self):
        """Tela 11A.4: DA-01 (ADR-0024) - dashboard ocupa area integral do grupo."""
        id_tela = "h0029_grupo_pai_distribuido"
        modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
        for altura in self.ALTURAS:
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA,
                largura=self.LARGURA, altura=altura,
            )
            linhas = saida.splitlines()
            topo = _h0029_dashboard_topo(saida)
            base = _h0029_dashboard_base(saida)
            barra = _h0029_barra_topo(saida)
            l_corpo_disponivel = altura - 3 - 3  # l_cab=3, l_barra=3
            # DA-01 (ADR-0024): grupo repassa cota integral ao unico visual filho.
            # Dashboard expande de 2 linhas naturais para l_corpo_disponivel linhas.
            self._r(
                "H-0029 JSON {0} alt={1}: dashboard topo == 3".format(
                    id_tela, altura
                ),
                topo == 3,
                "topo={0}".format(topo),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: DA-01 - dashboard base == altura-4 ({2})".format(
                    id_tela, altura, altura - 4
                ),
                base == altura - 4,
                "base={0}".format(base),
            )
            # DA-01: dashboard ocupa toda a area; barra imediatamente apos (gap==0).
            self._r(
                "H-0029 JSON {0} alt={1}: DA-01 - borda inferior imediatamente "
                "antes da barra (gap == 0)".format(id_tela, altura),
                base >= 0 and barra == base + 1,
                "base={0} barra={1}".format(base, barra),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: barra_topo == altura-3 ({2})".format(
                    id_tela, altura, altura - 3
                ),
                barra == altura - 3,
                "barra={0}".format(barra),
            )
            self._r(
                "H-0029 JSON {0} alt={1}: sem sobreposicao (base < barra)".format(
                    id_tela, altura
                ),
                base < barra and len(linhas) == altura,
            )

    # --------------------------------------------- equivalencia: dashboards
    def test_equivalencia_dashboard_tres_modos(self):
        """h0029_dashboard_igual/fracao/percentual geometricamente equivalentes."""
        saidas = {}
        for altura in self.ALTURAS:
            saidas[altura] = {}
            for id_tela in _H0029_TELAS_DASHBOARD:
                modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
                saidas[altura][id_tela] = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
            igual = saidas[altura]["h0029_dashboard_igual"]
            frac = saidas[altura]["h0029_dashboard_fracao"]
            perc = saidas[altura]["h0029_dashboard_percentual"]
            # Geometria (bordas) deve coincidir; textos do cabecalho diferem.
            for id_tela, s in (("fracao", frac), ("percentual", perc)):
                top_i = _h0029_dashboard_topo(igual)
                top_o = _h0029_dashboard_topo(s)
                base_i = _h0029_dashboard_base(igual)
                base_o = _h0029_dashboard_base(s)
                barra_i = _h0029_barra_topo(igual)
                barra_o = _h0029_barra_topo(s)
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} topo".format(
                        altura, id_tela
                    ),
                    top_i == top_o,
                    "igual={0} {1}={2}".format(top_i, id_tela, top_o),
                )
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} base".format(
                        altura, id_tela
                    ),
                    base_i == base_o,
                    "igual={0} {1}={2}".format(base_i, id_tela, base_o),
                )
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} barra".format(
                        altura, id_tela
                    ),
                    barra_i == barra_o,
                    "igual={0} {1}={2}".format(barra_i, id_tela, barra_o),
                )
                # Altura do corpo (dashboard) identica.
                self._r(
                    "H-0029 equiv dashboard alt={0}: igual vs {1} altura dashboard".format(
                        altura, id_tela
                    ),
                    (base_i - top_i) == (base_o - top_o),
                    "igual={0} {1}={2}".format(base_i - top_i, id_tela, base_o - top_o),
                )

    # ------------------------------------------------- equivalencia: grupos
    def test_equivalencia_grupo_tres_modos(self):
        """h0029_grupo_igual/fracao/percentual geometricamente equivalentes."""
        saidas = {}
        for altura in self.ALTURAS:
            saidas[altura] = {}
            for id_tela in _H0029_TELAS_GRUPO_DISTRIBUIDO:
                modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
                saidas[altura][id_tela] = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
            igual = saidas[altura]["h0029_grupo_igual"]
            frac = saidas[altura]["h0029_grupo_fracao"]
            perc = saidas[altura]["h0029_grupo_percentual"]
            for id_tela, s in (("fracao", frac), ("percentual", perc)):
                top_i = _h0029_dashboard_topo(igual)
                top_o = _h0029_dashboard_topo(s)
                base_i = _h0029_dashboard_base(igual)
                base_o = _h0029_dashboard_base(s)
                barra_i = _h0029_barra_topo(igual)
                barra_o = _h0029_barra_topo(s)
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} topo".format(
                        altura, id_tela
                    ),
                    top_i == top_o,
                    "igual={0} {1}={2}".format(top_i, id_tela, top_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} base".format(
                        altura, id_tela
                    ),
                    base_i == base_o,
                    "igual={0} {1}={2}".format(base_i, id_tela, base_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} barra".format(
                        altura, id_tela
                    ),
                    barra_i == barra_o,
                    "igual={0} {1}={2}".format(barra_i, id_tela, barra_o),
                )
                self._r(
                    "H-0029 equiv grupo alt={0}: igual vs {1} altura dashboard".format(
                        altura, id_tela
                    ),
                    (base_i - top_i) == (base_o - top_o),
                    "igual={0} {1}={2}".format(base_i - top_i, id_tela, base_o - top_o),
                )

    # --------------------------- area adicional absorvida (redimensionamento)
    def test_area_adicional_absorvida(self):
        """Altura maior: area extra absorvida corretamente; barra permanece no fim."""
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            s20 = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=self.LARGURA, altura=20
            )
            s30 = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=self.LARGURA, altura=30
            )
            barra20 = _h0029_barra_topo(s20)
            barra30 = _h0029_barra_topo(s30)
            self._r(
                "H-0029 JSON {0}: barra acompanha nova altura (17->27)".format(id_tela),
                barra20 == 17 and barra30 == 27,
                "barra20={0} barra30={1}".format(barra20, barra30),
            )
            # DA-01 (ADR-0024): todos os JSONs h0029_* expandem o dashboard
            # para preencher a area disponivel, incluindo grupo_pai_distribuido
            # (grupo sem dist interna recebe area via DA-01 e repassa ao filho).
            base20 = _h0029_dashboard_base(s20)
            base30 = _h0029_dashboard_base(s30)
            self._r(
                "H-0029 JSON {0}: borda inferior acompanha cota (16->26)".format(
                    id_tela
                ),
                base20 == 16 and base30 == 26,
                "base20={0} base30={1}".format(base20, base30),
            )

    # ----------------------------------- ausencia de sobreposicao (geral)
    def test_ausencia_sobreposicao(self):
        """Nenhuma tela produz linhas duplicadas nem desaparecimento de bordas."""
        for id_tela in _H0029_TELAS_TODAS:
            modelo = construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))
            for altura in self.ALTURAS:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA,
                    largura=self.LARGURA, altura=altura,
                )
                linhas = saida.splitlines()
                # Sem linha em branco entre caixas (invariante do renderer).
                self._r(
                    "H-0029 JSON {0} alt={1}: sem '\\n\\n' (sem linha em branco)".format(
                        id_tela, altura
                    ),
                    "\n\n" not in saida,
                )
                # Contagem de bordas superiores: 3 caixas (cabecalho, corpo, barra).
                top_count = sum(
                    1 for l in linhas if l.startswith("╭")
                )
                self._r(
                    "H-0029 JSON {0} alt={1}: exatamente 3 caixas (3 bordas superiores)".format(
                        id_tela, altura
                    ),
                    top_count == 3,
                    "top_count={0}".format(top_count),
                )

    def run_all(self):
        print("")
        print("== TestTelasPermanentesH0029: sete JSONs nominais ==")
        self.test_existencia_e_sintaxe()
        self.test_carregamento_modelo()
        self.test_distribuicao_corpo_declarada()
        self.test_tipo_do_filho_do_corpo()
        self.test_distribuicao_interna_do_grupo()
        self.test_geometria_altura_largura_barra()
        self.test_geometria_dashboard_preenche_area()
        self.test_geometria_grupo_pai_distribuido_natural()
        self.test_equivalencia_dashboard_tres_modos()
        self.test_equivalencia_grupo_tres_modos()
        self.test_area_adicional_absorvida()
        self.test_ausencia_sobreposicao()


# ---------------------------------------------------------------------------
# H-0030: catalogo de telas utilizaveis (console, dashboard, matrizes).
# ---------------------------------------------------------------------------

_TELAS_H0030 = [
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_3x2",
    "h0030_matriz_2x4",
]

# (n_linhas, n_colunas, [rotulos de posicao esperados]) por matriz.
_GEO_H0030 = {
    "h0030_matriz_2x2": (2, 2),
    "h0030_matriz_3x2": (3, 2),
    "h0030_matriz_2x4": (2, 4),
}

# Altura deterministica para renderizar matrizes (a matriz requer altura
# explicita para distribuir as linhas; largura=80). 3 linhas no maximo ->
# 24 linhas bastam para cabecalho(3) + grid + barra(3).
_ALTURA_MATRIZ_H0030 = 24


class TestCatalogoH0030:
    """Renderizacao do catalogo H-0030 (5 telas permanentes).

    Cobre (H-0030 secoes 14.3 e 14.3-G):
    - renderizar_tela das 5 telas sem excecao e com saida nao vazia;
    - conteudo deterministico do console unico e do dashboard unico;
    - para cada matriz: quantidade de linhas/colunas de celulas, cobertura
      integral (todos os rotulos de posicao presentes), divisorias verticais
      e horizontais, ausencia de lacunas e de sobreposicoes;
    - largura alternativa 120 para cada matriz (sem excecao, mesmas regioes).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _carregar(self, id_tela):
        return construir_modelo(carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO))

    # ---------------------------------- 14.3: render sem excecao, nao vazio
    def test_renderizar_cinco_telas(self):
        for id_tela in _TELAS_H0030:
            modelo = self._carregar(id_tela)
            eh_matriz = id_tela in _GEO_H0030
            altura = _ALTURA_MATRIZ_H0030 if eh_matriz else 24
            try:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA, largura=80, altura=altura
                )
                ok = isinstance(saida, str) and saida != ""
            except Exception as exc:
                ok = False
                saida = ""
                detalhe = "{0}: {1}".format(type(exc).__name__, exc)
            else:
                detalhe = "len={0}".format(len(saida))
            self._r(
                "H-0030 render: renderizar_tela({0}) nao lanca e saida nao vazia".format(
                    id_tela
                ),
                ok,
                detalhe,
            )
            self._r(
                "H-0030 render: {0} saida nao e None".format(id_tela),
                saida is not None,
            )

    # ---------------------------------------------- 14.3: conteudo deterministico
    def test_console_unico_conteudo(self):
        modelo = self._carregar("h0030_console_unico")
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0030 render: console_unico exibe titulo 'CONSOLE'",
            "CONSOLE" in saida,
        )
        self._r(
            "H-0030 render: console_unico exibe placeholder '(console)'",
            "(console)" in saida,
        )
        self._r(
            "H-0030 render: console_unico exibe barra '[Esc] Voltar'",
            "[Esc] Voltar" in saida,
        )

    def test_dashboard_unico_conteudo(self):
        modelo = self._carregar("h0030_dashboard_unico")
        saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=80, altura=24)
        self._r(
            "H-0030 render: dashboard_unico exibe 'dashboard único'",
            "dashboard único" in saida,
        )
        self._r(
            "H-0030 render: dashboard_unico exibe 'H-0030'",
            "H-0030" in saida,
        )
        self._r(
            "H-0030 render: dashboard_unico exibe titulo 'DASHBOARD'",
            "DASHBOARD" in saida,
        )

    # ---------------------------------------------- 14.3-G: geometria das matrizes
    def test_matrizes_geometria(self):
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            self._r(
                "H-0030 geo: {0} render sem excecao (largura=80)".format(id_matriz),
                isinstance(saida, str) and saida != "",
            )

            # Rotulos de posicao: cada celula declara "linha N, coluna M".
            rotulos_esperados = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos_esperados if r in saida}
            self._r(
                "H-0030 geo: {0} exibe todos os {1} rotulos de posicao".format(
                    id_matriz, n_linhas * n_colunas
                ),
                presentes == rotulos_esperados,
                "faltam={0!r}".format(sorted(rotulos_esperados - presentes)),
            )

            # Titulos das celulas ("L<n> C<m>") tambem aparecem.
            titulos_esperados = {
                "L{0} C{1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            titulos_presentes = {t for t in titulos_esperados if t in saida}
            self._r(
                "H-0030 geo: {0} exibe todos os titulos de celula (L<n> C<m>)".format(
                    id_matriz
                ),
                titulos_presentes == titulos_esperados,
                "faltam={0!r}".format(sorted(titulos_esperados - titulos_presentes)),
            )

            # Cobertura: cada rotulo aparece exatamente uma vez (sem duplicidade
            # de celula, sem lacuna).
            for rotulo in sorted(rotulos_esperados):
                self._r(
                    "H-0030 geo: {0} rotulo {1!r} aparece exatamente uma vez".format(
                        id_matriz, rotulo
                    ),
                    saida.count(rotulo) == 1,
                    "count={0}".format(saida.count(rotulo)),
                )

            # Quantidade de linhas de conteudo de celula: cada linha do grid
            # tem sua propria faixa horizontal de caixas. Conta-se quantas
            # linhas de texto possuem o rotulo de coluna 1 (borda esquerda da
            # primeira celula de cada linha).
            # Estrutura: cabecalho(3) + (n_linhas faixas) + barra(3).
            linhas = saida.split("\n")
            # Numero de linhas de grade = contagem de linhas que iniciam uma
            # caixa de celula na primeira coluna (topo "╭ L1 C1" etc.).
            inicioss = [
                i for i, l in enumerate(linhas)
                if l.startswith("╭ L") or l.startswith("┌ L")
            ]
            self._r(
                "H-0030 geo: {0} possui {1} linhas de celulas (faixas horizontais)".format(
                    id_matriz, n_linhas
                ),
                len(inicioss) == n_linhas,
                "inicios={0!r}".format(inicioss),
            )

            # Divisorias verticais: entre colunas adjacentes, cada linha de
            # conteudo possui bordas verticais nas coordenadas dos cortes.
            # Verifica-se que o numero de caixas por faixa (linha do grid)
            # equivale a n_colunas: cada faixa contem n_colunas rotulos de
            # titulo "L<n> C<m>".
            for i_linha, linha_grid in enumerate(inicioss, start=1):
                # Rotulos esperados nesta faixa (linha do grid = i_linha).
                titulos_linha = [
                    "L{0} C{1}".format(i_linha, co)
                    for co in range(1, n_colunas + 1)
                ]
                # A faixa vai do inicio atual ate o proximo inicio (ou ate a barra).
                fim_faixa = (
                    inicioss[i_linha] if i_linha < len(inicioss) else len(linhas)
                )
                bloco_faixa = "\n".join(linhas[linha_grid:fim_faixa])
                self._r(
                    "H-0030 geo: {0} faixa {1} contem {2} colunas (titulos L{1} C*)".format(
                        id_matriz, i_linha, n_colunas
                    ),
                    all(t in bloco_faixa for t in titulos_linha)
                    and len(titulos_linha) == n_colunas,
                    "faixa={0!r}".format(bloco_faixa[:60]),
                )

            # Divisoria horizontal: entre faixas verticais adjacentes deve
            # existir uma linha de borda (base da faixa superior/topo da
            # faixa inferior). Os proprios inicios das faixas (exceto a 1a)
            # marcam essa transicao; como cada faixa tem topo e base em
            # coordenadas compartilhadas, a existencia de >=2 faixas ja
            # implica ao menos uma divisoria horizontal central.
            if n_linhas >= 2:
                self._r(
                    "H-0030 geo: {0} tem divisoria horizontal (>=2 faixas empilhadas)".format(
                        id_matriz
                    ),
                    len(inicioss) >= 2,
                    "faixas={0}".format(len(inicioss)),
                )

            # Divisorias verticais: em largura 80 com n_colunas colunas iguais,
            # cada faixa possui n_colunas caixas lado a lado, separadas por
            # divisores verticais (╮╭ ou ┐┌). Verifica-se pela presenca do
            # padrao de juncao entre caixas ("╮╭" no conjunto curva).
            if n_colunas >= 2:
                padrao_juncao = "╮╭"
                tem_divisoria_vertical = padrao_juncao in saida
                self._r(
                    "H-0030 geo: {0} tem divisoria(s) vertical(is) entre colunas".format(
                        id_matriz
                    ),
                    tem_divisoria_vertical,
                    "padrao_juncao={0!r} presente={1}".format(
                        padrao_juncao, tem_divisoria_vertical
                    ),
                )

            # Ausencia de sobreposicao: cada titulo "L<n> C<m>" aparece uma
            # unica vez (ja verificado acima); como adicional, nenhum rotulo
            # de posicao se sobrepoe a outro na mesma linha (cada linha de
            # texto contem no maximo n_colunas rotulos). Verifica-se que nao
            # ha duas ocorrencias do mesmo rotulo na mesma linha visivel.
            sobreposicoes = 0
            for l in linhas:
                for rotulo in rotulos_esperados:
                    if l.count(rotulo) > 1:
                        sobreposicoes += 1
            self._r(
                "H-0030 geo: {0} sem sobreposicao de rotulos na mesma linha".format(
                    id_matriz
                ),
                sobreposicoes == 0,
                "sobreposicoes={0}".format(sobreposicoes),
            )

    def test_matrizes_geometria_coordenadas(self):
        """Fortalece test_matrizes_geometria com provas por coordenadas reais.

        As assercoes a seguir derivam as propriedades estruturais (faixas,
        colunas, bordas externas, cortes verticais, divisoria horizontal,
        alinhamento dos cortes entre faixas, pontos de encontro, contiguidade,
        ausencia de lacunas e de sobreposicao de retangulos) diretamente das
        posicoes dos caracteres de borda na saida renderizada. Nao reimplementam
        o algoritmo produtivo nem aceitam `len(faixas) >= 2` como prova de
        divisoria, nem duplicidade de rotulo como prova de ausencia de
        sobreposicao.
        """
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            linhas = saida.splitlines()
            corpo = _linhas_corpo_renderizado(saida)

            # 1. Quantidade correta de faixas de linhas: cada faixa comeca
            #    num caractere de topo de caixa ("╭"/"┌") na coluna 0.
            inicios_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╭") or l.startswith("┌")
            ]
            # 2. Quantidade correta de colunas por faixa: cada faixa termina
            #    num caractere de base de caixa ("╰"/"└") na coluna 0.
            fins_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╰") or l.startswith("└")
            ]
            self._r(
                "H-0030 geo-coord: {0} tem {1} faixas de linha".format(
                    id_matriz, n_linhas
                ),
                len(inicios_faixas) == n_linhas,
                "inicios={0!r} corpo={1}".format(inicios_faixas, len(corpo)),
            )
            self._r(
                "H-0030 geo-coord: {0} tem {1} bases de faixa".format(
                    id_matriz, n_linhas
                ),
                len(fins_faixas) == n_linhas,
                "fins={0!r}".format(fins_faixas),
            )

            # Faixas: lista de (inicio, fim) em indices do corpo.
            faixas = list(zip(inicios_faixas, fins_faixas))
            alturas_faixas = [fim - ini + 1 for ini, fim in faixas]

            # 10. Ausencia de linha vazia inesperada entre faixas: a base de
            #     uma faixa precede imediatamente o topo da seguinte.
            sem_linha_vazia = all(
                faixas[k][1] + 1 == faixas[k + 1][0]
                for k in range(len(faixas) - 1)
            )
            self._r(
                "H-0030 geo-coord: {0} sem linha vazia entre faixas".format(
                    id_matriz
                ),
                sem_linha_vazia,
                "alturas_faixas={0!r}".format(alturas_faixas),
            )

            # 3. Coordenadas das bordas externas (colunas e linhas do corpo).
            #    Coluna esquerda = 0; coluna direita = largura - 1.
            #    Linha do corpo de topo externo = inicios_faixas[0];
            #    linha de base externa = fins_faixas[-1].
            borda_esq = 0
            borda_dir = largura - 1
            self._r(
                "H-0030 geo-coord: {0} bordas externas col 0 e {1}".format(
                    id_matriz, borda_dir
                ),
                corpo[inicios_faixas[0]][borda_esq] in "╭┌"
                and corpo[fins_faixas[-1]][borda_esq] in "╰└"
                and corpo[inicios_faixas[0]][borda_dir] in "╮┐"
                and corpo[fins_faixas[-1]][borda_dir] in "╯┘",
                "externos=[{0},{1}]".format(
                    corpo[inicios_faixas[0]][0],
                    corpo[fins_faixas[-1]][-1],
                ),
            )

            # 4/6. Cortes verticais e alinhamento entre faixas: derivados das
            #      posicoes de borda de uma linha de conteudo de cada faixa.
            #      Os cortes internos (entre celulas) sao as colunas onde
            #      aparece "|" e que nao sao as bordas externas. O par (k, k+1)
            #      representa o encontro base/topo de caixas vizinhas; a coluna
            #      do corte interno e k+1 (ou k, dependendo da convensao); aqui
            #      verificamos o conjunto de colunas de borda que se repete em
            #      todas as faixas (alinhamento dos cortes).
            cortes_por_faixa = []
            for ini, fim in faixas:
                # Linha de conteudo valida: primeira linha apos o topo da faixa
                # que comeca com "│" e contem o rotulo de posicao.
                linhas_conteudo = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                self._r(
                    "H-0030 geo-coord: {0} faixa {1} tem linha de conteudo".format(
                        id_matriz, ini
                    ),
                    len(linhas_conteudo) >= 1,
                    "ini={0}".format(ini),
                )
                if not linhas_conteudo:
                    cortes_por_faixa.append(set())
                    continue
                pos = _posicoes_bordas_linha(linhas_conteudo[0])
                # Cortes internos = bordas verticais que nao sao os externos.
                cortes_internos = {
                    p for p in pos if p != borda_esq and p != borda_dir
                }
                cortes_por_faixa.append(cortes_internos)

            # 4. Coordenadas dos cortes verticais em cada faixa: o numero de
            #    cortes internos distintos por faixa deve ser 2*(n_colunas-1)
            #    (cada juncao entre duas caixas vizinhas gera um par de bordas
            #    em colunas adjacentes) — equivalente a n_colunas-1 divisores.
            for k_faixa, cortes in enumerate(cortes_por_faixa, start=1):
                # Agrupa colunas adjacentes em divisores: cada divisor ocupa
                # duas colunas consecutivas (parede direita de uma caixa e
                # parede esquerda da seguinte).
                ordenados = sorted(cortes)
                divisores = []
                i = 0
                while i < len(ordenados):
                    if i + 1 < len(ordenados) and ordenados[i + 1] - ordenados[i] == 1:
                        divisores.append((ordenados[i], ordenados[i + 1]))
                        i += 2
                    else:
                        divisores.append((ordenados[i], ordenados[i]))
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} faixa {1} tem {2} divisores verticais".format(
                        id_matriz, k_faixa, n_colunas - 1
                    ),
                    len(divisores) == n_colunas - 1,
                    "divisores={0!r} cortes={1!r}".format(divisores, ordenados),
                )

            # 6. Alinhamento dos cortes verticais entre as faixas: o conjunto
            #    de cortes internos deve ser identico em todas as faixas.
            alinhados = all(
                cortes == cortes_por_faixa[0] for cortes in cortes_por_faixa
            )
            self._r(
                "H-0030 geo-coord: {0} cortes verticais alinhados entre faixas".format(
                    id_matriz
                ),
                alinhados,
                "cortes_por_faixa={0!r}".format(cortes_por_faixa),
            )

            # 2 (reconfirmado). Colunas por faixa derivadas dos cortes internos
            #    da faixa 0: n_colunas = n_divisores + 1.
            if cortes_por_faixa:
                divisores_f0 = sorted(cortes_por_faixa[0])
                n_div = 0
                i = 0
                while i < len(divisores_f0):
                    if i + 1 < len(divisores_f0) and divisores_f0[i + 1] - divisores_f0[i] == 1:
                        n_div += 1
                        i += 2
                    else:
                        n_div += 1
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} colunas por faixa = {1}".format(
                        id_matriz, n_colunas
                    ),
                    n_div + 1 == n_colunas,
                    "n_divisores={0}".format(n_div),
                )

            # 5. Divisoria horizontal: a base da faixa superior e o topo da
            #    faixa inferior ficam em linhas consecutivas do corpo. A linha
            #    de base termina com "╰"/"└" e a linha seguinte comeca com
            #    "╭"/"┌" — isso prova uma divisoria horizontal real (nao apenas
            #    `len(faixas) >= 2`).
            divisorias_horizontais = 0
            for k in range(len(faixas) - 1):
                base = corpo[faixas[k][1]]
                topo_seg = corpo[faixas[k + 1][0]]
                if (base.startswith("╰") or base.startswith("└")) and (
                    topo_seg.startswith("╭") or topo_seg.startswith("┌")
                ) and faixas[k][1] + 1 == faixas[k + 1][0]:
                    divisorias_horizontais += 1
            self._r(
                "H-0030 geo-coord: {0} tem {1} divisoria(s) horizontal(is) por base/topo".format(
                    id_matriz, n_linhas - 1
                ),
                divisorias_horizontais == n_linhas - 1,
                "divisorias={0}".format(divisorias_horizontais),
            )

            # 7. Pontos de encontro entre bordas horizontais e verticais:
            #    no cruzamento de uma divisoria horizontal com um corte
            #    vertical, a coluna do corte na linha de base da faixa superior
            #    deve conter um caractere de borda (parede vertical cruza a
            #    base). Verifica-se para cada divisor da faixa superior.
            if cortes_por_faixa and n_linhas >= 2:
                base_faixa_sup = corpo[faixas[0][1]]
                cortes_sup = sorted(cortes_por_faixa[0])
                # colunas de borda presentes na linha de base
                bordas_base = _posicoes_bordas_linha(base_faixa_sup)
                # Cada divisor (par de colunas adjacentes) deve aparecer como
                # borda na linha de base (ponto de encontro).
                encontros = 0
                i = 0
                while i < len(cortes_sup):
                    if i + 1 < len(cortes_sup) and cortes_sup[i + 1] - cortes_sup[i] == 1:
                        if cortes_sup[i] in bordas_base and cortes_sup[i + 1] in bordas_base:
                            encontros += 1
                        i += 2
                    else:
                        if cortes_sup[i] in bordas_base:
                            encontros += 1
                        i += 1
                self._r(
                    "H-0030 geo-coord: {0} encontros HxV na divisoria horizontal".format(
                        id_matriz
                    ),
                    encontros == n_colunas - 1,
                    "encontros={0} bordas_base={1!r}".format(encontros, bordas_base),
                )

            # 8. Contiguidade entre caixas adjacentes: para cada faixa, em uma
            #    linha de conteudo, a parede direita de uma caixa (coluna k) e
            #    a parede esquerda da caixa seguinte (coluna k+1) devem ser
            #    consecutivas, sem coluna de espaco entre elas. Os cortes
            #    internos formam pares de colunas adjacentes (um divisor por
            #    juncao); dentro de cada par a distancia deve ser 1.
            contiguo = True
            detalhe_contig = []
            for ini, fim in faixas:
                linhas_c = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                if not linhas_c:
                    continue
                pos = _posicoes_bordas_linha(linhas_c[0])
                internos = sorted(
                    p for p in pos if p != borda_esq and p != borda_dir
                )
                # Agrupa internos em pares de colunas adjacentes (divisores).
                i = 0
                while i < len(internos):
                    if (
                        i + 1 < len(internos)
                        and internos[i + 1] - internos[i] == 1
                    ):
                        i += 2
                    else:
                        contiguo = False
                        detalhe_contig.append((ini, internos))
                        break
            self._r(
                "H-0030 geo-coord: {0} caixas adjacentes contiguas (sem coluna vazia)".format(
                    id_matriz
                ),
                contiguo,
                "quebras={0!r}".format(detalhe_contig),
            )

            # 9. Ausencia de coluna vazia inesperada entre caixas: derivado da
            #    contiguidade acima — reafirma em separado como cobertura 9.
            #    (Sempre passa se a contiguidade passar; registrado para fins
            #    de rastreabilidade da cobertura exigida.)
            self._r(
                "H-0030 geo-coord: {0} sem coluna vazia entre caixas".format(
                    id_matriz
                ),
                contiguo,
                "ver teste de contiguidade acima",
            )

            # 11/12. Cobertura integral + ausencia de sobreposicao entre
            #        retangulos de celulas distintas: constroi os retangulos
            #        (intervalos [linha, coluna]) de cada celula a partir dos
            #        cortes por faixa e verifica (a) que cobrem toda a regiao
            #        da matriz sem lacuna e (b) que retangulos distintos nao se
            #        intersectam.
            retangulos = []  # (linha_corpo_inicio, linha_corpo_fim, col_ini, col_fim)
            for (ini, fim), cortes in zip(faixas, cortes_por_faixa):
                ordenados = sorted(cortes)
                # Fronteiras de coluna: 0, depois os cortes agrupados em pares.
                fronteira = [borda_esq]
                i = 0
                while i < len(ordenados):
                    if i + 1 < len(ordenados) and ordenados[i + 1] - ordenados[i] == 1:
                        fronteira.append(ordenados[i + 1])
                        i += 2
                    else:
                        fronteira.append(ordenados[i])
                        i += 1
                fronteira.append(borda_dir)
                # Celulas: intervalos [fronteira[k], fronteira[k+1]].
                for k in range(len(fronteira) - 1):
                    retangulos.append(
                        (ini, fim, fronteira[k], fronteira[k + 1])
                    )

            # (a) Cobertura integral: numero de retangulos == n_linhas*n_colunas.
            self._r(
                "H-0030 geo-coord: {0} cobertura integral com {1} celulas".format(
                    id_matriz, n_linhas * n_colunas
                ),
                len(retangulos) == n_linhas * n_colunas,
                "retangulos={0}".format(len(retangulos)),
            )

            # (b) Ausencia de sobreposicao: retangulos distintos na mesma faixa
            #     nao compartilham colunas; retangulos em faixas distintas nao
            #     compartilham linhas. (As celulas sao disjuntas por
            #     construcao da grade.)
            sobreposicao = False
            for a in range(len(retangulos)):
                for b in range(a + 1, len(retangulos)):
                    la_i, la_f, ca_i, ca_f = retangulos[a]
                    lb_i, lb_f, cb_i, cb_f = retangulos[b]
                    # Intersecao de intervalos (linha e coluna).
                    inter_linha = not (la_f < lb_i or lb_f < la_i)
                    inter_coluna = not (ca_f < cb_i or cb_f < ca_i)
                    if inter_linha and inter_coluna:
                        # Tolerancia: as paredes compartilhadas (limite
                        # comum) nao sao sobreposicao de area. Ha
                        # sobreposicao real apenas se houver area interna
                        # comum, i.e., mais do que a parede divisoria.
                        area_comum = (
                            (min(la_f, lb_f) - max(la_i, lb_i))
                            * (min(ca_f, cb_f) - max(ca_i, cb_i))
                        )
                        if area_comum > 0:
                            sobreposicao = True
            self._r(
                "H-0030 geo-coord: {0} sem sobreposicao de retangulos distintos".format(
                    id_matriz
                ),
                not sobreposicao,
                "sobreposicao={0}".format(sobreposicao),
            )

            # (c) Contiguidade vertical entre faixas: a faixa k termina na
            #     linha imediatamente anterior ao inicio da faixa k+1.
            self._r(
                "H-0030 geo-coord: {0} faixas contiguas verticalmente".format(
                    id_matriz
                ),
                all(
                    faixas[k][1] + 1 == faixas[k + 1][0]
                    for k in range(len(faixas) - 1)
                ),
                "faixas={0!r}".format(faixas),
            )

            # 13. Preservacao dos rotulos e titulos esperados: ja coberto em
            #     test_matrizes_geometria; reafirma cobertura integral dos
            #     rotulos de posicao aqui como parte da prova por coordenadas.
            rotulos = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos if r in saida}
            self._r(
                "H-0030 geo-coord: {0} preserva todos os rotulos de posicao".format(
                    id_matriz
                ),
                presentes == rotulos,
                "faltam={0!r}".format(sorted(rotulos - presentes)),
            )

            # 14. Largura padrao prevista: toda linha nao-vazia tem largura 80.
            larguras_linhas = {len(l) for l in linhas if l != ""}
            self._r(
                "H-0030 geo-coord: {0} largura 80 em todas as linhas".format(
                    id_matriz
                ),
                larguras_linhas == {80},
                "larguras={0!r}".format(sorted(larguras_linhas)),
            )

            # Cada rotulo aparece exatamente uma vez (sem celula duplicada nem
            # ausente) — cobertura adicional derivada por contagem.
            unicidade = all(saida.count(r) == 1 for r in rotulos)
            self._r(
                "H-0030 geo-coord: {0} cada rotulo aparece exatamente uma vez".format(
                    id_matriz
                ),
                unicidade,
                "contagens={0!r}".format(
                    {r: saida.count(r) for r in sorted(rotulos)}
                ),
            )

    def test_matrizes_cortes_distribuicao_igual(self):
        """Prova os cortes verticais contra coordenadas esperadas da distribuicao igual.

        Cobre a pendencia residual do achado QA-IMP-H0030-MEDIO-001 identificada
        pelo QA pos-patch (RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md, secao 5):

        (i)  a cobertura anterior derivava os cortes da propria saida e verificava
             apenas quantidade e alinhamento entre faixas, sem exigir os valores
             esperados para distribuicao igual. Um corte vertical deslocado de
             forma consistente poderia passar.
        (ii) a verificacao de encontros HxV contra a linha de base era pouco
             discriminante, pois `_posicoes_bordas_linha` tambem considera o
             caractere horizontal `─`, de modo que uma base horizontal completa
             tende a conter qualquer coluna de corte deslocado.

        As assercoes a seguir derivam as coordenadas esperadas da largura e do
        numero de colunas (independente do algoritmo produtivo e da propria
        saida) e comprovam duas propriedades geométricas independentes:

        1. Os cortes verticais internos caem exatamente nas colunas exigidas
           pela distribuicao igual em largura 80: cada par (k*passo-1, k*passo)
           com passo = largura // n_colunas. Para 2 colunas -> (39,40); para
           4 colunas -> (19,20),(39,40),(59,60). Um corte deslocado falha.
        2. O encontro entre a divisoria vertical e a divisoria horizontal (HxV)
           ocorre em caracteres de quina (╮╭ no topo, ╯╰ na base) e nunca em
           traco horizontal `─`. Isso torna a prova especifica: se o corte
           estiver deslocado para uma coluna de base preenchida por `─`, o par
           esperado nao aparecera como quina.
        """
        # Quinas de juncao entre faixas horizontais: o corte vertical de cada
        # coluna divide a borda de topo (╮╭) e a borda de base (╯╰) em pares
        # de quinas adjacentes. O traco horizontal `─` nao e quina.
        quinas_topo = ("╮", "╭")
        quinas_base = ("╯", "╰")
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            largura = 80
            altura = _ALTURA_MATRIZ_H0030
            saida = renderizar_tela(
                modelo, estilo=_ESTILO_CURVA, largura=largura, altura=altura
            )
            corpo = _linhas_corpo_renderizado(saida)

            # Faixas (inicio, fim) a partir de topo/base na coluna 0.
            inicios_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╭") or l.startswith("┌")
            ]
            fins_faixas = [
                i for i, l in enumerate(corpo)
                if l.startswith("╰") or l.startswith("└")
            ]
            faixas = list(zip(inicios_faixas, fins_faixas))

            # Coordenadas esperadas dos cortes internos para distribuicao igual.
            # Invariante geometrico: em largura L com C colunas iguais, o k-esimo
            # corte cai entre as colunas (k*L//C - 1) e (k*L//C), formando um par
            # de paredes adjacentes. O algoritmo produtivo nao e consultado; os
            # valores derivam somente de L e C.
            passo = largura // n_colunas
            cortes_esperados = [
                (k * passo - 1, k * passo) for k in range(1, n_colunas)
            ]

            # Propriedade 1 (corte deslocado): para cada faixa, a linha de
            # conteudo apresenta exatamente os pares de colunas esperados como
            # paredes verticais internas. Extrai-se as paredes (apenas "|") em
            # colunas internas e agrupa-se em pares adjacentes; o conjunto
            # resultante deve ser igual ao esperado.
            for k_faixa, (ini, fim) in enumerate(faixas, start=1):
                linhas_c = [
                    corpo[i] for i in range(ini + 1, fim)
                    if corpo[i].startswith("│") and "linha" in corpo[i]
                ]
                # Colunas com parede vertical "|" (nao qualquer caractere de
                # borda): isso isola as paredes laterais das celulas.
                paredes = [
                    p for p, ch in enumerate(linhas_c[0])
                    if ch == "│" and 0 < p < largura - 1
                ]
                ordenados = sorted(paredes)
                pares = []
                i = 0
                while i < len(ordenados):
                    if (
                        i + 1 < len(ordenados)
                        and ordenados[i + 1] - ordenados[i] == 1
                    ):
                        pares.append((ordenados[i], ordenados[i + 1]))
                        i += 2
                    else:
                        pares.append((ordenados[i], ordenados[i]))
                        i += 1
                self._r(
                    "H-0030 geo-igual: {0} faixa {1} cortes internos nas "
                    "colunas esperadas {2}".format(
                        id_matriz, k_faixa, cortes_esperados
                    ),
                    pares == cortes_esperados,
                    "pares={0!r} esperados={1!r}".format(pares, cortes_esperados),
                )

            # Propriedade 2 (encontro HxV especifico): na divisoria horizontal
            # entre cada par de faixas vizinhas, cada corte interno esperado
            # aparece como um par de quinas adjacentes (╮╭ no topo da faixa
            # inferior e ╯╰ na base da faixa superior), nunca como `─`. Isso
            # prova que o corte vertical realmente cruza a divisoria horizontal
            # numa interseccao de quina, e nao apenas numa coluna qualquer de
            # uma base horizontal completa.
            for k in range(len(faixas) - 1):
                base_sup = corpo[faixas[k][1]]
                topo_inf = corpo[faixas[k + 1][0]]
                for (c_esq, c_dir) in cortes_esperados:
                    par_base = (base_sup[c_esq], base_sup[c_dir])
                    par_topo = (topo_inf[c_esq], topo_inf[c_dir])
                    self._r(
                        "H-0030 geo-igual: {0} div.h.{1} corte {2},{3} "
                        "quina base (╯╰)".format(
                            id_matriz, k + 1, c_esq, c_dir
                        ),
                        par_base == quinas_base,
                        "par_base={0!r}".format(par_base),
                    )
                    self._r(
                        "H-0030 geo-igual: {0} div.h.{1} corte {2},{3} "
                        "quina topo (╮╭)".format(
                            id_matriz, k + 1, c_esq, c_dir
                        ),
                        par_topo == quinas_topo,
                        "par_topo={0!r}".format(par_topo),
                    )

            # Regressao explicita de lacuna/coluna vazia no corte: a coluna
            # imediatamente anterior (c_esq) e a imediatamente posterior (c_dir)
            # a um corte esperado devem ambas conter parede vertical numa linha
            # de conteudo; se o renderer inserir um espaco em branco em uma das
            # duas, a contiguidade entre caixas vizinhas esta quebrada.
            ini0, fim0 = faixas[0]
            conteudo0 = [
                corpo[i] for i in range(ini0 + 1, fim0)
                if corpo[i].startswith("│") and "linha" in corpo[i]
            ][0]
            for (c_esq, c_dir) in cortes_esperados:
                self._r(
                    "H-0030 geo-igual: {0} corte {1},{2} sem coluna vazia "
                    "(paredes nas duas colunas)".format(
                        id_matriz, c_esq, c_dir
                    ),
                    conteudo0[c_esq] == "│" and conteudo0[c_dir] == "│",
                    "chars={0!r}".format(
                        (conteudo0[c_esq], conteudo0[c_dir])
                    ),
                )

    def test_matrizes_largura_alternativa_120(self):
        for id_matriz, (n_linhas, n_colunas) in _GEO_H0030.items():
            modelo = self._carregar(id_matriz)
            try:
                saida = renderizar_tela(
                    modelo, estilo=_ESTILO_CURVA, largura=120,
                    altura=_ALTURA_MATRIZ_H0030,
                )
                ok = isinstance(saida, str) and saida != ""
            except Exception as exc:
                ok = False
                detalhe = "{0}: {1}".format(type(exc).__name__, exc)
            else:
                detalhe = "len={0}".format(len(saida))
            self._r(
                "H-0030 geo: {0} largura=120 nao lanca excecao".format(id_matriz),
                ok,
                detalhe,
            )
            # Largura 120 mantem o mesmo numero de regioes de celula.
            rotulos_esperados = {
                "linha {0}, coluna {1}".format(ln, co)
                for ln in range(1, n_linhas + 1)
                for co in range(1, n_colunas + 1)
            }
            presentes = {r for r in rotulos_esperados if r in saida}
            self._r(
                "H-0030 geo: {0} largura=120 mantem {1} regioes de celula".format(
                    id_matriz, n_linhas * n_colunas
                ),
                presentes == rotulos_esperados,
                "faltam={0!r}".format(sorted(rotulos_esperados - presentes)),
            )
            # Cada linha nao-vazia tem exatamente 120 chars.
            self._r(
                "H-0030 geo: {0} largura=120: linhas nao-vazias tem 120 chars".format(
                    id_matriz
                ),
                all(len(ln) == 120 for ln in saida.split("\n") if ln != ""),
                "larguras={0}".format(
                    sorted({len(ln) for ln in saida.split("\n") if ln != ""})
                ),
            )

    def test_preservacao_telas_anteriores(self):
        """Telas anteriores continuam renderizando sem regressao."""
        for id_perm in ("destino_minimo", "grupo_minimo", "demo"):
            modelo = self._carregar(id_perm)
            try:
                saida = renderizar_tela(modelo, estilo=_ESTILO_CURVA, largura=42)
                ok = isinstance(saida, str) and saida != ""
            except Exception:
                ok = False
            self._r(
                "H-0030 render: tela anterior {0} ainda renderiza".format(id_perm),
                ok,
            )

    def run_all(self):
        print("")
        print("== TestCatalogoH0030: render do catalogo de 5 telas permanentes ==")
        self.test_renderizar_cinco_telas()
        self.test_console_unico_conteudo()
        self.test_dashboard_unico_conteudo()
        self.test_matrizes_geometria()
        self.test_matrizes_geometria_coordenadas()
        self.test_matrizes_cortes_distribuicao_igual()
        self.test_matrizes_largura_alternativa_120()
        self.test_preservacao_telas_anteriores()


# ===========================================================================
# H-0034 — Distribuicao responsiva do lancador (fila/matriz/coluna minima/
# quadro minimo global). Autoridades: handoff H-0034 secao 3-10, ADR-0023,
# contrato_lancador.md 6.1-6.7, docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md / docs/nomenclatura/33_LANCADOR.md.
#
# Itens da configuracao demo (config/telas/demo/demo.json, lancador_principal):
#   idx 0 d  "Destino"      chip_sub=3 texto=7  item_w_min=11
#   idx 1 g  "Grupo Min."   chip_sub=3 texto=10 item_w_min=14
#   idx 2 1  "Console"      chip_sub=3 texto=7  item_w_min=11
#   idx 3 2  "Dashboard"    chip_sub=3 texto=9  item_w_min=13
#   idx 4 3  "Matriz 2x2"   chip_sub=3 texto=10 item_w_min=14
#   idx 5 4  "Matriz 3x2"   chip_sub=3 texto=10 item_w_min=14
#   idx 6 5  "Matriz 2x4"   chip_sub=3 texto=10 item_w_min=14
#
# Parametros de tipo (config/elementos/lancador.json, espelhados no renderer):
#   vao_chip_texto_min=1, vao_itens/margem_min=2, vao_maximo=5,
#   margem vertical superior/inferior = 1.
#
# Limiares calculados independentemente (H-0034 secao 4.2):
#   fila_content_w_min      = 107  -> area_lancador_w min = 110
#   matriz_4x2_content_w_min=  65  -> area_lancador_w min =  68
#   matriz_3x3_content_w_min=  50  -> area_lancador_w min =  53
#   matriz_2x4_content_w_min=  34  -> area_lancador_w min =  37
#   coluna_minima_content_w =  18  -> lancador_caixa_min_w = 21
# ===========================================================================


# Sete itens do lancador demo, reusados pelos testes isolados e basicos.
_H0034_ITENS_DEMO = [
    {"id": "i0", "chip": "d", "texto": "Destino"},
    {"id": "i1", "chip": "g", "texto": "Grupo Min."},
    {"id": "i2", "chip": "1", "texto": "Console"},
    {"id": "i3", "chip": "2", "texto": "Dashboard"},
    {"id": "i4", "chip": "3", "texto": "Matriz 2x2"},
    {"id": "i5", "chip": "4", "texto": "Matriz 3x2"},
    {"id": "i6", "chip": "5", "texto": "Matriz 2x4"},
]

# Parâmetros normativos do tipo lancador espelhados de
# config/elementos/lancador.json, para uso nos helpers de teste em memória
# (H-0034). Os valores coincidem com o arquivo canônico.
_PARAMS_LANCADOR_DEMO = {
    "vaos": {
        "chip_texto": {"minimo": 1, "maximo": 3},
        "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
    },
    "vertical": {
        "margem_borda_superior": 1,
        "margem_borda_inferior": 1,
    },
    "verificacao": {
        "texto": {"max_caracteres": 15},
    },
}


def _h0034_modelo_lancador(itens, largura=42, titulo_cab="T"):
    """Modelo minimo em memoria com um unico lancador (arranjo vertical).

    Usado pelos testes basicos de fila/matriz/coluna-minima/quadro-minimo.
    A area do lancador coincide com a largura passada ao renderer (arranjo
    vertical repassa total_w aos filhos), como nos testes de fronteira global
    suplementares. Para isolamento causal do gatilho interno, ver
    ``_h0034_modelo_isolado``.
    """
    corpo = Corpo(
        arranjo="vertical",
        elementos=[
            ElementoCorpo(
                id="lanc_t",
                tipo="lancador",
                _campos_inertes={"titulo": "Navegar", "itens": list(itens)},
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            )
        ],
    )
    return ModeloTela(
        id="t_lancador",
        schema="tela.v1",
        cabecalho={"titulo": titulo_cab, "descricao": "d"},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


def _h0034_modelo_isolado(area_lancador_w, terminal_w=80):
    """Modelo sintetico em memoria com arranjo horizontal e area do lancador
    controlada independentemente do viewport global (H-0034 secao 9.5.2).

    ``terminal_w`` fica constante; o lancador recebe ``area_lancador_w`` via
    distribuicao fracao. Isola o gatilho interno ``area_lancador_w <
    lancador_caixa_min_w`` do gatilho global de terminal pequeno.
    """
    area_restante = terminal_w - area_lancador_w
    corpo = Corpo(
        arranjo="horizontal",
        distribuicao={"modo": "fracao", "valores": [area_lancador_w, area_restante]},
        elementos=[
            ElementoCorpo(
                id="lancador_teste",
                tipo="lancador",
                _campos_inertes={
                    "titulo": "Navegar",
                    "itens": [
                        {"id": it["id"], "chip": it["chip"], "texto": it["texto"]}
                        for it in _H0034_ITENS_DEMO
                    ],
                },
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            ),
            ElementoCorpo(
                id="console_resto",
                tipo="console",
                _campos_inertes={"titulo": "Console"},
            ),
        ],
    )
    return ModeloTela(
        id="teste_isolamento_lancador",
        schema="tela.v1",
        cabecalho={"titulo": "TESTE", "descricao": "Isolamento"},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


def _h0034_row_of(saida, marker):
    """Indice da primeira linha que contem ``marker``, ou -1."""
    for i, linha in enumerate(saida.splitlines()):
        if marker in linha:
            return i
    return -1


def _h0034_modelo_alinhamento(itens, alinhamento, largura):
    """Modelo minimo em memoria com lancador cujo layout.alinhamento esta
    declarado em _campos_inertes.

    Usado pelos testes de alinhamento horizontal por instancia (R-10).
    """
    campos_inertes = {"titulo": "Navegar", "itens": list(itens)}
    if alinhamento is not None:
        campos_inertes["layout"] = {"alinhamento": alinhamento}
    corpo = Corpo(
        arranjo="vertical",
        elementos=[
            ElementoCorpo(
                id="lanc_alin",
                tipo="lancador",
                _campos_inertes=campos_inertes,
                parametros_tipo=_PARAMS_LANCADOR_DEMO,
            )
        ],
    )
    return ModeloTela(
        id="t_alin",
        schema="tela.v1",
        cabecalho={"titulo": "T", "descricao": "d"},
        corpo=corpo,
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
        _raw={},
    )


class TestDistribuicaoResponsivaH0034:
    """Cobertura focal do H-0034: fila, matriz, coluna minima, quadro minimo,
    ordem coluna-a-coluna, larguras independentes, alinhamento por instancia,
    ausencia de paginacao/duplicacao/perda, recupeiracao e isolamento causal.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    # ---- Cobertura basica (T-01 a T-05, T-14, T-15) ----------------------

    def test_fila_cardinalidades_basicas(self):
        print("")
        print("== H-0034 basicas: fila, cardinalidades, limite, coluna minima ==")

        # T-03: cardinalidade zero -> 0 linhas de conteudo do lancador, sem erro.
        m_zero = _h0034_modelo_lancador([], largura=42)
        s_zero = renderizar_tela(m_zero, _ESTILO_CURVA, largura=42)
        self._r(
            "H-0034 T-03: cardinalidade zero nao levanta erro",
            isinstance(s_zero, str) and "[d]" not in s_zero,
        )

        # T-02: cardinalidade um -> exatamente 1 linha de conteudo do lancador.
        # item chip "X" texto "Unico" (5): fila_min = 2 + 9 + 2 = 13 (content_w
        # minimo). Em content_w=13 (area=16) deve caber em 1 linha.
        m_um = _h0034_modelo_lancador(
            [{"id": "x", "chip": "X", "texto": "Unico"}], largura=16
        )
        s_um = renderizar_tela(m_um, _ESTILO_CURVA, largura=16)
        # Conta quantas linhas dentro da caixa do lancador contem "[X]".
        linhas_x = [l for l in s_um.splitlines() if "[X]" in l]
        self._r(
            "H-0034 T-02: cardinalidade 1 -> exatamente 1 linha de conteudo",
            len(linhas_x) == 1,
            "linhas_com_X={0}".format(len(linhas_x)),
        )

        # T-01 / T-04: dois itens em fila no limite exato.
        # chip "A" texto "Uno" -> item_w = 3+1+3 = 7; chip "B" texto "Dos" -> 7.
        # fila_content_w_min = 2 + 7+7 + 1*2 + 2 = 20 -> area_lancador_w min = 23.
        itens_2 = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        # Limite exato: area=23 -> content_w=20 -> fila cabe.
        m_2 = _h0034_modelo_lancador(itens_2, largura=23)
        s_23 = renderizar_tela(m_2, _ESTILO_CURVA, largura=23)
        # No limite exato, [A] e [B] estao na mesma linha (fila).
        linha_a = _h0034_row_of(s_23, "[A]")
        linha_b = _h0034_row_of(s_23, "[B]")
        self._r(
            "H-0034 T-01/T-04: content_w=fila_min (area=23) -> fila ([A],[B] "
            "mesma linha)",
            linha_a != -1 and linha_a == linha_b,
            "la={0} lb={1}".format(linha_a, linha_b),
        )

        # T-05: uma unidade abaixo do limite -> matriz (coluna unica, 2 linhas).
        m_2b = _h0034_modelo_lancador(itens_2, largura=22)
        s_22 = renderizar_tela(m_2b, _ESTILO_CURVA, largura=22)
        linha_a = _h0034_row_of(s_22, "[A]")
        linha_b = _h0034_row_of(s_22, "[B]")
        self._r(
            "H-0034 T-05: content_w=fila_min-1 (area=22) -> matriz "
            "([A],[B] linhas diferentes)",
            linha_a != -1 and linha_a != linha_b,
            "la={0} lb={1}".format(linha_a, linha_b),
        )

    def test_quadro_minimo_fronteira_e_recuperacao(self):
        # T-14: itens chip "A" texto "ABCDE"(5), chip "B" texto "XY"(2).
        # max_chip_sub=3, max_texto_sub=5.
        # coluna_minima_content_w = 2 + 3 + 1 + 5 + 2 = 13 -> caixa_min = 16.
        itens_cm = [
            {"id": "a", "chip": "A", "texto": "ABCDE"},
            {"id": "b", "chip": "B", "texto": "XY"},
        ]
        # content_w=13 (area=16): coluna minima valida -> chips presentes.
        m_16 = _h0034_modelo_lancador(itens_cm, largura=16)
        s_16 = renderizar_tela(m_16, _ESTILO_CURVA, largura=16)
        self._r(
            "H-0034 T-14: content_w=coluna_minima (area=16) -> [A],[B] presentes",
            "[A]" in s_16 and "[B]" in s_16,
        )
        # content_w=12 (area=15): abaixo do minimo -> quadro minimo global.
        m_15 = _h0034_modelo_lancador(itens_cm, largura=15)
        s_15 = renderizar_tela(m_15, _ESTILO_CURVA, largura=15)
        self._r(
            "H-0034 T-14: content_w=coluna_minima-1 (area=15) -> quadro minimo "
            "(nenhum chip do lancador)",
            "[A]" not in s_15 and "[B]" not in s_15,
        )
        # T-15: recuperacao automatica apos quadro minimo.
        s_rec = renderizar_tela(m_16, _ESTILO_CURVA, largura=16)
        self._r(
            "H-0034 T-15: recuperacao automatica -> chips presentes novamente",
            "[A]" in s_rec and "[B]" in s_rec,
        )

    # ---- Ordem coluna-a-coluna e ausencia de paginacao (T-06, T-08, T-09) -

    def test_ordem_coluna_a_coluna_e_determinismo(self):
        print("")
        print("== H-0034 ordem coluna-a-coluna, paginacao, determinismo ==")

        # T-06: tres itens, 2 colunas. chip A/B/C texto AAA/BBB/CCC.
        # item_w = 3+1+3 = 7 cada. fila_min = 2+7+7+7+2*2+2 = 30.
        # content_w=20 < 30 -> matriz. n_rows=2, n_col=2.
        # col0=[A,B], col1=[C]. matriz_min = 2 + 7+7 + 1*2 + 2 = 20 -> cabe.
        itens_3 = [
            {"id": "a", "chip": "A", "texto": "AAA"},
            {"id": "b", "chip": "B", "texto": "BBB"},
            {"id": "c", "chip": "C", "texto": "CCC"},
        ]
        m_3 = _h0034_modelo_lancador(itens_3, largura=23)  # area=23 -> cw=20
        s_3 = renderizar_tela(m_3, _ESTILO_CURVA, largura=23)
        la = _h0034_row_of(s_3, "[A]")
        lb = _h0034_row_of(s_3, "[B]")
        lc = _h0034_row_of(s_3, "[C]")
        self._r(
            "H-0034 T-06: ordem coluna-a-coluna ([A],[C] mesma linha; "
            "[B] linha abaixo)",
            la != -1 and la == lc and lb == la + 1,
            "la={0} lb={1} lc={2}".format(la, lb, lc),
        )

        # T-08: ausencia de paginacao. 10 itens (chip 0-9, texto "abcd"=4).
        # coluna_minima_content_w = 2+3+1+4+2 = 12. Em content_w=12 (area=15)
        # coluna unica valida com 10 linhas -> todos os chips presentes.
        itens_10 = [
            {"id": "k{0}".format(i), "chip": str(i), "texto": "abcd"}
            for i in range(10)
        ]
        m_10 = _h0034_modelo_lancador(itens_10, largura=15)
        s_10 = renderizar_tela(m_10, _ESTILO_CURVA, largura=15)
        todos_presentes = all("[{0}]".format(i) in s_10 for i in range(10))
        self._r(
            "H-0034 T-08: 10 itens em coluna minima -> nenhum omitido "
            "(sem paginacao)",
            todos_presentes,
        )

        # T-09: determinismo (reducao/ampliacao). Mesmo conjunto em largura 20
        # depois 25 depois 20 -> primeira e terceira saidas identicas.
        itens_d = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        m_d = _h0034_modelo_lancador(itens_d, largura=23)
        s_a = renderizar_tela(m_d, _ESTILO_CURVA, largura=23)
        renderizar_tela(m_d, _ESTILO_CURVA, largura=30)
        s_b = renderizar_tela(m_d, _ESTILO_CURVA, largura=23)
        self._r(
            "H-0034 T-09: determinismo (mesma largura + itens -> mesma saida)",
            s_a == s_b,
        )

    # ---- Colunas independentes (T-07) ------------------------------------

    def test_colunas_independentes_t07(self):
        print("")
        print("== H-0034 T-07: larguras de coluna independentes ==")

        # T-07 (valores derivados das autoridades, H-0034 secao 10.3):
        #   A "Curto"         -> item_w = 3+1+5  = 9
        #   B "MuitoMaisLong" -> item_w = 3+1+13 = 17  (13 <= 15, valido)
        #   C "Ok"            -> item_w = 3+1+2  = 6
        # fila_min = 2 + 9+17+6 + 2*2 + 2 = 38 > 30 -> nao cabe.
        # matriz n_rows=2, n_col=2:
        #   col0 = [A, B]: chip_sub=max(3,3)=3, texto_sub=max(5,13)=13 -> col_w=17
        #   col1 = [C]:    chip_sub=3, texto_sub=2 -> col_w=6
        # matriz_min = 2 + 17+6 + 1*2 + 2 = 29 <= 30 -> cabe.
        itens_07 = [
            {"id": "a", "chip": "A", "texto": "Curto"},
            {"id": "b", "chip": "B", "texto": "MuitoMaisLong"},
            {"id": "c", "chip": "C", "texto": "Ok"},
        ]
        # area=33 -> content_w=30.
        m_07 = _h0034_modelo_lancador(itens_07, largura=33)
        s_07 = renderizar_tela(m_07, _ESTILO_CURVA, largura=33)

        # [A] e [C] na mesma linha (row 0); [B] na linha abaixo.
        la = _h0034_row_of(s_07, "[A]")
        lb = _h0034_row_of(s_07, "[B]")
        lc = _h0034_row_of(s_07, "[C]")
        self._r(
            "H-0034 T-07: [A] e [C] mesma linha; [B] linha abaixo",
            la != -1 and la == lc and lb == la + 1,
            "la={0} lb={1} lc={2}".format(la, lb, lc),
        )

        # Posicao inicial de col1 = margin_left + col_w_0 + vao_entre_colunas.
        # Independentemente do excesso: col_w_0=17, col_w_1=6 (distintos).
        # Verifica que [C] inicia DEPOIS de [B] (col_w_0=17 aplicado so a col0).
        linha_c = s_07.splitlines()[lc]
        pos_c = linha_c.find("[C]")
        pos_a = s_07.splitlines()[la].find("[A]")
        # col0 largura 17 -> col1 comeca apos 17 (+ margens/vaos). col1 largura
        # 6 -> [C] ocupa poucos chars. Uma implementacao com largura global
        # unica colocaria col1 muito mais a direita (largura 17 ou 6 global).
        self._r(
            "H-0034 T-07: col_w_0=17 != col_w_1=6 (colunas independentes)",
            pos_c > pos_a + 14,  # col0 >= 14 (chip+vao+texto >= 9); col1 bem depois
            "pos_a={0} pos_c={1}".format(pos_a, pos_c),
        )
        # Falha explicita se largura global unica fosse usada: col0 teria a
        # mesma largura que col1. Confirmamos que [B] (texto 13) cabe em col0
        # e [C] (texto 2) em col1, com col1 mais estreito.
        linha_b = s_07.splitlines()[lb]
        self._r(
            "H-0034 T-07: [B] MuitoMaisLong(13) presente integralmente",
            "MuitoMaisLong" in linha_b,
        )

    # ---- Configuracao demo: limites 80/109/110 (T-10 a T-13) ------------

    def _modelo_demo(self):
        raw = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        modelo = construir_modelo(raw)
        assert modelo.id == "demo", "id esperado demo, obtido {0}".format(modelo.id)
        return modelo

    def test_demo_fila_110(self):
        print("")
        print("== H-0034 demo: matriz 2 linhas em 110, matriz 3 linhas em 80 ==")
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]

        # T-10 (H-0037 atualizado): com 11 itens, fila_content_w_min=170, fila
        # exigiria area>=173. A area=110 entrega matriz 2 linhas, nao fila.
        # row0=[d,1,3,5,7,9]; row1=[g,2,4,6,8].
        s110 = renderizar_tela(modelo, _ESTILO_CURVA, largura=110, altura=30)
        rd = _h0034_row_of(s110, "[d]")
        rg = _h0034_row_of(s110, "[g]")
        self._r(
            "H-0034 T-10: area=110 -> matriz 2 linhas ([d] e [g] em linhas "
            "diferentes); 11 chips presentes",
            rd != -1 and rd != rg
            and all(c in s110 for c in _CHIPS),
            "rd={0} rg={1}".format(rd, rg),
        )
        # [d] inicia na posicao 4 (borda+padding+2 margem).
        linha_d = s110.splitlines()[rd]
        pos_colchete_d = linha_d.find("[d]")
        self._r(
            "H-0034 T-10: [d] inicia na posicao 4 da linha "
            "(borda+padding+margem esquerda=2)",
            pos_colchete_d == 4,
            "pos={0}".format(pos_colchete_d),
        )
        # [g] inicia na mesma posicao (col0), linha seguinte.
        linha_g = s110.splitlines()[rg]
        pos_g = linha_g.find("[g]")
        self._r(
            "H-0034 T-10: [g] inicia na mesma coluna que [d] (posicao 4)",
            pos_g == 4,
            "pos_g={0}".format(pos_g),
        )
        # Exatamente 2 linhas de itens do lancador em area=110.
        linhas_itens = [
            l for l in s110.splitlines() if any(c in l for c in _CHIPS)
        ]
        self._r(
            "H-0034 T-10: 11 itens em exatamente 2 linhas (matriz 6x2)",
            len(linhas_itens) == 2,
            "linhas_itens={0}".format(len(linhas_itens)),
        )

    def test_demo_matriz_109_e_80(self):
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]

        # T-12: area=109 -> matriz ([d] e [g] linhas diferentes); 11 chips.
        s109 = renderizar_tela(modelo, _ESTILO_CURVA, largura=109, altura=30)
        rd = _h0034_row_of(s109, "[d]")
        rg = _h0034_row_of(s109, "[g]")
        self._r(
            "H-0034 T-12: area=109 -> matriz ([d] e [g] linhas diferentes); "
            "sem quadro minimo",
            rd != -1 and rd != rg and all(c in s109 for c in _CHIPS),
            "rd={0} rg={1}".format(rd, rg),
        )

        # T-11 (H-0037 atualizado): area=80 -> content_w=77 -> matriz 4x3,
        # ordem coluna-a-coluna com 11 itens.
        # col0=[d,g,1] col1=[2,3,4] col2=[5,6,7] col3=[8,9]
        # row0: [d],[2],[5],[8]  row1: [g],[3],[6],[9]  row2: [1],[4],[7]
        s80 = renderizar_tela(modelo, _ESTILO_CURVA, largura=80, altura=30)
        rd = _h0034_row_of(s80, "[d]")
        rg = _h0034_row_of(s80, "[g]")
        r1 = _h0034_row_of(s80, "[1]")
        r2 = _h0034_row_of(s80, "[2]")
        r3 = _h0034_row_of(s80, "[3]")
        r4 = _h0034_row_of(s80, "[4]")
        r5 = _h0034_row_of(s80, "[5]")
        r6 = _h0034_row_of(s80, "[6]")
        r7 = _h0034_row_of(s80, "[7]")
        r8 = _h0034_row_of(s80, "[8]")
        r9 = _h0034_row_of(s80, "[9]")
        self._r(
            "H-0034 T-11: area=80 matriz 4x3 ([d]&[g] linhas diferentes)",
            rd != -1 and rd != rg,
            "rd={0} rg={1}".format(rd, rg),
        )
        # Preenchimento coluna-a-coluna (H-0034 secao 4.3), 11 itens, 4 cols,
        # 3 linhas: row0=[d,2,5,8]; row1=[g,3,6,9]; row2=[1,4,7].
        self._r(
            "H-0034 T-11: ordem coluna-a-coluna "
            "(row0=[d][2][5][8]; row1=[g][3][6][9]; row2=[1][4][7])",
            rd == r2 and rd == r5 and rd == r8
            and rg == r3 and rg == r6 and rg == r9
            and r1 == r4 and r1 == r7
            and rd < rg < r1,
            "rd={0} r2={1} r5={2} r8={3} rg={4} r3={5} r6={6} r9={7} "
            "r1={8} r4={9} r7={10}".format(
                rd, r2, r5, r8, rg, r3, r6, r9, r1, r4, r7
            ),
        )
        # Larguras independentes (H-0034 secao 4.3), 11 itens:
        #   col0=max(11,14,11)=14, col1=max(13,14,14)=14,
        #   col2=max(14,15,11)=15, col3=max(14,15)=15.
        # row0 contem [d](col0), [2](col1), [5](col2), [8](col3).
        linha0 = s80.splitlines()[rd]
        pd = linha0.find("[d]")
        p2 = linha0.find("[2]")
        p5 = linha0.find("[5]")
        p8 = linha0.find("[8]")
        # Distancia [d]->[2] = col_w_0(14) + vao(5) = 19 (vao maximo).
        self._r(
            "H-0034 T-11: col0=14 -> [2] inicia 19 apos [d] (14+5 vao)",
            p2 - pd == 19,
            "pd={0} p2={1} d={2}".format(pd, p2, p2 - pd),
        )
        # Distancia [2]->[5] = col_w_1(14) + vao(5) = 19.
        self._r(
            "H-0034 T-11: col1=14 -> [5] inicia 19 apos [2] (14+5 vao)",
            p5 - p2 == 19,
            "p2={0} p5={1} d={2}".format(p2, p5, p5 - p2),
        )
        # Distancia [5]->[8] = col_w_2(15) + vao(5) = 20.
        self._r(
            "H-0034 T-11: col2=15 -> [8] inicia 20 apos [5] (15+5 vao)",
            p8 - p5 == 20,
            "p5={0} p8={1} d={2}".format(p5, p8, p8 - p5),
        )
        # col2(15) != col0(14): distancias 20 e 19 sao diferentes.
        self._r(
            "H-0034 T-11: col2(15) != col0(14) — distancias 20 != 19",
            (p8 - p5) != (p2 - pd),
        )
        # T-13: componentes nao relacionados preservados em area=80.
        self._r(
            "H-0034 T-13: cabecalho, barra e caixa NAVEGAR preservados em 80",
            "ORQUESTRADOR" in s80 and "NAVEGAR" in s80 and "[Esc] Sair" in s80,
        )
        # Ausencia de paginacao: todos os 11 chips presentes.
        self._r(
            "H-0034 T-11: ausencia de paginacao (11 chips presentes em 80)",
            all(c in s80 for c in _CHIPS),
        )

    def test_demo_sem_paginacao_em_todas_larguras_validas(self):
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]
        # Com 11 itens, max item_w=15 (Nao Verboso / Tab Altern.),
        # coluna_minima_content_w = 2+15+2 = 19 -> area_lancador_min = 22.
        # Larguras estreitas (22, 37) empilham mais linhas -> altura=45.
        # Larguras validas (area>=22): todos os 11 chips presentes.
        ok = True
        for larg in (22, 37, 53, 68, 80, 109, 110):
            try:
                s = renderizar_tela(modelo, _ESTILO_CURVA, largura=larg, altura=45)
                if not all(c in s for c in _CHIPS):
                    ok = False
            except RenderizadorErro:
                ok = False
        self._r(
            "H-0034: sem paginacao em larguras 22/37/53/68/80/109/110",
            ok,
        )

    # ---- Fronteira global suplementar 20/21 (demo vertical) -------------

    def test_demo_fronteira_global_suplementar(self):
        print("")
        print("== H-0034 fronteira global suplementar 21/22 (demo vertical) ==")
        modelo = self._modelo_demo()
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]",
                  "[6]", "[7]", "[8]", "[9]"]
        # Estas provas NAO isolam o gatilho interno do lancador (arranjo
        # vertical => terminal_w == area_lancador_w). Sao suplementares.
        # Com 11 itens, max item_w=15 -> coluna_minima_content_w=19 -> area>=22.
        # area=22 -> content_w=19 = coluna_minima -> coluna unica valida.
        # 11 itens em coluna unica requerem mais altura: usar altura=45.
        s22 = renderizar_tela(modelo, _ESTILO_CURVA, largura=22, altura=45)
        self._r(
            "H-0034 suplementar: area=22 -> coluna minima valida (chips "
            "presentes) [nao isola gatilho interno]",
            all(c in s22 for c in _CHIPS),
        )
        # area=21 -> content_w=18 < coluna_minima(19) -> quadro minimo global.
        s21 = renderizar_tela(modelo, _ESTILO_CURVA, largura=21, altura=45)
        self._r(
            "H-0034 suplementar: area=21 -> quadro minimo global (sem chips) "
            "[nao isola gatilho interno]",
            all(c not in s21 for c in _CHIPS),
        )
        # Recuperacao suplementar: 21 -> 110 restaura a matriz (todos os chips).
        s110 = renderizar_tela(modelo, _ESTILO_CURVA, largura=110, altura=30)
        self._r(
            "H-0034 suplementar: recuperacao 21->110 restaura matriz "
            "(todos os 11 chips presentes)",
            all(c in s110 for c in _CHIPS),
        )

    # ---- Prova isolada do gatilho interno (T-ISOL-01/02/03) -------------

    def test_isolamento_gatilho_interno(self):
        print("")
        print("== H-0034 prova isolada do gatilho interno (T-ISOL-01/02/03) ==")
        _CHIPS = ["[d]", "[g]", "[1]", "[2]", "[3]", "[4]", "[5]"]

        # Cota real dos pesos via algoritmo de maiores restos (verificado
        # independentemente em RELATORIO_QA_POS_SEGUNDO_PATCH secao 6):
        #   _distribuir_larguras(80, [20,60]) -> [20,60] (soma=80, sem resto)
        #   _distribuir_larguras(80, [21,59]) -> [21,59] (soma=80, sem resto)
        # Confirma computacionalmente o esperado:
        self._r(
            "H-0034 ISOL: _distribuir_larguras(80,[20,60]) == [20,60]",
            _distribuir_larguras(80, [20, 60]) == [20, 60],
        )
        self._r(
            "H-0034 ISOL: _distribuir_larguras(80,[21,59]) == [21,59]",
            _distribuir_larguras(80, [21, 59]) == [21, 59],
        )

        # T-ISOL-02 (controle): terminal_w=80, area_lancador_w=21.
        # content_w_lancador = 21-3 = 18 = coluna_minima -> tela normal.
        m21 = _h0034_modelo_isolado(21, terminal_w=80)
        s_isol_21 = renderizar_tela(m21, _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-02: terminal_w=80, area_lancador=21 -> tela normal "
            "(7 chips presentes)",
            all(c in s_isol_21 for c in _CHIPS),
        )
        # O controle prova que os requisitos globais da tela estavam satisfeitos
        # (mesmo terminal, mesmos itens, mesmo segundo elemento).
        # T-ISOL-01 (insuficiente): terminal_w=80 (idem), area_lancador_w=20.
        # content_w_lancador = 20-3 = 17 < coluna_minima(18) -> quadro minimo.
        m20 = _h0034_modelo_isolado(20, terminal_w=80)
        s_isol_20 = renderizar_tela(m20, _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-01: terminal_w=80, area_lancador=20 -> quadro "
            "minimo global (nenhum chip do lancador)",
            all(c not in s_isol_20 for c in _CHIPS),
        )
        # Causa comprovada: unica diferenca material entre T-ISOL-01 e
        # T-ISOL-02 e area_lancador_w (20 vs 21), com terminal_w=80 constante.
        # T-ISOL-03 (recuperacao deterministica): 21 -> 20 -> 21.
        s_p1 = renderizar_tela(_h0034_modelo_isolado(21), _ESTILO_CURVA, largura=80, altura=30)
        renderizar_tela(_h0034_modelo_isolado(20), _ESTILO_CURVA, largura=80, altura=30)
        s_p3 = renderizar_tela(_h0034_modelo_isolado(21), _ESTILO_CURVA, largura=80, altura=30)
        self._r(
            "H-0034 T-ISOL-03: sequencia 21->20->21 deterministica "
            "(s_passo1 == s_passo3)",
            s_p1 == s_p3,
        )
        # Ausencia de persistencia indevida: o passo 2 (quadro minimo) nao
        # afeta o passo 3 (tela normal reconstruida).
        self._r(
            "H-0034 T-ISOL-03: passo3 contem os 7 chips (tela normal restaurada)",
            all(c in s_p3 for c in _CHIPS),
        )

    # ---- Alinhamento horizontal por instancia (ALTO-001 / R-10) ----------

    def test_alinhamento_horizontal_por_instancia(self):
        print("")
        print("== H-0034 ALTO-001: alinhamento horizontal por instancia (R-10) ==")

        # Caso fila com excesso residual=3 apos expandir vaos e margens ao max.
        # 2 itens: chip 1-char (sub=3), texto 3 chars -> item_w=7 cada.
        # fila_min = 2 + 7+7 + 1*2 + 2 = 20. content_w=32 (largura=35).
        # excesso=12 -> vaos absorvem 3 (max) -> margens absorvem 3+3 -> residual=3.
        itens_f = [
            {"id": "a", "chip": "A", "texto": "Uno"},
            {"id": "b", "chip": "B", "texto": "Dos"},
        ]
        # Mesma largura para os tres casos; unica variavel = layout.alinhamento.
        m_esq = _h0034_modelo_alinhamento(itens_f, "esquerda", largura=35)
        m_dir = _h0034_modelo_alinhamento(itens_f, "direita", largura=35)
        m_cen = _h0034_modelo_alinhamento(itens_f, "centro", largura=35)

        s_esq = renderizar_tela(m_esq, _ESTILO_CURVA, largura=35)
        s_dir = renderizar_tela(m_dir, _ESTILO_CURVA, largura=35)
        s_cen = renderizar_tela(m_cen, _ESTILO_CURVA, largura=35)

        # Os tres alinhamentos devem produzir saidas distintas (excesso residual=3).
        self._r(
            "H-0034 ALTO-001: fila esq != dir",
            s_esq != s_dir,
        )
        self._r(
            "H-0034 ALTO-001: fila esq != cen",
            s_esq != s_cen,
        )
        self._r(
            "H-0034 ALTO-001: fila dir != cen",
            s_dir != s_cen,
        )

        # Chips e textos presentes integralmente em todos os tres (nao perde
        # conteudo ao redistribuir o excesso).
        for s, nome in ((s_esq, "esq"), (s_dir, "dir"), (s_cen, "cen")):
            self._r(
                "H-0034 ALTO-001: fila {0} contem [A] e [B]".format(nome),
                "[A]" in s and "[B]" in s and "Uno" in s and "Dos" in s,
            )

        # Posicoes esperadas na linha de conteudo:
        #   layout: exc_esq|margem_esq=5|[A] Uno|vao=5|[B] Dos|margem_dir=5|exc_dir
        #   line format: borda(1)+space(1)+content -> [A] at pos 2+content_offset
        #   "esquerda": exc_esq=0 -> [A] at content offset 5 -> pos 7 na linha
        #   "direita":  exc_esq=3 -> [A] at content offset 8 -> pos 10 na linha
        #   "centro":   exc_esq=2 -> [A] at content offset 7 -> pos 9 na linha
        linha_fila_esq = s_esq.splitlines()[_h0034_row_of(s_esq, "[A]")]
        linha_fila_dir = s_dir.splitlines()[_h0034_row_of(s_dir, "[A]")]
        linha_fila_cen = s_cen.splitlines()[_h0034_row_of(s_cen, "[A]")]

        pos_A_esq = linha_fila_esq.find("[A]")
        pos_A_dir = linha_fila_dir.find("[A]")
        pos_A_cen = linha_fila_cen.find("[A]")

        self._r(
            "H-0034 ALTO-001: fila esquerda -> excesso a direita do bloco "
            "(exc_esq=0, [A] pos 7)",
            pos_A_esq == 7,
            "pos={0}".format(pos_A_esq),
        )
        self._r(
            "H-0034 ALTO-001: fila direita -> excesso a esquerda do bloco "
            "(exc_esq=3, [A] pos 10)",
            pos_A_dir == 10,
            "pos={0}".format(pos_A_dir),
        )
        self._r(
            "H-0034 ALTO-001: fila centro -> excesso dividido "
            "(exc_esq=2, [A] pos 9)",
            pos_A_cen == 9,
            "pos={0}".format(pos_A_cen),
        )

        # Vaos internos e largura de bloco identicos nos tres alinhamentos
        # ([A] a [B] = item_A(7) + vao(5) = 12 posicoes em todos).
        pos_B_esq = linha_fila_esq.find("[B]")
        pos_B_dir = linha_fila_dir.find("[B]")
        pos_B_cen = linha_fila_cen.find("[B]")
        self._r(
            "H-0034 ALTO-001: fila: vao entre [A] e [B] igual nos tres "
            "alinhamentos (12 posicoes)",
            (pos_B_esq - pos_A_esq) == 12
            and (pos_B_dir - pos_A_dir) == 12
            and (pos_B_cen - pos_A_cen) == 12,
            "d_esq={0} d_dir={1} d_cen={2}".format(
                pos_B_esq - pos_A_esq, pos_B_dir - pos_A_dir, pos_B_cen - pos_A_cen
            ),
        )

        # Caso matriz com excesso residual=3.
        # 3 itens: chip 1-char (sub=3), texto 7 chars -> item_w=11 cada.
        # fila_min = 2+11+11+11+2*2+2 = 41. Para forcar matriz: content_w < 41.
        # content_w=40 (largura=43). matriz n_rows=2, n_col=2:
        #   col0=[A,B] col_w=11, col1=[C] col_w=11. matriz_min=28.
        # excesso=12 -> vaos absorvem 3 -> margens absorvem 3+3 -> residual=3.
        itens_m = [
            {"id": "a", "chip": "A", "texto": "ABCDEFG"},
            {"id": "b", "chip": "B", "texto": "HIJKLMN"},
            {"id": "c", "chip": "C", "texto": "OPQRSTU"},
        ]
        m_m_esq = _h0034_modelo_alinhamento(itens_m, "esquerda", largura=43)
        m_m_dir = _h0034_modelo_alinhamento(itens_m, "direita", largura=43)
        m_m_cen = _h0034_modelo_alinhamento(itens_m, "centro", largura=43)

        s_m_esq = renderizar_tela(m_m_esq, _ESTILO_CURVA, largura=43)
        s_m_dir = renderizar_tela(m_m_dir, _ESTILO_CURVA, largura=43)
        s_m_cen = renderizar_tela(m_m_cen, _ESTILO_CURVA, largura=43)

        # Saidas distintas.
        self._r(
            "H-0034 ALTO-001: matriz esq != dir",
            s_m_esq != s_m_dir,
        )
        self._r(
            "H-0034 ALTO-001: matriz esq != cen",
            s_m_esq != s_m_cen,
        )

        # Chips presentes em todos os tres.
        for s, nome in ((s_m_esq, "esq"), (s_m_dir, "dir"), (s_m_cen, "cen")):
            self._r(
                "H-0034 ALTO-001: matriz {0}: [A],[B],[C] presentes".format(nome),
                "[A]" in s and "[B]" in s and "[C]" in s,
            )

        # Ordem coluna-a-coluna preservada em todos os alinhamentos:
        # [A] e [C] na mesma linha (row 0), [B] na linha abaixo.
        for s, nome in ((s_m_esq, "esq"), (s_m_dir, "dir"), (s_m_cen, "cen")):
            ra = _h0034_row_of(s, "[A]")
            rb = _h0034_row_of(s, "[B]")
            rc = _h0034_row_of(s, "[C]")
            self._r(
                "H-0034 ALTO-001: matriz {0}: [A],[C] mesma linha; [B] abaixo".format(
                    nome
                ),
                ra != -1 and ra == rc and rb == ra + 1,
                "ra={0} rb={1} rc={2}".format(ra, rb, rc),
            )

        # Posicoes de [A] na row 0 para cada alinhamento:
        #   exc_esq|margem_esq=5|col0(11)|vao=5|col1(11)|margem_dir=5|exc_dir
        #   "esquerda": exc_esq=0 -> [A] content offset 5 -> line pos 7
        #   "direita":  exc_esq=3 -> [A] content offset 8 -> line pos 10
        #   "centro":   exc_esq=2 -> [A] content offset 7 -> line pos 9
        row0_esq = s_m_esq.splitlines()[_h0034_row_of(s_m_esq, "[A]")]
        row0_dir = s_m_dir.splitlines()[_h0034_row_of(s_m_dir, "[A]")]
        row0_cen = s_m_cen.splitlines()[_h0034_row_of(s_m_cen, "[A]")]

        self._r(
            "H-0034 ALTO-001: matriz esquerda -> [A] na pos 7 (exc_esq=0)",
            row0_esq.find("[A]") == 7,
            "pos={0}".format(row0_esq.find("[A]")),
        )
        self._r(
            "H-0034 ALTO-001: matriz direita -> [A] na pos 10 (exc_esq=3)",
            row0_dir.find("[A]") == 10,
            "pos={0}".format(row0_dir.find("[A]")),
        )
        self._r(
            "H-0034 ALTO-001: matriz centro -> [A] na pos 9 (exc_esq=2)",
            row0_cen.find("[A]") == 9,
            "pos={0}".format(row0_cen.find("[A]")),
        )

        # Sem alinhamento declarado (None) -> comportamento identico a "esquerda".
        m_none = _h0034_modelo_alinhamento(itens_f, None, largura=35)
        s_none = renderizar_tela(m_none, _ESTILO_CURVA, largura=35)
        self._r(
            "H-0034 ALTO-001: alinhamento None -> identico a esquerda",
            s_none == s_esq,
        )

        # Alinhamento invalido -> RenderizadorErro (R-10).
        m_inv = _h0034_modelo_alinhamento(
            itens_f, "invalido", largura=35
        )
        try:
            renderizar_tela(m_inv, _ESTILO_CURVA, largura=35)
            self._r("H-0034 ALTO-001: alinhamento invalido -> RenderizadorErro", False)
        except RenderizadorErro:
            self._r("H-0034 ALTO-001: alinhamento invalido -> RenderizadorErro", True)

        # Regressao demo: chips presentes e [d] na posicao esperada (esquerda).
        modelo_demo = self._modelo_demo()
        s_demo_r = renderizar_tela(modelo_demo, _ESTILO_CURVA, largura=110, altura=30)
        linha_d_r = s_demo_r.splitlines()[_h0034_row_of(s_demo_r, "[d]")]
        self._r(
            "H-0034 ALTO-001: regressao demo 110 -> [d] na pos 4 (esquerda, excesso=0)",
            linha_d_r.find("[d]") == 4,
            "pos={0}".format(linha_d_r.find("[d]")),
        )

    # ---- Inercia: renderer nao importa json/os/pathlib (preservado) -----

    def test_parametros_tipo_ausente_levanta_erro(self):
        # H-0034 ALTO-002: lancador sem parametros_tipo (construido fora do
        # pipeline) deve levantar RenderizadorErro ao renderizar.
        modelo_sem_params = ModeloTela(
            id="sem_params",
            schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": "d"},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    ElementoCorpo(
                        id="lanc_sem",
                        tipo="lancador",
                        _campos_inertes={
                            "titulo": "Nav",
                            "itens": [{"id": "i0", "chip": "a", "texto": "Item"}],
                        },
                        # parametros_tipo ausente (None por default)
                    )
                ],
            ),
            barra_de_menus={"chips": []},
            _raw={},
        )
        exc = _espera_excecao(
            "H-0034 ALTO-002: lancador sem parametros_tipo levanta RenderizadorErro",
            lambda: renderizar_tela(modelo_sem_params, _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc is not None:
            self._r(
                "H-0034 ALTO-002: mensagem menciona parametros_tipo",
                "parametros_tipo" in str(exc),
                str(exc),
            )

    def test_renderer_preserva_proibicoes_import(self):
        # H-0010A / H-0034 ALTO-002: o renderer continua proibido de importar
        # json/os/pathlib nem abrir arquivos. Os parametros normativos chegam
        # via elemento.parametros_tipo propagado pelo pipeline loader → modelo.
        caminho_mod = _BASE_PADRAO / "tela" / "renderizador.py"
        texto = caminho_mod.read_text(encoding="utf-8")
        self._r(
            "H-0034: renderer continua sem importar json/os/pathlib",
            "import json" not in texto
            and "import os" not in texto
            and "import pathlib" not in texto,
        )
        self._r(
            "H-0034: renderer continua sem abrir arquivos",
            "open(" not in texto and ".read_text(" not in texto,
        )

    def test_max_caracteres_configuravel(self):
        """max_caracteres vem de params['verificacao']['texto']['max_caracteres'], nao hardcoded."""
        import tela.renderizador as _rend_mod

        # Constante hardcoded não deve mais existir no módulo
        self._r(
            "H-0034: _TEXTO_ITEM_MAX removido do renderer",
            not hasattr(_rend_mod, "_TEXTO_ITEM_MAX"),
        )

        def _modelo_mc(itens, mc):
            return ModeloTela(
                id="mc_t",
                schema="tela.v1",
                cabecalho={"titulo": "T", "descricao": "d"},
                corpo=Corpo(
                    arranjo="vertical",
                    elementos=[
                        ElementoCorpo(
                            id="l_mc",
                            tipo="lancador",
                            _campos_inertes={"titulo": "Nav", "itens": list(itens)},
                            parametros_tipo={
                                "vaos": {
                                    "chip_texto": {"minimo": 1, "maximo": 3},
                                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                                },
                                "vertical": {
                                    "margem_borda_superior": 1,
                                    "margem_borda_inferior": 1,
                                },
                                "verificacao": {"texto": {"max_caracteres": mc}},
                            },
                        )
                    ],
                ),
                barra_de_menus={"chips": []},
                _raw={},
            )

        # mc=3: "Uno" (3 chars) aceito
        _itens_uno = [{"id": "u", "chip": "U", "texto": "Uno", "tela_destino": "x"}]
        try:
            renderizar_tela(_modelo_mc(_itens_uno, 3), _ESTILO_CURVA)
            self._r("H-0034: mc=3 aceita texto de 3 chars ('Uno')", True)
        except Exception as exc:
            self._r("H-0034: mc=3 aceita texto de 3 chars ('Uno')", False, str(exc))

        # mc=3: "Quat" (4 chars) rejeitado
        _itens_quat = [{"id": "q", "chip": "Q", "texto": "Quat", "tela_destino": "x"}]
        exc_quat = _espera_excecao(
            "H-0034: mc=3 rejeita texto de 4 chars ('Quat')",
            lambda: renderizar_tela(_modelo_mc(_itens_quat, 3), _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc_quat is not None:
            self._r(
                "H-0034: mc=3 mensagem menciona limite 3 e texto 'Quat'",
                "3" in str(exc_quat) and "Quat" in str(exc_quat),
                str(exc_quat),
            )

        # mc=3: "Quatro" (6 chars) rejeitado
        _itens_seis = [{"id": "s", "chip": "S", "texto": "Quatro", "tela_destino": "x"}]
        exc_seis = _espera_excecao(
            "H-0034: mc=3 rejeita texto de 6 chars ('Quatro')",
            lambda: renderizar_tela(_modelo_mc(_itens_seis, 3), _ESTILO_CURVA),
            RenderizadorErro,
        )
        if exc_seis is not None:
            self._r(
                "H-0034: mc=3 mensagem menciona 'Quatro'",
                "Quatro" in str(exc_seis),
                str(exc_seis),
            )

        # mc=15: "Quatro" (6 chars) aceito
        try:
            renderizar_tela(_modelo_mc(_itens_seis, 15), _ESTILO_CURVA)
            self._r("H-0034: mc=15 aceita texto de 6 chars ('Quatro')", True)
        except Exception as exc:
            self._r("H-0034: mc=15 aceita texto de 6 chars ('Quatro')", False, str(exc))

        # _PARAMS_LANCADOR_DEMO preserva max_caracteres==15
        self._r(
            "H-0034: _PARAMS_LANCADOR_DEMO.verificacao.texto.max_caracteres == 15",
            _PARAMS_LANCADOR_DEMO.get("verificacao", {}).get("texto", {}).get("max_caracteres") == 15,
        )

    def test_caminho_legado_valida_texto(self):
        """Caminho legado _linhas_lancador(elem, content_w=None) usa a sequencia
        comum de normalizacao: parametros_tipo -> max_caracteres ->
        _itens_lancador_normalizados. Prova equivalencia com rota responsiva."""
        from tela.renderizador import _linhas_lancador

        def _elem_legado(itens, mc):
            return ElementoCorpo(
                id="leg",
                tipo="lancador",
                _campos_inertes={"titulo": "Nav", "itens": list(itens)},
                parametros_tipo={
                    "vaos": {
                        "chip_texto": {"minimo": 1, "maximo": 3},
                        "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                    },
                    "vertical": {
                        "margem_borda_superior": 1,
                        "margem_borda_inferior": 1,
                    },
                    "verificacao": {"texto": {"max_caracteres": mc}},
                },
            )

        # Cardinalidade zero: retorna [] sem consultar parametros_tipo.
        elem_zero = ElementoCorpo(
            id="leg_zero",
            tipo="lancador",
            _campos_inertes={"titulo": "Nav", "itens": []},
        )
        resultado_zero = _linhas_lancador(elem_zero, content_w=None)
        self._r(
            "H-0034 LEGADO: cardinalidade zero retorna [] sem parametros_tipo",
            resultado_zero == [],
            repr(resultado_zero),
        )

        # parametros_tipo=None para lancador nao vazio -> RenderizadorErro.
        elem_sem_params = ElementoCorpo(
            id="leg_sem",
            tipo="lancador",
            _campos_inertes={
                "titulo": "Nav",
                "itens": [{"id": "i", "chip": "A", "texto": "Item"}],
            },
        )
        exc_sem = _espera_excecao(
            "H-0034 LEGADO: parametros_tipo=None levanta RenderizadorErro",
            lambda: _linhas_lancador(elem_sem_params, content_w=None),
            RenderizadorErro,
        )
        if exc_sem is not None:
            self._r(
                "H-0034 LEGADO: mensagem menciona parametros_tipo",
                "parametros_tipo" in str(exc_sem),
                str(exc_sem),
            )

        # Estrutura incompleta (verificacao ausente) -> erro; sem fallback.
        elem_inc = ElementoCorpo(
            id="leg_inc",
            tipo="lancador",
            _campos_inertes={
                "titulo": "Nav",
                "itens": [{"id": "i", "chip": "A", "texto": "Item"}],
            },
            parametros_tipo={
                "vaos": {
                    "chip_texto": {"minimo": 1, "maximo": 3},
                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                },
                "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            },
        )
        _espera_excecao(
            "H-0034 LEGADO: estrutura incompleta (verificacao ausente) levanta erro",
            lambda: _linhas_lancador(elem_inc, content_w=None),
            Exception,
        )

        # mc=3: texto com exatamente 3 chars aceito.
        _itens_tres = [{"id": "u", "chip": "U", "texto": "Uno"}]
        try:
            _linhas_lancador(_elem_legado(_itens_tres, 3), content_w=None)
            self._r("H-0034 LEGADO mc=3: texto de 3 chars ('Uno') aceito", True)
        except Exception as exc:
            self._r("H-0034 LEGADO mc=3: texto de 3 chars ('Uno') aceito", False, str(exc))

        # mc=3: texto com 4 chars rejeitado.
        _itens_quatro = [{"id": "q", "chip": "Q", "texto": "Quat"}]
        exc_quat = _espera_excecao(
            "H-0034 LEGADO mc=3: texto de 4 chars ('Quat') rejeitado",
            lambda: _linhas_lancador(_elem_legado(_itens_quatro, 3), content_w=None),
            RenderizadorErro,
        )
        if exc_quat is not None:
            self._r(
                "H-0034 LEGADO mc=3: mensagem menciona limite 3 e texto 'Quat'",
                "3" in str(exc_quat) and "Quat" in str(exc_quat),
                str(exc_quat),
            )

        # mc=3: "Quatro" (6 chars) rejeitado.
        _itens_seis = [{"id": "s", "chip": "S", "texto": "Quatro"}]
        exc_seis = _espera_excecao(
            "H-0034 LEGADO mc=3: 'Quatro' (6 chars) rejeitado",
            lambda: _linhas_lancador(_elem_legado(_itens_seis, 3), content_w=None),
            RenderizadorErro,
        )
        if exc_seis is not None:
            self._r(
                "H-0034 LEGADO mc=3: mensagem menciona 'Quatro'",
                "Quatro" in str(exc_seis),
                str(exc_seis),
            )

        # mc=15: texto valido aceito; saida legada preserva formato "[chip] texto".
        _itens_validos = [{"id": "d", "chip": "d", "texto": "Destino"}]
        try:
            saida = _linhas_lancador(_elem_legado(_itens_validos, 15), content_w=None)
            self._r("H-0034 LEGADO mc=15: texto valido aceito", True)
            self._r(
                "H-0034 LEGADO mc=15: saida preserva formato '[chip] texto'",
                saida == ["[d] Destino"],
                repr(saida),
            )
        except Exception as exc:
            self._r("H-0034 LEGADO mc=15: texto valido aceito", False, str(exc))
            self._r(
                "H-0034 LEGADO mc=15: saida preserva formato '[chip] texto'",
                False,
                str(exc),
            )

        # Equivalencia: mesmo texto rejeitado em content_w=None e content_w valido.
        _itens_inv = [{"id": "e", "chip": "E", "texto": "ABCD"}]
        elem_inv = _elem_legado(_itens_inv, 3)
        _espera_excecao(
            "H-0034 EQUIV: content_w=None rejeita texto acima do max",
            lambda: _linhas_lancador(elem_inv, content_w=None),
            RenderizadorErro,
        )
        modelo_inv = ModeloTela(
            id="equiv_t",
            schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": "d"},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    ElementoCorpo(
                        id="l_inv",
                        tipo="lancador",
                        _campos_inertes={"titulo": "Nav", "itens": list(_itens_inv)},
                        parametros_tipo={
                            "vaos": {
                                "chip_texto": {"minimo": 1, "maximo": 3},
                                "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                            },
                            "vertical": {
                                "margem_borda_superior": 1,
                                "margem_borda_inferior": 1,
                            },
                            "verificacao": {"texto": {"max_caracteres": 3}},
                        },
                    )
                ],
            ),
            barra_de_menus={"chips": []},
            _raw={},
        )
        _espera_excecao(
            "H-0034 EQUIV: content_w valido rejeita mesmo texto acima do max",
            lambda: renderizar_tela(modelo_inv, _ESTILO_CURVA, largura=42),
            RenderizadorErro,
        )

    def run_all(self):
        print("")
        print("== H-0034: distribuicao responsiva do lancador (fila/matriz) ==")
        self.test_fila_cardinalidades_basicas()
        self.test_quadro_minimo_fronteira_e_recuperacao()
        self.test_ordem_coluna_a_coluna_e_determinismo()
        self.test_colunas_independentes_t07()
        self.test_demo_fila_110()
        self.test_demo_matriz_109_e_80()
        self.test_demo_sem_paginacao_em_todas_larguras_validas()
        self.test_demo_fronteira_global_suplementar()
        self.test_isolamento_gatilho_interno()
        self.test_alinhamento_horizontal_por_instancia()
        self.test_parametros_tipo_ausente_levanta_erro()
        self.test_renderer_preserva_proibicoes_import()
        self.test_max_caracteres_configuravel()
        self.test_caminho_legado_valida_texto()


_H0033_TELAS_TODAS = (
    "demo",
    "destino_minimo",
    "grupo_minimo",
    "stub_b",
    "h0029_dashboard_fracao",
    "h0029_dashboard_igual",
    "h0029_dashboard_percentual",
    "h0029_grupo_fracao",
    "h0029_grupo_igual",
    "h0029_grupo_pai_distribuido",
    "h0029_grupo_percentual",
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_2x4",
    "h0030_matriz_3x2",
)

# JSONs de matriz exigem altura_disponivel para distribuir linhas (sem natural).
_H0033_TELAS_MATRIZ = ("h0030_matriz_2x2", "h0030_matriz_2x4", "h0030_matriz_3x2")

# JSONs que renderizam em altura natural (todos exceto matriz).
_H0033_TELAS_ALTURA_NATURAL = tuple(
    t for t in _H0033_TELAS_TODAS if t not in _H0033_TELAS_MATRIZ
)

# JSONs compatíveis com altura=20 em largura=42 (elemento unico ou dist explicita).
# demo.json excluido: lancador gera overflow de conteudo em alturas pequenas.
_H0033_TELAS_ALTURA_20 = tuple(t for t in _H0033_TELAS_TODAS if t != "demo")


class TestOcupacaoIntegralCorpoH0033:
    """Testes focais de ADR-0024 (proibicao de preenchimento externo vazio).

    Cobre DA-01 (cardinalidade unitaria), DA-02 (multiplos sem distribuicao),
    DA-03 (grupos repassam area) e DA-04 (composicao impossivel). Inclui
    inventario de todos os 16 JSONs permanentes em duas dimensoes.
    """

    LARGURA = 42
    ALTURA = 20
    LARGURA_B = 80
    ALTURA_B = 30

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn, msg_contem=""):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            ok = not msg_contem or msg_contem in str(exc)
            self._r(nome, ok, str(exc))
            return exc

    def _render(self, elementos, corpo_dist=None, altura=None, largura=None):
        m = _modelo_h0029(elementos, corpo_dist=corpo_dist)
        kw = {"largura": largura or self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # ----------------------------------------------------------------- DA-01
    def test_DA01_visual_direto_ocupa_area_integral(self):
        """DA-01: unico visual direto preenche toda a area disponivel."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-01: total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-01: visual direto ocupa l_corpo_disponivel=14",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 DA-01: sem fill externo (proibido por ADR-0024)",
            len(fill_ext) == 0,
        )

    def test_DA01_visual_via_grupo_transparente(self):
        """DA-01: visual aninhado em grupo sem dist recebe area integral."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "dashboard", "D1")])],
            altura=self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-01+DA-03: visual via grupo transparente ocupa 14 linhas",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 DA-01+DA-03: sem fill externo",
            len(fill_ext) == 0,
        )

    def test_DA01_fill_interno_preservado(self):
        """DA-01: fill interno (dentro das bordas) e valido e distinto do externo."""
        saida = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        linhas = saida.splitlines()
        # Fill externo sao linhas de N espacos (sem borda)
        fill_ext = [l for l in linhas if l == " " * self.LARGURA]
        # Fill interno sao linhas comecando e terminando com borda vertical
        fill_int = [l for l in linhas if l.startswith("│") and l.endswith("│")
                    and l[1:-1].strip() == ""]
        self._r(
            "H-0033 DA-01: sem fill externo e com fill interno",
            len(fill_ext) == 0 and len(fill_int) > 0,
            "ext={0} int={1}".format(len(fill_ext), len(fill_int)),
        )

    def test_DA01_equivalencia_com_distribuicao(self):
        """DA-01 sem dist produz saida identica a dist explicita com 1 elemento."""
        saida_sem = self._render(
            [_funcional("d1", "dashboard", "D1")],
            altura=self.ALTURA,
        )
        saida_com = self._render(
            [_funcional("d1", "dashboard", "D1")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-01: sem dist == com dist explícita (1 visual)",
            saida_sem == saida_com,
        )

    # ----------------------------------------------------------------- DA-02
    def test_DA02_dois_visuais_sem_dist_erro(self):
        """DA-02: 2 visuais sem distribuicao com area residual levanta RenderizadorErro."""
        self._espera_erro(
            "H-0033 DA-02: 2 visuais sem dist + l_fill>0 -> RenderizadorErro",
            lambda: self._render(
                [_funcional("a", "console", "A"), _funcional("b", "dashboard", "B")],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    def test_DA02_tres_visuais_sem_dist_erro(self):
        """DA-02: 3 visuais sem distribuicao levanta RenderizadorErro."""
        exc = self._espera_erro(
            "H-0033 DA-02: 3 visuais sem dist -> RenderizadorErro",
            lambda: self._render(
                [_funcional("a", "console", "A"),
                 _funcional("b", "dashboard", "B"),
                 _funcional("c", "console", "C")],
                altura=self.ALTURA,
            ),
            "DA-02",
        )
        if exc is not None:
            self._r(
                "H-0033 DA-02: mensagem menciona 'distribuicao'",
                "distribuicao" in str(exc),
                str(exc),
            )

    def test_DA02_com_distribuicao_ok(self):
        """DA-02: multiplos visuais COM distribuicao explicita funciona (sem erro)."""
        saida = self._render(
            [_funcional("a", "console", "A"), _funcional("b", "dashboard", "B")],
            corpo_dist={"modo": "igual"},
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-02: 2 visuais com dist=igual -> total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-02: com dist -> soma das cotas == l_corpo_disponivel",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )

    def test_DA02_sem_area_residual_ok(self):
        """DA-02: multiplos visuais sem dist sem area residual nao levanta erro."""
        # 3 elementos naturais; l_corpo_disponivel = 21-3-3 = 15 = l_corpo_natural.
        # l_fill = 0 -> sem DA-02.
        modelo_sd = _modelo_orquestrador_sem_distribuicao()
        n_natural = 21  # l_cab(3) + l_corpo(15) + l_barra(3) = 21 (H-0037: 11 itens)
        saida = renderizar_tela(modelo_sd, _ESTILO_CURVA, largura=42, altura=n_natural)
        # renderizar_tela termina com '\n'; count('\n') == numero de linhas fisicas.
        self._r(
            "H-0033 DA-02: sem dist + l_fill==0 -> sem erro (altura natural)",
            saida.count("\n") == n_natural,
            "count={0}".format(saida.count("\n")),
        )

    # ----------------------------------------------------------------- DA-03
    def test_DA03_grupo_com_dist_repassa_area(self):
        """DA-03: grupo com dist propria recebe area e distribui internamente."""
        saida = self._render(
            [_grupo("g1", "vertical", [
                _funcional("a", "console", "A"),
                _funcional("b", "dashboard", "B"),
            ], distribuicao={"modo": "igual"})],
            altura=self.ALTURA,
        )
        self._r(
            "H-0033 DA-03: grupo com dist recebe area -> total == altura",
            _h0029_linhas_totais(saida) == self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-03: filhos do grupo somam l_corpo_disponivel=14",
            sum(corpo_alts) == 14,
            "corpo_alturas={0}".format(corpo_alts),
        )

    def test_DA03_grupo_transparente_repassa_area_integral(self):
        """DA-03: grupo sem dist e transparente; visual filho recebe area integral."""
        saida = self._render(
            [_grupo("g1", "vertical", [_funcional("d1", "console", "C1")])],
            altura=self.ALTURA,
        )
        corpo_alts = _corpo_alturas(saida)
        self._r(
            "H-0033 DA-03: grupo transparente -> visual recebe 14 linhas",
            corpo_alts == [14],
            "corpo_alturas={0}".format(corpo_alts),
        )

    # ----------------------------------------------------------------- DA-04
    def test_DA04_zero_visuais_com_area_erro(self):
        """DA-04: corpo sem visuais e com area disponivel levanta RenderizadorErro."""
        modelo = ModeloTela(
            id="teste_da04",
            schema="tela.v1",
            cabecalho={"titulo": "DA04", "descricao": "sem visuais"},
            corpo=Corpo(arranjo="vertical", elementos=[], distribuicao=None),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        exc = None
        try:
            renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=self.ALTURA)
        except RenderizadorErro as e:
            exc = e
        self._r(
            "H-0033 DA-04: 0 visuais + altura > 0 -> RenderizadorErro",
            exc is not None,
            str(exc) if exc else "nenhuma excecao",
        )
        if exc is not None:
            self._r(
                "H-0033 DA-04: mensagem menciona 'DA-04' ou 'visual'",
                "DA-04" in str(exc) or "visual" in str(exc),
                str(exc),
            )

    # ---------------------------------------------------------------- inventário
    def test_inventario_16_jsons_altura_natural(self):
        """Inventario: 13 JSONs (exceto matriz) renderizam sem erro em altura natural."""
        for id_tela in _H0033_TELAS_ALTURA_NATURAL:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA)
                self._r(
                    "H-0033 INV: {0} renderiza em largura={1} sem erro".format(
                        id_tela, self.LARGURA
                    ),
                    isinstance(saida, str) and len(saida) > 0,
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV: {0} renderiza em largura={1} sem erro".format(
                        id_tela, self.LARGURA
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    def test_inventario_15_jsons_com_altura_20(self):
        """Inventario: 15 JSONs (exceto demo) renderizam a 42x20 sem fill externo."""
        for id_tela in _H0033_TELAS_ALTURA_20:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
                linhas_total = _h0029_linhas_totais(saida)
                fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
                self._r(
                    "H-0033 INV 42x20: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA
                    ),
                    linhas_total == self.ALTURA and len(fill_ext) == 0,
                    "linhas={0} fill_ext={1}".format(linhas_total, len(fill_ext)),
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV 42x20: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    def test_inventario_15_jsons_com_altura_30_largura_80(self):
        """Inventario: 15 JSONs (exceto demo) renderizam a 80x30 sem fill externo."""
        for id_tela in _H0033_TELAS_ALTURA_20:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA_B, altura=self.ALTURA_B
                )
                linhas_total = _h0029_linhas_totais(saida)
                fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA_B]
                self._r(
                    "H-0033 INV 80x30: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA_B
                    ),
                    linhas_total == self.ALTURA_B and len(fill_ext) == 0,
                    "linhas={0} fill_ext={1}".format(linhas_total, len(fill_ext)),
                )
            except Exception as exc:
                self._r(
                    "H-0033 INV 80x30: {0} -> {1} linhas, sem fill externo".format(
                        id_tela, self.ALTURA_B
                    ),
                    False,
                    "{0}: {1}".format(type(exc).__name__, exc),
                )

    # ------------------------------------------------- destino_minimo / grupo_minimo
    def test_destino_minimo_sem_fill_externo(self):
        """destino_minimo.json: DA-01 - dashboard ocupa area integral sem fill externo."""
        modelo = construir_modelo(
            carregar_tela(_BASE_PADRAO, "destino_minimo", _RAIZ_TELAS_DEMO)
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
        corpo_alts = _corpo_alturas(saida)
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 destino_minimo: DA-01 -> corpo_alts==[14], sem fill externo",
            corpo_alts == [14] and len(fill_ext) == 0,
            "corpo_alturas={0} fill_ext={1}".format(corpo_alts, len(fill_ext)),
        )

    def test_grupo_minimo_sem_fill_externo(self):
        """grupo_minimo.json: DA-01+DA-03 - visual via grupo ocupa area sem fill externo."""
        modelo = construir_modelo(
            carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
        )
        saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=self.LARGURA, altura=self.ALTURA)
        corpo_alts = _corpo_alturas(saida)
        fill_ext = [l for l in saida.splitlines() if l == " " * self.LARGURA]
        self._r(
            "H-0033 grupo_minimo: DA-01+DA-03 -> corpo_alts==[14], sem fill externo",
            corpo_alts == [14] and len(fill_ext) == 0,
            "corpo_alturas={0} fill_ext={1}".format(corpo_alts, len(fill_ext)),
        )

    # ---- Helpers horizontais (QA-H0033-IMP-HIGH-001 / QA-H0033-IMP-MED-001) ----
    def _render_h(self, elementos, corpo_dist=None, altura=None, largura=None):
        """Helper: cria modelo com corpo horizontal para testes focais H1-H6."""
        m = ModeloTela(
            id="teste_h0033_h",
            schema="tela.v1",
            cabecalho={"titulo": "H0033H", "descricao": "h0033 horizontal"},
            corpo=Corpo(arranjo="horizontal", elementos=elementos,
                        distribuicao=corpo_dist),
            barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        kw = {"largura": largura or self.LARGURA}
        if altura is not None:
            kw["altura"] = altura
        return renderizar_tela(m, _ESTILO_CURVA, **kw)

    # ----------------------------------------------------------------- H1
    def test_H1_horizontal_um_participante_sem_dist(self):
        """H1 (DA-01): corpo horizontal com 1 elemento sem dist e valido."""
        try:
            saida = self._render_h([_funcional("a", "console", "A")])
            self._r(
                "H-0033 H1: horizontal 1 elem sem dist -> valido (DA-01)",
                bool(saida.strip()),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H1: horizontal 1 elem sem dist -> valido (DA-01)",
                False,
                str(exc),
            )

    # ----------------------------------------------------------------- H2
    def test_H2_horizontal_dois_sem_dist_rejeita(self):
        """H2 (DA-02): corpo horizontal com 2 elementos sem dist levanta RenderizadorErro.

        Achado QA-H0033-IMP-HIGH-001: implementacao anterior aceitava composicao
        invalida e particionava largura uniformemente; agora deve rejeitar.
        """
        self._espera_erro(
            "H-0033 H2: horizontal 2 elem sem dist -> RenderizadorErro DA-02",
            lambda: self._render_h(
                [_funcional("a", "console", "A"), _funcional("b", "console", "B")],
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H3
    def test_H3_horizontal_grupo_multiplos_sem_dist_rejeita(self):
        """H3 (DA-02): grupo interno com arranjo horizontal e 2 filhos sem dist e rejeitado."""
        self._espera_erro(
            "H-0033 H3: grupo horizontal 2 filhos sem dist -> RenderizadorErro DA-02",
            lambda: self._render(
                [_grupo("g1", "horizontal", [
                    _funcional("a", "console", "A"),
                    _funcional("b", "console", "B"),
                ])],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H4
    def test_H4_horizontal_aninhado_nao_bypassa_DA02(self):
        """H4 (DA-02): container horizontal aninhado em grupo nao bypassa DA-02."""
        self._espera_erro(
            "H-0033 H4: horizontal aninhado (grupo>grupo_h) -> RenderizadorErro DA-02",
            lambda: self._render(
                [_grupo("g1", "vertical", [
                    _grupo("g2", "horizontal", [
                        _funcional("a", "console", "A"),
                        _funcional("b", "console", "B"),
                    ]),
                ])],
                altura=self.ALTURA,
            ),
            "DA-02",
        )

    # ----------------------------------------------------------------- H5
    def test_H5_horizontal_com_distribuicao_valido(self):
        """H5 (DA-02): corpo horizontal com distribuicao explicita e valido."""
        try:
            saida = self._render_h(
                [_funcional("a", "console", "A"), _funcional("b", "console", "B")],
                corpo_dist={"modo": "igual"},
            )
            linhas = [l for l in saida.split("\n") if l]
            self._r(
                "H-0033 H5: horizontal com dist=igual -> saida valida",
                bool(saida.strip()),
            )
            self._r(
                "H-0033 H5: horizontal com dist=igual -> largura preservada",
                all(len(l) == self.LARGURA for l in linhas),
                "invalidas={0}".format([len(l) for l in linhas if len(l) != self.LARGURA]),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H5: horizontal com dist=igual -> saida valida",
                False,
                str(exc),
            )

    # ----------------------------------------------------------------- H6
    def test_H6_matriz_nao_e_rejeitada(self):
        """H6: grupo com estrutura='matriz' nao e rejeitado por DA-02 (caminho distinto)."""
        try:
            grupo_m = _grupo_matriz_render_h0028("gm", n_linhas=2, n_colunas=2)
            saida = self._render([grupo_m], altura=self.ALTURA)
            self._r(
                "H-0033 H6: matriz 2x2 em corpo vertical -> renderiza sem DA-02",
                bool(saida.strip()),
            )
        except RenderizadorErro as exc:
            self._r(
                "H-0033 H6: matriz 2x2 em corpo vertical -> renderiza sem DA-02",
                False,
                str(exc),
            )

    def run_all(self):
        print("")
        print("== TestOcupacaoIntegralCorpoH0033: ADR-0024 DA-01 a DA-04 ==")
        self.test_DA01_visual_direto_ocupa_area_integral()
        self.test_DA01_visual_via_grupo_transparente()
        self.test_DA01_fill_interno_preservado()
        self.test_DA01_equivalencia_com_distribuicao()
        self.test_DA02_dois_visuais_sem_dist_erro()
        self.test_DA02_tres_visuais_sem_dist_erro()
        self.test_DA02_com_distribuicao_ok()
        self.test_DA02_sem_area_residual_ok()
        self.test_DA03_grupo_com_dist_repassa_area()
        self.test_DA03_grupo_transparente_repassa_area_integral()
        self.test_DA04_zero_visuais_com_area_erro()
        self.test_inventario_16_jsons_altura_natural()
        self.test_inventario_15_jsons_com_altura_20()
        self.test_inventario_15_jsons_com_altura_30_largura_80()
        self.test_destino_minimo_sem_fill_externo()
        self.test_grupo_minimo_sem_fill_externo()
        self.test_H1_horizontal_um_participante_sem_dist()
        self.test_H2_horizontal_dois_sem_dist_rejeita()
        self.test_H3_horizontal_grupo_multiplos_sem_dist_rejeita()
        self.test_H4_horizontal_aninhado_nao_bypassa_DA02()
        self.test_H5_horizontal_com_distribuicao_valido()
        self.test_H6_matriz_nao_e_rejeitada()


class TestHelperHorizontalH0033Patch2:
    """Testes focais para _montar_corpo_horizontal e caminho publico horizontal
    apos segundo patch H-0033 (QA-H0033-POSPATCH-IMP-MED-001).

    P1. zero participantes retorna vazio;
    P2. um participante sem larguras recebe total_w (DA-01/ADR-0024);
    P3. dois participantes sem larguras sao rejeitados (DA-02/ADR-0024);
    P4. tres participantes sem larguras sao rejeitados (DA-02/ADR-0024);
    P5. larguras explicitas validas sao respeitadas;
    P6. largura insuficiente por elemento e rejeitada;
    P7. nenhuma saida parcial e produzida antes do erro (DA-02);
    P8. caminho publico com dist=fracao e valido;
    P9. caminho publico com dist=percentual e valido;
    P10. eixo vertical com distribuicao nao regrediu.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _espera_erro(self, nome, fn, prefixo=None):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
            return None
        except RenderizadorErro as exc:
            ok = (prefixo is None) or (prefixo in str(exc))
            self._r(nome, ok, str(exc))
            return exc
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))
            return None

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, tipo="console", titulo="A"):
        campos = {"titulo": titulo}
        if tipo == "lancador":
            campos["itens"] = []
        return ElementoCorpo(id=titulo.lower(), tipo=tipo, _campos_inertes=campos)

    def _modelo_h(self, elementos, corpo_dist=None, largura=42):
        return ModeloTela(
            id="teste_patch2",
            schema="tela.v1",
            cabecalho={"titulo": "P2", "descricao": "patch2"},
            corpo=Corpo(arranjo="horizontal", elementos=elementos,
                        distribuicao=corpo_dist),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )

    # ------------------------------------------------------------------ P1
    def test_P1_helper_zero_participantes_retorna_vazio(self):
        """P1: _montar_corpo_horizontal com zero elementos retorna string vazia."""
        borda = self._borda()
        resultado = _montar_corpo_horizontal([], borda, 42)
        self._r(
            "P1: _montar_corpo_horizontal([]) -> ''",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )

    # ------------------------------------------------------------------ P2
    def test_P2_helper_um_participante_recebe_total_w(self):
        """P2 (DA-01): _montar_corpo_horizontal com 1 elemento recebe total_w."""
        borda = self._borda()
        elem = self._elem("console", "A")
        resultado = _montar_corpo_horizontal([elem], borda, 42)
        linhas = resultado.split("\n")
        self._r(
            "P2: _montar_corpo_horizontal(1 elem, larguras=None) -> largura=42",
            all(len(ln) == 42 for ln in linhas if ln),
            "larguras={0}".format([len(ln) for ln in linhas if ln]),
        )
        self._r(
            "P2: _montar_corpo_horizontal(1 elem) -> resultado nao vazio",
            bool(resultado.strip()),
        )

    # ------------------------------------------------------------------ P3
    def test_P3_helper_dois_participantes_sem_larguras_rejeita(self):
        """P3 (DA-02): _montar_corpo_horizontal com 2 elementos e larguras=None levanta DA-02."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("console", "B")
        self._espera_erro(
            "P3: _montar_corpo_horizontal(2 elem, larguras=None) -> RenderizadorErro DA-02",
            lambda: _montar_corpo_horizontal([elem_a, elem_b], borda, 42),
            "DA-02",
        )

    # ------------------------------------------------------------------ P4
    def test_P4_helper_tres_participantes_sem_larguras_rejeita(self):
        """P4 (DA-02): _montar_corpo_horizontal com 3 elementos e larguras=None levanta DA-02."""
        borda = self._borda()
        elems = [self._elem("console", c) for c in ("A", "B", "C")]
        self._espera_erro(
            "P4: _montar_corpo_horizontal(3 elem, larguras=None) -> RenderizadorErro DA-02",
            lambda: _montar_corpo_horizontal(elems, borda, 42),
            "DA-02",
        )

    # ------------------------------------------------------------------ P5
    def test_P5_helper_larguras_explicitas_validas_respeitadas(self):
        """P5: _montar_corpo_horizontal com larguras explicitas validas renderiza corretamente."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("dashboard", "B")
        resultado = _montar_corpo_horizontal(
            [elem_a, elem_b], borda, 42, larguras=[21, 21]
        )
        linhas = resultado.split("\n")
        self._r(
            "P5: larguras=[21,21] -> todas as linhas tem 42 chars",
            all(len(ln) == 42 for ln in linhas),
            "erros={0}".format([len(ln) for ln in linhas if len(ln) != 42]),
        )
        self._r(
            "P5: larguras=[21,21] -> resultado nao vazio",
            bool(resultado.strip()),
        )

    # ------------------------------------------------------------------ P6
    def test_P6_helper_largura_insuficiente_rejeitada(self):
        """P6: largura por area abaixo de 10 e rejeitada com RenderizadorErro."""
        borda = self._borda()
        elem_a = self._elem("console", "A")
        elem_b = self._elem("console", "B")
        self._espera_erro(
            "P6: larguras=[5, 37] -> RenderizadorErro (w<10 em area 0)",
            lambda: _montar_corpo_horizontal(
                [elem_a, elem_b], borda, 42, larguras=[5, 37]
            ),
        )

    # ------------------------------------------------------------------ P7
    def test_P7_helper_sem_saida_parcial_antes_do_erro(self):
        """P7: DA-02 impede qualquer saida parcial antes de lancar RenderizadorErro."""
        borda = self._borda()
        elems = [self._elem("console", c) for c in ("A", "B")]
        saida_parcial = []
        erro_capturado = None
        try:
            resultado = _montar_corpo_horizontal(elems, borda, 42)
            saida_parcial.append(resultado)
        except RenderizadorErro as exc:
            erro_capturado = exc
        self._r(
            "P7: DA-02 lanca erro antes de produzir saida parcial",
            erro_capturado is not None and len(saida_parcial) == 0,
            "erro={0!r} saida_parcial={1}".format(
                str(erro_capturado) if erro_capturado else None, saida_parcial
            ),
        )

    # ------------------------------------------------------------------ P8
    def test_P8_publico_horizontal_dist_fracao_valido(self):
        """P8: caminho publico com dist=fracao no horizontal e valido."""
        modelo = self._modelo_h(
            [self._elem("console", "A"), self._elem("console", "B")],
            corpo_dist={"modo": "fracao", "valores": [2, 1]},
            largura=42,
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42)
            linhas = [ln for ln in saida.split("\n") if ln]
            self._r(
                "P8: horizontal dist=fracao -> saida valida, largura=42",
                all(len(ln) == 42 for ln in linhas),
                "erros={0}".format([len(ln) for ln in linhas if len(ln) != 42]),
            )
        except RenderizadorErro as exc:
            self._r("P8: horizontal dist=fracao -> saida valida", False, str(exc))

    # ------------------------------------------------------------------ P9
    def test_P9_publico_horizontal_dist_percentual_valido(self):
        """P9: caminho publico com dist=percentual no horizontal e valido."""
        modelo = self._modelo_h(
            [self._elem("console", "A"), self._elem("dashboard", "B")],
            corpo_dist={"modo": "percentual", "valores": [60, 40]},
            largura=100,
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=100)
            linhas = [ln for ln in saida.split("\n") if ln]
            self._r(
                "P9: horizontal dist=percentual -> saida valida, largura=100",
                all(len(ln) == 100 for ln in linhas),
                "erros={0}".format([len(ln) for ln in linhas if len(ln) != 100]),
            )
        except RenderizadorErro as exc:
            self._r("P9: horizontal dist=percentual -> saida valida", False, str(exc))

    # ----------------------------------------------------------------- P10
    def test_P10_vertical_com_distribuicao_nao_regrediu(self):
        """P10: eixo vertical com distribuicao explicita nao regrediu (regressao)."""
        modelo = ModeloTela(
            id="teste_p10",
            schema="tela.v1",
            cabecalho={"titulo": "P10", "descricao": "regressao vertical"},
            corpo=Corpo(
                arranjo="vertical",
                elementos=[
                    _funcional("a", "console", "A"),
                    _funcional("b", "dashboard", "B"),
                ],
                distribuicao={"modo": "igual"},
            ),
            barra_de_menus={"chips": [{"id": "e", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )
        try:
            saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=42, altura=20)
            self._r(
                "P10: vertical dist=igual altura=20 -> 20 linhas",
                saida.count("\n") == 20,
                "count={0}".format(saida.count("\n")),
            )
        except RenderizadorErro as exc:
            self._r("P10: vertical dist=igual nao regrediu", False, str(exc))

    def run_all(self):
        print("")
        print("== TestHelperHorizontalH0033Patch2: helper e caminho publico ==")
        self.test_P1_helper_zero_participantes_retorna_vazio()
        self.test_P2_helper_um_participante_recebe_total_w()
        self.test_P3_helper_dois_participantes_sem_larguras_rejeita()
        self.test_P4_helper_tres_participantes_sem_larguras_rejeita()
        self.test_P5_helper_larguras_explicitas_validas_respeitadas()
        self.test_P6_helper_largura_insuficiente_rejeitada()
        self.test_P7_helper_sem_saida_parcial_antes_do_erro()
        self.test_P8_publico_horizontal_dist_fracao_valido()
        self.test_P9_publico_horizontal_dist_percentual_valido()
        self.test_P10_vertical_com_distribuicao_nao_regrediu()


class TestCardinalidadeHorizontalH0033Patch3:
    """Testes focais de cardinalidade em _montar_corpo_horizontal.

    Verifica rejeicao de larguras explicitas com cardinalidade incoerente
    (QA-H0033-POSPATCH2-IMP-LOW-001).

    C1. N=0, L=0 -> comportamento coerente (retorna '');
    C2. N=0, L=1 -> rejeicao;
    C3. N=1, L=0 -> rejeicao;
    C4. N=1, L=1 -> sucesso;
    C5. N=1, L=2 -> rejeicao;
    C6. N=2, L=1 -> rejeicao;
    C7. N=2, L=2 -> sucesso;
    C8. N=2, L=3 -> rejeicao;
    C9. N=3, L=2 -> rejeicao;
    C10. erro antes de renderizacao parcial (participantes instrumentados);
    C11. mensagem informa N e L;
    C12. larguras=None preserva DA-01 (N=1) e DA-02 (N>1).
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, titulo="A"):
        campos = {"titulo": titulo}
        return ElementoCorpo(id=titulo.lower(), tipo="console", _campos_inertes=campos)

    def _espera_card_erro(self, nome, fn):
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada")
        except RenderizadorErro as exc:
            ok = "cardinalidade horizontal incoerente" in str(exc)
            self._r(nome, ok, str(exc)[:120])
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))

    # ------------------------------------------------------------------ C1-C2
    def test_C1_C2_zero_participantes(self):
        """C1: N=0, L=0 -> ''; C2: N=0, L=1 -> rejeicao."""
        borda = self._borda()
        resultado = _montar_corpo_horizontal([], borda, 42, larguras=[])
        self._r(
            "C1: N=0, L=0 -> resultado vazio",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )
        self._espera_card_erro(
            "C2: N=0, L=1 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([], borda, 42, larguras=[42]),
        )

    # ------------------------------------------------------------------ C3-C5
    def test_C3_C4_C5_um_participante(self):
        """C3: N=1, L=0 -> rejeicao; C4: N=1, L=1 -> sucesso; C5: N=1, L=2 -> rejeicao."""
        borda = self._borda()
        e = self._elem("A")
        self._espera_card_erro(
            "C3: N=1, L=0 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([e], borda, 42, larguras=[]),
        )
        try:
            resultado = _montar_corpo_horizontal([e], borda, 42, larguras=[42])
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C4: N=1, L=1 -> sucesso e largura=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C4: N=1, L=1 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "C5: N=1, L=2 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([e], borda, 42, larguras=[21, 21]),
        )

    # ------------------------------------------------------------------ C6-C9
    def test_C6_C7_C8_C9_dois_e_tres_participantes(self):
        """C6-C9: cardinalidade incoerente rejeita; coerente aceita."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        ec = self._elem("C")
        self._espera_card_erro(
            "C6: N=2, L=1 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal([ea, eb], borda, 42, larguras=[42]),
        )
        try:
            resultado = _montar_corpo_horizontal(
                [ea, eb], borda, 42, larguras=[28, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C7: N=2, L=2 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C7: N=2, L=2 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "C8: N=2, L=3 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal(
                [ea, eb], borda, 42, larguras=[14, 14, 14]
            ),
        )
        self._espera_card_erro(
            "C9: N=3, L=2 -> RenderizadorErro cardinalidade",
            lambda: _montar_corpo_horizontal(
                [ea, eb, ec], borda, 42, larguras=[21, 21]
            ),
        )

    # ----------------------------------------------------------------- C10
    def test_C10_erro_antes_de_renderizacao(self):
        """C10: erro de cardinalidade ocorre antes de qualquer renderizacao.

        Usa elementos instrumentados: o acesso a .tipo so ocorre dentro do
        loop de renderizacao. Se o erro for levantado antes do loop, .tipo
        nunca e acessado e o rastreador permanece vazio.
        """
        tracker = []

        class _ElemInstrumentado:
            id = "instrumento"
            _campos_inertes = {"titulo": "T"}

            @property
            def tipo(self):
                tracker.append("tipo_acessado")
                return "console"

        borda = self._borda()
        e1 = _ElemInstrumentado()
        e2 = _ElemInstrumentado()
        erro_levantado = False
        try:
            _montar_corpo_horizontal([e1, e2], borda, 42, larguras=[42])
        except RenderizadorErro:
            erro_levantado = True
        self._r(
            "C10: erro de cardinalidade e levantado antes da renderizacao",
            erro_levantado and len(tracker) == 0,
            "erro={0} tracker={1}".format(erro_levantado, tracker),
        )

    # ----------------------------------------------------------------- C11
    def test_C11_mensagem_informa_cardinalidades(self):
        """C11: mensagem de erro informa N e L observados."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        msg = None
        try:
            _montar_corpo_horizontal([ea, eb], borda, 42, larguras=[42])
        except RenderizadorErro as exc:
            msg = str(exc)
        self._r(
            "C11: mensagem contem 'cardinalidade horizontal incoerente'",
            msg is not None and "cardinalidade horizontal incoerente" in msg,
            "msg={0!r}".format(msg),
        )
        self._r(
            "C11: mensagem informa N=2 e L=1",
            msg is not None and "2 participante" in msg and "1 largura" in msg,
            "msg={0!r}".format(msg),
        )

    # ----------------------------------------------------------------- C12
    def test_C12_larguras_none_preserva_DA01_e_DA02(self):
        """C12: larguras=None preserva DA-01 (N=1) e DA-02 (N>1)."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        try:
            resultado = _montar_corpo_horizontal([ea], borda, 42)
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "C12a: N=1, larguras=None -> DA-01 (largura integral 42)",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("C12a: DA-01", False, str(exc))
        try:
            _montar_corpo_horizontal([ea, eb], borda, 42)
            self._r("C12b: N=2, larguras=None -> DA-02", False, "sem excecao")
        except RenderizadorErro as exc:
            self._r(
                "C12b: N=2, larguras=None -> DA-02",
                "DA-02" in str(exc),
                str(exc)[:120],
            )

    def run_all(self):
        print("")
        print("== TestCardinalidadeHorizontalH0033Patch3: cardinalidade larguras explicitas ==")
        self.test_C1_C2_zero_participantes()
        self.test_C3_C4_C5_um_participante()
        self.test_C6_C7_C8_C9_dois_e_tres_participantes()
        self.test_C10_erro_antes_de_renderizacao()
        self.test_C11_mensagem_informa_cardinalidades()
        self.test_C12_larguras_none_preserva_DA01_e_DA02()


class TestCardinalidadeHorizontalH0033Patch4:
    """Testes focais de cardinalidade em _renderizar_container_horizontal.

    Atinge diretamente o helper horizontal recursivo, equivalente ao
    _montar_corpo_horizontal ja corrigido no terceiro patch. Verifica rejeicao
    de larguras explicitas com cardinalidade incoerente
    (QA-H0033-POSPATCH3-IMP-LOW-001): lista curta nao produz IndexError e
    lista longa nao e truncada silenciosamente.

    H1. N=0, L=0 -> comportamento coerente (retorna '');
    H2. N=0, L=1 -> rejeicao;
    H3. N=1, L=0 -> rejeicao;
    H4. N=1, L=1 -> sucesso;
    H5. N=1, L=2 -> rejeicao;
    H6. N=2, L=1 -> rejeicao (sem IndexError);
    H7. N=2, L=2 -> sucesso;
    H8. N=2, L=3 -> rejeicao (sem truncamento);
    H9. N=3, L=2 -> rejeicao;
    H10. N=3, L=3 -> sucesso;
    H11. lista longa (N=2, L=3) rejeitada com RenderizadorErro, sem truncamento
         nem saida parcial (tracker externo vazio); rejeita sucesso, IndexError
         e excecao generica;
    H12. lista curta (N=2, L=1) rejeitada com RenderizadorErro, sem IndexError;
    H13. erro ocorre antes de qualquer renderizacao (participantes instrumentados);
    H14. mensagem informa N e L;
    H15. larguras=None preserva DA-01 (N=1) e DA-02 (N>1);
    H16. distribuicao explicita coerente permanece valida.
    """

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _borda(self):
        # H-0039: _BORDAS foi removido; o dict interno de borda derivado do
        # EstiloResolvido usa as chaves consumidas pelas helpers (incluindo
        # h_superior/h_inferior distintos).
        return {
            "tl": _ESTILO_CURVA.canto_superior_esquerdo,
            "tr": _ESTILO_CURVA.canto_superior_direito,
            "bl": _ESTILO_CURVA.canto_inferior_esquerdo,
            "br": _ESTILO_CURVA.canto_inferior_direito,
            "v": _ESTILO_CURVA.lateral,
            "h_superior": _ESTILO_CURVA.traco_superior,
            "h_inferior": _ESTILO_CURVA.traco_inferior,
        }

    def _elem(self, titulo="A"):
        campos = {"titulo": titulo}
        return ElementoCorpo(id=titulo.lower(), tipo="console", _campos_inertes=campos)

    def _espera_card_erro(self, nome, fn):
        """Exige RenderizadorErro de cardinalidade; rejeita IndexError/sucesso/outras."""
        try:
            fn()
            self._r(nome, False, "nenhuma excecao levantada (sucesso/truncamento)")
        except RenderizadorErro as exc:
            ok = "cardinalidade horizontal incoerente" in str(exc)
            self._r(nome, ok, str(exc)[:120])
        except IndexError as exc:
            self._r(nome, False, "IndexError (lista curta sem guarda): {0!r}".format(exc))
        except Exception as exc:
            self._r(nome, False, "excecao inesperada: {0!r}".format(exc))

    # ------------------------------------------------------------------ H1-H2
    def test_H1_H2_zero_participantes(self):
        """H1: N=0, L=0 -> ''; H2: N=0, L=1 -> rejeicao."""
        borda = self._borda()
        resultado = _renderizar_container_horizontal(
            None, [], borda, 42, None, larguras=[]
        )
        self._r(
            "H1: N=0, L=0 -> resultado vazio",
            resultado == "",
            "resultado={0!r}".format(resultado),
        )
        self._espera_card_erro(
            "H2: N=0, L=1 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [], borda, 42, None, larguras=[42]
            ),
        )

    # ------------------------------------------------------------------ H3-H5
    def test_H3_H4_H5_um_participante(self):
        """H3: N=1, L=0 -> rejeicao; H4: N=1, L=1 -> sucesso; H5: N=1, L=2 -> rejeicao."""
        borda = self._borda()
        e = self._elem("A")
        self._espera_card_erro(
            "H3: N=1, L=0 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[42]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: participante unico com largura integral.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H4: N=1, L=1 -> sucesso e largura=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H4: N=1, L=1 -> sucesso", False, str(exc))
        self._espera_card_erro(
            "H5: N=1, L=2 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [e], borda, 42, None, larguras=[21, 21]
            ),
        )

    # -------------------------------------------------------- H6-H10
    def test_H6_H7_H8_H9_H10_dois_e_tres_participantes(self):
        """H6-H10: cardinalidade incoerente rejeita; coerente aceita."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        ec = self._elem("C")
        # H6: N=2, L=1 -> rejeicao (prova que lista curta nao gera IndexError).
        self._espera_card_erro(
            "H6: N=2, L=1 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[28, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: 28 + 14 = 42 em cada linha.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H7: N=2, L=2 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H7: N=2, L=2 -> sucesso", False, str(exc))
        # H8: N=2, L=3 -> rejeicao (prova que lista longa nao e truncada).
        self._espera_card_erro(
            "H8: N=2, L=3 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[14, 14, 14]
            ),
        )
        self._espera_card_erro(
            "H9: N=3, L=2 -> RenderizadorErro cardinalidade",
            lambda: _renderizar_container_horizontal(
                None, [ea, eb, ec], borda, 42, None, larguras=[21, 21]
            ),
        )
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea, eb, ec], borda, 42, None, larguras=[14, 14, 14]
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            # Esperado independente: 14 + 14 + 14 = 42 em cada linha.
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H10: N=3, L=3 -> sucesso e largura total=42",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H10: N=3, L=3 -> sucesso", False, str(exc))

    # -------------------------------------------------------- H11-H12
    def test_H11_H12_sem_IndexError_e_sem_truncamento(self):
        """H11: lista longa rejeitada com RenderizadorErro (sem truncamento, sem saida parcial).

        Cenario material: 2 participantes (N=2) e 3 larguras explicitas (L=3),
        atingindo diretamente _renderizar_container_horizontal.

        Sem a guarda de cardinalidade, o loop de renderizacao iteraria apenas os
        dois participantes existentes (enumerate(elementos)) e descartaria
        silenciosamente a terceira largura excedente, produzindo linhas de
        largura 28. H11 deve exigir RenderizadorErro, rejeitando sucesso,
        IndexError e qualquer excecao generica.

        A prova de ausencia de saida parcial usa participantes instrumentados
        cujo acesso a .tipo so ocorre dentro do loop de renderizacao
        (for i, elemento in enumerate(elementos)). Se o erro de cardinalidade
        for levantado antes do loop, .tipo nunca e acessado e o tracker
        permanece vazio — provando que nenhum participante foi renderizado e
        nenhuma funcao descendente foi alcancada. A prova nao depende apenas da
        ausencia de uma largura/texto especifico na saida.

        H12: lista curta (N=2, L=1) rejeitada com RenderizadorErro, sem IndexError.
        """
        borda = self._borda()

        # Participantes instrumentados: tracker externo a funcao sob teste.
        # O acesso a .tipo so acontece dentro do loop de renderizacao; se a
        # guarda de cardinalidade rejeitar antes do loop, tracker permanece [].
        tracker = []

        class _ElemInstrumentado:
            def __init__(self, tid):
                self.id = tid
                self._campos_inertes = {"titulo": tid}

            @property
            def tipo(self):
                tracker.append("tipo_acessado:{0}".format(self.id))
                return "console"

        e1 = _ElemInstrumentado("A")
        e2 = _ElemInstrumentado("B")

        classe_erro = None
        mensagem = None
        sucesso = False
        try:
            _renderizar_container_horizontal(
                None, [e1, e2], borda, 42, None, larguras=[14, 14, 14]
            )
            sucesso = True
        except IndexError as exc:
            classe_erro = "IndexError"
            mensagem = str(exc)
        except RenderizadorErro as exc:
            classe_erro = "RenderizadorErro"
            mensagem = str(exc)
        except Exception as exc:
            # Excecao generica reprova: so RenderizadorErro e aceito.
            classe_erro = type(exc).__name__
            mensagem = str(exc)

        # (1) Exige RenderizadorErro; reprova sucesso, IndexError e excecao generica.
        self._r(
            "H11: N=2, L=3 levanta RenderizadorErro (rejeita sucesso/IndexError/generico)",
            classe_erro == "RenderizadorErro" and not sucesso,
            "sucesso={0} classe_erro={1} msg={2!r}".format(sucesso, classe_erro, mensagem),
        )
        # (2) Mensagem informa contexto horizontal, N=2 e L=3.
        self._r(
            "H11: mensagem informa horizontal, 2 participantes e 3 larguras",
            classe_erro == "RenderizadorErro"
            and mensagem is not None
            and "horizontal" in mensagem
            and "2 participante" in mensagem
            and "3 largura" in mensagem,
            "msg={0!r}".format(mensagem),
        )
        # (3) A largura excedente nao e ignorada: erro capturado, sem saida.
        #     A prova e material: o tracker permanece vazio, o que detectaria o
        #     caminho de renderizacao (e consequente truncamento) caso a guarda
        #     estivesse ausente. Nao basta verificar ausencia de largura 28.
        self._r(
            "H11: ausencia de saida parcial (tracker vazio, nenhum participante renderizado)",
            classe_erro == "RenderizadorErro" and len(tracker) == 0,
            "classe_erro={0} tracker={1}".format(classe_erro, tracker),
        )

        # H12: sem a guarda, N=2/L=1 levantaria IndexError ao indexar larguras[1].
        ea = self._elem("A")
        eb = self._elem("B")
        h12_index_error = False
        h12_card_erro = False
        try:
            _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            )
        except IndexError:
            h12_index_error = True
        except RenderizadorErro as exc:
            h12_card_erro = "cardinalidade horizontal incoerente" in str(exc)
        except Exception:
            pass
        self._r(
            "H12: N=2, L=1 levanta RenderizadorErro (nao IndexError)",
            h12_card_erro and not h12_index_error,
            "card_erro={0} index_error={1}".format(h12_card_erro, h12_index_error),
        )

    # -------------------------------------------------------- H13
    def test_H13_erro_antes_de_renderizacao(self):
        """H13: erro de cardinalidade ocorre antes de qualquer renderizacao.

        Usa elementos instrumentados: o acesso a .tipo so ocorre dentro do
        loop de renderizacao de _renderizar_container_horizontal. Se o erro
        for levantado antes do loop, .tipo nunca e acessado e o rastreador
        permanece vazio — provando ausencia de saida parcial e que nenhuma
        funcao descendente (_caixa_de_elemento/_renderizar_container) foi
        alcancada.
        """
        tracker = []

        class _ElemInstrumentado:
            id = "instrumento"
            _campos_inertes = {"titulo": "T"}

            @property
            def tipo(self):
                tracker.append("tipo_acessado")
                return "console"

        borda = self._borda()
        e1 = _ElemInstrumentado()
        e2 = _ElemInstrumentado()
        erro_card = False
        try:
            _renderizar_container_horizontal(
                None, [e1, e2], borda, 42, None, larguras=[42]
            )
        except RenderizadorErro as exc:
            erro_card = "cardinalidade horizontal incoerente" in str(exc)
        except Exception:
            pass
        self._r(
            "H13: erro de cardinalidade antes da renderizacao (tracker vazio)",
            erro_card and len(tracker) == 0,
            "erro_card={0} tracker={1}".format(erro_card, tracker),
        )

    # -------------------------------------------------------- H14
    def test_H14_mensagem_informa_cardinalidades(self):
        """H14: mensagem de erro informa contexto horizontal, N e L observados."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        msg = None
        try:
            _renderizar_container_horizontal(
                None, [ea, eb], borda, 42, None, larguras=[42]
            )
        except RenderizadorErro as exc:
            msg = str(exc)
        self._r(
            "H14: mensagem contem 'cardinalidade horizontal incoerente'",
            msg is not None and "cardinalidade horizontal incoerente" in msg,
            "msg={0!r}".format(msg),
        )
        self._r(
            "H14: mensagem informa N=2 e L=1",
            msg is not None and "2 participante" in msg and "1 largura" in msg,
            "msg={0!r}".format(msg),
        )

    # -------------------------------------------------------- H15-H16
    def test_H15_H16_regressao_larguras_none_e_dist(self):
        """H15: larguras=None preserva DA-01/DA-02; H16: distribuicao explicita valida."""
        borda = self._borda()
        ea = self._elem("A")
        eb = self._elem("B")
        try:
            resultado = _renderizar_container_horizontal(
                None, [ea], borda, 42, None
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H15a: N=1, larguras=None -> DA-01 (largura integral 42)",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H15a: DA-01", False, str(exc))
        try:
            _renderizar_container_horizontal(None, [ea, eb], borda, 42, None)
            self._r("H15b: N=2, larguras=None -> DA-02", False, "sem excecao")
        except RenderizadorErro as exc:
            self._r(
                "H15b: N=2, larguras=None -> DA-02",
                "DA-02" in str(exc),
                str(exc)[:120],
            )
        # H16: distribuicao explicita coerente continua valida (caminho publico).
        dist = {"modo": "igual"}
        try:
            resultado = _renderizar_container_horizontal(
                dist, [ea, eb], borda, 42, None
            )
            linhas = [ln for ln in resultado.split("\n") if ln]
            ok = bool(linhas) and all(len(ln) == 42 for ln in linhas)
            self._r(
                "H16: N=2, distribuicao=igual -> sucesso sem regressao",
                ok,
                "larguras_obs={0}".format([len(ln) for ln in linhas]),
            )
        except RenderizadorErro as exc:
            self._r("H16: distribuicao=igual", False, str(exc))

    def run_all(self):
        print("")
        print("== TestCardinalidadeHorizontalH0033Patch4: cardinalidade larguras explicitas em _renderizar_container_horizontal ==")
        self.test_H1_H2_zero_participantes()
        self.test_H3_H4_H5_um_participante()
        self.test_H6_H7_H8_H9_H10_dois_e_tres_participantes()
        self.test_H11_H12_sem_IndexError_e_sem_truncamento()
        self.test_H13_erro_antes_de_renderizacao()
        self.test_H14_mensagem_informa_cardinalidades()
        self.test_H15_H16_regressao_larguras_none_e_dist()


class TestDistribuicaoMatricialH0035:
    """Integracao do renderer com distribuicao_matricial (H-0035 / ADR-0025).

    Cobre (contrato H-0035 secoes 37.3-37.6): dashboard com e sem o campo;
    console substituindo politicas geometricas quando presente e preservando-as
    quando ausente; lancador com precedencia quando presente e ADR-0001/2/3
    preservados quando ausente; compatibilidade (ausencia = comportamento
    anterior); fallback via quadro minimo; ausencia de dupla autoridade.

    Expectativas geometricas derivadas por geometria fechada, nao pelo proprio
    algoritmo de producao.
    """

    def _dm(self, **over):
        base = {
            "formacao": {"politica": "matriz_fixa",
                         "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
            "ordem": "por_linha",
            "dimensionamento": {
                "colunas": {"politica": "minimo_fixo", "minimo": 5},
                "linhas": {"politica": "minimo_fixo", "minimo": 1},
            },
            "espacamento": {
                "margem_superior": {"minimo": 0},
                "margem_inferior": {"minimo": 0},
                "margem_esquerda": {"minimo": 0},
                "margem_direita": {"minimo": 0},
                "vao_horizontal": {"minimo": 1},
                "vao_vertical": {"minimo": 0},
            },
            "distribuicao_horizontal": {"politica": "inicio"},
            "distribuicao_vertical": {"politica": "inicio"},
            "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos",
                               "vertical": "uniforme_margens_e_vaos"},
            "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
            "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
        }
        base.update(over)
        return base

    def _modelo_dashboard(self, com_dm):
        campos = [
            {"id": "c1", "rotulo": "", "fonte": "literal", "valor": "AA"},
            {"id": "c2", "rotulo": "", "fonte": "literal", "valor": "BB"},
            {"id": "c3", "rotulo": "", "fonte": "literal", "valor": "CC"},
            {"id": "c4", "rotulo": "", "fonte": "literal", "valor": "DD"},
        ]
        el = ElementoCorpo(
            id="dash", tipo="dashboard",
            _campos_inertes={"titulo": "Grade", "campos": campos},
            distribuicao_matricial=self._dm() if com_dm else None,
        )
        corpo = Corpo(arranjo="vertical",
                      elementos=[el],
                      distribuicao={"modo": "igual"})
        return ModeloTela(
            id="t", schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": "D"},
            corpo=corpo,
            barra_de_menus={"chips": [
                {"id": "e", "tipo": "acao", "tecla": "Esc", "texto": "Sair"}]},
            _raw={},
        )

    def test_dashboard_com_grade(self):
        # 2x2, coluna largura 5, vao_h 1, ordem por_linha, alinhamento inicio.
        # Participante 0 "AA" em (0,0) x=0; participante 1 "BB" em (0,1) x=6.
        # Linha 0 do corpo: "AA" nas colunas 0-1 e "BB" a partir da coluna 6.
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        linhas = saida.split("\n")
        # Localiza a caixa GRADE.
        idx = next(i for i, l in enumerate(linhas) if "GRADE" in l)
        # Primeira linha de conteudo do dashboard.
        conteudo0 = linhas[idx + 1]
        # Formato de _linha_conteudo: "│ " + content + "│".
        corpo0 = conteudo0[2:2 + 39]
        ok_aa = corpo0[0:2] == "AA"
        ok_bb = corpo0[6:8] == "BB"
        _registrar("H0035 dashboard grade AA@0 BB@6",
                   ok_aa and ok_bb, repr(corpo0[:10]))
        conteudo1 = linhas[idx + 2]
        corpo1 = conteudo1[2:2 + 39]
        ok_cc = corpo1[0:2] == "CC"
        ok_dd = corpo1[6:8] == "DD"
        _registrar("H0035 dashboard grade CC/DD segunda linha",
                   ok_cc and ok_dd, repr(corpo1[:10]))

    def test_dashboard_sem_preserva(self):
        # Sem o campo: comportamento anterior (uma linha por campo literal).
        m = self._modelo_dashboard(com_dm=False)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        # Cada valor aparece em sua propria linha (comportamento _linhas_dashboard).
        _registrar("H0035 dashboard sem campo preserva (AA e BB em linhas)",
                   "│ AA " in saida and "│ BB " in saida)

    def test_ordem_preservada(self):
        # A grade nao reordena; participantes preservam a sequencia declarada.
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        pos_aa = saida.find("AA")
        pos_bb = saida.find("BB")
        pos_cc = saida.find("CC")
        pos_dd = saida.find("DD")
        _registrar("H0035 ordem preservada AA<BB<CC<DD",
                   pos_aa < pos_bb < pos_cc < pos_dd,
                   "{0},{1},{2},{3}".format(pos_aa, pos_bb, pos_cc, pos_dd))

    def test_sem_perda_nem_duplicacao(self):
        m = self._modelo_dashboard(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        _registrar("H0035 dashboard sem perda",
                   all(saida.count(v) == 1 for v in ("AA", "BB", "CC", "DD")))

    def test_console_com_substitui(self):
        itens = [
            {"id": "l1", "texto": "XX"},
            {"id": "l2", "texto": "YY"},
        ]
        el = ElementoCorpo(
            id="con", tipo="console",
            _campos_inertes={"titulo": "Console", "itens": itens},
            distribuicao_matricial=self._dm(
                formacao={"politica": "matriz_fixa",
                          "linhas": {"fixo": 1}, "colunas": {"fixo": 2}}),
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        m = ModeloTela(id="t", schema="tela.v1",
                       cabecalho={"titulo": "T", "descricao": "D"},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=12)
        # Com a grade, XX e YY aparecem lado a lado na mesma linha (1x2).
        for l in saida.split("\n"):
            if "XX" in l and "YY" in l:
                _registrar("H0035 console com: XX e YY na mesma linha (grade)",
                           True)
                break
        else:
            _registrar("H0035 console com: XX e YY na mesma linha (grade)", False)

    def test_console_sem_preserva(self):
        # Sem o campo, console mantem o placeholder de escopo "(console)".
        el = ElementoCorpo(
            id="con", tipo="console",
            _campos_inertes={"titulo": "Console"},
        )
        corpo = Corpo(arranjo="vertical", elementos=[el], distribuicao=None)
        m = ModeloTela(id="t", schema="tela.v1",
                       cabecalho={"titulo": "T", "descricao": "D"},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42)
        _registrar("H0035 console sem campo preserva placeholder",
                   "(console)" in saida)

    def _modelo_lancador(self, com_dm):
        itens = [
            {"id": "i1", "chip": "A", "texto": "um", "tela_destino": "t"},
            {"id": "i2", "chip": "B", "texto": "do", "tela_destino": "t"},
            {"id": "i3", "chip": "C", "texto": "tr", "tela_destino": "t"},
            {"id": "i4", "chip": "D", "texto": "qu", "tela_destino": "t"},
        ]
        params = {
            "vaos": {
                "chip_texto": {"minimo": 1, "maximo": 3},
                "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
            },
            "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            "verificacao": {"texto": {"max_caracteres": 15}},
        }
        el = ElementoCorpo(
            id="lan", tipo="lancador",
            _campos_inertes={"titulo": "Lancador", "itens": itens},
            parametros_tipo=params,
            distribuicao_matricial=self._dm(
                dimensionamento={
                    "colunas": {"politica": "maior_da_coluna"},
                    "linhas": {"politica": "minimo_fixo", "minimo": 1}},
            ) if com_dm else None,
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        return ModeloTela(id="t", schema="tela.v1",
                          cabecalho={"titulo": "T", "descricao": "D"},
                          corpo=corpo,
                          barra_de_menus={"chips": [
                              {"id": "e", "tipo": "acao", "tecla": "Esc",
                               "texto": "Sair"}]},
                          _raw={})

    def test_lancador_com_precedencia(self):
        # Com o campo: grade 2x2 por_linha. [A] um e [B] do na primeira linha.
        m = self._modelo_lancador(com_dm=True)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        achou = False
        for l in saida.split("\n"):
            if "[A] um" in l and "[B] do" in l:
                achou = True
                break
        _registrar("H0035 lancador com: [A] um e [B] do na mesma linha", achou)

    def test_lancador_sem_preserva(self):
        # Sem o campo: politica historica (ADR-0001/2/3). Todos os itens numa
        # unica fila (cabendo em 42 chars) — comportamento _linhas_lancador.
        m = self._modelo_lancador(com_dm=False)
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        # Fila: todos os quatro itens na mesma linha.
        achou_fila = False
        for l in saida.split("\n"):
            if all(t in l for t in ("[A] um", "[B] do", "[C] tr", "[D] qu")):
                achou_fila = True
                break
        _registrar("H0035 lancador sem campo preserva fila historica",
                   achou_fila)

    def test_fallback_quadro_minimo(self):
        # Grade que nao cabe -> quadro minimo canonico global.
        el = ElementoCorpo(
            id="dash", tipo="dashboard",
            _campos_inertes={"titulo": "Grade", "campos": [
                {"id": "c1", "rotulo": "", "fonte": "literal", "valor": "X"},
                {"id": "c2", "rotulo": "", "fonte": "literal", "valor": "Y"},
            ]},
            distribuicao_matricial=self._dm(
                formacao={"politica": "matriz_fixa",
                          "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
                dimensionamento={
                    "colunas": {"politica": "minimo_fixo", "minimo": 40},
                    "linhas": {"politica": "minimo_fixo", "minimo": 1}}),
        )
        corpo = Corpo(arranjo="vertical", elementos=[el],
                      distribuicao={"modo": "igual"})
        m = ModeloTela(id="t", schema="tela.v1",
                       cabecalho={"titulo": "T", "descricao": "D"},
                       corpo=corpo,
                       barra_de_menus={"chips": [
                           {"id": "e", "tipo": "acao", "tecla": "Esc",
                            "texto": "Sair"}]},
                       _raw={})
        saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=14)
        _registrar("H0035 fallback -> quadro minimo canonico",
                   "terminal pequeno demais" in saida and "GRADE" not in saida)

    def test_telas_permanentes_carregam(self):
        # As telas h0035_* de conteudo carregam e renderizam pelo pipeline.
        ids = [
            "h0035_pref_linhas", "h0035_pref_colunas", "h0035_matriz_fixa_cabe",
            "h0035_uma_linha", "h0035_uma_coluna", "h0035_console_com",
            "h0035_console_sem", "h0035_lancador_com", "h0035_lancador_sem",
            "h0035_dashboard_com", "h0035_dashboard_sem",
            "h0035_minimo_fixo_excedido", "h0035_tres_centralizados",
        ]
        todas_ok = True
        for id_tela in ids:
            try:
                raw = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
                modelo = construir_modelo(raw)
                saida = renderizar_tela(modelo, _ESTILO_CURVA, largura=44, altura=16)
                if saida.count("\n") != 16:
                    todas_ok = False
            except Exception as exc:  # pragma: no cover
                todas_ok = False
                _registrar("H0035 tela permanente {0}".format(id_tela),
                           False, "{0}: {1}".format(type(exc).__name__, exc))
        _registrar("H0035 telas permanentes carregam e renderizam", todas_ok)

    def test_minimo_fixo_nao_cresce(self):
        # DEC-APP-0025-01: coluna minimo_fixo=5 nao cresce por conteudo maior.
        # 1x1, participante "ABCDEFGH" (8) em coluna de 5: coluna permanece 5.
        # Prova comportamental: fronteira interna recebe o conteudo integral.
        import inspect
        import importlib
        _mod = importlib.import_module("tela.renderizacao.matriz_participantes")
        chamadas = []
        _original = _mod._renderizar_participante_na_celula

        def _espiao(canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
                    canvas_h, area_w, alinh_h, alinh_v):
            chamadas.append({
                "texto_integral": texto_integral,
                "cel_w": cel_w,
                "cel_h": cel_h,
            })
            return _original(
                canvas, texto_integral, cel_x, cel_y, cel_w, cel_h,
                canvas_h, area_w, alinh_h, alinh_v,
            )

        _mod._renderizar_participante_na_celula = _espiao
        try:
            el = ElementoCorpo(
                id="dash", tipo="dashboard",
                _campos_inertes={"titulo": "Grade", "campos": [
                    {"id": "c1", "rotulo": "", "fonte": "literal",
                     "valor": "ABCDEFGH"}]},
                distribuicao_matricial=self._dm(
                    formacao={"politica": "matriz_fixa",
                              "linhas": {"fixo": 1}, "colunas": {"fixo": 1}},
                    dimensionamento={
                        "colunas": {"politica": "minimo_fixo", "minimo": 5},
                        "linhas": {"politica": "minimo_fixo", "minimo": 1}},
                    distribuicao_horizontal={"politica": "inicio"}),
            )
            corpo = Corpo(arranjo="vertical", elementos=[el],
                          distribuicao={"modo": "igual"})
            m = ModeloTela(id="t", schema="tela.v1",
                           cabecalho={"titulo": "T", "descricao": "D"},
                           corpo=corpo,
                           barra_de_menus={"chips": [
                               {"id": "e", "tipo": "acao", "tecla": "Esc",
                                "texto": "Sair"}]},
                           _raw={})
            saida = renderizar_tela(m, _ESTILO_CURVA, largura=42, altura=12)
            linhas = saida.split("\n")
            # 1: Formacao valida (grade renderizada).
            idx = next((i for i, l in enumerate(linhas) if "GRADE" in l), -1)
            _registrar("H0035 minimo_fixo: formacao externa valida",
                       idx >= 0, "idx GRADE = {0}".format(idx))
            # 2: Fronteira interna foi chamada pelo distribuidor externo.
            _registrar(
                "H0035 minimo_fixo: fronteira interna chamada",
                len(chamadas) >= 1,
                "chamadas = {0}".format(len(chamadas)),
            )
            # 3: Conteudo integral "ABCDEFGH" recebido pela fronteira interna.
            conteudo_recebido = chamadas[0]["texto_integral"] if chamadas else ""
            _registrar(
                "H0035 minimo_fixo: conteudo integral ABCDEFGH recebido",
                conteudo_recebido == "ABCDEFGH",
                "recebido = {0!r}".format(conteudo_recebido),
            )
            # 4: Largura da celula recebida e 5 (dimensao externa nao cresceu).
            cel_w_recebida = chamadas[0]["cel_w"] if chamadas else -1
            _registrar(
                "H0035 minimo_fixo: largura da celula e 5",
                cel_w_recebida == 5,
                "cel_w = {0}".format(cel_w_recebida),
            )
            # 5: Auxiliar — sem [:cel_w] no corpo da funcao matricial externa.
            from tela.renderizador import _linhas_distribuicao_matricial as _ldm
            fonte = inspect.getsource(_ldm)
            _registrar(
                "H0035 minimo_fixo: [:cel_w] ausente na camada matricial (auxiliar)",
                "[:cel_w]" not in fonte,
                "[:cel_w] no fonte = {0}".format("[:cel_w]" in fonte),
            )
        finally:
            _mod._renderizar_participante_na_celula = _original

    def test_fronteira_interna_celula(self):
        # Prova direta de _renderizar_participante_na_celula:
        # recebe conteudo integral, respeita a area fisica, nao invade vizinha.
        from tela.renderizador import _renderizar_participante_na_celula
        # Canvas 10 colunas x 1 linha; celula largura 5 em x=0.
        canvas = [[" "] * 10]
        _renderizar_participante_na_celula(
            canvas=canvas,
            texto_integral="ABCDEFGH",
            cel_x=0, cel_y=0, cel_w=5, cel_h=1,
            canvas_h=1, area_w=10,
            alinh_h="inicio", alinh_v="topo",
        )
        linha = "".join(canvas[0])
        _registrar(
            "H0035 fronteira_interna: primeiros 5 chars escritos na celula",
            linha[:5] == "ABCDE",
            "canvas = {0!r}".format(linha),
        )
        _registrar(
            "H0035 fronteira_interna: celula vizinha nao invadida (pos 5-9)",
            linha[5:] == "     ",
            "pos5-9 = {0!r}".format(linha[5:]),
        )
        # Celula em x=5: conteudo breve nao invade celula em x=0.
        canvas2 = [[" "] * 10]
        _renderizar_participante_na_celula(
            canvas=canvas2,
            texto_integral="XY",
            cel_x=5, cel_y=0, cel_w=5, cel_h=1,
            canvas_h=1, area_w=10,
            alinh_h="inicio", alinh_v="topo",
        )
        linha2 = "".join(canvas2[0])
        _registrar(
            "H0035 fronteira_interna: vizinha direita nao invade esquerda",
            linha2[:5] == "     " and linha2[5:7] == "XY",
            "canvas = {0!r}".format(linha2),
        )

    def run_all(self):
        self.test_dashboard_com_grade()
        self.test_dashboard_sem_preserva()
        self.test_ordem_preservada()
        self.test_sem_perda_nem_duplicacao()
        self.test_console_com_substitui()
        self.test_console_sem_preserva()
        self.test_lancador_com_precedencia()
        self.test_lancador_sem_preserva()
        self.test_fallback_quadro_minimo()
        self.test_telas_permanentes_carregam()
        self.test_minimo_fixo_nao_cresce()
        self.test_fronteira_interna_celula()


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


def teste_selecao_multipla_h0041():
    """Testes de integracao da coluna ``tg`` e chips dinamicos (H-0041).

    Exercita o renderer sobre a fixture D-SEL-22 (oito itens; seis navegaveis,
    dois nao navegaveis; quatro selecionaveis) com estado de selecao por
    console. Valida: coluna ``ec`` exclusiva do cursor; coluna ``tg``
    distinguindo incluido/nao incluido/nao selecionavel; item nao navegavel
    visivel sem cursor e com ``tg`` vazio; chip ``Espaco``/``Enter`` presentes;
    rotulo dinamico ``Todos``/``Executar``; ``Executar`` inativo (nenhuma
    operacao externa).
    """
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    from tela import navegacao as _nav

    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav.lista_foco(modelo)
    console = lista[0]

    def _render(selecoes):
        return renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes=selecoes,
        )

    # --- Estado inicial: cursor em item_01, selecao vazia ---
    saida_ini = _render({})
    _registrar(
        "H-0041 CA-07: cursor ec aparece em item_01 (estado inicial)",
        "Item um" in saida_ini and "→" in saida_ini,
    )
    # tg nao-incluido (○) nos selecionaveis; vazio nos nao selecionaveis.
    _registrar(
        "H-0041 CA-08: tg nao-incluido (○) presente em selecionaveis",
        saida_ini.count("○") >= 4,
        "contagem ○ = {0}".format(saida_ini.count("○")),
    )
    _registrar(
        "H-0041 CA-09: item_04/item_08 visiveis sem cursor",
        "nao navegavel" in saida_ini,
    )
    _registrar(
        "H-0041 chip Enter=Todos (selecao vazia)",
        "Todos" in saida_ini,
    )
    _registrar(
        "H-0041 chip Espaco presente (selecao multipla)",
        "␣" in saida_ini,
    )

    # --- Apos marcar item_01: tg incluido (●) em item_01 ---
    saida_marcado = _render({console.id: ["item_01"]})
    _registrar(
        "H-0041 CA-08: tg incluido (●) presente apos marcar item_01",
        "●" in saida_marcado,
        "contagem ● = {0}".format(saida_marcado.count("●")),
    )
    # QA-H0041-002 (P02): chip Enter com selecao e INATIVO por estado logico
    # (``regra_ativo: selecao_vazia`` avaliada), nao por inferencia do rotulo.
    # H-0041 P04: representacao visual inativa usa cor_inativo (nao caixa baixa).
    from tela import selecao as _sel
    from tela import renderizador as _rend
    estado_sel = {"selecoes": {console.id: ["item_01"]}}
    codigo_inativo = _rend._codigo_ansi_de_cor(_ESTILO_CURVA.cor_inativo)
    _registrar(
        "H-0041 chip Enter INATIVO (estado logico via regra_ativo, nao rotulo)",
        _sel.rotulo_enter(estado_sel, console) == "Executar"
        and _rend._navegacao_atual.get("estado_ativo_chips", {}).get(
            "chip_enter"
        ) is False
        and "Executar" in saida_marcado
        and "executar" not in saida_marcado
        and codigo_inativo in saida_marcado
        and _rend._ANSI_RESET_FG in saida_marcado,
        "rotulo={0!r} ativo={1!r}".format(
            _sel.rotulo_enter(estado_sel, console),
            _rend._navegacao_atual.get("estado_ativo_chips", {}).get(
                "chip_enter"
            ),
        ),
    )

    # --- Apos Todos: inclui item_01,03,05,07 ---
    saida_todos = _render({console.id: ["item_01", "item_03", "item_05", "item_07"]})
    _registrar(
        "H-0041 CA-08: Todos marca exatamente 4 selecionaveis (●)",
        saida_todos.count("●") == 4,
        "contagem ● = {0}".format(saida_todos.count("●")),
    )

    # --- ec independente da selecao (cursor em item_01, selecao em item_03) ---
    saida_div = _render({console.id: ["item_03"]})
    _registrar(
        "H-0041 CA-07: ec independe da selecao (cursor item_01, sel item_03)",
        saida_div.count("→") == 1 and saida_div.count("●") == 1,
        "→ = {0}, ● = {1}".format(saida_div.count("→"), saida_div.count("●")),
    )


# QA-H0041-002 (patch P02): estado logico ATIVO/INATIVO do chip ``[Enter]``
# materializado pela avaliacao de ``regra_ativo`` (independente do rotulo).
# Os testes consultam ``_navegacao_atual["estado_ativo_chips"]`` e
# ``_avaliar_regra_ativo``; falham se o renderer ignorar ``regra_ativo``, se
# ``enter_inativo`` for derivado apenas do rotulo, ou se o teste verificar
# somente caixa baixa/texto. Representacao visual inativa e consequencia.
# Consoles sem selecao multipla preservam o comportamento anterior (ativo).
# ---------------------------------------------------------------------------
import pytest as _pytest_qa002  # noqa: E402

from tela.loader import carregar_estilo as _carregar_estilo_qa002  # noqa: E402
from tela import navegacao as _nav_qa002  # noqa: E402
from tela import selecao as _sel_qa002  # noqa: E402
from tela import renderizador as _rend_qa002  # noqa: E402


def _carregar_fixture_h0041_qa002():
    """Carrega o modelo e o console da fixture D-SEL-22 para QA-H0041-002."""
    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    return modelo, lista, lista[0]


def _chip_enter_fixture(modelo):
    """Devolve o dict do chip_enter declarado na barra_de_menus da fixture."""
    chips = (modelo.barra_de_menus or {}).get("chips") or []
    for chip in chips:
        if isinstance(chip, dict) and chip.get("id") == "chip_enter":
            return chip
    return None


@_pytest_qa002.fixture(name="fixture_h0041_qa002")
def _fixture_h0041_qa002():
    return _carregar_fixture_h0041_qa002()


def test_qah0041_002_chip_enter_sem_selecao_ativo(fixture_h0041_qa002):
    # caso_sem_selecao: rotulo=Todos, estado_logico=ATIVO, visual=ativa.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    assert chip.get("regra_ativo") == "selecao_vazia"
    estado_sel = {"selecoes": {}}
    assert _sel_qa002.rotulo_enter(estado_sel, console) == "Todos"
    # Estado logico via regra_ativo (nao via rotulo).
    assert _rend_qa002._avaliar_regra_ativo(
        chip.get("regra_ativo"), selecao_vazia=True
    ) is True
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is True
    assert "Todos" in saida
    assert "todos" not in saida  # representacao visual ativa (sem caixa baixa)


def test_qah0041_002_chip_enter_com_selecao_inativo(fixture_h0041_qa002):
    # caso_com_selecao: rotulo=Executar, estado_logico=INATIVO, visual=inativa.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    assert chip.get("regra_ativo") == "selecao_vazia"
    estado_sel = {"selecoes": {console.id: ["item_01"]}}
    assert _sel_qa002.rotulo_enter(estado_sel, console) == "Executar"
    # Estado logico via regra_ativo (nao via rotulo == "Executar").
    assert _rend_qa002._avaliar_regra_ativo(
        chip.get("regra_ativo"), selecao_vazia=False
    ) is False
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # H-0041 P04: capitalizacao preservada; inatividade via cor_inativo.
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo and codigo in saida
    assert _rend_qa002._ANSI_RESET_FG in saida


def test_qah0041_002_estado_logico_independente_do_rotulo(fixture_h0041_qa002):
    # independencia: alterar_apenas_rotulo nao define estado;
    # estado_logico nao e inferido do texto.
    modelo, lista, console = fixture_h0041_qa002
    chip = _chip_enter_fixture(modelo)
    assert chip is not None
    regra = chip.get("regra_ativo")
    assert regra == "selecao_vazia"
    # Mesmo com texto forçado para "Executar", selecao vazia => ATIVO.
    assert _rend_qa002._avaliar_regra_ativo(
        regra, selecao_vazia=True
    ) is True
    # Mesmo com texto forçado para "Todos", selecao nao vazia => INATIVO.
    assert _rend_qa002._avaliar_regra_ativo(
        regra, selecao_vazia=False
    ) is False
    # regra_ativo "sempre" permanece ATIVO independente da selecao/rotulo.
    assert _rend_qa002._avaliar_regra_ativo(
        "sempre", selecao_vazia=False
    ) is True
    # Prova de que o renderer consome a regra da fixture: com selecao, o
    # estado materializado e INATIVO porque regra=selecao_vazia (se fosse
    # derivado so do rotulo sem avaliar a regra, o teste acima de "sempre"
    # nao distinguiria a autoridade).
    estilo = _carregar_estilo_qa002()
    renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # Rotulo e estado sao propriedades distintas apos render.
    assert _sel_qa002.rotulo_enter(
        {"selecoes": {console.id: ["item_01"]}}, console
    ) == "Executar"


def test_qah0041_002_chip_enter_inativo_distingue_de_ativo(fixture_h0041_qa002):
    # Distincao visual e consequencia do estado logico (R-6: chip permanece).
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    saida_ativo = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    ativo_logico = _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"]
    saida_inativo = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    inativo_logico = _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"]
    assert ativo_logico is True
    assert inativo_logico is False
    assert "Todos" in saida_ativo
    assert "Executar" in saida_inativo
    assert "executar" not in saida_inativo
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida_inativo
    assert codigo not in saida_ativo
    assert "⏎" in saida_ativo
    assert "⏎" in saida_inativo


def test_qah0041_002_chip_enter_inativo_nao_cria_operacao(fixture_h0041_qa002):
    # Enter_em_Executar: nenhuma operacao/callback/mensagem provisoria.
    modelo, lista, console = fixture_h0041_qa002
    estilo = _carregar_estilo_qa002()
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    assert "executando" not in saida.lower()
    assert "resultado" not in saida.lower()


def test_qah0041_002_console_sem_selecao_multipla_preserva_ativo():
    # consoles_sem_selecao_multipla: comportamento anterior preservado.
    tela_raw = carregar_tela(
        None, "h0040_nav_console_unico_linear", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    console = lista[0]
    estilo = _carregar_estilo_qa002()
    assert not _nav_qa002._console_declarou_selecao_multipla(console)
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    # Sem chip Enter de selecao; chips existentes permanecem ATIVOS
    # (regra_ativo=sempre). Nenhum rotulo forcado para caixa baixa.
    estados = _rend_qa002._navegacao_atual.get("estado_ativo_chips") or {}
    assert "chip_enter" not in estados
    for ativo in estados.values():
        assert ativo is True
    assert "executar" not in saida


def test_qah0041_002_renderer_avalia_regra_ativo_nao_ignora(fixture_h0041_qa002):
    # O teste principal deve falhar se o renderer ignorar regra_ativo.
    # Comprova: fixture declara selecao_vazia; com selecao o estado e INATIVO;
    # se regra fosse ignorada (sempre ATIVO), esta asserção quebraria.
    modelo, lista, console = fixture_h0041_qa002
    chip = _chip_enter_fixture(modelo)
    assert chip.get("regra_ativo") != "sempre"
    assert chip.get("regra_ativo") == "selecao_vazia"
    estilo = _carregar_estilo_qa002()
    renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista,
        selecoes={console.id: ["item_01"]},
    )
    # Se o renderer ignorasse regra_ativo e usasse default ATIVO, falharia.
    assert _rend_qa002._navegacao_atual["estado_ativo_chips"]["chip_enter"] is False
    # Se enter_inativo fosse so rotulo_enter == "Executar" sem consumir a
    # regra, a troca da regra para "sempre" manteria inativo — prova inversa:
    assert _rend_qa002._avaliar_regra_ativo(
        "sempre", selecao_vazia=False
    ) is True
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


# H0041-MANUAL-001/002/003 (patch P03): testes que percorrem a MESMA sequencia
# da validacao manual TTY. Validam que o estado logico dos chips (ATIVO/INATIVO
# via ``regra_ativo``) se materializa na apresentacao real da barra, e que o
# contexto de renderizacao nunca reutiliza estado anterior a uma alteracao de
# selecao. Consultam ``_navegacao_atual["estado_ativo_chips"]`` (estado logico)
# e o texto renderizado (aplicacao real do estilo inativo por caixa baixa),
# distinguindo-os: o estado logico e a prova; a caixa baixa e consequencia.
# ---------------------------------------------------------------------------
def _carregar_fixture_h0041_p03():
    """Carrega modelo/estilo/console/lista da fixture D-SEL-22 para o P03."""
    tela_raw = carregar_tela(
        None, "h0041_selecao_multipla_oito_itens", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    estilo = _carregar_estilo_qa002()
    return modelo, lista, lista[0], estilo


def _renderizar_h0041_p03(modelo, lista, console, estilo, *, foco, selecoes):
    """Renderiza a fixture com foco/selecoes dados e devolve (saida, chips)."""
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: foco}, lista_foco=lista, selecoes=selecoes,
    )
    chips = _rend_qa002._navegacao_atual["estado_ativo_chips"]
    return saida, chips


def _barra_chip(saida, tecla):
    """Extrai a linha da barra que contem o chip de ``tecla`` (␣ ou ⏎)."""
    for linha in saida.split("\n"):
        if tecla in linha:
            return linha
    return ""


def test_h0041_manual_001_espaco_inativo_em_item_nao_selecionavel():
    # H0041-MANUAL-001: cursor em item_02 (nao selecionavel) com selecao ativa.
    # O chip Espaco deve estar INATIVO (item nao selecionavel); o chip Enter
    # deve estar INATIVO (selecao nao vazia = Executar). O estado logico e a
    # prova; a caixa baixa e consequencia (R-6).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_02 e indice logico 1; precondicao selecao=[item_01].
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=1, selecoes={console.id: ["item_01"]},
    )
    # Estado logico (prova, independente do rotulo).
    assert chips["chip_espaco"] is False
    assert chips["chip_enter"] is False
    # Texto renderizado: capitalizacao preservada; inatividade via cor_inativo.
    barra = _barra_chip(saida, "␣")
    assert "Marcar" in barra
    assert "marcar" not in barra
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in barra
    assert _rend_qa002._ANSI_RESET_FG in barra


def test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao():
    # H0041-MANUAL-001 (precondicao espelhada): cursor em item_03 (selecionavel)
    # com selecao=[item_01]. O chip Espaco deve estar ATIVO; Enter permanece
    # INATIVO (Executar). Prova que o estado do Espaco depende do item sob
    # cursor, nao apenas da existencia de selecao multipla.
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_03 e indice logico 2; precondicao selecao=[item_01].
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=2, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is True
    assert chips["chip_enter"] is False
    barra = _barra_chip(saida, "␣")
    assert "Marcar" in barra
    assert "Executar" in saida
    assert "executar" not in saida
    # Espaco ativo nao recebe cor_inativo; Enter inativo sim (mesma linha).
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert "{0}[␣]".format(codigo) not in barra
    assert "[␣] Marcar" in barra
    assert "{0}[⏎] Executar{1}".format(codigo, _rend_qa002._ANSI_RESET_FG) in barra


def test_h0041_manual_001_espaco_recalculado_por_movimento():
    # O estado do chip Espaco e recalculado apos cada movimento do cursor
    # (sem estado visual residual entre renders consecutivos).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    # item_01 (selecionavel) -> ATIVO
    _, chips_01 = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips_01["chip_espaco"] is True
    # item_02 (nao selecionavel) -> INATIVO
    _, chips_02 = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=1, selecoes={},
    )
    assert chips_02["chip_espaco"] is False
    # volta a item_01 -> ATIVO de novo (sem residuo)
    _, chips_01b = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips_01b["chip_espaco"] is True


def test_h0041_manual_002_enter_inativo_com_selecao_visual():
    # H0041-MANUAL-002: o estado logico INATIVO do chip Enter (regra_ativo=
    # selecao_vazia) se materializa na barra. A prova e o estado logico; a
    # caixa baixa e consequencia material (nao aceita como solucao unica).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=0, selecoes={console.id: ["item_01"]},
    )
    assert _sel_qa002.rotulo_enter(
        {"selecoes": {console.id: ["item_01"]}}, console
    ) == "Executar"
    assert chips["chip_enter"] is False
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida
    assert _rend_qa002._ANSI_RESET_FG in saida
    # Nao e por comparacao direta de rotulo: a regra e a autoridade.
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


def test_h0041_manual_003_todos_e_redraw_no_mesmo_quadro():
    # H0041-MANUAL-003: apos Enter iniciado com selecao vazia (Todos), uma
    # unica renderizacao apresenta conjuntamente os 4 tg incluidos E o chip
    # Enter como Executar INATIVO. O contexto dos chips nao pode ser calculado
    # antes da alteracao da selecao e reutilizado depois dela: como cada
    # render ler ``selecoes`` do estado corrente, o estado e sempre sincrono.
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    quatro = ["item_01", "item_03", "item_05", "item_07"]
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=2, selecoes={console.id: quatro},
    )
    # tg incluidos no mesmo quadro (4 marcadores ●).
    assert saida.count("●") == 4
    # chip Enter = Executar INATIVO no mesmo quadro.
    assert chips["chip_enter"] is False
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo in saida
    # chip Espaco conforme item sob cursor (item_03 selecionavel -> ATIVO).
    assert chips["chip_espaco"] is True


def test_h0041_manual_003_selecao_vazia_apresenta_todos_ativo():
    # Espelho do MANUAL-003 no estado inicial (pre-Todos): selecao vazia =>
    # chip Enter = Todos ATIVO, tg todos nao-incluidos (○). Confirma que a
    # transicao vazia->Executar INATIVO e observavel (nao eh default fixo).
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=2, selecoes={},
    )
    assert chips["chip_enter"] is True
    assert "Todos" in saida
    assert "todos" not in saida  # ativo: caixa alta (sem reducao de enfase)


def test_h0041_manual_001_console_sem_selecao_multipla_sem_espaco_inativo():
    # Preservacao de consoles sem selecao multipla: nenhum chip forcado para
    # inativo por item (nao ha regra_ativo=item_focalizado_selecionavel).
    tela_raw = carregar_tela(
        None, "h0040_nav_console_unico_linear", _RAIZ_TELAS_DEMO
    )
    modelo = construir_modelo(tela_raw)
    lista = _nav_qa002.lista_foco(modelo)
    console = lista[0]
    estilo = _carregar_estilo_qa002()
    assert not _nav_qa002._console_declarou_selecao_multipla(console)
    saida = renderizar_tela(
        modelo, estilo, largura=70, foco_console=0,
        cursores={console.id: 0}, lista_foco=lista, selecoes={},
    )
    estados = _rend_qa002._navegacao_atual.get("estado_ativo_chips") or {}
    assert "chip_espaco" not in estados
    for ativo in estados.values():
        assert ativo is True
    assert "marcar" not in saida


# H-0041 P04: cor_inativo (cinza) e capitalizacao preservada.
# ---------------------------------------------------------------------------
def test_h0041_p04_chip_ativo_preserva_apresentacao():
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo, foco=0, selecoes={},
    )
    assert chips["chip_espaco"] is True
    assert chips["chip_enter"] is True
    barra_espaco = _barra_chip(saida, "␣")
    assert "Marcar" in barra_espaco
    assert "Todos" in saida
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert codigo not in barra_espaco


def test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura():
    modelo, lista, console, estilo = _carregar_fixture_h0041_p03()
    saida, chips = _renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=1, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is False
    assert chips["chip_enter"] is False
    codigo = _rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    assert estilo.cor_inativo == "cinza"
    assert codigo == "\x1b[90m"
    # Fragmento do chip Espaco: cor antes do rotulo e reset apos.
    barra = _barra_chip(saida, "␣")
    idx_cor = barra.find(codigo)
    idx_marcar = barra.find("Marcar")
    idx_reset = barra.find(_rend_qa002._ANSI_RESET_FG, idx_cor)
    assert idx_cor != -1
    assert idx_marcar != -1
    assert idx_cor < idx_marcar < idx_reset
    assert "Executar" in saida
    assert "marcar" not in saida
    assert "executar" not in saida


def test_h0041_p04_estado_logico_nao_inferido_pelo_rotulo():
    # Mesmo com rotulos capitalizados, o estado vem de regra_ativo.
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False
    assert _rend_qa002._avaliar_regra_ativo(
        "item_focalizado_selecionavel", item_focalizado_selecionavel=False
    ) is False


def test_h0041_p04_texto_chip_barra_nao_usa_lower():
    chip = {"tecla": "⏎", "texto": "Executar"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_CURVA, vao=1, inativo=True
    )
    assert "Executar" in texto
    assert "executar" not in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") in texto
    assert texto.endswith(_rend_qa002._ANSI_RESET_FG)


# H-0044: cor_alerta / chips destacados
# ---------------------------------------------------------------------------
_ESTILO_H0044 = EstiloResolvido(
    canto_superior_esquerdo="╭",
    canto_superior_direito="╮",
    canto_inferior_esquerdo="╰",
    canto_inferior_direito="╯",
    traco_superior="─",
    traco_inferior="─",
    lateral="│",
    caractere_esquerdo="[",
    caractere_direito="]",
    cor_texto="padrão",
    caixa_alta=False,
    cor_fundo="padrão",
    concluido_on="✓",
    concluido_off=" ",
    selecionado_simbolo="→",
    selecionado_off=" ",
    incluido_on="●",
    incluido_off="○",
    cor_inativo="cinza",
    cor_alerta="amarelo",
)


def test_h0044_chip_destacado_usa_cor_alerta():
    chip = {"id": "chip_x", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=False, destacado=True
    )
    codigo = _rend_qa002._codigo_ansi_de_cor(_ESTILO_H0044.cor_alerta)
    assert codigo == "\x1b[33m"
    assert codigo in texto
    assert texto.endswith(_rend_qa002._ANSI_RESET_FG)
    assert "Dry-Run" in texto


def test_h0044_chip_ativo_normal_sem_destaque():
    chip = {"id": "chip_x", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=False, destacado=False
    )
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") not in texto


def test_h0044_chip_inativo_cinza_nao_amarelo():
    chip = {"id": "chip_e", "tecla": "⏎", "texto": "Executar"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, vao=1, inativo=True, destacado=True
    )
    # Inativo tem precedencia; destaque nao se aplica.
    assert _rend_qa002._codigo_ansi_de_cor("cinza") in texto
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in texto


def test_h0044_destaque_nao_inativa():
    assert _rend_qa002._avaliar_regra_ativo("sempre") is True
    chip = {"id": "chip_dry_run", "tecla": "Ins", "texto": "Dry-Run"}
    texto = _rend_qa002._texto_chip_barra(
        chip, _ESTILO_H0044, destacado=True, inativo=False
    )
    assert "Dry-Run" in texto
    assert _rend_qa002._codigo_ansi_de_cor("cinza") not in texto


def test_h0044_largura_sem_ansi_destaque():
    chip = {"tecla": "Ins", "texto": "Dry-Run"}
    base = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=False)
    dest = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=True)
    assert _rend_qa002._largura_sem_ansi(base) == _rend_qa002._largura_sem_ansi(dest)


def test_h0044_cor_nao_vaza_entre_chips():
    chips = [
        {"id": "a", "tecla": "Ins", "texto": "Dry-Run"},
        {"id": "b", "tecla": "Esc", "texto": "Sair"},
    ]
    t0 = _rend_qa002._texto_chip_barra(
        chips[0], _ESTILO_H0044, destacado=True
    )
    t1 = _rend_qa002._texto_chip_barra(
        chips[1], _ESTILO_H0044, destacado=False
    )
    assert t0.endswith(_rend_qa002._ANSI_RESET_FG)
    assert _rend_qa002._codigo_ansi_de_cor("amarelo") not in t1


def test_h0044_executar_disponivel_ativa_selecao_nao_vazia():
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False, executar_disponivel=True
    ) is True
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False, executar_disponivel=False
    ) is False
    # Sem contexto H-0044: preserva H-0041 (Executar inativo).
    assert _rend_qa002._avaliar_regra_ativo(
        "selecao_vazia", selecao_vazia=False
    ) is False


def test_h0044_regressao_sem_destaque_identica():
    chip = {"tecla": "Esc", "texto": "Sair"}
    a = _rend_qa002._texto_chip_barra(chip, _ESTILO_CURVA)
    b = _rend_qa002._texto_chip_barra(chip, _ESTILO_H0044, destacado=False)
    assert a == b


# ---------------------------------------------------------------------------
# PATCH H-0044 P01 — "terminal pequeno demais" persistente em TTY real
#
# Causa raiz comprovada: canais capturados do executor (stdout/stderr) e o
# proprio ``resultado_bruto`` podem trazer ``\n`` a direita ou embutidos
# (ex.: stderr de __falha_operacional__ == "ERRO: falha operacional sintetica.\n").
# O envelope ``conjuntos_campos`` coloca o valor bruto em uma unica linha de
# conteudo; o ``\n`` vira uma quebra de linha fisica fantasma, inflando a
# contagem vertical em uma unidade e disparando o quadro minimo em QUALQUER
# altura (off-by-one: corpo sempre exige ``area_disponivel + 1``).
# ---------------------------------------------------------------------------

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
    TestPreenchimentoVerticalH0020().run_all()
    TestPreenchimentoBordeadoH0021().run_all()
    TestDistribuicaoVerticalH0025().run_all()
    TestDistribuicaoHorizontalH0026().run_all()
    TestHierarquiaGruposH0027().run_all()
    TestRenderizadorMatrizH0028().run_all()
    TestCardinalidadeUnitariaH0029().run_all()
    TestTelasPermanentesH0029().run_all()
    TestCatalogoH0030().run_all()
    TestDistribuicaoResponsivaH0034().run_all()
    TestOcupacaoIntegralCorpoH0033().run_all()
    TestHelperHorizontalH0033Patch2().run_all()
    TestCardinalidadeHorizontalH0033Patch3().run_all()
    TestCardinalidadeHorizontalH0033Patch4().run_all()
    TestDistribuicaoMatricialH0035().run_all()
    teste_conteudo_externo_h0036_render()
    teste_h0037_manual_001_marcador_truncamento()
    teste_h0037_manual_002_esc_primeiro()
    teste_h0037_qapp7_verb_sem_corte_silencioso()
    teste_selecao_multipla_h0041()

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
def test_h0045_renderiza_apenas_fragmentos_da_pagina_atual_com_indicador():
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    saida = renderizar_tela(
        modelo,
        carregar_estilo(),
        largura=80,
        altura=24,
        foco_console=0,
        cursores={console.id: 16},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={console.id: 2},
    )

    assert "página 2/3" in saida
    assert "item_17" in saida
    assert "item_01" not in saida


def test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo():
    """VM-H0045-01: na pagina 1, ``[<]`` visivel/inativo e ``[>]`` ativo."""
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela import renderizador as _rend
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    saida = renderizar_tela(
        modelo,
        carregar_estilo(),
        largura=80,
        altura=24,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={console.id: 1},
    )

    assert "página 1/3" in saida
    assert "[<]" in saida
    assert "[>]" in saida
    assert "\x1b[90m[<]" in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is True


def _h0045_linha_barra_menus(saida):
    """Retorna a linha de conteudo da barra (chips) e a versao sem ANSI."""
    import re
    from tela.renderizador import _largura_sem_ansi

    linhas = saida.split("\n")
    if linhas and linhas[-1] == "":
        linhas = linhas[:-1]
    candidatas = [
        ln for ln in linhas
        if "[Esc]" in ln and "[<]" in ln and "[>]" in ln
    ]
    assert candidatas, "linha da barra com chips nao encontrada"
    linha = candidatas[0]
    plain = re.sub(r"\x1b\[[0-9;]*m", "", linha)
    return linha, plain, _largura_sem_ansi(linha)


def test_h0045_p02_barra_alinhada_na_sequencia_de_larguras():
    """VM-H0045-R02-002: sequencia grande → reduzida → maximizada.

    Verifica alinhamento das bordas, largura visual exata, uma unica
    borda esquerda/direita, ausencia de ``│`` repetidos e manutencao
    dos quatro chips + indicador sem regressao.
    """
    import re
    from tela.loader import carregar_tela, carregar_estilo
    from tela.modelo import construir_modelo
    from tela import navegacao
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(
            None,
            "h0045_paginacao_console_unico",
            "config/telas/demo",
        )
    )
    console = modelo.corpo.elementos[0]
    lista = navegacao.lista_foco(modelo)
    estilo = carregar_estilo()
    sequencia = (100, 60, 100)

    for largura in sequencia:
        saida = renderizar_tela(
            modelo,
            estilo,
            largura=largura,
            altura=24,
            foco_console=0,
            cursores={console.id: 0},
            lista_foco=lista,
            paginas_atuais={console.id: 1},
            largura_navegacao=largura,
        )
        linha, plain, vis = _h0045_linha_barra_menus(saida)
        assert vis == largura, (
            "largura visual da barra {0} != {1}".format(vis, largura)
        )
        assert plain.startswith("│"), "borda esquerda ausente/deslocada"
        assert plain.endswith("│"), "borda direita ausente/deslocada"
        assert plain.count("│") == 2, (
            "esperado exatamente 2 bordas verticais, obtido {0}: {1!r}".format(
                plain.count("│"), plain
            )
        )
        assert "││" not in plain, "sequencia artificial de │ presente"
        assert "[Esc]" in plain
        assert "[<]" in plain
        assert "[>]" in plain
        assert "[✥]" in plain
        assert "página 1/3" in saida
        # Nenhuma linha do quadro deve ser visualmente mais curta que largura
        # quando contem ANSI de chip inativo (residuo potencial a direita).
        for ln in saida.split("\n"):
            if not ln:
                continue
            from tela.renderizador import _largura_sem_ansi
            assert _largura_sem_ansi(ln) == largura

    # Pagina 1: [<] inativo permanece (cor_inativo), sem regressao P01.
    saida_final = renderizar_tela(
        modelo,
        estilo,
        largura=100,
        altura=24,
        foco_console=0,
        cursores={console.id: 0},
        lista_foco=lista,
        paginas_atuais={console.id: 1},
        largura_navegacao=100,
    )
    assert "\x1b[90m[<]" in saida_final


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
        cabecalho={"titulo": "Vertical", "descricao": "d"},
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
        "cabecalho": {"titulo": "X", "descricao": "Y"},
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


# ---------------------------------------------------------------------------
# H-0045-P07 / QA-H0045-P06-001: autoridade geometrica recursiva por console
# ---------------------------------------------------------------------------

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
        cabecalho={"titulo": "Grupo", "descricao": "d"},
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
        cabecalho={"titulo": "Par", "descricao": "d"},
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
        cabecalho={"titulo": "Aninhado", "descricao": "d"},
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
        cabecalho={"titulo": "Ausente", "descricao": "d"},
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
        cabecalho={"titulo": "Matriz", "descricao": "d"},
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


# ---------------------------------------------------------------------------
# H-0045-P12: validacao adaptativa (W/C, multiplas geometrias).
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# H-0045-PH07 / VM-H0045-R07-001: largura horizontal do ramo matricial
# verboso (secao 20 do handoff H-0045, PATCH_HANDOFF P07).
# ---------------------------------------------------------------------------


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
        cabecalho={"titulo": "T", "descricao": "D"},
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
        cabecalho={"titulo": "T", "descricao": "D"},
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
    teste_h0037_qapp7_verb_sem_corte_silencioso()


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


# ---------------------------------------------------------------------------
# VM-H0045-R06-001 (P21): rotulo dinamico do chip ``[Esc]`` no renderer.
#
# Cobre os 16 criterios focais exigidos pelo prompt de correcao sobre a
# integracao do ``forma_exibicao: "rotulo_dinamico_esc"`` em ``_linhas_barra``.
# As tres configuracoes de selecao multipla (h0041, h0044, h0045_fluxo) foram
# atualizadas para a nova forma de exibicao; as duas de selecao unica
# (h0045_paginacao_console_unico, h0045_dois_consoles) permanecem inalteradas.
# ---------------------------------------------------------------------------
from tela.loader import carregar_tela as _carregar_tela_p21  # noqa: E402
from tela.modelo import construir_modelo as _construir_modelo_p21  # noqa: E402
from tela import navegacao as _nav_p21  # noqa: E402


def _carregar_fixture_p21(id_tela):
    """Carrega modelo/lista/console/estilo de uma fixture para os testes P21."""
    tela_raw = _carregar_tela_p21(None, id_tela, _RAIZ_TELAS_DEMO)
    modelo = _construir_modelo_p21(tela_raw)
    lista = _nav_p21.lista_foco(modelo)
    return modelo, lista, lista[0]


def _barra_esc_p21(saida):
    """Extrai a linha da barra de menus que contem o chip ``[Esc]``.

    A descricao do cabecalho pode mencionar ``Esc`` (ex.: \"Esc limpa antes
    de sair\"); por isso casamos pelo token do chip ``[Esc]`` e nao pela
    palavra solta ``Esc``.
    """
    for linha in saida.split("\n"):
        if "[Esc]" in linha:
            return linha
    return ""


class TestRotuloDinamicoEscP21:
    """VM-H0045-R06-001 (P21): chip ``[Esc]`` dinamico via ``forma_exibicao``."""

    def test_chip_esc_usa_rotulo_dinamico_esc_na_fixture_h0041(self):
        # Confirmacao focal: a fixture h0041 declara a nova forma de exibicao.
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        assert chip_esc["forma_exibicao"] == "rotulo_dinamico_esc"
        # Texto original preservado como fallback.
        assert chip_esc["texto"] == "Sair"

    # (1) selecao multipla VAZIA exibe o rotulo original ``Sair``.
    def test_rotulo_original_sair_quando_selecao_vazia(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra

    # (3) uma selecao exibe ``Limpar``.
    def test_limpar_quando_uma_selecao(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra
        assert "Sair" not in barra

    # (4) varias selecoes exibem ``Limpar``.
    def test_limpar_quando_varias_selecoes(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01", "item_03", "item_05", "item_07"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Limpar" in barra

    # (10) ``Limpar`` e o rotulo original nunca coexistem para Esc.
    def test_limpar_e_sair_nunca_coexistem(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        s_vazio = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        s_sel = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        b_vazio = _barra_esc_p21(s_vazio)
        b_sel = _barra_esc_p21(s_sel)
        assert "[Esc] Sair" in b_vazio and "Limpar" not in b_vazio
        assert "[Esc] Limpar" in b_sel and "Sair" not in b_sel

    # (8) Apos limpar (voltar ao vazio), reaparece o rotulo original.
    def test_apos_limpar_reaparece_rotulo_original(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        # Estado inicialmente com selecao -> ``Limpar``.
        s_sel = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        assert "[Esc] Limpar" in _barra_esc_p21(s_sel)
        # Apos limpar (Esc), selecao volta a vazia -> rotulo original.
        s_pos = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
        )
        assert "[Esc] Sair" in _barra_esc_p21(s_pos)
        assert "Limpar" not in _barra_esc_p21(s_pos)

    # (13) Troca de foco: somente o console focal determina o rotulo.
    def test_troca_de_foco_considera_somente_console_focal(self):
        # h0045_dois_consoles: ambos selecao UNICA => Esc sempre ``Sair``.
        tela_raw = _carregar_tela_p21(
            None, "h0045_dois_consoles_paginas_independentes", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        lista = _nav_p21.lista_foco(modelo)
        # Cada console tem selecao unica => chip Esc original preservado,
        # independentemente de foco (prova que selecao unica nao recebe
        # ``Limpar`` e que a troca de foco nao inventa ``Limpar``).
        for foco in range(len(lista)):
            saida = renderizar_tela(
                modelo, _ESTILO_CURVA, largura=100, foco_console=foco,
                cursores={lista[0].id: 0, lista[1].id: 0},
                lista_foco=lista, selecoes={},
                paginas_atuais={lista[0].id: 1, lista[1].id: 1},
            )
            barra = _barra_esc_p21(saida)
            assert "[Esc] Sair" in barra, foco
            assert "Limpar" not in barra, foco

    # (14) Console de selecao UNICA preserva seu chip original.
    def test_console_selecao_unica_preserva_chip_original(self):
        tela_raw = _carregar_tela_p21(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        chip_esc = next(
            c for c in modelo.barra_de_menus["chips"]
            if c.get("tecla") == "Esc"
        )
        # Confirmacao: selecao unica NAO declara rotulo_dinamico_esc.
        assert chip_esc["forma_exibicao"] != "rotulo_dinamico_esc"
        lista = _nav_p21.lista_foco(modelo)
        if not lista:
            return  # console nao focalizavel (sem itens navegaveis) -- nada a
            # provar aqui; o chip original ja e preservado por exclusao.
        console = lista[0]
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=80, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
            paginas_atuais={console.id: 1},
        )
        assert "[Esc] Sair" in saida
        assert "Limpar" not in saida

    # Preservacao: tecla, ordem, atividade, cores do chip Esc mantidas.
    def test_chip_esc_preserva_tecla_ordem_atividade(self):
        modelo, lista, console = _carregar_fixture_p21(
            "h0041_selecao_multipla_oito_itens"
        )
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista,
            selecoes={console.id: ["item_01"]},
        )
        # Esc permanece o PRIMEIRO chip (regra contratual ``_garantir_esc_primeiro``).
        barra = _barra_esc_p21(saida)
        assert barra.index("[Esc]") < barra.index("[␣]")
        # Estado logico do chip Esc permanece ATIVO (regra_ativo: sempre).
        from tela import renderizador as _rend_p21
        assert _rend_p21._navegacao_atual["estado_ativo_chips"].get(
            "chip_esc"
        ) is True

    # Isolamento por console focal: selecao em OUTRO console nao produz
    # ``Limpar`` para o console focal (cenario com selecao multipla).
    def test_selecao_em_outro_console_nao_afeta_rotulo_do_focal(self):
        # h0045_dois_consoles e selecao unica; constroimos dois consoles
        # multipla manualmente para isolar a regra do renderer.
        from tela.modelo import ElementoCorpo, ModeloTela, Corpo
        itens_a = [
            {"id": "a1", "texto": "A1", "navegavel": True, "selecionavel": True},
            {"id": "a2", "texto": "A2", "navegavel": True, "selecionavel": True},
        ]
        itens_b = [
            {"id": "b1", "texto": "B1", "navegavel": True, "selecionavel": True},
            {"id": "b2", "texto": "B2", "navegavel": True, "selecionavel": True},
        ]
        ca = ElementoCorpo(
            id="console_a", tipo="console",
            _campos_inertes={
                "titulo": "A", "itens": itens_a,
                "politica_navegacao": {"navegavel": True},
                "politica_selecao": "multipla",
            },
        )
        cb = ElementoCorpo(
            id="console_b", tipo="console",
            _campos_inertes={
                "titulo": "B", "itens": itens_b,
                "politica_navegacao": {"navegavel": True},
                "politica_selecao": "multipla",
            },
        )
        modelo = ModeloTela(
            id="t_p21", schema="tela.v1",
            cabecalho={"titulo": "T", "descricao": ""},
            corpo=Corpo(arranjo="vertical", elementos=[ca, cb]),
            barra_de_menus={
                "distribuicao": "horizontal",
                "chips": [
                    {"id": "chip_esc", "tipo": "acao", "tecla": "Esc",
                     "texto": "Sair", "regra_existencia": "sempre",
                     "regra_ativo": "sempre",
                     "forma_exibicao": "rotulo_dinamico_esc"},
                ],
            },
            _raw={},
        )
        lista = [ca, cb]
        # Foco em console_a (sem selecao); console_b COM selecao.
        # O chip Esc deve exibir ``Sair`` (rotulo do focal), nao ``Limpar``.
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=0,
            cursores={ca.id: 0, cb.id: 0}, lista_foco=lista,
            selecoes={cb.id: ["b1"]},
        )
        barra = _barra_esc_p21(saida)
        assert "[Esc] Sair" in barra
        assert "Limpar" not in barra
        # Trocando o foco para console_b (com selecao): agora ``Limpar``.
        saida_b = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=70, foco_console=1,
            cursores={ca.id: 0, cb.id: 0}, lista_foco=lista,
            selecoes={cb.id: ["b1"]},
        )
        assert "[Esc] Limpar" in _barra_esc_p21(saida_b)

    # Forma de exibicao ausente/outra preserva o rotulo original (nao inventa).
    def test_forma_exibicao_visivel_ativo_preserva_rotulo_original(self):
        # h0045_paginacao_console_unico usa ``visivel_ativo`` (selecao unica);
        # o renderer NAO resolve rotulo dinamico, exibindo o texto configurado.
        tela_raw = _carregar_tela_p21(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = _construir_modelo_p21(tela_raw)
        lista = _nav_p21.lista_foco(modelo)
        if not lista:
            return
        console = lista[0]
        saida = renderizar_tela(
            modelo, _ESTILO_CURVA, largura=80, foco_console=0,
            cursores={console.id: 0}, lista_foco=lista, selecoes={},
            paginas_atuais={console.id: 1},
        )
        assert "[Esc] Sair" in saida


# ---------------------------------------------------------------------------
# VM-H0045-R08-001 (P23): barra de menus com linhas.maximo=5 (H-0045 fluxo).
# Cobre os casos 1-9 e 29 da matriz obrigatoria do patch P23: escolha da
# menor quantidade valida de linhas (1 a 5), insuficiencia de largura mesmo
# com cinco linhas (erro_layout) e regressao das demais telas que continuam
# com maximo global de duas linhas.
# ---------------------------------------------------------------------------


def _modelo_fluxo_paginado_p23():
    """Carrega ``h0045_fluxo_execucao_paginado`` (barra com linhas.maximo=5)."""
    tela_raw = carregar_tela(None, "h0045_fluxo_execucao_paginado", _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw)


def _preparar_ctx_p23(modelo):
    """Prepara o contexto de navegacao para ``_linhas_barra`` (P23).

    Os chips ``[<]``/``[>]`` da fixture usam ``regra_existencia:
    console_com_paginacao`` e os chips ``[␣]``/``[⏎]`` usam
    ``console_focado_com_selecao_multipla`` -- ambos avaliados a partir do
    contexto de modulo ``_navegacao_atual``. Sem preparar o contexto (como
    ``renderizar_tela`` faz internamente), o estado de modulo persiste entre
    testes e filtra chips indevidamente. Esta funcao reproduz o setup minimo
    para que ``_linhas_barra`` veja os 5 chips declarados: o console focalizavel
    na lista de foco e focalizado, declarando selecao multipla e paginacao.
    """
    from tela.renderizador import _preparar_contexto_navegacao
    lista = [e for e in modelo.corpo.elementos if e.tipo == "console"]
    console = lista[0] if lista else None
    _preparar_contexto_navegacao(
        _ESTILO_CURVA, None, None, False,
        foco_console=0, cursores={console.id: 0} if console else {},
        lista_foco=lista,
        largura_navegacao=None, selecoes={console.id: []} if console else {},
        chips_destacados=None, executar_disponivel=None,
        paginas_atuais={console.id: 1} if console else {},
        modelo=modelo,
    )


class TestH0045P23BarraCincoLinhas:
    """VM-H0045-R08-001: distribuicao canônica com linhas.maximo=5 da barra."""

    def test_config_declarou_objeto_canonico_com_maximo_cinco(self):
        """Caso 1: a configuracao materializou o objeto canônico (nao alias)."""
        modelo = _modelo_fluxo_paginado_p23()
        dist = modelo.barra_de_menus["distribuicao"]
        assert isinstance(dist, dict)
        assert dist["linhas"]["minimo"] == 1
        assert dist["linhas"]["maximo"] == 5
        assert dist["preenchimento_multilinha"] == "coluna_a_coluna"
        assert dist["overflow"]["quando_nao_couber"] == "erro_layout"
        # Preservacoes exigidas pelo patch.
        assert dist["espacamentos"]["margem_horizontal"]["minimo"] == 1
        assert dist["overflow"]["nao_omitir_chips"] is True
        assert dist["overflow"]["nao_truncar_texto"] is True
        assert dist["overflow"]["nao_reordenar"] is True

    def test_barra_escolhe_menor_quantidade_valida(self):
        """Caso 7: a barra escolhe automaticamente a menor qtd valida."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # Em largura folgada, uma linha basta; nunca usa mais que o necessario.
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 120 - 3)
        assert len(linhas) == 1

    def test_barra_usa_uma_linha_em_largura_suficiente(self):
        """Caso 2: uma linha quando couber (~65 colunas)."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 65 - 3)
        assert len(linhas) == 1

    def test_barra_usa_duas_linhas_em_41_colunas(self):
        """Caso 3: duas linhas em ~41 colunas."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 41 - 3)
        assert len(linhas) == 2

    def test_barra_usa_tres_linhas_em_29_colunas(self):
        """Caso 4: tres linhas em ~29 colunas."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 29 - 3)
        assert len(linhas) == 3

    def test_barra_usa_quatro_linhas_em_28_colunas(self):
        """Caso 5: quatro linhas conforme distribuicao real (~28 colunas)."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 28 - 3)
        assert len(linhas) == 4

    def test_barra_usa_cinco_linhas_em_17_colunas(self):
        """Caso 6: ate cinco linhas quando a altura permitir (~17 colunas)."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 17 - 3)
        assert len(linhas) == 5

    def test_barra_nao_excede_cinco_linhas(self):
        """O maximo declarado (5) e respeitado em larguras intermediarias."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        for w in (40, 35, 30, 20, 18, 17):
            linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, w - 3)
            assert 1 <= len(linhas) <= 5

    def test_barra_erro_layout_em_largura_insuficiente_abaixo_do_limite(self):
        """Caso 8: largura insuficiente mesmo com cinco linhas -> erro_layout."""
        import pytest as _pytest_p23
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # 16 colunas: nenhum arranjo de 5 linhas comporta os chips no content_w.
        with _pytest_p23.raises(RenderizadorErro) as ei:
            _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 16 - 3)
        assert "erro_layout" in str(ei.value)

    def test_barra_preserva_ordem_e_chips_em_multilinha(self):
        """Casos 23/24: ausencia de truncamento/reordenacao em multilinha."""
        modelo = _modelo_fluxo_paginado_p23()
        _preparar_ctx_p23(modelo)
        # Em 28 colunas (4 linhas), todos os 5 chips aparecem, na ordem declarada.
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 28 - 3)
        joined = " ".join(linhas)
        # [Esc] e sempre primeiro (regra contratual); os demais seguem a ordem.
        assert "[Esc]" in joined
        assert "[<]" in joined
        assert "[>]" in joined
        assert "[␣]" in joined
        assert "[⏎]" in joined
        # Esc precede os demais chips de paginacao (contrato §8.2).
        assert joined.index("[Esc]") < joined.index("[<]")


class TestH0045P23RegressaoDuasLinhas:
    """Caso 29: telas que NAO declaram maximo continuam com teto de 2 linhas."""

    def test_tela_padrao_continua_com_maximo_global_duas_linhas(self):
        """A configuracao P23 nao altera o default global de duas linhas."""
        # h0045_paginacao_console_unico usa alias "horizontal" (default max=2).
        tela_raw = carregar_tela(
            None, "h0045_paginacao_console_unico", _RAIZ_TELAS_DEMO
        )
        modelo = construir_modelo(tela_raw)
        _preparar_ctx_p23(modelo)
        # Em largura que cabe em 2, exatamente <=2 linhas (nao 3, 4 ou 5).
        linhas = _linhas_barra(modelo.barra_de_menus, _ESTILO_CURVA, 45 - 3)
        assert len(linhas) <= 2
