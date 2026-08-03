---
name: IMP-H0045-P16-politicas-distintas-modelo-fixo
description: "Delta factual do PATCH_IMPLEMENTACAO P16: tres politicas distintas, sem reconstrucao em resize, telas/casos fixos"
---

# IMP-H0045-P16 — Políticas distintas e modelo fixo

status_literal: IMPLEMENTATION_PATCHED
handoff: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
status_transportado: H1_HANDOFF_APPROVED

## Arquivos

criados:
- config/telas/demo/h0045_validacao_fluxo_continuo.json
- config/telas/demo/h0045_validacao_nova_pagina.json
- config/telas/demo/h0045_validacao_manter_junto.json
- config/telas/demo/h0045_validacao_continuacao.json
- config/telas/demo/h0045_validacao_vazio.json
- docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P16.md

alterados:
- tela/paginacao.py — ramos distintos para as tres politicas
- demo/demo.py — SIGWINCH nao reconstrói modelo; casos fixos sem regeneracao
- demo/casos_validacao_paginacao.py — VAZIO/CONTINUACAO fixos; helpers de hash; construtores legados so para testes
- tela/teste_paginacao.py — cobertura P16 das politicas e invariancia
- demo/teste_demo_paginacao.py — resize sem regeneracao; telas fixas; ajustes de regressao
- config/telas/demo/h0045_paginacao_console_unico.json
- config/telas/demo/h0045_dois_consoles_paginas_independentes.json
- config/telas/demo/h0045_fluxo_execucao_paginado.json
- config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json

removidos: nenhum

nao_alterados (escopo fechado): tela/renderizador.py, tela/teste_renderizador.py

## Correção das três políticas

- `permitir_quebra`: continua na proxima linha disponivel via `_fragmentar_entrada`.
- `evitar_quebra`: se a pagina corrente ja tem linhas usadas, abre pagina nova antes de colocar o item; fragmenta apenas se `linhas > capacidade`.
- `permitir_quebra_somente_se_maior_que_pagina`: aproveita residuo quando cabe inteiro; senao pagina seguinte inteira; se maior que a pagina, comeca no topo seguinte e continua.
- Default sem campo permanece `evitar_quebra` (assuncao explicita D-TEC-07).
- Fixtures H-0045 sem politica explicita passaram a declarar `permitir_quebra_somente_se_maior_que_pagina` para preservar o empacotamento historico calibrado.

## Retirada da reconstrução em resize

- O bloco SIGWINCH de `demo/demo.py` atualiza geometria e chama apenas `_reconciliar_paginacao_apos_resize`.
- Nao ha reaplicacao de caso nem substituicao de textos/IDs/itens/ordem/politicas apos resize.
- VAZIO/CONTINUACAO carregam JSON fixo; `_aplicar_caso_validacao_adaptativo` para esses IDs so resolve metadados geometricos, sem mutar itens.
- Construtores LARGURA/PERMITIR/EVITAR/CONDICIONAL permanecem como API de teste legado; entradas de produto substituidas pelas tres telas fixas.

## Telas e casos fixos

- Tres telas (§19.2): uma politica cada; intro nao navegavel; quatro itens `1.`–`4.`; texto legivel; conteudo invariavel.
- `H0045-VAL-VAZIO` e `H0045-VAL-CONTINUACAO`: JSON proprio, modelo unico por execucao, CONTINUACAO sem geracao a partir de `C`.

## Testes

focais:
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_paginacao.py demo/teste_demo_paginacao.py` → 64 passed
- coberturas P16: fluxo continuo; nova pagina; manter junto; item > pagina; multiplas geometrias; hash/snapshot; sem perda/duplicacao; resize; VAZIO; CONTINUACAO; pontos de entrada das tres telas

completa:
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q` → 851 passed
- `tela/teste_renderizador.py` (P12 CONTINUACAO/VAZIO/LARGURA) permanece verde sem alteracao do arquivo

verificacao semantica:
- mesmo setup (2+2 linhas, C=6): `permitir_quebra` e condicional → 1 pagina; `evitar_quebra` → 2 paginas

## Desvios

- API legada `construir_caso_*` / `_aplicar_caso_validacao_adaptativo` mantida para nao quebrar `tela/teste_renderizador.py` (fora de escopo de edicao); o caminho TUI da demo nao regenera em SIGWINCH.
- Expectativas de alguns testes de regressao (cursor em pagina so de continuacao no multilinha; pagina do item 1 em `nova_pagina`) alinhadas a semantica corrigida de `evitar_quebra`.

## Bloqueios

nenhum

## Fora deste patch

- `VM-H0045-R06-001` e `QA-H0045-P08-001` nao tratados
- validacao manual 15/17–17/17 nao executada
- sem stage/commit
