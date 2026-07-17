---
name: nomenclatura-sistema-novo
description: Glossario consolidado de termos do sistema novo, base para os contratos de estilo, composicao de corpo e barra_de_menus
metadata:
  type: nomenclatura
  scope: sistema_novo
  status: parcial
  origem_especificacao: usuario_sessao_2026-07-05
  atualizado_em: 2026-07-14
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
`config/elementos/lancador.json`; não criar `config/layout_lancador.json`.

**Localização**: todos os JSON de configuração ficam em `config/`, na raiz do
Orquestrador, irmã de `docs/` — nunca dentro de `docs/` (que é documentação
neutra, sem dado de produção, ver `docs/INDICE.md`).

**Política estrutural da ADR-0021 (2026-07-14)**:

| Termo | Definição |
|---|---|
| motor compartilhado | `tela/`; contém conceitualmente loader, modelo, renderizador e contratos genéricos de tela. É reutilizado pela demonstração e pelo produto real. |
| aplicação demonstrativa | `demo/`; diretório futuro, ainda não criado, destinado a pontos de entrada, utilitários e testes exclusivos da demonstração. |
| produto real | Orquestrador operacional futuro, com telas declarativas diretamente em `config/telas/<id>.json` e ponto de entrada principal futuro `orquestrador.py`. |
| tela demonstrativa | Tela declarativa usada pela demonstração, sob a futura raiz `config/telas/demo/<id>.json`. |
| tela do produto real | Tela declarativa do Orquestrador real, sob `config/telas/<id>.json`. |
| raiz declarativa da demonstração | `config/telas/demo/`, futura raiz das telas demonstrativas. |
| raiz declarativa do produto | `config/telas/`, raiz reservada às telas do produto real. |

`tela/` é motor, não ponto de entrada demonstrativo. `demo/` é aplicação
demonstrativa futura, não uma segunda implementação de loader, modelo ou
renderizador. Diretórios como `config/layouts/` e `config/elementos/` agrupam
configuração global por função; não são tipos de elemento do corpo.

**Política da tela inicial real pela ADR-0022 (2026-07-14)**:

| Termo | Definição |
|---|---|
| ponto de entrada real | `orquestrador.py`; arquivo futuro diretamente na raiz, reservado ao produto real e reutilizador do motor compartilhado `tela/`. |
| tela inicial real | `config/telas/orquestrador.json`; arquivo futuro/reservado ao produto real, com identificador interno `orquestrador`. |
| identidade real | `orquestrador`; identidade exclusiva do produto real, distinta de `demo`. |
| corpo inicial real | Corpo da tela inicial real composto por `console` e `dashboard`, ambos estruturalmente presentes e sem entradas iniciais de dados reais ou demonstrativos. |
| barra mínima real | Instância de `barra_de_menus` da tela inicial real com `Esc`, `?` e acesso a estilos. O acesso a estilos não cria tela funcional, destino inexistente, alias ou fallback. |

`orquestrador.py` e `config/telas/orquestrador.json` não são tratados por esta
nomenclatura como arquivos já criados. A demonstração preserva a identidade
`demo` na futura raiz `config/telas/demo/`. Não há alias, fallback ou busca
ambígua entre `orquestrador` e `demo`.

**Status dos artefatos JSON (modelo ADR-0008):**

| Artefato | Papel no novo modelo | Status |
|---|---|---|
| `config/estilo.json` | Biblioteca global de aparência — mantida | ativo (seção 1) |
| `config/telas/orquestrador.json` | Futuro caminho reservado à tela inicial real do produto, com `id: "orquestrador"` | reservado pela ADR-0022; não materializado por esta etapa |
| `config/layouts/layout_dado.json` | Futuro caminho do artefato obsoleto/transicional — rastreabilidade da migração `dado` → `console` | obsoleto; não é fonte canônica |
| `config/layouts/layout_menu.json` | Futuro caminho do artefato obsoleto/transicional — rastreabilidade da migração `menu` → `lancador` | obsoleto; não é fonte canônica |
| `config/elementos/lancador.json` | Futuro caminho dos parâmetros do tipo `lancador` — a reavaliar/migrar conforme ADR-0008 e ADR-0021 | ativo transicional (seção 8.4) |
| `config/layouts/layout_console.json` | Futuro caminho dos parâmetros de layout do tipo `console` — a reavaliar/migrar conforme ADR-0008 e ADR-0021 | ativo transicional (seção 4.4) |
| `config/elementos/barra_de_menus.json` | Futuro caminho dos parâmetros de `barra_de_menus` — a reavaliar/migrar conforme ADR-0008 e ADR-0021 | ativo transicional (seção 5.1.3) |
| `config/elementos/cabecalho.json` | Futuro caminho dos parâmetros de apresentação do `cabecalho` — a reavaliar/migrar conforme ADR-0008 e ADR-0021 | ativo transicional (seção 7.4) |
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

**Controle de aliases (sanitização 2026-07-10)**: `sobreposto` e `lado_a_lado`
são preservados apenas como aliases transicionais literais (entre backticks) para
compatibilidade com JSONs/contratos legados:
- não são terminologia final;
- não devem ser usados como termos normativos em novos textos;
- novos handoffs devem usar `vertical` ou `horizontal`;
- H-0019 deve implementar `corpo.arranjo = "horizontal"`, não o alias transicional.

Escolha manual do usuário, não decisão automática por largura de
terminal. Não existe largura mínima de segurança que force arranjo `vertical` —
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
2. **Corpo**: estrutura variavel — pode ter mais de um objeto, em arranjo
   vertical ou horizontal, dependendo do tipo dos objetos e da configuração da tela.
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
- `dashboard` (zero ou mais), quando houver saída passiva formatada, como estado
  agregado, resumo ou progresso (ADR-0019, D7);
