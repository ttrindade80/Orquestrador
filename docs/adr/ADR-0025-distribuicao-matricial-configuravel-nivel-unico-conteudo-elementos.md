---
name: ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos
description: Define a capacidade genérica de distribuição matricial configurável de nível único para o conteúdo de elementos — formação, ordem, dimensionamento, margens, espaços, distribuição do espaço excedente, alinhamento, fallback e determinismo; não define valores concretos, schema JSON final, paginação nem distribuição multinível
metadata:
  type: adr
  status: aceita e aplicada
  data: "2026-07-16"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_lancador.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0025 — Distribuição matricial configurável de nível único do conteúdo dos elementos

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0025 |
| Título | Distribuição matricial configurável de nível único do conteúdo dos elementos |
| Status | aceita e aplicada |
| Data | 2026-07-16 |
| Origem | Decisão explícita do usuário |

---

## 2. Status

`aceita e aplicada`

---

## 3. Contexto

Os contratos e ADRs anteriores formalizaram a composição hierárquica do corpo
como árvore de composição (ADR-0015), a distribuição de área entre filhos
diretos de um container (ADR-0015, ADR-0018), a especialização bidimensional do
nó `grupo` com coordenadas explícitas de células (ADR-0020), a proibição de
preenchimento vazio externo do corpo (ADR-0024), e a largura mínima funcional do
`lancador` (ADR-0023).

O sistema dispõe de mecanismos de composição estrutural do corpo (arranjo de
grupos, distribuição de área entre filhos diretos), mas não define ainda uma
capacidade genérica de organização interna do conteúdo de um elemento. Cada
elemento (dashboard, console, lancador) possui regras parciais registradas em
contratos específicos — vãos elásticos do `lancador` (ADR-0003), algoritmo de
matriz do `lancador` (ADR-0001, seção 8.3 da NOMENCLATURA), alinhamento do
`dashboard` (pendente de confirmação, seção 11 da NOMENCLATURA) — mas essas
regras são elementos isolados, não uma capacidade unificada e configurável por
qualquer tipo de elemento.

A capacidade de distribuição matricial configurável de nível único é distinta
da composição hierárquica do corpo (ADR-0015) e da especialização bidimensional
do nó `grupo` (ADR-0020): ela opera dentro de um elemento já posicionado na
árvore de composição, distribuindo os participantes imediatos daquele elemento
dentro da área útil que lhe foi alocada.

---

## 4. Problema

O renderizador precisa ser capaz de modelar o conteúdo de um elemento como um
conjunto ordenado de participantes distribuídos dentro de uma área matricial.

Essa distribuição deve poder controlar:

- formação por linhas;
- formação por colunas;
- matriz fixa;
- ordem de preenchimento;
- dimensões mínimas;
- margens;
- espaços entre participantes;
- distribuição do espaço excedente;
- alinhamento horizontal;
- alinhamento vertical;
- centralização;
- limites mínimos e máximos;
- comportamento determinístico quando a área disponível muda.

Esses comportamentos não devem ser fixados diretamente no código para um
elemento específico. Os valores concretos devem ser declarados na configuração
JSON do elemento responsável por organizar o conteúdo daquele nível.

---

## 5. Decisão

O renderizador deverá oferecer uma **capacidade genérica de distribuição
matricial configurável de nível único**.

A mesma capacidade poderá ser utilizada, conforme seus contratos específicos,
pelo conteúdo de:

- `dashboard`;
- `console`;
- `lancador`;
- outros tipos de elemento que venham a adotar explicitamente essa capacidade.

Esta ADR define:

- a semântica da formação;
- a semântica da ordem de preenchimento;
- a semântica do dimensionamento;
- a semântica das margens e dos espaços entre participantes;
- a semântica da distribuição do espaço excedente;
- a semântica do alinhamento;
- a semântica do fallback por impossibilidade geométrica;
- as obrigações de determinismo;
- os requisitos para os contratos JSON posteriores.

Esta ADR **não** define:

- valores concretos de um elemento ou tela;
- nomes finais dos campos JSON;
- organização sintática final do schema;
- nomes das telas de teste;
- nomes dos arquivos JSON de teste;
- nome final do demo dedicado;
- implementação do renderizador.

---

## 6. Objetivo

Definir a semântica normativa da distribuição matricial configurável de nível
único, de modo que:

1. qualquer elemento que adote explicitamente essa capacidade possa declarar
   suas políticas concretas no JSON da instância;
2. o renderizador calcule a geometria de forma determinística a partir da
   declaração;
3. nenhuma tela existente mude de layout sem adoção explícita;
4. a capacidade seja compatível com futura composição multinível sem exigi-la
   agora;
5. os contratos JSON e os handoffs futuros tenham critérios suficientes para
   definir schema, validações e implementação.

---

## 7. Escopo de nível único

Esta ADR define exclusivamente a distribuição matricial de **nível único**.

**Nível único** é a organização de um conjunto ordenado de participantes
pertencentes à mesma área de distribuição de um elemento.

