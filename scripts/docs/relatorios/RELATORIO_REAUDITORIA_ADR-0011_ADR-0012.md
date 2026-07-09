# Relatório de Reauditoria — ADR-0011 e ADR-0012

## Status

QA_REJECTED

## Contexto

Reauditoria documental das correções pós-auditoria aplicadas à documentação
ADR-0011/ADR-0012.

A auditoria anterior havia retornado dois achados bloqueantes:

1. contradição ativa entre chips canônicos sempre presentes e a ADR-0012;
2. referências operacionais residuais a H-0011A-D em contratos ativos.

Esta reauditoria verificou apenas documentação. Não foram alterados código,
JSONs, handoffs nem contratos. O único arquivo criado por esta etapa é este
relatório.

## Arquivos lidos

- `docs/relatorios/RELATORIO_AUDITORIA_ADR-0011_ADR-0012.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md`
- `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_chip.md`

## Verificações executadas

```text
$ git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
?? docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
?? docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0011_ADR-0012.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md
```

```text
$ git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 30 +++++++----
 scripts/docs/adr/INDICE_ADR.md                     |  2 +
 scripts/docs/contratos/contrato_barra_de_menus.md  | 40 ++++++++++-----
 .../docs/contratos/contrato_composicao_corpo.md    | 58 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    | 14 ++++--
 scripts/docs/contratos/contrato_tela_json.md       | 33 ++++++++----
 6 files changed, 121 insertions(+), 56 deletions(-)
```

```text
$ git diff --name-only
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

Busca direcionada executada:

```bash
grep -R "sempre.*chip\|chips.*sempre\|todos os chips canônicos\|conjunto canônico completo\|H-0011A\|H-0011B\|H-0011C\|H-0011D\|H-0011A-D" -n docs/NOMENCLATURA.md docs/contratos docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md || true
```

## Reavaliação do bloqueio 1 — chips canônicos

Resolvido.

A documentação agora distingue corretamente:

- catálogo/semântica canônica de chips;
- presença declarativa do chip em cada tela.

Evidências principais:

- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` afirma que
  canônico define semântica e ordem quando o chip está presente, não presença
  obrigatória em toda tela.
- `docs/NOMENCLATURA.md` afirma que a `barra_de_menus` não contém todos os
  chips canônicos por padrão e que cada tela declara apenas os chips
  aplicáveis.
- `docs/contratos/contrato_barra_de_menus.md` substitui a noção de chips de
  existência sempre presente por "chips canônicos de semântica fixa" e declara
  que a presença é por tela.
- `docs/contratos/contrato_barra_de_menus.md` mantém invariantes de posição
  apenas para chips declarados; o renderer não inventa chips ausentes.

Não foi encontrada regra ativa exigindo que toda tela contenha todos os chips
canônicos, que o Orquestrador declare todos por padrão, que o renderer complete
chips ausentes ou que testes esperem conjunto global obrigatório.

## Reavaliação do bloqueio 2 — referências H-0011A-D

Parcialmente resolvido, mas ainda há resíduo bloqueante.

