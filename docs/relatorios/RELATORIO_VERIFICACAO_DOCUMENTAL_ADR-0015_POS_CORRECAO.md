---
name: relatorio-verificacao-documental-adr-0015-pos-correcao
description: Verificação pós-correção do pacote documental da ADR-0015 após patch corretivo que resolveu os achados A-001 a A-004 do relatório rejeitado
metadata:
  type: relatorio
  scope: scripts
  status: DOCUMENTATION_VERIFIED_WITH_NOTES
  data: "2026-07-10"
---

# RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO

## Status

DOCUMENTATION_VERIFIED_WITH_NOTES

---

## Objetivo

Verificar se o patch corretivo aplicado após a rejeição do pacote documental da
ADR-0015 (`RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`,
status `DOCUMENTATION_REJECTED`) resolveu os achados A-001, A-002, A-003 e A-004
de forma correta e sem introduzir nova contradição normativa.

Escopo desta verificação:

1. Confirmar que A-001 foi corrigido.
2. Confirmar que A-002 foi corrigido.
3. Confirmar que A-003 foi corrigido.
4. Confirmar que A-004 foi corrigido.
5. Confirmar que não surgiu nova contradição normativa.
6. Confirmar que o pacote documental está pronto para commit.
7. Confirmar que nenhum arquivo proibido foi alterado.
8. Confirmar ausência de caches.

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
?? docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

### git diff --stat

```
 scripts/docs/NOMENCLATURA.md                        | 108 ++++++-
 scripts/docs/adr/INDICE_ADR.md                      |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md | 331 +++++++++++++++++++--
 scripts/docs/contratos/contrato_json_tela_minima.md |  40 ++-
 scripts/docs/contratos/contrato_tela_json.md        |  61 ++--
 5 files changed, 469 insertions(+), 72 deletions(-)
```

> Nota: o relatório rejeitado registrava 65 deleções em `contrato_composicao_corpo.md`.
> O diff atual mostra 72 deleções (diferença de 7 linhas), coerente com a remoção do
> critério antigo de "3 vãos iguais" e do label "Layout lado a lado" pelo patch corretivo.

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
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

**Confirmação**: o relatório rejeitado
`RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`
permanece no workspace como arquivo não rastreado (`??`). Não foi sobrescrito. Histórico
preservado conforme exigido.

---

## Arquivos lidos

Todos os seguintes arquivos foram lidos integralmente:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/handoff/H-0019-layout-horizontal-plano-corpo.md`

---

## Verificação dos achados anteriores

### A-001 — Regra antiga de 3 vãos iguais

**Resultado: CORRIGIDO**

**Comando executado:**

```bash
grep -n "3 vãos\|3 vaos\|N+1\|vãos iguais\|vaos iguais" docs/contratos/contrato_composicao_corpo.md || true
```

**Saída:**

```
485: > **Nota**: a formulação anterior de "3 vãos iguais" registrada neste contrato
750: no último caractere útil. A regra anterior de "3 vãos iguais" está supersedida
```

**Comando executado:**

```bash
grep -n "particionamento contíguo\|ADR-0015\|R-20" docs/contratos/contrato_composicao_corpo.md || true
```

**Saída (trecho relevante para A-001):**

```
479: a regra é **particionamento contíguo** da
483: a última termina no último caractere útil. (ADR-0015)
486: > e em `docs/NOMENCLATURA.md` seção 10 está **supersedida** pela ADR-0015. A
747: **R-20. Contato entre molduras — sem vão externo (ADR-0015).**
750: ... A regra anterior de "3 vãos iguais" está supersedida pela ADR-0015 e não deve ser implementada.
802: - [ ] Em modo horizontal (`horizontal`, ADR-0011; alias transicional `lado_a_lado`), o espaço
       horizontal é distribuído por particionamento contíguo entre os filhos diretos do container:
       molduras adjacentes ficam coladas, sem vão externo entre elas, e a soma das larguras alocadas
       deve fechar exatamente a largura disponível (ADR-0015, R-20).
