# RELATORIO QA POS-PATCH IMPLEMENTACAO H-0071 P01

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
etapa: QA_POS_PATCH
patch: P01
status: I3_HANDOFF_PATCH_REQUIRED
cadeia:
  raiz: docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P01.md
```

## 1. Status

`I3_HANDOFF_PATCH_REQUIRED`. A implementação corrigida está conforme a
autoridade do H-0071 nos focos executados, mas a suíte canônica contém
expectativas visuais que precisam de adaptação fora do escopo atual. Não há
bloqueio documental.

## 2. Achados do P01

| Achado | Estado | Evidência focal |
|---|---|---|
| QA-H0071-001 | RESOLVIDO | `config/estilo.json` materializa `chip.preset_default = "Colchete"`; os focais H-0071 passam. |
| QA-H0071-002 | RESOLVIDO | `Ornamental` materializa `caractere_esquerdo = "╭"` e `caractere_direito = "╮"`; os focais cobrem a forma `╭PgUp/PgDn╮`. |

## 3. Resíduos

| Teste | Classe | Evidência | Camada |
|---|---|---|---|
| `tela/testes_renderizador/barra_menus.py::test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta` | C | Com `Colchete.caixa_alta=false`, a saída visível é `Marcar`, não `MARCAR`; a expectativa é de caixa alta de outro preset. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo_paginacao.py::test_demo_h0045_p12_pty_continuacao_e_vazio_ponto_de_entrada_real` | C | O helper espera a forma nova, mas a asserção procura o literal bruto; ANSI fica contido dentro do chip no PTY. | TESTE_DENTRO_DO_HANDOFF |
| `demo/teste_demo_paginacao.py::test_p23_ausencia_truncamento_reordenacao_chips_na_barra_normal` | C | O teste já valida `_chip_paginas` com `/`, mas ainda ordena por substring antiga `[PgUp]`. | TESTE_DENTRO_DO_HANDOFF |
| `tela/teste_renderizador.py::test_h0041_manual_001_espaco_ativo_em_item_selecionavel_com_selecao` | C | A asserção exige ANSI antes de `[⏎]` e após a descrição; a composição vigente restaura dentro da unidade. | TESTE_FORA_DO_HANDOFF |
| `tela/teste_renderizador.py::test_h0041_p04_chip_inativo_usa_cor_inativo_e_restaura` | C | A cor inativa e o reset existem, mas em posição contida conforme H-0071, não no envelope antigo. | TESTE_FORA_DO_HANDOFF |
| `tela/teste_renderizador.py::test_h0041_p04_texto_chip_barra_nao_usa_lower` | C | O texto preserva a caixa declarada; a falha é a expectativa de reset terminal fora da unidade. | TESTE_FORA_DO_HANDOFF |
| `tela/teste_renderizador.py::test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos` | B | Procura `[PgUp]`, forma individual substituída por `[PgUp/PgDn]`. | TESTE_FORA_DO_HANDOFF |
| `tela/teste_renderizador.py::test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica` | B | Procura `[PgUp]` e `[PgDn]` separados, contrariando a unidade multitecla vigente. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo.py::test_h0050_espaco_parcial_insert_nao_altera_selecao_nem_semantica_todos` | C | A saída visível preserva `Simulação`; o literal bruto `[Ins]` é interrompido pelo ANSI contido. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo.py::test_h0050_renderiza_chip_com_rotulo_corrente` | C | Mesmo caso: `[Ins] Simulação` existe visualmente após remoção de ANSI, não como substring bruta. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo.py::test_h0050_simbolos_unicode_e_ausencia_de_literais_espaco_enter` | C | `[Ins]` é procurado sem tolerar ANSI interno; os símbolos e rótulos visíveis permanecem corretos. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo_console.py::teste_h0053_ponto_de_entrada_real_preserva_foco_cursor_navegacao_e_arvore` | C | `Expandir` permanece no rótulo; a busca bruta não considera o ANSI do chip inativo. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo_estilo_h0069.py::test_popup_usa_a_mesma_materializacao_local_da_demonstracao` | C | O preset preservado `Colchete` produz `Confirmar`; `CONFIRMAR` é expectativa de caixa alta de outro preset. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_demo_estilo_h0070.py::test_presets_de_uma_tecla_e_delimitado_preservam_composicao` | B | Exige explicitamente `[PgUp][PgDn]`, forma renderizável substituída por `[PgUp/PgDn]`. | TESTE_FORA_DO_HANDOFF |
| `demo/teste_diagnostico.py::teste_invariantes_anteriores` | E | O erro ocorre no teardown porque o gate depende de `tela/teste_renderizador.py` retornar zero; não é falha autônoma. | DERIVADO |

## 4. Testes

- Focais H-0071: **35 passed**.
- Barra: **84 passed, 1 failed**.
- Popup: **68 passed**.
- Paginação: **126 passed, 2 failed**.
- Suíte canônica: **1357 passed, 13 failed, 1 error**.

## 5. Conclusão

Não há regressão H-0071 nos focais: a composição única com `/`, os
delimitadores externos, `Colchete` preservado, Ornamental `╭/╮`, contenção
ANSI, assimetria de Destaque Texto, largura visual e Barra real estão
conformes. Os resíduos B/C exigem atualização de expectativas de testes; os
resíduos canônicos fora do handoff tornam necessária a ampliação documental
antes de nova implementação. O erro de diagnóstico é derivado.

## 6. Bloqueios

Nenhum bloqueio documental. Não foi feita validação manual.
