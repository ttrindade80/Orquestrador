---
name: REL-QA-H0045-P14-validacao-estrita-W-C
description: "Auditoria pós-patch P14 da validação estrita de W e C"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-08-01
rastreabilidade:
  autorizacao_qa: QA_POS_PATCH
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P13.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
  achados_tratados:
    - QA-H0045-P13-001
---

# REL-QA-H0045-P14 — Auditoria pós-patch

## 1. Identificação e status

```yaml
revisao: H-0045 / PATCH_IMPLEMENTACAO P14
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: implementation_patch_required
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: validação estrita dos valores geométricos W e C
autoridades_materiais:
  - demo/casos_validacao_paginacao.py:56-148, 174-440
  - demo/demo.py:929-983
  - tela/renderizador.py:4134-4187
  - demo/teste_demo_paginacao.py:2503-2633
escopo:
  - domínio inteiro positivo exato e rejeição de tipos não inteiros
  - ordem da validação de W antes do mapa físico
  - coerções residuais nos construtores
  - preservação nominal P12/P13, PTY e validação manual pendente
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: limites_focais_W_C
    comando_ou_metodo: leitura focal e testes P14-01..P14-08
    evidencia_focal: "_exigir_dimensao_positiva usa type(valor) is int and valor > 0; capacidade devolve 16 por identidade; strings, floats, bool, None, zero, negativo, vazio, lista e dict levantam GeometriaEfetivaAusente; largura inválida não consulta mapa"
    resultado: OK
  - id: residuos_de_coercao
    comando_ou_metodo: busca de int() e chamada direta controlada dos construtores
    evidencia_focal: "demo/casos_validacao_paginacao.py:176,218,260,301,361,408 usa int(W); construir_caso('H0045-VAL-LARGURA', '80', 16), 80.0 e 80.9 devolve W=80"
    resultado: FALHA
  - id: suites_independentes
    comando_ou_metodo: pytest focal, focais H-0045, ampliado e completo
    evidencia_focal: "40, 394, 605 e 837 passed; P14 foi coletado integralmente; nenhuma falha, erro ou skip novo"
    resultado: OK
  - id: demos_e_preservacao
    comando_ou_metodo: seis comandos demo h0045_validacao_*
    evidencia_focal: "seis saídas com código 0, rótulos, marcadores, controles e indicadores de página; P12/P13, geometrias e PTY permanecem cobertos"
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0045-P14-001 | alto | PI-H0045-P14-04/05; domínio estrito de W sem coerção residual | Os construtores de `demo/casos_validacao_paginacao.py` convertem W com `int(W)` antes de impor a regra estrita. Chamada direta com `"80"`, `80.0` e `80.9` foi aceita como `W=80`. | Um consumidor que invoque diretamente a construção pode aceitar e normalizar string ou float geométrico inválido; a entrada não é rejeitada com `GeometriaEfetivaAusente`. | Validar W com a regra estrita antes de qualquer conversão em cada fronteira construtora, ou centralizar essa validação em `construir_caso`, sem ampliar o domínio por `int(W)`. |

## 5. Delta de QA pós-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P14.md
achados_tratados:
  - QA-H0045-P13-001
achados_resolvidos:
  - QA-H0045-P13-001
achados_pendentes:
  - QA-H0045-P14-001
novos_achados:
  - QA-H0045-P14-001
```

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest demo/teste_demo_paginacao.py -v
    resultado_compacto: 40 passed
    prova_semantica: P12/P13 e oito testes P14 coletados e aprovados.
  - comando_ou_metodo: suites focais H-0045, ampliada e completa
    resultado_compacto: 394, 605 e 837 passed
    prova_semantica: paginação, atomicidade, geometrias, PTY e regressões preservados.
demonstracao:
  resultado: seis entradas executadas com código 0
  evidencia: rótulos, marcadores, cursor inicial, controles e indicadores de página presentes; VAZIO sem conteúdo sintético.
validacao_manual:
  necessaria: true
  metodo_reproduzivel: VALIDACAO_MANUAL — retomar em 15/17
  resultado: pendente; não executada pelo QA
  criterios_pendentes:
    - 15/17: LARGURA, PERMITIR, EVITAR, CONDICIONAL
    - 16/17: VAZIO
    - 17/17: CONTINUACAO
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
  staged: vazio
  unstaged: worktree acumulado H-0045/P01-P14 e patches de handoff
  nao_rastreados: artefatos acumulados do handoff, P14 e este relatório
itens_inesperados: []
```

## 9. Conclusão

O patch corrige o achado P13 no caminho focal: W e C efetivos rejeitam tipos não inteiros, a largura é validada antes do mapa e os testes, demos, P12/P13 e PTY permanecem aprovados. Contudo, coerções `int(W)` residuais nos construtores ainda aceitam diretamente W externo inválido, produzindo o achado QA-H0045-P14-001. A validação manual continua pendente e não foi executada.
