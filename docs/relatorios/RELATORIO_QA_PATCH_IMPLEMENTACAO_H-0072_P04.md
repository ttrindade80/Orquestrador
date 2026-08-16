# RELATÓRIO — QA_POS_PATCH H-0072 P04

```yaml
etapa: QA_POS_PATCH
objeto: H-0072
patch_implementacao: P04
natureza: QA_DE_EVIDENCIA_AUTOMATIZADA
achado_origem: VM-H0073-001
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P04.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: I1_IMPLEMENTATION_APPROVED
```

## Resultado

**I1_IMPLEMENTATION_APPROVED.** P04 fecha integralmente a evidência automatizada
pendente e não revela regressão causal nova.

**ACH-P03-01: RESOLVIDO e preservado.** O critério ANSI já resolvido no QA do
P03 não foi reaberto.

**ACH-P03-02: RESOLVIDO.** No teste focal, H-0063 é carregada uma vez por
`_abrir`; o fluxo entra efetivamente no nível filho e confirma isso antes da
renderização L1. `renderizar_estado(filhos, ..., largura=48)` ocorre
explicitamente antes de qualquer `navegacao.redimensionar`, e `tab_L1` é
extraída desse quadro. A continuidade é então `filhos → redimensionar(44) →
render L2 → redimensionar(43) → render L3`, sem reconstrução de tela ou
recarga do JSON. A evidência integrada usa o fluxo público de renderização e
resize, sem chamar diretamente helper privado de geometria.

As larguras observadas são `48 → 44 → 43`; as tabulações são `10 → 6 → 5`,
cumprindo `tab_L1 = 10`, `5 < tab_L2 < 10`, `tab_L3 = 5` e
`tab_L1 > tab_L2 >= tab_L3`.

Entre L1/L2/L3 permanecem a mesma tela e modelo, pai ativo, filho lógico,
foco, cursor, seleção e identidade lógica. H-0063 preserva designador ausente,
preset, amostra, duas colunas e alinhamento global. O critério
`H0063_ESPACAMENTO_COLUNAS_3_8` permanece **PRESERVADO**; os gaps observados
continuam em `3..8`.

## Escopo e testes

P04 declara e confirma nominalmente somente o teste focal e este relatório;
nenhum arquivo produtivo foi alterado pelo P04. Os demais deltas do worktree
são acumulados anteriores e não foram usados como prova causal única.

Resultados executados: teste focal H-0063 **6 passed**; suíte focal **159
passed**; H-0070 isolado **1 failed**, com `index("→") == 2` e esperado `>= 4`,
classificado **FALHA_HISTORICA_NAO_CAUSAL**; suíte canônica **1456 passed, 1
failed**, somente H-0070. H-0055 permanece sem regressão.

Não há achado material novo. `VM-H0073-001: PRONTO_PARA_REVALIDACAO`; a
revalidação manual em TTY continua necessária e não foi executada.
\n