# Relatório de Validação Manual — H-0050 — R02

- Executor: usuário humano.
- Ambiente: TTY real.
- Rodada: segunda validação manual, após `254_passed` nos testes focais e `1028_passed` nos testes completos.

## Critérios validados

1. Símbolos `␣` e `⏎`: **CONFORME**.
2. Chips Verboso e Ajuda, e ordem da barra: **CONFORME**.
3. Quatro itens e indicadores `○`/`●`: **CONFORME**.
4. Alternância por `Insert`: **CONFORME**.
5. Execução `dry_run` com `item_01` e `item_02`: **DIVERGENTE**. O usuário registrou: “A execução não está implementada.” Não houve fluxo de execução utilizável; não foi possível confirmar o modo recebido nem os dois IDs no resultado. Causa técnica: `NAO_CONFIRMADA`.
6. Retorno e nova abertura: o retorno preservando `dry_run` ficou **NAO_EXECUTADO_BLOQUEADO**, pois não foi possível chegar a um resultado executado e retornar à tela de origem. A nova abertura em `Executar` foi **CONFORME**. Observou-se adicionalmente que o comando `Todos` não está habilitado.
7. Redimensionamento: **CONFORME**.

## Novos achados

### MV-H0050-05 — execução não disponível na demonstração

- Resultado: aberto.
- Evidência: o cenário `dry_run` foi selecionado, mas não houve execução utilizável para validar modo e IDs no resultado; o usuário descreveu que a execução não está implementada.
- Impacto: impede validar o resultado com `item_01` e `item_02` e o retorno preservando `Dry-Run`.
- Causa: `NAO_CONFIRMADA`.

### MV-H0050-06 — comando `Todos` não habilitado

- Resultado: aberto.
- Evidência: o usuário informou que `Todos` não está habilitado.
- Impacto: impede validar a seleção coletiva prevista pela barra.
- Causa: `NAO_CONFIRMADA`.

## Conclusão

Permanecem conformes os símbolos, chips, ordem da barra, quatro itens, indicadores, alternância por `Insert`, redimensionamento e nova abertura iniciando em `Executar`. Os achados `MV-H0050-01` a `MV-H0050-04` permanecem resolvidos.

**Status global:** `MANUAL_VALIDATION_FAILED`

Há dois novos defeitos funcionais observados; a execução obrigatória não pôde ser validada e o retorno ficou bloqueado por consequência. A conformidade dos demais critérios não permite aprovação parcial.

**Próxima ação:** `PATCH_IMPLEMENTACAO`