```

**Análise:**

O critério ativo com "3 vãos iguais" que estava na seção 8 foi removido. A linha 802 agora
prescreve particionamento contíguo com referência explícita a ADR-0015 e R-20, alinhado
com a seção 5.6 e com R-20.

As ocorrências remanescentes nas linhas 485 e 750 são referências históricas marcadas
explicitamente como supersedidas — não são regras ativas. A linha 485 introduz uma nota
de rodapé com `> **Nota**: a formulação anterior...`. A linha 750 faz parte de R-20, que
diz "A regra anterior de '3 vãos iguais' **está supersedida pela ADR-0015 e não deve ser
implementada**."

A contradição normativa interna apontada no relatório rejeitado foi eliminada:
seção 5.6, R-20 e seção 8 agora convergem para particionamento contíguo.

---

### A-002 — Uso normativo de "layout lado a lado" na seção 8

**Resultado: CORRIGIDO**

**Comando executado:**

```bash
grep -n "lado a lado\|lado-a-lado\|layout lado" docs/contratos/contrato_composicao_corpo.md || true
```

**Saída:**

```
451: - **Combinação lado a lado + dashboard presente**: não definida — ver seção 9.
479: historicamente "lado a lado"): a regra é **particionamento contíguo** da
481: Molduras adjacentes ficam coladas, produzindo bordas lado a lado
```

**Análise:**

Nenhuma ocorrência de "lado a lado" na seção 8. O critério que o relatório rejeitado
identificou como "Em layout lado a lado, cada elemento exibe seu próprio indicador de
paginação..." foi corrigido. A linha 795 do arquivo agora contém:

```
- [ ] Em arranjo horizontal (`corpo.arranjo = "horizontal"`), cada elemento exibe seu
      próprio indicador de paginação dentro de sua própria borda.
```

Confirmado por:

```bash
grep -n "arranjo horizontal\|corpo\.arranjo.*horizontal" docs/contratos/contrato_composicao_corpo.md || true
```

Saída relevante:
```
795: - [ ] Em arranjo horizontal (`corpo.arranjo = "horizontal"`), cada elemento exibe
           seu próprio indicador de paginação dentro de sua própria borda.
```

O uso normativo ativo de "layout lado a lado" na seção 8 foi eliminado.

---

### A-003 — Label "Layout lado a lado" na seção 5.5

**Resultado: CORRIGIDO**

**Evidência:**

```bash
grep -n "arranjo horizontal\|corpo\.arranjo.*horizontal\|arranjo = \"horizontal\"" \
  docs/contratos/contrato_composicao_corpo.md || true
```

Saída relevante para linha 450:
```
450: - **Arranjo horizontal (`arranjo = "horizontal"`)**: cada elemento exibe sua própria
       paginação, ancorada à direita dentro da própria borda, independente do lado da tela.
```

O label "**Layout lado a lado**" foi substituído por "**Arranjo horizontal (`arranjo = "horizontal"`)**".
A regra prescrita permanece idêntica; apenas a terminologia foi atualizada.

---

### A-004 — Pendência obsoleta sobre NOMENCLATURA.md seção 10

**Resultado: CORRIGIDO**

**Comando executado:**

```bash
grep -n "NOMENCLATURA.md.*seção 10\|NOMENCLATURA.md.*pendência\|3 vãos.*NOMENCLATURA" \
  docs/contratos/contrato_composicao_corpo.md || true
```

**Saída:**

```
486: > e em `docs/NOMENCLATURA.md` seção 10 está **supersedida** pela ADR-0015. A
```

**Análise:**

A linha 486 está dentro de uma nota na seção 5.6 (não na seção 9). O trecho completo é:

```
> **Nota**: a formulação anterior de "3 vãos iguais" registrada neste contrato
> e em `docs/NOMENCLATURA.md` seção 10 está **supersedida** pela ADR-0015. A
> regra correta é particionamento contíguo, conforme decisão explícita do usuário
> na revisão pós-auditoria do H-0019 (2026-07-09). `docs/NOMENCLATURA.md`
> seção 10 deve ser atualizada em ciclo futuro.
```

Esta ocorrência é nota histórica dentro da seção 5.6, não pendência ativa. A pendência
da seção 9 do relatório rejeitado dizia:

```
- **`docs/NOMENCLATURA.md` seção 10** (ADR-0015): a referência a "3 vãos
  iguais" nessa seção está supersedida pela ADR-0015 e deve ser atualizada em
  ciclo futuro.
