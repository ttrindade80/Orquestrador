---
name: contrato-lancador
description: Schema e regras do lancador — membro do corpo que agrupa itens de navegação para outras telas, distinto da barra_de_menus
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#13-decisao-terminologica-lancador"
    reaproveitado_de_legado: false
---

# Contrato — lancador

## 1. Objetivo

Especificar o `lancador`: sua natureza de membro do corpo, a estrutura de
título e itens, o papel de cada campo de item, as regras de layout, e os
invariantes que vinculam todos os renderers a este contrato.

Este contrato cobre a seção 13 de `docs/NOMENCLATURA.md`. Estilo universal
(`contrato_estilo.md`, `ativo`), composição de corpo
(`contrato_composicao_corpo.md`, `ativo`) e `barra_de_menus`
(`contrato_barra_de_menus.md`, `ativo`) são módulos separados e externos —
este contrato pode referenciá-los como dependências, mas não redefine nem
duplica suas regras.

---

## 2. Distinção fundamental — `lancador` como membro do corpo

O `lancador` é um membro do corpo — não uma região da tela. Nenhum código,
documentação ou nomenclatura pode tratar o `lancador` como equivalente à
`barra_de_menus` ou a qualquer outra região fixa da tela.

| Conceito | O que é | Natureza |
|---|---|---|
| `lancador` | Objeto do corpo; caixa com título e itens de navegação | Membro do corpo — regido por este contrato |
| `barra_de_menus` | Região fixa inferior da tela com chips de ação e navegação | Região da tela — regida por `contrato_barra_de_menus.md` |
| `dado` | Objeto do corpo com dados tabulares ou de lista | Membro do corpo — regido por `contrato_composicao_corpo.md` |

**Nome anterior:** o `lancador` era chamado de `menu` (corpo) nos artefatos
anteriores a 2026-07-06. O termo `menu` está descontinuado para este tipo;
os artefatos existentes ainda o usam por rastreabilidade (migração: DOC-0009).

**Consequência direta:** o renderer do `lancador` não consulta, herda nem
aplica nenhuma regra da `barra_de_menus`. Os chips de ação da
`barra_de_menus` continuam sendo geridos exclusivamente por
`contrato_barra_de_menus.md`.

---

## 3. Estrutura

### 3.1 Título

O `lancador` tem exatamente um título, declarado pela classe de tela que o
instancia. O título é uma string e é exibido integrado à linha de borda
superior do `lancador`, no formato:

```
borda + espaço + título + espaço + borda
```

O estilo dos caracteres de borda (traços, cantos) segue o schema de estilo
ativo (`contrato_estilo.md`). A classe/tela fornece o texto concreto do
título — este contrato não define o conteúdo textual, apenas o formato de
exibição.

### 3.2 Itens

O `lancador` contém uma lista de itens. Cada item tem exatamente três
campos:

| Campo | Tipo | Função |
|---|---|---|
| `chip` | visual | Identificador de ação — ex.: `[A]` |
| `texto` | string | Rótulo descritivo da tela chamada |
| `tela_destino` | identificador | Referência formal à tela a ser aberta |

**Papel do item:** acionar navegação para a tela identificada por
`tela_destino`. O item não executa processo, não filtra dado, não altera
estado.

### 3.3 `chip`

O `chip` segue o schema de estilo ativo (`contrato_estilo.md`) e tem
exatamente três posições visuais:

| Posição | Função |
|---|---|
| Borda esquerda | Caractere de abertura do chip (ex.: `[`) |
| Tecla | Identificador da ação (ex.: `A`) |
| Borda direita | Caractere de fechamento do chip (ex.: `]`) |

Os caracteres de abertura e fechamento do chip vêm do estilo ativo. A tecla
exibida dentro do chip é declarada no próprio item do `lancador`.

### 3.4 `texto`

- **Máximo de 15 caracteres.**
- `texto` acima de 15 caracteres é **rejeitado em verificação** — nunca
  truncado, nunca abreviado automaticamente.
- Cabe à classe de tela garantir o limite antes de declarar o `lancador`.

### 3.5 `tela_destino`

Identificador formal da tela a ser aberta quando o item é acionado. O
`tela_destino` não é texto de exibição — é um identificador interno usado
pelo sistema de navegação.

---

## 4. Fonte dos valores concretos

Os parâmetros concretos de layout e verificação do `lancador` vivem em
**`config/lancador.json`** (política da seção 0 de `docs/NOMENCLATURA.md`).

Este contrato define a **semântica**, as **regras** e os **invariantes**.
O JSON guarda os **valores concretos**. Os dois artefatos têm
responsabilidades separadas e não sobrepostas.

O renderer deve ler `config/lancador.json` em tempo de execução. Nenhum
parâmetro de layout do `lancador` pode estar hardcoded no código.

`config/lancador.json` não contém textos concretos de telas nem lista de
itens reais — esses pertencem à classe/tela que instancia o `lancador`.

---

## 5. Schema de layout

### 5.1 Disposição em colunas

- Os itens do `lancador` são exibidos em colunas, preenchidas de cima para
  baixo.
- Quando há estouro vertical (itens não cabem na altura disponível), cria-se
  uma nova coluna à direita.
- A largura de cada coluna é definida pelo maior elemento daquela coluna
  específica — não pelo maior elemento de todo o `lancador`.

