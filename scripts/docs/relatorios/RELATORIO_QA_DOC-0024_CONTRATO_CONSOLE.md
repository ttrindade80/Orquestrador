---
name: relatorio-qa-doc-0024-contrato-console
description: QA documental do DOC-0024, contrato do console como container generico
metadata:
  type: relatorio_qa
  scope: docs
  doc: DOC-0024
  status: APROVADO_COM_AJUSTES
  criado_em: 2026-07-07
---

# Relatório QA — DOC-0024 — Contrato `console`

## Status final

`APROVADO_COM_AJUSTES`

O contrato `docs/contratos/contrato_console.md` está coerente com o modelo
documental vigente e cobre o objetivo do DOC-0024. O ajuste recomendado é
documental: expandir os critérios de validação para espelhar explicitamente
todos os campos mínimos da instância definidos na seção 3.

## Escopo verificado

Foram lidos e usados como base:

- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_console.md`
- `docs/INDICE.md`

Também foram executados os comandos solicitados:

```bash
git status --short
git diff --check -- docs/contratos/contrato_console.md docs/INDICE.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_console.md docs/INDICE.md docs/build_docs/to_do.md
```

## Evidências objetivas

- `contrato_console.md` existe e possui frontmatter compatível com contratos
  existentes: `type: contrato`, `scope: scripts`, `versao`, `status: ativo`,
  `rastreabilidade`, `adrs_aplicadas` e `reaproveitado_de_legado`
  (`docs/contratos/contrato_console.md`, linhas 1-20).
- O contrato define `console` como elemento de corpo interativo e navegável,
  declarado no `tela.json`, e como container genérico de itens heterogêneos
  (linhas 38-49).
- O contrato separa `console` de tela, `lancador`, `dashboard` e
  `barra_de_menus` (linhas 50-57).
- A instância concreta vem do `tela.json`, e o renderer executa a declaração
  validada sem decidir composição, itens, filtros, paginação, colunas, ações
  ou navegação (linhas 58-66; 394-422).
- A estrutura mínima da instância cobre `id`, `tipo = console`, título ou
  identificador visual, origem/binding, itens/regra de geração, e políticas
  de composição, navegação, seleção, paginação e exibição (linhas 70-100).
- Itens internos heterogêneos foram formalizados, com `id`, `tipo`,
  `binding`, `renderizador`, `navegavel`, `selecionavel`, `acao_enter`,
  `politica_quebra` e `politica_exibicao` (linhas 104-136).
- A navegação é por item, não por linha física; item pode ocupar uma ou mais
  linhas; item não navegável sai do ciclo; item não selecionável não participa
  de `[␣]`; itens diferentes podem ter ações diferentes; item sem ação válida
  torna `[⏎]` inativo (linhas 138-150; 210-230; 264-280).
- O contrato preserva contratos próprios futuros para tipos internos de item
  via pendência DOC-B008 (linhas 149-150; 463-465).
- A política de composição cobre modo normal compacto, truncamento com
  reticências e expansão em modo verboso; o exemplo foi marcado como
  conceitual e não obrigatório (linhas 154-181).
- `[V]` alterna modo verboso quando permitido, e modo verboso é estado de
  exibição reutilizável (linhas 185-206).
- `[✥]` fica restrito a `console` navegável e explicitamente não navega
  `lancador` nem `dashboard` (linhas 212-230; 450-451).
- As políticas de seleção `nenhuma`, `unica` e `multipla` foram definidas;
  `[␣]` só existe para seleção múltipla; seleção única usa cursor; seleção é
  estado de runtime, não JSON (linhas 234-260).
- `[⏎]` depende do item em foco e de ação registrada/whitelisted; comando
  arbitrário é proibido (linhas 264-280; 424-426).
- Filtros são declarativos, atuam sobre dados vinculados ao `console` e são
  aplicados antes da paginação (linhas 284-302; 407-409).
- Paginação é consequência do conteúdo renderizado que não cabe; página atual
  é estado de runtime; políticas de quebra foram previstas (linhas 306-329).
- Colunas ajustáveis foram tratadas como política declarada; `[-][+]` só
  existe quando a instância permite; ajuste de coluna é runtime (linhas
  333-348).
- A relação com `chip`/`barra_de_menus` está coerente: `console` não desenha a
  barra, expõe capacidades/estado, a barra reflete capacidades declaradas e
  chips continuam entidades da barra (linhas 352-371).
- A relação com `dashboard` e `lancador` está coerente (linhas 375-388).
- Pendências fora de escopo foram registradas sem tentar resolver
  implementação, JSON real, testes ou renderização final (linhas 459-483).
- `docs/INDICE.md` inclui `contrato_console.md` na ordem de leitura e na
  estrutura esperada (linhas 36-40; 62-71).
- `docs/build_docs/to_do.md` marcou DOC-0024 como `concluido`, com descrição
  compatível com o contrato e preservação de pendências derivadas (linhas
  288-295).
- DOC-B008, DOC-B009, DOC-B010 e DOC-B011 permanecem registrados e não foram
  fechados indevidamente (linhas 329-347).
- `git diff --check` não reportou problemas nos arquivos verificados.

## Problemas encontrados

### P1 — Critérios de validação não espelham todos os campos mínimos

A seção 3 define como mínimos `tipo = console`, `titulo ou identificador
visual`, `politica_composicao`, `politica_navegacao`, `politica_selecao`,
`politica_paginacao` e `politica_exibicao` (linhas 74-84). A seção 16 valida
alguns casos essenciais, mas não explicita erro para ausência de todos esses
campos mínimos (linhas 430-455).

Impacto: baixo. As regras normativas existem no contrato, mas a checklist de
validação fica menos completa do que o próprio schema mínimo declarado.

## Recomendações de ajuste

- Em tarefa posterior, acrescentar à seção 16 critérios explícitos para:
  `tipo` diferente de `console`, ausência de identificador visual quando não
  houver `titulo`, ausência de `politica_composicao`, `politica_navegacao`,
  `politica_selecao`, `politica_paginacao` e `politica_exibicao`.
- Não é necessário alterar JSON real, ADR, código ou implementação para este
  ajuste; trata-se apenas de refinamento contratual.

## Confirmação de não alteração fora do escopo

Nesta tarefa de QA, nenhum JSON, ADR, código ou contrato preexistente foi
alterado. O único arquivo criado por esta tarefa foi este relatório:

`docs/relatorios/RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md`

O `git status --short` executado antes da criação deste relatório já indicava
mudanças documentais preexistentes no workspace, incluindo alterações em
`docs/INDICE.md`, `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
`docs/build_docs/to_do.md`, contratos existentes, e arquivos novos do ciclo
ADR-0008/DOC-0023/DOC-0024/DOC-0026. Essas mudanças foram apenas verificadas
por esta QA, não editadas.
