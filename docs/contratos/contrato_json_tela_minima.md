---
name: contrato-json-tela-minima
description: Especifica o envelope JSON mínimo de uma tela concreta — campos obrigatórios, caminho canônico e restrições declarativas do arquivo tela.json
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_tela_json.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
      - docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
      - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
      - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
      - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
      - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
      - docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo de tela (`contrato_json_tela_minima.md`)

## 1. Objetivo

Especificar o envelope JSON mínimo de uma tela concreta: os campos
obrigatórios, a estrutura hierárquica mínima de `corpo`, o caminho canônico
do arquivo em disco, a regra de coincidência entre `id` interno e nome base
do arquivo, e as restrições fundamentais da natureza declarativa do JSON de
tela.

Este contrato é operacional e incremental: parte de `contrato_tela_json.md`
(macrocontrato do schema completo) e especifica apenas o envelope mínimo que
torna um JSON de tela válido e carregável pelo renderer. Não redefine nem
duplica o macrocontrato.

---

## 2. Natureza e escopo

O JSON de tela é a declaração configurável de uma tela concreta. Ele é
declarativo — descreve a configuração que o renderer deve validar, resolver e
renderizar.

Propriedades fundamentais:

- o JSON de tela **não é código executável**;
- o JSON de tela **não contém estado de runtime** — cursor, página atual,
  filtro ativo, seleção atual, item focado;
