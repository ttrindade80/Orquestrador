---
name: historico-orquestrador
description: Registro compacto de itens encerrados
metadata:
  type: historico
  scope: orquestrador
---

# Histórico

## Regra

Somente itens encerrados pertencem a este histórico. Itens históricos não
permanecem em `docs/backlog.md` — no mesmo fechamento documental em que um
item é encerrado, ele é removido do backlog e registrado aqui. Este
histórico é um índice compacto de resultados; ele não substitui ADRs,
contratos, handoffs, relatórios ou commits — a evidência detalhada
permanece nesses documentos de origem. Dado desconhecido não é inventado:
quando data, referência ou detalhe não puder ser confirmado, usa-se
`NAO_CONFIRMADA` ou a omissão explícita do campo. Reabertura futura de um
item aqui registrado exige novo registro ativo em `docs/backlog.md`, não a
edição da entrada histórica.

## Concluídos

### DOC-0001 — ADR: permitir `menu` em matriz

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/adr/ADR-0001-menu-suporta-matriz.md
**Resumo:** `menu` passou a suportar fila horizontal e matriz, com eixo `distribuicao_menu` calculado pela largura do terminal.

### DOC-0002 — ADR: `menu` usa sobra à direita

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/adr/ADR-0002-menu-sobra-direita.md
**Resumo:** Alinhamento horizontal do `menu` mudou de centralizado para alinhado à esquerda com sobra de espaço à direita.

### DOC-0003 — ADR: vãos elásticos do `menu`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/adr/ADR-0003-vaos-elasticos-menu.md
**Resumo:** Vãos do `menu` passaram a ter mínimo/máximo elástico, parametrizados em `config/layout_menu.json`.

### DOC-0004 — ADR: campos `cor_inativo` e `cor_alerta`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
**Resumo:** Dois campos novos adicionados ao schema de estilo: cor de elemento inativo e cor de alerta de limite atingido.

### DOC-0005 — Migrar presets de estilo para `config/estilo.json`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Resumo:** Presets de borda, chip, `selecionado` e `incluido` migrados para `config/estilo.json`; tabelas de valores removidas de `NOMENCLATURA.md` e `contrato_estilo.md`.

### DOC-0006 — Criar contrato da barra_de_menus

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/contratos/contrato_barra_de_menus.md
**Resumo:** Contrato da `barra_de_menus` criado, distinguindo-a do `menu` e formalizando o comportamento de `[Esc]` e `[⏎]`.

### DOC-0007 — Formalizar cabecalho

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-05
**Referências:** docs/contratos/contrato_cabecalho.md
**Resumo:** `cabecalho` formalizado como domínio próprio, com `config/cabecalho.json` e contrato ativo criados.

### DOC-0008 — Criar contrato do `lancador`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Referências:** docs/contratos/contrato_lancador.md
**Resumo:** Contrato do `lancador` criado com estrutura mínima de título e itens (`chip`, `texto`, `tela_destino`).

### DOC-0009 — Migrar artefatos de `menu` para `lancador`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Resumo:** Artefatos existentes migrados do termo `menu` para `lancador`; `config/lancador.json` tornou-se canônico.

### DOC-0010 — ADR: lancador não é corpo navegável por [✥]

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Referências:** docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
**Resumo:** ADR-0005 aplicada, restringindo `[✥]` ao corpo tipo `dado`; aprovada após ajuste.

### DOC-0011 — ADR: renomeação `dado` → `console` e `Info` → `dashboard`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Referências:** docs/adr/ADR-0006-renomeacao-console-dashboard.md
**Resumo:** Taxonomia de tipos de corpo renomeada para `console`, `lancador` e `dashboard`.

### DOC-0012 — Aplicar ADR-0006 em nomenclatura, contratos e configs

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Resumo:** ADR-0006 aplicada em nomenclatura, contratos e configs ativos; `config/layout_console.json` criado como canônico.

### DOC-0013 — ADR: tela de processamento é composição de tipos existentes

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Referências:** docs/adr/ADR-0007-tela-processamento-composicao.md
**Resumo:** Tela de processamento registrada como composição de `console` + `dashboard` + chips específicos, não como quarto tipo de corpo.

