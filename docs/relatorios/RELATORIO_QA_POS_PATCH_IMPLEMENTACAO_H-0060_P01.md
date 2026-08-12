# Relatório de QA pós-patch da implementação H-0060 P01

## Cadeia

- raiz: `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0060_P01.md`

## Achados retestados

- QA-IMP-0060-001 — resolvido. Para `marcacao: exclusiva` e `marcacao: multipla`, o teste demonstrativo executa linha → matriz e matriz → coluna na mesma instância. Afirma formação anterior/posterior, identidade, `cursor_id`, marcações por ID, grade física e os seis textos em cada saída materializada.
- QA-IMP-0060-002 — resolvido. O caso H-0058 em `23x6` compara por igualdade com o quadro vigente de terminal insuficiente, confirma largura e altura exatas, quatro linhas vazias, ausência dos seis textos e ausência de reticências. A asserção permissiva anterior não existe mais; representação parcial não é aceita.
- QA-IMP-0060-003 — resolvido. Em `55x13`, instrução de uma linha/duas linhas seleciona coluna/matriz; em `40x13`/`35x13`, chips em uma/duas linhas selecionam coluna/matriz. As linhas físicas de instrução/chips são afirmadas, ambas as saídas são materializadas e os seis itens permanecem presentes.

## Execução independente

- `python -m pytest tela/teste_popup.py` — 63 passed.
- `python -m pytest demo/teste_demo_popup.py` — 15 passed.
- `python -m pytest` — 1.175 passed em 29,92 s.
- `git diff --check` — limpo, sem saída.

## Escopo e preservação

O diff focal obrigatório mostra alterações P01 em `tela/teste_popup.py` e `demo/teste_demo_popup.py`, além do relatório do patch declarado. O diff do renderer corresponde ao delta original de implementação; não há delta da fixture `demo/fixtures/h0058_popup_lista_marcacao.py`. Não foi identificado novo defeito material diretamente relacionado. As demais alterações já presentes no worktree não foram atribuídas ao P01 nem modificadas por este QA.

## Status final

`IMPLEMENTATION_APPROVED`
