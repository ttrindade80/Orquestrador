---
name: ADR-0020-matriz-de-grupos-coordenadas-explicitas
description: Formaliza dois comportamentos estruturais do nó grupo (livre e matriz), o seletor declarativo estrutura, a grade bidimensional comum com coordenadas explícitas de células, distribuições independentes por eixo, regras de compatibilidade retroativa e preservação integral das ADRs-0015, 0018 e 0019
metadata:
  type: adr
  status: aceita
  data: "2026-07-12"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0020 — Matriz declarativa de grupos com coordenadas explícitas

## Status

aceita

## Data

2026-07-12

---

## Contexto

A ADR-0015 formalizou o corpo da tela como árvore de composição, introduziu o
nó estrutural `grupo`, definiu `arranjo` e `distribuicao` por container e os
modos `igual`, `percentual` e `fracao`. A ADR-0018 esclareceu que a ausência de
`distribuicao` preserva a construção orientada pelo conteúdo e não equivale ao
modo `igual`. A ADR-0019 definiu a contagem de profundidade exclusivamente por
níveis de grupos (não por listas `elementos[]`), fixou o limite de três níveis de
grupos e removeu a cardinalidade global de um `dashboard` por tela.

O ciclo H-0027 (commit `c003f3e`) implementou a composição hierárquica com até
três níveis de grupos, aprovada com `I1_IMPLEMENTATION_APPROVED` e 1004/1004
testes passados. O ciclo H-0026 (commit `40015b6`) implementou a distribuição
horizontal percentual e fracionária.

O levantamento documental
(`RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`, `RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`)
confirmou que o comportamento atual do nó `grupo` é inteiramente uniforme: cada
container declara arranjo unidimensional local (`vertical` ou `horizontal`) e
distribui sua área localmente entre seus filhos diretos. Não existe seletor
declarativo de comportamento de grupo, grade bidimensional compartilhada,
coordenadas de células, linhas, colunas ou schema matricial na documentação
normativa ativa.

O levantamento concluiu com `DOCUMENTATION_PATCH_APPROVED_WITH_NOTES` e
indicou como próxima categoria `CRIAR_ADR_MATRIZ_GRUPOS`.

---

## Problema

O comportamento atual do nó `grupo` realiza composição hierárquica recursiva
por containers unidimensionais locais:

- cada container declara arranjo vertical ou horizontal;
- cada container distribui área somente entre seus filhos diretos;
- grupos irmãos calculam suas divisões localmente;
- o alinhamento interno entre grupos distintos depende de condições coincidentes
  (mesmo eixo de arranjo, mesma quantidade de filhos, mesma distribuição,
  mesma dimensão e mesma assinatura de restrições dimensionais —
  conforme ADR-0015 D14 e `contrato_composicao_corpo.md` seção 5.12);
- não existe uma grade bidimensional única compartilhada pelo container;
- não existe seletor declarativo de comportamento estrutural do grupo;
- não existem linhas, colunas e células declarativas para caixas do corpo.

O novo caso de uso requer que todas as caixas de uma composição bidimensional
compartilhem as mesmas coordenadas de linhas e colunas, garantindo alinhamento
das bordas horizontais e verticais de forma determinística, independentemente
de coincidências entre distribuições independentes de grupos irmãos.

---

## Estado atual comprovado de entrada

```yaml
H-0026:
  commit: 40015b6
  estado: fechado

H-0027:
  commit: c003f3e
  estado: fechado
  qa_handoff: H1_HANDOFF_APPROVED
  qa_implementacao: I1_IMPLEMENTATION_APPROVED
  testes: 1004/1004

ADR-0019:
  status: aceita
  aplicacao_documental: aprovada

ADR-0018:
  decisao_normativa: incorporada_aos_contratos_ativos
  status_textual_no_arquivo: proposta
  status_no_indice: aceita
  pendencia: divergencia_documental_localizada
```

A divergência documental da ADR-0018 é histórica e separada desta ADR. Não é
objeto desta ADR, não é corrigida aqui e não bloqueia as decisões abaixo.

---

## Decisões

As decisões abaixo são o registro das decisões explicitamente tomadas pelo
usuário. Esta ADR não escolhe arquitetura adicional, não completa lacunas
silenciosamente, não altera decisões e não amplia o escopo.

---

### D1 — Dois comportamentos estruturais de grupo

O nó `grupo` passa a admitir dois comportamentos estruturais:

```text
livre
matriz
```

#### `livre`

É o nome do comportamento hierárquico atual.

Preserva:

- composição recursiva por containers;
- `arranjo` vertical ou horizontal;
- `distribuicao` local;
- cálculo independente por container;
- todos os JSONs atuais;
- todas as regras atuais quando não há seleção de matriz.

