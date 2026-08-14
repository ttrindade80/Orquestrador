---
name: contrato-estilo
description: Schema e regras do módulo de estilo universal — borda, chip, indicadores e tiling
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/nomenclatura/10_ESTILO.md"
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
      - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
      - docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/10_ESTILO.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
        quando: o contrato tratar tiling ou arranjo do corpo
      - modulo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
        quando: o contrato tratar chip como entidade de interface
      - modulo: docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md
        quando: houver termo legado sobreposto ou lado_a_lado
---

# Contrato — Módulo de Estilo

## 1. Objetivo

Especificar o schema de estilo universal do sistema novo: os campos que
compõem borda, chip, indicadores e tiling, e as regras de uso que vinculam
todos os módulos a esse schema.

Este contrato cobre a terminologia de `docs/nomenclatura/10_ESTILO.md`.
Composição de corpo (`contrato_composicao_corpo.md`,
`ativo`) e barra_de_menus (`contrato_barra_de_menus.md`, `ativo`) são módulos
separados com contratos próprios. Os demais domínios devem ser tratados em
contratos próprios quando formalizados.

Pela ADR-0021, `config/estilo.json` permanece em seu caminho atual. Pela
ADR-0046, este contrato também governa o ciclo normativo de materialização,
edição candidata, demonstração local, persistência e publicação do estilo
global para a funcionalidade do `ITEM-0010`; a implementação continua fora
desta aplicação documental.

---

## 2. Regra fundamental e autoridade global (formal, não observação)

**`config/estilo.json` é a biblioteca global de aparência compartilhada e a
autoridade global exclusiva para a aparência do terminal (ADR-0008, ADR-0030
D1).** A escolha de aparência é global —
não é possível escolha diferente por tela neste modelo. Nenhuma classe de tela
ou renderer pode hardcodar símbolo, cor ou caractere pertencente a esta
especificação. Todo valor de aparência — incluindo os defaults listados abaixo
e os estados dinâmicos de cor da seção 3.5 (`cor_inativo` e `cor_alerta`,
conforme ADR-0004) — deve vir do schema de estilo em tempo de execução, já
resolvido pelo loader a partir de `config/estilo.json`.
Hardcoding de qualquer campo desta seção é violação contratual.

Como biblioteca global, `config/estilo.json` contém aparência compartilhada,
incluindo bordas, forma visual de chips, indicadores, cores globais e demais
campos universais vigentes. Não pertencem a `config/estilo.json`:

- textos concretos de cabeçalho;
- parâmetros locais de apresentação do cabeçalho;
- composição de tela;
- conteúdo de tela;
- instâncias de `console`, `dashboard`, `lancador` ou `barra_de_menus`;
- destinos, ações, bindings ou regras locais de uma tela.

Esses elementos são configuração concreta da tela e pertencem ao JSON
estrutural da respectiva tela. O estado vivo da execução também não pertence
à biblioteca global de estilo.

**Consumidores**: loader ou camada equivalente, renderer e demais componentes
que precisem de valores de aparência. A sessão carrega, valida e realiza a
materialização inicial a partir de `config/estilo.json`. Consumidores recebem
o objeto de estilo resolvido — não relêem o arquivo em cada render. A
ADR-0046 substitui a limitação de carga/materialização única por sessão: uma
aplicação explicitamente confirmada e persistida pode publicar uma nova
materialização global de forma controlada, conforme as seções 3.8 e 4.

**Não pertencem à autoridade de `config/estilo.json`**: estado vivo de cursor
corrente, itens incluídos em seleção, foco de corpo, página atual, modo verboso
ativo, navegação e seleção em progresso. Esses são estados de execução, não
configuração de aparência.

Esta regra vem de `docs/nomenclatura/10_ESTILO.md` §2 e ADR-0030 D1.

---

## 3. Schema de estilo

### 3.1 Borda

Sete campos obrigatórios. Todos são do tipo **caractere**.

| Campo | Função |
|---|---|
| `traco_superior` | Caractere da linha superior da moldura |
| `traco_inferior` | Caractere da linha inferior da moldura |
| `canto_superior_esquerdo` | Canto superior esquerdo da moldura |
| `canto_superior_direito` | Canto superior direito da moldura |
| `canto_inferior_esquerdo` | Canto inferior esquerdo da moldura |
| `canto_inferior_direito` | Canto inferior direito da moldura |
| `lateral` | Caractere das colunas esquerda e direita da moldura |

