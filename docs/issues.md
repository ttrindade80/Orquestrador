---
name: issues-orquestrador
description: Modelo neutro para registrar impedimentos e bugs
metadata:
  type: issues
  scope: orquestrador
---

# Issues — Modelo

## Regra

Issues registram impedimentos ativos, bugs e decisoes pendentes. Elas nao
alteram contrato e nao autorizam implementacao fora de handoff.

## Estados

| Estado | Significado |
|---|---|
| OPEN | Registrada e ainda sem solucao |
| IN_REVIEW | Aguardando decisao documental |
| FIX_READY | Pode gerar handoff de correcao |
| CLOSED | Fechada com evidencia objetiva |

## Formato

```markdown
### ISSUE-NNNN — [Titulo curto]
**Tipo:** bug | impedimento | decisao_pendente | mudanca_contratual
**Severidade:** critica | alta | media | baixa
**Status:** OPEN
**Modulo:** [modulo afetado ou "processo"]
**Descricao:** [O que esta bloqueando ou quebrando]
**Evidencia:** [Arquivo, comando, relato ou criterio violado]
**Proxima acao:** [Decisao, ADR, contrato ou handoff necessario]
**Aberta em:** YYYY-MM-DD
**Artefatos relacionados:** [RFC-NNNN, ADR-NNNN, contrato_X.md, H-NNNN]
**Criterio de fechamento:** [Evidencia objetiva]
```

## Exemplo

```markdown
### ISSUE-0000 — Contrato do modulo exemplo ainda nao existe
**Tipo:** impedimento
**Severidade:** alta
**Status:** OPEN
**Modulo:** modulo_exemplo
**Descricao:** Nao ha contrato aprovado para orientar implementacao.
**Evidencia:** `docs/contratos/contrato_modulo_exemplo.md` ausente.
**Proxima acao:** Criar contrato antes de qualquer handoff.
**Aberta em:** YYYY-MM-DD
**Artefatos relacionados:** ITEM-0000
**Criterio de fechamento:** Contrato aprovado e referenciado no indice.
```
