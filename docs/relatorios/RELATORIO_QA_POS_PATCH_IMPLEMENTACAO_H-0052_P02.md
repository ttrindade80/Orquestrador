# Relatório QA pós-patch — H-0052 P02

```yaml
status: I5_MANUAL_VALIDATION_REQUIRED
handoff: H-0052
patch: P02
achado_corrigido: topologia_visual_inexistente_na_fixture_nivel_unico
teste_manual_1_de_3: APROVADO_NAO_REPETIR
teste_manual_2_de_3: PENDENTE_REEXECUCAO
teste_manual_3_de_3: PENDENTE
proxima_acao: VALIDACAO_MANUAL_2_DE_3
```

Causa confirmada: os itens já eram preservados no modelo/runtime, mas a
fixture não declarava a distribuição matricial necessária para materializar a
topologia visual.

Delta conferido: P02 adiciona a distribuição canônica de uma coluna à fixture
e amplia o teste do loader; `id`, `navegavel: true` e `tipo: nivel_unico`
permanecem intactos. Não há alteração runtime atribuível a P02.

Topologia runtime confirmada: o carregamento real produz um console
focalizável, dois itens navegáveis distintos na coleção e os mesmos dois itens
na grade. `mover_baixo` muda do item inicial para o outro e `mover_cima`
retorna ao anterior.

Teste preventivo: `test_h0052_fixtures_de_demonstracao_carregam` usa o modelo,
coleção, grade e movimentos reais, sem contagem de JSON bruto, rótulos
incidentais ou simulação paralela.

Testes reexecutados: focal `1 passed, 83 deselected`; suíte focal `134
passed`; suíte integral `1059 passed`. O runner carregou a fixture e encerrou
com código 0; nenhuma validação visual foi declarada.

Validação humana restante: reexecução manual 2/3 em TTY real e, depois, teste
manual 3/3.
