---
name: relatorio-verificacao-documental-adr-0015-composicao-hierarquica-distribuicao-corpo
description: Verifica coerência, completude e aptidão para commit do pacote documental da ADR-0015 após patches complementares de NOMENCLATURA.md e sanitização terminológica
metadata:
  type: relatorio
  scope: scripts
  status: DOCUMENTATION_REJECTED
  data: "2026-07-10"
---

# RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO

## Status

DOCUMENTATION_REJECTED

---

## Objetivo

Verificar se o pacote documental da ADR-0015 ficou coerente, completo e pronto
para commit após os patches complementares de `docs/NOMENCLATURA.md` e
sanitização terminológica, considerando:

- criação da ADR-0015;
- atualização do índice de ADRs;
- atualização dos contratos afetados;
- bloqueio do H-0019;
- atualização de NOMENCLATURA.md;
- remoção da regra ativa de "3 vãos iguais";
- sanitização de "lado a lado" e "sobreposto" como termos normativos;
- preservação de aliases transicionais apenas como literais de compatibilidade;
- atualização do relatório documental;
- ausência de alterações em código, config e testes;
- ausência de caches.

---

## Base observada

| Item | Valor |
|---|---|
| Commit HEAD | `3b98856 docs: registra levantamento pos H-0018` |
| Branch | HEAD |
| Data da verificação | 2026-07-10 |

### git status --short

```
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

### git diff --stat

```
 scripts/docs/NOMENCLATURA.md                       | 108 ++++++-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md| 324 +++++++++++++++++++--
 scripts/docs/contratos/contrato_json_tela_minima.md|  40 ++-
 scripts/docs/contratos/contrato_tela_json.md       |  61 ++--
 5 files changed, 469 insertions(+), 65 deletions(-)
```

### git diff --name-only

```
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

### Arquivos não rastreados (untracked — `??`)

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

---

## Arquivos lidos

Todos os seguintes arquivos foram lidos integralmente:

- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/handoff/H-0019-layout-horizontal-plano-corpo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`

---

## Verificação da ADR-0015

| Critério | Status | Evidência |
|---|---|---|
| Título coerente com "Composição hierárquica e distribuição de área do corpo" | OK | Linha 18: `# ADR-0015 — Composição hierárquica e distribuição de área do corpo` |
| Status aceita | OK | Frontmatter `status: aceita`; seção Status: `aceita` |
| Data 2026-07-10 | OK | Frontmatter `data: "2026-07-10"`; seção Data: `2026-07-10` |
| Corpo como árvore | OK | Decisão 1 |
| Grupo como nó estrutural | OK | Decisão 2 |
| Arranjo por container | OK | Decisão 4 |
| Distribuição por container | OK | Decisão 5 |
| Distribuição horizontal por largura | OK | Decisão 4: "`arranjo = horizontal` reparte largura" |
| Distribuição vertical por altura | OK | Decisão 4: "`arranjo = vertical` reparte altura" |
| Percentual soma 100 | OK | Decisão 6: "soma dos valores deve ser exatamente 100" |
| Fração por pesos | OK | Decisão 6: pesos relativos com denominador implícito |
| Quantidade de valores igual a filhos diretos | OK | Decisão 7 |
| Arredondamento por maiores restos | OK | Decisão 8 |
| Contato contíguo sem vãos externos | OK | Decisão 9 |
| Preenchimento de área alocada | OK | Decisão 10 |
| Ajustado ao conteúdo como preferido | OK | Decisão 11: "deve ser tratado como `preferido`, não como `minimo`" |
| Paginação dentro da área alocada | OK | Decisão 12 |
| Terminal pequeno como política futura determinística | OK | Decisão 13 |
| Sincronização de cortes | OK | Decisões 14 e 15 |
| Bloqueio do H-0019 | OK | Decisão 16 |

**ADR-0015**: CONFORME em todos os critérios.

---

## Verificação do índice de ADRs

Linha da ADR-0015 encontrada em `INDICE_ADR.md`:

```
| ADR-0015 | Composição hierárquica e distribuição de área do corpo | aceita | 2026-07-10 |
```

Nenhuma ADR anterior foi reescrita indevidamente. As entradas de ADR-0001 a ADR-0014
permanecem intactas. A linha da ADR-0015 está na posição correta (última da tabela).

**INDICE_ADR.md**: CONFORME.

---

## Verificação dos contratos

### contrato_composicao_corpo.md

| Critério | Status | Evidência |
|---|---|---|
| Versão 0.3 | OK | Frontmatter: `versao: "0.3"` |
| ADR-0015 na rastreabilidade | OK | `adrs_aplicadas` inclui `ADR-0015-composicao-hierarquica-distribuicao-corpo.md` |
| Regra antiga de "3 vãos iguais" não como regra ativa | OK | Seção 5.6 nota: "formulação anterior de '3 vãos iguais'... está **supersedida** pela ADR-0015"; R-20 diz "A regra anterior de '3 vãos iguais' está supersedida... não deve ser implementada" |
| Particionamento contíguo como regra vigente | OK | Seção 5.6: "a regra é **particionamento contíguo** da largura disponível" |
| Grupo como nó estrutural sem borda própria | OK | Seção 3.2 e R-15 |
| Nível/profundidade máxima definidos | OK | Seção 3.2: "profundidade máxima: **3 níveis**; nível 4 ou superior gera erro estrutural determinístico" |
| Arranjo e distribuição são por container | OK | Seções 4.8 e 4.9 |
| Distribuição aloca área, não apenas conteúdo | OK | Seção 4.9: "distribuição aloca área, não apenas conteúdo" |
| Horizontal reparte largura | OK | Seção 4.8 |
| Vertical reparte altura | OK | Seção 4.8 |
| Percentual soma 100 | OK | Seção 5.7 |
| Fração usa pesos positivos | OK | Seção 5.7 |
| Arredondamento por maiores restos | OK | Seção 5.8 e R-19 |
| Preenchimento horizontal e vertical explicitado | OK | Seção 5.9 |
| Regras dinâmicas marcadas como conceito/futuro | OK | Seção 5.10: "Conceitos futuros" |
| Ajustado ao conteúdo como preferido, não mínimo | OK | Seção 5.10: "deve ser tratado como `preferido`, não como `minimo`"; R-21 |
| Sincronização de cortes como conceito ADR-0015 | OK | Seção 5.12 |
| Terminal pequeno sem fallback silencioso | OK | Seção 5.10: "Não pode haver truncamento silencioso nem fallback silencioso" |

**ACHADO BLOQUEANTE (A-001) — seção 8 (Critérios de validação):**

A seção 8 contém o seguinte critério ativo, não atualizado pelo patch:

```
- [ ] Em modo horizontal (`horizontal`, ADR-0011; alias transicional
      `lado_a_lado`), o espaço horizontal é dividido em 3 vãos iguais
      (borda↔col_1, col_1↔col_2, col_2↔borda).
```

