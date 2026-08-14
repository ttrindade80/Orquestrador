# Relatório PATCH_HANDOFF H-0065 P02

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0065
  patch: P02
  predecessor:
    docs/relatorios/RELATORIO_QA_HANDOFF_H-0065_P01.md

resultado:
  status: HANDOFF_PATCHED
  achados_tratados:
    - QA-H0065-002
    - QA-H0065-003
  achados_preservados_como_resolvidos:
    - QA-H0065-001
  achados_pendentes: []
  arquivos_alterados:
    - docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P02.md

decisoes:
  estado_pos_saida: |
    No instante imediatamente posterior à saída efetiva, para cada uma das
    quatro categorias: baseline = A, candidato = A, selecoes = A — onde A
    são os presets projetados da baseline. Equivale a
    candidato.<cat>.preset_default == preset em selecoes ==
    baseline.<cat>.preset_default. Nenhum estado abandonado da visita pode
    permanecer em selecoes. Proibido baseline=A, candidato=A, selecoes=B.
  ordem_saida: |
    Sequência única ordenada: (1) recriar candidato da baseline via
    criar_candidato(); (2) reconciliar_selecoes_com_candidato();
    (3) verificar invariável candidato == fonte_semantica_de(selecoes);
    (4) só então popar/retornar/concluir. Qualquer SAÍDA EFETIVA herda a
    mesma sequência; Esc filho→pais, PageUp/PageDown, resize, redraw e
    foco interno não descartam.
  reconciliacao_saida: |
    Preferir reconciliação explícita antes da saída. selecoes permanece
    cache navegacional válido enquanto existir e deve ficar coerente com
    o candidato. Remoção integral do cache só é aceitável se o estado
    deixar de existir de forma inequívoca. Contrato mínimo: nenhum
    selecoes existente pode divergir do candidato.
  invariavel_selecoes: |
    Enquanto estado["selecoes"] existir, deve ser projeção válida do
    candidato. Sem exceções temporais para pós-Espaço, falha, redraw,
    resize ou saída. Intermediários internos de função atômica só se não
    observáveis e se a função restaurar a invariável antes de retornar.
    §9.3 lista todos os pontos, inclusive SAÍDA EFETIVA após recriar
    candidato e antes de concluir.
  F4_defensivo: |
    Cada F4 cria/reinicializa candidato da baseline e reconcilia selecoes,
    mesmo após saída já ter restaurado candidato==baseline e
    selecoes==baseline. Não é contradição: isolamento entre visitas.
    Teste de F4 pós-saída é prova defensiva distinta do descarte original.

verificacoes_executadas:
  - id: ocorrencias_reconciliar
    metodo: rg reconciliar_selecoes_com_candidato no handoff
    evidencia: múltiplas ocorrências em §§4.5–4.6, 7.1, 9.2–9.3, 10, 12.2–12.3, 18–19
    resultado: OK
  - id: saida_nos_pontos_reconciliacao
    metodo: leitura de §9.3
    evidencia: lista inclui abertura/F4, Espaço ok, falha Espaço, render/redraw, resize e SAÍDA EFETIVA após recriar candidato
    resultado: OK
  - id: teste_pos_esc_antes_f4
    metodo: leitura de §19 "Saída efetiva — instante exato"
    evidencia: assert imediato baseline/candidato/selecoes == A antes de qualquer novo F4; proíbe prova só via reabertura
    resultado: OK
  - id: esc_filho_vs_saida
    metodo: leitura de §§12.1, 12.2 e 19
    evidencia: Esc filho→pais preserva candidato=B/selecoes=B; saída efetiva restaura A/A/A; testes separados
    resultado: OK
  - id: qa001_preservado
    metodo: leitura de §7.1 e metadados P02
    evidencia: Fases A–D e direção preset→candidato→projeção intactas; QA-H0065-001 listado como preservado
    resultado: OK
  - id: git_diff_check
    metodo: git diff --check nos dois artefatos do P02
    evidencia: exit 0, sem erros de whitespace
    resultado: OK
  - id: stage_vazio
    metodo: git diff --cached --name-only
    evidencia: vazio
    resultado: OK

bloqueios: []
```

## Resumo

P02 fecha exclusivamente QA-H0065-002 e QA-H0065-003. A saída efetiva passa a
ser sequência ordenada com reconciliação de `selecoes` antes do pop; o estado
pós-saída exige `baseline=candidato=selecoes=A`; §9.3 inclui a saída; testes
exigem prova imediata pós-Esc, multi-categoria, cache divergente artificial e
F4 defensivo separado. QA-H0065-001 permanece resolvido e não reaberto. Lista
de implementação e fronteira de Aplicar/preview/persistência intactas.
