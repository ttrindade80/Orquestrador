"""Runner direto histórico da suíte do renderizador."""

import sys

__test__ = False


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
)

from tela.testes_renderizador.selecao import (
    teste_selecao_multipla_h0041,
)

from tela.testes_renderizador.comum import _BASE_PADRAO, _RESULTADOS

def main():
    print("Diagnostico H-0010A - renderer declarativo (curva/reta)")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_renderizador_orquestrador()
    teste_renderizador_destino_minimo()
    teste_renderizador_grupo_minimo()
    teste_modelo_fabricado()
    teste_erros_renderizador()
    teste_proibicoes_importacao()
    teste_inspecao_fonte_hardcoded()
    teste_inercia()
    teste_alternancia_borda()
    teste_largura_explicita()
    teste_altura_explicita()
    TestLinhasBarra().run_all()
    TestDistribuicaoH0018().run_all()
    TestArranjoH0019().run_all()
    TestPreenchimentoVerticalH0020().run_all()
    TestPreenchimentoBordeadoH0021().run_all()
    TestDistribuicaoVerticalH0025().run_all()
    TestDistribuicaoHorizontalH0026().run_all()
    TestHierarquiaGruposH0027().run_all()
    TestRenderizadorMatrizH0028().run_all()
    TestCardinalidadeUnitariaH0029().run_all()
    TestTelasPermanentesH0029().run_all()
    TestCatalogoH0030().run_all()
    TestDistribuicaoResponsivaH0034().run_all()
    TestOcupacaoIntegralCorpoH0033().run_all()
    TestHelperHorizontalH0033Patch2().run_all()
    TestCardinalidadeHorizontalH0033Patch3().run_all()
    TestCardinalidadeHorizontalH0033Patch4().run_all()
    TestDistribuicaoMatricialH0035().run_all()
    teste_conteudo_externo_h0036_render()
    teste_h0037_manual_001_marcador_truncamento()
    teste_h0037_manual_002_esc_primeiro()
    teste_h0037_qapp7_verb_sem_corte_silencioso()
    teste_selecao_multipla_h0041()

    print("")
    print("== Resumo ==")
    total = len(_RESULTADOS)
    passaram = sum(1 for _, ok in _RESULTADOS if ok)
    falharam = total - passaram
    print("Total de verificacoes: {0}".format(total))
    print("Passaram: {0}".format(passaram))
    print("Falharam: {0}".format(falharam))
    if falharam:
        print("")
        print("Verificacoes falhadas:")
        for nome, ok in _RESULTADOS:
            if not ok:
                print("  - {0}".format(nome))

    return 0 if falharam == 0 else 1
