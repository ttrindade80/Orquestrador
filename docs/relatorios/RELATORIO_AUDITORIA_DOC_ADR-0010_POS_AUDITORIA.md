---
name: RELATORIO_AUDITORIA_DOC_ADR-0010_POS_AUDITORIA
description: Re-auditoria documental pos-correcao da ADR-0010 e contratos JSON relacionados
metadata:
  type: relatorio_auditoria_documental
  status: QA_APPROVED_WITH_NOTES
  data: 2026-07-08
  escopo:
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
---

# Relatório de Auditoria Documental Pós-Correção — ADR-0010

## Status final

QA_APPROVED_WITH_NOTES

Os bloqueios documentais apontados na auditoria anterior foram removidos. Não
foi encontrada contradição ativa remanescente nem extrapolação de escopo fora
do conjunto documental esperado. Restam apenas notas não bloqueantes de
rastreabilidade e transição.

## Escopo auditado

Esta re-auditoria verificou a correção pós-auditoria registrada em
`docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md`, com foco nos bloqueios
anteriores em:

```text
docs/NOMENCLATURA.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
```

Também foi verificada a coerência com a ADR-0010, contratos centrais, relatório
IMP-DOC original e escopo Git da rodada documental.

## Arquivos lidos

Leitura obrigatória realizada:

```text
docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
```

Leitura adicional de coerência realizada:

```text
docs/adr/ADR-0006-renomeacao-console-dashboard.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_console.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
```

## Verificações executadas

Comandos obrigatórios executados:

```bash
git status --short
git diff --stat
git diff --name-only
git diff -- docs/NOMENCLATURA.md
git diff -- docs/contratos/contrato_json_tela_minima.md
git diff -- docs/contratos/contrato_json_dashboard.md
git diff -- docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
grep -R "posicao_dashboard\|posição do dashboard\|Posição do dashboard\|dashboard.*eixo\|eixo.*dashboard\|dashboard.*não.*afetado.*tiling\|tiling.*dashboard" docs/NOMENCLATURA.md docs/contratos docs/adr -n
git status --short tela config tests
git diff --name-only -- tela config tests
```

Observação operacional: `git diff -- docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md`
não mostrou conteúdo porque o arquivo está não rastreado; seu conteúdo foi lido
diretamente.

## Estado inicial do git

`git status --short` no início da auditoria:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
?? docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/docs/NOMENCLATURA.md                       | 21 ++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 81 ++++++++++++++--------
 scripts/docs/contratos/contrato_json_dashboard.md  | 24 +++++--
 .../docs/contratos/contrato_json_tela_minima.md    | 21 ++++--
 .../contratos/contrato_processo_desenvolvimento.md | 47 ++++++++++++-
 scripts/docs/contratos/contrato_tela_json.md       | 21 +++++-
 7 files changed, 164 insertions(+), 52 deletions(-)
```

`git diff --name-only`:

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_dashboard.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
```

## Auditoria dos bloqueios anteriores

| Bloqueio anterior | Resultado | Evidência |
|---|---|---|
| `NOMENCLATURA.md` mantinha `dashboard` como eixo próprio na seção 1.4 | Removido | A seção 1.4 agora declara que `console`, `lancador` e `dashboard` seguem a composição declarativa geral do `corpo`; `posicao_dashboard` está descontinuado como eixo independente. |
| `contrato_json_tela_minima.md` dizia que `arranjo` não decide `dashboard` | Removido | As seções 4.1 e 5.1 agora tratam `arranjo` como relevante para elementos funcionais do corpo, incluindo `dashboard`, e limitam `posicao_dashboard` a compatibilidade transicional. |
| `contrato_json_dashboard.md` tratava `posicao_dashboard` como regra ativa independente | Removido | A seção 4, a tabela da seção 5 e V-7 agora classificam o campo como transicional/descontinuado e remetem o posicionamento à composição geral do corpo. |
| IMP-DOC original marcou conclusão sem detectar contradições | Tratado | O relatório complementar preserva o histórico, registra a auditoria bloqueante e documenta a correção pós-auditoria sem alterar o IMP-DOC original. |

## Auditoria de NOMENCLATURA.md

