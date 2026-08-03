---
name: IMP-H0045-P15-remocao-coercoes-residuais-W
description: "Delta factual do PATCH_IMPLEMENTACAO P15: remoção das coerções int(W) residuais nas fronteiras construtoras (QA-H0045-P14-001)"
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
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P14.md
  achados_tratados:
    - QA-H0045-P14-001
---

# IMP-H0045-P15 — Remoção das coerções residuais de W

> Relatório sucinto, factual. Não aprova formalmente a implementação.

## 1. Identificação e status

```yaml
handoff: H-0045 — paginação interativa limitada em console
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
status_normalizado: patched
```

## 2. Delta material

Removidas as sete ocorrências de `int(W)` em `demo/casos_validacao_paginacao.py`: nos seis construtores diretamente invocáveis (`construir_caso_largura`, `_permitir`, `_evitar`, `_condicional`, `_continuacao`, `_vazio`) e no helper interno `_token_linha`. Cada construtor agora chama `_exigir_dimensao_positiva(W, "W")` como primeira operação, antes de qualquer cálculo, concatenação ou criação de item — mesmo domínio estrito já usado por `capacidade_fisica_efetiva`/`resolver_largura_util_efetiva`. `construir_caso_vazio` preserva a assinatura `W=None` (caso não necessite materialmente de W); quando `W` é fornecido, passa pela mesma validação estrita. `_token_linha` deixou de reconverter `W`: recebe sempre um inteiro já validado pelo construtor chamador (`w = W`, sem `max`/`int`).

### Cadeia de patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P14.md
achados_tratados:
  - QA-H0045-P14-001
achados_resolvidos:
  - QA-H0045-P14-001
achados_pendentes: []
novos_achados: []
```

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P15.md
    finalidade: este relatório
arquivos_alterados:
  - caminho: demo/casos_validacao_paginacao.py
    delta: remoção de int(W)/max(1,int(W)) em 6 construtores e em _token_linha; validação estrita via _exigir_dimensao_positiva
  - caminho: demo/teste_demo_paginacao.py
    delta: testes P15-01..P15-08 (rejeição direta dos construtores + despacho genérico + atomicidade)
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "rg int\\(W\\)|float\\(W\\)|str\\(W\\)|W\\s*=\\s*int\\( em demo/casos_validacao_paginacao.py"
    resultado_compacto: "nenhuma ocorrência"
    prova_semantica: "int_W_funcional: nenhuma_ocorrencia"
  - comando_ou_metodo: "rg def construir_caso_|def construir_caso\\(|_exigir_dimensao_positiva"
    resultado_compacto: "todas as 6 fronteiras chamam _exigir_dimensao_positiva antes do uso de W"
  - comando_ou_metodo: "pytest demo/teste_demo_paginacao.py -v"
    resultado_compacto: "48 passed (8 novos P15)"
  - comando_ou_metodo: "pytest focais H-0045"
    resultado_compacto: "402 passed"
  - comando_ou_metodo: "pytest suíte ampliada"
    resultado_compacto: "613 passed"
  - comando_ou_metodo: "pytest suíte completa"
    resultado_compacto: "845 passed (837 + 8 P15; sem skips novos, sem falhas)"
  - comando_ou_metodo: "seis demos h0045_validacao_*"
    resultado_compacto: "exit 0; rótulo, marcadores, [<]/[>], indicador de página presentes"
criterios_de_aceite:
  - {id: PI-H0045-P15-01, resultado: OK, evidencia: "busca rg sem ocorrências de int/float/str(W)"}
  - {id: PI-H0045-P15-02, resultado: OK, evidencia: "6 construtores chamam _exigir_dimensao_positiva antes do uso"}
  - {id: PI-H0045-P15-03, resultado: OK, evidencia: "P15-07 construir_caso rejeita string/float para os 6 IDs"}
  - {id: PI-H0045-P15-04, resultado: OK, evidencia: "P15-01/02/03 rejeitam string/float por construtor"}
  - {id: PI-H0045-P15-05, resultado: OK, evidencia: "P15-04 rejeita True/False"}
  - {id: PI-H0045-P15-06, resultado: OK, evidencia: "P15-06 W=80 preserva W_registrado=80, type int"}
  - {id: PI-H0045-P15-07, resultado: OK, evidencia: "P15-08 mock de _item nunca chamado com W inválido"}
  - {id: PI-H0045-P15-08, resultado: OK, evidencia: "845 passed inclui P12-P14 e PTY intactos"}
  - {id: PI-H0045-P15-09, resultado: OK, evidencia: "runtime funcional (tela/*) não alterado; seis demos exit 0"}
  - {id: PI-H0045-P15-10, resultado: OK, evidencia: "validação manual não executada neste patch"}
```

Ressalva de domínio: `construir_caso_vazio(W=None)` preserva `None` como estado válido (ausência material de W), conforme autorizado na seção 6 do prompt — os cinco demais construtores rejeitam `None` como qualquer outro tipo inválido (P15-05).

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
prova_semantica: "rótulo + marcadores/[<]/[>]/página em todas as seis saídas; caminho geométrico int válido; sem coerção/fallback"
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
staged: vazio
unstaged: worktree acumulado H-0045/P01-P15 e patches de handoff (inalterado além dos dois arquivos deste patch)
nao_rastreados: artefatos acumulados do handoff, P15 e este relatório
divergencias_materiais: []
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - "construir_caso_vazio(W=None) permanece caso válido por design (seção 6 do prompt); não é regressão do domínio estrito."
observacoes_para_qa:
  - "Achado QA-H0045-P14-001 tratado; P12/P13/P14 e demos positivas preservados."
  - "Retomar validação manual somente em 15/17; não reabrir 6/17..14/17."
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
