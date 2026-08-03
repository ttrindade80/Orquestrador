"""Fachada pública dos módulos internos de carregamento de telas.

A implementação vive em tela.carregamento; este módulo preserva os
caminhos públicos históricos por meio de reexportações nominais diretas.
"""

from tela.carregamento.d23_console import _validar_d23_console
from tela.carregamento.envelope_pre_adr_0028 import _console_em_escopo_d23
from tela.carregamento.erros import (
    EstiloErro,
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaElementoSemId,
    TelaElementoSemTipo,
    TelaErro,
    TelaEstruturaInvalida,
    TelaGrupoInvalido,
    TelaIdIncorreto,
    TelaIdNaoCoincideComArquivo,
    TelaJsonInvalido,
    TelaTipoDesconhecido,
)
from tela.carregamento.estilo import EstiloResolvido, carregar_estilo
from tela.carregamento.conteudo_externo import (
    carregar_conteudo_externo,
    validar_conteudo_externo,
)
from tela.carregamento.tela_json import carregar_tela
from tela.carregamento.taxonomia import (
    ARRANJOS_CORPO_VALIDOS,
    MODOS_DISTRIBUICAO_CORPO_VALIDOS,
    PERFIL_RESULTADO_EXECUCAO,
    TIPOS_CORPO_VALIDOS,
    TIPOS_ESTRUTURAIS_VALIDOS,
)
