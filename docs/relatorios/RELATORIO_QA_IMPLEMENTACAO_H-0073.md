# RELATÓRIO — QA_IMPLEMENTACAO H-0073

```yaml
etapa: QA_IMPLEMENTACAO
objeto: H-0073
cadeia_raiz: docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md
status: I1_IMPLEMENTATION_APPROVED
```

## Escopo auditado

Foram auditados os dois JSON estruturais, `tela/estilo.py`, os testes
nominais alterados/criados e os fluxos reais por `demo/demo.py`. Git confirmou
os deltas acumulados de H-0072 separadamente; não houve alteração causal de
H-0073 em seus artefatos.

## H-0055

Configuração literal confirmada: tabulação 5..10, designador
`alfabetico_maiusculo` com `sufixo: ")"` e apresentação `texto`, preservando
`formato.excesso`. A demonstração real passou 5/5 e confirmou `A)`–`D)`,
proveniência estrutural do sufixo, tabulação, deslocamento unitário
`ec`/`tg`/designador/conteúdo, navegação e seleção. O conteúdo externo foi
byte-a-byte igual a `HEAD`; ordem, identidade, toroides e resize permaneceram
preservados.

## H-0063

Configuração literal confirmada: tabulação 5..10, designador `nenhum`, tabela
com exatamente `preset` e `amostra`, sem espaçamento fora de 3..8. A projeção
preserva `preset` e `titulo` e acrescenta `amostra` diretamente por
`amostra_de_preset`, sem parsing. Os 18 critérios comportamentais passaram,
incluindo tabela local sem cabeçalho/borda/título/designador, alinhamento
global, unidade deslocada, quebra/identidade lógica, resize, navegação,
seleção e preservação do ciclo candidato-baseline-aplicar-persistir-publicar.
A demonstração real passou 4/4.

## Preservações, testes e causalidade

`h0062_estilo.json`, conteúdo externo H-0055 e `tela/renderizacao/estilo.py`
permaneceram intocados. A regressão H-0072 passou, sem alteração de seus
artefatos: testes de capacidade e demonstração verdes.

Suíte focal nominal: `236 passed, 1 failed`. Suíte canônica: `1452 passed,
1 failed`. A única falha é H-0070:
`test_filhos_sem_ordinais_cursor_e_indicadores_preservados`, com `index("→")`
igual a 2. É `FALHA_HISTORICA_NAO_CAUSAL`: o teste chama diretamente
`_linhas_apresentacao_hierarquia_com_mapa`, não percorre
`formato_filho_dois_niveis`; a assertiva e esse caminho não foram alterados
por H-0073.

Achados materiais: nenhum. Bloqueios: nenhum. Prontidão para fechamento:
`PRONTO`.
\n