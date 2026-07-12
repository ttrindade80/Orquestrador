# QA pós-patch — levantamento documental de matriz de grupos

## 1. Identificação

- projeto: `orquestrador_novo`
- etapa: `QA_POS_PATCH` (reauditoria independente do levantamento documental)
- artefato auditado: `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
- patch auditado: `PATCH_DOCUMENTACAO` com oito achados autorizados (`PATCH-MAT-001` a `PATCH-MAT-008`)
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- commit atual: `f00b0bb` (`docs: registra substituicao do H-0024 pelo H-0025`)

Papel: auditor documental independente. Este QA não corrigiu o levantamento, não alterou
ADR, handoff, contrato, nomenclatura, código, teste ou configuração, não criou patch, não
preparou nem executou commit e não aprovou a própria entrega.

## 2. Estado Git inicial

Comandos executados a partir da raiz Git (`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`);
os caminhos declarados na documentação são relativos a `scripts/`.

```text
git rev-parse --show-toplevel
  /home/tiago/Dropbox/UFRGS/Survey/versao_0_1

git branch --show-current
  master

git status --short
  ?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md

git log -3 --oneline
  f00b0bb docs: registra substituicao do H-0024 pelo H-0025
  c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos
  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria
```

Confirmações:

- o artefato auditado permanece **não rastreado** (`??`), conforme declarado pelo autor do patch;
- stage vazio — confirmado (nenhuma entrada em `git diff --cached`);
- o commit atual é `f00b0bb`; os dois commits anteriores são exatamente `c003f3e` (fechamento do
  H-0027) e `40015b6` (fechamento do H-0026), ambos referenciados pelo levantamento;
- nenhuma alteração rastreada no repositório além do artefato não rastreado sob auditoria.

## 3. Autoridades consultadas

Consultadas como autoridades normativas e evidenciais (somente leitura; nenhuma alterada):

- `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` — handoff H-0027
  (status declarado `proposto`; ADR base ADR-0019 `aceita`; escopo D1–D7).
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md` — QA pós-patch do handoff
  (`H1_HANDOFF_APPROVED`).
- `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` — relatório de
  implementação (1004/1004 verificações; commit-base `40015b6`).
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` — QA pós-patch da
  implementação (`I1_IMPLEMENTATION_APPROVED`; 1004/1004 independentes).
- `scripts/docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` — verificação de fechamento
  (`CLOSURE_READY_FOR_COMMIT_PREPARATION`; mensagem de commit sugerida coincide com `c003f3e`).
- `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` — ADR-0019
  (status `aceita` no frontmatter e no corpo).
- `scripts/docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` — QA da aplicação documental
  da ADR-0019 (`ADR_APPLICATION_APPROVED_WITH_NOTES`).
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md` — QA pós-patch da ADR-0019
  (`ADR_APPROVED`).
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` — ADR-0018
  (status `proposta` no frontmatter linha 6 e no corpo linha 25).
- `scripts/docs/adr/INDICE_ADR.md` — índice de ADRs (ADR-0018 linha 48 `aceita`; ADR-0019 linha 49 `aceita`).
- `scripts/docs/relatorios/RELATORIO_QA_ADR-0018.md` — QA da ADR-0018 (`ADR_APPROVED_WITH_NOTES`).
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md` — QA pós-patch da aplicação
  documental da ADR-0018 (`ADR_APPLICATION_APPROVED_WITH_NOTES`).
- `scripts/docs/NOMENCLATURA.md`, `scripts/docs/contratos/contrato_composicao_corpo.md`,
  `scripts/docs/contratos/contrato_tela_json.md`, `scripts/docs/contratos/contrato_json_tela_minima.md`
  — autoridades normativas ativas (consultadas em trechos diretamente relevantes).

Confirmação factual dos commits:

```text
git show --no-patch --oneline c003f3e
  c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos

git show --no-patch --oneline 40015b6
  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria
```

## 4. Verificação dos achados

