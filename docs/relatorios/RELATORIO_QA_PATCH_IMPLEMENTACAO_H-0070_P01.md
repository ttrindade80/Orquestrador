rastreabilidade:
  etapa: QA_POS_PATCH
  objeto: H-0070
  patch: P01
  cadeia:
    raiz: docs/relatorios/IMP-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md
    predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0070_P01.md

resultado:
  status: I1_IMPLEMENTATION_APPROVED
  A1: "A1_RESOLVIDO: expectativa residual substituída por prova semântica da unidade PgUp/PgDn.; delta P01 restrito ao teste, sem mudança atribuível no produto ou na configuração."
  achados_pendentes: []
  achados_novos: []
  bloqueios: []

testes:
  A1: "1 passed"
  paginacao: "108 passed / 20 failed; A1 passou."
  h0070: "7 passed / 0 failed"
  barra: "83 passed / 2 failed; mesmas falhas externas conhecidas."
  predecessores: "43 passed"
  suite_completa: "1262 passed / 73 failed / 17 errors; +1 passed, -1 failed, errors inalterados frente ao baseline."

falhas_externas_confirmadas:
  - "Paginação: 20 falhas em chips de uma tecla Ponto ([Esc], [✥], Marcar) e literais históricos [PgUp]/[PgDn] fora de A1; nenhuma passa pelo delta P01."
  - "Barra: h0045_p02 falha em [Esc] e h0050 em [␣] Marcar; ambas reproduzem expectativas históricas de chips de uma tecla, não a unidade multitecla A1."

validacao_manual_final_ITEM0010: OBRIGATORIA
