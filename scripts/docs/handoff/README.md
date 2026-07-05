---
name: handoff-readme
description: Regras neutras para criacao e ciclo de vida de handoffs
metadata:
  type: referencia
  scope: scripts
---

# Handoffs — Regras

## Definicao

Um handoff e uma ordem de trabalho fechada, verificavel e limitada por contrato.
Ele deve permitir que o executor saiba exatamente:

- o que fazer;
- quais arquivos pode tocar;
- quais arquivos nao pode tocar;
- quais contratos governam a tarefa;
- quais criterios provam que a tarefa terminou.

## Proibicoes

Um handoff nao pode:

- criar regra nova que contradiga contrato;
- autorizar implementacao sem contrato aplicavel;
- pedir refatoracao aberta;
- misturar implementacao, QA e decisao arquitetural no mesmo artefato;
- depender de conversa externa para completar escopo.

## Tipos

| Prefixo | Destinatario | Template |
|---|---|---|
| `H-NNNN` | Implementacao | `TEMPLATE_HANDOFF_IMPLEMENTACAO.md` |
| `QA-NNNN` | Revisao/QA | `TEMPLATE_HANDOFF_QA.md` |
| `BUG-NNNN` | Correcao ou registro de bug | `TEMPLATE_BUG.md` |

## Estados

| Estado | Uso |
|---|---|
| DRAFT | Ainda incompleto |
| READY_FOR_IMPLEMENTATION | Pronto para executor de implementacao |
| IMPLEMENTED | Implementacao reportada |
| READY_FOR_QA | Pronto para revisao |
| QA_APPROVED | Aprovado |
| QA_FAILED | Reprovado por falha local |
| ARCHITECTURE_REVIEW_REQUIRED | Bloqueado por lacuna contratual |

## Exemplo minimo

```text
Handoff: H-0001-criar-comando-exemplo.md
Contrato: docs/contratos/contrato_modulo_exemplo.md
Escopo permitido: scripts/modulo_exemplo/comandos.py
Escopo proibido: docs/contratos/, scripts/outro_modulo/
Criterio de aceite: comando retorna saida documentada para entrada valida.
```