**Invariante estrutural**: o espaço da moldura sempre existe; o que muda entre
estilos de borda é apenas o caractere de preenchimento de cada campo.
O schema não deve suprimir campos — mesmo que um estilo use o mesmo caractere
em múltiplos campos, cada campo continua declarado separadamente.

**Presets obrigatórios de borda**: três conjuntos nomeados ("Borda Curva",
"Borda Reta", "Linha") devem estar presentes na camada de dados. Valores
concretos em `config/estilo.json`, seção `borda.presets`.

**Catálogo e opção ativa (ADR-0030 D2)**: o campo `borda.preset_default` é
obrigatório em `config/estilo.json` e identifica o preset ativo. Ausência
de `preset_default`, referência a preset inexistente no catálogo ou catálogo
vazio são erros de validação — sem fallback silencioso.

**Materialização (ADR-0030 D3/D8)**: o loader resolve o preset ativo de
`borda.presets[preset_default]` e produz os sete campos de runtime listados
acima. A configuração parcialmente resolvida não pode ser usada.

**Preservação visual inicial (ADR-0030 D4)**: o preset `"Borda Curva"` é o
preset ativo inicial — correspondência verificada com os caracteres que estavam
hardcoded em `_BORDAS["curva"]` no renderer anterior ao H-0039 (estado
histórico; levantamento, seção 3.2 da ADR-0030). O renderer vigente recebe o
estilo global já resolvido; os sete campos de borda vêm de `EstiloResolvido`.
O renderer não mantém catálogo próprio nem escolhe preset. `_BORDAS` e
`tipo_borda` não pertencem ao estado executável vigente.

### 3.2 Chip

Cinco campos obrigatórios.

| Campo | Função | Tipo |
|---|---|---|
| `caractere_esquerdo` | Caractere de abertura do chip | caractere |
| `caractere_direito` | Caractere de fechamento do chip | caractere |
| `cor_texto` | Cor do texto/tecla do chip | nome semântico de cor (string) |
| `caixa_alta` | Texto em maiúscula (`True`) ou não (`False`) | booleano |
| `cor_fundo` | Cor de fundo do chip | nome semântico de cor (string) |

`cor_texto` e `cor_fundo` são nomes semânticos de cor — ex.: `"azul"`,
`"verde"`, `"padrão"` (sem cor diferenciada). A tradução desse nome para
o valor real de terminal (ANSI, paleta, etc.) é responsabilidade exclusiva
do renderer, nunca do schema de estilo.

**Presets obrigatórios de chip**: sete conjuntos nomeados ("Colchete",
"Curva", "Ornamental", "Traço", "Ponto", "Destaque Texto", "Destaque Fundo")
devem estar presentes na camada de dados. Valores concretos em
`config/estilo.json`, seção `chip.presets`.

**Catálogo e opção ativa (ADR-0030 D2)**: o campo `chip.preset_default` é
obrigatório em `config/estilo.json` e identifica o preset ativo. Ausência
de `preset_default`, referência a preset inexistente ou catálogo vazio são
erros de validação — sem fallback silencioso.

**Materialização (ADR-0030 D3/D8)**: o loader resolve o preset ativo de
`chip.presets[preset_default]` e produz os cinco campos de runtime listados
acima. A configuração parcialmente resolvida não pode ser usada.

**Preservação visual inicial (ADR-0030 D5)**: o preset `"Colchete"` é o
preset ativo inicial. Os delimitadores `[` e `]` correspondem exatamente ao
formato hardcoded `"[{tecla}]"` no renderer atual. `cor_texto: "padrão"` e
`cor_fundo: "padrão"` não introduzem nova cor concreta.

**`caixa_alta` é declarado por cada preset individualmente.** Não existe valor
global de `caixa_alta` independente do preset. O preset `"Colchete"` usa
`caixa_alta: false` para preservar a capitalização atual dos rótulos dos chips
("Sair", "Voltar", "Ajuda", "Verboso") — a mudança de `true` para `false` em
`config/estilo.json` pertence ao handoff do Bloco 1 (ADR-0030 D5).

`caractere_esquerdo` e `caractere_direito` sempre ocupam posição (nunca
vazios): espaço representa "sem moldura visível", não ausência de campo —
invariante equivalente ao da borda (seção 3.1).

