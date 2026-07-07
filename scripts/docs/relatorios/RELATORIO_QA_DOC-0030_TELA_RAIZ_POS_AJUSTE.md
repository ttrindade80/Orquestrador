---
name: RELATORIO_QA_DOC-0030_TELA_RAIZ_POS_AJUSTE
description: QA pos-ajuste do DOC-0030 sobre o draft da tela raiz do Orquestrador
metadata:
  type: relatorio_qa
  doc_origem: DOC-0030
  status: APROVADO
  criado_em: 2026-07-07
---

# Relatorio QA - DOC-0030 - Tela raiz pos-ajuste

## Status final

`APROVADO`

Os ajustes recomendados no relatorio
`docs/relatorios/RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON.md`
foram resolvidos no draft `config/telas/orquestrador.json`. O arquivo segue
sendo um draft declarativo, nao executavel como configuracao final enquanto
DOC-B008 e DOC-B009 permanecerem abertos.

## Comandos executados

```bash
git status --short
python3 -m json.tool config/telas/orquestrador.json >/dev/null
git diff --check -- config/telas/orquestrador.json docs/build_docs/to_do.md
git diff -- config/telas/orquestrador.json docs/build_docs/to_do.md
```

Resultados:

- `git status --short`: a worktree contem alteracoes acumuladas de ciclos
  documentais anteriores, incluindo ADRs, contratos, indices, `to_do.md` e
  `config/telas/orquestrador.json` nao rastreado.
- `python3 -m json.tool config/telas/orquestrador.json >/dev/null`: aprovado,
  sem saida.
- `git diff --check -- config/telas/orquestrador.json docs/build_docs/to_do.md`:
  aprovado, sem saida.
- `git diff -- config/telas/orquestrador.json docs/build_docs/to_do.md`:
  mostrou o diff rastreado de `docs/build_docs/to_do.md`; como
  `config/telas/orquestrador.json` ainda esta nao rastreado, seu conteudo foi
  verificado por leitura direta.

## Evidencias dos ajustes

### 1. Registry de acoes pendente

Resolvido. `referencias_de_acoes` declara `status: pendente_DOC-B009` e afirma
que as acoes usadas pelos chips sao referencias declarativas conceituais
provisorias, nao implementadas. Tambem explicita que nenhuma acao executa
comando shell, nenhuma chama Python arbitrariamente e nenhuma deve ser tratada
como executavel ate o registry formal ser fechado.

Evidencias: `config/telas/orquestrador.json`, linhas 253-256; reforco em
`metadados.pendencias`, linha 10.

### 2. Colunas ajustaveis

Resolvido. `console_principal.colunas_ajustavel` deixou de ser apenas a string
vaga `"com"` e passou a ser objeto declarativo com:

- `ativo: "com"`;
- `minimo: 1`;
- `maximo: 3`;
- nota explicita de que o valor runtime de colunas nao e guardado ali.

O minimo e menor que o maximo. Nao ha valor inicial/default de coluna declarado,
portanto nao ha default fora de intervalo. Nao foi identificado armazenamento
de coluna atual ajustada em runtime.

Evidencias: `config/telas/orquestrador.json`, linhas 54-59.

### 3. Filtro pendente

Resolvido para o nivel de draft. `filtro_grupo` referencia
`campo: "pendente_DOC-B008"`, declara `atua_antes_da_paginacao: true` e registra
em nota que o campo/atributo depende dos contratos de item interno de `console`
e do registry de tipos. A chave `filtro_ativo_runtime` tem valor
`"nao_guardado_aqui"`, deixando claro que o filtro ativo atual nao esta sendo
armazenado como estado vivo.

Nao ha sinal de logica hardcoded no renderer; o chip `chip_grupos` apenas
referencia declarativamente `filtro_grupo`.

Evidencias: `config/telas/orquestrador.json`, linhas 150-157 e 240-248.

### 4. `lancador_principal` vazio

Resolvido. `lancador_principal` permanece com `itens: []`, sem inventar itens
nem `tela_destino`. O campo `pendencia_itens` registra que itens e destinos
dependem da definicao posterior das telas do sistema e preserva a regra de que
o `lancador` nao e navegavel por setas / `[✥]`.

