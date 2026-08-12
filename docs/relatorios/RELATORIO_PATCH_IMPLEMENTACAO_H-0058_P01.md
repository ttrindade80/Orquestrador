---
cadeia:
  raiz: docs/relatorios/IMP-0058-popup-lista-navegavel-marcacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0058.md

achados_tratados:
  - MV-H0058-01
---

# Relatório do patch de implementação H-0058 P01

## Causa comprovada

O fluxo de composição de `PopupInstancia` já reexecuta `_selecionar_formacao`
em cada chamada de layout, usando `largura_corpo` e `altura_corpo` correntes.
O resize da demo dispara nova renderização pelo caminho existente até
`sobrepor_no_corpo`; não foi identificado cache da primeira formação nem
recriação da instância.

O teste de resize existente verificava identidade, cursor e marcações, mas
não verificava a formação física nem a grade resultante. Assim, não havia
regressão automatizada para o comportamento observado manualmente.

## Arquivos alterados

- `tela/teste_popup.py`
- este relatório.

## Correção aplicada

Foi acrescentado teste determinístico na mesma instância, com recomposições
nas dimensões que produzem, respectivamente, `coluna`, `matriz`, `linha` e
`coluna` novamente. O teste verifica a grade sem placeholders, a identidade da
instância, o cursor e as marcações por ID, além da preservação do envelope.

Não foram alterados configuração, demo, contrato, nomenclatura ou o caminho de
confirmação posterior H-0059.

## Testes executados

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py`: **60 passed**.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest`: **1157 passed**.
- `git diff --check`: sem achados.

## Bloqueios

Nenhum.
