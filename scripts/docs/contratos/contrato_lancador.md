---
name: contrato-lancador
description: Schema e regras do lancador — tipo de elemento do corpo que agrupa itens de navegação para outras telas; instância declarada no tela.json
metadata:
  type: contrato
  scope: scripts
  versao: "0.2"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#13-decisao-terminologica-lancador"
    adrs_aplicadas:
      - docs/adr/ADR-0001-menu-suporta-matriz.md
      - docs/adr/ADR-0002-menu-sobra-direita.md
      - docs/adr/ADR-0003-vaos-elasticos-menu.md
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    reaproveitado_de_legado: false
---

# Contrato — lancador

## 1. Objetivo

Especificar o `lancador` como tipo de elemento do corpo: sua natureza de
instância declarada no `tela.json`, a estrutura de título e itens, o papel de
cada campo de item, as regras de layout, e os invariantes que vinculam todos os
renderers a este contrato.

Este contrato define o schema, os invariantes e o comportamento mínimo do
**tipo** `lancador`. Conteúdo concreto, itens, textos, chips, destinos e regras
visuais de cada **instância** vêm do `tela.json` da tela onde o `lancador` é
declarado.

Este contrato cobre a seção 13 de `docs/NOMENCLATURA.md` e aplica ADR-0008.
Estilo universal (`contrato_estilo.md`, `ativo`), composição de corpo
(`contrato_composicao_corpo.md`, `ativo`) e `barra_de_menus`
(`contrato_barra_de_menus.md`, `ativo`) são módulos separados e externos —
este contrato pode referenciá-los como dependências, mas não redefine nem
duplica suas regras. A fonte de autoridade sobre o schema de `tela.json` é
`contrato_tela_json.md`.

---

## 2. Natureza do `lancador`

O `lancador` é um **tipo de elemento do corpo**. Uma ocorrência concreta de
`lancador` é uma **instância** declarada no `tela.json` da tela.

| Conceito | O que é |
|---|---|
| Tipo `lancador` | Conjunto de regras, invariantes e comportamento mínimo — definido por este contrato |
| Instância de `lancador` | Elemento do corpo declarado no `tela.json` de uma tela; contém título, lista de itens e regras de exibição concretas |

O renderer executa a instância conforme declarada e validada no `tela.json`. Ele
não decide composição, itens, textos, chips, destinos nem regras visuais da
instância.

---

## 3. Distinção fundamental — `lancador` não é região da tela

O `lancador` é um **elemento do corpo** — não uma região da tela. Nenhum código,
documentação ou nomenclatura pode tratar o `lancador` como equivalente à
`barra_de_menus` ou a qualquer outra região fixa da tela.

| Conceito | O que é | Natureza |
|---|---|---|
| `lancador` | Tipo de elemento do corpo; instância com título e itens de navegação | Elemento do corpo — regido por este contrato |
| `barra_de_menus` | Região fixa inferior da tela com chips de ação e navegação | Região da tela — regida por `contrato_barra_de_menus.md` |
| `console` | Tipo de elemento do corpo com dados e navegação por `[✥]` | Elemento do corpo — regido por `contrato_composicao_corpo.md` |

**Nome anterior:** o `lancador` era chamado de `menu` (corpo) nos artefatos
anteriores a 2026-07-06. O termo `menu` está descontinuado para este tipo;
os artefatos existentes ainda o usam por rastreabilidade (migração: DOC-0009).

**Consequência direta:** o renderer do `lancador` não consulta, herda nem
aplica nenhuma regra da `barra_de_menus`. Os chips de ação da
`barra_de_menus` continuam sendo geridos exclusivamente por
`contrato_barra_de_menus.md`.

---

## 4. Estrutura da instância no `tela.json`

Uma instância de `lancador` declarada no `tela.json` deve conter, no mínimo:

```text
id
tipo = lancador
titulo
itens[]
layout/regras_exibicao
```

### 4.1 `id`

Toda instância de `lancador` deve ter `id` estável e único no escopo do
`tela.json`. Instância sem `id` é inválida.

### 4.2 Título

