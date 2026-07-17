---
name: contrato-json-dashboard
description: Especifica o envelope mínimo de um elemento tipo dashboard em corpo.elementos[] do JSON de tela — passivo, opcional, sem conteúdo universal, modelo para contratos futuros de conteúdo
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_composicao_corpo.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo de elemento `dashboard` (`contrato_json_dashboard.md`)

## 1. Objetivo

Especificar apenas o **envelope mínimo** de um elemento do tipo `dashboard`
declarado em `corpo.elementos[]` no JSON de tela concreto: os campos mínimos
do envelope, a natureza passiva e opcional do elemento, a ausência de conteúdo
universal fixo, e o modelo normativo que todo contrato futuro de conteúdo de
`dashboard` deve seguir.

Este contrato fecha o envelope mínimo. Não fecha conteúdo interno. Cada tipo
real de conteúdo de `dashboard` terá contrato próprio.

---

## 2. Natureza e escopo

`dashboard` é um tipo de elemento do corpo passivo e opcional. Uma ocorrência
concreta de `dashboard` é uma instância declarada em `corpo.elementos[]` no
JSON de tela.

Propriedades fundamentais:

- `dashboard` é **passivo** — não aceita cursor navegável, não responde a
  setas do teclado, não expõe ação de Enter;
- `dashboard` é **opcional** — sua presença exige declaração explícita em
  `corpo.elementos[]`; ausência não gera estrutura nem espaço reservado;
- `dashboard` **não tem conteúdo universal fixo** — não existe conteúdo
  padrão válido para qualquer tela;
- conteúdo concreto pertence ao JSON da tela, declarado pela instância;
- **não existe `config/dashboard.json`** — conteúdo de `dashboard` não é
  configuração global por componente (ADR-0008, decisão 7).

Este contrato especifica apenas o **envelope mínimo** do elemento. As regras
de composição e posicionamento no corpo pertencem a
`contrato_composicao_corpo.md`.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seção 11) estabelece que:

- `dashboard` é instância passiva configurável por tela;
- não é navegável por `[✥]`;
- não é obrigatório;
- possui moldura própria;
- não possui conteúdo universal fixo.

Este contrato operacionaliza esses princípios para o formato JSON concreto e
estabelece o modelo para contratos futuros de conteúdo de `dashboard`.

---

## 4. JSON mínimo

O envelope mínimo de um elemento `dashboard` em `corpo.elementos[]` é:

```json
{
  "id": "dashboard_principal",
  "tipo": "dashboard",
  "titulo": "Resumo",
  "conteudo": {
    "tipo": "placeholder",
    "binding": null
  },
  "regras_exibicao": {
    "posicao_dashboard": "vertical"
  }
}
```

Observações sobre o envelope mínimo:

- `conteudo.tipo: "placeholder"` indica ausência de conteúdo real — é o
  valor mínimo válido antes de um contrato de conteúdo ser aplicado;
- `conteudo.binding: null` indica que não há vínculo de dados declarado;
- `regras_exibicao.posicao_dashboard`: **campo transicional — superado pela
  ADR-0010 (2026-07-08)**. A posição do `dashboard` no corpo é controlada
  pela estrutura declarativa geral do `corpo`, como acontece com `console` e
  `lancador`. O campo `posicao_dashboard` não é eixo independente de
  `arranjo` nem de `tiling`. JSONs existentes com este campo podem ser
  honrados por compatibilidade em ciclo futuro de migração. A migração/
  descarte do campo ocorrerá em handoff numerado posterior.
- Pela ADR-0022, a futura tela inicial real `orquestrador` deverá ter um
  `dashboard` estruturalmente presente e sem entradas iniciais. O envelope
  `conteudo.tipo: "placeholder"` com `conteudo.binding: null` representa
  ausência de dados reais ou demonstrativos; essa decisão não reativa
  `regras_exibicao.posicao_dashboard` como eixo de posicionamento.

---

