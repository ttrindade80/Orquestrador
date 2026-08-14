# Relatório QA_HANDOFF H-0067

```yaml
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0067
  handoff: docs/handoff/H-0067-confirmacao-aplicacao-estilo.md
  item: ITEM-0010
  adr: ADR-0046

resultado:
  status: H1_HANDOFF_APPROVED
  verificacoes_executadas:
    - Integral: H-0067, ADR-0046, H-0066, H-0061, contrato_popup,
      35_POPUP, contrato_barra_de_menus.
    - Focal: H-0065, H-0063, H-0056, H-0057, H-0059, ADR-0044/0045.
      H-0062 não autoridade.
    - RO: popup.py, estilo.py, demo.py, tela.py, fixture h0063,
      teste_popup, teste_demo_popup, teste_demo_estilo_h0066.
    - Git RO: master @ 77bd8bf; stage vazio.
  achados: []
  bloqueios: []
  estado_git:
    branch: master
    head: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage_vazio: true
    arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0067.md
    outros_arquivos_alterados_nesta_etapa: []

pontos_especiais:
  autoridade_popup_texto: >
    CONFIRMADA literalmente. contrato_popup §9.1 e 35_POPUP §6.1:
    confirmação ADR-0046 usa tipo: texto e devolve só CONFIRMADO ou
    ABORTADO. §9: Esc→ABORTADO; confirmação declarada→CONFIRMADO;
    Enter é a tecla quando o chip existe. Não depende do relatório
    de criação.
  extensao_popup: >
    Factual: validar_declaracao_popup rejeita Enter em tipo texto;
    consumir_tecla_popup só confirma Enter em marcacao. Escopo
    histórico H-0059, não contrato vigente. Extensão genérica
    texto+Enter→CONFIRMADO sem valor é implementação legítima;
    H-0067 delimita sem segundo renderer/shell/hardcode.
  chips: >
    Esc/Voltar→ABORTADO; Enter/Confirmar→CONFIRMADO; Esc antes de
    Enter. Literais exigidos pelo validador atual, não pela ADR;
    reuso operacional, não norma indevida.
  confirmado_abortado: >
    Já em contrato_popup §9/§9.1, 35_POPUP §6/§6.1, ADR-0046 §6/§7.
    Desta camada; sem literal novo.
  resultado_positivo: >
    Fecha popup; CONFIRMADO; solicitação retida; sem persistência/
    publicação/promoção; baseline/global/arquivo intactos.
  resultado_negativo: >
    ABORTADO; volta à Estilo; candidato/Aplicar preservados;
    solicitação descartada; novo Aplicar cria nova. Descarte OK.
  retencao_solicitacao: >
    Slot H-0066 solicitacao_aplicacao_estilo: CONFIRMADO mantém;
    posterior consome; imutável ante mutação do candidato.
  descarte_solicitacao: >
    ABORTADO limpa pendência; sem latência; candidato editável.
  modalidade: >
    demo.py ~860–872 intercepta toda tecla com popup aberto.
    Esc≠descartar_visita H-0065; Enter≠re-Aplicar; setas bloqueadas.
  snapshot: >
    Consome SolicitacaoAplicacaoEstilo; proíbe reconstruir do
    runtime. Prova A/B vs C coberta.
  resize: >
    Geometria/SIGWINCH/quadro mínimo genéricos; sem geometria Estilo.
  arquivos_autorizados: >
    Mínimos. Fixture h0063 necessária (contrato §3.1 popups[ID]).
    estilo.py: envelope/ID. teste_popup/demo_popup: extensão
    compartilhada. Só 3 testes H-0066 conflitam; H-0063/64/65 não.
  testes_h0066: >
    (1) test_aplicar_presente_ativo_enter_produz_somente_solicitacao
    L140–141; (2) test_fronteiras_apos_enter_aplicar_sem_popup…
    L377–379; (3) test_snapshot_imutavel… L346–349 engolidos pelo
    modal. Autorização só neles.
  regressao_popup: >
    §10: marcacao intacto; texto sem Enter inalterado; Esc→ABORTADO;
    regressão H-0056–H-0060.
  fronteira_posterior: >
    Fora: estilo.json, publicação, baseline, demo integrada, preview.
    Termina em decisão estrutural.
  validacao_manual: >
    Automatizável. Sem I5; TTY só se teclas físicas indistinguíveis.
```

Fatia exclusiva: SolicitacaoAplicacaoEstilo → popup `tipo: texto` →
CONFIRMADO/ABORTADO → resultado estrutural, antes de persistência/
publicação/baseline/preview. Partição sobre a tela de Estilo compatível
com ADR e H-0066. Pronto para implementação.
