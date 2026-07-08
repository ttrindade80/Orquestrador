---
name: IMP-DOC-composicao-hierarquica-corpo-dashboard
description: Relatório de implementação documental — ADR-0010 composição hierárquica do corpo e dashboard como elemento funcional
metadata:
  type: relatorio_implementacao_documental
  status: DOCUMENTATION_COMPLETED
  data: 2026-07-08
  adr_criada: docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
---

# Relatório de Implementação Documental — Composição hierárquica do corpo e dashboard

## Status

DOCUMENTATION_COMPLETED

---

## Objetivo

Criar a base documental que permita reescrever e auditar o H-0011 em ciclo
posterior, corrigindo a modelagem do `dashboard` e registrando a regra de
processo sobre mudanças declarativas em JSON.

O H-0011 foi bloqueado com `ARCHITECTURE_REVIEW_REQUIRED` porque:
1. A documentação tratava `dashboard` como eixo especial externo com campo
   `posicao_dashboard` "nunca afetado por `arranjo` nem por `tiling`".
2. O algoritmo do handoff (`col_w = total_w // 2` sem vãos) contradiz a
   regra contratual de 3 vãos iguais em `lado_a_lado`.
3. O fallback para 3+ elementos com `arranjo = "lado_a_lado"` autorizava
   ignorar o arranjo declarado por quantidade de elementos.

Esta tarefa documental resolve o ponto 1 (modelo do dashboard), prepara a
sequência H-0011A–D para tratar os demais pontos incrementalmente, e
formaliza a regra sobre mudanças declarativas em JSON.

---

## Arquivos lidos

```text
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md

docs/adr/INDICE_ADR.md
docs/adr/ADR-0006-renomeacao-console-dashboard.md
docs/adr/ADR-0007-tela-processamento-composicao.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md

docs/NOMENCLATURA.md
docs/INDICE.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
```

Todos os arquivos existem e foram lidos com sucesso. Nenhum arquivo ausente
impediu a tarefa.

---

## Arquivos criados

```text
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md  (este arquivo)
```

---

## Arquivos alterados

```text
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/NOMENCLATURA.md
```

Arquivos **não alterados** (verificados como desnecessários):

```text
docs/contratos/contrato_console.md     — sem inconsistência com ADR-0010
docs/contratos/contrato_lancador.md    — nenhuma regra do lancador muda
docs/contratos/contrato_barra_de_menus.md — nenhuma regra de chip ou barra muda
docs/contratos/contrato_chip.md        — nenhuma regra de chip muda
docs/INDICE.md                         — o índice de ADRs individuais não é
                                         exaustivo (ADR-0009 já não está lá);
                                         INDICE_ADR.md é o índice canônico
```

---

## ADR criada

**`docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`**

Decisões registradas:

1. `dashboard` segue o padrão geral de composição do corpo (deixa de ser
   eixo especial externo).
2. `console`, `lancador` e `dashboard` são elementos funcionais do corpo.
3. Composição visual pertence à estrutura declarada no `corpo` do `tela.json`.
4. Campo `posicao_dashboard` como eixo separado independente está descontinuado.
5. `corpo` passa a admitir estrutura declarativa hierárquica (incremental).
6. Campos internos de cada elemento continuam responsabilidade da instância.
7. `dashboard` continua passivo e não navegável por `[✥]`.
8. `console` continua o único tipo navegável por `[✥]`.
9. `lancador` continua não navegável por `[✥]`.
10. Regra de 3 vãos iguais para `lado_a_lado` aplica-se universalmente.
11. Sequência incremental H-0011A–D é a prevista próxima.
12. Esta ADR não corrige nem reescreve o handoff H-0011 bloqueado.

---

## Contratos atualizados

### `docs/contratos/contrato_composicao_corpo.md`

- Adicionado ADR-0010 em `rastreabilidade.adrs_aplicadas`.
- Seção 4.3 (`posicao_dashboard`): campo descontinuado como eixo separado;
  linguagem "eixo próprio — nunca afetado" removida; nota de compatibilidade
  para H-0011A adicionada.
- Seção 5.3 (`dashboard`): adicionada nota de que `dashboard` é elemento
  funcional do corpo; compositor não conhece campos internos.
- Seção 5.6 (tiling): removida exclusão explícita de `dashboard`; atualizado
  para refletir que dashboard segue composição geral (ADR-0010).
- R-5: atualizada de "posicao_dashboard é campo da instância, independente do
  tiling" para "Posicionamento de dashboard segue a composição geral do corpo".
- R-9: atualizada de "Tiling e arranjo não afetam o dashboard" para
  "Composição do corpo aplica-se a todos os elementos funcionais".
- Critério de validação sobre `posicao_dashboard` atualizado.
- Seção 9 (pendências): atualizada para refletir que ADR-0010 resolve
  conceitualmente a combinação `lado_a_lado + dashboard`; migração de
  `posicao_dashboard` adicionada como pendência; schema de grupos
  hierárquicos como pendência a ser resolvida nos handoffs H-0011A–D.

### `docs/contratos/contrato_tela_json.md`

