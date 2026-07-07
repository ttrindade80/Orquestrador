---
name: contrato-estilo
description: Schema e regras do módulo de estilo universal — borda, chip, indicadores e tiling
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#1-estilo-universal"
    reaproveitado_de_legado: false
---

# Contrato — Módulo de Estilo

## 1. Objetivo

Especificar o schema de estilo universal do sistema novo: os campos que
compõem borda, chip, indicadores e tiling, e as regras de uso que vinculam
todos os módulos a esse schema.

Este contrato cobre exclusivamente a seção 1 ("Estilo — universal") de
`docs/NOMENCLATURA.md`. Composição de corpo (`contrato_composicao_corpo.md`,
`ativo`) e barra_de_menus (`contrato_barra_de_menus.md`, `ativo`) são módulos
separados com contratos próprios. Os demais domínios devem ser tratados em
contratos próprios quando formalizados.

---

## 2. Regra fundamental (formal, não observação)

**Nenhuma classe de tela ou renderer pode hardcodar símbolo, cor ou caractere
pertencente a esta especificação.** Todo valor de estilo — incluindo os
defaults listados abaixo e os estados dinâmicos de cor da seção 3.5
(`cor_inativo` e `cor_alerta`, conforme ADR-0004) — deve vir do schema de
estilo em tempo de execução.
Hardcoding de qualquer campo desta seção é violação contratual.

Esta regra vem de `docs/NOMENCLATURA.md` seção 1, parágrafo de abertura e
parágrafo final da seção 1.3.

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

`caixa_alta: true` é o default de todos os presets — regra geral, não
exceção por preset.

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
universal por definição (NOMENCLATURA.md seção 1, abertura).

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
