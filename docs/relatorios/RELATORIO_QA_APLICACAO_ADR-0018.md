# RELATORIO_QA_APLICACAO_ADR-0018

## 1. Identificação

Relatório: `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`

Etapa executada: `QA_APLICACAO_ADR`

ADR auditada: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`

Aplicação auditada: `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`

Data da auditoria: 2026-07-11

Status principal: `ADR_APPLICATION_REJECTED`

## 2. Escopo

Auditoria formal da aplicação documental da ADR-0018 nos seis documentos normativos autorizados:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`

Esta etapa não corrigiu documentos, não alterou ADR, H-0024, JSON, código, testes, stash, stage, branch ou histórico Git. Criou somente este relatório.

## 3. Estado Git

| Comando | Resultado |
|---|---|
| `git status --short` | 6 documentos rastreados modificados; artefatos documentais não rastreados presentes; stage vazio |
| `git status` | branch `master`; nenhum arquivo staged |
| `git branch --show-current` | `master` |
| `git rev-parse HEAD` | `3332773a3f10e716115a164148af323fa86e608f` |
| `git log -1 --oneline` | `3332773 feat: implementa redimensionamento reativo da TUI` |
| `git diff --check` | sem saída |
| `git diff --stat` | 6 arquivos, 250 inserções, 11 remoções |
| `git diff --name-only` | somente os 6 documentos normativos autorizados |
| `git diff --cached --stat` | sem saída |
| `git diff --cached --name-only` | sem saída |

Arquivos rastreados modificados confirmados:

- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`

Não foram identificados conflito Git, operação Git em andamento, alteração em JSON, alteração em código, alteração em testes, alteração rastreada da ADR-0018 ou alteração rastreada do H-0024.

## 4. Estado do stash

| Comando | Resultado |
|---|---|
| `git stash list` | `stash@{0}: pre-H-0022 recuperado apos drop acidental` |
| `git rev-parse stash@{0} 2>/dev/null || true` | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |

O stash esperado foi preservado. Nenhum comando de manipulação de stash foi executado.

## 5. Segurança entre sessões

Antes da escrita deste relatório, foram feitas apenas verificações de leitura. Não foram encontrados `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, diretórios de rebase/sequencer ou locks Git no workspace. O caminho `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md` não existia antes da criação.

## 6. Artefatos auditados

Lidos integralmente:

- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/relatorios/RELATORIO_QA_ADR-0018.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`

Auditados na versão atual:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`

Consultados como evidência operacional e histórica, sem autoridade normativa:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`

## 7. Autoridades

Autoridades relacionadas consultadas:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`

Relatórios, handoff e implementação foram usados somente como evidência histórica.

## 8. Método

1. Verificação de estado Git, stage, stash e caminho do relatório.
2. Leitura integral da ADR-0018, do QA da ADR e do relatório de aplicação.
3. Comparação do diff rastreado contra a lista fechada de arquivos autorizados.
4. Auditoria semântica D1-D10 nos documentos modificados.
5. Busca contextual de resíduos nos documentos normativos ativos.
6. Verificação estrutural de seções, referências internas, blocos de código, exemplos e índice.
7. Registro de achados sem correção.

Não foi encontrado verificador documental estabelecido e diretamente aplicável por busca de arquivos/scripts. Suítes de código não foram executadas, por ser etapa documental.

## 9. Matriz D1-D10

