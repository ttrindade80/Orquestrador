---
name: RELATORIO_PATCH_ADR-0043_P01
description: "Delta factual do patch P01 da ADR-0043"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_ADR
  status: ADR_PATCHED
  data: "2026-08-08"
rastreabilidade:
  etapa: PATCH_ADR
  objeto: ADR-0043
  patch: P01
  cadeia_raiz: ADR-0043
  predecessor_imediato: QA_ADR-0043
  achados_tratados:
    - ADR-0043-A
    - ADR-0043-B
    - ADR-0043-C
    - ADR-0043-D
---

# RELATORIO_PATCH_ADR-0043_P01 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_ADR
status_literal: ADR_PATCHED
```

## 2. Cadeia

```yaml
raiz: ADR-0043
predecessor_imediato: QA_ADR-0043
achados_tratados:
  - ADR-0043-A
  - ADR-0043-B
  - ADR-0043-C
  - ADR-0043-D
achados_resolvidos:
  - ADR-0043-A
  - ADR-0043-B
  - ADR-0043-C
  - ADR-0043-D
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: ADR-0043-A
    alteracao: "D-CHIP-09 passou a exigir cursor/item corrente navegável; sem nós visíveis o console não é focalizável; reconciliação e validade prévia foram normatizadas."
  - id_achado: ADR-0043-B
    alteracao: "Exemplos de expansão/recolhimento foram descritos por efeito em prosa, sem IDs ou campos técnicos de ação."
  - id_achado: ADR-0043-C
    alteracao: "D-CHIP-03 passou a referenciar a gramática vigente para a faixa de chips específicos/contextuais, antes de Ajuda, sem segunda ordenação."
  - id_achado: ADR-0043-D
    alteracao: "Rastreabilidade atualizada para ITEM-0007 e H-0053, com a interrupção operacional aguardando aplicação e reconciliação explicitada."
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_PATCH_ADR-0043_P01.md
arquivos_alterados:
  - caminho: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
    delta: "Correções exclusivas dos achados ADR-0043-A a ADR-0043-D."
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "test -f docs/relatorios/RELATORIO_PATCH_ADR-0043_P01.md"
    resultado_compacto: "passou"
  - comando_ou_metodo: "git diff --check"
    resultado_compacto: "passou"
  - comando_ou_metodo: "git diff --cached --name-only"
    resultado_compacto: "vazio; stage vazio"
  - comando_ou_metodo: "git diff -- ADR-0043 e relatório P01"
    resultado_compacto: "sem saída; ambos permanecem não rastreados"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios:
  - "H-0053 permanece operacionalmente interrompido aguardando aplicação da ADR-0043 e reconciliação posterior; QA pós-patch é a próxima etapa."
stage: vazio
outros_arquivos_alterados_nesta_etapa: false
commit: false
```

Não foram lidos relatórios de QA nem alterados contratos, nomenclatura,
código, fixture, backlog, handoffs ou outros arquivos fora dos dois caminhos
autorizados.
