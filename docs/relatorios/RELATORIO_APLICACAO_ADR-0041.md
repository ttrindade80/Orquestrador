---
name: RELATORIO_APLICACAO_ADR-0041
description: "Aplicação documental da ADR-0041 (paginação universal por PageUp/PageDown) aos contratos de console, chip e barra de menus e aos módulos de nomenclatura 21 e 31"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED
  data: "2026-08-07"
rastreabilidade:
  etapa: aplicacao_documental
  objeto: ADR-0041-paginacao-universal-por-pageup-e-pagedown
  artefato_principal: docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
  autoridade_principal: docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
  cadeia_raiz: docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0041.md
  achados_tratados: []
---

# REL-ALT-0041 — Aplicação da ADR-0041

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0041-paginacao-universal-por-pageup-e-pagedown
status_literal: ADR_APPLICATION_COMPLETED
```

## 2. Delta material

```yaml
delta_material:
  - "Toda paginação comum do console passa a usar exclusivamente as teclas PageUp (página anterior) e PageDown (próxima página); ',', '<', '.' e '>' deixam de ter qualquer função de paginação, sem status de alias, atalho ou fallback."
  - "A representação canônica dos controles de paginação na barra de menus passa de [<][>] para [PgUp][PgDn] Páginas em todos os documentos normativos afetados."
  - "As demais treze decisões de paginação limitada da ADR-0038 (D-PAG-01 a D-PAG-13) permanecem integralmente preservadas e sem alteração de texto."
delta_nomenclatura:
  modulos_alterados:
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  termos_criados:
    - "teclas universais de paginação PageUp/PageDown (ADR-0041)"
    - "representação canônica [PgUp][PgDn] Páginas (ADR-0041)"
  termos_alterados:
    - "paginação limitada de [<][>] (ADR-0038) → paginação limitada de [PgUp][PgDn] (ADR-0038; especializada pela ADR-0041)"
    - "entradas aceitas de página anterior/próxima página (ADR-0038) → entradas universais PageUp/PageDown (ADR-0041)"
  aliases_ou_historicos:
    - "',', '<', '.', '>' e [<][>] permanecem citados exclusivamente em passagens históricas/comparativas de substituição — não como notação vigente"
```

Não descreve passo a passo. Delta terminológico completo:

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  termos_adicionados: []
  termos_alterados:
    - "§4.7/§4.3: chips [<][>] renomeados para [PgUp][PgDn] em todas as tabelas e diagramas de ordem canônica"
  distincoes_adicionadas:
    - "Nova subseção 4.8 em nomenclatura/21: tecla e representação universais de paginação (ADR-0041), distinta dos conceitos de página, repaginação e paginação limitada (ADR-0038), que permanecem intocados"
  fronteiras_alteradas:
    - "Nenhuma fronteira conceitual foi alterada; apenas tecla de acionamento e notação visual, conforme escopo fechado da ADR-0041 (D-PGU-07)"
```

`docs/nomenclatura/32_CONSOLE.md` foi lido e avaliado; não contém nenhuma
ocorrência de `[<]`, `[>]`, `[<][>]` ou de referência a `,`/`<`/`.`/`>` como
entrada de paginação — nenhuma alteração foi material nesse módulo.

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0041.md
    finalidade: registrar a aplicação documental desta etapa
arquivos_alterados:
  - caminho: docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
    delta: "status proposta → aceita; QA da ADR registrado (ADR_APPROVED, patch P01); critérios de aplicação marcados conforme materializado; QA da aplicação mantido pendente"
  - caminho: docs/adr/INDICE_ADR.md
    delta: "nova linha nominal da ADR-0041, status aceita, 2026-08-07"
  - caminho: docs/contratos/contrato_console.md
    delta: "§3, §12, §14, §24 (intro, título, 24.3, 24.11, 24.13): [<][>] → [PgUp][PgDn]; entradas D-PAG-14 especializadas para PageUp/PageDown; ADR-0041 adicionada a adrs_aplicadas e remissões"
  - caminho: docs/contratos/contrato_chip.md
    delta: "§5, §7, §9, §14: [<][>] → [PgUp][PgDn]; nota de entradas aceitas reescrita para PageUp/PageDown; ADR-0041 adicionada a adrs_aplicadas"
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: "§5, §7, §8.3, §20, §24 (integral): [<][>] → [PgUp][PgDn]; §24.4 reescrita com entradas PageUp/PageDown; ADR-0041 adicionada a adrs_aplicadas"
  - caminho: docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    delta: "novos termos proprietários; nova subseção 4.8 (teclas e representação universais); §4.6 e §7 atualizadas; ADR-0041 adicionada à proveniência"
  - caminho: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    delta: "§3, §4.3, §4.4.2 (título e corpo), §5, §7: [<][>] → [PgUp][PgDn]; novos termos proprietários; ADR-0041 adicionada à proveniência"
arquivos_removidos: []
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "grep -n '\\[<\\]|\\[>\\]|PgUp|PgDn|PageUp|PageDown' nos oito arquivos alteráveis"
    resultado_compacto: "todas as ocorrências residuais de [<]/[>] são exclusivamente comparativas/históricas dentro de frases de substituição ('substituindo ,/</./> e [<][>] por PageUp/PageDown e [PgUp][PgDn]'); nenhuma notação [<][>] permanece como autoridade vigente"
    prova_semantica: "nenhuma tabela, diagrama de ordem canônica ou bloco YAML de entradas_aceitas cita mais ,/</./> ou [<][>] como valor ativo nos sete artefatos aplicados"
  - comando_ou_metodo: "git diff --check nos oito arquivos alteráveis mais o relatório"
    resultado_compacto: "sem saída — nenhum erro de espaço em branco"
    prova_semantica: "diffs limpos, sem trailing whitespace"
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - "docs/nomenclatura/32_CONSOLE.md foi lido e avaliado conforme o manifesto, mas não sofreu alteração material — nenhuma ocorrência de notação antiga de paginação existia nesse módulo."
  - "QA da aplicação documental não foi executado nesta etapa, conforme limite desta execução."
```
