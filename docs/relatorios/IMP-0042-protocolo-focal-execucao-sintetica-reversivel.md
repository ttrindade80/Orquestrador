---
name: IMP-0042-protocolo-focal-execucao-sintetica-reversivel
description: "Resultado factual da implementação do protocolo focal de execução sintética reversível"
metadata:
  type: relatorio_implementacao
  tipo_execucao: IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-0042
  data: 2026-07-29
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_json_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  issues_relacionadas:
    - ITEM-0006
  bugs_abertos: []
  autorizacoes_operacionais:
    - "leitura focal adicional de docs/contratos/contrato_json_console.md §14 (1282–1636) e §12.1–§12.5 (515–774)"
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# IMP-0042 — Relatório de implementação

## 1. Identificação e status

```yaml
handoff: H-0042 — protocolo focal de execução sintética reversível
tipo_execucao: IMPLEMENTACAO
status_literal: IMPLEMENTED
status_normalizado: capacidade_focal_entregue_com_testes_e_demonstracoes
```

## 2. Delta material

- Motor focal compartilhado: validação atômica de `selecao_execucao.v1`, diretório temporário exclusivo, invocação por subprocesso sem shell, captura de código/`stdout`/`stderr`, preservação bruta de `resultado.json`, classificação (código `0` e JSON válido) e limpeza em `finally`.
- Executor sintético com CLI fechada (`--entrada`, `--resultado`, `--dry-run`), fixture irmã de `resultado.json`, semântica por item, documento multinível `conjuntos_campos`, aviso determinístico de sucesso sem mutação, controles sintéticos e interrupção com código `130`.
- Demonstração não interativa com `--fixture` exclusivo do ponto de entrada demonstrativo; inspeção antes da limpeza; baseline permanente intacta.
- Fixtures permanentes nominais criadas; nenhum arquivo existente alterado; chip `Executar` e H-0041 intocados.

## 3. Artefatos criados ou alterados

```yaml
diretorios_criados:
  - demo/fixtures/
arquivos_criados:
  - caminho: tela/execucao_focal.py
    finalidade: protocolo focal invocador
  - caminho: tela/teste_execucao_focal.py
    finalidade: testes unitários/integração do protocolo
  - caminho: demo/executor_sintetico.py
    finalidade: CLI sintética e documento multinível
  - caminho: demo/demo_execucao_focal.py
    finalidade: demonstração não interativa
  - caminho: demo/teste_executor_sintetico.py
    finalidade: testes focais do executor
  - caminho: demo/teste_demo_execucao_focal.py
    finalidade: testes da demonstração
  - caminho: demo/fixtures/h0042_fixture_execucao.json
    finalidade: baseline permanente
  - caminho: demo/fixtures/h0042_entrada_sucesso.json
    finalidade: entrada mista sucesso
  - caminho: demo/fixtures/h0042_entrada_sucesso_aviso.json
    finalidade: entrada somente item_03 (CA-09)
  - caminho: demo/fixtures/h0042_entrada_parcial.json
    finalidade: entrada parcial
  - caminho: demo/fixtures/h0042_entrada_falha_operacional.json
    finalidade: controle falha operacional
  - caminho: demo/fixtures/h0042_entrada_resultado_invalido.json
    finalidade: controle resultado inválido
  - caminho: demo/fixtures/h0042_entrada_interrupcao.json
    finalidade: controle interrupção
  - caminho: docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
    finalidade: este relatório
arquivos_alterados: []
arquivos_removidos: []
```

## 4. Dados, temporários e saídas

