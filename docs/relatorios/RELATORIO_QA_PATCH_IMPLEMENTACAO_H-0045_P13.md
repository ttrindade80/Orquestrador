---
name: REL-QA-H0045-P13-remocao-fallbacks-geometricos
description: "Auditoria pós-patch P13 do harness adaptativo"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-08-01
rastreabilidade:
  autorizacao_qa: QA_POS_PATCH
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P12.md
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
  achados_tratados:
    - QA-H0045-P12-001
---

# REL-QA-H0045-P13 — Auditoria pós-patch

## 1. Identificação e status

```yaml
revisao: H-0045 / PATCH_IMPLEMENTACAO P13
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: implementation_patch_required
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: remoção dos fallbacks geométricos no harness adaptativo
autoridades_materiais:
  - docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md §18
  - tela/renderizador.py: assinaturas de geometria_console, mapa_fisico_de_itens e largura_util_itens_console
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
escopo:
  - fallbacks de capacidade e largura
  - rejeição de geometria inválida
  - atomicidade e preservação funcional do P12
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: fallbacks_e_fluxo_atomico
    comando_ou_metodo: leitura focal e buscas autorizadas em demo/demo.py e demo/casos_validacao_paginacao.py
    evidencia_focal: não há caminho funcional altura - 8 nem largura substituta 80; fluxo resolve geometria, C, W e constrói antes de aplicar; restauração ocorre em finally
    resultado: OK
  - id: erro_e_validacao_geometrica
    comando_ou_metodo: leitura do helper, fluxo da demo, testes P13 e reteste independente de tipos
    evidencia_focal: GeometriaEfetivaAusente é local, objetiva e preserva o modelo para ausência; bool, None, zero, negativo, vazio e objeto incompatível são rejeitados, mas string numérica e float são convertidos por int(valor)
    resultado: FALHA
  - id: suites
    comando_ou_metodo: pytest focal, focais H-0045, ampliado e completo
    evidencia_focal: 32 passed; 386 passed; 597 passed; 829 passed
    resultado: OK
  - id: demonstracoes_e_pty
    comando_ou_metodo: seis entradas h0045_validacao_* e testes PTY P12/P13
    evidencia_focal: seis demonstrações com código 0, rótulos, marcadores, página e controles; CONTINUACAO, VAZIO e resize aprovados pelo caminho real
    resultado: OK
  - id: estado_git
    comando_ou_metodo: branch, HEAD, status e stage somente leitura
    evidencia_focal: master; b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; worktree acumulado anterior ao QA
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0045-P13-001 | alto | PI-H0045-P13-04; validação estrita de C/W | `demo/casos_validacao_paginacao.py:56-83` usa `int(valor)`; reteste aceitou capacidade `"16"` e `16.9`, e largura `"80"` e `80.9` | Entradas que não são inteiros positivos efetivamente resolvidos podem ser aceitas e normalizadas, violando a rejeição explícita e a autoridade geométrica | Exigir tipo inteiro positivo, sem coerção de strings, floats ou outros tipos; adicionar provas negativas nominais para esses tipos |

## 5. Delta de QA pós-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P13.md
achados_tratados:
  - QA-H0045-P12-001
achados_resolvidos: []
achados_pendentes:
  - QA-H0045-P12-001
  - QA-H0045-P13-001
novos_achados:
  - QA-H0045-P13-001
```

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest focal, focais H-0045, ampliado e completo
    resultado_compacto: 32, 386, 597 e 829 passed
    prova_semantica: casos P13, seis casos positivos, três geometrias, PTY, resize e regressões preservados
  - comando_ou_metodo: reteste direto dos helpers com string, float e objeto
    resultado_compacto: string numérica e float aceitos; objeto incompatível rejeitado
    prova_semantica: lacuna confirma o achado QA-H0045-P13-001
demonstracao:
  resultado: seis entradas concluídas com código 0
  evidencia: rótulos corretos, marcadores adaptativos, indicadores de página, cursor e controles sem fallback
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
  unstaged: worktree acumulado H-0045/P01-P13 e patches de handoff
  nao_rastreados: artefatos acumulados do handoff e P13; relatório deste QA criado somente nesta auditoria
itens_inesperados: []
```

## 9. Conclusão

Os fallbacks geométricos foram removidos, a atomicidade, os caminhos positivos, as geometrias válidas, o PTY e a paginação aprovada no P12 permanecem funcionais. Entretanto, a validação prometida como estrita ainda aceita string numérica e float por coerção. O achado impede aprovação técnica do patch; a validação manual permanece pendente e não foi executada.
