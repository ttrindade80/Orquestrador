status: PATCH_IMPLEMENTACAO_CONCLUIDO
handoff: H-0052
patch: P04
origem: validacao_manual_2_de_3_pos_P03
defeito: fixture_insuficiente_para_demonstrar_topologia_bidimensional_toroidal
itens_navegaveis_finais: 5
distribuicao_utilizada: distribuicao_matricial.formacao.preferencia_linhas, linhas 1..5
arquivos_alterados:
  - config/telas/demo/h0052_nivel_unico_explicito.json
  - tela/teste_navegacao.py
  - tela/teste_loader.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0052_P04.md
testes:
  - tela/teste_navegacao.py + tela/teste_loader.py: 135 passed
  - teste focal H-0052: passed
suite_integral: 1060 passed
validacao_manual: PENDENTE_REEXECUCAO_2_DE_3
bloqueios: nenhum

A fixture anterior limitava a formação a uma única coluna e tinha apenas dois
itens. Assim, não havia navegação horizontal nem célula matricial vazia, e a
largura não podia recompor a grade entre múltiplas colunas e uma coluna.

Foi reutilizada a configuração canônica existente de `distribuicao_matricial`
com `preferencia_linhas`, permitindo que a largura selecione naturalmente
formações diferentes. A fixture agora tem cinco itens navegáveis, preserva
`nivel_unico` e o chip `[✥] Navegar` do P03.

Os testes usam o loader, o modelo, `grade_de_itens` e os movimentos reais para
confirmar que todos os cinco itens permanecem na topologia, que uma geometria
bidimensional expõe célula vazia, que os quatro sentidos alcançam itens reais e
que os retornos toroidais preservam o item inicial. Os testes runtime
existentes continuam cobrindo o toroide e a exclusão de células vazias.

Nenhum arquivo de runtime foi alterado. Não houve validação visual/TTY.
