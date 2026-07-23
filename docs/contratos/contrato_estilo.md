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
      - docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
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
ADR-0022, a tela inicial real poderá exibir acesso a estilos na
`barra_de_menus`, mas a tela funcional de estilos, troca de borda, troca de
envelope de chips e persistência da seleção de estilo continuam fora deste
contrato e de sua aplicação documental.

---

## 2. Regra fundamental e autoridade global (formal, não observação)

**`config/estilo.json` é a autoridade global exclusiva para a aparência
compartilhada do terminal (ADR-0030 D1).** A escolha de aparência é global —
não é possível escolha diferente por tela neste modelo. Nenhuma classe de tela
ou renderer pode hardcodar símbolo, cor ou caractere pertencente a esta
especificação. Todo valor de aparência — incluindo os defaults listados abaixo
e os estados dinâmicos de cor da seção 3.5 (`cor_inativo` e `cor_alerta`,
conforme ADR-0004) — deve vir do schema de estilo em tempo de execução, já
resolvido pelo loader a partir de `config/estilo.json`.
Hardcoding de qualquer campo desta seção é violação contratual.

**Consumidores**: loader ou camada equivalente, renderer e demais componentes
que precisem de valores de aparência. O loader carrega, valida e materializa
o estilo uma única vez por sessão (ADR-0030 D8). Consumidores recebem o
objeto de estilo resolvido — não relêem `config/estilo.json` em cada render.

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

"Destaque Texto" e "Destaque Fundo" compartilham os mesmos delimitadores
— a distinção visual vem exclusivamente da cor aplicada (`cor_texto` vs
`cor_fundo`), não da moldura.

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
| `cor_alerta` | Cor aplicada quando um valor ou limite exige destaque visual | nome semântico de cor (string) |

`cor_inativo` e `cor_alerta` são nomes semânticos de cor — ex.: `"cinza"`,
`"amarelo"`, `"padrão"` (sem cor diferenciada). A tradução desse nome para
o valor real de terminal (ANSI, paleta, etc.) é responsabilidade exclusiva
do renderer, nunca do schema de estilo (R-7).

**Escopo de materialização em `config/estilo.json`**: o arquivo
`config/estilo.json` contém os valores concretos já decididos para presets de
estilo. A obrigatoriedade de `cor_inativo` e `cor_alerta` vale para o schema de
estilo em tempo de execução. Enquanto seus valores concretos não forem
definidos, eles permanecem documentados como campos obrigatórios do schema, mas
não como presets materializados no JSON.

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
cor especial a chips. Os valores de `cor_inativo` e `cor_alerta` não possuem
valor decidido neste ciclo (pendência registrada em `_meta` de
`config/estilo.json` e nas decisões deferidas da ADR-0030).

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

Continuam fora do estado implementado (pendências futuras):

- tela de escolha de estilo;
- persistência de escolha;
- troca de estilo durante sessão;
- `cor_inativo`;
- `cor_alerta`;
- `tiling`;
- Blocos 2 e 3;
- promoção de `_meta.status`.

---

## 4. Regras de uso

**R-1. Unicidade do schema em tempo de execução.**
Existe exatamente um objeto de estilo ativo por sessão. Todas as classes de
tela e todos os renderers leem desse objeto — nenhum mantém cópia local de
valores de estilo.

**R-2. Proibição de hardcoding.**
Decorre da seção 2 deste contrato. Aplica-se a qualquer símbolo, cor,
caractere ou valor de enumeração dos grupos borda, chip, indicadores e
tiling, bem como aos estados dinâmicos de cor da seção 3.5 (`cor_inativo` e
`cor_alerta`, conforme ADR-0004) — sem exceção para "valores óbvios" ou
"padrões universais".

**R-3. Completude do schema.**
Um schema de estilo que omita qualquer campo obrigatório listado nas seções
3.1, 3.2, 3.3, 3.4 e 3.5 é inválido e não deve ser aceito pelo sistema.

**R-4. Imutabilidade em tempo de execução.**
O schema de estilo não é alterado enquanto uma tela está aberta. Mudança de
estilo requer reconstrução da tela.

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

**R-10. Carregamento único e materialização integral (ADR-0030 D8).**
O loader carrega `config/estilo.json` uma única vez por sessão. Valida a
estrutura, resolve todas as seções e produz a representação de runtime. Não
relê `config/estilo.json` em cada chamada de renderização. Configura-
ção parcialmente resolvida não pode ser usada pelo renderer nem por nenhum
consumidor de aparência.

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