Nesse nível, o renderizador calcula somente:

- a formação da matriz;
- a posição dos participantes imediatos;
- as margens externas daquele nível;
- os espaços entre os participantes daquele nível;
- as dimensões das linhas e colunas daquele nível;
- a distribuição da sobra daquele nível;
- o alinhamento dos participantes daquele nível.

A configuração pertence ao elemento ou contêiner que organiza diretamente esse
conjunto.

**Exemplos conceituais:**

```text
dashboard
└── configuração da distribuição de seus participantes imediatos

console
└── configuração da distribuição de seus participantes imediatos

lancador
└── configuração da distribuição de seus itens imediatos
```

---

## 8. Limites do nível único

A implementação futura desta ADR **não deverá**:

- achatar participantes pertencentes a níveis diferentes em uma única matriz;
- percorrer descendentes e reorganizá-los implicitamente;
- aplicar recursivamente a configuração aos filhos;
- herdar parâmetros entre níveis;
- propagar automaticamente parâmetros do pai aos filhos;
- combinar margens de níveis diferentes;
- combinar espaços de níveis diferentes;
- tratar participantes internos como participantes diretos do nível externo;
- fazer cascata de configurações;
- redefinir a composição hierárquica já existente (ADR-0015, ADR-0019,
  ADR-0020).

Um participante do nível atual poderá futuramente conter outra distribuição
interna. No nível externo, esse participante continua sendo tratado como uma
única unidade.

**Exemplo conceitual:**

```text
nível 1

┌──────────────────────────────────┐
│ [A]                [B]           │
│                    ┌──────────┐  │
│                    │ B1 │ B2  │  │
│                    └──────────┘  │
└──────────────────────────────────┘
```

No nível 1:

- `A` é um participante;
- `B` é um participante;
- `B1` e `B2` não participam diretamente da matriz do nível 1.

A distribuição interna de `B` dependerá de uma decisão futura.

---

## 9. Compatibilidade com futura distribuição multinível

A solução de nível único não deve impedir uma futura composição multinível.

Entretanto, ficam **fora desta ADR**:

- semântica de distribuição multinível;
- recursão de layout;
- ordem de cálculo entre níveis;
- herança de configurações;
- cascata de parâmetros;
- interação entre margens internas e externas de níveis distintos;
- interação entre espaços de níveis distintos;
- propagação de dimensões mínimas entre níveis;
- propagação do fallback entre níveis;
- estrutura JSON específica para composição multinível;
- definição de como um erro interno de um participante afeta o nível externo.

Esses comportamentos exigirão decisão e ADR próprias.

Não devem ser inventadas regras multinível nesta ADR nem na implementação
futura que decorrer dela.

---

## 10. Itens multinível fora de escopo

São explicitamente excluídos desta ADR:

- distribuição multinível;
- recursão de layout;
- herança de configuração entre níveis;
- cascata de parâmetros entre níveis;
- interação geométrica entre margens de níveis distintos;
- interação geométrica entre espaços de níveis distintos;
- propagação de fallback entre níveis;
- propagação de dimensões mínimas entre níveis;
- estrutura JSON para composição multinível;
- regras de como erro em participante interno afeta nível externo.

---

## 11. Separação de responsabilidades

```text
ADR-0025
└── define capacidades, semântica e regras normativas

Contratos JSON (a serem atualizados em APLICAR_ADR)
└── definirão a estrutura declarativa e os campos aceitos

JSON do elemento (instância concreta)
└── escolherá as políticas e os valores concretos daquele nível

Loader e modelo
└── validarão e representarão a configuração declarada

Renderizador
└── interpretará a configuração e calculará a geometria

Telas de teste (a serem criadas em handoff futuro)
└── usarão valores concretos para cobrir combinações representativas

Demo dedicado (a ser criado em handoff futuro)
└── permitirá observar as telas sem ampliar excessivamente o demo principal
```

A decisão arquitetural desta ADR não deve ser confundida com a futura
construção das telas de demonstração.

---

## 12. Configuração no JSON do elemento

Os parâmetros de organização serão declarados no JSON do elemento que organiza
diretamente o conteúdo daquele nível.

A configuração deverá ser capaz de representar, conforme aplicável, os grupos
semânticos descritos nas seções seguintes desta ADR.

Os nomes finais dos campos não são definidos nesta ADR. Eles serão escolhidos
durante `APLICAR_ADR`, após verificação dos padrões documentais do projeto.

A estrutura sintática final será definida durante a aplicação da ADR aos
contratos JSON.

Nenhum default implícito introduzido por esta capacidade poderá alterar o
comportamento de elementos já configurados. A adoção é sempre explícita no JSON
do elemento.

---

## 13. Área útil

Todas as medidas deverão ser calculadas dentro da **área útil** disponível para
o conteúdo daquele elemento.

A área útil deverá ser determinada depois de descontados, quando existirem:

- bordas;
- títulos;
- cabeçalhos;
- barras;
- indicadores;
- padding estrutural;
- outros elementos que não participem da matriz daquele nível.

