# RELATORIO_APLICACAO_ADR-0019

## 1. Identificação

- ADR aplicada: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- Categoria processual executada: `APLICAR_ADR`
- Executor: agente de aplicação documental
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Evidências de entrada:
  - `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`
  - `docs/relatorios/RELATORIO_QA_ADR-0019.md`
  - `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md`

---

## 2. Objetivo

Propagar as sete decisões formais (D1–D7) da ADR-0019 nos documentos normativos do projeto,
tornando-as vigentes nos artefatos que definem as regras de composição hierárquica do corpo,
multiplicidade estrutural e cardinalidade de `dashboard`.

Limites estritos da etapa:

- apenas aplicação documental nos 8 arquivos permitidos;
- não implementar código;
- não fazer QA da própria aplicação;
- não criar handoff;
- não preparar commit;
- não fazer commit;
- não remover, mover, limpar ou adicionar ao stage os arquivos não rastreados existentes.

---

## 3. Estado Git inicial

Comandos executados a partir de `scripts/` (raiz efetiva; toplevel Git em
`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`).

```text
git rev-parse --show-toplevel
  /home/tiago/Dropbox/UFRGS/Survey/versao_0_1

git log --oneline -1
  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
  ?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
  ?? tela/__pycache__/

git diff --stat HEAD              (sem saída)
git diff --name-only HEAD         (sem saída)
git diff --cached --stat          (sem saída)
```

Estado confirmado: stage vazio, nenhuma alteração rastreada, quatro entradas não rastreadas
(ADR-0019, três relatórios, `tela/__pycache__/`). Coincide com o estado comprovado informado
pelo usuário.

---

## 4. Decisões a propagar

| ID | Decisão |
|---|---|
| D1 | Profundidade contada exclusivamente pelo aninhamento de nós estruturais `grupo` — o corpo raiz e listas `elementos[]` não são níveis |
| D2 | Profundidade máxima: 3 níveis de grupos |
| D3 | Elementos funcionais em grupo nível 3 não constituem nível 4 |
| D4 | Grupo filho de grupo nível 3 seria nível 4 — é estruturalmente inválido |
| D5 | Múltiplos grupos irmãos são permitidos em qualquer nível válido |
| D6 | Múltiplos elementos funcionais por grupo são permitidos em qualquer nível |
| D7 | Remoção da regra global "zero ou um `dashboard` por tela" |

---

## 5. Artefatos consultados (leitura, sem alteração)

| Arquivo | Propósito |
|---|---|
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | Fonte normativa das decisões D1–D7 |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Lida para identificar formulações de cardinalidade afetadas por D7 |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | Lida para verificar precedência e formulações |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | Lida para verificar definições de hierarquia e `grupo` |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | Lida para verificar ausência de impacto cruzado |
| `docs/adr/INDICE_ADR.md` | Lido para verificar formatação de entrada existente |
| `docs/NOMENCLATURA.md` | Lida para identificar formulações conflitantes com D1–D7 |
| `docs/contratos/contrato_composicao_corpo.md` | Lido para identificar todas as formulações afetadas por D1–D7 |
| `docs/contratos/contrato_tela_json.md` | Lido para identificar a seção de composição hierárquica afetada |
| `docs/contratos/contrato_json_tela_minima.md` | Lido para identificar a seção de `grupo` aninhado afetada |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md` | Lido para contexto de levantamento |
| `docs/relatorios/RELATORIO_QA_ADR-0019.md` | Lido para contexto de QA inicial |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md` | Lido para confirmar aprovação formal da ADR-0019 |

---

## 6. Arquivos permitidos para alteração

| Arquivo | Status |
|---|---|
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | permitido |
| `docs/adr/INDICE_ADR.md` | permitido |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | permitido |
| `docs/contratos/contrato_composicao_corpo.md` | permitido |
| `docs/contratos/contrato_tela_json.md` | permitido |
| `docs/contratos/contrato_json_tela_minima.md` | permitido |
| `docs/NOMENCLATURA.md` | permitido |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md` | permitido (este arquivo) |

Nenhum outro arquivo foi alterado.

---

## 7. Alterações executadas

### 7.1 `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`

| Campo alterado | Antes | Depois |
|---|---|---|
| Frontmatter `status` | `proposta` | `aceita` |
| Seção Status (corpo) | `\`proposta\`` | `\`aceita\`` |

