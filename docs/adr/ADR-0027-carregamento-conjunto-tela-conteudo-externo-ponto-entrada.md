---
name: ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada
description: Formaliza a responsabilidade do ponto de entrada real pelo carregamento separado do JSON estrutural da tela e do JSON externo de conteúdo, pela associação entre os dois documentos e pela entrega separada ao fluxo de construção e apresentação
metadata:
  type: adr
  status: aceita e aplicada
  data: "2026-07-17"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados:
    - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
---

# ADR-0027 — Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0027 |
| Título | Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada |
| Status | aceita e aplicada |
| Data | 2026-07-17 |
| Origem | Decisão explícita do usuário |

---

## 2. Status

`aceita e aplicada`

---

## 3. Contexto

### 3.1 Fechamento do H-0035

O ciclo H-0035 foi concluído com o commit `fb9e5be`, implementando a capacidade
genérica `distribuicao_matricial` de nível único para dashboard, console e
lançador. O H-0035 criou 26 configurações permanentes `h0035_*.json` em
`config/telas/demo/` e um demo dedicado em `demo/demo_distribuicao.py`.

### 3.2 ADR-0026 e sua aplicação

A ADR-0026 (2026-07-17, `aceita e aplicada`) formalizou a separação entre:

- **JSON estrutural da tela** (`tela.json`): composição e configuração
  estrutural da interface, sem dados de runtime do console;
- **documento externo de conteúdo**: dados de runtime fornecidos externamente
  ao console por JSON declarativo com envelope `{tipo, formato, dados}`;
- **resultado calculado**: representação física produzida exclusivamente pelo
  renderizador.

A aplicação documental da ADR-0026 atualizou os contratos ativos e a
nomenclatura para refletir essa separação. O QA pós-patch classificou a
aplicação como `ADR_APPLICATION_APPROVED_WITH_NOTES`.

### 3.3 Criação do H-0036

Com base na ADR-0026 aplicada, foi criado o H-0036 para implementar o
fornecimento externo de dados ao console por JSON multinível. O H-0036
definiu fixture permanente em `config/conteudo/h0036_console_multinivel.json`,
demo dedicado em `demo/demo_console_multinivel.py` como ponto de entrada e
mecanismo de carregamento direto pelo demo script.

### 3.4 Bloqueio H3_BLOCKED_DOCUMENTATION

O QA independente do H-0036 classificou o handoff como
`H3_BLOCKED_DOCUMENTATION`, com três achados bloqueantes:

1. **QAH-0036-001**: O mecanismo de entrega do documento externo ao console
   (carregamento por caminho de arquivo, loader com caminho, demo carregando
   diretamente a fixture) não tinha autoridade normativa ativa. A ADR-0026 e
   os contratos deixaram não decididos vínculo, caminho, mecanismo e APIs.

2. **QAH-0036-002**: A localização `config/conteudo/` foi identificada no
   próprio H-0036 como "a primeira convenção de localização de documentos
   externos de conteúdo", mas `NOMENCLATURA.md` §17.5 e ADR-0026 §14
   deixaram caminho, localização e ciclo de vida do documento externo como
   não decididos.

3. **QAH-0036-003**: O handoff exigia validações e provas de níveis,
   hierarquia, identificadores e campos obrigatórios, mas reconhecia que o
   schema interno de `dados[]` seria definido pela implementação ou por
   exceção operacional, deixando semântica material para o executor.

### 3.5 Necessidade desta ADR

A ADR-0026 separou estrutura e conteúdo, mas deixou em aberto:

- quem é responsável por carregar os dois documentos;
- como os dois documentos são associados para cada cenário;
- como a associação é feita sem criar campo de vínculo no JSON estrutural;
- onde as fixtures permanentes se localizam;
- como o conteúdo externo chega separado ao fluxo de construção da tela;
- como o demo real integra os dois documentos.

Sem essas decisões, qualquer handoff que tente implementar o fornecimento
externo precisará inventar mecanismo, localização ou protocolo sem autoridade.

### 3.6 Substituição futura da fixture

No H-0036, a fixture permanente funcionará como fonte controlada de
demonstração e teste. No produto final, os dados virão de um script que
buscará informações no projeto `Pipeline`. Esta ADR prepara a fronteira
semântica de consumo de forma que a troca futura da fonte não exija que o
console volte a depender de conteúdo incorporado ao JSON estrutural da tela.

