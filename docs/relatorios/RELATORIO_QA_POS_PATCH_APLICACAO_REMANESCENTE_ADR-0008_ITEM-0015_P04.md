# Relatório de QA pós-patch — ADR-0008 / ITEM-0015 / P04

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P04.md
bloqueio_retestado:
  - QPP03-04
```

## Resultado

`QPP03-04` está resolvido. O contrato fixa inequivocamente `c.isalpha()` —
semântica de `str.isalpha()` do Python — como único critério alfabético e
`c.upper()` como transformação exata. A regra é independente de locale, veda
normalização Unicode prévia e incorpora integralmente expansões de `upper()`.
O algoritmo preserva prefixo e sufixo, transforma somente o primeiro caractere
alfabético, encerra a busca, mantém frases posteriores e trata texto sem
caractere alfabético e string vazia.

Os exemplos normativos exigidos são compatíveis, inclusive `ßeta` → `SSeta`,
confirmado no Python 3.14.6. A nomenclatura registra `isalpha()`, `upper()` e
as restrições de locale/normalização, remetendo algoritmo, ordem e exemplos ao
contrato, sem autoridade concorrente. A ordem corte por `max_caracteres`,
capitalização, alinhamento/recuo e limitação geométrica, bem como o domínio
inteiro inclusivo de `1` a `200`, permanece preservada.

## Verificações e escopo

Foram executadas as leituras integrais do contrato, nomenclatura e relatório
P04; as buscas focais do P03 e H-0049; o `rg` normativo; o laço Python
independente; o diff obrigatório; e `git diff --check` nos três caminhos.
As buscas por alternativas ASCII, lista manual e locale só encontram
negações. O relatório P04 corresponde aos arquivos, decisão, exemplos,
verificações e ausência de bloqueios declarados. O diff do escopo mostra apenas
os dois documentos alterados; este relatório é o único arquivo criado pelo QA.
H-0049 não foi alterado e está liberado para o patch posterior.

```yaml
novos_achados: []
status: ADR_APPLICATION_APPROVED
patch_h0049_liberado: true
proxima_acao: PATCH_HANDOFF
```
