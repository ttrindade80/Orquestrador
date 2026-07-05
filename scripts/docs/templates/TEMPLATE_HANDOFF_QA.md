---
name: QA-NNNN-descricao
description: "[preencher] Objetivo verificavel da revisao"
metadata:
  type: handoff_qa
  status: READY_FOR_QA
  id: QA-NNNN
  handoff_origem: H-NNNN
  relatorio_impl: IMP-NNNN
  data_criacao: YYYY-MM-DD
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_modulo_exemplo.md"
  adr_relacionadas: []
  issues_relacionadas: []
---

# QA-NNNN — Revisar [handoff/modulo]

## Ordem de autoridade

1. Contrato de processo
2. ADRs relacionadas
3. Contrato alvo
4. Handoff de origem
5. Relatorio de implementacao

Se testes passam mas contrato e violado, reprovar.

## Escopo da revisao

- Verificar cada criterio de aceite do handoff.
- Verificar aderencia ao contrato alvo.
- Verificar se arquivos proibidos nao foram alterados.
- Classificar falhas como locais ou arquiteturais.

## Criterios de QA

| Item | Resultado esperado |
|---|---|
| Criterios do handoff | Todos com evidencia suficiente |
| Contrato alvo | Nenhuma violacao |
| Escopo de arquivos | Nenhuma alteracao proibida |
| Lacunas | Registradas como issue ou RFC |

## Saida esperada

Produzir relatorio `REL-QA-NNNN-descricao.md` usando
`docs/templates/TEMPLATE_RELATORIO_QA.md`.
