# QA pós-patch — H-0045 P16

## Achados

- Resolvidos pelo P16: as três políticas têm ramos distintos e efeito real; o
  resize do caminho TUI preserva o modelo lógico e recalcula apenas a
  apresentação; as telas fixas e os casos VAZIO/CONTINUACAO não regeneram
  conteúdo durante SIGWINCH.
- Pendentes transportados: `VM-H0045-R06-001` e `QA-H0045-P08-001` não foram
  declarados resolvidos.
- Novos achados técnicos: nenhum.

## Verificações focais

- `permitir_quebra` usa o espaço residual; `evitar_quebra` inicia cada item em
  página nova; a política condicional mantém o item junto quando possível,
  move-o inteiro quando necessário e fragmenta itens maiores que a página.
  Testes também confirmam identidade, ordem e soma de linhas sem perda ou
  duplicação.
- O bloco real de `SIGWINCH` em `demo/demo.py` não reconstrói modelo, reaplica
  caso nem zera foco/cursor/página; chama somente a reconciliação de paginação.
  Hash e snapshot estrutural permanecem invariantes nas geometrias verificadas.
  Construtores legados permanecem apenas para testes e não são usados nesse
  caminho TUI.
- Os cinco pontos de entrada foram verificados: três telas com introdução não
  navegável e quatro itens `1.`–`4.` sob uma única política; VAZIO com JSON
  próprio, zero itens e plano `1/1`; CONTINUACAO com JSON próprio, conteúdo
  fixo e páginas somente de continuação. O delta P16 não altera renderer,
  teste do renderer ou documentação normativa.

## Testes

- Focal obrigatório: `64 passed`.
- Suíte completa obrigatória: `851 passed`.
- Cobertura P16 focal: `11 passed`, incluindo políticas, resize, hashes,
  VAZIO, CONTINUACAO e os três pontos de entrada de política.
- `git diff --check`: sem saída.

## Status

`I5_MANUAL_VALIDATION_REQUIRED`

## Validação manual

15/17–17/17 permanece pendente e reservada ao usuário em TTY real. Não foi
executada validação interativa. 6/17–14/17 não foram reabertas.
