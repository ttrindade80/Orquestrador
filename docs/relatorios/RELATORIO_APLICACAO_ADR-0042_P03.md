# Relatório de aplicação — ADR-0042 P03

## Arquivos alterados

- `docs/contratos/contrato_console.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` (metadado de aplicação)
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0042_P03.md`

## Delta material

Aplicada a semântica `D-MULTI-06-P03` na seção vigente de
`selecao_multinivel`: qualquer item selecionável, em profundidade arbitrária,
possui estado binário e `tg`; item não selecionável não possui estado, não
recebe `tg` e é excluído da unanimidade. O estado do pai é derivado da
unanimidade dos filhos selecionáveis imediatos, sem estado parcial,
indeterminado, contador ou terceiro símbolo. Toggles manuais reconciliam pais
e ancestrais de baixo para cima; Espaço em pai mantém a propagação descendente
e, depois, a reconciliação ascendente. Os critérios de fixture demonstrativa
foram preservados como exigência futura, sem criação de fixture.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/32_CONSOLE.md
  termos_adicionados: []
  termos_alterados:
    - selecao_multinivel
  distincoes_adicionadas:
    - estado de seleção do pai é binário e derivado da unanimidade dos filhos selecionáveis imediatos
    - item não selecionável não participa da unanimidade
  fronteiras_alteradas:
    - nenhuma
  dependencias_condicionais_adicionadas: []
```

## Verificações

- Confirmados `tg` em qualquer item selecionável e ausência de estado/`tg` em item não selecionável.
- Confirmada a derivação binária do pai pela unanimidade dos filhos selecionáveis imediatos.
- Confirmadas reconciliações ascendentes após seleção manual e desseleção.
- Confirmadas propagação descendente por Espaço e reconciliação de baixo para cima.
- Confirmadas ausência de estado parcial e profundidade arbitrária.
- Confirmada preservação de árvore, paginação, cursor, foco, Enter e barra.
- Conferido o diff apenas dos arquivos autorizados; relatório materializado.

## Bloqueios

nenhum