---

## 4. Problema

### 4.1 Decisão da ADR-0026 que permaneceu em aberto

A ADR-0026 decidiu que configuração estrutural da tela e conteúdo de runtime
do console são documentos separados, mas deixou explicitamente não decididos
(ADR-0026 §14; contratos §§31.3, 19.7, 11.6, 11.8):

- a forma de vínculo entre `tela.json` e o documento externo;
- o mecanismo de carregamento e entrega do documento ao console;
- o caminho, a localização e o ciclo de vida do documento externo;
- as APIs, classes e módulos do consumidor;
- o schema completo e as validações do documento externo.

### 4.2 Consequência da lacuna

A lacuna deixada pela ADR-0026 permitiu um handoff (H-0036) que:

- usava `demo/demo_console_multinivel.py` como ponto de entrada em vez de
  `demo/demo.py`, deixando o ponto de entrada real fora do fluxo integrado;
- propunha demo dedicado como única forma de demonstrar a integração, sem
  exigir que o comportamento fosse acessível pelo ponto de entrada real;
- criava `config/conteudo/` como nova convenção global de localização de
  documentos externos de conteúdo, sem autoridade ativa para essa convenção;
- não definia quais JSONs do H-0035 com conteúdo de console precisariam ser
  revisados nominalmente;
- deixava parte da semântica de `dados[]` para decisão durante a
  implementação, via exceção operacional.

---

## 5. Decisão

Ficam registradas as seguintes decisões:

### D1 — Dois documentos separados

A demonstração e os testes do console usam dois documentos distintos:

1. um JSON estrutural que configura e monta a tela;
2. um JSON externo que contém o conteúdo de runtime apresentado pelo console.

Esses documentos não são fundidos. O JSON estrutural da tela não volta a
armazenar conteúdo de runtime do console.

### D2 — Responsabilidade do ponto de entrada real

O ponto de entrada real — `demo/demo.py` — é responsável por:

1. identificar a tela escolhida;
2. carregar o JSON estrutural correspondente;
3. carregar o JSON externo de conteúdo correspondente, quando a tela exigir
   conteúdo externo;
4. entregar separadamente a configuração estrutural e o conteúdo externo ao
   fluxo que constrói e apresenta a tela.

O `demo.py` não copia o conteúdo externo para dentro do objeto bruto do JSON
estrutural como se ele fizesse parte da configuração permanente da tela.

A separação conceitual e estrutural permanece observável durante todo o fluxo.

### D3 — Demonstração pelo ponto de entrada real

O H-0036 demonstra a capacidade pelo `demo/demo.py`.

Um demo dedicado não substitui o `demo.py` como única prova da integração.

Podem existir testes e auxiliares específicos, desde que o comportamento
também seja acessível e reproduzível pelo ponto de entrada real.

### D4 — JSONs permanentes do ciclo

O H-0036 cria ou atualiza nominalmente todos os arquivos JSON necessários para:

- testes automatizados;
- demonstração real;
- validação manual;
- prova da separação entre estrutura e conteúdo;
- prova da identidade semântica do conteúdo carregado.

O conteúdo necessário não pode ficar:

- codificado diretamente no teste;
- codificado diretamente no `demo.py`;
- codificado diretamente no renderizador;
- incorporado ao JSON estrutural;
- dependente de edição temporária feita pelo usuário.

### D5 — Revisão dos JSONs do H-0035

O H-0035 criou configurações permanentes em `config/telas/demo/h0035_*.json`.
Para cada JSON de tela afetado pelo H-0036 que contenha conteúdo de console
que deveria ser fornecido externamente:

1. preservar no arquivo estrutural somente a configuração da tela;
2. remover dele o conteúdo de runtime do console;
3. criar o documento externo correspondente;
4. atualizar testes e demonstrações para carregar os dois arquivos
   separadamente;
5. preservar a identidade e o objetivo original do cenário de teste.

JSONs do H-0035 que não contenham conteúdo de runtime do console não são
alterados. A futura correção do handoff deve inspecionar o repositório e
listar nominalmente apenas os arquivos realmente afetados.

### D6 — Localização das fixtures

Os documentos externos permanentes usados pelo H-0036 pertencem ao conjunto
existente de configurações e fixtures de teste e demonstração do projeto.

O H-0036 não cria silenciosamente uma nova convenção global de dados de
runtime do produto.