As referências em `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
e `docs/contratos/contrato_tela_json.md` foram corretamente reenquadradas como
histórico/canceladas/não orientadoras.

Entretanto, `docs/contratos/contrato_json_dashboard.md` ainda contém referência
operacional futura a H-0011A:

- `docs/contratos/contrato_json_dashboard.md:104-105`: JSONs existentes podem
  ser honrados por compatibilidade em H-0011A; migração/descarte ocorrerá em
  handoff específico após H-0011A.
- `docs/contratos/contrato_json_dashboard.md:120`: o campo
  `regras_exibicao.posicao_dashboard` pode ser honrado por compatibilidade em
  H-0011A.
- `docs/contratos/contrato_json_dashboard.md:157`: migração/descarte ocorrerá
  em handoff específico após H-0011A.

Essas ocorrências não estão classificadas como histórico/canceladas/não
orientadoras. Em contrato ativo, elas ainda indicam H-0011A como marco
operacional futuro, o que contradiz o critério de que H-0011A-D não deve
orientar novos ciclos.

## Verificação de escopo

`git status --short`, `git diff --stat` e `git diff --name-only` mostram
alterações apenas em documentação sob `docs/`.

Não houve alteração em:

- `config/`
- `tela/`
- `docs/handoff/`

A documentação auditada não tenta migrar JSONs agora, não implementa aliases
agora, não remove chips do Orquestrador agora, não cria H-0014 e não tenta
resolver a divergência `dashboard.campos[]` vs `conteudo`/`regras_exibicao`.

## Correspondências residuais do grep

- `docs/NOMENCLATURA.md:486` — ACEITÁVEL: negativa explícita; afirma que a
  barra não contém todos os chips canônicos por padrão.
- `docs/contratos/contrato_tela_json.md:200-201` — ACEITÁVEL: declara a
  sequência H-0011A-D como histórica/cancelada e não orientadora.
- `docs/contratos/contrato_barra_de_menus.md:111` — ACEITÁVEL: negativa
  explícita; afirma que a barra não contém todos os chips canônicos por padrão.
- `docs/contratos/contrato_barra_de_menus.md:113` — ACEITÁVEL: negativa
  explícita; afirma que o Orquestrador não precisa declarar todos os chips
  canônicos.
- `docs/contratos/contrato_json_dashboard.md:104-105` — BLOQUEANTE:
  referência operacional futura a H-0011A em contrato ativo.
- `docs/contratos/contrato_json_dashboard.md:120` — BLOQUEANTE: referência
  operacional futura a H-0011A em contrato ativo.
- `docs/contratos/contrato_json_dashboard.md:157` — BLOQUEANTE: referência
  operacional futura a H-0011A em contrato ativo.
- `docs/contratos/contrato_composicao_corpo.md:558` — ACEITÁVEL: classifica
  H-0011A-D como histórico e declara que não orienta novos ciclos.
- `docs/contratos/contrato_chip.md:204` — ACEITÁVEL: fala de regra
  `regra_existencia = sempre` para chip dentro daquela instância concreta,
  não de presença obrigatória de todos os chips canônicos em toda tela.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:42` —
  ACEITÁVEL: contexto histórico.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:55` —
  ACEITÁVEL: compatibilidade transicional sem reabrir ciclos cancelados.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:113` —
  ACEITÁVEL: título normativo que restringe H-0011A-D a histórico.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:116` —
  ACEITÁVEL: declara explicitamente que H-0011A-D não orienta novos ciclos.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:173` —
  ACEITÁVEL: preserva compatibilidade histórica sem reabrir H-0011/H-0011A.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:184` —
  ACEITÁVEL: preserva referências históricas em ADR aceita.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:60` —
  ACEITÁVEL: descreve leitura que a ADR rejeita.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:78` —
  ACEITÁVEL: negativa explícita; Orquestrador não deve declarar todos os chips
  canônicos por padrão.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:150` —
  ACEITÁVEL: consequência de alinhamento declarativo; não obriga conjunto
  global.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:151` —
  ACEITÁVEL: negativa explícita.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:170` —
  ACEITÁVEL: decisão futura fora de escopo sobre eventual contrato mínimo.
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md:192` —
  ACEITÁVEL: alternativa rejeitada; contradiz o princípio declarativo.

## Achados bloqueantes

1. `docs/contratos/contrato_json_dashboard.md` ainda possui referências
   operacionais futuras a H-0011A (`em H-0011A`, `após H-0011A`) em contrato
   ativo, sem reenquadramento como histórico/cancelado/não orientador.

## Achados não bloqueantes

- O bloqueio sobre chips canônicos sempre presentes foi resolvido nos arquivos
  auditados.
- `docs/contratos/contrato_chip.md` contém `regra_existencia = sempre`, mas a
  frase é limitada a uma instância concreta de tela e não impõe presença
  global de chips canônicos.
- As referências a H-0011A-D em ADR-0011, ADR-0012,
  `contrato_tela_json.md` e `contrato_composicao_corpo.md` estão
  adequadamente classificadas como históricas/canceladas/não orientadoras.
