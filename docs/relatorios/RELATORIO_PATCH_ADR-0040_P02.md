---
name: relatorio-patch-adr-0040-p02
description: Relatório do patch documental P02 da ADR-0040
metadata:
  type: relatorio
  escopo: patch_adr
  adr: ADR-0040
  patch: P02
---

# Relatório do patch P02 — ADR-0040

## Resultado

A ADR-0040 foi atualizada para incorporar a decisão complementar D-DRY-09 —
Estrutura declarativa do controle. O estado `metadata.status: aceita` e a
data vigente da ADR foram preservados. O bloqueio sobre o nome do campo de
configuração concreta foi encerrado documentalmente com a estrutura nominal
`controle_execucao.modo_inicial`.

## Rastreabilidade

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
achados_tratados:
  - BLOQUEIO-CAMPO-ESTADO-INICIAL
decisao_incorporada:
  - D-DRY-09
```

## Mudanças realizadas

- D-DRY-03 passou a referenciar a estrutura fechada por D-DRY-09, mantendo a
  declaração explícita, os valores `executar` e `dry_run`, a ausência de
  default e o modo corrente como estado de runtime.
- Foi adicionada D-DRY-09 com o objeto raiz `controle_execucao`, o campo
  obrigatório `modo_inicial`, enumeração fechada, ausência de default,
  ausência do objeto como não adoção e não persistência do estado vivo.
- A descrição, a rastreabilidade, a decisão consolidada, as consequências,
  o artefato `contrato_tela_json.md`, o fora de escopo e os critérios de
  aplicação foram ajustados para refletir a decisão nominal.
- A distinção de `dry_run_ativo` como estado da especialização focal da
  ADR-0037 foi preservada; nenhum outro campo interno foi decidido.

## Preservações e escopo

D-DRY-01 a D-DRY-08, a especialização focal da ADR-0037, a autoridade sobre
preservação e restauração da origem, as fronteiras operacionais, a proibição
de migração implícita e a necessidade de futura especificação e handoff de
reconciliação foram mantidas. Somente a ADR-0040 foi alterada; este relatório
foi criado sem sobrescrever o relatório de aplicação. Não foram alterados
contratos, código, configuração, testes, handoffs ou Git.

```yaml
status: PATCH_APPLIED
bloqueios: nenhum
```
