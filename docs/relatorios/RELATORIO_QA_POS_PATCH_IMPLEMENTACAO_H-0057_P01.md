# QA pós-patch — H-0057/P01

```yaml
item: ITEM-0017
handoff: H-0057
patch: P01
status: I5_MANUAL_VALIDATION_REQUIRED
```

## Resultado

`QA-H0057-IMP-001` está corrigido. `_quebrar_texto` consome separadores
fisicamente, sem `.strip()`, colapso, truncamento, duplicação ou reticências.
O mecanismo é `"".join(linhas) == entrada_original`; a verificação direta
passou para `a  b`, `a   b`, `aa  bb`, whitespace puro, extremidades e palavra
longa. Os testes também afirmam essa invariante, não apenas caracteres
não-espaço.

Casos confirmados: dois e três espaços preservados, separação entre palavras
maiores preservada, `"     "` em `3` resulta em `"   "` e `"  "`, whitespace
inicial/final preservado, palavras que cabem permanecem inteiras e palavra
maior que a largura é dividida em blocos limitados, sem perda.

## Testes

- Focal direto: `33 passed`, código 0.
- Conjunto H-0057 (`tela/teste_popup.py` + `demo/teste_demo_popup.py`):
  `42 passed`, código 0; os novos casos exercitam whitespace real e a
  reconstrução integral.
- Suíte canônica: `1139 passed`, código 0.

Alinhamento esquerda/centralizado/justificado, última linha justificada à
esquerda, geometria, chips multilinha, resize, centralização, terminal pequeno,
restauração e mesma instância permanecem cobertos. H-0056 (`popup_basico`,
modalidade, tecla inerte, `Esc`, `ABORTADO` sem payload e tela subjacente)
permanece verde. Não foram introduzidas capacidades de H-0058/H-0059.

## Diff e escopo

`git diff --check -- tela/renderizacao/popup.py tela/teste_popup.py` passou sem
apontamentos. A inspeção focal não encontrou regressão material; arquivos
adicionais presentes no worktree não foram atribuídos ao P01 sem evidência.

Não foi executada validação visual/interativa TTY. Com o achado corrigido,
testes verdes e sem novo defeito automatizado, resta somente a validação
manual visual/interativa prevista no handoff.
