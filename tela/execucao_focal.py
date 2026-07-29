"""Protocolo focal de invocacao de execucao sintetica reversivel (H-0042).

Prepara entrada e temporarios, invoca o processo autorizado por subprocesso,
captura codigo/stdout/stderr, preserva o conteudo bruto de resultado.json,
classifica o processo (codigo 0 E JSON semanticamente valido) e garante
limpeza protegida.

Nao ativa a interface TUI, nao invoca Pipeline real e nao cria binding.
Apenas biblioteca padrao do Python.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCHEMA_SELECAO = "selecao_execucao.v1"

NOME_ENTRADA = "entrada.json"
NOME_RESULTADO = "resultado.json"
NOME_FIXTURE_TRABALHO = "fixture_trabalho.json"

MODULO_EXECUTOR_AUTORIZADO = "demo.executor_sintetico"

CAMPOS_RESUMO_OBRIGATORIOS = (
    "modo",
    "status",
    "solicitados",
    "processados",
    "ignorados",
    "nao_encontrados",
    "falhos",
)
MODOS_AUTORIZADOS = frozenset({"dry_run", "executar"})
STATUS_AUTORIZADOS = frozenset({"sucesso", "parcial", "falha", "interrompido"})
RESULTADOS_INDIVIDUAIS = frozenset(
    {"processado", "ignorado", "nao_encontrado", "falhou"}
)
CAMPOS_ITEM_OBRIGATORIOS = (
    "id",
    "resultado",
    "aplicado",
    "processado_antes",
    "processado_depois",
)
IDS_NIVEIS_H0042 = ("secao", "registro", "campo")


class EntradaInvalida(ValueError):
    """Pedido ``selecao_execucao.v1`` estruturalmente invalido."""


def validar_selecao_execucao(dados):
    """Valida atomicamente um pedido ``selecao_execucao.v1``.

    Rejeita integralmente sem normalizacao silenciosa. Nao altera dados.
    Levanta ``EntradaInvalida`` em qualquer violacao estrutural.
    """
    if not isinstance(dados, dict):
        raise EntradaInvalida("raiz deve ser objeto")
    if "schema" not in dados:
        raise EntradaInvalida("schema ausente")
    if dados["schema"] != SCHEMA_SELECAO:
        raise EntradaInvalida("schema divergente de selecao_execucao.v1")
    if "ids" not in dados:
        raise EntradaInvalida("ids ausente")
    ids = dados["ids"]
    if not isinstance(ids, list):
        raise EntradaInvalida("ids deve ser array")
    if len(ids) == 0:
        raise EntradaInvalida("ids vazio")
    vistos = set()
    for item in ids:
        if not isinstance(item, str):
            raise EntradaInvalida("id deve ser string")
        if item == "":
            raise EntradaInvalida("id vazio")
        if item in vistos:
            raise EntradaInvalida("id duplicado")
        vistos.add(item)
    return list(ids)


def ler_e_validar_entrada(caminho):
    """Le JSON de entrada e valida ``selecao_execucao.v1``."""
    caminho = Path(caminho)
    try:
        texto = caminho.read_text(encoding="utf-8")
        dados = json.loads(texto)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EntradaInvalida(f"entrada ilegivel: {exc}") from exc
    validar_selecao_execucao(dados)
    return dados


def resultado_existente(resultado_bruto):
    """True quando ha conteudo bruto de resultado.json para classificar."""
    return resultado_bruto is not None


def resultado_json_sintaticamente_valido(resultado_bruto):
    """True quando o conteudo bruto decodifica como JSON."""
    if resultado_bruto is None:
        return False
    try:
        json.loads(resultado_bruto)
    except (TypeError, json.JSONDecodeError):
        return False
    return True


def _mapa_campos(filhos):
    if not isinstance(filhos, list):
        return None
    mapa = {}
    for campo in filhos:
        if not isinstance(campo, dict):
            return None
        nome = campo.get("nome")
        if not isinstance(nome, str) or nome == "":
            return None
        if nome in mapa:
            return None
        mapa[nome] = campo.get("valor")
    return mapa


def _validar_nivel_declarado(nivel, ids_niveis):
    if not isinstance(nivel, dict):
        return False
    nid = nivel.get("id")
    if not isinstance(nid, str) or nid == "" or nid not in ids_niveis:
        return False
    tipo = nivel.get("tipo")
    if tipo not in ("container", "conteudo", "nome_valor"):
        return False
    if "conteudo" not in nivel or "designador" not in nivel:
        return False
    designador = nivel["designador"]
    if not isinstance(designador, dict) or "tipo" not in designador:
        return False
    if tipo == "nome_valor":
        conteudo = nivel["conteudo"]
        if not isinstance(conteudo, dict):
            return False
        if conteudo.get("nome") != "nome" or conteudo.get("valor") != "valor":
            return False
    elif nivel["conteudo"] != "titulo":
        return False
    return True


def _validar_no(no, niveis_por_id):
    if not isinstance(no, dict):
        return False
    if "id" not in no or "nivel" not in no:
        return False
    if not isinstance(no["id"], str) or no["id"] == "":
        return False
    nivel_id = no["nivel"]
    if nivel_id not in niveis_por_id:
        return False
    decl = niveis_por_id[nivel_id]
    tipo = decl["tipo"]
    if tipo == "container":
        campo_titulo = decl["conteudo"]
        if campo_titulo not in no or not isinstance(no[campo_titulo], str):
            return False
        if "filhos" not in no or not isinstance(no["filhos"], list):
            return False
        for filho in no["filhos"]:
            if not _validar_no(filho, niveis_por_id):
                return False
        return True
    if tipo == "nome_valor":
        conteudo = decl["conteudo"]
        return conteudo["nome"] in no and conteudo["valor"] in no
    if tipo == "conteudo":
        return decl["conteudo"] in no
    return False


def _validar_item_registro(registro):
    mapa = _mapa_campos(registro.get("filhos"))
    if mapa is None:
        return False
    for nome in CAMPOS_ITEM_OBRIGATORIOS:
        if nome not in mapa:
            return False
    if not isinstance(mapa["id"], str) or mapa["id"] == "":
        return False
    if registro.get("titulo") != mapa["id"]:
        return False
    resultado = mapa["resultado"]
    if resultado not in RESULTADOS_INDIVIDUAIS:
        return False
    if not isinstance(mapa["aplicado"], bool):
        return False
    antes = mapa["processado_antes"]
    depois = mapa["processado_depois"]
    if resultado == "nao_encontrado":
        if antes is not None or depois is not None:
            return False
    else:
        if not isinstance(antes, bool) or not isinstance(depois, bool):
            return False
    if "diagnostico" in mapa:
        if resultado not in ("nao_encontrado", "falhou"):
            return False
        if not isinstance(mapa["diagnostico"], str):
            return False
    elif resultado in ("nao_encontrado", "falhou"):
        return False
    extras = set(mapa) - set(CAMPOS_ITEM_OBRIGATORIOS) - {"diagnostico"}
    return not extras


def resultado_semanticamente_valido(resultado_bruto):
    """True quando o JSON satisfaz o schema semantico H-0042 (§12 + §14.9)."""
    if not resultado_json_sintaticamente_valido(resultado_bruto):
        return False
    try:
        doc = json.loads(resultado_bruto)
    except (TypeError, json.JSONDecodeError):
        return False

    if not isinstance(doc, dict):
        return False
    if doc.get("tipo") != "multinivel":
        return False
    formato = doc.get("formato")
    if not isinstance(formato, dict):
        return False
    if formato.get("apresentacao") != "conjuntos_campos":
        return False
    if "campos" not in formato or not isinstance(formato["campos"], dict):
        return False
    niveis = formato.get("niveis")
    if not isinstance(niveis, list) or len(niveis) != 3:
        return False

    ids_niveis = []
    niveis_por_id = {}
    for nivel, esperado_id in zip(niveis, IDS_NIVEIS_H0042):
        if not _validar_nivel_declarado(nivel, {esperado_id}):
            return False
        if nivel.get("id") != esperado_id:
            return False
        tipo_esperado = {
            "secao": "container",
            "registro": "container",
            "campo": "nome_valor",
        }[esperado_id]
        if nivel.get("tipo") != tipo_esperado:
            return False
        ids_niveis.append(esperado_id)
        niveis_por_id[esperado_id] = nivel
    if len(set(ids_niveis)) != 3:
        return False

    dados = doc.get("dados")
    if not isinstance(dados, list) or len(dados) != 2:
        return False
    for no in dados:
        if not _validar_no(no, niveis_por_id):
            return False

    secoes = {no.get("titulo"): no for no in dados}
    if "Resumo" not in secoes or "Itens" not in secoes:
        return False

    resumo = secoes["Resumo"]
    if len(resumo.get("filhos", [])) != 1:
        return False
    reg_exec = resumo["filhos"][0]
    if reg_exec.get("titulo") != "Execução":
        return False
    mapa_resumo = _mapa_campos(reg_exec.get("filhos"))
    if mapa_resumo is None:
        return False
    if set(mapa_resumo) != set(CAMPOS_RESUMO_OBRIGATORIOS):
        return False
    if mapa_resumo["modo"] not in MODOS_AUTORIZADOS:
        return False
    if mapa_resumo["status"] not in STATUS_AUTORIZADOS:
        return False
    for contador in (
        "solicitados",
        "processados",
        "ignorados",
        "nao_encontrados",
        "falhos",
    ):
        valor = mapa_resumo[contador]
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
            return False

    itens = secoes["Itens"]
    filhos_itens = itens.get("filhos")
    if not isinstance(filhos_itens, list):
        return False
    for registro in filhos_itens:
        if registro.get("nivel") != "registro":
            return False
        if not _validar_item_registro(registro):
            return False

    return True


def classificar_processo(codigo_saida, resultado_bruto):
    """Classifica o processo externo.

    Sucesso externo exige simultaneamente codigo 0, existencia do resultado,
    JSON sintaticamente valido e documento semanticamente valido (H-0042).
    """
    if codigo_saida != 0:
        return "falha"
    if not resultado_existente(resultado_bruto):
        return "falha"
    if not resultado_json_sintaticamente_valido(resultado_bruto):
        return "falha"
    if not resultado_semanticamente_valido(resultado_bruto):
        return "falha"
    return "sucesso"


def _argv_executor_autorizado(entrada, resultado, dry_run):
    """Monta o argv fixo do unico executor autorizado."""
    argv = [
        sys.executable,
        "-m",
        MODULO_EXECUTOR_AUTORIZADO,
        "--entrada",
        str(entrada),
        "--resultado",
        str(resultado),
    ]
    if dry_run:
        argv.append("--dry-run")
    return argv


def _invocar_subprocesso(argv, *, cwd, env):
    """Invoca o subprocesso autorizado (substituivel apenas em teste)."""
    return subprocess.run(
        argv,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        check=False,
        shell=False,
    )


def _ler_resultado_bruto(caminho_resultado):
    caminho = Path(caminho_resultado)
    if not caminho.is_file():
        return None, False
    # Preserva bytes decodificados como texto UTF-8 sem re-serializar JSON.
    try:
        bruto = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        bruto = caminho.read_bytes().decode("utf-8", errors="surrogateescape")
    return bruto, True


def executar_protocolo_focal(
    caminho_entrada,
    caminho_fixture,
    *,
    dry_run=False,
    antes_da_limpeza=None,
    cwd=None,
):
    """Executa o protocolo focal completo sobre copia temporaria.

    Parametros
    ----------
    caminho_entrada:
        Fixture permanente de entrada ``selecao_execucao.v1``.
    caminho_fixture:
        Baseline permanente (nunca alterada).
    dry_run:
        Se True, repassa ``--dry-run`` ao executor.
    antes_da_limpeza:
        Callback opcional ``fn(contexto)`` chamado antes de remover o
        diretorio temporario (inspecao interna de teste/demonstracao).
    cwd:
        Diretorio de trabalho do subprocesso (default: raiz do repositorio).

    Retorna dict com codigo_saida, stdout, stderr, resultado_bruto,
    resultado_existe, classificacao e metadados. O diretorio temporario nao
    sobrevive ao retorno.

    O executor e exclusivamente ``python -m demo.executor_sintetico``. A API
    produtiva nao aceita argv, modulo, executavel ou comando alternativos.
    """
    caminho_entrada = Path(caminho_entrada).resolve()
    caminho_fixture = Path(caminho_fixture).resolve()
    if cwd is None:
        cwd = str(Path(__file__).resolve().parent.parent)

    diretorio = tempfile.mkdtemp(prefix="h0042_focal_")
    entrada_tmp = Path(diretorio) / NOME_ENTRADA
    resultado_tmp = Path(diretorio) / NOME_RESULTADO
    fixture_tmp = Path(diretorio) / NOME_FIXTURE_TRABALHO

    codigo_saida = 1
    stdout = ""
    stderr = ""
    resultado_bruto = None
    resultado_existe = False
    entrada_valida = False
    invocou = False

    try:
        shutil.copy2(caminho_entrada, entrada_tmp)
        shutil.copy2(caminho_fixture, fixture_tmp)
        # resultado.json criado previamente pela camada invocadora
        resultado_tmp.write_text("", encoding="utf-8")

        try:
            ler_e_validar_entrada(entrada_tmp)
            entrada_valida = True
        except EntradaInvalida as exc:
            stderr = f"ERRO: entrada invalida: {exc}\n"
            codigo_saida = 1
            entrada_valida = False

        if entrada_valida:
            argv = _argv_executor_autorizado(entrada_tmp, resultado_tmp, dry_run)
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            proc = _invocar_subprocesso(argv, cwd=cwd, env=env)
            invocou = True
            codigo_saida = int(proc.returncode)
            stdout = proc.stdout if proc.stdout is not None else ""
            stderr = proc.stderr if proc.stderr is not None else ""

        resultado_bruto, resultado_existe = _ler_resultado_bruto(resultado_tmp)
        classificacao = classificar_processo(codigo_saida, resultado_bruto)

        contexto = {
            "diretorio": diretorio,
            "entrada": str(entrada_tmp),
            "resultado": str(resultado_tmp),
            "fixture_trabalho": str(fixture_tmp),
            "codigo_saida": codigo_saida,
            "stdout": stdout,
            "stderr": stderr,
            "resultado_bruto": resultado_bruto,
            "resultado_existe": resultado_existe,
            "classificacao": classificacao,
            "entrada_valida": entrada_valida,
            "invocou": invocou,
            "dry_run": dry_run,
            "baseline": str(caminho_fixture),
        }
        if antes_da_limpeza is not None:
            antes_da_limpeza(contexto)

        return {
            "codigo_saida": codigo_saida,
            "stdout": stdout,
            "stderr": stderr,
            "resultado_bruto": resultado_bruto,
            "resultado_existe": resultado_existe,
            "classificacao": classificacao,
            "entrada_valida": entrada_valida,
            "invocou": invocou,
            "dry_run": dry_run,
            "diretorio_removido": True,
        }
    finally:
        shutil.rmtree(diretorio, ignore_errors=True)