#### `matriz`

É um comportamento declarativo bidimensional.

Define:

- quantidade de linhas;
- quantidade de colunas;
- distribuição independente das linhas;
- distribuição independente das colunas;
- associação explícita de elementos a coordenadas;
- uma grade comum de coordenadas para todas as células.

---

### D2 — Seletor declarativo

O campo canônico do seletor será:

```json
"estrutura": "livre"
```

ou:

```json
"estrutura": "matriz"
```

Não usar `tipo`, pois `tipo` já identifica o nó estrutural (`grupo`).

Não usar `arranjo`, pois `arranjo` já define o eixo de composição.

Não usar `modo` isoladamente, pois esse termo já participa de outros schemas
(campo `distribuicao.modo`).

---

### D3 — Compatibilidade por ausência

Quando `estrutura` não estiver declarada, o comportamento deve ser:

```text
livre
```

Essa regra preserva integralmente todos os JSONs existentes. A ausência do
seletor não pode ativar o comportamento `matriz`.

---

### D4 — Relação com o comportamento atual

`estrutura: livre` mantém a semântica já existente.

Nesse comportamento:

- `arranjo` continua válido;
- `distribuicao` continua local ao container;
- os modos atuais permanecem: `igual`, `percentual`, `fracao`;
- a ausência de `distribuicao` continua seguindo a semântica vigente da
  ADR-0018 (construção orientada pelo conteúdo, não equivalente a `igual`);
- não há grade bidimensional compartilhada;
- não há garantia nova de alinhamento entre divisões internas de grupos
  independentes — apenas as condições já enumeradas na ADR-0015 D14 garantem
  sincronização de cortes.

---

### D5 — Dimensões permitidas da matriz

A matriz deve possuir:

```text
mínimo: 2 linhas × 2 colunas
máximo: 4 linhas × 4 colunas
```

São válidas todas as combinações dentro desses limites, incluindo:

```text
2 × 2  |  2 × 3  |  2 × 4
3 × 2  |  3 × 3  |  3 × 4
4 × 2  |  4 × 3  |  4 × 4
```

Matrizes com uma dimensão menor que 2 ou maior que 4 são inválidas.

Não existe fallback silencioso de matriz inválida para o comportamento `livre`.

---

### D6 — Distribuição independente por eixo

No comportamento `matriz`, as distribuições dos dois eixos são obrigatórias.

Devem estar presentes obrigatoriamente:

```text
matriz.linhas.distribuicao
matriz.colunas.distribuicao
```

A ausência da distribuição de qualquer eixo torna a matriz inválida.

Não existe:

- distribuição implícita;
- default para `igual`;
- cálculo por conteúdo natural;
- herança de distribuição do container pai;
- inferência por quantidade de linhas ou colunas;
- fallback para `estrutura: livre`.

Para obter divisão igual, o JSON deve declarar explicitamente:

```json
"distribuicao": {
  "modo": "igual"
}
```

Cada eixo possui sua própria distribuição independente e pode utilizar as
semânticas já conhecidas de distribuição:

```text
igual
percentual
fracao
```

A distribuição de um eixo não é herdada, inferida ou reutilizada pelo outro eixo.

Nenhum eixo matricial é dimensionado por conteúdo natural.

Exemplo conceitual para uma matriz `2 × 4`:

```text
linhas:  [1, 2]
colunas: [1, 2, 1, 2]
```

Isso significa:

- duas faixas horizontais com proporção `1:2`;
- quatro faixas verticais com proporção `1:2:1:2`.

O primeiro vetor corresponde às linhas; o segundo, às colunas.

A quantidade de valores de cada eixo deve ser coerente com sua respectiva
dimensão declarada.

Para `percentual`, a soma deve ser 100.

Para `fracao`, os valores são pesos positivos.

O algoritmo de arredondamento preserva o princípio vigente dos maiores restos
(ADR-0015 D8), aplicado separadamente em cada eixo.

Esta regra é específica de `estrutura: matriz` e não altera a semântica de
ausência de distribuição no comportamento `livre`.

---

### D7 — Grade comum de coordenadas

O container `matriz` calcula uma única grade de:

- coordenadas horizontais das linhas;
- coordenadas verticais das colunas.

Todas as células usam essas coordenadas comuns.

Consequências obrigatórias:

- bordas horizontais de células da mesma linha permanecem alinhadas;
- bordas verticais de células da mesma coluna permanecem alinhadas;
- os encontros das divisórias compartilham as mesmas coordenadas;
- estruturas como `2 × 2`, `3 × 4` ou `4 × 3` mantêm alinhamento global
  dentro da matriz.

