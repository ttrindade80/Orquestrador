---
name: ADR-0022-ponto-entrada-tela-inicial-orquestrador
description: Define o futuro ponto de entrada real do Orquestrador, a identidade da tela inicial real, sua composicao estrutural minima, a separacao da demonstracao e os limites do acesso inicial a estilos
metadata:
  type: adr
  status: aceita
  data: "2026-07-14"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/adr/INDICE_ADR.md
    - docs/INDICE.md
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_json_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_json_cabecalho.md
  handoffs_bloqueados: []
---

# ADR-0022 - Ponto de entrada e tela inicial real do Orquestrador

## Status

aceita

## Data

2026-07-14

---

## Contexto

A ADR-0021 separou a demonstracao, o produto real e a politica de caminhos.
Ela estabeleceu:

- `tela/` como motor compartilhado;
- `demo/` como futura aplicacao demonstrativa;
- `config/telas/demo/` como raiz exclusiva das telas demonstrativas;
- `config/telas/` como raiz das telas do produto real;
- identidade demonstrativa `demo`;
- ausencia de wrappers, aliases e fallback entre demonstracao e produto;
- reutilizacao do mesmo loader, modelo e renderizador;
- preservacao de `config/estilo.json`;
- reserva da futura tela real e de `orquestrador.py` para decisao documental
  posterior.

