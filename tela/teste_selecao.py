"""Testes unitarios de selecao multipla por conjunto de IDs (H-0041 / ADR-0034).

Cobre as decisoes D-SEL-01 a D-SEL-09 do Handoff 1 (ITEM-0006) por meio dos
criterios canonicos exigidos na secao 10 do H-0041. Cada teste valida a
superficie observavel do modulo ``tela.selecao``: estado por IDs, toggle,
``Todos``, limpeza, reconciliacao, ordenacao logica e independencia do cursor.

Os modelos de teste sao construidos localmente a partir de dicts simples (a API
de selecao aceita ``ElementoCorpo`` direto), sem acoplar ao loader nem a JSONs.
Apenas biblioteca padrao do Python.
"""

import pytest

from tela.modelo import ElementoCorpo
from tela import selecao


# ---------------------------------------------------------------------------
# Fixtures auxiliares
# ---------------------------------------------------------------------------


def _console_oito_itens(idc="console_selecao"):
    """Console de oito itens da fixture D-SEL-22 (seis navegaveis, dois nao).

    Selecionaveis (navegavel + selecionavel): item_01, item_03, item_05, item_07.
    Nao selecionaveis navegaveis: item_02, item_06.
    Nao navegaveis: item_04, item_08.
    """
    itens = [
        {"id": "item_01", "texto": "Item um", "navegavel": True, "selecionavel": True},
        {"id": "item_02", "texto": "Item dois", "navegavel": True, "selecionavel": False},
        {"id": "item_03", "texto": "Item tres", "navegavel": True, "selecionavel": True},
        {"id": "item_04", "texto": "Item quatro", "navegavel": False},
        {"id": "item_05", "texto": "Item cinco", "navegavel": True, "selecionavel": True},
        {"id": "item_06", "texto": "Item seis", "navegavel": True, "selecionavel": False},
        {"id": "item_07", "texto": "Item sete", "navegavel": True, "selecionavel": True},
        {"id": "item_08", "texto": "Item oito", "navegavel": False},
    ]
    return ElementoCorpo(
        id=idc,
        tipo="console",
        _campos_inertes={
            "titulo": "Itens",
            "itens": itens,
            "politica_navegacao": {"navegavel": True},
            "politica_selecao": "multipla",
        },
    )


def _estado(selecoes=None):
    """Estado minimo de runtime com selecoes por console."""
    return {"selecoes": selecoes or {}}


# ---------------------------------------------------------------------------
# CA-01: selecao como conjunto de IDs, sem duplicatas, independente do cursor
# ---------------------------------------------------------------------------


class TestEstadoSelecao:
    """CA-01: estado da selecao por IDs estaveis, independente do cursor."""

    def test_selecao_inicial_vazia(self):
        # D-SEL-01/D-SEL-22: selecao inicial sempre vazia.
        console = _console_oito_itens()
        assert selecao.selecao(console, _estado()) == []

    def test_selecao_por_ids_sem_duplicatas(self):
        # D-SEL-01: conjunto de IDs; duplicatas no armazenamento sao removidas.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01", "item_01", "item_03"]})
        assert selecao.selecao(console, estado) == ["item_01", "item_03"]

    def test_selecao_independente_do_cursor(self):
        # CA-01: o cursor (estado["cursores"]) nao afeta a selecao.
        console = _console_oito_itens()
        estado_com_cursor = {
            "selecoes": {console.id: ["item_01"]},
            "cursores": {console.id: 5},
        }
        assert selecao.selecao(console, estado_com_cursor) == ["item_01"]


# ---------------------------------------------------------------------------
# CA-02: Espaco alterna item selecionavel; sem efeito em nao selecionavel
# ---------------------------------------------------------------------------


