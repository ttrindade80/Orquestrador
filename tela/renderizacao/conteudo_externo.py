"""Apresentações de conteúdo externo."""

from tela.renderizacao.designadores import _texto_designador, _texto_no_conteudo
from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.composicao_textual import compor_texto
from tela.renderizacao.texto_ansi import (
    _largura_sem_ansi,
    _ljust_sem_ansi,
)


def _campo_no(no, nome, padrao=None):
    campos = getattr(no, "campos", {})
    if not isinstance(campos, dict):
        return padrao
    return campos.get(nome, padrao)


def _no_navegavel(no):
    return _campo_no(no, "navegavel", True) is not False


def _no_selecionavel(no):
    return bool(_campo_no(no, "selecionavel", False)) and _no_navegavel(no)

def _linhas_conteudo_externo(
    conteudo, content_w, verboso=False, ramos_fechados=None,
    no_corrente_id=None, indicador=None, indicador_off=None,
    selecoes=None, incluir_selecao=False, incluido_on="●", incluido_off="○",
):
    """Despacha o conteudo externo para a apresentacao declarada (H-0036).

    Produz a lista de linhas de conteudo da caixa do console. As tres
    apresentacoes sao obrigatorias e provadas. O truncamento a ``content_w`` e
    aplicado pelo envelope ``_caixa`` (calculo do renderizador), preservando o
    texto semantico integral neste nivel.
    """
    apresentacao = getattr(conteudo, "apresentacao", None)
    if apresentacao == "hierarquia":
        return _linhas_apresentacao_hierarquia(
            conteudo, content_w, verboso,
            ramos_fechados=ramos_fechados,
            no_corrente_id=no_corrente_id,
            indicador=indicador,
            indicador_off=indicador_off,
            selecoes=selecoes,
            incluir_selecao=incluir_selecao,
            incluido_on=incluido_on,
            incluido_off=incluido_off,
        )
    if apresentacao == "tabela":
        return _linhas_apresentacao_tabela(conteudo, content_w, verboso)
    if apresentacao == "conjuntos_campos":
        return _linhas_apresentacao_conjuntos(conteudo, content_w, verboso)
    raise RenderizadorErro(
        "apresentacao de conteudo externo desconhecida: {0!r}".format(apresentacao)
    )


def _truncar_com_marcador(texto, largura):
    """Trunca ``texto`` para caber em ``largura`` com marcador ``...`` (H-0037).

    Comportamento obrigatorio (H0037-MANUAL-001 / contrato_console.md §21.2):

    - texto que cabe integralmente: retornado sem alteracao e sem marcador;
    - texto que excede e ``largura >= 3``: ``texto[:largura-3] + "..."`` —
      resultado com exatamente ``largura`` caracteres, sufixo visivel ``...``;
    - texto que excede e ``largura < 3``: truncamento silencioso
      ``texto[:largura]`` (o marcador nao cabe; segue a regra vigente para
      areas menores que o comprimento do marcador).

    O marcador e aplicado no renderizador ANTES do envelope de caixa, de modo
    que o sufixo ``...`` faz parte do trecho visivel e nao e acrescentado
    depois de o texto já ter sido cortado pela borda. A linha resultante
    nunca excede ``largura``.
    """
    if largura is None:
        return texto
    if largura <= 0:
        return ""
    if len(texto) <= largura:
        return texto
    if largura < 3:
        return texto[:largura]
    return texto[:largura - 3] + "..."


