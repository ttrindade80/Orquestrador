"""Controlador da tela normal de Estilo (H-0063..H-0067).

Projeta os quatro pais e filhos dinamicos a partir do candidato runtime
(H-0061) sobre um Console normal com politica ``dois_niveis_por_foco``.

H-0065: o candidato e a fonte semantica unica do preset escolhido;
``estado["selecoes"]`` e apenas projecao/cache navegacional reconciliada
a partir do candidato. ``Espaco`` atualiza o candidato de forma atomica
antes de projetar ``selecoes``.

H-0066: ``aplicar_disponivel`` deriva sempre de
``runtime.comparar_candidato_baseline()`` (nunca flag independente);
``solicitar_aplicacao`` entrega somente o snapshot imutavel
``SolicitacaoAplicacaoEstilo`` quando ativo.

H-0067: envelope ``conteudo_popup`` (tipo texto) derivado da solicitacao
ja recebida, para o popup generico de confirmacao.

H-0068: ``aplicar_solicitacao_confirmada`` orquestra a aplicacao
definitiva do snapshot confirmado via ``runtime.aplicar_candidato``.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from types import SimpleNamespace

from tela.carregamento.estilo import definir_preset_candidato
from tela.carregamento.erros import EstiloErro
from tela.modelo import ConteudoExterno, NivelConteudo, NoConteudo
from tela import navegacao
from tela.renderizacao.estilo import amostra_de_preset, compor_titulo_com_amostra
from tela.renderizacao.texto_ansi import _largura_sem_ansi


CATEGORIAS_ESTILO = (
    "borda",
    "chip",
    "indicadores.selecionado",
    "indicadores.incluido",
)

_CAMINHOS_CATEGORIAS = {
    "borda": ("borda",),
    "chip": ("chip",),
    "indicadores.selecionado": ("indicadores", "selecionado"),
    "indicadores.incluido": ("indicadores", "incluido"),
}

_CAMINHOS_PRESET_DEFAULT = {
    categoria: caminho + ("preset_default",)
    for categoria, caminho in _CAMINHOS_CATEGORIAS.items()
}

ID_TELA_ESTILO = "h0063_estilo_estrutura_navegacao_dois_niveis"
ID_CONSOLE_ESTILO = "console_h0063_estilo"
ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO = "popup_confirmacao_aplicacao_estilo"

_TEXTO_POPUP_CONFIRMACAO = (
    "Deseja aplicar o estilo selecionado? A alteracao ainda nao sera "
    "persistida nesta etapa."
)

_NIVEIS_FORMATO = (
    NivelConteudo(
        id="pai",
        tipo="container",
        conteudo="titulo",
        designador={"tipo": "decimal", "sufixo": "."},
    ),
    NivelConteudo(
        id="filho",
        tipo="conteudo",
        conteudo="titulo",
        designador={},
    ),
)


@dataclass(frozen=True)
class PresetEstilo:
    categoria: str
    nome: str
    dados: dict

    def __post_init__(self):
        object.__setattr__(self, "dados", copy.deepcopy(self.dados))


@dataclass(frozen=True)
class CategoriaEstilo:
    nome: str
    presets: tuple[PresetEstilo, ...]
    escolha: str


@dataclass(frozen=True)
class SolicitacaoAplicacaoEstilo:
    """Snapshot imutavel produzido ao acionar Aplicar ativo (H-0066).

    Copias independentes de candidato/baseline no instante do acionamento;
    mutacoes posteriores do runtime nao alteram esta instancia (contrato
    H-0066 secao 14). Nao representa persistencia, publicacao nem
    confirmacao -- somente a intencao estrutural entregue a etapa posterior.
    """

    baseline: dict
    candidato: dict

    def __post_init__(self):
        object.__setattr__(self, "baseline", copy.deepcopy(self.baseline))
        object.__setattr__(self, "candidato", copy.deepcopy(self.candidato))


def _em_caminho(documento, caminho):
    atual = documento
    for parte in caminho:
        atual = atual[parte]
    return atual


def _id_pai(categoria):
    return "estilo.{0}".format(categoria)


def _id_filho(categoria, nome_preset):
    return "estilo.{0}.{1}".format(categoria, nome_preset)


class ControladorTelaEstilo:
    """Projecao navegacional vinculada ao candidato runtime (H-0065)."""

    def __init__(self, runtime_estilo):
        self.runtime = runtime_estilo
        # Cada visita forma candidato novo a partir da baseline vigente.
        self.runtime.criar_candidato()
        self._catalogo = self.runtime.candidato
        self._nos_por_id = {}
        self._conteudo = self._construir_conteudo()
        if not navegacao.estrutura_dois_niveis_valida(
            SimpleNamespace(conteudo_externo=self._conteudo)
        ):
            raise ValueError("Projecao dinamica de estilo invalida")

    def _construir_conteudo(self):
        pais = []
        categorias = []
        for categoria in CATEGORIAS_ESTILO:
            secao = _em_caminho(self._catalogo, _CAMINHOS_CATEGORIAS[categoria])
            presets = []
            filhos = []
            largura_nome = max(
                (_largura_sem_ansi(nome) for nome in secao["presets"]),
                default=0,
            )
            for nome, dados in secao["presets"].items():
                preset = PresetEstilo(categoria, nome, dados)
                presets.append(preset)
                no_filho = NoConteudo(
                    id=_id_filho(categoria, nome),
                    nivel="filho",
                    campos={
                        "navegavel": True,
                        "selecionavel": True,
                        "titulo": compor_titulo_com_amostra(
                            nome, categoria, preset.dados,
                            largura_nome=largura_nome,
                        ),
                        "categoria": categoria,
                        "preset": nome,
                        "amostra": amostra_de_preset(categoria, preset.dados),
                    },
                    filhos=[],
                )
                filhos.append(no_filho)
                self._nos_por_id[no_filho.id] = no_filho
            no_pai = NoConteudo(
                id=_id_pai(categoria),
                nivel="pai",
                campos={
                    "navegavel": True,
                    "selecionavel": False,
                    "titulo": categoria,
                    "categoria": categoria,
                },
                filhos=filhos,
            )
            self._nos_por_id[no_pai.id] = no_pai
            pais.append(no_pai)
            categorias.append(
                CategoriaEstilo(
                    categoria,
                    tuple(presets),
                    secao["preset_default"],
                )
            )
        self._categorias = tuple(categorias)
        self._ids_escolha_inicial = tuple(
            _id_filho(categoria.nome, categoria.escolha)
            for categoria in self._categorias
        )
        formato = {
            "apresentacao": "hierarquia",
            "niveis": [
                {
                    "id": nivel.id,
                    "tipo": nivel.tipo,
                    "conteudo": nivel.conteudo,
                    "designador": dict(nivel.designador),
                }
                for nivel in _NIVEIS_FORMATO
            ],
        }
        return ConteudoExterno(
            tipo="multinivel",
            apresentacao="hierarquia",
            niveis=list(_NIVEIS_FORMATO),
            nos=pais,
            formato=formato,
            _raw={
                "id": "h0063_estilo_projecao",
                "schema": "conteudo.v1",
                "tipo": "multinivel",
                "apresentacao": "hierarquia",
                "formato": formato,
                "dados": [],
            },
        )

    @property
    def conteudo(self):
        return self._conteudo

    @property
    def categorias(self):
        return self._categorias

    @property
    def pais(self):
        return self._categorias

    @property
    def filhos(self):
        return {
            categoria.nome: categoria.presets for categoria in self._categorias
        }

    @property
    def escolhas_iniciais(self):
        return {
            categoria.nome: categoria.escolha
            for categoria in self._categorias
        }

    @property
    def ids_escolha_inicial(self):
        return list(self._ids_escolha_inicial)

    @property
    def baseline(self):
        return self.runtime.baseline

    @property
    def candidato(self):
        return self.runtime.candidato

    @property
    def estilo_global(self):
        return self.runtime.global_vigente

    @property
    def aplicar_disponivel(self):
        """Elegibilidade de Aplicar, derivada de candidato x baseline (H-0066).

        Ponte literal obrigatoria (nao inverter):
        ``not runtime.comparar_candidato_baseline()``. Recalculada a cada
        consulta -- nunca cache/flag independente capaz de sobreviver a
        A→B→A sem recalculo.
        """
        return not self.runtime.comparar_candidato_baseline()

    def solicitar_aplicacao(self):
        """Produz a solicitacao estrutural imutavel de Aplicar (H-0066).

        Somente quando ``aplicar_disponivel`` e True; caso contrario, no-op
        (retorna ``None``, sem efeito). Nao altera baseline, candidato,
        global nem arquivo; nao persiste, nao publica, nao abre popup. O
        candidato permanece o estado de edicao da visita corrente.
        """
        if not self.aplicar_disponivel:
            return None
        return SolicitacaoAplicacaoEstilo(
            baseline=self.runtime.baseline,
            candidato=self.runtime.candidato,
        )

    def aplicar_solicitacao_confirmada(self, solicitacao, estado, modelo=None):
        """Aplica o snapshot confirmado via ``aplicar_candidato`` (H-0068).

        Consome exclusivamente ``solicitacao.candidato``. Em sucesso,
        reconcilia ``estado["selecoes"]`` e devolve a materializacao.
        Propaga ``EstiloErro``. Nao relê ``runtime.candidato``. Nao
        remove a solicitacao do estado (responsabilidade do chamador).
        """
        if not isinstance(solicitacao, SolicitacaoAplicacaoEstilo):
            return dict(estado), None
        materializacao = self.runtime.aplicar_candidato(
            solicitacao.candidato,
            self.runtime.caminho_destino,
        )
        if modelo is None:
            return dict(estado), materializacao
        reconciliado = self.reconciliar_selecoes_com_candidato(
            dict(estado), modelo
        )
        return reconciliado, materializacao

    @staticmethod
    def conteudo_popup_confirmacao(solicitacao):
        """Envelope ``tipo: texto`` derivado da solicitacao ja recebida (H-0067).

        Nao reconsulta ``runtime.candidato``. Nao altera candidato, baseline,
        global nem arquivo. O texto e generico (margem da ADR); o vinculo
        estrutural com o snapshot e a propria ``SolicitacaoAplicacaoEstilo``
        retida pelo chamador, nao a serializacao dos presets no texto.
        """
        if not isinstance(solicitacao, SolicitacaoAplicacaoEstilo):
            raise TypeError(
                "conteudo_popup_confirmacao exige SolicitacaoAplicacaoEstilo"
            )
        return {
            "tipo": "texto",
            "texto": _TEXTO_POPUP_CONFIRMACAO,
        }

    def console_do_modelo(self, modelo):
        for elemento in modelo.corpo.elementos:
            if getattr(elemento, "tipo", None) == "console":
                return elemento
        return None

    def aplicar_ao_modelo(self, modelo):
        """Associa a projecao em memoria ao Console da tela normal."""
        modelo.conteudo_externo = self._conteudo
        console = self.console_do_modelo(modelo)
        if console is not None:
            console.conteudo_externo = self._conteudo
        return modelo

    def presets_do_candidato(self):
        """Le os quatro ``preset_default`` vigentes no candidato."""
        candidato = self.runtime.candidato
        resultado = {}
        for categoria in CATEGORIAS_ESTILO:
            secao = _em_caminho(candidato, _CAMINHOS_CATEGORIAS[categoria])
            resultado[categoria] = secao["preset_default"]
        return resultado

    def ids_escolha_do_candidato(self):
        """IDs de filho que projetam o candidato nas quatro categorias."""
        presets = self.presets_do_candidato()
        ids = []
        for categoria in CATEGORIAS_ESTILO:
            id_filho = _id_filho(categoria, presets[categoria])
            if id_filho not in self._nos_por_id:
                raise EstiloErro(
                    "Projecao inconsistente: preset {0!r} de {1} ausente "
                    "na estrutura navegacional".format(
                        presets[categoria], categoria
                    )
                )
            ids.append(id_filho)
        return ids

    def reconciliar_selecoes_com_candidato(self, estado, modelo):
        """Projeta ``estado["selecoes"]`` a partir do candidato (fonte unica).

        Nao altera candidato, baseline, global nem arquivo.
        """
        console = self.console_do_modelo(modelo)
        if console is None:
            return dict(estado)
        novo = dict(estado)
        selecoes = dict(estado.get("selecoes", {}) or {})
        selecoes[console.id] = self.ids_escolha_do_candidato()
        novo["selecoes"] = selecoes
        return novo

    def invariavel_candidato_selecoes(self, estado, modelo):
        """True se ``selecoes`` projeta exatamente o candidato corrente."""
        console = self.console_do_modelo(modelo)
        if console is None:
            return True
        atuais = list((estado.get("selecoes", {}) or {}).get(console.id, ()))
        return atuais == self.ids_escolha_do_candidato()

    def inicializar_estado(self, estado, modelo):
        """Define foco, cursor e escolhas iniciais projetadas do candidato."""
        console = self.console_do_modelo(modelo)
        if console is None:
            return dict(estado)
        novo = dict(estado)
        cursores = dict(estado.get("cursores", {}) or {})
        cursores[console.id] = 0
        novo["foco_console"] = 0
        novo["cursores"] = cursores
        return self.reconciliar_selecoes_com_candidato(novo, modelo)

    def escolhas_de(self, estado, modelo):
        """Mapeia a escolha exclusiva vigente (filho escolhido) por pai."""
        console = self.console_do_modelo(modelo)
        if console is None:
            return {}
        ids = list((estado.get("selecoes", {}) or {}).get(console.id, ()))
        resultado = {}
        for id_filho in ids:
            no = self._nos_por_id.get(id_filho)
            if no is None:
                continue
            categoria = no.campos.get("categoria")
            preset = no.campos.get("preset")
            if categoria and preset:
                resultado[categoria] = preset
        return {
            categoria: resultado[categoria]
            for categoria in CATEGORIAS_ESTILO
            if categoria in resultado
        }

    def filho_corrente(self, estado, modelo):
        """Retorna o no sob cursor quando o nivel ativo e o dos filhos."""
        console = self.console_do_modelo(modelo)
        if console is None or not navegacao.em_nivel_filhos(estado, console):
            return None
        item = navegacao.item_selecionado(console, dict(estado, modelo=modelo))
        if not isinstance(item, dict):
            return None
        return item.get("_no_multinivel")

    def pai_corrente(self, estado, modelo):
        """Retorna a categoria do pai sob cursor (ou do pai do filho corrente)."""
        console = self.console_do_modelo(modelo)
        if console is None:
            return CATEGORIAS_ESTILO[0]
        item = navegacao.item_selecionado(console, dict(estado, modelo=modelo))
        if isinstance(item, dict):
            no = item.get("_no_multinivel")
            if no is not None:
                return no.campos.get("categoria", CATEGORIAS_ESTILO[0])
        return CATEGORIAS_ESTILO[0]

    def aplicar_espaco_filho(self, estado, modelo):
        """Protocolo atomico Espaco: candidato aceito → projecao selecoes.

        Fase A: identifica pai/preset; nao altera selecoes ainda.
        Fase B: muta copia via H-0061 e materializa localmente.
        Fase C: falha → candidato anterior intacto; reconcilia selecoes.
        Fase D: sucesso → candidato aceito; reconcilia selecoes.
        """
        console = self.console_do_modelo(modelo)
        if console is None or not navegacao.em_nivel_filhos(estado, console):
            return dict(estado)

        filho = self.filho_corrente(estado, modelo)
        if filho is None:
            return dict(estado)

        categoria = filho.campos.get("categoria")
        preset = filho.campos.get("preset")
        if not categoria or not preset or categoria not in _CAMINHOS_PRESET_DEFAULT:
            return dict(estado)

        # Fase A — preservar candidato anterior; nao tocar selecoes.
        candidato_anterior = self.runtime.candidato
        caminho = _CAMINHOS_PRESET_DEFAULT[categoria]

        try:
            # Fase B — proposta sobre copia independente.
            proposta = copy.deepcopy(candidato_anterior)
            definir_preset_candidato(proposta, caminho, preset)
            self.runtime.materializar_local(proposta)
        except EstiloErro:
            # Fase C — falha: candidato runtime intacto; reconcilia selecoes.
            return self.reconciliar_selecoes_com_candidato(dict(estado), modelo)

        # Fase D — sucesso: reconcilia selecoes do candidato aceito.
        novo = self.reconciliar_selecoes_com_candidato(dict(estado), modelo)
        if not self.invariavel_candidato_selecoes(novo, modelo):
            return self.reconciliar_selecoes_com_candidato(dict(estado), modelo)
        return novo

    def aplicar_espaco_filho_invalido(self, estado, modelo, categoria, preset):
        """Mesmo protocolo atomico forçando preset (util em testes de falha)."""
        if categoria not in _CAMINHOS_PRESET_DEFAULT:
            raise EstiloErro("Categoria nao editavel: {0!r}".format(categoria))
        candidato_anterior = self.runtime.candidato
        caminho = _CAMINHOS_PRESET_DEFAULT[categoria]
        try:
            proposta = copy.deepcopy(candidato_anterior)
            definir_preset_candidato(proposta, caminho, preset)
            self.runtime.materializar_local(proposta)
        except EstiloErro:
            return self.reconciliar_selecoes_com_candidato(dict(estado), modelo)
        return self.reconciliar_selecoes_com_candidato(dict(estado), modelo)

    def descartar_visita(self, estado, modelo=None):
        """Saida efetiva: recria candidato da baseline e reconcilia selecoes.

        Sequencia: criar_candidato → reconciliar → verificar invariavel.
        Nao altera baseline, global nem arquivo.
        """
        self.runtime.criar_candidato()
        novo = dict(estado)
        if modelo is not None and self.console_do_modelo(modelo) is not None:
            novo = self.reconciliar_selecoes_com_candidato(novo, modelo)
            if not self.invariavel_candidato_selecoes(novo, modelo):
                raise EstiloErro(
                    "Invariavel candidato/selecoes violada na saida efetiva"
                )
        else:
            # Sem modelo observavel: limpa cache do console de estilo se existir.
            selecoes = dict(novo.get("selecoes", {}) or {})
            if ID_CONSOLE_ESTILO in selecoes:
                selecoes[ID_CONSOLE_ESTILO] = self.ids_escolha_do_candidato()
                novo["selecoes"] = selecoes
        return novo


__all__ = [
    "CATEGORIAS_ESTILO",
    "CategoriaEstilo",
    "ControladorTelaEstilo",
    "ID_CONSOLE_ESTILO",
    "ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO",
    "ID_TELA_ESTILO",
    "PresetEstilo",
    "SolicitacaoAplicacaoEstilo",
]
\n