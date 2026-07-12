# RELATORIO_QA_POS_PATCH_H-0027_HANDOFF

Reauditoria do handoff H-0027 após o patch de correção de `ACH-001`.
Verificação curta e objetiva concentrada na resolução de `ACH-001` e na
ausência de regressão. Não repete integralmente o QA anterior
(`RELATORIO_QA_H-0027_HANDOFF.md`).

---

## 1. Identificação

- Artefato auditado: `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
- Categoria processual executada: `QA_HANDOFF` (reauditoria pós-patch)
- ADR base: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` (status `aceita`)
- Auditor: agente formal de QA do handoff H-0027 (pós-patch)
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Relatório de QA anterior: `docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md`
- Achado corrigido: `ACH-001` (justificativa factual inexata sobre `elemento_por_id`/`elementos_por_tipo`)

Limites estritos desta etapa:

- somente reauditar o handoff H-0027 quanto à resolução de `ACH-001`;
- somente verificar ausência de regressão nas áreas preservadas;
- somente produzir este relatório;
- não corrigir o handoff;
- não implementar código;
- não alterar testes, ADRs, contratos, nomenclatura ou índice;
- não preparar commit;
- não executar etapa posterior.

---

## 2. Estado Git inicial

Comandos executados a partir de `scripts/` (raiz efetiva dos caminhos declarados
na documentação; toplevel Git em `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`).

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 27 +++++++++------
 .../adr/ADR-0007-tela-processamento-composicao.md  | 15 ++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 40 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    |  7 +++-
 scripts/docs/contratos/contrato_tela_json.md       | 15 +++++---
 6 files changed, 72 insertions(+), 33 deletions(-)

git diff --name-only
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/ADR-0007-tela-processamento-composicao.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md

git diff --check
(sem saída)

git diff --cached --stat
(sem saída)

