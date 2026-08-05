# Relatório de QA do patch de handoff — H-0049 / P04

```yaml
cadeia:
  raiz: docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P04.md

objeto_retestado:
  - manifesto_de_11_arquivos
  - politica_de_adequacao_de_fixtures
  - preservacao_funcional_dos_testes
```

## Resultado

O manifesto P04 está nominalmente completo. Os onze arquivos acrescentados são
exatamente:

- `tela/teste_resultado_execucao.py`
- `tela/teste_navegacao.py`
- `tela/testes_renderizador/integracao.py`
- `tela/testes_renderizador/composicao_corpo.py`
- `tela/testes_renderizador/comum.py`
- `tela/testes_renderizador/lancador.py`
- `tela/testes_renderizador/matriz_participantes.py`
- `tela/testes_renderizador/selecao.py`
- `demo/teste_demo_navegacao.py`
- `demo/teste_demo_paginacao.py`
- `demo/teste_diagnostico.py`

A conferência AST reproduziu 58 ocorrências antigas em 13 arquivos. O manifesto
fecha 2 arquivos originais + 11 adicionais = 14 autorizados; `tela/teste_loader.py`
é o único dos 14 sem ocorrência antiga e permanece reservado aos novos cenários
do schema. A classificação também fecha 4 falhas observadas + 7 casos mascarados
pelo fallback = 11. A correção factual do P03, de “seis” para sete mascarados,
está coerente no handoff e no relatório P04.

As quatro falhas observadas são `tela/teste_resultado_execucao.py`,
`tela/testes_renderizador/integracao.py`,
`tela/testes_renderizador/composicao_corpo.py` e `demo/teste_diagnostico.py`.
O handoff preserva, respectivamente, carregamento de resultado, IDs duplicados,
percentual cuja soma não é 100, fração com peso zero e ordem matricial inválida,
com as exceções e mensagens previstas. Os sete mascarados são `tela/teste_navegacao.py`,
`tela/testes_renderizador/comum.py`, `tela/testes_renderizador/lancador.py`,
`tela/testes_renderizador/matriz_participantes.py`,
`tela/testes_renderizador/selecao.py`, `demo/teste_demo_navegacao.py` e
`demo/teste_demo_paginacao.py`.

## Política confirmada

O baseline exigido está completo dentro de `cabecalho.apresentacao`, preservando
`titulo` e `descricao`, sem `3/10`, default, fallback ou configuração externa.
Os onze arquivos adicionais podem receber somente essa adequação em estruturas
preexistentes. Não são autorizados novos cenários, fixtures, helpers
compartilhados, arquivos, comportamentos, expectativas ou JSONs persistentes.
As negativas intencionais do H-0049 ficam somente nos três arquivos originais;
nenhuma das onze adicionais contém negativa desse schema. IDs duplicados,
percentual inválido, peso zero e ordem `diagonal` continuam esperando
`TelaEstruturaInvalida`, não `TelaCampoObrigatorioAusente`.

As proibições funcionais, a preservação visual baseline 0/1, o estado parcial,
o inventário AST final, a suíte focal única, o futuro `IMP-0049` e os registros
de zero alterações funcionais estão delimitados corretamente. Também permanecem
registradas as correções anteriores: 72 telas estruturais, 8 conteúdos externos
com hashes, domínio 1..200, Unicode de `inicio_de_frase`, descarte de 3/10,
proibição de fixture persistente, remoção futura de
`config/elementos/cabecalho.json` e manifesto técnico de produção.

## Achados e decisão

1. **H49-P04-QA-16 — defeito material.** A validação integral do handoff termina
   em `PYTHONDONTWRITEBYTECODE=1 python -m pytest`; a chamada focal usa `-q`, mas
   nenhuma contém o comando obrigatório
   `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --maxfail=0`. A exigência de
   suíte integral não está reproduzida literalmente e deve ser corrigida antes
   da implementação.

2. **H49-P04-QA-19 — evidência mecânica limitada.** O `git diff --` obrigatório
   não produziu saída porque o handoff e o relatório P04 estão não rastreados
   (`??`). Assim, a afirmação do P04 de que o diff foi revisado não é
   independentemente demonstrável neste worktree. Os onze arquivos adicionais
   estão sem alteração no estado atual; alterações externas já existentes foram
   preservadas e não foram atribuídas ao P04.

```yaml
status: H2_HANDOFF_PATCH_REQUIRED
implementacao_liberada: false
proxima_acao: PATCH_HANDOFF
```
