---
name: REL-PATCH-0041-P01-correcao-handoff-selecao-multipla
description: "Delta factual do patch documental do H-0041 (5 achados de QA_HANDOFF)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0041
  cadeia_raiz: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF.md
  achados_tratados:
    - H0041-QA-001
    - H0041-QA-002
    - H0041-QA-003
    - H0041-QA-004
    - H0041-QA-005
---

# REL-PATCH-0041-P01 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF.md
achados_tratados: [H0041-QA-001, H0041-QA-002, H0041-QA-003, H0041-QA-004, H0041-QA-005]
achados_resolvidos: [H0041-QA-001, H0041-QA-002, H0041-QA-003, H0041-QA-004, H0041-QA-005]
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: H0041-QA-001
    alteracao: >-
      Seção "3. Estado comprovado": removida a afirmação de que o backlog já
      registra a condição pós-aprovação; registrado que docs/backlog.md
      mantém redação anterior à aprovação (ITEM-0006 ainda condiciona a
      criação do handoff ao patch/QA pós-patch da aplicação) e que essa
      condição material foi satisfeita por
      RELATORIO_QA_APLICACAO_ADR-0034_P02.md (ADR_APPLICATION_APPROVED,
      achados_pendentes: []). Sem atribuir ao relatório autoridade superior
      ao backlog e sem exigir novo patch do backlog.
  - id_achado: H0041-QA-002
    alteracao: >-
      Seção "6.1": substituída a lista única mista por listas YAML
      separadas — arquivos_existentes_a_alterar, arquivos_novos_a_criar,
      fixture, demonstracao, testes_unitarios, testes_de_integracao,
      relatorio_de_implementacao — preservando todos os caminhos nominais e
      finalidades já autorizados, sem adição nem remoção de arquivo.
  - id_achado: H0041-QA-003
    alteracao: >-
      Seção "10. Testes obrigatórios": acrescentado bloco "Comandos focais"
      com dois comandos pytest reais (unitários: tela/teste_selecao.py
      tela/teste_navegacao.py; integração: tela/teste_renderizador.py
      demo/teste_demo.py demo/teste_demo_selecao.py), seguidos da suíte
      canônica completa preservada.
  - id_achado: H0041-QA-004
    alteracao: >-
      Seção "Roteiro sequencial de validação TTY": roteiro reduzido de 11
      para os 10 passos mínimos exigidos, eliminando os dois passos de
      "verificação sem tecla nova" e separando cada navegação de cada
      seleção em passos distintos e numerados. Ambiguidade "seta_direita ou
      seta_baixo" resolvida para "Seta para baixo" (console de nível único
      em lista vertical, conforme seção 4/ADR-0031/H-0040). Itens, ordem
      navegável e resultados já aprovados preservados.
  - id_achado: H0041-QA-005
    alteracao: >-
      Seção "12. Relatório da execução": teto normal alterado de "600
      palavras; até 900 somente quando houver conteúdo material que não
      possa ser reduzido" para "teto normal de 900 palavras". Caminhos do
      relatório e do template preservados.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_HANDOFF.md
arquivos_alterados:
  - caminho: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
    delta: >-
      seções 3, 6.1, 10, 11 (roteiro TTY) e 12 corrigidas conforme os cinco
      achados de QA_HANDOFF; nenhuma outra seção alterada.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git diff --check -- docs/handoff/H-0041-...md"
    resultado_compacto: sem problemas de whitespace
  - comando_ou_metodo: "test -e tela/teste_navegacao.py, tela/teste_renderizador.py, demo/teste_demo.py"
    resultado_compacto: >-
      os três existem, confirmando a classificação como testes existentes
      (não novos) nas listas nominais da seção 6.1
  - comando_ou_metodo: leitura integral pós-edição do H-0041
    resultado_compacto: estrutura íntegra; nenhuma seção fora do escopo dos 5 achados foi tocada
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
