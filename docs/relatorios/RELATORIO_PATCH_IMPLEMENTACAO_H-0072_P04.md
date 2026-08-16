# RELATÓRIO — PATCH_IMPLEMENTACAO H-0072 P04

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P04
natureza: COMPLETAR_EVIDENCIA_AUTOMATIZADA
achado_origem: VM-H0073-001
corrige:
  - ACH-P03-02
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P03.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: IMPLEMENTATION_PATCHED
```

## Escopo

Nenhuma alteração produtiva. P04 completa só a evidência automatizada de
resize integrado (ACH-P03-02). ACH-P03-01 permanece resolvido e não foi
reaberto. Código de produção, configuração, conteúdo, ADR, contratos,
nomenclatura e handoffs ficaram intactos.

## Lacuna do teste anterior

Em P03, `teste_resize_real_do_estado_recalcula_tabulacao_na_mesma_tela`
carregava H-0063, entra no nível filho por `processar_comando(..., " ", ...)`
e aplicava imediatamente `navegacao.redimensionar` para 48. O
`renderizar_estado` anterior à entrada produzia só `quadro_pai`. Faltava o
render explícito do estado filho em L1 antes do primeiro resize.

## Correção da evidência

O mesmo teste, em `demo/teste_demo_h0073_h0063_reconciliado.py`, agora fecha
uma única continuidade pelo fluxo real (sem helper privado de geometria):

1. carregar H-0063 (`_abrir`);
2. mesma tela/modelo/estado;
3. entrar no nível filho;
4. `renderizar_estado` em L1 **antes** de qualquer `redimensionar`;
5. capturar `tab_L1`;
6. `navegacao.redimensionar` para L2;
7. novo `renderizar_estado`;
8. capturar `tab_L2`;
9. `navegacao.redimensionar` para L3;
10. novo `renderizar_estado`;
11. capturar `tab_L3`.

Cadeia: estado filho → render L1 → resize → render L2 → resize → render L3.

## Geometria observada

Larguras totais preservadas: `48 → 44 → 43`. Tabulações físicas:
`tab_L1 = 10`, `tab_L2 = 6`, `tab_L3 = 5`. Cumpre
`tab_L1 > tab_L2 >= tab_L3`, máximo, intermediário (`5 < 6 < 10`) e mínimo.
A tela não é recriada nem o JSON recarregado entre larguras.

## Continuidade lógica

Entre L1, L2 e L3 permanecem: mesma tela, mesmo modelo, estado derivado do
mesmo fluxo, mesmo pai ativo, mesmo filho lógico, foco, cursor, seleção e
identidade lógica.

## Preservação H-0063

Designador ausente, preset, amostra, tabela de duas colunas, alinhamento
global e `H0063_ESPACAMENTO_COLUNAS_3_8: PRESERVADO` (gaps 3..8). H-0055 e
H-0070 não foram alterados.

## Testes

- Focal H-0063: **6 passed**.
- Suíte focal P03: **159 passed**.
- H-0070 isolado: **1 failed**, `index("→") == 2`, esperado `>= 4`;
  `FALHA_HISTORICA_NAO_CAUSAL`; teste intocado.
- Suíte canônica: **1456 passed, 1 failed**, somente H-0070.

Desvios: nenhum. Bloqueios: nenhum. Revalidação manual em TTY continua
necessária; não executada. Próxima ação: QA_POS_PATCH.

## Arquivos desta etapa

- `demo/teste_demo_h0073_h0063_reconciliado.py`
- este relatório
\n