# Relatório de QA do handoff H-0075 — pós-P02

```yaml
cadeia:
  raiz: H-0075
  predecessor_imediato: RELATORIO_PATCH_HANDOFF_H-0075_P02.md
achados_retestados:
  QA-H0075-001: resolvido
  QA-H0075-002: resolvido
fail_closed_inconsistencia:
  classificacao: aprovado
  evidencia: >-
    O mapa agrupa por documento externo + pai.id, consolida valores iguais e
    levanta TelaEstruturaInvalida para valores divergentes. A disponibilidade
    retorna False e a solicitação retorna None; assim não há eleição, snapshot,
    popup, escrita ou alteração da baseline. A ordem dos consoles e lista_foco
    não possui autoridade.
propagacao:
  politica: >-
    Predicado cumulativo: mesmo modelo, mesmo objeto ConteudoExterno, tipo
    navegacao_efetivo igual a dois_niveis_por_foco e semântica ITEM-0026.
  pai: >-
    Exige o mesmo pai.id presente no destino; compartilhar ConteudoExterno
    isoladamente não habilita propagação.
  preservacao_estado: >-
    Sincroniza somente a escolha do pai alvo, preservando demais seleções e
    estado; não insere pai ausente nem toca política distinta. H-0072 permanece
    caso positivo, e os itens 37–46 cobrem os casos positivo e negativos.
novos_achados: []
status: H1_HANDOFF_APPROVED
```