| Decisão | Documentos em que deveria aparecer | Trechos efetivamente atualizados | Conformidade | Ausência, contradição ou ampliação |
|---|---|---|---|---|
| D1 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `NOMENCLATURA.md`, `INDICE_ADR.md` | `contrato_composicao_corpo.md:280-288`, `contrato_tela_json.md:208-227`, `NOMENCLATURA.md:1203-1247`, `INDICE_ADR.md:48` | `CONTRADITORIA` | Persistem regras normativas ativas que colapsam arranjo e distribuição: `contrato_composicao_corpo.md:837-839` e `NOMENCLATURA.md:1168-1171`. |
| D2 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:533-549`, `contrato_tela_json.md:208-214`, `contrato_json_tela_minima.md:206-230`, `NOMENCLATURA.md:1222-1226` | `CONFORME` | Não foi encontrada formulação ativa de ausência como fallback `igual`; ocorrências remanescentes são negadas, históricas ou de substituição. |
| D3 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:301-310`, `contrato_tela_json.md:214-219`, `NOMENCLATURA.md:1229-1231` | `CONFORME` | Distribuição explícita é descrita como alocação integral da área útil aos filhos diretos. |
| D4 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:651-659`, `contrato_tela_json.md:217-219`, `NOMENCLATURA.md:1232-1235` | `CONFORME` | Preenchimento interno foi registrado sem criar regra especial para Orquestrador. |
| D5 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:551-556`, `contrato_tela_json.md:220-221`, `contrato_json_tela_minima.md:210-228`, `NOMENCLATURA.md:1227-1228` | `CONFORME` | `igual` permanece explícito e não reaparece como fallback de ausência. |
| D6 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md` | `contrato_composicao_corpo.md:558-567`, `contrato_tela_json.md:220-224`, `contrato_json_tela_minima.md:225-230` | `CONFORME` | Percentual preserva um valor por filho direto, soma 100 e cálculo genérico sobre área disponível. |
| D7 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:569-588`, `contrato_tela_json.md:220-224`, `contrato_json_tela_minima.md:225-230`, `NOMENCLATURA.md:1236-1238` | `CONFORME` | Vetores `[1,1,1]`, `[2,1,2]`, `[1,3,1]`, `[5,2,7]` aparecem como exemplos não exaustivos, sem default ou hardcode. |
| D8 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `NOMENCLATURA.md` | `contrato_composicao_corpo.md:590-608`, `contrato_tela_json.md:224-226`, `NOMENCLATURA.md:1239-1241` | `CONFORME` | Conteúdo maior que a cota permanece lacuna externa; não houve decisão de mínimo, overflow, truncamento, paginação, rejeição, degradação ou prioridade. |
| D9 | `contrato_processo_desenvolvimento.md` | `contrato_processo_desenvolvimento.md:155-176` | `CONFORME` | Preserva alteração puramente declarativa sem handoff próprio e exige JSON no mesmo handoff quando necessário à implementação. |
| D10 | `contrato_composicao_corpo.md`, `contrato_tela_json.md`, relatório de aplicação | `contrato_composicao_corpo.md:937-949`, `contrato_tela_json.md:222-224`, `RELATORIO_APLICACAO_ADR-0018.md:94-95` | `CONFORME` | Não criou matriz exaustiva, handoff de testes ou obrigação de todas as combinações no ciclo. |

## 10. Análise por documento

### `contrato_composicao_corpo.md`

Conforme em D2-D8: a ausência de `distribuicao` foi dissociada de `igual`; `igual` permanece explícito; `percentual` e `fracao` permanecem genéricos; preenchimento interno foi registrado; conteúdo maior que a cota permanece lacuna externa.

Defeito local: a regra ativa R-17 ainda afirma que o arranjo de um container declara o "eixo de distribuição" dos filhos diretos (`contrato_composicao_corpo.md:837-839`). Essa formulação contradiz D1, porque a ADR-0018 exige que arranjo seja ordem/composição e distribuição seja mecanismo separado.

### `contrato_tela_json.md`

Conforme. A seção de `corpo.distribuicao` diferencia ausência de distribuição explícita, preserva modos explícitos, descreve alocação integral da altura útil e separa configuração concreta de algoritmo genérico. Não foram identificadas contradições ativas neste arquivo.

### `contrato_json_tela_minima.md`

Conforme. As duas formulações antigas de ausência equivalente a `igual` foram removidas/substituídas. O campo `distribuicao` continua opcional; `igual`, `percentual` e `fracao` permanecem válidos quando declarados.

### `contrato_processo_desenvolvimento.md`

Conforme. A seção 10.1 distingue mudança puramente declarativa de JSON, que pode dispensar handoff próprio quando o suporte já existe, de alteração JSON necessária para handoff de implementação, que deve integrar o mesmo handoff.

### `NOMENCLATURA.md`

Parcial/contraditório em D1. A nova seção 14.1 diferencia `corpo.arranjo = "vertical"`, `ocupacao_vertical_terminal` e `corpo.distribuicao`; porém a seção ativa 14 preserva itens sem qualificador que afirmam: "`arranjo = horizontal` aloca colunas" e "`arranjo = vertical` aloca linhas" (`NOMENCLATURA.md:1168-1171`). Isso mantém colapso normativo entre arranjo e alocação/distribuição.

Conforme nos demais pontos auditados: ausência ≠ `igual`, preenchimento interno quando explícito, `fracao` genérica e conteúdo maior que a cota como lacuna externa.

### `INDICE_ADR.md`

