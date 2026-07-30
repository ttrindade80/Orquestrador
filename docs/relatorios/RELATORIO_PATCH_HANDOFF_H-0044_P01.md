---
name: REL-PATCH-H0044-P01-validacao-manual-roteiros-completos
description: "Delta factual: RVMs de H-0044 passam a conter comando integral, IDs concretos, sequências físicas completas e procedimento de redimensionamento"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: 2026-07-29
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: validacao_manual
  cadeia_raiz: H-0044
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0044.md
  achados_tratados: [QA-HANDOFF-H0044-001]
---

# REL-PATCH-H0044-P01 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: H-0044
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0044.md
achados_tratados: [QA-HANDOFF-H0044-001]
achados_resolvidos: [QA-HANDOFF-H0044-001]
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-HANDOFF-H0044-001
    alteracao: >-
      seção 11.1 reescrita: cada um dos dez RVMs passou a repetir
      integralmente `comando: python demo/demo.py
      h0044_fluxo_execucao_integrado`, declarar `itens_utilizados` com IDs
      literais dos oito itens (posições derivadas da distribuição
      matricial de coluna única reutilizada de H-0041, cursor inicial em
      item_01) e registrar `sequencia_fisica` somente com teclas
      suportadas (Seta para baixo × N, Espaço, Insert, Enter, Esc).
      RVM-04 (item_05), RVM-05 (item_01 + item_inexistente), RVM-06/07/08
      (controles sintéticos) e RVM-10 (item_07) substituíram instruções
      descritivas por sequências físicas completas. RVM-09 recebeu
      procedimento reproduzível de dois terminais com `tty`, `stty size` e
      `SIGWINCH` via `stty -F`. O gabarito de alternativas de cada roteiro
      foi completado com os termos aplicáveis do conjunto canônico. A
      evidência de CA-H0044-17 foi ajustada para exigir os sete pontos do
      achado.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0044_P01.md
arquivos_alterados:
  - caminho: docs/handoff/H-0044-integracao-fluxo-focal-dry-run-restauracao-origem.md
    delta: seção 11.1 (dez RVMs) e evidência de CA-H0044-17 reescritas
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git diff --check"
    resultado_compacto: sem problemas de whitespace
  - comando_ou_metodo: "grep -E 'navegar até|selecionar <item>|selecionar o item|redimensionar terminal|mesmo comando|comando acima'"
    resultado_compacto: nenhuma ocorrência
  - comando_ou_metodo: "grep -c '^id: RVM-H0044-'"
    resultado_compacto: 10
  - comando_ou_metodo: "grep -c comando integral por linha exata"
    resultado_compacto: presente nos dez RVMs
  - comando_ou_metodo: "git status --short / git diff --cached --name-only"
    resultado_compacto: stage vazio; nenhum caminho fora do ciclo ADR-0037/H-0044
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```

Nenhum código foi alterado; nenhum teste foi executado; nenhuma validação
manual foi preenchida; nenhuma sequência material foi delegada ao usuário;
os dez cenários originais (toggle, dry-run, execução real, parcial, falha
operacional, resultado inválido, interrupção, redimensionamento, duplo
`Esc`) foram preservados sem novo cenário nem remoção. O handoff continua
`status: READY_FOR_IMPLEMENTATION`. Manifesto, decisões D-H4-01 a D-H4-10,
IDs dos oito itens, critérios CA-H0044-01 a CA-H0044-16 e demais seções
listadas como preservadas permanecem intactos.