"Destaque Texto" e "Destaque Fundo" compartilham os mesmos delimitadores —
a distinção visual primária vem da cor aplicada (`cor_texto` vs
`cor_fundo`), não da moldura.

O preset "Destaque Texto" (`DEC-ITEM0010-CHIP-04`) altera somente a cor do
texto/conteúdo da unidade visual. O fundo normal do terminal é mantido em
toda a unidade: um espaço normal à esquerda, o conteúdo com foreground na
cor de destaque e um espaço normal à direita. A representação semântica é
` PgUp/PgDn `: espaço esquerdo, conteúdo e espaço direito usam o fundo
normal; somente `PgUp/PgDn` recebe a cor de destaque no foreground. Não
existe fundo de destaque no lado direito nem assimetria de fundo. Essa
semântica não exige `cor_fundo_esquerdo` nem `cor_fundo_direito`; esses
campos não integram o schema vigente.

O preset "Destaque Fundo" permanece intacto: `cor_fundo` aplica-se
simetricamente à unidade.

**Composição multitecla (ADR-0046).** Quando uma ação de chip é representada
por duas ou mais teclas, a composição visual (unidade única, separador `/`,
delimitadores externos) é regida por `contrato_chip.md` seção 10.1-10.5
(`DEC-ITEM0010-CHIP-01`, `-02`, `-05`, `-06`). Este contrato permanece a
autoridade do schema de campos e presets; a composição estrutural da
unidade multitecla não é duplicada aqui, para evitar mecanismo concorrente.

### 3.3 Indicadores

Três indicadores. Cada um tem natureza própria e defaults especificados.
Todos os valores de símbolo são defaults configuráveis — nunca fixos em código.

#### `concluido` — par on/off

O schema deve expor os dois campos: `concluido_on` e `concluido_off`.
Ambos são restritos a exatamente **1 caractere** — regra de alinhamento
colunar, aplicável a todos os símbolos do sistema (ver R-6).
Valores concretos em `config/estilo.json`, seção `indicadores.concluido`.

#### `selecionado` — símbolo único, condicional

`selecionado` só é renderizado quando o cursor está sobre o item.
O schema deve expor dois campos: `selecionado_simbolo` e `selecionado_off`.
`selecionado_off` garante alinhamento colunar quando o indicador não está
ativo. Ambos são restritos a exatamente **1 caractere** (ver R-6).
Quatro presets nomeados ("Seta" é o default). Valores concretos em
`config/estilo.json`, seção `indicadores.selecionado`.

#### `incluido` — par on/off

O schema deve expor os dois campos: `incluido_on` e `incluido_off`.
Quatro presets nomeados ("Círculo" é o default). Valores concretos em
`config/estilo.json`, seção `indicadores.incluido`.

#### Transformação de preset para campos de runtime

O indicador `incluido` é armazenado em `config/estilo.json` em estrutura
aninhada (`preset_default` + `presets`). O indicador `selecionado` tem
armazenamento misto: o símbolo ativo vem da estrutura de preset, enquanto o
estado off vem do campo direto `indicadores.selecionado.off`. O indicador
`concluido` é armazenado diretamente como par de campos (`on`/`off`), sem
estrutura de preset. Em todos os casos, o loader é responsável por
materializar os campos planos esperados pelo schema em runtime:

- `concluido`: lê `indicadores.concluido.on` e `indicadores.concluido.off`
  em `config/estilo.json` → produz `concluido_on` e `concluido_off` no schema
  de runtime.
- `selecionado`: lê `indicadores.selecionado.preset_default` → busca em
  `indicadores.selecionado.presets` → extrai `simbolo` → produz
  `selecionado_simbolo`; lê `indicadores.selecionado.off` → produz
  `selecionado_off`.
- `incluido`: lê `preset_default` → busca em `presets` → extrai `on` e `off`
  → produz campos de runtime `incluido_on` e `incluido_off`.

Os campos planos de runtime (`concluido_on`, `concluido_off`,
`selecionado_simbolo`, `selecionado_off`, `incluido_on`, `incluido_off`) são
os que o schema valida e o renderer usa. A estrutura de presets em
`config/estilo.json` é forma de armazenamento, não o formato de runtime.
Não alterar os valores dos presets com base nessa resolução — o loader
transforma, não substitui.

### 3.4 Tiling

Um campo obrigatório. Tipo: enumeração de string.

| Campo | Valores possíveis |
|---|---|
| `tiling` | `sobreposto` \| `lado_a_lado` |

