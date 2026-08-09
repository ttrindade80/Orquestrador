---
name: contrato-chip
description: Contrato documental da classe chip — entidade declarativa de interface textual usada principalmente na barra_de_menus; define campos minimos, tipos conceituais, regras de existencia, ativo/inativo e forma de exibicao
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - "docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md"
      - "docs/adr/ADR-0008-modelo-configuracao-por-tela.md"
      - "docs/contratos/contrato_tela_json.md"
      - "docs/contratos/contrato_barra_de_menus.md"
    adrs_aplicadas:
      - docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
      - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
      - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
      - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
      - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
      - docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/10_ESTILO.md
        quando: tratar forma visual do chip
      - modulo: docs/nomenclatura/32_CONSOLE.md
        quando: tratar chip associado ao console
      - modulo: docs/nomenclatura/33_LANCADOR.md
        quando: tratar distinção ou associação com lançador
      - modulo: docs/nomenclatura/34_DASHBOARD.md
        quando: tratar distinção ou associação com dashboard
      - modulo: docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md
        quando: houver termo descontinuado ou alias
---

# Contrato — `chip`

## 1. Objetivo

Definir a classe `chip` como entidade declarativa de interface textual. Este
contrato fecha os campos mínimos, os tipos conceituais, as regras de existência,
as regras de ativo/inativo, a forma de exibição e os critérios de validação de
qualquer chip declarado no `tela.json`.

Este contrato não implementa código, não cria JSON real de tela e não fecha o
registry completo de ações nem o registry completo de tipos de chip.

---

## 2. Natureza do `chip`

`chip` é uma **entidade declarativa de interface textual**. Representa uma
tecla ou símbolo acionável — ou informativo — exibido em uma região da tela,
especialmente na `barra_de_menus`.

Propriedades fundamentais:

- `chip` **não é ação** por si só: ele aponta para uma ação, filtro,
  alternância ou estado declarado. A ação pertence ao registro/whitelist;
  o chip é apenas o ponto de entrada declarativo.
- `chip` é **instanciado no `tela.json`**: cada chip concreto é uma instância
  declarada. Não existe chip sem declaração no JSON da tela.
- Aparência visual do chip vem do **`config/estilo.json`**: presets de
  moldura, cores, caixa alta e caracteres de abertura/fechamento pertencem ao
  schema de estilo universal.
- Comportamento vem de **ação ou regra declarada** no `tela.json`: o chip
  aponta para o que deve acontecer, não implementa a lógica.
- O **renderer não hardcoda** chip, tecla, texto, ação, regra de existência
  nem regra de estado. Percorre `chips[]` da instância declarada e aplica as
  regras deste contrato.

Distinção de conceito central (origem: ADR-0004 e `docs/nomenclatura/10_ESTILO.md`):

| Propriedade | Natureza | Quem decide |
|---|---|---|
| Existência do chip | Estática — derivada da declaração no `tela.json` | Classe de tela, via `regra_existencia` |
| Ativo/inativo | Dinâmica — recalculada a cada render | Renderer, com base no estado atual da execução |

---

## 3. Escopo principal

Nesta etapa, o uso primário de `chip` é a **`barra_de_menus`**. A instância da
`barra_de_menus` de uma tela é, no modelo ADR-0008, uma lista de chips
declarados no `tela.json`.

**Distinção obrigatória — chips do `lancador` não são chips da
`barra_de_menus`:**

Os itens do objeto `lancador` do corpo também possuem um `chip` visual (a
letra/tecla que identifica o item). Esses chips pertencem ao item do `lancador`
— são acionadores de navegação declarados dentro do próprio item. Eles **não
são** chips da instância da `barra_de_menus` e não pertencem a `chips[]` da
barra.

Essa distinção evita contaminação terminológica e é obrigatória em código,
documentação e nomenclatura. O contrato do `lancador`
(`docs/contratos/contrato_lancador.md`) é a autoridade sobre a estrutura do
item do `lancador`; este contrato é a autoridade sobre chips da
`barra_de_menus`.

---

## 4. Campos mínimos de um chip

Todo chip declarativo deve possuir, no mínimo:

```text
id
tipo
tecla
texto
acao ou referencia_regra
regra_existencia
regra_ativo
forma_exibicao
```

