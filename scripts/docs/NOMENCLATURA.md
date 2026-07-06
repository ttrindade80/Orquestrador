---
name: nomenclatura-sistema-novo
description: Glossario consolidado de termos do sistema novo, base para os contratos de estilo, composicao de corpo e barra_de_menus
metadata:
  type: nomenclatura
  scope: sistema_novo
  status: parcial
  origem_especificacao: usuario_sessao_2026-07-05
  atualizado_em: 2026-07-05
  reaproveitado_de_legado: false
---

# Nomenclatura — Sistema Novo

## Regra

Este documento e a unica fonte de nomes validos para os contratos que serao
escritos a partir dele. Nenhum contrato pode introduzir sinonimo ou renomear
termo aqui definido sem atualizar este glossario primeiro.

Nenhum termo aqui foi herdado do sistema antigo por leitura direta de codigo
ou documentacao antiga; toda definicao veio de decisao explicita do usuario
nesta sessao de trabalho. Onde o Codex extraiu fatos do sistema antigo (ver
seção 11), isso está marcado explicitamente como levantamento neutro, não
como origem da decisão — a decisão em si continua vindo do usuário.

## 0. Política — NOMENCLATURA.md vs arquivos JSON de dados (decidida nesta sessão)

Cada domínio de renderização (`estilo`, corpo tipo `menu`, corpo tipo `dado`,
`Info`, `barra_de_menus`, e possivelmente `cabecalho`) tem exatamente **dois**
artefatos, com responsabilidades separadas e não sobrepostas:

| Artefato | Responsabilidade |
|---|---|
| `docs/NOMENCLATURA.md` (este documento) | **Schema e semântica**: quais campos existem, o que cada um significa, tipo, restrições, e como o renderer deve interpretá-los. Não guarda valor concreto de produção. |
| `<dominio>.json` (arquivo próprio por domínio) | **Dados concretos**: os valores reais que o renderer lê e aplica. Serve também como gabarito de teste — uma implementação pode ser validada campo a campo contra esse arquivo. |

Isso substitui a prática usada para `estilo` (seção 1), onde os valores de
preset (bordas, chips, indicadores) foram embutidos diretamente nas tabelas
deste documento — inconsistência corrigida quando `estilo.json` foi gerado
(DOC-0005).

**Nomenclatura de arquivo**: nunca usar abreviação que misture dois termos
já distinguidos neste glossário (ex.: nunca `barra_menu.json` — usar
`barra_de_menus.json`; nunca `menu.json` sozinho se puder ser confundido com
`barra_de_menus` — usar `layout_menu.json`, já em uso).

**Localização**: todos os JSON de configuração ficam em `config/`, dentro de
`scripts/`, irmã de `docs/` — nunca dentro de `docs/` (que é documentação
neutra, sem dado de produção, ver `docs/INDICE.md`).

**Status de migração por domínio:**

| Domínio | JSON | Status |
|---|---|---|
| Estilo | `config/estilo.json` | feito (seção 1) |
| Corpo tipo `menu` | `config/layout_menu.json` | feito (seção 8.4) |
| Corpo tipo `dado` | `config/layout_dado.json` | feito (seção 4) |
| `Info` | *(a definir)* | não iniciado — vai ser tratado em outro chat |
| `barra_de_menus` | `config/barra_de_menus.json` | feito (seção 5.1) |
| Cabeçalho | *(avaliar se compensa)* | não decidido — cabeçalho é simples (posição de título, caixa de texto, alinhamento do texto de descrição: centralizado/justificado/esquerda, uma ou duas linhas); pode não justificar arquivo próprio |

---

## 1. Estilo (universal)

Aparencia. Nunca varia por tela ou classe. Nenhuma classe ou renderer pode
hardcodar simbolo, cor ou caractere que pertenca a esta secao — tudo vem do
schema de estilo.

### 1.1 Borda

| Campo | Funcao |
|---|---|
| `traco_superior` | caractere da linha superior |
| `traco_inferior` | caractere da linha inferior |
| `canto_superior_esquerdo` | canto superior esquerdo |
| `canto_superior_direito` | canto superior direito |
| `canto_inferior_esquerdo` | canto inferior esquerdo |
| `canto_inferior_direito` | canto inferior direito |
| `lateral` | caractere da coluna esquerda/direita |

O espaco da moldura sempre existe estruturalmente; o que muda entre estilos
de borda e so o caractere de preenchimento.

### 1.2 Chip

| Campo | Funcao |
|---|---|
| `caractere_esquerdo` | caractere de abertura do chip |
| `caractere_direito` | caractere de fechamento do chip |
| `cor_texto` | cor do texto/tecla do chip |
| `caixa_alta` | booleano — texto em maiuscula ou nao |
| `cor_fundo` | cor de fundo do chip |

### 1.3 Indicadores

| Indicador | Natureza | Simbolos (default) |
|---|---|---|
| `concluido` | par on/off | on: `✓`, off: configuravel (default espaco) |
| `selecionado` | simbolo unico, so aparece quando aplicavel | `→` |
| `incluido` | par on/off | on: `●`, off: `○` |

Todos os simbolos acima sao default configuravel via schema, nunca fixos em
codigo.

**Presets nomeados de `selecionado` e `incluido`**: não existe um único
símbolo fixo — existem conjuntos nomeados, e a implementação é testada
contra a capacidade de trocar entre eles via schema. `selecionado` tem 4
presets ("Seta" é o default); `incluido` tem 4 presets ("Círculo" é o
default). Valores concretos em `config/estilo.json`, seção `indicadores`.

