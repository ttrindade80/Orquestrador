# Relatório de patch documental — H-0055 P02

```yaml
patch: P02
resultado: HANDOFF_PATCH_APPLIED
raiz: docs/handoff/H-0055-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0055_P01.md
```

## Achados tratados e delta aplicado

### QA-H0055-001 — estado inicial obrigatório

Resolvido pela decisão explícita do usuário: o JSON de dados é a fonte do
valor inicial e, para cada pai, o primeiro filho direto na ordem já existente
do array é o filho inicialmente escolhido na entrada atual da demonstração ou
do teste. O handoff diferencia esse valor inicial do estado de runtime, no qual
Espaço transfere a escolha, e da persistência futura, que não é implementada e
não altera o JSON ao sair ou reabrir. O bloqueio documental foi removido.

### QA-H0055-002 — despacho contextual de Esc

Permanece resolvido documentalmente nos dois níveis: retorno aos pais no nível
dos filhos e retorno/saída existente no nível dos pais, sempre preservando a
escolha obrigatória sem criar cancelamento, Enter ou ação nova.

### QA-H0055-003 — `politica_selecao`

Permanece resolvido documentalmente com `politica_selecao: multipla` na
especificação nominal da fixture, somente para reutilizar `tg` e `[␣]`.

### QA-H0055-004 — D23 e modos

Permanece resolvido documentalmente com `alternavel` e
`modo_inicial: nao_verboso`, alternância reversível, preservação de
`modo normal` × `modo não verboso` e do nome `hierarquia`.

### QA-H0055-005 — paginação e conteúdo

Permanece resolvido documentalmente com `politica_paginacao: com`, 25 itens
lógicos estruturados em cinco pais e quatro filhos diretos por pai, e
demonstração de duas páginas com `PageDown`, `PageUp` e
`[PgUp][PgDn] Páginas`, sem paginação concorrente.

## Artefatos, verificações focais e pendências

- O handoff foi atualizado para `pronto_para_implementacao` documental, sem
  implementar a capacidade.
- `docs/backlog.md` recebeu o `ITEM-0026` — persistência futura da escolha de
  filho por pai — com status planejado e especificação própria como próxima
  ação; a referência factual de H-0055 foi atualizada sem reescrever histórico.
- O relatório P01 foi preservado sem alteração.
- Verificou-se a materialização do handoff, do backlog atualizado e deste
  relatório P02.
- Não houve implementação, execução de QA, alteração de fixtures existentes ou
  commit.
