# Relatório QA Handoff H-0062

## rastreabilidade

```yaml
etapa: QA_HANDOFF
objeto: H-0062
artefato_auditado: docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md
```

## resultado

```yaml
status: H2_HANDOFF_PATCH_REQUIRED
verificacoes_executadas:
  - leitura integral do handoff, ADR-0046, contratos e nomenclaturas do manifesto fechado, além de config/estilo.json
  - busca focal da política dois_niveis_por_foco e da entrada global/F4
  - leitura focal da infraestrutura de estilo e dos pontos vigentes de decoder/dispatcher
achados:
  - id: H0062-QA-001
    requisito_violado: barra de menus deve reutilizar a obrigatoriedade contratual de [?] Ajuda
    evidencia_focal: "H-0062 §6 condiciona [?] Ajuda a 'se exigido pelo schema vigente'; contrato_barra_de_menus.md §§8.2.1 e 20 tornam o chip obrigatório em toda tela, sempre ativo e último; nomenclatura/31 §4.3 confirma a mesma autoridade."
    impacto: "A implementação pode omitir o chip universal na tela de Estilo, produzindo barra incompatível com o contrato vigente, embora a ação F1/Ajuda permaneça corretamente fora do ciclo."
    correcao_necessaria: "Remover a condicionalidade e exigir explicitamente [?] Ajuda como chip visual canônico, sempre ativo e último; manter fora apenas a ação F1/Ajuda."
bloqueios: []
```
