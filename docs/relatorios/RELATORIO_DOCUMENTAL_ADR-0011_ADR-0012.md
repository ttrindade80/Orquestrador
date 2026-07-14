# Relatório documental — ADR-0011 e ADR-0012

## Status

DOCUMENTACAO_ATUALIZADA

## Contexto

O projeto está após o commit `ab48702 feat: adiciona acesso demonstravel ao
grupo minimo`. Um levantamento prévio
(`docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`)
pesquisou dois assuntos conjuntos: (a) terminologia de arranjo do corpo e
(b) origem dos chips da `barra_de_menus` do Orquestrador.

A decisão gerencial foi criar **duas ADRs separadas**, pois são relacionadas
pelo princípio declarativo, mas afetam módulos diferentes:

- **ADR-0011** — Terminologia de arranjo (`vertical`/`horizontal`).
- **ADR-0012** — `barra_de_menus` declarativa por tela.

Esta tarefa é estritamente documental e normativa. Não altera código, testes,
JSONs de produção, handoffs nem o levantamento. Não cria handoff de
implementação. Não faz commit.

## ADRs criadas

| Arquivo | Conteúdo normativo |
|---|---|
| `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md` | Fixa `vertical`/`horizontal` como terminologia final de `corpo.arranjo`; `sobreposto`/`lado_a_lado` viram aliases transicionais; `empilhado` permanece histórico; H-0014+ usam a nova terminologia; não implementa migração |
| `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` | `barra_de_menus` declarativa por tela; Orquestrador não declara todos os chips canônicos por padrão; renderer/loader/modelo/demo não inventam chips; testes validam chips declarados; não remove chips agora |

## Documentos atualizados

| Arquivo | Alteração mínima realizada |
|---|---|
| `docs/adr/INDICE_ADR.md` | Adicionadas as linhas de ADR-0011 e ADR-0012 à tabela de decisões registradas |
| `docs/NOMENCLATURA.md` | Seção 1.4: `vertical`/`horizontal` como terminologia final, `sobreposto`/`lado_a_lado` como aliases transicionais; seção 3 (linha de arranjo): valores finais `vertical`/`horizontal`; seção 5: nota de política declarativa por tela (ADR-0012); seção 10: terminologia atualizada; `atualizado_em` → 2026-07-08 |
| `docs/contratos/contrato_composicao_corpo.md` | Frontmatter: ADR-0011 em `adrs_aplicadas`; seção 4.2: `vertical`/`horizontal` como valores normativos finais, aliases transicionais registrados; seção 5.6 (Camada 1 e distribuição): terminologia final; seção 8 (critério de validação "modo horizontal"): atualizado; seção 9 (pendências): desvinculado de H-0011A–D, apontando para H-0014+ |
| `docs/contratos/contrato_tela_json.md` | Seção 8: nota de que a sequência H-0011A–D é histórica e H-0014+ não usa letras; seção 9: `vertical`/`horizontal` como valores finais de arranjo, aliases transicionais registrados |
| `docs/contratos/contrato_barra_de_menus.md` | Frontmatter: ADR-0012 em `adrs_aplicadas`; seção 4 (Regra fundamental): política declarativa por tela — barra não contém todos os chips canônicos por padrão, Orquestrador não precisa declarar todos, renderer não inventa chips, testes esperam chips declarados pela tela |
| `docs/contratos/contrato_json_tela_minima.md` | Frontmatter: ADR-0011 em `adrs_aplicadas`; seção 4.1 (exemplo de JSON): `arranjo: "vertical"` + nota de terminologia final; seção 5.1 (tabela): valores finais `vertical`/`horizontal`, aliases transicionais registrados |

### Documento avaliado e mantido inalterado

Nenhum documento contrato/ADR foi mantido inalterado por conter referência
operacional futura a H-0011A. O caso de `contrato_json_dashboard.md`, que
permanecera inalterado na rodada pós-auditoria inicial por estar fora da
lista de arquivos alteráveis naquele ciclo, foi corrigido na rodada
pós-reauditoria (ver seção "Correções pós-reauditoria" abaixo).

## Decisões registradas

### ADR-0011 — Terminologia de arranjo

1. Nomes finais de arranjo passam a ser `vertical` e `horizontal`.
2. `vertical` substitui os usos conceituais de `sobreposto` e `empilhado`.
3. `horizontal` substitui `lado_a_lado`.
4. `sobreposto` e `lado_a_lado` permanecem como aliases transicionais até
   migração específica.
5. Novos handoffs usam `vertical` e `horizontal`.
6. Novos JSONs de tela usam `vertical` e `horizontal`, salvo compatibilidade
   transicional explicitada.
7. Referências históricas a H-0011A–D podem permanecer como histórico, mas
   não orientam novos ciclos.
