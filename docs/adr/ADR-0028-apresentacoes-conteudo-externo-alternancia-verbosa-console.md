---
name: ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console
description: Formaliza as apresentações multinível de conteúdo externo no console, as regras normativas de cada apresentação, o estado de visualização verboso/não verboso e a semântica da tecla V para alternância durante a sessão
metadata:
  type: adr
  status: aceita e aplicada
  data: "2026-07-17"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0028 — Apresentações de conteúdo multinível no console e alternância verbosa

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0028 |
| Título | Apresentações de conteúdo multinível no console e alternância verbosa |
| Status | aceita e aplicada |
| Data | 2026-07-17 |
| Origem | Decisão explícita do usuário |

---

## 2. Status

`aceita e aplicada`

Aplicação documental registrada em:
`docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md`

---

## 3. Contexto

### 3.1 Estado documentado ao encerramento do H-0036

O ciclo H-0036 foi fechado com o commit `f6982d0`. Ele implementou:

- separação entre o JSON estrutural da tela e o JSON externo de conteúdo;
- carregamento separado dos dois documentos pelo ponto de entrada real;
- entrega conjunta da estrutura e do conteúdo ao fluxo de apresentação;
- conteúdo externo `tipo: multinivel`;
- apresentações em tabela, hierarquia e conjuntos;
- fixtures permanentes para esses três cenários.

O H-0036 não implementou como capacidade obrigatória completa:

- todas as políticas declarativas do conteúdo multinível;
- o cenário de conjunto com subconjunto e campos (três profundidades);
- a alternância interativa entre modo verboso e não verboso.

### 3.2 ADRs anteriores

A ADR-0026 (`aceita e aplicada`, 2026-07-17) formalizou:

- a separação entre JSON estrutural da tela e documento externo de conteúdo;
- o envelope conceitual `{tipo, formato, dados}`;
- a responsabilidade exclusiva do renderizador sobre os resultados físicos calculados.

A ADR-0027 (`aceita e aplicada`, 2026-07-17) formalizou:

- a responsabilidade do ponto de entrada real pelo carregamento separado dos dois documentos e pela entrega conjunta ao fluxo de construção e apresentação;
- o schema semântico multinível obrigatório com três apresentações, três tipos de nível, forma dos nós, designadores e 20 validações mínimas;
- o uso de fixtures permanentes junto ao conjunto existente de artefatos de demonstração.

### 3.3 Autoridade externa desta ADR

O usuário forneceu como autoridade normativa desta ADR o documento:

```text
CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md
```

Esse contrato estabelece regras normativas para representar, alinhar, espaçar, truncar, quebrar, paginar e renderizar conteúdos hierárquicos com múltiplos níveis. Ele define:

- modelo hierárquico comum com raiz única, níveis, tipos e relações;
- tipos de nível: contêiner, folha e campo;
- designadores configuráveis e independentes da estrutura;
- modos de apresentação: tabela, hierarquia indentada e conjuntos com campos;
- margens, recuos, vãos e preenchimentos;
- alinhamentos naturais e justificados com escopos;
- modos não verboso e verboso, truncamento, quebra e continuação;
- paginação com preservação de contexto e blocos indivisíveis;
- validações e impossibilidade geométrica.

O contrato está em estado de proposta consolidada para posterior definição do schema JSON. Os nomes definitivos das propriedades JSON, valores padrão e outros itens listados em §43 do contrato são deliberadamente adiados.

Este documento é entrada normativa desta ADR. Ele não é copiado para o repositório e suas regras não são declaradas como já aplicadas aos contratos existentes do projeto.

**O documento `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md`, utilizado como referência na versão inicial desta ADR, não é autoridade para esta decisão. Qualquer regra derivada exclusivamente desse documento foi removida nesta versão corrigida.**

### 3.4 Necessidade desta ADR

O H-0036 deixou fora do escopo original:

- as políticas declarativas completas das apresentações multinível;
- o cenário com subconjunto intermediário (conjunto → subconjunto → campo);
- a alternância interativa entre modo verboso e não verboso;
- a tecla `V` e a ação `[V] Verboso` na barra de menus;
- a distinção entre estado de visualização da sessão e persistência no arquivo externo.

Sem a formalização dessas decisões, qualquer ciclo subsequente precisará inventar estado, comportamento ou política sem autoridade normativa ativa.

---

## 4. Problema

### 4.1 Lacuna de cobertura normativa completa

As regras declarativas completas das apresentações multinível — modelo hierárquico, tipos de nível, designadores, espaçamentos, alinhamentos, excesso, paginação, validações e impossibilidade geométrica — não estão formalizadas como decisão normativa deste projeto.

### 4.2 Lacuna de cenários de demonstração

O cenário com estrutura de três profundidades (conjunto → subconjunto → campo) não está definido como demonstração permanente obrigatória.

### 4.3 Lacuna de alternância visual

Nenhuma ADR anterior decidiu:

- a existência do estado de visualização verboso/não verboso;
- a semântica da tecla `V`;
- como o estado é inicializado e mantido durante a sessão;
- que o estado de visualização é da sessão e não é persistente no arquivo externo;
- que a alternância não exige troca de tela.

### 4.4 Lacuna de critérios de teste

Os critérios de teste semântico para as novas capacidades — incluindo a exigência de que código de saída zero não é prova suficiente — não estão formalizados.

---

## 5. Autoridades lidas

| Documento | Relação com a decisão |
|---|---|
| `CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` | Autoridade normativa externa desta ADR. Define o modelo hierárquico, apresentações, espaçamentos, alinhamentos, excesso, paginação e validações. |
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | Autoridade sobre separação entre JSON estrutural e conteúdo externo; preservada sem alteração. |
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | Autoridade sobre carregamento separado, entrega conjunta, schema multinível e validações; preservada sem alteração. |
| `docs/adr/INDICE_ADR.md` | Registra sequência e status das ADRs aceitas. |

---

## 6. Escopo exclusivo: console com conteúdo multinível

Esta ADR aplica-se exclusivamente a dados multinível exibidos em componentes do tipo `console`.

Ela não se aplica a:

- `dashboard`;
- `lancador`;
- componentes genéricos que não sejam `console`;
- distribuição matricial de nível único (ADR-0025);
- conteúdo matricial (`tipo: matriz`);
- telas sem conteúdo multinível externo.

Quando esta ADR mencionar "conteúdo", "dados", "apresentação" ou "renderização", trata-se sempre de conteúdo multinível exibido no `console`.

---

## 7. Origem atual dos dados

Atualmente, o `console` recebe o conteúdo multinível como um documento JSON externo armazenado em arquivo.

O ponto de entrada — `orquestrador` ou `demo` — deve:

1. identificar a tela escolhida;
2. carregar o JSON estrutural da tela;
3. carregar separadamente o documento JSON externo de conteúdo multinível;
4. entregar os dois documentos conjuntamente ao fluxo de carregamento, modelo e renderização, mantendo-os como entradas distintas.

Os dois documentos permanecem separados. O JSON estrutural da tela não incorpora os dados de conteúdo.

---

## 8. Origem futura pelo Pipeline

Depois da integração com o projeto Pipeline, os dados de conteúdo multinível poderão ser produzidos ou fornecidos por um script do Pipeline.

Mesmo nessa integração futura:

- os dados continuarão chegando ao Orquestrador no formato de um documento JSON;
- o documento respeitará a mesma fronteira semântica esperada pelo `console`;
- o conteúdo continuará separado do JSON estrutural da tela;
- a substituição da origem em arquivo pela origem em script não exigirá reinserção dos dados no JSON estrutural;
- o `console` não dependerá internamente de qual mecanismo produziu o JSON.

Esta ADR não define o protocolo concreto de integração com o Pipeline. Ver §43 (decisões adiadas).

---

## 9. Fronteira estável em JSON

O documento JSON de conteúdo multinível é a fronteira semântica estável entre o produtor dos dados e o `console`.

Seja a origem um arquivo ou um script do Pipeline, o `console` consumirá sempre um documento com a mesma estrutura semântica declarada pelo projeto.

---

## 10. Relação com ADR-0026

