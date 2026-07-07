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

## Itens bloqueados (precisam de sessão de decisão antes de virar tarefa)

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
