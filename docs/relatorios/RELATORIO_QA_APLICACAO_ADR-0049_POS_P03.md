# Relatório de QA da aplicação — ADR-0049/P03

## Aplicação de D-0027-10

O contrato define o parágrafo completo como unidade lógica, recompõe no
resize a partir do texto lógico completo e não reutiliza linhas físicas
anteriores. As linhas são formadas por palavras inteiras; não há corte,
hifenização automática, separação silábica ou divisão por células. A
justificação ocorre somente depois da formação das linhas e expande os vãos
entre palavras das linhas aplicáveis.

## Remoção da política antiga

Não permanece requisito material de repartir segmentos, cortar conteúdo por
células ou dividir internamente palavras para satisfazer a largura.

## Palavra maior que a largura

A palavra permanece indivisível e não é alterada para caber. O contrato não
escolhe clipping, overflow, scroll, erro, fallback, truncamento, expansão de
container ou outra política física.

## Última linha

Permanece neutra quanto a justificar, não justificar, expandir ou distribuir.

## Whitespace/separadores

A expansão é específica da justificação de parágrafo e não cria política
global para tabs, preservação literal, normalização, condensação ou trimming.

## Preservações

Permanecem válidas a largura visual, ANSI/CSI indivisível, estado visual SGR,
ordem e conteúdo sem perda ou inserção indevida, a distinção entre composição
e truncamento deliberado, a justificação somente sob solicitação e a
coerência entre medição e renderização.

## Achados

Nenhum.

## Status final

`ADR_APPLICATION_APPROVED`
