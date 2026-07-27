---
name: REL-ALT-0032-aplicacao-adr-0032
description: Aplicação documental da ADR-0032 — pacote canônico de templates
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: DOCUMENTATION_APPLIED
  data: 2026-07-26
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0032
  artefato_principal: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  autoridade_principal: ADR-0032
---

# REL-ALT-0032 — Aplicação da ADR-0032

```yaml
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: ADR-0032
  artefato_principal: docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
  autoridade_principal: ADR-0032

execucao:
  status: DOCUMENTATION_APPLIED
  pacote_depositado_adotado: true
  arquivos_criados:
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0032.md
  arquivos_alterados:
    - docs/adr/ADR-0032-uso-obrigatorio-de-templates-canonicos.md
    - docs/INDICE.md
    - docs/adr/INDICE_ADR.md
    - docs/handoff/README.md
    - docs/relatorios/README.md
    - docs/contratos/contrato_processo_desenvolvimento.md
  arquivos_renomeados:
    - de: docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md
      para: docs/templates/00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md

resultado:
  delta_material:
    - status da ADR-0032 alterado de proposta para aceita, sem tocar decisões, consequências ou escopo
    - índice de templates renomeado sem alteração de conteúdo material
    - docs/relatorios/README.md substituído por roteamento conciso ao índice canônico, com remoção da matriz de tipos (IMP/REL-QA/REL-DOC) e da adaptação de TEMPLATE_RELATORIO_QA.md para auditoria documental
    - docs/INDICE.md passou a apontar nominalmente para o índice renomeado e a distinguir templates de artefatos documentais dos templates de relatórios/evidências
    - docs/adr/INDICE_ADR.md registrou a ADR-0032 e tornou explícito o uso obrigatório de TEMPLATE_ADR.md
    - docs/handoff/README.md passou a rotear handoffs e relatórios de implementação/QA ao índice canônico
    - contrato_processo_desenvolvimento.md ganhou a seção 14 reconciliando obrigatoriedade, resolução prévia, bloqueio, não retroatividade e armazenamento em docs/relatorios/
  incompatibilidades_materiais_corrigidas:
    - arquivo: docs/contratos/contrato_processo_desenvolvimento.md
      secao: "12. Exemplos neutros de nomes"
      motivo: exemplos citavam subpastas docs/handoff/para_implementacao/, docs/handoff/para_qa/, docs/relatorios/implementacao/ e docs/relatorios/qa/ que não existem na organização plana atual de docs/handoff/ e docs/relatorios/ (confirmado por listagem de diretório); caminhos ajustados para a raiz plana sem alterar nomes de arquivo
  referencias_reconciliadas:
    - docs/INDICE.md
    - docs/adr/INDICE_ADR.md
    - docs/handoff/README.md
    - docs/contratos/contrato_processo_desenvolvimento.md
  verificacoes_executadas:
    - comando: "rg 00_INDICE_TEMPLATES_RELATORIOS|00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS docs (excl. docs/relatorios/**)"
      resultado: caminho antigo remanesce apenas em ADR-0032 (texto histórico da própria decisão de renomeação); caminho novo presente em todos os pontos de roteamento
    - comando: "test -e docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md"
      resultado: ausente, conforme esperado
    - comando: "git diff --check"
      resultado: sem problemas de whitespace
  bloqueios: []

delta_nomenclatura:
  modulos_alterados: []
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
```

Nenhuma decisão nova foi introduzida. O pacote de 14 templates depositados foi preservado sem alteração de conteúdo. A obrigatoriedade geral ainda não está em vigor: entra em vigor somente após `QA_APLICACAO_ADR` aprovado.