A matriz não deve ser construída como vários grupos irmãos calculando cortes
independentes.

---

### D8 — Coordenadas explícitas para células

Foi escolhida a associação por coordenadas explícitas.

A representação conceitual será:

```json
"celulas": [
  {
    "linha": 1,
    "coluna": 1,
    "elemento": "id_do_elemento"
  },
  {
    "linha": 1,
    "coluna": 2,
    "elemento": "outro_elemento"
  }
]
```

Regras obrigatórias:

- `linha` e `coluna` usam índices iniciados em 1;
- cada entrada associa uma coordenada a um elemento filho;
- `elemento` referencia o `id` de um filho direto declarado em `elementos[]`;
- a posição é determinada pelas coordenadas, não pela ordem do array `celulas[]`;
- cada coordenada pode aparecer no máximo uma vez;
- cada elemento pode ser associado no máximo a uma célula;
- coordenadas fora das dimensões declaradas são inválidas;
- referência a elemento inexistente é inválida;
- duplicidade de coordenada é inválida;
- duplicidade de elemento é inválida.

Como a matriz inicial não admite células vazias:

```text
quantidade de células  = linhas × colunas
quantidade de filhos   = linhas × colunas
```

Toda coordenada válida deve ser declarada exatamente uma vez.

Todo filho direto do grupo `matriz` deve estar associado exatamente uma vez.

Não existe ordem implícita linha a linha ou coluna a coluna.

---

### D9 — Conteúdo das células

A célula referencia um filho direto já declarado em `elementos[]`.

Esse filho pode ser qualquer tipo já permitido pela composição atual:

```text
console
lancador
dashboard
grupo
```

O uso de um `grupo` dentro de uma célula não remove nem amplia o limite atual
de profundidade.

A profundidade continua sendo contada exclusivamente por nós `grupo`, conforme
ADR-0019. O limite máximo continua sendo três níveis de grupos.

Uma matriz não cria um novo tipo funcional.

---

### D10 — Células vazias

Na primeira versão normativa:

```text
células vazias não são permitidas
```

Não criar:

- placeholder;
- célula nula;
- elemento ausente;
- preenchimento automático;
- coordenada reservada sem elemento.

Esse tema poderá ser decidido futuramente por nova ADR ou revisão explícita.

---

### D11 — Mesclagem de células

Permanecem fora de escopo:

```text
rowspan
colspan
mesclagem de células
elemento ocupando múltiplas coordenadas
```

Cada elemento ocupa exatamente uma célula.

---

### D12 — Matriz inválida

Uma declaração matricial inválida deve ser rejeitada deterministicamente.

Não é permitido:

- ignorar campos inválidos;
- corrigir dimensões automaticamente;
- completar células ausentes;
- remover células excedentes;
- converter silenciosamente a estrutura para `livre`;
- inferir coordenadas ausentes.

A forma exata das mensagens de erro pertence à implementação futura, mas elas
devem identificar a região declarativa afetada.

---

### D13 — Interação com `arranjo`

Em `estrutura: matriz`, o posicionamento bidimensional é determinado por:

- linhas;
- colunas;
- distribuições por eixo;
- coordenadas das células.

O campo `arranjo` unidimensional não deve controlar o posicionamento das
células da matriz. Para evitar duas autoridades concorrentes de layout:

```text
arranjo é proibido em estrutura matriz
```

Portanto:

- `arranjo` permanece válido em `livre`;
- `arranjo` é inválido em `matriz`.

---

### D14 — Terminal e área insuficiente

Esta ADR não cria uma nova política global de terminal pequeno.

Preserva:

- obtenção dinâmica das dimensões do terminal (ADR-0017);
- reação a `SIGWINCH` (ADR-0017);
- quadro global de terminal pequeno já existente (ADR-0017);
- políticas atuais que não conflitem com a matriz.

Como consequência de implementação, a matriz não pode romper a integridade
estrutural das células. Entretanto, não estão decididos nesta ADR:

- largura mínima numérica por célula;
- altura mínima numérica por célula;
- truncamento específico para células de matriz;
- paginação da matriz;
- rolagem da matriz;
- redução automática da quantidade de linhas ou colunas.

Esses detalhes permanecem fora de escopo e devem bloquear implementação caso
não possam ser resolvidos pelas regras globais existentes.

---

### D15 — Preservação retroativa

Esta decisão preserva integralmente:

- grupos existentes sem `estrutura`;
- grupos explicitamente `livre`;
- JSONs ativos;
- composição plana;
- composição hierárquica de até três níveis;
- distribuição vertical e horizontal atual;
- ausência de distribuição;
- modos `igual`, `percentual` e `fracao`;
- maiores restos;
- navegação;
- passividade de `dashboard`;
- comportamento de `console` e `lancador`;
- regras de terminal pequeno existentes;
- redimensionamento reativo.

---

### D16 — Matriz não substitui a hierarquia

A matriz é uma especialização declarativa do container `grupo`.

Ela não substitui:

- a árvore do corpo;
- o nó estrutural `grupo`;
- o limite de profundidade;
- a lista `elementos[]`;
- os tipos funcionais existentes.

A matriz organiza os filhos diretos de um grupo em uma grade comum.

---

## Schema conceitual

O schema abaixo é conceitual. Ele não está aplicado aos contratos ativos. A
aplicação documental ocorrerá em etapa posterior, após QA desta ADR.

### Exemplo completo — grupo `matriz` 2 × 4

```json
{
  "id": "grupo_matriz_2x4",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {
        "modo": "fracao",
        "valores": [1, 2]
      }
    },
    "colunas": {
      "quantidade": 4,
      "distribuicao": {
        "modo": "fracao",
        "valores": [1, 2, 1, 2]
      }
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "tela_a"},
      {"linha": 1, "coluna": 2, "elemento": "tela_b"},
      {"linha": 1, "coluna": 3, "elemento": "tela_c"},
      {"linha": 1, "coluna": 4, "elemento": "tela_d"},
      {"linha": 2, "coluna": 1, "elemento": "tela_e"},
      {"linha": 2, "coluna": 2, "elemento": "tela_f"},
      {"linha": 2, "coluna": 3, "elemento": "tela_g"},
      {"linha": 2, "coluna": 4, "elemento": "tela_h"}
    ]
  },
  "elementos": [
    {"id": "tela_a", "tipo": "console"},
    {"id": "tela_b", "tipo": "console"},
    {"id": "tela_c", "tipo": "dashboard"},
    {"id": "tela_d", "tipo": "console"},
    {"id": "tela_e", "tipo": "console"},
    {"id": "tela_f", "tipo": "lancador"},
    {"id": "tela_g", "tipo": "dashboard"},
    {"id": "tela_h", "tipo": "console"}
  ]
}
```

---

## Exemplos válidos

### Grupo `livre` com `estrutura` ausente — comportamento preservado

```json
{
  "id": "grupo_existente",
  "tipo": "grupo",
  "arranjo": "horizontal",
  "distribuicao": {
    "modo": "fracao",
    "valores": [1, 1]
  },
  "elementos": [
    {"id": "a", "tipo": "console"},
    {"id": "b", "tipo": "dashboard"}
  ]
}
```

A ausência de `estrutura` equivale a `estrutura: "livre"`. Todos os JSONs
existentes sem o campo `estrutura` continuam válidos e seu comportamento é
preservado integralmente (D3, D15).

### Grupo `livre` declarado explicitamente

```json
{
  "id": "grupo_livre",
  "tipo": "grupo",
  "estrutura": "livre",
  "arranjo": "vertical",
  "elementos": [
    {"id": "c", "tipo": "console"},
    {"id": "d", "tipo": "lancador"}
  ]
}
```

### Grupo `matriz` mínimo 2 × 2

```json
{
  "id": "grupo_2x2",
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
      {"linha": 1, "coluna": 1, "elemento": "e1"},
      {"linha": 1, "coluna": 2, "elemento": "e2"},
      {"linha": 2, "coluna": 1, "elemento": "e3"},
      {"linha": 2, "coluna": 2, "elemento": "e4"}
    ]
  },
  "elementos": [
    {"id": "e1", "tipo": "console"},
    {"id": "e2", "tipo": "dashboard"},
    {"id": "e3", "tipo": "lancador"},
    {"id": "e4", "tipo": "console"}
  ]
}
```

---

## Exemplos inválidos

### Dimensão menor que 2 — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 1, "distribuicao": {"modo": "igual"}},
    "colunas": {"quantidade": 3, "distribuicao": {"modo": "igual"}},
    "celulas": [...]
  }
}
```

`quantidade: 1` para linhas viola o mínimo de 2 (D5). Deve ser rejeitado.

### Dimensão maior que 4 — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {"quantidade": 5, "distribuicao": {"modo": "igual"}},
    "colunas": {"quantidade": 3, "distribuicao": {"modo": "igual"}},
    "celulas": [...]
  }
}
```

`quantidade: 5` para linhas viola o máximo de 4 (D5). Deve ser rejeitado.

### `arranjo` em `estrutura: matriz` — inválido