git diff --cached --name-only
(sem saída)
```

Observações:

- stage vazio — confirmado (`git diff --cached --stat` sem saída);
- commit-base `40015b6` — confirmado (`git log -1 --oneline`);
- o handoff H-0027 permanece **não rastreado** (`?? docs/handoff/H-0027-...`),
  como esperado para arquivo recém-criado; `git diff` vazio sobre rastreados não
  é usado como prova de sua existência ou conteúdo;
- nenhuma alteração rastreada em `tela/*.py`;
- o patch de `ACH-001` foi aplicado ao handoff (edição em arquivo não rastreado),
  sem alterar arquivos rastreados nem o stage.

---

## 3. Verificação de ACH-001

### 3.1 Texto pós-patch da seção 14.2 (linhas 448–466)

Leitura direta do handoff após o patch:

```text
### 14.2 Métodos `elemento_por_id` e `elementos_por_tipo`

Esses métodos permanecem com semântica **plana**: percorrem somente
`self.corpo.elementos` diretos, sem descer na árvore de grupos.

Os contratos ativos e as docstrings atuais não definem se essas buscas devem
ser planas ou recursivas. A implementação existente percorre somente
`self.corpo.elementos`, e o H-0027 deve preservar esse comportamento
observável para não ampliar implicitamente a API pública. O renderizador não
usa esses métodos (acessa `modelo.corpo.elementos` diretamente). A árvore
hierárquica deve ser preservada integralmente no modelo por meio de
`ElementoCorpo.elementos`, sem obrigar esses dois métodos a percorrê-la
recursivamente neste ciclo. Caso a implementação edite o corpo desses métodos
ou a área correspondente em `tela/modelo.py`, as docstrings devem ser
atualizadas para declarar explicitamente o escopo plano preservado: elementos
dentro de grupos são acessíveis via navegação direta da árvore
(`elemento.elementos`), não por esses métodos. Busca recursiva pública,
alteração da semântica desses métodos ou criação de API recursiva permanecem
fora do escopo do H-0027 e dependem de decisão e documentação próprias.
```

### 3.2 Confirmação dos sete requisitos exigidos

| # | Requisito (roteiro) | Evidência pós-patch | Confirmado |
| --- | --- | --- | --- |
| 1 | Contratos e docstrings atuais não definem se devem ser planos ou recursivos | H-0027:453-454 "Os contratos ativos e as docstrings atuais não definem se essas buscas devem ser planas ou recursivas" | SIM |
| 2 | Implementação atual percorre somente `self.corpo.elementos` | H-0027:454-455 "A implementação existente percorre somente `self.corpo.elementos`"; confirmado em `tela/modelo.py:90-106` (`elemento_por_id` itera `self.corpo.elementos`; `elementos_por_tipo` filtra `self.corpo.elementos`) | SIM |
| 3 | O H-0027 preserva esse comportamento público observável | H-0027:455-456 "o H-0027 deve preservar esse comportamento observável para não ampliar implicitamente a API pública" | SIM |
| 4 | A árvore completa continua representada por `ElementoCorpo.elementos` | H-0027:457-459 "A árvore hierárquica deve ser preservada integralmente no modelo por meio de `ElementoCorpo.elementos`"; coerente com seção 14.1 (H-0027:429-446) e 14.3 (H-0027:468-473) | SIM |
| 5 | Os dois métodos públicos não precisam percorrer a árvore recursivamente neste ciclo | H-0027:459-460 "sem obrigar esses dois métodos a percorrê-la recursivamente neste ciclo" | SIM |
| 6 | Se o executor editar esses métodos ou a área correspondente, as docstrings deverão explicitar o escopo plano | H-0027:460-464 "Caso a implementação edite o corpo desses métodos ou a área correspondente em `tela/modelo.py`, as docstrings devem ser atualizadas para declarar explicitamente o escopo plano preservado" | SIM |
| 7 | Busca recursiva pública, alteração da semântica ou criação de nova API recursiva permanecem fora do escopo | H-0027:464-466 "Busca recursiva pública, alteração da semântica desses métodos ou criação de API recursiva permanecem fora do escopo do H-0027 e dependem de decisão e documentação próprias" | SIM |

Os sete requisitos estão integralmente atendidos.

### 3.3 Remoção da afirmação inexata

A afirmação inexata anterior — "sua documentação diz explicitamente que operam
sobre `self.corpo.elementos`" — foi **removida**. Confirmação por busca direta:

- `grep -n "diz explicitamente" docs/handoff/H-0027-...` não retorna ocorrência
  na seção 14.2;
- a redação atual substitui a premissa falsa pela afirmação correta de que
  "Os contratos ativos e as docstrings atuais não definem se essas buscas devem
  ser planas ou recursivas" (H-0027:453-454), confirmada pela inspeção das
  docstrings reais em `tela/modelo.py:90-106` (nenhuma explicita o escopo de
  busca) e pela ausência de definição contratual (`docs/contratos/` não menciona
  `elemento_por_id` nem `elementos_por_tipo`).

### 3.4 Classificação de ACH-001

```text
ACH-001: RESOLVIDO
```

A seção 14.2 agora (a) declara corretamente que contratos e docstrings não
definem o escopo; (b) descreve fielmente o comportamento atual plano; (c)
preserva o comportamento observável; (d) confirma a árvore integral em
`ElementoCorpo.elementos`; (e) dispensa recursão nestes métodos neste ciclo;
(f) exige docstring explícita condicional à edição da área; (g) exclui do
escopo busca recursiva/alteração de semântica/nova API recursiva. A afirmação
inexata foi removida.

---

## 4. Verificação de regressão

Verificação concentrada nos elementos preservados pelo patch. Não reauditoria
detalhada de áreas já classificadas como SUFICIENTE no QA anterior, salvo se o
patch as alterou — o patch alterou **somente** a seção 14.2.

| Área | Estado pós-patch | Evidência | Regressão? |
| --- | --- | --- | --- |
| D1–D7 | Intactas | H-0027:154-161 (tabela D1–D7 idêntica à do QA anterior) | NÃO |
| Construção recursiva da árvore no modelo (14.1) | Intacta | H-0027:429-446 (substituição de `_construir_elementos_internos_grupo` por função recursiva; `_campos_inertes` preserva `arranjo`/`distribuicao`) | NÃO |
| Loader recursivo (seção 13) | Intacto | H-0027:366-423 (validação recursiva, níveis 1–3, nível 4 inválido, modos, associação a filhos diretos, ausência de limite global de dashboards, diagnóstico determinístico) | NÃO |
| Renderizador recursivo (seção 15) | Intacto | H-0027:469-559 (composição recursiva por container, verticais/horizontais, combinações, distribuição por filhos diretos, ausência preservada, múltiplos dashboards, grupo sem moldura) | NÃO |
| Arquivos permitidos (seção 8) | Intactos | H-0027:258-274 (os sete `tela/*.py` + IMP-0028 + `config/telas/` para novas fixtures) | NÃO |
| Arquivos proibidos (seção 9) | Intactos | H-0027:278-292 (ADRs, contratos, NOMENCLATURA, handoffs, relatórios exceto IMP-0028, 4 JSONs ativos) | NÃO |
| Testes obrigatórios (seção 20) | Intactos | H-0027:664-734 (substituir não remover; cobertura de níveis, irmãos, funcionais, arranjos, distribuições, vetores inválidos, múltiplos dashboards, regressões) | NÃO |
| Critérios de aceite (seção 19) | Intactos | H-0027:645-652 (suítes em código 0, `git diff --check`, cobertura da seção 18, IMP-0028, stage vazio) | NÃO |
| Relatório IMP-0028 (seção 22) | Intacto | H-0027:756-786 (conteúdo obrigatório: arquivos, camadas, profundidade, multiplicidade, dashboards, testes, comandos, preservações, limitações, Git, bloqueios) | NÃO |
| Condições de bloqueio (seção 23) | Intactas | H-0027:790-804 (`BLOCKED_REPOSITORY_STATE`, `ARCHITECTURE_REVIEW_REQUIRED`, `BLOCKED_SCOPE`) | NÃO |
| Proibição de implementação e commit (seções 24, 25) | Intacta | H-0027:808-827 (executor não cria commit; limites de encerramento) | NÃO |
| Limitação documentada de `elemento_por_id`/`elementos_por_tipo` em teste e relatório | Preservada | H-0027:709 (teste `elemento_por_id`/`elementos_por_tipo` permanecem planos); H-0027:779-780 (IMP-0028 item 14 — limitação documentada, não bug) | NÃO |

Não houve regressão. O patch foi cirúrgico na seção 14.2 e preservou todas as
demais seções auditadas.

---

## 5. Achados novos

Nenhum achado novo foi identificado nesta reauditoria.

### 5.1 Observações anteriores reavaliadas

`OBS-001` (divergência de status da ADR-0018, pendência documental conhecida),
`OBS-002` (permissão de `tela/teste_demo.py` sem justificativa explícita) e
`OBS-003` (política de diagnóstico conforme ADR-0019 D4) não exigiam correção e
**não se tornaram defeito após o patch** — o patch não tocou nenhuma das áreas
relacionadas a essas observações.

---

## 6. Conclusão

O patch de `ACH-001` corrigiu integralmente a justificativa factual da seção
14.2 do handoff H-0027, atendendo aos sete requisitos exigidos pelo roteiro e
removendo a afirmação inexata anterior. A nova redação é fiel às autoridades
(ausência de definição contratual; docstrings omissas quanto ao escopo;
ausência de uso pelo renderizador) e compatível com `H-0002` (métodos
auxiliares somente leitura) e com o escopo permitido (`tela/modelo.py` na lista
da seção 8).

O patch foi cirúrgico: não alterou nenhuma outra seção do handoff, nenhum
arquivo rastreado, nenhum arquivo normativo, nenhum teste, e não preparou
commit. As decisões D1–D7, a construção recursiva do modelo, as validações
recursivas do loader, a composição recursiva do renderizador, os arquivos
permitidos e proibidos, os testes obrigatórios, os critérios de aceite, o
relatório IMP-0028, as condições de bloqueio e a proibição de implementação e
commit permanecem intactos. Não houve regressão.

Não há nova decisão do usuário necessária. Não há novo defeito que exija
correção. As observações anteriores permanecem como observações (não bloqueantes).

---

## 7. Status final

```text
H1_HANDOFF_APPROVED
```

Justificativa: `ACH-001` está **RESOLVIDO**; **não há regressão**; **não há nova
decisão necessária**; **não há novo defeito que exija correção**. O handoff
H-0027, em seu estado pós-patch, está aprovado para a próxima categoria
processual.

### 7.1 Matriz de achados (pós-patch)

| Achado  | Evidência pós-patch | Resultado |
| ------- | ------------------- | --------- |
| ACH-001 | `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md:448-466` (seção 14.2 reescrita) | RESOLVIDO |

---

## 8. Estado Git final

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 27 +++++++++------
 .../adr/ADR-0007-tela-processamento-composicao.md  | 15 ++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 40 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    |  7 +++-
 scripts/docs/contratos/contrato_tela_json.md       | 15 +++++---
 6 files changed, 72 insertions(+), 33 deletions(-)

git diff --name-only
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/ADR-0007-tela-processamento-composicao.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md

git diff --check
(sem saída)

git diff --cached --stat
(sem saída)

git diff --cached --name-only
(sem saída)
```

O único novo arquivo criado nesta auditoria é
`docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md` (este relatório,
não rastreado). Nenhum arquivo rastreado foi alterado. O handoff H-0027, a
ADR-0019, os relatórios do ciclo e `tela/__pycache__/` permanecem não
rastreados, sem alteração, remoção, movimentação ou stage. Stage permanece
vazio ao final.