```yaml
entradas_reais: []
fixtures:
  - demo/fixtures/h0042_fixture_execucao.json
  - demo/fixtures/h0042_entrada_*.json
configuracoes: []
temporarios_operacionais:
  - diretorio_exclusivo_por_invocacao_com_entrada_resultado_fixture_trabalho
caches: []
saidas_geradas:
  - docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
politica_de_sobrescrita_observada: nenhum_resultado_json_permanente
limpeza_realizada: >-
  temporários removidos em finally; nenhum h0042_focal_* residual em /tmp;
  __pycache__ de execução removido
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >-
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_execucao_focal.py demo/teste_executor_sintetico.py
      demo/teste_demo_execucao_focal.py
    resultado_compacto: 58 passed
    prova_semantica: CA-01 a CA-15 cobertos nos testes focais
  - comando_ou_metodo: >-
      PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
      tela/teste_selecao.py demo/teste_demo_selecao.py
    resultado_compacto: 35 passed
    prova_semantica: regressão H-0041 sem alteração de interface
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 617 passed
    prova_semantica: suíte completa sem regressão
criterios_de_aceite:
  - id: CA-01
    evidencia: teste integração sucesso multinível
    resultado: OK
  - id: CA-02
    evidencia: rejeições estruturais sem mutação
    resultado: OK
  - id: CA-03
    evidencia: dry-run fixture inalterada
    resultado: OK
  - id: CA-04
    evidencia: mutação só na cópia; baseline intacta
    resultado: OK
  - id: CA-05
    evidencia: item_03 ignorado
    resultado: OK
  - id: CA-06
    evidencia: parcial com código 0
    resultado: OK
  - id: CA-07
    evidencia: ordem dos IDs preservada
    resultado: OK
  - id: CA-08
    evidencia: stdout JSON-like ignorado; leitura de resultado.json
    resultado: OK
  - id: CA-09
    evidencia: aviso stderr exato; status sucesso; sem mutação
    resultado: OK
  - id: CA-10
    evidencia: falha operacional código ≠ 0
    resultado: OK
  - id: CA-11
    evidencia: texto inválido preservado byte a byte
    resultado: OK
  - id: CA-12
    evidencia: JSON interrompido; código 130
    resultado: OK
  - id: CA-13
    evidencia: limpeza em todos os términos
    resultado: OK
  - id: CA-14
    evidencia: hash baseline idêntico após suíte e demos
    resultado: OK
  - id: CA-15
    evidencia: controles ausentes da baseline; tratamento distinto
    resultado: OK
  - id: CA-16
    evidencia: nenhum arquivo H-0041 alterado; regressão OK
    resultado: OK
  - id: CA-17
    evidencia: git status restrito a nominais + docs do ciclo
    resultado: OK
  - id: CA-18
    evidencia: 617 passed
    resultado: OK
```

## 6. Demonstração operacional

```yaml
cwd: "."
comandos:
  - dry_run: demo.demo_execucao_focal --entrada ...sucesso.json --fixture ... --dry-run
  - real: idem sem --dry-run
  - aviso: ...sucesso_aviso.json
  - parcial: ...parcial.json
  - falha: ...falha_operacional.json
  - invalido: ...resultado_invalido.json
  - interrupcao: ...interrupcao.json
saida_observada:
  dry_run: "codigo 0; status sucesso; cópia inalterada; limpeza OK"
  real: "codigo 0; item_01 processado na cópia; stderr vazio"
  aviso: "codigo 0; stderr AVISO...; sem mutação"
  parcial: "codigo 0; status parcial; classificacao sucesso"
  falha: "codigo 1; classificacao falha"
  invalido: "codigo 0; classificacao falha (JSON inválido)"
  interrupcao: "codigo 130; status interrompido; mutação prévia observável"
comparacao_com_esperado: conforme
prova_semantica: >-
  baseline hash invariante; temporários removidos; canais e status
  conferidos semanticamente em cada cenário
codigo_de_saida: "0|0|0|0|1|0|130"
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: f4b5df1
staged: []
unstaged:
  - docs acumulados do ciclo ADR-0035/H-0042 (pré-existentes)
nao_rastreados:
  - arquivos nominais H-0042 criados nesta execução
  - docs/relatorios/IMP-0042-...
divergencias_materiais: []
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - >-
    Leitura focal adicional do contrato §14 e §12.1–§12.5 foi autorizada
    explicitamente antes da implementação; nenhum outro trecho contratual
    foi lido.
observacoes_para_qa:
  - >-
    CA-09 depende exclusivamente do estado processado:true dos IDs normais
    (item_03), sem flag, env, ID reservado ou nome de arquivo.
  - >-
    Classificação de processo (código 0 ∧ JSON válido) é independente do
    status semântico interno (sucesso/parcial/interrompido).
validacao_manual:
  executor_exclusivo_quando_TTY: NAO_APLICAVEL_EVIDENCIA_AUTOMATIZADA
  necessaria: false
  executada: false
  resultado: null
  itens_pendentes: []
```
