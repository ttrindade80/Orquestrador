---
name: relatorio-patch-aplicacao-adr-0047-p02
description: Patch P02 da aplicação documental da ADR-0047 — propaga o delta P03
metadata:
  type: relatorio
  scope: orquestrador
  etapa: PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_PATCHED_P02
---

# Relatório — Patch P02 da aplicação da ADR-0047

## Rastreabilidade

```yaml
etapa: PATCH_APLICACAO_ADR
objeto: ADR-0047 / aplicação / P02
patch_adr_origem: P03
cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0047.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0047_POS_P03.md
```

## Proveniência

`git status --short --untracked-files=all` capturado antes da escrita. O
worktree já continha deltas acumulados do ciclo. Este relatório atribui a
esta execução somente os arquivos efetivamente escritos abaixo. O
`RELATORIO_PATCH_APLICACAO_ADR-0047_P01.md` não foi sobrescrito.

## Delta P03 propagado

O bloco `formato.dois_niveis_por_foco.filho.designador` passa à forma
canônica com `tipo` obrigatório e `prefixo`/`sufixo` opcionais, ambos
strings. Tipos válidos: `decimal_composto`, `alfabetico_maiusculo`,
`nenhum`. Ausência de prefixo/sufixo equivale a string vazia para tipos
visuais. Para `tipo: nenhum`, prefixo e sufixo devem estar ausentes.
Chaves desconhecidas são inválidas. Não há herança automática, campo
`fonte`, campo `herdar` nem parsing do documento de conteúdo.

## Contratos

- `docs/contratos/contrato_tela_json.md` — atualizado. Schema de §36.2 e
  regras de §36.4 materializam `tipo`, `prefixo` e `sufixo`. Nova §36.9
  especializa H-0055 com `tipo: alfabetico_maiusculo`, `sufixo: ")"`,
  tabulação 5..10 e `apresentacao: texto`, produzindo `A)`, `B)`, `C)`,
  `D)` — não equivalente a `A`/`B`/`C`/`D` sem sufixo. §36.8 de H-0063
  permanece com `tipo: nenhum`, sem prefixo nem sufixo; `preset`,
  `amostra`, `titulo`, tabela, tabulação 5..10 e espaçamento 3..8
  preservados. Demais campos de `filho` não redesenhados.
- `docs/contratos/contrato_console.md` — alterado somente em §25.3: para
  tipos visuais, `designador_visual = prefixo + designador_base + sufixo`;
  para `nenhum`, nenhum designador é emitido. Tabulação, tabela, colunas,
  alinhamento, quebra, resize, navegação e seleção não foram alterados.
- `docs/contratos/contrato_json_console.md` — não alterado. P03 não
  modifica o documento de conteúdo.

## Nomenclatura

`docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`
preservado. `prefixo` e `sufixo` são campos do schema estrutural já
coberto pelo termo canônico de designador local; não há delta
terminológico.

## Especializações

- H-0055: `A)` com sufixo estrutural `")"`. Conteúdo externo inalterado.
- H-0063: `tipo: nenhum` sem prefixo/sufixo; especialização P01
  (`preset`/`amostra`) preservada integralmente.

## Índice

`docs/adr/INDICE_ADR.md` atualizado factualmente: ADR-0047 aceita; P03
aprovado (`ADR_APPROVED_WITH_NOTES`); aplicação documental em P02,
aguardando QA pós-patch. Nenhum ITEM. H-0072 e H-0073 não marcados como
concluídos.

## Arquivos efetivamente escritos

- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_console.md`
- `docs/adr/INDICE_ADR.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0047_P02.md`

## Verificações

- Relatório existe.
- `contrato_json_console.md` não alterado por esta execução.
- H-0072 e H-0073 não alterados.
- Config, código e testes não alterados por esta execução.
- `git diff --check` executado somente sobre os quatro arquivos acima.

## Bloqueios

nenhum

## delta_terminologico

```yaml
delta_terminologico:
  modulos_alterados: []
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
```
\n