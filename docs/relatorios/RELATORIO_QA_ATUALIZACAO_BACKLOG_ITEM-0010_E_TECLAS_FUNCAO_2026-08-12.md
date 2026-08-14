# Relatório QA da atualização do backlog — 2026-08-12

## Baseline Git observada

- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage: vazio.
- Antes da criação deste relatório, o worktree continha somente o delta não staged de `docs/backlog.md` e os dois relatórios documentais previstos.

## Arquivos e fontes auditados

- `docs/backlog.md`, lido integralmente.
- `docs/relatorios/RELATORIO_ATUALIZACAO_BACKLOG_ITEM-0010_E_TECLAS_FUNCAO_2026-08-12.md`, lido integralmente.
- `docs/relatorios/RELATORIO_PATCH_BACKLOG_ITEM-0010_P01.md`, lido integralmente.
- `git diff -- docs/backlog.md`.
- Versão baseline de `docs/backlog.md` em HEAD.
- `git status --short` e `git diff --check`.

## Resultado por item

### ITEM-0010

APROVADO. Há uma única ocorrência ativa, com identificador, título, tipo `implementacao` e prioridade `media` preservados; o status está `em_andamento`. A descrição limita a primeira versão a `borda`, `chip`, `indicadores.selecionado` e `indicadores.incluido`, deriva opções dos catálogos `presets`, mantém a seleção em `dois_niveis_por_foco` com escolha exclusiva por categoria, e registra candidato, ativação condicional de Enter/Aplicar, demonstração, confirmação por pop-up, persistência, vigência em runtime, cancelamento e descarte na saída. Registra os três handoffs, F4, as exclusões de escopo solicitadas e a criação/auditoria da ADR antes dos handoffs.

### ITEM-0012

APROVADO. Há uma única ocorrência, com título `Tiling por tela`, status `planejado` e prioridade `media` preservados. O item explicita a exclusão do ITEM-0010, o acionamento futuro por `|`, o caráter contextual e limitado à tela corrente, e reserva persistência, contrato e demais detalhes para especificação própria sem inventar JSON concreto.

### ITEM-0029

APROVADO. Há uma única ocorrência planejada para Ajuda global por F1 e ajuda declarativa dos chips. Registra F1, substituição de `?`, texto associado às declarações de chips, funções dos elementos efetivamente exibidos na `barra_de_menus`, teclas F globais e prevenção de lista manual desconectada, sem implementação antecipada.

### ITEM-0030

APROVADO. Há uma única ocorrência planejada para F11/tela cheia. Não inventa mecanismo técnico e exige levantamento focal da capacidade do terminal e do limite de responsabilidade do Orquestrador.

### ITEM-0031

NÃO CONFORME. Há uma única ocorrência, e o item permanece planejado, mas a descrição apenas afirma a futura consolidação do mapa. Faltam os registros obrigatórios `F1 = Ajuda`, `F4 = Estilo` e `F11 = Tela Cheia` subordinado ao trabalho próprio; a manutenção de F2, F3 e F5 sem função concreta; e a determinação de avaliação futura antes de reservar essas teclas. A ausência impede a aprovação do item.

## Preservação dos demais itens

O diff mostra alteração semântica somente no ITEM-0010 e no ITEM-0012, além da criação dos ITEM-0029, ITEM-0030 e ITEM-0031. Não houve renumeração, reordenação ampla ou alteração do ITEM-0027; ITEM-0028 não foi recriado; nenhum item adicional foi criado. Não foi criada ADR nem foi registrado número de ADR futura como se existente.

## Verificações mecânicas

- `git diff --check`: passou.
- Os dois relatórios de atualização e patch existem.
- O status observado não mostra arquivos de código, configuração ou ADR alterados.
- Nenhuma operação de commit ou push foi realizada pelo QA.
- O relatório presente é o único arquivo criado pelo QA e permanece não staged.

## Não conformidades

- ITEM-0031 não materializa o mapa global de teclas e as restrições de F2, F3 e F5 exigidas pelo critério de aprovação.

## Conclusão terminal

`BACKLOG_DOCUMENTATION_NEEDS_PATCH`
