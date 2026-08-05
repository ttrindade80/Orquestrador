# Relatório do patch de handoff — H-0049 / P01

```yaml
item: ITEM-0015
handoff: H-0049
patch: P01
escopo: documental
qa_original:
  - H49-QA-01
  - H49-QA-04
  - H49-QA-06
  - H49-QA-09
arquivos_alterados:
  - docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P01.md
arquivos_removidos: []
```

## Correções incorporadas

O handoff agora declara `cabecalho.apresentacao.descricao.max_caracteres`
como inteiro de `1` a `200`, com limites inclusivos. O plano de testes exige
aceitar `1` e `200` e rejeitar `0`, valores negativos, `201` e valores não
inteiros.

O baseline de migração foi alinhado à preservação visual aprovada: título à
esquerda, `recuo_lateral: 0`, maiúsculas e espaços laterais; descrição limitada
a `200`, alinhada à esquerda, com `recuo: 1` e início de frase. O handoff
explica que os espaços laterais já pertencem ao formato da borda, que `0` e
`1` preservam os espaços físicos vigentes e que `3` e `10` são valores
obsoletos de configuração global nunca consumida. A implementação não pode
migrar, reinterpretar ou compensar esses valores.

Fixture persistente foi proibida. Os três arquivos de teste já autorizados
devem fabricar documentos, modelos e variações em memória; nenhum arquivo
adicional é autorizado. A impossibilidade de expressar os testes nesse escopo
exige parada com `IMPLEMENTATION_BLOCKED`.

Também foi transportada a semântica normativa completa de `inicio_de_frase`:
busca do primeiro caractere com `str.isalpha()`, substituição exclusiva pelo
resultado exato de `str.upper()`, preservação literal do prefixo e do sufixo,
encerramento após a primeira substituição, preservação de maiúsculas
posteriores e incorporação integral de expansões Unicode. A regra é
independente de locale, não normaliza Unicode, não usa regex, lista manual,
limitação a ASCII ou biblioteca externa. Foram incluídos os exemplos
aprovados, inclusive `ßeta` → `SSeta`.

Não foram implementados código, JSONs, testes, contratos ou nomenclatura.


## Fechamento factual

execucao:
  status: PATCH_HANDOFF_COMPLETED
  verificacoes_executadas:
    - busca de max_caracteres, domínio 1..200 e formulações obsoletas no H-0049
    - busca de recuos, baseline 0/1, valores obsoletos 3/10 e preservação visual no H-0049
    - busca de fixture persistente, autorizações condicionais e arquivos adicionais no H-0049
    - busca de inicio_de_frase, isalpha, upper, locale, normalização e exemplos Unicode no H-0049
    - git diff --check no handoff e no relatório P01
    - git diff focal no handoff e no relatório P01
  bloqueios: []
