# Relatório QA pós-patch H-0058 P01

## Achado

`MV-H0058-01` permanece aberto somente para revalidação manual. O novo teste é suficiente como evidência automática: usa uma única `PopupInstancia`, seis itens reais e compõe a mesma instância nas dimensões `50x20`, `40x10`, `77x8` e `50x20`, produzindo `coluna → matriz → linha → coluna`. Verifica as grades físicas completas, sem placeholders, a identidade da instância, cursor e marcações por ID, a preservação da ordem e do envelope, e não atribui manualmente a formação nem mocka o algoritmo.

## Runtime e recomposição

`_layout_popup_marcacao` reexecuta `_selecionar_formacao` em toda composição, usando largura e altura correntes, e recalcula colunas e grade. Formação e grade são estado derivado vivo, não parte da declaração ou do envelope semântico; cursor e marcações permanecem por ID e a ordem lógica não muda. Na demo, resize atualiza as dimensões antes de `_resolver_conteudo`; `renderizar_estado` encaminha essas dimensões com a mesma instância.

## Verificações

- Testes focais: **60 passed**.
- Novo teste isolado `test_resize_recalcula_formacao_na_mesma_instancia_preservando_ids`: **1 passed**.
- Suíte completa: **1157 passed**.
- `git diff --check`: sem achados.

A divergência TTY anterior não é resolvida apenas pela aprovação automática. Requer repetição focal no TTY com dimensões explicitamente capazes de produzir coluna, matriz e linha. Não foi identificado defeito de implementação nem novo achado material.

## Status

`I5_MANUAL_VALIDATION_REQUIRED`
