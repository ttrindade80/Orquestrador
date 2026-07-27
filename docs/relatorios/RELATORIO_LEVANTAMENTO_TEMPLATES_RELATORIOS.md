---
name: RELATORIO_LEVANTAMENTO_TEMPLATES_RELATORIOS
description: "Levantamento documental sobre templates canonicos de relatorio, regras vigentes de producao de relatorios e lacunas para futura ADR"
metadata:
  type: relatorio_levantamento
  status: LEVANTAMENTO_CONCLUIDO
  data: 2026-07-26
rastreabilidade:
  etapa: LEVANTAMENTO_DOCUMENTAL_FORMAL
  objeto: templates canonicos para relatorios
---

```yaml
rastreabilidade:
  etapa: LEVANTAMENTO_DOCUMENTAL_FORMAL
  objeto: templates canônicos para relatórios

execucao:
  status: LEVANTAMENTO_CONCLUIDO
  arquivos_consultados:
    - docs/templates/TEMPLATE_ADR.md
    - docs/templates/TEMPLATE_BUG.md
    - docs/templates/TEMPLATE_HANDOFF_IMPLEMENTACAO.md
    - docs/templates/TEMPLATE_HANDOFF_QA.md
    - docs/templates/TEMPLATE_RELATORIO_IMPL.md
    - docs/templates/TEMPLATE_RELATORIO_QA.md
    - docs/templates/TEMPLATE_RFC.md
    - docs/INDICE.md (trechos)
    - docs/adr/INDICE_ADR.md (trecho)
    - docs/handoff/README.md (trecho)
    - docs/contratos/contrato_processo_desenvolvimento.md (trechos §5, §12)
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md (trecho)
    - docs/adr/ADR-0006-renomeacao-console-dashboard.md (trecho)
    - docs/adr/ADR-0007-tela-processamento-composicao.md (trecho)
    - docs/adr/ADR-0017-redimensionamento-reativo-tui.md (trecho)
    - docs/nomenclatura/32_CONSOLE.md (trecho, verificação lateral)

resultado:
  templates_existentes:
    - "TEMPLATE_ADR.md → ADR-NNNN"
    - "TEMPLATE_BUG.md → BUG-NNNN"
    - "TEMPLATE_HANDOFF_IMPLEMENTACAO.md → H-NNNN"
    - "TEMPLATE_HANDOFF_QA.md → QA-NNNN"
    - "TEMPLATE_RELATORIO_IMPL.md → IMP-NNNN (relatório de implementação de H-NNNN)"
    - "TEMPLATE_RELATORIO_QA.md → REL-QA-NNNN (relatório de QA de QA-NNNN)"
    - "TEMPLATE_RFC.md → RFC-NNNN"
    - "NAO_EXISTE template para: LEVANTAMENTO, APLICACAO_ADR, VALIDACAO_MANUAL, VERIFICACAO_FECHAMENTO, CONSOLIDACAO, INVESTIGACAO, CORRECAO, HISTORICO, ARQUIVAMENTO, AUDITORIA — tipos usados extensivamente em docs/relatorios/ (dezenas de ocorrências em ADRs e handoffs) sem template canônico correspondente"

  regras_vigentes:
    - "contrato_processo_desenvolvimento.md §5: ciclo padrão exige 'produzir relatório de implementação' (passo 5) e 'produzir relatório de QA' (passo 7); não menciona template para outros tipos de relatório"
    - "contrato_processo_desenvolvimento.md §12: exemplo neutro de caminho usa subpastas docs/relatorios/implementacao/ e docs/relatorios/qa/; prática observada no repositório usa docs/relatorios/<NOME>.md em caminho plano — NAO_CONFIRMADO se subpastas são regra vigente ou apenas exemplo ilustrativo"
    - "ADR-0005, ADR-0006, ADR-0007: 'Qualquer arquivo em docs/relatorios/ | Não é normativo(; não cria regra)'"
    - "ADR-0017: 'docs/relatorios/ | Artefatos históricos de rastreabilidade; não reescrever'"
    - "docs/handoff/README.md §Tipos: tabela prefixo→template vincula H-NNNN, QA-NNNN, BUG-NNNN aos templates de handoff, não aos de relatório"
    - "docs/adr/INDICE_ADR.md §Como criar ADR, passo 1: 'Copiar docs/templates/TEMPLATE_ADR.md'"

  referencias_a_obrigatoriedade:
    - "TEMPLATE_HANDOFF_IMPLEMENTACAO.md §Saída esperada: 'Produzir relatório IMP-NNNN-descricao.md usando docs/templates/TEMPLATE_RELATORIO_IMPL.md'"
    - "TEMPLATE_HANDOFF_QA.md §Saída esperada: 'Produzir relatório REL-QA-NNNN-descricao.md usando docs/templates/TEMPLATE_RELATORIO_QA.md'"
    - "docs/INDICE.md, item 8 da estrutura de leitura: 'Templates em docs/templates/, conforme a tarefa' — routing genérico, sem termo de obrigatoriedade explícita"
    - "Handoffs individuais (H-0001, H-0002, H-0024, H-0025, H-0030, H-0031) instruem o executor a usar TEMPLATE_RELATORIO_IMPL.md — instrução pontual por ciclo, não regra geral"
    - "NAO_ENCONTRADO: nenhuma ocorrência do padrão 'uso obrigatório ... template' fora dos casos acima"

  documentos_candidatos_a_alteracao:
    - docs/templates/ (novos arquivos a depositar; possível ajuste dos 7 existentes)
    - docs/INDICE.md (item 8 da estrutura)
    - docs/handoff/README.md (tabela tipo→template, se novos tipos passarem a ter handoff correspondente)
    - docs/contratos/contrato_processo_desenvolvimento.md (§5 ciclo padrão; §12 exemplos de nome/caminho)
    - docs/relatorios/README.md (NAO_CONFIRMADO — não lido nesta etapa por proibição do manifesto)
    - docs/adr/INDICE_ADR.md (possível, se o fluxo de criação de ADR passar a exigir relatório de levantamento com template próprio)

  conflitos_ou_lacunas:
    - "Sem conflito aparente entre 'docs/relatorios/ não é normativo/não reescrever' (ADR-0005/6/7/17) e uma futura obrigatoriedade de template: a obrigatoriedade regeria a criação de novos relatórios, não a reescrita dos existentes — mas a futura ADR deve declarar essa não retroatividade explicitamente"
    - "Lacuna material: a maior parte dos tipos de relatório em uso corrente (LEVANTAMENTO, APLICACAO, VALIDACAO_MANUAL, VERIFICACAO_FECHAMENTO etc.) não possui template canônico; a obrigatoriedade de uso de template não pode ser aplicada a esses tipos até o depósito"
    - "Conteúdo de docs/relatorios/README.md permanece desconhecido nesta etapa; pode conter regras de nomenclatura/cadeia relevantes que precisam ser conciliadas com a futura ADR"

  fatos_nao_confirmados:
    - "Conteúdo integral de docs/relatorios/README.md (fora do escopo de leitura autorizado)"
    - "Se subpastas docs/relatorios/implementacao/ e docs/relatorios/qa/ (contrato_processo_desenvolvimento.md §12) constituem regra vigente ou exemplo meramente ilustrativo"
    - "Nomes, campos e tipos de relatório que os novos templates do usuário cobrirão"
    - "Se a futura ADR pretende criar template por tipo de relatório (LEVANTAMENTO, APLICACAO etc.) ou um template único genérico"

  momento_recomendado_para_deposito:
    - "Antes da criação da ADR: os novos templates devem ser depositados em docs/templates/ e inventariados (nome do arquivo, tipo de relatório atendido, campos obrigatórios) para que a ADR possa referenciá-los como fato consumado, e não como proposta especulativa"
    - "O inventário dos templates depositados é pré-requisito factual da ADR, não uma decisão desta etapa"

bloqueios: []
```
