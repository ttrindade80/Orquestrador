---
name: REL-CRIACAO-NNNN-descricao
description: "[preencher] Resultado factual da criação documental"
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_ADR | CRIAR_HANDOFF | CRIAR_DOCUMENTO
  status: "[taxonomia definida no prompt]"
  data: YYYY-MM-DD
rastreabilidade:
  etapa:
  objeto:
  artefato_principal:
  autoridade_principal: null
  decisoes_materializadas: []
---

# REL-CRIACAO-NNNN — Criação documental

> Relatório sucinto, factual, assertivo e autocontido. Omitir seções e campos vazios.
>
> Teto normal: 600 palavras. Este relatório não aprova o documento criado.

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_ADR | CRIAR_HANDOFF | CRIAR_DOCUMENTO
artefato_criado:
status_literal:
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - caminho_ou_decisao:
decisoes_materializadas:
  - id:
    sintese:
```

Não reproduza a especificação nem o conteúdo do documento criado.

## 3. Delta documental

```yaml
delta_material:
  - [fato material incorporado ao artefato]
arquivos_criados: []
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo:
    resultado_compacto:
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas: []
```

Se a autoria exigir decisão nova, use bloqueio; não decida autonomamente.

## 6. Evidências separadas

[Omitir quando não aplicável.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```
