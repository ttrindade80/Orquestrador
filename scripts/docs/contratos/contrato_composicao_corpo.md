---
name: contrato-composicao-corpo
description: Schema e regras do módulo de composição de corpo — tipos de objeto, eixos declarados por classe de tela, layout de menu e Info, indicador de paginação e tiling
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#3-composicao-de-corpo, #6-layout-e-largura, #8-corpo-tipo-menu, #9-objeto-info, #10-tiling"
    reaproveitado_de_legado: false
---

# Contrato — Módulo de Composição de Corpo

## 1. Objetivo

Especificar a composição do corpo da tela: a taxonomia fechada dos tipos de
objeto do corpo, os eixos que a classe de tela declara, as regras de layout
para corpo tipo `menu` e para o objeto `Info`, a mecânica do indicador de
paginação, e as duas camadas de decisão de tiling.

Este contrato cobre as seções 2, 3, 6, 6.1, 8, 9 e 10 de
`docs/NOMENCLATURA.md`. Estilo universal (`contrato_estilo.md`, `ativo`),
barra_de_menus (contrato ainda não escrito) e mecanismos de seleção (contrato
ainda não escrito) são módulos separados. Este contrato pode referenciar esses
módulos como dependências externas, mas não redefine nem duplica suas regras.

---

## 2. Regra fundamental (formal, não observação)

**Toda propriedade de composição do corpo — tipo de conteúdo, tipo de
exibição, presença e posição do Info, quantidade de corpos, arranjo de
múltiplos corpos, paginação e colunas ajustável — é declarada pela classe de
tela, nunca decidida pelo renderer, pela barra_de_menus, ou pelo objeto de
estilo.**

O renderer recebe a composição já resolvida pela classe e a executa sem
deliberação própria. O renderer não possui lógica de seleção de tipo, não
possui fallback de tipo, e não toma nenhuma decisão de composição com base em
condições de ambiente (largura de terminal, conteúdo dos dados, etc.).

Esta regra deriva da abertura da seção 3 de `docs/NOMENCLATURA.md`.

---

## 3. Taxonomia de tipos de objeto do corpo

O corpo de uma tela pode conter objetos de exatamente três tipos. A lista é
**fechada** — não existe tipo de objeto fora desta taxonomia no sistema atual.
(Extensibilidade futura segue o schema aberto de `NOMENCLATURA.md` seção 2.1
sem reescrita do renderer, desde que a amarração declarativa seja mantida.)

| Tipo | Função | Presença |
|---|---|---|
| `dado` | Dados propriamente ditos, incluindo saída de script/log | Um ou mais por tela |
| `menu` | Composição de navegação no próprio corpo da tela | Um ou mais por tela |
| `Info` | Resumo/legenda dos dados exibidos | Zero ou um por tela — sempre opcional |

**Distinção obrigatória**: `menu` (tipo de objeto do corpo) e `barra_de_menus`
(região fixa da tela, contrato separado) são entidades distintas. Nenhum
código, documentação ou nomenclatura pode usar os dois termos como sinônimos
ou de forma intercambiável.

---

## 4. Eixos de composição (declarados pela classe de tela)

A classe de tela declara os valores dos eixos abaixo. O renderer lê esses
valores e os executa sem alteração.

| Eixo | Valores | Observação |
|---|---|---|
| `tipo_conteudo` | `menu` \| `dado` | Tipo do(s) corpo(s) principal(is) da tela |
| `tipo_exibicao` | `normal` \| `verboso` | Aplica-se **apenas** a corpos tipo `dado` — ver seção 5.1. Não existe para `menu` |
| `info` | `presente` \| `ausente` | Info é sempre opcional; ausência de declaração equivale a `ausente` |
| `quantidade_corpos` | `1` \| `multiplos` | — |
| `arranjo` | `sobreposto` \| `lado_a_lado` \| *(não declarado)* | Relevante apenas se `quantidade_corpos = multiplos`. Quando não declarado pela classe, o renderer usa o campo `tiling` do estilo ativo como default — ver seção 5.5 |
| `posicao_info` | `horizontal` \| `vertical` | Relevante apenas se `info = presente`. `horizontal`: Info ao lado do corpo; `vertical`: Info abaixo do corpo. Eixo próprio — **nunca afetado** por `arranjo` nem por `tiling` |
| `paginacao` | `com` \| `sem` | — |
| `colunas_ajustavel` | `com` \| `sem` | Eixo próprio, distinto de `paginacao` |

