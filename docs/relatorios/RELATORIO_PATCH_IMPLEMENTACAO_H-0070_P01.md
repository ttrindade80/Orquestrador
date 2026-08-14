# PATCH_IMPLEMENTACAO H-0070 P01

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0070.md
  achado_tratado: A1
natureza: expectativa_predecessora_superada_por_H0070
status: IMPLEMENTATION_PATCHED
patch: P01
validacao_manual_final_ITEM0010: OBRIGATORIA_APOS_QA_P01
```

## Expectativa obsoleta

A1: `demo/teste_demo_paginacao.py::test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1`

O teste já comprovava a unidade H-0070 ` PgUp/PgDn. PÁGINAS` na captura inicial.
No extremo PageUp da página 1 restava `assert "[PgUp]" in saida`, literal
predecessora de chips Colchete separados. Sob Ponto vigente, o par é um único
chip ` PgUp/PgDn.`. Não é regressão de produto.

## Alteração

Somente `demo/teste_demo_paginacao.py`. O assert residual foi substituído pela
unidade material H-0070, via `_sem_ansi`:

- ` PgUp/PgDn. PÁGINAS` presente;
- `visivel.count("PgUp/PgDn.") == 1`.

Não se exige `[PgUp]` nem `[PgDn]` separados. Produto, Barra, ADR, contratos,
nomenclatura, backlog e `config/estilo.json` não foram alterados.

## Semântica preservada

Permanecem cobertos: cadeia TTY PageUp/PageDown, páginas 1/2/3, extremos sem
wrap, chips ativo/inativo, cor inativa de PgUp, ação Páginas, PgUp e PgDn no
mesmo chip, `/` entre as teclas, um único ponto final Ponto.

## Testes

| Bateria | Resultado | Nota |
|---|---|---|
| A1 | 1 passed | achado resolvido |
| `demo/teste_demo_paginacao.py` | 108 passed / 20 failed | falhas externas |
| H-0070 (`tela` + `demo`) | 7 passed / 0 failed | sem regressão |
| Barra `tela/testes_renderizador/barra_menus.py` | 83 passed / 2 failed | falhas externas |
| H-0064, H-0068, H-0069 | 43 passed | sem regressão nova |
| suíte completa | **1262 passed, 73 failed, 17 errors** | baseline QA: 1261/74/17 |

A resolução de A1 é identificável: +1 passed, −1 failed.

## Falhas externas não tratadas (`EXTERNA_NAO_TRATADA`)

Família chip de uma tecla sob Ponto (`[Esc]`, `[?]`, `[✥]`, `[␣]`), não
autorizada neste patch:

- paginação: P02 (`[Esc]` no seletor da linha), P03 (`[✥]`), P09 (`Marcar` vs
  `MARCAR`), P21/P22/P23 (`[Esc] …`);
- Barra: `test_h0045_p02_barra_alinhada_na_sequencia_de_larguras` (`[Esc]`),
  `test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta`
  (`[␣] Marcar`).

Literais Colchete de paginação fora de A1 (`[PgUp]`/`[PgDn]` em P11/P12)
também não foram tocados.

## Bloqueios

Nenhum. Stage vazio. Sem commit/push. Validação manual não executada.
