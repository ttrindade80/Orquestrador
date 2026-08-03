---
name: REL-PATCH-H0045-P03-independencia-casos-e-gabarito-manual-unico
description: "Delta factual do patch P03 sobre o handoff H-0045: separa H0045-VAL-PERMITIR de H0045-VAL-CONTINUACAO e unifica o vocabulário de validação manual das etapas pendentes"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: "2026-08-01"
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0045_P02.md
  achados_tratados:
    - QA-H0045-P02-001
    - QA-H0045-P02-002
---

# REL-PATCH-H0045-P03 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0045_P02.md
achados_tratados:
  - QA-H0045-P02-001
  - QA-H0045-P02-002
achados_resolvidos:
  - QA-H0045-P02-001
  - QA-H0045-P02-002
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-H0045-P02-001
    alteracao: >
      §18.3 (dimensionamento): a bullet única "permitir_quebra com
      continuação pura" foi substituída por duas bullets nominais.
      H0045-VAL-PERMITIR passa a exigir apenas o mínimo suficiente para
      atravessar um limite de página (relação admissível: altura_do_item >
      capacidade_restante_da_pagina), sem fixar nem depender de 2C+1.
      H0045-VAL-CONTINUACAO passa a ser o único caso que exige 2C+1 (ou
      relação equivalente) e ganha marcadores próprios CONT_INICIO/
      CONT_MEIO/CONT_FIM. §18.4 (casos): acrescentado bloco
      `independencia` declarando explicitamente que H0045-VAL-PERMITIR não
      prova página somente de continuação e que H0045-VAL-CONTINUACAO não
      substitui a prova de permitir_quebra, com a regra de que os dois
      casos não compartilham entrada, marcadores, condição de aceite nem
      resultado manual. §18.6 (validação manual): a linha 15/17 foi
      restrita a provar apenas travessia de limite de página sob
      permitir_quebra, sem exigir página de continuação pura; a linha
      17/17 ganhou entrada própria e os marcadores CONT_INICIO/CONT_MEIO/
      CONT_FIM. §18.8 (critérios de aceite): acrescentado
      CA-H0045-PH-11, fixando a independência dos dois casos como critério
      de aceite do método. §18.5 (testes) e §18.1 (fenômenos) não exigiram
      alteração — não continham a conflação apontada.
  - id_achado: QA-H0045-P02-002
    alteracao: >
      §12 `validacao_manual`: a instrução operacional que pedia registro
      em passou/falhou/não se aplica foi removida. Acrescentados os campos
      `gabarito_manual` (APROVADO | REPROVADO | NÃO OBSERVADO) e
      `semantica_gabarito_manual` (definição operacional dos três valores,
      grafados sem underscore). A `observacao` foi reescrita para: (a)
      declarar explicitamente que 6/17..14/17 permanecem aprovadas e não
      devem ser reexecutadas nem reclassificadas; (b) remeter 15/17..17/17
      ao gabarito único acima e aos casos de §18.4/§18.6, sem reabrir
      etapas já aprovadas.
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
    delta: >
      Correção de método documental (não de arquitetura de produto):
      ajustes pontuais em §12 (`validacao_manual`) e §18.3/§18.4/§18.6/
      §18.8. Nenhuma ADR, contrato, nomenclatura, código, teste ou
      fixture alterados. D-PAG-01..14, D-TEC-01..17, §9 (critérios de
      aceite de implementação) e as seis causas PH-H0045-001..006
      resolvidas pelo P02 permanecem intactas.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git branch --show-current; git rev-parse HEAD; git status --short --untracked-files=all; git diff --cached --name-only"
    resultado_compacto: "master; HEAD b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; baseline conforme transportado; worktree acumulado H-0045/P01-P11 e patches de handoff P02 preservado sem limpeza"
  - comando_ou_metodo: "test -f docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P03.md (antes da criação)"
    resultado_compacto: "NAO_EXISTE — sem bloqueio de sobrescrita"
  - comando_ou_metodo: "git diff --check -- docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P03.md"
    resultado_compacto: "sem problemas de whitespace (arquivos não rastreados; sem diff contra índice)"
  - comando_ou_metodo: "rg -n 'H0045-VAL-PERMITIR|H0045-VAL-CONTINUACAO|2C \\+ 1|passou|falhou|não se aplica|APROVADO|REPROVADO|NÃO OBSERVADO' docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md"
    resultado_compacto: >
      vocabulário antigo (passou/falhou/não se aplica) ausente; 2C+1
      ocorre apenas no bloco de H0045-VAL-CONTINUACAO e em uma negação
      explícita dentro do bloco de H0045-VAL-PERMITIR ("não fixa nem
      depende de 2C+1"), confirmando a atribuição exclusiva exigida;
      APROVADO/REPROVADO/NÃO OBSERVADO presentes apenas como gabarito
      único, sem conflito.
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