Representa a preferência manual do usuário para a organização de múltiplos
objetos tipo `console`/`lancador` no corpo da tela. Não é calculado a partir
da largura do terminal — é lido do schema de estilo como qualquer outro campo.

Não existe valor de largura de terminal que force `sobreposto`: a preferência
do usuário é respeitada sempre, mesmo em terminal muito estreito.

**Materialização em `config/estilo.json`**: `tiling` é campo obrigatório do
schema de estilo em tempo de execução. Enquanto a preferência do usuário não
for decidida, o campo pode não estar materializado com valor concreto em
`config/estilo.json` — essa ausência é pendência de configuração/preferência,
não omissão silenciosa do schema. Quando um valor for decidido, deve ser
registrado em `config/estilo.json`. Tratamento análogo ao de `cor_inativo` e
`cor_alerta` (seção 3.5).

### 3.5 Estados dinâmicos de cor

Dois campos obrigatórios. Aplicam-se a qualquer chip ou indicador do sistema
quando houver estado dinâmico correspondente — não são específicos de um chip
isolado.

| Campo | Função | Tipo |
|---|---|---|
| `cor_inativo` | Cor aplicada quando um elemento existe mas está temporariamente inativo | nome semântico de cor (string) |
| `cor_alerta` | Cor aplicada a elemento operável em estado de destaque, ou quando um valor/limite exige atenção | nome semântico de cor (string) |

```yaml
cor_inativo:
  valor_concreto: cinza
  uso: elemento_existente_mas_nao_operavel

cor_alerta:
  valor_concreto: amarelo
  uso:
    - elemento_operavel_em_estado_de_destaque
    - valor_ou_limite_que_exige_atencao
```

`cor_inativo` e `cor_alerta` são nomes semânticos de cor. A tradução desse
nome para o valor real de terminal (ANSI, paleta, etc.) é responsabilidade
exclusiva do renderer, nunca do schema de estilo (R-7).

**Distinção ativo × destacado (ADR-0037)**:

- um elemento pode estar ativo e simultaneamente destacado;
- `cor_alerta` não implica inatividade;
- `[Ins] Dry-Run` ligado é a primeira especialização focal dessa distinção —
  não é regra universal de todos os toggles;
- os valores concretos existem em `config/estilo.json` (`cor_inativo: "cinza"`,
  `cor_alerta: "amarelo"`);
- a materialização pelo loader em `EstiloResolvido` e o consumo pelo renderer
  pertencem ao futuro handoff/implementação — este contrato não declara que
  loader ou renderer já implementam a nova capacidade;
- o estado vivo que determina o destaque (ex.: `dry_run_ativo`) não pertence
  ao estilo global nem a `config/estilo.json`.

**Preservação de `cor_inativo` (ADR-0046).** Chip existente funcionalmente
ativo usa a aparência ativa; chip existente funcionalmente inativo usa
`cor_inativo`. Composição, preset e aplicação de `cor_texto`/`cor_fundo`
não apagam, sobrepõem nem neutralizam `cor_inativo`. Isso vale inclusive
para Páginas e para `Enter/Aplicar` quando inativos. Esta preservação não
cria política nova de estado.

**Distinção fundamental (ADR-0004)**:

- **Existência** de um elemento = propriedade estrutural, declarada pela
  classe de tela. A classe decide se o chip ou indicador existe naquela tela.
- **Ativo/inativo e alerta** = estados dinâmicos de renderização, recalculados
  a cada render a partir do conteúdo atual. O renderer aplica a cor
  correspondente, mas não decide a existência estrutural do elemento.

### 3.6 Preservação visual inicial (ADR-0030)

Os presets ativos iniciais preservam a aparência vigente antes da migração:

| Categoria | Preset ativo inicial | Campos relevantes |
|---|---|---|
| `borda` | `"Borda Curva"` | sete caracteres: `╭` `╮` `╰` `╯` `─` `│` |
| `chip` | `"Colchete"` | `[`, `]`, `caixa_alta: false`, `cor_texto: "padrão"`, `cor_fundo: "padrão"` |
| `indicadores.selecionado` | `"Seta"` | `simbolo: →`, `selecionado_off: (espaço)` |
| `indicadores.incluido` | `"Círculo"` | `on: ●`, `off: ○` |
| `indicadores.concluido` | par direto | `on: ✓`, `off: (espaço)` |

