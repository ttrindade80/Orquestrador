# QA pós-patch P03 — ADR-0049

## D-0027-10

Não adequada como um todo. Os requisitos materiais estão presentes: o
parágrafo completo é a unidade lógica; resize recompõe do texto lógico;
palavras permanecem inteiras; não há hifenização, separação silábica ou
divisão pelo compositor; e a justificação ocorre após a formação das linhas,
nos vãos entre palavras.

## Reconciliação D-0027-04

Adequada. D-0027-04 foi alinhada à recomposição do parágrafo completo e às
palavras inteiras, sem autorização residual para divisão arbitrária,
particionamento físico ou recomposição a partir de linhas anteriores.

## Fronteira da palavra maior que a largura

Preservada. A ADR mantém a palavra indivisível e não escolhe clipping,
overflow, scroll, erro, fallback, expansão de container ou truncamento.

## Whitespace/separadores

Fronteira clara. A expansão entre palavras é limitada à justificação de
parágrafo e não cria política global para tabs, separadores, whitespace
arbitrário, preservação literal ou normalização.

## Sobre-especificação

P03 adiciona a regra de que “a última linha do parágrafo não deve ser
artificialmente expandida”. Essa política específica sobre a última linha não
é necessária para corrigir o defeito observado e excede a decisão conceitual
exigida, sem autoridade adicional para fechar esse algoritmo.

## Achados

- QA-ADR-0049-01 — Sobre-especificação algorítmica da política da última linha.

## Status final

`ADR_REJECTED`
