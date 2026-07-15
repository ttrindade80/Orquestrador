"""Loader e validador macro de tela.json (H-0001).

Carrega `config/telas/<id_tela>.json` a partir de um caminho base, valida a
estrutura macro conforme `docs/contratos/contrato_tela_json.md` (secao 3) e
produz uma representacao interna simples e auditavel.

ESCOPO (H-0001):
- Apenas validacao macro (schema, id, cabecalho, corpo, barra_de_menus,
  corpo.elementos[] com id+tipo, taxonomia fechada de tipos).
- Campos declarativos pendentes (bindings, referencias_de_acoes, filtros,
  chips, tela_destino, origem_dados, itens do lancador, etc.) sao carregados
  e preservados como declaracao inerte. Nao sao executados, nao sao
  resolvidos, nao recebem validacao funcional.
- Nao executa acoes, nao ativa bindings, nao resolve tela_destino, nao
  altera JSONs de configuracao.

Apenas biblioteca padrao do Python.
"""

import json
import os
from pathlib import Path


TIPOS_CORPO_VALIDOS = {"console", "lancador", "dashboard"}

# Tipos estruturais de composicao (H-0012 / ADR-0010). Sao distintos da
# taxonomia funcional fechada (console, lancador, dashboard). Container
# estrutural nao e elemento funcional, nao gera caixa visual propria, nao e
# navegavel e nao tem foco/chip/acao/registry.
TIPOS_ESTRUTURAIS_VALIDOS = {"grupo"}

# Arranjos validos para o container raiz corpo (H-0019 / ADR-0011 / ADR-0015).
# Ausencia (None) e "vertical" preservam comportamento atual.
# "horizontal" ativa particionamento contíguo da largura disponível.
# "sobreposto" e "lado_a_lado" sao aliases transicionais literais aceitos.
ARRANJOS_CORPO_VALIDOS = {None, "vertical", "horizontal", "sobreposto", "lado_a_lado"}

# Modos validos de corpo.distribuicao (H-0025 / ADR-0018). A ausencia de
# corpo.distribuicao NAO equivale a "igual": preserva a construcao orientada
# pelo conteudo (ADR-0018 D2). "igual" so existe quando declarado.
MODOS_DISTRIBUICAO_CORPO_VALIDOS = {"igual", "percentual", "fracao"}

ESTRUTURAS_GRUPO_VALIDAS = {None, "livre", "matriz"}

_ID_TELA_RAIZ = "orquestrador"


class TelaErro(Exception):
    """Base das excecoes de validacao de tela.json."""


class TelaArquivoNaoEncontrado(TelaErro):
    """Arquivo de tela nao encontrado em disco."""


class TelaJsonInvalido(TelaErro):
    """Conteudo do arquivo nao e JSON sintaticamente valido."""


class TelaCampoObrigatorioAusente(TelaErro):
    """Campo macro obrigatorio ausente ou vazio."""

    def __init__(self, campo):
        self.campo = campo
        super().__init__(
            "Campo obrigatorio ausente: {0}".format(campo)
        )


class TelaIdNaoCoincideComArquivo(TelaErro):
    """id interno diverge do nome base do arquivo."""

    def __init__(self, id_interno, basename):
        self.id_interno = id_interno
        self.basename = basename
        super().__init__(
            "id interno '{0}' nao coincide com nome do arquivo '{1}'".format(
                id_interno, basename
            )
        )


class TelaIdIncorreto(TelaErro):
    """id incorreto para a tela raiz."""

    def __init__(self, encontrado, esperado=_ID_TELA_RAIZ):
        self.encontrado = encontrado
        self.esperado = esperado
        super().__init__(
            "id esperado para tela raiz: '{0}'; encontrado: '{1}'".format(
                esperado, encontrado
            )
        )


class TelaEstruturaInvalida(TelaErro):
    """Estrutura macro invalida (tipo errado, formato errado)."""


