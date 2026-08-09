---
name: REL-PATCH-H-0053-P02-arvore-colapsavel
description: "Correção focal do redesenho após Espaço em arvore_colapsavel"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-08-08
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0053
  cadeia_raiz: IMP-0053-arvore-colapsavel
  predecessor_imediato: RELATORIO_VALIDACAO_MANUAL_H-0053
  achados_tratados:
    - H-0053-MANUAL-A
---

# REL-PATCH-H-0053-P02 — Correção focal

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
achado_tratado:
  id: H-0053-MANUAL-A
  requisito: Espaco_sobre_ramo_abre_ou_fecha
  evidencia: validacao_TTY_real_do_usuario
```

## 2. Cadeia

```yaml
raiz: IMP-0053-arvore-colapsavel
predecessor_imediato: RELATORIO_VALIDACAO_MANUAL_H-0053
achados_tratados:
  - H-0053-MANUAL-A
achados_resolvidos:
  - H-0053-MANUAL-A
achados_pendentes:
  - validacao_TTY_reexecutada_pelo_usuario
```

## 3. Causa técnica

A captura TTY preserva o literal `" "`, e o dispatch de
`demo/demo.py` já o encaminha para `navegacao.alternar_ramo`. O estado com
`ramos_fechados` também era retornado e propagado. A primeira fronteira
divergente era posterior: os loops TTY e não-TTY não consideravam a mudança
de `ramos_fechados` na decisão de redesenhar o quadro. Assim, a árvore mudava
em runtime, mas a tela permanecia com os descendentes visíveis.

## 4. Delta aplicado

```yaml
arquivos_alterados:
  - caminho: demo/demo.py
    delta: >-
      compara ramos_fechados antes/depois do comando e redesenha quando o
      estado de expansão/recolhimento muda nos dois loops de sessão.
  - caminho: demo/teste_demo_console.py
    delta: >-
      regressão pela fronteira do runner demo.demo_navegacao, com o literal
      " ", fechamento, permanência do cursor, renderização sem descendentes,
      reabertura e retorno dos descendentes.
arquivos_criados: []
```

## 5. Verificações

```yaml
testes_focais:
  - comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q
    resultado: 58_passed
  - comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console.py -q
    resultado: 8_passed
  - comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q
    resultado: 128_passed
suite_integral:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  resultado: 1069_passed
smoke:
  comando: >-
    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao
    --tela config/telas/demo/h0053_arvore_colapsavel.json
  resultado: codigo_0; arvore_aberta_renderizada; nao_prova_TTY
```

## 6. Bloqueios e pendências

```yaml
validacao_TTY: PENDENTE_DE_RETESTE
excecoes: []
bloqueios: []
stage: nao_executado
commit: nao_executado
```

Este relatório registra somente o delta do P02. QA pós-patch e nova
validação manual permanecem fora desta execução.
