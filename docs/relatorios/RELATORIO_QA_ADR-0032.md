---
name: relatorio-qa-adr-0032
description: QA documental independente da ADR-0032 (templates canônicos)
metadata:
  type: relatorio
  scope: qa-adr
---

# Relatório — QA da ADR-0032

Este QA ocorre antes da entrada em vigor da obrigação de templates; não declara
conformidade com o pacote ainda não aplicado.

```yaml
rastreabilidade:
  etapa: QA_ADR
  objeto: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  relatorio_autoria: docs/relatorios/RELATORIO_CRIACAO_ADR-0032.md

execucao:
  status: ADR_APPROVED
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_ADR-0032.md
  arquivos_alterados: []
  bloqueios: []
```

## Veredito

`ADR_APPROVED`. Sem achados materiais. A ADR materializa D-TPL-CICLO-01,
D-TPL-README-01 e D-TPL-01 a D-TPL-07 sem alteração de sentido; não inventa
política, exceção, artefato ou etapa; distingue depósito, adoção na aplicação
e vigência só após `QA_APLICACAO_ADR`; exclui o relatório externo do gerente;
preserva histórico; delimita candidatos de aplicação; fecha o ciclo
documental sem handoff/implementação.

## Verificações materiais

- Hashes SHA-256 dos 15 arquivos do pacote idênticos ao baseline do prompt e
  ao relatório de criação.
- Worktree: além do baseline pré-ADR (templates + levantamento), a criação
  acrescentou somente a ADR-0032 e `RELATORIO_CRIACAO_ADR-0032.md`.
- Índice ainda no nome pré-renomeação; README legado intacto; status
  `proposta`; pacote depositado, não exigível.
