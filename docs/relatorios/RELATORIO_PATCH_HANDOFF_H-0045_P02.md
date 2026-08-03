---
name: REL-PATCH-H0045-P02-correcao-metodo-validacao-adaptativa
description: "Delta factual do patch P02 sobre o handoff H-0045: corrige o método de implementação/demonstração/validação de 15/17-17/17 para geometria adaptativa em vez de fixture única calibrada em 80x24"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: "2026-08-01"
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P01.md
  achados_tratados:
    - PH-H0045-001
    - PH-H0045-002
    - PH-H0045-003
    - PH-H0045-004
    - PH-H0045-005
    - PH-H0045-006
---

# REL-PATCH-H0045-P02 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P01.md
achados_tratados:
  - PH-H0045-001
  - PH-H0045-002
  - PH-H0045-003
  - PH-H0045-004
  - PH-H0045-005
  - PH-H0045-006
achados_resolvidos:
  - PH-H0045-001
  - PH-H0045-002
  - PH-H0045-003
  - PH-H0045-004
  - PH-H0045-005
  - PH-H0045-006
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

Diagnóstico confirmado por leitura de P10/P11: as fixtures permanentes
provaram os fenômenos exclusivamente com valores absolutos calibrados para
80x24 (capacidade 16 linhas/página, item de 31 linhas, etc. —
RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P10.md, P11), sem garantia de
equivalência em outra geometria. `h0045_paginacao_politicas_quebra.json`
prova simultaneamente `evitar_quebra` e página de continuação pura na mesma
fixture, tornando a validação manual ambígua e frágil a redimensionamento.

```yaml
delta_material:
  - id_achado: PH-H0045-001..006
    alteracao: >
      Nova §18 ("Correção do método de validação — PATCH_HANDOFF P02"),
      normativa para 15/17-17/17 e prevalecente sobre redações anteriores
      conflitantes. §18.1 define nominalmente quatro fenômenos
      independentes (quebra textual por largura, fragmentação vertical,
      página somente de continuação, conjunto vazio) com prova mínima
      distinta para cada um. §18.2 especifica um harness adaptativo,
      separado do comportamento de produto, que obtém W/C pela mesma
      autoridade geométrica do renderer (D-TEC-04), sem duplicar fórmulas,
      e delimita o que uma fixture estática pode/não pode provar sozinha.
      §18.3 fixa relações derivadas (W, C) em vez de números absolutos
      para cada fenômeno, proibindo explicitamente fixar "31 linhas"/"16
      linhas por página" como critério geral. §18.4 define seis casos de
      validação separados (H0045-VAL-LARGURA/PERMITIR/EVITAR/CONDICIONAL/
      CONTINUACAO/VAZIO), proibindo que um único caso prove mais de um
      fenômeno. §18.5 exige geometrias múltiplas (regular, estreita, alta,
      redimensionamento) e PTY pelo ponto de entrada real, adicionalmente
      a §11. §18.6 preserva 6/17-14/17 e reespecifica 15/17-17/17 usando os
      casos de §18.4, com gabarito curto
      APROVADO/REPROVADO/NÃO OBSERVADO. §18.7 autoriza arquivos futuros
      (demo/demo.py, demo/teste_demo_paginacao.py,
      tela/teste_paginacao.py, tela/teste_renderizador.py e as três
      fixtures existentes ajustáveis) e resolve o caminho nominal canônico
      do helper novo — demo/casos_validacao_paginacao.py — coerente com o
      padrão já usado por demo/diagnostico.py e
      demo/executor_sintetico.py; distingue fixture estática, modelo de
      validação em memória, estado de runtime, comportamento de produto,
      teste automatizado e validação humana. §18.8 acrescenta dez
      critérios de aceite de método (CA-H0045-PH-01..10). Adicionalmente,
      corrigida a única ocorrência normativa de "exatamente 3 páginas" na
      finalidade da fixture `h0045_paginacao_console_unico.json` (§6.1) e
      marcados como exemplo de geometria controlada, não critério
      universal, os trechos de §12 que descreviam saída/prova semântica
      apenas em termos de "80x24"; §12 ganhou bloco
      `validacao_manual.estado_consolidado` apontando 15/17-17/17 para §18.6.
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
    delta: >
      Correção de método (não de arquitetura de produto): nova §18 (oito
      subseções); ajuste pontual em §6.1 e §12. Nenhuma ADR, contrato,
      nomenclatura, código, teste ou fixture alterados. D-PAG-01..14,
      D-TEC-01..17 e as 27 linhas de §9 (Critérios de aceite) permanecem
      intactas.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git branch --show-current; git rev-parse HEAD; git status --short --untracked-files=all; git diff --cached --name-only"
    resultado_compacto: "master; HEAD b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; baseline conforme transportado; worktree acumulado H-0045/P01-P11 preservado sem limpeza"
  - comando_ou_metodo: "git diff --check -- docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P02.md"
    resultado_compacto: "sem problemas de whitespace (arquivos não rastreados; sem diff contra índice)"
  - comando_ou_metodo: "rg -n 'exatamente 3 páginas|exatamente 6 páginas|capacidade.*16|16 linhas|quadros 80x24|somente 80x24|6/17\\.\\.17/17' docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md"
    resultado_compacto: "uma ocorrência remanescente ('16 linhas por página'), dentro de frase que proíbe explicitamente fixá-la como critério geral (§18.3) — marcação exemplificativa aceita pelo critério do prompt"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
