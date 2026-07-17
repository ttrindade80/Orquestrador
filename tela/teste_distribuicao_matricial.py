"""Testes do motor geometrico da distribuicao matricial (H-0035 / ADR-0025).

Executavel via:
    python tela/teste_distribuicao_matricial.py

Cobre (contrato H-0035 secao 37.3): todas as formacoes; ambas as ordens;
dimensionamento por linha/coluna/uniforme/minimo_fixo; tratamento interno;
margens; vaos; maximos; ordem de expansao; restos; alinhamentos;
cardinalidade unitaria; uma linha; uma coluna; formacao impossivel; fallback;
recuperacao; determinismo; ausencia de efeito parcial.

Independencia dos valores esperados (secao 37.9): as expectativas geometricas
sao derivadas manualmente por geometria fechada nos comentarios; nenhum teste
recalcula o valor esperado chamando o proprio algoritmo de producao.

Apenas biblioteca padrao do Python.
"""

import os
import sys
from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(_BASE_PADRAO))

from tela.distribuicao_matricial import (  # noqa: E402
    calcular_distribuicao,
    alinhar_na_celula,
    DistribuicaoMatricialErro,
)

_RESULTADOS = []


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _ok(nome, cond, detalhe=""):
    _registrar(nome, bool(cond), detalhe)


def _cfg(**over):
    """Config base valida; sobreposicoes por caminho pontilhado nao suportadas —
    usar dicts completos por chave."""
    base = {
        "formacao": {"politica": "preferencia_linhas", "linhas": {"minimo": 1}},
        "ordem": "por_linha",
        "dimensionamento": {
            "colunas": {"politica": "uniforme"},
            "linhas": {"politica": "uniforme"},
        },
        "espacamento": {
            "margem_superior": {"minimo": 0},
            "margem_inferior": {"minimo": 0},
            "margem_esquerda": {"minimo": 0},
            "margem_direita": {"minimo": 0},
            "vao_horizontal": {"minimo": 0},
            "vao_vertical": {"minimo": 0},
        },
        "distribuicao_horizontal": {"politica": "inicio"},
        "distribuicao_vertical": {"politica": "inicio"},
        "ordem_expansao": {
            "horizontal": "uniforme_margens_e_vaos",
            "vertical": "uniforme_margens_e_vaos",
        },
        "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
        "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
    }
    base.update(over)
    return base


def teste_formacao_pref_linhas():
    # 4 participantes, pref_linhas minimo=2, maximo=2 -> 2 linhas, ceil(4/2)=2 colunas.
    c = _cfg(formacao={"politica": "preferencia_linhas",
                       "linhas": {"minimo": 2, "maximo": 2}})
    r = calcular_distribuicao(20, 10, 4, c, min_ws=[1, 1, 1, 1], min_hs=[1, 1, 1, 1])
    _ok("pref_linhas formacao 2x2", r["formacao"] == (2, 2), str(r["formacao"]))
    _ok("pref_linhas sem fallback", r["fallback"] is False)


def teste_formacao_pref_colunas():
    # 6 participantes, pref_colunas minimo=3 -> tenta 3 colunas primeiro:
    # ceil(6/3)=2 linhas. Formacao esperada (2, 3).
    c = _cfg(formacao={"politica": "preferencia_colunas",
                       "colunas": {"minimo": 3, "maximo": 3}})
    r = calcular_distribuicao(30, 10, 6, c,
                              min_ws=[1] * 6, min_hs=[1] * 6)
    _ok("pref_colunas formacao 2x3", r["formacao"] == (2, 3), str(r["formacao"]))


def teste_formacao_matriz_fixa():
    # 3 participantes em matriz_fixa 2x2: grade 2x2 (cabe 3 dos 4 slots).
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}})
    r = calcular_distribuicao(20, 10, 3, c, min_ws=[1, 1, 1], min_hs=[1, 1, 1])
    _ok("matriz_fixa formacao 2x2", r["formacao"] == (2, 2), str(r["formacao"]))
    # Participante 2 (indice) em por_linha -> linha 1, coluna 0.
    cel2 = [c for c in r["celulas"] if c["participante"] == 2][0]
    _ok("matriz_fixa celula p2 (1,0)",
        cel2["linha"] == 1 and cel2["coluna"] == 0,
        "{0},{1}".format(cel2["linha"], cel2["coluna"]))


