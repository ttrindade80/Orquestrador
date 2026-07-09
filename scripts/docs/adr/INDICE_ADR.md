---
name: indice-adr
description: Modelo de indice para Architecture Decision Records
metadata:
  type: indice
  scope: scripts
---

# Indice — ADRs

## Regra

ADR registra uma decisao arquitetural aprovada ou rejeitada. Uma ADR aceita nao
deve ser editada para mudar decisao; se a decisao mudar, criar nova ADR que
substitui a anterior.

Este indice registra as ADRs aceitas do projeto.

## Como criar ADR

1. Copiar `docs/templates/TEMPLATE_ADR.md`.
2. Nomear como `ADR-NNNN-descricao-curta.md`.
3. Preencher contexto, decisao, consequencias e contratos afetados.
4. Atualizar este indice.
5. Atualizar os contratos afetados antes de gerar handoffs dependentes.

## Decisoes registradas

| ID | Titulo | Status | Data |
|---|---|---|---|
| ADR-0001 | `menu` suporta modo matriz (múltiplas colunas) | aceita | 2026-07-05 |
| ADR-0002 | `menu` usa sobra à direita | aceita | 2026-07-05 |
| ADR-0003 | Vãos elásticos do `menu` | aceita | 2026-07-05 |
| ADR-0004 | `cor_inativo` e `cor_alerta` no schema de estilo | aceita | 2026-07-05 |
| ADR-0005 | lancador não é corpo navegável por [✥] | aceita | 2026-07-06 |
| ADR-0006 | renomeação `dado` para `console` e `Info` para `dashboard` | aceita | 2026-07-06 |
| ADR-0007 | tela de processamento é composição de tipos existentes | aceita | 2026-07-06 |
| ADR-0008 | modelo de configuração por tela | aceita | 2026-07-07 |
| ADR-0009 | caminho, nomenclatura e formato dos JSONs de tela | aceita | 2026-07-07 |
| ADR-0010 | composição hierárquica do corpo e dashboard como elemento funcional | aceita | 2026-07-08 |
| ADR-0011 | terminologia de arranjo: `vertical`/`horizontal` (aliases transicionais `sobreposto`/`lado_a_lado`) | aceita | 2026-07-08 |
| ADR-0012 | `barra_de_menus` declarativa por tela | aceita | 2026-07-08 |
| ADR-0013 | ocupação vertical da janela do terminal pelo corpo (`ocupacao_vertical_terminal`) — distinta de `corpo.arranjo` | aceita | 2026-07-09 |
| ADR-0014 | distribuição horizontal **responsiva** da `barra_de_menus` (`distribuicao = "horizontal"` como alias transitório de `modo = "horizontal_responsiva"`) + regra de alteração por termo específico completo | aceita | 2026-07-09 |

## Exemplo de linha

| ADR-0000 | Escolher formato de persistencia do modulo exemplo | aceita | YYYY-MM-DD |