8. A ADR não implementa migração em código, JSON ou testes.
9. Disambiguação obrigatória: `corpo.arranjo`, `barra_de_menus.distribuicao`
   e `posicao_dashboard` são campos distintos e não colapsam.

### ADR-0012 — barra_de_menus declarativa por tela

1. A `barra_de_menus` é declarativa por tela.
2. O Orquestrador não declara todos os chips canônicos por padrão.
3. Cada tela declara apenas os chips aplicáveis ao seu estado/capacidade atual.
4. Renderer, loader, modelo e demo não geram chips canônicos por conta própria.
5. Testes validam os chips declarados no JSON da tela, não um conjunto global
   obrigatório.
6. Chip canônico existir não significa que deve aparecer em toda tela.
7. Chips condicionais só presentes quando a capacidade existir ou for
   aplicável.
8. Capacidade não implementada → chip não declarado apenas por ser canônico.
9. Remover chips extras do Orquestrador, com suporte declarativo já existente,
   é alteração declarativa em JSON e pode prescindir de handoff próprio se não
   exigir código novo.
10. A ADR não remove chips agora e não altera JSON.

Achado do levantamento incorporado à ADR-0012: os chips extras atuais do
Orquestrador vêm de `config/telas/orquestrador.json`; renderer, modelo, loader
e demo não inventam esses chips.

## Fora de escopo preservado

- **Código não alterado**: `tela/` intacto.
- **JSONs não alterados**: `config/` intacto.
- **Testes não alterados**: nenhum arquivo de teste tocado.
- **Handoffs não criados nem alterados**: `docs/handoff/` intacto; em
  particular, **H-0014 não foi criado**.
- **Levantamento não alterado**:
  `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
  permanece somente leitura (era arquivo não rastreado pré-existente).
- **ADR-0010 não alterada**: suas referências históricas a `lado_a_lado` e à
  sequência H-0011A–D permanecem como registro histórico.
- **`contrato_processo_desenvolvimento.md` não alterado**.
- **Divergência `dashboard.campos[]` vs `conteudo`/`regras_exibicao`** não
  resolvida (fora de escopo explícito).
- **Nenhum commit realizado**.

## Pendências futuras

- Migração de JSONs/código/testes para `vertical`/`horizontal` (handoff com
  prazo de remoção dos aliases transicionais `sobreposto`/`lado_a_lado`).
- Eventual remoção declarativa de chips extras do Orquestrador em
  `config/telas/orquestrador.json`, com atualização concomitante dos testes
  literais que cristalizam a saída atual.
- Harmonização futura `dashboard.campos[]` vs `conteudo`/`regras_exibicao`
  (fora de escopo desta tarefa).

## Verificações

Comandos executados para confirmar o escopo documental:

```text
$ git status --short
 M scripts/docs/NOMENCLATURA.md
 M scripts/docs/adr/INDICE_ADR.md
 M scripts/docs/contratos/contrato_barra_de_menus.md
 M scripts/docs/contratos/contrato_composicao_corpo.md
 M scripts/docs/contratos/contrato_json_tela_minima.md
 M scripts/docs/contratos/contrato_tela_json.md
?? scripts/docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
?? scripts/docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
?? scripts/docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md

$ git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 20 ++++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  2 +
 scripts/docs/contratos/contrato_barra_de_menus.md  | 13 +++++++
 .../docs/contratos/contrato_composicao_corpo.md    | 43 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    | 10 ++++-
 scripts/docs/contratos/contrato_tela_json.md       | 12 ++++++
 6 files changed, 79 insertions(+), 21 deletions(-)
```

Confirmação de preservação de escopo:

- Nenhuma alteração em `config/` (sem `config/...` em `git status`/`git diff`).
- Nenhuma alteração em `tela/` (sem `tela/...` em `git status`/`git diff`).
- Nenhuma alteração em `docs/handoff/`.
- O arquivo `LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
  aparece como `??` (não rastreado) por ser pré-existente a esta tarefa; não
  foi criado nem modificado aqui.

Nota: o relatório `RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md` (este arquivo)
passa a constar como não rastreado após sua criação, junto aos dois arquivos
de ADR criados.

## Resultado

Documentação normativa atualizada. ADR-0011 e ADR-0012 aceitas e registradas
no índice. Apenas arquivos de `docs/` foram criados/alterados. Código, JSONs,
testes e handoffs permanecem intactos. Nenhum commit realizado.

## Correções pós-auditoria

A auditoria Codex inicial retornou QA_REJECTED com dois achados bloqueantes.

Correções aplicadas:

1. Removidas contradições normativas sobre chips canônicos sempre presentes.
   A documentação agora distingue catálogo canônico de presença declarada por tela.

