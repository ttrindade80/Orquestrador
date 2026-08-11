# Relatório de validação manual — H-0055

## Identificação

```yaml
tipo_execucao: VALIDACAO_MANUAL
objeto: H-0055
capacidade: dois_niveis_por_foco
status: MANUAL_VALIDATION_APPROVED
executor: USUARIO
ambiente: TTY_REAL
data: 2026-08-10
```

## Rastreabilidade

```yaml
cadeia:
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0055_P02.md

qa_predecessor:
  status: I5_MANUAL_VALIDATION_REQUIRED

achados_que_motivaram_revalidacao:
  - MV-H0055-001
  - MV-H0055-002
```

`MV-H0055-001` e `MV-H0055-002` já estavam conformes na evidência
automatizável do QA predecessor. Esta execução forneceu a confirmação TTY
restante, conforme resultado informado pelo usuário.

## Método

O usuário executou, na raiz do Orquestrador, o comando:

```zsh
PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco
```

A execução ocorreu em TTY real. O agente não executou nem observou a
demonstração.

## Resultados

Os seis critérios foram informados pelo usuário como `OK` e estão registrados
como aprovados:

| Critério | Registro factual | Resultado |
|---|---|---|
| `VM-H0055-001` | Estado inicial com chip `[Esc] Sair` e chip `[V]` ausente. | `APROVADO` |
| `VM-H0055-002` | Espaço sobre pai com filhos entra no nível de filhos, com foco no toroide de filhos e chip `[Esc] Voltar`. | `APROVADO` |
| `VM-H0055-003` | `Esc` no nível de filhos retorna ao pai e restaura o chip `[Esc] Sair`. | `APROVADO` |
| `VM-H0055-004` | Repetição do ciclo entrar nos filhos, confirmar Voltar, retornar aos pais e confirmar Sair sem rótulo obsoleto. | `APROVADO` |
| `VM-H0055-005` | Chip `[V]` ausente; a tecla `V` não alterna verbosidade nem produz mudança visual associada. | `APROVADO` |
| `VM-H0055-006` | `Esc` retorna ao pai no nível de filhos, sai no nível de pais, e `[Esc] Limpar` está ausente no modo. | `APROVADO` |

## Resultado consolidado

```yaml
resultado_global:
  status: MANUAL_VALIDATION_APPROVED
  criterios_aprovados: 6
  criterios_falhos: 0
  achados_pendentes: []
  validacao_TTY_H0055: APROVADA
```

## Limites da evidência

Esta validação comprova somente os seis critérios enumerados neste relatório.
Não atribui aprovação manual a comportamentos não exercitados, a outros modos
de console, à suíte automatizada, a aspectos internos do loader, nem a código
ou arquitetura não visualizados pelo usuário. A conformidade automatizável
pertence ao QA predecessor.

## Próxima ação

```yaml
proxima_acao: FECHAMENTO_H-0055
```
