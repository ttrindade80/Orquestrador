---
name: RELATORIO_PATCH_IMPLEMENTACAO_H-0042_P01
description: "Delta factual do patch P01 da implementação H-0042"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_COMPLETED
  data: 2026-07-29
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0042
  cadeia_raiz: H-0042
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0042.md
  achados_tratados:
    - ACH-H0042-01
    - ACH-H0042-02
    - ACH-H0042-03
---

# RELATORIO_PATCH_IMPLEMENTACAO_H-0042_P01 — Patch

> Relatório incremental. Registre somente o delta desta execução.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_COMPLETED
patch: H-0042-P01
```

## 2. Cadeia

```yaml
raiz: H-0042
predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0042.md
achados_tratados:
  - ACH-H0042-01
  - ACH-H0042-02
  - ACH-H0042-03
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: ACH-H0042-01
    alteracao: >-
      Removido argv_executor da API produtiva; invocação fixa
      [sys.executable, -m, demo.executor_sintetico] com shell=False;
      substituição de subprocesso apenas via monkeypatch privado de teste.
  - id_achado: ACH-H0042-02
    alteracao: >-
      Separadas existência, validade sintática e validade semântica do
      resultado; classificar_processo exige documento H-0042 (§12+§14.9)
      para sucesso externo; bruto preservado sem reserialização.
  - id_achado: ACH-H0042-03
    alteracao: >-
      Demonstrador deriva expectativa dos ids; retorna 0 quando o cenário
      esperado é comprovado; resumo preserva codigo_saida observado do
      executor (1, 0, 130).
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0042_P01.md
arquivos_alterados:
  - caminho: tela/execucao_focal.py
    delta: executor fechado + validação semântica + classificação
  - caminho: tela/teste_execucao_focal.py
    delta: provas ACH-01 e ACH-02
  - caminho: demo/demo_execucao_focal.py
    delta: código do demonstrador vs observado
  - caminho: demo/teste_demo_execucao_focal.py
    delta: provas ACH-03
arquivos_removidos: []
```

### Fechamento do executor autorizado

Caminho produtivo exclusivo: `sys.executable -m demo.executor_sintetico`.
Tentativa de `argv_executor` rejeitada (`TypeError`). Sem executável,
módulo, string ou caminho configurável alternativos.

### Validação semântica

Camadas: `resultado_existente`, `resultado_json_sintaticamente_valido`,
`resultado_semanticamente_valido`, `classificacao_externa`. `{}`, `[]`,
tipo/apresentação/níveis incorretos, resumo/itens ausentes e registro
incompleto → falha externa. `parcial` válido com código 0 → sucesso
externo. Interrupção (130) → falha externa mesmo com JSON válido.

### Semântica de retorno do demonstrador

`codigo_observado` (executor) ≠ `codigo_do_demonstrador` (conformidade do
cenário). Expectativa só por conteúdo de `ids`.

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: pytest focal (tela + demo H-0042)
    resultado_compacto: 80 passed
  - comando_ou_metodo: pytest regressivo H-0041
    resultado_compacto: 35 passed
  - comando_ou_metodo: pytest completo
    resultado_compacto: 639 passed
  - comando_ou_metodo: sete demonstrações nominais
    resultado_compacto: >-
      7/7 codigo_demonstrador=0; observados 1/0/130 nos cenários
      falha/inválido/interrupção; semanticamente_valido False no inválido
  - comando_ou_metodo: higiene temporários e stage
    resultado_compacto: >-
      sem h0042_focal_* em /tmp; sem resultado.json permanente; stage
      vazio; baseline intacta
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
desvios: []
```
