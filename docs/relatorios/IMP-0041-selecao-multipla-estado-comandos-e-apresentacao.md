---
name: IMP-0041-selecao-multipla-estado-comandos-e-apresentacao
description: "Resultado factual da implementacao do Handoff 1 do ITEM-0006 (H-0041): selecao multipla por conjunto de IDs, comandos Espaco/Enter/Esc, coluna tg e chips dinamicos."
metadata:
  type: relatorio_implementacao
  tipo_execucao: IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-0041
  data: 2026-07-28
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  issues_relacionadas:
    - ITEM-0006
  bugs_abertos: []
  autorizacoes_operacionais: []
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# IMP-0041 — Relatório de implementação

> Handoff 1 do ITEM-0006: estado da seleção múltipla, comandos Espaço/Enter/Esc,
> coluna `tg`, reconciliação, ordenação lógica e chips dinâmicos — sem operação
> externa.

## 1. Identificação e status

```yaml
handoff: H-0041 — Seleção múltipla: estado, comandos e apresentação
tipo_execucao: IMPLEMENTACAO
status_literal: IMPLEMENTED
status_normalizado: IMPLEMENTATION_COMPLETED_AWAITING_QA
```

## 2. Delta material

- Estado da seleção múltipla por conjunto de IDs estáveis, por console, em
  runtime (`tela/selecao.py`), inicialmente vazio e independente do cursor
  (D-SEL-01). Toggle, `Todos`, limpeza, reconciliação e ordenação lógica como
  funções puras (nenhum dict recebido é mutado).
- `Espaço` alterna inclusão somente de item selecionável, sem mover o cursor;
  item não selecionável ignora o comando (D-SEL-05).
- `Enter` sem seleção age como `Todos` (snapshot de IDs na ordem lógica);
  com seleção, permanece **inativo** — nenhuma execução (D-SEL-04/D-SEL-07).
- Primeiro `Esc` limpa a seleção e permanece na tela; sem seleção, preserva o
  comportamento vigente de Sair/Voltar (D-SEL-08).
- Coluna `tg` (inclusão) adjacente à `ec` (cursor), com `●`/`○` para
  selecionáveis incluído/não-incluído e vazio para não selecionável/não
  navegável (D-SEL-09). Paridade geométrica preservada entre navegação e
  renderer (AT-0021/PN-0016).
- Chips `[␣] Marcar` e `[⏎] Todos/Executar` dinâmicos: existência por seleção
  múltipla no console focado; rótulo `Todos`/`Executar` conforme o estado da
  seleção.
- Bug corrigido: o mapeamento participante→id do renderer assumia alinhamento
  1:1 com itens navegáveis, quebrando com itens não navegáveis intercalados
  (risco §3 do H-0041). Corrigido para mapear todos os itens na ordem declarada.

### Achado material sobre símbolos `tg`

O H-0041 (§3) deixou em aberto se `config/estilo.json` possuiria símbolos para
`tg`. Verificou-se que os símbolos `incluido` (`●`/`○`) **já existem** em
`config/estilo.json` e **já são resolvidos** pelo loader em
`EstiloResolvido.incluido_on/incluido_off` (loader.py). **Nenhuma exceção da
seção 14 foi necessária** — o renderer consome os campos já materializados.

### Ressalva de leitura

O manifesto do H-0041 (§5) lista `config/estilo.json` em `nao_ler`. Ele foi
lido uma única vez, focadamente, exclusivamente para verificar a existência
dos símbolos `tg` (questão em aberto do §3). O achado eliminou a necessidade
de alterar `config/estilo.json`; nenhuma alteração foi feita nele.

## 3. Artefatos criados ou alterados