def _linhas_apresentacao_hierarquia_com_mapa(
    conteudo, content_w=None, verboso=False, ramos_fechados=None,
    no_corrente_id=None, indicador=None, indicador_off=None,
    selecoes=None, incluir_selecao=False, incluido_on="●", incluido_off="○",
):
    """Calcula as linhas de cada nó da apresentação ``hierarquia``.

    Regra por modo (H0037-MANUAL-001 / contrato_console.md §21.2-21.3):

    - **Modo verboso**: TODO no (container ou folha) pode ocupar varias linhas
      fisicas. O conteudo e quebrado em palavras pela largura restante real
      (``content_w`` menos prefixo, recuo e designador), preservando o texto
      integral. As linhas de continuacao usam indentacao deterministica (mesma
      largura do prefixo) e NAO repetem o designador. Nenhum marcador
      artificial ``...`` e inserido e o renderizador nao depende do corte final
      do envelope da caixa para ajustar a largura.
    - **Modo nao verboso**: cada item ocupa exatamente uma linha fisica; o
      excedente recebe marcador ``...`` (``_truncar_com_marcador``).

    Em modo verboso, o alinhamento de coluna do nivel raiz (largura maxima dos
    designadores) e pre-calculado para estabilidade visual entre irmaos.
    """
    niveis = {n.id: n for n in conteudo.niveis}
    entradas = []
    ramos_fechados = set(ramos_fechados or ())
    possui_indicador = indicador is not None
    indicador_off = indicador_off if indicador_off is not None else " "
    selecoes = set(selecoes or ())
    possui_inclusao = bool(incluir_selecao)

    def prefixo_filho_sem_designador(
        no, prefixo_indicador, prefixo_inclusao, recuo, nivel, marcador
    ):
        """Compõe o prefixo ``ec → tg → tx`` quando o filho não tem designador.

        O caso e deliberadamente estreito: somente um nivel focalizavel com
        indicador ativo, sem designador, recebe esta composicao. Niveis com
        designador continuam no caminho generico anterior.
        """
        designador = nivel.designador if nivel is not None else None
        if (
            possui_indicador
            and nivel is not None
            and not designador
            and _no_selecionavel(no)
            and not marcador
        ):
            # H-0071: ordem vigente ``ec → tg → tx``. A indentação aplica-se
            # ao prefixo visual completo da linha filha; cursor e toggle
            # ocupam colunas distintas, estáveis com ou sem cursor.
            return "{0}{1}{2}".format(
                recuo, prefixo_indicador, prefixo_inclusao
            )
        return None

    # H-0037: pre-calcula largura maxima dos designadores do nivel raiz para
    # alinhamento de coluna estavel em modo verboso (dois niveis).
    largura_desig_raiz = 0
    if verboso and content_w is not None and conteudo.nos:
        ordinal_tmp = 0
        for no_tmp in conteudo.nos:
            ordinal_tmp += 1
            nivel_tmp = niveis.get(no_tmp.nivel)
            marc_tmp = _texto_designador(
                nivel_tmp.designador if nivel_tmp else {}, ordinal_tmp, []
            )
            largura_desig_raiz = max(largura_desig_raiz, len(marc_tmp))

    def recorrer(nos, profundidade, ancestrais):
        ordinal = 0
        for no in nos:
            ordinal += 1
            nivel = niveis.get(no.nivel)
            marcador = _texto_designador(
                nivel.designador if nivel else {}, ordinal, ancestrais
            )
            texto = _texto_no_conteudo(no, nivel)
            recuo = "  " * profundidade
            prefixo_indicador = ""
            if possui_indicador:
                simbolo = indicador if no.id == no_corrente_id else indicador_off
                prefixo_indicador = "{0} ".format(simbolo)
            prefixo_inclusao = ""
            if possui_inclusao:
                if _no_selecionavel(no):
                    simbolo_inclusao = (
                        incluido_on if no.id in selecoes else incluido_off
                    )
                else:
                    simbolo_inclusao = " "
                prefixo_inclusao = "{0} ".format(simbolo_inclusao)
            if verboso and content_w is not None:
                # Modo verboso (contrato_console.md §21.3): TODO no (container
                # ou folha) pode ocupar varias linhas fisicas. O conteudo e
                # quebrado em palavras pela largura restante real, preservando
                # o texto integral. As linhas de continuacao usam indentacao
                # deterministica (mesma largura do prefixo) e NAO repetem o
                # designador. Nenhum marcador artificial `...` e inserido.
                # Alinhamento de coluna no nivel raiz (H-0037 dois niveis).
                if profundidade == 0 and largura_desig_raiz > 0 and marcador:
                    marc_fmt = marcador.ljust(largura_desig_raiz)
                else:
                    marc_fmt = marcador
                prefixo_sem_designador = prefixo_filho_sem_designador(
                    no, prefixo_indicador, prefixo_inclusao, recuo,
                    nivel, marcador,
                )
                if prefixo_sem_designador is not None:
                    prefixo = prefixo_sem_designador
                else:
                    prefixo = "{0}{1}{2}".format(
                        prefixo_indicador + prefixo_inclusao + recuo,
                        marc_fmt,
                        " " if marc_fmt else "",
                    )
                largura_disp = max(10, content_w - len(prefixo))
                fragmentos = compor_texto(texto, largura_disp)
                linhas_do_no = ["{0}{1}".format(prefixo, fragmentos[0])]
                indent_cont = " " * len(prefixo)
                for frag in fragmentos[1:]:
                    linhas_do_no.append("{0}{1}".format(indent_cont, frag))
            else:
                prefixo_sem_designador = prefixo_filho_sem_designador(
                    no, prefixo_indicador, prefixo_inclusao, recuo,
                    nivel, marcador,
                )
                if prefixo_sem_designador is not None:
                    prefixo_linha = prefixo_sem_designador
                elif marcador:
                    prefixo_linha = "{0}{1}{2} ".format(
                        prefixo_indicador + prefixo_inclusao,
                        recuo, marcador
                    )
                else:
                    prefixo_linha = prefixo_indicador + prefixo_inclusao + recuo
                # H0037-MANUAL-001: em modo nao verboso, o conteudo aplicavel
                # ocupa exatamente uma linha fisica com marcador de truncamento
                # quando excede a largura disponivel (contrato_console.md §21.2).
                if content_w is not None:
                    largura_linha = content_w - len(prefixo_linha)
                    texto_visivel = _truncar_com_marcador(texto, largura_linha)
                else:
                    texto_visivel = texto
                linhas_do_no = ["{0}{1}".format(prefixo_linha, texto_visivel)]
            entradas.append({"id": no.id, "linhas": linhas_do_no})
            if no.filhos and no.id not in ramos_fechados:
                recorrer(no.filhos, profundidade + 1, ancestrais + [ordinal])

    recorrer(conteudo.nos, 0, [])
    return entradas


