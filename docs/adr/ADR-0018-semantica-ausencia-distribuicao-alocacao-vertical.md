---
name: ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical
description: Distingue arranjo de distribuição; ausência de corpo.distribuicao deixa de ser equivalente ao modo igual e preserva a construção orientada pelo conteúdo; distribuição explícita reparte a altura útil entre os filhos diretos com preenchimento interno das áreas; percentual e fracao permanecem genéricos; conteúdo que não cabe é problema separado fora de escopo; não implementa código, não altera JSON, não altera o H-0024
metadata:
  type: adr
  status: proposta
  data: 2026-07-11
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0018 — Semântica da ausência de distribuição e da alocação vertical de área do corpo

## Status

`proposta`

## Data

2026-07-11

---

## Contexto

O corpo da tela ocupa a região variável entre o `cabecalho` (acima) e a
`barra_de_menus` (abaixo). A ADR-0013 fixou que essa região — a `altura_disponivel`
— deve ser ocupada pelo corpo, com preenchimento de linhas em branco pelo renderer
quando o conteúdo declarado for menor que a altura disponível. A ADR-0015 modelou o
corpo como árvore de composição, formalizou `arranjo` e `distribuicao` por container
e os modos `igual`, `percentual` e `fracao`. A ADR-0017 fixou como obter e manter as
dimensões válidas durante a sessão TTY (SIGWINCH, cadeia `ioctl → LINES/COLUMNS →
últimas dimensões válidas`), sem alterar a composição declarada.

No cenário visual apresentado pelo usuário, a tela possui três regiões macro —
`cabecalho`, `corpo` e `barra_de_menus` — e os três filhos diretos do corpo são:

1. `ITENS` / `console_principal`;
2. `INFO` / `dashboard_info`;
3. `NAVEGAR` / `lancador_principal`.

Atualmente, esses elementos são renderizados por suas alturas naturais e a grande
sobra vertical permanece **fora** das molduras dos elementos, acumulada entre a
moldura inferior de `NAVEGAR` e a moldura superior de `Menus`. Quando uma
distribuição for declarada, esse comportamento não é o desejado: a área vazia
pertence à área útil do corpo e deve ser repartida entre os filhos, ficando **dentro**
das molduras de `ITENS`, `INFO` e `NAVEGAR`.

Durante a tentativa de implementação do H-0024 (registrada em
`docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md` e no
`RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`, ambos evidências,
não autoridades), a semântica então vigente — em que a **ausência** de
`corpo.distribuicao` era tratada como **equivalente ao modo `igual`** — entrou em
contradição, no modelo real, com a regressão histórica que preserva o empilhamento
orientado pelo conteúdo. O executor retornou `ARCHITECTURE_REVIEW_REQUIRED`. Esta ADR
existe para registrar as decisões arquiteturais explícitas do usuário que resolvem a
ambiguidade normativa entre **arranjo** e **distribuição** e entre **ausência de
distribuição** e **modo `igual`**.

Esta ADR é normativa. Ela **não** implementa código, **não** altera contratos, **não**
altera JSON, **não** cria nem corrige handoff e **não** altera o H-0024. Define
exclusivamente a política a ser aplicada documentalmente em etapa posterior.

---

## Problema