O literal `"padrão"` em `cor_texto` e `cor_fundo` significa ausência de cor
diferenciada — preserva o comportamento atual do renderer, que não aplica
cor especial a chips. Os valores concretos de `cor_inativo` (`cinza`) e
`cor_alerta` (`amarelo`) existem em `config/estilo.json` (ADR-0037 para
`cor_alerta`; `cor_inativo` já materializado anteriormente). A materialização
completa pelo loader e o consumo pelo renderer de `cor_alerta` permanecem
para o Handoff 4.

### 3.7 Fronteira com implementação (ADR-0030)

**Na aplicação documental da ADR-0030** (estado histórico), as seguintes
decisões ainda não tinham sido realizadas — pertenciam ao handoff de
implementação do Bloco 1. A aplicação documental, isoladamente, não implementou
código.

- localização, nome e assinatura do loader de estilo;
- assinatura do objeto de estilo resolvido (estrutura dos campos de runtime);
- mecanismo de armazenamento do objeto por sessão;
- transição interna do parâmetro `tipo_borda` durante a migração;
- unidade técnica da validação de "exatamente 1 caractere" (R-6): code point,
  grapheme cluster ou largura visual de terminal;
- mecanismo de detecção de duplicidade de chaves no JSON bruto;
- inclusão de `preset_default: "Borda Curva"` na seção `borda` de
  `config/estilo.json`;
- inclusão de `preset_default: "Colchete"` na seção `chip` de
  `config/estilo.json`;
- mudança de `chip.presets["Colchete"].caixa_alta` de `true` para `false`
  em `config/estilo.json`;
- remoção de `_BORDAS` e do parâmetro `tipo_borda` do renderer;
- atualização dos testes que verificam constantes hardcoded de borda e chip;
- promoção de `_meta.status` em `config/estilo.json` (critério não definido).

**Distinção temporal — ciclo posterior H-0039:**

```yaml
aplicacao_documental_ADR_0030:
  implementacao_executada_naquela_etapa: false

ciclo_posterior_H_0039:
  carregamento_global: implementado
  materializacao_runtime: implementada
  renderer_migrado: true
  hardcodings_do_escopo_removidos: true
```

As capacidades normatizadas pela ADR-0046 continuam fora do estado
implementado nesta etapa documental:

- tela de escolha de estilo;
- persistência da escolha;
- troca controlada de estilo durante a sessão;

Seu comportamento normativo deixa de ser pendência documental e passa a ser
regido pela seção 3.8 e pelas regras de uso deste contrato. Continuam como
pendências futuras não abrangidas pela ADR-0046:

- materialização de `cor_alerta` pelo loader e consumo pelo renderer
  (valor concreto já em `config/estilo.json`; ADR-0037 / Handoff 4);
- `tiling`;
- Blocos 2 e 3;
- promoção de `_meta.status`.

`cor_inativo: "cinza"` permanece materializado em `config/estilo.json`.
O consumo completo de `cor_alerta` pelo runtime foi concluído e validado pelo H-0044; a capacidade correspondente do ITEM-0011 está encerrada.

### 3.8 Estados, materialização, persistência e publicação (ADR-0046)

O ciclo de estilo distingue normativamente quatro estados:

| Estado | Definição e fronteira |
|---|---|
| Configuração persistida | Configuração concreta global e completa mantida em `config/estilo.json`; é a autoridade persistida e não contém estado vivo da sessão. |
| Materialização global vigente | Único objeto integralmente resolvido que os consumidores globais usam na execução corrente. |
| Configuração candidata | Estado de runtime separado, derivado da configuração persistida e acumulador das escolhas ainda não publicadas; não é configuração persistida nem estilo global vigente. |
| Override local de demonstração | Materialização temporária derivada do candidato e limitada à apresentação da demonstração e de seu pop-up; não substitui o estilo global vigente nem vaza para outros consumidores. |

A sessão produz a materialização global inicial a partir da configuração
persistida. O candidato pode ser materializado integralmente para validação e
demonstração sem publicação. Candidato e override local não contam como
estilos globais concorrentes: em cada instante há somente uma materialização
global vigente.

No caminho confirmado, o chamador deve primeiro persistir uma configuração
completa e válida e somente depois publicar, por substituição controlada, a
materialização global correspondente. A substituição é atômica do ponto de
vista dos consumidores: nenhum deles observa objeto global parcialmente
alterado. Este contrato não impõe algoritmo físico específico de gravação.

