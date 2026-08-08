---
name: RELATORIO_QA_POS_PATCH_HANDOFF_H-0052_P01
description: "Reteste independente do patch P01 do handoff H-0052"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH_HANDOFF
  camada_auditada: HANDOFF
  status: H1_HANDOFF_APPROVED
  data: 2026-08-08
rastreabilidade:
  handoff: docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
  qa_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0052.md
  patch: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0052_P01.md
---

# QA pós-patch — H-0052 P01

## Resultado

```yaml
status: H1_HANDOFF_APPROVED
handoff: H-0052
patch: P01
achados_retestados:
  - H-0052-A
  - H-0052-B
  - H-0052-C
achados_pendentes: []
novos_achados: []
```

## Reteste focal

- **H-0052-A — RESOLVIDO.** §7.1 restringe o fallback a `politica_navegacao`
  `dict` sem a chave `tipo` ([linhas 195–206](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L195-L206)). A forma não-objeto não é normalizada, o valor presente é transportado literalmente e os casos NAO_OBJETO e a rejeição estrutural de carga estão previstos nos itens 2 e 5 de §11 ([linhas 440–454](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L440-L454)). Não restou autorização de fallback amplo.
- **H-0052-B — RESOLVIDO.** §7.3 torna obrigatória a validação no carregamento,
  fecha os cinco literais e exige `TelaEstruturaInvalida` para desconhecidos e
  formas incompatíveis, sem alias, coerção ou conversão ([linhas 262–292](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L262-L292)). §11 cobre aceitação dos cinco valores, desconhecido e não textual ([linhas 457–466](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L457-L466)).
- **H-0052-C — RESOLVIDO.** O critério não depende mais da lista de foco: §7.2
  exige no-op em chamada direta dos quatro `mover_*`, autoriza alteração focal
  em `tela/navegacao.py` e preserva `nivel_unico`, seleção e paginação ([linhas 239–260](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L239-L260)). O teste direto obrigatório está explícito no item 13 de §11 ([linhas 473–478](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L473-L478)).

## Preservações

QH52-CRIT-03 permanece como inércia técnica limitada: os três literais futuros
são aceitos e transportados, mas permanecem não focalizáveis e sem dispatch
antecipado ([linhas 81–91](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L81-L91)). QH52-CRIT-04 permanece usando `TelaEstruturaInvalida` em `_validar_valores_envelope_pre_adr_0028`, sem segunda camada ([linhas 262–272](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L262-L272)). `nivel_unico`, compatibilidade, escopo nominal e paginação continuam protegidos pelos critérios de aceite ([linhas 578–610](../../handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md#L578-L610)).

As formulações condicionais do caso não textual apenas delimitam a aplicação
direta do teste; não relaxam a obrigação normativa de §7.3. Não foi identificada
regressão material, nova decisão ou ampliação de escopo introduzida por P01.

## Método e integridade

Auditoria documental semântica/normativa do handoff pós-P01, do relatório de
patch e do QA de origem, com conferência focal dos proprietários indicados em
`tela/navegacao.py`, `tela/carregamento/envelope_pre_adr_0028.py`, dos contratos
e da ADR-0042. Nenhum código, teste, fixture, handoff, contrato, ADR,
nomenclatura ou backlog foi alterado nesta etapa. A implementação continua
`NAO_INICIADA`; portanto, a suíte de runtime permanece critério da etapa de
implementação, não evidência necessária deste QA do handoff.

```yaml
proxima_acao: PATCH_IMPLEMENTACAO
```
