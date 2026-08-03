# Relatório QA — PATCH_HANDOFF H-0045 P10

status: H1_HANDOFF_APPROVED

## Resolução de P09-QA-001

P09-QA-001 foi integralmente corrigido. A §22.3 separa nominalmente as
configurações autorizadas das preservadas, sem abertura residual para seleção
única.

## Configurações autorizadas

As três existem, declaram `politica_selecao: "multipla"`, possuem chip Esc,
rótulo estático `Sair` e reutilizam `forma_exibicao`; estão autorizadas em
§22.3.1:

- `config/telas/demo/h0045_fluxo_execucao_paginado.json`
- `config/telas/demo/h0044_fluxo_execucao_integrado.json`
- `config/telas/demo/h0041_selecao_multipla_oito_itens.json`

## Configurações preservadas

As duas existem, declaram `politica_selecao: "unica"` e estão nominalmente
fora da alteração em §22.3.2:

- `config/telas/demo/h0045_paginacao_console_unico.json`
- `config/telas/demo/h0045_dois_consoles_paginas_independentes.json`

Permanecem somente sob preservação e testes de regressão; não são candidatas
ao rótulo dinâmico de seleção múltipla, e seleção/estado de outro console não
altera seu chip Esc.

## Integridade e verificações

O restante de §22 permanece focal: renderer limitado a `_linhas_barra`,
interpretação de `forma_exibicao` e helper indispensável; `tela/selecao.py`
limitada à função pura do rótulo; `demo/demo.py` proibido. Permanecem os
quatro testes nominados, ausência de campo novo, reutilização de
`forma_exibicao`, primeiro/segundo Esc, foco/página/resize e preservação de
Enter, Espaço, seleção múltipla e paginação. Os 14 casos, suítes focal e
completa e validação manual continuam obrigatórios.

§§19–21 não foram alterados sem necessidade; não há contradição em §22.
`VM-H0045-R06-001` segue autorizado e não resolvido; `VM-H0045-R07-001`
permanece aprovado e `QA-H0045-P08-001`, tratado pela correção factual, não é
reaberto. `git diff --check` está limpo.

Achados: nenhum.

Próxima categoria objetiva: `PATCH_IMPLEMENTACAO`.
