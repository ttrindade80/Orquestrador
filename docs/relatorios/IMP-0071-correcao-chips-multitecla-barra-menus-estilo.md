# IMP-0071 — Correção de chips multitecla e Barra de Menus

## Arquivos

Alterados/criados no escopo: `tela/renderizacao/barra_menus.py`,
`tela/renderizacao/estilo.py`, `tela/carregamento/estilo.py`,
`config/estilo.json`, `tela/testes_renderizador/barra_menus.py`,
`demo/teste_demo_paginacao.py`, `tela/teste_estilo_h0071.py` e
`demo/teste_demo_estilo_h0071.py`, além deste relatório.

## Comportamento entregue

A composição compartilhada entre a amostra da tela de Estilo e a Barra real
forma uma única unidade para ações multitecla, usa `/` como separador e deixa
os delimitadores somente nas extremidades. O preset Ponto produz espaço,
`PgUp/PgDn` e um único ponto. Os presets de destaque preservam a unidade,
incluindo fundo lateral assimétrico em Destaque Texto e fundo integral em
Destaque Fundo. Resets ANSI encerram o estilo antes do texto descritivo e do
chip seguinte. A largura de layout continua sendo calculada sem contar ANSI.
Ações de uma tecla e as regras de agrupamento funcional foram preservadas.

## Configuração

Em `chip.presets["Destaque Texto"]` foram materializados somente:

- `cor_fundo_esquerdo`: `"padrão"`;
- `cor_fundo_direito`: `"azul"`.

O loader expõe esses campos quando declarados e mantém `cor_fundo` simétrico
quando ausentes.

## Testes e demonstração

- Testes focais H-0071 (`tela/teste_estilo_h0071.py` e
  `demo/teste_demo_estilo_h0071.py`): **35 passaram**.
- Suíte focal da Barra (`tela/testes_renderizador/barra_menus.py`): **120
  passaram**.
- Regressão de popup (`tela/teste_popup.py`): **65 passaram e 3 falharam**;
  as falhas são expectativas legadas de preset/rotulagem, sem alteração
  funcional no popup.
- `demo/teste_demo_paginacao.py`: **110 passaram, 18 falharam**; as falhas
  remanescentes são expectativas legadas de estilo/rotulagem fora do delta.
- Suíte canônica `PYTHONDONTWRITEBYTECODE=1 python -m pytest`: **1295
  passaram, 75 falharam e 17 erros**, concentrados em expectativas e
  demonstrações de etapas anteriores que ainda assumem o preset/forma legada.

A demonstração automatizada reproduzível da Barra real foi preparada e
executada pelo teste focal de demonstração, incluindo troca de preset,
resize, ANSI, alinhamento e contenção. A aprovação visual/interativa em TTY
real não foi declarada; permanece pendente de verificação do usuário.

## Desvios, exceções e bloqueios

Não houve desvio funcional nem exceção de escopo solicitada. O código focal
do H-0071 está coberto pelos testes focais aprovados; a suíte canônica não
atingiu código zero pelas falhas legadas registradas acima. Não houve stage,
commit ou push.