| Achado | Correção esperada | Evidência encontrada | Resultado |
|---|---|---|---|
| QA-MAT-001 | Registrar H-0026 em `40015b6` e H-0027 em `c003f3e` com mensagens corretas; toda ocorrência de `40015b6` limitada a fechamento do H-0026 ou commit-base do H-0027 | Linhas 19 e 23–24: `40015b6` associado ao fechamento do H-0026 e ao commit-base do H-0027; `c003f3e` associado ao fechamento do H-0027; mensagens coincidem com `git show --no-patch`. Busca de resíduos: as 3 ocorrências de `40015b6` (linhas 19, 23, 213) estão todas no contexto permitido | RESOLVIDO |
| QA-MAT-002 | Distinguir handoff `proposto`, QA `H1_HANDOFF_APPROVED`, implementado, `I1_IMPLEMENTATION_APPROVED`, 1004/1004, commit `c003f3e`, ciclo FECHADO; não classificar como ativo, não interpretar `proposto` como ausência de aprovação, não declarar que o handoff aprovou a própria entrega | Linhas 21–28 e 43: distinguem status declarado `proposto`, QA de handoff `H1_HANDOFF_APPROVED`, QA de implementação `I1_IMPLEMENTATION_APPROVED`, 1004/1004, commit `c003f3e`, estado FECHADO; o handoff é descrito como "registro de escopo executado", não como aprovação da entrega | RESOLVIDO |
| QA-MAT-003 | Distinguir status textual `proposta`, índice `aceita`, QA `ADR_APPROVED_WITH_NOTES`, aplicação `ADR_APPLICATION_APPROVED_WITH_NOTES`, decisão incorporada aos contratos ativos, pendência de divergência documental localizada de status; não tratar como rejeitada, não aplicada, coerente internamente, pendência resolvida ou alteração do ciclo H-0027 | Linhas 38, 174 e 219: distinguem arquivo `proposta`, índice `aceita`, QA `ADR_APPROVED_WITH_NOTES`, aplicação `ADR_APPLICATION_APPROVED_WITH_NOTES`, "decisão incorporada aos contratos ativos", divergência como "pendência documental localizada e separada"; a divergência de status é explicitamente registrada como não resolvida ("impede apresentar o status interno como coerente") | RESOLVIDO |
| QA-MAT-004 | ADR-0019: status no arquivo `aceita`, status no índice `aceita`, aplicação documental aprovada, ciclo relacionado H-0027; não listada como pendência | Linha 37: status no arquivo `aceita`, índice `aceita`, aplicação documental aprovada, ciclo relacionado H-0027; ADR-0019 não aparece em nenhuma lista de pendências (seções 15 e 18 listam apenas a divergência da ADR-0018) | RESOLVIDO |
| QA-MAT-005 | Separar expressamente regra atual (somente comportamento hierárquico; sem seletor declarativo; sem fallback entre dois comportamentos) de decisão candidata ainda não formalizada (criar seletor; preservar comportamento atual quando seletor ausente; adicionar comportamento de matriz; rejeitar matriz inválida sem fallback silencioso); a decisão candidata não pode aparecer como contrato, regra ativa ou comportamento implementado | Linha 60 (regra atual): "todos os grupos compartilham do mesmo e único comportamento de grupo... Não existe seletor declarativo de especialização de comportamento do grupo"; linha 154: "Não existe, portanto, fallback entre `hierárquico` e outro comportamento de grupo — há apenas um comportamento vigente. A preservação do comportamento atual quando um futuro seletor estiver ausente é uma decisão candidata ainda não formalizada em ADR"; seções 16 (lacunas) e 17 (decisões do usuário) listam as decisões candidatas como futuras e não formalizadas | RESOLVIDO |
| QA-MAT-006 | Ausência de `sólida`, `robusta`, `excelente`, `completa`, `bem-sucedida` como avaliação qualitativa sem critério verificável; conclusão descreve fatos, autoridades, testes e lacunas | Termos literais ausentes como avaliação qualitativa: `completa`/`completas` ocorrem apenas como adjetivo descritivo de lacunas ("lacunas normativas completas", linha 217) e dentro de citação de evidência ("incompleta", linha 125); conclusão (seção 19) é factual. Observação: "perfeitamente" na linha 158 é avaliativo em tom, embora substanciado por evidência de testes (1004/1004, regressões dos JSONs) | RESOLVIDO (com OBS-001) |
| QA-MAT-007 | Ausência de assinatura ou identificação de ferramenta, marca, modelo, fornecedor ou executor específico | Busca por `assinado`, `opencode`, `codex`, `gpt`, `claude`, `zcode`, `cursor`, `ferramenta`, `fornecedor`, `marca`: nenhuma ocorrência como identificação de executor. Ocorrências de `modelo` referem-se ao módulo `tela/modelo.py` ou ao campo de tela, não a modelo de IA | RESOLVIDO |
| QA-MAT-008 | Conclusão registra coerentemente: H-0026 fechado em `40015b6`; H-0027 fechado em `c003f3e`; composição hierárquica atual com até três níveis; matriz declarativa de grupos ainda inexistente; necessidade de ADR para introduzir o novo comportamento; divergência textual da ADR-0018 como pendência separada; ausência de regra aplicada sobre seletor, linhas, colunas, células e schema matricial | Seção 19 (linhas 211–219): registra H-0027 fechado em `c003f3e`, H-0026 fechado em `40015b6`, 1004/1004, composição hierárquica com até três níveis, matriz declarativa "inexistente", necessidade de ADR, divergência da ADR-0018 como "pendência documental localizada e separada", ausência de seletor/schema matricial/linhas/colunas/células documentados e "Nenhuma dessas decisões foi formalizada em ADR" | RESOLVIDO |