_MIN_UTIL_DOIS_NIVEIS_FILHO = 10


def _escolher_maior_que_cabe(minimo, maximo, cabe):
    """Maior valor em ``[minimo, maximo]`` para o qual ``cabe(valor)`` e True.

    ``cabe`` e monotonica decrescente (quanto maior o candidato, mais dificil
    caber): a busca para no primeiro candidato que nao cabe. Usa ``minimo``
    quando nem ele cabe (H-0072 §12/§17: "usa o maior valor que couber";
    sobra permanece a direita sem ampliacao artificial).
    """
    melhor = minimo
    for candidato in range(minimo, maximo + 1):
        if cabe(candidato):
            melhor = candidato
        else:
            break
    return melhor


def _linhas_dois_niveis_formatado_com_mapa(
    conteudo, config_filho, content_w=None, verboso=False,
    no_corrente_id=None, indicador=None, indicador_off=None,
    selecoes=None, incluir_selecao=False, incluido_on="●", incluido_off="○",
):
    """Formatacao generica dos filhos de ``dois_niveis_por_foco`` (H-0072).

    Aplica ``formato.dois_niveis_por_foco.filho`` (ADR-0047) — tabulacao,
    designador, apresentacao ``texto``/``tabela``, colunas e espacamento —
    exclusivamente aos nos de nivel FILHO. Os nos de nivel PAI preservam a
    mesma composicao ``ec``/``tg``/designador/texto ja vigente em
    ``_linhas_apresentacao_hierarquia_com_mapa`` (recuo zero — a tabulacao
    entre pai e filho e responsabilidade exclusiva deste handoff, nunca a
    formatacao do pai). Retorna a mesma forma de saida:
    ``[{"id":..., "linhas": [...]}, ...]`` em pre-ordem (pai, seus filhos, o
    proximo pai, ...), consumida identicamente por
    ``tela.renderizacao.console``.

    Ordem fisica obrigatoria por filho (H-0072 §13):
    ``tabulacao -> ec -> tg (quando existir) -> designador (quando existir)
    -> conteudo`` — a unidade inteira desloca-se junto, nunca so o texto.
    """
    niveis = {n.id: n for n in conteudo.niveis}
    possui_indicador = indicador is not None
    indicador_off_simb = indicador_off if indicador_off is not None else " "
    selecoes = set(selecoes or ())
    possui_inclusao = bool(incluir_selecao)
    ind_w = 2 if possui_indicador else 0
    tg_w = 2 if possui_inclusao else 0

    tabulacao_cfg = config_filho.get("tabulacao") or {}
    t_min = int(tabulacao_cfg.get("minimo", 0))
    t_max = int(tabulacao_cfg.get("maximo", t_min))
    designador_cfg = config_filho.get("designador") or {"tipo": "nenhum"}
    apresentacao_filho = config_filho.get("apresentacao", "texto")
    tabela_cfg = config_filho.get("tabela") or {}
    colunas_cfg = list(tabela_cfg.get("colunas") or [])
    espacamento_cfg = tabela_cfg.get("espacamento") or {}
    e_min = int(espacamento_cfg.get("minimo", 1))
    e_max = int(espacamento_cfg.get("maximo", e_min))

    def _prefixo_indicadores(no):
        prefixo_indicador = ""
        if possui_indicador:
            simbolo = indicador if no.id == no_corrente_id else indicador_off_simb
            prefixo_indicador = "{0} ".format(simbolo)
        prefixo_inclusao = ""
        if possui_inclusao:
            if _no_selecionavel(no):
                simbolo_inclusao = incluido_on if no.id in selecoes else incluido_off
            else:
                simbolo_inclusao = " "
            prefixo_inclusao = "{0} ".format(simbolo_inclusao)
        return prefixo_indicador, prefixo_inclusao

    # H-0072 §16 (alinhamento global): designador e colunas dos filhos sao
    # medidos sobre TODOS os filhos do console, nunca por pai isoladamente —
    # trocar o pai corrente nao pode deslocar horizontalmente as colunas.
    designadores_por_filho = {}
    designador_w = 0
    ordinal_pai = 0
    for pai in conteudo.nos:
        ordinal_pai += 1
        ordinal_filho = 0
        for filho in pai.filhos:
            ordinal_filho += 1
            texto_desig = _texto_designador(
                designador_cfg, ordinal_filho, [ordinal_pai]
            )
            designadores_por_filho[filho.id] = texto_desig
            designador_w = max(designador_w, len(texto_desig))

    larguras_col = []
    linhas_celulas_por_filho = {}
    if apresentacao_filho == "tabela" and colunas_cfg:
        larguras_col = [0] * len(colunas_cfg)
        for pai in conteudo.nos:
            for filho in pai.filhos:
                celulas = [
                    "{0}".format(filho.campos.get(col.get("campo"), ""))
                    for col in colunas_cfg
                ]
                linhas_celulas_por_filho[filho.id] = celulas
                for indice, texto_cel in enumerate(celulas):
                    larguras_col[indice] = max(
                        larguras_col[indice], _largura_sem_ansi(texto_cel)
                    )

    entradas = []
    ordinal_pai = 0
    for pai in conteudo.nos:
        ordinal_pai += 1
        nivel_pai = niveis.get(pai.nivel)
        marcador_pai = _texto_designador(
            nivel_pai.designador if nivel_pai else {}, ordinal_pai, []
        )
        texto_pai = _texto_no_conteudo(pai, nivel_pai)
        prefixo_indicador, prefixo_inclusao = _prefixo_indicadores(pai)
        if marcador_pai:
            prefixo_pai = "{0}{1}{2} ".format(
                prefixo_indicador, prefixo_inclusao, marcador_pai
            )
        else:
            prefixo_pai = prefixo_indicador + prefixo_inclusao
        if verboso and content_w is not None:
            largura_disp_pai = max(
                _MIN_UTIL_DOIS_NIVEIS_FILHO, content_w - len(prefixo_pai)
            )
            fragmentos_pai = compor_texto(texto_pai, largura_disp_pai)
            linhas_pai = ["{0}{1}".format(prefixo_pai, fragmentos_pai[0])]
            indent_pai = " " * len(prefixo_pai)
            for frag in fragmentos_pai[1:]:
                linhas_pai.append("{0}{1}".format(indent_pai, frag))
        else:
            if content_w is not None:
                texto_visivel_pai = _truncar_com_marcador(
                    texto_pai, max(0, content_w - len(prefixo_pai))
                )
            else:
                texto_visivel_pai = texto_pai
            linhas_pai = ["{0}{1}".format(prefixo_pai, texto_visivel_pai)]
        entradas.append({"id": pai.id, "linhas": linhas_pai})

        for filho in pai.filhos:
            texto_desig = designadores_por_filho[filho.id]
            desig_fmt = (
                texto_desig.ljust(designador_w) if designador_w else texto_desig
            )
            prefixo_indicador, prefixo_inclusao = _prefixo_indicadores(filho)

            # A tabulacao deve ser a maior que ainda permite a apresentacao
            # minima do proprio filho. O limite fixo de utilidade continua
            # protegendo texto curto; para tabelas, porem, a largura minima
            # real e a soma das colunas com o espacamento minimo. Sem essa
            # medida, a largura do terminal chegava ao calculo, mas a
            # tabulacao permanecia em 10 enquanto a tabela ja precisava
            # compactar para caber.
            nivel_filho = niveis.get(filho.nivel)
            texto_filho = _texto_no_conteudo(filho, nivel_filho)
            if apresentacao_filho == "tabela" and colunas_cfg:
                largura_minima_filho = (
                    sum(larguras_col)
                    + (len(colunas_cfg) - 1) * e_min
                )
            else:
                largura_minima_filho = max(
                    _MIN_UTIL_DOIS_NIVEIS_FILHO,
                    _largura_sem_ansi(texto_filho),
                )

            def _cabe_tabulacao(candidato, desig_fmt=desig_fmt):
                if content_w is None:
                    return True
                fixo = (
                    candidato + ind_w + tg_w + len(desig_fmt)
                    + (1 if desig_fmt else 0)
                )
                return (content_w - fixo) >= largura_minima_filho

            tabulacao_efetiva = _escolher_maior_que_cabe(
                t_min, t_max, _cabe_tabulacao
            )
            recuo = " " * tabulacao_efetiva
            desig_sep = "{0} ".format(desig_fmt) if desig_fmt else ""
            prefixo_filho = "{0}{1}{2}{3}".format(
                recuo, prefixo_indicador, prefixo_inclusao, desig_sep
            )
            largura_disponivel = (
                None if content_w is None
                else max(0, content_w - len(prefixo_filho))
            )

            if apresentacao_filho == "tabela" and colunas_cfg:
                celulas = linhas_celulas_por_filho[filho.id]
                n_col = len(celulas)

                def _cabe_espacamento(candidato):
                    if largura_disponivel is None:
                        return True
                    total = sum(larguras_col) + (n_col - 1) * candidato
                    return total <= largura_disponivel

                espacamento_efetivo = _escolher_maior_que_cabe(
                    e_min, e_max, _cabe_espacamento
                )
                sep = " " * espacamento_efetivo
                partes_fixas = [
                    _ljust_sem_ansi(celulas[i], larguras_col[i])
                    for i in range(n_col - 1)
                ]
                prefixo_ultima = sep.join(partes_fixas)
                if partes_fixas:
                    prefixo_ultima += sep
                ultima = celulas[n_col - 1]
                if largura_disponivel is not None:
                    largura_ultima = max(
                        1,
                        largura_disponivel - _largura_sem_ansi(prefixo_ultima),
                    )
                    if _largura_sem_ansi(ultima) <= largura_ultima:
                        fragmentos = [ultima]
                    else:
                        fragmentos = compor_texto(ultima, largura_ultima)
                else:
                    fragmentos = [ultima]
                linhas_filho = [
                    "{0}{1}{2}".format(
                        prefixo_filho, prefixo_ultima, fragmentos[0]
                    )
                ]
                indent_cont = " " * (
                    _largura_sem_ansi(prefixo_filho)
                    + _largura_sem_ansi(prefixo_ultima)
                )
                for frag in fragmentos[1:]:
                    linhas_filho.append("{0}{1}".format(indent_cont, frag))
            else:
                if verboso and largura_disponivel is not None:
                    largura_disp = max(
                        _MIN_UTIL_DOIS_NIVEIS_FILHO, largura_disponivel
                    )
                    fragmentos = compor_texto(texto_filho, largura_disp)
                    linhas_filho = [
                        "{0}{1}".format(prefixo_filho, fragmentos[0])
                    ]
                    indent_cont = " " * len(prefixo_filho)
                    for frag in fragmentos[1:]:
                        linhas_filho.append("{0}{1}".format(indent_cont, frag))
                else:
                    if largura_disponivel is not None:
                        texto_visivel = _truncar_com_marcador(
                            texto_filho, largura_disponivel
                        )
                    else:
                        texto_visivel = texto_filho
                    linhas_filho = [
                        "{0}{1}".format(prefixo_filho, texto_visivel)
                    ]
            entradas.append({"id": filho.id, "linhas": linhas_filho})

    return entradas


