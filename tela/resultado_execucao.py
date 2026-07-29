"""Carregamento e apresentacao da tela padrao de resultado (H-0043 / ADR-0036).

Valida o perfil ``resultado_execucao``, recebe o documento de runtime capturado
pelo fluxo focal (H-0042), classifica documento direto versus envelope de erro,
materializa o envelope deterministico quando aplicavel, preserva o texto bruto
de ``resultado_json`` e expoe um ``ModeloTela`` ja validado ao renderer.

Nao executa processo, nao seleciona itens, nao abre/troca telas, nao mantem
pilha, nao emite ANSI, nao escolhe cor e nao persiste o modelo.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from tela.execucao_focal import (
    resultado_json_sintaticamente_valido,
    resultado_semanticamente_valido,
)
from tela.loader import (
    PERFIL_RESULTADO_EXECUCAO,
    TelaEstruturaInvalida,
    carregar_tela,
    validar_conteudo_externo,
)
from tela.modelo import ModeloTela, construir_modelo


DIAGNOSTICO_CODIGO_NAO_ZERO = (
    "A execução terminou com código de saída não zero."
)
DIAGNOSTICO_RESULTADO_AUSENTE = (
    "A execução não produziu o documento de resultado."
)
DIAGNOSTICO_RESULTADO_MALFORMADO = (
    "O documento de resultado não contém JSON válido."
)
DIAGNOSTICO_RESULTADO_SEMANTICO = (
    "O documento de resultado não atende ao schema esperado."
)
DIAGNOSTICO_INTERRUPCAO = "A execução foi interrompida."

EXIBICAO_INDISPONIVEL = "indisponível"

CAMPOS_ENVELOPE_ORDEM = (
    "status",
    "diagnostico",
    "codigo_saida",
    "stdout",
    "stderr",
    "resultado_json",
)

CODIGO_INTERRUPCAO = 130

APRESENTACAO_DOCUMENTO = "documento"
APRESENTACAO_ENVELOPE = "envelope"

_CHAVES_RUNTIME = frozenset(
    {"codigo_saida", "stdout", "stderr", "resultado_bruto"}
)


class ResultadoExecucaoErro(ValueError):
    """Erro de dominio na construcao da tela de resultado."""


@dataclass(frozen=True)
class DocumentoRuntime:
    """Forma de entrada capturada pelo fluxo focal (H-0042), sem redefinicao."""

    codigo_saida: int
    stdout: str
    stderr: str
    resultado_bruto: str | None


@dataclass
class SessaoResultado:
    """Modelo composto em memoria para a sessao/cenario atual.

    O modelo e construido uma unica vez; redesenho/SIGWINCH reutilizam a
    mesma instancia sem reler tela.json nem o documento de runtime.
    """

    modelo: ModeloTela
    apresentacao: str
    diagnostico: str | None
    documento_runtime: DocumentoRuntime
    conteudo_apresentado: dict
    id_cenario: str | None = None


def carregar_documento_runtime(caminho):
    """Carrega a fixture de runtime (forma H-0042) a partir de um caminho."""
    caminho = Path(caminho)
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError as exc:
        raise ResultadoExecucaoErro(
            "documento de runtime ilegivel: {0}".format(exc)
        ) from exc
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ResultadoExecucaoErro(
            "documento de runtime nao e JSON valido: {0}".format(exc)
        ) from exc
    return validar_documento_runtime(dados)


def validar_documento_runtime(dados):
    """Valida a forma de entrada do documento de runtime capturado."""
    if not isinstance(dados, dict):
        raise ResultadoExecucaoErro("documento de runtime deve ser objeto")
    extras = set(dados) - _CHAVES_RUNTIME
    if extras:
        raise ResultadoExecucaoErro(
            "documento de runtime com campos nao reconhecidos: {0}".format(
                ", ".join(sorted(extras))
            )
        )
    faltando = _CHAVES_RUNTIME - set(dados)
    if faltando:
        raise ResultadoExecucaoErro(
            "documento de runtime sem campos obrigatorios: {0}".format(
                ", ".join(sorted(faltando))
            )
        )
    codigo = dados["codigo_saida"]
    if not isinstance(codigo, int) or isinstance(codigo, bool):
        raise ResultadoExecucaoErro("codigo_saida deve ser int")
    stdout = dados["stdout"]
    stderr = dados["stderr"]
    if not isinstance(stdout, str):
        raise ResultadoExecucaoErro("stdout deve ser str")
    if not isinstance(stderr, str):
        raise ResultadoExecucaoErro("stderr deve ser str")
    bruto = dados["resultado_bruto"]
    if bruto is not None and not isinstance(bruto, str):
        raise ResultadoExecucaoErro("resultado_bruto deve ser str ou null")
    return DocumentoRuntime(
        codigo_saida=codigo,
        stdout=stdout,
        stderr=stderr,
        resultado_bruto=bruto,
    )


def validar_compatibilidade_perfil(tela_raw):
    """Confirma que a tela carregada declara o perfil ``resultado_execucao``."""
    if not isinstance(tela_raw, dict):
        raise ResultadoExecucaoErro("tela_raw invalida")
    perfil = tela_raw.get("perfil")
    if perfil != PERFIL_RESULTADO_EXECUCAO:
        raise ResultadoExecucaoErro(
            "perfil incompativel: esperado {0!r}, recebido {1!r}".format(
                PERFIL_RESULTADO_EXECUCAO, perfil
            )
        )
    return tela_raw


def classificar_apresentacao(documento_runtime):
    """Decide documento direto versus envelope (D-H3-10).

    Ordem vinculante: interrupcao (130) > codigo nao zero > resultado ausente
    > malformado > semanticamente invalido > documento original.
    """
    if not isinstance(documento_runtime, DocumentoRuntime):
        raise ResultadoExecucaoErro("documento_runtime invalido")

    codigo = documento_runtime.codigo_saida
    bruto = documento_runtime.resultado_bruto

    if codigo == CODIGO_INTERRUPCAO:
        return APRESENTACAO_ENVELOPE, DIAGNOSTICO_INTERRUPCAO
    if codigo != 0:
        return APRESENTACAO_ENVELOPE, DIAGNOSTICO_CODIGO_NAO_ZERO
    if bruto is None:
        return APRESENTACAO_ENVELOPE, DIAGNOSTICO_RESULTADO_AUSENTE
    if not resultado_json_sintaticamente_valido(bruto):
        return APRESENTACAO_ENVELOPE, DIAGNOSTICO_RESULTADO_MALFORMADO
    if not resultado_semanticamente_valido(bruto):
        return APRESENTACAO_ENVELOPE, DIAGNOSTICO_RESULTADO_SEMANTICO
    return APRESENTACAO_DOCUMENTO, None


def _exibir_canal(texto):
    if texto is None or texto == "":
        return EXIBICAO_INDISPONIVEL
    return texto


def materializar_envelope(documento_runtime, diagnostico):
    """Materializa o envelope multinivel ``conjuntos_campos`` (D-H3-15a).

    Preserva ``resultado_bruto`` literalmente no campo ``resultado_json``:
    ausencia de conteudo permanece ``None`` no modelo (a conversao para o
    texto "indisponível" e responsabilidade exclusiva da apresentacao, em
    ``tela.renderizador``); presenca de conteudo preserva o texto bruto sem
    correcao, normalizacao ou reserializacao.
    """
    if diagnostico not in {
        DIAGNOSTICO_CODIGO_NAO_ZERO,
        DIAGNOSTICO_RESULTADO_AUSENTE,
        DIAGNOSTICO_RESULTADO_MALFORMADO,
        DIAGNOSTICO_RESULTADO_SEMANTICO,
        DIAGNOSTICO_INTERRUPCAO,
    }:
        raise ResultadoExecucaoErro(
            "diagnostico nao canonico: {0!r}".format(diagnostico)
        )

    valores = {
        "status": "falha",
        "diagnostico": diagnostico,
        "codigo_saida": documento_runtime.codigo_saida,
        "stdout": _exibir_canal(documento_runtime.stdout),
        "stderr": _exibir_canal(documento_runtime.stderr),
        "resultado_json": documento_runtime.resultado_bruto,
    }
    filhos = []
    for nome in CAMPOS_ENVELOPE_ORDEM:
        filhos.append(
            {
                "id": "env_{0}".format(nome),
                "nivel": "elemento",
                "nome": nome,
                "valor": valores[nome],
            }
        )

    envelope = {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "conjuntos_campos",
            "niveis": [
                {
                    "id": "conjunto",
                    "tipo": "container",
                    "conteudo": "titulo",
                    "designador": {"tipo": "nenhum"},
                },
                {
                    "id": "elemento",
                    "tipo": "nome_valor",
                    "conteudo": {"nome": "nome", "valor": "valor"},
                    "designador": {"tipo": "nenhum"},
                },
            ],
            "campos": {
                "separador": ":",
                "justificar_nomes": True,
                "escopo_justificacao": "por_conjunto",
            },
        },
        "dados": [
            {
                "id": "conjunto_envelope",
                "nivel": "conjunto",
                "titulo": "Erro",
                "filhos": filhos,
            }
        ],
    }
    validar_conteudo_externo(envelope, origem="envelope de erro")
    return envelope


def documento_para_apresentacao(documento_runtime):
    """Devolve (apresentacao, diagnostico, conteudo_multinivel)."""
    apresentacao, diagnostico = classificar_apresentacao(documento_runtime)
    if apresentacao == APRESENTACAO_DOCUMENTO:
        try:
            conteudo = json.loads(documento_runtime.resultado_bruto)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ResultadoExecucaoErro(
                "documento classificado como valido nao decodifica: {0}".format(
                    exc
                )
            ) from exc
        if not isinstance(conteudo, dict):
            raise ResultadoExecucaoErro(
                "documento de resultado nao e objeto apos decodificacao"
            )
        return apresentacao, diagnostico, conteudo
    envelope = materializar_envelope(documento_runtime, diagnostico)
    return apresentacao, diagnostico, envelope


def construir_modelo_resultado(tela_raw, documento_runtime):
    """Constroi o ``ModeloTela`` composto a partir de tela + runtime.

    A tela e o documento chegam separados; o conteudo nunca e reinserido no
    objeto bruto do ``tela.json``.
    """
    validar_compatibilidade_perfil(tela_raw)
    if not isinstance(documento_runtime, DocumentoRuntime):
        documento_runtime = validar_documento_runtime(documento_runtime)
    apresentacao, diagnostico, conteudo = documento_para_apresentacao(
        documento_runtime
    )
    modelo = construir_modelo(tela_raw, conteudo_externo=conteudo)
    return SessaoResultado(
        modelo=modelo,
        apresentacao=apresentacao,
        diagnostico=diagnostico,
        documento_runtime=documento_runtime,
        conteudo_apresentado=conteudo,
    )


def carregar_sessao_resultado(
    caminho_base,
    id_cenario,
    caminho_runtime,
    raiz_telas=None,
    id_tela=PERFIL_RESULTADO_EXECUCAO,
):
    """Carrega tela e documento uma vez e constroi a sessao em memoria.

    ``id_tela`` e sempre a tela estrutural ``resultado_execucao``; o cenario
    seleciona apenas a fixture de runtime.
    """
    if raiz_telas is None:
        raiz_telas = "config/telas/demo"
    tela_raw = carregar_tela(caminho_base, id_tela, raiz_telas=raiz_telas)
    documento = carregar_documento_runtime(caminho_runtime)
    sessao = construir_modelo_resultado(tela_raw, documento)
    sessao.id_cenario = id_cenario
    return sessao
