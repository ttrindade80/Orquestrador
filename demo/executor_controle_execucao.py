"""Executor sintético H-0050.

Este módulo conhece somente a captura privada e a fixture. Não consulta tela,
modelo, controlador, renderizador ou estado de sessão.
"""

from __future__ import annotations

import json


def _fixture_dict(fixture):
    if isinstance(fixture, dict):
        return fixture
    with open(fixture, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _campo(id_no, nome, valor):
    return {
        "id": id_no,
        "nivel": "campo",
        "nome": nome,
        "valor": valor,
    }


def _registro_item(id_item, *, aplicado):
    return {
        "id": "reg_{0}".format(id_item),
        "nivel": "registro",
        "titulo": id_item,
        "filhos": [
            _campo("{0}__id".format(id_item), "id", id_item),
            _campo("{0}__resultado".format(id_item), "resultado", "processado"),
            _campo("{0}__aplicado".format(id_item), "aplicado", aplicado),
            _campo(
                "{0}__processado_antes".format(id_item),
                "processado_antes",
                False,
            ),
            _campo(
                "{0}__processado_depois".format(id_item),
                "processado_depois",
                True,
            ),
        ],
    }


def documento_resultado_observavel(resultado):
    """Serializa o resultado sintético no schema observável H-0042.

    Produz ``resultado_bruto`` semanticamente válido para a tela vigente de
    resultado, com modo e IDs do lote reconciliado. Não consulta interface.
    """
    if not isinstance(resultado, dict):
        raise ValueError("resultado sintetico invalido")
    modo = resultado.get("modo")
    lote = list(resultado.get("lote_reconciliado") or ())
    if modo not in ("executar", "dry_run"):
        raise ValueError("resultado sintetico sem modo valido")
    if not lote:
        raise ValueError("resultado sintetico sem lote")
    aplicado = modo == "executar"
    n = len(lote)
    documento = {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "conjuntos_campos",
            "niveis": [
                {
                    "id": "secao",
                    "tipo": "container",
                    "conteudo": "titulo",
                    "designador": {"tipo": "nenhum"},
                },
                {
                    "id": "registro",
                    "tipo": "container",
                    "conteudo": "titulo",
                    "designador": {"tipo": "nenhum"},
                },
                {
                    "id": "campo",
                    "tipo": "nome_valor",
                    "conteudo": {"nome": "nome", "valor": "valor"},
                    "designador": {"tipo": "nenhum"},
                },
            ],
            "campos": {},
        },
        "dados": [
            {
                "id": "secao_resumo",
                "nivel": "secao",
                "titulo": "Resumo",
                "filhos": [
                    {
                        "id": "reg_execucao",
                        "nivel": "registro",
                        "titulo": "Execução",
                        "filhos": [
                            _campo("resumo_modo", "modo", modo),
                            _campo("resumo_status", "status", "sucesso"),
                            _campo("resumo_solicitados", "solicitados", n),
                            _campo("resumo_processados", "processados", n),
                            _campo("resumo_ignorados", "ignorados", 0),
                            _campo(
                                "resumo_nao_encontrados",
                                "nao_encontrados",
                                0,
                            ),
                            _campo("resumo_falhos", "falhos", 0),
                        ],
                    }
                ],
            },
            {
                "id": "secao_itens",
                "nivel": "secao",
                "titulo": "Itens",
                "filhos": [
                    _registro_item(item_id, aplicado=aplicado) for item_id in lote
                ],
            },
        ],
    }
    return json.dumps(documento, ensure_ascii=False, separators=(",", ":"))


def executar(captura, fixture):
    modo = getattr(captura, "modo_capturado", None)
    lote = tuple(getattr(captura, "lote_reconciliado", ()))
    if not isinstance(modo, str) or modo not in ("executar", "dry_run"):
        raise ValueError("captura sem modo de execucao valido")
    dados = _fixture_dict(fixture)
    itens = dados.get("itens") if isinstance(dados, dict) else None
    if not isinstance(itens, list):
        raise ValueError("fixture H-0050 sem lista itens")
    por_id = {item.get("id"): item for item in itens if isinstance(item, dict)}
    desconhecidos = [item_id for item_id in lote if item_id not in por_id]
    if desconhecidos:
        raise ValueError("lote contem IDs ausentes na fixture: {0!r}".format(desconhecidos))
    resultado = {
        "modo": modo,
        "lote_reconciliado": list(lote),
        "itens": [por_id[item_id] for item_id in lote],
        "resultado": "DRY_RUN" if modo == "dry_run" else "EXECUTADO",
    }
    resultado["resultado_bruto"] = documento_resultado_observavel(resultado)
    return resultado


executar_controle_execucao = executar


__all__ = [
    "documento_resultado_observavel",
    "executar",
    "executar_controle_execucao",
]
