---
name: relatorio-qa-doc-0016-doc-0023-tela-json
description: QA documental curta da ADR-0008 e do contrato tela.json
metadata:
  type: relatorio_qa
  scope: docs
  status: aprovado_com_ajustes
  data: 2026-07-07
---

# Relatorio QA — DOC-0016 / DOC-0023 — `tela.json`

## Status final

`APROVADO_COM_AJUSTES`

## Escopo verificado

- Indexacao da ADR-0008 em `docs/adr/INDICE_ADR.md`.
- Listagem de `contrato_tela_json.md` em `docs/INDICE.md`.
- Registro minimo de `tela.json` em `docs/NOMENCLATURA.md`.
- Registro de DOC-0016, DOC-0023 e pendencias derivadas em `docs/build_docs/to_do.md`.
- Coerencia entre ADR-0008 e `contrato_tela_json.md`.
- Coerencia com contratos ativos antigos, considerando pendencias posteriores registradas.
- Natureza declarativa de `tela.json`, separacao entre configuracao e estado de runtime, acoes registradas/whitelisted, filtros antes da paginacao, `console` como container generico e instancias declaradas de `dashboard`/`lancador`.
- Ausencia de alteracao de codigo e ausencia de criacao de JSON real de tela.
- Estado Git dos arquivos novos e modificados.

## Evidencias objetivas

### Indices

- `docs/adr/INDICE_ADR.md:38` lista `ADR-0008 | modelo de configuração por tela | aceita | 2026-07-07`.
- `docs/INDICE.md:39` inclui `contrato_tela_json.md` na ordem de leitura dos contratos ativos.
- `docs/INDICE.md:68` inclui `contrato_tela_json.md` na estrutura esperada de `docs/contratos/`.
- `docs/INDICE.md:78` inclui `ADR-0008-modelo-configuracao-por-tela.md` na estrutura esperada de ADRs.
- `docs/INDICE.md:102` registra a migracao para JSON por tela e referencia `contrato_tela_json.md`.

### Nomenclatura

- `docs/NOMENCLATURA.md:63` registra `Tela configurável | tela.json` com contrato criado e aplicacao ampla da ADR-0008 ainda pendente.
- `docs/NOMENCLATURA.md:221` abre secao especifica para `tela.json`.
- `docs/NOMENCLATURA.md:223-243` define `tela.json` como declaracao configuravel, declarativa e nao procedural, com campos minimos e referencia ao contrato ativo.
- O registro e minimo e nao antecipa regras detalhadas alem do essencial; os detalhes ficam no contrato.

### To Do

- `docs/build_docs/to_do.md:219-226` registra DOC-0016 como `concluido`, com ADR-0008 criada e indexada.
- `docs/build_docs/to_do.md:276-283` registra DOC-0023 como `concluido`, com `contrato_tela_json.md` criado e pendencias derivadas.
- `docs/build_docs/to_do.md:228-274` registra aplicacoes posteriores da ADR-0008 em nomenclatura, contratos afetados e indice como DOC-0017 a DOC-0022.
- `docs/build_docs/to_do.md:285-289` registra DOC-0024 para revisar `console` como container generico.
- `docs/build_docs/to_do.md:295-323` registra pendencias derivadas DOC-B006 a DOC-B011 para `chip`, arquivamento transicional, itens internos de `console`, registry, formato real/caminho dos JSONs de tela e draft real da tela raiz.

### Coerencia ADR-0008 x contrato `tela_json`

- ADR-0008 define JSON por tela e instancias de `lancador`, `dashboard`, `console` e `barra_de_menus` em `docs/adr/ADR-0008-modelo-configuracao-por-tela.md:58-90`.
- O contrato materializa essa decisao em `docs/contratos/contrato_tela_json.md:35-48`, listando estrutura, corpo, instancias, chips, filtros, bindings e acoes registradas.
- ADR-0008 declara que nao define o schema final em `docs/adr/ADR-0008-modelo-configuracao-por-tela.md:145-149`; DOC-0023 materializa o contrato conceitual posterior, sem criar JSON real.
- ADR-0008 preserva `config/estilo.json` como biblioteca global em `docs/adr/ADR-0008-modelo-configuracao-por-tela.md:105-114`; o contrato preserva essa separacao em `docs/contratos/contrato_tela_json.md:625-629`.

