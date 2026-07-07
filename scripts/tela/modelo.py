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

from tela.loader import TIPOS_CORPO_VALIDOS


class ModeloTelaErro(Exception):
    """Erro de construcao do modelo interno de tela."""


@dataclass
class ElementoCorpo:
    """Elemento do corpo com `id` e `tipo` acessiveis; demais campos inertes.

    Os campos adicionais do elemento (titulo, origem_dados, itens, etc.)
    sao preservados em `_campos_inertes` como declaracao inerte, sem
    execucao, sem resolucao e sem semantica nova.
    """

    id: str
    tipo: str
    _campos_inertes: dict = field(default_factory=dict, repr=False)


@dataclass
class Corpo:
    """Corpo da tela: arranjo declarativo e lista de elementos."""

    arranjo: str | None
    elementos: list  # lista de ElementoCorpo


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
        if tipo not in TIPOS_CORPO_VALIDOS:
            raise ModeloTelaErro(
                "Tipo desconhecido '{0}' em elemento '{1}'".format(
                    tipo, elemento["id"]
                )
            )
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

    corpo = Corpo(arranjo=corpo_raw.get("arranjo"), elementos=elementos)

    return ModeloTela(
        id=tela_raw["id"],
        schema=tela_raw["schema"],
        cabecalho=tela_raw["cabecalho"],
        corpo=corpo,
        barra_de_menus=tela_raw["barra_de_menus"],
        _raw=tela_raw["_raw"],
    )
