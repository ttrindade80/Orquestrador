---
name: indice-scripts
description: Indice da documentacao padrao para desenvolvimento de scripts
metadata:
  type: indice
  scope: scripts
---

# Indice — Documentacao de Scripts

## Proposito

Esta pasta guarda apenas regras documentais, templates e exemplos neutros para
conduzir desenvolvimento por especificacao. Ela nao deve conter codigo,
relatorios historicos, contratos de modulo ja decididos, nem referencia a
tentativas anteriores.

## Regra de limpeza

Antes de mover este padrao para outro projeto, verificar:

- nenhum arquivo de cache ou bytecode esta presente;
- nenhum documento afirma decisao concreta que ainda nao foi aprovada;
- exemplos usam nomes genericos como `modulo_exemplo`;
- contratos de modulo aparecem como exemplos ou pendencias, nunca como vigentes.

## Ordem de leitura

1. `docs/INDICE.md`
2. `docs/contratos/contrato_processo_desenvolvimento.md`
3. `docs/handoff/README.md`
4. `docs/relatorios/README.md`
5. Templates em `docs/templates/`, conforme a tarefa.

## Estrutura esperada

```text
docs/
  INDICE.md
  backlog.md
  issues.md
  contratos/
    contrato_processo_desenvolvimento.md
  adr/
    INDICE_ADR.md
  handoff/
    README.md
  relatorios/
    README.md
  templates/
    TEMPLATE_ADR.md
    TEMPLATE_BUG.md
    TEMPLATE_HANDOFF_IMPLEMENTACAO.md
    TEMPLATE_HANDOFF_QA.md
    TEMPLATE_RELATORIO_IMPL.md
    TEMPLATE_RELATORIO_QA.md
    TEMPLATE_RFC.md
```

## Artefatos

| Artefato | Funcao | Regra |
|---|---|---|
| Contrato | Define comportamento esperado | Deve ser aprovado antes da implementacao |
| ADR | Registra decisao arquitetural | Nao substitui contrato; contratos afetados devem ser atualizados |
| RFC | Propoe mudanca | Nao autoriza implementacao |
| Handoff | Ordem fechada de trabalho | Deve citar contrato e criterios de aceite |
| Relatorio | Evidencia do que foi feito | Nao cria regra nova |
| Bug | Registra falha observada | Deve classificar se e local ou arquitetural |

## Exemplo de referencia neutra

```text
Contrato alvo: docs/contratos/contrato_modulo_exemplo.md
Modulo alvo: scripts/modulo_exemplo/
Handoff: H-0001-criar-interface-minima.md
Relatorio: IMP-0001-criar-interface-minima.md
QA: REL-QA-0001-criar-interface-minima.md
```
