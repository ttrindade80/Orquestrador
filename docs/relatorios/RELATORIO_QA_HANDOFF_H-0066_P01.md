# Relatório QA_HANDOFF H-0066 P01

```yaml
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0066
  revisao: P01
  raiz:
    docs/relatorios/RELATORIO_QA_HANDOFF_H-0066.md
  predecessor_imediato:
    docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0066_P01.md
  handoff: docs/handoff/H-0066-acao-aplicar-candidato-estilo.md

resultado:
  status: H1_HANDOFF_APPROVED
  achados_retestados:
    - QA-H0066-001
    - QA-H0066-002
  achados_resolvidos:
    - QA-H0066-001
    - QA-H0066-002
  achados_pendentes: []
  novos_achados: []
  bloqueios: []
  estado_git:
    branch: master
    head: 77bd8bf3772985325bc51a850f7c6d76d61ad573
    stage_vazio: true
    arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0066_P01.md
    outros_arquivos_alterados_nesta_etapa: []

pontos_especiais:
  formula_aplicar_disponivel: >
    RESOLVIDO. §5.C/§6/§7/§12/§13/§16 fecham literalmente
    comparar True=igual/sem pendência; False=divergente/pendente; e
    aplicar_disponivel := not EstadoEstiloRuntime.comparar_candidato_baseline()
    (ou equivalente na instância). Código confirma: comparar é dict==dict;
    barra usa aplicar_disponivel como candidato_divergente (True=ativo).
    Sem inversão semântica: True ativa Aplicar; False mantém declarado inativo.
  fonte_elegibilidade: >
    Única fonte candidato×baseline. aplicar_disponivel é cache/projeção/
    contexto. A→B→A → inativo→ativo→inativo sem flag residual (§5.C/§5.G).
  recalc: >
    Pontos mínimos §5.G: F4/abertura; Espaço ok; falha+recomposição;
    redraw; resize; Esc filho→pais; restauração na saída efetiva enquanto
    o contexto existir. Sem arquitetura nova.
  esc_filho: >
    RESOLVIDO. §5.F + §13/§16 item 5: baseline=A, candidato=B, Aplicar
    ativo; Esc filho→pais preserva A/B, aplicar_disponivel True, Aplicar
    ativo; sem solicitação/descarte/persistência/publicação. Separado da
    saída efetiva.
  saida_efetiva: >
    Sem regressão H-0065. Antes A/B ativo; depois A/A inativo (§5.F/§13).
    Restauração deriva de candidato×baseline, não de flag manual.
  snapshot: >
    RESOLVIDO. §5.D + §13/§16 item 7: solicitacao_1 (A/B) permanece A/B
    após mutação runtime para C/A. Imutabilidade observável exigida;
    deepcopy não obrigatório se equivalente. Emitir Aplicar não altera
    baseline/candidato/global/arquivo; sem persistência/publicação/popup.
  fronteira_posterior: >
    Intacta (§2/§15/§17): popup, confirmar/cancelar, CONFIRMADO/ABORTADO,
    persistência, publicação, override local, demo integrada.
  arquivos_autorizados: >
    §12 preservada: fixture h0063; tela/estilo.py; demo/demo.py;
    tela/renderizacao/tela.py; testes H-0066; IMP-0066; predecessores
    nominais. Consumir sem alterar contexto_execucao e barra_menus.
  testes_predecessores: >
    Autorização restrita a ausência de Aplicar/chip_aplicar/"Aplicar" no
    quadro/solicitar_aplicacao. Proibido enfraquecer baseline/global/
    arquivo/popup/persistência/publicação/preview real.
  chip_foco_barra: >
    Chip sempre presente; ativo/inativo por divergência; Enter contextual;
    inativo=no-op. Sem dependência nova de foco (pais/filhos). Espaço=
    seleção filho. Posição [⏎]; Páginas quando aplicável; Ajuda último;
    sem ITEM-0032.
  evidencia_p01: >
    RELATORIO_PATCH_HANDOFF_H-0066_P01 registra fórmula literal, Esc
    filho, snapshot, distinção Esc×saída, lista §12, git diff --check e
    stage vazio — alinhado ao handoff atual.
  suficiencia: >
    Implementador executa sem inventar inversão do comparador, fonte de
    elegibilidade, A→B→A, Esc filho vs saída, snapshot ou fronteira
    posterior.
```

## Veredito

Reteste de `QA-H0066-001` e `QA-H0066-002` no H-0066 pós-P01:
ambos resolvidos; nenhum achado material novo.
Status: `H1_HANDOFF_APPROVED`.
