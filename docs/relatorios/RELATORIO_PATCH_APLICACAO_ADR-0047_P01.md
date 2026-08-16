---
name: relatorio-patch-aplicacao-adr-0047-p01
description: Patch P01 da aplicação documental da ADR-0047 — propaga o delta P02
metadata:
  type: relatorio
  scope: orquestrador
  etapa: PATCH_APLICACAO_ADR
  status: ADR_APPLICATION_PATCHED_P01
---

# Relatório — Patch P01 da aplicação da ADR-0047

## Rastreabilidade

- etapa: `PATCH_APLICACAO_ADR`
- objeto: ADR-0047 / aplicação / P01
- cadeia_raiz: `docs/relatorios/RELATORIO_APLICACAO_ADR-0047.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_QA_ADR-0047_POS_P02.md`
- patch_adr_origem: P02

## Proveniência

`git status --short --untracked-files=all` capturado antes da escrita. O
worktree já continha deltas acumulados do ciclo (contratos, índice,
código, config, testes, handoffs). Este relatório atribui a esta execução
somente os arquivos efetivamente escritos abaixo. O diff acumulado contra
HEAD não é prova isolada de causalidade.

## Delta P02 propagado

Para H-0063: `preset` permanece inalterado; `titulo` permanece
integralmente inalterado; `amostra` passa a existir como extensão
compatível da projeção semântica, com a mesma amostra já produzida no
fluxo, nunca por parsing de `titulo`; nenhum campo existente é removido,
renomeado ou redefinido. A configuração estrutural futura instancia
`formato.dois_niveis_por_foco.filho` com tabulação 5..10, designador
`nenhum`, apresentação `tabela`, colunas `preset`/`amostra` e espaçamento
3..8.

## Contratos efetivamente alterados

- `docs/contratos/contrato_tela_json.md` — nova §36.8: especialização
  concreta de H-0063; schema genérico de §36.2–§36.5 não redesenhado;
  `preset` e `amostra` são referências a campos semânticos, não dados
  copiados para a configuração.
- `docs/contratos/contrato_json_console.md` — nova §15.1: extensão da
  projeção de H-0063; `amostra` é dado semântico; `titulo` preservado;
  proibido obter `amostra` por parsing de `titulo`; proveniência no mesmo
  componente que já produz a amostra antes da composição de `titulo`;
  presença de `amostra` não transforma conteúdo em configuração.

## Nomenclatura

`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` alterado de forma
mínima: termos `projeção semântica` e `extensão compatível da projeção
semântica`; distinção extensão da projeção × alteração do conteúdo
visível. Sem regras de tabulação, apresentação tabela, geometria ou
renderer.

## Índice

`docs/adr/INDICE_ADR.md` atualizado factualmente: ADR-0047 permanece
aceita; P02 com QA ADR aprovado; aplicação documental em patch P01,
aguardando QA pós-patch. Nenhum ITEM nem handoff novo. H-0073 não marcado
como aprovado.

## Fronteira

CONFIGURAÇÃO ESTRUTURAL DA TELA = COMO apresentar. CONTEÚDO/PROJEÇÃO =
O QUE apresentar. RENDERER = geometria física. `amostra` é dado
semântico. Colunas `preset`/`amostra` permanecem decisão exclusiva da
configuração estrutural.

## Arquivos efetivamente escritos

- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_console.md`
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`
- `docs/adr/INDICE_ADR.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0047_P01.md`

## Verificações

- Relatório existe.
- Aplicação original `RELATORIO_APLICACAO_ADR-0047.md` não sobrescrita.
- H-0073 não alterado.
- Código, config e testes não alterados por esta execução.
- `git diff --check` executado somente sobre os cinco arquivos acima.

## Bloqueios

nenhum

## delta_terminologico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  termos_adicionados:
    - projeção semântica
    - extensão compatível da projeção semântica
  termos_alterados: []
  distincoes_adicionadas:
    - extensão compatível da projeção semântica × alteração do conteúdo visível
  fronteiras_alteradas: []
```
\n