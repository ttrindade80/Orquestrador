# Relatório QA pós-patch — H-0069 P01

rastreabilidade:
  etapa: QA_POS_PATCH
  objeto: H-0069
  patch: P01
  cadeia:
    raiz: docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md
    predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0069_P01.md

resultado:
  status: I1_IMPLEMENTATION_APPROVED
  achados_resolvidos:
    A1: >-
      Encerramento terminal centralizado em _encerrar_demonstracao_estilo.
      ABORTADO, CONFIRMADO e falha EstiloErro no ramo CONFIRMADO removem
      _sessao_demonstracao_estilo, _modelo_origem_demonstracao_estilo e
      estilo_demonstracao_local. ABORTADO preserva C/G1/B1 com Aplicar
      ativo; CONFIRMADO aplica H-0068, sincroniza G2/baseline/candidato/
      estado["estilo"] e deixa Aplicar inativo. Retorno à Estilo resolve
      pela tela atual, sem chave residual.
    A2: >-
      O teste focal materializa quadro-base e quadro com popup pela
      demonstração H-0069 sob C, não G1. Prova estrutural: linhas fora do
      retângulo, prefixos/sufixos horizontais, bordas, largura visual e
      composição ANSI. Invariável H-0067/P01 preservada; mudança de
      contexto, não enfraquecimento.
  achados_pendentes: []
  achados_novos: []
  testes:
    h0069_demo: "10 passed / 0 failed"
    h0069: "15 passed / 0 failed"
    h0068: "14 passed / 0 failed"
    h0067_A2: "1 passed / 0 failed"
    popup: "79 passed / 4 failed"
    regressao_h0063_h0069: "129 passed / 13 failed / 0 errors"
    suite_completa: "1250 passed / 76 failed / 17 errors"
  falhas_externas_nao_tratadas:
    - EXTERNAS_NAO_TRATADAS
    - config_estilo_preset_default_Ponto
  bloqueios: []
  git:
    branch: master
    HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage: vazio
  config_estilo_json: >-
    somente leitura; chip.preset_default permanece Ponto; P01 não escreveu
    no arquivo; A1/A2 não dependem de revertê-lo.

validacao:
  manual_H0069: OBRIGATORIA
  manual_final_ITEM0010: OBRIGATORIA
