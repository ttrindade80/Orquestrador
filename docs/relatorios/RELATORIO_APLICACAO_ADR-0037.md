---
name: REL-ALT-0037-aplicacao-adr-0037
description: "Resultado factual da aplicação documental da ADR-0037 aos contratos, nomenclatura, estilo, índice e backlog"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED
  data: 2026-07-29
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0037
  artefato_principal: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  autoridade_principal: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  cadeia_raiz: ITEM-0006
  predecessor_imediato: ADR_APPROVED
  achados_tratados: []
---

# REL-ALT-0037 — Aplicação documental da ADR-0037

> Relatório sucinto, factual, assertivo e autocontido.

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0037
status_literal: ADR_APPLICATION_COMPLETED
```

## 2. Delta material

```yaml
delta_material:
  - materializou cor_alerta: amarelo em config/estilo.json
  - reconciliou cor_inativo × cor_alerta e ativo destacado nos contratos de estilo/chip/barra
  - registrou [Ins] Dry-Run, ativação de Executar e supersessão pontual de D-SEL-19
  - especializou Handoff 4 em contrato_console (transição, origem, retornos, limpeza)
  - propagou terminologia nos módulos 10, 20, 31 e 32 sem duplicar autoridades
  - indexou ADR-0037 e reconciliou ITEM-0006, ITEM-0011 e ITEM-0020
delta_nomenclatura:
  modulos_alterados:
    - docs/nomenclatura/10_ESTILO.md
    - docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
  termos_criados:
    - reativação da origem
    - transição focal
    - tela ativa
  termos_especializados:
    - origem suspensa
    - cor_alerta
    - chip de alternancia
    - dry-run ativo
    - restauracao da origem
  aliases_ou_historicos: []
```

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0037.md
    finalidade: registrar a aplicação documental
arquivos_alterados:
  - caminho: config/estilo.json
    delta: cor_alerta amarelo; remoção da pendência correspondente; tiling preservado
  - caminho: docs/contratos/contrato_estilo.md
    delta: ADR-0037; valores concretos; ativo×destacado; loader/renderer futuros
  - caminho: docs/contratos/contrato_chip.md
    delta: três condições visuais; [Ins] Dry-Run; sem novo schema
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: Dry-Run; ativação de Executar; supersessão D-SEL-19
  - caminho: docs/contratos/contrato_console.md
    delta: §23.9 Handoff 4; supersessões; fronteiras H-0041/42/43
  - caminho: docs/nomenclatura/10_ESTILO.md
    delta: cor_alerta amarelo; distinção de cor_inativo
  - caminho: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    delta: origem suspensa especializada; tela ativa; reativação; transição
  - caminho: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    delta: [Ins] Dry-Run; ativo destacado; ITEM-0020
  - caminho: docs/nomenclatura/32_CONSOLE.md
    delta: termos de retorno dry-run/real; foco e cursor
  - caminho: docs/adr/INDICE_ADR.md
    delta: entrada ADR-0037 após ADR-0036
  - caminho: docs/backlog.md
    delta: ITEM-0006, ITEM-0011, ITEM-0020
arquivos_removidos: []
```

Supersessões aplicadas nos contratos: D-SEL-19 (chip dry-run); fronteira da barra; fora de escopo ADR-0036 (dry-run na UI e cor_alerta). ADRs 0034–0036 não editadas.

Reconciliação backlog: H1–H3 concluídos; especificação H4 e ADR-0037 aprovada/aplicada; próxima ação `CRIAR_HANDOFF`. ITEM-0011 permanece aberto até implementação. ITEM-0020 aberto para padronização genérica.

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: baseline git (branch/HEAD/stage/status)
    resultado_compacto: master @ 8af243c; stage vazio; worktree só ADR-0037 e relatórios de criação/QA
    prova_semantica: BASELINE_OK
  - comando_ou_metodo: python -m json.tool config/estilo.json
    resultado_compacto: JSON válido
    prova_semantica: cor_alerta e cor_inativo presentes; pendência tiling preservada
  - comando_ou_metodo: git diff --check + status final
    resultado_compacto: sem whitespace errors; stage vazio; somente caminhos autorizados
    prova_semantica: ADR/criação/QA intactos; sem implementação
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - contrato_json_console.md listado na ADR como afetado, mas fora da lista autorizada desta etapa — não alterado
  - materialização runtime de cor_alerta e handoff de implementação permanecem futuros
```
