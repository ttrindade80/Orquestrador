---
name: REL-CONSOLIDACAO-DOC-0010-DOC-0014
description: Consolidação documental final das decisões ADR-0005, ADR-0006 e ADR-0007
metadata:
  type: relatorio_consolidacao_documental
  status: APROVADO
  data: 2026-07-06
rastreabilidade:
  docs:
    - DOC-0010
    - DOC-0011
    - DOC-0013
    - DOC-0014
  adr_relacionadas:
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
    - docs/adr/ADR-0006-renomeacao-console-dashboard.md
    - docs/adr/ADR-0007-tela-processamento-composicao.md
  relatorios_qa:
    - docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md
    - docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md
    - docs/relatorios/RELATORIO_QA_DOC-0011_ADR-0006_APLICACAO.md
    - docs/relatorios/RELATORIO_QA_DOC-0014_ADR-0007_APLICACAO.md
---

# Consolidação documental — DOC-0010 a DOC-0014

## Status final

APROVADO.

Não foram encontrados bloqueantes nem pendências obrigatórias antes da revisão
humana/commit.

## Escopo consolidado

- DOC-0010 / ADR-0005: `lancador` não é corpo navegável por `[✥]`; a navegação
  por `[✥]` fica restrita ao corpo navegável, hoje denominado `console`.
- DOC-0011 / ADR-0006: renomeação de `dado` para `console` e de `Info` para
  `dashboard`; taxonomia ativa do corpo: `console`, `lancador`, `dashboard`.
- DOC-0013 / ADR-0007: tela de processamento é composição de tipos existentes,
  não quarto tipo de corpo.
- DOC-0014: aplicação da ADR-0007 em nomenclatura, contratos e controle de
  documentação.

## Manifesto de arquivos

### ADRs

- `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`
- `docs/adr/ADR-0006-renomeacao-console-dashboard.md`
- `docs/adr/ADR-0007-tela-processamento-composicao.md`
- `docs/adr/INDICE_ADR.md`

### índices/controle

- `docs/INDICE.md`
- `docs/build_docs/to_do.md`

### contratos

- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_lancador.md`

### nomenclatura

- `docs/NOMENCLATURA.md`

### configs

- `config/barra_de_menus.json`
- `config/layout_console.json`
- `config/layout_dado.json`

### relatórios

- `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md`
- `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md`
- `docs/relatorios/RELATORIO_QA_DOC-0011_ADR-0006_APLICACAO.md`
- `docs/relatorios/RELATORIO_QA_DOC-0014_ADR-0007_APLICACAO.md`
- `docs/relatorios/RELATORIO_CONSOLIDACAO_DOCUMENTAL_DOC-0010_DOC-0014.md`

## Evidências

### E-001 — ADRs e índices

ADRs 0005, 0006 e 0007 existem fisicamente:

- `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`
- `docs/adr/ADR-0006-renomeacao-console-dashboard.md`
- `docs/adr/ADR-0007-tela-processamento-composicao.md`

As três ADRs estão indexadas em `docs/adr/INDICE_ADR.md` como aceitas em
2026-07-06. `docs/INDICE.md` lista nominalmente os três arquivos de ADR.

Classificação: OK referência existente.

### E-002 — Relatórios de QA existentes

Foram encontrados os relatórios:

- `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md`
- `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md`
- `docs/relatorios/RELATORIO_QA_DOC-0011_ADR-0006_APLICACAO.md`
- `docs/relatorios/RELATORIO_QA_DOC-0014_ADR-0007_APLICACAO.md`

Classificação: OK referência existente.

### E-003 — Fechamentos em to_do.md

`docs/build_docs/to_do.md` registra:

- DOC-0010 com `Status: concluido`, `Concluido_em: 2026-07-06`,
  QA inicial `APROVADO_COM_AJUSTES`, QA pós-ajuste `APROVADO` e
  `Resultado final: APROVADO`.
- DOC-0011 com `Status: concluido`, `Concluido_em: 2026-07-06` e próxima ação
  concluída pela aplicação registrada em DOC-0012.
- DOC-0012 com QA `RELATORIO_QA_DOC-0011_ADR-0006_APLICACAO.md — APROVADO`
  e `Resultado final: APROVADO`.
- DOC-0013 com `Status: concluido`, `Concluido_em: 2026-07-06` e próxima ação
  encaminhada para DOC-0014.
- DOC-0014 com QA `RELATORIO_QA_DOC-0014_ADR-0007_APLICACAO.md — APROVADO`
  e `Resultado final: APROVADO`.

Classificação: OK regra correta ativa.

### E-004 — JSONs válidos

Validação executada com `python -m json.tool`:

- `config/barra_de_menus.json`: OK.
- `config/layout_console.json`: OK.
- `config/layout_dado.json`: OK.

Classificação: OK regra correta ativa.

### E-005 — Taxonomia ativa final

A taxonomia ativa final aparece como `console`, `lancador` e `dashboard` em
`docs/NOMENCLATURA.md`, `docs/contratos/contrato_composicao_corpo.md` e
`docs/contratos/contrato_cabecalho.md`.

Ocorrências de `dado` aparecem como nome antigo de `console` ou como referência
histórica/transicional. Não foi encontrada ocorrência de `Info` como tipo ativo.

Classificação: OK regra correta ativa; OK histórico; OK transicional.

### E-006 — Navegabilidade por `[✥]`

`[✥]` permanece restrito a corpo tipo `console` navegável:

- `docs/NOMENCLATURA.md` declara que `[✥]` controla somente cursor de corpo
  tipo `console`.
- `docs/contratos/contrato_composicao_corpo.md` declara que `console` cobre
  partes interativas ou navegáveis por `[✥]`.
- `docs/contratos/contrato_barra_de_menus.md` declara que `[✥]` só existe
  estruturalmente quando há ao menos um corpo tipo `console` navegável.
- `config/barra_de_menus.json` declara a condição de existência estrutural
  como tela com ao menos um corpo tipo `console` navegável.

`lancador` e `dashboard` aparecem como não navegáveis por `[✥]`.

Classificação: OK regra correta ativa; OK menção negativa.

### E-007 — Migração `layout_console` / `layout_dado`

`config/layout_console.json` existe e declara:

- `name: layout_console`
- `arquivo_canonico: true`
- `substitui: config/layout_dado.json`

`config/layout_dado.json` existe e declara:

- `name: layout_dado`
- `status: obsoleto_transicional`
- `arquivo_canonico: false`
- `substituido_por: config/layout_console.json`

Documentação e contratos tratam `layout_console` como canônico e
`layout_dado` como obsoleto/transicional.

Classificação: OK regra correta ativa; OK transicional.

### E-008 — `dashboard` sem universalização indevida

`docs/NOMENCLATURA.md` explicita que a estrutura de 8 campos de resumo + Total
+ 8 marcadores pertence ao caso específico legado do sistema de survey e não é
regra universal do tipo `dashboard`.

`docs/contratos/contrato_composicao_corpo.md` registra os 8 campos e 8
marcadores como caso legado/conjunto fechado do caso tratado, sem universalizar
a estrutura para todo `dashboard`.

Classificação: OK regra correta ativa; OK histórico.

### E-009 — Tela de processamento como composição

`docs/NOMENCLATURA.md` declara que tela de processamento não é tipo de corpo e
que não existe quarto tipo de corpo para processamento. O mesmo contrato aparece
em `docs/contratos/contrato_composicao_corpo.md`.

`docs/contratos/contrato_barra_de_menus.md` registra que chips específicos de
tela de processamento não transformam processamento em tipo de corpo.

Classificação: OK regra correta ativa; OK menção negativa.

### E-010 — Fora de escopo preservado

As ocorrências de `aciona_processo`, pop-up, seleção prévia, segundo plano e
renderer de progresso aparecem como fora de escopo, pendentes de contrato
próprio ou não definidos pela decisão atual.

Classificação: OK fora de escopo.

### E-011 — Código e configs preservados

`git diff --name-only` mostra alterações em documentação e nos configs
esperados:

- `scripts/config/barra_de_menus.json`
- `scripts/config/layout_dado.json`
- `scripts/docs/INDICE.md`
- `scripts/docs/NOMENCLATURA.md`
- `scripts/docs/adr/INDICE_ADR.md`
- `scripts/docs/build_docs/to_do.md`
- `scripts/docs/contratos/contrato_barra_de_menus.md`
- `scripts/docs/contratos/contrato_cabecalho.md`
- `scripts/docs/contratos/contrato_composicao_corpo.md`
- `scripts/docs/contratos/contrato_estilo.md`
- `scripts/docs/contratos/contrato_lancador.md`

Verificação específica de código com extensões `.py`, `.sh`, `.js`, `.ts`,
`.tsx`, `.jsx`, `.rs`, `.go`, `.java`, `.c`, `.cpp`, `.h`, `.hpp` não retornou
arquivos alterados.

`git diff -- config/lancador.json config/layout_menu.json config/cabecalho.json
config/estilo.json` não retornou alterações.

Classificação: OK regra correta ativa.

## Ocorrências remanescentes classificadas

| Arquivo:linha | Trecho | Classificação | Justificativa |
|---|---|---|---|
| `docs/NOMENCLATURA.md:59` | Antigo corpo tipo `dado`; `layout_dado` obsoleto/transicional | OK transicional | Preserva rastreabilidade da migração `dado` → `console`, sem manter `dado` como tipo ativo. |
| `docs/NOMENCLATURA.md:177` | preserva as regras do antigo tipo `dado` | OK histórico | Ocorrência explica herança conceitual do `console`. |
| `docs/build_docs/to_do.md:147` | `[✥]` restrito a corpo tipo `dado` | OK histórico | Registro de origem anterior à ADR-0006; fechamento posterior migra o termo para `console`. |
| `docs/NOMENCLATURA.md:188-193` | tela de processamento não é tipo de corpo; composição de tipos existentes | OK regra correta ativa | Confirma ADR-0007 e impede quarto tipo de corpo. |
| `docs/NOMENCLATURA.md:215-217` | pop-up, seleção prévia, segundo plano, `aciona_processo`, renderer de progresso fora de escopo | OK fora de escopo | Não especifica implementação desses itens. |
| `docs/NOMENCLATURA.md:316-318` | `[✥]` controla somente `console`; `lancador` e `dashboard` não são navegáveis | OK regra correta ativa | Reforça ADR-0005 atualizada pela ADR-0006. |
| `docs/NOMENCLATURA.md:486-487` | quarto tipo identificado sem estrutura definida | OK menção negativa | Refere-se a tipo de chip específico da `barra_de_menus`, não a tipo de corpo/processamento. |
| `docs/NOMENCLATURA.md:732-736` | `dashboard` não interage; 8 campos/8 marcadores são caso legado | OK regra correta ativa | Impede universalização indevida do `dashboard`. |
| `docs/contratos/contrato_composicao_corpo.md:57` | `console` preserva regras do antigo tipo `dado` | OK histórico | `dado` aparece como nome antigo, não tipo ativo. |
| `docs/contratos/contrato_composicao_corpo.md:70-83` | processamento não é tipo de corpo; `[✥]` restrito a `console` | OK regra correta ativa | Consolida taxonomia fechada e regra de navegabilidade. |
| `docs/contratos/contrato_composicao_corpo.md:86` | não define `aciona_processo` | OK fora de escopo | Mantém a decisão fora do contrato atual. |
| `docs/contratos/contrato_composicao_corpo.md:180-194` | 8 campos e 8 marcadores no caso legado | OK histórico | Estrutura delimitada ao caso legado, sem universalização do `dashboard`. |
| `docs/contratos/contrato_barra_de_menus.md:144-161` | `[✥]` existe quando há corpo tipo `console` navegável | OK regra correta ativa | Condição estrutural correta e restrita a `console`. |
| `docs/contratos/contrato_barra_de_menus.md:231-232` | `aciona_processo` permanece fora de escopo | OK fora de escopo | Não especifica estrutura além do limite declarado. |
| `config/barra_de_menus.json:87-90` | condição/comportamento de `[✥]` para corpo tipo `console` navegável | OK regra correta ativa | Config ativo não autoriza `lancador` nem `dashboard` como navegáveis por `[✥]`. |
| `config/layout_console.json:7-9` | arquivo canônico; substitui `layout_dado` | OK regra correta ativa | `layout_console` é canônico. |
| `config/layout_dado.json:6-8` | obsoleto/transicional; não canônico; substituído por `layout_console` | OK transicional | `layout_dado` não aparece como canônico. |

## Pendências

Nenhuma pendência bloqueante. Nenhuma pendência obrigatória antes da revisão humana/commit.

## Conclusão

O pacote documental DOC-0010 a DOC-0014 está coerente com as ADRs 0005, 0006 e
0007 e pronto para revisão humana/commit documental.