## 5. Campos obrigatórios

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador estável e único do elemento no escopo de `corpo.elementos[]`. Elemento sem `id` é inválido. |
| `tipo` | string | Deve ser o valor literal `"dashboard"`. |
| `titulo` | string | Rótulo identificador da instância — exibido na borda ou como cabeçalho do elemento. Declarado pela instância. |
| `conteudo` | objeto | Envelope de conteúdo. Deve declarar ao menos `tipo` e `binding`. Conteúdo concreto pertence ao JSON da tela; cada tipo real de conteúdo tem contrato próprio. |
| `conteudo.tipo` | string | Tipo de conteúdo: `"placeholder"` (sem conteúdo real) ou identificador de tipo real definido por contrato próprio. |
| `conteudo.binding` | objeto ou null | Vínculo declarativo com a origem de dados. `null` quando não há dados vinculados. |
| `regras_exibicao` | objeto | Regras de posicionamento e exibição da instância no corpo. A posição visual do `dashboard` é controlada pela estrutura declarativa geral do `corpo` (ADR-0010). |
| `regras_exibicao.posicao_dashboard` | string (transicional) | **Campo descontinuado como eixo independente (ADR-0010)**. `"vertical"` ou `"horizontal"`. JSONs existentes com este campo podem ser honrados por compatibilidade em handoff futuro de migração. Não é eixo separado de `arranjo` nem de `tiling`. |

---

## 6. Regras de validação

**V-1. `dashboard` é elemento do corpo e é opcional.**
`dashboard` só aparece como elemento de `corpo.elementos[]`. A ausência de
elemento com `tipo = "dashboard"` é estado normal — `dashboard` nunca existe
por default.

**V-2. `id` presente e único.**
Elemento `dashboard` sem `id` é inválido. `id` duplicado no escopo de
`corpo.elementos[]` é erro de validação.

**V-3. `dashboard` não é navegável por `[✥]`.**
`dashboard` é passivo. Não expõe cursor navegável. O chip `[✥]` não pode ter
`dashboard` como condição de existência ou de ativação (ADR-0005).

**V-4. Conteúdo pertence ao JSON da tela.**
Conteúdo concreto de `dashboard` é declarado pela instância no JSON de cada
tela. Não existe conteúdo universal padrão aplicável a qualquer tela.

**V-5. Não existe `config/dashboard.json`.**
Nenhum arquivo global `config/dashboard.json` deve ser criado. Conteúdo de
`dashboard` não é configuração global por componente (ADR-0008, decisão 7).

**V-6. Tipo de conteúdo desconhecido é erro de validação.**
`conteudo.tipo` com valor não registrado é erro de validação. `"placeholder"`
é valor de reserva enquanto não há contrato de conteúdo aplicado.

**V-7. Posição do `dashboard` é controlada pela composição geral do corpo (ADR-0010).**
A posição visual do `dashboard` no corpo é definida pela estrutura declarativa
do `corpo`, como acontece com `console` e `lancador`. O campo
`regras_exibicao.posicao_dashboard` está descontinuado como eixo de
posicionamento independente de `arranjo` e `tiling` (ADR-0010, 2026-07-08).
JSONs existentes com esse campo podem ser honrados por compatibilidade em
handoff futuro de migração; a migração/descarte ocorrerá em handoff
numerado posterior. A sequência anterior de planejamento foi
cancelada/removida e não orienta novos ciclos.

---

## 7. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- conteúdo interno de qualquer instância de `dashboard` — cada tipo real de
  conteúdo terá contrato próprio (`contrato_conteudo_dashboard_<tipo>.md`);
- regras de renderização visual do `dashboard` (moldura, alinhamento de
  rótulos) — pertencem a `contrato_composicao_corpo.md` seção 5.3;
- draft da instância de `dashboard` da tela raiz do Orquestrador (8 campos
  + Total + 8 marcadores) — é instância demonstrativa/transicional, não regra
  universal nem conteúdo da futura tela inicial real definida pela ADR-0022;
- posicionamento horizontal do bloco dentro do espaço disponível — pendência
  DOC-B004.

---

## Contratos futuros de conteúdo de `dashboard`

Todo contrato `contrato_conteudo_dashboard_<tipo>.md` deve conter:

1. Objetivo do tipo de conteúdo
2. Elemento hospedeiro permitido: `dashboard`
3. Campos próprios do conteúdo
4. Binding no `tela.json`
5. JSON mínimo associado
6. Regras de validação
7. Fora de escopo

