---
name: REL-QA-H-0042-handoff
description: "Auditoria independente do handoff do protocolo focal de execução sintética reversível"
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H2_HANDOFF_PATCH_REQUIRED
  data: 2026-07-29
rastreabilidade:
  autorizacao_qa: QA_HANDOFF H-0042
  adr_auditada: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  handoff_origem: docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
  contrato_alvo: docs/contratos/contrato_json_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
---

# REL-QA-H-0042 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: H-0042 — protocolo focal de execução sintética reversível
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: H2_HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_DOCUMENTAL_DO_HANDOFF
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
autoridades_materiais:
  - ADR-0034 D-SEL-12 a D-SEL-15, D-SEL-19 e D-SEL-21
  - ADR-0035 H2-ESP-01 a H2-ESP-18
  - contrato_json_console.md §14
escopo:
  - Handoff 2 isolado; sem binding real, TUI ou Handoffs 3 e 4
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QA-H0042-01
    comando_ou_metodo: gate Git, manifesto integral e recortes focais autorizados
    evidencia_focal: "master em f4b5df1; stage vazio; H-0042 identificável; artefatos futuros nominais ausentes"
    resultado: OK
  - id: QA-H0042-02
    comando_ou_metodo: confronto do protocolo, CLI, temporários, schema e testes com ADR-0034/0035 e contrato §14
    evidencia_focal: "capacidade permanece sintética, reversível e sem ativação da interface"
    resultado: FALHA
```

## 4. Achados

```yaml
- id: H0042-QA-001
  gravidade: MATERIAL
  requisito_violado: "CA-09 e §10 exigem cenário de sucesso com stderr determinístico e código 0, sem mudar a classificação; §11 exige demonstração reproduzível por entradas."
  secao_do_handoff: "§6.5.6, §9 CA-09, §10 (Canais) e §11"
  evidencia_focal: "§6.5.6 fixa stdout/stderr vazios no cenário normal. As cinco entradas nominais só definem sucesso, parcial e os três controles; nenhum ID, campo, fixture ou mecanismo interno aciona o aviso de sucesso. Os controles autorizados não o representam."
  impacto: "A implementação teria de inventar o gatilho do aviso, ou não conseguiria provar CA-09 de forma reproduzível sem ampliar a CLI ou o protocolo."
  correcao_necessaria: "Definir no próprio handoff um gatilho focal e determinístico, compatível com a CLI fechada e sem novo controle de domínio, e vinculá-lo nominalmente à fixture, demonstração e teste de CA-09."
```

## 9. Conclusão

O handoff é fiel às fronteiras normativas e a lista nominal não colide com o repositório. Contudo, a ausência do mecanismo exigido para o único cenário de sucesso com aviso impede implementar e demonstrar CA-09 sem decisão nova. Requer patch documental.