**Espaçamento interno (universal — não é eixo declarado pela classe):** o
renderer sempre insere uma linha em branco entre a borda e o conteúdo, em
qualquer corpo, sem exceção e sem possibilidade de supressão.

---

## 5. Regras de layout

### 5.1 Organização horizontal por tipo de conteúdo

| Tipo | Modo | Organização |
|---|---|---|
| `menu` | único (sem `tipo_exibicao`) | Lista vertical numerada, sem colunas, sem paginação |
| `dado` | `normal` | Colunar: `n_col` colunas, valor ajustável |
| `dado` | `verboso` | Tabular: largura de coluna calculada por conteúdo; texto longo quebra dentro da célula |

**Largura sempre dinâmica**: calculada a partir da largura real do terminal em
tempo real (redimensionamento reativo). O sistema reage a mudança de tamanho
enquanto a tela está aberta — a largura não é lida uma vez na inicialização.
Sem perfis fixos pré-definidos.

**Overflow**: nunca existe scroll. Conteúdo que excede o espaço disponível
sempre pagina. Espaço sobrando é preenchido (padding), nunca deixado vazio
de forma desorganizada.

---

### 5.2 Layout de corpo tipo `menu`

**Alinhamento horizontal:**

1. Calcular a largura do maior item, medida de `[` até o último caractere do
   texto do item.
2. Essa largura define o tamanho da coluna.
3. O bloco inteiro (a coluna) é centralizado no espaço horizontal disponível
   — o espaço sobrando se distribui igualmente dos dois lados do bloco.
4. Dentro do bloco, todos os itens ficam alinhados à esquerda entre si (todos
   os `[` na mesma posição horizontal).
5. Distância fixa de **2 espaços** entre o chip (`[X]`) e o texto do item.

**Alinhamento vertical:**

- Distribuição uniforme entre os itens.
- Nunca mais que 2 linhas em branco entre um item e o próximo.
- O espaço restante (após aplicar o limite acima) é distribuído entre topo e
  base do bloco.

---

### 5.3 Layout do objeto `Info`

O objeto `Info` tem a seguinte estrutura interna, em **ordem obrigatória**:

1. Lista de pares rótulo/valor (campos do resumo principal).
2. Linha separadora.
3. Linha de Total.
4. Exatamente **1 linha em branco** (obrigatória — não sujeita à distribuição
   uniforme geral).
5. Lista de marcadores: símbolo + rótulo + valor.

**Campos do resumo principal** (8 campos, conjunto fechado): Adicionados,
Fichados, Consolidados, Qualificados, Orfão, Missing, Secundários, Descartados.

**Marcadores** (8, conjunto fechado):

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

**Formato do valor numérico**: número puro, sem zero à esquerda, alinhado à
direita dentro do campo (ex.: `50`, não `050`). Não há padding de dígitos.
Todo campo sempre exibe um número — nunca existe estado de travessão (`—`) ou
"sem dado"; `0` é exibido normalmente.

*Distinção de escopo*: esta regra (número puro, sem padding, alinhado à
direita) é exclusiva dos valores do objeto `Info`. Não se confunde com a
restrição de exatamente 1 caractere fixo dos símbolos de borda, chip e
indicadores de estilo, definida em `contrato_estilo.md` (R-6) — que rege
caracteres de apresentação, não valores de dados.

**Alinhamento horizontal**: mesma mecânica do corpo tipo `menu` (seção 5.2) —
coluna dimensionada pelo maior rótulo, bloco centralizado no espaço disponível,
itens alinhados à esquerda dentro do bloco.

**Alinhamento vertical**: mesma mecânica do corpo tipo `menu` (seção 5.2), com
a exceção obrigatória já declarada acima: a linha em branco entre Total e
início da lista de marcadores é sempre exatamente 1 e não está sujeita à
distribuição uniforme geral.

---

### 5.4 Indicador de paginação (quando `paginacao = com`)

O indicador de página é renderizado na **última linha da borda do próprio
corpo paginado**, ancorado à direita. Pertence à borda do corpo — não ao
layout geral da tela, não à barra_de_menus, não ao objeto Info.

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