O título é declarado pela instância no `tela.json`. É uma string exibida
integrada à linha de borda superior do `lancador`, no formato:

```
borda + espaço + título + espaço + borda
```

O estilo dos caracteres de borda segue o schema de estilo ativo
(`contrato_estilo.md`). O texto concreto do título pertence à instância
declarada no `tela.json` — este contrato não define conteúdo textual.

### 4.3 Itens

A lista de itens é declarada pela instância no `tela.json`. Cada item deve
ter, no mínimo:

| Campo | Tipo | Função |
|---|---|---|
| `id` | identificador | Id estável do item no escopo da instância |
| `chip` ou tecla | visual | Identificador de ação — ex.: `[A]` |
| `texto` | string | Rótulo descritivo da tela chamada |
| `tela_destino` | identificador | Referência formal à tela a ser aberta |

Item sem `id`, sem `chip`/tecla, sem `texto` ou sem `tela_destino` é inválido.

**Papel do item:** acionar navegação para a tela identificada por
`tela_destino`. O item não executa processo, não filtra dado, não altera
estado.

### 4.4 `chip`

O `chip` segue o schema de estilo ativo (`contrato_estilo.md`) e tem
exatamente três posições visuais:

| Posição | Função |
|---|---|
| Borda esquerda | Caractere de abertura do chip (ex.: `[`) |
| Tecla | Identificador da ação — declarado no item no `tela.json` |
| Borda direita | Caractere de fechamento do chip (ex.: `]`) |

Os caracteres de abertura e fechamento vêm do estilo ativo. A tecla exibida
dentro do chip é declarada no item no `tela.json`. O renderer não hardcoda
nenhum desses valores.

### 4.5 `texto`

- **Máximo de 15 caracteres.**
- `texto` acima de 15 caracteres é **rejeitado em verificação** — nunca
  truncado, nunca abreviado automaticamente.
- O texto concreto pertence à instância declarada no `tela.json`. Cabe ao
  declarante garantir o limite antes de declarar o item.

### 4.6 `tela_destino`

Identificador formal da tela a ser aberta quando o item é acionado. Não é
texto de exibição — é um identificador interno usado pelo sistema de
navegação. A tela referenciada deve existir; `tela_destino` inexistente é
erro de validação.

### 4.7 `layout` / `regras_exibicao`

Regras de alinhamento, vãos, distribuição e demais parâmetros visuais da
instância são declaradas no `tela.json`. O renderer aplica a regra declarada
e não decide alinhamento por conta própria. Regra de alinhamento desconhecida
é erro de validação.

---

## 5. Fonte dos valores concretos

**Itens concretos** (`id`, `chip`, `texto`, `tela_destino`) e **regras visuais
da instância** (alinhamento, layout) pertencem ao `tela.json` da tela que
instancia o `lancador`. Nenhum desses dados pertence a `config/lancador.json`
nem a outro artefato global.

**Parâmetros de layout do tipo** (vãos mínimos e máximos, número mínimo de
linhas, regras de wrap) vivem em `config/lancador.json` como artefato ativo
transicional — **a reavaliar/migrar conforme ADR-0008**. Enquanto esse
artefato existir, o renderer deve lê-lo em tempo de execução sem hardcodar
os valores.

Este contrato define semântica, regras e invariantes. `config/lancador.json`
guarda parâmetros do tipo transicionalmente. `tela.json` guarda dados concretos
da instância.

Adicionar item ao `lancador`, mudar texto, mudar chip/letra ou mudar
`tela_destino` é **alteração declarativa no JSON da tela**. O código apenas
percorre `itens[]`.

---

## 6. Schema de layout

### 6.1 Disposição em fila ou matriz

O renderer calcula automaticamente a distribuição do `lancador` em dois modos:

- **`fila`**: todos os itens em linha única horizontal.
- **`matriz`**: grade de múltiplas colunas, preenchida coluna-a-coluna.

O modo é calculado automaticamente a partir da largura real do terminal — não
é declarado pela instância nem ajustável manualmente. A instância não declara
`distribuicao_lancador` como eixo explícito; o cálculo pertence ao renderer.