### DOC-0014 — Aplicar ADR-0007 em nomenclatura e contratos

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Resumo:** ADR-0007 aplicada em `NOMENCLATURA.md`, `contrato_composicao_corpo.md` e `contrato_barra_de_menus.md`.

### DOC-0015 — Consolidar, revisar e commitar ciclo DOC-0010 a DOC-0014

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-06
**Referências:** commit `6b609ed`
**Resumo:** Consolidação, revisão de diff e commit documental do pacote ADR-0005/ADR-0006/ADR-0007 e da taxonomia `console`/`lancador`/`dashboard`.

### DOC-0016 — ADR: modelo de configuração por tela

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/adr/ADR-0008-modelo-configuracao-por-tela.md
**Resumo:** Registrado o modelo de JSON por tela, substituindo o modelo de JSON por domínio/componente.

### DOC-0017 — Aplicar ADR-0008 em `NOMENCLATURA.md`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Resumo:** Política de JSON por domínio substituída pelo modelo de JSON por tela em `NOMENCLATURA.md`.

### DOC-0019 — Revisar `dashboard` conforme ADR-0008

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** NAO_CONFIRMADA
**Referências:** docs/adr/ADR-0008-modelo-configuracao-por-tela.md
**Resumo:** `dashboard` registrado como tipo mínimo — não navegável por `[✥]`, não obrigatório, com moldura própria e sem conteúdo universal fixo.

### DOC-0020 — Revisar `lancador` conforme ADR-0008

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_lancador.md
**Resumo:** `contrato_lancador.md` revisado (versão 0.2) como instância configurável por tela, com `id` e itens (`id`, `chip`/tecla, `texto`, `tela_destino`) obrigatórios.

### DOC-0021 — Revisar `barra_de_menus` conforme ADR-0008

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_barra_de_menus.md
**Resumo:** `contrato_barra_de_menus.md` revisado (versão 0.2): `tela.json` como fonte da lista concreta de chips; `[✥]` restrito a `console` navegável.

### DOC-0022 — Atualizar `docs/INDICE.md` após aplicação da ADR-0008

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** NAO_CONFIRMADA
**Referências:** docs/adr/ADR-0008-modelo-configuracao-por-tela.md
**Resumo:** Descrição da estrutura esperada e da função de `config/` em `docs/INDICE.md` atualizada para não priorizar o modelo antigo de JSON por domínio/componente.

### DOC-0023 — Criar contrato do schema de `tela.json`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_tela_json.md
**Resumo:** Contrato de `tela.json` criado, com estrutura obrigatória `schema`, `id`, `cabecalho`, `corpo` e `barra_de_menus`.

### DOC-0024 — Revisar `console` como container genérico

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_console.md
**Resumo:** Contrato do `console` criado como container genérico de itens heterogêneos declarado no `tela.json`.

### DOC-0025 — Aplicar ADR-0008 em `contrato_composicao_corpo.md`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Resumo:** `contrato_composicao_corpo.md` atualizado (versão 0.2) para refletir composição declarada no `tela.json`, não hardcoded.

### DOC-0026 — Criar contrato da classe `chip`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_chip.md
**Resumo:** Contrato da classe `chip` criado, com campos mínimos, tipos conceituais e ações declarativas whitelisted.

### DOC-0027 — Ajustar critérios de validação do `contrato_console` pós-QA

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md
**Resumo:** Seção 16 de `contrato_console.md` expandida para espelhar os campos mínimos definidos na seção 3.

### DOC-0028 — Consolidar Fase 0 após ADR-0008 na tela base

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/relatorios/RELATORIO_CONSOLIDACAO_FASE_0_ADR-0008_TELA_BASE.md
**Resumo:** Consolidação do ciclo ADR-0008 nos contratos centrais da tela base; resultado `LIBERADO_COM_PENDENCIAS_NAO_BLOQUEANTES`.

### DOC-0029 — ADR: caminho, nomenclatura e formato dos JSONs de tela

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/adr/ADR-0009-caminho-formato-jsons-tela.md
**Resumo:** Caminho canônico `config/telas/<id>.json` e regras de nomenclatura registrados; `DOC-B010` encerrado.

### DOC-0030 — Ajustar draft da tela raiz pós-QA DOC-B011

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/relatorios/RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON.md
**Resumo:** Ajustes pós-QA (problemas P1–P4) aplicados a `config/telas/orquestrador.json`.

