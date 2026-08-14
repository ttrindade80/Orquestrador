# RELATORIO_PATCH_IMPLEMENTACAO H-0071 P03

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch_implementacao: P03
data: 2026-08-13
status: IMPLEMENTATION_PATCHED
cadeia.raiz: docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md
cadeia.predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0071_P02.md
```

## 1. Inspeções alteradas

Somente as duas inspeções estruturais de `teste_alternancia_borda` em
`tela/testes_renderizador/fundamentos.py`, mais dois helpers locais
estritamente necessários (`_fonte_definicao`, `_corpo_executavel`).

Nenhuma outra inspeção do arquivo foi tocada.

## 2. Forma antiga removida

As inspeções exigiam literalmente `estilo.cor_texto` e `estilo.cor_fundo`
dentro de `tela/renderizacao/barra_menus.py`. Essa forma ficou obsoleta
quando a Barra passou a delegar a composição a
`tela.renderizacao.estilo.compor_chip_multitecla` (H-0071). Classificação
QA: `TESTE_FONTE_DESATUALIZADO_PELO_H0071`.

## 3. Nova verificação estrutural

Cada inspeção demonstra a cadeia material, não só o nome de uma função:

1. `barra_menus.py` importa o compositor compartilhado
   `compor_chip_multitecla`.
2. `_texto_chip_barra` e `_conteudo_chip_multitecla` delegam a esse
   compositor; `_texto_chip_multitecla` alcança a Barra real via o wrapper.
3. `compor_chip_multitecla` chama `_conteudo_chip`.
4. INSPECAO-01: `_conteudo_chip` lê `cor_texto` via `_valor_estilo` e
   materializa com `_codigo_ansi_de_cor(cor_texto)`.
5. INSPECAO-02: `_conteudo_chip` lê `cor_fundo` e os campos assimétricos
   `cor_fundo_esquerdo`/`cor_fundo_direito`, com fallback para `cor_fundo`,
   e materializa via `_codigo_ansi_de_fundo`.

Helpers extraem a definição e o corpo executável (após assinatura e
docstring) para não tratar menção histórica em comentário como código.

## 4. Invariável contra hardcoding e compositor paralelo

Preservada no corpo executável dos três pontos da Barra
(`_texto_chip_barra`, `_conteudo_chip_multitecla`, `_texto_chip_multitecla`):

- ausência de `_codigo_ansi_de_cor(`, `_codigo_ansi_de_fundo(`, sequências
  `\x1b[`/`\033[`, `_ANSI_RESET_FG` e `_ANSI_RESET_BG`;
- ausência de definição local de `_conteudo_chip`,
  `compor_chip_multitecla`, `_codigo_ansi_de_cor` e `_codigo_ansi_de_fundo`
  em `barra_menus.py`.

A Barra não reintroduz acesso direto a `estilo.cor_texto`/`estilo.cor_fundo`.

## 5. Arquivos não alterados por este patch

Produção, configuração, handoff, ADR, contratos, nomenclatura e demais
testes permanecem intocados, incluindo:

- `tela/renderizacao/barra_menus.py`
- `tela/renderizacao/estilo.py`
- `tela/teste_renderizador.py`
- `demo/teste_diagnostico.py`
- `config/estilo.json`

O `git diff` de P03 restringe-se a `fundamentos.py` (as duas inspeções e
helpers locais). Estado acumulado anterior de outros arquivos não pertence
a este patch.

## 6. Runner direto

```text
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
Total de verificacoes: 1308
Passaram: 1308
Falharam: 0
EXIT_CODE=0
```

Pytest equivalente: `371 passed` / código 0.

## 7. demo/teste_diagnostico.py

Inalterado. `6 passed` / código 0. O erro derivado desapareceu com o
runner direto em zero.

## 8. Focais

- `tela/teste_estilo_h0071.py` + `demo/teste_demo_estilo_h0071.py`: 35 passed
- `tela/testes_renderizador/barra_menus.py`: 85 passed
- `demo/teste_demo_paginacao.py`: 128 passed
- `tela/teste_popup.py`: 68 passed

Todos com código 0. Sem skip/xfail.

## 9. Suíte canônica

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short
1370 passed in 36.51s
EXIT_CODE=0
```

## 10. Resíduos

Nenhum resíduo funcional ou estrutural observado neste patch.

## 11. Bloqueios

Nenhum.

## Critérios H-0071 P03

- CA-H0071-20: inspeção reconhece delegação compartilhada.
- CA-H0071-21: consumo de `cor_texto`/`cor_fundo` demonstrável no caminho
  da Barra real.
- CA-H0071-22: hardcoding e compositor paralelo continuam protegidos.
- CA-H0071-23: produção intocada; invariável não enfraquecida.
- CA-H0071-24: runner direto código 0.
- CA-H0071-25: `demo/teste_diagnostico.py` intocado; gate normalizado.
