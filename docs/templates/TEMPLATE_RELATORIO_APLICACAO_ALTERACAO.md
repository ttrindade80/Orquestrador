---
name: REL-ALT-NNNN-descricao
description: "[preencher] Resultado factual da aplicação ou alteração de artefatos"
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR | ALTERAR_ARTEFATOS
  status: "[taxonomia definida no prompt]"
  data: YYYY-MM-DD
rastreabilidade:
  etapa:
  objeto:
  artefato_principal:
  autoridade_principal: null
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# REL-ALT-NNNN — Aplicação ou alteração de artefatos

> Relatório sucinto, factual, assertivo e autocontido. Omitir seções e campos vazios.
>
> Teto normal: 600 palavras. Este relatório registra execução; não declara aprovação.

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR | ALTERAR_ARTEFATOS
objeto:
status_literal:
```

## 2. Delta material

```yaml
delta_material:
  - [efeito produzido]
delta_nomenclatura:
  modulos_alterados: []
  termos_criados: []
  termos_alterados: []
  aliases_ou_historicos: []
```

Não descreva o passo a passo. Não copie ADR, contrato, diff ou conteúdo integral dos artefatos.

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho:
    finalidade:
arquivos_alterados:
  - caminho:
    delta:
arquivos_removidos:
  - caminho:
    motivo_autorizado:
```

Arquivo autorizado e não alterado só aparece quando isso for material.

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo:
    resultado_compacto:
    prova_semantica:
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas: []
```

## 6. Evidências separadas

[Omitir quando não aplicável.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```
