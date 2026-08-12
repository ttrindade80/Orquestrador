# Relatório do patch de implementação H-0060 P01

## Cadeia

- raiz: `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0060.md`

## Achados tratados

- QA-IMP-0060-001
- QA-IMP-0060-002
- QA-IMP-0060-003

## Evidências adicionadas ou fortalecidas

- O teste demonstrativo H-0060 percorre, para `marcacao: exclusiva` e
  `marcacao: multipla`, as transições diretas linha → matriz e matriz →
  coluna. Cada recomposição afirma a mesma instância, o cursor pelo ID, as
  marcações pelos IDs, a grade esperada e a presença dos seis itens na saída
  materializada.
- Para a fixture H-0058, o caso `23x6` usa igualdade contra o quadro vigente
  de terminal insuficiente: duas linhas de aviso e quatro linhas vazias. O
  teste também afirma largura/altura exatas, ausência dos seis textos de item
  e ausência de reticências, sem disjunção permissiva.
- A fronteira de wrapping da instrução usa `55x13`: uma linha seleciona
  coluna; duas linhas selecionam matriz. As duas saídas são materializadas e
  preservam todos os itens.
- A fronteira de chips compara `40x13` com `35x13`: uma linha de chips
  seleciona coluna; duas linhas selecionam matriz. As duas saídas são
  materializadas e preservam todos os itens.

## Arquivos alterados por este patch

- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`
- `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0060_P01.md`

`tela/renderizacao/popup.py` já possuía alterações no worktree antes deste
patch e não foi editado. `demo/fixtures/h0058_popup_lista_marcacao.py` também
permaneceu intacto. Não houve alteração normativa, de ADR, handoff ou
configuração estrutural.

## Comandos e resultados

- `python -m pytest tela/teste_popup.py` — 63 passed.
- `python -m pytest demo/teste_demo_popup.py` — 15 passed.
- `python -m pytest` — 1.175 passed em 30,10 s.
- `git diff --check` — passou sem saída.
- `git diff -- tela/teste_popup.py demo/teste_demo_popup.py tela/renderizacao/popup.py demo/fixtures/h0058_popup_lista_marcacao.py` — verificação focal executada; somente os testes autorizados receberam alterações neste patch, com renderer e fixture preservados.

## Bloqueios

Nenhum.
