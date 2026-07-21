---
name: nomenclatura-nucleo-comum
description: Conceitos transversais obrigatórios para interpretar qualquer módulo terminológico do sistema novo
metadata:
  type: nomenclatura
  scope: nucleo_comum
  fase_de_aplicacao: VIGENTE
---

# Núcleo comum

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo define exclusivamente os conceitos transversais necessários para
interpretar os demais módulos terminológicos. Ele não cobre domínios específicos
de componentes — esses pertencem aos módulos especializados.

Não incluir neste módulo: explicação detalhada de ADR, handoff, QA, relatório,
fluxo de desenvolvimento nem conteúdo de domínio de componente específico.

## 3. Termos proprietários

- autoridade terminológica
- termo canônico
- alias
- termo descontinuado
- schema
- configuração concreta
- estado de runtime
- elemento funcional
- container estrutural
- conteúdo
- produtor
- consumidor
- loader
- modelo
- renderizador
- regra de consulta ao módulo proprietário

## 4. Definições

### 4.1 Autoridade terminológica

Fonte documental que define oficialmente um termo. No sistema modular, cada
termo possui exatamente um módulo proprietário que detém sua autoridade
terminológica. Outros módulos podem referenciar o termo, nunca redefini-lo.

### 4.2 Termo canônico

Forma oficial e vigente de um nome. Usar o termo canônico em todos os novos
artefatos, contratos, handoffs e documentos normativos. Aliases e termos
descontinuados não são termos canônicos.

### 4.3 Alias

Forma alternativa reconhecida e controlada de um termo. Pode ser transitional
(compatibilidade com artefatos existentes) ou permanente. Todo alias possui
um termo canônico correspondente. Os aliases ativos estão em
`docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.

### 4.4 Termo descontinuado

Nome que foi substituído pelo termo canônico e não deve ser usado em novos
artefatos. Permanece reconhecível por compatibilidade histórica.
Registrado em `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.

### 4.5 Schema

Definição declarativa da estrutura de um documento ou campo: quais campos
existem, seus tipos, restrições e semântica. O schema não guarda valores
concretos de produção. No antigo monólito, substituído pela fachada na
fase 2 da ADR-0029, essa responsabilidade era do documento
`docs/NOMENCLATURA.md`, conforme ADR-0008. A autoridade vigente deste
domínio é o presente módulo e os demais módulos proprietários.
`docs/NOMENCLATURA.md` atua somente como fachada de compatibilidade e
navegação.

### 4.6 Configuração concreta

Documento que guarda os valores concretos que o renderer lê em tempo de
execução. Fica em `config/`, nunca dentro de `docs/`. Exemplos:
`config/estilo.json`, `config/telas/demo/<id>.json`.

### 4.7 Estado de runtime

Valores produzidos ou mantidos pela execução e não pertencentes ao JSON de
configuração. Exemplos: cursor atual, página atual, filtro ativo, modo
verboso ligado/desligado, seleção atual, item focado. O JSON pode declarar
defaults iniciais; o estado vivo pertence à execução.

### 4.8 Elemento funcional

Tipo de nó do corpo que produz saída visual e pode ser interativo. Os três
tipos funcionais válidos são `console`, `dashboard` e `lancador`. A lista é
fechada (ADR-0010, ADR-0015). Proprietário terminológico de cada tipo:
módulos `32`, `34` e `33` respectivamente.

### 4.9 Container estrutural

Nó de agrupamento que organiza outros nós mas não é elemento funcional.
O único container estrutural do corpo é `grupo`. `grupo` não tem borda própria,
título visual, ação, origem de dados nem `tela_destino`.
Proprietário: `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md`.

### 4.10 Conteúdo

Dados semânticos fornecidos a um elemento funcional. Pode ser declarado no
JSON estrutural da tela (estático) ou fornecido por documento externo de
runtime (dinâmico). Proprietário do vocabulário de conteúdo externo:
`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`.

### 4.11 Produtor

