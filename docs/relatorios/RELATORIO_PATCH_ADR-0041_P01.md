# Relatório — Patch da ADR-0041 (P01)

## Cadeia raiz

`RELATORIO_QA_ADR-0041.md`

## Achado tratado

`QA-ADR0041-01`

A seção 6 (Compatibilidade e transição) declarava que "console [...] com
paginação de página única, permanece fora do impacto desta ADR", criando
contradição/ambiguidade com D-PGU-05 (universalidade da mudança), D-PGU-06
(preservação das regras da ADR-0038, inclusive página única) e a
representação canônica `[PgUp][PgDn] Páginas`.

## Trecho semanticamente corrigido

Antes:

> Console sem `politica_paginacao` declarada, ou com paginação de página
> única, permanece fora do impacto desta ADR (`contrato_console.md` §12).

Depois, o trecho foi desdobrado em dois casos distintos:

1. Console sem `politica_paginacao` declarada permanece fora do impacto da
   ADR (não possui paginação comum à qual a autoridade se aplique) — mantida
   a citação a `contrato_console.md` §12.
2. Console com paginação de página única passa a ficar explicitamente
   submetido à autoridade universal da ADR (D-PGU-05), com a representação
   canônica `[PgUp][PgDn] Páginas` (D-PGU-03) quando os controles forem
   exibidos, e com as regras já preservadas da ADR-0038 (D-PGU-06) —
   indicador `página 1/1` e ambos os controles inativos — permanecendo
   vigentes. É registrado que a existência de somente uma página pode
   significar ausência de mudança comportamental de navegação perceptível,
   mas nunca exclusão de escopo ou de impacto da ADR.

## Ausência de outras mudanças materiais

Nenhum outro trecho do documento foi alterado. Nenhuma decisão D-PGU-01 a
D-PGU-08 foi reescrita, reaberta ou renumerada — apenas referenciadas, por
sigla, dentro do trecho corrigido da seção 6. Seções 1 a 5 e 7 a 11
permanecem textualmente inalteradas. Nenhum contrato, nomenclatura, backlog,
código ou teste foi tocado.

## `git diff --check`

Executado sobre `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`:
sem saída — nenhum problema de espaço em branco ou de marca de conflito
detectado.

## Bloqueios

Nenhum.
