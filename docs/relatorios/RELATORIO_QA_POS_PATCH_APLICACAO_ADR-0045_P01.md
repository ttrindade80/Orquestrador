# Relatório de QA pós-patch de aplicação — ADR-0045 P01

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0045.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0045_P01.md

achados_retestados:
  - QA-0045-001
  - QA-0045-002
```

## Resultado dos achados

- `QA-0045-001`: resolvido. O módulo 21 não possui delta no estado real em
  relação ao baseline; a reversão preservou seu conteúdo preexistente e não há
  evidência de arquivo alternativo usado para contornar a restrição.
- `QA-0045-002`: resolvido. O módulo 35 permanece materialmente aplicado; o
  `delta_terminologico` do patch corresponde ao estado real: módulo listado e
  todas as categorias classificáveis vazias, sem preenchimento artificial.

## Verificações focais

- Leitura integral do relatório do patch, do módulo 21 e do módulo 35.
- Diff focal: módulo 21 sem delta; módulo 35 e `contrato_popup.md` mantêm a
  aplicação autorizada; `docs/backlog.md` mantém `ITEM-0028` como
  `em_andamento`.
- `contrato_popup.md` mantém coluna → matriz → linha, critérios de encaixe,
  resize reversível, preservação de estado, navegação toroidal e aplicação a
  `marcacao: exclusiva` e `marcacao: multipla`.
- `git diff --check`: conforme.
- Nenhum arquivo normativo além dos deltas de aplicação já existentes foi
  alterado pelo patch; não há novo achado material diretamente relacionado.
- Este relatório existe no caminho nominal.

## Status atual da aplicação

`ADR_APPLICATION_APPROVED`