A ADR-0026 permanece autoridade ativa sobre:

- a separação entre JSON estrutural da tela e documento externo de conteúdo;
- o envelope conceitual `{tipo, formato, dados}`;
- o princípio de que o JSON declara intenção e conteúdo semântico, e o renderizador calcula a representação física.

Esta ADR amplia a fronteira normativa do conteúdo externo sem contradizer nem substituir a ADR-0026.

---

## 11. Relação com ADR-0027

A ADR-0027 permanece autoridade ativa sobre:

- a responsabilidade do ponto de entrada real pelo carregamento separado e entrega conjunta;
- o schema semântico multinível (envelope raiz, três apresentações, três tipos de nível, forma dos nós, designadores, 20 validações mínimas);
- o uso de fixtures permanentes.

Esta ADR complementa a ADR-0027, adicionando regras normativas derivadas do contrato correto. As 20 validações da ADR-0027 permanecem válidas e são complementadas pelas validações da §33 desta ADR.

---

## 12. Decisões

As seguintes decisões ficam registradas. Cada decisão reproduz a intenção explícita do usuário sem acrescentar política nova.

### D1 — Conteúdo externo ao JSON estrutural

Os dados multinível exibidos no `console` permanecem separados do JSON estrutural da tela.

O JSON estrutural não deve conter cópia dos dados exibidos.

### D2 — Documento JSON como fronteira de consumo

O `console` recebe um documento JSON de conteúdo multinível.

Atualmente o documento é lido de arquivo externo. Futuramente poderá ser produzido ou fornecido por um script do Pipeline. A origem concreta não altera a forma semântica consumida pelo `console`.

### D3 — Carregamento separado e entrega conjunta

O ponto de entrada deve:

1. carregar separadamente o JSON estrutural da tela e o documento JSON de conteúdo multinível;
2. entregar os dois documentos conjuntamente ao fluxo interno de carregamento, modelo e renderização.

Os documentos são carregados separadamente e entregues conjuntamente ao fluxo interno, permanecendo distintos e sem incorporação do conteúdo externo ao JSON estrutural da tela. Entrega conjunta não implica fusão, cópia ou reinserção de conteúdo.

Esta decisão preserva e reitera as decisões D2 e D8 da ADR-0027.

### D4 — Estrutura independente da apresentação

A estrutura dos dados de conteúdo multinível não depende do modo visual escolhido.

Os mesmos dados podem ser apresentados como tabela multinível, hierarquia indentada ou conjuntos e campos. A troca de modo visual não exige mudança dos dados, apenas configuração compatível.

A troca de modo de apresentação não altera níveis, relações pai–filho, ordem semântica, identidade dos nós nem valores originais.

### D5 — Designadores independentes da estrutura

Os designadores não definem a estrutura.

A troca entre tipos de designador (decimal, alfabético, símbolo, composto, nenhum) não altera os dados, os níveis ou as relações entre nós.

### D6 — Estrutura hierárquica declarada

O conteúdo multinível deve possuir estrutura hierárquica declarada, incluindo raiz única, identificadores de níveis, tipos de nível, relações, origens dos conteúdos e filhos quando aplicável.

O renderizador não deve inferir silenciosamente a hierarquia quando ela for requerida para a renderização.

### D7 — Tipos conceituais de níveis

O conteúdo multinível reconhece os seguintes tipos conceituais de nível:

- **contêiner**: nó que pode possuir filhos;
- **folha**: nó sem filhos;
- **campo**: folha composta por nome, separador opcional e valor.

O schema existente do projeto usa os termos `container`, `conteudo` e `nome_valor` para tipos correspondentes. A correspondência conceitual está registrada em §34. Nenhuma renomeação é decidida por esta ADR.

### D8 — Cenários de apresentação multinível

Os cenários mínimos de demonstração do conteúdo multinível no `console` são:

1. tabela multinível;
2. hierarquia indentada;
3. conjunto com campos nome–valor (dois níveis);
4. conjunto, subconjunto e campos nome–valor (três níveis).

Os cenários 3 e 4 podem pertencer ao mesmo modo conceitual de apresentação (`conjuntos_campos`), mas possuem estruturas semânticas diferentes e devem ser demonstrados separadamente.

### D9 — Modo não verboso

No modo não verboso, cada conteúdo aplicável ocupa uma única linha física. Ver §21 para as regras completas.

### D10 — Modo verboso

No modo verboso, o conteúdo pode ocupar várias linhas físicas. Ver §22 para as regras completas.

### D11 — Alternância pela tecla V em telas alternáveis

A tecla `V` atua exclusivamente em telas alternáveis, alternando entre os modos verboso e não verboso durante a sessão.

A alternância usa os mesmos dados, a mesma tela e o mesmo documento de conteúdo; não troca a apresentação e não persiste alteração. É reversível: uma segunda ativação retorna ao modo anterior.

Em telas de modo único (somente verbosa ou somente não verbosa), a tecla V não é ação aplicável da tela.

### D12 — Modo inicial

O modo inicial é determinado pela política de modo de apresentação declarada pela tela (D23):

- **telas de modo único** iniciam necessariamente em seu único modo — verboso para telas somente verbosas, não verboso para telas somente não verbosas;
- **telas alternáveis** devem declarar o modo inicial; o modo inicial pode ser verboso ou não verboso.

A pergunta "como uma tela alternável inicia?" não é mais uma lacuna aberta. A obrigação de declarar o modo inicial existe; o nome concreto do campo e o mecanismo de schema para essa declaração ficam adiados conforme §43.

### D13 — Conteúdo declarativo do JSON de conteúdo

O documento JSON deve declarar somente conteúdo semântico e políticas declarativas, incluindo quando aplicável: estrutura hierárquica, estilos de designadores, modo de apresentação, espaçamentos, alinhamentos, tratamento de excesso e paginação.

Ele não deve conter resultados físicos previamente calculados.

### D14 — Responsabilidade do renderizador

Pertencem ao renderizador: cálculo da área útil, larguras efetivas, alturas efetivas, recuos acumulados, larguras reservadas, colunas iniciais, linhas físicas, quebras, truncamentos aplicados, páginas, repetição visual de cabeçalhos, repetição visual de ancestrais, posições finais, impossibilidade geométrica e recuperação após redimensionamento.

### D15 — Tabela multinível

A tabela multinível deve ser implementada conforme as regras da §17.

### D16 — Hierarquia indentada

A hierarquia indentada deve ser implementada conforme as regras da §18.

### D17 — Conjuntos e campos

Os cenários de conjuntos e campos devem ser implementados conforme as regras da §19 e da §20.

### D18 — Quebra de palavras

O modo verboso deve possuir política declarada para palavras maiores que a largura disponível. Ver §28.

### D19 — Paginação e contexto

A paginação deve preservar contexto conforme as regras da §30 e §31.

### D20 — Impossibilidade geométrica

Quando nem a unidade mínima de conteúdo multinível couber na área útil disponível, o `console` deve acionar a política de impossibilidade geométrica. Ver §32.

### D21 — Validações

O loader ou camada equivalente deve rejeitar configurações inválidas conforme a §33.

### D22 — Demonstração e validação

A futura implementação deverá possuir demonstrações permanentes e provas semânticas conforme a §36 e a §37.

### D23 — Política de modo de apresentação da tela

Cada tela de console multinível deve declarar sua política de modo de apresentação. A política admite três classes conceituais:

a) **somente verbosa** — a tela sempre abre em modo verboso; não há alternância por `V`; o chip `[V] Verboso` não é obrigatório; o comportamento visual segue as regras do modo verboso;

b) **somente não verbosa** — a tela sempre abre em modo não verboso; não há alternância por `V`; o chip `[V] Verboso` não é obrigatório; o comportamento visual segue as regras do modo não verboso; truncamento com `...` permanece válido quando aplicável;

c) **alternável** — a tela suporta os dois modos; o chip `[V] Verboso` é obrigatório; a tecla `V` alterna entre os dois modos; a alternância é reversível; a tela deve declarar o modo inicial, que pode ser verboso ou não verboso.

**Escopo de aplicação de D23 — telas novas ou revisadas e telas legadas**

