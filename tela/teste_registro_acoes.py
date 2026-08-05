from tela.registro_acoes import (
    RegistroAcoes,
    RegistroAcoesErro,
    validar_elegibilidade,
)


def test_registro_resolve_categorias_e_preserva_modos_declarados():
    registro = RegistroAcoes()
    processo = registro.registrar(
        "processo.ok", "processo", ("dry_run", "executar"), executor=lambda captura: captura
    )
    navegacao = registro.registrar("nav.ok", "navegacao")
    visualizacao = registro.registrar("vis.ok", "visualizacao")

    assert processo.modos_execucao_aceitos == ("executar", "dry_run")
    assert registro.resolver("processo.ok") is processo
    assert registro.resolver({"id": "nav.ok"}) is navegacao
    assert registro.resolver("vis.ok") is visualizacao


def test_registro_rejeita_categoria_ausente_desconhecida_e_acao_ausente():
    registro = RegistroAcoes()
    try:
        registro.registrar("sem.categoria", None)
    except RegistroAcoesErro:
        pass
    else:
        raise AssertionError("categoria ausente deveria falhar")

    try:
        registro.registrar("categoria.ruim", "script")
    except RegistroAcoesErro:
        pass
    else:
        raise AssertionError("categoria desconhecida deveria falhar")

    try:
        registro.resolver("nao.registrada")
    except RegistroAcoesErro:
        pass
    else:
        raise AssertionError("acao ausente deveria falhar")


def test_registro_rejeita_processo_sem_modos_modo_desconhecido_e_duplicado():
    registro = RegistroAcoes()
    for identidade, modos in (
        ("sem.modos", None),
        ("modo.ruim", ("executar", "inexistente")),
        ("duplicada", ("executar", "executar")),
    ):
        try:
            registro.registrar(identidade, "processo", modos)
        except RegistroAcoesErro:
            continue
        raise AssertionError("declaracao invalida aceita: {0}".format(identidade))


def test_elegibilidade_exige_os_dois_modos_somente_de_processos():
    registro = RegistroAcoes()
    registro.registrar("nav", "navegacao")
    registro.registrar("vis", "visualizacao")
    registro.registrar("proc.um.modo", "processo", ("executar",))
    tela = {
        "controle_execucao": {"modo_inicial": "executar"},
        "referencias_de_acoes": {
            "navegacao": "nav",
            "visualizacao": "vis",
            "acao_enter": "proc.um.modo",
        },
    }
    try:
        validar_elegibilidade(tela, registro)
    except RegistroAcoesErro:
        pass
    else:
        raise AssertionError("processo de um modo deveria ser inelegivel")

    registro.registrar(
        "proc.dois.modos", "processo", ("executar", "dry_run")
    )
    tela["referencias_de_acoes"]["acao_enter"] = "proc.dois.modos"
    acoes = validar_elegibilidade(tela, registro)
    assert [acao.categoria for acao in acoes] == [
        "navegacao",
        "visualizacao",
        "processo",
    ]


def test_registro_nao_infere_compatibilidade_por_nome_ou_texto():
    registro = RegistroAcoes()
    registro.registrar("proc.com.nome.de.processo", "processo", ("executar",))
    tela = {
        "controle_execucao": {"modo_inicial": "dry_run"},
        "id": "proc.com.nome.de.processo",
        "titulo": "Executar",
    }
    assert validar_elegibilidade(tela, registro) == ()