Semântica de cada campo:

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string estável | Identificador único do chip no escopo da instância da `barra_de_menus`. Usado para validação, binding, diagnóstico e manutenção. |
| `tipo` | string (enum) | Tipo conceitual do chip — ver seção 5. Determina qual família de regras e validações se aplica. |
| `tecla` | string | Identificador acionável pelo usuário. Não pode duplicar dentro da mesma instância da `barra_de_menus`, salvo exceção futura explícita documentada em ADR. |
| `texto` | string | Rótulo exibido ao lado da tecla ou rótulo documental do chip. Pode ser estático ou dinâmico (ver seção 11). Não pode ser hardcoded pelo renderer. |
| `acao` ou `referencia_regra` | objeto declarativo | Para chips acionáveis: `acao` aponta para a ação declarada/registrada que será executada. Para chips informativos ou de estado: `referencia_regra` aponta para a regra que governa o chip. |
| `regra_existencia` | declaração estrutural | Determina se o chip existe naquela instância de tela. É estática: avaliada na carga do `tela.json`, não muda em runtime. Ver seção 8. |
| `regra_ativo` | declaração dinâmica | Determina se o chip está ativo ou inativo em cada render. É dinâmica: recalculada a cada render com base no estado da execução. Ver seção 9. |
| `forma_exibicao` | declaração de apresentação | Como o chip aparece visualmente — ativo, inativo, ausente, rótulo dinâmico, agrupamento. Ver seção 10. |

---

## 5. Tipos conceituais de chip

Os tipos abaixo são os tipos iniciais reconhecidos. A lista não é exaustiva —
extensão futura exige ADR.

```text
acao
filtro
alternancia
navegacao
informativo
especifico
```

Mapeamento conceitual:

| Tipo | Natureza |
|---|---|
| `acao` | Executa ação declarada e registrada no whitelist de ações. O chip aponta para a ação; a lógica pertence ao registro. |
| `filtro` | Altera o filtro ativo da instância de `console`. Atua sobre o conjunto exibido, antes da paginação. Referencia filtro declarado no `tela.json`. |
| `alternancia` | Liga ou desliga estado de exibição, como modo verboso (`[V]`), ou alterna foco entre consoles focalizáveis (`[⇆]`). |
| `navegacao` | Representa navegação ou cursor quando aplicável — ex.: `[✥]` como dica de navegação por setas, ou `[PgUp][PgDn]` como paginação. Não executa lógica arbitrária. |
| `informativo` | Exibe estado ou dica sem ação direta, se explicitamente permitido pela declaração da instância. |
| `especifico` | Chip próprio de uma tela ou processo, com ação declarada e registrada. Declarado pela classe de tela; posicionado na faixa canônica de específicos (entre `[⏎]` e `[V]`/`[?]`). |

Pela ADR-0022, o acesso a estilos da futura tela inicial real `orquestrador`
é um chip/item específico da instância da `barra_de_menus`. Enquanto a tela
funcional de estilos não existir, ele não pode simular destino, ação
temporária, alias ou fallback. Se for declarado como `informativo` ou item
não navegável, essa forma deverá ser admitida pelos contratos ativos no
momento da criação física da tela.

---

## 6. Distinção entre tipo `canonico` e tipos acima

O `contrato_barra_de_menus.md` menciona `canonico` como tipo documental de
chip (seções 6 e 7). Este contrato adota uma taxonomia ligeiramente mais
granular para uso nos campos do chip:

- `[?] Ajuda` é a identidade canônica de existência universal: possui
`regra_existencia: sempre` e é obrigatória em toda tela pela ADR-0043. `[Esc]`
e `[⏎]` continuam com as regras declarativas próprias da barra quando
presentes.
- Chips canônicos de existência condicional (`[PgUp][PgDn]`, `[-][+]`, `[#]`,
  `[⇆]`, `[✥]`, `[␣]`, `[V]`) são instâncias de tipos como `navegacao`,
  `filtro`, `alternancia` ou `acao`, com `regra_existencia` condicionada.
- A semântica de "canônico" como invariante contratual permanece definida no
  `contrato_barra_de_menus.md`.

O campo `tipo` do chip reflete a natureza funcional do chip, não apenas se ele
é canônico ou específico.

---

## 7. Chips canônicos como instâncias padronizadas

Chips canônicos são **instâncias padronizadas** da classe `chip` — não são
lista hardcoded no renderer. O contrato define a semântica e os invariantes;
a instância concreta é declarada no `tela.json`.

