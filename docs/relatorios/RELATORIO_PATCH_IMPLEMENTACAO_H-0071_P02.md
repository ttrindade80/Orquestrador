# RELATORIO_PATCH_IMPLEMENTACAO H-0071 P02

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch: P02
data: 2026-08-13
cadeia.raiz: docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md
cadeia.predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0071_P01.md
status: IMPLEMENTATION_PATCHED
```

## Escopo

Patch exclusivo de expectativas de teste autorizadas pelo H-0071 pós-P02.
Produção, configuração, handoff, ADR, contratos e nomenclatura não foram alterados.
`demo/teste_diagnostico.py` não foi alterado. Nenhum skip/xfail. Nenhum teste removido.

## Testes alterados e expectativa corrigida

### 1. `tela/testes_renderizador/barra_menus.py`

`test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta` (C)

- MARCAR/TODOS/SIMULAÇÃO/VERBOSO/AJUDA/REAL → caixa do preset Colchete (Marcar, Todos, Simulação, Verboso, Ajuda, Real).
- Preservados: rótulo dinâmico, ordem, atividade, cor de alerta, ausência de literais Espaço/Enter/Insert.

### 2. `demo/teste_demo_paginacao.py`

`test_demo_h0045_p12_pty_continuacao_e_vazio_ponto_de_entrada_real` (C)

- Substring bruta `_chip_paginas(...).encode() in vazio` substituída por conteúdo visível após strip ANSI + contenção `[\x1b[...mPgUp` na unidade.

`test_p23_ausencia_truncamento_reordenacao_chips_na_barra_normal` (C)

- `saida.index("[PgUp]")` → ordem via `[PgUp/PgDn]` no texto visível.
- Preservados: presença dos chips, ausência de truncamento, Esc primeiro.

### 3. `tela/teste_renderizador.py`

Fachada de coleta. Os cinco testes nominais foram redefinidos neste arquivo autorizado; os corpos originais em `selecao.py`/`integracao.py` ficaram fora do manifesto e não foram editados. A suíte canônica e `pytest tela/teste_renderizador.py` coletam as versões reconciliadas.

`test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao` (C)

- Envelope antigo `{cor}[⏎] Executar{reset}` → unidade `[cor+⏎+reset] Executar`.
- Preservados: espaço ativo, Enter inativo, capitalização.

`test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura` (C)

- Ordem `cor < Marcar < reset` → `cor < reset < Marcar` (reset no limite da unidade).
- Preservados: cor inativa, reset, sem vazamento para o rótulo.

`test_h0041_p04_texto_chip_barra_nao_usa_lower` (C)

- `endswith(reset)` → reset antes de "Executar".
- Preservada a capitalização declarada.

`test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos` (B)

- `[PgUp]`/`[PgDn]` separados → `[PgUp/PgDn]` visível; cor inativa contida em cada tecla da unidade.
- Preservados: visibilidade, estado inativo, conjunto vazio.

`test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica` (B)

- Mesma substituição da unidade; autoridade geométrica e cursores vazios preservados.

### 4. `demo/teste_demo.py`

Três testes H-0050 (C): busca bruta `[Ins]` / `[Ins] Simulação` → conteúdo visível + ANSI interno `[\x1b[...mIns\x1b[...m]`.
Preservados: seleção, Todos, rótulo corrente, Unicode ␣/⏎, ausência de Espaço/Enter/Insert.

### 5. `demo/teste_demo_console.py`

`teste_h0053_ponto_de_entrada_real_preserva_foco_cursor_navegacao_e_arvore` (C)

- Busca `[␣] Expandir` no quadro visível (ANSI interno no chip inativo da folha).
- Preservados: foco, cursor, navegação, árvore. MF-ITEM0010-003 intocado.

### 6. `demo/teste_demo_estilo_h0069.py`

`test_popup_usa_a_mesma_materializacao_local_da_demonstracao` (C)

- CONFIRMAR → Confirmar (preset Colchete). Mesma materialização popup/demonstração preservada.

### 7. `demo/teste_demo_estilo_h0070.py`

`test_presets_de_uma_tecla_e_delimitado_preservam_composicao` (B)

- `[PgUp][PgDn] Páginas` → `[PgUp/PgDn] Páginas`. Presets de uma tecla intactos.

## Arquivos não alterados

Produção, `config/estilo.json`, `demo/teste_diagnostico.py`, `tela/testes_renderizador/selecao.py`, `tela/testes_renderizador/integracao.py`, handoff, ADR, contratos, nomenclatura.

## Resultados focais

| Comando | Resultado |
|---|---|
| `tela/testes_renderizador/barra_menus.py` | 85 passed |
| `demo/teste_demo_paginacao.py` | 128 passed |
| `tela/teste_renderizador.py` | 371 passed |
| `demo/teste_demo.py` | 72 passed |
| `demo/teste_demo_console.py` | 19 passed |
| `demo/teste_demo_estilo_h0069.py` | 12 passed |
| `demo/teste_demo_estilo_h0070.py` | 5 passed |
| `tela/teste_estilo_h0071.py` + `demo/teste_demo_estilo_h0071.py` | 35 passed |
| `tela/teste_popup.py` | 68 passed |

## `demo/teste_diagnostico.py`

Não modificado. `pytest demo/teste_diagnostico.py`: 6 passed, 1 error.

O erro restante **não** é o resíduo B/C reconciliado. `teste_invariantes_anteriores` falha no teardown porque `python tela/teste_renderizador.py` (runner H-0010A, não a coleta pytest) retorna 1 por duas inspeções de fonte em `fundamentos.py`:

- renderer acessa `estilo.cor_texto` no caminho de renderizacao
- renderer acessa `estilo.cor_fundo` no caminho de renderizacao

Essas checagens não estão no manifesto P02. Corrigi-las exigiria produção ou arquivo fora da lista. Preservadas para o QA.

## Suíte canônica

`PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short`

**1370 passed, 1 error** — o mesmo erro independente de `demo/teste_diagnostico.py::teste_invariantes_anteriores`.

Todos os 14 testes nominais B/C passaram. CA-H0071-14 a CA-H0071-17 e CA-H0071-19 (não edição do diagnóstico) cumpridos. CA-H0071-18: código não-zero apenas pela falha independente acima.

## Falhas residuais

1. `demo/teste_diagnostico.py::teste_invariantes_anteriores` — inspeção `cor_texto`/`cor_fundo` no runner de `tela/teste_renderizador.py`. Fora do P02. Não classificada como legada.

## Bloqueios

Nenhum bloqueio de escopo do P02. Resíduos B/C autorizados reconciliados nos sete arquivos.

## Diff

`git diff` dos sete arquivos: apenas expectativas B/C (unidade `/`, contenção ANSI, caixa Colchete). Sem skip/xfail. Cobertura funcional preservada.
