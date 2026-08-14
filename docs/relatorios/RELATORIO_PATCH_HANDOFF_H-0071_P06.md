# RELATORIO_PATCH_HANDOFF_H-0071_P06

## Cadeia

- projeto: Orquestrador
- item: ITEM-0010
- adr: ADR-0046
- handoff: H-0071
- etapa: PATCH_HANDOFF P06
- predecessor imediato: PATCH_HANDOFF P05 (`PATCH_HANDOFF_CONCLUIDO`) e QA_HANDOFF pós-P05 (`H2_HANDOFF_PATCH_REQUIRED`)
- status: PATCH_HANDOFF_CONCLUIDO
- data: 2026-08-14

## Achado corrigido

ACH-QA-H0071-P05-01.

O H-0071 pós-P05 autorizava o relatório futuro da implementação como
artefato separado, sem informar o caminho nominal. A referência a
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` era histórica
e não definia o destino da próxima execução.

## Correção

Definido explicitamente no H-0071 que a próxima PATCH_IMPLEMENTACAO deverá
criar:

`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P05.md`

Esse caminho é o artefato obrigatório da próxima implementação.

Distinção deixada inequívoca:

1. `RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` é histórico e não deve ser
   sobrescrito;
2. a próxima execução cria um novo relatório P05 de implementação;
3. esse P05 pertence à etapa futura de PATCH_IMPLEMENTACAO;
4. `RELATORIO_PATCH_HANDOFF_H-0071_P05.md` pertence ao patch anterior do
   próprio handoff e não é relatório de implementação;
5. `RELATORIO_PATCH_HANDOFF_H-0071_P06.md` é o relatório desta etapa
   documental.

Não houve decisão além da nomeação/localização do relatório futuro.

## Preservação

Nenhuma outra decisão do H-0071 pós-P05 foi alterada materialmente.
Permanecem: Curva `╭`/`╮`; Ornamental `❲`/`❳`; distinção entre ambos;
composição multitecla única com `/`; `[PgUp][PgDn]` proibido como forma
física; correção declarativa de H-0054/H-0055/H-0063; restauração de
`config/estilo.json`; `cor_inativo` em página 1/1; escopo mínimo; exclusão
dos renderers sem defeito confirmado; três testes obrigatórios; teste do
caminho real H-0063; validação final pelo usuário em TTY; regra de exceção
operacional para arquivo não autorizado.

## Verificações

- leitura integral do H-0071;
- busca focal no próprio handoff (`relatorio|RELATORIO_|implementacao|P04|P05|P06`);
- revisão do diff focal;
- `git diff --check` nos dois artefatos desta etapa.

## Bloqueios

Nenhum.
