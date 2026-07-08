---
name: IMP-DOC-ADR-0010-POS_AUDITORIA
description: Relatório de implementação documental pós-auditoria Codex — correções cirúrgicas que tratam os bloqueios B-1 a B-3 identificados na auditoria RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
metadata:
  type: relatorio_implementacao_documental
  status: DOCUMENTATION_COMPLETED
  data: 2026-07-08
  adr_referencia: docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
  relatorio_auditoria: docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
  superado_por: este arquivo
---

# Relatório de Implementação Documental Pós-Auditoria — ADR-0010

## Status

DOCUMENTATION_COMPLETED

---

## Origem

A auditoria Codex (`RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md`)
finalizou com `DOCUMENTATION_BLOCKED` e `ARCHITECTURE_REVIEW_REQUIRED`.

Três bloqueios normativos ativos foram identificados como pendentes após a
rodada documental registrada em
`IMP-DOC-composicao-hierarquica-corpo-dashboard.md`:

- **B-1**: `docs/NOMENCLATURA.md` seção 1.4 ainda declarava `dashboard` como
  "eixo próprio" que `tiling` "nunca decide".
- **B-2**: `docs/contratos/contrato_json_tela_minima.md` ainda declarava que
  `arranjo` não decide `dashboard` e remetia a `posicao_dashboard` como campo
  normativo ativo.
- **B-3**: `docs/contratos/contrato_json_dashboard.md` ainda tratava
  `posicao_dashboard` como regra ativa independente de `arranjo` e `tiling`
  (texto, tabela e regra V-7).

O bloqueio não exigia nova decisão arquitetural. A decisão estava dada pela
ADR-0010: `dashboard` é elemento funcional do corpo e segue o padrão geral
de composição. A correção necessária era apenas documental.

---

## Bloqueios tratados

| Bloqueio | Arquivo | Tratamento |
|---|---|---|
| B-1 | `docs/NOMENCLATURA.md` seção 1.4 | Texto "eixo próprio" e "nunca decide" removidos; substituído por linguagem alinhada à ADR-0010 com referência explícita à descontinuação de `posicao_dashboard` |
| B-2 | `docs/contratos/contrato_json_tela_minima.md` seções 4.1 e 5.1 | Regra ativa de separação entre `arranjo` e `dashboard` removida; substituída por composição geral; `posicao_dashboard` marcado como campo descontinuado/transicional |
| B-3 | `docs/contratos/contrato_json_dashboard.md` — texto seção 4, tabela seção 5, V-7 | Texto normativo de independência de `arranjo`/`tiling` removido; campo marcado como transicional; V-7 reescrita alinhada à ADR-0010 |

---

## Arquivos lidos

```text
docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
```

Todos os arquivos existem e foram lidos com sucesso. Nenhum arquivo ausente
impediu a tarefa.

---

## Arquivos alterados

```text
docs/NOMENCLATURA.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
```

---

## Arquivos preservados (sem alteração nesta tarefa)

```text
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md   — ADR aprovada; sem contradição
docs/adr/INDICE_ADR.md                                        — já atualizado na rodada anterior
docs/contratos/contrato_composicao_corpo.md                   — auditoria classificou como aprovado
docs/contratos/contrato_tela_json.md                          — auditoria classificou como aprovado
docs/contratos/contrato_processo_desenvolvimento.md            — auditoria classificou como aprovado
docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md — não apagado
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md — preservado (ver seção abaixo)
```

---

## Correções em NOMENCLATURA.md

**Seção 1.4 — Preferência de tiling (default)**

Texto anterior (bloqueante):
```
**Escopo**: aplica-se apenas a arranjo de 2+ corpos tipo `console`/`lancador`.
Nunca decide posição do objeto `dashboard` (esse é eixo próprio, ver seção 3).
```

Texto corrigido:
```
**Escopo**: aplica-se ao arranjo de elementos funcionais do corpo —
`console`, `lancador` e `dashboard` seguem o mecanismo geral de composição
declarativa do `corpo` (ADR-0010, 2026-07-08). A posição do `dashboard` não
é eixo separado externo ao mecanismo de composição; é controlada pela
estrutura declarativa do `corpo`. Ver seção 3 para a tabela de eixos e
seção 10 para tiling. O campo `posicao_dashboard` está descontinuado como
eixo independente (ADR-0010); JSONs existentes com esse campo podem ser
honrados por compatibilidade em H-0011A.
```

As seções 3 e 10 já estavam alinhadas à ADR-0010 pela rodada anterior e não
foram alteradas.

---

## Correções em contrato_json_tela_minima.md

**Seção 4.1 — Exemplo com arranjo explícito**

Texto anterior (bloqueante): declarava que `arranjo` não decide `dashboard`,
determinado por `posicao_dashboard`, remetendo às seções 4.2 e 4.3 do
`contrato_composicao_corpo.md` que já haviam sido atualizadas para contradizer
essa afirmação.

