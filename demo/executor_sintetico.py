"""Executor sintetico demonstrativo do protocolo focal (H-0042).

CLI fechada:

    python -m demo.executor_sintetico \\
      --entrada <entrada.json> \\
      --resultado <resultado.json> \\
      [--dry-run]

Localiza ``fixture_trabalho.json`` como irma de ``resultado.json``.
Nao aceita ``--fixture``, flags de falha, shell arbitrario nem variaveis
de ambiente de controle. Apenas biblioteca padrao do Python.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz and _raiz not in sys.path:
        sys.path.insert(0, _raiz)

from tela.execucao_focal import (  # noqa: E402
    EntradaInvalida,
    ler_e_validar_entrada,
)

CONTROLE_FALHA = "__falha_operacional__"
CONTROLE_INVALIDO = "__resultado_invalido__"
CONTROLE_INTERRUPCAO = "__interrupcao__"
CONTROLES = frozenset({CONTROLE_FALHA, CONTROLE_INVALIDO, CONTROLE_INTERRUPCAO})

AVISO_TODOS_PROCESSADOS = (
    "AVISO: nenhum item foi alterado; todos ja estavam processados.\n"
)
STDERR_FALHA_OPERACIONAL = "ERRO: falha operacional sintetica.\n"
DIAGNOSTICO_NAO_ENCONTRADO = "ID nao encontrado na fixture."
TEXTO_RESULTADO_INVALIDO = "{isto nao e um JSON valido\n"


def _parse_argv(argv):
    parser = argparse.ArgumentParser(
        prog="demo.executor_sintetico",
        description="Executor sintetico focal H-0042.",
        add_help=True,
    )
    parser.add_argument("--entrada", required=True)
    parser.add_argument("--resultado", required=True)
    parser.add_argument("--dry-run", action="store_true", default=False)
    return parser.parse_args(argv[1:])


def _caminho_fixture_trabalho(caminho_resultado):
    return Path(caminho_resultado).resolve().parent / "fixture_trabalho.json"


def _carregar_fixture(caminho):
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if not isinstance(dados, dict) or "itens" not in dados:
        raise ValueError("fixture_trabalho.json invalida")
    itens = dados["itens"]
    if not isinstance(itens, list):
        raise ValueError("fixture.itens deve ser array")
    return dados


def _indice_por_id(fixture):
    mapa = {}
    for i, item in enumerate(fixture["itens"]):
        if isinstance(item, dict) and "id" in item:
            mapa[item["id"]] = i
    return mapa


def _gravar_fixture(caminho, fixture):
    Path(caminho).write_text(
        json.dumps(fixture, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _campo(id_no, nome, valor):
    return {
        "id": id_no,
        "nivel": "campo",
        "nome": nome,
        "valor": valor,
    }


def _registro_item(id_item, resultado, aplicado, antes, depois, diagnostico=None):
    filhos = [
        _campo(f"{id_item}__id", "id", id_item),
        _campo(f"{id_item}__resultado", "resultado", resultado),
        _campo(f"{id_item}__aplicado", "aplicado", aplicado),
        _campo(f"{id_item}__processado_antes", "processado_antes", antes),
        _campo(f"{id_item}__processado_depois", "processado_depois", depois),
    ]
    if diagnostico is not None:
        filhos.append(
            _campo(f"{id_item}__diagnostico", "diagnostico", diagnostico)
        )
    return {
        "id": f"reg_{id_item}",
        "nivel": "registro",
        "titulo": id_item,
        "filhos": filhos,
    }


def _documento_multinivel(modo, status, contagens, registros):
    resumo_filhos = [
        _campo("resumo_modo", "modo", modo),
        _campo("resumo_status", "status", status),
        _campo("resumo_solicitados", "solicitados", contagens["solicitados"]),
        _campo("resumo_processados", "processados", contagens["processados"]),
        _campo("resumo_ignorados", "ignorados", contagens["ignorados"]),
        _campo(
            "resumo_nao_encontrados",
            "nao_encontrados",
            contagens["nao_encontrados"],
        ),
        _campo("resumo_falhos", "falhos", contagens["falhos"]),
    ]
    return {
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
                        "filhos": resumo_filhos,
                    }
                ],
            },
            {
                "id": "secao_itens",
                "nivel": "secao",
                "titulo": "Itens",
                "filhos": list(registros),
            },
        ],
    }


def _gravar_resultado(caminho, documento):
    Path(caminho).write_text(
        json.dumps(documento, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _gravar_texto_bruto(caminho, texto):
    Path(caminho).write_text(texto, encoding="utf-8")


def _ids_normais(ids):
    return [i for i in ids if i not in CONTROLES]


def _item_processado(fixture, mapa, id_item):
    if id_item not in mapa:
        return None
    return bool(fixture["itens"][mapa[id_item]].get("processado"))


def _processar_id_normal(id_item, fixture, mapa, dry_run):
    if id_item not in mapa:
        return _registro_item(
            id_item,
            "nao_encontrado",
            False,
            None,
            None,
            DIAGNOSTICO_NAO_ENCONTRADO,
        ), "nao_encontrado"

    idx = mapa[id_item]
    antes = bool(fixture["itens"][idx].get("processado"))
    if antes:
        return _registro_item(id_item, "ignorado", False, True, True), "ignorado"

    depois = True
    aplicado = not dry_run
    if not dry_run:
        fixture["itens"][idx] = dict(fixture["itens"][idx], processado=True)
    return (
        _registro_item(id_item, "processado", aplicado, False, depois),
        "processado",
    )


def _contagens_de(resultados):
    cont = {
        "solicitados": len(resultados),
        "processados": 0,
        "ignorados": 0,
        "nao_encontrados": 0,
        "falhos": 0,
    }
    for r in resultados:
        if r == "processado":
            cont["processados"] += 1
        elif r == "ignorado":
            cont["ignorados"] += 1
        elif r == "nao_encontrado":
            cont["nao_encontrados"] += 1
        elif r == "falhou":
            cont["falhos"] += 1
    return cont


def _status_global(contagens):
    if contagens["nao_encontrados"] > 0 or contagens["falhos"] > 0:
        return "parcial"
    return "sucesso"


def executar(entrada_path, resultado_path, dry_run=False):
    """Executa a semantica sintetica e grava o resultado.

    Retorna codigo de saida inteiro. Escreve em stderr quando aplicavel.
    """
    try:
        dados = ler_e_validar_entrada(entrada_path)
    except EntradaInvalida as exc:
        sys.stderr.write(f"ERRO: entrada invalida: {exc}\n")
        return 1

    ids = list(dados["ids"])
    fixture_path = _caminho_fixture_trabalho(resultado_path)
    if not fixture_path.is_file():
        sys.stderr.write("ERRO: fixture_trabalho.json ausente.\n")
        return 1

    # Controles exclusivos de demonstracao — tratados antes da mutacao.
    if CONTROLE_FALHA in ids:
        sys.stderr.write(STDERR_FALHA_OPERACIONAL)
        return 1

    if CONTROLE_INVALIDO in ids:
        _gravar_texto_bruto(resultado_path, TEXTO_RESULTADO_INVALIDO)
        return 0

    fixture = _carregar_fixture(fixture_path)
    mapa = _indice_por_id(fixture)
    modo = "dry_run" if dry_run else "executar"
    normals = _ids_normais(ids)

    # Aviso: todos os IDs normais ja processados no momento da invocacao.
    if normals and all(
        _item_processado(fixture, mapa, i) is True for i in normals
    ):
        sys.stderr.write(AVISO_TODOS_PROCESSADOS)

    registros = []
    resultados = []
    fixture_alterada = False

    for id_item in ids:
        if id_item == CONTROLE_INTERRUPCAO:
            # Alteracao observavel na copia antes da interrupcao.
            if fixture_alterada:
                _gravar_fixture(fixture_path, fixture)
            try:
                raise KeyboardInterrupt()
            except KeyboardInterrupt:
                cont = _contagens_de(resultados)
                cont["solicitados"] = len(normals)
                doc = _documento_multinivel(
                    modo, "interrompido", cont, registros
                )
                _gravar_resultado(resultado_path, doc)
                return 130

        if id_item in CONTROLES:
            # Outros controles ja tratados acima; nao equivalem a nao_encontrado.
            continue

        registro, resultado = _processar_id_normal(
            id_item, fixture, mapa, dry_run
        )
        registros.append(registro)
        resultados.append(resultado)
        if resultado == "processado" and not dry_run:
            fixture_alterada = True

    if fixture_alterada:
        _gravar_fixture(fixture_path, fixture)

    cont = _contagens_de(resultados)
    # solicitados = IDs normais efetivamente processados nesta passagem
    cont["solicitados"] = len(normals)
    status = _status_global(cont)
    doc = _documento_multinivel(modo, status, cont, registros)
    _gravar_resultado(resultado_path, doc)
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = _parse_argv(argv)
    return executar(args.entrada, args.resultado, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
