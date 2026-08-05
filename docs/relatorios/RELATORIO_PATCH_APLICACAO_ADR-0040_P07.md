---
name: relatorio-patch-aplicacao-adr-0040-p07
description: "Relatório do patch de aplicação documental que propaga D-DRY-12 (rótulos visuais [Ins] Real/[Ins] Simulação) aos contratos e à nomenclatura da ADR-0040"
metadata:
  type: relatorio
  scope: orquestrador
---

# Relatório — Patch de Aplicação Documental ADR-0040 (P07)

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md

  origem_normativa_de_D-DRY-12:
    adr: docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
    qa: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0040_P04.md
    status: ADR_APPROVED_WITH_NOTES

  aplicacao_substantiva_anterior:
    patch: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md
    decisoes:
      - D-DRY-10
      - D-DRY-11

  regularizacao_da_aplicacao_anterior:
    patch: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P08.md
    qa: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0040_P08.md
    status: ADR_APPLICATION_APPROVED
    achados_abertos: []

  patch_desta_aplicacao:
    relatorio: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P07.md
    decisao:
      - D-DRY-12

decisao_aplicada:
  - D-DRY-12

numeracao:
  patch: P07
  motivo: >
    P06 já existia como registro substantivo da aplicação de
    D-DRY-10 e D-DRY-11 e foi preservado sem alteração.
```

A regularização P08 é posterior à execução material do P07, mas integra
a cadeia consolidada porque corrigiu e aprovou documentalmente a aplicação
substantiva anterior registrada no P06.

## 1. Escopo executado

Propagação incremental, exclusiva, de D-DRY-12 (reconciliação dos rótulos
visuais do controle universal `executar` → `[Ins] Real`, `dry_run` → `[Ins]
Simulação`, substituindo os rótulos `[Ins] Executar`/`[Ins] Dry-Run`
originalmente fixados por D-DRY-02) à base documental já aplicada e aprovada
da ADR-0040. D-DRY-01 a D-DRY-11 não foram reabertas; a aplicação original não
foi refeita.

## 2. Arquivos efetivamente alterados

- `docs/contratos/contrato_barra_de_menus.md` — §23.3.1 (título e corpo) e
  checklist da seção 20.
- `docs/contratos/contrato_chip.md` — §9.1 (corpo) e checklist da seção 17.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` — §4.4.3 (corpo).
- `docs/adr/INDICE_ADR.md` — descrição compacta da linha ADR-0040.

Sem delta material: `docs/contratos/contrato_tela_json.md` (schema já usa
exclusivamente `executar`/`dry_run`, sem menção aos rótulos visuais) e
`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` (já preserva a
separação entre configuração/runtime e apresentação sem citar rótulos).
Ambos permaneceram intactos por este patch.

`docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md` foi preservado
integralmente — não foi lido em profundidade nem alterado; apenas constatada
sua existência prévia e o conflito de numeração (seção 9).

## 3. Substituição aplicada e distinção modo/ação

Em todas as ocorrências do controle universal (ADR-0040), o rótulo textual
`[Ins] Executar`/`[Ins] Dry-Run` foi substituído por `[Ins] Real`/`[Ins]
Simulação`, com nota de histórico substituído por D-DRY-12. Foi inserida, em
`contrato_barra_de_menus.md` §23.3.1 e em `31_BARRA_DE_MENUS_E_CHIPS.md`
§4.4.3, a distinção obrigatória entre `[⏎] Executar` (ação que inicia o
processamento do lote) e `[Ins] Real`/`[Ins] Simulação` (modo da futura
execução) — eliminando a colisão lexical que motivou D-DRY-12.

## 4. Valores internos preservados

Nenhum arquivo passou a usar `real` ou `simulacao` como valor interno,
configuração ou schema. `executar` e `dry_run` permanecem os únicos valores
de `controle_execucao.modo_inicial` e do estado de runtime em todos os
arquivos tocados e não tocados.

## 5. Ocorrências antigas remanescentes e classificação