**Símbolo estático de `incluido` sem seleção real** (ver seção 4.2): quando
o item não tem seleção formável, `tg` mostra um símbolo fixo (não
alternante) em vez do par on/off — esse símbolo também é configurável via
schema; nenhum valor concreto foi decidido até o momento.

### 1.4 Preferência de tiling (default)

Campo `tiling`, valores possíveis: `sobreposto` | `lado_a_lado`.

Escolha manual do usuário, não decisão automática por largura de
terminal. Não existe largura mínima de segurança que force sobreposto —
a preferência do usuário sempre vale quando aplicada.

**Escopo**: aplica-se apenas a arranjo de 2+ corpos tipo `dado`/`menu`.
Nunca decide posição do objeto `Info` (esse é eixo próprio, ver seção 3).

**É default, não obrigatório**: a classe de tela pode fixar seu próprio
arranjo (seção 3, "Arranjo de múltiplos corpos") e ignorar a preferência
global do usuário para aquela tela especificamente. `tiling` só é
consultado quando a classe não especifica um arranjo fixo.

Campo já incluído em `contrato_estilo.md` (`ativo`).

### 1.5 Estados dinâmicos de elemento (ADR-0004 — incluído em `contrato_estilo.md`)

Dois campos genéricos novos, decididos nesta sessão, aplicáveis a qualquer
chip ou indicador do sistema — não específicos de um chip só:

| Campo | Função |
|---|---|
| `cor_inativo` | cor aplicada quando um elemento existe mas está temporariamente inativo (apagada/dessaturada) |
| `cor_alerta` | cor aplicada quando um valor atinge um limite (ex.: mínimo/máximo) |

Distinção de conceito importante, usada em toda a seção 5 (barra_de_menus):

- **Existência** de um chip = propriedade estática, declarada pela classe
  de tela (seção 3). Ex.: a classe declara `paginacao: com` → o chip
  `[<][>]` existe nessa tela.
- **Ativo/inativo** = estado dinâmico, recalculado a cada render, a partir
  do conteúdo atual. Ex.: `[<][>]` existe (paginação declarada), mas fica
  **inativo** (usa `cor_inativo`) quando há só 1 página no momento.

Esses dois campos foram incluídos em `contrato_estilo.md` via ADR-0004
(2026-07-05). Nenhum valor concreto de cor foi decidido — vivem apenas como
nomes semânticos no schema; quando decididos, entrarão em `config/estilo.json`.

---

## 2. Tela (estrutura base)

Toda tela do sistema tem exatamente estas tres regioes:

1. **Cabecalho**: titulo + descricao.
2. **Corpo**: estrutura variavel — pode ter mais de um objeto, sobrepostos
   ou lado a lado, dependendo do tamanho da tela e do tipo dos objetos.
   Cada objeto do corpo tem titulo e conteudo.
3. **barra_de_menus**: titulo fixo "Menu", contem os chips de acao (ver
   secao 5). Antes chamada de "menu" nesta conversa — esse nome esta
   descontinuado, o termo correto e `barra_de_menus`.

### 2.1 Tipos de objeto do corpo

- **dado**: dados propriamente ditos, incluindo saida de script/log.
- **menu**: um objeto do corpo que e, ele proprio, uma composicao de
  navegacao (nao confundir com `barra_de_menus`, que e a regiao fixa da
  tela).
- **Info**: objeto opcional do corpo — resumo/legenda dos dados exibidos.

Extensibilidade: um novo tipo de conteudo pode ser adicionado no futuro
seguindo o mesmo principio do estilo — schema aberto, sem exigir reescrita
do renderer, desde que a amarracao declarativa (classe declara, renderer so
executa) seja respeitada.

---

## 3. Composicao de corpo (por classe de tela)

Declarada pela classe de tela, nunca decidida pelo renderer ou pela
barra_de_menus.

| Eixo | Valores |
|---|---|
| Tipo de conteudo | `menu`, `dado` |
| Tipo de exibicao | `normal` (lista simples) / `verboso` (detalhes) — depende dos dados |
| Info | presente / ausente |
| Quantidade de corpos | 1 corpo / múltiplos corpos |
| Arranjo de múltiplos corpos (opcional) | `sobreposto` / `lado_a_lado` — a classe PODE fixar isso; se não fixar, usa o `tiling` global do estilo (seção 1.4) como default |
| Posição do Info | `horizontal` (lado) / `vertical` (inferior) — declarada por classe, sempre. Eixo próprio, **não** afetado pelo `tiling` do estilo — tiling só rege corpos tipo dado/menu, nunca a posição do Info |
| Paginacao | com / sem |
| Colunas ajustavel (tipo `dado`) | com / sem — eixo proprio, distinto de paginacao. Aplica-se apenas a corpos tipo `dado`, ajustável manualmente via chip `[-][+]` |
| `filtro_de_grupo` | `com` / `sem` — eixo próprio; condiciona a existência estrutural do chip `[#]`; não decide ainda a relação entre filtro de grupo e seleção |
| `formacao_de_selecao` | `com` / `sem` — eixo próprio; condiciona a existência estrutural do chip `[␣]` e participa da semântica do rótulo dinâmico de `[⏎]` |
| Espacamento interno | universal (renderer): linha em branco entre borda e conteudo, sempre |
| Organizacao horizontal | regra minima por tipo de conteudo (menu vs dado) — ver secao 6 |

