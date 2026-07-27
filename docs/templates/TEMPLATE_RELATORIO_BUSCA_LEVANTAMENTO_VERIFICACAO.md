---
name: REL-LEV-NNNN-descricao
description: "[preencher] Resultado factual da busca, levantamento ou verificação"
metadata:
  type: relatorio_busca_levantamento_verificacao
  tipo_execucao: BUSCA | LEVANTAMENTO | INVENTARIO | VERIFICACAO
  status: "[taxonomia definida no prompt]"
  data: YYYY-MM-DD
rastreabilidade:
  etapa:
  objeto:
  autoridade_principal: null
  cadeia_raiz: null
  predecessor_imediato: null
---

# REL-LEV-NNNN — Busca, levantamento ou verificação

> Relatório sucinto, factual, assertivo e autocontido. Omitir seções e campos vazios.
>
> Teto normal: 600 palavras. Não propor decisão, arquitetura, schema ou alteração sem autorização explícita no prompt.

## 1. Pergunta e status

```yaml
tipo_execucao: BUSCA | LEVANTAMENTO | INVENTARIO | VERIFICACAO
pergunta_factual:
status_literal:
```

## 2. Escopo fechado

```yaml
caminhos_consultados: []
buscas_executadas:
  - comando_ou_padrao:
    caminho:
    finalidade:
limites_aplicados: []
```

Registre padrões e caminhos, não a saída completa. Não liste nem explore diretórios fora do escopo autorizado.

## 3. Fatos confirmados

```yaml
fatos_confirmados:
  - id:
    fato:
    origem_focal:
```

`origem_focal` deve permitir localizar a prova por arquivo, seção, linha, símbolo ou comando.

## 4. Não confirmados

```yaml
nao_confirmados:
  - id:
    afirmacao:
    evidencia_ausente_ou_insuficiente:
```

Ausência de evidência permanece `NAO_CONFIRMADO`; não completar por inferência.

## 5. Achados e bloqueios

```yaml
achados:
  - id:
    fato:
    evidencia_focal:
bloqueios:
  - ponto_de_parada:
    motivo:
    informacao_necessaria:
```

## 6. Evidências separadas

[Omitir quando o relatório contiver toda a evidência material.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    prova:
    finalidade:
    leitura_necessaria_para: []
```

Nenhuma evidência material pode permanecer somente em `/tmp`.
