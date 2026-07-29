---
name: REL-CRIACAO-0034-selecao-multipla-e-fluxo-focal-de-processamento
description: "Resultado factual da criação da ADR-0034 (seleção múltipla e fluxo focal de processamento, ITEM-0006)"
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_ADR
  status: ADR_CREATED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: CRIAR_ADR
  objeto: ITEM-0006 — Seleção múltipla no console
  artefato_principal: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  autoridade_principal: null
  decisoes_materializadas:
    - D-SEL-01
    - D-SEL-02
    - D-SEL-03
    - D-SEL-04
    - D-SEL-05
    - D-SEL-06
    - D-SEL-07
    - D-SEL-08
    - D-SEL-09
    - D-SEL-10
    - D-SEL-11
    - D-SEL-12
    - D-SEL-13
    - D-SEL-14
    - D-SEL-15
    - D-SEL-16
    - D-SEL-17
    - D-SEL-18
    - D-SEL-19
    - D-SEL-20
    - D-SEL-21
    - D-SEL-22
    - D-SEL-23
    - D-SEL-24
    - D-SEL-25
    - D-SEL-26
---

# REL-CRIACAO-0034 — Criação documental

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_ADR
artefato_criado: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
status_literal: ADR_CREATED_AWAITING_QA
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - caminho_ou_decisao: docs/templates/TEMPLATE_ADR.md
  - caminho_ou_decisao: docs/adr/INDICE_ADR.md
  - caminho_ou_decisao: docs/backlog.md (ITEM-0006)
  - caminho_ou_decisao: docs/contratos/contrato_console.md
  - caminho_ou_decisao: docs/contratos/contrato_barra_de_menus.md
  - caminho_ou_decisao: docs/contratos/contrato_tela_json.md
  - caminho_ou_decisao: docs/contratos/contrato_composicao_corpo.md
  - caminho_ou_decisao: docs/contratos/contrato_json_console.md
  - caminho_ou_decisao: docs/nomenclatura/01_NUCLEO_COMUM.md
  - caminho_ou_decisao: docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - caminho_ou_decisao: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
  - caminho_ou_decisao: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - caminho_ou_decisao: docs/nomenclatura/32_CONSOLE.md
  - caminho_ou_decisao: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  - caminho_ou_decisao: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
  - caminho_ou_decisao: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - caminho_ou_decisao: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  - caminho_ou_decisao: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  - caminho_ou_decisao: docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
decisoes_materializadas:
  - id: D-SEL-01 a D-SEL-10
    sintese: Estado/identidade da seleção como conjunto de IDs de runtime, invariantes, ordem/reconciliação, teclas Espaço/Enter/Esc, indicadores ec/tg e chip Espaço
  - id: D-SEL-11 a D-SEL-15
    sintese: Fronteira da operação consumidora com o registry genérico (ITEM-0004), protocolo provisório de CLI, resultado estruturado com canais separados, classificação de sucesso/falha e envelope de erro multinível com preservação literal de texto inválido
  - id: D-SEL-16 a D-SEL-20
    sintese: Tela padrão de resultado (perfil resultado_execucao), validação antecipada, fluxo focal de abertura/retorno de uma única origem suspensa, dry-run e execução real reversível com restauração automática
  - id: D-SEL-21 a D-SEL-26
    sintese: Paginação da tela de resultado deferida a 80x24, decomposição em quatro handoffs sequenciais, fixture obrigatória de oito itens do Handoff 1, testes previstos, critérios de aplicação documental futura e deltas de compatibilidade
---
```

Não reproduz a especificação nem o conteúdo do documento criado.

## 3. Delta documental

```yaml
delta_material:
  - Criação da ADR-0034, próximo identificador livre confirmado por leitura do índice e por ausência de arquivo `ADR-0034-*.md` no repositório.
  - ADR organizada em 26 decisões fechadas (D-SEL-01 a D-SEL-26), formalizando seleção múltipla, protocolo focal de execução e tela padrão de resultado para o ITEM-0006, sem escolher alternativas nem introduzir arquitetura, schema ou protocolo definitivo além do fornecido.
  - Relação registrada com ADR-0026, ADR-0027 e ADR-0028 (separação JSON estrutural × conteúdo externo, tela de processamento como composição) e com ADR-0031 (D13/D15, que deferiu explicitamente `[␣]`, indicadores de inclusão e execução por `[⏎]` sobre conjunto marcado para este ciclo).
  - Decomposição do ciclo em quatro handoffs sequenciais (H1 a H4) com critérios próprios de aprovação registrados na ADR.
arquivos_criados:
  - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  - docs/relatorios/RELATORIO_CRIACAO_ADR-0034.md
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo: "git branch --show-current; git rev-parse --short HEAD; git diff --cached --name-only; git status --short --untracked-files=all"
    resultado_compacto: "branch=master, HEAD=721f8f1, stage vazio, worktree limpo — baseline conforme esperado"
  - comando_ou_metodo: "rg -n 'ADR-[0-9]{4}' docs/adr/INDICE_ADR.md | tail -n 12"
    resultado_compacto: "última entrada real ADR-0033 (2026-07-27); ADR-0034 confirmada como próximo identificador"
  - comando_ou_metodo: "printf '%s\\n' docs/adr/ADR-0034-*.md"
    resultado_compacto: "nenhum arquivo encontrado antes da criação — ADR-0034 estava livre"
  - comando_ou_metodo: "printf '%s\\n' docs/adr/ADR-0026-*.md docs/adr/ADR-0027-*.md docs/adr/ADR-0028-*.md docs/adr/ADR-0031-*.md"
    resultado_compacto: "os quatro padrões resolveram exatamente um arquivo cada — leitura fechada realizada sem pendência"
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas:
  - "A ADR usa codificação de decisão D-SEL-01 a D-SEL-26, seguindo o padrão observado na aplicação mais recente do template canônico (ADR-0033), não uma numeração ditada pelo prompt orquestrador."
  - "Os quatro itens bloqueados a criar futuramente (D-SEL-24) não receberam numeração de ADR nem de ITEM nesta execução, conforme exigido."
```

## 6. Evidências separadas

Não aplicável — nenhuma evidência separada foi produzida além deste
relatório e da própria ADR.
