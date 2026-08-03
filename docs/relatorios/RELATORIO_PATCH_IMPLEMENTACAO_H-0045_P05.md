---
name: REL-PATCH-H-0045-P05-repaginacao-apos-resize
description: "Corrige repaginação intermitente após redimensionamento: altura_interna real substitui aproximação fixa (altura-8) na reconciliação de página (R04)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P04.md
  achados_tratados:
    - VM-H0045-R04-004
---

# REL-PATCH-H-0045-P05 — Patch de implementação

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P05
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P04.md
falha_manual:
  rodada: R04
  progresso: 6/17
  id: VM-H0045-R04-004
  severidade: BLOQUEANTE
  componente: repaginacao_apos_resize
achados_tratados: [VM-H0045-R04-004]
achados_resolvidos: [VM-H0045-R04-004]
achados_pendentes: []
novos_achados: []
```

## 3. Diagnóstico (causa raiz)

```yaml
perguntas:
  1_eventos_sigwinch_por_reducao: "1 por acordar de select (o loop drena todos os bytes pendentes do wakeup pipe antes de consultar ioctl uma unica vez) -- nao e a causa"
  2_dimensoes_finais_ou_intermediarias: "ioctl consultado apos o dreno reflete as dimensoes CORRENTES no momento do wakeup -- nao ha uso de par intermediario obsoleto"
  3_reconciliacao_em_todos_os_eventos: "sim, em todo evento que muda largura/altura -- nao e seletiva"
  4_cursor_lido_antes_ou_depois: "depois -- cursores[console.id] e lido de estado ja atualizado com largura/altura novas (ordem correta, preservada desde P03)"
  5_mesma_geometria_reconciliacao_vs_render: >
    NAO. reconciliar_pagina_com_cursor (P03/P04) derivava altura_interna via
    tela.paginacao._geometria_do_estado, cujo fallback (estado sem
    "altura_interna" explicito, SEMPRE o caso em demo.py) e altura-8 --
    aproximacao fixa que assume cabecalho=3 linhas e barra_de_menus=1 linha
    de chips (3 linhas com borda). l_cab e de fato sempre 3, mas l_barra
    (renderer real, _linhas_barra) varia: depende de quais chips existem
    (regra_existencia, D-TEC-12) e de quantos cabem na largura corrente
    (H-0016). O render (_fragmentos_e_total_paginacao) usa
    altura_alvo-2, com altura_alvo derivado de l_corpo_disponivel =
    altura - l_cab - l_barra_REAL -- nao de altura-8.
  6_pagina_reconciliada_altera_mesmo_estado_do_render: "sim -- nao e o problema"
  7_etapa_posterior_clampa_ou_sobrescreve: "nao -- _pagina_clamp so agiria se a pagina reconciliada excedesse o total; o defeito produz um NUMERO de pagina valido, porem errado (sem o item)"
  8_renderer_recalcula_com_valores_diferentes: "sim -- essa e a causa raiz (pergunta 5)"
  9_diferenca_entre_geometria_do_1o_evento_e_final: "nao aplicavel -- a divergencia existe mesmo em um UNICO evento de resize, independente de sequencia"
  10_sequencia_pode_reconciliar_com_uma_pagina_e_renderizar_outra: "sim, confirmado empiricamente (ver evidencia)"
  11_pagina_do_item_logico_deterministica_em_1_item_por_pagina: "sim, deterministica -- o defeito esta na CAPACIDADE usada como entrada (altura_interna), nao na funcao"
  12_item_corrente_fragmentado_ou_nao_navegavel: "nao -- o item existe e e navegavel; ele so e colocado na pagina ERRADA pela reconciliacao"
  13_pagina_recalculada_por_indice_logico_ou_posicao_fisica: "por indice logico (correto) -- D-TEC-17 preservado"
  14_selecao_preservada_enquanto_cursor_pagina_divergem: "sim -- selecao (tela.selecao) e cursor (tela.navegacao/paginacao) sao trilhas de estado independentes; nao ha acoplamento"
  15_testes_anteriores_simulavam_so_resize_direto: >
    em parte: os testes P03/P04 fixam largura=80 durante toda a sequencia de
    resize. Nessa largura, a barra desta fixture SEMPRE cabe em 1 linha
    (l_barra=3) independentemente de altura -- por isso a aproximacao
    altura-8 nunca divergiu do render real nesses testes, mascarando o
    defeito. A divergencia so aparece em larguras onde o numero de linhas da
    barra (1 ou 2) muda -- inclusive de forma dependente de altura, quando a
    existencia de um chip como [✥] (que depende da contagem de navegaveis NA
    PAGINA CORRENTE) desloca o total de chips para o outro lado do limiar de
    quebra de linha.
