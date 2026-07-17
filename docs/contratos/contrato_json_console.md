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
      - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
      - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
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

---

## 11. Envelope declarativo do documento externo de conteúdo (ADR-0026)

A ADR-0026 (2026-07-17) formaliza a separação entre o envelope do console no
JSON estrutural da tela e o documento externo que transporta o conteúdo de
runtime.

### 11.1 JSON estrutural × documento externo

O envelope do console declarado em `corpo.elementos[]` pertence ao JSON
estrutural da tela e descreve configuração e composição da interface. O
conteúdo de runtime do console — dados, hierarquias, listas dinâmicas —
pertence a um documento externo separado.

### 11.2 Envelope declarativo mínimo do documento externo

O envelope conceitual mínimo do documento externo de conteúdo é:

```json
{
  "tipo": "multinivel",
  "formato": {},
  "dados": []
}
```

Cada bloco tem responsabilidade distinta:

| Bloco | Responsabilidade |
|---|---|
| `tipo` | Identifica o modo de apresentação do conteúdo (ex.: `"multinivel"`); autoridade da intenção de apresentação |
| `formato` | Descreve a intenção de apresentação — políticas declarativas, preferências de exibição; não contém resultados calculados |
| `dados` | Contém a estrutura semântica com os níveis hierárquicos declarados explicitamente |

O envelope mínimo acima é o ponto de partida. O schema semântico completo —
incluindo estrutura de `formato`, declaração de níveis, forma dos nós, tipos
de nível, designadores e validações obrigatórias — está formalizado pela
ADR-0027 (D11, D13) e propagado para a seção 12 deste contrato.

### 11.3 Foco inicial: `tipo: "multinivel"`

O formato inicial de interesse é `tipo: "multinivel"`. Os níveis são declarados
explicitamente no bloco `dados`. Os dados chegam previamente estruturados para
a apresentação multinível; o consumidor não reconstrói, descobre nem infere a
hierarquia a partir de dados de domínio não normalizados.

### 11.4 Restrição sobre o documento externo

O documento externo **não deve** conter resultados de cálculo físico de
runtime produzidos pelo renderizador:

- largura ou altura efetiva;
- linha ou coluna física calculada;
- posição ou coordenada física final;
- página calculada;
- quebra física pronta;
- truncamento já aplicado;
- geometria física final.

### 11.5 Princípio normativo

```text
O JSON externo declara a intenção de apresentação e o conteúdo semântico.
O renderizador calcula a representação física na área disponível.
```

### 11.6 Campo `origem_dados`

O campo `origem_dados` presente no envelope atual do console não é declarado
por esta ADR como mecanismo final de vínculo entre o `tela.json` e o documento
externo. A forma desse vínculo permanece para decisão futura.

### 11.7 Compatibilidade

A ausência do documento externo (console sem conteúdo de runtime) não invalida
o envelope do console no JSON estrutural da tela. JSONs existentes são
preservados.

### 11.8 Decisões deferidas

Permanecem para decisão futura, fora do escopo desta seção:

- vínculo entre `tela.json` e o documento externo;
- protocolo de invocação do script produtor;
- suporte ao `tipo: "matriz"` no mesmo mecanismo;
- comportamento diante de fonte ausente ou inválida;
- APIs, classes e módulos do consumidor/loader.

O schema semântico completo e as validações do documento externo foram decididos
pela ADR-0027 (D11, D13) e estão formalizados na seção 12 deste contrato. Não
são mais decisões deferidas.

### 11.9 Remissões

- `contrato_console.md` — seção 19 (ADR-0026): fronteira comportamental do console;
- `contrato_tela_json.md` — seção 31 (ADR-0026): fronteira do JSON estrutural;
- `docs/NOMENCLATURA.md` — seção 17: terminologia canônica da ADR-0026.

---

## 12. Schema semântico multinível do documento externo de conteúdo (ADR-0027)

A ADR-0027 (2026-07-17 D11, D13) decide e formaliza o schema semântico
multinível obrigatório para o documento externo de conteúdo. Esta seção propaga
esse schema para o contrato do console.

### 12.1 Envelope raiz obrigatório

