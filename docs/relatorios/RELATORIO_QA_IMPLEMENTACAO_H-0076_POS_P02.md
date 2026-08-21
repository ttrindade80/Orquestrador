# QA de implementação H-0076 pós-P02

## Formação por palavras

`compor_texto` forma linhas com palavras inteiras e vãos; não corta células,
não hifeniza nem faz separação silábica. O popup referencia diretamente o
núcleo canônico.

## Palavra maior que largura

Uma palavra individual maior que a largura útil permanece em uma linha lógica
íntegra, sem truncamento, fragmentação ou hifenização.

## Recomposição

Cada chamada recebe o texto lógico completo. O núcleo não guarda linhas
anteriores, e o popup lê `instancia.conteudo["texto"]` a cada layout; resize
não reutiliza saída anterior.

## Justificação

A formação precede a justificação. A expansão atua somente nos vãos internos
entre palavras e não altera palavras. `justificar_ultima` permanece escolha do
consumidor, sem regra universal imposta pelo núcleo.

## Whitespace

`isspace` é usado apenas para reconhecer fronteiras lexicais. Os testes
verificam conteúdo lógico não branco e não fixam representação concreta de
espaços, tabs ou separadores como contrato global.

## ANSI

O núcleo reutiliza `_tokens_ansi`, estado SGR, largura visual e fechamento ou
restabelecimento de SGR de `texto_ansi.py`. CSI não é partido e palavra
estilizada permanece indivisível; não há parser concorrente de wrapping.

## Popup

`popup.py` passa o parágrafo completo a `compor_texto`, sem pré-fragmentação ou
algoritmo concorrente. Geometria, moldura e padding continuam locais; resize
recompõe corretamente.

## Testes

`PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_composicao_textual.py tela/teste_popup.py demo/teste_demo_popup.py`: `91 passed`.
`git diff --check`: passou.

## Fronteira H-0077

Nenhum consumidor funcional de H-0077 foi alterado pelo delta P02 auditado.
Não foi realizada regressão transversal de H-0077.

## Achados

Nenhum.

## Status final

`I1_IMPLEMENTATION_APPROVED`
