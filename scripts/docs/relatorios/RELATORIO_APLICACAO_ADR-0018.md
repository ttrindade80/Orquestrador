# RELATORIO_APLICACAO_ADR-0018

## 1. Identificação

Relatório: `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`

Etapa executada: `APLICAR_ADR`

ADR aplicada: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`

Data da aplicação: 2026-07-11

Papel: aplicador documental da ADR-0018 aprovada. Propagação exclusiva das
decisões já aprovadas; sem introdução de arquitetura, sem completar lacunas, sem
QA da própria aplicação.

## 2. Escopo

Propagação documental das decisões D1–D10 da ADR-0018 para os documentos
normativos ativos autorizados. Esta etapa **não**: alterou a ADR-0018; corrigiu
ou recriou o H-0024; alterou JSON de produção/configuração; implementou código;
alterou testes; criou handoff; manipulou stash; preparou commit; executou etapa
posterior do fluxo.

## 3. ADR e QA utilizados

- ADR: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
  (lida integralmente).
- QA: `docs/relatorios/RELATORIO_QA_ADR-0018.md` (lido integralmente).
  Resultado do QA: `ADR_APPROVED_WITH_NOTES`; bloqueantes 0; altos 0; médios 0;
  baixos 1 (A-001); próxima categoria `APLICAR_ADR`.

## 4. Estado Git inicial

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git rev-parse HEAD` | `3332773a3f10e716115a164148af323fa86e608f` |
| `git log -1 --oneline` | `3332773 feat: implementa redimensionamento reativo da TUI` |
| `git status --short` | stage vazio; apenas arquivos não rastreados (ADR-0018, H-0024, relatórios contextuais) |
| `git stash list` | `stash@{0}: pre-H-0022 recuperado apos drop acidental` |
| `git rev-parse stash@{0}` | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |

Estado idêntico ao esperado. Sem `MERGE_HEAD`/`REBASE_HEAD`/`CHERRY_PICK_HEAD`/
`REVERT_HEAD`; sem operação Git ativa.

## 5. Segurança entre sessões

Confirmação feita apenas por comandos de leitura (seção 4). Não foi identificada
execução paralela sobre o mesmo workspace: stage vazio, sem conflito, sem
operação Git em curso. Nenhum stash foi aplicado, removido, limpo, recriado ou
renomeado. Branch, índice, worktree e histórico não foram alterados fora dos
arquivos permitidos.

## 6. Arquivos lidos

Autoridades e evidências lidas:

- ADR-0018 (integral) e `RELATORIO_QA_ADR-0018.md` (integral).
- Autoridades normativas: `docs/adr/ADR-0013-...`, `docs/adr/ADR-0015-...`,
  `docs/adr/ADR-0017-...` (via referências consolidadas nos contratos e na
  NOMENCLATURA), `docs/contratos/contrato_composicao_corpo.md`,
  `docs/contratos/contrato_tela_json.md`,
  `docs/contratos/contrato_json_tela_minima.md`,
  `docs/contratos/contrato_processo_desenvolvimento.md`, `docs/NOMENCLATURA.md`,
  `docs/adr/INDICE_ADR.md`.
- Evidência histórica (apenas leitura): `docs/handoff/H-0024-...`,
  `docs/relatorios/IMP-0025-...`,
  `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`.

## 7. Arquivos alterados

Alterados (lista fechada permitida):

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`

Criado:

- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md` (este relatório)

## 8. Aplicação por decisão D1–D10

