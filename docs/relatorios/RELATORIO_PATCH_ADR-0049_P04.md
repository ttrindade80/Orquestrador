# Relatório do patch P04 — ADR-0049

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_CRIACAO_ADR-0049.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0049_POS_P03.md

achados_tratados:
  - QA-ADR-0049-01
```

## Regra removida

Foi removida da D-0027-10 a obrigação normativa específica de que a última
linha do parágrafo não fosse artificialmente expandida para preencher a
largura.

## Confirmação

Nenhuma política substituta foi criada. A ADR permanece neutra quanto a
justificar, expandir, distribuir ou adotar qualquer outra política específica
para a última linha.

## D-0027-10 preservadas

Permanecem inequívocos: o parágrafo completo como unidade lógica multilinear;
recomposição a partir do texto lógico completo após resize; palavras
indivisíveis, sem divisão, hifenização ou separação silábica automáticas;
formação com palavras inteiras; justificação somente após a formação das
linhas; expansão nos vãos entre palavras das linhas aplicáveis; neutralidade
quanto a whitespace/separadores arbitrários; e não uso de linhas físicas
anteriores como entrada lógica.

## Verificações

- Busca focal na ADR: não permaneceu política normativa específica de última
  linha.
- `git diff --check` executado para a ADR e este relatório.

## Bloqueios

Nenhum.