class TestToggleEspaco:
    """CA-02: alternancia por Espaco."""

    def test_espaco_marca_item_selecionavel(self):
        # D-SEL-05: Espaco alterna inclusao de item selecionavel.
        console = _console_oito_itens()
        estado = _estado()
        novo = selecao.alternar(estado, console, "item_01")
        assert novo["selecoes"][console.id] == ["item_01"]

    def test_espaco_desmarca_item_ja_marcado(self):
        # D-SEL-05: segundo Espaco remove o item (toggle).
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01"]})
        novo = selecao.alternar(estado, console, "item_01")
        assert novo["selecoes"][console.id] == []

    def test_espaco_sem_efeito_em_nao_selecionavel(self):
        # D-SEL-05: item nao selecionavel ignora Espaco.
        console = _console_oito_itens()
        estado = _estado()
        novo = selecao.alternar(estado, console, "item_02")
        assert novo["selecoes"].get(console.id, []) == []

    def test_espaco_nao_move_cursor(self):
        # CA-02/CA-01: Espaco nao altera cursores (campo independente).
        console = _console_oito_itens()
        estado = {"selecoes": {}, "cursores": {console.id: 3}}
        novo = selecao.alternar(estado, console, "item_01")
        assert novo["cursores"] == {console.id: 3}

    def test_alternar_nao_muta_estado_recebido(self):
        # Pureza: nenhum dict recebido e mutado.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_03"]})
        selecao.alternar(estado, console, "item_01")
        assert estado["selecoes"][console.id] == ["item_03"]


# ---------------------------------------------------------------------------
# CA-03/CA-04: Todos e ordenacao logica
# ---------------------------------------------------------------------------


class TestTodosEOrdenacao:
    """CA-03/CA-04: Todos sobre selecionaveis; ordem logica do console."""

    def test_todos_produz_selecionaveis_na_ordem_logica(self):
        # CA-03: Enter=Todos produz exatamente item_01,03,05,07.
        console = _console_oito_itens()
        novo = selecao.selecionar_todos(_estado(), console)
        assert novo["selecoes"][console.id] == [
            "item_01", "item_03", "item_05", "item_07"
        ]

    def test_todos_sem_selecionaveis_produz_vazio(self):
        # D-SEL-06: com zero selecionaveis, Todos produz vazio.
        itens = [
            {"id": "a", "texto": "A", "navegavel": True, "selecionavel": False},
            {"id": "b", "texto": "B", "navegavel": True, "selecionavel": False},
        ]
        console = ElementoCorpo(
            id="c", tipo="console",
            _campos_inertes={"itens": itens, "politica_selecao": "multipla"},
        )
        novo = selecao.selecionar_todos(_estado(), console)
        assert novo["selecoes"][console.id] == []

    def test_ordenacao_segue_ordem_logica_nao_marcacao(self):
        # CA-04: a selecao segue a ordem do console, nao a ordem de marcacao.
        console = _console_oito_itens()
        # Marca na ordem inversa.
        estado = _estado({console.id: ["item_07", "item_03", "item_01"]})
        assert selecao.selecao(console, estado) == ["item_01", "item_03", "item_07"]

    def test_itens_nao_selecionaveis_excluidos_do_conjunto(self):
        # D-SEL-09/CA: itens nao selecionaveis nunca entram na selecao.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01", "item_02", "item_06"]})
        assert selecao.selecao(console, estado) == ["item_01"]


# ---------------------------------------------------------------------------
# CA-05: reconciliacao isolada
# ---------------------------------------------------------------------------


