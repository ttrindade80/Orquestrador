# Relatório — QA_HANDOFF_POS_PATCH H-0076 P01

## D-0027-10

O P01 operacionaliza integralmente a decisão: o texto lógico completo é a
entrada, as palavras formam as linhas, a justificação vem depois e a saída é
representada fisicamente. O popup permanece consumidor focal, sem autoridade
local concorrente, preservando geometria, moldura, largura útil e modo como
responsabilidades locais.

## Formação por palavras e resize

As palavras são indivisíveis: não há divisão por largura, células,
hifenização, separação silábica ou repartição de segmento longo. Cada resize
recompõe o parágrafo inteiro a partir do texto lógico, sem reutilizar linhas
físicas anteriores.

## Justificação

As linhas são formadas antes da justificação, que atua somente nos vãos entre
palavras das linhas aplicáveis, sem prescrever distribuição matemática,
restos, quantidade de espaços ou política para linha de uma palavra.

## Palavra maior que largura

O requisito comum limita-se a não dividir nem alterar semanticamente a
palavra. Clipping, overflow, scroll, erro, fallback, truncamento e expansão
de container permanecem fora da decisão.

## Última linha

Permanece neutra. Eventual parâmetro histórico só pode ser compatibilidade
local do consumidor, não regra do núcleo.

## Testes

Os testes previstos detectam formação por palavras, recomposição global em
larguras distintas, palavra larga sem política física, justificação posterior
nos vãos, e ANSI por largura visual, CSI, SGR e palavras estilizadas. Também
preveem a reprodução manual de `h0077_texto_amplo_justificado`, com largura
ampla, redução progressiva, aumento e verificação visual. O escopo futuro
disponibiliza núcleo, popup, testes do núcleo/popup/demo e `texto_ansi.py`
condicionalmente.

## Fronteira H-0077

H-0077 não é reconciliado nem autoriza alterações funcionais nos consumidores
externos; regressão e reconciliação ficam para depois da aprovação do núcleo.

## Achados

Nenhum.

## Status final

`H1_HANDOFF_APPROVED`
