---
name: REL-QA-ADR-0036
description: "Auditoria documental independente da ADR-0036"
metadata:
  type: relatorio_qa
  etapa_qa: QA_ADR
  camada_auditada: ADR
  status: ADR_REJECTED
  data: 2026-07-29
rastreabilidade:
  autorizacao_qa: "QA_ADR — decisões D-H3-01 a D-H3-18"
  adr_auditada: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  issues_relacionadas:
    - ITEM-0006
---

# REL-QA-ADR-0036 — Auditoria da ADR-0036

## 1. Identificação e status

```yaml
objeto_auditado: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
etapa_qa: QA_ADR
status_literal: ADR_REJECTED
status_normalizado: ADR_REJECTED
proxima_categoria: PATCH_ADR
```

## 2. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-ADR0036-001 | material | D-H3-11 e D-H3-15; ordem fixa do envelope | §3, D-H3-11 fixa apenas `status: falha`; §4 menciona “campos fixos”, sem declarar `tipo: multinivel`, `apresentacao: conjuntos_campos` e a sequência dos seis campos. | A implementação futura não tem, nesta ADR, a ordem normativa verificável de `status`, `diagnostico`, `codigo_saida`, `stdout`, `stderr`, `resultado_json`. | Declarar normativamente a estrutura e a ordem fixa integral do envelope. |
| QA-ADR0036-002 | material | Compatibilidade afirmada com ADR-0034 D-SEL-21 e `contrato_json_console.md` §14.11 | §§2, 4, 8 e 10 deixam abertura, retorno, suspensão e restauração para o Handoff 4, embora D-SEL-21 e §14.11 os atribuam ao Handoff 3. A ADR se apresenta como especialização que não substitui a ADR-0034. | Há contradição documental sobre a fronteira dos handoffs e sobre o alcance da especialização. | Formalizar expressamente o ajuste/supersessão da divisão de D-SEL-21 determinada para esta ADR, ou adequar a fronteira declarada à autoridade preservada. |

## 3. Arquivos verificados e checks

```yaml
arquivos_verificados:
  - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  - docs/templates/TEMPLATE_RELATORIO_QA.md
  - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  - docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
checks:
  - decisao_D_H3_01_a_18: FALHA
  - escopo_e_deferimentos: OK
  - preservacao_literal_resultado_json: OK
  - ausencia_de_cor_alerta_paginacao_truncamento_modo_alternavel: OK
  - compatibilidade_ADR_0034_ADR_0035_H_0042: FALHA
  - estado_git_previo: "ADR-0036 não rastreada; conforme estado transportado"
bloqueios: nenhum
```

## 4. Conclusão

`ADR_REJECTED`: os dois achados materiais exigem `PATCH_ADR`. Não há bloqueio de decisão do usuário nem insuficiência documental.
