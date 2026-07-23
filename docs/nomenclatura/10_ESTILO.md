---
name: nomenclatura-estilo
description: Terminologia do estilo universal — borda, chip visual, indicadores, estados dinâmicos de cor, tiling como preferência global de arranjo
metadata:
  type: nomenclatura
  scope: estilo
  fase_de_aplicacao: VIGENTE
---

# Estilo universal

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário da terminologia de:
- estilo universal e aparência;
- bordas;
- chips como forma visual (campos de estilo);
- indicadores visuais;
- cores e estados dinâmicos de cor (`cor_inativo`, `cor_alerta`);
- `tiling` como preferência global de arranjo;
- aliases de arranjo transitórios referenciados no contexto de estilo.

**Fronteira com o módulo `02`**: o vocabulário de estilo (campos, presets,
indicadores e distinções semânticas) é proprietário deste módulo. Os valores
de estilo são materializados em `config/estilo.json`, cujo artefato e caminho
são propriedade terminológica do módulo `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`.
Este módulo não lista `config/estilo.json` como termo proprietário — apenas
documenta que os valores vivem nesse artefato.

Regra fundamental: nenhuma classe de tela ou renderer pode hardcodar símbolo,
cor ou caractere pertencente ao estilo. Todo valor de estilo vem do schema
em tempo de execução.

## 3. Termos proprietários

- campos de borda: `traco_superior`, `traco_inferior`, `canto_superior_esquerdo`,
  `canto_superior_direito`, `canto_inferior_esquerdo`, `canto_inferior_direito`, `lateral`
- campos de chip visual: `caractere_esquerdo`, `caractere_direito`, `cor_texto`,
  `caixa_alta`, `cor_fundo`
- indicadores: `concluido`, `selecionado`, `incluido` (como campos de estilo)
- presets de borda: "Borda Curva", "Borda Reta", "Linha"
- presets de chip: "Colchete", "Curva", "Ornamental", "Traço", "Ponto", "Destaque Texto", "Destaque Fundo"
- presets de `selecionado` e `incluido`
- catálogo de presets (`presets`)
- preset ativo / `preset_default`
- preset resolvido
- materialização
- `cor_inativo`
- `cor_alerta`
- `tiling` (como campo de preferência global)
- existência vs ativo/inativo (distinção do §4.7)
- configuração de aparência vs estado vivo de execução

## 4. Definições

### 4.1 Estilo universal

Aparência do sistema. Nunca varia por tela ou classe. Definido em
`config/estilo.json`. Nenhuma classe ou renderer pode hardcodar símbolo, cor
ou caractere desta seção — tudo vem do schema de estilo.

### 4.2 Borda

Campos do schema de borda:

| Campo | Função |
|---|---|
| `traco_superior` | caractere da linha superior |
| `traco_inferior` | caractere da linha inferior |
| `canto_superior_esquerdo` | canto superior esquerdo |
| `canto_superior_direito` | canto superior direito |
| `canto_inferior_esquerdo` | canto inferior esquerdo |
| `canto_inferior_direito` | canto inferior direito |
| `lateral` | caractere da coluna esquerda/direita |

O espaço da moldura sempre existe estruturalmente; o que muda entre estilos
de borda é só o caractere de preenchimento.

**Catálogo e preset ativo (ADR-0030 D2)**: três presets nomeados — "Borda
Curva", "Borda Reta", "Linha". O preset ativo é indicado por
`borda.preset_default` em `config/estilo.json`. O preset ativo inicial é
`"Borda Curva"`. **Materialização**: o loader resolve o preset ativo e
produz os sete campos de runtime acima.

### 4.3 Chip (forma visual)

Campos do schema de aparência do chip:

| Campo | Função |
|---|---|
| `caractere_esquerdo` | caractere de abertura do chip |
| `caractere_direito` | caractere de fechamento do chip |
| `cor_texto` | cor do texto/tecla do chip |
| `caixa_alta` | booleano — texto em maiúscula (`true`) ou não (`false`) |
| `cor_fundo` | cor de fundo do chip |

Estes são os campos de estilo visual do chip. O comportamento e semântica
de cada chip canônico pertencem ao contrato `contrato_barra_de_menus.md` e ao
módulo `31_BARRA_DE_MENUS_E_CHIPS.md`.

**Catálogo e preset ativo (ADR-0030 D2)**: sete presets nomeados — "Colchete",
"Curva", "Ornamental", "Traço", "Ponto", "Destaque Texto", "Destaque Fundo".
O preset ativo é indicado por `chip.preset_default` em `config/estilo.json`.
O preset ativo inicial é `"Colchete"`. **Materialização**: o loader resolve o
preset ativo e produz os cinco campos de runtime acima.