def teste_ordem_por_linha():
    # 4 participantes, 2x2, por_linha: p0=(0,0), p1=(0,1), p2=(1,0), p3=(1,1).
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
             ordem="por_linha")
    r = calcular_distribuicao(20, 10, 4, c, min_ws=[1] * 4, min_hs=[1] * 4)
    esperado = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)}
    obtido = {c["participante"]: (c["linha"], c["coluna"]) for c in r["celulas"]}
    _ok("ordem por_linha atribuicao", obtido == esperado, str(obtido))


def teste_ordem_por_coluna():
    # 4 participantes, 2x2, por_coluna: p0=(0,0), p1=(1,0), p2=(0,1), p3=(1,1).
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
             ordem="por_coluna")
    r = calcular_distribuicao(20, 10, 4, c, min_ws=[1] * 4, min_hs=[1] * 4)
    esperado = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}
    obtido = {c["participante"]: (c["linha"], c["coluna"]) for c in r["celulas"]}
    _ok("ordem por_coluna atribuicao", obtido == esperado, str(obtido))


def teste_dimensionamento_maior_da_coluna():
    # 2 colunas, uma linha. min_ws = [3, 7]. maior_da_coluna:
    # col0 = max(3) = 3; col1 = max(7) = 7.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "maior_da_coluna"},
                              "linhas": {"politica": "uniforme"}})
    r = calcular_distribuicao(30, 5, 2, c, min_ws=[3, 7], min_hs=[1, 1])
    _ok("dim maior_da_coluna larguras [3,7]",
        r["grade"]["larguras_colunas"] == [3, 7],
        str(r["grade"]["larguras_colunas"]))


def teste_dimensionamento_uniforme():
    # uniforme: todas as colunas = max global dos min_ws = 7.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "uniforme"},
                              "linhas": {"politica": "uniforme"}})
    r = calcular_distribuicao(30, 5, 2, c, min_ws=[3, 7], min_hs=[1, 1])
    _ok("dim uniforme larguras [7,7]",
        r["grade"]["larguras_colunas"] == [7, 7],
        str(r["grade"]["larguras_colunas"]))


def teste_dimensionamento_minimo_fixo():
    # minimo_fixo: todas as colunas = 5, ignorando min_ws maiores (DEC-APP-0025-01).
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "uniforme"}})
    r = calcular_distribuicao(40, 5, 2, c, min_ws=[3, 99], min_hs=[1, 1])
    _ok("dim minimo_fixo larguras [5,5]",
        r["grade"]["larguras_colunas"] == [5, 5],
        str(r["grade"]["larguras_colunas"]))
    _ok("dim minimo_fixo nao cresce por exigencia interna",
        r["fallback"] is False)


def teste_margens_e_dist_horizontal_inicio():
    # 1 participante, 1 coluna largura 5, area_w=20, margem_esq_min=1, dir_min=1.
    # total_min = 1 + 5 + 1 = 7; sobra = 13. dist_h=inicio -> excesso todo a
    # margem_dir. margem_esq=1, margem_dir=1+13=14.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 1}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "uniforme"}},
             espacamento={
                 "margem_superior": {"minimo": 0},
                 "margem_inferior": {"minimo": 0},
                 "margem_esquerda": {"minimo": 1},
                 "margem_direita": {"minimo": 1},
                 "vao_horizontal": {"minimo": 0},
                 "vao_vertical": {"minimo": 0},
             },
             distribuicao_horizontal={"politica": "inicio"})
    r = calcular_distribuicao(20, 5, 1, c, min_ws=[5], min_hs=[1])
    g = r["grade"]
    _ok("dist inicio margem_esq=1", g["margem_esq"] == 1, str(g["margem_esq"]))
    _ok("dist inicio margem_dir=14", g["margem_dir"] == 14, str(g["margem_dir"]))


def teste_dist_horizontal_centro():
    # sobra=13, centro: metade=6 para cada; resto=1 vai ao_ultimo=margem_fim.
    # margem_esq = 1+6 = 7; margem_dir = 1+6+1 = 8.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 1}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "uniforme"}},
             espacamento={
                 "margem_superior": {"minimo": 0},
                 "margem_inferior": {"minimo": 0},
                 "margem_esquerda": {"minimo": 1},
                 "margem_direita": {"minimo": 1},
                 "vao_horizontal": {"minimo": 0},
                 "vao_vertical": {"minimo": 0},
             },
             distribuicao_horizontal={"politica": "centro"},
             politica_resto={"horizontal": "ao_ultimo", "vertical": "ao_ultimo"})
    r = calcular_distribuicao(20, 5, 1, c, min_ws=[5], min_hs=[1])
    g = r["grade"]
    _ok("dist centro margem_esq=7", g["margem_esq"] == 7, str(g["margem_esq"]))
    _ok("dist centro margem_dir=8", g["margem_dir"] == 8, str(g["margem_dir"]))


