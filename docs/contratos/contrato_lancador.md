---
name: contrato-lancador
description: Schema e regras do lancador — tipo de elemento do corpo que agrupa itens de navegação para outras telas; instância declarada no tela.json
metadata:
  type: contrato
  scope: orquestrador
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
      - docs/adr/ADR-0023-largura-minima-funcional-lancador.md
      - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
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
instancia o `lancador`. Nenhum desses dados pertence a
`config/elementos/lancador.json` nem a outro artefato global.

**Parâmetros de layout do tipo** (vãos mínimos e máximos, número mínimo de
linhas, regras de wrap) vivem no futuro caminho
`config/elementos/lancador.json` como artefato ativo transicional — **a
reavaliar/migrar conforme ADR-0008 e ADR-0021**. Enquanto esse artefato existir,
o renderer deve lê-lo em tempo de execução sem hardcodar os valores.

Este contrato define semântica, regras e invariantes.
O futuro caminho `config/elementos/lancador.json` guardará parâmetros do tipo
transicionalmente. `tela.json` guarda dados concretos da instância.

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
concretos em `config/elementos/lancador.json` (transicional por ADR-0008 e
ADR-0021).

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

Parâmetros concretos de vãos mínimos e máximos estão em
`config/elementos/lancador.json` (transicional por ADR-0008 e ADR-0021).

### 6.6 Espaçamento vertical

| Posição | Regra |
|---|---|
| Entre borda superior e primeiro item | Mínimo 1 linha em branco |
| Entre último item e borda inferior | Mínimo 1 linha em branco |
| Entre elementos consecutivos | Mínimo 0, máximo 2 linhas em branco |

### 6.7 Largura mínima funcional e fallback global (ADR-0023)

Esta seção declara o limite inferior de validade das representações do
`lancador` e o comportamento quando esse limite não é atingido.

**Grandezas de largura**

Esta seção distingue quatro grandezas, que não devem ser confundidas entre si:

- **`terminal_w`**: largura total do terminal ou viewport.
- **`area_lancador_w`**: largura total efetivamente alocada ao elemento
  `lancador` pela composição — inclui a caixa completa com bordas e padding
  externos.
- **`lancador_caixa_min_w`**: largura mínima total da caixa do `lancador`,
  incluindo as unidades estruturais obrigatórias (bordas e padding externos).
  Relação conceitual:
  `lancador_caixa_min_w = coluna_minima_content_w + largura_estrutural_da_caixa`
- **`coluna_minima_content_w`** (largura mínima funcional do `lancador`):
  largura mínima do conteúdo necessária para representar integralmente uma
  coluna válida completa, sem bordas nem padding externo da caixa. É a menor
  largura de conteúdo para a qual existe ao menos uma distribuição válida do
  conjunto de itens declarados.

A comparação normativa deve usar grandezas no mesmo domínio:

```text
content_w < coluna_minima_content_w    (domínio do conteúdo)
```

ou, equivalentemente:

```text
area_lancador_w < lancador_caixa_min_w    (domínio da caixa completa)
```

Não é válido comparar `terminal_w` com `coluna_minima_content_w`, nem
comparar `area_lancador_w` com `coluna_minima_content_w` sem converter bordas
e padding.

A fórmula de `coluna_minima_content_w`:

```text
coluna_minima_content_w = vao_margem_min
                        + max_chip_sub_w + vao_chip_texto_min + max_texto_sub_w
                        + vao_margem_min
```

onde:
- `max_chip_sub_w = max(len(item["chip"]) + 2  para item em itens)`
- `max_texto_sub_w = max(len(item["texto"])     para item em itens)`
- `vao_margem_min` e `vao_chip_texto_min` vêm de `config/elementos/lancador.json`

Todos os parâmetros numéricos de vão provêm de `config/elementos/lancador.json`
sem hardcoding. Bordas e padding da caixa pertencem ao cálculo de
`lancador_caixa_min_w` e não devem ser incluídos em `coluna_minima_content_w`.

