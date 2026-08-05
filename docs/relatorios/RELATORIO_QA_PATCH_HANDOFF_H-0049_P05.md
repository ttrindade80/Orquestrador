# Relatório de QA do patch de handoff — H-0049 / P05

```yaml
cadeia:
  raiz: docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P05.md

objetos_retestados:
  - H49-P04-QA-16
  - H49-P04-QA-19
```

## Resultado

O comando integral exato ocorre uma vez no handoff:
`PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --maxfail=0`.
A chamada multilinear dos onze arquivos e as três chamadas `-k h0049`
permanecem focais. Não há chamada integral concorrente incompleta.

O resultado obrigatório está fechado: `falhas: 0`, `erros: 0`,
`reducao_de_testes: false`, `fixture_antiga_incompativel: false` e
`fallback_de_apresentacao: false`. O handoff também mantém explícitos
`--maxfail=0`, o efeito somente de verbosidade de `-q`, a proibição de
`skip`/`xfail`/filtros/redução de coleta, a comparação da coleta válida e as
pré-condições para remover `config/elementos/cabecalho.json` e criar
`IMP-0049`.

O manifesto aprovado no P04 permanece preservado na leitura integral dos
quatro documentos autorizados; não há versão Git histórica dos documentos
não rastreados para uma comparação material anterior.

## H49-P04-QA-19 — evidência

Ambos os documentos estão `??` e, portanto, o modo correto é
`git_diff_no_index`:

```yaml
docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md:
  modo: git_diff_no_index
  retorno_git_diff_no_index: 1
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P05.md:
  modo: git_diff_no_index
  retorno_git_diff_no_index: 1
```

O retorno `1` foi confirmado como diferença esperada na chamada direta, sem
stage preparado. Contudo, a função prescrita no handoff falha em `zsh` antes
de tratar esse retorno: `local status` colide com o parâmetro somente leitura
`status`, produzindo `read-only variable: status` nos dois documentos. Assim,
a evidência mecânica exigida pela função não está concluída, e o relatório P05
afirma uma verificação que não se reproduz. `git diff --check` e o check
textual passaram.

```yaml
status: H4_QA_EVIDENCE_INCOMPLETE
implementacao_liberada: false
proxima_acao: COMPLETAR_EVIDENCIA
```
