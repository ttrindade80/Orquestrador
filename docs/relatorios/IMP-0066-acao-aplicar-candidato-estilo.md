# IMP-0066 — Ação Aplicar sobre o candidato de estilo

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0066
  predecessor: H-0065
  artefato_principal:
    docs/handoff/H-0066-acao-aplicar-candidato-estilo.md
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - tela/teste_estilo_h0066.py
    - demo/teste_demo_estilo_h0066.py
    - docs/relatorios/IMP-0066-acao-aplicar-candidato-estilo.md
  arquivos_alterados:
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
    - tela/estilo.py
    - demo/demo.py
    - tela/renderizacao/tela.py
    - tela/teste_estilo_h0063.py
    - tela/teste_estilo_h0064.py
    - tela/teste_estilo_h0065.py
    - demo/teste_demo_estilo_h0063.py
    - demo/teste_demo_estilo_h0064.py
    - demo/teste_demo_estilo_h0065.py

autorizacao_adicional_de_escopo:
  arquivo: tela/teste_estilo_h0064.py
  motivo: >
    solicitar_aplicacao é capacidade única na classe compartilhada
    ControladorTelaEstilo; teste_estilo_h0064.py:318 tinha a mesma
    expectativa "sem Aplicar" já autorizada em h0063/h0065, mas ausente
    da lista nominal do handoff. Suíte confirmou a falha antes da correção.
  concedida_por: gerente (perfil GERENTE_DE_ADR_IMPLEMENTACAO), continuação
    explícita após status AUTORIZACAO_DE_ESCOPO_NECESSARIA.
  mudanca_aplicada: só a asserção superada; demais garantias preservadas.

resultado:
  formula_aplicar_disponivel: >
    ControladorTelaEstilo.aplicar_disponivel = not
    runtime.comparar_candidato_baseline(), recalculada a cada consulta
    (nunca invertida, nunca flag independente). demo.py injeta o valor em
    renderizar_estado; tela/renderizacao/tela.py o encaminha a
    _preparar_contexto_navegacao, já consumido por barra_menus._linhas_barra
    como candidato_divergente (infra H-0062 reutilizada, sem shell popup).
  chip_aplicar: >
    Declarado em h0063_...json (chip_aplicar, tecla ⏎, texto Aplicar,
    regra_ativo candidato_divergente), entre [␣] Selecionar e [?] Ajuda.
    Sempre presente; inativo usa cor_inativo canônico já existente.
  enter: >
    demo.py intercepta Enter na tela de Estilo (qualquer nível) antes do
    dispatch genérico Todos/Executar. Inativo: no-op. Ativo: chama
    solicitar_aplicacao() e grava o retorno em
    estado["solicitacao_aplicacao_estilo"]. Não substitui Espaço nem altera
    outras telas.
  solicitacao: >
    solicitar_aplicacao() retorna None quando inativo; ativo retorna
    SolicitacaoAplicacaoEstilo(baseline, candidato) — nome alinhado ao
    precedente documental de H-0062 (histórico), reimplementado nesta
    fatia. Sem persistência, publicação, popup ou literal de estado novo.
  snapshot: >
    SolicitacaoAplicacaoEstilo é dataclass frozen com deepcopy em
    __post_init__ (padrão já usado por PresetEstilo). Imutável mesmo após
    mutação posterior do runtime/candidato.
  esc_filho: >
    Esc filho→pais continua puramente navegacional (H-0065); nenhum gancho
    novo o toca, logo candidato/baseline/aplicar_disponivel intactos.
  saida_efetiva: >
    Preservada de H-0065 (descartar_visita): candidato volta à baseline,
    aplicar_disponivel recalcula para False.
  resize_redraw: >
    Elegibilidade nunca é armazenada; cada render recalcula
    aplicar_disponivel a partir do runtime.
  fronteira_posterior: sem popup, confirmação, persistência, publicação ou preview real.
  testes:
    h0066: 27 passed (14 tela + 13 demo)
    regressao_h0063_h0064_h0065: 64 passed
    suite_completa: 1269 passed
  demonstracao:
    - F4 com Aplicar inativo
    - Enter inativo -> no-op sem solicitacao
    - Espaco diverge candidato -> Aplicar ativo
    - Enter ativo -> solicitacao estrutural produzida
    - sem popup
    - runtime nao persiste/publica; config/estilo.json intacto
    - snapshot estavel apos mutacao posterior
    - Esc filho preserva candidato/baseline/elegibilidade
    - saida efetiva restaura e desativa Aplicar
  validacao_manual_necessaria: []
  desvios:
    - >
      O 6º chip (Aplicar) estourava por 1 char o layout de 2 linhas em
      62 colunas (nivel de filhos, rotulo "Retornar aos pais"), quebrando
      resize ja suportado. Corrigido com linhas.maximo: 3 na propria
      distribuicao da fixture h0063 (resto identico ao default do
      renderer); nenhum codigo do renderer foi alterado, e larguras ja
      suportadas continuam usando o mesmo numero de linhas de antes.
  bloqueios: []

