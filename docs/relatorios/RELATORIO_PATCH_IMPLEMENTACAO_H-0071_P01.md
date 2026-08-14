# RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P01

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
etapa: PATCH_IMPLEMENTACAO
patch: P01
data: 2026-08-13
status: IMPLEMENTATION_PATCHED
cadeia:
  raiz: docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0071.md
arquivos_alterados:
  - config/estilo.json
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P01.md
```

## 1. Escopo executado

Patch de implementação restrito aos dois achados confirmados transportados
pelo prompt. Nenhum código, teste, handoff, ADR, contrato ou nomenclatura
foi alterado. QA-H0071-003 permaneceu fora de correção.

## 2. Achados tratados

### QA-H0071-001 — tratado

`chip.preset_default` foi restaurado de `"Curva"` para `"Colchete"`.

Nenhum outro preset ou propriedade foi alterado para compensar. Em
particular, `caixa_alta` do preset `Colchete` permanece `false`, valor
próprio já existente.

### QA-H0071-002 — tratado

No preset `chip.presets["Ornamental"]`:

- `caractere_esquerdo`: `"❲"` → `"╭"`
- `caractere_direito`: `"❳"` → `"╮"`

A forma exigida por CA-H0071-05 passa a ser materializável como
`╭PgUp/PgDn╮`.

## 3. Delta concreto em `config/estilo.json`

Delta material **deste patch** (relativo ao estado pré-P01 no worktree):

1. `chip.preset_default`: `"Curva"` → `"Colchete"`
2. `chip.presets["Ornamental"].caractere_esquerdo`: `"❲"` → `"╭"`
3. `chip.presets["Ornamental"].caractere_direito`: `"❳"` → `"╮"`

Preservado, sem alteração neste patch:

- `chip.presets["Destaque Texto"].cor_fundo_esquerdo` = `"padrão"`
- `chip.presets["Destaque Texto"].cor_fundo_direito` = `"azul"`
- `chip.presets["Colchete"].caixa_alta` = `false`
- demais presets, categorias e campos

`git diff -- config/estilo.json` contra HEAD ainda mostra trabalho
acumulado do ITEM-0010 (campos de Destaque Texto e reformatação de
`selecionado`/`incluido`). Esse delta acumulado **não** foi produzido
neste P01. A restauração de `preset_default` para `"Colchete"` faz esse
campo coincidir novamente com HEAD, por isso não aparece no diff contra
HEAD. O trecho Ornamental (`❲`/`❳` → `╭`/`╮`) é a única alteração
deste patch visível nesse diff.

## 4. Testes e contagens

Comando: `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q …`

| Suíte | Resultado |
|---|---|
| `tela/teste_estilo_h0071.py` + `demo/teste_demo_estilo_h0071.py` | 35 passed |
| `tela/testes_renderizador/barra_menus.py` | 84 passed, 1 failed |
| `tela/teste_popup.py` | 68 passed |
| `demo/teste_demo_paginacao.py` | 126 passed, 2 failed |
| suíte canônica (`pytest -q --tb=short`) | 1357 passed, 13 failed, 1 error |

Nenhum teste foi alterado.

## 5. Resíduos ainda observados

Registrados factual e separadamente. Sem classificação como legado,
regressão ou independência.

### Suíte da Barra

- `tela/testes_renderizador/barra_menus.py::test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta`
  — `AssertionError`: esperava `"MARCAR"` em `' [Esc] Sair  [␣] Marcar  [⏎] Todos  [Ins] Simulação  [V] Verboso  [?] Ajuda'`.

### Paginação

- `demo/teste_demo_paginacao.py::test_demo_h0045_p12_pty_continuacao_e_vazio_ponto_de_entrada_real`
  — `AssertionError`: `b'[PgUp/PgDn] Páginas'` não encontrado no buffer PTY.
- `demo/teste_demo_paginacao.py::test_p23_ausencia_truncamento_reordenacao_chips_na_barra_normal`
  — `ValueError: substring not found` em `saida.index("[PgUp]")`.

### Suíte canônica (além das duas de paginação acima)

- `tela/teste_renderizador.py::test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao` — `AssertionError` em trecho com `"[⏎] Executar"`.
- `tela/teste_renderizador.py::test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura` — `AssertionError`: `idx_cor < idx_marcar < idx_reset`.
- `tela/teste_renderizador.py::test_h0041_p04_texto_chip_barra_nao_usa_lower` — `AssertionError`: `texto.endswith(...)`.
- `tela/teste_renderizador.py::test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos` — `assert "[PgUp]" in saida`.
- `tela/teste_renderizador.py::test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica` — `assert "[PgUp]" in saida and "[PgDn]" in saida`.
- `demo/teste_demo.py::test_h0050_espaco_parcial_insert_nao_altera_selecao_nem_semantica_todos` — `assert '[Ins] Simulação' in saida`.
- `demo/teste_demo.py::test_h0050_renderiza_chip_com_rotulo_corrente` — `assert '[Ins] Simulação' in saida`.
- `demo/teste_demo.py::test_h0050_simbolos_unicode_e_ausencia_de_literais_espaco_enter` — `assert '[Ins]' in saida`.
- `demo/teste_demo_console.py::teste_h0053_ponto_de_entrada_real_preserva_foco_cursor_navegacao_e_arvore` — `assert '[␣] Expandir' in quadros[7]`.
- `demo/teste_demo_estilo_h0069.py::test_popup_usa_a_mesma_materializacao_local_da_demonstracao` — `assert "CONFIRMAR" in quadro`.
- `demo/teste_demo_estilo_h0070.py::test_presets_de_uma_tecla_e_delimitado_preservam_composicao` — `assert '[PgUp/PgDn] Páginas' == '[PgUp][PgDn] Páginas'`.
- `demo/teste_diagnostico.py::teste_invariantes_anteriores` — ERROR no teardown: gate H-0038, `'invariantes H-0010A preservados (tela/teste_renderizador.py retorna 0)'`.

Nenhum desses resíduos foi corrigido neste patch.

## 6. Bloqueios

Nenhum. Os dois achados autorizados foram materializados. QA-H0071-003
permanece sem correção, conforme o manifesto.

## 7. Critérios de conclusão

1. `preset_default` voltou a `"Colchete"`.
2. Ornamental usa `"╭"` e `"╮"`.
3. Destaque Texto mantém `"padrão"` e `"azul"`.
4. Nenhum código ou teste foi alterado.
5. Os testes obrigatórios foram executados.
6. Este relatório foi materializado.
7. Nenhum resíduo NAO_CONFIRMADO foi corrigido por inferência.
