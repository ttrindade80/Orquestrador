# Relatório de patch documental — H-0055 P01

```yaml
patch: P01
resultado: HANDOFF_PATCH_APPLIED
raiz: docs/handoff/H-0055-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0055.md
status_anterior: H2_HANDOFF_PATCH_REQUIRED
```

## Achados tratados

### QA-H0055-001 — estado inicial obrigatório

O handoff deixou de aparentar liberação para implementação e passou a registrar
o bloqueio documental objetivo: D-MULTI-09 e §22.16 exigem exatamente um filho
por pai, mas as autoridades lidas não determinam qual filho inicial nem um
mecanismo vigente de materialização. Foram removidas a condicionalidade e
qualquer autorização para primeiro item, índice, fallback, default, campo,
schema ou política novos.

Status: PENDENTE/BLOQUEADO por decisão ausente nas autoridades vigentes.

### QA-H0055-002 — despacho contextual de Esc

O despacho foi fechado nos dois níveis: Esc no nível dos filhos retorna aos
pais preservando escolhas; Esc no nível dos pais usa somente o retorno/saída
existente de §23.4, também preservando escolhas. A declaração compatível
`politica_selecao: multipla` não encaminha esta escolha distinta ao ramo
genérico de limpeza. Nenhum cancelamento, Enter ou ação nova foi introduzido.

Status: RESOLVIDO documentalmente.

### QA-H0055-003 — `politica_selecao`

A especificação nominal da fixture estrutural passou a declarar
`politica_selecao: multipla`, exclusivamente para reutilizar `tg` e `[␣]`, sem
rebatizar ou ampliar D-MULTI-09.

Status: RESOLVIDO documentalmente.

### QA-H0055-004 — D23 e modos

A fixture foi fechada com a combinação válida
`formato.excesso.politica_modo: alternavel` e
`formato.excesso.modo_inicial: nao_verboso`; a alternância por `[V]` é
reversível. `modo normal` × `modo não verboso` e `hierarquia` foram preservados.

Status: RESOLVIDO documentalmente.

### QA-H0055-005 — paginação e conteúdo

A fixture foi fechada com `politica_paginacao: com`, cinco pais e quatro filhos
diretos por pai (25 itens lógicos), sem terceiro nível. O handoff exige duas
páginas demonstráveis, `PageDown`, `PageUp` e `[PgUp][PgDn] Páginas`, sem
paginação concorrente ou tamanho de página novo.

Status: RESOLVIDO documentalmente.

## Verificações focais e bloqueios

- O handoff alterado contém as cinco correções e mantém os caminhos,
  proibições, autoridades e arquivos preservados fora do patch.
- O relatório é novo; nenhum relatório anterior foi sobrescrito.
- Não foi executado QA, código, implementação, alteração de fixture existente
  ou commit.
- Bloqueio pendente único: materialização do filho inicial obrigatório, conforme
  QA-H0055-001; não há decisão implícita aplicada.
