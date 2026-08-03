---
name: REL-QA-H0045-P03-cursor-navegacao-paginacao
description: "Auditoria independente pos-patch P03 do H-0045"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-31
rastreabilidade:
  autorizacao_qa: null
  adr_auditada: docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0038.md
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas: []
  issues_relacionadas: [ITEM-0003]
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
  achados_tratados: [VM-H0045-R03-003]
---

# REL-QA-H0045-P03 - Relatorio de QA

## 1. Identificacao e status

```yaml
revisao: REL-QA-H0045-P03-cursor-navegacao-paginacao
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: Patch P03 da implementacao de paginacao H-0045
autoridades_materiais:
  - docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
  - docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
arquivos_auditados:
  - tela/renderizador.py
  - tela/paginacao.py
  - tela/navegacao.py
  - demo/demo.py
  - demo/teste_demo_paginacao.py
  - docs/templates/TEMPLATE_RELATORIO_QA.md
escopo:
  - VM-H0045-R03-003: cursor ausente, navegacao visual ausente e cursor desaparecendo apos resize
  - preservacao direta de P01/P02, sem validacao manual TTY
```

## 3. Verificacoes executadas

```yaml
verificacoes:
  - id: VAL-INICIAL
    comando_ou_metodo: git branch/status/stage e existencia de relatorios
    evidencia_focal: branch master; HEAD b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; P03 presente; este relatorio inexistente antes da auditoria.
    resultado: OK
  - id: VAL-IDENTIDADE-NOMINAL
    comando_ou_metodo: auditoria estatica de _mesmo_console_de_contexto, _console_focalizavel_de_contexto, _console_focado_de_contexto e _console_original_de_contexto
    evidencia_focal: clone paginado com mesmo id e reconhecido; comparacao por identidade permanece valida; console original e resolvido pela lista de foco. Entretanto, ids duplicados aceitos pelo loader criam correspondencia silenciosa indevida.
    resultado: FALHA
  - id: VAL-INDICE-GLOBAL
    comando_ou_metodo: auditoria estatica e teste renderizado em pagina com primeiro indice global maior que zero
    evidencia_focal: _item_corrente_de_contexto resolve cursores[console.id] contra o console original completo; pagina 2 renderiza cursor em item_17 e seta move para item_18.
    resultado: OK
  - id: VAL-RENDER-CURSOR
    comando_ou_metodo: auditoria estatica, testes P03 e demonstracao por pipe
    evidencia_focal: coluna do indicador reservada; simbolo "->"/estilo real "→" materializado no item corrente; paginas sem navegaveis nao exibem cursor; pagina com multiplos navegaveis diferencia [✥] e cursor.
    resultado: OK
  - id: VAL-PAGINACAO-SETAS-RESIZE
    comando_ou_metodo: auditoria de processar_comando, reconciliar_pagina_com_cursor, _reconciliar_paginacao_apos_resize e fluxo SIGWINCH
    evidencia_focal: ./> e ,/< reposicionam cursor no primeiro navegavel da pagina; setas usam linhas_logicas_navegaveis_da_pagina e nao mudam pagina; SIGWINCH atualiza geometria antes de reconciliar cada console paginado.
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidencia focal | Impacto | Correcao necessaria |
|---|---|---|---|---|---|
| QA-H0045-P03-001 | BLOQUEANTE | Correspondencia por ID nao pode ser ambigua; foco de um console nao pode produzir cursor em outro. | O loader aceitou uma tela derivada de `h0045_dois_consoles_paginas_independentes` com dois consoles `id: console_a`. Com `foco_console: 1`, `renderizar_estado` materializou o cursor em `a01` no primeiro console, nao no segundo (`cursor_count=1`, linha observada: `│  → a01 ... ││    b01 ... │`). A causa direta e `_mesmo_console_de_contexto`, que casa por `e.id == elemento.id` sem garantir unicidade no contexto. | Dois consoles podem compartilhar estado/chave de cursor ou foco por correspondencia inadequada quando IDs duplicados entram por caminho aceito pelo loader. | Impedir ambiguidade antes da correspondencia por id: rejeitar IDs duplicados no modelo/loader aplicavel ou fazer o helper casar por id somente quando a correspondencia for unica no contexto. |

## 5. Delta de QA pos-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
achados_tratados:
  - VM-H0045-R03-003
achados_resolvidos: []
achados_pendentes:
  - VM-H0045-R03-003
novos_achados:
  - QA-H0045-P03-001
causa_raiz:
  confirmada_no_caminho_nominal:
    - clone paginado nao era reconhecido por comparacao de identidade
    - cursor global era resolvido contra lista local recortada
    - pagina atual precisava reconciliar com o cursor apos resize
  rejeitada_como_solucao_completa:
    - correspondencia por id sem prova de unicidade permite ambiguidade bloqueante
```