### DOC-0031 — Consolidação final pré-commit da Fase 0 / ADR-0008 / tela raiz

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/relatorios/RELATORIO_CONSOLIDACAO_FINAL_FASE_0_ADR-0008_TELA_RAIZ.md
**Resumo:** Consolidação final do pacote ADR-0008/ADR-0009/tela raiz; status `PRONTO_PARA_COMMIT`.

### DOC-0032 — Auditoria e arquivamento histórico/transicional pós-ADR-0008/ADR-0009

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/relatorios/RELATORIO_ARQUIVAMENTO_DOC-0032_HISTORICOS_TRANSICIONAIS.md
**Resumo:** Auditoria de artefatos históricos/transicionais concluída; nenhum arquivo movido; resultado `APROVADO_COM_RESSALVAS`.

### DOC-B006 — Definir contrato/classe `chip`

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/contratos/contrato_chip.md
**Resumo:** Contrato `chip` criado (DOC-0026); registry completo de ações e tipos permanece pendente em `DOC-B009`.

### DOC-B010 — Definir formato real e caminho dos JSONs de tela

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** docs/adr/ADR-0009-caminho-formato-jsons-tela.md
**Resumo:** ADR-0009 fechou caminho canônico, nomenclatura e organização dos JSONs de tela.

### DOC-B011 — Criar draft do JSON da tela raiz do Orquestrador

**Resultado:** CONCLUIDO
**Origem:** build_docs
**Data:** 2026-07-07
**Referências:** config/telas/orquestrador.json
**Resumo:** Primeiro draft real da tela raiz do Orquestrador criado, com cabeçalho, corpo e barra_de_menus declarados.

### ITEM-0002 — Navegação simples e seleção única em console

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-07-26
**Referências:** ADR-0031; H-0040; commit `13d743d2def11ea4e32b936d9b5accb71346dc5c`
**Resumo:** Navegação simples, foco entre consoles e seleção única implementados, validados e encerrados no Git.

### ITEM-0022 — Modularizacao estrutural do runtime de telas

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-04
**Referências:** docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md; docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md; docs/handoff/H-0047-modularizacao-estrutural-do-loader.md; docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md; docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0048_P01.md
**Resumo:** Modularizacao estrutural do runtime de telas concluida em tres handoffs sequenciais. O H-0046 extraiu a producao do renderizador para `tela/renderizacao/`; o H-0047 extraiu o carregamento para `tela/carregamento/`; e o H-0048 reorganizou o monolito de testes em oito modulos proprietarios, um modulo comum e um runner, preservando `tela/teste_renderizador.py` como fachada compativel. As fachadas publicas, o comportamento, o schema, a politica e a API permaneceram inalterados. O fechamento tecnico confirmou 371 testes do renderizador, runner direto com 1308/1308 verificacoes, 365 testes externos relacionados e suite completa com 970 testes aprovados.

### ITEM-0020 — Chip de escolha entre execucao real e dry-run

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-05
**Referências:** docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md; docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md; docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0050_P06.md; docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0050_P04.md; docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0050_R03.md; docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0050_R04.md
**Resumo:** O controle universal reutilizavel de escolha entre execucao real e dry-run foi concluido. O schema raiz fechado `controle_execucao.modo_inicial` aceita somente `executar` e `dry_run`; a compatibilidade pertence ao registro autoritativo das acoes; o modo e unico por instancia, capturado explicitamente na requisicao e preservado no retorno. D-DRY-12 consolidou os rotulos visuais `[Ins] Real` e `[Ins] Simulação`, com aparencia normal em Real e `cor_alerta` em Simulação, preservando `[⏎] Executar` como acao separada e mantendo sem delta a especializacao focal `[Ins] Dry-Run` do H-0044. O fechamento tecnico confirmou 268 testes focais, 1037 testes na suite completa, 17 provas isoladas do H-0050, validacao manual funcional R03 em 7/7 e validacao complementar R04 em 4/4.

## Cancelados

### DOC-B003 — Segunda pauta de "estilo de exibição de dados no corpo"

**Resultado:** CANCELADO
**Origem:** build_docs
**Data:** 2026-07-27
**Resumo:** Segundo ponto de estilo de exibição de dados no corpo, mencionado em sessão e nunca descrito pelo usuário.
**Motivo:** O objeto da segunda pauta de estilo não foi descrito de forma suficiente e não será preservado como pendência.

