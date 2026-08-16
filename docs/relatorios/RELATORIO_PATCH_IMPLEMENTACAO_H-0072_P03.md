# RELATÓRIO — PATCH_IMPLEMENTACAO H-0072 P03

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P03
achado_origem: VM-H0073-001
corrige:
  - ACH-P03-01
  - ACH-P03-02
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P02.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: IMPLEMENTATION_PATCHED
```

## Correções

A causa original foi preservada: `_cabe_tabulacao` precisava considerar a
apresentação real, não somente a reserva fixa mínima. P02 usava `len()` nas
larguras globais da tabela e em `len(texto_filho)`. Em H-0063, amostras reais
contêm SGR ANSI; esses bytes não ocupam colunas físicas.

Em `tela/renderizacao/conteudo_externo.py`, P03 reutiliza as métricas canônicas
`_largura_sem_ansi` e `_ljust_sem_ansi`. As larguras globais, a necessidade
mínima para texto, a sobra antes da última célula e o preenchimento das colunas
passam a usar a mesma largura visual do renderer. A decisão continua sendo o
maior valor que cabe entre 5 e 10. O algoritmo separado que escolhe o
espaçamento permanece o mesmo, com intervalo contratado 3..8.

## Evidências

H-0063 usa a projeção real e confirma que a amostra `Destaque Texto` contém
ANSI. Com larguras úteis `(51, 39, 38, 34)`, a tabulação observada é
`10, 10, 9, 5`; o ponto `39` prova contra a compactação prematura de P02.
Os gaps correspondentes são `8, 3, 3, 3`, sempre no intervalo aprovado.
Assim, a evidência cobre máximo, intermediário e mínimo sem contar SGR como
coluna. H-0055 preserva a evidência existente na mesma estrutura, `10, 9, 5`,
com `A)` e a unidade inteira `ec → tg → designador → conteúdo`.

Foi acrescentada, em
`demo/teste_demo_h0073_h0063_reconciliado.py`, uma prova pelo fluxo real: a
mesma tela, modelo e estado entram no nível filho; `navegacao.redimensionar`
é aplicado sucessivamente nas larguras totais `48, 44, 43`; cada estado é
renderizado novamente por `renderizar_estado`. As tabulações físicas são
`10, 6, 5`. Cursor, seleção, preset, amostra, designador ausente, identidade
lógica, alinhamento e gaps 3..8 permanecem preservados. Isso comprova a cadeia
estado existente → resize → novo render; não há chamada direta ao helper no
teste integrado.

## Arquivos efetivamente alterados

- `tela/renderizacao/conteudo_externo.py`
- `demo/teste_demo_h0073_h0063_reconciliado.py`
- este relatório

Nenhuma configuração, conteúdo externo, documento normativo, modelo, loader,
`demo.py`, H-0055, H-0070 ou algoritmo contratual de espaçamento foi alterado
por P03. Os demais deltas visíveis no worktree são acumulados e não foram
atribuídos a este patch.

## Testes e estado

- Focais obrigatórios: **159 passed**.
- H-0070 isolado: **falha histórica não causal**, `index("→") == 2`, esperado
  `>= 4`; o teste permaneceu intacto.
- Suíte canônica: **1456 passed, 1 failed**, somente H-0070.
- Monotonicidade: preservada; tabulação não aumenta em larguras decrescentes,
  permanece em 5..10 e alcança 5.
- Desvios: nenhum. Bloqueios de implementação: nenhum.

Revalidação manual em TTY continua necessária como gate posterior; não foi
executada neste patch.
\n