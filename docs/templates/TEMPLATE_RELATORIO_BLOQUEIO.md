---
name: REL-BLOCKED-NNNN-descricao
description: "[preencher] Resultado material preservado antes do bloqueio"
metadata:
  type: relatorio_bloqueio
  etapa:
  status: BLOCKED
  data: YYYY-MM-DD
rastreabilidade:
  objeto:
  artefato_principal: null
  cadeia_raiz: null
  predecessor_imediato: null
---

# REL-BLOCKED-NNNN — Execução bloqueada

> Use somente quando a execução já produziu leitura, verificação, alteração ou evidência material que precise sobreviver ao contexto.
>
> Se o bloqueio ocorreu antes de qualquer resultado material, não criar relatório.

## 1. Ponto de parada

```yaml
etapa:
objeto:
status: BLOCKED
ponto_de_parada:
motivo:
```

## 2. Resultado material preservado

```yaml
fatos_confirmados: []
verificacoes_executadas: []
evidencia_focal:
```

Não registrar hipótese como fato.

## 3. Estado dos artefatos

```yaml
arquivos_criados: []
arquivos_alterados: []
arquivos_removidos: []
estado_relevante:
```

Indique exatamente como ficaram os arquivos alterados antes do bloqueio.

## 4. Informação necessária

```yaml
informacao_necessaria:
responsavel_pela_decisao_ou_acao:
```

O agente não amplia o escopo para resolver autonomamente o bloqueio.

## 5. Evidências separadas

[Omitir quando não aplicável.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```
