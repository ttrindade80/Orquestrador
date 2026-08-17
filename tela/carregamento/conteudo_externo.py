"""Validação e carregamento de conteúdo externo multinível."""

import copy
import json
import os
import tempfile

from tela.carregamento.caminho_base import _para_base
from tela.carregamento.erros import (
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaEstruturaInvalida,
    TelaJsonInvalido,
)

APRESENTACOES_CONTEUDO_VALIDAS = {"tabela", "hierarquia", "conjuntos_campos"}

# Tipos de nivel (contrato_json_console.md secao 12.3).
TIPOS_NIVEL_CONTEUDO_VALIDOS = {"container", "conteudo", "nome_valor"}

# Tipos de designador (contrato_json_console.md secao 12.3 / secao 13.7 H-0036).
TIPOS_DESIGNADOR_VALIDOS = {
    "nenhum", "simbolo", "decimal", "alfabetico_minusculo",
    "alfabetico_maiusculo", "romano_minusculo", "romano_maiusculo",
    "decimal_composto", "personalizado",
}

# Blocos especificos por apresentacao (contrato_json_console.md secao 12.2):
# ``tabela`` somente em ``tabela``; ``campos`` somente em ``conjuntos_campos``;
# nenhum bloco especifico em ``hierarquia``.
_BLOCO_ESPECIFICO_POR_APRESENTACAO = {
    "tabela": "tabela",
    "conjuntos_campos": "campos",
}
_BLOCOS_ESPECIFICOS_APRESENTACAO = {"tabela", "campos"}

# Nomes de campo de resultado fisico calculado proibidos no documento externo
# (contrato_json_console.md secao 12.6; H-0036 secao 13.8). Cada nome mapeia
# uma das formas fisicas proibidas normativas. A deteccao rejeita qualquer
# ocorrencia destes nomes de campo em qualquer profundidade do documento.
CAMPOS_RESULTADO_FISICO_PROIBIDOS = {
    "largura_efetiva",        # largura efetiva
    "altura_efetiva",         # altura efetiva
    "linhas_calculadas",      # quantidade fisica calculada de linhas
    "colunas_calculadas",     # quantidade fisica calculada de colunas
    "posicao_final",          # posicao final
    "coordenada_final",       # coordenada fisica final
    "pagina_calculada",       # pagina calculada
    "quebra_pronta",          # quebra fisica pronta
    "truncamento_aplicado",   # truncamento ja aplicado
    "distribuicao_concreta",  # distribuicao concreta do espaco restante
    "celulas_vazias",         # celulas vazias calculadas
    "geometria_final",        # geometria final
    "numeracao_concreta",     # numeracao concreta de designadores
}
def _validar_designador_conteudo(designador, id_nivel, origem):
    """Valida a politica declarativa de designador de um nivel.

    O designador declara a forma do marcador; o renderizador calcula a
    sequencia concreta. O documento externo NAO armazena a numeracao ja
    calculada (contrato_json_console.md secao 12.3 / secao 13.7 do H-0036).
    """
    if not isinstance(designador, dict):
        raise TelaEstruturaInvalida(
            "{0}: nivel {1!r}.designador deve ser objeto".format(origem, id_nivel)
        )
    if "tipo" not in designador:
        raise TelaCampoObrigatorioAusente(
            campo="formato.niveis[{0}].designador.tipo".format(id_nivel)
        )
    tipo_desig = designador["tipo"]
    if tipo_desig not in TIPOS_DESIGNADOR_VALIDOS:
        raise TelaEstruturaInvalida(
            "{0}: nivel {1!r}.designador.tipo invalido: {2!r}; aceitos: "
            "{3}".format(
                origem, id_nivel, tipo_desig,
                ", ".join(sorted(TIPOS_DESIGNADOR_VALIDOS)),
            )
        )


def _rejeitar_resultados_fisicos_conteudo(obj, origem, caminho="documento"):
    """Rejeita recursivamente campos de resultado fisico calculado (validacao 20).

    Percorre objetos e arrays em qualquer profundidade. Nao amplia a proibicao
    para campos semanticos validos: rejeita apenas os nomes exatos declarados
    em ``CAMPOS_RESULTADO_FISICO_PROIBIDOS`` (contrato_json_console.md 12.6).
    """
    if isinstance(obj, dict):
        for chave, valor in obj.items():
            if chave in CAMPOS_RESULTADO_FISICO_PROIBIDOS:
                raise TelaEstruturaInvalida(
                    "{0}: campo de resultado fisico calculado proibido: "
                    "{1!r} em {2} (contrato_json_console 12.6)".format(
                        origem, chave, caminho
                    )
                )
            _rejeitar_resultados_fisicos_conteudo(
                valor, origem, "{0}.{1}".format(caminho, chave)
            )
    elif isinstance(obj, list):
        for indice, item in enumerate(obj):
            _rejeitar_resultados_fisicos_conteudo(
                item, origem, "{0}[{1}]".format(caminho, indice)
            )
