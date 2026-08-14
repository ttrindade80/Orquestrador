# IMP-0067 — Confirmação da aplicação do estilo

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0067
  predecessor: H-0066
  artefato_principal:
    docs/handoff/H-0067-confirmacao-aplicacao-estilo.md
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - tela/teste_estilo_h0067.py
    - demo/teste_demo_estilo_h0067.py
    - docs/relatorios/IMP-0067-confirmacao-aplicacao-estilo.md
  arquivos_alterados:
    - tela/renderizacao/popup.py
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
    - tela/estilo.py
    - demo/demo.py
    - tela/teste_popup.py
    - demo/teste_demo_estilo_h0066.py
  arquivos_autorizados_inalterados:
    - demo/teste_demo_popup.py

resultado:
  extensao_popup_texto: >
    validar_declaracao_popup aceita tipo texto com chip Enter/Confirmar
    (referencia_regra CONFIRMADO). consumir_tecla_popup despacha CR/LF para
    _confirmar_texto → {status: CONFIRMADO} sem valor. Texto sem Enter e
    marcacao permanecem intactos.
  popup_confirmacao: >
    popups.popup_confirmacao_aplicacao_estilo na fixture H-0063 (tipo texto,
    Esc/Voltar, Enter/Confirmar). ID exposto como
    ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO. Envelope via
    ControladorTelaEstilo.conteudo_popup_confirmacao(solicitacao) sem
    reconsultar runtime.candidato.
  confirmado: >
    Enter no popup fecha, grava popup_resultado CONFIRMADO, retém
    solicitacao_aplicacao_estilo; baseline/global/arquivo/candidato intactos.
  abortado: >
    Esc fecha, ABORTADO, descarta solicitacao da tentativa; permanece na
    tela de Estilo; candidato/selecoes/aplicar_disponivel preservados;
    nova Enter produz nova solicitacao+popup. Nao dispara descartar_visita.
  modalidade: >
    Ramificacao modal H-0059 preservada: com estado["popup"], toda tecla e
    consumida antes do dispatch da tela. Enter nao reexecuta Aplicar; Esc
    nao sai; setas/PgUp/PgDn/Espaco nao mutam subjacente.
  snapshot: >
    Popup e resultado usam a SolicitacaoAplicacaoEstilo do acionamento;
    mutacao posterior do candidato nao altera a solicitacao retida.
  retencao_solicitacao: >
    solicitacao_aplicacao_estilo preservada entre comandos; apos CONFIRMADO
    permanece disponivel para H-0068.
  descarte_solicitacao: >
    ABORTADO no popup de confirmacao de estilo remove a chave; tentativa
    abortada nao fica pendente.
  resize: >
    Geometria generica reutilizada; reducao/crescimento preservam a mesma
    instancia logica e o overlay.
  fronteira_posterior: >
    Sem persistencia, publicacao, promocao de baseline, preview real ou
    demonstracao integrada.
  testes:
    h0067: 14 passed
    popup: 81 passed
    h0066: 27 passed
    regressao_h0063_h0064_h0065_h0066: 91 passed
    suite_completa: 1286 passed
  demonstracao:
    - F4 abre Estilo
    - Espaco/seta/Espaco diverge candidato; Aplicar ativo
    - Enter produz solicitacao e abre popup tipo texto
    - setas com popup aberto nao mutam candidato
    - resize 80x24 / 62x20 / 100x30 preserva instancia
    - Esc → ABORTADO; candidato preservado; solicitacao descartada
    - nova Enter → nova solicitacao; Enter → CONFIRMADO retido
    - config/estilo.json, baseline e global intactos
  validacao_manual_necessaria: []
  desvios:
    - >
      demo/teste_demo_popup.py nao exigiu alteracao: declaracoes
      demonstrativas H-0056–H-0059 nao declaram Enter em tipo texto;
      regressao coberta pela suíte existente (81 passed).
    - >
      Demonstracao ponta a ponta do ciclo Enter/CONFIRMADO usa
      processar_comando (fluxo real non-TTY). O loop main line-oriented
      descarta CR/LF via rstrip — mesma limitacao ja aceita em H-0066;
      smoke main sem Enter permanece como complementar.
  bloqueios: []

tratamento_testes_h0066:
  alterados:
    - test_aplicar_presente_ativo_enter_produz_somente_solicitacao
    - test_fronteiras_apos_enter_aplicar_sem_popup_persistencia_publicacao
      → test_fronteiras_apos_enter_aplicar_abre_popup_sem_persistencia_publicacao
    - test_snapshot_imutavel_apos_mutacao_posterior_via_dispatch
  expectativas_superadas:
    - Enter ativo nao abre popup
    - fronteira "sem popup" apos Enter/Aplicar
  invariantes_preservados:
    - baseline/global/arquivo intactos apos Enter
    - ausencia de persistencia/publicacao
    - imutabilidade do snapshot (referencia Python apos fechar popup)
    - demais testes H-0066 inalterados
```

## Resumo da implementação

Extensão genérica em `popup.py`: texto + Enter válido produz `CONFIRMADO`
sem payload. Na tela de Estilo, `Enter/Aplicar` ativo (H-0066) abre no mesmo
evento o popup declarado, com envelope derivado da solicitação. A ramificação
modal existente retém a solicitação em `CONFIRMADO` e a descarta em
`ABORTADO`, sem saída efetiva H-0065 e sem persistência/publicação.

## Inspeção final

- `config/estilo.json`: sem delta
- stage: vazio
- nenhum segundo sistema de popup
- somente três testes H-0066 alterados
- H-0063/H-0064/H-0065: arquivos de teste não alterados
- `git diff --check` limpo nos arquivos desta fatia
