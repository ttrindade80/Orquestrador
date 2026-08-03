# Relatório de análise de causa raiz — H-0045 largura horizontal

## Medição reproduzível

A medição foi feita por chamadas diretas a `geometria_console`,
`mapa_fisico_de_itens`, `plano_de_paginacao` e ao caminho público do renderer;
não houve interação em TTY. Neste ambiente, stdin/stdout não são TTY,
`COLUMNS`/`LINES` estão ausentes e `shutil.get_terminal_size(fallback=(80,24))`
resolve 80×24. Em TTY real, a demo obtém a largura via `ioctl` e a atualiza no
`SIGWINCH` (`demo/demo.py:1211-1252, 1444-1451, 1485-1509`).

No caso principal `h0045_validacao_continuacao`, em modo verboso e console
focalizado, a composição declara margem esquerda/direita de 1 coluna e o
indicador consome 2 colunas:

| terminal | console externo | interno / conteúdo | paginação (argumento / área efetiva) | quebra recebida | maior linha | úteis não usadas |
|---:|---:|---:|---:|---:|---:|---:|
| 80 | 80 | 78 / 77 | 80 / 77 | 37 | 36 | 37 |
| 120 | 120 | 118 / 117 | 120 / 117 | 57 | 56 | 57 |
| 160 | 160 | 158 / 157 | 160 / 157 | 77 | 76 | 77 |
| 200 | 200 | 198 / 197 | 200 / 197 | 97 | 96 | 97 |

“Úteis não usadas” é a capacidade textual esperada após conteúdo, as duas
margens e o indicador (`W-7`), menos a maior linha física produzida. O mesmo
alocador entregou células 39/59/79/99, portanto a quebra ficou praticamente
em metade da área textual disponível. As cinco telas H-0045 comparadas
(`continuacao`, `fluxo_continuo`, `nova_pagina`, `manter_junto` e
`paginacao_modo_verboso_multilinha`) apresentam a mesma sequência de larguras;
varia apenas o comprimento natural da última palavra de cada linha.

## Causa e abrangência

Até `geometria_console`/`_caixa_de_elemento`, a geometria está correta:
largura externa = `W`, área interna após bordas = `W-2` e conteúdo do envelope =
`W-3` (`tela/renderizador.py:3294-3334, 4332-4340`). A primeira divergência
surge em `_linhas_distribuicao_matricial`, linha 3074: no ramo verboso,
`min_ws` limita `texto_min` a `(area_w - ind_w) // 2`. A distribuição recebe
esse mínimo e não expande a célula única até a margem direita. O mesmo cálculo
é duplicado em `_larguras_mapa_fisico_matricial`, linha 2683, que alimenta o
mapa usado pela paginação. Assim, renderer e paginação concordam sobre uma
largura incorreta; a paginação não recebe uma largura menor por integração.

Causa direta: teto arbitrário de metade da área no cálculo de `min_ws`.
Causa contribuinte: a política de alocação usa o mínimo calculado como largura
da célula; as margens e o indicador são consumidos uma vez e não há evidência
de desconto duplicado. O valor esperado para o texto no caso principal era
73/113/153/193; o recebido foi 37/57/77/97.

O defeito afeta as cinco telas H-0045, não somente `continuacao`, e também o
ramo comum de qualquer console com `distribuicao_matricial`, modo verboso e
itens internos sem conteúdo externo. Não afeta automaticamente todo console:
o caminho externo anterior H-0037 (`h0037_console_verboso_dois_niveis`) mediu
156 caracteres em 157 de conteúdo a 160 colunas, sem o teto pela metade.
Não há quebras fixas nos textos JSON; a string chega inteira e
`_quebrar_texto` cria as linhas (`renderizador.py:2597-2602`). Os construtores
adaptativos legados não são usados pelas cinco telas fixas.

## Hipóteses

H1 limite fixo: **REFUTADA** (o limite escala com `W`, embora seja metade).
H2 largura na configuração: **REFUTADA** (não há largura fixa/máxima; há apenas
cardinalidade e margens). H3 modelo antigo: **REFUTADA** (resize repassa a
largura corrente e preserva o modelo). H4 redução duplicada: **REFUTADA**.
H5 paginação incorreta: **PARCIALMENTE_CONFIRMADA** (o mapa paginado reproduz
o cálculo errado, mas recebe `W` e o desconto estrutural correto).
H6 conteúdo previamente quebrado: **REFUTADA**. H7 fixture exclusiva:
**REFUTADA**. H8 limitação geral do console: **PARCIALMENTE_CONFIRMADA**,
restrita ao ramo matricial verboso de itens internos.

## Próximas ações

Camada responsável: cálculo de layout/distribuição, com duplicação do cálculo
no mapa físico usado pela paginação. Arquivo de implementação provável:
`tela/renderizador.py`; não há necessidade evidenciada de alterar demo, JSON ou
`tela/paginacao.py`. Testes necessários: quatro larguras nos cinco pontos de
entrada, assert de largura da célula/quebra e igualdade renderer–paginação;
regressão de resize e de console externo H-0037.

Teste manual focal posterior: executar `python demo/demo.py
h0045_validacao_continuacao` em terminal largo e redimensionar, verificando
texto até a margem interna direita, indicador de página preservado e ausência
de overflow/truncamento.

Bloqueios: nenhum para determinar a causa. Não houve correção, QA, validação
manual, stage ou commit; nenhuma validação anterior foi reaberta.

Próxima categoria: **PATCH_IMPLEMENTACAO**.
