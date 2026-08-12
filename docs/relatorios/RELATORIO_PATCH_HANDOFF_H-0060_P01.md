# Relatório do patch do handoff H-0060 P01

## Cadeia

- raiz: `docs/handoff/H-0060-resize-responsivo-formacoes-popup-marcacao.md`
- origem_do_patch: `MV-H0060-001`
- diagnostico: `BLOCKED_SCOPE`

## Causa transportada

O novo par físico do resize chega corretamente ao renderer. A falha estava na
fronteira de `renderizar_tela`: embora `l_corpo_disponivel` represente a altura
física reservada ao corpo, a sobreposição fornecia ao pop-up a altura natural
excedente do bloco subjacente. O pop-up escolhia a formação com linhas
fictícias e a verificação final, usando a cota física correta, produzia
insuficiência geométrica convertida pelo runtime em `Terminal pequeno demais`.

## Ampliação de escopo

O H-0060 passou a autorizar `tela/renderizacao/tela.py`, função
`renderizar_tela`, além de `tela/renderizacao/popup.py`. A nova autorização é
focal à integração entre `l_corpo_disponivel`, materialização do corpo,
`sobrepor_no_corpo` e verificação final quando existe pop-up aberto.

O handoff distingue altura natural e altura física, exige que o bloco de
sobreposição represente exatamente a cota reservada e preserva integralmente
a política de composição sem pop-up. A implementação aprovada das formações
em `popup.py` foi registrada como fora de reabertura sem necessidade
demonstrada.

## Seções e critérios acrescentados

- causa factual de integração e casos diagnósticos `80x18` e `77x14`;
- responsabilidade focal de `tela/renderizacao/tela.py`;
- invariantes da integração da altura física do corpo;
- fronteiras negativas contra truncamento, paginação, remoção de itens,
  redução de espaçamentos e desativação da verificação final;
- regressão obrigatória através de `renderizar_tela` ou do caminho público
  imediatamente superior;
- casos objetivos de matriz, linha e terminal pequeno real;
- critérios de aceite para altura física, não regressão sem pop-up e
  preservação dos testes diretos do pop-up;
- comandos focais e suíte completa de validação pós-implementação.

## Arquivos autorizados e teste canônico

- novo arquivo de produção autorizado: `tela/renderizacao/tela.py`;
- implementação já autorizada e preservada: `tela/renderizacao/popup.py`;
- teste canônico do compositor identificado:
  `tela/testes_renderizador/integracao.py`;
- teste canônico do fluxo modal/runtime mantido:
  `demo/teste_demo_popup.py`;
- testes diretos preservados: `tela/teste_popup.py`.

## Buscas focais usadas

- `rg -n "renderizar_tela|l_corpo_disponivel|sobrepor_no_corpo|terminal pequeno" tela demo`
- `rg -n "def renderizar_tela|_renderizar_container|_contar_linhas" tela/renderizacao/tela.py tela`
- busca focal de funções em `tela/testes_renderizador/integracao.py` para
  confirmar o arquivo canônico existente.

## Decisões e bloqueios

Nenhuma decisão de produto ou arquitetura foi criada. O patch apenas tornou
implementável, na fronteira real diagnosticada, a prioridade já aprovada
`coluna → matriz → linha → quadro mínimo de terminal pequeno`.

Não houve bloqueio. Nenhum código, ADR, contrato, nomenclatura ou backlog foi
alterado; somente o handoff H-0060 e este relatório foram materializados.
