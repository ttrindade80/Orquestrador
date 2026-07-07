---
name: relatorio-qa-doc-0027-contrato-console-pos-ajuste
description: QA pos-ajuste do DOC-0027 sobre criterios de validacao do contrato console
metadata:
  type: relatorio_qa
  scope: docs
  doc: DOC-0027
  status: APROVADO
  criado_em: 2026-07-07
---

# Relatorio QA — DOC-0027 — Contrato `console` Pos-Ajuste

## Status final

`APROVADO`

O problema P1 apontado em
`docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md` foi resolvido.
A secao de criterios de validacao de `docs/contratos/contrato_console.md`
agora espelha explicitamente todos os campos minimos da instancia definidos
na secao 3.

## Escopo verificado

Foram lidos antes da avaliacao:

- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/contratos/contrato_console.md`
- `docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md`

Tambem foram executados os comandos solicitados:

```bash
git diff --check -- docs/contratos/contrato_console.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_console.md docs/build_docs/to_do.md
```

`git diff --check` nao reportou problemas. O `git diff` mostrou alteracoes
em `docs/build_docs/to_do.md`; `docs/contratos/contrato_console.md` esta
como arquivo ainda nao rastreado no workspace, portanto nao aparece no diff
padrao do Git, mas foi lido diretamente para esta QA.

## Evidencias do ajuste

- A estrutura minima da instancia declara `id`, `tipo = console`, `titulo ou
  identificador visual`, `origem_dados ou binding`, `itens ou regra de
  geracao de itens`, `politica_composicao`, `politica_navegacao`,
  `politica_selecao`, `politica_paginacao` e `politica_exibicao`
  (`docs/contratos/contrato_console.md`, linhas 70-100).
- A secao 16 agora invalida instancia sem `id` (linha 432), sem `tipo`
  (linha 433) e com `tipo` diferente de `console` (linhas 434-435).
- A secao 16 agora invalida instancia sem `titulo` ou identificador visual
  (linha 436).
- A secao 16 agora invalida instancia sem `origem_dados`, `binding` ou regra
  de geracao de itens (linhas 437-438).
- A secao 16 agora invalida ausencia de `politica_composicao`,
  `politica_navegacao`, `politica_selecao`, `politica_paginacao` e
  `politica_exibicao` (linhas 439-443).

## Criterios preservados

Os criterios anteriores foram preservados na secao 16:

- itens: `id`, `tipo`, tipo desconhecido, navegabilidade e selecionabilidade
  (linhas 444-451);
- acoes: `acao_enter` deve estar registrada no whitelist (linha 452);
- filtros: campo inexistente e ordem filtro antes da paginacao (linhas 453 e
  463-464);
- paginacao: instancia com `paginacao: com` exige `politica_paginacao`
  declarada (linhas 454-455);
- quebra: politica de quebra desconhecida e invalida (linha 456);
- colunas, navegacao, composicao, itens, filtros, acoes e paginacao nao podem
  ser hardcoded (linhas 457-458);
- selecao: `[␣]` nao pode existir sem `politica_selecao = multipla` (linhas
  461-462);
- restricao de navegacao: `[✥]` nao pode ser vinculado a `lancador` nem a
  `dashboard` (linhas 459-460).

## Registro em `to_do.md`

`docs/build_docs/to_do.md` criou DOC-0027 como concluido, com
`Concluido_em: 2026-07-07`, envolvendo `docs/contratos/contrato_console.md`
e `docs/build_docs/to_do.md`, e referenciando explicitamente
`docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md` como origem do
problema P1 (linhas 306-313).

## Confirmacao de escopo

Nesta tarefa de QA pos-ajuste, nenhum contrato adicional, ADR, indice, JSON
ou codigo foi alterado. O unico arquivo criado por esta tarefa foi este
relatorio:

`docs/relatorios/RELATORIO_QA_DOC-0027_CONTRATO_CONSOLE_POS_AJUSTE.md`

Observacao: antes da criacao deste relatorio, o workspace ja continha
alteracoes e arquivos nao rastreados de tarefas documentais anteriores,
incluindo contratos, ADR, indices e relatorios. Essas mudancas foram apenas
inspecionadas quando necessario para a QA e nao foram editadas nesta tarefa.