A obrigação declarativa de D23 aplica-se a telas novas ou revisadas para adotar a capacidade definida por esta ADR:

- omitir a política é inválido para essas telas;
- uma tela alternável deve declarar também o modo inicial;
- não existe default implícito que substitua a declaração obrigatória.

Telas criadas antes da incorporação de D23 — como as do ciclo H-0036, usado aqui apenas como exemplo histórico de tela legada — permanecem válidas segundo os contratos vigentes no momento de sua criação:

- não devem ser reinterpretadas automaticamente como uma das três políticas;
- não recebem campo, valor ou default por inferência;
- não precisam ser migradas por esta ADR;
- continuam sujeitas a futura decisão de migração e compatibilidade.

---

## 13. Modelo hierárquico comum

O conteúdo multinível exibido no `console` é representável como árvore:

```text
nível_1
├── nível_2
│   ├── nível_3
│   └── nível_3
└── nível_2
    └── nível_3
```

### 13.1 Raiz única

A estrutura deve possuir exatamente um nível raiz.

### 13.2 Identificadores de níveis

Os níveis devem possuir identificadores estruturais independentes de sua designação visual.

### 13.3 Relações pai–filho

Cada nível, exceto a raiz, deve declarar seu nível pai ou ser referenciado como filho por exatamente um nível estrutural compatível.

### 13.4 Quantidade de níveis

A quantidade de níveis deve ser declarada pela estrutura e não deve ser presumida pelo renderizador.

### 13.5 Compatibilidade dos dados

Os dados recebidos devem ser compatíveis com a estrutura declarada. Dados com nível ausente, relação inválida ou tipo incompatível devem provocar rejeição ou erro de validação.

### 13.6 Determinismo

A mesma configuração, os mesmos dados e a mesma área útil devem produzir o mesmo resultado.

### 13.7 Estabilidade entre páginas

Larguras, alinhamentos e designadores calculados para uma renderização não devem variar entre páginas, salvo quando a configuração declarar explicitamente escopo por página.

---

## 14. Tipos conceituais de níveis e conteúdo associado

### 14.1 Contêiner

Nível do tipo contêiner pode possuir filhos. Deve declarar o nível de seus filhos.

Um contêiner pode declarar título, chave, descrição, metadados auxiliares e filhos.

### 14.2 Folha

Nível do tipo folha não deve declarar filhos.

Uma folha pode declarar texto principal, chave, título, valor simples e metadados auxiliares.

### 14.3 Campo

Nível do tipo campo deve ser composto conceitualmente por:

```text
designador + nome + separador + valor
```

O designador e o separador podem não existir, desde que a configuração assim declare.

Um campo deve declarar, no mínimo: origem do nome, origem do valor e separador quando existente.

### 14.4 Origem dos valores

Cada conteúdo exibido deve possuir uma origem declarada nos dados, como chave, título, nome, valor ou campo equivalente.

---

## 15. Designadores

### 15.1 Presença opcional

Cada nível deve poder declarar designador presente ou designador ausente.

### 15.2 Tipos mínimos de designador

O sistema deve admitir, no mínimo:

```text
nenhum
simbolo fixo
decimal
alfabetico minusculo
alfabetico maiusculo
romano minusculo
romano maiusculo
composto
personalizado
```

### 15.3 Componentes do designador

Um estilo de designador pode ser composto por prefixo, valor gerado e sufixo.

### 15.4 Designadores compostos

Designadores compostos podem incorporar valores de níveis ancestrais.

Exemplos:

```text
1.
1.1
1.1.1
```

### 15.5 Escopo de reinício

Cada estilo enumerativo deve declarar seu escopo de reinício:

```text
global
por pai
por pagina
sem reinicio
```

Quando o escopo for por pai, a contagem do nível filho deve reiniciar para cada novo pai.

A paginação não deve reiniciar a numeração, salvo declaração explícita de reinício por página.

### 15.6 Largura e alinhamento do designador

O alinhamento dos designadores pode usar largura fixa, calculada entre irmãos, calculada em todo o nível, calculada no conteúdo completo ou calculada por página.

Recomenda-se evitar cálculo por página quando a estabilidade visual entre páginas for necessária.

---

## 16. Modos de apresentação multinível

O sistema deve admitir:

1. `tabela` — apresentação tabular multinível;
2. hierarquia indentada — apresentação hierárquica com recuo por nível;
3. `conjuntos_campos` — apresentação de conjuntos com campos nome–valor.

Cada modo deve validar se a estrutura declarada é compatível com sua forma de apresentação. A troca de modo visual não deve exigir mudança dos dados.

**Nota terminológica:** O contrato externo usa `hierarquia_indentada` para o modo de apresentação hierárquica. O schema existente do projeto (estabelecido pela ADR-0027) usa `hierarquia`. Esta diferença está registrada em §34. Nenhuma renomeação é decidida por esta ADR.

---

## 17. Tabela multinível

### 17.1 Cabeçalho obrigatório

Toda apresentação em tabela deve possuir cabeçalho declarado. Tabela sem cabeçalho é inválida.

### 17.2 Colunas declaradas

Cada coluna deve declarar: identificador, texto do cabeçalho, nível ou campo de origem, ordem, política de largura, alinhamento horizontal, alinhamento vertical e tratamento de excesso.

Coluna de tabela sem nível ou campo de origem é inválida.

### 17.3 Caminho completo por linha lógica

Por padrão, cada caminho completo da raiz até uma folha deve produzir uma linha lógica.

Exemplo:

```text
NÍVEL 1      NÍVEL 2       NÍVEL 3
Conjunto 1   Elemento A    Valor X
Conjunto 1   Elemento B    Valor Y
Conjunto 2   Elemento C    Valor Z
```

### 17.4 Ordem das linhas

A ordem das linhas deve preservar a ordem dos dados ou a ordenação explicitamente declarada.

### 17.5 Política de ancestrais

Para valores ancestrais repetidos, a tabela deve declarar uma política:

- repetir em todas as linhas;
- mostrar apenas na primeira linha do grupo;
- mesclar visualmente.

A mesclagem visual não deve alterar a quantidade de linhas lógicas nem os dados subjacentes.

### 17.6 Margens e espaços estruturais

A tabela deve poder declarar: margem superior, inferior, esquerda e direita; espaço antes do cabeçalho; espaço entre cabeçalho e corpo; espaço entre colunas; e espaço entre linhas.

Preenchimento interno e espaço entre colunas não devem ser tratados como a mesma medida.

### 17.7 Preenchimento de célula

Cada célula ou estilo de coluna deve poder declarar preenchimento esquerdo, direito, superior e inferior.

### 17.8 Largura das colunas

Cada coluna deve admitir pelo menos uma das políticas de largura: fixa, mínima, máxima, ajustada ao conteúdo, proporcional ou uniformemente distribuída.

A largura útil interna da célula é calculada por:

```text
largura útil = largura da coluna - preenchimento esquerdo - preenchimento direito
```

Quando houver largura mínima e máxima, a máxima deve ser maior ou igual à mínima; caso contrário a configuração é inválida.

Larguras ajustadas ao conteúdo devem declarar o escopo de cálculo.

### 17.9 Alinhamento da tabela

Cada coluna deve poder declarar alinhamento horizontal (início, centro, fim) e alinhamento vertical quando verbosa (topo, centro, base). O cabeçalho pode possuir alinhamento distinto do corpo.

### 17.10 Excesso não verboso em tabela

No modo não verboso, cada célula deve ocupar exatamente uma linha física. Quando o conteúdo não couber, ele deve ser truncado dentro da largura útil. O marcador de truncamento deve caber integralmente na largura útil.

### 17.11 Excesso verboso em tabela

No modo verboso, o conteúdo pode ocupar várias linhas físicas dentro da mesma célula.

A altura física de uma linha lógica deve ser determinada pela célula que produzir a maior quantidade de linhas físicas. As demais células da mesma linha lógica devem respeitar a altura calculada e seu alinhamento vertical.

O modo verboso pode declarar quantidade máxima de linhas. Quando excedido, a última linha permitida deve aplicar a política final declarada.

