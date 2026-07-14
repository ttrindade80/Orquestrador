# RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018

## 1. Identificacao

Etapa executada: `QA_APLICACAO_ADR`

Escopo: QA formal pos-patch da aplicacao documental da ADR-0018.

Relatorio criado: `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`

Data: 2026-07-11

Papel: auditor formal pos-correcao. Nenhum documento normativo, relatorio
anterior, ADR, JSON, codigo, teste, stash, branch, indice ou historico Git foi
corrigido por este QA.

## 2. Estado operacional e repositorio

O caminho do relatorio estava livre antes da criacao.

Nao foi identificada outra sessao executando trabalho sobre o mesmo workspace. A
verificacao de processos retornou apenas a propria execucao encapsulada do Codex.
Tambem nao havia `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`
ou `index.lock`.

Comandos obrigatorios executados:

| Comando | Resultado |
|---|---|
| `git status --short` | 6 arquivos rastreados modificados e artefatos novos nao rastreados do ciclo |
| `git status` | branch `master`; stage vazio; sem operacao Git ativa |
| `git branch --show-current` | `master` |
| `git rev-parse HEAD` | `3332773a3f10e716115a164148af323fa86e608f` |
| `git log -1 --oneline` | `3332773 feat: implementa redimensionamento reativo da TUI` |
| `git diff --check` | sem saida |
| `git diff --stat` | 6 arquivos, 267 insercoes, 19 remocoes |
| `git diff --name-only` | somente os 6 documentos rastreados esperados |
| `git diff --cached --stat` | sem saida |
| `git diff --cached --name-only` | sem saida |
| `git stash list` | `stash@{0}: pre-H-0022 recuperado apos drop acidental` |
| `git rev-parse stash@{0}` | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |

Arquivos rastreados modificados pela aplicacao acumulada:

- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`

Artefatos novos nao rastreados do ciclo permanecem nao rastreados, incluindo
ADR-0018, H-0024, relatorios historicos/contextuais e relatorios de QA/aplicacao.

## 3. Artefatos auditados

Lidos integralmente:

- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/relatorios/RELATORIO_QA_ADR-0018.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`

Auditadas as versoes atuais de:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`

Consultadas como autoridades relacionadas:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`

