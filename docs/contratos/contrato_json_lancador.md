---
name: contrato-json-lancador
description: Especifica a forma mínima de um elemento tipo lancador em corpo.elementos[] do JSON de tela — campos de item, tela_destino, regras de exibicao e limites declarativos
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_lancador.md
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_composicao_corpo.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo de elemento `lancador` (`contrato_json_lancador.md`)

## 1. Objetivo

Especificar a forma mínima de um elemento do tipo `lancador` declarado em
`corpo.elementos[]` no JSON de tela concreto: os campos obrigatórios do
envelope do elemento, os campos obrigatórios de cada item, as regras de
`tela_destino`, os limites de `texto`, e as restrições que decorrem de
`contrato_lancador.md`.

---

## 2. Natureza e escopo

`lancador` é um tipo de elemento do corpo. Uma ocorrência concreta de
`lancador` é uma instância declarada em `corpo.elementos[]` no JSON de tela.
O `lancador` não é uma região fixa da tela — não é `barra_de_menus`, não é
`cabecalho`.

Este contrato especifica apenas a **representação mínima de um elemento
`lancador` no JSON de tela**. As regras semânticas completas (layout de
matriz/fila, vãos, alinhamento, título na borda) pertencem a
`contrato_lancador.md`, que continua sendo a autoridade sobre o comportamento
do tipo.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seção 10) estabelece que:

- `lancador` é elemento de corpo do tipo `lancador`;
- campos mínimos da instância: `id`, `tipo = lancador`, `titulo`,
  `itens[]`, `layout`/`regras_exibicao`;
- cada item deve ter no mínimo: `id`, `chip` ou tecla, `texto`,
  `tela_destino`;
- adicionar item ao `lancador` é alteração declarativa no JSON;
- o código apenas percorre `itens[]`;
- `lancador` não é navegável por `[✥]`.

Este contrato operacionaliza esses princípios para o formato JSON concreto.

---

## 4. JSON mínimo

A forma mínima de um elemento `lancador` em `corpo.elementos[]` é:

```json
{
  "id": "lancador_principal",
  "tipo": "lancador",
  "titulo": "Navegar",
  "itens": [
    {
      "id": "abrir_destino_minimo",
      "chip": "D",
      "texto": "Destino",
      "tela_destino": "destino_minimo"
    }
  ],
  "regras_exibicao": {
    "alinhamento": "esquerda"
  }
}
```

---

## 5. Campos obrigatórios

### 5.1 Campos do envelope do elemento `lancador`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador estável e único do elemento no escopo do `tela.json`. Elemento sem `id` é inválido. |
| `tipo` | string | Deve ser o valor literal `"lancador"`. |
| `titulo` | string | Texto exibido integrado à linha de borda superior do `lancador`. Declarado pela instância. |
| `itens` | array | Lista de itens da instância. Itens concretos pertencem ao JSON da tela. O renderer apenas percorre. |
| `regras_exibicao` | objeto | Regras de alinhamento e layout da instância. O renderer aplica; não decide. |
| `regras_exibicao.alinhamento` | string | `"esquerda"`, `"centro"` ou `"direita"`. Regra desconhecida é erro de validação. |

### 5.2 Campos obrigatórios de cada item em `itens[]`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador estável do item no escopo da instância. Item sem `id` é inválido. |
| `chip` | string | Tecla/letra de identificação do item — exibida dentro do chip visual. O renderer não hardcoda este valor. |
| `texto` | string | Rótulo descritivo do destino. **Máximo de 15 caracteres.** Item com `texto` acima de 15 caracteres é rejeitado em validação — nunca truncado automaticamente. |
| `tela_destino` | string | Identificador formal da tela a ser aberta. Não é texto de exibição — é chave de carregamento. |

---

## 6. Regras de validação

**V-1. `lancador` é elemento do corpo.**
O `lancador` só pode aparecer como elemento de `corpo.elementos[]`. Nunca
como seção raiz da tela, nunca como substituto de `barra_de_menus`.

**V-2. `id` do elemento presente e único.**
Elemento `lancador` sem `id` é inválido. `id` duplicado no escopo de
`corpo.elementos[]` é erro de validação.

