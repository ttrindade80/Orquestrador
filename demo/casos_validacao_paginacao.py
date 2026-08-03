"""Harness de validacao da paginacao (H-0045 / §18–§19).

P16: o caminho de produto carrega modelos fixos uma unica vez e nao
reconstrói conteudo em SIGWINCH. Os construtores adaptativos abaixo
permanecem apenas como API de compatibilidade para testes legados do
renderer (fora de escopo de alteracao); as entradas LARGURA/PERMITIR/
EVITAR/CONDICIONAL estao substituidas pelas tres telas fixas de §19.2.
VAZIO e CONTINUACAO usam JSON fixo (sem geracao a partir de C no runtime
da demo).
"""

from __future__ import annotations

import hashlib
import json

# Identificadores de ponto de entrada (demo.py) → id canonico do caso.
CASOS_POR_ID_ENTRADA = {
    "h0045_validacao_largura": "H0045-VAL-LARGURA",
    "h0045_validacao_permitir": "H0045-VAL-PERMITIR",
    "h0045_validacao_evitar": "H0045-VAL-EVITAR",
    "h0045_validacao_condicional": "H0045-VAL-CONDICIONAL",
    "h0045_validacao_continuacao": "H0045-VAL-CONTINUACAO",
    "h0045_validacao_vazio": "H0045-VAL-VAZIO",
}

# Esqueleto JSON associado a cada caso.
# VAZIO/CONTINUACAO apontam para fixtures fixas proprias (§19.3).
# Os quatro adaptativos legados mantêm esqueleto apenas para testes.
ESQUELETO_POR_CASO = {
    "H0045-VAL-LARGURA": "h0045_paginacao_modo_verboso_multilinha",
    "H0045-VAL-PERMITIR": "h0045_paginacao_politicas_quebra",
    "H0045-VAL-EVITAR": "h0045_paginacao_politicas_quebra",
    "H0045-VAL-CONDICIONAL": "h0045_paginacao_politicas_quebra",
    "H0045-VAL-CONTINUACAO": "h0045_validacao_continuacao",
    "H0045-VAL-VAZIO": "h0045_validacao_vazio",
}

CASOS_ADAPTATIVOS_SUBSTITUIDOS = frozenset(
    (
        "H0045-VAL-LARGURA",
        "H0045-VAL-PERMITIR",
        "H0045-VAL-EVITAR",
        "H0045-VAL-CONDICIONAL",
    )
)

CASOS_FIXOS_SEM_REGENERACAO = frozenset(
    (
        "H0045-VAL-VAZIO",
        "H0045-VAL-CONTINUACAO",
    )
)

TELAS_POLITICA_FIXA = frozenset(
    (
        "h0045_validacao_fluxo_continuo",
        "h0045_validacao_nova_pagina",
        "h0045_validacao_manter_junto",
    )
)

ROTULOS = {
    "H0045-VAL-LARGURA": "H0045-VAL-LARGURA",
    "H0045-VAL-PERMITIR": "H0045-VAL-PERMITIR",
    "H0045-VAL-EVITAR": "H0045-VAL-EVITAR",
    "H0045-VAL-CONDICIONAL": "H0045-VAL-CONDICIONAL",
    "H0045-VAL-CONTINUACAO": "H0045-VAL-CONTINUACAO",
    "H0045-VAL-VAZIO": "H0045-VAL-VAZIO",
}


class GeometriaEfetivaAusente(ValueError):
    """Harness: geometria/W/C nao resolvidos pela autoridade vigente."""


def id_caso_de_entrada(id_entrada):
    """Retorna o id canonico do caso ou ``None`` se nao for caso de validacao."""
    return CASOS_POR_ID_ENTRADA.get(id_entrada)


def esqueleto_de_caso(caso_id):
    """Id da fixture-esqueleto associada ao caso."""
    return ESQUELETO_POR_CASO[caso_id]


def caso_usa_modelo_fixo(caso_id):
    """True se o caso carrega JSON fixo sem regeneracao por W/C na demo."""
    return caso_id in CASOS_FIXOS_SEM_REGENERACAO


