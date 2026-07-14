---
name: REL-QA-NNNN-descricao
description: "[preencher] Resultado da revisao"
metadata:
  type: relatorio_qa
  status: QA_APPROVED
  handoff_qa: QA-NNNN
  handoff_origem: H-NNNN
  relatorio_impl: IMP-NNNN
  data: YYYY-MM-DD
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_modulo_exemplo.md"
  adr_relacionadas: []
  bugs_abertos: []
---

# REL-QA-NNNN — Relatorio de QA

## Revisao executada

`QA-NNNN — [titulo]`

## Status final

`QA_APPROVED` | `QA_FAILED` | `ARCHITECTURE_REVIEW_REQUIRED`

## Evidencia por criterio de aceite

| Criterio do handoff | Evidencia verificada | Resultado |
|---|---|---|
| [criterio] | [evidencia] | OK/FALHA |

## Verificacao contratual

| Regra contratual | Evidencia | Resultado |
|---|---|---|
| [contrato §N] | [evidencia] | OK/FALHA/NAO VERIFICADO |

## Verificacao de escopo

| Item | Resultado |
|---|---|
| Apenas arquivos permitidos alterados | OK/FALHA |
| Arquivos proibidos preservados | OK/FALHA |
| Relatorio de implementacao completo | OK/FALHA |

## Falhas encontradas

| Falha | Classificacao | Acao recomendada |
|---|---|---|
| [descricao] | local/arquitetural | [bug/RFC/novo handoff] |

## Conclusao

[Explicar em poucas linhas por que o status final foi atribuido.]
