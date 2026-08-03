---
name: REL-PATCH-H0045-P01-correcao-template-e-conteudo-renderizado
description: "Delta factual do patch P01 sobre o handoff H-0045: restauração de critérios de aceite canônicos e correção da redução técnica de paginação"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: "2026-07-30"
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  cadeia_raiz: H-0045
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0045.md
  achados_tratados:
    - QAH45-001
    - QAH45-002
---

# REL-PATCH-H0045-P01 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: H-0045
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0045.md
achados_tratados:
  - QAH45-001
  - QAH45-002
achados_resolvidos:
  - QAH45-001
  - QAH45-002
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QAH45-001
    alteracao: >
      §9 restaurada como "Critérios de aceite" canônica, com tabela
      ID/Critério/Evidência independente esperada (CA-H0045-01 a
      CA-H0045-27), cobrindo paginação limitada, extremos, cursor, página
      sem navegáveis, conteúdo multilinha, as três políticas de quebra,
      modo normal/verboso, repaginação material, filtro/atualização, dois
      consoles, seleção, ADR-0037, indicador, chips, loader, regressão
      completa, demonstração automatizada e validação manual pendente.
      "Decisões técnicas" movida para nova §10 (era §9); §§10-16 antigas
      renumeradas para §§11-17; referências internas de seção atualizadas.
  - id_achado: QAH45-002
    alteracao: >
      Removidas as três reduções indevidas: "cada item ocupa exatamente
      uma linha física" (D-TEC-06 antigo), "politica_quebra ignorada
      silenciosamente" (D-TEC-07 antigo) e exclusão de "modo verboso
      multi-linha + paginação" do escopo negativo. D-TEC-02/04/05
      reescritas para distinguir grade lógica de navegação (inalterada) de
      conteúdo físico paginado, com uma autoridade física única
      (mapa_fisico_de_itens, nova função pública em tela/renderizador.py,
      reaproveitando _altura_quebra_item/_linhas_distribuicao_matricial/
      _linhas_fisicas_por_item já existentes) consumida por
      tela/paginacao.py via import local, evitando cálculo duplicado.
      D-TEC-06 novo delimita o universo (console com distribuicao_matricial
      já coberto por H-0040; conteudo_externo hierárquico permanece fora,
      como fronteira pré-existente da H-0036, não redução nova). D-TEC-07
      novo dá efeito real às três políticas de quebra (transcritas
      verbatim de contrato_console.md §12), com fragmentação de item maior
      que a página. D-TEC-17 novo resolve cursor/indicador de item
      fragmentado por derivação de D12 + D-PAG-03 (sem inventar regra de
      interface). Duas fixtures novas adicionadas ao manifesto
      (h0045_paginacao_modo_verboso_multilinha.json,
      h0045_paginacao_politicas_quebra.json), com finalidade e motivo
      registrados por caminho. §6.1 reestruturada no formato
      caminho/finalidade/motivo_da_inclusao_ou_preservacao.
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
    delta: >
      Reescrita integral preservando decisões D-PAG-01 a D-PAG-14 e a
      cadeia de autoridade; nenhuma ADR, contrato ou nomenclatura alterada.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "rg '^## 9\\. Critérios de aceite$' e tabela ID/Critério/Evidência"
    resultado_compacto: "presentes, com 27 critérios nominais"
  - comando_ou_metodo: "rg 'ignorada silenciosamente|cada item navegável ocupa exatamente uma linha|modo verboso multi-linha.*fora de escopo|paginação aplica-se somente.*grade'"
    resultado_compacto: "nenhuma ocorrência"
  - comando_ou_metodo: "rg 'evitar_quebra|permitir_quebra|permitir_quebra_somente_se_maior_que_pagina|modo verboso|conteúdo renderizado|multilinha|plano de paginação'"
    resultado_compacto: "presentes materialmente em §4, §6.3, §10 (D-TEC-06/07/17), §9, §11, §12"
  - comando_ou_metodo: "git status --short --untracked-files=all; git diff --cached --name-only"
    resultado_compacto: "stage vazio; apenas H-0045 (modificado) e relatório P01 (novo) tocados nesta etapa"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
