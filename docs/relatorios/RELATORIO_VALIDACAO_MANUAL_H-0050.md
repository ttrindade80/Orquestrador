# Relatório de validação manual H-0050

```yaml
handoff: H-0050
executor: USUARIO_EM_TTY_REAL
ambiente: TTY real
telas:
  - config/telas/demo/h0050_controle_execucao_universal_dry_run_inicial.json
  - config/telas/demo/h0050_controle_execucao_universal.json
```

## Resultados dos critérios

| Critério | Resultado | Registro factual |
|---|---|---|
| 1. Configuração com `dry_run` inicial | `DIVERGENTE` | Foram exibidos `[Espaço] Marcar` e `[Enter]`, em vez dos símbolos Unicode previstos. `[V] Verboso` e `[?] Ajuda` não apareceram. Espaço selecionou; o chip mudou de `Todos` para `Executar`, mas não houve marcador visual no item. `[Ins] Dry-Run` e sua cor estavam corretos. |
| 2. Abertura principal em `Executar` | `DIVERGENTE` | Os mesmos defeitos visuais ocorreram. A tela apresentou somente um item, impedindo selecionar os dois itens exigidos. |
| 3. Alternância por `Insert` | `CONFORME` | `Insert` alternou `[Ins]` entre `Dry-Run` e `Executar`, com mudança correspondente de cor. |
| 4. Resultado com `dry_run` e dois IDs | `NAO_EXECUTADO_BLOQUEADO` | Bloqueado pela existência de somente um item na tela principal. |
| 5. Retorno preservando `Dry-Run` | `NAO_EXECUTADO_BLOQUEADO` | Dependia do critério 4; não foi possível chegar ao resultado e ao retorno previstos. |
| 6. Nova abertura em `Executar` | `CONFORME` | Após sair e abrir novamente a configuração principal, o modo inicial retornou para `Executar`. |
| 7. Redimensionamento estreito e largo | `CONFORME_PARCIAL` | O conteúdo exibido permaneceu estável; isso não valida chips ausentes nem o marcador ausente. |

## Achados

### MV-H0050-01 — símbolos de teclado divergentes

Resultado: `aberto`. `[Espaço] Marcar` e `[Enter]` foram exibidos em vez dos
símbolos Unicode previstos, divergindo da apresentação esperada. Causa:
`NAO_CONFIRMADA`.

### MV-H0050-02 — chips Verboso e Ajuda ausentes

Resultado: `aberto`. `[V] Verboso` e `[?] Ajuda` não foram exibidos,
deixando incompleta a composição da barra nas duas telas demonstrativas.
Causa: `NAO_CONFIRMADA`.

### MV-H0050-03 — indicador visual de seleção ausente

Resultado: `aberto`. Espaço alterou a seleção e o chip mudou de `Todos` para
`Executar`, mas não apareceu marcador ou toggle visual no item. A seleção é
funcional, porém sem confirmação visual direta. Causa: `NAO_CONFIRMADA`.

### MV-H0050-04 — corpus demonstrativo insuficiente

Resultado: `aberto`. A configuração principal apresentou somente um item,
impedindo validar dois IDs, o resultado correspondente e a preservação do
modo após o retorno. Causa: `NAO_CONFIRMADA`.

## Conformidades preservadas e conclusão

Permaneceram conformes a alternância por `Insert`, a mudança de cor conforme
o modo, a reinicialização em `Executar` após nova abertura, a estabilidade do
conteúdo durante o redimensionamento e a seleção funcional por Espaço.

Os critérios 4 e 5 ficaram bloqueados pela tela com um único item. Há
divergências concretas e critérios obrigatórios não executados; portanto, a
validação não é aprovada parcialmente nem é inconclusiva.

```yaml
status: MANUAL_VALIDATION_FAILED
proxima_acao: PATCH_IMPLEMENTACAO
```