def _linhas_dois_niveis_formatado(
    conteudo, config_filho, content_w=None, verboso=False,
    no_corrente_id=None, indicador=None, indicador_off=None,
    selecoes=None, incluir_selecao=False, incluido_on="●", incluido_off="○",
):
    """Achata ``_linhas_dois_niveis_formatado_com_mapa`` em lista de linhas."""
    entradas = _linhas_dois_niveis_formatado_com_mapa(
        conteudo, config_filho, content_w, verboso,
        no_corrente_id=no_corrente_id, indicador=indicador,
        indicador_off=indicador_off, selecoes=selecoes,
        incluir_selecao=incluir_selecao, incluido_on=incluido_on,
        incluido_off=incluido_off,
    )
    return [linha for entrada in entradas for linha in entrada["linhas"]]


def _linhas_apresentacao_hierarquia(
    conteudo, content_w=None, verboso=False, ramos_fechados=None,
    no_corrente_id=None, indicador=None, indicador_off=None,
    selecoes=None, incluir_selecao=False, incluido_on="●", incluido_off="○",
):
    """Apresentacao ``hierarquia``: lista recuada com designadores por nivel."""
    entradas = _linhas_apresentacao_hierarquia_com_mapa(
        conteudo, content_w, verboso, ramos_fechados=ramos_fechados,
        no_corrente_id=no_corrente_id, indicador=indicador,
        indicador_off=indicador_off, selecoes=selecoes,
        incluir_selecao=incluir_selecao, incluido_on=incluido_on,
        incluido_off=incluido_off,
    )
    return [linha for entrada in entradas for linha in entrada["linhas"]]


