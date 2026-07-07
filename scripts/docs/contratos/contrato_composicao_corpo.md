---
name: contrato-composicao-corpo
description: Schema e regras do módulo de composição de corpo — tipos de elemento declarados em tela.json, regras de console, lancador e dashboard, indicador de paginação e tiling
metadata:
  type: contrato
  scope: scripts
  versao: "0.2"
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
    reaproveitado_de_legado: false
---

# Contrato — Módulo de Composição de Corpo

## 1. Objetivo

Especificar a composição do corpo da tela: a taxonomia fechada dos tipos de
elemento do corpo, os campos declarados no `tela.json`, as regras de layout
para `lancador`, `dashboard` e `console`, a mecânica do indicador de
paginação e as duas camadas de decisão de tiling.

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

O corpo de uma tela pode conter elementos de exatamente três tipos. A lista é
**fechada** — não existe tipo de elemento fora desta taxonomia no sistema atual.
Extensões futuras exigem ADR.

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

| Campo | Valores | Observação |
|---|---|---|
| `arranjo` | `sobreposto` \| `lado_a_lado` \| *(não declarado)* | Relevante com 2+ elementos `console`/`lancador`. Quando não declarado no `tela.json`, o renderer usa o campo `tiling` do estilo ativo como default — ver seção 5.6 |

`estilo.json` não decide composição. `tela.json` é a fonte de arranjo concreto.
Se houver default histórico de artefato transicional, ele deve ser marcado como
transicional/a reavaliar pela ADR-0008.

### 4.3 Posicionamento do `dashboard`

A posição do `dashboard` no corpo é regra de layout da instância declarada no
`tela.json` — não é eixo universal fixo separado por tela.

| Campo | Valores | Observação |
|---|---|---|
| `posicao_dashboard` | `horizontal` \| `vertical` | Declarado na instância do elemento `tipo=dashboard`. `horizontal`: dashboard ao lado do corpo; `vertical`: dashboard abaixo. Eixo próprio — **nunca afetado** por `arranjo` nem por `tiling` |

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

---

## 5. Regras de layout

### 5.1 Organização horizontal por tipo de conteúdo

| Tipo | Modo | Organização |
|---|---|---|
| `lancador` | `fila` ou `matriz` (calculado automaticamente) | Linha única horizontal ou grade de colunas; nunca pagina — ver seção 5.2 |
| `console` | `normal` | Colunar: `n_col` colunas, valor ajustável |
| `console` | `verboso` | Tabular: largura de coluna calculada por conteúdo; texto longo quebra dentro da célula |

**Largura sempre dinâmica**: calculada a partir da largura real do terminal em
tempo real (redimensionamento reativo). Sem perfis fixos pré-definidos.

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

`dashboard` é elemento passivo do corpo declarado no `tela.json`:

- não é navegável por `[✥]`;
- não é obrigatório — sua presença exige elemento `tipo=dashboard` em
  `corpo.elementos[]` no `tela.json`;
- possui moldura própria;
- não possui conteúdo universal fixo;
- não haverá `config/dashboard.json`;
- conteúdo e campos vêm da instância declarada no `tela.json` da tela;
- o renderer não deve hardcodar conteúdo, composição ou campos de nenhuma
  instância de `dashboard`.

A estrutura de 8 campos de resumo + Total + 8 marcadores abaixo é o **draft
da instância de `dashboard` da tela raiz do Orquestrador** — exemplo e instância
conhecida, não regra universal da classe `dashboard`. O antigo `Info` é o draft
dessa instância.

**Alinhamento horizontal**: coluna dimensionada pelo maior rótulo, itens alinhados
à esquerda dentro do bloco. **Pendente de decisão (DOC-B004)**: o posicionamento
do bloco do `dashboard` no espaço horizontal disponível não está fechado. Não
implementar nem assumir comportamento até a decisão ser registrada.

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
- **Layout lado a lado**: cada elemento exibe sua própria paginação, ancorada
  à direita dentro da própria borda, independente do lado da tela.
- **Combinação lado a lado + dashboard presente**: não definida — ver seção 9.

---

### 5.6 Tiling — duas camadas de decisão

Aplica-se exclusivamente ao arranjo de 2+ elementos `console`/`lancador`. Nunca
decide a posição do `dashboard` — esse é o campo `posicao_dashboard` declarado
na instância (seção 4.3).

**Camada 1 — Fixação no `tela.json`**: o `tela.json` pode declarar
explicitamente `arranjo = sobreposto` ou `arranjo = lado_a_lado`. Quando
declarado, o renderer usa esse valor diretamente e **ignora** o campo `tiling`
do estilo ativo para aquela tela.

**Camada 2 — Default do estilo**: quando o `tela.json` não declara `arranjo`,
o renderer consulta o campo `tiling` do estilo ativo (`config/estilo.json`).
Esse valor é escolha manual do usuário; o renderer usa-o diretamente, sem
modificação, sem fallback baseado em largura de terminal.