As notações abaixo são **identificadores documentais/canônicos**: nomes de
referência usados nesta documentação para identificar cada chip. Eles não são
valores renderizáveis obrigatórios — a renderização concreta vem da declaração
da instância e do estilo ativo.

```text
[Esc]    — Sair / Voltar / Limpar (ver contrato_barra_de_menus.md seção 9)
[PgUp][PgDn] — Páginas (paginação de console)
[-][+]   — Colunas (ajuste de colunas de console)
[#]      — Grupos (filtro de grupo)
[⇆]      — Alternar (foco entre consoles focalizáveis)
[✥]      — Navegar (cursor de console por setas do teclado)
[␣]      — Selecionar (toggle de seleção múltipla)
[⏎]      — Ação do item em foco (Todos / Executar / Visualizar)
[V]      — Verboso (alterna modo verboso de console)
[?]      — Ajuda (universal, último chip)
```

Para `politica_navegacao.tipo = arvore_colapsavel`, também existem as
identidades contextuais `[␣] Expandir` e `[␣] Recolher`. Elas não são aliases de
`[␣] Selecionar`: a tecla física é a mesma, mas a função contextual é
expansão/recolhimento.

Chips específicos de classe de tela são instâncias adicionais, não incluídas
nessa lista canônica, declaradas individualmente pela classe no `tela.json`.

---

## 8. Regra de existência (`regra_existencia`)

`regra_existencia` é uma **regra estrutural** que determina se o chip existe
naquela instância de tela. É avaliada na carga do `tela.json` — antes do
render — e não muda enquanto a tela está aberta.

Exemplos de valores conceituais:

```text
sempre                                              — chip sempre existe nessa instância; para `[?] Ajuda`, em toda tela
console_com_paginacao                               — existe se a instância de console declara paginacao: com
console_com_colunas_ajustavel                       — existe se a instância de console declara colunas_ajustavel: com
console_com_filtro_de_grupo                         — existe se a instância de console declara filtro_de_grupo: com
console_com_selecao_multipla                        — existe se a instância de console declara seleção múltipla
console_com_modo_verboso                            — existe se a instância de console permite modo verboso
tela_com_controle_execucao_valido                   — existe se a raiz do tela.json declara controle_execucao válido e a tela satisfaz a compatibilidade integral das ações de processo relevantes
tela_com_pelo_menos_dois_consoles_focalizaveis      — existe se a tela possui pelo menos dois consoles focalizáveis (ADR-0031 D14; substitui tela_com_multiplos_corpos)
console_focado_com_mais_de_um_item_navegavel        — aparece quando o console focado possui mais de um item navegável (ADR-0031 D14; substitui tela_com_console_navegavel; existência dinâmica — ver nota)
acao_especifica_declarada                           — existe se a classe de tela declara esta ação específica
filtro_declarado                                    — existe se a tela declara o filtro referenciado
```

O chip `[?] Ajuda` é sempre existente, permanece entre estados, páginas e
mudanças de foco da mesma tela e ocupa a última posição canônica. A falta de
largura não permite omiti-lo; aplica-se `erro_layout` quando a distribuição
declarada não couber.

O chip contextual de `arvore_colapsavel` existe quando há console focalizado
com item corrente navegável. Seu rótulo e estado são derivados desse item,
conforme a seção 9, sem criar identificador técnico ou campo de schema.

A existência é **estática** para a tela carregada na maioria dos chips. Exceção
documentada: `[✥]` (ADR-0031 D14) possui existência **dinâmica** — aparece e
desaparece conforme o console em foco; não assume estado inativo: está ausente
ou presente. Outras exceções de existência dinâmica exigem ADR.

Chip cuja `regra_existencia` não é satisfeita para a instância concreta não
ocupa espaço na `barra_de_menus`. Os chips existentes mantêm a ordem relativa
canônica entre si.

---

## 9. Regra de ativo/inativo (`regra_ativo`)

`regra_ativo` é uma **regra dinâmica** recalculada a cada render. Determina se
um chip que existe na instância está operável no estado atual da execução.

Três condições visuais semanticamente distintas (ADR-0037):

```text
ausente
visível e inativo
visível, ativo e opcionalmente destacado
```

Um chip inativo:

