---
name: contrato-composicao-corpo
description: Schema e regras do módulo de composição de corpo — tipos de elemento declarados em tela.json, regras de console, lancador e dashboard, indicador de paginação e tiling
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.3"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#3-composicao-de-corpo, #6-layout-e-largura, #8-corpo-tipo-lancador, #9-objeto-dashboard, #10-tiling"
    adrs_aplicadas:
      - docs/adr/ADR-0001-menu-suporta-matriz.md
      - docs/adr/ADR-0002-menu-sobra-direita.md
      - docs/adr/ADR-0003-vaos-elasticos-menu.md
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0006-renomeacao-console-dashboard.md
      - docs/adr/ADR-0007-tela-processamento-composicao.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
      - docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
      - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
      - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
      - docs/adr/ADR-0017-redimensionamento-reativo-tui.md
      - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
      - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
      - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
    reaproveitado_de_legado: false
---

# Contrato — Módulo de Composição de Corpo

## 1. Objetivo

Especificar a composição do corpo da tela: a taxonomia fechada dos tipos de
elemento do corpo (funcionais e estruturais), os campos declarados no
`tela.json`, as regras de layout para `lancador`, `dashboard` e `console`, a
mecânica do indicador de paginação, as camadas de decisão de tiling, e as
regras de composição hierárquica do corpo como árvore — incluindo o nó
estrutural `grupo`, arranjo e distribuição por container, arredondamento
determinístico, preenchimento de área alocada, regras dinâmicas de dimensão
e sincronização de cortes (ADR-0015, 2026-07-10).

Este contrato cobre as seções 2, 3, 6, 6.1, 8, 9 e 10 de
`docs/NOMENCLATURA.md`. Estilo universal (`contrato_estilo.md`),
barra_de_menus (`contrato_barra_de_menus.md`) e mecanismos de seleção
(contrato ainda não escrito) são módulos separados. Este contrato pode referenciar
esses módulos como dependências externas, mas não redefine nem duplica suas regras.

A fonte de autoridade sobre o schema de `tela.json` é `contrato_tela_json.md`.
Este contrato define as regras de composição de corpo e as invariantes de cada
tipo de elemento; não redefine o schema completo da tela.

---

## 2. Regra fundamental

**Toda propriedade concreta de composição do corpo é declarada no `tela.json`
da tela. O renderer recebe a declaração validada e a executa sem deliberar
tipo, arranjo, presença de elemento, posicionamento ou fallback de composição.**

O renderer não possui lógica de seleção de tipo, não possui fallback de tipo,
e não toma nenhuma decisão de composição com base em condições de ambiente
(largura de terminal, conteúdo dos dados, etc.).

Complementos obrigatórios da regra:

- a classe/código não decide composição hardcoded;
- a `barra_de_menus` não decide composição do corpo;
- `estilo.json` não decide composição;
- o estado de runtime não pertence ao JSON da tela.

Esta regra deriva da ADR-0008 e da seção 3 de `docs/NOMENCLATURA.md`.

---

## 3. Taxonomia de tipos de elemento do corpo

**ADR-0015 (2026-07-10)**: o corpo é modelado como **árvore de composição**
com dois tipos de nó: funcionais e estrutural.

### 3.0 Nós funcionais (taxonomia fechada)

O corpo de uma tela pode conter elementos funcionais de exatamente três tipos.
A lista é **fechada** — não existe tipo funcional fora desta taxonomia no
sistema atual. Extensões futuras exigem ADR.

| Tipo | Função | Presença |
|---|---|---|
| `console` | Container interativo e navegável genérico; pode conter itens heterogêneos; inclui saída de script/log | Um ou mais por tela |
| `lancador` | Elemento de navegação — lista de itens com chip, texto e `tela_destino` | Um ou mais por tela |
| `dashboard` | Saída passiva formatada, resumo/legenda ou visão consolidada; elemento passivo não navegável | Sempre opcional; sem limite global de cardinalidade por tela — uma tela pode conter múltiplos dashboards (ADR-0019, D7) |

**Distinção obrigatória**: `lancador` (elemento do corpo) e
`barra_de_menus` (região fixa da tela, contrato separado) são entidades
distintas. Nenhum código, documentação ou nomenclatura pode usar os dois
termos como sinônimos ou de forma intercambiável. O nome antigo do
`lancador` era `menu`; esse termo permanece apenas em contexto histórico
e em ADRs já emitidas.

### 3.1 Tela de processamento como composição

Tela de processamento não é tipo de elemento. Não existe quarto tipo além de
`console`, `lancador` e `dashboard`.

A composição de uma tela de processamento deve usar os tipos existentes:

- `console` cobre partes interativas ou navegáveis por `[✥]`;
- `dashboard` cobre saída passiva formatada;
- `lancador` não representa processamento.

Chips específicos ficam fora do corpo, na `barra_de_menus`, declarados pela
classe de tela. O renderer de composição de corpo não decide chips específicos.

A regra de `[✥]` continua restrita a `console`.

### 3.2 Tela inicial real `orquestrador` (ADR-0022)

A futura tela inicial real do produto, `config/telas/orquestrador.json`, deverá
declarar no corpo os elementos funcionais:

```text
console
dashboard
```

Ambos deverão estar estruturalmente presentes e começar sem entradas de dados
reais ou demonstrativos. Essa regra é específica da tela inicial real
`orquestrador`: não torna `dashboard` obrigatório em todas as telas, não cria
tipo de corpo novo, não autoriza conteúdo fictício e não reintroduz
`posicao_dashboard` como eixo ativo de alinhamento.

### 3.3 Nó estrutural `grupo` (ADR-0015)

`grupo` é o único nó estrutural do corpo. Não é tipo funcional.

`grupo`:
- não tem borda própria;
- não tem moldura visual;
- não tem título visual próprio;
- não tem conteúdo próprio;
- não é navegável por `[✥]`;
- não possui ação, item, chip, origem de dados ou `tela_destino`;
- recebe uma área do container pai;
- redistribui essa área entre seus filhos diretos;
- declara seu próprio `arranjo`;
- declara sua própria `distribuicao`;
- pode conter filhos funcionais (`console`, `lancador`, `dashboard`) e grupos
  aninhados até o nível de grupo 3 (ADR-0019);
- pode conter **múltiplos elementos funcionais** e **múltiplos grupos irmãos**
  em qualquer nível permitido (ADR-0019, D5, D6).

**Nível de grupo** é contado exclusivamente pelo aninhamento de nós estruturais
`grupo` (ADR-0019, D1):
- o corpo raiz **não** é contado como nível de grupo;
- um `grupo` filho direto de `corpo.elementos[]` está no **nível de grupo 1**;
- um `grupo` filho direto de um grupo do nível 1 está no **nível de grupo 2**;
- um `grupo` filho direto de um grupo do nível 2 está no **nível de grupo 3**;
- profundidade máxima: **3 níveis de grupos** (ADR-0019, D2);
- elementos funcionais em qualquer grupo **não acrescentam** nível de grupo,
  inclusive no nível 3 (ADR-0019, D3);
- um `grupo` filho de grupo do nível 3 estaria no nível 4 e é **estruturalmente
  inválido** (ADR-0019, D4);
- nível 4 ou superior gera erro estrutural determinístico.

### 3.4 Comportamentos estruturais do `grupo` — `livre` e `matriz` (ADR-0020)

O nó `grupo` admite dois comportamentos estruturais, selecionados pelo campo
`estrutura` (ADR-0020, D1–D3).

#### Seletor `estrutura`

```json
"estrutura": "livre"
```

ou:

```json
"estrutura": "matriz"
```

**Ausência equivale a `livre` (D3)**: quando `estrutura` não é declarado, o
comportamento é `livre`. A ausência **nunca** ativa `matriz`. Esta regra
preserva integralmente todos os JSONs existentes sem exigir nenhum campo novo.

**Não usar como seletor**: `tipo` (já identifica o nó como `grupo`), `arranjo`
(já define o eixo de composição em `livre`) nem `modo` isoladamente (já
participa do schema de `distribuicao.modo`) — (D2).

#### `estrutura: livre`

Preserva o comportamento hierárquico unidimensional atual do nó `grupo`:

- `arranjo` continua válido;
- `distribuicao` continua local ao container e é opcional;
- modos `igual`, `percentual`, `fracao` permanecem;
- ausência de `distribuicao` segue a semântica da ADR-0018 (construção
  orientada pelo conteúdo, não equivalente a `igual`);
- não há grade bidimensional compartilhada;
- não há garantia nova de alinhamento entre cortes independentes de grupos
  distintos (ver seção 5.12).

#### `estrutura: matriz`

Define o comportamento bidimensional com grade comum:

- quantidade de linhas e colunas declaradas;
- distribuição obrigatória e independente de cada eixo;
- grade comum de coordenadas compartilhada por todas as células;
- associação de filhos a células por coordenadas explícitas.

`arranjo` é **proibido** em `estrutura: matriz` (D13).

Ver seções 5.13–5.21 para as regras completas de validação, composição,
exemplos e invariantes da matriz.

---

## 4. Campos de composição declarados no `tela.json`

Os campos de composição do corpo pertencem ao `corpo` declarado no `tela.json`
da tela. O renderer lê esses valores do JSON validado e os executa sem alteração.

O `corpo` contém obrigatoriamente:

```text
tiling (ou arranjo equivalente)
elementos[]
```

Cada elemento em `elementos[]` deve declarar, no mínimo:

```text
id
tipo   (console | lancador | dashboard)
```

### 4.1 Tipo dos elementos