def teste_vao_maximo_respeitado():
    # 2 colunas largura 5, vao min=1 max=2, margens min=0.
    # total_min = 0 + 5 + 1 + 5 + 0 = 11; area_w=30 -> sobra=19.
    # margens_limitadas: margens max=None -> absorvem tudo antes dos vaos.
    # Testamos entre_participantes com vao_max=2: vao recebe ate 2, ou seja
    # +1 (de 1 para 2), sobra restante 18 vai para margens.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "uniforme"}},
             espacamento={
                 "margem_superior": {"minimo": 0},
                 "margem_inferior": {"minimo": 0},
                 "margem_esquerda": {"minimo": 0},
                 "margem_direita": {"minimo": 0},
                 "vao_horizontal": {"minimo": 1, "maximo": 2},
                 "vao_vertical": {"minimo": 0},
             },
             distribuicao_horizontal={"politica": "entre_participantes"})
    r = calcular_distribuicao(30, 5, 2, c, min_ws=[5, 5], min_hs=[1, 1])
    g = r["grade"]
    _ok("vao maximo respeitado (vao <= 2)",
        g["vaos_h"] == [2], str(g["vaos_h"]))


def teste_ordem_expansao_vaos_primeiro():
    # uniforme com ordem_expansao vaos_primeiro_depois_margens.
    # 2 col largura 5, vao min=0 max=None, margens min=0 max=None, area_w=20.
    # total_min = 0+5+0+5+0 = 10; sobra=10. vaos_primeiro: 1 vao recebe tudo (10).
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 1}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "uniforme"}},
             espacamento={
                 "margem_superior": {"minimo": 0},
                 "margem_inferior": {"minimo": 0},
                 "margem_esquerda": {"minimo": 0},
                 "margem_direita": {"minimo": 0},
                 "vao_horizontal": {"minimo": 0},
                 "vao_vertical": {"minimo": 0},
             },
             distribuicao_horizontal={"politica": "uniforme"},
             ordem_expansao={"horizontal": "vaos_primeiro_depois_margens",
                             "vertical": "uniforme_margens_e_vaos"})
    r = calcular_distribuicao(20, 5, 2, c, min_ws=[5, 5], min_hs=[1, 1])
    g = r["grade"]
    _ok("expansao vaos_primeiro vao=10",
        g["vaos_h"] == [10] and g["margem_esq"] == 0 and g["margem_dir"] == 0,
        "vaos={0} esq={1} dir={2}".format(g["vaos_h"], g["margem_esq"], g["margem_dir"]))


def teste_resto_horizontal_ao_ultimo_vs_ao_primeiro():
    # uniforme entre 3 slots com ordem uniforme_margens_e_vaos.
    # 2 colunas -> slots agregados na ordem [margem_esq, margem_dir, vao].
    # area_w=20, 2 col largura 5, min todos 0. total_min=10, sobra=10.
    # uniforme: 10 // 3 = 3 cada (soma 9), resto 1 unidade inteira.
    # A unidade residual segue politica_resto sobre a lista agregada
    # [margem_esq, margem_dir, vao]: ao_ultimo -> reversed -> primeiro da lista
    # invertida = vao (o "ultimo" slot agregado). Logo [esq,vao,dir] = [3,4,3].
    base_esp = {
        "margem_superior": {"minimo": 0}, "margem_inferior": {"minimo": 0},
        "margem_esquerda": {"minimo": 0}, "margem_direita": {"minimo": 0},
        "vao_horizontal": {"minimo": 0}, "vao_vertical": {"minimo": 0},
    }
    dim = {"colunas": {"politica": "minimo_fixo", "minimo": 5},
           "linhas": {"politica": "uniforme"}}
    forma = {"politica": "matriz_fixa", "linhas": {"fixo": 1}, "colunas": {"fixo": 2}}
    c_u = _cfg(formacao=forma, dimensionamento=dim, espacamento=base_esp,
               distribuicao_horizontal={"politica": "uniforme"},
               politica_resto={"horizontal": "ao_ultimo", "vertical": "ao_ultimo"})
    r_u = calcular_distribuicao(20, 5, 2, c_u, min_ws=[5, 5], min_hs=[1, 1])
    g = r_u["grade"]
    _ok("resto ao_ultimo -> vao recebe unidade residual",
        [g["margem_esq"], g["vaos_h"][0], g["margem_dir"]] == [3, 4, 3],
        str([g["margem_esq"], g["vaos_h"][0], g["margem_dir"]]))

    c_p = _cfg(formacao=forma, dimensionamento=dim, espacamento=base_esp,
               distribuicao_horizontal={"politica": "uniforme"},
               politica_resto={"horizontal": "ao_primeiro", "vertical": "ao_ultimo"})
    r_p = calcular_distribuicao(20, 5, 2, c_p, min_ws=[5, 5], min_hs=[1, 1])
    g2 = r_p["grade"]
    _ok("resto ao_primeiro -> margem_esq recebe unidade residual",
        [g2["margem_esq"], g2["vaos_h"][0], g2["margem_dir"]] == [4, 3, 3],
        str([g2["margem_esq"], g2["vaos_h"][0], g2["margem_dir"]]))


