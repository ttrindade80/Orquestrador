"""Orquestração de alto nível da renderização de telas."""

from tela.modelo import ModeloTela
from tela.renderizacao.barra_menus import _linhas_barra
from tela.renderizacao.composicao_corpo import _renderizar_container
from tela.renderizacao.contexto_execucao import (
    _preparar_contexto_navegacao,
    _quadro_minimo_lancador_esta_ativo,
    _reiniciar_quadro_minimo_lancador,
)
from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.geometria_caixa import (
    _LABEL_BARRA,
    TOTAL_WIDTH,
    _borda_de_estilo,
    _caixa,
    _contar_linhas,
)
from tela.renderizacao.popup import sobrepor_no_corpo


def _quadro_minimo_global(total_w, altura):
    """Gera o quadro mínimo canônico global (ADR-0017 seção 9 / ADR-0023).

    Reutilizado tanto para terminal fisicamente pequeno (ADR-0017) quanto para
    inviabilidade da área alocada ao ``lancador`` (ADR-0023): em ambos os casos
    o quadro mínimo substitui integralmente toda a tela normal. Comunica
    inequivocamente "terminal pequeno demais", adequa-se à largura disponível,
    não gera scroll nem overflow, não cria mensagem local do ``lancador`` e é
    substituído automaticamente pela tela normal quando o espaço retorna.

    ``altura`` pode ser ``None``: neste caso, o quadro usa apenas a linha de
    aviso (comportamento determinístico sem ocupação vertical).
    """
    if total_w >= 23:
        msg = "terminal pequeno demais"
    elif total_w >= 9:
        msg = "tela peq."
    else:
        msg = ""
    linha_aviso = msg[:total_w].ljust(total_w)
    linha_vazia = " " * total_w
    if altura is None:
        return linha_aviso + "\n"
    linhas = [linha_aviso] + [linha_vazia] * (altura - 1)
    return "\n".join(linhas) + "\n"