| Campo | Valores | Observação |
|---|---|---|
| `tipo` | `console` \| `lancador` \| `dashboard` | Tipo do elemento de corpo |

A presença de elemento `tipo=dashboard` em `corpo.elementos[]` equivale ao antigo
eixo `dashboard = presente`. A ausência de elemento `tipo=dashboard` equivale a
`dashboard = ausente`. `dashboard` não é eixo universal separado — é elemento
opcional declarado no corpo.

### 4.2 Tiling e arranjo

**Terminologia final (ADR-0011, 2026-07-08)**: os valores normativos finais
de `corpo.arranjo` são `vertical` e `horizontal`. Os termos `sobreposto` e
`lado_a_lado` são **aliases transicionais** — `sobreposto → vertical` e
`lado_a_lado → horizontal` — aceitos temporariamente para compatibilidade de
JSONs/contratos legados até migração específica; não são terminologia final.

| Campo | Valores | Observação |
|---|---|---|
| `arranjo` | `vertical` \| `horizontal` \| *(não declarado)* | Valores finais (ADR-0011). Relevante com 2+ elementos `console`/`lancador`. Quando não declarado no `tela.json`, o renderer usa o campo `tiling` do estilo ativo como default — ver seção 5.6. `sobreposto`/`lado_a_lado` aceitos como aliases transicionais |

`estilo.json` não decide composição. `tela.json` é a fonte de arranjo concreto.
Se houver default histórico de artefato transicional, ele deve ser marcado como
transicional/a reavaliar pela ADR-0008.

### 4.3 Posicionamento do `dashboard`

**ADR-0010**: o posicionamento do `dashboard` no corpo é controlado pela
estrutura declarativa geral do `corpo` do `tela.json`. `dashboard` é
elemento funcional do corpo como `console` e `lancador` — não possui eixo
de posicionamento separado que contradiga o mecanismo geral de composição.

O campo `posicao_dashboard` declarado na instância, que era tratado como
"eixo próprio — nunca afetado por `arranjo` nem por `tiling`", está
**descontinuado** como mecanismo separado. JSONs existentes com
`posicao_dashboard` podem ser honrados por compatibilidade durante handoff
futuro de migração;
a migração/descarte do campo ocorrerá em handoff específico.

| Campo | Valores | Status |
|---|---|---|
| `posicao_dashboard` | `horizontal` \| `vertical` | Descontinuado como eixo separado (ADR-0010). Mantido apenas por compatibilidade em handoff futuro de migração. Substituído pela composição declarativa geral do corpo. |

### 4.4 Capacidades declaradas por instância de `console`

As capacidades abaixo são declaradas pela instância de `console` no `tela.json`,
não como eixo universal por tela:

| Capacidade | Valores | Observação |
|---|---|---|
| `tipo_exibicao` | `normal` \| `verboso` | Aplica-se **apenas** a `console`; modo verboso é estado de exibição reutilizável |
| `paginacao` | `com` \| `sem` | Paginação é consequência do conteúdo renderizado que não cabe; filtros atuam antes |
| `colunas_ajustavel` | `com` \| `sem` | `com` habilita chip `[-][+]` |
| `filtro_de_grupo` | `com` \| `sem` | `com` condiciona a existência do chip `[#]` |
| `formacao_de_selecao` | `com` \| `sem` | `com` condiciona a existência do chip `[␣]` e participa do rótulo dinâmico de `[⏎]` |

### 4.5 `lancador` — itens declarados na instância

Cada instância de `lancador` declara no `tela.json`:

- título;
- lista de itens (`itens[]`);
- cada item: `chip`, `texto`, `tela_destino`.

Adicionar item ao `lancador` é alteração declarativa no JSON da tela. Detalhes
internos do `lancador` pertencem a `contrato_lancador.md`.

### 4.6 Espaçamento interno (universal)

O renderer sempre insere uma linha em branco entre a borda e o conteúdo em
qualquer elemento do corpo, sem exceção e sem possibilidade de supressão pela
tela, pelo estilo ou pelo tipo de conteúdo.

### 4.7 Ocupação vertical da janela (ADR-0013)

A tela deve ocupar a largura **e** a altura disponíveis da janela do terminal.
A largura já é tratada dinamicamente; a `altura_disponivel` é **dimensão
futura** da renderização da tela, a ser propagada em handoff futuro.

Distinção obrigatória (não colapsa):

| Termo específico | Significado |
|---|---|
| `corpo.arranjo = "vertical"` | Ordem/composição vertical dos elementos do corpo (ADR-0011) |
| `ocupacao_vertical_terminal` / `preenchimento_altura_corpo` | Preenchimento da altura da janela entre `cabecalho` e `barra_de_menus` (ADR-0013) |

O corpo deve poder ocupar a altura disponível com **preenchimento de linhas
em branco** adicionadas pelo renderer quando o conteúdo declarado for menor
que a altura disponível. Esse preenchimento é **responsabilidade do
renderer**, não do `tela.json` — o JSON não declara linhas de preenchimento.

A decisão de ocupação vertical **não introduz novo arranjo nem altera a
composição** declarada em `corpo.arranjo`: uma tela com
`corpo.arranjo = "horizontal"` também deve poder ocupar a altura disponível.
A representação exata das linhas de preenchimento (linha visual interna à
caixa do corpo vs. linha física com largura total) é decisão de handoff
futuro, desde que não seja tratada como novo arranjo nem novo tipo de
elemento do corpo.

**Mecanismo de obtenção de dimensões (ADR-0017, 2026-07-11)**: a política
normativa de obtenção, validação e atualização de largura e altura durante a
sessão TTY é definida pela ADR-0017. A cadeia de obtenção — `ioctl(TIOCGWINSZ)`
→ `LINES`/`COLUMNS` → fallback ou últimas dimensões válidas — e a política de
redimensionamento reativo estão registradas em `contrato_tela_json.md` seção 24.
A `altura_disponivel` é obtida por esse mecanismo durante a sessão TTY. O
redimensionamento não altera `corpo.arranjo` nem `tiling`.

### 4.8 Arranjo por container (ADR-0015)

Cada container (`corpo` ou `grupo`) declara o **arranjo dos seus filhos diretos**.

| Valor | Efeito |
|---|---|
| `horizontal` | reparte largura entre filhos diretos |
| `vertical` | reparte altura entre filhos diretos |

O arranjo de um container **não obriga** o arranjo dos containers filhos.

**Arranjo e distribuição são distintos (ADR-0018, 2026-07-11)**: `arranjo`
declara a **ordem/composição** dos filhos diretos no eixo; ele **não** determina
sozinho a repartição proporcional de toda a área do container. Em particular,
`corpo.arranjo = "vertical"` ordena os filhos verticalmente, mas **não** implica
automaticamente o modo `igual` nem obriga repartir proporcionalmente toda a altura
disponível. `arranjo` permanece válido sem `distribuicao`. A repartição
proporcional de área só ocorre quando o container declara `distribuicao`
(seção 4.9). A tabela acima descreve o eixo repartido **quando há distribuição
explícita**; sem distribuição, ver a semântica de ausência na seção 5.7.

### 4.9 Distribuição por container (ADR-0015)

A distribuição pertence ao mesmo container que declara o arranjo.

- container horizontal: distribuição reparte colunas/largura;
- container vertical: distribuição reparte linhas/altura;
- distribuição aloca área, não apenas conteúdo;
- elemento funcional deve preservar a área alocada;
- sobra horizontal vira padding/espaços em branco;
- sobra vertical vira linhas em branco.

**Ausência × distribuição explícita (ADR-0018, 2026-07-11)**: a `distribuicao`
é **opcional**. Sua ausência **não** equivale ao modo `igual` e **não** dispara
repartição proporcional automática da área útil (ver seção 5.7). Quando um
container **declara** `distribuicao`, a área útil disponível — no eixo do arranjo —
é repartida integralmente entre os filhos diretos: a soma das cotas ocupa **toda**
a área distribuível, descontadas apenas as linhas/colunas estruturais externas
definidas pelos contratos aplicáveis. A distribuição aloca área (não somente o
tamanho natural do conteúdo), e a cota excedente ao conteúdo vira preenchimento
**interno** da moldura do elemento (seção 5.9), nunca sobra acumulada fora do
último filho.

**Regra de quantidade de valores:**

```
len(distribuicao.valores) == len(elementos)
```

Conta somente filhos diretos do container. Não conta netos, descendentes
internos de grupo nem elementos visuais resultantes de expansão.

---

## 5. Regras de layout

### 5.1 Organização horizontal por tipo de conteúdo

| Tipo | Modo | Organização |
|---|---|---|
| `lancador` | `fila` ou `matriz` (calculado automaticamente) | Linha única horizontal ou grade de colunas; nunca pagina — ver seção 5.2 |
| `console` | `normal` | Colunar: `n_col` colunas, valor ajustável |
| `console` | `verboso` | Tabular: largura de coluna calculada por conteúdo; texto longo quebra dentro da célula |

**Largura e altura dinâmicas (ADR-0017)**: calculadas a partir das dimensões
reais do terminal em sessão TTY ativa. A cadeia normativa de obtenção e
validação do par largura/altura, a política de `SIGWINCH` e a cadeia de fallback
são definidas pela ADR-0017 e registradas em `contrato_tela_json.md` seção 24.
Sem perfis fixos pré-definidos. O redimensionamento não altera `corpo.arranjo`
nem `tiling`; somente distribuições visuais já autorizadas e dependentes da
dimensão real são recalculadas.

