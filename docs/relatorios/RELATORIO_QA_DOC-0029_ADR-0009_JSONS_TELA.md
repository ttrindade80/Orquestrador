---
name: relatorio-qa-doc-0029-adr-0009-jsons-tela
description: QA documental da ADR-0009 sobre caminho, nomenclatura e formato dos JSONs de tela
metadata:
  type: relatorio_qa
  scope: docs
  status: aprovado_com_ajustes
  data: 2026-07-07
---

# Relatorio QA — DOC-0029 / ADR-0009 / JSONs de tela

## Status final

`APROVADO_COM_AJUSTES`

A ADR-0009 esta tecnicamente coerente com o DOC-0029 e fecha o DOC-B010. A
ressalva e de rastreabilidade do worktree: ha alteracoes documentais
acumuladas de ciclos anteriores fora do pacote estrito do DOC-0029, inclusive
contratos e indices. Essas alteracoes nao foram feitas por esta QA e nao
alteram a aprovacao tecnica da ADR-0009.

## Escopo verificado

Foram verificados:

- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`;
- `docs/adr/INDICE_ADR.md`;
- `docs/build_docs/to_do.md`;
- `docs/contratos/contrato_tela_json.md`;
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`;
- `docs/relatorios/RELATORIO_CONSOLIDACAO_FASE_0_ADR-0008_TELA_BASE.md`;
- estado do worktree e diffs solicitados.

## Evidencias objetivas

Comandos executados:

```bash
git status --short
git diff --check -- docs/adr/ADR-0009-caminho-formato-jsons-tela.md docs/adr/INDICE_ADR.md docs/build_docs/to_do.md
git diff -- docs/adr/INDICE_ADR.md docs/build_docs/to_do.md
```

Resultado:

- `git diff --check` nao reportou problemas.
- `git diff -- docs/adr/INDICE_ADR.md docs/build_docs/to_do.md` mostra inclusao da ADR-0009 no indice e inclusao do DOC-0029/DOC-B010 no `to_do.md`.
- Como `ADR-0009-caminho-formato-jsons-tela.md` esta nao rastreado, seu conteudo foi verificado por leitura direta.
- `git status --short` mostra worktree acumulado com arquivos modificados e nao rastreados do ciclo ADR-0008, alem da ADR-0009.

## Resultado por criterio

| Criterio | Resultado | Evidencia |
|---|---|---|
| ADR-0009 existe | OK | Arquivo lido diretamente em `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`. |
| Caminho canonico definido | OK | Decisao 2 define `config/telas/<id_da_tela>.json`. |
| Um JSON proprio por tela concreta | OK | Decisao 1 declara um arquivo separado por tela. |
| Regra de nome clara | OK | Decisao 3 exige minusculo, sem acentos, sem espacos e preferencialmente `snake_case`. |
| `id` interno coincide com nome base | OK | Decisao 3 exige coincidencia, salvo excecao futura em ADR propria. |
| Tela raiz usa `orquestrador` | OK | Decisao 4 define identificador canonico `orquestrador`. |
| Futuro arquivo raiz definido | OK | Decisao 4 define `config/telas/orquestrador.json`. |
| Arquivo raiz nao deve ser criado agora | OK | Decisao 4 e Fora de escopo indicam criacao futura em DOC-B011. |
| `config/estilo.json` fora de `config/telas/` | OK | Decisao 6 preserva `config/estilo.json` como biblioteca global. |
| Sem `config/dashboard.json` | OK | Consequencias declaram que nao se deve criar `config/dashboard.json`. |
| JSONs transicionais preservados | OK | Decisao 7 marca arquivos existentes como artefatos a reavaliar/migrar, sem apagar agora. |
| Sem indice central obrigatorio | OK | Decisao 5 nao cria nem exige indice central nesta etapa. |
| `contrato_tela_json.md` preservado como contrato de formato | OK | Decisao 8 remete detalhes de campo, tipos, validacao e composicao ao contrato. |
| Consequencias coerentes | OK | Consequencias liberam DOC-B011, preservam termo generico `tela.json` e orientam carregamento por `id`. |
| Fora de escopo correto | OK | Fora de escopo exclui JSON real, loader, validacao automatica, migracao, exclusao de antigos, registries e revisao de contratos. |
| `INDICE_ADR.md` inclui ADR-0009 | OK | Linha `ADR-0009 | caminho, nomenclatura e formato dos JSONs de tela | aceita | 2026-07-07`. |
| `to_do.md` fecha DOC-B010 e cria DOC-0029 | OK | DOC-0029 esta concluido; DOC-B010 esta concluido com resolucao pela ADR-0009. |
| DOC-B011, DOC-B008, DOC-B009 e DOC-0018 preservados | OK | Permanecem listados; DOC-B008/B009/B011 como `bloqueado_decisao`, DOC-0018 como `pronto_para_execucao`. |
| Sem alteracao de contrato, JSON de producao, `NOMENCLATURA.md`, `INDICE.md` ou codigo por DOC-0029 | OK com ressalva | O pacote declarado do DOC-0029 envolve apenas ADR-0009, `INDICE_ADR.md` e `to_do.md`. O worktree, porem, ja contem alteracoes acumuladas em contratos, `NOMENCLATURA.md` e `INDICE.md` de tarefas anteriores. Nenhum arquivo `config/*.json` ou codigo aparece alterado no status. |

## Problemas encontrados

Nenhum problema tecnico bloqueante foi encontrado na ADR-0009.

Ressalva documental: o worktree esta acumulado com alteracoes fora do escopo
estrito do DOC-0029. Isso impede uma confirmacao puramente por `git status` de
que contratos, `NOMENCLATURA.md` e `INDICE.md` estejam limpos no repositorio
como um todo, embora o DOC-0029 declare e evidencie escopo restrito.

## Recomendacoes de ajuste

- Antes do commit final, separar ou consolidar o pacote DOC-0029 para que o
  commit da ADR-0009 contenha apenas:
  - `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`;
  - `docs/adr/INDICE_ADR.md`;
  - `docs/build_docs/to_do.md`;
  - este relatorio de QA.
- Manter DOC-B011 bloqueado ate a decisao operacional de executar o draft real,
  apesar de DOC-B010 estar fechado.

## Confirmacao de nao alteracao fora do escopo desta QA

Esta QA alterou somente este arquivo:

```text
docs/relatorios/RELATORIO_QA_DOC-0029_ADR-0009_JSONS_TELA.md
```

Nao foram alterados por esta QA: contratos, JSONs de producao,
`docs/NOMENCLATURA.md`, `docs/INDICE.md` ou codigo.
