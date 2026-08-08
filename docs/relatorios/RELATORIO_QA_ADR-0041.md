# Relatório QA — ADR-0041

status: ADR_REJECTED
objeto: docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md

## Achado material

A universalidade da mudança não está semanticamente inequívoca. D-PGU-05
determina que toda paginação comum, presente ou futura, está submetida à
padronização e declara expressamente que não há exceções (seção 3, linhas
147–157). Porém, a seção 6 afirma que um console “com paginação de página
única” permanece fora do impacto da ADR (linhas 303–308).

Essa ressalva não pode ser tratada apenas como ausência de migração: a
ADR-0038 considera a paginação habilitada mesmo quando há uma única página,
mantendo o indicador `página 1/1` e os controles existentes, embora inativos
(D-PAG-11 e D-PAG-12). A própria ADR-0041 preserva esse comportamento em
D-PGU-06 e, na seção 4, inclui a paginação de uma página no modelo universal.
Assim, a redação da seção 6 introduz uma exceção material ou, no mínimo, uma
ambiguidade incompatível com a afirmação de universalidade e com a
representação canônica obrigatória. Não é possível determinar se a
representação `[PgUp][PgDn] Páginas` também substitui a notação anterior nesse
caso.

O achado afeta diretamente os critérios 1, 3 e 5. Enquanto a exceção não for
eliminada ou semanticamente delimitada como mera transição sem exclusão de
escopo, a ADR não pode ser aprovada.
