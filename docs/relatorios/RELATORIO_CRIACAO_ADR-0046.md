# RELATORIO_CRIACAO_ADR-0046

## Baseline

- Projeto: Orquestrador.
- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage inicial: vazio.
- O worktree já continha somente deltas documentais aprovados e relatórios
  do ciclo atual; esses deltas foram preservados.
- ADR-0046: caminho livre e número não ocupado antes da criação.

## Fontes efetivamente lidas

- `docs/backlog.md` — bloco `ITEM-0010`.
- `config/estilo.json`.
- `docs/nomenclatura/01_NUCLEO_COMUM.md`.
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`.
- `docs/nomenclatura/10_ESTILO.md`.
- `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.
- `docs/nomenclatura/32_CONSOLE.md`.
- `docs/nomenclatura/35_POPUP.md`.
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`.
- `docs/contratos/contrato_estilo.md`.
- `docs/contratos/contrato_barra_de_menus.md`.
- `docs/contratos/contrato_chip.md`.
- `docs/contratos/contrato_popup.md`.
- `docs/contratos/contrato_console.md`.

## ADR criada

`docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`, vinculada ao
`ITEM-0010 — Tela de escolha do estilo global`.

## Principais decisões materializadas

- F4 abre a funcionalidade; F1/Ajuda e F11/tela cheia permanecem fora.
- Primeira versão limitada a `borda`, `chip`, `indicadores.selecionado` e
  `indicadores.incluido`; tiling, cores e `indicadores.concluido` ficaram fora.
- Categorias são estruturais; filhos vêm dinamicamente de `presets`, com
  escolha inicial por `preset_default`, sem hardcode de presets concretos.
- Navegação preserva `dois_niveis_por_foco`, com escolha exclusiva de um filho
  por pai e transferência somente por Espaço.
- Candidato, baseline persistida, materialização global e override de
  demonstração foram separados.
- Enter/Aplicar depende de diferença frente à última configuração persistida;
  demonstração integrada usa override local e inclui Cabeçalho, Console,
  Dashboard e Barra de Menus representativa.
- Pop-up genérico sobre a demonstração retorna apenas `CONFIRMADO` ou
  `ABORTADO`; a lógica de negócio permanece no chamador.
- Aplicação confirmada persiste antes de trocar o estilo global, sem reinício;
  falha de persistência é fail-closed e preserva o candidato.
- Saída sem aplicação descarta somente diferenças não confirmadas; não há
  restauração de padrão de fábrica.
- Foram registrados, sem criação, os handoffs H-0061, H-0062 e H-0063.

## Regras anteriores explicitamente substituídas

- Carregamento único com materialização imutável durante toda a sessão
  (`docs/nomenclatura/10_ESTILO.md` §4.8 e distinções relacionadas).
- Imutabilidade do schema durante tela aberta e exigência de reconstrução para
  mudar estilo (`docs/contratos/contrato_estilo.md` R-4).
- Limitação da materialização à carga inicial única por sessão
  (`docs/contratos/contrato_estilo.md` R-10).

A ADR preserva a autoridade global de `config/estilo.json`, a materialização
integral, a validação fechada, a proibição de hardcode e a existência de um
único estilo global vigente; candidato e override não são estilo global.

## Arquivos criados

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`
- `docs/relatorios/RELATORIO_CRIACAO_ADR-0046.md`

Nenhum handoff foi criado e nenhum arquivo existente foi alterado.

## Verificação

- `git diff --check`: PASS.
- Stage final: vazio.

## Bloqueios

Nenhum.