**V-3. `itens[]` é array.**
O campo `itens` deve ser array. Pode ser vazio estruturalmente, mas
`lancador` sem itens é semanticamente inútil.

**V-4. Todo item tem `id`.**
Item sem `id` é inválido.

**V-5. Todo item tem `chip`.**
Item sem `chip` é inválido.

**V-6. `texto` máximo 15 caracteres — rejeitado, nunca truncado.**
`texto` acima de 15 caracteres deve ser rejeitado em verificação. O renderer
nunca trunca nem abrevia o `texto` silenciosamente.

**V-7. `tela_destino` é campo declarativo válido.**
`tela_destino` é um campo declarativo formal em todo item. Sua ausência é
inválida. Quando a validação semântica completa é executada, a tela
referenciada deve existir na raiz declarativa explícita do ponto de entrada:
`config/telas/<tela_destino>.json` para produto real ou
`config/telas/demo/<tela_destino>.json` para demonstração.

Nota: em ciclo inerte (renderização sem navegação ativa), `tela_destino` pode
não ser acionado — mas permanece campo declarativo obrigatório do item. Não
declarar `tela_destino` por razão de ciclo inerte é violação contratual.

**V-8. Ações do item são declarativas.**
O item do `lancador` só aciona navegação declarativa para `tela_destino`.
Nenhum item pode executar processo, filtrar dado ou declarar lógica
procedural.

**V-9. `lancador` não é navegável por `[✥]`.**
O chip `[✥]` e as setas do teclado controlam somente cursor de `console`
navegável. `lancador` não participa da condição de existência nem de ativação
de `[✥]` (ADR-0005).

**V-10. Renderer percorre `itens[]`; não hardcoda itens.**
O renderer não cria item não declarado, não hardcoda chip, texto ou destino.
Adicionar, remover ou alterar item é alteração declarativa no JSON da tela.

---

## 7. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- regras de layout interno do `lancador` (matriz/fila, vãos, sub-colunas) —
  pertencem a `contrato_lancador.md` seção 6;
- parâmetros de layout do tipo em `config/elementos/lancador.json`
  (transicional por ADR-0008 e ADR-0021) — pertencem ao artefato transicional;
- título do `lancador` na borda — regido por `contrato_lancador.md`
  seção 4.2;
- estilo visual do chip do item (caracteres de abertura/fechamento) —
  pertencem ao schema de estilo ativo (`contrato_estilo.md`).

---

## 8. Critérios de aceite documental

- [ ] O JSON mínimo contém `id`, `tipo`, `titulo`, `itens[]` e
      `regras_exibicao`.
- [ ] Cada item do JSON mínimo contém `id`, `chip`, `texto` e
      `tela_destino`.
- [ ] `texto` máximo de 15 caracteres está formalizado.
- [ ] `tela_destino` é campo declarativo obrigatório, mesmo em ciclo inerte.
- [ ] `lancador` está posicionado em `corpo.elementos[]`, não como seção raiz
      nem como substituto de `barra_de_menus`.
- [ ] `lancador` não é navegável por `[✥]` está declarado.
- [ ] O JSON mínimo não contradiz `contrato_lancador.md` nem
      `contrato_tela_json.md`.

---

## 9. Distribuição matricial de nível único (ADR-0025)

A ADR-0025 (2026-07-16) permite que o `lancador` adote a capacidade de
distribuição matricial configurável de nível único mediante declaração explícita
no seu JSON em `corpo.elementos[]`. Esta seção formaliza a adoção explícita e
mapeia os parâmetros específicos existentes.

### 9.1 Localização do campo

O campo `distribuicao_matricial` é declarado no nível do elemento `lancador`,
ao lado dos demais campos do envelope:

