---
name: IMP-H0043-P01-resultado-json-null
description: "Patch de implementação — QA-IMPL-H0043-001: resultado_json ausente preserva null no modelo"
metadata:
  type: relatorio_implementacao
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-0043
  data: 2026-07-29
rastreabilidade:
  contrato_alvo: null
  adr_relacionadas: [ADR-0036]
  issues_relacionadas: []
  bugs_abertos: []
  autorizacoes_operacionais: []
  cadeia_raiz: H-0043
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0043.md
  achados_tratados: [QA-IMPL-H0043-001]
---

# IMP-H0043-P01 — Patch de implementação

## 1. Identificação e status

```yaml
handoff: H-0043 — carregamento e apresentação da tela padrão de resultado
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTED
status_normalizado: IMPLEMENTATION_PATCHED
```

## 2. Delta material

Achado QA-IMPL-H0043-001: `_exibir_resultado_json` convertia `resultado_bruto is None` para a string `"indisponível"` antes da materialização do envelope, gravando a string no modelo. Correção: o modelo passa a armazenar `resultado_json: None`; a conversão visual move-se exclusivamente para `tela.renderizador._texto_valor_campo`, aplicada apenas quando o valor de um campo `nome_valor` é `None`, sem afetar `0`, `False` ou `""`.

### Cadeia de patch

```yaml
raiz: H-0043
predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0043.md
achados_tratados: [QA-IMPL-H0043-001]
achados_resolvidos: [QA-IMPL-H0043-001]
achados_pendentes: []
novos_achados: []
```

## 3. Artefatos alterados

```yaml
arquivos_alterados:
  - caminho: tela/resultado_execucao.py
    delta: removida _exibir_resultado_json; resultado_json materializa resultado_bruto literal (None ou texto bruto)
  - caminho: tela/renderizador.py
    delta: adicionado _texto_valor_campo focal em _linhas_apresentacao_conjuntos; None -> "indisponível" somente na apresentação
  - caminho: tela/teste_resultado_execucao.py
    delta: corrigida asserção que esperava string no modelo; adicionados testes de identidade `is None`, posição/obrigatoriedade do campo, apresentação e preservação de conteúdo presente
```

## 5. Verificações e evidência

```yaml
testes_focais: "410 passed (tela/teste_resultado_execucao.py, tela/teste_renderizador.py, demo/teste_demo.py)"
testes_regressao_h0042: "80 passed"
testes_regressao_selecao: "35 passed"
suite_completa: "704 passed em 21.52s"
quadros_80x24: "6/6 idênticos às fixtures h0043_quadro_*_80x24.txt, sem alteração de expectativa"
modelo_resultado_json_null: "confirmado via `is None`"
apresentacao_resultado_json_null: "confirmado texto 'indisponível' no quadro renderizado"
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: 6ecc4cd
staged: []
residuos: nenhum (__pycache__/*.pyc ausentes; git diff --check limpo)
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas: []
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada: false
  resultado: PENDENTE_DO_USUARIO
  itens_pendentes: [RVM-H0043-01, RVM-H0043-02, RVM-H0043-03, RVM-H0043-04, RVM-H0043-05, RVM-H0043-06]
```
