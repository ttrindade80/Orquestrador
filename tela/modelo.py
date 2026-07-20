"""Modelo interno normalizado de tela (H-0002).

Camada estruturada sobre o dict retornado pelo loader H-0001
(`carregar_tela`). Converte o dict plano em dataclasses acessiveis por
nome, preservando o JSON original em `_raw` e os campos adicionais de cada
elemento do corpo em `_campos_inertes`.

ESCOPO (H-0002):
- Apenas construcao inerte a partir de dict ja validado pelo loader.
- Nao revalida a estrutura macro (responsabilidade do H-0001).
- Nao executa, nao resolve nem atribui semantica nova a chips, bindings,
  filtros, referencias_de_acoes, tela_destino, origem_dados,
  regra_geracao_itens, itens vazios de lancador, etc.
- Nao cria subclasses por tipo, nao cria registry, nao cria estado de
  runtime (cursor, pagina, filtro ativo, selecao, foco).
- Nao altera o JSON em runtime.

Apenas biblioteca padrao do Python.
"""

from dataclasses import dataclass, field

from tela.loader import TIPOS_CORPO_VALIDOS, TIPOS_ESTRUTURAIS_VALIDOS


# Conjunto aceito pelo construtor de modelo: tipos funcionais fechados
# (console, lancador, dashboard) mais tipos estruturais de composicao
# (grupo - H-0012/ADR-0010). Grupo e container estrutural, nao elemento
# funcional.
_TIPOS_VALIDOS_MODELO = TIPOS_CORPO_VALIDOS | TIPOS_ESTRUTURAIS_VALIDOS


class ModeloTelaErro(Exception):
    """Erro de construcao do modelo interno de tela."""


@dataclass
class ElementoCorpo:
    """Elemento do corpo com `id` e `tipo` acessiveis; demais campos inertes.

    Os campos adicionais do elemento (titulo, origem_dados, itens, etc.)
    sao preservados em `_campos_inertes` como declaracao inerte, sem
    execucao, sem resolucao e sem semantica nova.

    Para o tipo estrutural `grupo` (H-0012), `elementos` carrega os
    ElementoCorpo dos elementos funcionais internos do grupo. Para tipos
    funcionais diretos (console/lancador/dashboard) `elementos` permanece
    vazio -- eles nao sao containers.
    """

    id: str
    tipo: str
    _campos_inertes: dict = field(default_factory=dict, repr=False)
    elementos: list = field(default_factory=list, repr=False)
    parametros_tipo: dict | None = field(default=None, repr=False)
    # H-0035 / ADR-0025: configuracao de distribuicao matricial de nivel unico,
    # declarada explicitamente por elementos funcionais (dashboard/console/
    # lancador). None quando ausente (preserva comportamento anterior). O
    # loader ja validou os 26 caminhos antes de chegar aqui; o modelo apenas
    # transporta o dict fiel, sem defaults estruturais e sem logica geometrica.
    distribuicao_matricial: dict | None = field(default=None, repr=False)
    # H-0036 / ADR-0026 / ADR-0027: conteudo externo multinivel associado ao
    # elemento console. None quando o cenario nao possui documento externo
    # (preserva o placeholder). A origem e SEPARADA do JSON estrutural: este
    # campo transporta um ConteudoExterno tipado, nunca reinserido em _raw nem
    # em _campos_inertes. O modelo nao abre arquivos e nao escolhe a fonte (o
    # demo.py carrega e associa; o loader valida).
    conteudo_externo: object = field(default=None, repr=False)
    # H-0037 / ADR-0028 D23: politica de modo de verbosidade do elemento
    # console, extraida de formato.excesso.politica_modo. None preserva o
    # comportamento legado (sem politica declarada). O loader ja validou a
    # combinacao valida antes de chegar aqui; o modelo apenas transporta.
    politica_modo: str | None = field(default=None, repr=False)
    # modo_inicial: valor inicial de verbosidade para politica 'alternavel',
    # extraido de formato.excesso.modo_inicial. None para politicas fixas.
    modo_inicial: str | None = field(default=None, repr=False)


