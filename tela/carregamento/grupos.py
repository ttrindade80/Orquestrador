"""Validação dos grupos estruturais de tela.json."""

from tela.carregamento.distribuicao_corpo import _validar_distribuicao_corpo
from tela.carregamento.erros import (
    TelaEstruturaInvalida,
    TelaGrupoInvalido,
    TelaTipoDesconhecido,
)
from tela.carregamento.taxonomia import (
    ARRANJOS_CORPO_VALIDOS,
    ESTRUTURAS_GRUPO_VALIDAS,
    TIPOS_CORPO_VALIDOS,
)
from tela.carregamento.validacao_matricial import _validar_distribuicao_matricial

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
            # H-0035 / ADR-0025: elemento funcional interno de grupo pode
            # declarar distribuicao_matricial (adocao explicita, nivel unico).
            if "distribuicao_matricial" in item:
                _validar_distribuicao_matricial(
                    item["distribuicao_matricial"],
                    "{0} → {1}".format(caminho_grupo, id_item),
                )
        else:
            raise TelaTipoDesconhecido(tipo=tipo_item, id_elemento=id_item)
