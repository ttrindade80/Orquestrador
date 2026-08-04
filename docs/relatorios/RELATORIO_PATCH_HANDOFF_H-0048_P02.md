---
name: REL-PATCH-0048-P02-handoff
description: "Patch do H-0048: registro da fixture pela fachada via importação nominal e substituição do compileall por compilação/importação em memória"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: 2026-08-03
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0048-reorganizacao-estrutural-dos-testes-do-renderizador
  cadeia_raiz: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0048.md
  achados_tratados:
    - H0048-HANDOFF-QA-001
    - H0048-HANDOFF-QA-002
---

# REL-PATCH-0048-P02 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0048.md
achados_tratados:
  - H0048-HANDOFF-QA-001
  - H0048-HANDOFF-QA-002
achados_resolvidos:
  - H0048-HANDOFF-QA-001
  - H0048-HANDOFF-QA-002
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: H0048-HANDOFF-QA-001
    alteracao: >
      A fixture `_fixture_h0041_qa002` permanece com proprietário único em
      `selecao.py`, sem duplicação, renomeação ou wrapper. A fachada
      `tela/teste_renderizador.py` passa a autorizar explicitamente a
      importação nominal `from tela.testes_renderizador.selecao import
      _fixture_h0041_qa002 as _fixture_h0041_qa002`, exclusivamente para que
      o pytest registre o objeto no namespace da fachada. A fixture não
      integra nenhum `__all__`. Nenhum `conftest.py`, plugin ou nova
      infraestrutura de fixtures foi introduzido. Reconciliadas as seções
      6.4, 8.2 (selecao.py e fachada), 8.3 (diagrama de imports), 12
      (critérios 16-21), 13.3, 14.4 (provas focais `-k 'qah0041_002'` e
      execução direta de `selecao.py`, 30 passed), 15, 17.3 e 19.
  - id_achado: H0048-HANDOFF-QA-002
    alteracao: >
      Removido o comando `python -m compileall` da seção 14.1, pois grava
      bytecode em disco mesmo com `PYTHONDONTWRITEBYTECODE=1`. Substituído
      por compilação inteiramente em memória (`compile(..., dont_inherit=True)`
      sobre os 12 arquivos do subpacote e da fachada) e por uma prova
      separada de importação real via `importlib.import_module` dos 11
      módulos. Acrescentada prova de ausência de resíduos em
      `tela/testes_renderizador/` após compilação, importação e testes.
      Reconciliadas as seções 10 (temporários), 12 (critério 22), 13.4,
      14.1, 15, 17.2 e 17.3.
arquivos_criados: []
arquivos_alterados:
  - caminho: docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
    delta: >
      Seções 6.4, 8.2, 8.3, 10, 12, 13.3, 13.4, 14.1, 14.4, 15, 17.2, 17.3 e
      19 corrigidas conforme os dois achados do QA; nenhuma outra seção,
      contagem, arquitetura ou nomenclatura foi alterada.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: grep "compileall" no handoff patcheado
    resultado_compacto: única ocorrência restante é a frase que proíbe seu uso; nenhum comando compileall é mais executado
  - comando_ou_metodo: leitura integral do documento patcheado
    resultado_compacto: fixture com proprietário único preservado; importação nominal explícita na fachada; compilação/importação em memória sem resíduos
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```