- **Info presente**: o indicador permanece na borda do corpo paginado. O
  objeto Info não herda, não desloca, e não recebe o indicador — mesmo
  estando fisicamente mais próximo da barra_de_menus do que o corpo paginado.
- **Layout lado a lado**: cada corpo exibe sua própria paginação, ancorada
  à direita dentro da própria borda, independente do lado da tela que aquele
  corpo ocupa fisicamente.
- **Combinação lado a lado + Info presente**: não definida — ver seção 7.

---

### 5.5 Tiling — duas camadas de decisão

Aplica-se exclusivamente ao arranjo de 2+ corpos tipo `dado`/`menu`. Nunca
decide a posição do objeto `Info` — esse é o eixo `posicao_info` (seção 4),
declarado independentemente pela classe.

**Camada 1 — Fixação pela classe**: a classe de tela pode declarar
explicitamente `arranjo = sobreposto` ou `arranjo = lado_a_lado`. Quando
declarado, o renderer usa esse valor diretamente e **ignora** o campo `tiling`
do estilo ativo para aquela tela.

**Camada 2 — Default do estilo**: quando a classe não declara `arranjo`, o
renderer consulta o campo `tiling` do estilo ativo (definido em
`contrato_estilo.md`). Esse valor é escolha manual do usuário; o renderer usa-o
diretamente, sem modificação, sem fallback baseado em largura de terminal.

**Distribuição de espaço em modo lado a lado**: o espaço horizontal disponível
é distribuído em **3 vãos iguais**: borda↔coluna_1, coluna_1↔coluna_2,
coluna_2↔borda.

---

## 6. Regras de uso

**R-1. Declaração exclusiva pela classe.**
Nenhum dos eixos listados na seção 4 pode ser resolvido, modificado ou
sobrescrito pelo renderer, pela barra_de_menus, ou pelo objeto de estilo. A
classe de tela é a única fonte de decisão sobre composição de corpo.

**R-2. Renderer como executor puro.**
O renderer recebe a composição já resolvida e a executa. Não possui lógica
de seleção de tipo, não possui fallback de tipo, e não toma nenhuma decisão
de composição com base em condições de ambiente.

**R-3. Info é sempre opcional e sempre ausente por omissão.**
Nenhuma tela tem `Info` presente por default. A presença deve ser declaração
explícita da classe. A ausência de declaração equivale a `info = ausente`;
o renderer não reserva espaço nem cria estrutura para Info ausente.

**R-4. Separação terminológica entre `menu` e `barra_de_menus`.**
Os termos não são intercambiáveis em nenhum contexto — código, comentário ou
documentação. `menu` designa o tipo de objeto do corpo (seção 3); `barra_de_menus`
designa a região fixa da tela (contrato separado).

**R-5. `posicao_info` é eixo independente.**
O eixo `posicao_info` (`horizontal`/`vertical`) é declarado pela classe e não
é afetado pelo valor de `arranjo`, pelo campo `tiling` do estilo ativo, nem
por qualquer outra condição de ambiente ou estrutura da tela.

**R-6. `tipo_exibicao` só existe para corpo tipo `dado`.**
Para corpos tipo `menu`, não existe o eixo `tipo_exibicao` — há um único modo
de layout (seção 5.1). A classe não deve declarar `tipo_exibicao` para corpos
tipo `menu`.

**R-7. Indicador de paginação pertence à borda do corpo, não ao layout da tela.**
O renderer posiciona o indicador na última linha da borda do corpo paginado.
Não deve movê-lo para a barra_de_menus, para o Info, nem para nenhuma outra
região, independente do arranjo visual.

**R-8. Traço do indicador de paginação é sempre literal.**
O bloco `─ página X/Y ─` usa traço `─` fixo em código, independente do estilo
ativo. Esta é a única exceção ao princípio de que todos os caracteres de borda
vêm do estilo — e ela existe especificamente e apenas no indicador de paginação.

**R-9. Tiling e arranjo não afetam o Info.**
O campo `tiling` do estilo e o eixo `arranjo` da classe regem apenas a
disposição de corpos tipo `dado`/`menu` entre si. A posição do objeto `Info`
é determinada exclusivamente pelo eixo `posicao_info` declarado pela classe.

