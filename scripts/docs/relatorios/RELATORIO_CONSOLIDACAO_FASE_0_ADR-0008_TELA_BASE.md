---
name: relatorio-consolidacao-fase-0-adr-0008-tela-base
description: Consolidacao documental curta da Fase 0 apos aplicacao da ADR-0008 aos contratos centrais da tela base
metadata:
  type: relatorio_consolidacao
  scope: docs
  status: concluido
  data: 2026-07-07
---

# Relatorio de Consolidacao — Fase 0 / ADR-0008 / Tela Base

## 1. Escopo

Este relatorio consolida o ciclo documental ligado a:

- ADR-0008;
- `contrato_tela_json.md`;
- aplicacao em `NOMENCLATURA.md`;
- `contrato_composicao_corpo.md`;
- `contrato_lancador.md`;
- `contrato_barra_de_menus.md`;
- `contrato_chip.md`;
- `contrato_console.md`;
- ajuste pos-QA do `contrato_console.md`.

Nao cria JSON real, nao altera contratos, nao altera ADRs e nao altera codigo.

## 2. Estado documental fechado

Itens fechados no `to_do.md` e seus artefatos principais:

| Item | Estado | Artefato principal |
|---|---|---|
| DOC-0016 — ADR-0008 | concluido | `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` |
| DOC-0023 — contrato `tela_json` | concluido | `docs/contratos/contrato_tela_json.md` |
| DOC-0017 — aplicacao em `NOMENCLATURA.md` | concluido | `docs/NOMENCLATURA.md` |
| DOC-0025 — contrato de composicao do corpo | concluido | `docs/contratos/contrato_composicao_corpo.md` |
| DOC-0020 — contrato do `lancador` | concluido | `docs/contratos/contrato_lancador.md` |
| DOC-0021 — contrato da `barra_de_menus` | concluido | `docs/contratos/contrato_barra_de_menus.md` |
| DOC-0026 — contrato `chip` | concluido | `docs/contratos/contrato_chip.md` |
| DOC-0024 — contrato `console` | concluido | `docs/contratos/contrato_console.md` |
| DOC-0027 — ajuste pos-QA do `console` | concluido | `docs/contratos/contrato_console.md` |

## 3. Status das QAs

| Relatorio | Status | Natureza da ressalva |
|---|---|---|
| `RELATORIO_QA_DOC-0016_DOC-0023_TELA_JSON.md` | APROVADO_COM_AJUSTES | Problema tecnico documental menor: DOC-0023 omitira DOC-B011 na frase de proxima acao. |
| `RELATORIO_QA_DOC-0016_DOC-0023_TELA_JSON_POS_AJUSTE.md` | APROVADO | Ajuste aplicado; pendencias derivadas citadas ate DOC-B011. |
| `RELATORIO_QA_DOC-0017_NOMENCLATURA_ADR-0008.md` | APROVADO | Sem ressalva tecnica bloqueante. |
| `RELATORIO_QA_DOC-0020_CONTRATO_LANCADOR_ADR-0008.md` | APROVADO | Sem ressalva tecnica bloqueante. |
| `RELATORIO_QA_DOC-0021_CONTRATO_BARRA_DE_MENUS_ADR-0008.md` | APROVADO_COM_AJUSTES | Ressalva de worktree acumulado; conteudo normativo aprovado. |
| `RELATORIO_QA_DOC-0025_CONTRATO_COMPOSICAO_ADR-0008.md` | APROVADO_COM_AJUSTES | Ressalva de worktree acumulado; conteudo normativo aprovado. |
| `RELATORIO_QA_DOC-0026_CONTRATO_CHIP.md` | APROVADO | Sem ressalva tecnica bloqueante. |
| `RELATORIO_QA_DOC-0024_CONTRATO_CONSOLE.md` | APROVADO_COM_AJUSTES | Problema tecnico real P1: criterios de validacao nao espelhavam todos os campos minimos da instancia. |
| `RELATORIO_QA_DOC-0027_CONTRATO_CONSOLE_POS_AJUSTE.md` | APROVADO | P1 tecnico do `contrato_console.md` resolvido em DOC-0027. |

