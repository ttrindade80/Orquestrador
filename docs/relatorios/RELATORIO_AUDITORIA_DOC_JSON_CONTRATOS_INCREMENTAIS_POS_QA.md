# Relatório de Auditoria — DOC JSON Contratos Incrementais Pós-QA

## Status final

QA_APPROVED_WITH_NOTES

## Escopo auditado

Auditoria pós-QA da correção aplicada ao bloqueio anterior em
`docs/contratos/contrato_json_tela_minima.md`.

Objetivo verificado:

- confirmar que `corpo.arranjo` deixou de ser obrigatório no JSON mínimo;
- confirmar que `corpo.elementos[]` permanece obrigatório;
- confirmar que `arranjo` continua permitido como campo opcional;
- confirmar que ausência de `arranjo` remete ao `tiling` do estilo ativo;
- confirmar que a redação não autoriza fallback inventado pelo renderer nem
  decisão de arranjo por largura de terminal;
- confirmar ausência de nova contradição com os contratos ativos auditados.

Esta auditoria não corrigiu contratos, ADRs, JSONs, `NOMENCLATURA.md` nem
código. O único arquivo criado por esta etapa é este relatório.

## Arquivos lidos

- `docs/relatorios/RELATORIO_AUDITORIA_DOC_JSON_CONTRATOS_INCREMENTAIS.md`
- `docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS_POS_QA.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_estilo.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

## Comandos executados

```bash
git status --short
git diff --stat
git diff --name-only
git diff -- docs/contratos/contrato_json_tela_minima.md
git status --short -- tela
git status --short -- config
git status --short -- docs/adr
git status --short -- docs/NOMENCLATURA.md docs/contratos/contrato_json_tela_minima.md docs/relatorios/RELATORIO_AUDITORIA_DOC_JSON_CONTRATOS_INCREMENTAIS_POS_QA.md
find tela config docs/adr -type f -print
```

## Escopo Git

`git status --short` no início da auditoria mostrou:

```text
 M docs/INDICE.md
