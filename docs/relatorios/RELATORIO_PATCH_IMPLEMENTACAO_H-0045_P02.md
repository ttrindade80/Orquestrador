---
name: REL-PATCH-H-0045-P02-geometria-barra-resize
description: "Corrige desalinhamento e resíduos da moldura da barra após resize (R02)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P01.md
  achados_tratados:
    - VM-H0045-R02-002
---

# REL-PATCH-H-0045-P02 — Patch de implementação

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P02
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P01.md
patch_anterior:
  id: P01
  status: APROVADO
  efeito_confirmado:
    - chips "[<]" e "[>]" visíveis
    - comandos "," "." "<" ">" funcionais
    - navegação entre páginas aprovada manualmente (R02)
falha_manual:
  rodada: R02
  id: VM-H0045-R02-002
  severidade: BLOQUEANTE
  componente: barra_de_menus
  observado_na_abertura:
    - moldura deslocada para a esquerda
    - trecho residual "│─────╯" à direita da barra
  observado_ao_reduzir:
    - conteúdo redesenhado em largura menor
    - resíduos da borda anterior à direita
    - barras verticais repetidas
  observado_ao_maximizar:
    - quadro ainda deslocado
  navegacao: APROVADA
achados_tratados:
  - VM-H0045-R02-002
achados_resolvidos:
  - VM-H0045-R02-002
achados_pendentes: []
novos_achados: []
```

## 3. Diagnóstico (causa raiz)

```yaml
perguntas:
  1_largura_calculada: >
    raw len(linha_barra)==total_w, mas largura VISUAL menor
    (ex.: raw=80, vis=70 com [<] inativo em cor_inativo)
  2_borda_esquerda: mesma origem (coluna 1 / "│ ") — OK
  3_borda_direita: deslocada à esquerda; pad usava len() com ANSI
  4_espacos_apagar: nao — pad visual insuficiente
  5_limpa_tela_inteira: nao; ESC[2J so na entrada da sessao
  6_ordem: le dimensoes novas, depois redesenha sem clear total
  7_linha_antiga_mais_longa: sim — sobrescrita parcial a direita
  8_limpeza: por linha (CSI n;1H + pad), nao por tela
  9_mistura_larguras: sim — len() bruto vs largura visual/ANSI
  10_testes_anteriores: quadros independentes; sem sequencia de tamanhos
diferenca_renderer_vs_limpeza: COMBINACAO
  renderer: >
    _linha_conteudo usava len()/slice brutos; chips com SGR ANSI
    encurtavam a moldura (borda direita cedo demais).
  limpeza: >
    _apresentar_quadro usava len(linha) para pad; com ANSI,
    pad=0 mesmo com visual < w — residuos a direita apos resize.
causa_raiz: >
  Combinacao de preenchimento da barra por len() bruto (ignorando SGR
  de cor_inativo do P01) e pad de redesenho por len() bruto. A moldura
  nasce visualmente curta; o loop nao apaga a area a direita.
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VM-H0045-R02-002
    alteracao: >
      (1) _linha_conteudo passa a truncar/preencher por largura visual
      (_cortar_sem_ansi / _ljust_sem_ansi); (2) _apresentar_quadro
      preenche por _largura_sem_ansi e emite CSI K apos cada linha;
      altura opcional para limpar linhas residuais (teste).
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P02.md
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: _cortar_sem_ansi; _linha_conteudo ANSI-aware
  - caminho: demo/demo.py
    delta: _apresentar_quadro pad visual + CSI K; import _largura_sem_ansi
  - caminho: tela/teste_renderizador.py
    delta: teste sequencial 100→60→100 na barra
  - caminho: demo/teste_demo_paginacao.py
    delta: sequencia resize + teste de limpeza _apresentar_quadro
arquivos_removidos: []
documentos_normativos_alterados: []
preservacoes:
  - indicador página X/Y
  - chips [<]/[>] e comandos , . < >
  - foco inicial P01; cores ativo/inativo; ordem; navegacao; selecao
  - cenarios sem paginacao; alternate screen / restauracao
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest
      tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 336 passed
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest
      tela/teste_paginacao.py tela/teste_navegacao.py
      tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 547 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 779 passed
  - comando_ou_metodo: python demo/demo.py h0045_paginacao_console_unico
    resultado_compacto: >
      barra com borda esquerda/direita alinhadas; [<] inativo;
      pagina 1/3; sem trecho residual apos a moldura no quadro inicial
validacao_manual:
  navegacao_paginas: APROVADA_R02
  barra_de_menus_resize: REPROVADA_R02
  nova_validacao: PENDENTE_USUARIO_R03
```

Verificação local não equivale a QA independente.

## 6. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P01.md
    finalidade: predecessor aprovado (chips/teclas)
    leitura_necessaria_para: [cadeia P01]
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P01.md
    finalidade: QA do P01
    leitura_necessaria_para: [cadeia]
```