```

Esse item foi removido da seção 9. A seção 9 atual não lista `NOMENCLATURA.md`
seção 10 como pendência futura.

**NOTA adicional:** A nota na seção 5.6 (linha 486) diz "deve ser atualizada em ciclo
futuro" — mas `NOMENCLATURA.md` seção 10 já foi atualizada neste ciclo (patch complementar).
Esta frase remanescente na nota da seção 5.6 é levemente imprecisa (diz "ciclo futuro"
para algo já feito). Contudo, está em contexto de nota histórica (bloqueada por `>`),
não em seção de pendências ativas, e não gera regra técnica errada. Classificado como
NOTA — não bloqueia.

---

## Verificação de ocorrências remanescentes de "lado a lado"

Ocorrências em `contrato_composicao_corpo.md` após o patch corretivo:

| Linha | Trecho | Classificação | Bloqueia? |
|---|---|---|---|
| 451 | `**Combinação lado a lado + dashboard presente**: não definida — ver seção 9.` | Label de caso não definido; seção 9 usa terminologia correta (`arranjo = "horizontal"`) | Não — BAIXO |
| 479 | `historicamente "lado a lado"): a regra é **particionamento contíguo** da` | Referência histórica supersedida, entre aspas com marcador explícito "historicamente" | Não — aceitável |
| 481 | `Molduras adjacentes ficam coladas, produzindo bordas lado a lado` | Descrição visual física do resultado de molduras coladas (`││`, `╮╭`, `╯╰`); não é terminologia normativa | Não — aceitável |

**Análise das ocorrências:**

- **Linha 451**: O label usa "lado a lado" em contexto de caso especial marcado como
  "não definida". A seção 9, que documenta essa pendência, usa terminologia correta:
  "Combinação `arranjo = horizontal` + `dashboard` presente". O label é apenas um
  identificador de referência cruzada dentro da seção 5.5. Não prescreve nenhuma regra
  e não contradiz a terminologia vigente. Achado BAIXO — não bloqueia.
- **Linha 479**: "historicamente" é marcador explícito de referência histórica. O trecho
  está entre aspas e imediatamente seguido por "a regra é **particionamento contíguo**",
  que estabelece a terminologia vigente. Aceitável.
- **Linha 481**: "bordas lado a lado" é descrição visual do fenômeno físico (molduras
  coladas), não terminologia normativa. O contrato usa isso para explicar o aspecto visual
  de `││`, `╮╭`, `╯╰`. Aceitável.

**Nenhum uso normativo ativo de "lado a lado"** foi encontrado no contrato.

---

## Verificação do relatório documental

**Comando executado:**

```bash
grep -n "Patch corretivo pós-verificação\|A-001\|A-002\|A-003\|A-004\|DOCUMENTATION_COMPLETED" \
  docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md || true
```

**Saída:**

```
7:   status: DOCUMENTATION_COMPLETED
15:  DOCUMENTATION_COMPLETED
391: ## Patch corretivo pós-verificação documental (2026-07-10)
396: - **A-001 corrigido**: critério de validação da seção 8 substituiu "o espaço
399: - **A-002 corrigido**: critério da seção 8 "Em layout lado a lado, cada elemento
403: - **A-003 corrigido**: label de caso especial da seção 5.5 reescrito de
405: - **A-004 corrigido**: pendência obsoleta sobre `docs/NOMENCLATURA.md` seção 10
416: DOCUMENTATION_COMPLETED
```

**Avaliação:**

| Critério | Status | Evidência |
|---|---|---|
| Status DOCUMENTATION_COMPLETED | OK | Frontmatter (linha 7) e seção Status (linha 15) |
| Seção de patch corretivo pós-verificação | OK | Linha 391: "## Patch corretivo pós-verificação documental (2026-07-10)" |
| A-001 registrado como corrigido | OK | Linha 396 |
| A-002 registrado como corrigido | OK | Linha 399 |
| A-003 registrado como corrigido | OK | Linha 403 |
| A-004 registrado como corrigido | OK | Linha 405 |
| Não diz que o pacote está pronto para commit antes desta verificação | OK | Linha 410: "O pacote precisa passar por nova verificação antes do commit." |

**Relatório documental**: CONFORME.

---

## Verificação do H-0019

**Comandos executados:**

```bash
grep -n "HANDOFF_READY" docs/handoff/H-0019-layout-horizontal-plano-corpo.md || true
# (sem saída)

grep -n "BLOCKED_BY_ADR_0015_PENDING_REVISION\|ARCHITECTURE_REVIEW_REQUIRED\|ADR-0015" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md | head -10 || true
```

**Saída:**

```
4:  status: BLOCKED_BY_ADR_0015_PENDING_REVISION
16: ## Bloqueio por ADR-0015
20: A ADR-0015 formalizou novas regras normativas...
25: ...deve ser revisado antes de qualquer implementação...
27: ...revisada compatível com a ADR-0015...
30: `ARCHITECTURE_REVIEW_REQUIRED`.
37: BLOCKED_BY_ADR_0015_PENDING_REVISION
72: ADR-0015 (bloqueante)
90: ADRs aceitas (..., ADR-0015)
92: este handoff (H-0019)  [BLOQUEADO — ver seção "Bloqueio por ADR-0015"]
```

**Avaliação:**

| Critério | Status | Evidência |
|---|---|---|
| `HANDOFF_READY` não aparece | OK | Sem saída no grep |
| `BLOCKED_BY_ADR_0015_PENDING_REVISION` aparece | OK | Linhas 4 e 37 |
| H-0019 não deve ser implementado no estado atual | OK | "Este handoff não deve ser implementado no estado atual." |
| Execução bloqueia com `ARCHITECTURE_REVIEW_REQUIRED` | OK | Linha 30 e linhas 97-100 |
| ADR-0015 citada como autoridade superior | OK | Linhas 16, 20, 72, 90, 92 |

**H-0019**: CONFORME. Continua bloqueado. Não sofreu alteração.

---

## Verificação de NOMENCLATURA.md

**Comandos executados:**

```bash
grep -n "lado a lado\|lado-a-lado\|layout lado" docs/NOMENCLATURA.md || true
# (sem saída)

