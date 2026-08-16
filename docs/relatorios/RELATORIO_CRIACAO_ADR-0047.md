---
name: relatorio-criacao-adr-0047
description: Relatório factual da criação da ADR-0047 (formatação dos filhos de dois_niveis_por_foco)
metadata:
  type: relatorio
  etapa: CRIAR_ADR
  adr: ADR-0047
---

# Relatório — Criação da ADR-0047

## Etapa

`CRIAR_ADR`

## Artefato principal

`docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`

## Status da ADR

`proposta` (conforme frontmatter `metadata.status` do artefato).

## Decisões materializadas

D-DNF-01 a D-DNF-11, transportadas integralmente do prompt fechado ao autor
documental, sem escolha, reabertura ou alteração de alternativa por este
documento.

## Síntese factual do objeto

A ADR-0047 fecha a evolução exclusiva da apresentação/formatação dos filhos
da política canônica `dois_niveis_por_foco` (já fechada pela ADR-0042):
tabulação declarativa mínima/máxima entre pai e filhos, deslocamento da
unidade inteira do filho (`ec`, `tg`, designador e conteúdo movidos juntos,
a partir de antes de `ec`), designadores restritos aos tipos já existentes
no schema semântico multinível, apresentação tabular local de filhos sem
cabeçalho/borda/título próprios, alinhamento global de colunas entre todos
os filhos do console independentemente do pai corrente, espaçamento
declarativo mínimo/máximo entre colunas, quebra de conteúdo em múltiplas
linhas físicas preservando o item lógico, comportamento em resize, e
especialização declarativa da tela de Estilo (`h0063`) sem qualquer
alteração de conteúdo, presets, símbolos, candidato, baseline, aplicação ou
persistência. A navegação, a seleção exclusiva obrigatória de filho por pai
e o schema semântico multinível vigente permanecem preservados sem
redesenho.

## Arquivos criados nesta etapa

- `docs/relatorios/RELATORIO_CRIACAO_ADR-0047.md`

Nenhum outro arquivo foi criado por esta continuação. A ADR-0047 já existia
materialmente no início desta execução, produzida por execução anterior da
mesma etapa `CRIAR_ADR`.

## Arquivos alterados

Nenhum. Esta continuação não alterou `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
nem qualquer outro arquivo do repositório.

## Verificações executadas

- Confirmação de branch, HEAD, stage e worktree via Git antes de qualquer
  escrita.
- Leitura integral de `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
  para extrair os fatos deste relatório.
- Confirmação de que `docs/relatorios/RELATORIO_CRIACAO_ADR-0047.md` não
  existia antes desta execução.
- Após a escrita: confirmação material da existência dos dois artefatos e
  execução de `git diff --check` restrito a ambos.
- Confirmação de que nenhum arquivo além deste relatório foi criado ou
  alterado por esta continuação.

## Baseline Git efetivamente observada

- branch: `master`
- HEAD: `8668ea3f79340a434f46780b0ad0533a0084290b`
- stage: vazio
- worktree: apenas `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
  como arquivo não rastreado, preexistente ao início desta continuação.

## Bloqueios e ressalvas reais

Nenhum bloqueio. Ressalva já registrada na própria ADR-0047 (§5, §7, §8):
a nomenclatura literal de campo JSON para tabulação min/max, estrutura de
colunas e espaçamento min/max entre colunas não foi fixada por esta ADR —
fica deferida à aplicação documental futura que reconciliar
`contrato_console.md` e `contrato_json_console.md`.

## Próxima ação objetiva

`QA_ADR`
\n