### 17.12 Paginação da tabela

A tabela pagina por linhas lógicas. O cabeçalho deve ser repetido em todas as páginas.

Uma linha lógica verbosa não deve ser dividida entre páginas quando couber integralmente em uma página vazia.

Quando uma única linha lógica for maior que toda a área útil de uma página vazia, a configuração deve declarar uma política: permitir divisão, limitar linhas e truncar, ou declarar impossibilidade.

A política de repetição ou mesclagem de ancestrais deve continuar determinística entre páginas.

---

## 18. Hierarquia indentada

### 18.1 Uma linha lógica por nó

Cada nó deve gerar uma linha lógica própria, salvo quando um modo específico agrupar nome e valor na mesma linha.

### 18.2 Recuo por nível

Cada transição de nível deve possuir recuo declarado em espaços. O sistema deve admitir recuo uniforme por nível ou recuo específico por transição.

O recuo de um nível deve ser a soma dos recuos das transições ancestrais.

O renderizador não deve depender do caractere de tabulação do terminal. O equivalente ao "tab" deve ser declarado em espaços.

### 18.3 Margens e espaços internos

A apresentação deve poder declarar: margem superior, inferior, esquerda e direita; espaço entre designador e conteúdo; espaço entre linhas do mesmo nó; espaço entre nós irmãos; espaço entre níveis; espaço entre grupos; e espaço entre subconjuntos.

Os espaços entre irmãos, níveis e grupos não devem ser combinados em uma única medida implícita.

### 18.4 Alinhamento natural dos designadores

No alinhamento natural, o conteúdo começa imediatamente após o designador real e o espaço configurado.

Exemplo:

```text
1. Texto
10. Texto
100. Texto
```

### 18.5 Alinhamento justificado dos designadores

No alinhamento justificado, o sistema deve reservar uma largura comum para designadores.

Exemplo:

```text
  1. Texto
 10. Texto
100. Texto
```

A configuração deve separar o alinhamento do designador dentro da largura reservada do início do conteúdo após essa largura. Toda justificação deve declarar seu escopo.

### 18.6 Excesso não verboso em hierarquia

No modo não verboso, cada nó deve ocupar uma linha física.

A largura disponível do conteúdo deve descontar margem esquerda, margem direita, recuo acumulado, largura reservada do designador e espaço entre designador e conteúdo.

Quando o texto exceder a largura disponível, ele deve ser truncado com o marcador configurado.

### 18.7 Excesso verboso em hierarquia

No modo verboso, o conteúdo pode ocupar várias linhas físicas.

As linhas de continuação devem começar na coluna inicial do conteúdo e não na coluna inicial do designador.

A coluna de continuação deve considerar:

```text
margem esquerda
+ recuo acumulado
+ largura reservada do designador
+ espaço entre designador e conteúdo
```

Exemplo:

```text
1. Este é o início de um conteúdo extenso
   que continua na linha seguinte e permanece
   alinhado ao início do conteúdo.
```

### 18.8 Paginação hierárquica

Ancestrais devem ser repetidos ou indicados quando a página começar no interior de um ramo. Ver §30 e §31.

---

## 19. Conjuntos com campos nome–valor (dois níveis)

### 19.1 Estrutura

O sistema deve admitir a estrutura de dois níveis:

```text
conjunto
└── campo nome–valor
```

Exemplo de saída:

```text
1. Título do conjunto 1:
    a. Nome do elemento 1: valor do elemento 1.
    b. Nome do elemento 2: valor do elemento 2.
```

### 19.2 Estrutura da linha nome–valor

Uma linha nome–valor deve ser composta conceitualmente por:

```text
designador + nome + separador + valor
```

O separador pode ser omitido quando a configuração declarar conteúdo sem separador.

### 19.3 Separador

O separador pode ser `:`, `=`, `-`, `→` ou outro valor personalizado.

A configuração deve distinguir espaço antes do separador e espaço depois do separador.

### 19.4 Justificação dos nomes

No modo não justificado, o valor começa após o nome real, o separador e os espaços configurados.

No modo justificado, o sistema deve reservar uma largura comum para os nomes.

Exemplo:

```text
1. Conjunto 1:
    a. nome:             valor
    b. nome muito maior: valor
    c. id:               valor
```

A largura reservada para nomes deve declarar um escopo.

### 19.5 Coluna inicial do valor

A coluna inicial do valor deve ser calculada com base em todos os componentes anteriores:

```text
margem esquerda
+ recuo acumulado
+ largura do designador
+ espaço entre designador e nome
+ largura reservada do nome
+ espaço antes do separador
+ largura do separador
+ espaço depois do separador
+ espaço adicional antes do valor
```

O renderizador não deve usar uma quantidade fixa de espaços ignorando esses componentes.

### 19.6 Espaçamentos nome–valor

A configuração deve poder declarar: espaço entre designador e nome; largura reservada para o nome; espaço antes do separador; espaço depois do separador; espaço adicional antes do valor; espaço entre campos; e espaço entre conjuntos.

### 19.7 Excesso não verboso em nome–valor

No modo não verboso, a linha nome–valor deve ocupar uma única linha física.

Quando o espaço for insuficiente, recomenda-se a seguinte prioridade de preservação:

1. recuo estrutural;
2. designador obrigatório;
3. nome;
4. separador;
5. espaço mínimo;
6. valor;
7. marcador de truncamento.

Por padrão, o valor deve ser truncado antes do nome. Outra prioridade somente pode ser usada mediante declaração explícita.

Quando nem nome, separador e marcador de truncamento couberem, o layout deve ser considerado geometricamente impossível.

### 19.8 Excesso verboso em nome–valor

No modo verboso, o valor pode continuar em múltiplas linhas.

Toda linha de continuação deve começar exatamente na coluna inicial do valor.

Exemplo:

```text
elemento 1:       início do texto até o
                  limite disponível; o texto
                  continua alinhado ao valor.
```

---

## 20. Conjuntos, subconjuntos e campos nome–valor (três níveis)

### 20.1 Estrutura

O sistema deve admitir a estrutura de três níveis:

```text
conjunto
└── subconjunto
    └── campo nome–valor
```

Exemplo de saída:

```text
1. Conjunto 1:
    1.1 Subconjunto 1.1:
        a. Elemento 1: valor do elemento 1.
        b. Elemento 2: valor do elemento 2.
```

### 20.2 Designadores independentes por nível

Conjuntos, subconjuntos e campos podem usar estilos de designador distintos ou nenhum designador.

### 20.3 Quantidade declarada

A quantidade de níveis não deve ser inferida pelo modo de apresentação de conjuntos e campos.

### 20.4 Espaçamentos com subconjunto

A configuração deve poder declarar espaço entre subconjuntos, além dos espaços já definidos em §19.6.

### 20.5 Repetição de contexto na paginação

O título do conjunto e, quando aplicável, do subconjunto devem ser repetidos quando seus campos continuarem em nova página. Ver §30 e §31.

---

## 21. Modo não verboso

No modo não verboso:

1. cada conteúdo aplicável ocupa uma única linha física;
2. não há continuação em linhas adicionais;
3. o conteúdo excedente é truncado;
4. o marcador de truncamento deve caber integralmente na largura útil;
5. os dados originais permanecem inalterados;
6. o JSON não armazena texto previamente truncado.

Aplicações por apresentação:

- **Tabela**: uma linha física por célula;
- **Hierarquia**: uma linha física por nó;
- **Nome–valor**: uma linha física para os componentes da linha lógica.

Modo não verboso configurado para mais de uma linha é inválido.

---

## 22. Modo verboso

No modo verboso:

1. o conteúdo pode ocupar várias linhas físicas;
2. as quebras são calculadas pelo renderizador;
3. as linhas de continuação respeitam o alinhamento definido;
4. pode existir limite máximo de linhas por nó ou célula;
5. o excesso ao limite segue a política final declarada;
6. as linhas físicas calculadas não são armazenadas no JSON.

Aplicações por apresentação:

- **Tabela**: a altura da linha lógica é determinada pela célula de maior altura; as demais células respeitam essa altura;
- **Hierarquia**: a continuação começa na coluna inicial do conteúdo;
- **Nome–valor**: a continuação começa na coluna inicial calculada para o valor.

