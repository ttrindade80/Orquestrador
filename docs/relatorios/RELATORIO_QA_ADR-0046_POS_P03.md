# Relatório QA — ADR-0046 pós-P03

## Verificações focais

- Curva está normativamente associada a `╭`/`╮`, com o exemplo `╭PgUp/PgDn╮`.
- Ornamental está normativamente associada a `❲`/`❳`, com o exemplo `❲PgUp/PgDn❳`; os dois presets permanecem graficamente distintos.
- A composição multitecla exige uma única unidade visual, usa `/` como separador e reserva delimitadores às extremidades. `[PgUp][PgDn]` aparece apenas como notação histórica/documental e é explicitamente excluída como forma física.
- A decisão permanece limitada à composição e semântica visual do ITEM-0010: não escolhe novo schema, renderer ou arquitetura, não altera a semântica de paginação e não afirma correção ou validação do runtime atual.
- A leitura integral preserva materialmente Destaque Texto foreground-only com espaços laterais em fundo normal, Ponto, Destaque Fundo, `cor_inativo`, console `ec → tg → tx`, F1/F2/F3/F5/F11, tiling e a ordem global da Barra.

## Resultado

Não foi encontrada associação normativa incompatível nem extrapolação material do P03.

## Status

ADR_APPROVED