@dataclass
class Corpo:
    """Corpo da tela: arranjo declarativo e lista de elementos.

    ``distribuicao`` (H-0025 / ADR-0018) e OPCIONAL: ``None`` significa
    ausencia declarada, que preserva a construcao orientada pelo conteudo
    (cada filho usa sua dimensao natural). Quando declarado, transporta o
    dict validado ``{"modo": ..., "valores": ...}`` sem conversao implicita
    de valores e sem materializar ``igual`` na ausencia.
    """

    arranjo: str | None
    elementos: list  # lista de ElementoCorpo
    distribuicao: dict | None = None


@dataclass
class ModeloTela:
    """Modelo interno normalizado da tela.

    Campos estruturais minimos acessiveis por nome. O JSON original
    completo fica preservado em `_raw` para auditoria. Demais campos
    top-level do JSON (bindings, referencias_de_acoes, filtros, metadados)
    sao acessiveis via `_raw`, como declaracao inerte.
    """

    id: str
    schema: str
    cabecalho: dict
    corpo: Corpo
    barra_de_menus: dict
    _raw: dict = field(repr=False)
    # H-0036: conteudo externo multinivel do cenario (origem separada). None
    # quando o cenario nao possui documento externo. Acessivel diretamente para
    # inspecao/teste; tambem propagado aos ElementoCorpo do tipo console.
    conteudo_externo: object = field(default=None, repr=False)

    def elemento_por_id(self, id_elemento):
        """Retorna o primeiro ElementoCorpo com o id informado, ou None.

        Escopo plano: percorre somente ``self.corpo.elementos`` diretos, sem
        descer na arvore de grupos (H-0027 — limitacao documentada, nao bug).
        Elementos dentro de grupos sao acessiveis via navegacao direta da
        arvore (``elemento.elementos``), nao por este metodo.
        Somente leitura. Nao ativa bindings, nao executa acoes.
        """
        for elemento in self.corpo.elementos:
            if elemento.id == id_elemento:
                return elemento
        return None

    def elementos_por_tipo(self, tipo):
        """Retorna lista de ElementoCorpo cujo ``tipo`` coincide.

        Escopo plano: percorre somente ``self.corpo.elementos`` diretos, sem
        descer na arvore de grupos (H-0027 — limitacao documentada, nao bug).
        Elementos dentro de grupos sao acessiveis via navegacao direta da
        arvore (``elemento.elementos``), nao por este metodo.
        Somente leitura. Nao cria registry de tipos nem subclasses.
        """
        return [e for e in self.corpo.elementos if e.tipo == tipo]

    def diagnostico(self) -> str:
        """Representacao textual auditavel do modelo.

        Contem ao menos: `id`, `schema`, `corpo.arranjo` e a lista de
        elementos com `id` e `tipo` de cada um.
        """
        linhas = []
        linhas.append("id: {0}".format(self.id))
        linhas.append("schema: {0}".format(self.schema))
        linhas.append("corpo.arranjo: {0}".format(self.corpo.arranjo))
        for elemento in self.corpo.elementos:
            linhas.append(
                "  elemento: id={0!r} tipo={1!r}".format(
                    elemento.id, elemento.tipo
                )
            )
        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# H-0036 / ADR-0026 / ADR-0027: representacao semantica do conteudo externo
# multinivel. O modelo recebe o documento ja carregado e validado pelo loader
# (origem separada do JSON estrutural), constroi a representacao tipada e
# preserva ordem, niveis, pais e filhos. NAO abre arquivos, NAO escolhe fonte,
# NAO calcula geometria e NAO infere hierarquia (declarada por ``filhos``).
# ---------------------------------------------------------------------------


@dataclass
class NivelConteudo:
    """Declaracao de um nivel do documento externo (formato.niveis[]).

    ``conteudo`` e o nome do campo textual (container/conteudo) ou o objeto
    ``{"nome": ..., "valor": ...}`` (nome_valor). ``designador`` transporta a
    politica declarativa; a sequencia concreta e calculada pelo renderizador.
    """

    id: str
    tipo: str
    conteudo: object
    designador: dict
    _campos_inertes: dict = field(default_factory=dict, repr=False)


@dataclass
class NoConteudo:
    """No de conteudo (item de ``dados`` ou de ``filhos``).

    ``campos`` preserva todos os campos semanticos do no (titulo, nome, valor,
    etc.) sem execucao. ``filhos`` preserva a hierarquia declarada, na ordem
    original; o modelo nunca reordena nem infere pais.
    """

    id: str
    nivel: str
    campos: dict = field(default_factory=dict, repr=False)
    filhos: list = field(default_factory=list, repr=False)


