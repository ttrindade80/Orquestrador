---
name: REL-QA-PATCH-0045-P04-handoff
description: "QA independente do handoff H-0045 após o PATCH_HANDOFF P04"
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H2_HANDOFF_PATCH_REQUIRED
  data: "2026-08-02"
rastreabilidade:
  autorizacao_qa: "QA_HANDOFF — auditoria independente do handoff corrigido"
  adr_auditada: docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  handoff_origem: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  contrato_alvo: docs/contratos/contrato_console.md
  issues_relacionadas:
    - ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P04.md
  achados_tratados:
    - HANDOFF_METHOD_DEFECT
---

# REL-QA-PATCH-0045-P04 — QA do handoff corrigido

## 1. Identificação e status

```yaml
revisao: QA independente do H-0045 após PATCH_HANDOFF P04
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_HANDOFF
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
autoridades_materiais:
  - docs/contratos/contrato_console.md §12 v0.2
  - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0045_P04.md
  - docs/relatorios/RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md
escopo:
  - políticas de quebra, método de resize, três telas e escopo futuro
  - preservação dos achados VM-H0045-R06-001 e QA-H0045-P08-001
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: QA-P04-01
    comando_ou_metodo: leitura integral do contrato, ADR, handoff, cadeia P04/causa-raiz e templates autorizados
    evidencia_focal: §10/D-TEC-07 reproduz as três políticas de contrato_console.md §12; §19 exige modelo único, três telas, textos fixos, resize livre, testes estruturais e preserva 6/17–14/17 e os dois achados abertos
    resultado: OK
  - id: QA-P04-02
    comando_ou_metodo: leitura focal de demo/demo.py, demo/casos_validacao_paginacao.py e tela/paginacao.py
    evidencia_focal: SIGWINCH ainda chama o helper que recria itens e zera foco/cursor/página; os construtores ainda geram conteúdo a partir de W/C; o ramo condicional ainda cai no mesmo planejamento de evitar_quebra. O handoff identifica e autoriza tratar esses pontos
    resultado: OK
  - id: QA-P04-03
    comando_ou_metodo: git diff --check e verificação equivalente para o handoff não rastreado
    evidencia_focal: nenhuma mensagem de whitespace; saída do diff check com código 0 no caminho rastreado
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0045-P04-001 | alto | O handoff não deve autorizar mudança no renderer sem nova evidência e não pode conter contradição de escopo | §6.1 lista `tela/renderizador.py` como alterável e §8/D-TEC-04, 06, 11 ordenam sua extensão; §19.6 condiciona mudança no renderer a nova evidência, sem retirar ou delimitar a autorização anterior. A análise causal autorizada registra ausência de regressão no renderer | Implementador pode alterar o renderer sob a autorização geral, embora o patch metodológico exija uma fronteira mais estreita | Harmonizar §6.1, §8, D-TEC-04/11 e §19.6: remover a autorização ativa ou definir uma porta de evidência objetiva e aprovação específica |
| QA-H0045-P04-002 | alto | Os casos adaptativos antigos devem ser substituídos/desativados e o método não pode recriar modelo lógico durante resize | §18.2, §18.4 e §18.5 ainda tornam obrigatório o harness adaptativo e seis casos; §19.1 proíbe geração por W/C, §19.2–19.3 substitui quatro casos por três telas fixas, mas §19.4 diz ser adicional a §18.5 | Permanecem instruções incompatíveis: executar casos adaptativos proibidos ou manter uma obrigação de testes que o patch diz substituir | Declarar expressamente quais trechos de §18 ficam supersedidos, retendo apenas os casos fixos de VAZIO/CONTINUACAO e as três telas, e alinhar §19.4 |

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: auditoria documental e leitura focal autorizada; sem pytest ou execução TTY
    resultado_compacto: achados documentais reproduzidos; nenhuma implementação foi validada
    prova_semantica: não aplicável à etapa QA_HANDOFF
demonstracao:
  resultado: não executada
  evidencia: validação manual permanece reservada ao usuário em TTY real
validacao_manual:
  necessaria: true
  metodo_reproduzivel: §19.5 para as três telas; §18.6 para 16/17 e 17/17
  resultado: pendente; 6/17–14/17 não reexecutadas
  criterios_pendentes: [15/17, 16/17, 17/17]
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  staged: vazio
  unstaged: worktree já continha alterações acumuladas fora desta auditoria
  nao_rastreados: artefatos H-0045/P01–P15 já existentes; relatório QA atual criado nesta execução
itens_inesperados: []
```

## 9. Conclusão

O P04 corrige materialmente as três políticas, a proibição de reconstrução e o roteiro em três telas, preservando os itens manualmente aprovados e os achados abertos. O handoff ainda precisa de patch para fechar a autorização do renderer e eliminar a obrigação residual do harness adaptativo; portanto, não está aprovado.