```yaml
ocorrencias_remanescentes:
  - arquivo: docs/adr/INDICE_ADR.md
    linha: 69
    classificacao: ESPECIALIZACAO_FOCAL_H0044
  - arquivo: docs/adr/INDICE_ADR.md
    linha: 72
    classificacao: HISTORICA_SUBSTITUIDA
  - arquivo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    linhas: [49, 113, 152, 209, 227]
    classificacao: ESPECIALIZACAO_FOCAL_H0044
  - arquivo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    linhas: [142, 143]
    classificacao: HISTORICA_SUBSTITUIDA
  - arquivo: docs/contratos/contrato_barra_de_menus.md
    linhas: [932, 935, 986]
    classificacao: ESPECIALIZACAO_FOCAL_H0044
  - arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 977
    classificacao: HISTORICA_SUBSTITUIDA
  - arquivo: docs/contratos/contrato_chip.md
    linhas: [323, 352]
    classificacao: ESPECIALIZACAO_FOCAL_H0044
  - arquivo: docs/contratos/contrato_chip.md
    linhas: [345, 346]
    classificacao: HISTORICA_SUBSTITUIDA
```

Nenhuma ocorrência foi classificada como `DEFEITO_REMANESCENTE`.

## 6. Preservação do H-0044

Todas as menções literais a `[Ins] Dry-Run` que restaram nos arquivos
alterados pertencem exclusivamente à especialização focal do Handoff 4
(ADR-0037/H-0044, §23.3 e §4.4.1) e não foram alteradas — nome, semântica,
tecla e regra de destaque permanecem idênticos. Nenhum arquivo de handoff,
implementação, teste ou configuração concreta foi lido ou tocado.

## 7. Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/adr/INDICE_ADR.md
  termos_adicionados: []
  termos_alterados:
    - de: "[Ins] Executar / [Ins] Dry-Run (rótulo do controle universal, ADR-0040)"
      para: "[Ins] Real / [Ins] Simulação (rótulo do controle universal, ADR-0040)"
  distincoes_adicionadas:
    - "[⏎] Executar (ação) × [Ins] Real / [Ins] Simulação (modo corrente)"
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

## 8. Verificações realizadas

- Busca restrita pós-alteração executada nos seis arquivos autorizados;
  todas as ocorrências remanescentes classificadas (seção 5).
- `git diff --check` sem apontamentos nos seis arquivos autorizados e neste
  relatório.
- Valores internos `executar`/`dry_run` conferidos como únicos em todos os
  trechos alterados; nenhum `real`/`simulacao` introduzido como valor de
  schema.
- `[⏎] Executar` permanece textualmente inalterado em todos os arquivos.
- `contrato_tela_json.md` e `nomenclatura/02` conferidos sem delta material
  necessário; permanecem no estado anterior a este patch (incluindo
  modificações prévias não relacionadas, já pendentes no repositório antes
  desta execução).
- Nenhum arquivo de contrato de console, backlog, handoff, código,
  configuração ou teste foi lido ou alterado.
- Nenhuma alteração foi staged ou commitada por este agente.

## 9. Conflito de numeração identificado e resolução

`docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md` já existia ao
início desta execução, documentando a aplicação de **D-DRY-10 e D-DRY-11**
(não D-DRY-12), com artefatos próprios (`contrato_registro_acoes.md`,
`contrato_console.md`, `contrato_json_console.md`, `backlog.md`, entre
outros) fora do escopo de leitura e alteração autorizado a este patch. Diante
do critério de aceite da ADR-0040 que veda sobrescrever relatório de execução
anterior, o conflito foi levado ao usuário, que confirmou: preservar o `P06`
existente sem alteração e registrar esta aplicação de D-DRY-12 sob o nome
`P07`. Nenhum conteúdo do `P06` foi lido em profundidade, reutilizado ou
incorporado.

## 10. Bloqueios

Nenhum.

## 11. Status

```yaml
status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P07.md
artefatos:
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/adr/INDICE_ADR.md
delta_terminologico:
  modulos_alterados:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/adr/INDICE_ADR.md
  termos_adicionados: []
  termos_alterados:
    - de: "[Ins] Executar / [Ins] Dry-Run (rótulo do controle universal, ADR-0040)"
      para: "[Ins] Real / [Ins] Simulação (rótulo do controle universal, ADR-0040)"
  distincoes_adicionadas:
    - "[⏎] Executar (ação) × [Ins] Real / [Ins] Simulação (modo corrente)"
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
proxima_acao: QA_POS_PATCH_APLICACAO_ADR
```
