---
name: contrato-json-tela-minima
description: Especifica o envelope JSON mínimo de uma tela concreta — campos obrigatórios, caminho canônico e restrições declarativas do arquivo tela.json
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_tela_json.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
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
    "arranjo": "sobreposto",
    "elementos": []
  },
  "barra_de_menus": {
    "chips": []
  }
}
```

`arranjo` declarado fixa o layout para aquela tela; o renderer usa esse valor
e ignora o campo `tiling` do estilo ativo. `arranjo` é relevante para 2+
elementos `console`/`lancador` — não decide a posição do `dashboard`, que é
determinada pelo campo `posicao_dashboard` da instância, conforme
`contrato_composicao_corpo.md` seções 4.2 e 4.3.

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
| `corpo.arranjo` | `"sobreposto"` \| `"lado_a_lado"` | Quando declarado, fixa o arranjo para a tela e o renderer ignora `tiling` do estilo ativo. Quando não declarado, o renderer consulta o campo `tiling` do estilo ativo como default — ver `contrato_composicao_corpo.md` seção 5.6. |

Regras complementares:

- `corpo.arranjo` é relevante para 2+ elementos `console`/`lancador` no corpo.
- `corpo.arranjo` **não** decide a posição do `dashboard` — essa é determinada
  pelo campo `posicao_dashboard` da instância, independente de `arranjo` ou
  `tiling`.
- O renderer não inventa arranjo, não cria fallback próprio baseado em largura
  de terminal e não decide composição por condição de ambiente.

---

## 6. Tipos válidos em `corpo.elementos[]`

Cada item de `corpo.elementos[]` deve declarar `tipo` como um dos valores
abaixo. A lista é fechada nesta versão — extensões exigem ADR.

| Tipo | Contrato de referência |
|---|---|
| `console` | `contrato_json_console.md`, `contrato_console.md` |
| `dashboard` | `contrato_json_dashboard.md`, `contrato_composicao_corpo.md` |
| `lancador` | `contrato_json_lancador.md`, `contrato_lancador.md` |

Tipo desconhecido em `corpo.elementos[]` é erro de validação.

---

## 7. Caminho canônico e regra de coincidência de `id`

Conforme ADR-0009, o caminho canônico de qualquer JSON de tela concreta é:

```text
config/telas/<id>.json
```

Regras obrigatórias:

- o diretório `config/telas/` é exclusivo para JSONs de tela;
- o `id` interno declarado no campo `"id"` do JSON deve coincidir com o nome
  base do arquivo em disco;
- o nome do arquivo segue as regras de identificador estável: minúsculo, sem
  acentos, sem espaços, preferencialmente `snake_case`;
- `id` divergente do nome base do arquivo é inconsistência de validação.

Exemplo: tela com `"id": "orquestrador"` deve estar em
`config/telas/orquestrador.json`.

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
- [ ] O caminho canônico `config/telas/<id>.json` está registrado e a regra
      de coincidência de `id` está formalizada.
- [ ] Nenhuma seção deste contrato autoriza estado de runtime no JSON de tela.
- [ ] Nenhuma seção deste contrato autoriza lógica procedural ou comando
      arbitrário no JSON de tela.
