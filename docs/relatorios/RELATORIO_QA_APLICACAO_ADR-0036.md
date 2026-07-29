---
name: REL-QA-APLICACAO-ADR-0036
description: "Auditoria independente da aplicação documental da ADR-0036"
metadata:
  type: relatorio_qa
  etapa_qa: QA_APLICACAO_ADR
  camada_auditada: APLICACAO_ADR
  status: ADR_APPLICATION_REJECTED
  data: 2026-07-29
rastreabilidade:
  autorizacao_qa: QA_APLICACAO_ADR
  adr_auditada: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0036_P01.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_ADR-0036.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0036_P01.md
  achados_tratados: []
---

# REL-QA-APLICACAO-ADR-0036 — QA da aplicação documental

## 1. Identificação e status

```yaml
revisao: Aplicação documental da ADR-0036
etapa_qa: QA_APLICACAO_ADR
camada_auditada: APLICACAO_ADR
status_literal: ADR_APPLICATION_REJECTED
status_normalizado: ADR_APPLICATION_REJECTED
proxima_categoria: PATCH_APLICACAO_ADR
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
autoridades_materiais:
  - ADR-0036, D-H3-10 a D-H3-15a e D-H3-19
  - ADR-0034, D-SEL-16, D-SEL-17 e D-SEL-21
  - ADR-0035 e H-0042, classificação por código, resultado e interrupção
escopo:
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/adr/INDICE_ADR.md e docs/backlog.md
  - seis módulos autorizados de nomenclatura
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V-01
    comando_ou_metodo: leitura integral dos artefatos do manifesto e leitura focal das autoridades permitidas
    evidencia_focal: identidade, composição, carregamento único e supersessão H3/H4 propagados nos contratos aplicáveis
    resultado: OK
  - id: V-02
    comando_ou_metodo: comparação da seção 14 de contrato_json_console.md com D-H3-10 a D-H3-15a
    evidencia_focal: envelope não recebeu integralmente a especialização da ADR-0036
    resultado: FALHA
  - id: V-03
    comando_ou_metodo: git diff --check, diff focal, status e hashes antes da escrita
    evidencia_focal: stage vazio; nenhum código, teste, fixture, configuração ou handoff alterado; H-0043 inexistente
    resultado: OK
  - id: V-04
    comando_ou_metodo: análise dos módulos de nomenclatura 20, 31, 32, 42, 43 e 44
    evidencia_focal: conceitos já possuem proprietário; não há termo novo, contradição ou especialização terminológica necessária
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-APLICACAO-ADR0036-001 | material | Propagação integral de D-H3-10 a D-H3-15a no contrato proprietário do envelope | `contrato_json_console.md` §§14.5–14.6 preserva a escolha básica, os seis nomes e a preservação literal, mas não fixa `status: falha`, os cinco diagnósticos canônicos, `stdout`/`stderr` vazios como `indisponível`, obrigatoriedade e não omissão dos seis campos, ausência de estilo/`cor_alerta`, nem declara que documento semanticamente `falha` com código zero é direto. O código 130 aparece somente como controle sintético, não como regra do envelope. | A futura implementação não tem contrato completo e determinístico para materializar todos os envelopes exigidos pela ADR. | Especializar somente a seção 14 com essas regras normativas, preservando `selecao_execucao.v1` e o protocolo H2. |

```yaml
id: QA-APLICACAO-ADR0036-001
severidade: material
arquivo: docs/contratos/contrato_json_console.md
local: "§§14.5–14.6"
evidencia: "O delta alterou §14.11 para H3/H4, mas não materializou integralmente D-H3-10 a D-H3-15a."
regra_violada: "ADR-0036 exige critérios completos, estrutura normativa do envelope e apresentação sem estilo especial."
correcao_necessaria: "Patch focal em §14; sem ampliar protocolo, schema ou Handoff 2."
```

## 5. Estado Git e itens inesperados

```yaml
hashes_antes:
  adr: 27a5474e4c0c97bd80ae2d81e3939ff225535b94f6ad942c821206471f07d9b3
  relatorio_aplicacao: 214f5a13a2d91bc598be3b399bab43c79029de1873107e14c1dd66d53d013ced
  relatorio_qa_pos_patch: 7841a4e44d57306c99e86e318d78ff5daa1db2b5fdfc55c7889904022cc79b4c
stage: vazio
itens_inesperados:
  - item: docs/relatorios/RELATORIO_QA_ADR-0036.md
    origem: NAO_CONFIRMADA
    evidencia: "não rastreado no estado inicial, fora do estado transportado e não lido por vedação do manifesto"
```

## 6. Conclusão

`ADR_APPLICATION_REJECTED`: a aplicação preserva escopo, nomenclatura sem delta proprietário material, índice, backlog e a divisão H3/H4, mas requer `PATCH_APLICACAO_ADR` focal no contrato do envelope. Objetos auditados permaneceram intactos durante este QA.