- continua existindo na posição canônica da `barra_de_menus`;
- usa `cor_inativo` do schema de estilo (`ADR-0004`, `contrato_estilo.md`
  seção 3.5);
- não reage a acionamento do usuário;
- não desaparece da `barra_de_menus`.

Um chip pode estar **ativo e simultaneamente destacado**: o destaque usa
`cor_alerta` e **não** altera `regra_ativo`. Destaque não implica inatividade.

Chip do tipo `alternancia` pode permanecer ativo nos dois estados do toggle.
O estado ligado pode usar `cor_alerta` sem usar `cor_inativo`.

Exemplos de regras de ativo/inativo:

| Chip (notação documental) | Condição de inativo |
|---|---|
| `[PgUp]` (página anterior) | Página atual é a primeira |
| `[PgDn]` (próxima página) | Página atual é a última |
| `[-]` (menos colunas) | `n_col` está no mínimo (1) |
| `[+]` (mais colunas) | `n_col` está no máximo que a largura atual comporta |
| `[⏎]` | Item em foco não tem ação válida declarada ou não há alvo válido |
| `[␣]` | Item em foco não é selecionável |
| filtro | Não há valores aplicáveis no conjunto atual |
| específico | Pré-condição declarada pela classe não está satisfeita |

Estado inativo é sempre derivado do estado da execução — nunca hardcoded pelo
renderer.

**Nota sobre `[✥]` (ADR-0031 D14; especializada por ADR-0038 D-PAG-04)**:
`[✥]` **não possui estado inativo**. Ele aparece somente quando o console em
foco possui mais de um item navegável; está **ausente** (não inativo) nos
demais casos. Sua existência é dinâmica, em contraste com o modelo estático
geral desta seção. Em console paginado, o universo de avaliação é restrito
aos itens navegáveis da **página atual** do console focado — itens
navegáveis presentes apenas em outras páginas não fazem `[✥]` aparecer nem
permanecer (ADR-0038 D-PAG-04).

**Nota sobre `[PgUp][PgDn]` (ADR-0038; tecla e notação especializadas pela
ADR-0041)**: chips de tipo `navegacao`, existência condicionada a
`paginacao: com` (§8). A topologia entre páginas é **limitada**, não
circular: `[PgUp]` fica inativo na primeira página e `[PgDn]` fica inativo na
última; ambos ficam inativos quando há apenas uma página (`página 1/1`),
inclusive quando o conjunto de itens visíveis é vazio. O estado ativo/inativo
de ambos é calculado a partir da página do console focado; sem console
focado, ou com o console focado sem `paginacao: com` declarada, ambos ficam
inativos (D-PAG-13) — a mesma distinção desta seção entre existência estática
e ativo/inativo dinâmico se aplica: a existência de `[PgUp][PgDn]` depende da
declaração da instância; o estado ativo/inativo depende da página corrente do
console focado no momento do render. A entrada de teclado aceita para página
anterior é exclusivamente `PageUp`; para próxima página, exclusivamente
`PageDown` (ADR-0041 D-PGU-01, D-PGU-02) — tradução de tecla física para
esses valores permanece de implementação. Os caracteres `,`, `<`, `.` e `>`
deixam de ter qualquer função de paginação — não são alias, atalho nem
fallback (ADR-0041 D-PGU-04). A apresentação visual passa a ser `[PgUp]` e
`[PgDn]`, representação canônica `[PgUp][PgDn] Páginas` (ADR-0041 D-PGU-03),
em substituição a `[<][>]`.

**Nota sobre `[Ins] Dry-Run` (ADR-0037)**: chip específico do fluxo focal do
Handoff 4 — tipo `alternancia`. Permanece ativo nos estados ligado e
desligado; nunca usa `cor_inativo`. Com `dry_run_ativo: true`, usa
`cor_alerta` como único eco. Não entra na lista universal de chips canônicos
(§7). O estado `dry_run_ativo` é estado vivo da instância; a codificação
física da associação entre estado e apresentação será fechada no handoff —
esta aplicação não cria novo campo de schema (`regra_destaque`,
`estado_visual`, preset específico ou chave nova de `tela.json`).

### 9.1 Controle universal de execução real e `dry-run` (ADR-0040)

