status: I2_IMPLEMENTATION_PATCH_REQUIRED

arquivos_auditados:
  handoff: docs/handoff/H-0075-aplicar-confirmar-persistir-filho-default.md (P02)
  implementacao: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0075.md
  codigo_config_testes: tela/selecao.py, tela/carregamento/conteudo_externo.py, tela/modelo.py, demo/demo.py, os dois JSON estruturais e os três arquivos de teste declarados
  diff: delta causal H-0075 confirmado nos arquivos declarados; o worktree também contém deltas H-0074 e mudanças externas ao manifesto, preservados e excluídos desta atribuição.

compartilhamento_documento_pai: Conforme no caminho normal: sincronização exige mesmo modelo enumerado, mesma referência ConteudoExterno, política dois_niveis_por_foco e pai apresentado; preserva outros pais, políticas e consoles incompatíveis. Achado: a origem passada a alternar(..., modelo=...) não é validada como pertencente ao modelo.

inconsistencia_fail_closed: Conforme. mapa_candidato_filho_default levanta TelaEstruturaInvalida para valores distintos; disponibilidade retorna False, solicitação não é criada, popup não abre e não há escrita/promoção. Teste adversarial confirmou ausência de eleição por foco/ordem.

aplicar_snapshot_popup: Conforme nos casos válidos. Aplicar deriva do mapa coerente versus baseline; cursor/foco não interferem. Snapshot frozen copia baseline/candidato, congela caminho como str e não acompanha mutações posteriores. Popup é schema texto vigente, retorna ABORTADO/CONFIRMADO e não persiste.

persistencia:
  atomicidade: Conforme: deepcopy, validação antes da autoridade, tempfile no mesmo diretório, flush, fsync, os.replace único e limpeza em falha.
  preservacao: Conforme: patch recursivo altera somente filho_default pertinente e preserva _raw/campos desconhecidos; múltiplos pais usam uma substituição.
  falha: Conforme. Falha injetada preserva arquivo, baseline e candidato divergente; Aplicar permanece ativo. Promoção ocorre somente após retorno físico sem exceção.

h0072: Conforme. Três consoles compartilham candidato por pai; alterações A↔B, foco e ordem são irrelevantes; confirmação/reabertura e isolamento de política passaram.

testes_focais: Execução canônica dos focais sem hook falhou na coleta por resíduo histórico. Evidência complementar somente em memória, neutralizando o literal EOF: 33 passed no conjunto declarado expandido explicitamente; conjunto H-0074 ampliado: 37 passed. Demo, ABORTADO, CONFIRMADO, persistência, caminho, H-0072 e regressão H-0074 cobertos.

suite_canonica:
  resultado: 44 errors during collection.
  causalidade: PREEXISTENTE_NAO_CAUSAL. Primeiras classes: SyntaxError por bytes finais literais \\n em tela/carregamento/tela_json.py:528, tela/estilo.py:540, tela/renderizacao/texto_ansi.py:213 e testes históricos. Os bytes finais literais \\n estavam também no HEAD; não são introduzidos pelo delta H-0075.

demo_py:
  classificacao: PREEXISTENTE_NAO_CAUSAL
  evidencia: demo/demo.py termina com literal \\n no estado atual e no HEAD. Remoção apenas em memória permite compilação sintática e os testes de demo exercitam os ramos novos; o diff H-0075 não introduz nem desloca o resíduo.

json_estruturais: Conforme. A remoção do literal EOF era necessária para manter JSON válido após edição. O diff semântico contém somente chip_aplicar e popup_confirmacao_aplicacao_filho_default; não houve reformatação indevida.

validacao_manual: VALIDACAO_MANUAL_NECESSARIA. QA não executou TTY. Após correção do achado técnico, permanece necessária a observação humana de Enter, popup, ABORTADO, CONFIRMADO e reabertura em cópia temporária.

novos_achados:
  - id: QA-IMPL-H0075-001
    requisito: todo console participante, inclusive a origem da sincronização, deve pertencer ao mesmo modelo.
    evidencia: tela/selecao.py:334-347 enumera somente destinos do modelo, mas _origem_satisfaz_predicado() não verifica a pertinência da origem. Caso reproduzido em memória com console clonado fora do modelo alterou a seleção do console real do modelo.
    impacto: chamada válida da API com origem estrangeira contamina um modelo diferente do contexto da origem, violando a identidade documento+pai e o predicado fechado do handoff.
    correcao_necessaria: rejeitar/ignorar a sincronização quando a origem não estiver na enumeração do modelo recebido; adicionar teste regressivo.