- chips específicos declarados pela classe de tela na `barra_de_menus`.

Chips específicos pertencem à `barra_de_menus`, nunca ao corpo. A classe de
tela declara sua existência; a `barra_de_menus` continua sendo espelho da
declaração, não fonte de decisão.

`lancador` não representa processamento. O `lancador` continua sendo navegação
para outras telas via `tela_destino`. Nenhuma regra de `[✥]` muda: `[✥]`
continua restrito a corpo tipo `console`.

Exemplo conceitual, não obrigatório: uma tela de processamento pode conter
`cabecalho`, corpo com `console` Lista, corpo com `console` Detalhe, corpo com
`console` Log se o log for navegável, `dashboard` (zero ou mais) de estado
agregado/resumo/progresso (ADR-0019, D7), e `barra_de_menus` com chips canônicos e chips
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
seção 8.3; valores no futuro caminho `config/elementos/lancador.json`.

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
daquele item (marcado ou não), os dois espaços coexistem em posições distintas
e adjacentes, não se sobrepõem entre si. (A sobreposição só acontecia na formulação antiga
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

### 4.4 Parametrização externa — `config/layouts/layout_console.json`

Seguindo a política da seção 0: os valores concretos e configuráveis do layout
do corpo tipo `console` vivem no futuro caminho
`config/layouts/layout_console.json`, não hardcoded. Esta seção define o schema
e a semântica; o arquivo guarda os dados.

`config/layouts/layout_dado.json` permanece apenas como artefato
obsoleto/transicional de rastreabilidade da migração `dado` → `console`; não é
fonte canônica nova.

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


### 5.1.3 Arquivo de dados — `config/elementos/barra_de_menus.json`

Seguindo a política da seção 0: a ordem canônica, os rótulos e o mapeamento
de cada chip para o eixo de composição que controla sua existência vivem em
`config/elementos/barra_de_menus.json`, não hardcoded. Esta seção do glossário
(5.1) define o que cada campo do JSON significa; o JSON guarda os valores.

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
- **Redimensionamento reativo da TUI (ADR-0017)**: o sistema detecta mudança de
  tamanho da janela do terminal via `SIGWINCH` e reage atualizando dimensões e
  redesenhando o quadro — sem reiniciar a sessão, sem usar `ncurses`/`curses`.
  A política normativa completa está em `contrato_tela_json.md` seção 24. Os
  termos específicos estão definidos na seção 6.2 abaixo.
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

**Arranjo horizontal**: cada corpo exibe sua própria paginação, ancorada à
direita **dentro da própria borda**, independente de qual lado da tela
aquele corpo ocupa fisicamente.

**Ainda não definido (adiado, sem caso de uso real ainda)**: combinação de
`corpo.arranjo = "horizontal"` com objeto `dashboard` presente ao mesmo tempo.

### 6.2 Termos do redimensionamento reativo da TUI (ADR-0017, 2026-07-11)

Os termos abaixo são a autoridade terminológica para contratos, handoffs e
código relacionados ao redimensionamento reativo. A política normativa completa
está em `contrato_tela_json.md` seção 24.

| Termo | Definição |
|---|---|
| `redimensionamento reativo da TUI` | Capacidade de detectar mudança de tamanho da janela do terminal em sessão TTY ativa (via `SIGWINCH`), obter novo par válido de dimensões e redesenhar o quadro sem encerrar a sessão |
| `SIGWINCH` | Sinal POSIX recebido quando a janela do terminal muda de tamanho; gatilho normativo do redimensionamento reativo em sessão TTY ativa |
| `ioctl(TIOCGWINSZ)` | Chamada de sistema que obtém as dimensões atuais da janela do terminal; fonte primária normativa de largura e altura durante sessão TTY |
| `par de dimensões válido` | Par (largura, altura) em que ambos os valores estão presentes, podem ser interpretados como inteiros e são maiores que zero; único estado que pode ser aplicado ao renderer |
| `últimas dimensões válidas` | O par (largura, altura) mais recente que satisfez os critérios de validade; conservado quando a obtenção pós-`SIGWINCH` não produz par válido; não é substituído pelo fallback fixo durante sessão já ativa |
| `quadro mínimo de terminal pequeno` | Quadro substituto exibido quando as dimensões são válidas mas insuficientes para a tela normal; comunica inequivocamente "terminal pequeno demais"; cabe nas dimensões atuais; é substituído automaticamente pela tela normal quando dimensões suficientes forem restauradas |

**Distinções obrigatórias (não colapsam)**:

| Termo específico | Significado | Não confundir com |
|---|---|---|
| `redimensionamento reativo da TUI` | Detecção de `SIGWINCH` e redesenho com novo par válido em sessão TTY | `corpo.arranjo` ou `tiling` (composição declarativa, não sessão TTY) |
| `par de dimensões válido` | Par (largura > 0, altura > 0) de fonte normativa | Par parcial ou zerado — não aplicável ao renderer |
| `últimas dimensões válidas` | Par conservado durante sessão quando nova obtenção falha | Fallback fixo `(80, 24)` — este só se aplica na inicialização sem fontes válidas |
| `ocupacao_vertical_terminal` | Preenchimento da altura disponível pelo renderer (ADR-0013) | `corpo.arranjo = "vertical"` (composição dos elementos do corpo, ADR-0011) |
| `corpo.arranjo` | Ordem/composição dos elementos do corpo declarada no `tela.json` | Resultado visual do redimensionamento — o redimensionamento não altera `corpo.arranjo` |
| `tiling` | Preferência de arranjo do estilo ou fixação pela classe de tela | Resultado de redimensionamento — o redimensionamento não altera `tiling` |
| `quadro mínimo de terminal pequeno` | Aviso exibido quando tela não cabe mas sessão permanece ativa | Encerramento da sessão TUI ou propagação de classe de erro como saída normal |

**Regras normativas derivadas da ADR-0017**:

- Redimensionamento não altera `corpo.arranjo`, `tiling`, chips nem elementos declarados.
- Redimensionamento não cria fallback de composição baseado em largura ou altura.
- Par inválido não é aplicado ao renderer; `últimas dimensões válidas` são mantidas.
- Fallback fixo `(80, 24)` somente na inicialização sem fontes válidas; nunca substitui
  `últimas dimensões válidas` durante sessão ativa.
- `quadro mínimo de terminal pequeno` não encerra a sessão; recuperação é automática.
- Comportamento não-TTY permanece inalterado; `SIGWINCH` não é tratado fora de sessão TTY.
- `ncurses`, `curses`, `textual` e `rich` permanecem proibidos para esta capacidade.

### 6.3 Grandezas de largura do `lancador` e gatilho por área interna (ADR-0023)

Os termos abaixo são a autoridade terminológica para a largura mínima funcional
do `lancador` e para o gatilho do quadro mínimo global por insuficiência de
área interna. A política normativa completa está em
`docs/contratos/contrato_lancador.md` seção 6.7 e na ADR-0023.

| Termo | Definição |
|---|---|
| `area_lancador_w` | Largura total efetivamente alocada ao elemento `lancador` pela composição — inclui bordas e padding externos da caixa completa |
| `lancador_caixa_min_w` | Largura mínima total da caixa do `lancador`; inclui as unidades estruturais obrigatórias (bordas e padding externos). Relação: `lancador_caixa_min_w = coluna_minima_content_w + largura_estrutural_da_caixa` |
| `coluna_minima_content_w` (largura mínima funcional do `lancador`) | Largura mínima do conteúdo necessária para representar integralmente uma coluna válida completa, sem bordas nem padding externo da caixa; é a menor largura de conteúdo para a qual existe ao menos uma distribuição válida dos itens declarados |
| `coluna válida completa` | Uma coluna do `lancador` cujo conteúdo — chip, vão e texto — cabe integralmente na largura disponível, com todos os itens visíveis e sem truncamento, overflow, omissão ou paginação |
| `content_w` | Largura de conteúdo do `lancador`, obtida descontando bordas e padding externos de `area_lancador_w`; é o domínio de comparação com `coluna_minima_content_w` |
| `quadro mínimo global acionado por inviabilidade do lancador` | O mesmo `quadro mínimo de terminal pequeno` (ADR-0017, seção 6.2) acionado quando `area_lancador_w < lancador_caixa_min_w`, mesmo que `terminal_w` seja maior; o escopo visual é idêntico e global — toda a tela ou sessão TUI normal é substituída |
| `fallback local do lancador` | **Proibido.** Nenhum estado visual, mensagem, truncamento, omissão ou variante restrita à caixa ou área do `lancador` é permitido quando a coluna mínima não couber. O único resultado admissível é o quadro mínimo global. |
| `recuperação automática por redesenho` | A cada redesenho, o renderer reavalia as grandezas de largura; quando `area_lancador_w >= lancador_caixa_min_w`, o quadro mínimo desaparece e a tela normal é reconstruída sem ação do usuário |

**Distinções obrigatórias (não colapsam)**:

| Termo | Significado | Não confundir com |
|---|---|---|
| `area_lancador_w` | Largura total da caixa alocada ao `lancador` (inclui bordas/padding) | `coluna_minima_content_w` (grandeza de conteúdo, exclui bordas/padding) |
| `lancador_caixa_min_w` | Largura mínima da caixa do `lancador` (inclui bordas/padding) | `coluna_minima_content_w` (largura de conteúdo, exclui bordas/padding) |
| `coluna_minima_content_w` | Largura mínima do conteúdo para uma coluna válida (exclui bordas/padding) | `area_lancador_w` ou `lancador_caixa_min_w` (são larguras de caixa) |
| `terminal_w` | Largura total do terminal ou viewport | Qualquer grandeza interna do `lancador` — não comparável diretamente |
| `quadro mínimo global` | Substitui integralmente toda a tela normal | `fallback local do lancador` — este é proibido |

**Regras normativas derivadas da ADR-0023**:

- `coluna_minima_content_w` é calculada a partir dos parâmetros de `config/elementos/lancador.json`; nenhum valor é hardcoded.
- A comparação normativa usa grandezas no mesmo domínio: `content_w` contra `coluna_minima_content_w` (domínio do conteúdo), ou `area_lancador_w` contra `lancador_caixa_min_w` (domínio da caixa).
- É proibido comparar `terminal_w` contra `coluna_minima_content_w`.
- É proibido comparar `area_lancador_w` contra `coluna_minima_content_w` sem converter bordas e padding.
- O gatilho por `area_lancador_w < lancador_caixa_min_w` aciona o mesmo estado canônico global da ADR-0017, com o mesmo alcance visual.
- A regra aplica-se exclusivamente ao `lancador`; não é criada regra genérica de falha global para outros componentes sem autoridade explícita.
- A recuperação é automática: a cada redesenho, quando `area_lancador_w >= lancador_caixa_min_w`, o quadro mínimo desaparece e a tela normal é reconstruída.

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
| `titulo` | Texto curto de identificação da tela | Sem limite de caracteres definido — o estilo de apresentação é configurável via `config/elementos/cabecalho.json` |
| `descricao` | Texto longo de contextualização | Máximo de 200 caracteres (`max_caracteres` em `config/elementos/cabecalho.json`) |

**Os textos concretos de `titulo` e `descricao` pertencem à classe/tela**,
não ao JSON de configuração global. A classe declara o conteúdo textual;
`config/elementos/cabecalho.json` guarda somente os parâmetros de apresentação.

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

### 7.4 Parametrização externa — `config/elementos/cabecalho.json`

Seguindo a política da seção 0: os parâmetros de apresentação do `cabecalho`
vivem no futuro caminho `config/elementos/cabecalho.json`, não hardcoded. Esta
seção define o schema e a semântica; o arquivo guarda os valores concretos de
apresentação.

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

**Número mínimo de linhas**: 1 (configurável via
`config/elementos/lancador.json`, ver 8.4).

### 8.4 Parametrização externa — `config/elementos/lancador.json`

Decisão desta sessão: as regras de vão, alinhamento e linhas mínimas do
corpo tipo `lancador` vivem num arquivo de configuração próprio, não
hardcoded — mesmo espírito da "proibição de hardcoding" já usada no schema
de estilo (seção 1, `contrato_estilo.md`). Caminho do arquivo:
`config/elementos/lancador.json` (ver política da seção 0). Não criar
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
  ADR-0011; `sobreposto`/`lado_a_lado` são aliases transicionais) pode ser
  **fixado pela própria classe** — nesse caso, a preferência global do
  usuário é ignorada para aquela tela.