**Sequência normativa de decisão do renderer**

```text
obter area_lancador_w (largura total alocada ao lancador pela composição)
→ converter para content_w (descontar bordas e padding da caixa)
→ testar fila
→ testar matrizes válidas (n_rows = 2 .. n_itens, decrescente em colunas)
→ testar coluna mínima válida (n_col = 1, n_rows = n_itens)
→ se coluna mínima não couber: acionar o quadro mínimo canônico global
```

A verificação da coluna mínima não é um novo modo de layout; é o limite
inferior de validade das representações do `lancador`. O fallback final é o
quadro mínimo canônico global (`quadro mínimo de terminal pequeno`, ADR-0017) —
não uma disposição parcial nem um estado local.

**Fallback global — proibições**

Quando a coluna mínima não couber (`content_w < coluna_minima_content_w`):

- o quadro mínimo canônico global (`quadro mínimo de terminal pequeno`,
  ADR-0017) substitui integralmente toda a tela ou sessão TUI normal;
- nenhuma representação do `lancador` é renderizada;
- nenhum componente da tela normal permanece visível;
- é proibido renderizar mensagem dentro da caixa ou área do `lancador`;
- é proibido criar estado visual local restrito ao `lancador`;
- é proibido truncar textos ou chips para forçar encaixe;
- é proibido permitir overflow horizontal;
- é proibido omitir, duplicar ou reordenar itens;
- é proibido paginar o `lancador`;
- é proibido criar rolagem específica;
- é proibido criar mensagem nova específica para o `lancador`.

**Recuperação automática**

O estado de quadro mínimo não é permanente. A cada redesenho:

- o renderer recalcula as grandezas de largura e a sequência de decisão;
- quando `content_w >= coluna_minima_content_w` (equivalente a
  `area_lancador_w >= lancador_caixa_min_w`), o quadro mínimo desaparece;
- a tela normal é reconstruída integralmente;
- o `lancador` volta à representação normal (fila ou matriz, conforme couber),
  recalculada a partir da largura atual;
- não é necessária ação do usuário;
- não é necessário reiniciar a aplicação;
- não há persistência do estado de quadro mínimo entre redesenhos.

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
Parâmetros do tipo serão lidos do futuro caminho
`config/elementos/lancador.json` (transicional por ADR-0008 e ADR-0021).
Regras visuais da instância são lidas do `tela.json`.

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

**R-11. Grandezas de largura no mesmo domínio (ADR-0023).**
A comparação normativa de cabimento usa grandezas no mesmo domínio: `content_w`
contra `coluna_minima_content_w` (domínio do conteúdo), ou `area_lancador_w`
contra `lancador_caixa_min_w` (domínio da caixa). Nunca `terminal_w` contra
`coluna_minima_content_w`. Nunca `area_lancador_w` contra
`coluna_minima_content_w` sem converter bordas e padding. Os parâmetros de
`coluna_minima_content_w` provêm de `config/elementos/lancador.json` sem
hardcoding.

**R-12. Fallback global quando coluna mínima não couber (ADR-0023).**
Quando `content_w < coluna_minima_content_w` (equivalente:
`area_lancador_w < lancador_caixa_min_w`), o renderer aciona o quadro mínimo
canônico global (ADR-0017). Nenhuma representação parcial, mensagem local ou
variante visual restrita ao `lancador` é permitida nessa condição.

**R-13. Proibição absoluta de fallback local (ADR-0023).**
Nenhum estado visual restrito ao `lancador` pode ser criado quando a coluna
mínima não couber. A ausência de representação válida do `lancador` torna a
tela normal inutilizável; o único resultado admissível é o quadro mínimo
canônico global. Mensagem, truncamento, omissão ou variante visual local são
proibidos.