def _linhas_apresentacao_tabela(conteudo, content_w, verboso=False):
    """Apresentacao ``tabela``: cabecalho e linhas com colunas alinhadas.

    Cada no folha vira uma linha. Quando ``formato.tabela.ancestrais`` e
    ``"repetir"``, os textos dos ancestrais containers sao repetidos como
    colunas iniciais de cada linha. As larguras de coluna sao calculadas pelo
    renderizador (nao vem do documento).
    """
    niveis = {n.id: n for n in conteudo.niveis}
    bloco = conteudo.formato.get("tabela", {}) if isinstance(conteudo.formato, dict) else {}
    cabecalho = list(bloco.get("cabecalho", []) or [])
    repetir = bloco.get("ancestrais") == "repetir"

    linhas_celulas = []

    def recorrer(nos, ancestrais_texto, ancestrais_ord):
        ordinal = 0
        for no in nos:
            ordinal += 1
            nivel = niveis.get(no.nivel)
            marcador = _texto_designador(
                nivel.designador if nivel else {}, ordinal, ancestrais_ord
            )
            texto = _texto_no_conteudo(no, nivel)
            if nivel is not None and nivel.tipo == "container":
                novo_texto = ancestrais_texto + [texto] if repetir else [texto]
                if no.filhos:
                    recorrer(no.filhos, novo_texto, ancestrais_ord + [ordinal])
                else:
                    linhas_celulas.append(
                        (ancestrais_texto if repetir else []) + [texto]
                    )
            else:
                prefixo = (ancestrais_texto if repetir else [])
                celula = ("{0} {1}".format(marcador, texto) if marcador else texto)
                # nome_valor produz duas colunas (nome | valor); demais, uma.
                if nivel is not None and nivel.tipo == "nome_valor":
                    campo_nome = nivel.conteudo.get("nome")
                    campo_valor = nivel.conteudo.get("valor")
                    nome = "{0}".format(no.campos.get(campo_nome, ""))
                    if marcador:
                        nome = "{0} {1}".format(marcador, nome)
                    valor = "{0}".format(no.campos.get(campo_valor, ""))
                    linhas_celulas.append(prefixo + [nome, valor])
                else:
                    linhas_celulas.append(prefixo + [celula])

    recorrer(conteudo.nos, [], [])

    # Numero de colunas = maximo entre cabecalho e linhas.
    n_col = max([len(cabecalho)] + [len(l) for l in linhas_celulas] + [0])
    if n_col == 0:
        return []
    matriz = []
    if cabecalho:
        matriz.append(cabecalho + [""] * (n_col - len(cabecalho)))
    for l in linhas_celulas:
        matriz.append(l + [""] * (n_col - len(l)))
    larguras = [
        max(len(str(linha[c])) for linha in matriz) for c in range(n_col)
    ]
    sep = "  "

    # H-0037: em modo verboso e com content_w disponivel, quebra a ultima
    # coluna de cada linha de dados (nao do cabecalho) para que o texto
    # completo seja exibido em multiplas linhas fisicas.
    if verboso and content_w is not None and n_col > 0:
        w_prefix = sum(larguras[c] for c in range(n_col - 1))
        if n_col > 1:
            w_prefix += (n_col - 1) * len(sep)
        w_ultima = max(10, content_w - w_prefix)
        linhas = []
        for idx, linha in enumerate(matriz):
            partes_fixas = [
                str(linha[c]).ljust(larguras[c]) for c in range(n_col - 1)
            ]
            prefixo_str = sep.join(partes_fixas) + (sep if partes_fixas else "")
            ultima_cel = str(linha[n_col - 1])
            if idx == 0 and cabecalho:
                # Cabecalho: linha unica sem quebra
                linhas.append((prefixo_str + ultima_cel).rstrip())
                regua = sep.join("-" * larguras[c] for c in range(n_col - 1))
                if partes_fixas:
                    regua += sep
                regua += "-" * larguras[n_col - 1]
                linhas.append(regua.rstrip())
            else:
                fragmentos = compor_texto(ultima_cel, w_ultima)
                linhas.append((prefixo_str + fragmentos[0]).rstrip())
                indent = " " * len(prefixo_str)
                for frag in fragmentos[1:]:
                    linhas.append((indent + frag).rstrip())
        return linhas

    linhas = []
    for idx, linha in enumerate(matriz):
        partes = [str(linha[c]).ljust(larguras[c]) for c in range(n_col)]
        linha_str = sep.join(partes).rstrip()
        # H0037-MANUAL-001: em modo nao verboso, cada linha da tabela que
        # excede a largura disponivel recebe marcador de truncamento `...`
        # (uma linha fisica por celula; contrato_console.md §21.2).
        if content_w is not None and len(linha_str) > content_w:
            linha_str = _truncar_com_marcador(linha_str, content_w)
        linhas.append(linha_str)
        if idx == 0 and cabecalho:
            # Regua sob o cabecalho (calculo do renderizador).
            regua = sep.join("-" * larguras[c] for c in range(n_col))
            regua_str = regua.rstrip()
            if content_w is not None and len(regua_str) > content_w:
                regua_str = _truncar_com_marcador(regua_str, content_w)
            linhas.append(regua_str)
    return linhas


