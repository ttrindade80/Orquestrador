# Relatório — Criação do handoff H-0070

## Handoff criado

`docs/handoff/H-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md`,
status `READY_FOR_IMPLEMENTATION`, item `ITEM-0010`, `ADR-0046`, predecessor
funcional `H-0069` (`TECNICAMENTE_E_MANUALMENTE_APROVADO` nos itens já
validados; validação manual final do `ITEM-0010` permanece pendente,
aguardando os refinamentos deste handoff).

## Capacidade

Fatia única cobrindo: remoção dos ordinais alfabéticos (`A)`/`B)`/`C)`) dos
filhos da tela Estilo com reposicionamento do cursor na região liberada;
alinhamento em coluna comum das amostras de uma mesma categoria; correção da
composição multitecla dos presets de chip `Ponto`, `Destaque Texto` e
`Destaque Fundo`; e aplicação real desses três presets aos chips efetivos da
Barra de Menus (hoje inexistente), preservando geometria sob troca de estilo
em runtime e resize. Nenhuma funcionalidade nova fora desse conjunto.

## Achados que fundamentam o handoff

A leitura focal do código (restrita a `tela/` e `demo/`, termos autorizados)
encontrou evidência concreta e reproduzível do defeito-alvo: com
`config/estilo.json` atual (`chip.preset_default = "Ponto"`, alteração já
presente e não commitada no worktree), a Barra de Menus real hoje produz
`PgUp. PgDn.` em vez de `PgUp/PgDn.` — exatamente o padrão que o prompt de
autoria proíbe. A causa raiz foi localizada: o agrupamento exclusivo do par
`chip_pagina_anterior`/`chip_pagina_proxima` em
`tela/renderizacao/barra_menus.py` (H-0051/D-PGU-01 a D-PGU-03) apenas
concatena o texto de cada chip renderizado individualmente, correto só para
presets delimitados. Adicionalmente, `_texto_chip_barra` já lê `cor_texto`/
`cor_fundo` do estilo resolvido mas descarta ambos explicitamente
(`_ = (cor_texto, cor_fundo)`) — os presets `Destaque Texto`/`Destaque
Fundo` hoje não têm nenhum efeito na Barra real, só nas amostras da tela
Estilo. Também foi confirmado que `EstiloResolvido` do chip não carrega o
nome do preset, exigindo discriminação estrutural pelos 5 campos já
resolvidos (delimitadores + cores), sem inventar preset novo. Para os
ordinais dos filhos, foi localizado o ponto exato de composição do prefixo
de linha (`tela/renderizacao/conteudo_externo.py::_linhas_apresentacao_
hierarquia_com_mapa`) e confirmado que remover o designador do nível
`filho` exige, para atender a decisão de cursor ocupando a região liberada,
uma alteração pontual e condicionada nessa função genérica — único
consumidor de produção afetado é `tela/estilo.py`; duas fixtures de teste
(`h0055_dois_niveis_por_foco_conteudo.json`, `h0036_hierarquia_conteudo.json`)
foram nomeadas para checagem de não regressão.

## Arquivos candidatos/autorizados resolvidos

`tela/estilo.py` (designador do filho + pré-cálculo de largura de nome por
categoria); `tela/renderizacao/estilo.py` (padding do nome antes da
amostra); `tela/renderizacao/conteudo_externo.py` (reposicionamento
condicionado do cursor); `tela/renderizacao/barra_menus.py`
(`_texto_chip_barra` aplicando cor; bloco de agrupamento tornando-se
dependente da família estrutural do preset); dois arquivos de teste novos
(`tela/teste_estilo_h0070.py`, `demo/teste_demo_estilo_h0070.py`);
relatório futuro `IMP-0070`. Nenhuma fixture nova autorizada — as fixtures
`h0045_paginacao_console_unico`, `h0069_estilo_demonstracao_integrada.json`
e `h0063_estilo_estrutura_navegacao_dois_niveis` já cobrem toda a
reprodução/demonstração necessária.

## Testes e demonstração definidos

Nove categorias de teste obrigatório (A a I no handoff), cobrindo filhos,
amostras, chips de uma tecla, multitecla delimitada, `Ponto`, `Destaque
Texto`, `Destaque Fundo`, Barra de Menus real e regressão completa. Achado
relevante: três testes de `demo/teste_demo_paginacao.py` já falham hoje no
worktree (asserções literais `"[PgUp][PgDn] Páginas"` desatualizadas frente
a `chip.preset_default = "Ponto"`) — o handoff classifica isso explicitamente
como manifestação direta do defeito-alvo, não como falha externa a ignorar,
e exige a correção dessas asserções como parte da entrega. Demonstração
reproduzível definida em quatro passos, todos sobre fixtures/mecanismos já
existentes, sem tocar `config/estilo.json` de produção.

## Preservações materiais

Chips de uma tecla; presets delimitados (`[PgUp][PgDn]`); indicador de
preset vigente/não vigente; indentação dos filhos; ordem lógica e posição
global da Barra de Menus; toda a semântica de candidato/aplicação/
confirmação/persistência de H-0065–H-0068; sessão de demonstração local
H-0069; `config/estilo.json` sem escrita antes da confirmação.

## Bloqueios

Nenhum. As decisões fechadas do prompt de autoria são executáveis dentro dos
mecanismos já existentes no código (estrutura de `EstiloResolvido`,
utilitários de largura visual de `texto_ansi.py`, agrupamento H-0051,
mecanismo de inclusão/cursor de `conteudo_externo.py`), sem exigir novo
preset, novo campo de configuração, segunda noção de override ou alteração
normativa de ADR-0046.

## Status

`HANDOFF_CREATED`.
