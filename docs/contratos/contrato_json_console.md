---
name: contrato-json-console
description: Especifica o envelope mínimo de um elemento tipo console em corpo.elementos[] do JSON de tela — container genérico, políticas de composição, modelo para contratos futuros de conteúdo
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_console.md
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_composicao_corpo.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo de elemento `console` (`contrato_json_console.md`)

## 1. Objetivo

Especificar apenas o **envelope mínimo** de um elemento do tipo `console`
declarado em `corpo.elementos[]` no JSON de tela concreto: os campos mínimos
do envelope e suas políticas, a natureza de container genérico, a separação
entre envelope e tipos internos de item, e o modelo normativo que todo
contrato futuro de conteúdo interno de `console` deve seguir.

Este contrato fecha o envelope mínimo. Não fecha tipos internos de item nem
registry de ações. Cada tipo real de item/conteúdo de `console` terá contrato
próprio.

---

## 2. Natureza e escopo

`console` é um container interativo e navegável genérico. Uma ocorrência
concreta de `console` é uma instância declarada em `corpo.elementos[]` no
JSON de tela.

Propriedades fundamentais:

- `console` é **container genérico** — não mapeia para um único tipo de dado
  ou estrutura interna fixa;
- `console` pode conter **itens heterogêneos** — itens de tipos diferentes
  coexistem na mesma instância;
- `console` é navegável por `[✥]` (setas do teclado) quando a instância
  declara navegação habilitada e há ao menos um item com `navegavel: true`;
- `console` **não é `lancador`** — `lancador` aciona navegação para outras
  telas; `console` é container de dados ou saída;
- `console` **não é `dashboard`** — `dashboard` é passivo; `console` é
  interativo;
- **o envelope do `console` não fecha tipos internos de item** — campos de
  item como `tipo`, `binding`, `renderizador`, `navegavel`, `selecionavel`,
  `acao_enter`, `politica_quebra` e `politica_exibicao` existem como parte do
  item, não do envelope da instância.

Este contrato especifica o **envelope mínimo** da instância. As regras
semânticas completas (navegação por item, seleção por política, ação de Enter
por item, modo verboso, filtros, paginação, colunas) pertencem a
`contrato_console.md`, que continua sendo a autoridade sobre o comportamento
do tipo.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seções 12 e 13) estabelece que:

- `console` é container interativo e navegável genérico;
- pode conter itens heterogêneos;
- o cursor navega por itens, não por linhas físicas;
- cada item declara se é navegável, selecionável e qual ação tem;
- filtros atuam antes da paginação;
- modo verboso é estado de exibição reutilizável.

Este contrato operacionaliza esses princípios para o formato JSON concreto e
estabelece o modelo para contratos futuros de tipos internos de item.

---

## 4. JSON mínimo

O envelope mínimo de um elemento `console` em `corpo.elementos[]` é:

```json
{
  "id": "console_principal",
  "tipo": "console",
  "titulo": "Console",
  "origem_dados": null,
  "itens": [],
  "politica_composicao": {
    "alinhamento": "esquerda",
    "overflow_normal": "truncar_com_reticencias"
  },
  "politica_navegacao": {
    "navegavel": false
  },
  "politica_selecao": "nenhuma",
  "politica_paginacao": "sem",
  "politica_exibicao": {
    "modo_inicial": "normal",
    "verboso": false
  }
}
```

Observações sobre o envelope mínimo:

- `origem_dados: null` indica ausência de vínculo de dados — valor de
  reserva antes de contrato de conteúdo ser aplicado;
- `itens: []` é a lista de itens; itens concretos pertencem ao JSON da tela;
- `politica_navegacao.navegavel: false` indica `console` não navegável no
  estado mínimo — deve ser declarado `true` e incluir itens navegáveis para
  habilitar `[✥]`;
- `politica_selecao: "nenhuma"` indica ausência de seleção — valores
  alternativos: `"unica"` ou `"multipla"`;
- `politica_paginacao: "sem"` indica sem paginação — valor alternativo:
  `"com"`;
