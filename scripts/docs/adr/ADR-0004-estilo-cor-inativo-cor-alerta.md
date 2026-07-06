---
name: ADR-0004-estilo-cor-inativo-cor-alerta
description: Inclusão dos campos cor_inativo e cor_alerta como nomes semânticos de cor no schema de estilo
metadata:
  type: adr
  status: aceita
  data: 2026-07-05
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_estilo.md
  handoffs_bloqueados: []
---

# ADR-0004 — `cor_inativo` e `cor_alerta` no schema de estilo

## Status

`aceita`

## Contexto

O schema de estilo (`contrato_estilo.md`, status: `ativo`) expõe campos de
cor para chip (`cor_texto`, `cor_fundo`), mas não possui campos para estados
dinâmicos de renderização. A seção 1.5 de `docs/NOMENCLATURA.md` definiu dois
campos genéricos que cobrem esses estados:

- **`cor_inativo`**: cor aplicada quando um elemento existe mas está
  temporariamente inativo (ex.: chip de paginação `[<]` existe porque a
  classe declarou `paginacao: com`, mas fica inativo quando há só uma página).
- **`cor_alerta`**: cor aplicada quando um valor atinge um limite que exige
  destaque visual (ex.: mínimo ou máximo de uma escala).

Esses campos são genéricos — aplicam-se a qualquer chip ou indicador do
sistema quando houver estado dinâmico correspondente, não são exclusivos de um
chip isolado.

Como `contrato_estilo.md` já está `ativo`, a inclusão desses campos não pode
ser feita diretamente no contrato — deve entrar via ADR primeiro, conforme
regra 6 do processo (`docs/build_docs/instruction.md`) e seção 12 de
`docs/NOMENCLATURA.md`.

Distinção de conceito central desta ADR:

- **Existência** de um elemento = propriedade estrutural, declarada pela
  classe de tela. A classe decide se o chip ou indicador existe naquela tela.
- **Ativo/inativo e alerta** = estados dinâmicos de renderização, recalculados
  a cada render a partir do conteúdo atual. O renderer aplica a cor
  correspondente, mas não decide a existência estrutural do elemento.

## Decisão

O schema de estilo passa a conter dois campos genéricos de cor para estados
dinâmicos:

| Campo | Função |
|---|---|
| `cor_inativo` | Nome semântico de cor aplicada quando um elemento existe mas está temporariamente inativo |
| `cor_alerta` | Nome semântico de cor aplicada quando um valor ou limite exige destaque visual |

Ambos os campos seguem exatamente as mesmas regras de `cor_texto` e
`cor_fundo` (seção 3.2 de `contrato_estilo.md`):

- São nomes semânticos de cor (strings), ex.: `"cinza"`, `"amarelo"`,
  `"padrão"`.
- A tradução do nome semântico para valor de terminal (ANSI, paleta, etc.)
  é responsabilidade exclusiva do renderer, nunca do schema.
- Hardcoding de qualquer um desses valores é violação contratual (R-2).
- Ambos os campos são obrigatórios no schema — a ausência de qualquer um
  torna o schema inválido (R-3).

A existência estrutural do elemento continua sendo decisão da classe de tela.
Ativo/inativo e alerta são estados de renderização — o renderer aplica a cor,
mas não decide se o elemento existe.

## Consequências

- O schema de estilo passa a expor dois campos para estados dinâmicos de cor,
  permitindo que renderers de qualquer chip ou indicador representem esses
  estados sem hardcoding.
- `contrato_estilo.md` recebe nova seção no schema (3.5) e atualizações nas
  regras R-3 e nos critérios de validação (seção 5).
- Nenhuma alteração em `contrato_composicao_corpo.md`, nos contratos de
  `menu`, `dado` ou `Info`, nem em `config/estilo.json` (ainda pendente —
  DOC-0005 trata dos valores concretos).
- O renderer é responsável por decidir quando aplicar `cor_inativo` ou
  `cor_alerta` com base no estado dinâmico recebido — o schema declara os
  campos, não a lógica de quando usá-los.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Embutir `cor_inativo`/`cor_alerta` diretamente na seção de chip (3.2) | Esses campos não são exclusivos do chip — aplicam-se a qualquer chip ou indicador; embutir em 3.2 violaria a generalidade declarada em NOMENCLATURA.md seção 1.5 |
| Tratar como metadados da classe de tela, não do schema de estilo | Contradiz a separação estilo × composição: cor é responsabilidade do schema de estilo, não da estrutura da tela |
| Definir como campos opcionais | Optionalidade introduz inconsistência entre implementações; a regra de completude do schema (R-3) é um invariante do contrato |