_VALOR_CAMPO_AUSENTE_TEXTO = "indisponível"


def _texto_valor_campo(valor_bruto):
    """Texto visivel do ``valor`` de um campo ``nome_valor`` (H0043-P01).

    ``None`` representa ausencia semantica de conteudo (ex.: resultado_json
    sem documento) e e exibido como texto fixo; qualquer outro valor
    (incluindo falsy nao-None, como ``0``, ``False`` ou string vazia) segue a
    formatacao padrao, sem tratamento especial.

    QA-PATCH-H0044-P01: cada campo ``nome_valor`` ocupa exatamente uma linha
    visivel. Canais capturados do executor (``stdout``/``stderr``) e o proprio
    ``resultado_json`` bruto podem trazer ``\\n`` a direita ou embutidos (ex.:
    ``"ERRO: falha operacional sintetica.\\n"``). Sem normalizacao, o ``\\n``
    vira uma quebra de linha fisica fantasma dentro de uma unica "linha" de
    conteudo, inflando a contagem vertical em uma unidade e disparando
    indevidamente o quadro minimo "terminal pequeno demais" em qualquer altura.
    O espaco em branco e normalizado para um unico espaco (cada campo segue
    sendo uma linha); o valor bruto do envelope permanece intocado (preservacao
    literal de ``resultado_bruto`` e testada no dominio do resultado).
    """
    if valor_bruto is None:
        return _VALOR_CAMPO_AUSENTE_TEXTO
    return " ".join("{0}".format(valor_bruto).split())


