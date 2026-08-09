---
name: RELATORIO_APLICACAO_ADR-0043
description: "Resultado factual da aplicação documental da ADR-0043"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLIED
  data: 2026-08-08
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0043
  artefato_principal: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  autoridade_principal: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  cadeia_raiz: ITEM-0007
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0043_P01.md
  achados_tratados: []
---

# REL-ALT-ADR-0043 — Aplicação documental

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0043
status_literal: ADR_APPLIED
```

## 2. Delta material

```yaml
delta_material:
  - "Ajuda passou a ser universal, sempre presente, ativa e última; insuficiência de largura mantém erro_layout."
  - "arvore_colapsavel passou a distinguir os chips contextuais de expansão/recolhimento da seleção, derivados do item corrente."
  - "ITEM-0007 foi reconciliado para QA_APLICACAO_ADR; H-0053 permanece interrompido."
delta_nomenclatura:
  modulos_alterados:
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
  termos_criados:
    - "Ajuda universal"
    - "chip contextual de arvore_colapsavel"
    - "[␣] Expandir"
    - "[␣] Recolher"
  termos_alterados:
    - "[?] Ajuda: obrigatória em toda tela e última"
    - "relação entre foco, cursor, item corrente e seleção em arvore_colapsavel"
  aliases_ou_historicos:
    - "Formulação de Ajuda opcional/declarativa por tela: supersedida parcialmente pela ADR-0043."
```

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0043.md
    finalidade: "Registrar a execução documental e a rastreabilidade da aplicação."
arquivos_alterados:
  - caminho: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
    delta: "Status aceita e aplicada; aplicação executada; QA da aplicação pendente."
  - caminho: docs/adr/INDICE_ADR.md
    delta: "ADR-0043 inserida como aceita e aplicada, com QA da aplicação pendente."
  - caminho: docs/backlog.md
    delta: "ITEM-0007 mantém-se em_andamento; próxima ação é QA_APLICACAO_ADR ADR-0043."
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: "Ajuda universal, ordem e chips contextuais de árvore."
  - caminho: docs/contratos/contrato_chip.md
    delta: "Existência de Ajuda, estados contextuais e separação funcional de Espaço."
  - caminho: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    delta: "Termos universais de Ajuda e chips contextuais."
  - caminho: docs/nomenclatura/32_CONSOLE.md
    delta: "Invariantes de foco, cursor, item corrente e reconciliação sem algoritmo novo."
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "rg focal em contrato JSON"
    resultado_compacto: "Nenhuma contradição material de schema; arquivo preservado."
    prova_semantica: "A representação continua declarativa e não recebe campo novo."
  - comando_ou_metodo: "rg focal de Ajuda, Espaço e cursor/foco"
    resultado_compacto: "Regras universais, contextuais e invariantes presentes."
    prova_semantica: "Folha usa Expandir inativo; Selecionar permanece distinto."
  - comando_ou_metodo: "git diff --check"
    resultado_compacto: "Sem erro de whitespace."
    prova_semantica: "Integridade textual verificada."
  - comando_ou_metodo: "git diff/status/stage focal"
    resultado_compacto: "Somente os oito caminhos autorizados foram escritos; stage vazio."
    prova_semantica: "H-0053, código e fixtures não foram alterados."
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - "QA_APLICACAO_ADR permanece pendente; H-0053 só será reconciliado após QA aprovado."
```
