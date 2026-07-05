---
name: relatorios-readme
description: Regras neutras para relatorios de implementacao e QA
metadata:
  type: referencia
  scope: scripts
---

# Relatorios — Regras

## Definicao

Relatorio e evidencia. Ele descreve o que foi feito, o que foi verificado e o
que ficou bloqueado. Relatorio nao altera contrato, nao aprova ADR e nao cria
escopo novo.

## Tipos

| Prefixo | Funcao | Template |
|---|---|---|
| `IMP-NNNN` | Evidencia de implementacao | `TEMPLATE_RELATORIO_IMPL.md` |
| `REL-QA-NNNN` | Evidencia de revisao/QA | `TEMPLATE_RELATORIO_QA.md` |
| `REL-DOC-NNNN` | Evidencia de auditoria documental | `TEMPLATE_RELATORIO_QA.md` adaptado |

## Regras obrigatorias

- Todo criterio de aceite do handoff deve ter uma linha de evidencia.
- Toda regra contratual relevante deve ser marcada como OK, FALHA ou NAO VERIFICADA.
- Falha contratual reprova o trabalho mesmo que testes passem.
- Lacuna de contrato deve virar RFC ou issue, nao decisao local.
- Comandos podem ser citados como exemplos de validacao, mas o relatorio deve
  deixar claro quem executou e qual foi a saida observada.

## Exemplo de evidencia

```markdown
| Criterio | Evidencia | Resultado |
|---|---|---|
| Entrada invalida gera erro documentado | Teste `test_entrada_invalida` passou | OK |
| Nao altera arquivo de estado fora do escopo | Diff revisado sem alteracao em `estado.json` | OK |
```
