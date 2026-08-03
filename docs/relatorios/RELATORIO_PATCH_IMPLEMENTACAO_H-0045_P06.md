---
name: REL-PATCH-H-0045-P06-autoridade-geometrica-unica
description: "Unifica a autoridade geometrica de renderer, resize, comandos de pagina e setas; corrige capacidade 1 forcada em arranjo horizontal e o fallback altura-8 no caminho interativo"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P05.md
  achados_tratados:
    - QA-H0045-P05-001
    - QA-H0045-P05-002
---

# REL-PATCH-H-0045-P06 — Patch de implementação

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P06
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P05.md
achados_tratados: [QA-H0045-P05-001, QA-H0045-P05-002]
achados_resolvidos: [QA-H0045-P05-001, QA-H0045-P05-002]
achados_pendentes: []
novos_achados: []
```

## 3. Causa raiz comum

Os dois achados compartilham a mesma origem: **duas autoridades de geometria calculavam valores diferentes para o mesmo console**.

1. `_renderizar_container_horizontal` nunca repassava `altura_disponivel` como `altura_alvo` a `_caixa_de_elemento` para elementos diretos (apenas para `grupo`). Um console paginado dentro de uma coluna horizontal chamava `_fragmentos_e_total_paginacao` com `altura_alvo=None`, cuja regra interna (`capacidade = 1 if altura_alvo is None else ...`) forçava capacidade **1**, mascarada apenas depois por um preenchimento posterior que só ajusta linhas de fill, nunca a paginação real. `altura_interna_disponivel` (P05), por outro lado, calculava corretamente `l_corpo_disponível - 2` para colunas horizontais — mas esse valor nunca chegava ao render real. Daí a divergência 12↔1 do achado 001.
2. `tela.paginacao._geometria_do_estado` usa `altura - 8` sempre que `estado["altura_interna"]` está ausente. `demo.processar_comando` nunca populava essa chave fora de `_reconciliar_paginacao_apos_resize` — logo, `.`/`>`/`,`/`<` e as setas (via `linhas_logicas_navegaveis_da_pagina`) sempre operavam sobre a aproximação fixa, divergente de `l_barra` real (achado 002).

## 4. Autoridade geométrica única adotada

`tela/renderizador.py` ganhou `_geometria_por_console` (privada): reproduz `l_cab`/`l_barra`/particionamento vertical (`_distribuir_alturas`) ou colunas horizontais (`_distribuir_larguras`, mesma altura plena) de UMA vez para todos os elementos de primeiro nível, sem materializar texto. `geometria_console(...)` (pública) seleciona a entrada de um console (`{"largura", "altura_interna"}`); `altura_interna_disponivel` vira wrapper retrocompatível. `_renderizar_container_horizontal` foi corrigido para repassar `altura_alvo=altura_disponivel` a `_caixa_de_elemento` (idempotente para conteúdo não paginado). `demo.py` ganhou `_com_geometria_real_do_console`, que injeta `largura`/`altura_interna` reais no `nav_estado` antes de qualquer comando de página ou seta sobre console **paginado** (Tab/Shift-Tab, `.`/`>`/`,`/`<`, setas); `_reconciliar_paginacao_apos_resize` passou a usar `geometria_console` (largura + altura) em vez de só altura. `tela.paginacao.reconciliar_pagina_com_cursor` ganhou parâmetro `largura` (mesmo padrão de `altura_interna`, precedência sobre `_geometria_do_estado`).

## 5. Correção de instrução (setas) — prevalece o handoff

O prompt original citava "seta em item_17 move para item_18" para 1 item/página; o usuário corrigiu: prevalece H-0045/D15 — **setas nunca mudam de página**, restritas aos itens navegáveis da página visual atual; com 1 item, seta produz SEM_MOVIMENTO; somente `.`/`>`/`,`/`<` avançam página. Implementado assim: `_com_geometria_real_do_console` alimenta `linhas_logicas_navegaveis_da_pagina` com geometria real (não amplia para o grid completo).

## 6. Fallback `altura - 8`

```yaml
classificacao:
  - uso: runtime_interativo
    caminhos: [demo.processar_comando (Tab/setas/paginas), _reconciliar_paginacao_apos_resize]
    status: ELIMINADO — geometria real injetada antes de qualquer chamada a tela.paginacao/tela.navegacao
  - uso: fallback_para_chamador_sem_contexto_visual
    caminhos: [tela.paginacao._geometria_do_estado, reconciliar_pagina_com_cursor sem largura/altura_interna]
    status: preservado, documentado, nunca acionado pelo runtime
  - uso: somente_teste_legado
    caminhos: [chamadas diretas a paginacao.* em testes sem geometria explícita]
    status: preservado
```

## 7. Delta aplicado

```yaml
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: _geometria_por_console + geometria_console (nova autoridade única); altura_interna_disponivel vira wrapper; _renderizar_container_horizontal repassa altura_alvo
  - caminho: tela/paginacao.py
    delta: reconciliar_pagina_com_cursor ganha parametro largura
  - caminho: demo/demo.py
    delta: geometria_console importada; _com_geometria_real_do_console + _chips_destacados_e_executar; injeção em Tab/Shift-Tab/paginas/setas; _reconciliar_paginacao_apos_resize usa geometria_console
  - caminho: tela/teste_navegacao.py
    delta: corrigida asserção que dependia do bug (h0040_nav_tres_consoles_em_grupo agora renderiza, não cai em quadro mínimo)
  - caminho: tela/teste_renderizador.py
    delta: teste P04 corrigido (capacidade real, não mais forçada) + teste novo de distribuição vertical (Teste 5)
  - caminho: demo/teste_demo_paginacao.py
    delta: _passo_tty renderiza na largura/altura do estado (não mais 80 fixo); teste P04 corrigido; 4 testes novos (dois consoles horizontais, seta 1 item/página, comandos de página, sequência integrada)
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P06.md
documentos_normativos_alterados: []
```

## 8. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: pytest tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 393 passed (5 novos)
  - comando_ou_metodo: pytest ...(+loader/selecao/fluxo_execucao/demo_navegacao/demo_selecao/demo) -v
    resultado_compacto: 563 passed
  - comando_ou_metodo: pytest (suite completa)
    resultado_compacto: 795 passed (790 anterior + 5 novos), sem regressão
```

## 9. Demonstração automatizada

Script ad-hoc (sem TTY) cobrindo console único, dois consoles horizontais, 1 item/página, seta, `.`, `,`, resize, troca de console e seleção preservada — quadro final verificado em cada passo: 11/11 verificações OK.

## 10. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P05.md
    finalidade: achados QA-H0045-P05-001/002 tratados por este patch
    leitura_necessaria_para: [cadeia P05]
```

## 11. Validação manual

```yaml
progresso_anterior: 6/17
nova_rodada: PENDENTE_USUARIO_R05_CONSOLIDADA
status: BLOQUEADA_ATE_QA_DO_P06
```