| Decisão | Onde propagada |
|---|---|
| D1 — arranjo × distribuição distintos | `contrato_composicao_corpo.md` §4.8 (nova nota); `contrato_tela_json.md` §8; `NOMENCLATURA.md` §14.1 (tabela de termos) |
| D2 — ausência de `distribuicao` preserva conteúdo, não é `igual` | `contrato_composicao_corpo.md` §4.9 e §5.7 (subseção de ausência); `contrato_tela_json.md` §8; `contrato_json_tela_minima.md` §6.2 e §6.3; `NOMENCLATURA.md` §14.1 |
| D3 — distribuição explícita reparte a altura útil integralmente | `contrato_composicao_corpo.md` §4.9; `contrato_tela_json.md` §8; `NOMENCLATURA.md` §14.1 |
| D4 — preenchimento interno das áreas | `contrato_composicao_corpo.md` §5.9 (nova nota); `contrato_tela_json.md` §8; `NOMENCLATURA.md` §14.1 |
| D5 — modo `igual` explícito, não fallback | `contrato_composicao_corpo.md` §5.7 (Modo `igual` explícito); `contrato_json_tela_minima.md` §6.2/§6.3; `NOMENCLATURA.md` §14.1 |
| D6 — modo `percentual` genérico | preservado em `contrato_composicao_corpo.md` §5.7; reforço de genericidade em §8 (critérios) |
| D7 — modo `fracao` genérico, vetores como exemplos | `contrato_composicao_corpo.md` §5.7 (genericidade + exemplos não exaustivos); `NOMENCLATURA.md` §14.1 |
| D8 — conteúdo maior que a cota fora de escopo | `contrato_composicao_corpo.md` §5.7.1 (nova); `contrato_tela_json.md` §8; `NOMENCLATURA.md` §14.1 |
| D9 — JSON necessário ao handoff | `contrato_processo_desenvolvimento.md` §10.1 (nova) |
| D10 — cobertura de testes (distinção normativa) | `contrato_composicao_corpo.md` §10 e critérios §8 registram algoritmo genérico × configuração concreta; nenhum handoff de testes criado; nenhuma matriz exaustiva definida |

## 9. Aplicação por documento

- **`contrato_composicao_corpo.md`**: ADR-0018 adicionada ao frontmatter;
  §4.8 recebeu a distinção arranjo × distribuição; §4.9 recebeu a semântica
  ausência × distribuição explícita e alocação integral; §5.7 recebeu subseção de
  ausência (construção orientada pelo conteúdo) e reformulou `igual` como modo
  explícito; §5.7 (fracao) explicitou genericidade e exemplos não exaustivos;
  nova §5.7.1 (conteúdo maior que a cota — lacuna externa); §5.9 recebeu o
  preenchimento interno das molduras; nova §10 (relação normativa ADR-0015 ×
  ADR-0018) e novos critérios em §8. Preservados: árvore de composição, `grupo`,
  profundidade, filhos diretos, maiores restos, desempate, redimensionamento,
  arranjo horizontal e demais decisões não conflitantes.
- **`contrato_tela_json.md`**: §8 recebeu a semântica conceitual de
  `corpo.distribuicao` (ausência sem fallback `igual`, modos explícitos, alocação
  vertical integral, distinção configuração concreta × algoritmo genérico,
  conteúdo fora de escopo). Envelope macro da tela não alterado.
- **`contrato_json_tela_minima.md`**: ADR-0018 adicionada ao frontmatter; §6.2
  (`grupo`) e §6.3 (distribuição por container) removeram a afirmação de que a
  ausência equivale a `igual`, substituindo pela semântica da ADR-0018.
  Preservados: `distribuicao` opcional, `igual` explícito válido, `percentual`,
  `fracao` e validações compatíveis. Exemplos mínimos não passaram a obrigar
  declaração de `distribuicao`.
- **`contrato_processo_desenvolvimento.md`**: nova §10.1 registra a regra de
  JSON necessário ao handoff que também altera código, preservando a distinção
  da §10 (mudança puramente declarativa dispensa handoff próprio).
- **`NOMENCLATURA.md`**: nova §14.1 diferencia `corpo.arranjo = "vertical"`,
  `ocupacao_vertical_terminal` e `corpo.distribuicao`; diferencia ausência de
  distribuição e modo `igual`; descreve preenchimento interno; preserva `fracao`
  como pesos genéricos; referencia ADR-0018. Termos específicos completos, sem
  sinônimos novos.
- **`INDICE_ADR.md`**: entrada da ADR-0018 adicionada com o vocabulário de status
  existente (`aceita`), refletindo a aprovação da ADR em QA próprio. Não declara
  QA da aplicação aprovado.

## 10. Formulações removidas

- `contrato_json_tela_minima.md` §6.2: "Quando não declarada, o comportamento é
  equivalente ao modo `igual`." (removida).
- `contrato_json_tela_minima.md` §6.3: "sua ausência é válida e equivale ao modo
  `igual`." (removida).

Nenhuma outra formulação normativa ativa de "ausência ≡ `igual`" foi encontrada
para remoção nos documentos permitidos.