causa_raiz_confirmada: >
  tela.paginacao.reconciliar_pagina_com_cursor calculava altura_interna por
  uma aproximacao fixa (altura-8) nunca alinhada ao l_barra REAL do render
  (variavel). O erro constante nao muda o resultado em geometrias folgadas,
  mas se torna catastrofico perto da capacidade minima (1 item/pagina): o
  item logico do cursor deixa de aparecer na pagina reconciliada -- exibida
  apenas por coincidencia nas geometrias em que o erro nao cruza um limiar de
  paginacao (explica o carater "intermitente" do achado).
evidencia_empirica: >
  Script ad-hoc sobre h0045_paginacao_console_unico, largura=45 fixa, cursor
  em item_17 (indice 16), sequencia de alturas [30,25,20,15,10,8,10,15,24,30]
  comparando a reconciliacao ANTIGA (sem altura_interna explicito) contra o
  render real: altura=25 e altura=10 (e as repeticoes) produzem cursor
  AUSENTE do quadro ("página 1/3"/"página 9/34" em vez da pagina real que
  contem item_17); altura=8 cai em quadro minimo (RenderizadorErro no
  render, silenciosamente contornado pela reconciliacao antiga que so
  clampava). Com a nova autoridade (altura_interna_disponivel), as 10
  alturas produzem cursor visivel no item correto em todas as geometrias
  suficientes, e a reconciliacao e corretamente pulada (estado preservado)
  na geometria insuficiente.
hipotese_confirmada: altura_interna_ou_desconto_estrutural_divergentes
hipoteses_descartadas:
  - dimensoes_intermediarias_de_multiplos_SIGWINCH
  - reconciliacao_executada_antes_da_geometria_final
  - estado_reconciliado_nao_e_o_estado_renderizado
  - pagina_reconciliada_sobrescrita_por_clamp_posterior
  - indice_logico_convertido_com_geometria_antiga
  - pagina_do_item_logico_incorreta_em_um_item_por_pagina
  - cursor_preservado_mas_pagina_antiga_mantida  # o numero MUDAVA, mas para o numero errado
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VM-H0045-R04-004
    alteracao: >
      (1) tela/renderizador.py: extraida _preparar_contexto_navegacao
      (bloco de popular _navegacao_atual, antes inline em renderizar_tela) e
      adicionada altura_interna_disponivel(modelo, estilo, largura, altura,
      verboso, console=None, ...) -- autoridade publica que reproduz
      EXATAMENTE o calculo de l_cab/l_barra/l_corpo_disponivel de
      renderizar_tela (mesmo _linhas_barra, mesmo contexto de chips) e a
      regra de particionamento do corpo (DA-01 para descendente unico e
      colunas horizontais de altura plena -- os dois casos das fixtures
      H-0045; distribuicao vertical explicita via _distribuir_alturas
      reutilizado sem duplicar o algoritmo de pesos). Retorna None quando a
      geometria e insuficiente (mesmo caso de RenderizadorErro no render).
      (2) tela/paginacao.py: reconciliar_pagina_com_cursor ganha parametro
      opcional altura_interna, com PRECEDENCIA sobre a aproximacao de
      _geometria_do_estado quando fornecido; chamadores sem esse valor
      preservam o comportamento anterior (retrocompatibilidade). (3)
      demo/demo.py: _reconciliar_paginacao_apos_resize calcula a capacidade
      real por console via altura_interna_disponivel (mesmo contexto de
      navegacao/chips que o render seguinte vai usar) e a repassa a
      reconciliar_pagina_com_cursor; geometria insuficiente (None) preserva
      pagina/cursor correntes sem reconciliar.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P05.md
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: >
      nova _preparar_contexto_navegacao (extraida de renderizar_tela, sem
      mudanca de comportamento); nova altura_interna_disponivel (autoridade
      publica de geometria vertical para paginacao)
  - caminho: tela/paginacao.py
    delta: reconciliar_pagina_com_cursor aceita altura_interna opcional (precedencia sobre a aproximacao)
  - caminho: demo/demo.py
    delta: >
      import de altura_interna_disponivel;
      _reconciliar_paginacao_apos_resize calcula e repassa a capacidade real
      por console em vez de depender do fallback altura-8
  - caminho: demo/teste_demo_paginacao.py
    delta: >
      dois testes novos (sequencia completa de resize com cursor distante +
      selecao preservada + geometria insuficiente + caso de 1 item/pagina;
      teste especifico do caso limite 1 item/pagina); nova fixture auxiliar
      _modelo_fluxo_paginado (h0045_fluxo_execucao_paginado, ja existente,
      paginacao + selecao multipla)
