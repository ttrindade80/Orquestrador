---
name: relatorio-patch-aplicacao-adr-0040-p04
description: Correção incremental dos achados QA-APL-0040-P03-01 e QA-APL-0040-P03-02
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
  data: 2026-08-04
---

# REL-PATCH-0040-P04 — Aplicação documental

## Cadeia e achados

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0040_P03.md
achados_tratados:
  - QA-APL-0040-P03-01
  - QA-APL-0040-P03-02
```

## Arquivos e regras propagadas

```yaml
arquivos_alterados:
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P04.md
regras_D-DRY-07_propagadas:
  - abertura inicializa o modo por controle_execucao.modo_inicial
  - a escolha é preservada na mesma instância
  - suspensão por tela de resultado preserva o modo
  - retorno à mesma instância preserva o modo corrente
  - nova abertura reinicializa pelo valor declarado
  - recarga reinicializa pelo valor declarado, mesmo se coincidir com o modo anterior
  - encerramento da instância não persiste o modo
  - dry_run_ativo continua restrito à especialização focal da ADR-0037
preservacoes:
  - o modo corrente permanece estado de runtime e não é escrito no tela.json
  - o ciclo de vida pertence à tela/runtime; barra e chip apenas representam o modo
  - o console não se torna proprietário do modo global
  - a especialização focal da ADR-0037 não é migrada nem alterada
```

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  termos_adicionados:
    - preservação do modo corrente na mesma instância suspensa
    - reinicialização do modo em nova abertura ou recarga
  termos_alterados:
    - ciclo de vida do modo como responsabilidade da tela/runtime, não do chip
  distincoes_adicionadas:
    - suspensão e retorno à mesma instância versus nova abertura ou recarga
    - rótulo que representa o modo corrente versus ciclo de vida que o inicializa
  fronteiras_alteradas:
    - barra e chip representam o modo; a tela/runtime inicializa, preserva e reinicializa o estado
  dependencias_condicionais_adicionadas: []

delta_terminologico_consolidado:
  proveniente_do_P03:
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
      - controle_execucao.modo_inicial como configuração concreta versus modo corrente como estado de runtime
      - modo transmitido junto ao lote reconciliado versus identidade do lote
    fronteiras_alteradas:
      - console transmite o modo na requisição, mas não é proprietário do modo global da tela
    dependencias_condicionais_adicionadas: []
  adicional_do_P04:
    modulos_alterados:
      - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
      - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    termos_adicionados:
      - preservação do modo corrente na mesma instância suspensa
      - reinicialização do modo em nova abertura ou recarga
    termos_alterados:
      - ciclo de vida do modo como responsabilidade da tela/runtime, não do chip
    distincoes_adicionadas:
      - suspensão e retorno à mesma instância versus nova abertura ou recarga
      - rótulo que representa o modo corrente versus ciclo de vida que o inicializa
    fronteiras_alteradas:
      - barra e chip representam o modo; a tela/runtime inicializa, preserva e reinicializa o estado
    dependencias_condicionais_adicionadas: []
```

## Verificações, bloqueios e status

```yaml
verificacoes:
  - busca focal confirmou suspensão/retorno preservados, nova abertura/recarga reinicializadas por modo_inicial e ausência de persistência no JSON
  - contratos e nomenclaturas confirmaram que chip e console não são proprietários do modo global
  - delta P03 foi confirmado nos módulos 02, 31 e 32; 32 não foi alterado no P04
  - diff revisado somente nos arquivos autorizados
  - git diff --check concluído sem erros nos arquivos autorizados
bloqueios: []
status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
proxima_acao: QA_POS_PATCH_APLICACAO_ADR
```
