---
name: H-NNNN-descricao
description: "[preencher] Objetivo verificavel da implementacao"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-NNNN
  data_criacao: YYYY-MM-DD
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_modulo_exemplo.md"
  adr_relacionadas: []
  issues_relacionadas: []
  handoffs_anteriores: []
---

# H-NNNN — [Verbo + objeto + modulo]

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. ADRs relacionadas
3. Contrato alvo
4. Este handoff

Se houver conflito, bloquear e registrar a divergencia.

## Escopo

**Objetivo:** [descrever resultado esperado em uma frase]

**Arquivos permitidos:**

- `tela/modulo_exemplo/arquivo_exemplo.py`

**Arquivos proibidos:**

- `docs/contratos/`
- `tela/outro_modulo/`

## Tarefas

1. [Tarefa pequena e objetiva]
2. [Tarefa pequena e objetiva]
3. [Atualizar somente arquivos permitidos]

## Criterios de aceite

| Criterio | Evidencia esperada |
|---|---|
| [Comportamento contratado X ocorre] | [Teste, diff ou verificacao manual] |
| [Comportamento proibido Y nao ocorre] | [Teste, diff ou verificacao manual] |

## Saida esperada

Produzir relatorio `IMP-NNNN-descricao.md` usando
`docs/templates/TEMPLATE_RELATORIO_IMPL.md`.
