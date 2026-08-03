---
name: REL-PATCH-H-0045-P11-diagnostico-politicas-quebra-e-conjunto-vazio
description: "Corrige a validabilidade material das políticas de quebra e do conjunto vazio, e um defeito real de existência dos chips [<]/[>]"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-08-01
rastreabilidade:
  etapa: DIAGNOSTICO_E_PATCH_IMPLEMENTACAO
  objeto: h0045_paginacao_politicas_quebra / h0045_paginacao_conjunto_vazio
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P10.md
  achados_tratados: [VM-H0045-R07-003]
---

# REL-PATCH-H-0045-P11 — Patch de implementação

## Diagnóstico e causa raiz

**Teste 15 (políticas de quebra).** `h0045_paginacao_politicas_quebra.json`
tinha só 3 itens, cada um uma string curta (~60 chars) que cabia inteira em
uma linha de 80 colunas mesmo em modo verboso. Nenhum item jamais fragmentava
nem excedia a página: as três políticas produziam o MESMO resultado visual
(tudo na página 1), tornando-as indistinguíveis. Não havia defeito de
runtime/loader/renderer aqui: `tela/paginacao.py::plano_de_paginacao` já
implementa as três políticas corretamente, inclusive a fragmentação forçada
quando um item excede a capacidade de uma página vazia. `evitar_quebra` e
`permitir_quebra_somente_se_maior_que_pagina` são, de fato, comportamentalmente
idênticas na implementação — isso reflete o texto quase idêntico do contrato
(`contrato_console.md` §12), reconhecido e não resolvido pelo próprio handoff
(§6.4); não é regressão deste patch.

**Teste 17 (página sem navegáveis).** Mesma causa: nenhum item era grande o
bastante para produzir uma página inteira de continuação pura.

**Teste 16 (conjunto vazio).** A fixture não tinha `itens: []`: tinha 4 itens
reais (`info_01..04`, `navegavel: false`) — os "quatro itens" observados na
validação manual eram exatamente o conteúdo declarado, não um fallback
sintético (loader, modelo e `mapa_fisico_de_itens` não têm nenhum mecanismo de
substituição de lista vazia; confirmado por leitura de código e execução
direta). Corrigindo isso, porém, um SEGUNDO defeito real emergiu: um console
com `politica_paginacao: "com"` e zero itens navegáveis nunca é focalizável
(`navegacao.console_e_focalizavel` exige ≥1 item navegável — ADR-0031 D2) e
por isso nunca entra em `navegacao.lista_foco`. Em `tela/renderizador.py`, a
existência dos chips `[<]`/`[>]` era derivada de `any(_console_tem_paginacao(c)
for c in lista_foco)` — logo, para este cenário, os chips eram **omitidos por
completo**, não "inativos". Isso viola `contrato_console.md` §12 ("existem
quando a instância declara paginação: com") e CA-H0045-04. Causa raiz:
combinação de fixture insuficiente **e** defeito real de código no critério de
existência dos chips (não apenas nas fixtures).

## Delta aplicado

- `config/telas/demo/h0045_paginacao_conjunto_vazio.json`: `itens: []` real.
- `config/telas/demo/h0045_paginacao_politicas_quebra.json`: 4 itens —
  `permitir_quebra_01` (31 linhas), `evitar_quebra_02` (6 linhas),
  `condicional_cabe_03` (12 linhas, cabe em página vazia),
  `condicional_maior_04` (20 linhas, maior que a capacidade). Textos com
  tokens estáveis (`PERM_L01..31`, `EVIT_L01..06`, `CABE_L01..12`,
  `MAIOR_L01..20`) calibrados para produzir, em 80×24 (capacidade real 16
  linhas/página, calculada via `geometria_console`, nunca chutada): 6
  páginas — pg1 (item1 início, 16 linhas), pg2 (item1 continuação, 15
  linhas, **somente continuação, zero navegável, resíduo de 1 linha
  insuficiente para o item2**), pg3 (item2 inteiro), pg4 (item3 inteiro),
  pg5–pg6 (item4 fragmentado, 16+4). Prova simultânea de `evitar_quebra`
  (item2 não vaza para o resíduo de 1 linha da pg2) e do teste 17 (pg2 é
  página de continuação pura).
- `tela/renderizador.py`: nova `_algum_console_paginado_no_corpo` (travessia
  recursiva do corpo, sem filtro de focalizabilidade); `_preparar_contexto_
  navegacao` ganhou parâmetro `modelo` e passou a alimentar
  `_navegacao_atual["existe_console_paginado"]`; `_linhas_barra` passou a
  usar essa chave (em vez de `lista_foco`) para decidir a existência de
  `[<]`/`[>]`. Os dois pontos de chamada (`renderizar_tela`,
  `_geometria_por_console`) repassam `modelo`.
- `tela/teste_paginacao.py`: 2 testes ajustados às novas fixtures (id
  `permitir_quebra_01` em vez de `permitir`; teste do conjunto vazio
  reescrito para `itens: []` real, sem a asserção obsoleta de conteúdo
  não-vazio).
- `tela/teste_renderizador.py` (+1) e `demo/teste_demo_paginacao.py` (+3):
  cobertura completa dos 15 requisitos de políticas (incl. dimensão menor
  80×15 → 11 páginas, provando derivação da capacidade, não de números
  fixos) e dos 10 requisitos do conjunto vazio (chips inativos via
  `estado_ativo_chips`/código ANSI de `cor_inativo`, comandos/setas sem
  efeito, resize preserva estado, nenhum conteúdo default).

## Verificações

```yaml
focais: 402 passed
expandidos: 578 passed
suite_completa: 810 passed
demonstracao_pty: >
  python demo/demo.py h0045_paginacao_politicas_quebra e
  h0045_paginacao_conjunto_vazio, PTY real, 80x24: 6 paginas percorridas
  (".", ","), pagina 2 confirmada como continuacao pura com setas
  SEM_MOVIMENTO; conjunto vazio com [<]/[>] visiveis+inativos, comandos e
  setas SEM_MOVIMENTO, resize 100x30 preserva pagina 1/1 -- sem erros.
manual_usuario: pendente (não executada)
etapas_preservadas: 6/17..14/17
retomada: R08_CONSOLIDADA em 15/17
```

Nenhum documento normativo foi alterado. Stage e commit não foram
executados. Achados não bloqueantes preservados sem tratamento neste
patch: `VM-H0045-R06-001` (chip `[Esc]` limpa seleção antes de sair) e
`QA-H0045-P08-001` (pendente de saneamento documental).