**R-10. Espaçamento interno é universal e não configurável.**
O renderer sempre insere uma linha em branco entre borda e conteúdo em qualquer
corpo. Esta regra não pode ser suprimida pela classe de tela, pelo objeto de
estilo, nem pelo tipo de conteúdo.

**R-11. Valores do Info são sempre numéricos, nunca ausentes.**
Nenhum campo de resumo principal ou marcador do objeto `Info` exibe estado de
"sem dado", travessão (`—`), ou campo vazio. O valor `0` é exibido normalmente.

**R-12. Tiling tem duas camadas de decisão — nenhuma é única.**
O renderer não consulta `tiling` do estilo quando a classe já declarou `arranjo`
explicitamente. O renderer não inventa um arranjo quando nenhuma das duas fontes
define um — essa combinação é proibida: ou a classe declara ou o estilo provê.

---

## 7. Critérios de validação

- [ ] Nenhum renderer possui lógica de escolha de tipo de conteúdo, tipo de
      exibição, presença de Info ou posição de Info — todos esses valores são
      lidos exclusivamente da declaração da classe.
- [ ] Corpo tipo `menu` não declara nem processa `tipo_exibicao` — o eixo é
      inexistente para esse tipo (R-6).
- [ ] Info ausente não gera nenhuma estrutura no layout (sem espaço reservado,
      sem objeto vazio).
- [ ] Com `posicao_info = horizontal`, Info renderiza ao lado do corpo principal;
      com `posicao_info = vertical`, renderiza abaixo — independente do valor de
      `arranjo` ou `tiling`.
- [ ] O indicador de paginação aparece na última linha da borda do corpo
      paginado, ancorado à direita, nunca em outra região da tela.
- [ ] O bloco `─ página X/Y ─` usa traço `─` literal mesmo quando o estilo
      ativo tem `traco_inferior = " "` (estilo `aberta`) — R-8.
- [ ] A composição da linha do indicador obedece a ordem (da direita para a
      esquerda): `canto_inferior_direito` | 1 × `traco_inferior` | bloco literal
      | preenchimento com `traco_inferior`.
- [ ] O preenchimento da posição 4 do indicador encurta quando X/Y tem mais
      dígitos, mantendo a largura total da linha constante.
- [ ] Em layout lado a lado, cada corpo exibe seu próprio indicador de paginação
      dentro de sua própria borda.
- [ ] Info presente não recebe nem desloca o indicador de paginação do corpo
      paginado — R-7.
- [ ] Com `quantidade_corpos = multiplos` e `arranjo` declarado pela classe, o
      renderer usa o arranjo fixo e ignora `tiling` do estilo ativo.
- [ ] Com `quantidade_corpos = multiplos` e `arranjo` não declarado pela classe,
      o renderer consulta `tiling` do estilo ativo sem modificação, sem fallback
      automático baseado em largura de terminal.
- [ ] Em modo lado a lado, o espaço horizontal é dividido em 3 vãos iguais
      (borda↔col_1, col_1↔col_2, col_2↔borda).
- [ ] Todo campo do resumo principal e todo marcador do Info exibe valor numérico
      — nunca `—`, nunca vazio; `0` é exibido normalmente (R-11).
- [ ] O bloco do menu (corpo tipo `menu`) está centralizado horizontalmente no
      espaço disponível; dentro do bloco, todos os `[` estão na mesma coluna.
- [ ] A distância entre chip e texto de item de menu é exatamente 2 espaços.
- [ ] A distribuição vertical de menu e Info respeita o limite de 2 linhas em
      branco entre itens consecutivos.
- [ ] A linha em branco entre Total e lista de marcadores no Info é exatamente
      1 — não sujeita à distribuição uniforme e não comprimível.
- [ ] O renderer insere linha em branco entre borda e conteúdo em todo corpo,
      sem exceção (R-10).

---

## 8. Pendências

Itens adiados intencionalmente — não são lacunas de especificação, são
decisões conscientes de adiar até surgir caso de uso real (conforme
`docs/NOMENCLATURA.md` seções 6.1, 10 e 11):

- **Combinação `arranjo = lado_a_lado` + `info = presente` ao mesmo tempo**:
  comportamento do indicador de paginação e posicionamento do objeto Info
  quando ambas as condições estão ativas simultaneamente. Sem caso de uso
  real até o momento — não especificar nem implementar até surgir caso
  concreto.
