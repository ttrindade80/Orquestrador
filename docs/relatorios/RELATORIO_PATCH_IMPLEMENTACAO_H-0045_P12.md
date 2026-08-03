---
name: IMP-H0045-P12-metodo-adaptativo-validacao
description: "Delta factual do PATCH_IMPLEMENTACAO P12: harness adaptativo de validação (W/C), seis casos independentes, testes multi-geometria e PTY pelo ponto de entrada real"
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
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0045_P03.md
  achados_tratados:
    - PH-H0045-001
    - PH-H0045-002
    - PH-H0045-003
    - PH-H0045-004
    - PH-H0045-005
    - PH-H0045-006
    - QA-H0045-P02-001
    - QA-H0045-P02-002
---

# IMP-H0045-P12 — Método adaptativo de validação

> Relatório sucinto, factual. Não aprova formalmente a implementação.

## 1. Identificação e status

```yaml
handoff: H-0045 — paginação interativa limitada em console
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
status_normalizado: patched
```

## 2. Delta material

Harness de validação adaptativa (§18): conteúdo gerado em memória após resolução de `W`/`C` pelas autoridades do renderer; seis casos independentes executáveis pelo ponto de entrada real; provas automatizadas em múltiplas geometrias e PTY. Implementação funcional de paginação (P01–P11) preservada.

### Cadeia de patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0045_P03.md
achados_tratados:
  - PH-H0045-001
  - PH-H0045-002
  - PH-H0045-003
  - PH-H0045-004
  - PH-H0045-005
  - PH-H0045-006
  - QA-H0045-P02-001
  - QA-H0045-P02-002
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

### API do helper e geometria

```yaml
modulo: demo/casos_validacao_paginacao.py
api:
  - id_caso_de_entrada / esqueleto_de_caso
  - capacidade_fisica_efetiva(altura_interna) → C
  - resolver_largura_util_efetiva(elemento, largura, altura_interna, ...) → W
    # via mapa_fisico_de_itens (probe); sem fórmula própria
  - construir_caso_* / construir_caso / construir_e_aplicar / aplicar_caso_ao_modelo
W: largura util efetiva de conteudo (autoridade mapa_fisico_de_itens)
C: altura_interna de geometria_console
fluxo: geometria → W/C → helper → itens em memoria → processar_comando/renderizar_estado
```

### Seis casos e distinção PERMITIR × CONTINUAÇÃO

| ID | Entrada demo | Fenômeno |
|---|---|---|
| H0045-VAL-LARGURA | `h0045_validacao_largura` | linha lógica > W |
| H0045-VAL-PERMITIR | `h0045_validacao_permitir` | fragmentação; `altura > residuo`; **não** prova continuação pura |
| H0045-VAL-EVITAR | `h0045_validacao_evitar` | transferência inteira |
| H0045-VAL-CONDICIONAL | `h0045_validacao_condicional` | CABE ≤C e MAIOR >C |
| H0045-VAL-CONTINUACAO | `h0045_validacao_continuacao` | `≥2C+1`; marcadores CONT_*; entrada própria |
| H0045-VAL-VAZIO | `h0045_validacao_vazio` | `itens: []`; página 1/1 |

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: demo/casos_validacao_paginacao.py
    finalidade: helper puro dos seis casos adaptativos
  - caminho: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P12.md
    finalidade: este relatório
arquivos_alterados:
  - caminho: demo/demo.py
    delta: despacho h0045_validacao_*; resolve geometria; aplica/regenera caso
  - caminho: demo/teste_demo_paginacao.py
    delta: testes multi-geometria + PTY CONTINUACAO/VAZIO
  - caminho: tela/teste_paginacao.py
    delta: testes unitários adaptativos (C, políticas, continuação, vazio)
  - caminho: tela/teste_renderizador.py
    delta: largura, continuação sem cursor, vazio, autoridade geométrica
  - caminho: config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
    delta: metadados — esqueleto/regressão controlada, não prova universal
  - caminho: config/telas/demo/h0045_paginacao_politicas_quebra.json
    delta: idem
  - caminho: config/telas/demo/h0045_paginacao_conjunto_vazio.json
    delta: idem