A raiz do documento externo de conteúdo é um objeto com os campos:

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "hierarquia",
    "niveis": []
  },
  "dados": []
}
```

Regras:

- a raiz é um objeto;
- `tipo` é obrigatório e deve ser `"multinivel"`;
- `formato` é obrigatório e deve ser objeto;
- `dados` é obrigatório e deve ser array;
- `formato.apresentacao` é obrigatório;
- `formato.niveis` é obrigatório e deve ser array;
- os níveis são declarados explicitamente em `formato.niveis`;
- o consumidor não infere a hierarquia a partir de dados de domínio não
  normalizados.

O valor `"hierarquia"` no exemplo de envelope não torna essa apresentação
obrigatória para todos os documentos.

### 12.2 Apresentações previstas

```text
tabela
hierarquia
conjuntos_campos
```

Cada apresentação possui blocos próprios de `formato`:

**Tabela:**

```json
{
  "apresentacao": "tabela",
  "niveis": [],
  "tabela": {
    "cabecalho": [],
    "ancestrais": "repetir"
  },
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

**Hierarquia:**

```json
{
  "apresentacao": "hierarquia",
  "niveis": [],
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

**Conjuntos e campos:**

```json
{
  "apresentacao": "conjuntos_campos",
  "niveis": [],
  "campos": {},
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

Compatibilidade dos blocos:

- `tabela` somente em `apresentacao: "tabela"`;
- `campos` somente em `apresentacao: "conjuntos_campos"`;
- nenhum desses blocos específicos em `apresentacao: "hierarquia"`.

### 12.3 Forma dos níveis

Cada item de `formato.niveis` deve conter:

```json
{
  "id": "identificador_do_nivel",
  "tipo": "container",
  "conteudo": "titulo",
  "designador": {
    "tipo": "decimal"
  }
}
```

**Campo `id`:**

- identifica o nível;
- deve ser string não vazia;
- deve ser único dentro de `formato.niveis`;
- é referenciado pelo campo `nivel` dos nós.

**Campo `tipo`** — valores permitidos:

```text
container
conteudo
nome_valor
```

**Campo `conteudo`:**

Para `container` e `conteudo`, indica o nome do campo do nó que contém o
texto exibível:

```json
{ "conteudo": "titulo" }
```

Para `nome_valor`, declara os campos usados:

```json
{
  "conteudo": {
    "nome": "nome",
    "valor": "valor"
  }
}
```

**Campo `designador`:**

Declara a forma do marcador visual do nível. Tipos previstos:

```text
nenhum
simbolo
decimal
alfabetico_minusculo
alfabetico_maiusculo
romano_minusculo
romano_maiusculo
decimal_composto
personalizado
```

Campos condicionais conforme o tipo: `prefixo`, `sufixo`, `valor`, `separador`.
A sequência concreta do designador é calculada pelo renderizador. O documento
externo não deve armazenar a numeração concreta já calculada.

### 12.4 Forma comum dos nós

Cada nó em `dados` ou em `filhos` deve possuir:

```json
{
  "id": "identificador",
  "nivel": "id_de_nivel_declarado"
}
```

Regras comuns:

- `id` é obrigatório;
- `nivel` é obrigatório;
- `nivel` deve referenciar um item de `formato.niveis`;
- a ordem dos arrays é a ordem semântica original;
- o consumidor não reordena os nós;
- a hierarquia é expressa por `filhos`;
- o consumidor não reconstrói hierarquia a partir de nomes, IDs ou convenções
  externas.

**Nós de nível `container`:**

```json
{
  "id": "conjunto_1",
  "nivel": "conjunto",
  "titulo": "Conjunto 1",
  "filhos": []
}
```

- deve conter o campo indicado por `nivel.conteudo`;
- deve conter `filhos` como array;
- os filhos são validados recursivamente.

**Nós de nível `conteudo`:**

```json
{
  "id": "conteudo_1",
  "nivel": "item",
  "titulo": "Texto exibível"
}
```

- deve conter o campo indicado por `nivel.conteudo`;
- representa conteúdo diretamente exibível.

**Nós de nível `nome_valor`:**

```json
{
  "id": "elemento_1",
  "nivel": "elemento",
  "nome": "Elemento 1",
  "valor": "Valor do elemento 1."
}
```

- deve conter o campo indicado por `conteudo.nome`;
- deve conter o campo indicado por `conteudo.valor`;
- o separador visual pertence a `formato.campos`, quando aplicável;
- o documento externo não deve armazenar alinhamentos físicos já calculados.

### 12.5 Validações semânticas mínimas

As validações abaixo são obrigatórias e devem ser verificadas pelo loader ou
camada equivalente:

1. raiz é objeto;
2. presença e tipo correto de `tipo`;
3. valor de `tipo` igual a `"multinivel"`;
4. presença e tipo objeto de `formato`;
5. presença e tipo array de `dados`;
6. presença de `formato.apresentacao`;
7. `formato.apresentacao` pertence ao conjunto permitido (`tabela`, `hierarquia`,
   `conjuntos_campos`);
8. presença e tipo array de `formato.niveis`;
9. cada item de `formato.niveis` possui `id`, `tipo`, `conteudo` e `designador`;
10. IDs de nível não vazios e não duplicados em `formato.niveis`;
11. tipos de nível pertencem ao conjunto permitido (`container`, `conteudo`,
    `nome_valor`);
12. cada nó em `dados` possui `id` e `nivel`;
13. cada valor de `nivel` em nó existe na declaração de `formato.niveis`;
14. nós de tipo `container` possuem o campo declarado em `conteudo` e `filhos`
    como array;
15. nós de tipo `conteudo` possuem o campo declarado em `conteudo`;
16. nós de tipo `nome_valor` possuem os campos declarados em `conteudo.nome` e
    `conteudo.valor`;
17. filhos são validados recursivamente com as mesmas regras;
18. a ordem dos arrays é preservada pelo consumidor;
19. campos específicos da apresentação são compatíveis com `apresentacao`;
20. o documento não contém resultados físicos calculados.

### 12.6 Resultados físicos proibidos no documento externo

O documento externo não pode armazenar:

```text
largura efetiva
altura efetiva
quantidade física calculada de linhas ou colunas
posição final
coordenada física final
página calculada
quebra física pronta
truncamento já aplicado
distribuição concreta do espaço restante
células vazias calculadas
geometria final
numeração concreta de designadores
```

### 12.7 Exemplo normativo de três níveis

O exemplo abaixo é normativo: demonstra o schema semântico como autoridade
para o H-0036. Não é uma fixture definitiva do ciclo, não fixa caminho nem
nome de arquivo.

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "conjuntos_campos",
    "niveis": [
      {
        "id": "conjunto",
        "tipo": "container",
        "conteudo": "titulo",
        "designador": {
          "tipo": "decimal",
          "sufixo": "."
        }
      },
      {
        "id": "subconjunto",
        "tipo": "container",
        "conteudo": "titulo",
        "designador": {
          "tipo": "decimal_composto",
          "separador": ".",
          "sufixo": "."
        }
      },
      {
        "id": "elemento",
        "tipo": "nome_valor",
        "conteudo": {
          "nome": "nome",
          "valor": "valor"
        },
        "designador": {
          "tipo": "nenhum"
        }
      }
    ],
    "campos": {
      "separador": ":",
      "justificar_nomes": true,
      "escopo_justificacao": "por_conjunto"
    },
    "espacamento": {},
    "alinhamento": {},
    "excesso": {
      "modo": "verboso"
    },
    "paginacao": {}
  },
  "dados": [
    {
      "id": "conjunto_1",
      "nivel": "conjunto",
      "titulo": "Conjunto 1",
      "filhos": [
        {
          "id": "subconjunto_1_1",
          "nivel": "subconjunto",
          "titulo": "Subconjunto 1.1",
          "filhos": [
            {
              "id": "elemento_1",
              "nivel": "elemento",
              "nome": "Elemento 1",
              "valor": "Valor do elemento 1."
            }
          ]
        }
      ]
    }
  ]
}
```

### 12.8 Relação com as fixtures do H-0036

O H-0036 criará fixtures permanentes que seguem este contrato. Os JSONs
estruturais e de conteúdo permanecerão separados. Os caminhos concretos serão
definidos nominalmente no handoff corrigido. Este contrato não cria um
diretório global definitivo de runtime.

### 12.9 Relação com o Pipeline

O produtor futuro ligado ao Pipeline deverá produzir documento compatível com
este schema semântico. A mudança de fixture para produtor não altera a fronteira
semântica do console.

Permanecem deferidos: protocolo, transporte, argumentos, códigos de saída,
timeout, autenticação, atualização, cache, versionamento e persistência.

### 12.10 Remissões

- `contrato_console.md` — seção 20 (ADR-0027): fluxo de responsabilidade;
- `contrato_tela_json.md` — seção 32 (ADR-0027): fronteira do JSON estrutural;
- `docs/NOMENCLATURA.md` — seção 18: terminologia canônica da ADR-0027.
