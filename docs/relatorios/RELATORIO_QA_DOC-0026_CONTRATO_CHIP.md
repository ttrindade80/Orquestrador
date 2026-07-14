---
name: RELATORIO_QA_DOC-0026_CONTRATO_CHIP
description: QA documental do contrato da classe chip referente ao DOC-0026
metadata:
  type: relatorio_qa
  scope: docs
  status: aprovado
  data: 2026-07-07
  alvo:
    - docs/contratos/contrato_chip.md
    - docs/INDICE.md
    - docs/build_docs/to_do.md
---

# Relatorio QA — DOC-0026 — Contrato `chip`

## Status final

`APROVADO`

## Escopo verificado

Foram verificados:

- `docs/contratos/contrato_chip.md`;
- `docs/INDICE.md`;
- `docs/build_docs/to_do.md`;
- compatibilidade com `docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md`;
- compatibilidade com `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`;
- compatibilidade com `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`;
- compatibilidade com `docs/contratos/contrato_tela_json.md`;
- compatibilidade com `docs/contratos/contrato_barra_de_menus.md`.

Este QA nao alterou JSON, ADR, codigo, contrato preexistente, `INDICE.md` ou
`to_do.md`. O unico arquivo criado por esta tarefa e este relatorio.

## Evidencias objetivas

### Existencia e frontmatter

- `docs/contratos/contrato_chip.md` existe.
- O frontmatter e compativel com contratos existentes: possui `name`,
  `description`, `metadata.type: contrato`, `metadata.scope: scripts`,
  `metadata.versao`, `metadata.status: ativo` e bloco de rastreabilidade.
- A rastreabilidade referencia `NOMENCLATURA`, ADR-0008,
  `contrato_tela_json.md`, `contrato_barra_de_menus.md` e aplica ADR-0004,
  ADR-0005 e ADR-0008.

### Natureza declarativa

- A secao 2 define `chip` como entidade declarativa de interface textual.
- A secao 2 declara explicitamente que `chip` nao e acao por si so.
- A secao 2 declara que cada chip concreto e instanciado no `tela.json`.
- A secao 16 define acao de chip como declarativa, registrada/whitelisted.
- A secao 16 proibe comando arbitrario, chamada livre de script e logica
  procedural, incluindo exemplo proibido com `python script_x.py --algo`.

### Escopo e separacoes

- A secao 3 registra que o uso primario atual de `chip` e a
  `barra_de_menus`.
- A secao 3 distingue chips internos de itens do `lancador` dos chips da
  `barra_de_menus`.
- A secao 15 reforca que chips da `barra_de_menus` nao sao chips internos dos
  itens do `lancador`.
- A secao 13 define que a `barra_de_menus` lista, ordena/distribui e exibe
  chips declarados, sem criar chip nao declarado nem decidir composicao.

### Campos e tipos

- A secao 4 define os campos minimos: `id`, `tipo`, `tecla`, `texto`, `acao`
  ou `referencia_regra`, `regra_existencia`, `regra_ativo` e
  `forma_exibicao`.
- A secao 5 registra os tipos conceituais iniciais: `acao`, `filtro`,
  `alternancia`, `navegacao`, `informativo` e `especifico`.
- A secao 6 resolve a diferenca entre o uso documental de `canonico` no
  contrato da barra e a taxonomia funcional adotada pelo contrato de `chip`.

### Chips canonicos e notacoes

- A secao 7 trata chips canonicos como instancias padronizadas, nao lista
  hardcoded no renderer.
- A secao 7 declara que `[Esc]`, `[<][>]`, `[-][+]`, `[#]`, `[⇆]`, `[✥]`,
  `[␣]`, `[⏎]`, `[V]` e `[?]` sao identificadores documentais/canonicos,
  nao valores renderizaveis obrigatorios.

### Existencia, ativo/inativo e estilo

- A secao 8 define `regra_existencia` como regra estrutural, avaliada na carga
  do `tela.json`, sem mudanca durante a tela aberta.
- A secao 9 define `regra_ativo` como regra dinamica recalculada a cada
  render.
