# Relatório QA pós-patch — ADR-0008 / ITEM-0015 / P02

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P02.md

bloqueio_retestado:
  - schema_local_do_cabecalho_insuficientemente_determinado
```

## Resultado

O bloqueio foi resolvido. O contrato determina `cabecalho` como objeto fechado
com exatamente os campos diretos obrigatórios `titulo`, `descricao` e
`apresentacao`; os dois primeiros permanecem strings. `apresentacao` contém,
obrigatoriamente e sem extensão, os subobjetos `titulo` e `descricao`, cada um
com exatamente seus quatro parâmetros declarativos locais.

Tipos, domínios, enumerações, limites, semântica, obrigatoriedade e critérios
de erro estão determinados em `contrato_cabecalho.md`. O contrato também
proíbe campos desconhecidos, aliases, fallback, valores implícitos e fontes
globais alternativas, preservando a fronteira com `config/estilo.json`.

## Verificações e achados

Foram lidos integralmente a ADR, o contrato do cabeçalho, o módulo de
nomenclatura e o relatório P02. A busca focal autorizada no contrato de
console não encontrou afirmação incompatível. O JSON legado foi conferido
somente quanto aos oito nomes, à separação lógica e aos valores baseline; não
foi usado como autoridade. O diff exigido, as buscas autorizadas e
`git diff --check` não revelaram defeito material nem alteração fora do
escopo documental do P02.

Há uma correção factual pontual pendente no relatório P02: `execucao.status:
APLICADO` deve ser alinhado ao literal terminal canônico
`PATCH_APLICACAO_ADR_COMPLETED`. Esse achado não reduz a suficiência do schema.

```yaml
status: ADR_APPLICATION_APPROVED_WITH_NOTES
bloqueio_resolvido: true
handoff_h0049: possivel_apos_correcao_factual_pontual_do_relatorio_p02
```
