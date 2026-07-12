# RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO

## 1. Identificacao

- Categoria executada: `QA_APLICACAO_ADR`
- ADR auditada: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- Aplicacao auditada: `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md`
- Data: 2026-07-12
- Auditoria formal independente, sem correcao documental.

## 2. Estado Git inicial

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
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
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
(sem saida)

git diff --cached --stat
(sem saida)

git diff --cached --name-only
(sem saida)
```

## 3. Arquivos consultados

Leitura integral:

- `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md`

Leitura das secoes alteradas e contexto necessario:

- `docs/adr/ADR-0007-tela-processamento-composicao.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` para confirmar ausencia de alteracao indevida de status.

## 4. Matriz D1-D7

| Decisão | Evidência principal | Resultado |
| ------- | ------------------- | --------- |
| D1 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:104`, `docs/contratos/contrato_composicao_corpo.md:134`, `docs/contratos/contrato_tela_json.md:194`, `docs/NOMENCLATURA.md:1149` | APLICADA |
| D2 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:135`, `docs/contratos/contrato_composicao_corpo.md:140`, `docs/contratos/contrato_tela_json.md:199`, `docs/NOMENCLATURA.md:1156` | APLICADA |
| D3 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:150`, `docs/contratos/contrato_composicao_corpo.md:141`, `docs/contratos/contrato_json_tela_minima.md:192`, `docs/NOMENCLATURA.md:1159` | APLICADA |
| D4 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:164`, `docs/contratos/contrato_composicao_corpo.md:143`, `docs/contratos/contrato_json_tela_minima.md:191`, `docs/contratos/contrato_composicao_corpo.md:946` | APLICADA |
| D5 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:175`, `docs/contratos/contrato_composicao_corpo.md:131`, `docs/contratos/contrato_tela_json.md:202`, `docs/contratos/contrato_json_tela_minima.md:193` | APLICADA |
| D6 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:188`, `docs/contratos/contrato_composicao_corpo.md:131`, `docs/contratos/contrato_tela_json.md:202`, `docs/contratos/contrato_json_tela_minima.md:193` | APLICADA |
| D7 | `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:209`, `docs/adr/ADR-0007-tela-processamento-composicao.md:68`, `docs/contratos/contrato_composicao_corpo.md:85`, `docs/NOMENCLATURA.md:235` | APLICADA |

## 5. Verificacao de ADR-0007, indice, contratos e nomenclatura

- ADR-0019: status coerente entre frontmatter e corpo: `aceita` em `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md:6` e `:24`.
- Indice: entrada unica da ADR-0019 em `docs/adr/INDICE_ADR.md:49`, com status `aceita`, data correta e resumo das D1-D7.
- ADR-0018: sem diff no arquivo `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`; a aplicacao nao alterou seu status.
- ADR-0007: telas de processamento admitem `dashboard` zero ou mais e sem limite global em `docs/adr/ADR-0007-tela-processamento-composicao.md:68`; a expressao antiga aparece apenas em nota de superacao em `:113`; demais pontos 1, 2, 4-10 preservados em `:113`.
- Contrato de composicao: define nivel de grupo, exclui corpo raiz da contagem, permite tres niveis, invalida nivel 4, permite funcionais no nivel 3, grupos irmaos e multiplos funcionais em `docs/contratos/contrato_composicao_corpo.md:129`, `:134`, `:140`, `:141`, `:143`; remove limite global de dashboard em `:85`.
- Contratos JSON: `docs/contratos/contrato_tela_json.md:194` e `docs/contratos/contrato_json_tela_minima.md:187` registram ate tres niveis de grupos, funcionais no nivel 3, grupo nivel 4 invalido, multiplicidade estrutural e funcional. Nao ha campos novos inventados nem obrigacao de tres niveis em toda tela; a forma plana permanece valida em `docs/contratos/contrato_tela_json.md:201`.
- Nomenclatura: removeu a norma ativa antiga de corpo raiz como nivel 0, nivel 3 proibido e profundidade antiga; a contagem vigente esta em `docs/NOMENCLATURA.md:1149`. Dashboard zero ou mais aparece em `docs/NOMENCLATURA.md:235` e `:249`.

## 6. Busca de residuos

Busca executada apenas nos documentos normativos alterados:

```text
docs/NOMENCLATURA.md
docs/adr/ADR-0007-tela-processamento-composicao.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
```

| Padrao | Ocorrencia | Classificacao |
| ------ | ---------- | ------------- |
| `zero ou um dashboard` | `docs/adr/INDICE_ADR.md:49` | NORMATIVA_COMPATIVEL |
| `zero ou um \`dashboard\`` | `docs/adr/ADR-0007-tela-processamento-composicao.md:114` | HISTORICA |
| `Nível 3 proibido` | nenhuma | NAO_APLICAVEL |
| `nivel 3 proibido` | nenhuma | NAO_APLICAVEL |
| `corpo raiz como nível 0` | nenhuma | NAO_APLICAVEL |
| `corpo raiz = nível 0` | nenhuma | NAO_APLICAVEL |
| `profundidade ≥ 3` | nenhuma | NAO_APLICAVEL |
| `profundidade >= 3` | nenhuma | NAO_APLICAVEL |
| `exatamente um elemento` | nenhuma | NAO_APLICAVEL |
| `exatamente 1 elemento` | nenhuma | NAO_APLICAVEL |
| `um único grupo` | nenhuma | NAO_APLICAVEL |

Residuo normativo incompativel: nenhum.

## 7. Escopo dos arquivos alterados

Arquivos normativos rastreados alterados no diff real:

- `docs/NOMENCLATURA.md`
- `docs/adr/ADR-0007-tela-processamento-composicao.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_tela_json.md`

Arquivos novos permitidos observados:

- `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md`

Este relatorio e o unico arquivo novo desta reexecucao:

- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md`

Nenhum outro arquivo rastreado alterado foi identificado. Arquivos nao rastreados previamente listados pelo usuario nao constituem desvio de escopo.

## 8. Achados

Nenhum achado bloqueante, alto, medio ou baixo.

Observacao nao bloqueante:

```text
ID: OBS-001
severidade: observacao
categoria: OBSERVACAO_NAO_BLOQUEANTE
arquivo e linha: docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:6; docs/adr/INDICE_ADR.md:48
descrição: permanece divergencia historica ja conhecida entre status interno da ADR-0018 (`proposta`) e indice (`aceita`), mas a aplicacao da ADR-0019 nao alterou esse arquivo nem esse status.
impacto: nao bloqueia esta QA; a verificacao solicitada era ausencia de alteracao indevida no status da ADR-0018.
correção necessária: nao nesta etapa.
nova decisão necessária: nao.
```

## 9. Conclusao

D1-D7 estao aplicadas integralmente nos documentos normativos afetados. Nao ha residuo normativo incompativel, nao ha alteracao rastreada fora do escopo, o indice contem entrada unica correta da ADR-0019 e a ADR-0007 foi superada apenas na cardinalidade de `dashboard`.

## 10. Status final

`ADR_APPLICATION_APPROVED_WITH_NOTES`

## 11. Estado Git final

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
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
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
(sem saida)

git diff --cached --stat
(sem saida)

git diff --cached --name-only
(sem saida)
```
