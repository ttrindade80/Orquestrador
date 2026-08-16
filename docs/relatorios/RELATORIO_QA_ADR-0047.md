# Relatório QA — ADR-0047

status: ADR_REJECTED

## QA-ADR-0047-001

- requisito: A ADR deve ser suficiente para APLICAR_ADR sem nova decisão material de schema/arquitetura; D-DNF-01, D-DNF-04, D-DNF-07 e D-DNF-11 exigem declarações JSON consumíveis pelo renderer.
- evidência focal: §5 afirma que os nomes literais dos campos de tabulação min/max, estrutura de colunas e espaçamento min/max não são fixados e pertencem à aplicação documental; §§6–8 repetem que a aplicação deverá decidir essa nomenclatura. Os blocos vigentes `formato.espacamento`, `formato.alinhamento` e `conteudo` são apenas pontos de extensão e não determinam a localização, a forma nem a cardinalidade dessas declarações.
- impacto material: APLICAR_ADR não consegue definir, validar ou reconciliar de modo determinístico o schema para tabulação pai→filho, número/dados das colunas e espaçamento entre colunas. Permanece aberta, inclusive, a distinção entre declaração por apresentação, nível filho ou nó, além dos campos literais correspondentes. Isso viola a suficiência exigida e deixa decisão material indevidamente aberta.
- correção necessária: Fechar na ADR, antes de APLICAR_ADR, a localização canônica, a forma/cardinalidade e os nomes literais dos campos para as três capacidades, mantendo os limites declarativos e a proibição de persistir geometria física. Não basta remeter a escolha à aplicação documental.
\n