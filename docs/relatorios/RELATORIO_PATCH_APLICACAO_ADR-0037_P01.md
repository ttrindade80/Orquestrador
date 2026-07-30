---
name: REL-PATCH-0037-P01-status-normativo-aceita
description: "Alinha metadata.status e seção 1 da ADR-0037 de proposta para aceita"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_PATCHED
  data: 2026-07-29
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ADR-0037
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0037.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0037.md
  achados_tratados:
    - QA-APLICACAO-ADR0037-001
---

# REL-PATCH-0037-P01 — Patch de status normativo da ADR-0037

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_APLICACAO_ADR
status_literal: ADR_APPLICATION_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0037.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0037.md
achados_tratados:
  - QA-APLICACAO-ADR0037-001
achados_resolvidos:
  - QA-APLICACAO-ADR0037-001
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-APLICACAO-ADR0037-001
    alteracao: metadata.status e secao_1_status de proposta para aceita
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0037_P01.md
arquivos_alterados:
  - caminho: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
    delta:
      - metadata.status: proposta -> aceita
      - secao_1_status: proposta -> aceita
arquivos_removidos: []
```

Nenhuma decisão material (D-H4-01 a D-H4-10) foi modificada. Índice e backlog não foram alterados porque já estavam coerentes. Contratos, nomenclatura e estilo não foram alterados. O relatório original de aplicação e os relatórios de QA permanecem históricos e intactos. Validação manual não se aplica.

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: leitura focal metadata.status e secao_1_status
    resultado_compacto: ambos aceita; 10 decisoes D-H4 preservadas
  - comando_ou_metodo: git diff --check
    resultado_compacto: sem erros de espaco
  - comando_ou_metodo: git diff focal ADR-0037 e este relatorio
    resultado_compacto: somente as duas trocas de status na ADR
  - comando_ou_metodo: git diff --cached --name-only; git status --short
    resultado_compacto: stage vazio; worktree coerente com o patch
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0037.md
    finalidade: predecessor que transportou QA-APLICACAO-ADR0037-001
    leitura_necessaria_para: []
```
