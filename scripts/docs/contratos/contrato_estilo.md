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
`docs/NOMENCLATURA.md`. Composição de corpo, barra_de_menus e layout são
contratos separados, ainda não escritos.

---

## 2. Regra fundamental (formal, não observação)

**Nenhuma classe de tela ou renderer pode hardcodar símbolo, cor ou caractere
pertencente a esta especificação.** Todo valor de estilo — incluindo os
defaults listados abaixo — deve vir do schema de estilo em tempo de execução.
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

**Conjuntos obrigatórios de borda** (exemplos canônicos; não esgotam os
valores possíveis, mas devem estar presentes como presets nomeados):

| Campo | "Borda Curva" | "Borda Reta"  | "Linha" |
|---|---|---|---|
| `canto_superior_esquerdo` | `╭` | `┌` | `─` |
| `canto_superior_direito` | `╮` | `┐` | `─` |
| `canto_inferior_esquerdo` | `╰` | `└` | `" "` |
| `canto_inferior_direito` | `╯` | `┘` | `" "` |
| `traco_superior` | `─` | `─` | `─` |
| `traco_inferior` | `─` | `─` | `" "` |
| `lateral` | `│` | `│` | `" "` |

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

**Conjuntos obrigatórios de chip** (exemplos canônicos; não esgotam os
valores possíveis, mas devem estar presentes como presets nomeados):

| Campo | "Colchete" | "Curva" | "Ornamental" | "Traço" | "Ponto" | "Destaque Texto" | "Destaque Fundo" |
|---|---|---|---|---|---|---|---|
| `caractere_esquerdo` | `[` | `╭` | `❲` | `-` | `" "` | `" "` | `" "` |
| `caractere_direito` | `]` | `╮` | `❳` | `-` | `.` | `" "` | `" "` |
| `cor_texto` | `"padrão"` | `"padrão"` | `"padrão"` | `"padrão"` | `"padrão"` | `"azul"` | `"padrão"` |
| `cor_fundo` | `"padrão"` | `"padrão"` | `"padrão"` | `"padrão"` | `"padrão"` | `"padrão"` | `"azul"` |
| `caixa_alta` | `true` | `true` | `true` | `true` | `true` | `true` | `true` |

`caixa_alta: true` é o default de todos os presets — regra geral, não
exceção por preset.

`caractere_esquerdo` e `caractere_direito` sempre ocupam posição (nunca
vazios): espaço representa "sem moldura visível", não ausência de campo —
invariante equivalente ao da borda (seção 3.1).

"Destaque Texto" e "Destaque Fundo" têm `caractere_esquerdo` e
`caractere_direito` iguais (`" "` / `" "`) entre si — a distinção visual
vem exclusivamente da cor aplicada (`cor_texto` vs `cor_fundo`), não da
moldura.

### 3.3 Indicadores

Três indicadores. Cada um tem natureza própria e defaults especificados.
Todos os valores de símbolo são defaults configuráveis — nunca fixos em código.

#### `concluido` — par on/off

| Estado | Símbolo default |
|---|---|
| `on` | `✓` |
| `off` | espaço (configurável) |

O schema deve expor os dois campos: `concluido_on` e `concluido_off`.
O default de `concluido_off` é um caractere de espaço (`" "`).
Ambos os campos são restritos a exatamente **1 caractere** — regra de
alinhamento colunar, aplicável a todos os símbolos do sistema (ver R-6).

#### `selecionado` — símbolo único, condicional

| Estado | Símbolo default |
|---|---|
| aparece (quando aplicável) | `→` |

`selecionado` só é renderizado quando o cursor está sobre o item.
O schema deve expor dois campos:

| Campo | Default |
|---|---|
| `selecionado_simbolo` | `→` |
| `selecionado_off` | `" "` (espaço) |

`selecionado_off` garante alinhamento colunar quando o indicador não está
ativo. Ambos os campos são restritos a exatamente **1 caractere** (ver R-6).

#### `incluido` — par on/off

| Estado | Símbolo default |
|---|---|
| `on` | `●` |
| `off` | `○` |

O schema deve expor os dois campos: `incluido_on` e `incluido_off`.

### 3.4 Tiling

Um campo obrigatório. Tipo: enumeração de string.

| Campo | Valores possíveis |
|---|---|
| `tiling` | `sobreposto` \| `lado_a_lado` |

Representa a preferência manual do usuário para a organização de múltiplos
objetos no corpo da tela. Não é calculado a partir da largura do terminal —
é lido do schema de estilo como qualquer outro campo.

Não existe valor de largura de terminal que force `sobreposto`: a preferência
do usuário é respeitada sempre, mesmo em terminal muito estreito.

---

## 4. Regras de uso

**R-1. Unicidade do schema em tempo de execução.**
Existe exatamente um objeto de estilo ativo por sessão. Todas as classes de
tela e todos os renderers leem desse objeto — nenhum mantém cópia local de
valores de estilo.

**R-2. Proibição de hardcoding.**
Decorre da seção 2 deste contrato. Aplica-se a qualquer símbolo, cor,
caractere ou valor de enumeração dos grupos borda, chip, indicadores e
tiling — sem exceção para "valores óbvios" ou "padrões universais".

**R-3. Completude do schema.**
Um schema de estilo que omita qualquer campo obrigatório listado nas seções
3.1, 3.2, 3.3 e 3.4 é inválido e não deve ser aceito pelo sistema.

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

- [ ] Todo acesso a símbolo, cor ou caractere de borda, chip ou indicador em
      qualquer classe ou renderer é feito exclusivamente via objeto de estilo —
      nenhuma string ou constante de estilo aparece hardcoded no código-fonte.
- [ ] O schema rejeita (ou registra erro) quando instanciado sem algum dos
      campos obrigatórios de borda (7), chip (5) ou indicadores (6 campos:
      `concluido_on`, `concluido_off`, `selecionado_simbolo`, `selecionado_off`,
      `incluido_on`, `incluido_off`).
- [ ] O schema rejeita (ou registra erro) qualquer campo de símbolo/caractere
      com comprimento diferente de 1 (R-6).
- [ ] Os defaults de indicadores (`✓`, `→`, `●`, `○`, `" "`) só existem na
      camada de construção do schema padrão — não no renderer nem nas classes.
- [ ] Dado um objeto de estilo com valores substituídos, o renderer produz
      saída com os valores fornecidos, não com os defaults.
- [ ] Nenhuma classe de tela altera o objeto de estilo recebido.
- [ ] O renderer traduz nomes semânticos de cor para valores de terminal — o
      schema não contém nenhuma lógica de tradução de cor (R-7).
- [ ] Os três presets de borda ("Borda Curva", "Borda Reta", "Linha" ) estão
      presentes e correspondem exatamente à tabela da seção 3.1.
- [ ] Os sete presets de chip ("Colchete", "Curva", "Ornamental", "Traço",
      "Ponto", "Destaque Texto", "Destaque Fundo") estão presentes e
      correspondem exatamente à tabela da seção 3.2.
- [ ] `tiling` aceita apenas `"sobreposto"` ou `"lado_a_lado"`; qualquer
      outro valor é inválido.
- [ ] O renderer não altera `tiling` com base em largura de terminal —
      o valor do schema é usado diretamente, sem fallback automático (R-8).

