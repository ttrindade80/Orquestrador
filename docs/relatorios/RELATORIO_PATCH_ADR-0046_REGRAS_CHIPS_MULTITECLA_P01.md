# Relatório — Patch ADR-0046: regras de chips multitecla (P01)

## Arquivo alterado

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`

## Decisões incorporadas

Nova seção "10. Patch normativo — composição de chips multitecla e semântica
de destaque (ITEM-0010)", inserida entre a seção 9 e "Regras anteriores
substituídas", contendo:

- `DEC-ITEM0010-CHIP-01` — composição multitecla como unidade visual única,
  teclas separadas por `/`, delimitadores externos únicos; substitui
  explicitamente a concatenação individual por tecla anteriormente adotada
  em H-0070.
- `DEC-ITEM0010-CHIP-02` — semântica do preset Ponto (espaço à esquerda,
  ponto único à direita) aplicada também à unidade multitecla.
- `DEC-ITEM0010-CHIP-03` — presets de destaque/cor seguem a mesma unidade
  multitecla; aplicação obrigatória à Barra de Menus real, sem vazamento.
- `DEC-ITEM0010-CHIP-04` — semântica de "Destaque Texto" preservada
  literalmente (espaço esquerdo na cor do terminal, direito na cor de
  destaque do fundo), sem reinterpretação e sem antecipar schema.
- `DEC-ITEM0010-CHIP-05` — `/` como separador canônico normativo, sem fixar
  sua localização arquitetural.
- `DEC-ITEM0010-CHIP-06` — composição/alinhamento por largura visual
  efetiva, desconsiderando sequências ANSI.
- `DEC-ITEM0010-CHIP-07` — hierarquia/cursor explicitamente fora deste
  patch, tratada como não conformidade de implementação já existente.

A seção também registra a relação com `MF-ITEM0010-001`, `MF-ITEM0010-002` e
`MF-ITEM0010-003`, e lista os documentos a reconciliar na aplicação futura:
`contrato_estilo.md`, `contrato_chip.md`, `contrato_barra_de_menus.md` e a
nomenclatura de estilo/chips quando afetada.

## Seções afetadas

- Nova seção "10." dentro de "## Decisão".
- Nenhuma outra seção da ADR foi alterada; decisões vigentes (seções 1 a 9,
  "Regras anteriores substituídas", "Invariantes", "Particionamento
  previsto", "Fora de escopo", "Consequências", "Detalhes deliberadamente
  não fechados", "Referências normativas") permanecem intactas.

## Consequências documentais declaradas

A própria ADR declara, na nova seção, que a aplicação posterior deverá
reconciliar `contrato_estilo.md`, `contrato_chip.md`,
`contrato_barra_de_menus.md` e a nomenclatura de estilo/chips afetada. Nenhum
desenho físico de schema ou de renderer foi antecipado.

## Verificações executadas

- Leitura integral do arquivo antes e depois da edição.
- Confirmação de que nenhum outro arquivo foi tocado (apenas a ADR e este
  relatório).
- Confirmação de que nenhuma decisão arquitetural além das fechadas neste
  prompt foi introduzida.
- Confirmação da existência final dos dois artefatos exigidos.

## Bloqueios

Nenhum. Não houve contradição entre as decisões fechadas fornecidas.
