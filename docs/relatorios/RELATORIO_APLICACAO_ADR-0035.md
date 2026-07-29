---
name: REL-ALT-0035-aplicacao-adr-0035
description: "Aplicação documental da ADR-0035 — protocolo focal de execução sintética reversível"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED
  data: 2026-07-29
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0035
  artefato_principal: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  autoridade_principal: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  cadeia_raiz: ITEM-0006
  predecessor_imediato: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  achados_tratados: []
---

# REL-ALT-0035 — Aplicação documental da ADR-0035

> Relatório sucinto, factual, assertivo e autocontido.
>
> Teto normal: 600 palavras. Este relatório registra execução; não declara aprovação.

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0035
status_literal: ADR_APPLICATION_COMPLETED
continuidade: >
  primeira tentativa bloqueada por caminho incorreto de template no prompt
  do gerente (TEMPLATE_RELATORIO_APLICACAO_ADR.md); nenhuma alteração
  normativa ocorreu antes desta continuidade; template correto:
  TEMPLATE_RELATORIO_APLICACAO_ALTERACAO.md
```

## 2. Delta material

```yaml
delta_material:
  - ADR-0035 marcada como aceita e aplicada; relações documentais registradas
  - INDICE_ADR registra ADR-0035 (ITEM-0006; especialização do Handoff 2 da ADR-0034)
  - contrato_console §23.6 recebe fronteira comportamental do Handoff 2
  - contrato_json_console §14 especializa entrada, CLI, fixture, temporários,
    documento de sucesso, status/código, canais e controles sintéticos;
    §14.3 e §14.6 preservados
  - ITEM-0006 atualizado sem conclusão; próxima capacidade = criar Handoff 2
delta_nomenclatura:
  modulos_alterados: []
  termos_criados: []
  termos_alterados: []
  aliases_ou_historicos: []
```

Compatibilidade preservada: ADR-0035 especializa sem substituir a ADR-0034;
D-SEL-01 a D-SEL-10 inalterados; CLI provisória com os mesmos argumentos;
envelope de erro multinível inalterado; documento de sucesso = uso concreto
do schema multinível vigente; binding definitivo pode substituir o protocolo
demonstrativo sem reabrir a seleção múltipla; Handoff 3 consumirá o
documento/envelopes; Handoff 4 fará a integração.

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0035.md
    finalidade: relatório desta aplicação
arquivos_alterados:
  - caminho: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
    delta: status aceita e aplicada; relações e critérios de aplicação
  - caminho: docs/adr/INDICE_ADR.md
    delta: entrada ADR-0035
  - caminho: docs/contratos/contrato_console.md
    delta: §23.6 fronteira Handoff 2; remissão ADR-0035
  - caminho: docs/contratos/contrato_json_console.md
    delta: especialização §14 (H2-ESP)
  - caminho: docs/backlog.md
    delta: estado material do ITEM-0006
arquivos_removidos: []
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: gate Git pré-aplicação e pós-bloqueio
    resultado_compacto: master @ f4b5df1; stage vazio; baseline acumulada esperada
    prova_semantica: sem alteração normativa na tentativa bloqueada
  - comando_ou_metodo: git diff --check nos artefatos autorizados
    resultado_compacto: sem problemas de whitespace
    prova_semantica: arquivos focais limpos
  - comando_ou_metodo: git status --short --untracked-files=all
    resultado_compacto: somente artefatos autorizados + QA prévio intacto
    prova_semantica: stage vazio; sem arquivo fora da lista
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - QA da aplicação, handoff, código, fixtures, testes e Git de escrita fora deste prompt
```