grep -n "3 vãos\|3 vaos\|N+1\|vãos iguais\|vaos iguais" docs/NOMENCLATURA.md || true
# 950:  "3 vãos iguais" foi supersedida pela ADR-0015.

grep -n "ADR-0015\|particionamento contíguo\|corpo\.arranjo = \"horizontal\"" docs/NOMENCLATURA.md || true
# 143, 171, 527, 709, 946-950, 957, 1014, 1100, 1102, 1104, 1160
```

**Avaliação:**

| Critério | Status | Evidência |
|---|---|---|
| "lado a lado" não aparece como termo normativo ativo | OK | Sem saída no grep |
| "3 vãos iguais" apenas como referência histórica supersedida | OK | Linha 950: "foi supersedida pela ADR-0015" |
| ADR-0015 referenciada corretamente | OK | Seções 10 e 14 (múltiplas linhas) |
| Particionamento contíguo como regra vigente | OK | Linha 946: "particionado de forma contígua" |

**NOMENCLATURA.md**: CONFORME. Permanece sanitizado. Nenhuma alteração detectada
nesta rodada (mesmo diff que o relatório rejeitado registrou).

---

## Verificação de escopo negativo

**Comandos executados:**

```bash
git status --short tela config 2>/dev/null || true
# (sem saída)

git diff --name-only -- tela config 2>/dev/null || true
# (sem saída)

git diff --name-only | grep -E '\.py$|teste_|/test_' 2>/dev/null || true
# (sem saída)
```

**Avaliação:**

| Critério | Status |
|---|---|
| Nenhum arquivo em `tela/` alterado | OK — sem saída |
| Nenhum arquivo em `config/` alterado | OK — sem saída |
| Nenhum teste alterado | OK — sem saída |
| Nenhum arquivo Python alterado | OK — sem saída |

**Escopo negativo**: CONFORME.

---

## Verificação de caches

**Comandos executados:**

```bash
find . -name '__pycache__' -type d -prune -print
# (sem saída)

