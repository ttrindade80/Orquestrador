---
name: REL-PATCH-H-0045-P03-cursor-navegacao-paginacao
description: "Corrige ausência do cursor e da navegação visual de itens em consoles paginados (R03)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
  achados_tratados:
    - VM-H0045-R03-003
---

# REL-PATCH-H-0045-P03 — Patch de implementação

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P03
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
patches_anteriores:
  P01: {efeito: ["[<]"/"[>]" visíveis, comandos ", . < >" funcionais]}
  P02: {efeito: [geometria da barra corrigida, resíduos pós-resize eliminados]}
falha_manual:
  rodada: R03
  progresso: 6/17
  id: VM-H0045-R03-003
  severidade: BLOQUEANTE
  componente: cursor_e_navegacao_de_itens
  observado:
    - cursor ausente em qualquer página (1 a 34 páginas)
    - itens sem navegação visual
    - "[✥] Navegar" visível (>1 navegável no contexto)
achados_tratados: [VM-H0045-R03-003]
achados_resolvidos: [VM-H0045-R03-003]
achados_pendentes: []
novos_achados: []
```

## 3. Diagnóstico (causa raiz)

```yaml
perguntas:
  1_foco_valido_pos_p01: sim
  2_cursores_recebe_entrada: sim (cursores[console.id]=0 na abertura)
  3_quem_inicializa: "_estabelecer_foco_paginacao_inicial (abertura) e paginacao.ir_para_pagina (troca de página) — ambos corretos"
  4_ordem_vs_primeiro_render: inicialização ocorre ANTES do primeiro render
  5_troca_pagina_grava_primeiro_navegavel: sim (ir_para_pagina/primeiro_item_logico_da_pagina)
  6_indice_global_ou_local: GLOBAL (mesma autoridade de navegacao.grade_de_itens e paginacao.mapa_fisico_de_itens)
  7_renderer_interpreta_mesmo_indice: "NÃO — causa raiz nº2 (ver abaixo)"
  8_plano_associa_item_e_fragmento: sim (tela/paginacao.py correto; defeito é só do lado do renderer)
  9_primeira_linha_marcada_focalizavel: sim (_elemento_fragmentado_para_pagina correto)
  10_cursor_descartado_indice_global_vs_local: "sim — causa raiz nº2"
  11_recorte_transitorio_remove_ou_renumera: "remove (lista local do clone só tem itens da página) — correto para composição visual, mas reusado indevidamente para localizar o cursor"
  12_renderer_recebe_cursores_atualizado: sim
  13_simbolo_existe_mas_invisivel: "não — causa raiz nº1 impede a própria RESERVA da coluna (ind_w=0)"
  14_navegar_e_cursor_autoridades_divergentes: "sim, confirmado — ver causa_raiz_1"
  15_testes_so_verificavam_estado_cursores: "em parte — nenhum teste existente buscava o símbolo do cursor no quadro renderizado"
causa_raiz_1_identidade_de_objeto: >
  _console_focalizavel_de_contexto/_console_focado_de_contexto comparavam por
  identidade (`is`) contra lista_foco. No caminho de paginação matricial
  (_caixa_de_elemento -> _elemento_fragmentado_para_pagina), o console é
  CLONADO (copy.copy) por página, com _campos_inertes["itens"] substituído
  pela fatia física da página. O clone nunca É (is) o objeto original em
  lista_foco: eh_console_com_indicador ficava sempre False, a coluna do
  indicador nunca era reservada e o símbolo nunca era emitido — em NENHUMA
  página, para qualquer console paginado com distribuicao_matricial (todos
  os fixtures H-0045).
causa_raiz_2_indice_global_vs_local: >
  Corrigindo (1), _item_corrente_de_contexto resolvia cursores[console.id]
  (índice GLOBAL) contra _itens_navegaveis_do_elemento(elemento) do PRÓPRIO
  elemento recebido — que no caminho de paginação é a lista LOCAL (só os
  itens da página). A partir da segunda página o índice global excede/
  desalinha a lista local: o item corrente deixava de ser localizado.
