---
name: REL-QA-H-0041-implementacao-P01
description: "QA pós-patch P01 da implementação do H-0041"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-28
rastreabilidade:
  etapa: QA_POS_PATCH
  objeto: H-0041
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_H-0041_P01.md
  patch_auditado: P01
  achados_retestados:
    - QA-H0041-001
    - QA-H0041-002
---

# REL-QA-H-0041-P01 — QA pós-patch da implementação

## 1. Identificação e status

```yaml
revisao: H-0041 — reteste independente do patch P01
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: correcao_focal_da_implementacao_e_do_relatorio_de_patch
```

## 2. Escopo e verificações

```yaml
objeto_auditado: patch P01 dos achados QA-H0041-001 e QA-H0041-002
autoridades_materiais:
  - docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO.md
  - docs/relatorios/RELATORIO_PATCH_H-0041_P01.md
escopo:
  - dispatch de Enter, renderer, fixture e testes autorizados
verificacoes:
  - id: V1
    comando_ou_metodo: gate Git e diff focal autorizado
    evidencia_focal: master; HEAD 721f8f1; stage vazio; diff_check limpo
    resultado: OK
  - id: V2
    comando_ou_metodo: reproducao independente de dois Enters
    evidencia_focal: "[item_inexistente] -> [] -> [item_01,item_03,item_05,item_07]; sem campos de operacao externa"
    resultado: OK
  - id: V3
    comando_ou_metodo: auditoria do estado do chip Enter
    evidencia_focal: "enter_inativo = rotulo_enter == 'Executar'; regra_ativo nao e avaliada"
    resultado: FALHA
```

## 3. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0041-002 | alto | estado lógico independente para `Executar` inativo | A fixture ainda declara `regra_ativo: sempre`; `_linhas_barra` não a avalia e deriva `enter_inativo` exclusivamente do rótulo. | A distinção visual em caixa baixa é somente consequência textual, não estado lógico materializado. | Materializar e testar estado inativo independente do rótulo, sem operação externa. |
| REL-PATCH-H0041-P01 | médio | exatidão factual do relatório | `metadata.tipo_execucao` e §1 dizem `PATCH_HANDOFF`, enquanto a própria rastreabilidade diz `PATCH_IMPLEMENTACAO`. O tipo correto é `PATCH_IMPLEMENTACAO`. | Rastreabilidade contraditória; o relatório também declara uso estrutural de `regra_ativo` que o código não realiza. | Corrigir somente o relatório do patch e suas declarações de design. |

Uso de função privada: `selecao._selecao_do_console` apenas lê uma cópia da lista bruta, sem mutação nem estado persistente novo. A API pública `selecao()` reconcilia o valor e, por isso, não é adequada para decidir se a seleção já era vazia antes do acionamento. Classificação: `NOTA — uso_focal_sem_risco_material`.

O registro autoral de leituras fora do manifesto é `DESVIO_DE_LEITURA_SEM_IMPACTO_MATERIAL`: não há evidência, no delta P01, de decisão arquitetural nova derivada delas.

## 4. Delta de QA pós-patch

```yaml
raiz: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_H-0041_P01.md
achados_tratados: [QA-H0041-001, QA-H0041-002]
achados_resolvidos: [QA-H0041-001]
achados_pendentes: [QA-H0041-002]
novos_achados: [REL-PATCH-H0041-P01]
```

## 5. Testes e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 34 aprovados, 0 falhas
    prova_semantica: reteste de Enter residual e ausência de operação externa
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short tela/teste_renderizador.py
    resultado_compacto: 298 aprovados, 0 falhas
    prova_semantica: apresentação distinta, insuficiente como prova do estado independente
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short tela/teste_selecao.py tela/teste_renderizador.py demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 357 aprovados, 0 falhas
    prova_semantica: regressão focal
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 530 aprovados, 0 falhas
    prova_semantica: regressão geral
validacao_manual:
  necessaria: true
  metodo_reproduzivel: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao --tela config/telas/demo/h0041_selecao_multipla_oito_itens.json
  resultado: PENDENTE — exclusiva do usuário em TTY real
  criterios_pendentes: [roteiro_TTY_H-0041]
```

## 6. Conclusão

`QA-H0041-001` foi resolvido: o primeiro Enter somente reconcilia o resíduo e o segundo aplica Todos. `QA-H0041-002` permanece pendente porque o estado inativo é calculado exclusivamente por `rotulo_enter == "Executar"`; caixa baixa não supre essa ausência. A contradição de tipo de execução do relatório P01 também exige correção. A validação TTY continua pendente e não foi executada.
