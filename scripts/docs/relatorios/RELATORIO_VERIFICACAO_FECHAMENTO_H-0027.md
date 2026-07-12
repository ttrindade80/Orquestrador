# RELATORIO_VERIFICACAO_FECHAMENTO_H-0027

## 1. Identificação

- Ciclo: H-0027
- Categoria executada: `VERIFICAR_FECHAMENTO`
- Verificador: agente formal de fechamento
- Data: 2026-07-12
- Branch: `master`
- Commit-base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Relatório de QA final da implementação: `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`

---

## 2. Objetivo

Verificar se todos os artefatos, aprovações, testes, arquivos alterados, arquivos não rastreados e condições processuais do ciclo H-0027 estão completos, coerentes e prontos para preparação de commit. Este relatório não corrige artefatos, não altera código, não modifica testes, não adiciona arquivos ao stage e não executa commit.

---

## 3. Estado Git inicial

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git branch --show-current
master

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                                  |  27 +-
 scripts/docs/adr/ADR-0007-tela-processamento-composicao.md    |  15 +-
 scripts/docs/adr/INDICE_ADR.md                                |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md           |  40 +-
 scripts/docs/contratos/contrato_json_tela_minima.md           |   7 +-
 scripts/docs/contratos/contrato_tela_json.md                  |  15 +-
 scripts/tela/loader.py                                        | 165 +++---
 scripts/tela/modelo.py                                        | 106 ++--
 scripts/tela/renderizador.py                                  | 297 ++++++----
 scripts/tela/teste_loader.py                                  | 460 +++++++++++++--
 scripts/tela/teste_modelo.py                                  | 185 ++++++
 scripts/tela/teste_renderizador.py                            | 621 +++++++++++++++++++++
 12 files changed, 1669 insertions(+), 270 deletions(-)

git diff --check
(sem saída — código de saída 0)

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)
```

---

## 4. Artefatos do fluxo documental

### 4.1 Levantamento

**Arquivo:** `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`

- Existe: **sim**
- Commit-base registrado: `40015b6` — correto
- Status final declarado: `L3_DECISAO_DO_USUARIO_E_ADR_NECESSARIAS`
- Conclusão: identificou ambiguidade normativa sobre profundidade de grupos e cardinalidade de dashboards; classificou necessidade de decisão do usuário e criação de ADR. Confirma fluxo documental que originou ADR-0019.

### 4.2 ADR-0019

**Arquivo:** `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`

- Existe: **sim** (não rastreado — novo artefato do ciclo)
- Status no frontmatter: `aceita`
- Status no corpo: `aceita`
- Data: 2026-07-12
- Decisões D1–D7: presentes
- Contratos afetados declarados: `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `NOMENCLATURA.md`, `INDICE_ADR.md`, `ADR-0007-tela-processamento-composicao.md`
- Coerência: ADR não aplicou alterações aos documentos normativas — delega para etapa `APLICAR_ADR`. Correto.

### 4.3 QA inicial da ADR-0019

**Arquivo:** `docs/relatorios/RELATORIO_QA_ADR-0019.md`

- Existe: **sim** (não rastreado)
- Commit-base: `40015b6` — correto
- Status final: `ADR_REJECTED`
- Achados identificados: QA-001 a QA-004 (defeitos na ADR)
- Conclusão: rejeição legítima; exigiu patch da ADR antes da aprovação.

### 4.4 QA pós-patch da ADR-0019

**Arquivo:** `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md`

- Existe: **sim** (não rastreado)
- QA anterior referenciado: `RELATORIO_QA_ADR-0019.md` (`ADR_REJECTED`) — correto
- Status final: `ADR_APPROVED`
- Status da ADR auditada: `aceita` (frontmatter e corpo)
- QA-001 a QA-004: todos resolvidos
- Conclusão: aprovação formalmente documentada.

### 4.5 Aplicação documental da ADR-0019

**Arquivo:** `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md`

- Existe: **sim** (não rastreado)
- Evidências de entrada listadas: levantamento, QA inicial, QA pós-patch — correto
- Escopo: propagação de D1–D7 nos 6 documentos normativos
- Conclusão: aplicação documental concluída; não implementou código, não criou handoff.

### 4.6 QA da aplicação documental (reexecução)

**Arquivo:** `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md`

- Existe: **sim** (não rastreado)
- Commit-base: `40015b6` — correto
- Status final: `ADR_APPLICATION_APPROVED_WITH_NOTES`
- Nota registrada: divergência histórica de status da ADR-0018 (frontmatter `proposta` × índice `aceita`); a aplicação da ADR-0019 não alterou o arquivo nem o status da ADR-0018. Classificada como pendência documental separada, sem bloquear esta QA.
- Sem correção documental necessária nesta QA.
- Status da ADR-0018: **não alterado** neste ciclo (confirmado: `git diff --name-only` não inclui `ADR-0018`).

