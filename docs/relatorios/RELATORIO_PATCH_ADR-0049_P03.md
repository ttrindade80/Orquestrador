cadeia:
  raiz: docs/relatorios/RELATORIO_CRIACAO_ADR-0049.md
  origem_reabertura: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_ITEM-0027_R01.md
decisoes_adicionadas:
  - D-0027-10

## Causa da reabertura

A validação manual do ITEM-0027 foi reprovada após observação visual, durante
resize, de palavras partidas pela largura física e de composição que não
tratava o parágrafo completo como unidade.

## Decisão adicionada

A ADR-0049 recebeu D-0027-10 — Composição de parágrafo por palavras
indivisíveis. A decisão estabelece recomposição do parágrafo lógico completo,
distribuição de palavras inteiras em linhas e justificação somente depois da
definição dessas palavras, com espaço distribuído entre palavras da mesma
linha. Proíbe hifenização automática, separação silábica e divisão de palavras
pelo compositor, inclusive durante resize. Uma palavra maior que a largura
útil permanece indivisível; o tratamento físico dessa condição ficou fora da
decisão do compositor.

## Trechos anteriores reconciliados

D-0027-04 foi explicitamente alinhada à recomposição do parágrafo completo e
às palavras inteiras. Os critérios de aplicação foram ampliados para refletir
D-0027-10. Não havia na ADR uma autorização textual explícita para repartir
segmentos ou palavras; a nova decisão elimina essa interpretação e também
deixa claro que linhas físicas anteriormente produzidas não são a entrada de
uma recomposição após resize.

## Fronteiras preservadas

Permanecem inalteradas a autoridade canônica única, a distinção entre
composição e truncamento deliberado, a largura dinâmica, a segurança ANSI, a
coerência entre medição e renderização, as responsabilidades locais dos
consumidores, a ausência de política global genérica de whitespace e a
ausência de arquitetura Python prescrita. Não foram decididos clipping, scroll
horizontal, overflow visual, erro, fallback ou expansão de container.

## Bloqueios

Nenhum.