**Overflow**: nunca existe scroll. Conteúdo que excede o espaço disponível
sempre pagina, exceto `lancador`. Espaço sobrando é preenchido (padding), nunca
deixado vazio de forma desorganizada.

**Valores parametrizados de layout do `console`**: vãos, alinhamento,
configuração de colunas e navegação são lidos no futuro caminho
`config/layouts/layout_console.json`, não hardcoded — artefato ativo
transicional a reavaliar conforme ADR-0008 e organizado pela ADR-0021.
O `lancador` lê seus próprios parâmetros no futuro caminho
`config/elementos/lancador.json`, conforme `contrato_lancador.md` — também
ativo transicional a reavaliar conforme ADR-0008. `config/layouts/layout_dado.json`
permanece apenas como artefato obsoleto/transicional de rastreabilidade da
migração `dado` → `console`.

---

### 5.2 Elemento `lancador`

`lancador` é elemento do corpo declarado no `tela.json`. Este contrato define
apenas seu encaixe na composição geral do corpo:

- `lancador` é elemento válido do corpo.
- `lancador` não é navegável por `[✥]` nem pelas setas da `barra_de_menus`.
- `lancador` não usa `tipo_exibicao`.
- `lancador` não pagina.
- O modo calculado automaticamente pelo renderer é `distribuicao_lancador`: `fila` ou `matriz`.
- A tela não declara `distribuicao_lancador` como eixo explícito.
- `lancador` possui título e lista de itens declarados no `tela.json`.
- Cada item declara chip/letra, texto (máx. 15 caracteres) e `tela_destino`.
- Adicionar item ao `lancador` é alteração declarativa no JSON da tela.

As regras internas de estrutura, vãos, colunas, título, item, navegação e
validação do `lancador` pertencem a `contrato_lancador.md` e aos valores
concretos de `config/elementos/lancador.json`; este contrato não as duplica.
`contrato_lancador.md` será revisado conforme ADR-0008 e ADR-0021 em tarefa
posterior.

---

### 5.3 Elemento `dashboard`

**ADR-0010**: `dashboard` é elemento funcional do corpo como `console` e
`lancador`. Seu posicionamento é controlado pela estrutura declarativa geral
do `corpo` — não por eixo separado.

`dashboard` é elemento passivo do corpo declarado no `tela.json`:

- não é navegável por `[✥]`;
- não é obrigatório — sua presença exige elemento `tipo=dashboard` em
  `corpo.elementos[]` no `tela.json`;
- possui moldura própria;
- não possui conteúdo universal fixo;
- não haverá `config/dashboard.json`;
- conteúdo e campos vêm da instância declarada no `tela.json` da tela;
- o compositor não conhece os campos internos do `dashboard`;
- o renderer não deve hardcodar conteúdo, composição ou campos de nenhuma
  instância de `dashboard`.

A estrutura de 8 campos de resumo + Total + 8 marcadores abaixo é o **draft
da instância de `dashboard` da tela raiz do Orquestrador** — exemplo e instância
conhecida, não regra universal da classe `dashboard`. O antigo `Info` é o draft
dessa instância.

**Alinhamento horizontal**: coluna dimensionada pelo maior rótulo, itens alinhados
à esquerda dentro do bloco. O posicionamento horizontal do `dashboard` na
composição da tela é determinado pela estrutura declarativa do `corpo`
(ADR-0010); o campo `posicao_dashboard` como eixo separado foi descontinuado.

**Alinhamento vertical**: mesma mecânica do `lancador` (seção 5.2), com a exceção
obrigatória: a linha em branco entre Total e início da lista de marcadores é
sempre exatamente 1 e não está sujeita à distribuição uniforme geral.

**Draft da instância do Orquestrador — campos do resumo** (8 campos, conjunto
fechado do draft): Adicionados, Fichados, Consolidados, Qualificados, Orfão,
Missing, Secundários, Descartados.

**Draft — marcadores** (8, conjunto fechado do draft):

| Símbolo | Rótulo |
|---|---|
| `!` | Retido |
| `@` | Incompleto |
| `?` | Ausência |
| `*` | Revisão |
| `&` | Dissonância |
| `%` | Indevido |
| `~` | Atualização |
| `^` | Mesclado |

**Formato do valor numérico** (draft do Orquestrador): número puro, sem zero à
esquerda, alinhado à direita dentro do campo. Todo campo sempre exibe um número
— nunca existe travessão (`—`) ou campo vazio; `0` é exibido normalmente.

*Distinção de escopo*: esta regra numérica é exclusiva do draft do Orquestrador.
Não se confunde com a restrição de exatamente 1 caractere fixo dos símbolos de
borda, chip e indicadores de estilo, definida em `contrato_estilo.md`.

---

### 5.4 Elemento `console`

`console` é um container interativo e navegável genérico. A política geral de
composição pertence à instância do `console`, declarada pelo `tela.json`:

- pode conter itens heterogêneos;
- o cursor navega por itens, não por linhas físicas;
- cada item pode declarar tipo, binding, navegabilidade, seleção e ação;
- filtros atuam antes da paginação;
- paginação é consequência do conteúdo renderizado que não cabe;
- modo verboso é estado de exibição reutilizável — não é variação específica
  de cada tela;
- `[⏎]` fica ativo quando o item em foco possui ação válida; inativo caso contrário;
- `[✥]` é restrito a `console` navegável;
- `[␣]` só existe quando a instância declara formação de seleção múltipla.

Os contratos/classes de tipos internos de item de `console` são pendência
DOC-B008. A revisão formal do `console` como container genérico é DOC-0024.

---

### 5.5 Indicador de paginação (quando `paginacao = com`)

O indicador de página é renderizado na **última linha da borda do próprio
elemento paginado**, ancorado à direita. Pertence à borda do elemento — não ao
layout geral da tela, não à barra_de_menus, não ao objeto dashboard.

**Composição da linha, lida da direita para a esquerda:**

| Posição | Elemento | Fonte |
|---|---|---|
| 1 (extrema direita) | `canto_inferior_direito` | estilo ativo |
| 2 | 1 unidade de `traco_inferior` | estilo ativo |
| 3 | bloco `─ página X/Y ─` | **traço literal** `─`, independente do estilo ativo |
| 4 (até a extrema esquerda) | preenchimento até `canto_inferior_esquerdo` | `traco_inferior` do estilo ativo |

O bloco de texto na posição 3 estica conforme o número de dígitos de X e Y
(ex.: `1/3` vs `12/47`). O preenchimento da posição 4 encolhe para compensar,
mantendo a largura total da borda constante.

O traço literal da posição 3 é sempre `─`, inclusive no estilo `aberta`, onde
`traco_inferior` normal é espaço. Esta é a única exceção ao princípio geral de
que todos os caracteres de borda vêm do estilo ativo.

**Casos especiais:**

- **dashboard presente**: o indicador permanece na borda do elemento paginado.
  O objeto dashboard não herda, não desloca, e não recebe o indicador — mesmo
  estando fisicamente mais próximo da barra_de_menus.
- **Arranjo horizontal (`arranjo = "horizontal"`)**: cada elemento exibe sua própria paginação, ancorada à direita dentro da própria borda, independente do lado da tela.
- **Combinação `corpo.arranjo = "horizontal"` + `dashboard` presente**: não definida — ver seção 9.

---

### 5.6 Tiling — duas camadas de decisão

Aplica-se ao arranjo de elementos do corpo declarados em `corpo.elementos[]`.
**ADR-0010**: `dashboard` é elemento funcional do corpo e pode participar da
composição declarada. O campo `posicao_dashboard` como eixo separado está
descontinuado (seção 4.3).

**Camada 1 — Fixação no `tela.json`**: o `tela.json` pode declarar
explicitamente `arranjo = vertical` ou `arranjo = horizontal` (terminologia
final, ADR-0011; `sobreposto`/`lado_a_lado` aceitos como aliases
transicionais). Quando declarado, o renderer usa esse valor diretamente e
**ignora** o campo `tiling` do estilo ativo para aquela tela.

**Camada 2 — Default do estilo**: quando o `tela.json` não declara `arranjo`,
o renderer consulta o campo `tiling` do estilo ativo (`config/estilo.json`).
Esse valor é escolha manual do usuário; o renderer usa-o diretamente, sem
modificação, sem fallback baseado em largura de terminal.

`estilo.json` não decide composição — provê apenas o default de arranjo quando
o `tela.json` não o declara. O renderer não decide sozinho o arranjo por largura.
O cálculo visual permitido pelo renderer limita-se à distribuição de espaço
dentro da regra declarada.

**Distribuição de espaço em modo horizontal** (`horizontal`, ADR-0011;
historicamente "lado a lado"): a regra é **particionamento contíguo** da
largura disponível entre os filhos diretos. Não existem vãos externos entre
molduras. Molduras adjacentes ficam coladas, produzindo bordas lado a lado
(`││`, `╮╭`, `╯╰`). A primeira moldura inicia no primeiro caractere útil;
a última termina no último caractere útil. (ADR-0015)

> **Nota**: a formulação anterior de "3 vãos iguais" registrada neste contrato
> e em `docs/NOMENCLATURA.md` seção 10 está **supersedida** pela ADR-0015. A
> regra correta é particionamento contíguo, conforme decisão explícita do usuário
> na revisão pós-auditoria do H-0019 (2026-07-09). `docs/NOMENCLATURA.md`
> seção 10 foi atualizada neste ciclo — a regra de "3 vãos iguais" consta apenas
> como referência histórica supersedida; a regra vigente é particionamento contíguo
> conforme ADR-0015.

---