@dataclass
class ConteudoExterno:
    """Representacao semantica tipada do documento externo multinivel.

    Transporta ``apresentacao``, os niveis declarados, os nos de topo (``nos``)
    com filhos recursivos e o bloco ``formato`` (para blocos especificos de
    apresentacao). ``_raw`` preserva o documento validado para auditoria. A
    origem e SEPARADA do JSON estrutural da tela.
    """

    tipo: str
    apresentacao: str
    niveis: list  # lista de NivelConteudo
    nos: list     # lista de NoConteudo (nos de topo, ordem de dados[])
    formato: dict = field(default_factory=dict, repr=False)
    _raw: dict = field(default_factory=dict, repr=False)

    def nivel_por_id(self, id_nivel):
        """Retorna o NivelConteudo com o id informado, ou None."""
        for nivel in self.niveis:
            if nivel.id == id_nivel:
                return nivel
        return None


def _construir_no_conteudo(no_raw):
    """Constroi recursivamente um NoConteudo a partir do dict validado."""
    if not isinstance(no_raw, dict):
        raise ModeloTelaErro("no de conteudo externo nao e dict")
    campos = {
        chave: valor
        for chave, valor in no_raw.items()
        if chave not in ("id", "nivel", "filhos")
    }
    filhos_raw = no_raw.get("filhos", []) or []
    filhos = [_construir_no_conteudo(f) for f in filhos_raw]
    return NoConteudo(
        id=no_raw.get("id"),
        nivel=no_raw.get("nivel"),
        campos=campos,
        filhos=filhos,
    )


def construir_conteudo_externo(conteudo_raw):
    """Constroi ConteudoExterno a partir do documento validado pelo loader.

    ``conteudo_raw`` e o dict devolvido por ``carregar_conteudo_externo`` (ja
    validado). None produz None (cenario sem conteudo externo). O modelo apenas
    tipa e transporta; nao revalida geometria, nao abre arquivos, nao escolhe
    fonte e nao reconstroi hierarquia (usa ``filhos`` como declarado).
    """
    if conteudo_raw is None:
        return None
    if not isinstance(conteudo_raw, dict):
        raise ModeloTelaErro(
            "conteudo externo nao e dict: {0}".format(type(conteudo_raw).__name__)
        )
    formato = conteudo_raw.get("formato", {}) or {}
    niveis = []
    for nivel_raw in formato.get("niveis", []) or []:
        inertes = {
            chave: valor
            for chave, valor in nivel_raw.items()
            if chave not in ("id", "tipo", "conteudo", "designador")
        }
        niveis.append(
            NivelConteudo(
                id=nivel_raw.get("id"),
                tipo=nivel_raw.get("tipo"),
                conteudo=nivel_raw.get("conteudo"),
                designador=nivel_raw.get("designador"),
                _campos_inertes=inertes,
            )
        )
    nos = [_construir_no_conteudo(no) for no in conteudo_raw.get("dados", []) or []]
    return ConteudoExterno(
        tipo=conteudo_raw.get("tipo"),
        apresentacao=formato.get("apresentacao"),
        niveis=niveis,
        nos=nos,
        formato=formato,
        _raw=conteudo_raw,
    )


def _propagar_conteudo_externo(elementos, conteudo):
    """Associa ``conteudo`` a cada ElementoCorpo do tipo console (recursivo).

    A associacao pertence ao ponto de entrada/modelo, nunca ao JSON estrutural.
    Percorre grupos para alcancar consoles internos. Ausencia de console nao e
    erro (o conteudo permanece acessivel em ModeloTela.conteudo_externo).
    """
    for elemento in elementos:
        if elemento.tipo == "console":
            elemento.conteudo_externo = conteudo
        elif elemento.tipo == "grupo":
            _propagar_conteudo_externo(elemento.elementos, conteudo)


