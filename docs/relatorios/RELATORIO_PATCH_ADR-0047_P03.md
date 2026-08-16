# RELATÓRIO PATCH ADR-0047 P03

## Rastreabilidade

```yaml
etapa: PATCH_ADR
objeto: ADR-0047
patch: P03
causa: BLOCKED_DOCUMENTATION em PATCH_HANDOFF H-0073 P02
cadeia_raiz: docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0073_P02.md
```

## Limitação encontrada

H-0073 P02 comprovou que, com `formato.dois_niveis_por_foco.filho`
presente, o schema estrutural exigia `designador`, mas aceitava somente
`tipo`. O renderer formatado usava essa configuração e não incorporava o
`sufixo` do designador no documento de conteúdo. Assim, a capacidade H-0072
produzia `A`, embora a forma semanticamente fechada pela ADR-0047 fosse
`A)`.

## Causa e correção documental

A causa era a especificação insuficiente do objeto estrutural em §4.13,
incompatível com §4.4 e D-DNF-03. P03 fecha `designador` como objeto com
`tipo` obrigatório e somente `prefixo` e `sufixo` opcionais, ambos strings;
ausência equivale a string vazia. Os tipos válidos permanecem
`decimal_composto`, `alfabetico_maiusculo` e `nenhum`. Para tipos visuais, o
resultado é `prefixo + designador_base_do_tipo + sufixo`; `decimal_composto`
não teve sua lógica redefinida. Para `nenhum`, não há designador visual e
`prefixo`/`sufixo` devem estar ausentes. Chaves desconhecidas e tipos fora do
conjunto são inválidos.

Foi registrada a especialização futura de H-0055 com `tipo:
alfabetico_maiusculo`, `sufixo: ")"`, tabulação 5..10 e apresentação texto,
produzindo `A)`, `B)`, `C)`, `D)`. O documento externo de conteúdo permanece
inalterado. H-0063 permanece com `tipo: nenhum`, sem prefixo ou sufixo, e
todo o restante de sua especialização permanece intocado. Não foi criada
herança automática, campo `fonte`, campo `herdar`, parsing externo ou nova
política de navegação. A configuração estrutural continua autoridade de
como apresentar; conteúdo continua dados.

## Trechos corrigidos

Foram ajustados somente a decisão D-DNF-03, §4.4, §4.11 (H-0063), a nova
especialização registrada em §4.11.2 (H-0055), §4.13, §6 e os critérios
relacionados de §10. O texto de compatibilidade declara P03 como extensão
compatível do schema fechado em P01/P02 e preserva política, tabulação,
apresentação, tabela, colunas, espaçamento, alinhamento, quebra, resize,
item lógico, seleção e navegação.

## Verificações e bloqueios

- `git diff --check --` foi executado somente sobre a ADR e este relatório.
- A lista de estado confirmou que nenhum outro arquivo foi alterado por
  esta execução; alterações preexistentes foram preservadas.
- Não houve aplicação da ADR, QA pós-P03, alteração de contratos, handoffs,
  código, configuração ou testes.

Bloqueios: nenhum novo. `QA_POS_PATCH_ADR` permanece pendente e H-0072/H-0073
não foram corrigidos nesta etapa.
\n