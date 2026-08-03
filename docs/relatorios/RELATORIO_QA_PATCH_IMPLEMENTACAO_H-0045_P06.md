---
name: REL-QA-H0045-P06-autoridade-geometrica-unica
description: "Auditoria QA_POS_PATCH do P06: achados P05 resolvidos nos cenarios diretos, com novo bloqueio em geometria_console para console ausente/em grupo"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-31
rastreabilidade:
  autorizacao_qa: null
  adr_auditada: null
  relatorio_aplicacao: null
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P06.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P05.md
  contrato_alvo: null
  adr_relacionadas: []
  issues_relacionadas: []
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P06.md
  achados_tratados:
    - QA-H0045-P05-001
    - QA-H0045-P05-002
---

# REL-QA-H0045-P06 - Relatorio de QA

## 1. Identificacao e status

```yaml
revisao: QA_POS_PATCH do P06 - autoridade geometrica unica
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: P06 / QA-H0045-P05-001 / QA-H0045-P05-002
autoridades_materiais:
  - docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  - docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P05.md
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P06.md
  - tela/renderizador.py::_geometria_por_console
  - tela/renderizador.py::geometria_console
  - tela/renderizador.py::_renderizar_container_horizontal
  - tela/paginacao.py::_geometria_do_estado
  - demo/demo.py::_com_geometria_real_do_console
  - demo/demo.py::_reconciliar_paginacao_apos_resize
escopo:
  - autoridade geometrica unica por console
  - renderer horizontal e plano de paginacao
  - runtime interativo sem fallback altura-8
  - consoles diretos e consoles dentro de grupo permitido
```

## 3. Verificacoes executadas

```yaml
verificacoes:
  - id: entrada
    comando_ou_metodo: git branch/status/stage e existencia de relatorios
    evidencia_focal: branch master; HEAD b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96; stage vazio; relatorio P06 presente; relatorio QA P06 ausente antes desta auditoria
    resultado: OK
  - id: diff_focal
    comando_ou_metodo: git diff --name-only/--stat nos caminhos focais
    evidencia_focal: diff local mostra demo/demo.py, tela/renderizador.py, tela/teste_navegacao.py, tela/teste_renderizador.py e tela/navegacao.py; demo/teste_demo_paginacao.py e tela/paginacao.py estao nao rastreados no worktree acumulado
    resultado: INCOMPLETA
  - id: p05_001_dois_consoles_horizontais
    comando_ou_metodo: demonstracao programatica sem TTY sobre h0045_dois_consoles_paginas_independentes, largura 80, altura 20
    evidencia_focal: geometria_console retorna largura 40 e altura_interna 12 por console; render final indica pagina 1/1 em ambos; a11/b09 aparecem e ha cursor visivel unico
    resultado: OK
  - id: p05_002_comandos_e_setas
    comando_ou_metodo: demonstracao programatica sem TTY sobre h0045_paginacao_console_unico, largura 45, altura 10
    evidencia_focal: seta para baixo permanece na pagina 17 e no cursor item_17; '.' avanca para pagina 18/cursor item_18; ',' retorna para pagina 17/cursor item_17
    resultado: OK
  - id: fallback_altura_8
    comando_ou_metodo: busca textual por "altura - 8" e equivalentes
    evidencia_focal: tela/paginacao.py::_geometria_do_estado preserva fallback_para_api_sem_contexto; tela/fluxo_execucao.py::_reconciliar_paginas usa fallback legado fora do caminho auditado; demo.processar_comando injeta largura/altura_interna reais antes de Tab/Shift-Tab/paginas/setas paginadas
    resultado: OK
  - id: console_ausente_e_grupo
    comando_ou_metodo: leitura de tela/renderizador.py e demonstracao programatica sem TTY com console ausente e console paginado dentro de grupo
    evidencia_focal: geometria_console retorna a primeira geometria calculada quando console.id nao esta em _geometria_por_console; _geometria_por_console declara que nao recursiona em grupo/matriz; chamadas para console ausente e para console interno retornaram {'largura': 80, 'altura_interna': 17} em vez de None/erro/geometry do console
    resultado: FALHA
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidencia focal | Impacto | Correcao necessaria |
|---|---|---|---|---|---|
| QA-H0045-P06-001 | BLOQUEANTE | A geometria por console deve ser por `console.id`, incluindo console dentro de grupo permitido, e ausencia de console nao deve produzir correspondencia silenciosa. | Em `tela/renderizador.py`, `_geometria_por_console` popula somente elementos diretos do corpo e documenta que nao recursiona em `grupo`/`estrutura: matriz`; `geometria_console` retorna `next(iter(geometria.values()))` quando o `console.id` nao aparece. Demonstracao programatica: um console ausente e um console paginado dentro de grupo receberam ambos `{'largura': 80, 'altura_interna': 17}` por fallback silencioso. | O runtime de H-0045 usa `lista_foco`, que atravessa grupos. Para console paginado interno, comandos de pagina, setas e reconciliacao podem receber geometria de outro elemento/topo, reintroduzindo divergencia entre plano logico e quadro renderizado em composicoes permitidas. | Fazer a autoridade geometrica mapear consoles reais recursivamente pelos mesmos containers do renderer, ou retornar `None`/falhar quando o console solicitado nao estiver no mapa; remover fallback silencioso da API especifica por console. |

## 5. Delta de QA pos-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P06.md
achados_tratados:
  - QA-H0045-P05-001
  - QA-H0045-P05-002
achados_resolvidos:
  - QA-H0045-P05-001
  - QA-H0045-P05-002
achados_pendentes:
  - QA-H0045-P06-001
novos_achados:
  - QA-H0045-P06-001
```

## 6. Testes, demonstracao e validacao manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_renderizador.py demo/teste_demo_paginacao.py -q -p no:cacheprovider
    resultado_compacto: 393 passed
    prova_semantica: cobre os cenarios diretos declarados pelo P06 para dois consoles horizontais, comandos de pagina, setas e distribuicao vertical
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
    resultado_compacto: 795 passed
    prova_semantica: regressao completa verde; nao cobre o achado de console ausente/em grupo
validacao_manual:
  necessaria: false
  metodo_reproduzivel: null
  resultado: NAO_EXECUTADA_POR_INSTRUCAO
  criterios_pendentes:
    - validacao manual R05 consolidada nao deve iniciar ate novo patch de implementacao
```

## 7. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
  staged: vazio
  unstaged: worktree acumulado H-0045/P01-P06, sem limpeza/restauracao
  nao_rastreados: fixtures, modulos/testes/relatorios H-0045 acumulados; este relatorio criado por esta auditoria
itens_inesperados:
  - item: tela/navegacao.py aparece no diff focal, mas nao nos seis arquivos declarados pelo relatorio P06
    origem: NAO_CONFIRMADA
    evidencia: git diff --name-only focal lista tela/navegacao.py; o worktree esta acumulado e nao ha separacao local confiavel por patch
```

## 8. Conclusao

O P06 resolve materialmente os dois achados P05 nos cenarios diretos auditados: o renderer horizontal recebe `altura_alvo`, os comandos e setas paginadas usam geometria real, e o fallback `altura - 8` nao foi acionado no caminho interativo coberto. A aprovacao ainda fica bloqueada porque a nova autoridade `geometria_console` nao e segura por `console.id`: consoles ausentes ou dentro de grupo recebem uma geometria silenciosamente reaproveitada de outro elemento. Status: `I2_IMPLEMENTATION_PATCH_REQUIRED`.