- `politica_exibicao.verboso: false` indica modo verboso desabilitado.
- Pela ADR-0022, a futura tela inicial real `orquestrador` deverá ter um
  `console` estruturalmente presente e sem entradas iniciais; `origem_dados:
  null` com `itens: []` é a forma mínima compatível com essa semântica, desde
  que preservadas as demais políticas obrigatórias deste envelope.

---

## 5. Campos obrigatórios

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador estável e único do elemento no escopo de `corpo.elementos[]`. Elemento sem `id` é inválido. |
| `tipo` | string | Deve ser o valor literal `"console"`. |
| `titulo` | string | Identificador visual da instância. Pode ser omitido se a instância não exibir título, desde que haja outra forma de identificação. |
| `origem_dados` | objeto ou null | Fonte dos dados dos itens. `null` quando não há dados vinculados. Instância sem `origem_dados`, `binding` ou regra de geração de itens é inválida semanticamente. |
| `itens` | array | Lista de itens declarados ou vazia. Itens concretos pertencem ao JSON da tela. |
| `politica_composicao` | objeto | Define organização visual dos itens. Campos mínimos: `alinhamento` e `overflow_normal`. |
| `politica_navegacao` | objeto | Define se o `console` é navegável e como o cursor se move. Campo mínimo: `navegavel` (booleano). |
| `politica_selecao` | string | `"nenhuma"`, `"unica"` ou `"multipla"`. Valor desconhecido é erro de validação. |
| `politica_paginacao` | string | `"sem"` ou `"com"`. Quando `"com"`, a instância deve declarar política de paginação adicional. |
| `politica_exibicao` | objeto | Define modo inicial e se verboso é permitido. Campos mínimos: `modo_inicial` e `verboso`. |

---

## 6. Campos de item — envelope aberto

O envelope do `console` não fecha os tipos internos de item. Cada item em
`itens[]` pode declarar os campos abaixo, conforme o contrato do tipo de
item correspondente:

| Campo do item | Descrição |
|---|---|
| `id` | Identificador estável do item no escopo da instância. Obrigatório. |
| `tipo` | Tipo do item — determina contrato de renderização. Tipo desconhecido é erro. |
| `binding` | Vínculo entre dados e campos exibidos pelo item. |
| `renderizador` | Identificador do renderizador responsável por este tipo de item. |
| `navegavel` | `true` \| `false`. Se o cursor pode entrar neste item. |
| `selecionavel` | `true` \| `false`. Se participa do toggle de seleção `[␣]`. |
| `acao_enter` | Ação declarativa registrada executada quando `[⏎]` é acionado com este item em foco. |
| `politica_quebra` | `"evitar_quebra"`, `"permitir_quebra"` ou `"permitir_quebra_somente_se_maior_que_pagina"`. |
| `politica_exibicao` | Regras internas de renderização em modo normal e verboso. |

Esses campos pertencem ao contrato do tipo de item específico, não a este
envelope. O renderer não hardcoda estrutura de item.

---

## 7. Regras de validação

**V-1. `console` é elemento do corpo.**
`console` só aparece como elemento de `corpo.elementos[]`. Nunca como seção
raiz da tela.

**V-2. `id` presente e único.**
Elemento `console` sem `id` é inválido. `id` duplicado no escopo de
`corpo.elementos[]` é erro de validação.

**V-3. `politica_selecao` com valor conhecido.**
Valores permitidos: `"nenhuma"`, `"unica"`, `"multipla"`. Valor desconhecido
é erro de validação.

**V-4. Seleção é estado de runtime — não pertence ao JSON.**
Estado de seleção atual, item selecionado e cursor não devem ser persistidos
no JSON de tela. O JSON declara a política; a execução gerencia o estado.

**V-5. Filtros atuam antes da paginação.**
O conjunto paginado é sempre o resultado filtrado. Filtros são declarados no
JSON da tela — não hardcoded no renderer.

**V-6. Ação de Enter pertence ao item ou binding do item.**
`acao_enter` é campo do item, não da tela inteira de forma monolítica. Itens
diferentes podem ter ações diferentes. Ação não registrada é erro de
validação.

**V-7. Seleção por toggle não é estado persistido.**
Seleção é estado de runtime — não consta no JSON como campo vivo.