## 11. Formulações adicionadas

- Distinção arranjo × distribuição (D1).
- Ausência de `distribuicao` preserva construção orientada pelo conteúdo e não
  equivale a `igual` (D2/D5).
- Distribuição explícita reparte integralmente a altura útil e aloca área (D3).
- Preenchimento interno das molduras quando há distribuição explícita (D4).
- `igual` como modo explícito, não fallback (D5).
- Genericidade de `fracao`/`percentual` com exemplos não exaustivos (D6/D7).
- Conteúdo maior que a cota como lacuna externa à ADR-0018 (D8).
- Regra de JSON necessário ao handoff (D9).
- Distinção normativa algoritmo genérico × configuração concreta × cobertura
  ampliada (D10).
- Registro da relação normativa ADR-0015 × ADR-0018 e preservação de ADR-0013 e
  ADR-0017.

## 12. Relação preservada com ADR-0013

Preservada. Na **ausência** de `distribuicao`, o preenchimento externo da altura
(`ocupacao_vertical_terminal`, ADR-0013) permanece o comportamento aplicável. A
altura útil repartida pela distribuição explícita continua obtida pelo mecanismo
de dimensões vigente. Registrado em `contrato_composicao_corpo.md` §5.7 e §10,
`contrato_tela_json.md` §8 e `NOMENCLATURA.md` §14.1.

## 13. Ponto substituído da ADR-0015

A ADR-0015 permanece autoridade da composição hierárquica. Substituído **apenas**
o ponto em que a ausência de `distribuicao` era tratada como equivalente ao modo
`igual`. Registrado explicitamente em `contrato_composicao_corpo.md` §10 e
`NOMENCLATURA.md` §14.1. A ADR-0015 histórica não foi alterada.

## 14. Preservação da ADR-0017

Preservada integralmente. Nenhuma regra de redimensionamento reativo, SIGWINCH,
cadeia de dimensões ou quadro mínimo foi alterada. Registrado como preservação em
`contrato_composicao_corpo.md` §10 e `NOMENCLATURA.md` §14.1.

## 15. Regra de JSON incorporada ao processo

`contrato_processo_desenvolvimento.md` §10.1: mudança puramente declarativa com
suporte completo existente pode continuar sem handoff próprio; alteração de JSON
necessária para implementar/demonstrar/validar um handoff que também altera
código deve integrar o próprio handoff (caminho, alteração, valores concretos,
validação sintática, critérios e testes), sem que o implementador introduza JSON
omitido e sem autorizar hardcode de valores do JSON.

## 16. Busca de resíduos

Busca contextual (sem substituição automática por substring) por: "ausência
equivale a igual", "ausencia equivale a igual", "ausência/ausencia de
distribuição/distribuicao", "default igual", "modo igual por omissão/omissao",
"distribuicao/distribuição ausente", além de referências a ADR-0015, ADR-0018,
preenchimento externo/interno, altura natural e área/area alocada.

Resultado após a aplicação: nenhum documento normativo ativo mantém a
formulação conflitante "ausência ≡ `igual`". As ocorrências remanescentes nos
documentos ativos são: (a) formas **negadas** ("**não** equivale ao modo
`igual`"); (b) descrição da substituição normativa (relação ADR-0015 ×
ADR-0018); (c) a equivalência não relacionada de `dashboard`
presente/ausente em `contrato_composicao_corpo.md` §4.1 (conceito distinto,
descritivo, não conflitante).

> **Correção pós-QA (ver seção 26).** A conclusão acima estava **incompleta**. A
> busca de resíduos desta etapa concentrou-se na equivalência "ausência ≡
> `igual`" (D2/D5) e **deixou de identificar** as formulações normativas ativas
> que colapsam arranjo e distribuição (D1): R-17 em
> `contrato_composicao_corpo.md` afirmava que o arranjo declara o "eixo de
> distribuição", e os itens 12–13 da seção 14 de `NOMENCLATURA.md` afirmavam que
> arranjo horizontal/vertical aloca colunas/linhas. O QA da aplicação
> classificou-as como achado APL-001. A seção 26 registra a busca direcionada
> posterior e a correção documental.

## 17. Ocorrências históricas preservadas

