---
name: BUG-NNNN-descricao
description: "[preencher] Sintoma principal do bug"
metadata:
  type: bug
  status: OPEN
  classificacao: local
  severidade: media
  data_abertura: YYYY-MM-DD
rastreabilidade:
  handoff_origem: null
  relatorio_impl: null
  relatorio_qa: null
  contrato_alvo: null
  issues_relacionadas: []
  evidencias_relacionadas: []
---

# BUG-NNNN — [Descrição curta]

## 1. Classificação

- `local`: corrigível sem mudar contrato, arquitetura, schema ou política.
- `arquitetural`: exige decisão documental antes da correção.
- `NAO_CONFIRMADO`: evidência insuficiente para classificar.

## 2. Sintoma

[O que acontece e em qual cenário.]

## 3. Comportamento esperado

[Cite a autoridade que define o comportamento.]

## 4. Evidência reproduzível

```text
Raiz de execução: .
Comando:
Entrada ou fixture:
Configuração:
Resultado observado:
Resultado esperado:
Código de saída:
Arquivos produzidos ou alterados:
Origem focal da evidência:
```

Código de saída zero não substitui a comparação semântica.

Não copie dumps extensos. Preserve fatos, trechos materiais, hashes, comandos reproduzíveis e resultados necessários.

Nenhuma evidência material pode existir somente em `/tmp`. Quando um arquivo separado for indispensável por formato, tamanho ou reutilização direta, grave-o em `docs/relatorios/` e registre:

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```

## 5. Dados e artefatos

```yaml
entrada_real:
fixture:
temporarios_operacionais:
saidas_geradas:
origem_de_item_inesperado: NAO_CONFIRMADA | CONFIRMADA | nao_aplicavel
```

Temporário operacional não substitui a preservação da evidência material.

## 6. Escopo permitido para correção

### Arquivos e diretórios autorizados

- `[caminho relativo à raiz]`

### Arquivos e diretórios preservados

- `[caminho relativo à raiz]`

Diretório novo deve ser autorizado nominalmente.

## 7. Critério de fechamento

- [ ] Causa classificada com evidência.
- [ ] Correção local executada ou fluxo documental iniciado.
- [ ] Testes relevantes executados.
- [ ] Cada execução material produziu seu próprio relatório em `docs/relatorios/`.
- [ ] QA independente concluído.