```json
{
  "tipo": "grupo",
  "estrutura": "matriz",
  "arranjo": "horizontal",
  "matriz": {...}
}
```

`arranjo` é inválido em `estrutura: matriz` (D13). Deve ser rejeitado.

### Coordenada duplicada — inválido

```json
{
  "celulas": [
    {"linha": 1, "coluna": 1, "elemento": "e1"},
    {"linha": 1, "coluna": 1, "elemento": "e2"}
  ]
}
```

Coordenada `(1, 1)` duplicada (D8). Deve ser rejeitado.

### Elemento duplicado — inválido

```json
{
  "celulas": [
    {"linha": 1, "coluna": 1, "elemento": "e1"},
    {"linha": 1, "coluna": 2, "elemento": "e1"}
  ]
}
```

`e1` aparece em duas células (D8). Deve ser rejeitado.

### Célula excedente — inválido

Matriz declarada como `2 × 2` com 5 células declaradas. Deve ser rejeitado
(D8): a quantidade de células declaradas deve ser exatamente `linhas × colunas`.

### Célula faltante — inválido

Matriz declarada como `2 × 2` com apenas 3 células declaradas. Deve ser
rejeitado (D8): toda coordenada válida deve ser declarada exatamente uma vez.

### Conversão silenciosa para `livre` — proibida

Uma declaração matricial inválida não pode ser silenciosamente convertida para
`livre` (D12). Deve ser rejeitada com erro determinístico.

### Distribuição de linhas ausente — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2
    },
    "colunas": {
      "quantidade": 3,
      "distribuicao": {"modo": "igual"}
    },
    "celulas": [...]
  }
}
```

`linhas.distribuicao` ausente. A distribuição de linhas é obrigatória (D6).
Deve ser rejeitado antes da construção do modelo.

### Distribuição de colunas ausente — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {"modo": "igual"}
    },
    "colunas": {
      "quantidade": 3
    },
    "celulas": [...]
  }
}
```

`colunas.distribuicao` ausente. A distribuição de colunas é obrigatória (D6).
Deve ser rejeitado antes da construção do modelo.

### Tentativa de depender de default implícito — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2
    },
    "colunas": {
      "quantidade": 2
    },
    "celulas": [...]
  }
}
```

Ambos os eixos sem `distribuicao`. Não existe default implícito para `igual` nem
cálculo por conteúdo natural (D6). Deve ser rejeitado.

### Somente um eixo com distribuição — inválido

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {"modo": "igual"}
    },
    "colunas": {
      "quantidade": 2
    },
    "celulas": [...]
  }
}
```

`colunas.distribuicao` ausente. Declarar distribuição em apenas um eixo não
torna a matriz válida; ambos os eixos são obrigatórios (D6). Deve ser rejeitado.

---

## Invariantes

1. `estrutura` ausente equivale a `livre` (D3).
2. `estrutura: livre` preserva o comportamento hierárquico atual sem alteração (D4).
3. `estrutura: matriz` requer o objeto `matriz` com `linhas`, `colunas` e `celulas` (D1, D6, D8).
4. Dimensões válidas: `2 ≤ linhas ≤ 4` e `2 ≤ colunas ≤ 4` (D5).
5. `quantidade de celulas == linhas × colunas` (D8, D10).
6. `quantidade de elementos == linhas × colunas` (D8, D10).
7. Cada coordenada `(linha, coluna)` aparece exatamente uma vez em `celulas[]` (D8).
8. Cada `id` de filho aparece exatamente uma vez em `celulas[]` (D8).
9. Toda referência em `elemento` aponta para um `id` em `elementos[]` (D8).
10. Coordenadas fora das dimensões declaradas são inválidas (D8).
11. `arranjo` é inválido em `estrutura: matriz` (D13).
12. `arranjo` permanece válido em `estrutura: livre` (D4, D13).
13. A grade de coordenadas é calculada uma única vez e compartilhada por todas as células (D7).
14. Divisórias horizontais de células da mesma linha compartilham coordenada (D7).
15. Divisórias verticais de células da mesma coluna compartilham coordenada (D7).
16. Matriz não acrescenta nível de grupo: apenas um nó estrutural `grupo` conta (D9, ADR-0019 D1).
17. Distribuição de cada eixo aplica maiores restos separadamente (D6, ADR-0015 D8).
18. Matriz inválida é rejeitada deterministicamente, sem fallback silencioso (D12).

### Invariantes de distribuição de eixo matricial