**R-14. Recuperação automática por redesenho (ADR-0023).**
O estado de quadro mínimo provocado por insuficiência de `area_lancador_w` é
reavaliado em cada redesenho. Quando `area_lancador_w >= lancador_caixa_min_w`,
a tela normal é reconstruída automaticamente, sem ação do usuário e sem
reinicialização. O `lancador` retorna à distribuição válida (`fila` ou
`matriz`, conforme a largura atual).

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
- [ ] Nenhum parâmetro de layout do tipo está hardcoded no código — parâmetros do tipo vêm do futuro caminho `config/elementos/lancador.json`; regras da instância vêm do `tela.json`.
- [ ] A largura de cada coluna é calculada pelo maior elemento daquela coluna específica.
- [ ] `chip` e `texto` formam duas sub-colunas independentes, alinhadas à esquerda.
- [ ] O espaço entre `chip` e `texto` está entre 1 e 3 caracteres.
- [ ] Há pelo menos 1 linha em branco entre a borda superior e o primeiro item.
- [ ] Há pelo menos 1 linha em branco entre o último item e a borda inferior.
- [ ] O número de linhas em branco entre elementos consecutivos está entre 0 e 2.
- [ ] O renderer não cria item não declarado no `tela.json`.
- [ ] O renderer não hardcoda item, texto, chip ou destino.
- [ ] O `lancador` não é navegável por `[✥]` nem pelas setas da `barra_de_menus`.
- [ ] O renderer calcula `coluna_minima_content_w` a partir de `config/elementos/lancador.json`; nenhum parâmetro de vão está hardcoded (R-11, ADR-0023).
- [ ] A comparação normativa de cabimento usa grandezas no mesmo domínio: `content_w` contra `coluna_minima_content_w`, ou `area_lancador_w` contra `lancador_caixa_min_w`; nunca `terminal_w` contra `coluna_minima_content_w` (R-11, ADR-0023).
- [ ] Quando `content_w < coluna_minima_content_w`, o renderer aciona o quadro mínimo canônico global; nenhuma representação do `lancador` permanece visível (R-12, ADR-0023).
- [ ] Nenhuma mensagem, estado visual ou variante local é criado dentro da caixa ou área do `lancador` quando a coluna mínima não couber (R-13, ADR-0023).
- [ ] Nenhum item é truncado, omitido, duplicado, reordenado ou paginado para forçar encaixe quando a coluna mínima não couber (R-13, ADR-0023).
- [ ] O estado de quadro mínimo é reavaliado em cada redesenho; quando `area_lancador_w >= lancador_caixa_min_w`, a tela normal é reconstruída automaticamente sem ação do usuário (R-14, ADR-0023).

---

## 10. Pendências em aberto

- **`config/elementos/lancador.json` como artefato transicional (ADR-0008,
  ADR-0021)**: os parâmetros de layout do tipo vivem nesse futuro caminho como
  artefato ativo transicional. Devem ser reavaliados e migrados para o modelo
  de configuração por tela conforme ADR-0008 em tarefa posterior.
- **Campos de navegação interna em `config/elementos/lancador.json`**: vãos e alinhamento
  já formalizados; pendente a formalização dos campos de `navegacao` (wrap
  toroidal, célula vazia) que aguardam contrato de mecanismos de
  seleção/navegação.

---

## 11. Capacidade de distribuição matricial (ADR-0025)

A ADR-0025 (2026-07-16) define a capacidade genérica de distribuição matricial
configurável de nível único, que o `lancador` pode adotar mediante declaração
explícita no seu JSON. Esta seção delimita o que a ADR-0025 acrescenta, o que
permanece como política específica do `lancador` e o que requer reconciliação
futura.

### 11.1 O que a ADR-0025 acrescenta ao `lancador`

O `lancador` poderá declarar o campo opcional `distribuicao_matricial` no seu
JSON em `corpo.elementos[]`. Quando presente:

- a organização interna dos itens segue as políticas declaradas nesse campo;
- a formação pode ser `preferencia_linhas`, `preferencia_colunas` ou
  `matriz_fixa`;
- a ordem de preenchimento, o dimensionamento, o espaçamento, a distribuição
  e o alinhamento são configuráveis.

