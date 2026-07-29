---
name: REL-QA-H-0041-implementacao
description: "Auditoria independente da implementação do H-0041"
metadata:
  type: relatorio_qa
  etapa_qa: QA_IMPLEMENTACAO
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-28
rastreabilidade:
  handoff_origem: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  relatorio_impl: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
---

# REL-QA-H-0041 — QA da implementação

## 1. Identificação e status

```yaml
revisao: H-0041 — seleção múltipla: estado, comandos e apresentação
etapa_qa: QA_IMPLEMENTACAO
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: correcao_de_implementacao_e_reteste_QA
```

## 2. Escopo e verificações

Foram auditados o handoff e o relatório de implementação, além dos dez arquivos técnicos reais: `tela/selecao.py`, `tela/navegacao.py`, `tela/renderizador.py`, `demo/demo.py`, a fixture, a demonstração dedicada e seus testes. O diff está limitado aos arquivos autorizados; não há alteração em `config/estilo.json`. A leitura histórica desse arquivo é registrada como `DESVIO_DE_LEITURA_SEM_IMPACTO_MATERIAL`.

```yaml
verificacoes:
  - id: V1
    comando_ou_metodo: gate Git e diff focal
    evidencia_focal: master, HEAD 721f8f1, stage vazio e git diff --check limpo
    resultado: OK
  - id: V2
    comando_ou_metodo: inspecao de selecao, dispatch, fixture e renderer
    evidencia_focal: participante->ID usa a ordem de todos os itens declarados; item_04/item_08 nao deslocam item_05/06/07
    resultado: OK
  - id: V3
    comando_ou_metodo: reproducao semantica do Enter com selecao residual
    evidencia_focal: estado [item_inexistente] seguido de Enter produziu [item_01, item_03, item_05, item_07]
    resultado: FALHA
```

## 3. Achados

```yaml
achados:
  - id: QA-H0041-001
    gravidade: MATERIAL
    arquivo: demo/demo.py
    requisito: D-SEL-04 — reconciliacao vazia apos Enter nao pode aplicar Todos no mesmo acionamento
    evidencia_focal: processar_comando consulta esta_vazia(), que ja descarta IDs residuais, e chama selecionar_todos(); reproducao confirmou a inclusao dos quatro IDs
    impacto: um Enter destinado somente a reconciliar selecao invalida altera a selecao para Todos
    correcao_necessaria: distinguir selecao originalmente vazia de selecao que se tornou vazia pela reconciliacao; acrescentar teste de integracao
  - id: QA-H0041-002
    gravidade: MATERIAL
    arquivo: config/telas/demo/h0041_selecao_multipla_oito_itens.json; tela/renderizador.py
    requisito: Enter com selecao deve apresentar Executar em estado INATIVO
    evidencia_focal: a fixture declara regra_ativo: sempre e o renderer declara que regra_ativo nao e avaliada; apenas troca o rotulo para Executar
    impacto: o comando inerte permanece apresentado como ativo, contrariando o estado exigido
    correcao_necessaria: representar e testar explicitamente o estado inativo de Executar, sem criar operacao externa
```

## 4. Testes, demonstração e validação manual

```yaml
testes_focais:
  - comando_ou_metodo: python -m pytest -q --tb=short tela/teste_selecao.py tela/teste_renderizador.py
    resultado_compacto: 318 coletados, 318 aprovados, 0 falhas
  - comando_ou_metodo: python -m pytest -q --tb=short demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 31 coletados, 31 aprovados, 0 falhas
suite_canonica:
  comando_ou_metodo: python -m pytest
  resultado_compacto: 522 coletados, 522 aprovados, 0 falhas
demonstracao:
  resultado: ponto de entrada e carregamento da fixture cobertos automaticamente; nenhuma operacao externa identificada
validacao_manual:
  necessaria: true
  metodo_reproduzivel: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao --tela config/telas/demo/h0041_selecao_multipla_oito_itens.json
  resultado: PENDENTE — exclusiva do usuario em TTY real
  criterios_pendentes: [roteiro_TTY_H-0041]
```

## 5. Conclusão

A suíte aprovada não cobre as duas transições materiais acima. A correção participante→ID é necessária ao H-0041 e aceitável. O status é `I2_IMPLEMENTATION_PATCH_REQUIRED`; a validação manual permanece pendente após o reteste.
