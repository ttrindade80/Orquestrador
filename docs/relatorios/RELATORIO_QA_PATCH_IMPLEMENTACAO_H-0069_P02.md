rastreabilidade:
  etapa: QA_POS_PATCH
  objeto: H-0069
  patch: P02
  cadeia:
    raiz: docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md
    predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0069_P02.md

resultado:
  status: I1_IMPLEMENTATION_APPROVED
  MV_A1:
    causa_confirmada: >-
      CONFIRMADO encerra H-0069, mantém tela_atual em H-0063 e o loop
      reobtém o modelo. O shell H-0063 cru, de dois_niveis_por_foco, tem
      conteudo_externo=None; a preparação vigente injeta os nós necessários.
    correcao_validada: >-
      _modelo_corrente recarrega H-0063 e reutiliza _preparar_modelo_estilo,
      sem tolerância em navegacao.py, duplicação ou hardcode no loop.
    teste_reproducao: >-
      PASSOU: os testes pós-CONFIRMADO e pós-ABORTADO observam o estado antes,
      processam o comando, reobtêm o modelo e observam novamente; ambos
      cobrem a avaliação pós-comando que faltava.
  A1_P01: PRESERVADO; as três chaves privadas e a solicitação são removidas em ambos os terminais.
  A2_P01: >-
    PRESERVADO semanticamente, mas o teste focal falha por geometria do
    overlay (diffs 10,12,14). O mesmo assert falhou com o ramo P02 bypassado
    em processo separado, enquanto a sessão H-0069 permanecia aberta; é a
    família externa popup/overlay, não efeito de _modelo_corrente.
  achados_pendentes: []
  achados_novos: []
  testes:
    h0069: 17 passed / 0 failed
    h0068: 14 passed / 0 failed
    A2_focal: >-
      1 failed: demo/teste_demo_estilo_h0067.py::test_borda_console_subjacente_preservada_fora_do_popup;
      classificado EXTERNA_CONFIRMADA pela reprodução sem o delta P02.
    popup: >-
      79 passed / 4 failed; falhas nominais em chips multilinha, overlay ANSI,
      marcacao e modal H-0058; todas coerentes com preset Ponto/rotulagem
      externa já observada.
    regressao_h0063_h0069: >-
      130 passed / 14 failed. As 13 falhas de chips/barra/paginação são
      EXTERNA_CONFIRMADA (config Ponto); a 14a é A2_focal, EXTERNA_CONFIRMADA
      por reprodução independente do P02. Nenhuma REGRESSAO_P02.
    suite_completa: >-
      1246 passed / 82 failed / 19 errors, contra 1250/76/17. Amostragem
      nominal: teste_carregar_estilo e h0052 do loader, chips/paginação de
      renderizador/demo, popup, e gates downstream em demo/teste_demo.py,
      demo/teste_diagnostico.py e demo/teste_explorar_barra_de_menus.py.
      As causas observadas são preset Ponto e famílias externas de barra,
      paginação, popup e loaders; não há falha H-0069 nem evidência ligada ao
      ramo P02.
  falhas_externas_confirmadas:
    - config/estilo.json com chip.preset_default=Ponto e borda Borda Reta.
    - popup/overlay: A2 focal e quatro falhas genéricas, reproduzidas fora do ramo P02.
  bloqueios: []

validacao:
  manual_H0069: REVALIDACAO_OBRIGATORIA
  manual_final_ITEM0010: OBRIGATORIA
