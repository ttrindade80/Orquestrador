---
name: REL-DOC-DOC-0006-BARRA-DE-MENUS
description: Auditoria documental do item DOC-0006 — criação do contrato da barra_de_menus
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-05
rastreabilidade:
  auditoria: "DOC-0006"
  contratos_alvo:
    - docs/contratos/contrato_barra_de_menus.md
  adr_relacionadas:
    - docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
  bugs_abertos: []
---

# REL-DOC — Auditoria DOC-0006 — contrato_barra_de_menus

## Revisão executada

Auditoria documental do item DOC-0006: criação de
`docs/contratos/contrato_barra_de_menus.md` e atualização de
`docs/INDICE.md` e `docs/build_docs/to_do.md`.

## Status final

`APROVADO`

## Arquivos esperados alterados

| Arquivo | Status |
|---|---|
| `docs/contratos/contrato_barra_de_menus.md` | Criado |
| `docs/INDICE.md` | Atualizado |
| `docs/build_docs/to_do.md` | Atualizado |

## Achados bloqueantes

Nenhum.

## Evidências verificadas

### E-001 — Dependências de `cor_inativo` e `cor_alerta` satisfeitas

Verificação:

- `docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md` existe.
- `docs/adr/INDICE_ADR.md` lista ADR-0004 como aceita.
- `docs/contratos/contrato_estilo.md` contém a seção 3.5 "Estados dinâmicos de cor".
- `contrato_estilo.md` declara `cor_inativo` e `cor_alerta` como campos obrigatórios do schema.
- `contrato_barra_de_menus.md` referencia `cor_inativo` e `cor_alerta` apontando para o schema de estilo ativo — sem hardcoding de cor.

Resultado: OK.

### E-002 — DOC-0006 registrado em `to_do.md` como concluído

Verificação:

- `docs/build_docs/to_do.md` contém entrada `DOC-0006 — Criar contrato da barra_de_menus`.
- Campo `Status: concluido`.
- Campo `Concluido_em: 2026-07-05`.
- Arquivo envolvido `contrato_barra_de_menus.md` listado.

Resultado: OK.

### E-003 — `INDICE.md` aponta para o novo contrato

Verificação:

- `docs/INDICE.md` lista `contrato_barra_de_menus.md` na ordem de leitura (contratos ativos).
- `docs/INDICE.md` lista `contrato_barra_de_menus.md` na estrutura esperada de `contratos/`.
- `docs/INDICE.md` lista `barra_de_menus.json` na estrutura esperada de `config/`.

Resultado: OK.

### E-004 — Distinção `barra_de_menus` vs objeto `menu` do corpo declarada explicitamente

Verificação:

- Seção 2 do contrato apresenta tabela comparativa direta.
- O contrato declara que `barra_de_menus` não herda regras de layout do objeto `menu` do corpo.
- O contrato declara arquivos de dados separados: `config/barra_de_menus.json` vs `config/layout_menu.json`.
- R-4 das regras de uso reforça a separação terminológica.
- Critério de validação confirma que o renderer da `barra_de_menus` não consulta `config/layout_menu.json`.

Resultado: OK.

### E-005 — Valores concretos não duplicados no contrato

Verificação:

- O contrato não reproduz tabelas de símbolos, rótulos nem mapeamentos concretos de `config/barra_de_menus.json`.
- A seção 4 aponta explicitamente `config/barra_de_menus.json` como única fonte de valores concretos.
- As tabelas do contrato declaram semântica e regras — não valores.

Resultado: OK.

### E-006 — Escopo restrito: nenhum arquivo proibido alterado

Verificação via `git status`:

- `contrato_estilo.md` — não alterado nesta execução.
- `contrato_composicao_corpo.md` — não alterado nesta execução.
- `NOMENCLATURA.md` — não alterado nesta execução.
- `config/barra_de_menus.json` — não alterado.
- Nenhum ADR criado ou alterado.
- Nenhum RFC criado ou alterado.
- Nenhum arquivo de código alterado.

Resultado: OK.

## Verificações sem achados

- `contrato_barra_de_menus.md` declara `status: ativo` no frontmatter.
- O contrato cobre todos os tópicos exigidos pelo escopo da tarefa: escopo da `barra_de_menus`, distinção com `menu`, fonte de valores concretos, relação com `contrato_estilo.md`, `cor_inativo` e `cor_alerta`, existência estrutural vs estado dinâmico, ordem canônica, comportamento contextual de `[Esc]`, rótulo dinâmico de `[⏎]`, chips específicos e critérios de validação.
- A ordem canônica registrada no contrato é consistente com `docs/NOMENCLATURA.md` seção 5.1.
- O comportamento de `[Esc]` (Limpar / Sair / Voltar) está consistente com `docs/NOMENCLATURA.md` seção 5.1.2.
- Os três rótulos de `[⏎]` (Todos / Executar / Visualizar) estão consistentes com `docs/NOMENCLATURA.md` seção 5.1.2.
- As pendências herdadas (`config/barra_de_menus.json` `_meta.pendencias`) estão registradas na seção 13 do contrato.

## Observação não bloqueante

Em QA futuro, vale conferir se `filtro_de_grupo` e `formacao_de_selecao` serão
nomes formais de eixo no schema da classe de tela ou apenas chaves internas de
`config/barra_de_menus.json`. Essa decisão não existe ainda em `NOMENCLATURA.md`
como eixo declarado formalmente — mas não bloqueia DOC-0006, pois os chips que
dependem desses eixos são condicionais e a semântica está corretamente descrita
no contrato e no JSON.

## Verificação de escopo

| Item | Resultado |
|---|---|
| Relatório QA formal criado | OK |
| `contrato_barra_de_menus.md` criado e `status: ativo` | OK |
| `INDICE.md` atualizado | OK |
| `to_do.md` atualizado com DOC-0006 concluído | OK |
| Contratos existentes preservados sem alteração | OK |
| ADRs preservadas sem alteração | OK |
| `NOMENCLATURA.md` preservado sem alteração | OK |
| Configs preservados sem alteração | OK |
| Nenhum código alterado | OK |

## Conclusão

A auditoria DOC-0006 foi registrada com status `APROVADO`. Zero achados
bloqueantes. Zero achados remanescentes. Uma observação não bloqueante registrada
para QA futuro sobre a formalização dos nomes de eixo `filtro_de_grupo` e
`formacao_de_selecao`.

## Errata posterior

Após a verificação acumulada DOC-0001 a DOC-0006, a observação não bloqueante
sobre `filtro_de_grupo` e `formacao_de_selecao` ficou obsoleta. Esses eixos
foram formalizados posteriormente em `docs/NOMENCLATURA.md`,
`docs/contratos/contrato_composicao_corpo.md` e `config/barra_de_menus.json`.

O relatório original permanece como evidência histórica do estado de DOC-0006 no
momento da emissão; apenas essa observação específica foi superada por ajustes
documentais posteriores.