## 5. Verificação factual dos commits

Confirmação independente por `git show --no-patch --oneline`:

```text
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria
c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos
```

Mensagens registradas pelo levantamento (linhas 19 e 24) coincidem integralmente com as
mensagens reais do repositório.

Distribuição das ocorrências de `40015b6` no levantamento (busca `rg`):

| Linha | Contexto | Classificação |
|---|---|---|
| 19 | "Ciclo H-0026 — Commit final: `40015b6`" | fechamento do H-0026 (permitido) |
| 23 | "Ciclo H-0027 — Commit-base do desenvolvimento: `40015b6`" | commit-base do H-0027 (permitido) |
| 213 | "o ciclo H-0026 está fechado (commit `40015b6`)" | fechamento do H-0026 (permitido) |

Todas as ocorrências de `40015b6` estão limitadas ao fechamento do H-0026 ou ao commit-base do
desenvolvimento do H-0027. Nenhuma ocorrência associa `40015b6` ao fechamento do H-0027 ou a
outra capacidade. Conforme.

Distribuição das ocorrências de `c003f3e`:

| Linha | Contexto | Classificação |
|---|---|---|
| 24 | "Ciclo H-0027 — Commit final: `c003f3e`" | fechamento do H-0027 (correto) |
| 43 | "commit de fechamento: `c003f3e`" | fechamento do H-0027 (correto) |
| 213 | "O ciclo H-0027 está fechado (commit `c003f3e`)" | fechamento do H-0027 (correto) |

Todas as ocorrências de `c003f3e` associam-se corretamente ao fechamento do H-0027. Conforme.

## 6. Continuidade do H-0027

O levantamento distingue corretamente os estados do ciclo H-0027:

```yaml
handoff: H-0027
status_declarado_no_handoff: proposto
qa_handoff: H1_HANDOFF_APPROVED
implementado: true
qa_implementacao: I1_IMPLEMENTATION_APPROVED
testes: 1004/1004
commit: c003f3e
estado_do_ciclo: FECHADO
```

Evidência cruzada com as autoridades:

- `H-0027` frontmatter (linha 6) e seção 1 (linha 54): status `proposto` — confirmado.
- `RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md` seção 7 (linha 239): `H1_HANDOFF_APPROVED` — confirmado.
- `RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` seção 14 (linha 587): `I1_IMPLEMENTATION_APPROVED`
  com 1004/1004 independentes — confirmado.
- `RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` seção 17 (linha 445): `CLOSURE_READY_FOR_COMMIT_PREPARATION`
  e seção 15 (linha 426) mensagem de commit sugerida `feat: implementa composicao hierarquica do corpo
  com tres niveis de grupos` — coincide com `c003f3e`.

Verificações negativas exigidas:

