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

    def elemento_por_id(self, id_elemento):
        """Retorna o primeiro ElementoCorpo com o id informado, ou None.

        Somente leitura. Nao ativa bindings, nao executa acoes, nao
        resolve pendencias.
        """
        for elemento in self.corpo.elementos:
            if elemento.id == id_elemento:
                return elemento
        return None

    def elementos_por_tipo(self, tipo):
        """Retorna lista de ElementoCorpo cujo `tipo` coincide.

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


def _construir_elementos_internos_grupo(elemento_grupo, id_grupo):
    """Constroi a lista de ElementoCorpo dos elementos internos do grupo.

    Os elementos internos sao funcionais (console/lancador/dashboard) --
    o loader (H-0012) ja garantiu exatamente 1 item, nao-grupo e tipo
    funcional. Nao ha recursao: grupo dentro de grupo e rejeitado pelo
    loader antes de chegar aqui.
    """
    sub_raw = elemento_grupo.get("elementos", [])
    if not isinstance(sub_raw, list):
        return []
    sub_elementos = []
    for sub_indice, sub_el in enumerate(sub_raw):
        if not isinstance(sub_el, dict):
            raise ModeloTelaErro(
                "Elemento interno na posicao {0} do grupo '{1}' nao e um "
                "dict".format(sub_indice, id_grupo)
            )
        if "id" not in sub_el:
            raise ModeloTelaErro(
                "Elemento interno na posicao {0} do grupo '{1}' sem campo "
                "'id'".format(sub_indice, id_grupo)
            )
        if "tipo" not in sub_el:
            raise ModeloTelaErro(
                "Elemento interno '{0}' do grupo '{1}' sem campo "
                "'tipo'".format(sub_el.get("id"), id_grupo)
            )
        sub_tipo = sub_el["tipo"]
        if sub_tipo not in TIPOS_CORPO_VALIDOS:
            raise ModeloTelaErro(
                "Tipo interno desconhecido '{0}' em elemento '{1}' do grupo "
                "'{2}'".format(sub_tipo, sub_el["id"], id_grupo)
            )
        sub_inertes = {
            chave: valor
            for chave, valor in sub_el.items()
            if chave not in ("id", "tipo")
        }
        sub_elementos.append(
            ElementoCorpo(
                id=sub_el["id"],
                tipo=sub_el["tipo"],
                _campos_inertes=sub_inertes,
            )
        )
    return sub_elementos


def construir_modelo(tela_raw: dict) -> ModeloTela:
    """Constroi ModeloTela a partir do dict retornado por carregar_tela.

    Nao valida novamente a estrutura macro -- essa responsabilidade
    pertence ao loader (H-0001). Constroi a estrutura tipada a partir dos
    campos ja validados.

    Parametros:
        tela_raw: dict retornado por carregar_tela(caminho_base, id_tela).

    Retorna:
        ModeloTela com campos acessiveis por nome.

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
            sub_elementos = _construir_elementos_internos_grupo(
                elemento, elemento["id"]
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
                if chave not in ("id", "tipo")
            }
            elementos.append(
                ElementoCorpo(
                    id=elemento["id"],
                    tipo=elemento["tipo"],
                    _campos_inertes=inertes,
                )
            )

    corpo = Corpo(
        arranjo=corpo_raw.get("arranjo"),
        elementos=elementos,
        distribuicao=corpo_raw.get("distribuicao"),
    )

    return ModeloTela(
        id=tela_raw["id"],
        schema=tela_raw["schema"],
        cabecalho=tela_raw["cabecalho"],
        corpo=corpo,
        barra_de_menus=tela_raw["barra_de_menus"],
        _raw=tela_raw["_raw"],
    )