Não alteradas (evidência histórica): `docs/handoff/H-0024-...`,
`docs/relatorios/IMP-0025-...`,
`docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`,
`docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`,
`docs/relatorios/RELATORIO_QA_ADR-0018.md`,
`docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`,
`docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`,
`docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md` e demais
relatórios/ADRs históricos. A ADR-0018 permaneceu somente leitura.

## 18. Documentos normativos adicionais encontrados

Nenhum documento normativo **ativo** fora da lista fechada de arquivos
permitidos precisou ser alterado. Todas as demais ocorrências da equivalência
estão em relatórios históricos, handoffs históricos e ADRs anteriores, todos
preservados. Portanto não houve necessidade de `BLOCKED_EVIDENCE`.

## 19. Nota A-001 e tratamento não bloqueante

A nota baixa A-001 do QA aponta que a ADR-0018 usa mais de uma formulação para o
impacto sobre o H-0024 ("retomado, corrigido ou recriado"). Conforme o mandato
desta etapa: a ADR-0018 não foi alterada; o H-0024 não foi corrigido, recriado
nem declarado pronto para implementação. Registra-se como **consequência
operacional** (risco processual baixo) que o H-0024 deverá ser corrigido ou
recriado somente após a aplicação documental ser aprovada em QA próprio. Nenhuma
decisão nova foi inventada.

## 20. Verificações executadas

| Comando | Resultado |
|---|---|
| `git diff --check` | sem saída (nenhum conflito/whitespace) |
| `git diff --stat` | 6 arquivos alterados; +250 / −11 |
| `git diff --name-only` | apenas os 6 arquivos permitidos |
| `git status --short` | 6 arquivos permitidos como `M`; relatório novo e artefatos históricos como `??` |
| `grep` de resíduos ativos | somente formas negadas / descrição de substituição / equivalência de `dashboard` (não conflitante) — **conclusão incompleta; ver seção 26** |

Confirmações: somente arquivos permitidos alterados; relatório de aplicação
criado; nenhuma ADR anterior modificada; H-0024 intacto; nenhum JSON alterado;
nenhum arquivo de código ou teste alterado; stash intocado
(`21f98d0f4a479d72e6df21b1dca1511c3ad38937`).

**Verificador documental**: não há verificador documental estabelecido e
diretamente aplicável no repositório (nenhum script `.py` de validação/lint de
documentação foi localizado). Nenhum comando de validação foi inventado. As
suítes de código não foram executadas, por ser etapa documental.

## 21. Estado Git final

- Branch: `master`.
- HEAD: `3332773a3f10e716115a164148af323fa86e608f` (inalterado).
- Stage: vazio (sem `git add`).
- Alterações não commitadas: os 6 arquivos permitidos (`M`).
- Stash: `stash@{0}` = `21f98d0f4a479d72e6df21b1dca1511c3ad38937` (inalterado).
- Nenhum commit, push ou alteração de histórico executado.

## 22. Arquivos não rastreados

Permanecem não rastreados e não alterados por esta etapa:
`docs/adr/ADR-0018-...`, `docs/handoff/H-0024-...`,
`docs/relatorios/IMP-0025-...`,
`docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`,
`docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`,
`docs/relatorios/RELATORIO_QA_ADR-0018.md`,
`docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`,
`docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`. Novo não rastreado:
este relatório.

## 23. Limitações

- Aplicação estritamente documental; nenhuma implementação, teste ou JSON foi
  tocado.
- Não foi executado QA da própria aplicação (fora de escopo desta etapa).
- Não há verificador documental automatizado no repositório para registro de
  comando/resultado.
- O H-0024 permanece pendente de correção/recriação após QA da aplicação.
- A busca de resíduos original desta etapa foi incompleta quanto a D1: não
  identificou o colapso arranjo/distribuição corrigido posteriormente sob
  APL-001 (ver seção 26). A aplicação continua pendente de novo QA formal e
  **não** é declarada aprovada por este relatório.

## 24. Bloqueios

Nenhum. Não houve `BLOCKED_REPOSITORY_STATE`, `BLOCKED_DOCUMENTATION` nem
`BLOCKED_EVIDENCE`.

## 25. Próxima categoria recomendada

`QA_APLICACAO_ADR`

## 26. Correção pós-QA — APL-001 e APL-002