**`caixa_alta` é valor per-preset** — não existe default global de `caixa_alta`
independente do preset. O preset "Colchete" usa `caixa_alta: false` para
preservar a capitalização atual dos rótulos (ADR-0030 D5).

**Capitalização como propriedade do estilo**: o campo `caixa_alta` do preset
resolvido controla se o renderer aplica transformação para maiúsculas no texto
do chip. A capitalização NÃO é definida pela declaração do chip no `tela.json`
— vem exclusivamente do preset de estilo resolvido.

### 4.4 Indicadores

| Indicador | Natureza | Símbolos (default) |
|---|---|---|
| `concluido` | par on/off | on: `✓`, off: configurável (default espaço) |
| `selecionado` | símbolo único, só aparece quando aplicável | `→` |
| `incluido` | par on/off | on: `●`, off: `○` |

Todos os símbolos são default configurável via schema, nunca fixos em código.

**Presets nomeados**: não existe um único símbolo fixo — existem conjuntos
nomeados. `selecionado` tem 4 presets ("Seta" é o default); `incluido` tem 4
presets ("Círculo" é o default). Valores concretos em `config/estilo.json`,
seção `indicadores`.

**Símbolo estático de `incluido` sem seleção real**: quando o item não tem
seleção formável, `tg` mostra um símbolo fixo (não alternante) em vez do par
on/off — esse símbolo também é configurável via schema; nenhum valor concreto
foi decidido até o momento.

### 4.5 Estados dinâmicos de cor (ADR-0004)

Dois campos genéricos aplicáveis a qualquer chip ou indicador do sistema:

| Campo | Função |
|---|---|
| `cor_inativo` | cor aplicada quando um elemento existe mas está temporariamente inativo (apagada/dessaturada) |
| `cor_alerta` | cor aplicada quando um valor atinge um limite (ex.: mínimo/máximo) |

Nenhum valor concreto de cor foi decidido — vivem apenas como nomes semânticos
no schema; quando decididos, entrarão em `config/estilo.json`.

### 4.6 `tiling` — preferência global de arranjo

Campo `tiling`. Terminologia final de arranjo (ADR-0011): valores finais são
`vertical` | `horizontal`.

`tiling` é a **preferência global do usuário** para arranjo de elementos
funcionais do corpo. É default, não obrigatório: a classe de tela pode fixar
seu próprio arranjo e ignorar a preferência global para aquela tela.
`tiling` só é consultado quando a classe não especifica arranjo fixo.

Escolha manual do usuário, não decisão automática por largura de terminal.
Não existe largura mínima de segurança que force arranjo `vertical` — a
preferência do usuário sempre vale quando aplicada.

### 4.7 Distinção existência vs ativo/inativo

- **Existência** de um chip = propriedade estática, declarada pela classe de
  tela. Ex.: a classe declara `paginacao: com` → o chip `[<][>]` existe nessa tela.
- **Ativo/inativo** = estado dinâmico, recalculado a cada render, a partir
  do conteúdo atual. Ex.: `[<][>]` existe, mas fica **inativo** (usa
  `cor_inativo`) quando há só 1 página no momento.

### 4.8 Materialização e carregamento global (ADR-0030)

**Materialização** é o processo pelo qual o loader converte a estrutura de
`config/estilo.json` — catálogos, `preset_default`, campos diretos — em uma
representação de runtime com campos planos que os consumidores usam.

O loader carrega `config/estilo.json` **uma única vez por sessão**. O resultado
(objeto de estilo resolvido) é imutável durante a sessão:

| Seção em `config/estilo.json` | Resultado da materialização |
|---|---|
| `borda` (catálogo + `preset_default`) | 7 campos de runtime de borda |
| `chip` (catálogo + `preset_default`) | 5 campos de runtime de chip |
| `indicadores.concluido` (par direto) | `concluido_on`, `concluido_off` |
| `indicadores.selecionado` (catálogo + `preset_default` + campo `off`) | `selecionado_simbolo`, `selecionado_off` |
| `indicadores.incluido` (catálogo + `preset_default`) | `incluido_on`, `incluido_off` |

O renderer e demais consumidores recebem o objeto já resolvido. Não releem
`config/estilo.json` em cada render. Configuração parcialmente resolvida não
pode ser usada.

**Preset resolvido**: o preset cujos campos foram extraídos e estão disponíveis
no objeto de runtime como campos planos. "Resolver um preset" = identificar o
preset indicado por `preset_default`, validar e extrair seus campos.

