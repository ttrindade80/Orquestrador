---
name: RELATORIO_QA_DOC-0021_CONTRATO_BARRA_DE_MENUS_ADR-0008
description: QA documental da aplicacao da ADR-0008 no contrato da barra_de_menus
metadata:
  type: relatorio_qa
  escopo: DOC-0021
  status_final: APROVADO_COM_AJUSTES
  data: 2026-07-07
---

# Relatorio QA — DOC-0021 — contrato_barra_de_menus + ADR-0008

## Status final

`APROVADO_COM_AJUSTES`

O conteudo normativo de `docs/contratos/contrato_barra_de_menus.md` aplica
corretamente a ADR-0008 para o escopo do DOC-0021. A aprovacao fica com ajuste
porque o `git status --short` mostra outros contratos, ADRs e indices alterados
no worktree atual; portanto, a confirmacao de exclusividade da tarefa nao pode
ser dada sem ressalva.

## Escopo verificado

Foram lidos e confrontados:

- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md`
- `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_barra_de_menus.md`

Comandos executados:

```bash
git status --short
git diff --check -- docs/contratos/contrato_barra_de_menus.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_barra_de_menus.md docs/build_docs/to_do.md
```

## Evidencias objetivas

- `contrato_barra_de_menus.md` esta em `versao: "0.2"` e `status: ativo`
  (linhas 4-8).
- A rastreabilidade inclui ADR-0004, ADR-0005 e ADR-0008 em `adrs_aplicadas`
  (linhas 9-15).
- A `barra_de_menus` foi definida como regiao fixa inferior e como instancia
  declarada no `tela.json` (linhas 45-65).
- A distincao entre `barra_de_menus` e `lancador` foi preservada: a barra fica
  fora do corpo, e chips de itens do `lancador` nao pertencem a ela
  (linhas 69-92).
- A lista concreta de chips, textos, teclas, acoes e regras da instancia vem
  do `tela.json`; `config/barra_de_menus.json` foi marcado como artefato ativo
  transicional, a reavaliar/migrar conforme ADR-0008 (linhas 111-128).
- Chips foram tratados como entidades declarativas com campos conceituais
  `id`, `tipo`, `tecla`, `texto`, `acao`, `regra_existencia`,
  `regra_ativo` e `forma_exibicao` (linhas 132-168).
- Chips canonicos foram tratados como instancias padronizadas, nao lista
  hardcoded (linhas 161-164).
- A futura classe/contrato `chip` ficou como pendencia DOC-B006, sem ser criada
  nesta tarefa (linhas 166-168 e 630-635).
- `[✥]` ficou restrito a `console` navegavel, sem navegar `lancador` nem
  `dashboard` (linhas 301-329 e 563-566).
- `[␣]` ficou restrito a selecao multipla (linhas 333-344).
- `[⏎]` ficou dependente de acao valida do item em foco, com acao pertencendo
  ao item/binding, nao a tela monolitica (linhas 265-297 e 549-552).
- Filtros foram formalizados como declarativos e aplicados antes da paginacao
  (linhas 348-381).
- `[V]` foi formalizado como alternancia de modo verboso quando permitido
  (linhas 385-399).
- Acoes em chips foram registradas/whitelisted, com proibicao de comando
  arbitrario (linhas 403-439 e 558-561).
- A distribuicao da barra foi declarada por instancia, incluindo lista concreta
  de chips, regra de distribuicao e parametros visuais locais (linhas 467-484).
- Os criterios de validacao cobrem barra sem `chips[]`, chip sem `id`, sem
  `tecla`, sem `texto`, chip acionavel sem acao, tecla duplicada, acao nao
  registrada, filtro inexistente, `[✥]` indevido em `lancador`/`dashboard`,
  `[␣]` sem selecao multipla e hardcoding pelo renderer (linhas 570-626).
- `to_do.md` marca DOC-0021 como `concluido` e registra que DOC-B006 permanece
  como pendencia para contrato/classe `chip` (linhas 262-269 e 307-310).
- `to_do.md` atualiza DOC-0018 coerentemente: `contrato_barra_de_menus.md` foi
  tratado em DOC-0021, restando `contrato_cabecalho.md` e
  `contrato_estilo.md` (linhas 237-243).
- `git diff --check -- docs/contratos/contrato_barra_de_menus.md docs/build_docs/to_do.md`
  nao produziu saida, indicando ausencia de erros de whitespace nesses arquivos.

## Problemas encontrados

1. Confirmacao de exclusividade com ressalva.

   O comando `git status --short` mostrou alteracoes em outros arquivos alem de
   `docs/contratos/contrato_barra_de_menus.md` e `docs/build_docs/to_do.md`:
   `docs/INDICE.md`, `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
   `docs/contratos/contrato_composicao_corpo.md`,
   `docs/contratos/contrato_lancador.md`, alem de novos arquivos de ADR,
   contrato e relatorios. Nao foram observadas alteracoes em JSON ou codigo no
   `git status`, mas ha outros contratos, ADRs e indices modificados no
   worktree.

   Assim, este QA nao confirma que nenhum outro contrato, ADR ou indice foi
   alterado no estado atual do repositorio. Pelo conteudo de `to_do.md`, essas
   alteracoes parecem pertencer a outras tarefas da aplicacao da ADR-0008
   (DOC-0016, DOC-0017, DOC-0020, DOC-0023 e DOC-0025), mas a exclusividade do
   DOC-0021 deve ser verificada por diff/commit isolado.

## Recomendacoes de ajuste

- Isolar o pacote DOC-0021 em commit ou diff proprio contendo apenas
  `docs/contratos/contrato_barra_de_menus.md` e `docs/build_docs/to_do.md`, ou
  registrar explicitamente que o worktree atual agrega varias tarefas da
  aplicacao da ADR-0008.
- Antes do fechamento final, executar nova verificacao de escopo com
  `git diff --name-only` contra a base esperada do DOC-0021.

## Confirmacao de alteracoes fora do escopo

Durante este QA, somente este relatorio foi criado.

Quanto ao estado preexistente do worktree, nao e possivel confirmar sem
ressalva que nenhum outro contrato, JSON, ADR, indice ou codigo foi alterado
por esta tarefa: o `git status --short` mostra outros contratos, ADRs e indices
alterados/untracked. Nao ha JSON nem codigo listado como alterado no status
observado.
