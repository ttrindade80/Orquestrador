---
name: REL-QA-H-0045-P10
description: "QA pós-patch do cenário verboso multilinha paginado"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I5_MANUAL_VALIDATION_REQUIRED
  data: 2026-08-01
rastreabilidade:
  autorizacao_qa: QA_POS_PATCH
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P10.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P10.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  achados_tratados: [VM-H0045-R06-002]
---

# REL-QA-H-0045-P10 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: "QA pós-patch P10 — VM-H0045-R06-002"
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: I5_MANUAL_VALIDATION_REQUIRED
proxima_categoria: VALIDACAO_MANUAL
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: h0045_paginacao_modo_verboso_multilinha / ITEM-0003
autoridades_materiais:
  - docs/contratos/contrato_console.md §§6, 12, 21, 22, 24
  - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md D-PAG-01..14
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
escopo:
  - autoridade de [V] Verboso e compatibilidade legado/D23
  - fixture real, mapa físico, materialização, cursor e políticas de quebra
  - paginação 80x24/80x15, fronteira mínima e regressões
```

`politica_modo: alternavel` exige V e o chip `[V]`; somente verboso e somente
não verboso não exigem alternância. A fixture P10 não declara `politica_modo`:
usa exclusivamente o envelope legado `politica_exibicao.verboso: true` e
`modo_inicial: verboso`. Portanto nasce verbosa, não deve exibir `[V]`, e o
H-0045 não exige alternância nesse cenário. Não houve comando normativo omitido.

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QA-P10-GIT
    comando_ou_metodo: "branch/HEAD/status/stage e existência dos relatórios"
    evidencia_focal: "master; HEAD b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; P10 presente; QA ausente no início"
    resultado: OK
  - id: QA-P10-LEGADO-D23
    comando_ou_metodo: "provas positivas/negativas no loader e runtime"
    evidencia_focal: "legado verboso OK; moderno somente_verboso e alternavel OK; legado sem política OK; híbrido legado+D23 rejeitado; consumidor moderno sem política rejeitado; V alterna somente no moderno alternavel"
    resultado: OK
  - id: QA-P10-FIXTURE
    comando_ou_metodo: "carregamento real e mapa_fisico_de_itens"
    evidencia_focal: "quatro IDs estáveis; segmento_01..26 uma vez cada; linhas físicas longo_01=23, longo_02=7, curto_03=3, curto_04=3; políticas permitir, evitar, default evitar, default evitar"
    resultado: OK
  - id: QA-P10-GEOMETRIA
    comando_ou_metodo: "leitura focal do renderer + testes de matriz/grupo + fixture real"
    evidencia_focal: "mapa/materialização usam largura efetiva de 77 na célula de 80x24; saída e plano não divergem; nenhum item não paginado regrediu"
    resultado: OK
  - id: QA-P10-PAGINACAO
    comando_ou_metodo: "plano e render reais em 80x24 e 80x15"
    evidencia_focal: "3 páginas com 16; 7+7; 3+3 linhas e 6 páginas na dimensão menor; sem perda, duplicação ou terminal pequeno demais"
    resultado: OK
  - id: QA-P10-CURSOR
    comando_ou_metodo: "percurso de páginas e inspeção do quadro"
    evidencia_focal: "exatamente um cursor; na página 2 a continuação de longo_01 não recebe cursor e longo_02 recebe o cursor; setas permanecem intrapágina"
    resultado: OK
  - id: QA-P10-LIMITE
    comando_ou_metodo: "80x10, 80x9 e 80x8, com retorno"
    evidencia_focal: "80x10/80x9 funcionais; 80x8 exibe quadro mínimo; retorno preserva estado lógico"
    resultado: OK
```

## 4. Achados

nenhum.

## 5. Delta de QA pós-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P10.md
achados_tratados: [VM-H0045-R06-002]
achados_resolvidos: [VM-H0045-R06-002]
achados_pendentes: []
novos_achados: []
```

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py tela/teste_paginacao.py demo/teste_demo_paginacao.py -v"
    resultado_compacto: "363 passed"
    prova_semantica: "fixture real, multilinha, fragmentação, cursor, tokens e 80x15"
  - comando_ou_metodo: "comando expandido solicitado"
    resultado_compacto: "574 passed"
    prova_semantica: "compatibilidade loader, navegação, seleção, D15, resize e fluxo focal"
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest"
    resultado_compacto: "806 passed"
    prova_semantica: "nenhuma regressão na suíte completa"
  - comando_ou_metodo: "ponto de entrada demo.py em PTY automatizado"
    resultado_compacto: "80x24 1/3; . 2/3; . 3/3; , 2/3; 80x15 5/6; 80x8 mínimo; retorno 80x24 2/3"
    prova_semantica: "comandos e redimensionamentos reproduzidos sem validar usuário"
demonstracao:
  resultado: OK_AUTOMATIZADA
  evidencia: "python demo/demo.py h0045_paginacao_modo_verboso_multilinha; [V] ausente e todos os tokens recuperáveis"
validacao_manual:
  necessaria: true
  metodo_reproduzivel: "retomar o roteiro manual R07_CONSOLIDADA na etapa 14/17"
  resultado: PENDENTE_USUARIO_R07_CONSOLIDADA
  criterios_pendentes: ["validação manual das etapas 14/17..17/17"]
```

Foram identificados três testes P10 adicionados, dois em `demo/teste_demo_paginacao.py`
e um em `tela/teste_renderizador.py`. Todos carregam a fixture real; não há
fixture equivalente conveniente, monkeypatch do resultado, remoção ou
renomeação observada. As contagens 574/806 são coerentes com P09: 571/803 + 3.

## 7. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
  staged: []
  unstaged: "worktree acumulado de P01-P10 preservado; alterações P10 atribuíveis somente aos cinco caminhos declarados"
  nao_rastreados: "artefatos e relatórios acumulados de P01-P10; relatório deste QA criado pela auditoria"
itens_inesperados: []
```

## 8. Conclusão

O patch resolve materialmente `VM-H0045-R06-002`: a fixture é multilinha real,
o plano físico e a renderização concordam, o cursor e as políticas de quebra
seguem o contrato, e as dimensões e regressões foram aprovadas. Permanecem
preservados, sem agravamento, `QA-H0045-P08-001` e `VM-H0045-R06-001`. O próximo
passo é exclusivamente a validação manual R07, preservando 6/17..13/17 e
retomando em 14/17.
