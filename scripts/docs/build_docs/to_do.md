---
name: to_do-build-docs
description: Lista de tarefas de construcao de documentacao (nao e backlog de implementacao)
metadata:
  type: to_do
  scope: build_docs
  status: em_andamento
  criado_em: 2026-07-05
---

# To Do — Construção de Documentação

## Regra

Este arquivo é exclusivo da fase de **construção de documentação**
(`NOMENCLATURA.md`, contratos, ADRs, `config/*.json`). Não é backlog de
implementação de código — isso vive em `docs/backlog.md`, separado, e só
começa a ser populado depois que a documentação relevante estiver pronta.

Esta pasta inteira (`scripts/docs/build_docs/`) é temporária: arquivada
depois que a documentação estiver fechada.

## Status possíveis

| Status | Significado |
|---|---|
| `pronto_para_execucao` | Decisão já fechada em `NOMENCLATURA.md`; só falta materializar no arquivo de destino (ADR, contrato, JSON) |
| `bloqueado_decisao` | Ainda precisa de sessão interativa com o usuário antes de poder ser executado |
| `concluido` | Item já materializado nos arquivos de destino e sem próxima ação pendente neste controle |

## Itens prontos para execução

### DOC-0001 — ADR: permitir `menu` em matriz
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `docs/adr/`, `docs/contratos/contrato_composicao_corpo.md`
**Origem:** `docs/NOMENCLATURA.md` seções 3, 6, 8
**Descrição:** menu deixa de ter apenas layout vertical legado — passa a
suportar fila horizontal e matriz; eixo `distribuicao_menu` (`fila` |
`matriz`), calculado automaticamente pela largura do terminal.
**Próxima ação:** — (concluído; ADR criada em `docs/adr/ADR-0001-menu-suporta-matriz.md`; seção 5.1 de `contrato_composicao_corpo.md` e R-6 atualizadas)

### DOC-0002 — ADR: `menu` usa sobra à direita
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0002-menu-sobra-direita.md`, `docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_composicao_corpo.md`
**Origem:** `docs/NOMENCLATURA.md` seção 8.1
**Descrição:** alinhamento horizontal do corpo tipo `menu` muda de
centralizado para alinhado à esquerda com sobra de espaço à direita. Não
afeta `dado` nem `Info` (Info aguarda decisão específica — DOC-B004).
**Próxima ação:** — (concluído)

### DOC-0003 — ADR: vãos elásticos do `menu`
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0003-vaos-elasticos-menu.md`, `docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_composicao_corpo.md`
**Origem:** `docs/NOMENCLATURA.md` seção 8.1
**Descrição:** vãos do `menu` (chip↔rótulo, entre itens/colunas) deixam de
ser valores fixos e passam a ter mínimo/máximo elástico (1–3 e 2–5),
parametrizados em `config/layout_menu.json`.
**Próxima ação:** — (concluído)

### DOC-0004 — ADR: campos `cor_inativo` e `cor_alerta`
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md`, `docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_estilo.md`
**Origem:** `docs/NOMENCLATURA.md` seção 1.5
**Descrição:** dois campos genéricos novos no schema de estilo — cor de
elemento existente-mas-inativo, e cor de alerta de limite atingido.
**Próxima ação:** — (concluído)

### DOC-0005 — Migrar presets de estilo para `config/estilo.json`
**Tipo:** documentacao
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `config/estilo.json` (criado), `docs/NOMENCLATURA.md` (seções 0, 1.3, 1.5), `docs/contratos/contrato_estilo.md` (seções 3.1, 3.2, 3.3, 5)
**Origem:** `docs/NOMENCLATURA.md` seção 0 (política schema × dados)
**Descrição:** presets de borda (3), chip (7), `selecionado` (4 presets),
`incluido` (4 presets) e defaults de `concluido` migrados para
`config/estilo.json`. Tabelas de valores concretos removidas de
`NOMENCLATURA.md` e `contrato_estilo.md`, substituídas por referência ao JSON.
**Próxima ação:** — (concluído)

### DOC-0006 — Criar contrato da barra_de_menus
**Tipo:** documentacao
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_barra_de_menus.md` (criado), `docs/INDICE.md` (atualizado)
**Origem:** `docs/NOMENCLATURA.md` seção 5, `config/barra_de_menus.json`
**Descrição:** contrato da `barra_de_menus` formaliza a distinção entre
`barra_de_menus` (região fixa da tela) e `menu` (objeto do corpo); define
existência estática vs estado dinâmico ativo/inativo; especifica comportamento
contextual de `[Esc]` e rótulo dinâmico de `[⏎]`; aponta `config/barra_de_menus.json`
como fonte de valores concretos; referencia `contrato_estilo.md` para `cor_inativo`
e `cor_alerta`; declara ordem canônica e semântica de cada chip.
**Próxima ação:** — (concluído)