O `lancador` **nunca pagina**, independente do número de itens ou do modo.

### 6.2 Largura de coluna

A largura de cada coluna é definida pelo maior elemento daquela coluna
específica — não pelo maior elemento de todo o `lancador`.

### 6.3 Organização interna do item

Dentro de cada coluna, `chip` e `texto` formam **duas sub-colunas
independentes**, alinhadas à esquerda:

- A sub-coluna do `chip` alinha à esquerda pela largura do maior `chip`
  daquela coluna.
- A sub-coluna do `texto` alinha à esquerda pela largura do maior `texto`
  daquela coluna.

**Espaço `chip`↔`texto`:** mínimo 1 caractere, máximo 3 caracteres. Parâmetros
concretos em `config/lancador.json` (transicional por ADR-0008).

### 6.4 Alinhamento horizontal

O alinhamento horizontal do bloco de itens é uma **regra declarada pela
instância no `tela.json`**. A instância pode declarar alinhamento à esquerda,
ao centro ou à direita, conforme o schema de tela.

O renderer não decide o alinhamento sozinho. Ele aplica a regra da instância
validada.

**Rastreabilidade histórica (ADR-0002):** a ADR-0002 estabeleceu, para o
antigo `menu`, o bloco à esquerda com toda a sobra à direita, substituindo a
centralização anterior. Essa regra permanece como referência histórica e pode
ser usada como comportamento default quando declarado ou herdado pela instância.
Ela não contraria o modelo por instância da ADR-0008 — é um valor possível de
alinhamento, não uma regra universal obrigatória.

### 6.5 Distribuição de espaço dentro da regra declarada

Depois de determinado o alinhamento pela instância, o renderer distribui o
espaço disponível segundo a regra declarada:

- Estica os vãos entre itens/colunas até o máximo;
- O espaço restante vai para a margem borda↔elemento;
- O cálculo automático do renderer é apenas distribuição visual dentro da
  regra declarada — não é decisão de composição.

Parâmetros concretos de vãos mínimos e máximos estão em `config/lancador.json`
(transicional por ADR-0008).

### 6.6 Espaçamento vertical

| Posição | Regra |
|---|---|
| Entre borda superior e primeiro item | Mínimo 1 linha em branco |
| Entre último item e borda inferior | Mínimo 1 linha em branco |
| Entre elementos consecutivos | Mínimo 0, máximo 2 linhas em branco |

---

## 7. Relação com `barra_de_menus`

- Os chips dos itens do `lancador` não são chips da `barra_de_menus`.
- A `barra_de_menus` não controla os itens do `lancador`.
- O chip `[✥]` não navega itens do `lancador`.
- O `lancador` não é corpo navegável por `[✥]` nem pelas setas da
  `barra_de_menus` (ADR-0005).
- O acionamento de um item do `lancador` é direto pelo chip/tecla do próprio
  item, conforme declaração da instância no `tela.json`.

---

## 8. Regras de uso

**R-1. `lancador` é elemento do corpo, não região da tela.**
Nenhum renderer pode instanciar ou posicionar o `lancador` como se fosse uma
região fixa (como `cabecalho` ou `barra_de_menus`). O `lancador` só existe
como elemento do corpo.

**R-2. Item só navega.**
O acionamento de um item do `lancador` resulta exclusivamente em navegação
para a tela identificada por `tela_destino`. Nenhum item pode executar
processo, filtrar dado ou alterar estado do sistema.

**R-3. `texto` máximo 15 caracteres — rejeitado, nunca truncado.**
`texto` acima de 15 caracteres deve ser rejeitado em verificação estática,
antes da renderização. O renderer nunca trunca nem abrevia o `texto`
silenciosamente.

**R-4. `chip` combina estilo ativo e item declarado no `tela.json`.**
Os caracteres de abertura e fechamento do `chip` vêm do schema de estilo ativo
(`contrato_estilo.md`). A tecla exibida dentro do `chip` vem do item declarado
no `tela.json`. O renderer não hardcoda nenhum desses valores.

**R-5. Título na borda.**
O título do `lancador` aparece integrado à linha de borda superior no
formato `borda + espaço + título + espaço + borda`. Nenhum outro formato
é válido.

