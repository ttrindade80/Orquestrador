---
name: nomenclatura-dados-externos-multinivel
description: Terminologia dos dados externos multinível — envelope declarativo, nível, entrada, lista canônica, schema semântico, domínio declarado
metadata:
  type: nomenclatura
  scope: dados_externos_multinivel
  fase_de_aplicacao: VIGENTE
---

# Dados externos multinível

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
- dados externos fornecidos ao console (envelope declarativo e schema);
- nível como camada da hierarquia de dados;
- entrada como unidade básica de dado;
- lista canônica de níveis;
- schema semântico multinível;
- domínio declarado;
- fronteira entre o que é dado (módulo 42) e o que é carregamento (módulo 43).

Não confundir com carregamento (como esse dado é associado ao console — módulo `43`),
nem com apresentação (como esse dado é exibido — módulo `44`).

**Referência permitida a `02`**: este módulo usa o termo `JSON estrutural da tela`
exclusivamente para delimitar a fronteira entre o JSON estrutural e o `JSON externo
de conteúdo`. A definição, a identidade do artefato e a propriedade desse termo
pertencem ao módulo `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`. Esta referência é
classificada como `REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA`; este módulo não
assume co-propriedade nem redefine o artefato.

## 3. Termos proprietários

- dado externo
- envelope declarativo
- nível (camada hierárquica do dado)
- entrada (unidade básica do dado)
- lista canônica de níveis
- nível raiz (nível 1)
- schema semântico
- domínio declarado
- campo semântico
- tipo semântico
- dado multinível
- hierarquia de dados
- dado homogêneo por nível
- dado heterogêneo entre níveis

## 4. Definições

### 4.1 Dado externo e envelope declarativo (ADR-0026)

`dado externo` é qualquer conjunto de dados fornecido ao console de fora do
contrato de composição do corpo, via envelope declarativo.

O **envelope declarativo** é a estrutura JSON que encapsula os dados
externos antes de serem associados ao console. É distinto do schema da tela
e do contrato do console.

### 4.2 Nível

`nível` é cada camada da hierarquia de dados externos. O sistema suporta
hierarquias de múltiplos níveis. A lista de níveis e seus nomes é a
**lista canônica de níveis** declarada no envelope.

| Termo | Definição |
|---|---|
| `nível raiz` | O primeiro nível da hierarquia — nível 1 |
| `lista canônica de níveis` | Conjunto ordenado de todos os níveis declarados no envelope; determina profundidade e nomenclatura |

### 4.3 Entrada

`entrada` é a unidade básica do dado externo. Cada entrada pertence a um nível
específico e pode ter filhos (entradas de nível inferior).

### 4.4 Schema semântico multinível (ADR-0026)

O schema semântico descreve o significado dos campos de dado para cada nível.
Cada nível pode ter campos semânticos distintos.

| Termo | Definição |
|---|---|
| `schema semântico` | Descrição dos campos de dado de um nível específico — quais campos existem e o que significam |
| `campo semântico` | Campo nomeado no schema de um nível |
| `tipo semântico` | Classificação do campo (texto, número, referência, etc.) |
| `domínio declarado` | Conjunto de campos declarados como pertencentes ao domínio do envelope |
| `dado homogêneo por nível` | Todas as entradas de um mesmo nível compartilham o mesmo schema |
| `dado heterogêneo entre níveis` | Entradas de níveis distintos podem ter schemas diferentes |

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `JSON estrutural da tela` × `JSON externo de conteúdo` | `JSON estrutural da tela`: documento de configuração da interface — artefato de competência do módulo `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`; declara composição, tipos e elementos da tela; lido antes da execução. `JSON externo de conteúdo`: documento runtime externo fornecido ao console via envelope declarativo — de competência deste módulo; contém dados associados ao console durante a execução |
| `dado externo` × `dado de configuração` | Dado externo: fornecido ao console via envelope, não está no JSON de configuração do elemento; dado de configuração: campos declarados no schema da tela ou do contrato |
| `envelope declarativo` × `contrato_json_console.md` | Envelope: estrutura de dado externo fornecida ao console; contrato_json_console.md: schema normativo do próprio console |
| `nível` (dado) × `nível de grupo` (composição) | Nível do dado: camada hierárquica do envelope; nível de grupo: profundidade de aninhamento dos nós estruturais (módulo `40`) |
| `dado externo` (módulo 42) × `carregamento` (módulo 43) | Dado externo: o que existe no envelope; carregamento: como esse envelope é associado ao console e ao momento de carga |
| `schema semântico` × `schema de configuração` | Schema semântico: descreve campos de dado por nível; schema de configuração: descreve campos da tela, do console ou do contrato |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo do console que
  recebe dados externos.
- `contrato_json_console.md`: schema dos campos do console; o envelope declarativo
  é fornecido externamente e não coincide com o schema do contrato.

## 7. Relação com ADRs

- ADR-0026: fornecimento externo de dados ao console; envelope declarativo;
  schema semântico multinível.

## 8. Aliases ou termos descontinuados relacionados

Nenhum neste módulo.

## 8A. Termos concorrentes deferidos

Os termos abaixo aparecem em fontes primárias deste domínio mas **não são
termos canônicos ativos confirmados**. Registram diferenças terminológicas
ainda não reconciliadas. Não integram a contagem de termos ativos.

| Termo | Correspondência atual no schema | Estado | Localização no módulo `90` |
|---|---|---|---|
| `folha` | `conteudo` (campo do schema) | TERMO_CONCORRENTE_DEFERIDO | ver `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` |
| `campo` | `nome_valor` (campo do schema) | TERMO_CONCORRENTE_DEFERIDO | ver `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` |

A reconciliação entre esses termos e os nomes canônicos do schema está deferida
(ADR-0028). Nenhum dos dois nomes — nem o do termo nem o do schema — venceu
definitivamente a disputa terminológica. Os campos do schema não devem ser
renomeados com base nestes termos concorrentes.

## 9. Conteúdo que não pertence a este módulo

- Carregamento e associação do envelope ao console → módulo `43`.
- Apresentação e modos de exibição do dado carregado → módulo `44`.
- Schema normativo do console (campos de configuração) → `contrato_json_console.md`.
- Grupo como nó estrutural → módulo `40`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§17 (linhas 1535-1615)"
  intervalo_ou_bloco: "NOM-LEV-025"
origem_normativa: ADR-0026
contratos_relacionados:
  - contrato_console.md
  - contrato_json_console.md
adrs_relacionadas:
  - ADR-0026
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