**V-8. Renderer não hardcoda item, filtro, ação, política.**
O renderer percorre as listas e objetos declarados. Nenhum item, filtro,
ação, política de paginação, regra de coluna, composição ou navegação pode
estar hardcoded no código.

---

## 8. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- contratos de tipos internos de item de `console` — pendência DOC-B008;
  cada tipo real terá `contrato_conteudo_console_<tipo>.md`;
- registry completo de ações — pendência DOC-B009;
- implementação de cursor, paginação, filtros, colunas — pertencem à
  implementação futura;
- chips de `barra_de_menus` que refletem capacidades de `console` (`[✥]`,
  `[␣]`, `[V]`, `[<][>]`, `[-][+]`) — regidos por `contrato_barra_de_menus.md`;
- modo verboso: lógica interna de cada tipo de item em modo verboso pertence
  ao contrato do tipo de item.

---

## Contratos futuros de conteúdo de `console`

Todo contrato `contrato_conteudo_console_<tipo>.md` deve conter:

1. Objetivo do tipo de conteúdo/item
2. Elemento hospedeiro permitido: `console`
3. Campos próprios do item/conteúdo
4. Binding no `tela.json`
5. JSON mínimo associado
6. Regras de navegação, seleção e ação
7. Política de quebra/paginação, quando aplicável
8. Fora de escopo

Esses contratos são os responsáveis por fechar o que este envelope não fecha.
Nenhum tipo real de item de `console` pode ser declarado no JSON de tela sem
que exista contrato próprio do tipo correspondente.

---

## 9. Critérios de aceite documental

- [ ] O JSON mínimo contém `id`, `tipo`, `titulo`, `origem_dados`, `itens[]`,
      `politica_composicao`, `politica_navegacao`, `politica_selecao`,
      `politica_paginacao` e `politica_exibicao`.
- [ ] O envelope não fecha tipos internos de item.
- [ ] Os campos de item são listados como envelope aberto, com remissão a
      contratos futuros.
- [ ] Seleção como estado de runtime está declarada.
- [ ] Filtros antes da paginação estão declarados.
- [ ] Ação de Enter como propriedade do item está declarada.
- [ ] A seção "Contratos futuros de conteúdo de `console`" contém o modelo
      com as 8 seções obrigatórias.
- [ ] O JSON mínimo não contradiz `contrato_console.md` nem
      `contrato_tela_json.md`.

---

## 10. Distribuição matricial de nível único (ADR-0025)

A ADR-0025 (2026-07-16) permite que o `console` adote a capacidade de
distribuição matricial configurável de nível único mediante declaração explícita
no seu JSON em `corpo.elementos[]`.

### 10.1 Localização do campo

O campo `distribuicao_matricial` é declarado no nível do elemento `console`,
ao lado dos demais campos do envelope:

```json
{
  "id": "console_principal",
  "tipo": "console",
  "titulo": "Console",
  "origem_dados": null,
  "itens": [],
  "politica_composicao": { "alinhamento": "esquerda", "overflow_normal": "cortar_direita" },
  "politica_navegacao":  { "navegavel": false },
  "politica_selecao":    "nenhuma",
  "politica_paginacao":  "sem",
  "politica_exibicao":   { "modo_verboso": false },
  "distribuicao_matricial": {
    "formacao": {
      "politica": "preferencia_linhas",
      "colunas": { "minimo": 1 },
      "linhas":  { "minimo": 1 }
    },
    "ordem": "por_linha",
    "dimensionamento": {
      "colunas": { "politica": "maior_da_coluna" },
      "linhas":  { "politica": "maior_da_linha" }
    },
    "espacamento": {
      "margem_superior":  { "minimo": 1 },
      "margem_inferior":  { "minimo": 1 },
      "margem_esquerda":  { "minimo": 1 },
      "margem_direita":   { "minimo": 1 },
      "vao_horizontal":   { "minimo": 2 },
      "vao_vertical":     { "minimo": 0 }
    },
    "distribuicao_horizontal": { "politica": "inicio" },
    "distribuicao_vertical":   { "politica": "inicio" },
    "ordem_expansao": {
      "horizontal": "margens_primeiro_depois_vaos",
      "vertical":   "uniforme_margens_e_vaos"
    },
    "politica_resto": {
      "horizontal": "ao_ultimo",
      "vertical":   "ao_ultimo"
    },
    "alinhamento_interno": {
      "horizontal": "inicio",
      "vertical":   "topo"
    }
  }
}
```

