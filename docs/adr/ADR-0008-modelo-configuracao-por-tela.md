---
name: ADR-0008-modelo-configuracao-por-tela
description: modelo de configuracao passa de JSON por dominio/componente para JSON por tela, mantendo estilo.json como biblioteca global de estilo
metadata:
  type: adr
  status: aceita
  data: 2026-07-07
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/NOMENCLATURA.md
    - docs/INDICE.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_estilo.md
    - config/estilo.json
  handoffs_bloqueados: []
---

# ADR-0008 — modelo de configuração por tela

## Status

`aceita`

## Data

2026-07-07

## Contexto

A documentação vigente ainda segue a política de JSON por domínio ou por
componente de renderização. Nesse modelo, cada domínio como `estilo`,
`lancador`, `dashboard`, `barra_de_menus` e `cabecalho` tende a possuir seu
próprio JSON com dados concretos ou parâmetros de apresentação.

Esse modelo separou responsabilidades durante a Fase 0, mas agora cria uma
fronteira inadequada para a evolução do programa: composição de tela, itens de
`lancador`, chips, destinos, ações, regras de existência, regras de
ativo/inativo e casamento entre dados produzidos por scripts/leitores e campos
exibidos pertencem à tela concreta, não a uma classe global isolada.

Manter JSONs globais por componente faria o código ou os contratos globais
assumirem decisões que deveriam ser declarativas por tela. Isso aumentaria o
risco de hardcoding de composição, alinhamento, listas de itens, destinos e
regras visuais de instância.

Também é necessário corrigir a interpretação do `dashboard`: a estrutura
histórica do antigo `Info` com 8 campos, Total e 8 marcadores é uma instância
conhecida da tela raiz do Orquestrador, não uma regra universal da classe
`dashboard`.

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. O modelo canônico de configuração passa a ser por tela.**
Cada tela terá seu próprio JSON de configuração concreta. Esse JSON declara a
configuração da tela que o renderer deve executar.

**2. A estrutura macro da tela permanece fixa.**
Toda tela continua composta pelas três regiões macro já aprovadas:

1. `cabecalho`;
2. corpo;
3. `barra_de_menus`.

O JSON da tela configura essas regiões e suas instâncias; não redefine a
existência da estrutura macro.

**3. O JSON da tela declara a composição concreta da tela.**
O JSON de cada tela é a fonte dos dados concretos de:

- composição do corpo;
- tiling e posicionamento;
- instâncias de `lancador`, `dashboard`, `console` e `barra_de_menus`;
- parâmetros visuais locais;
- listas de itens;
- chips;
- destinos;
- ações;
- regras de existência;
- regras de ativo/inativo;
- casamento entre dados produzidos por scripts/leitores e campos exibidos.

**4. Mudanças declarativas devem ser possíveis sem alterar código.**
Quando uma mudança puder ser expressa por configuração, o programa deve mudar
pela alteração do JSON da tela, não por alteração de código. Exemplos:

- adicionar item ao `lancador`;
- mudar texto de item;
- mudar letra/chip;
- apontar para uma nova tela, desde que a nova tela tenha seu próprio JSON;
- ajustar alinhamento, colunas, espaçamento e regras de exibição.

**5. O código não deve hardcodar composição ou dados de instância.**
O código não deve hardcodar composição, alinhamento, itens de `lancador`, lista
de chips, destinos, nem regras visuais de instância. O renderer percorre as
listas declaradas no JSON da tela e renderiza conforme os contratos.

**6. `config/estilo.json` fica restrito à biblioteca global de estilo.**
`config/estilo.json` permanece como arquivo global apenas para presets e
parâmetros gerais de aparência, como:

- tipos de borda;
- tipos de moldura de chip;
- demais presets gerais de aparência, se mantidos.

`config/estilo.json` não declara tela, conteúdo de tela, composição, destino,
ação, item de `lancador` ou instância de `dashboard`.

**7. Não haverá `config/dashboard.json` próprio da classe `dashboard`.**
`dashboard` passa a ser definido como tipo mínimo:

- não navegável por `[✥]`;
- não obrigatório;
- com moldura própria;
- posicionável dentro do corpo conforme configuração da tela específica;
- sem conteúdo universal fixo.

**8. O antigo `Info` é draft de instância, não contrato universal.**
A especificação histórica do antigo `Info`, com 8 campos, Total e 8
marcadores, deve ser tratada como draft da instância de `dashboard` da tela
raiz do Orquestrador. Ela não define a classe universal `dashboard`.

**9. `lancador` passa a ser instância configurável por tela.**
Cada instância de `lancador` é declarada pelo JSON da tela, incluindo:

- título;
- lista de itens;
- chip/letra de cada item;
- texto de cada item;
- `tela_destino`;
- regras de exibição e layout da instância.

**10. A `barra_de_menus` deve preparar futura modelagem por classe `chip`.**
Chips canônicos e específicos devem poder ser instâncias declaradas em JSON. A
`barra_de_menus` de uma tela será uma lista desses chips. Cada chip poderá
declarar tecla/letra, texto, ação, regra de existência, regra de ativo/inativo
e forma de surgimento.