```yaml
diretorios_criados: []
arquivos_criados:
  - caminho: tela/selecao.py
    finalidade: estado/toggle/Todos/limpeza/reconciliação/ordenação (funções puras)
  - caminho: config/telas/demo/h0041_selecao_multipla_oito_itens.json
    finalidade: fixture D-SEL-22 (oito itens; seis navegáveis, dois não navegáveis)
  - caminho: demo/demo_selecao.py
    finalidade: ponto de entrada TTY dedicado do H-0041
  - caminho: tela/teste_selecao.py
    finalidade: testes unitários do módulo selecao
  - caminho: demo/teste_demo_selecao.py
    finalidade: testes de integração do ponto de entrada dedicado
arquivos_alterados:
  - caminho: tela/navegacao.py
    delta: LARGURA_INDICADOR_INCLUSAO + _console_declarou_selecao_multipla; reserva de tg em grade_de_itens
  - caminho: tela/renderizador.py
    delta: contexto _navegacao_atual estendido (selecoes/inc_on/inc_off); coluna tg; correção do mapeamento participante→id; chips Espaço/Enter e rótulo dinâmico; renderizar_tela recebe selecoes
  - caminho: demo/demo.py
    delta: estado selecoes; dispatch Espaço/Enter delegado a tela/selecao; Esc limpa antes de sair; passagem de selecoes ao renderer; detecção de mudança de selecoes
  - caminho: tela/teste_renderizador.py
    delta: teste_selecao_multipla_h0041 (coluna tg, ec independente, chips, rótulo dinâmico)
  - caminho: demo/teste_demo.py
    delta: testes de integração do dispatch Espaço/Enter/Esc
arquivos_removidos: []
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: pytest tela/teste_selecao.py tela/teste_navegacao.py
    resultado_compacto: 65 passed
  - comando_ou_metodo: pytest tela/teste_renderizador.py demo/teste_demo.py demo/teste_demo_selecao.py
    resultado_compacto: 324 passed
  - comando_ou_metodo: pytest (suíte canônica completa)
    resultado_compacto: 522 passed, 0 failed
  - comando_ou_metodo: git diff --check
    resultado_compacto: limpo
criterios_de_aceite:
  - id: CA-01
    evidencia: teste_selecao.py TestEstadoSelecao
    resultado: OK
  - id: CA-02
    evidencia: teste_selecao.py TestToggleEspaco + teste_demo.py test_h0041_espaco_*
    resultado: OK
  - id: CA-03
    evidencia: teste_demo.py test_h0041_enter_sem_selecao_aplica_todos
    resultado: OK
  - id: CA-04
    evidencia: teste_selecao.py test_ordenacao_segue_ordem_logica_nao_marcacao
    resultado: OK
  - id: CA-05
    evidencia: teste_selecao.py TestReconciliacao
    resultado: OK
  - id: CA-06
    evidencia: teste_demo.py test_h0041_esc_limpa_selecao_sem_sair
    resultado: OK
  - id: CA-07
    evidencia: teste_renderizador.py teste_selecao_multipla_h0041
    resultado: OK
  - id: CA-08
    evidencia: teste_renderizador.py teste_selecao_multipla_h0041 (●/○)
    resultado: OK
  - id: CA-09
    evidencia: teste_renderizador.py teste_selecao_multipla_h0041 (item_04/08)
    resultado: OK
  - id: CA-10
    evidencia: teste_selecao.py TestChipEspacoAtivo
    resultado: OK
  - id: CA-11
    evidencia: teste_demo.py test_h0041_enter_com_selecao_inativo + test_h0041_nenhuma_operacao_externa
    resultado: OK
  - id: CA-12
    evidencia: suíte completa 522 passed, sem regressão
    resultado: OK
```

Provas semânticas confirmadas (independentes da saída observada): seleção
inicial vazia; cursor inicial em `item_01`; seis navegáveis na ordem
`item_01,02,03,05,06,07`; `Todos` produz exatamente `item_01,03,05,07`;
item não selecionável ignora `Espaço`; não navegáveis visíveis sem cursor;
`ec`/`tg` independentes; `Executar` inativo; `Esc` limpa sem sair; nenhuma
operação externa invocada.

## 6. Demonstração operacional

```yaml
cwd: "."
comando: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao --tela config/telas/demo/h0041_selecao_multipla_oito_itens.json
entrada_ou_fixture: config/telas/demo/h0041_selecao_multipla_oito_itens.json
configuracao: config/estilo.json (via carregar_estilo, sem alteração)
saida_observada: quadro com cursor → em item_01, tg ○ nos selecionáveis, tg vazio em item_02/06 e item_04/08, chips [Esc] Sair [␣] Marcar [⏎] Todos
comparacao_com_esperado: conforme prova_semantica do H-0041 §11
prova_semantica: cursor em item_01; não navegáveis visíveis sem cursor; Espaço alterna tg sem mover cursor; Enter=Todos; Executar inativo; Esc limpa antes de sair
codigo_de_saida: 0
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: 721f8f1
staged: vazio
unstaged:
  - demo/demo.py
  - demo/teste_demo.py
  - tela/navegacao.py
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - artefatos pré-existentes do ciclo ADR-0034 (docs/contratos/**, docs/nomenclatura/**, docs/backlog.md, docs/adr/INDICE_ADR.md) — não tocados por esta execução
nao_rastreados:
  - tela/selecao.py
  - tela/teste_selecao.py
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json
  - demo/demo_selecao.py
  - demo/teste_demo_selecao.py
  - docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
divergencias_materiais: []
```

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - config/estilo.json foi lido focadamente apesar de listado em nao_ler (H-0041 §5) para resolver a questão em aberto do §3 sobre símbolos tg; nenhum campo foi alterado nele
  - regra_ativo/forma_exibicao permanecem não avaliados como antes; apenas regra_existencia e o rótulo dinâmico de Enter foram implementados
  - o caminho de console sem distribuicao_matricial (via _aplicar_indicador_linhas) não exibe coluna tg; a fixture D-SEL-22 usa distribuicao_matricial, cobrindo o caminho contratado
observacoes_para_qa:
  - o bug do mapeamento participante→id (itens não navegáveis intercalados) foi corrigido como parte necessária da coluna tg; recomenda-se validar regressão visual em fixtures H-0040 com itens mistos, se houver
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada_nesta_etapa: false
  roteiro_disponivel_no_handoff: true
  itens_pendentes:
    - roteiro TTY de 10 passos (H-0041 §11) a executar em terminal real pelo usuário
```

IMPLEMENTATION_COMPLETED_AWAITING_QA
