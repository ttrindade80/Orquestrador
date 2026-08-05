# Relatório do patch documental — ADR-0008 / ITEM-0015 / P03

```yaml
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ITEM-0015 / ADR-0008 / P03
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  origem:
    - docs/relatorios/RELATORIO_QA_HANDOFF_H-0049.md
  achados_documentais_tratados:
    - H49-QA-01
    - H49-QA-09

execucao:
  status: PATCH_APLICACAO_ADR_COMPLETED
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P03.md
  arquivos_alterados:
    - docs/contratos/contrato_cabecalho.md
    - docs/nomenclatura/30_CABECALHO.md

resultado:
  delta_material:
    - algoritmo fechado de inicio_de_frase, com alteração exclusiva do primeiro caractere alfabético, preservação literal dos demais caracteres e exemplos normativos;
    - ordem fechada da descrição: corte por max_caracteres, capitalização, alinhamento e recuo, e limitação geométrica já contratada;
    - domínio integral de max_caracteres como inteiro entre 1 e 200, inclusive, sem default e com rejeição dos valores fora do domínio ou não inteiros.
  verificacoes_executadas:
    - rg de inicio_de_frase e max_caracteres nos dois documentos autorizados;
    - rg de formulações sem limite superior nos dois documentos autorizados;
    - git diff --check nos três arquivos do patch;
    - git diff dos três arquivos do patch.
  bloqueios: []
```
