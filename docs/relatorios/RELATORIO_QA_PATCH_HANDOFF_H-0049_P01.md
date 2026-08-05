# Relatório QA do patch de handoff — H-0049 / P01

```yaml
cadeia:
  raiz: docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P01.md
achados_retestados:
  - H49-QA-01
  - H49-QA-04
  - H49-QA-06
  - H49-QA-09
```

## Resultado do reteste

- `H49-QA-01`: resolvido. O domínio de `max_caracteres` está fechado como
  inteiro `1..200`, com limites inclusivos; o plano exige aceitar `1` e `200`
  e rejeitar zero, negativos, `201` e valores não inteiros.
- `H49-QA-04`: resolvido. O baseline dos 74 JSONs usa título à esquerda,
  `recuo_lateral: 0`, maiúsculas e espaços laterais; a descrição usa `200`,
  esquerda, `recuo: 1` e `inicio_de_frase`. O texto identifica `0/1` como
  baseline de migração, preserva o quadro físico vigente e descarta `3/10`,
  pertencentes ao artefato global não consumido, sem migração, compensação ou
  reinterpretação. O bloqueio `IMPLEMENTATION_BLOCKED` permanece previsto.
- `H49-QA-06`: resolvido. Fixtures persistentes e arquivos adicionais estão
  proibidos; dados extras devem ser fabricados em memória somente nos três
  arquivos de teste autorizados, com bloqueio se forem insuficientes.
- `H49-QA-09`: resolvido. O algoritmo fechado usa o primeiro `c.isalpha()` e
  somente `c.upper()`, preserva prefixo/sufixo, incorpora expansões Unicode e
  veda locale, normalização, regex, lista manual, ASCII e biblioteca externa;
  todos os exemplos exigidos estão presentes.

## Evidências e preservações

A comparação nominal produziu `74` entradas em cada lista, sem diferença,
duplicata ou arquivo inexistente. A leitura de `config/elementos/cabecalho.json`
confirma `3` e `10` apenas no artefato obsoleto. A busca focal em
`geometria_caixa.py` confirma o quadro vigente de um espaço no topo e um espaço
com alinhamento à esquerda no conteúdo, compatível com `0/1`.

Foram executados o diff obrigatório, as quatro buscas de resíduos,
`git diff --check` e os testes de existência dos dois documentos.

```yaml
status: H1_HANDOFF_APPROVED
implementacao_liberada: true
nota_factual_relatorio_patch: true
proxima_acao: CORRECAO_FACTUAL_RELATORIO
```

Nota factual: o relatório P01 não registra explicitamente
`status: PATCH_HANDOFF_COMPLETED`, os comandos de verificação executados nem
os bloqueios. Corrigir pontualmente esse relatório antes da implementação; não
é necessário novo patch do handoff.
