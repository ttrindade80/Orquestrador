---
name: ADR-0011-terminologia-arranjo-vertical-horizontal
description: Terminologia final de arranjo do corpo passa a ser vertical e horizontal; sobreposto e lado_a_lado tornam-se aliases transicionais; empilhado permanece histórico; nao implementa migracao
metadata:
  type: adr
  status: aceita
  data: 2026-07-08
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  handoffs_bloqueados: []
---

# ADR-0011 — Terminologia de arranjo: vertical/horizontal

## Status

`aceita`

## Data

2026-07-08

## Contexto

O levantamento `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
mapeou a terminologia atual de `corpo.arranjo` e constatou:

- **`sobreposto`** é o valor ativo de `corpo.arranjo` nos JSONs de produção
  (`orquestrador`, `destino_minimo`, `stub_b`, `grupo_minimo`) e aparece como
  valor permitido em contratos ativos (`contrato_composicao_corpo.md`,
  `contrato_json_tela_minima.md`, `NOMENCLATURA.md`).
- **`lado_a_lado`** não possui JSON ativo, mas permanece como valor permitido
  em contratos ativos e é rejeitado apenas como `arranjo` de grupo estrutural
  no loader. É também a denominação usada pela ADR-0010 e por ciclos
  históricos cancelados/removidos.
- **`empilhado`** existe apenas como descrição visual histórica em handoff/relatório;
  não é valor contratual, não aparece em JSON nem em código.
- **`vertical`** e **`horizontal`** já existem no sistema, mas em campos distintos:
  `barra_de_menus.distribuicao` (ativo) e o campo descontinuado
  `posicao_dashboard` (transicional, ADR-0010). Não são, hoje, valores de
  `corpo.arranjo`.

Essa dispersão terminológica gera ambiguidade: o mesmo conceito de arranjo
do corpo é nomeado de três formas diferentes (`sobreposto`, `empilhado`,
`lado_a_lado`), e as palavras `vertical`/`horizontal` já circulam no sistema
com outros significados. A decisão gerencial é padronizar a terminologia
**final** de `corpo.arranjo` em `vertical` e `horizontal`, preservando
compatibilidade transicional sem reabrir ciclos cancelados/removidos.

Esta ADR é normativa: define nomes e aliases. Ela **não** implementa migração
em código, JSONs de produção ou testes — essas são pendências futuras.

A separação em duas ADRs (ADR-0011 e ADR-0012) reflete o princípio comum
declarativo, mas isenta módulos: ADR-0011 trata de nomes/valores de arranjo;
ADR-0012 trata da política declarativa da `barra_de_menus`.

---

## Decisão

As declarações abaixo constituem a decisão formal desta ADR.

**1. Os nomes finais de arranjo passam a ser `vertical` e `horizontal`.**

Para `corpo.arranjo`, os valores terminológicos finais são `vertical` e
`horizontal`. Esta é a terminologia que novos contratos, handoffs e JSONs
devem adotar.

**2. `vertical` substitui os usos conceituais de `sobreposto` e `empilhado`.**

Toda referência conceitual ao arranjo "empilhado"/"sobreposto" (elementos do
corpo dispostos um sobre o outro, verticalmente) passa a ser denominada
`vertical`. `sobreposto` e `empilhado` deixam de ser a terminologia final.

**3. `horizontal` substitui `lado_a_lado`.**

Toda referência conceitual ao arranjo "lado a lado" (elementos do corpo
dispostos lado a lado, horizontalmente) passa a ser denominada `horizontal`.
`lado_a_lado` deixa de ser a terminologia final.

**4. `sobreposto` e `lado_a_lado` podem permanecer como aliases transicionais
até migração específica.**

Os termos `sobreposto` e `lado_a_lado` são aceitos como aliases transicionais
de `vertical` e `horizontal`, respectivamente, para preservar compatibilidade
de JSONs legados, contratos ainda não migrados e artefatos históricos usados
como referência. A aceitação dos aliases é temporária: deve haver um ciclo
futuro explícito de migração e um prazo de remoção definido no handoff
correspondente. Aliases não são terminologia final.

**5. Novos handoffs devem usar `vertical` e `horizontal`.**

A partir desta ADR, todo handoff novo (a partir de H-0014) deve usar
`vertical` e `horizontal` como termos de arranjo. Handoffs não devem
introduzir `sobreposto`, `empilhado` nem `lado_a_lado` como terminologia
final em novas regras.

**6. Novos JSONs de tela devem usar `vertical` e `horizontal`, salvo
compatibilidade transicional explicitada.**

Todo novo JSON de tela concreto deve declarar `corpo.arranjo` com `vertical`
ou `horizontal`. O uso de `sobreposto`/`lado_a_lado` em JSON novo só é
admitido quando explicitamente marcado como compatibilidade transicional e
acompanhado de registro de migração.

**7. Referências históricas à sequência cancelada podem permanecer apenas
como histórico, mas não devem orientar novos ciclos.**

As menções a `lado_a_lado` e à sequência histórica cancelada em ADR-0010 e
em handoffs/relatórios históricos permanecem válidas como registro histórico e
de rastreabilidade. Elas **não** orientam novos ciclos. A partir desta ADR,
o planejamento incremental de composição deve usar `vertical`/`horizontal`
e a numeração sem letras (H-0014, H-0015, …), conforme já estabelecido por
H-0012/H-0013.

**8. Esta ADR não implementa migração em código, JSON ou testes.**

Esta ADR não altera `config/`, `tela/`, nem artefatos de teste. A migração
de JSONs ativos, a eventual aceitação de aliases no loader e a atualização
de testes literais são pendências de handoff futuro. Esta ADR apenas fixa a
terminologia normativa.

### Disambiguação obrigatória de campos

A padronização de `corpo.arranjo` em `vertical`/`horizontal` **não** colapsa
estes campos distintos, que continuam independentes:

| Campo | Significado | Status |
|---|---|---|
| `corpo.arranjo` | Arranjo (vertical/horizontal) dos elementos funcionais do corpo | terminologia final (esta ADR) |
| `barra_de_menus.distribuicao` | Distribuição dos chips na barra (ex.: `horizontal`) | campo ativo, semântica própria |
| `posicao_dashboard` | Campo descontinuado de posicionamento do dashboard (ADR-0010) | transicional, semântica própria |

`corpo.arranjo = "horizontal"` não substitui nem colide com
`barra_de_menus.distribuicao = "horizontal"`; são campos diferentes. O mesmo
vale para `vertical` frente ao `posicao_dashboard` descontinuado.

---

## Consequências

### Obrigatórias

- **Contratos e NOMENCLATURA devem passar a usar `vertical`/`horizontal` como
  termos finais.** Os contratos ativos afetados passam a registrar
  `vertical`/`horizontal` como valores normativos de `corpo.arranjo`.
- **Loader/testes poderão precisar aceitar aliases transicionais em handoff
  futuro.** A migração de JSONs e testes para `vertical`/`horizontal` poderá
  exigir, temporariamente, aceitação de `sobreposto → vertical` e
  `lado_a_lado → horizontal` no loader/normalização. Isso é decisão de
  handoff futuro, não desta ADR.
- **H-0014 e seguintes devem usar `vertical`/`horizontal`.** Novos handoffs
  não devem usar `lado_a_lado`/`sobreposto`/`empilhado` como terminologia
  final em regras novas.
- **`lado_a_lado`/`sobreposto` devem ser marcados como transicionais ou
  históricos quando aparecerem em regra ativa.** Sempre que um contrato ativo
  mencionar esses termos, deve assinalar sua natureza transicional/histórica
  e apontar `vertical`/`horizontal` como terminologia final.

### Artefatos a atualizar nesta tarefa documental

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0011 |
| `docs/NOMENCLATURA.md` | Registrar `vertical`/`horizontal` como terminologia final de arranjo; marcar `sobreposto`, `empilhado` e `lado_a_lado` como transicionais/históricos |
| `docs/contratos/contrato_composicao_corpo.md` | Usar `vertical`/`horizontal` como termos normativos finais; registrar aliases transicionais; preservar compatibilidade histórica sem reabrir a sequência cancelada |
| `docs/contratos/contrato_tela_json.md` | Refletir `vertical`/`horizontal` como valores finais de arranjo; evitar sequência futura com letras |
| `docs/contratos/contrato_json_tela_minima.md` | Atualizar valores ativos de `corpo.arranjo` para `vertical`/`horizontal`, com aliases transicionais registrados |

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `config/` | Migração de JSONs é pendência de handoff futuro |
| `tela/` | Aceitação de aliases e testes é pendência de handoff futuro |
| `docs/handoff/` | Artefatos históricos permanecem; novos handoffs usarão a nova terminologia |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | ADR aceita não é reescrita; suas referências históricas a `lado_a_lado` e à sequência cancelada permanecem como histórico |
| `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md` | Levantamento de pesquisa, somente leitura |

### Pendências derivadas

- Handoff futuro de migração: JSONs ativos (`orquestrador`, `destino_minimo`,
  `stub_b`, `grupo_minimo`) trocando `corpo.arranjo` de `sobreposto` para
  `vertical`, com atualização concomitante de testes literais.
- Decidir, no handoff de migração, se o loader normaliza aliases ou se exige
  troca direta, e definir prazo de remoção dos aliases.
- Revisar `contrato_estilo.md`/`config/estilo.json` caso o campo `tiling`
  também deva migrar seus valores — decisão adiada, não coberta por esta ADR.

---

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR:

- Implementar `corpo.arranjo = "horizontal"` no renderer (execução visual de
  composição horizontal). Continua pendência de handoff de implementação.
- Decidir o conjunto exato de capacidades do grupo estrutural com múltiplos
  elementos — pertence a H-0014 e seguintes.
- Migrar o campo descontinuado `posicao_dashboard` — pendência já registrada
  em ADR-0010.
- Migrar valores de `tiling` em `config/estilo.json`.
- Remover aliases transicionais — pendência de handoff com prazo explícito.

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Manter `sobreposto`/`lado_a_lado` como terminologia final | Perpetua dispersão terminológica (`sobreposto`/`empilhado`/`lado_a_lado`) e ambiguidade com `vertical`/`horizontal` já existentes em outros campos |
| Troca direta sem aliases transicionais | Viável nos JSONs ativos, mas arriscada para artefatos históricos e contratos ainda não migrados; exige unidade de trabalho maior em handoff único |
| Renomear também `barra_de_menus.distribuicao` e `posicao_dashboard` | Escopo excessivo; esses campos têm semântica própria e não são `corpo.arranjo` |
| Criar uma única ADR cobrindo arranjo e `barra_de_menus` | Decisão gerencial: são relacionadas pelo princípio declarativo, mas afetam módulos diferentes — justifica-se ADR-0011 e ADR-0012 separadas |