### Regras especificas verificadas

- Declarativo, nao procedural: `docs/contratos/contrato_tela_json.md:51-52`, `529` e `633-646`.
- Separacao configuracao x estado de runtime: `docs/contratos/contrato_tela_json.md:115-135`.
- Acoes whitelisted/registradas, sem comando arbitrario: `docs/contratos/contrato_tela_json.md:502-503`.
- Filtros antes da paginacao: `docs/contratos/contrato_tela_json.md:365` e `573`.
- `console` como container generico de itens heterogeneos: `docs/contratos/contrato_tela_json.md:279-303`.
- `dashboard` como instancia declarada, nao classe universal fixa: `docs/contratos/contrato_tela_json.md:240-275`.
- `lancador` como instancia declarada no JSON da tela: `docs/contratos/contrato_tela_json.md:208-236`.
- `barra_de_menus` como instancia declarada pela tela: `docs/contratos/contrato_tela_json.md:457-464`.

### Contratos ativos antigos

- `contrato_composicao_corpo.md`, `contrato_lancador.md`, `contrato_barra_de_menus.md`, `contrato_cabecalho.md` e `contrato_estilo.md` ainda preservam regras do modelo anterior ou transicional, como declaracao por classe de tela e JSONs por componente.
- Essa diferenca esta coberta por pendencias posteriores: DOC-0017 a DOC-0022, DOC-0024 e DOC-B006 a DOC-B011.
- Nao foi encontrada contradicao silenciosa sem pendencia registrada.

## Comandos executados

```text
$ git status --short
 M docs/INDICE.md
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/build_docs/to_do.md
?? docs/adr/ADR-0008-modelo-configuracao-por-tela.md
?? docs/contratos/contrato_tela_json.md
```

```text
$ git diff --check
<sem saida>
```

```text
$ git diff --stat
 scripts/docs/INDICE.md           |   8 +--
 scripts/docs/NOMENCLATURA.md     |  28 ++++++++++-
 scripts/docs/adr/INDICE_ADR.md   |   1 +
 scripts/docs/build_docs/to_do.md | 104 +++++++++++++++++++++++++++++++++++++++
 4 files changed, 137 insertions(+), 4 deletions(-)
```

Observacao: os comandos acima foram executados antes da criacao deste relatorio.

## Problemas encontrados

1. Ajuste menor de rastreabilidade em `docs/build_docs/to_do.md`.

   DOC-0023 registra que as pendencias derivadas foram registradas em DOC-0017 a DOC-0022, DOC-0024 e DOC-B006 a DOC-B010 (`docs/build_docs/to_do.md:283`), mas existe tambem DOC-B011 (`docs/build_docs/to_do.md:320-323`) derivado do contrato `tela_json`, para criar o draft real da tela raiz do Orquestrador.

   Impacto: baixo. A pendencia existe e esta bem descrita, mas a frase de proxima acao de DOC-0023 omite DOC-B011.

## Recomendacoes de ajuste

- Em tarefa documental posterior, ajustar a linha de proxima acao de DOC-0023 para incluir DOC-B011 ou explicitar que DOC-B011 e uma pendencia operacional derivada de DOC-B010.
- Manter DOC-0017 a DOC-0022 como tarefas de aplicacao ampla da ADR-0008 nos contratos antigos, pois elas explicam a transicao e evitam contradicao silenciosa.

## Arquivos verificados

- `docs/INDICE.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_estilo.md`

## Confirmacoes finais

- Nenhum codigo foi alterado por esta QA.
- Nenhum JSON real de tela foi criado.
- Antes da criacao deste relatorio, os arquivos novos apareciam como nao rastreados no `git status --short`: `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` e `docs/contratos/contrato_tela_json.md`.
- A unica alteracao feita por esta QA foi a criacao deste relatorio em `docs/relatorios/RELATORIO_QA_DOC-0016_DOC-0023_TELA_JSON.md`.
