# Relatório de patch — H-0053 P04

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status: IMPLEMENTATION_PATCHED
objeto: H-0053
patch: P04
achados_tratados:
  - H-0053-P03-A
```

## Execução

* Causa raiz: o renderer de `arvore_colapsavel` convertia cursor ausente em
  índice `0`, enquanto `estado_chip_arvore()` reconhecia corretamente a
  ausência. Assim, foco sem cursor marcava visualmente o primeiro nó sem item
  corrente real.
* Correção: `tela/navegacao.py` ganhou a reconciliação do cursor focalizado
  usando a projeção visível existente. Quando há nós visíveis, o primeiro
  índice válido é usado somente como cursor reconciliado; projeção vazia não
  recebe cursor sintético. `demo/demo.py` aplica essa reconciliação no
  boundary de preparação, processamento e renderização.
* Renderer: `tela/renderizacao/console.py` deixou de usar fallback semântico
  para `cursor=0`; ausência de cursor não produz indicador. Chip e renderer
  recebem o mesmo estado reconciliado.
* Testes: adicionada reprodução no boundary real com foco de árvore e
  `cursores={}`, verificando cursor runtime, indicador e chip no mesmo nó.
  Também foi adicionada prova negativa do fallback visual e prova de projeção
  vazia sem cursor.

## Validação

```text
pytest -q tela/teste_navegacao.py       -> 60 passed
pytest -q demo/teste_demo_console.py    -> 11 passed
pytest -q                               -> 1074 passed
git diff --check                        -> OK
```

Arquivos alterados no patch: `tela/navegacao.py`,
`tela/renderizacao/console.py`, `demo/demo.py`, `tela/teste_navegacao.py` e
`demo/teste_demo_console.py`. Fixture e documentação normativa não foram
alteradas. Relatório criado: este arquivo.

Stage permaneceu vazio; nenhum commit foi feito. Validação manual em TTY real
continua pendente e pertence à etapa posterior `QA_POS_PATCH_IMPLEMENTACAO`.
