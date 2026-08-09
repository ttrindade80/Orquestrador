---
name: RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0053_P03
description: "Auditoria independente do patch de implementação P03"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-08-09
rastreabilidade:
  autorizacao_qa: H-0053 P03
  adr_auditada:
    - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
    - docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  handoff_origem: docs/handoff/H-0053-arvore-colapsavel.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03.md
  predecessor_imediato: RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03
  achados_tratados: []
---

# REL-QA — H-0053 P03

## 1. Identificação e status

```yaml
revisao: H-0053 P03 — QA pós-patch de implementação
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: H-0053 — arvore_colapsavel
autoridades_materiais:
  - ADR-0042 D-MULTI-05 e §4.5
  - ADR-0043 D-CHIP-01 a D-CHIP-12
  - H-0053 P02 aprovado
  - RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03
escopo:
  - chips, cursor, projeção, renderer, fixture, multiline, regressões e paginação fora de escopo
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QA-P03-preflight
    comando_ou_metodo: branch, HEAD, stage, status e existência dos artefatos obrigatórios
    evidencia_focal: master; 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d; stage vazio
    resultado: OK
  - id: QA-P03-semantica
    comando_ou_metodo: leitura de código, fixtures, testes e buscas focais de seleção, hardcode e paginação
    evidencia_focal: chips contextuais derivados do item corrente; ConteudoExterno/NoConteudo preservado; sem dependência de IDs da fixture ou nova paginação
    resultado: INCOMPLETA
  - id: QA-P03-testes-focais
    comando_ou_metodo: pytest -q tela/teste_navegacao.py; pytest -q demo/teste_demo_console.py
    evidencia_focal: 59 passed; 9 passed
    resultado: OK
  - id: QA-P03-suite
    comando_ou_metodo: pytest -q
    evidencia_focal: 1071 passed in 27.61s
    resultado: OK
  - id: QA-P03-git
    comando_ou_metodo: git diff --check; git diff --cached --name-only; git status --short --untracked-files=all
    evidencia_focal: diff --check limpo; stage vazio; estado transportado além do conjunto declarado por P03
    resultado: OK
```

## 4. Achados

```yaml
achados:
  - id: H-0053-P03-A
    severidade: alto
    requisito: invariável de cursor — árvore focalizada deve possuir cursor/item corrente válido e não pode ser renderizada como interativa sem ele
    evidencia_focal: >-
      estado_chip_arvore() retorna None sem cursor (tela/navegacao.py:792-798),
      mas _parametros_renderizacao_arvore() usa cursor default 0 e marca o
      primeiro nó quando focado (tela/renderizacao/console.py:53-65). Na
      reprodução non-TTY com modelo H-0053, foco_console=0 e cursores={}, o
      resultado foi chip None, linha com indicador "→ 1. ..." e chip
      declarativo [␣] Expandir presente.
    impacto: >-
      O boundary real de renderização mantém a árvore focalizada e mascara a
      ausência de cursor, divergindo da invariável ADR-0043 e da alegação de
      P03; o rótulo/estado contextual deixa de representar um item corrente
      válido.
    correcao_material_necessaria: >-
      Corrigir o fluxo de renderização para não materializar indicador nem
      chip contextual de árvore focalizada sem cursor válido, preservando a
      inicialização normal de foco/cursor.
```

## 5. Delta de QA pós-patch

```yaml
raiz: H-0053-P03-A
predecessor_imediato: RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03
achados_tratados: []
achados_resolvidos: []
achados_pendentes:
  - H-0053-P03-A
novos_achados:
  - H-0053-P03-A
```

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest -q tela/teste_navegacao.py
    resultado_compacto: 59 passed
    prova_semantica: cobre expansão, recolhimento, folhas, cursor, chips e projeção paginada
  - comando_ou_metodo: pytest -q demo/teste_demo_console.py
    resultado_compacto: 9 passed
    prova_semantica: cobre fixture, Ajuda, chips, redraw non-TTY e multiline
  - comando_ou_metodo: pytest -q
    resultado_compacto: 1071 passed
    prova_semantica: regressão integral aprovada
demonstracao:
  resultado: não executada em TTY interativa
  evidencia: fluxo non-TTY e testes automatizados aprovados; paginação dedicada fora de escopo
validacao_manual:
  necessaria: true
  metodo_reproduzivel: sessão TTY real após correção do achado
  resultado: PENDENTE_USUARIO
  criterios_pendentes:
    - cursor válido e chip contextual em todos os estados
```

## 7. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d
  staged: vazio
  unstaged: alterações transportadas do ciclo, incluindo código/render/documentação
  nao_rastreados: fixtures, relatórios e caches já presentes no preflight
itens_inesperados:
  - item: arquivos fora da lista declarada por P03 no estado do worktree
    origem: NAO_CONFIRMADA
    evidencia: status inicial já os listava; não foram alterados pelo QA
```

## 8. Conclusão

Os chips, a projeção hierárquica, a fixture, o multiline, as regressões e as
suítes estão aprovados, e não há hardcode de fixture nem paginação nova
atribuível ao patch. O achado H-0053-P03-A impede a aprovação da implementação;
a validação manual permanece posterior ao patch de implementação.
