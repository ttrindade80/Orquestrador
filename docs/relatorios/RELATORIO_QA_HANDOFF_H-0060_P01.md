# Relatório QA do handoff H-0060 P01

status: H1_HANDOFF_APPROVED

## Escopo auditado

O handoff transporta corretamente a causa de `MV-H0060-001`: `renderizar_tela`
calculava o pop-up com a altura natural excedente do corpo, embora
`l_corpo_disponivel` fosse a cota física reservada, e a verificação final depois
convertesse o excesso em terminal pequeno.

`tela/renderizacao/tela.py` foi explicitamente incorporado à autorização de
produção. A autorização está limitada ao caminho de `renderizar_tela` quando há
pop-up aberto, entre `l_corpo_disponivel`, materialização do corpo,
`sobrepor_no_corpo` e a verificação final de ocupação. A política geral sem
pop-up permanece explicitamente inalterada. `popup.py` continua sendo a
implementação aprovada das formações e não é reaberto sem necessidade
demonstrada.

## Invariantes e fronteiras

As sete invariantes físicas exigidas estão presentes: a sobreposição deve usar
a altura física real; a altura natural excedente não pode ser apresentada como
espaço; o bloco de sobreposição deve ter a cota física exata; a verificação
final não pode ser desativada ou contornada; composição maior que a região
reservada não é aceita; o caminho sem pop-up não muda; e o quadro mínimo segue
vigente quando nenhuma formação cabe.

O handoff também proíbe truncamento, paginação, remoção de itens, reticências,
redução silenciosa de espaçamento, corte da instrução ou dos chips e qualquer
alteração genérica da composição sem pop-up. Os requisitos já aprovados de
`popup.py` (colunas, matriz, linha, vão, navegação e marcações) permanecem fora
de reabertura desnecessária.

## Regressão de integração

O arquivo canônico `tela/testes_renderizador/integracao.py` foi identificado e
incluído no handoff. A regressão exigida deve atravessar `renderizar_tela` (ou
superior público equivalente), não apenas funções de layout, e deve preservar
também um caso sem pop-up.

Os três casos estão objetivos e implementáveis:

* matriz: coluna fisicamente inválida, matriz válida, renderização completa sem
  terminal pequeno;
* linha: coluna e matriz fisicamente inválidas, linha válida, renderização
  completa sem terminal pequeno;
* terminal pequeno real: nenhuma das três formações cabe e o quadro vigente é
  produzido.

Os valores diagnósticos 80x18 e 77x14 são corretamente tratados como pontos de
partida, não como política normativa. `tela/teste_popup.py` e
`demo/teste_demo_popup.py` permanecem como regressões dos testes já aprovados e
do fluxo de demonstração.

## Implementabilidade e decisão

O escopo corrigido permanece uma única unidade implementável: dois arquivos de
produção da mesma fronteira (`popup.py` e `tela.py`) e os testes canônicos
correspondentes. A distinção entre altura natural e área física, bem como as
invariantes de saída, é suficiente para orientar a escolha interna de
materialização do bloco sem introduzir política nova. Não há lacuna que exija
decisão arquitetural, documental ou de usuário.

O item `ITEM-0028` e seu objetivo no backlog permanecem coerentes com a
ampliação focal.

## Achados materiais

Nenhum. O handoff P01 resolve o `BLOCKED_SCOPE` de `MV-H0060-001` sem ampliar
indevidamente o escopo ou reabrir decisões já aprovadas.

## Materialização

`docs/relatorios/RELATORIO_QA_HANDOFF_H-0060_P01.md` foi criado no caminho
nominal. Nesta etapa de QA, nenhum arquivo auditado foi escrito ou corrigido.