- Seção 8 (`corpo`): adicionada nota sobre composição hierárquica (ADR-0010);
  schema pode evoluir para grupos; sequência H-0011A–D documentada;
  declaração de que todos os elementos funcionais seguem composição geral.

### `docs/contratos/contrato_processo_desenvolvimento.md`

- Adicionada Seção 9 "Mudanças declarativas em JSON" com:
  - condições para que mudança não exija handoff próprio (5 condições de
    suporte já existente);
  - lista de exemplos validados (stub_b, f41bd2f);
  - condições que tornam ciclo formal obrigatório;
  - nota de que mudança declarativa pode exigir verificação/commit sem
    virar handoff.
- Seção anterior "9. Exemplos neutros de nomes" renumerada para 10.

### `docs/NOMENCLATURA.md`

- Seção 3, tabela de eixos: linha "Posição do dashboard" atualizada para
  remover "Eixo próprio, não afetado pelo tiling" e referenciar ADR-0010.
- Seção 10, título: "não se aplica ao dashboard" removido do título da seção.
- Seção 10, conteúdo: linha sobre posição do dashboard como "eixo separado —
  nunca decidida por tiling nem pelo arranjo" atualizada para refletir ADR-0010.

### `docs/adr/INDICE_ADR.md`

- Linha de ADR-0010 adicionada à tabela de decisões registradas.

---

## Regra de JSON declarativo registrada

Regra adicionada em `docs/contratos/contrato_processo_desenvolvimento.md`
seção 9:

**Sem handoff próprio quando:**
- schema já suporta a declaração;
- loader/modelo já preserva e valida os campos;
- renderer/binding já interpreta a declaração;
- não há novo comportamento de código;
- não há novo tipo estrutural;
- não há nova ação, navegação, binding ou regra de renderização.

**Ciclo formal obrigatório quando a alteração exigir:**
- novo binding;
- nova validação estrutural ou campo de schema;
- nova regra de renderização;
- nova navegação;
- nova ação;
- novo tipo estrutural;
- mudança de contrato;
- mudança de arquitetura;
- alteração de código.

Exemplos validados registrados: stub_b (f41bd2f).

---

## Itens explicitamente fora de escopo

Não documentados nesta tarefa, conforme instrução do gerente:

```text
foco multi-console com Tab
pop-up de qualquer tipo
execução multi-console
seleção entre múltiplos consoles
realce visual de console ativo
política completa futura de Enter
Orquestrador real completo
execução real de processos
registry novo de telas ou ações
novos tipos de corpo fora de console/lancador/dashboard
handoffs futuros além da sequência H-0011A–D
algoritmo completo de distribuição para 3+ elementos em lado_a_lado
schema detalhado de grupos hierárquicos
especificação de campos que substituem posicao_dashboard
correção do handoff H-0011 bloqueado
auditoria própria deste relatório
commit
```

---

## Verificações executadas

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
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
```

```bash
git diff --stat
```

```text
 scripts/docs/NOMENCLATURA.md                       | 11 +--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 scripts/docs/contratos/contrato_composicao_corpo.md    | 81 ++++++++++++------
 scripts/docs/contratos/contrato_processo_desenvolvimento.md | 47 +++++++++++-
 scripts/docs/contratos/contrato_tela_json.md       | 21 +++++-
 5 files changed, 125 insertions(+), 36 deletions(-)
```

```bash
git diff --name-only
```

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
```

**Verificação de escopo:**

Nenhum arquivo fora do escopo documental foi alterado.

```text
config/     — não alterado ✓
tela/       — não alterado ✓
testes      — não alterados ✓
```

---

## Estado final do git

5 arquivos documentais modificados (M).
2 novos arquivos documentais não rastreados (??):
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md`

2 arquivos não rastreados pré-existentes (não alterados nesta tarefa):
- `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md`

Nenhum commit realizado.

---

## Observações para auditoria Codex

1. **Backward compatibility garantida por H-0011A**: a ADR-0010 estabelece
   que JSONs existentes com `posicao_dashboard` podem ser honrados durante
   H-0011A. O handoff H-0011A deve especificar o tratamento de compatibilidade.

2. **Achados bloqueantes da auditoria H-0011 ainda pendentes de handoff**:
   - Algoritmo `col_w = total_w // 2` sem vãos: será tratado em H-0011B
     quando o layout horizontal for implementado com a regra de 3 vãos.
   - Fallback para 3+ elementos com `lado_a_lado`: será tratado em H-0011D
     (aninhamento de grupos).

3. **Sequência H-0011A–D é o próximo passo**: esta base documental libera
   a criação do handoff H-0011A. O handoff H-0011A deve referenciar ADR-0010
   e descrever o layout hierárquico vertical compatível sem quebrar JSONs
   existentes.

4. **Regra de JSON declarativo formalizada**: a regra adicionada ao
   contrato de processo (seção 9) formaliza o que a validação com stub_b
   demonstrou empiricamente. Futuros auditores podem usar esta regra para
   decidir se mudança em JSON exige ou não handoff próprio.

5. **`posicao_dashboard` como campo legado**: o campo não foi removido dos
   JSONs existentes nesta tarefa (fora de escopo). A migração é pendência
   explícita documentada em ADR-0010.
