# Relatório QA_HANDOFF H-0065

rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0065
  handoff: docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  item: ITEM-0010
  adr: ADR-0046

resultado:
  status: H2_HANDOFF_PATCH_REQUIRED
  verificacoes_executadas:
    - Leitura integral do H-0065, ADR-0046, H-0061, H-0063 e H-0064.
    - Leitura focal do contrato de estilo e da nomenclatura de estilo.
    - Inspeção das primitivas runtime, do controlador e do dispatch permitido.
    - Auditoria de ciclo de vida, categorias, mapeamento, presets dinâmicos,
      amostras, preview, Aplicar, persistência e publicação.
    - Auditoria dos testes obrigatórios, regressões e validação manual.
    - Estado Git verificado; stage vazio no início da etapa.
  achados:
    - id: QA-H0065-001
      requisito: Espaço deve ser uma transição atômica e falha inválida não pode deixar escolhido e candidato divergentes.
      autoridade: ADR-0046 §7; contrato_estilo.md §§3.8, R-11, R-12; H-0061 §§6–7; H-0065 §§7 e 17.
      evidência: H-0065 exige a mesma transição e preserva o candidato em falha, mas declara que não prescreve qual suboperação ocorre primeiro. Também divide a evolução entre controlador e dispatch, sem definir fronteira de commit ou rollback de `selecoes`.
      impacto: Um implementador pode consolidar a escolha navegacional antes da validação/materialização e terá de inventar como desfazê-la quando o candidato for recusado.
      correção necessária: Definir a ordem e o protocolo: operar em cópia, validar/materializar, comitar o candidato e somente então comitar a escolha; ou especificar transação/rollback observável para ambos, incluindo o caminho de erro.
      camada responsável: H-0065, coordenação controlador/dispatch.
    - id: QA-H0065-002
      requisito: O candidato deve ser a referência semântica única do preset escolhido; eventual projeção local precisa de reconciliação determinística.
      autoridade: ADR-0046 §§3–4; H-0063 §§4.4–5; H-0065 §9.
      evidência: H-0065 chama o candidato de referência semântica, mas mantém `estado["selecoes"]` como mecanismo canônico de renderização/navegação e só especifica sincronização na formação e em Espaço bem-sucedido. Não há regra geral de reconciliação candidato→seleções para divergência preexistente, redraw ou falha.
      impacto: Permanecem duas representações capazes de sustentar A/B, permitindo estado observável divergente em um caminho não coberto pelo evento normal.
      correção necessária: Declarar `selecoes` como projeção/cache não autoritativa, definir o candidato como fonte semântica e fixar a operação determinística de projeção/reconciliação, inclusive após erro e antes de renderizar.
      camada responsável: H-0065, controlador/integração de estado.
    - id: QA-H0065-003
      requisito: Saída sem Aplicar deve descartar o candidato não confirmado e restaurar o estado transitório da baseline.
      autoridade: ADR-0046 §§7 e 9; contrato_estilo.md §3.8/R-12; H-0065 §§4.5–4.6 e 12.
      evidência: H-0065 afirma descarte na saída, mas depois deixa aberto se ele ocorre no Esc ou somente pela recriação na próxima abertura, exigindo apenas o efeito observado na reabertura. O runtime de H-0061 mantém o candidato até `criar_candidato()` ser chamado.
      impacto: O estado de `RuntimeEstilo` imediatamente após sair pode conter mutações não confirmadas, e o implementador não sabe quando o descarte deve ocorrer nem qual estado deve ser testado.
      correção necessária: Fixar o ponto de descarte no Esc de saída, ou declarar normativamente a retenção até F4 seguinte e delimitar sua observabilidade; exigir teste do estado no instante definido, além da reabertura.
      camada responsável: H-0065, integração de saída/ciclo de vida.
  bloqueios: []
  estado_git:
    branch: master
    head: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage_vazio: true
    arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
    outros_arquivos_alterados_nesta_etapa: []
    observacao: Havia alterações e arquivos não rastreados preexistentes no worktree; não foram tratados nesta etapa.

pontos_especiais:
  ciclo_vida: Nascimento, baseline, F4, reabertura e preservação de baseline/global/arquivo estão documentalmente encaminhados; o momento do descarte na saída é o achado QA-H0065-003.
  fonte_escolhido: A intenção candidato→escolhido está declarada, mas a coexistência de `selecoes` canônico e candidato carece da reconciliação determinística do achado QA-H0065-002.
  atomicidade: A primitiva H-0061 protege o candidato; a atomicidade conjunta com a escolha navegacional não está implementavelmente fechada, conforme QA-H0065-001.
  falha_invalida: O candidato anterior é preservado pela primitiva existente e o teste é exigido, mas o rollback/reconciliação da escolha não está definido.
  esc_saida: Filhos→pais preserva a escolha; pais→saída tem descarte temporalmente ambíguo.
  fronteira_aplicar: H-0065 proíbe preview real, Aplicar/Enter, popup, confirmação, persistência e publicação; a fronteira é coerente com as autoridades.
  arquivos_autorizados: A lista é suficiente, mínima e coerente: `tela/estilo.py` e `demo/demo.py` são os pontos corretos para controlador/ciclo F4-Esc/dispatch; não há necessidade estrutural de alterar renderer.
  testes: Há cobertura nominal para inicialização, setas, quatro categorias, troca sucessiva, pais independentes, inválido, Esc, reabertura e regressões H-0063/H-0064/suíte. Faltam as decisões executáveis apontadas nos três achados.
  validacao_manual: Corretamente essencialmente automatizável; não há requisito físico novo que justifique gate TTY.
