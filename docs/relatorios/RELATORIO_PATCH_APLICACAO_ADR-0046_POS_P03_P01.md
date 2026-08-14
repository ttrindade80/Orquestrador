# RELATORIO_PATCH_APLICACAO_ADR-0046_POS_P03_P01

Cadeia: ADR-0046 pós-P03 (ADR_APPROVED).

Etapa: PATCH_APLICACAO_ADR. Escopo fechado no achado
ACH-APLICACAO-ADR0046-P03-01. Sem nova aplicação ampla da ADR.

## Achado tratado

ACH-APLICACAO-ADR0046-P03-01: a seção de composição multitecla de
`docs/contratos/contrato_chip.md` reproduzia a associação incompatível
anteriormente existente na ADR, antes do PATCH_ADR P03.

## Arquivo alterado

- `docs/contratos/contrato_chip.md` — somente a passagem de exemplos
  normativos da seção 10.1 (`DEC-ITEM0010-CHIP-01`).

Nenhum outro arquivo de contrato, nomenclatura, handoff, configuração,
código ou teste foi alterado.

## Associação anterior incompatível

Na enumeração Colchete, Curva, Ornamental, Traço, os exemplos associavam
Curva a forma que não corresponde ao catálogo preservado e Ornamental a
`╭` / `╮`.

## Associação final

- Curva = `╭` / `╮`
- Ornamental = `❲` / `❳`

Curva e Ornamental permanecem nomeados de forma distinta, cada um com os
próprios delimitadores. Colchete e Traço não foram redefinidos.

## Preservação da unidade multitecla

A regra de uma única unidade visual com `/` nas extremidades foi
preservada. `[PgUp][PgDn]` não foi reintroduzido como forma física; permanece
somente como identificador documental, como já estava no contrato.

O restante do contrato não foi modificado.

## Verificações executadas

- Leitura integral da ADR-0046 pós-P03 e de `contrato_chip.md`.
- Busca focal autorizada (`Curva`, `Ornamental`, `PgUp`, `PgDn`,
  `multitecla`, `DEC-ITEM0010-CHIP-01`) restrita a esses dois arquivos.
- Diff focal da seção 10.1: associação nome–delimitador reconciliada;
  demais regras intactas.
- `git diff --check` nos dois artefatos permitidos.

## Bloqueios

Nenhum. A correção não exigiu alterar outro documento.
