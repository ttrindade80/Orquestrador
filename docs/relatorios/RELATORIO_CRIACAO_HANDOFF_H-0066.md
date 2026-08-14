# Relatório — Criação do Handoff H-0066

```yaml
rastreabilidade:
  etapa: CRIAR_HANDOFF
  objeto: H-0066
  item: ITEM-0010
  adr: ADR-0046
  predecessor: H-0065
```

## Papel executado

Autoria documental exclusiva do handoff H-0066. Nenhum código, ADR,
contrato, nomenclatura ou backlog foi alterado nesta etapa. Nenhum stage,
commit ou push foi realizado.

## Autoridades lidas

Integralmente: `ADR-0046`, `H-0061`, `H-0065`, `contrato_estilo.md`,
`10_ESTILO.md`, `contrato_barra_de_menus.md` (incl. §10.1),
`31_BARRA_DE_MENUS_E_CHIPS.md` §4.5.1. Focalmente: `H-0063`, `H-0064`.
Código inspecionado (somente leitura): `tela/carregamento/estilo.py`
(`comparar_candidato_baseline`), `tela/estilo.py`, `demo/demo.py`,
shell H-0063, `contexto_execucao.aplicar_disponivel`,
`barra_menus.candidato_divergente`, precedente declarativo H-0062.

## Análise Aplicar

```yaml
analise_aplicar:
  existencia_acao: >
    DETERMINADO. Chip declarado existe sempre; ativo/inativo e dinamico.
    Sem divergencia permanece inativo (cor_inativo), nao ausente.
    Forma derivavel: chip_aplicar / tecla ⏎ / texto Aplicar /
    regra_ativo candidato_divergente.
  elegibilidade: >
    DETERMINADO. comparar_candidato_baseline True → inativo;
    False → ativo. Derivado de candidato×baseline H-0061; sem flag residual.
  papel_enter: >
    DETERMINADO. Enter aciona Aplicar na tela de Estilo (contextual);
    inativo = no-op; nao substitui Espaco; nao vira Todos/Executar.
  resultado_da_acao: >
    DETERMINADO na particao. Ativo produz somente solicitacao/transicao
    estrutural imutavel (copias de candidato e baseline) para etapa
    posterior; nao abre demo/popup; nao persiste; nao publica.
    Compativel com ADR: Aplicar e origem da transicao; confirmacao e destino.
  candidato_antes_confirmacao: >
    DETERMINADO. Acionar Aplicar nao altera baseline/global/arquivo e nao
    destroi o candidato.
  esc: >
    DETERMINADO. Sem confirmacao aberta, Esc permanece H-0065
    (navegacional ou descarte na saida efetiva).
  retorno_a_baseline: >
    DETERMINADO. A→B→A reavalia elegibilidade; sem flag residual.
  literal_evento: >
    Sem literais ADR novos (APPLY_REQUESTED etc.). Efeito estrutural basta.
  suficiencia_documental: >
    SUFICIENTE. Nenhum ponto necessario admite duas semanticas materiais
    sem resolucao normativa; divisao gerencial e compativel com ADR-0046.
```

## Resultado

```yaml
resultado:
  status: HANDOFF_CREATED
  handoff: docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
  capacidade:
    - elegibilidade_aplicar_candidato_baseline
    - chip_enter_aplicar_contextual
    - solicitacao_estrutural_para_confirmacao_posterior
  arquivos_implementacao_autorizados:
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
    - tela/estilo.py
    - demo/demo.py
    - tela/renderizacao/tela.py
    - tela/teste_estilo_h0066.py
    - demo/teste_demo_estilo_h0066.py
    - docs/relatorios/IMP-0066-acao-aplicar-candidato-estilo.md
    - demo/teste_demo_estilo_h0063.py  # so expectativas "sem Aplicar"
    - demo/teste_demo_estilo_h0064.py  # so expectativas "sem Aplicar"
    - demo/teste_demo_estilo_h0065.py  # so expectativas "sem Aplicar"
    - tela/teste_estilo_h0063.py       # so expectativas "sem Aplicar"
    - tela/teste_estilo_h0065.py       # so expectativas "sem Aplicar"
  testes_requeridos:
    - baseline_igual_aplicar_inativo_enter_noop
    - candidato_diferente_aplicar_ativo_so_solicitacao
    - volta_A_B_A_sem_flag_residual
    - quatro_categorias_afetam_elegibilidade
    - setas_nao_afetam_elegibilidade
    - resize_redraw_preservam_derivado
    - esc_saida_preserva_descarte_h0065
    - fronteiras_sem_persistencia_publicacao_popup_demo
    - regressao_h0063_h0064_h0065_e_suite
  fora_de_escopo:
    - popup_de_confirmacao
    - CONFIRMADO_ABORTADO
    - demonstracao_integrada_override_local
    - persistencia
    - publicacao
    - preview_real_global
    - ITEM-0032
  bloqueios: []
```

## Estado Git (somente leitura)

```text
branch: master
HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
staged: (vazio)
```

Worktree acumulado pré-existente preservado; stage permanece vazio. Artefatos
criados nesta etapa: apenas o handoff H-0066 e este relatório.
