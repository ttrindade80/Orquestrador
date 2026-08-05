"""Controle de execução real/dry-run por instância de tela."""

from __future__ import annotations

import copy
from dataclasses import dataclass


MODOS_EXECUCAO = ("executar", "dry_run")
ROTULOS_EXECUCAO = {"executar": "Real", "dry_run": "Simulação"}


class ControleExecucaoErro(ValueError):
    """Falha fechada do controle de execução."""


@dataclass(frozen=True)
class _RequisicaoExecucaoCapturada:
    """Detalhe interno, imutável e não serializado da chamada registrada."""

    lote_reconciliado: tuple
    modo_capturado: str

    def __post_init__(self):
        if self.modo_capturado not in MODOS_EXECUCAO:
            raise ControleExecucaoErro("modo capturado invalido")
        object.__setattr__(
            self,
            "lote_reconciliado",
            tuple(copy.deepcopy(tuple(self.lote_reconciliado))),
        )

    @property
    def modo(self):
        return self.modo_capturado

    @property
    def lote(self):
        return self.lote_reconciliado


@dataclass(frozen=True)
class ControleExecucaoRepresentacao:
    """Valor transitório consumido pela barra, sem virar estado de UI."""

    modo: str
    chip_id: str
    rotulo: str
    destacado: bool

    def __bool__(self):
        return True


def validar_configuracao_controle_execucao(configuracao, caminho="controle_execucao"):
    if not isinstance(configuracao, dict):
        raise ControleExecucaoErro(
            "CONFIGURACAO_INVALIDA em {0}: esperado objeto".format(caminho)
        )
    desconhecidos = sorted(set(configuracao) - {"modo_inicial"})
    if desconhecidos:
        raise ControleExecucaoErro(
            "CONFIGURACAO_INVALIDA em {0}: campo(s) desconhecido(s) {1!r}".format(
                caminho, desconhecidos
            )
        )
    if "modo_inicial" not in configuracao:
        raise ControleExecucaoErro(
            "CONFIGURACAO_INVALIDA em {0}.modo_inicial: campo ausente".format(
                caminho
            )
        )
    modo = configuracao["modo_inicial"]
    if not isinstance(modo, str) or modo not in MODOS_EXECUCAO:
        raise ControleExecucaoErro(
            "CONFIGURACAO_INVALIDA em {0}.modo_inicial: valor {1!r}".format(
                caminho, modo
            )
        )
    return {"modo_inicial": modo}


def configuracao_controle_execucao_de(tela_raw):
    if not isinstance(tela_raw, dict):
        raise ControleExecucaoErro("tela_raw invalida")
    if "controle_execucao" not in tela_raw:
        return None
    return validar_configuracao_controle_execucao(tela_raw["controle_execucao"])


class ControleExecucao:
    """Estado único e descartável de uma instância aberta."""

    def __init__(self, configuracao, acoes, *, chip_id="chip_controle_execucao"):
        self._configuracao = validar_configuracao_controle_execucao(configuracao)
        self._acoes = tuple(acoes or ())
        self._modo_atual = self._configuracao["modo_inicial"]
        self._chip_id = chip_id
        processos = [acao for acao in self._acoes if acao.categoria == "processo"]
        self._acao_processo = processos[0] if processos else None
        if self._acao_processo is None:
            raise ControleExecucaoErro(
                "tela adotante sem acao de processo resolvida"
            )
        modos = set(self._acao_processo.modos_execucao_aceitos or ())
        if modos != set(MODOS_EXECUCAO):
            raise ControleExecucaoErro(
                "acao de processo inelegivel para controle de execucao"
            )

    @property
    def modo_inicial(self):
        return self._configuracao["modo_inicial"]

    @property
    def modo_atual(self):
        return self._modo_atual

    @property
    def acao_processo(self):
        return self._acao_processo

    @property
    def configuracao(self):
        return dict(self._configuracao)

    def alternar(self):
        self._modo_atual = (
            "dry_run" if self._modo_atual == "executar" else "executar"
        )
        return self._modo_atual

    def representacao_chip(self):
        return ControleExecucaoRepresentacao(
            modo=self._modo_atual,
            chip_id=self._chip_id,
            rotulo=ROTULOS_EXECUCAO[self._modo_atual],
            destacado=self._modo_atual == "dry_run",
        )

    def contexto_renderizacao(self):
        representacao = self.representacao_chip()
        return ({representacao.chip_id: representacao.destacado}, representacao)

    def capturar(self, lote_reconciliado):
        lote = tuple(lote_reconciliado)
        if not lote:
            return None
        return _RequisicaoExecucaoCapturada(
            lote_reconciliado=lote,
            modo_capturado=self._modo_atual,
        )

    def executar(self, lote_reconciliado):
        lote = tuple(lote_reconciliado)
        if not lote:
            return None
        captura = self.capturar(lote)
        if captura is None:
            return None
        return self._acao_processo.executar(captura)


def criar_controle_execucao(configuracao, acoes, *, chip_id="chip_controle_execucao"):
    return ControleExecucao(configuracao, acoes, chip_id=chip_id)


__all__ = [
    "ControleExecucao",
    "ControleExecucaoErro",
    "ControleExecucaoRepresentacao",
    "MODOS_EXECUCAO",
    "ROTULOS_EXECUCAO",
    "configuracao_controle_execucao_de",
    "criar_controle_execucao",
    "validar_configuracao_controle_execucao",
]