**Nota — corpo tipo `menu` também pode ter múltiplas colunas** (decisão
desta sessão, formalizada em ADR-0001 — `docs/adr/ADR-0001-menu-suporta-matriz.md`): diferente
do eixo `colunas_ajustavel` do `dado` (declarado com/sem pela classe,
ajustável manualmente via chip), o número de colunas do `menu` é regido
pelo eixo **`distribuicao_menu`** (valores `fila` | `matriz`), calculado
**automaticamente** a partir da largura real do terminal — não é declarado
pela classe nem ajustável manualmente via chip. Algoritmo completo na
seção 8.3; valores em `config/layout_menu.json`.

---

## 4. Mecanismos de selecao (corpo tipo `dado`)

Quatro conceitos distintos, em camadas:

| Conceito | O que e | Como se forma |
|---|---|---|
| **Cursor / selecionado** | aponta um item; `[⏎]` executa acao sobre ele | navegacao via `[✥]` (setas do teclado), indicador `→` |
| **Grupo** | origem/categoria do dado (ex.: grupo 1, 2, 3) — atributo do proprio dado | ja existe nos dados, filtra **exibicao** via `[#]` |
| **Selecao** | conjunto **nomeado** de elementos (ex.: selecao `a`, `b`) — **cruza grupos livremente**, sem limite. Mecanismo geral: serve tanto para selecionar itens de dado quanto, futuramente, para selecionar ferramentas em um processo — o mecanismo e o mesmo, o contexto de uso e que muda | toggle via `[␣]`, indicador `●`/`○`, persiste com nome |
| **Lote** | unidade de **execucao** — calculado a partir de uma selecao no momento de rodar um processo especifico, tipicamente `selecao − o que ja foi processado por aquele processo`. A mesma selecao pode gerar lotes diferentes dependendo do processo | derivado, nao e marcado manualmente |

Termo descontinuado: **"lote" nao e sinonimo de "grupo"** nem de "selecao".
Grupo e origem/escopo de exibicao. Selecao e um conjunto nomeado que cruza
grupos. Lote e o resultado, calculado por processo, a partir de uma selecao.

**Em aberto por decisao do usuario (nao e pendencia, e escolha consciente)**:
a relacao exata entre `[#]` (filtro de grupo exibido) e `[␣]` (toggle de
selecao) — incluindo a possibilidade futura de "marcar todos os itens do
grupo filtrado" como atalho — fica para ser definida quando o caso de uso
aparecer. Nao ha decisao de coexistencia/exclusividade travada agora.

### 4.1 Navegação por `[✥]` (decidido nesta sessão)

`[✥]` é a dica visual de "use as setas do teclado" — a navegação em si é
feita pelas quatro setas, não por uma tecla própria.

- **Corpo em formato de matriz/grade** (ex.: `menu` em matriz, `dado` em
  colunas): as setas seguem a geometria real da grade — cima/baixo move
  dentro da coluna, esquerda/direita move entre colunas. Não é uma ordem
  abstrata de "próximo/anterior", é navegação 2D pela posição visual.
- **Dados mais complexos, sem grade regular**: é a própria tela/dataset que
  declara o que é navegável — regra geral, não fixa por formato. O corpo
  não assume uma estrutura só porque parece uma lista.

**Wrap toroidal (fechado nesta sessão)**: a grade se comporta como um
toróide — fecha nos dois eixos, cada um independente do outro.

- Seta pra cima na primeira linha de uma coluna → vai pra última linha
  **da mesma coluna**.
- Seta pra baixo na última linha → vai pra primeira linha da mesma coluna.
- Seta pra direita na última coluna → vai pra primeira coluna da mesma
  linha.
- Seta pra esquerda na primeira coluna → vai pra última coluna da mesma
  linha.

**Célula vazia (linha/coluna incompleta) — toróide local, não pula de
eixo**: como o preenchimento é coluna-a-coluna (seção 8.2), só a última
coluna pode ficar incompleta. Uma linha ou coluna incompleta forma seu
próprio toróide menor, contando só as posições realmente preenchidas —
o cursor nunca entra numa célula vazia, e o movimento nunca muda de eixo
pra "escapar" do vazio (ex.: seta pra direita não vira seta pra baixo).
Exemplo: cursor na última posição preenchida de uma linha incompleta,
seta direita → volta direto pra primeira posição da mesma linha, pulando
as células vazias intermediárias como se elas não existissem.

**Paginação é independente da navegação (fechado nesta sessão)**: se o
corpo também pagina (`[<][>]` existe), o cursor **nunca** troca de página
sozinho ao cruzar a borda do toróide — cada página é seu próprio toróide
fechado, só `[<][>]` muda de página. A seleção (ver seção 4.3), porém,
persiste entre páginas — o usuário pode ir e voltar com `[<][>]` marcando
itens de páginas diferentes antes de executar.

### 4.2 Estrutura do item do corpo tipo `dado` (decidido nesta sessão)

Todo item de um corpo tipo `dado` navegável tem exatamente três partes,
sempre na mesma ordem:

| Parte | Sigla | Função |
|---|---|---|
| Espaço do cursor | `ec` | onde `selecionado` (`→` ou preset equivalente) aparece quando o cursor está na linha |
| Espaço de toggle | `tg` | onde `incluido` (`●`/`○` ou preset equivalente) aparece |
| Texto do item | `tx` | conteúdo, tamanho variável |