def teste_coordenadas_celulas():
    # 2x2, largura 5 por col, altura 1 por linha, vao_h=1, vao_v=1, margens 0.
    # x col0=0, col1=5+1=6. y lin0=0, lin1=1+1=2.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 5},
                              "linhas": {"politica": "minimo_fixo", "minimo": 1}},
             espacamento={
                 "margem_superior": {"minimo": 0},
                 "margem_inferior": {"minimo": 0},
                 "margem_esquerda": {"minimo": 0},
                 "margem_direita": {"minimo": 0},
                 "vao_horizontal": {"minimo": 1},
                 "vao_vertical": {"minimo": 1},
             },
             distribuicao_horizontal={"politica": "inicio"},
             distribuicao_vertical={"politica": "inicio"})
    r = calcular_distribuicao(11, 3, 4, c, min_ws=[5] * 4, min_hs=[1] * 4)
    coords = {cc["participante"]: (cc["x"], cc["y"]) for cc in r["celulas"]}
    esperado = {0: (0, 0), 1: (6, 0), 2: (0, 2), 3: (6, 2)}
    _ok("coordenadas celulas 2x2", coords == esperado, str(coords))


def teste_cardinalidade_unitaria():
    c = _cfg(formacao={"politica": "preferencia_linhas", "linhas": {"minimo": 1}})
    r = calcular_distribuicao(20, 10, 1, c, min_ws=[3], min_hs=[1])
    _ok("cardinalidade unitaria 1x1",
        r["formacao"] == (1, 1) and len(r["celulas"]) == 1,
        str(r["formacao"]))


def teste_uma_linha():
    # pref_linhas fixa em 1 linha -> ceil(3/1) = 3 colunas.
    c = _cfg(formacao={"politica": "preferencia_linhas",
                       "linhas": {"minimo": 1, "maximo": 1}})
    r = calcular_distribuicao(30, 5, 3, c, min_ws=[1] * 3, min_hs=[1] * 3)
    _ok("uma linha formacao (1,3)", r["formacao"] == (1, 3), str(r["formacao"]))


def teste_uma_coluna():
    c = _cfg(formacao={"politica": "preferencia_colunas",
                       "colunas": {"minimo": 1, "maximo": 1}})
    r = calcular_distribuicao(10, 10, 3, c, min_ws=[1] * 3, min_hs=[1] * 3)
    _ok("uma coluna formacao (3,1)", r["formacao"] == (3, 1), str(r["formacao"]))


def teste_formacao_impossivel_fallback():
    # area minuscula, exige 4 participantes de largura 10 em uma linha.
    c = _cfg(formacao={"politica": "preferencia_linhas",
                       "linhas": {"minimo": 1, "maximo": 1}},
             dimensionamento={"colunas": {"politica": "maior_da_coluna"},
                              "linhas": {"politica": "uniforme"}})
    r = calcular_distribuicao(5, 2, 4, c, min_ws=[10] * 4, min_hs=[1] * 4)
    _ok("formacao impossivel -> fallback",
        r["fallback"] is True and r["grade"] is None, str(r["fallback"]))


def teste_recuperacao_apos_aumento():
    # Mesma config: pequena -> fallback; grande -> sem fallback. Determinismo.
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
             dimensionamento={"colunas": {"politica": "minimo_fixo", "minimo": 10},
                              "linhas": {"politica": "uniforme"}})
    r_peq = calcular_distribuicao(5, 2, 4, c, min_ws=[1] * 4, min_hs=[1] * 4)
    r_grande = calcular_distribuicao(40, 10, 4, c, min_ws=[1] * 4, min_hs=[1] * 4)
    _ok("recuperacao: pequena e fallback", r_peq["fallback"] is True)
    _ok("recuperacao: grande sem fallback", r_grande["fallback"] is False)


