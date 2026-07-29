---
name: REL-QA-0034-P01-aplicacao-selecao-multipla
description: "QA pós-patch P01 da aplicação documental da ADR-0034"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: APLICACAO_ADR
  patch_auditado: P01
  status: ADR_APPLICATION_REJECTED
  data: 2026-07-28
rastreabilidade:
  autorizacao_qa: ADR-0034
  adr_auditada: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  predecessor_qa: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034.md
  patch_auditado: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0034_P01.md
  achados_retestados:
    - QAA-0034-01
    - QAA-0034-02
    - QAA-0034-03
---

# REL-QA-0034-P01 — QA pós-patch da aplicação da ADR-0034

## 1. Identificação e status

```yaml
revisao: "Aplicação documental da ADR-0034 — reteste do patch P01"
etapa_qa: QA_POS_PATCH
camada_auditada: APLICACAO_ADR
patch_auditado: P01
status_literal: ADR_APPLICATION_REJECTED
status_normalizado: ADR_APPLICATION_REJECTED
proxima_categoria: correcao_documental
```

## 2. Escopo e método de continuação

Este QA continua o resultado de `RELATORIO_QA_APLICACAO_ADR-0034.md`; não
reinicia a auditoria da ADR. Foram retestados os achados tratados pelo P01 e
mantidas as verificações anteriores que o patch não alcançou.

Leitura adicional autorizada, limitada às seções materiais de
`contrato_json_console.md`:

```yaml
secoes_lidas:
  - "§14.4 — Canais do processo e arquivo de resultado"
  - "§14.6 — Envelope de erro multinível"
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QAA-0034-V01
    comando_ou_metodo: "git diff --check; conferência de stage e do conjunto de artefatos"
    evidencia_focal: "diff --check limpo; stage vazio; alterações e artefatos não rastreados permanecem na cadeia documental esperada da ADR-0034."
    resultado: OK
  - id: QAA-0034-V02
    comando_ou_metodo: "reteste do backlog e confronto com o relatório P01"
    evidencia_focal: "ITEM-0006 está em_andamento e sua próxima ação condiciona o Handoff 1 à aprovação deste QA pós-patch."
    resultado: OK
  - id: QAA-0034-V03
    comando_ou_metodo: "busca focal e confronto entre módulos 42/43, §§14.4/14.6 e relatório factual da aplicação"
    evidencia_focal: "os pseudo-termos foram removidos dos módulos, mas o delta_nomenclatura e o delta_terminologico do RELATORIO_APLICACAO_ADR-0034.md ainda os declaram como termos criados."
    resultado: FALHA
```

## 4. Reteste dos achados

```yaml
reteste:
  - id: QAA-0034-01
    resultado: RESOLVIDO
    evidencia: "docs/backlog.md mantém ITEM-0006 em_andamento e proíbe criar o Handoff 1 antes da aprovação do QA pós-patch."
  - id: QAA-0034-02
    resultado: PARCIALMENTE_RESOLVIDO
    evidencia: "As quatro entradas foram removidas do módulo 43; §§14.4 confirma validação única na entrada, modelo em memória, ausência de releitura em redesenho/SIGWINCH e limpeza do temporário. O módulo 43 remete descritivamente à autoridade comportamental."
    pendencia: "RELATORIO_APLICACAO_ADR-0034.md ainda registra temporário fornecido explicitamente, validação única na entrada, ausência de releitura e limpeza do temporário como termos criados."
  - id: QAA-0034-03
    resultado: PARCIALMENTE_RESOLVIDO
    evidencia: "A entrada foi removida do módulo 42; §14.6 preserva literalmente o texto inválido e proíbe correção, normalização, reserialização, inferência e reinterpretação. O módulo 42 remete descritivamente à autoridade comportamental."
    pendencia: "RELATORIO_APLICACAO_ADR-0034.md ainda registra preservação literal do texto inválido como termo criado."
```

## 5. Achado remanescente

```yaml
achados:
  - id: QAA-0034-04
    gravidade: MATERIAL
    arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0034.md
    requisito: "Correção necessária dos achados QAA-0034-02 e QAA-0034-03: atualizar o delta terminológico do relatório factual."
    evidencia_focal: "As linhas do delta_nomenclatura e do delta_terminologico ainda incluem os quatro pseudo-termos de §14.4 e preservação literal do texto inválido; P01 declara que esses deltas foram atualizados, mas o arquivo não foi alterado."
    impacto: "O registro factual permanece inexato e contradiz a remoção efetiva das entradas terminológicas, impedindo encerrar os achados originais."
    correcao_necessaria: "Remover do RELATORIO_APLICACAO_ADR-0034.md, em delta_nomenclatura e delta_terminologico, os cinco itens que deixaram de ser termos. Preservar a referência às obrigações comportamentais no contrato."
```

## 6. Conclusão

`ADR_APPLICATION_REJECTED`: P01 resolve `QAA-0034-01` e a remoção material
dos pseudo-termos, mas não atualiza o relatório factual como exigido para
`QAA-0034-02` e `QAA-0034-03`. A correção documental de
`QAA-0034-04` e novo QA pós-patch são obrigatórios antes de promover o
ITEM-0006 para handoff.