Modo verboso com limite de uma linha não deve ser tratado automaticamente como modo não verboso. Modo verboso sem regra de alinhamento da continuação é inválido.

---

## 23. Tecla V

A tecla `V` atua exclusivamente em telas alternáveis, alternando entre os modos verboso e não verboso durante a sessão.

Em telas alternáveis, a barra de menus deve apresentar:

```text
[V] Verboso
```

O chip `[V] Verboso` é obrigatório somente em telas alternáveis. Sua presença representa a disponibilidade da alternância. Em telas de modo único (somente verbosa ou somente não verbosa), o chip não é obrigatório e a tecla `V` não é ação aplicável da tela.

A alternância: usa os mesmos dados; usa a mesma tela; usa o mesmo documento de conteúdo; não troca a apresentação; não persiste alteração; é reversível. Uma segunda ativação deve retornar ao modo anterior.

---

## 24. Estado visual da sessão

O estado de visualização verboso/não verboso é um estado da sessão. Ele não deve:

- reescrever o JSON externo de conteúdo;
- reescrever o JSON estrutural da tela;
- alterar permanentemente uma fixture;
- substituir os dados;
- persistir preferência global;
- vazar para outro `console`;
- alterar a identidade do cenário.

Ao recarregar a tela ou trocar de cenário, o modo inicial volta a ser determinado pela configuração declarativa carregada.

---

## 25. Modo inicial

O modo inicial é determinado pela política de modo de apresentação declarada pela tela (D23).

- **Telas de modo único** iniciam necessariamente em seu único modo — verboso para telas somente verbosas, não verboso para telas somente não verbosas.

- **Telas alternáveis** devem declarar o modo inicial. O modo inicial pode ser verboso ou não verboso. A obrigação de declarar existe; o nome concreto do campo e os valores aceitos no schema ficam adiados conforme §43.

A pergunta "como uma tela alternável inicia?" não é mais uma lacuna aberta: a resposta é obrigatoriamente declarada pela própria tela.

Ao recarregar a tela ou trocar de cenário, o modo inicial volta a ser determinado pela política declarada carregada.

Esta obrigação aplica-se a telas novas ou revisadas conforme o escopo de D23. Telas legadas — criadas antes da incorporação de D23 — não precisam declarar modo inicial até futura decisão de migração.

---

## 26. Espaçamentos

O sistema de apresentação multinível no `console` deve admitir as seguintes categorias de medidas espaciais.

**Medidas externas:** margem superior, inferior, esquerda e direita.

**Medidas hierárquicas:** recuo entre níveis; largura reservada para designador; espaço entre designador e conteúdo; espaço entre nós irmãos; espaço entre níveis; espaço entre grupos; espaço entre subconjuntos.

**Medidas nome–valor:** largura reservada para nome; espaço antes do separador; espaço depois do separador; espaço adicional antes do valor; coluna inicial do valor.

**Medidas de tabela:** largura de coluna; espaço entre colunas; espaço entre linhas; preenchimentos internos; espaço entre cabeçalho e corpo.

**Medidas de continuação:** coluna ou recuo da continuação; espaço entre linhas do mesmo conteúdo; quantidade máxima de linhas.

Medidas mínimas, margens, recuos, vãos e preenchimentos não devem ser negativos. Medidas horizontais são em espaços; medidas verticais são em linhas.

O bloco de espaçamentos deve conter apenas medidas espaciais e não deve misturar regras de origem dos dados.

---

## 27. Alinhamentos

O bloco de alinhamentos deve declarar alinhamentos, justificações e seus escopos.

Todos os cálculos devem usar a área útil, depois de descontados elementos externos ao conteúdo.

**Alinhamento do designador:** natural ou justificado. Toda justificação deve declarar seu escopo.

**Escopos de alinhamento possíveis:**

```text
irmãos
grupo
nível
página
conteúdo completo
```

**Alinhamento de continuação:** as linhas de continuação devem começar na coluna calculada conforme a apresentação.

Larguras e alinhamentos calculados não devem variar entre páginas, salvo quando o escopo declarar por página.

---

## 28. Quebra de palavras

O modo verboso deve declarar uma política para palavras maiores que a largura disponível:

```text
quebrar palavra
truncar palavra
mover palavra inteira para a próxima linha
declarar impossibilidade
```

Recomenda-se: quebrar preferencialmente em espaços; mover a palavra inteira para a linha seguinte quando ela couber; quebrar a palavra apenas quando ela for maior que toda a largura útil.

Marcadores de truncamento ou continuação devem ser considerados no cálculo da largura útil.

A ADR não decide o comportamento padrão desta política; ele fica adiado conforme §43.

---

## 29. Limites de linhas

Qualquer conteúdo verboso pode declarar quantidade máxima de linhas físicas.

Quando o limite for atingido e ainda houver conteúdo, a última linha permitida deve aplicar a política final declarada.

Modo verboso com limite de uma linha não deve ser tratado automaticamente como modo não verboso.

---

## 30. Paginação e contexto

O JSON declara políticas de paginação. O renderizador produz os resultados físicos.

O renderizador deve calcular: capacidade, quantidade de páginas, posição das quebras, repetição de cabeçalhos, repetição visual de ancestrais, blocos que cabem integralmente e recuperação após redimensionamento.

### 30.1 Por modo de apresentação

- **Tabela**: o cabeçalho deve ser repetido em cada página;
- **Hierarquia**: ancestrais devem ser repetidos ou indicados quando a página começar no interior de um ramo;
- **Conjuntos**: o título do conjunto e, quando aplicável, do subconjunto devem ser repetidos quando seus campos continuarem em nova página.

### 30.2 Contexto repetido

Um filho não deve aparecer no início de uma nova página sem contexto suficiente para identificar seus ancestrais.

Ancestrais repetidos são contexto visual e não devem: alterar a numeração, duplicar dados, reiniciar contagens ou ser tratados como novos nós.

### 30.3 Indicador de continuação

O indicador de continuação deve ser configurável. Exemplo:

```text
1. Conjunto 1: [continuação]
    1.2 Subconjunto 1.2: [continuação]
        a. Elemento 4: valor
```

### 30.4 Paginação não corrige largura

Paginação não resolve impossibilidade horizontal. Ver §32.

---

## 31. Blocos indivisíveis

A configuração deve poder declarar como indivisíveis: título do conjunto e primeiro filho; título do subconjunto e primeiro filho; linha nome–valor; nó e suas linhas de continuação; linha lógica de tabela.

Um título não deve permanecer sozinho no final da página quando houver exigência de mantê-lo com pelo menos um filho.

Quando um bloco indivisível for maior que uma página vazia, a configuração deve definir: permitir divisão excepcional; truncar; ou declarar impossibilidade.

---

## 32. Impossibilidade geométrica

O renderizador deve calcular a largura mínima e a altura mínima necessárias para cada modo de apresentação, considerando todos os componentes obrigatórios.

Paginação não resolve impossibilidade horizontal. Quando nem a unidade mínima de conteúdo multinível couber na largura útil da área disponível, o renderizador deve acionar a política de impossibilidade.

A configuração geral deve definir como tratar impossibilidade geométrica:

```text
quadro mínimo
fallback
mensagem de erro
rejeição da renderização
```

As ADRs vigentes do projeto (ADR-0017 e ADR-0023) já estabelecem políticas de quadro mínimo para a TUI. Esta ADR não cria política nova de impossibilidade; relaciona a regra do contrato às autoridades já existentes.

Se existir lacuna entre o contrato e as autoridades vigentes sobre o tratamento de impossibilidade para conteúdo multinível, essa lacuna será tratada na aplicação documental, sem invenção de política nova por esta ADR.

---

## 33. Validações

O loader ou camada equivalente deve rejeitar ao menos as seguintes configurações inválidas:

| Código | Condição | Status |
|---|---|---|
| V-01 | Tabela sem cabeçalho | INVÁLIDO |
| V-02 | Referência a nível filho inexistente | INVÁLIDO |
| V-03 | Múltiplas raízes | INVÁLIDO |
| V-04 | Folha que declara filhos | INVÁLIDO |
| V-05 | Contêiner sem nível filho declarado | INVÁLIDO |
| V-06 | Campo nome–valor sem origem do valor | INVÁLIDO |
| V-07 | Medidas negativas (margens, recuos, vãos, preenchimentos) | INVÁLIDO |
| V-08 | Largura máxima inferior à mínima | INVÁLIDO |
| V-09 | Modo não verboso configurado para mais de uma linha | INVÁLIDO |
| V-10 | Modo verboso sem regra de alinhamento da continuação | INVÁLIDO |
| V-11 | Justificação sem escopo | INVÁLIDO |
| V-12 | Designador composto que depende de ancestral inexistente | INVÁLIDO |
| V-13 | Dados incompatíveis com a estrutura declarada | INVÁLIDO |
| V-14 | Coluna de tabela sem nível ou campo de origem | INVÁLIDO |
| V-15 | Condição excepcional possível sem política explícita declarada | INVÁLIDO |

As validações V-01 a V-15 complementam as 20 validações da ADR-0027 (D13). As validações desta seção derivam do contrato externo (R-146 a R-160).

---

## 34. Diferenças terminológicas

O contrato externo e o schema atual do projeto usam termos diferentes para conceitos equivalentes.

| Conceito normativo | Contrato externo | Schema atual do projeto (ADR-0027) |
|---|---|---|
| Tipo de nível — folha, conteúdo exibível | `folha` | `conteudo` |
| Tipo de nível — par nome e valor | `campo` | `nome_valor` |
| Apresentação hierárquica com recuo | `hierarquia_indentada` | `hierarquia` |
| Bloco de estrutura da hierarquia | `estrutura` | `formato.niveis` e campos do envelope |
| Bloco de estilos de designador | `estilos_designadores` | `formato.niveis[].designador` |
| Modo de apresentação | `apresentacao` (bloco separado) | `formato.apresentacao` |
| Espaçamentos | `espacamentos` (bloco separado) | `formato.espacamento` |
| Alinhamentos | `alinhamentos` (bloco separado) | `formato.alinhamento` |
| Excesso | `excesso` (bloco separado) | `formato.excesso` |
| Paginação | `paginacao` (bloco separado) | `formato.paginacao` |

Esta ADR:

1. registra as diferenças materiais;
2. distingue conceito normativo de nome concreto do schema;
3. não renomeia propriedades ou valores existentes;
4. não declara migração sem decisão explícita;
5. não escolhe entre os nomes do contrato e os nomes do schema atual.

O desenho concreto do schema — incluindo nomes definitivos das propriedades — é adiado conforme §43.

### Diferença adicional: `modo normal` e `modo não verboso`

O `contrato_console.md` (§6) utiliza o termo **`modo normal`** para o modo operacional de exibição do console sem quebra de linha, declarando-o como o default da instância. A ADR-0028 utiliza o termo **`modo não verboso`** (§§21–22, D9) para o mesmo comportamento conceitual aplicado às apresentações de conteúdo multinível no `console`.

Os dois termos descrevem o mesmo comportamento: exibição de cada conteúdo aplicável em uma única linha física, com truncamento do excedente. Esta equivalência conceitual é registrada aqui para que a futura aplicação documental possa reconciliar explicitamente os termos, sem que nenhum deles seja silenciosamente renomeado ou declarado como já substituído.

A reconciliação terminológica definitiva — incluindo qual dos termos será adotado como nome concreto no schema — é adiada para a futura aplicação documental. O registro desta diferença não constitui decisão de valor padrão para o modo inicial, que permanece adiado conforme §43 item 3 desta ADR e §43 item 3 do contrato externo.

---

## 35. Responsabilidades das camadas

### 35.1 Ponto de entrada

O ponto de entrada (`orquestrador` ou `demo`) é responsável por:

1. identificar a tela escolhida;
2. carregar o JSON estrutural da tela;
3. carregar separadamente o documento JSON de conteúdo multinível;
4. entregar os dois documentos conjuntamente ao fluxo interno, mantendo-os como entradas distintas sem incorporação do conteúdo externo ao JSON estrutural da tela;
5. não copiar o conteúdo externo para dentro do JSON estrutural.

### 35.2 Loader ou camada equivalente

O loader é responsável por: validar o documento externo conforme as regras da §33; converter os documentos; produzir representação interna.

O loader não abre arquivos por conta própria. Os arquivos são entregues pelo ponto de entrada.

### 35.3 Modelo

O modelo é responsável por: transportar o conteúdo semântico sem lógica geométrica; não descobrir sozinho qual arquivo carregar; não reconstruir hierarquia a partir de dados não normalizados.

### 35.4 Renderizador

O renderizador é responsável pelos resultados físicos calculados. Ele não abre arquivos.

Resultados calculados exclusivamente pelo renderizador:

```text
área útil
larguras efetivas
alturas efetivas
recuos acumulados
larguras reservadas
colunas iniciais
linhas físicas
quebras
truncamentos aplicados
páginas
repetição visual de cabeçalhos
repetição visual de ancestrais
posições finais
impossibilidade geométrica
recuperação após redimensionamento
```

---

## 36. Demonstrações obrigatórias

A futura implementação deve possuir uma demonstração permanente e repetível para cada cenário:

1. tabela multinível;
2. hierarquia indentada;
3. conjunto com campos nome–valor (dois níveis);
4. conjunto, subconjunto e campos nome–valor (três níveis).

Cada cenário deve possuir:

- tela estrutural identificável;
- conteúdo JSON externo identificado;
- associação permanente entre tela e conteúdo;
- ponto de entrada real (`demo.py` ou equivalente);
- comando exato de abertura;
- identidade semântica verificável.

Para telas alternáveis, cada cenário deve permitir observar os mesmos dados nos modos verboso e não verboso, com o mesmo JSON estrutural e o mesmo documento de conteúdo. Telas de modo único não precisam permitir alternância.

### 36.2 Cenários futuros mínimos por política de modo

As demonstrações futuras devem incluir ao menos os seguintes quatro cenários mínimos, cobrindo as três políticas de modo:

1. **Tela somente não verbosa** — com conteúdo que produza truncamento por `...`; sem chip `[V] Verboso`; sem alternância por `V`;

2. **Tela somente verbosa** — com conteúdo de dois níveis exibido em várias linhas físicas; sem chip `[V] Verboso`; sem alternância por `V`;

3. **Tela alternável de três níveis** — iniciando em modo não verboso; com chip `[V] Verboso`; alternância para modo verboso pela tecla `V`; conteúdo no formato:

```text
1. valor
  1.1 valor
      1.1.1 texto
```

4. **Tabela alternável** — iniciando em modo verboso; com chip `[V] Verboso`; com possibilidade de alternância para modo não verboso pela tecla `V`.

### 36.3 Alinhamento no cenário de dois níveis em modo verboso

No cenário de tela somente verbosa com conteúdo de dois níveis (cenário 2 de §36.2), a largura de referência para alinhamento deve ser calculada considerando todos os textos identificadores do primeiro nível pertencentes ao conteúdo lógico completo do cenário.

A maior largura encontrada entre esses textos determina a coluna comum a partir da qual o conteúdo do segundo nível deve iniciar. Essa coluna deve permanecer estável entre páginas: paginação e repetição visual de contexto não alteram o resultado da medição. As linhas de continuação do conteúdo do segundo nível devem permanecer alinhadas à mesma coluna inicial.

A medição usa o escopo `conteúdo completo` definido em §27, restrito ao conteúdo lógico do cenário. Ela não estabelece largura fixa global para outras telas ou outros cenários.

---

## 37. Testes futuros

A futura implementação deve possuir testes que provem semanticamente:

1. qual tela foi aberta;
2. qual JSON externo foi associado;
3. qual apresentação foi selecionada;
4. qual era o modo inicial;
5. que `V` alterou efetivamente o modo;
6. que uma segunda ativação de `V` restaurou o modo anterior;
7. que os dados não mudaram durante a alternância;
8. que a troca não vazou para outra tela;
9. que o comportamento se recupera após redimensionamento.

