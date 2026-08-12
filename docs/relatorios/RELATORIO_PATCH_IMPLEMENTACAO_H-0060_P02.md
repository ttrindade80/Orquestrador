# Relatório do patch de implementação H-0060 P02

## Cadeia

- raiz: `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0060_P01.md`

## Achado tratado

- `MV-H0060-001`

## Causa factual

O resize TTY atualiza corretamente o par físico `(largura, altura)` antes do
redesenho. A falha ocorre na integração de `renderizar_tela`: a altura física
reservada ao corpo é calculada em `l_corpo_disponivel`, mas o corpo subjacente
pode ser materializado por `_renderizar_container` com uma altura natural
maior. A sobreposição recebe `_contar_linhas(bloco_corpo)`, isto é, essa altura
natural excedente, e não `l_corpo_disponivel`.

Consequentemente, o pop-up recalcula sua formação contra uma área maior que a
área física realmente disponível. Depois da sobreposição, a verificação final
de ocupação de `renderizar_tela` detecta que o corpo excede
`l_corpo_disponivel` e lança `RenderizadorErro`. `_resolver_conteudo` classifica
essa exceção como insuficiência geométrica e substitui todo o quadro pela
mensagem `Terminal pequeno demais`.

Sondagens focais no caminho de integração mostraram, entre outros casos:

- `80x22`: área física do corpo igual a 16 linhas, corpo materializado com 17;
  o pop-up ainda permanece em coluna e o renderer rejeita o corpo em seguida;
- `80x18`: área física do corpo igual a 12 linhas, na qual a coluna já não
  cabe e uma matriz é válida, mas o pop-up recebe 14 linhas, mantém coluna e o
  renderer produz insuficiência geométrica;
- `77x14`: área física do corpo igual a 8 linhas, na qual a linha é válida,
  mas o pop-up recebe 12 linhas, escolhe matriz e o renderer produz
  insuficiência geométrica.

## Caminho runtime

1. `demo.demo._instalar_handler_sigwinch` sinaliza o resize pelo wakeup pipe.
2. `demo.demo.main` obtém o novo par em `_obter_dimensoes_apos_sigwinch`,
   atualiza `largura` e `altura` e chama `_resolver_conteudo`.
3. `_resolver_conteudo` chama `renderizar_estado`.
4. `renderizar_estado` chama `tela.renderizador.renderizar_tela`, implementado
   por `tela/renderizacao/tela.py`.
5. `renderizar_tela` calcula `l_corpo_disponivel`, materializa o corpo e chama
   `sobrepor_no_corpo` com `altura_corpo = _contar_linhas(bloco_corpo)`.
6. `sobrepor_no_corpo` e `_layout_popup_marcacao` recalculam a formação usando
   essa altura natural excedente.
7. A verificação final de `renderizar_tela` decide que o corpo não cabe e
   lança a insuficiência geométrica.
8. `_resolver_conteudo` converte a exceção no quadro vigente de terminal
   pequeno.

## Relação com o layout do pop-up

`tela/renderizacao/popup.py` já recalcula coluna, matriz e linha a partir das
dimensões que recebe. O defeito não está na seleção das formações: o nível de
integração entrega ao pop-up uma altura diferente da área física reservada e,
em seguida, aplica a decisão global com a altura correta.

## Arquivos necessários e autorização

- Produção necessária: `tela/renderizacao/tela.py`, função
  `renderizar_tela`, na fronteira entre `l_corpo_disponivel`, a materialização
  do corpo e `sobrepor_no_corpo`.
- Teste regressivo, após autorização de produção:
  `demo/teste_demo_popup.py`, atravessando `_resolver_conteudo` para matriz,
  linha e quadro mínimo.

`tela/renderizacao/tela.py` não está entre os arquivos permitidos para escrita
neste patch e o H-0060 determina não alterar o dispatcher/compositor geral.
Portanto, nenhuma correção de produção ou teste regressivo foi aplicada.

A menor alteração esperada é especializar, em `renderizar_tela`, a área do
corpo usada pela sobreposição quando existe pop-up aberto, entregando ao
pop-up a cota física `l_corpo_disponivel` e materializando um bloco de corpo
com exatamente essa altura antes da sobreposição. A política geral sem pop-up
deve permanecer inalterada. O detalhe de composição dessa especialização
precisa ser autorizado por `PATCH_HANDOFF` antes da implementação.

## Testes

Os testes obrigatórios pós-correção não foram executados, pois nenhuma
correção é permitida dentro do escopo vigente. Não foi realizada QA
pós-patch nem validação manual. As únicas execuções foram sondagens
diagnósticas, sem escrita, do caminho de integração descrito acima.

## Bloqueio

- status: `BLOCKED_SCOPE`
- caminho: `tela/renderizacao/tela.py`
- motivo: a correção de `MV-H0060-001` exige alterar a fronteira de produção
  que fornece a altura física ao pop-up, fora dos arquivos autorizados pelo
  H-0060/P02.