- Se a classe não fixar arranjo, usa-se o campo `tiling` do estilo (seção
  1.4) como default — escolha manual do usuário, sem largura mínima de
  segurança que force arranjo `vertical`.
- Em `corpo.arranjo = "horizontal"`, o espaço horizontal é **particionado de forma
  contígua** entre os filhos diretos do container — sem vão externo entre
  eles (ADR-0015, 2026-07-10). A área de um filho termina imediatamente onde
  a do próximo começa; não existe espaço entre eles. A regra anterior de
  "3 vãos iguais" foi supersedida pela ADR-0015.
- A posição do objeto **dashboard** é controlada pela estrutura declarativa
  geral do `corpo` (ADR-0010, 2026-07-08). `dashboard` é elemento funcional
  do corpo como `console` e `lancador`; o campo `posicao_dashboard` como
  eixo separado está descontinuado.
- Quando há múltiplos corpos, `[⇆]` alterna o foco de interação entre eles
  (ver seção 5.1).
- **Pendente** (já registrado seção 6.1): combinação de `corpo.arranjo = "horizontal"`
  com objeto `dashboard` presente ao mesmo tempo.

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
- **`config/elementos/lancador.json` — campos de navegação**: vãos, alinhamento e número
  mínimo de linhas já formalizados via ADR-0003 e `contrato_composicao_corpo.md`
  (seção 5.2). Pendente apenas a formalização dos campos de `navegacao` em
  `config/elementos/lancador.json`, que deve aguardar o contrato de mecanismos
  de seleção/navegação.
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
- Resize: não há resize real por terminal no legado (arquivo legado homônimo
  `orquestrador.py`, distinto do futuro ponto de entrada real da ADR-0022, lia
  `shutil.get_terminal_size` no render, mas sem handler de `SIGWINCH`).
