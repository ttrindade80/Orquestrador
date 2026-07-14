---
name: BUG-NNNN-descricao
description: "[preencher] Sintoma principal do bug"
metadata:
  type: bug
  status: OPEN
  classificacao: local
  severidade: media
  data_abertura: YYYY-MM-DD
rastreabilidade:
  handoff_origem: null
  relatorio_impl: null
  relatorio_qa: null
  contrato_alvo: null
  issues_relacionadas: []
---

# BUG-NNNN — [Descricao curta]

## Classificacao

- `local`: corrigivel sem mudar contrato.
- `arquitetural`: exige RFC, ADR ou mudanca de contrato.

## Sintoma

[O que acontece que nao deveria acontecer.]

## Esperado

[O que o contrato ou handoff exige.]

## Evidencia

```text
Comando/verificacao: [exemplo]
Resultado observado: [exemplo]
Resultado esperado: [exemplo]
```

## Escopo permitido para correcao

- [Arquivos permitidos]

## Criterio de fechamento

- [ ] Causa identificada
- [ ] Correcao local ou RFC registrada
- [ ] QA atualizado com evidencia