def _linhas_apresentacao_conjuntos(conteudo, content_w=None, verboso=False):
    """Apresentacao ``conjuntos_campos``: conjuntos com pares nome-valor.

    Cada container e um conjunto (com designador e titulo); seus filhos
    ``nome_valor`` sao exibidos como ``"nome<sep> valor"`` com os nomes
    justificados por conjunto (``formato.campos.justificar_nomes`` /
    ``escopo_justificacao``). O separador vem de ``formato.campos.separador``.
    ``valor is None`` (ausencia semantica de conteudo) e exibido como
    "indisponível" (H0043-P01 / QA-IMPL-H0043-001); demais valores falsy
    (``0``, ``False``, ``""``) permanecem sem tratamento especial.
    """
    niveis = {n.id: n for n in conteudo.niveis}
    campos_cfg = conteudo.formato.get("campos", {}) if isinstance(conteudo.formato, dict) else {}
    separador = campos_cfg.get("separador", ":")
    justificar = campos_cfg.get("justificar_nomes", False)
    linhas = []

    def largura_nomes(nos):
        maior = 0
        for no in nos:
            nivel = niveis.get(no.nivel)
            if nivel is not None and nivel.tipo == "nome_valor":
                campo_nome = nivel.conteudo.get("nome")
                maior = max(maior, len("{0}".format(no.campos.get(campo_nome, ""))))
        return maior

    def recorrer(nos, profundidade, ancestrais):
        ordinal = 0
        largura_local = largura_nomes(nos) if justificar else 0
        for no in nos:
            ordinal += 1
            nivel = niveis.get(no.nivel)
            recuo = "  " * profundidade
            if nivel is not None and nivel.tipo == "nome_valor":
                campo_nome = nivel.conteudo.get("nome")
                campo_valor = nivel.conteudo.get("valor")
                nome = "{0}".format(no.campos.get(campo_nome, ""))
                valor = _texto_valor_campo(no.campos.get(campo_valor, ""))
                nome_fmt = nome.ljust(largura_local) if justificar else nome
                prefixo_linha = "{0}{1}{2} ".format(recuo, nome_fmt, separador)
                if verboso and content_w is not None:
                    largura_val = max(10, content_w - len(prefixo_linha))
                    fragmentos = compor_texto(valor, largura_val)
                    linhas.append("{0}{1}".format(prefixo_linha, fragmentos[0]))
                    indent_val = " " * len(prefixo_linha)
                    for frag in fragmentos[1:]:
                        linhas.append("{0}{1}".format(indent_val, frag))
                else:
                    # H0037-MANUAL-001: modo nao verboso ocupa uma linha fisica
                    # com marcador de truncamento quando excede a largura.
                    if content_w is not None:
                        largura_val = max(0, content_w - len(prefixo_linha))
                        valor = _truncar_com_marcador(valor, largura_val)
                    linhas.append("{0}{1}".format(prefixo_linha, valor))
            else:
                marcador = _texto_designador(
                    nivel.designador if nivel else {}, ordinal, ancestrais
                )
                texto = _texto_no_conteudo(no, nivel)
                if marcador:
                    prefixo_linha = "{0}{1} ".format(recuo, marcador)
                else:
                    prefixo_linha = recuo
                # H0037-MANUAL-001: modo nao verboso com marcador de truncamento.
                if content_w is not None:
                    largura_linha = content_w - len(prefixo_linha)
                    texto_visivel = _truncar_com_marcador(texto, largura_linha)
                else:
                    texto_visivel = texto
                linhas.append("{0}{1}".format(prefixo_linha, texto_visivel))
            if no.filhos:
                recorrer(no.filhos, profundidade + 1, ancestrais + [ordinal])

    recorrer(conteudo.nos, 0, [])
    return linhas


def _participantes_de_conteudo_externo(conteudo):
    """Achata o conteudo externo em participantes para a distribuicao matricial.

    H-0035/H-0036: os cenarios ``h0035_console_*`` preservam a distribuicao
    matricial (ADR-0025) enquanto seus dados passam a vir do documento externo.
    Cada no vira um participante (texto de identidade com designador, quando
    houver), em ordem de documento; a hierarquia e achatada em sequencia (a
    grade so muda a celula, nunca a ordem).
    """
    niveis = {n.id: n for n in conteudo.niveis}
    participantes = []

    def recorrer(nos, ancestrais):
        ordinal = 0
        for no in nos:
            ordinal += 1
            nivel = niveis.get(no.nivel)
            marcador = _texto_designador(
                nivel.designador if nivel else {}, ordinal, ancestrais
            )
            texto = _texto_no_conteudo(no, nivel)
            if marcador:
                participantes.append("{0} {1}".format(marcador, texto))
            else:
                participantes.append(texto)
            if no.filhos:
                recorrer(no.filhos, ancestrais + [ordinal])

    recorrer(conteudo.nos, [])
    return participantes
