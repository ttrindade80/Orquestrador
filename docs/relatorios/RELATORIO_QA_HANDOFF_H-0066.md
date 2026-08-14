# Relatório QA_HANDOFF H-0066

```yaml
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0066
  handoff: docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
  item: ITEM-0010
  adr: ADR-0046

resultado:
  status: H2_HANDOFF_PATCH_REQUIRED
  verificacoes_executadas:
    - Leitura integral de H-0066, ADR-0046, H-0061, H-0065,
      contrato_estilo, contrato_barra_de_menus, 10_ESTILO, 31_BARRA.
    - Leitura focal de H-0063 e H-0064.
    - Inspeção de comparar_configuracoes_estilo /
      comparar_candidato_baseline, aplicar_disponivel,
      candidato_divergente, renderizar_tela, fixture H-0063,
      precedente h0062_estilo.json e testes predecessores.
    - Estado Git somente leitura; stage vazio.
  achados:
    - id: QA-H0066-001
      requisito: >
        Injeção de aplicar_disponivel deve refletir divergência
        (chip ativo), sem inverter o booleano de comparação.
      autoridade: >
        H-0066 §5.C/§7/§12; barra_menus.py regra candidato_divergente;
        carregamento/estilo.py comparar_candidato_baseline;
        precedente H-0062 §9.
      evidência: >
        Código: comparar retorna True iff candidato==baseline
        (dict==dict). regra candidato_divergente ativa o chip quando o
        valor é True; aplicar_disponivel é alias desse valor. H-0066
        mapeia comparar→Aplicar corretamente, mas ao mandar “injetar
        aplicar_disponivel” não fecha a fórmula
        aplicar_disponivel = not comparar_candidato_baseline().
      impacto: >
        Implementador pode injetar o retorno bruto de comparar e
        inverter ativo/inativo.
      correção_necessária: >
        Declarar explicitamente a ponte:
        aplicar_disponivel := not EstadoEstiloRuntime.comparar_candidato_baseline().
      camada_responsável: H-0066 (documentação de elegibilidade/UI).
    - id: QA-H0066-002
      requisito: >
        Cobertura automatizada de Esc filho→pais (preserva
        candidato/elegibilidade) e de snapshot imutável da solicitação
        após mutações posteriores.
      autoridade: >
        Prompt QA §21; H-0066 §5.D/§5.F; ADR-0046 §4/§7.
      evidência: >
        Comportamentos estão no texto normativo, mas §13 só exige Esc
        de saída efetiva e não lista caso Esc filho nem asserção de que
        mutar candidato após Aplicar não altera a solicitação já emitida.
      impacto: >
        Aceite pode passar sem provar preservação navegacional da
        elegibilidade nem imutabilidade do snapshot.
      correção_necessária: >
        Acrescentar testes mínimos nominais: Esc filho com candidato
        divergente preserva elegibilidade ativa; após solicitação,
        mutação posterior do candidato não altera cópias na solicitação.
      camada_responsável: H-0066 §13/§16.
  bloqueios: []
  estado_git:
    branch: master
    head: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage_vazio: true
    arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0066.md
    outros_arquivos_alterados_nesta_etapa: []

pontos_especiais:
  existencia_aplicar: >
    DETERMINADO. Chip sempre declarado; sem divergência permanece
    visível e inativo (cor_inativo); não some. Forma derivável:
    chip_aplicar / ⏎ / Aplicar / candidato_divergente (precedente H-0062
    + contratos §8.1/§10.1). Sem literal inventado.
  comparador_candidato_baseline: >
    COMPROVADO. True = equivalência semântica; False = divergência.
    H-0066 §5.C está correto; não há inversão na afirmação do handoff.
  elegibilidade: >
    Sem flag residual; A→B→A fechado; quatro categorias corretas.
    Lacuna só na ponte UI (QA-H0066-001).
  enter: >
    Enter=Aplicar contextual na tela de Estilo; inativo=no-op; não
    Todos/Executar; não substitui Espaço; não redefine outras telas.
  foco_precedencia: >
    Global à tela enquanto Estilo ativa, independente do toroide
    pais/filhos — inequívoco.
  solicitacao_estrutural: >
    Fronteira correta: só intenção/solicitação com cópias de candidato e
    baseline; sem popup/CONFIRMADO/ABORTADO/persistência/publicação.
    Partição operacional compatível com ADR (origem da transição).
    Sem literais novos.
  snapshot: >
    Exigido normativamente (§5.D); falta teste explícito (QA-H0066-002).
    Cópias alinhadas a deepcopy já exposto pelo runtime.
  esc: >
    Antes de confirmação: Esc filho preserva; saída efetiva descarta
    (H-0065). Aplicar nesta fatia não é confirmação.
  barra: >
    Inserção na posição [⏎]; preserva Páginas/?/Ajuda último; sem
    ITEM-0032; inativo via mecanismo canônico.
  fronteira_posterior: >
    Explicitamente fora: popup, confirmação, persistência, publicação,
    override, demo integrada.
  arquivos_autorizados: >
    Mínimo coerente. tela/renderizacao/tela.py é NECESSÁRIO:
    renderizar_tela/_geometria não encaminham aplicar_disponivel a
    _preparar_contexto_navegacao (que zera o campo). Fixture h0063
    compartilhada adequada, com preservação H-0063/64/65.
  testes_predecessores:
    demo/teste_demo_estilo_h0063.py: NECESSARIO
      (Ausência de Aplicar/chip_aplicar em
      test_ajuda_ultimo_e_sem_aplicar… e "Aplicar" not in quadro).
    demo/teste_demo_estilo_h0064.py: NECESSARIO
      ("Aplicar" not in quadro).
    demo/teste_demo_estilo_h0065.py: NECESSARIO
      (ausência no quadro/chips;
      test_sem_aplicar_nem_preview_real_no_quadro).
    tela/teste_estilo_h0063.py: NECESSARIO
      (not hasattr(..., solicitar_aplicacao) e fronteira sem ação).
    tela/teste_estilo_h0065.py: NECESSARIO
      (idem + test_sem_aplicar_persistencia_ou_publicacao).
  validacao_manual: >
    Nenhuma — corretamente automatizável (chips/estado_ativo_chips,
    solicitação, arquivo/baseline/global).
```