achado_correlato_resize: >
  pagina_atual[console.id] não era recalculada após redimensionamento
  (altura muda -> altura_interna muda -> distribuição por página muda). A
  página antiga era só clampada ao novo total, podendo deixar de conter o
  item lógico do cursor: o cursor sumia apenas por mudar a altura do
  terminal, violando o requisito de preservação do item lógico (D10).
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VM-H0045-R03-003
    alteracao: >
      (1) tela/renderizador.py: _console_focalizavel_de_contexto e
      _console_focado_de_contexto passam a casar também por id do console
      (_mesmo_console_de_contexto), reconhecendo o clone de paginação como o
      mesmo console da lista de foco; nova _console_original_de_contexto
      resolve o console de lista completa correspondente a um elemento
      potencialmente clonado; _item_corrente_de_contexto resolve o índice
      GLOBAL contra essa lista completa, não mais contra a lista local do
      clone. (2) tela/paginacao.py: nova reconciliar_pagina_com_cursor
      recalcula pagina_atual[console.id] para a página que contém o item
      lógico do cursor, sob a geometria corrente. (3) demo/demo.py: nova
      _reconciliar_paginacao_apos_resize, chamada no bloco de redesenho por
      SIGWINCH após atualizar largura/altura/desconto_estrutural e antes de
      renderizar — percorre todos os consoles paginados da lista de foco
      (páginas independentes preservadas).
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: >
      _mesmo_console_de_contexto (novo helper de identidade/id);
      _console_focalizavel_de_contexto e _console_focado_de_contexto casam
      por id; nova _console_original_de_contexto;
      _item_corrente_de_contexto resolve contra a lista completa
  - caminho: tela/paginacao.py
    delta: nova reconciliar_pagina_com_cursor(estado, console)
  - caminho: demo/demo.py
    delta: >
      nova _reconciliar_paginacao_apos_resize; chamada no bloco SIGWINCH
      antes de _apresentar_quadro
  - caminho: demo/teste_demo_paginacao.py
    delta: >
      dois testes ponta a ponta novos (ciclo completo de navegação + resize
      1/3/muitas páginas; página intermediária sem navegáveis)
arquivos_removidos: []
documentos_normativos_alterados: []
preservacoes:
  - patches P01 e P02 (chips, comandos de página, geometria da barra, sem resíduo)
  - indicador "página X/Y"; "[<]"/"[>]"; "[✥]"; seleção múltipla; "Todos"
  - modo verboso; políticas de quebra; fluxo focal da ADR-0037
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py
      tela/teste_navegacao.py tela/teste_renderizador.py
      demo/teste_demo_paginacao.py -v
    resultado_compacto: 383 passed
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py
      tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 549 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 781 passed
  - comando_ou_metodo: >
      printf '.\n\x1b[B\n,\n' | COLUMNS=80 LINES=24 python demo/demo.py
      h0045_paginacao_console_unico (pipe, não-TTY)
    resultado_compacto: >
      cursor "→" visível em item_01 (pág.1/3); avança para item_17 (pág.2/3);
      seta move para item_18 na mesma página; "," retorna a item_01 (pág.1/3);
      barra e chips [<]/[>]/[✥] preservados em todos os quadros
validacao_manual:
  progresso_anterior: 6/17
  nova_rodada: PENDENTE_USUARIO_R04
```

Verificação local não equivale a QA independente. A validação TTY real (terminal interativo) permanece pendente do usuário — as verificações acima cobrem o caminho não-TTY (pipe) e a suíte automatizada.

## 6. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P02.md
    finalidade: predecessor aprovado (geometria da barra)
    leitura_necessaria_para: [cadeia P02]
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
    finalidade: QA do P02
    leitura_necessaria_para: [cadeia]
```