Componente ou script que produz o documento externo de conteúdo e o entrega
ao fluxo de apresentação. No ciclo atual da demonstração, o papel é exercido
por fixture permanente. No produto final, será um script ligado ao Pipeline.
Proprietário: `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`.

### 4.12 Consumidor

Componente que carrega e usa o documento externo de conteúdo. Não reconstrói
nem infere hierarquia. Trata a separação entre JSON estrutural e documento
externo. Proprietário: `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`.

### 4.13 Loader

Componente responsável por ler documentos, validar estrutura, converter
conteúdo externo para representação interna e preparar para o modelo.
Não decide geometria nem infere hierarquia.
Proprietário: `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`.

### 4.14 Modelo

Componente que transporta a estrutura semântica. Preserva ordem, níveis e
relação entre pais e filhos. Pode compor internamente sem apagar distinção
das origens. Não abre arquivos, não escolhe fontes, não calcula representação
física.

### 4.15 Renderizador

Componente que produz a representação física: linhas, colunas, truncamentos,
alinhamentos, posições, quebras e paginação. Tem responsabilidade exclusiva
sobre geometria, dimensões efetivas e resultados calculados. Não declara
intenção, não produz conteúdo semântico.

### 4.16 Regra de consulta ao módulo proprietário

Quando um termo for necessário para interpretar um artefato e não estiver
definido no módulo carregado:
1. Consultar `docs/nomenclatura/00_INDICE.md`.
2. Localizar o módulo proprietário do termo.
3. Ler somente esse módulo.
4. Não carregar todos os módulos preventivamente.

## 5. Distinções obrigatórias

| Par | Distinção |
|---|---|
| `schema` × `configuração concreta` | Schema define estrutura e semântica; configuração concreta guarda os valores |
| `configuração concreta` × `estado de runtime` | Configuração é declarada no JSON antes da execução; estado é produzido e mantido pela execução corrente |
| `elemento funcional` × `container estrutural` | Elementos funcionais produzem saída visual (`console`, `dashboard`, `lancador`); containers estruturais organizam outros nós (`grupo`) |
| `produtor` × `consumidor` | Produtor gera o documento externo de conteúdo; consumidor carrega e usa |
| `loader` × `renderizador` | Loader lê e converte; renderizador produz representação física |

## 6. Relação com contratos

Os contratos do sistema são autoridade do comportamento completo, validade,
processamento, erros e critérios de aceite. Este módulo define vocabulário
transversal que os contratos utilizam.

## 7. Relação com ADRs

- ADR-0008: estabelece a separação entre schema (atribuído ao antigo
  `docs/NOMENCLATURA.md`; autoridade migrada para os módulos proprietários
  pela ADR-0029), configuração concreta (`config/*.json`) e estado de runtime.
- ADR-0015: define elementos funcionais e container estrutural (`grupo`).
- ADR-0026, ADR-0027: definem produtor, consumidor, loader no contexto de dados externos.
- ADR-0029 (D-NOM-13): aprova a lista restrita de conceitos deste módulo.

## 8. Aliases ou termos descontinuados relacionados

Nenhum. Os aliases e termos descontinuados do sistema estão em
`docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.

## 9. Conteúdo que não pertence a este módulo

- Definição detalhada dos tipos funcionais (`console`, `dashboard`, `lancador`) →
  módulos `32`, `34`, `33`.
- Definição de `grupo` → módulo `40`.
- Comportamento completo de qualquer componente → contratos correspondentes.
- Explicação de ADR, handoff, QA, relatório, fluxo de desenvolvimento →
  documentação do processo.
- Domínio de qualquer componente específico → módulo proprietário do domínio.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "Regra (linhas 15-25) e §0 (linhas 27-56)"
  intervalo_ou_bloco: "NOM-LEV-002, NOM-LEV-003"
origem_normativa: ADR-0008, ADR-0015, ADR-0026, ADR-0027, ADR-0029 D-NOM-13
contratos_relacionados:
  - todos os contratos ativos (terminologia transversal)
adrs_relacionadas:
  - ADR-0008
  - ADR-0015
  - ADR-0026
  - ADR-0027
  - ADR-0029
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