Esta seção registra, com transparência, a correção documental posterior ao QA da
aplicação (`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`,
`ADR_APPLICATION_REJECTED`). Ela não reescreve o histórico da execução original:
as seções 16 e 20 permanecem no relatório como evidência de que a busca inicial
foi incompleta.

### 26.1 Falha da busca inicial

A busca de resíduos da execução original (seção 16) concentrou-se na equivalência
"ausência ≡ `igual`" (D2/D5) e **deixou de identificar** as formulações
normativas ativas que colapsam arranjo e distribuição (D1):

- `contrato_composicao_corpo.md` R-17: afirmava que o arranjo de um container
  "declara o eixo de distribuição" dos filhos diretos;
- `NOMENCLATURA.md` seção 14, itens 12–13: afirmavam que `arranjo = horizontal`
  aloca colunas e `arranjo = vertical` aloca linhas.

Essas formulações contradiziam a ADR-0018 D1, que separa arranjo (ordem/eixo de
composição) de distribuição (repartição da dimensão).

### 26.2 Identificação pelo QA

O QA da aplicação identificou essas ocorrências e as registrou como achado
**APL-001** (severidade alta), citando
`contrato_composicao_corpo.md:837`, `NOMENCLATURA.md:1168` e
`NOMENCLATURA.md:1170`. A inconsistência do próprio relatório de aplicação — que
declarava não haver resíduo normativo ativo — foi registrada como achado
**APL-002** (severidade média).

### 26.3 Correção documental aplicada

Etapa `PATCH_DOCUMENTACAO`, restrita aos achados APL-001 e APL-002:

- `contrato_composicao_corpo.md` R-17: reformulado para distinguir o **eixo de
  composição** definido pelo arranjo da **repartição da dimensão** feita somente
  pela `distribuicao` explícita. Arranjo horizontal/vertical passa a apenas
  organizar os filhos no eixo correspondente; sem `distribuicao`, o arranjo não
  reparte nem aloca a dimensão disponível.
- `NOMENCLATURA.md` itens 12–13 da seção 14: reformulados para declarar que
  arranjo horizontal/vertical organiza os filhos horizontal/verticalmente e que a
  alocação proporcional de colunas ou linhas ocorre **apenas** quando o mesmo
  container possui `distribuicao` explícita. Preservada a distinção entre
  `arranjo`, `ocupacao_vertical_terminal` e `corpo.distribuicao`, sem sinônimos
  novos.
- Este relatório (seção 16, seção 20 e seção 23): anotado que a conclusão
  original da busca de resíduos era incompleta, com remissão a esta seção.

As regras de maiores restos, desempate, modos `igual`/`percentual`/`fracao`,
grupos, profundidade, redimensionamento e conteúdo maior que a cota **não** foram
alteradas.

### 26.4 Nova busca direcionada

Após a correção, foi executada busca contextual direcionada nos dois documentos
(`eixo de distribuição`, `arranjo … aloca/reparte/distribui`, `aloca/reparte
colunas/linhas`, e verificação ampliada por `arranjo`, `distribuicao`, `altura
natural`, `área alocada`). As ocorrências remanescentes classificam-se como:

- formulação correta de composição (arranjo apenas organiza os filhos);
- distribuição explicitamente declarada (repartição atribuída à `distribuicao`);
- registro da relação/substituição normativa ADR-0015 × ADR-0018.

Não restou formulação ativa que atribua repartição ou alocação de dimensão ao
arranjo sozinho. Nenhum novo conflito normativo ativo foi encontrado fora dos
trechos autorizados.

### 26.5 Estado e bloqueios remanescentes

- O patch documental corrigiu APL-001 e APL-002; a aplicação da ADR-0018
  **continua pendente de novo QA formal** e **não** é declarada aprovada por este
  relatório.
- Somente os três arquivos autorizados desta etapa foram alterados
  (`contrato_composicao_corpo.md`, `NOMENCLATURA.md`, este relatório). ADR-0018,
  relatório de QA, H-0024, JSON, código e testes permaneceram intactos; stage
  vazio; stash inalterado (`21f98d0f4a479d72e6df21b1dca1511c3ad38937`).
- O H-0024 permanece pendente de correção/recriação somente após aprovação da
  aplicação documental em QA próprio.
