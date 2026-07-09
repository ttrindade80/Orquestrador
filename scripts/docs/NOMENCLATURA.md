---
name: nomenclatura-sistema-novo
description: Glossario consolidado de termos do sistema novo, base para os contratos de estilo, composicao de corpo e barra_de_menus
metadata:
  type: nomenclatura
  scope: sistema_novo
  status: parcial
  origem_especificacao: usuario_sessao_2026-07-05
  atualizado_em: 2026-07-09
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

## 0. Política — NOMENCLATURA.md, `estilo.json` e JSONs de tela (ADR-0008)

O modelo de configuração passou de JSON por domínio/componente para JSON por
tela (ADR-0008, 2026-07-07). A responsabilidade de cada artefato é:

| Artefato | Responsabilidade |
|---|---|
| `docs/NOMENCLATURA.md` (este documento) | **Schema e semântica**: quais campos existem, o que cada um significa, tipo, restrições e como o renderer deve interpretá-los. Não guarda valor concreto de produção, composição de tela nem instância. |
| `config/estilo.json` | **Biblioteca global de aparência**: presets de borda, chip, indicadores e demais parâmetros gerais de aparência. Não declara tela, conteúdo, composição, destino, ação, item de `lancador` nem instância de `dashboard`. |
| `tela.json` (JSON próprio de cada tela) | **Declaração concreta da tela**: composição do corpo, instâncias de `console`, `dashboard`, `lancador` e `barra_de_menus`, listas de itens, chips, destinos, ações registradas, regras de existência/ativo-inativo, parâmetros visuais locais, bindings, filtros e regras de exibição. Não é código executável. Não guarda estado de runtime. |

**Regra declarativa (ADR-0008)**: toda mudança que puder ser expressa por
configuração deve ser feita alterando o JSON da tela, não o código. Exemplos:
adicionar item ao `lancador`, mudar texto ou chip, apontar para nova tela,
ajustar alinhamento, colunas, espaçamento e regras de exibição.

**Estado de runtime não pertence ao JSON da tela**: cursor atual, página
atual, filtro ativo, modo verboso ligado/desligado, seleção atual e item
focado são estado de execução, não configuração. O JSON pode declarar
defaults iniciais; o estado vivo pertence à execução.

**Nomenclatura de arquivo**: nunca usar abreviação que misture dois termos
já distinguidos neste glossário (ex.: nunca `barra_menu.json` — usar
`barra_de_menus.json`). Para o corpo tipo `lancador`, o arquivo canônico é
`config/lancador.json`; não criar `config/layout_lancador.json`.

**Localização**: todos os JSON de configuração ficam em `config/`, dentro de
`scripts/`, irmã de `docs/` — nunca dentro de `docs/` (que é documentação
neutra, sem dado de produção, ver `docs/INDICE.md`).

**Status dos artefatos JSON (modelo ADR-0008):**

| Artefato | Papel no novo modelo | Status |
|---|---|---|
| `config/estilo.json` | Biblioteca global de aparência — mantida | ativo (seção 1) |
| `config/layout_dado.json` | Obsoleto/transicional — rastreabilidade da migração `dado` → `console` | obsoleto; não é fonte canônica |
| `config/layout_menu.json` | Obsoleto/transicional — rastreabilidade da migração `menu` → `lancador` | obsoleto; não é fonte canônica |
| `config/lancador.json` | Parâmetros de layout do tipo `lancador` — a reavaliar/migrar conforme ADR-0008 | ativo transicional (seção 8.4) |
| `config/layout_console.json` | Parâmetros de layout do tipo `console` — a reavaliar/migrar conforme ADR-0008 | ativo transicional (seção 4.4) |
| `config/barra_de_menus.json` | Parâmetros de `barra_de_menus` — a reavaliar/migrar conforme ADR-0008 | ativo transicional (seção 5.1.3) |
| `config/cabecalho.json` | Parâmetros de apresentação do `cabecalho` — a reavaliar/migrar conforme ADR-0008 | ativo transicional (seção 7.4) |
| `tela.json` (por tela) | Declaração concreta de cada tela — modelo canônico ADR-0008 | contrato ativo em `docs/contratos/contrato_tela_json.md`; JSONs reais aguardam DOC-B010 |

**`dashboard` não terá `config/dashboard.json` próprio.** A classe `dashboard`
é definida como tipo mínimo (seção 9); dados concretos pertencem ao JSON da
tela onde o `dashboard` for instanciado.

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

Campo `tiling`. **Terminologia final de arranjo (ADR-0011, 2026-07-08)**:
valores finais são `vertical` | `horizontal`. Os termos `sobreposto` e
`lado_a_lado` permanecem como **aliases transicionais** — `sobreposto → vertical`
e `lado_a_lado → horizontal` — apenas para compatibilidade de JSONs/contratos
legados até migração específica; não são terminologia final.