```

## 4. Dados, temporários e saídas

```yaml
fixtures:
  - esqueletos ajustados (conteúdo estático de regressão controlada preservado)
  - conteúdo adaptativo apenas em memória
temporarios_operacionais: []
saidas_geradas:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P12.md
```

## 5. Verificações e evidência

```yaml
geometrias_testadas: [regular 80x24, estreita 50x24, alta 80x40, redimensionada]
verificacoes_executadas:
  - comando_ou_metodo: "pytest tela/teste_paginacao.py tela/teste_renderizador.py demo/teste_demo_paginacao.py -q"
    resultado_compacto: "379 passed"
    prova_semantica: "focais P12 + regressão P10/P11"
  - comando_ou_metodo: "pytest (suíte ampliada H-0045)"
    resultado_compacto: "590 passed"
  - comando_ou_metodo: "pytest (suíte completa)"
    resultado_compacto: "822 passed"
    prova_semantica: "antes do patch ~810; delta = novos testes P12"
  - comando_ou_metodo: "python demo/demo.py h0045_validacao_{largura,permitir,evitar,condicional,continuacao,vazio}"
    resultado_compacto: "exit 0; rótulo e marcadores no quadro"
  - comando_ou_metodo: "PTY automatizado CONTINUACAO+VAZIO"
    resultado_compacto: "pass; ponto de entrada real"
criterios_de_aceite:
  - {id: PI-H0045-P12-01, resultado: OK, evidencia: "resolver_largura_util_efetiva via mapa; sem fórmula duplicada"}
  - {id: PI-H0045-P12-02, resultado: OK, evidencia: "_aplicar_caso_validacao_adaptativo após geometria_console"}
  - {id: PI-H0045-P12-03, resultado: OK, evidencia: "seis construtores + entradas demo"}
  - {id: PI-H0045-P12-04, resultado: OK, evidencia: "PERMITIR altura_alvo ≠ 2C+1; nao_prova declarado"}
  - {id: PI-H0045-P12-05, resultado: OK, evidencia: "CONTINUACAO 2C+1 + CONT_* próprios"}
  - {id: PI-H0045-P12-06, resultado: OK, evidencia: "linha lógica > W; marcadores únicos"}
  - {id: PI-H0045-P12-07, resultado: OK, evidencia: "itens []"}
  - {id: PI-H0045-P12-08, resultado: OK, evidencia: "C=32 em altura 40 ainda produz continuação pura"}
  - {id: PI-H0045-P12-09, resultado: OK, evidencia: "subprocess demo/demo.py + PTY"}
  - {id: PI-H0045-P12-10, resultado: OK, evidencia: "manual não marcada"}
  - {id: PI-H0045-P12-11, resultado: OK, evidencia: "paginacao.py/renderizador.py funcionais intactos"}
  - {id: PI-H0045-P12-12, resultado: OK, evidencia: "822 passed"}
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
saida_observada: "rótulo do caso no cabeçalho/console; marcadores; página X/Y"
codigo_de_saida: 0
prova_semantica: "PTY + testes de integração; não substitui validação manual"
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
  - "Import do helper via importlib (caminho do arquivo): python demo/demo.py registra o script como módulo 'demo'."
observacoes_para_qa:
  - "Retomar somente 15/17..17/17; gabarito APROVADO|REPROVADO|NÃO OBSERVADO"
  - "6/17..14/17 preservadas — não reabrir"
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada: false
  resultado: null
  itens_pendentes:
    - "15/17 — LARGURA, PERMITIR, EVITAR, CONDICIONAL (separados)"
    - "16/17 — VAZIO"
    - "17/17 — CONTINUACAO"
```
