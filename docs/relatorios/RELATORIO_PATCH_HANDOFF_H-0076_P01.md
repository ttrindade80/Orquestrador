---
cadeia:
  raiz: docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0076.md
  origem_reabertura: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_ITEM-0027_R01.md

decisao_aplicada:
  - D-0027-10
---

# Relatório — PATCH_HANDOFF H-0076 P01

## Requisitos antigos removidos

Removidas as autorizações para repartir segmentos maiores que a largura,
quebrar segmentos longos, usar unidades visuais que pudessem cortar palavras
e preservar comportamentos locais genéricos de quebra. Também foram retiradas
as políticas abertas para última linha e separadores que poderiam transformar
compatibilidades históricas em regra canônica.

## Nova semântica executiva

O parágrafo lógico completo é a entrada de toda composição. O núcleo distribui
palavras inteiras em linhas, não divide nem altera palavras, não hifeniza, não
separa sílabas e não faz divisão arbitrária por largura. Resize recompõe o
texto lógico completo. A justificação ocorre somente depois da formação das
linhas e expande apenas os vãos entre palavras das linhas aplicáveis. Não foi
criada política global para whitespace ou separadores arbitrários.

## Testes futuros reconciliados

O handoff passou a exigir testes diretos de formação por palavras, parágrafo
completo em larguras distintas, palavra maior que a largura sem alteração
semântica, justificação posterior à formação e proteção ANSI. Inclui a
reprodução do popup com parágrafo longo justificado, resize progressivo e
retorno à largura original, verificando palavras, conteúdo, geometria,
moldura e ANSI.

## Neutralidade e fronteiras

A última linha permanece neutra: nenhum comportamento específico foi tornado
normativo. Para palavra maior que a largura, o handoff exige apenas que o
compositor não divida nem altere a palavra; clipping, overflow, scroll, erro,
fallback, truncamento e expansão de container permanecem fora da decisão.

O popup continua consumidor focal, responsável por texto lógico completo,
geometria, moldura, largura útil e modo, sem implementação local concorrente.
`texto_ansi.py` só pode ser alterado se estritamente necessário. H-0077 não
foi reconciliado: consumidores externos dependerão da semântica nova e terão
regressão posterior após a aprovação do núcleo corrigido.

## Bloqueios

Nenhum bloqueio documental. Código, testes, validação manual, QA do handoff,
H-0077, stage, commit e push permanecem fora desta etapa.
