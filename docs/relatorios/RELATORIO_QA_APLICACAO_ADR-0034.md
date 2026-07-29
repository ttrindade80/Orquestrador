---
name: REL-QA-0034-aplicacao-selecao-multipla
description: "QA da aplicação documental da ADR-0034"
metadata:
  type: relatorio_qa
  etapa_qa: QA_APLICACAO_ADR
  camada_auditada: APLICACAO_ADR
  status: ADR_APPLICATION_REJECTED
  data: 2026-07-28
rastreabilidade:
  autorizacao_qa: ADR-0034
  adr_auditada: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0034.md
  achados_tratados: []
---

# REL-QA-0034 — QA da aplicação da ADR-0034

## 1. Identificação e status

```yaml
revisao: "Aplicação documental da ADR-0034 — seleção múltipla e fluxo focal"
etapa_qa: QA_APLICACAO_ADR
camada_auditada: APLICACAO_ADR
status_literal: ADR_APPLICATION_REJECTED
status_normalizado: ADR_APPLICATION_REJECTED
proxima_categoria: correcao_documental
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: aplicação da ADR-0034
autoridades_materiais:
  - ADR-0034 e relatório factual da aplicação
  - contratos, módulos terminológicos, índice de ADRs e backlog alterados
escopo:
  - ITEM-0006 e itens bloqueados ITEM-0018 a ITEM-0021
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QAA-0034-V01
    comando_ou_metodo: gate Git e diff real dos arquivos autorizados
    evidencia_focal: "master, 721f8f1, stage vazio, somente itens esperados e git diff --check limpo"
    resultado: OK
  - id: QAA-0034-V02
    comando_ou_metodo: confronto ADR, contratos, índice, backlog e relatório
    evidencia_focal: "cobertura focal preserva seleção por IDs, protocolo provisório, tela de resultado, quatro handoffs e itens bloqueados"
    resultado: FALHA
  - id: QAA-0034-V03
    comando_ou_metodo: auditoria terminológica focal
    evidencia_focal: "lote reconciliado permanece denominação focal distinta da seleção; há regras promovidas indevidamente a termos"
    resultado: FALHA
```

## 4. Achados

```yaml
achados:
  - id: QAA-0034-01
    gravidade: MATERIAL
    arquivo: docs/backlog.md
    requisito: "NOTA-QAA-01; handoff somente após base documental aprovada neste QA"
    evidencia_focal: "ITEM-0006 está pronto_para_handoff e manda criar Handoff 1, enquanto o relatório da aplicação declara ADR_APPLICATION_COMPLETED_AWAITING_QA."
    impacto: "Autoriza iniciar handoff sobre aplicação ainda não aprovada e declara a aplicação como concluída prematuramente."
    correcao_necessaria: "Manter ITEM-0006 em estado anterior a pronto_para_handoff, com próxima ação condicionada à aprovação deste QA; promover somente após a correção e novo QA favorável."
  - id: QAA-0034-02
    gravidade: MATERIAL
    arquivo: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
    requisito: "NOTA-QAA-03; nomenclatura não deve transformar regras ou sequência operacional em termos."
    evidencia_focal: "temporário fornecido explicitamente, validação única na entrada, ausência de releitura e limpeza do temporário são listados e definidos como termos, mas reproduzem regras de execução de contrato_json_console.md §14.4."
    impacto: "Duplica norma comportamental em autoridade terminológica e torna inexato o delta terminológico do relatório da aplicação."
    correcao_necessaria: "Remover essas quatro entradas terminológicas e suas definições; conservar as regras somente no contrato e atualizar o delta do RELATORIO_APLICACAO_ADR-0034.md."
  - id: QAA-0034-03
    gravidade: MATERIAL
    arquivo: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    requisito: "NOTA-QAA-03; cada termo deve ser conceito necessário, não regra comportamental."
    evidencia_focal: "preservação literal do texto inválido é incluída como termo e definida pela proibição de correção, normalização, reserialização e reinterpretação."
    impacto: "Promove uma regra de preservação do envelope a termo canônico e o relatório registra um termo criado que não existe como conceito terminológico autônomo."
    correcao_necessaria: "Remover preservação literal do texto inválido da nomenclatura e do delta terminológico; manter a obrigação em contrato_json_console.md §14.6."
```

## 9. Conclusão

`ADR_APPLICATION_REJECTED`: há correção documental obrigatória no backlog e na nomenclatura. A ADR própria permanece inalterada; o índice e a fronteira focal de `lote reconciliado` estão conformes. Nenhum patch foi aplicado nesta auditoria.