- Bordas incompletas: preenchidas com célula vazia (`None` / string vazia
  + `rstrip()`).

Itens adiados intencionalmente (não são lacuna, são decisão de adiar):

- Relação entre `[#]` (filtro de grupo) e `[␣]` (toggle de seleção) — ver
  seção 4.
- Estrutura do chip "aciona processo" — ver seção 5.2, será extraída do código
  legado homônimo `orquestrador.py` quando o primeiro caso concreto for definido,
  separando lógica de processo de código de exibição (`print`) misturado.
- Combinação de `corpo.arranjo = "horizontal"` com objeto `dashboard` presente
  ao mesmo tempo — ver seção 6.1, sem caso de uso real ainda.

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
- O nome histórico do arquivo de configuração foi **`config/lancador.json`** (decisão fechada em 2026-07-06), parcialmente atualizado pela ADR-0021 para o futuro caminho `config/elementos/lancador.json`.

Concluído — DOC-0008:
- Contrato próprio do `lancador` criado em
  `docs/contratos/contrato_lancador.md`; arquivo canônico inicial criado em
  `config/lancador.json`.

Concluído — DOC-0009:
- Artefatos vigentes migrados para `lancador`; `config/lancador.json` foi o
  arquivo canônico inicial. Pela ADR-0021, o futuro caminho previsto é
  `config/elementos/lancador.json`. `config/layouts/layout_menu.json` permanece
  apenas como artefato obsoleto/transicional de rastreabilidade.

---

## 14. Composição hierárquica e distribuição de área do corpo (ADR-0015)

A ADR-0015 (2026-07-10) estabelece as definições normativas do sistema de
composição hierárquica do corpo. Esta seção é a referência terminológica
canônica; a especificação completa com exemplos está na ADR-0015 e no
`contrato_composicao_corpo.md` (v0.3).

1. **Corpo como árvore de composição** — o corpo é modelado como árvore, não
   lista plana de elementos.
2. **Profundidade contada por níveis de grupos** — a profundidade hierárquica
   é contada exclusivamente pelo aninhamento de nós estruturais `grupo`
   (ADR-0019, D1). O corpo raiz não conta como nível de grupo.