Para o `ITEM-0010` atual, somente os `preset_default` das categorias expostas
`borda`, `chip`, `indicadores.selecionado` e `indicadores.incluido` são
alterados; todos os demais valores persistidos permanecem preservados. Antes
da publicação, o conteúdo gravado deve representar integralmente a
configuração escolhida e ser válido segundo este contrato.

Falha de persistência não confirma a aplicação nem publica o candidato. A
configuração persistida anterior e a materialização global anterior permanecem
vigentes, e o candidato continua disponível como estado de runtime para nova
tentativa ou edição.

No fluxo do `ITEM-0010`, o resultado `ABORTADO` do pop-up de demonstração
encerra a demonstração e retorna à tela de seleção de estilos. A configuração
candidata é preservada integralmente; a baseline persistida — a última
configuração persistida conhecida pelo fluxo — permanece inalterada, assim
como o estilo global materializado vigente. Nenhuma persistência é realizada.
`ABORTADO` cancela somente a tentativa de aplicação, não a edição do
candidato.

Após `CONFIRMADO`, persistência completa e válida e publicação bem-sucedida do
novo estilo global, a configuração recém-persistida passa a ser a nova
baseline persistida do fluxo. O candidato deve ser atualizado e sincronizado
com essa mesma configuração, de modo que candidato e baseline sejam
semanticamente equivalentes. O novo estilo permanece globalmente vigente, o
fluxo retorna à tela de seleção e recalcula o estado contextual de
`Enter/Aplicar`; como não há divergência nesse instante, a ação fica inativa.
Edições posteriores passam a ser comparadas contra essa nova baseline. Uma
aplicação confirmada anteriormente não é desfeita por alterações posteriores
que sejam abandonadas sem nova confirmação.

---

## 4. Regras de uso

**R-1. Unicidade do schema em tempo de execução.**
Existe exatamente uma materialização global de estilo vigente em cada
instante. Todas as classes de tela e todos os renderers fora de uma
demonstração sob override leem desse objeto. Candidato e override local não
são estilos globais concorrentes.

**R-2. Proibição de hardcoding.**
Decorre da seção 2 deste contrato. Aplica-se a qualquer símbolo, cor,
caractere ou valor de enumeração dos grupos borda, chip, indicadores e
tiling, bem como aos estados dinâmicos de cor da seção 3.5 (`cor_inativo` e
`cor_alerta`, conforme ADR-0004) — sem exceção para "valores óbvios" ou
"padrões universais".

**R-3. Completude do schema.**
Um schema de estilo que omita qualquer campo obrigatório listado nas seções
3.1, 3.2, 3.3, 3.4 e 3.5 é inválido e não deve ser aceito pelo sistema.

**R-4. Substituição controlada em tempo de execução (ADR-0046).**
O objeto global vigente não é mutado parcialmente. Após persistência completa,
válida e bem-sucedida, ele pode ser substituído de forma controlada durante a
sessão, e os consumidores passam a usar imediatamente a nova materialização,
sem exigir reconstrução integral da tela ou reinício da execução.

**R-5. Independência de tela e classe.**
O schema não carrega referência a nenhuma tela ou classe específica. É
universal por definição (`docs/nomenclatura/10_ESTILO.md`).

**R-6. Restrição de comprimento de símbolos.**
Todo campo de símbolo ou caractere do schema (borda, chip, indicadores) é
restrito a exatamente 1 caractere. Strings de comprimento diferente de 1 são
inválidas. A restrição existe para preservar alinhamento colunar em toda a
saída do sistema.

**R-7. Responsabilidade de tradução de cor.**
O schema armazena nomes semânticos de cor (strings). Nenhuma lógica de
tradução de nome semântico para valor de terminal (ANSI, paleta, RGB, etc.)
reside no schema ou nas classes de tela — essa responsabilidade é exclusiva
do renderer.

**R-8. Tiling é escolha do usuário, não decisão automática.**
O renderer não sobrescreve `tiling` com base em largura de terminal ou
qualquer outra condição de ambiente. Não existe lógica de fallback que force
`sobreposto` em terminais estreitos. O valor lido do schema é usado
diretamente, sem exceção.