- o relatório **não** classifica o ciclo H-0027 como ainda ativo (linha 28: "Estado do ciclo: FECHADO");
- o relatório **não** interpreta `proposto` como ausência de aprovação posterior (linha 43 correlaciona
  explicitamente `proposto` com `H1_HANDOFF_APPROVED`, `I1_IMPLEMENTATION_APPROVED` e commit de fechamento);
- o relatório **não** declara que o handoff aprovou a própria entrega (linha 43 descreve o handoff como
  "registro de escopo executado"; o handoff é explicitamente "ordem de trabalho fechada para o executor
  de implementação" segundo `H-0027` seção 1).

Conforme.

## 7. Estado documental da ADR-0018

O levantamento distingue corretamente os estados da ADR-0018:

```yaml
status_textual_no_arquivo: proposta
status_no_indice: aceita
qa_adr: ADR_APPROVED_WITH_NOTES
aplicacao_documental: concluida
qa_aplicacao_final: ADR_APPLICATION_APPROVED_WITH_NOTES
decisao_normativa: incorporada_aos_contratos_ativos
pendencia: divergencia_documental_localizada_de_status
```

Evidência cruzada:

- `ADR-0018` frontmatter (linha 6) e corpo (linha 25): `status: proposta` — confirmado.
- `INDICE_ADR.md` linha 48: ADR-0018 `aceita` — confirmado.
- `RELATORIO_QA_ADR-0018.md` linha 13: `ADR_APPROVED_WITH_NOTES` — confirmado.
- `RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md` seção 11 (linha 273): `ADR_APPLICATION_APPROVED_WITH_NOTES`
  — confirmado.

Verificações negativas exigidas:

- a ADR-0018 **não** é tratada como rejeitada (linha 38: "Decisão incorporada aos contratos ativos");
- a ADR-0018 **não** é tratada como não aplicada (linha 38: "aplicação documental: aprovada");
- a ADR-0018 **não** é tratada como coerente internamente (linha 38: "A divergência de status não anula
  as decisões normativas incorporadas, mas impede apresentar o status interno como coerente"; linha 174
  registra explicitamente o desalinhamento);
- a divergência **não** é tratada como pendência resolvida (linha 219: "pendência documental localizada
  e separada");
- a ADR-0018 **não** é tratada como alteração pertencente ao ciclo H-0027 (linha 174 atribui a divergência
  ao "achado ACH-008 do H-0027" como registro prévio, e a seção 12.2 da verificação de fechamento do H-0027
  confirma que a ADR-0018 "não alterada neste ciclo"; a aplicação documental da ADR-0018 é ciclo anterior
  distinto, datado de 2026-07-11).

Conforme.

## 8. Estado documental da ADR-0019

O levantamento registra corretamente:

```yaml
status_no_arquivo: aceita
status_no_indice: aceita
aplicacao_documental: aprovada
ciclo_relacionado: H-0027
```

Evidência cruzada:

- `ADR-0019` frontmatter (linha 6) e corpo (linha 26): `aceita` — confirmado.
- `INDICE_ADR.md` linha 49: ADR-0019 `aceita` — confirmado.
- `RELATORIO_QA_POS_PATCH_ADR-0019.md` seção 15 (linha 368): `ADR_APPROVED` — confirmado.
- `RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` seção 10 (linha 172): `ADR_APPLICATION_APPROVED_WITH_NOTES`
  — confirmado (a aplicação documental é aprovada).
- Ciclo relacionado H-0027: confirmado por `H-0027` seção 1 (ADR base ADR-0019) e por
  `RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` seção 4.2.

Verificação negativa exigida:

- a ADR-0019 **não** é listada como pendência. A seção 15 do levantamento lista apenas a divergência da
  ADR-0018; a seção 18 (lacunas) trata de ausência de regras para matriz declarativa, não da ADR-0019.
  Conforme.

## 9. Regra atual versus decisão candidata

O levantamento separa expressamente os dois domínios.

### Regra atual

| Exigência | Evidência no levantamento | Confirmado |
|---|---|---|
| Existe somente o comportamento hierárquico de grupo | Linha 60: "todos os grupos compartilham do mesmo e único comportamento de grupo (a composição hierárquica recursiva)"; linha 215: "O grupo atual é inteiramente uniforme, seguindo o arranjo unidimensional local" | SIM |
| Não existe seletor declarativo entre comportamento hierárquico e matriz | Linha 60: "Não existe seletor declarativo de especialização de comportamento do grupo (ex.: hierárquico versus matricial)"; seção 16 item 3: "Ausência de campos para chaveamento declarativo de comportamentos estruturais de grupo" | SIM |
| Não existe atualmente fallback entre dois comportamentos | Linha 154: "Não existe, portanto, fallback entre `hierárquico` e outro comportamento de grupo — há apenas um comportamento vigente" | SIM |

### Decisão candidata ainda não formalizada

| Exigência | Evidência no levantamento | Confirmado |
|---|---|---|
| Criar seletor declarativo | Seção 17: "Qual termo (...) será adotado para o seletor declarativo de comportamento do grupo"; seção 16 item 3 registra como lacuna | SIM |
| Preservar o comportamento atual quando o seletor estiver ausente | Linha 154: "A preservação do comportamento atual quando um futuro seletor estiver ausente é uma decisão candidata ainda não formalizada em ADR" | SIM |
| Adicionar comportamento de matriz | Seção 17: decisões sobre dimensões, preenchimento, distribuição bidimensional e aninhamento em células de matriz — todas como decisões do usuário a estabelecer | SIM |
| Rejeitar matriz inválida sem fallback silencioso | Linha 157: "sem fallbacks silenciosos (R-22 do contrato de composição)" — referente ao comportamento atual; a seção 17 registra a validação de terminal pequeno na matriz como decisão necessária | SIM |

Verificação negativa exigida:

- a decisão candidata **não** aparece como contrato, regra ativa ou comportamento já implementado.
  A seção 13 (linha 154) qualifica expressamente a preservação como "decisão candidata ainda não
  formalizada em ADR"; a seção 14 (documentos potencialmente afetados) condiciona toda alteração a
  "Nova ADR aprovada/aceita"; a seção 19 (linha 219) afirma "Nenhuma dessas decisões foi formalizada
  em ADR". Conforme.

## 10. Neutralidade e linguagem factual

### Termos literais proibidos

Busca `rg -ni 'sólida|robusta|excelente|completa|bem-sucedida'`:

| Linha | Ocorrência | Classificação |
|---|---|---|
| 125 | "incompleta" (dentro de citação de evidência do `NOMENCLATURA.md`) | não avaliativa — citação textual |
| 217 | "lacunas normativas completas" | não avaliativa — adjetivo descritivo de lacuna (ausência), não elogio |

Nenhuma ocorrência dos termos como avaliação qualitativa do trabalho sem critério verificável.

### Equivalentes semânticos

Busca ampliada por `perfeit[ao]|impecável|consistente|coerente|suficiente|adequada|confiável|consolidad[ao]|rigoros[ao]|precis[ao]|corret[ao]|fiel`:

| Linha | Ocorrência | Classificação |
|---|---|---|
| 38 | "impede apresentar o status interno como coerente" | não avaliativa — descreve a divergência da ADR-0018 |
| 158 | "carregados e validados perfeitamente sob as regras do H-0027" | avaliativa em tom — ver OBS-001 |
| 188, 200, 206, 217 | "alinhamento perfeito" / "grade de divisórias perfeita compartilhada" | não avaliativa — descreve conceito futuro/hipotético inexistente, registrado como lacuna ou decisão necessária |

A conclusão (seção 19) descreve fatos (commits, testes, estados de ciclo), autoridades
(ADR-0018, ADR-0019, IMP-0028), testes (1004/1004) e lacunas (matriz declarativa inexistente,
ausência de seletor/schema). Conforme, com a observação registrada em OBS-001.

### Neutralidade do executor (QA-MAT-007)

Busca por `assinado|executor|agente|ferramenta|modelo|fornecedor|marca|opencode|codex|gpt|claude|zcode|cursor`:
nenhuma ocorrência como identificação de ferramenta, marca, modelo, fornecedor ou executor
específico. Ocorrências de `modelo` referem-se ao módulo `tela/modelo.py` ou ao campo de tela;
`agente` não ocorre como executor. Conforme.

## 11. Preservações

Verificação de que o patch não removeu ou distorceu, sem justificativa, os elementos exigidos.
Confirmação cruzada com os contratos e a nomenclatura ativos.

| Elemento preservado | Presente no levantamento | Fiel às autoridades |
|---|---|---|
| Definição atual de `grupo` (único nó estrutural, sem natureza funcional, não navegável, sem moldura/conteúdo próprios, redistribui área recursivamente) | Seção 4 (linhas 48–50) | SIM — `contrato_composicao_corpo.md` seção 3.2 e R-15 |
| Máximo de três níveis de grupos | Seção 6 (linha 75) e seção 8 (linha 101) | SIM — ADR-0019 D2; `contrato_composicao_corpo.md` seção 3.2 |
| Composição recursiva | Seção 4 (linha 60) e seção 6 | SIM — `contrato_composicao_corpo.md` seção 3.2; `contrato_tela_json.md` |
| Distribuição local por container | Seção 7 (linha 96) | SIM — `contrato_composicao_corpo.md` seção 4.9 |
| Modos `igual`, `percentual` e `fracao` | Seção 7 (linhas 88–90) | SIM — `contrato_composicao_corpo.md` seção 5.7 |
| Associação dos valores aos filhos diretos | Seção 7 (linha 91) | SIM — `contrato_composicao_corpo.md` seção 4.9 |
| Algoritmo de maiores restos | Seção 7 (linha 95) | SIM — `contrato_composicao_corpo.md` seção 5.8 e R-19 |
| Garantias atuais de alinhamento | Seção 9 (linhas 108–112) | SIM — `contrato_composicao_corpo.md` seções 5.6, 5.9 e 5.12 |
| Inexistência de matriz declarativa de grupos | Seção 10 (linha 127), seção 16 item 4 e seção 19 (linha 217) | SIM — ausência confirmada por busca negativa nos contratos e nomenclatura |
| Análise terminológica | Seção 12 (linhas 138–150) | SIM —术语 classificados conforme disponibilidade documental |
| Lista de lacunas | Seção 16 (linhas 179–190) — 11 lacunas enumeradas | SIM |
| Lista de documentos potencialmente afetados | Seção 14 (linhas 162–170) — 5 documentos | SIM |
| Decisões ainda necessárias do usuário | Seção 17 (linhas 192–201) — 7 decisões | SIM |

Nenhuma preservação exigida foi removida ou distorcida pelo patch.

## 12. Resíduos

Busca executada:

```bash
rg -n '40015b6|c003f3e|Ativo/Proposto|proposta aceita|fallback implícito seguro|sólida|robusta|Assinado:|opencode|H-0027|ADR-0018|ADR-0019' \
  scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
```

Análise de cada ocorrência encontrada (análise também de equivalentes semânticos):

| Padrão | Ocorrências | Classificação |
|---|---|---|
| `40015b6` | linhas 19, 23, 213 | todas no contexto permitido (fechamento do H-0026 ou commit-base do H-0027) — conforme QA-MAT-001 |
| `c003f3e` | linhas 24, 43, 213 | todas associadas ao fechamento do H-0027 — conforme |
| `Ativo/Proposto` | nenhuma | não ocorre |
| `proposta aceita` | nenhuma | não ocorre (a ADR-0018 é tratada com `proposta` no arquivo e `aceita` no índice, separadamente) |
| `fallback implícito seguro` | nenhuma | não ocorre |
| `sólida` | nenhuma | não ocorre |
| `robusta` | nenhuma | não ocorre |
| `Assinado:` | nenhuma | não ocorre |
| `opencode` | nenhuma | não ocorre |
| `H-0027` | linhas 21, 43, 158, 213 | todas no contexto correto (ciclo fechado, escopo executado, regras do H-0027) |
| `ADR-0018` | linhas 38, 59, 97, 174, 219 | todas no contexto correto (divergência de status, ausência de distribuição, pendência separada) |
| `ADR-0019` | linhas 37, 76, 78, 80 | todas no contexto correto (status aceita, D1/D4, D5/D6, regras de profundidade) |

Equivalentes semânticos verificados: `perfeitamente` (linha 158, avaliativo — OBS-001);
`perfeito` (linhas 188, 200, 206, 217, conceito futuro hipotético — não avaliativo); `coerente`
(linha 38, descreve divergência — não avaliativo). Nenhum resíduo normativo incompatível,
nenhuma regra futura apresentada como vigente, nenhuma autoridade distorcida.

## 13. Achados do QA

Nenhum achado bloqueante, alto ou médio. Os oito achados autorizados (`PATCH-MAT-001` a
`PATCH-MAT-008`, aqui referidos como `QA-MAT-001` a `QA-MAT-008`) estão todos resolvidos.

### OBS-001

- ID: `OBS-001`
- Severidade: `OBSERVACAO`
- Categoria: `OBSERVACAO`
- Arquivo e linha: `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md:158`
- Descrição: a frase "Os arquivos JSON legados (...) são carregados e validados perfeitamente sob
  as regras do H-0027" usa o advérbio "perfeitamente" como avaliação qualitativa sem critério
  verificável expresso no ponto. A alegação é substanciada por evidência testável registrada
  no `IMP-0028` (regressões dos quatro JSONs com 1004/1004 verificações aprovadas), mas o
  advérbio é avaliativo em tom e não acrescenta informação factual verificável no próprio trecho.
- Impacto: nenhum impacto na utilização do levantamento como base para a futura ADR da matriz
  de grupos; o fato subjacente (compatibilidade retroativa comprovada por testes) é correto.
- Correção necessária: nenhuma por este QA (o levantamento não é corrigido pelo auditor).

## 14. Estado Git final

```text
git rev-parse --show-toplevel
  /home/tiago/Dropbox/UFRGS/Survey/versao_0_1

git branch --show-current
  master

git log -1 --oneline
  f00b0bb docs: registra substituicao do H-0024 pelo H-0025

git status --short
  ?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
  ?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md

git diff --no-index --check /dev/null scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
  scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md:49: trailing whitespace.
  scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md:57: trailing whitespace.
  scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md:58: trailing whitespace.
  scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md:76: trailing whitespace.
  (código de saída 3)
```

Observações de estado Git:

- o artefato auditado permanece **não rastreado** e **não alterado** por este QA (timestamp do
  arquivo preservado);
- o único novo arquivo criado por esta auditoria é
  `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md` (este relatório,
  não rastreado);
- stage permanece vazio;
- nenhuma alteração rastreada foi introduzida pelo QA.

Nota sobre `git diff --no-index --check`: o comando reporta espaços em branco à direita nas
linhas 49, 57, 58 e 76 do artefato auditado. Trata-se de condição preexistente do arquivo
(introduzida antes desta auditoria; o QA não modificou o artefato), não introduzida pelo patch
sob auditoria e não objeto de nenhum dos oito achados `PATCH-MAT`. Não constitui regressão
introduzida pelo patch documental nem afeta o conteúdo semântico do levantamento. Registrada
como constatação de estado, sem classificação como achado (não é erro factual, não distorce
autoridade, não apresenta regra futura como vigente).

## 15. Status final

```text
DOCUMENTATION_PATCH_APPROVED_WITH_NOTES
```

Justificativa:

- os oito achados autorizados (`PATCH-MAT-001` a `PATCH-MAT-008`) estão **resolvidos`;
- as correções são **fiéis** às autoridades e evidências (commits, handoff, ADRs, relatórios QA,
  contratos e nomenclatura);
- **nenhuma regra futura** (seletor declarativo, matriz declarativa, schema matricial, linhas,
  colunas, células) é apresentada como norma vigente;
- **nenhuma autoridade foi distorcida**;
- **nenhuma regressão semântica** foi introduzida no restante do levantamento;
- o relatório permanece **neutro, factual e adequado** para subsidiar a criação futura da ADR
  da matriz de grupos;
- resta apenas `OBS-001` (observação de linguagem na linha 158), sem impacto na utilização do
  levantamento como base para a ADR;
- não há achado bloqueante, alto ou médio.

## 16. Próxima categoria processual

`CRIAR_ADR_MATRIZ_GRUPOS` (decisão do usuário; o levantamento está aprovado como base factual
neutra para a futura ADR da matriz de grupos).

Esta auditoria não cria ADR, não implementa, não aplica decisão, não prepara nem executa commit
e não inicia outro ciclo. O levantamento não foi corrigido pelo auditor.
