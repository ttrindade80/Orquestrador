"""Registro autoritativo e pequeno de ações de tela.

O registro é deliberadamente explícito: uma referência só é resolvida quando
foi registrada pelo chamador. Não há descoberta, reflexão, persistência ou
inferência a partir de nomes, rótulos ou implementações.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


CATEGORIAS_VALIDAS = frozenset(("processo", "navegacao", "visualizacao"))
MODOS_EXECUCAO_VALIDOS = ("executar", "dry_run")
_MODOS_EXECUCAO_SET = frozenset(MODOS_EXECUCAO_VALIDOS)
_CAMPOS_REFERENCIA_ORDEM = (
    "acao_enter",
    "executar_acao",
    "acao",
    "processo",
    "navegacao",
    "visualizacao",
)
_CAMPOS_REFERENCIA = frozenset(_CAMPOS_REFERENCIA_ORDEM)


class RegistroAcoesErro(ValueError):
    """Falha fechada na declaração, resolução ou elegibilidade de uma ação."""


@dataclass(frozen=True)
class AcaoRegistrada:
    """Entrada autoritativa resolvida pelo registro."""

    identidade: str
    categoria: str
    modos_execucao_aceitos: tuple[str, ...] | None = None
    executor: object = None

    def executar(self, requisicao):
        if self.executor is None or not callable(self.executor):
            raise RegistroAcoesErro(
                "acao sem executor chamavel: {0!r}".format(self.identidade)
            )
        return self.executor(requisicao)


def _identidade_valida(identidade):
    return isinstance(identidade, str) and bool(identidade)


def _normalizar_modos(modos, identidade):
    if modos is None:
        return None
    if isinstance(modos, str) or not isinstance(modos, (list, tuple, set, frozenset)):
        raise RegistroAcoesErro(
            "modos_execucao_aceitos invalido para acao {0!r}".format(identidade)
        )
    valores = tuple(modos)
    desconhecidos = sorted(set(valores) - _MODOS_EXECUCAO_SET)
    if desconhecidos:
        raise RegistroAcoesErro(
            "modo(s) de execucao desconhecido(s) para acao {0!r}: {1!r}".format(
                identidade, desconhecidos
            )
        )
    if len(set(valores)) != len(valores):
        raise RegistroAcoesErro(
            "modos_execucao_aceitos duplicados para acao {0!r}".format(identidade)
        )
    return tuple(modo for modo in MODOS_EXECUCAO_VALIDOS if modo in valores)


def _validar_entrada(identidade, categoria, modos):
    if not _identidade_valida(identidade):
        raise RegistroAcoesErro("identidade de acao invalida")
    if categoria not in CATEGORIAS_VALIDAS:
        raise RegistroAcoesErro(
            "categoria desconhecida para acao {0!r}: {1!r}".format(
                identidade, categoria
            )
        )
    if categoria == "processo" and modos is None:
        raise RegistroAcoesErro(
            "acao de processo sem modos_execucao_aceitos: {0!r}".format(identidade)
        )
    if categoria != "processo" and modos not in (None, (), [], set(), frozenset()):
        raise RegistroAcoesErro(
            "acao nao-processo nao declara modos de execucao: {0!r}".format(
                identidade
            )
        )


class RegistroAcoes:
    """Registro explícito, independente e reutilizável de ações."""

    def __init__(self):
        self._acoes = {}

    def registrar(
        self,
        identidade,
        categoria,
        modos_execucao_aceitos=None,
        executor=None,
    ):
        modos = _normalizar_modos(modos_execucao_aceitos, identidade)
        _validar_entrada(identidade, categoria, modos)
        if identidade in self._acoes:
            raise RegistroAcoesErro(
                "acao ja registrada: {0!r}".format(identidade)
            )
        acao = AcaoRegistrada(
            identidade=identidade,
            categoria=categoria,
            modos_execucao_aceitos=modos,
            executor=executor,
        )
        self._acoes[identidade] = acao
        return acao

    def registrar_acao(self, *args, **kwargs):
        return self.registrar(*args, **kwargs)

    def resolver(self, referencia):
        if isinstance(referencia, dict):
            if set(referencia) - frozenset(("id", "identidade", "referencia")):
                raise RegistroAcoesErro(
                    "referencia de acao possui propriedades desconhecidas"
                )
            referencia = (
                referencia.get("id")
                or referencia.get("identidade")
                or referencia.get("referencia")
            )
        if not _identidade_valida(referencia) or referencia not in self._acoes:
            raise RegistroAcoesErro(
                "acao nao resolvida: {0!r}".format(referencia)
            )
        return self._acoes[referencia]

    def resolver_acao(self, referencia):
        return self.resolver(referencia)

    def declaracoes(self):
        return MappingProxyType(dict(self._acoes))


def registrar_acao(registro, identidade, categoria, modos_execucao_aceitos=None, executor=None):
    """Atalho nominal para registrar em uma instância fornecida pelo chamador."""
    if not isinstance(registro, RegistroAcoes):
        raise RegistroAcoesErro("registro explicito obrigatorio")
    return registro.registrar(
        identidade,
        categoria,
        modos_execucao_aceitos=modos_execucao_aceitos,
        executor=executor,
    )


def _referencias_de_no(no):
    if isinstance(no, str):
        return [no]
    if isinstance(no, list):
        referencias = []
        for item in no:
            referencias.extend(_referencias_de_no(item))
        return referencias
    if not isinstance(no, dict):
        raise RegistroAcoesErro("referencia de acao deve ser string, lista ou objeto")
    desconhecidos = set(no) - _CAMPOS_REFERENCIA
    if desconhecidos:
        raise RegistroAcoesErro(
            "campo(s) de referencia de acao desconhecido(s): {0!r}".format(
                sorted(desconhecidos)
            )
        )
    referencias = []
    for campo in no:
        referencias.extend(_referencias_de_no(no[campo]))
    return referencias


def referencias_de_acoes_de(tela_raw):
    """Retorna somente referências declaradas nos campos vigentes da tela."""
    if not isinstance(tela_raw, dict):
        raise RegistroAcoesErro("tela_raw invalida")
    referencias = []
    if "referencias_de_acoes" in tela_raw:
        referencias.extend(_referencias_de_no(tela_raw["referencias_de_acoes"]))
    if "acao_enter" in tela_raw:
        referencias.extend(_referencias_de_no(tela_raw["acao_enter"]))
    return tuple(dict.fromkeys(referencias))


def resolver_acoes_relevantes(tela_raw, registro):
    """Resolve as referências declaradas, sem fallback ou descoberta."""
    if not isinstance(registro, RegistroAcoes):
        raise RegistroAcoesErro("registro explicito obrigatorio")
    return tuple(registro.resolver(ref) for ref in referencias_de_acoes_de(tela_raw))


def validar_elegibilidade(tela_raw, registro):
    """Resolve ações e aplica a regra de elegibilidade do controle."""
    acoes = resolver_acoes_relevantes(tela_raw, registro)
    if not isinstance(tela_raw, dict) or "controle_execucao" not in tela_raw:
        return acoes
    for acao in acoes:
        if acao.categoria not in CATEGORIAS_VALIDAS:
            raise RegistroAcoesErro(
                "categoria invalida na acao {0!r}".format(acao.identidade)
            )
        if acao.categoria == "processo":
            modos = set(acao.modos_execucao_aceitos or ())
            if modos != _MODOS_EXECUCAO_SET:
                raise RegistroAcoesErro(
                    "acao de processo inelegivel para os dois modos: {0!r}".format(
                        acao.identidade
                    )
                )
    return acoes


__all__ = [
    "AcaoRegistrada",
    "CATEGORIAS_VALIDAS",
    "MODOS_EXECUCAO_VALIDOS",
    "RegistroAcoes",
    "RegistroAcoesErro",
    "registrar_acao",
    "referencias_de_acoes_de",
    "resolver_acoes_relevantes",
    "validar_elegibilidade",
]