_CAMPOS_COLUNA_RECONHECIVEL = frozenset({"titulo", "nivel", "campo"})
def _coluna_reconhecivel(entrada):
    """True quando ``entrada`` satisfaz a forma contratual minima de coluna.

    Usado por V-01 (cabecalho) e distinto de V-14 (origem da coluna).
    Uma coluna e estruturalmente reconhecivel quando:

    - e uma string com ao menos um caractere nao-espaco (cabecalho simples,
      como ``["Grupo", "Valor"]``), ou
    - e um objeto em que ao menos um campo minimo (``titulo``, ``nivel`` ou
      ``campo``) possui valor semanticamente nao vazio.

    Valor semanticamente vazio: None, string vazia ou string composta apenas de
    espacos. A simples presenca da chave nao basta — o valor deve ser nao vazio.
    Entradas nulas, tipos incorretos, objetos vazios, objetos sem campos minimos
    e objetos cujos campos minimos possuem valores semanticamente vazios NAO sao
    colunas reconheciveis.

    Distincao com V-14: V-14 rejeita coluna reconhecivel (forma valida) sem
    origem; V-01 rejeita ausencia total de qualquer coluna reconhecivel.
    """
    if isinstance(entrada, str):
        return entrada.strip() != ""
    if isinstance(entrada, dict):
        for campo in _CAMPOS_COLUNA_RECONHECIVEL:
            if campo not in entrada:
                continue
            v = entrada[campo]
            if v is not None and not (isinstance(v, str) and v.strip() == ""):
                return True
        return False
    return False
def _validar_no_conteudo(no, niveis_por_id, origem, caminho):
    """Valida um no de ``dados``/``filhos`` (validacoes 12-17).

    Recursivo para nos de tipo ``container`` (validacao 17). A ordem dos
    arrays e preservada (validacao 18): esta funcao nao reordena nada.
    """
    if not isinstance(no, dict):
        raise TelaEstruturaInvalida(
            "{0}: {1} nao e objeto".format(origem, caminho)
        )
    # Validacao 12: cada no possui id e nivel.
    if "id" not in no:
        raise TelaCampoObrigatorioAusente(campo="{0}.id".format(caminho))
    if "nivel" not in no:
        raise TelaCampoObrigatorioAusente(campo="{0}.nivel".format(caminho))
    nivel_ref = no["nivel"]
    # Validacao 13: nivel referencia item declarado em formato.niveis.
    if nivel_ref not in niveis_por_id:
        raise TelaEstruturaInvalida(
            "{0}: {1}.nivel referencia nivel nao declarado: {2!r}".format(
                origem, caminho, nivel_ref
            )
        )
    nivel = niveis_por_id[nivel_ref]
    tipo_nivel = nivel["tipo"]
    conteudo_decl = nivel["conteudo"]

    if tipo_nivel == "container":
        # Validacao 14: campo semantico declarado + filhos como array.
        if not isinstance(conteudo_decl, str) or conteudo_decl not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (container)".format(caminho, conteudo_decl)
            )
        filhos = no.get("filhos")
        if not isinstance(filhos, list):
            raise TelaEstruturaInvalida(
                "{0}: {1} (nivel container) exige 'filhos' como array".format(
                    origem, caminho
                )
            )
        # V-05: container com filhos declarados mas vazios e invalido.
        if len(filhos) == 0:
            raise TelaEstruturaInvalida(
                "{0}: V-05: {1} (container) com 'filhos' vazio; pelo menos "
                "um filho e obrigatorio".format(origem, caminho)
            )
        # Validacao 17: filhos validados recursivamente com as mesmas regras.
        for indice, filho in enumerate(filhos):
            _validar_no_conteudo(
                filho, niveis_por_id, origem,
                "{0}.filhos[{1}]".format(caminho, indice),
            )
    elif tipo_nivel == "conteudo":
        # Validacao 15: campo semantico declarado.
        if not isinstance(conteudo_decl, str) or conteudo_decl not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (conteudo)".format(caminho, conteudo_decl)
            )
        # V-04: no folha (conteudo) nao pode declarar filhos (inclusive lista vazia).
        if "filhos" in no:
            raise TelaEstruturaInvalida(
                "{0}: V-04: {1} (conteudo, folha) nao pode declarar "
                "filhos".format(origem, caminho)
            )
    elif tipo_nivel == "nome_valor":
        # Validacao 16: campos de nome e valor declarados presentes.
        campo_nome = conteudo_decl.get("nome")
        campo_valor = conteudo_decl.get("valor")
        if campo_nome not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (nome_valor.nome)".format(caminho, campo_nome)
            )
        if campo_valor not in no:
            raise TelaCampoObrigatorioAusente(
                campo="{0}.{1} (nome_valor.valor)".format(caminho, campo_valor)
            )
        # V-04: no folha (nome_valor) nao pode declarar filhos (inclusive lista vazia).
        if "filhos" in no:
            raise TelaEstruturaInvalida(
                "{0}: V-04: {1} (nome_valor, folha) nao pode declarar "
                "filhos".format(origem, caminho)
            )