Esses contratos são os responsáveis por fechar o que este envelope não fecha.
Nenhum conteúdo real de `dashboard` pode ser declarado no JSON de tela sem
que exista contrato próprio do tipo de conteúdo correspondente.

---

## 8. Critérios de aceite documental

- [ ] O JSON mínimo contém `id`, `tipo`, `titulo`, `conteudo` e
      `regras_exibicao`.
- [ ] `conteudo` declara `tipo` e `binding`, sem fechar conteúdo universal.
- [ ] `dashboard` está posicionado em `corpo.elementos[]`.
- [ ] `dashboard` não é navegável por `[✥]` está declarado.
- [ ] `dashboard` é opcional está declarado.
- [ ] Ausência de `config/dashboard.json` está declarada e fundamentada.
- [ ] A seção "Contratos futuros de conteúdo de `dashboard`" contém o modelo
      com as 7 seções obrigatórias.
- [ ] O JSON mínimo não contradiz `contrato_tela_json.md` nem
      `contrato_composicao_corpo.md`.

---

## 9. Distribuição matricial de nível único (ADR-0025)

A ADR-0025 (2026-07-16) permite que o `dashboard` adote a capacidade de
distribuição matricial configurável de nível único mediante declaração explícita
no seu JSON em `corpo.elementos[]`.

### 9.1 Localização do campo

O campo `distribuicao_matricial` é declarado no nível do elemento `dashboard`,
ao lado dos demais campos do envelope:

