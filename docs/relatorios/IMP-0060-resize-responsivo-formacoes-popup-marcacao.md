# Implementação H-0060 — Resize responsivo das formações do pop-up de marcação

## Arquivos alterados

- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`
- `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md`

A fixture `demo/fixtures/h0058_popup_lista_marcacao.py` permaneceu intacta.

## Implementação

- A seleção mantém `coluna` como formação preferencial.
- A seleção de `matriz` avalia todas as candidatas com pelo menos duas linhas,
  normaliza colunas não vazias e retém a maior quantidade real de colunas que
  cabe integralmente.
- `linha` é tratada como formação distinta e só é escolhida com exatamente uma
  linha física disponível.
- O vão de dois espaços entre itens usa uma constante única no cálculo e na
  materialização da saída.
- A grade continua sendo preenchida verticalmente, sem placeholders, com todos
  os IDs uma única vez e na ordem lógica.
- O estado vivo, a identidade da instância, cursor e marcações são preservados
  durante a recomposição; a navegação existente por eixo permanece vigente.
- O overhead real continua descontando instrução embrulhada, chips distribuídos
  e espaçamentos antes da escolha da formação.

## Testes alterados

`tela/teste_popup.py` recebeu cobertura para maximização de colunas reais,
colunas vazias, mínimo de duas linhas da matriz, formação linha, vão
compartilhado, largura integral dos itens, overhead de instrução/chips,
recomposição e navegação toroidal. `demo/teste_demo_popup.py` recebeu a
sequência dimensional H-0058 para as políticas exclusiva e múltipla, mantendo
a mesma instância e o estado vivo.

## Comandos e resultados

- `python -m pytest tela/teste_popup.py` — **61 passed**.
- `python -m pytest demo/teste_demo_popup.py` — **15 passed**.
- `python -m pytest` — **1173 passed** em 29,98 s, conforme `pytest.ini`
  (`testpaths = tela demo`).
- `git diff --check` — executado sem achados.

## Bloqueios ou desvios

Nenhum. Não foram introduzidos paginação, truncamento, reticências,
placeholders, redução de espaçamentos ou mecanismo paralelo de `SIGWINCH`.
