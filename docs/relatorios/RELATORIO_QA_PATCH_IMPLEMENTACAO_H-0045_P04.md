---
name: REL-QA-H0045-P04-unicidade-ids-consoles
description: "QA pos-patch do P04: rejeicao de IDs de console duplicados no loader"
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: IMPLEMENTACAO
  status: I5_MANUAL_VALIDATION_REQUIRED
  data: 2026-07-31
rastreabilidade:
  autorizacao_qa: null
  adr_auditada: null
  relatorio_aplicacao: null
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  relatorio_impl: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P04.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P03.md
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas: []
  issues_relacionadas: []
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P04.md
  achados_tratados:
    - QA-H0045-P03-001
---

# REL-QA-H0045-P04 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: QA pos-patch P04 — unicidade de IDs de console no loader
etapa_qa: QA_POS_PATCH
camada_auditada: IMPLEMENTACAO
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: APROVADO_SEM_ACHADOS_BLOQUEANTES
proxima_categoria: VALIDACAO_MANUAL_R04
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: patch P04 (tela/loader.py, tela/renderizador.py, tela/teste_loader.py, tela/teste_renderizador.py, demo/teste_demo_paginacao.py)
autoridades_materiais:
  - docs/contratos/contrato_console.md §3 (linha 119): "Identificador estável e único do elemento no escopo do tela.json"
escopo:
  - abrangencia da validacao de unicidade (_iterar_consoles_do_corpo / _validar_unicidade_ids_consoles / chamada em carregar_tela)
  - rejeicao de duplicatas (mensagem, ausencia de estado parcial)
  - preservacao de estruturas validas (P01/P02/P03)
  - documentacao do renderer sem fallback novo
```

Isolamento do delta do P04: nada foi commitado desde antes de H-0045 (HEAD `b88e49b`), portanto `git diff` acumula P01–P04. O isolamento foi feito por `find . -newer <RELATORIO_QA_..._P03.md>`, confirmando que somente os 5 arquivos declarados (mais o próprio relatório do P04) foram tocados após o QA do P03.

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V1
    comando_ou_metodo: leitura de tela/loader.py::_iterar_consoles_do_corpo/_validar_unicidade_ids_consoles e chamada em carregar_tela (linha 1502, apos validar toda a arvore e antes de qualquer construcao do dict de retorno)
    evidencia_focal: recursao cobre consoles diretos e aninhados em grupo (qualquer profundidade, via chamada recursiva em tipo=="grupo"); nao filtra por navegabilidade; ignora tipos nao-console sem falso positivo; ids invalidos ja rejeitados antes (TelaElementoSemId/TelaGrupoInvalido) sao pulados sem mascarar o erro canonico anterior
    resultado: OK
  - id: V2
    comando_ou_metodo: leitura de tela/renderizador.py::_mesmo_console_de_contexto/_console_focalizavel_de_contexto/_console_focado_de_contexto/_console_original_de_contexto
    evidencia_focal: logica de casamento (identidade -> id) inalterada desde P03; apenas docstrings novas documentando a precondicao de unicidade agora garantida pelo loader; sem fallback novo; contexto inconsistente devolve o proprio elemento, nunca escolhe outro console
    resultado: OK
  - id: V3
    comando_ou_metodo: leitura de tela/navegacao.py, tela/paginacao.py, tela/selecao.py (uso de console.id como chave)
    evidencia_focal: cursores/pagina_atual/selecoes indexados por console.id em todos os pontos; nenhum desses modulos foi alterado pelo P04 (mtime anterior ao QA do P03) — consistente, pois a garantia de unicidade upstream no loader torna essas chaves inambiguas sem exigir mudanca de codigo ali
    resultado: OK
  - id: V4
    comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    evidencia_focal: 376 passed (inclui os 5 testes novos de unicidade no loader e os 2 novos no renderer/demo)
    resultado: OK
  - id: V5
    comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py tela/teste_selecao.py tela/teste_fluxo_execucao.py demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py demo/teste_demo_selecao.py demo/teste_demo.py -v
    evidencia_focal: 556 passed, sem regressao de P01/P02/P03, navegacao, selecao multipla ou fluxo focal
    resultado: OK
  - id: V6
    comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest (suite completa)
    evidencia_focal: 788 passed
    resultado: OK
```

