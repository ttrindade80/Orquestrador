---
name: REL-PATCH-0038-P01-correcao-politicas-quebra
description: "Delta factual do patch que corrige, em contrato_console.md §12, a redação das três políticas de quebra de página (evitar_quebra, permitir_quebra, permitir_quebra_somente_se_maior_que_pagina), eliminando a equivalência textual entre evitar_quebra e permitir_quebra_somente_se_maior_que_pagina"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_PATCHED
  data: 2026-08-02
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ADR-0038
  cadeia_raiz: ADR-0038
  predecessor_imediato: docs/relatorios/RELATORIO_APLICACAO_ADR-0038.md
  achados_tratados: []
---

# REL-PATCH-0038-P01 — Correção das políticas de quebra em `contrato_console.md`

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_APLICACAO_ADR
status_literal: ADR_APPLICATION_PATCHED
```

## 2. Cadeia

```yaml
raiz: ADR-0038
predecessor_imediato: docs/relatorios/RELATORIO_APLICACAO_ADR-0038.md
achados_tratados: []
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - alteracao: reescrita da tabela de política de quebra de página (§12) e
    acréscimo de parágrafo de distinção explícita
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/contratos/contrato_console.md
    delta: |
      §12 — tabela de `politica_quebra` reescrita para as três políticas com
      comportamento próprio e distinto:
      - `permitir_quebra`: fluxo contínuo — começa na próxima linha
        disponível, usa o espaço restante da página atual (inclusive a
        última linha) e continua nas páginas seguintes;
      - `evitar_quebra`: sempre começa em página nova, mesmo havendo espaço
        na página anterior; item maior que uma página continua nas páginas
        seguintes; o próximo item com a mesma política também espera página
        nova;
      - `permitir_quebra_somente_se_maior_que_pagina`: mantém junto quando
        possível — permanece na página atual se couber inteiro no espaço
        restante; se não couber mas couber inteiro em página vazia, começa
        inteiro na próxima; se maior que uma página inteira, começa na
        primeira linha útil da página seguinte e continua.
      Acrescentado parágrafo explícito distinguindo `evitar_quebra` de
      `permitir_quebra_somente_se_maior_que_pagina`, eliminando a
      equivalência textual registrada como ambiguidade em
      `H-0045` §6.4 e D-TEC-07.
      Nenhum campo, enum, schema, nome de política, regra de cursor,
      seleção, foco, navegação ou redimensionamento foi alterado.
      `metadata.versao` avançada de "0.1" para "0.2", seguindo o padrão já
      usado em `contrato_barra_de_menus.md`.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: leitura integral de ADR-0038, contrato_console.md e
      leitura focal de D-TEC-07, §6.4 e CA-H0045-06/07/08 em H-0045
    resultado_compacto: "os três nomes técnicos permanecem; cada política tem
      descrição própria; permitir_quebra usa espaço imediato disponível;
      evitar_quebra sempre inicia página nova; permitir_quebra_somente_se_
      maior_que_pagina mantém junto quando cabe; item maior que uma página
      tratado nas três políticas conforme aplicável; nenhuma regra de
      cursor/seleção/foco/navegação/redimensionamento tocada"
  - comando_ou_metodo: "git diff --check -- docs/contratos/contrato_console.md"
    resultado_compacto: "sem erros (exit 0)"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
