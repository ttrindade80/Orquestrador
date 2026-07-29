---
name: REL-PATCH-H0041-P02-selecao-multipla-estado-comandos-e-apresentacao
description: "Correção do estado lógico independente do chip Enter (QA-H0041-002) e correção factual do relatório P01 (REL-PATCH-H0041-P01)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0041
  cadeia_raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P01.md
  achados_tratados:
    - QA-H0041-002
    - REL-PATCH-H0041-P01
---

# REL-PATCH-H0041-P02 — Patch da implementação do H-0041

> Relatório incremental. Delta focal de QA-H0041-002 e REL-PATCH-H0041-P01.
> Não reimplementa a capacidade; não substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P01.md
achados_tratados:
  - QA-H0041-002
  - REL-PATCH-H0041-P01
achados_resolvidos:
  - QA-H0041-002
  - REL-PATCH-H0041-P01
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-H0041-002
    alteracao: >
      Estado lógico ATIVO/INATIVO do chip Enter materializado pela avaliação
      de regra_ativo, independente do rótulo. Fixture: chip_enter passa de
      regra_ativo:sempre para regra_ativo:selecao_vazia (convenção paralela a
      regra_existencia). Renderer: _avaliar_regra_ativo consome a regra;
      estado consultável em _navegacao_atual["estado_ativo_chips"];
      representação visual (caixa baixa) é apenas consequência do estado
      inativo — enter_inativo = (rotulo_enter == "Executar") removido.
      sem_selecao: Todos + ATIVO; com_selecao: Executar + INATIVO.
      Nenhuma operação externa criada. Consoles sem seleção múltipla
      preservam comportamento anterior (regra_ativo=sempre → ATIVO).

  - id_achado: REL-PATCH-H0041-P01
    alteracao: >
      metadata e §1 passam a declarar PATCH_IMPLEMENTACAO. Declarações de
      design do P01 alinhadas ao código histórico: P01 tentou redução de
      ênfase; não avaliou estruturalmente regra_ativo; não materializou
      estado lógico independente; QA-P01 considerou insuficiente; P02
      responsável pela correção final. QA-H0041-001 permanece como
      resolvido do P01.

arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_P02.md

arquivos_alterados:
  - caminho: config/telas/demo/h0041_selecao_multipla_oito_itens.json
    delta: chip_enter.regra_ativo = selecao_vazia
  - caminho: tela/renderizador.py
    delta: >
      _avaliar_regra_ativo; avaliação por chip em _linhas_barra;
      estado_ativo_chips no contexto; visual inativo derivado da regra
  - caminho: tela/teste_renderizador.py
    delta: >
      testes QA-H0041-002 reescritos (estado lógico, independência do
      rótulo, consumo de regra_ativo, visual como consequência)
  - caminho: demo/teste_demo.py
    delta: Enter_em_Executar reforçado; fixture regra_ativo assertada
  - caminho: demo/teste_demo_selecao.py
    delta: teste de regra_ativo=selecao_vazia na fixture
  - caminho: docs/relatorios/RELATORIO_PATCH_H-0041_P01.md
    delta: tipo_execucao e factualidade de QA-H0041-002 corrigidos

arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_renderizador.py
    resultado_compacto: 300 passed

  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 36 passed

  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_selecao.py tela/teste_renderizador.py
      demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 361 passed

  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 534 passed (530 prévios + 4; sem regressão)

confirmacao_semantica:
  - estado_logico_independente_do_rotulo: true
  - Todos_sem_selecao_ATIVO: true
  - Executar_com_selecao_INATIVO: true
  - Enter_em_Executar_selecao_inalterada: true
  - primeiro_Enter_residual_somente_reconcilia: true
  - segundo_Enter_vazio_seleciona_quatro_itens: true
  - nenhuma_operacao_externa: true
  - demo.py_preservado: true
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios:
  - validacao_TTY_manual: permanece_pendente_usuario
evidencias_separadas: []
```

## 6. Estado Git

```yaml
branch: master
HEAD: 721f8f1
stage: vazio
diff_check: limpo
```
