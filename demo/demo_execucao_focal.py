"""Demonstracao nao interativa do protocolo focal H-0042.

Interface:

    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_execucao_focal \\
      --entrada <entrada.json> \\
      --fixture <fixture.json> \\
      [--dry-run]

Reutiliza ``tela.execucao_focal``, nao ativa a interface TUI e nao cria
resultado permanente. A opcao ``--fixture`` pertence somente a este ponto
de entrada demonstrativo. Apenas biblioteca padrao do Python.
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

from tela import execucao_focal  # noqa: E402


ID_FALHA_OPERACIONAL = "__falha_operacional__"
ID_RESULTADO_INVALIDO = "__resultado_invalido__"
ID_INTERRUPCAO = "__interrupcao__"
CONTROLES_SINTETICOS = frozenset(
    {ID_FALHA_OPERACIONAL, ID_RESULTADO_INVALIDO, ID_INTERRUPCAO}
)


def _parse_argv(argv):
    parser = argparse.ArgumentParser(
        prog="demo.demo_execucao_focal",
        description="Demonstracao H-0042: execucao sintetica reversivel.",
        add_help=True,
    )
    parser.add_argument("--entrada", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--dry-run", action="store_true", default=False)
    return parser.parse_args(argv[1:])


def _extrair_status(resultado_bruto):
    if not resultado_bruto:
        return None
    try:
        doc = json.loads(resultado_bruto)
    except json.JSONDecodeError:
        return None
    try:
        for secao in doc.get("dados", []):
            if secao.get("titulo") == "Resumo":
                for reg in secao.get("filhos", []):
                    for campo in reg.get("filhos", []):
                        if campo.get("nome") == "status":
                            return campo.get("valor")
    except (TypeError, AttributeError):
        return None
    return None


def expectativa_de_ids(ids):
    """Deriva a expectativa demonstrativa exclusivamente do conteudo de ids."""
    if not isinstance(ids, list):
        raise ValueError("ids deve ser lista")
    presentes = [i for i in ids if i in CONTROLES_SINTETICOS]
    if len(presentes) > 1:
        raise ValueError("entrada com multiplos controles sinteticos")
    if ID_FALHA_OPERACIONAL in ids:
        return {
            "cenario": "falha_operacional",
            "codigo_observado": "nao_zero",
            "resultado_semanticamente_valido": None,
            "classificacao_externa": "falha",
            "status_interno": None,
            "exige_alteracao_pre_interrupcao": False,
        }
    if ID_RESULTADO_INVALIDO in ids:
        return {
            "cenario": "resultado_invalido",
            "codigo_observado": 0,
            "resultado_semanticamente_valido": False,
            "classificacao_externa": "falha",
            "status_interno": None,
            "exige_alteracao_pre_interrupcao": False,
        }
    if ID_INTERRUPCAO in ids:
        return {
            "cenario": "interrupcao",
            "codigo_observado": 130,
            "resultado_semanticamente_valido": True,
            "classificacao_externa": "falha",
            "status_interno": "interrompido",
            "exige_alteracao_pre_interrupcao": any(
                i not in CONTROLES_SINTETICOS for i in ids
            ),
        }
    return {
        "cenario": "normal",
        "codigo_observado": 0,
        "resultado_semanticamente_valido": True,
        "classificacao_externa": "sucesso",
        "status_interno": None,
        "exige_alteracao_pre_interrupcao": False,
    }


def _fixture_mapa(conteudo):
    if conteudo is None:
        return None
    try:
        doc = json.loads(conteudo)
    except (TypeError, json.JSONDecodeError):
        return None
    itens = doc.get("itens")
    if not isinstance(itens, list):
        return None
    return {i.get("id"): i.get("processado") for i in itens if isinstance(i, dict)}


def cenario_conforme_esperado(resultado, expectativa, inspecao, ids):
    """Comprova se o observado corresponde a expectativa derivada dos ids."""
    codigo = resultado["codigo_saida"]
    classificacao = resultado["classificacao"]
    bruto = resultado.get("resultado_bruto")
    semantico = execucao_focal.resultado_semanticamente_valido(bruto)

    if expectativa["codigo_observado"] == "nao_zero":
        if codigo == 0:
            return False
    elif codigo != expectativa["codigo_observado"]:
        return False

    if classificacao != expectativa["classificacao_externa"]:
        return False

    esperado_sem = expectativa["resultado_semanticamente_valido"]
    if esperado_sem is not None and semantico is not esperado_sem:
        return False

    status = _extrair_status(bruto)
    if expectativa["status_interno"] is not None:
        if status != expectativa["status_interno"]:
            return False

    if expectativa["exige_alteracao_pre_interrupcao"]:
        ids_normais = [i for i in ids if i not in CONTROLES_SINTETICOS]
        if not ids_normais:
            return False
        mapa = _fixture_mapa(inspecao.get("fixture_trabalho_conteudo"))
        if mapa is None:
            return False
        # Alteracao observavel do primeiro ID normal antes da interrupcao.
        primeiro = ids_normais[0]
        if mapa.get(primeiro) is not True:
            return False

    return True


def _resumo_humano(resultado, inspecao):
    linhas = []
    linhas.append(f"codigo_saida: {resultado['codigo_saida']}")
    linhas.append(f"classificacao: {resultado['classificacao']}")
    status = _extrair_status(resultado.get("resultado_bruto"))
    linhas.append(f"status: {status}")
    linhas.append(f"stdout_vazio: {resultado['stdout'] == ''}")
    linhas.append(f"stderr: {resultado['stderr']!r}")
    linhas.append(f"resultado_existe: {resultado['resultado_existe']}")
    semantico = execucao_focal.resultado_semanticamente_valido(
        resultado.get("resultado_bruto")
    )
    linhas.append(f"resultado_semanticamente_valido: {semantico}")
    linhas.append(
        f"resultado_valido: {resultado['classificacao'] == 'sucesso'}"
    )
    fixture_apos = inspecao.get("fixture_trabalho_conteudo")
    linhas.append(f"fixture_trabalho_apos: {fixture_apos}")
    baseline = inspecao.get("baseline_conteudo")
    baseline_atual = Path(inspecao["baseline"]).read_text(encoding="utf-8")
    linhas.append(f"baseline_intacta: {baseline == baseline_atual}")
    linhas.append(
        f"temporario_existia_antes_limpeza: {inspecao.get('diretorio_existia')}"
    )
    return "\n".join(linhas) + "\n"


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = _parse_argv(argv)

    entrada_dados = execucao_focal.ler_e_validar_entrada(args.entrada)
    ids = list(entrada_dados["ids"])
    expectativa = expectativa_de_ids(ids)

    baseline_texto = Path(args.fixture).read_text(encoding="utf-8")
    inspecao = {
        "baseline": str(Path(args.fixture).resolve()),
        "baseline_conteudo": baseline_texto,
        "diretorio_existia": False,
        "fixture_trabalho_conteudo": None,
        "resultado_bruto": None,
    }

    def _antes(ctx):
        inspecao["diretorio_existia"] = Path(ctx["diretorio"]).is_dir()
        caminho_fx = Path(ctx["fixture_trabalho"])
        if caminho_fx.is_file():
            inspecao["fixture_trabalho_conteudo"] = caminho_fx.read_text(
                encoding="utf-8"
            )
        inspecao["resultado_bruto"] = ctx.get("resultado_bruto")

    resultado = execucao_focal.executar_protocolo_focal(
        args.entrada,
        args.fixture,
        dry_run=args.dry_run,
        antes_da_limpeza=_antes,
    )

    # Resumo humano fora de resultado.json (stdout da demonstracao).
    # Preserva o codigo real observado do executor.
    sys.stdout.write(_resumo_humano(resultado, inspecao))
    # Confirma remocao do temporario apos o protocolo.
    sys.stdout.write("temporario_removido: True\n")

    # Baseline permanente deve permanecer intacta.
    atual = Path(args.fixture).read_text(encoding="utf-8")
    if atual != baseline_texto:
        sys.stderr.write("ERRO: baseline permanente foi alterada.\n")
        return 1

    if cenario_conforme_esperado(resultado, expectativa, inspecao, ids):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