**R-9. `preset_default` obrigatório em categorias com catálogo (ADR-0030 D2).**
As categorias `borda`, `chip`, `indicadores.selecionado` e
`indicadores.incluido` devem possuir campo `preset_default` em
`config/estilo.json`. A ausência de `preset_default`, a referência a preset
inexistente no catálogo e o catálogo vazio são erros de validação. Não existe
fallback silencioso — configuração inválida não produz estilo degradado.

**R-10. Materialização inicial e materializações de aplicação (ADR-0030 D8;
ADR-0046).**
A sessão carrega `config/estilo.json`, valida a estrutura, resolve todas as
seções e produz a materialização global inicial. Não relê o arquivo em cada
chamada de renderização. Materializações adicionais são admitidas para validar
ou demonstrar um candidato sem publicá-lo e, após aplicação confirmada e
persistida com sucesso, para substituir o único estilo global vigente.
Configuração parcialmente resolvida não pode ser usada pelo renderer nem por
nenhum consumidor de aparência.

**R-11. Ordem de persistência e publicação (ADR-0046).**
A publicação do candidato obedece obrigatoriamente à ordem persistência
completa e válida → substituição da materialização global. Falha de
persistência mantém a configuração persistida anterior e o estilo global
anterior como vigentes.

**R-12. Isolamento de candidato e override (ADR-0046).**
Editar ou demonstrar um candidato não persiste configuração e não altera o
estilo global vigente. O override local pertence apenas à apresentação da
demonstração e de seu pop-up e deve cessar ao sair desse contexto.

**R-13. Transições do fluxo de aplicação do `ITEM-0010` (ADR-0046).**
`ABORTADO` encerra a demonstração, retorna à seleção, preserva integralmente o
candidato e deixa inalterados a baseline persistida e o estilo global vigente;
ele cancela somente a tentativa de aplicação. Depois de `CONFIRMADO` seguido
de persistência completa e válida e publicação bem-sucedida, a configuração
persistida torna-se a nova baseline, o candidato é equalizado a ela, o estilo
global publicado permanece vigente e `Enter/Aplicar` fica inativo por ausência
de divergência. Qualquer edição posterior é comparada contra essa nova
baseline.

**R-14. Composição multitecla e contenção de estilo (ADR-0046).**
Quando um chip representa ação multitecla, a composição segue a unidade
única definida em `contrato_chip.md` seção 10.1: delimitadores do preset
somente nas extremidades externas, teclas separadas pelo caractere canônico
`/` (seção 10.3), sem delimitador completo independente por tecla. Cor e
fundo do chip ficam contidos à unidade visual do chip; não vazam para o
texto descritivo da ação nem para o chip seguinte. Esta regra se aplica à
`barra_de_menus` real, não somente à demonstração de estilo. Composição,
preset e contenção não neutralizam `cor_inativo` (seção 3.5).

**R-15. Largura visual efetiva (ADR-0046).**
A composição e o alinhamento de chips, incluindo unidades multitecla,
consideram a largura visual efetiva ocupada no terminal; sequências ANSI
usadas para cor não ocupam célula e não entram nessa largura. A unidade
técnica de medição não é fixada por este contrato (mesma fronteira da seção
3.7).

---

## 5. Critérios de validação

- [ ] Todo acesso a símbolo, cor ou caractere de borda, chip, indicador ou
      estado dinâmico de cor em qualquer classe ou renderer é feito
      exclusivamente via objeto de estilo — nenhuma string ou constante de
      estilo aparece hardcoded no código-fonte.
- [ ] O schema rejeita (ou registra erro) quando instanciado sem algum dos
      campos obrigatórios de borda (7), chip (5), indicadores (6 campos:
      `concluido_on`, `concluido_off`, `selecionado_simbolo`, `selecionado_off`,
      `incluido_on`, `incluido_off`) ou estados dinâmicos de cor (2 campos:
      `cor_inativo`, `cor_alerta`).
- [ ] `cor_inativo` e `cor_alerta` são nomes semânticos de cor (strings) —
      nenhum valor hardcoded de terminal (ANSI, RGB, etc.) aparece nesses
      campos no schema ou nas classes de tela.
- [ ] O schema rejeita (ou registra erro) qualquer campo de símbolo/caractere
      com comprimento diferente de 1 (R-6).
- [ ] Os valores de indicadores carregados pelo schema vêm exclusivamente de
      `config/estilo.json` — nenhum símbolo de indicador aparece hardcoded no
      renderer nem nas classes.
- [ ] Dado um objeto de estilo com valores substituídos, o renderer produz
      saída com os valores fornecidos, não com os defaults.
