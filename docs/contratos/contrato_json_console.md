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