def snapshot_itens_logicos(console):
    """Instantaneo estrutural do modelo logico (sem geometria)."""
    itens = []
    for item in list(console._campos_inertes.get("itens") or []):
        itens.append(
            {
                "id": item.get("id"),
                "texto": item.get("texto"),
                "navegavel": bool(item.get("navegavel")),
                "politica_quebra": item.get("politica_quebra"),
            }
        )
    return itens


def hash_modelo_logico(console):
    """Hash estavel do conteudo logico (IDs, textos, ordem, politicas)."""
    payload = json.dumps(
        snapshot_itens_logicos(console),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _exigir_dimensao_positiva(valor, nome):
    """Exige int exato positivo ja resolvido; sem coercao nem fallback.

    Dominio: ``type(valor) is int and valor > 0``. Rejeita bool (subtipo de
    int), float, string numerica e demais tipos — sem ``int(valor)``.
    """
    if type(valor) is int and valor > 0:
        return valor
    if valor is None:
        raise GeometriaEfetivaAusente(
            "{0} ausente: geometria efetiva do console nao resolvida".format(nome)
        )
    raise GeometriaEfetivaAusente(
        "{0} invalida: geometria efetiva do console nao resolvida".format(nome)
    )


def capacidade_fisica_efetiva(altura_interna):
    """C: capacidade fisica efetiva da pagina (``altura_interna`` do renderer)."""
    return _exigir_dimensao_positiva(altura_interna, "capacidade_fisica_efetiva")


def resolver_largura_util_efetiva(
    elemento,
    largura_console,
    altura_interna,
    verboso=True,
    desconto_estrutural=None,
):
    """Resolve W pela autoridade ``mapa_fisico_de_itens`` (sem formula propria)."""
    from tela.renderizador import DESCONTO_ESTRUTURAL_CONSOLE, mapa_fisico_de_itens

    largura_resolvida = _exigir_dimensao_positiva(
        largura_console, "largura_console"
    )
    altura_resolvida = _exigir_dimensao_positiva(
        altura_interna, "altura_interna"
    )
    if desconto_estrutural is None:
        desconto_estrutural = DESCONTO_ESTRUTURAL_CONSOLE
    itens_originais = list(elemento._campos_inertes.get("itens") or [])
    try:
        limite = max(8, largura_resolvida)
        lo, hi = 1, limite
        while lo < hi:
            mid = (lo + hi + 1) // 2
            elemento._campos_inertes["itens"] = [
                {
                    "id": "_probe_w",
                    "texto": "W" * mid,
                    "navegavel": True,
                }
            ]
            mapa = mapa_fisico_de_itens(
                elemento,
                largura_resolvida,
                altura_resolvida,
                verboso,
                desconto_estrutural=desconto_estrutural,
            )
            if not mapa:
                raise GeometriaEfetivaAusente(
                    "mapa_fisico_de_itens nao resolveu largura util efetiva: "
                    "geometria efetiva do console nao resolvida"
                )
            linhas = int(mapa[0]["linhas_fisicas"])
            if linhas <= 1:
                lo = mid
            else:
                hi = mid - 1
        if lo < 1:
            raise GeometriaEfetivaAusente(
                "largura util efetiva invalida: "
                "geometria efetiva do console nao resolvida"
            )
        return lo
    finally:
        elemento._campos_inertes["itens"] = itens_originais


def _token_linha(prefixo, indice, W):
    """Token que ocupa exatamente uma linha fisica na largura ``W``."""
    w = W
    base = "{0}_L{1:02d}_".format(prefixo, indice)
    if len(base) >= w:
        return base[:w]
    return (base + ("-" * (w - len(base))))[:w]


def texto_com_n_linhas_fisicas(n, W, prefixo):
    """Texto com exatamente ``n`` linhas fisicas sob largura util ``W``."""
    n = max(1, int(n))
    return " ".join(_token_linha(prefixo, i + 1, W) for i in range(n))


def _item(id_item, texto, politica_quebra, navegavel=True):
    return {
        "id": id_item,
        "texto": texto,
        "navegavel": navegavel,
        "politica_quebra": politica_quebra,
    }


def construir_caso_largura(W, C=None):
    """H0045-VAL-LARGURA — legado/teste; substituido pela tela de fluxo continuo."""
    w = _exigir_dimensao_positiva(W, "W")
    inicio, meio, fim = "LARGURA_INICIO", "LARGURA_MEIO", "LARGURA_FIM"
    for marcador in (inicio, meio, fim):
        if len(marcador) > w:
            raise ValueError(
                "W={0} insuficiente para marcador {1!r}".format(w, marcador)
            )
    alvo = min(2 * w, max(w + 1, w + max(1, w // 2)))
    fixos = len(inicio) + len(meio) + len(fim) + 4
    resto = max(2, alvo - fixos)
    pad1 = max(1, resto // 2)
    pad2 = max(1, resto - pad1)
    texto = "{0} {1} {2} {3} {4}".format(
        inicio, "-" * pad1, meio, "-" * pad2, fim
    )
    if len(texto) <= w:
        extra = w + 1 - len(texto)
        texto = "{0} {1} {2} {3} {4}".format(
            inicio, "-" * (pad1 + extra), meio, "-" * pad2, fim
        )
    assert len(texto) > w
    return {
        "caso_id": "H0045-VAL-LARGURA",
        "fenomeno": "quebra_textual_por_largura",
        "rotulo": ROTULOS["H0045-VAL-LARGURA"],
        "W": w,
        "C": None if C is None else capacidade_fisica_efetiva(C),
        "itens": [
            _item("val_largura_01", texto, "permitir_quebra"),
        ],
        "marcadores": [inicio, meio, fim],
        "propriedades": {
            "comprimento_logico": len(texto),
            "linhas_fisicas_minimas": 2,
            "marcadores_unicos": True,
        },
    }


def construir_caso_permitir(W, C):
    """H0045-VAL-PERMITIR — legado/teste; substituido pela tela de fluxo continuo."""
    w = _exigir_dimensao_positiva(W, "W")
    c = capacidade_fisica_efetiva(C)
    residuo = 1 if c > 1 else 0
    altura_filler = max(1, c - residuo) if residuo else 0
    altura_alvo = max(2, residuo + 2) if c > 1 else 2
    itens = []
    if altura_filler > 0:
        itens.append(
            _item(
                "val_permitir_filler",
                texto_com_n_linhas_fisicas(altura_filler, w, "PFILL"),
                "evitar_quebra",
            )
        )
    itens.append(
        _item(
            "val_permitir_alvo",
            texto_com_n_linhas_fisicas(altura_alvo, w, "PERMITIR"),
            "permitir_quebra",
        )
    )
    return {
        "caso_id": "H0045-VAL-PERMITIR",
        "fenomeno": "fragmentacao_vertical_permitir_quebra",
        "rotulo": ROTULOS["H0045-VAL-PERMITIR"],
        "W": w,
        "C": c,
        "itens": itens,
        "marcadores": ["PERMITIR_L01_"],
        "propriedades": {
            "residuo": residuo,
            "altura_filler": altura_filler,
            "altura_alvo": altura_alvo,
            "politica_quebra": "permitir_quebra",
            "nao_prova": ["pagina_somente_de_continuacao"],
        },
    }


def construir_caso_evitar(W, C):
    """H0045-VAL-EVITAR — legado/teste; substituido pela tela nova_pagina.

    Com a semantica corrigida de ``evitar_quebra``, o alvo sempre inicia em
    pagina nova apos o filler (mesmo com residuo suficiente).
    """
    w = _exigir_dimensao_positiva(W, "W")
    c = capacidade_fisica_efetiva(C)
    residuo = 1 if c > 1 else 0
    altura_filler = max(1, c - residuo) if residuo else max(1, c - 1)
    altura_item = min(c, max(residuo + 1, 2 if c > 1 else 1))
    if altura_item <= residuo and c > 1:
        altura_item = residuo + 1
    if altura_item > c:
        altura_item = c
    itens = [
        _item(
            "val_evitar_filler",
            texto_com_n_linhas_fisicas(altura_filler, w, "EFILL"),
            "evitar_quebra",
        ),
        _item(
            "val_evitar_alvo",
            texto_com_n_linhas_fisicas(altura_item, w, "EVITAR"),
            "evitar_quebra",
        ),
    ]
    return {
        "caso_id": "H0045-VAL-EVITAR",
        "fenomeno": "inicio_obrigatorio_em_nova_pagina",
        "rotulo": ROTULOS["H0045-VAL-EVITAR"],
        "W": w,
        "C": c,
        "itens": itens,
        "marcadores": ["EVITAR_L01_"],
        "propriedades": {
            "residuo": residuo if residuo else (c - altura_filler),
            "altura_filler": altura_filler,
            "altura_item": altura_item,
            "politica_quebra": "evitar_quebra",
        },
    }


def construir_caso_condicional(W, C):
    """H0045-VAL-CONDICIONAL — legado/teste; substituido pela tela manter_junto."""
    w = _exigir_dimensao_positiva(W, "W")
    c = capacidade_fisica_efetiva(C)
    altura_cabe = max(1, c - 1) if c > 1 else 1
    altura_maior = c + 1
    residuo = 1 if c > 1 else 0
    altura_filler = max(1, c - residuo) if residuo else 0
    itens = []
    if altura_filler > 0:
        itens.append(
            _item(
                "val_cond_filler",
                texto_com_n_linhas_fisicas(altura_filler, w, "CFILL"),
                "evitar_quebra",
            )
        )
    itens.extend(
        [
            _item(
                "CONDICIONAL_CABE",
                texto_com_n_linhas_fisicas(altura_cabe, w, "CABE"),
                "permitir_quebra_somente_se_maior_que_pagina",
            ),
            _item(
                "CONDICIONAL_MAIOR",
                texto_com_n_linhas_fisicas(altura_maior, w, "MAIOR"),
                "permitir_quebra_somente_se_maior_que_pagina",
            ),
        ]
    )
    return {
        "caso_id": "H0045-VAL-CONDICIONAL",
        "fenomeno": "politica_condicional",
        "rotulo": ROTULOS["H0045-VAL-CONDICIONAL"],
        "W": w,
        "C": c,
        "itens": itens,
        "marcadores": ["CABE_L01_", "MAIOR_L01_"],
        "subcasos": [
            {
                "id": "CONDICIONAL_CABE",
                "relacao": "altura_do_item <= C",
                "altura": altura_cabe,
                "esperado": "item_inteiro",
            },
            {
                "id": "CONDICIONAL_MAIOR",
                "relacao": "altura_do_item > C",
                "altura": altura_maior,
                "esperado": "item_fragmentado",
            },
        ],
        "propriedades": {
            "altura_cabe": altura_cabe,
            "altura_maior": altura_maior,
        },
    }


def construir_caso_continuacao(W, C):
    """API legada de teste: gera CONTINUACAO a partir de C.

    O ponto de entrada de produto ``h0045_validacao_continuacao`` usa JSON
    fixo e nao chama este construtor (§19.1/§19.3).
    """
    w = _exigir_dimensao_positiva(W, "W")
    c = capacidade_fisica_efetiva(C)
    altura = 2 * c + 1
    tokens = [_token_linha("CONT", i + 1, w) for i in range(altura)]
    tokens[0] = ("CONT_INICIO" + tokens[0][len("CONT_INICIO"):])[:w]
    if len(tokens[0]) < w:
        tokens[0] = tokens[0].ljust(w, "-")
    meio_idx = altura // 2
    tokens[meio_idx] = ("CONT_MEIO" + tokens[meio_idx][len("CONT_MEIO"):])[:w]
    if len(tokens[meio_idx]) < w:
        tokens[meio_idx] = tokens[meio_idx].ljust(w, "-")
    tokens[-1] = ("CONT_FIM" + tokens[-1][len("CONT_FIM"):])[:w]
    if len(tokens[-1]) < w:
        tokens[-1] = tokens[-1].ljust(w, "-")
    if "CONT_INICIO" not in tokens[0]:
        tokens[0] = ("CONT_INICIO" + ("-" * max(0, w - 11)))[:w]
    if "CONT_MEIO" not in tokens[meio_idx]:
        tokens[meio_idx] = ("CONT_MEIO" + ("-" * max(0, w - 9)))[:w]
    if "CONT_FIM" not in tokens[-1]:
        tokens[-1] = ("CONT_FIM" + ("-" * max(0, w - 8)))[:w]
    texto = " ".join(tokens)
    return {
        "caso_id": "H0045-VAL-CONTINUACAO",
        "fenomeno": "pagina_somente_de_continuacao",
        "rotulo": ROTULOS["H0045-VAL-CONTINUACAO"],
        "W": w,
        "C": c,
        "itens": [
            _item("val_continuacao_01", texto, "permitir_quebra"),
        ],
        "marcadores": ["CONT_INICIO", "CONT_MEIO", "CONT_FIM"],
        "propriedades": {
            "altura_item": altura,
            "relacao": "altura_do_item >= 2C + 1",
            "nao_substitui": ["prova_de_permitir_quebra"],
        },
    }


def construir_caso_vazio(W=None, C=None):
    """H0045-VAL-VAZIO — conjunto paginado com zero itens reais."""
    return {
        "caso_id": "H0045-VAL-VAZIO",
        "fenomeno": "conjunto_paginado_vazio",
        "rotulo": ROTULOS["H0045-VAL-VAZIO"],
        "W": None if W is None else _exigir_dimensao_positiva(W, "W"),
        "C": None if C is None else capacidade_fisica_efetiva(C),
        "itens": [],
        "marcadores": [],
        "propriedades": {
            "pagina": "1/1",
            "chips_inativos": True,
            "itens": [],
            "modelo": "fixo",
        },
    }


_CONSTRUTORES = {
    "H0045-VAL-LARGURA": construir_caso_largura,
    "H0045-VAL-PERMITIR": construir_caso_permitir,
    "H0045-VAL-EVITAR": construir_caso_evitar,
    "H0045-VAL-CONDICIONAL": construir_caso_condicional,
    "H0045-VAL-CONTINUACAO": construir_caso_continuacao,
    "H0045-VAL-VAZIO": construir_caso_vazio,
}


def construir_caso(caso_id, W, C):
    """Constroi um dos seis casos a partir de W e C ja resolvidos."""
    if caso_id not in _CONSTRUTORES:
        raise ValueError("caso de validacao desconhecido: {0!r}".format(caso_id))
    if caso_id == "H0045-VAL-LARGURA":
        return construir_caso_largura(W, C)
    if caso_id == "H0045-VAL-VAZIO":
        return construir_caso_vazio(W, C)
    return _CONSTRUTORES[caso_id](W, C)


def aplicar_caso_ao_modelo(modelo, caso):
    """Incorpora ``caso['itens']`` e o rotulo no modelo (em memoria)."""
    rotulo = caso.get("rotulo") or caso.get("caso_id")
    cabecalho = getattr(modelo, "cabecalho", None)
    if isinstance(cabecalho, dict):
        cabecalho["titulo"] = rotulo
        cabecalho["descricao"] = caso.get("fenomeno") or rotulo
    elif cabecalho is not None:
        try:
            cabecalho.titulo = rotulo
            if getattr(cabecalho, "descricao", None) is not None:
                cabecalho.descricao = caso.get("fenomeno") or rotulo
        except AttributeError:
            pass
    for elemento in modelo.corpo.elementos:
        if getattr(elemento, "tipo", None) == "console":
            elemento._campos_inertes["itens"] = list(caso.get("itens") or [])
            if rotulo:
                elemento._campos_inertes["titulo"] = rotulo
            break
    return modelo


def construir_e_aplicar(modelo, caso_id, W, C):
    """Atalho: constroi o caso e aplica ao modelo."""
    caso = construir_caso(caso_id, W, C)
    aplicar_caso_ao_modelo(modelo, caso)
    return caso


def meta_caso_fixo(caso_id):
    """Metadados de caso fixo sem reconstruir itens."""
    if caso_id == "H0045-VAL-VAZIO":
        return construir_caso_vazio()
    if caso_id == "H0045-VAL-CONTINUACAO":
        return {
            "caso_id": "H0045-VAL-CONTINUACAO",
            "fenomeno": "pagina_somente_de_continuacao",
            "rotulo": ROTULOS["H0045-VAL-CONTINUACAO"],
            "marcadores": ["CONT_INICIO", "CONT_MEIO", "CONT_FIM"],
            "propriedades": {
                "modelo": "fixo",
                "nao_gera_a_partir_de_C": True,
            },
        }
    raise ValueError("caso fixo desconhecido: {0!r}".format(caso_id))
