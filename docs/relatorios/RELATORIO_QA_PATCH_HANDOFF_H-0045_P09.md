# Relatório QA — PATCH_HANDOFF H-0045 P09

status: H2_HANDOFF_PATCH_REQUIRED

## Suficiência e limites da autorização

§22 autoriza nominalmente `VM-H0045-R06-001` e descreve corretamente a
diferença entre `[Esc] Limpar` e o rótulo original (`Sair`, `Voltar ou outro`),
usando somente a seleção reconciliada do console focado. Exige primeiro Esc
para limpar e segundo Esc para a ação original, atualização após seleção,
limpeza, página, foco e resize, e preserva cursor, foco, página, Enter,
Espaço, paginação e seleção múltipla.

O limite de código é focal e suficiente: `_linhas_barra`/interpretação de
`forma_exibicao` em `tela/renderizador.py`, função pura e estado reconciliado
em `tela/selecao.py`, e testes integrados nominados. `demo/demo.py` não é
autorizado. Não há campo novo de configuração nem refatoração geral. As
validações anteriores permanecem aprovadas; `VM-H0045-R07-001` não é reaberto
e `QA-H0045-P08-001` permanece separado.

## Arquivos e configurações conferidos

Existem os quatro testes autorizados: `tela/teste_renderizador.py`,
`tela/teste_selecao.py`, `demo/teste_demo_paginacao.py` e
`demo/teste_demo_navegacao.py`. A evidência focal confirma que o renderer já
interpreta `forma_exibicao` para o rótulo dinâmico de Enter, que seleção
reconciliada e limpeza são puras, e que o Esc funcional em `demo/demo.py` já
limpa a seleção focada sem sair.

Todos os cinco caminhos de configuração existem. `h0045_fluxo_execucao_paginado.json`,
`h0044_fluxo_execucao_integrado.json` e
`h0041_selecao_multipla_oito_itens.json` combinam seleção múltipla, chip Esc e
rótulo estático (`Sair`) que pode usar `forma_exibicao`. A busca focal não
encontrou outra configuração material omitida.

## Testes futuros exigidos

Devem ser provados os 14 casos de §22.4: estados vazio/uma/múltiplas
seleções, seleção entre páginas, primeiro/segundo Esc, exclusão simultânea de
rótulos, página, resize, foco, cursor e regressões de Enter/Espaço/paginação.
Executar as suítes focal e completa especificadas em §22.4.

## Achado

`P09-QA-001`: a enumeração de configurações de §22.3 inclui
`config/telas/demo/h0045_paginacao_console_unico.json` e
`config/telas/demo/h0045_dois_consoles_paginas_independentes.json`, mas ambas
declaram `politica_selecao: "unica"`. Elas não satisfazem os três critérios
da autorização focal. A ressalva de “preservar comportamento” reduz o risco,
mas não elimina a abertura nominal indevida e a contradição com a exigência
de não incluir configuração sem necessidade. O PATCH_HANDOFF deve remover
esses caminhos da lista autorizada ou marcá-los explicitamente como somente
preservados, fora do escopo de alteração.

As verificações documentais confirmaram §22 no local correto, sem substituição
silenciosa de §§19–21, e `git diff --check` sem saída.

## Próxima categoria objetiva

PATCH_HANDOFF
