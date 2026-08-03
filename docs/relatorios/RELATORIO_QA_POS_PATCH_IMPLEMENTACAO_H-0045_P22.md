# QA pós-patch de implementação — H-0045 / P22

status: I5_MANUAL_VALIDATION_REQUIRED

## Estado dos achados

- `QA-H0045-P21-001`: atendido. A prova ponta a ponta ausente no P21 foi
  confirmada no teste P22.
- `VM-H0045-R06-001`: QA técnico conforme, mas permanece aberto até a
  validação manual focal do usuário.

## Continuidade do estado e provas

`_p22_modelos_tela_aninhada` cria uma raiz real com lançador e uma tela
aninhada com console `politica_selecao: multipla`, chip Esc com texto original
`Voltar` e `forma_exibicao: rotulo_dinamico_esc`. `processar_comando("x")`
empilha a raiz e abre a tela aninhada; `Tab` estabelece o foco e `Espaço`
seleciona o item. Não há inserção manual na pilha nem limpeza direta.

Antes do primeiro Esc, o teste confirma tela/pilha, seleção não vazia,
`saindo == False`, foco, cursor e página válidos, além de `[Esc] Limpar` sem
`[Esc] Voltar` ou `[Esc] Sair` no quadro renderizado.

O primeiro Esc usa `processar_comando` e o estado resultante alimenta o segundo
comando. A seleção é limpa integralmente; a tela, pilha, foco, cursor, página
e `saindo` permanecem preservados. Nova renderização confirma `[Esc] Voltar`
e ausência de `[Esc] Limpar`. O segundo Esc, novamente por
`processar_comando`, retorna à raiz e reduz a pilha exatamente uma vez, sem
saída global.

## Escopo e verificações

O delta P22 está restrito a `demo/teste_demo_paginacao.py`, com o teste e o
helper `_p22_modelos_tela_aninhada`; alterações históricas já presentes no
worktree não foram atribuídas ao P22. Não há achados materiais.

- teste nominal: `1 passed`;
- suíte focal: `483 passed`;
- suíte completa: `897 passed`;
- `git diff --check`: limpo.

Validação manual focal não executada. É a próxima ação necessária para o
encerramento de `VM-H0045-R06-001`.
