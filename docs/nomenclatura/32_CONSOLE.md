---
name: nomenclatura-console
description: Terminologia do console — container interativo e navegável, cursor, seleção, lote, grupo como origem do dado, partes do item (ec/tg/tx), navegação
metadata:
  type: nomenclatura
  scope: console
  fase_de_aplicacao: VIGENTE
---

# Console

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário dos termos de:
- console como container interativo e navegável;
- cursor (selecionado);
- seleção como conjunto nomeado;
- lote como unidade de execução;
- grupo quando usado como categoria ou origem do dado (sentido do dado);
- item do console e suas partes `ec`, `tg`, `tx`;
- navegação do console enquanto vocabulário;
- relações conceituais com barra e conteúdo externo.

Não redefinir `grupo` como nó estrutural; esse sentido pertence ao módulo `40`.

## 3. Termos proprietários

- `console` (identificação e tipo)
- cursor / `selecionado` (como mecanismo de navegação)
- `grupo` (como origem/categoria do dado)
- seleção (conjunto nomeado de elementos)
- lote (unidade de execução)
- `ec` (espaço do cursor)
- `tg` (espaço de toggle)
- `tx` (texto do item)
- item de console
- `[✥]` (enquanto dica visual de navegação)
- wrap toroidal
- paginação é independente da navegação
- console focalizável / console focado (ADR-0031)
- item lógico / item corrente (ADR-0031)
- lista de foco / ordem de foco (ADR-0031)
- travessia em profundidade (ADR-0031)
- navegação toroidal por eixo (ADR-0031)
- linha física / coluna indicadora (ADR-0031)
- seleção única (ADR-0031)
- seleção múltipla (ADR-0034)
- conjunto de IDs estáveis (ADR-0034)
- reconciliação (ADR-0034)
- item selecionável (ADR-0034)
- lote reconciliado (ADR-0034)
- preservação da origem em dry-run (ADR-0037)
- restauração da origem após execução real (ADR-0037)
- reconciliação de foco (ADR-0037)
- preservação de cursor por ID (ADR-0037)
- fallback de cursor (ADR-0037)
- página atual / página de destino (ADR-0038)
- paginação limitada (ADR-0038)
- página lógica vazia (ADR-0038)
- repaginação (ADR-0038)
- política de navegação declarada (ADR-0042)
- `politica_navegacao.tipo` (ADR-0042)
- `nivel_unico` (ADR-0042)
- `tabela` como política de navegação (ADR-0042)
- `arvore_colapsavel` (ADR-0042)
- chip contextual de `arvore_colapsavel` (`[␣] Expandir` / `[␣] Recolher`) (ADR-0043)
- `selecao_multinivel` (ADR-0042)
- `dois_niveis_por_foco` (ADR-0042)
- seleção exclusiva obrigatória de filho por pai (ADR-0042)
- unidade inteira do filho deslocada (ADR-0047)
- baseline persistida da escolha de filho por pai (ADR-0048)
- candidato de runtime da escolha de filho por pai (ADR-0048)

## 4. Definições

### 4.1 Console como container

`console` é um container interativo e navegável genérico. Pode conter itens
heterogêneos. O cursor navega por itens, não por linhas físicas. Não é
sinônimo de tela, não é `lancador`, não é `dashboard`, não é `barra_de_menus`.

### 4.2 Mecanismos de seleção (quatro conceitos distintos)

| Conceito | O que é | Como se forma |
|---|---|---|
| **Cursor / selecionado** | Aponta um item; `[⏎]` executa ação sobre ele | Navegação via `[✥]` (setas do teclado), indicador `→` |
| **Grupo** | Origem/categoria do dado (ex.: grupo 1, 2, 3) — atributo do próprio dado | Já existe nos dados, filtra exibição via `[#]` |
| **Seleção** | Conjunto nomeado de elementos — cruza grupos livremente, sem limite | Toggle via `[␣]`, indicador `●`/`○`, persiste com nome |
| **Lote** | Unidade de execução — calculado a partir de uma seleção no momento de rodar um processo específico, tipicamente `seleção − o que já foi processado` | Derivado, não é marcado manualmente |

