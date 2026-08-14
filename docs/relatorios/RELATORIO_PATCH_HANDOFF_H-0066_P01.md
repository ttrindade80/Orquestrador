# Relatório PATCH_HANDOFF H-0066 P01

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0066
  patch: P01
  predecessor:
    docs/relatorios/RELATORIO_QA_HANDOFF_H-0066.md

resultado:
  status: HANDOFF_PATCHED
  achados_tratados:
    - QA-H0066-001
    - QA-H0066-002
  achados_pendentes: []
  arquivos_alterados:
    - docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0066_P01.md

decisoes:
  formula_aplicar_disponivel: |
    §5.C declara a semântica literal de comparar_candidato_baseline()
    (True=igual/sem alteração pendente; False=divergente/alteração
    pendente) e a ponte UI obrigatória:
    aplicar_disponivel := not EstadoEstiloRuntime.comparar_candidato_baseline()
    (ou equivalente na instância runtime). A implementação não pode
    inferir a inversão. aplicar_disponivel True → candidato_divergente
    considera Aplicar ativo; False → chip declarado e inativo. Única
    fonte: relação candidato×baseline.
  cache_ui: |
    Qualquer armazenamento intermediário de aplicar_disponivel é cache
    de renderização/contexto, nunca autoridade. Recálculo/projeção
    exigido após abertura/F4, Espaço ok, falha/reconciliação com
    recomposição, redraw, resize, Esc filho→pais e restauração na saída
    efetiva. Proibido self.aplicar_disponivel=True residual em A→B→A.
  esc_filho: |
    Esc filho→pais (baseline=A, candidato=B) preserva candidato B,
    baseline A, aplicar_disponivel True e Aplicar ativo; sem solicitação,
    descarte, persistência ou publicação. Distinto da saída efetiva, que
    restaura candidato=A e Aplicar inativo (H-0065).
  snapshot: |
    Solicitação carrega snapshot/cópias do instante de Aplicar, sem
    referências mutáveis retroativas. Imutabilidade observável exigida
    (não obriga deepcopy literal). Teste nominal: após solicitacao_1
    (A/B), mutar candidato para C/A não altera a solicitação. Runtime
    baseline/candidato/global/arquivo intactos; sem popup/persistência/
    publicação nesta fatia.
  arquivos_autorizados_preservados: |
    Lista §12 intacta (fixture h0063, tela/estilo.py, demo/demo.py,
    tela/renderizacao/tela.py com encaminhamento pontual de
    aplicar_disponivel, testes H-0066, IMP-0066 e predecessores
    H-0063/64/65). Predecessores só nas expectativas “sem Aplicar”
    concretamente superadas.

verificacoes_executadas:
  - ocorrencia_literal_formula_not_comparar_candidato_baseline:
      evidencia: >
        H-0066 §5.C, §6, §7, §12 (demo.py), §13 e §16 item 1 trazem
        `not …comparar_candidato_baseline()` / `not comparar_candidato_baseline()`.
  - teste_nominal_esc_filho_pais:
      evidencia: >
        §13 “Esc filho→pais (distinto da saída efetiva)” e §16 item 5;
        preparação A/B, resultado preserva elegibilidade ativa sem
        solicitação/descarte.
  - teste_nominal_snapshot_imutavel:
      evidencia: >
        §5.D reforça imutabilidade observável; §13 “Snapshot imutável
        da solicitação” com solicitacao_1 e mutação posterior C/A;
        §16 item 7.
  - distincao_esc_filho_versus_saida_efetiva:
      evidencia: >
        §5.F e §13 separam Esc filho→pais (preserva) de Esc de saída
        efetiva (restaura candidato e Aplicar inativo).
  - lista_arquivos_autorizados_preservada:
      evidencia: >
        §12 mantém fixture h0063, tela/estilo.py, demo/demo.py,
        tela/renderizacao/tela.py, testes H-0066, IMP-0066 e
        predecessores h0063/h0064/h0065 (demo e tela).
  - git_diff_check:
      comando: >
        git diff --check --
        docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
        docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0066_P01.md
      resultado: limpo
  - stage_vazio:
      comando: git diff --cached --stat
      resultado: vazio
bloqueios: []
```

## Resumo do patch

O handoff H-0066 foi corrigido exclusivamente nos achados
`QA-H0066-001` e `QA-H0066-002` do `RELATORIO_QA_HANDOFF_H-0066.md`.

**QA-H0066-001.** §5.C/§6/§7 fecham a ponte
`aplicar_disponivel := not comparar_candidato_baseline()`, o significado
UI, a proibição de flag residual e os pontos mínimos de recálculo;
exemplo A→B→A fica explícito com comparar/`aplicar_disponivel`/Aplicar.

**QA-H0066-002.** §5.D/§5.F e §13/§16 acrescentam testes nominais de Esc
filho→pais, saída efetiva distinta e snapshot imutável da solicitação,
sem reabrir decisões já aprovadas nem a fronteira posterior.
