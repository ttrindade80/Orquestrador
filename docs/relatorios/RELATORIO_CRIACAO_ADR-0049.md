---
name: REL-CRIACAO-0049-composicao-justificacao-global-texto-tui
description: "Resultado factual da criação da ADR-0049 (ITEM-0027)"
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_ADR
  status: ADR_CREATED
  data: 2026-08-19
rastreabilidade:
  etapa: CRIAR_ADR
  objeto: ITEM-0027
  artefato_principal: docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
  autoridade_principal: null
  decisoes_materializadas:
    - D-0027-01
    - D-0027-02
    - D-0027-03
    - D-0027-04
    - D-0027-05
    - D-0027-06
    - D-0027-07
    - D-0027-08
    - D-0027-09
---

# REL-CRIACAO-0049 — Criação documental

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_ADR
artefato_criado: docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
status_literal: ADR_CREATED
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - caminho_ou_decisao: docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md
  - caminho_ou_decisao: docs/nomenclatura/01_NUCLEO_COMUM.md
  - caminho_ou_decisao: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
  - caminho_ou_decisao: docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - caminho_ou_decisao: docs/templates/TEMPLATE_ADR.md
decisoes_materializadas:
  - id: D-0027-01
    sintese: Autoridade global única de composição/justificação, substituindo autoridades locais equivalentes.
  - id: D-0027-02
    sintese: Contrato canônico novo e explícito, previsto em docs/contratos/contrato_composicao_textual.md, a materializar em APLICAR_ADR.
  - id: D-0027-03
    sintese: Peculiaridades históricas não são preservadas automaticamente; convergem salvo semântica necessária de consumidor.
  - id: D-0027-04
    sintese: Escopo do núcleo comum — wrap, composição de linhas, justificação, largura visual, segurança ANSI.
  - id: D-0027-05
    sintese: Fronteira preservada com regras semânticas próprias dos consumidores.
  - id: D-0027-06
    sintese: Padding/alinhamento/colunas/chips/grade/moldura não são justificação de parágrafo.
  - id: D-0027-07
    sintese: Compatibilidade estrutural integral com corpo.arranjo, tiling, paginação, taxonomia e schema.
  - id: D-0027-08
    sintese: Consistência obrigatória entre medição e renderização sob a mesma autoridade canônica.
  - id: D-0027-09
    sintese: Truncamento de linha única permanece distinguível de wrap/composição.
```

Não reproduz a especificação nem o conteúdo integral do relatório de
levantamento; a ADR referencia a evidência sem reproduzi-la.

## 3. Delta documental

```yaml
delta_material:
  - Nova ADR-0049 registrando autoridade global de composição/justificação textual da TUI.
  - Papel do contrato canônico previsto (docs/contratos/contrato_composicao_textual.md) definido sem criá-lo.
  - Tabela de artefatos afetados aponta os módulos de produção a reconciliar em aplicação futura.
  - Dimensionamento gerencial de 2 handoffs registrado como informação de planejamento, sem criar handoff.
arquivos_criados:
  - docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
  - docs/relatorios/RELATORIO_CRIACAO_ADR-0049.md
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo: "git branch --show-current"
    resultado_compacto: "master"
  - comando_ou_metodo: "git rev-parse HEAD"
    resultado_compacto: "bd6fb46d8b841b38f3098f7187d3b71bee3c2ad7 (bate com o baseline observado)"
  - comando_ou_metodo: "git status --short"
    resultado_compacto: "Somente arquivo não rastreado pré-existente do levantamento (RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md); sem alteração inesperada"
  - comando_ou_metodo: "rg -n 'ADR-0048|ADR-0049' docs/adr/INDICE_ADR.md"
    resultado_compacto: "Somente ADR-0048 (predecessora vigente) encontrada; nenhuma colisão de ADR-0049"
  - comando_ou_metodo: "find docs -iname '*template*'"
    resultado_compacto: "Localizado docs/templates/TEMPLATE_ADR.md e TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md, usados para compatibilizar o formato dos dois artefatos"
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas:
  - "O índice docs/adr/INDICE_ADR.md não foi alterado nesta etapa, por estar fora dos arquivos permitidos."
  - "Nenhum handoff foi criado; o dimensionamento em 2 handoffs consta apenas como informação de planejamento na ADR."
```

## 6. Evidências separadas

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md
    finalidade: Evidência factual do levantamento que fundamenta o contexto e a tabela de artefatos afetados da ADR-0049.
    leitura_necessaria_para:
      - APLICAR_ADR
