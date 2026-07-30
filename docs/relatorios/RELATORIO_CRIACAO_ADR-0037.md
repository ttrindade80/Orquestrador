---
name: REL-CRIACAO-0037-integracao-fluxo-focal-dry-run-restauracao-origem
description: "Resultado factual da criação da ADR-0037 (especialização do Handoff 4 da ADR-0034)"
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_ADR
  status: ADR_CREATED
  data: 2026-07-29
rastreabilidade:
  etapa: CRIAR_ADR
  objeto: ADR-0037
  artefato_principal: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  autoridade_principal: null
  decisoes_materializadas:
    - D-H4-01
    - D-H4-02
    - D-H4-03
    - D-H4-04
    - D-H4-05
    - D-H4-06
    - D-H4-07
    - D-H4-08
    - D-H4-09
    - D-H4-10
---

# REL-CRIACAO-0037 — Criação documental

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_ADR
artefato_criado: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
status_literal: ADR_CREATED
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - caminho_ou_decisao: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md (D-SEL-18 a D-SEL-21)
  - caminho_ou_decisao: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  - caminho_ou_decisao: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md (D-H3-19)
decisoes_materializadas:
  - id: D-H4-01
    sintese: tela de origem específica do Handoff 4, reutilizando a semântica da fixture de oito itens do H-0041 sem alterar a tela histórica; nome físico deferido ao handoff
  - id: D-H4-02
    sintese: toggle focal [Ins] Dry-Run como chip de alternância de estado vivo da instância, iniciando em execução real
  - id: D-H4-03
    sintese: cor_alerta (amarelo) aplicada ao chip em dry-run, concretizando o campo no estilo global e absorvendo a parte pendente do ITEM-0011
  - id: D-H4-04
    sintese: fronteira pontual com o ITEM-0020; supersessão pontual de D-SEL-19, de contrato_barra_de_menus.md e dos fora de escopo de dry-run/cor_alerta da ADR-0036
  - id: D-H4-05
    sintese: ativação condicional do chip Executar sobre lote reconciliado não vazio, executor disponível e tela de resultado pré-validada
  - id: D-H4-06
    sintese: transição atômica entre acionamento e apresentação do resultado, sem tela vazia nem estado intermediário
  - id: D-H4-07
    sintese: origem suspensa como referência de runtime (não snapshot), sem entrada nem mutação enquanto o resultado está aberto
  - id: D-H4-08
    sintese: retorno de dry-run sem recarregar dados, preservando seleção/filtro/página/foco/cursor/toggle
  - id: D-H4-09
    sintese: retorno de execução real com seleção sempre limpa, dados recarregados, filtro reaplicado e foco/cursor reconciliados
  - id: D-H4-10
    sintese: limpeza por propriedade entre H-0042, H-0043 e o próprio Handoff 4
```

## 3. Delta documental

```yaml
delta_material:
  - Novo documento ADR-0037, especialização do Handoff 4 do ITEM-0006, ainda não registrada no índice nem aplicada.
  - Supersessão pontual declarada (não aplicada) sobre D-SEL-19 (ADR-0034), sobre a fronteira de contrato_barra_de_menus.md §23.3 e sobre os itens de fora de escopo de dry-run/cor_alerta da ADR-0036.
  - Absorção declarada da parcela pendente de cor_alerta do ITEM-0011, condicionada a implementação e validação futuras.
arquivos_criados:
  - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  - docs/relatorios/RELATORIO_CRIACAO_ADR-0037.md
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo: "git branch --show-current && git rev-parse HEAD && git diff --cached --name-only && git status --short"
    resultado_compacto: "branch master; HEAD 8af243c336ca5eb3bdc7ae888009ab404c883ab6; stage vazio; worktree limpo — baseline conforme"
  - comando_ou_metodo: "leitura de docs/adr/INDICE_ADR.md"
    resultado_compacto: "ADR-0037 confirmado como próximo identificador livre (última entrada: ADR-0036)"
  - comando_ou_metodo: "leitura integral do manifesto fechado (templates, INDICE_ADR, backlog, ADR-0034/0035/0036, H-0041/0042/0043, contratos e módulos de nomenclatura listados)"
    resultado_compacto: "concluída antes da escrita da ADR"
  - comando_ou_metodo: "leitura focal de tela/loader.py, tela/renderizador.py, tela/execucao_focal.py, tela/resultado_execucao.py, config/telas/demo/h0041_selecao_multipla_oito_itens.json, demo/demo.py"
    resultado_compacto: "confirmado: EstiloResolvido possui cor_inativo mas não cor_alerta; paleta ANSI do renderer já mapeia \"amarelo\"; interfaces públicas de execucao_focal.py e resultado_execucao.py identificadas; fixture h0041 íntegra"
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas: []
```

## 6. Evidências separadas

Não aplicável — nenhuma evidência externa ao próprio artefato criado.