Conforme. A entrada da ADR-0018 foi adicionada com identificador, título, data e status no padrão do índice. Não declara antecipadamente QA da aplicação aprovada.

## 11. Relação com ADR-0013

Conforme. A ocupação da altura da janela permanece válida; a área útil do corpo continua situada entre `cabecalho` e `barra_de_menus`; a ADR-0018 apenas diferencia o destino da sobra na ausência ou presença de distribuição explícita. Não houve alteração indevida da obtenção de dimensões.

## 12. Relação com ADR-0015

Parcial por causa de D1. A aplicação preserva filhos diretos, modos `igual`/`percentual`/`fracao`, maiores restos, desempate, árvore, grupos, profundidade e preenchimento de área alocada. Contudo, duas formulações herdadas da ADR-0015 continuam ativas e não foram suficientemente qualificadas após a ADR-0018: R-17 em `contrato_composicao_corpo.md` e os itens 12-13 da seção 14 de `NOMENCLATURA.md`.

Cada documento ativo identifica em algum ponto a prevalência da ADR-0018 sobre ausência ≡ `igual`, mas nem todos removeram ou neutralizaram a leitura antiga em que arranjo aloca/reparte área.

## 13. Relação com ADR-0017

Conforme. Permanecem intactos: obtenção de largura e altura, cadeia de fallback, redimensionamento reativo, uso das dimensões atuais e ausência de nova arquitetura de eventos ou sinais.

## 14. Busca de resíduos

Busca contextual executada nos documentos normativos ativos por:

`ausência equivale a igual`, `ausencia equivale a igual`, `ausência de distribuição`, `ausencia de distribuicao`, `default igual`, `modo igual por omissão`, `modo igual por omissao`, `distribuicao ausente`, `distribuição ausente`, `preenchimento externo`, `preenchimento interno`, `altura natural`, `área alocada`, `area alocada`, `ADR-0015`, `ADR-0018`.

Classificação das ocorrências relevantes:

| Ocorrência | Classificação | Observação |
|---|---|---|
| `contrato_composicao_corpo.md:540-556` | forma negada / normativa conforme | Ausência não equivale a `igual`; `igual` explícito. |
| `contrato_json_tela_minima.md:206-230` | forma negada / normativa conforme | Remove equivalência de ausência com `igual`. |
| `contrato_tela_json.md:208-227` | normativa conforme | Distingue ausência, distribuição explícita e algoritmo genérico. |
| `NOMENCLATURA.md:1222-1228` | forma negada / normativa conforme | Ausência de `corpo.distribuicao` não é `igual`. |
| `contrato_composicao_corpo.md:547-549`, `1013-1043` | explicação da substituição | Relação ADR-0015 × ADR-0018. |
| `NOMENCLATURA.md:1205-1208` | explicação da substituição | Relação ADR-0015 × ADR-0018. |
| `contrato_composicao_corpo.md:837-839` | normativa conflitante | R-17 ainda diz que arranjo declara eixo de distribuição. |
| `NOMENCLATURA.md:1168-1171` | normativa conflitante | Itens 12-13 ainda dizem que arranjo horizontal/vertical aloca colunas/linhas. |
| `contrato_composicao_corpo.md:166-167` | ocorrência não relacionada | Equivalência de presença/ausência de `dashboard`, conceito distinto. |

Não há resíduo ativo de ausência ≡ `igual`; há resíduo ativo de colapso arranjo/distribuição.

## 15. Integridade estrutural

`git diff --check` não apontou conflitos ou problemas de whitespace. Não foram encontrados marcadores de conflito nos arquivos auditados.

As referências internas principais adicionadas existem: `contrato_composicao_corpo.md` possui seções 4.8, 4.9, 5.7, 5.9 e 10; `contrato_tela_json.md` possui seção 8; `contrato_json_tela_minima.md` possui seções 6.2 e 6.3; `contrato_processo_desenvolvimento.md` possui seção 10 e subseção 10.1; `NOMENCLATURA.md` possui seção 14.1.

Defeito semântico, não estrutural: a integridade de títulos, links e blocos não elimina a contradição normativa ativa em D1.

## 16. Regra de JSON em handoff

Conforme. `contrato_processo_desenvolvimento.md:155-176` preserva a regra de que alteração puramente declarativa pode dispensar handoff próprio quando suporte, schema, loader/modelo e renderer já existem; e estabelece que alteração JSON necessária para implementar, demonstrar ou validar handoff que também altera código deve constar no mesmo handoff, com caminho, alteração, valores decididos, validação sintática, critérios e testes.