A aplicacao documental da ADR-0021 foi aprovada em:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
```

com status formal:

```text
ADR_APPLICATION_APPROVED
```

No estado fisico anterior a implementacao futura:

- `orquestrador.py` ainda nao existe;
- `demo/` ainda nao existe;
- `config/telas/demo/` ainda nao existe;
- `config/telas/orquestrador.json` ainda representa a demonstracao atual;
- as movimentacoes fisicas decididas pela ADR-0021 ainda nao foram executadas;
- nenhuma implementacao fisica e autorizada por esta ADR.

## Problema

Depois da separacao estrutural definida pela ADR-0021, ainda faltava registrar
qual sera o ponto de entrada real do Orquestrador, qual identidade pertence a
tela inicial real, quais elementos estruturais minimos essa tela tera e como
ela se distingue da demonstracao.

Tambem faltava registrar a presenca inicial do acesso a estilos sem antecipar
a tela funcional de estilos, troca de borda, troca de envelope de chips,
persistencia de selecao de estilo ou qualquer navegacao para destino ainda
inexistente.

## Forcas e restricoes

Esta ADR registra apenas decisoes ja tomadas pelo usuario.

Restricoes normativas:

- nao implementar;
- nao escolher mecanismo tecnico;
- nao criar schema novo;
- nao definir API concreta de selecao de raiz declarativa;
- nao definir binding, navegacao ou integracao ainda nao decididos;
- nao alterar codigo, JSON, contratos, indices ou configuracoes;
- nao reabrir a ADR-0021;
- nao introduzir alias entre `orquestrador` e `demo`;
- nao compartilhar implicitamente o mesmo JSON entre produto e demonstracao;
- nao definir protocolo de integracao com o Pipeline;
- nao resolver `destino_minimo` nem `grupo_minimo`.

## Decisao

Ficam registradas as seguintes decisoes:

- o ponto de entrada principal do produto real sera `orquestrador.py`, na raiz;
- `orquestrador.py` sera ponto de entrada do Orquestrador real, nao da
  demonstracao;
- a tela inicial declarativa real sera `config/telas/orquestrador.json`;
- o identificador da tela real sera `orquestrador`;
- a identidade `orquestrador` pertence exclusivamente ao produto real;
- a demonstracao preservara a identidade `demo` em sua propria raiz;
- o envelope da tela real tera `cabecalho`, `corpo` e `barra_de_menus`;
- o corpo inicial tera os elementos `console` e `dashboard`, ambos presentes e
  sem entradas iniciais de conteudo;
- a barra minima da tela real declarara `Esc`, `?` e acesso a estilos;
- a tela funcional de estilos nao pertence a este ciclo;
- o motor compartilhado em `tela/` sera reutilizado.

## Ponto de entrada real

O ponto de entrada principal do produto real sera:

```text
orquestrador.py
```

Ele ficara diretamente na raiz do repositorio.

Esse arquivo sera o ponto de entrada do Orquestrador real. Ele nao sera ponto
de entrada da demonstracao.

O ponto de entrada real devera reutilizar o motor compartilhado existente em:

```text
tela/
```

Esta ADR nao decide:

- assinatura de `main`;
- argumentos de linha de comando;
- classes;
- funcoes auxiliares;
- mecanismo de import;
- tratamento de excecoes;
- protocolo de comunicacao com o Pipeline;
- execucao assincrona;
- ciclo de vida completo da aplicacao.

## Identidade da tela inicial

A tela inicial real sera identificada por:

```json
"id": "orquestrador"
```

Essa identidade pertence exclusivamente ao produto real.

Nao havera alias entre:

```text
orquestrador
demo
```

O ponto de entrada `orquestrador.py` devera iniciar explicitamente pela tela
real `orquestrador`.

## Raiz declarativa do produto

A raiz declarativa do produto real sera:

```text
config/telas/
```

A tela inicial real sera:

```text
config/telas/orquestrador.json
```

O nome base do arquivo e o campo `id` deverao coincidir, preservando os
contratos ativos de JSON de tela.

Esta ADR nao define a API concreta, parametro, classe ou funcao usada para
selecionar essa raiz.

## Envelope da tela

A tela real inicial tera o envelope macro ja contratado:

```text
cabecalho
corpo
barra_de_menus
```

Esse envelope deve continuar compativel com:

- modelo declarativo por tela;
- contrato minimo do JSON de tela;
- motor compartilhado;
- composicao hierarquica documentada;
- regras atuais de `barra_de_menus`;
- regras atuais de `console` e `dashboard`.

Esta ADR nao cria schema novo.

## Corpo inicial

O corpo da tela real sera composto por:

```text
console
dashboard
```

Ambos os elementos deverao estar presentes como elementos estruturais do corpo.

O `console` comecara sem entradas de conteudo.

O `dashboard` comecara sem entradas de conteudo.

## Semantica de conteudo vazio

Nesta ADR, "sem entradas" significa ausencia de dados instanciados para
exibicao inicial.

Essa decisao distingue:

```text
elemento presente
conteudo inicial vazio
```

Ela nao significa:

- remover o elemento estrutural;
- criar conteudo ficticio;
- criar placeholder textual nao decidido;
- criar dados de demonstracao;
- copiar dados atuais da tela demonstrativa;
- definir integracao com o Pipeline;
- decidir schema futuro de entrada;
- decidir politica futura de atualizacao dos dados.

O contrato de `console` ja admite `itens: []` no envelope minimo. O contrato
de `dashboard` ja admite conteudo de reserva sem binding como envelope minimo.
A futura implementacao devera usar somente formas compativeis com esses
contratos ou registrar bloqueio documental antes de implementar.

## Ausencia de dados demonstrativos

A futura tela real:

```text
config/telas/orquestrador.json
```

nao deve herdar dados demonstrativos atualmente presentes na tela que sera
migrada para:

```text
config/telas/demo/demo.json
```

Dados, titulos, textos, entradas ou conteudos que existam apenas para
demonstrar dashboard, console, lancador ou telas de catalogo nao pertencem a
tela real inicial.

Fica decidido que:

- a demonstracao preservara seus proprios dados em sua raiz;
- o produto real comecara sem dados demonstrativos;
- nao havera compartilhamento implicito do mesmo JSON;
- a tela real e a tela demonstrativa serao arquivos distintos.

Esta ADR nao enumera quais campos concretos deverao ser removidos do JSON
atual. Essa enumeracao pertence ao handoff de aplicacao/implementacao.

## Cabecalho

A tela real tera `cabecalho` declarativo.

Os contratos ativos de cabecalho exigem `titulo` e `descricao` como campos da
secao `cabecalho`; `titulo` deve ser string nao vazia, e `descricao` deve
estar presente.

Esta ADR nao define os valores concretos de:

- titulo;
- descricao;
- textos institucionais;
- versao;
- nome do Pipeline exibido;
- estado de conexao;
- indicadores dinamicos;
- conteudo operacional.

Antes da implementacao da tela real, os valores concretos obrigatorios do
cabecalho deverao estar definidos por autoridade documental suficiente ou
registrados no handoff quando houver decisao do usuario. Esta ADR nao preenche
esses valores por suposicao.

## Barra minima

A barra da tela real devera declarar, no minimo:

```text
Esc
?
Estilos
```

A grafia, chip, tecla, texto, acao, regra de existencia, regra de ativo e
forma de exibicao de cada item deverao respeitar os contratos ativos de
`barra_de_menus` e `chip`.

Se `Esc` e `?` ja tiverem representacao canonica documentada, a futura
implementacao devera preserva-la.

Esta ADR nao inventa atalhos literais adicionais, bindings ou acoes concretas.

## Limite funcional do acesso a estilos

O item `Estilos` devera estar visivel desde a tela inicial real.

A tela funcional de estilos sera implementada em ciclo posterior.

Portanto, nesta decisao:

- a presenca declarativa do item `Estilos` pertence a tela inicial;
- a implementacao da tela destino de estilos nao pertence a este ciclo;
- troca de borda nao pertence a este ciclo;
- troca de envelope dos chips nao pertence a este ciclo;
- catalogo completo de formatos como `[A]`, `-A-` e demais opcoes nao pertence
  a este ciclo;
- persistencia da selecao de estilo nao pertence a este ciclo.

A futura aplicacao nao deve criar navegacao invalida para destino inexistente.

Enquanto a tela funcional correspondente nao existir, o item `Estilos` devera
ser inicialmente declarativo e nao navegavel, caso essa forma seja admitida
pelos contratos ativos. Se, no momento da aplicacao, a autoridade documental
vigente exigir que todo item visivel seja acionavel por `acao` ou
`tela_destino` existente e nao permitir item declarativo sem acao, a aplicacao
devera parar com `BLOCKED_USER_DECISION`.

Esta ADR nao define:

- arquivo da futura tela de estilos;
- ID da futura tela de estilos;
- atalho;
- binding;
- acao temporaria;
- mensagem de indisponibilidade;
- fallback para a demonstracao.

## Reutilizacao do motor

`demo.py` e `orquestrador.py` deverao reutilizar o mesmo motor compartilhado.

As diferencas entre demonstracao e produto serao determinadas por:

- ponto de entrada;
- raiz declarativa selecionada;
- tela inicial;
- configuracoes declarativas;
- integracoes especificas do produto quando forem futuramente decididas.

Fica proibido:

- copiar o loader para `orquestrador.py`;
- copiar o renderizador;
- manter versoes divergentes do modelo;
- criar regras exclusivas equivalentes para a mesma composicao declarativa.

Uma capacidade visual ja implementada e contratada podera ser testada primeiro
pela demonstracao e posteriormente declarada em uma tela do produto sem
reescrever o motor.

## Relacao com a demonstracao

A demonstracao e o produto real terao identidades, pontos de entrada e raizes
declarativas distintos:

```text
demonstracao:
  ponto de entrada: demo.py
  raiz declarativa: config/telas/demo/
  identidade inicial: demo

