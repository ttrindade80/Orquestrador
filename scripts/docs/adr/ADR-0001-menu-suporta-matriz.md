---
name: ADR-0001-menu-suporta-matriz
description: menu deixa de ser fixo em coluna única e passa a suportar modo matriz de múltiplas colunas, calculado automaticamente pela largura do terminal
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

# ADR-0001 — `menu` suporta modo matriz (múltiplas colunas)

## Status

`aceita`

## Contexto

O contrato `contrato_composicao_corpo.md` (seção 5.1 e R-6) especificava que
corpo tipo `menu` tem um único modo de layout: lista vertical em coluna única,
sem colunas e sem paginação.

Decisão fechada em sessão de 2026-07-05 (`docs/NOMENCLATURA.md` seções 3, 6
e 8): o `menu` deve aproveitar a largura disponível do terminal — se todos os
itens couberem em uma linha com vãos mínimos, usa modo `fila` (linha única horizontal);
caso contrário, distribui em modo `matriz` (múltiplas colunas). O cálculo é
automático pelo renderer; não é declarado pela classe de tela nem ajustável
manualmente via chip.

A restrição "sem colunas" da seção 5.1 e a afirmação "único modo de layout"
da R-6 precisam ser atualizadas.

## Decisão

O corpo tipo `menu` passa a ter dois modos de layout, governados pelo eixo
`distribuicao_menu` calculado pelo renderer:

| Modo | Descrição |
|---|---|
| `fila` | Todos os itens em uma única linha horizontal |
| `matriz` | Grade de múltiplas colunas |

**Algoritmo de seleção de modo:**

1. Tenta encaixar todos os itens em uma única linha (`n_col` = total de
   itens) com vãos no mínimo. Se couber → modo `fila`.
2. Se não couber → modo `matriz`: maximiza o número de colunas com vãos no
   mínimo; reduz colunas (adiciona uma linha) somente se a distribuição não
   couber na largura disponível. Sem teto absoluto de colunas.

**Regras do modo `matriz`:**

- Largura de cada coluna = largura do maior item daquela coluna específica
  (não o maior item do menu inteiro).
- Preenchimento coluna-a-coluna: completa a coluna atual antes de passar à
  próxima.
- Chip (`[R]`) e rótulo alinham como duas sub-colunas independentes dentro
  de cada coluna da grade — não como string única tratada como bloco.
- Células incompletas (somente possíveis na última coluna): ficam vazias,
  sem preenchimento visual especial.
- Número mínimo de linhas: `1` (configurável via `config/layout_menu.json`).
- Sem paginação, mesmo em modo `matriz` — overflow de `menu` nunca pagina.

O eixo `distribuicao_menu` é calculado pelo renderer — não declarado pela
classe. Trata-se de decisão de **layout** (como renderizar o tipo já declarado
`menu`), não de **composição** (qual tipo exibir), preservando a separação de
responsabilidades de R-1 e R-2.

## Consequências

- Menu passa a aproveitar a largura do terminal — terminais largos exibem o
  menu em grade.
- O renderer de `menu` precisa implementar o algoritmo de cálculo de colunas
  e o preenchimento coluna-a-coluna.
- `contrato_composicao_corpo.md` seção 5.1 e R-6 são atualizados junto com
  esta ADR.
- Seção 5.2 do contrato recebe a descrição dos dois modos e o algoritmo;
  as regras de alinhamento horizontal e vãos serão atualizadas pelas ADRs
  seguintes (ADR-0002: bloco à esquerda com sobra à direita; ADR-0003: vãos elásticos).

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Manter coluna única sempre | Não aproveita o espaço horizontal disponível em terminais largos |
| `distribuicao_menu` declarado pela classe | Acoplamento desnecessário — o cálculo por largura real elimina configuração manual; a classe não precisa conhecer a quantidade de itens do menu |
| Paginar quando não cabe em uma linha | Contraria regra já fechada de que `menu` nunca pagina (seção 5.1) |
