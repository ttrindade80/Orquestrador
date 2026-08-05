---
name: REL-PATCH-APLICACAO-0040-P06
description: Aplicação documental incremental de D-DRY-10 e D-DRY-11
metadata:
  type: relatorio_aplicacao
  status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
  data: 2026-08-05
---

# Relatório de patch de aplicação — ADR-0040 P06

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0040_P03.md
achados_tratados:
  - QA-H0050-03
  - QA-H0050-04
  - QA-H0050-09
decisoes_aplicadas:
  - D-DRY-10
  - D-DRY-11
```

## Aplicação

Foram alterados `contrato_tela_json.md`, `contrato_json_console.md`,
`contrato_console.md`, `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`, `32_CONSOLE.md`,
`INDICE_ADR.md` e `backlog.md`. Foram criados `contrato_registro_acoes.md` e
este relatório.

`controle_execucao` foi fechado como objeto raiz opcional contendo exatamente
`modo_inicial`, com os valores `executar` e `dry_run`; propriedades adicionais
são inválidas, não há default e o modo vivo permanece separado da configuração.
O novo contrato registra a autoridade documental da implementação da ação,
`categoria` obrigatória (`processo`, `navegacao`, `visualizacao`) e
`modos_execucao_aceitos` obrigatório para processo, limitado a `executar` e
`dry_run`. Processo pode declarar subconjunto real, mas tela adotante exige os
dois modos. Resolução ausente ou insuficiente falha de forma fechada; não há
inferência, migração global, arquitetura física obrigatória ou protocolo público
novo.

A elegibilidade da tela exige resolução autoritativa de todas as ações
relevantes; navegação e visualização ficam fora da exigência dos dois modos. O
JSON do console mantém suas referências e não declara categoria ou
compatibilidade. O console pode acionar a ação, mas não é proprietário desses
metadados; o modo capturado acompanha a requisição e o lote reconciliado quando
aplicável, sem pertencer ao lote.

D-DRY-01 a D-DRY-09 foram preservadas, assim como a separação entre configuração
e runtime, a transmissão explícita e imutável do modo e a representação interna
reversível. O H-0050 permaneceu sem alteração; não houve implementação, QA do
handoff, validação manual, testes de código ou escrita de Git.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/32_CONSOLE.md
  termos_adicionados:
    - controle_execucao
    - controle_execucao.modo_inicial
    - registro de ações
    - ação registrada
    - categoria da ação
    - modos de execução aceitos
    - autoridade implementacional da compatibilidade
    - falha fechada de resolução
    - ação legada não classificada
  termos_alterados: []
  distincoes_adicionadas:
    - controle_execucao × modo corrente
    - contrato semântico do registro × arquitetura física
    - modo universal × console/lote
  fronteiras_alteradas:
    - JSON da tela/console referencia ações, mas não declara categoria ou compatibilidade
    - registro da implementação é autoridade sobre categoria e modos aceitos
  dependencias_condicionais_adicionadas:
    - tela com controle_execucao exige registro completo e os dois modos em toda ação de processo relevante
```

## Verificações, bloqueios e próximo passo

Foram revisados os valores exatos, o fechamento semântico, a ausência de campos
de compatibilidade no JSON, a autoridade do registro, a falha fechada, a
ausência de inferência, a ausência de migração global e a ausência de protocolo
público novo. Foi revisado o diff somente dos arquivos autorizados e executado
`git diff --check` nesses arquivos. Não há bloqueios documentais nesta aplicação.

```yaml
status: PATCH_APLICACAO_ADR_COMPLETED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md
artefatos:
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_registro_acoes.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_console.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
  - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md
bloqueios: nenhum
proxima_acao: QA_POS_PATCH_APLICACAO_ADR
```