A correção é adequada. A seção 1.4 não mantém mais a regra ativa de que
`tiling` nunca decide a posição do `dashboard` por ele ser eixo próprio. A
seção 3 declara que a posição do `dashboard` é controlada pela estrutura
declarativa geral do `corpo`, e a seção 10 afirma que `dashboard` é elemento
funcional do corpo como `console` e `lancador`.

Não foi encontrada reintrodução de `dashboard` como eixo especial externo ao
mecanismo geral de composição.

## Auditoria de contrato_json_tela_minima.md

A correção é adequada. O contrato não mantém regra ativa dizendo que
`corpo.arranjo` é exclusivo de `console`/`lancador` ou que não decide
`dashboard`.

As ocorrências de `posicao_dashboard` estão restritas ao tratamento
transicional/descontinuado, com compatibilidade temporária para H-0011A.

## Auditoria de contrato_json_dashboard.md

A correção é adequada. O contrato deixa claro que:

- o `dashboard` é passivo, opcional e declarado em `corpo.elementos[]`;
- o contrato trata o envelope e os campos/conteúdo internos da instância;
- as regras de composição e posicionamento geral pertencem a
  `contrato_composicao_corpo.md`;
- `regras_exibicao.posicao_dashboard` é campo transicional/descontinuado, não
  eixo independente de `arranjo` nem de `tiling`.

Nota não bloqueante: o exemplo mínimo ainda contém `posicao_dashboard`, mas o
texto imediatamente circundante marca o campo como transicional e superado
pela ADR-0010. Isso é aceitável para rastreabilidade e compatibilidade.

## Auditoria do relatório pós-auditoria

`docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md` registra corretamente:

- a origem no bloqueio da auditoria anterior;
- os três bloqueios B-1, B-2 e B-3;
- os arquivos alterados na correção pós-auditoria;
- a preservação do relatório IMP-DOC original;
- a razão para não alterar retroativamente o relatório original.

O relatório não falsifica histórico: ele reconhece que o IMP-DOC anterior foi
superado pela auditoria e que a superação ocorre por relatório complementar.

## Busca de contradições remanescentes

Resultado do `grep` obrigatório, com classificação:

| Ocorrência | Classificação | Justificativa |
|---|---|---|
| `docs/NOMENCLATURA.md:142` | regra ativa coerente | Campo `posicao_dashboard` descontinuado como eixo independente. |
| `docs/NOMENCLATURA.md:284` | regra ativa coerente | Posição do dashboard controlada pela estrutura declarativa geral do corpo. |
| `docs/NOMENCLATURA.md:884` | regra ativa coerente | Tiling agora inclui composição de múltiplos elementos do corpo e descontinua eixo separado. |
| `docs/contratos/contrato_json_tela_minima.md:122` | campo transicional/descontinuado aceitável | `posicao_dashboard` aparece somente como campo descontinuado com compatibilidade H-0011A. |
| `docs/contratos/contrato_json_tela_minima.md:156` | campo transicional/descontinuado aceitável | Mesma classificação, sem regra ativa independente. |
| `docs/contratos/contrato_json_dashboard.md:89` | histórico/rastreabilidade aceitável | Exemplo JSON preserva campo legado, explicado pelo texto circundante. |
| `docs/contratos/contrato_json_dashboard.md:99` | campo transicional/descontinuado aceitável | Campo explicitamente superado pela ADR-0010. |
| `docs/contratos/contrato_json_dashboard.md:102` | regra ativa coerente | Afirma que o campo não é eixo independente de `arranjo` nem de `tiling`. |
| `docs/contratos/contrato_json_dashboard.md:120` | campo transicional/descontinuado aceitável | Tabela marca campo como descontinuado. |
| `docs/contratos/contrato_json_dashboard.md:154` | regra ativa coerente | V-7 declara composição geral do corpo como fonte do posicionamento. |
| `docs/contratos/contrato_composicao_corpo.md:128-129` | regra ativa coerente | `dashboard` é elemento opcional do corpo, não eixo universal separado. |
| `docs/contratos/contrato_composicao_corpo.md:149-157` | campo transicional/descontinuado aceitável | `posicao_dashboard` descontinuado e mantido apenas por compatibilidade H-0011A. |
| `docs/contratos/contrato_composicao_corpo.md:267` | regra ativa coerente | Posicionamento por composição declarada; campo separado descontinuado. |
| `docs/contratos/contrato_composicao_corpo.md:359` | regra ativa coerente | Tiling inclui `dashboard` como elemento funcional. |
| `docs/contratos/contrato_composicao_corpo.md:425` | regra ativa coerente | R-5 atualizado para composição geral do corpo. |
| `docs/contratos/contrato_composicao_corpo.md:493-494` | regra ativa coerente | Critério de validação impede eixo separado independente. |
| `docs/contratos/contrato_composicao_corpo.md:541-542` | nota não bloqueante | Pendência de migração/descarte do campo legado. |
| `docs/adr/ADR-0006-renomeacao-console-dashboard.md:144` | histórico/rastreabilidade aceitável | ADR antiga lista tarefa de renomeação, sem decidir posicionamento atual. |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:3` | histórico/rastreabilidade aceitável | Frontmatter descreve a decisão. |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:37-41` | histórico/rastreabilidade aceitável | Contexto histórico do problema antigo. |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:95-101` | regra ativa coerente | Decisão formal descontinua `posicao_dashboard`. |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:176-231` | histórico/rastreabilidade aceitável | Consequências, pendências e alternativa rejeitada. |

