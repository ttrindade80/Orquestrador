---
name: REL-PATCH-H0041-P01-selecao-multipla-estado-comandos-e-apresentacao
description: "Correção focal dos achados QA-H0041-001 (reconciliação no Enter) e tentativa de QA-H0041-002 (representação inativa de Executar) da implementação do H-0041"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0041
  cadeia_raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO.md
  achados_tratados:
    - QA-H0041-001
    - QA-H0041-002
---

# REL-PATCH-H0041-P01 — Patch da implementação do H-0041

> Relatório incremental. Delta focal dos achados QA-H0041-001 e QA-H0041-002.
> Não reimplementa a capacidade; não substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO.md
achados_tratados:
  - QA-H0041-001
  - QA-H0041-002
achados_resolvidos:
  - QA-H0041-001
achados_pendentes:
  - QA-H0041-002
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-H0041-001
    alteracao: >
      Enter passa a distinguir seleção originalmente vazia (aplica Todos) de
      seleção originalmente não vazia que se torna vazia após reconciliação
      (somente reconcilia, sem aplicar Todos no mesmo acionamento). A decisão
      consulta a seleção bruta no início do acionamento (antes de descartar
      IDs residuais), preservando IDs inválidos descartados (D-SEL-03).

  - id_achado: QA-H0041-002
    alteracao: >
      O P01 tentou representar a inatividade do chip [Enter]/Executar por
      redução de ênfase visual (rótulo em caixa baixa), sem trocar apenas o
      rótulo capitalizado. A tecla e os delimitadores permaneceram (R-6).
      cor_inativo não tinha valor ANSI concreto; o renderer não inventou cor
      nem alterou símbolos do estilo. A decisão de inativo no P01 derivava de
      rotulo_enter == "Executar" — o P01 NÃO materializou estado lógico
      ATIVO/INATIVO independente do texto e NÃO avaliou estruturalmente
      regra_ativo (a fixture manteve regra_ativo: sempre). O QA posterior
      (RELATORIO_QA_H-0041_IMPLEMENTACAO_P01) considerou essa solução
      insuficiente. A correção final do estado lógico independente fica a
      cargo do P02.

arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_P01.md

arquivos_alterados:
  - caminho: demo/demo.py
    delta: >
      processar_comando: branch do Enter em console com seleção multipla
      decidida pela seleção originalmente vazia (leitura bruta via
      selecao._selecao_do_console) antes da reconciliação; seleção com
      resíduo apenas reconcilia (selecao.reconciliar); seleção
      originalmente vazia aplica selecionar_todos.

  - caminho: tela/renderizador.py
    delta: >
      _texto_chip_barra ganha parâmetro inativo (default False): chip
      inativo exibe rótulo em caixa baixa (redução de ênfase). _linhas_barra
      computava enter_inativo (rotulo_enter == "Executar") e aplicava-o ao
      chip com forma_exibicao "rotulo_dinamico_selecao". Nenhum schema/cor/
      símbolo novo; demais chips e consoles sem seleção multipla inalterados.
      Observação factual: regra_ativo NÃO era avaliada neste P01.

  - caminho: demo/teste_demo.py
    delta: >
      3 testes novos de integração reproduzindo o cenário QA-H0041-001
      (seleção residual [item_inexistente] -> Enter -> [] sem Todos;
      segundo Enter -> [item_01,03,05,07]; sem operação externa).

  - caminho: tela/teste_renderizador.py
    delta: >
      Atualizado teste_selecao_multipla_h0041 para verificar representação
      inativa (caixa baixa) com rótulo Executar. 5 testes pytest novos
      (test_qah0041_002_*): chip ativo sem seleção; chip inativo com
      seleção; distinção visual ativo/inativo; ausência de operação
      externa; console sem seleção multipla preserva ativo. Esses testes
      do P01 ainda acoplavam inatividade ao rótulo — insuficiente perante
      o QA-P01; P02 substitui a prova por estado lógico via regra_ativo.

arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 34 passed

  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_renderizador.py
    resultado_compacto: 298 passed

  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_selecao.py tela/teste_renderizador.py
      demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 357 passed

  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 530 passed (522 prévios + 8 novos; sem regressão)

  - comando_ou_metodo: confirmação semântica isolada (Python direto)
    resultado_compacto: >
      seleção residual -> Enter -> [] (Todos não aplicado);
      segundo Enter (vazio) -> [item_01,03,05,07];
      Executar renderizado com redução de ênfase (caixa baixa);
      Enter em Executar não altera seleção;
      nenhuma operação externa introduzida.
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas: []
```

## 6. Decisões de design (QA-H0041-002) — registro factual do P01

O P01 adotou redução de ênfase (caixa baixa) porque:

- `cor_inativo` não possui valor ANSI concreto decidido;
- o renderer não inventa cor, não altera símbolos do estilo e não cria schema;
- a representação visual sinalizava inatividade sem remover o chip (R-6).

Limite factual do P01 (confirmado pelo QA-P01):

- o P01 **não** avaliou estruturalmente `regra_ativo`;
- o P01 derivava `enter_inativo` de `rotulo_enter == "Executar"`;
- a fixture manteve `regra_ativo: sempre` — contradição com o estado inativo;
- não havia estado lógico ATIVO/INATIVO independente do texto apresentado;
- o QA posterior considerou a solução insuficiente;
- o P02 é responsável pela correção final (avaliação de `regra_ativo` e
  estado lógico consultável, independente do rótulo).

## 7. Estado Git

```yaml
branch: master
HEAD: 721f8f1
stage: vazio
diff_check: limpo
```
