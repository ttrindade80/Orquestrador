---
name: RELATORIO_QA_HANDOFF_H-0048
description: "Resultado factual da auditoria do H-0048 após P01"
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H2_HANDOFF_PATCH_REQUIRED
  data: 2026-08-03
rastreabilidade:
  autorizacao_qa: QA_HANDOFF — H-0048
  adr_auditada: docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md
  handoff_origem: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
  contrato_alvo: null
  adr_relacionadas: [ADR-0039]
  issues_relacionadas: [ITEM-0022]
  predecessor_imediato: P01
  achados_tratados: []
---

# RELATORIO_QA_HANDOFF_H-0048 — Auditoria independente

## 1. Identificação e status

```yaml
revisao: H-0048 — Reorganizar estruturalmente os testes do renderizador
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: H2_HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_HANDOFF
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
autoridades_materiais:
  - docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md
  - docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  - docs/handoff/H-0047-modularizacao-estrutural-do-loader.md
  - ITEM-0022 em docs/backlog.md
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V-001
    comando_ou_metodo: baseline Git e manifesto fechado de leitura
    evidencia_focal: branch master, HEAD 5d5d4c7, stage vazio e alterações rastreadas ausentes; leitura dos quatro documentos, bloco do ITEM-0022 e template QA
    resultado: OK
  - id: V-002
    comando_ou_metodo: inventário AST focal de tela/teste_renderizador.py
    evidencia_focal: 13.960 linhas; 120 funções top-level; 72 funções coletáveis; 21 classes; 299 métodos test_*; 371 testes; 1 fixture; 0 parametrizações; 1 main e 1 guard; 47 helpers
    resultado: OK
  - id: V-003
    comando_ou_metodo: coleta e execução baseline
    evidencia_focal: fachada atual coleta e aprova 371; suíte completa coleta 970; runner direto aprova 1.308/1.308
    resultado: OK
  - id: V-004
    comando_ou_metodo: pytest.ini, três buscas fechadas e AST de tela/renderizacao/*.py
    evidencia_focal: somente pytest.ini existe, com python_files=test_*.py e testpaths=tela demo; nenhum ciclo nem importação inversa; consumidores externos usam a fachada
    resultado: OK
  - id: V-005
    comando_ou_metodo: prova descartável de fixture e compileall
    evidencia_focal: fachada importada coleta, mas não registra fixture indireta; compileall criou dois .pyc apesar da variável de ambiente
    resultado: FALHA
```

## 4. Achados

```yaml
- id: H0048-HANDOFF-QA-001
  severidade: alto
  requisito: H-0048 §6.4 e §8.2 — fixture executável pela fachada
  evidencia_focal: >
    fixture_h0041_qa002 é definida em selecao.py, enquanto a fachada
    reexporta somente testes/classes. Prova pytest: coleta indireta passa,
    execução falha com fixture não encontrada; coleta direta do proprietário
    passa.
  impacto: Os testes QAH0041/seleção não executam pela suíte canônica da fachada.
  correcao_necessaria: >
    Corrigir o handoff para que a fixture seja registrada no caminho de coleta
    autorizado, sem mudar identidade, consumidores ou criar solução fora do escopo.
- id: H0048-HANDOFF-QA-002
  severidade: alto
  requisito: H-0048 §10, §14.1 e §10 — política de temporários e resíduos
  evidencia_focal: >
    Em cópia descartável, PYTHONDONTWRITEBYTECODE=1 python -m compileall -q
    tela/teste_renderizador.py tela/testes_renderizador terminou com código 0
    e criou __pycache__/*.pyc. O handoff autoriza apenas saídas transitórias
    do pytest e não define limpeza/autorização para esses resíduos.
  impacto: >
    A prova obrigatória deixa resíduos novos em escopo nominal proibido,
    contrariando a reversibilidade e a política de não persistência.
  correcao_necessaria: >
    Ajustar o handoff para usar uma prova sem resíduos ou autorizar e fechar
    explicitamente a limpeza dos .pyc produzidos.
```

## 5. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_renderizador.py
    resultado_compacto: 371 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
    resultado_compacto: 970 tests collected
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
    resultado_compacto: 1.308 verificações passaram
demonstracao:
  resultado: INCOMPLETA
  evidencia: o handoff falha na visibilidade da fixture e na política de resíduos
validacao_manual:
  necessaria: false
```

## 6. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 5d5d4c794508b1981f5fa65be079b8db748c6064
  staged: vazio
  unstaged: nenhum
  nao_rastreados: baseline esperado e este relatório QA
itens_inesperados: []
```

## 7. Conclusão

O diagnóstico estrutural e os números transportados pelo H-0048 são confirmados, e a autoridade da ADR-0039 permanece fiel. Entretanto, a combinação declarada para a fixture não é executável pela fachada e o comando obrigatório de compilação viola a política de resíduos. O H-0048 requer patch documental antes da implementação.