2. Removidas referências operacionais residuais a H-0011A-D em contratos ativos.
   Referências futuras agora usam linguagem neutra de handoff/ciclo futuro.

### Detalhamento das correções

**Achado 1 — chips canônicos sempre presentes:**

- `docs/NOMENCLATURA.md` seção 5.1: a coluna "Presença (existência)" de
  `[Esc]`, `[⏎]` e `[?]` deixou de afirmar "sempre"; agora registra
  "declarativa por tela" e preserva apenas o invariantes de posição
  (primeiro/último) quando o chip está presente.
- `docs/contratos/contrato_barra_de_menus.md` seção 8.2: reformulada de
  "Chips canônicos de existência sempre presente" para "Chips canônicos de
  semântica fixa", registrando que "canônico" significa nome/semântica
  reconhecida pelo sistema, não presença obrigatória em toda tela (ADR-0012).
- `docs/contratos/contrato_barra_de_menus.md` seção 9: `[Esc]` deixou de
  afirmar "sempre existe"; agora é "quando declarado na instância".
- `docs/contratos/contrato_barra_de_menus.md` seção 20 (critérios de
  validação): o critério de `[?]` passou a "quando declarado, é o último chip
  da instância", sem afirmar existência em toda instância.

**Achado 2 — referências operacionais a H-0011A-D:**

- `docs/NOMENCLATURA.md` (2 ocorrências): "honrados por compatibilidade em
  H-0011A" → "honrados por compatibilidade em handoff futuro de migração".
- `docs/contratos/contrato_composicao_corpo.md` (5 ocorrências operacionais):
  substituídas por "handoff futuro de migração"; mantida apenas a declaração
  histórica explícita de que referências a H-0011A–D não orientam novos ciclos.
- `docs/contratos/contrato_json_tela_minima.md` (2 ocorrências):
  substituídas por linguagem neutra de handoff futuro de migração.
- `docs/contratos/contrato_tela_json.md` seção 8: a sequência H-0011A–D,
  antes apresentada como roteiro incremental ativo, foi reenquadrada como
  plano histórico cancelado; as capacidades futuras permanecem listadas sem
  rótulos H-0011A–D e sem orientar novos ciclos.

### Fora do escopo destas correções (resíduos aceitáveis)

- `docs/adr/ADR-0011` mantém menções a H-0011A–D estritamente como histórico,
  com afirmação explícita de que não orientam novos ciclos — permitido pelo
  critério (referência histórica em ADR aceita).
- `docs/adr/ADR-0010` (não alterada) mantém suas referências históricas.
- Divergência `dashboard.campos[]` vs `conteudo`/`regras_exibicao` segue fora
  de escopo explícito, conforme registro anterior.

## Correções pós-reauditoria

A reauditoria Codex (foco no bloqueio restante) retornou QA_REJECTED com um
único achado bloqueante: o contrato ativo
`docs/contratos/contrato_json_dashboard.md` ainda tratava H-0011A como marco
operacional futuro, em três pontos. H-0011 foi cancelado e H-0011A foi
removido como handoff ativo, de modo que referências a H-0011A-D não podem
orientar novos ciclos.

Correções aplicadas em `docs/contratos/contrato_json_dashboard.md`:

1. Seção 4 (Observações sobre o envelope mínimo), linhas 104-105:
   "honrados por compatibilidade em H-0011A. A migração/descarte do campo
   ocorrerá em handoff específico após H-0011A" → "honrados por
   compatibilidade em ciclo futuro de migração. A migração/descarte do
   campo ocorrerá em handoff numerado posterior".

2. Seção 5 (tabela de Campos obrigatórios), linha 120:
   "honrados por compatibilidade em H-0011A" → "honrados por compatibilidade
   em handoff futuro de migração".

3. Seção 6, regra V-7, linhas 156-158:
   "honrados por compatibilidade em H-0011A; a migração/descarte ocorrerá
   em handoff específico após H-0011A" → "honrados por compatibilidade em
   handoff futuro de migração; a migração/descarte ocorrerá em handoff
   numerado posterior", acrescida da nota histórica explícita de que
   H-0011 foi cancelado e H-0011A foi removido como handoff ativo, e que
   referências a essa sequência não orientam novos ciclos.

As três ocorrências bloqueantes (marco operacional futuro) foram
neutralizadas. A menção residual a H-0011A agora é apenas a declaração
histórica de cancelamento — ACEITÁVEL pelo critério de referência
histórica/cancelada/não orientadora.

## Limpeza final de resíduos textuais

Após a reauditoria final aprovar com notas, foram removidas menções explícitas residuais à sequência cancelada com letras nos documentos normativos ativos e na ADR-0011. A documentação passa a usar linguagem neutra como "sequência histórica cancelada" e "handoff futuro específico".