Evidencias: `config/telas/orquestrador.json`, linhas 100-109.

### 5. `chip_estilo`

Resolvido para o nivel de draft. `chip_estilo` esta marcado como especifico,
subtipo `aciona_tela`, mas seu `tela_destino` permanece `"pendente"` com nota
explicita: placeholder nao executavel, aguardando definicao das telas do
sistema e formalizacao do registry de acoes em DOC-B009. Nao ha comando
arbitrario, chamada Python ou acao final inventada.

Evidencias: `config/telas/orquestrador.json`, linhas 202-216.

### 6. Pendencias internas

Resolvido. `metadados.pendencias` foi atualizado e menciona as pendencias
aplicaveis:

- DOC-B008: tipos internos de item de `console` e campo do `filtro_grupo`;
- DOC-B009: registry completo de acoes e tipos de chip;
- DOC-0018: contratos `cabecalho` e `estilo` ainda nao revisados formalmente;
- destinos do `lancador`;
- `chip_estilo`;
- DOC-B004, apenas em relacao ao alinhamento horizontal do dashboard.

DOC-B007 nao aparece em `metadados.pendencias`, o que esta correto porque nao
ha relacao direta registrada no JSON.

Evidencias: `config/telas/orquestrador.json`, linhas 8-16.

### 7. Estado de runtime proibido

Nao foi encontrado armazenamento de:

- pagina atual;
- item em foco atual;
- selecao atual;
- filtro atualmente ativo;
- modo verboso atual;
- coluna atual ajustada em runtime.

`modo_inicial: "normal"` e default declarativo permitido. A coluna atual nao
aparece; apenas limites declarativos aparecem. O filtro ativo atual e
explicitamente marcado como nao guardado no JSON.

Evidencias: `config/telas/orquestrador.json`, linhas 50-58 e 240-248.

## `to_do.md`

DOC-0030 esta criado como `concluido`, referencia o relatorio de origem
`RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON.md`, resume os ajustes
aplicados e preserva pendencias abertas.

Pendencias preservadas corretamente:

- DOC-B008 permanece `bloqueado_decisao`;
- DOC-B009 permanece `bloqueado_decisao`;
- DOC-0018 permanece pendente em `pronto_para_execucao`;
- destinos do `lancador` e `chip_estilo.tela_destino` continuam pendentes;
- nenhuma pendencia aberta foi fechada indevidamente por DOC-0030.

Evidencias: `docs/build_docs/to_do.md`, linhas 343-351 e 367-375.

## Escopo

No escopo declarado do DOC-0030, os arquivos envolvidos foram somente:

- `config/telas/orquestrador.json`;
- `docs/build_docs/to_do.md`.

Nao foi identificado, como parte do DOC-0030, ajuste em contratos, ADRs,
indices, outros JSONs ou codigo. A worktree, entretanto, ja contem alteracoes
acumuladas fora deste QA em contratos, ADRs, indices e relatorios; elas nao
foram produzidas por esta verificacao.

Esta tarefa de QA criou somente este relatorio:

- `docs/relatorios/RELATORIO_QA_DOC-0030_TELA_RAIZ_POS_AJUSTE.md`

## Problemas restantes

Nenhum problema bloqueante restante para o objetivo do DOC-0030.

Pendencias documentais preservadas, nao reprovantes:

- DOC-B008: definir contratos/classes dos itens internos de `console`;
- DOC-B009: definir registry de tipos, acoes, chips, filtros, origens de dados
  e validacoes;
- DOC-0018: revisar contratos remanescentes `cabecalho` e `estilo`;
- definir destinos reais do `lancador`;
- definir `tela_destino` real de `chip_estilo`.

## Conclusao

`APROVADO`. Os ajustes solicitados pelo QA do DOC-B011 foram aplicados de forma
objetiva, mantendo o JSON valido, declarativo, sem execucao arbitraria, sem
estado de runtime proibido e com as pendencias corretas preservadas.
