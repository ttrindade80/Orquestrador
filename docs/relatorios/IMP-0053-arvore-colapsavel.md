---
name: IMP-0053-arvore-colapsavel
description: "Implementação factual da política de navegação arvore_colapsavel"
metadata:
  type: relatorio_implementacao
  tipo_execucao: IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-0053
  data: 2026-08-08
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas: [ADR-0042, ADR-0041, ADR-0026, ADR-0027, ADR-0028]
  issues_relacionadas: [ITEM-0007]
  bugs_abertos: []
  autorizacoes_operacionais: [H-0053, P01]
  cadeia_raiz: H-0053
  predecessor_imediato: H-0052
  achados_tratados: [H-0053-A, H-0053-B, H-0053-C, H-0053-D]
---

# IMP-0053 — Relatório de implementação

## 1. Identificação e status

```yaml
handoff: H-0053 — Ativar navegação arvore_colapsavel sobre o console
tipo_execucao: IMPLEMENTACAO
status_literal: IMPLEMENTED
status_normalizado: IMPLEMENTED
```

## 2. Delta material

`arvore_colapsavel` foi ativada sobre a representação canônica
`ConteudoExterno/NoConteudo`. Consoles com conteúdo hierárquico navegável são
focalizáveis; a sequência é pré-ordem visível, com `↑/↓` restritos à projeção
vigente. `Espaço` alterna somente ramos com filhos; folhas não alteram estado,
seleção ou ação. `←/→`, `Enter`, `Todos` e seleção permanecem sem nova
semântica.

O estado transitório `ramos_fechados[console]` usa conjuntos de IDs no mesmo
estado de runtime de foco/cursor, não é persistido e não cria campo de schema.
O renderer deriva as linhas da mesma projeção, oculta descendentes fechados e
marca o nó corrente com o símbolo de foco. A paginação existente continua
autoritativa; setas não trocam página.

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: config/telas/demo/h0053_arvore_colapsavel.json
    finalidade: fixture estrutural com política declarada
  - caminho: config/telas/demo/h0053_arvore_colapsavel_conteudo.json
    finalidade: fixture externa hierárquica demonstrativa
  - caminho: docs/relatorios/IMP-0053-arvore-colapsavel.md
    finalidade: relatório desta implementação
arquivos_alterados:
  - caminho: tela/navegacao.py
    delta: foco, projeção, movimento, alternância e chip da árvore
  - caminho: tela/renderizacao/conteudo_externo.py
    delta: ocultação de ramos e indicador corrente
  - caminho: tela/renderizacao/console.py
    delta: composição da árvore, estado runtime e mapa paginável
  - caminho: demo/demo.py
    delta: runtime, dispatch de Espaço, catálogo e preparação de renderização
  - caminho: tela/teste_navegacao.py
    delta: testes focais H-0053 e regressões
  - caminho: demo/teste_demo_console.py
    delta: smoke da fixture e alternância demonstrativa
```

## 4. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q"
    resultado_compacto: "57 passed"
    prova_semantica: "ativação, percurso, fechamento, reabertura, folha, chip e página"
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console.py -q"
    resultado_compacto: "7 passed"
    prova_semantica: "catálogo, fixture H-0053, render sem placeholder e alternância"
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q"
    resultado_compacto: "128 passed"
    prova_semantica: "paginação vigente preservada"
  - comando_ou_metodo: "PYTHONDONTWRITEBYTECODE=1 python -m pytest"
    resultado_compacto: "1067 passed in 29.58s"
    prova_semantica: "suíte integral verde"
  - comando_ou_metodo: git diff --check
    resultado_compacto: "sem erros"
    prova_semantica: "diff da implementação sem whitespace inválido"
```

## 5. Demonstração operacional

```yaml
cwd: "."
comando: |
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao \
    --tela config/telas/demo/h0053_arvore_colapsavel.json
entrada_ou_fixture: config/telas/demo/h0053_arvore_colapsavel.json
configuracao: "catálogo interno demo/demo.py associa o documento externo"
saida_observada: "código 0; árvore aberta, cursor no primeiro nó e [✥] Navegar"
comparacao_com_esperado: "fixture correta, conteúdo esperado e sem placeholder"
prova_semantica: "smoke não-TTY concluído; interação TTY não simulada"
codigo_de_saida: 0
```

## 6. Estado Git observado

```yaml
branch: master
HEAD: 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d
staged: []
unstaged: "seis arquivos de código/teste alterados e três artefatos H-0053 novos"
nao_rastreados: "artefatos documentais preexistentes do ciclo e relatório H-0053"
divergencias_materiais: []
```

## 7. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas: []
observacoes_para_qa:
  - "validar em TTY real o percurso, Espaço, indicador e página corrente"
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada: false
  resultado: PENDENTE
  itens_pendentes: [validacao TTY real]
```