O exemplo acima é ilustrativo. Valores concretos pertencem ao JSON da tela.

### 10.2 Vocabulário de campos

O vocabulário de campos de `distribuicao_matricial` para o `console` é idêntico
ao definido em `contrato_json_dashboard.md` seções 9.2 e 9.2.1. Todos os
campos, valores permitidos, obrigatoriedades, rejeições e regras de tratamento
se aplicam sem exceção, incluindo o tratamento normativo de `"minimo_fixo"`
definido na seção 9.2.1 daquele contrato.

### 10.3 Substituição de políticas geométricas quando `distribuicao_matricial` está presente (DEC-APP-0025-03)

Quando `distribuicao_matricial` for declarado em um `console`, as políticas
existentes relacionadas à organização geométrica do conteúdo são
**integralmente substituídas** pela nova configuração.

**Políticas substituídas** quando `distribuicao_matricial` está presente:

| Política substituída | Fonte da política antiga | Substituída por |
|---|---|---|
| Alinhamento horizontal do bloco (`politica_composicao.alinhamento`) | `contrato_json_console.md` seção 5 | `distribuicao_horizontal.politica` + `espacamento.margem_*` |
| Espaçamento universal entre borda e conteúdo | `contrato_composicao_corpo.md` seção 4.6 | `espacamento.margem_*` declarado em `distribuicao_matricial` |
| Quantidade ou ajuste de colunas (`colunas_ajustavel`) | `contrato_composicao_corpo.md` seção 4.4 | `formacao.colunas.*` declarado em `distribuicao_matricial` |
| Alinhamento de colunas interno | Regras internas do `console` | `alinhamento_interno.*` declarado em `distribuicao_matricial` |
| Vãos entre participantes e colunas | Políticas internas do `console` | `espacamento.vao_*` declarado em `distribuicao_matricial` |
| Formação e distribuição geométrica do conjunto de participantes | Políticas herdadas de layout | Todas as sub-configurações de `distribuicao_matricial` |

As políticas substituídas **não coexistem, não complementam, não concorrem
e não são herdadas parcialmente** pela nova configuração. Quando
`distribuicao_matricial` está presente, ela é a única autoridade geométrica
para o conjunto organizado.

**Políticas preservadas** mesmo quando `distribuicao_matricial` está presente
(não são políticas de layout ou distribuição geométrica):

- `politica_composicao.overflow_normal` — tratamento de overflow de conteúdo;
- `politica_navegacao` — navegabilidade por `[✥]` e comportamento do cursor;
- `politica_selecao` — política de seleção de itens;
- `politica_paginacao` — paginação do conteúdo (explicitamente fora do escopo
  da ADR-0025);
- `politica_exibicao` — modo inicial e modo verboso;
- `acao_enter` por item — ações funcionais declarativas;
- `filtro_de_grupo`, `formacao_de_selecao` — capacidades funcionais;
- `origem_dados` — vínculo de dados;
- `itens[]` — conteúdo declarado dos itens.

**Quando `distribuicao_matricial` está ausente**: todas as políticas anteriores
do `console` continuam vigentes integralmente. JSONs existentes preservam o
comportamento. Nenhuma migração automática ocorre. Nenhum default novo é
aplicado.

### 10.4 Compatibilidade com JSONs existentes

A ausência do campo `distribuicao_matricial` em um JSON de `console` existente
preserva integralmente o comportamento anterior. Não há migração automática, não
há reescrita do JSON e não há default estrutural que reorganize instâncias
existentes.

### 10.5 Fallback

Quando nenhuma formação válida conseguir acomodar todos os participantes e todos
os mínimos, o estado exibido é o `quadro mínimo de terminal pequeno` (ADR-0017,
ADR-0023). Não é criada variante concorrente de estado de fallback.
