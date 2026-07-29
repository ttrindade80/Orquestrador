---
name: REL-QA-H0041-IMPLEMENTACAO-P03
description: "QA pós-patch P03 da implementação do H-0041"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-28
rastreabilidade:
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P02.md
  cadeia_raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_H-0041_P03.md
  patch_auditado: P03
  achados_retestados:
    - H0041-MANUAL-001
    - H0041-MANUAL-002
    - H0041-MANUAL-003
---

# REL-QA-H0041 — QA pós-patch P03 da implementação

## 1. Identificação e status

```yaml
revisao: H-0041 — reteste focal do P03
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: correção factual do relatório P03 requerida
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e verificações

```yaml
objeto_auditado: correções P03 dos achados H0041-MANUAL-001/002/003
autoridades_materiais:
  - docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0041.md
  - docs/relatorios/RELATORIO_PATCH_H-0041_P03.md
escopo:
  - regra e apresentação dos chips Espaço e Enter
  - sincronização após Todos
  - exatidão documental do P03
verificacoes:
  - id: GIT
    comando_ou_metodo: gate Git de leitura
    evidencia_focal: master, HEAD 721f8f1, stage vazio, diff --check limpo; artefatos requeridos presentes e QA-P03 inicialmente ausente
    resultado: OK
  - id: H0041-MANUAL-001
    comando_ou_metodo: inspeção focal e reprodução não interativa
    evidencia_focal: fixture declara item_focalizado_selecionavel; renderer repassa selecao.chip_espaco_ativo e recalcula a cada render
    resultado: OK
  - id: H0041-MANUAL-002-003
    comando_ou_metodo: reprodução não interativa do dispatcher e redraw
    evidencia_focal: Enter=Executar/INATIVO com seleção; Todos produz quatro tg e Enter INATIVO no mesmo quadro
    resultado: OK
```

## 3. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| H0041-P03-DOC-001 | alto | Exatidão e rastreabilidade do relatório de patch | O P03 declara `tipo_execucao: PATCH_HANDOFF`, `cadeia_raiz: ADR-0034` e predecessor textual. O registro formal requerido é `PATCH_IMPLEMENTACAO`, a raiz `docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md` e o predecessor `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0041.md`. | O artefato autoral identifica incorretamente a execução e quebra a cadeia rastreável. | Corrigir somente os campos factuais do relatório P03. |

## 4. Delta de QA pós-patch

```yaml
raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_H-0041_P03.md
achados_tratados:
  - H0041-MANUAL-001
  - H0041-MANUAL-002
  - H0041-MANUAL-003
achados_resolvidos:
  - H0041-MANUAL-001
  - H0041-MANUAL-002
  - H0041-MANUAL-003
achados_pendentes: []
novos_achados:
  - H0041-P03-DOC-001
```

`H0041-MANUAL-001` está resolvido: em `item_02`, não selecionável, Espaço ficou lógico e visualmente inativo; em item selecionável ele fica ativo. Espaço não alterou a seleção sobre `item_02`. A decisão não usa o texto do chip.

`H0041-MANUAL-002` está resolvido nos três casos requisitados: o rótulo Executar permanece visível, mas o estado lógico é INATIVO e a apresentação é inativa; o renderer consome `estado_ativo_chips`, o chip não desaparece e não há operação, callback ou mensagem. Consoles sem seleção múltipla preservam os chips vigentes.

`H0041-MANUAL-003` está resolvido: Enter com seleção inicialmente vazia selecionou `item_01`, `item_03`, `item_05` e `item_07`; a renderização seguinte, sem redraw adicional, mostrou quatro `tg` e Executar INATIVO. A cadeia observada é alteração de runtime, reconstrução de contexto e avaliação de chips no render corrente, sem contexto anterior reutilizado.

Foram preservados: primeiro Enter sobre resíduo apenas reconcilia; segundo Enter iniciado vazio seleciona os quatro itens; Enter em Executar não tem efeito; associação participante→ID; Esc limpa seleção e permanece, e Esc sem seleção encerra.

## 5. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest -q tela/teste_renderizador.py
    resultado_compacto: 307 coletados, 307 aprovados, 0 falhas
  - comando_ou_metodo: pytest -q demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 42 coletados, 42 aprovados, 0 falhas
  - comando_ou_metodo: pytest -q tela/teste_selecao.py tela/teste_renderizador.py demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 374 coletados, 374 aprovados, 0 falhas
  - comando_ou_metodo: pytest
    resultado_compacto: 547 coletados, 547 aprovados, 0 falhas
demonstracao:
  resultado: APROVADA_NAO_INTERATIVA
  evidencia: os três cenários materiais produziram os estados esperados no mesmo processo de runtime
validacao_manual:
  necessaria: true
  metodo_reproduzivel: terminal TTY real com a fixture H-0041
  resultado: PENDENTE_APOS_CORRECAO_DOCUMENTAL
  criterios_pendentes:
    - revalidação TTY pelo usuário
```

As 547 aprovações declaradas no P03 correspondem à execução independente. H0041-MANUAL-002/003 foram considerados resolvidos pela evidência independente acima, não apenas pela reprodução autoral. O P03 não declara aprovação autoral; mantém corretamente a situação de aguardar QA. O delta funcional inspecionado limita-se aos arquivos técnicos autorizados, sem schema, símbolo de estilo ou operação externa novos; nenhum arquivo normativo é atribuído ao P03.

## 6. Conclusão

A correção funcional do P03 resolve os três achados manuais e preserva os comportamentos anteriores. Contudo, as inexatidões materiais de tipo e cadeia no relatório P03 exigem patch factual do próprio relatório. Por isso, o status é `I2_IMPLEMENTATION_PATCH_REQUIRED`; após essa correção, permanece obrigatória a revalidação em TTY real pelo usuário.
