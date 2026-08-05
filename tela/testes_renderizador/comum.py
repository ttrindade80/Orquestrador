"""Helpers e estado compartilhados pelos testes do renderizador."""

import os
from pathlib import Path

from tela.loader import carregar_tela, EstiloResolvido
from tela.modelo import Corpo, ElementoCorpo, ModeloTela, construir_modelo

_BASE_PADRAO = Path(__file__).resolve().parents[2]


_RESULTADOS = []


_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")


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


def _funcional(fid, tipo, titulo=None):
    """Helper: cria ElementoCorpo funcional simples."""
    inertes = {}
    if titulo:
        inertes["titulo"] = titulo
    if tipo == "lancador":
        inertes["itens"] = []
    return ElementoCorpo(id=fid, tipo=tipo, _campos_inertes=inertes)


def _grupo(gid, arranjo, filhos, distribuicao=None):
    """Helper: cria ElementoCorpo tipo 'grupo' com arranjo e filhos."""
    inertes = {}
    if arranjo is not None:
        inertes["arranjo"] = arranjo
    if distribuicao is not None:
        inertes["distribuicao"] = distribuicao
    return ElementoCorpo(id=gid, tipo="grupo", _campos_inertes=inertes,
                         elementos=filhos)


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


def _modelo_h0029(elementos, corpo_dist=None, largura=42):
    """Cria ModeloTela sintetico para testes H-0029.

    Cabecalho de 3 linhas, barra de 3 linhas com chip unico.
    Para largura=42 e altura=20: l_corpo_disponivel=14.
    """
    return ModeloTela(
        id="teste_h0029",
        schema="tela.v1",
        cabecalho={"titulo": "H0029", "descricao": "h0029", "apresentacao": {"titulo": {"posicao": "esquerda", "recuo_lateral": 0, "capitalizacao": "maiusculas", "formato_na_borda": "com_espacos_laterais"}, "descricao": {"max_caracteres": 200, "alinhamento": "esquerda", "recuo": 1, "capitalizacao": "preservar"}}},
        corpo=Corpo(arranjo="vertical", elementos=elementos, distribuicao=corpo_dist),
        barra_de_menus={"chips": [{"id": "esc", "tecla": "Esc", "texto": "Voltar"}]},
        _raw={},
    )


def _h0029_linhas_totais(saida):
    return len(saida.splitlines())


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