**11. Esta ADR não define o schema final de `tela.json`.**
O schema detalhado do JSON de tela será tratado em tarefa ou ADR posterior.
Esta ADR registra a mudança de arquitetura e os limites de responsabilidade,
mas não fecha todos os nomes de campo, validações e estruturas internas.

**12. Esta ADR não implementa código e não altera contratos ativos.**
A aplicação em `NOMENCLATURA.md`, contratos ativos, arquivos JSON e eventual
código será feita em tarefas separadas. Esta tarefa apenas registra a decisão
arquitetural.

**13. Artefatos históricos/transicionais devem ser arquivados no fechamento da Fase 0.**
Como pendência obrigatória de fechamento da Fase 0, os artefatos históricos ou
transicionais de rastreabilidade devem ser arquivados para limpar a
documentação ativa e evitar que buscas futuras priorizem contextos superados.

## Consequências

### Consequências arquiteturais

- O eixo principal de configuração concreta deixa de ser componente/domínio e
  passa a ser tela.
- O renderer passa a operar sobre declarações de instância por tela, percorrendo
  listas e objetos configurados em JSON.
- Componentes como `lancador`, `dashboard`, `console`, `cabecalho` e
  `barra_de_menus` continuam existindo como conceitos e contratos, mas seus
  dados concretos de instância pertencem ao JSON da tela.
- `config/estilo.json` permanece global, mas restrito a biblioteca de aparência.
- O modelo anterior de JSON por domínio/componente fica superado para conteúdo,
  composição, ações, destinos e instâncias.

### Artefatos a atualizar em tarefas posteriores

As alterações abaixo são obrigatórias, mas devem ocorrer em tarefas separadas:

| Arquivo | Atualização necessária |
|---|---|
| `docs/NOMENCLATURA.md` | Substituir a política de JSON por domínio/componente pelo modelo de JSON por tela; registrar `estilo.json` como biblioteca global; atualizar pendências de `dashboard`, `lancador`, `barra_de_menus` e `chip` |
| `docs/INDICE.md` | Atualizar a descrição de `config/` e a lista esperada de arquivos quando o novo modelo for aplicado |
| `docs/contratos/contrato_composicao_corpo.md` | Ajustar a origem da composição concreta para JSON da tela; remover dependência de JSON global por tipo de corpo quando aplicável |
| `docs/contratos/contrato_lancador.md` | Revisar `lancador` como instância configurável por tela; retirar a noção de lista global de itens |
| `docs/contratos/contrato_barra_de_menus.md` | Preparar chips canônicos e específicos como instâncias declaradas no JSON da tela; preparar contrato/classe `chip` |
| `docs/contratos/contrato_cabecalho.md` | Revisar textos e parâmetros locais como parte da configuração da tela, preservando a estrutura macro fixa |
| `docs/contratos/contrato_estilo.md` | Restringir `config/estilo.json` à biblioteca global de estilo e remover qualquer leitura como fonte de composição de tela |
| `config/*.json` | Revisar em tarefa própria; esta ADR não altera arquivos JSON |

### Arquivos que não devem ser alterados nesta tarefa

| Arquivo ou grupo | Motivo |
|---|---|
| Contratos ativos | A ADR deve ser aceita antes da aplicação contratual |
| `docs/NOMENCLATURA.md` | Aplicação da ADR fica para tarefa separada |
| `config/*.json` | O schema de `tela.json` ainda não foi detalhado |
| Qualquer arquivo de código | Implementação aguarda nomenclatura, contratos e schemas atualizados |

## Pendências derivadas

- Aplicar esta ADR em `docs/NOMENCLATURA.md`.
- Aplicar esta ADR nos contratos afetados.
- Definir o schema detalhado de `tela.json` em tarefa ou ADR posterior.
- Definir contrato/classe `chip`.
- Revisar `dashboard` como tipo mínimo e tratar o antigo `Info` como instância
  da tela raiz do Orquestrador.
- Revisar `lancador` como instância configurável por tela.
- Revisar `barra_de_menus` como lista de chips declarados por tela.
- Arquivar artefatos históricos/transicionais de rastreabilidade no fechamento
  da Fase 0.

## Fora de escopo

Os pontos abaixo não são decididos por esta ADR:

- Schema detalhado de `tela.json`.
- Estrutura final da classe/contrato `chip`.
- Nome, caminho e organização final dos JSONs de tela.
- Migração dos arquivos JSON existentes.
- Implementação em código.
- Alteração de contratos ativos nesta tarefa.
- Alteração de dados reais de telas.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Manter JSON por domínio/componente | Faz composição, itens, destinos e regras de instância vazarem para arquivos globais; incentiva hardcoding e dificulta mudar telas declarativamente |
| Criar `config/dashboard.json` universal | Universalizaria uma classe que deve ser mínima e sem conteúdo fixo; a estrutura do antigo `Info` é instância, não definição de tipo |
| Manter `config/lancador.json` com lista global de itens | Itens, textos, chips e destinos pertencem à tela concreta; uma lista global impede múltiplas instâncias com conteúdos diferentes |
| Resolver o schema completo de `tela.json` nesta ADR | A decisão arquitetural precisa ser registrada agora; o schema exige tarefa posterior própria para não misturar decisão de modelo com desenho detalhado de campos |
