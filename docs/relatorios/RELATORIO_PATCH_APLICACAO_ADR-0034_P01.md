---
name: REL-PATCH-0034-P01-aplicacao-selecao-multipla
description: "Patch documental da aplicação da ADR-0034: reversão do estado prematuro do ITEM-0006 e remoção de pseudo-termos nos módulos 42 e 43"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ADR-0034
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0034.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034.md
  achados_tratados:
    - QAA-0034-01
    - QAA-0034-02
    - QAA-0034-03
---

# REL-PATCH-0034-P01 — Patch da aplicação da ADR-0034

Template usado: `docs/templates/TEMPLATE_RELATORIO_PATCH.md`.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_APLICACAO_ADR
status_literal: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0034.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034.md
achados_tratados: [QAA-0034-01, QAA-0034-02, QAA-0034-03]
achados_resolvidos: [QAA-0034-01, QAA-0034-02, QAA-0034-03]
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QAA-0034-01
    alteracao: "ITEM-0006 revertido de pronto_para_handoff para em_andamento; pré-requisitos e próxima ação passam a condicionar a criação do Handoff 1 à aprovação do QA pós-patch."
  - id_achado: QAA-0034-02
    alteracao: "Removidas as quatro entradas terminológicas (temporário fornecido explicitamente, validação única na entrada, ausência de releitura, limpeza do temporário) e sua tabela de definições; §4.5 e a distinção correspondente passam a referenciar contrato_json_console.md §14.4 de forma descritiva."
  - id_achado: QAA-0034-03
    alteracao: "Removida a entrada e a definição de preservação literal do texto inválido; §7 passa a referenciar a obrigação como regra fixada em contrato_json_console.md §14.6, sem tratá-la como termo."
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/backlog.md
    delta: "ITEM-0006: Status em_andamento; pré-requisitos e próxima ação revisados."
  - caminho: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    delta: "Removido termo preservação literal do texto inválido (lista §3, definição §4.5); §7 com referência descritiva ao contrato."
  - caminho: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
    delta: "Removidos quatro termos ADR-0034 (lista §3, definições §4.5); §4.5, distinção em §5 e §6/§7 reescritos de forma descritiva."
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git diff --check"
    resultado_compacto: "limpo"
  - comando_ou_metodo: "grep dos quatro pseudo-termos removidos e de preservação literal do texto inválido nos módulos 42 e 43"
    resultado_compacto: "somente uma ocorrência remanescente, referência descritiva permitida em §7 do módulo 42"
  - comando_ou_metodo: "git status --short --untracked-files=all"
    resultado_compacto: "stage vazio; worktree contém somente os 18 artefatos já esperados da ADR-0034"
  - comando_ou_metodo: "conferência visual de contrato_json_console.md"
    resultado_compacto: "não alterado neste patch"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```

## Termos preservados e conceitos não tocados

`documento de resultado de execução`, `envelope de erro multinível` e `lote reconciliado` permanecem sem alteração. `ITEM-0018` a `ITEM-0021` não foram tocados. Nenhum contrato, ADR ou índice de ADRs foi alterado.
