---
name: REL-VALIDACAO-MANUAL-H0041
description: "Primeira validação manual TTY do H-0041"
metadata:
  type: relatorio_validacao_manual
  etapa: VALIDACAO_MANUAL
  status: MANUAL_VALIDATION_FAILED
  data: 2026-07-28
rastreabilidade:
  handoff: H-0041
  qa_anterior: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P02.md
  executor: USUARIO
  ambiente: terminal_TTY_real
---

# Validação manual TTY — H-0041

## Execução

```yaml
comando: >-
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao
  --tela config/telas/demo/h0041_selecao_multipla_oito_itens.json
executor: USUARIO
ambiente: terminal_TTY_real
resultado: REPROVADO
```

## Resultado dos passos

```yaml
passos:
  1: APROVADO
  2: REPROVADO
  3: REPROVADO
  4: APROVADO
  5: REPROVADO
  6: REPROVADO
  7: APROVADO
  8: APROVADO
  9: REPROVADO
  10: APROVADO
```

## Achados

```yaml
achados:
  - id: H0041-MANUAL-001
    gravidade: MATERIAL
    componente: chip_Espaco
    esperado: INATIVO sobre item não selecionável
    observado: permaneceu ATIVO sobre item_02
    impacto: barra apresenta ação indisponível como ativa

  - id: H0041-MANUAL-002
    gravidade: MATERIAL
    componente: chip_Enter
    esperado: Executar visível e INATIVO quando existe seleção
    observado: Executar permaneceu visualmente ATIVO
    passos_afetados: [2, 3, 5, 6]
    impacto: estado lógico não se materializa corretamente na barra

  - id: H0041-MANUAL-003
    gravidade: MATERIAL
    componente: selecionar_Todos_e_redesenhar_barra
    esperado: quatro tg incluídos e chip Executar INATIVO
    observado: quatro tg preenchidos, mas chip permaneceu Todos ATIVO
    impacto: divergência entre os itens selecionados e a barra
```

O passo 9 não prova falha na inclusão dos quatro itens: seus indicadores `tg`
foram preenchidos. A falha comprovada é a ausência de sincronização da barra.

## Comportamentos aprovados

```yaml
navegacao: APROVADA
itens_nao_navegaveis: APROVADOS
toggle_de_itens: APROVADO
indicadores_ec_tg: APROVADOS
Enter_em_Executar_sem_efeito: APROVADO
operacao_externa_ausente: APROVADO
Esc_limpa_selecao: APROVADO
Esc_sem_selecao_encerra: APROVADO
```

## Conclusão

```yaml
status_literal: MANUAL_VALIDATION_FAILED
resultado_geral: REPROVADO
achados:
  - H0041-MANUAL-001
  - H0041-MANUAL-002
  - H0041-MANUAL-003
proxima_categoria: PATCH_IMPLEMENTACAO
```