Escolha manual do usuário, não decisão automática por largura de
terminal. Não existe largura mínima de segurança que force sobreposto —
a preferência do usuário sempre vale quando aplicada.

**Escopo**: aplica-se ao arranjo de elementos funcionais do corpo —
`console`, `lancador` e `dashboard` seguem o mecanismo geral de composição
declarativa do `corpo` (ADR-0010, 2026-07-08). A posição do `dashboard` não
é eixo separado externo ao mecanismo de composição; é controlada pela
estrutura declarativa do `corpo`. Ver seção 3 para a tabela de eixos e
seção 10 para tiling. O campo `posicao_dashboard` está descontinuado como
eixo independente (ADR-0010); JSONs existentes com esse campo podem ser
honrados por compatibilidade em handoff futuro de migração.

**É default, não obrigatório**: a classe de tela pode fixar seu próprio
arranjo (seção 3, "Arranjo de múltiplos corpos") e ignorar a preferência
global do usuário para aquela tela especificamente. `tiling` só é
consultado quando a classe não especifica um arranjo fixo.

Campo já incluído em `contrato_estilo.md` (`ativo`).

**Disambiguação terminológica obrigatória (ADR-0013, 2026-07-09)**:
`corpo.arranjo = "vertical"` é **arranjo/composição** dos elementos do corpo
(ADR-0011), **não** ocupação da altura do terminal. O preenchimento da altura
da janela do terminal é conceito distinto, com termo específico próprio —
`ocupacao_vertical_terminal` (ou equivalente, como `preenchimento_altura_corpo`
ou `altura_disponivel`). Os dois conceitos coexistem independentemente: uma
tela com `corpo.arranjo = "horizontal"` também deve poder ocupar a altura
disponível. A substring `vertical` sozinha é ambígua e não deve ser usada
como critério de alteração normativa (ver ADR-0014, regra contra filtro
parcial).

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

- **console**: corpo interativo com dados, incluindo saída de script/log;
  preserva as regras do antigo tipo `dado`.
- **lancador**: objeto do corpo que é uma composição de navegação para outras
  telas (não confundir com `barra_de_menus`, que é a região fixa da tela).
- **dashboard**: objeto opcional do corpo — saída passiva formatada,
  resumo/legenda ou visão consolidada dos dados exibidos; antigo `Info`.

Extensibilidade: um novo tipo de conteudo pode ser adicionado no futuro
seguindo o mesmo principio do estilo — schema aberto, sem exigir reescrita
do renderer, desde que a amarracao declarativa (classe declara, renderer so
executa) seja respeitada.

**Tela de processamento como composição (ADR-0007)**: tela de processamento
não é tipo de corpo. A taxonomia fechada do corpo permanece `console`,
`lancador`, `dashboard`; não existe quarto tipo de corpo para processamento.

Uma tela de processamento é descrita como composição de tipos existentes:

- um ou mais corpos tipo `console`, quando houver região interativa ou
  navegável por `[✥]`;
- zero ou um `dashboard`, quando houver saída passiva formatada, como estado
  agregado, resumo ou progresso;
- chips específicos declarados pela classe de tela na `barra_de_menus`.

Chips específicos pertencem à `barra_de_menus`, nunca ao corpo. A classe de
tela declara sua existência; a `barra_de_menus` continua sendo espelho da
declaração, não fonte de decisão.

`lancador` não representa processamento. O `lancador` continua sendo navegação
para outras telas via `tela_destino`. Nenhuma regra de `[✥]` muda: `[✥]`
continua restrito a corpo tipo `console`.

Exemplo conceitual, não obrigatório: uma tela de processamento pode conter
`cabecalho`, corpo com `console` Lista, corpo com `console` Detalhe, corpo com
`console` Log se o log for navegável, zero ou um `dashboard` de estado
agregado/resumo/progresso, e `barra_de_menus` com chips canônicos e chips
específicos da classe. Este exemplo não obriga toda tela de processamento a
ter exatamente essa estrutura.

Ficam fora de escopo desta decisão: pop-up de ferramenta, seleção prévia de
ferramenta, execução em segundo plano, estrutura do chip `aciona_processo`,
renderer de progresso, implementação e alteração de dados reais de
classes/telas.

### 2.2 `tela.json` — declaração configurável da tela

`tela.json` é o nome canônico da declaração configurável de uma tela. Ele é
o arquivo declarativo que descreve a configuração concreta que o renderer
deve validar e executar.

O JSON de uma tela pode declarar:

- estrutura do `cabecalho` (título e descrição);
- composição do `corpo` e seus elementos;
- instâncias de `console`, `dashboard` e `lancador`;
- instância de `barra_de_menus` e lista de chips;
- bindings entre dados e campos exibidos;
- filtros declarativos;
- ações registradas/whitelisted;
- regras de exibição, layout e tiling.

`tela.json` é declarativo, não procedural. Ele não executa comandos
arbitrários, scripts livres, loops ou lógica executável não registrada. Ele
não guarda estado de runtime (cursor, página, seleção, filtro ativo ou modo
verboso corrente).

Toda tela declarada por JSON deve conter, no mínimo:

```text
schema
id
cabecalho
corpo
barra_de_menus
```

O contrato ativo de referência é `docs/contratos/contrato_tela_json.md`.

---

## 3. Composicao de corpo (por classe de tela)

Declarada pela classe de tela, nunca decidida pelo renderer ou pela
barra_de_menus.

| Eixo | Valores |
|---|---|
| Tipo de conteudo | `console`, `lancador` |
| Tipo de exibicao | `normal` (lista simples) / `verboso` (detalhes) — aplica-se apenas a `console` |
| Dashboard | presente / ausente |
| Quantidade de corpos | 1 corpo / múltiplos corpos |
| Arranjo de múltiplos corpos (opcional) | `vertical` / `horizontal` (terminologia final, ADR-0011) — a classe PODE fixar isso; se não fixar, usa o `tiling` global do estilo (seção 1.4) como default. `sobreposto`/`lado_a_lado` são aliases transicionais |
| Posição do dashboard | Controlada pela estrutura declarativa geral do `corpo` (ADR-0010). `dashboard` é elemento funcional do corpo como `console` e `lancador`; não possui eixo de posicionamento separado. O campo `posicao_dashboard` (`horizontal`/`vertical`) está descontinuado como eixo independente; JSONs existentes com este campo podem ser honrados por compatibilidade em handoff futuro de migração. |
| Paginacao | com / sem |
| Colunas ajustavel (tipo `console`) | com / sem — eixo proprio, distinto de paginacao. Aplica-se apenas a corpos tipo `console`, ajustável manualmente via chip `[-][+]` |
| `filtro_de_grupo` | `com` / `sem` — eixo próprio; condiciona a existência estrutural do chip `[#]`; não decide ainda a relação entre filtro de grupo e seleção |
| `formacao_de_selecao` | `com` / `sem` — eixo próprio; condiciona a existência estrutural do chip `[␣]` e participa da semântica do rótulo dinâmico de `[⏎]` |
| Espacamento interno | universal (renderer): linha em branco entre borda e conteudo, sempre |
| Organizacao horizontal | regra minima por tipo de conteudo (lancador vs console) — ver secao 6 |

**Nota — corpo tipo `lancador` também pode ter múltiplas colunas** (decisão
desta sessão, formalizada em ADR-0001 — `docs/adr/ADR-0001-menu-suporta-matriz.md`): diferente
do eixo `colunas_ajustavel` do `console` (declarado com/sem pela classe,
ajustável manualmente via chip), o número de colunas do `lancador` é regido
pelo eixo **`distribuicao_lancador`** (valores `fila` | `matriz`), calculado
**automaticamente** a partir da largura real do terminal — não é declarado
pela classe nem ajustável manualmente via chip. Algoritmo completo na
seção 8.3; valores em `config/lancador.json`.

---

## 4. Corpo tipo `console`

`console` é um container interativo e navegável genérico (ver seção 2.1).
A política geral de composição pertence à instância do `console`, declarada
pelo JSON da tela. Os itens internos definem sua renderização específica.

Propriedades gerais:

- pode conter itens heterogêneos;
- o cursor navega por itens, não por linhas físicas;
- cada item pode declarar tipo, binding, navegabilidade, seleção e ação;
- filtros atuam antes da paginação;
- modo verboso é estado de exibição reutilizável — não é variação específica
  de cada tela.

A instância de `console` em uma tela é declarada pelo JSON da tela. O
contrato detalhado de tipos internos de item de `console` é pendência
DOC-B008. A revisão formal como container genérico é DOC-0024.

### 4.0 Mecanismos de seleção (corpo tipo `console`)

Quatro conceitos distintos, em camadas:

| Conceito | O que e | Como se forma |
|---|---|---|
| **Cursor / selecionado** | aponta um item; `[⏎]` executa acao sobre ele | navegacao via `[✥]` (setas do teclado), indicador `→` |
| **Grupo** | origem/categoria do dado (ex.: grupo 1, 2, 3) — atributo do proprio dado | ja existe nos dados, filtra **exibicao** via `[#]` |
| **Selecao** | conjunto **nomeado** de elementos (ex.: selecao `a`, `b`) — **cruza grupos livremente**, sem limite. Mecanismo geral: serve tanto para selecionar itens de console quanto, futuramente, para selecionar ferramentas em um processo — o mecanismo e o mesmo, o contexto de uso e que muda | toggle via `[␣]`, indicador `●`/`○`, persiste com nome |
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

- **Corpo tipo `console` em formato de matriz/grade**: as setas seguem a
  geometria real da grade — cima/baixo move dentro da coluna,
  esquerda/direita move entre colunas. Não é uma ordem abstrata de
  "próximo/anterior", é navegação 2D pela posição visual.
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

**Escopo de `[✥]` (ADR-0005, atualizado pela ADR-0006)**: `[✥]` e as setas da
`barra_de_menus` controlam somente cursor de corpo tipo `console`. Corpo tipo
`lancador` possui navegação própria por itens via `tela_destino`, mas não é
corpo navegável por `[✥]`; `dashboard` também não é corpo navegável por `[✥]`.

### 4.2 Estrutura do item do corpo tipo `console` (decidido nesta sessão)

Todo item de um corpo tipo `console` navegável tem exatamente três partes,
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

### 4.3 Espaçamento e layout do corpo tipo `console` (decidido nesta sessão)

Regras próprias, distintas das do corpo tipo `lancador` (seção 8) — **não
compartilham arquivo de configuração** (ver seção 4.4).

**Vãos** (valores iniciais, todos configuráveis):

| Vão | Mínimo | Máximo |
|---|---|---|
| `ec`↔`tg` e `tg`↔`tx` (dentro do item) | 1 espaço | 3 espaços |
| Entre colunas | 5 espaços | 10 espaços |
| Coluna ↔ borda | 5 espaços | sem teto — sobra vai pra cá |

**Alinhamento**: `ec`, `tg` e `tx` sempre alinhados verticalmente entre
todas as linhas de uma coluna (uniformidade de coluna). **Sobra de espaço
fica centralizada** (esquerda e direita) — diferente do corpo tipo `lancador`,
que fechou em bloco à esquerda com sobra à direita (seção 8.1, ADR-0002); são regras independentes
por tipo de corpo, não uma regra geral do sistema.

**Tamanho de coluna**: definido pelo maior item daquela coluna específica
(mesma lógica já usada no `lancador` em matriz, seção 8.2).

**Número de colunas**:
- Inicial: o máximo possível, aplicando a distribuição de vãos acima
  sobre a largura real do terminal.
- Ajuste manual: via `[-][+]` (chip `colunas`, seção 5.1) — sempre
  respeitando mínimo 1 e máximo conforme o que a largura atual comporta.

**Pendência**: regras de ajuste do próprio `tx` quando o texto não cabe no
espaço disponível (truncar com reticências, quebrar em múltiplas linhas,
outra estratégia) — ainda não definidas, ver seção 11.

### 4.4 Parametrização externa — `config/layout_console.json`

Seguindo a política da seção 0: os valores concretos e configuráveis do layout
do corpo tipo `console` vivem em `config/layout_console.json`, não hardcoded. Esta
seção define o schema e a semântica; o arquivo guarda os dados.

`config/layout_dado.json` permanece apenas como artefato obsoleto/transicional
de rastreabilidade da migração `dado` → `console`; não é fonte canônica nova.

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

A `barra_de_menus` é uma instância declarada pela tela. Cada tela declara
sua `barra_de_menus` no JSON da tela como uma lista de chips. A barra
continua sendo espelho da declaração — nunca fonte de decisão sobre
composição.

**Declarativa por tela (ADR-0012, 2026-07-08)**: a `barra_de_menus` não
contém todos os chips canônicos por padrão. Cada tela declara apenas os
chips aplicáveis ao seu estado/capacidade atual; renderer, loader, modelo e
demo não geram chips canônicos por conta própria; testes validam os chips
declarados no JSON da tela. A existência de um chip canônico como categoria
não obriga sua presença em toda tela.

