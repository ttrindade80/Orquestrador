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
- documento de resultado de execução (ADR-0034)
- envelope de erro multinível (ADR-0034)
- projeção semântica
- extensão compatível da projeção semântica (ADR-0047)
- escolha ativa persistida (ADR-0048)
- literal público `filho_default` (ADR-0048, D-0026-12)

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

### 4.5 Documento de resultado de execução (ADR-0034)

A ADR-0034 introduz um subtipo específico de dado externo: o documento
produzido pelo Orquestrador para apresentar o resultado (ou o erro) de uma
operação focal invocada sobre um lote reconciliado (`ITEM-0006`).
Autoridade comportamental completa em `contrato_json_console.md` §14.

| Termo | Definição |
|---|---|
| `documento de resultado de execução` | Documento JSON externo, distinto do `JSON externo de conteúdo` genérico (§4.1), que transporta o resultado estruturado ou o envelope de erro de uma operação focal executada sobre o lote reconciliado |
| `envelope de erro multinível` | Forma do documento de resultado quando o processo falha ou produz resultado ausente/inválido — reutiliza o `tipo: "multinivel"` e a apresentação `conjuntos_campos` já definidos por este módulo, com a lista fixa de campos `status`, `diagnostico`, `codigo_saida`, `stdout`, `stderr`, `resultado_json` |

O documento de resultado de execução não redefine o schema semântico
multinível geral (§4.4); ele é um uso concreto desse schema para um
propósito específico (apresentar resultado/erro de execução), com campos
fixos próprios em vez do vocabulário livre de níveis do conteúdo do
console.

### 4.6 Extensão compatível da projeção semântica (ADR-0047)

A `projeção semântica` é o conjunto de campos semânticos entregues ao
console. Uma `extensão compatível da projeção semântica` expõe
separadamente um dado semântico que já existe no fluxo, preservando os
campos antigos para compatibilidade. Não constitui alteração do conteúdo
visível nem do significado dos dados.

### 4.7 Escolha ativa persistida de filho por pai (ADR-0048)

Para cada pai sujeito à política `dois_niveis_por_foco`
(`docs/nomenclatura/32_CONSOLE.md` §4.10; ADR-0042), a `escolha ativa
persistida` é o dado semântico, fornecido explicitamente pelo produtor no
documento externo de conteúdo, que identifica exatamente um filho ativo.
Não é resultado físico calculado, não é geometria e não é configuração de
apresentação da tela.

A escolha ativa persistida é distinta de:

- seleção exclusiva obrigatória de filho por pai
  (`docs/nomenclatura/32_CONSOLE.md` §4.10) — mecanismo comportamental de
  runtime que transfere a escolha por Espaço; a escolha ativa persistida é o
  dado de origem/destino desse mecanismo quando carregado ou aplicado;
- posição do primeiro filho — não é tratada como autoridade persistida da
  escolha (comportamento predecessor da capacidade, ADR-0042).

Autoridade comportamental completa do ciclo de baseline, candidato e
aplicação: `contrato_console.md` §26. Literal público fechado:
`filho_default` (D-0026-12, patch `P02`; ver `contrato_json_console.md`
§16.7).

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `JSON estrutural da tela` × `JSON externo de conteúdo` | `JSON estrutural da tela`: documento de configuração da interface — artefato de competência do módulo `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`; declara composição, tipos e elementos da tela; lido antes da execução. `JSON externo de conteúdo`: documento runtime externo fornecido ao console via envelope declarativo — de competência deste módulo; contém dados associados ao console durante a execução |
| `dado externo` × `dado de configuração` | Dado externo: fornecido ao console via envelope, não está no JSON de configuração do elemento; dado de configuração: campos declarados no schema da tela ou do contrato |
| `envelope declarativo` × `contrato_json_console.md` | Envelope: estrutura de dado externo fornecida ao console; contrato_json_console.md: schema normativo do próprio console |
| `nível` (dado) × `nível de grupo` (composição) | Nível do dado: camada hierárquica do envelope; nível de grupo: profundidade de aninhamento dos nós estruturais (módulo `40`) |
| `dado externo` (módulo 42) × `carregamento` (módulo 43) | Dado externo: o que existe no envelope; carregamento: como esse envelope é associado ao console e ao momento de carga |
| `schema semântico` × `schema de configuração` | Schema semântico: descreve campos de dado por nível; schema de configuração: descreve campos da tela, do console ou do contrato |
| `JSON externo de conteúdo` (genérico) × `documento de resultado de execução` (ADR-0034) | Conteúdo genérico: dados de domínio apresentados pelo console em operação; documento de resultado: resultado ou erro estruturado de uma operação focal executada sobre um lote reconciliado — campos fixos, não vocabulário livre de níveis |
| `envelope de entrada do pop-up` × `envelope declarativo multinível` | O envelope do pop-up pertence ao domínio `35` e transporta conteúdo pronto de uma abertura; não é o envelope multinível do console e não declara níveis, produtor ou origem de dados |
| `extensão compatível da projeção semântica` × `alteração do conteúdo visível` | Uma projeção pode expor separadamente um dado semântico já existente no fluxo, preservando os campos antigos para compatibilidade. Isso não altera o conteúdo visível. A extensão não transfere configuração, tabulação, colunas, espaçamento nem geometria para os dados |
| `escolha ativa persistida` (ADR-0048) × `seleção exclusiva obrigatória de filho por pai` (ADR-0042, módulo `32`) | A escolha ativa persistida é o dado semântico do documento externo que declara o filho ativo por pai; a seleção exclusiva obrigatória de filho por pai é o mecanismo comportamental de runtime que a lê, transfere por Espaço e, quando confirmado, converte um candidato em novo valor a persistir |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo do console que
  recebe dados externos.
- `contrato_json_console.md`: schema dos campos do console; o envelope declarativo
  é fornecido externamente e não coincide com o schema do contrato; seção 14
  fecha o documento de resultado de execução e o envelope de erro multinível;
  seção 16 fecha a escolha ativa persistida e o literal público
  `filho_default` (ADR-0048, D-0026-12).

## 7. Relação com ADRs

- ADR-0026: fornecimento externo de dados ao console; envelope declarativo;
  schema semântico multinível.
- ADR-0034: documento de resultado de execução; envelope de erro multinível;
  obrigação de preservação literal do texto inválido fixada em
  `contrato_json_console.md` §14.6.
- ADR-0047: extensão compatível da projeção semântica, distinta de
  alteração do conteúdo visível; tabulação, apresentação tabular e
  geometria não pertencem a este módulo.
- ADR-0048: escolha ativa persistida de filho por pai como dado semântico do
  documento externo, distinta da posição do primeiro filho e da seleção
  exclusiva obrigatória de runtime (módulo `32`); literal público
  `filho_default` fechado por D-0026-12 (patch `P02`); autoridade
  comportamental completa em `contrato_console.md` §26.

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
- Envelope de entrada do pop-up modal → módulo `35`; não ampliar este domínio
  para cobrir a capacidade da ADR-0044.

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
