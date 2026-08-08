# Relatório de implementação — H-0052 P02

## Escopo

Correção exclusiva do defeito de demonstrabilidade da navegação `nivel_unico`
da fixture `h0052_nivel_unico_explicito`.

## Diagnóstico

O carregamento real preservava os dois itens em
`ElementoCorpo._campos_inertes["itens"]`, fonte consumida por
`tela.navegacao.itens_navegaveis`. A fixture, porém, não declarava a
`distribuicao_matricial` usada para materializar a topologia visual. A
fixture legada `h0045_validacao_nova_pagina.json` foi usada como referência.

## Alterações

- `config/telas/demo/h0052_nivel_unico_explicito.json`: adicionada a
  distribuição matricial canônica de uma coluna, preservando
  `id = h0052_nivel_unico_explicito` e
  `politica_navegacao = {"navegavel": true, "tipo": "nivel_unico"}`.
- `tela/teste_loader.py`: o teste da fixture passou a carregar o modelo pelo
  mecanismo real, identificar o console focalizável, verificar a coleção e a
  grade runtime com pelo menos dois itens distintos, avançar com `mover_baixo`
  e restaurar com `mover_cima`.

Nenhuma alteração foi feita em `tela/navegacao.py`, loader, handoff,
autoridades ou funcionalidades H-0053/H-0054/H-0055. Não houve commit nem QA.

## Testes executados

- Teste focal: 1 passed, 83 deselected.
- `tela/teste_navegacao.py tela/teste_loader.py`: 134 passed.
- Suíte completa: 1.059 passed em 28,73 s.

A confirmação visual no TTY não foi declarada; permanece como validação manual
posterior do usuário.
