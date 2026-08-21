# Relatório de implementação H-0077

## Arquivos alterados

- `tela/renderizacao/conteudo_externo.py`
- `tela/renderizacao/matriz_participantes.py`
- `tela/renderizacao/paginacao_interna.py`
- `tela/renderizador.py`
- `tela/teste_estilo_h0073_h0063.py` (ajuste do consumo da função removida)
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md`

`console.py` e `texto_ansi.py` não exigiram alteração. O núcleo canônico, o
popup e seus testes foram preservados.

## Migração e reconciliação

`conteudo_externo.py` deixou de definir `_quebrar_texto` e deixou de importar
`_quebrar_sem_ansi` para esse papel. Hierarquia, dois níveis por foco, tabela e
conjuntos passaram a chamar diretamente `compor_texto`. `_truncar_com_marcador`
permaneceu local e separado.

Matriz de participantes e paginação interna passaram a consumir `compor_texto`
diretamente. A medição de `_altura_quebra_item`, o mapa físico e a renderização
usam a mesma composição; a paginação fragmenta as linhas desse mapa. O
`renderizador` reexporta a referência canônica privada `_quebrar_texto` apenas
para manter compatibilidade de fachada e os imports foram reconciliados.

## Testes e demonstração

Executado o comando focal do H-0077: `621 passed, 11 failed`.
`tela/teste_composicao_textual.py` e `tela/teste_popup.py` passaram dentro da
suíte focal; `demo/teste_demo_popup.py`: `15 passed`.

As demonstrações diretas de conteúdo externo, truncamento, ESC, hierarquia
verbosa e `TestDistribuicaoMatricialH0035` produziram 118 verificações, com
117 aprovadas. As integrações H-0045 de mapa físico confirmaram a coerência
entre mapa, renderização e fragmentação nos casos aprovados.

## Desvios, exceções e bloqueios

Três falhas P16 e três falhas de demonstração P10/P12 mantêm expectativas de
contagem baseadas na antiga quebra por palavras; a composição canônica aprovada
reparte texto por largura, e medição, mapa e paginação agora concordam com essa
realidade. Uma verificação VERB-11 também espera um token contíguo que passou a
ser separado por fronteira física. Não foi alterado o núcleo nem teste
preservado para mascarar a convergência.

As sete falhas restantes da suíte focal são resíduos fora do escopo: uma
expectativa de estilo preexistente e testes H-0073 que carregam o fixture JSON
com resíduo literal já identificado no ciclo anterior. Não houve bloqueio de
escopo nem alteração fora da lista autorizada.