tratamento_testes_predecessores:
  arquivos:
    - tela/teste_estilo_h0063.py
    - tela/teste_estilo_h0064.py
    - tela/teste_estilo_h0065.py
    - demo/teste_demo_estilo_h0063.py
    - demo/teste_demo_estilo_h0064.py
    - demo/teste_demo_estilo_h0065.py
  expectativas_superadas:
    - "tela/teste_estilo_h0063.py::test_fronteira_sem_candidato_nem_mutacao_de_baseline: hasattr(solicitar_aplicacao) agora True; aplicar_disponivel False; solicitar_aplicacao() None"
    - "tela/teste_estilo_h0064.py::test_fronteira_navegacao_nao_muta_candidato_nem_config: hasattr(solicitar_aplicacao) agora True (autorizacao adicional)"
    - "tela/teste_estilo_h0065.py::test_sem_aplicar_persistencia_ou_publicacao: hasattr(solicitar_aplicacao) agora True"
    - "demo/teste_demo_estilo_h0063.py::test_ajuda_ultimo_e_sem_aplicar_nem_entrada_no_nivel (renomeado test_ajuda_ultimo_e_aplicar_presente_inativo_sem_entrada_no_nivel): chip_aplicar presente e inativo, antes de chip_ajuda"
    - "demo/teste_demo_estilo_h0063.py::test_barra_selecionar_canonico: 'Aplicar' presente e inativo (candidato ainda igual a baseline)"
    - "demo/teste_demo_estilo_h0063.py::test_fronteira_sem_confirmado_abortado_aplicar_popup: 'Aplicar' presente e ativo (sequencia diverge candidato); sem solicitacao pois Enter nao foi acionado"
    - "demo/teste_demo_estilo_h0064.py::test_navegacao_e_espaco_respeitam_fronteira_candidato_vs_aplicado: 'Aplicar' presente e ativo; solicitacao None sem Enter"
    - "demo/teste_demo_estilo_h0065.py::test_demonstracao_non_tty_ciclo_completo: 'Aplicar' presente e ativo apos divergencia; sem solicitacao/popup"
    - "demo/teste_demo_estilo_h0065.py::test_sem_aplicar_nem_preview_real_no_quadro (renomeado test_aplicar_presente_ativo_sem_preview_real_no_quadro): 'Aplicar' presente e ativo; preview real continua ausente"
  invariantes_preservados:
    - baseline
    - global
    - arquivo
    - ausencia_popup
    - ausencia_persistencia
    - ausencia_publicacao
    - ausencia_preview_real
```

## Resumo

H-0066 introduz a fatia "AÇÃO APLICAR" sobre a tela normal de Estilo
(H-0063/H-0064/H-0065): o chip `[⏎] Aplicar` passa a existir sempre,
ativo/inativo conforme `candidato x baseline`; Enter, quando ativo, produz
**somente** a solicitação estrutural imutável `SolicitacaoAplicacaoEstilo`
para a etapa posterior de confirmação — sem popup, sem persistência, sem
publicação, sem preview real. A elegibilidade reutiliza integralmente
`EstadoEstiloRuntime.comparar_candidato_baseline` (H-0061) via a ponte
literal `aplicar_disponivel = not comparar_candidato_baseline()`, nunca
invertida e nunca armazenada como flag independente.

A infraestrutura declarativa de H-0062 (`aplicar_disponivel` em
`contexto_execucao.py`, regra `candidato_divergente` em `barra_menus.py`) já
existia, mas não estava encadeada: `renderizar_tela` não repassava
`aplicar_disponivel` a `_preparar_contexto_navegacao`, zerando o valor antes
de chegar à barra. O ajuste pontual autorizado (novo parâmetro + repasse,
espelhando `executar_disponivel`) fechou esse elo sem redesenho do renderer.

Durante a implementação surgiram dois pontos fora da lista original de
arquivos/escopo, tratados conforme protocolo:

1. `tela/teste_estilo_h0064.py` continha a mesma expectativa "sem Aplicar"
   corrigida nos demais arquivos de teste, mas não estava autorizado. A
   implementação parou, emitiu `AUTORIZACAO_DE_ESCOPO_NECESSARIA` e só
   prosseguiu após autorização adicional explícita do gerente.
2. O sexto chip da barra estourava por 1 caractere o layout de 2 linhas em
   terminais de 62 colunas no nível de filhos, quebrando resize já
   suportado. Corrigido declarando `linhas.maximo: 3` na `distribuicao` da
   própria fixture h0063 (resto idêntico ao default do renderer); nenhum
   código do renderer foi tocado, e larguras já suportadas continuam
   usando o mesmo número de linhas de antes.

Todos os testes predecessores de H-0063/H-0064/H-0065 foram reexecutados e
ajustados apenas nas asserções literalmente superadas pela introdução de
Aplicar; nenhuma garantia de baseline, global, arquivo, ausência de popup,
persistência, publicação ou preview real foi enfraquecida.

Suíte completa: **1269 passed**, sem falhas. `config/estilo.json` sem
delta, stage vazio, `git diff --check` limpo, nenhum popup/CONFIRMADO/
ABORTADO introduzido.