3. **Nível de grupo 1** — um `grupo` filho direto de `corpo.elementos[]` está
   no nível de grupo 1.
4. **Nível de grupo 2** — um `grupo` filho de um grupo do nível 1 está no
   nível de grupo 2.
5. **Nível de grupo 3 — profundidade máxima** — um `grupo` filho de um grupo
   do nível 2 está no nível de grupo 3, que é o máximo permitido (ADR-0019,
   D2). Estruturas com grupo no nível 4 ou superior são rejeitadas com erro
   estrutural determinístico. Elementos funcionais dentro de um grupo do
   nível 3 não constituem nível 4 (ADR-0019, D3).
6. **Grupo como nó estrutural** — `grupo` é nó estrutural de composição;
   não é tipo funcional.
7. **Grupo não tem borda própria nem conteúdo próprio** — não tem título
   visual, moldura, ação, item, origem de dados ou `tela_destino`.
8. **Elementos funcionais** — `console`, `dashboard` e `lancador` são os três
   tipos funcionais válidos; a lista é fechada.
9. **Arranjo pertence ao container** — cada container (`corpo` ou `grupo`)
   declara o `arranjo` dos seus filhos diretos.
10. **Distribuição pertence ao container** — `distribuicao` é atributo do
    container, não do filho.
11. **Distribuição reparte área entre filhos diretos** — somente filhos
    imediatos são contados; netos não entram na contagem.
12. **Arranjo horizontal organiza os filhos horizontalmente** —
    `arranjo = horizontal` dispõe os filhos no eixo horizontal; a alocação
    proporcional de colunas de caracteres entre eles ocorre apenas quando o
    mesmo container possui `distribuicao` explícita.
13. **Arranjo vertical organiza os filhos verticalmente** —
    `arranjo = vertical` dispõe os filhos no eixo vertical; a alocação
    proporcional de linhas entre eles ocorre apenas quando o mesmo container
    possui `distribuicao` explícita.
14. **Distribuição aloca área, não apenas conteúdo** — a área é reservada
    independentemente do conteúdo do filho.
15. **Sobra horizontal vira espaços dentro da área alocada** — colunas
    excedentes são preenchidas com espaços; a largura da faixa é preservada.
16. **Sobra vertical vira linhas em branco dentro da área alocada** — linhas
    excedentes são adicionadas como linhas em branco; a altura da faixa é
    preservada.
17. **Percentual deve somar 100** — soma diferente de 100 é erro de
    configuração.
18. **Fração usa pesos positivos e denominador implícito pela soma dos pesos**
    — `[1, 1, 1]` resulta em `1/3`, `1/3`, `1/3`; `[2, 1]` resulta em
    `2/3`, `1/3`.
19. **Modos de distribuição previstos** — `igual`, `percentual`, `fracao`,
    `restrito`, `dinamico`.
20. **Arredondamento usa maiores restos, de forma determinística** — soma
    final deve ser exatamente igual à área disponível; empates resolvidos
    pela ordem declarada em `elementos[]`.
21. **Contato entre áreas de filhos é contíguo, sem vão externo** — a área de
    um filho termina imediatamente onde a do próximo começa.
22. **`ajustado_ao_conteudo` é dimensão preferida, não dimensão mínima
    absoluta** — permite combinar `preferido = conteudo` com `maximo`
    sem contradição.
23. **Paginação ocorre dentro da área alocada** — o elemento pagina
    internamente sem transbordar para a área de outro filho.
24. **Terminal pequeno tem política determinística futura** — não existe
    comportamento inventado; nenhum fallback silencioso é permitido.
25. **Sincronização automática de cortes entre grupos no mesmo nível** —
    grupos irmãos com mesma assinatura de restrições têm cortes
    sincronizados automaticamente (conceito ADR-0015; mecanismo explícito
    é extensão futura).

### 14.1 Semântica da ausência de distribuição e alocação vertical (ADR-0018)

A ADR-0018 (2026-07-11) substitui parcialmente a ADR-0015 **somente** no ponto em
que a ausência de `distribuicao` era tratada como equivalente ao modo `igual`. A
composição hierárquica, os modos e o arredondamento da seção 14 permanecem
vigentes; muda apenas a semântica da ausência e a localização da sobra na
distribuição explícita. Termos específicos completos, sem sinônimos novos:

| Termo específico completo | Conceito | Não confundir com |
|---|---|---|
| `corpo.arranjo = "vertical"` | ordem/composição vertical dos filhos diretos do container (ADR-0011) | `ocupacao_vertical_terminal` nem `corpo.distribuicao` |
| `ocupacao_vertical_terminal` | preenchimento da altura da janela pelo renderer (ADR-0013) | `corpo.arranjo = "vertical"` nem `corpo.distribuicao` |
| `corpo.distribuicao` | repartição proporcional da área útil entre os filhos diretos quando declarada (ADR-0015/ADR-0018) | `corpo.arranjo` (ordem) nem `ocupacao_vertical_terminal` (preenchimento) |

Regras normativas derivadas da ADR-0018:

- **Arranjo não é distribuição** — `corpo.arranjo = "vertical"` ordena os filhos
  verticalmente; por si só **não** reparte proporcionalmente a altura nem implica
  modo `igual`. `arranjo` permanece válido sem `corpo.distribuicao`.
- **Ausência de `corpo.distribuicao` ≠ modo `igual`** — quando `corpo.distribuicao`
  não é declarada, cada filho usa sua **altura natural** e a ocupação integral da
  área deve ser garantida pelos elementos visuais conforme DA-01 a DA-04 (ADR-0024):
  com um único descendente visual, ele ocupa toda a área (DA-01); com múltiplos
  elementos no mesmo eixo, a composição é inválida (DA-02). Não há repartição
  proporcional automática. A ausência **não** é fallback do modo `igual`.