Justificativa: a ADR foi aprovada formalmente no QA pós-patch; o status deve refletir a
aprovação antes da propagação para os demais documentos.

---

### 7.2 `docs/adr/INDICE_ADR.md`

Adicionada linha de entrada da ADR-0019:

```
| ADR-0019 | Profundidade contada por aninhamento de grupos, multiplicidade estrutural e
remoção da cardinalidade global de dashboard — D1: contagem por grupos; D2: máximo 3
níveis; D3: funcionais no nível 3 não são nível 4; D4: grupo no nível 4 é inválido; D5:
múltiplos grupos irmãos permitidos; D6: múltiplos funcionais por grupo permitidos; D7:
remoção da regra "zero ou um dashboard" | aceita | 2026-07-12 |
```

Decisões propagadas: D1, D2, D3, D4, D5, D6, D7 (todas, via registro de entrada).

---

### 7.3 `docs/adr/ADR-0007-tela-processamento-composicao.md`

Três edições:

**Edição 1 — Ponto 3 (cardinalidade de `dashboard` para telas de processamento):**
Substituída a formulação que implicava cardinalidade máxima de um `dashboard` pela nova
formulação que remove o limite global e referencia a ADR-0019 D7 (2026-07-12).

**Edição 2 — Nota de superação parcial (após ponto 10):**
Inserida nota explícita de que a ADR-0019 supera parcialmente a ADR-0007 exclusivamente
nas formulações de cardinalidade "zero ou um `dashboard`", identificando os pontos afetados
(ponto 3 e exemplo da seção Composição conceitual) e preservando os pontos 1, 2, 4–10
como vigentes sem alteração.

**Edição 3 — Seção "Composição conceitual" (item `dashboard` do exemplo):**
Substituído "`dashboard` (zero ou um)" por "`dashboard` (zero ou mais)" com referência à
ADR-0019 D7.

Decisões propagadas: D7.

---

### 7.4 `docs/contratos/contrato_composicao_corpo.md`

Quatro edições:

**Edição 1 — Tabela de tipos (seção 3.0), linha `dashboard`:**
Coluna de restrição atualizada para remover limite global de cardinalidade e referencing
ADR-0019 D7.

**Edição 2 — Seção 3.2, definição de `grupo` e "Nível":**
Substituída a definição de "Nível" (que contava `corpo.elementos[]` como nível 1, tornando
`grupo.elementos[]` nível 2 e proibindo nível 3) pela definição canônica de "Nível de
grupo" da ADR-0019 D1–D4, incluindo:
- corpo raiz não conta;
- nível de grupo 1 = `grupo` filho direto de `corpo.elementos[]`;
- nível de grupo 2 = `grupo` filho de grupo do nível 1;
- nível de grupo 3 = `grupo` filho de grupo do nível 2 (máximo);
- elementos funcionais em grupo nível 3 não constituem nível 4;
- grupo nível 4 é estruturalmente inválido;
- múltiplos grupos irmãos e múltiplos elementos funcionais por grupo são permitidos.

**Edição 3 — R-16:**
Atualizada a regra R-16 para "3 níveis de grupos" com referência à ADR-0019.

**Edição 4 — Critérios de validação (seção 8):**
Substituída a formulação "Estruturas com profundidade superior a 3 níveis" por "Estruturas
com grupo no nível 4 ou superior" com referência à ADR-0019 D3.

Decisões propagadas: D1, D2, D3, D4, D5, D6, D7.

---

### 7.5 `docs/contratos/contrato_tela_json.md`

Uma edição:

**Edição 1 — Seção 8, parágrafo "Composição hierárquica como árvore":**
Substituída a definição que usava `corpo.elementos[]` como nível 1 e proibia nível 4
(formulação ADR-0015 original) pela nova definição canônica com contagem por níveis de
grupos (ADR-0019), incluindo esclarecimento de que elementos funcionais no nível 3 não
constituem nível 4, múltiplos grupos irmãos e múltiplos elementos funcionais por grupo são
permitidos, e referências à ADR-0015 e ADR-0019.

