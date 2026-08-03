---
name: REL-PATCH-H-0045-P01-paginacao-tty-chips-e-teclas
description: "Corrige ausência de chips [<]/[>] e ineficácia de , . < > no TTY do H-0045"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0045.md
  achados_tratados:
    - VM-H0045-01
---

# REL-PATCH-H-0045-P01 — Patch de implementação

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P01
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0045.md
falha_manual:
  rodada: R01
  teste: VM-H0045-01
  comando: python demo/demo.py h0045_paginacao_console_unico
  observado:
    - tela montada; indicador "página 1/3" presente
    - chips "[<]" e "[>]" ausentes
    - "," "." "<" ">" sem mudança de página
achados_tratados:
  - VM-H0045-01
achados_resolvidos:
  - VM-H0045-01
achados_pendentes: []
novos_achados: []
```

## 3. Diagnóstico (causa raiz)

```yaml
evidencias:
  1_politica_paginacao: "com" no JSON carregado (h0045_paginacao_console_unico)
  2_barra_declara_chips: chip_pagina_anterior/proxima com tecla "<"/">"
  3_existencia_pre_patch: console_tem_paginacao só True com console FOCADO
  4_chips_inativos: mecanismo cor_inativo já vigente; defeito era remoção por existência
  5_6_teclas: _ler_tecla_sessao devolve "," "." "<" ">" literais (não-Esc)
  7_8_9_processar: com foco, processar_comando altera pagina_atual e o loop redesenha
  10_testes_anteriores: chamavam processar_comando com foco_console=0; não exercitavam main/TTY sem foco
causa_raiz: >
  main() abria o cenário com foco_console=None. Sem foco, _linhas_barra
  filtrava [<]/[>] (existencia condicionada ao console focado) e
  processar_comando ignorava "," "." "<" ">" (console_focado ausente).
  O indicador na borda independe de foco — por isso 1/3 aparecia sozinho.
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VM-H0045-01
    alteracao: >
      (1) demo.py estabelece foco no primeiro console com politica_paginacao
      "com" ao abrir o cenário; (2) renderizador avalia console_com_paginacao
      sobre qualquer console da lista_foco; sem foco, chips ficam visíveis e
      inativos (D-PAG-13), nunca removidos.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P01.md
arquivos_alterados:
  - caminho: demo/demo.py
    delta: _estabelecer_foco_paginacao_inicial; chamada em main após carregar modelo
  - caminho: tela/renderizador.py
    delta: existencia estática de [<]/[>]; inativos sem foco paginado
  - caminho: demo/teste_demo_paginacao.py
    delta: teste cadeia TTY dos quatro caracteres + chips na página 1; chips sem foco
  - caminho: tela/teste_renderizador.py
    delta: regressão chips página 1 ([<] inativo visível, [>] ativo)
arquivos_removidos: []
documentos_normativos_alterados: []
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest
      tela/teste_paginacao.py tela/teste_navegacao.py
      tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 378 passed
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest
      tela/teste_paginacao.py tela/teste_navegacao.py
      tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 544 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 776 passed
  - comando_ou_metodo: python demo/demo.py h0045_paginacao_console_unico
    resultado_compacto: >
      quadro inicial com página 1/3, [<] inativo (cor_inativo), [>] ativo;
      "." e ">" avançam página via processar_comando
teste_regressao_adicionado: >
  test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1
  (_ler_tecla_sessao → processar_comando → renderizar_estado; "," "<" "." ">")
```

Verificação local não equivale a QA independente.

## 6. Bloqueios e validação manual

```yaml
bloqueios: []
validacao_manual:
  rodada_anterior: R01_REPROVADA
  nova_rodada: PENDENTE_USUARIO
  observacao: implementação não declara R02 aprovada
proxima_acao: QA_IMPLEMENTACAO_PATCH
```