### 5.7 Modos de distribuição (ADR-0015, ADR-0018)

#### Ausência de `distribuicao` — construção orientada pelo conteúdo (ADR-0018)

Quando um container **não** declara `distribuicao`:

- preserva-se a construção orientada pelo conteúdo;
- cada filho direto usa sua **dimensão natural** conforme o conteúdo e as regras
  próprias do tipo;
- a ausência **não** equivale ao modo `igual` e **não** é fallback implícito de
  nenhum modo;
- **não** se reparte automaticamente toda a área útil entre os filhos;
- a sobra no eixo do arranjo pode permanecer como **preenchimento externo** do
  container, conforme o mecanismo de ocupação já existente (ADR-0013) — no eixo
  vertical, linhas em branco acumuladas entre o último filho e a região seguinte.

Esta é a substituição normativa introduzida pela ADR-0018 (2026-07-11) sobre o
ponto em que a ausência de `distribuicao` era tratada como equivalente ao modo
`igual`. Ver seção 10 (relação ADR-0015 × ADR-0018).

#### Modo `igual` (explícito)

Divide a área disponível igualmente entre filhos diretos, com pesos iguais,
aplicando arredondamento e resíduos conforme a seção 5.8. `igual` é um modo
**válido apenas quando declarado explicitamente**; **não** é o significado
implícito da ausência de `distribuicao` (ADR-0018).

#### Modo `percentual`

- `distribuicao.valores[]` declara percentuais explícitos;
- quantidade de valores deve ser igual à quantidade de filhos diretos;
- soma dos valores deve ser exatamente 100;
- valores devem ser positivos;
- soma diferente de 100 é inválida.

Exemplo: `[40, 20, 40]` significa 40%, 20%, 40%.

#### Modo `fracao`

- `distribuicao.valores[]` declara pesos relativos;
- quantidade de valores deve ser igual à quantidade de filhos diretos;
- todos os valores devem ser positivos;
- denominador implícito é a soma dos pesos;
- fração de cada filho é `valor_do_filho / soma_dos_valores`.

**Genericidade (ADR-0018)**: qualquer vetor válido de pesos positivos deve ser
suportado. O renderer **não** pode ser especializado para um vetor concreto nem
hardcodar valores. Os vetores abaixo são **exemplos não exaustivos**, não
defaults nem regras internas:

- `[1, 1, 1]` significa `1/3`, `1/3`, `1/3` (pesos iguais);
- `[2, 1, 2]` significa `2/5`, `1/5`, `2/5`, equivalente a 40%, 20%, 40%;
- `[1, 3, 1]` e `[5, 2, 7]` são igualmente válidos.

`[2, 1, 2]` é apenas uma possível configuração concreta de tela — não é regra
interna do renderer. Um vetor matematicamente válido não se torna inválido
apenas porque o conteúdo natural de um elemento não cabe na cota em terminal
pequeno; esse caso é lacuna externa à ADR-0018 (ver seção 5.7.1).

#### 5.7.1 Conteúdo maior que a cota — lacuna externa à ADR-0018

Quando uma cota atribuída for menor que a altura/largura natural do conteúdo de
um elemento (por exemplo, em terminal muito pequeno), o tratamento **não** está
decidido por esta versão. Ficam explicitamente **fora de escopo** da ADR-0018,
sem política escolhida aqui:

- altura mínima;
- overflow;
- truncamento;
- paginação de `lancador`;
- rejeição;
- degradação;
- redistribuição baseada no conteúdo natural;
- prioridade por tipo de elemento.

Um vetor válido continua válido; a insuficiência de cota é problema normativo
separado (conteúdo que não cabe) e não bloqueia a distribuição geral em alturas
onde o conteúdo cabe. Ver também a seção 5.10 (conceitos dinâmicos futuros) e a
política de terminal pequeno da ADR-0017.

#### Distribuição restrita/dinâmica

Conceitos futuros: `minimo`, `preferido`, `maximo`, `restante`, `conteudo`.
Ver seção 5.10.

---

### 5.8 Arredondamento determinístico (ADR-0015)

Como terminal usa células inteiras, percentuais/frações devem ser convertidos
pelo **método dos maiores restos**.

Regras:
- soma final das áreas alocadas deve ser exatamente igual à área disponível
  do container;
- empates de resto são resolvidos pela ordem declarada em `elementos[]`.

**Algoritmo:**
1. calcular tamanho ideal real de cada filho;
2. tomar a parte inteira;
3. somar partes inteiras;
4. calcular o resto necessário para fechar a área total;
5. distribuir unidades restantes aos maiores restos;
6. em empate, priorizar ordem declarada.

**Exemplos:**
- 68 linhas com `[1, 1, 1]` resulta em `[23, 23, 22]`.
- 68 linhas com `[2, 1, 2]` resulta em `[27, 14, 27]`.

---

### 5.9 Preenchimento de área alocada (ADR-0015)

A distribuição define **área alocada**. O renderer deve preservar a área
alocada. Se o conteúdo não preencher a área, o restante deve ser preenchido
com branco.

- **Horizontal:** preencher com espaços; preservar largura da faixa.
- **Vertical:** preencher com linhas em branco; preservar altura da faixa.

**Preenchimento interno quando há distribuição explícita (ADR-0018, 2026-07-11)**:
quando a cota atribuída for maior que o conteúdo natural do elemento, a moldura
do elemento ocupa a **cota completa** e a sobra vira linhas em branco (ou espaços,
no eixo horizontal) **dentro** da moldura desse elemento. A sobra **não** fica
acumulada externamente abaixo do último filho. No eixo vertical com distribuição
explícita, o espaço entre a borda inferior do último elemento e a região seguinte
(por exemplo, a `barra_de_menus`) é incorporado às áreas dos filhos. A distinção
é normativa: **sem** `distribuicao`, a sobra pode permanecer externa (seção 5.7,
ADR-0013); **com** `distribuicao`, a sobra é interna às molduras.

---

### 5.10 Regras dinâmicas de dimensão (ADR-0015 — conceitos futuros)

Conceitos registrados para ciclos futuros:

| Conceito | Significado |
|---|---|
| `minimo` | menor dimensão permitida |
| `preferido` | dimensão desejada |
| `maximo` | maior dimensão permitida |
| `restante` | recebe espaço remanescente após alocação de outros |
| `conteudo` | dimensão ajustada ao conteúdo renderizado |

**Decisão normativa**: `ajustado ao conteúdo` deve ser tratado como
`preferido`, não como `minimo`.

Justificativa:
- permite combinar `preferido = conteudo` com `maximo = 30%`;
- evita contradição quando conteúdo exigiria mais espaço que o máximo;
- se o conteúdo exceder o máximo, o elemento recebe o máximo e aplica
  overflow/paginação.

**Terminal pequeno demais (ADR-0017)**: quando as dimensões forem válidas mas
insuficientes para a tela normal, a sessão TUI exibe quadro mínimo de aviso
("terminal pequeno demais") e recupera automaticamente quando dimensões
suficientes forem restauradas — ver `contrato_tela_json.md` seção 24. Área
menor que a mínima normal deve ter política determinística. Representação
compacta futura com `...` é política de overflow/compactação — não fallback de
composição. Não pode haver truncamento silencioso nem fallback silencioso para
outro arranjo.

---

### 5.11 Paginação dentro da área alocada (ADR-0015)

A composição aloca área. A paginação acontece **dentro** da área alocada.

Se um `console` recebe 10 linhas e tem conteúdo para 100 linhas, o compositor
não aumenta automaticamente o console. O console pagina dentro das 10 linhas,
conforme política declarada.

---

### 5.12 Sincronização de cortes entre grupos (ADR-0015)

Sincronização automática de cortes entre grupos irmãos só é garantida quando
os grupos possuem:
- mesmo eixo interno de arranjo;
- mesma quantidade de filhos diretos;
- mesma distribuição declarada;
- mesma dimensão disponível no eixo distribuído;
- mesma assinatura de restrições dimensionais (`minimo`, `preferido`,
  `maximo`, `overflow`, `restante`, `conteudo`).

Se restrições diferentes alterarem os cortes, a sincronização automática
não é garantida.

**Sincronização explícita futura (conceito):**

```json
{
  "sincronizacao": {
    "grupo": "colunas_principais",
    "cortes": "obrigatorio"
  }
}
```

Se `cortes = obrigatorio` e os grupos não puderem alinhar cortes, o renderer
deve gerar erro determinístico — nunca ajustar silenciosamente. Schema final
deste campo não é fechado nesta versão.

---

### 5.13 Distinção normativa `livre` × `matriz` (ADR-0020, D1–D4)

**Em `estrutura: livre`** (ou ausência de `estrutura`):

- `arranjo` é válido;
- `distribuicao` é opcional; sua ausência preserva a construção orientada pelo
  conteúdo (ADR-0018) e **não** equivale ao modo `igual`;
- não há grade bidimensional compartilhada.

**Em `estrutura: matriz`**:

- `arranjo` é proibido;
- distribuição de **ambos os eixos** é obrigatória;
- ausência de distribuição em qualquer eixo invalida a matriz;
- não existe distribuição implícita, default para `igual`, dimensionamento por
  conteúdo natural, herança nem inferência (D6);
- existe uma única grade compartilhada de coordenadas (D7).

Esta distinção não altera a semântica da ADR-0018 para grupos `livre`.

---

### 5.14 Dimensões da matriz (ADR-0020, D5)

Em `estrutura: matriz`, as dimensões devem respeitar:

```text
mínimo: 2 linhas × 2 colunas
máximo: 4 linhas × 4 colunas
```

