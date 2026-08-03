---
name: IMP-H0045-P14-validacao-estrita-W-C
description: "Delta factual do PATCH_IMPLEMENTACAO P14: validação estrita de W e C sem coerção (QA-H0045-P13-001)"
metadata:
  type: relatorio_implementacao
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  handoff_origem: H-0045
  data: 2026-08-01
rastreabilidade:
  contrato_alvo: null
  adr_relacionadas:
    - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  issues_relacionadas:
    - ITEM-0003
  bugs_abertos: []
  autorizacoes_operacionais: []
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P13.md
  achados_tratados:
    - QA-H0045-P13-001
---

# IMP-H0045-P14 — Validação estrita de W e C

> Relatório sucinto, factual. Não aprova formalmente a implementação.

## 1. Identificação e status

```yaml
handoff: H-0045 — paginação interativa limitada em console
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
status_normalizado: patched
```

## 2. Delta material

Removida a coerção `int(valor)` de `_exigir_dimensao_positiva` no helper adaptativo. Capacidade e largura passam a aceitar somente `type(valor) is int and valor > 0`, devolvendo o mesmo inteiro sem normalização. Strings numéricas, floats (integrais ou fracionários), bool, None, zero, negativo, vazio, lista e dict são rejeitados com `GeometriaEfetivaAusente`. Largura inválida aborta antes de consultar `mapa_fisico_de_itens`. Fallbacks P13, atomicidade, seis casos, PTY e runtime funcional preservados.

### Cadeia de patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P13.md
achados_tratados:
  - QA-H0045-P13-001
achados_resolvidos:
  - QA-H0045-P13-001
achados_pendentes: []
novos_achados: []
```

### Regra de tipo e coerções removidas

```yaml
regra: type(valor) is int and valor > 0
coercoes_removidas:
  - int(valor) em _exigir_dimensao_positiva
aceitos: [1, 16, 80]
rejeitados: ["16", 16.0, 16.9, "80", 80.0, 80.9, null, true, false, 0, -1, "", [], {}]
mapa_fisico_em_largura_invalida: nao_consultado
int_residual_fora_validacao_geometrica:
  - "linhas = int(mapa[0]['linhas_fisicas']) — leitura do mapa, nao entrada W/C"
  - "int(W)/int(n) nos construtores de caso — pos-resolucao, nao aceitacao geometrica"
```

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
    finalidade: este relatório
arquivos_alterados:
  - caminho: demo/casos_validacao_paginacao.py
    delta: _exigir_dimensao_positiva sem coerção; domínio int exato positivo
  - caminho: demo/teste_demo_paginacao.py
    delta: testes P14-01..P14-08 (negativos + identidade + domínio)
```

## 4. Dados, temporários e saídas

```yaml
fixtures: []
temporarios_operacionais: []
saidas_geradas:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "rg int(|float(|fallbacks em demo/casos_validacao_paginacao.py"
    resultado_compacto: "sem coerção em _exigir_dimensao_positiva; int residual só fora da validação W/C"
    prova_semantica: "aceita somente int exato positivo"
  - comando_ou_metodo: "pytest demo/teste_demo_paginacao.py -v"
    resultado_compacto: "40 passed (8 novos P14)"
  - comando_ou_metodo: "pytest focais H-0045"
    resultado_compacto: "394 passed"
  - comando_ou_metodo: "pytest suíte ampliada"
    resultado_compacto: "605 passed"
  - comando_ou_metodo: "pytest suíte completa"
    resultado_compacto: "837 passed (829 + 8 P14; sem skips novos)"
  - comando_ou_metodo: "seis demos h0045_validacao_*"
    resultado_compacto: "exit 0; rótulo, marcadores, página"
criterios_de_aceite:
  - {id: PI-H0045-P14-01, resultado: OK, evidencia: "P14-01..03 + identidade 16→16"}
  - {id: PI-H0045-P14-02, resultado: OK, evidencia: "P14-04..06 + P14-07 W=80"}
  - {id: PI-H0045-P14-03, resultado: OK, evidencia: "P14-08 True/False"}
  - {id: PI-H0045-P14-04, resultado: OK, evidencia: "P14-01/04 strings"}
  - {id: PI-H0045-P14-05, resultado: OK, evidencia: "P14-02/03/05/06 floats"}
  - {id: PI-H0045-P14-06, resultado: OK, evidencia: "assert_not_called mapa P14-04..06"}
  - {id: PI-H0045-P14-07, resultado: OK, evidencia: "P14-07 call_count>=1"}
  - {id: PI-H0045-P14-08, resultado: OK, evidencia: "P12/P13/PTY intactos"}
  - {id: PI-H0045-P14-09, resultado: OK, evidencia: "runtime nao alterado"}
  - {id: PI-H0045-P14-10, resultado: OK, evidencia: "manual nao executada"}
```

## 6. Demonstração operacional

```yaml
cwd: "."
comando:
  - python demo/demo.py h0045_validacao_largura
  - python demo/demo.py h0045_validacao_permitir
  - python demo/demo.py h0045_validacao_evitar
  - python demo/demo.py h0045_validacao_condicional
  - python demo/demo.py h0045_validacao_continuacao
  - python demo/demo.py h0045_validacao_vazio
codigo_de_saida: 0
prova_semantica: "rótulo + marcadores/página; caminho geométrico int válido; sem coerção/fallback"
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
staged: vazio
commit_realizado: false
atribuiveis_ao_P14:
  - demo/casos_validacao_paginacao.py
  - demo/teste_demo_paginacao.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - "int(...) residual nos construtores e na leitura de linhas_fisicas nao participa da aceitacao geometrica de W/C."
observacoes_para_qa:
  - "Achado QA-H0045-P13-001 tratado; P12/P13 e demos positivas preservados."
  - "Retomar somente em 15/17; nao reabrir 6/17..14/17."
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada: false
  resultado: null
  itens_pendentes:
    - "15/17 — LARGURA, PERMITIR, EVITAR, CONDICIONAL (separados)"
    - "16/17 — VAZIO"
    - "17/17 — CONTINUACAO"
  retomada_futura: "15/17"
```