Consultadas somente como evidencia historica:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`

`git diff --no-index /dev/null docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`
retornou codigo 1 esperado para arquivo com conteudo e exibiu o relatorio
completo como arquivo novo.

## 4. Revalidacao de APL-001

Status: resolvido.

Evidencia principal:

- `docs/contratos/contrato_composicao_corpo.md:837-844`: R-17 agora define
  `arranjo` como eixo de composicao dos filhos diretos, declara que arranjo
  sozinho nao reparte nem aloca a dimensao disponivel, e condiciona a reparticao
  da largura/altura a `distribuicao` explicita.
- `docs/NOMENCLATURA.md:1168-1175`: itens 12-13 agora dizem que arranjo
  horizontal/vertical organiza os filhos no eixo correspondente, e que a alocacao
  proporcional de colunas/linhas ocorre apenas quando o mesmo container possui
  `distribuicao` explicita.
- `docs/contratos/contrato_composicao_corpo.md:278-288`: preserva que o arranjo
  de um container nao obriga o arranjo dos filhos e qualifica a tabela de eixo
  como aplicavel quando ha distribuicao explicita.
- `docs/NOMENCLATURA.md:1217-1219`: distingue `corpo.arranjo = "vertical"`,
  `ocupacao_vertical_terminal` e `corpo.distribuicao`.
- `docs/NOMENCLATURA.md:1223-1230`: reafirma que arranjo nao e distribuicao, que
  ausencia de `corpo.distribuicao` preserva altura natural e que nao ha
  reparticao proporcional automatica.

Critérios de resolucao:

| Criterio | Resultado |
|---|---|
| `arranjo` define organizacao/eixo de composicao | conforme |
| `arranjo` sozinho nao aloca nem reparte proporcionalmente | conforme |
| `distribuicao` explicita e gatilho da reparticao | conforme |
| arranjo horizontal com distribuicao reparte colunas/largura | conforme |
| arranjo vertical com distribuicao reparte linhas/altura | conforme |
| sem distribuicao preserva composicao orientada pelo conteudo | conforme |
| `arranjo`, `ocupacao_vertical_terminal` e `distribuicao` seguem distintos | conforme |
| container filho pode ter arranjo diferente do pai | conforme |

Nao resta contradicao normativa ativa relacionada ao achado APL-001.

## 5. Revalidacao de APL-002

Status: resolvido.

Evidencia principal em `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`:

- linhas 191-215 preservam a busca original e anotam que sua conclusao estava
  incompleta.
- linhas 317-329 registram explicitamente a falha da busca inicial quanto ao
  colapso arranjo/distribuicao.
- linhas 331-338 identificam o QA que detectou APL-001 e APL-002.
- linhas 340-356 registram os documentos corrigidos e a natureza da correcao.
- linhas 362-375 registram nova busca direcionada e ausencia de conflito ativo.
- linhas 377-381 declaram que a aplicacao continuava pendente de novo QA formal
  e nao era aprovada por aquele relatorio.

Critérios de resolucao:

| Criterio | Resultado |
|---|---|
| nao reescreve historico como se a busca original estivesse correta | conforme |
| registra omissao inicial | conforme |
| identifica o QA que detectou APL-001/APL-002 | conforme |
| registra documentos corrigidos | conforme |
| registra busca posterior | conforme |
| declara pendencia de novo QA | conforme |
| nao declara aprovacao antecipada | conforme |
| nao apaga evidencias originais relevantes | conforme |

## 6. Busca de residuos

Busca direcionada executada:

```text
rg -n 'eixo de distribuição|eixo de distribuicao|arranjo.*aloca|arranjo.*reparte|arranjo.*distribui|aloca colunas|aloca linhas|reparte colunas|reparte linhas' docs/contratos/contrato_composicao_corpo.md docs/NOMENCLATURA.md
```

Classificacao das ocorrencias relevantes:

| Ocorrencia | Classificacao | Decisao |
|---|---|---|
| `NOMENCLATURA.md:1169-1171` | distribuicao explicitamente condicionada | nao conflitante |
| `NOMENCLATURA.md:1173-1175` | distribuicao explicitamente condicionada | nao conflitante |
| `NOMENCLATURA.md:1217-1219` | composicao correta / distincao terminologica | nao conflitante |
| `NOMENCLATURA.md:1225` | forma negada | nao conflitante |
| `contrato_composicao_corpo.md:285-288` | distribuicao explicitamente condicionada | nao conflitante |
| `contrato_composicao_corpo.md:294-295` | distribuicao explicitamente condicionada | nao conflitante |
| `contrato_composicao_corpo.md:837-844` | composicao correta + distribuicao condicionada | nao conflitante |
| `contrato_composicao_corpo.md:1030-1037` | relacao normativa ADR-0015 x ADR-0018 | nao conflitante |

Busca ampliada executada:

```text
rg -n 'arranjo|distribuicao|distribuição|ocupacao_vertical_terminal|ocupação vertical|altura natural|área alocada|area alocada' docs/contratos/contrato_composicao_corpo.md docs/NOMENCLATURA.md
```

Resultado: as ocorrencias remanescentes sao composicao correta, distribuicao
explicitamente condicionada, explicacao historica, exemplo nao normativo ou forma
negada. Nenhuma ocorrencia foi classificada como conflito normativo ativo.

Busca adicional por equivalencia/fallback `igual` em documentos ativos encontrou
apenas formas negadas, historicas/substitutivas ou a equivalencia nao relacionada
de `dashboard` presente/ausente em `contrato_composicao_corpo.md:167-168`.

## 7. Matriz D1-D10

| Decisao | Resultado | Evidencia |
|---|---|---|
| D1 | conforme | `contrato_composicao_corpo.md:280-288`, `837-844`; `NOMENCLATURA.md:1168-1175`, `1217-1225`; `contrato_tela_json.md:208-227` |
| D2 | conforme | `contrato_composicao_corpo.md:533-549`; `contrato_json_tela_minima.md:206-224`; `NOMENCLATURA.md:1226-1230` |
| D3 | conforme | `contrato_composicao_corpo.md:301-310`; `contrato_tela_json.md:214-219`; `NOMENCLATURA.md:1233-1235` |
| D4 | conforme | `contrato_composicao_corpo.md:651-659`; `NOMENCLATURA.md:1236-1238` |
| D5 | conforme | `contrato_composicao_corpo.md:551-556`; `NOMENCLATURA.md:1231-1232`; `contrato_json_tela_minima.md:224-228` |
| D6 | conforme | `contrato_composicao_corpo.md:558-567`; `contrato_tela_json.md:220-224`; `contrato_json_tela_minima.md:225-230` |
| D7 | conforme | `contrato_composicao_corpo.md:568-588`; `NOMENCLATURA.md:1239-1241` |
| D8 | conforme | `contrato_composicao_corpo.md:590-608`; `contrato_tela_json.md:224-226`; `NOMENCLATURA.md:1242-1245` |
| D9 | conforme | `contrato_processo_desenvolvimento.md:155-176` |
| D10 | conforme | `contrato_composicao_corpo.md:937-949`; `contrato_tela_json.md:222-224`; `RELATORIO_APLICACAO_ADR-0018.md:94-99` |

D1-D10 permanecem coerentes. A aplicacao nao decidiu altura minima, overflow,
truncamento, paginacao de `lancador`, rejeicao, degradacao, redistribuicao por
altura natural ou prioridade por tipo. Tambem nao criou matriz exaustiva
obrigatoria.

## 8. Integridade estrutural

Nos tres arquivos tocados pelo patch (`contrato_composicao_corpo.md`,
`NOMENCLATURA.md`, `RELATORIO_APLICACAO_ADR-0018.md`) foram verificados titulos,
subtitulos, numeracao, tabelas Markdown, blocos de codigo, referencias internas,
nomes de campos e nomes de ADRs.

Resultado: sem regressao estrutural observada. A correcao ficou localizada nos
trechos dos achados e nas anotacoes historicas do relatorio de aplicacao.

Os outros quatro documentos rastreados da aplicacao anterior
(`contrato_tela_json.md`, `contrato_json_tela_minima.md`,
`contrato_processo_desenvolvimento.md`, `INDICE_ADR.md`) permanecem coerentes com
a aplicacao original da ADR-0018; nao ha evidencia de alteracao nova indevida
durante o patch.

Tambem nao ha diff em `config/`, `tela/`, `docs/templates/`, testes ou codigo.

## 9. Escopo do patch e arquivos preservados

Alteracoes especificas do patch confirmadas:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`