class TelaElementoSemId(TelaErro):
    """Elemento de corpo sem campo id."""

    def __init__(self, indice):
        self.indice = indice
        super().__init__(
            "Elemento na posicao {0} nao possui campo 'id'".format(indice)
        )


class TelaElementoSemTipo(TelaErro):
    """Elemento de corpo sem campo tipo."""

    def __init__(self, indice, id_elemento):
        self.indice = indice
        self.id_elemento = id_elemento
        super().__init__(
            "Elemento '{0}' (posicao {1}) nao possui campo 'tipo'".format(
                id_elemento, indice
            )
        )


class TelaTipoDesconhecido(TelaErro):
    """tipo de elemento de corpo fora da taxonomia fechada."""

    def __init__(self, tipo, id_elemento):
        self.tipo = tipo
        self.id_elemento = id_elemento
        super().__init__(
            "Tipo desconhecido '{0}' em elemento '{1}'; tipos validos: "
            "console, lancador, dashboard".format(tipo, id_elemento)
        )


class TelaGrupoInvalido(TelaErro):
    """Invariante do tipo estrutural 'grupo' violada (H-0012)."""


def _caminho_padrao_base():
    """Diretorio raiz do repositorio do Orquestrador (pai de tela/)."""
    return Path(__file__).resolve().parent.parent


