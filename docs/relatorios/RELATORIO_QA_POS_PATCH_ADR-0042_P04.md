# Relatório QA pós-patch — ADR-0042 P04

## Resultado

`D-MULTI-07-P04` está incorporado de forma coerente: descendente selecionável implica o nó e todos os ancestrais estruturais selecionáveis, em profundidade arbitrária. Pais válidos com seleção abaixo possuem estado binário e `tg`; pai não selecionável com descendente selecionável é explicitamente configuração inválida/incoerente, sem comportamento funcional de Espaço.

## Compatibilidade com D-MULTI-06-P03

Compatível integralmente. Permanecem a topologia única, o estado binário, `tg` para todo item selecionável, a unanimidade sobre filhos selecionáveis imediatos, as propagações descendente e ascendente, a desseleção ascendente, a reconciliação recursiva e a ausência de estado parcial.

## Fixture e caso negativo

H-0054 preserva pelo menos três pais de nível 1, o primeiro ramo com dois pais de nível 2 e múltiplas folhas, o pai `2.` selecionável com `tg`, o item não selecionável interno sem `tg` e sem descendentes selecionáveis, e o terceiro ramo. O caso negativo é corretamente modelado como pai selecionável com filho selecionável e item não selecionável; este é ignorado na unanimidade e na seleção recursiva.

## Preservações e achados

H-0053, H-0055, barra, paginação, `PageUp`/`PageDown`, `tg`, símbolos e política de navegação permanecem fora de alteração. Não há nova política ou símbolo. A distinção nominal entre `D-MULTI-07-P04` e `D-MULTI-07 — dois_niveis_por_foco` é inequívoca.

Os 24 critérios obrigatórios foram confirmados semanticamente. Achados materiais: nenhum.

## Status

`ADR_APPROVED`