def validar_conteudo_externo(documento, origem="documento externo"):
    """Executa as 20 validacoes semanticas do documento externo de conteudo.

    Autoridade: ADR-0027 D11/D13; contrato_json_console.md secao 12.5;
    H-0036 secao 14. As validacoes sao verificadas nominalmente e na ordem
    das secoes do contrato. Erros usam as classes de dominio existentes.

    Nao calcula geometria, nao infere hierarquia (declarada por ``filhos``),
    nao reordena arrays (validacao 18 e preservada por construcao) e nao muta
    o documento recebido. Devolve o proprio ``documento`` quando valido, para
    encadeamento conveniente.
    """
    # Validacao 1: raiz e objeto.
    if not isinstance(documento, dict):
        raise TelaEstruturaInvalida(
            "{0}: raiz do documento externo nao e objeto (recebido: {1})".format(
                origem, type(documento).__name__
            )
        )
    # Validacao 2: tipo presente e do tipo correto (string).
    if "tipo" not in documento:
        raise TelaCampoObrigatorioAusente(campo="tipo (documento externo)")
    tipo = documento["tipo"]
    if not isinstance(tipo, str):
        raise TelaEstruturaInvalida(
            "{0}: campo 'tipo' deve ser string; recebido: {1}".format(
                origem, type(tipo).__name__
            )
        )
    # Validacao 3: tipo igual a "multinivel".
    if tipo != "multinivel":
        raise TelaEstruturaInvalida(
            "{0}: tipo {1!r} nao suportado; unico tipo aceito: "
            "'multinivel'".format(origem, tipo)
        )
    # Validacao 4: formato presente e objeto.
    if "formato" not in documento:
        raise TelaCampoObrigatorioAusente(campo="formato (documento externo)")
    formato = documento["formato"]
    if not isinstance(formato, dict):
        raise TelaEstruturaInvalida(
            "{0}: 'formato' deve ser objeto".format(origem)
        )
    # Validacao 5: dados presente e array.
    if "dados" not in documento:
        raise TelaCampoObrigatorioAusente(campo="dados (documento externo)")
    dados = documento["dados"]
    if not isinstance(dados, list):
        raise TelaEstruturaInvalida(
            "{0}: 'dados' deve ser array".format(origem)
        )
    # Validacao 6: formato.apresentacao presente.
    if "apresentacao" not in formato:
        raise TelaCampoObrigatorioAusente(
            campo="formato.apresentacao (documento externo)"
        )
    apresentacao = formato["apresentacao"]
    # Validacao 7: apresentacao pertence ao conjunto previsto.
    if apresentacao not in APRESENTACOES_CONTEUDO_VALIDAS:
        raise TelaEstruturaInvalida(
            "{0}: formato.apresentacao invalida: {1!r}; aceitas: "
            "{2}".format(
                origem, apresentacao,
                ", ".join(sorted(APRESENTACOES_CONTEUDO_VALIDAS)),
            )
        )
    # Validacao 8: formato.niveis presente e array.
    if "niveis" not in formato:
        raise TelaCampoObrigatorioAusente(
            campo="formato.niveis (documento externo)"
        )
    niveis = formato["niveis"]
    if not isinstance(niveis, list):
        raise TelaEstruturaInvalida(
            "{0}: formato.niveis deve ser array".format(origem)
        )
    # Validacoes 9, 10, 11: cada nivel possui id/tipo/conteudo/designador;
    # ids nao vazios e unicos; tipos de nivel validos. Coleta niveis_por_id.
    niveis_por_id = {}
    for indice, nivel in enumerate(niveis):
        if not isinstance(nivel, dict):
            raise TelaEstruturaInvalida(
                "{0}: formato.niveis[{1}] nao e objeto".format(origem, indice)
            )
        # Validacao 9: possui id, tipo, conteudo e designador.
        for campo in ("id", "tipo", "conteudo", "designador"):
            if campo not in nivel:
                raise TelaCampoObrigatorioAusente(
                    campo="formato.niveis[{0}].{1}".format(indice, campo)
                )
        id_nivel = nivel["id"]
        # Validacao 10: id nao vazio e unico.
        if not isinstance(id_nivel, str) or id_nivel == "":
            raise TelaEstruturaInvalida(
                "{0}: formato.niveis[{1}].id vazio ou nao-string".format(
                    origem, indice
                )
            )
        if id_nivel in niveis_por_id:
            raise TelaEstruturaInvalida(
                "{0}: id de nivel duplicado em formato.niveis: {1!r}".format(
                    origem, id_nivel
                )
            )
        # Validacao 11: tipo de nivel pertence ao conjunto previsto.
        tipo_nivel = nivel["tipo"]
        if tipo_nivel not in TIPOS_NIVEL_CONTEUDO_VALIDOS:
            raise TelaEstruturaInvalida(
                "{0}: nivel {1!r} com tipo invalido: {2!r}; aceitos: "
                "{3}".format(
                    origem, id_nivel, tipo_nivel,
                    ", ".join(sorted(TIPOS_NIVEL_CONTEUDO_VALIDOS)),
                )
            )
        # Coerencia da declaracao de conteudo por tipo de nivel.
        conteudo_decl = nivel["conteudo"]
        if tipo_nivel == "nome_valor":
            if (
                not isinstance(conteudo_decl, dict)
                or not isinstance(conteudo_decl.get("nome"), str)
                or not isinstance(conteudo_decl.get("valor"), str)
            ):
                raise TelaEstruturaInvalida(
                    "{0}: V-06: nivel {1!r} (nome_valor) exige conteudo com "
                    "'nome' e 'valor' como nomes de campo string (campo "
                    "nome-valor sem origem do valor)".format(origem, id_nivel)
                )
        else:
            if not isinstance(conteudo_decl, str) or conteudo_decl == "":
                raise TelaEstruturaInvalida(
                    "{0}: nivel {1!r} exige conteudo como nome de campo "
                    "(string nao vazia)".format(origem, id_nivel)
                )
        _validar_designador_conteudo(nivel["designador"], id_nivel, origem)
        niveis_por_id[id_nivel] = nivel

    # Validacao 19: blocos especificos compativeis com a apresentacao.
    for bloco in _BLOCOS_ESPECIFICOS_APRESENTACAO:
        if bloco in formato and _BLOCO_ESPECIFICO_POR_APRESENTACAO.get(
            apresentacao
        ) != bloco:
            raise TelaEstruturaInvalida(
                "{0}: bloco {1!r} incompativel com apresentacao {2!r}; "
                "'tabela' so em apresentacao tabela, 'campos' so em "
                "conjuntos_campos".format(origem, bloco, apresentacao)
            )

    # Validacao 20: documento nao contem resultados fisicos calculados.
    _rejeitar_resultados_fisicos_conteudo(documento, origem)

    # Validacoes 12-18: nos de dados (recursivo, ordem preservada).
    for indice, no in enumerate(dados):
        _validar_no_conteudo(
            no, niveis_por_id, origem, "dados[{0}]".format(indice)
        )

    # Catalogo estrutural de campos de nos de dados derivado de
    # ``formato.niveis[].conteudo`` (contrato_json_console.md §12.3). Para cada
    # nivel, ``conteudo`` declara os nomes dos campos do no que carregam
    # conteudo exibivel:
    #   - ``container``/``conteudo``: ``conteudo`` e uma string com o nome do
    #     campo de texto do no (ex.: "titulo", "texto");
    #   - ``nome_valor``: ``conteudo`` e um objeto declarando os campos
    #     ``nome`` e ``valor`` (nomes dos campos do no).
    # Esse conjunto e a autoridade estrutural para validar ``campo`` de colunas
    # de tabela em V-13 (H0037-IMPL-QAPP5-002): o contrato nao define um
    # catalogo literal fechado de valores de ``campo``, mas define onde estao os
    # campos validos — na estrutura declarada. ``nivel`` e validado contra
    # ``niveis_por_id`` (chaves do nivel); ``campo`` e validado contra os nomes
    # de campos de conteudo de todos os niveis. Nao inventa catalogo novo:
    # reaproveita exclusivamente o que ``formato.niveis`` declarou.
    _campos_validos_por_no = set()
    for _nivel_campo in niveis_por_id.values():
        _cont = _nivel_campo.get("conteudo")
        if isinstance(_cont, str) and _cont.strip() != "":
            _campos_validos_por_no.add(_cont)
        elif isinstance(_cont, dict):
            for _chave_cont in ("nome", "valor"):
                _nome_cont = _cont.get(_chave_cont)
                if isinstance(_nome_cont, str) and _nome_cont.strip() != "":
                    _campos_validos_por_no.add(_nome_cont)

    # --- Validacoes H-0037 / ADR-0028 (V-01 a V-15) ---

    # V-01: tabela sem cabecalho semanticamente reconhecivel.
    # O cabecalho deve ser uma lista contendo ao menos uma coluna valida. Nao
    # basta que a lista seja nao vazia: cada entrada deve satisfazer a forma
    # contratual de coluna. Uma coluna e estruturalmente reconhecivel quando e:
    #   - uma string nao vazia (cabecalho simples), ou
    #   - um objeto declarando origem/rotulo (campos minimos: 'titulo' para
    #     rotulo, ou 'nivel'/'campo' para origem - a forma verificada por V-14).
    # Uma lista sem nenhuma coluna reconhecivel (vazia, entradas nulas, tipos
    # incorretos, objetos sem os campos minimos) e rejeitada por V-01. A
    # distincao entre V-01 e V-14: V-01 cobre ausencia total de coluna
    # reconhecivel; V-14 cobre coluna reconhecivel sem origem.
    if apresentacao == "tabela":
        bloco_tabela = formato.get("tabela")
        cabecalho_tb = (
            bloco_tabela.get("cabecalho") if isinstance(bloco_tabela, dict) else None
        )
        if not isinstance(cabecalho_tb, list):
            raise TelaEstruturaInvalida(
                "{0}: V-01: apresentacao 'tabela' exige formato.tabela.cabecalho "
                "como lista de colunas".format(origem)
            )
        if not any(_coluna_reconhecivel(c) for c in cabecalho_tb):
            raise TelaEstruturaInvalida(
                "{0}: V-01: apresentacao 'tabela' exige formato.tabela.cabecalho "
                "com ao menos uma coluna semanticamente valida".format(origem)
            )

    # V-02: referencia a nivel filho inexistente em formato.niveis[].filhos.
    for nivel in niveis:
        id_nivel = nivel.get("id", "?")
        if "filhos" in nivel and isinstance(nivel["filhos"], list):
            for id_filho in nivel["filhos"]:
                if not isinstance(id_filho, str) or id_filho == "":
                    raise TelaEstruturaInvalida(
                        "{0}: V-02: nivel {1!r}.filhos contem entrada "
                        "nao-string ou vazia".format(origem, id_nivel)
                    )
                if id_filho not in niveis_por_id:
                    raise TelaEstruturaInvalida(
                        "{0}: V-02: nivel {1!r}.filhos referencia nivel filho "
                        "inexistente: {2!r}".format(origem, id_nivel, id_filho)
                    )

    # V-03: multiplas raizes na hierarquia de niveis (quando filhos declarados).
    _niveis_filhos_fmt = set()
    _tem_filhos_fmt = False
    for nivel in niveis:
        _f = nivel.get("filhos")
        if isinstance(_f, list):
            _tem_filhos_fmt = True
            for _id_f in _f:
                if isinstance(_id_f, str):
                    _niveis_filhos_fmt.add(_id_f)
    if _tem_filhos_fmt:
        _raizes = [
            n.get("id") for n in niveis
            if isinstance(n.get("id"), str)
            and n.get("id") not in _niveis_filhos_fmt
        ]
        if len(_raizes) > 1:
            raise TelaEstruturaInvalida(
                "{0}: V-03: hierarquia de niveis tem {1} raizes ({2!r}); "
                "deve haver exatamente uma raiz quando filhos sao "
                "declarados".format(origem, len(_raizes), _raizes)
            )

    # V-07: medidas negativas em formato.espacamento.
    _esp_fmt = formato.get("espacamento")
    if isinstance(_esp_fmt, dict):
        for _nome_mc, _val_mc in _esp_fmt.items():
            if isinstance(_val_mc, (int, float)) and _val_mc < 0:
                raise TelaEstruturaInvalida(
                    "{0}: V-07: medida negativa em formato.espacamento.{1}: "
                    "{2}".format(origem, _nome_mc, _val_mc)
                )

    # V-08: largura maxima inferior a minima em colunas de tabela.
    if apresentacao == "tabela":
        _bloco_tab_v8 = formato.get("tabela")
        _colunas_v8 = (
            _bloco_tab_v8.get("colunas", [])
            if isinstance(_bloco_tab_v8, dict) else []
        )
        if isinstance(_colunas_v8, list):
            for _i_col, _col in enumerate(_colunas_v8):
                if isinstance(_col, dict):
                    _lm = _col.get("largura_minima")
                    _lx = _col.get("largura_maxima")
                    if (
                        isinstance(_lm, (int, float))
                        and isinstance(_lx, (int, float))
                        and _lx < _lm
                    ):
                        raise TelaEstruturaInvalida(
                            "{0}: V-08: coluna[{1}]: largura_maxima ({2}) "
                            "inferior a largura_minima ({3})".format(
                                origem, _i_col, _lx, _lm
                            )
                        )

    # V-09: modo nao verboso configurado para mais de uma linha.
    _excesso_fmt = formato.get("excesso")
    if isinstance(_excesso_fmt, dict):
        _linhas_nv = _excesso_fmt.get("linhas_nao_verboso")
        if isinstance(_linhas_nv, int) and _linhas_nv > 1:
            raise TelaEstruturaInvalida(
                "{0}: V-09: formato.excesso.linhas_nao_verboso={1}; modo "
                "nao verboso deve ocupar exatamente uma linha".format(
                    origem, _linhas_nv
                )
            )

    # V-10: modo verboso sem regra de alinhamento da continuacao.
    if isinstance(_excesso_fmt, dict):
        _verboso_cfg = _excesso_fmt.get("verboso")
        if isinstance(_verboso_cfg, dict) and "continuacao" not in _verboso_cfg:
            raise TelaEstruturaInvalida(
                "{0}: V-10: formato.excesso.verboso declarado sem campo "
                "'continuacao' (regra de alinhamento obrigatoria)".format(origem)
            )

    # V-11: justificacao sem escopo em formato.alinhamento.
    _alin_fmt = formato.get("alinhamento")
    if isinstance(_alin_fmt, dict):
        if (
            _alin_fmt.get("tipo") == "justificado"
            and "escopo" not in _alin_fmt
        ):
            raise TelaEstruturaInvalida(
                "{0}: V-11: formato.alinhamento.tipo='justificado' sem campo "
                "'escopo' obrigatorio".format(origem)
            )

    # V-12: designador composto (decimal_composto) sem ancestral declarado.
    # Nivel com decimal_composto nao pode aparecer como no raiz nos dados.
    for _no_raiz in dados:
        _nivel_ref = _no_raiz.get("nivel") if isinstance(_no_raiz, dict) else None
        if _nivel_ref in niveis_por_id:
            _nivel_dec = niveis_por_id[_nivel_ref]
            if _nivel_dec.get("designador", {}).get("tipo") == "decimal_composto":
                raise TelaEstruturaInvalida(
                    "{0}: V-12: no raiz {1!r} usa nivel {2!r} com designador "
                    "'decimal_composto' que requer ancestral; designador "
                    "composto invalido em no raiz dos dados".format(
                        origem,
                        _no_raiz.get("id") if isinstance(_no_raiz, dict) else "?",
                        _nivel_ref,
                    )
                )

    # V-13: dados incompativeis com a estrutura declarada.
    # Coberto pelas validacoes 12-17 em _validar_no_conteudo (executadas acima).

    # V-14: coluna de tabela sem nivel ou campo de origem.
    if apresentacao == "tabela":
        _bloco_tab_v14 = formato.get("tabela")
        _colunas_v14 = (
            _bloco_tab_v14.get("colunas", [])
            if isinstance(_bloco_tab_v14, dict) else []
        )
        if isinstance(_colunas_v14, list):
            for _i_col, _col in enumerate(_colunas_v14):
                if isinstance(_col, dict):
                    _nv = _col.get("nivel") if "nivel" in _col else None
                    _cp = _col.get("campo") if "campo" in _col else None
                    _nivel_ok = (
                        "nivel" in _col
                        and isinstance(_nv, str)
                        and _nv.strip() != ""
                    )
                    _campo_ok = (
                        "campo" in _col
                        and isinstance(_cp, str)
                        and _cp.strip() != ""
                    )
                    if not _nivel_ok and not _campo_ok:
                        raise TelaEstruturaInvalida(
                            "{0}: V-14: coluna[{1}] de tabela sem campo "
                            "'nivel' ou 'campo' de origem valido".format(
                                origem, _i_col
                            )
                        )
                    # V-13: nivel declarado mas incompativel com a estrutura.
                    if _nivel_ok and _nv not in niveis_por_id:
                        raise TelaEstruturaInvalida(
                            "{0}: V-13: coluna[{1}] referencia nivel {2!r} "
                            "nao declarado em formato.niveis; nivel de coluna "
                            "incompativel com a estrutura "
                            "declarada".format(origem, _i_col, _nv)
                        )
                    # V-13 por campo (H0037-IMPL-QAPP5-002): campo declarado
                    # mas incompativel com a estrutura. O contrato nao define um
                    # catalogo literal de valores de ``campo`` (V-14 exige apenas
                    # presenca de string nao-vazia); mas define onde estao os
                    # campos validos — em ``formato.niveis[].conteudo``
                    # (contrato_json_console.md §12.3): o campo de texto do no
                    # (para ``container``/``conteudo``) ou os campos ``nome`` e
                    # ``valor`` (para ``nome_valor``). ``campo`` e validado contra
                    # esse conjunto estrutural, distinguindo:
                    #   - campo ausente/nulo/vazio/whitespace -> V-14 (origem sem
                    #     valor semantico, ja tratado acima);
                    #   - campo declarado mas inexistente na estrutura -> V-13
                    #     (origem declarada mas incompativel).
                    if _campo_ok and _cp not in _campos_validos_por_no:
                        raise TelaEstruturaInvalida(
                            "{0}: V-13: coluna[{1}] referencia campo {2!r} "
                            "nao declarado em formato.niveis[].conteudo; campo "
                            "de coluna incompativel com a estrutura "
                            "declarada".format(origem, _i_col, _cp)
                        )

    # V-15: condicao excepcional sem politica explicita declarada.
    # politica_modo, modo_inicial ou excesso.modo (legado) no documento externo
    # sao invalidos; campos de politica de modo pertencem ao JSON estrutural
    # da tela (ADR-0028 D23).
    _campos_politica = {"politica_modo", "modo_inicial", "modo"}
    if isinstance(_excesso_fmt, dict):
        _campos_encontrados = _campos_politica & _excesso_fmt.keys()
        if _campos_encontrados:
            raise TelaEstruturaInvalida(
                "{0}: V-15: campo(s) de politica de modo proibido(s) em "
                "formato.excesso do documento externo: {1!r}; politicas de "
                "modo pertencem ao JSON estrutural da tela "
                "(ADR-0028 D23)".format(origem, sorted(_campos_encontrados))
            )
    if "politica_modo" in documento:
        raise TelaEstruturaInvalida(
            "{0}: V-15: campo 'politica_modo' proibido na raiz do documento "
            "externo; politicas de modo pertencem ao JSON estrutural da "
            "tela".format(origem)
        )
    if "modo_inicial" in documento:
        raise TelaEstruturaInvalida(
            "{0}: V-15: campo 'modo_inicial' proibido na raiz do documento "
            "externo; modos iniciais pertencem ao JSON estrutural da "
            "tela".format(origem)
        )

    return documento


