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

## Itens bloqueados (precisam de sessão de decisão antes de virar tarefa)

### DOC-B001 — Regras de ajuste do `tx` (corpo tipo `dado`)
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 4.3, seção 11
**Descrição:** o que acontece quando o texto do item não cabe no espaço
disponível — truncar com reticências, quebrar em múltiplas linhas, ou
outra estratégia. Ainda não descrito pelo usuário.

### DOC-B002 — `popup_execucao` (estrutura nova)
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 11
**Descrição:** janela temporária de saída de execução de script — não é
corpo, Info, nem barra_de_menus. Usuário mencionou já ter ideias, mas
decidiu tratar depois de fechar o `lancador`. Precisa de: tamanho, posição,
critério de fechamento, se bloqueia a tela por trás, borda própria do
schema de estilo.

### DOC-B003 — Segunda pauta de "estilo de exibição de dados no corpo"
**Status:** bloqueado_decisao
**Origem:** mencionada em sessão, nunca descrita
**Descrição:** usuário citou a existência de um segundo ponto de estilo
de exibição de dados a definir, mas nunca chegou a descrever do que se
trata. Precisa perguntar antes de qualquer coisa.

### DOC-B004 — Reorganização corpo × Info e alinhamento do `Info`
**Status:** bloqueado_decisao
**Origem:** `docs/NOMENCLATURA.md` seção 9, seção 11
**Descrição:** duas coisas amarradas — (a) se `Info` acompanha a mudança
se o `Info` acompanha a regra de sobra à direita do `lancador` ou mantém centralização como o `dado`;
(b) a reorganização maior de telas só-visualização usarem `Info` como
conteúdo principal e telas de processo usarem `corpo`. Explicitamente
remarcado para um chat/sessão dedicado a `Info` — escopo grande demais
pra resolver de raspão.