- **Modo `igual` é explícito** — `igual` divide a área igualmente entre filhos
  diretos apenas quando declarado; não é o significado implícito da ausência.
- **Distribuição explícita aloca `área alocada`** — com `corpo.distribuicao`
  declarada, a altura útil é repartida integralmente entre os filhos diretos; a
  distribuição aloca **área**, não apenas o tamanho do conteúdo natural.
- **Preenchimento interno quando há distribuição explícita** — a cota excedente ao
  conteúdo vira linhas em branco **dentro** da moldura de cada filho; a sobra
  **não** fica acumulada externamente abaixo do último filho.
- **`fracao` são pesos genéricos** — qualquer vetor de pesos positivos é aceito;
  `[1,1,1]`, `[2,1,2]`, `[1,3,1]`, `[5,2,7]` são exemplos não exaustivos; nenhum
  vetor concreto é default ou hardcode do renderer.
- **Conteúdo maior que a cota é lacuna externa** — altura mínima, overflow,
  truncamento, paginação, rejeição e degradação permanecem fora de escopo da
  ADR-0018; um vetor válido não se torna inválido porque o conteúdo não cabe em
  altura pequena.

A ADR-0013 (cláusulas 1–3, 5–10) e a ADR-0017 permanecem preservadas: a altura
útil repartida pela distribuição é obtida pelo mecanismo da ADR-0017; a ocupação
integral da área na ausência de distribuição deve ser garantida por elementos
visuais conforme DA-01 a DA-04 da ADR-0024 — não por preenchimento externo vazio.
A especificação normativa completa está na ADR-0018, na ADR-0024 e em
`contrato_composicao_corpo.md` seções 4.8, 4.9, 5.7 a 5.9 e 10.

---

### 14.2 Glossário da proibição de preenchimento vazio externo do corpo (ADR-0024)

A ADR-0024 (2026-07-15) proíbe o preenchimento externo vazio do corpo e introduz
os termos normativos abaixo. Esta seção é a referência terminológica canônica;
a especificação normativa completa está na ADR-0024 e em
`contrato_composicao_corpo.md` seção 5.7.

| Termo | Definição normativa | Não confundir com |
|---|---|---|
| **elemento visual** | Nó de corpo do tipo `console`, `dashboard` ou `lancador` — taxonomia fechada; única categoria que pode concretizar ocupação visual da área do corpo (ADR-0024) | `grupo` (estrutural, não visual) |
| **grupo** | Nó estrutural de agrupamento; não é elemento visual; não pode justificar área vazia; toda área atribuída a ele deve ser repassada aos descendentes visuais (DA-03) | elemento visual; não satisfaz ocupação sozinho |
| **espaço externo proibido** | Linhas, colunas ou células fora das molduras dos elementos visuais, pertencentes apenas ao corpo ou a container estrutural; inserção pelo renderer é proibida pela ADR-0024 | espaço interno (preenchimento dentro da moldura de um elemento visual) |
| **espaço interno** | Linhas em branco **dentro** da moldura de um elemento visual, resultado de distribuição explícita com cota maior que o conteúdo — permitido e distinto do espaço externo | espaço externo proibido |
| **cardinalidade unitária** | Situação em que um corpo ou container tem exatamente um descendente visual; esse elemento ocupa integralmente toda a área disponível mesmo sem `distribuicao` declarada — não equivale a `distribuicao: igual` (DA-01) | modo `igual`; distribuição implícita |
| **composição inválida** | Configuração em que dois ou mais elementos disputam o mesmo eixo sem `distribuicao` declarada, ou em que o invariante de ocupação visual integral não pode ser satisfeito; deve ser rejeitada explicitamente, sem fallback silencioso (DA-02, DA-04) | ausência de `distribuicao` com descendente único (DA-01, que é válida) |

Regras normativas derivadas da ADR-0024:

- **Elemento visual é o único que justifica área** — `console`, `dashboard` e
  `lancador` são os únicos tipos de corpo que podem concretizar a ocupação visual
  da área; `grupo` não satisfaz esse critério.
- **Toda área do corpo deve pertencer a elemento visual** — nenhuma linha, coluna
  ou célula entre `cabecalho` e `barra_de_menus` pode ficar atribuída apenas ao
  corpo ou a container estrutural; o renderer não completa com linhas externas.
- **DA-01 não é distribuição implícita** — um único descendente visual ocupa toda
  a área por cardinalidade unitária, não porque o renderer aplicou `igual`
  silenciosamente.
- **DA-04 é rejeição, não fallback** — quando o invariante não pode ser satisfeito,
  a composição é rejeitada com erro identificável; sem distribuição implícita, sem
  escolha silenciosa, sem alteração automática do JSON.

---

## 15. Comportamento estrutural do `grupo` — `livre` e `matriz` (ADR-0020)

A ADR-0020 (2026-07-12) formaliza dois comportamentos estruturais do nó
`grupo`. Esta seção é a referência terminológica canônica; a especificação
normativa completa está na ADR-0020 e em `contrato_composicao_corpo.md`.

### 15.1 Seletor declarativo `estrutura`

O campo `estrutura` é o seletor canônico do comportamento de um nó `grupo`.

| Valor | Comportamento |
|---|---|
| `"livre"` | Comportamento hierárquico unidimensional existente — `arranjo` e `distribuicao` local por container |
| `"matriz"` | Comportamento bidimensional com grade comum, distribuições independentes por eixo e coordenadas explícitas de células |
| *(ausente)* | Equivale a `"livre"` — compatibilidade retroativa integral (D3) |

