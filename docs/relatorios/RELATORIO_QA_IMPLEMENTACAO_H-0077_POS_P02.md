---
item: ITEM-0027
adr: ADR-0049
decisao: D-0027-10
patch: H-0077 P02
---

# QA de implementação H-0077 pós-P02

## Alterações auditadas

O delta do P02 restringe-se aos fixtures/expectativas de `tela/teste_formato_filho_dois_niveis_por_foco.py`, `tela/teste_paginacao.py` e `tela/teste_estilo_h0073_h0063.py`, além deste relatório. Não houve nova alteração funcional no núcleo ou nos consumidores; a migração anterior permanece consumindo `compor_texto`.

## Dois níveis por foco

Os dois focos usam `Valor um`, com duas palavras lógicas. Produzem multilinha real após compactação, uma única identidade lógica, continuação sem novo cursor e sem novo toggle/indicador. Não há fragmentação, hifenização ou recomposição de linhas físicas anteriores.

## P16

O fixture usa palavras de 37 colunas em largura textual efetiva 76: 7/5 palavras produzem 4/3 linhas e 17 palavras produzem 9 linhas. Os três testes passam e preservam fluxo contínuo, movimento integral condicional e item maior que a página. A paginação funcional não foi alterada; nenhuma expectativa depende de palavra partida.

## ANSI

O caso usa duas palavras estilizadas (`A B`) com `CSI/SGR` íntegros. Os testes confirmam reset, ausência de CSI incompleto/vazamento, largura visual e palavras não partidas.

## Consumidores, medição, mapa e paginação

`conteudo_externo.py`, `matriz_participantes.py`, `paginacao_interna.py` e `renderizador.py` continuam referenciando o núcleo canônico. Medição, renderização, mapa físico e paginação derivam a mesma composição lógica. Palavra maior que a largura permanece íntegra, sem truncamento, divisão, hifenização ou fallback. `_truncar_com_marcador` permanece separado e deliberado.

## Autoridade única

A busca encontrou uma implementação genérica em `composicao_textual.py`; `_quebrar_sem_ansi` é apenas a primitiva ANSI interna, e os demais usos são import/alias compatíveis. Não há autoridade concorrente. `git diff --check`: passou.

## Testes

- Suíte focal: `635 passed, 1 failed`.
- Regressão H-0076: `91 passed`.
- P16 isolado: `3 passed`.
- Dois níveis autorizados: `2 passed`.

## H-0070 e achados

A única falha é `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`, com a mesma causa independente registrada como `QA-IMPL-H0077-03`. H-0070 não foi alterado e não há nexo causal com D-0027-10/P02.

Achados: nenhum.

## Status final

`I1_IMPLEMENTATION_APPROVED`