## 4. Achados

nenhum

## 5. Delta de QA pós-patch

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P04.md
achados_tratados:
  - QA-H0045-P03-001
achados_resolvidos:
  - QA-H0045-P03-001
achados_pendentes: []
novos_achados: []
```

Verificação de resolução: `test_h0045_p04_loader_rejeita_ids_de_console_duplicados` (e as variantes paginado/não-paginado e grupo aninhado, `tela/teste_loader.py`) provam `TelaEstruturaInvalida` com os dois caminhos na mensagem; `test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao` (`tela/teste_renderizador.py`) prova ausência de quadro parcial; `test_h0045_p04_dois_consoles_ids_unicos_foco_cursor_e_paginas_independentes` (renderer) e `test_demo_h0045_p04_dois_consoles_ids_unicos_foco_e_paginas_independentes` (demo) provam foco/cursor/página exclusivos ao segundo console com IDs únicos — o cenário original do achado (cursor materializado em `a01` com `foco_console=1`) não se reproduz mais.

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest tela/teste_loader.py tela/teste_renderizador.py demo/teste_demo_paginacao.py
    resultado_compacto: 376 passed
    prova_semantica: aceitacao de IDs unicos, rejeicao de duplicatas (corpo direto, paginado/nao-paginado, grupo aninhado) com TelaEstruturaInvalida e ambos os caminhos na mensagem; ausencia de renderizacao parcial; foco/cursor/pagina exclusivos ao console correto
  - comando_ou_metodo: pytest ampliado (paginacao/navegacao/renderizador/loader/selecao/fluxo_execucao/demos)
    resultado_compacto: 556 passed
    prova_semantica: regressao de P01/P02/P03 preservada
  - comando_ou_metodo: pytest (suite completa)
    resultado_compacto: 788 passed
    prova_semantica: nenhuma regressao automatizada em todo o repositorio
demonstracao:
  resultado: APROVADO_AUTOMATIZADO_NO_CAMINHO_NOMINAL
  evidencia: |
    printf '.\n\x1b[B\n,\n' | COLUMNS=80 LINES=24 python demo/demo.py h0045_paginacao_console_unico
    Sequencia observada identica ao relatorio do patch: item_01 (pagina 1/3) -> "." -> item_17 (pagina 2/3) -> seta -> item_18 (pagina 2/3) -> "," -> item_01 (pagina 1/3). Cursor, barra [Esc]/[<]/[>]/[✥] e chips preservados. A rejeicao de duplicatas nao foi demonstrada por fixture nova, apenas pelos testes automatizados acima (conforme instrucao).
validacao_manual:
  necessaria: true
  metodo_reproduzivel: printf '.\n\x1b[B\n,\n' | COLUMNS=80 LINES=24 python demo/demo.py h0045_paginacao_console_unico
  resultado: PENDENTE_USUARIO_R04
  criterios_pendentes:
    - confirmacao visual TTY real do usuario (R04)
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
  staged: vazio
  unstaged: conforme esperado para H-0045 acumulado (P01-P04), sem arquivo fora do escopo declarado do P04
  nao_rastreados: fixtures/relatorios previos de H-0045, conforme esperado
```

Nenhum item inesperado. Isolamento por mtime confirmou que somente os 5 arquivos declarados foram alterados pelo P04.

## 9. Conclusão

O patch P04 resolve QA-H0045-P03-001: a unicidade de `id` de console é validada recursivamente (corpo direto e aninhado em grupo, qualquer profundidade, independente de navegabilidade) antes de qualquer construção de runtime, com `TelaEstruturaInvalida` e mensagem identificando os dois caminhos; nenhuma renderização parcial ocorre. A autoridade de unicidade já existe em `contrato_console.md §3`; a correção é validação estrutural, não schema novo. O renderer não recebeu fallback novo — apenas documentação da precondição agora garantida. Regressão integral (788 testes) sem falhas. Aprovado para validação manual R04.