**R-6. Proibição de hardcoding.**
Nenhum parâmetro de layout do tipo `lancador` pode estar hardcoded no código.
Parâmetros do tipo são lidos de `config/lancador.json` (transicional por
ADR-0008). Regras visuais da instância são lidas do `tela.json`.

**R-7. Largura de coluna pelo maior elemento da própria coluna.**
A largura de cada coluna é calculada a partir do maior elemento daquela
coluna — nunca pelo maior elemento de todo o `lancador`.

**R-8. Sub-colunas independentes, alinhadas à esquerda.**
`chip` e `texto` formam duas sub-colunas independentes. Ambas alinham à
esquerda dentro da coluna.

**R-9. Itens e destinos concretos vêm do `tela.json`.**
O renderer percorre `itens[]` declarado na instância do `tela.json`. Não pode
criar item não declarado, não pode hardcodar item, texto, chip ou destino.

**R-10. Alinhamento é regra da instância.**
O renderer não decide o alinhamento horizontal do bloco de itens. Aplica a
regra declarada pela instância no `tela.json`. Regra de alinhamento desconhecida
é erro de validação.

---

## 9. Critérios de validação

- [ ] A instância de `lancador` tem `id` — instância sem `id` é inválida.
- [ ] O `lancador` existe somente como elemento do corpo — nunca como região fixa da tela.
- [ ] Cada item tem `id` — item sem `id` é inválido.
- [ ] Cada item tem `chip` ou tecla — item sem `chip`/tecla é inválido.
- [ ] Cada item tem `texto` — item sem `texto` é inválido.
- [ ] Cada item tem `tela_destino` — item sem `tela_destino` é inválido.
- [ ] `texto` de qualquer item tem no máximo 15 caracteres; itens com `texto` acima desse limite são rejeitados em verificação (nunca truncados).
- [ ] `tela_destino` de cada item referencia tela existente — `tela_destino` inexistente é erro de validação.
- [ ] A regra de alinhamento declarada pela instância é reconhecida — alinhamento desconhecido é erro de validação.
- [ ] O acionamento de qualquer item resulta exclusivamente em navegação para a tela de `tela_destino` — sem execução de processo, filtro de dado ou alteração de estado.
- [ ] O `chip` de cada item usa abertura e fechamento vindos do estilo ativo, e tecla vinda do item declarado no `tela.json`, sem hardcoding pelo renderer.
- [ ] O título do `lancador` aparece na linha de borda superior no formato `borda + espaço + título + espaço + borda`.
- [ ] Nenhum parâmetro de layout do tipo está hardcoded no código — parâmetros do tipo vêm de `config/lancador.json`; regras da instância vêm do `tela.json`.
- [ ] A largura de cada coluna é calculada pelo maior elemento daquela coluna específica.
- [ ] `chip` e `texto` formam duas sub-colunas independentes, alinhadas à esquerda.
- [ ] O espaço entre `chip` e `texto` está entre 1 e 3 caracteres.
- [ ] Há pelo menos 1 linha em branco entre a borda superior e o primeiro item.
- [ ] Há pelo menos 1 linha em branco entre o último item e a borda inferior.
- [ ] O número de linhas em branco entre elementos consecutivos está entre 0 e 2.
- [ ] O renderer não cria item não declarado no `tela.json`.
- [ ] O renderer não hardcoda item, texto, chip ou destino.
- [ ] O `lancador` não é navegável por `[✥]` nem pelas setas da `barra_de_menus`.

---

## 10. Pendências em aberto

- **`config/lancador.json` como artefato transicional (ADR-0008)**: os
  parâmetros de layout do tipo vivem em `config/lancador.json` como artefato
  ativo transicional. Devem ser reavaliados e migrados para o modelo de
  configuração por tela conforme ADR-0008 em tarefa posterior.
- **Campos de navegação interna em `config/lancador.json`**: vãos e alinhamento
  já formalizados; pendente a formalização dos campos de `navegacao` (wrap
  toroidal, célula vazia) que aguardam contrato de mecanismos de
  seleção/navegação.
