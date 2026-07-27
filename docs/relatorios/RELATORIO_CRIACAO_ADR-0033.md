---
name: REL-CRIACAO-0033-adr-separacao-backlog-historico-arquivo
description: Resultado factual da criação da ADR-0033 (separação entre backlog, histórico e arquivo documental)
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_ADR
  status: ADR_CREATED
  data: 2026-07-27
rastreabilidade:
  etapa: CRIAR_ADR
  objeto: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
  artefato_principal: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
  autoridade_principal: null
  decisoes_materializadas:
    - D-HIST-01
    - D-HIST-02
    - D-HIST-03
    - D-HIST-04
    - D-HIST-05
    - D-HIST-06
    - D-HIST-07
    - D-HIST-08
    - D-HIST-09
    - D-HIST-10
    - D-HIST-11
    - D-HIST-12
    - D-HIST-13
    - D-HIST-14
---

# REL-CRIACAO-0033 — Criação documental

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_ADR
artefato_criado: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
status_literal: aceita
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - caminho_ou_decisao: docs/backlog.md
  - caminho_ou_decisao: docs/build_docs/instruction.md
  - caminho_ou_decisao: docs/build_docs/prompts.md
  - caminho_ou_decisao: docs/build_docs/to_do.md
  - caminho_ou_decisao: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  - caminho_ou_decisao: docs/INDICE.md
decisoes_materializadas:
  - id: D-HIST-01
    sintese: separação de responsabilidades entre backlog ativo, histórico compacto e arquivo documental; ADR/handoff/contrato/relatório/commit continuam autoridade e evidência detalhada
  - id: D-HIST-02
    sintese: estados permitidos no backlog restritos a planejado, bloqueado, em_andamento, pronto_para_handoff
  - id: D-HIST-03
    sintese: no fechamento, item sai do backlog e entra no histórico com um dos quatro resultados de encerramento
  - id: D-HIST-04
    sintese: caminho canônico inicial docs/HISTORICO.md, ao lado de docs/backlog.md; estrutura maior fica para decisão futura
  - id: D-HIST-05
    sintese: estrutura de docs/HISTORICO.md em quatro seções, ordenação crescente por identificador, formato mínimo sem inventar dado ausente
  - id: D-HIST-06
    sintese: docs/arquivo/ como área canônica de obsoletos, preservando estrutura de origem, com README declarando ausência de autoridade vigente
  - id: D-HIST-07
    sintese: aviso literal obrigatório no início de todo arquivo movido para docs/arquivo/
  - id: D-HIST-08
    sintese: migração nominal dos três arquivos de docs/build_docs/ para docs/arquivo/build_docs/; pasta deixa de ser ativa
  - id: D-HIST-09
    sintese: itens concluido do to_do.md legado (incl. DOC-0019, DOC-0022) aceitos como realizados e registrados compactamente
  - id: D-HIST-10
    sintese: DOC-B003, DOC-B004, DOC-B007, DOC-B008, DOC-B009 registrados como CANCELADO com motivos compactos definidos
  - id: D-HIST-11
    sintese: criação de ITEM-0015, ITEM-0016, ITEM-0017 no backlog, todos bloqueado, sem campo de origem legada
  - id: D-HIST-12
    sintese: fechamento do ITEM-0002 como CONCLUIDO com dados comprovados de ADR-0031/H-0040/commit
  - id: D-HIST-13
    sintese: ITEM-0003 a ITEM-0014 permanecem no backlog, sujeitos só à nova taxonomia de estados, sem reescrita por inferência
  - id: D-HIST-14
    sintese: docs/INDICE.md deve identificar as três novas funções documentais
```

## 3. Delta documental

```yaml
delta_material:
  - ADR-0033 registra a separação entre docs/backlog.md, docs/HISTORICO.md e docs/arquivo/, sem executar a migração
  - taxonomia de estados de backlog e de resultados de histórico formalizada
  - migração nominal inicial (três arquivos de docs/build_docs/) e fechamento do ITEM-0002 registrados como decisão fechada, pendentes de aplicação
arquivos_criados:
  - docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo: leitura integral de docs/templates/TEMPLATE_ADR.md e docs/templates/TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md
    resultado_compacto: ambos usados sem adaptação; nenhuma seção do template de ADR omitida
  - comando_ou_metodo: ls docs/adr/ e ls docs/relatorios/
    resultado_compacto: ADR-0033 é numeração inédita; nenhum arquivo inesperado além dos 4 relatórios já sinalizados como esperados pelo prompt
  - comando_ou_metodo: git diff --check -- docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md docs/relatorios/RELATORIO_CRIACAO_ADR-0033.md
    resultado_compacto: sem problemas de espaço em branco ou marcador de conflito
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas:
  - "docs/adr/INDICE_ADR.md" instrui atualizar o índice ao criar ADR, mas o escopo fechado deste prompt restringe alteração a apenas dois arquivos; a atualização do índice (e de docs/backlog.md, docs/HISTORICO.md, docs/arquivo/, docs/INDICE.md) fica para a etapa de aplicação da ADR-0033.
```

## 6. Evidências separadas

Omitido — não aplicável.