Decisões propagadas: D1, D2, D3, D5, D6.

---

### 7.6 `docs/contratos/contrato_json_tela_minima.md`

Uma edição:

**Edição 1 — Seção 6.2, descrição de `grupo` aninhado:**
Substituída a descrição genérica "até nível 3" (que usava a contagem antiga de profundidade)
pela descrição explícita com os três níveis de grupos, a invalidade do nível 4, a
não-constituição de nível 4 por elementos funcionais no nível 3, e a permissão de múltiplos
grupos irmãos e múltiplos elementos funcionais por grupo. Referência a ADR-0019 D1–D6.

Decisões propagadas: D1, D2, D3, D4, D5, D6.

---

### 7.7 `docs/NOMENCLATURA.md`

Três edições:

**Edição 1 — Seção 2.1, primeiro item `dashboard`:**
Substituído "zero ou um `dashboard`, quando houver saída passiva formatada" por
"`dashboard` (zero ou mais), quando houver saída passiva formatada" com referência à
ADR-0019 D7.

**Edição 2 — Seção 2.1, exemplo conceitual:**
Substituído "zero ou um `dashboard` de estado agregado/resumo/progresso" por
"`dashboard` (zero ou mais) de estado agregado/resumo/progresso (ADR-0019, D7)".

**Edição 3 — Seção 14, pontos 2–5:**
Substituídos os quatro pontos que definiam a hierarquia com base em "Corpo raiz como nível
0 / Filhos diretos como nível 1 / Filhos de grupo como nível 2 / Nível 3 proibido" pelos
quatro pontos canônicos com a definição de "Nível de grupo" da ADR-0019:
- ponto 2: profundidade contada por níveis de grupos; corpo raiz não conta (D1);
- ponto 3: nível de grupo 1 = `grupo` filho direto de `corpo.elementos[]` (D1);
- ponto 4: nível de grupo 2 = `grupo` filho de grupo nível 1 (D1);
- ponto 5: nível de grupo 3 = profundidade máxima; grupo nível 4 = inválido; funcionais em
  nível 3 não constituem nível 4 (D2, D3).

Decisões propagadas: D1, D2, D3, D5, D6, D7.

---

## 8. Mapeamento decisão × artefato

| Decisão | Arquivos onde foi propagada |
|---|---|
| D1 (contagem por grupos) | INDICE_ADR, contrato_composicao_corpo, contrato_tela_json, contrato_json_tela_minima, NOMENCLATURA |
| D2 (máx. 3 níveis) | INDICE_ADR, contrato_composicao_corpo, contrato_tela_json, contrato_json_tela_minima, NOMENCLATURA |
| D3 (funcionais nível 3 ≠ nível 4) | INDICE_ADR, contrato_composicao_corpo, contrato_tela_json, contrato_json_tela_minima, NOMENCLATURA |
| D4 (grupo nível 4 inválido) | INDICE_ADR, contrato_composicao_corpo, contrato_json_tela_minima, NOMENCLATURA |
| D5 (múltiplos grupos irmãos) | INDICE_ADR, contrato_composicao_corpo, contrato_tela_json, contrato_json_tela_minima, NOMENCLATURA |
| D6 (múltiplos funcionais por grupo) | INDICE_ADR, contrato_composicao_corpo, contrato_tela_json, contrato_json_tela_minima, NOMENCLATURA |
| D7 (remoção da regra global de dashboard) | INDICE_ADR, ADR-0007 (3 edições), contrato_composicao_corpo, NOMENCLATURA (2 edições) |

---

## 9. Busca de resíduos

Busca executada em todos os arquivos alterados (exceto este relatório) com os padrões:

| Padrão | Resultado |
|---|---|
| `zero ou um.*dashboard` (excluindo referências à ADR-0019 ou D7) | 1 ocorrência — ADR-0007 linha 114, dentro da nota de superação (referência historiográfica legítima, não norma ativa) |
| `Corpo raiz como nível 0` | 0 ocorrências |
| `Filhos diretos do corpo como nível 1` | 0 ocorrências |
| `Filhos de grupo como nível 2` | 0 ocorrências |
| `Nível 3 proibido` | 0 ocorrências |
| `profundidade ≥ 3` | 0 ocorrências |
| `profundidade superior a 3 níveis` | 0 ocorrências |
| `nível 0` (referindo-se ao corpo) | 0 ocorrências |
| `Profundidade máxima: 3 níveis` (sem "de grupos") | 0 ocorrências |

**Avaliação do falso positivo da linha 114 do ADR-0007:** a ocorrência encontrada está
dentro da nota de superação inserida por esta aplicação, que cita a formulação antiga
explicitamente para identificar o que foi superado. Não constitui norma ativa.

Resultado da busca: **nenhum resíduo normativo ativo** detectado nos arquivos permitidos.

---

## 10. Arquivos não alterados

Os seguintes arquivos foram lidos mas não alterados, por decisão de escopo:

| Arquivo | Motivo |
|---|---|
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | ADR aceita; não contém formulações conflitantes com D1–D7 nos pontos lidos |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | ADR aceita; a nova definição de nível de grupo é compatível — ADR-0019 a refina, não a contradiz na essência |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ADR aceita; sem impacto cruzado com D1–D7 |
| Qualquer arquivo de código | Fora do escopo desta etapa |
| Qualquer outro arquivo em `docs/` | Fora do conjunto de arquivos permitidos |

---

## 11. Estado Git final

```text
git status --short
  M docs/NOMENCLATURA.md
  M docs/adr/ADR-0007-tela-processamento-composicao.md
  M docs/adr/INDICE_ADR.md
  M docs/contratos/contrato_composicao_corpo.md
  M docs/contratos/contrato_json_tela_minima.md
  M docs/contratos/contrato_tela_json.md
  ?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
  ?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
  ?? tela/__pycache__/

git diff --stat HEAD
  docs/NOMENCLATURA.md                        | 27 +++++++++------
  docs/adr/ADR-0007-tela-processamento-composicao.md | 15 ++++++--
  docs/adr/INDICE_ADR.md                      |  1 +
  docs/contratos/contrato_composicao_corpo.md | 40 ++++++++++++++--------
  docs/contratos/contrato_json_tela_minima.md |  7 +++-
  docs/contratos/contrato_tela_json.md        | 15 +++++---
  6 files changed, 72 insertions(+), 33 deletions(-)
```

Stage: vazio. Nenhum arquivo rastreado anteriormente foi excluído, movido ou adicionado ao
stage. Os arquivos não rastreados preexistentes permaneceram intactos.

---

## 12. Verificação de invariantes

| Invariante | Status |
|---|---|
| Apenas 8 arquivos permitidos foram alterados | ✅ — 7 arquivos normativos + este relatório |
| Nenhum arquivo de código foi tocado | ✅ |
| Nenhum arquivo não rastreado preexistente foi removido, movido ou adicionado ao stage | ✅ |
| Stage permanece vazio ao final | ✅ |
| ADR-0019 permanece como arquivo não rastreado (untracked) | ✅ |
| Nenhuma nova decisão foi introduzida além de D1–D7 | ✅ |
| Pontos 1, 2, 4–10 da ADR-0007 permanecem vigentes sem alteração | ✅ |
| ADR-0015 não foi contraditada — D1–D6 a refinam | ✅ |
| ADR-0018 não foi afetada | ✅ |

---

## 13. Conclusão

A aplicação documental da ADR-0019 foi concluída. Todas as sete decisões (D1–D7) foram
propagadas nos documentos normativos correspondentes dentro do conjunto de 8 arquivos
permitidos. Nenhum resíduo normativo ativo da formulação anterior foi detectado. O stage
permanece vazio e nenhum arquivo preexistente não rastreado foi perturbado.

A etapa `APLICAR_ADR` para a ADR-0019 está completa. As próximas etapas (QA desta
aplicação, commit, handoff de implementação) são responsabilidade de ciclos processuais
subsequentes distintos desta etapa.