find . -name '*.pyc' -print
# (sem saída)
```

**Caches**: SEM `__pycache__`. SEM `.pyc`. CONFORME.

---

## Achados

### B-001 — BAIXO

**ID**: B-001
**Severidade**: BAIXO
**Descrição**: `contrato_composicao_corpo.md`, seção 5.5, linha 451, label de caso
especial ainda usa "lado a lado":

```
- **Combinação lado a lado + dashboard presente**: não definida — ver seção 9.
```

**Evidência**: A terminologia deprecada persiste como identificador de caso em seção 5.5.
A seção 9, que documenta a mesma pendência, já usa terminologia correta:
"Combinação `arranjo = horizontal` + `dashboard` presente".

**Impacto**: Inconsistência terminológica de baixa severidade. Não prescreve nenhuma
regra técnica — o caso é marcado como "não definida". Não contradiz nenhuma regra
vigente. Não afeta implementação.

**Recomendação**: Substituir "**Combinação lado a lado + dashboard presente**" por
"**Combinação `arranjo = "horizontal"` + `dashboard` presente**" para consistência
plena com a seção 9 e com a terminologia vigente. Pode ser corrigido neste ciclo
ou em ciclo futuro.

---

### B-002 — NOTA

**ID**: B-002
**Severidade**: NOTA
**Descrição**: `contrato_composicao_corpo.md`, seção 5.6, nota de rodapé (linha 488),
diz `docs/NOMENCLATURA.md` seção 10 "deve ser atualizada em ciclo futuro", mas a
correção já foi aplicada neste ciclo.

**Evidência**:
```
> `docs/NOMENCLATURA.md` seção 10 deve ser atualizada em ciclo futuro.
```

**Impacto**: Frase levemente imprecisa em nota histórica (blockquote `>`). Não gera
regra técnica errada. O estado real de NOMENCLATURA.md seção 10 está correto.
A nota está em contexto histórico explícito.

**Recomendação**: Sem necessidade de correção urgente. Nota para rastreabilidade.

---

## Decisão

```
APROVADO_COM_NOTAS_PARA_COMMIT
```

**Justificativa:**

Os quatro achados bloqueantes/alto/médio do relatório rejeitado foram todos corrigidos:

- **A-001 (BLOQUEANTE)**: critério ativo de "3 vãos iguais" na seção 8 foi substituído
  por particionamento contíguo com referência a ADR-0015 e R-20. Contradição normativa
  interna eliminada.
- **A-002 (ALTO)**: critério "Em layout lado a lado" na seção 8 foi substituído por
  "Em arranjo horizontal (`corpo.arranjo = "horizontal"`)". Terminologia deprecada removida
  de posição normativa.
- **A-003 (MÉDIO)**: label "**Layout lado a lado**" na seção 5.5 foi substituído por
  "**Arranjo horizontal (`arranjo = "horizontal"`)**". Terminologia vigente adotada.
- **A-004 (MÉDIO)**: pendência obsoleta sobre `docs/NOMENCLATURA.md` seção 10 foi removida
  da seção 9 do contrato. Seção de pendências está coerente com o estado atual.

Os achados pós-correção identificados (B-001 BAIXO, B-002 NOTA) não bloqueiam o commit.
B-001 é inconsistência terminológica em label de caso não definido; B-002 é imprecisão em
nota histórica. Nenhum deles cria regra técnica errada nem contradiz regra vigente.

O pacote documental está normativo, internamente coerente e coerente com a ADR-0015.

---

## Próximo passo recomendado

**O pacote está apto para revisão humana final e commit.**

O commit deve incluir todos os arquivos modificados e não rastreados do pacote documental
da ADR-0015:

- `docs/NOMENCLATURA.md` (modificado)
- `docs/adr/INDICE_ADR.md` (modificado)
- `docs/contratos/contrato_composicao_corpo.md` (modificado)
- `docs/contratos/contrato_json_tela_minima.md` (modificado)
- `docs/contratos/contrato_tela_json.md` (modificado)
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` (não rastreado)
- `docs/handoff/H-0019-layout-horizontal-plano-corpo.md` (não rastreado)
- `docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md` (não rastreado)
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md` (não rastreado)
- `docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md` (não rastreado — histórico rejeitado)
- `docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md` (este relatório — não rastreado)

A correção do B-001 (label da linha 451) pode ocorrer neste commit ou em ciclo futuro,
a critério do usuário.

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
?? docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

### git diff --stat

```
 scripts/docs/NOMENCLATURA.md                        | 108 ++++++-
 scripts/docs/adr/INDICE_ADR.md                      |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md | 331 +++++++++++++++++++--
 scripts/docs/contratos/contrato_json_tela_minima.md |  40 ++-
 scripts/docs/contratos/contrato_tela_json.md        |  61 ++--
 5 files changed, 469 insertions(+), 72 deletions(-)
```

### git diff --name-only

```
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

### grep "3 vãos\|vãos iguais" contrato_composicao_corpo.md

```
485: > **Nota**: a formulação anterior de "3 vãos iguais" registrada neste contrato...
750: ...A regra anterior de "3 vãos iguais" está supersedida pela ADR-0015 e não deve ser implementada.
```

(Ambas referências históricas — não regras ativas.)

### grep "lado a lado\|layout lado" contrato_composicao_corpo.md

```
451: - **Combinação lado a lado + dashboard presente**: não definida — ver seção 9.
479: historicamente "lado a lado"): a regra é **particionamento contíguo** da
481: Molduras adjacentes ficam coladas, produzindo bordas lado a lado
```

(Nenhuma em contexto normativo ativo de regra.)

### grep "lado a lado\|layout lado" docs/NOMENCLATURA.md

```
(sem saída)
```

### grep "3 vãos\|vãos iguais" docs/NOMENCLATURA.md

```
950:  "3 vãos iguais" foi supersedida pela ADR-0015.
```

(Referência histórica supersedida.)

### grep "HANDOFF_READY" H-0019

```
(sem saída)
```

### grep "BLOCKED_BY_ADR_0015_PENDING_REVISION" H-0019

```
4:  status: BLOCKED_BY_ADR_0015_PENDING_REVISION
37: BLOCKED_BY_ADR_0015_PENDING_REVISION
```

### git status --short tela config

```
(sem saída)
```

### git diff --name-only — tela config

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
?? docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md
```
