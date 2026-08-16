# RELATÓRIO — QA_POS_PATCH H-0072 P03

```yaml
etapa: QA_POS_PATCH
objeto: H-0072
patch_implementacao: P03
achado_origem: VM-H0073-001
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P03.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: I6_QA_EVIDENCE_INCOMPLETE
```

## ACH-P03-01 — ANSI

**RESOLVIDO.** `tela/renderizacao/conteudo_externo.py` reutiliza a métrica
canônica vigente `_largura_sem_ansi`, definida em
`tela/renderizacao/texto_ansi.py`, para as larguras globais das colunas, a
necessidade mínima do texto e a sobra física da última célula. O preenchimento
usa `_ljust_sem_ansi`; SGR não entra como coluna. Não há novo stripping ANSI na
implementação produtiva. O algoritmo de espaçamento permanece separado e
escolhe o maior valor entre 3 e 8.

O caso regressivo real de H-0063 passa pela saída física do renderer auxiliar:
com `Destaque Texto` contendo ANSI, `content_w = 39` mantém tabulação 10 e
gap 3. A sequência observada é `content_w 51, 39, 38, 34` → tabulação
`10, 10, 9, 5` → gaps `8, 3, 3, 3`. Assim, a compactação prematura do P02
não se reproduz. Preset, amostra, designador ausente e apresentação tabular
permanecem preservados.

## ACH-P03-02 — resize integrado

**PENDENTE.** O teste novo usa a mesma tela H-0063, o mesmo modelo, entra em
L1 pelo fluxo normal, chama `navegacao.redimensionar` e chama
`renderizar_estado`, chegando a `10 → 6 → 5` nas larguras `48 → 44 → 43`.
Também preserva cursor, seleção e identidade lógica nas asserções.

Contudo, a cadeia obrigatória não é comprovada integralmente na mesma
continuidade: `renderizar_estado` antes da entrada em L1 produz `quadro_pai`;
após `processar_comando(..., " ", ...)`, o teste aplica imediatamente o
primeiro resize. Falta uma renderização explícita de L1 entre a entrada no
nível filho e o primeiro `navegacao.redimensionar`. Os demais testes renderizam
L1 ou testam resize, mas não fecham essa sequência em um único estado.

## Preservação e regressões

H-0055 permanece válido: `A)`, sufixo estrutural, apresentação texto,
conteúdo externo, unidade `ec/tg/designador/conteúdo`, navegação, seleção e
tabulações `10, 9, 5`. H-0063 preserva designador `nenhum`, preset, amostra,
título, duas colunas, alinhamento global, quebra física, identidade lógica,
navegação, seleção, resize e espaçamento `3..8`.

Testes focais obrigatórios: **159 passed**. H-0070 isolado: **1 failed**, com
`index("→") == 2` e esperado `>= 4`; falha histórica não causal ao P03. Suíte
canônica: **1456 passed, 1 failed**, somente H-0070.

O escopo causal nominal do P03 permanece restrito a
`tela/renderizacao/conteudo_externo.py`,
`demo/teste_demo_h0073_h0063_reconciliado.py` e ao relatório de patch; os
demais deltas do worktree são acumulados. Não foi identificada regressão
causal nova nem lacuna normativa. A métrica ANSI está aprovada, mas a
evidência integrada de resize está incompleta.

## Prontidão

`VM-H0073-001: BLOQUEADO`. Não marcar `PRONTO_PARA_REVALIDACAO` enquanto
ACH-P03-02 não tiver a renderização L1 explícita na cadeia integrada.
\n