Esta ADR não redefine os contratos atuais de cálculo da área útil. Ela registra
que a aplicação documental (`APLICAR_ADR`) precisará reconciliar esta capacidade
com os contratos já existentes, em especial com `contrato_composicao_corpo.md`,
`contrato_lancador.md` e `contrato_tela_json.md`.

---

## 14. Eixos e unidades

As medidas verticais devem ser expressas em **linhas**.

As medidas horizontais devem ser expressas em **colunas ou espaços de terminal**.

**São medidas verticais:**

- margem superior;
- margem inferior;
- espaço entre linhas;
- altura das linhas;
- altura das células;
- altura dos participantes.

**São medidas horizontais:**

- margem esquerda;
- margem direita;
- espaço entre colunas;
- largura das colunas;
- largura das células;
- largura dos participantes.

---

## 15. Formação da matriz

A configuração deverá permitir declarar, no mínimo:

1. **formação com preferência por linhas** — organiza o conteúdo priorizando a
   ocupação ao longo das linhas, respeitando os limites declarados e a área
   disponível;
2. **formação com preferência por colunas** — organiza o conteúdo priorizando a
   ocupação ao longo das colunas, respeitando os limites declarados e a área
   disponível;
3. **matriz fixa obrigatória** — exige a quantidade declarada de linhas e
   colunas; se não couber respeitando todos os mínimos, não deve ser reduzida
   ou reorganizada silenciosamente.

A configuração deverá poder declarar, quando necessário:

- quantidade fixa de linhas;
- quantidade fixa de colunas;
- quantidade preferida de linhas;
- quantidade preferida de colunas;
- limite mínimo de linhas;
- limite máximo de linhas;
- limite mínimo de colunas;
- limite máximo de colunas;
- critérios determinísticos para escolha da formação válida;
- ordem completa de desempate.

Não deve existir formação estrutural implícita capaz de alterar silenciosamente
um elemento existente.

---

## 16. Ordem de preenchimento

A ordem de preenchimento é **independente** da formação.

A configuração deverá permitir, no mínimo:

### Preenchimento por linha

```text
[1] [2] [3]
[4] [5] [6]
```

### Preenchimento por coluna

```text
[1] [3] [5]
[2] [4] [6]
```

O renderizador deverá:

- preservar a ordem original do conjunto recebido;
- alterar somente a célula ocupada por cada posição;
- não reordenar semanticamente os participantes;
- não perder participantes;
- não duplicar participantes.

---

## 17. Independência das decisões

São decisões **independentes** entre si:

1. formação da matriz;
2. ordem de preenchimento;
3. dimensionamento das linhas;
4. dimensionamento das colunas;
5. distribuição horizontal;
6. distribuição vertical;
7. alinhamento horizontal interno;
8. alinhamento vertical interno;
9. tratamento da sobra;
10. fallback de impossibilidade geométrica.

Uma decisão não deve modificar implicitamente outra.

Os eixos horizontal e vertical deverão ser configuráveis separadamente.

**Exemplo válido de combinação:**

```text
formação = preferência por colunas
distribuição horizontal = centro
distribuição vertical = uniforme
ordem = por coluna
```

---

## 18. Distâncias fundamentais

A configuração deverá permitir representar independentemente:

1. margem superior;
2. margem inferior;
3. margem esquerda;
4. margem direita;
5. espaço horizontal entre colunas ou participantes;
6. espaço vertical entre linhas ou participantes.

Nenhuma dessas medidas deverá ser inferida de outra sem regra contratual
explícita.

---

## 19. Mínimos e máximos

Cada distância fundamental deverá possuir um **mínimo inteiro não negativo**.

Os mínimos são **invioláveis**. O renderizador não deverá reduzir um mínimo
para tentar fazer a formação caber.

Cada distância poderá possuir um **máximo opcional**.

Quando houver máximo:

- ele deverá ser maior ou igual ao mínimo correspondente;
- o renderizador não poderá ultrapassá-lo;
- a sobra não absorvida deverá seguir a próxima regra de distribuição configurada;
- o comportamento deverá permanecer determinístico.

Quando não houver máximo, a distância poderá crescer conforme a política
declarada e os limites do contrato aplicável.

---

## 20. Dimensionamento das linhas e colunas

A configuração deverá poder representar políticas de dimensionamento.

### Colunas

- largura baseada no maior participante da própria coluna;
- largura uniforme baseada no maior participante da matriz;
- largura mínima fixa;
- outra política futura explicitamente contratada.

### Linhas

- altura baseada no maior participante da própria linha;
- altura uniforme baseada no maior participante da matriz;
- altura mínima fixa;
- outra política futura explicitamente contratada.

O contrato JSON deverá declarar como tratar um participante que exija dimensão
maior que uma dimensão fixa. Não deve existir comportamento implícito.

As alternativas futuras poderão incluir: crescimento da linha ou coluna,
tratamento interno do participante, ou invalidação da formação. Esta ADR não
seleciona uma dessas alternativas sem decisão explícita adicional.

---

## 21. Cálculo da formação válida

