---
name: ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard
description: Define que a profundidade hierárquica do corpo é contada por aninhamento de grupos (não por listas elementos[]); formaliza o limite de três níveis de grupos; permite múltiplos grupos irmãos e múltiplos elementos funcionais por grupo, inclusive no nível 3; remove a restrição global de zero ou um dashboard por tela
metadata:
  type: adr
  status: aceita
  data: 2026-07-12
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - docs/adr/ADR-0007-tela-processamento-composicao.md
  handoffs_bloqueados: []
---

# ADR-0019 — Profundidade contada por aninhamento de grupos, multiplicidade estrutural e remoção da cardinalidade global de dashboard

## Status

`aceita`

## Data

2026-07-12

---

## Contexto

A ADR-0015 formalizou o corpo como árvore de composição e introduziu o nó
estrutural `grupo`, o conceito de nível como conjunto de filhos diretos de um
container e a profundidade máxima de três níveis. A contagem registrada nos
contratos e na ADR-0015 define nível como: `corpo.elementos[]` é nível 1;
`grupo.elementos[]` cria o próximo nível; cada grupo aninhado cria um novo
nível (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:93–103`;
`docs/contratos/contrato_composicao_corpo.md:132–137`).

Essa formulação trata toda lista `elementos[]` — seja do corpo raiz, seja de
um grupo, seja de um elemento funcional que possua subelementos — como
criadoras de nível hierárquico. Isso gera uma ambiguidade: elementos funcionais
contidos num grupo de nível 3 poderiam ser lidos como instanciando um nível 4,
tornando inválida qualquer composição com elementos funcionais dentro de grupos
no nível mais profundo permitido.

Paralelamente, o contrato de composição registrava "zero ou um dashboard por
tela" como restrição universal do tipo (`docs/contratos/contrato_composicao_corpo.md:87–89`),
o que limitava a presença de mais de um `dashboard` na mesma tela mesmo quando
colocados em grupos distintos. Essa restrição foi identificada como originada
especificamente na tela raiz do Orquestrador, não como política geral do tipo.

O levantamento `RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`
classificou esses pontos como achados bloqueantes (`ACH-007 — Ambiguidade de
grupo no nível 3` e `ACH-009 — Cardinalidade de dashboard por tela`) e indicou
que ambos exigiam decisão explícita do usuário antes de qualquer handoff que
abrangesse composições hierárquicas de três níveis ou múltiplos dashboards em
grupos distintos. O levantamento concluiu com status
`L3_DECISAO_DO_USUARIO_E_ADR_NECESSARIAS`.

Esta ADR registra as decisões explícitas do usuário que resolvem as duas
ambiguidades normativas.

---

## Problema identificado pelo levantamento

### Ambiguidade ACH-007 — Grupo no nível 3

A formulação normativa vigente não esclarecia se um `grupo` declarado como
filho de um container no nível 2 (portanto, no nível 3) poderia conter elementos
funcionais sem criar um nível 4. A regra de que "`grupo.elementos[]` cria o
próximo nível" tornava ambíguo se os filhos **funcionais** de um grupo no nível
3 constituíam ou não um quarto nível (`RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md:287–295`).

Sem resolução, qualquer especificação de composição em três níveis contendo
elementos funcionais dentro do grupo mais profundo arriscava violar o limite de
profundidade, impedindo o uso prático da hierarquia completa.

### Ambiguidade ACH-009 — Cardinalidade global de dashboard

O contrato de composição registrava `dashboard` com presença "zero ou um por
tela". Essa formulação, quando combinada com a autorização de grupos aninhados,
proibiria que dois grupos distintos de uma mesma tela contivessem cada um um
`dashboard`. O levantamento identificou que essa restrição decorreu da
especificação particular da tela raiz do Orquestrador e não de uma política
intencionalmente global do tipo
(`RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md:306–313`).

---

## Decisões

As decisões abaixo são o registro das decisões explicitamente tomadas pelo
usuário. Esta ADR não escolhe arquitetura adicional, não completa lacunas e não
introduz regras além das aqui enunciadas.

---

### D1 — O limite hierárquico é contado por níveis de grupos

A profundidade hierárquica do corpo passa a ser contada exclusivamente pelos
**níveis de grupos** — nós estruturais do tipo `grupo` — e não pelo número de
listas `elementos[]` aninhadas.

A contagem de nível de grupo é:

```text
nível de grupo 1:
    grupo que é filho direto de corpo.elementos[]

nível de grupo 2:
    grupo que é filho direto de um grupo do nível 1

nível de grupo 3:
    grupo que é filho direto de um grupo do nível 2
```

O corpo raiz não é contado como nível de grupo.

Elementos funcionais (`console`, `lancador`, `dashboard`) contidos em qualquer
grupo não acrescentam um novo nível de grupo — independentemente do nível do
grupo que os contém.

Esta decisão substitui a leitura operacional anterior que tratava toda lista
`elementos[]` como criadora de novo nível hierárquico, para fins da regra de
profundidade máxima.

---

### D2 — Profundidade máxima de três níveis de grupos

O limite de profundidade máxima do corpo continua sendo **três**, mas esse
limite passa a ser contado em **níveis de grupos** conforme D1.

Uma estrutura que contenha um grupo do nível 3 é válida. Um grupo que estaria
no nível 4 — filho direto de um grupo do nível 3 — é estruturalmente inválido.

A validação futura deverá distinguir a profundidade de grupos da profundidade
genérica de listas `elementos[]`. Esta ADR registra a regra normativa; não
define nesta etapa textos exatos de mensagens de erro nem implementa a
validação.

---

### D3 — Elementos funcionais dentro de um grupo do nível 3

Um grupo do nível 3:

- **pode** conter um ou mais elementos funcionais do conjunto permitido
  (`console`, `lancador`, `dashboard`);
- **não pode** conter outro `grupo`, porque isso criaria o nível 4 de grupo.

Os elementos funcionais dentro de um grupo do nível 3 **não constituem** um
quarto nível de grupo. A regra de contagem da D1 aplica-se: somente a
introdução de um nó estrutural `grupo` como filho cria um novo nível.

---

### D4 — Proibição de grupo no nível de grupo 4 ou superior

Um `grupo` declarado como filho de um grupo do nível 3 estaria no nível 4 e
é **estruturalmente inválido**.

Estruturas que exigirem um grupo no nível 4 ou superior devem ser rejeitadas
com erro estrutural determinístico. A forma exata do erro é decisão de
implementação futura — esta ADR registra apenas a proibição normativa.

---

### D5 — Multiplicidade de grupos irmãos

Em qualquer nível de grupo permitido, o container pai pode declarar **múltiplos
grupos irmãos** em `elementos[]`.

O sistema não limita cada nível a um único grupo. Dois ou mais grupos podem
coexistir como filhos diretos do mesmo container — seja do corpo raiz, seja de
um grupo de nível 1 ou de um grupo de nível 2.

Esta ADR não introduz cardinalidade máxima para quantidade de grupos irmãos.

---

### D6 — Multiplicidade de elementos funcionais dentro de grupos

Um grupo — incluindo um grupo do nível 3 — **pode** conter mais de um elemento
funcional.

Não existe regra geral de "exatamente um elemento funcional por grupo". A
multiplicidade de filhos funcionais dentro de um grupo é permitida conforme a
estrutura declarada.

As regras já existentes aplicáveis por container permanecem em vigor:

- ordem declarada em `elementos[]`;
- filhos diretos como unidade de contagem da distribuição;
- arranjo declarado pelo container;
- distribuição declarada pelo container;
- associação posicional dos valores de distribuição.

Estas regras não são reescritas nem aplicadas aos contratos nesta etapa.

---

### D7 — Remoção da cardinalidade global de um dashboard por tela

A restrição normativa "zero ou um dashboard por tela" é **removida** como regra
global do tipo `dashboard`.

A nova regra é:

- uma tela pode conter mais de um elemento do tipo `dashboard`;
- dashboards podem aparecer em diferentes grupos da mesma tela;
- não existe limite global de um único dashboard por tela;
- esta ADR não cria cardinalidade máxima substituta.

Esta decisão altera **somente** a cardinalidade global do tipo. Ela não altera:

- a natureza passiva do `dashboard`;
- as regras de navegação (dashboard não é navegável por `[✥]`);
- o comportamento do indicador `[✥]`;
- o arranjo e a distribuição;
- a estrutura interna própria de cada instância de `dashboard`;
- qualquer regra específica de uma tela concreta que, declarativamente, possua
  apenas um `dashboard`.

A restrição "zero ou um por tela" existia como restrição documental herdada da
especificação da tela raiz do Orquestrador e não deve permanecer como política
universal do tipo.

---

## Exemplos estruturais

Os exemplos abaixo são conceituais. Não representam schema JSON completo nem
campos que não estejam confirmados nas autoridades normativas ativas.

### Válido — três níveis de grupos com múltiplos elementos funcionais no nível 3

```text
corpo
└── grupo nível 1
    ├── elemento funcional
    └── grupo nível 2
        ├── elemento funcional
        └── grupo nível 3
            ├── elemento funcional
            └── elemento funcional
```

Os dois elementos funcionais dentro do grupo do nível 3 **não** formam nível
de grupo 4. Conforme D1 e D3, somente um nó estrutural `grupo` declarado como
filho cria um novo nível de grupo.

### Válido — múltiplos grupos irmãos

```text
corpo
├── grupo nível 1
├── grupo nível 1
└── elemento funcional
```

Dois grupos irmãos no nível 1 são válidos. O corpo raiz pode conter múltiplos
grupos irmãos e elementos funcionais misturados, conforme D5.

### Válido — múltiplos dashboards em grupos distintos

```text
corpo
├── grupo nível 1
│   └── dashboard
└── grupo nível 1
    └── dashboard
```

Dois dashboards em grupos distintos da mesma tela são válidos. A restrição
global de "zero ou um dashboard por tela" foi removida pela D7. A ADR remove
apenas a cardinalidade global — não define layout específico nem impõe que
toda tela deva conter múltiplos dashboards.

### Inválido — grupo no nível 4

```text
corpo
└── grupo nível 1
    └── grupo nível 2
        └── grupo nível 3
            └── grupo nível 4    ← inválido
```

Um grupo filho de um grupo do nível 3 estaria no nível 4 e é estruturalmente
inválido conforme D4.

---

## Consequências documentais

As consequências abaixo são identificadas para aplicação futura. Nenhum
documento é alterado por esta ADR.

### Consequências normativas a serem aplicadas

- **Revisão da definição e contagem de níveis**: substituir formulações que
  tratam toda lista `elementos[]` como criadora de novo nível hierárquico pela
  definição de nível de grupo conforme D1.
- **Explicitação do limite como aninhamento de grupos**: deixar inequívoco nos
  contratos e na nomenclatura que o limite de três níveis refere-se ao
  aninhamento de nós estruturais `grupo`, não a toda lista `elementos[]`.
- **Explicitação de que grupo do nível 3 pode conter elementos funcionais**:
  registrar explicitamente que elementos funcionais dentro de um grupo do nível
  3 não constituem nível 4 (D3).
- **Proibição de grupo no nível 4**: reforçar nos contratos que `grupo` filho
  de grupo do nível 3 é inválido (D4).
- **Remoção de "zero ou um dashboard por tela" como regra global**: remover
  ou rever a formulação de cardinalidade universal do tipo `dashboard` nos
  contratos afetados (D7).
- **Revisão dos exemplos normativos**: atualizar exemplos que limitem a
  presença de elementos funcionais em grupos profundos ou que afirmem
  cardinalidade única de dashboard por tela.
- **Revisão das validações estruturais descritas nos contratos**: identificar
  e ajustar descrições de validação que rejeitem grupo aninhado, múltiplos
  filhos em grupo ou múltiplos dashboards, quando divergentes desta ADR.

### Consequências futuras para loader, modelo, renderizador e testes

As consequências abaixo são identificadas como decorrência desta ADR para
futuros ciclos de implementação. Esta ADR **não implementa** nenhuma delas.

- **Loader**: a validação atual rejeita grupos aninhados e múltiplos filhos
  em grupos (`tela/loader.py:269–306`). Deverá ser revisada para distinguir
  profundidade de grupos de profundidade genérica de listas, e para rejeitar
  apenas grupo no nível 4 ou superior, não qualquer aninhamento.
- **Modelo**: a representação interna não preserva árvore de grupos além de
  um nível interno (`tela/modelo.py:127–133`). Deverá suportar a árvore
  integral de até três níveis de grupos.
- **Renderizador**: não percorre a estrutura recursivamente além do primeiro
  nível de grupos (`tela/renderizador.py:1107–1117`). Deverá expandir grupos
  recursivamente até o nível 3, aplicando arranjo e distribuição por container.
- **Testes**: os testes atuais esperam rejeição de grupos aninhados e de mais
  de um filho em grupo, sem autoridade ativa superior para essas restrições
  (`tela/teste_loader.py:645–681`). Deverão ser revistos para cobrir estruturas
  de dois e três níveis de grupos, múltiplos grupos irmãos, múltiplos elementos
  funcionais por grupo e múltiplos dashboards na mesma tela.
- **Testes de nível 4 inválido**: cobertura executável específica para
  rejeição de grupo no nível 4 está ausente e deverá ser criada em ciclo
  futuro.

---

## Compatibilidade e preservações

Esta ADR preserva integralmente:

- A taxonomia fechada de tipos funcionais: `console`, `lancador`, `dashboard`
  (ADR-0010; ADR-0006).
- A lista plana de elementos no corpo raiz permanece válida como caso do nível
  1 sem grupos.
- `grupo` como nó estrutural sem borda, moldura, título, conteúdo, ação, chip,
  origem de dados nem `tela_destino` (ADR-0015).
- Arranjo e distribuição declarados por container (`corpo` ou `grupo`) (ADR-0015).
- Ausência de `distribuicao` como construção orientada pelo conteúdo, sem
  equivalência ao modo `igual` (ADR-0018).
- Regras de arredondamento determinístico (maiores restos, empate pela ordem
  declarada) (ADR-0015).
- Distribuição conta somente filhos diretos do container; não conta netos nem
  descendentes (ADR-0015).
- Associação posicional dos valores de distribuição pela ordem declarada
  em `elementos[]` (ADR-0018).
- `dashboard` continua passivo e não navegável por `[✥]` (ADR-0010).
- `lancador` continua não navegável por `[✥]` (ADR-0005).
- `console` continua o único tipo navegável por `[✥]` (ADR-0010).
- JSONs de tela existentes continuam carregáveis: telas com lista plana e
  telas com um único grupo de nível 1 permanecem válidas.
- Qualquer regra específica de uma tela concreta que, declarativamente,
  possua apenas um `dashboard` permanece válida como declaração daquela
  tela — esta ADR remove a restrição global, não impõe multiplicidade.

---

## Relação com ADR-0007

A ADR-0007 declarou que telas de processamento devem ser especificadas como
composição de tipos existentes e registrou, em seu ponto de decisão 3, que a
composição de uma tela de processamento envolve "um ou mais `console`, zero ou
um `dashboard`, e chips específicos" (`ADR-0007:71`). O exemplo da seção
"Composição conceitual" da mesma ADR repete essa formulação: "zero ou um
`dashboard` — por exemplo estado agregado do processo" (`ADR-0007:123`).

A D7 desta ADR remove "zero ou um dashboard por tela" como regra global do
tipo `dashboard`. Essa remoção **supera parcialmente** a ADR-0007
exclusivamente nas formulações de cardinalidade "zero ou um `dashboard`":
telas de processamento passam a admitir mais de um `dashboard`, exatamente
como qualquer outra tela.

A formulação "zero ou um `dashboard`" da ADR-0007 é uma restrição normativa
para a categoria de tela de processamento — não a declaração de configuração
de uma tela concreta individual. Por isso, ela não se enquadra na preservação
de "qualquer regra específica de uma tela concreta que, declarativamente,
possua apenas um `dashboard`" (D7, última alínea). A D7 remove a restrição
global do tipo; a ADR-0007 estabelecia uma restrição da categoria. Ambas
operam no mesmo plano normativo de cardinalidade. A D7 prevalece.

A ADR-0007 permanece vigente em todos os demais pontos:

- tela de processamento não é quarto tipo de corpo (decisão 1 da ADR-0007);
- a taxonomia fechada `console`, `lancador`, `dashboard` permanece;
- `console` representa a região interativa/navegável da tela de processamento;
- `dashboard` representa a saída passiva formatada;
- `lancador` não é usado para representar processamento;
- chips específicos pertencem à `barra_de_menus`, não ao corpo;
- as regras de `[✥]` permanecem inalteradas.

A futura etapa de aplicação documental deverá revisar na ADR-0007:

- o ponto de decisão 3 (`ADR-0007:71`), que contém "zero ou um `dashboard`":
  substituir por formulação sem cardinalidade máxima imposta para a categoria
  de tela de processamento;
- o exemplo da seção "Composição conceitual" (`ADR-0007:123`), que repete
  "zero ou um `dashboard`": substituir por formulação sem cardinalidade máxima.

Não é necessária nova decisão do usuário para esta revisão. A D7 é inequívoca
como remoção de cardinalidade global do tipo, incluindo a formulação da
ADR-0007 para a categoria de tela de processamento.

---

## Relação com ADR-0010

A ADR-0010 declarou `dashboard` como elemento funcional do corpo, submetido
ao mecanismo geral de composição declarativa, e removeu `posicao_dashboard`
como eixo separado. Esta ADR **é coerente** com a ADR-0010: ao remover a
cardinalidade global de "zero ou um por tela", reforça que o dashboard segue
o mesmo mecanismo de composição que `console` e `lancador`, sem restrição
especial por tipo.

A ADR-0010 permanece vigente em todos os demais pontos.

---

## Relação com ADR-0015

A ADR-0015 formalizou o corpo como árvore de composição, definiu `grupo`
como nó estrutural, estabeleceu o conceito de nível e fixou a profundidade
máxima em três. A ADR-0019 **substitui parcialmente** a regra de contagem de
profundidade da ADR-0015, exclusivamente no critério usado para contar os
níveis: a contagem passa a ser feita exclusivamente por níveis de grupos,
excluindo elementos funcionais da contagem. A ADR-0015 permanece vigente em
todos os demais pontos — arranjo por container, distribuição por container,
arredondamento, preenchimento de área alocada e demais decisões.

Esta ADR **não reescreve** nem **cancela** a ADR-0015. Substitui somente o
critério de contagem de profundidade, sem alterar os demais pontos.

---

## Relação com ADR-0018

A ADR-0018 formalizou a semântica da ausência de `distribuicao` e a semântica
da distribuição explícita. Esta ADR **não altera** a ADR-0018. As regras de
ausência de distribuição como construção orientada pelo conteúdo e de
distribuição explícita como repartição da área útil permanecem integralmente
válidas para todos os containers, incluindo grupos dos três níveis permitidos.

---

## Pendência documental da ADR-0018

O levantamento identificou que o índice `docs/adr/INDICE_ADR.md` lista a
ADR-0018 como `aceita`, enquanto o arquivo da ADR-0018 declara internamente
`status: proposta` (`RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md:297–304`,
achado ACH-008). Essa divergência é pendência documental separada, identificada
pelo levantamento, e não é objeto desta ADR.

---

## Documentos que precisarão ser atualizados na etapa futura de aplicação

| Documento | Ponto a revisar |
|---|---|
| `docs/contratos/contrato_composicao_corpo.md` | Revisar a definição de nível para contar por grupos (D1); explicitar que elementos funcionais em grupo do nível 3 não formam nível 4 (D3); registrar proibição de grupo no nível 4 (D4); remover "zero ou um dashboard por tela" como regra global (D7); revisar exemplos |
| `docs/contratos/contrato_tela_json.md` | Alinhar a descrição de profundidade hierárquica à contagem por níveis de grupos; atualizar referências à cardinalidade de dashboard |
| `docs/contratos/contrato_json_tela_minima.md` | Revisar a formulação de grupos aninhados e os exemplos de hierarquia; alinhar à nova contagem de níveis |
| `docs/NOMENCLATURA.md` | Revisão normativa substantiva (não apenas terminológica): remover ou corrigir as formulações que contam o corpo raiz como nível 0; remover ou corrigir a afirmação "Nível 3 proibido"; remover ou corrigir a rejeição de estruturas com profundidade ≥ 3 segundo a contagem antiga; alinhar à contagem exclusiva por níveis de grupos e à permissão de três níveis de grupos (D1, D2) |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Revisar o ponto de decisão 3 (`ADR-0007:71`), que contém "zero ou um `dashboard`", e o exemplo da seção "Composição conceitual" (`ADR-0007:123`), que repete essa cardinalidade: substituir ambos por formulação sem cardinalidade máxima imposta para a categoria de tela de processamento (D7) |
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0019 |

---

## Itens fora de escopo desta ADR

Declarados explicitamente fora de escopo:

- textos exatos de mensagens de erro para estruturas inválidas;
- implementação de qualquer validação, loader, modelo ou renderizador;
- alteração de testes;
- cardinalidade máxima de grupos irmãos por nível;
- cardinalidade mínima de grupos por tela;
- obrigação de existirem todos os três níveis em toda tela;
- obrigação de todo grupo conter outro grupo;
- cardinalidade mínima ou máxima geral de elementos funcionais por grupo;
- política de mistura entre grupos e elementos funcionais além do que já
  existe nas autoridades ativas;
- nova regra de distribuição, arredondamento, dimensão ou overflow;
- novo formato de erro;
- nova estrutura interna de `dashboard`;
- limites específicos por tipo funcional;
- comportamento de renderização;
- estratégia de implementação;
- correção da divergência de status da ADR-0018;
- atualização do índice de ADRs;
- alteração de qualquer contrato ou nomenclatura;
- criação de handoff;
- preparação de commit.

---

## Critérios para futura aplicação documental

A aplicação documental futura precisa:

- substituir nos contratos a formulação de nível como "toda lista `elementos[]`
  cria um novo nível" pela contagem exclusiva por níveis de grupos (D1);
- registrar explicitamente que elementos funcionais dentro de um grupo do
  nível 3 não constituem nível 4 (D3);
- registrar que `grupo` filho de grupo do nível 3 é inválido (D4);
- remover ou rever a formulação "zero ou um dashboard por tela" como regra
  global (D7);
- revisar na ADR-0007 o ponto de decisão 3 e o exemplo da seção "Composição
  conceitual" que contêm "zero ou um `dashboard`", removendo a cardinalidade
  máxima imposta para a categoria de tela de processamento (D7);
- preservar a natureza passiva e não navegável do `dashboard`;
- preservar a compatibilidade retroativa das telas existentes;
- não introduzir cardinalidade máxima de grupos irmãos;
- não alterar as regras de distribuição, arranjo ou arredondamento;
- atualizar os exemplos normativos que hoje limitam profundidade funcional ou
  cardinalidade de dashboard;
- registrar ADR-0019 no índice.

---

## Critérios que permitirão criar o handoff subsequente

Um handoff para implementação dos três níveis de grupos poderá ser criado após:

- QA desta ADR;
- aplicação documental confirmada (contratos e nomenclatura refletem D1–D7);
- QA da aplicação documental;
- os contratos afetados não contradizerem a nova regra de contagem de níveis;
- os contratos afetados não registrarem "zero ou um dashboard por tela" como
  regra global;
- o levantamento de implementação do handoff identificar o escopo mínimo de
  alterações no loader, modelo, renderizador e testes necessário para suportar
  a profundidade definida por esta ADR.

---

## Ausência de implementação nesta etapa

Esta ADR não altera código, testes, JSON de tela, contratos, nomenclatura,
handoffs, relatórios, índice de ADRs, estado operacional ou histórico Git.
Cria somente este arquivo. Toda aplicação é diferida para a etapa de aplicação
documental subsequente, após QA desta ADR.
