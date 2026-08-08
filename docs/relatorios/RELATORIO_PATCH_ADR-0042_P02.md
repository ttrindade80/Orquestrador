---
status: PATCH_ADR_CONCLUIDO
adr: ADR-0042
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0042.md
  predecessor_imediato: docs/relatorios/RELATORIO_APLICACAO_ADR-0042.md
---

# Relatório do patch da ADR-0042 — P02

## Decisões incorporadas

- D-MULTI-12: `politica_navegacao` permanece objeto; `tipo` é o
  discriminador canônico, com os cinco valores fechados, e não há segunda
  forma de declaração.
- D-MULTI-13: a ausência de `politica_navegacao.tipo` equivale a
  `nivel_unico`, não invalida a configuração por si só e serve apenas como
  fallback de compatibilidade. Não há inferência por dados, apresentação,
  nome de fixture ou outro atributo.

## Trechos materialmente alterados

- Metadados e rastreabilidade passaram a registrar D-MULTI-01 a D-MULTI-13.
- A seção de decisão declarativa passou a definir o objeto, o campo `tipo`,
  os cinco valores fechados e o fallback de compatibilidade.
- A seção de compatibilidade e os critérios de aplicação passaram a registrar
  a preservação da semântica vigente de `navegavel` e a ausência de segunda
  forma de declaração.

## Preservações relevantes

Foram preservadas materialmente D-MULTI-01 a D-MULTI-11, o comportamento
vigente de `nivel_unico`, as incompatibilidades já fechadas para `tabela`, a
semântica das demais políticas, a precedência de Esc em
`dois_niveis_por_foco`, a subordinação à ADR-0041 e a vedação de antecipar
Enter, execução, persistência, `Pai: filho_ativo` ou geometria.

## Verificações

- A ADR mantém `politica_navegacao` como objeto e chama o discriminador
  exatamente de `tipo`.
- Os cinco valores e o fallback para `nivel_unico` estão registrados.
- Não foi redefinido `navegavel`, nem criada matriz adicional entre
  `navegavel` e `tipo`.
- A ADR e este relatório existem; `git diff --check` foi executado sem
  apontar erros nos arquivos alterados.

## Bloqueios

Nenhum. O bloqueio histórico da aplicação não foi convertido em estado atual
da ADR.
