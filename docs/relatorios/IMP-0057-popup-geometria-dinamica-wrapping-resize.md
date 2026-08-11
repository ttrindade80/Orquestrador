# Relatório de implementação — H-0057

## Arquivos

Criado: `demo/fixtures/h0057_popup_texto_dinamico.py` e este relatório.

Alterados: `tela/renderizacao/popup.py`, `tela/renderizacao/tela.py`,
`tela/teste_popup.py`, `demo/demo.py`, `demo/teste_demo_popup.py` e
`config/telas/demo/demo.json`.

## Implementação

O pop-up calcula largura intrínseca incluindo moldura, título, padding,
conteúdo e chips. Quando necessário, limita a largura pela largura física das
linhas materializadas do corpo. Com a largura final, recalcula wrapping,
chips, altura e centralização usando divisão determinística da sobra com
`// 2`.

O wrapping preserva as palavras e divide somente palavras maiores que a
largura útil quando inevitável. O alinhamento é aplicado depois da quebra para
`esquerda`, `centralizado` e `justificado`; linhas completas são justificadas
entre vãos e a última linha permanece à esquerda. A altura deriva das bordas,
espaçamentos declarados, linhas de texto e linhas de chips.

Chips usam a primitiva textual canônica da barra, o espaçamento comum e a
ordem declarada. A distribuição gulosa mantém chips inteiros, aceita múltiplas
linhas e centraliza cada linha independentemente. Chip isolado ou altura
inviável produz erro geométrico para a cadeia geral de terminal pequeno.

O overlay usa a área materializada do corpo. Resize não altera a instância
`PopupInstancia`; conteúdo, estado modal e tela subjacente permanecem. O
fluxo existente de dimensões válidas, `SIGWINCH` e quadro geral é reutilizado,
com restauração automática quando a geometria volta a caber. A declaração
`popup_basico`, seu acionamento `p` e a fixture H-0056 permaneceram sem mudança
semântica. A nova declaração `popup_texto_dinamico` e o acionamento `w` usam
conteúdo runtime determinístico.

## Verificações

- Testes focais: `35 passed` em `tela/teste_popup.py` e
  `demo/teste_demo_popup.py` (código de saída 0).
- Suíte canônica: `1132 passed` (código de saída 0), acima do baseline de
  `1118 passed`.
- Demonstração programática não-TTY, incluindo o fluxo principal com entrada
  `w`, `x` e `Esc`: abertura, wrapping em larguras 80/75, quadro geral por
  altura insuficiente, restauração, tecla `x` inerte e `Esc` com `ABORTADO` sem
  payload confirmados.
- `git diff --check`: sem apontamentos.
- Não houve stage nem commit.

## Validação manual pendente

Permanece pendente no TTY do usuário: wrapping visual, centralização,
recomposição ao reduzir/aumentar largura, entrada no quadro geral de terminal
pequeno, restauração automática, preservação da mesma instância visual e
`Esc` com retorno à tela inferior.

## Desvios e bloqueios

Nenhum desvio de escopo e nenhum bloqueio de implementação.
