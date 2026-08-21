# Relatório QA pós-P04 — ADR-0049

```yaml
QA-ADR-0049-01: resolvido

integridade_D-0027-10:
  status: íntegra
  observacao: >-
    Permanecem o parágrafo completo como unidade lógica, recomposição pelo
    texto lógico após resize, palavras indivisíveis e inteiras, ausência de
    quebra, hifenização e separação silábica automáticas, formação das linhas
    antes da justificação, expansão nos vãos entre palavras das linhas
    aplicáveis e exclusão das linhas físicas anteriores como entrada lógica.
  ultima_linha: neutra, sem política específica

palavra_maior_que_largura: >-
  Somente a indivisibilidade para o compositor permanece decidida; clipping,
  overflow, scroll, erro, fallback, truncamento e expansão de container não
  foram escolhidos.

whitespace_separadores: >-
  Os vãos entre palavras podem receber expansão da justificação, sem política
  global para whitespace ou separadores arbitrários.

novo_achado: nenhum
status: ADR_APPROVED
```
