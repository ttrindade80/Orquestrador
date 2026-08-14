---
name: REL-QA-H0065-P02-vinculacao-candidato-estilo
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H1_HANDOFF_APPROVED
  revisao: P02
---

rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0065
  revisao: P02
  raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
  predecessor_qa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065_P01.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P02.md

resultado:
  status: H1_HANDOFF_APPROVED
  achados_retestados:
    - QA-H0065-002
    - QA-H0065-003
  achados_preservados_resolvidos:
    - QA-H0065-001
  achados_resolvidos: []
  achados_pendentes: []
  novos_achados: []
  bloqueios: []

pontos_especiais:
  fonte_semantica: "OK — candidato runtime é a fonte semântica única; selecoes é projeção/cache não autoritativa e a invariável vale enquanto existir (§§9.1–9.4)."
  reconciliacao_saida: "OK — a lista normativa inclui F4, Espaço com sucesso/falha, redraw, resize e saída efetiva; na saída ocorre após recriar o candidato e antes de concluir (§9.3, §12.2)."
  estado_pos_saida: "OK — antes de qualquer F4, cada categoria exige baseline = candidato = selecoes = A; há testes imediato, multi-categoria e cache divergente (§§12.2, 19)."
  esc_filho: "OK — Esc filho→pais preserva candidato e selecoes da visita, sem descarte (§12.1, §19)."
  F4_defensivo: "OK — cada F4 recria da baseline e reconcilia, como isolamento defensivo separado do descarte (§§4.6, 12.3, 19)."
  atomicidade_preservada: "OK — QA-H0065-001 permanece candidato aceito → projeção, com falha sem mutação parcial (§§7.1–7.2, 17)."
  evidencias_p02: "OK — P02 registra ocorrências da reconciliação, saída entre pontos, pós-Esc antes de F4, Esc filho versus saída, preservação de QA-H0065-001, diff --check e stage vazio."
  arquivos_autorizados: "OK — preservados tela/estilo.py, demo/demo.py, os dois testes H-0065 e IMP-0065; renderer permanece fora (§18)."

Conclusão: o handoff fecha fonte de verdade, reconciliação, descarte imediato,
distinção entre retorno de nível e abandono efetivo, reabertura e fronteira
posterior. Um implementador pode executar H-0065 sem inventar semântica ou
protocolo adicional. Nesta etapa, somente este relatório foi criado; alterações
e arquivos não rastreados já existentes no worktree foram preservados.