def _geometria_por_console(
    modelo, estilo, largura, altura, verboso=False,
    foco_console=None, cursores=None, lista_foco=None,
    selecoes=None, chips_destacados=None, executar_disponivel=None,
    paginas_atuais=None,
):
    """Autoridade unica RECURSIVA de geometria por console (H-0045-P07).

    Reproduz EXATAMENTE o mesmo calculo de ``l_cab``/``l_barra``/
    ``l_corpo_disponivel`` de ``renderizar_tela`` (mesmo contexto de
    navegacao via ``_preparar_contexto_navegacao``, portanto o mesmo
    ``l_barra``) e entao delega a particao do corpo a
    ``_renderizar_container`` -- a MESMA funcao que ``renderizar_tela`` usa
    para montar o corpo real, incluindo a recursao em ``grupo`` e
    ``estrutura: matriz`` ja implementada por
    ``_renderizar_container_vertical``/``_renderizar_container_horizontal``/
    ``_renderizar_container_matriz`` (H-0027/H-0035). Nenhuma regra de
    particionamento/distribuicao e reimplementada aqui: a geometria e
    coletada como efeito colateral do proprio render, via o parametro
    ``registro_geometria`` (ver docstrings de ``_renderizar_container`` e de
    ``_caixa_de_elemento``), por isso nunca diverge do quadro que
    ``renderizar_tela`` produziria para a mesma largura/altura/estado.

    QA-H0045-P06-001: ate este patch, a autoridade so calculava os elementos
    DIRETOS de ``corpo.elementos[]``, documentando explicitamente que "nao
    recursiona em grupo/estrutura: matriz". Consoles dentro de um grupo
    permitido (H-0027) nunca apareciam no mapa resultante, e o wrapper
    ``geometria_console`` reagia a essa ausencia devolvendo a PRIMEIRA
    geometria do mapa (``next(iter(...))``) -- a geometria de outro elemento
    do corpo raiz, nunca a do console solicitado. Agora a recursao cobre
    TODOS os niveis de grupo permitidos (H-0027 D5/D6: ate 3 niveis) e todas
    as celulas de ``estrutura: matriz``, exatamente como o renderer as
    percorre.

    Cada entrada e mapeada por ``console.id`` (chave inequivoca -- unicidade
    garantida pelo loader, ``_validar_unicidade_ids_consoles``). Um console
    so recebe entrada quando o container pai lhe atribui uma cota FISICA
    concreta (``altura_alvo`` resolvido, nao ``None``); quando o console so
    seria desenhado com altura natural (orientada por conteudo, fora de
    qualquer particionamento fixo), nenhuma entrada e registrada -- essa
    geometria nao e uma capacidade de paginacao estavel (ausencia explicita,
    nao uma aproximacao).

    Retorna ``{}`` quando a geometria e insuficiente para cabecalho +
    barra_de_menus, quando o corpo esta vazio, ou quando a composicao
    declarada e invalida (``RenderizadorErro`` -- o mesmo caso em que
    ``renderizar_tela`` rejeitaria a tela e o render seguinte substituira a
    tela pelo quadro minimo); o chamador deve preservar pagina/estado
    correntes nesse caso.
    """
    borda = _borda_de_estilo(estilo)
    total_w = TOTAL_WIDTH if largura is None else largura
    inner_w = total_w - 2
    content_w = total_w - 3
    label_max = total_w - 4

    _preparar_contexto_navegacao(
        estilo, largura, altura, verboso,
        foco_console=foco_console, cursores=cursores, lista_foco=lista_foco,
        largura_navegacao=largura, selecoes=selecoes,
        chips_destacados=chips_destacados,
        executar_disponivel=executar_disponivel,
        paginas_atuais=paginas_atuais, modelo=modelo,
    )

    titulo = modelo.cabecalho["titulo"]
    descricao = modelo.cabecalho["descricao"]
    apresentacao = modelo.cabecalho["apresentacao"]
    caixa_cab = _caixa(
        titulo, [descricao], borda, inner_w, content_w, label_max,
        apresentacao=apresentacao,
    )
    l_cab = _contar_linhas(caixa_cab)

    linhas_barra = _linhas_barra(modelo.barra_de_menus, estilo, content_w)
    l_barra = len(linhas_barra) + 2

    if altura is None or l_cab + l_barra > altura:
        return {}
    l_corpo_disponivel = altura - l_cab - l_barra

    arranjo_corpo = modelo.corpo.arranjo
    elementos = modelo.corpo.elementos
    if not elementos:
        return {}

    resultado = {}
    try:
        _renderizar_container(
            arranjo_corpo, modelo.corpo.distribuicao, elementos, borda,
            total_w, l_corpo_disponivel, verboso=verboso,
            registro_geometria=resultado,
        )
    except RenderizadorErro:
        return {}
    return resultado


def geometria_console(
    modelo, estilo, largura, altura, verboso=False,
    console=None, foco_console=None, cursores=None, lista_foco=None,
    selecoes=None, chips_destacados=None, executar_disponivel=None,
    paginas_atuais=None,
):
    """Geometria real (``largura``/``altura_interna``) de UM console (H-0045-P07).

    Wrapper de ``_geometria_por_console`` que seleciona a entrada
    correspondente a ``console`` por ``id``. Retorna ``{"largura": int,
    "altura_interna": int}`` quando -- e somente quando -- ``console`` e um
    console real do modelo com geometria fisica resolvida pela autoridade
    recursiva. Retorna ``None`` em qualquer outro caso: geometria
    globalmente insuficiente, ``console`` ausente/``None``, ou
    ``console.id`` nao presente no mapa (console que nao existe no modelo,
    ou cuja caixa e desenhada com altura natural sem cota fisica estavel).

    QA-H0045-P06-001: ate este patch, ausencia de ``console.id`` no mapa
    produzia ``next(iter(geometria.values()))`` -- a geometria de QUALQUER
    outro elemento do corpo raiz, entregue silenciosamente para um console
    ausente ou para um console dentro de grupo (que nunca chegava a
    ``_geometria_por_console`` antes deste patch). Essa correspondencia
    silenciosa foi removida: nao ha mais fallback para "a primeira entrada
    calculada". Os chamadores (``demo._com_geometria_real_do_console``,
    ``demo._reconciliar_paginacao_apos_resize``) ja tratam ``None``
    preservando o estado corrente sem processar o comando de pagina/seta com
    geometria alheia (ver seus docstrings).

    Autoridade unica consumida por render (via
    ``_renderizar_container_horizontal``/``_renderizar_container_vertical``/
    ``_renderizar_container_matriz``), reconciliacao de resize e comandos de
    pagina/setas (``demo.processar_comando``) -- nenhum caminho interativo do
    H-0045 deve aproximar essa geometria por conta propria.
    """
    if console is None:
        return None
    geometria = _geometria_por_console(
        modelo, estilo, largura, altura, verboso,
        foco_console=foco_console, cursores=cursores, lista_foco=lista_foco,
        selecoes=selecoes, chips_destacados=chips_destacados,
        executar_disponivel=executar_disponivel, paginas_atuais=paginas_atuais,
    )
    if not geometria:
        return None
    console_id = getattr(console, "id", None)
    if console_id is None:
        return None
    return geometria.get(console_id)


