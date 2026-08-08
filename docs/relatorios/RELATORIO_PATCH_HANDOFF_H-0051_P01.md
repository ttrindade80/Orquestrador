---
name: RELATORIO_PATCH_HANDOFF_H-0051_P01
description: "Patch documental do handoff H-0051 para fechar os dois achados materiais do QA (H-0051-A e H-0051-B)"
metadata:
  type: relatorio_patch_handoff
  status: HANDOFF_PATCHED
  handoff: H-0051
  data_criacao: "2026-08-07"
---

# Relatório de patch — H-0051 (P01)

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0051.md
  predecessor_imediato: docs/handoff/H-0051-paginacao-universal-pageup-pagedown.md

achados_tratados:
  - H-0051-A
  - H-0051-B

delta_material:
  - fechamento da expansão de arquivos não enumerados
  - autorização focal do renderer para agrupamento visual dos controles
  - materialização fechada de [PgUp][PgDn] Páginas

verificacoes: []
bloqueios: []
```

## Achado H-0051-A

O §6.3 do handoff continha uma autorização aberta: se `pytest` revelasse
arquivo de teste não enumerado com dependência de `,`/`<`/`.`/`>` ou
`[<]`/`[>]`, sua correção era considerada automaticamente dentro do escopo
("regressão direta"). Essa cláusula foi removida e substituída pela regra
fechada: qualquer dependência material em arquivo não enumerado interrompe o
trabalho antes de leitura ou alteração, com retorno de
`LEITURA_ADICIONAL_NECESSARIA` (caminho, alvo, motivo e impacto sem a
expansão). Nenhum arquivo não enumerado pode ser alterado automaticamente.

Foi encontrada e reconciliada uma contradição residual em §9 (relatório da
execução), que ainda previa registrar "arquivo de teste adicional corrigido
além dos listados em §6.3" — texto incompatível com a regra fechada. A
frase foi substituída por registro de eventual bloqueio por
`LEITURA_ADICIONAL_NECESSARIA`.

## Achado H-0051-B

O handoff exigia a representação `[PgUp][PgDn] Páginas`, mas mantinha
`tela/renderizacao/barra_menus.py` como integralmente preservado e deixava
à decisão do implementador a forma concreta de alcançar o agrupamento
visual — decisão estrutural que o handoff não pode delegar.

Correções aplicadas:

- `tela/renderizacao/barra_menus.py` passa a constar em §6.1 como arquivo de
  implementação, com autorização estritamente focal (novo §6.1.1), limitada
  ao tratamento necessário para apresentar `chip_pagina_anterior` e
  `chip_pagina_proxima` como o agrupamento canônico, sem criar mecanismo
  genérico de agrupamento nem afetar distribuição, outros chips, regras de
  existência/ativo, cores, foco, paginação ou navegação;
- §6.4 deixa de listar `barra_menus.py` como integralmente preservado,
  preservando apenas a lógica não relacionada ao agrupamento focal;
- §6.2 fixa os valores concretos das 11 fixtures, sem escolha material
  remanescente: `chip_pagina_anterior` com `"tecla": "PgUp"` e
  `"texto": ""`; `chip_pagina_proxima` com `"tecla": "PgDn"` e
  `"texto": "Páginas"` — produzindo, combinados ao tratamento focal do
  renderer, a sequência contígua `[PgUp][PgDn] Páginas`, sem separador
  entre `[PgUp]` e `[PgDn]`, com `Páginas` uma única vez após `[PgDn]`;
  os dois chips continuam declarados separadamente nas fixtures;
- §7 (testes obrigatórios) passa a exigir explicitamente os critérios 7.1 a
  7.6: existência lógica independente, estado ativo/inativo independente,
  representação visual literal e contígua, ausência de separador,
  `Páginas` uma única vez, e ausência de efeito colateral nos demais chips.

## Verificações

- Nenhum arquivo não enumerado ficou autorizado implicitamente: §6.3 fecha a
  expansão e §9 foi reconciliado.
- `tela/renderizacao/barra_menus.py` está nominalmente autorizado em §6.1,
  com limites explícitos em §6.1.1.
- Os dois chips (`chip_pagina_anterior`, `chip_pagina_proxima`) permanecem
  logicamente independentes: `regra_existencia`, `regra_ativo`, cor e
  acionamento por `PageUp`/`PageDown` continuam distintos e preservados.
- A saída observável exigida é literalmente `[PgUp][PgDn] Páginas`,
  registrada em §6.2 e §7.
- Nenhuma decisão material de apresentação restou ao implementador: os
  valores de `tecla`/`texto` das fixtures e o limite da alteração do
  renderer estão fixados.
- Nenhuma capacidade de navegação multinível (`ITEM-0007`) entrou no
  escopo; as preservações de §4.2 e §10 permanecem intactas.

## Limite desta etapa

Nenhuma implementação, QA pós-patch, stage ou commit foi realizado. Somente
`docs/handoff/H-0051-paginacao-universal-pageup-pagedown.md` foi alterado;
este relatório foi criado.