def _eh_numero_nao_bool(valor):
    """True quando valor e int/float mas nao bool (bool e subclasse de int)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _validar_distribuicao_corpo(distribuicao, n_elementos, prefixo_caminho="corpo"):
    """Valida corpo.distribuicao declarado (H-0025 / ADR-0018).

    A distribuicao e OPCIONAL. Esta funcao so e chamada quando o campo existe.
    A ausencia de distribuicao preserva a construcao orientada pelo conteudo
    (ADR-0018 D2) e nao e tratada aqui.

    Regras (H-0025 secao 2; contrato_composicao_corpo.md secao 5.7):

    - deve ser um objeto;
    - ``modo`` em {igual, percentual, fracao};
    - ``igual``: nao exige ``valores`` (pesos equivalentes entre os filhos
      diretos); nao e fallback da ausencia;
    - ``percentual``: um valor por filho direto, todos positivos, soma
      exatamente 100, associacao posicional;
    - ``fracao``: um peso por filho direto, todos estritamente positivos,
      denominador igual a soma dos pesos, associacao posicional;
    - ``len(valores) == n_elementos`` (filhos diretos do container).

    Erros sao levantados como ``TelaEstruturaInvalida`` (categoria ja usada
    para corpo.arranjo), de forma deterministica, sem fallback silencioso.
    Nao muta o dict recebido.

    prefixo_caminho: caminho estrutural do container que declara a distribuicao
    (ex.: "corpo" para o corpo raiz; "corpo → g1" para um grupo). Usado para
    compor mensagens de diagnóstico que reflitam o container afetado.
    """
    _p = prefixo_caminho
    if not isinstance(distribuicao, dict):
        raise TelaEstruturaInvalida(
            "{0}.distribuicao deve ser um objeto; recebido: {1}".format(
                _p, type(distribuicao).__name__
            )
        )

    modo = distribuicao.get("modo")
    if modo not in MODOS_DISTRIBUICAO_CORPO_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.modo invalido: {1!r}; valores aceitos: "
            "igual, percentual, fracao".format(_p, modo)
        )

    if modo == "igual":
        # igual nao exige vetor concreto (H-0025 secao 2). Pesos equivalentes
        # sao derivados no renderer ([1]*n). Nao ha validacao de valores aqui.
        return

    valores = distribuicao.get("valores")
    if not isinstance(valores, list):
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.valores invalido para modo {1!r}: "
            "esperado lista".format(_p, modo)
        )

    if len(valores) != n_elementos:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao.valores com quantidade {1} divergente da "
            "quantidade de filhos diretos ({2})".format(
                _p, len(valores), n_elementos
            )
        )

    for indice, valor in enumerate(valores):
        if not _eh_numero_nao_bool(valor) or valor <= 0:
            raise TelaEstruturaInvalida(
                "{0}.distribuicao.valores[{1}] invalido: {2!r}; esperado "
                "numero estritamente positivo".format(_p, indice, valor)
            )

    if modo == "percentual" and sum(valores) != 100:
        raise TelaEstruturaInvalida(
            "{0}.distribuicao percentual exige soma igual a 100; soma "
            "encontrada: {1}".format(_p, sum(valores))
        )


def _para_base(caminho_base):
    if caminho_base is None:
        return _caminho_padrao_base()
    if isinstance(caminho_base, Path):
        return caminho_base
    return Path(caminho_base)


def _validar_quantidade_matriz(matriz, eixo, id_grupo, caminho_grupo):
    caminho_eixo = "{0}.matriz.{1}".format(caminho_grupo, eixo)
    dados_eixo = matriz.get(eixo)
    if not isinstance(dados_eixo, dict):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} deve ser um objeto".format(
                id_grupo, caminho_grupo, caminho_eixo
            )
        )

    quantidade = dados_eixo.get("quantidade")
    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade < 2
        or quantidade > 4
    ):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2}.quantidade invalida: {3!r}; "
            "esperado inteiro entre 2 e 4".format(
                id_grupo, caminho_grupo, caminho_eixo, quantidade
            )
        )
    return dados_eixo, quantidade


def _validar_distribuicao_matriz(dados_eixo, quantidade, eixo, id_grupo, caminho_grupo):
    caminho_eixo = "{0}.matriz.{1}".format(caminho_grupo, eixo)
    if "distribuicao" not in dados_eixo:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2}.distribuicao ausente; "
            "distribuicao de {3} e obrigatoria em matriz".format(
                id_grupo, caminho_grupo, caminho_eixo, eixo
            )
        )
    _validar_distribuicao_corpo(
        dados_eixo.get("distribuicao"), quantidade, caminho_eixo
    )


def _validar_celulas_matriz(matriz, sub, id_grupo, caminho_grupo, n_linhas, n_colunas):
    caminho_celulas = "{0}.matriz.celulas".format(caminho_grupo)
    celulas = matriz.get("celulas")
    if not isinstance(celulas, list):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} deve ser uma lista".format(
                id_grupo, caminho_grupo, caminho_celulas
            )
        )

    esperado = n_linhas * n_colunas
    if len(celulas) != esperado:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': {2} com quantidade invalida; "
            "esperado {3}, encontrado {4} (cobertura completa obrigatoria)".format(
                id_grupo, caminho_grupo, caminho_celulas, esperado, len(celulas)
            )
        )

    ids_filhos = []
    for indice, item in enumerate(sub):
        id_item = item.get("id") if isinstance(item, dict) else None
        if not isinstance(id_item, str) or id_item == "":
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': elementos[{2}].id invalido para "
                "cobertura de matriz".format(id_grupo, caminho_grupo, indice)
            )
        ids_filhos.append(id_item)

    ids_filhos_set = set(ids_filhos)
    if len(ids_filhos_set) != len(ids_filhos):
        vistos = set()
        duplicado = None
        for id_item in ids_filhos:
            if id_item in vistos:
                duplicado = id_item
                break
            vistos.add(id_item)
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': elementos[] contem id duplicado para "
            "matriz: {2!r}".format(id_grupo, caminho_grupo, duplicado)
        )

    coordenadas_vistas = set()
    elementos_vistos = set()
    for indice, celula in enumerate(celulas):
        caminho_celula = "{0}[{1}]".format(caminho_celulas, indice)
        if not isinstance(celula, dict):
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} deve ser objeto com linha, "
                "coluna e elemento".format(id_grupo, caminho_grupo, caminho_celula)
            )

        linha = celula.get("linha")
        coluna = celula.get("coluna")
        elemento_ref = celula.get("elemento")

        if not isinstance(linha, int) or isinstance(linha, bool) or linha < 1:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.linha invalida: {3!r}; "
                "coordenadas iniciam em 1".format(
                    id_grupo, caminho_grupo, caminho_celula, linha
                )
            )
        if not isinstance(coluna, int) or isinstance(coluna, bool) or coluna < 1:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.coluna invalida: {3!r}; "
                "coordenadas iniciam em 1".format(
                    id_grupo, caminho_grupo, caminho_celula, coluna
                )
            )
        if not isinstance(elemento_ref, str) or elemento_ref == "":
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.elemento invalido; "
                "celula vazia e proibida".format(
                    id_grupo, caminho_grupo, caminho_celula
                )
            )

        if linha > n_linhas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.linha fora do limite: {3}; "
                "limite de linhas: {4}".format(
                    id_grupo, caminho_grupo, caminho_celula, linha, n_linhas
                )
            )
        if coluna > n_colunas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.coluna fora do limite: {3}; "
                "limite de colunas: {4}".format(
                    id_grupo, caminho_grupo, caminho_celula, coluna, n_colunas
                )
            )

        coordenada = (linha, coluna)
        if coordenada in coordenadas_vistas:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} contem coordenada duplicada: "
                "linha={3}, coluna={4}".format(
                    id_grupo, caminho_grupo, caminho_celulas, linha, coluna
                )
            )
        coordenadas_vistas.add(coordenada)

        if elemento_ref in elementos_vistos:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2} contem elemento duplicado: {3!r}".format(
                    id_grupo, caminho_grupo, caminho_celulas, elemento_ref
                )
            )
        elementos_vistos.add(elemento_ref)

        if elemento_ref not in ids_filhos_set:
            raise TelaGrupoInvalido(
                "Grupo '{0}' em '{1}': {2}.elemento referencia filho direto "
                "inexistente: {3!r}".format(
                    id_grupo, caminho_grupo, caminho_celula, elemento_ref
                )
            )

    coordenadas_esperadas = {
        (linha, coluna)
        for linha in range(1, n_linhas + 1)
        for coluna in range(1, n_colunas + 1)
    }
    faltantes = coordenadas_esperadas - coordenadas_vistas
    if faltantes:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': cobertura incompleta em matriz.celulas; "
            "coordenadas faltantes: {2!r}".format(
                id_grupo, caminho_grupo, sorted(faltantes)
            )
        )

    filhos_sem_celula = ids_filhos_set - elementos_vistos
    if filhos_sem_celula:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': elementos sem celula na cobertura da matriz: "
            "{2!r}".format(id_grupo, caminho_grupo, sorted(filhos_sem_celula))
        )


def _validar_matriz_grupo(elemento, sub, id_grupo, caminho_grupo):
    matriz = elemento.get("matriz")
    if not isinstance(matriz, dict):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}': matriz deve ser objeto obrigatorio em "
            "estrutura: \"matriz\"".format(id_grupo, caminho_grupo)
        )

    linhas, n_linhas = _validar_quantidade_matriz(
        matriz, "linhas", id_grupo, caminho_grupo
    )
    colunas, n_colunas = _validar_quantidade_matriz(
        matriz, "colunas", id_grupo, caminho_grupo
    )
    _validar_distribuicao_matriz(
        linhas, n_linhas, "linhas", id_grupo, caminho_grupo
    )
    _validar_distribuicao_matriz(
        colunas, n_colunas, "colunas", id_grupo, caminho_grupo
    )
    _validar_celulas_matriz(
        matriz, sub, id_grupo, caminho_grupo, n_linhas, n_colunas
    )


def _validar_grupo(elemento, id_grupo, nivel_grupo=1, caminho="corpo"):
    """Valida os invariantes do tipo estrutural 'grupo' (ADR-0019 / H-0027).

    Valida recursivamente com contagem de profundidade exclusivamente por nós
    estruturais ``grupo`` (ADR-0019 D1). Niveis 1, 2 e 3 sao validos; nivel
    4 e invalido e rejeitado com erro determinístico (ADR-0019 D4). Multiplos
    filhos e grupos irmaos sao permitidos (ADR-0019 D5, D6).

    Parametros:
        elemento: dict do grupo a validar.
        id_grupo: id declarado do grupo.
        nivel_grupo: profundidade do grupo atual (1 = filho direto do corpo).
        caminho: string de contexto para diagnostico (ex.: "corpo → g1").
    """
    estrutura = elemento.get("estrutura")
    if estrutura not in ESTRUTURAS_GRUPO_VALIDAS:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com estrutura invalida em {1}.estrutura: "
            "{2!r}; valores aceitos: livre, matriz, ou ausente".format(
                id_grupo, caminho, estrutura
            )
        )

    # Validar arranjo contra o mesmo conjunto do corpo raiz (ADR-0015 / H-0027).
    arranjo = elemento.get("arranjo")
    if estrutura == "matriz" and arranjo is not None:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' declara arranjo em estrutura: \"matriz\"; "
            "arranjo e proibido em matriz".format(id_grupo, caminho)
        )
    if estrutura != "matriz" and arranjo not in ARRANJOS_CORPO_VALIDOS:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com arranjo invalido: {2!r}; "
            "valores aceitos: vertical, horizontal, sobreposto, lado_a_lado, "
            "ou ausente".format(id_grupo, caminho, arranjo)
        )

    if "elementos" not in elemento:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' sem campo 'elementos'".format(
                id_grupo, caminho
            )
        )

    sub = elemento.get("elementos")
    if not isinstance(sub, list):
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com 'elementos' nao e uma lista".format(
                id_grupo, caminho
            )
        )

    if len(sub) == 0:
        raise TelaGrupoInvalido(
            "Grupo '{0}' em '{1}' com 'elementos' vazio".format(
                id_grupo, caminho
            )
        )

    # Caminho que inclui o grupo atual, usado em erros dos filhos e na
    # distribuicao (para que mensagens reflitam o container afetado, nao "corpo").
    caminho_grupo = "{0} → {1}".format(caminho, id_grupo)

    if estrutura == "matriz":
        try:
            _validar_matriz_grupo(elemento, sub, id_grupo, caminho_grupo)
        except TelaEstruturaInvalida as exc:
            raise TelaEstruturaInvalida(
                "Grupo '{0}' em '{1}': {2}".format(id_grupo, caminho, exc)
            ) from exc

    # Validar distribuicao do grupo se declarada (ADR-0015 / ADR-0019).
    # Passa caminho_grupo como prefixo para que as mensagens de erro usem o
    # caminho estrutural real (ex.: "corpo → g1.distribuicao.modo invalido")
    # em vez de "corpo.distribuicao.modo invalido" (ACH-005 patch H-0027).
    distribuicao = elemento.get("distribuicao")
    if estrutura != "matriz" and distribuicao is not None:
        try:
            _validar_distribuicao_corpo(distribuicao, len(sub), caminho_grupo)
        except TelaEstruturaInvalida as exc:
            raise TelaEstruturaInvalida(
                "Grupo '{0}' em '{1}': {2}".format(id_grupo, caminho, exc)
            ) from exc

    for sub_indice, item in enumerate(sub):
        if not isinstance(item, dict) or "id" not in item:
            raise TelaGrupoInvalido(
                "Elemento interno na posicao {0} do grupo '{1}' em '{2}' "
                "sem campo 'id'".format(sub_indice, id_grupo, caminho)
            )
        id_item = item.get("id")
        if not isinstance(id_item, str) or id_item == "":
            raise TelaGrupoInvalido(
                "Elemento interno na posicao {0} do grupo '{1}' em '{2}' "
                "com 'id' invalido".format(sub_indice, id_grupo, caminho)
            )

        if "tipo" not in item:
            raise TelaGrupoInvalido(
                "Elemento interno '{0}' do grupo '{1}' em '{2}' sem campo "
                "'tipo'".format(id_item, id_grupo, caminho)
            )
        tipo_item = item.get("tipo")
        if not isinstance(tipo_item, str) or tipo_item == "":
            raise TelaGrupoInvalido(
                "Elemento interno '{0}' do grupo '{1}' em '{2}' com 'tipo' "
                "invalido".format(id_item, id_grupo, caminho)
            )

        if tipo_item == "grupo":
            if nivel_grupo == 3:
                # Grupo filho de grupo no nivel 3 estaria no nivel 4: invalido.
                raise TelaGrupoInvalido(
                    "Grupo '{0}' em '{1}' criaria nivel 4 de grupo, que e "
                    "invalido; maximo e 3 niveis de grupos "
                    "(ADR-0019 D4)".format(id_item, caminho_grupo)
                )
            # Recursao: validar grupo filho com nivel_grupo + 1.
            _validar_grupo(item, id_item, nivel_grupo + 1, caminho_grupo)
        elif tipo_item in TIPOS_CORPO_VALIDOS:
            pass  # elemento funcional aceito (ADR-0019 D3, D6)
        else:
            raise TelaTipoDesconhecido(tipo=tipo_item, id_elemento=id_item)


def carregar_tela(caminho_base, id_tela, raiz_telas=None):
    """Carrega e valida macro de `<raiz_telas>/<id_tela>.json`.

    Parametros:
        caminho_base: diretorio raiz do repositorio do Orquestrador. Se None,
            usa o pai do diretorio deste modulo (tela/).
        id_tela: identificador estavel da tela. Define o nome do arquivo
            (`<raiz_telas>/<id_tela>.json`) e e comparado ao `id` interno.
        raiz_telas: caminho relativo ao repositorio onde estao os JSONs de
            tela. Se None, usa `config/telas` (raiz do produto real). Para
            a demonstracao, passar `config/telas/demo` explicitamente. Nao
            ha fallback entre raizes: ausencia em uma raiz nao dispara
            tentativa na outra.

    Retorna:
        dict com representacao interna minima:
            {
                "id": str,
                "schema": str,
                "cabecalho": dict,
                "corpo": {"arranjo": str | None, "elementos": [...]},
                "barra_de_menus": dict,
                "_raw": dict,
            }

    Lanca:
        TelaArquivoNaoEncontrado, TelaJsonInvalido,
        TelaCampoObrigatorioAusente, TelaIdNaoCoincideComArquivo,
        TelaIdIncorreto, TelaEstruturaInvalida,
        TelaElementoSemId, TelaElementoSemTipo, TelaTipoDesconhecido.

    Observacoes:
        - Campos declarativos pendentes (DOC-B008 / DOC-B009) sao
          preservados em `_raw` e nos subdicts como declaracao inerte.
        - Nao executa, nao resolve nem valida funcionalmente esses campos.
    """
    base = _para_base(caminho_base)
    if not isinstance(id_tela, str) or not id_tela:
        raise TelaCampoObrigatorioAusente(campo="id (parametro id_tela)")

    if raiz_telas is None:
        raiz_telas = os.path.join("config", "telas")

    caminho_relativo = os.path.join(raiz_telas, id_tela + ".json")
    caminho_arquivo = base / caminho_relativo

    if not caminho_arquivo.is_file():
        raise TelaArquivoNaoEncontrado(
            "Arquivo nao encontrado: {0}".format(caminho_relativo)
        )

    try:
        texto = caminho_arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        raise TelaArquivoNaoEncontrado(
            "Arquivo nao encontrado: {0} ({1})".format(caminho_relativo, exc)
        )

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise TelaJsonInvalido(
            "JSON invalido em: {0} - {1}".format(caminho_relativo, exc)
        )

    if not isinstance(dados, dict):
        raise TelaJsonInvalido(
            "JSON invalido em: {0} - raiz nao e um objeto".format(
                caminho_relativo
            )
        )

    if "schema" not in dados:
        raise TelaCampoObrigatorioAusente(campo="schema")

    id_interno = dados.get("id")
    if not isinstance(id_interno, str) or id_interno == "":
        raise TelaCampoObrigatorioAusente(campo="id")

    basename = caminho_arquivo.stem
    if id_interno != basename:
        raise TelaIdNaoCoincideComArquivo(id_interno, basename)

    if id_tela == _ID_TELA_RAIZ and id_interno != _ID_TELA_RAIZ:
        raise TelaIdIncorreto(encontrado=id_interno)

    if "cabecalho" not in dados:
        raise TelaCampoObrigatorioAusente(campo="cabecalho")

    if "corpo" not in dados:
        raise TelaCampoObrigatorioAusente(campo="corpo")

    if "barra_de_menus" not in dados:
        raise TelaCampoObrigatorioAusente(campo="barra_de_menus")

    corpo = dados.get("corpo")
    if not isinstance(corpo, dict):
        raise TelaEstruturaInvalida(
            "'corpo' nao e um objeto"
        )

    if "elementos" not in corpo:
        raise TelaCampoObrigatorioAusente(campo="corpo.elementos")

    elementos = corpo.get("elementos")
    if not isinstance(elementos, list):
        raise TelaEstruturaInvalida(
            "'corpo.elementos' ausente ou nao e uma lista"
        )

    elementos_internos = []
    for indice, elemento in enumerate(elementos):
        if not isinstance(elemento, dict):
            raise TelaElementoSemId(indice=indice)
        if "id" not in elemento:
            raise TelaElementoSemId(indice=indice)
        id_elemento = elemento.get("id")
        if not isinstance(id_elemento, str) or id_elemento == "":
            raise TelaElementoSemId(indice=indice)
        if "tipo" not in elemento:
            raise TelaElementoSemTipo(indice=indice, id_elemento=id_elemento)
        tipo = elemento.get("tipo")
        if not isinstance(tipo, str) or tipo == "":
            raise TelaElementoSemTipo(indice=indice, id_elemento=id_elemento)
        if tipo in TIPOS_ESTRUTURAIS_VALIDOS:
            _validar_grupo(elemento, id_elemento)
        elif tipo not in TIPOS_CORPO_VALIDOS:
            raise TelaTipoDesconhecido(tipo=tipo, id_elemento=id_elemento)
        elementos_internos.append(elemento)

    arranjo = corpo.get("arranjo")
    if arranjo not in ARRANJOS_CORPO_VALIDOS:
        raise TelaEstruturaInvalida(
            "corpo.arranjo invalido: {0!r}; valores aceitos: "
            "vertical, horizontal, sobreposto (alias), lado_a_lado (alias)".format(
                arranjo
            )
        )

    # H-0025 / ADR-0018: corpo.distribuicao e OPCIONAL. A ausencia preserva
    # a construcao orientada pelo conteudo (nao materializa "igual"). Quando
    # declarada, e validada e preservada no dict de saida sem conversao.
    distribuicao = corpo.get("distribuicao")
    if distribuicao is not None:
        _validar_distribuicao_corpo(distribuicao, len(elementos_internos))

    return {
        "id": id_interno,
        "schema": dados.get("schema"),
        "cabecalho": dados.get("cabecalho"),
        "corpo": {
            "arranjo": arranjo,
            "distribuicao": distribuicao,
            "elementos": elementos_internos,
        },
        "barra_de_menus": dados.get("barra_de_menus"),
        "_raw": dados,
    }