def altura_interna_disponivel(
    modelo, estilo, largura, altura, verboso=False,
    console=None, foco_console=None, cursores=None, lista_foco=None,
    selecoes=None, chips_destacados=None, executar_disponivel=None,
    paginas_atuais=None,
):
    """Capacidade fisica vertical de paginacao de UM console (H-0045-P05/P06).

    Retrocompativel: wrapper de ``geometria_console`` que devolve apenas
    ``altura_interna`` (``int``) ou ``None``. Ver ``geometria_console`` e
    ``_geometria_por_console`` para a autoridade completa (inclui largura de
    coluna, necessaria em arranjo horizontal e agora tambem consumida pelo
    render real -- QA-H0045-P05-001/QA-H0045-P05-002).
    """
    geometria = geometria_console(
        modelo, estilo, largura, altura, verboso,
        console=console, foco_console=foco_console, cursores=cursores,
        lista_foco=lista_foco, selecoes=selecoes,
        chips_destacados=chips_destacados,
        executar_disponivel=executar_disponivel,
        paginas_atuais=paginas_atuais,
    )
    if geometria is None:
        return None
    return geometria["altura_interna"]


def renderizar_tela(
    modelo: ModeloTela,
    estilo: "EstiloResolvido",
    largura: int | None = None,
    altura: int | None = None,
    verboso: bool = False,
    foco_console=None,
    cursores=None,
    lista_foco=None,
    largura_navegacao=None,
    selecoes=None,
    chips_destacados=None,
    executar_disponivel=None,
    paginas_atuais=None,
    popup=None,
) -> str:
    """Renderiza ModeloTela como string visual declarativa (H-0010A).

    H-0039 / ADR-0030: os caracteres de borda e os delimitadores/capitalizacao
    dos chips vêm do ``EstiloResolvido`` carregado de ``config/estilo.json``
    via ``carregar_estilo``. O renderer nao abre ``config/estilo.json``,
    nao resolve preset, nao mantém catálogo visual proprio e nao aplica
    fallback -- consome exclusivamente o ``estilo`` recebido.

    Parametros:
        modelo: ModeloTela produzido por construir_modelo (H-0002) a
            partir do dict retornado por carregar_tela (H-0001).
        estilo: ``EstiloResolvido`` (tela.loader) carregado uma vez por
            sessao. Fonte unica de borda (7 campos), chip (5 campos) e
            indicadores materializados (6 campos). Argumento obrigatorio
            -- nao ha default: o renderer nunca decide borda autonomamente.
        largura: largura total (em caracteres Python) de cada linha
            nao-vazia da saida. Quando ``None`` (default), usa o fallback
            deterministico ``TOTAL_WIDTH = 42``. Quando fornecida, deriva
            ``inner_w = largura - 2``, ``content_w = largura - 3`` e
            ``label_max = largura - 4``. ``largura < 10`` tem comportamento
            indefinido neste ciclo (nao validado, nao tratado).
        altura: altura alvo (em linhas fisicas) da saida. Quando ``None``
            (default), nenhuma area distribuivel e considerada e a saida
            tem apenas as linhas das caixas (cabecalho + corpo +
            barra_de_menus) orientadas pelo conteudo. Quando fornecida,
            define a area disponivel do corpo (ADR-0024 DA-01 a DA-04):
            o descendente visual unico ocupa integralmente essa area
            (DA-01), grupos repassam a area aos filhos (DA-03), e
            composicoes invalidas — multiplos elementos sem distribuicao
            (DA-02) ou area sem elemento visual (DA-04) — sao rejeitadas
            com RenderizadorErro identificavel. Preenchimento externo
            vazio entre cabecalho e barra_de_menus e proibido (ADR-0024).
            Se a altura for insuficiente para cabecalho + barra_de_menus
            ou para o conteudo do corpo, lanca RenderizadorErro.

    Retorna:
        str com a representacao visual no formato definido pelo H-0010A:
        uma caixa de cabecalho derivada de ``modelo.cabecalho``, seguida
        de uma caixa por elemento de ``corpo.elementos[]`` (na ordem do
        JSON) e por fim uma caixa da ``barra_de_menus``. Os caracteres de
        canto e os delimitadores/capitalizacao dos chips derivam do
        ``estilo``. Cada linha nao-vazia tem exatamente ``largura`` (ou 42
        no fallback) chars Python; a string termina com ``"\\n"``. Quando
        ``altura`` e fornecida e suficiente, a saida tem exatamente
        ``altura`` linhas (``saida.count("\\n") == altura``).

    Lancamentos:
        RenderizadorErro quando:
            - o argumento ``modelo`` nao e um ModeloTela valido;
            - algum item de lancador possui ``texto`` acima de 15
              caracteres (rejeitado sem truncamento);
            - ``altura`` e fornecida e e insuficiente para cabecalho +
              barra_de_menus (``L_cab + L_barra > altura``) ou para o
              conteudo do corpo (``L_corpo_conteudo > L_corpo_disponivel``).
        TypeError quando ``estilo`` e omitido. Uma chamada legada que ainda
            passe ``tipo_borda`` (argumento removido) tambem levanta
            ``TypeError`` -- nao ha compatibilidade permanente.

    Efeitos colaterais:
        Nenhum. Nao altera o modelo, nao grava arquivo, nao consulta
        JSON em disco, nao executa acao, nao ativa binding, nao le o
        terminal. O ``estilo`` e consumido por leitura (duck typing) e
        nunca modificado.
    """
    if not isinstance(modelo, ModeloTela):
        raise RenderizadorErro(
            "renderizar_tela exige ModeloTela; recebido: {0}".format(
                type(modelo).__name__
            )
        )

    # H-0039 / ADR-0030: a borda deixa de ser escolha do renderer e passa a
    # ser dado de entrada. ``estilo`` e obrigatorio (sem default); se algum
    # chamador legado passar ``tipo_borda=...``, o Python levanta TypeError
    # porque este parametro nao existe mais -- estado final sem compatibilidade
    # transitória permanente.
    borda = _borda_de_estilo(estilo)

    # H-0034 / ADR-0023: o sinal de quadro mínimo global é redefinido a cada
    # chamada — o renderer é puro e nunca persiste o estado entre redesenhos
    # (R-14). Se qualquer ``lancador`` da composição sinalizar inviabilidade
    # (``content_w < coluna_minima_content_w``), a tela normal inteira é
    # substituída pelo quadro mínimo canônico (ADR-0017).
    _reiniciar_quadro_minimo_lancador()

    # H-0040 / ADR-0031: o contexto de navegacao de runtime é redefinido a cada
    # chamada (R-14) e populado com os parametros opcionais recebidos. Quando
    # ``lista_foco``/``foco_console``/``cursores`` sao omitidos, o contexto fica
    # inativo e o renderer preserva integralmente o comportamento pre-H-0040
    # (sem indicador de cursor, sem chips dinamicos). Os dados sao
    # EXCLUSIVAMENTE de runtime (NC-005): nunca persistem em JSON. Os símbolos
    # do indicador derivam do estilo global materializado (D12/ADR-0030).
    #
    # H-0045-P05: extraido para ``_preparar_contexto_navegacao`` (reutilizado
    # por ``altura_interna_disponivel``), garantindo que a autoridade de
    # geometria vertical usada pela reconciliacao de pagina avalia EXATAMENTE
    # o mesmo contexto de chips (regra_existencia/regra_ativo) que este render.
    _preparar_contexto_navegacao(
        estilo, largura, altura, verboso,
        foco_console=foco_console, cursores=cursores, lista_foco=lista_foco,
        largura_navegacao=largura_navegacao, selecoes=selecoes,
        chips_destacados=chips_destacados, executar_disponivel=executar_disponivel,
        paginas_atuais=paginas_atuais, modelo=modelo,
    )

    total_w = TOTAL_WIDTH if largura is None else largura
    inner_w = total_w - 2
    content_w = total_w - 3
    label_max = total_w - 4

    titulo = modelo.cabecalho["titulo"]
    descricao = modelo.cabecalho["descricao"]
    apresentacao = modelo.cabecalho["apresentacao"]

    partes = [
        _caixa(
            titulo, [descricao], borda, inner_w, content_w, label_max,
            apresentacao=apresentacao,
        )
    ]

    # H-0019: normalizar arranjo do corpo (aliases transicionais — ADR-0011).
    # Normalizacao local ao renderer; modelo e loader nao sao alterados.
    arranjo_corpo = modelo.corpo.arranjo
    if arranjo_corpo == "sobreposto":
        arranjo_corpo = "vertical"
    if arranjo_corpo == "lado_a_lado":
        arranjo_corpo = "horizontal"

    # H-0020: linhas_barra inicializada antes do bloco de corpo para permitir
    # pré-computação no modo horizontal com altura (evitar dupla chamada — R-4).
    linhas_barra = None

    # H-0025 / ADR-0018: distribuicao vertical explicita. So ativa quando o
    # container declara ``distribuicao`` (ausencia NAO equivale a ``igual``),
    # o arranjo e vertical (None/sobreposto normalizados inclusive) e uma
    # ``altura`` util foi fornecida. Sem ``altura`` nao ha area distribuivel e
    # o caminho orientado pelo conteudo e tomado integralmente.
    distribuicao_corpo = modelo.corpo.distribuicao
    _corpo_vertical_distribuido = False

    # H-0027 / ADR-0019: composicao recursiva por container. Determina a altura
    # disponivel do corpo antes de renderizar para passar ao container raiz.
    # Ausencia de altura -> composicao orientada pelo conteudo (ADR-0018 D2).
    l_corpo_disponivel = None
    if altura is not None:
        if linhas_barra is None:
            linhas_barra = _linhas_barra(modelo.barra_de_menus, estilo, content_w)
        l_cab = _contar_linhas(partes[0])
        l_barra = len(linhas_barra) + 2
        if l_cab + l_barra > altura:
            raise RenderizadorErro(
                "altura insuficiente: terminal com {0} linhas nao comporta "
                "cabecalho ({1}) + barra_de_menus ({2})".format(
                    altura, l_cab, l_barra
                )
            )
        l_corpo_disponivel = altura - l_cab - l_barra

    bloco_corpo = _renderizar_container(
        arranjo_corpo, distribuicao_corpo,
        modelo.corpo.elementos, borda, total_w, l_corpo_disponivel,
        verboso=verboso,
    )
    if popup is not None:
        if not bloco_corpo:
            raise RenderizadorErro(
                "popup exige corpo materializado para sobreposicao"
            )
        linhas_corpo = bloco_corpo.split("\n")
        if linhas_corpo and linhas_corpo[-1] == "":
            linhas_corpo.pop()
        largura_corpo = max((len(linha) for linha in linhas_corpo), default=0)
        altura_corpo = len(linhas_corpo)
        if l_corpo_disponivel is not None:
            # H-0060/P01: a altura natural do corpo subjacente nao representa
            # espaco fisico adicional para o popup. A sobreposicao opera sobre
            # uma projecao com exatamente a cota reservada ao corpo; assim, o
            # layout recebe a mesma autoridade vertical que a verificacao final.
            linhas_corpo = linhas_corpo[:l_corpo_disponivel]
            linhas_corpo.extend(
                [" " * largura_corpo]
                * (l_corpo_disponivel - len(linhas_corpo))
            )
            bloco_corpo = "\n".join(linhas_corpo)
            altura_corpo = l_corpo_disponivel
        bloco_corpo = sobrepor_no_corpo(
            bloco_corpo, popup, estilo, largura_corpo, altura=altura_corpo
        )
    if bloco_corpo:
        partes.append(bloco_corpo)

    # Corpo absorveu todo o espaco internamente quando: arranjo horizontal
    # (fill por coluna em _renderizar_container_horizontal) ou arranjo
    # vertical com distribuicao e altura fornecidos (fill por cota em
    # _renderizar_container_vertical). Nenhum fill externo e necessario.
    _corpo_vertical_distribuido = (
        arranjo_corpo != "horizontal"
        and distribuicao_corpo is not None
        and l_corpo_disponivel is not None
    )

    # Linhas de conteudo da barra_de_menus, computadas uma vez e reutilizadas
    # tanto para a contagem de L_barra (H-0015) quanto para a caixa final.
    # H-0016: distribuicao horizontal responsiva (ADR-0014) derivada de
    # barra_de_menus.distribuicao + chips[], usando a largura de conteudo
    # disponivel para decidir linha unica vs multilinha vs erro_layout.
    # H-0020 (R-4): pular se já computada no modo horizontal com altura.
    if linhas_barra is None:
        linhas_barra = _linhas_barra(modelo.barra_de_menus, estilo, content_w)

    # ADR-0024 (H-0033): verificacao pos-renderizacao de ocupacao integral.
    # Quando ``altura`` e fornecida e o arranjo e vertical sem distribuicao,
    # _renderizar_container_vertical ja aplicou DA-01 (unico visual ocupa
    # toda a area) ou lancou DA-02/DA-04. Aqui apenas verificamos que nenhuma
    # area externa ficou descoberta (guarda de seguranca para caminhos
    # nao verticais ou casos distribuidos).
    # Quando ``altura is None``, o corpo usa altura natural e nao ha area
    # residual a verificar.
    if altura is not None:
        l_cab = _contar_linhas(partes[0])
        l_barra = len(linhas_barra) + 2
        l_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])

        if l_cab + l_barra > altura:
            raise RenderizadorErro(
                "altura insuficiente: terminal com {0} linhas nao comporta "
                "cabecalho ({1}) + barra_de_menus ({2})".format(
                    altura, l_cab, l_barra
                )
            )
        l_corpo_disponivel = altura - l_cab - l_barra
        if l_corpo_conteudo > l_corpo_disponivel:
            raise RenderizadorErro(
                "altura insuficiente: corpo requer {0} linhas mas area "
                "disponivel e {1} linhas (altura={2}, cabecalho={3}, "
                "barra={4})".format(
                    l_corpo_conteudo, l_corpo_disponivel,
                    altura, l_cab, l_barra,
                )
            )
        l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
        if l_corpo_fill > 0 and arranjo_corpo != "horizontal" and not _corpo_vertical_distribuido:
            # ADR-0024 DA-04: preenchimento externo vazio e proibido.
            # _renderizar_container_vertical deve ter detectado DA-02/DA-04
            # e lancado RenderizadorErro antes de chegar aqui. Se chegou,
            # e um estado inesperado que tambem viola o invariante.
            raise RenderizadorErro(
                "DA-04 (ADR-0024): preenchimento externo vazio detectado — "
                "{0} linhas nao pertencem a nenhum elemento visual; toda "
                "area do corpo deve pertencer a console, dashboard ou "
                "lancador".format(l_corpo_fill)
            )

    partes.append(_caixa(
        _LABEL_BARRA, linhas_barra,
        borda, inner_w, content_w, label_max,
    ))

    # H-0034 / ADR-0023: se algum ``lancador`` da composição sinalizou
    # inviabilidade (``content_w < coluna_minima_content_w``), a tela normal é
    # integralmente substituída pelo quadro mínimo canônico global
    # (``quadro mínimo de terminal pequeno``, ADR-0017). Cabeçalho, corpo,
    # ``lancador``, dashboards e ``barra_de_menus`` não são exibidos (R-12/R-13).
    # O quadro mínimo reutiliza o mecanismo canônico: aviso textual adequado à
    # largura, sem truncamento, sem overflow, sem mensagem local do ``lancador``.
    if _quadro_minimo_lancador_esta_ativo():
        return _quadro_minimo_global(total_w, altura)

    return "\n".join(partes) + "\n"
