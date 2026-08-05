---
name: relatorio-patch-aplicacao-adr-0040-p03
description: Delta incremental da aplicação documental da ADR-0040 após resolução do campo declarativo
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_APLICACAO_ADR
  status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
  data: 2026-08-04
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ADR-0040 / aplicação documental P03
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0040_P02.md
  achados_tratados:
    - BLOQUEIO-CAMPO-ESTADO-INICIAL
---

# REL-PATCH-0040-P03 — Aplicação documental

> Relatório incremental. Registra somente o delta desta execução; não substitui o relatório raiz nem o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_APLICACAO_ADR
status_literal: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0040_P02.md
achados_tratados:
  - BLOQUEIO-CAMPO-ESTADO-INICIAL
achados_resolvidos:
  - controle_execucao.modo_inicial aplicado nominalmente nos artefatos autorizados
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: BLOQUEIO-CAMPO-ESTADO-INICIAL
    alteracao: Aplicada a declaração raiz opcional controle_execucao com modo_inicial obrigatório e enumeração executar | dry_run; propagado o vínculo declarativo nos contratos e nomenclaturas autorizados.
arquivos_criados:
  - caminho: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P03.md
arquivos_alterados:
  - caminho: docs/contratos/contrato_tela_json.md
    delta: Estrutura nominal, ciclo de vida, compatibilidade e validações do controle universal.
  - caminho: docs/contratos/contrato_barra_de_menus.md
    delta: Existência vinculada a controle_execucao válido e destaque somente em Dry-Run.
  - caminho: docs/contratos/contrato_chip.md
    delta: Identidade reutilizável, não canônica, existência declarativa e operação nos dois estados.
  - caminho: docs/contratos/contrato_console.md
    delta: Formulação explícita de que o modo capturado acompanha o lote reconciliado na requisição; fronteiras de lote, seleção e propriedade do modo preservadas.
  - caminho: docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    delta: controle_execucao.modo_inicial como configuração concreta e modo vivo não persistido.
  - caminho: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    delta: Vínculo declarativo, rótulos dinâmicos, posição e distinção focal.
  - caminho: docs/nomenclatura/32_CONSOLE.md
    delta: Fronteira do modo em relação a lote, requisição e propriedade do console.
  - caminho: docs/adr/INDICE_ADR.md
    delta: ADR-0040 marcada como aplicação documental concluída, aguardando QA independente.
  - caminho: docs/backlog.md
    delta: ITEM-0020 atualizado para em_andamento e aguardando QA antes do handoff.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: leitura focal dos contratos, nomenclaturas, índice, backlog e ADR
    resultado_compacto: conformidade textual verificada; contrato_console foi apenas completado na formulação explícita da transmissão já vigente.
  - comando_ou_metodo: buscas focais por controle_execucao, modo_inicial, dry_run_ativo, ITEM-0020 e ADR-0040
    resultado_compacto: declaração nominal, distinções e estados atualizados; uma única linha da ADR-0040 no índice.
  - comando_ou_metodo: git diff --check nos arquivos alterados
    resultado_compacto: sem erros de whitespace.
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas: []
```