### DOC-B004 — Reorganização corpo × dashboard e alinhamento do `dashboard`

**Resultado:** CANCELADO
**Origem:** build_docs
**Data:** 2026-07-27
**Resumo:** Reorganização de telas só-visualização usando `dashboard` como conteúdo principal e telas de processo usando `corpo`, incluindo alinhamento do `dashboard`.
**Motivo:** Foi cancelada a reorganização corpo × dashboard e a pendência de alinhamento associada.

### DOC-B007 — Arquivar artefatos históricos/transicionais no fechamento da Fase 0

**Resultado:** CANCELADO
**Origem:** build_docs
**Data:** 2026-07-27
**Resumo:** Pendência de arquivamento de artefatos históricos/transicionais no fechamento da Fase 0 do ciclo ADR-0008.
**Motivo:** A pendência legada de arquivamento foi encerrada; esta ADR (ADR-0033) estabelece solução documental própria.

### DOC-B008 — Definir contratos/classes de itens internos de `console`

**Resultado:** CANCELADO
**Origem:** build_docs
**Data:** 2026-07-27
**Resumo:** Taxonomia, campos obrigatórios, renderização, quebra de página, navegabilidade e ação de Enter de cada tipo interno de item do `console`.
**Motivo:** Soluções posteriores tornaram desnecessária a pendência legada sobre tipos internos do console.

### DOC-B009 — Definir registry de tipos válidos

**Resultado:** CANCELADO
**Origem:** build_docs
**Data:** 2026-07-27
**Resumo:** Registry de tipos reconhecidos pelo renderer — tipos de corpo, itens de `console`, chip, filtro e ação registrada.
**Motivo:** Soluções posteriores tornaram desnecessária a pendência legada sobre registry de tipos ou ações.

## Substituídos

Nenhum item registrado.

## Incompatíveis

Nenhum item registrado.

### ITEM-0006 — Selecao multipla no console

**Resultado:** CONCLUIDO
**Data:** 2026-07-29
**Referências:** docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md; docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md; docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md; docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md; docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md; docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md; docs/handoff/H-0043-carregamento-apresentacao-tela-padrao-resultado.md; docs/handoff/H-0044-integracao-fluxo-focal-dry-run-restauracao-origem.md; docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0044.md
**Resumo:** Selecao multipla concluida em quatro handoffs: estado, comandos e apresentacao pelo H-0041; executor focal sintetico reversivel pelo H-0042; tela padrao de resultado pelo H-0043; integracao completa com toggle Dry-Run, transicao atomica, suspensao e restauracao da origem pelo H-0044. O patch P01 do H-0044 foi aprovado, a suite completa alcançou 763 testes aprovados e a validacao manual terminou com dez de dez roteiros aprovados.

### ITEM-0011 — Cores de estado inativo e de alerta

**Resultado:** CONCLUIDO
**Data:** 2026-07-29
**Referências:** docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md; docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md; docs/contratos/contrato_estilo.md; config/estilo.json; tela/loader.py; tela/renderizador.py
**Resumo:** `cor_inativo: cinza` e `cor_alerta: amarelo` ficaram definidas no estilo global e traduzidas pelo runtime. O H-0044 materializou `cor_alerta` em `EstiloResolvido`, exigiu o campo sem fallback silencioso e comprovou seu consumo pelo renderer no destaque ativo do chip `[Ins] Dry-Run`, sem hardcoding funcional de cor ou ID.

### ITEM-0003 — Paginacao interativa do console

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-03
**Referências:** docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md; docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md; docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P25.md; docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0045.md
**Resumo:** Paginacao interativa limitada implementada com estado independente por console, comandos explicitos de pagina, indicador X/Y, reconciliacao de cursor por item logico, selecao persistente, tres politicas de quebra, conteudo multilinha, conjunto vazio e paginas somente de continuacao. O ciclo terminou com 970 testes aprovados, matriz tecnica de 60 dimensoes, validacao manual consolidada das etapas 6/17 a 17/17 e aprovacao das correcoes focais de Esc dinamico, largura horizontal e terminal insuficiente. O encerramento do ITEM-0003 removeu o bloqueio tecnico do ITEM-0018.

