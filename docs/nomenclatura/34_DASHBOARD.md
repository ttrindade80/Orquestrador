---
name: nomenclatura-dashboard
description: Terminologia do dashboard — saída passiva formatada, marcadores, campos de resumo, total e apresentação de dashboard
metadata:
  type: nomenclatura
  scope: dashboard
  fase_de_aplicacao: VIGENTE
---

# Dashboard

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário dos termos de:
- dashboard como tipo de elemento;
- saída passiva;
- marcador (símbolo + rótulo);
- campos de resumo;
- Total;
- apresentação de dashboard.

Instâncias concretas (como a tela raiz do Orquestrador) não são definições
universais e estão no relatório histórico.

## 3. Termos proprietários

- `dashboard` (tipo de elemento)
- saída passiva formatada
- marcador
- campo de resumo
- Total

## 4. Definições

### 4.1 Dashboard como tipo de elemento

`dashboard` é um tipo de elemento do corpo — saída passiva formatada, resumo,
legenda ou visão consolidada dos dados exibidos. Antigo `Info` (ADR-0006).

Propriedades fundamentais:
- não navegável por `[✥]`;
- não obrigatório;
- possui moldura própria;
- aceita posicionamento dentro do corpo conforme configuração da tela;
- sem conteúdo universal fixo.

`dashboard` não terá `config/dashboard.json` próprio. Cada instância é
declarada pelo JSON da tela onde é usada.

### 4.2 Marcador

Par de símbolo e rótulo que representa uma condição ou categoria na
apresentação do dashboard. Marcadores oficiais da instância de referência
(tela raiz do Orquestrador — instância, não definição universal):

| Símbolo | Rótulo |
|---|---|
| `!` | Retido |
| `@` | Incompleto |
| `?` | Ausência |
| `*` | Revisão |
| `&` | Dissonância |
| `%` | Indevido |
| `~` | Atualização |
| `^` | Mesclado |

Este conjunto é da instância raiz conhecida; não define a classe universal.

### 4.3 Campos de resumo e Total

Campos do resumo principal: Adicionados, Fichados, Consolidados, Qualificados,
Orfão, Missing, Secundários, Descartados (8 campos — da instância raiz).

**Formato do valor**: número puro, sem zero à esquerda, alinhado à direita
dentro do campo. Não há padding de dígitos. Nenhum estado de travessão (`—`)
existe — todo campo sempre exibe um número, `0` incluso.

### 4.4 Alinhamento (pendência)

O alinhamento horizontal do dashboard está pendente de confirmação: falta
decidir se acompanha a mudança do `lancador` (bloco à esquerda com sobra à
direita, ADR-0002) ou mantém centralização. Ver relatório de aplicação,
pendências NOM-LEV-015.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `dashboard` × `console` | Dashboard: saída passiva, não navegável por `[✥]`; console: container interativo e navegável |
| `dashboard` × `lancador` | Dashboard: saída passiva; lancador: navegação para outras telas |
| instância de dashboard × definição universal | A instância da tela raiz do Orquestrador é exemplo, não definição da classe |

## 6. Relação com contratos

Não existe contrato próprio de `dashboard` nesta fase; a composição do corpo
que inclui dashboard é coberta por `contrato_composicao_corpo.md`.

## 7. Relação com ADRs

- ADR-0006: renomeação `Info` para `dashboard`.
- ADR-0008: `dashboard` não terá `config/dashboard.json` próprio.
- ADR-0010: `dashboard` como elemento funcional do corpo.
- ADR-0019: múltiplos `dashboard` por tela (remove restrição de zero ou um).

## 8. Aliases ou termos descontinuados relacionados

- `Info` → descontinuado; substituído por `dashboard` (ADR-0006). Ver módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- Instância concreta da tela raiz do Orquestrador → relatório histórico.
- Composição do corpo que inclui dashboard → módulo `20` e `contrato_composicao_corpo.md`.
- Pendências de alinhamento → classificadas no relatório de aplicação.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§9 (linhas 987-1045)"
  intervalo_ou_bloco: "NOM-LEV-015"
origem_normativa: ADR-0006, ADR-0008, ADR-0010, ADR-0019
contratos_relacionados:
  - contrato_composicao_corpo.md
adrs_relacionadas:
  - ADR-0006
  - ADR-0008
  - ADR-0010
  - ADR-0019
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
  - CLASSIFICADO_COMO_HISTORICO
partes_NAO_CONFIRMADAS:
  - "Alinhamento do dashboard: falta decidir se acompanha lancador ou mantém centralização — PENDENCIA"
```
