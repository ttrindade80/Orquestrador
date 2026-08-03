"""Hierarquia de erros do carregamento de telas."""

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

    def __init__(self, encontrado, esperado="orquestrador"):
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


class EstiloErro(Exception):
    """Erro de carregamento ou validacao de ``config/estilo.json`` (H-0039).

    Levantada por ``carregar_estilo`` em qualquer condicao invalida listada
    nas validacoes V-01 a V-29 (ADR-0030 D9). Configuracao parcialmente
    resolvida nunca produz ``EstiloResolvido`` -- nao existe fallback
    silencioso.
    """
