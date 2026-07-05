---
name: RFC-NNNN-descricao
description: "[preencher] Mudanca proposta em uma linha"
metadata:
  type: rfc
  status: pendente
  id: RFC-NNNN
  aberta_por: "[papel ou pessoa]"
  data_abertura: YYYY-MM-DD
rastreabilidade:
  contratos_afetados: []
  issues_relacionadas: []
  bugs_relacionados: []
  handoffs_bloqueados: []
---

# RFC-NNNN — [Titulo curto]

## Problema

[Descrever a lacuna ou contradicao que nao pode ser resolvida localmente.]

## Por que exige decisao

[Explicar por que implementar diretamente seria arriscado ou violaria contrato.]

## Proposta

[Descrever a mudanca sugerida.]

## Impacto documental

| Artefato | Mudanca necessaria |
|---|---|
| `docs/contratos/contrato_modulo_exemplo.md` | [Regra a alterar ou criar] |

## Criterio de aceitacao da RFC

- [ ] Decisao aprovada ou rejeitada
- [ ] ADR criada se necessario
- [ ] Contratos afetados atualizados
- [ ] Handoffs bloqueados revisados

## Exemplo

```text
RFC: permitir novo estado intermediario no modulo exemplo.
Motivo: o contrato atual nao cobre validacao pendente.
```