Uma formação será **válida** somente quando respeitar simultaneamente:

- dimensões mínimas dos participantes;
- dimensões mínimas das linhas;
- dimensões mínimas das colunas;
- margens mínimas;
- espaços mínimos;
- limites de formação;
- largura disponível;
- altura disponível.

Uma formação com falta de espaço em qualquer eixo será **inválida**.

A distribuição do espaço excedente somente poderá ocorrer depois que uma
formação válida tiver sido escolhida.

---

## 22. Distribuição horizontal

A capacidade deverá permitir configurações que representem, no mínimo:

- alinhamento no início ou à esquerda;
- centralização horizontal;
- alinhamento no fim ou à direita;
- distribuição entre colunas;
- distribuição uniforme entre margens e espaços internos;
- distribuição com margens limitadas por mínimos e máximos e sobra restante
  destinada aos espaços entre os participantes.

A ADR distingue:

- **posição global da matriz** — onde a matriz toda se situa na área útil;
- **margens externas** — espaço entre a borda da área útil e o início da matriz;
- **espaços internos** — espaço entre colunas ou participantes dentro da
  matriz;
- **alinhamento do participante dentro da célula** — posição interna do
  participante na célula que lhe foi alocada.

Centralizar a matriz não implica centralizar cada participante dentro de sua
célula.

---

## 23. Distribuição vertical

A capacidade deverá permitir configurações que representem, no mínimo:

- alinhamento no início ou no topo;
- centralização vertical;
- alinhamento no fim ou na base;
- distribuição entre linhas;
- distribuição uniforme entre margens e espaços internos;
- distribuição com margens limitadas por mínimos e máximos e sobra restante
  destinada aos espaços entre as linhas.

A distribuição vertical deverá ser **independente** da distribuição horizontal.

---

## 24. Aplicação dos mínimos e distribuição da sobra

A seguinte sequência conceitual deve ser respeitada:

1. determinar a área útil;
2. validar a configuração;
3. obter as dimensões mínimas dos participantes;
4. construir ou enumerar as formações permitidas;
5. calcular a dimensão mínima de cada formação;
6. descartar formações inválidas;
7. selecionar uma formação válida por critérios determinísticos;
8. aplicar todos os mínimos;
9. calcular a sobra horizontal;
10. calcular a sobra vertical;
11. distribuir cada sobra segundo sua política própria;
12. respeitar os máximos;
13. distribuir restos inteiros;
14. calcular as coordenadas;
15. posicionar os participantes;
16. aplicar o alinhamento interno;
17. produzir o resultado renderizável.

Nenhuma etapa posterior poderá corrigir silenciosamente uma violação produzida
por uma etapa anterior.

---

## 25. Ordem de expansão

Quando margens ou espaços puderem crescer, a configuração deverá declarar uma
**ordem determinística de expansão**.

Uma política poderá, por exemplo:

- aplicar todos os mínimos; ampliar as margens até seus máximos; distribuir a
  sobra restante entre os participantes;

Outra política poderá:

- aplicar todos os mínimos; distribuir uniformemente a sobra entre margens e
  espaços internos;

Outra poderá:

- aplicar todos os mínimos; ampliar os espaços internos até seus máximos;
  ampliar as margens; enviar a sobra restante ao destino final do eixo.

Esta ADR define a capacidade de declarar essas políticas. Ela não impõe uma
única ordem global para todos os elementos. Os valores e a política concreta
serão escolhidos no JSON do elemento.

---

## 26. Distribuição inteira e restos

Todas as medidas finais deverão ser **inteiras**.

Quando uma divisão produzir resto, deverá existir uma **ordem determinística**
para distribuir as unidades residuais.

A ADR exige que:

- a política declare como os restos são distribuídos;
- o resultado seja estável;
- a mesma entrada produza o mesmo resultado;
- cardinalidade unitária não gere divisão por zero;
- políticas dependentes de múltiplos intervalos declarem comportamento para
  uma única linha ou coluna.

Os nomes finais dos campos para essas regras não são definidos nesta ADR.

---

## 27. Alinhamento dentro da célula

O alinhamento do participante dentro da célula é **independente** da
distribuição global da matriz.

A configuração deverá admitir, no mínimo:

### Alinhamento horizontal interno

- início;
- centro;
- fim.

### Alinhamento vertical interno

- topo;
- centro;
- base.

Quando uma centralização produzir resto ímpar, deverá existir uma regra
determinística. Os contratos JSON deverão documentar essa regra.

---

## 28. Determinismo

Para a mesma:

- configuração;
- sequência ordenada de participantes;
- área útil;
- dimensão mínima dos participantes;

o renderizador deverá produzir sempre:

- a mesma formação;
- a mesma quantidade de linhas;
- a mesma quantidade de colunas;
- as mesmas dimensões;
- as mesmas margens;
- os mesmos espaços;
- as mesmas coordenadas;
- a mesma ordem;
- a mesma distribuição de restos;
- o mesmo fallback.

Toda política capaz de produzir mais de um resultado válido deverá ter
**critérios completos de desempate**.