A adoção da capacidade é **explícita**: a ausência de `distribuicao_matricial`
preserva integralmente as políticas específicas do `lancador` definidas pelas
ADR-0001, ADR-0002 e ADR-0003.

### 11.2 O que permanece como política específica do `lancador`

Enquanto `distribuicao_matricial` não for declarado, permanecem vigentes:

- algoritmo automático de cálculo de colunas (ADR-0001): modo `fila` ou
  `matriz` calculado automaticamente pela largura real do terminal;
- bloco à esquerda com sobra à direita (ADR-0002);
- vãos elásticos entre itens (ADR-0003);
- largura mínima funcional e fallback global (ADR-0023);
- sub-colunas independentes de `chip` e `texto` (seção 6.3 deste contrato);
- parâmetros transicionais de `config/elementos/lancador.json`.

### 11.3 Precedência quando `distribuicao_matricial` está presente (DEC-APP-0025-02)

Quando o `lancador` declarar explicitamente `distribuicao_matricial`, essa
configuração tem precedência sobre as políticas das ADR-0001, ADR-0002 e
ADR-0003 que tratem das mesmas responsabilidades de layout.

| Responsabilidade | Regra quando `distribuicao_matricial` está ausente | Regra quando `distribuicao_matricial` está presente |
|---|---|---|
| Formação (modo fila ou matriz) | Algoritmo automático calculado pela largura real do terminal (ADR-0001) | `formacao.politica` declarado em `distribuicao_matricial` |
| Distribuição horizontal (bloco à esquerda, sobra à direita) | Bloco à esquerda com toda a sobra à direita (ADR-0002) | `distribuicao_horizontal.politica` + `espacamento.margem_direita` declarados |
| Vãos horizontais elásticos entre itens e colunas | Vãos elásticos com mínimo e máximo (ADR-0003) | `espacamento.vao_horizontal` declarado em `distribuicao_matricial` |
| Margens borda↔bloco | Parâmetros de `config/elementos/lancador.json` (ADR-0003) | `espacamento.margem_esquerda` e `espacamento.margem_direita` declarados |

As políticas das ADR-0001, ADR-0002 e ADR-0003 listadas acima **não
concorrem, não complementam e não coexistem** com `distribuicao_matricial`
na mesma instância quando o campo está presente. A interpretação dessas
responsabilidades é determinada exclusivamente pela nova configuração.

Responsabilidades do `lancador` não relacionadas ao layout matricial **não
são afetadas** pela precedência e permanecem vigentes mesmo quando
`distribuicao_matricial` está presente:

- identidade, conteúdo textual e navegação dos itens (`id`, `chip`, `texto`,
  `tela_destino`);
- acionamento de navegação por item;
- largura mínima funcional e fallback global (ADR-0023, seção 6.7 deste
  contrato);
- sub-colunas independentes de `chip` e `texto` (seção 6.3 deste contrato);
- parâmetros de `config/elementos/lancador.json` não relacionados ao layout
  matricial (por exemplo, campos de navegação interna).

**Quando `distribuicao_matricial` está ausente**: ADR-0001, ADR-0002, ADR-0003,
ADR-0023 e as demais políticas específicas do `lancador` permanecem vigentes
integralmente. Nenhum JSON existente muda. Nenhuma migração ocorre.

### 11.4 A divergência do H-0034 não é corrigida por esta aplicação

A presente aplicação documental não corrige nem resolve silenciosamente a
divergência da política geométrica do H-0034. A correção geométrica do
`lancador` continua sendo ciclo documental próprio, independente da ADR-0025.

### 11.5 Fallback

Quando `distribuicao_matricial` for declarado e nenhuma formação válida couber
na área útil, o estado exibido é o `quadro mínimo de terminal pequeno`
(ADR-0017, ADR-0023). Este estado substitui integralmente toda a tela ou
sessão TUI normal. As regras da seção 6.7 permanecem vigentes.