Esta é a **regra antiga explicitamente supersedida** pela ADR-0015 (Decisão 9) e
corrigida na seção 5.6 do próprio contrato (que diz "R-20. ... A regra anterior de
'3 vãos iguais' está supersedida pela ADR-0015 e **não deve ser implementada**").
A seção 8 não foi atualizada para refletir o particionamento contíguo. Há contradição
normativa interna no contrato: seção 5.6 e R-20 ditam particionamento contíguo;
seção 8 dita 3 vãos iguais.

**ACHADO ALTO (A-002) — seção 8 (Critérios de validação):**

A seção 8 contém o seguinte critério com uso normativo de "lado a lado":

```
- [ ] Em layout lado a lado, cada elemento exibe seu próprio indicador de paginação
      dentro de sua própria borda.
```

O termo "layout lado a lado" é usado como descritor normativo ativo em critério de
validação. A sanitização aplicada ao patch complementar não alcançou a seção 8.

**ACHADO MÉDIO (A-003) — seção 5.5 (Indicador de paginação):**

O subitem de casos especiais:

```
- **Layout lado a lado**: cada elemento exibe sua própria paginação, ancorada à
  direita dentro da própria borda, independente do lado da tela.
```

Usa "Layout lado a lado" como label de caso em contexto normativo. Não é regra,
mas é descritor de caso que persiste com terminologia deprecada.

**ACHADO MÉDIO (A-004) — seção 9 (Pendências):**

A seção 9 lista a seguinte pendência:

```
- **`docs/NOMENCLATURA.md` seção 10** (ADR-0015): a referência a "3 vãos
  iguais" nessa seção está supersedida pela ADR-0015 e deve ser atualizada em
  ciclo futuro.
```

Esta pendência foi **resolvida** no patch complementar deste mesmo ciclo.
`NOMENCLATURA.md` seção 10 já foi corrigida. O item permanece como pendência futura,
induzindo confusão sobre o estado do ciclo. Deve ser marcado como concluído ou removido.

### contrato_tela_json.md

| Critério | Status | Evidência |
|---|---|---|
| `grupo` como nó estrutural, não tipo funcional | OK | Seção 8: "Nó estrutural `grupo` (ADR-0015, 2026-07-10)": `grupo` não é tipo funcional |
| `console`, `dashboard` e `lancador` permanecem tipos funcionais | OK | Seção 8: "Tipos funcionais válidos" lista os três |
| Corpo pode ser árvore de composição | OK | Seção 8: "Composição hierárquica como árvore (ADR-0015)" |
| Distribuição pertence a containers | OK | Seção 8: "Distribuição pertence a containers (ADR-0015)" |
| Schema não fechado além do que a ADR decidiu | OK | Distribuição dinâmica registrada como "conceitos futuros"; sincronização não fechada |

**contrato_tela_json.md**: CONFORME.

### contrato_json_tela_minima.md

| Critério | Status | Evidência |
|---|---|---|
| Envelope mínimo preservado | OK | Seção 4: estrutura `schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus` inalterada |
| Distribuição não obrigatória | OK | Seção 6.3: "`distribuicao` é **opcional** no envelope mínimo" |
| Grupos estruturais permitidos conforme contrato | OK | Seção 6.2: Nó estrutural `grupo` (ADR-0015) |
| `corpo.arranjo` continua opcional | OK | Seção 5.1: "`corpo.arranjo` é campo **permitido** no JSON de tela, mas **não obrigatório**" |
| ADR-0015 na rastreabilidade | OK | Frontmatter `adrs_aplicadas` inclui `ADR-0015` |

**contrato_json_tela_minima.md**: CONFORME.

---

## Verificação de NOMENCLATURA.md

### Comandos executados

```bash
grep -n "lado a lado|lado-a-lado|layout lado" docs/NOMENCLATURA.md || true
# (sem saída — nenhuma ocorrência)

grep -n "sobreposto|sobrepostos" docs/NOMENCLATURA.md || true
# 132: Os termos `sobreposto` e
# 133: `lado_a_lado` permanecem como **aliases transicionais** — `sobreposto → vertical`
# 137: **Controle de aliases (sanitização 2026-07-10)**: `sobreposto` e `lado_a_lado`
# 306: `sobreposto`/`lado_a_lado` são aliases transicionais
# 940: ADR-0011; `sobreposto`/`lado_a_lado` são aliases transicionais) pode ser

grep -n "lado_a_lado|vertical|horizontal|corpo.arranjo" docs/NOMENCLATURA.md || true
# (relevante) 132-143: seção 1.4, bloco de Controle de aliases
# 306: tabela com aliases transicionais
# 940: seção 10, texto corrigido
# 1128, 1130: seção 14, itens 12 e 13

grep -n "3 vãos|3 vaos|N+1|vãos iguais|vaos iguais" docs/NOMENCLATURA.md || true
# 950:  "3 vãos iguais" foi supersedida pela ADR-0015.

grep -n "ADR-0015|particionamento contíguo|distribuição por container|arranjo por container" docs/NOMENCLATURA.md || true
# 948-950: seção 10 — particionamento contíguo; supersessão de "3 vãos iguais"
# 1100: ## 14. Composição hierárquica e distribuição de área do corpo (ADR-0015)
# 1102: A ADR-0015 (2026-07-10) estabelece...
# 1104: ...está na ADR-0015 e no `contrato_composicao_corpo.md` (v0.3).
# 1160: ...sincronizados automaticamente (conceito ADR-0015...)
```

### Avaliação

| Critério | Status | Evidência |
|---|---|---|
| "lado a lado" não aparece como termo normativo ativo | OK | grep sem saída — nenhuma ocorrência |
| "lado a lado" não aparece (preferencialmente) | OK | Nenhuma ocorrência em toda a NOMENCLATURA.md |
| `lado_a_lado` apenas como alias transicional literal (backticks) | OK | Ocorrências são em backticks como alias, com controle de aliases explícito |
| `sobreposto` apenas como alias transicional literal (backticks) | OK | Todas as ocorrências são em backticks ou na frase de alias transitório |
| "sobrepostos" não como descrição normativa ativa | OK | Não encontrado |
| "3 vãos iguais" apenas como referência histórica supersedida | OK | Linha 950: "A regra anterior de '3 vãos iguais' foi supersedida pela ADR-0015." |
| NOMENCLATURA.md reflete ADR-0015 | OK | Seção 14 com 25 itens normativos; seção 10 corrigida |
| Pendências de dashboard usam `corpo.arranjo = "horizontal"` + `dashboard` | OK | Seções 6.1, 10 e 11 corrigidas para usar `corpo.arranjo = "horizontal"` |
| Bloco de controle de aliases adicionado na seção 1.4 | OK | Linhas 137-143: "Controle de aliases (sanitização 2026-07-10)" |

**NOMENCLATURA.md**: CONFORME.

---

## Verificação do bloqueio do H-0019

### Comandos executados

```bash
grep -n "HANDOFF_READY" docs/handoff/H-0019-layout-horizontal-plano-corpo.md || true
# (sem saída — HANDOFF_READY não existe no arquivo)

grep -n "BLOCKED_BY_ADR_0015_PENDING_REVISION|ARCHITECTURE_REVIEW_REQUIRED|ADR-0015" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md || true
# linha 4:   status: BLOCKED_BY_ADR_0015_PENDING_REVISION
# linha 16:  ## Bloqueio por ADR-0015
# linha 20:  A ADR-0015 formalizou novas regras normativas...
# linha 25:  ...deve ser revisado antes de qualquer implementação...
# linha 27:  ...revisada compatível com a ADR-0015...
# linha 30:  deve bloquear com `ARCHITECTURE_REVIEW_REQUIRED`.
# linha 37:  BLOCKED_BY_ADR_0015_PENDING_REVISION
# linha 72:  ADR-0015 (bloqueante)
# linha 90-100: ordem de autoridade com bloqueio explícito
```

| Critério | Status | Evidência |
|---|---|---|
| `HANDOFF_READY` não aparece | OK | grep sem saída |
| `BLOCKED_BY_ADR_0015_PENDING_REVISION` aparece | OK | Linhas 4 e 37 |
| H-0019 diz que não pode ser implementado no estado atual | OK | "Este handoff não deve ser implementado no estado atual." |
| H-0019 exige revisão antes de implementação | OK | "deve ser revisado antes de qualquer implementação" |
| H-0019 cita ADR-0015 como autoridade superior | OK | Seção "Ordem de autoridade" e linha 72 |
| Execução baseada na versão atual bloqueia com `ARCHITECTURE_REVIEW_REQUIRED` | OK | Linha 30 e linhas 97-100 |

**H-0019**: CONFORME.

---

## Verificação do relatório documental

| Critério | Status | Evidência |
|---|---|---|
| Status DOCUMENTATION_COMPLETED | OK | Frontmatter e seção Status |
| Registra criação da ADR-0015 | OK | Seção "Arquivos criados" |
| Registra atualização dos contratos | OK | Seção "Contratos atualizados" |
| Registra bloqueio do H-0019 | OK | Seção "Bloqueio aplicado ao H-0019" |
| Registra atualização de NOMENCLATURA.md | OK | Seção "Arquivos alterados"; seção "Patch complementar" |
| Registra sanitização de "lado a lado" | OK | Seção "Patch complementar — Sanitização terminológica" |
| Registra `sobreposto` e `lado_a_lado` apenas como aliases transicionais | OK | Seção "Patch complementar": "preservado apenas como alias transicional literal" |
| Não deixa NOMENCLATURA.md como pendência futura | OK | A seção "Pontos pendentes para ciclo futuro" NÃO inclui NOMENCLATURA.md |
| Registra ausência de alterações em tela/, config/, testes e código Python | OK | Seção "Fora de escopo preservado" |
| Registra ausência de caches | OK | Seções de verificações executadas |
| Registra ausência de commit | OK | "Nenhum commit foi criado nesta etapa" |

**NOTA (A-005) — Divergência numérica no diff stat do relatório documental:**

O relatório documental registra o diff stat de NOMENCLATURA.md como "~70 ++-"
(com til de aproximação), enquanto o diff real mostra 108 linhas modificadas.
Trata-se de estimativa aproximada explicitamente marcada com "~"; sem impacto
funcional.

**Relatório documental**: CONFORME (com nota A-005).

---

## Verificação de escopo negativo

```bash
git status --short tela config 2>/dev/null || true
# (sem saída)

git diff --name-only -- tela config 2>/dev/null || true
# (sem saída)

git diff --name-only | grep -E '\.py$|teste_|/test_' 2>/dev/null || true
# (sem saída)
```

| Critério | Status |
|---|---|
| Nenhum arquivo em `tela/` alterado | OK — nenhuma saída |
| Nenhum arquivo em `config/` alterado | OK — nenhuma saída |
| Nenhum teste alterado | OK — nenhuma saída |
| Nenhum arquivo Python alterado | OK — nenhuma saída |

---

## Verificação de caches

```bash
find . -name '__pycache__' -type d -prune -print
# (sem saída)

find . -name '*.pyc' -print
# (sem saída)
```

**Caches**: SEM `__pycache__`. SEM `.pyc`. CONFORME.

---

## Achados

### A-001 — BLOQUEANTE

**ID**: A-001
**Severidade**: BLOQUEANTE
**Descrição**: `contrato_composicao_corpo.md`, seção 8 (Critérios de validação) ainda
contém o seguinte critério de validação ativo com a regra antiga de "3 vãos iguais":

```
- [ ] Em modo horizontal (`horizontal`, ADR-0011; alias transicional
      `lado_a_lado`), o espaço horizontal é dividido em 3 vãos iguais
      (borda↔col_1, col_1↔col_2, col_2↔borda).
```

**Evidência**: O critério está em vigência formal como checklist de validação, enquanto
a seção 5.6 do mesmo contrato afirma: "a formulação anterior de '3 vãos iguais'... está
**supersedida** pela ADR-0015" e a regra R-20 afirma explicitamente "A regra anterior de
'3 vãos iguais' está supersedida pela ADR-0015 e **não deve ser implementada**".

**Impacto**: Contradição normativa interna ao contrato. Um implementador que siga a
seção 8 (critérios de aceite) implementará a regra antiga errada — com vãos externos
entre molduras — em vez do particionamento contíguo. Um agente de QA que aplique a
seção 8 literalmente reprovará uma implementação correta. A coexistência de R-20 e
deste critério torna o contrato auto-contraditório.

**Recomendação**: Corrigir o critério na seção 8 para refletir o particionamento
contíguo (ADR-0015, Decisão 9), alinhando-o com a seção 5.6 e com R-20.
Formulação sugerida:
```
- [ ] Em modo horizontal (`horizontal`, ADR-0011; alias transicional `lado_a_lado`),
      o espaço horizontal é distribuído por particionamento contíguo entre os filhos
      diretos: molduras adjacentes ficam coladas, sem vão externo entre elas (R-20,
      ADR-0015).
```

---

### A-002 — ALTO

**ID**: A-002
**Severidade**: ALTO
**Descrição**: `contrato_composicao_corpo.md`, seção 8 (Critérios de validação) contém
o seguinte critério com uso normativo ativo do termo deprecado "lado a lado":

```
- [ ] Em layout lado a lado, cada elemento exibe seu próprio indicador de paginação
      dentro de sua própria borda.
```

**Evidência**: O termo "layout lado a lado" é utilizado como descritor normativo ativo
de um caso de validação na seção 8. A sanitização terminológica aplicada no patch
complementar não alcançou a seção 8.

**Impacto**: Uso normativo de termo deprecado em critério de aceite formal. Contradiz
a sanitização declarada no relatório documental e no bloco de controle de aliases da
NOMENCLATURA.md. Embora menos grave que A-001 (não cria regra técnica errada), mantém
a terminologia deprecada em posição normativa.

**Recomendação**: Substituir "Em layout lado a lado" por "Em arranjo horizontal
(`corpo.arranjo = "horizontal"`)".

---

### A-003 — MÉDIO

**ID**: A-003
**Severidade**: MÉDIO
**Descrição**: `contrato_composicao_corpo.md`, seção 5.5 (Indicador de paginação),
subitem de casos especiais:

```
- **Layout lado a lado**: cada elemento exibe sua própria paginação, ancorada à
  direita dentro da própria borda, independente do lado da tela.
```

**Evidência**: Label de caso "Layout lado a lado" usa a terminologia deprecada como
cabeçalho de um caso especial em seção normativa.

**Impacto**: Uso de terminologia deprecada em label normativo descritivo. Menos crítico
que A-001 e A-002 pois não gera regra técnica errada, mas é inconsistente com a
sanitização declarada.

**Recomendação**: Substituir "**Layout lado a lado**" por
"**Arranjo horizontal (`arranjo = "horizontal"`)**".

---

### A-004 — MÉDIO

**ID**: A-004
**Severidade**: MÉDIO
**Descrição**: `contrato_composicao_corpo.md`, seção 9 (Pendências) ainda lista como
pendência futura:

```
- **`docs/NOMENCLATURA.md` seção 10** (ADR-0015): a referência a "3 vãos
  iguais" nessa seção está supersedida pela ADR-0015 e deve ser atualizada em
  ciclo futuro.
```

**Evidência**: O patch complementar deste ciclo já aplicou a correção na
`docs/NOMENCLATURA.md` seção 10. O relatório documental registra explicitamente
"seção 10 corrigida (regra de '3 vãos iguais' removida/supersedida)". A pendência
está obsoleta.

**Impacto**: Pendência stale induz confusão sobre o estado do ciclo. Leitores
futuros podem entender que a correção de NOMENCLATURA.md ainda está pendente.
Não cria erro técnico, mas compromete a consistência do histórico documental.

**Recomendação**: Remover ou marcar como resolvida a pendência sobre NOMENCLATURA.md
seção 10 na seção 9 de `contrato_composicao_corpo.md`.

---

### A-005 — NOTA

**ID**: A-005
**Severidade**: NOTA
**Descrição**: O `RELATORIO_DOCUMENTAL_ADR-0015...md` registra o diff stat de
NOMENCLATURA.md como "~70 ++-" (com til de aproximação), enquanto o `git diff --stat`
real mostra 108 linhas modificadas.

**Evidência**: `git diff --stat` retorna `scripts/docs/NOMENCLATURA.md | 108 ++++++-`.
Relatório documental registra "~70 ++-".

**Impacto**: Divergência numérica não crítica. O til indica valor aproximado deliberado.
Sem impacto funcional ou normativo.

**Recomendação**: Sem necessidade de correção — o til é marcador de aproximação.
Nota para rastreabilidade.

---

## Decisão

```
REJEITADO_CORRIGIR_ANTES_DO_COMMIT
```

**Justificativa**: O achado A-001 é BLOQUEANTE. A seção 8 (Critérios de validação)
de `contrato_composicao_corpo.md` contém um critério ativo que prescreve a regra
antiga de "3 vãos iguais" — regra explicitamente supersedida pela ADR-0015 e
corrigida na seção 5.6 do mesmo contrato. O contrato está auto-contraditório:
a seção normativa (5.6 + R-20) diz que "3 vãos iguais" não deve ser implementada;
a seção de critérios de aceite (8) diz que deve. Esta contradição impede que o
pacote seja commitado com integridade documental.

O achado A-002 (ALTO) agrava a situação: o mesmo critério de aceite usa o termo
normativo deprecado "layout lado a lado" sem correção.

---

## Próximo passo recomendado

**O pacote NÃO pode seguir para commit no estado atual.**

Antes do commit, é necessário corrigir `contrato_composicao_corpo.md`:

1. **Obrigatório — A-001 (BLOQUEANTE)**: Corrigir o critério de validação na seção 8
   que descreve "o espaço horizontal é dividido em 3 vãos iguais" para refletir o
   particionamento contíguo conforme ADR-0015 e seção 5.6.

2. **Obrigatório — A-002 (ALTO)**: Corrigir o critério "Em layout lado a lado, cada
   elemento exibe seu próprio indicador de paginação" para usar terminologia vigente
   (`arranjo horizontal`).

3. **Recomendado — A-003 (MÉDIO)**: Atualizar o label "**Layout lado a lado**" na
   seção 5.5 para "**Arranjo horizontal**".

4. **Recomendado — A-004 (MÉDIO)**: Marcar como resolvida ou remover a pendência
   sobre NOMENCLATURA.md seção 10 da seção 9 de pendências.

Após essas correções, o pacote pode seguir para nova verificação antes do commit.

Os demais elementos do pacote (ADR-0015, INDICE_ADR.md, contrato_tela_json.md,
contrato_json_tela_minima.md, H-0019, NOMENCLATURA.md e o relatório documental)
estão CONFORMES e não precisam de alteração.

---

## Verificações executadas

### git status --short

```
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

### git diff --stat

```
 scripts/docs/NOMENCLATURA.md                        | 108 ++++++-
 scripts/docs/adr/INDICE_ADR.md                      |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md | 324 +++++++++++++++++++--
 scripts/docs/contratos/contrato_json_tela_minima.md |  40 ++-
 scripts/docs/contratos/contrato_tela_json.md        |  61 ++--
 5 files changed, 469 insertions(+), 65 deletions(-)
```

### git diff --name-only

```
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

### grep "lado a lado|lado-a-lado|layout lado" docs/NOMENCLATURA.md

```
(sem saída)
```

### grep "sobreposto|sobrepostos" docs/NOMENCLATURA.md

```
132: Os termos `sobreposto` e
133: `lado_a_lado` permanecem como **aliases transicionais**
137: **Controle de aliases (sanitização 2026-07-10)**: `sobreposto` e `lado_a_lado`
306: `sobreposto`/`lado_a_lado` são aliases transicionais
940: `sobreposto`/`lado_a_lado` são aliases transicionais
```

### grep "3 vãos|vãos iguais" docs/NOMENCLATURA.md

```
950: "3 vãos iguais" foi supersedida pela ADR-0015.
```

### grep "HANDOFF_READY" docs/handoff/H-0019-layout-horizontal-plano-corpo.md

```
(sem saída)
```

### grep "BLOCKED_BY_ADR_0015" docs/handoff/H-0019-layout-horizontal-plano-corpo.md

```
linha 4:  status: BLOCKED_BY_ADR_0015_PENDING_REVISION
linha 37: BLOCKED_BY_ADR_0015_PENDING_REVISION
```

### git status --short tela config

```
(sem saída)
```

### git diff --name-only -- tela config

```
(sem saída)
```

### git diff --name-only | grep -E '.py$|teste_|/test_'

```
(sem saída)
```

### find . -name '__pycache__' -type d -prune -print

```
(sem saída)
```

### find . -name '*.pyc' -print

```
(sem saída)
```

---

## Git status final

```
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
?? docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```