arquivos_removidos: []
documentos_normativos_alterados: []
preservacoes:
  - P01 (chips e comandos de pagina)
  - P02 (geometria da barra, sem residuo)
  - P03 (cursor renderizado, indice logico global, reconciliacao inicial apos resize)
  - P04 (unicidade de IDs de console)
  - pagina sem navegaveis, dois consoles independentes, modo verboso, politicas de quebra, selecao multipla, Todos, fluxo focal
limitacao_residual_fora_do_escopo: >
  ir_para_pagina/pagina_anterior/pagina_proxima/linhas_logicas_navegaveis_da_pagina
  (comandos de teclado ","/"."/"<"/">" e setas, fora do tratamento de
  resize) continuam usando a aproximacao de _geometria_do_estado quando o
  estado nao fixa altura_interna -- o MESMO defeito de classe pode
  teoricamente se manifestar em navegacao por teclado em larguras onde
  l_barra real diverge de 3. Fora do escopo deste patch (objeto:
  especificamente repaginacao apos SIGWINCH); registrado para eventual
  achado futuro se a validacao manual expuser sintoma equivalente fora de
  resize.
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py
      tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 347 passed (2 novos: test_demo_h0045_p05_repaginacao_preserva_item_cursor_e_selecao_em_sequencia_de_resize, test_demo_h0045_p05_caso_limite_um_item_por_pagina)
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py
      tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 558 passed (556 anterior + 2 novos)
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 790 passed (788 anterior + 2 novos), sem regressao
  - comando_ou_metodo: >
      script ad-hoc comparando reconciliacao ANTIGA (fallback altura-8) vs
      NOVA (altura_interna_disponivel) sobre h0045_paginacao_console_unico,
      largura=45, sequencia [30,25,20,15,10,8,10,15,24,30]
    resultado_compacto: >
      antiga: FALHA em altura=25 e altura=10 (cursor ausente do quadro,
      "página 9/34" em vez da pagina real de item_17); nova: OK em todas as
      10 geometrias suficientes, skip correto na insuficiente (altura=8)
```

Verificação local não equivale a QA independente.

## 6. Demonstração automatizada

```yaml
cenario: h0045_paginacao_console_unico
largura_fixa: 45
item_logico_inicial: 0 (item_01)
apos_avancar_pagina: item_logico=16 (item_17) -- item distante do inicio
selecao: nao_aplicavel (politica_selecao=unica nesta fixture; cobertura de
  selecao preservada feita em demo/teste_demo_paginacao.py com a fixture
  h0045_fluxo_execucao_paginado, que declara politica_selecao=multipla)
sequencia_alturas: [30, 25, 20, 15, 10, 8, 10, 15, 24, 30]
resultado_por_altura:
  30: "página 1/2, cursor em item_17, OK"
  25: "página 2/3, cursor em item_17, OK"
  20: "página 2/4, cursor em item_17, OK"
  15: "página 3/6, cursor em item_17, OK"
  10: "página 17/34 (capacidade 1 item/pagina), cursor em item_17, OK"
  8: "quadro minimo (geometria insuficiente para cabecalho+barra+corpo) -- sem crash, cursor logico preservado"
  10_retorno: "página 17/34, cursor em item_17, OK"
  15_retorno: "página 3/6, cursor em item_17, OK"
  24_retorno: "página 2/3, cursor em item_17, OK"
  30_retorno: "página 1/2, cursor em item_17, OK"
falhas: 0
```

Não substitui validação TTY real.

## 7. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
    finalidade: reconciliacao introduzida no P03 (base sobre a qual este patch corrige a fonte de geometria)
    leitura_necessaria_para: [cadeia P03]
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P04.md
    finalidade: baseline aprovado ate P04 (788 testes)
    leitura_necessaria_para: [cadeia]
```

## 8. Validação manual

```yaml
progresso_anterior: 6/17
nova_rodada: PENDENTE_USUARIO_R05
```
