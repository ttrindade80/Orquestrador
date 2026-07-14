---
name: ADR-0010-composicao-hierarquica-corpo-dashboard
description: dashboard deixa de ser eixo especial externo e passa a seguir a composicao geral do corpo; corpo admite estrutura declarativa hierarquica; console, lancador e dashboard sao elementos funcionais do corpo
metadata:
  type: adr
  status: aceita
  data: 2026-07-08
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/NOMENCLATURA.md
  handoffs_bloqueados:
    - docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
---

# ADR-0010 — Composição hierárquica do corpo e dashboard como elemento funcional

## Status

`aceita`

## Data

2026-07-08

## Contexto

O H-0011 foi preparado para implementar renderização `lado_a_lado` e barra
mínima do Orquestrador. A auditoria bloqueou o handoff com
`ARCHITECTURE_REVIEW_REQUIRED` identificando a seguinte causa central:

> A documentação atual ainda trata `dashboard` como exceção com eixo próprio,
> mas a direção correta agora é que `dashboard` siga o padrão geral de
> composição do corpo.

O contrato vigente (`contrato_composicao_corpo.md`) declara `posicao_dashboard`
como "eixo próprio — **nunca afetado** por `arranjo` nem por `tiling`",
o que cria uma regra especial que contradiz o mecanismo geral de composição
do corpo. O handoff H-0011, ao separar `grupo_lado_a_lado` de `grupo_dashboard`
no renderer, perpetuava esse modelo incorreto.

A validação declarativa registrada em `f41bd2f` (stub_b) confirmou que
alterações puramente declarativas em JSON — quando o suporte/binding já existe
— não exigem ciclo completo de handoff. Essa regra precisava ser formalizada
no contrato de processo.

Dois achados bloqueantes da auditoria exigem correção arquitetural antes da
implementação:

1. **Algoritmo `lado_a_lado` contradiz o contrato**: o handoff autorizava
   `col_w = total_w // 2` sem vãos entre colunas, mas o contrato de
   composição seção 5.6 exige 3 vãos iguais (`borda↔coluna_1`,
   `coluna_1↔coluna_2`, `coluna_2↔borda`).

2. **Fallback para 3+ elementos contradiz a regra declarativa**: o handoff
   permitia empilhar 3+ elementos `console`/`lancador` mesmo com
   `arranjo = "lado_a_lado"`, o que autoriza ignorar o arranjo declarado
   por quantidade de elementos.

Esta ADR não corrige o handoff H-0011 — prepara a base documental para
que o H-0011 seja reescrito ou auditado em ciclo posterior, na sequência
H-0011A–D.

---

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. `dashboard` segue o padrão geral de composição do corpo.**

`dashboard` deixa de ser tratado como exceção com posicionamento próprio
especial. A composição visual de `dashboard` no corpo é determinada pela
estrutura declarativa do `corpo` do `tela.json`, como acontece com
`console` e `lancador`.

**2. `console`, `lancador` e `dashboard` são elementos funcionais do corpo.**

Os três tipos são elementos declarados em `corpo.elementos[]`. Nenhum deles
tem mecanismo de posicionamento que contradiga o mecanismo geral de composição.
A taxonomia fechada (`console`, `lancador`, `dashboard`) permanece inalterada.

**3. Composição visual pertence à estrutura declarada no corpo da tela.**

O compositor não conhece regras especiais de posicionamento de elemento por
tipo. Ele executa a estrutura declarada no `corpo` do `tela.json`. O renderer
não pode separar elementos por tipo para aplicar lógica de posicionamento
diferenciada não declarada.

**4. `campo posicao_dashboard` como eixo separado independente está descontinuado.**

O campo `posicao_dashboard` declarado na instância do elemento `tipo=dashboard`,
tratado como "eixo próprio — nunca afetado por `arranjo` nem por `tiling`",
está descontinuado como mecanismo separado. O posicionamento do `dashboard` é
controlado pela estrutura declarativa do `corpo`. JSONs existentes com
`posicao_dashboard` podem ser honrados por compatibilidade em H-0011A; a
migração/descarte do campo ocorrerá em handoff específico.

**5. O `corpo` passa a admitir estrutura declarativa hierárquica.**

`corpo.elementos[]` pode evoluir de uma lista plana de elementos para uma
estrutura que admite agrupamentos e composição hierárquica. A lista plana
atual permanece válida e compatível. A evolução é incremental:

| Etapa | Capacidade prevista |
|---|---|
| H-0011A | Layout hierárquico vertical compatível — estrutura pode ter grupos; JSONs atuais permanecem válidos |
| H-0011B | Layout horizontal plano — todos os elementos, incluindo `dashboard`, participam do arranjo horizontal |
| H-0011C | Distribuição por percentual/fração |
| H-0011D | Aninhamento de grupos |

**6. Campos internos de cada elemento continuam sendo responsabilidade do tipo/instância.**

A estrutura declarada no `corpo` controla posicionamento e composição
inter-elemento. O que está dentro de cada elemento — campos de `dashboard`,
itens de `console`, itens de `lancador` — continua sendo responsabilidade
da instância declarada, não do compositor geral. O compositor não conhece
os campos internos de `dashboard`.

**7. `dashboard` continua passivo e não navegável por `[✥]`.**

Esta decisão não altera a natureza do `dashboard`. Ele permanece:
- não navegável por `[✥]`;
- não obrigatório — sua presença exige elemento `tipo=dashboard` em
  `corpo.elementos[]`;
