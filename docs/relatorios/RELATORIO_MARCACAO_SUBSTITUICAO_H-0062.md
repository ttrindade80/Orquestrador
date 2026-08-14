# Relatório de marcação de substituição — H-0062

```yaml
rastreabilidade:
  etapa: MARCAR_HANDOFF_SUBSTITUIDO
  objeto: H-0062
  sucessor: H-0063
  artefato_alterado:
    docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md

mecanismo:
  status_aplicado: substituido
  sucessor_nomeado: H-0063
  campo_substituido_por_criado: false
  vinculo_reverso_no_sucessor:
    campo: rastreabilidade.handoff_historico
    valor: H-0062

execucao:
  status: HANDOFF_MARKED_SUBSTITUIDO
  arquivos_alterados:
    - docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_MARCACAO_SUBSTITUICAO_H-0062.md

resultado:
  delta_material: []
  verificacoes_executadas:
    - H-0062 contém status: substituido e nomeia H-0063.
    - H-0063 referencia H-0062 em rastreabilidade.handoff_historico.
    - Não existe campo substituido_por nos handoffs verificados.
    - O diff de H-0062 é focal à marcação documental.
  preservacoes_confirmadas:
    - H-0062 foi preservado além da marcação focal de status e substituição.
    - H-0063 não foi alterado.
    - H-0062 não foi reescrito além da marcação focal.
  bloqueios: []
```

H-0063 não foi alterado. H-0062 não foi reescrito além da marcação focal e
nenhum campo `substituido_por` foi criado.