**Lote não é sinônimo de grupo nem de seleção**:
- Grupo: origem/escopo de exibição.
- Seleção: conjunto nomeado que cruza grupos.
- Lote: resultado calculado por processo a partir de uma seleção.

### 4.3 Navegação por `[✥]`

`[✥]` é a dica visual de "use as setas do teclado". A navegação em si é feita
pelas quatro setas.

**Escopo**: `[✥]` e as setas da `barra_de_menus` controlam somente cursor de
corpo tipo `console`. `lancador` não é corpo navegável por `[✥]`. `dashboard`
não é corpo navegável por `[✥]` (ADR-0005).

**Wrap toroidal**: a grade fecha nos dois eixos, cada um independente.
Célula vazia não recebe cursor e não participa do toróide. Se uma linha ou
coluna não possui outro item ocupado no eixo do movimento, a seta correspondente
resulta em `SEM_MOVIMENTO`. Não existe compensação para outra coluna, salto
diagonal, busca pelo item geometricamente mais próximo nem toróide composto por
células vazias.

**Paginação é independente da navegação**: o cursor nunca troca de página
sozinho ao cruzar a borda do toróide. Cada página é seu próprio toróide
fechado.

### 4.4 Estrutura do item do console

No item navegável, `ec` identifica o espaço do cursor e `tx` o texto. Item
selecionável acrescenta `tg`, sempre na ordem `ec`, `tg`, `tx`:

| Parte | Sigla | Função |
|---|---|---|
| Espaço do cursor | `ec` | onde `selecionado` (`→` ou preset equivalente) aparece quando o cursor está na linha |
| Espaço de toggle | `tg` | onde `incluido` (`●`/`○` ou preset equivalente) aparece em item selecionável |
| Texto do item | `tx` | conteúdo, tamanho variável |

**Uma estrutura só, não duas**: a apresentação de seleção usa `tg` no item
selecionável. Item não selecionável não possui estado de seleção e não recebe
`tg`.

- Com seleção real: `tg` mostra par on/off completo.
- Item não selecionável: não possui `tg` nem estado de seleção.

**Sobreposição `ec` × `tg`**: quando `tg` existe, os dois espaços coexistem em
posições distintas e adjacentes, não se sobrepõem entre si.

### 4.5 Terminologia de navegação de nível único (ADR-0031)

Os termos abaixo foram introduzidos pela ADR-0031. Autoridade comportamental
completa em `contrato_console.md` §22.

| Termo | Definição |
|---|---|
| **console focalizável** | Console que declara `politica_navegacao.navegavel: true` E possui ao menos um item com `navegavel: true` (D2). |
| **console focado** | O console focalizável que está atualmente em foco na sessão — o destino das setas do teclado (D2). |
| **item lógico** | Unidade de navegação por cursor — o item sob cursor, indexado pela sua posição na lista de itens navegáveis; independente das linhas físicas que ocupa na tela. |
| **item corrente** | Sinônimo de item lógico no contexto da posição do cursor. |
| **seleção única** | O item atualmente sob cursor é o "selecionado" sem toggle; mudar o cursor muda a seleção automaticamente (D13). |
| **lista de foco** | Sequência linear de consoles focalizáveis construída por travessia em profundidade da árvore de corpo (D3). |
| **ordem de foco** | Posição de um console na lista de foco; Tab avança em ordem crescente, Shift+Tab recua, circularmente (D5). |
| **travessia em profundidade** | Algoritmo que percorre a árvore de composição do corpo para construir a lista de foco: grupos são não-focalizáveis; irmãos em ordem da declaração JSON (esquerda→direita, cima→baixo em matrizes) (D3/D4). |
| **navegação toroidal por eixo** | Modelo de navegação em que cada eixo (horizontal, vertical) é um toróide independente; célula vazia é excluída do toróide; não há compensação entre eixos (D8/D9). |
| **linha física** | Linha do terminal ocupada por parte de um item ou por marcador de continuação; o cursor se move por item lógico, não por linha física. |
| **coluna indicadora** | Primeira linha física do console focado que recebe o símbolo indicador de foco derivado do `config/estilo.json` (D11/D12). |

`marcacao: exclusiva` é a política própria do pop-up e não é o termo
`seleção única` do console: no pop-up, mover o cursor não altera a marcação.

**Distinções adicionais obrigatórias (ADR-0031):**

