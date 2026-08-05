---
name: relatorio-aplicacao-adr-0040
description: Relatório da aplicação documental da ADR-0040
metadata:
  type: relatorio
  escopo: aplicacao_adr
---

# Relatório de aplicação — ADR-0040

## Resultado

A ADR-0040 foi aprovada e seu estado documental foi atualizado para `aceita`.
A propagação independente foi realizada, mas a aplicação não pode ser
concluída porque falta decisão material sobre o nome do campo de configuração
concreta que declara o estado inicial universal.

Nenhum campo vigente foi reutilizado. `dry_run_ativo` foi verificado como
estado de runtime da especialização focal da ADR-0037 e não foi promovido nem
reinterpretado como configuração concreta.

## Arquivos alterados

- `docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_console.md`
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/adr/INDICE_ADR.md`
- `docs/backlog.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md`

## Mudanças e preservações

Foram propagados o chip específico reutilizável, `Insert`, os rótulos
dinâmicos, a operação nos dois estados, o destaque por `cor_alerta`, o modo
único por instância, a compatibilidade integral das ações de processo e a
transmissão explícita do modo junto ao lote reconciliado. A obrigação de
estado inicial explícito foi registrada sem criar chave de schema.

O `[Ins] Dry-Run` focal da ADR-0037, sua autoridade sobre preservação e
restauração da origem e o comportamento vigente do H-0044 foram preservados.
Nenhum código, configuração concreta, teste, handoff ou histórico foi
alterado.

O `ITEM-0020` permanece no backlog com status `bloqueado`.

## Verificações

Foram feitas buscas focais nos arquivos autorizados, revisão do diff restrita
ao manifesto e `git diff --check` nos arquivos alterados. Não foi executada
suíte de código nem QA da aplicação.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
  termos_adicionados:
    - controle universal de execução real e dry-run
    - chip específico padronizado e reutilizável
  termos_alterados:
    - distinção documental do [Ins] Dry-Run focal da ADR-0037
  distincoes_adicionadas:
    - controle universal reutilizável versus especialização focal
    - estado inicial declarado em configuração concreta versus modo corrente em runtime
    - modo transmitido junto ao lote reconciliado versus identidade do lote
  fronteiras_alteradas:
    - console transmite o modo na requisição, mas não é proprietário do modo global da tela
  dependencias_condicionais_adicionadas: []
```

## Saída

```yaml
status: BLOCKED_USER_DECISION
relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
bloqueios:
  - nome do campo de configuração concreta para o estado inicial universal não definido por autoridade vigente
proxima_acao: obter decisão do usuário sobre o nome do campo e retomar a aplicação documental/QA
```
