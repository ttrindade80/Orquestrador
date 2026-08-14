# Relatório — Criação do Handoff H-0065

```yaml
rastreabilidade:
  etapa: CRIAR_HANDOFF
  objeto: H-0065
  item: ITEM-0010
  adr: ADR-0046
  predecessor: H-0064
```

## Papel executado

Autoria documental exclusiva do handoff H-0065. Nenhum código, ADR,
contrato, nomenclatura ou backlog foi alterado nesta etapa. Nenhum stage,
commit ou push foi realizado.

## Autoridades lidas

Integralmente: `ADR-0046`, `H-0061`, `H-0063`, `H-0064`. Focalmente:
`contrato_estilo.md` §2, §3.8, §4 (R-1, R-4, R-11, R-12, R-13);
`10_ESTILO.md` §4.8, §4.9. Código inspecionado (leitura, sem alteração):
`tela/carregamento/estilo.py` (primitivas de `EstadoEstiloRuntime`),
`tela/estilo.py` (`ControladorTelaEstilo`), `demo/demo.py` (instanciação de
`RuntimeEstilo`, tratamento de `F4`/`Esc`, `_anexar_tela_estilo`).

## Análise do ciclo de vida do candidato

```yaml
analise_ciclo_vida_candidato:
  nascimento: >
    DETERMINADO_PELA_AUTORIDADE. ADR-0046 §7 (linha F4) e §4: o candidato
    nasce a cada visita à tela, não uma unica vez por sessao.
  inicializacao: >
    DETERMINADO_PELA_AUTORIDADE. Derivado da baseline (ultima configuracao
    persistida); escolhas correntes vem dos preset_default.
  abertura_F4: >
    DETERMINADO_PELA_AUTORIDADE. F4 cria/reinicializa candidato a partir da
    baseline vigente naquele instante.
  saida_sem_aplicar: >
    DETERMINADO_PELA_AUTORIDADE. Descarta diferencas nao confirmadas;
    candidato volta a refletir a baseline. Como H-0065 nao cria Aplicar,
    toda mutacao desta capacidade e por definicao nao confirmada.
  reabertura: >
    DETERMINADO_PELA_AUTORIDADE. Mesmo efeito da abertura F4 (novo
    candidato = baseline vigente, que nao muda nesta capacidade).
  fonte_escolhido: >
    DETERMINADO_PELA_AUTORIDADE (ADR-0046 §7, linha Espaco: transferencia
    navegacional e atualizacao do candidato sao o mesmo evento). O
    mecanismo canonico dois_niveis_por_foco (H-0055/H-0063) continua sendo
    a fonte de renderizacao; a exigencia e que ele nunca divirja do
    candidato, por serem mutados juntos no mesmo evento de Espaco.
  suficiencia_documental: >
    SUFICIENTE. Nenhum ponto necessario ao H-0065 ficou NAO_DETERMINADO com
    mais de uma semantica materialmente diferente possivel. A ADR-0046
    fixa efeito observavel do ciclo de vida do candidato e o codigo de
    H-0061 ja oferece exatamente as primitivas necessarias
    (criar_candidato, definir_preset_candidato, materializar_local) sem
    exigir nenhuma nova estrutura ou decisao normativa adicional.
```

## Decisões de mapeamento

Os quatro caminhos de mutação (`borda.preset_default`,
`chip.preset_default`, `indicadores.selecionado.preset_default`,
`indicadores.incluido.preset_default`) já coincidem exatamente entre
`CAMINHOS_PRESET_DEFAULT_PERMITIDOS` (H-0061) e `_CAMINHOS_CATEGORIAS`
(H-0063) — nenhum caminho novo foi criado; nenhuma lógica por nome de
preset foi autorizada. A atomicidade da mutação reutiliza o par
`definir_preset_candidato` (mutação de cópia) →
`EstadoEstiloRuntime.materializar_local` (validação e commit), já
implementado e já garantindo que falha não compromete o candidato anterior.

## Resultado

```yaml
resultado:
  status: HANDOFF_CREATED
  handoff: docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  capacidade:
    - escolha_atualiza_candidato_runtime
  arquivos_implementacao_autorizados:
    - tela/estilo.py
    - demo/demo.py
    - tela/teste_estilo_h0065.py
    - demo/teste_demo_estilo_h0065.py
    - docs/relatorios/IMP-0065-vinculacao-escolha-candidato-estilo.md
  testes_requeridos:
    - inicializacao_candidato_conforme_ciclo_de_vida
    - setas_nao_mutam_candidato
    - espaco_muta_somente_categoria_correspondente_nas_quatro_categorias
    - filho_escolhido_reflete_candidato_sem_divergencia
    - baseline_global_arquivo_intactos_em_todos_os_cenarios
    - troca_sucessiva_termina_no_ultimo_escolhido
    - pais_independentes_acumulam_corretamente
    - preset_invalido_preserva_candidato_integro
    - esc_e_reabertura_conforme_ciclo_de_vida_documentado
    - regressao_integral_h0063_h0064_e_suite_completa
  fora_de_escopo:
    - Aplicar/Enter_contextual
    - chip_aplicar_na_barra_de_menus
    - popup_de_confirmacao
    - demonstracao_integrada_e_override_local
    - preview_real_do_candidato
    - persistencia_em_config_estilo_json
    - publicacao_de_estilo_global
    - CONFIRMADO_ABORTADO
    - tiling_cor_inativo_cor_alerta_indicadores_concluido
    - ITEM-0024
    - ITEM-0032
  bloqueios: []
```

## Verificação

```zsh
git diff --check -- \
  docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md \
  docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0065.md
```

Executado; sem marcadores de conflito. Nenhum `git add`/`git commit`/`git
push` foi realizado — stage permanece exatamente como estava antes desta
etapa.

## Limite

Etapa encerrada após criação do handoff e deste relatório. Não foi
implementado código, não foi executado QA_HANDOFF, não foi criado H-0066,
não foi introduzido `Aplicar`, backlog/ADR não foram alterados, e nenhuma
ação de stage/commit/push foi realizada.
