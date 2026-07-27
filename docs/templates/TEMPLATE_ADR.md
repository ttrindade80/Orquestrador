---
name: ADR-NNNN-descricao
description: "[preencher] Decisão arquitetural em uma linha"
metadata:
  type: adr
  status: proposta
  id: ADR-NNNN
  data: YYYY-MM-DD
  substitui: null
rastreabilidade:
  decisao_usuario: "[referência ou síntese validada]"
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados: []
  handoffs_bloqueados: []
---

# ADR-NNNN — [Título curto]

## 1. Status

`proposta` | `aceita` | `rejeitada` | `substituida`

## 2. Contexto

[Descreva o problema e as autoridades existentes. Não trate sugestão como decisão.]

## 3. Decisão explícita do usuário

[Registre somente a decisão já tomada. Não escolha alternativa, arquitetura, schema, formato ou diretório não autorizado.]

## 4. Decisão

[Formalize objetivamente a decisão e seus limites.]

## 5. Consequências

### Positivas

- [Consequência]

### Custos e restrições

- [Custo, restrição ou risco]

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `[caminho relativo à raiz]` | [Alteração documental esperada] |

## 6. Compatibilidade e transição

[Explique compatibilidade, migração, substituição ou `não aplicável`.]

## 7. Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| [Opção] | [Motivo registrado] |

## 8. Itens fora de escopo

- [Item não decidido]
- [Item que exige decisão futura]

## 9. Critérios para aplicação

- [ ] A decisão foi propagada somente aos documentos afetados.
- [ ] Não restaram contradições normativas ativas.
- [ ] Nenhuma implementação de código foi feita durante a aplicação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] Diretórios previstos e criados foram distinguidos.
- [ ] A execução de aplicação produziu relatório próprio em `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução anterior.
- [ ] Evidência material necessária foi preservada no relatório ou em arquivo referenciado dentro de `docs/relatorios/`.
- [ ] A aplicação foi submetida a QA independente.

## 10. Bloqueios

[Use `nenhum` ou descreva a decisão ainda ausente.]
