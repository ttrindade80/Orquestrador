status: I5_MANUAL_VALIDATION_REQUIRED
handoff: H-0052
patch: P05
estado_consolidado: P03_P04_P05_APROVADO_AUTOMATICAMENTE
teste_manual_1_de_3: APROVADO_NAO_REPETIR
teste_manual_2_de_3: PENDENTE_REEXECUCAO_FINAL
teste_manual_3_de_3: PENDENTE
proxima_acao: VALIDACAO_MANUAL_2_DE_3

## Auditoria consolidada

A fixture `h0052_nivel_unico_explicito` carrega com `navegavel: true` e
`tipo: nivel_unico`, preservando os cinco IDs `item_a`–`item_e`, a
`preferencia_linhas` e o chip `[✥] Navegar`. Os cinco rótulos têm 26
caracteres; não há paginação interna nem regra especial para largura 31.

A API real de `grade_de_itens` produz 5×1 entre larguras 20–61 e 3×2 entre
62–80. Em largura 31 produz naturalmente cinco linhas e uma coluna; na
formação 3×2, todos os cinco itens permanecem presentes e uma célula é
`None`. `item_logico_de_posicao` exclui essa célula, e os quatro movimentos
alcançam somente itens reais. Os testes AT-0022–AT-0027 cobrem
horizontal/vertical, wrap toroidal por eixo e exclusão de vazios; o teste
H-0052 exercita os quatro movimentos na fixture consolidada.

`exibir_chip_navegar` permanece verdadeiro para o console focalizado com mais
de um item, e a renderização materializa `[✥] Navegar`.

Resultados: H-0052, 23 passed; focal (`tela/teste_navegacao.py` e
`tela/teste_loader.py`), 135 passed; suíte integral, 1060 passed. O diff
obrigatório não mostra runtime no delta P04/P05; alterações runtime existentes
no worktree pertencem ao estado anterior e não foram modificadas. A
validação manual não foi simulada; permanece somente a reexecução final do
teste 2/3 e a execução posterior do teste 3/3 pelo usuário.
