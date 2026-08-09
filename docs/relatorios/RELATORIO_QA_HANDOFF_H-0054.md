# Relatório QA do handoff H-0054

```yaml
status: H2_HANDOFF_PATCH_REQUIRED
handoff: H-0054
capacidade: selecao_multinivel
```

## Achados materiais

### QA-H0054-001 — Invariantes de atualização dos chips são excessivas

- **Requisito/autoridade afetada:** preservação das regras vigentes de chips; `contrato_console.md` §§23.4–23.5, `contrato_barra_de_menus.md` §§9 e 23.1 e `contrato_chip.md` §9.
- **Evidência focal:** na seção 3, o handoff afirma que ao mover o cursor “somente `ec` muda” e que ao selecionar/desselecionar “somente” os marcadores `tg` mudam. A seção 2.2 também exclui ação posterior à seleção, embora o cenário declare `[Esc]`.
- **Impacto:** a atividade de `[␣] Selecionar` deve ser recalculada quando o cursor muda entre itens selecionáveis e não selecionáveis; com seleção ativa, `[Esc]` conserva a semântica vigente de `Limpar`. A redação pode impedir essas atualizações legítimas e alterar comportamento transversal.
- **Correção material necessária:** limitar as invariantes a cursor e marcadores no corpo e declarar explicitamente a recomputação dos chips existentes, inclusive a limpeza por `[Esc]`, sem criar semântica nova de `Enter` ou de execução.

### QA-H0054-002 — Reconciliação não remove IDs que deixam de ser navegáveis

- **Requisito/autoridade afetada:** invariantes e reconciliação da seleção múltipla em `contrato_console.md` §§23.2–23.3.
- **Evidência focal:** a seção 2.2 restringe a remoção a IDs inexistentes ou que deixaram de ser selecionáveis.
- **Impacto:** um ID que permaneça existente e selecionável, mas deixe de ser navegável, pode continuar no conjunto de seleção, contrariando a invariável vigente e podendo contaminar a operação consumidora.
- **Correção material necessária:** incluir a perda de navegabilidade entre as condições já contratadas de reconciliação, preservando a ordem lógica e sem criar estado novo.

### QA-H0054-003 — Relatório nominal conflita com a fronteira de arquivos preservados

- **Requisito/autoridade afetada:** exequibilidade e distinção entre arquivos autorizados e preservados; seções 4, 5 e 11 do próprio handoff.
- **Evidência focal:** a seção 11 exige `docs/relatorios/IMP-0054-selecao-multinivel.md`, mas esse caminho não está na seção 4 e a seção 5 manda preservar qualquer caminho não listado, incluindo relatórios.
- **Impacto:** a entrega nominal do relatório de implementação fica simultaneamente exigida e fora da autorização, podendo ser tratada como alteração proibida.
- **Correção material necessária:** isentar explicitamente esse relatório novo da preservação e autorizar sua criação no caminho exato, mantendo relatórios históricos preservados; ou definir formalmente o responsável externo por sua materialização.
