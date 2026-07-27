---
name: REL-ADF-NNNN-descricao
description: "[preencher] Resultado da análise documental final"
metadata:
  type: relatorio_analise_documental_final
  etapa: ANALISE_DOCUMENTAL_FINAL
  status: "[taxonomia definida no prompt]"
  data: YYYY-MM-DD
rastreabilidade:
  ciclo:
  adr_relacionadas: []
  handoffs_relacionados: []
  relatorios_materiais: []
---

# REL-ADF-NNNN — Análise documental final

> Relatório sucinto e proporcional. Não refaça os QAs anteriores nem consolide toda a história do ciclo.
>
> Teto normal: 600 palavras.

## 1. Objeto e status

```yaml
ciclo:
status_literal:
```

## 2. Verificações finais

```yaml
verificacoes:
  - item_material:
    metodo_ou_origem:
    resultado: OK | FALHA | NAO_CONFIRMADO
```

Verifique somente consistência final, rastreabilidade necessária, artefatos esperados e ausência de contradição material ativa.

## 3. Pendências e achados

```yaml
achados:
  - id:
    requisito_ou_contradicao:
    evidencia_focal:
    impacto:
pendencias_nao_bloqueantes: []
bloqueios: []
```

Não criar nova etapa administrativa por prudência abstrata.

## 4. Estado para fechamento

```yaml
pronto_para_fechamento_manual: true | false
validacao_manual:
  necessaria:
  resultado:
workspace_compacto:
  branch:
  HEAD:
  staged:
  unstaged:
  nao_rastreados:
```

Não copiar saídas Git completas quando o estado estiver conforme. O fechamento Git permanece manual.
