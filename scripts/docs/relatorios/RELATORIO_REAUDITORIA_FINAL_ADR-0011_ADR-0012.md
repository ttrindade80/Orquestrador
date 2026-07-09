# Relatório de Reauditoria Final — ADR-0011 e ADR-0012

## Status

QA_APPROVED_WITH_NOTES

## Contexto

Reauditoria final focada após a correção do bloqueio restante apontado na
reauditoria anterior: `docs/contratos/contrato_json_dashboard.md` ainda
tratava H-0011A como marco operacional futuro.

Esta reauditoria verificou somente documentação e criou apenas este relatório.
Não foram alterados código, JSONs, testes, handoffs, contratos ou ADRs.

## Arquivos lidos

- `docs/relatorios/RELATORIO_REAUDITORIA_ADR-0011_ADR-0012.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`

## Verificações executadas

```text
$ git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
?? docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
?? docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0011_ADR-0012.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md
?? docs/relatorios/RELATORIO_REAUDITORIA_ADR-0011_ADR-0012.md
```

```text
$ git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 30 +++++++----
 scripts/docs/adr/INDICE_ADR.md                     |  2 +
 scripts/docs/contratos/contrato_barra_de_menus.md  | 40 ++++++++++-----
 .../docs/contratos/contrato_composicao_corpo.md    | 58 ++++++++++++++--------
 scripts/docs/contratos/contrato_json_dashboard.md  | 10 ++--
 .../docs/contratos/contrato_json_tela_minima.md    | 14 ++++--
 scripts/docs/contratos/contrato_tela_json.md       | 33 ++++++++----
 7 files changed, 127 insertions(+), 60 deletions(-)
```

```text
$ git diff --name-only
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_dashboard.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

Busca direcionada executada, com caminhos equivalentes ao workspace atual
(`docs/...`, pois a auditoria foi executada a partir de `scripts/`):

```bash
grep -R "H-0011A\|H-0011B\|H-0011C\|H-0011D\|H-0011A-D" -n \
  docs/contratos/contrato_json_dashboard.md \
  docs/contratos/contrato_tela_json.md \
  docs/contratos/contrato_composicao_corpo.md \
  docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md \
  docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md \
  || true
```

Resultado:

```text
docs/contratos/contrato_json_dashboard.md:158:numerado posterior. H-0011 foi cancelado e H-0011A foi removido como
docs/contratos/contrato_tela_json.md:200:A sequência histórica H-0011A–D era o plano registrado pela ADR-0010, mas foi
docs/contratos/contrato_tela_json.md:201:cancelada como roteiro ativo: H-0011 foi cancelado e H-0011A removido como
docs/contratos/contrato_composicao_corpo.md:558:  implementada. Referências históricas à sequência H-0011A–D (ADR-0010)
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:42:  históricos H-0011/H-0011A–D.
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:55:compatibilidade transicional sem reabrir ciclos cancelados (H-0011/H-0011A–D).
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:113:**7. Referências históricas a H-0011A–D podem permanecer apenas como
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:116:As menções a `lado_a_lado` e à sequência H-0011A–D em ADR-0010 e em
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:173:| `docs/contratos/contrato_composicao_corpo.md` | Usar `vertical`/`horizontal` como termos normativos finais; registrar aliases transicionais; preservar compatibilidade histórica sem reabrir H-0011/H-0011A |
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:184:| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | ADR aceita não é reescrita; suas referências históricas a `lado_a_lado`/H-0011A–D permanecem como histórico |
```

## Reavaliação do bloqueio restante

O bloqueio restante foi resolvido.

`docs/contratos/contrato_json_dashboard.md` não usa mais H-0011A como marco
operacional futuro. As referências antes bloqueantes foram substituídas por
linguagem neutra:

- "ciclo futuro de migração";
- "handoff numerado posterior";
- "handoff futuro de migração".

A única menção residual a H-0011A no contrato é uma nota explícita de
cancelamento: H-0011 foi cancelado, H-0011A foi removido como handoff ativo e
referências a essa sequência não orientam novos ciclos. Essa ocorrência é
aceitável pelo critério da reauditoria.

## Ocorrências residuais de H-0011A-D

- `docs/contratos/contrato_json_dashboard.md:158` — ACEITÁVEL —
  cancelada/não orientadora. Declara que H-0011 foi cancelado, H-0011A foi
  removido como handoff ativo e que a sequência não orienta novos ciclos.
- `docs/contratos/contrato_tela_json.md:200` — ACEITÁVEL —
  histórica/cancelada. Apresenta H-0011A-D como sequência histórica.
- `docs/contratos/contrato_tela_json.md:201` — ACEITÁVEL —
  cancelada/não orientadora. Declara que H-0011 foi cancelado e H-0011A foi
  removido como handoff ativo.
- `docs/contratos/contrato_composicao_corpo.md:558` — ACEITÁVEL —
  histórica/não orientadora. Declara que referências históricas à sequência
  H-0011A-D permanecem apenas como histórico e não orientam novos ciclos.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:42` —
  ACEITÁVEL — contexto histórico dos ciclos H-0011/H-0011A-D.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:55` —
  ACEITÁVEL — compatibilidade transicional sem reabrir ciclos cancelados.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:113` —
  ACEITÁVEL — título normativo que limita H-0011A-D a referência histórica.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:116` —
  ACEITÁVEL — declara que a sequência H-0011A-D não orienta novos ciclos.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:173` —
  ACEITÁVEL — preserva compatibilidade histórica sem reabrir H-0011/H-0011A.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:184` —
  ACEITÁVEL — preserva referências históricas em ADR aceita.

Não foram encontradas ocorrências residuais em
`docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` pela busca focada.

## Verificação de escopo

`git status --short`, `git diff --stat` e `git diff --name-only` mostram
alterações somente em documentação sob `docs/`.

Não há alterações em:

- `config/`;
- `tela/`;
- `docs/handoff/`.

As alterações rastreadas seguem o escopo documental esperado para ADR-0011 e
ADR-0012. Código, JSONs, testes e handoffs permanecem fora do diff.

## Achados bloqueantes

0.

## Achados não bloqueantes

1. Permanecem ocorrências residuais de H-0011A-D em contratos/ADR, mas todas
   estão explicitamente enquadradas como históricas, canceladas ou não
   orientadoras.

## Conclusão

A documentação pode seguir para commit documental.

Status final: QA_APPROVED_WITH_NOTES, pois há ocorrências residuais
aceitáveis de H-0011A-D que foram classificadas nesta reauditoria.