| Par | Distinção normativa |
|---|---|
| foco × cursor | Foco: qual console está ativo na sessão (Tab/Shift+Tab); cursor: qual item está selecionado dentro do console focado (setas). |
| item corrente × item incluído | Item corrente: item sob cursor (seleção única); item incluído: item marcado na seleção múltipla (`[␣]`) — mecanismos independentes; seleção múltipla está fora de ADR-0031. |
| console focalizável × console não navegável | Não navegável: não declara `politica_navegacao.navegavel: true`; não entra na lista de foco. Console com `navegavel: true` mas zero itens navegáveis também não entra na lista de foco (D2). |
| item lógico × linha física | Item lógico é a unidade de navegação; linha física é o espaço visual. Redistribuição ou mudança de modo preserva o item lógico e recalcula as linhas físicas (D10). |

### 4.6 Terminologia de seleção múltipla (ADR-0034)

Os termos abaixo foram introduzidos pela ADR-0034. Autoridade comportamental
completa em `contrato_console.md` §23.

| Termo | Definição |
|---|---|
| **seleção múltipla** | Política de seleção (`politica_selecao: multipla`) em que o conjunto de itens marcados é um estado de runtime independente por console, persistente entre páginas, descartado ao sair ou recarregar a tela (D-SEL-01). Distinta de **seleção única** (ADR-0031), em que o único item marcado é sempre o item sob cursor. |
| **conjunto de IDs estáveis** | Forma de armazenamento da seleção múltipla — um snapshot de identificadores de item, não uma consulta dinâmica; não incorpora automaticamente itens criados após um acionamento de `Todos` (D-SEL-01). |
| **item selecionável** | Item com `selecionavel: true` que pode participar do toggle de `[␣]`; todo item selecionável é necessariamente navegável (D-SEL-02). Distinto de **item selecionado**/**item corrente** (módulo `32`, seleção única), que designa o item sob cursor. |
| **reconciliação** | Operação que remove da seleção os IDs inexistentes e os itens que deixaram de ser selecionáveis, executada antes da execução da operação consumidora e após atualização dos dados, preservando a ordem lógica do console (D-SEL-03, D-SEL-04). |
| **lote reconciliado** | Lista sem duplicatas, ordenada pela ordem lógica estável do console, resultante da reconciliação — entrada da operação consumidora focal (D-SEL-03, D-SEL-11). |

**Distinções adicionais obrigatórias (ADR-0034):**

| Par | Distinção normativa |
|---|---|
| seleção única (ADR-0031) × seleção múltipla (ADR-0034) | Seleção única: item sob cursor, sem toggle, sem persistência como conjunto; seleção múltipla: conjunto de IDs estáveis, com toggle por `[␣]`, persistente entre páginas. |
| seleção (módulo `32`, conjunto nomeado geral) × seleção múltipla (ADR-0034) | Seleção múltipla é a materialização concreta do conceito geral de "seleção" (§4.2) para o `ITEM-0006`, com identidade por conjunto de IDs estáveis e reconciliação fechadas pela ADR-0034. |
| lote (§4.2, unidade de execução) × lote reconciliado (ADR-0034) | Lote (§4.2) é o conceito geral de unidade de execução calculada a partir de uma seleção; lote reconciliado é a forma concreta desse lote no `ITEM-0006`, após reconciliação. |

### 4.7 Estado do console no retorno (ADR-0037)

Termos do estado do console no retorno após `resultado_execucao`. A definição
geral de origem suspensa pertence ao módulo `20` — este módulo não a duplica.
Autoridade comportamental: `contrato_console.md` §23.9.

| Termo | Definição |
|---|---|
| **preservação da origem em dry-run** | Retorno sem recarregar o binding: mesma instância e mesmos dados; seleção, filtro, página, foco e cursor preservados; `dry_run_ativo` permanece ligado |
| **restauração da origem após execução real** | Retorno com seleção limpa, binding recarregado, filtro reaplicado e `dry_run_ativo: false` — aplicável a sucesso, parcial, falha operacional, resultado inválido e interrupção `130` |
| **reconciliação de foco** | Preserva o foco anterior se o console continuar válido; caso contrário, fallback para o primeiro console focalizável |
| **preservação de cursor por ID** | Mantém o cursor no item cujo ID permanece válido após a recarga |
| **fallback de cursor** | Quando o ID anterior é inválido, posiciona no primeiro item navegável |

Distinções:

| Par | Distinção normativa |
|---|---|
| dry-run × execução real (retorno) | Dry-run: mesma instância e mesmos dados; execução real: recarga do binding somente no retorno |
| geometria física recalculada × recarga semântica | Redimensionamento recalcula geometria sem releitura de arquivos; recarga semântica só ocorre no retorno de execução real |

### 4.8 Terminologia de paginação interativa (ADR-0038)

Os termos abaixo foram introduzidos pela ADR-0038. Autoridade comportamental
completa em `contrato_console.md` §24.

| Termo | Definição |
|---|---|
| **página atual** | Página em que se encontra o cursor do console focado; estado de runtime independente por console — cada console mantém a própria página durante a sessão (D-PAG-13). |
| **página de destino** | Página para a qual o cursor é reposicionado — no primeiro item navegável dessa página — após troca explícita de página (D-PAG-02) ou após retorno por foco a um console paginado (D-PAG-05). |
| **paginação limitada** | Topologia sem wrap entre a primeira e a última página: página anterior inativa na primeira página; próxima página inativa na última (D-PAG-01). Distinta da navegação toroidal por eixo (§4.5), que é interna a uma mesma página. |
| **página sem item navegável** | Página com conteúdo visível e nenhum item navegável; permanece acessível, com o console focado, sem cursor visível e sem movimento de setas (D-PAG-03). |
| **repaginação** | Recálculo da página que contém o item lógico corrente após redimensionamento, mudança de modo, filtro ou atualização genérica dos dados, preservando o item lógico e não o número anterior da página (D-PAG-06 a D-PAG-10). |

**Relação entre foco, cursor lógico, seleção e página**: foco determina qual
console recebe as setas e os comandos de página; cursor lógico é o item sob
foco dentro do console; seleção múltipla é conjunto de IDs independente de
cursor e de página (ADR-0034 §4.6); página é quarta camada de estado,
também independente por console, que determina qual subconjunto de itens do
console está atualmente acessível às setas. As quatro camadas são
reconciliadas de forma determinística nos eventos de troca de página, retorno
por foco, redimensionamento, mudança de modo, filtro e atualização genérica
dos dados (D-PAG-02 a D-PAG-10).

**Entrada por foco em console paginado**: ao retornar por Tab ou Shift+Tab a
um console paginado, a página anterior desse console é preservada; o cursor
não é restaurado ao item que ocupava antes da saída — é reposicionado no
primeiro item navegável da página preservada (D-PAG-05), especialização de
`console focalizável`/`console focado` (§4.5) para o caso paginado.

**Reconciliação por filtro e por atualização genérica**: quando um filtro
oculta o item corrente ou zera os itens navegáveis, ou quando uma atualização
genérica dos dados remove o item corrente, o cursor e a página são
reconciliados por prioridade determinística (próximo item navegável da ordem
lógica, com fallback no item navegável anterior) — D-PAG-07 a D-PAG-10.

**Precedência do retorno especializado da ADR-0037**: a reconciliação
genérica de D-PAG-10 não substitui a reconciliação especializada por ID já
fixada pela ADR-0037 (§4.7, **preservação de cursor por ID** e **fallback de
cursor**) para o retorno após execução real do Handoff 4 do `ITEM-0006`; as
duas regras operam em fronteiras distintas e coexistem sem conflito.

### 4.9 Transmissão do modo universal junto ao lote reconciliado (ADR-0040)

Quando uma operação baseada em seleção adota o controle universal da
ADR-0040, o modo corrente é transmitido explicitamente na requisição junto ao
lote reconciliado. O modo não compõe a identidade do lote nem altera seleção
ou reconciliação. Esta relação registra a entrada adicional da requisição; a
propriedade do modo global permanece na instância da tela, não no console. O
modo capturado e o lote reconciliado são dados da requisição para o executor;
`controle_execucao` e `controle_execucao.modo_inicial` não pertencem ao domínio
terminológico do console. O console não é proprietário do modo global da tela.

As referências de ação configuradas pelo console são resolvidas no registro
autoritativo da implementação. O console pode referenciar ou acionar uma ação,
mas não declara nem possui sua categoria ou seus modos de execução aceitos; a
aparência da configuração não os define. Incompatibilidade ou resolução
insuficiente deve falhar de forma fechada antes da execução. O modo acompanha a
requisição, mas não pertence ao console nem ao lote.

### 4.10 Vocabulário de navegação multinível (ADR-0042)

| Termo | Definição |
|---|---|
| **política de navegação declarada** | Política informada explicitamente no objeto `politica_navegacao` da instância do `console`; não é inferida da estrutura dos dados, da apresentação, do nome da fixture ou de outro campo. |
| **`politica_navegacao.tipo`** | Campo discriminador canônico da política de navegação. Aceita somente `nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel` e `dois_niveis_por_foco`; quando ausente, equivale a `nivel_unico`. |
| **`nivel_unico`** | Política que preserva integralmente o comportamento vigente de nível único, sem redesenho. |
| **`tabela` como política de navegação** | Política passiva: não participa do foco, não recebe cursor entre linhas, não é percorrida pelas setas, não exibe `[✥]` e não tem fallback para `nivel_unico`. Não é propriedade terminológica da apresentação `tabela`; uma declaração incompatível como navegável é falha focal. |
| **`arvore_colapsavel`** | Política de árvore hierárquica navegável sem seleção; ↑/↓ percorrem o que está visível e Espaço abre ou fecha o ramo corrente. |
| **`selecao_multinivel`** | Política única de profundidade arbitrária e selecionabilidade estruturalmente coerente: descendente selecionável implica todos os ancestrais estruturais selecionáveis; pai com seleção abaixo possui estado binário e `tg`; item não selecionável não possui estado nem `tg`, fica fora da seleção e da unanimidade e implica subárvore integralmente não selecionável; pai não selecionável com descendente selecionável é configuração inválida. D-MULTI-06-P03 permanece vigente: o pai deriva seu estado da unanimidade dos filhos selecionáveis imediatos, com reconciliação ascendente, sem estado parcial. |
| **`dois_niveis_por_foco`** | Política com exatamente dois níveis — pais e filhos diretos —, um toroide único de pais e um toroide próprio de filhos para cada pai. |
| **seleção exclusiva obrigatória de filho por pai** | Mecanismo de `dois_niveis_por_foco` em que cada pai mantém exatamente um filho escolhido; Espaço transfere a escolha para outro filho, mas mover o cursor não a transfere. |

`seleção exclusiva obrigatória de filho por pai` não é `seleção única`: esta
última continua designando, na ADR-0031, o item sob cursor que muda com o
cursor. Também não é seleção múltipla. Foco, cursor, seleção e escolha do
filho permanecem mecanismos distintos.

Para `arvore_colapsavel`, a relação entre foco, cursor e o chip contextual é
fechada assim:

```yaml
arvore_colapsavel:
  quando_focalizado:
    item_corrente_navegavel: obrigatorio
    cursor_valido: obrigatorio

  sem_nos_navegaveis_visiveis:
    focalizavel: false
```

Após troca de página, expansão, recolhimento ou recomputação da projeção
visível, o cursor deve estar reconciliado para item válido antes da interação
contextual. Esta relação não cria algoritmo de reconciliação, política de
borda ou nova regra de paginação. Foco, cursor e seleção continuam distintos:
`foco ≠ cursor ≠ seleção`.

### 4.11 Unidade inteira do filho deslocada (ADR-0047)

A ADR-0047 fecha a evolução exclusiva de apresentação/formatação dos
filhos de `dois_niveis_por_foco` (§4.10). Autoridade comportamental
completa em `contrato_console.md` §25; schema literal da tabulação e da
apresentação em `contrato_tela_json.md` §36 — ambos fora do escopo deste
módulo (ver módulo `44` para os termos proprietários de apresentação).

| Termo | Definição |
|---|---|
| **unidade inteira do filho deslocada** | Em `dois_niveis_por_foco`, o conjunto formado por `ec`, `tg` (quando existir), designador (quando existir) e conteúdo do filho, deslocado como um só bloco pela tabulação declarada em relação ao pai. Nenhum desses elementos se desloca isoladamente. |

O deslocamento preserva integralmente a estrutura `ec`/`tg`/`tx` já fixada
em §4.4: a tabulação é um recuo aplicado antes do início dessa estrutura,
não uma redefinição dela. O cursor do filho (`ec`) permanece sempre para
dentro do primeiro caractere visual do item pai. É proibido recuar somente
o texto (`tx`) mantendo `ec` ou `tg` alinhados ao pai — os dois espaços
continuam coexistindo em posições distintas e adjacentes, sem sobreposição
(§4.4).

### 4.12 Baseline e candidato da escolha de filho por pai (ADR-0048)

A ADR-0048 fecha o ciclo de persistência da seleção exclusiva obrigatória de
filho por pai (§4.10; ADR-0042), sem redefinir o mecanismo de runtime já
fixado. Autoridade comportamental completa: `contrato_console.md` §26.

| Termo | Definição |
|---|---|
| **baseline persistida da escolha de filho por pai** | A escolha ativa persistida (`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` §4.7), tal como carregada do documento externo de conteúdo, usada como referência de comparação do fluxo de aplicação |
| **candidato de runtime da escolha de filho por pai** | Estado vivo de sessão que acumula as transferências de escolha feitas por Espaço, distinto da baseline até uma aplicação confirmada e bem-sucedida |

Baseline e candidato desta capacidade não redefinem cursor, foco ou a
seleção exclusiva obrigatória de filho por pai (§4.10) — apenas acrescentam
o ciclo de persistência sobre o mesmo mecanismo.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `grupo` (sentido do dado) × `grupo` (nó estrutural) | Grupo como origem/categoria do dado pertence ao domínio do console; grupo como nó estrutural do corpo pertence ao módulo `40` — requerem contexto para desambiguação |
| seleção × lote | Seleção: conjunto nomeado persistente; lote: calculado por processo específico no momento de execução |
| cursor × seleção | Cursor aponta um item; seleção é conjunto de itens marcados — são mecanismos independentes |
| `[✥]` (console) × `[⇆]` (barra) | `[✥]` move cursor dentro do console focado; `[⇆]` move foco entre consoles focalizáveis (ADR-0031 D14) |
| página × seleção | Página é estado de runtime independente por console que delimita o subconjunto de itens acessível às setas; seleção é conjunto de IDs independente de página e persistente entre páginas (ADR-0034) — não se confundem |
| modo universal da tela × console | O modo universal pode acompanhar o lote reconciliado na requisição, mas não pertence ao lote nem ao console; `controle_execucao` pertence à declaração e ao runtime da tela (ADR-0040) |
| repaginação (D-PAG-10) × reconciliação especializada por ID (ADR-0037) | Repaginação genérica é regra padrão do `ITEM-0003` para atualização de dados; a reconciliação por ID do retorno pós-execução real do Handoff 4 é especialização exclusiva da ADR-0037 e tem precedência onde as duas poderiam se sobrepor |
| `tabela` como política × `tabela` como apresentação | A política `tabela` é passiva e define navegabilidade; a apresentação `tabela` pertence ao vocabulário de apresentação e não recebe propriedade da política por homonímia |
| cursor × escolha do filho | Cursor indica o item corrente; em `dois_niveis_por_foco`, a escolha do filho só muda por Espaço e permanece independente do movimento do cursor |
| estado de seleção do pai × estado paralelo | O estado do pai é binário e derivado da unanimidade dos filhos selecionáveis imediatos; não é contador, seleção independente, estado parcial ou terceiro estado |
| item não selecionável × unanimidade | Item não selecionável não possui estado de seleção, não recebe `tg` e não participa da unanimidade |
| seleção única × seleção exclusiva obrigatória de filho por pai | Seleção única é o item sob cursor da ADR-0031; seleção exclusiva obrigatória de filho por pai mantém uma escolha persistente e exclusiva por pai em `dois_niveis_por_foco` |
| navegação × paginação | Navegação move o cursor conforme a política ativa; paginação permanece independente e subordinada à ADR-0041, sem troca implícita de página pelo cursor |
| unidade inteira do filho deslocada × `ec`/`tg` individualmente | A tabulação desloca `ec`, `tg`, designador e conteúdo do filho como um só bloco; nenhum desses elementos é deslocado isoladamente, e a coexistência adjacente de `ec` e `tg` (§4.4) permanece preservada dentro do bloco deslocado |
| chip contextual × seleção | `[␣] Expandir`/`[␣] Recolher` refletem o item corrente de `arvore_colapsavel`; `[␣] Selecionar` pertence à seleção múltipla — a tecla física compartilhada não funde as semânticas |
| baseline persistida × candidato de runtime (ADR-0048) | Baseline é a última escolha persistida conhecida, carregada do documento externo (`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` §4.7); candidato acumula transferências de escolha ainda não aplicadas — distinção específica desta capacidade, análoga em filosofia à de Estilo (ADR-0046), sem autoridade compartilhada |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo completo do console.
- `contrato_barra_de_menus.md`: chips `[✥]`, `[␣]`, `[#]`, `[⏎]` são declarados pela barra.

## 7. Relação com ADRs

- ADR-0005: escopo de `[✥]` restrito a console.
- ADR-0006: renomeação `dado` para `console`.
- ADR-0026, ADR-0027, ADR-0028: dados externos e modos de apresentação do console.
- ADR-0031: navegação simples e seleção única; terminologia de console focalizável/focado, item lógico, lista de foco, travessia em profundidade, navegação toroidal por eixo, coluna indicadora, seleção única.
- ADR-0034: seleção múltipla e fluxo focal de processamento; terminologia de seleção múltipla, conjunto de IDs estáveis, reconciliação, item selecionável e lote reconciliado.
- ADR-0037: preservação/restauração da origem no retorno; reconciliação de foco; preservação e fallback de cursor.
- ADR-0038: paginação interativa limitada e independência de página por console; terminologia de página atual, página de destino, página sem item navegável e repaginação; precedência da reconciliação especializada por ID da ADR-0037 sobre a regra genérica de atualização de dados.
- ADR-0040: transmissão explícita do modo universal junto ao lote reconciliado, sem atribuir o modo ao console.
- ADR-0042: política de navegação declarada, cinco valores fechados de `tipo`, políticas multinível, precedência contextual de Esc e seleção exclusiva obrigatória de filho por pai.
- ADR-0043: Ajuda universal e chip contextual de expansão/recolhimento em
  `arvore_colapsavel`; fecha a relação semântica entre console focalizado,
  item corrente, cursor válido e chip contextual.
- ADR-0047: unidade inteira do filho deslocada em `dois_niveis_por_foco` —
  `ec`, `tg`, designador e conteúdo do filho movidos juntos pela tabulação
  declarada; apresentação e tabulação em si são terminologia proprietária
  do módulo `44` e autoridade comportamental de `contrato_console.md` §25.
- ADR-0048: baseline persistida e candidato de runtime da escolha de filho
  por pai; ciclo de aplicação, confirmação e persistência delegada;
  autoridade comportamental completa em `contrato_console.md` §26.

## 8. Aliases ou termos descontinuados relacionados

- `dado` → termo descontinuado substituído por `console` (ADR-0006). Ver módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- `grupo` como nó estrutural de composição do corpo → módulo `40`.
- Regras comportamentais completas de navegação → `contrato_console.md`.
- Apresentações multinível e modos verboso/não verboso → módulo `44`; a navegação multinível comportamental pertence à ADR-0042 e ao contrato do console.
- Carregamento e associação de conteúdo externo → módulo `43`.
- Dados externos e envelope declarativo → módulo `42`.
- Pendência `tx` (regras de ajuste quando texto não cabe) → classificada como pendência
  no relatório de aplicação (NOM-LEV-017); sem decisão vigente.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§4.0 (linhas 359-398), §4.1-4.4 (linhas 399-531)"
  intervalo_ou_bloco: "NOM-LEV-009, NOM-LEV-010"
origem_normativa: ADR-0005, ADR-0006
contratos_relacionados:
  - contrato_console.md
  - contrato_barra_de_menus.md
adrs_relacionadas:
  - ADR-0005
  - ADR-0006
  - ADR-0026
  - ADR-0027
  - ADR-0028
  - ADR-0031
  - ADR-0038
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS:
  - "Pendência tx: regras de ajuste do texto quando não cabe — classificada como PENDENCIA (NOM-LEV-017)"
  - "Relação [#] × [␣]: explicitamente adiada, não é pendência normativa atual"
```