Nenhuma ocorrência foi classificada como contradição bloqueante.

## Auditoria de escopo Git

Não houve alteração em `tela/`, `config/` ou `tests/`:

```text
git status --short tela config tests
git diff --name-only -- tela config tests
```

Ambos os comandos não retornaram saída.

As alterações rastreadas e arquivos não rastreados estão dentro do escopo
documental descrito para a rodada, incluindo os arquivos pós-auditoria
permitidos e os artefatos anteriores de ADR-0010/H-0011 bloqueado.

## Coerência com H-0011A–D

A documentação está apta para permitir a futura reescrita do H-0011 como
sequência H-0011A–D:

- `dashboard` é elemento funcional do corpo;
- `dashboard` não é eixo especial externo ao mecanismo geral de composição;
- composição visual pertence à estrutura declarativa do corpo;
- `console`, `lancador` e `dashboard` são posicionados pela composição do corpo;
- campos internos de `dashboard` continuam responsabilidade da instância/tipo
  `dashboard`;
- `dashboard` permanece passivo e não navegável por `[✥]`;
- `console` permanece o único tipo navegável por `[✥]`;
- `lancador` permanece não navegável por `[✥]`.

A ADR-0010 está registrada no `INDICE_ADR.md` com status `aceita` e permanece
coerente com `contrato_composicao_corpo.md` e `contrato_tela_json.md`.

## Achados bloqueantes

Nenhum.

## Achados não bloqueantes

1. `docs/contratos/contrato_json_dashboard.md` mantém `posicao_dashboard` no
   exemplo mínimo, mas com marcação explícita de campo transicional superado
   pela ADR-0010. Classificação: rastreabilidade/compatibilidade aceitável.
2. `docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md` está não rastreado no
   Git no momento da auditoria. Classificação: nota operacional não bloqueante,
   pois o escopo permite a criação do relatório complementar e o conteúdo foi
   auditado diretamente.
3. `git diff --stat` e `git diff --name-only` não listam arquivos não
   rastreados; por isso o estado completo deve ser lido junto com
   `git status --short`.

## Recomendações

- Prosseguir com a documentação/reescrita futura de H-0011A–D a partir da
  ADR-0010 e dos contratos corrigidos.
- Manter `posicao_dashboard` apenas como compatibilidade transicional até o
  handoff específico de migração/descarte.
- Ao preparar commit futuro, incluir explicitamente os arquivos não rastreados
  relevantes da rodada documental, caso o fluxo do projeto peça versionamento
  desta entrega.

## Estado final do git

`git status --short` após a criação deste relatório:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
?? docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_ADR-0010_POS_AUDITORIA.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
```

Verificações finais de escopo:

```text
git status --short tela config tests
git diff --name-only -- tela config tests
```

Ambos os comandos não retornaram saída.

Nenhum commit foi realizado.
