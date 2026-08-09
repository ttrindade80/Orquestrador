---
tipo: relatorio_patch_adr
status: ADR_PATCH_APPLIED
rastreabilidade:
  etapa: PATCH_ADR
  objeto: ADR-0042
  patch: P04
  artefato_principal: docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0042_P03.md
  motivo: MUDANCA_DECISAO_USUARIO
  decisoes_tratadas:
    - D-MULTI-07-P04
---

# Relatório do patch ADR-0042 P04

## Resultado

`ADR_PATCH_APPLIED`

A ADR-0042 foi atualizada para incorporar D-MULTI-07-P04 — coerência
estrutural de selecionabilidade. Este relatório registra somente o patch
documental solicitado; aplicação documental, implementação, handoff e QA não
foram executados.

## Decisão incorporada

Em `selecao_multinivel`, um nó que possua ao menos um descendente
selecionável deve ser selecionável, assim como todos os seus ancestrais
estruturais até a raiz. Todo pai válido que contenha seleção abaixo dele
possui estado binário e `tg`. A regra vale em profundidade arbitrária.

Um item declarado não selecionável não possui estado de seleção, não recebe
`tg`, não entra no conjunto selecionado, não participa da unanimidade e não
pode introduzir uma subárvore com itens selecionáveis. Assim, sua subárvore é
integralmente não selecionável; ele pode ser folha ou pai de conteúdo também
integralmente não selecionável.

## Relação com D-MULTI-06-P03

D-MULTI-07-P04 adiciona somente a coerência estrutural. Permanecem vigentes,
sem alteração, o estado binário, `tg` para itens selecionáveis, a unanimidade
dos filhos selecionáveis imediatos, a reconciliação ascendente, a propagação
descendente, a ausência de estado parcial e a profundidade arbitrária de
D-MULTI-06-P03.

Para pais válidos com descendentes selecionáveis, Espaço continua operando
pela política descendente vigente. O cenário `pai não selecionável +
descendente selecionável` passa a ser configuração inválida/incoerente e não
é comportamento funcional suportado. O suporte específico a esse cenário não
é requisito e deverá ser removido ou reconciliado na futura aplicação da
implementação.

## Fixture H-0054 e caso negativo

A exigência de pelo menos três pais de nível 1 foi preservada. O segundo ramo
é explicitamente interpretado como:

```text
2. Pai nível 1 selecionável
   └── item explicitamente não selecionável
```

O pai `2.` possui `tg` e participa normalmente da seleção. O item interno não
selecionável permanece sem `tg`, fora da seleção e sem descendentes
selecionáveis.

O caso negativo correto é:

```text
pai selecionável
├── filho selecionável
└── item não selecionável
```

O item não selecionável não é marcado pela seleção recursiva e não impede a
unanimidade calculada somente sobre os filhos selecionáveis.

## Preservações

O patch não altera `arvore_colapsavel`, H-0053, H-0055, paginação,
PageUp/PageDown, cursor, foco, barra, Enter, execução, símbolos ou a
apresentação `tg`. Não foi criada nova navegação, geometria, política, estado
parcial ou símbolo.

## Bloqueios e próxima etapa

Não há bloqueio para o patch documental. QA não foi executado nesta etapa e
permanece como próxima etapa formal: `QA_ADR`.