?? docs/contratos/contrato_json_barra_de_menus.md
?? docs/contratos/contrato_json_cabecalho.md
?? docs/contratos/contrato_json_console.md
?? docs/contratos/contrato_json_dashboard.md
?? docs/contratos/contrato_json_lancador.md
?? docs/contratos/contrato_json_tela_minima.md
?? docs/handoff/H-0010-lancador-visual-inerte.md
?? docs/relatorios/RELATORIO_AUDITORIA_DOC_JSON_CONTRATOS_INCREMENTAIS.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0010_HANDOFF.md
?? docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS.md
?? docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS_POS_QA.md
```

`git diff --stat` mostrou apenas:

```text
scripts/docs/INDICE.md | 5 ++++-
1 file changed, 4 insertions(+), 1 deletion(-)
```

`git diff --name-only` mostrou apenas:

```text
scripts/docs/INDICE.md
```

`git diff -- docs/contratos/contrato_json_tela_minima.md` não produziu saída,
porque `contrato_json_tela_minima.md` ainda está não rastreado (`??`), e
`git diff` não exibe conteúdo de arquivo untracked por padrão.

Checagens específicas de escopo proibido:

- `git status --short -- tela` não mostrou alterações.
- `git status --short -- config` não mostrou alterações.
- `git status --short -- docs/adr` não mostrou alterações.
- `docs/NOMENCLATURA.md` não aparece alterado.
- `docs/contratos/contrato_json_tela_minima.md` aparece como arquivo não
  rastreado.

Nota de escopo: o worktree contém arquivos não rastreados e `docs/INDICE.md`
modificado que pertencem ao pacote documental anterior ou a artefatos paralelos
já visíveis na auditoria anterior. Para a correção pós-QA propriamente dita, o
relatório de implementação declara alteração exclusiva em
`docs/contratos/contrato_json_tela_minima.md`. Esta auditoria não identificou
alterações em `tela/`, `config/`, ADRs ou `docs/NOMENCLATURA.md`.

## Verificação do bloqueio anterior

Bloqueio anterior:

```text
contrato_json_tela_minima.md tornava corpo.arranjo obrigatório, contradizendo
a regra ativa que permite arranjo não declarado e uso de tiling do estilo como
default.
```

Resultado pós-QA: corrigido.

Evidências em `docs/contratos/contrato_json_tela_minima.md`:

- Seção 4, JSON mínimo: `corpo` contém apenas `elementos: []`; não contém
  `arranjo`.
- Seção 4, observações: declara que `corpo.arranjo` não aparece no envelope
  mínimo, é campo permitido mas opcional, e quando ausente o renderer usa
  `tiling` do estilo ativo conforme `contrato_composicao_corpo.md` seção 5.6.
- Seção 4, observações: proíbe explicitamente que o renderer invente arranjo,
  crie fallback próprio ou decida composição por largura de terminal.
- Seção 4.1: apresenta exemplo separado com `arranjo` explícito opcional,
  deixando claro que essa declaração fixa o layout para aquela tela.
- Seção 5, campos obrigatórios: mantém `schema`, `id`, `cabecalho`, `corpo`,
  `corpo.elementos`, `barra_de_menus` e `barra_de_menus.chips`; não lista
  `corpo.arranjo` como obrigatório.
- Seção 5.1: declara `corpo.arranjo` como permitido e não obrigatório no
  envelope mínimo.

Conferência com contratos superiores:

- `contrato_composicao_corpo.md` seção 4.2 admite `arranjo` como
  `sobreposto`, `lado_a_lado` ou não declarado.
- `contrato_composicao_corpo.md` seção 5.6 define duas camadas de decisão:
  fixação explícita em `tela.json` ou default pelo `tiling` do estilo ativo.
- `contrato_estilo.md` seção 3.4 define `tiling` como preferência manual do
  usuário, não calculada pela largura do terminal.
- `contrato_estilo.md` R-8 proíbe sobrescrever `tiling` com base em largura de
  terminal ou condição de ambiente.

Conclusão: o achado bloqueante anterior foi removido sem introduzir nova regra
de fallback do renderer.

## Verificação de regressão

Não foram identificadas regressões bloqueantes.

Verificações realizadas:

- `schema` permanece obrigatório e fixado em `"tela.v1"` na versão atual.
- `id` permanece obrigatório, estável, validável e coincidente com o nome base
  do arquivo em disco.
- `cabecalho` permanece obrigatório.
- `corpo` permanece obrigatório.
- `corpo.elementos[]` permanece obrigatório, tipado como array e com itens
  exigindo ao menos `id` e `tipo`.
- `barra_de_menus` permanece obrigatória.
- `barra_de_menus.chips[]` permanece obrigatória.
- Tipos válidos em `corpo.elementos[]` continuam fechados em `console`,
  `dashboard` e `lancador`.
- Regras de `lancador` não foram relativizadas pelo contrato mínimo; seguem
  remetidas aos contratos próprios.
- `dashboard` não foi universalizado: continua opcional, sem conteúdo universal
  fixo, com posição própria via `posicao_dashboard`.
- `console` não teve tipo interno universal fechado; permanece container
  genérico com detalhes internos pendentes/contratuais próprios.
- A redação pós-QA não cria hardcoding de composição, itens, tipos, fallback,
  largura de terminal ou conteúdo.

Verificação de aderência a `contrato_composicao_corpo.md`:

- A correção respeita as duas camadas de decisão: `arranjo` explícito no JSON
  da tela ou `tiling` do estilo ativo quando `arranjo` está ausente.
- A correção não transforma `estilo.json` em fonte de composição concreta; ele
  fornece apenas default de arranjo quando a tela não fixa `arranjo`.
- `dashboard` continua com eixo próprio de posição (`posicao_dashboard`), não
  decidido por `arranjo` nem por `tiling`.

## Achados bloqueantes

Nenhum.

## Achados não bloqueantes

1. O estado Git ainda contém escopo documental mais amplo que a correção
   pós-QA isolada: `docs/INDICE.md` modificado e diversos arquivos não
   rastreados do pacote anterior ou de artefatos paralelos. Não há alteração
   detectada em `tela/`, `config/`, ADRs ou `docs/NOMENCLATURA.md`; por isso,
   este achado é tratado como nota de rastreabilidade, não como bloqueio da
   correção do contrato mínimo.

2. Permanece não corrigida a observação não bloqueante da auditoria anterior
   sobre `contrato_json_barra_de_menus.md`: o exemplo/descrição de `acao` como
   string é menos preciso que a preferência dos contratos superiores por ação
   declarativa registrada/whitelisted. O relatório de implementação pós-QA
   justificou que esse achado não foi tratado porque o escopo da correção era
   apenas o bloqueio em `contrato_json_tela_minima.md`.

## Observações

- A correção preserva a autoridade de `contrato_composicao_corpo.md` e
  `contrato_estilo.md` sobre `arranjo`/`tiling`.
- A ausência de saída no comando
  `git diff -- docs/contratos/contrato_json_tela_minima.md` não indica ausência
  de conteúdo no arquivo; indica que o arquivo está não rastreado.
- A numeração do contrato mínimo contém `## 8. Critérios de aceite documental`
  após `## 9. Fora de escopo`. Essa inconsistência editorial não afeta a
  correção auditada.

## Conclusão

O bloqueio anterior foi corrigido: `corpo.arranjo` não é mais obrigatório no
JSON mínimo, `corpo.elementos[]` permanece obrigatório, `arranjo` aparece como
campo opcional/permitido e a ausência de `arranjo` remete corretamente ao
`tiling` do estilo ativo. A redação não autoriza o renderer a inventar fallback
nem a decidir arranjo por largura de terminal.

O pacote pós-QA está aprovado com notas de rastreabilidade sobre o estado Git
mais amplo e sobre a observação não bloqueante remanescente em
`contrato_json_barra_de_menus.md`.
