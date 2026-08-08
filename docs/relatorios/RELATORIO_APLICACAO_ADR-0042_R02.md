# Relatório de aplicação documental — ADR-0042 R02

## Status

```yaml
status: ADR_APPLIED
adr: ADR-0042
qa_da_adr: ADR_APPROVED
qa_da_aplicacao: PENDENTE
```

A aplicação R02 foi executada após a resolução de D-MULTI-12 e D-MULTI-13.
A primeira execução ficou bloqueada porque a forma declarativa do schema não
havia sido determinada pela autoridade. O relatório histórico dessa execução
foi preservado e não foi sobrescrito.

## Arquivos efetivamente alterados

- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`
- `docs/adr/INDICE_ADR.md`
- `docs/backlog.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0042_R02.md`

## Propagação material

D-MULTI-01 a D-MULTI-13 foram propagadas sem decisão nova. Os contratos
registram as cinco políticas, as regras transversais, a distinção entre foco,
cursor e seleção, a seleção recursiva multinível, os dois toroides de
`dois_niveis_por_foco`, a escolha exclusiva obrigatória de filho por pai e a
precedência contextual de `Esc`. A declaração permanece como objeto, com
`tipo` e cinco valores fechados; a ausência resolve para `nivel_unico`.
A paginação multinível permanece subordinada integralmente à ADR-0041.

O índice registra ADR-0042 como aceita, com aplicação concluída, QA da
aplicação pendente e implementação não iniciada. O ITEM-0007 foi mantido como
trabalho planejado, com próxima ação `QA_APLICACAO_ADR`.

## Preservações e verificações

O contrato de chip foi preservado porque a leitura focal não demonstrou
contradição material com `[✥]`. A aplicação não criou código, testes,
fixtures, geometria, apresentação, Enter, execução, confirmação,
cancelamento, persistência ou handoff. A verificação de integridade textual
obrigatória foi executada com `git diff --check` nos arquivos alterados; a
validação independente da aplicação permanece pendente. O relatório bloqueado
anterior permaneceu sem alteração.

## Bloqueios

Nenhum bloqueio material para a aplicação documental. QA da aplicação ainda
não foi executado.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  termos_adicionados:
    - política de navegação declarada
    - politica_navegacao.tipo
    - nivel_unico
    - tabela como política de navegação
    - arvore_colapsavel
    - selecao_multinivel
    - dois_niveis_por_foco
    - seleção exclusiva obrigatória de filho por pai
  termos_alterados:
    - navegação multinível passa a referenciar ADR-0042
  distincoes_adicionadas:
    - tabela como política versus tabela como apresentação
    - seleção única versus seleção exclusiva obrigatória de filho por pai
    - cursor versus escolha do filho
    - navegação versus paginação
  fronteiras_alteradas:
    - apresentação multinível permanece no módulo 44 e navegação multinível referencia ADR-0042
    - Esc contextual em dois_niveis_por_foco precede a limpeza geral da seleção
  dependencias_condicionais_adicionadas:
    - ausência de politica_navegacao.tipo resolve para nivel_unico
    - paginação multinível consome exclusivamente a ADR-0041
```
