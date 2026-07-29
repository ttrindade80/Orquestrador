---
name: REL-ALT-0036-aplicacao-adr-0036
description: "Aplicação documental da ADR-0036 aos contratos, índice de ADRs, backlog e módulos de nomenclatura afetados"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED
  data: 2026-07-29
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  artefato_principal: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  autoridade_principal: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_ADR-0036.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0036_P01.md
  achados_tratados: []
---

# REL-ALT-0036 — Aplicação da ADR-0036

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: ADR-0036 (aceita; QA_POS_PATCH ADR_APPROVED)
status_literal: ADR_APPLICATION_COMPLETED
```

## 2. Delta material

```yaml
delta_material:
  - contrato_tela_json.md §34: novas §34.7 (identidade concreta resultado_execucao/console_resultado, ciclo de carregamento D-H3-09) e §34.8 (supersessão H3/H4, D-H3-19)
  - contrato_composicao_corpo.md §3.1.1: id concreto console_resultado, arranjo vertical explícito, fronteira H3/H4 atualizada
  - contrato_barra_de_menus.md §23: nova §23.4 (instância concreta Esc/Voltar da tela de resultado); remissões renumeradas para §23.5
  - contrato_console.md §23.6/23.7: fronteira comportamental do Handoff 3 (carregamento, escolha documento/envelope) e atualização das fronteiras aplicadas conforme D-H3-19
  - contrato_json_console.md §14.11: divisão H3/H4 corrigida — supersede a atribuição original de abertura/retorno ao Handoff 3
  - INDICE_ADR.md: linha ADR-0036 adicionada após ADR-0035
  - backlog.md ITEM-0006: pré-requisitos e próxima ação atualizados; H-0043 indicado como não criado
delta_nomenclatura:
  modulos_alterados: []
  termos_criados: []
  termos_alterados: []
  aliases_ou_historicos: []
```

Não descreve passo a passo. Não copia conteúdo integral da ADR nem dos contratos.

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md
    finalidade: registrar a aplicação documental desta etapa
arquivos_alterados:
  - caminho: docs/contratos/contrato_tela_json.md
    delta: frontmatter (ADR-0036 em adrs_aplicadas); §34.7 e §34.8 novas
  - caminho: docs/contratos/contrato_composicao_corpo.md
    delta: frontmatter; §3.1.1 com identidade concreta e fronteira H3/H4 atualizada
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: frontmatter; nova §23.4, remissões renumeradas para §23.5
  - caminho: docs/contratos/contrato_console.md
    delta: frontmatter; §23.6 ampliada, §23.7 e §23.8 atualizadas
  - caminho: docs/contratos/contrato_json_console.md
    delta: frontmatter; §14.11 corrigida (divisão H3/H4), §14.12 ampliada
  - caminho: docs/adr/INDICE_ADR.md
    delta: linha ADR-0036 adicionada
  - caminho: docs/backlog.md
    delta: ITEM-0006 — pré-requisitos e próxima ação atualizados
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: leitura integral do manifesto (ADR-0036, QA raiz, QA pós-patch, template, índice, backlog, 5 contratos, 6 módulos de nomenclatura)
    resultado_compacto: leitura completa; nenhum conflito material encontrado
    prova_semantica: decisões D-H3-01 a D-H3-19 propagadas sem reabrir D-SEL-01 a D-SEL-10 nem redefinir ADR-0035/H-0042
  - comando_ou_metodo: avaliação dos módulos 42 e 43 quanto a termos novos (exigência explícita da ADR §5)
    resultado_compacto: termos já vigentes (§4.5 de ambos) cobrem os conceitos de D-H3-09/D-H3-15a por especialização; nenhum termo novo necessário
    prova_semantica: proibição de criar termo quando especialização de termo vigente basta (seção "Módulos de nomenclatura")
  - comando_ou_metodo: git status/diff --check pós-edição
    resultado_compacto: somente arquivos autorizados alterados; stage vazio; QA reports intactos
    prova_semantica: ver seção 6 do prompt (verificações finais) executada nesta etapa
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - Módulos de nomenclatura 20, 31, 32, 44 foram lidos e permanecem intactos: as decisões da ADR-0036 já são cobertas por especializações de termos vigentes (tela de resultado, documento de resultado, envelope de erro, carregamento) sem exigir termo novo.
  - A renumeração de §23.4→§23.5 em contrato_barra_de_menus.md e a expansão de §23.6/23.7 em contrato_console.md ocorreram somente dentro dos próprios arquivos, sem remissão externa quebrada identificada na leitura focal.
```

## 6. Evidências separadas

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_QA_ADR-0036.md
    finalidade: auditoria raiz (ADR_REJECTED, achados QA-ADR0036-001/002)
    leitura_necessaria_para: []
  - arquivo: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0036_P01.md
    finalidade: reteste do patch P01 (ADR_APPROVED)
    leitura_necessaria_para: []
```
