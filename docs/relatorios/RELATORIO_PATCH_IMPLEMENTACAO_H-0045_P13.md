---
name: IMP-H0045-P13-remocao-fallbacks-geometricos
description: "Delta factual do PATCH_IMPLEMENTACAO P13: remoção dos fallbacks altura-8 e largura 80 no harness adaptativo (QA-H0045-P12-001)"
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
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P12.md
  achados_tratados:
    - QA-H0045-P12-001
---

# IMP-H0045-P13 — Remoção de fallbacks geométricos

> Relatório sucinto, factual. Não aprova formalmente a implementação.

## 1. Identificação e status

```yaml
handoff: H-0045 — paginação interativa limitada em console
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
status_normalizado: patched
```

## 2. Delta material

Removidos os dois caminhos incompatíveis com o método adaptativo (§18): cálculo de capacidade por `altura - 8` em `demo/demo.py` e substituição de largura ausente por `80` em `demo/casos_validacao_paginacao.py`. Ausência de geometria/W/C passa a rejeição explícita via `GeometriaEfetivaAusente` (helper local), com construção antes da mutação definitiva e restauração do esqueleto em falha. Seis casos P12, PTY e implementação funcional de paginação preservados.

### Cadeia de patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P12.md
achados_tratados:
  - QA-H0045-P12-001
achados_resolvidos:
  - QA-H0045-P12-001
achados_pendentes: []
novos_achados: []
```

### Fallbacks removidos e erro

```yaml
removidos:
  - demo/demo.py: fallback C ≈ altura - 8 quando geometria_console retorna None
  - demo/casos_validacao_paginacao.py: limite = largura_console or 80
comportamento_ausencia:
  - GeometriaEfetivaAusente com mensagem "geometria efetiva do console nao resolvida"
  - capacidade_fisica_efetiva / resolver_largura_util_efetiva rejeitam None, bool, 0, negativo, tipo incompatível
  - atomicidade: itens do esqueleto restaurados; aplicar_caso_ao_modelo só após W/C resolvidos
```

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
    finalidade: este relatório
arquivos_alterados:
  - caminho: demo/casos_validacao_paginacao.py
    delta: GeometriaEfetivaAusente; validação estrita de C e largura; sem 80
  - caminho: demo/demo.py
    delta: _aplicar_caso_validacao_adaptativo rejeita geometria None; atomicidade
  - caminho: demo/teste_demo_paginacao.py
    delta: testes P13-01..P13-08 (negativos + nominal + multi-geometria)
```

## 4. Dados, temporários e saídas

```yaml
fixtures: []  # esqueletos P12 intactos
temporarios_operacionais: []
saidas_geradas:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "rg fallbacks (altura-8|or 80) em demo.py e helper"
    resultado_compacto: "sem ocorrência funcional; restos só em comentários de proibição / get_terminal_size"
    prova_semantica: "caminhos de construção não inventam W/C"
  - comando_ou_metodo: "pytest demo/teste_demo_paginacao.py -v"
    resultado_compacto: "32 passed (7 novos P13)"
  - comando_ou_metodo: "pytest focais H-0045"
    resultado_compacto: "386 passed"
  - comando_ou_metodo: "pytest suíte ampliada"
    resultado_compacto: "597 passed"
  - comando_ou_metodo: "pytest suíte completa"
    resultado_compacto: "829 passed (822 + 7 P13; sem skips novos)"
  - comando_ou_metodo: "seis demos h0045_validacao_*"
    resultado_compacto: "exit 0; rótulo, marcadores, página"
criterios_de_aceite:
  - {id: PI-H0045-P13-01, resultado: OK, evidencia: "sem altura-8 funcional"}
  - {id: PI-H0045-P13-02, resultado: OK, evidencia: "sem or 80 no helper"}
  - {id: PI-H0045-P13-03, resultado: OK, evidencia: "P13-01/06: modelo intacto após erro"}
  - {id: PI-H0045-P13-04, resultado: OK, evidencia: "P13-02..05 rejeitam inválidos"}
  - {id: PI-H0045-P13-05, resultado: OK, evidencia: "C=altura_interna da autoridade"}
  - {id: PI-H0045-P13-06, resultado: OK, evidencia: "P13-07 + demos seis casos"}
  - {id: PI-H0045-P13-07, resultado: OK, evidencia: "P13-08 regular/estreita/alta"}
  - {id: PI-H0045-P13-08, resultado: OK, evidencia: "P12 PTY e testes intactos"}
  - {id: PI-H0045-P13-09, resultado: OK, evidencia: "paginacao/renderizador não alterados"}
  - {id: PI-H0045-P13-10, resultado: OK, evidencia: "manual não executada"}
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
prova_semantica: "rótulo + marcadores/página; sem fallback"
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
staged: vazio
commit_realizado: false
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - "Import do helper via importlib permanece (P12); testes P13 usam casos_val do demo.demo quando checam a exceção do fluxo."
observacoes_para_qa:
  - "Achado QA-H0045-P12-001 tratado; validação manual ainda pendente."
  - "Retomar somente em 15/17; não reabrir 6/17..14/17."
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
