---
name: relatorio-criacao-adr-0032
description: Relatório de criação da ADR-0032 (uso obrigatório de templates canônicos)
metadata:
  type: relatorio
  scope: documental
---

# Relatório — Criação da ADR-0032

Este relatório pertence ao período anterior à entrada em vigor da nova
obrigação de templates. Não declara conformidade com o pacote ainda não
aplicado.

```yaml
rastreabilidade:
  etapa: CRIAR_ADR
  objeto: ADR-0032
  artefato_principal: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md

execucao:
  status: ADR_CREATED
  arquivos_criados:
    - docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
    - docs/relatorios/RELATORIO_CRIACAO_ADR-0032.md

resultado:
  decisoes_materializadas:
    - D-TPL-CICLO-01
    - D-TPL-README-01
    - D-TPL-01
    - D-TPL-02
    - D-TPL-03
    - D-TPL-04
    - D-TPL-05
    - D-TPL-06
    - D-TPL-07
  verificacoes_executadas:
    - test -f docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md (confirmado ausente antes da criação)
    - leitura integral de TEMPLATE_ADR.md, 00_INDICE_TEMPLATES_RELATORIOS.md e docs/relatorios/README.md
    - leitura focal de docs/INDICE.md, docs/adr/INDICE_ADR.md, docs/handoff/README.md e docs/contratos/contrato_processo_desenvolvimento.md via rg
    - confirmação de que ADR-0031 é a última ADR registrada em docs/adr/INDICE_ADR.md, tornando ADR-0032 o próximo número livre
  bloqueios: []
```

## Baseline SHA-256 do depósito (referenciado na ADR-0032, §4)

```yaml
templates:
  00_INDICE_TEMPLATES_RELATORIOS.md: f7346b0718c439f176f9920209f21443785f17931cf51eba6609be924900af96
  TEMPLATE_ADR.md: 7fc839ec9e43e677a8df0918c60ec3707303a405d6416dda06e23a41552f13a4
  TEMPLATE_BUG.md: a4ec33906c2ece607af3fb9c9ddca7732313a3e678208bfc368dfe57101c78cc
  TEMPLATE_EVIDENCIA_MATERIAL.md: a75647a6bdb1831d7bf01b437cea3dd8957c8ac2e3fff30414917bcc960d47ee
  TEMPLATE_HANDOFF_IMPLEMENTACAO.md: d517451ef2547fa57e4583436eb02ab06e78bcf4771d57fe63a4e618f0efe9f2
  TEMPLATE_HANDOFF_QA.md: 2b4caa3c33d5b0892bb3c48e138fb9237bb9cd974d3f4413032a119b3b909da3
  TEMPLATE_RELATORIO_ANALISE_DOCUMENTAL_FINAL.md: 46251d0a055ac83954f53ba8ecfbe310d5ecd16f9e75325b517caaf95b77bb5e
  TEMPLATE_RELATORIO_APLICACAO_ALTERACAO.md: 296bfdca588b91201387f7803f1b00ced435a444f942c3a0c765012303ddda70
  TEMPLATE_RELATORIO_BLOQUEIO.md: 55f9a971aec4afee31d71c74ddb0c08c53f36c01c45c48e33ebcc423f5a30326
  TEMPLATE_RELATORIO_BUSCA_LEVANTAMENTO_VERIFICACAO.md: 9d9ad8902253cbdab94c9d591921ed548d30166774e473026126972849c69e13
  TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md: 2e7a402ce6c2177467e541308ffb855d35768658bf99c52694298de9fe4f9302
  TEMPLATE_RELATORIO_IMPL.md: 03b8547ec2ca1820cfc254afef3a075358a6aba1d603108ba9db85d8dbc4eb5c
  TEMPLATE_RELATORIO_PATCH.md: fe14d12ef6a184ff9816cc0f02e03f0cab61a4b300185e644a3e46174a6e081c
  TEMPLATE_RELATORIO_QA.md: af4beb7b4f362ea99845a4f4778d1027db747ba4c11bb51e36270543459da213
  TEMPLATE_RFC.md: 937ab6ecf8a5248fd67dde96d9a111a0e147fdf5c99fed0c1a32bbad53095c4e
```

Os hashes registram o baseline factual fornecido para esta decisão; não
exigem que uma incompatibilidade material autorizada, na aplicação futura,
preserve o mesmo hash.

## Escopo desta execução

Apenas os dois arquivos listados em `execucao.arquivos_criados` foram
criados. Nenhum template, índice, README, contrato ou handoff foi
modificado. Não houve QA, aplicação, handoff ou implementação nesta etapa.
