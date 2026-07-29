---
name: REL-QA-POS-PATCH-ADR-0036-P01
description: "Reteste independente do patch P01 da ADR-0036"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: ADR
  status: ADR_APPROVED
  data: 2026-07-29
rastreabilidade:
  autorizacao_qa: "QA_POS_PATCH — P01"
  adr_auditada: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_ADR-0036.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_ADR-0036.md
  predecessor_imediato: P01
  achados_tratados:
    - QA-ADR0036-001
    - QA-ADR0036-002
---

# REL-QA-POS-PATCH-ADR-0036-P01 — Reteste do patch P01

## 1. Identificação e status

```yaml
etapa_qa: QA_POS_PATCH
camada_auditada: ADR
status_normalizado: ADR_APPROVED
proxima_categoria: nenhuma
```

## 2. Escopo focal

Reteste direto da ADR atual para os achados raiz e regressões materiais do P01; consulta focal de ADR-0034 D-SEL-21 e `contrato_json_console.md` §14.11.

## 3. Resultado dos achados anteriores

```yaml
QA-ADR0036-001:
  resultado: RESOLVIDO
  evidencia_focal: "D-H3-15a materializa envelope multinível, conjuntos_campos e os seis campos obrigatórios em ordem normativa; fixa falha, indisponível, preservação literal e ausência de estilo especial."
QA-ADR0036-002:
  resultado: RESOLVIDO
  evidencia_focal: "D-H3-19 identifica as duas autoridades, limita a supersessão à divisão H3/H4, lista responsabilidades, preserva ADR-0034 e delega a propagação futura à APLICAR_ADR."
```

## 4. Delta de QA pós-patch

```yaml
raiz: docs/relatorios/RELATORIO_QA_ADR-0036.md
predecessor_imediato: P01
achados_resolvidos: [QA-ADR0036-001, QA-ADR0036-002]
achados_pendentes: []
novos_achados: []
```

Regressões novas: nenhuma. A leitura focal preserva identidade, console único, cabeçalho, arranjo vertical, associação runtime, modo, limites visuais, cenários/evidências, H-0042 e os fora de escopo requeridos.

## 5. Estado e integridade

```yaml
hashes_antes:
  adr: 27a5474e4c0c97bd80ae2d81e3939ff225535b94f6ad942c821206471f07d9b3
  relatorio_raiz: 4eb2269777f8d428dc6b74c82a9f046fac17bd844a6cb424755a07bfa33e56ae
hashes_depois:
  adr: 27a5474e4c0c97bd80ae2d81e3939ff225535b94f6ad942c821206471f07d9b3
  relatorio_raiz: 4eb2269777f8d428dc6b74c82a9f046fac17bd844a6cb424755a07bfa33e56ae
stage: vazio
```

ADR e relatório raiz já estavam não rastreados antes do reteste; nesta etapa foi criado somente este relatório.

## 6. Conclusão

`ADR_APPROVED`: ambos os achados materiais foram resolvidos e não foi detectada regressão material provocada pelo P01.
