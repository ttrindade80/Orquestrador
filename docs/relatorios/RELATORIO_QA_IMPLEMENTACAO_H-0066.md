# Relatório QA de Implementação — H-0066

```yaml
rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0066
  handoff: docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
  implementacao: docs/relatorios/IMP-0066-acao-aplicar-candidato-estilo.md
  item: ITEM-0010
  adr: ADR-0046
  perfil_auditor: auditor independente da implementacao
  contexto_agente: LIMPO

resultado:
  status: I1_IMPLEMENTATION_APPROVED
  verificacoes_executadas:
    - leitura integral H-0066 / IMP-0066 e leitura focal das infraestruturas
      consumidas (contexto_execucao.aplicar_disponivel,
      barra_menus.candidato_divergente, comparar_candidato_baseline)
    - inspeção dos arquivos do manifesto H-0066 e das atualizações
      predecessoras autorizadas (incl. autorização adicional de
      tela/teste_estilo_h0064.py)
    - git: stage vazio; config/estilo.json sem delta; tela.py = +2 linhas
      de encaminhamento de aplicar_disponivel
    - probes independentes: fórmula literal; chip sempre presente;
      Enter contextual em pais e filhos; snapshot imutável;
      resize 62/80/120 com linhas.maximo: 3 + preferir_menor_numero;
      ausência de popup/persistência/publicação/origem H-0062
    - pytest H-0066; regressão H-0063/H-0064/H-0065; suíte completa
  testes:
    h0066: 27 passed
    regressao_h0063_h0064_h0065: 64 passed
    suite_completa: 1269 passed
  achados: []
  validacao_manual_necessaria: []
  bloqueios: []
  desvios_avaliados:
    - id: DESVIO-LINHAS-MAXIMO-H0066
      decisao: aceito na fronteira de H-0066; sem achado
      evidencia: >
        O 6º chip (Aplicar) estoura o layout de 2 linhas em 62 colunas no
        nível de filhos. A fixture h0063 declara linhas.maximo: 3 com
        preferir_menor_numero: true (resto idêntico ao default do
        renderer, cujo maximo default permanece 2). Probe: 120→1 linha,
        80→2, 62→3; resize H-0063 (62x20) permanece sem
        "Aumente a janela". Nenhum código de barra_menus/renderer foi
        redesenhado além do encaminhamento autorizado em tela.py.
    - id: AUTORIZACAO-ESCOPO-TESTE-H0064
      decisao: aceito; sem achado
      evidencia: >
        tela/teste_estilo_h0064.py atualizou somente a expectativa
        histórica hasattr(solicitar_aplicacao); demais garantias de
        baseline/candidato/global/arquivo preservadas. Autorização
        adicional do gerente registrada no IMP.

pontos_especiais:
  formula_aplicar_disponivel: >
    aprovado; ControladorTelaEstilo.aplicar_disponivel =
    not runtime.comparar_candidato_baseline(), property recalculada a
    cada consulta. Testes e probe confirmam igualdade à ponte e
    desigualdade ao retorno bruto de comparar; A→B→A sem flag residual.
  chip_sempre_presente: >
    aprovado; chip_aplicar declarado (tecla ⏎, texto Aplicar,
    regra_ativo candidato_divergente), antes de chip_ajuda. Presente
    com candidato==baseline (inativo/cor_inativo) e com divergência
    (ativo). Existência estática × ativo/inativo dinâmico respeitados.
  enter_contextual: >
    aprovado; demo.py intercepta Enter na tela H-0063 antes de
    Todos/Executar, em qualquer nível. Probe: Enter inativo = no-op;
    Enter ativo no nível dos pais (após Esc filho→pais com candidato
    divergente) produz SolicitacaoAplicacaoEstilo. Não substitui Espaço.
  solicitacao_estrutural_snapshot: >
    aprovado; solicitar_aplicacao() retorna None se inativo; se ativo,
    SolicitacaoAplicacaoEstilo(baseline, candidato) frozen + deepcopy.
    Não abre popup, não confirma, não persiste, não publica; baseline/
    candidato/global/arquivo intactos. Snapshot permanece A/B após
    mutação posterior do runtime.
  solicitacao_sem_arquitetura_h0062: >
    aprovado; SolicitacaoAplicacaoEstilo reimplementada em tela/estilo.py
    com campos apenas baseline/candidato — sem identidade de origem
    H-0062, sem shell popup-like, sem restauração do fluxo substituído.
    Consome infra vigente (aplicar_disponivel / candidato_divergente)
    sem redesenho.
  linhas_maximo_3: >
    aprovado como desvio justificado na fixture autorizada; ver
    DESVIO-LINHAS-MAXIMO-H0066. Dentro da fronteira: preserva resize
    H-0063 após introdução do chip, sem alterar o default global do
    renderer.
  tela_py_encaminhamento: >
    aprovado; diff de tela/renderizacao/tela.py limita-se a aceitar e
    repassar aplicar_disponivel até _preparar_contexto_navegacao
    (padrão espelhado de executar_disponivel). Sem redesign.
  testes_predecessores: >
    aprovado; H-0063/H-0064/H-0065 (tela+demo) atualizados só nas
    expectativas "sem Aplicar"/ausência de chip_aplicar/solicitar_aplicacao
    superadas. Invariantes de baseline, global, arquivo, ausência de
    popup/persistência/publicação/preview real preservados. Nome de
    alguns testes de fronteira foi alinhado à nova presença de Aplicar
    sem enfraquecer o restante.
```

## Síntese

H-0066 entrega a fatia AÇÃO APLICAR sobre a tela normal vigente
(H-0063/H-0064/H-0065): elegibilidade derivada exclusivamente de
`not comparar_candidato_baseline()`, chip `[⏎] Aplicar` sempre presente
(ativo/inativo), Enter contextual produzindo somente o snapshot imutável
`SolicitacaoAplicacaoEstilo`, sem confirmação/popup/persistência/publicação.

O worktree permanece sujo com artefatos de etapas anteriores do ITEM-0010;
o QA não os alterou. Stage vazio; `config/estilo.json` sem delta. Único
artefato criado por esta etapa: este relatório.
