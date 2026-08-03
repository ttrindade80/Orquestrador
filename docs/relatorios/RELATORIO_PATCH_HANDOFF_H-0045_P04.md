---
name: REL-PATCH-0045-P04-handoff-politicas-e-metodo-adaptativo
description: "Corrige D-TEC-07/§6.4 conforme contrato_console.md v0.2 e proíbe reconstrução de modelo durante resize"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: 2026-08-02
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md
  achados_tratados:
    - HANDOFF_METHOD_DEFECT
---

# REL-PATCH-0045-P04 — Patch de handoff (políticas e método adaptativo)

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md
achados_tratados:
  - HANDOFF_METHOD_DEFECT
achados_resolvidos: []  # correção documental; resolução material pertence a PATCH_IMPLEMENTACAO futuro
achados_pendentes:
  - VM-H0045-R06-001
  - QA-H0045-P08-001
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: HANDOFF_METHOD_DEFECT
    alteracao: >
      D-TEC-07 (§10) substituída pela definição vigente das três políticas
      (contrato_console.md §12 v0.2); removida a afirmação de equivalência
      entre evitar_quebra e permitir_quebra_somente_se_maior_que_pagina e a
      ambiguidade registrada em §6.4 (bullet removido). Nova seção 19 proíbe
      expressamente reconstrução de conteúdo lógico durante resize, define
      três telas fixas de validação (uma por política), determina
      substituição/desativação dos casos adaptativos LARGURA/PERMITIR/
      EVITAR/CONDICIONAL, preserva VAZIO/CONTINUACAO com exigência de
      conteúdo fixo, autoriza nominalmente os arquivos de implementação
      futura, exige testes por hash/comparação estrutural e redireciona a
      validação manual 15/17 às três telas, sem reabrir 6/17-14/17.
arquivos_alterados:
  - caminho: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
    delta: >
      §10 D-TEC-07 corrigida; bullet de ambiguidade removido de §6.4; nova
      seção 19 (9 subseções, 8 critérios de aceite CA-H0045-PH-12..19).
arquivos_criados: []
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: leitura integral de contrato_console.md §12 (v0.2) vs. D-TEC-07 antiga
    resultado_compacto: "confirmada divergência; contrato já corrigido, handoff desatualizado — corrigido"
  - comando_ou_metodo: leitura focal de demo/demo.py (SIGWINCH e _aplicar_caso_validacao_adaptativo, linhas ~929-1005 e ~1471-1483)
    resultado_compacto: "confirma reconstrução de itens e zeragem de foco/cursores/pagina_atual no resize — proibição de §19.1 é factualmente ancorada"
  - comando_ou_metodo: leitura focal de demo/casos_validacao_paginacao.py (constructores H0045-VAL-*)
    resultado_compacto: "confirma geração de conteúdo em função de W/C nos quatro casos a substituir"
  - comando_ou_metodo: leitura focal de tela/paginacao.py (plano_de_paginacao/_fragmentar_entrada)
    resultado_compacto: "confirma que evitar_quebra e permitir_quebra_somente_se_maior_que_pagina caem no mesmo ramo hoje — motiva autorização de correção em §19.6"
  - comando_ou_metodo: "git diff --check -- docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md"
    resultado_compacto: "sem erro de whitespace (exit 0)"
  - comando_ou_metodo: grep de "6/17"/"VM-H0045-R06-001"/"QA-H0045-P08-001" no arquivo patcheado
    resultado_compacto: "6/17-14/17 preservadas como não reexecutadas; os dois achados aparecem registrados como não resolvidos em §19.7/§19.8"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
