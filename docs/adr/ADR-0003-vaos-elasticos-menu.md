---
name: ADR-0003-vaos-elasticos-menu
description: Vãos do corpo tipo menu deixam de ser fixos e passam a ser elásticos com mínimo e máximo, parametrizados por config/layout_menu.json
metadata:
  type: adr
  status: aceita
  data: 2026-07-05
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
  handoffs_bloqueados: []
---

# ADR-0003 — Vãos elásticos do `menu`

## Status

`aceita`

## Contexto

A seção 5.2 de `contrato_composicao_corpo.md` definia a distância entre chip
(`[X]`) e texto do item de `menu` como **fixa em 2 espaços**. Nenhuma regra
explícita existia para o espaçamento entre itens na mesma linha, entre colunas
da grade em modo `matriz`, nem entre a borda e o primeiro/último elemento.

Decisão fechada em sessão de 2026-07-05 (`docs/NOMENCLATURA.md` seção 8.1):
os vãos do corpo tipo `menu` passam a ser **elásticos** — cada vão tem um
mínimo (usado para calcular se a distribuição cabe na largura disponível) e
um máximo (até onde o vão pode crescer para absorver a sobra). Essa regra
vale para modo `fila` e modo `matriz`.

A decisão complementa ADR-0001 (que definiu o algoritmo de seleção de modo
usando vãos no mínimo como critério de corte) e ADR-0002 (que estabeleceu
que a sobra além da largura do bloco fica à direita). Os valores concretos
de mínimo e máximo são parametrizados em `config/layout_menu.json`.

A decisão não afeta corpo tipo `dado`, o objeto `Info`, nem as regras de
paginação.

## Decisão

Os vãos do corpo tipo `menu` são elásticos, com mínimo e máximo definidos
em `config/layout_menu.json`. As regras são:

### Vão chip↔rótulo (entre `[X]` e o texto do item)

| Parâmetro | Valor |
|---|---|
| Mínimo | `1` espaço |
| Máximo | `3` espaços |

### Vão entre itens / entre colunas / borda↔extremo

Aplica-se ao espaçamento entre itens consecutivos na mesma linha (modo
`fila`), entre colunas adjacentes da grade (modo `matriz`), e entre a borda
do bloco e o primeiro/último elemento.

| Parâmetro | Valor |
|---|---|
| Mínimo | `2` espaços |
| Máximo | `5` espaços |

### Algoritmo de distribuição elástica

1. O renderer calcula a distribuição usando os vãos **no mínimo** para
   determinar se o layout cabe na largura disponível (critério de ADR-0001
   permanece inalterado).
2. Uma vez encontrada a distribuição que cabe, os vãos entre itens/colunas
   crescem primeiro até o máximo definido para absorver a sobra de espaço
   horizontal disponível dentro do bloco.
3. Depois que esses vãos atingem o máximo, a margem borda↔elemento recebe o
   restante até seu próprio teto.
4. Só depois de todos os tetos serem atingidos, a sobra excedente permanece
   inteiramente à direita do bloco, conforme ADR-0002.

### Abrangência

Esta regra vale para os dois modos de layout do corpo tipo `menu`:

| Modo | Vãos afetados |
|---|---|
| `fila` | chip↔rótulo de cada item; entre itens consecutivos na linha; borda↔primeiro item e último item↔borda |
| `matriz` | chip↔rótulo de cada item; entre colunas adjacentes; borda↔primeira coluna e última coluna↔borda |

### Parametrização

Os valores de mínimo e máximo são lidos de `config/layout_menu.json`. Esta
ADR formaliza a decisão e os valores; a materialização do arquivo JSON é
escopo de item separado.

## Consequências

- Os vãos do `menu` deixam de ser fixos — o renderer passa a calcular a
  distribuição elástica a partir dos parâmetros de `config/layout_menu.json`.
- O critério de corte do algoritmo de seleção de modo (ADR-0001) não muda:
  usa vãos no mínimo, agora com valores explícitos.
- Sobra além dos máximos acumula à direita do bloco (ADR-0002 preservada).
- Corpo tipo `dado`, objeto `Info` e regras de paginação não são afetados.
- `contrato_composicao_corpo.md` seção 5.2 (alinhamento horizontal) e os
  critérios de validação correspondentes na seção 7 são atualizados junto
  com esta ADR.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Manter vão chip↔rótulo fixo em 2 | Contraria a decisão fechada em sessão de 2026-07-05 |
| Vão único para todos os espaçamentos | Semântica diferente justifica valores distintos: vão interno ao item (chip↔rótulo) deve ser mais compacto que vão entre itens |
| Distribuição proporcional à posição | Não foi esta a decisão — primeiro crescem vãos entre itens/colunas, depois margem borda↔elemento, e só então sobra excedente fica à direita |
| Aplicar mesma regra ao `dado` e ao `Info` | `dado` e `Info` estão fora de escopo desta ADR |
