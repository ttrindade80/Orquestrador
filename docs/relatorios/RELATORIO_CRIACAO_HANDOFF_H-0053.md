---
name: REL-CRIACAO-0053-arvore-colapsavel
description: "Resultado factual da criação do handoff H-0053 (ativação de arvore_colapsavel sobre a fundação de H-0052)"
metadata:
  type: relatorio_criacao_documental
  tipo_execucao: CRIAR_HANDOFF
  status: HANDOFF_CREATED
  data: "2026-08-08"
rastreabilidade:
  etapa: CRIAR_HANDOFF
  objeto: H-0053
  artefato_principal: docs/handoff/H-0053-arvore-colapsavel.md
  autoridade_principal: docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  decisoes_materializadas:
    - D-MULTI-05
    - D-MULTI-01
    - D-MULTI-02
    - D-MULTI-10
    - D-MULTI-11
    - D-MULTI-12
    - D-MULTI-13
---

# REL-CRIACAO-0053 — Criação documental do handoff H-0053

## 1. Identificação e status

```yaml
tipo_execucao: CRIAR_HANDOFF
artefato_criado: docs/handoff/H-0053-arvore-colapsavel.md
status_literal: HANDOFF_CREATED
```

## 2. Autoridades e decisões materializadas

```yaml
autoridades_materiais:
  - docs/adr/ADR-0042-navegacao-multinivel-do-console.md (D-MULTI-05 principal; D-MULTI-01/02/10/11/12/13 transversais)
  - docs/contratos/contrato_console.md (§7, §19-§21, §22.11-§22.18, §24)
  - docs/contratos/contrato_json_console.md (§7.1, §11-§12)
  - docs/nomenclatura/32_CONSOLE.md (§4.10)
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
  - docs/backlog.md (ITEM-0007)
  - docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md (predecessor técnico, leitura focal por rg)
decisoes_materializadas:
  - id: D-MULTI-05
    sintese: arvore_colapsavel é árvore navegável sem seleção; ↑/↓ percorrem a sequência visível; Espaço abre/fecha ramo; ramo fechado permanece corrente
  - id: D-MULTI-13
    sintese: reutiliza o resolver tipo_navegacao_efetivo de H-0052 sem coação para nivel_unico
  - id: D-MULTI-10
    sintese: paginação integralmente subordinada à ADR-0041, sem regra concorrente
```

Não reproduz a especificação nem o conteúdo do handoff criado.

## 3. Delta documental

```yaml
delta_material:
  - "Handoff H-0053 fecha o ponto de intervenção exato deixado por H-0052: substitui o stub de console_e_focalizavel que hoje retorna sempre False para arvore_colapsavel (tela/navegacao.py linhas 85-87) por ativação real"
  - "Identifica a hierarquia real vigente como ConteudoExterno/NoConteudo (tela/modelo.py, ADR-0026/0027) — não a lista plana de itens do console — fechando a questão de representação sem inventar schema"
  - "Fecha o armazenamento do estado de expansão/recolhimento como nova chave (ramos_fechados) no mesmo dicionário de runtime que já hospeda cursores/selecoes, com justificativa explícita de por que não há alternativa arquitetural material em aberto"
  - "Identifica os pontos de renderer (tela/renderizacao/console.py e conteudo_externo.py) que precisam passar a conhecer estado de runtime pela primeira vez, hoje puramente declarativos"
  - "Fecha lista nominal de arquivos alteráveis, preservados e fixtures, com fixture de referência estrutural (h0036_console_hierarquia + h0036_hierarquia_conteudo) já lida integralmente"
arquivos_criados:
  - docs/handoff/H-0053-arvore-colapsavel.md
  - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0053.md
arquivos_alterados: []
```

## 4. Verificações executadas

```yaml
verificacoes:
  - comando_ou_metodo: "git branch --show-current && git rev-parse HEAD && git status --short --untracked-files=all && git diff --cached --name-only"
    resultado_compacto: "branch=master; HEAD=0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d; stage vazio; worktree limpo — baseline conforme"
  - comando_ou_metodo: "test ! -e docs/handoff/H-0053-arvore-colapsavel.md; test ! -e docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0053.md"
    resultado_compacto: "ambos ausentes antes da criação — confirmado"
  - comando_ou_metodo: "leitura integral das 9 autoridades do manifesto (ADR-0042, ADR-0041, contrato_console.md, contrato_json_console.md, 32_CONSOLE.md, 44_APRESENTACOES..., backlog.md, TEMPLATE_HANDOFF_IMPLEMENTACAO.md, TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md)"
    resultado_compacto: "concluída antes de qualquer escrita"
  - comando_ou_metodo: "rg focal sobre H-0052 (tipo_navegacao_efetivo|console_e_focalizavel|Escopo futuro nominal|...)"
    resultado_compacto: "localizado o stub em tela/navegacao.py console_e_focalizavel (linhas 85-87) que H-0053 substitui"
  - comando_ou_metodo: "rg/leitura focal em tela/navegacao.py, tela/modelo.py, tela/renderizacao/conteudo_externo.py, tela/renderizacao/console.py, demo/demo.py"
    resultado_compacto: "confirmada a separação entre itens (lista plana) e ConteudoExterno/NoConteudo (hierarquia real); confirmado o catálogo cenário→conteúdo em demo/demo.py e o bloco de dispatch de teclado (~linhas 695-844)"
  - comando_ou_metodo: "leitura de config/telas/demo/h0036_console_hierarquia.json e h0036_hierarquia_conteudo.json"
    resultado_compacto: "fixture de referência estrutural confirmada e citada no handoff"
```

## 5. Bloqueios e ressalvas

```yaml
bloqueios: []
ressalvas:
  - "A questão de armazenamento do estado de expansão/recolhimento foi avaliada quanto ao critério de BLOCKED_USER_DECISION do prompt de origem e considerada NÃO bloqueante: o padrão já vigente de estado em tela/navegacao.py (cursores/selecoes no mesmo dicionário de runtime) e a ausência de campo de schema para estado inicial por nó resolvem objetivamente a escolha, sem abrir duas alternativas materialmente equivalentes de ownership. A justificativa completa está no handoff (§8.5)."
```

## 6. Evidências separadas

Não aplicável.