- o JSON de tela **não pode carregar lógica procedural arbitrária**;
- composição, itens, chips, destinos, bindings e ações são declarativos,
  nunca hardcoded pelo renderer.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` é o macrocontrato do envelope completo da tela — define
o schema conceitual, campos opcionais, bindings, ações, filtros, validação e
pipeline de renderização.

Este contrato (`contrato_json_tela_minima.md`) especifica **somente o envelope
mínimo obrigatório** de um arquivo JSON de tela concreto. Contratos
incrementais específicos de cada região (`contrato_json_cabecalho.md`,
`contrato_json_barra_de_menus.md`, etc.) detalham os campos de cada seção.

---

## 4. JSON mínimo

O envelope mínimo de um JSON de tela válido é:

```json
{
  "schema": "tela.v1",
  "id": "exemplo",
  "cabecalho": {},
  "corpo": {
    "elementos": []
  },
  "barra_de_menus": {
    "chips": []
  }
}
```

Observações sobre o envelope acima:

- `cabecalho: {}` indica presença obrigatória; campos mínimos são definidos
  em `contrato_json_cabecalho.md`.
- `corpo.elementos: []` é lista; tela sem elementos de corpo é válida
  estruturalmente, mas pode ser inválida semanticamente se vazia.
- `corpo.arranjo` não aparece no envelope mínimo — é campo permitido mas
  opcional. Quando não declarado, o renderer usa o campo `tiling` do estilo
  ativo como default, conforme `contrato_composicao_corpo.md` seção 5.6. O
  renderer não inventa arranjo, não cria fallback próprio e não decide
  composição por largura de terminal.
- `barra_de_menus.chips: []` é lista; a lista concreta de chips pertence à
  declaração da tela, não ao renderer.

### 4.1 Exemplo com arranjo explícito (opcional)

Quando a tela fixa explicitamente o arranjo do corpo:

```json
{
  "schema": "tela.v1",
  "id": "exemplo",
  "cabecalho": {},
  "corpo": {
    "arranjo": "vertical",
    "elementos": []
  },
  "barra_de_menus": {
    "chips": []
  }
}
```

`arranjo` declarado fixa o layout para aquela tela; o renderer usa esse valor
e ignora o campo `tiling` do estilo ativo. `arranjo` é relevante para 2+
elementos funcionais do corpo (`console`, `lancador`, `dashboard`) — todos os
elementos do corpo seguem o mecanismo geral de composição declarativa
(ADR-0010). O campo `posicao_dashboard` está descontinuado como eixo de
posicionamento independente; JSONs existentes com esse campo podem ser
  honrados por compatibilidade em handoff futuro de migração. Ver `contrato_composicao_corpo.md`
e `contrato_json_dashboard.md`.

> **Terminologia final (ADR-0011)**: `vertical`/`horizontal` são os valores
> finais de `corpo.arranjo`. `sobreposto`/`lado_a_lado` são aliases
> transicionais aceitos para compatibilidade de JSONs legados até migração
> específica.

### 4.2 Tela inicial real `orquestrador` (ADR-0022)

A tela inicial real do produto fica reservada para:

```text
config/telas/orquestrador.json
```

com:

```json
"id": "orquestrador"
```

Essa reserva não declara que o arquivo já existe fisicamente. O ponto de
entrada real futuro `orquestrador.py` deverá carregar explicitamente a raiz
`config/telas/` e iniciar pela identidade `orquestrador`, sem alias, fallback
ou busca ambígua com `demo`.

O envelope macro dessa tela deve manter exatamente:

```text
cabecalho
corpo
barra_de_menus
```

O corpo inicial deverá conter `console` e `dashboard` estruturalmente
presentes, ambos sem entradas iniciais de dados reais ou demonstrativos.
Os valores concretos obrigatórios de `cabecalho.titulo` e
`cabecalho.descricao` permanecem pendentes de decisão documental suficiente
antes da criação física do JSON.

---

## 5. Campos obrigatórios

| Campo | Tipo | Regra |
|---|---|---|
| `schema` | string | Deve ser `"tela.v1"` nesta versão. Um renderer só aceita versão conhecida e suportada. |
| `id` | string | Identificador estável da tela — minúsculo, sem acentos, sem espaços, preferencialmente `snake_case`. Deve coincidir com o nome base do arquivo em disco. |
| `cabecalho` | objeto | Obrigatório e presente. Campos mínimos definidos em `contrato_json_cabecalho.md`. |
| `corpo` | objeto | Obrigatório e presente. Deve conter ao menos `elementos[]`. |
| `corpo.elementos` | array | Lista de elementos do corpo. Cada elemento deve declarar ao menos `id` e `tipo`. |
| `barra_de_menus` | objeto | Obrigatório e presente. Deve conter ao menos `chips[]`. |
| `barra_de_menus.chips` | array | Lista de chips da barra. Chips concretos pertencem à declaração da tela. |

### 5.1 Campo opcional `corpo.arranjo`

`corpo.arranjo` é campo **permitido** no JSON de tela, mas **não obrigatório**
no envelope mínimo.

| Campo | Valores | Regra |
|---|---|---|
| `corpo.arranjo` | `"vertical"` \| `"horizontal"` | Valores finais (ADR-0011). Quando declarado, fixa o arranjo para a tela e o renderer ignora `tiling` do estilo ativo. Quando não declarado, o renderer consulta o campo `tiling` do estilo ativo como default — ver `contrato_composicao_corpo.md` seção 5.6. Os aliases transicionais `sobreposto` (→ `vertical`) e `lado_a_lado` (→ `horizontal`) são aceitos para compatibilidade de JSONs legados até migração específica. |

Regras complementares:

- `corpo.arranjo` é relevante para 2+ elementos funcionais do corpo
  (`console`, `lancador`, `dashboard`).
- A composição visual do `dashboard` segue o mecanismo geral de composição do
  `corpo`, não um eixo independente (ADR-0010, 2026-07-08). O campo
  `posicao_dashboard` está descontinuado como eixo independente; JSONs
  existentes com esse campo podem ser honrados por compatibilidade transicional
  em handoff futuro de migração. Ver `contrato_json_dashboard.md`.
- O renderer não inventa arranjo, não cria fallback próprio baseado em largura
  de terminal e não decide composição por condição de ambiente.

---

## 6. Tipos válidos em `corpo.elementos[]`

`corpo.elementos[]` pode conter elementos funcionais e o nó estrutural `grupo`
(ADR-0015, 2026-07-10).

### 6.1 Tipos funcionais (taxonomia fechada)

| Tipo | Contrato de referência |
|---|---|
| `console` | `contrato_json_console.md`, `contrato_console.md` |
| `dashboard` | `contrato_json_dashboard.md`, `contrato_composicao_corpo.md` |
| `lancador` | `contrato_json_lancador.md`, `contrato_lancador.md` |

A lista de tipos funcionais é fechada — extensões exigem ADR.

### 6.2 Nó estrutural `grupo` (ADR-0015)

`grupo` é nó estrutural de composição. Não é tipo funcional. Pode aparecer em
`corpo.elementos[]` (nível de grupo 1) ou em `grupo.elementos[]` de grupos do
nível 1 (nível de grupo 2) ou do nível 2 (nível de grupo 3). Um `grupo` filho
de grupo do nível 3 estaria no nível 4 e é estruturalmente inválido. Elementos
funcionais dentro de um grupo do nível 3 não constituem nível 4. Múltiplos
grupos irmãos e múltiplos elementos funcionais por grupo são permitidos em
qualquer nível (ADR-0019, D1-D6).

`grupo` não declara: borda, moldura, título, conteúdo, ação, chip, origem de
dados nem `tela_destino`. Declara: `estrutura` (opcional), `arranjo`,
`distribuicao` e `elementos[]`.

Campos mínimos de `grupo` com comportamento `livre` (ou ausência de `estrutura`):

```json
{
  "id": "...",
  "tipo": "grupo",
  "arranjo": "horizontal",
  "elementos": []
}
```

`distribuicao` é opcional em `estrutura: "livre"`. Sua ausência **não** equivale
ao modo `igual` (ADR-0018, 2026-07-11): quando `distribuicao` não é declarada,
o container preserva a construção orientada pelo conteúdo — cada filho usa sua
altura/largura natural, sem repartição proporcional automática. A ausência de
`distribuicao` **não** autoriza sobra como preenchimento externo do container;
toda área atribuída ao grupo deve ser repassada integralmente aos descendentes
visuais (DA-03, ADR-0024): com exatamente um descendente visual (`console`,
`dashboard` ou `lancador`), esse elemento ocupa integralmente a área disponível,
mesmo sem `distribuicao` declarada — decorre da cardinalidade unitária, não
equivale a `distribuicao: igual` (DA-01); com múltiplos descendentes disputando
o mesmo eixo, `distribuicao` é obrigatória — a ausência torna a composição
inválida e exige rejeição explícita (DA-02, DA-04). `igual` permanece modo
válido apenas quando declarado explicitamente. Ver `contrato_composicao_corpo.md`
seção 5.7, ADR-0018 e ADR-0024.

**Comportamento estrutural `estrutura` (ADR-0020, 2026-07-12)**: o campo
`estrutura` é opcional e seleciona o comportamento do `grupo`.

| Valor | Comportamento |
|---|---|
| ausente | equivale a `"livre"` — todos os JSONs existentes continuam válidos |
| `"livre"` | hierárquico unidimensional existente |
| `"matriz"` | bidimensional com grade comum — ver seção 6.4 |

O contrato exige que a ausência de `estrutura` **nunca** ative o comportamento
`matriz`. Grupos sem `estrutura` são tratados como `livre`.

### 6.3 Distribuição por container (ADR-0015)

`corpo` e `grupo` podem declarar `distribuicao`. `distribuicao` é **opcional**
no envelope mínimo — sua ausência é válida.

**Ausência de `distribuicao` não é modo `igual` (ADR-0018, ADR-0024)**: a
ausência **não** equivale ao modo `igual`. Quando `distribuicao` não é
declarada, o container preserva a construção orientada pelo conteúdo — cada filho
usa sua dimensão natural, sem repartição proporcional automática de toda a área
útil. A ausência de `distribuicao` **não** autoriza sobra como preenchimento
externo do container (ADR-0024): com exatamente um descendente visual aplicável,
esse elemento ocupa integralmente a área disponível (DA-01); com múltiplos
elementos disputando o mesmo eixo, `distribuicao` é obrigatória — a ausência
torna a composição inválida e exige rejeição explícita (DA-02, DA-04); composição
que não consiga atribuir toda a área a elemento visual é inválida e deve ser
rejeitada explicitamente, sem fallback silencioso, sem distribuição implícita e
sem alteração automática do JSON (DA-04).

Quando declarada, `distribuicao` rege como a área disponível do container é
repartida entre seus filhos diretos e **aloca área**, não apenas o tamanho do
conteúdo natural. Os modos explícitos válidos são `igual`, `percentual` e
`fracao`; `igual` só se aplica quando declarado, não como default implícito da
ausência. Ver `contrato_composicao_corpo.md` seções 5.7 a 5.9 para modos e regras
de arredondamento, e a ADR-0018 para a semântica de ausência × distribuição
explícita.

Tipo desconhecido em `corpo.elementos[]` é erro de validação.

### 6.4 Campos mínimos de `grupo` com `estrutura: "matriz"` (ADR-0020)

Quando `estrutura: "matriz"`, o objeto `matriz` é obrigatório. O envelope mínimo
válido de uma matriz é:

```json
{
  "id": "...",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {"modo": "igual"}
    },
    "colunas": {
      "quantidade": 2,
      "distribuicao": {"modo": "igual"}
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "a"},
      {"linha": 1, "coluna": 2, "elemento": "b"},
      {"linha": 2, "coluna": 1, "elemento": "c"},
      {"linha": 2, "coluna": 2, "elemento": "d"}
    ]
  },
  "elementos": [
    {"id": "a", "tipo": "console"},
    {"id": "b", "tipo": "console"},
    {"id": "c", "tipo": "dashboard"},
    {"id": "d", "tipo": "console"}
  ]
}
```

Campos obrigatórios em `estrutura: "matriz"`:

| Campo | Regra |
|---|---|
| `matriz.linhas.quantidade` | inteiro no intervalo [2, 4] |
| `matriz.linhas.distribuicao` | obrigatório — ausência invalida a matriz |
| `matriz.colunas.quantidade` | inteiro no intervalo [2, 4] |
| `matriz.colunas.distribuicao` | obrigatório — ausência invalida a matriz |
| `matriz.celulas[]` | quantidade exata = `linhas × colunas`; índices iniciados em 1 |
| `elementos[]` | quantidade exata = `linhas × colunas`; cada `id` referenciado em `celulas[]` |

**O modo `igual` deve ser declarado explicitamente.** Não existe default implícito
para `igual` nem dimensionamento por conteúdo natural em eixo matricial.

**Proibições em `estrutura: "matriz"`:**

- `arranjo` é proibido;
- objeto `matriz` ausente é inválido;
- distribuição ausente em qualquer eixo é inválida;
- célula vazia é proibida na versão atual;
- mesclagem (`rowspan`/`colspan`) está fora de escopo;
- fallback silencioso para `livre` é proibido.

**Rejeição determinística**: o loader deverá futuramente rejeitar toda matriz
inválida com erro determinístico. Nenhuma condição de invalidade pode resultar
em conversão silenciosa para `livre`.

**Matriz não torna-se obrigatória para toda tela.** A matriz é um comportamento
opcional de `grupo` — nenhuma tela é obrigada a usar `estrutura: "matriz"`.

---

## 7. Caminhos canônicos e regra de coincidência de `id`

Conforme ADR-0009 atualizada parcialmente pela ADR-0021, os JSONs de tela
concreta usam duas raízes declarativas:

```text
produto real:  config/telas/<id>.json
demonstracao: config/telas/demo/<id>.json
```

Regras obrigatórias:

- `config/telas/` é reservado às telas do produto real;
- `config/telas/demo/` é a futura raiz das telas demonstrativas;
- o `id` interno declarado no campo `"id"` do JSON deve coincidir com o nome
  base do arquivo em disco, em qualquer uma das raízes;
- o nome do arquivo segue as regras de identificador estável: minúsculo, sem
  acentos, sem espaços, preferencialmente `snake_case`;
- `id` divergente do nome base do arquivo é inconsistência de validação.

Exemplo demonstrativo futuro: tela com `"id": "demo"` deve estar em
`config/telas/demo/demo.json`.

A futura `config/telas/orquestrador.json` fica reservada ao produto real. Pela
ADR-0022, sua identidade será `orquestrador`, seu envelope macro será
`cabecalho`, `corpo` e `barra_de_menus`, e seu corpo inicial conterá `console`
e `dashboard` presentes sem entradas iniciais. Não há alias entre `demo` e
`orquestrador`, nem fallback silencioso entre as duas raízes.

---

## 8. Regras de validação

**V-1. Campos obrigatórios presentes.**
`schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus` devem existir no JSON.
Ausência de qualquer um desses campos é erro de validação.

**V-2. `schema` suportado.**
O valor de `schema` deve ser reconhecido pelo renderer. Versão desconhecida é
erro de validação — o renderer não tenta inferir compatibilidade.

**V-3. `id` estável e sem espaços.**
`id` deve ser string minúscula, sem acentos, sem espaços, sem caracteres
especiais além de `_`. Identificador inválido é erro de validação.

**V-4. `corpo.elementos[]` é lista.**
O campo `elementos` deve ser um array — pode ser vazio mas não pode ser
omitido nem ser de tipo diferente de array.

**V-5. Tipos de elemento conhecidos.**
Todo elemento de `corpo.elementos[]` com `tipo` desconhecido é erro de
validação.

**V-6. Sem estado de runtime.**
O JSON não deve conter campos de estado vivo: cursor atual, página atual,
filtro ativo atual, seleção atual, item focado. Estado pertence à execução,
não à configuração.

**V-7. Sem lógica procedural.**
O JSON não pode declarar comando arbitrário, script livre, loop ou expressão
avaliável em tempo de carga.

**V-8. Coincidência `id`–nome de arquivo.**
O `id` interno deve coincidir com o nome base do arquivo em disco. Divergência
é inconsistência de validação.

**V-9. `estrutura` ausente em `grupo` equivale a `livre` (ADR-0020).**
O loader deverá futuramente tratar a ausência como `livre`. A ausência nunca
ativa o comportamento `matriz`.

**V-10. `estrutura: "matriz"` requer objeto `matriz` com `linhas`, `colunas`
e `celulas` (ADR-0020).**
Ausência do objeto `matriz` em grupo com `estrutura: "matriz"` é inválida.

**V-11. Distribuições de ambos os eixos são obrigatórias em `estrutura: "matriz"`
(ADR-0020).**
O loader deverá futuramente rejeitar qualquer matriz sem
`matriz.linhas.distribuicao` ou sem `matriz.colunas.distribuicao`.

**V-12. Cobertura completa e coordenadas válidas obrigatórias (ADR-0020).**
O loader deverá futuramente rejeitar matrizes com quantidade de células diferente
de `linhas × colunas`, coordenadas duplicadas, elementos duplicados, referências
inválidas ou `arranjo` declarado em conjunto com `estrutura: "matriz"`.

---

## 9. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- campos opcionais do envelope da tela (`metadados`, `bindings`,
  `acoes_registradas`, `filtros`) — cobertos por `contrato_tela_json.md`;
- schema detalhado de cada região (`cabecalho`, `barra_de_menus`) e de cada
  elemento (`console`, `dashboard`, `lancador`) — cobertos por contratos
  incrementais específicos;
- implementação do loader de JSON de tela;
- migração de JSONs transicionais existentes em `config/`;
- criação do JSON real da tela raiz do Orquestrador — aguarda DOC-B011;
- registry de ações, registry de tipos de chip e registry de telas.

---

## 8. Critérios de aceite documental

- [ ] Os seis campos obrigatórios (`schema`, `id`, `cabecalho`, `corpo`,
      `barra_de_menus`, `corpo.elementos`) estão presentes e tipados
      corretamente no JSON mínimo.
- [ ] O JSON mínimo de exemplo deste contrato não contradiz
      `contrato_tela_json.md` nem a ADR-0008 nem a ADR-0009.
- [ ] A lista de tipos válidos em `corpo.elementos[]` é fechada e coincide com
      a taxonomia de `contrato_composicao_corpo.md`.
- [ ] Os caminhos canônicos `config/telas/<id>.json` e
      `config/telas/demo/<id>.json` estão registrados e a regra de coincidência
      de `id` está formalizada para ambas as raízes.
- [ ] Nenhuma seção deste contrato autoriza estado de runtime no JSON de tela.
- [ ] Nenhuma seção deste contrato autoriza lógica procedural ou comando
      arbitrário no JSON de tela.
- [ ] Grupos existentes sem `estrutura` continuam válidos e são tratados como
      `estrutura: "livre"` — nenhum campo novo é obrigatório (ADR-0020, D3, D15).
- [ ] `estrutura: "livre"` preserva `arranjo`, `distribuicao` opcional e semântica
      de ausência conforme ADR-0018 (ADR-0020, D4).
- [ ] `estrutura: "matriz"` requer objeto `matriz` com `linhas.distribuicao`,
      `colunas.distribuicao` e `celulas[]` com cobertura completa (ADR-0020, D6, D8, D10).
- [ ] O envelope mínimo de matriz 2×2 com `igual` explícito nos dois eixos está
      formalmente especificado na seção 6.4 deste contrato.
- [ ] Matriz não é obrigatória para toda tela; `estrutura: "matriz"` é opcional
      para o nó `grupo`.