---

## 29. Terminal muito pequeno — fallback de impossibilidade geométrica

Quando nenhuma formação permitida conseguir acomodar todos os participantes e
todos os mínimos, o renderizador deverá apresentar o estado ou mensagem canônica
de:

```text
terminal muito pequeno
```

O nome técnico exato do estado deverá ser reconciliado com a nomenclatura e os
contratos ativos durante `APLICAR_ADR`, em especial com o termo `quadro mínimo
de terminal pequeno` já definido na ADR-0017 e com o fallback global do
`lancador` definido na ADR-0023.

Neste escopo, o renderizador **não deverá**:

- criar páginas;
- ocultar participantes;
- truncar o conjunto;
- perder participantes;
- duplicar participantes;
- sobrepor participantes;
- reduzir medidas mínimas;
- gerar coordenadas negativas;
- alterar automaticamente a configuração;
- selecionar silenciosamente apenas parte do conteúdo;
- renderizar uma formação geometricamente inválida.

Quando a área voltar a comportar uma formação válida, o renderizador deverá sair
do fallback e reconstruir integralmente a distribuição. A recuperação deverá ser
**determinística**.

---

## 30. Exclusão de paginação

Paginação ainda não foi especificada para esta capacidade. Ela fica
**integralmente fora desta ADR**.

Não devem ser definidos nesta ADR:

- capacidade por página;
- divisão do conjunto em páginas;
- navegação entre páginas;
- controles de página;
- indicador de página;
- página anterior;
- página seguinte;
- compactação da última página;
- estabilidade entre páginas;
- metadados de paginação.

Regras de paginação presentes em minutas conceituais externas não devem ser
reutilizadas nem adaptadas nesta ADR.

---

## 31. Compatibilidade com telas existentes

Esta ADR determina:

- nenhuma tela existente muda silenciosamente de layout;
- a nova capacidade depende de adoção explícita no JSON do elemento;
- não haverá reorganização automática de JSONs antigos;
- não haverá migração automática sem levantamento;
- não haverá default estrutural implícito capaz de alterar elementos existentes;
- configurações antigas continuarão sujeitas aos contratos vigentes até migração
  explícita;
- a aplicação documental (`APLICAR_ADR`) deverá definir a compatibilidade;
- a futura implementação deverá rejeitar configurações inválidas de modo
  controlado.

A atualização indiscriminada de todos os JSONs existentes não está autorizada.

---

## 32. Relação com ocupação integral do corpo

A nova capacidade preserva as regras de ocupação integral do corpo já aprovadas
pela ADR-0024.

A distribuição interna do conteúdo de um elemento:

- não autoriza espaço externo indevido no corpo;
- não autoriza retenção de área estrutural vazia pelo corpo;
- não redefine a área entregue ao elemento pela composição do corpo;
- não permite que margens internas sejam confundidas com preenchimento externo
  do corpo;
- não reabre a ADR-0024.

As margens configuradas nesta ADR pertencem à distribuição interna do conteúdo
do elemento. Elas são distintas do preenchimento externo proibido pela ADR-0024.

---

## 33. Aplicação a dashboard, console e lançador

Esta ADR permite que `dashboard`, `console` e `lancador` adotem a capacidade
mediante atualização explícita dos seus contratos e JSONs.

Ela **não** declara que todos já utilizam automaticamente a nova capacidade.

A aplicação documental deverá avaliar individualmente:

- quais contratos são afetados;
- quais tipos de elemento podem declarar a distribuição;
- quais validações específicas permanecem necessárias;
- quais regras específicas de cada componente prevalecem;
- quais conflitos precisam ser reconciliados.

Se existir contradição material entre a capacidade genérica e um contrato
específico ativo (em particular com as regras de vãos e alinhamento do
`lancador` definidas nas ADR-0001, ADR-0002 e ADR-0003, ou com as regras de
layout do `console` da seção 4.3 da NOMENCLATURA), essa contradição deverá ser
registrada como necessidade de reconciliação em `APLICAR_ADR`. A solução não
deve ser inventada nesta ADR.

A nova ADR não redefine silenciosamente nenhuma política específica do
`lancador`.

---

## 34. Contratos e documentos afetados

Os contratos JSON precisarão ser alterados posteriormente para definir:

- em qual objeto a configuração de distribuição matricial será declarada;
- quais tipos de elemento podem utilizá-la;
- quais campos serão obrigatórios;
- quais campos serão opcionais;
- vocabulário fechado das políticas;
- valores inteiros aceitos;
- relação entre mínimos e máximos;
- validações de linhas e colunas;
- validações de cardinalidade;
- regras de compatibilidade;
- tratamento de campos desconhecidos;
- ausência ou existência de defaults normativos;
- mensagens de erro;
- representação do fallback;
- relação com configurações antigas.

**Documentos consultados nesta etapa** (existência confirmada):

