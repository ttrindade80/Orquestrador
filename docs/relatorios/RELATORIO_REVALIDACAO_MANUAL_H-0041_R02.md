---
name: REL-REVALIDACAO-MANUAL-H0041-R02
description: "Segunda validação manual TTY do H-0041"
metadata:
  type: relatorio_validacao_manual
  etapa: REVALIDACAO_MANUAL
  rodada: 2
  status: MANUAL_VALIDATION_FAILED
  data: 2026-07-28
rastreabilidade:
  handoff: H-0041
  validacao_anterior: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0041.md
  qa_anterior: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P03.md
  executor: USUARIO
  ambiente: terminal_TTY_real
---

# Revalidação manual TTY — H-0041 — Rodada 2

## 1. Resultado

```yaml
status_literal: MANUAL_VALIDATION_FAILED
resultado_geral: REPROVADO
executor: USUARIO
ambiente: terminal_TTY_real
```

## 2. Passos

```yaml
passos:
  1_estado_inicial: APROVADO
  2_selecionar_item_01: REPROVADO
  3_mover_para_item_02: REPROVADO
  4_espaco_em_item_02: APROVADO
  5_mover_para_item_03: REPROVADO
  6_selecionar_item_03: REPROVADO
  7_enter_em_Executar: APROVADO
  8_limpar_selecao: APROVADO
  9_selecionar_Todos: REPROVADO
  10_limpeza_final: APROVADO
```

## 3. Achados

```yaml
achados:
  - id: H0041-MANUAL-R02-001
    gravidade: MATERIAL
    componente: Enter_Todos
    esperado:
      selecao:
        - item_01
        - item_03
        - item_05
        - item_07
    observado: Enter sem seleção não selecionou os quatro itens
    impacto: seleção em massa não funciona em TTY real

  - id: H0041-MANUAL-R02-002
    gravidade: MATERIAL
    componente: chip_Enter
    esperado:
      rotulo: Executar
      estado: INATIVO
      apresentacao: cor_inativo
    observado:
      rotulo: executar
      estado_visual: ATIVO
    impacto: estado inativo não segue o contrato de cor

  - id: H0041-MANUAL-R02-003
    gravidade: MATERIAL
    componente: chip_Espaco
    esperado:
      item_nao_selecionavel: INATIVO
      apresentacao: cor_inativo
    observado:
      item_nao_selecionavel: ATIVO
    impacto: barra apresenta ação indisponível como ativa
```

## 4. Comportamentos preservados

```yaml
estado_inicial: APROVADO
Espaco_em_item_nao_selecionavel_sem_efeito: APROVADO
Enter_em_Executar_sem_operacao: APROVADO
Esc_limpa_selecao: APROVADO
Esc_sem_selecao_encerra: APROVADO
```

## 5. Conclusão

```yaml
status_literal: MANUAL_VALIDATION_FAILED
resultado_geral: REPROVADO
achados:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
proxima_categoria: DECISAO_DE_CONFIGURACAO_E_PATCH_DO_HANDOFF
```