**Código de saída zero não é prova suficiente** de que a tela, o conteúdo ou o modo correto foi selecionado.

---

## 38. Validação manual em TTY real

A futura implementação deve incluir: fixtures permanentes; telas permanentes; ponto de entrada real; comandos exatos de abertura; identidade semântica observável; validação humana em TTY real.

---

## 39. Compatibilidade

Esta ADR é compatível com e não altera:

| Autoridade | Preservação |
|---|---|
| ADR-0026 | Separação entre JSON estrutural e documento externo de conteúdo preservada e estendida. Nenhuma decisão da ADR-0026 é reescrita. Esta ADR não substitui a ADR-0026. |
| ADR-0027 | Carregamento separado, entrega conjunta, schema semântico multinível e 20 validações mínimas continuam vigentes. Esta ADR não substitui a ADR-0027. |
| H-0036 | As três apresentações multinível implementadas (`tabela`, `hierarquia`, `conjuntos_campos`) e suas fixtures permanecem válidas. O ciclo H-0036 pré-data a incorporação de D23; suas telas não declaram política de modo e não devem ser reinterpretadas automaticamente como uma das três políticas. Migração futura permanece adiada conforme §43 item 3. |
| ADR-0025 / H-0035 | Distribuição matricial de nível único permanece inalterada. Esta ADR não afeta essa capacidade. |
| Responsabilidade geométrica do renderizador | Geometria, quebras, truncamentos, alinhamentos, paginação e posições continuam sob responsabilidade exclusiva do renderizador. |
| Console sem conteúdo externo | Preserva o comportamento histórico. Nenhuma migração automática. |

**Conflitos encontrados:** nenhum conflito material foi identificado entre as autoridades lidas e as decisões desta ADR.

---

## 40. Consequências

### 40.1 Consequências positivas

- base normativa completa para as apresentações multinível do `console`;
- definição dos tipos conceituais (contêiner, folha, campo) e suas regras;
- formalização de designadores, espaçamentos, alinhamentos, excesso, paginação, blocos indivisíveis, impossibilidade e validações;
- semântica definida para alternância verboso/não verboso nas apresentações multinível;
- estado de visualização explicitamente separado da persistência;
- quatro cenários de demonstração obrigatórios definidos;
- critérios de teste semântico definidos.

### 40.2 Custos e riscos

- a implementação de quatro demonstrações e das regras normativas completas exige ciclo dedicado;
- diferenças terminológicas entre o contrato externo e o schema atual do projeto precisarão ser reconciliadas em etapa futura;
- a ausência de aplicação documental deixa as regras desta ADR como referência normativa ainda não propagada.

---

## 41. Documentos afetados

Documentos a atualizar em etapa futura, sem alteração nesta etapa:

| Documento | Motivo |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0028 após QA e aplicação documental autorizada. |
| `docs/NOMENCLATURA.md` | Formalizar: estado de visualização, alternância por V, modo inicial, modos verboso e não verboso, tipos de nível conceituais e diferenças terminológicas. |
| `docs/contratos/contrato_json_console.md` | Propagar as regras normativas do conteúdo multinível, os cenários de apresentação, o bloco de excesso, o modo inicial e a semântica da tecla V. |
| `docs/contratos/contrato_console.md` | Registrar estado de visualização da sessão, alternância por V e não persistência da alternância. |
| `docs/contratos/contrato_barra_de_menus.md` | Avaliar se a definição da ação `[V] Verboso` nas demonstrações de dados do `console` (§23) requer atualização deste contrato. A ação `[V]` pode já estar parcialmente coberta pela seção 14 do `contrato_console.md`; a aplicação documental decidirá se alteração deste contrato é necessária. |
| `docs/contratos/contrato_tela_json.md` | Confirmar que o JSON estrutural não incorpora conteúdo nem modo de visualização. |
| `docs/contratos/contrato_composicao_corpo.md` | Avaliar impacto das demonstrações permanentes. |
| `config/telas/demo/` | Criação das telas de demonstração permanentes dos quatro cenários multinível. |
| `config/` ou localização equivalente | Criação das fixtures permanentes dos JSONs de conteúdo para os quatro cenários, seguindo a organização existente do repositório. |
| `demo/demo.py` | Registro dos quatro cenários multinível no catálogo ou mecanismo de associação. |

---

## 42. Escopo negativo

Esta ADR não decide nem autoriza:

- conteúdo matricial (`tipo: matriz`);
- mudança em `dashboard` ou `lancador`;
- mudança em componentes que não sejam `console`;
- implementação de qualquer funcionalidade;
- alteração dos JSONs existentes;
- criação das telas de demonstração;
- alteração da barra de menus;
- alteração de loader, modelo ou renderizador;
- navegação interativa entre nós;
- expansão e recolhimento de hierarquia;
- edição dos dados;
- persistência do modo além da sessão;
- integração concreta com o projeto Pipeline;
- protocolo de transporte entre projetos;
- cache;
- autenticação;
- atualização automática;
- renomeação de propriedades do schema atual;
- mudança de teclas diferente de `V`;
- commit ou push;
- QA desta ADR;
- aplicação documental desta ADR;
- criação de handoff.

---

## 43. Decisões adiadas

As seguintes decisões não foram tomadas por esta ADR nem pelo contrato externo, e devem ser tratadas em etapas futuras:

1. nomes definitivos das propriedades do JSON de conteúdo multinível;
2. versão inicial do schema;
3. nomes concretos dos campos para declaração da política de modo de apresentação da tela e do modo inicial em telas alternáveis (conceito decidido em D23 e §25; mecanismo concreto de schema adiado); estratégia de migração das telas legadas e eventual representação de compatibilidade no loader (para telas novas ou revisadas, política ausente é inválida e default implícito é proibido; para telas legadas, política ausente é compatibilidade preservada e interpretação automática é proibida);
4. marcador padrão de truncamento;
5. estilos de designador obrigatórios no schema;
6. limites máximos de profundidade;
7. política global de fallback visual para impossibilidade no conteúdo multinível;
8. estratégia concreta de navegação entre páginas;
9. formato de mensagens de validação;
10. protocolo de integração com o Pipeline;
11. comando, repositório e localização do script do Pipeline;
12. transporte do JSON produzido pelo Pipeline;
13. persistência intermediária;
14. timeout;
15. tratamento de falha ou indisponibilidade do Pipeline.

---

## 44. Critérios para futura aplicação documental

A aplicação documental desta ADR deverá, no mínimo:

- propagar as regras normativas do conteúdo multinível nos contratos afetados;
- formalizar a política de modo de apresentação da tela (somente verbosa, somente não verbosa, alternável) e o modo inicial em telas alternáveis;
- distinguir explicitamente telas novas ou revisadas — que exigem declaração de política — de telas legadas que permanecem válidas sem declaração;
- formalizar a semântica da tecla `V` e o estado de visualização da sessão;
- confirmar que o JSON externo não contém resultados calculados;
- registrar a não persistência da alternância;
- propagar as regras específicas de tabela, hierarquia e conjuntos nos contratos;
- propagar as validações da §33;
- registrar as diferenças terminológicas entre o contrato e o schema atual;
- atualizar o índice de ADRs;
- identificar nominalmente todos os documentos afetados;
- não alterar nenhum código.

---

## 45. Critérios para futuro handoff

O handoff que implementar esta ADR deverá:

- criar ou atualizar as fixtures permanentes para os quatro cenários multinível;
- criar as telas de demonstração permanentes;
- integrar os quatro cenários ao ponto de entrada real;
- implementar as três políticas de modo de apresentação (somente verbosa, somente não verbosa, alternável) conforme declarado por cada tela nova ou revisada;
- respeitar a distinção entre telas novas ou revisadas com política declarada e telas legadas sem declaração — telas legadas não recebem política por inferência;
- implementar a tecla `V` e o chip `[V] Verboso` na barra de menus exclusivamente em telas alternáveis;
- implementar a alternância de modo sem troca de tela;
- implementar a inicialização do modo a partir da política declarada pela tela;
- implementar a recuperação do modo inicial ao trocar de tela;
- garantir que a alternância não reescreve o JSON externo;
- criar testes semânticos conforme §37;
- incluir validação humana em TTY real conforme §38;
- reconciliar diferenças terminológicas conforme decisão da etapa de schema.