| Documento | Papel nesta etapa |
|---|---|
| `docs/adr/INDICE_ADR.md` | Consultado para verificar a sequência documental existente; permaneceu inalterado durante `CRIAR_ADR`; inclusão de ADR-0025 pendente de `APLICAR_ADR` |
| `docs/NOMENCLATURA.md` | Referência terminológica e semântica |
| `docs/contratos/contrato_tela_json.md` | Referência de schema e pipeline |
| `docs/contratos/contrato_composicao_corpo.md` | Referência de composição hierárquica |
| `docs/contratos/contrato_lancador.md` | Referência de regras específicas do lancador |
| `docs/contratos/contrato_json_dashboard.md` | Referência de envelope do dashboard |
| `docs/contratos/contrato_json_console.md` | Referência de envelope do console |
| `docs/contratos/contrato_json_lancador.md` | Referência de JSON mínimo do lancador |
| `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md` | Regras de ocupação integral |
| `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | Contexto de composição bidimensional existente |
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | Contexto de profundidade hierárquica |
| `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` | Terminologia de terminal pequeno |
| `docs/adr/ADR-0023-largura-minima-funcional-lancador.md` | Terminologia de fallback do lancador |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | Composição hierárquica do corpo |

**Documentos que precisarão de alteração em `APLICAR_ADR`** (nenhum alterado
nesta etapa):

| Documento | Razão da alteração futura |
|---|---|
| `docs/contratos/contrato_tela_json.md` | Registrar capacidade e referência ao schema de distribuição |
| `docs/contratos/contrato_composicao_corpo.md` | Reconciliar com regras de distribuição interna de elementos |
| `docs/contratos/contrato_lancador.md` | Reconciliar ou adotar a nova capacidade para o lancador |
| `docs/contratos/contrato_json_dashboard.md` | Definir o envelope de distribuição no JSON do dashboard |
| `docs/contratos/contrato_json_console.md` | Definir o envelope de distribuição no JSON do console |
| `docs/contratos/contrato_json_lancador.md` | Definir o envelope de distribuição no JSON do lancador |
| `docs/NOMENCLATURA.md` | Formalizar termos novos que a aplicação introduzir |
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0025 |

Nenhum desses documentos foi alterado durante `CRIAR_ADR`.

---

## 35. Telas de teste futuras

As telas de teste serão construídas posteriormente por configurações JSON
permanentes e repetíveis. Esses JSONs deverão ser criados como parte da futura
implementação ou de handoff especificamente autorizado.

A criação das telas deverá permanecer separada da definição abstrata desta ADR.
Os valores concretos serão escolhidos na construção das telas para cobrir o
maior número razoável de combinações.

O futuro handoff e a implementação deverão prever telas permanentes que cubram,
no mínimo, as seguintes famílias:

### Formação

1. conteúdo com preferência por linhas;
2. conteúdo com preferência por colunas;
3. conteúdo com matriz fixa obrigatória.

### Distribuição horizontal

4. conteúdo centralizado horizontalmente com preferência por colunas;
5. conteúdo justificado à esquerda com margem horizontal mínima e máxima;
6. matriz com distribuição uniforme do espaço entre margem esquerda,
   participantes ou colunas e margem direita;
7. matriz com margens horizontais mínimas e máximas e sobra remanescente
   distribuída entre os participantes.

### Distribuição vertical

8. conteúdo com margem superior mínima e margem inferior mínima;
9. conteúdo com margens superior e inferior mínimas e máximas e sobra
   distribuída entre as linhas;
10. conteúdo com distribuição vertical uniforme entre margem superior, linhas
    ou participantes e margem inferior.

### Casos especiais

11. um único participante centralizado horizontal e verticalmente;
12. conjunto com três ou quatro participantes — centralizado horizontalmente,
    centralizado verticalmente e com distribuição uniforme entre participantes
    e margens.

A escolha concreta entre três e quatro participantes pertence à construção da
fixture e não altera a decisão arquitetural. Esta ADR não deve transformar essa
lista em nomes definitivos de arquivos.

---

## 36. Demo dedicado futuro

Como consequência para uma futura implementação, deverá ser criado um **demo
dedicado à distribuição de conteúdo**, evitando que o demo principal cresça
excessivamente.

O demo dedicado deverá futuramente:

- abrir telas permanentes de demonstração;
- permitir selecionar configurações de distribuição;
- permitir redimensionamento real da janela;
- confirmar semanticamente qual tela foi carregada;
- permitir observar o fallback de terminal pequeno;
- permitir observar a recuperação ao aumentar novamente a janela.

O futuro handoff deverá definir nominalmente o nome, a estrutura, a forma de
invocação e o mecanismo de seleção do demo dedicado, preservando a separação
entre demonstração e produto real estabelecida pelas autoridades ativas.

Nenhum demo foi criado ou alterado nesta etapa.

---

## 37. Cobertura de testes futura

A futura implementação deverá permitir testar, no mínimo:

- validação da configuração;
- formação selecionada;
- quantidade de linhas;
- quantidade de colunas;
- preferência por linhas;
- preferência por colunas;
- matriz fixa;
- ordem por linha;
- ordem por coluna;
- preservação da ordem original;
- dimensões mínimas;
- largura das colunas;
- altura das linhas;
- margens efetivas;
- espaços efetivos;
- respeito aos mínimos;
- respeito aos máximos;
- ordem de expansão;
- distribuição horizontal;
- distribuição vertical;
- distribuição uniforme;
- centralização horizontal;
- centralização vertical;
- alinhamento interno;
- distribuição de restos;
- cardinalidade unitária;
- cardinalidade múltipla;
- comportamento com uma única linha;
- comportamento com uma única coluna;
- ausência de divisão por zero;
- ausência de perda de participantes;
- ausência de duplicação de participantes;
- ausência de truncamento;
- ausência de sobreposição;
- coordenadas não negativas;
- acionamento do estado de terminal muito pequeno;
- recuperação após redimensionamento;
- determinismo;
- compatibilidade com telas antigas.

Os valores esperados materiais não poderão ser calculados a partir da própria
saída observada. Os testes deverão possuir expectativas independentes.

Código de saída zero não será prova suficiente de que a tela ou a configuração
correta foi selecionada.

---

## 38. Demonstração e validação visual futuras

Qualquer implementação visual decorrente desta decisão deve ter:

- configuração permanente e repetível;
- tela identificável;
- ponto de entrada real;
- comando exato;
- confirmação semântica da identidade da tela;
- critérios observáveis;
- possibilidade de redimensionamento;
- teste do estado de terminal muito pequeno;
- teste de recuperação;
- validação humana em TTY real quando exigida pelo QA.

Testes automatizados não substituirão a observação humana quando o comportamento
depender de geometria visual real.

---

## 39. Validações conceituais mínimas

Os contratos posteriores deverão validar, no mínimo:

- margens inteiras não negativas;
- espaços inteiros não negativos;
- dimensões mínimas inteiras não negativas;
- quantidades de linhas e colunas inteiras positivas;
- máximo maior ou igual ao mínimo correspondente;
- limites máximos não inferiores aos mínimos;
- política pertencente ao vocabulário aceito;
- cobertura de cardinalidade unitária;
- cobertura dos restos inteiros;
- cobertura da impossibilidade geométrica;
- ausência de campos ou combinações semanticamente contraditórias.

---

## 40. Consequências

### Positivas

- capacidade configurável por elemento e por tela;
- reutilização entre `dashboard`, `console` e `lancador`;
- redução de hardcoding de layout em código;
- testes geométricos mais completos e independentes;
- demonstração repetível e semânticamente identificável;
- separação clara entre semântica de layout e valores concretos;
- preparação compatível com futura composição multinível.

### Custos e riscos

- ampliação dos contratos JSON existentes;
- ampliação do loader e do modelo para carregar e validar configuração de
  distribuição;
- maior complexidade geométrica no renderizador;
- necessidade de vocabulário fechado de políticas;
- necessidade de validações cruzadas entre campos;
- necessidade de testes extensivos de geometria;
- risco de conflito com contratos específicos ativos (especialmente regras de
  `lancador` nas ADR-0001, ADR-0002, ADR-0003);
- necessidade de preservar compatibilidade com elementos e telas existentes;
- necessidade de separar claramente nível único e multinível na documentação e
  na implementação.

---

## 41. Critérios para futura aplicação da ADR (`APLICAR_ADR`)

`APLICAR_ADR` deverá:

- atualizar `docs/adr/INDICE_ADR.md` registrando ADR-0025;
- atualizar `docs/NOMENCLATURA.md` quando termos novos precisarem ser
  formalizados;
- alterar os contratos JSON aplicáveis;
- reconciliar contratos específicos de `lancador`, `console` e `dashboard`;
- definir nomes e estrutura dos campos de distribuição;
- definir validações;
- definir vocabulário fechado das políticas;
- definir compatibilidade com configurações existentes;
- definir defaults somente se houver decisão normativa explícita;
- registrar os documentos alterados;
- produzir relatório de aplicação;
- não implementar código.

---

## 42. Critérios para o futuro handoff

O futuro handoff deverá:

- autorizar nominalmente: código, loader, modelo e renderizador da distribuição
  matricial;
- autorizar testes da capacidade;
- autorizar os JSONs permanentes das telas de teste;
- autorizar o demo dedicado à distribuição de conteúdo;
- autorizar o relatório de implementação;
- separar arquivos do autor do handoff dos arquivos da futura implementação;
- conter escopo suficiente para testes e demonstração;
- definir comandos exatos de execução;
- definir identidade semântica de cada tela de teste;
- definir suíte canônica de verificações;
- definir critérios de acionamento do estado de terminal muito pequeno;
- definir critérios de recuperação após redimensionamento;
- preservar nível único como escopo exclusivo;
- manter multinível fora do escopo;
- conter cláusula de exceção operacional para arquivo estritamente necessário
  fora da lista, quando comprovada a necessidade.

---

## 43. Relação com ADRs anteriores

| ADR | Relação com ADR-0025 |
|---|---|
| ADR-0001 (menu em modo matriz) | Complementa: ADR-0025 generaliza a capacidade de matriz do lancador para qualquer elemento; ADR-0001 permanece como especificação concreta do algoritmo do lancador; reconciliação necessária em APLICAR_ADR |
| ADR-0002 (sobra à direita do lancador) | Preserva: ADR-0025 não altera essa política; reconciliação necessária para verificar como ela se expressa no vocabulário da nova capacidade |
| ADR-0003 (vãos elásticos do lancador) | Preserva: ADR-0025 não altera os vãos do lancador; reconciliação necessária para mapeá-los ao modelo de margens e espaços desta ADR |
| ADR-0010 (composição hierárquica corpo) | Complementa: ADR-0025 opera dentro de um elemento já posicionado pela composição hierárquica; não substitui nem redefine a composição hierárquica |
| ADR-0013 (ocupação vertical do corpo) | Preserva: ADR-0025 não altera a ocupação do terminal; as margens internas desta ADR não se confundem com o preenchimento vertical do corpo |
| ADR-0014 (distribuição responsiva da barra) | Não altera: ADR-0025 não trata da barra_de_menus |
| ADR-0015 (composição hierárquica e distribuição) | Complementa: ADR-0025 opera no nível de conteúdo interno de um elemento, não no nível de distribuição de área entre filhos de um container do corpo |
| ADR-0017 (redimensionamento reativo da TUI) | Preserva e referencia: o fallback de terminal muito pequeno desta ADR deve ser reconciliado com o `quadro mínimo de terminal pequeno` da ADR-0017 em APLICAR_ADR |
| ADR-0018 (semântica ausência distribuição) | Não altera: a ausência de distribuição no corpo preserva construção orientada pelo conteúdo; ADR-0025 trata de distribuição dentro de um elemento, não de distribuição de área do corpo |
| ADR-0019 (profundidade grupos) | Preserva: ADR-0025 não altera contagem de níveis de grupos nem cardinalidade de dashboard |
| ADR-0020 (matriz declarativa de grupos) | Complementa sem conflito: ADR-0020 trata da grade de grupos do nó `grupo` da árvore de composição do corpo; ADR-0025 trata da distribuição matricial dos participantes imediatos dentro de um elemento funcional |
| ADR-0023 (largura mínima do lancador) | Preserva e referencia: o fallback global do lancador permanece ativo; ADR-0025 não cria fallback local; reconciliação necessária sobre como a impossibilidade geométrica desta ADR interage com o fallback global da ADR-0023 |
| ADR-0024 (proibição preenchimento vazio) | Preserva: ADR-0025 não autoriza espaço vazio externo no corpo; as margens internas desta ADR são distintas do preenchimento externo proibido pela ADR-0024 |

---

## 44. Itens fora de escopo

São explicitamente excluídos desta ADR:

- distribuição multinível;
- recursão de layout;
- herança de configuração entre níveis;
- cascata de parâmetros;
- interação geométrica entre níveis;
- propagação de fallback entre níveis;
- paginação;
- navegação entre páginas;
- controles de paginação;
- valores concretos de telas;
- nomes definitivos dos campos JSON;
- schema JSON final;
- nomes definitivos dos JSONs de teste;
- nome definitivo do demo dedicado;
- implementação do loader;
- implementação do modelo;
- implementação do renderizador;
- criação das telas de teste;
- criação dos JSONs de teste;
- criação do demo dedicado;
- alteração de contratos (reservada para APLICAR_ADR);
- migração de configurações existentes;
- handoff;
- QA;
- validação manual;
- commit.

---

## 45. Decisões futuras

As seguintes questões ficam abertas para decisão futura:

1. **Nomes finais dos campos JSON** — definidos em `APLICAR_ADR` após revisão
   dos padrões documentais do projeto.
2. **Vocabulário fechado completo das políticas** — definido em `APLICAR_ADR`.
3. **Defaults normativos** — somente se houver decisão normativa explícita em
   `APLICAR_ADR`.
4. **Tratamento de participante maior que dimensão fixa** — exige decisão
   explícita adicional antes ou durante a implementação.
5. **Reconciliação dos contratos do `lancador`** — como as políticas de
   ADR-0001, ADR-0002 e ADR-0003 se expressam no vocabulário da nova
   capacidade.
6. **Reconciliação do fallback** — como o estado de terminal muito pequeno
   desta ADR interage com o `quadro mínimo de terminal pequeno` (ADR-0017)
   e com o fallback global do `lancador` (ADR-0023).
7. **Alinhamento do `dashboard`** — a questão pendente da seção 11 da
   NOMENCLATURA (centralizado vs. bloco à esquerda com sobra à direita)
   deverá ser reconciliada em `APLICAR_ADR`.
8. **Adoção por console** — a relação entre as regras da seção 4.3 da
   NOMENCLATURA e a nova capacidade exige avaliação explícita em `APLICAR_ADR`.
9. **Distribuição multinível** — requer decisão e ADR próprias.
10. **Paginação** — requer especificação e ADR próprias.
