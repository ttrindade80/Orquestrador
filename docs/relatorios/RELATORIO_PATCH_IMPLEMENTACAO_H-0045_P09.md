---
name: REL-PATCH-H-0045-P09-selecao-multipla-console-paginado-nao-reproduz
description: "Diagnostica VM-H0045-R05-005 (selecao multipla indisponivel em h0045_fluxo_execucao_paginado): nao reproduz no estado atual do codigo; fecha a lacuna de cobertura ponta a ponta via TTY real que teria detectado uma regressao"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_BLOCKED
  data: 2026-08-01
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P08.md
  achados_tratados:
    - VM-H0045-R05-005
---

# REL-PATCH-H-0045-P09 — Patch de implementação

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_BLOCKED
patch_id: P09
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P08.md
falha_manual:
  rodada: R05_CONSOLIDADA
  progresso: 6/17..9/17 aprovadas
  id: VM-H0045-R05-005
  severidade: BLOQUEANTE
  componente: selecao_multipla_em_console_paginado
achados_tratados: [VM-H0045-R05-005]
achados_resolvidos: []
achados_pendentes: [VM-H0045-R05-005]
novos_achados: []
```

## 3. Diagnóstico (causa raiz)

```yaml
perguntas:
  1_fixture_declara_multipla: "sim -- config/telas/demo/h0045_fluxo_execucao_paginado.json, console_selecao.politica_selecao == 'multipla' (confirmado por leitura direta e por navegacao._console_declarou_selecao_multipla(console) == True)"
  2_elemento_de_declaracao: "unico elemento do corpo, id console_selecao (tipo console)"
  3_console_carregado_preserva_politica: "sim -- construir_modelo preserva _campos_inertes['politica_selecao'] inalterado; verificado em sessao real"
  4_clone_paginado_preserva_campos: "sim -- _elemento_fragmentado_para_pagina (tela/renderizador.py) faz copy.copy(elemento) + dict(_campos_inertes) e dict(item) por item; politica_selecao, id e selecionavel sobrevivem ao clone (leitura de codigo confirmada linha a linha)"
  5_console_focado_reconhecido_selecionavel: "sim -- _estabelecer_foco_paginacao_inicial estabelece foco_console=0/cursores/pagina_atual no 1o console paginado ja no 1o quadro"
  6_item_corrente_selecionavel: "sim -- item_01 tem selecionavel:true; chip_espaco_ativo(console, estado, navegacao) == True no 1o quadro"
  7_chip_marcar_existe_visivel_ativo: "existe, visivel e ATIVO no 1o quadro (sem cor de inativo) -- confirmado por captura ANSI real via PTY"
  8_espaco_chega_a_tela_selecao: "sim -- processar_comando despacha ' ' para selecao.alternar quando console declara multipla; estado['selecoes'] muda de {} para {'console_selecao': ['item_01']} apos uma unica tecla real"
  9_executar_bloqueia_selecao: "nao -- selecao.alternar/selecionar_todos nunca consultam fluxo_execucao/executar_disponivel; confirmado por leitura e por selecao funcionando com fluxo_execucao ausente (None) durante toda a sessao"
  10_confusao_selecao_com_executar: "nao encontrada -- chip [Enter] fica INATIVO (Executar, cor de inativo) apos marcar, exatamente conforme D-SEL-07/D-SEL-21; a marcacao em si nunca depende disso"
  11_politica_carregada_diverge_da_declarada: "nao -- valor lido em runtime (multipla) e identico ao do JSON em todas as chamadas testadas"
  12_selecoes_tem_entrada_por_console_id: "sim, apos o 1o toggle; _selecao_do_console trata ausencia previa como lista vazia (nao e falha)"
  13_clone_de_paginacao_remove_campos: "nao -- ver pergunta 4; adicionalmente, todo o caminho de COMANDO (processar_comando/navegacao/selecao) opera sobre os elementos ORIGINAIS de modelo.corpo.elementos (via lista_foco), nunca sobre o clone efemero de renderizacao -- o clone so existe dentro de tela/renderizador.py para desenhar o conteudo da pagina"
  14_testes_verificam_quadro_ou_so_estado: "MISTO -- varios testes P01-P08 ja verificam o quadro renderizado (ex.: _cursor_visivel_no_item, contagem de '●'/'○'), mas NENHUM teste existente antes deste patch abria demo/demo.py h0045_fluxo_execucao_paginado por um processo real (subprocess+PTY) e conduzia Espaco/pagina/resize/Todos nessa ordem -- lacuna real de cobertura, ainda que nao seja a causa do achado"
  15_todos_depende_da_mesma_condicao_que_espaco: "sim, por design (regra_existencia console_focado_com_selecao_multipla em ambos) -- e por isso os dois sintomas relatados (Espaco e Todos) sao consistentes com uma UNICA causa; essa causa nao foi localizada no codigo/fixture atuais"
