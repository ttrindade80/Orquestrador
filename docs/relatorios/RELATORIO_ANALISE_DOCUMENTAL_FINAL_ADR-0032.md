---
name: REL-ADF-0032-templates-canonicos
description: "Análise documental final do ciclo ADR-0032 antes do fechamento manual"
metadata:
  type: relatorio_analise_documental_final
  etapa: ANALISE_DOCUMENTAL_FINAL
  status: "DOCUMENTATION_FINAL_APPROVED"
  data: 2026-07-26
rastreabilidade:
  ciclo: ADR-0032
  adr_relacionadas:
    - docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  handoffs_relacionados: []
  relatorios_materiais:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_TEMPLATES_RELATORIOS.md
    - docs/relatorios/RELATORIO_CRIACAO_ADR-0032.md
    - docs/relatorios/RELATORIO_QA_ADR-0032.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0032.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0032.md
---

# REL-ADF-0032 — Análise documental final

## 1. Objeto e status

```yaml
ciclo: ADR-0032 — uso obrigatório de templates canônicos
status_literal: DOCUMENTATION_FINAL_APPROVED
```

## 2. Verificações finais

```yaml
verificacoes:
  - item_material: status da ADR-0032
    metodo_ou_origem: leitura integral do arquivo
    resultado: OK
  - item_material: caminho antigo do índice ausente
    metodo_ou_origem: test -e no caminho antigo
    resultado: OK
  - item_material: referência normativa ativa ao caminho antigo
    metodo_ou_origem: rg fora de docs/relatorios e do próprio ADR
    resultado: OK
  - item_material: cinco roteadores apontando ao índice vigente
    metodo_ou_origem: rg pelo caminho novo nos cinco arquivos
    resultado: OK
  - item_material: presença dos 14 templates e do índice
    metodo_ou_origem: loop de test -f sobre a lista fechada
    resultado: OK
  - item_material: regra ativa de adaptação por proximidade
    metodo_ou_origem: rg por padrões de proximidade/matriz/REL-DOC-NNNN
    resultado: OK
  - item_material: README de relatórios sem REL-DOC-NNNN
    metodo_ou_origem: leitura integral do arquivo
    resultado: OK
  - item_material: exclusão do relatório externo do gerente
    metodo_ou_origem: leitura integral da ADR e do README de relatórios
    resultado: OK
  - item_material: ausência de migração retroativa determinada
    metodo_ou_origem: leitura integral da ADR (§4 "Não retroatividade")
    resultado: OK
  - item_material: ausência de handoff/implementação para o ciclo
    metodo_ou_origem: git status e leitura de docs/handoff/README.md
    resultado: OK
  - item_material: worktree corresponde aos artefatos acumulados
    metodo_ou_origem: git status --short --untracked-files=all
    resultado: OK
  - item_material: ausência de problema de whitespace
    metodo_ou_origem: git diff --check
    resultado: OK
```

## 3. Pendências e achados

```yaml
achados: []
pendencias_nao_bloqueantes:
  - nota_processual (DESVIO_SEM_IMPACTO_MATERIAL) transportada do QA de
    aplicação: consulta adicional por listagem de diretório durante a
    aplicação; sem exigência de patch, sem nova evidência material que a
    reclassifique.
bloqueios: []
```

A única ocorrência do padrão `REL-DOC-NNNN` fora de `docs/relatorios/` está no
§2 "Contexto" da própria ADR-0032, narrando o estado legado que a decisão
substitui — não é regra ativa.

## 4. Estado para fechamento

```yaml
pronto_para_fechamento_manual: true
validacao_manual:
  necessaria: false
  resultado: não aplicável — ciclo puramente documental
workspace_compacto:
  branch: master
  HEAD: 13d743d
  staged: nenhum
  unstaged: 12 modificados (5 roteadores/autoridade + 7 templates canônicos preexistentes)
  nao_rastreados: 15 (ADR-0032, índice renomeado, 7 templates novos, 6 relatórios de evidência do ciclo)
```