```json
{
  "id": "dashboard_principal",
  "tipo": "dashboard",
  "titulo": "Resumo",
  "conteudo": { "tipo": "placeholder", "binding": null },
  "regras_exibicao": {},
  "distribuicao_matricial": {
    "formacao": {
      "politica": "preferencia_colunas",
      "colunas": { "minimo": 2, "maximo": 4 },
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
      "margem_esquerda":  { "minimo": 2 },
      "margem_direita":   { "minimo": 2 },
      "vao_horizontal":   { "minimo": 2 },
      "vao_vertical":     { "minimo": 1 }
    },
    "distribuicao_horizontal": { "politica": "centro" },
    "distribuicao_vertical":   { "politica": "inicio" },
    "ordem_expansao": {
      "horizontal": "uniforme_margens_e_vaos",
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

### 9.2 Vocabulário de campos

| Campo | Tipo | Obrigatório quando | Valores |
|---|---|---|---|
| `formacao.politica` | string | sempre | `"preferencia_linhas"`, `"preferencia_colunas"`, `"matriz_fixa"` |
| `formacao.linhas.minimo` | int ≥ 1 | opcional | só para políticas responsivas |
| `formacao.linhas.maximo` | int ≥ minimo | opcional | só para políticas responsivas |
| `formacao.linhas.fixo` | int ≥ 1 | `politica == "matriz_fixa"` | inválido nas demais políticas |
| `formacao.colunas.minimo` | int ≥ 1 | opcional | só para políticas responsivas |
| `formacao.colunas.maximo` | int ≥ minimo | opcional | só para políticas responsivas |
| `formacao.colunas.fixo` | int ≥ 1 | `politica == "matriz_fixa"` | inválido nas demais políticas |
| `ordem` | string | sempre | `"por_linha"`, `"por_coluna"` |
| `dimensionamento.colunas.politica` | string | sempre | `"maior_da_coluna"`, `"uniforme"`, `"minimo_fixo"` |
| `dimensionamento.colunas.minimo` | int ≥ 0 | `politica == "minimo_fixo"` | — |
| `dimensionamento.linhas.politica` | string | sempre | `"maior_da_linha"`, `"uniforme"`, `"minimo_fixo"` |
| `dimensionamento.linhas.minimo` | int ≥ 0 | `politica == "minimo_fixo"` | — |
| `espacamento.margem_superior` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `espacamento.margem_inferior` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `espacamento.margem_esquerda` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `espacamento.margem_direita` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `espacamento.vao_horizontal` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `espacamento.vao_vertical` | `{minimo, maximo?}` | sempre | int ≥ 0 |
| `distribuicao_horizontal.politica` | string | sempre | `"inicio"`, `"centro"`, `"fim"`, `"entre_participantes"`, `"uniforme"`, `"margens_limitadas"` |
| `distribuicao_vertical.politica` | string | sempre | `"inicio"`, `"centro"`, `"fim"`, `"entre_linhas"`, `"uniforme"`, `"margens_limitadas"` |
| `ordem_expansao.horizontal` | string | sempre | `"margens_primeiro_depois_vaos"`, `"uniforme_margens_e_vaos"`, `"vaos_primeiro_depois_margens"` |
| `ordem_expansao.vertical` | string | sempre | `"margens_primeiro_depois_vaos"`, `"uniforme_margens_e_vaos"`, `"vaos_primeiro_depois_margens"` |
| `politica_resto.horizontal` | string | sempre | `"ao_primeiro"`, `"ao_ultimo"` |
| `politica_resto.vertical` | string | sempre | `"ao_primeiro"`, `"ao_ultimo"` |
| `alinhamento_interno.horizontal` | string | sempre | `"inicio"`, `"centro"`, `"fim"` |
| `alinhamento_interno.vertical` | string | sempre | `"topo"`, `"centro"`, `"base"` |

Campos desconhecidos dentro de `distribuicao_matricial` são rejeitados por
validação controlada. Não há defaults implícitos: todos os campos marcados como
"sempre" obrigatórios devem ser declarados quando `distribuicao_matricial` é
presente.

### 9.2.1 Tratamento quando participante excede a dimensão `minimo_fixo` (DEC-APP-0025-01)

Quando `dimensionamento.colunas.politica` ou `dimensionamento.linhas.politica`
for `"minimo_fixo"` e um participante exigir dimensão superior ao valor
declarado em `dimensionamento.*.minimo`, aplicam-se as seguintes regras:

- A dimensão externa declarada **não cresce automaticamente** por exigência
  interna do participante.
- A formação externa **não se torna inválida** exclusivamente por essa
  exigência interna.
- O participante **trata internamente seu conteúdo** dentro da área recebida.
- Aplicam-se as autoridades ativas de organização interna do participante:
  ADR-0025 seções 7 e 8 (o participante é tratado como unidade única no nível
  externo; a distribuição interna de `B` é responsabilidade própria de `B`);
  `contrato_composicao_corpo.md` seção 11.1 (separação de responsabilidades
  entre composição hierárquica, distribuição de área e distribuição interna de
  participantes); e o contrato específico do elemento participante.
- A distribuição externa **não reorganiza, não achata e não interpreta
  diretamente os descendentes** do participante.
- A responsabilidade pelo conteúdo interno permanece no participante e no
  contrato de seu conteúdo.

Este contrato **não introduz** truncamento, quebra, rolagem, paginação,
propagação de fallback, redução de mínimos ou crescimento externo automático
como resposta a essa condição.

A área externa ainda pode receber espaço excedente por sua própria política de
distribuição (`distribuicao_horizontal`, `distribuicao_vertical`,
`ordem_expansao`). Essa ampliação decorre da política de distribuição externa,
não da exigência interna do participante.

O literal `"minimo_fixo"` permanece semanticamente coerente com essa regra:
ele fixa o requisito externo declarado sem transferir para o nível externo a
exigência dimensional do conteúdo interno do participante. O mínimo é externo,
fixo e inviolável; a organização interna é responsabilidade do participante.

### 9.3 Compatibilidade com JSONs existentes

A ausência do campo `distribuicao_matricial` em um JSON de `dashboard` existente
preserva integralmente o comportamento anterior. Não há migração automática, não
há reescrita do JSON e não há default estrutural que reorganize instâncias
existentes.

### 9.4 Fallback

Quando nenhuma formação válida conseguir acomodar todos os participantes e todos
os mínimos, o estado exibido é o `quadro mínimo de terminal pequeno` (ADR-0017,
ADR-0023). Não é criada variante concorrente de estado de fallback.

### 9.5 Pendência de alinhamento horizontal do `dashboard`

A questão pendente de alinhamento horizontal do `dashboard` (seção 11 de
`docs/NOMENCLATURA.md` — centralizado vs. bloco à esquerda com sobra à direita)
não é resolvida por esta aplicação documental. A reconciliação permanece como
tarefa futura explicitamente identificada.
