# Relatório PATCH_ADR — ADR-0042

## Cadeia

- raiz: `docs/relatorios/RELATORIO_QA_ADR-0042.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_QA_ADR-0042.md`

## Achados tratados

- `QA-ADR-0042-01`
- `QA-ADR-0042-02`
- `QA-ADR-0042-03`

## Trechos materialmente corrigidos

- Removidas da ADR as referências à decomposição, quantidade ou sequência de handoffs como exigência do `ITEM-0007`, bem como a afirmação de que a ADR condicionaria o avanço para aplicação, handoff e implementação.
- Em §4.4, mantida a classificação como `falha focal` para declaração incompatível de `tabela` navegável, sem fixar momento, camada ou mecanismo de falha, e preservado o não fallback para `nivel_unico`.
- Em §4.7, registrada a precedência contextual de `Esc` no toroide de filhos de `dois_niveis_por_foco`: retorno aos pais, preservação da escolha exclusiva obrigatória, sem limpeza e sem cancelamento.

## Preservações relevantes

D-MULTI-01 a D-MULTI-11 permanecem fechadas, com D-MULTI-11 mantendo apenas os critérios futuros de demonstração. Permanecem também a passividade de `tabela`, a escolha obrigatória de exatamente um filho por pai, a independência entre cursor e escolha, a subordinação à ADR-0041, as demais semânticas de `Esc` e os itens fora de escopo.

## Verificações executadas

- Leitura integral da ADR-0042 e do relatório de QA autorizado.
- Revisão do conteúdo corrigido restrita aos dois arquivos permitidos.
- `git diff --no-index --check` executado para cada arquivo permitido, sem apontamentos.
- Conferência semântica dos três achados e das preservações listadas acima.

## Bloqueios

nenhum
