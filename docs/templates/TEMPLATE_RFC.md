---
name: RFC-NNNN-descricao
description: "[preencher] Mudança proposta em uma linha"
metadata:
  type: rfc
  status: pendente
  id: RFC-NNNN
  aberta_por: "[papel ou pessoa]"
  data_abertura: YYYY-MM-DD
rastreabilidade:
  contratos_afetados: []
  issues_relacionadas: []
  bugs_relacionados: []
  handoffs_bloqueados: []
  evidencias_relacionadas: []
---

# RFC-NNNN — [Título curto]

## 1. Status

`pendente` | `em_analise` | `aceita` | `rejeitada` | `substituida`

RFC aceita não substitui ADR ou atualização contratual quando esses artefatos forem necessários.

## 2. Problema

[Descreva a lacuna, contradição ou necessidade.]

## 3. Evidência

[Registre somente fatos materiais, origens focais, comandos reproduzíveis e resultados necessários. Use `NAO_CONFIRMADO` quando a evidência for insuficiente.]

Não copie dumps extensos. Nenhuma evidência material pode existir somente em `/tmp`.

Quando um arquivo separado for indispensável por formato, tamanho ou reutilização direta, grave-o em `docs/relatorios/` e registre:

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```

## 4. Por que exige decisão

[Explique por que a mudança não pode ser tratada como correção local.]

## 5. Proposta

[Descreva a alternativa proposta sem apresentá-la como já aprovada.]

## 6. Alternativas

| Alternativa | Benefícios | Custos ou riscos |
|---|---|---|
| [Opção] | | |

## 7. Impacto documental

| Artefato | Mudança necessária |
|---|---|
| `[caminho relativo à raiz]` | [Regra a criar, alterar ou remover] |

## 8. Impacto operacional previsto

```yaml
diretorios_previstos:
arquivos_previstos:
configuracoes_previstas:
entradas_afetadas:
saidas_afetadas:
migracao_necessaria:
```

Previsão não comprova criação e não autoriza implementação.

## 9. Decisão necessária do usuário

[Formule a escolha objetiva que precisa ser feita.]

## 10. Critério de encerramento da RFC

- [ ] Decisão explícita registrada.
- [ ] ADR criada, quando necessária.
- [ ] Contratos atualizados, quando necessários.
- [ ] Handoffs bloqueados revisados.
- [ ] Evidências materiais persistidas de forma localizável.
- [ ] Nenhuma implementação foi iniciada apenas com base nesta RFC.
