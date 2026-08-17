---
name: relatorio-qa-aplicacao-adr-0048
description: QA documental da aplicação da ADR-0048
metadata:
  type: relatorio
  scope: orquestrador
  item: ITEM-0026
  adr: ADR-0048
---

# Relatório — QA da aplicação da ADR-0048

## Status

`BLOCKED_DOCUMENTATION`

## Parecer

A aplicação registrou corretamente a ADR como `ADR_APPLIED`, incluiu a
ADR-0048 no índice e reconciliou os contratos e os módulos 32, 42 e 43. O
módulo 02 permanece conforme: não há delta novo de sua propriedade. O
contrato do console (§26) cobre baseline × candidato, cursor × escolha,
alteração sem gravação imediata, divergência, confirmação, responsabilidade
do chamador, sucesso, `ABORTADO`, fail-closed, restauração e a ausência de
persistência no renderer/pop-up. O contrato JSON (§16) cobre autoridade no
documento externo, exatamente um ativo por pai, estrutura × escolha, primeiro
filho sem autoridade e origem da baseline, sem chave inventada. A distinção
terminológica entre escolha persistida e seleção exclusiva de runtime é
válida e não duplica `seleção única`.

### Classificação das seis dimensões executivas

| Dimensão | Classificação |
|---|---|
| Nome literal do campo | Decisão/schema público indispensável antes de `CRIAR_HANDOFF` |
| Nome de script | Detalhe executivo, desde que preserve a autoridade aprovada |
| Nome de função | Detalhe executivo interno |
| Caminho do script | Detalhe de artefato executivo, resolvível conforme autoridades/repositório |
| Assinatura interna | Detalhe executivo interno |
| Escrita/atomicidade | Detalhe de implementação, condicionado ao fail-closed |

## Achados

### QA-APP-0048-001 — Literal de schema delegado indevidamente ao handoff

- **Requisito:** o handoff não pode escolher schema público; o documento
  externo deve ter uma representação executável e interoperável da escolha.
- **Evidência focal:** `contrato_json_console.md` §§16.1–16.2 exige declaração
  explícita e única; §16.7 declara aberto o nome literal, enum, versão e
  formato. O relatório de aplicação chama o nome literal de “necessidade
  executiva posterior” a ser fechada no handoff.
- **Impacto:** produtor e consumidor não têm chave pública para interoperar.
  Criá-la no handoff seria uma decisão de schema que essa etapa não pode
  tomar. `pronto_para_handoff` não é factual enquanto essa decisão faltar.
- **Correção necessária:** a autoridade competente deve decidir e aprovar o
  nome literal do campo no documento externo (e a representação pública
  necessária), reconciliando o contrato antes de `CRIAR_HANDOFF`. Nenhuma
  alternativa é escolhida neste QA.

### QA-APP-0048-002 — Backlog avança apesar do bloqueio de schema

- **Requisito:** `ITEM-0026` só pode estar pronto para handoff quando não
  houver decisão indispensável pendente.
- **Evidência focal:** `docs/backlog.md` marca `pronto_para_handoff`, mas a
  próxima ação admite que o nome literal permanece pendente “para essa
  etapa”; o relatório de aplicação registra “Bloqueios: Nenhum”.
- **Impacto:** o estado permite iniciar um handoff que teria de inventar o
  schema público.
- **Correção necessária:** manter o item bloqueado até a decisão do achado
  QA-APP-0048-001 e só então reconciliar status e próxima ação.

### QA-APP-0048-003 — Exclusão não autorizada do modelo

- **Requisito:** a aplicação não pode inserir decisão arquitetural além da
  ADR aprovada.
- **Evidência focal:** `contrato_json_console.md` §16.6 acrescenta que a
  persistência não pertence ao “modelo”. A ADR-0048 D-0026-06 fecha apenas a
  delegação à camada responsável pelos dados e exclui renderer/pop-up; não
  decide essa fronteira adicional. O relatório declara que nenhuma decisão
  foi inventada.
- **Impacto:** a aplicação pode restringir uma camada que a ADR deliberadamente
  não escolheu, contradizendo a alegação de aplicação sem nova arquitetura.
- **Correção necessária:** remover essa exclusão ou obter decisão autoritativa
  específica antes do handoff; não resolvê-la por implementação.

ITEM-0023 e ITEM-0024 não foram alterados pela aplicação.