def resolver_caminho_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None):
    """Compoe o caminho canonico do documento externo (mesma formula da carga)."""
    base = _para_base(caminho_base)
    if raiz_telas is None:
        raiz_telas = os.path.join("config", "telas")
    return base / os.path.join(raiz_telas, id_conteudo + ".json")


def aplicar_filho_default_no_documento(documento, mapa_candidato):
    """Devolve copia profunda com ``filho_default`` atualizado so onde diverge."""
    copia = copy.deepcopy(documento)
    candidatos = mapa_candidato or {}

    def _aplicar(nos):
        for no in nos or ():
            if not isinstance(no, dict):
                continue
            filhos = no.get("filhos")
            if isinstance(filhos, list):
                no_id = no.get("id")
                if (
                    no_id in candidatos
                    and no.get("filho_default") != candidatos[no_id]
                ):
                    no["filho_default"] = candidatos[no_id]
                _aplicar(filhos)

    _aplicar(copia.get("dados") or [])
    return copia


def persistir_conteudo_externo(documento, caminho_destino):
    """Persiste o documento com substituicao atomica no destino dado."""
    if caminho_destino is None:
        raise TelaEstruturaInvalida("Destino de persistencia deve ser fornecido")
    destino = os.fspath(caminho_destino)
    if not destino:
        raise TelaEstruturaInvalida("Destino de persistencia nao pode ser vazio")
    if not isinstance(documento, dict):
        raise TelaEstruturaInvalida(
            "Documento externo a persistir nao e objeto"
        )

    temporario = None
    try:
        diretorio = os.path.dirname(os.path.abspath(destino))
        os.makedirs(diretorio, exist_ok=True)
        nome = os.path.basename(destino)
        fd, temporario = tempfile.mkstemp(
            prefix=".{0}.".format(nome), suffix=".tmp", dir=diretorio
        )
        with os.fdopen(fd, "w", encoding="utf-8") as arquivo:
            json.dump(
                documento,
                arquivo,
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, destino)
        temporario = None
    except (OSError, TypeError, ValueError) as exc:
        raise TelaEstruturaInvalida(
            "Falha ao persistir conteudo externo em {0}: {1}".format(
                destino, exc
            )
        ) from exc
    finally:
        if temporario is not None:
            try:
                os.unlink(temporario)
            except OSError:
                pass
    return destino


