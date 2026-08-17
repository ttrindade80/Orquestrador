---
name: relatorio-aplicacao-adr-0048
description: Relatório da aplicação documental da ADR-0048 (persistência da escolha de filho por pai) aos contratos e módulos de nomenclatura afetados
metadata:
  type: relatorio
  scope: orquestrador
  item: ITEM-0026
  adr: ADR-0048
---

# Relatório — Aplicação da ADR-0048

## ADR aplicada

`docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` (D-0026-01 a
D-0026-11, patch `P01` aprovado, achado QA-ADR0048-001 resolvido). Status
interno atualizado de `ADR_CREATED` para `ADR_APPLIED`; nenhuma decisão foi
reaberta ou alterada.

## Arquivos efetivamente alterados

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` — status e
  parágrafo introdutório atualizados para refletir QA aprovado e aplicação
  concluída.
- `docs/adr/INDICE_ADR.md` — nova linha ADR-0048 (`aceita e aplicada`).
- `docs/backlog.md` — `ITEM-0026` reconciliado: pré-requisitos e próxima
  ação atualizados; status `planejado` → `pronto_para_handoff`; descrição
  preservada (capacidade ainda não implementada).
- `docs/contratos/contrato_console.md` — nova seção 26: ciclo comportamental
  completo (baseline, candidato, `Aplicar`/divergência, pop-up genérico,
  persistência delegada, sucesso, `ABORTADO`, fail-closed, restauração).
- `docs/contratos/contrato_json_console.md` — nova seção 16: autoridade
  persistida no documento externo, exclusividade, posição do primeiro filho
  não é autoridade, distinção estrutura×escolha, origem da baseline, e
  fronteira de schema literal não fechado.
- `docs/nomenclatura/32_CONSOLE.md` — nova subseção 4.12 (baseline/candidato
  da escolha de filho por pai); termos, distinção e remissão de ADR.
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` — nova subseção 4.7
  (escolha ativa persistida); termo, distinção e remissões.
- `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` — nova
  subseção 4.6 (restauração × persistência); termo, distinção e remissões.
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0048.md` — este relatório.

`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` não foi alterado:
a ADR não produz distinção nova pertencente estritamente a este módulo — a
autoridade do documento externo já é de competência do módulo `42`, e a
regra de que `tela.json` não guarda estado vivo já está registrada sem
delta material.

## Contratos reconciliados

`contrato_console.md` (§26) e `contrato_json_console.md` (§16), conforme
listado acima.

## Backlog/índice alterados

`docs/backlog.md` (`ITEM-0026`) e `docs/adr/INDICE_ADR.md`, conforme listado
acima.

## Decisões não inventadas por falta de literal executivo

Nenhum nome de campo, enum, versão de schema ou formato físico foi criado
para representar a escolha ativa persistida no documento externo
(`contrato_json_console.md` §16.7). A obrigação semântica foi registrada sem
chave presumida. Necessidade executiva posterior: a etapa de handoff deverá
fechar esse nome literal antes de qualquer implementação, junto de nome de
script/função, caminho, assinatura e mecanismo de escrita atômica
(D-0026-06, D-0026-09 — também não fechados).

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    - docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
  termos_adicionados:
    - "escolha ativa persistida (módulo 42)"
    - "baseline persistida da escolha de filho por pai (módulo 32)"
    - "candidato de runtime da escolha de filho por pai (módulo 32)"
    - "restauração da escolha ativa por pai (módulo 43)"
  termos_alterados: []
  distincoes_adicionadas:
    - "escolha ativa persistida × seleção exclusiva obrigatória de filho por pai (módulo 42)"
    - "baseline persistida × candidato de runtime (módulo 32)"
    - "carregamento (inclui restauração) × persistência (módulo 43)"
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

## Verificações

`git diff --check` executado sobre os nove arquivos autorizados; sem
conflitos de espaço em branco. Existência do relatório confirmada por
escrita bem-sucedida deste arquivo.

## Bloqueios

Nenhum.
