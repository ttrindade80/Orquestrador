# Relatório PATCH_HANDOFF H-0065 P01

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0065
  patch: P01
  predecessor:
    docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md

resultado:
  status: HANDOFF_PATCHED
  achados_tratados:
    - QA-H0065-001
    - QA-H0065-002
    - QA-H0065-003
  achados_pendentes: []
  arquivos_alterados:
    - docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P01.md

decisoes:
  fonte_semantica: |
    Declarado literalmente que o candidato runtime é a fonte semântica única
    do preset escolhido. `estado["selecoes"]` deixa de poder ser autoridade:
    existe apenas como projeção/cache navegacional da política
    `dois_niveis_por_foco`. Estado candidato=B com selecoes=A é inválido.
  projecao_selecoes: |
    Operação conceitual obrigatória `reconciliar_selecoes_com_candidato()`:
    lê os quatro `preset_default` do candidato, localiza dinamicamente o
    filho em cada pai, reconstrói a escolha exclusiva, substitui `selecoes`,
    sem tocar candidato/baseline/global/arquivo e sem mapa de nomes.
    Reconciliação exigida na abertura, após Espaço ok, após falha, antes de
    render/redraw com residual e após resize se `selecoes` for reconstruído.
    Inconsistência de projeção é falha de invariável, não silêncio.
  protocolo_espaco: |
    Protocolo atômico fechado em fases A–D: preparar (sem alterar selecoes)
    → mutar cópia e materializar → só então reconciliar selecoes no sucesso;
    em falha, candidato anterior intacto e selecoes reconciliado dele.
    Direção: preset solicitado → candidato aceito → projeção navegacional.
    Commit observável só com candidato e selecoes coerentes; atomicidade no
    controlador/runtime/dispatch, não no renderer.
  falha: |
    Validação/materialização falha sem consolidar o novo filho em selecoes;
    sem rollback inventado de persistência/global (nunca mudaram); evento
    termina sem mutação parcial observável.
  esc_saida: |
    Esc que efetivamente sai da tela descarta imediatamente todas as
    diferenças não confirmadas: abandona o candidato da visita, recria via
    `criar_candidato()` a partir da baseline, sem persistir/publicar/alterar
    baseline/global, e só então conclui a saída. Estado pós-saída:
    candidato == baseline. Qualquer SAÍDA EFETIVA equivalente herda a regra;
    Esc filho→pais, paginação, resize e foco interno não descartam.
  reabertura: |
    F4 continua criando/reinicializando candidato da baseline mesmo após
    descarte na saída (dupla garantia intencional). Após criar, reconciliar
    selecoes; escolhas iniciais refletem a baseline vigente.

verificacoes_executadas: []
bloqueios: []
```

## Resumo do patch

O handoff H-0065 foi corrigido exclusivamente nos três achados do
`RELATORIO_QA_HANDOFF_H-0065.md`.

**QA-H0065-001.** §§7 e 17 fecham ordem obrigatória de Espaço (Fases A–D),
fronteira de commit observável e proibição de consolidar escolha antes do
candidato aceito.

**QA-H0065-002.** §9 declara fonte semântica única, define
`reconciliar_selecoes_com_candidato()`, pontos de reconciliação, falha
extraordinária de projeção, troca sucessiva e pais independentes.

**QA-H0065-003.** §§4.5, 4.6 e 12 fixam descarte imediato na saída efetiva,
preservam Esc filho→pais sem desfazer candidato, mantêm dupla garantia de
F4 e estendem a regra a qualquer saída efetiva.

§19 passou a exigir testes de atomicidade (sucesso/falha/janela), fonte
única com divergência artificial, redraw/resize, instante exato da saída e
Esc filho separado. Lista de arquivos autorizados preservada; renderer
permanece fora. Escopo de Aplicar/preview/persistência/publicação intacto.
