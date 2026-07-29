---
name: REL-QA-POS-PATCH-APLICACAO-ADR-0036-P01
description: "Reteste independente do P01 da aplicação da ADR-0036"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: APLICACAO_ADR
  patch: P01
  status: ADR_APPLICATION_APPROVED
  data: 2026-07-29
rastreabilidade:
  aplicacao_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md
  qa_raiz: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0036.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0036_P01.md
  achados_tratados:
    - QA-APLICACAO-ADR0036-001
---

# REL-QA-POS-PATCH-APLICACAO-ADR-0036-P01 — Reteste do P01

## Identificação e status

```yaml
etapa_qa: QA_POS_PATCH
camada_auditada: APLICACAO_ADR
patch: P01
objeto_auditado: docs/contratos/contrato_json_console.md
status: ADR_APPLICATION_APPROVED
```

## Escopo focal e resultado

`QA-APLICACAO-ADR0036-001`: **RESOLVIDO**. As §§14.5.1 e 14.6.1–14.6.6 passam a declarar apresentação direta somente com código `0` e documento sintática e semanticamente válido — inclusive `status_semantico: falha` — e envelope para código não zero, ausência, malformação ou invalidade semântica. Código não zero preserva o texto bruto em `resultado_json`.

O envelope é multinível, `conjuntos_campos`, com seis campos obrigatórios em ordem fixa, sem omissão, intercalação ou reordenação. `status` é sempre `falha`; os cinco diagnósticos canônicos são do Orquestrador, separados de `stdout`/`stderr`. Interrupção fixa código `130`, diagnóstico canônico e envelope, preservando o resultado prévio literalmente. Canais vazios e `resultado_json: null` exibem `indisponível`; conteúdo presente preserva texto bruto exato, sem correção, normalização, reserialização ou inferência. Não há cor, moldura ou estilo especial.

## Regressões e preservações

```yaml
novos_achados: nenhuma
preservacoes_verificadas:
  - selecao_execucao.v1, classificação por código e dry-run/execução real
  - canais separados e preservação do H-0042
  - apresentações permitidas, §14.11 e fronteira Handoff 3/Handoff 4
  - ADRs, backlog, índice, estilo, código, testes, fixtures e handoffs sem delta declarado pelo P01
```

## Integridade e conclusão

```yaml
hashes_antes:
  contrato: 6032aca357a0818aa9bb726a62b88a7e1c52a1c7af148446200a37d1d7eb9648
  qa_raiz: 75d088c9f79c72397c74ce09383a9776c892c0e2726c268c8b6aef195173b02d
  relatorio_patch: 61568116308c5a0930c7151fdcf4d202e10a274bfef8e080d13f9a6b6541591d
hashes_depois:
  contrato: 6032aca357a0818aa9bb726a62b88a7e1c52a1c7af148446200a37d1d7eb9648
  qa_raiz: 75d088c9f79c72397c74ce09383a9776c892c0e2726c268c8b6aef195173b02d
  relatorio_patch: 61568116308c5a0930c7151fdcf4d202e10a274bfef8e080d13f9a6b6541591d
estado_git_inicial:
  branch: master
  HEAD: 6ecc4cd
  stage: vazio
  observacao: alteracoes e nao-rastreados preexistentes foram preservados; somente este relatorio foi criado nesta etapa.
H-0043: inexistente
```

Conclusão: `ADR_APPLICATION_APPROVED`; o achado foi resolvido e não há regressão material diretamente causada pelo P01.