causa_raiz_confirmada: >
  NAO CONFIRMADA. Todas as 15 perguntas do diagnostico obrigatorio foram
  verificadas com evidencia (leitura de codigo + execucao real) e NENHUMA
  aponta para um defeito no estado atual do repositorio (todos os arquivos
  de tela/, demo/demo.py e a fixture, incluindo as modificacoes locais nao
  commitadas de P01-P08). O comportamento requerido pela secao
  "Comportamento obrigatorio" do prompt (cursor selecionavel, chip Marcar
  ativo, toggle refletido no quadro, persistencia por ID entre paginas,
  persistencia apos resize ate 1 item/pagina, Todos cobrindo todas as
  paginas, Executar permanecendo inativo) foi reproduzido INTEGRALMENTE em
  sessao PTY real (sessao controladora de terminal propria, TIOCSWINSZ +
  SIGWINCH reais, mesmo binario `python demo/demo.py
  h0045_fluxo_execucao_paginado` do enunciado) e tambem pela suite
  automatizada (ver evidencia_empirica). Nenhuma das 9 hipoteses da lista
  fornecida se sustenta com o codigo em disco.
evidencia_empirica: >
  (1) Script PTY ad-hoc (sessao com terminal controlador proprio via
  TIOCSCTTY, 80x24): quadro inicial mostra "→ ○ item_01" e "[␣] Marcar" sem
  cor de inativo; Espaco produz "→ ● item_01" no MESMO quadro e muda o
  rotulo/cor de [Enter] para "Executar" inativo; "." leva a pagina 2/2
  (item_17/18); "," retorna a pagina 1/2 com "● item_01" preservado; resize
  para 45x10 (via TIOCSWINSZ no master + SIGWINCH real) produz "página
  1/18" com "● item_01" preservado; resize de volta a 80x24 preserva a
  mesma marcacao; Espaco remove a marcacao; Enter (Todos) marca os 16 itens
  da pagina 1, e a pagina 2 (via ".") mostra item_17/item_18 TAMBEM
  marcados -- Todos cobre todas as paginas, nao so a corrente. (2) O teste
  automatizado test_demo_h0045_p05_repaginacao_preserva_item_cursor_e_selecao_em_sequencia_de_resize
  (ja existente, demo/teste_demo_paginacao.py) exercita exatamente esta
  fixture com Espaco real (via _passo_tty) e uma sequencia de 9
  redimensionamentos, incluindo 1 item/pagina, e ja passava antes deste
  patch. (3) O novo teste ponta a ponta
  test_demo_h0045_p09_pty_selecao_multipla_em_console_paginado_ponto_de_entrada_real
  (adicionado por este patch, ver secao 4) reproduz o roteiro completo do
  achado por um processo real de `demo/demo.py` e PASSA de forma estavel
  (3 execucoes consecutivas, sem flakiness observada).
