# Relatório de criação — ADR-0044

- ADR criada em `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`.
- Foram materializadas as decisões fechadas D-POP-01 a D-POP-24 sobre a
  capacidade genérica de pop-up modal, incluindo fronteiras, separação entre
  configuração, conteúdo e runtime, tipos de conteúdo, geometria, resize,
  navegação, marcação, entrada, saída, validação, compatibilidade, escopo e
  decomposição incremental.
- Arquivos criados:
  - `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`
  - `docs/relatorios/RELATORIO_CRIACAO_ADR-0044.md`
- Verificações realizadas: existência dos dois artefatos; conferência focal
  de que o pop-up não foi descrito como `console`, nova região da tela ou
  executor de ações; distinção entre `seleção única` do console e
  `marcacao: exclusiva`; ausência de paginação; conteúdo recebido pronto, sem
  origem ou produtor declarado pelo pop-up; e distinção entre `ABORTADO` e
  valor vazio.
- Foi executado diff focal somente dos dois arquivos criados.
- Bloqueios: nenhum.
