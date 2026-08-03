---
name: REL-PATCH-H-0045-P04-unicidade-ids-consoles
description: "Rejeita IDs de console duplicados antes do runtime (QA-H0045-P03-001)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045 / ITEM-0003
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P03.md
  achados_tratados:
    - QA-H0045-P03-001
---

# REL-PATCH-H-0045-P04 — Patch de implementação

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
patch_id: P04
handoff: H-0045
item: ITEM-0003
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P03.md
patches_anteriores:
  P01: {efeito: ["[<]"/"[>]" visíveis, comandos funcionais]}
  P02: {efeito: [geometria da barra, limpeza pós-resize]}
  P03: {efeito: [cursor visível, índice global, setas, páginas, resize]}
achados_tratados: [QA-H0045-P03-001]
achados_resolvidos: [QA-H0045-P03-001]
achados_pendentes: []
novos_achados: []
```

## 3. Diagnóstico (causa estrutural)

```yaml
perguntas:
  1_elementos_com_id_como_chave: "cursores, pagina_atual/paginas_atuais, selecoes — todos por console.id"
  2_indexados_por_console_id: sim
  3_duplicatas_tornam_ambiguos: sim (cursor/página/seleção/foco compartilham a mesma chave)
  4_loader_ja_valida_duplicatas: "parcial — só ids de filhos em matriz de grupo; não consoles do corpo"
  5_erro_estrutural_canonico: TelaEstruturaInvalida
  6_ponto_minimo: "carregar_tela, após validar a árvore de elementos, antes do retorno ao modelo/runtime"
  7_abrangencia: "todos os consoles do corpo (incl. aninhados em grupos); não só focalizáveis/lista_foco"
  8_contrato_id_estavel: "contrato_console.md §3 — id estável e único no escopo do tela.json"
  9_rejeicao_sem_schema: sim (apenas validação; sem novo campo JSON)
  10_fallback_id_seguro_apos: sim (_mesmo_console_de_contexto por id permanece determinístico)
causa_estrutural: >
  P03 passou a casar clone paginado e original por console.id. O loader
  aceitava dois consoles com o mesmo id; foco_console=1 materializava
  cursor no primeiro homônimo e cursores/pagina_atual/selecoes
  compartilhavam a chave. A autoridade de unicidade já existia no
  contrato; faltava a rejeição estrutural antes do runtime.
ponto_validacao: tela/loader.py::_validar_unicidade_ids_consoles
autoridade: docs/contratos/contrato_console.md §3 (id único no tela.json)
```

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: QA-H0045-P03-001
    alteracao: >
      Loader percorre recursivamente o corpo e rejeita id de console
      duplicado com TelaEstruturaInvalida (mensagem com caminhos do
      primeiro e do duplicado). Renderer preserva casamento por id
      (P03) documentando a precondição de unicidade; sem fallback
      silencioso para outro console.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P04.md
arquivos_alterados:
  - caminho: tela/loader.py
    delta: >
      _iterar_consoles_do_corpo; _validar_unicidade_ids_consoles;
      chamada em carregar_tela antes do retorno
  - caminho: tela/renderizador.py
    delta: documentação de P04 em _mesmo_console_de_contexto/_console_original_de_contexto
  - caminho: tela/teste_loader.py
    delta: testes de aceitação (ids únicos) e rejeição (duplicados, misto paginado/não, grupo)
  - caminho: tela/teste_renderizador.py
    delta: foco no 2º console + páginas independentes; duplicidade sem render parcial
  - caminho: demo/teste_demo_paginacao.py
    delta: dois consoles com ids únicos — foco, cursor e páginas independentes
arquivos_removidos: []
documentos_normativos_alterados: []
preservacoes:
  - P01/P02/P03 (chips, geometria, cursor, índice global, setas, resize)
  - seleção múltipla; Todos; modo verboso; políticas de quebra; ADR-0037
```

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py
      tela/teste_renderizador.py demo/teste_demo_paginacao.py -v
    resultado_compacto: 376 passed
  - comando_ou_metodo: >
      PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py
      tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py
      tela/teste_selecao.py tela/teste_fluxo_execucao.py
      demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      demo/teste_demo_selecao.py demo/teste_demo.py -v
    resultado_compacto: 556 passed
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: 788 passed
  - comando_ou_metodo: >
      printf '.\n\x1b[B\n,\n' | COLUMNS=80 LINES=24 python demo/demo.py
      h0045_paginacao_console_unico
    resultado_compacto: >
      → item_01 (pág.1/3); . → item_17 (pág.2/3); seta → item_18;
      , → item_01 (pág.1/3); barra/chips [<][>][✥] preservados
validacao_manual:
  nova_rodada: PENDENTE_USUARIO_R04
  status: BLOQUEADA_ATE_QA_DO_P04
```

Verificação local não equivale a QA independente.

## 6. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P03.md
    finalidade: achado bloqueante QA-H0045-P03-001
    leitura_necessaria_para: [cadeia P03/QA]
  - arquivo: docs/contratos/contrato_console.md
    finalidade: autoridade de id único no escopo do tela.json
    leitura_necessaria_para: [diagnóstico §3]
```