- sem conteúdo universal fixo;
- passivo — o usuário lê; não interage.

**8. `console` continua o único tipo navegável por `[✥]`.**

Esta decisão não altera a restrição de `[✥]`. Somente `console` navegável
é condição de existência e ativação de `[✥]`. `lancador` e `dashboard` não
são condição de existência nem de ativação de `[✥]`. A ADR-0005 e a
ADR-0006 permanecem em vigor neste ponto.

**9. `lancador` continua não navegável por `[✥]`.**

Nenhuma regra do `lancador` muda. O `lancador` permanece corpo de navegação
por itens via `tela_destino`, não navegável por `[✥]` nem pelas setas da
`barra_de_menus`. A ADR-0005 permanece em vigor.

**10. A regra de 3 vãos iguais para `lado_a_lado` é aplicada universalmente.**

A distribuição de espaço em modo `lado_a_lado`, conforme `contrato_composicao_corpo.md`
seção 5.6 (`borda↔coluna_1`, `coluna_1↔coluna_2`, `coluna_2↔borda`), aplica-se
à composição geral do corpo incluindo `dashboard` quando participar do
arranjo horizontal. O algoritmo do handoff H-0011 (`col_w = total_w // 2`
sem vãos) está em contradição com este contrato e deve ser corrigido.

**11. A sequência H-0011A–D é a sequência incremental prevista próxima.**

Esta ADR prepara a base para os handoffs H-0011A, H-0011B, H-0011C e H-0011D.
Não decide arquitetura futura além desta sequência. Handoffs futuros além
desta sequência não são decididos agora.

**12. Esta ADR não corrige nem reescreve o handoff H-0011 bloqueado.**

O handoff H-0011 permanece bloqueado (`ARCHITECTURE_REVIEW_REQUIRED`) como
artefato não rastreado. A correção ocorrerá em ciclo posterior que produza
H-0011A como novo handoff incremental a partir desta base documental.

---

## Consequências

### Artefatos a atualizar nesta tarefa

| Arquivo | Atualização necessária |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0010 na tabela |
| `docs/contratos/contrato_composicao_corpo.md` | Remover `posicao_dashboard` como eixo separado; declarar `dashboard` como elemento funcional da composição geral; atualizar R-5, R-9 e critérios de validação; atualizar pendência de composição `lado_a_lado` + `dashboard` |
| `docs/contratos/contrato_tela_json.md` | Atualizar schema conceitual do `corpo` para aceitar composição hierárquica; registrar a sequência H-0011A–D |
| `docs/contratos/contrato_processo_desenvolvimento.md` | Adicionar regra sobre mudanças declarativas em JSON |
| `docs/NOMENCLATURA.md` | Atualizar linha de "Posição do dashboard" na seção 3 para remover linguagem de eixo separado não afetado por tiling |

### Arquivos que não devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `docs/contratos/contrato_lancador.md` | Nenhuma regra do `lancador` muda |
| `docs/contratos/contrato_barra_de_menus.md` | Nenhuma regra de `[✥]` muda; barra continua espelho da declaração |
| `docs/contratos/contrato_console.md` | Nenhuma regra do `console` muda |
| `docs/contratos/contrato_chip.md` | Nenhuma regra de `chip` muda |
| Qualquer arquivo em `config/` | Implementação aguarda handoffs H-0011A–D |
| Qualquer arquivo em `tela/` | Implementação aguarda handoffs H-0011A–D |
| `docs/handoff/H-0011-*` | O handoff bloqueado não é corrigido agora |

### Pendências derivadas

- Criar H-0011A: handoff de layout hierárquico vertical compatível, baseado
  nesta ADR e no `contrato_composicao_corpo.md` atualizado.
- Migrar/descartar `posicao_dashboard` nos JSONs de tela existentes em
  handoff específico após H-0011A.
- H-0011B, H-0011C, H-0011D: sequência incremental após H-0011A aprovado.

---

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR:

- Foco multi-console com Tab.
- Pop-up de qualquer tipo.
- Execução multi-console.
- Seleção entre múltiplos consoles.
- Realce visual de console ativo.
- Política completa futura de Enter.
- Orquestrador real completo.
- Execução real de processos.
- Registry novo de telas ou ações.
- Novos tipos de corpo fora de `console`, `lancador` e `dashboard`.
- Handoffs futuros além da sequência H-0011A–D.
- Algoritmo de distribuição de espaço para 3+ elementos em `lado_a_lado`
  (será tratado em H-0011D com aninhamento de grupos).
- Schema detalhado de grupos no `corpo.elementos[]`.
- Especificação de quais campos substituem `posicao_dashboard` na composição
  hierárquica — será tratado nos handoffs H-0011A–D conforme cada capacidade
  for implementada.

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Manter `posicao_dashboard` como eixo separado e corrigir apenas o algoritmo do H-0011 | Perpetua o modelo errado; não resolve o bloqueio arquitetural central identificado na auditoria; deixa contradição entre eixo especial e mecanismo geral |
| Criar quarto tipo de corpo para composição hierárquica | Contradiz ADR-0006 e ADR-0007; a taxonomia fechada já cobre os casos de uso; hierarquia é mecanismo de composição, não tipo de conteúdo |
| Tratar a sequência H-0011A–D como único handoff grande | Viola o princípio de ciclos coesos e incrementais; cada etapa é implementação separada verificável |
| Especificar o schema completo de grupos hierárquicos agora | Precipitado; H-0011A não exige schema completo; prematura criação de DSL ampla sem caso de uso concreto imediato |