`estilo.json` não decide composição — provê apenas o default de arranjo quando
o `tela.json` não o declara. O renderer não decide sozinho o arranjo por largura.
O cálculo visual permitido pelo renderer limita-se à distribuição de espaço
dentro da regra declarada.

**Distribuição de espaço em modo lado a lado**: o espaço horizontal disponível
é distribuído em **3 vãos iguais**: borda↔coluna_1, coluna_1↔coluna_2,
coluna_2↔borda.

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

**R-5. `posicao_dashboard` é campo da instância, independente do tiling.**
O campo `posicao_dashboard` (`horizontal`/`vertical`) é declarado na instância
do elemento `tipo=dashboard` e não é afetado pelo valor de `arranjo`, pelo campo
`tiling` do estilo ativo, nem por qualquer condição de ambiente.

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

**R-9. Tiling e arranjo não afetam o `dashboard`.**
O campo `tiling` do estilo e o `arranjo` do `tela.json` regem apenas a
disposição de elementos `console`/`lancador` entre si. A posição do `dashboard`
é determinada exclusivamente por `posicao_dashboard`.

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
- [ ] Com `posicao_dashboard = horizontal`, `dashboard` renderiza ao lado do corpo
      principal; com `posicao_dashboard = vertical`, renderiza abaixo — independente
      de `arranjo` ou `tiling`.
- [ ] O indicador de paginação aparece na última linha da borda do elemento paginado,
      ancorado à direita, nunca em outra região.
- [ ] O bloco `─ página X/Y ─` usa traço `─` literal mesmo quando o estilo ativo
      tem `traco_inferior = " "` — R-8.
- [ ] A composição da linha do indicador obedece a ordem (da direita para a esquerda):
      `canto_inferior_direito` | 1 × `traco_inferior` | bloco literal | preenchimento
      com `traco_inferior`.
- [ ] O preenchimento da posição 4 do indicador encurta quando X/Y tem mais dígitos,
      mantendo a largura total da linha constante.
- [ ] Em layout lado a lado, cada elemento exibe seu próprio indicador de paginação
      dentro de sua própria borda.
- [ ] `dashboard` presente não recebe nem desloca o indicador de paginação do elemento
      paginado (R-7).
- [ ] Com `arranjo` declarado no `tela.json`, o renderer usa o arranjo fixo e ignora
      `tiling` do estilo ativo.
- [ ] Com `arranjo` não declarado no `tela.json`, o renderer consulta `tiling` do
      estilo ativo sem modificação, sem fallback automático baseado em largura.
- [ ] Em modo lado a lado, o espaço horizontal é dividido em 3 vãos iguais
      (borda↔col_1, col_1↔col_2, col_2↔borda).
- [ ] Campo do draft de dashboard do Orquestrador exibe valor numérico — nunca `—`,
      nunca vazio; `0` é exibido normalmente (R-11).
- [ ] `lancador` não pagina; o renderer calcula `distribuicao_lancador` automaticamente.
- [ ] Valores de layout do `console` são lidos de `config/layout_console.json`, não
      hardcoded; `config/layout_dado.json` é obsoleto/transicional.
- [ ] A linha em branco entre Total e marcadores no draft do Orquestrador é exatamente
      1 — não sujeita à distribuição uniforme e não comprimível.
- [ ] O renderer insere linha em branco entre borda e conteúdo em todo elemento do
      corpo, sem exceção (R-10).

---

## 9. Pendências

Itens adiados intencionalmente — não são lacunas de especificação:

- **Combinação `arranjo = lado_a_lado` + `dashboard` presente ao mesmo tempo**:
  comportamento do indicador de paginação e posicionamento do `dashboard` quando
  ambas as condições estão ativas simultaneamente. Sem caso de uso real até o
  momento — não especificar nem implementar até surgir caso concreto.
- **Relação entre `filtro_de_grupo` e `formacao_de_selecao`**: coexistência,
  exclusividade ou atalho entre `[#]` (filtrar exibição por grupo) e `[␣]`
  (marcar item para seleção) — não está definida. Ver
  `docs/NOMENCLATURA.md` seção 4.
- **Posicionamento horizontal do bloco de `dashboard`** (DOC-B004): se acompanha
  a regra do `lancador` (bloco à esquerda com sobra à direita, ADR-0002) ou
  mantém centralização. Não implementar nem assumir comportamento até a decisão
  ser registrada; ver `docs/NOMENCLATURA.md` seção 11.
- **Revisão de `contrato_lancador.md` conforme ADR-0008** (DOC-0020): detalhes
  da instância de `lancador` em `tela.json` pertencem ao contrato próprio.
- **Revisão de `console` como container genérico** (DOC-0024): contrato e
  classes de tipos internos de item de `console` são pendência DOC-B008.
