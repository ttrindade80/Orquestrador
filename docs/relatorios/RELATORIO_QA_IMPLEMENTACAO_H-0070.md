# Relatório QA — implementação H-0070

rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0070
  handoff: docs/handoff/H-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md
  git:
    branch: master
    HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage: vazio

resultado:
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados:
    - "A1 — demo/teste_demo_paginacao.py::test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1 foi alvo explícito de §19-I e ainda falha em `assert \"[PgUp]\" in saida` (L218). As asserções H-0070 do chip agrupado (` PgUp/PgDn. PÁGINAS`, ANSI de inativo) já passaram no mesmo teste. O literal restante descreve o par PgUp/PgDn que H-0070 reescreveu na Barra real, não um chip de uma tecla. Não é EXTERNA_CONFIRMADA."
  bloqueios:
    - "Patch de implementação requerido nos testes-alvo de paginação; validação manual final do ITEM-0010 não iniciada."

validacoes:
  filhos: "OK. Sem A)/B)/C); ●/○ e recuo preservados; cursor na região liberada; mesma coluna de texto com/sem foco. Condicionamento em conteudo_externo.py só no nível selecionável com designador vazio; demais apresentações intactas."
  amostras: "OK. Largura máxima por categoria em tela/estilo.py via _largura_sem_ansi; padding em compor_titulo_com_amostra via _ljust_sem_ansi; ANSI fora da coluna."
  h0064: "OK. Só a geometria do título foi alinhada ao padding; amostra e coluna continuam verificadas."
  chips_uma_tecla: "OK. _texto_chip_barra sem aplicar_estilo; lógica / só no agrupamento H-0051."
  multitecla_delimitados: "OK. Família delimitado concatena teclas; Colchete [PgUp][PgDn]; _ESTILO_CURVA ainda cobre."
  ponto: "OK. Unidade  PgUp/PgDn. com espaço inicial e um ponto."
  destaque_texto: "OK. Unidade  PgUp/PgDn ; cor no conteúdo; rótulo fora; largura visual ignora ANSI."
  destaque_fundo: "OK. Fundo cobre os espaços laterais; rótulo fora."
  barra_real: "OK no produto. Discriminador pelos 5 campos resolvidos, sem nome de preset nem schema novo. Catálogo vigente não colide."
  runtime_resize: "OK em demo/teste_demo_estilo_h0070.py (Ponto/Destaque, 100/60/100, página 2)."
  paginacao: "Produto correto; entrega de teste incompleta (A1). p02 ainda vermelho por [Esc]/[✥] de uma tecla."
  regressao_generica: "OK. tela/testes_renderizador/conteudo_externo.py 17 passed (H-0036/H-0037)."

testes:
  h0070: "7 passed / 0 failed"
  h0064: "12 passed / 0 failed"
  barra: "83 passed / 2 failed / 0 errors (85 coletados)"
  h0068_h0069: "31 passed / 0 failed"
  focal_combinada: "421 passed / 39 failed / 0 errors"
  suite_completa: "1261 passed / 74 failed / 17 errors"

falhas_externas_confirmadas:
  - "config/estilo.json vigente Ponto/caixa_alta (fato anterior ao H-0070, arquivo não escrito por esta fatia): chips de uma tecla [Esc]/[␣]/[?]/[✥] vs  Esc./ ␣./ ?. / ✥.; Ajuda vs AJUDA; popup [A] vs  A.; h0050  ␣. MARCAR; loader H-0038 espera Colchete ativo."
  - "testes não autorizados que ainda exigem [PgUp][PgDn] Páginas (h0055, rótulos P21, H-0041/H-0043/H-0050/H-0053–H-0058): já falhavam sob Ponto pré-H-0070 (` PgUp. PgDn.`). Não são regressão nova."
  - "17 errors: gate H-0038 Colchete e snapshots de explorar_barra/diagnóstico; loader/outros, não o renderer H-0070."

observacao:
  baseline_pre_H0070: "1246 passed / 82 failed / 19 errors"
  delta_liquido: "melhora; não prova ausência de A1"
  p02: "test_demo_h0045_p02 e barra_menus.h0045_p02 atualizaram o agrupamento mas o localizador ainda exige [Esc]; uma tecla Ponto permanece  Esc. (tipo A). A geometria ficou coberta pela suíte H-0070."

validacao_manual_final_ITEM0010: OBRIGATORIA