### DOC-0007 — Formalizar cabecalho
**Tipo:** documentacao
**Status:** concluido
**Concluido_em:** 2026-07-05
**Arquivo(s) envolvido(s):** `config/cabecalho.json` (criado), `docs/contratos/contrato_cabecalho.md` (criado), `docs/NOMENCLATURA.md` (seção 0 e nova seção 7), `docs/INDICE.md` (atualizado), `docs/relatorios/RELATORIO_QA_DOC-0007_CABECALHO.md` (criado)
**Origem:** `docs/NOMENCLATURA.md` seção 0 (entrada Cabeçalho — pendente), seção 2 (estrutura da tela)
**Descrição:** `cabecalho` formalizado como domínio próprio: região fixa superior da tela, sempre presente,
com dois campos textuais (`titulo` e `descricao`); textos pertencem à classe/tela; `config/cabecalho.json`
guarda somente parâmetros de apresentação; contrato ativo criado com schema, semântica e regras de uso.
**Próxima ação:** — (concluído)

### DOC-0008 — Criar contrato do `lancador`
**Tipo:** documentacao
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_lancador.md` (criado), `config/lancador.json` (criado), `docs/INDICE.md` (atualizado)
**Origem:** `docs/NOMENCLATURA.md` seção 13
**Descrição:** criar o contrato próprio do `lancador` (antigo corpo tipo `menu`)
e o arquivo inicial `config/lancador.json`. Decisão terminológica fechada em
seção 13 do `NOMENCLATURA.md`; nome do arquivo de configuração definido como
`config/lancador.json` (decisão fechada em 2026-07-06). Estrutura mínima
definida: título + itens com `chip`, `texto` (máx. 15 caracteres, rejeitado em
verificação se exceder) e `tela_destino`. Migração dos artefatos existentes
que ainda usam `menu` como nome do tipo fica para DOC-0009.
**Próxima ação:** — (concluído)

### DOC-0009 — Migrar artefatos de `menu` para `lancador`
**Tipo:** documentacao
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/NOMENCLATURA.md` (seções 2–10), `docs/contratos/contrato_composicao_corpo.md`, `config/lancador.json`, `config/layout_menu.json`, `docs/INDICE.md`
**Origem:** `docs/NOMENCLATURA.md` seção 13; DOC-0008
**Descrição:** revisar e atualizar os artefatos existentes que ainda referenciam
o tipo de objeto do corpo como `menu`, substituindo pelo termo canônico
`lancador`. Executado após conclusão de DOC-0008. `config/lancador.json`
passa a ser o arquivo canônico, com parâmetros úteis migrados de
`config/layout_menu.json`; `config/layout_menu.json` permanece apenas como
artefato obsoleto/transicional de rastreabilidade.
**Próxima ação:** — (concluído)

### DOC-0010 — ADR: lancador não é corpo navegável por [✥]
**Tipo:** adr/documentação
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md` (criado), `docs/adr/INDICE_ADR.md` (atualizado), `docs/build_docs/to_do.md` (atualizado), `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md`, `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md`
**Origem:** decisão arquitetural — `lancador` não é corpo navegável por `[✥]`; `[✥]` restrito a corpo tipo `dado`
**Descrição:** Aplicar ADR-0005 nos contratos/configs ativos, restringindo `[✥]` a `dado`.
**QA inicial:** `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md` — APROVADO_COM_AJUSTES
**QA pós-ajuste:** `docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md` — APROVADO
**Resultado final:** APROVADO
**Próxima ação:** — (concluído; ADR-0006 iniciada em DOC-0011)

### DOC-0011 — ADR: renomeação `dado` → `console` e `Info` → `dashboard`
**Tipo:** adr/documentação
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0006-renomeacao-console-dashboard.md` (criado), `docs/adr/INDICE_ADR.md` (atualizado), `docs/build_docs/to_do.md` (atualizado), `docs/INDICE.md` (atualizado — lista nominal de ADRs)
**Origem:** decisão arquitetural de taxonomia — `dado` → `console`, `Info` → `dashboard`; `lancador` permanece
**Descrição:** registrar formalmente a decisão de renomeação terminológica dos tipos de corpo.
`console` preserva todas as regras do antigo `dado` (navegável por `[✥]`, estrutura `ec`/`tg`/`tx`,
eixos de composição). `dashboard` é saída passiva formatada, não navegável, não universalizado pela
estrutura de 8 campos legados. `lancador` permanece inalterado. Taxonomia fechada: `console`,
`lancador`, `dashboard`. Aplicação efetiva em contratos/configs fica para próxima tarefa.
**Próxima ação:** — (concluído; aplicação registrada em DOC-0012)

