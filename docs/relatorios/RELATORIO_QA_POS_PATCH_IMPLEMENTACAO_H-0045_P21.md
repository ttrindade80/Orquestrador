---
tipo_execucao: QA_POS_PATCH_IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
achado: VM-H0045-R06-001
data: "2026-08-02"
---

# QA pós-patch — H-0045 P21

## Status

`I2_IMPLEMENTATION_PATCH_REQUIRED`. `VM-H0045-R06-001` permanece aberto.

## Conformidade do código e das configurações

O delta focal de `tela/selecao.py` está conforme: `rotulo_esc` é pura, usa a
seleção reconciliada do console recebido, retorna `Limpar` somente para
seleção múltipla não vazia e preserva `Sair`, `Voltar` ou outro rótulo nos
demais casos. Não altera `rotulo_enter`, `limpar`, `reconciliar` ou políticas
de seleção. O helper focal tem a mesma semântica da autoridade existente para
consoles válidos; não foi registrado achado por duplicação nominal.

Em `_linhas_barra`, o fallback original é preservado e apenas o texto do chip
`Esc` é materializado quando `forma_exibicao` é `rotulo_dinamico_esc`. Tecla,
ordem, atividade, cores, foco, paginação, largura e comportamento de Enter
permanecem preservados; ausência de foco mantém o rótulo original.

Nas três configurações de seleção múltipla, somente o `forma_exibicao` do chip
`Esc` mudou para `rotulo_dinamico_esc`; `Sair`, os demais chips e os demais
campos permanecem preservados. As duas configurações de seleção única mantêm
`visivel_ativo` e não recebem comportamento dinâmico. O delta P21 efetivo está
limitado aos oito arquivos declarados; `demo/teste_demo_navegacao.py` não tem
delta P21 obrigatório. Alterações históricas adicionais presentes no worktree
não foram atribuídas a este patch.

## Provas automáticas e suítes

Há prova para seleção vazia, `Voltar` como fallback puro, uma/várias seleções,
seleção entre páginas, primeiro `Esc` limpando sem sair, reaparecimento do
rótulo original, segundo `Esc` em tela raiz (`Sair`), exclusão simultânea dos
rótulos, mudança de página, resize, foco, seleção única, reconciliação e
regressões de Enter/Espaço/paginação.

As execuções obrigatórias resultaram em:

- suíte focal: **482 passed**;
- suíte completa: **896 passed**;
- `git diff --check`: **limpo**.

## Achado — segundo Esc em tela aninhada

Não existe prova ponta a ponta de uma tela aninhada com seleção ativa em que o
primeiro `Esc` limpa sem retornar, o chip volta a `Voltar` e o segundo `Esc`
retorna à tela anterior. O teste existente prova somente o segundo `Esc` em
tela raiz, com `Sair`; o teste de `Voltar` cobre apenas a função pura de
fallback. A exigência de §22 permanece materialmente incompleta. É necessário
patch que forneça essa prova real antes do encerramento do achado.

## Validação manual focal

Não executada, conforme o escopo. Após correção do achado, permanece necessária
a validação manual focal do usuário, incluindo a sequência aninhada.
