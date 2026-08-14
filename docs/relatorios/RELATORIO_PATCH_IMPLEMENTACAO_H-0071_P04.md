# RELATORIO_PATCH_IMPLEMENTACAO H-0071 P04

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch_implementacao: P04
data: 2026-08-14
status: IMPLEMENTATION_PATCHED
```

## Arquivos alterados

Produção:

- `tela/renderizacao/estilo.py` — compositor compartilhado;
- `tela/renderizacao/barra_menus.py` — caminho de composição da Barra real;
- `tela/renderizacao/conteudo_externo.py` — prefixo físico `ec → tg → tx`.

Testes:

- `tela/teste_estilo_h0071.py`;
- `demo/teste_demo_estilo_h0071.py`;
- `tela/testes_renderizador/fundamentos.py`.

ADR, contratos, nomenclatura, handoff, loader e configuração concreta não
foram alterados neste patch.

## Correções realizadas

1. Destaque Texto: somente o foreground de `PgUp/PgDn` recebe a cor de
   destaque; fundo normal em toda a unidade; um espaço normal à esquerda e
   à direita. Removido o consumo residual de `cor_fundo_esquerdo` e
   `cor_fundo_direito`.
2. Ação multitecla como unidade única com `/` e delimitadores só nas
   extremidades. Barra real: `[PgUp/PgDn] Páginas`. A forma
   `[PgUp][PgDn] Páginas` não aparece na saída. Amostra de Estilo e Barra
   real usam o mesmo compositor.
3. Estado funcional preservado: Aplicar inativo e Páginas inativo usam
   `cor_inativo`; PgUp/PgDn com estados diferentes permanecem distintos
   dentro da unidade; foreground/fundo do preset não substituem
   `cor_inativo`.
4. Filhos sem designador: `recuo + cursor + toggle + texto`. Com ou sem
   cursor, toggle e texto ficam na mesma coluna.

Preservados: Ponto; Destaque Fundo; Ornamental `╭`/`╮`; largura visual sem
ANSI; contenção de estilo; navegação; paginação.

## Testes executados

| Suíte | Resultado |
|---|---|
| Focais H-0071 (`teste_estilo_h0071` + `teste_demo_estilo_h0071`) | 45 passed |
| Runner direto `tela/teste_renderizador.py` | 1308/1308, código 0 |
| Barra, popup, paginação, fachada do renderizador | 652 passed |
| `demo/teste_demo.py`, `teste_demo_console.py`, `teste_diagnostico.py` e regressões H-0069/H-0070 | 349 passed no lote focal+regressão |
| Suíte canônica `pytest -q` | 1379 passed, 1 failed, 36.50s |

Sem skip/xfail. Nenhum commit.

## Falha restante

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
exige `index("→") >= 4`.

Evidência observável: esse bound só vale para o prefixo antigo
`tg + recuo + ec` (`●   →`, cursor no índice 4). A saída P04 é
`'  → ● Borda Curva  ╭─╮││╰─╯'` (cursor 2, toggle 4), que é a ordem
`ec → tg → tx` exigida pelo H-0071. Os demais asserts do mesmo teste
(sem ordinais, coluna de texto estável, indicadores) continuam
verdadeiros. O arquivo não está na autorização nominal P04 e não foi
alterado. Não é defeito da produção deste patch.

## Bloqueios

Nenhum bloqueio de implementação. Validação manual em TTY real permanece
fora desta etapa.