```text
INV-MAT-DIST-01:
Toda matriz declara distribuição de linhas.

INV-MAT-DIST-02:
Toda matriz declara distribuição de colunas.

INV-MAT-DIST-03:
A ausência da distribuição de qualquer eixo invalida a matriz.

INV-MAT-DIST-04:
O modo igual depende de declaração explícita.

INV-MAT-DIST-05:
Nenhum eixo matricial é dimensionado por conteúdo natural.

INV-MAT-DIST-06:
A distribuição de um eixo não é herdada, inferida ou reutilizada pelo outro eixo.
```

---

## Relação com ADR-0015

A ADR-0015 é **preservada e complementada**:

- a composição hierárquica do corpo como árvore permanece vigente;
- o nó estrutural `grupo` permanece como única instância sem natureza funcional;
- `arranjo` e `distribuicao` por container permanecem válidos no comportamento `livre`;
- os modos `igual`, `percentual` e `fracao` permanecem;
- o algoritmo dos maiores restos permanece, aplicado por eixo na matriz;
- o preenchimento da área alocada permanece;
- a sincronização de cortes descrita na D14 da ADR-0015 permanece para `livre`;
- esta ADR **adiciona** uma especialização bidimensional ao nó `grupo` —
  o comportamento `matriz` — sem cancelar nem reescrever a ADR-0015.

A ADR-0020 não substitui a ADR-0015 integralmente. Especializa o campo de
atuação do nó `grupo` sem alterar as regras para o comportamento `livre`.

---

## Relação com ADR-0018

### Comportamento `livre`

A ausência de `distribuicao` no comportamento `livre` continua seguindo a
semântica vigente da ADR-0018:

- não equivale automaticamente a `igual`;
- preserva a construção orientada pelo conteúdo;
- nenhuma regra do comportamento atual é modificada.

### Comportamento `matriz`

A matriz é uma especialização nova que exige distribuição explícita nos dois eixos.

Por isso:

- a ausência de `matriz.linhas.distribuicao` é inválida;
- a ausência de `matriz.colunas.distribuicao` é inválida;
- essa obrigatoriedade não redefine a semântica geral da ADR-0018;
- não existe equivalência entre ausência e `igual` na matriz;
- o modo `igual` deve ser explicitamente declarado.

A ADR-0020 não corrige nem substitui integralmente a ADR-0018. A ADR-0018 é
preservada integralmente no que diz respeito ao comportamento `livre`. A
obrigatoriedade de distribuição explícita nos eixos da matriz é uma decisão de
especialização nova, não uma alteração da semântica geral da ADR-0018.

A distinção entre arranjo e distribuição permanece vigente (ADR-0018 D1).

A divergência textual de status da ADR-0018 (arquivo: `proposta`; índice:
`aceita`) é pendência histórica separada e não é objeto desta ADR.

---

## Relação com ADR-0019

A ADR-0019 é **preservada integralmente**:

- o limite máximo de três níveis de grupos permanece;
- a contagem de profundidade continua sendo feita exclusivamente por nós
  estruturais `grupo`;
- a multiplicidade de filhos por container permanece;
- `estrutura: matriz` não acrescenta nível por linha, coluna ou célula;
- um `grupo` usado como filho dentro de uma célula da matriz continua sendo
  contado como nível de grupo normalmente;
- somente nós `grupo` contam na profundidade — elementos funcionais dentro de
  células não criam nível adicional.

---

## Compatibilidade retroativa

Esta ADR é retroativamente compatível com todos os JSONs existentes.

Mecanismo de compatibilidade:

1. Grupos sem `estrutura` continuam operando como `livre` (D3).
2. O comportamento `livre` preserva `arranjo`, `distribuicao` e todos os modos
   vigentes (D4).
3. Nenhum campo novo é obrigatório em grupos existentes.
4. Os JSONs de tela ativos (`orquestrador.json`, `grupo_minimo.json`,
   `destino_minimo.json`, `stub_b.json`) continuam válidos sem alteração.

---

## Consequências documentais

Os documentos abaixo são identificados para futura aplicação documental. Nenhum
é alterado por esta ADR.

| Documento | Ação futura |
|---|---|
| `scripts/docs/NOMENCLATURA.md` | Adicionar termos: `estrutura`, `livre`, `matriz`, `linhas`, `colunas`, `celulas`; definir limites de dimensão e regras de coordenadas |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | Adicionar D1–D16; especificar objeto `matriz`, grade comum, validações de coordenadas, invariantes e proibições |
| `scripts/docs/contratos/contrato_tela_json.md` | Adicionar campo `estrutura` ao schema do nó `grupo`; registrar objeto `matriz` e seus sub-campos |
| `scripts/docs/contratos/contrato_json_tela_minima.md` | Integrar regras de validação para `estrutura` e `matriz` |
| `scripts/docs/adr/INDICE_ADR.md` | Registrar ADR-0020 na tabela de decisões |