**Distribuição visual da barra (ADR-0014, 2026-07-09)**: o campo
`barra_de_menus.distribuicao` é termo específico completo que controla a
disposição visual dos chips na região da barra. Quando
`barra_de_menus.distribuicao = "horizontal"`, os chips devem ser dispostos
como **distribuição horizontal responsiva** — não linha única fixa e não
empilhados um por linha; se não couberem em uma linha, a barra quebra em
multilinha de forma determinística conforme declarado. A string `"horizontal"`
é **alias transitório** de
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`; o formato
canônico futuro é objeto declarativo, registrado na ADR-0014, aplicável em
handoff futuro.

**Disambiguação obrigatória — três termos distintos e independentes**:

| Termo específico completo | Conceito | Região | Forma |
|---|---|---|---|
| `corpo.arranjo = "horizontal"` | ordem/composição horizontal dos elementos do corpo (ADR-0011) | corpo | arranjo |
| `barra_de_menus.distribuicao = "horizontal"` | distribuição horizontal **responsiva** dos chips (alias transitório) | barra_de_menus | string transitória |
| `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` | forma canônica futura da distribuição responsiva dos chips | barra_de_menus | objeto declarativo |

Esses três termos **não colapsam**: uma substring (`horizontal`) não os
identifica unicamente. `barra_de_menus.distribuicao` é **independente** de
`corpo.arranjo` — uma tela pode ter `corpo.arranjo = "vertical"` e
`barra_de_menus.distribuicao = "horizontal"` simultaneamente. Chips de itens
do `lancador`/corpo (ex.: `g`, `d`) não são chips da `barra_de_menus` e não
seguem esta distribuição.

**Regra de alteração por termo específico (ADR-0014, Parte B)**: alterações
normativas e implementações devem atingir apenas termos específicos
completos (ex.: `corpo.arranjo = "vertical"`,
`barra_de_menus.distribuicao = "horizontal"`, `ocupacao_vertical_terminal`).
Filtros parciais por substring (`vertical`, `horizontal`, `barra`, `chip`,
`arranjo`) podem ser usados apenas para busca/auditoria, nunca como
critério automático de substituição.

Chips canônicos e chips específicos devem poder ser instâncias declaradas
no JSON da tela. A futura classe `chip` será detalhada em contrato próprio
(DOC-B006). Até lá, a ordem e semântica de cada chip são definidas nesta
seção.

### 5.1 Chips canônicos e ordem fixa (revisado nesta sessão)

```
[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

| Chip | Rótulo | Presença (existência) | Condição de existência | Estado ativo/inativo |
|---|---|---|---|---|
| `[Esc]` | Sair (só na tela Orquestrador) / Voltar (demais telas) / **Limpar** (ver 5.1.2) | declarativa por tela; quando presente, primeiro na ordem | fixo — "Sair" é exclusivo da tela raiz (Orquestrador); qualquer outra tela usa "Voltar" | sempre ativo |
| `[<][>]` | Páginas | condicional | classe declara `paginacao: com` | inativo quando há apenas 1 página no momento |
| `[-][+]` | Colunas | condicional | classe declara `colunas_ajustavel: com` (tipo `console`) | `[-]` inativo em `n_col` mínimo (1); `[+]` inativo em `n_col` máximo que a largura atual comporta |
| `[#]` | Grupos | condicional | classe declara filtro por grupo — abre entrada para digitar número do grupo, filtra exibição | — |
| `[⇆]` | Alternar | condicional | `quantidade_corpos: multiplos` — alterna foco de interação entre corpos | — |
| `[✥]` | Navegar | condicional | tela possui ao menos um corpo tipo `console` navegável — move o cursor via setas do teclado quando o corpo em foco é `console` navegável (ver 4.1) | inativo via `cor_inativo` quando há outro corpo tipo `console` navegável na tela, mas o corpo em foco não é `console` |
| `[␣]` | Selecionar | condicional | classe declara formação de seleção (ver seção 4) — toggle nomeado, indicador `●`/`○` | — |
| `[⏎]` | **Todos** / **Executar** / **Visualizar** (ver 5.1.2) | declarativa por tela | executa a ação vinculada ao item sob o cursor ou sobre a seleção, conforme o tipo de tela | inativo quando não há alvo válido sob o cursor |
| específicos | (por classe) | condicional | chips próprios da classe — ver seção 5.2 | — |
| `[V]` | Verboso | condicional | classe/dados aceitam `tipo_exibicao: verboso` (só existe pra `console`, ver seção 3) | — |
| `[?]` | Ajuda | declarativa por tela; quando presente, último na ordem | — | sempre ativo |

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
(relatórios só-visualização usando `dashboard` como conteúdo principal, telas
de processo usando `corpo`) fica para o chat dedicado a `dashboard` — não foi
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
| **Aciona processo** | *(estrutura a definir)* | executa lógica sobre seleção/lote; estrutura formal pendente e fora do escopo da ADR-0007 |
| **Aciona tela** | texto, tecla, `tela_destino`, papel | abre outra tela (navegação) — ex.: `[\|] Estilo` abre a tela de seleção de estilo. Diferente de "aciona processo": não executa lógica de fundo, só troca de tela |

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
  - `lancador`: **pode ser linha única horizontal (fila) ou matriz de múltiplas
    colunas**, calculado automaticamente pela largura real do terminal
    (ADR-0001 — supera a regra anterior de "sempre coluna única, sem colunas";
    ver `docs/adr/ADR-0001-menu-suporta-matriz.md` e seção 12). Continua **sem paginação** mesmo em modo matriz —
    overflow em `lancador` não pagina (regra mantida). Regras completas de
    layout na seção 8.
  - `console`: colunar (modo normal, `n_col` ajustável) ou tabular (modo
    verboso, largura de coluna calculada por conteúdo, texto longo quebra
    dentro da coluna).
- **Overflow**: nunca existe scroll. Conteúdo que excede o espaço
  disponível sempre pagina (exceto `lancador`, ver acima). Espaço sobrando é
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
objeto dashboard, corpo e "linha acima da barra_de_menus" costumam coincidir
visualmente, mas isso é coincidência, não regra: o indicador pertence à
borda do corpo, nunca ao layout geral da tela.

**Exceção — dashboard presente**: o objeto dashboard não herda nem desloca o
indicador de página. Ele nunca aparece na borda do dashboard, mesmo o dashboard
estando mais próximo da barra_de_menus. O indicador continua preso à
borda do corpo paginado, mesmo com dashboard ocupando o espaço abaixo dele.

**Lado a lado**: cada corpo exibe sua própria paginação, ancorada à
direita **dentro da própria borda**, independente de qual lado da tela
aquele corpo ocupa fisicamente.

**Ainda não definido (adiado, sem caso de uso real ainda)**: combinação de
layout lado a lado com objeto dashboard presente ao mesmo tempo.

---

## 7. Cabeçalho

Região fixa superior de toda tela do sistema (ver seção 2). Sempre existe;
nunca ausente, condicional ou opcional.

O `cabecalho` não é corpo, não é `dashboard`, não é `lancador` e não é
`barra_de_menus`. Não herda regras de layout de nenhuma dessas regiões.

### 7.1 Campos textuais

O `cabecalho` tem exatamente dois campos textuais:

| Campo | Função | Restrição |
|---|---|---|
| `titulo` | Texto curto de identificação da tela | Sem limite de caracteres definido — o estilo de apresentação é configurável via `config/cabecalho.json` |
| `descricao` | Texto longo de contextualização | Máximo de 200 caracteres (`max_caracteres` em `config/cabecalho.json`) |

**Os textos concretos de `titulo` e `descricao` pertencem à classe/tela**,
não ao JSON de configuração global. A classe declara o conteúdo textual;
`config/cabecalho.json` guarda somente os parâmetros de apresentação.

### 7.2 Schema de apresentação — `titulo`

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `posicao` | `esquerda` \| `centro` \| `direita` | Posição horizontal do bloco do título na linha da borda superior |
| `recuo_lateral` | inteiro ≥ 0 | Distância em caracteres do canto esquerdo (posicao `esquerda`) ou do canto direito (posicao `direita`). Ignorado quando `posicao = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto do `titulo` antes da renderização |
| `formato_na_borda` | `com_espacos_laterais` | Estilo de integração do título à linha da borda superior |

**Semântica de `formato_na_borda`:**

- `com_espacos_laterais`: o bloco exibido é `borda + espaço + título + espaço + borda`.

**Semântica de `posicao`:**

- `esquerda`: o bloco do título inicia a `recuo_lateral` caracteres do canto esquerdo da borda.
- `centro`: o bloco do título fica centralizado na linha da borda superior; `recuo_lateral` é ignorado.
- `direita`: o bloco do título termina a `recuo_lateral` caracteres do canto direito da borda.

### 7.3 Schema de apresentação — `descricao`

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `max_caracteres` | inteiro > 0 | Número máximo de caracteres; texto que exceder é truncado antes da renderização |
| `alinhamento` | `esquerda` \| `centro` \| `direita` | Alinhamento horizontal do texto da descrição |
| `recuo` | inteiro ≥ 0 | Distância em caracteres da borda esquerda (alinhamento `esquerda`) ou da borda direita (alinhamento `direita`). Ignorado quando `alinhamento = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto da `descricao` antes da renderização |

**Semântica de `alinhamento`:**

- `esquerda`: a descrição começa a `recuo` caracteres da borda esquerda.
- `centro`: a descrição fica centralizada na largura disponível; `recuo` é ignorado.
- `direita`: a descrição termina a `recuo` caracteres da borda direita.

### 7.4 Parametrização externa — `config/cabecalho.json`

Seguindo a política da seção 0: os parâmetros de apresentação do `cabecalho`
vivem em `config/cabecalho.json`, não hardcoded. Esta seção define o schema e
a semântica; o arquivo guarda os valores concretos de apresentação.

O arquivo não contém textos concretos de telas (valores de `titulo` e
`descricao`) — esses pertencem a cada classe/tela.

---

## 8. Corpo tipo `lancador`

Aplica-se a qualquer corpo cujo tipo de conteúdo seja `lancador` (ver seção
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
  específica (não do maior item de todo o `lancador`).
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
   aproximação pelo maior item do `lancador` inteiro.

Em ambas as etapas, depois de achar a distribuição que cabe, os vãos
esticam até o máximo pra preencher a sobra (ver 8.1). **Sem teto absoluto
de colunas** — o único limite é a largura disponível.

**Número mínimo de linhas**: 1 (configurável via `config/lancador.json`, ver
8.4).

### 8.4 Parametrização externa — `config/lancador.json`

Decisão desta sessão: as regras de vão, alinhamento e linhas mínimas do
corpo tipo `lancador` vivem num arquivo de configuração próprio, não
hardcoded — mesmo espírito da "proibição de hardcoding" já usada no schema
de estilo (seção 1, `contrato_estilo.md`). Caminho do arquivo:
`config/lancador.json` (ver política da seção 0). Não criar
`config/layout_lancador.json`.

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

## 9. Objeto `dashboard` — definição e regras de layout

`dashboard` é definido como tipo mínimo (ADR-0008):

- não navegável por `[✥]`;
- não obrigatório;
- possui moldura própria;
- aceita posicionamento dentro do corpo conforme configuração da tela;
- sem conteúdo universal fixo.

`dashboard` não terá `config/dashboard.json` próprio. Cada instância de
`dashboard` é declarada pelo JSON da tela onde é usada. O código não deve
hardcodar conteúdo, composição ou campos de nenhuma instância de `dashboard`.

O usuário lê; não interage; não há cursor navegável por `[✥]`.

A estrutura de 8 campos de resumo + Total + 8 marcadores abaixo é o **draft
da instância de `dashboard` da tela raiz do Orquestrador**. Ela é exemplo
e instância conhecida; não define a classe universal `dashboard`.

**Alinhamento horizontal:** mesma regra do corpo tipo `lancador` (seção 8) —
coluna dimensionada pelo maior rótulo, alinhamento à esquerda dentro do
bloco. **Pendente de confirmação** (ver seção 11): o `lancador` adotou bloco
à esquerda com sobra à direita (ADR-0002) — falta decidir se o `dashboard`
acompanha essa mudança ou mantém centralização.

**Alinhamento vertical:** mesma regra do corpo tipo `lancador` (seção 8), com
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

## 10. Tiling (composição de múltiplos elementos do corpo)

- Quantidade de corpos (1 / múltiplos) é declarada pela classe de tela
  (seção 3).
- Se múltiplos, o **arranjo** (`vertical`/`horizontal` — terminologia final,
  ADR-0011; `sobreposto`/`lado a lado` são aliases transicionais) pode ser
  **fixado pela própria classe** — nesse caso, a preferência global do
  usuário é ignorada para aquela tela.
- Se a classe não fixar arranjo, usa-se o campo `tiling` do estilo (seção
  1.4) como default — escolha manual do usuário, sem largura mínima de
  segurança que force sobreposto.
- Em modo lado a lado (2 colunas), o espaço horizontal se distribui em 3
  vãos, igualmente: borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda.
- A posição do objeto **dashboard** é controlada pela estrutura declarativa
  geral do `corpo` (ADR-0010, 2026-07-08). `dashboard` é elemento funcional
  do corpo como `console` e `lancador`; o campo `posicao_dashboard` como
  eixo separado está descontinuado.
- Quando há múltiplos corpos, `[⇆]` alterna o foco de interação entre eles
  (ver seção 5.1).
- **Pendente** (já registrado seção 6.1): combinação de lado a lado com
  objeto dashboard presente ao mesmo tempo.

## 11. Pendências em aberto

Itens que ainda não têm decisão do usuário:

- **Regras de ajuste do `tx`** (corpo tipo `console`, seção 4.3): quando o
  texto do item não cabe no espaço disponível — truncar com reticências,
  quebrar em múltiplas linhas, ou outra estratégia. Ainda não definidas.
- **`popup_execucao`** (estrutura nova, não é corpo/dashboard/barra_de_menus):
  janela temporária de saída de execução de script. Mencionada nesta
  sessão, usuário já tem ideias mas decidiu tratar depois de fechar o que
  já estava em andamento. Precisa de regras próprias (tamanho, posição,
  fechamento, bloqueio de tela por trás, borda própria do schema de
  estilo).
- **Impacto no alinhamento do objeto `dashboard`**: ver seção 9 — falta
  confirmar se acompanha a mudança do `lancador` (centralizado → bloco à esquerda com sobra à direita) ou
  segue centralizado como o `console` (seção 4.3). Tratar junto do chat
  dedicado a `dashboard`.
- **Segunda pauta de "estilos de exibição de dados no corpo"**:
  mencionada pelo usuário nesta sessão, ainda não descrita.
- **`config/lancador.json` — campos de navegação**: vãos, alinhamento e número
  mínimo de linhas já formalizados via ADR-0003 e `contrato_composicao_corpo.md`
  (seção 5.2). Pendente apenas a formalização dos campos de `navegacao` em
  `config/lancador.json`, que deve aguardar o contrato de mecanismos de
  seleção/navegação.
- **Reorganização corpo × dashboard** (relatórios só-visualização usando `dashboard`
  como conteúdo principal, telas de processo usando `corpo`): mencionada
  nesta sessão, explicitamente adiada para o chat dedicado a `dashboard` — não
  é lacuna, é escopo remarcado de propósito.

### Levantamento do Codex — `teste_classe_c.py` / `teste_combo.py` (referência, não decisão)

Resumo do levantamento neutro já recebido, mantido aqui como evidência de
apoio (não substitui decisão do usuário):

- Preenchimento de matriz: coluna-a-coluna (`_grade_coluna_continua`,
  `_colunar_ajustado`), com exceção especial para o antigo menu de 2 linhas.
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
- Combinação de layout lado a lado com objeto dashboard presente ao mesmo
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

---

## 13. Decisão terminológica — `lancador` (antigo corpo tipo `menu`)

**Data da decisão:** 2026-07-06

O tipo de objeto do corpo até aqui chamado de `menu` passa a ser chamado
formalmente de **`lancador`**. Em texto humano, pode aparecer como "lançador".

### Motivação

O termo `menu` criava contaminação terminológica com `barra_de_menus`:
- `barra_de_menus` é a região fixa da tela (contrato: `contrato_barra_de_menus.md`, `ativo`).
- O antigo `menu` era um **membro do corpo** — não uma região da tela.

Com `barra_de_menus` já formalizada e fechada, manter `menu` como nome do
tipo de objeto tornava ambígua qualquer referência genérica a "menu" no
sistema. `lancador` é um nome sem colisão.

### Desambiguação de termos

| Termo | O que é | Status |
|---|---|---|
| `lancador` | membro do corpo; caixa com título e itens `chip + texto + tela_destino` | **ativo** — termo canônico a partir desta decisão |
| `menu` (corpo) | nome antigo do tipo `lancador` | **descontinuado** — presente nos artefatos existentes por rastreabilidade; não usar em novas decisões |
| `barra_de_menus` | região fixa da tela — não é membro do corpo | **ativo**, fechado — não reabrir |

### Estrutura conceitual mínima do `lancador`

O `lancador` é uma instância declarada pelo JSON da tela. Cada instância tem
título e uma lista de itens. Cada item tem exatamente três partes:

| Parte | Descrição |
|---|---|
| `chip` | identificador visual de ação (ex.: `[A]`) |
| `texto` | rótulo do item — **máximo 15 caracteres** |
| `tela_destino` | campo formal que identifica a tela a ser aberta |

**Regra do texto:** texto acima de 15 caracteres é **rejeitado em
verificação** — não é truncado nem abreviado. Cabe à classe de tela garantir
o limite antes de declarar o `lancador`.

**Papel de cada item**: aciona navegação para outra tela (`tela_destino`).
Não executa processo, não filtra dado, não altera estado.

**Mudança declarativa**: adicionar item ao `lancador`, mudar texto, mudar
chip/letra ou mudar `tela_destino` deve ser alteração declarativa no JSON da
tela. O código apenas percorre a lista de itens declarada.

### Escopo desta decisão

Fechado:
- O nome formal do tipo é `lancador`.
- A estrutura mínima (título + itens `chip + texto + tela_destino`) está definida.
- O limite de 15 caracteres para `texto` é absoluto e verificado (não truncado).

Fechado nesta etapa:
- O nome do arquivo de configuração é **`config/lancador.json`** (decisão fechada em 2026-07-06).

Concluído — DOC-0008:
- Contrato próprio do `lancador` criado em
  `docs/contratos/contrato_lancador.md`; arquivo canônico inicial criado em
  `config/lancador.json`.

Concluído — DOC-0009:
- Artefatos vigentes migrados para `lancador`; `config/lancador.json` é o
  arquivo canônico. `config/layout_menu.json` permanece apenas como artefato
  obsoleto/transicional de rastreabilidade.
