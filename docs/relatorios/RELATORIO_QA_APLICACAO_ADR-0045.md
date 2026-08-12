# Relatório de QA da aplicação — ADR-0045

```yaml
etapa: QA_APLICACAO_ADR
item: ITEM-0028
adr: docs/adr/ADR-0045-resize-responsivo-formacoes-popup-marcacao.md
status: ADR_APPLICATION_REJECTED
```

## Resultado

O contrato substituiu efetivamente a regra do menor número de colunas pela
maximização das colunas fisicamente ocupadas, exigiu pelo menos duas linhas na
matriz e manteve `linha` como formação distinta. Também materializou o vão de
`2` espaços no encaixe e na representação, largura integral, overhead real,
recomposição por par de dimensões válido, reversibilidade, preservação de
estado, navegação toroidal e aplicação a `marcacao: exclusiva` e
`marcacao: multipla`. O módulo `35_POPUP.md` permanece um resumo terminológico
compatível e o pop-up continua distinto de `console`. O `ITEM-0028` permanece
`em_andamento`; `docs/INDICE.md` e a ADR não foram alterados.

## Achados materiais

### QA-0045-001 — Alteração fora da autorização de escrita

- **Requisito violado:** o manifesto de APLICAR_ADR autorizava escrita apenas
  nos arquivos listados e exigia leitura, não escrita, de
  `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`.
- **Evidência focal:** o diff altera o módulo `21` ao incluir uma exceção de
  formação do pop-up em sua regra geral de redimensionamento e uma relação com
  a ADR-0045. O relatório de aplicação também o declara alterado.
- **Impacto:** a alteração é material e não autorizada; correção semântica não
  elimina a violação de autoridade documental.
- **Correção necessária:** reverter as alterações do módulo `21`. Qualquer
  regularização posterior exige autorização própria, inexistente neste escopo.

### QA-0045-002 — `delta_terminologico` factualmente vazio

- **Requisito violado:** o relatório deve registrar módulos de nomenclatura
  efetivamente alterados e as categorias aplicáveis do delta.
- **Evidência focal:** o diff altera materialmente `docs/nomenclatura/35_POPUP.md`
  e `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`, enquanto o
  relatório declara `modulos_alterados: []` e todas as demais categorias vazias.
- **Impacto:** a evidência de aplicação não corresponde aos artefatos
  efetivamente modificados, prejudicando a rastreabilidade.
- **Correção necessária:** corrigir o `delta_terminologico` para refletir ao
  menos o módulo `35` e, se o módulo `21` não for revertido sob autoridade
  válida, também esse módulo e as categorias aplicáveis.

Os demais arquivos alterados pertencem ao escopo autorizado e não foi
identificada regra concorrente ou expansão material para as fronteiras fora da
ADR. A aplicação, porém, não pode ser aprovada enquanto os dois achados
permanecerem.