### ITEM-0015 — Aplicar ADR-0008 aos contratos de cabeçalho e estilo

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-04
**Referências:** docs/adr/ADR-0008-modelo-configuracao-por-tela.md; docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md; docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0049.md
**Resumo:** A aplicação remanescente da ADR-0008 foi concluída. Os oito parâmetros de apresentação do cabeçalho passaram a pertencer ao JSON estrutural de cada tela; 72 telas foram migradas com baseline geométrico 0/1 e capitalização literal `preservar` para a descrição; oito conteúdos externos foram mantidos intactos; loader, modelo, renderer e geometria passaram a consumir o schema local fechado; 58 fixtures antigas foram adequadas; a configuração global obsoleta foi removida; e a suíte integral terminou com 998 testes aprovados.

### ITEM-0007 — Navegacao multinivel do console

**Resultado:** CONCLUIDO
**Origem:** backlog
**Referências:** H-0052; H-0053; H-0054; H-0055; commit `cbd9946`
**Resumo:** Navegacao multinivel do console concluida pelos H-0052 (`nivel_unico`), H-0053 (`arvore_colapsavel`), H-0054 (`selecao_multinivel`) e H-0055 (`dois_niveis_por_foco`), com fechamento final pelo H-0055 no commit `cbd9946`; capacidades futuras foram separadas em ITEM-0023 a ITEM-0026.

### ITEM-0017 — Capacidade de pop-up modal genérico de decisão

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-11
**Referências:** docs/adr/ADR-0044-popup-modal-generico-de-decisao.md; H-0056; H-0057; H-0058; H-0059
**Resumo:** Pop-up modal genérico concluído pelos H-0056 a H-0059, com modalidade textual, aborto sem payload, geometria dinâmica e resize, lista navegável e marcação exclusiva/múltipla, e confirmação `CONFIRMADO` com `valor` e binding no consumidor. ITEM-0017 concluído.

### ITEM-0028 — Resize das formações da lista do pop-up antes de terminal pequeno

**Resultado:** CONCLUIDO
**Data:** 2026-08-12
**Referências:** docs/adr/ADR-0045-resize-responsivo-formacoes-popup-marcacao.md; docs/handoff/H-0060-resize-responsivo-formacoes-popup-marcacao.md; docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0060.md
**Resumo:** ITEM-0028 concluído com ADR-0045 e H-0060: resize coluna → matriz → linha antes de terminal pequeno; correção focal da integração da altura física em `tela/renderizacao/tela.py`; QA automatizado final aprovado (23 testes de integração, 63 do pop-up, 15 de demo e 1175 canônicos); validação manual TTY aprovada; fechamento em 2026-08-12.

### ITEM-0010 — Tela de escolha do estilo global

**Resultado:** CONCLUIDO
**Origem:** backlog
**Data:** 2026-08-14
**Referências:** docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md; docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md; docs/relatorios/RELATORIO_FECHAMENTO_H-0071_ADR-0046.md
**Resumo:** Escolha e aplicação do estilo global concluídas com a composição reconciliada de chips multitecla, distinção Curva `╭`/`╮` × Ornamental `❲`/`❳`, paginação `[PgUp/PgDn]` como unidade visual única e preservação de `cor_inativo`; o fechamento registrou validação manual TTY aprovada e a suíte final de 1381 testes aprovados e uma falha conhecida não causal do H-0071 P05.

### ADR-0047 / H-0072 / H-0073 — Formatação de filhos em dois níveis por foco

**Resultado:** CONCLUIDO
**Data:** 2026-08-16
**Referências:** docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md; docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md; docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md; docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0073_POS_H0072_P05_P06.md
**Resumo:** Capacidade genérica concluída para formatar filhos de `dois_niveis_por_foco`, com tabulação estrutural dinâmica 5..10, designador configurável por prefixo/sufixo, apresentações texto/tabela, alinhamento global, wrap e correção ANSI no resize. Aplicação real concluída em H-0055 (preservando `A)`) e H-0063 (tabela `preset`/`amostra`, espaçamento 3..8 e fundo de “Destaque Fundo” restrito ao chip). A revalidação manual final foi aprovada, com VM-H0073-001 e VM-H0073-002 resolvidos. H-0070 permanece resíduo histórico não causal, fora deste ciclo.
\n