```json
{
  "id": "lancador_principal",
  "tipo": "lancador",
  "titulo": "Navegar",
  "itens": [],
  "regras_exibicao": {
    "alinhamento": "esquerda"
  },
  "distribuicao_matricial": {
    "formacao": {
      "politica": "preferencia_colunas",
      "colunas": { "minimo": 1 },
      "linhas":  { "minimo": 1 }
    },
    "ordem": "por_coluna",
    "dimensionamento": {
      "colunas": { "politica": "maior_da_coluna" },
      "linhas":  { "politica": "maior_da_linha" }
    },
    "espacamento": {
      "margem_superior":  { "minimo": 1 },
      "margem_inferior":  { "minimo": 1 },
      "margem_esquerda":  { "minimo": 2, "maximo": 5 },
      "margem_direita":   { "minimo": 2 },
      "vao_horizontal":   { "minimo": 2, "maximo": 5 },
      "vao_vertical":     { "minimo": 0, "maximo": 2 }
    },
    "distribuicao_horizontal": { "politica": "inicio" },
    "distribuicao_vertical":   { "politica": "inicio" },
    "ordem_expansao": {
      "horizontal": "vaos_primeiro_depois_margens",
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

O exemplo acima é ilustrativo e não substitui as políticas específicas ativas.
Valores concretos pertencem ao JSON da tela.

### 9.2 Vocabulário de campos

O vocabulário de campos de `distribuicao_matricial` para o `lancador` é idêntico
ao definido em `contrato_json_dashboard.md` seções 9.2 e 9.2.1. Todos os campos,
valores permitidos, obrigatoriedades, rejeições e regras de tratamento se aplicam
sem exceção, incluindo o tratamento normativo de `"minimo_fixo"` definido na
seção 9.2.1 daquele contrato.

### 9.3 Compatibilidade com JSONs existentes e parâmetros específicos

A ausência de `distribuicao_matricial` preserva integralmente as políticas
específicas do `lancador`:

- algoritmo automático de cálculo de colunas (ADR-0001): modo `fila` ou
  `matriz` calculado a partir da largura real do terminal;
- bloco à esquerda com sobra à direita (ADR-0002);
- vãos elásticos entre itens com mínimos e máximos (ADR-0003);
- largura mínima funcional e fallback global (ADR-0023);
- parâmetros de `config/elementos/lancador.json` (transicional).

### 9.4 Precedência quando `distribuicao_matricial` está presente (DEC-APP-0025-02)

Quando `distribuicao_matricial` for declarado em um `lancador`, essa
configuração tem precedência sobre as políticas das ADR-0001, ADR-0002 e
ADR-0003 que tratem das mesmas responsabilidades. Ver `contrato_lancador.md`
seção 11.3 para a tabela normativa completa de precedência.

| Campo em `distribuicao_matricial` | Política substituída | Regra |
|---|---|---|
| `formacao.politica` | Algoritmo automático fila/matriz (ADR-0001) | `distribuicao_matricial` tem precedência quando presente |
| `distribuicao_horizontal.politica` + `espacamento.margem_direita` | Bloco à esquerda + sobra à direita (ADR-0002) | `distribuicao_matricial` tem precedência quando presente |
| `espacamento.vao_horizontal` | Vãos elásticos entre itens/colunas (ADR-0003) | `distribuicao_matricial` tem precedência quando presente |
| `espacamento.margem_esquerda` / `margem_direita` | Margens borda↔elemento (ADR-0003) | `distribuicao_matricial` tem precedência quando presente |

As políticas substituídas **não concorrem, não complementam e não coexistem**
com `distribuicao_matricial` quando o campo está presente.

**Quando `distribuicao_matricial` está ausente**: ADR-0001, ADR-0002 e ADR-0003
permanecem vigentes integralmente. Os parâmetros de
`config/elementos/lancador.json` não são alterados por esta aplicação.

### 9.5 Divergência do H-0034

A divergência da política geométrica do H-0034 não é corrigida por esta
aplicação documental nem pelo PATCH_APLICACAO_ADR. A correção geométrica do
`lancador` continua sendo ciclo documental próprio, independente da ADR-0025.

A reconciliação entre `distribuicao_matricial` e as políticas das ADR-0001,
ADR-0002 e ADR-0003 foi formalizada pela seção 9.4 (DEC-APP-0025-02) e pela
seção 11.3 de `contrato_lancador.md`. A H-0034 é divergência distinta e
permanece separada.

### 9.6 Fallback

Quando `distribuicao_matricial` for declarado e nenhuma formação válida couber,
o estado exibido é o `quadro mínimo de terminal pequeno` (ADR-0017, ADR-0023).
As regras da seção 6.7 de `contrato_lancador.md` permanecem vigentes.
