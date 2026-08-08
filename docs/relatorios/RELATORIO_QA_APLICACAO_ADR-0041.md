---
name: RELATORIO_QA_APLICACAO_ADR-0041
description: "QA documental da aplicação da ADR-0041"
metadata:
  type: relatorio_qa_aplicacao
  status: ADR_APPLICATION_APPROVED
  data: "2026-08-07"
---

# QA da aplicação da ADR-0041

## Achados materiais

Nenhum.

## Suficiência factual do relatório de aplicação

O relatório de aplicação é factual e suficiente. O delta declarado coincide
com os documentos auditados: `PageUp`/`PageDown` são as únicas entradas de
paginação; `[PgUp][PgDn] Páginas` é a representação canônica; e `<`, `>`, `,`
e `.` não têm função de paginação, alias, atalho ou fallback.

`contrato_console.md`, `contrato_chip.md` e
`contrato_barra_de_menus.md` estão semanticamente alinhados. Os módulos 21 e
31 refletem a nova autoridade; o módulo 32 não contém regra vigente conflitante
nem exigia alteração material. As ocorrências da notação antiga permanecem
somente em contexto histórico, comparativo ou explicitamente fora do escopo
vigente.

As regras materiais da paginação limitada da ADR-0038 permanecem preservadas:
topologia, cursor, seleção, repaginação, indicador e independência por console.
Não foi introduzido comportamento novo de cursor, seleção, navegação
multinível, layout ou cálculo de página. O índice registra a ADR-0041 como
aceita, aplicada e com QA da aplicação pendente; a própria ADR mantém o mesmo
estado documental.

## Status final

`ADR_APPLICATION_APPROVED`
