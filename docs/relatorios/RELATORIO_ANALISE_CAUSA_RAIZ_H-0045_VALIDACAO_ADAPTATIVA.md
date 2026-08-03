---
name: REL-H0045-analise-causa-raiz-validacao-adaptativa
description: "Análise técnica forense da regeneração lógica durante resize"
metadata:
  type: relatorio_busca_levantamento_verificacao
  tipo_execucao: ANALISE_TECNICA_FORENSE
  status: ANALYSIS_COMPLETED
  data: 2026-08-02
extensao_excepcional:
  motivo: "As provas A-E, hashes, caminho de chamadas e avaliação de invariantes são exigidos pelo manifesto forense."
rastreabilidade:
  etapa: ANALISE_TECNICA_FORENSE
  objeto: H-0045 / regeneração indevida durante resize
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
---

# REL-H0045 — Análise técnica forense

## 1. Pergunta e status

```yaml
pergunta: determinar se resize altera conteúdo lógico e localizar a camada causal
status_literal: ANALYSIS_COMPLETED
validacao_manual: nao_executada
produto_aprovado_ou_reprovado: nao_declarado
```

Evidência visual transportada textualmente: na geometria estreita, a linha foi observada como `LARGURA_INICIO - LARGURA_MEIO - LARGURA_FIM`; na larga, como a mesma sequência com mais `-`. Isso é representação textual da observação, não validação manual adicional.

## 2. Escopo fechado

Consultados integralmente: handoff H-0045; `demo/casos_validacao_paginacao.py`; `demo/demo.py`; `demo/teste_demo_paginacao.py`; relatórios P12 e P15; índice de templates e `TEMPLATE_RELATORIO_BUSCA_LEVANTAMENTO_VERIFICACAO.md`. Consulta focal: `tela/renderizador.py` e `tela/paginacao.py`. Não foram alterados código, handoff, testes ou fixtures.

## 3. Hipóteses e provas

```yaml
H1: CONFIRMADA — o helper gera conteúdo maior com W maior.
H2: CONFIRMADA — resize despacha novamente o helper e substitui itens.
H3: CONFIRMADA — despacho restrito a h0045_validacao_*.
H4: REFUTADA_NO_ESCOPO — demos normais não passam pelo helper e mantiveram o hash.
H5: CONFIRMADA — entrada fixa reduz quebras quando W aumenta.
H6: CONFIRMADA_NO_ESCOPO — runtime P01-P11 não apresentou regressão focal.
H7: PARCIALMENTE_CONFIRMADA — §18 autoriza geração após geometria e exige validade em geometrias múltiplas, mas não fixa congelamento do modelo durante uma execução.
```

**A — helper.** Chamadas diretas equivalentes: `W=50` produziu linha lógica de 75 caracteres, hash `229334bc2b9c85306452ec0e788de03244516538fd7e06b3838544e1dbf62569`, 34 hifens e cada marcador uma vez; `W=80` produziu 120 caracteres, hash `1c89b53ea3a9482c363abe42d3663393abeed6e411b2cda15fe70cad068256a6`, 79 hifens e cada marcador uma vez. Prova H1, não defeito isolado.

**B — caminho de resize.** `demo.py:1241-1248` instala `SIGWINCH`; `demo.py:1443-1459` drena o wakeup pipe e resolve dimensões; `demo.py:1465-1470` atualiza geometria; `demo.py:1473-1477` chama `_aplicar_caso_validacao_adaptativo`; só depois `demo.py:1481-1486` reconcilia e renderiza. Dentro do helper, `demo.py:953-981` mede W/C e constrói novos itens; `casos_validacao_paginacao.py:445-464` grava-os no modelo; `demo.py:994-997` zera foco, cursores e páginas. A reconciliação posterior (`tela/paginacao.py:287-304`) não consegue preservar o item porque o cursor já foi removido.

**C — invariância.** Em `h0045_validacao_largura`, W/C mudou `22/16 → 37/16`; ID, quantidade e política permaneceram, mas texto/hash mudaram (`0a6e4494b46bc4459feb8358cda352295bf8ea4553b0c6995b0d86c0a9f40b90 → da6cd4b91217eef9abfea41c1ace66d21b8d890ba4f8484afb4e6a983d1baf53`) e cursor/página foram zerados. Em `h0045_validacao_continuacao`, C mudou `16 → 32`, a relação gerada `33 → 65` linhas e o hash mudou (`181ac59d32dbc8e244e179138e7b71d302c5e2179cb589faf20674d8fefe5fd6 → e88bca94258cc2acd9974996ec44b4932ca262d2d09c6e530bb655f1cc597299`). Em `h0045_paginacao_console_unico` e `h0040_nav_matriz_26_itens_redimensionamento`, sem `caso_validacao_adaptativo`, o hash do modelo permaneceu igual e o cursor não foi reconstruído. H3 confirmada e H4 refutada no caminho observado.

**D — renderer com entrada fixa.** Uma única entrada lógica fixa, hash `d5686968a72a8db349a14565f3b707050869c1106329f1feb5463dde90319c3d`, foi renderizada em 50 e 100 colunas sem troca do modelo. O mapa físico caiu de 5 para 3 linhas; `FIXO_INICIO`, `FIXO_MEIO` e `FIXO_FIM` apareceram uma vez, em ordem, nas duas geometrias. Não há perda, duplicação ou defeito observado no renderer; H5 confirmada.

**E — paginação funcional.** Verificação automatizada focal de paginação, navegação, renderer, fluxo e demos P01–P11: `36 passed`. Os testes cobriram troca/extremos, cursor, resize, consoles independentes, grupos, item multilinha, políticas, conjunto vazio e coerência plano/render. Não foi observada regressão do runtime funcional no escopo testado; isso não substitui QA integral.

## 4. Classificação

```yaml
classificacoes:
  - VALIDATION_HARNESS_ONLY
  - DEMO_INTEGRATION_REGRESSION
  - HANDOFF_METHOD_DEFECT
  - MULTIPLE_LAYERS
nao_classificadas:
  - RUNTIME_PAGINATION_REGRESSION
  - RENDERER_REGRESSION
```

A causa direta está na integração do harness adaptativo em `demo.py`, não em `tela/paginacao.py` nem no renderer. A §18 é metodologicamente incompleta: `§18.2.2`, `§18.3`, `§18.5` e `§18.7` legitimam geração dependente de geometria, mas não dizem que a geração ocorre somente uma vez por execução; ao mesmo tempo, `CA-H0045-12` e `§18.6` exigem preservar o item lógico no resize. Essa lacuna permite a interpretação que causou a regeneração.

## 5. Invariantes avaliados

INV-01–INV-06 são adequados e corrigiriam o fenômeno. Ajustes necessários: INV-01 deve dizer explicitamente “uma vez por execução do caso”; INV-02 deve separar metadados diagnósticos W/C do modelo lógico e proibir que sejam usados para substituir itens; INV-06 deve declarar expressamente que resize usa a mesma entrada e pode fazer a página de continuação desaparecer, sem reconstruí-la.

## 6. Próxima etapa e bloqueios

Recomendação: `PATCH_HANDOFF → QA_HANDOFF → PATCH_IMPLEMENTACAO → QA_POS_PATCH → nova validação manual 15/17–17/17`. A validação manual permanece bloqueada pelo método atual; não foi executada nem reclassificada.

## 7. Estado Git

```yaml
branch: master
HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
stage: vazio
worktree: acumulado H-0045/P01-P15 e patches de handoff
alteracoes_desta_analise: somente este relatório; sem stage e sem commit
```
