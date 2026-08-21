---
name: RELATORIO_PATCH_HANDOFF_H-0077_P02
handoff: H-0077
patch_handoff: P02
---

cadeia:
  raiz: docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0077.md
  origem_reabertura: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0076_POS_P02.md

decisao_aplicada:
  - D-0027-10

## Impacto do novo núcleo

O H-0077 foi reconciliado com o núcleo corrigido de H-0076: a entrada é o
parágrafo lógico completo, a composição distribui palavras inteiras em linhas
físicas e a justificação ocorre depois da formação das linhas aplicáveis.
Resize recompõe o texto lógico completo. Não há hifenização automática,
separação silábica, divisão por largura/células ou reutilização de linhas
físicas como entrada lógica. A decisão aprovada para whitespace/separadores
permanece sem política global concreta; vãos entre palavras podem participar
da justificação.

## Consumidores reconciliados

Hierarquia, dois níveis por foco, tabela e conjuntos de campos devem fornecer
ao núcleo o parágrafo lógico apropriado, sem pré-fragmentá-lo fisicamente.
Prefixos, designadores, indicadores, indentação, largura útil, estrutura de
coluna, seleção de campos, modo verboso/não verboso e truncamento deliberado
continuam locais. O escopo funcional permanece em `conteudo_externo.py`,
`matriz_participantes.py` e `paginacao_interna.py`, com
`renderizador.py` limitado a import/alias quando necessário.

## Medição, mapa e paginação

`_altura_quebra_item`, `_renderizar_participante_com_indicador` e
`_larguras_mapa_fisico_matricial` devem usar a mesma semântica de palavras
inteiras e a mesma composição efetivamente renderizada. A altura não pode
contar uma palavra longa como múltiplas linhas por fragmentação anterior. O
mapa físico e a paginação devem derivar das linhas reais, sem perda, duplicação
ou recorte baseado em uma quebra antiga.

## P16

Os três P16 serão submetidos a nova regressão semântica após D-0027-10. Se um
fixture deixar de exercer a política desejada, deverá ser reconstruído
preservando essa política; não se restaura a quebra antiga nem se altera a
paginação para satisfazer expectativas obsoletas.

## Palavra maior que a largura

O compositor mantém a palavra íntegra e não escolhe globalmente clipping,
overflow, scroll, erro, fallback, truncamento ou expansão de container.
Tratamento físico local só permanece quando for responsabilidade própria e
não alterar semanticamente a palavra dentro do compositor. Truncamento com
marcador não simula essa condição.

## ANSI

A largura continua visual, CSI permanece íntegro, SGR não vaza e palavra
estilizada é indivisível. Não se cria parser ANSI ou autoridade de wrap
paralela.

## Regressões previstas

Além da suíte focal de H-0077 e da nova validação semântica dos P16, permanece
obrigatória a regressão de H-0076:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_composicao_textual.py \
  tela/teste_popup.py \
  demo/teste_demo_popup.py
```

## Resíduo H-0070

`QA-IMPL-H0077-03` continua fora do ITEM-0027 como resíduo independente de
H-0070. Não deve ser corrigido automaticamente sem nova evidência causal.

## Bloqueios

Nenhum bloqueio documental. Esta etapa não implementa código, testes ou demo.
