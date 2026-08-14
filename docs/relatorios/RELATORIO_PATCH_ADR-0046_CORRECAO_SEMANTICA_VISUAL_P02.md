# Relatório — PATCH_ADR-0046 P02

## Item

`ITEM-0010` — correção normativa sem aplicação da ADR.

## Correções e preservações

- **Destaque Texto corrigido:** o preset altera somente o foreground do
  texto/conteúdo. A unidade inteira, incluindo os espaços normal à esquerda e
  à direita, mantém o fundo normal do terminal. Não há fundo destacado à
  direita nem assimetria de fundo.
- **Notação documental × renderização multitecla:** `[PgUp][PgDn]` pode
  permanecer como identificador documental de teclas/controles. A renderização
  física de uma única ação é uma unidade com `/`, como `[PgUp/PgDn]`.
- **`cor_inativo`:** permanece obrigatório para chip existente funcionalmente
  inativo, inclusive Páginas e Aplicar quando inativos; a nova composição não
  pode neutralizá-lo.
- **Console:** a estrutura `ec → tg → tx` permanece vigente e com posições
  distintas; a autoridade comportamental continua nos documentos próprios do
  Console.
- **Demais decisões:** Ponto, Destaque Fundo e as demais decisões não
  abrangidas por este patch foram preservados.

## Consequências para aplicação documental posterior

Contratos, nomenclatura, schema e configuração concreta criados ou alterados
exclusivamente para a interpretação anterior de fundo assimétrico deverão ser
reconciliados. Esta ADR não decide quais campos físicos serão removidos. A
aplicação deve eliminar somente semântica ou estrutura sem outra autoridade ou
uso vigente.

## Bloqueios

Nenhum bloqueio para concluir o PATCH_ADR P02. A aplicação documental,
incluindo eventual reconciliação física, permanece fora desta etapa. O
worktree já continha alterações e arquivos fora do manifesto; foram apenas
constatados e preservados. Os únicos arquivos escritos nesta etapa são os dois
do manifesto.
