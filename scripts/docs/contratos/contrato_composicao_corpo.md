---
name: contrato-composicao-corpo
description: Schema e regras do módulo de composição de corpo — tipos de elemento declarados em tela.json, regras de console, lancador e dashboard, indicador de paginação e tiling
metadata:
  type: contrato
  scope: scripts
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
| `dashboard` | Saída passiva formatada, resumo/legenda ou visão consolidada; elemento passivo não navegável | Zero ou um por tela — sempre opcional |

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

### 3.2 Nó estrutural `grupo` (ADR-0015)

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
- pode conter filhos funcionais (`console`, `lancador`, `dashboard`) e, em
  ciclo futuro, grupos aninhados.

**Nível** é o conjunto de filhos diretos de um mesmo container:
- `corpo.elementos[]` é o nível 1;
- `grupo.elementos[]` cria o próximo nível;
- cada grupo aninhado cria um novo nível;
- profundidade máxima: **3 níveis**;
- nível 4 ou superior gera erro estrutural determinístico.

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

### 4.9 Distribuição por container (ADR-0015)

A distribuição pertence ao mesmo container que declara o arranjo.

- container horizontal: distribuição reparte colunas/largura;
- container vertical: distribuição reparte linhas/altura;
- distribuição aloca área, não apenas conteúdo;
- elemento funcional deve preservar a área alocada;
- sobra horizontal vira padding/espaços em branco;
- sobra vertical vira linhas em branco.

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
configuração de colunas e navegação são lidos de `config/layout_console.json`,
não hardcoded — artefato ativo transicional a reavaliar conforme ADR-0008.
O `lancador` lê seus próprios parâmetros em `config/lancador.json`, conforme
`contrato_lancador.md` — também ativo transicional a reavaliar conforme ADR-0008.
`config/layout_dado.json` permanece apenas como artefato obsoleto/transicional
de rastreabilidade da migração `dado` → `console`.

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
concretos de `config/lancador.json`; este contrato não as duplica.
`contrato_lancador.md` será revisado conforme ADR-0008 em tarefa posterior (DOC-0020).

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

### 5.7 Modos de distribuição (ADR-0015)

#### Modo `igual`

Divide a área disponível igualmente entre filhos diretos.

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

Exemplos:
- `[1, 1, 1]` significa `1/3`, `1/3`, `1/3`.
- `[2, 1, 2]` significa `2/5`, `1/5`, `2/5`, equivalente a 40%, 20%, 40%.

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

**R-11. Valores do draft de dashboard do Orquestrador são sempre numéricos.**
Nenhum campo do draft exibe travessão (`—`), campo vazio ou "sem dado". O valor
`0` é exibido normalmente. Esta regra aplica-se ao draft da instância do
Orquestrador; outras instâncias de `dashboard` seguem suas próprias declarações.

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

**R-16. Profundidade máxima 3 (ADR-0015).**
Estruturas com nível 4 ou superior devem ser rejeitadas com erro estrutural
determinístico. O renderer não tenta renderizar estruturas além do nível 3.

**R-17. Arranjo por container (ADR-0015).**
O arranjo de um container (`corpo` ou `grupo`) declara o eixo de distribuição
dos seus filhos diretos. Um container filho pode ter arranjo diferente do
container pai.

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
- [ ] Campo do draft de dashboard do Orquestrador exibe valor numérico — nunca `—`,
      nunca vazio; `0` é exibido normalmente (R-11).
- [ ] `lancador` não pagina; o renderer calcula `distribuicao_lancador` automaticamente.
- [ ] Valores de layout do `console` são lidos de `config/layout_console.json`, não
      hardcoded; `config/layout_dado.json` é obsoleto/transicional.
- [ ] A linha em branco entre Total e marcadores no draft do Orquestrador é exatamente
      1 — não sujeita à distribuição uniforme e não comprimível.
- [ ] O renderer insere linha em branco entre borda e conteúdo em todo elemento do
      corpo, sem exceção (R-10).
- [ ] `grupo` em `corpo.elementos[]` ou em `grupo.elementos[]` não gera borda,
      moldura, título, conteúdo próprio nem estrutura visual independente (R-15).
- [ ] Estruturas com profundidade superior a 3 níveis são rejeitadas com erro
      estrutural determinístico (R-16).
- [ ] O arranjo declarado por cada container se aplica somente aos seus filhos
      diretos, sem herança obrigatória para containers filhos (R-17).
- [ ] A área alocada pela distribuição é preservada; conteúdo menor recebe
      preenchimento de espaços ou linhas em branco (R-18).
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
