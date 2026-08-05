# RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0050_P02

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P02.md
achados_retestados:
  - MV-H0050-01
  - MV-H0050-02
  - MV-H0050-03
  - MV-H0050-04
```

## Resultado do reteste

- `MV-H0050-01`: **passou**. Causa confirmada: literais divergentes nas
  configurações. Ambas renderizam `[␣] Marcar`, `[⏎] Todos`/`Executar` e
  preservam `[Ins] Executar`/`Dry-Run`; `[Espaço]` e `[Enter]` não aparecem
  como rótulos.
- `MV-H0050-02`: **passou**. `[V] Verboso` e `[?] Ajuda` vêm da declaração
  das duas barras. A ordem observada é `[Esc]`, seleção, Enter, `[Ins]`,
  Verboso, Ajuda; não há injeção focal em `demo/demo.py` ou no renderizador.
  Alternância de Verboso/Ajuda não altera o controle universal.
- `MV-H0050-03`: **passou**. As duas telas declaram `distribuicao_matricial`;
  os quatro itens aparecem com `→` distinto de `○`/`●`. Espaço marca,
  desmarca e alterna Enter entre Todos e Executar. A infraestrutura e a
  política visual existentes foram preservadas.
- `MV-H0050-04`: **passou**. Ambas têm exatamente quatro IDs estáveis
  (`item_01` a `item_04`) e a fixture cobre todos. `item_01` + `item_02`
  produzem lote ordenado de dois IDs; o modo `dry_run` aparece no resultado,
  é preservado no retorno e reinicializa conforme `modo_inicial` em nova
  abertura.

`linhas.maximo: 3` está restrito às duas configurações H-0050. A demonstração
  automatizada em 42 colunas manteve os seis chips acessíveis, sem perda
  semântica; em largura normal não criou linhas extras desnecessárias. Não há
  delta em `config/estilo.json`, `demo/demo.py` ou no renderizador de barra.

## Evidências e preservações

Testes focais: **254 passed**. Suíte completa: **1028 passed**. A demonstração
das duas configurações confirmou os quatro itens, símbolos, chips, marcador,
lote, modo, retorno e reinicialização. As preservações do P01, inclusive
validação fechada, tipos inválidos, `[Ins]`, posição após Enter, registro,
captura privada, lote vazio, `cor_alerta`, retorno, nova abertura e H-0044,
permanecem cobertas; não surgiu novo achado. `git diff --check` passou.

Não há bloqueio técnico. A validação manual em TTY real permanece pendente e
não foi executada nem aprovada pelo QA.

```yaml
status: I5_MANUAL_VALIDATION_REQUIRED
proxima_acao: VALIDACAO_MANUAL
```