- A secao 9 determina que chip inativo continua existindo, usa `cor_inativo`
  do schema de estilo e nao reage a acionamento.
- A secao 12 define que a aparencia vem exclusivamente de `config/estilo.json`
  e que `cor_inativo`/`cor_alerta` pertencem ao schema de estilo universal.
- A secao 18 do contrato da barra confirma a mesma relacao com
  `contrato_estilo.md`.

### Relacoes com `console`, `lancador` e `dashboard`

- A secao 14 registra que `[✥]` depende de `console` navegavel.
- A secao 14 registra que `[␣]` depende de selecao multipla.
- A secao 14 registra que `[⏎]` depende da acao declarada pelo item em foco.
- A secao 14 registra que filtros atuam sobre dados vinculados ao `console`.
- A secao 14 registra que `[V]` alterna modo verboso quando permitido.
- A secao 15 registra que `[✥]` nao navega `lancador`.
- A secao 15 registra que `[✥]` nao navega `dashboard`.

### Validacao e pendencias

- A secao 17 cobre criterios minimos de validacao: campos obrigatorios,
  acao registrada, filtro existente, alternancia existente, tecla duplicada,
  proibicao de hardcoding, restricoes de `[✥]`, `[␣]` e `[⏎]`.
- A secao 18 registra pendencias fora de escopo sem tentar resolver
  implementacao, registry completo, JSON real de tela, dispatcher de acoes ou
  layout final detalhado.

### Indice e `to_do.md`

- `docs/INDICE.md` inclui `contrato_chip.md` na ordem de leitura e na
  estrutura esperada.
- `docs/build_docs/to_do.md` registra DOC-0026 como concluido.
- `docs/build_docs/to_do.md` registra DOC-B006 como concluido e resolvido pelo
  contrato criado em DOC-0026.

## Comandos executados

```bash
git status --short
git diff --check -- docs/contratos/contrato_chip.md docs/INDICE.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_chip.md docs/INDICE.md docs/build_docs/to_do.md
```

Resultados:

- `git status --short` mostrou alteracoes documentais ja presentes no working
  tree, incluindo `docs/INDICE.md`, `docs/NOMENCLATURA.md`,
  `docs/adr/INDICE_ADR.md`, `docs/build_docs/to_do.md`,
  `docs/contratos/contrato_barra_de_menus.md`,
  `docs/contratos/contrato_composicao_corpo.md`,
  `docs/contratos/contrato_lancador.md` e arquivos novos ainda nao rastreados,
  incluindo `docs/contratos/contrato_chip.md`.
- `git diff --check -- docs/contratos/contrato_chip.md docs/INDICE.md docs/build_docs/to_do.md`
  nao retornou erros.
- `git diff -- docs/contratos/contrato_chip.md docs/INDICE.md docs/build_docs/to_do.md`
  confirma que `docs/INDICE.md` passou a listar `contrato_chip.md` e que
  `docs/build_docs/to_do.md` passou a registrar DOC-0026 como concluido e
  DOC-B006 como encerrado.

Observacao: por `contrato_chip.md` ser arquivo novo ainda nao rastreado, o
`git diff` sem `--cached` nao exibe seu conteudo. A existencia e o conteudo do
arquivo foram verificados por leitura direta.

## Problemas encontrados

Nenhum problema bloqueante encontrado.

Nao ha recomendacao obrigatoria de ajuste para `contrato_chip.md`.

## Recomendacoes de ajuste

Sem ajustes necessarios para aprovacao.

Recomendacao nao bloqueante: quando DOC-B009 for executado, manter a distincao
ja registrada entre tipos funcionais de chip e o atributo documental
"canonico", para evitar que o registry futuro reintroduza ambiguidade.

## Confirmacao de integridade do escopo

Confirmado: esta tarefa de QA criou somente
`docs/relatorios/RELATORIO_QA_DOC-0026_CONTRATO_CHIP.md`.

Nenhum JSON, ADR, codigo ou contrato preexistente foi alterado por esta tarefa
de QA.
