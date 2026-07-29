---
name: REL-PATCH-0036-P01-envelope-json-console
description: "Especialização focal de contrato_json_console.md §14.5-14.6 propagando D-H3-10 a D-H3-15a"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_PATCHED
  data: 2026-07-29
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: docs/contratos/contrato_json_console.md
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0036.md
  achados_tratados:
    - QA-APLICACAO-ADR0036-001
---

# REL-PATCH-0036-P01 — Especialização focal do envelope em `contrato_json_console.md`

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_APLICACAO_ADR
status_literal: ADR_APPLICATION_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0036.md
achados_tratados:
  - QA-APLICACAO-ADR0036-001
achados_resolvidos:
  - QA-APLICACAO-ADR0036-001
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-APLICACAO-ADR0036-001
    alteracao: seções 14.5.1 e 14.6.1 a 14.6.6 acrescentadas, sem renumerar 14.7 a 14.12
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/contratos/contrato_json_console.md
    delta: >
      §14.5.1 — documento válido com status_semantico falha e código 0
      permanece apresentação direta (D-H3-10). §14.6.1 — status: falha
      único e os cinco diagnósticos canônicos (D-H3-11, D-H3-12). §14.6.2 —
      código 130 como regra normativa do envelope de interrupção (D-H3-11;
      H2-ESP-18). §14.6.3 — obrigatoriedade, ordem fixa e não omissão dos
      seis campos (D-H3-15a). §14.6.4 — stdout/stderr obrigatórios, vazios
      como indisponível (D-H3-14). §14.6.5 — resultado_json obrigatório,
      null como indisponível, preservação literal (D-H3-15). §14.6.6 —
      ausência de estilo especial e de cor_alerta (D-H3-13).
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: git diff --check
    resultado_compacto: sem erros de espaço em branco
  - comando_ou_metodo: leitura focal de H2-ESP-18 (ADR-0035) e §6.5.6/6.5.7 (H-0042)
    resultado_compacto: código 130 e preservação do JSON pré-interrupção já fixados por H-0042; apenas ausentes como regra do envelope em §14.6
  - comando_ou_metodo: sha256sum de ADR-0036, RELATORIO_APLICACAO_ADR-0036.md e RELATORIO_QA_APLICACAO_ADR-0036.md antes/depois
    resultado_compacto: hashes idênticos — autoridades intactas
  - comando_ou_metodo: git status/diff --cached pós-edição
    resultado_compacto: stage vazio; único arquivo tocado foi contrato_json_console.md
```

Verificação local não equivale a QA independente.

## 5. Preservações

`selecao_execucao.v1` (§14.2) intacto. §14.11 (fronteira Handoff 3/4)
semanticamente intacta, nenhuma linha alterada. Protocolo e executor do
`H-0042` preservados, sem alteração de código, teste, fixture ou
configuração. Nenhum outro contrato, nomenclatura, ADR, handoff, índice ou
backlog tocado. `cor_alerta` declarada `nao_utilizada`, sem cor concreta
nem alteração de `config/estilo.json`.

## 6. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas: []
```