---

## 46. Verificações de integridade

| # | Verificação | Resultado |
|---|---|---|
| 1 | Autoridade incorreta removida | Confirmado — `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md` não é mais autoridade; `CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` adotado (§3.3) |
| 2 | Sem regras matriciais | Confirmado — `tipo: matriz` removido de todas as seções; conteúdo matricial listado no escopo negativo (§42) |
| 3 | Escopo limitado ao console com conteúdo multinível | Confirmado — §6 |
| 4 | Origem atual em arquivo JSON registrada | Confirmado — §7 |
| 5 | Origem futura por script do Pipeline registrada | Confirmado — §8 |
| 6 | Protocolo com Pipeline não inventado | Confirmado — §8, §42, §43 itens 10–15 |
| 7 | Fronteira semântica em JSON preservada | Confirmado — §9 |
| 8 | Quatro cenários de demonstração explícitos | Confirmado — D8, §36 |
| 9 | Modos verboso e não verboso definidos | Confirmado — §21, §22 |
| 10 | Tecla `V` definida como alternância da sessão | Confirmado — §23, §24 |
| 11 | Alternância não altera dados ou arquivos | Confirmado — §24 |
| 12 | Responsabilidades das camadas separadas | Confirmado — §35 |
| 13 | Paginação e contexto contemplados | Confirmado — §30, §31 |
| 14 | Impossibilidades geométricas contempladas | Confirmado — §32 |
| 15 | Validações do contrato contempladas | Confirmado — §33 (V-01 a V-15) |
| 16 | Decisões adiadas não preenchidas | Confirmado — §43 |
| 17 | Diferenças terminológicas não resolvidas por invenção | Confirmado — §34 |
| 18 | Somente a ADR-0028 foi alterada | Confirmado |
| 19 | Política de modo de apresentação declarada pela tela (D23) | Confirmado — três classes: somente verbosa, somente não verbosa, alternável |
| 20 | Modo não verboso como escolha declarativa da tela | Confirmado — D23 classe b), §25 |
| 21 | Telas de modo único e telas alternáveis distintas | Confirmado — D23, D11, D12, §23, §25 |
| 22 | Telas alternáveis exigem modo inicial declarado | Confirmado — D12, D23 classe c), §25 |
| 23 | Chip [V] Verboso vinculado a telas alternáveis | Confirmado — D23 classe c), §23 |
| 24 | Quatro cenários futuros mínimos registrados | Confirmado — §36.2 |
| 25 | Alinhamento de dois níveis em modo verboso registrado | Confirmado — §36.3 |
| 26 | Decisões adiadas atualizadas (item 3) | Confirmado — §43 |
| 27 | Escopo da medição de alinhamento em §36.3 definido como conteúdo lógico completo do cenário | Confirmado — §36.3 |
| 28 | Coluna do segundo nível estável entre páginas — paginação não altera a medição | Confirmado — §36.3 |
| 29 | Linhas de continuação do segundo nível alinhadas à mesma coluna inicial | Confirmado — §36.3 |
| 30 | D23 distingue telas novas ou revisadas (política obrigatória) de telas legadas (compatibilidade preservada) | Confirmado — D23, §25, §39, §43 item 3 |
| 31 | Telas legadas permanecem válidas sem declaração de política | Confirmado — D23, §39 |
| 32 | Telas legadas não são reinterpretadas automaticamente como uma das três políticas | Confirmado — D23, §39 |
| 33 | Migração de telas legadas permanece adiada | Confirmado — §43 item 3 |
| 34 | Ausência de política é inválida somente para telas novas ou revisadas; default implícito é proibido | Confirmado — D23, §43 item 3 |

---

## 47. Histórico de alterações

| Data | Alteração |
|---|---|
| 2026-07-17 | Correção pós-QA (PATCH_ADR): reconciliação terminológica entre carregamento separado e entrega conjunta em D3 e §35.1; remoção do qualificador indevido de V-05; registro terminológico de `modo normal` e `modo não verboso` em §34; inclusão de `docs/contratos/contrato_barra_de_menus.md` entre os documentos afetados no frontmatter e em §41. |
| 2026-07-17 | Aplicação documental (APLICAR_ADR): status atualizado para `aceita e aplicada`; decisões D1–D22 propagadas para `docs/adr/INDICE_ADR.md` (nova entrada ADR-0028), `docs/NOMENCLATURA.md` (seção 19), `docs/contratos/contrato_json_console.md` (seção 13), `docs/contratos/contrato_console.md` (seção 21), `docs/contratos/contrato_tela_json.md` (seção 33), `docs/contratos/contrato_composicao_corpo.md` (seção 12) e `docs/contratos/contrato_barra_de_menus.md` (seção 22). Relatório: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md`. |
| 2026-07-17 | Correção pós-bloqueio H-0037 (PATCH_ADR): incorporação da decisão do usuário sobre política de modo de apresentação da tela. Adicionada D23 (política de modo: somente verbosa / somente não verbosa / alternável). D11 restringida a telas alternáveis. D12 reescrita: telas de modo único iniciam em seu único modo; telas alternáveis devem declarar modo inicial (não mais lacuna aberta). §23 atualizado: chip [V] Verboso vinculado exclusivamente a telas alternáveis. §25 reescrito: modo inicial determinado pela política da tela, sem comportamento indefinido. §36.2 e §36.3 adicionados: quatro cenários futuros mínimos e regra de alinhamento de dois níveis em modo verboso. §43 item 3 atualizado: conceito decidido em D23/§25; schema concreto adiado. §44, §45, §46 atualizados. |
| 2026-07-17 | Correção pós-QA da revisão de modos por tela (PATCH_ADR): (1) §36.3 — definição do escopo de medição de alinhamento no cenário verboso de dois níveis: conteúdo lógico completo do cenário, coluna comum estável entre páginas, continuação do segundo nível alinhada à mesma coluna inicial, sem largura fixa global (QA-MODOS-001); (2) D23, §25, §39 e §43 item 3 — distinção explícita entre telas novas ou revisadas (política obrigatória, ausência inválida, default implícito proibido) e telas legadas (compatibilidade preservada, reinterpretação automática proibida, migração adiada); §44 e §45 atualizados com critério de distinção; §46 atualizado com verificações 27–34 (QA-MODOS-002). A aplicação documental anterior (D1–D22) precisará ser revisada para incorporar D23 quando a ADR for aprovada. |
| 2026-07-18 | Aplicação documental da revisão D23 (APLICAR_ADR — segunda aplicação): D23 propagada para todos os contratos afetados. Campos canônicos definidos: `formato.excesso.politica_modo` e `formato.excesso.modo_inicial` no JSON estrutural da tela (elemento `console`). Contratos atualizados: `contrato_json_console.md` (§13.11 corrigido; §13.13 adicionado com localização, tipos, valores, matriz de validade, quatro exemplos válidos, exemplos inválidos, proibições, campo legado, compatibilidade, separação estrutural/externo e cenários futuros); `contrato_console.md` (§21.4 atualizado; §21.5 corrigido — chip restrito a alternáveis; §21.7 corrigido — política em JSON estrutural, não no documento externo; §21.11 adicionado — três políticas); `contrato_barra_de_menus.md` (§22.1 corrigido — política `"alternavel"` como condição do chip; §22.3 corrigido — modo inicial da política estrutural; §22.8 adicionado — tabela de chip por política); `contrato_tela_json.md` (§33.2 corrigido — distinção política/estado; §33.6 adicionado — declaração de política no JSON estrutural); `contrato_composicao_corpo.md` (§12.8 adicionado — delegação de política ao console); `NOMENCLATURA.md` (§19.6 atualizado — item de migração legada adicionado; §19.7 adicionado — termos D23: política de modo, somente verbosa, somente não verbosa, alternável, modo inicial D23, tela legada); `INDICE_ADR.md` (entrada ADR-0028 atualizada com D23 e segunda aplicação). Relatório: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`. |
