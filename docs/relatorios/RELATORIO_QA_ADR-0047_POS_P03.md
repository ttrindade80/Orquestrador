# RELATORIO QA ADR-0047 POS P03

## Rastreabilidade

```yaml
etapa: QA_POS_PATCH_ADR
objeto: ADR-0047
patch_auditado: P03
cadeia_raiz: docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_ADR-0047_P03.md
```

## Status

`ADR_APPROVED_WITH_NOTES`

## Auditoria

A causa original — impossibilidade de expressar o `sufixo: ")"` no
`formato.dois_niveis_por_foco.filho.designador` estrutural — foi resolvida.
P03 fecha o objeto com `tipo` obrigatório e somente `prefixo` e `sufixo`
opcionais, ambos string; ausência equivale a vazio para tipos visuais. Os
tipos válidos são exatamente `decimal_composto`, `alfabetico_maiusculo` e
`nenhum`. Chaves desconhecidas são inválidas; `tipo: nenhum` exige prefixo e
sufixo ausentes e não produz designador visual. Para tipos visuais, o
resultado é `prefixo + designador_base + sufixo`.

H-0055 fica deterministicamente especificada como
`alfabetico_maiusculo` com `sufixo: ")"`, tabulação 5..10 e apresentação
`texto`, produzindo `A)`, `B)`, `C)`, `D)`. O conteúdo externo permanece
inalterado. Não há herança automática, `fonte`, `herdar` ou parsing do
conteúdo: a configuração estrutural é autoridade de COMO apresentar.

H-0063 permanece semanticamente intacta: `preset`, `amostra`, `titulo`
preservado, tabela de duas colunas, `tipo: nenhum` sem prefixo/sufixo,
tabulação 5..10 e espaçamento 3..8.

O conceito canônico verificado em `tela/renderizacao/designadores.py`
aplica prefixo/sufixo ao designador-base e preserva a lógica de
`decimal_composto`. P03 não reabre tabulação, texto/tabela, colunas,
espaçamento, alinhamento, quebra, resize, item lógico, navegação ou seleção.

As regras de validação e a localização/cardinalidade do schema são
suficientemente fechadas para APLICAR_ADR sem decisão material nova. O
`contrato_tela_json.md` ainda registra o schema anterior somente-tipo; o
delta futuro é propagar `prefixo`/`sufixo` e suas regras, sem decisão nova.
Isso não é defeito do P03. Não há achados materiais nem decisão documental
pendente.

## Verificações

`git diff --check -- docs/relatorios/RELATORIO_QA_ADR-0047_POS_P03.md`
passou sem apontamentos. A execução criou somente este relatório; alterações
anteriores do worktree foram preservadas.
\n