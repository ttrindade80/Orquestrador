"""Fachada pública compatível do renderizador.

As implementações vivem em tela.renderizacao; este módulo preserva os nomes
públicos existentes por reexportação nominal.
"""

from tela.renderizacao.erros import RenderizadorErro
from tela.renderizacao.contexto_execucao import (
    DESCONTO_ESTRUTURAL_CONSOLE,
    _navegacao_atual,
    _preparar_contexto_navegacao,
)
from tela.renderizacao.geometria_caixa import (
    _distribuir_alturas,
    _distribuir_larguras,
    _pesos_distribuicao,
)
from tela.renderizacao.designadores import _alfabetico, _romano, _texto_designador
from tela.renderizacao.conteudo_externo import (
    _quebrar_texto,
    _texto_valor_campo,
    _truncar_com_marcador,
)
from tela.renderizacao.lancador import _linhas_lancador
from tela.renderizacao.barra_menus import (
    _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT,
    _avaliar_regra_ativo,
    _garantir_esc_primeiro,
    _linhas_barra,
    _normalizar_distribuicao,
    _texto_chip_barra,
    _validar_distribuicao,
)
from tela.renderizacao.texto_ansi import (
    _ANSI_RESET_FG,
    _codigo_ansi_de_cor,
    _largura_sem_ansi,
    _ljust_sem_ansi,
)
from tela.renderizacao.matriz_participantes import (
    _largura_indicador_do_elemento,
    _larguras_mapa_fisico_matricial,
    _participantes_distribuicao_matricial,
    _renderizar_participante_na_celula,
    calcular_distribuicao,
)
from tela.renderizacao.console import _linhas_console, mapa_fisico_de_itens
from tela.renderizacao.paginacao_interna import _linhas_distribuicao_matricial
from tela.renderizacao.composicao_corpo import (
    _montar_corpo_horizontal,
    _renderizar_container_horizontal,
)
from tela.renderizacao.tela import (
    altura_interna_disponivel,
    geometria_console,
    renderizar_tela,
)
