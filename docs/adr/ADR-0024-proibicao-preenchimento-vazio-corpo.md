---
name: ADR-0024-proibicao-preenchimento-vazio-corpo
description: Proibe que o corpo ocupe espaco proprio na exibicao; toda area disponivel do corpo deve ser preenchida por elemento visual (console, dashboard ou lancador); substitui parcialmente ADR-0013 e ADR-0018 no ponto do preenchimento externo vazio
metadata:
  type: adr
  status: aceita
  data: 2026-07-15
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/NOMENCLATURA.md
  handoffs_bloqueados: []
---

# ADR-0024 — Proibição de preenchimento vazio externo do corpo

## Status

`aceita`

## Data

2026-07-15

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0024 |
| Título | Proibição de preenchimento vazio externo do corpo |
| Status | aceita |
| Data | 2026-07-15 |
| Origem | Decisão explícita do usuário pós-levantamento H-0030 |
| Substitui parcialmente | ADR-0013 (cláusula 4) e ADR-0018 (D2), nos pontos do preenchimento externo vazio |

---

## 2. Contexto

Após a conclusão do ciclo H-0030 e do levantamento de revisões futuras registrado em
`docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`, foram identificados dois casos
concretos — `destino_minimo` e `grupo_minimo` — onde linhas físicas vazias de largura
total aparecem entre o último elemento visual do corpo e a `barra_de_menus`.

O levantamento (pontos 4 e 5 do relatório) comprovou que essas linhas não pertencem ao
conteúdo interno de nenhum elemento visual: não são padding interno do dashboard, não são
espaçamento normativo de borda, não são linhas da `barra_de_menus`. São preenchimento
externo inserido pelo renderer para completar a altura do corpo quando não há
`corpo.distribuicao` declarada.

