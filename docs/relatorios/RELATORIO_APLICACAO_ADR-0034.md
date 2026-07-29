---
name: REL-ALT-0034-aplicacao-selecao-multipla
description: "Aplicação documental da ADR-0034 (seleção múltipla e fluxo focal de processamento) aos contratos, nomenclatura, índice de ADRs e backlog"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED_AWAITING_QA
  data: "2026-07-28"
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0034
  artefato_principal: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  autoridade_principal: null
  cadeia_raiz: null
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0034.md
  achados_tratados: []
---

# REL-ALT-0034 — Aplicação documental da ADR-0034

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0034
status_literal: ADR_APPLICATION_COMPLETED_AWAITING_QA
```

## 2. Delta material

```yaml
delta_material:
  - contrato_console.md: nova seção 23 fecha D-SEL-01 a D-SEL-11 (identidade e
    persistência da seleção, invariantes, reconciliação, teclas Espaço/Enter/Esc,
    indicadores, chip Espaço, fronteira com ITEM-0004)
  - contrato_barra_de_menus.md: nova seção 23 fecha a condição de existência do
    chip Espaço e o rótulo dinâmico Todos/Executar de [⏎] para politica_selecao multipla
  - contrato_tela_json.md: nova seção 34 fecha o campo raiz perfil, o perfil
    resultado_execucao, o binding da tela de resultado e a validação antecipada
    (CONFIGURACAO_INVALIDA)
  - contrato_composicao_corpo.md: nova subseção 3.1.1 registra a tela de resultado
    como composição de um único console passivo, sem tipo de elemento novo
  - contrato_json_console.md: nova seção 14 fecha o protocolo provisório de
    entrada/execução por CLI, canais do processo, classificação de sucesso/falha,
    envelope de erro multinível e dry-run/execução real reversível
  - INDICE_ADR.md: linha da ADR-0034 registrada
  - backlog.md: ITEM-0006 atualizado para pronto_para_handoff; criados ITEM-0018
    a ITEM-0021 (itens bloqueados de D-SEL-24)

delta_nomenclatura:
  modulos_alterados:
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    - docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
  termos_criados:
    - seleção múltipla, conjunto de IDs estáveis, reconciliação, item selecionável,
      lote reconciliado (módulo 32)
    - perfil (módulo 02)
    - tela de resultado, origem suspensa (módulo 20)
    - documento de resultado de execução, envelope de erro multinível (módulo 42)
  aliases_ou_historicos: []

delta_terminologico:
  modulos_alterados:
    - "02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md"
    - "20_TELA_CORPO_E_COMPOSICAO.md"
    - "31_BARRA_DE_MENUS_E_CHIPS.md"
    - "32_CONSOLE.md"
    - "42_DADOS_EXTERNOS_MULTINIVEL.md"
    - "43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md"
  termos_adicionados:
    - seleção múltipla
    - conjunto de IDs estáveis
    - reconciliação
    - item selecionável
    - lote reconciliado
    - perfil
    - tela de resultado
    - origem suspensa
    - documento de resultado de execução
    - envelope de erro multinível
  termos_alterados: []
  distincoes_adicionadas:
    - seleção única (ADR-0031) × seleção múltipla (ADR-0034)
    - JSON externo de conteúdo (genérico) × documento de resultado de execução
    - carregamento genérico × carregamento do temporário de resultado
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0034.md
    finalidade: relatório factual desta aplicação

arquivos_alterados:
  - caminho: docs/adr/INDICE_ADR.md
    delta: linha da ADR-0034 registrada
  - caminho: docs/backlog.md
    delta: ITEM-0006 atualizado; ITEM-0018 a ITEM-0021 criados
  - caminho: docs/contratos/contrato_console.md
    delta: seção 23 (D-SEL-01 a D-SEL-11)
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: seção 23 (chip Espaço, rótulo Todos/Executar)
  - caminho: docs/contratos/contrato_tela_json.md
    delta: seção 34 (perfil, resultado_execucao, validação antecipada)
  - caminho: docs/contratos/contrato_composicao_corpo.md
    delta: subseção 3.1.1 (tela de resultado como composição)
  - caminho: docs/contratos/contrato_json_console.md
    delta: seção 14 (protocolo provisório e envelope de erro)
  - caminho: docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    delta: termo perfil; nota de seleção múltipla como estado de runtime
  - caminho: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    delta: termos tela de resultado e origem suspensa
  - caminho: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    delta: referência de fechamento da ADR-0034 sobre termos já genéricos
  - caminho: docs/nomenclatura/32_CONSOLE.md
    delta: terminologia de seleção múltipla (§4.6)
  - caminho: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    delta: documento de resultado de execução (§4.5)
  - caminho: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
    delta: carregamento do temporário de resultado (§4.5)
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git status --short --untracked-files=all (antes e depois)"
    resultado_compacto: "worktree conforme esperado; nenhum arquivo fora da lista permitida"
    prova_semantica: "somente os 13 arquivos autorizados aparecem como modificados, mais os 3 itens preexistentes"
  - comando_ou_metodo: "git diff --check"
    resultado_compacto: "vazio"
    prova_semantica: "nenhum conflito de whitespace"
  - comando_ou_metodo: "git diff --cached --name-only"
    resultado_compacto: "vazio"
    prova_semantica: "stage permanece vazio"
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - "ADR-0034 (arquivo próprio) não foi alterada: o template TEMPLATE_ADR.md não
    prevê campo distinto para 'aplicação executada'; o status aceita já registra
    a aprovação, mesmo padrão observado na aplicação da ADR-0033."
```
