---
name: nomenclatura-carregamento-e-associacao-de-conteudo
description: Terminologia do carregamento e associação de conteúdo externo ao console — loader, associação, momento de carga, vínculo, instância carregada, carregamento conjunto
metadata:
  type: nomenclatura
  scope: carregamento_associacao_conteudo
  fase_de_aplicacao: VIGENTE
---

# Carregamento e associação de conteúdo

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário de:
- loader como produtor de conteúdo para o console;
- associação do envelope de dados ao console;
- momento de carga;
- vínculo (relação entre envelope e instância de console);
- instância carregada;
- carregamento conjunto (ADR-0027).

Não confundir com o dado externo em si (o que é o envelope — módulo `42`),
nem com a apresentação (como o dado é exibido — módulo `44`).

## 3. Termos proprietários

- loader (como produtor de conteúdo)
- carregamento
- associação de conteúdo
- momento de carga
- vínculo (envelope × instância de console)
- instância carregada
- carregamento conjunto
- conteúdo associado
- origem de dados declarada
- vinculação declarativa

## 4. Definições

### 4.1 Loader como produtor (ADR-0027)

`loader` é o componente produtor de conteúdo que fornece o envelope de dados
externos ao console. A definição terminológica de `loader` como conceito
transversal está no módulo `01` (núcleo comum).

Neste módulo, `loader` aparece no contexto específico de:
- quem produz o envelope de dados externos;
- como esse envelope é entregue ao console;
- em que momento essa entrega ocorre.

### 4.2 Carregamento e associação

**Carregamento** é o processo pelo qual o envelope de dados externos (módulo `42`)
é vinculado a uma instância de console.

| Termo | Definição |
|---|---|
| `carregamento` | Processo de vincular um envelope de dados externos a uma instância de console |
| `associação de conteúdo` | Relação estabelecida entre envelope e instância de console após o carregamento |
| `momento de carga` | Instante declarativo em que o carregamento ocorre — pode ser na construção da tela, na navegação para a tela, ou sob demanda |
| `vínculo` | Relação formal entre envelope e instância de console que persiste durante a sessão de uso |
| `instância carregada` | Console cujo conteúdo já foi associado a um envelope de dados externos |
| `conteúdo associado` | O envelope de dados externos após ser vinculado à instância de console |

### 4.3 Carregamento conjunto (ADR-0027)

**Carregamento conjunto** é a capacidade de associar múltiplos envelopes de
dados externos a um único console ou associar dados de múltiplos consoles no
mesmo carregamento.

Termo canônico: `carregamento conjunto`. Não é `carregamento simultâneo` nem
`carregamento múltiplo`.

### 4.4 Origem de dados declarada

`origem de dados declarada` é o campo do JSON do console que aponta o produtor
(loader) responsável pelo envelope. Não é o dado em si nem a instância do console.

A **vinculação declarativa** é o ato de declarar essa origem no JSON, antes de
o carregamento ocorrer em runtime.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `carregamento` × `dado externo` | Dado externo (módulo 42): o envelope e seu conteúdo; carregamento: o processo de vincular esse envelope ao console |
| `loader` (transversal) × `loader` (produtor de dados externos) | Loader transversal (módulo 01): conceito geral; loader como produtor de dados externos: uso específico no contexto do carregamento de conteúdo externo (este módulo) |
| `momento de carga` × `momento de apresentação` | Carga: quando o envelope é vinculado; apresentação: como o conteúdo vinculado é exibido — são temporalidades distintas |
| `carregamento conjunto` × `apresentações multinível` | Carregamento conjunto (ADR-0027): associação de múltiplos envelopes; apresentações multinível (ADR-0028): como esses dados são exibidos nos modos verboso/não verboso — módulo `44` |
| `vínculo` × `composição do corpo` | Vínculo: relação entre envelope e instância de console; composição do corpo: estrutura de grupos e elementos na tela (módulo `20`, `40`) |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo do console
  que recebe o carregamento.
- `contrato_json_console.md`: schema dos campos de carregamento no JSON do console.

## 7. Relação com ADRs

- ADR-0027: carregamento conjunto; vinculação declarativa; momento de carga.
- ADR-0026: dado externo que é carregado (parcial — o dado em si está no módulo 42).

## 8. Aliases ou termos descontinuados relacionados

Nenhum neste módulo.

## 9. Conteúdo que não pertence a este módulo

- O envelope de dados em si (schema semântico, campos, níveis) → módulo `42`.
- Apresentação e modos de exibição do conteúdo carregado → módulo `44`.
- `loader` como conceito transversal (definição geral) → módulo `01`.
- Regras comportamentais completas do carregamento → `contrato_console.md` e
  `contrato_json_console.md`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§18 (linhas 1618-1718)"
  intervalo_ou_bloco: "NOM-LEV-026"
origem_normativa: ADR-0027
contratos_relacionados:
  - contrato_console.md
  - contrato_json_console.md
adrs_relacionadas:
  - ADR-0026
  - ADR-0027
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