A localização e os nomes exatos dos arquivos devem:

- seguir a organização já existente no repositório;
- ficar nominalmente definidos no handoff corrigido;
- permitir distinguir claramente o JSON estrutural do JSON de conteúdo;
- ser permanentes e repetíveis;
- não depender de diretório global de runtime ainda não decidido.

Esta ADR não formaliza um diretório global definitivo para dados produzidos
pelo produto final.

### D7 — Associação no catálogo da demonstração

O catálogo ou mecanismo interno usado pelo `demo.py` deve ser capaz de
associar, para cada cenário aplicável:

```text
configuração estrutural da tela
+
documento externo de conteúdo
```

Essa associação pertence ao ponto de entrada e à demonstração do ciclo.

Ela não cria um campo de vínculo dentro do JSON estrutural da tela.

Ela também não define o protocolo final entre o Orquestrador e o projeto
Pipeline.

Os detalhes de implementação da associação — nome de variável, classe, função,
estrutura interna de dicionário, assinatura concreta, formato de argumento de
linha de comando — não são decididos por esta ADR. Esses detalhes podem ser
definidos na implementação, desde que preservem a responsabilidade e a
separação aprovadas.

### D8 — Entrega ao fluxo da tela

A configuração estrutural e o conteúdo externo chegam como entradas separadas
ao fluxo de construção e apresentação da tela.

A implementação define a representação interna necessária, mas não pode:

- reinserir o conteúdo no JSON estrutural;
- exigir que o renderizador abra arquivos;
- exigir que o modelo descubra sozinho qual arquivo carregar;
- exigir que o console reconstrua a hierarquia a partir de dados não
  normalizados.

As responsabilidades em camadas são:

| Camada | Responsabilidade |
|---|---|
| Ponto de entrada (`demo.py`) | Carregar os dois documentos; associar para o cenário; entregá-los separadamente ao fluxo |
| Loader ou camada equivalente | Validar e converter os documentos; produzir representação interna |
| Modelo | Transportar o conteúdo semântico sem lógica geométrica |
| Renderizador | Produzir a representação física na área disponível |

### D9 — Fonte provisória e produtor futuro

No H-0036, o arquivo JSON permanente funciona como fonte controlada de
demonstração e teste.

No produto final, o conteúdo virá de um script que buscará dados no projeto
`Pipeline`. O script futuro produzirá ou devolverá dados compatíveis com o
mesmo contrato semântico consumido pelo console.

A troca futura:

```text
arquivo JSON permanente de teste
→
resultado produzido pelo script de integração com o Pipeline
```

não exige que o console volte a depender de conteúdo incorporado ao JSON
estrutural da tela.

### D10 — Direção da integração futura com o Pipeline

Ficam registradas somente as seguintes direções já decididas:

- haverá um script produtor;
- o script buscará dados no projeto `Pipeline`;
- os dados retornados já estarão adequados à representação multinível;
- o Orquestrador consumirá o documento resultante pela mesma fronteira
  semântica preparada no H-0036.

O protocolo concreto de integração permanece para decisão futura (ADR-0026 §14).

### D11 — Schema semântico multinível: decidido e obrigatório

O schema semântico multinível definido pela decisão explícita do usuário e
pelo anexo externo `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md` é
**decidido e obrigatório** para o H-0036. Ele não está deferido.

Este registro não constitui escolha nova do autor desta ADR: incorpora a
semântica que estava implícita na decisão original, tornando-a verificável
pelos ciclos subsequentes.

#### D11.1 — Envelope raiz obrigatório

