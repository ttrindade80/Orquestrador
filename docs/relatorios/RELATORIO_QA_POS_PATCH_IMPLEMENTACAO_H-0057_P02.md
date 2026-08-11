# Relatório QA pós-patch — H-0057 P02

```yaml
item: ITEM-0017
handoff: H-0057
patch: P02
status: I5_MANUAL_VALIDATION_REQUIRED
```

## Resultado

`MV-H0057-001` está corrigido. Em `tela/renderizacao/popup.py`, a
justificação mede o comprimento físico atual com `_largura_sem_ansi`, calcula
`extra = largura_alvo - comprimento_atual` e usa
`base, resto = divmod(extra, numero_de_vaos)`. Cada vão recebe `base`, e os
primeiros `resto` vãos recebem `+1`, da esquerda para a direita. Não há
condição baseada na paridade do terminal.

Os casos explícitos verificam divisão exata, resto 1 e resto maior que 1. O
exemplo `extra = 5`, `vaos = 3` produz incrementos `[2, 2, 1]`; as asserções
confirmam a linha `a   b   c  d` com largura final 12. Os casos também
confirmam largura final exata, última linha alinhada à esquerda e linha sem
vão sem espaços internos inventados.

O whitespace original entre tokens, inclusive múltiplo e nas extremidades, é
preservado; a justificação apenas acrescenta espaços. Não há `.strip()`,
colapso ou normalização no caminho auditado. O wrapping P01 permanece
íntegro.

## Regressões e fronteiras

Os testes preservam largura intrínseca, wrapping, altura, centralização,
resize, chips multilinha, terminal pequeno, restauração e a mesma instância.
H-0056 permanece íntegro: `popup_basico`, `[Esc] Voltar`, modalidade,
tecla não declarada inerte, `ABORTADO` sem payload e retorno à mesma tela.
Não foram introduzidas capacidades de H-0058/H-0059.

## Evidências

- `tela/teste_popup.py`: **39 passed**, código 0.
- Conjunto focal H-0057: **48 passed**, código 0.
- Suíte canônica: **1145 passed**, código 0.
- `git diff --check -- tela/renderizacao/popup.py tela/teste_popup.py`: OK.
- Diff focal restrito aos dois arquivos auditados; nenhum outro arquivo do
  worktree foi atribuído ao P02.

Não foi executada validação TTY. Solicita-se validação manual focal de texto
justificado em largura par e ímpar, redução/aumento de largura, ocupação da
borda direita e centralização contínua do pop-up.