### 4.9 Configuração de aparência vs estado vivo de execução (ADR-0030 D10)

| Tipo | Origem | Exemplos |
|---|---|---|
| Configuração de aparência | `config/estilo.json` via loader | caracteres de borda, preset de chip, símbolos de indicadores |
| Estado vivo de execução | produzido e mantido pela execução corrente | cursor corrente, itens incluídos, foco de corpo, página atual, modo verboso ativo |

Estado vivo **não pertence** a `config/estilo.json` e não é armazenado nele.
Os símbolos de cursor (`selecionado_simbolo`) e de inclusão (`incluido_on`,
`incluido_off`) vêm da configuração global materializada; **onde** o cursor está
e **quais** itens estão incluídos são estado vivo.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `tiling` × `corpo.arranjo` | `tiling` é preferência global de estilo consultada quando a classe não fixa arranjo; `corpo.arranjo` é arranjo fixado pela própria classe de tela — são conceitos diferentes em camadas diferentes |
| `tiling` × redimensionamento | Redimensionamento não altera `tiling`; `tiling` é configuração declarativa |
| `cor_inativo` × existência de chip | `cor_inativo` indica estado inativo de chip que existe; um chip pode existir e estar inativo — são propriedades independentes |
| chip como forma visual × chip como entidade de interface | A forma visual (campos de estilo) pertence a este módulo; a entidade declarativa de interface pertence ao módulo `31` e ao `contrato_chip.md` |
| configuração de aparência × estado vivo | Configuração: carregada uma vez de `config/estilo.json`, imutável na sessão; estado vivo: produzido e mantido pela execução (cursor, inclusão, foco, página) |
| preset resolvido × valor hardcoded | Preset resolvido: extraído do catálogo pelo loader a partir de `preset_default`; hardcoded: violação contratual (ADR-0030 D1) |
| símbolo materializado × estado de inclusão | O símbolo `●`/`○` vem do preset de `incluido` (configuração); quais itens estão incluídos é estado vivo de execução |

## 6. Relação com contratos

- `contrato_estilo.md`: autoridade do comportamento normativo completo do módulo de estilo.
- `contrato_barra_de_menus.md`: usa os estados `cor_inativo` e os campos de chip visual.
- `contrato_chip.md`: aparência visual dos chips vem do `config/estilo.json`.
- `contrato_composicao_corpo.md`: usa `tiling` como preferência global.

## 7. Relação com ADRs

- ADR-0004: introduz `cor_inativo` e `cor_alerta` no schema de estilo.
- ADR-0011: terminologia de arranjo `vertical`/`horizontal`; aliases transitórios
  `sobreposto`/`lado_a_lado`.
- ADR-0013: distinção entre `corpo.arranjo = "vertical"` e `ocupacao_vertical_terminal`.
- ADR-0014: regra de alteração por termo específico completo.
- ADR-0030: formaliza catálogo + `preset_default` como padrão canônico; materialização
  integral de todas as seções de `config/estilo.json`; `caixa_alta` per-preset;
  distinção configuração de aparência vs estado vivo; carregamento único por sessão.

## 8. Aliases ou termos descontinuados relacionados

- `sobreposto` → alias transitório de `vertical` (ADR-0011). Ver `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.
- `lado_a_lado` → alias transitório de `horizontal` (ADR-0011). Ver `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.

Esses aliases pertencem ao módulo `90` como entradas completas. Este módulo
apenas os referencia para indicar o contexto de estilo/arranjo.

## 9. Conteúdo que não pertence a este módulo

- Comportamento completo dos chips → `contrato_barra_de_menus.md` e `contrato_chip.md`.
- Semântica de `corpo.arranjo` → módulo `20_TELA_CORPO_E_COMPOSICAO.md`.
- `ocupacao_vertical_terminal` → módulo `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`.
- Distribuição da barra de menus → módulo `31_BARRA_DE_MENUS_E_CHIPS.md`.
- Valores concretos de estilo → `config/estilo.json`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§1 (linhas 109-233)"
  intervalo_ou_bloco: "NOM-LEV-006"
origem_normativa: ADR-0004, ADR-0011, ADR-0013, ADR-0014
contratos_relacionados:
  - contrato_estilo.md
  - contrato_barra_de_menus.md
  - contrato_chip.md
  - contrato_composicao_corpo.md
adrs_relacionadas:
  - ADR-0004
  - ADR-0011
  - ADR-0013
  - ADR-0014
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
  - REFERENCIADO
partes_NAO_CONFIRMADAS: []
```
