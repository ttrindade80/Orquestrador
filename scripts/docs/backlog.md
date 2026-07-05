---
name: backlog-scripts
description: Modelo neutro para registrar trabalho planejado
metadata:
  type: backlog
  scope: scripts
---

# Backlog — Modelo

## Regra

Este arquivo deve conter somente itens planejados ainda nao iniciados. Ele nao
e contrato, nao e autorizacao de implementacao e nao substitui handoff.

Ao copiar este padrao para um projeto novo, manter apenas exemplos ou limpar
esta lista.

## Formato

```markdown
### ITEM-NNNN — [Titulo curto]
**Tipo:** contrato | implementacao | qa | documentacao | infraestrutura
**Prioridade:** alta | media | baixa
**Status:** planejado | bloqueado | pronto_para_handoff
**Descricao:** [O que precisa existir]
**Pre-requisitos:** [Contratos, ADRs ou decisoes necessarias]
**Proxima acao:** [A menor acao documental verificavel]
```

## Exemplos

### ITEM-0000 — Criar contrato do modulo exemplo
**Tipo:** contrato
**Prioridade:** media
**Status:** planejado
**Descricao:** Especificar entradas, saidas, estados e erros do `modulo_exemplo`.
**Pre-requisitos:** Nenhum.
**Proxima acao:** Escrever `docs/contratos/contrato_modulo_exemplo.md` a partir do template acordado.

### ITEM-0001 — Preparar handoff de implementacao exemplo
**Tipo:** implementacao
**Prioridade:** baixa
**Status:** bloqueado
**Descricao:** Gerar handoff para implementar comportamento ja contratado.
**Pre-requisitos:** Contrato do modulo aprovado.
**Proxima acao:** Criar `H-0001-descricao-curta.md`.
