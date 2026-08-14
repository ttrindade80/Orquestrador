# RELATORIO_APLICACAO_ADR-0046_POS_P02

## Baseline

- ADR: `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` (pós-PATCH_ADR P02).
- QA da ADR: `ADR_APPROVED_WITH_NOTES`.
- Etapa: aplicação documental somente das correções do P02.
- Código, testes, handoffs e demais ADRs: não alterados. Commit: não realizado.

## Arquivos efetivamente alterados

- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `config/estilo.json`

Preservado sem alteração: `docs/nomenclatura/32_CONSOLE.md`.

## Destaque Texto — remoção da assimetria

A semântica vigente é a do P02 (`DEC-ITEM0010-CHIP-04`): somente o foreground do conteúdo recebe a cor de destaque; fundo normal em toda a unidade; um espaço normal à esquerda e à direita; nenhum fundo destacado lateral.

`cor_fundo_esquerdo` e `cor_fundo_direito` não possuíam outra autoridade nem uso vigente independente: foram criados exclusivamente para a interpretação anterior de fundo assimétrico. Removidos:

- do schema (`contrato_estilo.md` §3.2; extensão opcional e critério de validação);
- da nomenclatura (`10_ESTILO.md` termos e §4.3);
- da relação de chip com estilo (`contrato_chip.md` §12);
- da materialização concreta em `chip.presets["Destaque Texto"]`.

O preset concreto restante é `cor_texto: "azul"`, `cor_fundo: "padrão"`, delimitadores espaço. Ponto e Destaque Fundo permanecem intactos.

## Identificador × forma física

`[PgUp][PgDn]` permanece identificador documental das duas teclas/controles. A forma física renderizada da ação única é `[PgUp/PgDn]` (preset Colchete), com `/` e delimitadores só nas extremidades.

Nenhum trecho vigente dos artefatos alterados chama `[PgUp][PgDn] Páginas` de representação física ou visual canônica. Reconciliação explícita em `21_LAYOUT` §4.8/§5 e `31_BARRA_DE_MENUS_E_CHIPS` §4.3.1/§4.4.2/§5/§7; `contrato_chip.md` §9/§10.1; `contrato_barra_de_menus.md` §18.1/§24.4.

## `cor_inativo`

Regra já vigente tornada explícita nos contratos afetados e em `31`: chip existente funcionalmente ativo usa aparência ativa; inativo usa `cor_inativo`; composição, preset e aplicação de cor/fundo não a neutralizam — inclusive Páginas e `Enter/Aplicar` quando inativos. Nenhuma política nova de estado.

## `ec → tg → tx`

`32_CONSOLE.md` permanece autoridade terminológica: ordem `ec`, `tg`, `tx` com posições distintas. Nenhum documento alterado pelo ITEM-0010 nesta etapa revoga ou contradiz essa estrutura. O módulo não foi modificado.

## Campos removidos ou preservados

| Campo / artefato | Situação | Autoridade |
|---|---|---|
| `cor_fundo_esquerdo`, `cor_fundo_direito` | Removidos de schema, nomenclatura e `config/estilo.json` | ADR-0046 P02: não exigidos por Destaque Texto; sem outro uso vigente |
| cinco campos obrigatórios de chip | Preservados | `contrato_estilo.md` §3.2 |
| Ponto (` ` / `.`) | Preservado | `DEC-ITEM0010-CHIP-02` |
| Destaque Fundo | Preservado | `DEC-ITEM0010-CHIP-03` |
| `/` como separador | Preservado | `DEC-ITEM0010-CHIP-05` |
| contenção ANSI e largura visual efetiva | Preservadas | `DEC-ITEM0010-CHIP-03`, `-06` |
| `cor_inativo` | Preservado e explicitado | ADR-0004; preservação ADR-0046 |

## Delta terminológico

Removidos: `cor_fundo_esquerdo`, `cor_fundo_direito`, “assimetria de Destaque Texto”, “representação canônica `[PgUp][PgDn] Páginas`” como forma visual.

Nomeados/explicitados: identificador documental `[PgUp][PgDn]`; forma física `[PgUp/PgDn]`; Destaque Texto = foreground destacado com fundo normal simétrico.

## Verificação final

1. Nenhum texto vigente define fundo assimétrico para Destaque Texto.
2. Destaque Texto usa apenas foreground destacado.
3. `[PgUp/PgDn]` é a renderização física.
4. `[PgUp][PgDn]` não é chamado de representação visual canônica.
5. `cor_inativo` continua obrigatório.
6. Ponto e Destaque Fundo intactos.
7. `ec → tg → tx` não contradito.
8. Nenhum código, teste ou handoff alterado.

## Bloqueios

Nenhum bloqueio documental. A implementação ainda contém leitura opcional dos campos laterais; correção de código fica fora desta etapa.

## Status

`ADR_APPLICATION_COMPLETED`