Não foi criada a regra incorreta de que toda alteração JSON exige handoff próprio.

## 17. Tratamento de testes

Conforme. A documentação aplicada distingue capacidade genérica do algoritmo, configuração concreta de tela e cobertura ampliada. Não cria matriz exaustiva, não cria handoff de testes, não exige todas as combinações no mesmo ciclo e não dispensa testes mínimos da capacidade implementada.

## 18. Nota A-001

Conforme como tratamento não bloqueante. A ADR-0018 não foi alterada durante a aplicação. A aplicação não tentou corrigir a nota baixa A-001 do QA da ADR nem alterou o H-0024. Os documentos aplicados não transformaram a ambiguidade de redação do H-0024 em nova regra.

Permanece claro no relatório de aplicação que o H-0024 deve ser corrigido ou recriado somente após a aplicação documental ser aprovada em QA próprio. A nota A-001 não foi reclassificada como defeito da aplicação.

## 19. Escopo dos arquivos

Conforme quanto ao escopo físico dos arquivos rastreados. Somente os seis documentos rastreados autorizados foram modificados. `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md` está criado como arquivo não rastreado. A ADR-0018, o H-0024, JSONs, código, testes, templates, config e estado operacional não apresentam alteração rastreada.

Arquivos não rastreados relevantes foram tratados como evidência/contexto preexistente e não como prova de ausência por diff vazio.

## 20. Achados

### APL-001

- Severidade: alta.
- Categoria: `APLICACAO_LOCAL`.
- Arquivo e linha: `docs/contratos/contrato_composicao_corpo.md:837`; `docs/NOMENCLATURA.md:1168`; `docs/NOMENCLATURA.md:1170`.
- Decisão ou autoridade afetada: ADR-0018 D1; relação com ADR-0013 e ADR-0015.
- Evidência: R-17 afirma que o arranjo declara o "eixo de distribuição"; a NOMENCLATURA afirma que `arranjo = horizontal` aloca colunas e `arranjo = vertical` aloca linhas.
- Impacto: mantém contradição normativa ativa com a ADR-0018, que determina que arranjo é ordem/composição e não reparte/aloca área sozinho. Isso pode reabrir a leitura antiga que colapsa arranjo vertical, ocupação vertical e distribuição.
- Categoria: `APLICACAO_LOCAL`.
- Próxima ação apropriada: `PATCH_DOCUMENTACAO`.

### APL-002

- Severidade: média.
- Categoria: `EVIDENCIA`.
- Arquivo e linha: `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md:166`; `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md:246`.
- Decisão ou autoridade afetada: QA da aplicação; busca de resíduos.
- Evidência: o relatório de aplicação afirma que a busca de resíduos encontrou somente formas negadas, substituição histórica e equivalência não relacionada de `dashboard`, mas deixou de registrar as ocorrências normativas ativas de arranjo como alocação/distribuição em `contrato_composicao_corpo.md` e `NOMENCLATURA.md`.
- Impacto: o relatório de aplicação subestima resíduo normativo relevante para D1. O defeito material está nos documentos normativos; este achado registra a inconsistência do relatório de aplicação.
- Categoria: `EVIDENCIA`.
- Próxima ação apropriada: `PATCH_DOCUMENTACAO`.

## 21. Riscos residuais

- Enquanto APL-001 persistir, handoffs futuros podem interpretar `corpo.arranjo = "vertical"` como gatilho de alocação/repartição mesmo sem `corpo.distribuicao`.
- A aplicação de D2-D10 está amplamente coerente, mas D1 é fundacional para impedir a leitura antiga.
- H-0024 continua evidência histórica e permanece pendente de correção ou recriação somente após aprovação da aplicação documental.

## 22. Classificação final

`ADR_APPLICATION_REJECTED`

Justificativa: há defeito local corrigível de aplicação documental. A ADR-0018 foi propagada corretamente em D2-D10, mas D1 não ficou livre de contradições normativas ativas nos documentos aplicados.

## 23. Única próxima categoria

`PATCH_DOCUMENTACAO`

## 24. Arquivos criados ou alterados pelo QA

Criado por este QA:

- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`

Não alterado por este QA:

- ADR-0018
- contratos
- nomenclatura
- índice ADR
- H-0024
- JSON
- código
- testes
- stash
- stage
- branch
- histórico Git
