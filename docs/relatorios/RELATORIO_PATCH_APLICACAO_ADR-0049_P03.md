# Relatório do patch de aplicação — ADR-0049/P03

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0049.md
  origem_reabertura: docs/relatorios/RELATORIO_QA_ADR-0049_POS_P04.md

decisao_aplicada:
  - D-0027-10
```

## Trechos reconciliados

- A definição de entrada e resultado foi explicitada para tratar o parágrafo
  completo como unidade lógica da composição multilinear, inclusive em toda
  recomposição após resize; linhas físicas anteriores não substituem essa
  entrada.
- A regra de wrap passou a formar linhas com palavras inteiras, sem corte,
  hifenização automática, separação silábica ou divisão arbitrária por células.
- A justificação foi explicitamente posicionada depois da formação das linhas,
  com expansão nos vãos entre palavras das linhas às quais se aplica.

## Nova regra comportamental incorporada

- D-0027-10 foi reconciliada no contrato: palavras permanecem indivisíveis para
  o compositor e a representação física de palavra maior que a largura não é
  escolhida pelo contrato comum.

## Conflitos anteriores removidos

Foi removida a exigência de repartir segmentos maiores que a largura e a regra
correlata de cortar conteúdo em fronteiras de células para satisfazer a largura.
Também foi removida a exigência implícita de que toda palavra ou segmento
respeite a largura por divisão interna.

## Última linha

A última linha permanece neutra. O contrato não determina justificar, não
justificar, expandir, não expandir ou aplicar distribuição especial.

## Palavra maior que a largura

O contrato fixa somente que a palavra permanece semanticamente indivisível para
o compositor e não pode ser alterada para caber. Não escolhe clipping, overflow,
scroll horizontal, erro, fallback, truncamento, expansão de container ou outra
política física.

## Preservação das demais regras

Foram preservadas ordem e conteúdo sem perda, duplicação ou inserção indevida,
largura visual para palavras acomodáveis, distinção entre wrap e truncamento,
justificação somente sob solicitação, coerência entre medição e renderização,
segurança ANSI/CSI e estado visual. A afirmação sobre vãos entre palavras não
cria política global para tabs, whitespace arbitrário ou separadores.

## Bloqueios

Nenhum.