def carregar_conteudo_externo(
    caminho_base, id_conteudo, raiz_telas=None, caminho_arquivo=None
):
    """Carrega, decodifica e valida um documento externo de conteudo.

    Parametros analogos a ``carregar_tela``: ``caminho_base`` (None usa a raiz
    do repositorio), ``id_conteudo`` (nome base do arquivo, sem extensao) e
    ``raiz_telas`` (diretorio relativo; None usa ``config/telas``; a
    demonstracao passa ``config/telas/demo``). ``caminho_arquivo``, quando
    fornecido, substitui a composicao canonica; ``id_conteudo`` permanece
    para mensagens.

    Devolve o documento validado (dict) como representacao semantica. O
    consumidor (modelo) constroi a representacao tipada; o renderizador calcula
    a geometria. Este loader NAO abre o JSON estrutural, NAO vincula tela e
    conteudo (responsabilidade do ``demo.py``), NAO calcula geometria e NAO
    infere hierarquia.

    Lanca: TelaArquivoNaoEncontrado, TelaJsonInvalido,
    TelaCampoObrigatorioAusente, TelaEstruturaInvalida.
    """
    if not isinstance(id_conteudo, str) or not id_conteudo:
        raise TelaCampoObrigatorioAusente(campo="id_conteudo (documento externo)")

    if caminho_arquivo is None:
        caminho_arquivo = resolver_caminho_conteudo_externo(
            caminho_base, id_conteudo, raiz_telas
        )
    else:
        from pathlib import Path
        caminho_arquivo = Path(caminho_arquivo)

    if raiz_telas is None:
        raiz_telas = os.path.join("config", "telas")
    caminho_relativo = os.path.join(raiz_telas, id_conteudo + ".json")

    if not caminho_arquivo.is_file():
        raise TelaArquivoNaoEncontrado(
            "Documento externo de conteudo nao encontrado: {0}".format(
                caminho_relativo
            )
        )

    try:
        texto = caminho_arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        raise TelaArquivoNaoEncontrado(
            "Documento externo de conteudo nao encontrado: {0} ({1})".format(
                caminho_relativo, exc
            )
        )

    try:
        documento = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise TelaJsonInvalido(
            "JSON invalido em documento externo: {0} - {1}".format(
                caminho_relativo, exc
            )
        )

    validar_conteudo_externo(documento, origem=caminho_relativo)
    return documento
