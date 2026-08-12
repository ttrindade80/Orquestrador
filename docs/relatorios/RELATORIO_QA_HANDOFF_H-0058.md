# Relatório QA — Handoff H-0058

status: H1_HANDOFF_APPROVED
handoff: H-0058-popup-lista-navegavel-marcacao.md

A auditoria não encontrou achado material. O handoff materializa somente
`tipo: marcacao`, as políticas literais `marcacao: exclusiva` e
`marcacao: multipla`, envelope fechado, IDs, foco, marcações, formações,
navegação toroidal, `SEM_MOVIMENTO`, `SEM_MUDANCA`, resize e preservação da
instância, mantendo separadas configuração, conteúdo e estado vivo.

Os critérios, testes focais e demonstração distinguem os dois modos, cobrem
regressão textual, geometria, terminal pequeno, `Esc`/`ABORTADO` sem `valor` e
explicitamente impedem confirmação por `Enter`. Fixture, configuração,
acionamento e superfícies autorizadas são nominais e compatíveis com as
superfícies vigentes. A demonstração TTY permanece separada dos testes
determinísticos.

Não há prescrição de schema, aparência, layout, paginação, produtor,
persistência externa ou ação de negócio além das autoridades. H-0059 permanece
íntegro: confirmação, `CONFIRMADO`, payload, binding, interpretação pelo
chamador e ação não são exigidos.