O controle universal é uma identidade reutilizável da classe `chip`, de
categoria `especifico` e tipo conceitual `alternancia`; não é chip canônico.
Sua existência é condicionada à declaração válida, na raiz do `tela.json`, do
objeto opcional `controle_execucao` com o campo
`controle_execucao.modo_inicial` obrigatório em `executar` ou `dry_run`, além
da compatibilidade integral de todas as ações de
processo relevantes com execução real e `dry-run`. Ações de navegação e simples
visualização não entram nessa condição. Sem o objeto, com objeto inválido ou
sem a compatibilidade exigida, o chip está ausente.

Quando declarado, o chip usa `Insert` e alterna o rótulo entre `[Ins]
Real` e `[Ins] Simulação` (D-DRY-12, rótulos vigentes que substituem `[Ins]
Executar`/`[Ins] Dry-Run`, originalmente fixados por D-DRY-02 — histórico
substituído). Ele não possui estado inativo enquanto declarado e permanece
operável nos dois estados. Em `Real`, usa a aparência ativa normal; somente em
`Simulação`, o texto usa `cor_alerta`. O texto é a indicação
primária e a cor é apenas reforço. O modo corrente é único por instância de
tela e pertence ao runtime; não é modo do console nem do item corrente. Essa
identidade universal não substitui nem migra o `[Ins] Dry-Run` focal da
ADR-0037. O rótulo reflete o modo corrente preservado enquanto a mesma
instância existir. A inicialização e a reinicialização em nova abertura ou
recarga pertencem ao ciclo de vida da tela, não a uma decisão autônoma do
chip.

### 9.2 Chip contextual de árvore (ADR-0043)

Quando o console focalizado declara `politica_navegacao.tipo =
arvore_colapsavel`, o rótulo e o estado do chip de Espaço derivam
exclusivamente do item corrente:

| Item corrente | Estado | Chip |
|---|---|---|
| ramo com filhos | expandido | `[␣] Recolher` ativo |
| ramo com filhos | recolhido | `[␣] Expandir` ativo |
| folha | não aplicável | `[␣] Expandir` inativo |

O chip contextual é funcionalmente distinto de `[␣] Selecionar`. Folha não
possui ação de Espaço. O estado inativo permanece visível, com capitalização
normal e forma canônica de chip inativo. A regra não introduz ação textual,
ID técnico, enum, registry ou campo novo de schema.

---

## 10. Forma de exibição (`forma_exibicao`)

`forma_exibicao` define como o chip aparece visualmente na `barra_de_menus`.

Aspectos cobertos pelo campo:

- chip ausente (quando `regra_existencia` não é satisfeita);
- chip visível e inativo (usa `cor_inativo`);
- chip visível, ativo e opcionalmente destacado (destaque via `cor_alerta`,
  sem alterar `regra_ativo` — ADR-0037);
- texto/rótulo dinâmico (quando o rótulo muda conforme estado — ex.: `[⏎]`
  alternando entre `Todos`, `Executar` e `Visualizar`);
- agrupamento visual (quando dois ou mais chips aparecem juntos — ex.:
  `[-][+]` e `[PgUp][PgDn]`);
- posição relativa conforme distribuição canônica da `barra_de_menus`.

O layout final detalhado da `barra_de_menus` não é fechado por este contrato.
`forma_exibicao` declara a intenção de exibição; a aplicação visual concreta
respeita o schema de estilo ativo e a ordem canônica definida em
`contrato_barra_de_menus.md` seção 7.

---

## 11. Texto e tecla

**`tecla`** é o identificador acionável pelo usuário — a tecla física ou
combinação de teclas que dispara o chip.

**`texto`** é o rótulo exibido junto à tecla ou o rótulo documental do chip.

Regras:

- `tecla` não pode duplicar dentro da mesma instância da `barra_de_menus`,
  salvo exceção futura explicitamente documentada em ADR.
- `texto` pode ser **dinâmico** quando derivado de estado ou ação, mas deve
  ter regra declarada no `tela.json` — não pode ser hardcoded no renderer.
- Chip não pode depender de texto hardcoded no renderer para nenhum estado.
- A tradução de `tecla` para valor de terminal (código de tecla, símbolo de
  display) é responsabilidade do renderer, com base na declaração da instância
  e no estilo ativo — não do schema do chip.

Exemplo de rótulo dinâmico contratual: `[⏎]` tem texto diferente conforme o
estado da seleção e o tipo de ação do item em foco (ver `contrato_barra_de_menus.md`
seção 10 e `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`).

---

## 12. Relação com estilo