### 4.7 Tentativa interrompida `RELATORIO_QA_APLICACAO_ADR-0019.md`

**Arquivo:** `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019.md`

- Existe: **não**
- Conclusão: nenhuma evidência de tentativa interrompida sem identificação; o ciclo transitou diretamente para a reexecução. Sem risco de interpretação conflitante.

---

## 5. Artefatos do handoff

### 5.1 Handoff H-0027

**Arquivo:** `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`

- Existe: **sim** (não rastreado)
- Status declarado: `proposto`
- ADR de origem: ADR-0019 (`aceita`) — referenciada corretamente
- Scope negativo inclui: correção da divergência de status da ADR-0018
- Não autoaprova: status `proposto`, sem classificação de QA.

### 5.2 QA inicial do handoff

**Arquivo:** `docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md`

- Existe: **sim** (não rastreado)
- Status final: `H2_HANDOFF_PATCH_REQUIRED`
- Achados registrados: OBS-001 (divergência ADR-0018, pendência conhecida); achados que exigiram patch
- Não cria IMP-0028, não implementa, não aprova a si próprio.

### 5.3 QA pós-patch do handoff

**Arquivo:** `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md`

- Existe: **sim** (não rastreado)
- Classificação anterior referenciada: `H2_HANDOFF_PATCH_REQUIRED` — correto
- Status final: `H1_HANDOFF_APPROVED`
- OBS-001 (divergência ADR-0018): mantida como pendência documental conhecida, sem bloquear aprovação do handoff.

---

## 6. Artefatos da implementação

### 6.1 IMP-0028

**Arquivo:** `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`

- Existe: **sim** (não rastreado)
- Handoff implementado: H-0027 — declarado
- Autoridades: ADR-0019, ADR-0015, contratos — declaradas
- Estado Git inicial: seção 2 — presente com saída dos comandos exigidos
- Estado Git final: seção 8 — presente com saída dos comandos exigidos
- Arquivos alterados: seção 3 — tabela presente
- Implementação do loader: seção 5.1 — presente
- Implementação do modelo: seção 5.2 — presente
- Implementação do renderizador: seção 5.3 — presente
- D1–D7: seção 4 — todos cobertos
- Métodos públicos planos: `elemento_por_id` e `elementos_por_tipo` com escopo plano — documentados
- Testes iniciais: seção 6 — presentes
- Achados do QA (ACH-001 a ACH-006): referenciados e resolvidos pelo patch
- Patch: descrito nas seções de cada módulo e na seção de testes
- Testes pós-patch: tabela "Resultados finais pós-patch" — presente
- Resultado de `teste_demo.py`: 303/303, código 0 — registrado (seção 6)
- Bloqueios: seção 9 — nenhum encontrado
- Autoaprovação: **ausente** (status declarado: `IMPLEMENTADO (patch aplicado — aguarda QA_POS_PATCH)`; nenhuma classificação reservada ao QA usada).

### 6.2 QA inicial da implementação

**Arquivo:** `docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md`

- Existe: **sim** (não rastreado)
- Status final: `I2_IMPLEMENTATION_PATCH_REQUIRED`
- Achados: ACH-001 a ACH-006 identificados e descritos
- IMP-0028 referenciado: não aprova a si próprio — confirmado

### 6.3 QA pós-patch da implementação

**Arquivo:** `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`

- Existe: **sim** (não rastreado)
- Classificação anterior referenciada: `I2_IMPLEMENTATION_PATCH_REQUIRED` — correto
- ACH-001: RESOLVIDO (3 métodos novos em `teste_renderizador.py`; 491/491 incluindo 24 verificações ACH-001a/b/c)
- ACH-002: RESOLVIDO (IMP-0028 registra `teste_demo.py` 303/303, total 1004/1004)
- ACH-003: RESOLVIDO (IMP-0028 contém seções 2 e 8 com saída dos comandos Git exigidos)
- ACH-004: RESOLVIDO (IMP-0028 seção 9 declara ausência de bloqueios)
- ACH-005: RESOLVIDO (`_validar_distribuicao_corpo` parametrizada com `prefixo_caminho`; 2 verificações no `teste_loader.py`)
- ACH-006: RESOLVIDO (comentário de `_montar_corpo_horizontal` reescrito)
- Achado novo: nenhum
- Regressão: nenhuma
- Validação manual em TTY real: **não necessária** (confirmado em linhas 522, 579, 592)
- Status final: `I1_IMPLEMENTATION_APPROVED`

---

## 7. Sequência de status