A raiz do documento externo de conteúdo é um objeto com os campos:

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "hierarquia",
    "niveis": []
  },
  "dados": []
}
```

Regras:

- a raiz é um objeto;
- `tipo` é obrigatório e deve ser `"multinivel"`;
- `formato` é obrigatório e deve ser objeto;
- `dados` é obrigatório e deve ser array;
- `formato.apresentacao` é obrigatório;
- `formato.niveis` é obrigatório e deve ser array;
- os níveis são declarados explicitamente no campo `formato.niveis`;
- o consumidor não infere a hierarquia a partir de dados de domínio não
  normalizados.

#### D11.2 — Apresentações multinível previstas

O schema reconhece as seguintes apresentações:

```text
tabela
hierarquia
conjuntos_campos
```

Cada apresentação possui blocos próprios de `formato`:

**Tabela:**

```json
{
  "apresentacao": "tabela",
  "niveis": [],
  "tabela": {
    "cabecalho": [],
    "ancestrais": "repetir"
  },
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

**Hierarquia:**

```json
{
  "apresentacao": "hierarquia",
  "niveis": [],
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

**Conjuntos e campos:**

```json
{
  "apresentacao": "conjuntos_campos",
  "niveis": [],
  "campos": {},
  "espacamento": {},
  "alinhamento": {},
  "excesso": {},
  "paginacao": {}
}
```

Blocos específicos devem ser omitidos quando não pertencem à apresentação
escolhida:

- `tabela` somente em `apresentacao: "tabela"`;
- `campos` somente em `apresentacao: "conjuntos_campos"`;
- nenhum dos dois em `apresentacao: "hierarquia"`.

#### D11.3 — Declaração dos níveis

Cada item de `formato.niveis` deve declarar:

```json
{
  "id": "identificador_do_nivel",
  "tipo": "container",
  "conteudo": "titulo",
  "designador": {
    "tipo": "decimal"
  }
}
```

**Campo `id`:**

- identifica o nível;
- deve ser string não vazia;
- deve ser único dentro de `formato.niveis`;
- é referenciado pelo campo `nivel` dos nós.

**Campo `tipo`** — valores previstos:

```text
container
conteudo
nome_valor
```

**Campo `conteudo`:**

Para `container` e `conteudo`, indica o nome do campo do nó que contém o
texto exibível:

```json
{ "conteudo": "titulo" }
```

Para `nome_valor`, declara os campos usados:

```json
{
  "conteudo": {
    "nome": "nome",
    "valor": "valor"
  }
}
```

**Campo `designador`:**

Declara a forma do marcador visual do nível. Tipos previstos:

```text
nenhum
simbolo
decimal
alfabetico_minusculo
alfabetico_maiusculo
romano_minusculo
romano_maiusculo
decimal_composto
personalizado
```

Podem ser usados, conforme o tipo: `prefixo`, `sufixo`, `valor`,
`separador`. A sequência concreta do designador é calculada pelo
renderizador. O JSON não deve armazenar a numeração concreta já calculada.

#### D11.4 — Forma canônica dos nós

Cada nó em `dados` ou em `filhos` deve possuir:

```json
{
  "id": "identificador",
  "nivel": "id_de_nivel_declarado"
}
```

Regras comuns:

- `id` é obrigatório;
- `nivel` é obrigatório;
- `nivel` deve referenciar um item de `formato.niveis`;
- a ordem dos arrays é a ordem semântica original;
- o consumidor não reordena os nós;
- a hierarquia é expressa por `filhos`;
- o consumidor não reconstrói hierarquia a partir de nomes, IDs ou
  convenções externas.

**Nós de nível `container`:**

```json
{
  "id": "conjunto_1",
  "nivel": "conjunto",
  "titulo": "Conjunto 1",
  "filhos": []
}
```

- deve conter o campo indicado por `nivel.conteudo`;
- deve conter `filhos` como array;
- os filhos são outros nós do mesmo schema.

**Nós de nível `conteudo`:**

```json
{
  "id": "conteudo_1",
  "nivel": "item",
  "titulo": "Texto exibível"
}
```

- deve conter o campo indicado por `nivel.conteudo`;
- representa conteúdo diretamente exibível;
- não depende de inferência de outro dado de domínio.

**Nós de nível `nome_valor`:**

```json
{
  "id": "elemento_1",
  "nivel": "elemento",
  "nome": "Elemento 1",
  "valor": "Valor do elemento 1."
}
```

- deve conter o campo indicado por `conteudo.nome`;
- deve conter o campo indicado por `conteudo.valor`;
- o separador visual pertence a `formato.campos`, quando aplicável;
- o JSON não deve armazenar alinhamentos físicos já calculados.

#### D11.5 — Exemplo normativo mínimo de três níveis

O exemplo abaixo é normativo: demonstra o schema semântico como autoridade
para o H-0036, não é fixture definitiva do ciclo.

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "conjuntos_campos",
    "niveis": [
      {
        "id": "conjunto",
        "tipo": "container",
        "conteudo": "titulo",
        "designador": {
          "tipo": "decimal",
          "sufixo": "."
        }
      },
      {
        "id": "subconjunto",
        "tipo": "container",
        "conteudo": "titulo",
        "designador": {
          "tipo": "decimal_composto",
          "separador": ".",
          "sufixo": "."
        }
      },
      {
        "id": "elemento",
        "tipo": "nome_valor",
        "conteudo": {
          "nome": "nome",
          "valor": "valor"
        },
        "designador": {
          "tipo": "nenhum"
        }
      }
    ],
    "campos": {
      "separador": ":",
      "justificar_nomes": true,
      "escopo_justificacao": "por_conjunto"
    },
    "espacamento": {},
    "alinhamento": {},
    "excesso": {
      "modo": "verboso"
    },
    "paginacao": {}
  },
  "dados": [
    {
      "id": "conjunto_1",
      "nivel": "conjunto",
      "titulo": "Conjunto 1",
      "filhos": [
        {
          "id": "subconjunto_1_1",
          "nivel": "subconjunto",
          "titulo": "Subconjunto 1.1",
          "filhos": [
            {
              "id": "elemento_1",
              "nivel": "elemento",
              "nome": "Elemento 1",
              "valor": "Valor do elemento 1."
            }
          ]
        }
      ]
    }
  ]
}
```

#### D11.6 — Resultados físicos proibidos no schema

Os seguintes resultados são de responsabilidade exclusiva do renderizador e
**não devem** constar no documento externo:

```text
larguras e alturas efetivas
quantidade física final de linhas e colunas
posições finais
coordenadas físicas
páginas calculadas
quebras físicas
truncamentos já aplicados
distribuição concreta do espaço restante
células vazias calculadas
geometria final
numeração concreta de designadores
```

O renderizador continua responsável por:

- geometria e dimensões efetivas;
- quebras físicas;
- truncamentos;
- alinhamentos calculados;
- paginação física;
- posições finais;
- recuperação após redimensionamento.

### D12 — Alcance do H-0036

O H-0036 deve implementar:

- leitura separada dos dois documentos pelo `demo.py`;
- entrega separada ao fluxo da tela;
- validação do JSON externo segundo os contratos ativos;
- representação semântica;
- apresentação no console;
- atualização dos JSONs permanentes afetados do H-0035;
- criação dos JSONs externos permanentes correspondentes;
- testes;
- demonstração real pelo `demo.py`;
- validação manual.

O H-0036 não implementa:

- o script que buscará dados no Pipeline;
- protocolo definitivo de integração entre projetos;
- suporte externo ao tipo `matriz`, salvo nova decisão;
- cache;
- atualização automática;
- persistência;
- versionamento;
- navegação multinível;
- expansão ou recolhimento;
- paginação interativa.

O H-0036 deverá tratar as três apresentações multinível previstas no schema
(`tabela`, `hierarquia`, `conjuntos_campos`) conforme as regras incorporadas
nesta ADR e nos contratos resultantes da sua aplicação. Nenhuma apresentação
pode ser silenciosamente descartada pelo executor sem nova decisão do usuário.

### D13 — Validações semânticas mínimas

As seguintes validações são obrigatórias para o documento externo de conteúdo
e devem ser verificadas pelo loader ou camada equivalente:

1. raiz é objeto;
2. presença e tipo correto de `tipo`;
3. valor de `tipo` é `"multinivel"`;
4. presença e tipo objeto de `formato`;
5. presença e tipo array de `dados`;
6. presença de `formato.apresentacao`;
7. `formato.apresentacao` pertence ao conjunto previsto
   (`tabela`, `hierarquia`, `conjuntos_campos`);
8. presença e tipo array de `formato.niveis`;
9. cada item de `formato.niveis` possui `id`, `tipo`, `conteudo` e `designador`;
10. IDs de nível não vazios e não duplicados em `formato.niveis`;
11. tipos de nível pertencem ao conjunto previsto
    (`container`, `conteudo`, `nome_valor`);
12. cada nó em `dados` possui `id` e `nivel`;
13. cada valor de `nivel` em nó existe na declaração de `formato.niveis`;
14. nós de tipo `container` possuem o campo declarado em `conteudo` e `filhos`
    como array;
15. nós de tipo `conteudo` possuem o campo declarado em `conteudo`;
16. nós de tipo `nome_valor` possuem os campos declarados em `conteudo.nome`
    e `conteudo.valor`;
17. filhos são validados recursivamente com as mesmas regras;
18. a ordem dos arrays é preservada pelo consumidor;
19. campos específicos da apresentação são compatíveis com `apresentacao`;
20. o documento não contém resultados físicos calculados.

---

## 6. Fluxo conceitual

```text
JSON estrutural da tela ─┐
                         ├─> demo.py / ponto de entrada
JSON externo de conteúdo ┘
                                   ↓
                     validação e construção do modelo
                     (loader ou camada equivalente)
                                   ↓
                          modelo com conteúdo semântico
                                   ↓
                               renderizador
                                   ↓
                       representação física na área disponível
```

Os dois documentos permanecem separados em todo o fluxo. O ponto de entrada
os carrega; o loader os valida; o modelo os transporta; o renderizador produz
a representação física.

O renderizador não abre arquivos. O modelo não descobre qual arquivo carregar.
O console não reconstrói hierarquia.

---

## 7. JSONs permanentes

### 7.1 Princípio

Todos os JSONs necessários aos cenários devem ser criados ou atualizados pelo
H-0036. Cada cenário afetado deve possuir arquivos permanentes nominalmente
definidos no handoff corrigido.

### 7.2 Proibições

Dados de cenários de teste e demonstração não podem ficar:

- codificados em Python (em teste, demo ou renderizador);
- incorporados ao JSON estrutural da tela como se fossem configuração
  permanente da interface;
- dependentes de edição temporária pelo usuário.

### 7.3 JSONs do H-0035 afetados

A futura correção do H-0036 deve:

1. inspecionar os 26 JSONs `h0035_*.json` criados em `config/telas/demo/`;
2. identificar quais contêm conteúdo de console que deveria ser fornecido
   externamente;
3. listar nominalmente cada arquivo afetado;
4. para cada arquivo afetado: separar configuração estrutural de conteúdo
   externo, criar o JSON externo correspondente, e preservar a identidade do
   cenário original.

JSONs não afetados permanecem intactos.

### 7.4 Localização das fixtures

As fixtures permanentes seguem a organização existente do repositório. O
handoff corrigido define nominalmente cada arquivo. A localização deve
distinguir claramente o JSON estrutural do JSON de conteúdo e ser repetível
sem depender de convenção global de runtime não decidida.

---

## 8. Demonstração real

### 8.1 Ponto de entrada obrigatório

`demo/demo.py` é o ponto de entrada obrigatório da demonstração integrada. O
comportamento do H-0036 deve ser acessível e reproduzível por esse ponto de
entrada.

### 8.2 Demos e auxiliares específicos

Podem existir demos dedicados, testes auxiliares e scripts de diagnóstico
específicos para o H-0036. Esses artefatos são válidos e bem-vindos.

### 8.3 Proibição

Um demo dedicado não pode ser a única prova do comportamento integrado. A
integração deve também ser demonstrável pelo ponto de entrada real.

---

## 9. Fronteira com o Pipeline

### 9.1 Fixture como substituto controlado

No H-0036, o arquivo JSON permanente funciona como substituto controlado do
produtor futuro. Ele tem o mesmo formato semântico que o script futuro deverá
produzir.

### 9.2 Compatibilidade futura

O script futuro do projeto Pipeline deverá fornecer um documento com o mesmo
tipo de contrato semântico consumido pelo console neste ciclo. A substituição:

```text
fixture permanente → resultado do script de integração
```

não exigirá que o console receba conteúdo incorporado ao JSON estrutural.

### 9.3 Protocolo não definido

O protocolo do script futuro — nome, repositório, localização, forma de
execução, argumentos, transporte, stdout, arquivo temporário, códigos de
saída, mensagens de erro, timeout, sincronismo, autenticação, versionamento,
atualização automática e cache — permanece para decisão futura.

---

## 10. Compatibilidade

Esta ADR é compatível com e não altera:

| Autoridade | Preservação |
|---|---|
| ADR-0025 e H-0035 | Distribuição matricial configurável de nível único permanece inalterada |
| ADR-0026 | Separação entre JSON estrutural e documento externo de conteúdo é preservada e estendida; nenhuma decisão da ADR-0026 é reescrita |
| Contratos ativos | Seções existentes sobre distribuição matricial, composição do corpo, loader, modelo e renderizador permanecem válidas |
| Telas não afetadas | Telas sem conteúdo externo de console não são alteradas; placeholder `"(console)"` é preservado para essas telas |
| Responsabilidade geométrica do renderizador | Geometria, quebras, truncamentos, alinhamentos, paginação e posições continuam sob responsabilidade exclusiva do renderizador |
| Comportamento sem conteúdo externo | Console sem conteúdo externo preserva o comportamento histórico; nenhuma migração automática |

---

## 11. Documentos afetados

Documentos normativos a atualizar na aplicação desta ADR:

| Documento | Motivo |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0027 após QA e aplicação documental autorizada |
| `docs/NOMENCLATURA.md` | Formalizar a responsabilidade do ponto de entrada pelo carregamento e associação separados; formalizar a fixture como fonte provisória; preservar decisões deferidas da ADR-0026 |
| `docs/contratos/contrato_tela_json.md` | Registrar que o JSON estrutural da tela não contém campo de vínculo ao documento externo; que a associação é responsabilidade do ponto de entrada |
| `docs/contratos/contrato_console.md` | Formalizar como o conteúdo externo chega ao console: pelo ponto de entrada via loader, não pelo console abrindo arquivos; formalizar as camadas de responsabilidade |
| `docs/contratos/contrato_json_console.md` | Formalizar o uso de fixtures permanentes; registrar a responsabilidade do ponto de entrada pela associação; propagar o schema semântico multinível de D11 e as validações de D13; preservar como não decididos os demais itens da ADR-0026 §14 |

---

## 12. Aplicação futura

A aplicação documental desta ADR deve, no mínimo:

- atualizar o índice com a ADR-0027;
- propagar a responsabilidade do ponto de entrada nos contratos afetados;
- formalizar a associação externa sem campo de vínculo no JSON estrutural;
- propagar o schema semântico multinível de D11 e as validações de D13 nos
  contratos afetados;
- formalizar o uso das fixtures permanentes e sua organização junto ao
  conjunto existente de artefatos de teste e demonstração;
- formalizar a revisão dos JSONs afetados do H-0035 como obrigação do ciclo;
- manter deferido o protocolo com o Pipeline;
- registrar as camadas de responsabilidade (ponto de entrada, loader, modelo,
  renderizador) sem inventar APIs, classes ou assinaturas;
- preparar a base para o `PATCH_HANDOFF` do H-0036.

---

## 13. Relação com o H-0036 atual

O handoff H-0036 permanece como artefato criado e reprovado por bloqueio
documental (`H3_BLOCKED_DOCUMENTATION`). Ele não é cancelado, substituído
nem renumerado.

Depois da aplicação desta ADR, o H-0036 deverá ser corrigido por
`PATCH_HANDOFF`. A futura correção deverá remover ou substituir qualquer
regra incompatível com as decisões desta ADR, especialmente:

- preservação de `demo/demo.py` como apenas um arquivo a não alterar, sem
  atribuir a ele a responsabilidade de carregamento dos dois documentos;
- uso de demo dedicado como única integração;
- criação não autorizada de `config/conteudo/` como convenção global;
- autorização de decisão de schema semântico por exceção operacional sem
  autoridade normativa;
- preservação genérica dos JSONs do H-0035 sem revisão nominal dos afetados;
- afirmação de exequibilidade baseada apenas no envelope mínimo, sem
  confirmar mecanismo de entrega ao console.

O H-0036 não é corrigido nesta etapa.

---

## 14. Decisões deferidas

Permanecem para decisão futura, não decididos por esta ADR:

| Item | Status |
|---|---|
| Nome de variável, classe, função, dicionário, assinatura, argumento de linha de comando do mecanismo de associação | Não decidido — definível na implementação |
| Lista nominal dos JSONs do H-0035 realmente afetados | Não decidido — definível na inspeção do `PATCH_HANDOFF` |
| Localização e nomes exatos das fixtures permanentes | Não decidido — definível no `PATCH_HANDOFF`, com restrição: seguir organização existente |
| APIs e classes definitivas do consumidor/loader | Não decidido (ADR-0026 §14; contratos §19.3, §11.8) |
| Forma de vínculo entre `tela.json` e documento externo no produto final | Não decidido (ADR-0026 §14; contratos §31.3) |
| Nome do script produtor futuro, repositório, localização | Não decidido |
| Forma de execução do script futuro | Não decidido |
| Argumentos do script | Não decidido |
| Transporte (stdout, arquivo temporário, outro) | Não decidido |
| Códigos de saída do script | Não decidido |
| Mensagens de erro | Não decidido |
| Timeout | Não decidido |
| Sincronismo | Não decidido |
| Autenticação | Não decidido |
| Versionamento do documento externo ou do produtor | Não decidido |
| Ciclo de vida do documento externo no produto final | Não decidido |
| Atualização automática | Não decidido |
| Cache | Não decidido |
| Diretório global definitivo de dados de runtime do produto | Não decidido |
| Suporte ao tipo `matriz` no mecanismo de fornecimento externo | Não decidido (ADR-0026 §9) |
| Comportamento diante de fonte ausente ou inválida | Não decidido |
| Navegação multinível, expansão, recolhimento, paginação interativa | Não decididos |

---

## 15. Fora de escopo

Estão explicitamente fora do escopo desta ADR:

- aplicação documental desta ADR;
- QA desta ADR;
- correção do H-0036;
- implementação de qualquer funcionalidade;
- criação ou alteração dos JSONs permanentes de teste ou demonstração;
- alteração do `demo.py` ou de qualquer arquivo de código;
- integração real com o Pipeline;
- execução de testes;
- validação manual;
- commit.

---

## 16. Verificações de integridade

Esta ADR foi verificada quanto aos seguintes critérios:

| # | Verificação | Resultado |
|---|---|---|
| 1 | Não incorpora conteúdo ao JSON estrutural | Confirmado — D1, D4, D8 proíbem explicitamente |
| 2 | Não cria campo de vínculo no JSON estrutural | Confirmado — D7 especifica que a associação não cria campo no JSON estrutural |
| 3 | Torna o `demo.py` responsável por carregar os dois documentos | Confirmado — D2, D3, D8 |
| 4 | Exige JSONs permanentes para todos os cenários afetados | Confirmado — D4, §7 |
| 5 | Exige revisão nominal dos JSONs do H-0035 afetados | Confirmado — D5, §7.3 |
| 6 | Não cria diretório global definitivo de runtime | Confirmado — D6, §7.4, §13 (deferred decisions) |
| 7 | Não define o protocolo do script futuro | Confirmado — D10, §9.3, §14 |
| 8 | Preserva a mesma fronteira semântica para a futura origem Pipeline | Confirmado — D9, D10, §9 |
| 9 | Não corrige o H-0036 antecipadamente | Confirmado — §13 |
| 10 | Não altera a ADR-0026 retrospectivamente | Confirmado — §10, §3.2 |
| 11 | Não atribui ao renderizador a leitura de arquivos | Confirmado — D8 |
| 12 | Schema semântico multinível decidido e incorporado; não delegado silenciosamente à implementação | Confirmado — D11 (D11.1–D11.6), D13 |

---

## 17. Critérios para aplicação

A aplicação documental desta ADR só poderá ocorrer depois de:

- ADR criada;
- QA independente da ADR;
- ausência de bloqueio documental;
- identificação nominal dos documentos afetados.

---

## 18. Patch — correção do achado QAADR-0027-001

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_ADR-0027.md
achado_corrigido: QAADR-0027-001
correcao:
  - schema semântico multinível incorporado em D11 (D11.1–D11.6)
  - validações mínimas incorporadas em D13
  - schema removido das decisões deferidas (§14)
  - H-0036 passa a poder criar fixtures e renderização sem decisão arquitetural silenciosa
```

Este patch corrige a contradição identificada no QA: a ADR exigia representação
multinível material, validação, fixtures, identidade semântica e apresentação no
console, mas mantinha o schema de `dados[]` como não decidido.

O schema semântico incorporado neste patch tem como autoridade a decisão
explícita do usuário e o anexo externo
`ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md`. Ele não constitui escolha
nova do autor desta ADR.

O futuro `PATCH_HANDOFF` poderá, sem inventar schema adicional:

- criar fixtures permanentes multinível com os campos definidos em D11;
- validar os campos obrigatórios de níveis e nós segundo D13;
- implementar representação semântica no modelo;
- produzir renderização conforme `formato`;
- criar testes de nós e níveis;
- verificar prova de identidade semântica;
- inspecionar e revisar nominalmente os JSONs afetados do H-0035;
- demonstrar o fluxo completo pelo `demo.py`.

Os caminhos definitivos das fixtures e a lista nominal dos JSONs afetados do
H-0035 continuam pertencendo ao futuro `PATCH_HANDOFF` (§14).