- [ ] Nenhuma classe de tela altera o objeto de estilo recebido.
- [ ] A sessão cria a materialização global inicial a partir da configuração
      válida de `config/estilo.json` e mantém exatamente uma materialização
      global vigente em cada instante.
- [ ] Materializar, editar ou demonstrar um candidato não altera a
      materialização global vigente nem persiste estado vivo no JSON.
- [ ] O override do candidato alcança somente a demonstração e seu pop-up e
      deixa de ser consumido quando esse contexto termina.
- [ ] Para o `ITEM-0010`, somente os `preset_default` das quatro categorias
      expostas são modificados, com preservação integral dos demais valores.
- [ ] A publicação ocorre somente depois de a configuração escolhida estar
      completa, válida e persistida com sucesso.
- [ ] Falha de persistência preserva a configuração persistida anterior e a
      materialização global anterior, sem descartar o candidato.
- [ ] Chip que representa ação multitecla é composto como unidade visual
      única, com delimitadores do preset apenas nas extremidades e teclas
      separadas por `/` — sem delimitador completo por tecla
      (`contrato_chip.md` seção 10.1).
- [ ] Cor ou fundo aplicados a um chip não aparecem no texto descritivo da
      ação nem no chip seguinte.
- [ ] Chip existente funcionalmente inativo usa `cor_inativo`; composição,
      preset e aplicação de cor/fundo não a neutralizam.
- [ ] O alinhamento e a largura de chips usam largura visual efetiva,
      desconsiderando sequências ANSI que não ocupam célula.
- [ ] O renderer traduz nomes semânticos de cor para valores de terminal — o
      schema não contém nenhuma lógica de tradução de cor (R-7).
- [ ] Os três presets de borda ("Borda Curva", "Borda Reta", "Linha") estão
      presentes em `config/estilo.json` e correspondem exatamente à seção
      `borda.presets` desse arquivo.
- [ ] Os sete presets de chip ("Colchete", "Curva", "Ornamental", "Traço",
      "Ponto", "Destaque Texto", "Destaque Fundo") estão presentes em
      `config/estilo.json` e correspondem exatamente à seção `chip.presets`
      desse arquivo.
- [ ] `tiling` aceita apenas `"sobreposto"` ou `"lado_a_lado"`; qualquer
      outro valor é inválido.
- [ ] O renderer não altera `tiling` com base em largura de terminal —
      o valor do schema é usado diretamente, sem fallback automático (R-8).
- [ ] O loader produz erro explícito e interrompe a inicialização quando
      `config/estilo.json` está ausente — sem fallback silencioso (ADR-0030 D9).
- [ ] O loader produz erro explícito quando `config/estilo.json` contém
      JSON inválido (parse error) (ADR-0030 D9).
- [ ] O loader produz erro explícito quando uma seção obrigatória (`borda`,
      `chip`, `indicadores`) está ausente (ADR-0030 D9).
- [ ] O loader produz erro explícito quando `preset_default` está ausente em
      categoria com catálogo (`borda`, `chip`, `indicadores.selecionado`,
      `indicadores.incluido`) (ADR-0030 D9, R-9).
- [ ] O loader produz erro explícito quando o catálogo de uma categoria
      obrigatória está vazio (ADR-0030 D9).
- [ ] O loader produz erro explícito quando o preset referenciado por
      `preset_default` não existe no catálogo — sem fallback para outro preset
      (ADR-0030 D9).
- [ ] O loader produz erro explícito quando campos obrigatórios do preset
      escolhido estão ausentes (ADR-0030 D9).
- [ ] O loader produz erro explícito quando o tipo de um campo é inválido
      (ex.: não-booleano em `caixa_alta`, não-string em `caractere_esquerdo`)
      (ADR-0030 D9).
- [ ] O loader produz erro explícito quando símbolo ou caractere obrigatório
      é string vazia (ADR-0030 D9).
- [ ] Configuração parcialmente resolvida não é aceita — erro explícito; nenhum
      consumidor recebe objeto de estilo incompleto (ADR-0030 D9, R-10).
- [ ] Duplicidade de identificadores ou nomes que permaneça observável na
      estrutura materializada produz erro explícito (ADR-0030 D9).
- [ ] O contrato não redefine "1 caractere" como code point, grapheme cluster
      ou largura visual — essa unidade técnica pertence ao handoff (ADR-0030 D9).
