# Relatório — PATCH_ADR ADR-0046 P03

```yaml
etapa: PATCH_ADR
objeto: docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md
patch: P03
data: 2026-08-14
```

## Achados corrigidos

**ACH-ADR0046-P03-01.** `DEC-ITEM0010-CHIP-01` associava Curva a `( … )` e
Ornamental a `╭ … ╮`, redefinindo símbolos concretos que a própria ADR
declara não escolher. A associação foi revertida ao catálogo preservado.

**ACH-ADR0046-P03-02.** Os exemplos concretos de Curva e Ornamental passam a
usar uma única unidade visual com `/` e os delimitadores do próprio preset,
sem concatenação `[PgUp][PgDn]` e sem símbolo de outro preset.

## Trechos materialmente corrigidos

Em `DEC-ITEM0010-CHIP-01`:

- removidos os exemplos `Curva (PgUp/PgDn)` e `Ornamental ╭PgUp/PgDn╮`;
- registrados explicitamente os delimitadores preservados de Curva e
  Ornamental;
- afirmado que Curva e Ornamental permanecem distintos, sem equivalência
  gráfica;
- afirmado que a decisão não redefine símbolos concretos nem escolhe novo
  schema ou renderer;
- exemplos concretos atualizados para `╭PgUp/PgDn╮` (Curva) e
  `❲PgUp/PgDn❳` (Ornamental).

Colchete `[PgUp/PgDn]`, Traço `-PgUp/PgDn-`, Ponto ` PgUp/PgDn.` e Destaque
Texto ` PgUp/PgDn ` não foram alterados. A menção a `[PgUp][PgDn]` permanece
somente como forma histórica/inválida substituída.

Nenhuma outra ocorrência de Curva, Ornamental ou associação incompatível
foi encontrada na ADR.

## Estado final

- Curva = `╭` / `╮`
- Ornamental = `❲` / `❳`
- ação multitecla = uma única unidade visual
- `/` = separador interno
- delimitadores somente nas extremidades

Demais decisões vigentes (Destaque Texto, Ponto, Destaque Fundo,
`cor_inativo`, Console `ec → tg → tx`, F1/F2/F3/F5/F11, tiling, ordem
global da Barra) não foram alteradas.

Este patch estabelece o comportamento normativo correto. Não declara que o
runtime atual já o satisfaz.

## Verificações

- busca focal na própria ADR por `Curva|Ornamental|PgUp|PgDn|multitecla|DEC-ITEM0010-CHIP-01`;
- revisão do diff focal;
- `git diff --check` nos dois arquivos permitidos.

## Bloqueios

Nenhum.