Combinações válidas:

```text
2 × 2  |  2 × 3  |  2 × 4
3 × 2  |  3 × 3  |  3 × 4
4 × 2  |  4 × 3  |  4 × 4
```

São inválidas: dimensão menor que 2; dimensão maior que 4; matriz com somente
uma linha; matriz com somente uma coluna. Não existe fallback para `livre`.

---

### 5.15 Distribuições obrigatórias por eixo (ADR-0020, D6)

Em `estrutura: matriz`, as distribuições de ambos os eixos são **obrigatórias**:

```text
matriz.linhas.distribuicao   — obrigatório
matriz.colunas.distribuicao  — obrigatório
```

Regras:

- a omissão de qualquer distribuição invalida a matriz;
- cada eixo possui sua própria distribuição independente;
- a distribuição de um eixo não é herdada, inferida ou reutilizada pelo outro;
- não existe distribuição implícita;
- não existe default para `igual`;
- não existe dimensionamento por conteúdo natural;
- não existe herança do container pai;
- não existe inferência pela quantidade de linhas ou colunas;
- não existe fallback para `estrutura: livre`.

Para divisão igual, deve existir declaração explícita:

```json
"distribuicao": {
  "modo": "igual"
}
```

Para `percentual`: `valores` possui quantidade igual à dimensão do eixo e a
soma deve ser 100. Para `fracao`: `valores` possui quantidade igual à dimensão
do eixo e os valores são pesos positivos. O algoritmo dos maiores restos
(seção 5.8) é aplicado **separadamente** em cada eixo.

**Esta obrigatoriedade é específica de `estrutura: matriz` e não altera a
semântica de ausência de distribuição para grupos `livre` (ADR-0018).**

Invariantes de distribuição de eixo matricial:

```text
INV-MAT-DIST-01: Toda matriz declara distribuição de linhas.
INV-MAT-DIST-02: Toda matriz declara distribuição de colunas.
INV-MAT-DIST-03: A ausência da distribuição de qualquer eixo invalida a matriz.
INV-MAT-DIST-04: O modo igual depende de declaração explícita.
INV-MAT-DIST-05: Nenhum eixo matricial é dimensionado por conteúdo natural.
INV-MAT-DIST-06: A distribuição de um eixo não é herdada, inferida ou
                  reutilizada pelo outro eixo.
```

---

### 5.16 Grade comum de coordenadas (ADR-0020, D7)

O container `matriz` exige o cálculo de **uma única grade compartilhada** de:

- coordenadas horizontais das linhas;
- coordenadas verticais das colunas.

Todas as células usam essas coordenadas comuns.

Consequências normativas obrigatórias:

- bordas de células da mesma linha permanecem alinhadas horizontalmente;
- bordas de células da mesma coluna permanecem alinhadas verticalmente;
- encontros de divisórias compartilham coordenadas;
- os cortes não são calculados de forma independente por célula.

A implementação futura deverá calcular os cortes horizontais (linhas) e
verticais (colunas) uma única vez para o container, usando a grade comum
para todas as células. O renderizador deverá futuramente aplicar maiores
restos separadamente por eixo e preservar bordas alinhadas dentro da matriz.

---

### 5.17 Células com coordenadas explícitas (ADR-0020, D8)

A posição de cada filho na grade é determinada por coordenadas explícitas:

```json
{
  "linha": 1,
  "coluna": 1,
  "elemento": "id_do_elemento"
}
```

Regras:

- índices iniciados em 1;
- `elemento` referencia o `id` de um filho direto declarado em `elementos[]`;
- a posição é determinada pelas coordenadas, não pela ordem de `celulas[]`;
- cada coordenada aparece exatamente uma vez em `celulas[]`;
- cada elemento é associado exatamente uma vez;
- coordenada fora das dimensões declaradas é inválida;
- referência a elemento inexistente é inválida;
- duplicidade de coordenada é inválida;
- duplicidade de elemento é inválida.

---

### 5.18 Cobertura completa (ADR-0020, D10)

Na versão atual da especificação:

- células vazias são proibidas;
- toda coordenada válida deve estar preenchida;
- todo filho direto deve estar associado;
- quantidade de células = `linhas × colunas`;
- quantidade de elementos associados = `linhas × colunas`.

O contrato exige cobertura total. Não criar placeholder, célula nula ou
preenchimento automático. Esse tema poderá ser revisado futuramente por nova
ADR.

---

### 5.19 Conteúdo das células e profundidade (ADR-0020, D9; ADR-0019)

Uma célula referencia um filho direto dos tipos já permitidos:

```text
console
lancador
dashboard
grupo
```

Um `grupo` dentro de uma célula continua sujeito ao limite de profundidade
da ADR-0019:

- a matriz não acrescenta nível de profundidade;
- somente nós `grupo` contam como nível (ADR-0019, D1);
- linhas, colunas e células não contam como níveis;
- um `grupo` filho de um grupo do nível 3 estaria no nível 4 e é
  estruturalmente inválido mesmo que esteja dentro de uma célula matricial.

---

### 5.20 Rejeição determinística de matriz inválida (ADR-0020, D12)

Uma declaração matricial inválida deve ser rejeitada deterministicamente.

O loader deverá futuramente rejeitar sem exceções — não é permitido:

- ignorar campos inválidos;
- corrigir dimensões automaticamente;
- completar células ausentes;
- remover células excedentes;
- inferir coordenadas;
- inferir distribuição;
- converter silenciosamente para `livre`.

---

### 5.21 Terminal e área insuficiente em matriz (ADR-0020, D14)

Preservar as regras globais existentes (ADR-0017):

- dimensões dinâmicas;
- `SIGWINCH`;
- quadro global de terminal pequeno;
- integridade estrutural.

A política específica de área insuficiente para matrizes permanece pendente.

Não estão decididos nesta versão:

- mínimo numérico por célula;
- paginação da matriz;
- rolagem da matriz;
- truncamento específico por célula;
- redução automática de dimensões.

---

### 5.22 Schema normativo da matriz (ADR-0020)

O schema abaixo é normativo e deve ser documentado como norma aprovada,
não como implementação concluída.

```json
{
  "id": "grupo_matriz_2x2",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {
        "modo": "igual"
      }
    },
    "colunas": {
      "quantidade": 2,
      "distribuicao": {
        "modo": "igual"
      }
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "a"},
      {"linha": 1, "coluna": 2, "elemento": "b"},
      {"linha": 2, "coluna": 1, "elemento": "c"},
      {"linha": 2, "coluna": 2, "elemento": "d"}
    ]
  },
  "elementos": [
    {"id": "a", "tipo": "console"},
    {"id": "b", "tipo": "console"},
    {"id": "c", "tipo": "dashboard"},
    {"id": "d", "tipo": "console"}
  ]
}
```

---

### 5.23 Exemplos válidos de composição matricial (ADR-0020)

#### EX-MAT-V1 — Matriz 2×2 com `igual` explícito nos dois eixos

```json
{
  "id": "g_2x2",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
    "colunas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "e1"},
      {"linha": 1, "coluna": 2, "elemento": "e2"},
      {"linha": 2, "coluna": 1, "elemento": "e3"},
      {"linha": 2, "coluna": 2, "elemento": "e4"}
    ]
  },
  "elementos": [
    {"id": "e1", "tipo": "console"},
    {"id": "e2", "tipo": "dashboard"},
    {"id": "e3", "tipo": "lancador"},
    {"id": "e4", "tipo": "console"}
  ]
}
```

#### EX-MAT-V2 — Matriz 2×4 com frações diferentes entre linhas e colunas

```json
{
  "id": "g_2x4",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {"modo": "fracao", "valores": [1, 2]}
    },
    "colunas": {
      "quantidade": 4,
      "distribuicao": {"modo": "fracao", "valores": [1, 2, 1, 2]}
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "a"},
      {"linha": 1, "coluna": 2, "elemento": "b"},
      {"linha": 1, "coluna": 3, "elemento": "c"},
      {"linha": 1, "coluna": 4, "elemento": "d"},
      {"linha": 2, "coluna": 1, "elemento": "e"},
      {"linha": 2, "coluna": 2, "elemento": "f"},
      {"linha": 2, "coluna": 3, "elemento": "g"},
      {"linha": 2, "coluna": 4, "elemento": "h"}
    ]
  },
  "elementos": [
    {"id": "a", "tipo": "console"}, {"id": "b", "tipo": "console"},
    {"id": "c", "tipo": "dashboard"}, {"id": "d", "tipo": "console"},
    {"id": "e", "tipo": "console"}, {"id": "f", "tipo": "lancador"},
    {"id": "g", "tipo": "dashboard"}, {"id": "h", "tipo": "console"}
  ]
}
```

#### EX-MAT-V3 — Matriz com modos diferentes entre linhas e colunas

```json
{
  "id": "g_modos_diff",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 3,
      "distribuicao": {"modo": "igual"}
    },
    "colunas": {
      "quantidade": 2,
      "distribuicao": {"modo": "percentual", "valores": [40, 60]}
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "c1"},
      {"linha": 1, "coluna": 2, "elemento": "c2"},
      {"linha": 2, "coluna": 1, "elemento": "c3"},
      {"linha": 2, "coluna": 2, "elemento": "c4"},
      {"linha": 3, "coluna": 1, "elemento": "c5"},
      {"linha": 3, "coluna": 2, "elemento": "c6"}
    ]
  },
  "elementos": [
    {"id": "c1", "tipo": "console"}, {"id": "c2", "tipo": "dashboard"},
    {"id": "c3", "tipo": "console"}, {"id": "c4", "tipo": "console"},
    {"id": "c5", "tipo": "lancador"}, {"id": "c6", "tipo": "console"}
  ]
}
```