Permaneceram intactos durante o patch, por ausencia de diff rastreado ou por
preservacao como artefatos nao rastreados/historicos:

- ADR-0018
- `RELATORIO_QA_ADR-0018.md`
- `RELATORIO_QA_APLICACAO_ADR-0018.md`
- H-0024
- `config/`
- `tela/`
- `docs/templates/`
- ADRs anteriores
- testes
- estado operacional Git

## 10. Achados

Nao ha achados bloqueantes, altos, medios ou baixos.

### OBS-001

- ID: `OBS-001`
- Severidade: observacao.
- Arquivo e linha: `docs/contratos/contrato_composicao_corpo.md:273-288`.
- Achado original relacionado: APL-001.
- Decisao ou autoridade afetada: ADR-0018 D1.
- Evidencia: a tabela de `contrato_composicao_corpo.md:273-276` ainda usa
  "reparte" na coluna "Efeito", mas o texto imediatamente subsequente
  (`contrato_composicao_corpo.md:280-288`) a qualifica de forma inequivoca como
  eixo repartido somente quando ha `distribuicao` explicita.
- Impacto: nao ha contradicao normativa ativa nem bloqueio de retomada do fluxo;
  o trecho subsequente neutraliza a leitura antiga.
- Categoria: `OBSERVACAO`.
- Proxima acao apropriada: nenhuma correcao exigida por este QA.

## 11. Resultado final

Status: `ADR_APPLICATION_APPROVED_WITH_NOTES`

Justificativa: APL-001 esta resolvido; APL-002 esta resolvido; D1-D10 permanecem
conformes; nao ha contradicao normativa ativa; nao ha achado bloqueante, alto,
medio ou baixo; resta apenas `OBS-001`, observacao sem prejuizo para a retomada
do fluxo; o escopo do patch esta correto; stage e stash permanecem preservados.

Proxima categoria: `RETOMAR_OU_RECRIAR_HANDOFF`

## 12. Alteracoes feitas por este QA

Criado somente:

- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`

Nenhum outro arquivo foi alterado por esta etapa.
