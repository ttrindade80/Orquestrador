---
name: REL-PATCH-NNNN-PXX-descricao
description: "[preencher] Delta factual do patch"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_ADR | PATCH_APLICACAO_ADR | PATCH_HANDOFF | PATCH_DOCUMENTAL
  status: "[taxonomia definida no prompt]"
  data: YYYY-MM-DD
rastreabilidade:
  etapa:
  objeto:
  cadeia_raiz:
  predecessor_imediato:
  achados_tratados: []
---

# REL-PATCH-NNNN-PXX — Patch

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_ADR | PATCH_APLICACAO_ADR | PATCH_HANDOFF | PATCH_DOCUMENTAL
status_literal:
```

## 2. Cadeia

```yaml
raiz:
predecessor_imediato:
achados_tratados: []
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado:
    alteracao:
arquivos_criados: []
arquivos_alterados:
  - caminho:
    delta:
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo:
    resultado_compacto:
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```

Omitir campos vazios. Não sobrescrever o relatório raiz nem o predecessor.