A moldura visual do chip vem exclusivamente do `config/estilo.json`:

- caracteres de abertura/fechamento (`caractere_esquerdo`, `caractere_direito`);
- cor do texto/tecla (`cor_texto`);
- cor de fundo (`cor_fundo`);
- maiúsculas (`caixa_alta`).

Estados dinâmicos de cor (`cor_inativo`, `cor_alerta`) pertencem ao schema de
estilo universal, formalizados pela ADR-0004 e reconciliados pela ADR-0037
(`contrato_estilo.md` seção 3.5):

- `cor_inativo` (`cinza`): aplicada quando o chip existe mas está
  temporariamente inativo;
- `cor_alerta` (`amarelo`): aplicada a elemento operável em estado de
  destaque, ou quando um valor/limite exige atenção — não implica
  inatividade.

O chip **não define** diretamente caractere de borda global nem valor de cor
próprio — lê do schema de estilo ativo. O chip pode referenciar preset de estilo
nomeado, se o schema do `tela.json` permitir futuramente.

Hardcoding de qualquer valor de cor, caractere de moldura ou símbolo de chip no
renderer é violação contratual.

---

## 13. Relação com `barra_de_menus`

A `barra_de_menus` é uma lista de chips declarados no `tela.json`. Este
contrato define a classe `chip`; `contrato_barra_de_menus.md` define a região
`barra_de_menus` como um todo.

A `barra_de_menus`:

- ordena e distribui chips conforme a ordem canônica (seção 7 de
  `contrato_barra_de_menus.md`);
- aplica a regra de distribuição declarada pela instância;
- exibe os chips existentes, respeitando `regra_existencia`;
- aplica estado ativo/inativo conforme `regra_ativo`;
- não decide composição do corpo;
- não cria chip não declarado no `tela.json`.

O renderer da `barra_de_menus` percorre `chips[]` da instância. Não possui
lógica de seleção de chips nem fallback próprio.

---

## 14. Relação com `console`

Chips podem refletir capacidades declaradas por uma instância de `console`:

- `[✥]` depende de `console` focalizável com mais de um item navegável em foco
  — aparece dinamicamente quando o console focado possui mais de um item
  navegável; ausente nos demais casos (ADR-0031 D14; ver §8 nota e §22.8 de
  `contrato_console.md`);
- `[␣]` depende de `console` com seleção múltipla declarada;
- `[␣] Expandir`/`[␣] Recolher` dependem da política declarada
  `arvore_colapsavel` e do item corrente navegável do console focalizado;
- `[⏎]` depende da ação declarada pelo item em foco no `console` atual;
- `[PgUp][PgDn]`, `[-][+]` dependem das capacidades declaradas pela instância de
  `console` (paginação, colunas ajustáveis);
- filtros atuam sobre dados vinculados ao `console` — o chip de filtro
  referencia o filtro declarado no `tela.json` para aquela instância;
- `[V]` alterna modo verboso quando a instância de `console` permite.

---

## 15. Relação com `lancador` e `dashboard`

**`[✥]` não navega `lancador`**: `[✥]` e as setas do teclado controlam somente
cursor de `console` navegável. `lancador` tem navegação própria por itens via
`tela_destino` e não é corpo navegável por `[✥]` (ADR-0005).

**`[✥]` não navega `dashboard`**: `dashboard` é saída passiva não interativa —
não expõe cursor navegável.

**Chips da `barra_de_menus` não são os chips internos dos itens do
`lancador`**: os chips visuais de itens do `lancador` (a letra/tecla que
identifica o item) pertencem ao item do `lancador`, regido por
`contrato_lancador.md`. Não pertencem a `chips[]` da instância da barra.

**`dashboard` como elemento de corpo não é afetado por chips de navegação**:
`dashboard` pode ser afetado por ações ou filtros somente se a tela declarar
isso futuramente, mas não é navegável por chip de navegação de `[✥]`.

---

## 16. Ação

Ação de chip deve ser **declarativa e registrada/whitelisted**. O JSON nunca
pode declarar comando arbitrário.

**Permitido conceitualmente:**

```json
{
  "acao": {
    "tipo": "abrir_tela",
    "alvo": "selecao"
  }
}
```

```json
{
  "acao": {
    "tipo": "alternar_filtro",
    "filtro": "grupo"
  }
}
```

