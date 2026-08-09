rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0054
  artefato_principal: docs/handoff/H-0054-selecao-multinivel.md
  cadeia_raiz: docs/handoff/H-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0054.md
  achados_tratados:
    - QA-H0054-001
    - QA-H0054-002
    - QA-H0054-003

execucao:
  status: HANDOFF_PATCH_APPLIED

resultado:
  delta_material:
    - recomputação dos chips vigentes preservada durante mudanças de cursor/seleção, incluindo `[Esc] Limpar` quando aplicável
    - reconciliação passou a contemplar perda de navegabilidade
    - criação de `docs/relatorios/IMP-0054-selecao-multinivel.md` explicitamente autorizada, preservando relatórios históricos
  verificacoes_executadas:
    - diff focal do handoff