**Não usar como seletor**: `tipo` (já identifica o nó como `grupo`), `arranjo`
(já define o eixo de composição em `livre`), nem `modo` isoladamente (já
participa do schema de `distribuicao.modo`).

### 15.2 Comportamento `livre`

`estrutura: "livre"` nomeia o comportamento hierárquico atual do nó `grupo`.

Preserva integralmente:

- composição recursiva por containers;
- `arranjo` vertical ou horizontal;
- `distribuicao` local ao container (opcional);
- modos `igual`, `percentual`, `fracao`;
- ausência de `distribuicao` como construção orientada pelo conteúdo
  (ADR-0018 — não equivale ao modo `igual`);
- todos os JSONs ativos sem alteração.

A ausência de `estrutura` equivale a `livre` e **nunca** ativa `matriz`.

### 15.3 Comportamento `matriz` — matriz de grupos

`estrutura: "matriz"` define um comportamento declarativo bidimensional.

**Termo canônico**: `matriz de grupos` — especialização do nó `grupo` que
organiza os filhos diretos em uma grade bidimensional com grade comum de
coordenadas.

**Distinção obrigatória**: `matriz de grupos` (ADR-0020) não se confunde com:

- modo matriz do `lancador` (cálculo automático de colunas, ADR-0001 e
  seção 8.2 desta nomenclatura) — domínios distintos;
- navegação em grade 2D de `console` por `[✥]` (seção 4.1);
- qualquer uso anterior de "matriz" em menu, tabela ou item de corpo.

### 15.4 Termos da matriz de grupos

| Termo | Definição |
|---|---|
| `linha da matriz` | Faixa horizontal da grade; cada linha ocupa altura calculada pela distribuição de linhas |
| `coluna da matriz` | Faixa vertical da grade; cada coluna ocupa largura calculada pela distribuição de colunas |
| `célula da matriz` | Interseção de uma linha e uma coluna; contém exatamente um filho direto do grupo matricial |
| `coordenada explícita` | Par `(linha, coluna)` com índices iniciados em 1 que identifica unicamente uma célula na grade |
| `distribuição de linhas` | Campo `matriz.linhas.distribuicao` — distribui a altura do container entre as linhas; obrigatório em `estrutura: matriz` |
| `distribuição de colunas` | Campo `matriz.colunas.distribuicao` — distribui a largura do container entre as colunas; obrigatório em `estrutura: matriz` |
| `grade comum` | Única grade de coordenadas calculada para o container matricial, compartilhada por todas as células — bordas de células da mesma linha/coluna são sempre alinhadas |
| `cobertura completa` | Restrição de que toda coordenada válida deve ser preenchida e todo filho direto deve estar associado exatamente uma vez |

### 15.5 Termos desaconselhados ou inválidos em `estrutura: matriz`

| Termo | Status | Motivo |
|---|---|---|
| Ordem implícita de células | **inválido** | Posição determinada por coordenadas explícitas; a ordem de `celulas[]` não define posição (D8) |
| Matriz por grupos irmãos independentes | **inválido** | A grade compartilhada não pode ser construída por grupos com cortes independentes (D7) |
| Célula vazia | **proibida** na versão atual | Toda célula deve ser preenchida (D10) |
| Mesclagem (`rowspan`/`colspan`) | **fora de escopo** | Não previsto na ADR-0020 (D11) |
| Distribuição implícita de eixo | **inválido** | Ambas as distribuições são obrigatórias e explícitas; ausência invalida a matriz (D6) |
| `arranjo` em `estrutura: matriz` | **proibido** | `arranjo` é autoridade concorrente ao posicionamento bidimensional (D13) |

---

## 16. Distribuição matricial configurável de nível único (ADR-0025)

A ADR-0025 (2026-07-16) formaliza a capacidade genérica de distribuição
matricial configurável de nível único do conteúdo dos elementos. Esta seção é a
referência terminológica canônica; a especificação normativa completa está na
ADR-0025 e nos contratos JSON dos elementos afetados.

### 16.1 Termos fundamentais

