# Relatório de patch de implementação — H-0069 P01

rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0069
  patch: P01
  cadeia:
    raiz: docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md
    predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0069.md
  achados_tratados:
    - A1
    - A2

resultado:
  status: IMPLEMENTATION_PATCHED
  A1:
    correcao: >-
      O encerramento terminal do popup de confirmação foi centralizado em
      _encerrar_demonstracao_estilo. ABORTADO e CONFIRMADO removem
      _sessao_demonstracao_estilo, _modelo_origem_demonstracao_estilo,
      estilo_demonstracao_local e a solicitação conforme a política vigente.
      CONFIRMADO aplica a solicitação H-0068 antes da limpeza. O retorno à
      Estilo resolve o modelo pela tela atual, sem chave privada residual.
    testes: >-
      demo/teste_demo_estilo_h0069.py passou 10/10; as provas ABORTADO e
      CONFIRMADO verificam ausência das três chaves e preservam os estados
      C/G1/B1 ou G2/baseline/candidato, com Aplicar ativo ou inativo.
  A2:
    natureza: expectativa_predecessora_superada_por_H0069
    correcao: >-
      O teste focal passou a materializar o quadro base e o quadro com popup
      pela demonstração integrada H-0069 sob C. A geometria visual é calculada
      com a mesma materialização local e a comparação verifica prefixos,
      sufixos, linhas fora do retângulo, bordas e largura visual.
    invariavel_preservada: >-
      O popup apenas substitui seu retângulo visual; não desloca bordas, não
      altera o quadro fora dele, não causa overflow e mantém composição ANSI
      visualmente coerente. A infraestrutura genérica continua coberta
      independentemente por tela/teste_popup.py e demo/teste_demo_popup.py.
    testes: >-
      demo/teste_demo_estilo_h0067.py::test_borda_console_subjacente_preservada_fora_do_popup
      passou 1/1.
  falhas_externas_nao_tratadas:
    - config_estilo_preset_default_Ponto
  suite_focal: >-
    H-0069: 15 passed / 0 failed; H-0068: 14 passed / 0 failed; H-0067
    focal: 1 passed / 0 failed; popup genérico: 79 passed / 4 failed,
    falhas externas já atribuídas a chips/ANSI; regressão H-0063–H-0069:
    129 passed / 13 failed, somente as 13 falhas externas conhecidas do
    preset Ponto. A2 não reaparece.
  suite_completa: >-
    1250 passed / 76 failed / 17 errors. Comparada ao QA anterior
    (1249 passed / 77 failed / 17 errors), a redução de uma falha corresponde
    a A2; não foi identificada falha nova atribuível a H-0069. O remanescente
    pertence às alterações externas de configuração/worktree já registradas.
  config_estilo_json: >-
    somente leitura neste patch; chip.preset_default permanece Ponto e o
    arquivo não foi escrito.
  validacao_manual_H0069: OBRIGATORIA
  validacao_manual_final_item_0010: OBRIGATORIA
  bloqueios: []