A formulação anterior tratava a ausência de `corpo.distribuicao` como semanticamente
equivalente ao modo `igual` (ver `contrato_json_tela_minima.md`, "sua ausência é
válida e equivale ao modo `igual`", e o contexto do modo `igual` na ADR-0015). Essa
equivalência produz três problemas:

1. **Colapso conceitual entre arranjo e distribuição.** `corpo.arranjo = "vertical"`
   passa a ser lido como obrigação de repartir proporcionalmente toda a altura
   disponível, quando arranjo declara apenas ordem/composição.
2. **Perda da construção orientada pelo conteúdo.** Um corpo vertical sem
   distribuição declarada passaria a dividir a altura útil igualmente, substituindo
   o empilhamento por alturas naturais mesmo quando o usuário não pediu repartição.
3. **Localização incorreta da sobra na distribuição explícita.** Quando uma
   distribuição *é* declarada, a sobra vertical não deve permanecer acumulada
   externamente abaixo do último elemento; deve ser incorporada às áreas atribuídas
   aos filhos.

A ADR registra a distinção entre arranjo e distribuição, a nova semântica da
ausência de distribuição, a semântica da distribuição explícita e o preenchimento
interno das áreas alocadas, sem decidir qualquer política de conteúdo que não cabe.

---

## Decisões

As decisões abaixo são registro das decisões já tomadas explicitamente pelo usuário.
A ADR não escolhe arquitetura adicional nem completa lacunas.

### D1 — Distinção entre arranjo e distribuição

`corpo.arranjo = "vertical"` define a **ordem vertical** dos filhos.

O arranjo vertical, sozinho, **não obriga** a repartir proporcionalmente toda a
altura disponível. Arranjo e distribuição são conceitos distintos: arranjo é ordem
de composição; distribuição é repartição de área.

### D2 — Ausência de `distribuicao`

Quando `corpo.distribuicao` **não** estiver declarada:

- preservar a construção inicial orientada pelo conteúdo;
- cada elemento usa sua altura natural conforme o conteúdo e as regras próprias do
  tipo;
- não transformar automaticamente a ausência em modo `igual`;
- não repartir automaticamente toda a altura útil entre os filhos;
- o espaço vertical excedente pode permanecer como preenchimento externo do corpo,
  conforme o comportamento de ocupação já existente (ADR-0013).
  *(Este bullet é **substituído pela ADR-0024**: o preenchimento externo vazio é
  proibido; a ocupação deve ser concretizada por elementos visuais conforme DA-01
  a DA-04 da ADR-0024.)*

A ausência de `distribuicao` **deixa de ser** semanticamente equivalente ao modo
`igual`.

### D3 — `distribuicao` explicitamente declarada

Quando `corpo.distribuicao` estiver declarada em um container com
`arranjo: "vertical"`, a distribuição deve **repartir a altura útil vertical
disponível** entre os filhos diretos.

A altura útil é a região do corpo situada entre o `cabecalho` e a `barra_de_menus`,
descontadas somente as linhas estruturais já definidas pelos contratos aplicáveis.

A distribuição **aloca área**, não apenas conteúdo.

### D4 — Preenchimento interno da área alocada

Quando a área atribuída a um elemento for maior que seu conteúdo natural:

- a moldura do elemento deve ocupar a área atribuída;
- a sobra deve virar **linhas em branco dentro da área desse elemento**;
- a sobra **não** deve permanecer acumulada externamente abaixo do último elemento;
- a soma das áreas atribuídas deve ocupar **toda** a altura distribuível do corpo.

Em termos visuais, o espaço atualmente localizado entre a borda inferior de `NAVEGAR`
e a borda superior de `Menus` deve ser repartido e incorporado às caixas de `ITENS`,
`INFO` e `NAVEGAR` quando houver distribuição explícita.

### D5 — Modo `igual` explícito

Quando o modo `igual` for declarado explicitamente:

- a área distribuível é dividida igualmente entre os filhos diretos;
- `igual` continua sendo um modo válido;
- `igual` **não** é o fallback implícito da ausência de `distribuicao`.

### D6 — Modo `percentual`

O modo `percentual` deve continuar genérico e seguir as regras normativas aplicáveis:

- um valor por filho direto;
- associação posicional na ordem declarada;
- soma normativa de 100;
- cálculo sobre toda a área distribuível;
- arredondamento e linhas residuais conforme o método normativo existente (maiores
  restos; empates pela ordem declarada).

### D7 — Modo `fracao`

O modo `fracao` deve aceitar **qualquer** vetor válido de pesos positivos. A
semântica é:

- um peso por filho direto;
- associação posicional na ordem declarada;
- denominador igual à soma dos pesos;
- cota de cada filho proporcional ao próprio peso;
- arredondamento e linhas residuais conforme o método normativo existente.

O código **não** pode ser especializado para um vetor concreto. São exemplos válidos,
sem caráter exaustivo:

```text
[1, 1, 1]
[2, 1, 2]
[1, 3, 1]
[5, 2, 7]
```

`[1, 1, 1]` é válido e representa pesos iguais. `[2, 1, 2]` é apenas uma possível
configuração concreta de tela e **não** é regra interna do renderer.

### D8 — Terminal pequeno e conteúdo que não cabe

O fato de um vetor válido produzir uma cota menor que a altura natural de algum
elemento em terminal muito pequeno **não** torna o vetor inválido.

Esse caso pertence a outro problema normativo, entre outros:

- altura mínima;
- overflow;
- truncamento;
- paginação;
- rejeição;
- degradação;
- ou outra política para conteúdo que não cabe.

**Nenhuma** dessas políticas está sendo decidida nesta ADR. Esse problema permanece
fora de escopo e **não** pode bloquear a implementação geral da distribuição em
alturas onde o conteúdo cabe.

### D9 — Mudança JSON necessária ao handoff

Qualquer alteração concreta em JSON necessária para implementar ou demonstrar um
handoff deve estar prevista no **próprio handoff**. O handoff deve identificar:

- arquivo JSON alterável;
- alteração declarativa;
- valores concretos, quando já decididos;
- critérios de aceite;
- validação sintática;
- testes correspondentes.

Essa regra **não** autoriza o renderer a hardcodar valores do JSON.

### D10 — Testes deste ciclo

A ADR distingue:

- capacidade genérica do algoritmo;
- configuração concreta de uma tela;
- cobertura exaustiva de combinações.

A ADR **não** exige que todas as combinações possíveis de pesos, alturas e
quantidades de filhos sejam testadas no mesmo ciclo de implementação. Também **não**
define agora um novo handoff de testes. Registra apenas que a implementação deve
possuir verificação mínima suficiente para a capacidade entregue e que cobertura
ampliada **não** altera a semântica decidida nesta ADR.

---

## Exemplo visual (descrição textual)

Considere a tela com as três regiões macro e os três filhos diretos do corpo, na
ordem declarada:

```text
┌──────────────── cabecalho ────────────────┐
│                                            │
└────────────────────────────────────────────┘
┌──────────────── ITENS (console) ──────────┐   ← filho 1: console_principal
│  (conteúdo natural)                        │
└────────────────────────────────────────────┘
┌──────────────── INFO (dashboard) ─────────┐   ← filho 2: dashboard_info
│  (conteúdo natural)                        │
└────────────────────────────────────────────┘
┌──────────────── NAVEGAR (lancador) ───────┐   ← filho 3: lancador_principal
│  (conteúdo natural)                        │
└────────────────────────────────────────────┘

              ┃  GRANDE SOBRA VERTICAL  ┃         ← hoje: fora das molduras,
              ┃  (área vazia acumulada) ┃           entre NAVEGAR e Menus

┌──────────────── barra_de_menus / Menus ───┐
└────────────────────────────────────────────┘
```

**Estado atual (sem distribuição):** a sobra vertical fica acumulada *externamente*,
entre a moldura inferior de `NAVEGAR` e a moldura superior de `Menus`. Sob a semântica
da D2, esse comportamento orientado pelo conteúdo é **preservado** enquanto
`corpo.distribuicao` não for declarada.

**Estado desejado com distribuição explícita (D3, D4):** a mesma sobra vertical é
repartida entre os três filhos e passa a ficar *dentro* das molduras de `ITENS`,
`INFO` e `NAVEGAR`, como linhas em branco internas a cada caixa. As três caixas
crescem para preencher a altura útil, e não resta espaço acumulado abaixo de
`NAVEGAR`:

```text
┌──────────────── ITENS (console) ──────────┐
│  (conteúdo natural)                        │
│  (linhas em branco internas da cota)       │
└────────────────────────────────────────────┘
┌──────────────── INFO (dashboard) ─────────┐
│  (conteúdo natural)                        │
│  (linhas em branco internas da cota)       │
└────────────────────────────────────────────┘
┌──────────────── NAVEGAR (lancador) ───────┐
│  (conteúdo natural)                        │
│  (linhas em branco internas da cota)       │
└────────────────────────────────────────────┘
┌──────────────── barra_de_menus / Menus ───┐
└────────────────────────────────────────────┘
```

---

## Semântica da ausência de `distribuicao`

Sem `corpo.distribuicao` declarada, o corpo vertical mantém a construção orientada
pelo conteúdo: cada filho usa sua altura natural. A ausência **não** é interpretada
como `igual` e **não** dispara repartição proporcional automática da altura útil (D2).
A ocupação integral da área deve ser garantida por elementos visuais conforme a
ADR-0024 (DA-01 a DA-04): com um único descendente visual, ele ocupa toda a área
(DA-01); com múltiplos elementos no mesmo eixo, a composição é inválida (DA-02).

---

## Semântica da distribuição explícita

Com `corpo.distribuicao` declarada em container vertical, a altura útil (região entre
`cabecalho` e `barra_de_menus`, descontadas as linhas estruturais dos contratos) é
repartida entre os filhos diretos. A distribuição aloca área, e a área alocada deve
ser preservada e preenchida internamente (D3, D4). A soma das áreas atribuídas ocupa
toda a altura distribuível do corpo.

---

## Modo `igual` explícito

`igual` divide a área distribuível igualmente entre os filhos diretos. Permanece um
modo válido e explícito. Deixa de ser o significado implícito da ausência de
`distribuicao` (D5).

---

## Modo `percentual`

Modo genérico: um valor por filho direto, associação posicional na ordem declarada,
soma normativa de 100, cálculo sobre toda a área distribuível, arredondamento e
linhas residuais pelo método dos maiores restos com empate pela ordem declarada (D6).

---

## Modo `fracao` genérico

Modo genérico: um peso positivo por filho direto, associação posicional na ordem
declarada, denominador igual à soma dos pesos, cota proporcional ao próprio peso,
arredondamento e linhas residuais pelo método existente. Qualquer vetor válido de
pesos positivos é aceito; o renderer não pode ser especializado para um vetor
concreto (D7).

---

## Preenchimento interno das áreas

Quando a área atribuída exceder o conteúdo natural do elemento, a moldura ocupa a
área atribuída e a sobra vira linhas em branco **dentro** da área do elemento, nunca
acumulada externamente abaixo do último filho (D4). Isto é coerente com a ADR-0015
(preenchimento de área alocada) e localiza inequivocamente a sobra da distribuição
explícita dentro das molduras.

---

## Distinção entre vetor válido e conteúdo que não cabe

Um vetor de pesos é válido quando satisfaz as regras do modo (positividade,
cardinalidade por filho direto, soma normativa quando aplicável). A eventual
insuficiência de uma cota frente à altura natural de um elemento, em terminal muito
pequeno, é um problema **separado** de conteúdo que não cabe (altura mínima, overflow,
truncamento, paginação, rejeição, degradação). Vetor válido continua válido; a política
para cota insuficiente não é decidida aqui e não bloqueia a distribuição geral em
alturas onde o conteúdo cabe (D8).

---

## Consequências

- A distinção entre arranjo e distribuição fica normatizada: arranjo vertical não
  obriga repartição proporcional da altura (D1).
- A ausência de `distribuicao` preserva a construção orientada pelo conteúdo e deixa
  de ser equivalente ao modo `igual` — formulações normativas que afirmam essa
  equivalência tornam-se conflitantes e deverão ser removidas na aplicação documental
  (D2, D5).
- A distribuição explícita reparte a altura útil e incorpora a sobra às áreas dos
  filhos, dentro das molduras (D3, D4).
- `percentual` e `fracao` permanecem genéricos; nenhum vetor concreto pode ser
  hardcoded no renderer (D6, D7).
- O problema de conteúdo que não cabe permanece explicitamente fora de escopo e não
  pode ser usado para bloquear a implementação geral (D8).
- A regra processual sobre alteração de JSON necessária ao handoff é reafirmada (D9).
- A cobertura de testes exigida é a mínima suficiente para a capacidade entregue;
  cobertura ampliada não altera a semântica decidida (D10).
- Documentos que hoje afirmam ausência ≡ `igual` precisarão ser revisados na etapa de
  aplicação documental (ver "Documentos afetados").

---

## Compatibilidade

- Telas verticais **sem** `corpo.distribuicao` mantêm o comportamento orientado pelo
  conteúdo (D2), portanto o comportamento observável dessas telas é preservado quanto
  ao empilhamento por altura natural e à ocupação vertical externa da ADR-0013.
- Telas que declararem `corpo.distribuicao` passam a repartir a altura útil conforme o
  modo declarado. `igual`, `percentual` e `fracao` permanecem os modos válidos já
  registrados pela ADR-0015.
- O algoritmo de arredondamento (maiores restos, empate pela ordem declarada) e o
  princípio de preenchimento da área alocada da ADR-0015 permanecem vigentes.
- Esta ADR não introduz novo modo, novo campo obrigatório nem novo tipo de elemento.

---

## Relação com a ADR-0013

A ADR-0013 é **preservada** quanto à ocupação vertical da janela e à existência de
uma área útil entre `cabecalho` e `barra_de_menus`. Esta ADR **esclarece** onde o
preenchimento fica quando existe distribuição explícita: **dentro** das áreas
atribuídas aos filhos. Na ausência de distribuição, a obrigação de ocupação vertical
da ADR-0013 continua vigente e é complementada pela ADR-0024: a ocupação deve ser
realizada por elementos visuais, não por preenchimento externo vazio (DA-01 a DA-04
da ADR-0024).

---

## Relação com a ADR-0015

A ADR-0015 é **parcialmente substituída somente** no ponto em que a ausência de
`distribuicao` foi tratada como equivalente ao modo `igual`. Esta ADR registra a
substituição normativa desse trecho conflitante.

Permanecem válidas, salvo conflito explícito:

- distribuição por container;
- associação aos filhos diretos;
- modos `igual`, `percentual` e `fracao`;
- pesos;
- soma percentual;
- maiores restos;
- desempate pela ordem declarada;
- preenchimento da área alocada;
- composição hierárquica.

Esta ADR **não** reescreve nem altera a ADR-0015. Registra apenas a substituição
normativa do trecho em que ausência era tratada como `igual`.

---

## Relação com a ADR-0017

A ADR-0017 é **preservada integralmente** quanto à obtenção de dimensões e ao
redimensionamento reativo (SIGWINCH, cadeia `ioctl → LINES/COLUMNS → últimas dimensões
válidas`, quadro mínimo de aviso). Esta ADR **não** cria nova arquitetura de eventos.
A altura útil repartida pela distribuição é obtida pelo mecanismo da ADR-0017; o
redimensionamento recalcula as cotas dependentes da dimensão sem alterar a composição
declarada.

---

## Documentos afetados

Documentos identificados para aplicação documental futura (etapa posterior; não
alterados por esta ADR):

| Documento | Ponto a revisar |
|---|---|
| `docs/contratos/contrato_composicao_corpo.md` | Registrar a distinção arranjo × distribuição (D1); ausência de `distribuicao` preserva construção orientada pelo conteúdo e não equivale a `igual` (D2, D5); distribuição explícita reparte a altura útil e incorpora a sobra dentro das molduras (D3, D4); manter `percentual`/`fracao` genéricos (D6, D7) |
| `docs/contratos/contrato_tela_json.md` | Alinhar a descrição de `corpo.distribuicao` à nova semântica de ausência × explícita |
| `docs/contratos/contrato_json_tela_minima.md` | Remover/rever a formulação "sua ausência é válida e equivale ao modo `igual`" para `corpo` vertical, conforme D2/D5 (o texto de `grupo` deve ser revisto no mesmo espírito) |
| `docs/contratos/contrato_processo_desenvolvimento.md` | Registrar a regra processual de que alteração de JSON necessária ao handoff pertence ao próprio handoff (D9), quando confirmado pelo conteúdo real |
| `docs/NOMENCLATURA.md` | Registrar a distinção arranjo × distribuição e a nova semântica de ausência; não afirmar ausência ≡ `igual` |
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0018 |
| Exemplos normativos que afirmem ausência ≡ `igual` | Localizar e corrigir os exemplos que codifiquem essa equivalência |

O H-0024 deverá ser retomado, corrigido ou recriado **somente após**: (1) criação
desta ADR; (2) QA da ADR; (3) aplicação documental; (4) QA da aplicação. Esta ADR
não corrige o H-0024.

---

## Itens fora de escopo

Declarados explicitamente fora de escopo desta ADR:

- implementação de qualquer código ou teste;
- alteração do H-0024;
- alteração de `config/telas/orquestrador.json` ou de qualquer JSON;
- escolha definitiva de um vetor de distribuição para todas as telas;
- hardcode de `[2, 1, 2]` (ou de qualquer vetor concreto);
- especialização do renderer para a tela Orquestrador;
- altura mínima por tipo;
- overflow;
- truncamento;
- paginação de `lancador`;
- degradação em terminal insuficiente;
- política para conteúdo maior que a cota;
- matriz exaustiva de testes;
- validação manual em TTY;
- manipulação de stash;
- preparação de commit.

---

## Critérios para futura aplicação

A aplicação documental futura precisa:

- remover formulações normativas que tratem ausência como `igual`;
- preservar `igual` como modo explícito;
- deixar inequívoca a diferença entre conteúdo natural e área distribuída;
- registrar que a sobra vertical distribuída fica dentro das molduras;
- preservar o caráter genérico de `percentual` e `fracao`;
- não transformar exemplos concretos em hardcode;
- registrar a regra processual sobre JSON necessário ao handoff;
- identificar exemplos e schemas afetados;
- não definir altura mínima ou overflow.

---

## Impacto esperado sobre o H-0024

O bloqueio do H-0024 (`ARCHITECTURE_REVIEW_REQUIRED`) decorreu, segundo as evidências
(IMP-0025 e o relatório de levantamento), da colisão entre a semântica então vigente
de ausência ≡ `igual` aplicada ao `orquestrador.json` real e a regressão histórica que
preserva o empilhamento orientado pelo conteúdo. Ao registrar que a ausência de
`distribuicao` preserva a construção orientada pelo conteúdo (D2) e que a repartição da
altura útil só ocorre com distribuição explícita (D3), esta ADR fornece a decisão
arquitetural que faltava para desbloquear o trabalho.

Esta ADR **não** retoma, corrige nem recria o H-0024. A retomada ocorrerá apenas após
QA desta ADR, aplicação documental e QA da aplicação, em etapa posterior.

---

## Ausência de implementação nesta etapa

Esta ADR não altera código, testes, JSON, contratos, nomenclatura, handoffs,
relatórios, índice de ADRs, estado operacional, stash ou histórico Git. Cria somente
este arquivo. Toda aplicação é diferida para a etapa `APLICAR_ADR` subsequente, após
QA desta ADR.

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Manter ausência de `distribuicao` ≡ modo `igual` | Colapsa arranjo e distribuição, elimina a construção orientada pelo conteúdo e contradiz a decisão explícita do usuário (D1, D2) |
| Repartir a altura útil automaticamente sempre que `arranjo = "vertical"` | Trata arranjo como distribuição; não é o comportamento desejado quando não há distribuição declarada (D1, D2) |
| Deixar a sobra vertical externamente acumulada mesmo com distribuição explícita | Contradiz o resultado visual desejado; a sobra deve ficar dentro das molduras dos filhos (D4) |
| Hardcodar um vetor concreto (ex.: `[2, 1, 2]`) no renderer | `fracao`/`percentual` devem permanecer genéricos; vetor concreto é configuração de tela, não regra do renderer (D7) |
| Definir altura mínima/overflow nesta ADR para resolver o caso-limite | Fora de escopo explícito; conteúdo que não cabe é problema normativo separado (D8) |

## Exemplo

```text
Decidimos que, para o corpo com arranjo vertical, a ausência de corpo.distribuicao
preserva a construção orientada pelo conteúdo (não equivale a igual), e que a
distribuição explícita reparte a altura útil entre os filhos diretos, com a sobra
incorporada como linhas em branco dentro das molduras.
Contratos afetados (aplicação futura): docs/contratos/contrato_composicao_corpo.md,
docs/contratos/contrato_json_tela_minima.md, docs/NOMENCLATURA.md e outros listados
em "Documentos afetados".
```

---

## Substituição parcial pela ADR-0024 (2026-07-15)

A ADR-0024 — Proibição de preenchimento vazio externo do corpo (2026-07-15) — substitui parcialmente a **D2** desta ADR no ponto do preenchimento externo vazio.

**Trecho substituído em D2:**

> "o espaço vertical excedente pode permanecer como preenchimento externo do corpo, conforme o comportamento de ocupação já existente (ADR-0013)."

**Partes de D2 que permanecem válidas:**

- Preservar a construção inicial orientada pelo conteúdo.
- Cada elemento usa sua altura natural conforme o conteúdo e as regras próprias do tipo.
- Não transformar automaticamente a ausência em modo `igual`.
- Não repartir automaticamente toda a altura útil entre os filhos.
- A ausência de `distribuicao` não é semanticamente equivalente ao modo `igual`.

**Nova distinção normativa (ADR-0024):**

A ausência de `distribuicao` passa a ter dois comportamentos distintos, dependendo da quantidade de descendentes visuais no mesmo eixo:

- **Cardinalidade unitária (DA-01):** quando o container possuir exatamente um descendente visual aplicável (`console`, `dashboard` ou `lancador`), esse elemento ocupa integralmente toda a área disponível, mesmo sem `distribuicao` declarada. Isso decorre da cardinalidade unitária — não equivale a `distribuicao: igual` e não cria distribuição implícita entre múltiplos elementos.
- **Múltiplos elementos (DA-02):** quando dois ou mais elementos disputam o mesmo eixo sem `distribuicao` declarada, a composição é inválida. A sobra não pode permanecer como preenchimento externo.

O restante das decisões desta ADR (D1, D3 a D10) permanece integralmente vigente.