produto real:
  ponto de entrada: orquestrador.py
  raiz declarativa: config/telas/
  identidade inicial: orquestrador
```

Nao havera:

- alias entre `demo` e `orquestrador`;
- fallback silencioso entre as duas raizes;
- compartilhamento implicito do mesmo JSON;
- duplicacao de loader, modelo ou renderizador.

## Relacao com o Pipeline

Esta ADR prepara a identidade do produto real, mas nao define a integracao
concreta com o Pipeline.

Continuam nao decididos:

- protocolo;
- canal de comunicacao;
- processo pai ou filho;
- arquivos de troca;
- eventos;
- polling;
- mensagens;
- comandos;
- schemas de entrada;
- schemas de saida;
- tratamento de falhas;
- encerramento coordenado.

`orquestrador.py` sera o ponto de entrada real preparado para integracao futura,
mas essa integracao dependera de contrato e ciclo proprios.

## Consequencias positivas

- A identidade do produto real fica separada da identidade demonstrativa.
- `orquestrador.py` passa a ter reserva documental como ponto de entrada real.
- `config/telas/orquestrador.json` passa a ter reserva documental como tela
  real.
- A tela inicial real fica definida sem herdar dados demonstrativos.
- A reutilizacao do motor compartilhado fica explicita.
- A futura integracao com o Pipeline fica preparada sem ser antecipada.
- O acesso inicial a estilos fica visivel sem forcar a tela funcional de
  estilos neste ciclo.

## Consequencias negativas e custos

- A aplicacao futura tera que separar fisicamente a tela demonstrativa atual da
  tela real.
- A suite e os comandos documentados deverao comprovar identidade carregada,
  raiz declarativa e ausencia de dados demonstrativos, nao apenas codigo de
  saida zero.
- O cabecalho real ainda exige valores concretos antes da implementacao.
- O item `Estilos` pode exigir decisao adicional se os contratos vigentes no
  momento da aplicacao nao permitirem item visivel inicialmente nao navegavel.
- A implementacao futura devera atualizar varios documentos e testes no mesmo
  ciclo ou dividir handoffs para preservar auditabilidade.

## Compatibilidade com ADRs anteriores

### ADR-0008

Preserva o modelo de configuracao declarativa por tela. A tela real sera uma
tela declarada por JSON proprio, sem hardcoding de composicao no renderer.

### ADR-0009

Preserva a regra de caminho e formato de JSON de tela sob a politica atualizada
pela ADR-0021: produto real em `config/telas/<id>.json` e demonstracao em
`config/telas/demo/<id>.json`.

### ADR-0010

Preserva a composicao hierarquica do corpo. `console` e `dashboard` sao
elementos do corpo, nao secoes raiz novas.

### ADR-0012

Preserva a barra declarativa por tela. A barra minima desta tela e decisao da
instancia `orquestrador`, nao lista global injetada pelo renderer.

### ADR-0014

Preserva os termos especificos da distribuicao horizontal da `barra_de_menus`.
Esta ADR nao muda layout responsivo de chips.

### ADR-0015

Preserva a composicao hierarquica e a distribuicao por container. Esta ADR nao
cria novo comportamento estrutural de corpo.

### ADR-0018

Preserva a semantica de ausencia de `distribuicao`. Esta ADR nao define vetor
concreto de distribuicao para a tela real.

### ADR-0019

Preserva profundidade, multiplicidade e cardinalidade de dashboard. A presenca
de um `dashboard` inicial nao reintroduz limite global de um dashboard por tela.

### ADR-0020

Preserva a matriz de grupos com coordenadas explicitas. Esta ADR nao exige
`grupo` nem `matriz` para a tela inicial real.

### ADR-0021

Depende da separacao estrutural definida pela ADR-0021.

Esta ADR:

- usa `config/telas/` como raiz do produto;
- preserva `config/telas/demo/` como raiz exclusiva da demonstracao;
- reutiliza `tela/` como motor compartilhado;
- nao reabre a politica sem aliases ou fallback;
- nao altera a organizacao de `config/layouts/` e `config/elementos/`;
- preserva `config/estilo.json`;
- nao implementa a tela de estilos.

## Documentos afetados

Esta ADR identifica documentos que deverao ser avaliados em sua futura
aplicacao. Nenhum deles e alterado nesta etapa.

Documentos minimos:

```text
docs/adr/INDICE_ADR.md
docs/INDICE.md
docs/NOMENCLATURA.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_cabecalho.md
```

Documentos adicionais com relacao material comprovada pelos contratos ativos:

```text
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
```

## Criterios para aplicacao

A aplicacao documental desta ADR so estara completa quando:

1. `orquestrador.py` estiver normativamente definido como ponto de entrada
   real, sem especificar implementacao;
2. `config/telas/orquestrador.json` estiver normativamente reservada a tela
   real;
3. a identidade `orquestrador` estiver distinta de `demo`;
4. o corpo inicial estiver definido com `console` e `dashboard` presentes,
   ambos sem entradas;
5. a barra minima estiver definida com `Esc`, `?` e acesso a estilos;
6. a ausencia de dados demonstrativos estiver explicita;
7. o item de estilos nao criar navegacao invalida antes da tela futura;
8. a reutilizacao do motor compartilhado estiver explicita;
9. a integracao concreta com Pipeline continuar fora de escopo;
10. a implementacao fisica continuar reservada ao handoff;
11. nao houver contradicoes ativas com a ADR-0021;
12. as pendencias `destino_minimo` e `grupo_minimo` continuarem separadas.

## Demonstracao operacional futura

A futura implementacao desta decisao devera oferecer uma forma reproduzivel de
comprovar que:

- `orquestrador.py` iniciou a tela real;
- a identidade carregada foi `orquestrador`;
- a raiz usada foi `config/telas/`;
- a tela demonstrativa `demo` nao foi carregada;
- o `console` esta estruturalmente presente e sem entradas;
- o `dashboard` esta estruturalmente presente e sem entradas;
- a barra apresenta os itens obrigatorios;
- nao foram exibidos dados demonstrativos;
- o motor compartilhado foi reutilizado.

Codigo de saida zero, isoladamente, nao prova esses itens.

Esta ADR nao decide fixture, comando exato nem metodo de smoke test. Esses
detalhes pertencem ao handoff, desde que confirmem semanticamente a identidade
carregada.

## Itens fora de escopo

Esta ADR nao decide nem implementa:

- migracao fisica de `tela/demo.py` para `demo/demo.py`;
- movimentacao fisica dos JSON demonstrativos;
- movimentacao dos arquivos gerais de configuracao;
- criacao fisica de `orquestrador.py`;
- criacao fisica de `config/telas/orquestrador.json`;
- valor concreto do titulo e da descricao do cabecalho sem autoridade;
- schema de integracao com Pipeline;
- protocolo de comunicacao;
- dados reais de console;
- dados reais de dashboard;
- tela funcional de estilos;
- ID ou arquivo da tela de estilos;
- troca de borda;
- troca de envelope de chip;
- persistencia de estilo;
- correcao de `destino_minimo`;
- correcao de `grupo_minimo`;
- testes;
- demonstracao;
- handoff;
- implementacao;
- commit.

## Pendencias preservadas

As pendencias de preenchimento de:

```text
destino_minimo
grupo_minimo
```

continuam fora desta ADR.

Esta ADR nao diagnostica, corrige nem relaciona automaticamente essas pendencias
a tela real. Elas exigirao levantamento focal reproduzivel.

Tambem permanecem pendentes para decisao futura:

- valores concretos do `titulo` e da `descricao` do cabecalho real;
- forma concreta de declarar `Estilos` sem navegacao invalida enquanto a tela
  funcional de estilos nao existir;
- metodo de demonstracao operacional da identidade carregada.

## Condicoes de bloqueio

A futura aplicacao desta ADR devera parar com:

```text
BLOCKED_USER_DECISION
```

quando qualquer uma das condicoes abaixo ocorrer:

- contratos vigentes exigirem acao ou `tela_destino` para todo item da barra e
  nao permitirem o item de estilos inicialmente nao navegavel;
- titulo ou descricao concretos forem obrigatorios para implementar a tela real
  e ainda nao houver decisao documental suficiente sobre seus valores;
- `console` sem entradas for incompatibilizado por schema ativo posterior;
- `dashboard` sem entradas for incompatibilizado por schema ativo posterior;
- houver contradicao entre a ADR-0021 e contratos ativos;
- a decisao exigir escolher protocolo de integracao;
- qualquer lacuna exigir inventar comportamento.

Formato de bloqueio esperado:

```yaml
documento:
secao_ou_regra:
contradicao:
decisao_adicional_necessaria:
```

## Relacao com o futuro handoff

Depois da aprovacao e aplicacao desta ADR, devera ser avaliado se os itens
abaixo cabem em um unico handoff coeso e auditavel:

- migracao estrutural da ADR-0021;
- criacao de `orquestrador.py`;
- criacao da tela real;
- atualizacao integral da suite;
- demonstracao operacional.

Se a lista nominal de arquivos, testes, comandos e criterios ficar excessiva,
os handoffs deverao ser divididos.

Esta ADR nao define antecipadamente o numero final de handoffs.

## Controle de alteracoes

```text
2026-07-14: Criacao da ADR para registrar ponto de entrada real, tela inicial
real, separacao da demonstracao, barra minima e limites do acesso a estilos.
```