#### EX-MAT-V4 — Grupo `livre` sem `estrutura` (comportamento preservado)

```json
{
  "id": "grupo_existente",
  "tipo": "grupo",
  "arranjo": "horizontal",
  "distribuicao": {"modo": "fracao", "valores": [1, 1]},
  "elementos": [
    {"id": "a", "tipo": "console"},
    {"id": "b", "tipo": "dashboard"}
  ]
}
```

A ausência de `estrutura` equivale a `livre`. Todos os JSONs existentes sem
`estrutura` continuam válidos e com comportamento preservado (D3, D15).

#### EX-MAT-V5 — Grupo `livre` com `estrutura` declarado explicitamente

```json
{
  "id": "grupo_livre",
  "tipo": "grupo",
  "estrutura": "livre",
  "arranjo": "vertical",
  "elementos": [
    {"id": "c", "tipo": "console"},
    {"id": "d", "tipo": "lancador"}
  ]
}
```

---

### 5.24 Exemplos inválidos de composição matricial (ADR-0020)

#### EX-MAT-I1 — Ausência de distribuição de linhas — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 2},
    "colunas": {"quantidade": 3, "distribuicao": {"modo": "igual"}},
    "celulas": [...]
  }
}
```

`linhas.distribuicao` ausente. O contrato exige que a distribuição de linhas
seja explícita (INV-MAT-DIST-01). O loader deverá futuramente rejeitar antes
da construção do modelo.

#### EX-MAT-I2 — Ausência de distribuição de colunas — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
    "colunas": {"quantidade": 3},
    "celulas": [...]
  }
}
```

`colunas.distribuicao` ausente. O contrato exige que a distribuição de colunas
seja explícita (INV-MAT-DIST-02).