---

## Consequências futuras de implementação

As consequências abaixo são identificadas para ciclos de implementação futuros.
Esta ADR não implementa nenhuma delas.

### Loader

Deverá futuramente validar:

- presença e valor do campo `estrutura`;
- objeto `matriz` quando `estrutura: matriz`;
- dimensões entre 2 e 4 para linhas e colunas;
- presença de `matriz.linhas.distribuicao`;
- presença de `matriz.colunas.distribuicao`;
- objeto de distribuição válido em cada eixo;
- modo aceito em cada eixo (`igual`, `percentual` ou `fracao`);
- quantidade de valores coerente com a dimensão do eixo;
- soma percentual igual a 100 (modo `percentual`);
- pesos positivos (modo `fracao`);
- array `celulas[]`;
- cobertura completa de coordenadas (`linhas × colunas` células);
- referências a filhos diretos válidos em `elementos[]`;
- ausência de duplicidade de coordenadas;
- ausência de duplicidade de elemento;
- proibição de células vazias;
- proibição de `arranjo` quando `estrutura: matriz`;
- limite de profundidade (ADR-0019).

A rejeição de qualquer eixo sem distribuição deve ocorrer de forma determinística,
antes da construção do modelo e antes da renderização.

### Modelo

O modelo deverá receber uma matriz já validada pelo loader, contendo:

- distribuição explícita de linhas;
- distribuição explícita de colunas;
- nenhuma representação de eixo matricial sem distribuição.

O modelo não deve preencher defaults nem inferir distribuição. A validação da
presença e da validade das distribuições é responsabilidade do loader.

Deverá futuramente preservar:

- estrutura escolhida (`livre` ou `matriz`);
- dados das linhas e colunas com distribuições explícitas por eixo;
- coordenadas explícitas de cada célula;
- vínculo entre célula e filho direto;
- ordem declarativa dos filhos;
- árvore de composição.

### Renderizador

O renderizador recebe os dois eixos com distribuições explícitas e:

- não calcula tamanho natural para linhas ou colunas;
- não escolhe default de distribuição;
- não converte omissão em `igual`;
- aplica o algoritmo do modo declarado separadamente em cada eixo.

Deverá futuramente:

- calcular cortes horizontais (linhas) uma única vez para o container;
- calcular cortes verticais (colunas) uma única vez para o container;
- usar a grade comum calculada para todas as células;
- renderizar cada elemento na área da célula correspondente;
- aplicar maiores restos separadamente por eixo;
- preservar bordas alinhadas dentro da matriz;
- não calcular subgrades independentes para grupos irmãos pertencentes à mesma
  matriz.

---

## Testes futuros

Deverão futuramente cobrir, no mínimo:

- todas as dimensões de `2 × 2` a `4 × 4`;
- matriz válida com `igual` explícito nos dois eixos;
- matriz válida com modos diferentes entre os eixos (ex.: `igual` em linhas e
  `fracao` em colunas);
- distribuições iguais por eixo;
- percentuais por eixo;
- frações por eixo;
- pesos diferentes por eixo;
- ausência da distribuição de linhas — deve ser rejeitado;
- ausência da distribuição de colunas — deve ser rejeitado;
- ausência em ambos os eixos — deve ser rejeitado;
- somente um eixo com distribuição — deve ser rejeitado;
- tentativa de depender de `igual` implícito — deve ser rejeitado;
- coordenadas fora do limite declarado;
- coordenadas duplicadas;
- elementos duplicados em `celulas[]`;
- elementos inexistentes em `celulas[]`;
- células faltantes (menos de `linhas × colunas`);
- células excedentes (mais de `linhas × colunas`);
- `arranjo` presente em `estrutura: matriz` — deve ser rejeitado;
- ausência de `estrutura` — deve comportar-se como `livre`;
- `estrutura: livre` explícito;
- confirmação de que grupos `livre` continuam aceitando ausência de distribuição
  segundo a ADR-0018;
- confirmação de que matriz inválida não cai para `livre`;
- matriz dentro dos limites de profundidade permitidos;
- `grupo` dentro de célula da matriz que criaria quarto nível de grupo — deve
  ser rejeitado;
- preservação dos JSONs existentes sem alteração de comportamento;
- alinhamento de divisórias horizontais entre células da mesma linha;
- alinhamento de divisórias verticais entre células da mesma coluna;
- redimensionamento reativo com matriz ativa (`SIGWINCH`);
- terminal pequeno segundo as regras globais existentes da ADR-0017.

---

## Limitações