### DOC-0012 — Aplicar ADR-0006 em nomenclatura, contratos e configs
**Tipo:** documentação/configuração
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/contratos/contrato_composicao_corpo.md`, `docs/contratos/contrato_barra_de_menus.md`, `docs/contratos/contrato_lancador.md`, `docs/contratos/contrato_cabecalho.md`, `docs/contratos/contrato_estilo.md`, `config/barra_de_menus.json`, `config/layout_console.json` (criado), `config/layout_dado.json`, `docs/build_docs/to_do.md`
**Origem:** `docs/adr/ADR-0006-renomeacao-console-dashboard.md`
**Descrição:** aplicação da ADR-0006 em nomenclatura, contratos e configs ativos.
Taxonomia ativa do corpo passa a ser `console`, `lancador`, `dashboard`; `[✥]`,
`[-][+]` e `[V]` ficam restritos a `console`; `dashboard` substitui `Info` como
saída passiva não navegável; `config/layout_console.json` foi criado como
canônico; `config/layout_dado.json` foi marcado como obsoleto/transicional.
**QA:** `docs/relatorios/RELATORIO_QA_DOC-0011_ADR-0006_APLICACAO.md` — APROVADO
**Resultado final:** APROVADO
**Próxima ação:** — (concluído; próxima tarefa: iniciar ADR/tarefa separada para composição de tela de processamento)

### DOC-0013 — ADR: tela de processamento é composição de tipos existentes
**Tipo:** adr/documentação
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0007-tela-processamento-composicao.md` (criado), `docs/adr/INDICE_ADR.md` (atualizado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** ADR-0006 decisão 11 — tela de processamento remetida para decisão própria ou composição de tipos existentes
**Descrição:** registrar formalmente que tela de processamento não é quarto tipo de corpo; deve ser
modelada como composição de `console` + `dashboard` + chips específicos da `barra_de_menus`.
Taxonomia fechada do corpo permanece: `console`, `lancador`, `dashboard`. Aplicação efetiva
em nomenclatura e contratos ativos fica para próxima tarefa.
**Próxima ação:** — (concluído; aplicação registrada em DOC-0014)

### DOC-0014 — Aplicar ADR-0007 em nomenclatura e contratos
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/NOMENCLATURA.md`, `docs/contratos/contrato_composicao_corpo.md`, `docs/contratos/contrato_barra_de_menus.md`, `docs/build_docs/to_do.md`
**Origem:** `docs/adr/ADR-0007-tela-processamento-composicao.md`
**Descrição:** aplicação da ADR-0007 em `NOMENCLATURA.md`, `contrato_composicao_corpo.md`
e `contrato_barra_de_menus.md`. Tela de processamento foi registrada como composição
de tipos existentes, sem criação de quarto tipo de corpo; chips específicos foram
mantidos na `barra_de_menus`, declarados pela classe de tela.
**QA:** `docs/relatorios/RELATORIO_QA_DOC-0014_ADR-0007_APLICACAO.md` — APROVADO
**Resultado final:** APROVADO
**Próxima ação:** — (concluído; consolidação, revisão final e commit registrados em DOC-0015)

### DOC-0015 — Consolidar, revisar e commitar ciclo DOC-0010 a DOC-0014
**Tipo:** consolidação/documentação
**Status:** concluido
**Concluido_em:** 2026-07-06
**Arquivo(s) envolvido(s):** `docs/relatorios/RELATORIO_CONSOLIDACAO_DOCUMENTAL_DOC-0010_DOC-0014.md`, `docs/build_docs/to_do.md`
**Origem:** fechamento do ciclo documental DOC-0010 a DOC-0014
**Descrição:** consolidação final, revisão de diff, commit documental e check pós-commit do pacote que registrou ADR-0005, ADR-0006 e ADR-0007, aplicou a taxonomia `console`/`lancador`/`dashboard`, criou `config/layout_console.json` como canônico, marcou `config/layout_dado.json` como obsoleto/transicional e registrou tela de processamento como composição de tipos existentes.
**Commit:** `6b609ed docs: consolidar taxonomia de corpos e processamento`
**Resultado final:** APROVADO
**Próxima ação:** — (concluído; próximos trabalhos permanecem nos itens bloqueados DOC-B001 a DOC-B004, dependentes de decisão)

### DOC-0016 — ADR: modelo de configuração por tela
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`, `docs/adr/INDICE_ADR.md`, `docs/build_docs/to_do.md`
**Origem:** decisão arquitetural — substituir JSON por domínio/componente por JSON por tela; manter `config/estilo.json` como biblioteca global de estilo.
**Descrição:** registrar formalmente que cada tela terá JSON próprio com composição concreta, instâncias de `console`, `lancador`, `dashboard` e `barra_de_menus`, listas de itens, chips, destinos, ações, regras de existência/ativo-inativo, parâmetros visuais locais e casamento entre dados produzidos por scripts/leitores e campos exibidos. A ADR também registra que `dashboard` não terá `config/dashboard.json` universal, que o antigo `Info` é draft de instância da tela raiz do Orquestrador, e que o schema detalhado de `tela.json` será definido em tarefa/ADR posterior.
**Próxima ação:** — (concluído; aplicação registrada nos itens DOC-0017 a DOC-0022; schema de `tela.json` materializado em DOC-0023; pendências remanescentes em DOC-B006 a DOC-B011)

### DOC-0017 — Aplicar ADR-0008 em `NOMENCLATURA.md`
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/NOMENCLATURA.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** substituir a política de JSON por domínio/componente pelo modelo de JSON por tela; registrar `config/estilo.json` como biblioteca global de estilo; registrar `tela.json` como declaração concreta de cada tela; atualizar quadro/status de JSONs; atualizar definição de `dashboard` como tipo mínimo; registrar `lancador` como instância declarada por tela com mudança declarativa; registrar `barra_de_menus` como instância declarada por tela com lista de chips; registrar `console` como container genérico de itens heterogêneos; separar explicitamente configuração de estado de runtime.
**Próxima ação:** — (concluído; seções afetadas: 0, 2.2, 4, 5, 9, 13)

### DOC-0018 — Aplicar ADR-0008 nos contratos afetados
**Tipo:** documentação
**Status:** pronto_para_execucao
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_cabecalho.md`, `docs/contratos/contrato_estilo.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`; depois de DOC-0017.
**Descrição:** revisar contratos ativos para que dados concretos de instância passem a pertencer ao JSON da tela, preservando contratos como definição de semântica, invariantes e validação. `contrato_composicao_corpo.md` foi tratado em DOC-0025. `contrato_lancador.md` foi tratado em DOC-0020. `contrato_barra_de_menus.md` foi tratado em DOC-0021.
**Próxima ação:** executar em tarefa separada para os contratos remanescentes (`contrato_cabecalho.md` e `contrato_estilo.md`).

### DOC-0019 — Revisar `dashboard` conforme ADR-0008
**Tipo:** documentação
**Status:** pronto_para_execucao
**Arquivo(s) envolvido(s):** `docs/NOMENCLATURA.md`, `docs/contratos/contrato_composicao_corpo.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** registrar `dashboard` como tipo mínimo: não navegável por `[✥]`, não obrigatório, com moldura própria, posicionável dentro do corpo conforme configuração da tela e sem conteúdo universal fixo. Tratar a especificação do antigo `Info` como draft da instância de `dashboard` da tela raiz do Orquestrador.
**Próxima ação:** pode ser executado junto de DOC-0017/DOC-0018 ou em tarefa separada de revisão de `dashboard`.

### DOC-0020 — Revisar `lancador` conforme ADR-0008
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_lancador.md`, `docs/build_docs/to_do.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** revisar `lancador` como instância configurável por tela, incluindo título, itens, chip/letra, texto, `tela_destino` e regras de exibição/layout da instância, sem lista global de itens. Aplicado em `contrato_lancador.md` (versão 0.2): natureza do tipo vs instância declarada no `tela.json`; instância com `id` obrigatório; cada item com `id`, `chip`/tecla, `texto` e `tela_destino` obrigatórios; `config/lancador.json` marcado como artefato ativo transicional; alinhamento horizontal como regra da instância (não regra universal); ADR-0002 preservada como referência histórica e default possível; seção explícita sobre relação com `barra_de_menus`; critérios de validação expandidos; ADR-0008 adicionada à rastreabilidade.
**Próxima ação:** — (concluído; contratos remanescentes de DOC-0018 permanecem em aberto)

### DOC-0021 — Revisar `barra_de_menus` conforme ADR-0008
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_barra_de_menus.md`, `docs/build_docs/to_do.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** aplicar ADR-0008 em `contrato_barra_de_menus.md` (versão 0.2): natureza do tipo vs instância declarada no `tela.json`; `tela.json` como fonte da lista concreta de chips; `config/barra_de_menus.json` marcado como artefato ativo transicional; chips como entidades declarativas com campos conceituais (id, tipo, tecla, texto, acao, regra_existencia, regra_ativo, forma_exibicao); tipos conceituais de chip registrados; chips canônicos reposicionados como instâncias padronizadas; `[✥]` restrito a `console` navegável — não navega `lancador` nem `dashboard`; `[␣]` restrito a seleção múltipla; `[⏎]` atualizado como ação por item/binding; filtros declarativos formalizados; modo verboso `[V]` formalizado; ações whitelisted; seção de distribuição de instância adicionada; ADR-0004, ADR-0005 e ADR-0008 na rastreabilidade; critérios de validação expandidos. `docs/NOMENCLATURA.md` não foi alterado — os conceitos necessários já estão registrados na seção 5.
**Próxima ação:** — (concluído; pendência de contrato/classe `chip` permanece em DOC-B006)

### DOC-0022 — Atualizar `docs/INDICE.md` após aplicação da ADR-0008
**Tipo:** documentação
**Status:** pronto_para_execucao
**Arquivo(s) envolvido(s):** `docs/INDICE.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** atualizar a descrição da estrutura esperada e da função de `config/` para não priorizar o modelo antigo de JSON por domínio/componente depois que `NOMENCLATURA.md` e contratos forem revisados.
**Próxima ação:** executar junto da aplicação documental da ADR-0008.

### DOC-0023 — Criar contrato do schema de `tela.json`
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_tela_json.md` (criado), `docs/INDICE.md` (atualizado), `docs/NOMENCLATURA.md` (atualizado minimamente), `docs/build_docs/to_do.md` (atualizado)
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`; antigo DOC-B005
**Descrição:** criar contrato documental de `tela.json` como declaração configurável de uma tela, com estrutura obrigatória `schema`, `id`, `cabecalho`, `corpo` e `barra_de_menus`; corpo como lista de elementos `console`, `dashboard` e `lancador`; `console` como container genérico; filtros e bindings declarativos; ações whitelisted/registradas; validação obrigatória antes de renderizar; separação entre configuração e estado de runtime; e pendências derivadas para contratos futuros.
**Próxima ação:** — (concluído; pendências derivadas registradas em DOC-0017 a DOC-0022, DOC-0024 e DOC-B006 a DOC-B011)

### DOC-0024 — Revisar `console` como container genérico
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_console.md` (criado), `docs/INDICE.md` (atualizado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** `docs/contratos/contrato_tela_json.md`
**Descrição:** criar contrato documental do `console` como container genérico de itens heterogêneos, declarado no `tela.json`. Contrato cobre: natureza do tipo vs instância declarada no `tela.json`; instância com `id` obrigatório e campos mínimos; itens heterogêneos com `navegavel`, `selecionavel`, `acao_enter`, `politica_quebra` e `politica_exibicao`; política geral de composição com truncamento em modo normal e expansão em modo verboso; navegação por item (não por linha física); três políticas de seleção (`nenhuma`, `unica`, `multipla`); ação Enter por item; filtros declarativos aplicados antes da paginação; paginação com políticas de quebra; colunas ajustáveis; relação com `chip` e `barra_de_menus`; relação com `dashboard` e `lancador`; regras de uso; critérios de validação; pendências fora de escopo.
**Próxima ação:** — (concluído; pendências derivadas preservadas em DOC-B008, DOC-B009, DOC-B010, DOC-B011)

### DOC-0026 — Criar contrato da classe `chip`
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_chip.md` (criado), `docs/INDICE.md` (atualizado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`; antigo DOC-B006
**Descrição:** criar o contrato documental da classe `chip` como entidade declarativa de interface textual. Definidos: natureza do chip (não é ação por si só; aponta para ação/filtro/alternância/estado declarado); escopo principal na `barra_de_menus` com distinção obrigatória dos chips internos do `lancador`; campos mínimos (`id`, `tipo`, `tecla`, `texto`, `acao`/`referencia_regra`, `regra_existencia`, `regra_ativo`, `forma_exibicao`); tipos conceituais (`acao`, `filtro`, `alternancia`, `navegacao`, `informativo`, `especifico`); chips canônicos como instâncias padronizadas, não hardcoded; ações declarativas e whitelisted com proibição de comandos arbitrários; regra de existência como regra estrutural estática; regra de ativo/inativo como regra dinâmica; forma de exibição; texto e tecla; relação com estilo (aparência exclusivamente via `config/estilo.json`); relação com `barra_de_menus`; relação com `console`; relação com `lancador` e `dashboard`; critérios de validação; pendências fora de escopo. DOC-B006 fechado.
**Próxima ação:** — (concluído; pendências derivadas registradas em DOC-B009 — registry de ações e tipos; DOC-B006 encerrado)

### DOC-0027 — Ajustar critérios de validação do `contrato_console` pós-QA
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_console.md`, `docs/build_docs/to_do.md`
**Origem:** `docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md` — problema P1
**Descrição:** expandir a seção 16 de `contrato_console.md` para espelhar explicitamente todos os campos mínimos definidos na seção 3. Critérios adicionados: instância sem `tipo`, instância com `tipo` diferente de `console`, instância sem `titulo` ou identificador visual, e ausência de `politica_composicao`, `politica_navegacao`, `politica_selecao`, `politica_paginacao` e `politica_exibicao`. Critérios existentes sobre itens, ações, filtros, paginação, quebra, colunas, seleção e hardcoding preservados. Wording de `origem_dados` atualizado de "regra de itens" para "regra de geração de itens" para alinhar com seção 3.
**Próxima ação:** — (concluído; ajuste pós-QA responde ao relatório `RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md`)

### DOC-0025 — Aplicar ADR-0008 em `contrato_composicao_corpo.md`
**Tipo:** documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/contratos/contrato_composicao_corpo.md`, `docs/build_docs/to_do.md`
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`; DOC-0018 (parcial — apenas `contrato_composicao_corpo.md`)
**Descrição:** atualizar `contrato_composicao_corpo.md` para refletir que a composição concreta da tela é declarada no `tela.json`, não hardcoded em classe Python nem em JSON global por domínio/componente. Mudanças aplicadas: regra fundamental reescrita (declaração no `tela.json`, renderer executa sem deliberar); eixos de composição migrados para campos declarados por instância; `dashboard` deixa de ser eixo universal e passa a ser elemento opcional de `corpo.elementos[]`; `posicao_dashboard` passa a ser campo da instância; capacidades de `console` (paginação, colunas, filtros, seleção, modo verboso) passadas para declaração por instância; `lancador` refletido como instância declarada por tela; seção própria para `console` como container genérico adicionada; tiling atualizado para declaração em `tela.json`; seção de relação com `barra_de_menus` adicionada; R-13/R-14 adicionados; critérios de validação atualizados com regras ADR-0008; versão do contrato atualizada para `0.2`. Pendências derivadas preservadas (DOC-0020, DOC-0024, DOC-B004, DOC-B008).
**Próxima ação:** — (concluído; contratos remanescentes de DOC-0018 permanecem em aberto)

### DOC-0029 — ADR: caminho, nomenclatura e formato dos JSONs de tela
**Tipo:** adr
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` (criado), `docs/adr/INDICE_ADR.md` (atualizado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** DOC-B010; `docs/contratos/contrato_tela_json.md`; `docs/relatorios/RELATORIO_CONSOLIDACAO_FASE_0_ADR-0008_TELA_BASE.md`
**Descrição:** registrar formalmente o caminho canônico `config/telas/<id>.json`, a regra de nomenclatura por identificador estável em `snake_case` minúsculo sem acentos, a coincidência obrigatória entre `id` interno e nome base do arquivo, o identificador canônico `orquestrador` para a tela raiz, a ausência de índice central obrigatório nesta etapa, a permanência de `config/estilo.json` fora de `config/telas/`, e o status de artefatos transicionais existentes em `config/`. DOC-B010 encerrado.
**Próxima ação:** — (concluído; DOC-B011 liberado para criar `config/telas/orquestrador.json`)

### DOC-0028 — Consolidar Fase 0 após ADR-0008 na tela base
**Tipo:** consolidação/documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/relatorios/RELATORIO_CONSOLIDACAO_FASE_0_ADR-0008_TELA_BASE.md`, `docs/build_docs/to_do.md`
**Origem:** fechamento documental curto do ciclo ADR-0008 aplicado aos contratos centrais da tela base.
**Descrição:** relatório de consolidação criado para registrar o que já está fechado, o que foi aprovado com ressalva, quais ressalvas são apenas de worktree acumulado, quais ressalvas técnicas já foram resolvidas, quais pendências permanecem antes do draft do JSON da tela raiz do Orquestrador e se `contrato_cabecalho.md` ou `contrato_estilo.md` bloqueiam o próximo passo. Ciclo consolidado: ADR-0008, `contrato_tela_json.md`, aplicação em `NOMENCLATURA.md`, `contrato_composicao_corpo.md`, `contrato_lancador.md`, `contrato_barra_de_menus.md`, `contrato_chip.md`, `contrato_console.md` e ajuste pós-QA do `console`.
**Resultado da análise de bloqueio:** `LIBERADO_COM_PENDENCIAS_NAO_BLOQUEANTES`; `contrato_cabecalho.md` e `contrato_estilo.md` permanecem pendentes em DOC-0018, mas não bloqueiam o draft conceitual da tela raiz.
**Próxima ação:** tratar DOC-B010 antes do draft real, definindo formato, caminho, nomenclatura e organização dos JSONs de tela; em seguida abrir DOC para o draft do JSON da tela raiz do Orquestrador.

### DOC-0030 — Ajustar draft da tela raiz pós-QA DOC-B011
**Tipo:** documentação/configuração
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `config/telas/orquestrador.json`, `docs/build_docs/to_do.md`
**Origem:** `docs/relatorios/RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON.md`
**Descrição:** ajustes pós-QA ao draft `config/telas/orquestrador.json` com base nos problemas P1–P4 do relatório DOC-B011. Ajustes aplicados: (1) `referencias_de_acoes` expandida com `status: pendente_DOC-B009` e nota explícita de que nenhuma ação executa comando shell, nenhuma chama Python arbitrariamente e todas são referências declarativas provisórias; (2) `colunas_ajustavel` do `console_principal` convertida de string `"com"` para objeto com `ativo`, `minimo: 1`, `maximo: 3` e nota; (3) `filtro_grupo` expandido com `atua_antes_da_paginacao: true`, `filtro_ativo_runtime: "nao_guardado_aqui"`, `campo: "pendente_DOC-B008"` e nota mais explícita; (4) `lancador_principal` recebeu campo `pendencia_itens` explicitando que `itens: []` aguarda definição de telas do sistema e que o lancador não é navegável por setas (ADR-0005); (5) `chip_estilo` recebeu campo `pendencia` e nota na ação marcando o chip como placeholder não executável; (6) `metadados.pendencias` atualizado para refletir todos os ajustes com referências explícitas a DOC-B008, DOC-B009, DOC-0018 e DOC-B004.
**Pendências preservadas:** DOC-B008 (tipos internos de item de console e campo do filtro_grupo), DOC-B009 (registry de ações e tipos), DOC-0018 (contratos cabecalho/estilo), DOC-B004 (alinhamento do dashboard), DOC-B007 (arquivamento de artefatos), destinos do lancador, chip_estilo tela_destino.
**Próxima ação:** DOC-B008 (tipos internos de item de console) ou DOC-B009 (registry de ações/tipos), conforme decisão de prioridade do usuário.

### DOC-0031 — Consolidação final pré-commit da Fase 0 / ADR-0008 / tela raiz
**Tipo:** consolidação/documentação
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/relatorios/RELATORIO_CONSOLIDACAO_FINAL_FASE_0_ADR-0008_TELA_RAIZ.md` (criado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** fechamento do ciclo documental Fase 0 / ADR-0008 / tela raiz do Orquestrador.
**Descrição:** consolidação final pré-commit do pacote documental que cobre ADR-0008, ADR-0009, `contrato_tela_json.md`, aplicação em `NOMENCLATURA.md`, contratos `composicao_corpo`, `lancador`, `barra_de_menus`, `chip` e `console`, ajustes pós-QA, e draft real `config/telas/orquestrador.json`. Relatório criado com arrolamento completo de artefatos, itens fechados, pendências preservadas, resultado das QAs, checks finais e recomendação de commit.
**Status final do pacote:** `PRONTO_PARA_COMMIT`
**Checks executados:** `git diff --check` — aprovado; `python3 -m json.tool config/telas/orquestrador.json` — aprovado.
**Pendências preservadas:** DOC-B008, DOC-B009, DOC-0018 (cabecalho/estilo), DOC-B001 a DOC-B004, DOC-B007.
**Próxima ação:** commit documental único da Fase 0 / ADR-0008 / tela raiz.

### DOC-0032 — Auditoria e arquivamento histórico/transicional pós-ADR-0008/ADR-0009
**Tipo:** documentação/auditoria
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `docs/relatorios/RELATORIO_ARQUIVAMENTO_DOC-0032_HISTORICOS_TRANSICIONAIS.md`, `docs/build_docs/to_do.md`
**Origem:** ADR-0008, ADR-0009, consolidação final da Fase 0 e pendência de arquivamento histórico/transicional
**Descrição:** auditoria dos artefatos históricos/transicionais pós-ADR-0008/ADR-0009. Nenhum artefato foi classificado como inequivocamente histórico; nenhum arquivo foi movido, apagado ou arquivado. Artefatos transicionais foram preservados por rastreabilidade, função ativa, referência normativa ou dúvida razoável.
**Relatório:** `docs/relatorios/RELATORIO_ARQUIVAMENTO_DOC-0032_HISTORICOS_TRANSICIONAIS.md`
**Resultado final:** APROVADO_COM_RESSALVAS
**Ressalvas:** `config/layout_dado.json` e `config/layout_menu.json` permanecem obsoletos/transicionais; JSONs ativos/transicionais permanecem para reavaliação futura; DOC-B007 não deve ser removido silenciosamente sem decisão específica.
**Próxima ação:** — (concluído; seguir para QA pós-DOC-0032 e, se aprovado, commit documental final da Fase 0 com ressalvas registradas)

## Itens bloqueados (precisam de sessão de decisão antes de virar tarefa)

### DOC-B006 — Definir contrato/classe `chip`
**Status:** concluido
**Concluido_em:** 2026-07-07
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`; `docs/NOMENCLATURA.md` seção 5.2
**Descrição:** chips canônicos e específicos devem poder ser instâncias declaradas em JSON, mas ainda falta fechar contrato/classe `chip`: campos obrigatórios, tipos formais, ações, regras de existência, regras de ativo/inativo e forma de surgimento.
**Resolução:** contrato criado em `docs/contratos/contrato_chip.md` (DOC-0026). Campos mínimos, tipos conceituais, regras de existência/ativo-inativo, forma de exibição, relações e critérios de validação definidos. Registry completo de ações e de tipos de chip permanece pendente em DOC-B009.

### DOC-B007 — Arquivar artefatos históricos/transicionais no fechamento da Fase 0
**Status:** bloqueado_decisao
**Origem:** `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** pendência obrigatória de fechamento da Fase 0: arquivar artefatos históricos/transicionais de rastreabilidade para limpar a documentação ativa e evitar que buscas futuras priorizem contextos superados. Depende da decisão operacional de fechamento da etapa.
**Observação pós-DOC-0032:** a auditoria DOC-0032 foi concluída com `APROVADO_COM_RESSALVAS` e não executou arquivamento físico; esta pendência permanece como decisão operacional futura, salvo decisão humana em contrário.

### DOC-B008 — Definir contratos/classes de itens internos de `console`
**Status:** bloqueado_decisao
**Origem:** `docs/contratos/contrato_tela_json.md`
**Descrição:** o contrato de `tela.json` define `console` como container genérico e admite itens heterogêneos, mas ainda não fecha a taxonomia, campos obrigatórios, renderização normal/verbosa, quebra de página, navegabilidade, selecionabilidade e ação de Enter de cada tipo interno de item.

### DOC-B009 — Definir registry de tipos válidos
**Status:** bloqueado_decisao
**Origem:** `docs/contratos/contrato_tela_json.md`
**Descrição:** falta definir o registry de tipos reconhecidos pelo renderer: tipos de corpo, tipos internos de item de `console`, tipos de chip, tipos de filtro, tipos de ação registrada, origens de dados e regras de validação de cada família.

### DOC-B010 — Definir formato real e caminho dos JSONs de tela
**Status:** concluido
**Concluido_em:** 2026-07-07
**Origem:** `docs/contratos/contrato_tela_json.md`; `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
**Descrição:** o contrato de `tela.json` fecha o schema conceitual, mas ainda falta decidir caminho, nomenclatura, organização em diretórios, granularidade, exemplos reais mínimos e convenções de referência entre JSONs de tela.
**Resolução:** ADR-0009 criada em `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` (DOC-0029). Caminho canônico `config/telas/<id>.json`; identificador `orquestrador` para a tela raiz; nome base do arquivo coincide com `id` interno; `config/estilo.json` permanece fora de `config/telas/`; JSONs transicionais existentes marcados como artefatos a reavaliar/migrar; sem índice central obrigatório nesta etapa.

### DOC-B011 — Criar draft do JSON da tela raiz do Orquestrador
**Status:** concluido
**Concluido_em:** 2026-07-07
**Arquivo(s) envolvido(s):** `config/telas/orquestrador.json` (criado; diretório `config/telas/` criado), `docs/build_docs/to_do.md` (atualizado)
**Origem:** `docs/contratos/contrato_tela_json.md`; `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
**Descrição:** criado o primeiro draft real da tela raiz do Orquestrador em `config/telas/orquestrador.json`. Estrutura: `schema: tela.v1`, `id: orquestrador`, cabeçalho com `titulo` e `descricao`, corpo com 3 elementos (`console_principal`, `dashboard_info`, `lancador_principal`), barra_de_menus com 11 chips declarativos na ordem canônica, filtros, bindings e referencias_de_acoes declarados como pendentes. Dashboard com 8 campos do resumo (Adicionados, Fichados, Consolidados, Qualificados, Orfão, Missing, Secundários, Descartados) + Total + 8 marcadores (!, @, ?, *, &, %, ~, ^) conforme NOMENCLATURA.md seção 9. Lancador declarado sem itens — itens e destinos pendentes de documentação. Pendências preservadas em `metadados.pendencias`.
**Próxima ação:** — (concluído; pendências remanescentes: DOC-B008, DOC-B009, DOC-0018, DOC-B007, DOC-B001 a DOC-B004)

### DOC-B001 — Regras de ajuste do `tx` (corpo tipo `console`)
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 4.3, seção 11
**Descrição:** o que acontece quando o texto do item não cabe no espaço
disponível — truncar com reticências, quebrar em múltiplas linhas, ou
outra estratégia. Ainda não descrito pelo usuário.

### DOC-B002 — `popup_execucao` (estrutura nova)
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 11
**Descrição:** janela temporária de saída de execução de script — não é
corpo, dashboard, nem barra_de_menus. Usuário mencionou já ter ideias, mas
decidiu tratar depois de fechar o `lancador`. Precisa de: tamanho, posição,
critério de fechamento, se bloqueia a tela por trás, borda própria do
schema de estilo.

### DOC-B003 — Segunda pauta de "estilo de exibição de dados no corpo"
**Status:** bloqueado_decisao
**Origem:** mencionada em sessão, nunca descrita
**Descrição:** usuário citou a existência de um segundo ponto de estilo
de exibição de dados a definir, mas nunca chegou a descrever do que se
trata. Precisa perguntar antes de qualquer coisa.

### DOC-B004 — Reorganização corpo × dashboard e alinhamento do `dashboard`
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 9, seção 11
**Descrição:** duas coisas amarradas — (a) se `dashboard` acompanha a mudança
se o `dashboard` acompanha a regra de sobra à direita do `lancador` ou mantém centralização como o `console`;
(b) a reorganização maior de telas só-visualização usarem `dashboard` como
conteúdo principal e telas de processo usarem `corpo`. Explicitamente
remarcado para um chat/sessão dedicado a `dashboard` — escopo grande demais
pra resolver de raspão.