```text
L3_DECISAO_DO_USUARIO_E_ADR_NECESSARIAS   (levantamento)
→ ADR-0019 criada (status: proposta)
→ ADR_REJECTED                             (QA inicial da ADR)
→ patch da ADR
→ ADR_APPROVED                             (QA pós-patch da ADR; ADR: aceita)
→ aplicação documental concluída
→ ADR_APPLICATION_APPROVED_WITH_NOTES     (QA da aplicação — reexecução)
→ H-0027 criado (status: proposto)
→ H2_HANDOFF_PATCH_REQUIRED               (QA inicial do handoff)
→ patch do handoff
→ H1_HANDOFF_APPROVED                     (QA pós-patch do handoff)
→ implementação executada (IMP-0028 criado)
→ I2_IMPLEMENTATION_PATCH_REQUIRED        (QA inicial da implementação)
→ patch da implementação
→ I1_IMPLEMENTATION_APPROVED              (QA pós-patch da implementação)
```

Nenhum relatório intermediário foi sobrescrito. A sequência está íntegra.

---

## 8. Testes e validação manual

### 8.1 Reexecução dos testes

```text
python tela/teste_loader.py
  Total de verificacoes: 129 | Passaram: 129 | Falharam: 0
  Código de saída: 0

python tela/teste_modelo.py
  Total de verificacoes: 81 | Passaram: 81 | Falharam: 0
  Código de saída: 0

python tela/teste_renderizador.py
  Total de verificacoes: 491 | Passaram: 491 | Falharam: 0
  Código de saída: 0

python tela/teste_demo.py
  Total de verificacoes: 303 | Passaram: 303 | Falharam: 0
  Código de saída: 0

Total geral: 1004 verificações | Passaram: 1004 | Falharam: 0

git diff --check
  (sem saída — código de saída 0)
```

### 8.2 Correspondência com QA formal

Os resultados correspondem exatamente aos declarados no `RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`:
- loader: 129/129 ✅
- modelo: 81/81 ✅
- renderizador: 491/491 ✅
- demo: 303/303 ✅
- total: 1004/1004 ✅
- `git diff --check`: código 0 ✅

### 8.3 Validação manual em TTY real

Classificada como não necessária pelo QA final (`RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`, linhas 522, 579, 592). Nenhum relatório posterior reintroduziu pendência manual.

---

## 9. Arquivos rastreados alterados

Todos 12 arquivos rastreados modificados pertencem ao ciclo H-0027. Nenhum arquivo rastreado foi adicionado ao stage.

| Arquivo | Categoria | Pertence ao ciclo |
|---|---|---|
| `docs/NOMENCLATURA.md` | Aplicação documental ADR-0019 | sim |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Aplicação documental ADR-0019 | sim |
| `docs/adr/INDICE_ADR.md` | Aplicação documental ADR-0019 | sim |
| `docs/contratos/contrato_composicao_corpo.md` | Aplicação documental ADR-0019 | sim |
| `docs/contratos/contrato_json_tela_minima.md` | Aplicação documental ADR-0019 | sim |
| `docs/contratos/contrato_tela_json.md` | Aplicação documental ADR-0019 | sim |
| `tela/loader.py` | Implementação H-0027 (inicial + patch ACH-005) | sim |
| `tela/modelo.py` | Implementação H-0027 (inicial) | sim |
| `tela/renderizador.py` | Implementação H-0027 (inicial + patch ACH-006) | sim |
| `tela/teste_loader.py` | Implementação H-0027 (inicial + patch ACH-005) | sim |
| `tela/teste_modelo.py` | Implementação H-0027 (inicial) | sim |
| `tela/teste_renderizador.py` | Implementação H-0027 (inicial + patch ACH-001) | sim |

**`tela/teste_demo.py`**: existe, não modificado neste ciclo (não aparece em `git diff --name-only`); já rastreado de ciclo anterior; apenas executado para validação.

---

## 10. Arquivos não rastreados do ciclo

