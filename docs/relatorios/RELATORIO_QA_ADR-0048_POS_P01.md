# Relatório de QA pós-patch — ADR-0048 P01

## Cadeia

- `cadeia.raiz`: ADR-0048.
- `cadeia.predecessor_imediato`: `RELATORIO_PATCH_ADR-0048_P01.md`.

## Achado retestado

- `QA-ADR0048-001`: resolvido.

## Verificações focais

- A busca autorizada na ADR-0048 não encontrou `seleção única` nem `selecao unica`; encontrou apenas a formulação corrigida `escolha ativa exclusiva de filho por pai`.
- A formulação corrigida preserva a decisão de exatamente um filho ativo por pai, com escolha explícita, exclusiva, obrigatória e persistida no documento externo.
- Permanecem inalterados baseline, candidato, confirmação, persistência, `ABORTADO`, falha de persistência e restauração em nova execução.
- O patch é terminológico e não introduz decisão nova, arquitetura, schema ou fluxo.
- As fronteiras de `ITEM-0023` e `ITEM-0024` permanecem expressamente fora do escopo.

## Status atual

`ADR_APPROVED`