def _construir_elementos_recursivo(elementos_raw, id_pai, parametros_lancador=None):
    """Constroi recursivamente a lista de ElementoCorpo a partir de uma lista raw.

    Tipos funcionais (console/lancador/dashboard) produzem ElementoCorpo com
    elementos=[]. Tipo 'grupo' produz ElementoCorpo com tipo='grupo' e
    elementos preenchido recursivamente (ADR-0019 D2/D3 — ate 3 niveis).
    O loader (ADR-0019 / H-0027) ja garantiu a validade estrutural antes de
    chegar aqui.

    parametros_lancador: dict validado de config/elementos/lancador.json
        (subset de 'layout'), propagado para cada ElementoCorpo do tipo
        'lancador' como parametros_tipo (H-0034). None para telas sem lancador.
    """
    resultado = []
    for sub_indice, sub_el in enumerate(elementos_raw):
        if not isinstance(sub_el, dict):
            raise ModeloTelaErro(
                "Elemento interno na posicao {0} de '{1}' nao e um "
                "dict".format(sub_indice, id_pai)
            )
        if "id" not in sub_el:
            raise ModeloTelaErro(
                "Elemento interno na posicao {0} de '{1}' sem campo "
                "'id'".format(sub_indice, id_pai)
            )
        if "tipo" not in sub_el:
            raise ModeloTelaErro(
                "Elemento interno '{0}' de '{1}' sem campo "
                "'tipo'".format(sub_el.get("id"), id_pai)
            )
        sub_tipo = sub_el["tipo"]
        sub_id = sub_el["id"]

        if sub_tipo == "grupo":
            sub_raw = sub_el.get("elementos", [])
            if not isinstance(sub_raw, list):
                sub_raw = []
            sub_elementos = _construir_elementos_recursivo(
                sub_raw, sub_id, parametros_lancador
            )
            inertes = {
                chave: valor
                for chave, valor in sub_el.items()
                if chave not in ("id", "tipo", "elementos")
            }
            resultado.append(
                ElementoCorpo(
                    id=sub_id,
                    tipo="grupo",
                    _campos_inertes=inertes,
                    elementos=sub_elementos,
                )
            )
        elif sub_tipo in TIPOS_CORPO_VALIDOS:
            inertes = {
                chave: valor
                for chave, valor in sub_el.items()
                if chave not in ("id", "tipo", "distribuicao_matricial")
            }
            params = parametros_lancador if sub_tipo == "lancador" else None
            dm = sub_el.get("distribuicao_matricial")
            excesso = sub_el.get("formato", {}).get("excesso", {})
            pm = excesso.get("politica_modo") if sub_tipo == "console" else None
            mi = excesso.get("modo_inicial") if sub_tipo == "console" else None
            resultado.append(
                ElementoCorpo(
                    id=sub_id,
                    tipo=sub_tipo,
                    _campos_inertes=inertes,
                    parametros_tipo=params,
                    distribuicao_matricial=dm,
                    politica_modo=pm,
                    modo_inicial=mi,
                )
            )
        else:
            raise ModeloTelaErro(
                "Tipo desconhecido '{0}' em elemento '{1}' de '{2}'".format(
                    sub_tipo, sub_id, id_pai
                )
            )
    return resultado


