---
name: RELATORIO-QA-H-0041-HANDOFF
description: "QA independente do Handoff 1 do ITEM-0006"
metadata:
  type: handoff_qa
  status: CONCLUIDO
  id: QA-H-0041
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  data_criacao: 2026-07-28
rastreabilidade:
  adr_alvo: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  relatorio_aplicacao: null
  handoff_origem: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  relatorio_impl: null
  relatorio_qa_anterior: null
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  issues_relacionadas:
    - ITEM-0006
---

# QA-H-0041 — Revisar Handoff 1 da seleção múltipla

## 1. Etapa única

`QA_HANDOFF`

## 2. Papel

Auditoria documental independente. Nenhuma correção ou implementação foi feita.

## 3. Manifesto fechado de leitura

Foram lidos integralmente o template aplicável, H-0041, ADR-0034, backlog, os
contratos de console e barra, e os módulos 31 e 32. A inspeção técnica ficou
restrita aos caminhos nominais autorizados pelo H-0041. Gate Git conforme:
`master`, `721f8f1`, stage vazio, handoff presente e relatório ausente.

## 4. Autoridades e objeto auditado

H-0041 foi confrontado com ADR-0034 e suas autoridades aplicadas. A capacidade
pretendida permanece Handoff 1, sem autorizar operação externa; os achados abaixo
impedem sua aprovação documental.

## 5. Escopo da revisão

Foram verificados fidelidade, lista nominal, testes, demonstração, roteiro TTY,
relatório futuro e coerência factual com o backlog.

## 6. Achados

```yaml
- id: H0041-QA-001
  gravidade: MATERIAL
  secao_do_handoff: "3. Estado comprovado"
  requisito: "Estado factual fiel às autoridades aplicadas."
  evidencia_focal: "Afirma que docs/backlog.md registra a mesma condição de criação; o ITEM-0006 ainda manda concluir patch documental e QA pós-patch antes do Handoff 1."
  impacto: "O handoff transporta um estado documental incompatível com a autoridade lida."
  correcao_necessaria: "Atualizar a declaração para o estado efetivamente autorizado ou sanar a contradição documental antes da aprovação."

- id: H0041-QA-002
  gravidade: MATERIAL
  secao_do_handoff: "6.1 e 10"
  requisito: "Listas nominais separadas para existentes, novos, fixture, demonstração, testes unitários, integração e relatório."
  evidencia_focal: "A seção 6.1 mistura arquivos existentes e novos em uma única lista; a seção 10 agrupa testes por categoria sem uma lista nominal separada de integração."
  impacto: "A implementação precisa reconstruir a classificação do escopo, contrariando o handoff fechado."
  correcao_necessaria: "Separar explicitamente as listas exigidas, mantendo cada caminho nominal e sua finalidade."

- id: H0041-QA-003
  gravidade: MATERIAL
  secao_do_handoff: "10. Testes obrigatórios"
  requisito: "Comandos reproduzíveis devem incluir testes focais e a suíte canônica."
  evidencia_focal: "Há somente o comando da suíte completa: PYTHONDONTWRITEBYTECODE=1 python -m pytest."
  impacto: "Não existe comando focal para validar de modo direto os testes unitários e de integração previstos."
  correcao_necessaria: "Declarar comandos focais reais, além da suíte canônica."

- id: H0041-QA-004
  gravidade: MATERIAL
  secao_do_handoff: "11. Roteiro sequencial de validação TTY"
  requisito: "Roteiro fechado, sequencial e executável, com tecla acionada em cada passo."
  evidencia_focal: "O passo 3 permite 'seta_direita ou seta_baixo' e o passo 5 usa 'navegação até item_03 + Espaço', sem sequência determinística de teclas."
  impacto: "O usuário não consegue reproduzir um único percurso TTY verificável."
  correcao_necessaria: "Fixar a tecla ou sequência exata para cada transição."

- id: H0041-QA-005
  gravidade: MATERIAL
  secao_do_handoff: "12. Relatório da execução"
  requisito: "Relatório futuro com teto normal de 900 palavras."
  evidencia_focal: "O H-0041 estabelece teto normal de 600 palavras, elevável a 900 somente excepcionalmente."
  impacto: "A instrução do relatório futuro diverge da convenção canônica exigida para este handoff."
  correcao_necessaria: "Ajustar o teto normal para 900 palavras."
```

## 7. Taxonomia obrigatória

`status_literal: H2_HANDOFF_PATCH_REQUIRED`

## 8. Relatório de QA

Este é o relatório solicitado. Não foram produzidos artefatos de implementação.

## 9. Resposta terminal

```yaml
status: H2_HANDOFF_PATCH_REQUIRED
relatorio: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF.md
```

## 10. Limite de encerramento

Encerrado após o relatório.
