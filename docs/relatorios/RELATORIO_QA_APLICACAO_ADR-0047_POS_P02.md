---
name: relatorio-qa-aplicacao-adr-0047-pos-p02
description: QA pós-patch da aplicação documental da ADR-0047 P02
metadata:
  type: relatorio
  scope: orquestrador
  etapa: QA_POS_PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_APPROVED
---

# Relatório — QA da aplicação da ADR-0047 pós-P02

## Rastreabilidade

```yaml
etapa: QA_POS_PATCH_APLICACAO_ADR
objeto: ADR-0047 / aplicação / P02
patch_adr_origem: P03
cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0047.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0047_P02.md
```

## Status

`ADR_APPLICATION_APPROVED`

## Auditoria

- O schema estrutural de `designador` fecha `tipo` obrigatório, `prefixo` e
  `sufixo` opcionais string, os tipos `decimal_composto`,
  `alfabetico_maiusculo` e `nenhum`, rejeição de chaves desconhecidas e
  ausência de prefixo/sufixo para `nenhum`.
- H-0055 está fechado com tabulação 5..10, apresentação `texto`,
  `alfabetico_maiusculo` e sufixo `)`, preservando `A)`, `B)`, `C)`, `D)`;
  o conteúdo externo permanece inalterado.
- H-0063 preserva `preset`, `amostra`, `titulo`, tabela de duas colunas,
  `tipo: nenhum` sem prefixo/sufixo, tabulação 5..10 e espaçamento 3..8.
- `contrato_console.md` materializa `prefixo + designador_base + sufixo`,
  mantém `decimal_composto` e não emite designador para `nenhum`; tabulação,
  tabela, colunas, alinhamento, quebra, resize, navegação e seleção permanecem.
- `contrato_json_console.md` permanece fora do delta causal P02 e preserva a
  autoridade do documento de conteúdo como dados sem configuração visual.
- A nomenclatura 44 é coerente e não exige atualização material. O índice é
  factual: ADR-0047 aplicada em P02, aguardando QA, sem concluir H-0072/H-0073.
- A documentação está suficientemente fechada para o futuro patch de H-0072;
  a limitação atual do runtime a `tipo` não é defeito deste patch documental.

## Achados materiais

Nenhum. Não permanece decisão documental aberta antes da correção de H-0072.
\n