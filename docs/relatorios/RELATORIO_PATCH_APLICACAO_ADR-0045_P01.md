# Relatório de patch de aplicação — ADR-0045

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0045.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0045.md

achados_tratados:
  - QA-0045-001
  - QA-0045-002
```

## Reversão focal

Foi revertido exclusivamente o delta da aplicação da ADR-0045 em
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`. O arquivo não
apresenta mais delta correspondente à ADR-0045.

Nenhum outro arquivo normativo foi alterado por este patch. A aplicação
aprovada permanece em `docs/nomenclatura/35_POPUP.md` e
`docs/contratos/contrato_popup.md`; `docs/backlog.md` permanece sem correção.

## Estado final dos achados

- `QA-0045-001`: tratado pela reversão focal do módulo 21.
- `QA-0045-002`: tratado pelo registro do delta terminológico material
  remanescente no módulo 35.

`ITEM-0028` permanece `em_andamento`.

## Verificações focais executadas

- `git diff -- docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`:
  sem delta após a reversão.
- `git diff --check`.
- Diff focal de módulo 21, módulo 35, contrato e backlog: confirmação da
  preservação dos deltas autorizados; existência deste relatório confirmada no
  caminho nominal.

## Delta terminológico corrigido

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/35_POPUP.md
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```