class TestReconciliacao:
    """CA-05: reconciliacao remove IDs inexistentes e nao selecionaveis."""

    def test_reconcilia_id_inexistente(self):
        # D-SEL-03: ID inexistente removido, ordem logica preservada.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01", "item_99", "item_03"]})
        novo = selecao.reconciliar(estado, console)
        assert novo["selecoes"][console.id] == ["item_01", "item_03"]

    def test_reconcilia_item_que_deixou_de_ser_selecionavel(self):
        # D-SEL-03: item que deixou de ser selecionavel removido.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01", "item_02"]})
        novo = selecao.reconciliar(estado, console)
        assert novo["selecoes"][console.id] == ["item_01"]

    def test_reconciliacao_isolada_sem_binding(self):
        # CA-05: funcao pura, testavel diretamente sem teclado.
        console = _console_oito_itens()
        novo = selecao.reconciliar(
            _estado({console.id: ["item_01", "fantasma"]}), console
        )
        assert novo["selecoes"][console.id] == ["item_01"]

    def test_reconciliacao_vazia_nao_marca(self):
        # D-SEL-04: reconciliacao vazia nao executa nem aplica Todos.
        console = _console_oito_itens()
        novo = selecao.reconciliar(_estado(), console)
        assert novo["selecoes"][console.id] == []


# ---------------------------------------------------------------------------
# CA-06: limpeza por Esc
# ---------------------------------------------------------------------------


class TestLimpezaEsc:
    """CA-06: Esc limpa selecao (o comportamento de permanecer e do chamador)."""

    def test_limpar_esvazia_selecao(self):
        # D-SEL-08: limpar remove todos os IDs marcados.
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01", "item_03"]})
        novo = selecao.limpar(estado, console)
        assert novo["selecoes"][console.id] == []

    def test_limpar_preserva_outros_consoles(self):
        # D-SEL-01: selecao e independente por console.
        c1 = _console_oito_itens("c1")
        c2 = _console_oito_itens("c2")
        estado = _estado({
            "c1": ["item_01"],
            "c2": ["item_03", "item_05"],
        })
        novo = selecao.limpar(estado, c1)
        assert novo["selecoes"]["c1"] == []
        assert novo["selecoes"]["c2"] == ["item_03", "item_05"]


# ---------------------------------------------------------------------------
# Rotulo dinamico e estado vazio
# ---------------------------------------------------------------------------


class TestRotuloEValores:
    """Rotulo Todos/Executar e deteccao de selecao vazia."""

    def test_rotulo_todos_quando_vazio(self):
        console = _console_oito_itens()
        assert selecao.rotulo_enter(_estado(), console) == "Todos"

    def test_rotulo_executar_quando_ha_selecao(self):
        # D-SEL-07: com selecao, rotulo e Executar (inativo no handoff).
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01"]})
        assert selecao.rotulo_enter(estado, console) == "Executar"

    def test_esta_vazia_true_quando_vazio(self):
        console = _console_oito_itens()
        assert selecao.esta_vazia(_estado(), console) is True

    def test_esta_vazia_false_quando_ha_selecao(self):
        console = _console_oito_itens()
        estado = _estado({console.id: ["item_01"]})
        assert selecao.esta_vazia(estado, console) is False


# ---------------------------------------------------------------------------
# chip Espaco ativo/inativo (CA-10)
# ---------------------------------------------------------------------------


class TestChipEspacoAtivo:
    """CA-10: chip Espaco ativo conforme selecionabilidade do item sob cursor."""

    def _stub_nav(self, item_id):
        """Stub do modulo navegacao com item_selecionado retornando um item."""

        class _Nav:
            def item_selecionado(self, console, estado):
                itens = console._campos_inertes.get("itens", [])
                for it in itens:
                    if it.get("id") == item_id:
                        return it
                return None

        return _Nav()

    def test_chip_ativo_item_selecionavel(self):
        console = _console_oito_itens()
        nav = self._stub_nav("item_01")
        assert selecao.chip_espaco_ativo(console, _estado(), nav) is True

    def test_chip_inativo_item_nao_selecionavel(self):
        console = _console_oito_itens()
        nav = self._stub_nav("item_02")
        assert selecao.chip_espaco_ativo(console, _estado(), nav) is False

    def test_chip_inativo_item_inexistente(self):
        console = _console_oito_itens()
        nav = self._stub_nav("item_99")
        assert selecao.chip_espaco_ativo(console, _estado(), nav) is False
