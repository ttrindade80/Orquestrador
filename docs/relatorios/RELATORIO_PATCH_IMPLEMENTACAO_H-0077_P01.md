---
cadeia:
  raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0077_POS_P01.md

achados_tratados:
  - QA-IMPL-H0077-01
  - QA-IMPL-H0077-02

achados_nao_tratados:
  - QA-IMPL-H0077-03
---

# Relatório do patch de implementação H-0077 P01

## Alterações

Os três testes P16 autorizados em `tela/teste_paginacao.py` foram
reconstruídos para usar fixtures cuja ocupação corresponde às linhas físicas
produzidas pela composição canônica. As mesmas políticas foram preservadas:
`permitir_quebra` aproveita o resíduo e continua na página seguinte;
`permitir_quebra_somente_se_maior_que_pagina` move integralmente o item quando
ele não cabe no resíduo; e o item maior que a página continua fragmentado nas
três políticas, com início em nova página para as políticas que o exigem.
Não houve alteração funcional de composição ou paginação.

Em `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`, foi
removido exclusivamente o literal residual `\n` fora do objeto JSON. A
estrutura, os valores e a semântica foram preservados.

## Verificações

- Fixture H-0063: `python -m json.tool` passou; o diff contém somente a
  remoção do residual autorizado.
- Três testes P16: `3 passed`.
- Sete testes H-0063 solicitados: `7 passed`.
- Suíte focal integral H-0077: `631 passed, 1 failed`.
- Regressão H-0076: `87 passed`.

A única falha da suíte focal é a permanência exata do resíduo independente
H-0070: `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`,
na expectativa de recuo (`2 >= 4`). O caminho não verboso e o arquivo H-0070
não foram alterados. Não surgiram falhas novas relativas aos achados tratados.

## Bloqueios

Nenhum bloqueio de escopo. Os comandos pytest emitiram apenas aviso de cache
não gravável no ambiente, sem afetar a execução. QA pós-patch, fechamento,
stage, commit e push não foram realizados.
