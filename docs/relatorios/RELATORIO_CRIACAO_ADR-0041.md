# Relatório de criação — ADR-0041

**Data:** 2026-08-07
**Etapa:** CRIAR_ADR
**Papel:** autor documental

## ADR criada

`docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`, status
`proposta`. Documento registra apenas as decisões fechadas fornecidas;
nenhuma alternativa foi escolhida, nenhuma implementação, aplicação de
contrato/nomenclatura, handoff ou validação foi executada.

## Decisões materializadas

D-PGU-01 a D-PGU-08, transcritas integralmente na seção 3 da ADR:

- D-PGU-01/02: teclas físicas exclusivas `PageUp` (página anterior) e
  `PageDown` (próxima página).
- D-PGU-03: representação canônica `[PgUp][PgDn] Páginas` na barra de menus.
- D-PGU-04: extinção de qualquer função de paginação para `<`, `>`, `,` e
  `.` — sem status de alias, atalho ou fallback.
- D-PGU-05: universalidade — aplica-se a toda paginação comum do
  Orquestrador, presente ou futura, não restrita a consoles multinível.
- D-PGU-06: preservação integral das demais regras de paginação limitada já
  vigentes pela ADR-0038 (topologia sem wrap, controles inativos nas bordas,
  página como estado de runtime, reposicionamento na troca explícita, setas
  internas não mudam de página, indicador `página X/Y`, repaginação e
  reconciliação).
- D-PGU-07: a especialização é restrita a tecla e representação visual; as
  demais D-PAG-01 a D-PAG-13 não são reabertas.
- D-PGU-08: a futura navegação multinível deve consumir esta autoridade
  universal, sem definir comandos próprios de paginação.

A ADR também contém: contexto e problema (seção 2), decisão consolidada
(seção 4), consequências e tabela de artefatos potencialmente afetados
(seção 5), compatibilidade e transição (seção 6), alternativas consideradas
— nenhuma (seção 7), itens fora de escopo (seção 8), critérios para
aplicação não marcados (seção 9), relação explícita com a ADR-0038 (seção
10) e bloqueios — nenhum (seção 11).

## Autoridades usadas

Leitura integral: `docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md`,
`docs/nomenclatura/01_NUCLEO_COMUM.md`,
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`,
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.

Leitura focal (ocorrências de paginação, `[<][>]`, `<`, `>`, `,`, `.`):
`docs/contratos/contrato_console.md` (§12, §24), `docs/contratos/contrato_barra_de_menus.md`
(§8.3, §24), `docs/contratos/contrato_chip.md` (§7, §8, §9).

Não foram lidos: relatórios, código, testes, ADR-0041/H-0051 de branch
descartada, nem implementação da tentativa multinível descartada.

## Arquivos criados

- `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`
- `docs/relatorios/RELATORIO_CRIACAO_ADR-0041.md` (este relatório)

## Verificações

- `git status --short` confirma que, entre os artefatos desta execução,
  somente os dois arquivos acima foram criados; nenhum arquivo existente foi
  alterado por esta etapa.
- Pré-existência não relacionada a esta execução, já presente no diretório
  de trabalho antes desta tarefa e não tocada por ela: `docs/backlog.md`
  (modificado) e `docs/relatorios/RELATORIO_ATUALIZACAO_BACKLOG_MULTINIVEL_2026-08-07.md`
  (não rastreado).
- `git diff --check` executado sobre a árvore de trabalho: sem problemas de
  espaço em branco a reportar.
- Nenhum `git add` e nenhum `git commit` foram executados.

## Bloqueios

nenhum