**Uma estrutura só, não duas** — a diferença entre um item com seleção
real (ex.: tela de execução, como os "Artigos") e um item navegável sem
seleção (ex.: `[⏎]` = "Visualizar", ver seção 5.1.2) não é uma estrutura
separada: é só o **conteúdo visual de `tg`** que muda.

- Com seleção real: `tg` mostra o par on/off completo (`●`/`○` ou preset
  equivalente, seção 1.3).
- Sem seleção (só navegação + visualizar detalhe): `tg` mostra um símbolo
  **estático** (não alterna), configurável via schema — mantém o
  alinhamento uniforme entre os dois casos sem inventar uma segunda
  estrutura de item.

**Sobreposição `ec` × `tg`**: quando o cursor está na linha, `selecionado`
ocupa `ec` normalmente — `tg` continua mostrando o estado de seleção
daquele item (marcado ou não), os dois espaços coexistem lado a lado, não
se sobrepõem entre si. (A sobreposição só acontecia na formulação antiga
de uma coluna única — com `ec` e `tg` como espaços distintos, cada um tem
seu próprio lugar fixo.)

### 4.3 Espaçamento e layout do corpo tipo `dado` (decidido nesta sessão)

Regras próprias, distintas das do corpo tipo `menu` (seção 8) — **não
compartilham arquivo de configuração** (ver seção 4.4).

**Vãos** (valores iniciais, todos configuráveis):

| Vão | Mínimo | Máximo |
|---|---|---|
| `ec`↔`tg` e `tg`↔`tx` (dentro do item) | 1 espaço | 3 espaços |
| Entre colunas | 5 espaços | 10 espaços |
| Coluna ↔ borda | 5 espaços | sem teto — sobra vai pra cá |

**Alinhamento**: `ec`, `tg` e `tx` sempre alinhados verticalmente entre
todas as linhas de uma coluna (uniformidade de coluna). **Sobra de espaço
fica centralizada** (esquerda e direita) — diferente do corpo tipo `menu`,
que fechou em bloco à esquerda com sobra à direita (seção 8.1, ADR-0002); são regras independentes
por tipo de corpo, não uma regra geral do sistema.

**Tamanho de coluna**: definido pelo maior item daquela coluna específica
(mesma lógica já usada no `menu` em matriz, seção 8.2).

**Número de colunas**:
- Inicial: o máximo possível, aplicando a distribuição de vãos acima
  sobre a largura real do terminal.
- Ajuste manual: via `[-][+]` (chip `colunas`, seção 5.1) — sempre
  respeitando mínimo 1 e máximo conforme o que a largura atual comporta.

**Pendência**: regras de ajuste do próprio `tx` quando o texto não cabe no
espaço disponível (truncar com reticências, quebrar em múltiplas linhas,
outra estratégia) — ainda não definidas, ver seção 11.

### 4.4 Parametrização externa — `config/layout_dado.json`

Seguindo a política da seção 0: os valores concretos e configuráveis do layout
do corpo tipo `dado` vivem em `config/layout_dado.json`, não hardcoded. Esta
seção define o schema e a semântica; o arquivo guarda os dados.

Campos cobertos pelo arquivo:

- `estrutura_item`: ordem e papel das partes `ec`, `tg`, `tx` de cada item.
- `vaos`: mínimos e máximos de espaçamento entre partes do item (`ec`↔`tg`
  e `tg`↔`tx`), entre colunas e entre coluna e borda.
- `alinhamento`: regra de distribuição da sobra horizontal (centralizado) e
  uniformidade vertical de coluna.
- `colunas`: largura por maior item da própria coluna, número inicial e regra
  de ajuste via chip `[-][+]`.
- `navegacao`: wrap toroidal por eixo, tratamento de célula vazia e
  independência de paginação — origem semântica em seção 4.1.

---

## 5. barra_de_menus

### 5.1 Chips canônicos e ordem fixa (revisado nesta sessão)