### 5.2 Organização interna do item

Dentro de cada coluna, `chip` e `texto` formam **duas sub-colunas
independentes**, alinhadas à esquerda:

- A sub-coluna do `chip` alinha à esquerda pela largura do maior `chip`
  daquela coluna.
- A sub-coluna do `texto` alinha à esquerda pela largura do maior `texto`
  daquela coluna.
- Não há alinhamento à direita dentro do item.

**Espaço chip↔texto:** mínimo 1 caractere, máximo 3 caracteres. Valores
concretos em `config/lancador.json`.

### 5.3 Distribuição horizontal

- **Uma coluna:** o bloco de itens é centralizado horizontalmente dentro do
  espaço disponível.
- **Múltiplas colunas:** o espaço horizontal é distribuído uniformemente
  entre bordas e colunas. Duas colunas geram três áreas iguais:
  `borda↔coluna1`, `coluna1↔coluna2`, `coluna2↔borda`.

### 5.4 Espaçamento vertical

| Posição | Regra |
|---|---|
| Entre borda superior e primeiro item | Mínimo 1 linha em branco |
| Entre último item e borda inferior | Mínimo 1 linha em branco |
| Entre elementos consecutivos | Mínimo 0, máximo 2 linhas em branco |

---

## 6. Regras de uso

**R-1. `lancador` é membro do corpo, não região da tela.**
Nenhum renderer pode instanciar ou posicionar o `lancador` como se fosse uma
região fixa (como `cabecalho` ou `barra_de_menus`). O `lancador` só existe
como objeto do corpo.

**R-2. Item só navega.**
O acionamento de um item do `lancador` resulta exclusivamente em navegação
para a tela identificada por `tela_destino`. Nenhum item pode executar
processo, filtrar dado ou alterar estado do sistema.

**R-3. `texto` máximo 15 caracteres — rejeitado, nunca truncado.**
`texto` acima de 15 caracteres deve ser rejeitado em verificação estática,
antes da renderização. O renderer nunca trunca nem abrevia o `texto`
silenciosamente.

**R-4. `chip` combina estilo ativo e item do `lancador`.**
Os caracteres de abertura e fechamento do `chip` vêm do schema de estilo ativo
(`contrato_estilo.md`). A tecla exibida dentro do `chip` vem do item declarado
no `lancador`. O renderer não hardcoda nenhum desses valores.

**R-5. Título na borda.**
O título do `lancador` aparece integrado à linha de borda superior no
formato `borda + espaço + título + espaço + borda`. Nenhum outro formato
é válido.

**R-6. Proibição de hardcoding de layout.**
Nenhum parâmetro de layout (vãos, margens, alinhamento) do `lancador` pode
estar hardcoded no código. Todos vêm de `config/lancador.json`, lido em
tempo de execução.

**R-7. Largura de coluna pelo maior elemento da própria coluna.**
A largura de cada coluna é calculada a partir do maior elemento daquela
coluna — nunca pelo maior elemento de todo o `lancador`.

**R-8. Sub-colunas independentes, alinhadas à esquerda.**
`chip` e `texto` formam duas sub-colunas independentes. Ambas alinham à
esquerda dentro da coluna. Nenhum alinhamento à direita dentro do item é
permitido.

---

## 7. Critérios de validação

- [ ] O `lancador` existe somente como membro do corpo — nunca como região fixa da tela.
- [ ] Cada item do `lancador` tem exatamente os campos `chip`, `texto` e `tela_destino`.
- [ ] `texto` de qualquer item tem no máximo 15 caracteres; itens com `texto` acima desse limite são rejeitados em verificação (nunca truncados).
- [ ] O acionamento de qualquer item resulta exclusivamente em navegação para a tela de `tela_destino` — sem execução de processo, filtro de dado ou alteração de estado.
- [ ] O `chip` de cada item usa abertura e fechamento vindos do estilo ativo, e tecla vinda do item do `lancador`, sem hardcoding pelo renderer.
- [ ] O título do `lancador` aparece na linha de borda superior no formato `borda + espaço + título + espaço + borda`.
- [ ] Nenhum parâmetro de layout do `lancador` está hardcoded no código — todos vêm de `config/lancador.json`.
- [ ] A largura de cada coluna é calculada pelo maior elemento daquela coluna específica.
- [ ] `chip` e `texto` formam duas sub-colunas independentes, alinhadas à esquerda.
- [ ] O espaço entre `chip` e `texto` está entre 1 e 3 caracteres.
- [ ] Com uma coluna, o bloco de itens é centralizado horizontalmente.
- [ ] Com múltiplas colunas, o espaço horizontal é distribuído uniformemente entre bordas e colunas.
- [ ] Há pelo menos 1 linha em branco entre a borda superior e o primeiro item.
- [ ] Há pelo menos 1 linha em branco entre o último item e a borda inferior.
- [ ] O número de linhas em branco entre elementos consecutivos está entre 0 e 2.

---

## 8. Pendências em aberto

Nenhuma pendência em aberto para este contrato no momento da emissão.

A migração dos artefatos existentes que ainda referenciam o tipo como `menu`
(`NOMENCLATURA.md` seções 2–10, `contrato_composicao_corpo.md`,
`config/layout_menu.json`) é escopo do DOC-0009, não deste contrato.
