---
name: REL-QA-APP-0032-aplicacao-adr-0032
description: QA da aplicacao documental da ADR-0032
metadata:
  type: relatorio_qa
  etapa_qa: QA_APLICACAO_ADR
  camada_auditada: APLICACAO_ADR
  status: ADR_APPLICATION_APPROVED_WITH_NOTES
  data: 2026-07-26
rastreabilidade:
  adr_auditada: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0032.md
---

# REL-QA-APP-0032 - QA da aplicacao da ADR-0032

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
objeto_auditado: aplicacao documental da ADR-0032
```

Verificacoes materiais: ADR-0032 esta `aceita` e preserva as decisoes; o indice novo existe, o caminho antigo esta ausente e nao ha alias permanente; o indice, `docs/INDICE.md`, `docs/adr/INDICE_ADR.md`, `docs/handoff/README.md`, `docs/relatorios/README.md` e o contrato roteiam a obrigatoriedade, a resolucao previa pelo gerente, o bloqueio por ausencia/conflito, a nao retroatividade e a exclusao do relatorio externo do gerente. Os 14 hashes SHA-256 dos templates coincidem com o baseline aprovado. `git diff --check` nao apontou problemas.

Buscas autorizadas: referencias ao indice antigo remanescem em contexto historico da ADR e em relatorios do ciclo; a busca por regras conflitantes retornou apenas o contexto historico da propria ADR. Nao foi encontrada regra ativa permitindo template por proximidade nem matriz obrigatoria de criterios conformes.

```yaml
consulta_adicional:
  ocorreu: true
  comando_ou_escopo_confirmado: "listagem de diretorio declarada; comando exato nao confirmado"
  resultado_material: exemplos do contrato ajustados para a organizacao plana atual
  impacto_na_aplicacao: sem impacto material; estado auditavel sustenta a correcao focal
  classificacao: DESVIO_SEM_IMPACTO_MATERIAL
```

Achados materiais: nenhum.

Conclusao: aplicacao aprovada com nota processual, sem patch, handoff, implementacao ou etapa seguinte.