```json
{
  "acao": {
    "tipo": "toggle_estado",
    "estado": "modo_verboso"
  }
}
```

**Proibido conceitualmente:**

```json
{
  "acao": "python script_x.py --algo"
}
```

O JSON não pode executar comando arbitrário, chamar script livre nem declarar
lógica procedural. Toda ação declarada em chip deve pertencer ao registro de
ações conhecidas. Ação não registrada é erro de validação — não é ignorada nem
executada.

---

## 17. Validação

Critérios mínimos de validação de um chip:

- [ ] Chip sem `id` é inválido.
- [ ] Chip sem `tipo` é inválido.
- [ ] Chip sem `tecla` é inválido, salvo chip informativo futuro
      explicitamente permitido por extensão documentada.
- [ ] Chip sem `texto` é inválido, salvo exceção documentada.
- [ ] Chip acionável sem `acao` (ou `referencia_regra` equivalente) é inválido.
- [ ] Ação não registrada no whitelist é inválida — erro de validação, não
      ignorada.
- [ ] Filtro referenciado por chip de tipo `filtro` que não existe na
      declaração da tela é inválido.
- [ ] Estado alternado referenciado por chip de tipo `alternancia` que não
      existe na declaração da tela é inválido.
- [ ] Tecla duplicada na mesma instância da `barra_de_menus` é erro de
      validação.
- [ ] `[✥]` vinculado a `lancador` ou `dashboard` como condição de existência
      é violação contratual (ADR-0005).
- [ ] `[␣]` declarado em tela sem `console` com seleção múltipla é inválido.
- [ ] `[?] Ajuda` existe em toda tela, é sempre ativo, permanece entre estados,
      páginas e focos da mesma tela e é o último chip; não pode ser omitido
      para caber, pois a insuficiência de largura é `erro_layout`.
- [ ] `[␣] Expandir`/`[␣] Recolher` não compartilham identidade funcional com
      `[␣] Selecionar`; seu rótulo e estado derivam do item corrente de
      `arvore_colapsavel`, e folha apresenta `[␣] Expandir` inativo sem ação de
      Espaço.
- [ ] `[⏎]` declarado sem política de item em foco (ação por item/binding) é
      inválido.
- [ ] O controle universal só existe quando `controle_execucao` é declarado
      validamente na raiz do `tela.json`, com `modo_inicial` em `executar` ou
      `dry_run`, e a compatibilidade integral das ações de processo relevantes
      é satisfeita.
- [ ] A ausência de `controle_execucao` não produz o chip universal.
- [ ] O controle universal permanece ativo nos dois estados e usa
      `cor_alerta` somente em `Simulação` (rótulo vigente de `dry_run`,
      D-DRY-12); não usa `cor_inativo`.
- [ ] Hardcoding de chip, tecla, texto, ação, `regra_existencia` ou
      `regra_ativo` pelo renderer é violação contratual.
- [ ] Toda ação declarada em chip pertence ao registro de ações conhecidas.

---

## 18. Pendências fora de escopo

Os itens abaixo estão fora do escopo deste contrato e devem ser tratados em
tarefas ou ADRs posteriores:

- **Layout final detalhado da `barra_de_menus`**: distribuição de espaço,
  alinhamento interno, espaçamento entre chips.
- **JSON real de telas**: este contrato não cria JSON de nenhuma tela.
- **Implementação do dispatcher de ações**: a lógica de execução de ações
  registradas pertence ao código, não a este contrato.
- **Registry completo de ações**: os tipos de ação declaráveis e seus
  parâmetros formam um registry a ser definido em tarefa própria (DOC-B009).
- **Registry completo de tipos de chip**: a lista exaustiva de tipos
  reconhecidos pelo renderer pertence ao registry de tipos válidos (DOC-B009).
- **Atalhos avançados**: combinações de tecla, modos de ativação diferenciados
  por contexto.
- **Conflitos condicionais de teclas**: regras de desambiguação quando uma
  mesma tecla pode ter significados diferentes em contextos diferentes.
- **Internacionalização de rótulos**: tradução ou adaptação de `texto` para
  diferentes localidades.
- **Estrutura formal do chip específico tipo "aciona processo"**: estrutura
  a definir quando o primeiro caso concreto for especificado.
- **Relação entre `[#]` (filtro de grupo) e `[␣]` (toggle de seleção)**
  quando ambos estão ativos simultaneamente.