Esse comportamento é autorizado explicitamente pela ADR-0013 (cláusula 4: "o renderer
deve preencher o espaço restante com linhas em branco") e pela ADR-0018 (D2: "o espaço
vertical excedente pode permanecer como preenchimento externo do corpo"). Está reproduzido
em `docs/contratos/contrato_composicao_corpo.md` seção 5.7 e em
`docs/contratos/contrato_tela_json.md` seção 8.

A decisão do usuário — registrada na seção 3 — proíbe esse comportamento de forma
normativa e substitui as autorizações existentes.

Esta ADR é normativa. Ela não implementa código, não altera testes, não altera contratos,
não altera JSONs de tela e não cria handoff. Define exclusivamente a norma a ser aplicada
em etapa posterior.

---

## 3. Problema comprovado

O levantamento executável do ponto 4 e do ponto 5 do relatório
`docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md` confirmou as seguintes evidências:

### `destino_minimo`

Arquivo: `config/telas/demo/destino_minimo.json`

Identidade comprovada pelo levantamento:

- `raw_id = destino_minimo`, `modelo_id = destino_minimo`
- `cabecalho.titulo = Destino Minimo`
- `corpo.arranjo = sobreposto` (alias transicional de `vertical`)
- `modelo.corpo.distribuicao = None`
- Único filho direto: `dashboard_teste`, tipo `dashboard`, título `Teste`

Evidência executável:

| Dimensão | Linhas do dashboard `Teste` | Linha inicial da `barra_de_menus` | Linhas externas vazias |
|---|---|---|---|
| 42×20 | 3–5 | 17 | 6 a 16 (11 linhas) |
| 80×30 | 3–5 | 27 | 6 a 26 (21 linhas) |

As linhas externas são de largura total e não pertencem a nenhum elemento visual.
O preenchimento cresce com a dimensão do terminal.

### `grupo_minimo`

Arquivo: `config/telas/demo/grupo_minimo.json`

Identidade comprovada pelo levantamento:

- `raw_id = grupo_minimo`, `modelo_id = grupo_minimo`
- `cabecalho.titulo = Grupo Minimo`
- `corpo.arranjo = vertical`
- `modelo.corpo.distribuicao = None`
- Filho direto do corpo: `grupo_principal`, tipo `grupo`, arranjo `vertical`, sem `distribuicao`
- Filho interno do grupo: `dashboard_conteudo`, tipo `dashboard`, título `Conteudo`

**Nota de identidade:** O dashboard presente em `grupo_minimo` é `Conteudo`
(id: `dashboard_conteudo`). A menção anterior a um dashboard `TESTE` nesta tela
não foi confirmada pelo levantamento e está incorreta.

Evidência executável:

| Dimensão | Linhas do dashboard `Conteudo` | Linha inicial da `barra_de_menus` | Linhas externas vazias |
|---|---|---|---|
| 42×20 | 3–5 | 17 | 6 a 16 (11 linhas) |
| 80×30 | 3–5 | 27 | 6 a 26 (21 linhas) |

As linhas externas são de largura total e não pertencem nem ao dashboard nem ao
`grupo_principal`. O preenchimento cresce com a dimensão do terminal.

Em ambas as telas, a origem do preenchimento é o renderer — confirmada de forma
independente pelo levantamento.

---

## 4. Decisão explícita do usuário

> **É expressamente proibido que o corpo ocupe espaço próprio na exibição.
> Toda a área disponível do corpo deve ser preenchida por um elemento visual:
> `console`, `dashboard` ou `lancador`.**

As declarações abaixo registram, sem alterar o sentido, os aspectos normativos
dessa decisão:

**D1 — O corpo é região de composição, não elemento visual.**
O corpo não é capaz de ocupar linhas, colunas ou células por si mesmo. A área
atribuída ao corpo deve ser integralmente ocupada pelos elementos visuais que
ele contém.

**D2 — Linhas ou áreas vazias inseridas exclusivamente como preenchimento externo
do corpo são proibidas.**
O espaço atribuído ao corpo não pode ser ocupado por conteúdo gerado pelo renderer
sem pertencer à moldura de um elemento visual.

**D3 — Toda área física disponível entre `cabecalho` e `barra_de_menus` deve
pertencer visualmente a um `console`, `dashboard` ou `lancador`.**
Não existe área excedente legítima que permaneça exclusivamente sob o corpo.

**D4 — Um `grupo` ou outro container estrutural não conta como elemento visual
capaz de justificar área vazia.**
`grupo` não tem borda visual própria, não tem conteúdo visual próprio e não
constitui ocupação visual. A presença de `grupo` não satisfaz a obrigação de
ocupação por elemento visual.

**D5 — O espaço administrado por um grupo deve resultar em ocupação por seus
descendentes visuais.**
Um `grupo` não pode acumular área vazia que não pertença a nenhum dos seus
descendentes funcionais.

**D6 — A ausência de `distribuicao` não pode autorizar preenchimento externo vazio
do corpo.**
A construção orientada pelo conteúdo preservada pela ADR-0018 (D2) continua válida
para a disposição dos elementos pelo conteúdo natural. O que esta decisão proíbe é o
espaço residual vazio que permanece fora de qualquer elemento visual após essa
disposição.

**D7 — Regras anteriores que determinam ou permitem linhas em branco externas para
completar a altura do corpo devem ser substituídas na aplicação futura desta ADR.**
A autorização da ADR-0013 (cláusula 4) e a permissividade da ADR-0018 (D2) sobre
preenchimento externo são conflitantes com esta decisão.

**D8 — Bordas, conteúdo interno, padding normativo e espaços internos pertencentes
ao próprio elemento não são "espaço ocupado pelo corpo".**
A proibição alcança exclusivamente a área externa que não pertence a nenhum elemento
visual — as linhas físicas de largura total inseridas pelo renderer fora de qualquer
caixa de elemento.

**D9 — A regra vale independentemente da dimensão do terminal ou da quantidade de
área excedente.**
Não existe limiar de tamanho abaixo do qual a proibição deixa de se aplicar.

---

## 5. Definição de "espaço próprio do corpo"

Para fins desta ADR, "espaço próprio do corpo" ou "preenchimento externo vazio do corpo"
é:

> Todo espaço físico (linhas de largura total, colunas vazias ou área bidimensional)
> existente entre os elementos visuais do corpo e as regiões fixas da tela (`cabecalho`,
> `barra_de_menus`) que não pertence à moldura, ao conteúdo interno, ao padding
> normativo ou ao espaçamento interno de nenhum `console`, `dashboard` ou `lancador`.

Esse espaço é atribuível exclusivamente ao renderer ou ao container em que os elementos
estão inseridos. Sua existência visível viola o invariante desta ADR.

---

## 6. Elementos visuais admitidos

A área disponível do corpo deve ser preenchida por elementos visuais dos seguintes tipos:

| Tipo | Natureza |
|---|---|
| `console` | Container interativo e navegável genérico |
| `dashboard` | Saída passiva formatada |
| `lancador` | Elemento de navegação com chips |

A lista é fechada: `grupo` não é elemento visual admitido. Tipos funcionais fora desta
lista não existem no sistema atual — extensões exigem ADR.

---

## 7. Distinções normativas

### 7.1 Espaço externo do corpo

Espaço externo do corpo é a área física entre o final da ocupação dos elementos visuais
e a `barra_de_menus` (ou o `cabecalho`, conforme o eixo). É precisamente o que esta ADR
proíbe. Nas telas `destino_minimo` e `grupo_minimo`, as linhas 6 a 16 (em 42×20) e 6 a
26 (em 80×30) identificadas pelo levantamento são exemplos concretos desse espaço proibido.

### 7.2 Container estrutural

Um `grupo` é um container estrutural que redistribui área entre seus filhos. Conforme
`docs/contratos/contrato_composicao_corpo.md` seção 3.3:

- não tem borda própria;
- não tem moldura visual;
- não tem título visual próprio;
- não tem conteúdo próprio;
- recebe área do container pai e redistribui entre seus filhos diretos.

A área de um `grupo` deve resultar integralmente em ocupação pelos seus descendentes
visuais. O `grupo` em si não constitui ocupação visual e não pode ser tratado como
elemento capaz de justificar área vazia.

### 7.3 Espaço interno pertencente a um elemento

Espaço interno de um elemento é a área pertencente à sua própria moldura:

- bordas (linhas de borda superior, inferior, laterais);
- padding normativo (linha em branco entre borda e conteúdo, conforme seção 4.6 do
  `contrato_composicao_corpo.md`);
- linhas em branco de preenchimento de área alocada quando há `distribuicao` explícita
  (ADR-0018, D4) — espaço que fica **dentro** da moldura do elemento.

Esse espaço não é "espaço externo do corpo" e não é atingido pela proibição desta ADR.
A proibição alcança apenas o espaço que está **fora** de toda moldura de elemento visual.

---

## 8. Aplicação conceitual a `destino_minimo`

**Tela:** `config/telas/demo/destino_minimo.json`
**Elemento visual:** dashboard `Teste` (`id: dashboard_teste`, tipo `dashboard`)
**Estrutura:** corpo com `arranjo: "sobreposto"` (alias transicional de `vertical`),
`corpo.distribuicao` ausente.

**Estado atual — não conforme com esta ADR:**
O espaço entre a base do dashboard `Teste` e a `barra_de_menus` é preenchido por linhas
físicas de largura total inseridas pelo renderer. Esse espaço é externo ao dashboard e
pertence ao corpo — não a nenhum elemento visual. O comportamento está comprovado pelo
levantamento para as dimensões 42×20 e 80×30, crescendo com o terminal.

**Consequência normativa desta ADR:**
O espaço entre o dashboard `Teste` e a `barra_de_menus` não pode continuar sendo
preenchido por linhas externas do corpo.

Pela regra DA-01 (seção 21), o dashboard `Teste` é o único descendente visual do corpo
nesta tela. Por cardinalidade unitária, ele deverá ocupar integralmente toda a área
disponível, mesmo sem `distribuicao` declarada. Nenhuma sobra poderá permanecer entre
ele e a `barra_de_menus`.

---

## 9. Aplicação conceitual a `grupo_minimo`

**Tela:** `config/telas/demo/grupo_minimo.json`
**Elemento visual:** dashboard `Conteudo` (`id: dashboard_conteudo`, tipo `dashboard`)
**Container estrutural:** `grupo_principal` (`id: grupo_principal`, tipo `grupo`,
arranjo `vertical`, `distribuicao` ausente)
**Estrutura:** corpo com `arranjo: "vertical"`, `corpo.distribuicao` ausente;
`grupo_principal` com `distribuicao` ausente.

**Identidade correta confirmada:** O dashboard presente em `grupo_minimo` é `Conteudo`
(id: `dashboard_conteudo`), contido em `grupo_principal`. Não existe dashboard `TESTE`
em `grupo_minimo`. A menção anterior a esse nome não foi confirmada pelo levantamento
e está incorreta.

**Estado atual — não conforme com esta ADR:**
O espaço entre a base do dashboard `Conteudo` e a `barra_de_menus` é preenchido por
linhas físicas de largura total. Esse espaço não pertence ao dashboard nem ao
`grupo_principal` — é preenchimento externo do corpo. O comportamento está comprovado
pelo levantamento para as dimensões 42×20 e 80×30.

**Consequência normativa desta ADR:**
O espaço entre o dashboard `Conteudo` e a `barra_de_menus` não pode continuar sendo
preenchido por linhas externas do corpo ou do grupo.

Pela regra DA-03 (seção 21), `grupo_principal` é container estrutural: toda a área que
lhe for atribuída deve ser repassada ao seu descendente visual. Pela regra DA-01
(seção 21), `dashboard_conteudo` é o único descendente visual aplicável do grupo — por
cardinalidade unitária, ele deverá ocupar integralmente essa área, mesmo sem
`distribuicao` declarada. Nenhuma sobra poderá permanecer entre o descendente visual e
a `barra_de_menus`.

---

## 10. Relação com ADR-0013

A ADR-0013 permanece vigente nos pontos não conflitantes:

- A definição da `altura_disponivel` como região entre `cabecalho` e `barra_de_menus`
  é preservada.
- A obrigação do corpo de ocupar a altura disponível é preservada — esta ADR reafirma
  a obrigação, mas exige que a ocupação seja feita por elementos visuais.
- A distinção entre `corpo.arranjo = "vertical"` (composição) e
  `ocupacao_vertical_terminal` (preenchimento de altura) é preservada.
- A responsabilidade do renderer de garantir a ocupação é preservada.

**Ponto conflitante — substituído por esta ADR:**
A ADR-0013, cláusula 4, determina: "quando o conteúdo funcional do corpo não ocupar
toda a altura disponível, o renderer deve preencher o espaço restante com linhas em
branco." A presente ADR proíbe esse preenchimento externo vazio — a área não coberta por
elementos visuais não pode ser preenchida pelo renderer com linhas em branco externas.

A cláusula 4 da ADR-0013 é conflitante com a decisão desta ADR e deverá ser substituída
na aplicação documental futura.

A ADR-0013 não é reescrita por esta ADR. Registra-se apenas a substituição normativa do
ponto conflitante (D7).

---

## 11. Relação com ADR-0018

A ADR-0018 permanece vigente nos pontos não conflitantes:

- A distinção entre arranjo e distribuição (D1) é preservada.
- A construção orientada pelo conteúdo na ausência de `distribuicao` (D2) é preservada
  quanto à disposição dos elementos — cada elemento usa sua dimensão natural.
- A semântica de distribuição explícita — área alocada, preenchimento interno das
  molduras (D3, D4) — é preservada.
- Os modos `igual`, `percentual` e `fracao` são preservados.

**Ponto conflitante — substituído por esta ADR:**
A ADR-0018, D2, afirma: "o espaço vertical excedente pode permanecer como preenchimento
externo do corpo, conforme o comportamento de ocupação já existente (ADR-0013)." A
presente ADR proíbe esse preenchimento externo vazio. A permissividade de D2 é
conflitante com a decisão desta ADR.

A proibição desta ADR aplica-se independentemente da presença ou ausência de
`distribuicao`: mesmo quando não há distribuição declarada, a área excedente não pode
permanecer como preenchimento externo vazio do corpo.

A ADR-0018 não é reescrita por esta ADR. Registra-se apenas a substituição normativa do
ponto conflitante (D7).

---

## 12. Regras anteriores substituídas ou a revisar

As seguintes formulações normativas são conflitantes com esta ADR e deverão ser
substituídas na aplicação documental futura:

| Documento | Trecho conflitante | Natureza do conflito |
|---|---|---|
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | Cláusula 4: "quando o conteúdo funcional do corpo não ocupar toda a altura disponível, o renderer deve preencher o espaço restante com linhas em branco" | Autoriza preenchimento externo vazio — proibido por esta ADR |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | D2: "o espaço vertical excedente pode permanecer como preenchimento externo do corpo, conforme o comportamento de ocupação já existente (ADR-0013)" | Permite preenchimento externo vazio — proibido por esta ADR |
| `docs/contratos/contrato_composicao_corpo.md` | Seção 5.7: "a sobra no eixo do arranjo pode permanecer como preenchimento externo do container, conforme o mecanismo de ocupação já existente (ADR-0013)" | Repete a permissividade conflitante |
| `docs/contratos/contrato_composicao_corpo.md` | Seção 4.7: "O corpo deve poder ocupar a altura disponível com preenchimento de linhas em branco adicionadas pelo renderer quando o conteúdo declarado for menor" | Deve ser revisto para distinguir preenchimento interno de elemento (admitido) de preenchimento externo do corpo (proibido) |
| `docs/contratos/contrato_tela_json.md` | Seção 8: "a sobra permanece como preenchimento externo, conforme a ocupação vertical da ADR-0013" | Conflitante com a proibição de preenchimento externo vazio |
| `docs/contratos/contrato_tela_json.md` | Seção 9: "o corpo deve preencher a área vertical disponível entre `cabecalho` e `barra_de_menus`, com preenchimento de linhas em branco pelo renderer quando o conteúdo declarado for menor" | Deve ser revisto para que o preenchimento seja por elemento visual, não por linhas externas do corpo |

Testes e fixtures que verificam a presença de linhas vazias externas em `destino_minimo`
e `grupo_minimo` como comportamento esperado também precisarão ser revisados, mas essa
revisão pertence à implementação futura pelo H-0033.

---

## 13. Consequências para contratos e nomenclatura

*Nenhum documento é alterado por esta ADR. As consequências abaixo são pendências
de aplicação futura.*

**`docs/contratos/contrato_composicao_corpo.md`:**
- Seção 4.7 (ocupação vertical): rever para proibir preenchimento externo vazio;
  exigir que toda área do corpo pertença a elemento visual.
- Seção 5.7 (ausência de `distribuicao`): rever para remover a afirmação de que a
  sobra "pode permanecer como preenchimento externo do container".

**`docs/contratos/contrato_tela_json.md`:**
- Seções 8 e 9: rever para alinhar com a proibição; substituir "preenchimento de
  linhas em branco pelo renderer" por exigência de que toda área pertença a elemento
  visual.

**`docs/NOMENCLATURA.md`:**
- Verificar e rever quaisquer formulações que autorizem o corpo a reter área vazia
  não pertencente a elemento visual.

**`docs/adr/INDICE_ADR.md`:**
- Registrar ADR-0024.

---

## 14. Consequências futuras para renderer, testes e fixtures

*Esta seção é prospectiva — nenhuma implementação ocorre por esta ADR. A implementação
será conduzida pelo handoff H-0033 (ver seção 22).*

**Renderer (`tela/renderizador.py`):**
- O bloco de preenchimento externo identificado pelo levantamento em
  `tela/renderizador.py` linhas 1315–1360 (bloco que insere linhas físicas de largura
  total entre o último elemento do corpo e a `barra_de_menus` quando `altura` é
  fornecida e não há `distribuicao` vertical explícita) deverá ser revisado.
- O novo comportamento deverá garantir que toda linha entre `cabecalho` e
  `barra_de_menus` pertença à moldura de um elemento visual. O mecanismo exato
  é regido pelas regras DA-01 a DA-04 (seção 21).
- O renderer não deve gerar linhas físicas de largura total que não pertençam a
  nenhuma caixa de elemento visual.
- O renderer deverá rejeitar explicitamente composições que violem o invariante de
  ocupação visual integral, conforme DA-04 (seção 21).

**Testes (`tela/teste_renderizador.py`):**
- Os testes que preservam `destino_minimo` sem distribuição com preenchimento externo
  (identificados pelo levantamento nas linhas 5754–5768) e os testes de `grupo_minimo`
  (linhas 5721–5751) precisarão ser revisados.
- Novos testes devem verificar que nenhuma linha externa ao corpo existe entre os
  elementos visuais e a `barra_de_menus`.
- Devem ser adicionados testes para múltiplos elementos sem `distribuicao` (DA-02) e
  para a rejeição explícita de composições impossíveis (DA-04).
- Os critérios de aceite observáveis desta ADR (seção 20) devem ser usados como base
  para os novos testes.

**Fixtures e snapshots:**
- Snapshots que capturaram a saída com linhas externas vazias como comportamento
  esperado precisarão ser recriados após a implementação.

**Configurações JSON de telas de teste:**
- Todos os JSONs existentes de telas de teste deverão ser inventariados e revisados
  conforme o requisito normativo da seção 22.

---

## 15. Compatibilidade

**Telas com exatamente um elemento visual e sem `corpo.distribuicao`** — como
`destino_minimo` e `grupo_minimo` — aplicam a regra DA-01 (seção 21): o elemento único
ocupa integralmente a área disponível por cardinalidade unitária. O comportamento atual
de preenchimento externo vazio é não conforme e deverá ser corrigido na implementação
do H-0033. A construção orientada pelo conteúdo (ADR-0018, D2) é preservada para a
disposição dos elementos pelo conteúdo natural; a regra DA-01 determina que nenhuma
sobra pode permanecer como área do corpo.

**Telas com múltiplos elementos e `corpo.distribuicao` explícita** (`igual`, `percentual`
ou `fracao`) em que a distribuição garante que toda a área disponível é alocada aos
filhos visuais (conforme ADR-0018, D3, D4 e seção 5.9 do `contrato_composicao_corpo.md`)
já possuem comportamento compatível com esta ADR nesse ponto — a sobra fica **dentro**
das molduras dos elementos, não externamente.

**Telas com múltiplos elementos no mesmo eixo e sem `corpo.distribuicao`** configuram
composição inválida sob a regra DA-02 (seção 21): a declaração de `distribuicao` é
obrigatória quando dois ou mais elementos disputam espaço no mesmo eixo. A configuração
deverá ser rejeitada explicitamente conforme DA-04 (seção 21).

**Grupos e containers estruturais** devem repassar toda a área atribuída aos seus
descendentes visuais, conforme DA-03 (seção 21). A regra DA-01 se aplica dentro do grupo
quando há exatamente um descendente visual; a regra DA-02 se aplica quando há múltiplos
descendentes disputando o mesmo eixo.

Nenhum JSON de tela existente é alterado por esta ADR.

---

## 16. Documentos afetados

### 16.1 Aplicação documental futura

Documentos normativos que necessitarão de aplicação futura da decisão desta ADR:

| Documento | Ação necessária |
|---|---|
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | Revisar cláusula 4 (proibir preenchimento externo; exigir elemento visual) |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | Revisar D2 (remover permissividade do preenchimento externo vazio) |
| `docs/contratos/contrato_composicao_corpo.md` | Revisar seções 4.7 e 5.7; registrar regras DA-01 a DA-04 |
| `docs/contratos/contrato_tela_json.md` | Revisar seções 8 e 9; registrar invalidade de múltiplos elementos sem distribuição |
| `docs/NOMENCLATURA.md` | Revisar formulações permissivas sobre preenchimento externo; registrar DA-01 a DA-04 |
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0024 |

### 16.2 Implementação futura pelo H-0033

Artefatos técnicos que serão alterados exclusivamente na implementação do H-0033:

| Artefato | Ação necessária |
|---|---|
| `tela/renderizador.py` | Remover bloco de preenchimento externo vazio (linhas 1315–1360 conforme levantamento); implementar DA-01 a DA-04 |
| `tela/teste_renderizador.py` | Revisar expectativas de testes de `destino_minimo` e `grupo_minimo`; adicionar casos para DA-02 e DA-04 |
| Fixtures e snapshots | Recriar após implementação |
| Configurações JSON de telas de teste | Inventariar todos os JSONs; atualizar incompatíveis; preservar e registrar compatíveis (ver seção 22) |
| Demonstração real | Executar em mais de uma dimensão de terminal |
| Relatório de implementação | Apresentar inventário completo, classificação e justificativa por artefato |

---

## 17. Itens fora de escopo

Os seguintes itens não são decididos por esta ADR:

- **Distribuição implícita de qualquer tipo** (`igual`, `fracao`, `percentual`).
  Não autorizada por esta ADR. A distribuição continua exigindo declaração explícita
  conforme ADR-0018. A remoção do preenchimento externo não autoriza automaticamente
  o renderer a criar distribuição implícita.
- **Alteração automática de configurações declarativas.** Não autorizada. Alterações de
  `distribuicao` pertencem ao `tela.json` de cada tela.
- **Novos tipos de elementos visuais.** Não introduzidos.
- **Novas regras de altura mínima por tipo de elemento.** Não estabelecidas.
- **Algoritmo específico do renderer** para garantir a cobertura visual integral.
  Não especificado. Os detalhes técnicos pertencem à implementação do H-0033.
- **Implementação de qualquer código, teste, fixture ou JSON.** Nenhuma implementação
  ocorre por esta ADR.
- **Reabertura ou reclassificação do H-0030.** O ciclo está encerrado e não é reaberto.
- **Detalhes técnicos da rejeição explícita (DA-04):** o tipo nominal da exceção, a
  função ou camada que primeiro detectará a invalidade, a estrutura interna da mensagem
  de erro e a organização interna das validações. Esses detalhes pertencem à
  implementação do H-0033 e não alteram a semântica normativa de rejeição explícita
  registrada em DA-04 (seção 21).

---

## 18. Critérios para futura aplicação documental

A aplicação documental futura precisa:

- Identificar e substituir toda formulação que autorize ou permita preenchimento externo
  vazio do corpo (ver seção 12).
- Preservar a distinção entre espaço interno dos elementos (admitido) e espaço externo
  do corpo (proibido) (ver seção 7).
- Registrar explicitamente que `grupo` não constitui elemento visual para fins de
  ocupação visual integral.
- Registrar as regras DA-01 a DA-04 (seção 21) nos documentos normativos aplicáveis.
- Preservar a semântica de distribuição explícita (ADR-0018, D3, D4) — quando há
  distribuição, o preenchimento interno das molduras é admitido e permanece válido.
- Não introduzir mecanismo de distribuição implícita não autorizado por ADR existente.
- Não alterar a construção orientada pelo conteúdo além do ponto conflitante do
  preenchimento externo.
- Preservar a diferença semântica entre ausência de distribuição e `distribuicao: igual`.
- Preservar integralmente todos os pontos não conflitantes da ADR-0013 e da ADR-0018.

---

## 19. Critérios para futura implementação

A implementação futura (H-0033) deverá:

- Garantir que o renderer não gere linhas físicas de largura total entre o último
  elemento visual e a `barra_de_menus`.
- Garantir que toda linha renderizada entre `cabecalho` e `barra_de_menus` pertença
  à moldura de um elemento visual (`console`, `dashboard` ou `lancador`).
- Revisar o bloco de preenchimento externo identificado em `tela/renderizador.py`
  (linhas 1315–1360 conforme o levantamento), sem introduzir distribuição implícita
  como efeito colateral.
- Implementar a regra DA-01 (seção 21): o descendente visual único ocupa integralmente
  a área disponível, mesmo sem `distribuicao` declarada.
- Implementar a regra DA-02 (seção 21): rejeitar composições com múltiplos elementos
  disputando o mesmo eixo sem `distribuicao` declarada.
- Implementar a regra DA-03 (seção 21): repassar a área de grupos e containers
  estruturais aos seus descendentes visuais.
- Implementar a regra DA-04 (seção 21): rejeitar explicitamente composições cujo
  invariante não puder ser satisfeito — emitir erro identificável, sem fallback
  silencioso, sem distribuição implícita, sem alteração automática do JSON.
- Realizar inventário nominal completo de todos os JSONs de telas de teste e cenários
  permanentes equivalentes, conforme os requisitos da seção 22.
- Verificar a conformidade nas telas `destino_minimo` e `grupo_minimo` com as
  identidades corretas dos elementos (seções 8 e 9 e AC-03 e AC-04 da seção 20).

---

## 20. Critérios observáveis de aceite

A futura implementação deverá conseguir provar semanticamente que:

**AC-01 — Ausência de linhas externas:**
Não existem linhas ou células externas atribuíveis somente ao corpo. Toda linha
renderizada entre `cabecalho` e `barra_de_menus` pertence à moldura de um elemento
visual.

**AC-02 — Cobertura total por elementos visuais:**
Toda área renderizada do corpo pertence a um `console`, `dashboard` ou `lancador`.
O renderer não produz área vazia não coberta por nenhum desses três tipos.

**AC-03 — `destino_minimo` conforme:**
`destino_minimo` não apresenta área externa vazia entre o dashboard `Teste` e a
`barra_de_menus`. A identidade correta é: dashboard com título `Teste`,
`id: dashboard_teste`, único elemento visual em `config/telas/demo/destino_minimo.json`.

**AC-04 — `grupo_minimo` conforme:**
`grupo_minimo` não apresenta área externa vazia entre o dashboard `Conteudo` e a
`barra_de_menus`. A identidade correta é: dashboard com título `Conteudo`,
`id: dashboard_conteudo`, filho de `grupo_principal`, em
`config/telas/demo/grupo_minimo.json`.

**AC-05 — Identidades corretas confirmadas:**
Testes não confundem o dashboard `Teste` de `destino_minimo` com o dashboard `Conteudo`
de `grupo_minimo`. A menção a dashboard `TESTE` em `grupo_minimo` não está presente em
nenhum teste ou expectativa.

**AC-06 — Código de saída zero não é prova suficiente:**
O aceite exige verificação da composição visual linha a linha — não apenas ausência de
exceção ou código de saída zero.

**AC-07 — Verificação em múltiplas dimensões:**
A conformidade deve ser verificada em pelo menos duas dimensões distintas de terminal
(por exemplo, 42×20 e 80×30), pois o comportamento atual de preenchimento varia com
a dimensão.

**AC-08 — Independência das expectativas:**
Testes materiais devem usar expectativas independentes da própria saída observada do
comportamento antigo. Não é admitido capturar a saída atual e usá-la como expectativa
de referência para o novo comportamento.

**AC-09 — Descendente visual único ocupa integralmente a área:**
Quando um corpo ou container possuir exatamente um descendente visual aplicável, a
implementação comprova que esse elemento ocupa toda a área disponível — sem sobra
externa, sem `distribuicao` declarada obrigatória para esse caso.

**AC-10 — Múltiplos elementos sem distribuição são rejeitados:**
Quando dois ou mais elementos disputam o mesmo eixo sem `distribuicao` declarada, a
composição é rejeitada explicitamente antes ou durante a renderização. O erro é
identificável e nenhum fallback silencioso ocorre.

**AC-11 — Múltiplos elementos com distribuição válida continuam funcionando:**
Telas com `distribuicao` explícita (`igual`, `percentual` ou `fracao`) e múltiplos
elementos no mesmo eixo continuam renderizando corretamente, sem regressão.

**AC-12 — Grupos não retêm espaço próprio:**
Nenhuma área é atribuída exclusivamente a um `grupo` ou container estrutural. Toda
área de grupo é repassada aos descendentes visuais.

**AC-13 — Configurações impossíveis são rejeitadas explicitamente:**
Composições que não permitem ocupação visual integral são rejeitadas com erro
identificável. O sistema não insere área vazia, não aplica distribuição implícita,
não escolhe silenciosamente um elemento e não altera o JSON automaticamente.

**AC-14 — Ausência de fallback ou preenchimento externo silencioso:**
Nenhum caminho do renderer produz área vazia não pertencente a moldura de elemento
visual sem emitir rejeição explícita. O comportamento silencioso de fallback é
comprovadamente inexistente após a implementação.

**AC-15 — Inventário completo de JSONs de telas de teste:**
O relatório do H-0033 apresenta inventário nominal de todos os JSONs de telas de
teste, fixtures visuais e cenários permanentes equivalentes. Cada JSON é classificado
como compatível ou incompatível. Os incompatíveis são atualizados; os compatíveis são
nominalmente registrados como revisados e preservados, com justificativa por arquivo.
Nenhuma configuração histórica permanece reproduzindo a regra antiga de preenchimento
externo vazio.

**AC-16 — Validação humana observa ausência de faixas vazias externas:**
A demonstração real, executada em mais de uma dimensão de terminal, é validada por
observação humana direta. Nenhuma faixa vazia externa é visível entre os elementos
visuais e a `barra_de_menus`.

---

## 21. Decisões arquiteturais incorporadas

As políticas a seguir foram aprovadas explicitamente pelo usuário e são parte normativa
desta ADR. Elas substituem as pendências anteriormente registradas como DA-01 a DA-04.
O futuro executor do H-0033 não pode escolher ou redefinir essas políticas.

**DA-01 — Elemento visual único.**

Quando um corpo ou container possuir exatamente um descendente visual aplicável, esse
elemento deverá ocupar integralmente toda a área disponível, mesmo quando não houver
`distribuicao` declarada.

Esta regra:

- não representa `distribuicao: igual`;
- não cria uma distribuição entre múltiplos elementos;
- decorre da cardinalidade unitária;
- impede que qualquer sobra permaneça atribuída ao corpo ou ao container estrutural.

**DA-02 — Múltiplos elementos sem distribuição.**

Quando dois ou mais elementos disputarem espaço no mesmo eixo, a declaração de
`distribuicao` será obrigatória.

A ausência de `distribuicao`:

- não significa `igual`;
- não permite ao renderer escolher implicitamente quem recebe a sobra;
- não permite preenchimento externo vazio;
- torna a composição inválida quando existir área que precise ser distribuída entre
  múltiplos elementos.

A diferença semântica entre ausência de distribuição e `distribuicao: igual` é
preservada (ADR-0018, D5).

**DA-03 — Grupos e containers estruturais.**

O `grupo` continua sendo exclusivamente estrutural e não conta como elemento visual.

Toda área atribuída a um grupo ou container estrutural deve ser repassada aos seus
descendentes visuais.

Regras:

1. com exatamente um descendente visual aplicável, ele ocupa integralmente a área
   disponível (DA-01);
2. com múltiplos descendentes disputando o mesmo eixo, `distribuicao` é obrigatória
   (DA-02);
3. nenhuma linha, coluna ou célula pode permanecer atribuída exclusivamente ao grupo;
4. o grupo não pode justificar preenchimento vazio externo;
5. a ocupação visual deve ser realizada por `console`, `dashboard` ou `lancador`.

**DA-04 — Invariante impossível de satisfazer.**

Quando uma configuração não permitir que toda a área do corpo pertença visualmente a
`console`, `dashboard` ou `lancador`, a configuração será inválida.

O sistema deverá:

- rejeitar explicitamente a composição;
- interromper sua construção ou renderização;
- emitir erro identificável;
- não inserir linhas ou áreas externas vazias;
- não aplicar distribuição implícita;
- não escolher silenciosamente um elemento;
- não alterar automaticamente o JSON;
- não usar fallback silencioso.

Os seguintes detalhes técnicos pertencem à implementação do H-0033 (seção 22) e não
alteram a semântica normativa de rejeição explícita:

- o tipo nominal da exceção;
- a função ou camada que primeiro detectará a invalidade;
- a estrutura interna da mensagem de erro;
- a organização interna das validações.

---

## 22. Vinculação ao H-0033 e inventário de JSONs de telas de teste

A futura implementação desta ADR será conduzida pelo handoff **H-0033**.

O H-0033 não existe ainda. Será criado após a aprovação desta ADR e a conclusão da
aplicação documental. A numeração de handoffs é estritamente sequencial; não existe
reserva de número; atividades adiadas não preservam número reservado; não existem
sufixos por letras. O H-0033 será o próximo handoff real.

### Requisito normativo — Inventário completo de JSONs de telas de teste

O H-0033 deverá realizar inventário nominal de todos os arquivos JSON existentes
usados como configurações de telas de teste, demonstração, fixtures visuais ou
cenários permanentes equivalentes.

O inventário não poderá ficar limitado a:

- `destino_minimo.json`;
- `grupo_minimo.json`.

Todos os JSONs existentes de telas de teste deverão ser avaliados contra:

- ocupação integral da área do corpo;
- cardinalidade unitária (DA-01);
- obrigatoriedade de `distribuicao` para múltiplos elementos no mesmo eixo (DA-02);
- propagação de área por grupos (DA-03);
- invalidade de sobra externa (DA-04).

Os JSONs incompatíveis deverão ser atualizados na mesma implementação do H-0033.

JSONs avaliados como compatíveis deverão ser nominalmente registrados como revisados
e preservados.

O relatório de implementação do H-0033 deverá apresentar:

- inventário completo;
- classificação de cada JSON (compatível / incompatível);
- arquivos atualizados;
- arquivos preservados;
- justificativa por arquivo.

Não será permitido deixar configurações de teste históricas reproduzindo a regra antiga
de preenchimento externo vazio.

A atualização dos JSONs pertence à implementação do H-0033, não à aplicação documental
desta ADR. Esta ADR não inventa antecipadamente a lista real de JSONs: o H-0033 deverá
realizar a descoberta completa no estado real do repositório e converter o resultado em
lista nominal auditável.

---

## Ausência de implementação nesta etapa

Esta ADR não altera código, testes, JSON, contratos, nomenclatura, handoffs, relatórios,
índice de ADRs, estado operacional ou histórico Git. Cria somente este arquivo. Toda
aplicação é diferida para etapa posterior.
