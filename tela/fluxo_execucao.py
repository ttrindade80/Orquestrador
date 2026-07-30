"""Coordenador focal do fluxo integrado H-0044 / ADR-0037.

Mantem a origem viva, o toggle dry-run, a ativacao cumulativa de Executar,
a transicao atomica origem→resultado (H-0042 + H-0043) e os retornos
diferenciados dry-run/real. Modulo especifico do H-0044 — nao e gerenciador
generico de telas, nem dispatcher, nem pilha.

Apenas biblioteca padrao do Python.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from tela import navegacao
from tela import selecao
from tela.execucao_focal import executar_protocolo_focal
from tela.loader import carregar_tela
from tela.resultado_execucao import (
    DocumentoRuntime,
    construir_modelo_resultado,
)

ID_TELA_H0044 = "h0044_fluxo_execucao_integrado"
ID_TELA_RESULTADO = "resultado_execucao"
ID_CHIP_DRY_RUN = "chip_dry_run"

TECLA_INSERT = "\x1b[2~"
TECLAS_ENTER = ("\r", "\n")
TECLA_ESC = "\x1b"

SCHEMA_SELECAO = "selecao_execucao.v1"

_RAIZ = Path(__file__).resolve().parent.parent
_RAIZ_TELAS_DEMO = _RAIZ / "config" / "telas" / "demo"
_FIXTURE_BASELINE = _RAIZ / "demo" / "fixtures" / "h0042_fixture_execucao.json"


class FluxoExecucaoErro(RuntimeError):
    """Erro interno do coordenador focal H-0044."""


class FluxoExecucao:
    """Estado focal da sessao H-0044.

    Representacao equivalente obrigatoria:

    - ``origem_ativa``: referencia viva (modelo + estado de runtime)
    - ``origem_suspensa``: zero ou uma referencia (mesma instancia)
    - ``modelo_resultado``: zero ou uma ``SessaoResultado``
    - ``dry_run_ativo``: bool
    - ``transicao_em_andamento``: bool
    """

    def __init__(
        self,
        modelo_origem,
        *,
        tela_resultado_raw=None,
        caminho_fixture=None,
        executor_disponivel=None,
        recarregador=None,
        protocolo_focal=None,
        id_chip_dry_run=ID_CHIP_DRY_RUN,
    ):
        self.origem_ativa = modelo_origem
        self.origem_suspensa = None
        self.modelo_resultado = None
        self.dry_run_ativo = False
        self.transicao_em_andamento = False

        self._tela_resultado_raw = tela_resultado_raw
        self._resultado_prevalidado = tela_resultado_raw is not None
        self._caminho_fixture = Path(
            caminho_fixture if caminho_fixture is not None else _FIXTURE_BASELINE
        )
        if executor_disponivel is None:
            self._executor_disponivel = callable(executar_protocolo_focal)
        else:
            self._executor_disponivel = bool(executor_disponivel)
        self._recarregador = recarregador
        self._chamadas_recarregador = 0
        self._protocolo = protocolo_focal or executar_protocolo_focal
        self._id_chip_dry_run = id_chip_dry_run
        # Snapshot semantico capturado na suspensao (mesma referencia de modelo).
        self._modo_na_transicao = None
        self._filtro_suspenso = None
        self._pagina_suspensa = None
        self._foco_suspenso = None
        self._cursores_suspensos = None
        self._ids_cursor_suspensos = None
        self._id_console_foco_suspenso = None
        self._selecoes_suspensas = None
        self._estado_runtime = None

    # ------------------------------------------------------------------
    # Fabrica / pre-validacao
    # ------------------------------------------------------------------

    @classmethod
    def criar_sessao(
        cls,
        modelo_origem,
        *,
        raiz_telas=None,
        caminho_fixture=None,
        recarregador=None,
        protocolo_focal=None,
        executor_disponivel=None,
        id_chip_dry_run=ID_CHIP_DRY_RUN,
    ):
        """Pre-valida ``resultado_execucao`` e confirma o executor focal."""
        if raiz_telas is None:
            raiz_telas = str(_RAIZ_TELAS_DEMO)
        tela_raw = carregar_tela(None, ID_TELA_RESULTADO, raiz_telas=raiz_telas)
        if not callable(executar_protocolo_focal) and executor_disponivel is None:
            raise FluxoExecucaoErro("executor focal indisponivel")
        return cls(
            modelo_origem,
            tela_resultado_raw=tela_raw,
            caminho_fixture=caminho_fixture,
            executor_disponivel=executor_disponivel,
            recarregador=recarregador,
            protocolo_focal=protocolo_focal,
            id_chip_dry_run=id_chip_dry_run,
        )

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    @property
    def resultado_ativo(self):
        return self.modelo_resultado is not None and self.origem_suspensa is not None

    @property
    def chamadas_recarregador(self):
        return self._chamadas_recarregador

    @property
    def resultado_prevalidado(self):
        return self._resultado_prevalidado

    @property
    def executor_disponivel(self):
        return self._executor_disponivel

    def chips_destacados(self):
        """Conjunto de IDs ja resolvidos para o renderer (sem hardcoding la)."""
        if self.resultado_ativo:
            return frozenset()
        if self.dry_run_ativo:
            return frozenset({self._id_chip_dry_run})
        return frozenset()

    def lote_reconciliado(self, estado, console=None):
        console = console or self._console_focado(estado)
        if console is None:
            return []
        return list(selecao.selecao(console, estado))

    def condicoes_executar(self, estado, console=None):
        lote = self.lote_reconciliado(estado, console)
        return {
            "lote_reconciliado_nao_vazio": len(lote) > 0,
            "executor_focal_disponivel": bool(self._executor_disponivel),
            "resultado_execucao_prevalidada": bool(self._resultado_prevalidado),
        }

    def executar_disponivel(self, estado, console=None):
        cond = self.condicoes_executar(estado, console)
        return all(cond.values())

    def modelo_para_render(self):
        if self.resultado_ativo:
            return self.modelo_resultado.modelo
        return self.origem_ativa

    # ------------------------------------------------------------------
    # Entrada
    # ------------------------------------------------------------------

    def processar_comando(self, estado, comando, modelo=None):
        """Processa Insert / Enter / Esc no fluxo H-0044.

        Retorna ``(novo_estado, modelo_render, consumido)``.
        ``consumido=False`` indica que o chamador deve seguir o dispatch legado.
        """
        if modelo is None:
            modelo = self.origem_ativa if not self.resultado_ativo else (
                self.modelo_resultado.modelo if self.modelo_resultado else None
            )

        if self.resultado_ativo:
            if comando == TECLA_ESC:
                return self._retornar_de_resultado(estado), self.origem_ativa, True
            # Insert e demais teclas nao atuam no resultado; nao mutam origem.
            return estado, self.modelo_resultado.modelo, True

        if comando == TECLA_INSERT:
            return self._toggle_dry_run(estado), self.origem_ativa, True

        if comando in TECLAS_ENTER:
            return self._processar_enter(estado, modelo)

        if comando == TECLA_ESC:
            return self._processar_esc_origem(estado, modelo)

        return estado, self.origem_ativa, False

    def _toggle_dry_run(self, estado):
        self.dry_run_ativo = not self.dry_run_ativo
        return estado

    def _processar_esc_origem(self, estado, modelo):
        # Delega limpeza de selecao / sair ao chamador (H-0041 + demo).
        return estado, self.origem_ativa, False

    def _processar_enter(self, estado, modelo):
        console = self._console_focado(estado, modelo)
        if console is None or not navegacao._console_declarou_selecao_multipla(console):
            return estado, self.origem_ativa, False

        selecao_bruta = selecao._selecao_do_console(estado, console)
        estado = selecao.reconciliar(estado, console)
        lote = self.lote_reconciliado(estado, console)

        if len(selecao_bruta) > 0 and len(lote) == 0:
            # Reconciliacao esvaziou: nao executa, nao aplica Todos.
            return estado, self.origem_ativa, True

        if len(lote) == 0:
            # Todos (H-0041) — nao consumido pelo fluxo de execucao.
            return estado, self.origem_ativa, False

        if not self.executar_disponivel(estado, console):
            return estado, self.origem_ativa, True

        estado, modelo_res = self.executar_transicao(estado, modelo, lote)
        return estado, modelo_res, True

    # ------------------------------------------------------------------
    # Transicao atomica
    # ------------------------------------------------------------------

    def executar_transicao(self, estado, modelo, lote=None):
        """Sequencia obrigatoria origem → resultado.

        A origem permanece ativa ate o modelo do resultado estar pronto.
        """
        if self.transicao_em_andamento or self.resultado_ativo:
            raise FluxoExecucaoErro("transicao ja em andamento ou resultado ativo")

        console = self._console_focado(estado, modelo)
        if console is None:
            raise FluxoExecucaoErro("console focado ausente")

        self.transicao_em_andamento = True
        caminho_entrada = None
        try:
            # 1. reconciliar
            estado = selecao.reconciliar(estado, console)
            # 2. congelar lote
            if lote is None:
                lote = self.lote_reconciliado(estado, console)
            lote = list(lote)
            if not lote:
                raise FluxoExecucaoErro("lote vazio apos reconciliacao")
            # 3. capturar dry_run
            dry = bool(self.dry_run_ativo)
            self._modo_na_transicao = dry
            # 4. preservar referencia da origem (ainda ativa)
            origem_ref = modelo
            assert origem_ref is self.origem_ativa
            # 5. entrada temporaria
            caminho_entrada = self._criar_entrada_temporaria(lote)
            # 6-7. H-0042
            resultado = self._protocolo(
                caminho_entrada,
                self._caminho_fixture,
                dry_run=dry,
            )
            # 8-9. DocumentoRuntime + modelo H-0043
            documento = DocumentoRuntime(
                codigo_saida=int(resultado["codigo_saida"]),
                stdout=resultado.get("stdout") or "",
                stderr=resultado.get("stderr") or "",
                resultado_bruto=resultado.get("resultado_bruto"),
            )
            sessao = construir_modelo_resultado(
                self._tela_resultado_raw, documento
            )
            # 10. somente entao suspender origem
            self._capturar_estado_suspensao(estado)
            self.origem_suspensa = origem_ref
            self.origem_ativa = None
            self.modelo_resultado = sessao
            return estado, sessao.modelo
        except Exception:
            # Excecao antes da suspensao: origem permanece ativa; limpa refs.
            self._limpar_refs_proprias(preservar_origem=True)
            raise
        finally:
            self.transicao_em_andamento = False
            if caminho_entrada is not None:
                try:
                    os.unlink(caminho_entrada)
                except OSError:
                    pass

    def _criar_entrada_temporaria(self, ids):
        fd, caminho = tempfile.mkstemp(prefix="h0044_selecao_", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(
                    {"schema": SCHEMA_SELECAO, "ids": list(ids)},
                    fh,
                    ensure_ascii=False,
                )
        except Exception:
            try:
                os.unlink(caminho)
            except OSError:
                pass
            raise
        return caminho

    def _capturar_estado_suspensao(self, estado):
        self._estado_runtime = estado
        self._filtro_suspenso = estado.get("filtro")
        self._pagina_suspensa = estado.get("pagina")
        self._foco_suspenso = estado.get("foco_console")
        self._cursores_suspensos = dict(estado.get("cursores") or {})
        self._selecoes_suspensas = {
            k: list(v) for k, v in (estado.get("selecoes") or {}).items()
        }
        self._ids_cursor_suspensos = {}
        self._id_console_foco_suspenso = None
        modelo = self.origem_ativa
        if modelo is None:
            return
        lista = navegacao.lista_foco(modelo)
        foco = estado.get("foco_console")
        if isinstance(foco, int) and 0 <= foco < len(lista):
            self._id_console_foco_suspenso = lista[foco].id
        for cons in lista:
            item = navegacao.item_selecionado(cons, estado)
            if isinstance(item, dict) and item.get("id") is not None:
                self._ids_cursor_suspensos[cons.id] = item.get("id")

    # ------------------------------------------------------------------
    # Retornos
    # ------------------------------------------------------------------

    def _retornar_de_resultado(self, estado):
        if not self.resultado_ativo:
            return estado
        foi_dry = bool(self._modo_na_transicao)
        origem = self.origem_suspensa
        estado_base = dict(estado)
        # Preserva geometria / estilo do estado corrente (SIGWINCH).
        if self._estado_runtime is not None:
            for chave in (
                "selecoes", "cursores", "foco_console", "filtro", "pagina",
            ):
                if chave in self._estado_runtime:
                    estado_base[chave] = self._estado_runtime[chave]

        if foi_dry:
            novo = self._retorno_dry_run(estado_base, origem)
        else:
            novo = self._retorno_real(estado_base, origem)

        self._limpar_refs_proprias(preservar_origem=False)
        self.origem_ativa = origem
        self.origem_suspensa = None
        self.modelo_resultado = None
        self._modo_na_transicao = None
        return novo

    def _retorno_dry_run(self, estado, origem):
        novo = dict(estado)
        if self._selecoes_suspensas is not None:
            novo["selecoes"] = {
                k: list(v) for k, v in self._selecoes_suspensas.items()
            }
        if self._cursores_suspensos is not None:
            novo["cursores"] = dict(self._cursores_suspensos)
        if self._foco_suspenso is not None:
            novo["foco_console"] = self._foco_suspenso
        if self._filtro_suspenso is not None:
            novo["filtro"] = self._filtro_suspenso
        if self._pagina_suspensa is not None:
            novo["pagina"] = self._pagina_suspensa
        # dry_run permanece ligado; zero recargas.
        self.dry_run_ativo = True
        return novo

    def _retorno_real(self, estado, origem):
        novo = dict(estado)
        console = None
        lista = navegacao.lista_foco(origem)
        # Limpar selecao
        novo["selecoes"] = {}
        for cons in lista:
            novo = selecao.limpar(novo, cons)

        # Recarregador focal exatamente uma vez
        if self._recarregador is not None:
            self._recarregador(origem)
            self._chamadas_recarregador += 1

        # Reaplicar filtro (valor preservado)
        if self._filtro_suspenso is not None:
            novo["filtro"] = self._filtro_suspenso

        # Reconciliar foco e cursor por ID
        novo = self._reconciliar_foco_cursor(
            novo,
            origem,
            self._foco_suspenso,
            self._cursores_suspensos or {},
        )
        self.dry_run_ativo = False
        return novo

    def _reconciliar_foco_cursor(self, estado, modelo, foco_ant, cursores_ant):
        novo = dict(estado)
        lista = navegacao.lista_foco(modelo)
        if not lista:
            novo["foco_console"] = None
            novo["cursores"] = {}
            return novo

        ids_lista = {c.id: i for i, c in enumerate(lista)}
        if (
            self._id_console_foco_suspenso is not None
            and self._id_console_foco_suspenso in ids_lista
        ):
            novo["foco_console"] = ids_lista[self._id_console_foco_suspenso]
        elif isinstance(foco_ant, int) and 0 <= foco_ant < len(lista):
            novo["foco_console"] = foco_ant
        else:
            novo["foco_console"] = 0

        ids_por_console = self._ids_cursor_suspensos or {}
        cursores = {}
        for cons in lista:
            itens = navegacao.itens_navegaveis(cons)
            ids = [
                it.get("id") for it in itens
                if isinstance(it, dict) and it.get("id") is not None
            ]
            id_ant = ids_por_console.get(cons.id)
            if id_ant is None and cursores_ant and cons.id in cursores_ant:
                idx_ant = cursores_ant[cons.id]
                if isinstance(idx_ant, int) and 0 <= idx_ant < len(itens):
                    item = itens[idx_ant]
                    if isinstance(item, dict):
                        id_ant = item.get("id")
            if id_ant is not None and id_ant in ids:
                cursores[cons.id] = ids.index(id_ant)
            else:
                cursores[cons.id] = 0
        novo["cursores"] = cursores
        return novo

    def _limpar_refs_proprias(self, *, preservar_origem):
        self.modelo_resultado = None
        self.transicao_em_andamento = False
        self._filtro_suspenso = None
        self._pagina_suspensa = None
        self._foco_suspenso = None
        self._cursores_suspensos = None
        self._ids_cursor_suspensos = None
        self._id_console_foco_suspenso = None
        self._selecoes_suspensas = None
        self._estado_runtime = None
        if not preservar_origem:
            self.origem_suspensa = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _console_focado(self, estado, modelo=None):
        if modelo is None:
            modelo = self.origem_ativa or self.origem_suspensa
        if modelo is None:
            return None
        nav = dict(estado)
        nav["modelo"] = modelo
        return navegacao.console_focado(nav)


def e_tecla_insert(comando):
    """True quando ``comando`` e a sequencia fisica Insert."""
    return comando == TECLA_INSERT


def recarregador_noop(modelo):
    """Recarregador observavel minimo (nao altera fixture baseline)."""
    return modelo