def construir_modelo(tela_raw: dict, conteudo_externo=None) -> ModeloTela:
    """Constroi ModeloTela a partir do dict retornado por carregar_tela.

    Nao valida novamente a estrutura macro -- essa responsabilidade
    pertence ao loader (H-0001). Constroi a estrutura tipada a partir dos
    campos ja validados.

    Parametros:
        tela_raw: dict retornado por carregar_tela(caminho_base, id_tela).
        conteudo_externo: documento externo de conteudo ja carregado e
            validado pelo loader (dict devolvido por
            ``carregar_conteudo_externo``) OU um ConteudoExterno ja tipado.
            None (default) preserva o comportamento historico (cenario sem
            conteudo externo; console mantem o placeholder). Estrutura e
            conteudo sao entradas SEPARADAS; a origem e preservada. O modelo
            nao abre arquivos e nao escolhe a fonte (H-0036 / ADR-0027).

    Retorna:
        ModeloTela com campos acessiveis por nome. Quando ha conteudo externo,
        ``ModeloTela.conteudo_externo`` transporta o ConteudoExterno tipado e
        cada ElementoCorpo do tipo console recebe a mesma referencia.

    Lanca:
        ModeloTelaErro se o dict de entrada nao tiver o formato minimo
        esperado (ausencia de chave que o loader deveria ter produzido).
    """
    if not isinstance(tela_raw, dict):
        raise ModeloTelaErro(
            "Entrada de construir_modelo nao e um dict"
        )

    for chave in ("id", "schema", "cabecalho", "corpo",
                  "barra_de_menus", "_raw"):
        if chave not in tela_raw:
            raise ModeloTelaErro(
                "Campo esperado ausente no dict do loader: {0!r}".format(chave)
            )

    # H-0034: parametros normativos do tipo lancador, carregados pelo loader
    # de config/elementos/lancador.json. None quando nao ha lancador na tela.
    parametros_lancador = tela_raw.get("_config_lancador")

    corpo_raw = tela_raw["corpo"]
    if not isinstance(corpo_raw, dict):
        raise ModeloTelaErro("'corpo' nao e um dict")

    if "elementos" not in corpo_raw:
        raise ModeloTelaErro(
            "Campo esperado ausente no dict do loader: 'corpo.elementos'"
        )

    elementos_raw = corpo_raw["elementos"]
    if not isinstance(elementos_raw, list):
        raise ModeloTelaErro("'corpo.elementos' nao e uma lista")

    elementos = []
    for indice, elemento in enumerate(elementos_raw):
        if not isinstance(elemento, dict):
            raise ModeloTelaErro(
                "Elemento na posicao {0} nao e um dict".format(indice)
            )
        if "id" not in elemento:
            raise ModeloTelaErro(
                "Elemento na posicao {0} sem campo 'id'".format(indice)
            )
        if "tipo" not in elemento:
            raise ModeloTelaErro(
                "Elemento na posicao {0} sem campo 'tipo'".format(indice)
            )
        tipo = elemento["tipo"]
        if tipo not in _TIPOS_VALIDOS_MODELO:
            raise ModeloTelaErro(
                "Tipo desconhecido '{0}' em elemento '{1}'".format(
                    tipo, elemento["id"]
                )
            )

        if tipo == "grupo":
            sub_raw = elemento.get("elementos", [])
            if not isinstance(sub_raw, list):
                sub_raw = []
            sub_elementos = _construir_elementos_recursivo(
                sub_raw, elemento["id"], parametros_lancador
            )
            inertes = {
                chave: valor
                for chave, valor in elemento.items()
                if chave not in ("id", "tipo", "elementos")
            }
            elementos.append(
                ElementoCorpo(
                    id=elemento["id"],
                    tipo=elemento["tipo"],
                    _campos_inertes=inertes,
                    elementos=sub_elementos,
                )
            )
        else:
            inertes = {
                chave: valor
                for chave, valor in elemento.items()
                if chave not in ("id", "tipo", "distribuicao_matricial")
            }
            params = parametros_lancador if tipo == "lancador" else None
            dm = elemento.get("distribuicao_matricial")
            excesso = elemento.get("formato", {}).get("excesso", {})
            pm = excesso.get("politica_modo") if tipo == "console" else None
            mi = excesso.get("modo_inicial") if tipo == "console" else None
            elementos.append(
                ElementoCorpo(
                    id=elemento["id"],
                    tipo=elemento["tipo"],
                    _campos_inertes=inertes,
                    parametros_tipo=params,
                    distribuicao_matricial=dm,
                    politica_modo=pm,
                    modo_inicial=mi,
                )
            )

    corpo = Corpo(
        arranjo=corpo_raw.get("arranjo"),
        elementos=elementos,
        distribuicao=corpo_raw.get("distribuicao"),
    )

    # H-0036: tipa o conteudo externo (quando fornecido) e propaga aos consoles.
    # Aceita tanto o dict validado do loader quanto um ConteudoExterno ja tipado.
    if isinstance(conteudo_externo, ConteudoExterno) or conteudo_externo is None:
        conteudo = conteudo_externo
    else:
        conteudo = construir_conteudo_externo(conteudo_externo)
    if conteudo is not None:
        _propagar_conteudo_externo(elementos, conteudo)

    return ModeloTela(
        id=tela_raw["id"],
        schema=tela_raw["schema"],
        cabecalho=tela_raw["cabecalho"],
        corpo=corpo,
        barra_de_menus=tela_raw["barra_de_menus"],
        _raw=tela_raw["_raw"],
        conteudo_externo=conteudo,
    )
