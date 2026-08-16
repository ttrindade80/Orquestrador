# Relatório de Revalidação Manual — H-0073 (pós H-0072 P05+P06)

```yaml
etapa: REGISTRAR_REVALIDACAO_MANUAL
objeto: H-0073 / capacidade consumida H-0072
executor_da_validacao: USUARIO
ambiente: TTY_REAL
status: MANUAL_REVALIDATION_APPROVED
predecessor_imediato:
  docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P05_P06.md
achados_encerrados:
  - VM-H0073-001
  - VM-H0073-002
proxima_acao: FECHAMENTO_H0072_H0073_ADR0047
```

## Resultado global

A revalidação manual TTY realizada pelo usuário passou integralmente:
`MANUAL_REVALIDATION_APPROVED`.

## H-0055 — VM-H0073-001

Comando executado:
`PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco`.

Durante o resize horizontal, a tabulação pai→filho variou, o comportamento
mínimo/máximo funcionou e `A)` permaneceu correto. Não foi observado erro
visual impeditivo.

```yaml
VM-H0073-001: RESOLVIDO_NA_REVALIDACAO_MANUAL
H0055_TABULACAO_DINAMICA: APROVADO
```

## H-0063 — VM-H0073-002

Comando executado: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py`.
Percurso: `F4`.

“Destaque Fundo” manteve o fundo contido no chip, sem vazamento para as
regiões superior ou inferior, outras linhas ou o restante da tela. A
tabulação dinâmica continuou funcionando normalmente.

```yaml
VM-H0073-002: RESOLVIDO_NA_REVALIDACAO_MANUAL
H0063_ESPACAMENTO_COLUNAS_3_8: PRESERVADO
H0063_TABULACAO_DINAMICA: APROVADO
```

## Estado dos achados e estado operacional

```yaml
achados_abertos: []
VM-H0073-001:
  estado: RESOLVIDO
VM-H0073-002:
  estado: RESOLVIDO
fechamento: PRONTO
proxima_acao: FECHAMENTO_H0072_H0073_ADR0047
```

Este relatório registra somente os fatos informados pelo usuário na
revalidação manual. Não realiza diagnóstico, QA ou fechamento.
\n