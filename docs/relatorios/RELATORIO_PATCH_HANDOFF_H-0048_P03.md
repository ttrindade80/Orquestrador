---
name: REL-PATCH-0048-P03-correcao-lista-symbols-coletaveis-8-3
description: "Remove comum.py da lista de módulos com __all__ coletável na seção 8.3 do H-0048"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: 2026-08-03
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
  cadeia_raiz: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0048_P02.md
  achados_tratados:
    - H0048-HANDOFF-QA-P02-001
---

# REL-PATCH-0048-P03 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0048_P02.md
achados_tratados:
  - H0048-HANDOFF-QA-P02-001
achados_resolvidos:
  - H0048-HANDOFF-QA-001
  - H0048-HANDOFF-QA-002
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: H0048-HANDOFF-QA-P02-001
    alteracao: >
      Na seção 8.3 (Direção de imports), removida a linha
      "tela/testes_renderizador/comum.py" da lista de módulos cujos
      __all__ fornecem símbolos coletáveis à fachada
      tela/teste_renderizador.py. A lista passou a conter exatamente
      os oito módulos proprietários (fundamentos.py, barra_menus.py,
      composicao_corpo.py, matriz_participantes.py, lancador.py,
      conteudo_externo.py, selecao.py, integracao.py). Preservadas
      imediatamente abaixo as linhas de _fixture_h0041_qa002 e main,
      e preservado o bloco de direção de dependências que já listava
      comum.py como consumido por runner.py e pelos módulos
      proprietários.
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
    delta: >
      Seção 8.3: remoção de uma linha (comum.py) da lista de módulos
      com símbolos coletáveis por __all__. Nenhuma outra seção foi
      tocada.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: rg -n -A12 -B2 'símbolos coletáveis declarados nos __all__' docs/handoff/H-0048-...md
    resultado_compacto: lista contém exatamente os oito módulos proprietários; comum.py ausente; fixture e main preservados abaixo
  - comando_ou_metodo: git status --short --untracked-files=all
    resultado_compacto: stage vazio; nenhum arquivo além do H-0048 e do relatório P03 foi tocado; não rastreados preexistentes e .pyc intactos
  - comando_ou_metodo: git diff --check
    resultado_compacto: sem conflitos de whitespace
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
