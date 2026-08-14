rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0070
  handoff: docs/handoff/H-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md

resultado:
  status: H1_HANDOFF_APPROVED
  achados: []
  notas:
    - O handoff materializa integralmente as decisões fechadas para filhos, amostras, chips de uma tecla, presets delimitados e os três formatos multitecla.
    - A aplicação na Barra real, a medição visual sem ANSI, runtime, resize, paginação afetada, regressões genéricas e preservações funcionais estão explicitamente cobertas.
    - A discriminação estrutural reutiliza os campos e mecanismos vigentes, sem novo preset, schema, política, ordem ou arquitetura.
  bloqueios: []

exequibilidade:
  arquivos_autorizados: suficientes_e_minimos
  testes: cobertura A-I, incluindo paginação diretamente afetada, regressões H-0063–H-0069, popup, suíte completa e apresentações genéricas.
  demonstracao: reproduzível sem alterar config/estilo.json, com candidato runtime e fixture integrada H-0069.
  validacao_manual_final: TTY posterior obrigatória, incluindo chips, Barra real, runtime, resize, Aplicar, ABORTADO, CONFIRMADO e retorno à Estilo.
