tipo_execucao: QA_ALTERACAO_DECLARATIVA
objeto: H-0053
achado_retestado:
  - VM-H0053-R02-001
resultado:
  rotulo_Esc: "APROVADO: configuração materializada declara [Esc] Sair e não declara [Esc] Voltar."
  coerencia_funcional: "APROVADO: H-0053 inicia com pilha_telas vazia; Esc define saindo = True e encerra a demonstração."
  preservacao_demais_chips: "APROVADO: [✥] Navegar, [␣] Expandir/Recolher e [?] Ajuda permanecem preservados, com a ordem relativa mantida."
testes:
  pytest_demo: "11 passed in 0.77s"
  pytest_suite: "1074 passed in 28.07s"
  git_diff_check: passed
status: DECLARATIVE_CHANGE_APPROVED
proxima_acao: REVALIDACAO_MANUAL_FOCAL
stage: vazio
commit: false
