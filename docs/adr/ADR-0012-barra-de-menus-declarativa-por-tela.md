---
name: ADR-0012-barra-de-menus-declarativa-por-tela
description: barra_de_menus e declarativa por tela; o Orquestrador nao declara todos os chips canonicos por padrao; renderer/loader/modelo/demo nao inventam chips; testes validam chips declarados no JSON da tela
metadata:
  type: adr
  status: aceita
  data: 2026-07-08
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_tela_json.md
    - docs/NOMENCLATURA.md
  handoffs_bloqueados: []
---

# ADR-0012 — barra_de_menus declarativa por tela

## Status

`aceita`

## Data

2026-07-08

## Contexto

A `barra_de_menus` é a região fixa inferior da tela, modelada como instância
declarada no `tela.json` (ADR-0008). O contrato `contrato_barra_de_menus.md`
já estabelece que a barra é "espelho, nunca fonte de decisão" e que a lista
concreta de chips pertence ao JSON da tela.

O levantamento `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
investigou a origem concreta dos chips atualmente exibidos no Orquestrador e
confirmou:

> Os chips extras atuais do Orquestrador vêm de
> `config/telas/orquestrador.json`. Renderer, modelo, loader e demo **não**
> inventam esses chips.

Especificamente:

- O JSON `config/telas/orquestrador.json` declara 11 chips em
  `barra_de_menus.chips[]`.
- `tela/loader.py` preserva `barra_de_menus` como dict; não adiciona chip.
- `tela/modelo.py` copia `barra_de_menus` do JSON; não adiciona chip.
- `tela/renderizador.py` lê `barra_de_menus.get("chips", [])` e monta cada
  chip como `"[{tecla}] {texto}"`; não gera lista própria.
- `tela/demo.py` interpreta comandos internos e itens do `lancador`; não
  adiciona chip à `barra_de_menus`.
- Os testes atuais cristalizam a saída literal do JSON atual (11 chips),
  mas não existe teste que obrigue o renderer a produzir um conjunto
  canônico global.

Apesar dessa origem já ser declarativa, linguagem contratual como "chips
canônicos de existência sempre presente" pode ser lida como obrigação global
de declarar todos os chips canônicos em toda tela. Essa leitura contraria o
princípio declarativo: uma tela deve declarar apenas os chips aplicáveis ao
seu estado/capacidade atual. A decisão gerencial é formalizar essa política
como ADR para que contratos, handoffs e testes fiquem alinhados.

Esta ADR é normativa. Ela **não** remove chips agora e **não** altera JSONs.

---

## Decisão

As declarações abaixo constituem a decisão formal desta ADR.

**1. A `barra_de_menus` é declarativa por tela.**

A `barra_de_menus` é uma instância declarada no `tela.json` de cada tela. A
presença de cada chip é derivada da declaração daquela tela específica.

**2. O Orquestrador não deve declarar todos os chips canônicos por padrão.**

Nenhuma tela — incluindo o Orquestrador — é obrigada a declarar o conjunto
completo de chips canônicos. "Canônico" define semântica e ordem quando o
chip está presente, não obrigatoriedade de presença em toda tela.

**3. Cada tela declara apenas os chips aplicáveis ao seu estado/capacidade atual.**

A declaração de chips de uma tela reflete as capacidades que aquela tela
efetivamente oferece no ciclo atual.

**4. Renderer, loader, modelo e demo não devem gerar chips canônicos por conta própria.**

Nenhum módulo de código inventa, completa ou injeta chips canônicos além dos
declarados no `tela.json`. O renderer percorre `barra_de_menus.chips[]`
declarado; o loader e o modelo preservam; a demo não adiciona chip à barra.

**5. Testes devem validar os chips declarados no JSON da tela, não um conjunto global obrigatório.**

Testes comparam a saída com os chips efetivamente declarados pela tela. Não
existe conjunto global obrigatório de chips que toda tela deva exibir.

**6. Chip canônico existir no sistema não significa que ele deve aparecer em toda tela.**

A existência de um chip canônico como categoria semântica não obriga sua
presença em toda instância de `barra_de_menus`.

**7. Chips condicionais só devem estar presentes quando a capacidade correspondente existir ou for aplicável à tela.**

Um chip condicional (ex.: `[<][>]`, `[-][+]`, `[#]`, `[⇆]`, `[✥]`, `[␣]`,
`[V]`) só deve ser declarado quando a capacidade correspondente existir ou
for aplicável à tela em questão.

