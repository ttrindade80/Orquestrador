# Relatório QA — implementação H-0069

rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0069

resultado:
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  testes:
    h0069: "15 passed / 0 failed"
    h0068: "14 passed / 0 failed"
    popup: "79 passed / 4 failed"
    regressao_h0063_h0069: "128 passed / 14 failed / 0 errors"
    suite_completa: "1249 passed / 77 failed / 17 errors"
  achados:
    - "A1 — após ABORTADO e CONFIRMADO, _sessao_demonstracao_estilo, estilo_demonstracao_local e solicitacao_aplicacao_estilo são removidas, mas _modelo_origem_demonstracao_estilo permanece. A sessão não fica totalmente limpa; a remoção só ocorre depois, ao sair da tela Estilo."
    - "A2 — a falha demo/teste_demo_estilo_h0067.py::test_borda_console_subjacente_preservada_fora_do_popup atravessa H-0069: durante a sessão ativa renderizar_estado recebe o modelo predecessor e aplica a borda local C (┐), divergindo da expectativa global G1 (╮)."
    - "A3 — as outras 13 falhas focais são explicadas por alteração externa confirmada em config/estilo.json (chip.preset_default: Colchete → Ponto): os chips continuam no quadro, mas aparecem como AJUDA/SELECIONAR/APLICAR/PÁGINAS."
  bloqueios:
    - "Patch de implementação requerido; validação manual não iniciada."

proveniencia_falhas:
  baseline_h0068: "1311 passed / 0 failed"
  alegacao_imp_h0069: "As 14 falhas focais e 77 failed / 17 errors seriam pré-existentes por repetição sem os testes H-0069."
  conclusao: "A alegação não é aceita como prova. Não há falha preexistente comprovada: 13 falhas são atribuíveis à alteração externa nominalizada e uma é causalmente atravessada por H-0069."
  evidencia: "A suíte H-0063–H-0068 reproduziu 113 passed / 14 failed; a execução H-0063–H-0069 reproduziu 128 passed / 14 failed. O Git mostra modificações fora do escopo H-0069 em config/estilo.json, tela/carregamento/estilo.py, tela/loader.py, tela/renderizacao/barra_menus.py, contexto_execucao.py, popup.py, tela.py, tela/renderizador.py e tela/teste_popup.py. A diferença de configuração explica a capitalização; os testes popup também falham em alterações externas de chips/ANSI."

pontos_especiais:
  fluxo_normal_sem_demo: "Probes sem sessão preservaram o modelo Estilo, o global vigente e telas externas; não foi observado vazamento H-0069 fora da demonstração."
  demonstracao_local: "A suíte dedicada confirmou C materializado localmente, G1/B1/config preservados e um quadro único com Cabeçalho, Console, Dashboard e Barra."
  popup: "Reutiliza ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO, modalidade textual, geometria e materialização local; o caminho dedicado passou."
  abortado: "Demonstração fechada, C/G1/B1 preservados e Aplicar ativo; permanece a chave de origem residual de A1."
  confirmado: "H-0068 foi reutilizado; C virou G2, baseline/global/estado[\"estilo\"] ficaram coerentes e Aplicar inativo; permanece a chave de origem residual de A1."
  limpeza_estado: "Incompleta: _modelo_origem_demonstracao_estilo sobrevive a ABORTADO e CONFIRMADO."
  categorias: "Fixture/render real expõe borda, chips e indicadores selecionado/incluído sem presets hardcoded na lógica do produto."
  validacao_manual_H0069: OBRIGATORIA
  validacao_manual_final_item_0010: OBRIGATORIA
