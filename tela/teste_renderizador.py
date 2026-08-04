"""Fachada de coleta e execução direta dos testes do renderizador.

As definições vivem em tela.testes_renderizador; este caminho legado agrega
nominalmente os proprietários para preservar a descoberta histórica.
"""

import os
import sys

sys.dont_write_bytecode = True

from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))


from tela.testes_renderizador.fundamentos import (
    teste_renderizador_orquestrador,
    teste_renderizador_destino_minimo,
    teste_renderizador_grupo_minimo,
    teste_modelo_fabricado,
    teste_erros_renderizador,
    teste_proibicoes_importacao,
    teste_inspecao_fonte_hardcoded,
    teste_inercia,
    teste_alternancia_borda,
    teste_largura_explicita,
    teste_altura_explicita,
)

from tela.testes_renderizador.barra_menus import (
    TestLinhasBarra,
    TestDistribuicaoH0018,
    TestH0045P23BarraCincoLinhas,
    TestH0045P23RegressaoDuasLinhas,
    test_h0044_chip_destacado_usa_cor_alerta,
    test_h0044_chip_ativo_normal_sem_destaque,
    test_h0044_chip_inativo_cinza_nao_amarelo,
    test_h0044_destaque_nao_inativa,
    test_h0044_largura_sem_ansi_destaque,
    test_h0044_cor_nao_vaza_entre_chips,
    test_h0044_executar_disponivel_ativa_selecao_nao_vazia,
    test_h0044_regressao_sem_destaque_identica,
    test_h0045_renderiza_apenas_fragmentos_da_pagina_atual_com_indicador,
    test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo,
    test_h0045_p02_barra_alinhada_na_sequencia_de_larguras,
)

from tela.testes_renderizador.composicao_corpo import (
    TestArranjoH0019,
    TestPreenchimentoVerticalH0020,
    TestPreenchimentoBordeadoH0021,
    TestDistribuicaoVerticalH0025,
    TestDistribuicaoHorizontalH0026,
    TestHierarquiaGruposH0027,
    TestOcupacaoIntegralCorpoH0033,
    TestHelperHorizontalH0033Patch2,
    TestCardinalidadeHorizontalH0033Patch3,
    TestCardinalidadeHorizontalH0033Patch4,
)

from tela.testes_renderizador.matriz_participantes import (
    TestRenderizadorMatrizH0028,
    TestCardinalidadeUnitariaH0029,
    TestTelasPermanentesH0029,
    TestCatalogoH0030,
    TestDistribuicaoMatricialH0035,
)

from tela.testes_renderizador.lancador import (
    TestDistribuicaoResponsivaH0034,
)

from tela.testes_renderizador.conteudo_externo import (
    teste_conteudo_externo_h0036_render,
    teste_h0037_manual_001_marcador_truncamento,
    teste_h0037_manual_002_esc_primeiro,
    teste_h0037_qapp7_verb_sem_corte_silencioso,
    test_h0044_p01_valor_campo_normaliza_newline_a_direita,
    test_h0044_p01_valor_campo_normaliza_newlines_embutidos,
    test_h0044_p01_valor_campo_none_continua_indisponivel,
    test_h0044_p01_valor_campo_falsy_nao_none_preservado,
    test_h0044_p01_envelope_falha_cabe_em_altura_suficiente,
    test_h0044_p01_limite_calculado_corresponde_ao_conteudo_natural,
    test_h0044_p01_tres_controles_envelope_renderizam,
    test_h0044_p01_redimensionamento_decide_capacidade_sem_reiniciar,
)

from tela.testes_renderizador.selecao import (
    teste_selecao_multipla_h0041,
    test_qah0041_002_chip_enter_sem_selecao_ativo,
    test_qah0041_002_chip_enter_com_selecao_inativo,
    test_qah0041_002_estado_logico_independente_do_rotulo,
    test_qah0041_002_chip_enter_inativo_distingue_de_ativo,
    test_qah0041_002_chip_enter_inativo_nao_cria_operacao,
    test_qah0041_002_console_sem_selecao_multipla_preserva_ativo,
    test_qah0041_002_renderer_avalia_regra_ativo_nao_ignora,
    test_h0041_manual_001_espaco_inativo_em_item_nao_selecionavel,
    test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao,
    test_h0041_manual_001_espaco_recalculado_por_movimento,
    test_h0041_manual_002_enter_inativo_com_selecao_visual,
    test_h0041_manual_003_todos_e_redraw_no_mesmo_quadro,
    test_h0041_manual_003_selecao_vazia_apresenta_todos_ativo,
    test_h0041_manual_001_console_sem_selecao_multipla_sem_espaco_inativo,
    test_h0041_p04_chip_ativo_preserva_apresentacao,
    test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura,
    test_h0041_p04_estado_logico_nao_inferido_pelo_rotulo,
    test_h0041_p04_texto_chip_barra_nao_usa_lower,
    TestRotuloDinamicoEscP21,
)

from tela.testes_renderizador.integracao import (
    test_h0045_p04_dois_consoles_ids_unicos_foco_cursor_e_paginas_independentes,
    test_h0045_p06_distribuicao_vertical_geometria_por_console_e_renderer_concordam,
    test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao,
    test_h0045_p07_console_direto_preservado_regressao,
    test_h0045_p07_console_dentro_de_grupo_geometria_real,
    test_h0045_p07_dois_consoles_mesmo_grupo_geometrias_independentes,
    test_h0045_p07_grupo_aninhado_geometria_considera_ancestrais,
    test_h0045_p07_console_ausente_retorna_none_sem_fallback,
    test_h0045_p07_estrutura_matriz_geometria_por_celula,
    test_h0045_p10_mapa_fisico_usa_largura_da_celula_e_preserva_fragmentos,
    test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos,
    test_h0045_p12_quebra_textual_por_largura_marcadores_unicos,
    test_h0045_p12_continuacao_sem_cursor_regular_e_alta,
    test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica,
    test_h0045_ph07_largura_horizontal_celula_unica_quatro_larguras,
    test_h0045_ph07_coerencia_renderer_mapa_fisico,
    test_h0045_ph07_distribuicao_matricial_multiplas_celulas_preservada,
    test_h0045_ph07_regressao_h0037_console_externo,
    test_h0045_ph07_cinco_telas_validacao,
)

from tela.testes_renderizador.selecao import (
    _fixture_h0041_qa002 as _fixture_h0041_qa002,
)

from tela.testes_renderizador.runner import main



if __name__ == "__main__":
    sys.exit(main())