- A grade compartilhada garante alinhamento dentro do container `matriz`. O
  alinhamento entre diferentes containers (dois grupos `matriz` irmãos, ou um
  grupo `matriz` e um grupo `livre` irmão) não é objeto desta ADR e segue as
  regras vigentes da ADR-0015 D14.
- A política de terminal insuficiente para matrizes grandes (ex.: `4 × 4` em
  terminal estreito) não está decidida além das regras globais existentes da
  ADR-0017.

---

## Fora de escopo

Declarados explicitamente fora de escopo desta ADR:

- implementação de qualquer código;
- alteração de testes existentes;
- alteração de JSON ativo;
- aplicação documental (contratos, nomenclatura, índice);
- atualização de `INDICE_ADR.md`;
- criação de handoff;
- correção da divergência de status da ADR-0018;
- matriz com mais de quatro linhas;
- matriz com mais de quatro colunas;
- matriz com dimensão 1 (uma linha ou uma coluna);
- células vazias em qualquer forma (placeholders, nulos, reservados);
- `rowspan`;
- `colspan`;
- mesclagem de células;
- paginação da matriz;
- rolagem da matriz;
- nova política global de terminal pequeno;
- alteração de comportamento de navegação;
- novo tipo funcional;
- alteração dos comportamentos internos de `console`, `lancador` ou `dashboard`;
- alinhamento entre containers distintos (`matriz`–`livre` ou `matriz`–`matriz`
  irmãos).

---

## Critérios para futura aplicação documental

A aplicação documental futura precisa:

- registrar o campo `estrutura` e seus valores (`livre`, `matriz`) em todos os
  contratos afetados;
- registrar o objeto `matriz` com `linhas`, `colunas` e `celulas`;
- registrar as dimensões mínima e máxima;
- registrar a proibição de `arranjo` em `estrutura: matriz`;
- registrar as regras de coordenadas e de cobertura completa;
- registrar a proibição de células vazias nesta versão;
- preservar todas as regras do comportamento `livre`;
- preservar a compatibilidade retroativa dos JSONs existentes;
- não alterar as regras de distribuição, arredondamento ou profundidade;
- não introduzir campos obrigatórios em grupos sem `estrutura`.

---

## Critérios para futuro handoff

Um handoff de implementação poderá ser criado após:

- QA desta ADR;
- aplicação documental confirmada (contratos e nomenclatura refletem D1–D16);
- QA da aplicação documental;
- os contratos afetados não contradizerem as decisões desta ADR;
- o levantamento de implementação do handoff identificar o escopo mínimo de
  alterações no loader, modelo, renderizador e testes necessário para suportar
  o comportamento `matriz`.

---

## Pendências não resolvidas

As pendências abaixo são externas às decisões D1–D16 e permanecem abertas:

1. **Política específica para área insuficiente na matriz**: quando o terminal
   não comporta a grade bidimensional declarada e as regras globais existentes
   da ADR-0017 não resolvem, a política específica para a matriz ainda não está
   decidida. Esse item deve bloquear implementação se não puder ser resolvido
   pelas regras globais.
2. **Suporte futuro a células vazias**: poderá ser decidido por nova ADR ou
   revisão explícita desta.
3. **Suporte futuro a mesclagem (`rowspan`/`colspan`)**: poderá ser decidido por
   nova ADR.
4. **Suporte futuro a dimensões acima de `4 × 4`**: poderá ser decidido por nova
   ADR mediante decisão explícita do usuário.

Essas pendências não enfraquecem as decisões D1–D16.

---

## Documentos consultados

| Documento | Tipo | Papel nesta ADR |
|---|---|---|
| `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md` | Relatório | Evidência processual e técnica do estado atual |
| `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md` | Relatório | Confirmação da qualidade do levantamento |
| `scripts/docs/NOMENCLATURA.md` | Nomenclatura | Autoridade terminológica |
| `scripts/docs/adr/INDICE_ADR.md` | Índice | Confirmação do próximo identificador sequencial |
| `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | ADR | Autoridade normativa sobre composição hierárquica e distribuição |
| `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ADR | Autoridade normativa sobre ausência de distribuição |
| `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | ADR | Autoridade normativa sobre profundidade e multiplicidade |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | Contrato | Norma de aplicação direta sobre composição |
| `scripts/docs/contratos/contrato_tela_json.md` | Contrato | Norma de aplicação direta sobre schema de tela |
| `scripts/docs/contratos/contrato_json_tela_minima.md` | Contrato | Norma de aplicação direta sobre JSON mínimo |
| `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` | Handoff | Registro histórico de escopo executado |
| `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` | Relatório | Evidência de conformidade (1004/1004) |
| `scripts/docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` | Relatório | Evidência de fechamento do ciclo H-0027 |