hipotese_confirmada: nenhuma
hipoteses_descartadas:
  - fixture_nao_declara_selecao_multipla
  - loader_nao_propaga_politica_de_selecao
  - clone_paginado_perde_politica_ou_selecionabilidade
  - console_focado_nao_e_reconhecido_pela_selecao
  - item_logico_resolvido_na_lista_errada
  - chip_marcar_calculado_com_contexto_incorreto
  - comando_espaco_nao_encaminhado
  - selecao_bloqueada_indevidamente_por_executar_inativo
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VM-H0045-R05-005
    alteracao: >
      Nenhuma alteracao funcional em tela/*.py ou demo/demo.py: o
      diagnostico obrigatorio nao localizou causa raiz no codigo (ver
      secao 3) e o prompt proibe correcao por tentativa. Unica alteracao:
      adicionado teste ponta a ponta que abre `demo/demo.py
      h0045_fluxo_execucao_paginado` via subprocess+PTY real (mesmo caminho
      de main(), nao processar_comando isolado, nenhuma injecao direta em
      estado["selecoes"]) cobrindo os 15 passos do roteiro obrigatorio do
      prompt: cursor selecionavel, chip Marcar, toggle com verificacao no
      quadro renderizado, persistencia por pagina, persistencia por resize
      (incluindo 1 item/pagina), remocao da selecao, Todos cobrindo TODAS
      as paginas e ausencia de qualquer sinal de execucao disparada. Fecha
      a lacuna real identificada na pergunta 14 (nenhum teste anterior
      exercitava esta fixture especifica por um processo real).
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P09.md
arquivos_alterados:
  - caminho: demo/teste_demo_paginacao.py
    delta: >
      Adicionado
      test_demo_h0045_p09_pty_selecao_multipla_em_console_paginado_ponto_de_entrada_real
      ao final do arquivo (subprocess.Popen + pty.openpty, seguindo o
      precedente ja estabelecido em
      demo/teste_demo_selecao.py::test_h0041_p04_pty_enter_todos_ponto_de_entrada_real
      e em demo/teste_demo.py secao 8.16). Nenhum teste preexistente foi
      alterado.
arquivos_removidos: []
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 pytest tela/teste_selecao.py
      tela/teste_renderizador.py demo/teste_demo_selecao.py
      demo/teste_demo_paginacao.py -v
    resultado_compacto: 391 passed (390 preexistentes + 1 novo)
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 pytest tela/teste_paginacao.py
      tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -q
    resultado_compacto: 571 passed (570 preexistentes + 1 novo)
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 pytest -q (suite completa)
    resultado_compacto: 803 passed (802 preexistentes + 1 novo)
  - comando_ou_metodo: >
      novo teste isolado executado 3x consecutivas para descartar
      flakiness de temporizacao PTY
    resultado_compacto: PASSED nas 3 execucoes (0.52-0.53s cada)
  - comando_ou_metodo: >
      demonstracao automatizada sem TTY (processar_comando/renderizar_estado
      em sequencia, sem injetar IDs em estado["selecoes"]) registrando
      pagina_atual/item_com_cursor/ids_selecionados/chips a cada passo
    resultado_compacto: >
      abertura: pagina=1 item=item_01 selecionados=[] Marcar=ativo
      Todos=ativo; apos Espaco: selecionados=[item_01] Executar=inativo;
      apos .: pagina=2 item=item_17 selecionados=[item_01] preservados;
      apos ,: pagina=1 item=item_01 selecionados=[item_01]; apos resize
      45x10: pagina=1 (1 item/pagina) selecionados=[item_01] preservados;
      apos resize 80x24: selecionados=[item_01] preservados; apos Espaco:
      selecionados=[] Todos=ativo; apos Enter: selecionados=18 itens
      (item_01..item_18, todas as paginas) Executar=inativo; apos .:
      pagina=2 confirma item_17/item_18 marcados; fluxo_execucao=None em
      toda a sequencia (nenhuma execucao disparada)
```

Verificação local não equivale a QA independente. Nenhuma validação TTY manual é declarada aprovada por este relatório — apenas a demonstração automatizada acima e o novo teste PTY automatizado (que roda sob pytest, não é validação manual do usuário).

## 6. Bloqueios e evidências

```yaml
bloqueios:
  - id: VM-H0045-R05-005
    tipo: causa_raiz_nao_confirmada
    descricao: >
      O diagnostico obrigatorio (15 perguntas) nao encontrou defeito no
      codigo/fixture atuais; o comportamento requerido reproduz
      corretamente em sessao PTY real e na suite automatizada. Aplicar uma
      alteracao sem causa raiz identificada violaria a proibicao explicita
      de "correcao por tentativa" do prompt.
    hipotese_de_diferenca_operacional: >
      Como nenhuma das 9 hipoteses de codigo se sustenta e o roteiro
      completo passa em um processo real do proprio `demo/demo.py`, a
      explicacao mais provavel para o achado original e uma diferenca
      OPERACIONAL na sessao de validacao manual (nao de codigo) --
      candidatos plausiveis, nenhum verificavel por este ambiente
      automatizado: terminal/emulador ou locale sem suporte aos glifos
      "␣"/"⏎" usados nos chips (levando o validador a nao reconhecer o chip
      Marcar como presente/ativo), dimensoes de terminal na fronteira em
      que a barra de menus ocupa 2 linhas, ou uma sequencia de teclas
      diferente da literal (ex.: tecla fisica que nao emite 0x20).
    recomendacao: >
      Repetir a validacao manual (R06) SOMENTE a partir da etapa 10/17,
      sobre o estado atual do worktree; se a falha persistir ao vivo,
      registrar o terminal/emulador/locale exatos e a sequencia literal de
      teclas observada, pois nenhuma dessas variaveis e reproduzivel por
      este ambiente de execucao automatizado.
evidencias_separadas:
  - arquivo: demo/teste_demo_paginacao.py
    finalidade: >
      teste PTY ponta a ponta que documenta e trava (regressao futura) o
      comportamento correto observado nesta investigacao
    leitura_necessaria_para: [QA_POS_PATCH]
```

Omitir campos vazios. Não sobrescrever o relatório raiz nem o predecessor.
