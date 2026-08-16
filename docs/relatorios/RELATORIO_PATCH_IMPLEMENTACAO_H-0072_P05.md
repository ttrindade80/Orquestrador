# RELATÓRIO — PATCH_IMPLEMENTACAO H-0072 P05

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P05
achados_origem:
  - VM-H0073-001
  - VM-H0073-002
predecessor_imediato:
  docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0073_POS_H0072_P04.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: IMPLEMENTATION_PATCHED
```

## Execução

A primeira tentativa de P05 parou sem alterar código:
`AUTORIZACAO_DE_ESCOPO_NECESSARIA` para
`tela/renderizacao/matriz_participantes.py` (VM-H0073-002). Este prompt
concedeu autorização focal para esse arquivo e para o campo
`barra_de_menus.distribuicao.linhas.maximo` de H-0055 (2→3). As causas A e B
permanecem independentes; não houve rediagnóstico.

## VM-H0073-001

A tabulação genérica não foi alterada. Texto e tabela continuam em
`_escolher_maior_que_cabe` / `_cabe_tabulacao`. SIGWINCH e `content_w`
já chegavam corretamente.

H-0055 não declarava `distribuicao`; o teto implícito era
`linhas.maximo: 2` (`tela/renderizacao/barra_menus.py`). H-0063 declara
`maximo: 3`. P05 declara em H-0055 somente o bloco canônico de
distribuição, com `linhas.maximo: 3`. Chips, tabulação 5..10, `A)`,
apresentação texto, navegação e seleção não mudaram. O conteúdo externo
permanece byte-a-byte.

Antes: `renderizar_estado` falhava com `erro_layout` em W=48.
Depois: W=48 e W=40 renderizam. Em 80→48→40 a tabulação observada no
fluxo real permanece 10, porque o texto curto ainda cabe. A transição
helper 10/9/5 (content_w 28/27/23, W≈37..32) continua abaixo do novo
piso da barra (W=39). Sem algoritmo novo e sem elevar `maximo` além de 3,
o fluxo real não demonstra intermediário nem 5.

**VM-H0073-001: PENDENTE.**

## VM-H0073-002

Em W=50, `_linhas_console` emitia `\x1b[44m A \x1b[49m` íntegro (36
colunas / 46 bytes). `_aplicar_indicador_linhas` prefixava 2 colunas e
cortava com `[:content_w]` (47 bytes), deixando `\x1b[49` e background 44
ativo. Padding e linhas seguintes herdavam o fundo.

Correção: os dois cortes passaram a `_cortar_sem_ansi`. Em
`texto_ansi.py`, o corte nunca emite CSI partido; se trunca com SGR
ativo, fecha com `_ANSI_RESET_FG` / `_ANSI_RESET_BG` sem mudar a largura
visual. Estilização que cabe integralmente permanece.

`_quebrar_texto` ainda partia CSI por `len()` em compactação extrema
(content_w=25). P05 desvia texto com SGR para `_quebrar_sem_ansi`: quebra
visual, não parte CSI, fecha SGR em cada linha física e reabre só se a
região estilizada continua. Indentação fora do chip fica neutra.

Antes (W=50): reset partido, `last_sgr=44`. Depois: reset completo,
padding após `\x1b[49m`, linha seguinte sem `\x1b[44m`, cabeçalho e base
neutros. O chip continua com fundo 44. Tabulação 10→6→5 em 48/44/43 e
gaps 3..8 preservados.

**VM-H0073-002: CORRIGIDO** (sujeito a revalidação TTY).

## Arquivos efetivamente escritos

- `config/telas/demo/h0055_dois_niveis_por_foco.json`
- `tela/renderizacao/matriz_participantes.py`
- `tela/renderizacao/texto_ansi.py`
- `tela/renderizacao/conteudo_externo.py`
- `demo/teste_demo_h0073_h0055_reconciliado.py`
- `demo/teste_demo_h0073_h0063_reconciliado.py`
- `tela/teste_estilo_h0073_h0063.py`
- este relatório

H-0063 JSON, conteúdo H-0055, preset, 3..8, H-0070, ADR, contratos,
handoffs e nomenclatura não foram editados por P05. Sem stage.

## Testes

Focais: **168 passed**. H-0070 isolado: **1 failed**, `index("→") == 2`,
esperado `>= 4`; `FALHA_HISTORICA_NAO_CAUSAL`. Suíte canônica:
**1460 passed, 1 failed**, somente H-0070.

Evidência ANSI: fatiamento `[:n]` parte `\x1b[49m`; `_cortar_sem_ansi`
não. Wrap cobre linha única, compactação e duas linhas com reset. Quadro
H-0063 via `renderizar_estado` em 120/50/48/44/43/40: fundo no chip, sem
CSI truncado, sem herança na linha seguinte nem no quadro. Gaps 3..8.

H-0055: continuidade 80→48→40 sem `erro_layout`, `A)` e identidade
preservados; tabulação 10 em todas. Helper 10/9/5 permanece.

Desvios: nenhum além de 001 pendente. Bloqueios: nenhum novo de escopo.
Revalidação manual TTY: necessária.
\n