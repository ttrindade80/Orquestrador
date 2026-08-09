# Relatório de patch — ADR-0042 P03

```yaml
rastreabilidade:
  etapa: PATCH_ADR
  objeto: ADR-0042
  patch: P03
  artefato_principal: docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  cadeia_raiz: docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0042_P02.md
  motivo: MUDANCA_DECISAO_USUARIO
  decisoes_tratadas:
    - D-MULTI-06-P03
```

## Delta material incorporado

`D-MULTI-06-P03` fecha, em `selecao_multinivel`, estado binário para toda
folha, pai intermediário e raiz selecionáveis, sempre com a apresentação `tg`
existente. O estado do pai é derivado pela unanimidade dos filhos
selecionáveis imediatos; itens não selecionáveis não têm estado, não recebem
`tg` e são ignorados. Toggles de folha reconciliam pais e ancestrais de baixo
para cima. Espaço em pai mantém a propagação descendente e, ao final,
reconcilia os pais pela mesma regra. Estado parcial, indeterminado, contador,
seleção independente ou nova linguagem visual permanecem proibidos.

Também foi fechada a fixture demonstrativa mínima de H-0054: três pais de
nível 1, dois pais de nível 2 no primeiro ramo, múltiplas folhas selecionáveis
em cada um, caso não selecionável em outro ramo e terceiro ramo para
diversidade, com cenários de seleção descendente, ascendente e desseleção.

## Seções da ADR afetadas

- metadados de rastreabilidade e bloco de patch;
- D-MULTI-06 e §4.6 (`selecao_multinivel`);
- §5.3 (integração com `tg` existente);
- §7 (consequências);
- §8 (preservações e fora de escopo);
- §9 (critérios de aplicação e demonstração).

## Preservações

Mantidos profundidade arbitrária, topologia única, toggle de folha, alcance
recursivo de Espaço em pai, itens não selecionáveis sem alteração, `tg`,
símbolos, cursor, foco, Enter, execução, confirmação, persistência, paginação
e PageUp/PageDown. `arvore_colapsavel`, `dois_niveis_por_foco`, H-0053 e H-0055
não foram alterados. Os quatro handoffs do ITEM-0007 não foram reespecificados.

## Verificações

- ADR atualizada somente nos pontos correspondentes ao P03.
- Relatório materializado no caminho rastreado.
- QA, aplicação documental, implementação e testes não foram executados.
- Diff final conferido somente para a ADR e este relatório.

## Bloqueios

Nenhum. Próxima etapa: `QA_ADR`.