As ressalvas de `barra_de_menus` e `composicao_corpo` sao de escopo Git/worktree,
nao de contradicao tecnica com a ADR-0008. A ressalva tecnica do `console` foi
resolvida pelo DOC-0027 e aprovada no relatorio pos-ajuste.

## 4. Modelo consolidado

```text
tela.json declara a tela concreta
estilo.json fornece biblioteca global de aparencia
corpo contem elementos declarados: console, lancador, dashboard
barra_de_menus e instancia declarada na tela
chip e entidade declarativa usada pela barra
console e container generico de itens heterogeneos
lancador e elemento de corpo acionado diretamente por seus itens
dashboard e elemento passivo, nao navegavel
```

Tambem fica consolidado:

- renderer valida e executa declaracao;
- renderer nao hardcoda composicao;
- JSON de tela nao guarda estado de runtime;
- acoes sao registradas/whitelisted;
- comandos arbitrarios no JSON sao proibidos.

## 5. Pendencias preservadas

Pendencias abertas preservadas com o status atual do `to_do.md`:

| Item | Status atual | Observacao |
|---|---|---|
| DOC-B008 — Definir contratos/classes de itens internos de `console` | bloqueado_decisao | Necessario para fechar taxonomia e campos dos itens internos. |
| DOC-B009 — Definir registry de tipos validos | bloqueado_decisao | Necessario para registry de tipos, acoes, filtros, origens e validacoes. |
| DOC-B010 — Definir formato real e caminho dos JSONs de tela | bloqueado_decisao | Necessario antes de criar draft real de JSON de tela. |
| DOC-B011 — Criar draft do JSON da tela raiz do Orquestrador | bloqueado_decisao | Deve aguardar DOC-B010 e revisao das instancias relevantes. |
| DOC-0018 — Aplicar ADR-0008 nos contratos afetados | pronto_para_execucao | Remanescem `contrato_cabecalho.md` e `contrato_estilo.md`. |

Tambem permanecem fora deste fechamento, sem alteracao de status neste
relatorio, DOC-B007 e DOC-B001 a DOC-B004.

## 6. Analise de bloqueio para o proximo passo

`contrato_cabecalho.md` nao contradiz materialmente a ADR-0008 para o draft
conceitual da tela raiz. O contrato ainda nao foi revisado formalmente pelo
DOC-0018, mas ja separa textos concretos de `titulo` e `descricao` como dados
da classe/tela e reserva `config/cabecalho.json` para parametros de
apresentacao. A revisao remanescente deve ajustar o enquadramento para
`tela.json`, mas nao bloqueia o desenho conceitual.

`contrato_estilo.md` nao contradiz materialmente a ADR-0008 para o draft
conceitual da tela raiz. Ele define estilo como schema universal e independente
de tela, coerente com `config/estilo.json` como biblioteca global de aparencia.
A revisao remanescente deve explicitar a restricao da ADR-0008 e limpar leituras
transicionais, mas nao bloqueia o desenho conceitual.

Pendencias abertas que afetam o proximo passo:

- DOC-B010 bloqueia o draft real em arquivo, porque ainda falta decidir caminho,
  nomenclatura e organizacao dos JSONs de tela.
- DOC-B011 permanece bloqueado no `to_do.md` porque depende de DOC-B010.
- DOC-B008 e DOC-B009 podem afetar implementacao e validacao futura, mas nao
  impedem um draft conceitual orientado por contrato.
- DOC-0018 remanescente para `cabecalho` e `estilo` nao bloqueia o draft
  conceitual, desde que a pendencia seja preservada explicitamente.

Classificacao do proximo passo:

```text
LIBERADO_COM_PENDENCIAS_NAO_BLOQUEANTES
```

## 7. Recomendacao de proximo passo

Recomenda-se tratar DOC-B010 antes do draft real: definir formato, caminho,
nomenclatura e organizacao dos JSONs de tela. Em seguida, abrir o DOC para o
draft do JSON da tela raiz do Orquestrador.

## 8. Observacao sobre worktree

O worktree esta acumulado com multiplos artefatos documentais modificados e
nao rastreados, incluindo indices, nomenclatura, ADR, contratos e relatorios
do ciclo ADR-0008. Esse acumulo explica as ressalvas de escopo em algumas QAs.

Isso nao deve ser tratado como problema tecnico do modelo documental.