#### EX-MAT-I3 — Somente um eixo com distribuição — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
    "colunas": {"quantidade": 2},
    "celulas": [...]
  }
}
```

Declarar distribuição em apenas um eixo não torna a matriz válida; ambos os
eixos são obrigatórios (INV-MAT-DIST-03).

#### EX-MAT-I4 — Coordenada duplicada — inválido

```json
{
  "celulas": [
    {"linha": 1, "coluna": 1, "elemento": "e1"},
    {"linha": 1, "coluna": 1, "elemento": "e2"}
  ]
}
```

Coordenada `(1, 1)` duplicada (D8). O loader deverá futuramente rejeitar.

#### EX-MAT-I5 — Elemento duplicado — inválido

```json
{
  "celulas": [
    {"linha": 1, "coluna": 1, "elemento": "e1"},
    {"linha": 1, "coluna": 2, "elemento": "e1"}
  ]
}
```

`e1` aparece em duas células (D8). O loader deverá futuramente rejeitar.

#### EX-MAT-I6 — Célula faltante — inválido

Matriz declarada como `2 × 2` com apenas 3 células declaradas. O contrato
exige que toda coordenada válida seja declarada exatamente uma vez (D8, D10).

#### EX-MAT-I7 — `arranjo` em `estrutura: matriz` — inválido

```json
{
  "tipo": "grupo",
  "estrutura": "matriz",
  "arranjo": "horizontal",
  "matriz": {...}
}
```

`arranjo` é proibido em `estrutura: matriz` (D13). O loader deverá futuramente
rejeitar.

#### EX-MAT-I8 — Quarto nível de grupo em célula — inválido

```json
{
  "id": "nivel1",
  "tipo": "grupo",
  "elementos": [{
    "id": "nivel2",
    "tipo": "grupo",
    "elementos": [{
      "id": "nivel3_mat",
      "tipo": "grupo",
      "estrutura": "matriz",
      "matriz": {
        "linhas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
        "colunas": {"quantidade": 2, "distribuicao": {"modo": "igual"}},
        "celulas": [
          {"linha": 1, "coluna": 1, "elemento": "nivel4"},
          ...
        ]
      },
      "elementos": [
        {"id": "nivel4", "tipo": "grupo", ...}
      ]
    }]
  }]
}
```

`nivel4` seria nível de grupo 4 (inválido — ADR-0019, D4). A matriz não cria
nível extra, mas o `grupo` filho dentro da célula conta normalmente.

#### EX-MAT-I9 — Matriz inválida sem fallback — inválido

Uma declaração matricial inválida não pode ser convertida silenciosamente para
`livre` (D12). O loader deverá futuramente rejeitar com erro determinístico —
nunca ajustar silenciosamente nem tentar renderizar como `livre`.

---

## 6. Relação com `barra_de_menus`

`barra_de_menus` fica fora do corpo. Chips não decidem composição do corpo.

- Chips podem refletir capacidades declaradas na tela ou na instância de `console`.
- `[✥]` é restrito a elemento `console` navegável. Quando há mais de um elemento
  de corpo, `[✥]` fica inativo se o elemento em foco não for `console` navegável.
- `[␣]` só existe quando a instância de `console` declara formação de seleção múltipla.
- `[⏎]` fica ativo/inativo conforme o item em foco possui ou não ação válida.
- `[⇆]` alterna o foco de interação entre elementos de corpo quando há múltiplos.

As regras completas da `barra_de_menus` pertencem a `contrato_barra_de_menus.md`.
Este contrato não altera `contrato_barra_de_menus.md`.

---

## 7. Regras de uso

**R-1. Declaração exclusiva no `tela.json`.**
Nenhum dos campos de composição do corpo pode ser resolvido, modificado ou
sobrescrito pelo renderer, pela `barra_de_menus`, pelo `estilo.json`, ou por
código hardcoded. O `tela.json` validado é a única fonte de decisão sobre
composição de corpo.

**R-2. Renderer como executor puro.**
O renderer recebe a declaração validada e a executa. Não possui lógica de
seleção de tipo, não possui fallback de tipo, e não toma nenhuma decisão de
composição com base em condições de ambiente.

**R-3. `dashboard` é sempre opcional e sempre ausente por omissão.**
Nenhuma tela tem `dashboard` presente por default. A presença exige elemento
`tipo=dashboard` em `corpo.elementos[]`. A ausência não gera estrutura, espaço
reservado nem objeto vazio no renderer.

**R-4. Separação terminológica entre `lancador` e `barra_de_menus`.**
Os termos não são intercambiáveis em nenhum contexto — código, comentário ou
documentação. `lancador` designa o tipo de elemento do corpo (seção 3);
`barra_de_menus` designa a região fixa da tela (contrato separado).

**R-5. Posicionamento de `dashboard` segue a composição geral do corpo.**
O posicionamento do `dashboard` na composição da tela é controlado pela
estrutura declarativa do `corpo` do `tela.json`, como qualquer outro
elemento funcional (ADR-0010). O campo `posicao_dashboard` como eixo
separado independente está descontinuado; JSONs existentes com este campo
podem ser honrados por compatibilidade em handoff futuro de migração.

**R-6. `tipo_exibicao` só existe para `console`.**
Para elementos `lancador`, não existe `tipo_exibicao`. O layout do `lancador`
é calculado automaticamente pelo renderer — modo `fila` ou `matriz`, a partir
da largura real do terminal (seção 5.2).

**R-7. Indicador de paginação pertence à borda do elemento, não ao layout da tela.**
O renderer posiciona o indicador na última linha da borda do elemento paginado.
Não deve movê-lo para a barra_de_menus, para o dashboard, nem para nenhuma outra
região, independente do arranjo visual.

**R-8. Traço do indicador de paginação é sempre literal.**
O bloco `─ página X/Y ─` usa traço `─` fixo em código, independente do estilo
ativo. Esta é a única exceção ao princípio de que todos os caracteres de borda
vêm do estilo.

**R-9. Composição do corpo aplica-se a todos os elementos funcionais.**
`dashboard`, `console` e `lancador` são elementos funcionais do corpo. A
estrutura declarativa do `corpo` do `tela.json` é a fonte de posicionamento
de todos eles. O renderer não separa `dashboard` dos demais elementos para
aplicar lógica de posicionamento diferenciada não declarada (ADR-0010).

**R-10. Espaçamento interno é universal e não configurável.**
O renderer sempre insere uma linha em branco entre borda e conteúdo em qualquer
elemento do corpo. Esta regra não pode ser suprimida.

**R-11. Draft demonstrativo de dashboard não contamina a tela real.**
Regras históricas do draft de dashboard da demonstração não definem conteúdo
da futura tela inicial real. Pela ADR-0022, o `dashboard` inicial do
Orquestrador real deverá estar estruturalmente presente e sem entradas de dados
reais ou demonstrativos; outras instâncias de `dashboard` seguem suas próprias
declarações.

**R-12. Tiling tem duas camadas de decisão — nenhuma é única.**
O renderer não consulta `tiling` do estilo quando o `tela.json` já declarou
`arranjo` explicitamente. O renderer não inventa arranjo quando nenhuma das
duas fontes o define — essa combinação é proibida: ou o `tela.json` declara ou
o estilo provê.

**R-13. Renderer não hardcoda composição.**
O renderer percorre as listas e objetos declarados no `tela.json`. Nenhuma
composição, lista de itens, tipo de elemento ou regra visual de instância pode
estar hardcoded no código.

**R-14. Filtros atuam antes da paginação.**
Para qualquer instância de `console`, filtros são aplicados antes de calcular a
paginação. O conjunto paginado é sempre o resultado filtrado.

**R-15. `grupo` é nó estrutural, não funcional (ADR-0015).**
`grupo` não tem borda, moldura, título, conteúdo, ação, chip, origem de dados
nem `tela_destino`. Não é navegável por `[✥]`. Qualquer tratamento de `grupo`
como elemento funcional é erro estrutural.

**R-16. Profundidade máxima 3 níveis de grupos (ADR-0015; ADR-0019).**
A profundidade é contada por **níveis de grupos** — nós estruturais do tipo
`grupo`. Grupos com nível 4 ou superior devem ser rejeitados com erro estrutural
determinístico. Elementos funcionais dentro de um grupo do nível 3 **não**
constituem nível 4. O renderer não tenta renderizar estruturas além do nível de
grupo 3.

**R-17. Arranjo por container (ADR-0015; ADR-0018).**
O arranjo de um container (`corpo` ou `grupo`) define o eixo de composição dos
seus filhos diretos: `arranjo = horizontal` organiza os filhos no eixo
horizontal; `arranjo = vertical` organiza os filhos no eixo vertical. O arranjo,
sozinho, não reparte nem aloca a dimensão disponível: sem `distribuicao`, ele
apenas organiza os filhos conforme suas dimensões orientadas pelo conteúdo.
A repartição da dimensão é feita somente pela `distribuicao` explícita — quando
declarada, ela reparte a largura no arranjo horizontal ou a altura no arranjo
vertical. Um container filho pode ter arranjo diferente do container pai.

**R-18. Distribuição aloca área, não apenas conteúdo (ADR-0015).**
O renderer deve preservar a área alocada. Conteúdo menor que a área recebe
preenchimento (espaços ou linhas em branco). O elemento funcional não pode
encolher abaixo da área alocada.

**R-19. Arredondamento por maiores restos (ADR-0015).**
Toda conversão de percentual/fração para células inteiras usa o método dos
maiores restos. A soma das áreas alocadas deve ser exatamente igual à área
disponível do container. Empates são resolvidos pela ordem declarada.

**R-20. Contato entre molduras — sem vão externo (ADR-0015).**
Em layout horizontal, molduras adjacentes ficam coladas. Não existem vãos
externos. Primeira moldura inicia no primeiro caractere útil; última termina
no último caractere útil. A regra anterior de "3 vãos iguais" está supersedida
pela ADR-0015 e não deve ser implementada.

**R-21. `ajustado ao conteúdo` = `preferido` (ADR-0015).**
O conceito `conteudo` (ajustado ao conteúdo renderizado) é tratado como
dimensão preferida — não mínima. Quando combinado com restrição de `maximo`,
o elemento recebe o menor entre preferido e máximo.

**R-22. Sem fallback silencioso de composição (ADR-0015).**
O renderer nunca ajusta silenciosamente arranjo, distribuição ou profundidade
para contornar restrição. Qualquer condição inválida gera erro determinístico
com mensagem descritiva.

**R-23. Redimensionamento não altera composição declarativa (ADR-0017).**
O redimensionamento reativo (por `SIGWINCH`) não modifica `corpo.arranjo`,
`tiling`, presença de elementos, chips ou qualquer outra decisão declarativa de
composição. Somente distribuições visuais já autorizadas e dependentes da dimensão
real podem ser recalculadas.

**R-24. Novo par de dimensões válido aciona recálculo de áreas (ADR-0017).**
Quando a sessão TTY receber novo par válido de largura/altura, o renderer deve
recalcular áreas, paginação e distribuições visuais dependentes, e redesenhar o
quadro completo. Par inválido não é aplicado; as últimas dimensões válidas são
mantidas sem que o redesenho seja acionado.

**R-25. `estrutura` ausente equivale a `livre` (ADR-0020).**
O loader deverá futuramente tratar a ausência de `estrutura` como equivalente
a `estrutura: "livre"`. A ausência nunca ativa o comportamento `matriz`.

**R-26. `estrutura: matriz` requer o objeto `matriz` com `linhas`, `colunas`
e `celulas` (ADR-0020).**
A ausência do objeto `matriz` em um `grupo` com `estrutura: "matriz"` é inválida.
O loader deverá futuramente rejeitar antes de qualquer construção do modelo.

**R-27. Distribuições de linhas e colunas são obrigatórias em `estrutura: matriz`
(ADR-0020).**
O loader deverá futuramente rejeitar qualquer matriz sem
`matriz.linhas.distribuicao` ou sem `matriz.colunas.distribuicao`. Não existe
default implícito para `igual` nem dimensionamento por conteúdo natural.

**R-28. Dimensões válidas: 2 ≤ linhas ≤ 4 e 2 ≤ colunas ≤ 4 (ADR-0020).**
O loader deverá futuramente rejeitar dimensões fora desses limites sem fallback.

**R-29. Cobertura completa obrigatória (ADR-0020).**
O loader deverá futuramente rejeitar matrizes onde a quantidade de células em
`celulas[]` difira de `linhas × colunas`, ou onde algum filho direto não esteja
associado exatamente uma vez.

**R-30. `arranjo` é proibido em `estrutura: matriz` (ADR-0020).**
O loader deverá futuramente rejeitar qualquer `grupo` com `estrutura: "matriz"`
que declare `arranjo`.

**R-31. Rejeição determinística de matriz inválida sem fallback (ADR-0020).**
Nenhuma condição de invalidade da matriz pode resultar em conversão silenciosa
para `livre`. O loader deverá futuramente gerar erro determinístico.

**R-32. Matriz não acrescenta nível de profundidade (ADR-0020; ADR-0019).**
`estrutura: matriz` não cria nível de grupo extra. Linhas, colunas e células
não contam como níveis. Um `grupo` filho dentro de uma célula matricial conta
normalmente como nível de grupo.

---

## 8. Critérios de validação

- [ ] O `tela.json` é validado antes de renderizar; composição ausente ou inválida é erro.
- [ ] Tipos desconhecidos em `corpo.elementos[]` são erro de validação.
- [ ] Elemento sem `id` é erro de validação.
- [ ] `dashboard` não pode ser tratado como elemento navegável por `[✥]`.
- [ ] `lancador` não pode ser tratado como navegável por `[✥]` nem pelas setas
      da `barra_de_menus`.
- [ ] `console` pode ter itens heterogêneos; a lista não precisa ser homogênea.
- [ ] Filtros são aplicados antes da paginação em toda instância de `console`.
- [ ] O renderer não hardcoda composição, arranjo, presença de elemento ou
      posicionamento (R-13).
- [ ] Nenhum renderer possui lógica de escolha de tipo de conteúdo ou fallback de tipo.
- [ ] `lancador` não declara nem processa `tipo_exibicao` — o eixo é inexistente
      para esse tipo (R-6).
- [ ] `dashboard` ausente não gera nenhuma estrutura no layout.
- [ ] O posicionamento de `dashboard` na composição da tela é determinado pela
      estrutura declarativa do `corpo` do `tela.json`, não por campo `posicao_dashboard`
      tratado como eixo separado independente (ADR-0010). O campo `posicao_dashboard`
      legado pode ser honrado por compatibilidade em handoff futuro de migração
      enquanto a migração não ocorrer.
- [ ] O indicador de paginação aparece na última linha da borda do elemento paginado,
      ancorado à direita, nunca em outra região.
- [ ] O bloco `─ página X/Y ─` usa traço `─` literal mesmo quando o estilo ativo
      tem `traco_inferior = " "` — R-8.
- [ ] A composição da linha do indicador obedece a ordem (da direita para a esquerda):
      `canto_inferior_direito` | 1 × `traco_inferior` | bloco literal | preenchimento
      com `traco_inferior`.
- [ ] O preenchimento da posição 4 do indicador encurta quando X/Y tem mais dígitos,
      mantendo a largura total da linha constante.
- [ ] Em arranjo horizontal (`corpo.arranjo = "horizontal"`), cada elemento exibe seu próprio indicador de paginação dentro de sua própria borda.
- [ ] `dashboard` presente não recebe nem desloca o indicador de paginação do elemento
      paginado (R-7).
- [ ] Com `arranjo` declarado no `tela.json`, o renderer usa o arranjo fixo e ignora
      `tiling` do estilo ativo.
- [ ] Com `arranjo` não declarado no `tela.json`, o renderer consulta `tiling` do
      estilo ativo sem modificação, sem fallback automático baseado em largura.
- [ ] Em modo horizontal (`horizontal`, ADR-0011; alias transicional `lado_a_lado`), o espaço horizontal é distribuído por particionamento contíguo entre os filhos diretos do container: molduras adjacentes ficam coladas, sem vão externo entre elas, e a soma das larguras alocadas deve fechar exatamente a largura disponível (ADR-0015, R-20).
- [ ] Regras históricas do draft demonstrativo de dashboard não definem
      conteúdo da futura tela inicial real `orquestrador`; o `dashboard`
      inicial real permanece estruturalmente presente e sem entradas (R-11).
- [ ] `lancador` não pagina; o renderer calcula `distribuicao_lancador` automaticamente.
- [ ] Valores de layout do `console` são lidos de
      `config/layouts/layout_console.json`, não hardcoded;
      `config/layouts/layout_dado.json` é obsoleto/transicional.
- [ ] A linha em branco entre Total e marcadores no draft do Orquestrador é exatamente
      1 — não sujeita à distribuição uniforme e não comprimível.
- [ ] O renderer insere linha em branco entre borda e conteúdo em todo elemento do
      corpo, sem exceção (R-10).
- [ ] `grupo` em `corpo.elementos[]` ou em `grupo.elementos[]` não gera borda,
      moldura, título, conteúdo próprio nem estrutura visual independente (R-15).
- [ ] Estruturas com grupo no nível 4 ou superior são rejeitadas com erro
      estrutural determinístico (R-16); elementos funcionais dentro de grupo do
      nível 3 não constituem nível 4 (ADR-0019, D3).
- [ ] O arranjo declarado por cada container se aplica somente aos seus filhos
      diretos, sem herança obrigatória para containers filhos (R-17).
- [ ] A área alocada pela distribuição é preservada; conteúdo menor recebe
      preenchimento de espaços ou linhas em branco (R-18).
- [ ] `corpo.arranjo = "vertical"` sozinho não dispara repartição proporcional da
      altura nem modo `igual`; a repartição só ocorre com `distribuicao` declarada
      (seção 4.8, ADR-0018).
- [ ] A ausência de `distribuicao` preserva a construção orientada pelo conteúdo
      (dimensão natural + preenchimento externo da ADR-0013) e não equivale ao
      modo `igual` (seção 5.7, ADR-0018).
- [ ] `igual` só reparte área igualmente quando declarado explicitamente; não é
      fallback implícito da ausência (seção 5.7, ADR-0018).
- [ ] Com `distribuicao` explícita, a soma das cotas ocupa toda a área
      distribuível e a cota excedente ao conteúdo vira preenchimento interno da
      moldura do elemento, não sobra acumulada abaixo do último filho
      (seções 4.9 e 5.9, ADR-0018).
- [ ] `fracao`/`percentual` aceitam qualquer vetor válido de valores positivos;
      nenhum vetor concreto é hardcodado (seção 5.7, ADR-0018).
- [ ] `len(distribuicao.valores) == len(elementos)` para o container onde a
      distribuição é declarada, contando somente filhos diretos (seção 4.9).
- [ ] Arredondamento usa método dos maiores restos; soma das áreas alocadas é
      exatamente igual à área disponível do container (R-19).
- [ ] Em layout horizontal, molduras adjacentes ficam coladas; não há vão externo
      entre molduras (R-20).
- [ ] Conceito `conteudo` (dimensão ajustada ao conteúdo) é tratado como `preferido`,
      não como `minimo` (R-21).
- [ ] Condição que impeça composição declarada gera erro determinístico; nunca
      fallback silencioso (R-22).
- [ ] O redimensionamento reativo não altera `corpo.arranjo`, `tiling`, presença
      de elementos nem chips — somente distribuições visuais dependentes de dimensão
      são recalculadas (R-23, ADR-0017).
- [ ] Par inválido de dimensões não é aplicado ao renderer; as últimas dimensões
      válidas são mantidas e não provocam redesenho por si sós (R-24, ADR-0017).
- [ ] Ausência de `estrutura` em `grupo` é tratada como `estrutura: "livre"`;
      nunca ativa `matriz` (R-25, ADR-0020).
- [ ] `estrutura: "matriz"` sem objeto `matriz` é inválido; o loader deverá
      futuramente rejeitar antes da construção do modelo (R-26, ADR-0020).
- [ ] `matriz` sem `linhas.distribuicao` ou sem `colunas.distribuicao` é inválido;
      o loader deverá futuramente rejeitar; não existe default implícito para `igual`
      (R-27, ADR-0020; INV-MAT-DIST-01, INV-MAT-DIST-02, INV-MAT-DIST-03).
- [ ] Dimensão de linhas ou colunas fora do intervalo [2, 4] é inválida; o loader
      deverá futuramente rejeitar sem fallback (R-28, ADR-0020).
- [ ] Quantidade de células em `celulas[]` diferente de `linhas × colunas` é
      inválida; filho direto não associado exatamente uma vez é inválido (R-29,
      ADR-0020).
- [ ] `grupo` com `estrutura: "matriz"` que declare `arranjo` é inválido; o loader
      deverá futuramente rejeitar (R-30, ADR-0020).
- [ ] Coordenada duplicada em `celulas[]` é inválida; elemento duplicado em
      `celulas[]` é inválido; referência a `id` inexistente em `elementos[]` é
      inválida (ADR-0020, D8).
- [ ] Coordenada fora das dimensões declaradas é inválida (ADR-0020, D8).
- [ ] Matriz inválida não pode ser convertida silenciosamente para `livre`; o
      loader deverá futuramente gerar erro determinístico (R-31, ADR-0020).
- [ ] `estrutura: "livre"` explícito: `arranjo` é válido; `distribuicao` é
      opcional; ausência de `distribuicao` segue ADR-0018 (ADR-0020, D4).
- [ ] `estrutura: "matriz"` não cria nível de profundidade extra; linhas, colunas
      e células não contam como nível de grupo (R-32, ADR-0020; ADR-0019, D1).

---

## 9. Pendências

Itens adiados intencionalmente — não são lacunas de especificação:

- **Combinação `arranjo = horizontal` + `dashboard` presente** (`horizontal`,
  ADR-0011; alias transicional `lado_a_lado`): o comportamento do indicador de
  paginação quando `dashboard` participa do arranjo horizontal será tratado em
  handoff futuro. ADR-0010 resolve conceitualmente que `dashboard` segue a
  composição geral; a implementação do indicador de paginação nesse contexto
  aguarda o handoff.
- **Relação entre `filtro_de_grupo` e `formacao_de_selecao`**: coexistência,
  exclusividade ou atalho entre `[#]` (filtrar exibição por grupo) e `[␣]`
  (marcar item para seleção) — não está definida. Ver
  `docs/NOMENCLATURA.md` seção 4.
- **Migração do campo `posicao_dashboard`** (ADR-0010): JSONs existentes com
  `posicao_dashboard` serão migrados/descartados em handoff futuro de migração.
  Até então, o campo pode ser honrado por compatibilidade.
- **Implementação do `grupo` e hierarquia em 3 níveis** (ADR-0015): H-0020
  será responsável por criar/expandir grupos conforme planejamento futuro. A
  hierarquia em 3 níveis ocorrerá em ciclo posterior. Testes específicos de
  verificação dos níveis serão criados depois que H-0019 e a hierarquia em
  3 níveis estiverem implementados.
- **H-0019 bloqueado** (ADR-0015): H-0019 não deve ser implementado na forma
  atual. Deve ser revisado após os contratos serem atualizados. A retomada do
  H-0019 deve citar ADR-0015 como autoridade superior e remover qualquer regra
  conflitante.
- **Schema de sincronização explícita entre grupos** (ADR-0015): o mecanismo
  de `sincronizacao.cortes = "obrigatorio"` tem conceito registrado, mas o
  schema final não foi fechado. Deve ser detalhado em ciclo futuro.
- **Distribuição restrita/dinâmica** (ADR-0015): os conceitos `minimo`,
  `preferido`, `maximo`, `restante`, `conteudo` estão registrados mas não
  têm schema de declaração fechado. Detalhamento em ciclo futuro.
- **Política de terminal pequeno demais** (ADR-0015, ADR-0017): a ADR-0017
  estabelece que terminal com dimensões válidas mas insuficientes deve exibir
  quadro mínimo de aviso e recuperar automaticamente quando dimensões suficientes
  forem restauradas — ver `contrato_tela_json.md` seção 24. A representação
  compacta com `...` para overflow/compactação é política complementar a ser
  detalhada em ciclo futuro.
- **Revisão de `contrato_lancador.md` conforme ADR-0008** (DOC-0020): detalhes
  da instância de `lancador` em `tela.json` pertencem ao contrato próprio.
- **Revisão de `console` como container genérico** (DOC-0024): contrato e
  classes de tipos internos de item de `console` são pendência DOC-B008.

---

## 10. Relação normativa entre ADR-0015 e ADR-0018

A ADR-0015 permanece a autoridade da composição hierárquica do corpo: árvore de
composição, nó `grupo`, arranjo e distribuição por container, associação a filhos
diretos, modos `igual`/`percentual`/`fracao`, arredondamento por maiores restos,
desempate pela ordem declarada e preenchimento de área alocada. Todos esses
pontos continuam vigentes.

A ADR-0018 (2026-07-11) **substitui parcialmente** a ADR-0015 **somente** no ponto
em que a ausência de `distribuicao` era tratada como equivalente ao modo `igual`.
A partir da ADR-0018:

- `arranjo` e `distribuicao` são conceitos distintos: arranjo é ordem de
  composição; distribuição é repartição de área (seção 4.8);
- a ausência de `distribuicao` preserva a construção orientada pelo conteúdo e
  **não** equivale ao modo `igual` (seção 5.7);
- `igual` permanece modo válido apenas quando declarado explicitamente e não é
  fallback implícito da ausência (seção 5.7);
- a distribuição explícita reparte integralmente a altura/largura útil e a sobra
  vira preenchimento interno das molduras dos filhos (seções 4.9 e 5.9);
- `percentual` e `fracao` permanecem genéricos; nenhum vetor concreto pode ser
  hardcodado (seção 5.7);
- conteúdo maior que a cota é lacuna externa à ADR-0018 e não é decidido aqui
  (seção 5.7.1).

A ADR-0015 histórica **não** é reescrita por este contrato; registra-se apenas
que o ponto conflitante foi substituído pela ADR-0018. A ADR-0013 (ocupação
vertical) e a ADR-0017 (redimensionamento reativo) permanecem preservadas: a
altura útil repartida pela distribuição é obtida pelo mecanismo da ADR-0017, e o
preenchimento externo da ADR-0013 é o comportamento aplicável **na ausência** de
distribuição.