| Termo | Definição normativa | Não confundir com |
|---|---|---|
| `distribuição matricial de nível único` | Capacidade de organizar os participantes imediatos de um elemento em uma grade configurável, dentro da área útil daquele elemento | `distribuicao` (campo de alocação de área entre filhos de container); `matriz de grupos` (ADR-0020, grade do nó estrutural `grupo`) |
| `elemento organizador` | Elemento funcional (`dashboard`, `console` ou `lancador`) que organiza diretamente o conjunto de participantes e declara `distribuicao_matricial` em seu JSON | `grupo` (nó estrutural, não funcional); `corpo` (raiz estrutural) |
| `participante imediato` | Cada unidade do conjunto ordenado organizado pelo elemento no nível atual; perante o nível externo é tratado como unidade única | filho de `grupo`; item de lista de dados |
| `formação` | Decisão de como os participantes são distribuídos em linhas e colunas — `preferencia_linhas`, `preferencia_colunas` ou `matriz_fixa` | `ordem` (sequência de preenchimento das células); `distribuicao_horizontal` (posição da matriz na área útil) |
| `preferência por linhas` | Política de formação que prioriza o preenchimento ao longo das linhas, respeitando limites declarados e a área disponível | `preferência por colunas`; `matriz fixa` |
| `preferência por colunas` | Política de formação que prioriza o preenchimento ao longo das colunas, respeitando limites declarados e a área disponível | `preferência por linhas`; `matriz fixa` |
| `matriz fixa` | Política de formação que exige a quantidade declarada de linhas e colunas; sem redução ou reorganização silenciosa — se não couber, aciona o estado canônico | `preferência por linhas`; `preferência por colunas` |
| `célula` (contexto ADR-0025) | Posição individual na grade dos participantes imediatos do elemento, identificada por (linha, coluna) | `célula da matriz` (ADR-0020, coordenada na grade de grupos); `item de lista` |
| `margem` (contexto ADR-0025) | Distância entre a borda da área útil do elemento e o início da grade matricial; medida interna ao elemento | `vão`; `espaço externo proibido` (ADR-0024); `padding estrutural` |
| `vão` (contexto ADR-0025) | Distância entre colunas da grade (horizontal) ou entre linhas da grade (vertical) | `margem` |
| `espaço excedente` | Diferença entre a área útil e a área mínima necessária para a formação válida; distribuído pelas políticas de distribuição e expansão | área útil; área mínima |
| `distribuição uniforme` | Política de distribuição que reparte o espaço excedente igualmente entre margens e vãos de um eixo | `entre_participantes`; `entre_linhas` |
| `alinhamento interno` | Posição do participante dentro da célula que lhe foi alocada — horizontal (`inicio`, `centro`, `fim`) e vertical (`topo`, `centro`, `base`) | `distribuicao_horizontal` (posição global da grade na área útil); `distribuicao_vertical` |
| `formação válida` | Formação capaz de acomodar todos os participantes e todos os mínimos declarados dentro da área útil disponível | formação inválida; impossibilidade geométrica |
| `impossibilidade geométrica` | Condição em que nenhuma formação válida consegue acomodar todos os participantes e todos os mínimos; aciona o estado canônico | formação inválida isolada (quando ainda existem alternativas válidas) |
| `recuperação determinística` | Processo de reconstrução da distribuição válida quando a área volta a ser suficiente após impossibilidade geométrica; a mesma entrada produz sempre o mesmo resultado | degradação parcial; ajuste silencioso |

### 16.2 Termos canonizados para o fallback

O estado exibido quando ocorre impossibilidade geométrica é o estado já
estabelecido pela ADR-0017 e ADR-0023:

| Termo canônico | Definição |
|---|---|
| `quadro mínimo de terminal pequeno` | Estado canônico exibido quando as dimensões são insuficientes — incluindo quando a impossibilidade decorre da configuração de `distribuicao_matricial` |

A ADR-0025 usa a expressão **"terminal muito pequeno"** para descrever a
**condição** geométrica (nenhuma formação válida cabe). O **estado exibido**
permanece o `quadro mínimo de terminal pequeno` já estabelecido pela ADR-0017 e
ADR-0023. As duas expressões não são concorrentes:

- "terminal muito pequeno" = condição geométrica que aciona o fallback;
- `quadro mínimo de terminal pequeno` = estado canônico exibido, independente
  da causa que o acionou.

Nenhuma variante concorrente de quadro mínimo é criada para impossibilidade
geométrica por distribuição matricial.

### 16.3 Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `distribuicao_matricial` × `distribuicao` (área) | `distribuicao_matricial` organiza participantes dentro da área útil de um elemento; `distribuicao` (ADR-0015, ADR-0018) aloca área entre filhos diretos de um container estrutural |
| `participante imediato` × filho de `grupo` | Participante imediato é unidade perante o elemento organizador funcional; filho de `grupo` é filho de nó estrutural |
| `matriz de grupos` (ADR-0020) × `distribuição matricial` (ADR-0025) | ADR-0020 trata a grade bidimensional do nó estrutural `grupo`; ADR-0025 trata a organização interna dos participantes de um elemento funcional |
| `nível único` × multinível | Nível único: apenas participantes imediatos do elemento; multinível: composição recursiva entre níveis — fora do escopo da ADR-0025 |
| `margem interna` × `espaço externo proibido` | Margem interna é distância configurável dentro da área útil do elemento; espaço externo proibido é linha ou coluna fora das molduras dos elementos visuais (ADR-0024) |
| `formação` × `ordem` | Formação: como os participantes são distribuídos em linhas e colunas; ordem: sequência em que as posições sequenciais são mapeadas para as células da grade |
| `alinhamento interno` × `distribuição horizontal/vertical` | Alinhamento interno: posição do participante dentro de sua célula; distribuição horizontal/vertical: posição da grade inteira na área útil |

### 16.4 Vocabulário normativo dos campos

Os valores aceitos pelos campos de `distribuicao_matricial` estão definidos
nos contratos JSON de cada elemento (`contrato_json_dashboard.md`,
`contrato_json_console.md`, `contrato_json_lancador.md`) e no contrato geral
(`contrato_tela_json.md`, seção 30).

Adições a este vocabulário exigem atualização normativa dos contratos afetados
antes de uso em qualquer JSON de tela.

### 16.5 Itens fora do escopo da ADR-0025

| Item | Status |
|---|---|
| Distribuição multinível (mais de um nível de recursão) | Fora do escopo — requer decisão e ADR próprias |
| Recursão de configuração entre níveis | Fora do escopo |
| Herança de parâmetros entre níveis | Fora do escopo |
| Cascata de configurações entre ancestral e descendente | Fora do escopo |
| Paginação do conjunto de participantes | Fora do escopo |
| Navegação entre páginas | Fora do escopo |
| Aplicação automática a descendentes | Proibida |
| Migração automática de JSONs existentes | Proibida |
| Default estrutural implícito capaz de reorganizar elementos existentes | Proibido |
