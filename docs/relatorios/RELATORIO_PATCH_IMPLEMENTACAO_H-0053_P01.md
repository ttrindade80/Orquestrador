---
name: REL-PATCH-H-0053-P01-arvore-colapsavel
description: "Correção focal da implementação de H-0053"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-08-08
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0053
  cadeia_raiz: IMP-0053-arvore-colapsavel
  predecessor_imediato: RELATORIO_QA_IMPLEMENTACAO_H-0053
  achados_tratados:
    - H-0053-IMP-A
    - H-0053-IMP-B
---

# REL-PATCH-H-0053-P01 — Patch

> Relatório incremental do patch de implementação. Não substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
```

## 2. Cadeia

```yaml
raiz: IMP-0053-arvore-colapsavel
predecessor_imediato: RELATORIO_QA_IMPLEMENTACAO_H-0053
achados_tratados:
  - H-0053-IMP-A
  - H-0053-IMP-B
achados_resolvidos:
  - H-0053-IMP-A
  - H-0053-IMP-B
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: H-0053-IMP-A
    alteracao: >-
      Removido o ramos_fechados vazio da inicialização/transporte genérico;
      a demonstração H-0053 prepara explicitamente seu ramo de prova aberto
      como estado runtime transitório, sem campo no JSON.
  - id_achado: H-0053-IMP-B
    alteracao: >-
      Extraído o cálculo comum de linhas físicas por nó da apresentação
      hierarquia; o renderer e mapa_fisico_de_itens reutilizam essa fonte,
      incluindo modo verboso e ramos fechados.
arquivos_alterados:
  - caminho: demo/demo.py
    delta: Estado inicial genérico sem expansão e preparação exclusiva da fixture H-0053.
  - caminho: demo/teste_demo_console.py
    delta: Prova de preparação determinística, transitoriedade e ausência no JSON.
  - caminho: tela/renderizacao/conteudo_externo.py
    delta: Cálculo compartilhado das linhas produzidas por cada nó hierárquico.
  - caminho: tela/renderizacao/console.py
    delta: Mapa físico derivado das linhas efetivas do renderer.
  - caminho: tela/teste_navegacao.py
    delta: Regressão comportamental verbosa e paginada.
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q
    resultado_compacto: 58 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console.py -q
    resultado_compacto: 7 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q
    resultado_compacto: 128 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 1068 passed
  - comando_ou_metodo: smoke não-TTY da fixture H-0053 com demo.demo_navegacao --verboso
    resultado_compacto: código 0; árvore carregada/renderizada com ramo aberto e chip [✥] Navegar
  - comando_ou_metodo: validação TTY manual
    resultado_compacto: PENDENTE; executor exclusivo USUARIO_EM_TTY_REAL
```

Verificações locais não equivalem a QA independente.

## 5. Bloqueios e exceções

```yaml
excecoes: nenhuma
validacao_TTY_executada: false
stage: vazio
commit: false
```
