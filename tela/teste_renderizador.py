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

import re as _re_h0071

from tela.testes_renderizador.comum import (
    _ESTILO_CURVA as _h0071_ESTILO_CURVA,
    _RAIZ_TELAS_DEMO as _h0071_RAIZ_TELAS_DEMO,
)
from tela.testes_renderizador.selecao import (
    _barra_chip as _h0071_barra_chip,
    _carregar_fixture_h0041_p03 as _h0071_carregar_fixture_h0041_p03,
    _renderizar_h0041_p03 as _h0071_renderizar_h0041_p03,
    _rend_qa002 as _h0071_rend_qa002,
)
from tela.testes_renderizador.integracao import (
    _p12_montar_caso_render as _h0071_p12_montar_caso_render,
)


def _h0071_sem_ansi(texto):
    return _re_h0071.sub(r"\x1b\[[0-9;]*m", "", texto)


def test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao():
    modelo, lista, console, estilo = _h0071_carregar_fixture_h0041_p03()
    saida, chips = _h0071_renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=2, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is True
    assert chips["chip_enter"] is False
    barra = _h0071_barra_chip(saida, "␣")
    assert "Marcar" in barra
    assert "Executar" in saida
    assert "executar" not in saida
    codigo = _h0071_rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    reset = _h0071_rend_qa002._ANSI_RESET_FG
    assert "{0}[␣]".format(codigo) not in barra
    assert "[␣] Marcar" in barra
    barra_visivel = _h0071_sem_ansi(barra)
    assert "[⏎] Executar" in barra_visivel
    assert "[{0}⏎{1}] Executar".format(codigo, reset) in barra


def test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura():
    modelo, lista, console, estilo = _h0071_carregar_fixture_h0041_p03()
    saida, chips = _h0071_renderizar_h0041_p03(
        modelo, lista, console, estilo,
        foco=1, selecoes={console.id: ["item_01"]},
    )
    assert chips["chip_espaco"] is False
    assert chips["chip_enter"] is False
    codigo = _h0071_rend_qa002._codigo_ansi_de_cor(estilo.cor_inativo)
    reset = _h0071_rend_qa002._ANSI_RESET_FG
    assert estilo.cor_inativo == "cinza"
    assert codigo == "\x1b[90m"
    barra = _h0071_barra_chip(saida, "␣")
    idx_cor = barra.find(codigo)
    idx_marcar = barra.find("Marcar")
    idx_reset = barra.find(reset, idx_cor)
    assert idx_cor != -1
    assert idx_marcar != -1
    assert idx_reset != -1
    assert idx_cor < idx_reset < idx_marcar
    assert "Executar" in saida
    assert "marcar" not in saida
    assert "executar" not in saida


def test_h0041_p04_texto_chip_barra_nao_usa_lower():
    chip = {"tecla": "⏎", "texto": "Executar"}
    texto = _h0071_rend_qa002._texto_chip_barra(
        chip, _h0071_ESTILO_CURVA, vao=1, inativo=True
    )
    assert "Executar" in texto
    assert "executar" not in texto
    codigo = _h0071_rend_qa002._codigo_ansi_de_cor("cinza")
    reset = _h0071_rend_qa002._ANSI_RESET_FG
    assert codigo in texto
    assert reset in texto
    assert texto.index(codigo) < texto.index(reset) < texto.index("Executar")


def test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos():
    from tela import navegacao
    from tela import renderizador as _rend
    from tela.loader import carregar_tela
    from tela.modelo import construir_modelo
    from tela.renderizador import renderizar_tela

    modelo = construir_modelo(
        carregar_tela(None, "h0045_paginacao_conjunto_vazio", _h0071_RAIZ_TELAS_DEMO)
    )
    console = modelo.corpo.elementos[0]
    assert console._campos_inertes.get("itens") == []
    assert navegacao.console_e_focalizavel(console) is False
    assert navegacao.lista_foco(modelo) == []

    saida = renderizar_tela(
        modelo,
        _h0071_ESTILO_CURVA,
        largura=80,
        altura=24,
        foco_console=None,
        cursores={},
        lista_foco=navegacao.lista_foco(modelo),
        paginas_atuais={},
    )
    assert "página 1/1" in saida
    saida_visivel = _h0071_sem_ansi(saida)
    assert "[PgUp/PgDn]" in saida_visivel
    assert "[PgUp][PgDn]" not in saida_visivel
    codigo_inativo = _rend._codigo_ansi_de_cor(_h0071_ESTILO_CURVA.cor_inativo)
    reset = _rend._ANSI_RESET_FG
    unidade_inativa = (
        "[" + codigo_inativo + "PgUp" + reset
        + "/" + codigo_inativo + "PgDn" + reset + "]"
    )
    assert unidade_inativa in saida
    estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
    assert estados.get("chip_pagina_anterior") is False
    assert estados.get("chip_pagina_proxima") is False
    assert _rend._navegacao_atual.get("cursores") == {}
    assert "aviso_" not in saida
    assert "info_0" not in saida


def test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica():
    from tela import renderizador as _rend
    from tela.renderizador import geometria_console
    from demo.demo import processar_comando, renderizar_estado
    from tela import navegacao

    for largura, altura in ((80, 24), (80, 40), (50, 20)):
        estado, modelo, caso = _h0071_p12_montar_caso_render(
            "h0045_validacao_vazio", largura, altura
        )
        console = modelo.corpo.elementos[0]
        assert console._campos_inertes.get("itens") == []
        saida = renderizar_estado(estado, modelo, largura, altura)
        assert "página 1/1" in saida
        saida_visivel = _h0071_sem_ansi(saida)
        assert "[PgUp/PgDn]" in saida_visivel
        assert "[PgUp][PgDn]" not in saida_visivel
        assert _h0071_ESTILO_CURVA.selecionado_simbolo not in saida
        estados = _rend._navegacao_atual.get("estado_ativo_chips") or {}
        assert estados.get("chip_pagina_anterior") is False
        assert estados.get("chip_pagina_proxima") is False
        for cmd in (",", ".", "\x1b[A", "\x1b[B"):
            novo = processar_comando(estado, cmd, modelo)
            assert novo["cursores"] == {}
        geo = geometria_console(
            modelo, _h0071_ESTILO_CURVA, largura, altura, False,
            console=console, foco_console=None, cursores={},
            lista_foco=navegacao.lista_foco(modelo),
            paginas_atuais={},
        )
        assert geo is not None
        assert geo["altura_interna"] == caso["C"]


if __name__ == "__main__":
    sys.exit(main())