```
[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

| Chip | Rótulo | Presença (existência) | Condição de existência | Estado ativo/inativo |
|---|---|---|---|---|
| `[Esc]` | Sair (só na tela Orquestrador) / Voltar (demais telas) / **Limpar** (ver 5.1.2) | sempre, primeiro | fixo — "Sair" é exclusivo da tela raiz (Orquestrador); qualquer outra tela usa "Voltar" | sempre ativo |
| `[<][>]` | Páginas | condicional | classe declara `paginacao: com` | inativo quando há apenas 1 página no momento |
| `[-][+]` | Colunas | condicional | classe declara `colunas_ajustavel: com` (tipo `dado`) | `[-]` inativo em `n_col` mínimo (1); `[+]` inativo em `n_col` máximo que a largura atual comporta |
| `[#]` | Grupos | condicional | classe declara filtro por grupo — abre entrada para digitar número do grupo, filtra exibição | — |
| `[⇆]` | Alternar | condicional | `quantidade_corpos: multiplos` — alterna foco de interação entre corpos | — |
| `[✥]` | Navegar | condicional | tela possui ao menos um corpo navegável (tipo `dado` ou `menu`) — move o cursor via setas do teclado quando o corpo em foco é navegável (ver 4.1) | inativo via `cor_inativo` quando o corpo em foco não é navegável |
| `[␣]` | Selecionar | condicional | classe declara formação de seleção (ver seção 4) — toggle nomeado, indicador `●`/`○` | — |
| `[⏎]` | **Todos** / **Executar** / **Visualizar** (ver 5.1.2) | sempre | executa a ação vinculada ao item sob o cursor ou sobre a seleção, conforme o tipo de tela | inativo quando não há alvo válido sob o cursor |
| específicos | (por classe) | condicional | chips próprios da classe — ver seção 5.2 | — |
| `[V]` | Verboso | condicional | classe/dados aceitam `tipo_exibicao: verboso` (só existe pra `dado`, ver seção 3) | — |
| `[?]` | Ajuda | sempre, último | — | sempre ativo |

**`[-][+]` — `n_col` não aparece no chip (decisão intencional)**: o chip
exibe o rótulo "Colunas"; o número atual de colunas (`n_col`) não aparece
dentro do chip. Essa ausência é decisão de design, não omissão; esta regra
não define outro local para exibir `n_col`.

Regra estrutural (mantida): **nenhum chip canônico decide sua própria
exibição** — presença é sempre derivada de uma propriedade de composição já
declarada pela classe de tela (seção 3). A barra_de_menus é só um espelho,
nunca uma fonte de decisão.

**Distinção existência vs ativo/inativo** (nova, ver seção 1.5): a presença
de um chip na barra é sempre estática, derivada da composição declarada. O
estado ativo/inativo é dinâmico, recalculado a cada render, e indicado
visualmente por `cor_inativo` — o chip continua ocupando a posição/ordem
(não desaparece), só muda de cor e para de reagir ao acionamento.

**`[⇆]` Alternar vs `[✥]` Navegar** — são conceitos de nível diferente:
`[⇆]` move o foco de interação **entre corpos** (só existe quando há mais
de um corpo na tela); `[✥]` move o cursor **dentro do corpo** que está em
foco no momento. Não são intercambiáveis.

### 5.1.2 Rótulo dinâmico — `[⏎]` e `[Esc]` (decidido nesta sessão)

Terceiro tipo de propriedade dinâmica de chip, além de existência (1.5) e
ativo/inativo (1.5): **rótulo que muda** conforme o estado atual, sempre
que a classe declarar `formação de seleção: com` (mesmo eixo que já
controla a existência do `[␣]`, seção 4) — regra válida para qualquer tela
nessa condição, não é caso a caso.

**`[⏎]` — três estados possíveis:**

| Estado | Rótulo | Ação |
|---|---|---|
| Nada selecionado ainda, tela com seleção/execução | `Todos` | marca todos os itens do corpo — depois disso o rótulo vira `Executar` |
| Alguma seleção marcada (manual ou via `Todos`) | `Executar` | roda a função da tela sobre os itens selecionados |
| Tela de visualização, sem execução (ex.: relatórios só-leitura) | `Visualizar` | abre o detalhe do item sob o cursor — não depende de seleção |

**`[Esc]` — camada extra sobre Sair/Voltar:**

- Se há seleção ativa no momento → `[Esc]` **limpa a seleção** (fica na
  mesma tela, não navega).
- Sem seleção ativa → comportamento normal (`Sair` na tela raiz / `Voltar`
  nas demais, seção 5.1).

**Fora de escopo desta sessão**: a reorganização de arquitetura de tela
(relatórios só-visualização usando `Info` como conteúdo principal, telas
de processo usando `corpo`) fica para o chat dedicado a `Info` — não foi
decidida aqui, só o terceiro rótulo `Visualizar` do `[⏎]`.


### 5.1.3 Arquivo de dados — `config/barra_de_menus.json`

Seguindo a política da seção 0: a ordem canônica, os rótulos e o mapeamento
de cada chip para o eixo de composição que controla sua existência vivem em
`config/barra_de_menus.json`, não hardcoded. Esta seção do glossário (5.1)
define o que cada campo do JSON significa; o JSON guarda os valores.

### 5.2 Chips específicos — categoria formal

Três tipos conhecidos, não texto livre. Um quarto tipo foi identificado
mas ainda não tem estrutura definida:

| Tipo | Estrutura | Natureza |
|---|---|---|
| **Toggle** | texto, tecla, `ativo` (booleano), papel | filtro de exibição, liga/desliga |
| **Múltiplo** | texto, teclas (plural), cores (por tecla), papel | filtro de exibição, conjunto de opções (`set`), tipicamente mutuamente exclusivas entre si |
| **Aciona processo** | *(estrutura a definir)* | executa lógica sobre seleção/lote — sem precedente formal em `teste_classe_c.py`. Lógica real de execução existe em `orquestrador.py` (não `teste_orquestrador_v2.py`), mas está misturada com `print()` direto no meio do código — na extração, separar o que é *processo* (mantém) do que é *exibição* (descarta, substituído pelo renderer novo) |
| **Aciona tela** | texto, tecla, `tela_destino`, papel | abre outra tela (navegação) — ex.: `[\|] Estilo` abre a tela/shadow menu de seleção de estilo. Diferente de "aciona processo": não executa lógica de fundo, só troca de tela |

`[|] Estilo` é um exemplo de específico do tipo **aciona tela**, presente
na barra_de_menus do Orquestrador; provavelmente recorrente em várias
telas, mas classificado como específico, não como canônico da ordem fixa
(seção 5.1) — fica na mesma posição que qualquer outro específico, entre
`[␣]` e `[V]`/`[?]`.

---

## 6. Layout e largura

- **Largura de tela**: sempre dinâmica, calculada a partir da largura real
  do terminal — sem perfis fixos pré-definidos. Sustentável porque nenhuma
  regra de composição (colunas, quebra de texto, padding, paginação)
  depende de largura fixa.
- **Redimensionamento reativo**: o sistema reage a mudança de tamanho do
  terminal em tempo real — não lê a largura uma vez na inicialização e
  guarda; a tela se ajusta enquanto está aberta, sem precisar reiniciar.
- **Organização horizontal por tipo de conteúdo do corpo** (revisado):
  - `menu`: **pode ser linha única horizontal (fila) ou matriz de múltiplas
    colunas**, calculado automaticamente pela largura real do terminal
    (ADR-0001 — supera a regra anterior de "sempre coluna única, sem colunas";
    ver `docs/adr/ADR-0001-menu-suporta-matriz.md` e seção 12). Continua **sem paginação** mesmo em modo matriz —
    overflow em `menu` não pagina (regra mantida). Regras completas de
    layout na seção 8.
  - `dado`: colunar (modo normal, `n_col` ajustável) ou tabular (modo
    verboso, largura de coluna calculada por conteúdo, texto longo quebra
    dentro da coluna).
- **Overflow**: nunca existe scroll. Conteúdo que excede o espaço
  disponível sempre pagina (exceto `menu`, ver acima). Espaço sobrando é
  preenchido (padding), nunca deixado vazio de forma desorganizada.

### 6.1 Indicador de paginação

Quando o corpo tem paginação, a última linha da própria borda do corpo
exibe o indicador de página, ancorado à direita, no formato:

```
─ página X/Y ─
```

**Composição da linha, lida da direita para a esquerda:**

| Posição | Elemento | Fonte |
|---|---|---|
| 1 | `canto_inferior_direito` | estilo ativo |
| 2 | 1 unidade de `traco_inferior` | estilo ativo (dash ou espaço, conforme o estilo) |
| 3 | bloco `─ página X/Y ─` | **sempre traço literal**, independente do estilo ativo (mesmo no estilo "aberta", onde `traco_inferior` normal é espaço) |
| 4 | resto da linha até `canto_inferior_esquerdo` | preenchido com `traco_inferior` do estilo ativo |

O bloco de texto estica conforme o tamanho de X/Y (ex.: "1/3" vs "12/47");
o preenchimento da posição 4 encolhe para compensar, mantendo a largura
total da borda.

**Posição na tela**: sempre na última linha do próprio corpo com
paginação — não necessariamente colada na barra_de_menus. Quando não há
objeto Info, corpo e "linha acima da barra_de_menus" costumam coincidir
visualmente, mas isso é coincidência, não regra: o indicador pertence à
borda do corpo, nunca ao layout geral da tela.

**Exceção — Info presente**: o objeto Info não herda nem desloca o
indicador de página. Ele nunca aparece na borda do Info, mesmo o Info
estando mais próximo da barra_de_menus. O indicador continua preso à
borda do corpo paginado, mesmo com Info ocupando o espaço abaixo dele.

**Lado a lado**: cada corpo exibe sua própria paginação, ancorada à
direita **dentro da própria borda**, independente de qual lado da tela
aquele corpo ocupa fisicamente.

**Ainda não definido (adiado, sem caso de uso real ainda)**: combinação de
layout lado a lado com objeto Info presente ao mesmo tempo.

---

## 8. Corpo tipo `menu` — regras de layout (revisado nesta sessão)

Aplica-se a qualquer corpo cujo tipo de conteúdo seja `menu` (ver seção
2.1), não apenas à tela Orquestrador. Cobre os dois modos: **fila** (linha única horizontal) e **matriz** (múltiplas colunas) — ver seção 6.

### 8.1 Vãos (espaçamento) — mínimo e máximo, nunca fixo

Substitui a regra anterior de valores fixos (2 espaços entre chip e texto,
bloco sempre centralizado). Formalizado por ADR-0002 (bloco à esquerda com
sobra à direita) e ADR-0003 (vãos elásticos) — ver seção 12.

| Vão | Mínimo | Máximo |
|---|---|---|
| `[R]` ↔ Rótulo (dentro do próprio item) | 1 espaço | 3 espaços |
| Entre itens na mesma linha / entre colunas (matriz) / borda ↔ primeiro-último elemento | 2 espaços | 5 espaços |

**Prioridade de distribuição de espaço sobrando**: primeiro estica os vãos
entre itens/colunas até o máximo (5); só depois disso, o que sobrar vai
para a margem borda↔elemento (também respeitando seu próprio teto).

**Alinhamento final**: espaço que sobra além de todos os tetos (vãos e
margens já no máximo) fica à **direita** — não há mais centralização do
bloco. Vale tanto para o modo fila quanto para o modo matriz.

### 8.2 Modo matriz

- Largura de cada coluna = largura do maior item **daquela coluna**
  específica (não do maior item de todo o menu).
- Itens alinhados à esquerda dentro da coluna.
- **Chip e rótulo alinham como duas sub-colunas independentes** (fechado
  nesta sessão): dentro de cada coluna da grade, o chip (`[R]`) alinha à
  esquerda pela largura do maior chip daquela coluna, e o rótulo alinha à
  esquerda pela largura do maior rótulo daquela coluna — não é uma string
  única "chip+rótulo" tratada como bloco. Isso garante que todos os
  rótulos de uma coluna comecem na mesma posição horizontal, mesmo com
  chips de tamanhos diferentes (ex.: `[Esc]` vs `[<][>]`).
- Ordem de preenchimento: **coluna-a-coluna** — desce até completar as
  linhas da coluna atual, depois passa para a próxima coluna. Confirmado
  por levantamento neutro do Codex em `teste_combo.py`
  (`_grade_coluna_continua`, `_colunar_ajustado`) — ver seção 11.
- Colunas incompletas: célula vazia, sem preenchimento visual especial.

### 8.3 Algoritmo de cálculo de colunas (fechado nesta sessão)

Duas etapas, nesta ordem:

1. **Tenta uma linha só**: calcula se todos os itens cabem numa única
   linha (`n_col` = número de itens), usando os vãos no **mínimo** (1
   espaço `[R]`↔rótulo, 2 espaços entre itens). Se couber, usa essa
   distribuição — vira o modo fila, uma linha, sem crescer verticalmente.
2. **Se não couber em uma linha, distribui em matriz**: maximiza o número
   de colunas usando os vãos no mínimo; só aumenta uma linha (reduz uma
   coluna) se a distribuição anterior não coube na largura disponível
   mesmo com os vãos no mínimo. A largura de cada coluna já usa a largura
   do maior item **daquela coluna específica** (seção 8.2), não uma
   aproximação pelo maior item do menu inteiro.

Em ambas as etapas, depois de achar a distribuição que cabe, os vãos
esticam até o máximo pra preencher a sobra (ver 8.1). **Sem teto absoluto
de colunas** — o único limite é a largura disponível.

**Número mínimo de linhas**: 1 (configurável via `layout_menu.json`, ver
8.4).

### 8.4 Parametrização externa — `config/layout_menu.json`

Decisão desta sessão: as regras de vão, alinhamento e linhas mínimas do
corpo tipo `menu` vivem num arquivo de configuração próprio, não
hardcoded — mesmo espírito da "proibição de hardcoding" já usada no schema
de estilo (seção 1, `contrato_estilo.md`). Caminho do arquivo:
`config/layout_menu.json` (ver política da seção 0) — **não usar
"barra_menu"**, pois mistura os termos `menu` (tipo de objeto do corpo) e
`barra_de_menus` (região fixa da tela), que a seção 2 proíbe confundir.

Campos identificados até agora (schema ainda não fechado como contrato
formal — ver seção 11):

- vão mínimo/máximo chip↔rótulo
- vão mínimo/máximo entre itens/colunas/margem
- alinhamento da sobra (`direita`)
- número mínimo de linhas (default `1`)
- regras de navegação: `wrap` toroidal (cada eixo fecha de forma
  independente) e `celula_vazia` (linha ou coluna incompleta forma seu
  próprio toróide local, sem entrar em célula vazia nem mudar de eixo) —
  origem semântica: seção 4.1

### Alinhamento vertical (mantido sem alteração nesta sessão)

- Distribuição uniforme entre os itens.
- Nunca mais que 2 linhas em branco entre um item e o próximo.
- Espaço restante (após aplicar o limite acima) é distribuído entre topo e
  base do bloco.

---

## 9. Objeto `Info` — regras de layout

`Info` é um objeto opcional do corpo (ver seção 2.1), tipo "resumo".
Estrutura: lista de pares rótulo/valor, uma linha separadora, uma linha de
Total, uma linha em branco obrigatória, e uma segunda lista de marcadores
(símbolo + rótulo + valor).

**Alinhamento horizontal:** mesma regra do corpo tipo `menu` (seção 8) —
coluna dimensionada pelo maior rótulo, alinhamento à esquerda dentro do
bloco. **Pendente de confirmação** (ver seção 11): o `menu` adotou bloco
à esquerda com sobra à direita (ADR-0002) — falta decidir se o `Info`
acompanha essa mudança ou mantém centralização.

**Alinhamento vertical:** mesma regra do corpo tipo `menu` (seção 8), com
uma exceção obrigatória: sempre existe exatamente 1 linha em branco entre
a linha de "Total" e o início da lista de marcadores — essa linha não é
opcional nem sujeita à distribuição uniforme geral.

**Formato do valor numérico:** número puro, sem zero à esquerda, alinhado
à direita dentro do campo (ex.: `50`, não `050`). Não há padding de
dígitos.

**Marcadores oficiais (8), confirmados nesta sessão:**

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

Este conjunto substitui qualquer legenda de sistema antigo — não deriva de
`teste_classe_c.py` nem de nenhuma captura de tela do sistema legado.

**Campos do resumo principal (antes do Total), confirmados:** Adicionados,
Fichados, Consolidados, Qualificados, Orfão, Missing, Secundários,
Descartados (8 campos).

**Valor sempre numérico**: nunca existe estado de travessão (`—`) ou
"sem dado" — todo campo sempre exibe um número, `0` incluso. Uma captura
de tela anterior mostrou `—` em dois campos, mas isso era mockup
incompleto, não um estado real do sistema.

---

## 10. Tiling (2+ corpos tipo dado/menu — não se aplica ao Info)

- Quantidade de corpos (1 / múltiplos) é declarada pela classe de tela
  (seção 3).
- Se múltiplos, o **arranjo** (sobreposto vs lado a lado) pode ser
  **fixado pela própria classe** — nesse caso, a preferência global do
  usuário é ignorada para aquela tela.
- Se a classe não fixar arranjo, usa-se o campo `tiling` do estilo (seção
  1.4) como default — escolha manual do usuário, sem largura mínima de
  segurança que force sobreposto.
- Em modo lado a lado (2 colunas), o espaço horizontal se distribui em 3
  vãos, igualmente: borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda.
- A posição do objeto **Info** é eixo separado (seção 3, "Posição do
  Info") — nunca decidida por `tiling` nem pelo arranjo de múltiplos
  corpos.
- Quando há múltiplos corpos, `[⇆]` alterna o foco de interação entre eles
  (ver seção 5.1).
- **Pendente** (já registrado seção 6.1): combinação de lado a lado com
  objeto Info presente ao mesmo tempo.

## 11. Pendências em aberto

Itens que ainda não têm decisão do usuário:

- **Regras de ajuste do `tx`** (corpo tipo `dado`, seção 4.3): quando o
  texto do item não cabe no espaço disponível — truncar com reticências,
  quebrar em múltiplas linhas, ou outra estratégia. Ainda não definidas.
- **`popup_execucao`** (estrutura nova, não é corpo/Info/barra_de_menus):
  janela temporária de saída de execução de script. Mencionada nesta
  sessão, usuário já tem ideias mas decidiu tratar depois de fechar o que
  já estava em andamento. Precisa de regras próprias (tamanho, posição,
  fechamento, bloqueio de tela por trás, borda própria do schema de
  estilo).
- **Impacto no alinhamento do objeto `Info`**: ver seção 9 — falta
  confirmar se acompanha a mudança do `menu` (centralizado → bloco à esquerda com sobra à direita) ou
  segue centralizado como o `dado` (seção 4.3). Tratar junto do chat
  dedicado a `Info`.
- **Segunda pauta de "estilos de exibição de dados no corpo"**:
  mencionada pelo usuário nesta sessão, ainda não descrita.
- **`layout_menu.json` — campos de navegação**: vãos, alinhamento e número
  mínimo de linhas já formalizados via ADR-0003 e `contrato_composicao_corpo.md`
  (seção 5.2). Pendente apenas a formalização dos campos de `navegacao` em
  `config/layout_menu.json`, que deve aguardar o contrato de mecanismos de
  seleção/navegação.
- **Reorganização corpo × Info** (relatórios só-visualização usando `Info`
  como conteúdo principal, telas de processo usando `corpo`): mencionada
  nesta sessão, explicitamente adiada para o chat dedicado a `Info` — não
  é lacuna, é escopo remarcado de propósito.

### Levantamento do Codex — `teste_classe_c.py` / `teste_combo.py` (referência, não decisão)

Resumo do levantamento neutro já recebido, mantido aqui como evidência de
apoio (não substitui decisão do usuário):

- Preenchimento de matriz: coluna-a-coluna (`_grade_coluna_continua`,
  `_colunar_ajustado`), com exceção especial pro menu de 2 linhas.
- Colunas: legado usa perfis fixos de largura (67/101/135) via `Tab`, não
  largura real do terminal — **não aplicável** ao sistema novo (regra de
  largura dinâmica já fechada, seção 6).
- Navegação: não há cursor/setas em matriz no legado; usa teclas diretas
  (`Esc`, `Tab`, `|`, `V`, `+`, `-`, `<`, `>`, `J`, `#`, `Enter`) e seleção
  por número digitado após `Enter`. Comportamento de wrap: não encontrado.
- Resize: não há resize real por terminal no legado (`orquestrador.py` lê
  `shutil.get_terminal_size` no render, mas sem handler de `SIGWINCH`).
- Bordas incompletas: preenchidas com célula vazia (`None` / string vazia
  + `rstrip()`).

Itens adiados intencionalmente (não são lacuna, são decisão de adiar):

- Relação entre `[#]` (filtro de grupo) e `[␣]` (toggle de seleção) — ver
  seção 4.
- Estrutura do chip "aciona processo" — ver seção 5.2, será extraída de
  `orquestrador.py` quando o primeiro caso concreto for definido,
  separando lógica de processo de código de exibição (`print`) misturado.
- Combinação de layout lado a lado com objeto Info presente ao mesmo
  tempo — ver seção 6.1, sem caso de uso real ainda.

## 12. ADRs aceitas (decisões desta sessão que reabriam contratos ativos)

As quatro mudanças abaixo estavam pendentes de ADR formal e foram todas
formalizadas em 2026-07-05. A implementação pode incorporá-las.

| ADR | Contrato afetado | Mudança | Origem (nesta sessão) |
|---|---|---|---|
| ADR-0001 | `contrato_composicao_corpo.md` | `menu` deixa de ser fixo em coluna única — passa a suportar `fila` e `matriz` (múltiplas colunas) | Seções 6, 8 |
| ADR-0002 | `contrato_composicao_corpo.md` | Bloco do `menu` à esquerda com sobra acumulada à direita do bloco (substituí centralização) | Seção 8.1 |
| ADR-0003 | `contrato_composicao_corpo.md` | Vãos do `menu` (chip↔rótulo, entre itens) deixam de ser valores fixos e passam a ter mínimo/máximo elástico | Seção 8.1 |
| ADR-0004 | `contrato_estilo.md` | Novos campos genéricos `cor_inativo` e `cor_alerta` | Seção 1.5 |