**8. Se uma capacidade não está implementada na tela, seu chip não deve ser declarado apenas por ser canônico.**

A natureza canônica de um chip não basta para justificar sua declaração. Se
a capacidade não existe ou não se aplica à tela, o chip correspondente não
deve ser declarado naquela instância.

**9. Remover chips extras do Orquestrador, quando o suporte declarativo já existe, é alteração declarativa em JSON e pode ser feita sem handoff próprio se não exigir código novo.**

Conforme `contrato_processo_desenvolvimento.md` seção 9, uma alteração
puramente declarativa em JSON — quando o loader, o modelo, o renderer e o
binding já suportam a declaração — não exige handoff próprio. Assim, remover
chips não aplicáveis do `orquestrador.json` pode ser feito como alteração
declarativa, desde que não exija código novo. Se a remoção exigir código,
binding ou teste novo, handoff próprio se aplica.

**10. Esta ADR não remove chips agora e não altera JSON.**

Esta ADR não altera `config/`, `tela/` nem testes. A eventual remoção
declarativa de chips extras do Orquestrador é pendência futura, a ser feita
conforme a decisão do item 9.

### Achado do levantamento incorporado

O levantamento confirmou que os chips extras atuais do Orquestrador vêm de
`config/telas/orquestrador.json`. Renderer, modelo, loader e demo não
inventam esses chips. Portanto, o excesso de chips é primariamente uma
questão de declaração de JSON (e de testes que cristalizam essa saída), não
de renderer. Esta ADR formaliza a política declarativa para alinhar
contratos, handoffs e testes.

---

## Consequências

### Artefatos a atualizar nesta tarefa documental

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0012 |
| `docs/contratos/contrato_barra_de_menus.md` | Deixar claro que a barra é declarada por tela; o renderer não inventa chips canônicos; o Orquestrador não precisa declarar todos os chips canônicos; testes devem esperar os chips declarados pela tela |
| `docs/NOMENCLATURA.md` | Registrar que a `barra_de_menus` é declarativa por tela e não contém todos os chips canônicos por padrão |

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `config/` | Remoção de chips é pendência futura |
| `tela/` | Nenhum código inventa chips; não há alteração de código nesta ADR |
| `docs/handoff/` | Artefatos históricos permanecem |
| `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md` | Levantamento de pesquisa, somente leitura |

### Pendências derivadas

- Remoção declarativa de chips extras do `orquestrador.json`, conforme item 9,
  quando houver decisão sobre quais chips são aplicáveis ao Orquestrador no
  ciclo atual.
- Atualização dos testes literais (`teste_renderizador.py`, `teste_demo.py`,
  `teste_diagnostico.py`) junto com qualquer remoção de chips do JSON, já que
  cristalizam a saída atual.
- Decisão sobre quais chips (ex.: `[Esc]`, `[?]`) permanecem sempre presentes
  por contrato mínimo, versus chips puramente declarativos por tela.

---

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR:

- Decidir exatamente quais chips o Orquestrador deve manter ou remover no
  ciclo atual — pendência de decisão funcional/handoff.
- Criar contrato completo da classe `chip` (DOC-B006).
- Implementar avaliação de `regra_existencia`/`regra_ativo` no renderer.
- Definir conjunto mínimo obrigatório de chips por contrato (ex.: se `[Esc]`
  e `[?]` são sempre obrigatórios).

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Exigir que toda tela declare todos os chips canônicos | Contradiz o princípio declarativo; obriga chips não aplicáveis; gera barra barulhenta e incorreta |
| Fazer o renderer gerar chips canônicos faltantes | Quebra a regra do renderer como executor puro; reintroduz hardcoding; contradiz ADR-0008 |
| Tratar a política como mero ajuste de contrato, sem ADR | A política afeta contratos, handoffs e testes simultaneamente; merece registro como decisão arquitetural aceita |
