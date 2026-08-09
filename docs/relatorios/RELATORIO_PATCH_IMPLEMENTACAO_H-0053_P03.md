---
name: RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03
description: "Materialização da ADR-0043 na demonstração H-0053"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-08-09
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0053
  patch: P03
  autoridades:
    - ADR-0042
    - ADR-0043
    - H-0053 P02 aprovado

---

# Relatório — Patch de implementação H-0053 P03

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status: IMPLEMENTATION_PATCHED
objeto: H-0053
patch: P03
autoridades:
  - ADR-0042
  - ADR-0043
  - H-0053 P02 aprovado
```

## Delta

```yaml
delta:
  ajuda: "Fixture declara [?] Ajuda como último chip, sempre presente e ativa."
  chip_contextual: >-
    Chip declarativo de Espaço é projetado a partir do item corrente da
    árvore: Recolher para ramo aberto, Expandir para ramo fechado e Expandir
    inativo para folha. A atualização ocorre no mesmo redesenho do cursor ou
    da expansão/recolhimento, sem semântica de seleção.
  cursor: >-
    A derivação usa exclusivamente a projeção visível e retorna ausência para
    cursor inexistente; a invariável de árvore focalizada com item corrente
    válido permanece preservada.
  fixture: >-
    Hierarquia externa atualizada para 1., 1.1, 1.2, 1.2.1, 2. e 2.1,
    mantendo a relação pai/filho do modelo e removendo a). A associação
    continua no catálogo do ponto de entrada.
  multiline: >-
    Conteúdos demonstrativos foram alongados em alguns nós e a apresentação
    verbosa existente da fixture produz quebras físicas reais.

arquivos_alterados:
  - demo/demo.py
  - tela/navegacao.py
  - tela/teste_navegacao.py
  - demo/teste_demo_console.py
  - config/telas/demo/h0053_arvore_colapsavel.json
  - config/telas/demo/h0053_arvore_colapsavel_conteudo.json
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0053_P03.md
```

O estado de expansão/recolhimento permanece exclusivamente em runtime. A
projeção da barra usa a declaração existente de chip e cópia efêmera do modelo;
nenhum schema, registry, action ID ou estado de fixture foi criado.

## Verificações

```yaml
testes_focais:
  comando: "pytest -q tela/teste_navegacao.py; pytest -q demo/teste_demo_console.py"
  resultado: "59 passed; 9 passed"
suite_integral:
  comando: "pytest -q"
  resultado: "1071 passed"
git_diff_check:
  resultado: OK

paginacao_dedicada:
  estado: FORA_DE_ESCOPO
validacao_manual:
  estado: PENDENTE_USUARIO
```

Não foram alteradas a política de paginação, a solução de mapa físico/
renderer ou o redraw aprovado no P02. A suíte preservou regressões de
navegação, seleção, paginação e consoles fora do escopo.

## Estado Git

```yaml
stage: vazio
commit: false
branch: master
HEAD: 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d
```

Próxima etapa: `QA_POS_PATCH_IMPLEMENTACAO`.
