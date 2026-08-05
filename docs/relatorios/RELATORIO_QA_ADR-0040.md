# Relatório QA — ADR-0040

## Objeto auditado

`docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md`

## Autoridades

Foram consideradas as decisões fechadas D-DRY-01 a D-DRY-08, a ADR-0037 como
autoridade do fluxo focal e a ADR-0034 quanto à seleção, lote reconciliado e
fronteiras do ITEM-0006. Também foram verificados o template canônico, o índice,
o backlog, os quatro contratos enumerados e os módulos de nomenclatura `01`,
`02`, `31` e `32` do manifesto fechado.

## Verificações materiais

A ADR representa substancialmente D-DRY-01 a D-DRY-08: categoria e posição do
chip, rótulo dinâmico, operação nos dois estados, estado inicial sem default,
modo único por instância, compatibilidade integral, destaque por `cor_alerta`,
ciclo de vida, captura e transmissão explícita do modo. Também preserva o
`[Ins] Dry-Run` focal da ADR-0037, mantém o ITEM-0020 aberto e veda migração
implícita, sem alterar seleção, lote, foco, paginação ou modos de visualização.

## Achados

1. **Material — decisão de schema transferida indevidamente.** A seção D-DRY-03
   declara que nenhum nome de campo foi fechado, mas também afirma que sua
   nomeação será decisão da futura aplicação documental (linhas 125–135). O
   critério de aplicação torna isso obrigatório (linhas 372–374). Aplicação
   documental deve propagar decisão, não decidir campo novo; isso contradiz a
   proibição de inventar schema e transfere uma escolha material para etapa
   posterior.

2. **Material — escopo futuro não fechado apresentado como obrigação.** A
   seção de compatibilidade determina que a futura migração deverá preservar
   comportamento e alterar somente uma lista específica de aspectos (linhas
   321–331). As autoridades exigem reconciliação futura própria e proíbem
   migração implícita, mas não fecham esse escopo normativo detalhado.

3. **Conformidade formal — template.** A seção 7 não usa a tabela de
   alternativas prevista pelo `TEMPLATE_ADR.md`; registra a ausência de
   alternativas apenas em prosa.

## Status

`ADR_REJECTED`

## Próxima ação

`PATCH_ADR`: remover a decisão transferida à aplicação documental, retirar ou
reformular a obrigação normativa sobre a futura migração e alinhar a seção 7
ao template, preservando D-DRY-01 a D-DRY-08.