| Arquivo | Tipo |
|---|---|
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | ADR nova |
| `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` | Handoff |
| `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` | Relatório de implementação |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md` | Relatório de aplicação documental |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md` | Relatório de levantamento |
| `docs/relatorios/RELATORIO_QA_ADR-0019.md` | QA inicial ADR |
| `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` | QA da aplicação documental |
| `docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md` | QA inicial do handoff |
| `docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md` | QA inicial da implementação |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md` | QA pós-patch da ADR |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md` | QA pós-patch do handoff |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` | QA pós-patch da implementação |
| `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` | Este relatório (criado nesta verificação) |

Total de arquivos não rastreados do ciclo: 13 (12 pré-existentes + este relatório).

---

## 11. Caches e temporários

| Item | Status | Ação necessária |
|---|---|---|
| `tela/__pycache__/` | não rastreado; pré-existente desde o início do ciclo | não integrar ao commit |

Nenhum outro cache, log casual, backup ou temporário identificado. `tela/__pycache__/` deve permanecer fora do stage no `PREPARAR_COMMIT`.

---

## 12. Verificação de escopo

### 12.1 Fixtures em `config/telas/`

Arquivos presentes: `destino_minimo.json`, `grupo_minimo.json`, `orquestrador.json`, `stub_b.json`.

Nenhuma fixture nova foi criada neste ciclo. Nenhum JSON ativo foi substituído ou alterado (`git diff --name-only` não inclui arquivos de `config/`).

### 12.2 ADR-0018

Não alterada neste ciclo: não aparece em `git diff --name-only`. A divergência de status (frontmatter `proposta` × índice `aceita`) é pendência documental separada, registrada como tal na `RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` e no QA final do handoff (OBS-001). Não bloqueia este fechamento.

### 12.3 Arquivos fora do escopo

Nenhum arquivo fora do escopo identificado. Os 12 arquivos rastreados e os 12 artefatos não rastreados pertencem integralmente ao ciclo H-0027.

---

## 13. Capacidade consolidada

Baseada no handoff H-0027, IMP-0028 e QA final:

| Capacidade | Status |
|---|---|
| Profundidade contada exclusivamente por nós `grupo` (não por `elementos[]`) | entregue |
| Máximo de 3 níveis de grupos | entregue |
| Grupo no nível 4 rejeitado com `TelaGrupoInvalido` e mensagem determinística contendo id, caminho e referência a ADR-0019 D4 | entregue |
| Múltiplos grupos irmãos em qualquer nível | entregue |
| Múltiplos elementos funcionais por grupo, incluindo no nível 3 | entregue |
| Grupos verticais (`arranjo: vertical`) e horizontais (`arranjo: horizontal`, `lado_a_lado`, `sobreposto`) | entregue |
| Combinações de arranjo entre níveis (ex: v→h→v, h→v→h) | entregue |
| Distribuição por container (raiz e grupos) | entregue |
| Modos `igual`, `percentual` e `fracao` | entregue |
| Remoção da restrição global de dashboards: múltiplos dashboards por tela | entregue |
| Árvore recursiva preservada no modelo (`_construir_elementos_recursivo`) | entregue |
| Métodos públicos de busca mantidos planos (`elemento_por_id`, `elementos_por_tipo`) | entregue |
| Regressões anteriores preservadas | entregue (1004/1004) |

---

## 14. Pendências e bloqueios

| Item | Status |
|---|---|
| Achados ACH-001 a ACH-006 | todos resolvidos |
| Achado novo | nenhum |
| Regressão | nenhuma |
| Validação manual pendente | nenhuma |
| Arquivo fora do escopo | nenhum |
| Correção adicional necessária | nenhuma |
| Decisão do usuário pendente | nenhuma |
| Stage com conteúdo inesperado | não — stage vazio |
| Artefato faltante | nenhum |
| Artefato com status conflitante | nenhum |

Pendência documental separada (não bloqueia este fechamento): divergência de status da ADR-0018 entre frontmatter (`proposta`) e índice (`aceita`). Registrada em OBS-001 do QA do handoff e na nota da QA da aplicação documental.

---

## 15. Mensagem de commit sugerida

```text
feat: implementa composicao hierarquica do corpo com tres niveis de grupos
```

A mensagem abrange:
- composição hierárquica como capacidade entregue;
- três níveis de grupos como limite formal (ADR-0019 D2);
- sem enumerar todos os detalhes (D1–D7, modos de distribuição, multiplicidade estrutural, cardinalidade de dashboard).

---

## 16. Conclusão

Todos os artefatos obrigatórios do ciclo H-0027 existem, têm conteúdo mínimo verificado e statuses finais aprovados. A sequência processual está íntegra e sem sobrescrita. Os testes executados nesta verificação confirmam 1004/1004 com código de saída 0 em todos os módulos. O `git diff --check` está limpo. O stage está vazio. Não há arquivo fora do escopo, fixture nova não justificada, validação manual pendente, decisão do usuário aberta ou bloqueio de qualquer natureza.

---

## 17. Status final

```text
CLOSURE_READY_FOR_COMMIT_PREPARATION
```

---

## 18. Próxima categoria permitida

`PREPARAR_COMMIT`

Esta verificação não executa `PREPARAR_COMMIT`. A execução é responsabilidade do gerente em prompt separado.

---

## 19. Estado Git final

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git branch --show-current
master

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md
?? tela/__pycache__/

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)

git diff --check
(sem saída — código de saída 0)
```

O único arquivo novo em relação ao estado Git inicial é `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` (este relatório), adicionado como não rastreado.