def teste_determinismo():
    c = _cfg(formacao={"politica": "preferencia_colunas",
                       "colunas": {"minimo": 2}})
    r1 = calcular_distribuicao(30, 10, 5, c, min_ws=[2] * 5, min_hs=[1] * 5)
    r2 = calcular_distribuicao(30, 10, 5, c, min_ws=[2] * 5, min_hs=[1] * 5)
    _ok("determinismo identico", r1 == r2)


def teste_sem_perda_nem_duplicacao():
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 3}, "colunas": {"fixo": 3}})
    r = calcular_distribuicao(60, 30, 7, c, min_ws=[1] * 7, min_hs=[1] * 7)
    participantes = sorted(cc["participante"] for cc in r["celulas"])
    _ok("sem perda nem duplicacao (7 participantes unicos)",
        participantes == list(range(7)), str(participantes))
    coords = [(cc["linha"], cc["coluna"]) for cc in r["celulas"]]
    _ok("sem sobreposicao de celulas", len(coords) == len(set(coords)))


def teste_coordenadas_nao_negativas():
    c = _cfg(formacao={"politica": "matriz_fixa",
                       "linhas": {"fixo": 2}, "colunas": {"fixo": 2}},
             distribuicao_horizontal={"politica": "centro"},
             distribuicao_vertical={"politica": "centro"})
    r = calcular_distribuicao(40, 20, 4, c, min_ws=[3] * 4, min_hs=[1] * 4)
    negativos = [cc for cc in r["celulas"] if cc["x"] < 0 or cc["y"] < 0]
    _ok("nenhuma coordenada negativa", not negativos, str(negativos))


def teste_alinhamento_na_celula():
    # centro horizontal: livre=(10-4)=6 -> dx=3. base vertical: livre=(3-1)=2 -> dy=2.
    dx, dy = alinhar_na_celula(4, 1, 10, 3, "centro", "base")
    _ok("alinhamento centro/base dx=3 dy=2", (dx, dy) == (3, 2), str((dx, dy)))
    # inicio/topo: dx=0 dy=0.
    dx2, dy2 = alinhar_na_celula(4, 1, 10, 3, "inicio", "topo")
    _ok("alinhamento inicio/topo 0,0", (dx2, dy2) == (0, 0), str((dx2, dy2)))
    # fim/centro impar: livre_w=6 dx=6; livre_h=3 dy=1 (floor de 3/2).
    dx3, dy3 = alinhar_na_celula(4, 1, 10, 4, "fim", "centro")
    _ok("alinhamento fim/centro impar dx=6 dy=1", (dx3, dy3) == (6, 1), str((dx3, dy3)))


def teste_zero_participantes():
    c = _cfg()
    r = calcular_distribuicao(10, 5, 0, c)
    _ok("zero participantes sem fallback e sem celulas",
        r["fallback"] is False and r["celulas"] == [], str(r))


def teste_erros_dominio():
    def espera(nome, fn):
        try:
            fn()
        except DistribuicaoMatricialErro:
            _ok(nome, True)
        except Exception as exc:  # pragma: no cover
            _ok(nome, False, "excecao errada: {0}".format(type(exc).__name__))
        else:
            _ok(nome, False, "nenhuma excecao")

    espera("n_participantes negativo -> erro",
           lambda: calcular_distribuicao(10, 5, -1, _cfg()))
    espera("politica formacao invalida -> erro",
           lambda: calcular_distribuicao(
               10, 5, 2,
               _cfg(formacao={"politica": "inexistente"}),
               min_ws=[1, 1], min_hs=[1, 1]))


def main():
    print("Diagnostico H-0035 - motor de distribuicao matricial")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))
    print("")

    teste_formacao_pref_linhas()
    teste_formacao_pref_colunas()
    teste_formacao_matriz_fixa()
    teste_ordem_por_linha()
    teste_ordem_por_coluna()
    teste_dimensionamento_maior_da_coluna()
    teste_dimensionamento_uniforme()
    teste_dimensionamento_minimo_fixo()
    teste_margens_e_dist_horizontal_inicio()
    teste_dist_horizontal_centro()
    teste_vao_maximo_respeitado()
    teste_ordem_expansao_vaos_primeiro()
    teste_resto_horizontal_ao_ultimo_vs_ao_primeiro()
    teste_coordenadas_celulas()
    teste_cardinalidade_unitaria()
    teste_uma_linha()
    teste_uma_coluna()
    teste_formacao_impossivel_fallback()
    teste_recuperacao_apos_aumento()
    teste_determinismo()
    teste_sem_perda_nem_duplicacao()
    teste_coordenadas_nao_negativas()
    teste_alinhamento_na_celula()
    teste_zero_participantes()
    teste_erros_dominio()

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