Texto corrigido: `arranjo` é relevante para 2+ elementos funcionais do corpo
(`console`, `lancador`, `dashboard`); todos seguem o mecanismo geral de
composição declarativa (ADR-0010); `posicao_dashboard` descontinuado como
eixo independente; compatibilidade transicional em H-0011A.

**Seção 5.1 — Campo opcional `corpo.arranjo`**

Texto anterior (bloqueante — duas linhas):
- `corpo.arranjo` relevante apenas para `console`/`lancador`
- `corpo.arranjo` **não** decide posição do `dashboard`; independente de
  `arranjo` ou `tiling`

Texto corrigido: `corpo.arranjo` relevante para 2+ elementos funcionais;
composição do `dashboard` segue mecanismo geral (ADR-0010); `posicao_dashboard`
descontinuado como eixo independente; compatibilidade transicional em H-0011A.

**Frontmatter:**

ADR-0010 adicionada em `adrs_aplicadas`.

---

## Correções em contrato_json_dashboard.md

**Frontmatter:**

ADR-0010 adicionada em `adrs_aplicadas`.

**Seção 4 — Observações sobre o envelope mínimo**

Texto anterior (bloqueante): "`regras_exibicao.posicao_dashboard` declara a
posição relativa no corpo: `"vertical"` (abaixo) ou `"horizontal"` (ao lado)."

Texto corrigido: campo marcado como **transicional — superado pela ADR-0010**;
posição do `dashboard` controlada pela estrutura declarativa geral do `corpo`;
não é eixo independente de `arranjo` nem de `tiling`; compatibilidade em
H-0011A; migração ocorrerá em handoff específico.

O JSON de exemplo na seção 4 foi preservado (mantém `posicao_dashboard`
para rastreabilidade de JSONs existentes); a nota circundante deixa explícito
o caráter transicional do campo.

**Seção 5 — Tabela de campos obrigatórios, linha `posicao_dashboard`**

Texto anterior (bloqueante): "Posição do elemento no corpo — independente de
`arranjo` e `tiling`."

Texto corrigido: campo marcado como `string (transicional)` com descrição
"**Campo descontinuado como eixo independente (ADR-0010)**"; referência a
compatibilidade em H-0011A; "Não é eixo separado de `arranjo` nem de
`tiling`."

**V-7 — Regra de validação**

Texto anterior (bloqueante): "`posicao_dashboard` não é afetada por `arranjo`
nem por `tiling`." — afirmava independência como regra ativa.

Texto corrigido: "Posição do `dashboard` é controlada pela composição geral
do corpo (ADR-0010)." — posição definida pela estrutura declarativa do
`corpo`; `posicao_dashboard` descontinuado como eixo independente; compatibilidade
em H-0011A; migração em handoff específico.

---

## Tratamento do relatório IMP-DOC anterior

`docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md` foi
preservado intacto.

Opção escolhida: **preservar o arquivo e registrar a superação neste relatório
complementar** — é a opção menos invasiva conforme instrução.

Justificativa:
- O relatório original registra corretamente o que foi feito na rodada anterior.
- A auditoria Codex detectou que o relatório reportou `DOCUMENTATION_COMPLETED`
  sem registrar a busca textual ampla nem as ocorrências remanescentes nos
  contratos JSON incrementais (B-4 da auditoria).
- Alterar o relatório original falsificaria o histórico documental.
- Este relatório complementar é o artefato correto para registrar a
  superação: o status original `DOCUMENTATION_COMPLETED` foi superado pelo
  bloqueio detectado pela auditoria Codex; a correção desta tarefa resolve os
  bloqueios e restabelece o estado de documentação completa.

---

## Buscas de contradições remanescentes

Comando executado após as correções:

```bash
grep -R "posicao_dashboard\|posição do dashboard\|Posição do dashboard\|dashboard.*eixo\|eixo.*dashboard\|dashboard.*não.*afetado.*tiling\|tiling.*dashboard" docs/NOMENCLATURA.md docs/contratos docs/adr -n
```

Classificação de todas as ocorrências remanescentes:

| Arquivo | Linha | Classificação | Justificativa |
|---|---|---|---|
| `contrato_json_dashboard.md` | 89 | histórico/rastreabilidade aceitável | JSON de exemplo preservado para compatibilidade; texto circundante marca como campo transicional |
| `contrato_json_dashboard.md` | 99 | regra ativa coerente | Agora diz "campo transicional — superado pela ADR-0010" |
| `contrato_json_dashboard.md` | 102 | regra ativa coerente | "não é eixo independente de `arranjo` nem de `tiling`" — correto |
| `contrato_json_dashboard.md` | 120 | regra ativa coerente | Tabela: "Campo descontinuado como eixo independente (ADR-0010)" |
| `contrato_json_dashboard.md` | 154 | regra ativa coerente | V-7 reescrita: campo descontinuado como eixo independente |
| `contrato_json_tela_minima.md` | 122 | regra ativa coerente | Seção 4.1: campo descontinuado como eixo independente |
| `contrato_json_tela_minima.md` | 156 | regra ativa coerente | Seção 5.1: campo descontinuado como eixo independente |
| `ADR-0010-composicao-hierarquica-corpo-dashboard.md` | 3 | histórico/rastreabilidade aceitável | Frontmatter da ADR descrevendo a mudança |
| `ADR-0010-composicao-hierarquica-corpo-dashboard.md` | 37 | histórico/rastreabilidade aceitável | Seção de contexto da ADR descrevendo o modelo antigo |
| `ADR-0010-composicao-hierarquica-corpo-dashboard.md` | 41, 95, 97, 101 | regra ativa coerente | Decisão 4 da ADR: campo descontinuado |
| `ADR-0010-composicao-hierarquica-corpo-dashboard.md` | 176, 179, 197, 221, 231 | histórico/rastreabilidade aceitável | Tabela de consequências e alternativas da ADR |
| `ADR-0006-renomeacao-console-dashboard.md` | 144 | histórico/rastreabilidade aceitável | ADR antiga lista tarefas de renomeação; não decide posicionamento atual |
| `contrato_composicao_corpo.md` | 128–129, 149–157, 267, 359, 425, 493–494, 541–542 | regra ativa coerente | Auditoria Codex classificou este contrato como aprovado |
| `NOMENCLATURA.md` | 142 | regra ativa coerente | Seção 1.4 agora corrigida: campo descontinuado como eixo independente |
| `NOMENCLATURA.md` | 284 | regra ativa coerente | Seção 3 já estava correta (rodada anterior) |
| `NOMENCLATURA.md` | 884 | regra ativa coerente | Seção 10 já estava correta (rodada anterior) |

**Nenhuma contradição ativa remanescente.**

---

## Verificações executadas

### Antes das correções

```bash
git status --short
```

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
```

### Após as correções

```bash
git status --short
```

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
?? docs/relatorios/IMP-DOC-ADR-0010-POS_AUDITORIA.md
```

Novos arquivos modificados nesta tarefa: `contrato_json_dashboard.md` e
`contrato_json_tela_minima.md`. Este relatório adicionado como não rastreado.

```bash
git diff --stat
```

```text
 scripts/docs/NOMENCLATURA.md                       | 21 ++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 scripts/docs/contratos/contrato_composicao_corpo.md    | 81 ++++++++++++------
 scripts/docs/contratos/contrato_json_dashboard.md  | 24 +++++--
 scripts/docs/contratos/contrato_json_tela_minima.md    | 21 ++++--
 scripts/docs/contratos/contrato_processo_desenvolvimento.md | 47 +++++++++++-
 scripts/docs/contratos/contrato_tela_json.md       | 21 +++++-
 7 files changed, 164 insertions(+), 52 deletions(-)
```

### Verificação de escopo negativo

```bash
git status --short tela/ config/ tests/
git diff --name-only -- tela/ config/ tests/
```

Ambos retornaram vazio.

Nenhum arquivo em `tela/`, `config/` ou `tests/` foi alterado. Nenhum JSON
de configuração foi alterado.

---

## Estado final do git

- 7 arquivos documentais modificados (M)
- 5 arquivos não rastreados pré-existentes (??): ADR-0010, H-0011,
  IMP-DOC anterior, relatório de auditoria, relatório de auditoria H-0011
- 1 novo arquivo não rastreado criado nesta tarefa: este relatório

Nenhum commit realizado.

---

## Observações para auditoria Codex

1. **Bloqueios B-1, B-2 e B-3 tratados cirurgicamente**: todas as ocorrências
   normativas ativas de `dashboard` como "eixo próprio" ou `posicao_dashboard`
   como "independente de `arranjo` e `tiling`" foram removidas ou reescritas.
   Nenhuma contradição ativa remanescente foi identificada.

2. **Campo `posicao_dashboard` preservado como transicional**: o campo
   permanece rastreável nos contratos mas marcado explicitamente como
   descontinuado pela ADR-0010. JSONs existentes com esse campo podem ser
   honrados por compatibilidade em H-0011A; migração/descarte em handoff
   específico após H-0011A.

3. **IMP-DOC anterior preservado sem alteração**: não foi falsificado nem
   apagado. Sua inadequação (status `DOCUMENTATION_COMPLETED` sem busca
   textual ampla) é registrada como achado histórico, não corrigida
   retroativamente.

4. **Bloqueio B-4 da auditoria** (relatório anterior marcou
   `DOCUMENTATION_COMPLETED` sem detectar as contradições remanescentes):
   este ponto é registrado e tratado estruturalmente pela existência deste
   relatório complementar, que documenta a busca textual obrigatória e a
   classificação de todas as ocorrências.

5. **Sequência H-0011A–D permanece liberada documentalmente**: com as
   correções desta tarefa, a base documental está alinhada à ADR-0010 em
   todos os contratos ativos. H-0011A pode ser iniciado a partir desta base.