## 6. Testes, demonstracao e validacao manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 383 passed
    prova_semantica: cobre cursor renderizado, pagina 1/3, pagina 2 com item_17, seta para item_18, retorno, resize 1/1 -> muitas -> 3 paginas, pagina sem navegaveis, [✥] e cursor por assercoes distintas.
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py tela/teste_selecao.py tela/teste_fluxo_execucao.py demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 549 passed
    prova_semantica: regressao ampliada de P01, P02, navegacao, loader, selecao, fluxo focal e demos.
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 781 passed
    prova_semantica: suite completa sem regressao automatizada.
  - comando_ou_metodo: auditoria estatica dos dois testes P03 novos
    resultado_compacto: OK
    prova_semantica: os testes verificam o quadro renderizado e nao monkeypatcham o resultado que deveriam comprovar.
demonstracao:
  resultado: APROVADO_AUTOMATIZADO_NO_CAMINHO_NOMINAL
  evidencia: |
    printf '.\n\x1b[B\n,\n' | COLUMNS=80 LINES=24 python demo/demo.py h0045_paginacao_console_unico
    Quadro inicial mostra "→ item_01" em "pagina 1/3"; "." mostra "→ item_17" em "pagina 2/3"; seta baixo mostra "→ item_18" ainda em "pagina 2/3"; "," retorna a "→ item_01" em "pagina 1/3"; barra e chips preservados.
validacao_manual:
  necessaria: true
  metodo_reproduzivel: VALIDACAO_MANUAL_R04 apos patch corretivo do achado bloqueante.
  resultado: PENDENTE_USUARIO_R04_BLOQUEADA_POR_PATCH
  criterios_pendentes:
    - validacao visual TTY real do usuario apos correcao de QA-H0045-P03-001
```

## 7. Evidencias separadas

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P03.md
    finalidade: declaracao do patch P03 e causa raiz proposta
    leitura_necessaria_para: [delta P03]
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P02.md
    finalidade: preservacao do P02
    leitura_necessaria_para: [cadeia P02]
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
  staged: []
  preexistentes_modificados_ou_nao_rastreados: muitos artefatos da cadeia H-0045 ja estavam presentes antes desta auditoria
  criado_por_esta_auditoria:
    - docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P03.md
itens_inesperados:
  - item: git diff focal contra HEAD lista apenas demo/demo.py e tela/renderizador.py; tela/paginacao.py e demo/teste_demo_paginacao.py aparecem como nao rastreados nesta arvore
    origem: NAO_CONFIRMADA
    evidencia: "git diff -- tela/renderizador.py tela/paginacao.py demo/demo.py demo/teste_demo_paginacao.py nao inclui arquivos nao rastreados"
```

## 9. Conclusao

O P03 corrige o caminho nominal de VM-H0045-R03-003: cursor aparece no quadro, usa indice logico global, navega dentro da pagina, troca pagina sem wrap e preserva o item logico apos resize. P01 e P02 permanecem preservados e as suites automatizadas passaram.

A aprovacao nao pode avancar para validacao manual porque a nova equivalencia por `id` e ambigua quando IDs duplicados sao aceitos pelo loader. O resultado e bloqueante pelo criterio expresso desta auditoria: consoles podem compartilhar cursor/foco por correspondencia inadequada. Status final: `I2_IMPLEMENTATION_PATCH_REQUIRED`.
