# Relatório — Patch P01 da ADR-0048

## Cadeia raiz

- ADR: `ADR-0048` — Persistência da escolha de filho por pai (`ITEM-0026`).
- Predecessor imediato: achado `QA-ADR0048-001`, transportado integralmente
  no prompt de execução (QA `ADR_REJECTED`). O QA confirmou D-0026-01 a
  D-0026-11 como materialmente cobertas e não apontou outro defeito. Este
  patch preserva integralmente essas decisões.

## Achado tratado

`QA-ADR0048-001` — uso indevido de "seleção única" na ADR-0048 §2.2
(D-0026-02). A formulação `seleção única dentro de cada conjunto de filhos`
colidia com o termo canônico "seleção única" (item sob cursor, ADR-0031),
que é mecanismo distinto da escolha persistida de filho por pai.

## Trecho material corrigido

Em `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` §2.2
(D-0026-02 — Exclusividade persistida):

- Antes: `A estrutura persistida representa **seleção única dentro de cada
  conjunto de filhos**: para cada pai há exatamente um filho ativo.`
- Depois: `A estrutura persistida representa **escolha ativa exclusiva de
  filho por pai**: para cada pai há exatamente um filho ativo.`

A decisão material foi preservada sem alteração: exatamente um filho ativo
por pai, escolha explícita, exclusiva, obrigatória (implícita em "há
exatamente um filho ativo" — nenhum pai fica sem filho ativo) e persistida
no documento externo. Nenhuma arquitetura, schema, fluxo de persistência ou
tratamento de `CONFIRMADO`/`ABORTADO`/falha foi tocado.

## Verificação focal de resíduos

Comando executado (antes e depois do patch):

```
rg -n 'seleção única|selecao unica' docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md
```

- Antes do patch: uma única ocorrência, linha 93 (o próprio trecho do
  achado).
- Depois do patch: nenhuma ocorrência (código de saída 1).

Não havia outra ocorrência do termo na ADR-0048 usando-o para nomear a
escolha persistida de filho. A ocorrência de "seleção exclusiva obrigatória
de filho por pai" em §1.1 (linha 29) nomeia o mecanismo runtime já fechado
pela ADR-0042 (D-MULTI-09) e não usa o termo "seleção única" — não é
resíduo do achado e não foi alterada.

## Arquivos alterados

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` — correção
  terminológica pontual em §2.2.
- `docs/relatorios/RELATORIO_PATCH_ADR-0048_P01.md` — este relatório
  (criado).

Nenhum outro arquivo foi lido além do manifesto autorizado (ADR-0048,
ADR-0042, `contrato_console.md`) e nenhum outro arquivo foi alterado.

## `git diff --check`

```
git diff --check -- docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md docs/relatorios/RELATORIO_PATCH_ADR-0048_P01.md
```

Resultado: sem saída — nenhum problema de espaço em branco ou conflito
detectado.

## Bloqueios

Nenhum. A correção não exigiu alterar a decisão material de exatamente um
filho ativo por pai, e não houve conflito terminológico adicional não
resolvível pelas autoridades enumeradas.
